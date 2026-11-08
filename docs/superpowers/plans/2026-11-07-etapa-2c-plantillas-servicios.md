# Etapa 2c · Plantillas: servicios (diseño, mantenimiento, riego) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tercer sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2c; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §3.4, §4, §5, §10): `/diseno-jardines-tampico`, `/mantenimiento-jardines-tampico` y `/sistema-riego-tampico` dejan de ser HTML a mano parchado por `tools/servicios` y salen de la plantilla `servicio` de 2a con su contenido en `tools/site/contenido/`, con planes (máx. 3) que llevan **cada uno su propio mensaje de WhatsApp** y, en diseño, su línea de mensualidades con la fórmula oficial; una sola sección de precio y un solo proceso por página; precios, frecuencias, ahorro de agua y opiniones desde `datos.py`; paridad de contenido contra lo publicado. Antes, una tarea aplica en todo el sitio las respuestas del dueño del 2026-11-07: la visita para cotizar cuesta según la ubicación (`datos.VISITA_COSTO`) y fuera cualquier frase de "liquidar el saldo". Se publica en el lote 3 (con 2d) o sola si el dueño lo pide.

**Architecture:** Igual que 2a/2b: `tools/site/contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD`; `tools/site/plantillas/servicio.py` lo arma con `tools/site/componentes.py`; `tools/site/generar.py` registra la fila y `build.py` la escribe con el shell solo si cambia. Lo nuevo es pequeño y genérico: `componentes.opciones()` acepta precio cerrado (`desde: False`), "por cotización" (`precio_texto`), opción sin precio (tipos de riego) y una línea `vt-modo__mes` con el plazo más largo de `mensualidades.planes()` (`componentes.linea_mensualidad`, sustituye a `tools/servicios/planes_diseno.py`); `componentes.fichas()` (lo que incluye cada visita, reutiliza `.vt-modos` sin CSS nuevo); `garantia()` sin cifra; la plantilla gana `incluye`, tabla y nota bajo los planes, rótulos propios y objeción de una sola tabla, sin cambiar un byte de pasto en rollo ni de sintético en Tampico (lo prueba `test_generar`). Los mensajes de portada de las tres páginas viven en `mensajes_paginas.SERVICIOS` y por `RUTAS` también llegan al menú, la barra móvil y el pie. **CSS:** una regla nueva (`.vt-modo__precio .vt-modo__mes`) y la rejilla de `.vt-modos` pasa a `minmax(min(100%,18rem),1fr)` para que 3 planes no desborden a 768 px (8.4 KB gzip; presupuesto 10 KB). **Retiro de `tools/servicios` para estas páginas** (como 2a con pasto en rollo): sus entradas salen de `pages.py`; `planes_diseno.py`, `simulador.py`, `tests/test_simulador.py` y la línea `pago_nota` de `hero.py` se borran (ya no hay página que los use). `hero.py`, `pages.py` y `servicios.css` **se quedan**: los usan mayoreo, plantas, materiales y vivero (2d–2g); `servicios.css` se borra al cerrar la Etapa 2 (2i). Esto corrige la hoja de ruta, que daba por retirados `hero.py` y `servicios.css` en 2c. **SEO:** título, descripción, canonical, Open Graph, Twitter Card y tipos de JSON-LD intactos (`Service`, `FAQPage`, `BreadcrumbList`, `SpeakableSpecification` y, en riego, `HowTo`); el `Service` se copia tal cual (sus acentos rotos los arregla el grafo único de la Etapa 4); `FAQPage` y `HowTo` salen de lo visible. H1 con beneficio y lugar; mantenimiento agrega "jardinero" (auditoría 03); riego conserva su intención transaccional con una sola respuesta de precio y una sola lista de pasos (la canibalización con los 3 blogs de riego se resuelve con 301/fusión en la Etapa 3).

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en las pruebas de navegador; CSS plano; JavaScript vanilla existente (`vt-mensualidades.js`, `vt-simulador.js`, `terra.js`) sin cambios; `cwebp` (Homebrew) solo para reducir 9 fotos; Lighthouse 12 con `npx` en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2c` (rama `feat/etapa-2c`, Tarea 0). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- Cada parche de este plan se probó sobre `main` en `1d3fe59`, en este orden, en una copia de trabajo: aplica con `git apply` tal cual. Si `git apply` falla, `main` cambió: detente y reporta (no edites a mano para "hacerlo entrar").
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`).
- Cuando una tarea cambia `terra.css`, el build cambia el hash, reescribe el `<head>` de las 108 páginas, agrega `public/css/terra.<hash>.css` nuevo y borra la generación más vieja (`activos.json` guarda dos): es esperado y se versiona todo (`git add public tools/site/activos.json`), revisando antes `git status --short | grep -v '\.html$'`.
- Reglas del dueño (las prueban `test_reglas.py` y `test_consistencia.py`): nunca "Oasis"; nunca marcas de proveedor de pasto sintético (PastoPlus); nunca el nombre del proveedor de la terminal en `public/`; solo "mensualidades con tarjeta de crédito" (nunca "MSI", "meses sin intereses" ni "sin intereses"); sin pádel ni canchas para sintético (riego y pasto natural para **campos deportivos sí** son servicio real y se quedan); sin muestras físicas; nunca "pagas cuando ves…"; sin fechas de disponibilidad ni de corte; nunca "visita sin costo", "gratis" ni "gratuita" para la visita: **la visita para cotizar cuesta según la ubicación** (`datos.VISITA_COSTO`, decisión del dueño del 2026-11-07); ninguna frase sobre "liquidar el saldo" o "el resto se liquida" (decisión del 2026-11-07); "anticipo" sin porcentaje (`datos.ANTICIPO`); promesa única `datos.PROMESA_COMPLETA`; garantía de plantas de 30 días siempre condicionada y enlazada a `/politicas#garantia-plantas`; "flamboyán"; sin "crédito para clientes"; sin testimonios ni nombres inventados (los de estas páginas se conservan textuales y quedan pendientes de confirmación del dueño, ver al final); precios que el dueño aún no da (palmas sin precio, mármol, piedra bola, tezontle por camión) siguen "según cotización": no se inventan aquí ni en 2d–2f.
- Dos textos de CTA y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008". El "Pedir visita" de riego desaparece.

## Cobertura del spec y qué queda fuera

| Pide el spec / la hoja de ruta / el jurado | Dónde |
|---|---|
| §3.3 secuencia de servicio local: migas → H1 → precio ancla → CTA con promesa → prueba (datos y 3 fotos FIG.) → planes (máx. 3, un mensaje cada uno) → objeción → proceso de 5 pasos (uno solo) → garantía con condiciones → mensualidades → FAQ (8) → cobertura → relacionados → CTA final | Tareas 5, 7–9; `ComunTest.test_orden_de_secciones_del_spec` |
| Hoja de ruta 2c: planes con mensaje propio y línea de mensualidades por plan (sustituye `planes_diseno.py`) | Tarea 4 (`linea_mensualidad`, `opciones`), Tarea 7 |
| Auditoría 02: los 4 CTA de mantenimiento mandaban el mismo texto | Tarea 8 (`MantenimientoTest.test_un_mensaje_por_plan`), Tarea 11 (`generate_lead` por plan) |
| Auditoría 02: riego repetía precio y proceso | Tarea 9 (una sección de precio, un `vt-pasos`, `PARIDAD` mapea la lista duplicada) |
| Auditoría 03: "jardinero Tampico" no aparece en mantenimiento | Tarea 8 (H1, cobertura e incluye) |
| §3.4 recorrido de diseño: plan → WhatsApp → cuestionario enviado por el asesor | Tarea 7 (paso 2 del proceso; `/cuestionario` sigue `noindex` y sin enlace público) |
| §5.2 garantía de plantas condicionada en diseño | Tarea 7 (`test_garantia_de_plantas_condicionada`, `test_consistencia`) |
| Datos oficiales: diseño $3,000 / $6,500 / desde $18,000 (descuento en Premium solo en proyectos de más de $150,000, como en main); mantenimiento desde $750/mes y premium desde $1,800/mes (publicado en main); frecuencias semanal / cada 15 / cada 21 días / mensual; riego $180–$320/m² y "hasta 40%" de agua | Tarea 3 (`datos.py`) |
| Respuestas del dueño 2026-11-07: costo de la visita según ubicación; fuera "liquidas el saldo"; precios desconocidos "según cotización" | Tarea 2 (todo el sitio) |
| Retirar `tools/servicios` de estas páginas | Tareas 7–9 |
| AdsBot sin bloqueo en las tres URLs | Ya en `main` (`robots.txt`, `test_robots.py`); Tarea 12 lo verifica en vivo |
| Paridad (encabezados, FAQ, precios, enlaces, meta, tipos de JSON-LD) y opiniones | Tareas 1, 7–9 (`test_paridad.py`, `test_servicios_jardin.py`) |

Fuera de 2c: títulos y descripciones nuevos (Etapa 3; el `<title>` de mantenimiento con "jardinero" va ahí), 301 y fusión de los blogs de riego (Etapa 3), grafo JSON-LD único y acentos del `Service` (Etapa 4), borrar `servicios.css` (2i).

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{diseno-jardines-tampico,mantenimiento-jardines-tampico,sistema-riego-tampico}.json` | Lo que publicaba cada página antes de migrar (las escribe `paridad.py capturar`). |
| `tools/site/contenido/diseno_jardines.py` | Plan Terra: 3 planes con mensaje y mensualidad, tabla comparativa, objeción "¿y si no contrato la obra?", proceso, garantía de plantas, simulador, FAQ. |
| `tools/site/contenido/mantenimiento_jardines.py` | 3 planes ($750 / $1,800 / por cotización) con mensaje propio, qué incluye, frecuencia por temporada, proceso, sin permanencia forzada, pago mensual. |
| `tools/site/contenido/sistema_riego.py` | 3 tipos de sistema con mensaje propio, una sección de precio, comparativa, un proceso (HowTo), garantía de instalación, simulador. |
| `tools/site/tests/test_plantilla_servicio.py` | Secciones opcionales nuevas de la plantilla. |
| `tools/site/tests/test_servicios_jardin.py` | Las tres páginas: secuencia, mensajes, precios, copy, garantía, opiniones, JSON-LD. |
| `public/img/obra/{diseno-jardin-*,mantenimiento-*,riego-*}.webp` (9) | Fotos de prueba a 640/960 px. |

Se modifican: `tools/site/datos.py`, `mensajes_paginas.py`, `componentes.py`, `plantillas/servicio.py`, `generar.py`, `corregir_datos.py`, `contenido/{inicio,pasto_en_rollo,sintetico_tampico}.py`, `public/css/terra.css`; `tools/pasto/{zonas,precios}.py`; `public/blog/cuanto-cuesta-jardin-tampico-precios/index.html` y `public/gracias/index.html` (a mano, siguen sin plantilla); `tools/servicios/{pages,hero}.py` y `tests/test_pagos.py`; pruebas `test_datos`, `test_paginas`, `test_reglas`, `test_consistencia`, `test_pasto_en_rollo`, `test_componentes`, `test_terra_css`, `test_generar`, `test_navegador`, `test_corregir_datos`, `test_plantillas_navegador`. Se borran: `tools/servicios/planes_diseno.py`, `tools/servicios/simulador.py`, `tools/servicios/tests/test_simulador.py`. Regenerados por el build: las 3 páginas, home, pasto en rollo, sintético en Tampico, 6 zonas, `/precios` y el `<head>` de todas por el hash de `terra.css`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Crear el worktree desde `main` actualizado**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git worktree add ~/dev/viverosterra-e2c -b feat/etapa-2c
cd ~/dev/viverosterra-e2c && git log --oneline -1
```

Expected: el commit de `main` que agrega este plan (padre `1d3fe59`).

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"; which cwebp
```

Expected: `plantillas: 0 de 25 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 323 tests` y `OK`; `Ran 34 tests` y `OK`; `Ran 11 tests` y `OK`; `ℹ pass 41` y `ℹ fail 0`; `playwright ok`; la ruta de `cwebp` (si falta: `brew install webp`).

---

### Task 1: Capturas de paridad antes de migrar

**Files:**
- Create: `tools/site/tests/paridad/diseno-jardines-tampico.json`, `tools/site/tests/paridad/mantenimiento-jardines-tampico.json`, `tools/site/tests/paridad/sistema-riego-tampico.json`

- [ ] **Step 1: Capturar las tres páginas tal como están en `main`**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/paridad.py capturar /diseno-jardines-tampico /mantenimiento-jardines-tampico /sistema-riego-tampico
python3 -c "
import json
for p in ('diseno-jardines-tampico','mantenimiento-jardines-tampico','sistema-riego-tampico'):
    d=json.load(open(f'tools/site/tests/paridad/{p}.json')); print(p, len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']), 'HowTo' in d['jsonld_tipos'])"
```

Expected: tres líneas `captura: …`; luego `diseno-jardines-tampico 25 13 17 9 False`, `mantenimiento-jardines-tampico 32 13 9 8 False` y `sistema-riego-tampico 31 11 9 6 True`.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/tests/paridad/diseno-jardines-tampico.json tools/site/tests/paridad/mantenimiento-jardines-tampico.json tools/site/tests/paridad/sistema-riego-tampico.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de diseño, mantenimiento y riego antes de migrarlas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Respuestas del dueño del 2026-11-07 en todo el sitio (visita con costo según ubicación, sin "liquidar el saldo")

Decisiones: (1) "El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar." (forma corta: "Visita para medir y cotizar: su costo depende de la ubicación") en cada mención de la visita para medir o cotizar; sigue prohibido "visita sin costo/gratis", y por la misma razón sale "sin cargo extra por traslado" de las zonas. (2) Ninguna frase sobre liquidar el saldo: el "El resto se liquida según lo acordado en tu cotización" de pasto en rollo y sintético en Tampico se cambia por las formas de pago; el pago se explica con `datos.ANTICIPO`. En `main` el proceso de pasto en rollo (y su `HowTo`) ya no tiene frase de pago (paso 5: "Primera poda"); la prueba lo deja fijo. (3) Precios desconocidos siguen "según cotización" (nada que cambiar aquí). Las páginas de mantenimiento y riego todavía a mano quedan en `VISITA_COSTO_PENDIENTES` hasta las Tareas 8 y 9.

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/contenido/inicio.py`, `tools/site/contenido/pasto_en_rollo.py`, `tools/site/contenido/sintetico_tampico.py`, `tools/pasto/zonas.py`, `tools/pasto/precios.py`, `tools/site/corregir_datos.py`, `public/blog/cuanto-cuesta-jardin-tampico-precios/index.html`, `public/gracias/index.html`
- Test: `tools/site/tests/test_datos.py`, `tools/site/tests/test_reglas.py`, `tools/site/tests/test_consistencia.py`, `tools/site/tests/test_pasto_en_rollo.py`

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_consistencia.py b/tools/site/tests/test_consistencia.py
index 2d9f1c5..4aabfc7 100644
--- a/tools/site/tests/test_consistencia.py
+++ b/tools/site/tests/test_consistencia.py
@@ -22,6 +22,9 @@ PAGINAS = {p: p.read_text(encoding="utf-8") for p in sorted(PUBLIC.rglob("*.html
 TEXTOS = {p: textos_publicos(h) for p, h in PAGINAS.items()}
 LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
 PRECIOS = datos.PRECIOS
+# Páginas que todavía mencionan la visita sin su costo. Solo puede encoger: diseño, mantenimiento y riego salen de su
+# plantilla en las Tareas 7 a 9 de la Etapa 2c y las quitan de aquí.
+VISITA_COSTO_PENDIENTES = frozenset({"mantenimiento-jardines-tampico/index.html", "sistema-riego-tampico/index.html"})
 
 PROHIBIDAS = (
     ("promesa de respuesta vieja",
@@ -150,6 +153,20 @@ class ConsistenciaTest(unittest.TestCase):
             with self.subTest(pagina=archivo):
                 self.assertIn("/politicas#garantia-plantas", PAGINAS[PUBLIC / archivo])
 
+    def test_visita_con_costo_segun_la_ubicacion(self):
+        """Decisión del dueño (2026-11-07): la visita para medir o cotizar tiene un costo que depende de la ubicación;
+        cada mención lo dice cerca (datos.VISITA_COSTO o datos.VISITA_COSTO_CORTO) y nada promete traslado sin cargo."""
+        mencion = re.compile(r"\bvisita\s+(?:t[eé]cnica\s+)?para\s+(?:medir|cotizar)", re.I)
+        hallazgos = {}
+        for path, texto in TEXTOS.items():
+            for m in mencion.finditer(texto):
+                if "depende de la ubicación" not in texto[max(0, m.start() - 150):m.end() + 200]:
+                    hallazgos.setdefault(nombre(path), f"…{texto[max(0, m.start() - 60):m.end() + 60]}…")
+            if re.search(r"sin cargo (?:extra )?por traslado", texto, re.I):
+                hallazgos.setdefault(nombre(path), "traslado sin cargo")
+        self.assertEqual({k: v for k, v in hallazgos.items() if k not in VISITA_COSTO_PENDIENTES}, {})
+        self.assertEqual(sorted(VISITA_COSTO_PENDIENTES - set(hallazgos)), [], "ya lo dicen: sácalas de la lista")
+
     def test_home_con_cifras_oficiales(self):
         home = TEXTOS[PUBLIC / "index.html"]
         self.assertIn(f"{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones", home)
diff --git a/tools/site/tests/test_datos.py b/tools/site/tests/test_datos.py
index 43928e1..559bce6 100644
--- a/tools/site/tests/test_datos.py
+++ b/tools/site/tests/test_datos.py
@@ -80,6 +80,12 @@ class DatosTest(unittest.TestCase):
                                                           r"septiembre|octubre|noviembre|diciembre|vigentes)\b")
         self.assertFalse(hasattr(datos, "VIGENCIA"))
 
+    def test_visita_con_costo_segun_la_ubicacion(self):
+        """Decisión del dueño (2026-11-07): la visita para cotizar tiene costo y depende de la ubicación del servicio."""
+        self.assertEqual(datos.VISITA_COSTO, "El costo de la visita para cotizar depende de la ubicación del servicio; "
+                                             "te lo confirmamos por WhatsApp antes de agendar.")
+        self.assertEqual(datos.VISITA_COSTO_CORTO, "Visita para medir y cotizar: su costo depende de la ubicación")
+
     def test_mensajes_terminan_con_la_firma(self):
         for servicio in datos.MENSAJES:
             with self.subTest(servicio=servicio):
diff --git a/tools/site/tests/test_pasto_en_rollo.py b/tools/site/tests/test_pasto_en_rollo.py
index d00df96..a59f0fe 100644
--- a/tools/site/tests/test_pasto_en_rollo.py
+++ b/tools/site/tests/test_pasto_en_rollo.py
@@ -121,6 +121,9 @@ class PastoEnRolloTest(unittest.TestCase):
         titulos = [re.sub(r"\s*<span.*", "", h) for h in re.findall(r"<li><h3>(.*?)</h3>", proceso)]
         self.assertEqual([p["name"] for p in pasos], titulos)
         self.assertEqual(len(pasos), 5)
+        # Decisión del dueño (2026-11-07): ningún paso del proceso habla de liquidar el saldo ni de pagos.
+        for paso in pasos:
+            self.assertNotRegex(paso["text"], r"(?i)saldo|liquid|pagas|anticipo")
         for paso in pasos:
             self.assertIn(paso["text"], TEXTO)
         self.assertEqual(MAIN.count('class="vt-pasos"'), 1)
diff --git a/tools/site/tests/test_reglas.py b/tools/site/tests/test_reglas.py
index 1959aed..d4c6e0a 100644
--- a/tools/site/tests/test_reglas.py
+++ b/tools/site/tests/test_reglas.py
@@ -30,6 +30,9 @@ PROHIBIDAS = (
 )
 DEPORTES_RE = re.compile(r"p[aá]del|canchas?", re.I)
 PAGO_AL_TERMINAR_RE = re.compile(r"\bpagas\s+(?:cuando|al\s+ver)\b", re.I)
+# Decisión del dueño (2026-11-07): no le gusta "liquidas el saldo según lo acordado"; no se escribe ninguna frase sobre
+# liquidar el saldo o el resto (el pago se explica con el anticipo y las formas de pago). Las citas de clientes no cuentan.
+SALDO_RE = re.compile(r"\bliquid(?:as|a|amos|ar|es)\s+el\s+(?:saldo|resto)\b|\bel\s+(?:saldo|resto)\s+se\s+liquida\b", re.I)
 # Decisión del dueño (2026-11-07): no se ofrece crédito a clientes (ni a instaladores ni a constructoras recurrentes).
 CREDITO_CLIENTES_RE = re.compile(r"\bcr[eé]dito\s+(?:para|a)\s+(?:(?:los|sus|nuestros)\s+)?clientes\b", re.I)
 # Decisión del dueño (2026-11-07): la visita para medir tiene costo o depende; nunca "visita sin costo", "visita
@@ -173,6 +176,21 @@ class ReglasDelDuenoTest(unittest.TestCase):
                 hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
         self.assertEqual(hallazgos, [])
 
+    def test_sin_liquidar_el_saldo(self):
+        hallazgos = []
+        for path, texto in publicados():
+            for m in SALDO_RE.finditer(texto):
+                hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
+        self.assertEqual(hallazgos, [])
+
+    def test_liquidar_el_saldo_se_detecta(self):
+        for sucio in ("Liquidas el saldo según lo acordado en tu cotización", "El resto se liquida según lo acordado",
+                      "liquidamos el saldo", "el saldo se liquida al terminar"):
+            self.assertTrue(SALDO_RE.search(sucio), sucio)
+        for limpio in ("Pagué el resto hasta que lo vi terminado", "Puedes pagar de contado o en mensualidades",
+                       "Liquidambar styraciflua"):
+            self.assertIsNone(SALDO_RE.search(limpio), limpio)
+
     def test_sin_credito_para_clientes(self):
         hallazgos = []
         for path, texto in publicados():
@@ -205,6 +223,8 @@ class ReglasDelDuenoTest(unittest.TestCase):
                       "diagnóstico gratuito", "una visita de diagnóstico sin costo", "diagnósticos de pasto sin costo"):
             self.assertRegex(sucio, VISITA_GRATIS_RE)
         for limpio in ("Agendamos una visita para medir y cotizar", "Cotización gratis por WhatsApp",
+                       "El costo de la visita para cotizar depende de la ubicación del servicio",
+                       "Visita para medir y cotizar: su costo depende de la ubicación",
                        "la reponemos sin costo", "Visítanos en el vivero",
                        "el resto de Altamira, sin cargo extra por traslado", "no cuesta como un pasto de lujo"):
             self.assertNotRegex(limpio, VISITA_GRATIS_RE)
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_reglas tests.test_consistencia tests.test_pasto_en_rollo 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"`
Expected: `ERROR: test_visita_con_costo_segun_la_ubicacion (tests.test_datos…)`, `FAIL: test_sin_liquidar_el_saldo`, `FAIL: test_visita_con_costo_segun_la_ubicacion (tests.test_consistencia…)` y `FAILED (failures=2, errors=1)`.

- [ ] **Step 3: Datos, contenido de las plantillas y generadores de `tools/pasto`**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/pasto/precios.py b/tools/pasto/precios.py
index 9a3281c..c1621f4 100644
--- a/tools/pasto/precios.py
+++ b/tools/pasto/precios.py
@@ -2,10 +2,16 @@
 
 Los precios de pasto sintético salen de data.py; el resto son los datos oficiales confirmados por el dueño.
 """
+import sys
+from pathlib import Path
+
 from common import (SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, footer, head, jsonld, section_open, wa)
 from data import MODELOS, PHONE_DISPLAY, SITE, UPDATED, WA_NUMBER
 from mensualidades import PLAZOS, minimo_de, total_a_plazos
 
+sys.path.append(str(Path(__file__).resolve().parents[1] / "site"))  # al final: tools/site también tiene un build.py
+import datos  # noqa: E402  (VISITA_COSTO: decisión del dueño 2026-11-07)
+
 URL = f"{SITE}/precios"
 BUSINESS_ID = f"{SITE}/#negocio"
 IMG = "/img/precios/pasto-rollo-jardin"
@@ -241,7 +247,7 @@ def build_precios():
   <section class="closing" aria-labelledby="cierre">
     <div class="wrap">
       <h2 id="cierre">¿Quieres el precio exacto <em>de tu jardín?</em></h2>
-      <p>Mándanos tu colonia, los metros aproximados y una foto del espacio. Te respondemos en menos de 1 hora en horario y, si hace falta, agendamos una visita para medir.</p>
+      <p>Mándanos tu colonia, los metros aproximados y una foto del espacio. Te respondemos en menos de 1 hora en horario y, si hace falta, agendamos una visita para medir. {esc(datos.VISITA_COSTO)}</p>
       <div class="closing__actions">
         <a class="btn btn--light" href="{wa('Hola, quiero el precio exacto de mi jardín. Mi colonia es: ___ · Metros aprox.: ___ · Te mando foto del espacio.')}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
         <a class="btn btn--ghost" href="tel:+528333268008">Llamar {PHONE_DISPLAY}</a>
diff --git a/tools/pasto/zonas.py b/tools/pasto/zonas.py
index 2f9e3c2..41b3887 100644
--- a/tools/pasto/zonas.py
+++ b/tools/pasto/zonas.py
@@ -4,9 +4,15 @@ Sustituyen a las 20 páginas por colonia (las demás redirigen en vercel.json).
 Colonias, municipios y códigos postales verificados con directorios SEPOMEX (septiembre 2026).
 No afirmar obras concretas en una colonia sin foto o dato del dueño.
 """
+import sys
+from pathlib import Path
+
 from common import SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, footer, head, jsonld, section_open, wa
 from data import SITE
 
+sys.path.append(str(Path(__file__).resolve().parents[1] / "site"))  # al final: tools/site también tiene un build.py
+import datos  # noqa: E402  (VISITA_COSTO: decisión del dueño 2026-11-07)
+
 BUSINESS_ID = f"{SITE}/#negocio"
 
 PRECIOS = [
@@ -32,7 +38,7 @@ ZONAS = {
         ],
         img=("diseno-jardines-tampico-proyecto", 960, 1574, "center 55%"),
         faqs=[
-            ("¿Dan servicio de jardinería en Lomas de Rosales?", "Sí. Atendemos Lomas de Rosales, Lomas de la Aurora y Vista Hermosa en Tampico con instalación de pasto, diseño, riego y mantenimiento. Agendamos una visita para medir y cotizar."),
+            ("¿Dan servicio de jardinería en Lomas de Rosales?", "Sí. Atendemos Lomas de Rosales, Lomas de la Aurora y Vista Hermosa en Tampico con instalación de pasto, diseño, riego y mantenimiento. Agendamos una visita para medir y cotizar. " + datos.VISITA_COSTO),
             ("¿Cuánto cuesta el mantenimiento de jardín en Lomas de Rosales?", "Desde $750 al mes. El precio final depende de los metros del jardín y de la frecuencia de visitas."),
             ("¿Qué riego conviene en un jardín con pendiente?", "Goteo en jardineras y aspersión de bajo caudal en el pasto, con zonas separadas para la parte alta y la baja. Así el agua no escurre y se aprovecha mejor."),
         ],
@@ -87,7 +93,7 @@ ZONAS = {
         img=("riego-pro-01", 960, 640, None),
         faqs=[
             ("¿Atienden jardines en Lomas del Chairel y Colinas de San Gerardo?", "Sí. Atendemos Lomas del Chairel, Colinas de San Gerardo y Flamboyanes en Tampico con pasto, riego, diseño y mantenimiento."),
-            ("¿Qué hago si mi jardín se encharca?", "Revisamos el nivel del terreno y el drenaje. A veces basta con nivelar y mejorar la tierra; en otros casos hace falta un dren. Lo revisamos en la visita para medir."),
+            ("¿Qué hago si mi jardín se encharca?", "Revisamos el nivel del terreno y el drenaje. A veces basta con nivelar y mejorar la tierra; en otros casos hace falta un dren. Lo revisamos en la visita para medir. " + datos.VISITA_COSTO),
             ("¿Necesito tierra negra antes de poner pasto?", "En casas nuevas con suelo de relleno, sí. La tierra negra vegetal cuesta $90 el costal o $1,500 el m³."),
         ],
     ),
@@ -114,7 +120,7 @@ ZONAS = {
         title="Jardinería en Altamira y Lagunas de Miralta: pasto, diseño y mantenimiento",
         h1="Jardinería en Altamira", accent="y Lagunas de Miralta",
         colonias=[("Residencial Lagunas de Miralta", "89605"), ("Altamira Centro", "89600")],
-        lede="Pasto en rollo, diseño, riego y mantenimiento para Residencial Lagunas de Miralta y el resto de Altamira, sin cargo extra por traslado.",
+        lede="Pasto en rollo, diseño, riego y mantenimiento para Residencial Lagunas de Miralta y el resto de Altamira.",
         retos=[
             ("Jardines de fraccionamiento", "En fraccionamientos cerrados coordinamos horarios y acceso con la administración para instalar y dar mantenimiento."),
             ("Áreas verdes amplias", "Para jardines grandes, el riego automático por zonas y un plan de mantenimiento mensual mantienen el pasto parejo."),
@@ -122,7 +128,7 @@ ZONAS = {
         ],
         img=("jardineria-areas-verdes-tampico", 793, 1190, "center 45%"),
         faqs=[
-            ("¿Dan servicio de jardinería en Lagunas de Miralta?", "Sí. Atendemos Residencial Lagunas de Miralta y el resto de Altamira con pasto, diseño, riego y mantenimiento, sin cargo extra por traslado."),
+            ("¿Dan servicio de jardinería en Lagunas de Miralta?", "Sí. Atendemos Residencial Lagunas de Miralta y el resto de Altamira con pasto, diseño, riego y mantenimiento. " + datos.VISITA_COSTO),
             ("¿Cuánto cuesta el mantenimiento de jardín en Altamira?", "Desde $750 al mes. El precio depende de los metros y de la frecuencia de visitas."),
             ("¿Atienden empresas en el puerto industrial de Altamira?", 'Sí. Tenemos REPSE 773725 y factura CFDI 4.0 para contratos de mantenimiento de áreas verdes. Ve el <a href="/mantenimiento-jardines-tampico">servicio de mantenimiento</a>.'),
         ],
@@ -168,7 +174,7 @@ def colonias_html(z):
         f'            <tr><th scope="row">{esc(c)}<span>{esc(z["municipio"])}</span></th><td><strong>{cp}</strong></td></tr>'
         for c, cp in z["colonias"]
     )
-    return f"""<p class="section__intro">Llegamos sin cargo extra por traslado. Si tu colonia está cerca y no aparece, también te atendemos.</p>
+    return f"""<p class="section__intro">{esc(datos.VISITA_COSTO)} Si tu colonia está cerca y no aparece, también te atendemos.</p>
         <div class="table-scroll" tabindex="0" role="region" aria-label="Colonias atendidas">
           <table class="compare-table compare-table--prices num">
             <thead><tr><th scope="col">Colonia</th><th scope="col">Código postal</th></tr></thead>
@@ -242,7 +248,7 @@ def build_zona(slug, z):
   <section class="closing" aria-labelledby="cierre">
     <div class="wrap">
       <h2 id="cierre">Cotiza tu jardín <em>en {esc(z["corto"])}</em></h2>
-      <p>Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. Te respondemos en menos de 1 hora en horario y, si hace falta, agendamos una visita para medir.</p>
+      <p>Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. Te respondemos en menos de 1 hora en horario y, si hace falta, agendamos una visita para medir. {esc(datos.VISITA_COSTO)}</p>
       <div class="closing__actions">
         <a class="btn btn--light" href="{wa(guided(z["corto"]))}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
         <a class="btn btn--ghost" href="/vivero-tampico">Visitar el vivero</a>
diff --git a/tools/site/contenido/inicio.py b/tools/site/contenido/inicio.py
index 7648bac..00cb316 100644
--- a/tools/site/contenido/inicio.py
+++ b/tools/site/contenido/inicio.py
@@ -205,8 +205,8 @@ CONTENIDO = {
             {"titulo": "Nos mandas medidas y foto", "quien": "tu", "cuando": "Día 0 · por WhatsApp",
              "texto": f"Tu colonia, los metros aproximados y una foto del espacio. {datos.PROMESA}."},
             {"titulo": "Medimos y decidimos", "quien": "juntos", "cuando": "Visita para medir",
-             "texto": ("Agendamos una visita para medir y cotizar, y recorremos el espacio contigo. Si hace falta tierra "
-                       f"negra o nivelación, te decimos cuánto cuesta antes de empezar. {datos.ANTICIPO}")},
+             "texto": (f"{datos.VISITA_COSTO_CORTO}. Recorremos el espacio contigo y, si hace falta tierra negra o "
+                       f"nivelación, te decimos cuánto cuesta antes de empezar. {datos.ANTICIPO}")},
             {"titulo": "Instalamos en un día", "quien": "nosotros", "cuando": "Día de instalación",
              "texto": f"El pasto llega del campo {datos.LLEGADA_PASTO}, se corta para tu pedido y va directo a tu jardín."},
             {"titulo": "El primer riego", "quien": "tu", "cuando": "Días 1 a 20",
@@ -264,7 +264,7 @@ CONTENIDO = {
     "cierre": {
         "titulo": "Mándanos tus medidas y una foto del espacio.",
         "lede": ("Tu colonia, los metros aproximados y qué quieres hacer. Si hace falta, agendamos una visita para medir y "
-                 "cotizar."),
+                 f"cotizar. {datos.VISITA_COSTO}"),
         "mensaje": datos.MENSAJES["general"],
     },
 }
diff --git a/tools/site/contenido/pasto_en_rollo.py b/tools/site/contenido/pasto_en_rollo.py
index 9d00e5e..e503666 100644
--- a/tools/site/contenido/pasto_en_rollo.py
+++ b/tools/site/contenido/pasto_en_rollo.py
@@ -246,8 +246,8 @@ CONTENIDO = {
     },
     "pago": {
         "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
-        "lede": (f"{datos.ANTICIPO} El resto se liquida según lo acordado en tu cotización, de contado o en "
-                 f"mensualidades con tarjeta de crédito desde {DESDE_MENSUALIDADES}."),
+        "lede": (f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito desde "
+                 f"{DESDE_MENSUALIDADES}."),
         "puntos": (
             "Recibes el precio del pasto, la entrega y la instalación por separado.",
             "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
@@ -261,7 +261,7 @@ CONTENIDO = {
     "cierre": {
         "titulo": "Tu jardín verde, instalado en un día.",
         "lede": ("Dinos si lo quieres solo pasto o instalado, tu colonia y tus metros, y mándanos una foto. Si hace falta, "
-                 "agendamos una visita para medir y cotizar."),
+                 f"agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}"),
         "mensaje": datos.MENSAJES["pasto-natural"],
     },
     "cobertura": {
diff --git a/tools/site/contenido/sintetico_tampico.py b/tools/site/contenido/sintetico_tampico.py
index d137136..d4d355f 100644
--- a/tools/site/contenido/sintetico_tampico.py
+++ b/tools/site/contenido/sintetico_tampico.py
@@ -65,7 +65,8 @@ PREGUNTAS = (
 
 PASOS = (
     {"titulo": "Visita y medición", "quien": "nosotros", "cuando": "Antes de cotizar",
-     "texto": "Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso."},
+     "texto": ("Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso. "
+               f"{datos.VISITA_COSTO_CORTO}.")},
     {"titulo": "Preparación del terreno", "quien": "nosotros", "cuando": "Si hace falta",
      "texto": ("Si hace falta, retiramos lo existente, nivelamos y ponemos grava fina para que drene. Se cotiza aparte "
                "según tu espacio.")},
@@ -163,7 +164,7 @@ CONTENIDO = {
              "mensaje": "Hola, quiero comprar pasto sintético en el showroom. ¿Tienen existencia?\nModelo: ___\nMetros: ___"},
             {"rotulo": "Opción 2", "titulo": "Nosotros lo instalamos", "precio": INST_MIN, "unidad": "/m²",
              "detalle": "Material y colocación", "rec": True,
-             "puntos": ("Visita y cotización sin compromiso", "Colocación, uniones, orillas y cepillado",
+             "puntos": (datos.VISITA_COSTO_CORTO, "Colocación, uniones, orillas y cepillado",
                         "Material con garantía de fábrica"),
              "nota": ("Cada terreno es distinto. Si el tuyo necesita retiro, nivelación o base drenante, lo vemos en la "
                       "visita y te lo cotizamos aparte, antes de empezar y sin sorpresas."),
@@ -208,8 +209,7 @@ CONTENIDO = {
     },
     "pago": {
         "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
-        "lede": (f"{datos.ANTICIPO} El resto se liquida según lo acordado en tu cotización, de contado o en mensualidades "
-                 "con tarjeta de crédito."),
+        "lede": f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito.",
         "puntos": ("Recibes el precio del material, la instalación y la preparación del terreno por separado.",
                    "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
                    ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos "
diff --git a/tools/site/corregir_datos.py b/tools/site/corregir_datos.py
index 33c632f..dda13d4 100644
--- a/tools/site/corregir_datos.py
+++ b/tools/site/corregir_datos.py
@@ -267,7 +267,7 @@ POR_ARCHIVO = (
      "          <li><strong>Si te interesa:</strong> arrancamos el proyecto en 3–10 días.</li>\n        </ol>",
      "<h3>Qué sigue ahora</h3>\n        <ol>\n"
      f"          <li><strong>En menos de 1 hora en horario</strong> te escribimos por WhatsApp o correo con tu cotización.</li>\n"
-     "          <li><strong>Si hace falta,</strong> agendamos contigo una visita para medir.</li>\n"
+     f"          <li><strong>Si hace falta,</strong> agendamos contigo una visita para medir. {datos.VISITA_COSTO}</li>\n"
      "          <li><strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.</li>\n        </ol>"),
     ("public/gracias/index.html", "        Hablar ahora por WhatsApp\n", "        Adelantar por WhatsApp\n"),
     ("public/gracias/index.html", "💡 <strong>Tip:</strong> mientras esperas, revisa nuestro", "<strong>Mientras tanto:</strong> revisa nuestro"),
diff --git a/tools/site/datos.py b/tools/site/datos.py
index 7653725..a930895 100644
--- a/tools/site/datos.py
+++ b/tools/site/datos.py
@@ -73,6 +73,11 @@ GARANTIA_PASTO = ("Si una sección no arraiga en 15 a 20 días, la reponemos sin
 GARANTIA_PLANTAS = "30 días en las plantas que sembramos nosotros, con el riego indicado (ver condiciones)."
 PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."
 ARRAIGO = "15 a 20 días"
+# Decisión del dueño (2026-11-07): la visita para medir y cotizar tiene un costo que depende de la ubicación del
+# servicio. Nunca "visita sin costo" ni "gratis" (test_reglas.py); toda mención de la visita lleva una de estas dos.
+VISITA_COSTO = ("El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por "
+                "WhatsApp antes de agendar.")
+VISITA_COSTO_CORTO = "Visita para medir y cotizar: su costo depende de la ubicación"
 LLEGADA_PASTO = "una vez por semana, generalmente los viernes"
 ANTICIPO = ("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
             "un anticipo.")
EOF
```

`tools/pasto/zonas.py` y `precios.py` importan `datos` agregando `tools/site` **al final** de `sys.path` (igual que `componentes.py` con `tools/pasto`): los dos paquetes tienen un `build.py`. El renglón de `corregir_datos.py` es el reemplazo de `gracias/` que ahora termina con la frase nueva (si no, su prueba de idempotencia lo marcaría como texto perdido).

- [ ] **Step 4: Las dos páginas que siguen a mano**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/public/blog/cuanto-cuesta-jardin-tampico-precios/index.html b/public/blog/cuanto-cuesta-jardin-tampico-precios/index.html
index 8056b63..b8603a7 100644
--- a/public/blog/cuanto-cuesta-jardin-tampico-precios/index.html
+++ b/public/blog/cuanto-cuesta-jardin-tampico-precios/index.html
@@ -62,7 +62,7 @@ h1,h2,h3,h4{font-family:"Playfair Display",serif}
 {"@type":"Question","name":"¿Hay financiamiento para hacer un jardín en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN previo acuerdo. Muchos clientes financian su jardín a través de créditos personales o de nómina. Para proyectos pequeños de $5,000-$15,000, el pago de contado es habitual."}},
 {"@type":"Question","name":"¿Cuánto tiempo tarda la instalación de un jardín en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Un jardín pequeño de 30-50 m² tarda 1 día de instalación. Un proyecto mediano de 80-150 m² toma entre 2 y 4 días. Un proyecto premium de 200+ m² con diseño y riego automatizado puede tomar entre 1 y 3 semanas según complejidad. El diseño previo toma entre 3 y 7 días adicionales."}},
 {"@type":"Question","name":"¿Necesito permisos para hacer un jardín en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Para jardines residenciales privados no se requieren permisos en Tampico, Madero ni Altamira. Sí puede requerirse permiso municipal si el proyecto modifica banquetas, calles o áreas de uso común en fraccionamientos. Viveros Terra te asesora sobre estos casos al momento de presupuestar tu proyecto."}},
-{"@type":"Question","name":"¿Pueden ir a cotizar mi jardín a domicilio en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Sí. Viveros Terra agenda una visita para medir y cotizar proyectos de diseño de jardín en Tampico, Madero y Altamira. El equipo técnico visita el terreno, toma medidas, evalúa el suelo y entrega una propuesta detallada en menos de 48 horas. Agenda tu visita por WhatsApp al 833 326 8008."}}
+{"@type":"Question","name":"¿Pueden ir a cotizar mi jardín a domicilio en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Sí. Viveros Terra agenda una visita para medir y cotizar proyectos de diseño de jardín en Tampico, Madero y Altamira. El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar. El equipo técnico visita el terreno, toma medidas, evalúa el suelo y entrega una propuesta detallada en menos de 48 horas. Agenda tu visita por WhatsApp al 833 326 8008."}}
 ]},
 {"@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Inicio","item":"https://www.viverosterra.com"},
@@ -384,7 +384,7 @@ h1,h2,h3,h4{font-family:"Playfair Display",serif}
         <li>Diseño + instalación integral = $120,000 MXN aprox.</li>
       </ul>
 
-      <p>Para proyectos de cualquier tamaño, el primer paso es siempre una cotización sin compromiso. El equipo de Viveros Terra agenda una visita para medir y cotizar en Tampico, Madero y Altamira.</p>
+      <p>Para proyectos de cualquier tamaño, el primer paso es siempre una cotización sin compromiso. El equipo de Viveros Terra agenda una visita para medir y cotizar en Tampico, Madero y Altamira. El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar.</p>
 
     </div><!-- /article-prose -->
 
@@ -414,7 +414,7 @@ h1,h2,h3,h4{font-family:"Playfair Display",serif}
 
       <div class="faq-block">
         <h3>¿Pueden ir a cotizar mi jardín a domicilio en Tampico?</h3>
-        <p>Sí. Viveros Terra agenda una visita para medir y cotizar proyectos de diseño de jardín en Tampico, Madero y Altamira. El equipo visita el terreno, toma medidas, evalúa el suelo y entrega una propuesta en menos de 48 horas. Agenda tu visita por WhatsApp al 833 326 8008.</p>
+        <p>Sí. Viveros Terra agenda una visita para medir y cotizar proyectos de diseño de jardín en Tampico, Madero y Altamira. El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar. El equipo visita el terreno, toma medidas, evalúa el suelo y entrega una propuesta en menos de 48 horas. Agenda tu visita por WhatsApp al 833 326 8008.</p>
       </div>
     </section>
 
diff --git a/public/gracias/index.html b/public/gracias/index.html
index f0d617e..28f311b 100644
--- a/public/gracias/index.html
+++ b/public/gracias/index.html
@@ -101,7 +101,7 @@ h1{font-family:'Playfair Display',serif;font-size:38px;color:#0D2B0E;line-height
         <h3>Qué sigue ahora</h3>
         <ol>
           <li><strong>En menos de 1 hora en horario</strong> te escribimos por WhatsApp o correo con tu cotización.</li>
-          <li><strong>Si hace falta,</strong> agendamos contigo una visita para medir.</li>
+          <li><strong>Si hace falta,</strong> agendamos contigo una visita para medir. El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar.</li>
           <li><strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.</li>
         </ol>
       </div>
EOF
```

- [ ] **Step 5: Build y pruebas en verde**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Expected: primera corrida `plantillas: 3 de 25 páginas escritas` (home, pasto en rollo, sintético en Tampico); la segunda `0 de 25` y `shell: 0 de 108`; `git status` sin archivos ajenos: las rutas de `tools/` de este paso y 12 `.html` (home, pasto en rollo, sintético en Tampico, 6 `jardineria-*`, `precios`, el blog y `gracias`).

Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_reglas tests.test_consistencia tests.test_pasto_en_rollo tests.test_inicio tests.test_tienda tests.test_corregir_datos tests.test_paridad tests.test_generar 2>&1 | tail -1` y `cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1`
Expected: `OK` y `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/datos.py tools/site/contenido/inicio.py tools/site/contenido/pasto_en_rollo.py tools/site/contenido/sintetico_tampico.py tools/pasto/zonas.py tools/pasto/precios.py tools/site/corregir_datos.py tools/site/tests/test_datos.py tools/site/tests/test_reglas.py tools/site/tests/test_consistencia.py tools/site/tests/test_pasto_en_rollo.py public/index.html public/pasto-en-rollo-tampico/index.html public/pasto-sintetico-tampico/index.html public/jardineria-*/index.html public/precios/index.html public/blog/cuanto-cuesta-jardin-tampico-precios/index.html public/gracias/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(dueño): la visita para cotizar cuesta según la ubicación y fuera “el resto se liquida”" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Datos de los servicios de jardín y mensajes de cada página

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/mensajes_paginas.py`, `public/{diseno-jardines-tampico,mantenimiento-jardines-tampico,sistema-riego-tampico}/index.html` (solo el shell)
- Test: `tools/site/tests/test_datos.py`, `tools/site/tests/test_paginas.py`

Las opiniones con nombre de las tres páginas se copian **textuales** de `main` a `datos.py` (verificado palabra por palabra contra el HTML publicado) con la marca "PENDIENTE DEL DUEÑO": no se inventa ni se edita ninguna. Los mensajes de portada son los de main con los huecos `___` y, para mantenimiento, con las cuatro frecuencias.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_datos.py b/tools/site/tests/test_datos.py
index 559bce6..62c61ad 100644
--- a/tools/site/tests/test_datos.py
+++ b/tools/site/tests/test_datos.py
@@ -86,6 +86,18 @@ class DatosTest(unittest.TestCase):
                                              "te lo confirmamos por WhatsApp antes de agendar.")
         self.assertEqual(datos.VISITA_COSTO_CORTO, "Visita para medir y cotizar: su costo depende de la ubicación")
 
+    def test_datos_de_servicios_etapa_2c(self):
+        p = datos.PRECIOS
+        self.assertEqual((p["diseno"], p["diseno_completo"], p["diseno_premium"]), (3000, 6500, 18000))
+        self.assertEqual(p["diseno_premium_descuento_desde"], 150000)
+        self.assertEqual((p["mantenimiento_mes"], p["mantenimiento_premium_mes"]), (750, 1800))
+        self.assertEqual(datos.RIEGO_AHORRO, "hasta 40%")
+        self.assertEqual(datos.FRECUENCIAS_MANTENIMIENTO, ("semanal", "cada 15 días", "cada 21 días", "mensual"))
+        nombres = [n for grupo in (datos.OPINIONES_DISENO, datos.OPINIONES_MANTENIMIENTO, datos.OPINIONES_RIEGO)
+                   for _c, n, _d in grupo]
+        self.assertEqual(nombres, ["Daniela M.", "Ing. Roberto S.", "Carolina R.", "Ing. Gerardo M.", "Roberto C.",
+                                   "María V."])
+
     def test_mensajes_terminan_con_la_firma(self):
         for servicio in datos.MENSAJES:
             with self.subTest(servicio=servicio):
diff --git a/tools/site/tests/test_paginas.py b/tools/site/tests/test_paginas.py
index 93cf318..5dbd324 100644
--- a/tools/site/tests/test_paginas.py
+++ b/tools/site/tests/test_paginas.py
@@ -6,6 +6,7 @@ from pathlib import Path
 sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
 import datos  # noqa: E402
+import mensajes_paginas  # noqa: E402
 import paginas  # noqa: E402
 
 
@@ -91,6 +92,17 @@ class ContextoTest(unittest.TestCase):
                 self.assertEqual(ctx["mensaje_pie"], "Hola, tengo una pregunta sobre pasto sintético" + firma)
         self.assertEqual(paginas.contexto("/")["mensaje_pie"], datos.mensaje("general"))
 
+    def test_servicios_de_jardin_con_su_mensaje_en_menu_barra_y_pie(self):
+        """Etapa 2c: el menú, la barra móvil y el pie llevan el mismo mensaje que la portada de la página."""
+        for ruta, texto in mensajes_paginas.SERVICIOS.items():
+            ctx = paginas.contexto(ruta)
+            with self.subTest(ruta=ruta):
+                self.assertEqual(ctx["mensaje"], datos.con_firma(texto))
+                self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
+                self.assertIn("Colonia: ___", texto)
+        self.assertEqual(sorted(mensajes_paginas.SERVICIOS), ["/diseno-jardines-tampico", "/mantenimiento-jardines-tampico",
+                                                              "/sistema-riego-tampico"])
+
     def test_ruta_desconocida_falla(self):
         with self.assertRaises(KeyError):
             paginas.contexto("/no-existe")
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas 2>&1 | grep -E "^(FAIL|ERROR):|FAILED"`
Expected: `ERROR: test_datos_de_servicios_etapa_2c`, `ERROR: test_servicios_de_jardin_con_su_mensaje_en_menu_barra_y_pie` y `FAILED (errors=2)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/datos.py b/tools/site/datos.py
index a930895..a427be7 100644
--- a/tools/site/datos.py
+++ b/tools/site/datos.py
@@ -56,6 +56,10 @@ PRECIOS = {
     "pasto_mayoreo_minimo_m2": 500,
     "mantenimiento_mes": 750,
     "diseno": 3000,
+    "diseno_completo": 6500,
+    "diseno_premium": 18000,
+    "diseno_premium_descuento_desde": 150000,
+    "mantenimiento_premium_mes": 1800,
     "riego_m2": (180, 320),
     "sintetico_instalado_m2": (385, 650),
     "sintetico_tienda_m2": 139,
@@ -78,6 +82,10 @@ ARRAIGO = "15 a 20 días"
 VISITA_COSTO = ("El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por "
                 "WhatsApp antes de agendar.")
 VISITA_COSTO_CORTO = "Visita para medir y cotizar: su costo depende de la ubicación"
+# Servicios de jardín (Etapa 2c): ahorro de agua del riego (publicado en main) y frecuencias de mantenimiento según el
+# plan y lo que necesita el jardín (decisión del dueño).
+RIEGO_AHORRO = "hasta 40%"
+FRECUENCIAS_MANTENIMIENTO = ("semanal", "cada 15 días", "cada 21 días", "mensual")
 LLEGADA_PASTO = "una vez por semana, generalmente los viernes"
 ANTICIPO = ("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
             "un anticipo.")
@@ -125,6 +133,35 @@ OPINIONES_PASTO_EN_ROLLO = (
      "facturaron sin problema y respetaron el calendario de entrega por etapas. Ya son nuestro proveedor recurrente.",
      "Arq. Patricia L.", "Constructora · Altamira · Proyecto 2,400 m²"),
 )
+# Opiniones con nombre que publicaban en main las páginas de diseño, mantenimiento y riego antes de la Etapa 2c, textuales.
+# PENDIENTE DEL DUEÑO: confirmar que son reales y que hay permiso (plan 2c, "Lo que aporta el dueño"). Si alguna no lo
+# es, se borra de aquí y su encabezado pasa a PARIDAD["retirados"] con el motivo; nunca se edita ni se inventa otra.
+OPINIONES_DISENO = (
+    ("Contratamos el Plan Completo para remodelar el jardín de la casa. Hicieron la visita, nos preguntaron qué nos "
+     "gustaba y qué no, y la propuesta visual que nos mandaron fue exactamente lo que teníamos en mente. El manual de "
+     "cuidados nos ha servido muchísimo.",
+     "Daniela M.", "Plan Completo · Residencial Tampico"),
+    ("Somos un hotel boutique en Altamira y necesitábamos entregables formales para el proyecto de áreas verdes. El Plan "
+     "Premium incluyó planos ejecutivos, render 3D y presentación para la junta. Muy profesional, justo lo que nuestro "
+     "comité necesitaba para aprobar.",
+     "Ing. Roberto S.", "Plan Premium · Hotel Boutique · Altamira"),
+)
+OPINIONES_MANTENIMIENTO = (
+    ("Tenemos contrato mensual desde hace más de 2 años. Vienen puntuales, el jardín siempre está impecable y me avisan "
+     "cuando detectan plagas o alguna planta con problemas. Ya no tengo que estar pendiente de nada.",
+     "Carolina R.", "Residencial · Tampico Zona Norte"),
+    ("Contratamos a Terra para mantener las áreas verdes de nuestra nave industrial en Altamira. Son más de 3,000 m² y "
+     "desde que llegaron se nota la diferencia. Presentan reporte fotográfico de cada visita y facturan puntuales.",
+     "Ing. Gerardo M.", "Industrial · Altamira Puerto"),
+)
+OPINIONES_RIEGO = (
+    ("Tenía el jardín seco porque se me olvidaba regar. Terra instaló el sistema en un día, me programaron los horarios "
+     "y ahora siempre está perfecto. Mi recibo de agua bajó casi a la mitad.",
+     "Roberto C.", "Residencial · Tampico"),
+    ("Instalaron el sistema de riego en las áreas verdes de nuestra planta industrial en Altamira. Llegaron a tiempo, el "
+     "diseño es eficiente y el equipo de calidad. 100% recomendados.",
+     "María V.", "Parque Industrial · Altamira"),
+)
 # Zonas con página propia (nombre visible, ruta) y las que se atienden por proyecto.
 ZONAS = (
     ("Lomas de Rosales y Vista Hermosa", "/jardineria-lomas-de-rosales-tampico"),
diff --git a/tools/site/mensajes_paginas.py b/tools/site/mensajes_paginas.py
index 8336e32..415e23c 100644
--- a/tools/site/mensajes_paginas.py
+++ b/tools/site/mensajes_paginas.py
@@ -5,11 +5,24 @@ Los textos son los de main; solo se corrigieron dos artículos que decían "Palm
 (duranta y nortes) y los huecos vacíos se marcan con ___ como en datos.MENSAJES. La firma se agrega en datos.con_firma.
 """
 
+# Servicios de jardín (Etapa 2c): la plantilla de main de cada portada, con los huecos marcados ___. Lo usan la portada y
+# el cierre de la página (tools/site/contenido/) y, por RUTAS, el menú, la barra móvil y el pie.
+SERVICIOS = {
+    "/diseno-jardines-tampico": ("Hola, me interesa el diseño de mi jardín.\nColonia: ___\nMetros aprox.: ___\n"
+                                 "Plan que me interesa: ___\nLes mando fotos del espacio."),
+    "/mantenimiento-jardines-tampico": ("Hola, quiero cotizar mantenimiento de jardín.\nColonia: ___\n"
+                                        "Metros aprox. del jardín: ___\nCasa o empresa: ___\n"
+                                        "Frecuencia (semanal, cada 15 días, cada 21 días o mensual): ___"),
+    "/sistema-riego-tampico": ("Hola, quiero cotizar riego automático.\nColonia: ___\nMetros aprox. del jardín: ___\n"
+                               "Tengo pasto, plantas o ambos: ___\nLes mando fotos del espacio."),
+}
+
 # Ruta exacta → (mensaje del menú y la barra, mensaje del pie o None para usar el mismo).
 RUTAS = {
     "/blog": ("Hola, vi el blog de Viveros Terra y quiero cotizar", None),
     "/catalogo": ("Hola, vi el catálogo y quiero cotizar una planta", None),
     "/precios": ("Hola, vi la lista de precios y quiero cotizar", "Hola, tengo una pregunta sobre precios"),
+    **{ruta: (texto, None) for ruta, texto in SERVICIOS.items()},
 }
 # Tienda y páginas de envío: el pie conserva su "pregunta"; el menú usa el mensaje de cotizar pasto sintético.
 PIE_TIPO = {
EOF
```

- [ ] **Step 4: Build y pruebas**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Expected: `plantillas: 0 de 25`, `shell: 3 de 108 páginas actualizadas` (el menú, la barra y el pie de las tres páginas llevan ya su mensaje) y luego `0 de 108`.
Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas tests.test_reglas tests.test_consistencia 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/datos.py tools/site/mensajes_paginas.py tools/site/tests/test_datos.py tools/site/tests/test_paginas.py public/diseno-jardines-tampico/index.html public/mantenimiento-jardines-tampico/index.html public/sistema-riego-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(datos): planes de diseño y mantenimiento, ahorro de riego, frecuencias y mensajes de los servicios de jardín" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Componentes de planes, fichas y garantía sin cifra

**Files:**
- Modify: `tools/site/componentes.py`, `public/css/terra.css`
- Test: `tools/site/tests/test_componentes.py`, `tools/site/tests/test_terra_css.py`

`opciones()` sigue dando el mismo HTML para lo que ya existía (sintético en Tampico): `desde` vale `True` por omisión y la línea de mensualidad solo aparece con `mensualidad: True`. `linea_mensualidad()` usa `mensualidades.planes()` (la fórmula de `vt-mensualidades.js`) y falla si el monto no alcanza ningún plazo, para que nadie publique una línea vacía. La rejilla de `.vt-modos` cambia porque con 3 planes a 768 px el botón (texto sin corte) desbordaba 27 px; con 2 opciones el resultado es el mismo que antes.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_componentes.py b/tools/site/tests/test_componentes.py
index 6ff068a..410b502 100644
--- a/tools/site/tests/test_componentes.py
+++ b/tools/site/tests/test_componentes.py
@@ -136,6 +136,60 @@ class BloquesTest(unittest.TestCase):
         self.assertEqual([unquote(t).split("\n")[0] for t in re.findall(r"text=([^\"&]+)", html)], ["Hola A", "Hola B"])
 
 
+class PlanesTest(unittest.TestCase):
+    """Etapa 2c: planes con precio cerrado, por cotización o sin precio, con línea de mensualidades; tarjetas de lo
+    que incluye un servicio y garantía sin cifra."""
+    BASE = {"rotulo": "Plan 1", "titulo": "Esencial", "unidad": "MXN", "detalle": "d", "puntos": ("p",),
+            "mensaje": "Hola, me interesa el Plan Terra Esencial"}
+
+    def test_linea_de_mensualidades_con_el_plazo_mas_largo(self):
+        self.assertEqual(c.linea_mensualidad(3000),
+                         "o en 3 mensualidades de ≈ $1,105 con tarjeta de crédito (total $3,315)")
+        self.assertEqual(c.linea_mensualidad(6500),
+                         "o en 6 mensualidades de ≈ $1,245 con tarjeta de crédito (total $7,468)")
+        self.assertEqual(c.linea_mensualidad(18000),
+                         "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)")
+        with self.assertRaises(ValueError):
+            c.linea_mensualidad(750)  # bajo el mínimo de $2,000 no hay plazos
+
+    def test_precio_cerrado_sin_desde_y_con_mensualidad(self):
+        html = c.opciones((dict(self.BASE, precio=3000, desde=False, mensualidad=True),), "servicio-diseno")
+        self.assertIn('<p class="vt-modo__precio"><span class="vt-precio-marca">$3,000</span> MXN', html)
+        self.assertIn('<small class="vt-modo__mes">o en 3 mensualidades de ≈ $1,105', html)
+        self.assertNotIn("desde ", html)
+
+    def test_precio_desde_por_omision_y_sin_mensualidad(self):
+        html = c.opciones((dict(self.BASE, precio=18000),), "servicio-diseno")
+        self.assertIn('desde <span class="vt-precio-marca">$18,000</span>', html)
+        self.assertNotIn("vt-modo__mes", html)
+
+    def test_por_cotizacion_y_sin_precio(self):
+        html = c.opciones((dict(self.BASE, precio_texto="Por cotización"), dict(self.BASE, titulo="Goteo")),
+                          "servicio-mantenimiento")
+        self.assertIn('<p class="vt-modo__precio">Por cotización <small>d</small></p>', html)
+        self.assertEqual(html.count('class="vt-modo__precio"'), 1)
+        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html),
+                         ["servicio-mantenimiento:opcion-1", "servicio-mantenimiento:opcion-2"])
+
+    def test_maximo_tres_opciones(self):
+        with self.assertRaises(ValueError):
+            c.opciones((self.BASE,) * 4, "servicio-diseno")
+
+    def test_fichas_sin_precio_ni_boton(self):
+        html = c.fichas(({"titulo": "Poda de pasto", "texto": "Corte parejo."},
+                         {"titulo": "Goteo", "texto": "A la raíz.", "puntos": ("Menos agua",)}))
+        self.assertTrue(html.startswith('<ul class="vt-modos vt-fichas">'))
+        self.assertIn("<h3>Poda de pasto</h3><p>Corte parejo.</p></li>", html)
+        self.assertIn('<ul class="vt-checks"><li>Menos agua</li></ul>', html)
+        self.assertNotIn("wa.me", html)
+
+    def test_garantia_con_y_sin_cifra(self):
+        g = {"titulo": "Garantía.", "id_titulo": "vt-h-garantia", "numero": 6, "rotulo": "Garantía", "resumen": "r",
+             "puntos": (("a", True), ("b", False)), "pie": "p"}
+        self.assertNotIn("vt-grande", c.garantia(g))
+        self.assertIn('<p class="vt-grande">30<small> días</small></p>', c.garantia(dict(g, grande="30", unidad="días")))
+
+
 class MedidorTest(unittest.TestCase):
     def test_html_del_medidor(self):
         html = c.medidor("prueba", "home")
diff --git a/tools/site/tests/test_terra_css.py b/tools/site/tests/test_terra_css.py
index 7653f05..7e522a8 100644
--- a/tools/site/tests/test_terra_css.py
+++ b/tools/site/tests/test_terra_css.py
@@ -152,7 +152,8 @@ class TerraCssTest(unittest.TestCase):
 
     def test_componentes_del_cuerpo_presentes(self):
         for selector in (".vt-pagina", ".vt-portada", ".vt-etiqueta", ".vt-datos", ".vt-medidor", ".vt-tabla",
-                         ".vt-pasos", ".vt-nota", ".vt-faq summary", ".vt-cierre", ".vt-sim .sim-plan"):
+                         ".vt-pasos", ".vt-nota", ".vt-faq summary", ".vt-cierre", ".vt-sim .sim-plan",
+                         ".vt-modo__precio .vt-modo__mes"):
             with self.subTest(selector=selector):
                 self.regla(selector)
         for token in ("--vt-text-h1", "--vt-text-h2", "--vt-text-h3", "--vt-text-precio", "--vt-space-section"):
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_componentes tests.test_terra_css 2>&1 | grep -E "FAILED"`
Expected: `FAILED (failures=2, errors=5)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/public/css/terra.css b/public/css/terra.css
index 2c80bc0..ef5bd14 100644
--- a/public/css/terra.css
+++ b/public/css/terra.css
@@ -456,12 +456,13 @@
 
 /* ---------- formas de contratar (máx. 3, cada una con su mensaje) ---------- */
 .vt-modos{display:grid;gap:20px;list-style:none}
-@media (min-width:768px){.vt-modos{grid-template-columns:repeat(auto-fit,minmax(0,1fr))}}
+@media (min-width:768px){.vt-modos{grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr))}}
 .vt-modo{display:grid;gap:14px;align-content:start;padding:24px 20px;border:1px solid var(--vt-line);background:var(--vt-card)}
 .vt-modo--rec{border:1.5px solid var(--vt-field)}
 .vt-pagina main .vt-modo p{margin:0}
 .vt-pagina main .vt-modo__n{font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
 .vt-modo__precio small{display:block;margin-top:4px;font-size:var(--vt-text-sm);color:var(--vt-muted)}
+.vt-modo__precio .vt-modo__mes{color:var(--vt-ink-2);font-weight:600}
 .vt-modo .vt-btn{width:100%}
 
 /* ---------- proceso NOSOTROS / TÚ / JUNTOS ---------- */
diff --git a/tools/site/componentes.py b/tools/site/componentes.py
index 34ab49e..2eb4ad9 100644
--- a/tools/site/componentes.py
+++ b/tools/site/componentes.py
@@ -243,21 +243,57 @@ def tabla_comparativa(columnas, filas, caption):
             f'<tbody>{cuerpo}</tbody></table>')
 
 
+def linea_mensualidad(contado):
+    """Plazo más largo disponible para un precio de contado, con la fórmula oficial (tools/pasto/mensualidades.py, la
+    misma de vt-mensualidades.js): "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)"."""
+    disponibles = [p for p in mensualidades.planes(contado) if p["disponible"]]
+    if not disponibles:
+        raise ValueError(f"{dinero(contado)}: no hay plazos de mensualidades para ese monto")
+    p = disponibles[-1]
+    return (f'o en {p["plazo"]} mensualidades de ≈ {dinero(p["mensualidad"])} con tarjeta de crédito '
+            f'(total {dinero(p["total"])})')
+
+
+def _precio_opcion(o):
+    """Renglón de precio de una opción: "desde $X unidad" (o sin "desde"), un texto propio o nada."""
+    if "precio" in o:
+        desde = "desde " if o.get("desde", True) else ""
+        mes = f'<small class="vt-modo__mes">{linea_mensualidad(o["precio"])}</small>' if o.get("mensualidad") else ""
+        return (f'<p class="vt-modo__precio">{desde}<span class="vt-precio-marca">{dinero(o["precio"])}</span> '
+                f'{o["unidad"]} <small>{o["detalle"]}</small>{mes}</p>')
+    if "precio_texto" in o:
+        return f'<p class="vt-modo__precio">{o["precio_texto"]} <small>{o["detalle"]}</small></p>'
+    return ""
+
+
 def opciones(items, tipo):
-    """Formas de contratar (máx. 3, spec §3.3), cada una con su precio "desde", lo que incluye, su nota y su propio
-    mensaje de WhatsApp. items: rotulo, titulo, precio (número), unidad, detalle, puntos, nota, mensaje, rec."""
+    """Formas de contratar o planes (máx. 3, spec §3.3), cada uno con su propio mensaje de WhatsApp (data-cta
+    <tipo>:opcion-<n>). items: rotulo, titulo, puntos, mensaje y, opcionales, precio (número) con unidad y detalle,
+    desde (False para un precio cerrado), mensualidad (True: línea con el plazo más largo), precio_texto (en vez de
+    precio: "Por cotización"), nota y rec (recomendado)."""
+    if len(items) > 3:
+        raise ValueError("máximo 3 opciones por página (spec §3.3)")
     filas = []
     for i, o in enumerate(items, 1):
         clase = "vt-modo vt-modo--rec" if o.get("rec") else "vt-modo"
         puntos = "".join(f"<li>{x}</li>" for x in o["puntos"])
         nota_html = f'<p class="vt-promesa">{o["nota"]}</p>' if o.get("nota") else ""
         filas.append(f'<li class="{clase}"><p class="vt-modo__n">{o["rotulo"]}</p><h3>{o["titulo"]}</h3>'
-                     f'<p class="vt-modo__precio">desde <span class="vt-precio-marca">{dinero(o["precio"])}</span> '
-                     f'{o["unidad"]} <small>{o["detalle"]}</small></p><ul class="vt-checks">{puntos}</ul>{nota_html}'
+                     f'{_precio_opcion(o)}<ul class="vt-checks">{puntos}</ul>{nota_html}'
                      f'{boton_wa(o["mensaje"], f"{tipo}:opcion-{i}")}</li>')
     return f'<ul class="vt-modos">{"".join(filas)}</ul>'
 
 
+def fichas(items):
+    """Tarjetas de lo que incluye un servicio, sin precio ni botón. items: titulo, texto y, opcional, puntos."""
+    filas = []
+    for f in items:
+        puntos = "".join(f"<li>{x}</li>" for x in f.get("puntos", ()))
+        lista = f'<ul class="vt-checks">{puntos}</ul>' if puntos else ""
+        filas.append(f'<li class="vt-modo"><h3>{f["titulo"]}</h3><p>{f["texto"]}</p>{lista}</li>')
+    return f'<ul class="vt-modos vt-fichas">{"".join(filas)}</ul>'
+
+
 def relacionados(items):
     """Tarjetas del sistema: foto, título con enlace (toda la tarjeta lo abre) y texto. items: titulo, href, texto, img,
     ancho, alto."""
@@ -303,13 +339,15 @@ def howto(nombre, items):
 
 
 def garantia(g):
-    """g: titulo, id_titulo, numero, rotulo, grande, unidad, resumen, puntos (texto, si_aplica), pie."""
+    """g: titulo, id_titulo, numero, rotulo, resumen, puntos (texto, si_aplica), pie y, opcionales, grande y unidad (la
+    cifra de la garantía; riego no tiene un plazo y la omite)."""
     no_aplica = ' class="vt-checks__no"'
+    cifra = f'<p class="vt-grande">{g["grande"]}<small> {g["unidad"]}</small></p>' if g.get("grande") else ""
     puntos = "".join(f'<li{"" if ok else no_aplica}>{t}</li>' for t, ok in g["puntos"])
     ident = esc(g["id_titulo"])
     return (f'<section class="vt-bloque vt-bloque--tinte" aria-labelledby="{ident}"><div class="vt-wrap vt-dos">'
             f'<div><p class="vt-bloque__no"><b>{g["numero"]:02d}</b>{g["rotulo"]}</p><h2 id="{ident}">'
-            f'{g["titulo"]}</h2><p class="vt-grande">{g["grande"]}<small> {g["unidad"]}</small></p>'
+            f'{g["titulo"]}</h2>{cifra}'
             f'<p class="vt-promesa">{g["resumen"]}</p></div><div><ul class="vt-checks">{puntos}</ul>'
             f'<p class="vt-promesa">{g["pie"]}</p></div></div></section>')
 
EOF
```

- [ ] **Step 4: Build (nuevo hash de `terra.css`) y pruebas**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Expected: `plantillas: 25 de 25` y `shell: 76 de 108` en la primera corrida (solo el hash del `<head>`), `0` en la segunda; `git status` muestra `public/css/terra.css`, un `public/css/terra.<hash>.css` nuevo, la copia vieja borrada y `tools/site/activos.json`.
Run: `cd tools/site && python3 -m unittest tests.test_componentes tests.test_terra_css tests.test_generar tests.test_activos 2>&1 | tail -1` y `python3 -c "import sys; sys.path.insert(0,'tools/site'); import activos,gzip; m=activos.minificar_css(open('public/css/terra.css').read()).encode(); print(len(gzip.compress(m,mtime=0)))"`
Expected: `OK` y `8432` (menos de 10,240).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/componentes.py tools/site/tests/test_componentes.py tools/site/tests/test_terra_css.py tools/site/activos.json public
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(componentes): planes con precio cerrado, por cotización o sin precio, línea de mensualidades, fichas y garantía sin cifra" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Plantilla de servicio con las secciones opcionales de 2c

**Files:**
- Modify: `tools/site/plantillas/servicio.py`
- Test: `tools/site/tests/test_plantilla_servicio.py`

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_plantilla_servicio.py` (archivo nuevo, completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/site/tests/test_plantilla_servicio.py <<'EOF'
"""Plantilla de servicio (tools/site/plantillas/servicio.py): las secciones opcionales que agrega la Etapa 2c."""
import copy
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
from plantillas import servicio  # noqa: E402

BASE = generar.cargar("pasto_en_rollo").CONTENIDO


def main_de(k):
    return re.search(r'<main id="main">(.*)</main>', servicio.render(k), re.S).group(1)


class PlantillaServicioTest(unittest.TestCase):
    def test_objecion_con_una_sola_tabla_y_rotulo_propio(self):
        k = copy.deepcopy(BASE)
        for clave in ("comparativa_2", "titulo_2"):
            del k["objecion"][clave]
        k["objecion"]["rotulo"] = "Frecuencia"
        conviene = main_de(k).split('id="vt-h-conviene"')[0].rsplit("<section", 1)[1]
        self.assertIn("<b>03</b>Frecuencia", conviene)
        cuerpo = main_de(k).split('id="vt-h-conviene"')[1].split("</section>")[0]
        self.assertEqual(cuerpo.count("<table"), 1)

    def test_opciones_con_tabla_nota_y_rotulo(self):
        k = copy.deepcopy(BASE)
        k["opciones"] = {"rotulo": "Planes", "titulo": "¿Cuánto cuesta?", "nota": "Nota de planes.",
                         "items": ({"rotulo": "Plan 1", "titulo": "A", "precio_texto": "Por cotización", "detalle": "d",
                                    "puntos": ("p",), "mensaje": "Hola A"},),
                         "tabla": {"titulo": "Compara", "columnas": ("Plan", "A"), "filas": (("Precio", "x"),),
                                   "caption": "c"}}
        html = main_de(k)
        opciones = html.split('id="vt-h-opciones"')[1].split("</section>")[0]
        self.assertIn('<h3 class="vt-mt">Compara</h3><table class="vt-tabla vt-tabla--comparar">', opciones)
        self.assertIn('<p class="vt-promesa">Nota de planes.</p>', opciones)
        self.assertIn("<b>02</b>Planes", html)

    def test_que_incluye_va_despues_de_las_opciones(self):
        k = copy.deepcopy(BASE)
        k["opciones"] = {"titulo": "Planes", "items": ({"rotulo": "1", "titulo": "A", "puntos": (), "mensaje": "Hola"},)}
        k["incluye"] = {"titulo": "Qué incluye cada visita", "items": ({"titulo": "Poda", "texto": "Corte."},)}
        html = main_de(k)
        self.assertLess(html.index('id="vt-h-opciones"'), html.index('id="vt-h-incluye"'))
        self.assertLess(html.index('id="vt-h-incluye"'), html.index('id="vt-h-precio"'))
        self.assertIn('<ul class="vt-modos vt-fichas">', html)

    def test_las_paginas_de_antes_no_cambian(self):
        """Pasto en rollo y sintético en Tampico salen idénticos (test_generar compara contra public/)."""
        self.assertNotIn("incluye", BASE)
        self.assertIn("comparativa_2", BASE["objecion"])


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_plantilla_servicio 2>&1 | tail -1`
Expected: `FAILED (failures=1, errors=2)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/plantillas/servicio.py b/tools/site/plantillas/servicio.py
index 68fab6b..4812483 100644
--- a/tools/site/plantillas/servicio.py
+++ b/tools/site/plantillas/servicio.py
@@ -5,8 +5,12 @@ pago (anticipo y mensualidades con tarjeta de crédito, con su simulador) → pr
 final. Las secciones que el contenido no trae se omiten (diseño, mantenimiento y riego no llevan Medidor de pasto).
 Opcionales desde 2b: formas de contratar (máx. 3, cada una con su mensaje), tabla comparativa de precios, cotizador de
 la tienda (tienda-pasto.js, con lista de cotización y barra de compra), visita al showroom y pago sin simulador (con
-los plazos de mensualidades). Páginas: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py) y
-/pasto-sintetico-tampico (contenido/sintetico_tampico.py)."""
+los plazos de mensualidades). Desde 2c: planes con precio cerrado, "por cotización" o sin precio y con línea de
+mensualidades, tabla comparativa bajo los planes, "qué incluye" en tarjetas, objeción con una sola tabla y garantía
+sin cifra. Páginas: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py), /pasto-sintetico-tampico
+(contenido/sintetico_tampico.py), /diseno-jardines-tampico (contenido/diseno_jardines.py),
+/mantenimiento-jardines-tampico (contenido/mantenimiento_jardines.py) y /sistema-riego-tampico
+(contenido/sistema_riego.py)."""
 import componentes as c
 import componentes_tienda as t
 from plantillas import base
@@ -44,11 +48,24 @@ def _precio(k, numero):
 
 
 def _opciones(k, numero):
+    """Formas de contratar o planes (máx. 3), cada uno con su mensaje; opcionales: tabla comparativa y nota debajo."""
     o = k["opciones"]
-    return c.bloque(numero, "Opciones", "vt-h-opciones", o["titulo"], c.opciones(o["items"], k["tipo"]), lede=o.get("lede"),
+    cuerpo = c.opciones(o["items"], k["tipo"])
+    if o.get("tabla"):
+        tb = o["tabla"]
+        cuerpo += f'<h3 class="vt-mt">{tb["titulo"]}</h3>' + c.tabla_comparativa(tb["columnas"], tb["filas"], tb["caption"])
+    if o.get("nota"):
+        cuerpo += f'<p class="vt-promesa">{o["nota"]}</p>'
+    return c.bloque(numero, o.get("rotulo", "Opciones"), "vt-h-opciones", o["titulo"], cuerpo, lede=o.get("lede"),
                     id_seccion="opciones")
 
 
+def _incluye(k, numero):
+    """Qué incluye el servicio, en tarjetas sin precio (mantenimiento: lo que se hace en cada visita)."""
+    i = k["incluye"]
+    return c.bloque(numero, "Qué incluye", "vt-h-incluye", i["titulo"], c.fichas(i["items"]), lede=i.get("lede"))
+
+
 def _aparte(items):
     """Columna junto al cotizador: (título, puntos, nota) por bloque."""
     salida = []
@@ -78,11 +95,14 @@ def _visita(k, numero):
 
 
 def _objecion(k, numero):
+    """La objeción principal en una tabla con su cierre; una segunda tabla es opcional (pasto en rollo trae dos)."""
     o = k["objecion"]
-    a, b = o["comparativa"], o["comparativa_2"]
-    cuerpo = (c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
-              + f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"]))
-    return c.bloque(numero, "Cuál te conviene", "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])
+    a = o["comparativa"]
+    cuerpo = c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
+    if o.get("comparativa_2"):
+        b = o["comparativa_2"]
+        cuerpo += f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"])
+    return c.bloque(numero, o.get("rotulo", "Cuál te conviene"), "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])
 
 
 def _pago(k, numero):
@@ -114,7 +134,7 @@ def render(k):
     g, f, ci, p = k["garantia"], k["faq"], k["cierre"], k["proceso"]
     secciones = [c.portada(k["portada"], tipo, k["migas"]), _prueba(k, 1)]
     numero = 2
-    for clave, armar in (("opciones", _opciones), ("precio", _precio), ("cotizador", _cotizador),
+    for clave, armar in (("opciones", _opciones), ("incluye", _incluye), ("precio", _precio), ("cotizador", _cotizador),
                          ("objecion", _objecion)):
         if clave in k:
             secciones.append(armar(k, numero))
EOF
```

- [ ] **Step 4: Nada publicado cambia**

Run: `python3 tools/site/build.py | tail -2 && cd tools/site && python3 -m unittest tests.test_plantilla_servicio tests.test_generar tests.test_pasto_en_rollo tests.test_tienda 2>&1 | tail -1`
Expected: `plantillas: 0 de 25 páginas escritas`, `shell: 0 de 108 páginas actualizadas` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/plantillas/servicio.py tools/site/tests/test_plantilla_servicio.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantilla): servicio con planes, tabla bajo los planes, qué incluye y objeción de una tabla" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Fotos de prueba a su tamaño

**Files:**
- Create: 9 × `public/img/obra/*.webp`

Las galerías viejas cargaban fotos de 240–380 KB. Se reducen 9 (la primera de cada página a 960 px porque va a lo ancho; las otras a 640 px). Las de diseño son propuestas visuales y su pie dice "Proyecto · referencia" (como el render de 2a) hasta que el dueño confirme que son obras terminadas.

- [ ] **Step 1: Reducir**

```bash
cd ~/dev/viverosterra-e2c
I=public/img; O=$I/obra
cwebp -quiet -q 72 -resize 960 0 $I/paisajismo-alberca-plantas-tampico.webp -o $O/diseno-jardin-alberca-tampico.webp
cwebp -quiet -q 72 -resize 640 0 $I/paisajismo-diseno-jardines-tampico.webp -o $O/diseno-jardin-paisajismo-tampico.webp
cwebp -quiet -q 72 -resize 640 0 $I/diseno-jardines-madero-altamira-pasto.webp -o $O/diseno-jardin-pasto-madero.webp
cwebp -quiet -q 72 -resize 960 0 $I/jardin-residencial-tropical-tampico.webp -o $O/mantenimiento-jardin-tropical-tampico.webp
cwebp -quiet -q 72 -resize 640 0 $I/jardineria-areas-verdes-tampico.webp -o $O/mantenimiento-areas-verdes-empresa.webp
cwebp -quiet -q 72 -resize 640 0 $I/jardin-residencial-plantas-pasto-tampico.webp -o $O/mantenimiento-jardin-residencial-pasto.webp
cwebp -quiet -q 72 -resize 960 0 $I/riego-pro-05.webp -o $O/riego-tecnico-sistema-industrial.webp
cwebp -quiet -q 72 -resize 640 0 $I/riego-tampico-05.webp -o $O/riego-aspersor-emergente-pasto.webp
cwebp -quiet -q 72 -resize 640 0 $I/riego-tampico-03.webp -o $O/riego-goteo-philodendron.webp
python3 -c "
import glob, os, struct
for p in sorted(glob.glob('public/img/obra/*.webp')):
    if not any(k in p for k in ('diseno-jardin', 'mantenimiento-a', 'mantenimiento-jardin-t', 'mantenimiento-jardin-r', 'riego-t', 'riego-asp', 'riego-g')): continue
    b = open(p, 'rb').read(30)
    w, h = (struct.unpack('<HH', b[26:30]) if b[12:16] == b'VP8 ' else (int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1))
    print(p.split('/')[-1], w & 0x3fff, h & 0x3fff, os.path.getsize(p) // 1024, 'KB')"
```

Expected (ancho × alto, y menos de 150 KB cada una): `diseno-jardin-alberca-tampico 960 640`, `diseno-jardin-paisajismo-tampico 640 427`, `diseno-jardin-pasto-madero 640 427`, `mantenimiento-areas-verdes-empresa 640 961`, `mantenimiento-jardin-residencial-pasto 640 961`, `mantenimiento-jardin-tropical-tampico 960 640`, `riego-aspersor-borde-pasto 700 875` (ya existía), `riego-aspersor-emergente-pasto 640 1423`, `riego-goteo-philodendron 640 1423`, `riego-tecnico-sistema-industrial 960 640`. Estas medidas son las que usan los módulos de contenido (`ancho`, `alto`).

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add public/img/obra/diseno-jardin-alberca-tampico.webp public/img/obra/diseno-jardin-paisajismo-tampico.webp public/img/obra/diseno-jardin-pasto-madero.webp public/img/obra/mantenimiento-jardin-tropical-tampico.webp public/img/obra/mantenimiento-areas-verdes-empresa.webp public/img/obra/mantenimiento-jardin-residencial-pasto.webp public/img/obra/riego-tecnico-sistema-industrial.webp public/img/obra/riego-aspersor-emergente-pasto.webp public/img/obra/riego-goteo-philodendron.webp
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(img): fotos de diseño, mantenimiento y riego a su tamaño para los pies FIG." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Diseño de jardines sale de la plantilla

**Files:**
- Create: `tools/site/contenido/diseno_jardines.py`, `tools/site/tests/test_servicios_jardin.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `tools/servicios/simulador.py`, `public/diseno-jardines-tampico/index.html`
- Delete: `tools/servicios/planes_diseno.py`
- Test: `tools/site/tests/test_generar.py`, `tools/site/tests/test_navegador.py`, `tools/servicios/tests/test_pagos.py`

Lo que cambia para el visitante: el formulario "Cotización Plan Terra" (`sendWA()` con selector de plan) desaparece; cada plan tiene su botón con su mensaje ("Hola, me interesa el Plan Terra Completo ($6,500)…") y su línea de mensualidades; la tabla "Compara los 3 planes" queda bajo los planes; la objeción "¿Y si al final no contratas la obra?" dice qué pasa con lo pagado (lo que decía main en el paso 5 y el FAQ); la garantía de plantas va condicionada con su enlace; "el diseño termina siendo gratuito" sale (se dice "se descuenta"); el bloque de autor con "+200 proyectos B2B" y "Certificación SENASICA" sale (cifras sin respaldo, ver dueño). La prueba de navegador del `window.open` firmado pasa a `/piedra-bola-rio-tampico`, que conserva `sendWA()` hasta 2f.

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_servicios_jardin.py` (archivo nuevo, completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/site/tests/test_servicios_jardin.py <<'EOF'
"""Diseño, mantenimiento y riego salen de la plantilla de servicio (Etapa 2c): secuencia del spec §3.3, un mensaje de
WhatsApp por plan, precios de datos.py, garantía condicionada, visita con su costo según la ubicación y JSON-LD de lo
visible. Cada página migrada agrega su fila a ESPERADO y su clase de pruebas propia."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import componentes  # noqa: E402
import datos  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

P = datos.PRECIOS
BASE_LD = {"Service", "FAQPage", "BreadcrumbList", "SpeakableSpecification"}
# ruta, secciones propias de la página (entre opciones y la objeción), cifras visibles y tipos del JSON-LD.
ESPERADO = {
    "diseno": {"ruta": "/diseno-jardines-tampico", "extra": (), "ld": BASE_LD,
               "cifras": ("$3,000", "$6,500", "desde $18,000", "en proyectos de más de $150,000")},
}


def pagina(clave):
    html = (paginas.PUBLIC / ESPERADO[clave]["ruta"].strip("/") / "index.html").read_text(encoding="utf-8")
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
    return html, main, textos_publicos(html), grafo


def mensajes_de(html, patron):
    """Textos de WhatsApp (con la firma) de los enlaces cuyo data-cta coincide con el patrón."""
    return [unquote(t) for t in re.findall(rf'data-cta="{patron}" href="https://wa\.me/\d+\?text=([^"]+)"', html)]


def opiniones_textuales(caso, clave, opiniones):
    _h, main, _t, _g = pagina(clave)
    prueba = main[main.index('id="vt-h-prueba"'):main.index('id="vt-h-opciones"')]
    for cita, nombre, detalle in opiniones:
        with caso.subTest(pagina=clave, nombre=nombre):
            caso.assertIn(f"<p>“{cita}”</p>", prueba)
            caso.assertIn(f"<b>{nombre}</b><span>{detalle}</span>", prueba)


class ComunTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        inicio = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', ':hero"', 'id="vt-h-prueba"', 'id="vt-h-opciones"')
        final = ('id="vt-h-conviene"', 'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-pago"', 'id="vt-h-faq"',
                 'id="vt-h-cobertura"', 'id="vt-h-rel"', 'class="vt-cierre"')
        for clave, e in ESPERADO.items():
            _h, main, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                posiciones = [main.index(m) for m in inicio + e["extra"] + final]
                self.assertEqual(posiciones, sorted(posiciones))
                self.assertEqual(len(re.findall(r"<h1\b", main)), 1)
                self.assertEqual(main.count('class="vt-pasos"'), 1)  # un solo proceso (auditoría 02 en riego)

    def test_sin_css_viejo_formularios_ni_parches_de_servicios(self):
        for clave in ESPERADO:
            html, _m, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertNotRegex(html, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
                for viejo in ("svc-hero", "plan-pay", "<form", "sendWA", "sendRW", "sim-titulo", "<style"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_tres_opciones_cada_una_con_su_mensaje(self):
        for clave, e in ESPERADO.items():
            html, _m, _t, _g = pagina(clave)
            tipo = paginas.contexto(e["ruta"])["tipo"]
            with self.subTest(pagina=clave):
                self.assertEqual(len(set(mensajes_de(html, rf"{tipo}:opcion-\d"))), 3)

    def test_portada_cierre_menu_y_barra_con_el_mensaje_de_la_pagina(self):
        for clave, e in ESPERADO.items():
            html, _m, _t, _g = pagina(clave)
            tipo = paginas.contexto(e["ruta"])["tipo"]
            esperado = datos.con_firma(mensajes_paginas.SERVICIOS[e["ruta"]])
            for seccion in ("hero", "cierre", "barra", "header"):
                with self.subTest(pagina=clave, seccion=seccion):
                    self.assertEqual(mensajes_de(html, f"{tipo}:{seccion}")[0], esperado)

    def test_precios_de_datos(self):
        for clave, e in ESPERADO.items():
            _h, _m, texto, _g = pagina(clave)
            for cifra in e["cifras"]:
                with self.subTest(pagina=clave, cifra=cifra):
                    self.assertIn(cifra, texto)

    def test_copy_del_dueno(self):
        for clave in ESPERADO:
            _h, main, texto, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertIn(datos.PROMESA_COMPLETA, texto)
                self.assertIn(datos.ANTICIPO, texto)
                self.assertIn("mensualidades con tarjeta de crédito", texto)
                self.assertIn('href="/politicas#mensualidades"', main)
                self.assertNotRegex(texto, r"(?i)\bMSI\b|sin intereses|oasis|pagas cuando|liquida|visita\w*\W+"
                                           r"(?:\w+\W+){0,4}?(?:gratis|gratuit|sin costo)")

    def test_garantia_enlaza_sus_condiciones(self):
        for clave in ESPERADO:
            _h, main, _t, _g = pagina(clave)
            garantia = main[main.index('id="vt-h-garantia"'):main.index('id="vt-h-pago"')]
            with self.subTest(pagina=clave):
                self.assertRegex(garantia, r'href="/politicas(?:#garantia-plantas)?"')

    def test_json_ld_conservado_y_faq_de_lo_visible(self):
        for clave, e in ESPERADO.items():
            _h, main, _t, grafo = pagina(clave)
            nodos = {n["@type"]: n for n in grafo}
            visibles = [componentes.texto_plano(s) for s in re.findall(r"<summary>(.*?)</summary>", main)]
            with self.subTest(pagina=clave):
                self.assertEqual(set(nodos), e["ld"])
                self.assertEqual([q["name"] for q in nodos["FAQPage"]["mainEntity"]], visibles)
                self.assertEqual(len(visibles), 8)


class DisenoTest(unittest.TestCase):
    def test_tres_planes_con_su_mensaje_y_mensualidad(self):
        html, main, texto, grafo = pagina("diseno")
        planes = mensajes_de(html, r"servicio-diseno:opcion-\d")
        for plan, precio in (("Esencial", "$3,000"), ("Completo", "$6,500"), ("Premium", "desde $18,000")):
            with self.subTest(plan=plan):
                self.assertTrue(any(m.startswith(f"Hola, me interesa el Plan Terra {plan} ({precio})") for m in planes))
        for linea in ("o en 3 mensualidades de ≈ $1,105 con tarjeta de crédito (total $3,315)",
                      "o en 6 mensualidades de ≈ $1,245 con tarjeta de crédito (total $7,468)",
                      "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)"):
            self.assertIn(linea, texto)
        self.assertEqual(main.count('class="vt-modo__mes"'), 3)
        self.assertIn("Compara los 3 planes en detalle", texto)
        ofertas = next(n for n in grafo if n["@type"] == "Service")["offers"]
        self.assertEqual([o["price"] for o in ofertas], [str(P["diseno"]), str(P["diseno_completo"]),
                                                         str(P["diseno_premium"])])

    def test_garantia_de_plantas_condicionada(self):
        _h, main, texto, _g = pagina("diseno")
        self.assertIn("las plantas que sembramos", main)
        self.assertIn('href="/politicas#garantia-plantas"', main)
        self.assertNotRegex(texto, r"(?i)gratuit")

    def test_opiniones_de_main_textuales(self):
        opiniones_textuales(self, "diseno", datos.OPINIONES_DISENO)


if __name__ == "__main__":
    unittest.main()
EOF
```
```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/servicios/tests/test_pagos.py b/tools/servicios/tests/test_pagos.py
index cefed75..fdb6de0 100644
--- a/tools/servicios/tests/test_pagos.py
+++ b/tools/servicios/tests/test_pagos.py
@@ -5,15 +5,10 @@ from pathlib import Path
 sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
 import hero  # noqa: E402
-import planes_diseno  # noqa: E402
 from pages import PAGES  # noqa: E402
 
-CARD = """<div class="flex items-baseline gap-2">
-            <span class="text-4xl font-display font-bold text-primary">{p}</span>
-            <span class="text-gray-400 text-sm">MXN</span>
-          </div>
-          <p class="text-gray-500 text-xs mt-1">Entrega</p>"""
-PAGE = "\n".join(CARD.format(p=p) for p in ("$3,000", "$6,500", "$18,000")) + '\n<span>$3,000</span>'
+# Salen de tools/site/plantillas/ (Etapas 2a y 2c): ningún parche de tools/servicios las toca.
+CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico")
 
 
 class PagoNotaTest(unittest.TestCase):
@@ -30,29 +25,14 @@ class PagoNotaTest(unittest.TestCase):
         cfg = {k: v for k, v in self.cfg().items() if k != "pago_nota"}
         self.assertNotIn("svc-hero__pay", hero.hero_html(cfg))
 
-    def test_solo_dos_paginas_con_pago_nota(self):
+    def test_solo_riego_con_pago_nota(self):
         con = sorted(slug for slug, cfg in PAGES.items() if cfg.get("pago_nota"))
-        self.assertEqual(con, ["diseno-jardines-tampico", "sistema-riego-tampico"])
+        self.assertEqual(con, ["sistema-riego-tampico"])
 
     def test_paginas_con_plantilla_fuera_de_los_parches(self):
-        self.assertNotIn("pasto-en-rollo-tampico", PAGES)
-
-
-class PlanesDisenoTest(unittest.TestCase):
-    def test_plazo_mas_largo_por_precio(self):
-        html = planes_diseno.apply_html(PAGE)
-        self.assertIn("o en 3 mensualidades de ≈ $1,105 con tarjeta (total $3,315)", html)
-        self.assertIn("o en 6 mensualidades de ≈ $1,245 con tarjeta (total $7,468)", html)
-        self.assertIn("o en 12 mensualidades de ≈ $1,852 con tarjeta (total $22,220)", html)
-
-    def test_idempotente(self):
-        once = planes_diseno.apply_html(PAGE)
-        self.assertEqual(planes_diseno.apply_html(once), once)
-        self.assertEqual(once.count("plan-pay"), 3)
-
-    def test_pagina_real_tiene_tres_lineas(self):
-        html = planes_diseno.PAGE.read_text(encoding="utf-8")
-        self.assertEqual(html.count('class="plan-pay'), 3)
+        for slug in CON_PLANTILLA:
+            with self.subTest(slug=slug):
+                self.assertNotIn(slug, PAGES)
 
 
 if __name__ == "__main__":
diff --git a/tools/site/tests/test_generar.py b/tools/site/tests/test_generar.py
index ea054fd..7f09235 100644
--- a/tools/site/tests/test_generar.py
+++ b/tools/site/tests/test_generar.py
@@ -17,8 +17,8 @@ import shell  # noqa: E402
 
 class GenerarTest(unittest.TestCase):
     def test_paginas_registradas_tienen_contexto(self):
-        esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/pasto-sintetico",
-                      "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
+        esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
+                      "/pasto-sintetico", "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                      + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
         self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
         for ruta, salida, _p, _c in generar.PAGINAS:
diff --git a/tools/site/tests/test_navegador.py b/tools/site/tests/test_navegador.py
index 6a28692..2f0f364 100644
--- a/tools/site/tests/test_navegador.py
+++ b/tools/site/tests/test_navegador.py
@@ -192,8 +192,9 @@ class NavegadorTest(unittest.TestCase):
     def test_window_open_de_whatsapp_sale_firmado(self):
         page = self.pagina(1440)
         page.add_init_script("window.__abiertos = []; window.open = (url) => { window.__abiertos.push(String(url)); return null; };")
-        page.goto(self.base + "/diseno-jardines-tampico/", wait_until="load")
-        page.evaluate("() => sendWA('Hola, me interesa el Plan Terra')")
+        # Diseño sale de su plantilla desde la Etapa 2c (un botón por plan); piedra bola conserva sendWA hasta la 2f.
+        page.goto(self.base + "/piedra-bola-rio-tampico/", wait_until="load")
+        page.evaluate("() => sendWA('Hola, quiero cotizar piedra bola de río')")
         abiertos = page.evaluate("() => window.__abiertos")
         self.assertEqual(len(abiertos), 1)
         self.assertEqual(abiertos[0].count("viverosterra.com"), 1)
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)`
Expected: `FAILED (failures=11, errors=5)` y `FAILED (failures=2)`.

- [ ] **Step 3: El contenido**

`tools/site/contenido/diseno_jardines.py` (archivo nuevo, completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/site/contenido/diseno_jardines.py <<'EOF'
"""Contenido de /diseno-jardines-tampico (Plan Terra en 3 niveles). Solo datos: la plantilla es
tools/site/plantillas/servicio.py, con planes (cada uno con su mensaje y su línea de mensualidades), tabla comparativa,
objeción "¿y si no contrato la obra?", proceso, garantía de plantas condicionada y simulador.

Precios de datos.PRECIOS (Esencial $3,000, Completo $6,500, Premium desde $18,000 y su descuento en proyectos de más
de $150,000); mensualidades con la fórmula de tools/pasto/mensualidades.py. Título, descripción, canonical, Open Graph,
Twitter Card, Service y migas del JSON-LD como estaban publicados en main (los acentos del JSON-LD los arregla la
Etapa 4); FAQPage sale de las preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero, mensualidades

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/diseno-jardines-tampico"
OBRA = "/img/obra"
ESENCIAL, COMPLETO, PREMIUM = P["diseno"], P["diseno_completo"], P["diseno_premium"]
DESCUENTO_PREMIUM = dinero(P["diseno_premium_descuento_desde"])
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
MENSAJE = mensajes_paginas.SERVICIOS["/diseno-jardines-tampico"]
CONDICIONES = '<a href="/politicas#garantia-plantas">ver condiciones</a>'

META = {
    "title": "Diseño de Jardines Tampico · Plan Terra",
    "description": (f"Diseño profesional de jardines en Tampico. Plan Terra en 3 niveles: Esencial {dinero(ESENCIAL)}, "
                    f"Completo {dinero(COMPLETO)}, Premium desde {dinero(PREMIUM)}. Descuento al contratar."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", f"Diseño de Jardines Tampico | Plan Terra desde {dinero(ESENCIAL)} — Viveros Terra"),
        ("og:description", ("Diseño profesional de jardines en Tampico, Madero y Altamira. Plan Terra en 3 niveles: "
                            f"Esencial desde {dinero(ESENCIAL)}, Completo {dinero(COMPLETO)} y Premium con planos AutoCAD "
                            "y render 3D. Cotiza gratis por WhatsApp.")),
        ("og:image", f"{SITE}/img/diseno-jardines-tampico-viveros-terra.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}

# Service y migas como estaban publicados (texto sin acentos incluido: el grafo único es de la Etapa 4).
_PROVEEDOR = {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
              "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                          "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}}
SERVICIO = {
    "@type": "Service", "serviceType": "Diseno de Jardines", "name": "Diseno de Jardines Tampico - Plan Terra",
    "description": ("Servicio profesional de diseno de jardines residenciales, corporativos y de desarrollo en Tampico, "
                    "Ciudad Madero y Altamira. Plan Terra con propuesta visual, seleccion de plantas y planos segun el "
                    "nivel contratado."),
    "provider": _PROVEEDOR,
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
    "offers": [
        {"@type": "Offer", "name": "Plan Terra Esencial", "price": str(ESENCIAL), "priceCurrency": "MXN",
         "description": ("Propuesta visual con montajes, diseno basado en gustos, lista de plantas, cotizacion y asesoria "
                         "7 dias. Entrega 3 a 5 dias habiles.")},
        {"@type": "Offer", "name": "Plan Terra Completo", "price": str(COMPLETO), "priceCurrency": "MXN",
         "description": ("Visita tecnica, toma de medidas, diseno detallado, fichas de plantas, cuantificacion de "
                         "materiales, manual de cuidados PDF, consulta estacional 6 meses y garantia de arraigo 30 dias "
                         "en las plantas que sembramos, con el riego indicado. Entrega 10 dias habiles.")},
        {"@type": "Offer", "name": "Plan Terra Premium", "price": str(PREMIUM), "priceCurrency": "MXN",
         "description": ("Proyecto ejecutivo con 2 visitas tecnicas, planos AutoCAD, render 3D alta resolucion, plan de "
                         "riego tecnico, plan de mantenimiento 12 meses, arquitecto paisajista asignado, presentacion "
                         "ejecutiva y revision post-ejecucion. Entrega 15 a 21 dias habiles.")},
    ],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Diseno de Jardines Tampico", "item": URL},
]}

PLANES = (
    {"rotulo": "Plan 1 · Remoto", "titulo": "Esencial", "precio": ESENCIAL, "desde": False, "unidad": "MXN",
     "mensualidad": True, "detalle": "Visualiza tu jardín antes de invertir · entrega en 3 a 5 días hábiles",
     "puntos": ("Propuesta visual con montajes fotográficos personalizados",
                "Diseño basado en el estudio de tus gustos y preferencias",
                "Lista de plantas seleccionadas para el clima de Tampico",
                "Cotización detallada del proyecto completo",
                "Asesoría por WhatsApp con el diseñador (7 días)",
                "Garantía de precio: cotización respetada 30 días",
                f"Los {dinero(ESENCIAL)} se descuentan si contratas la obra"),
     "mensaje": (f"Hola, me interesa el Plan Terra Esencial ({dinero(ESENCIAL)}).\nColonia: ___\nMetros aprox.: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Plan 2 · Con visita", "titulo": "Completo", "precio": COMPLETO, "desde": False, "unidad": "MXN",
     "mensualidad": True, "rec": True, "detalle": "Del diseño al jardín terminado · entrega en 10 días hábiles",
     "puntos": ("Todo lo del Esencial",
                "Visita técnica al sitio (1 hora con el diseñador)",
                "Toma de medidas profesional y análisis del terreno",
                "Selección de plantas con la ficha técnica de cada una",
                "Cuantificación completa de materiales",
                "Manual de cuidados personalizado en PDF (10+ páginas)",
                "Consulta estacional de 30 min a los 6 meses y carpeta digital del proyecto",
                # Sin enlace dentro de la lista (vt-checks es grid): las condiciones se enlazan en la garantía.
                "Garantía de arraigo de 30 días en las plantas que sembramos nosotros, con el riego indicado",
                f"Los {dinero(COMPLETO)} se descuentan si contratas la obra"),
     "mensaje": (f"Hola, me interesa el Plan Terra Completo ({dinero(COMPLETO)}).\nColonia: ___\nMetros aprox.: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Plan 3 · Proyecto ejecutivo", "titulo": "Premium", "precio": PREMIUM, "unidad": "MXN",
     "mensualidad": True, "detalle": "Hoteles, corporativos, fraccionamientos y desarrollos · entrega en 15 a 21 días hábiles",
     "puntos": ("Todo lo del Completo",
                "2 visitas técnicas (diagnóstico y presentación en sitio)",
                "Planos ejecutivos en AutoCAD (planta, alzados y cortes)",
                "Render 3D profesional en alta resolución",
                "Plan de riego técnico y plan de mantenimiento de 12 meses",
                "Arquitecto paisajista asignado y presentación ejecutiva (PDF y PowerPoint)",
                "Revisión a 1 año: 2 visitas después de la obra",
                f"Factura {datos.FACTURA} con complemento de servicios",
                f"Se descuenta en proyectos de más de {DESCUENTO_PREMIUM}"),
     "mensaje": (f"Hola, me interesa el Plan Terra Premium (desde {dinero(PREMIUM)}).\nEmpresa o tipo de proyecto: ___\n"
                 "Ubicación: ___\nMetros aprox.: ___")},
)

COMPARA = {
    "titulo": "Compara los 3 planes en detalle",
    "columnas": ("Incluye", f"Esencial {dinero(ESENCIAL)}", f"Completo {dinero(COMPLETO)}",
                 f"Premium desde {dinero(PREMIUM)}"),
    "filas": (
        ("Diseño basado en tus gustos", "Sí", "Detallado", "Detallado"),
        ("Lista de plantas", "Básica", "Con fichas técnicas", "Con fichas técnicas"),
        ("Asesoría por WhatsApp", "7 días", "Incluida", "Incluida"),
        ("Visita técnica", "—", "1", "2"),
        ("Manual de cuidados en PDF", "—", "Sí", "Ampliado"),
        ("Cuantificación de materiales", "—", "Sí", "Sí"),
        ("Consulta estacional a los 6 meses", "—", "Sí", "Sí"),
        ("Garantía de arraigo en plantas que sembramos", "—", "30 días", "30 días"),
        ("Planos AutoCAD y render 3D", "—", "—", "Sí"),
        ("Plan de mantenimiento de 12 meses", "—", "—", "Sí"),
        ("Revisión después de la obra (1 año)", "—", "—", "2 visitas"),
        ("Descuento al contratar la obra", "Total", "Total", f"En proyectos de más de {DESCUENTO_PREMIUM}"),
        ("Tiempo de entrega", "3 a 5 días", "10 días", "15 a 21 días"),
    ),
    "caption": f"Precios {datos.ANIO} con IVA. Días hábiles desde que recibimos las fotos.",
}

PREGUNTAS = (
    ("¿Cuánto cuesta el diseño de un jardín en Tampico?",
     f"El Plan Terra tiene 3 niveles: Esencial ({dinero(ESENCIAL)}), Completo ({dinero(COMPLETO)}) y Premium (desde "
     f"{dinero(PREMIUM)}), con IVA. En Esencial y Completo el costo se descuenta completo si contratas la obra con "
     f"Viveros Terra; en el Premium, en proyectos de más de {DESCUENTO_PREMIUM}."),
    ("¿Qué diferencia al Plan Esencial del Completo?",
     "El Esencial es remoto: nos envías fotos y te regresamos la propuesta visual y la cotización en 3 a 5 días hábiles. "
     "El Completo incluye una visita técnica con toma de medidas, cuantificación de materiales, manual de cuidados en PDF "
     "y acompañamiento después de la entrega, con consulta estacional y garantía de arraigo en las plantas que sembramos "
     f"nosotros ({CONDICIONES})."),
    ("¿Cuándo conviene el Plan Premium?",
     "Cuando necesitas entregables técnicos formales para un comité, una junta directiva, inversionistas o una aprobación "
     "corporativa. Incluye planos ejecutivos en AutoCAD, render 3D, plan de mantenimiento a 12 meses y presentación "
     "ejecutiva. Es para hoteles, corporativos, fraccionamientos y desarrollos."),
    ("¿Se descuenta el costo del diseño si contrato la ejecución?",
     "Sí. En los planes Esencial y Completo el monto se descuenta completo. En el Premium aplica a proyectos con "
     f"presupuesto de ejecución de más de {DESCUENTO_PREMIUM}."),
    ("¿Cómo se eligen las plantas para mi jardín?",
     "Con el estudio de tus gustos y preferencias elegimos plantas para el clima cálido y húmedo de Tampico, según el sol "
     "que recibe cada zona, el tipo de suelo, el mantenimiento que puedes darle y el estilo que buscas (tropical, "
     'minimalista, mediterráneo). Puedes ver especies en el <a href="/catalogo">catálogo del vivero</a>.'),
    ("¿Puedo ver ejemplos de diseños anteriores?",
     "Sí. En esta página ves algunos proyectos, y por WhatsApp te enviamos carpetas con casos residenciales, corporativos "
     "y hoteleros parecidos al tuyo para que sepas qué esperar."),
    ("¿Cuánto tiempo tardan en entregar el diseño?",
     "Plan Esencial: 3 a 5 días hábiles desde que recibimos las fotos. Plan Completo: 10 días hábiles. Plan Premium: 15 a "
     "21 días hábiles por los entregables técnicos."),
    ("¿Facturan CFDI 4.0?",
     f"Sí. Emitimos factura {datos.FACTURA} en todos los planes. El Premium incluye factura con complemento de servicios "
     "profesionales para que lo registres como proyecto de inversión."),
)

PASOS = (
    {"titulo": "Envías fotos y cuéntanos tu visión", "quien": "tu", "cuando": "Por WhatsApp",
     "texto": ("Nos mandas fotos del espacio, medidas aproximadas, tu estilo preferido y el uso que le darás al "
               "jardín.")},
    {"titulo": "Estudio de gustos y preferencias", "quien": "juntos", "cuando": "Antes de diseñar",
     "texto": ("Tu asesor te manda un cuestionario breve: colores, texturas, cuánto mantenimiento puedes darle, si hay "
               "mascotas o niños y cuánto sol recibe cada zona.")},
    {"titulo": "Elegimos el Plan Terra correcto para ti", "quien": "nosotros", "cuando": "Al cotizar",
     "texto": ("Te recomendamos Esencial, Completo o Premium según la complejidad del proyecto y si necesitas "
               "entregables técnicos.")},
    {"titulo": "Entrega del diseño", "quien": "nosotros", "cuando": "3 a 21 días hábiles",
     "texto": ("Recibes la propuesta visual, la cotización del proyecto y los entregables de tu plan: 3 a 5 días "
               "(Esencial), 10 días (Completo) o 15 a 21 días (Premium).")},
    {"titulo": "Ejecución del proyecto (opcional)", "quien": "juntos", "cuando": "Cuando tú decidas",
     "texto": ("Si lo ejecutamos nosotros, el costo del diseño se descuenta del proyecto. Si no, el diseño es tuyo para "
               "cuando quieras usarlo.")},
)

FIGURAS = (
    {"src": f"{OBRA}/diseno-jardin-alberca-tampico.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Escalones de concreto entre helechos y plantas tropicales junto a una alberca.",
     "lugar": "Jardín tropical junto a la alberca", "etapa": "Proyecto · referencia"},
    {"src": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427, "numero": 3,
     "alt": "Jardín residencial con pasto, arriates y plantas ornamentales.",
     "lugar": "Paisajismo residencial", "etapa": "Proyecto · referencia"},
    {"src": f"{OBRA}/diseno-jardin-pasto-madero.webp", "ancho": 640, "alto": 427, "numero": 4,
     "alt": "Jardín con pasto San Agustín y plantas en Ciudad Madero.",
     "lugar": "Jardín con pasto en Madero", "etapa": "Proyecto · referencia"},
)

CONTENIDO = {
    "tipo": "servicio-diseno",
    "prefijo": "diseno",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Diseño de jardines", None)),
    "portada": {
        "kicker": "Diseño de jardines · Tampico, Madero y Altamira",
        "h1": 'Diseño de jardines en Tampico <span class="vt-serif">con plan y presupuesto claros</span>',
        "lede": ("Te entregamos el diseño, la lista de plantas y materiales y el costo de la obra. Si nos contratas para "
                 f"hacerla, el diseño se descuenta (en el Premium, en proyectos de más de {DESCUENTO_PREMIUM})."),
        "etiqueta": {
            "codigo": "Diseño · Plan Terra", "aviso": "Con IVA", "nombre": "Plan Terra Esencial",
            "antes": "Propuesta visual · 3 a 5 días", "monto": dinero(ESENCIAL), "unidad": "MXN",
            "filas": (("Plan Completo, con visita", dinero(COMPLETO)), ("Plan Premium", f"desde {dinero(PREMIUM)}")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Se descuenta si contratas la obra · <a href="#opciones">compara los 3 planes</a> · '
                    f'<a href="#mensualidades">mensualidades con tarjeta de crédito</a> desde {DESDE_MENSUALIDADES}'),
        "foto": {"src": "/img/portadas/diseno-jardines-tampico-proyecto-sm.webp",
                 "srcset": ("/img/portadas/diseno-jardines-tampico-proyecto-sm.webp 560w, "
                            "/img/portadas/diseno-jardines-tampico-proyecto.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1574, "numero": 1,
                 "alt": "Jardín residencial diseñado por Viveros Terra en Tampico",
                 "lugar": "Proyecto de diseño de jardín", "etapa": "Tampico"},
    },
    "prueba": {
        "titulo": "Jardines que hemos diseñado en Tampico",
        "lede": "Propuestas y jardines del Plan Terra en casas, hoteles y desarrollos de la zona.",
        "figuras": FIGURAS,
        "nota": ("Si ya sabes qué plantas quieres y dónde van, no necesitas un plan de diseño: arma tu lista en el "
                 '<a href="/catalogo">catálogo</a> y te la cotizamos directo.', "Antes de contratar"),
        # La opinión de diseño aprobada de la home y las dos que publicaba esta página en main (pendientes de
        # confirmación del dueño: datos.OPINIONES_DISENO).
        "titulo_opinion": "Lo que dicen quienes contrataron diseño",
        "opiniones": datos.OPINIONES[1:2] + datos.OPINIONES_DISENO,
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "opciones": {
        "rotulo": "Planes",
        "titulo": "¿Cuánto cuesta un diseño de jardín en Tampico?",
        "lede": (f"Desde {dinero(ESENCIAL)} con el Plan Terra, en 3 niveles: Esencial {dinero(ESENCIAL)}, Completo "
                 f"{dinero(COMPLETO)} y Premium desde {dinero(PREMIUM)}, con IVA. Incluye la propuesta de diseño, la "
                 "lista de plantas y materiales y la cotización de la obra; el costo se descuenta si contratas el "
                 f'proyecto. Precios {datos.ANIO}; lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "items": PLANES,
        "tabla": COMPARA,
    },
    "objecion": {
        "rotulo": "Tu diseño",
        "titulo": "¿Y si al final no contratas la obra?",
        "lede": ("El diseño es tuyo: lo puedes ejecutar cuando quieras, con nosotros o por tu cuenta. Si lo hacemos "
                 "nosotros, lo que pagaste se descuenta."),
        "comparativa": {
            "columnas": ("Plan", "Si contratas la obra con nosotros", "Si no la contratas"),
            "filas": (
                (f"Esencial · {dinero(ESENCIAL)}", f"Se descuentan los {dinero(ESENCIAL)}",
                 "Te quedas con la propuesta visual, la lista de plantas y la cotización"),
                (f"Completo · {dinero(COMPLETO)}", f"Se descuentan los {dinero(COMPLETO)}",
                 "Te quedas con el diseño, las fichas de plantas, la cuantificación y el manual de cuidados"),
                (f"Premium · desde {dinero(PREMIUM)}", f"Se descuenta en proyectos de más de {DESCUENTO_PREMIUM}",
                 "Te quedas con los planos, el render, el plan de riego y el plan de mantenimiento"),
            ),
            "caption": "Lo que pasa con el pago del diseño.",
            "cierre": "Garantía de precio: la cotización de la obra se respeta 30 días.",
        },
    },
    "proceso": {"titulo": "Del primer WhatsApp a tu jardín ejecutado",
                "lede": "Cinco pasos; el último solo si decides que ejecutemos la obra.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo de 30 días en las plantas que sembramos.", "grande": "30", "unidad": "días",
        "resumen": "En las plantas que sembramos nosotros al ejecutar tu proyecto, con el riego indicado.",
        "puntos": (
            ("Si una planta que sembramos no prende en 30 días y se regó como te indicamos, la reponemos sin costo.",
             True),
            ("Garantía de precio: la cotización de la obra se respeta 30 días.", True),
            (f"El costo del diseño se descuenta si contratas la obra (en el Premium, en proyectos de más de "
             f"{DESCUENTO_PREMIUM}).", True),
            (f"Factura {datos.FACTURA} en todos los planes.", True),
            ("No cubre falta o exceso de riego, plantas movidas de lugar ni plantas que siembras por tu cuenta.", False),
        ),
        "pie": '<a href="/politicas#garantia-plantas">Lee las condiciones de la garantía de plantas</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} El diseño y la obra se cotizan por separado; los dos se pueden pagar de contado o "
                 f"en mensualidades con tarjeta de crédito desde {DESDE_MENSUALIDADES}."),
        "puntos": (
            "Cada plan muestra su precio de contado y su plazo más largo con tarjeta de crédito.",
            "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
            ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos antes "
             'de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>'),
        ),
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "el diseño de mi jardín", "monto": COMPLETO},
    },
    "faq": {"titulo": "Todo sobre el Plan Terra", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Listo para ver cómo se vería tu jardín?",
        "lede": ("Envíanos fotos de tu espacio por WhatsApp y dinos qué plan te interesa. Si no estás seguro, te "
                 "recomendamos uno."),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Diseñamos jardines en Tampico, Madero y Altamira.",
        "lede": "Casas, hoteles, corporativos y desarrollos de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo San Agustín", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"Pasto desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Sistema de Riego", "href": "/sistema-riego-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": f"Automatizado · Ahorra {datos.RIEGO_AHORRO} de agua"},
            {"titulo": "Mantenimiento de Jardines", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": f"Desde {dinero(P['mantenimiento_mes'])}/mes · Poda y cuidados"},
        ),
    },
}

PARIDAD = {
    "reemplazos": {
        "Diseño de jardines con plan y presupuesto claros": "Diseño de jardines en Tampico con plan y presupuesto claros",
        "Elige el plan que se ajusta a tu proyecto": "¿Cuánto cuesta un diseño de jardín en Tampico?",
        # Las preguntas del JSON-LD sin acentos: el FAQPage sale ahora de las preguntas visibles.
        "Cuanto cuesta el diseno de un jardin en Tampico?": "¿Cuánto cuesta el diseño de un jardín en Tampico?",
        "Que incluye el Plan Terra?": "¿Qué diferencia al Plan Esencial del Completo?",
        "Se descuenta el costo del diseno si contrato la ejecucion?": (
            "¿Se descuenta el costo del diseño si contrato la ejecución?"),
        "Tardan cuanto tiempo en entregar el diseno?": "¿Cuánto tiempo tardan en entregar el diseño?",
        "Como se eligen las plantas para mi jardin?": "¿Cómo se eligen las plantas para mi jardín?",
    },
    "retirados": {
        "Diseño de jardines profesional con acompañamiento": (
            "La definición del Plan Terra queda en la entrada de la portada y en la respuesta directa de los planes."),
        "Cotización Plan Terra": (
            "El formulario que armaba el mensaje con un selector de plan (sendWA) se sustituye por un botón con su "
            "propio mensaje en cada plan (spec §3.3: un mensaje por plan) y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor con cifras sin respaldo en datos.py (+200 proyectos B2B, certificación SENASICA); la "
            "entidad y el autor son de la Etapa 4. El dueño confirma esas cifras (plan 2c)."),
        "$90": "“Complementa tu proyecto” (tierra negra, mármol, tezontle) sale; los materiales siguen en el menú y el pie.",
        "$1,500": "“Complementa tu proyecto” (tierra negra, mármol, tezontle) sale; los materiales siguen en el menú y el pie.",
        "$150": "“Aplica +$150k” de la tabla de planes ahora se escribe completo: “en proyectos de más de $150,000”.",
    },
}
EOF
```

- [ ] **Step 4: Registrar la página y sacarla de `tools/servicios`**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/servicios/pages.py b/tools/servicios/pages.py
index 81e7068..adc3589 100644
--- a/tools/servicios/pages.py
+++ b/tools/servicios/pages.py
@@ -17,7 +17,8 @@ GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
 DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
 VARIEDADES = ("+200", "Variedades en el vivero")
 
-# /pasto-en-rollo-tampico y la home salen de tools/site/plantillas/ desde la Etapa 2a: este script ya no las toca.
+# La home y /pasto-en-rollo-tampico (Etapa 2a) y /diseno-jardines-tampico (Etapa 2c) salen de tools/site/plantillas/:
+# este script ya no las toca.
 PAGES = {
     "mayoreo-pasto-tampico": dict(
         eyebrow="Constructoras · Fraccionamientos · Industria",
@@ -39,16 +40,6 @@ PAGES = {
         alt="Jardinero de Viveros Terra podando pasto en un jardín de Tampico", caption="Poda y mantenimiento en Tampico.",
         wa=guided("Hola, quiero cotizar mantenimiento de jardín.", "Colonia", "Metros aprox. del jardín", "Casa o empresa"),
     ),
-    "diseno-jardines-tampico": dict(
-        title="Diseño de jardines", accent="con plan y presupuesto claros",
-        price_pre="Plan Esencial", price="$3,000", price_unit="", price_alt="· Completo $6,500 · Premium desde $18,000",
-        lede="Te entregamos el diseño, la lista de plantas y materiales y el costo de la obra. Si nos contratas para hacerlo, el diseño se descuenta.",
-        facts=[("3 a 5 días", "Entrega del plan Esencial"), ("Se descuenta", "Si contratas la obra"), GARANTIA_PLANTAS],
-        img="/img/diseno-jardines-tampico-proyecto.webp", img_pos="center 55%",
-        alt="Jardín residencial diseñado por Viveros Terra en Tampico", caption="Proyecto de diseño de jardín en Tampico.",
-        wa=guided("Hola, me interesa el diseño de mi jardín.", "Colonia", "Metros aprox.", "Plan que me interesa"),
-        pago_nota="Paga en mensualidades con tarjeta de crédito en cotizaciones desde $2,000.",
-    ),
     "sistema-riego-tampico": dict(
         title="Riego automático", accent="para jardines en Tampico",
         price_pre="De", price="$180 a $320", price_unit="/m²", price_alt="· según el tipo de sistema",
diff --git a/tools/servicios/simulador.py b/tools/servicios/simulador.py
index e1598a4..796b345 100644
--- a/tools/servicios/simulador.py
+++ b/tools/servicios/simulador.py
@@ -11,10 +11,9 @@ from html import escape
 from pathlib import Path
 
 ROOT = Path(__file__).resolve().parents[2] / "public"
-# /pasto-en-rollo-tampico trae su simulador desde tools/site/plantillas/servicio.py (Etapa 2a).
+# /pasto-en-rollo-tampico (2a) y /diseno-jardines-tampico (2c) traen su simulador desde tools/site/plantillas/servicio.py.
 PAGES = (
     ("sistema-riego-tampico", "un sistema de riego", 18000),
-    ("diseno-jardines-tampico", "el diseño de mi jardín", 6500),
 )
 SCRIPTS = (
     '<script src="/js/vt-mensualidades.js?v=20261104" defer></script>',
diff --git a/tools/site/generar.py b/tools/site/generar.py
index a25afa3..97b6795 100644
--- a/tools/site/generar.py
+++ b/tools/site/generar.py
@@ -24,6 +24,7 @@ PAGINAS = (
     ("/", "index.html", "inicio", "inicio"),
     ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
     ("/pasto-sintetico-tampico", "pasto-sintetico-tampico/index.html", "servicio", "sintetico_tampico"),
+    ("/diseno-jardines-tampico", "diseno-jardines-tampico/index.html", "servicio", "diseno_jardines"),
     ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
     ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
 ) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
EOF
```
```bash
cd ~/dev/viverosterra-e2c
git rm tools/servicios/planes_diseno.py
```

- [ ] **Step 5: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Run: `python3 tools/site/paridad.py informe /diseno-jardines-tampico`
Expected: `plantillas: 1 de 26` y luego `0 de 26`; el informe con `ok` en `encabezados`, `faq`, `precios`, `enlaces`, `meta` y `jsonld_tipos`.

Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_corregir_datos 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1); (cd tools/site && python3 -m unittest tests.test_navegador.NavegadorTest.test_window_open_de_whatsapp_sale_firmado 2>&1 | tail -1)`
Expected: `OK`, `OK`, `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/contenido/diseno_jardines.py tools/site/tests/test_servicios_jardin.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_navegador.py tools/servicios/pages.py tools/servicios/simulador.py tools/servicios/tests/test_pagos.py public/diseno-jardines-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(diseno): el Plan Terra sale de la plantilla de servicio con un mensaje y una mensualidad por plan" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Mantenimiento de jardines sale de la plantilla

**Files:**
- Create: `tools/site/contenido/mantenimiento_jardines.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `public/mantenimiento-jardines-tampico/index.html`
- Test: `tools/site/tests/test_servicios_jardin.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_consistencia.py`, `tools/servicios/tests/test_pagos.py`

Lo que cambia: tres planes (Residencial básico desde $750/mes, Residencial premium desde $1,800/mes, Empresa e industria por cotización), cada uno con su mensaje (auditoría 02); las frecuencias semanal, cada 15, cada 21 días o mensual "según tu plan y lo que necesita tu jardín"; "jardinero" en el H1, en lo que incluye y en la cobertura (auditoría 03); la visita inicial con su costo según ubicación; la garantía es "sin permanencia forzada" (cancelas con 30 días de aviso, como decía main) y enlaza la garantía de plantas; el pago es mensual con factura, y las mensualidades con tarjeta solo se ofrecen para trabajos desde $2,000 (el plan de $750 no alcanza el mínimo). Salen el rango "aprox. $6–$12 por m²" (no es dato oficial), "Complementa tu proyecto" y el bloque de autor.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/servicios/tests/test_pagos.py b/tools/servicios/tests/test_pagos.py
index fdb6de0..3f2cb82 100644
--- a/tools/servicios/tests/test_pagos.py
+++ b/tools/servicios/tests/test_pagos.py
@@ -8,7 +8,7 @@ import hero  # noqa: E402
 from pages import PAGES  # noqa: E402
 
 # Salen de tools/site/plantillas/ (Etapas 2a y 2c): ningún parche de tools/servicios las toca.
-CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico")
+CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico", "mantenimiento-jardines-tampico")
 
 
 class PagoNotaTest(unittest.TestCase):
diff --git a/tools/site/tests/test_consistencia.py b/tools/site/tests/test_consistencia.py
index 4aabfc7..ff7b1ec 100644
--- a/tools/site/tests/test_consistencia.py
+++ b/tools/site/tests/test_consistencia.py
@@ -24,7 +24,7 @@ LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
 PRECIOS = datos.PRECIOS
 # Páginas que todavía mencionan la visita sin su costo. Solo puede encoger: diseño, mantenimiento y riego salen de su
 # plantilla en las Tareas 7 a 9 de la Etapa 2c y las quitan de aquí.
-VISITA_COSTO_PENDIENTES = frozenset({"mantenimiento-jardines-tampico/index.html", "sistema-riego-tampico/index.html"})
+VISITA_COSTO_PENDIENTES = frozenset({"sistema-riego-tampico/index.html"})
 
 PROHIBIDAS = (
     ("promesa de respuesta vieja",
diff --git a/tools/site/tests/test_generar.py b/tools/site/tests/test_generar.py
index 7f09235..5b0c8b7 100644
--- a/tools/site/tests/test_generar.py
+++ b/tools/site/tests/test_generar.py
@@ -18,7 +18,7 @@ import shell  # noqa: E402
 class GenerarTest(unittest.TestCase):
     def test_paginas_registradas_tienen_contexto(self):
         esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
-                      "/pasto-sintetico", "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
+                      "/mantenimiento-jardines-tampico", "/pasto-sintetico", "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                      + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
         self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
         for ruta, salida, _p, _c in generar.PAGINAS:
diff --git a/tools/site/tests/test_servicios_jardin.py b/tools/site/tests/test_servicios_jardin.py
index e90948c..6950f0a 100644
--- a/tools/site/tests/test_servicios_jardin.py
+++ b/tools/site/tests/test_servicios_jardin.py
@@ -23,6 +23,8 @@ BASE_LD = {"Service", "FAQPage", "BreadcrumbList", "SpeakableSpecification"}
 ESPERADO = {
     "diseno": {"ruta": "/diseno-jardines-tampico", "extra": (), "ld": BASE_LD,
                "cifras": ("$3,000", "$6,500", "desde $18,000", "en proyectos de más de $150,000")},
+    "mantenimiento": {"ruta": "/mantenimiento-jardines-tampico", "extra": ('id="vt-h-incluye"',), "ld": BASE_LD,
+                      "cifras": ("$750", "desde $1,800", "Por cotización")},
 }
 
 
@@ -148,5 +150,27 @@ class DisenoTest(unittest.TestCase):
         opiniones_textuales(self, "diseno", datos.OPINIONES_DISENO)
 
 
+class MantenimientoTest(unittest.TestCase):
+    def test_un_mensaje_por_plan(self):
+        """Auditoría 02: los 4 CTA mandaban el mismo texto; ahora el plan elegido viaja al chat."""
+        html, _m, texto, _g = pagina("mantenimiento")
+        planes = mensajes_de(html, r"servicio-mantenimiento:opcion-\d")
+        self.assertIn(f"Residencial básico (desde ${P['mantenimiento_mes']}/mes)", planes[0])
+        self.assertIn(f"Residencial premium (desde ${P['mantenimiento_premium_mes']:,}/mes)", planes[1])
+        self.assertIn("empresa o industria", planes[2])
+        self.assertGreaterEqual(len(set(mensajes_de(html, r"servicio-mantenimiento:[a-z0-9-]+"))), 4)
+        for frecuencia in datos.FRECUENCIAS_MANTENIMIENTO:
+            self.assertIn(frecuencia, texto)
+
+    def test_visita_con_costo_y_jardinero(self):
+        _h, main, texto, _g = pagina("mantenimiento")
+        self.assertIn('href="/politicas#garantia-plantas"', main)
+        self.assertIn(datos.VISITA_COSTO, texto)
+        self.assertIn("jardinero", texto.split("Preguntas")[0])  # auditoría 03: "jardinero Tampico"
+
+    def test_opiniones_de_main_textuales(self):
+        opiniones_textuales(self, "mantenimiento", datos.OPINIONES_MANTENIMIENTO)
+
+
 if __name__ == "__main__":
     unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar tests.test_consistencia 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)`
Expected: `FAILED (failures=9, errors=6)` y `FAILED (failures=1)`.

- [ ] **Step 3: El contenido**

`tools/site/contenido/mantenimiento_jardines.py` (archivo nuevo, completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/site/contenido/mantenimiento_jardines.py <<'EOF'
"""Contenido de /mantenimiento-jardines-tampico (jardinero y mantenimiento mensual). Solo datos: la plantilla es
tools/site/plantillas/servicio.py, con 3 planes (cada uno con su propio mensaje de WhatsApp: auditoría 02, "el plan
elegido no viaja al chat"), tabla comparativa, lo que incluye cada visita, frecuencia por temporada, proceso, garantía
sin permanencia forzada y pago mensual.

Precios de datos.PRECIOS (desde $750/mes; residencial premium desde $1,800/mes, publicado en main); frecuencias de
datos.FRECUENCIAS_MANTENIMIENTO; visita con datos.VISITA_COSTO (su costo depende de la ubicación; nunca gratis). Título, descripción, canonical, Open Graph,
Twitter Card, Service y migas como estaban publicados; FAQPage de las preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/mantenimiento-jardines-tampico"
OBRA = "/img/obra"
BASICO, PREMIUM = P["mantenimiento_mes"], P["mantenimiento_premium_mes"]
FRECUENCIAS = ", ".join(datos.FRECUENCIAS_MANTENIMIENTO[:-1]) + " o " + datos.FRECUENCIAS_MANTENIMIENTO[-1]
MENSAJE = mensajes_paginas.SERVICIOS["/mantenimiento-jardines-tampico"]

META = {
    "title": f"Mantenimiento de Jardines Tampico · desde {dinero(BASICO)}/mes",
    "description": (f"Mantenimiento profesional de jardines en Tampico desde {dinero(BASICO)}/mes. Poda, fertilización y "
                    "control de plagas. Planes residencial, empresarial e industrial."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", f"Mantenimiento de Jardines Tampico desde {dinero(BASICO)}/mes | Viveros Terra"),
        ("og:description", (f"Mantenimiento profesional de jardines en Tampico, Madero y Altamira desde "
                            f"{dinero(BASICO)}/mes. Poda, fertilización, control de plagas y cuidados programados. "
                            "Residencial, empresarial e industrial. Cotiza gratis por WhatsApp.")),
        ("og:image", f"{SITE}/img/mantenimiento-jardines-poda-pasto-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}

SERVICIO = {
    "@type": "Service", "serviceType": "Mantenimiento de Jardines", "name": "Mantenimiento de Jardines Tampico",
    "description": ("Servicio profesional de mantenimiento de jardines residenciales, corporativos e industriales en "
                    "Tampico, Ciudad Madero y Altamira. Incluye poda, fertilizacion, control de plagas y revision "
                    f"general. Desde {BASICO} pesos mensuales con cotizacion personalizada segun el espacio."),
    "provider": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
                 "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                             "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}},
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
    "offers": {"@type": "Offer", "priceCurrency": "MXN", "price": str(BASICO),
               "description": (f"Servicio mensual desde {BASICO} pesos con cotizacion personalizada segun tamano, tipo "
                               "y ubicacion del jardin.")},
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Mantenimiento de Jardines Tampico", "item": URL},
]}

PLANES = (
    {"rotulo": "Plan 1 · Hasta 200 m²", "titulo": "Residencial básico", "precio": BASICO, "unidad": "/mes",
     "detalle": "Visita mensual; cada 21 días en lluvias si tu jardín lo pide",
     "puntos": ("Poda de pasto, arbustos y plantas", "Fertilización trimestral", "Control de plagas a solicitud",
                "Limpieza y recolección de residuos", "Reporte con fotos de cada visita"),
     "mensaje": (f"Hola, me interesa el plan de mantenimiento Residencial básico (desde {dinero(BASICO)}/mes).\n"
                 "Colonia: ___\nMetros aprox. del jardín: ___\nFrecuencia que busco (mensual o cada 21 días): ___")},
    {"rotulo": "Plan 2 · 200 a 500 m²", "titulo": "Residencial premium", "precio": PREMIUM, "unidad": "/mes",
     "rec": True, "detalle": "Visita cada 15 días",
     "puntos": ("Poda especializada de pasto, arbustos y palmas", "Fertilización mensual",
                "Control de plagas preventivo", "Revisión del sistema de riego", "Reporte con fotos de cada visita"),
     "mensaje": (f"Hola, me interesa el plan de mantenimiento Residencial premium (desde {dinero(PREMIUM)}/mes).\n"
                 "Colonia: ___\nMetros aprox. del jardín: ___\nTengo palmas o sistema de riego: ___")},
    {"rotulo": "Plan 3 · 500 m² o más", "titulo": "Empresa e industria", "precio_texto": "Por cotización",
     "detalle": f"Visita semanal con cuadrilla · REPSE {datos.REPSE} y factura {datos.FACTURA}",
     "puntos": ("Poda con cuadrilla", "Fertilización quincenal", "Programa anual de control de plagas",
                "Operación del sistema de riego", "Contrato de servicios y reporte con fotos de cada visita"),
     "mensaje": ("Hola, me interesa el plan de mantenimiento para empresa o industria.\nEmpresa: ___\nUbicación: ___\n"
                 f"m² de áreas verdes: ___\nFrecuencia que buscan ({FRECUENCIAS}): ___")},
)

COMPARA = {
    "titulo": "Planes de Mantenimiento — comparativa por tipo de jardín",
    "columnas": ("Plan", "Residencial básico", "Residencial premium", "Empresa e industria"),
    "filas": (
        ("Tamaño ideal", "Hasta 200 m²", "200 a 500 m²", "500 m² o más"),
        ("Frecuencia", "Mensual", "Cada 15 días", "Semanal"),
        ("Poda", "Incluida", "Especializada", "Con cuadrilla"),
        ("Fertilización", "Trimestral", "Mensual", "Quincenal"),
        ("Control de plagas", "A solicitud", "Preventivo", "Programa anual"),
        ("Riego automatizado", "No incluido", "Revisión incluida", "Operación incluida"),
        ("Precio", f"desde {dinero(BASICO)}/mes", f"desde {dinero(PREMIUM)}/mes", "Cotización"),
    ),
    "caption": f"Precios {datos.ANIO} con IVA. La frecuencia final depende de tu plan y de lo que necesita tu jardín.",
}

INCLUYE = (
    {"titulo": "Poda de pasto",
     "texto": ("Corte parejo a la altura de cada variedad. El San Agustín se mantiene entre 5 y 8 cm para conservar la "
               "humedad con el calor.")},
    {"titulo": "Poda de arbustos y plantas",
     "texto": "Poda de formación y sanitaria de arbustos, setos y plantas, con la técnica de cada especie."},
    {"titulo": "Fertilización programada",
     "texto": "Calendario según especies, temporada y tipo de suelo, para que el pasto siga verde todo el año."},
    {"titulo": "Control de plagas",
     "texto": ("Monitoreo y tratamiento preventivo de las plagas de Tampico: gusano del pasto, chinches, hormigas "
               "cortadoras y hongos por exceso de humedad.")},
    {"titulo": "Limpieza y recolección",
     "texto": "Retiro de hojas, ramas y residuos después de cada servicio, y traslado de la basura vegetal."},
    {"titulo": "Revisión general",
     "texto": "El jardinero revisa el pasto, las plantas y el riego, y te reporta cualquier problema con su recomendación."},
)

PREGUNTAS = (
    ("¿Cuánto cuesta el mantenimiento mensual?",
     f"Desde {dinero(BASICO)} al mes en jardines residenciales de hasta 200 m², y desde {dinero(PREMIUM)} al mes en "
     "jardines de 200 a 500 m² con visita cada 15 días. El precio exacto depende del tamaño, las plantas, el nivel de "
     f"servicio y la ubicación. {datos.VISITA_COSTO}"),
    ("¿Con qué frecuencia vienen al jardín?",
     f"Según tu plan y lo que necesita tu jardín: {FRECUENCIAS}. En temporada de lluvias (junio a septiembre) el pasto "
     "crece rápido y conviene cada 15 o 21 días; en temporada seca (octubre a mayo), mensual."),
    ("¿Qué incluye cada visita?",
     "Poda de pasto y arbustos, fertilización según el calendario, control preventivo de plagas, limpieza y recolección "
     "de residuos, y revisión general del jardín. Si hay sistema de riego, el jardinero revisa que funcione bien."),
    ("¿Puedo contratar sin haber hecho el jardín con Terra?",
     "Sí. Atendemos jardines existentes sin importar quién los instaló. En la visita revisamos el estado actual, "
     f"identificamos problemas y te proponemos el plan mensual adecuado. {datos.VISITA_COSTO}"),
    ("¿Trabajan con empresas, hoteles y parques industriales?",
     "Sí. Atendemos corporativos, hoteles, fraccionamientos, escuelas, parques industriales y gobierno. Emitimos factura "
     f"{datos.FACTURA}, contamos con REPSE {datos.REPSE}, trabajamos con contrato de servicios y adaptamos el calendario "
     "a la operación del cliente."),
    ("¿Hay permanencia forzada o puedo cancelar?",
     "No hay permanencia forzada. El contrato es mensual y renovable, y puedes cancelar con 30 días de aviso."),
    ("¿Qué pasa si detectan una plaga o problema?",
     "Te lo reportamos de inmediato con fotos y una recomendación. Si el tratamiento cabe en tu plan, lo hacemos en la "
     "misma visita; si requiere un tratamiento especializado o materiales adicionales, te mandamos la cotización para "
     "que la autorices."),
    ("¿Hacen mantenimiento correctivo además del preventivo?",
     "Sí. Si el jardín está descuidado, primero hacemos un servicio correctivo para ponerlo en condiciones, que se cotiza "
     "aparte del mantenimiento mensual. Después entramos al ritmo de mantenimiento programado."),
)

PASOS = (
    {"titulo": "Visita inicial", "quien": "nosotros", "cuando": "Antes de cotizar",
     "texto": (f"{datos.VISITA_COSTO_CORTO}. Revisamos el estado del jardín, medimos el área, identificamos las plantas y revisamos "
               "el riego si lo hay.")},
    {"titulo": "Plan personalizado", "quien": "juntos", "cuando": "Al cotizar",
     "texto": (f"Definimos contigo la frecuencia ({FRECUENCIAS}), el alcance (poda, fertilización, plagas, riego) y el "
               "precio mensual fijo.")},
    {"titulo": "Primera visita técnica", "quien": "nosotros", "cuando": "Primera visita",
     "texto": ("Los jardineros llegan a la hora acordada, hacen la primera intervención completa y detectan cualquier "
               "problema de plagas, nutrición o riego.")},
    {"titulo": "Mantenimiento programado", "quien": "nosotros", "cuando": "Según el calendario",
     "texto": "Poda de pasto y arbustos, fertilización, control de plagas, limpieza y revisión del riego en cada visita."},
    {"titulo": "Reportes mensuales con fotos", "quien": "juntos", "cuando": "Después de cada visita",
     "texto": ("Recibes un reporte con fotos de lo realizado y del estado del jardín. Si algo requiere atención "
               "especial, te avisamos antes de actuar.")},
)

FIGURAS = (
    {"src": f"{OBRA}/mantenimiento-jardin-tropical-tampico.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Jardín residencial tropical con pasto y plantas recién podadas.",
     "lugar": "Jardín residencial tropical", "etapa": "Mantenimiento mensual"},
    {"src": f"{OBRA}/mantenimiento-areas-verdes-empresa.webp", "ancho": 640, "alto": 961, "numero": 3,
     "alt": "Áreas verdes de una empresa con pasto cortado y arriates.",
     "lugar": "Áreas verdes de empresa", "etapa": "Mantenimiento programado"},
    {"src": f"{OBRA}/mantenimiento-jardin-residencial-pasto.webp", "ancho": 640, "alto": 961, "numero": 4,
     "alt": "Jardín residencial con pasto parejo y plantas ornamentales.",
     "lugar": "Jardín residencial", "etapa": "Después de la visita"},
)

SECTORES = (
    ("Residenciales", "Casas y privadas"),
    ("Empresas y oficinas", "Contrato de servicios con factura"),
    ("Hoteles y restaurantes", "Jardines de imagen"),
    ("Fraccionamientos", "Áreas comunes"),
    ("Parques industriales", f"REPSE {datos.REPSE}"),
    ("Escuelas e instituciones", "Áreas verdes y patios"),
)

CONTENIDO = {
    "tipo": "servicio-mantenimiento",
    "prefijo": "mantenimiento",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Mantenimiento de jardines", None)),
    "portada": {
        "kicker": "Mantenimiento de jardines · Tampico, Madero y Altamira",
        "h1": 'Mantenimiento de jardines y jardinero en Tampico <span class="vt-serif">con visitas programadas</span>',
        "lede": ("Poda, fertilización, control de plagas y revisión del riego para casas, fraccionamientos y empresas. "
                 f"Vamos {FRECUENCIAS}, según tu plan y lo que necesita tu jardín."),
        "etiqueta": {
            "codigo": "Jardín · mensual", "aviso": "Con IVA", "nombre": "Mantenimiento de jardín",
            "antes": "Residencial · desde", "monto": dinero(BASICO), "unidad": "/mes",
            "filas": (("Residencial premium", f"desde {dinero(PREMIUM)} /mes"), ("Empresa e industria", "por cotización")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'REPSE {datos.REPSE} y factura {datos.FACTURA} para empresas · '
                    '<a href="#opciones">elige tu plan</a> · sin permanencia forzada'),
        "foto": {"src": "/img/portadas/mantenimiento-jardines-poda-pasto-tampico-sm.webp",
                 "srcset": ("/img/portadas/mantenimiento-jardines-poda-pasto-tampico-sm.webp 560w, "
                            "/img/portadas/mantenimiento-jardines-poda-pasto-tampico.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Jardinero de Viveros Terra podando pasto en un jardín de Tampico",
                 "lugar": "Poda de pasto", "etapa": "Tampico"},
    },
    "prueba": {
        "titulo": "Jardines que mantenemos en Tampico",
        "lede": "Casas, empresas y áreas verdes de la zona con mantenimiento programado.",
        "figuras": FIGURAS,
        "nota": ("Si tu jardín está muy descuidado, la primera visita no es de mantenimiento: es un correctivo que se "
                 "cotiza aparte. Te lo decimos antes de empezar.", "En la visita inicial"),
        # La opinión de mantenimiento aprobada de la home y las dos que publicaba esta página en main (pendientes de
        # confirmación del dueño: datos.OPINIONES_MANTENIMIENTO).
        "titulo_opinion": "Lo que dicen nuestros clientes mensuales",
        "opiniones": datos.OPINIONES[3:4] + datos.OPINIONES_MANTENIMIENTO,
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "opciones": {
        "rotulo": "Planes",
        "titulo": "¿Cuánto cuesta el mantenimiento de jardín en Tampico?",
        "lede": (f"Desde {dinero(BASICO)} al mes en jardines residenciales de hasta 200 m², con poda, fertilización y "
                 f"control de plagas; desde {dinero(PREMIUM)} al mes de 200 a 500 m² o con palmas y riego. Empresas, "
                 f"fraccionamientos e industria se cotizan con REPSE {datos.REPSE} y factura {datos.FACTURA}. Precios "
                 f'{datos.ANIO} con IVA; lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "items": PLANES,
        "tabla": COMPARA,
        "nota": ("Para jardines de hasta 200 m², el plan básico es suficiente. Si tu jardín tiene palmas grandes o sistema "
                 "de riego, el premium cada 15 días da mejor resultado a largo plazo."),
    },
    "incluye": {
        "titulo": "Servicios de mantenimiento profesional",
        "lede": "Cada visita sigue el mismo protocolo, y el reporte con fotos te dice qué se hizo.",
        "items": INCLUYE,
    },
    "objecion": {
        "rotulo": "Frecuencia",
        "titulo": "Dos temporadas, dos ritmos de mantenimiento",
        "lede": "Ajustamos la frecuencia al ritmo real de crecimiento de tu jardín en Tampico, dentro de tu plan.",
        "comparativa": {
            "columnas": ("Temporada", "Meses", "Qué pasa en el jardín", "Frecuencia recomendada"),
            "filas": (
                ("Temporada de lluvias", "Junio a septiembre",
                 "El pasto y las plantas crecen más rápido con la humedad y el calor.",
                 "Cada 15 o 21 días; semanal en jardines grandes"),
                ("Temporada seca", "Octubre a mayo",
                 "Crece más lento, pero necesita fertilización y revisar el riego para seguir verde.",
                 "Mensual o cada 21 días"),
            ),
            "caption": "Frecuencia según la temporada en Tampico.",
            "cierre": f"La frecuencia final ({FRECUENCIAS}) la fijamos contigo según tu plan y lo que necesita tu jardín.",
        },
    },
    "proceso": {"titulo": "Cómo contratar mantenimiento de jardines en 5 pasos",
                "lede": "Para que tu jardín esté siempre en condiciones sin que tengas que estar pendiente.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Sin permanencia forzada: contrato mensual renovable.", "grande": "30",
        "unidad": "días de aviso para cancelar",
        "resumen": "Te quedas porque el servicio es constante, no porque te obliguemos.",
        "puntos": (
            ("Contrato mensual renovable; puedes cancelar con 30 días de aviso.", True),
            ("Precio mensual fijo según tu plan, sin sorpresas.", True),
            ("Si detectamos una plaga o un problema, te lo reportamos con fotos; si cabe en tu plan, lo atendemos en la "
             "misma visita.", True),
            (f"Factura {datos.FACTURA} y contrato de servicios; REPSE {datos.REPSE} para empresas.", True),
            ("Los tratamientos especializados, los materiales adicionales y el correctivo de un jardín descuidado se "
             "cotizan aparte.", False),
        ),
        "pie": ('<a href="/politicas#garantia-plantas">Las plantas que sembramos nosotros tienen 30 días de garantía de '
                "arraigo, con el riego indicado (ver condiciones)</a>"),
    },
    "pago": {
        "titulo": "Cómo se paga: cada mes, con factura.",
        "lede": (f"{datos.ANTICIPO} Después pagas cada mes el precio fijo de tu plan, por transferencia, efectivo o "
                 "tarjeta."),
        "puntos": (
            "Precio mensual fijo según tu plan y la frecuencia acordada.",
            f"Factura {datos.FACTURA} para persona física o moral.",
            ("El correctivo inicial, una obra de jardín o un sistema de riego se pueden pagar en mensualidades con tarjeta "
             "de crédito: el total a plazos es mayor que el de contado. "
             '<a href="/politicas#mensualidades">Condiciones</a>'),
        ),
    },
    "faq": {"titulo": "Todo sobre mantenimiento de jardines", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Tu jardín necesita mantenimiento profesional?",
        "lede": (f"Dinos tu colonia, los metros de tu jardín y si es casa o empresa. Agendamos una visita para medir y "
                 f"cotizar. {datos.VISITA_COSTO}"),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Jardinero y mantenimiento en Tampico, Madero y Altamira.",
        "lede": "Casas, empresas e industria de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo San Agustín", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"Pasto desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Diseño de Jardines", "href": "/diseno-jardines-tampico",
             "img": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427,
             "texto": f"Plan Terra desde {dinero(P['diseno'])} · Propuesta visual"},
            {"titulo": "Sistema de Riego", "href": "/sistema-riego-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": f"Automatizado · Ahorra {datos.RIEGO_AHORRO} de agua"},
        ),
    },
}

PARIDAD = {
    "reemplazos": {
        "Mantenimiento de jardines en Tampico, cada mes": (
            "Mantenimiento de jardines y jardinero en Tampico con visitas programadas"),
        "Atendemos": "Sectores que atendemos",
        "Cuanto cuesta el mantenimiento de jardin en Tampico?": "¿Cuánto cuesta el mantenimiento mensual?",
        "Con que frecuencia se hace el mantenimiento?": "¿Con qué frecuencia vienen al jardín?",
        "Que incluye el servicio de mantenimiento?": "¿Qué incluye cada visita?",
        "Trabajan con empresas, hoteles y fraccionamientos?": "¿Trabajan con empresas, hoteles y parques industriales?",
        "Puedo contratar mantenimiento sin haber hecho el jardin con Viveros Terra?": (
            "¿Puedo contratar sin haber hecho el jardín con Terra?"),
    },
    "retirados": {
        "Cuidado profesional programado para tu jardín": (
            "La definición del servicio queda en la entrada de la portada y en la respuesta directa de los planes."),
        "Temporada de lluvias": "Las dos temporadas pasan a filas de la tabla “Dos temporadas, dos ritmos de mantenimiento”.",
        "Temporada seca": "Las dos temporadas pasan a filas de la tabla “Dos temporadas, dos ritmos de mantenimiento”.",
        "Desde $750/mes": (
            "El precio desde $750/mes y sus factores quedan en la etiqueta de la portada y en los planes ($750, $1,800 y "
            "por cotización), una sola sección de precio."),
        "Cotización mensual por WhatsApp": (
            "El formulario que armaba el mensaje (sendWA) se sustituye por un botón con su propio mensaje en cada plan "
            "(auditoría 02: los 4 CTA mandaban el mismo texto) y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor con cifras sin respaldo en datos.py (+200 proyectos B2B, certificación SENASICA); la "
            "entidad y el autor son de la Etapa 4. El dueño confirma esas cifras (plan 2c)."),
        "$6": "El rango “aprox. $6–$12 por m² al mes” no es dato oficial (datos.py); el precio sale de la visita.",
        "$12": "El rango “aprox. $6–$12 por m² al mes” no es dato oficial (datos.py); el precio sale de la visita.",
        "$90": "“Complementa tu proyecto” (tierra negra) sale; los materiales siguen en el menú y el pie.",
        "$1,500": "“Complementa tu proyecto” (tierra negra) sale; los materiales siguen en el menú y el pie.",
    },
}
EOF
```

- [ ] **Step 4: Registrar la página y sacarla de `tools/servicios`**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/servicios/pages.py b/tools/servicios/pages.py
index adc3589..5c902f3 100644
--- a/tools/servicios/pages.py
+++ b/tools/servicios/pages.py
@@ -17,7 +17,7 @@ GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
 DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
 VARIEDADES = ("+200", "Variedades en el vivero")
 
-# La home y /pasto-en-rollo-tampico (Etapa 2a) y /diseno-jardines-tampico (Etapa 2c) salen de tools/site/plantillas/:
+# La home y /pasto-en-rollo-tampico (Etapa 2a) y diseño y mantenimiento (Etapa 2c) salen de tools/site/plantillas/:
 # este script ya no las toca.
 PAGES = {
     "mayoreo-pasto-tampico": dict(
@@ -31,15 +31,6 @@ PAGES = {
         wa=guided("Hola, necesito pasto al mayoreo para un proyecto.", "Empresa", "Ubicación de la obra", "Metros totales", "Fecha de entrega", foto=False),
         cta="Cotizar mayoreo",
     ),
-    "mantenimiento-jardines-tampico": dict(
-        title="Mantenimiento de jardines", accent="en Tampico, cada mes",
-        price_pre="Desde", price="$750", price_unit="/mes", price_alt="· según metros y frecuencia",
-        lede="Poda, fertilización, control de plagas y revisión del riego para casas, fraccionamientos y empresas en Tampico, Madero y Altamira.",
-        facts=[("Cada 15 a 21 días", "Visitas en temporada de lluvias"), ("Cada 30 días", "Visitas en temporada seca"), ("REPSE 773725", "Contratos con empresas")],
-        img="/img/mantenimiento-jardines-poda-pasto-tampico.webp", img_pos="center 45%",
-        alt="Jardinero de Viveros Terra podando pasto en un jardín de Tampico", caption="Poda y mantenimiento en Tampico.",
-        wa=guided("Hola, quiero cotizar mantenimiento de jardín.", "Colonia", "Metros aprox. del jardín", "Casa o empresa"),
-    ),
     "sistema-riego-tampico": dict(
         title="Riego automático", accent="para jardines en Tampico",
         price_pre="De", price="$180 a $320", price_unit="/m²", price_alt="· según el tipo de sistema",
diff --git a/tools/site/generar.py b/tools/site/generar.py
index 97b6795..0388dbe 100644
--- a/tools/site/generar.py
+++ b/tools/site/generar.py
@@ -25,6 +25,8 @@ PAGINAS = (
     ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
     ("/pasto-sintetico-tampico", "pasto-sintetico-tampico/index.html", "servicio", "sintetico_tampico"),
     ("/diseno-jardines-tampico", "diseno-jardines-tampico/index.html", "servicio", "diseno_jardines"),
+    ("/mantenimiento-jardines-tampico", "mantenimiento-jardines-tampico/index.html", "servicio",
+     "mantenimiento_jardines"),
     ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
     ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
 ) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
EOF
```

- [ ] **Step 5: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Run: `python3 tools/site/paridad.py informe /mantenimiento-jardines-tampico`
Expected: `plantillas: 1 de 27` y luego `0 de 27`; `ok` en las seis categorías.
Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)`
Expected: `OK` y `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/contenido/mantenimiento_jardines.py tools/site/generar.py tools/site/tests/test_servicios_jardin.py tools/site/tests/test_generar.py tools/site/tests/test_consistencia.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/mantenimiento-jardines-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(mantenimiento): planes con su propio mensaje, frecuencias, jardinero y visita con su costo" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Riego automático sale de la plantilla y se retira lo que queda de `tools/servicios` para servicios

**Files:**
- Create: `tools/site/contenido/sistema_riego.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `tools/servicios/hero.py`, `public/sistema-riego-tampico/index.html`
- Delete: `tools/servicios/simulador.py`, `tools/servicios/tests/test_simulador.py`
- Test: `tools/site/tests/test_servicios_jardin.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_consistencia.py`, `tools/servicios/tests/test_pagos.py`

Lo que cambia: una sola sección de precio ("¿Cuánto cuesta…?" con la tabla $180–$320/m² y el ejemplo de 100 m² **calculado de `datos.py`: $18,000 a $32,000**; main decía $15,000, un error) y un solo proceso de 5 pasos (era doble; es también el `HowTo`); tres tipos de sistema, cada uno con su mensaje, y "Industrial y deportivo" se queda (campos deportivos con pasto natural, decisión del dueño); el ahorro es siempre "hasta 40%" (salen el "30% a 50% según la FAO", "hasta 60%" del goteo y "se amortiza en 18–24 meses", sin fuente en `datos.py`); "Pedir visita" sale; la garantía de materiales e instalación va sin cifra; "+200 sistemas instalados" sale (sin respaldo, ver dueño). Al terminar ninguna página usa `simulador.py` ni la línea `pago_nota` de `hero.py`: se borran. `hero.py`, `pages.py` (13 páginas de 2d–2g) y `servicios.css` se quedan.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_consistencia.py b/tools/site/tests/test_consistencia.py
index ff7b1ec..121ca0e 100644
--- a/tools/site/tests/test_consistencia.py
+++ b/tools/site/tests/test_consistencia.py
@@ -22,9 +22,8 @@ PAGINAS = {p: p.read_text(encoding="utf-8") for p in sorted(PUBLIC.rglob("*.html
 TEXTOS = {p: textos_publicos(h) for p, h in PAGINAS.items()}
 LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
 PRECIOS = datos.PRECIOS
-# Páginas que todavía mencionan la visita sin su costo. Solo puede encoger: diseño, mantenimiento y riego salen de su
-# plantilla en las Tareas 7 a 9 de la Etapa 2c y las quitan de aquí.
-VISITA_COSTO_PENDIENTES = frozenset({"sistema-riego-tampico/index.html"})
+# Páginas que todavía mencionan la visita sin su costo. Debe quedar vacía y solo puede encoger.
+VISITA_COSTO_PENDIENTES = frozenset()
 
 PROHIBIDAS = (
     ("promesa de respuesta vieja",
diff --git a/tools/site/tests/test_generar.py b/tools/site/tests/test_generar.py
index 5b0c8b7..38467cc 100644
--- a/tools/site/tests/test_generar.py
+++ b/tools/site/tests/test_generar.py
@@ -18,7 +18,8 @@ import shell  # noqa: E402
 class GenerarTest(unittest.TestCase):
     def test_paginas_registradas_tienen_contexto(self):
         esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
-                      "/mantenimiento-jardines-tampico", "/pasto-sintetico", "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
+                      "/mantenimiento-jardines-tampico", "/sistema-riego-tampico", "/pasto-sintetico",
+                      "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                      + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
         self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
         for ruta, salida, _p, _c in generar.PAGINAS:
diff --git a/tools/site/tests/test_servicios_jardin.py b/tools/site/tests/test_servicios_jardin.py
index 6950f0a..cf064aa 100644
--- a/tools/site/tests/test_servicios_jardin.py
+++ b/tools/site/tests/test_servicios_jardin.py
@@ -25,6 +25,8 @@ ESPERADO = {
                "cifras": ("$3,000", "$6,500", "desde $18,000", "en proyectos de más de $150,000")},
     "mantenimiento": {"ruta": "/mantenimiento-jardines-tampico", "extra": ('id="vt-h-incluye"',), "ld": BASE_LD,
                       "cifras": ("$750", "desde $1,800", "Por cotización")},
+    "riego": {"ruta": "/sistema-riego-tampico", "extra": ('id="vt-h-precio"',), "ld": BASE_LD | {"HowTo"},
+              "cifras": ("$180", "$320", "$18,000 a $32,000", datos.RIEGO_AHORRO)},
 }
 
 
@@ -172,5 +174,24 @@ class MantenimientoTest(unittest.TestCase):
         opiniones_textuales(self, "mantenimiento", datos.OPINIONES_MANTENIMIENTO)
 
 
+class RiegoTest(unittest.TestCase):
+    def test_un_mensaje_por_tipo_de_sistema(self):
+        html, _m, texto, grafo = pagina("riego")
+        sistemas = mensajes_de(html, r"servicio-riego:opcion-\d")
+        self.assertIn("aspersores emergentes", sistemas[0])
+        self.assertIn("goteo", sistemas[1])
+        self.assertIn("campo deportivo", sistemas[2])
+        self.assertNotIn("$15,000", texto)  # 100 m² × $180 = $18,000
+        self.assertEqual(len(next(n for n in grafo if n["@type"] == "HowTo")["step"]), 5)
+
+    def test_visita_con_costo_y_campos_deportivos(self):
+        _h, _m, texto, _g = pagina("riego")
+        self.assertIn(datos.VISITA_COSTO, texto)
+        self.assertIn("campos deportivos con pasto natural", texto)  # decisión del dueño: sí es servicio
+
+    def test_opiniones_de_main_textuales(self):
+        opiniones_textuales(self, "riego", datos.OPINIONES_RIEGO)
+
+
 if __name__ == "__main__":
     unittest.main()
EOF
```
`tools/servicios/tests/test_pagos.py` (reemplaza el archivo completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/servicios/tests/test_pagos.py <<'EOF'
"""tools/servicios ya no toca las páginas que salen de tools/site/plantillas/ (Etapas 2a y 2c)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hero  # noqa: E402
from pages import PAGES  # noqa: E402

CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico", "mantenimiento-jardines-tampico",
                 "sistema-riego-tampico")


class PaginasConPlantillaTest(unittest.TestCase):
    def test_paginas_con_plantilla_fuera_de_los_parches(self):
        for slug in CON_PLANTILLA:
            with self.subTest(slug=slug):
                self.assertNotIn(slug, PAGES)

    def test_la_portada_ya_no_lleva_linea_de_pago_ni_ancla_al_simulador_viejo(self):
        cfg = dict(PAGES["mayoreo-pasto-tampico"], img=None)
        html = hero.hero_html(cfg)
        self.assertNotIn("svc-hero__pay", html)
        self.assertNotIn("#sim-titulo", html)
        self.assertFalse(any(c.get("pago_nota") for c in PAGES.values()))


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar tests.test_consistencia 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)`
Expected: `FAILED (failures=8, errors=6)` y `FAILED (failures=2)`.

- [ ] **Step 3: El contenido**

`tools/site/contenido/sistema_riego.py` (archivo nuevo, completo):

```bash
cd ~/dev/viverosterra-e2c
cat > tools/site/contenido/sistema_riego.py <<'EOF'
"""Contenido de /sistema-riego-tampico (riego automático para jardines, industria y campos deportivos con pasto
natural). Solo datos: la plantilla es tools/site/plantillas/servicio.py, con los 3 tipos de sistema (cada uno con su
mensaje), una sola sección de precio, la comparativa aspersión / goteo / microaspersión, un solo proceso de 5 pasos
(auditoría 02: antes había dos) y simulador de mensualidades.

Precio de datos.PRECIOS["riego_m2"] ($180 a $320/m²; el ejemplo de 100 m² sale de ahí) y ahorro de datos.RIEGO_AHORRO
("hasta 40%"). Los campos deportivos con pasto natural son un servicio real (decisión del dueño): la regla de no
deportes es solo del sintético. Título, descripción, canonical, Open Graph, Twitter Card, Service y migas como estaban
publicados; FAQPage de las preguntas visibles y HowTo de los 5 pasos visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero, mensualidades

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/sistema-riego-tampico"
OBRA = "/img/obra"
RIEGO_MIN, RIEGO_MAX = P["riego_m2"]
EJEMPLO_M2 = 100
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
MENSAJE = mensajes_paginas.SERVICIOS["/sistema-riego-tampico"]
AHORRO = datos.RIEGO_AHORRO

META = {
    "title": "Sistema de Riego Automático Tampico · Viveros Terra",
    "description": (f"Instalación de sistemas de riego automático en Tampico. Ahorra {AHORRO} en agua. Aspersión, "
                    "goteo y microaspersión. Cotiza por WhatsApp."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:title", "Sistema de Riego Automático Tampico · Viveros Terra"),
        ("og:description", f"Instalación de sistemas de riego automático en Tampico. Ahorra {AHORRO} en agua. Cotiza por WhatsApp."),
        ("og:image", f"{SITE}/img/tecnico-terra-riego-industrial-tampico.avif"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", "Sistema de Riego Automático Tampico · Viveros Terra"),
        ("twitter:description", (f"Instalación de sistemas de riego automático en Tampico. Ahorra {AHORRO} en agua. "
                                 "Cotiza por WhatsApp.")),
        ("twitter:image", f"{SITE}/img/sistema-riego-automatizado-tampico.webp"),
    ),
}

SERVICIO = {
    "@type": "Service", "name": "Sistema de Riego Automático Tampico",
    "description": ("Instalación profesional de sistemas de riego automatizado para jardines residenciales, comerciales e "
                    "industriales en Tampico, Madero y Altamira, Tamaulipas. Aspersores emergentes, riego por goteo y "
                    "programadores digitales."),
    "provider": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
                 "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                             "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}},
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas", "Norte Veracruz"],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Sistema de Riego Tampico", "item": URL},
]}

SISTEMAS = (
    {"rotulo": "Sistema 1 · Pasto", "titulo": "Aspersores emergentes",
     "puntos": ("Cobertura uniforme de 2 a 15 m", "Ideal para pasto San Agustín", "Se ocultan en el suelo cuando no riegan"),
     "nota": "Para áreas de pasto: emergen al regar y cubren toda el área verde de forma pareja.",
     "mensaje": ("Hola, quiero cotizar riego con aspersores emergentes para mi pasto.\nColonia: ___\n"
                 "Metros aprox. del jardín: ___\nLes mando fotos del espacio.")},
    {"rotulo": "Sistema 2 · Plantas", "titulo": "Riego por goteo",
     "puntos": ("Lleva el agua directo a la raíz", "Ideal para plantas, arbustos, árboles y camellones",
                "Menos maleza: solo humedece donde hace falta"),
     "nota": "Para arriates y jardineras: la forma más eficiente de regar plantas ornamentales.",
     "mensaje": ("Hola, quiero cotizar riego por goteo para mis plantas.\nColonia: ___\nMetros aprox. de jardineras: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Sistema 3 · Grandes áreas", "titulo": "Industrial y deportivo",
     "puntos": ("Aspersores de largo alcance", "Controladores con varios programas",
                "De 500 m² hasta campos deportivos completos"),
     "nota": "Para parques industriales, escuelas, áreas de gobierno y campos deportivos con pasto natural.",
     "mensaje": ("Hola, quiero cotizar riego para un área grande.\nEmpresa o institución: ___\nUbicación: ___\n"
                 "m² aprox.: ___\nTipo de área (industrial, escuela, campo deportivo): ___")},
)

PREGUNTAS = (
    ("¿Cuánto cuesta instalar un sistema de riego automático en Tampico?",
     f"Entre {dinero(RIEGO_MIN)} y {dinero(RIEGO_MAX)} por m², según el tamaño del área, el tipo de sistema, el número de "
     f"zonas y la complejidad. Para cotizar, mándanos fotos y medidas aproximadas por WhatsApp al "
     f"{datos.TELEFONO_VISIBLE}; {datos.PROMESA[0].lower()}{datos.PROMESA[1:]}."),
    ("¿Cuánta agua ahorra un sistema de riego automático?",
     f"{AHORRO[0].upper()}{AHORRO[1:]} frente al riego manual. El ahorro viene de regar de madrugada (menos "
     "evaporación), evitar excesos y calibrar cada zona según el tipo de planta y la temporada."),
    ("¿Qué tipo de riego es mejor para jardines en Tampico?",
     "Para pasto San Agustín, los aspersores emergentes, por su cobertura pareja. Para plantas, arbustos y camellones, el "
     "goteo, que lleva el agua directo a la raíz y evapora menos. En jardines mixtos diseñamos sistemas combinados."),
    ("¿Cuánto tiempo tarda la instalación?",
     "Un sistema residencial de hasta 200 m² se instala en 1 a 2 días hábiles. Áreas industriales o campos deportivos "
     "pueden llevar de 3 a 7 días según la extensión. El jardín queda funcionando al terminar."),
    ("¿Funciona con la presión de agua de la red municipal?",
     "Sí. La mayoría de los sistemas residenciales funcionan con la presión normal de la red (1.5 a 4 bar). Si la presión "
     "es baja, se puede incluir una bomba pequeña en el diseño."),
    ("¿Dan garantía en la instalación?",
     "Sí. Garantizamos la instalación y los materiales: fugas o fallas por causas de la instalación se atienden sin costo "
     "adicional. También damos mantenimiento preventivo y correctivo del sistema ya instalado."),
    ("¿Instalan riego para áreas comerciales e industriales en Tampico?",
     "Sí. Tenemos experiencia en parques industriales, escuelas, áreas verdes de gobierno y campos deportivos con pasto "
     "natural en Tampico, Altamira y Madero, con aspersores de largo alcance para grandes extensiones."),
    ("¿Qué marcas de aspersores y programadores instalan?",
     "Hunter, Rain Bird y Toro, según el presupuesto y las necesidades del proyecto. Son estándares de la industria, con "
     "repuestos en México."),
)

PASOS = (
    {"titulo": "Cotización y visita técnica", "quien": "juntos", "cuando": "Antes de cotizar",
     "texto": ("Nos mandas fotos y medidas del área por WhatsApp o agendamos una visita para medir y cotizar. "
               f"{datos.VISITA_COSTO} Revisamos el área, la fuente de agua y el tipo de plantas.")},
    {"titulo": "Diseño del sistema", "quien": "nosotros", "cuando": "Al cotizar",
     "texto": ("Hacemos el plano con la distribución de aspersores o goteros, el número de zonas y el programador, con el "
               "recorrido de tuberías que menos obra requiere.")},
    {"titulo": "Instalación de tuberías", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Instalamos la red de tuberías subterráneas sin dañar raíces ni áreas del jardín, con conexiones selladas."},
    {"titulo": "Aspersores y programador", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": ("Colocamos aspersores o goteros en su posición final y conectamos el programador que riega solo en los "
               "horarios que elijas.")},
    {"titulo": "Prueba y calibración", "quien": "juntos", "cuando": "Al terminar",
     "texto": ("Probamos todo el sistema, ajustamos la cobertura y programamos horarios para el clima de Tampico. Te "
               "explicamos cómo operarlo y ajustarlo en temporada de lluvias.")},
)

FIGURAS = (
    {"src": f"{OBRA}/riego-tecnico-sistema-industrial.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Técnico de Viveros Terra revisando aspersores en el área verde de una planta industrial.",
     "lugar": "Riego en una planta industrial", "etapa": "Prueba y calibración"},
    {"src": f"{OBRA}/riego-aspersor-emergente-pasto.webp", "ancho": 640, "alto": 1423, "numero": 3,
     "alt": "Aspersor emergente regando pasto San Agustín.", "lugar": "Aspersor emergente en pasto",
     "etapa": "Tampico"},
    {"src": f"{OBRA}/riego-goteo-philodendron.webp", "ancho": 640, "alto": 1423, "numero": 4,
     "alt": "Goteo instalado al pie de un philodendron.", "lugar": "Goteo en plantas ornamentales",
     "etapa": "Tampico"},
)

SECTORES = (
    ("Residencial", "Casas y jardines familiares"),
    ("Comercios y hoteles", "Jardines de imagen y áreas exteriores"),
    ("Industria", "Parques industriales y áreas perimetrales"),
    ("Escuelas y gobierno", "Patios, parques y áreas públicas"),
    ("Campos deportivos", "Con pasto natural"),
)

CONTENIDO = {
    "tipo": "servicio-riego",
    "prefijo": "riego",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "howto": "Cómo instalar un sistema de riego automático en Tampico",
               "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Riego automático", None)),
    "portada": {
        "kicker": "Riego automático · Tampico, Madero y Altamira",
        "h1": f'Riego automático para jardines en Tampico <span class="vt-serif">que ahorra {AHORRO} de agua</span>',
        "lede": ("Aspersión, goteo o microaspersión con programador, para casas, fraccionamientos, hoteles, industria y "
                 "campos deportivos con pasto natural."),
        "etiqueta": {
            "codigo": "Riego · 01", "aviso": "Con IVA", "nombre": "Sistema de riego automático",
            "antes": "Instalado · según el sistema", "monto": f"{dinero(RIEGO_MIN)}–{dinero(RIEGO_MAX)}", "unidad": "/m²",
            "filas": ((f"Jardín de {EJEMPLO_M2} m²",
                       f"{dinero(RIEGO_MIN * EJEMPLO_M2)} a {dinero(RIEGO_MAX * EJEMPLO_M2)}"),
                      ("Instalación residencial", "1 a 2 días")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Fotos y medidas por WhatsApp para cotizar · <a href="#mensualidades">mensualidades con tarjeta de '
                    f'crédito</a> desde {DESDE_MENSUALIDADES}'),
        "foto": {"src": "/img/portadas/riego-pro-01-sm.webp",
                 "srcset": "/img/portadas/riego-pro-01-sm.webp 560w, /img/portadas/riego-pro-01.webp 960w",
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 640, "numero": 1,
                 "alt": "Aspersores de riego automático funcionando en un jardín",
                 "lugar": "Sistema de riego por aspersión", "etapa": "Instalado"},
    },
    "prueba": {
        "titulo": "Instalaciones en Tampico y la región",
        "lede": "Aspersores, goteo y microaspersión en jardines residenciales e industriales de la zona.",
        "figuras": FIGURAS,
        "nota": ("Si tu jardín es chico y tienes tiempo de regar, quizá no necesitas un sistema completo: un programador "
                 "con goteo en las jardineras puede bastar. Te lo decimos al cotizar.", "Al cotizar"),
        # La opinión de riego aprobada de la home y las dos que publicaba esta página en main (pendientes de
        # confirmación del dueño: datos.OPINIONES_RIEGO).
        "titulo_opinion": "Resultados comprobados en Tampico",
        "opiniones": datos.OPINIONES[2:3] + datos.OPINIONES_RIEGO,
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "opciones": {
        "rotulo": "Sistemas",
        "titulo": "Tipos de sistema según tu jardín",
        "lede": "Diseñamos el sistema según el tamaño del área, el tipo de plantas y tu presupuesto.",
        "items": SISTEMAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta un sistema de riego automático en Tampico?",
        "lede": (f"Entre {dinero(RIEGO_MIN)} y {dinero(RIEGO_MAX)} por m² instalado, según el tipo (aspersores, goteo o "
                 f"mixto), el número de zonas y la fuente de agua. Un jardín residencial de {EJEMPLO_M2} m² queda entre "
                 f"{dinero(RIEGO_MIN * EJEMPLO_M2)} y {dinero(RIEGO_MAX * EJEMPLO_M2)} con programador incluido, y ahorra "
                 f"{AHORRO} de agua frente al riego manual. Precios {datos.ANIO} con IVA."),
        "tabla": {"columnas": ("Concepto", "Unidad", "Precio"),
                  "filas": (("Sistema de riego automático instalado", "/m²",
                             f"{dinero(RIEGO_MIN)} a {dinero(RIEGO_MAX)}"),
                            (f"Jardín residencial de {EJEMPLO_M2} m²", "por jardín",
                             f"{dinero(RIEGO_MIN * EJEMPLO_M2)} a {dinero(RIEGO_MAX * EJEMPLO_M2)}"))},
        "caption": ('El precio cerrado sale de las fotos y medidas o de la visita. Lista completa en '
                    '<a href="/precios">viverosterra.com/precios</a>.'),
    },
    "objecion": {
        "titulo": "Aspersión, goteo o microaspersión",
        "lede": "Los tres sistemas de riego automático más usados en jardines residenciales y comerciales de Tampico.",
        "comparativa": {
            "columnas": ("Característica", "Aspersores emergentes", "Riego por goteo", "Microaspersión"),
            "filas": (
                ("Ideal para", "Pasto y áreas grandes", "Plantas y arriates", "Camellones"),
                ("Cobertura", "2 a 15 m de radio", "Punto por punto", "1 a 3 m de radio"),
                ("Presión requerida", "2 a 4 bar", "1 a 1.5 bar", "1.5 a 2 bar"),
                ("Se ve cuando no riega", "No, se ocultan", "Sí, mangueras", "Sí, estacas"),
            ),
            "caption": "Los tres sistemas, lado a lado.",
            "cierre": ("En jardines mixtos de Tampico (pasto y plantas), lo más eficiente es combinar aspersores en el pasto "
                       "y goteo en los arriates."),
        },
    },
    "proceso": {"titulo": "Cómo instalar un sistema de riego automático en 5 pasos",
                "lede": "De la cotización a tu jardín regándose solo, sin sorpresas en el precio.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía en materiales e instalación.",
        "resumen": "Fugas o fallas por causas de la instalación se atienden sin costo adicional.",
        "puntos": (
            ("Garantizamos la instalación y los materiales: fugas o fallas por causas de la instalación se atienden sin "
             "costo adicional.", True),
            ("Equipo Hunter, Rain Bird y Toro, con repuestos en México.", True),
            ("Programamos en horarios de baja evaporación y te explicamos cómo ajustarlo en temporada de lluvias.", True),
            ("Mantenimiento preventivo y correctivo del sistema ya instalado.", True),
            (f"Factura {datos.FACTURA} para persona física o moral.", True),
        ),
        "pie": '<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito desde "
                 f"{DESDE_MENSUALIDADES}."),
        "puntos": (
            "Recibes el precio del sistema, la instalación y la obra civil por separado.",
            "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
            ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos antes "
             'de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>'),
        ),
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "un sistema de riego", "monto": 18000},
    },
    "faq": {"titulo": "Todo sobre sistemas de riego en Tampico", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Listo para automatizar el riego de tu jardín?",
        "lede": ("Envíanos fotos y medidas aproximadas, y dinos si tienes pasto, plantas o ambos. Si hace falta, "
                 f"agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}"),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Riego automático en Tampico, Madero y Altamira.",
        "lede": "Casas, comercios, industria y campos deportivos de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"San Agustín desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Diseño de Jardines", "href": "/diseno-jardines-tampico",
             "img": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427,
             "texto": f"Plan Terra desde {dinero(P['diseno'])} · Propuesta visual incluida"},
            {"titulo": "Mantenimiento", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": f"Desde {dinero(P['mantenimiento_mes'])}/mes · Poda, fertilización y cuidados"},
        ),
    },
}

PARIDAD = {
    "reemplazos": {
        "Aspersores Emergentes": "Aspersores emergentes",
        "Riego por Goteo": "Riego por goteo",
        "Industrial y Deportivo": "Industrial y deportivo",
        # La segunda lista de 5 pasos repetía la primera (auditoría 02): queda una sola.
        "Instalación en 5 pasos": "Cómo instalar un sistema de riego automático en 5 pasos",
        "Cotización y diagnóstico": "Cotización y visita técnica",
        "Excavación e instalación de tuberías": "Instalación de tuberías",
        "Instalación de aspersores y programador": "Aspersores y programador",
        "Prueba, calibración y entrega": "Prueba y calibración",
        "¿Cuánto tiempo tarda la instalación de un sistema de riego?": "¿Cuánto tiempo tarda la instalación?",
        "¿El sistema funciona con la presión de agua municipal?": "¿Funciona con la presión de agua de la red municipal?",
        "¿Qué marcas de aspersores instalan?": "¿Qué marcas de aspersores y programadores instalan?",
    },
    "retirados": {
        "La forma más eficiente de mantener tu jardín verde en Tampico": (
            "La definición del sistema queda en la entrada de la portada y en la sección de tipos de sistema."),
        "+200 sistemas instalados en la región": (
            "Cifra sin respaldo en datos.py; el dueño la confirma (plan 2c). Sus garantías pasan a la sección de garantía."),
        "Cotización por WhatsApp": (
            "El formulario que armaba el mensaje (sendRW) se sustituye por un botón con su propio mensaje en cada tipo "
            "de sistema y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor con cifras sin respaldo en datos.py (+200 proyectos B2B, certificación SENASICA); la "
            "entidad y el autor son de la Etapa 4. El dueño confirma esas cifras (plan 2c)."),
        "$15,000": (f"Error aritmético: {EJEMPLO_M2} m² × ${RIEGO_MIN} = ${RIEGO_MIN * EJEMPLO_M2:,}; el rango del "
                    "ejemplo sale ahora de datos.PRECIOS['riego_m2']."),
    },
}
EOF
```

- [ ] **Step 4: Registrar la página y retirar `simulador.py` y `pago_nota`**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/servicios/hero.py b/tools/servicios/hero.py
index 59511e8..a091c03 100644
--- a/tools/servicios/hero.py
+++ b/tools/servicios/hero.py
@@ -76,10 +76,6 @@ def hero_html(cfg):
     else:
         klass += " svc-hero--nomedia"
     secondary = cfg.get("secondary", ("tel:8333268008", "Llamar 833 326 8008"))
-    pay = ""
-    if cfg.get("pago_nota"):
-        # el ancla #sim-titulo la pone tools/servicios/simulador.py (solo en las páginas con pago_nota)
-        pay = f'\n      <p class="svc-hero__pay">{e(cfg["pago_nota"])} <a href="#sim-titulo">Calcula tu plan</a></p>'
     return f"""<!-- svc-hero -->
 <section class="{klass}" aria-labelledby="svc-titulo">
   <div class="svc-hero__wrap">
@@ -87,7 +83,7 @@ def hero_html(cfg):
       <p class="svc-hero__eyebrow">{e(cfg.get("eyebrow", "Tampico · Madero · Altamira"))}</p>
       <h1 class="svc-hero__title" id="svc-titulo">{title}</h1>
       <p class="svc-hero__price">{price}</p>
-      <p class="svc-hero__lede">{cfg["lede"]}</p>{pay}
+      <p class="svc-hero__lede">{cfg["lede"]}</p>
       <div class="svc-hero__ctas">
         <a class="svc-hero__cta svc-hero__cta--wa" href="{wa_link(cfg["wa"])}" target="_blank" rel="noopener">{WA_ICON}{e(cfg.get("cta", "Cotizar por WhatsApp"))}</a>
         <a class="svc-hero__cta svc-hero__cta--ghost" href="{secondary[0]}">{e(secondary[1])}</a>
@@ -107,8 +103,6 @@ def apply(slug, cfg):
     html = path.read_text(encoding="utf-8")
     if not HERO_RE.search(html):
         raise SystemExit(f"{slug}: no encontré la portada")
-    if cfg.get("pago_nota") and 'id="sim-titulo"' not in html:
-        raise SystemExit(f"{slug}: pago_nota enlaza a #sim-titulo; corre primero tools/servicios/simulador.py")
     html = HERO_RE.sub(lambda _m: hero_html(cfg), html, count=1)
     if CSS_LINK.split("?")[0] not in html:
         html = html.replace("</head>", f"{CSS_LINK}\n</head>", 1)
diff --git a/tools/servicios/pages.py b/tools/servicios/pages.py
index 5c902f3..7ad59f6 100644
--- a/tools/servicios/pages.py
+++ b/tools/servicios/pages.py
@@ -1,8 +1,7 @@
 """Contenido de la portada de cada página de servicio o producto.
 
-Precios y datos: ver la memoria de datos oficiales (pasto $85 / $120, mayoreo $60 desde 500 m²,
-mantenimiento desde $750/mes, diseño $3,000 / $6,500 / desde $18,000, riego $180 a $320/m²,
-palmas desde $250 (areca y coco plumoso) y real desde $500 en tamaño chico, garantía de plantas 30 días con riego y cuidado indicados).
+Precios y datos: ver la memoria de datos oficiales (pasto $85 / $120, mayoreo $60 desde 500 m², palmas desde $250
+(areca y coco plumoso) y real desde $500 en tamaño chico, garantía de plantas 30 días con riego y cuidado indicados).
 """
 
 
@@ -17,8 +16,8 @@ GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
 DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
 VARIEDADES = ("+200", "Variedades en el vivero")
 
-# La home y /pasto-en-rollo-tampico (Etapa 2a) y diseño y mantenimiento (Etapa 2c) salen de tools/site/plantillas/:
-# este script ya no las toca.
+# La home y /pasto-en-rollo-tampico (Etapa 2a), y diseño, mantenimiento y riego (Etapa 2c) salen de
+# tools/site/plantillas/: este script ya no las toca. Quedan las páginas de las Etapas 2d a 2g.
 PAGES = {
     "mayoreo-pasto-tampico": dict(
         eyebrow="Constructoras · Fraccionamientos · Industria",
@@ -31,17 +30,6 @@ PAGES = {
         wa=guided("Hola, necesito pasto al mayoreo para un proyecto.", "Empresa", "Ubicación de la obra", "Metros totales", "Fecha de entrega", foto=False),
         cta="Cotizar mayoreo",
     ),
-    "sistema-riego-tampico": dict(
-        title="Riego automático", accent="para jardines en Tampico",
-        price_pre="De", price="$180 a $320", price_unit="/m²", price_alt="· según el tipo de sistema",
-        lede="Aspersión, goteo o microaspersión con programador, para casas, fraccionamientos, hoteles e industria en Tampico, Madero y Altamira.",
-        facts=[("Hasta 40%", "Menos agua que el riego manual"), ("Por WhatsApp", "Fotos y medidas para cotizar"), ("Aspersión o goteo", "Según tus plantas y tu pasto")],
-        img="/img/riego-pro-01.webp",
-        alt="Aspersores de riego automático funcionando en un jardín", caption="Sistema de riego por aspersión instalado.",
-        wa=guided("Hola, quiero cotizar riego automático.", "Colonia", "Metros aprox. del jardín", "Tengo pasto, plantas o ambos"),
-        secondary=("tel:8333268008", "Pedir visita"),
-        pago_nota="Paga en mensualidades con tarjeta de crédito en cotizaciones desde $2,000.",
-    ),
     "vivero-tampico": dict(
         title="Vivero en Tampico", accent="y Ciudad Madero, desde 2007",
         price_pre="Palmas desde", price="$250", price_unit="", price_alt="· pasto $85/m² · plantas por tamaño",
diff --git a/tools/site/generar.py b/tools/site/generar.py
index 0388dbe..f33f69e 100644
--- a/tools/site/generar.py
+++ b/tools/site/generar.py
@@ -27,6 +27,7 @@ PAGINAS = (
     ("/diseno-jardines-tampico", "diseno-jardines-tampico/index.html", "servicio", "diseno_jardines"),
     ("/mantenimiento-jardines-tampico", "mantenimiento-jardines-tampico/index.html", "servicio",
      "mantenimiento_jardines"),
+    ("/sistema-riego-tampico", "sistema-riego-tampico/index.html", "servicio", "sistema_riego"),
     ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
     ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
 ) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
EOF
```
```bash
cd ~/dev/viverosterra-e2c
git rm tools/servicios/simulador.py tools/servicios/tests/test_simulador.py
grep -rn "planes_diseno\|simulador.py\|pago_nota\|sim-titulo" tools | grep -v "/tests/" || echo "sin restos"
```

Expected: `sin restos`.

- [ ] **Step 5: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
```

Run: `python3 tools/site/paridad.py informe /sistema-riego-tampico`
Expected: `plantillas: 1 de 28` y luego `0 de 28`; `ok` en las seis categorías.
Run: `(cd tools/site && python3 -m unittest tests.test_servicios_jardin tests.test_generar tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia 2>&1 | tail -1); (cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -3)`
Expected: `OK`; `Ran 2 tests` y `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/contenido/sistema_riego.py tools/site/generar.py tools/site/tests/test_servicios_jardin.py tools/site/tests/test_generar.py tools/site/tests/test_consistencia.py tools/servicios/pages.py tools/servicios/hero.py tools/servicios/tests/test_pagos.py public/sistema-riego-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(riego): una sola sección de precio y de proceso, un mensaje por sistema; fuera simulador.py y pago_nota" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: `corregir_datos.py` no toca páginas que salen de su plantilla

`tools/site/corregir_datos.py` (corrector de la Etapa 1b, se corre a mano) tiene reemplazos para el HTML viejo de la home y de pasto en rollo (desde 2a) y ahora de diseño y riego: su texto ya no existe, así que `main()` se detendría con "no encontré el texto". Se filtran con `generar.PAGINAS`; sus filas se borran al cerrar la Etapa 2 (2i), junto con `migrar_shell.py`.

**Files:**
- Modify: `tools/site/corregir_datos.py`
- Test: `tools/site/tests/test_corregir_datos.py`

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_corregir_datos.py b/tools/site/tests/test_corregir_datos.py
index 536fea2..713eb98 100644
--- a/tools/site/tests/test_corregir_datos.py
+++ b/tools/site/tests/test_corregir_datos.py
@@ -81,6 +81,20 @@ class HerramientasTest(unittest.TestCase):
                 una = c.reemplazar(f"a {viejo} b", viejo, nuevo, rel)
                 self.assertEqual(c.reemplazar(una, viejo, nuevo, rel), una)
 
+    def test_no_toca_paginas_con_plantilla(self):
+        """Etapas 2a y 2c: el HTML de esas páginas sale de su contenido; sus reemplazos viejos ya no aplican."""
+        fuera = c.con_plantilla()
+        for rel in ("public/index.html", "public/pasto-en-rollo-tampico/index.html",
+                    "public/diseno-jardines-tampico/index.html", "public/sistema-riego-tampico/index.html"):
+            self.assertIn(rel, fuera)
+        for rel, *_resto in c.vigentes(c.POR_ARCHIVO) + c.vigentes(c.ELEMENTOS):
+            self.assertNotIn(rel, fuera)
+
+    def test_cada_reemplazo_vigente_encuentra_su_texto_o_su_correccion(self):
+        for rel, viejo, nuevo in c.vigentes(c.POR_ARCHIVO):
+            with self.subTest(archivo=rel, viejo=viejo[:60]):
+                c.reemplazar((c.RAIZ / rel).read_text(encoding="utf-8"), viejo, nuevo, rel)
+
 
 if __name__ == "__main__":
     unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_corregir_datos 2>&1 | tail -1`
Expected: `FAILED (errors=2)` (`AttributeError: … 'con_plantilla'`).

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/corregir_datos.py b/tools/site/corregir_datos.py
index dda13d4..7d7b441 100644
--- a/tools/site/corregir_datos.py
+++ b/tools/site/corregir_datos.py
@@ -349,14 +349,27 @@ def _escribir_si_cambia(path, nuevo, cambiados):
         cambiados.add(path)
 
 
+def con_plantilla():
+    """Rutas ("public/…") de las páginas que salen de tools/site/generar.py: su texto vive en tools/site/contenido/ y
+    ya trae las correcciones, así que los reemplazos por archivo de su HTML viejo no aplican (Etapas 2a y 2c)."""
+    import generar  # noqa: E402  (solo aquí: generar importa las plantillas)
+    return {f"public/{salida}" for _r, salida, _p, _c in generar.PAGINAS}
+
+
+def vigentes(entradas):
+    """Las entradas (rel, …) de POR_ARCHIVO o ELEMENTOS cuyo archivo sigue escrito a mano."""
+    fuera = con_plantilla()
+    return tuple(e for e in entradas if e[0] not in fuera)
+
+
 def main():
     cambiados = set()
     for path in archivos_globales():
         _escribir_si_cambia(path, corregir_texto(path.read_text(encoding="utf-8")), cambiados)
-    for rel, viejo, nuevo in POR_ARCHIVO:
+    for rel, viejo, nuevo in vigentes(POR_ARCHIVO):
         path = RAIZ / rel
         _escribir_si_cambia(path, reemplazar(path.read_text(encoding="utf-8"), viejo, nuevo, rel), cambiados)
-    for rel, patron in ELEMENTOS:
+    for rel, patron in vigentes(ELEMENTOS):
         path = RAIZ / rel
         _escribir_si_cambia(path, quitar_elementos(path.read_text(encoding="utf-8"), patron), cambiados)
     print(f"{len(cambiados)} archivos corregidos")
EOF
```

- [ ] **Step 4: Pruebas**

Run: `cd tools/site && python3 -m unittest tests.test_corregir_datos 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/corregir_datos.py tools/site/tests/test_corregir_datos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(corregir_datos): no reemplaza el HTML viejo de las páginas que salen de su plantilla" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Pruebas en navegador de los servicios

**Files:**
- Test: `tools/site/tests/test_plantillas_navegador.py`

Las tres páginas entran a axe de página completa (375 y 1440), primer pantallazo móvil (precio y CTA a 375 × 812), sin desbordar a 320/375/768/1024/1440 y CLS < 0.1; se agregan el clic de un plan por página (mensaje con el plan y `generate_lead` con `cta_id` `<tipo>:opcion-<n>` y `service` `jardin`) y el simulador de diseño y riego.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2c
git apply <<'EOF'
diff --git a/tools/site/tests/test_plantillas_navegador.py b/tools/site/tests/test_plantillas_navegador.py
index f25db19..a6d4370 100644
--- a/tools/site/tests/test_plantillas_navegador.py
+++ b/tools/site/tests/test_plantillas_navegador.py
@@ -17,6 +17,9 @@ except ImportError:
 
 AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
 PAGINAS = ("/", "/pasto-en-rollo-tampico/")
+# Etapa 2c: servicios de jardín con la plantilla de servicio (sin Medidor).
+SERVICIOS = ("/diseno-jardines-tampico/", "/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/")
+CON_PLANTILLA = PAGINAS + SERVICIOS
 AXE_PAGINA = """async () => {
   const r = await axe.run(document, { resultTypes: ['violations'] });
   return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
@@ -56,7 +59,7 @@ class PlantillasNavegadorTest(unittest.TestCase):
         script = AXE.read_text(encoding="utf-8")
         for ancho in (375, 1440):
             page = self.pagina(ancho)
-            for ruta in PAGINAS:
+            for ruta in CON_PLANTILLA:
                 page.goto(self.base + ruta, wait_until="load")
                 page.add_script_tag(content=script)
                 with self.subTest(ruta=ruta, ancho=ancho):
@@ -64,7 +67,7 @@ class PlantillasNavegadorTest(unittest.TestCase):
 
     def test_precio_y_cta_en_el_primer_pantallazo_movil(self):
         page = self.pagina(375, 812)
-        for ruta in PAGINAS:
+        for ruta in CON_PLANTILLA:
             page.goto(self.base + ruta, wait_until="load")
             precio = page.locator(".vt-portada .vt-etiqueta__precio").bounding_box()
             cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
@@ -73,9 +76,9 @@ class PlantillasNavegadorTest(unittest.TestCase):
                 self.assertLessEqual(cta["y"] + cta["height"], 812)
 
     def test_sin_desbordar_en_cuatro_anchos(self):
-        for ancho in (320, 375, 768, 1440):
+        for ancho in (320, 375, 768, 1024, 1440):
             page = self.pagina(ancho)
-            for ruta in PAGINAS:
+            for ruta in CON_PLANTILLA:
                 page.goto(self.base + ruta, wait_until="load")
                 sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                 with self.subTest(ruta=ruta, ancho=ancho):
@@ -165,9 +168,39 @@ class PlantillasNavegadorTest(unittest.TestCase):
         self.assertEqual(page.locator("[data-sim-list] .sim-plan").count(), 5)
         self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))
 
+    def test_cada_plan_manda_su_mensaje_y_su_generate_lead(self):
+        """Etapa 2c (auditoría 02): el plan elegido viaja al chat y a GA4 con su propio cta_id."""
+        casos = (("/diseno-jardines-tampico/", "servicio-diseno", 2, "Plan Terra Completo ($6,500)"),
+                 ("/mantenimiento-jardines-tampico/", "servicio-mantenimiento", 2, "Residencial premium"),
+                 ("/sistema-riego-tampico/", "servicio-riego", 3, "campo deportivo"))
+        for ruta, tipo, n, frase in casos:
+            page = self.pagina()
+            page.add_init_script("window.open = () => null;")
+            page.goto(self.base + ruta, wait_until="load")
+            boton = page.locator(f'[data-cta="{tipo}:opcion-{n}"]')
+            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
+            boton.click()
+            eventos = page.evaluate(
+                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
+            with self.subTest(ruta=ruta):
+                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": f"{tipo}:opcion-{n}",
+                                                          "service": "jardin"}], eventos)
+                texto = unquote(boton.get_attribute("href").split("text=", 1)[1])
+                self.assertIn(frase, texto)
+                self.assertTrue(texto.endswith(datos.FIRMA))
+
+    def test_simulador_de_diseno_y_riego_funciona(self):
+        for ruta, monto in (("/diseno-jardines-tampico/", "6500"), ("/sistema-riego-tampico/", "18000")):
+            page = self.pagina()
+            page.goto(self.base + ruta, wait_until="load")
+            with self.subTest(ruta=ruta):
+                self.assertEqual(page.input_value("[data-sim-monto]"), monto)
+                self.assertGreaterEqual(page.locator("[data-sim-list] .sim-plan").count(), 4)
+                self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))
+
     def test_cls_bajo_0_1_en_movil(self):
         page = self.pagina(375, 812)
-        for ruta in PAGINAS:
+        for ruta in CON_PLANTILLA:
             page.goto(self.base + ruta, wait_until="load")
             with self.subTest(ruta=ruta):
                 self.assertLess(page.evaluate(CLS), 0.1)
EOF
```

- [ ] **Step 2: Correrlas**

Run: `cd tools/site && python3 -m unittest tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `Ran 12 tests` y `OK` (con la rejilla de la Tarea 4; sin ella, 768 px desborda 27 px en las tres páginas).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2c
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): axe, primer pantallazo, desborde a 1024, CLS, planes con generate_lead y simulador en los servicios de jardín" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Verificación final, puertas de revisión, merge y producción

**Files:** ninguno nuevo (correcciones de los revisores, cada una con su prueba y su commit).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2c
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 28 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 361 tests` y `OK`; `OK`; `Ran 2 tests` y `OK`; `ℹ pass 41` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas y consistencia a la vista**

```bash
cd ~/dev/viverosterra-e2c
for r in /diseno-jardines-tampico /mantenimiento-jardines-tampico /sistema-riego-tampico; do python3 tools/site/paridad.py informe $r; done
(cd tools/site && python3 -m unittest tests.test_reglas tests.test_consistencia tests.test_paridad tests.test_contenido tests.test_servicios_jardin 2>&1 | tail -1)
grep -oiE "oasis|pasto ?plus|\bMSI\b|sin intereses|p[aá]del|canchas?|lote semanal|pagas cuando|liquida|visita (sin costo|gratis)|gratuit" public/{diseno-jardines-tampico,mantenimiento-jardines-tampico,sistema-riego-tampico}/index.html | sort | uniq -c
git diff main...feat/etapa-2c -- public/{diseno-jardines-tampico,mantenimiento-jardines-tampico,sistema-riego-tampico}/index.html | grep -E '^[-+].*(<title>|name="description"|rel="canonical"|property="og:|name="twitter:)'
curl -s https://www.viverosterra.com/robots.txt | grep -iA2 adsbot
```

Expected: `ok` en las seis categorías de las tres páginas; `OK`; el `grep` de palabras vacío; el `diff` de meta vacío; `robots.txt` sin `Disallow` para AdsBot.

- [ ] **Step 3: Consola limpia en las 108 páginas y axe**

Run: `cd ~/dev/viverosterra-e2c/tools/site && python3 -m unittest tests.test_navegador tests.test_tienda_navegador tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `OK` (incluye consola sin errores en las 108 páginas y axe del shell).

- [ ] **Step 4: Lighthouse móvil en las tres páginas**

```bash
cd ~/dev/viverosterra-e2c
(cd public && python3 -m http.server 8766 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in diseno-jardines-tampico mantenimiento-jardines-tampico sistema-riego-tampico; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8766/$r/" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2c-lh-$r.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2c-lh-$r.json"
done
pkill -f "http.server 8766"
```

Expected por página: Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s. CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. Si Performance queda abajo por GA4, anota valor y causa (`largest-contentful-paint-element`) en el PR (GA4 diferido es Etapa 5).

- [ ] **Step 5: Capturas a 320, 375, 768, 1024 y 1440**

```bash
cd ~/dev/viverosterra-e2c/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in ('diseno-jardines-tampico', 'mantenimiento-jardines-tampico', 'sistema-riego-tampico'):
        for w in (320, 375, 768, 1024, 1440):
            p = b.new_page(viewport={'width': w, 'height': 900})
            p.goto(f'{base}/{r}/', wait_until='load')
            p.screenshot(path=f'/tmp/vt-e2c-{r}-{w}.png', full_page=True)
            p.close()
    b.close()
srv.shutdown()
print('15 capturas')
PY
```

Expected: `15 capturas`. Revisa a mano: una etiqueta amarilla por primer pantallazo móvil, precio y CTA visibles a 375; planes en 1 columna a 320/375, 2 a 768 y 3 desde 1024, botón entero; la línea de mensualidades bajo cada precio de diseño; tablas legibles a 320 (tarjetas); pies `FIG.`; NOSOTROS / TÚ / JUNTOS; nada que desborde.

- [ ] **Step 6: Abrir el PR**

```bash
cd ~/dev/viverosterra-e2c
git push -u origin feat/etapa-2c
gh pr create --base main --head feat/etapa-2c --title "Etapa 2c · Plantillas: servicios (diseño, mantenimiento, riego)" --body "$(cat <<'BODY'
## Qué cambia
- Diseño, mantenimiento y riego salen de la plantilla de servicio con su contenido en `tools/site/contenido/`; precios, frecuencias, ahorro y opiniones desde `datos.py`.
- Un mensaje de WhatsApp por plan (auditoría 02) y, en diseño, la línea de mensualidades con la fórmula oficial; una sola sección de precio y un solo proceso en riego.
- Decisiones del dueño del 2026-11-07 en todo el sitio: la visita para cotizar cuesta según la ubicación; fuera “el resto se liquida”.
- `tools/servicios`: fuera `planes_diseno.py`, `simulador.py` y `pago_nota`; `hero.py`, `pages.py` y `servicios.css` siguen para 2d–2g.
- Título, descripción, canonical, Open Graph, Twitter y tipos de JSON-LD intactos; FAQPage y HowTo de lo visible.

## Verificación
- [ ] Build reproducible y 4 suites en verde
- [ ] Paridad en las tres páginas
- [ ] Lighthouse móvil (Perf, A11y, CLS, LCP de las tres)
- [ ] Capturas 320/375/768/1024/1440
- [ ] Puertas: diseño, SEO/AEO, CRO, cumplimiento
- [ ] Vista previa aprobada por el dueño y opiniones confirmadas

🤖 Generated with [Claude Code](https://claude.com/claude-code)
BODY
)"
```

- [ ] **Step 7: Puertas de revisión en paralelo (spec §11)**

Lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2c --stat`, los módulos de contenido, `componentes.py`, `plantillas/servicio.py`, el bloque de `terra.css`, la vista previa de Vercel, `/tmp/vt-e2c-*.png`, los JSON de Lighthouse, el `paridad.py informe` y el spec (§3.3, §3.4, §4, §5, §6.6, §7, §8.3, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta, cuadro de datos, FIG., NOSOTROS/TÚ/JUNTOS), jerarquía de los 3 planes (el recomendado se distingue sin depender del color), la línea de mensualidades legible, tablas a 320, foco y objetivos de 44 px, capturas.
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta (Step 2), JSON-LD válido en Rich Results Test, un H1 con lugar, "jardinero" en mantenimiento, respuesta directa de precio en las tres, `HowTo` = proceso visible en riego, enlaces internos y zonas, imágenes con `width`/`height` y alt, LCP precargado.
3. **CRO** (`general-purpose` con `page-cro`): un mensaje distinto por plan y que llegue firmado; primer pantallazo móvil; objeciones (descuento del diseño, frecuencia, permanencia, costo de la visita según ubicación); que quitar los formularios no deje a nadie sin camino.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): reglas del dueño, datos solo de `datos.py`, opiniones textuales de main, `tools/servicios` sin restos, consola limpia, sin `.DS_Store`.

Corrige en la rama todo crítico o alto (prueba, commit, Step 1 otra vez) y vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan en el PR.

- [ ] **Step 8: Aprobación del dueño**

Comparte la vista previa y las capturas, y pide en el mismo mensaje lo de "Lo que aporta el dueño". Sin su "sí" explícito no hay merge. Si alguna opinión no es real o no tiene permiso: bórrala de `datos.OPINIONES_*`, quita su caso de `test_servicios_jardin.py` y, si el bloque queda vacío, pasa su encabezado a `PARIDAD["retirados"]` con el motivo.

- [ ] **Step 9: Merge, push y despliegue (lo hace el controlador)**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2c -m "feat: Etapa 2c, servicios de diseño, mantenimiento y riego con el sistema de componentes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 28 …`, `shell: 0 de 108 …`, `0`; Vercel despliega `main`.

- [ ] **Step 10: Verificación en vivo**

```bash
W=https://www.viverosterra.com
for r in diseno-jardines-tampico mantenimiento-jardines-tampico sistema-riego-tampico; do
  curl -s $W/$r | grep -o "<h1[^>]*>.*</h1>" | head -1
  curl -s $W/$r | grep -cE "fonts.googleapis|tailwind.css|design-system.css|servicios.css"
  curl -s $W/$r | grep -oE 'data-cta="servicio-[a-z]+:opcion-[123]"' | sort -u | wc -l
done
curl -s $W/sistema-riego-tampico | grep -c "depende de la ubicación"
curl -s $W/pasto-en-rollo-tampico | grep -ci "se liquida"
```

Expected por página: su H1, `0`, `3`; luego `2` o más y `0`. En Chrome (escritorio y iPhone): consola limpia, botones de plan que abren WhatsApp con el plan, simulador de diseño y riego, menú y barra. En GA4 DebugView: `generate_lead` con `cta_id` `servicio-diseno:opcion-2`, `servicio-mantenimiento:opcion-1` y `servicio-riego:opcion-3`.

- [ ] **Step 11: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 12: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2c && git branch -d feat/etapa-2c
```

---

## Correcciones a la hoja de ruta

- `tools/servicios/hero.py`, `pages.py` y `servicios.css` **no** se retiran en 2c: los usan mayoreo, palmas para proyectos, plantas, materiales y vivero. 2c retira solo `planes_diseno.py`, `simulador.py` y `pago_nota`. `servicios.css` se borra en 2i.
- La prueba del `window.open` firmado (`test_window_open_de_whatsapp_sale_firmado`) pasa a `/piedra-bola-rio-tampico` (2f la vuelve a mover).
- El "paso 5 de pasto en rollo con la frase de pago" ya no existe en `main` (el paso 5 es "Primera poda"); la frase que sí existía era "El resto se liquida según lo acordado en tu cotización" en el pago de pasto en rollo y sintético en Tampico, y sale en la Tarea 2.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Opiniones con nombre de main que no sean reales (6: Daniela M., Ing. Roberto S., Carolina R., Ing. Gerardo M., Roberto C., María V.) | Se conservan textuales, marcadas "PENDIENTE DEL DUEÑO" en `datos.py`; el merge espera su confirmación (Step 8 dice cómo retirarlas). |
| Las fotos de diseño parecen propuestas o renders | Pie "Proyecto · referencia"; se sustituyen con la sesión de fotos real cambiando solo `src`. |
| `$1,800/mes` del plan premium no estaba en `datos.py` | Estaba publicado en main; queda en `datos.PRECIOS["mantenimiento_premium_mes"]` y en la lista del dueño. |
| Marcas de equipo de riego (Hunter, Rain Bird, Toro) | La regla del dueño es para proveedores de pasto sintético; se conservan como en main y el revisor de cumplimiento lo confirma. |
| Quitar el bloque de autor y "+200 sistemas/proyectos", "SENASICA" | Cifras sin respaldo; vuelven si el dueño las confirma (Etapa 4 pone autor y entidad). |
| Formularios que armaban el mensaje (`sendWA`, `sendRW`) | Un botón por plan con el mensaje propio y el CTA final; la medición sigue con `data-cta` (prueba de `generate_lead`). |
| La rejilla nueva de `.vt-modos` toca sintético en Tampico | Con 2 opciones da las mismas columnas en todos los anchos; `test_plantillas_navegador` y las capturas lo vigilan. |
| Presupuesto de `terra.css` | 8.4 KB gzip tras 2c; quedan 1.8 KB para 2d–2i. |

## Lo que aporta el dueño

1. Confirmar que las 6 opiniones con nombre de estas páginas son reales y tienen permiso (o cuáles retirar).
2. Confirmar el plan Residencial premium "desde $1,800/mes" y las cifras retiradas que quiera recuperar ("+200 sistemas de riego instalados", "+200 proyectos B2B", certificación SENASICA, "se amortiza en 18–24 meses").
3. Confirmar si las fotos de diseño son obras terminadas (para quitar "referencia") y fecha de la sesión de fotos real.
4. Precios "desde" que siguen pendientes y por eso van "según cotización": palmas sin precio, mármol, piedra bola y tezontle por camión (los usan 2d–2f).
