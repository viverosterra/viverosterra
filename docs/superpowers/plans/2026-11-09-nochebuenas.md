# Página de temporada de Nochebuenas: plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** publicar `/post/nochebuenas-tampico-madero-mayoreo` con cotizador por volumen, WhatsApp, registro en Sheets y tres modos.
**Architecture:** página del build de `tools/site/`; datos en `datos.NOCHEBUENAS`; un JS sin dependencias lee esos datos de un JSON incrustado.
**Tech Stack:** Python 3 (build, unittest), JavaScript simple (`node --test`), Playwright, Google Apps Script.
**Spec:** `docs/superpowers/specs/2026-11-09-nochebuenas-temporada-design.md` manda sobre este plan.

Reglas para todo agente: trabaja solo en `~/dev/viverosterra-nochebuenas`. No hagas commit (lo hace quien coordina). No publiques. Ningún script
de navegador sale de localhost: `contexto.route("**/*", ...)` con deny por defecto. No debilites una prueba existente: si una regla
choca con una decisión del dueño, agrega una excepción acotada a esta ruta y comentada. Prohibido en la página: "gratis", "sin costo",
"garantía", "reponemos", "con IVA", "Oasis", "paraíso", "mágico", "transformar", "increíble", "espectacular", "sueño".

## Contrato de datos (`tools/site/datos.py`)

`productos` es tupla con "clave": un objeto JS reordenaría las claves numéricas.

```python
NOCHEBUENAS = {
    "ruta": "/post/nochebuenas-tampico-madero-mayoreo",
    "temporada": 2026,
    "modo": "temporada",  # "preventa" | "temporada" | "postemporada"
    "sheets_endpoint": "",  # URL del Web App de apps-script/nochebuenas-pedidos.gs
    "cortes": (1, 12, 50, 200),
    "nombres_escalon": ("Menudeo", "Mayoreo", "Mayoreo Plus", "Proyecto"),
    "productos": (
        {"clave": "5", "nombre": 'Maceta 5"', "precios": (89, 75, 69, 65)},
        {"clave": "6", "nombre": 'Maceta 6"', "precios": (139, 119, 109, 105)},
        {"clave": "7", "nombre": 'Maceta 7"', "precios": (199, 169, 155, 149)},
        {"clave": "colgante", "nombre": "Colgante", "precios": (339, 279, 259, 249)},
        {"clave": "12", "nombre": 'Macetón 12"', "precios": (1195, 995, 899, 865), "sobre_pedido": True},
    ),
    "variedades": ("Roja", "Rosa", "Jaspeada"),
    "zonas": ("Tampico", "Madero", "Altamira", "Recojo en vivero"),
    "tipos_cliente": ("Hogar", "Empresa/regalo", "Restaurante/hotel", "Comercio/plaza", "Gobierno", "Evento/posada", "Iglesia/escuela"),
    "entrega_incluida_desde": 3500,
    "preventa": {"descuento": 0.05, "hasta": "2026-11-20", "aplica_hasta_escalon": 2},
    "fecha_limite_mayoreo": "2026-11-30",
    "ultima_actualizacion": "2026-11-08",
}
```

## Contrato de fotos (`tools/site/contenido/nochebuenas_fotos.py`)

```python
FOTOS = ({"id": "...", "src": "/img/nochebuenas/x-800.webp", "srcset": "/img/nochebuenas/x-800.webp 800w, ...", "ancho": 800, "alto": 1000,
          "alt": "...", "rotulo": "...", "uso": "hero" | "galeria" | "kraft"}, ...)
```
Exactamente una con `uso == "hero"`.

## Task 1: datos y motor del cotizador

**Files:** Modify `tools/site/datos.py` (bloque NOCHEBUENAS). Create `public/js/vt-nochebuenas.js`, `public/js/tests/vt-nochebuenas.test.js`. Modify `tools/site/tests/test_datos.py`.

API pura, exportada con el patrón de `public/js/vt-medidor.js` (`module.exports` y `window.VTNochebuenas`). Sin precios en el JS: todo llega de `cfg`, el dict de arriba como JSON.

- `hoyMX(date)` → "YYYY-MM-DD" en America/Mexico_City.
- `cotizar(lineas, cfg, hoy)`; `lineas`: `[{clave, variedad, cantidad}]`. Cantidad se normaliza a entero 0–9999. Devuelve `{piezas, escalon, nombreEscalon, lineas:[{clave,nombre,variedad,cantidad,precio,subtotal,sobrePedido}], subtotal, preventa, descuento, total, ahorro, proyecto, haySobrePedido}`. Sin piezas: `escalon -1`, total 0. `descuento = Math.round(subtotal * cfg.preventa.descuento)`, si `hoy <= hasta` y `0 <= escalon <= aplica_hasta_escalon`. `total = subtotal - descuento`. `ahorro` = total a precio menudeo sin preventa − total.
- `nudge(lineas, cfg, hoy)` → `null` o `{faltan, nombre, objetivo, diferencia, ahorro, texto}`. Si faltan de 1 a 4 para el siguiente corte, suma las piezas a la última línea con cantidad > 0. `diferencia` = total objetivo − total actual. `ahorro` = objetivo a precio del escalón actual (misma preventa actual) − total objetivo.
  Texto, con `dinero`: diferencia > 0 `Te faltan 2 piezas para precio Mayoreo: por $38 más te llevas 12 y ahorras $240`; diferencia < 0 `Te falta 1 pieza para precio Proyecto: te llevas 200, pagas $731 menos y ahorras $800`; diferencia 0 `... : por el mismo total te llevas N y ahorras $Y`.
- `entrega(total, zona, cfg)` → `null` si zona "Recojo en vivero"; `{incluida:true, texto:"Entrega incluida"}`, o `{incluida:false, faltan, texto:"Te faltan $X para entrega incluida. Entrega según tu ubicación o colonia; te la cotizamos por WhatsApp."}`.
- `mensaje(cot, extras, cfg)`; `extras`: `{zona, fecha, tipo, factura}`, todas opcionales.
- `registro(cot, extras, cfg, ubicacion)` → objeto para Sheets: `{lineas, piezas, escalon, total, preventa, zona, fecha_deseada, tipo_cliente, factura, origen, utm_source, utm_medium, utm_campaign}`; `lineas` es texto con ` | `, `origen` es el pathname, `escalon` el nombre.
- `enviarRegistro(endpoint, datos, nav)`: si `endpoint` no empieza con `https://script.google.com/macros/s/`, no hace nada. Si no, `nav.sendBeacon(endpoint, JSON.stringify(datos))` dentro de try/catch; nunca lanza.

Interfaz (sección final del mismo archivo, solo si hay `document` y `[data-nb-cotizador]`): lee `cfg` de `<script type="application/json" id="nb-config">`. Una línea inicial `6"`/Roja con cantidad 1; − / + ; agregar y quitar líneas. Pinta subtotales, total, escalón, ahorro, nudge, preventa, entrega, sobre pedido y proyecto en `[data-nb-o="..."]`, con `aria-live="polite"` en el total. El botón es un `<a data-cta="nochebuenas:cotizador">`: su `href` se reescribe en cada cambio con `https://wa.me/<wa>?text=` (terra.js firma y mide los `a[href]`; así no hay bloqueo de ventanas emergentes). Sin piezas: `aria-disabled="true"` y `preventDefault`. En el `click`: `enviarRegistro` y `gtag('event','nb_whatsapp_click',{total,escalon})`, sin bloquear ni esperar. Primer cambio: `nb_cotizador_uso`; primera vez que hay nudge: `nb_nudge_visto`. `[data-nb-hasta="AAAA-MM-DD"]` se oculta si `hoy > fecha`. `[data-nb-total-barra]` muestra `Cotizar · $total`; `[data-nb-bar]` se oculta con IntersectionObserver mientras `#cotizador` está a la vista. `data-nb-modo="preventa"`: mensaje con "Quiero apartar" en vez de "Quiero cotizar".

- [ ] **Step 1: escribir la prueba que falla** en `public/js/tests/vt-nochebuenas.test.js`:

```js
const test = require('node:test');
const assert = require('node:assert');
const nb = require('../vt-nochebuenas.js');
const cfg = { temporada:2026, cortes:[1,12,50,200], nombres_escalon:['Menudeo','Mayoreo','Mayoreo Plus','Proyecto'],
  productos:[{clave:'5',nombre:'Maceta 5"',precios:[89,75,69,65]},{clave:'6',nombre:'Maceta 6"',precios:[139,119,109,105]},
    {clave:'7',nombre:'Maceta 7"',precios:[199,169,155,149]},{clave:'colgante',nombre:'Colgante',precios:[339,279,259,249]},
    {clave:'12',nombre:'Macetón 12"',precios:[1195,995,899,865],sobre_pedido:true}],
  entrega_incluida_desde:3500, preventa:{descuento:0.05,hasta:'2026-11-20',aplica_hasta_escalon:2} };
const FUERA = '2026-12-01';
const L = (clave, cantidad, variedad='Roja') => ({clave, variedad, cantidad});
const mixto = [L('6',16), L('7',4,'Jaspeada'), L('colgante',6,'Rosa')];

test('10 de 6" a menudeo, con nudge honesto', () => {
  assert.strictEqual(nb.cotizar([L('6',10)], cfg, FUERA).total, 1390);
  const n = nb.nudge([L('6',10)], cfg, FUERA);
  assert.deepStrictEqual([n.faltan,n.nombre,n.objetivo,n.diferencia,n.ahorro],[2,'Mayoreo',12,38,240]);
  assert.strictEqual(n.texto,'Te faltan 2 piezas para precio Mayoreo: por $38 más te llevas 12 y ahorras $240');
});
test('12 de 6" a mayoreo, sin nudge', () => {
  const c = nb.cotizar([L('6',12)], cfg, FUERA);
  assert.deepStrictEqual([c.total,c.nombreEscalon,c.ahorro],[1428,'Mayoreo',240]);
  assert.strictEqual(nb.nudge([L('6',12)], cfg, FUERA), null);
});
test('26 mezcladas recalculan todas las líneas', () => {
  const c = nb.cotizar(mixto, cfg, FUERA);
  assert.deepStrictEqual([c.piezas,c.total,c.nombreEscalon,c.ahorro],[26,4254,'Mayoreo',800]);
  assert.deepStrictEqual(c.lineas.map(l=>l.subtotal),[1904,676,1674]);
});
test('preventa incluye el último día y no el siguiente', () => {
  assert.deepStrictEqual((({preventa,descuento,total})=>[preventa,descuento,total])(nb.cotizar([L('6',12)],cfg,'2026-11-20')),[true,71,1357]);
  assert.strictEqual(nb.cotizar([L('6',12)],cfg,'2026-11-21').total,1428);
});
test('preventa nunca en Proyecto', () => {
  const c = nb.cotizar([L('5',200)],cfg,'2026-11-10');
  assert.deepStrictEqual([c.preventa,c.total,c.proyecto],[false,13000,true]);
});
test('nudge cuando el pedido completo sale más barato', () => {
  const n = nb.nudge([L('5',199)],cfg,FUERA);
  assert.deepStrictEqual([n.faltan,n.diferencia,n.ahorro],[1,-731,800]);
  assert.strictEqual(n.texto,'Te falta 1 pieza para precio Proyecto: te llevas 200, pagas $731 menos y ahorras $800');
});
test('nudge solo con 4 piezas o menos', () => {
  assert.strictEqual(nb.nudge([L('6',7)],cfg,FUERA),null);
  assert.strictEqual(nb.nudge([L('6',8)],cfg,FUERA).faltan,4);
});
test('pedido vacío y cantidades inválidas', () => {
  const c = nb.cotizar([L('6',-3),L('7','x')],cfg,FUERA);
  assert.deepStrictEqual([c.piezas,c.escalon,c.total],[0,-1,0]);
  assert.strictEqual(nb.nudge([L('6',0)],cfg,FUERA),null);
});
test('macetón marca sobre pedido', () => assert.ok(nb.cotizar([L('12',1)],cfg,FUERA).haySobrePedido));
test('entrega', () => {
  assert.strictEqual(nb.entrega(3500,'Altamira',cfg).texto,'Entrega incluida');
  assert.strictEqual(nb.entrega(3499,'Madero',cfg).faltan,1);
  assert.strictEqual(nb.entrega(9000,'Recojo en vivero',cfg),null);
});
test('mensaje con el formato del dueño', () => {
  const c = nb.cotizar(mixto,cfg,FUERA);
  assert.strictEqual(nb.mensaje(c,{zona:'Madero',fecha:'2026-11-28',tipo:'Restaurante/hotel',factura:true},cfg),
`Hola Viveros Terra 🌺 Quiero cotizar Nochebuenas 2026:
• 16 × Maceta 6" Roja
• 4 × Maceta 7" Jaspeada
• 6 × Colgante Rosa
Total: 26 piezas · Escalón: Mayoreo · Total estimado: $4,254
Entrega: Madero · 28 nov · Requiero factura
Tipo de cliente: Restaurante/hotel`);
});
test('mensaje indica preventa', () => assert.match(nb.mensaje(nb.cotizar([L('6',12)],cfg,'2026-11-10'),{},cfg),/Precio preventa/));
test('un endpoint inválido o una falla no rompen nada', () => {
  let n = 0; const nav = {sendBeacon(){ n++; throw new Error('x'); }};
  nb.enviarRegistro('', {}, nav); nb.enviarRegistro('https://evil.example/', {}, nav); assert.strictEqual(n,0);
  assert.doesNotThrow(()=>nb.enviarRegistro('https://script.google.com/macros/s/abc/exec',{a:1},nav)); assert.strictEqual(n,1);
});
test('hoyMX usa la hora de México', () => assert.strictEqual(nb.hoyMX(new Date('2026-11-21T03:00:00Z')),'2026-11-20'));
```

- [ ] **Step 2:** `node --test public/js/tests/vt-nochebuenas.test.js` → FALLA, módulo inexistente.
- [ ] **Step 3:** implementar y agregar `NOCHEBUENAS` a `datos.py`, con una prueba en `test_datos.py` de los cortes y los 5 productos.
- [ ] **Step 4:** `node --test public/js/tests/*.test.js` y `cd tools/site && python3 -m unittest tests.test_datos` → PASA.

## Task 2: fotos

**Files:** Create `public/img/nochebuenas/*.webp`, `tools/site/contenido/nochebuenas_fotos.py`.

Origen, solo lectura: `/Users/luisgovela/Desktop/Escritorio - Mac mini de Luis/Plantas Variedades Vivero/Fotos Plantas/Nochebuenas`.
Script en el scratchpad, no en el repo. Respeta la orientación EXIF.

- [ ] No uses `Tamanos Nochebuenas.png`. Mira cada foto recortada antes de aceptarla.
- [ ] Recorta sin personas, carro blanco, suelo sucio ni objetos ajenos; recorta las zonas crema y amarillas. Si tras el recorte no queda una composición digna, descarta la foto y dilo.
- [ ] Ajuste natural y leve de exposición y saturación. Nada generado ni clonado.
- [ ] WebP sin metadatos (EXIF/GPS), calidad 80, anchos 800 y 1600 solo si el recorte mide al menos ese ancho; nunca ampliar. Nombres descriptivos: `nochebuena-roja-...-tampico-800.webp`.
- [ ] Escribe `nochebuenas_fotos.py` con el contrato. `alt` y `rotulo` dicen solo lo que se ve; no afirmes tamaño de maceta si no se distingue. Las de bolsa kraft: `uso: "kraft"`, rótulo "Pedido de volumen listo para entregar". Hero: la mejor, solo roja, nítida.
- [ ] Entrega una hoja de contacto en el scratchpad y reporta ancho, peso y qué descartaste.

## Task 3: Google Sheets

**Files:** Create `apps-script/nochebuenas-pedidos.gs`, `apps-script/README.md`, `apps-script/tests/nochebuenas-pedidos.test.js`.

Código a entregar:

```js
const HOJA = 'Pedidos Nochebuenas 2026';
const COLUMNAS = ['fecha_hora','lineas','piezas','escalon','total','preventa','zona','fecha_deseada','tipo_cliente','factura','origen','utm_source','utm_medium','utm_campaign'];
const ESCALONES = ['Menudeo','Mayoreo','Mayoreo Plus','Proyecto'];
const ZONAS = ['','Tampico','Madero','Altamira','Recojo en vivero'];
const TIPOS = ['','Hogar','Empresa/regalo','Restaurante/hotel','Comercio/plaza','Gobierno','Evento/posada','Iglesia/escuela'];
const MAX_CUERPO = 5000, MAX_POR_MINUTO = 60;

function limpiar(valor, max) {
  const texto = String(valor == null ? '' : valor).replace(/[\r\n\t]+/g, ' ').slice(0, max);
  return /^[=+\-@]/.test(texto) ? "'" + texto : texto;
}
function numero(valor, max) {
  const n = Number(valor);
  if (!Number.isFinite(n) || n < 0 || n > max) throw new Error('numero');
  return Math.round(n);
}
function fila(d, ahora) {
  if (ESCALONES.indexOf(d.escalon) < 0 || ZONAS.indexOf(d.zona || '') < 0 || TIPOS.indexOf(d.tipo_cliente || '') < 0) throw new Error('catalogo');
  if (!/^(\d{4}-\d{2}-\d{2})?$/.test(d.fecha_deseada || '')) throw new Error('fecha');
  return [ahora, limpiar(d.lineas, 1500), numero(d.piezas, 100000), d.escalon, numero(d.total, 100000000), d.preventa ? 'sí' : 'no',
    d.zona || '', d.fecha_deseada || '', d.tipo_cliente || '', d.factura ? 'sí' : 'no',
    limpiar(d.origen, 200), limpiar(d.utm_source, 100), limpiar(d.utm_medium, 100), limpiar(d.utm_campaign, 100)];
}
function excedido() {
  const cache = CacheService.getScriptCache();
  const n = Number(cache.get('n') || 0) + 1;
  cache.put('n', String(n), 60);
  return n > MAX_POR_MINUTO;
}
function hoja() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  const h = libro.getSheetByName(HOJA) || libro.insertSheet(HOJA);
  if (h.getLastRow() === 0) h.appendRow(COLUMNAS);
  return h;
}
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    const cuerpo = e && e.postData && e.postData.contents || '';
    if (cuerpo.length > MAX_CUERPO || excedido()) return respuesta('ignorado');
    lock.waitLock(5000);
    hoja().appendRow(fila(JSON.parse(cuerpo), new Date()));
    return respuesta('ok');
  } catch (err) {
    console.error('nochebuenas', err && err.message);
    return respuesta('error');
  } finally {
    lock.releaseLock();
  }
}
function respuesta(texto) { return ContentService.createTextOutput(texto); }
```

- [ ] Prueba en node (`vm`, con stubs de `SpreadsheetApp`, `CacheService`, `LockService`, `ContentService`): fila válida con 14 columnas; fórmula en `lineas`, `origen` y UTM neutralizada; zona fuera de catálogo, JSON roto y cuerpo enorme no agregan fila; más de 60 por minuto se ignora; crea encabezados una sola vez.
- [ ] `README.md` en español llano para el dueño: crear la hoja, Extensiones → Apps Script, pegar, Implementar → Aplicación web, "Ejecutar como: yo", "Acceso: cualquier persona", copiar la URL y dársela a quien mantiene el sitio. Aclarar que registra clics de envío, no pedidos confirmados.

## Task 4: página, navegación y URL (depende de 1 y 2)

**Files:** Create `tools/site/contenido/nochebuenas.py`, `tools/site/plantillas/nochebuenas.py`, `public/css/terra-nochebuenas.css`, `tools/site/tests/test_nochebuenas.py`, `tools/site/tests/test_nochebuenas_navegador.py`, `tools/site/tests/test_terra_nochebuenas_css.py`.
Modify `generar.py` (PAGINAS, salida `post/nochebuenas-tampico-madero-mayoreo/index.html`), `paginas.py` (EXACTAS `("nochebuenas","plantas","plantas")`, y la ruta en RUTAS_SIN_BARRA), `activos.py` y `activos.json`, `partials.py` y `shell.py` (hoja por `vt-nochebuenas` en body; "Nochebuenas" en el menú y en PIE; sin "con IVA incluido" en la línea legal cuando `tipo == "nochebuenas"`), `mensajes_paginas.py`, `vercel.json`, `public/sitemap.xml`, `public/llms.txt`, `contenido/inicio.py` + `plantillas/inicio.py`, `contenido/plantas_hub.py`, y las pruebas que enumeran rutas (`test_generar.py` y las que falle).

Requisitos:
- Secciones y textos: spec §4, en ese orden. Reusa `c.portada`, `c.bloque`, `c.bloque_dos`, `c.logos`, `c.cierre`, `base.documento`, `base.jsonld`. No uses `c.garantia`. Preguntas: `<h3>` y `<p>` visibles, no `c.faq` (que usa details), con `c.faq_jsonld` para el schema. `pasos` con `c.pasos`.
- Tabla: `<table>` estática con `<caption>`, columnas Tamaño | 1–11 pzas | 12–49 | 50–199 | 200+, generada de `datos.NOCHEBUENAS`.
- Cotizador: HTML inicial real; `<script type="application/json" id="nb-config">` con el dict, `<` escapado; `wa` del número de `datos.TELEFONO_WA`; `/js/vt-nochebuenas.js` en `scripts`. El `<a>` funciona sin JS con un mensaje genérico. `<select>` o botones con `<label>`; objetivo táctil de 44 px; −/+ con `aria-label`. Fechas con `data-nb-hasta`.
- Barra fija: `[data-nb-bar]`, enlace a `#cotizador`, altura `--vt-bar-h`, fuera de `<main>` con `tras_main`; solo móvil, con `padding-bottom` en el body de esta página para no tapar el pie.
- Modos (spec §7): en `render`, según `datos.NOCHEBUENAS["modo"]`; acepta el modo como parámetro para probar los tres sin tocar `datos`. La franja de la home solo si el modo no es postemporada.
- Diseño: hoja bajo `.vt-nochebuenas`, solo tokens de terra.css, Plano + Etiqueta (`c.etiqueta` para el total si encaja); menos de 12 KB. `terra.css` no tiene presupuesto: la franja de la home reutiliza clases existentes.
- SEO y JSON-LD: spec §5. `@graph` con WebPage (`about` y `publisher` a `/#negocio`), Product × 5, FAQPage, BreadcrumbList y `dateModified`.
- `vercel.json`: quitar el redirect de esta URL; `/nochebuenas-mayoreo-tampico` y `/post/productores-de-nochebuenas-mayoreo` apuntan aquí; `https://script.google.com` en `connect-src`.
- `sitemap.xml`: `<lastmod>` = `ultima_actualizacion`. Módulo con `PARIDAD` vacío: página nueva, sin captura previa; si la suite de paridad lo exige, exclúyela con comentario.
- Hub: "Nochebuenas de temporada" en relacionados o subcategorías, según lo que haya.

- [ ] **Step 1: pruebas que fallan** en `test_nochebuenas.py`: título y descripción exactos; canonical; `index, follow`; tabla como texto con `$1,195` y `$65`; sin palabras prohibidas en el texto visible; JSON-LD parseable con 5 Product, low/high correctos, FAQ igual a lo visible, availability por modo; postemporada sin `data-nb-cotizador` ni `data-nb-bar` y con "Temporada 2026 cerrada · Gracias"; preventa con "Aparta tus Nochebuenas 2026"; `vercel.json` sin esa fuente y con los dos destinos; sitemap; `connect-src`.
- [ ] **Step 2:** correrlas → FALLAN.
- [ ] **Step 3:** implementar. `python3 tools/site/build.py` y una segunda corrida debe escribir 0.
- [ ] **Step 4:** `test_nochebuenas_navegador.py`, deny por defecto, con reloj fijo vía `context.add_init_script` si hace falta: los tres casos del dueño; − / + y agregar línea; el href del botón lleva el mensaje completo; con `sendBeacon` que lanza, el href y la navegación siguen; sin desborde en 320, 360, 768, 1440; barra visible al inicio y oculta con el cotizador a la vista; axe sin violaciones serias.
- [ ] **Step 5:** suites: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover`, `node --test public/js/tests/*.test.js`.

## Task 5: revisión y publicación (coordinador)

- [ ] Revisores independientes: diseño móvil, SEO y schema, cumplimiento de reglas del dueño, seguridad.
- [ ] Lighthouse móvil: rendimiento ≥ 85, accesibilidad ≥ 90, SEO 100.
- [ ] `/verify`, commit, merge a main, push, comprobación en vivo (200 sin redirección), limpieza del worktree, memoria y aviso.
