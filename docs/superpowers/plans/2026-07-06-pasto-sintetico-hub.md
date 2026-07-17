# Hub Nacional Pasto Sintético — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar `/pasto-sintetico` (tienda nacional con cotizador híbrido de 9 modelos), conectar las páginas locales existentes, y 2 artículos de blog answer-first — Fase 1 de la spec `docs/superpowers/specs/2026-07-06-pasto-sintetico-hub-design.md`.

**Architecture:** Sitio estático HTML+Tailwind compilado (`/css/tailwind.css`) + `/css/design-system.css` compartido. Cada página es standalone (nav/footer/estilos inline copiados de páginas hermanas). El cotizador es JS vanilla inline. Deploy = push a `main` (Vercel auto).

**Tech Stack:** HTML estático, Tailwind compilado, JS vanilla, JSON-LD, Vercel.

**Working dir:** `/Users/luisgovela/Documents/GitHub/viverosterra` (páginas en `public/`)

**Verificación estándar (usar en cada task):**
```bash
# Validez HTML (desde public/):
python3 -c "
from html.parser import HTMLParser
class V(HTMLParser):
    def error(self,m): raise Exception(m)
V().feed(open('RUTA/index.html').read()); print('HTML OK')"
```
Preview: `preview_start` name `viverosterra` (launch.json ya existe, puerto 8899, mobile 375×812). Verificar por DOM con `preview_eval` (los screenshots no scrollean en este sitio).

---

## Datos canónicos (fuente única — usar EXACTAMENTE estos valores)

```js
// 9 modelos residenciales. Precios IVA incluido $/m². t1=1-9m², t2=10-49m², rollo=50m²+
const MODELOS=[
 {id:'aruba10',  nombre:'Aruba 10',   mm:10, peso:1000, gar:5, t1:189, t2:159, rollo:139, stock:false, tag:'Decorativo · balcones y terrazas', ideal:'Espacios decorativos, terrazas pequeñas, balcones y áreas de bajo tránsito', icons:['mascotas','fuego','antibacterial','bajopeso']},
 {id:'toscana18',nombre:'Toscana 18', mm:18, peso:1000, gar:5, t1:199, t2:169, rollo:149, stock:true,  tag:'Económico · el mejor precio', ideal:'Áreas decorativas, jardines pequeños, uso residencial ligero', icons:['mascotas','fuego','antibacterial','bajopeso']},
 {id:'toscana28',nombre:'Toscana 28', mm:28, peso:1100, gar:5, t1:279, t2:229, rollo:199, stock:true, masVendido:true, tag:'Premium residencial · MÁS VENDIDO', ideal:'Jardines residenciales, terrazas, áreas de convivencia familiares', icons:['durabilidad','mascotas','ninos','transito','suavidad','fuego']},
 {id:'capri20',  nombre:'Capri 20',   mm:20, peso:1580, gar:8, t1:279, t2:239, rollo:209, stock:false, tag:'Alta densidad comercial', ideal:'Espacios comerciales, áreas de alto tránsito, jardines de uso intenso', icons:['durabilidad','mascotas','ninos','transito','suavidad','fuego']},
 {id:'irlanda25',nombre:'Irlanda 25', mm:25, peso:1400, gar:8, t1:279, t2:239, rollo:209, stock:false, tag:'Alto tránsito · niños y mascotas', ideal:'Jardines residenciales de alto tránsito con niños y mascotas', icons:['durabilidad','mascotas','ninos','transito','suavidad','fuego']},
 {id:'viena30',  nombre:'Viena 30',   mm:30, peso:1800, gar:8, t1:339, t2:279, rollo:249, stock:false, tag:'Premium natural', ideal:'Jardines premium residenciales con acabado natural realista', icons:['durabilidad','ninos','suavidad','fuego','antibacterial']},
 {id:'japones35',nombre:'Japonés 35', mm:35, peso:1800, gar:8, t1:359, t2:299, rollo:269, stock:false, tag:'Lujo · máximo realismo', ideal:'Jardines de lujo con máximo realismo estético', icons:['durabilidad','ninos','suavidad','fuego','antibacterial']},
 {id:'monaco35', nombre:'Mónaco 35',  mm:35, peso:2100, gar:8, t1:399, t2:339, rollo:299, stock:false, tag:'Premium exclusivo · hoteles', ideal:'Residencias premium, hoteles boutique, espacios de alto valor', icons:['durabilidad','ninos','suavidad','fuego','antibacterial']},
 {id:'bali35',   nombre:'Bali 35',    mm:35, peso:2100, gar:8, t1:399, t2:339, rollo:299, stock:false, tag:'Tropical premium', ideal:'Jardines exclusivos con acabado tropical premium', icons:['durabilidad','ninos','suavidad','fuego','antibacterial']},
];
// Envío ESTIMADO por rollo (o fracción) según zona. SIEMPRE con leyenda "estimado, se confirma por WhatsApp con tu C.P."
const ZONAS={
 A:{tarifa:900,  nombre:'Centro y Occidente'},
 B:{tarifa:1150, nombre:'Norte y Sur'},
 C:{tarifa:1400, nombre:'Sureste y Fronteras'},
};
const ESTADO_ZONA={
 'Aguascalientes':'A','CDMX':'A','Colima':'A','Estado de México':'A','Guanajuato':'A','Hidalgo':'A','Jalisco':'A','Michoacán':'A','Morelos':'A','Nayarit':'A','Puebla':'A','Querétaro':'A','San Luis Potosí':'A','Tlaxcala':'A','Zacatecas':'A',
 'Coahuila':'B','Durango':'B','Guerrero':'B','Nuevo León':'B','Oaxaca':'B','Sinaloa':'B','Tamaulipas':'B','Veracruz':'B',
 'Baja California':'C','Baja California Sur':'C','Campeche':'C','Chiapas':'C','Chihuahua':'C','Quintana Roo':'C','Sonora':'C','Tabasco':'C','Yucatán':'C',
};
// Reglas de negocio:
// - Mínimo nacional: 25 m². Presets del input: 25 / 50 / 100.
// - Precio/m² según m²: <10→t1 (no aplica online, min 25), 10-49→t2, >=50→rollo.
// - Rollos para envío: Math.ceil(m2/50). Envío = rollos × ZONAS[z].tarifa.
// - ENVÍO GRATIS si m2 >= 100.
// - Tamaulipas: mostrar además nota "Estás en nuestra zona — visita el showroom" + link /venta-pasto-sintetico-tampico.
// - WhatsApp: 528333268008.
// Casos de prueba del cotizador (verificar EXACTO):
//   Toscana 28, 50 m², Nuevo León → material $9,950 + envío est. $1,150 = $11,100 · ahorro vs corte $4,000
//   Toscana 18, 25 m², Jalisco    → 25×169=$4,225 + $900 = $5,125
//   Bali 35, 100 m², Yucatán      → 100×299=$29,900 + GRATIS = $29,900 (muestra "Envío GRATIS")
```

**Fotos:** usar por ahora las existentes en `/img/` (pasto-sintetico-*.webp). Cards sin foto propia del modelo usan `pasto-sintetico-textura-detalle.webp` o el gradiente fallback del design-system.

---

### Task 1: Esqueleto de `/pasto-sintetico` — head, nav, hero, footer

**Files:**
- Create: `public/pasto-sintetico/index.html`
- Referencia de patrón: `public/venta-pasto-sintetico-tampico/index.html` (head líneas 1-147, nav hasta ~línea 194, hero vt-hero línea 195+, footer al final)

- [ ] **Step 1:** Copiar `venta-pasto-sintetico-tampico/index.html` como base: `cp -r` NO — crear `public/pasto-sintetico/` y copiar el archivo. Es el patrón aprobado (hero claro vt-hero + nav + footer ya consistentes).
- [ ] **Step 2:** Reemplazar `<head>`: title `Pasto Sintético — Venta con Envío a Todo México · Viveros Terra`; meta description `Pasto sintético con envío a todo México desde $139/m². 9 modelos residenciales, precio de productor, factura CFDI. Cotiza online y recibe en 3-5 días.`; canonical `https://www.viverosterra.com/pasto-sintetico`; OG equivalentes. ELIMINAR los JSON-LD copiados (se rehacen en Task 4).
- [ ] **Step 3:** Reescribir hero vt-hero: H1 `Pasto Sintético con <span class="vt-hero__title-accent">Envío a Todo México.</span>`; subtitle "9 modelos residenciales a precio de productor. Cotiza en línea, paga fácil y recibe en 3-5 días hábiles. Factura CFDI 4.0."; badges: `📦 Envío nacional 3-5 días` / `Factura CFDI 4.0` / `+500,000 m² instalados` / accent `Desde $139/m² en rollo`; métricas: `9 modelos` / `$139 desde·m²` / `3-5 días de entrega` / `+900 clientes`. CTAs: WhatsApp (texto "Hola, quiero cotizar pasto sintético con envío a mi ciudad") y ancla `#cotizador` "Cotizar en línea ↓".
- [ ] **Step 4:** Vaciar el body entre hero y footer (las secciones viejas de venta local se eliminan; el footer se conserva). Dejar comentarios `<!-- COTIZADOR -->`, `<!-- CATALOGO -->`, `<!-- COMPARATIVA -->`, `<!-- ENVIO -->`, `<!-- DIY -->`, `<!-- FAQ -->`, `<!-- LOCAL -->` como marcadores.
- [ ] **Step 5:** Validar HTML (comando estándar) + `git add public/pasto-sintetico && git commit -m "feat(hub): esqueleto /pasto-sintetico con hero nacional"`.

### Task 2: Catálogo de 9 modelos + comparativa

**Files:** Modify: `public/pasto-sintetico/index.html` (marcadores CATALOGO y COMPARATIVA)

- [ ] **Step 1:** Insertar `<script>` con `MODELOS` (datos canónicos completos de arriba) antes de `</body>`.
- [ ] **Step 2:** Sección catálogo `<section id="modelos">`: H2 `Los 9 modelos — ¿cuál pasto es para ti?`; grid responsive (1 col móvil / 3 desktop) renderizado por JS: card = nombre + tag + stat-block (mm / peso g/m² / garantía años) + fila de íconos (emoji: 🐕 niños👶 tránsito👟 suavidad☁️ fuego🔥 antibact🛡 durab💪 según `icons`) + precio grande `desde $XXX/m² en rollo` + badges STOCK/MÁS VENDIDO + botón "Cotizar este modelo" (hace scroll a #cotizador y preselecciona el modelo).
- [ ] **Step 3:** Sección comparativa: tabla HTML estática (NO JS, para SEO/AEO) con las 9 filas: Modelo · Altura · Peso g/m² · Garantía · Precio rollo $/m² · Ideal para. Fila Toscana 28 con clase destacada. Debajo: `<p>` "A mayor altura y peso, mayor densidad, realismo y suavidad." + nota "Rollos de 2 m de ancho · 50 m² por rollo · IVA incluido".
- [ ] **Step 4:** Verificar en preview (DOM): `document.querySelectorAll('#modelos .modelo-card').length===9` y tabla con 9 `<tr>` de datos. Validar HTML. Commit `feat(hub): catálogo 9 modelos + comparativa`.

### Task 3: Cotizador híbrido

**Files:** Modify: `public/pasto-sintetico/index.html` (marcador COTIZADOR + script)

- [ ] **Step 1:** Insertar `ZONAS` y `ESTADO_ZONA` (datos canónicos) al script.
- [ ] **Step 2:** HTML `<section id="cotizador">`: (a) selector de modelo (dropdown con los 9 + precio rollo visible), (b) input m² `min=25 step=1 value=50` + presets botones 25/50/100, (c) dropdown estado (las 32 entradas de ESTADO_ZONA ordenadas alfabético), (d) caja resultado, (e) leyenda fija: `⚠️ El envío mostrado es un estimado. El costo exacto se confirma por WhatsApp con tu dirección y C.P.`, (f) 2 CTAs.
- [ ] **Step 3:** JS `calcular()`:
```js
function precioM2(m,m2){return m2>=50?m.rollo:(m2>=10?m.t2:m.t1);}
function calcular(){
  const m=MODELOS.find(x=>x.id===selModelo.value);
  let m2=Math.max(25,parseInt(inpM2.value)||25);
  const z=ESTADO_ZONA[selEstado.value];
  const pm2=precioM2(m,m2), material=pm2*m2;
  const rollos=Math.ceil(m2/50);
  const envio=m2>=100?0:ZONAS[z].tarifa*rollos;
  const total=material+envio;
  const ahorro=(m.t1-pm2)*m2; // vs precio de corte
  // pinta: $material + envío estimado (o "GRATIS 🎉") = total estimado + "Ahorras $X vs precio de corte"
  // si estado==='Tamaulipas': mostrar nota showroom + link /venta-pasto-sintetico-tampico
}
```
- [ ] **Step 4:** CTAs: `Pedir por WhatsApp` abre `https://wa.me/528333268008?text=` con mensaje URL-encoded: `Hola, quiero cotizar pasto sintético con envío:\n• Modelo: {nombre} ({mm} mm)\n• Cantidad: {m2} m²\n• Destino: {estado}\n• Total estimado: ${total} (material ${material} + envío est. ${envio})\n¿Me confirman costo de envío con mi C.P. y disponibilidad?`. `Solicitar link de pago` = mismo mensaje + línea `Quiero pagar con link de pago 💳`.
- [ ] **Step 5:** Verificar en preview los 3 casos de prueba canónicos EXACTOS (Toscana28/50/NL=11,100 · Toscana18/25/Jal=5,125 · Bali/100/Yuc=29,900 gratis) leyendo el DOM del resultado, y que el href de WhatsApp contenga modelo+m²+estado. Validar HTML. Commit `feat(hub): cotizador híbrido con envío estimado por zona`.

### Task 4: Envío + DIY + FAQ + banda local + Schema

**Files:** Modify: `public/pasto-sintetico/index.html`

- [ ] **Step 1:** Sección ENVIO: H2 "Cómo funciona tu pedido" — 4 pasos numerados: 1 Cotiza en línea o por WhatsApp → 2 Confirmamos envío exacto con tu C.P. y pagas (transferencia o link de pago) → 3 Embarcamos tu rollo (2 m de ancho) → 4 Recibes en 3-5 días hábiles con guía de rastreo. Nota: `Envío GRATIS a partir de 2 rollos (100 m²)` + `Mínimo de compra nacional: 25 m²`.
- [ ] **Step 2:** Sección DIY: H2 "¿Lo instalas tú mismo? Es más fácil de lo que crees" — resumen 5 pasos (nivelar/compactar → base drenante → extender y clavar → unir tramos → cepillar) + link `/blog/como-instalar-pasto-sintetico` "Ver la guía completa paso a paso →".
- [ ] **Step 3:** Sección FAQ (9 preguntas, cada una `<details>` o bloque visible): ¿Cuánto cuesta el pasto sintético con envío incluido? / ¿Cuál es la compra mínima? (25 m² nacional, desde 2 m² en showroom Tampico) / ¿Cuánto tarda el envío? / ¿Cómo pago? (transferencia, link de pago; anticipo confirma pedido) / ¿Dan factura? (CFDI 4.0) / ¿Qué modelo me conviene? (referir comparativa) / ¿Puedo instalarlo yo? / ¿Qué incluye el rollo? (2×25 m = 50 m²) / ¿Hacen instalación fuera de Tampico? (No — solo material con envío; instalación solo zona conurbada).
- [ ] **Step 4:** Banda LOCAL: "¿Estás en Tampico, Madero o Altamira? Tenemos showroom, venta desde 2 m² e instalación llave en mano" + 2 botones → `/venta-pasto-sintetico-tampico` y `/pasto-sintetico-tampico`.
- [ ] **Step 5:** JSON-LD en `<head>`: (a) `BreadcrumbList` (Inicio → Pasto Sintético), (b) `FAQPage` con las 9 Q&A del Step 3, (c) `ItemList` de 9 `Product` — cada uno: name `Pasto Sintético {Modelo}`, description (tag+ideal), offers `{price: rollo, priceCurrency:'MXN', availability:'InStock'}` y `shippingDetails:{'@type':'OfferShippingDetails','shippingDestination':{'@type':'DefinedRegion','addressCountry':'MX'},'deliveryTime':{'@type':'ShippingDeliveryTime','transitTime':{'@type':'QuantitativeValue','minValue':3,'maxValue':5,'unitCode':'DAY'}}}`. Validar cada bloque con `python3 -c "import json;json.loads(open('/dev/stdin').read())"`.
- [ ] **Step 6:** "Actualizado julio 2026" visible antes del footer. Validar HTML. Commit `feat(hub): envío, DIY, FAQ, banda local y schema completo`.

### Task 5: Interlinking del ecosistema

**Files:**
- Modify: `public/venta-pasto-sintetico-tampico/index.html`
- Modify: `public/pasto-sintetico-tampico/index.html`
- Modify: `public/index.html`
- Modify: `public/blog/pasto-sintetico-vs-natural-tampico/index.html`
- Modify: `public/sitemap.xml`
- Modify: `public/catalogo.html` (pcard "Pasto Sintético" de la sección pasto)

- [ ] **Step 1:** En ambas páginas locales, banda bajo el hero: `📦 ¿No estás en Tampico? Enviamos pasto sintético a todo México — 9 modelos desde $139/m² → <a href="/pasto-sintetico">Cotiza tu envío aquí</a>` (estilo consistente: fondo bggreen suave, 1 línea móvil).
- [ ] **Step 2:** Homepage: en la service-card de Pasto Sintético agregar al texto "· Envíos a todo México"; el link de la card sigue a la local (no canibalizar).
- [ ] **Step 3:** Blog vs-natural: en "También te puede interesar" agregar links a `/pasto-sintetico` (anchor "Envíos a todo México — precios por modelo") y a `/venta-pasto-sintetico-tampico`.
- [ ] **Step 4:** `catalogo.html`: en la pcard de Pasto Sintético, botón secundario "Envíos nacionales →" a `/pasto-sintetico`.
- [ ] **Step 5:** sitemap.xml: agregar `<url>` de `/pasto-sintetico` (priority 0.9) y de los 2 artículos futuros (Task 6-7) con lastmod 2026-07-06. Validar XML: `python3 -c "import xml.dom.minidom as m;m.parse('sitemap.xml');print('XML OK')"`. Validar HTMLs tocados. Commit `feat(hub): interlinking nacional en páginas locales, home, blog y sitemap`.

### Task 6: Artículo "¿Cuánto cuesta el pasto sintético en México? (2026)"

**Files:** Create: `public/blog/cuanto-cuesta-pasto-sintetico-mexico/index.html` (patrón: copiar `public/blog/pasto-sintetico-vs-natural-tampico/index.html` y reemplazar contenido)

- [ ] **Step 1:** Head: title `¿Cuánto Cuesta el Pasto Sintético en México? Precios 2026 por m²`; description con el rango $139-$399; canonical propio.
- [ ] **Step 2:** Contenido answer-first: H1 + **primer párrafo respuesta directa**: "El pasto sintético en México cuesta entre $139 y $399 por m² (IVA incluido) según altura y densidad, comprando por rollo directo de distribuidor. La instalación profesional agrega $150-$250/m². El envío nacional por paquetería va de ~$900 a ~$1,400 por rollo de 50 m²." Secciones H2: Precios 2026 por modelo (TABLA con los 9 y sus 3 escalones) / Qué hace variar el precio (altura, densidad g/m², garantía) / Costo real con envío (ejemplos: los 3 casos canónicos del cotizador) / ¿Rollo o por m²? / Precios de instalación vs DIY / FAQ (4 Q con FAQPage schema). CTA final + cotizador link `/pasto-sintetico#cotizador`. "Actualizado julio 2026" + Article schema (datePublished/dateModified).
- [ ] **Step 3:** Links internos: al hub (2), a guía DIY, a vs-natural. Validar HTML. Commit `feat(blog): artículo precios pasto sintético México 2026`.

### Task 7: Artículo "Cómo instalar pasto sintético tú mismo — guía paso a paso"

**Files:** Create: `public/blog/como-instalar-pasto-sintetico/index.html` (mismo patrón)

- [ ] **Step 1:** Head: title `Cómo Instalar Pasto Sintético Tú Mismo: Guía Paso a Paso 2026`; description con "en 1 día" y herramientas.
- [ ] **Step 2:** Contenido: respuesta directa (se puede instalar en 1 día un jardín de 25-50 m² con nivelación, base compactada, clavado y cepillado) + H2: Herramientas y materiales (lista) / Paso 1 Retira y nivela / Paso 2 Base drenante compactada / Paso 3 Extiende y deja reposar 2h / Paso 4 Corta y une tramos / Paso 5 Clava perímetro / Paso 6 Cepilla las fibras / Errores comunes (5) / ¿Cuántos m² pedir? (fórmula +5-10% merma, ancho 2 m) / FAQ (4 Q) — **HowTo schema** con los 6 pasos + FAQPage + Article.
- [ ] **Step 3:** Links: hub (2, incluyendo "pide tu material desde $139/m²"), artículo precios, local instalación (para Tampico). Validar HTML. Commit `feat(blog): guía DIY instalación pasto sintético`.

### Task 8: Verificación integral + deploy + verificación en producción

- [ ] **Step 1:** Preview móvil (375px): hub carga sin errores de consola; cotizador pasa los 3 casos canónicos; 9 cards; tabla 9 filas; sin overflow horizontal (`document.documentElement.scrollWidth<=clientWidth`); links internos responden 200 (fetch de las 6 URLs tocadas).
- [ ] **Step 2:** Validar los 4 JSON-LD del hub + schemas de ambos artículos (parsear con python json).
- [ ] **Step 3:** `git push origin main`. Esperar deploy (~30-60s).
- [ ] **Step 4:** Producción: `curl` del hub → contiene `id="cotizador"` y hash byte-idéntico al local; curl de los 2 artículos → 200; sitemap accesible.
- [ ] **Step 5:** Reportar al usuario: URLs live + pendientes manuales (Search Console: solicitar indexación de las 3 URLs nuevas; GBP: dar de alta los 9 productos — kit aparte).

---

## Self-review (hecho)
- Cobertura de spec: secciones 1-9 del hub ✓ (Task 1-4), ajustes locales ✓ (Task 5), 2 artículos fase 1 ✓ (Task 6-7), schema ✓ (Task 4/6/7), medición → Step 5 de Task 8 deja lo manual documentado. Páginas ciudad/3 artículos restantes = fase 2, fuera de este plan (explícito en spec).
- Sin placeholders: datos canónicos completos arriba; los textos de FAQ/pasos están especificados.
- Consistencia: `MODELOS`/`ZONAS`/`ESTADO_ZONA`/`precioM2()`/casos de prueba usados con los mismos nombres en Tasks 2-4 y verificados en Task 8.
