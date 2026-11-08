# Etapa 2d · Plantillas: empresas (mayoreo de pasto y palmas para proyectos) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cuarto sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2d; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §3.4, §4, §5, §7.3, §10): `/mayoreo-pasto-tampico` y `/palmas-mayoreo-proyectos` dejan de ser HTML a mano parchado por `tools/servicios` y salen de una plantilla nueva `b2b` con su contenido en `tools/site/contenido/`. Secuencia B2B del spec: H1 por segmento con precio por volumen y mínimo → CTA con la plantilla de compras y la promesa única → clientes con nombre y logo y REPSE verificable → tabla de escalas, capacidad y tiempos con su cotizador → documentación (CFDI 4.0, REPSE, anticipo y avances de obra, entregas por etapas) → paquetes por obra (máx. 3, cada uno con su mensaje) → proceso → garantía con condiciones → preguntas de compras → cobertura → otras páginas para empresas → CTA. Dos cotizadores nuevos que arman el WhatsApp: **pasto por volumen** (m² totales → mayoreo desde $60/m² con 500 m² o más; con menos, $85/m² solo pasto y el aviso, la misma regla del Medidor) y **armador de palmas** (especie, altura y cantidad por renglón → un solo mensaje). Precios de palmas del dueño (areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; el resto, según cotización). `/empresas` **se queda en la Etapa 3** (spec §3.5 y §10): 2d deja las páginas listas para enlazarse desde ahí. Se publica en el lote 3 (con 2c ya en producción).

**Architecture:** Igual que 2a–2c: `tools/site/contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD`; la plantilla nueva `tools/site/plantillas/b2b.py` arma la página con `tools/site/componentes.py`; `generar.py` registra la fila y `build.py` la escribe con el shell solo si cambia. Lo nuevo: (1) `datos.py` gana `ANTICIPO_PROYECTOS` (la frase del dueño, sin porcentaje), `REPSE_PADRON` (padrón público de la STPS, verificado con `curl`: responde 200), `PALMAS_PROYECTO` (12 especies con precio "desde" o `None`) y `PRECIOS["palma_real"]`; `mensajes_paginas.EMPRESAS` lleva la plantilla de compras de cada página al menú, la barra móvil y el pie. (2) `componentes.cotizador_volumen()` reutiliza `calculo_medidor(m2, 1, "mayoreo")` en Python y, en el navegador, `VTMedidor.calcular` de `vt-medidor.js` (la regla "con menos de 500 m² calcula a $85 y lo avisa" no se reimplementa); `componentes.armador_palmas()` no muestra total (depende de la altura). Un archivo JS nuevo, `public/js/vt-b2b.js` (vanilla, funciones puras exportadas para `node --test`), actualiza la etiqueta y el `href` de enlaces `wa.me` con `data-cta`: terra.js los mide (`generate_lead`) y los firma sin `window.open`. Paridad Python–JS en `public/js/tests/casos-b2b.json`. (3) `contenido/b2b_comun.py` guarda lo que comparten las dos páginas (documentación, dos preguntas de compras, sectores, cobertura y `PAGINAS`, el índice B2B que reutilizará `/empresas` en la Etapa 3). (4) `paridad.py` acepta un cambio de meta solo si el contenido declara el valor nuevo exacto y el motivo (`PARIDAD["meta"]`): la descripción de palmas decía "12 especies desde $850" y la de mayoreo "Factura CFDI, factura CFDI". **CSS:** 14 reglas (`.vt-b2b*`, `.vt-control select` y `.vt-b2b [hidden]`) (45.4 KB sin comprimir, 8.74 KB gzip; presupuesto 48 KB / 10 KB). **Retiro de `tools/servicios` para estas páginas:** salen de `pages.py`; `hero.py`, `pages.py` y `servicios.css` se quedan para plantas, materiales y vivero (2e–2g). **SEO:** título, robots, canonical, Open Graph, Twitter Card, `Service`, migas y tipos de JSON-LD como estaban (el `@id` `#localbusiness` de palmas se va con el grafo único de la Etapa 4); `FAQPage` sale de lo visible; `ItemList` y `AggregateOffer` de palmas con los precios nuevos y sin `InStock`; respuesta directa citable en la entrada de cada portada y encabezados en pregunta (spec §7.3).

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en las pruebas de navegador; CSS plano; JavaScript vanilla (un archivo nuevo, `vt-b2b.js`; `vt-medidor.js` y `terra.js` sin cambios); `node --test` sin `package.json`; Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2d` (rama `feat/etapa-2d`, Tarea 0). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- Cada parche y cada archivo de este plan se probó sobre `main` en `00cad4d`, en este orden, en una copia de trabajo (las salidas "Expected" son las de esa corrida): los parches aplican con `git apply` tal cual y los archivos nuevos se escriben completos con `cat > … <<'EOF'`. Si `git apply` falla, `main` cambió: detente y reporta (no edites a mano para "hacerlo entrar").
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`).
- Cuando una tarea cambia `terra.css`, el build cambia el hash, reescribe el `<head>` de las páginas, agrega `public/css/terra.<hash>.css` y borra la generación más vieja (`activos.json` guarda dos): es esperado y se versiona todo (`git add public tools/site/activos.json`), revisando antes `git status --short | grep -v '\.html$'`.
- Reglas del dueño (las prueban `test_reglas.py`, `test_consistencia.py` y `test_b2b.py`): nunca "Oasis"; nunca marcas de proveedor de pasto sintético (PastoPlus); nunca el nombre del proveedor de la terminal en `public/`; nunca "MSI", "meses sin intereses" ni "sin intereses"; sin SENASICA, SADER ni certificados fitosanitarios; nunca "se paga solo" ni amortización; nunca "pagas cuando ves…"; nunca "liquidas el saldo" ni "el resto se liquida" (sí "el resto se acuerda contra avances de obra", frase del dueño en `datos.ANTICIPO_PROYECTOS`); nunca "visita sin costo"; sin crédito ni pago diferido para clientes, empresas o proyectos; sin fechas de disponibilidad ni de corte; "flamboyán"; "anticipo" sin porcentaje; sin testimonios, nombres ni proyectos inventados (la única opinión de estas páginas es la de la Arq. Patricia L., real y con permiso, de `datos.OPINIONES_PASTO_EN_ROLLO`); precios, escalas, capacidades y plazos que el dueño no dio **no se publican**: van "según cotización" o "por escrito en tu cotización".
- Dos textos de CTA y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008". El "Cotizar mayoreo" de main desaparece. Todo WhatsApp lleva la plantilla de compras (`Empresa: ___`, `Obra y ubicación: ___`…) y la firma.

## `/empresas`: se queda en la Etapa 3

El spec la pone en la Etapa 3 (§3.5 "Páginas nuevas" y §10 "Etapa 3 · Arquitectura y contenido": `/nosotros`, `/empresas`, `/zonas`…) y el menú ya tiene "Empresas" como panel sin enlace propio (`partials.MENU`, `href: None`). 2d no la crea. Deja las dos páginas listas para colgarse de ella:

- `contenido/b2b_comun.PAGINAS` es el índice B2B (mayoreo, palmas, mantenimiento de áreas verdes y riego para grandes áreas, con su "desde" de `datos.py`): hoy alimenta "Otras soluciones para empresas" de cada página; en la Etapa 3 será el cuerpo de `/empresas`.
- Las migas visibles y el `BreadcrumbList` de cada contenido llevan un comentario con el cambio exacto para la Etapa 3 ("Inicio › Empresas › …").
- `test_b2b.ComunTest.test_empresas_todavia_sin_enlace` falla si alguna página enlaza `/empresas` antes de que exista (la Etapa 3 lo invierte).

## Cobertura del spec y qué queda fuera

| Pide el spec / la hoja de ruta / las auditorías | Dónde |
|---|---|
| §3.3 secuencia B2B: H1 por segmento + precio por volumen con mínimo → CTA → clientes con nombre y REPSE verificable → escalas, capacidad y tiempos → documentación (CFDI, REPSE) → paquetes por obra → FAQ de compras → CTA | Tarea 6 (`plantillas/b2b.py`), `test_b2b.ComunTest.test_orden_de_secciones_del_spec` |
| §3.3 "ficha descargable solo si existe el PDF real" | No hay PDF: no se publica (pregunta al dueño 9) |
| §3.4 recorrido B2B: clientes con nombre + REPSE → escalas → WhatsApp con plantilla de compras | Tareas 2, 4, 6 y 7 (`mensajes_paginas.EMPRESAS`, cotizadores, paquetes) |
| §4.3 "mayoreo con menos de 500 m² calcula a $85 y lo avisa" | Tarea 4 (`cotizador_volumen` usa `calculo_medidor` / `VTMedidor.calcular`), `test_b2b.MayoreoTest.test_con_menos_de_500_m2_nunca_a_60`, `vt-b2b.test.js` |
| §5.2 mayoreo "200 m²" → 500 m² | Ya en `main`; `test_consistencia.test_mayoreo_desde_500_m2` sigue en verde |
| §7.3 respuesta directa y encabezados en pregunta en mayoreo | Entrada de cada portada; "¿Cuánto cuesta el pasto al mayoreo?", "¿Cuánto cuestan las palmas para proyecto?" |
| Hoja de ruta 2d: clientes con `logos()` de 2a, REPSE verificable, "Para proyectos solicitamos un anticipo…" dos veces | Tareas 2, 4 y 6 (`componentes.repse()`, `datos.ANTICIPO_PROYECTOS`, `test_consistencia`) |
| Hoja de ruta 2d: escalas y capacidades que no estén en `datos.py` no se publican | Tabla de escalas con "Por escrito en tu cotización"; preguntas al dueño 3 y 4 |
| Auditoría 02: mayoreo solo listaba categorías; mínimo único; promesa única; pasto en rollo manda el CTA de mayoreo a la página B2B | Logos con nombre (Tarea 6); 500 m² en todo; `datos.PROMESA_COMPLETA` del shell; el enlace de pasto en rollo ya existe en `main` |
| Auditoría 03: mayoreo y palmas por intención B2B; imágenes con `width`/`height` | Contenido de las dos páginas; `componentes.figura` siempre las pone |
| Retirar `tools/servicios` de estas páginas | Tareas 6 y 7 (`pages.py`, `test_pagos.py`) |
| Paridad (encabezados, FAQ, precios, enlaces, meta, tipos de JSON-LD) | Tareas 1, 3, 6 y 7 (`test_paridad.py`, `PARIDAD`) |

Fuera de 2d: `/empresas` (Etapa 3), títulos y descripciones nuevos salvo los dos arreglos declarados (Etapa 3), grafo JSON-LD único y el `@id` `#localbusiness` (Etapa 4), corregir la URL del REPSE en `llms.txt` (`/Publico` responde 404; Etapa 4), mensualidades con tarjeta en B2B (el pago de proyectos es anticipo y avances), borrar `servicios.css` (2i).

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{mayoreo-pasto-tampico,palmas-mayoreo-proyectos}.json` | Lo que publicaba cada página antes de migrar (los escribe `paridad.py capturar`). |
| `tools/site/plantillas/b2b.py` | Plantilla B2B: portada, clientes, escalas con cotizador, documentación, paquetes, proceso, garantía, FAQ, cobertura, relacionados, cierre y JSON-LD. |
| `tools/site/contenido/b2b_comun.py` | Documentación, preguntas de compras, sectores, cobertura e índice B2B (`PAGINAS`) que comparten las dos páginas y reutilizará `/empresas`. |
| `tools/site/contenido/mayoreo_pasto.py` | Mayoreo: escalas de `datos.py`, cotizador por volumen, opinión de la constructora, 3 paquetes, 8 preguntas, garantía de arraigo cuando instalamos. |
| `tools/site/contenido/palmas_proyectos.py` | Palmas: tabla de 12 especies, armador de palmas, 3 paquetes por tipo de obra, 8 preguntas, garantía de plantas condicionada, ItemList y AggregateOffer nuevos. |
| `public/js/vt-b2b.js` | Cotizador por volumen (con `VTMedidor.calcular`) y armador de palmas; funciones puras exportadas. |
| `public/js/tests/vt-b2b.test.js`, `public/js/tests/casos-b2b.json` | Pruebas de `node --test` y casos de paridad con Python. |
| `tools/site/tests/test_b2b_paridad.py` | Los casos de `casos-b2b.json` contra `componentes.py`. |
| `tools/site/tests/test_b2b.py` | Las dos páginas: secuencia, clientes, mensajes, precios, anticipo, enlaces, JSON-LD. |

Se modifican: `tools/site/datos.py`, `mensajes_paginas.py`, `paridad.py`, `componentes.py`, `generar.py`, `public/css/terra.css`; `tools/servicios/pages.py` y `tools/servicios/tests/test_pagos.py`; pruebas `test_datos`, `test_paginas`, `test_paridad`, `test_componentes`, `test_terra_css`, `test_generar`, `test_consistencia`, `test_guia_palmas`, `test_reglas`, `test_plantillas_navegador`. Regenerados por el build: las dos páginas, `public/css/terra.<hash>.css`, `tools/site/activos.json` y el `<head>` de las páginas por el hash de `terra.css`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Crear el worktree desde `main` actualizado**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git worktree add ~/dev/viverosterra-e2d -b feat/etapa-2d
cd ~/dev/viverosterra-e2d && git log --oneline -1
```

Expected: el commit de `main` que agrega este plan (padre `00cad4d`).

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
curl -s -o /dev/null -w "%{http_code}\n" https://repse.stps.gob.mx/
```

Expected: `plantillas: 0 de 28 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 368 tests` y `OK`; `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 42` y `ℹ fail 0`; `playwright ok`; `200` (el padrón del REPSE que enlazan las páginas; si no responde 200, detente y avisa).

---

### Task 1: Capturas de paridad antes de migrar

**Files:**
- Create: `tools/site/tests/paridad/mayoreo-pasto-tampico.json`, `tools/site/tests/paridad/palmas-mayoreo-proyectos.json`

- [ ] **Step 1: Capturar las dos páginas tal como están en `main`**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/paridad.py capturar /mayoreo-pasto-tampico /palmas-mayoreo-proyectos
python3 -c "
import json
for p in ('mayoreo-pasto-tampico','palmas-mayoreo-proyectos'):
    d=json.load(open(f'tools/site/tests/paridad/{p}.json')); print(p, len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']), len(d['jsonld_tipos']))"
```

Expected: dos líneas `captura: …`; luego `mayoreo-pasto-tampico 11 4 1 1 9` y `palmas-mayoreo-proyectos 56 9 17 1 14`.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/tests/paridad/mayoreo-pasto-tampico.json tools/site/tests/paridad/palmas-mayoreo-proyectos.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de mayoreo y palmas para proyectos antes de migrarlas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Datos de empresas y mensajes de compras

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/mensajes_paginas.py`, `public/{mayoreo-pasto-tampico,palmas-mayoreo-proyectos}/index.html` (solo el shell)
- Test: `tools/site/tests/test_datos.py`, `tools/site/tests/test_paginas.py`

`ANTICIPO_PROYECTOS` es la frase que ya publica palmas en `main` (decisión del dueño, sin porcentaje). `PALMAS_PROYECTO` son las 12 especies que listaba palmas en `main`, con los únicos precios que dio el dueño el 2026-11-07; las demás llevan `None` y la página dice "Según cotización". Los mensajes de compras son los de `main` (`tools/servicios/pages.py`) con los huecos `___`.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/tests/test_datos.py b/tools/site/tests/test_datos.py
index 523c622..08d4fac 100644
--- a/tools/site/tests/test_datos.py
+++ b/tools/site/tests/test_datos.py
@@ -103,6 +103,17 @@ class DatosTest(unittest.TestCase):
         self.assertEqual(nombres, ["Daniela M.", "Ing. Roberto S.", "Carolina R.", "Ing. Gerardo M.", "Roberto C.",
                                    "María V."])
 
+    def test_datos_de_empresas_etapa_2d(self):
+        self.assertEqual(datos.ANTICIPO_PROYECTOS, "Para proyectos solicitamos un anticipo al confirmar y el resto se "
+                                                   "acuerda contra avances de obra; te lo detallamos en la cotización.")
+        self.assertNotIn("%", datos.ANTICIPO_PROYECTOS)
+        self.assertEqual(datos.REPSE_PADRON, "https://repse.stps.gob.mx/")
+        self.assertEqual(len(datos.PALMAS_PROYECTO), 12)
+        con_precio = {n: p for n, _sci, p in datos.PALMAS_PROYECTO if p is not None}
+        self.assertEqual(con_precio, {"Palma areca": 250, "Coco plumoso": 250, "Palma real": 500})
+        self.assertEqual((datos.PRECIOS["palma_desde"], datos.PRECIOS["palma_real"]), (250, 500))
+        self.assertEqual(len({n for n, _s, _p in datos.PALMAS_PROYECTO}), 12)
+
     def test_mensajes_terminan_con_la_firma(self):
         for servicio in datos.MENSAJES:
             with self.subTest(servicio=servicio):
diff --git a/tools/site/tests/test_paginas.py b/tools/site/tests/test_paginas.py
index 5dbd324..a4c8af1 100644
--- a/tools/site/tests/test_paginas.py
+++ b/tools/site/tests/test_paginas.py
@@ -103,6 +103,17 @@ class ContextoTest(unittest.TestCase):
         self.assertEqual(sorted(mensajes_paginas.SERVICIOS), ["/diseno-jardines-tampico", "/mantenimiento-jardines-tampico",
                                                               "/sistema-riego-tampico"])
 
+    def test_empresas_con_su_mensaje_en_menu_barra_y_pie(self):
+        """Etapa 2d: mayoreo y palmas para proyectos llevan en el menú, la barra y el pie su plantilla de compras."""
+        for ruta, texto in mensajes_paginas.EMPRESAS.items():
+            ctx = paginas.contexto(ruta)
+            with self.subTest(ruta=ruta):
+                self.assertEqual(ctx["mensaje"], datos.con_firma(texto))
+                self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
+                self.assertIn("Empresa: ___", texto)
+                self.assertIn("Obra y ubicación: ___", texto)
+        self.assertEqual(sorted(mensajes_paginas.EMPRESAS), ["/mayoreo-pasto-tampico", "/palmas-mayoreo-proyectos"])
+
     def test_ruta_desconocida_falla(self):
         with self.assertRaises(KeyError):
             paginas.contexto("/no-existe")
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas 2>&1 | grep -E "^(FAIL|ERROR):|FAILED"`
Expected: `ERROR: test_datos_de_empresas_etapa_2d`, `ERROR: test_empresas_con_su_mensaje_en_menu_barra_y_pie` y `FAILED (errors=2)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/datos.py b/tools/site/datos.py
index 766c789..4431ba4 100644
--- a/tools/site/datos.py
+++ b/tools/site/datos.py
@@ -65,6 +65,7 @@ PRECIOS = {
     "poda": 500,
     "flamboyan": 250,
     "palma_desde": 250,
+    "palma_real": 500,
     "tierra_negra_costal": 90,
     "tierra_negra_m3": 1500,
     "tezontle_costal": 200,
@@ -94,6 +95,13 @@ MANTENIMIENTO_PREMIUM = SEGUN_COTIZACION
 # (test_reglas.py).
 SISTEMAS_RIEGO = "+200"
 PROYECTOS_B2B = "+200"
+# Empresas (Etapa 2d). Cómo se paga un proyecto (decisión del dueño): anticipo al confirmar y el resto contra avances de
+# obra, sin porcentaje y sin crédito. La misma frase en mayoreo y en palmas para proyectos (test_consistencia.py).
+ANTICIPO_PROYECTOS = ("Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contra avances de obra; "
+                      "te lo detallamos en la cotización.")
+# Padrón público del REPSE de la STPS, donde cualquiera consulta el folio. (La ruta /Publico que cita llms.txt responde
+# 404: se corrige con llms.txt en la Etapa 4.)
+REPSE_PADRON = "https://repse.stps.gob.mx/"
 LLEGADA_PASTO = "una vez por semana, generalmente los viernes"
 ANTICIPO = ("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
             "un anticipo.")
@@ -106,6 +114,24 @@ RESPUESTA_PRECIO_PASTO = (
     f"Precios {ANIO}, con IVA, para Tampico, Ciudad Madero y Altamira."
 )
 
+# Palmas y especies para proyectos (nombre, nombre científico, precio "desde" o None). Decisión del dueño (2026-11-07):
+# areca y coco plumoso desde $250 y palma real desde $500 en su tamaño más chico; el precio sube con la altura. Las demás,
+# "según cotización" (SEGUN_COTIZACION): no se inventa ningún precio. Cycas, bambú y yucca se piden junto con las palmas.
+PALMAS_PROYECTO = (
+    ("Palma areca", "Dypsis lutescens", PRECIOS["palma_desde"]),
+    ("Coco plumoso", "Syagrus romanzoffiana", PRECIOS["palma_desde"]),
+    ("Palma real", "Roystonea regia", PRECIOS["palma_real"]),
+    ("Palma washingtonia", "Washingtonia robusta", None),
+    ("Palma del viajero", "Ravenala madagascariensis", None),
+    ("Palma cola de zorro", "Wodyetia bifurcata", None),
+    ("Palma triángulo", "Dypsis decaryi", None),
+    ("Palma kerpis", "Hyophorbe lagenicaulis", None),
+    ("Palma bambú", "Chamaedorea seifrizii", None),
+    ("Cycas revoluta", "Cycas revoluta", None),
+    ("Bambú tarro", "Bambusa vulgaris", None),
+    ("Yucca rostrata", "Yucca rostrata", None),
+)
+
 # Permiso del dueño (2026-11-07) para mostrarlos con nombre y logo. Renault (cliente real, permiso del dueño) va con su
 # nombre en texto: no hay logo en public/img/clientes y no se inventa uno.
 CLIENTES_B2B = ("BMW", "Taghleef Industries", "Gobierno de Tampico", "Grupo Velas", "Velamar", "Flex", "Renault")
diff --git a/tools/site/mensajes_paginas.py b/tools/site/mensajes_paginas.py
index 415e23c..6cae001 100644
--- a/tools/site/mensajes_paginas.py
+++ b/tools/site/mensajes_paginas.py
@@ -17,12 +17,22 @@ SERVICIOS = {
                                "Tengo pasto, plantas o ambos: ___\nLes mando fotos del espacio."),
 }
 
+# Empresas (Etapa 2d): la plantilla de compras de cada página B2B (la de main, con los huecos ___). La usan la portada, el
+# cierre y los cotizadores mientras no tienen datos y, por RUTAS, el menú, la barra móvil y el pie.
+EMPRESAS = {
+    "/mayoreo-pasto-tampico": ("Hola, quiero cotizar pasto San Agustín al mayoreo para un proyecto.\nEmpresa: ___\n"
+                               "Obra y ubicación: ___\nm² totales: ___\nFecha de la primera entrega: ___"),
+    "/palmas-mayoreo-proyectos": ("Hola, quiero cotizar palmas para un proyecto.\nEmpresa: ___\nObra y ubicación: ___\n"
+                                  "Especies, altura y cantidad: ___\nFecha de entrega: ___"),
+}
+
 # Ruta exacta → (mensaje del menú y la barra, mensaje del pie o None para usar el mismo).
 RUTAS = {
     "/blog": ("Hola, vi el blog de Viveros Terra y quiero cotizar", None),
     "/catalogo": ("Hola, vi el catálogo y quiero cotizar una planta", None),
     "/precios": ("Hola, vi la lista de precios y quiero cotizar", "Hola, tengo una pregunta sobre precios"),
     **{ruta: (texto, None) for ruta, texto in SERVICIOS.items()},
+    **{ruta: (texto, None) for ruta, texto in EMPRESAS.items()},
 }
 # Tienda y páginas de envío: el pie conserva su "pregunta"; el menú usa el mensaje de cotizar pasto sintético.
 PIE_TIPO = {
EOF
```

- [ ] **Step 4: Build y pruebas**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
```

Expected: `plantillas: 0 de 28 páginas escritas`, `shell: 2 de 108 páginas actualizadas` (el menú, la barra y el pie de las dos páginas llevan ya su plantilla de compras) y luego `0 de 108`; el `status` solo muestra los cuatro `.py`.
Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas tests.test_reglas tests.test_consistencia 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/datos.py tools/site/mensajes_paginas.py tools/site/tests/test_datos.py tools/site/tests/test_paginas.py public/mayoreo-pasto-tampico/index.html public/palmas-mayoreo-proyectos/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(datos): anticipo de proyectos, padrón del REPSE, palmas para proyectos y mensajes de compras" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: La paridad acepta un cambio de meta declarado

**Files:**
- Modify: `tools/site/paridad.py`
- Test: `tools/site/tests/test_paridad.py`

Hasta 2c la meta tenía que quedar idéntica. En 2d dos descripciones publicadas no pueden seguir: palmas dice "12 especies desde $850" (precio sin confirmar que contradice el "desde $250" del dueño) y mayoreo repite "Factura CFDI, factura CFDI". `meta_distinta` acepta el cambio solo con el valor nuevo exacto y un motivo de más de 20 caracteres en `PARIDAD["meta"]`; cualquier otro cambio de título, descripción, canonical u Open Graph sigue fallando.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/tests/test_paridad.py b/tools/site/tests/test_paridad.py
index 0717537..9972c59 100644
--- a/tools/site/tests/test_paridad.py
+++ b/tools/site/tests/test_paridad.py
@@ -27,6 +27,26 @@ class ParidadTest(unittest.TestCase):
                 with self.subTest(ruta=ruta, entrada=viejo):
                     self.assertIn(viejo, conocidos)
 
+    def test_cambios_de_meta_declarados_son_de_la_captura(self):
+        """PARIDAD["meta"] solo nombra claves que la página publicaba, con un valor distinto al de la captura."""
+        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
+            cambios = generar.cargar(contenido).PARIDAD.get("meta", {})
+            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
+            for clave, (nuevo, _motivo) in cambios.items():
+                with self.subTest(ruta=ruta, clave=clave):
+                    self.assertIn(clave, captura["meta"])
+                    self.assertNotEqual(captura["meta"][clave], nuevo)
+
+    def test_meta_distinta(self):
+        viejo = {"title": "T", "description": "Desde $850"}
+        self.assertEqual(paridad.meta_distinta(viejo, dict(viejo)), [])
+        nuevo = {"title": "T", "description": "Desde $250"}
+        self.assertEqual(paridad.meta_distinta(viejo, nuevo), ["description: 'Desde $850' → 'Desde $250'"])
+        motivo = "Precio corregido por el dueño el 2026-11-07"
+        self.assertEqual(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $250", motivo)}), [])
+        self.assertEqual(len(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $300", motivo)})), 1)
+        self.assertEqual(len(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $250", "corto")})), 1)
+
     def test_opiniones_de_la_home_se_conservan(self):
         """Decisión del dueño (2026-11-07): las opiniones con nombre de la home son reales; no se pueden retirar."""
         mapa = generar.cargar("inicio").PARIDAD
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_paridad 2>&1 | grep -E "^(FAIL|ERROR):|FAILED"`
Expected: `ERROR: test_meta_distinta` y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/paridad.py b/tools/site/paridad.py
index 4f1ecef..9171bb2 100644
--- a/tools/site/paridad.py
+++ b/tools/site/paridad.py
@@ -3,7 +3,9 @@
 Antes de migrar se congela lo que la página publicaba (`capturar`): meta (título, descripción, robots, canonical, Open
 Graph), tipos del JSON-LD, encabezados h1–h3, preguntas frecuentes, precios y enlaces internos del <main>. Después,
 tests/test_paridad.py exige que cada elemento siga en la página nueva o que el contenido diga a dónde fue
-(PARIDAD["reemplazos"]) o por qué se retiró (PARIDAD["retirados"]).
+(PARIDAD["reemplazos"]) o por qué se retiró (PARIDAD["retirados"]). La meta no cambia salvo que el contenido declare el
+valor nuevo y el motivo (PARIDAD["meta"]: {clave: (valor nuevo, motivo)}; desde 2d, para no publicar un precio que el
+dueño corrigió).
 
 Uso:
   python3 tools/site/paridad.py capturar /pasto-en-rollo-tampico   (congela tests/paridad/pasto-en-rollo-tampico.json)
@@ -113,6 +115,21 @@ def faltantes(viejos, nuevos, mapa):
     return salida
 
 
+def meta_distinta(viejo, nuevo, cambios=None):
+    """Claves de la meta que cambiaron sin un cambio declarado con su valor nuevo exacto y un motivo escrito."""
+    cambios = cambios or {}
+    salida = []
+    for clave, valor in viejo.items():
+        actual = nuevo.get(clave)
+        if actual == valor:
+            continue
+        declarado = cambios.get(clave)
+        if declarado and declarado[0] == actual and len(declarado[1]) > 20:
+            continue
+        salida.append(f"{clave}: {valor!r} → {actual!r}")
+    return salida
+
+
 def nombre_captura(ruta):
     return "index" if ruta == "/" else ruta.strip("/").replace("/", "_")
 
@@ -141,8 +158,7 @@ def comparar(ruta, mapa, public=paginas.PUBLIC, capturas=CAPTURAS):
     nuevo = extraer(html)
     nuevo["enlaces"] = enlaces(html)
     resultado = {c: faltantes(viejo[c], nuevo[c], mapa) for c in CATEGORIAS}
-    resultado["meta"] = [f"{k}: {v!r} → {nuevo['meta'].get(k)!r}" for k, v in viejo["meta"].items()
-                         if nuevo["meta"].get(k) != v]
+    resultado["meta"] = meta_distinta(viejo["meta"], nuevo["meta"], mapa.get("meta"))
     resultado["jsonld_tipos"] = sorted(set(viejo["jsonld_tipos"]) - set(nuevo["jsonld_tipos"]))
     return resultado
 
EOF
```

- [ ] **Step 4: Pruebas**

Run: `cd tools/site && python3 -m unittest tests.test_paridad 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/paridad.py tools/site/tests/test_paridad.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(paridad): la meta cambia solo con el valor nuevo y el motivo declarados en PARIDAD" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Cotizador de pasto por volumen y armador de palmas

**Files:**
- Modify: `tools/site/componentes.py`
- Create: `public/js/vt-b2b.js`, `public/js/tests/vt-b2b.test.js`, `public/js/tests/casos-b2b.json`, `tools/site/tests/test_b2b_paridad.py`
- Test: `tools/site/tests/test_componentes.py`

Lo que hace cada pieza:

- `leer_m2` / `leerM2`: "1,200" y "1200" son 1,200 m² (coma de miles, como se escribe en México), "12,5" es 12.5 y "800 m²" es 800; vacío, negativo, texto o más de 1,000,000 m² dan 0 y el botón se queda con la plantilla de compras.
- `calculo_volumen(m2)` es `calculo_medidor(m2, 1, "mayoreo")`: misma regla, mismo aviso ("El mayoreo aplica desde 500 m². Te faltan N m²; mientras, calculamos a $85/m² (solo pasto)."). En el navegador, `vt-b2b.js` llama a `VTMedidor.calcular` con los modos que el HTML trae en `data-modos` (escritos desde `MODOS_MEDIDOR`, es decir desde `datos.py`).
- `cotizador_volumen` y `armador_palmas` llevan `data-hero-cta` (la barra móvil se esconde mientras se ven, como con el Medidor), labels visibles en cada control, `role="status"` en la etiqueta y un enlace `wa.me` con `data-cta` (`b2b:cotizador`, `b2b:armador`): terra.js mide el clic y firma el mensaje.
- El armador empieza con 3 renglones; "Agregar otra especie" sale con `hidden` (sin JS no ofrece un botón que no hace nada) y agrega hasta 8 renglones con ids y `for` propios. No muestra total: el precio depende de la altura de cada ejemplar.
- `repse()`: "REPSE 773725 · consulta el folio en el padrón público de la STPS" con enlace a `datos.REPSE_PADRON`.

- [ ] **Step 1: Escribir las pruebas y los casos de paridad**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/tests/test_componentes.py b/tools/site/tests/test_componentes.py
index 410b502..711e55a 100644
--- a/tools/site/tests/test_componentes.py
+++ b/tools/site/tests/test_componentes.py
@@ -225,6 +225,62 @@ class MedidorTest(unittest.TestCase):
         self.assertEqual(html.count("aria-live"), 0)
 
 
+class EmpresasTest(unittest.TestCase):
+    def test_cotizador_por_volumen_empieza_vacio_con_los_precios_de_datos(self):
+        html = c.cotizador_volumen("may", "b2b", "Hola, quiero cotizar pasto al mayoreo.")
+        self.assertIn('data-vt-volumen data-hero-cta', html)  # la barra móvil se esconde con el cotizador a la vista
+        self.assertIn('data-cta="b2b:cotizador"', html)
+        self.assertIn('<label for="may-m2">m² totales de la obra</label>', html)
+        self.assertIn('id="may-m2" data-vt-campo="m2" inputmode="decimal"', html)
+        self.assertIn(f">{c.VACIO_VOLUMEN['medida']}<", html)
+        self.assertIn('class="vt-etiqueta__precio is-vacio"', html)
+        self.assertIn('&quot;mayoreo&quot;:{&quot;precio&quot;:60,&quot;desde&quot;:true,&quot;minimo&quot;:500', html)
+        self.assertIn('&quot;solo&quot;:{&quot;precio&quot;:85', html)
+        self.assertNotIn("instalado", html.split("data-modos=")[1].split('"')[1])
+        enlace = re.search(r'data-vt-o="cta" href="([^"]+)"', html).group(1)
+        self.assertTrue(unquote(enlace.split("text=", 1)[1].replace("&amp;", "&")).endswith(datos.FIRMA))
+        for campo in ("empresa", "obra", "fecha"):
+            self.assertIn(f'data-vt-campo="{campo}" type="text"', html)
+
+    def test_volumen_con_menos_de_500_m2_nunca_a_precio_de_mayoreo(self):
+        for m2 in (1, 250, 499.9):
+            with self.subTest(m2=m2):
+                r = c.calculo_volumen(m2)
+                self.assertEqual(r["precio"], datos.PRECIOS["pasto_solo_m2"])
+                self.assertIn("Te faltan", r["aviso"])
+        self.assertEqual(c.calculo_volumen(500)["precio"], datos.PRECIOS["pasto_mayoreo_m2"])
+
+    def test_armador_de_palmas_con_las_especies_de_datos_y_labels(self):
+        html = c.armador_palmas("pal", "b2b", "Hola, quiero cotizar palmas.")
+        self.assertEqual(html.count("data-vt-fila>"), c.FILAS_PALMAS)
+        for n in range(1, c.FILAS_PALMAS + 1):
+            for campo in ("especie", "altura", "cantidad"):
+                self.assertIn(f'<label for="pal-{campo}-{n}">', html)
+                self.assertIn(f'id="pal-{campo}-{n}"', html)
+        for nombre, cientifico, _precio in datos.PALMAS_PROYECTO:
+            self.assertIn(f'<option value="{nombre}">{nombre} ({cientifico})</option>', html)
+        self.assertIn(c.OTRA_ESPECIE, html)
+        self.assertIn('data-vt-palmas data-hero-cta', html)
+        self.assertIn('data-vt-agregar hidden', html)  # sin JS no se ofrece un botón que no hace nada
+        self.assertIn('data-cta="b2b:armador"', html)
+        self.assertNotRegex(html, r"\$\d")  # sin precio total: depende de la altura
+
+    def test_mensaje_y_resumen_de_palmas(self):
+        filas = [("Palma real", "3", "40"), ("Coco plumoso", "", ""), ("", "5", "10")]
+        self.assertEqual(c.mensaje_palmas(filas, "Mi empresa").split("\n"), [
+            "Hola, quiero cotizar palmas para un proyecto.", "- 40 × Palma real, altura aprox.: 3 m",
+            "- ___ × Coco plumoso, altura aprox.: ___", "Empresa: Mi empresa", "Obra y ubicación: ___",
+            "Fecha de entrega: ___"])
+        self.assertEqual(c.resumen_palmas(filas), "2 especies · 40 piezas")
+        self.assertEqual(c.mensaje_palmas([("", "", "")]), "")
+        self.assertEqual(c.resumen_palmas([("", "", "")]), c.VACIO_PALMAS)
+
+    def test_repse_verificable(self):
+        html = c.repse()
+        self.assertIn(f"REPSE {datos.REPSE}", html)
+        self.assertIn(f'href="{datos.REPSE_PADRON}" target="_blank" rel="noopener"', html)
+
+
 class EscapeTest(unittest.TestCase):
     def test_bloque_y_figura_escapan_atributos(self):
         html = c.bloque(1, "R", 'a"b', "T", "", id_seccion='c"d')
EOF
cat > tools/site/tests/test_b2b_paridad.py <<'EOF'
"""Los cotizadores de empresas dan lo mismo en Python (componentes.py, HTML inicial y pruebas) y en JavaScript
(public/js/vt-b2b.js con VTMedidor.calcular). Los casos viven en public/js/tests/casos-b2b.json; node --test los corre
contra el JS."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-b2b.json")
                   .read_text(encoding="utf-8"))


class B2BParidadTest(unittest.TestCase):
    def test_volumen_igual_que_el_js(self):
        for caso in CASOS["volumen"]:
            e = caso["entrada"]
            r = c.calculo_volumen(c.leer_m2(e["texto"]))
            obtenido = {k: r[k] for k in ("m2", "precio", "desde", "total", "rotulo", "aviso")}
            obtenido.update(c.textos_volumen(r, e["empresa"], e["obra"], e["fecha"]))
            with self.subTest(entrada=e):
                self.assertEqual(obtenido, caso["esperado"])

    def test_lecturas_de_m2(self):
        for texto, esperado in CASOS["lecturas"]:
            with self.subTest(texto=texto):
                self.assertEqual(c.leer_m2(texto), esperado)

    def test_palmas_igual_que_el_js(self):
        for caso in CASOS["palmas"]:
            e = caso["entrada"]
            filas = [tuple(f) for f in e["filas"]]
            with self.subTest(entrada=e):
                self.assertEqual(c.mensaje_palmas(filas, e["empresa"], e["obra"], e["fecha"]), caso["esperado"]["mensaje"])
                self.assertEqual(c.resumen_palmas(filas), caso["esperado"]["resumen"])

    def test_modos_del_json_son_los_del_medidor(self):
        self.assertEqual(CASOS["modos"], {k: {kk: v for kk, v in c.MODOS_MEDIDOR[k].items() if kk != "opcion"}
                                          for k in ("mayoreo", "solo")})

    def test_hay_casos_bajo_y_sobre_el_minimo(self):
        precios = {caso["esperado"]["precio"] for caso in CASOS["volumen"]}
        self.assertEqual(precios, {c.P["pasto_mayoreo_m2"], c.P["pasto_solo_m2"]})


if __name__ == "__main__":
    unittest.main()
EOF
cat > public/js/tests/casos-b2b.json <<'EOF'
{
 "modos": {"mayoreo": {"precio": 60, "desde": true, "minimo": 500, "texto": "pasto San Agustín de mayoreo (solo pasto)", "rotulo": "Mayoreo · desde"}, "solo": {"precio": 85, "desde": false, "texto": "solo el pasto San Agustín (yo lo instalo)", "rotulo": "Solo pasto"}},
 "volumen": [
  {"entrada": {"texto": "1,200", "empresa": "", "obra": "", "fecha": ""}, "esperado": {"m2": 1200.0, "precio": 60, "desde": true, "total": 72000, "rotulo": "Mayoreo · desde", "aviso": "", "medida": "1,200 m²", "monto": "$72,000", "calc": "1,200 m² × desde $60/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar pasto San Agustín de mayoreo (solo pasto) para un proyecto.\nm² totales: 1,200 m²\nEstimado de la web: desde $72,000 con IVA (desde $60/m²)\nEmpresa: ___\nObra y ubicación: ___\nFecha de la primera entrega: ___"}},
  {"entrada": {"texto": "500", "empresa": "Mi empresa", "obra": "Fraccionamiento en Altamira", "fecha": "marzo"}, "esperado": {"m2": 500.0, "precio": 60, "desde": true, "total": 30000, "rotulo": "Mayoreo · desde", "aviso": "", "medida": "500 m²", "monto": "$30,000", "calc": "500 m² × desde $60/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar pasto San Agustín de mayoreo (solo pasto) para un proyecto.\nm² totales: 500 m²\nEstimado de la web: desde $30,000 con IVA (desde $60/m²)\nEmpresa: Mi empresa\nObra y ubicación: Fraccionamiento en Altamira\nFecha de la primera entrega: marzo"}},
  {"entrada": {"texto": "499.5", "empresa": "", "obra": "", "fecha": ""}, "esperado": {"m2": 499.5, "precio": 85, "desde": false, "total": 42458, "rotulo": "Solo pasto (mayoreo desde 500 m²)", "aviso": "El mayoreo aplica desde 500 m². Te faltan 1 m²; mientras, calculamos a $85/m² (solo pasto).", "medida": "499.5 m²", "monto": "$42,458", "calc": "499.5 m² × $85/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo) para un proyecto.\nm² totales: 499.5 m²\nEstimado de la web: $42,458 con IVA ($85/m²)\nEmpresa: ___\nObra y ubicación: ___\nFecha de la primera entrega: ___"}},
  {"entrada": {"texto": "12,5", "empresa": "", "obra": "", "fecha": ""}, "esperado": {"m2": 12.5, "precio": 85, "desde": false, "total": 1063, "rotulo": "Solo pasto (mayoreo desde 500 m²)", "aviso": "El mayoreo aplica desde 500 m². Te faltan 488 m²; mientras, calculamos a $85/m² (solo pasto).", "medida": "12.5 m²", "monto": "$1,063", "calc": "12.5 m² × $85/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo) para un proyecto.\nm² totales: 12.5 m²\nEstimado de la web: $1,063 con IVA ($85/m²)\nEmpresa: ___\nObra y ubicación: ___\nFecha de la primera entrega: ___"}},
  {"entrada": {"texto": "320 m²", "empresa": "Mi empresa", "obra": "", "fecha": ""}, "esperado": {"m2": 320.0, "precio": 85, "desde": false, "total": 27200, "rotulo": "Solo pasto (mayoreo desde 500 m²)", "aviso": "El mayoreo aplica desde 500 m². Te faltan 180 m²; mientras, calculamos a $85/m² (solo pasto).", "medida": "320 m²", "monto": "$27,200", "calc": "320 m² × $85/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo) para un proyecto.\nm² totales: 320 m²\nEstimado de la web: $27,200 con IVA ($85/m²)\nEmpresa: Mi empresa\nObra y ubicación: ___\nFecha de la primera entrega: ___"}},
  {"entrada": {"texto": "2,500.5", "empresa": "", "obra": "", "fecha": ""}, "esperado": {"m2": 2500.5, "precio": 60, "desde": true, "total": 150030, "rotulo": "Mayoreo · desde", "aviso": "", "medida": "2,500.5 m²", "monto": "$150,030", "calc": "2,500.5 m² × desde $60/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.", "mensaje": "Hola, quiero cotizar pasto San Agustín de mayoreo (solo pasto) para un proyecto.\nm² totales: 2,500.5 m²\nEstimado de la web: desde $150,030 con IVA (desde $60/m²)\nEmpresa: ___\nObra y ubicación: ___\nFecha de la primera entrega: ___"}}
 ],
 "lecturas": [["1,200", 1200.0], ["1200", 1200.0], ["12,5", 12.5], ["800 m²", 800.0], ["", 0], ["-3", 0], ["abc", 0], ["2,000,000", 0], ["1e3", 0], ["0", 0]],
 "palmas": [
  {"entrada": {"filas": [["Palma real", "3", "40"], ["Coco plumoso", "", ""], ["", "5", "10"]], "empresa": "Mi empresa", "obra": "", "fecha": ""}, "esperado": {"mensaje": "Hola, quiero cotizar palmas para un proyecto.\n- 40 × Palma real, altura aprox.: 3 m\n- ___ × Coco plumoso, altura aprox.: ___\nEmpresa: Mi empresa\nObra y ubicación: ___\nFecha de entrega: ___", "resumen": "2 especies · 40 piezas"}},
  {"entrada": {"filas": [["Palma areca", "2,5", "120 pzas"], ["Otra especie", "", "3"]], "empresa": "", "obra": "", "fecha": ""}, "esperado": {"mensaje": "Hola, quiero cotizar palmas para un proyecto.\n- 120 × Palma areca, altura aprox.: 2.5 m\n- 3 × Otra especie, altura aprox.: ___\nEmpresa: ___\nObra y ubicación: ___\nFecha de entrega: ___", "resumen": "2 especies · 123 piezas"}},
  {"entrada": {"filas": [["", "", ""], ["", "", ""]], "empresa": "", "obra": "", "fecha": ""}, "esperado": {"mensaje": "", "resumen": "Elige especie y cantidad"}},
  {"entrada": {"filas": [["Palma washingtonia", "60", "0"]], "empresa": "", "obra": "", "fecha": ""}, "esperado": {"mensaje": "Hola, quiero cotizar palmas para un proyecto.\n- ___ × Palma washingtonia, altura aprox.: ___\nEmpresa: ___\nObra y ubicación: ___\nFecha de entrega: ___", "resumen": "1 especie · cantidad por definir"}}
 ]
}
EOF
cat > public/js/tests/vt-b2b.test.js <<'EOF'
// public/js/tests/vt-b2b.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const { calcular } = require('../vt-medidor.js');
const B = require('../vt-b2b.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-b2b.json'), 'utf8'));

test('cotizador por volumen: mismos resultados que tools/site/componentes.py en casos-b2b.json', () => {
  for (const { entrada, esperado } of CASOS.volumen) {
    const r = calcular(B.leerM2(entrada.texto), 1, 'mayoreo', CASOS.modos);
    const t = B.textosVolumen(r, entrada);
    const obtenido = { m2: r.m2, precio: r.precio, desde: r.desde, total: r.total, rotulo: r.rotulo, aviso: r.aviso, ...t };
    assert.deepStrictEqual(obtenido, esperado, JSON.stringify(entrada));
  }
});

test('lectura de m²: miles con coma, coma decimal y valores inválidos', () => {
  for (const [texto, esperado] of CASOS.lecturas) assert.strictEqual(B.leerM2(texto), esperado, texto);
});

test('con menos de 500 m² nunca sale a precio de mayoreo', () => {
  for (const m2 of [1, 120, 499, 499.9]) {
    const r = calcular(m2, 1, 'mayoreo', CASOS.modos);
    assert.strictEqual(r.precio, CASOS.modos.solo.precio);
    assert.match(B.textosVolumen(r, {}).mensaje, /solo el pasto San Agustín/);
  }
  assert.strictEqual(calcular(500, 1, 'mayoreo', CASOS.modos).precio, CASOS.modos.mayoreo.precio);
});

test('armador de palmas: mismo mensaje y resumen que componentes.py', () => {
  for (const { entrada, esperado } of CASOS.palmas) {
    assert.strictEqual(B.mensajePalmas(entrada.filas, entrada), esperado.mensaje, JSON.stringify(entrada));
    assert.strictEqual(B.resumenPalmas(entrada.filas), esperado.resumen, JSON.stringify(entrada));
  }
});

test('el mensaje de palmas es texto plano: un renglón por especie y los huecos de compras al final', () => {
  const m = B.mensajePalmas([['Palma real', '3', '40'], ['Coco plumoso', '', '']], {});
  const renglones = m.split('\n');
  assert.strictEqual(renglones.length, 6);
  assert.deepStrictEqual(renglones.slice(-3), ['Empresa: ___', 'Obra y ubicación: ___', 'Fecha de entrega: ___']);
  assert.doesNotMatch(m, /</);
});
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_componentes tests.test_b2b_paridad 2>&1 | tail -1`
Expected: `FAILED (errors=23)` (las funciones nuevas no existen).
Run: `node --test public/js/tests/vt-b2b.test.js 2>&1 | grep -E "Cannot find module|^ℹ fail"`
Expected: `Error: Cannot find module '../vt-b2b.js'` y `ℹ fail 1`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/componentes.py b/tools/site/componentes.py
index ad69b01..6524137 100644
--- a/tools/site/componentes.py
+++ b/tools/site/componentes.py
@@ -6,6 +6,7 @@ verifica); los atributos (href, src, alt, data-*) se escapan aquí. Todo número
 mensualidades es la de tools/pasto/mensualidades.py (la misma de public/js/vt-mensualidades.js): aquí no se reimplementa.
 """
 import html as html_mod
+import json
 import math
 import re
 import sys
@@ -555,6 +556,177 @@ def medidor(prefijo, tipo, largo=8, ancho=6, modo="instalado", mensaje=None):
         f'</span></a></div></div></div>')
 
 
+# ---------- empresas: cotizador por volumen y armador de palmas (public/js/vt-b2b.js; casos en casos-b2b.json) ----------
+M2_MAXIMO = 1_000_000  # más que esto no es una obra: el cotizador vuelve al mensaje de la página
+ALTURA_MAXIMA = 40
+CANTIDAD_MAXIMA = 100_000
+FILAS_PALMAS = 3  # renglones al cargar; vt-b2b.js agrega hasta 8
+MILES_RE = re.compile(r"^\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
+DECIMAL_RE = re.compile(r"^\d+(?:\.\d+)?$")
+ALTURA_RE = re.compile(r"^\s*(\d+(?:[.,]\d+)?)")
+CANTIDAD_RE = re.compile(r"^\s*(\d+)")
+VACIO_VOLUMEN = {"medida": "Escribe los m² de tu obra", "monto": "—",
+                 "calc": (f"Desde {MINIMO_MAYOREO} m², mayoreo desde ${P['pasto_mayoreo_m2']}/m²; con menos, "
+                          f"${P['pasto_solo_m2']}/m² (solo pasto). Con IVA.")}
+VACIO_PALMAS = "Elige especie y cantidad"
+OTRA_ESPECIE = "Otra especie (la escribo en el chat)"
+
+
+def _hueco(valor):
+    return (valor or "").strip() or "___"
+
+
+def leer_m2(texto):
+    """m² escritos por el visitante (como leerM2 de vt-b2b.js): "1,200" y "1200" son 1200, "12,5" es 12.5 y "800 m²" es
+    800. Devuelve 0 si no es un número mayor que 0 y hasta M2_MAXIMO."""
+    t = re.sub(r"\s|m²|m2", "", str(texto or ""), flags=re.I)
+    t = t.replace(",", "") if MILES_RE.match(t) else t.replace(",", ".", 1)
+    if not DECIMAL_RE.match(t):
+        return 0
+    n = float(t)
+    return n if 0 < n <= M2_MAXIMO else 0
+
+
+def calculo_volumen(m2):
+    """La regla del Medidor para el pasto de obra: mayoreo desde el mínimo y, con menos, solo pasto con su aviso."""
+    return calculo_medidor(m2, 1, "mayoreo")
+
+
+def textos_volumen(r, empresa="", obra="", fecha=""):
+    """Etiqueta y mensaje de compras para el resultado `r` de calculo_volumen."""
+    desde = "desde " if r["desde"] else ""
+    m2 = formato_m2(r["m2"])
+    mensaje = "\n".join((f"Hola, quiero cotizar {r['texto']} para un proyecto.", f"m² totales: {m2} m²",
+                         f"Estimado de la web: {desde}{dinero(r['total'])} con IVA ({desde}${r['precio']}/m²)",
+                         f"Empresa: {_hueco(empresa)}", f"Obra y ubicación: {_hueco(obra)}",
+                         f"Fecha de la primera entrega: {_hueco(fecha)}"))
+    return {"medida": f"{m2} m²", "monto": dinero(r["total"]),
+            "calc": (f"{m2} m² × {desde}${r['precio']}/m², con IVA. Solo pasto: la entrega por etapas y la instalación "
+                     "se cotizan con tu obra."),
+            "mensaje": mensaje}
+
+
+def leer_altura(texto):
+    m = ALTURA_RE.match(str(texto or ""))
+    n = redondear(float(m.group(1).replace(",", ".")) * 10) / 10 if m else 0
+    return n if 0 < n <= ALTURA_MAXIMA else 0
+
+
+def leer_cantidad(texto):
+    m = CANTIDAD_RE.match(str(texto or ""))
+    n = int(m.group(1)) if m else 0
+    return n if 0 < n <= CANTIDAD_MAXIMA else 0
+
+
+def linea_palma(especie, altura="", cantidad=""):
+    """Renglón del mensaje: "- 40 × Palma real, altura aprox.: 3 m"; sin especie no hay renglón."""
+    especie = (especie or "").strip()
+    if not especie:
+        return ""
+    n, alto = leer_cantidad(cantidad), leer_altura(altura)
+    return f"- {n or '___'} × {especie}, altura aprox.: {f'{formato_m2(alto)} m' if alto else '___'}"
+
+
+def mensaje_palmas(filas, empresa="", obra="", fecha=""):
+    """Un solo mensaje con toda la lista. filas: (especie, altura, cantidad) como los escribió el visitante. Sin
+    renglones devuelve "" (el botón se queda con el mensaje de la página)."""
+    lineas = [x for x in (linea_palma(*f) for f in filas) if x]
+    if not lineas:
+        return ""
+    return "\n".join(("Hola, quiero cotizar palmas para un proyecto.", *lineas, f"Empresa: {_hueco(empresa)}",
+                      f"Obra y ubicación: {_hueco(obra)}", f"Fecha de entrega: {_hueco(fecha)}"))
+
+
+def resumen_palmas(filas):
+    """Lo que dice la etiqueta: "2 especies · 60 piezas" (o "cantidad por definir")."""
+    con_especie = [f for f in filas if (f[0] or "").strip()]
+    if not con_especie:
+        return VACIO_PALMAS
+    n = len(con_especie)
+    piezas = sum(leer_cantidad(f[2]) for f in con_especie)
+    especies = f"{n} {'especie' if n == 1 else 'especies'}"
+    return f"{especies} · {piezas:,} piezas" if piezas else f"{especies} · cantidad por definir"
+
+
+def _campo(ident, campo, etiqueta, placeholder, unidad="", modo=None):
+    """Campo con su label visible; modo="decimal" o "numeric" pone el teclado numérico."""
+    teclado = f' inputmode="{modo}"' if modo else ' type="text"'
+    sufijo = f"<span>{unidad}</span>" if unidad else ""
+    return (f'<div class="vt-campo"><label for="{esc(ident)}">{etiqueta}</label><div class="vt-control"><input '
+            f'id="{esc(ident)}" data-vt-campo="{esc(campo)}"{teclado} placeholder="{esc(placeholder)}" '
+            f'autocomplete="off">{sufijo}</div></div>')
+
+
+def _datos_obra(prefijo):
+    return (_campo(f"{prefijo}-empresa", "empresa", "Empresa (opcional)", "Ej. tu razón social")
+            + _campo(f"{prefijo}-obra", "obra", "Obra y ubicación (opcional)", "Ej. fraccionamiento en Altamira")
+            + _campo(f"{prefijo}-fecha", "fecha", "Fecha aprox. de entrega (opcional)", "Ej. marzo"))
+
+
+def _boton_cta(tipo, seccion, mensaje):
+    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:{seccion}" data-vt-o="cta" '
+            f'href="{esc(datos.wa_url(mensaje))}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp'
+            '<span class="vt-flecha" aria-hidden="true">→</span></a>')
+
+
+def cotizador_volumen(prefijo, tipo, mensaje):
+    """Pasto para obra: m² totales → precio por volumen (la regla del Medidor: mayoreo desde el mínimo; con menos, solo
+    pasto y el aviso) → etiqueta → WhatsApp con m², estimado, empresa, obra y fecha. Los precios viajan en data-modos
+    (de MODOS_MEDIDOR, es decir de datos.py) y vt-b2b.js calcula con VTMedidor.calcular de vt-medidor.js."""
+    generico = datos.con_firma(mensaje)
+    modos = {k: {kk: v for kk, v in MODOS_MEDIDOR[k].items() if kk != "opcion"} for k in ("mayoreo", "solo")}
+    return (
+        f'<div class="vt-b2b" data-vt-volumen data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
+        f'data-mensaje="{esc(generico)}" data-modos="{esc(json.dumps(modos, ensure_ascii=False, separators=(",", ":")))}">'
+        '<div class="vt-b2b__form" role="group" aria-label="Cotizador de pasto por volumen">'
+        f'{_campo(f"{prefijo}-m2", "m2", "m² totales de la obra", "Ej. 1,200", "m²", "decimal")}{_datos_obra(prefijo)}'
+        '</div><div class="vt-etiqueta-x"><div class="vt-etiqueta vt-medidor__res" role="status">'
+        '<p class="vt-etiqueta__cod"><span>Tu etiqueta</span><span>Estimado</span></p>'
+        f'<p class="vt-etiqueta__nombre" data-vt-o="m2">{VACIO_VOLUMEN["medida"]}</p>'
+        '<p class="vt-etiqueta__sci">Stenotaphrum secundatum</p>'
+        f'<p class="vt-etiqueta__precio is-vacio"><small data-vt-o="rotulo">{MODOS_MEDIDOR["mayoreo"]["rotulo"]}</small>'
+        f'<b data-vt-o="monto">{VACIO_VOLUMEN["monto"]}</b><span>con IVA</span></p>'
+        f'<p class="vt-medidor__calc" data-vt-o="calc">{VACIO_VOLUMEN["calc"]}</p>'
+        '<p class="vt-medidor__aviso" data-vt-o="aviso" hidden></p>'
+        f'{_boton_cta(tipo, "cotizador", generico)}</div></div></div>')
+
+
+def _fila_palma(prefijo, n, especies):
+    opciones = "".join(f'<option value="{esc(nombre)}">{nombre} ({cientifico})</option>'
+                       for nombre, cientifico, _precio in especies)
+    return (f'<li class="vt-b2b__fila" data-vt-fila><div class="vt-campo"><label for="{prefijo}-especie-{n}">Especie'
+            f'</label><div class="vt-control"><select id="{prefijo}-especie-{n}" data-vt-campo="especie">'
+            f'<option value="">Elige una especie</option>{opciones}<option value="Otra especie">{OTRA_ESPECIE}</option>'
+            f'</select></div></div>{_campo(f"{prefijo}-altura-{n}", "altura", "Altura aprox.", "Ej. 3", "m", "decimal")}'
+            f'{_campo(f"{prefijo}-cantidad-{n}", "cantidad", "Cantidad", "Ej. 20", "pzas", "numeric")}</li>')
+
+
+def armador_palmas(prefijo, tipo, mensaje, especies=datos.PALMAS_PROYECTO):
+    """Palmas para obra: especie, altura y cantidad por renglón → un solo WhatsApp con la lista, empresa, obra y fecha.
+    Sin precio total: depende de la altura de cada ejemplar y se da por escrito en la cotización."""
+    generico = datos.con_firma(mensaje)
+    filas = "".join(_fila_palma(prefijo, n, especies) for n in range(1, FILAS_PALMAS + 1))
+    return (
+        f'<div class="vt-b2b" data-vt-palmas data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
+        f'data-mensaje="{esc(generico)}">'
+        '<div class="vt-b2b__form" role="group" aria-label="Lista de palmas para cotizar">'
+        f'<ol class="vt-b2b__filas" data-vt-filas>{filas}</ol>'
+        '<button type="button" class="vt-btn vt-btn--linea" data-vt-agregar hidden>Agregar otra especie</button>'
+        f'{_datos_obra(prefijo)}</div><div class="vt-etiqueta-x"><div class="vt-etiqueta" role="status">'
+        '<p class="vt-etiqueta__cod"><span>Tu lista</span><span>Para cotizar</span></p>'
+        f'<p class="vt-etiqueta__nombre" data-vt-o="resumen">{VACIO_PALMAS}</p>'
+        '<p class="vt-b2b__msg" data-vt-o="lista"></p>'
+        '<p class="vt-medidor__calc">El precio depende de la especie, la altura y la cantidad: te lo damos por escrito '
+        'en la cotización.</p>'
+        f'{_boton_cta(tipo, "armador", generico)}</div></div></div>')
+
+
+def repse():
+    """REPSE verificable: el folio y el padrón público de la STPS donde se consulta."""
+    return (f'<p class="vt-promesa">REPSE {datos.REPSE} · <a href="{esc(datos.REPSE_PADRON)}" target="_blank" '
+            'rel="noopener">consulta el folio en el padrón público de la STPS</a></p>')
+
+
 # ---------- portada (primer pantallazo: qué, dónde, precio y CTA) ----------
 def portada(p, tipo, migas_items=None):
     """p: kicker, h1, lede, etiqueta, mensaje, tambien y foto; opcional compacta (a 1024–1199 px la etiqueta va en su
EOF
cat > public/js/vt-b2b.js <<'EOF'
// public/js/vt-b2b.js
/* Cotizadores de las páginas para empresas (Etapa 2d). Mismo cálculo y mismos textos que tools/site/componentes.py
   (paridad en tests/casos-b2b.json); los precios no viven aquí:
   - [data-vt-volumen]: m² totales de la obra → precio por volumen con VTMedidor.calcular (vt-medidor.js): mayoreo desde
     el mínimo y, con menos, solo pasto con su aviso. Los modos y precios llegan en data-modos, escritos desde datos.py.
   - [data-vt-palmas]: especie, altura y cantidad por renglón (hasta 8) → un solo mensaje con toda la lista.
   Los botones son enlaces de WhatsApp con data-cta: terra.js los mide (generate_lead) y los firma al hacer clic. Sin JS, el
   botón manda la plantilla de compras de la página (data-mensaje). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const M2_MAXIMO = 1000000;
  const ALTURA_MAXIMA = 40;
  const CANTIDAD_MAXIMA = 100000;
  const FILAS_MAXIMAS = 8;

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const formatoM2 = (x) => x.toLocaleString('es-MX', { maximumFractionDigits: 1 });
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;
  const hueco = (v) => String(v == null ? '' : v).trim() || '___';

  // "1,200" y "1200" son 1200; "12,5" es 12.5; "800 m²" es 800. 0 si no es un número mayor que 0 y hasta M2_MAXIMO.
  function leerM2(texto) {
    let t = String(texto == null ? '' : texto).replace(/\s|m²|m2/gi, '');
    t = /^\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(t) ? t.replace(/,/g, '') : t.replace(',', '.');
    if (!/^\d+(?:\.\d+)?$/.test(t)) return 0;
    const n = Number(t);
    return n > 0 && n <= M2_MAXIMO ? n : 0;
  }

  function textosVolumen(r, campos) {
    const desde = r.desde ? 'desde ' : '';
    const m2 = formatoM2(r.m2);
    const mensaje = [`Hola, quiero cotizar ${r.texto} para un proyecto.`, `m² totales: ${m2} m²`,
      `Estimado de la web: ${desde}${dinero(r.total)} con IVA (${desde}$${r.precio}/m²)`,
      `Empresa: ${hueco(campos.empresa)}`, `Obra y ubicación: ${hueco(campos.obra)}`,
      `Fecha de la primera entrega: ${hueco(campos.fecha)}`].join('\n');
    return { medida: `${m2} m²`, monto: dinero(r.total),
      calc: `${m2} m² × ${desde}$${r.precio}/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.`,
      mensaje };
  }

  function leerAltura(texto) {
    const m = /^\s*(\d+(?:[.,]\d+)?)/.exec(String(texto == null ? '' : texto));
    const n = m ? Math.round(Number(m[1].replace(',', '.')) * 10) / 10 : 0;
    return n > 0 && n <= ALTURA_MAXIMA ? n : 0;
  }

  function leerCantidad(texto) {
    const m = /^\s*(\d+)/.exec(String(texto == null ? '' : texto));
    const n = m ? Number(m[1]) : 0;
    return n > 0 && n <= CANTIDAD_MAXIMA ? n : 0;
  }

  // fila: [especie, altura, cantidad] tal como los escribió el visitante.
  function lineaPalma(fila) {
    const especie = String(fila[0] == null ? '' : fila[0]).trim();
    if (!especie) return '';
    const n = leerCantidad(fila[2]);
    const alto = leerAltura(fila[1]);
    return `- ${n || '___'} × ${especie}, altura aprox.: ${alto ? formatoM2(alto) + ' m' : '___'}`;
  }

  function mensajePalmas(filas, campos) {
    const lineas = filas.map(lineaPalma).filter(Boolean);
    if (!lineas.length) return '';
    return ['Hola, quiero cotizar palmas para un proyecto.', ...lineas, `Empresa: ${hueco(campos.empresa)}`,
      `Obra y ubicación: ${hueco(campos.obra)}`, `Fecha de entrega: ${hueco(campos.fecha)}`].join('\n');
  }

  function resumenPalmas(filas) {
    const conEspecie = filas.filter((f) => String(f[0] == null ? '' : f[0]).trim());
    if (!conEspecie.length) return 'Elige especie y cantidad';
    const n = conEspecie.length;
    const piezas = conEspecie.reduce((suma, f) => suma + leerCantidad(f[2]), 0);
    const especies = `${n} ${n === 1 ? 'especie' : 'especies'}`;
    return piezas ? `${especies} · ${piezas.toLocaleString('es-MX')} piezas` : `${especies} · cantidad por definir`;
  }

  function camposObra(caja) {
    const valor = (n) => caja.querySelector(`[data-vt-campo="${n}"]`).value;
    return { empresa: valor('empresa'), obra: valor('obra'), fecha: valor('fecha') };
  }

  function iniciarVolumen(caja, calcular) {
    const modos = JSON.parse(caja.dataset.modos);
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    const vacio = { medida: salida('m2').textContent, monto: salida('monto').textContent, calc: salida('calc').textContent };
    function actualizar() {
      const m2 = leerM2(caja.querySelector('[data-vt-campo="m2"]').value);
      const precio = salida('monto').parentElement;
      if (!m2) {
        salida('m2').textContent = vacio.medida;
        salida('rotulo').textContent = modos.mayoreo.rotulo;
        salida('monto').textContent = vacio.monto;
        precio.classList.add('is-vacio');
        salida('calc').textContent = vacio.calc;
        salida('aviso').textContent = '';
        salida('aviso').hidden = true;
        salida('cta').setAttribute('href', enlace(caja.dataset.wa, caja.dataset.mensaje));
        return;
      }
      const r = calcular(m2, 1, 'mayoreo', modos);
      const t = textosVolumen(r, camposObra(caja));
      salida('m2').textContent = t.medida;
      salida('rotulo').textContent = r.rotulo;
      salida('monto').textContent = t.monto;
      precio.classList.remove('is-vacio');
      salida('calc').textContent = t.calc;
      salida('aviso').textContent = r.aviso;
      salida('aviso').hidden = !r.aviso;
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    actualizar();
  }

  function iniciarPalmas(caja) {
    const lista = caja.querySelector('[data-vt-filas]');
    const agregar = caja.querySelector('[data-vt-agregar]');
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    function filas() {
      return Array.from(lista.querySelectorAll('[data-vt-fila]')).map((f) =>
        ['especie', 'altura', 'cantidad'].map((n) => f.querySelector(`[data-vt-campo="${n}"]`).value));
    }
    function actualizar() {
      const f = filas();
      const mensaje = mensajePalmas(f, camposObra(caja));
      salida('resumen').textContent = resumenPalmas(f);
      salida('lista').textContent = f.map(lineaPalma).filter(Boolean).join('\n');
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, mensaje || caja.dataset.mensaje));
    }
    // Copia del último renglón, vacía y con ids nuevos (cada label sigue apuntando a su control).
    function otraFila() {
      const renglones = lista.querySelectorAll('[data-vt-fila]');
      const nueva = renglones[renglones.length - 1].cloneNode(true);
      const n = renglones.length + 1;
      nueva.querySelectorAll('[id]').forEach((el) => { el.id = el.id.replace(/\d+$/, String(n)); });
      nueva.querySelectorAll('label[for]').forEach((el) => { el.htmlFor = el.htmlFor.replace(/\d+$/, String(n)); });
      nueva.querySelectorAll('input, select').forEach((el) => { el.value = ''; });
      lista.appendChild(nueva);
      agregar.hidden = n >= FILAS_MAXIMAS;
      nueva.querySelector('select').focus();
    }
    agregar.hidden = false;
    agregar.addEventListener('click', otraFila);
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { leerM2, textosVolumen, leerAltura, leerCantidad, lineaPalma, mensajePalmas, resumenPalmas, enlace };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTB2B = Object.freeze(api);
  const arrancar = () => {
    if (root.VTMedidor) document.querySelectorAll('[data-vt-volumen]').forEach((c) => iniciarVolumen(c, root.VTMedidor.calcular));
    document.querySelectorAll('[data-vt-palmas]').forEach(iniciarPalmas);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
EOF
```

- [ ] **Step 4: Pruebas y build**

```bash
cd ~/dev/viverosterra-e2d
(cd tools/site && python3 -m unittest tests.test_componentes tests.test_b2b_paridad tests.test_medidor_paridad tests.test_reglas 2>&1 | tail -1)
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 tools/site/build.py | tail -2
```

Expected: `OK`; `ℹ pass 47` y `ℹ fail 0`; `plantillas: 0 de 28 páginas escritas` y `shell: 0 de 108 páginas actualizadas` (ninguna página usa todavía los componentes nuevos).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/componentes.py tools/site/tests/test_componentes.py tools/site/tests/test_b2b_paridad.py public/js/vt-b2b.js public/js/tests/casos-b2b.json public/js/tests/vt-b2b.test.js
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(empresas): cotizador de pasto por volumen y armador de palmas con paridad Python–JS" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Estilos de los cotizadores de empresas

**Files:**
- Modify: `public/css/terra.css`; regenerados `public/css/terra.<hash>.css`, `tools/site/activos.json` y el `<head>` de las páginas
- Test: `tools/site/tests/test_terra_css.py`

Reutiliza `.vt-campo`, `.vt-control`, `.vt-etiqueta`, `.vt-medidor__calc` y `.vt-medidor__aviso` del Medidor. Lo nuevo: la rejilla `.vt-b2b` (una columna; desde 1024 px formulario 7fr y etiqueta 5fr), los renglones del armador (especie a lo ancho y altura y cantidad en dos columnas en celular; tres columnas desde 640 px), `.vt-control select` con el mismo control que los campos y `.vt-b2b [hidden]{display:none}`: sin esa regla, `display:inline-flex` de `.vt-btn` le gana al atributo `hidden` y "Agregar otra especie" se ve sin JS (lo encontró la prueba de navegador del prototipo).

- [ ] **Step 1: Escribir la prueba**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/tests/test_terra_css.py b/tools/site/tests/test_terra_css.py
index 7e522a8..3d2b21d 100644
--- a/tools/site/tests/test_terra_css.py
+++ b/tools/site/tests/test_terra_css.py
@@ -91,6 +91,13 @@ class TerraCssTest(unittest.TestCase):
         self.assertLess(len(gzip.compress(datos, mtime=0)), 10 * 1024)
         self.assertLess(len(datos), 48 * 1024)
 
+    def test_cotizadores_de_empresas(self):
+        """Etapa 2d: [hidden] gana a .vt-btn (el botón "Agregar otra especie" sale oculto sin JS) y el select del armador
+        de palmas usa el mismo control que los campos."""
+        self.assertIn(".vt-b2b [hidden]{display:none}", self.css)
+        self.assertIn(".vt-control select{", self.css)
+        self.assertIn("@media (min-width:1024px){.vt-b2b{grid-template-columns:7fr 5fr", self.css)
+
     def test_fuentes_referenciadas_existen(self):
         urls = re.findall(r'url\("(/fonts/[^"]+)"\)', self.css)
         self.assertEqual(len(urls), 2)
EOF
```

- [ ] **Step 2: Verla fallar**

Run: `cd tools/site && python3 -m unittest tests.test_terra_css 2>&1 | grep -E "^(FAIL|ERROR):|FAILED"`
Expected: `FAIL: test_cotizadores_de_empresas` y `FAILED (failures=1)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/public/css/terra.css b/public/css/terra.css
index 897f893..041925c 100644
--- a/public/css/terra.css
+++ b/public/css/terra.css
@@ -414,6 +414,21 @@
 .vt-medidor .vt-etiqueta-x{width:100%}
 @media (min-width:640px) and (max-width:1023px){.vt-medidor{grid-template-columns:repeat(2,minmax(0,1fr));align-items:start}.vt-medidor__form{grid-row:span 2}}
 @media (min-width:1024px){.vt-medidor{grid-template-columns:4fr 4fr 4fr;gap:32px;align-items:start}}
+/* Empresas (Etapa 2d): cotizador de pasto por volumen y armador de palmas (vt-b2b.js) */
+.vt-b2b{display:grid;gap:24px}
+.vt-b2b__form{display:grid;gap:16px;align-content:start}
+.vt-b2b__form>.vt-btn{justify-self:start}
+.vt-b2b [hidden]{display:none}
+.vt-b2b__filas{display:grid;gap:16px;margin:0;padding:0;list-style:none}
+.vt-b2b__fila{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
+.vt-b2b__fila>.vt-campo:first-child{grid-column:1/-1}
+.vt-control select{flex:1;width:100%;min-width:0;height:50px;padding:0 12px;border:0;background:transparent;font:500 16px var(--vt-font-sans);color:var(--vt-ink)}
+.vt-control select:focus{outline:none}
+.vt-b2b .vt-etiqueta-x{width:100%}
+.vt-b2b .vt-etiqueta .vt-btn{width:100%;margin-top:14px}
+.vt-pagina main .vt-b2b__msg{margin-top:8px;white-space:pre-line;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
+@media (min-width:640px){.vt-b2b__fila{grid-template-columns:minmax(0,2fr) minmax(0,1fr) minmax(0,1fr)}.vt-b2b__fila>.vt-campo:first-child{grid-column:auto}}
+@media (min-width:1024px){.vt-b2b{grid-template-columns:7fr 5fr;gap:48px;align-items:start}}
 
 /* ---------- precios con columna Unidad y mensualidades ---------- */
 .vt-tabla{width:100%;border-collapse:collapse;border:1px solid var(--vt-line);background:var(--vt-card)}
EOF
```

- [ ] **Step 4: Build, presupuesto y pruebas**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
git diff --quiet -- public/sitemap.xml || git diff -U0 public/sitemap.xml | grep -q '^[-+][^-+].*lastmod' && git checkout -- public/sitemap.xml
python3 -c "import gzip,sys;sys.path.insert(0,'tools/site');import activos;m=activos.minificar_css(open('public/css/terra.css').read()).encode();print(len(m),len(gzip.compress(m,mtime=0)))"
(cd tools/site && python3 -m unittest tests.test_terra_css tests.test_activos tests.test_shell tests.test_generar 2>&1 | tail -1)
```

Expected: `plantillas: 28 de 28 páginas escritas` y `shell: 73 de 108 páginas actualizadas` (el hash nuevo en el `<head>`), luego `0 de 28` y `0 de 108`; el `status` muestra `D public/css/terra.cbf51c7c5a.css`, `M public/css/terra.css`, `M tools/site/activos.json`, `M tools/site/tests/test_terra_css.py` y `?? public/css/terra.c4ecf9ebca.css`; `45411 8737`; `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add public tools/site/activos.json tools/site/tests/test_terra_css.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "style(empresas): cotizador por volumen y armador de palmas en terra.css" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Plantilla `b2b` y mayoreo de pasto

**Files:**
- Create: `tools/site/plantillas/b2b.py`, `tools/site/contenido/b2b_comun.py`, `tools/site/contenido/mayoreo_pasto.py`, `tools/site/tests/test_b2b.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `public/mayoreo-pasto-tampico/index.html` (regenerado)
- Test: `tools/site/tests/test_generar.py`, `tools/site/tests/test_consistencia.py`, `tools/servicios/tests/test_pagos.py`

Contenido de mayoreo, todo de `datos.py`: portada con la respuesta directa ("En Viveros Terra el pasto San Agustín al mayoreo cuesta desde $60/m² (solo pasto) en pedidos de 500 m² o más…") y la etiqueta "Mayoreo · desde $60/m²" con "Pedido mínimo 500 m²" y "Con menos de 500 m² · $85/m² solo pasto"; clientes con logo (BMW, Taghleef, Gobierno de Tampico, Grupo Velas, Velamar, Flex) y Renault en texto, REPSE verificable, 3 fotos `FIG.` reales del sitio, una nota de campo honesta (con menos de 500 m² conviene pasto en rollo) y la opinión real de la Arq. Patricia L. (constructora, Altamira); tabla de escalas (menos de 500 m² · $85; 500 m² o más · desde $60; instalado en obra · según cotización; capacidad y calendario · por escrito en tu cotización, con `datos.LLEGADA_PASTO`) y el cotizador por volumen; documentación; 3 paquetes (solo pasto desde $60/m², instalado en obra según cotización, pasto + palmas + riego según cotización), cada uno con su mensaje; proceso de 5 pasos con anticipo y entregas por etapas; garantía de arraigo solo cuando instala la cuadrilla de Viveros Terra (en mayoreo solo pasto no aplica y se dice); 8 preguntas de compras (las 4 de `main` y capacidad por entrega, instalación en obra, cómo se paga y REPSE). Se retiran "entrega con grúa" (no está en `datos.py`; pregunta al dueño 6) y el bloque de autor (Etapa 4). `test_b2b.py` nace con `RUTAS = {"mayoreo": …}`; la Tarea 7 le agrega palmas.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/servicios/tests/test_pagos.py b/tools/servicios/tests/test_pagos.py
index f8233d2..a9c1770 100644
--- a/tools/servicios/tests/test_pagos.py
+++ b/tools/servicios/tests/test_pagos.py
@@ -1,4 +1,4 @@
-"""tools/servicios ya no toca las páginas que salen de tools/site/plantillas/ (Etapas 2a y 2c)."""
+"""tools/servicios ya no toca las páginas que salen de tools/site/plantillas/ (Etapas 2a, 2c y 2d)."""
 import sys
 import unittest
 from pathlib import Path
@@ -9,7 +9,7 @@ import hero  # noqa: E402
 from pages import PAGES  # noqa: E402
 
 CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico", "mantenimiento-jardines-tampico",
-                 "sistema-riego-tampico")
+                 "sistema-riego-tampico", "mayoreo-pasto-tampico")
 
 
 class PaginasConPlantillaTest(unittest.TestCase):
@@ -19,7 +19,7 @@ class PaginasConPlantillaTest(unittest.TestCase):
                 self.assertNotIn(slug, PAGES)
 
     def test_la_portada_ya_no_lleva_linea_de_pago_ni_ancla_al_simulador_viejo(self):
-        cfg = dict(PAGES["mayoreo-pasto-tampico"], img=None)
+        cfg = dict(PAGES["vivero-tampico"], img=None)
         html = hero.hero_html(cfg)
         self.assertNotIn("svc-hero__pay", html)
         self.assertNotIn("#sim-titulo", html)
diff --git a/tools/site/tests/test_consistencia.py b/tools/site/tests/test_consistencia.py
index 513ad93..d9ab5a1 100644
--- a/tools/site/tests/test_consistencia.py
+++ b/tools/site/tests/test_consistencia.py
@@ -202,9 +202,10 @@ class ConsistenciaTest(unittest.TestCase):
         self.assertIn("Recibes el precio del pasto, la entrega y la instalación por separado.",
                       TEXTOS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"])
         self.assertEqual(TEXTOS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"].count("Cortado para tu pedido"), 2)
-        palmas = TEXTOS[PUBLIC / "palmas-mayoreo-proyectos" / "index.html"]
-        self.assertEqual(palmas.count("Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contra "
-                                      "avances de obra; te lo detallamos en la cotización."), 2)
+        # Etapa 2d: la misma frase del dueño en las dos páginas para empresas, en el FAQ visible y en su FAQPage.
+        for pagina in ("mayoreo-pasto-tampico", "palmas-mayoreo-proyectos"):
+            with self.subTest(pagina=pagina):
+                self.assertEqual(TEXTOS[PUBLIC / pagina / "index.html"].count(datos.ANTICIPO_PROYECTOS), 2)
 
     def test_same_as_igual_a_redes_oficiales(self):
         oficiales = {url for _, url in datos.REDES}
diff --git a/tools/site/tests/test_generar.py b/tools/site/tests/test_generar.py
index 38467cc..82574b8 100644
--- a/tools/site/tests/test_generar.py
+++ b/tools/site/tests/test_generar.py
@@ -18,7 +18,8 @@ import shell  # noqa: E402
 class GenerarTest(unittest.TestCase):
     def test_paginas_registradas_tienen_contexto(self):
         esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
-                      "/mantenimiento-jardines-tampico", "/sistema-riego-tampico", "/pasto-sintetico",
+                      "/mantenimiento-jardines-tampico", "/sistema-riego-tampico", "/mayoreo-pasto-tampico",
+                      "/pasto-sintetico",
                       "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                      + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
         self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
EOF
cat > tools/site/tests/test_b2b.py <<'EOF'
"""Mayoreo de pasto y palmas para proyectos salen de la plantilla b2b (Etapa 2d): secuencia del spec §3.3, clientes con
nombre y REPSE verificable, un mensaje de compras por paquete, precios de datos.py (mayoreo nunca a $60 con menos de
500 m²; palmas con los precios del dueño y el resto según cotización), anticipo sin porcentaje ni crédito, cotizadores
con su JS y JSON-LD de lo visible. /empresas es de la Etapa 3: mientras tanto nadie la enlaza."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

P = datos.PRECIOS
# Cada página migrada agrega su fila aquí y en SCRIPTS (palmas llega en la tarea siguiente).
RUTAS = {"mayoreo": "/mayoreo-pasto-tampico"}
SCRIPTS = {"mayoreo": ["/js/vt-medidor.js", "/js/vt-b2b.js"]}


def pagina(clave):
    html = (paginas.PUBLIC / RUTAS[clave].strip("/") / "index.html").read_text(encoding="utf-8")
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
    return html, main, textos_publicos(html), grafo


def mensajes_de(html, patron):
    return [unquote(t) for t in re.findall(rf'data-cta="{patron}" href="https://wa\.me/\d+\?text=([^"]+)"', html)]


class ComunTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        orden = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', 'data-cta="b2b:hero"', 'id="vt-h-prueba"',
                 'class="vt-logos"', "padrón público de la STPS", 'id="vt-h-precio"', "data-hero-cta data-wa",
                 'id="vt-h-docs"', 'id="vt-h-opciones"', 'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-faq"',
                 'id="vt-h-cobertura"', 'id="vt-h-rel"', 'class="vt-cierre"')
        for clave in RUTAS:
            _h, main, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                posiciones = [main.index(m) for m in orden]
                self.assertEqual(posiciones, sorted(posiciones))
                self.assertEqual(len(re.findall(r"<h1\b", main)), 1)
                self.assertEqual(main.count('class="vt-pasos"'), 1)

    def test_sin_css_viejo_formularios_ni_parches_de_servicios(self):
        for clave in RUTAS:
            html, _m, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertNotRegex(html, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
                for viejo in ("svc-hero", "<form", "<style", "cta-submit", "calc-cta", "window.open", "Sección 1",
                              "sticky-cta", "faq-btn"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_scripts_del_cotizador_en_orden(self):
        for clave, esperados in SCRIPTS.items():
            html, _m, _t, _g = pagina(clave)
            propios = [s for s in re.findall(r'<script src="([^"]+)" defer></script>', html) if "/terra." not in s]
            with self.subTest(pagina=clave):
                self.assertEqual(propios, esperados)

    def test_clientes_con_nombre_y_repse_verificable(self):
        for clave in RUTAS:
            _h, main, _t, _g = pagina(clave)
            prueba = main[main.index('id="vt-h-prueba"'):main.index('id="vt-h-precio"')]
            with self.subTest(pagina=clave):
                for cliente in datos.CLIENTES_B2B:
                    self.assertRegex(prueba, rf'alt="{re.escape(cliente)}"|>{re.escape(cliente)}</li>')
                self.assertIn(f'REPSE {datos.REPSE} · <a href="{datos.REPSE_PADRON}"', prueba)

    def test_portada_cierre_y_shell_con_la_plantilla_de_compras(self):
        for clave, ruta in RUTAS.items():
            html, _m, _t, _g = pagina(clave)
            esperado = datos.con_firma(mensajes_paginas.EMPRESAS[ruta])
            with self.subTest(pagina=clave):
                for seccion in ("hero", "cierre", "barra", "footer"):
                    self.assertEqual(set(mensajes_de(html, f"b2b:{seccion}")), {esperado}, seccion)

    def test_tres_paquetes_cada_uno_con_su_mensaje(self):
        for clave in RUTAS:
            html, _m, _t, _g = pagina(clave)
            mensajes = [mensajes_de(html, f"b2b:opcion-{i}") for i in (1, 2, 3)]
            with self.subTest(pagina=clave):
                self.assertTrue(all(len(m) == 1 for m in mensajes))
                planos = [m[0] for m in mensajes]
                self.assertEqual(len(set(planos)), 3)
                for m in planos:
                    self.assertIn("Empresa", m)
                    self.assertTrue(m.endswith(datos.FIRMA))
                self.assertEqual(mensajes_de(html, "b2b:opcion-4"), [])

    def test_anticipo_sin_porcentaje_ni_credito(self):
        for clave in RUTAS:
            _h, _m, texto, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertEqual(texto.count(datos.ANTICIPO_PROYECTOS), 2)  # FAQ visible y FAQPage
                self.assertNotRegex(texto, r"(?i)pago diferido|a crédito|\d+ ?% de anticipo")

    def test_empresas_todavia_sin_enlace(self):
        """/empresas es de la Etapa 3 (spec §3.5): hasta entonces ninguna página la enlaza."""
        for path in paginas.PUBLIC.rglob("*.html"):
            with self.subTest(pagina=str(path.relative_to(paginas.PUBLIC))):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r'href="/empresas(?:[/"#?])')

    def test_las_paginas_para_empresas_se_enlazan_entre_si(self):
        for clave, ruta in RUTAS.items():
            _h, main, _t, _g = pagina(clave)
            rel = main[main.index('id="vt-h-rel"'):main.index('class="vt-cierre"')]
            otros = [r for r in RUTAS.values() if r != ruta]
            with self.subTest(pagina=clave):
                for destino in otros + ["/mantenimiento-jardines-tampico", "/sistema-riego-tampico"]:
                    self.assertIn(f'href="{destino}"', rel)
                self.assertNotIn(f'href="{ruta}"', rel)

    def test_faq_y_json_ld_dicen_lo_mismo(self):
        for clave in RUTAS:
            _h, main, _t, grafo = pagina(clave)
            visibles = [re.sub(r"<[^>]+>", "", q) for q in re.findall(r"<summary>(.*?)</summary>", main)]
            faq = next(n for n in grafo if n["@type"] == "FAQPage")
            with self.subTest(pagina=clave):
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)
                self.assertGreaterEqual(len(visibles), 8)


class MayoreoTest(unittest.TestCase):
    def test_precio_y_minimo_de_datos(self):
        _h, main, texto, _g = pagina("mayoreo")
        portada = main[:main.index('id="vt-h-prueba"')]
        self.assertIn(f"<b>${P['pasto_mayoreo_m2']}</b>", portada)
        self.assertIn(f"{P['pasto_mayoreo_minimo_m2']} m²", portada)
        self.assertIn(f"a partir de {P['pasto_mayoreo_minimo_m2']} m²", texto)

    def test_con_menos_de_500_m2_nunca_a_60(self):
        _h, main, texto, _g = pagina("mayoreo")
        minimo, mayoreo, solo = P["pasto_mayoreo_minimo_m2"], P["pasto_mayoreo_m2"], P["pasto_solo_m2"]
        fila = re.search(rf'<th scope="row">Menos de {minimo} m²</th>(.*?)</tr>', main).group(1)
        self.assertIn(f"${solo}", fila)
        self.assertNotIn(f"${mayoreo}", fila)
        self.assertNotRegex(texto, rf"(?:menos de|bajo) {minimo} m²[^.]{{0,40}}\${mayoreo}\b")
        self.assertIn(f'&quot;minimo&quot;:{minimo}', main)

    def test_opinion_real_de_una_constructora(self):
        _h, main, _t, _g = pagina("mayoreo")
        cita, nombre, detalle = datos.OPINIONES_PASTO_EN_ROLLO[1]
        self.assertIn(f"<p>“{cita}”</p>", main)
        self.assertIn(f"<b>{nombre}</b><span>{detalle}</span>", main)

    def test_json_ld_como_estaba_publicado(self):
        _h, _m, _t, grafo = pagina("mayoreo")
        self.assertEqual([n["@type"] for n in grafo], ["Service", "FAQPage", "BreadcrumbList", "SpeakableSpecification"])
        self.assertEqual(grafo[0]["provider"]["address"]["streetAddress"], datos.CALLE)


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_b2b tests.test_generar 2>&1 | tail -1`
Expected: `FAILED (failures=8, errors=5)` (la página sigue siendo la de `main`).
Run: `cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^FAIL:|FAILED"`
Expected: `FAIL: test_paginas_con_plantilla_fuera_de_los_parches … (slug='mayoreo-pasto-tampico')` y `FAILED (failures=1)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
cat > tools/site/plantillas/b2b.py <<'EOF'
"""Plantilla para empresas (spec §3.3, B2B): ruta visible → H1 por segmento con el precio por volumen y su mínimo en la
etiqueta → CTA con la plantilla de compras y la promesa → clientes con nombre y logo, REPSE verificable y fotos FIG. →
escalas, capacidad y tiempos con su cotizador (pasto por volumen o armador de palmas) → documentación (CFDI, REPSE,
anticipo y avances, entregas) → paquetes por obra (máx. 3, cada uno con su mensaje) → proceso NOSOTROS / TÚ → garantía
con condiciones → preguntas de compras → cobertura → otras páginas para empresas → CTA final. Sin ficha descargable:
no hay un PDF real (spec §3.3). Páginas: /mayoreo-pasto-tampico (contenido/mayoreo_pasto.py) y
/palmas-mayoreo-proyectos (contenido/palmas_proyectos.py); la página /empresas de la Etapa 3 reutiliza
contenido/b2b_comun.py."""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"
COTIZADORES = {"volumen": c.cotizador_volumen, "palmas": c.armador_palmas}
# vt-b2b.js calcula el volumen con VTMedidor.calcular: vt-medidor.js va antes (sin [data-vt-medidor] no hace nada más).
SCRIPTS = {"volumen": ("/js/vt-medidor.js", "/js/vt-b2b.js"), "palmas": ("/js/vt-b2b.js",)}


def _prueba(k, numero):
    pr = k["prueba"]
    cuerpo = c.logos() + c.repse() + c.obras(pr["figuras"], c.nota(*pr["nota"]))
    if pr.get("opiniones"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_opinion"]}</h3>' + c.testimonios(pr["opiniones"])
    return c.bloque(numero, "Clientes", "vt-h-prueba", pr["titulo"], cuerpo, lede=pr["lede"])


def _escalas(k, numero):
    e = k["escalas"]
    cotizador = COTIZADORES[e["cotizador"]](k["prefijo"], k["tipo"], k["portada"]["mensaje"])
    cuerpo = (c.tabla_comparativa(e["columnas"], e["filas"], e["caption"])
              + f'<h3 class="vt-mt">{e["titulo_cotizador"]}</h3>{cotizador}')
    return c.bloque(numero, "Precio por volumen", "vt-h-precio", e["titulo"], cuerpo, lede=e["lede"], tinte=True,
                    id_seccion="precio")


def _documentacion(k, numero):
    d = k["documentacion"]
    return c.bloque(numero, "Documentación", "vt-h-docs", d["titulo"], c.fichas(d["items"]), lede=d.get("lede"),
                    id_seccion="documentacion")


def _paquetes(k, numero):
    p = k["paquetes"]
    cuerpo = c.opciones(p["items"], k["tipo"]) + (f'<p class="vt-promesa">{p["nota"]}</p>' if p.get("nota") else "")
    return c.bloque(numero, "Paquetes por obra", "vt-h-opciones", p["titulo"], cuerpo, lede=p.get("lede"),
                    id_seccion="paquetes")


def _cobertura(k, numero):
    co = k["cobertura"]
    return c.bloque(numero, "Cobertura", "vt-h-cobertura", co["titulo"],
                    c.cobertura(co["zonas"], co["por_proyecto"], co.get("sectores", ())), lede=co["lede"])


def render(k):
    tipo = k["tipo"]
    p, g, f, r, ci = k["proceso"], k["garantia"], k["faq"], k["relacionados"], k["cierre"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), _prueba(k, 1), _escalas(k, 2), _documentacion(k, 3),
                 _paquetes(k, 4),
                 c.bloque(5, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]),
                 c.garantia(dict(g, numero=6, id_titulo="vt-h-garantia", rotulo="Garantía")),
                 c.bloque_dos(7, "Preguntas de compras", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True),
                 _cobertura(k, 8),
                 c.bloque(9, "Para empresas", "vt-h-rel", r["titulo"], c.relacionados(r["items"]), tinte=True),
                 c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo)]
    j = k["jsonld"]
    speakable = [{"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    grafo = [j["producto"], *j.get("nodos", ()), c.faq_jsonld(f["preguntas"]), j["migas"], *speakable]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          scripts=SCRIPTS[k["escalas"]["cotizador"]])
EOF
cat > tools/site/contenido/b2b_comun.py <<'EOF'
"""Piezas comunes de las páginas para empresas (Etapa 2d): documentación para compras, dos preguntas de compras, los
sectores, la cobertura y las páginas B2B que se enlazan entre sí. Las usan contenido/mayoreo_pasto.py y
contenido/palmas_proyectos.py; la página /empresas de la Etapa 3 (spec §3.1 y §3.5) tomará de aquí su índice
(PAGINAS) sin repetir textos. Mientras /empresas no exista, ninguna página la enlaza (test_b2b.py lo prueba).
Solo datos de datos.py: ninguna escala, capacidad ni plazo que el dueño no haya dado."""
import datos
from componentes import dinero

P = datos.PRECIOS
OBRA = "/img/obra"
MINIMO = P["pasto_mayoreo_minimo_m2"]
PADRON = f'<a href="{datos.REPSE_PADRON}" target="_blank" rel="noopener">padrón público de la STPS</a>'

DOCUMENTACION = (
    {"titulo": f"Factura {datos.FACTURA}",
     "texto": "Para persona física o moral, emitida el día del pago. Solo necesitamos tu RFC y tus datos fiscales."},
    {"titulo": f"REPSE {datos.REPSE}",
     "texto": f"Registro de la STPS para prestar servicios especializados a empresas. Consulta el folio en el {PADRON}."},
    {"titulo": "Anticipo y avances de obra",
     "texto": ("Confirmas con un anticipo; los pagos siguientes se acuerdan contra avances de obra y quedan por escrito "
               "en la cotización.")},
    {"titulo": "Entregas por etapas",
     "texto": "Un pedido global con entregas parciales en las fechas que tu obra necesita, para que cada entrega llegue fresca."},
)
PREGUNTA_PAGO = ("¿Cómo se paga un proyecto?",
                 f"{datos.ANTICIPO_PROYECTOS} Cada pago lleva su factura {datos.FACTURA}.")
PREGUNTA_REPSE = ("¿Están dados de alta en el REPSE?",
                  f"Sí: REPSE {datos.REPSE}, el registro de la STPS para prestar servicios especializados a empresas. "
                  f"Puedes consultar el folio en el {PADRON}.")
SECTORES = (
    ("Constructoras y desarrolladoras", "Fraccionamientos, vivienda y casa muestra"),
    ("Arquitectos y paisajistas", "Proyectos con especificación"),
    ("Hoteles y comercios", "Áreas verdes de imagen"),
    ("Industria", "Parques industriales y áreas perimetrales"),
    ("Gobierno", "Parques y áreas públicas"),
)
COBERTURA = {
    "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
}
PAGINAS = (
    {"titulo": "Mayoreo de pasto", "href": "/mayoreo-pasto-tampico",
     "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
     "texto": f"San Agustín desde {dinero(P['pasto_mayoreo_m2'])}/m² en pedidos de {MINIMO} m² o más · entregas por etapas"},
    {"titulo": "Palmas para proyectos", "href": "/palmas-mayoreo-proyectos",
     "img": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961,
     "texto": (f"Areca y coco plumoso desde {dinero(P['palma_desde'])} y palma real desde {dinero(P['palma_real'])} en "
               "tamaño chico")},
    {"titulo": "Mantenimiento de áreas verdes", "href": "/mantenimiento-jardines-tampico",
     "img": f"{OBRA}/mantenimiento-areas-verdes-empresa.webp", "ancho": 640, "alto": 961,
     "texto": f"Empresas, fraccionamientos e industria · REPSE {datos.REPSE} y factura {datos.FACTURA}"},
    {"titulo": "Riego para grandes áreas", "href": "/sistema-riego-tampico",
     "img": f"{OBRA}/riego-tecnico-sistema-industrial.webp", "ancho": 960, "alto": 640,
     "texto": "Parques industriales, escuelas y campos deportivos con pasto natural"},
)


def relacionados(excepto):
    """Las otras páginas para empresas (la propia no se enlaza)."""
    return tuple(p for p in PAGINAS if p["href"] != excepto)
EOF
cat > tools/site/contenido/mayoreo_pasto.py <<'EOF'
"""Contenido de /mayoreo-pasto-tampico (pasto San Agustín al mayoreo para obras). Solo datos: la plantilla es
tools/site/plantillas/b2b.py, con el cotizador de pasto por volumen (componentes.cotizador_volumen: la regla del
Medidor, así que con menos de 500 m² nunca sale a $60), clientes con nombre y logo, REPSE verificable, la opinión real
de una constructora (datos.OPINIONES_PASTO_EN_ROLLO, con permiso del dueño) y 3 paquetes con su mensaje.

Precios de datos.PRECIOS ($60 desde 500 m², $85 solo pasto, desde $120 instalado). La capacidad por entrega y los plazos
no están en datos.py: la tabla dice que van por escrito en la cotización (hoja de ruta 2d: el dueño los da o no se
publican). Título, canonical, robots, Open Graph, Service y migas como estaban publicados; la descripción y su
og:description corrigen el "Factura CFDI, factura CFDI" repetido (PARIDAD["meta"]). FAQPage de las preguntas visibles.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import b2b_comun

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/mayoreo-pasto-tampico"
URL = f"{SITE}{RUTA}"
OBRA = "/img/obra"
MAYOREO, MINIMO, SOLO, INSTALADO = (P["pasto_mayoreo_m2"], P["pasto_mayoreo_minimo_m2"], P["pasto_solo_m2"],
                                    P["pasto_instalado_m2"])
MENSAJE = mensajes_paginas.EMPRESAS[RUTA]
DESCRIPCION = (f"Pasto San Agustín en rollo al mayoreo desde ${MAYOREO}/m² en pedidos de {MINIMO} m² o más, para "
               f"constructoras y proyectos en Tampico. Factura {datos.FACTURA} y entrega por etapas. Viveros Terra, desde "
               f"{datos.DESDE}.")
DESCRIPCION_OG = (f"Pasto San Agustín en rollo al mayoreo desde ${MAYOREO}/m² en pedidos de {MINIMO} m² o más, para "
                  f"constructoras y proyectos en Tampico. Factura {datos.FACTURA} y entrega por etapas.")

META = {
    "title": f"Pasto al mayoreo en Tampico desde ${MAYOREO}/m² para constructoras · Viveros Terra",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Pasto al Mayoreo en Tampico para Constructoras · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/pasto-en-rollo-san-agustin-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}
SERVICIO = {
    "@type": "Service", "serviceType": "Suministro de Pasto al Mayoreo",
    "name": "Pasto al Mayoreo en Tampico para Constructoras",
    "description": ("Suministro de pasto San Agustín en rollo al mayoreo para constructoras, arquitectos, fraccionamientos, "
                    "hoteles y empresas en Tampico, Ciudad Madero y Altamira. Precio preferencial por volumen, factura "
                    "CFDI 4.0 y entrega por etapas según avance de obra."),
    "provider": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
                 "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                             "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}},
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Pasto en Rollo Tampico", "item": f"{SITE}/pasto-en-rollo-tampico"},
    {"@type": "ListItem", "position": 3, "name": "Mayoreo Pasto Tampico", "item": URL},
]}

PREGUNTAS = (
    ("¿Cuál es el pedido mínimo para mayoreo de pasto en Tampico?",
     f"Para precios de mayoreo manejamos pedidos a partir de {MINIMO} m²: desde {dinero(MAYOREO)}/m² solo pasto, con IVA. "
     f"Con menos de {MINIMO} m² también te atendemos, a {dinero(SOLO)}/m² solo pasto o desde {dinero(INSTALADO)}/m² "
     'instalado (<a href="/pasto-en-rollo-tampico">pasto en rollo</a>).'),
    ("¿Facturan CFDI para constructoras?",
     f"Sí, emitimos factura {datos.FACTURA} para constructoras, empresas y cualquier cliente que requiera comprobante "
     "fiscal, el día del pago. Solo necesitamos tu RFC y datos fiscales al momento de la compra."),
    ("¿Pueden entregar pasto fuera de Tampico?",
     f"Sí. Además de Tampico, Ciudad Madero y Altamira, atendemos proyectos en {datos.ZONAS_POR_PROYECTO}. Para "
     "proyectos fuera del área metropolitana cotizamos el flete por separado según la distancia y el volumen."),
    ("¿Cómo funciona la entrega por etapas para obras?",
     "Coordinamos la entrega de pasto según el avance de tu obra. Puedes hacer un pedido global y programar las entregas "
     "parciales en las fechas que necesitas, para que cada etapa reciba pasto fresco. Esto evita que el material se "
     "dañe si no se instala de inmediato."),
    ("¿Cuánto pasto pueden surtir por entrega?",
     "Depende de tu calendario: el volumen de cada entrega y sus fechas van por escrito en la cotización, antes de que "
     f"confirmes. El pasto llega del campo {datos.LLEGADA_PASTO} y se corta para tu pedido."),
    ("¿También instalan el pasto en la obra?",
     "Sí, con nuestra cuadrilla. La instalación en obra se cotiza según el terreno y el volumen, e incluye la garantía de "
     f"arraigo de {datos.ARRAIGO} siguiendo el protocolo de riego. Si lo instala tu cuadrilla, te entregamos el pasto "
     "fresco y el protocolo por escrito."),
    b2b_comun.PREGUNTA_PAGO,
    b2b_comun.PREGUNTA_REPSE,
)

PASOS = (
    {"titulo": "Contáctanos por WhatsApp", "quien": "tu", "cuando": "Para empezar",
     "texto": ("Cuéntanos tu proyecto: superficie en m², ubicación de la obra y fecha de inicio de la instalación. Si "
               "tienes plano, mándalo.")},
    {"titulo": "Cotización por escrito", "quien": "nosotros", "cuando": "Al revisar tu proyecto",
     "texto": "Te enviamos precio por m², costo total, condiciones de pago y el calendario de entregas por etapas."},
    {"titulo": "Anticipo y calendario", "quien": "juntos", "cuando": "Al confirmar",
     "texto": "Confirmas con un anticipo y fijamos juntos las fechas de cada entrega según el avance de la obra."},
    {"titulo": "Entregas por etapas", "quien": "nosotros", "cuando": "En cada etapa",
     "texto": f"El pasto llega del campo {datos.LLEGADA_PASTO} y se corta para tu pedido: cada entrega llega fresca."},
    {"titulo": "Factura y siguiente etapa", "quien": "juntos", "cuando": "Contra avance",
     "texto": f"Cada pago lleva su factura {datos.FACTURA}; los siguientes se acuerdan contra avances de obra."},
)

FIGURAS = (
    {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 2,
     "alt": "Rollos de pasto San Agustín recién cortados en la camioneta de reparto.",
     "lugar": "Rollos recién cortados", "etapa": "En la camioneta de reparto"},
    {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp", "ancho": 640, "alto": 960, "numero": 3,
     "alt": "Cuadrilla de Viveros Terra tendiendo pasto San Agustín en rollo.", "lugar": "Cuadrilla tendiendo pasto",
     "etapa": "Instalación"},
    {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 4,
     "alt": "Pasto San Agustín recién instalado junto a un andador.", "lugar": "Después", "etapa": "Día de instalación"},
)

PAQUETES = (
    {"rotulo": "Paquete 1 · Solo pasto", "titulo": "Pasto de mayoreo para tu cuadrilla", "precio": MAYOREO,
     "unidad": "/m²", "detalle": f"en pedidos de {MINIMO} m² o más",
     "puntos": ("Pasto San Agustín cortado para tu pedido", "Entregas parciales según el avance de la obra",
                f"Factura {datos.FACTURA} el día del pago"),
     "mensaje": ("Hola, quiero cotizar pasto San Agustín al mayoreo (solo pasto).\nEmpresa: ___\nObra y ubicación: ___\n"
                 "m² totales: ___\nEntregas (fechas o etapas): ___")},
    {"rotulo": "Paquete 2 · Instalado", "titulo": "Pasto instalado en obra", "precio_texto": datos.SEGUN_COTIZACION,
     "detalle": "según el terreno y el volumen", "rec": True,
     "puntos": ("Preparación básica del terreno y colocación con nuestra cuadrilla",
                f"Garantía de arraigo de {datos.ARRAIGO} siguiendo el protocolo de riego",
                f"REPSE {datos.REPSE} para trabajar dentro de tu obra"),
     "mensaje": ("Hola, quiero cotizar pasto instalado en una obra.\nEmpresa: ___\nObra y ubicación: ___\n"
                 "m² totales: ___\nEstado del terreno (nivelado, con tierra, con escombro): ___")},
    {"rotulo": "Paquete 3 · Áreas verdes", "titulo": "Pasto, palmas y riego para la obra",
     "precio_texto": datos.SEGUN_COTIZACION, "detalle": "con un solo proveedor",
     "puntos": ('Pasto, <a href="/palmas-mayoreo-proyectos">palmas para proyectos</a> y árboles',
                '<a href="/sistema-riego-tampico">Riego automático</a> para grandes áreas',
                '<a href="/mantenimiento-jardines-tampico">Mantenimiento</a> después de la entrega'),
     "mensaje": ("Hola, quiero cotizar las áreas verdes de una obra (pasto, palmas y riego).\nEmpresa: ___\n"
                 "Obra y ubicación: ___\nm² de áreas verdes: ___\nFecha de entrega: ___")},
)

CONTENIDO = {
    "tipo": "b2b",
    "prefijo": "may",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    # /empresas llega en la Etapa 3: entonces se inserta ("Empresas", "/empresas") aquí y en MIGAS_LD.
    "migas": (("Inicio", "/"), ("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Mayoreo", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Constructoras · Fraccionamientos · Industria",
        "h1": 'Pasto al mayoreo <span class="vt-serif">para obras y fraccionamientos</span>',
        "lede": (f"En Viveros Terra el pasto San Agustín al mayoreo cuesta desde {dinero(MAYOREO)}/m² (solo pasto) en "
                 f"pedidos de {MINIMO} m² o más, con IVA y factura {datos.FACTURA}. Entregamos por etapas según el "
                 "avance de tu obra en Tampico, Madero y Altamira; fuera de la zona, por proyecto."),
        "etiqueta": {
            "codigo": "Mayoreo · 01", "aviso": "Con IVA", "nombre": "Pasto San Agustín para obra",
            "cientifico": "Stenotaphrum secundatum", "antes": "Mayoreo · desde", "monto": dinero(MAYOREO),
            "unidad": "/m²",
            "filas": (("Pedido mínimo", f"{MINIMO} m²"), (f"Con menos de {MINIMO} m²", f"{dinero(SOLO)}/m² solo pasto")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'REPSE {datos.REPSE} · factura {datos.FACTURA} · <a href="#precio">calcula tu obra por m²</a>'),
        "foto": {"src": "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp",
                 "srcset": ("/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp 560w, "
                            "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Cuadrilla instalando pasto San Agustín en rollo", "lugar": "Pasto San Agustín para obra",
                 "etapa": "Instalación"},
    },
    "prueba": {
        "titulo": "Clientes que confían en Viveros Terra",
        "lede": (f"{datos.PROYECTOS_B2B} proyectos B2B y {datos.M2_INSTALADOS} instalados en Tamaulipas y la Huasteca, "
                 f"desde {datos.DESDE}: constructoras, fraccionamientos, hoteles, industria y gobierno."),
        "figuras": FIGURAS,
        "nota": (f'Si tu obra necesita menos de {MINIMO} m², el mayoreo no aplica: te conviene el '
                 f'<a href="/pasto-en-rollo-tampico">pasto en rollo</a> a {dinero(SOLO)}/m², con el mismo pasto y la '
                 "misma entrega.", "Al cotizar"),
        "titulo_opinion": "Lo que dice una constructora",
        "opiniones": datos.OPINIONES_PASTO_EN_ROLLO[1:],
    },
    "escalas": {
        "titulo": "¿Cuánto cuesta el pasto al mayoreo?",
        "lede": (f"Desde {dinero(MAYOREO)}/m² solo pasto en pedidos de {MINIMO} m² o más; con menos, {dinero(SOLO)}/m². "
                 f"La instalación en obra, {datos.SEGUN_COTIZACION.lower()}. Precios {datos.ANIO} con IVA; lista "
                 'completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "columnas": ("Volumen", "Unidad", "Precio", "Entrega"),
        "filas": (
            (f"Menos de {MINIMO} m²", "/m²", f"{dinero(SOLO)} solo pasto", "Se cotiza según tu obra"),
            (f"{MINIMO} m² o más", "/m²", f"desde {dinero(MAYOREO)} solo pasto", "Por etapas, según el avance de obra"),
            ("Pasto instalado en obra", "/m²", datos.SEGUN_COTIZACION, "Con nuestra cuadrilla"),
            ("Capacidad y calendario", "por entrega", "Por escrito en tu cotización",
             f"El pasto llega del campo {datos.LLEGADA_PASTO}"),
        ),
        "caption": "Con IVA. El cotizador estima solo el pasto; la entrega y la instalación se cotizan con tu obra.",
        "titulo_cotizador": "Calcula tu obra por m²",
        "cotizador": "volumen",
    },
    "documentacion": {
        "titulo": "Documentación para compras",
        "lede": "Lo que piden compras, finanzas y supervisión de obra para liberar el pago.",
        "items": b2b_comun.DOCUMENTACION,
    },
    "paquetes": {
        "titulo": "Paquetes por tipo de obra",
        "lede": "Cada botón abre WhatsApp con la plantilla de ese paquete.",
        "items": PAQUETES,
        "nota": (f'¿Menos de {MINIMO} m²? <a href="/pasto-en-rollo-tampico">Pasto en rollo</a> a {dinero(SOLO)}/m² solo '
                 f"pasto o desde {dinero(INSTALADO)}/m² instalado."),
    },
    "proceso": {"titulo": "Proceso de cotización", "lede": "De tu mensaje a la última entrega, todo por escrito.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo cuando instalamos nosotros.", "grande": "15–20", "unidad": "días",
        "resumen": f"Garantía de arraigo de {datos.ARRAIGO} con instalación contratada.",
        "puntos": (
            ("Si contratas la instalación y se sigue el protocolo de riego de 20 días, garantizamos el arraigo: si una "
             f"sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo.", True),
            (f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}; cada entrega por etapas llega fresca.", True),
            ("Protocolo de riego por escrito para quien riega la obra.", True),
            ("En mayoreo solo pasto, la instalación es de tu cuadrilla: la garantía de arraigo no aplica, pero te "
             "entregamos el protocolo de riego.", False),
        ),
        "pie": ('<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a> · '
                '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de cuidados de 20 días</a>'),
    },
    "faq": {"titulo": "Preguntas de compras sobre pasto al mayoreo", "preguntas": PREGUNTAS},
    "cobertura": dict(b2b_comun.COBERTURA, titulo="Pasto para obras en Tampico, Madero, Altamira y la región.",
                      lede="Entregamos en la zona conurbada y, por proyecto, en el resto de la región; el flete se cotiza "
                           "por distancia y volumen."),
    "relacionados": {"titulo": "Otras soluciones para empresas", "items": b2b_comun.relacionados(RUTA)},
    "cierre": {
        "titulo": "¿Listo para cotizar tu obra?",
        "lede": ("Mándanos los m² totales, la ubicación y la fecha de la primera entrega. Te enviamos precio por m², "
                 "calendario y condiciones por escrito."),
        "mensaje": MENSAJE,
    },
}

PARIDAD = {
    "meta": {
        "description": (DESCRIPCION, "Corrige el “Factura CFDI, factura CFDI” repetido de main; el resto queda igual."),
        "og:description": (DESCRIPCION_OG, "Corrige el “Factura CFDI, factura CFDI” repetido de main; el resto queda igual."),
    },
    "reemplazos": {
        "Ventajas para tu empresa u obra": "Documentación para compras",
        "Precio preferencial por volumen": "¿Cuánto cuesta el pasto al mayoreo?",
        "Entrega por etapas según obra": "Entregas por etapas",
        "Preguntas frecuentes — Mayoreo B2B": "Preguntas de compras sobre pasto al mayoreo",
    },
    "retirados": {
        "Pasto en rollo al mayoreo para constructoras y proyectos": (
            "La definición pasa a la entrada de la portada como respuesta directa (spec §7.3), con precio, mínimo, "
            "factura y cobertura de datos.py."),
        "Pasto fresco garantizado": (
            "Pasa a la garantía (“Cortado para tu pedido: llega del campo…”) y al paso “Entregas por etapas”; “entrega "
            "con grúa” no está en datos.py y queda como pregunta al dueño."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” (confirmado por el dueño) "
            "pasa a la entrada de la sección de clientes."),
    },
}
EOF
git apply <<'EOF'
diff --git a/tools/servicios/pages.py b/tools/servicios/pages.py
index 8afdde2..01bf5e1 100644
--- a/tools/servicios/pages.py
+++ b/tools/servicios/pages.py
@@ -16,20 +16,9 @@ GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
 DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
 VARIEDADES = ("+200", "Variedades en el vivero")
 
-# La home y /pasto-en-rollo-tampico (Etapa 2a), y diseño, mantenimiento y riego (Etapa 2c) salen de
-# tools/site/plantillas/: este script ya no las toca. Quedan las páginas de las Etapas 2d a 2g.
+# La home y /pasto-en-rollo-tampico (Etapa 2a), diseño, mantenimiento y riego (Etapa 2c) y mayoreo de pasto (Etapa 2d)
+# salen de tools/site/plantillas/: este script ya no las toca. Quedan palmas para proyectos (2d) y las de 2e a 2g.
 PAGES = {
-    "mayoreo-pasto-tampico": dict(
-        eyebrow="Constructoras · Fraccionamientos · Industria",
-        title="Pasto al mayoreo", accent="para obras y fraccionamientos",
-        price_pre="Desde", price="$60", price_unit="/m²", price_alt="· pedidos de 500 m² o más",
-        lede="Pasto San Agustín en rollo para constructoras, desarrolladoras, hoteles e industria. Entregas por etapas según el avance de la obra.",
-        facts=[("500 m²", "Pedido mínimo de mayoreo"), ("CFDI 4.0", "Factura y REPSE 773725"), ("Por etapas", "Entregas según el avance de obra")],
-        img="/img/instalacion-pasto-rollo-san-agustin-tampico.webp", img_pos="center 40%",
-        alt="Cuadrilla instalando pasto San Agustín en rollo", caption="Pasto San Agustín cortado para obra.",
-        wa=guided("Hola, necesito pasto al mayoreo para un proyecto.", "Empresa", "Ubicación de la obra", "Metros totales", "Fecha de entrega", foto=False),
-        cta="Cotizar mayoreo",
-    ),
     "vivero-tampico": dict(
         title="Vivero en Tampico", accent="y Ciudad Madero, desde 2007",
         price_pre="Palmas desde", price="$250", price_unit="", price_alt="· pasto $85/m² · plantas por tamaño",
diff --git a/tools/site/generar.py b/tools/site/generar.py
index f33f69e..4e165a2 100644
--- a/tools/site/generar.py
+++ b/tools/site/generar.py
@@ -28,6 +28,7 @@ PAGINAS = (
     ("/mantenimiento-jardines-tampico", "mantenimiento-jardines-tampico/index.html", "servicio",
      "mantenimiento_jardines"),
     ("/sistema-riego-tampico", "sistema-riego-tampico/index.html", "servicio", "sistema_riego"),
+    ("/mayoreo-pasto-tampico", "mayoreo-pasto-tampico/index.html", "b2b", "mayoreo_pasto"),
     ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
     ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
 ) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
EOF
```

- [ ] **Step 4: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short
python3 tools/site/paridad.py informe /mayoreo-pasto-tampico
(cd tools/site && python3 -m unittest tests.test_b2b tests.test_generar tests.test_paridad tests.test_contenido tests.test_consistencia tests.test_reglas tests.test_enlaces 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
```

Expected: `plantillas: 1 de 29 páginas escritas` y `shell: 0 de 108`, luego `0 de 29`; el `status` muestra los archivos de esta tarea y `M public/mayoreo-pasto-tampico/index.html`; `ok` en las seis categorías (`encabezados`, `faq`, `precios`, `enlaces`, `meta`, `jsonld_tipos`); `OK`; `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/plantillas/b2b.py tools/site/contenido/b2b_comun.py tools/site/contenido/mayoreo_pasto.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_b2b.py tools/site/tests/test_consistencia.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/mayoreo-pasto-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(empresas): plantilla b2b y mayoreo de pasto con cotizador por volumen, clientes y REPSE" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Palmas para proyectos

**Files:**
- Create: `tools/site/contenido/palmas_proyectos.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `public/palmas-mayoreo-proyectos/index.html` (regenerado)
- Test: `tools/site/tests/test_b2b.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_guia_palmas.py`, `tools/site/tests/test_reglas.py`, `tools/servicios/tests/test_pagos.py`

Lo que cambia frente a `main` y por qué (cada retiro tiene su motivo en `PARIDAD`):

| En `main` | En 2d |
|---|---|
| Precios "desde" por especie de $850 a $4,200 y paquetes "desde $90,000 / $150,000 / $180,000" | Areca y coco plumoso desde $250 y palma real desde $500 en tamaño chico (dueño, 2026-11-07); las otras 9 especies y los 3 paquetes, "Según cotización" (pregunta al dueño 2) |
| Calculadora con "Rango referencia $180K–$260K" | Armador de palmas: lista real de especie, altura y cantidad, sin total |
| "Proyectos recientes" anónimos con año (6) y "bajo NDA" | Fuera: proyectos sin nombre ni permiso verificables (pregunta 5) |
| Tres "personas" con citas ficticias | Fuera; sus necesidades pasan a los paquetes y a las preguntas de compras |
| Plazos "2–5 días", "lead time 2–8 sem", alturas por especie, "+15 especies", "80+ proyectos", "500 Km²" | Fuera: no están en `datos.py`; el plazo va por escrito en la cotización (pregunta 3) |
| "¿Aceptan pago diferido / a crédito para proyectos? Sí, para proyectos >$100K" | "¿Cómo se paga un proyecto?" con `datos.ANTICIPO_PROYECTOS` (sin crédito: decisión del dueño); `test_reglas` ahora también detecta "pago diferido" y "a crédito para proyectos" |
| Gobierno: "alta en padrón, fianzas de cumplimiento, acta entrega-recepción" | "El Gobierno de Tampico es cliente nuestro… los requisitos de tu convocatoria los revisamos contigo al cotizar" (pregunta 6) |
| Formulario de cotización (no mandaba correo: armaba un WhatsApp y exigía correo y teléfono) | Armador de palmas y CTA final por WhatsApp (pregunta 1) |
| Descripción "12 especies desde $850" | "12 especies; areca y coco plumoso desde $250" (`PARIDAD["meta"]`) |
| `AggregateOffer` 850–4200 y 12 `Offer` con `InStock` | `AggregateOffer` con `lowPrice` 250 y sin `highPrice`; `Offer` solo en las 3 especies con precio, sin disponibilidad |

Se conservan: H1, título, robots, canonical, Open Graph, Twitter Card, `Service` con su `@id`, el nodo `LocalBusiness` `#localbusiness` (Etapa 4), migas, garantía de 30 días en las palmas que siembra el equipo (condicionada y enlazada a `/politicas#garantia-plantas`), factura el día del pago, maniobra incluida en la zona conurbada, las 8 preguntas (7 con su texto ajustado a `datos.py` y la de crédito sustituida) y los tres estados en el título.

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/servicios/tests/test_pagos.py b/tools/servicios/tests/test_pagos.py
index a9c1770..767d8bc 100644
--- a/tools/servicios/tests/test_pagos.py
+++ b/tools/servicios/tests/test_pagos.py
@@ -9,7 +9,7 @@ import hero  # noqa: E402
 from pages import PAGES  # noqa: E402
 
 CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico", "mantenimiento-jardines-tampico",
-                 "sistema-riego-tampico", "mayoreo-pasto-tampico")
+                 "sistema-riego-tampico", "mayoreo-pasto-tampico", "palmas-mayoreo-proyectos")
 
 
 class PaginasConPlantillaTest(unittest.TestCase):
diff --git a/tools/site/tests/test_b2b.py b/tools/site/tests/test_b2b.py
index d1f1716..0490925 100644
--- a/tools/site/tests/test_b2b.py
+++ b/tools/site/tests/test_b2b.py
@@ -18,9 +18,10 @@ import paginas  # noqa: E402
 from test_reglas import textos_publicos  # noqa: E402
 
 P = datos.PRECIOS
-# Cada página migrada agrega su fila aquí y en SCRIPTS (palmas llega en la tarea siguiente).
-RUTAS = {"mayoreo": "/mayoreo-pasto-tampico"}
-SCRIPTS = {"mayoreo": ["/js/vt-medidor.js", "/js/vt-b2b.js"]}
+RUTAS = {"mayoreo": "/mayoreo-pasto-tampico", "palmas": "/palmas-mayoreo-proyectos"}
+SCRIPTS = {"mayoreo": ["/js/vt-medidor.js", "/js/vt-b2b.js"], "palmas": ["/js/vt-b2b.js"]}
+PRECIOS_VIEJOS_PALMAS = ("$850", "$1,200", "$1,500", "$1,600", "$1,800", "$2,000", "$2,200", "$2,400", "$2,800",
+                         "$3,200", "$4,200", "$90,000", "$150,000", "$180,000", "$180K", "$260K", "$100K")
 
 
 def pagina(clave):
@@ -157,5 +158,50 @@ class MayoreoTest(unittest.TestCase):
         self.assertEqual(grafo[0]["provider"]["address"]["streetAddress"], datos.CALLE)
 
 
+class PalmasTest(unittest.TestCase):
+    def test_tabla_de_especies_con_los_precios_del_dueno(self):
+        _h, main, _t, _g = pagina("palmas")
+        tabla = main[main.index('id="vt-h-precio"'):main.index("<h3", main.index('id="vt-h-precio"'))]
+        for nombre, cientifico, precio in datos.PALMAS_PROYECTO:
+            fila = re.search(rf'<th scope="row">{re.escape(nombre)}</th>(.*?)</tr>', tabla).group(1)
+            with self.subTest(especie=nombre):
+                self.assertIn(f"<i>{cientifico}</i>", fila)
+                esperado = f"desde ${precio:,} · tamaño chico" if precio else datos.SEGUN_COTIZACION
+                self.assertIn(esperado, fila)
+
+    def test_sin_precios_ni_proyectos_viejos(self):
+        _h, _m, texto, _g = pagina("palmas")
+        for viejo in PRECIOS_VIEJOS_PALMAS + ("Casos anónimos", "bajo NDA", "Lead time", "spec sheet", "+15",
+                                               "fianzas de cumplimiento", "alta en padrón", "80+"):
+            with self.subTest(viejo=viejo):
+                self.assertNotIn(viejo, texto)
+
+    def test_armador_con_todas_las_especies(self):
+        _h, main, _t, _g = pagina("palmas")
+        armador = main[main.index("data-vt-palmas"):]
+        for nombre, _c, _p in datos.PALMAS_PROYECTO:
+            self.assertEqual(armador.count(f'<option value="{nombre}">'), 3)
+        self.assertIn('data-cta="b2b:armador"', armador)
+
+    def test_garantia_de_plantas_condicionada(self):
+        _h, main, _t, _g = pagina("palmas")
+        garantia = main[main.index('id="vt-h-garantia"'):main.index('id="vt-h-faq"')]
+        self.assertIn("/politicas#garantia-plantas", garantia)
+        self.assertIn("sembramos", garantia)
+
+    def test_json_ld_con_precios_nuevos(self):
+        _h, _m, texto, grafo = pagina("palmas")
+        servicio = grafo[0]
+        self.assertEqual(servicio["offers"], {"@type": "AggregateOffer", "lowPrice": "250", "priceCurrency": "MXN",
+                                              "offerCount": "12"})
+        lista = next(n for n in grafo if n["@type"] == "ItemList")["itemListElement"]
+        con_precio = {e["item"]["name"]: e["item"]["offers"]["price"] for e in lista if "offers" in e["item"]}
+        self.assertEqual(con_precio, {"Palma areca": "250", "Coco plumoso": "250", "Palma real": "500"})
+        self.assertEqual(len(lista), 12)
+        self.assertNotIn("InStock", texto)
+        self.assertEqual([n["@type"] for n in grafo],
+                         ["Service", "LocalBusiness", "ItemList", "FAQPage", "BreadcrumbList", "SpeakableSpecification"])
+
+
 if __name__ == "__main__":
     unittest.main()
diff --git a/tools/site/tests/test_generar.py b/tools/site/tests/test_generar.py
index 82574b8..0d3a92a 100644
--- a/tools/site/tests/test_generar.py
+++ b/tools/site/tests/test_generar.py
@@ -19,7 +19,7 @@ class GenerarTest(unittest.TestCase):
     def test_paginas_registradas_tienen_contexto(self):
         esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
                       "/mantenimiento-jardines-tampico", "/sistema-riego-tampico", "/mayoreo-pasto-tampico",
-                      "/pasto-sintetico",
+                      "/palmas-mayoreo-proyectos", "/pasto-sintetico",
                       "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                      + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
         self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
diff --git a/tools/site/tests/test_guia_palmas.py b/tools/site/tests/test_guia_palmas.py
index 146c64f..b1dbabe 100644
--- a/tools/site/tests/test_guia_palmas.py
+++ b/tools/site/tests/test_guia_palmas.py
@@ -17,7 +17,7 @@ class GuiaPalmasTest(unittest.TestCase):
         for viejo in ('id="lead"', "lead-cta", "lead-email", "Guía gratuita", "Descargar guía", "Lead Magnet"):
             with self.subTest(viejo=viejo):
                 self.assertNotIn(viejo, html)
-        self.assertIn("Sección 11 · Preguntas frecuentes", html)
+        self.assertIn('id="vt-h-faq"', html)  # la página sigue con sus preguntas (plantilla b2b desde la Etapa 2d)
         self.assertFalse((PUBLIC / "pdf" / "guia-12-palmas-arquitectos.pdf").exists())
 
     def test_ninguna_pagina_enlaza_la_guia(self):
diff --git a/tools/site/tests/test_reglas.py b/tools/site/tests/test_reglas.py
index 22dfd15..17cb802 100644
--- a/tools/site/tests/test_reglas.py
+++ b/tools/site/tests/test_reglas.py
@@ -34,7 +34,8 @@ PAGO_AL_TERMINAR_RE = re.compile(r"\bpagas\s+(?:cuando|al\s+ver)\b", re.I)
 # liquidar el saldo o el resto (el pago se explica con el anticipo y las formas de pago). Las citas de clientes no cuentan.
 SALDO_RE = re.compile(r"\bliquid(?:as|a|amos|ar|es)\s+el\s+(?:saldo|resto)\b|\bel\s+(?:saldo|resto)\s+se\s+liquida\b", re.I)
 # Decisión del dueño (2026-11-07): no se ofrece crédito a clientes (ni a instaladores ni a constructoras recurrentes).
-CREDITO_CLIENTES_RE = re.compile(r"\bcr[eé]dito\s+(?:para|a)\s+(?:(?:los|sus|nuestros)\s+)?clientes\b", re.I)
+CREDITO_CLIENTES_RE = re.compile(r"\bcr[eé]dito\s+(?:para|a)\s+(?:(?:los|sus|nuestros)\s+)?clientes\b"
+                                 r"|\bpago\s+diferido\b|\ba\s+cr[eé]dito\s+para\s+(?:proyectos|empresas|obras?)\b", re.I)
 # Decisión del dueño (2026-11-07): la visita para medir tiene costo o depende; nunca "visita sin costo", "visita
 # gratis", "visita gratuita", "la visita no tiene costo", "sin cargo" ni "no cuesta" (tampoco "vamos a medir sin costo").
 GRATIS = (r"(?:sin\s+(?:costo|cargo)|gratis|gratuit(?:[ao]s?|amente)|no\s+(?:tiene\s+(?:ning[uú]n\s+)?costo|cuesta"
@@ -213,7 +214,8 @@ class ReglasDelDuenoTest(unittest.TestCase):
         self.assertEqual(hallazgos, [])
 
     def test_credito_y_pago_al_terminar_se_detectan_sin_tocar_citas_de_clientes(self):
-        for sucio in ("crédito para clientes recurrentes", "Crédito a clientes recurrentes", "crédito a nuestros clientes"):
+        for sucio in ("crédito para clientes recurrentes", "Crédito a clientes recurrentes", "crédito a nuestros clientes",
+                      "¿Aceptan pago diferido o a crédito para proyectos?", "a crédito para empresas"):
             self.assertRegex(sucio, CREDITO_CLIENTES_RE)
         for limpio in ("mensualidades con tarjeta de crédito", "tarjeta de débito o crédito para tu compra"):
             self.assertNotRegex(limpio, CREDITO_CLIENTES_RE)
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_b2b tests.test_generar tests.test_guia_palmas tests.test_reglas 2>&1 | tail -1`
Expected: `FAILED (failures=34, errors=6)` (entre ellas `test_sin_credito_para_clientes`, que ya ve el "pago diferido" de `main`, y 24 subpruebas de `test_sin_precios_ni_proyectos_viejos`).
Run: `cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1`
Expected: `FAILED (failures=1)`.

- [ ] **Step 3: Implementar**

```bash
cd ~/dev/viverosterra-e2d
cat > tools/site/contenido/palmas_proyectos.py <<'EOF'
"""Contenido de /palmas-mayoreo-proyectos (palmas al mayoreo para hoteles, fraccionamientos, industria y gobierno).
Solo datos: la plantilla es tools/site/plantillas/b2b.py, con la tabla de las 12 especies de datos.PALMAS_PROYECTO y
el armador de palmas (componentes.armador_palmas: especie, altura y cantidad → un solo WhatsApp), clientes con nombre y
logo, REPSE verificable y 3 paquetes por tipo de obra con su mensaje.

Precios (decisión del dueño, 2026-11-07): areca y coco plumoso desde $250 y palma real desde $500 en tamaño chico; el
precio sube con la altura; las demás especies, según cotización. Se retiran los precios “desde” de main ($850 a
$4,200 por ejemplar), los paquetes con monto, los proyectos anónimos, los plazos de entrega, las alturas y los “lead
time” por especie, la calculadora de rangos ($180K–$260K) y el pago “a crédito”: nada de eso está en datos.py ni lo
confirmó el dueño (preguntas al final del plan 2d). Título, canonical, robots, Open Graph (salvo la descripción, que
decía “desde $850”: PARIDAD["meta"]), Twitter Card, Service, el nodo LocalBusiness #localbusiness (se va con el grafo
único de la Etapa 4) y migas como estaban publicados; ItemList y AggregateOffer con los precios nuevos.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import b2b_comun

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/palmas-mayoreo-proyectos"
URL = f"{SITE}{RUTA}"
OBRA = "/img/obra"
DESDE, REAL = dinero(P["palma_desde"]), dinero(P["palma_real"])
MENSAJE = mensajes_paginas.EMPRESAS[RUTA]
OG_IMAGEN = f"{SITE}/img/jardin-diseno-paisajismo-pasto-san-agustin-tampico-og.webp"
DESCRIPCION = (f"Productor directo de palmas para proyectos B2B. 12 especies; areca y coco plumoso desde {DESDE}. "
               f"Cobertura Tamaulipas, Veracruz y SLP. {datos.FACTURA} y garantía de arraigo de 30 días en siembra propia.")

META = {
    "title": "Palmas Mayoreo para Proyectos B2B en Tamaulipas, Veracruz y SLP · Viveros Terra",
    "description": DESCRIPCION,
    "robots": "index, follow, max-snippet:-1, max-image-preview:large",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Palmas Mayoreo para Proyectos B2B · Viveros Terra"),
        ("og:description", ("12 especies de palmas para proyectos en Tamaulipas, Veracruz y SLP. CFDI 4.0 y garantía de "
                            "arraigo de 30 días en siembra propia.")),
        ("og:image", OG_IMAGEN),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:locale", "es_MX"),
        ("og:site_name", "Viveros Terra Tampico"),
    ),
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", "Palmas Mayoreo Proyectos B2B · Viveros Terra"),
        ("twitter:description", ("12 especies. CFDI y garantía de arraigo de 30 días en siembra propia. Cobertura "
                                 "Tamaulipas, Veracruz y SLP.")),
        ("twitter:image", OG_IMAGEN),
    ),
}
NEGOCIO = f"{SITE}#localbusiness"  # @id de main; el grafo único con #negocio es de la Etapa 4
SERVICIO = {
    "@type": "Service", "@id": f"{URL}#service", "name": "Palmas al mayoreo para proyectos B2B",
    "serviceType": ("Venta y entrega de palmas para proyectos arquitectónicos, hoteleros, gubernamentales e "
                    "industriales"),
    "provider": {"@id": NEGOCIO},
    "areaServed": [{"@type": "State", "name": n} for n in ("Tamaulipas", "Veracruz", "San Luis Potosí")],
    "offers": {"@type": "AggregateOffer", "lowPrice": str(P["palma_desde"]), "priceCurrency": "MXN",
               "offerCount": str(len(datos.PALMAS_PROYECTO))},
}
LOCAL = {
    "@type": "LocalBusiness", "@id": NEGOCIO, "name": datos.NOMBRE, "url": SITE, "telephone": datos.TELEFONO_TEL,
    "address": {"@type": "PostalAddress", "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas",
                "addressCountry": "MX"},
    "sameAs": ["https://www.facebook.com/viverosterra/", "https://www.instagram.com/viverosterramx"],
}


def _producto(nombre, cientifico, precio):
    producto = {"@type": "Product", "name": nombre, "alternateName": cientifico}
    if precio is not None:
        producto["offers"] = {"@type": "Offer", "price": str(precio), "priceCurrency": "MXN",
                              "description": "Tamaño chico; el precio sube con la altura."}
    return producto


ESPECIES_LD = {"@type": "ItemList", "name": "12 palmas para proyectos B2B", "itemListElement": [
    {"@type": "ListItem", "position": i, "item": _producto(*e)} for i, e in enumerate(datos.PALMAS_PROYECTO, 1)]}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
    {"@type": "ListItem", "position": 2, "name": "Mayoreo B2B", "item": f"{SITE}/mayoreo-pasto-tampico"},
    {"@type": "ListItem", "position": 3, "name": "Palmas Mayoreo Proyectos", "item": URL},
]}

PREGUNTAS = (
    ("¿Cuál es el pedido mínimo al mayoreo?",
     "El precio por volumen depende de la especie, la altura y la cantidad de cada una: con tu lista te damos el precio "
     f"por escrito. Como referencia, la areca y el coco plumoso cuestan desde {DESDE} y la palma real desde {REAL} en "
     "su tamaño más chico."),
    ("¿Hacen envíos fuera de Tamaulipas?",
     f"Sí, por proyecto. Además de Tampico, Madero y Altamira, atendemos {datos.ZONAS_POR_PROYECTO}, y obras en el resto "
     "de Tamaulipas, el norte de Veracruz y San Luis Potosí. El flete se cotiza por ruta y volumen."),
    ("¿Qué pasa si una palma no arraiga?",
     "Las palmas que sembramos nosotros tienen garantía de arraigo de 30 días: si se regaron como te indicamos y no "
     "prende, la reponemos sin costo. No cubre falta o exceso de riego, daños por terceros ni clima extremo. "
     '<a href="/politicas#garantia-plantas">Ver condiciones</a>.'),
    ("¿Tienen factura?",
     f"Sí. {datos.FACTURA} emitida el día del pago, para persona física o moral, con tus datos fiscales validados "
     "antes de la entrega."),
    ("¿Cuánto tarda la entrega?",
     "Depende de la especie, la altura y el destino: el plazo va por escrito en la cotización, con el calendario de "
     "entregas si la obra avanza por etapas."),
    b2b_comun.PREGUNTA_PAGO,
    ("¿Pueden hacer instalación llave en mano?",
     "Sí: maniobra de plantación con nuestra cuadrilla, supervisión y guía de cuidado. La garantía de 30 días aplica a "
     "las palmas que sembramos nosotros. Fuera de la zona conurbada de Tampico, la siembra se cotiza por proyecto."),
    ("¿Trabajan con compras de gobierno?",
     f"Sí: el Gobierno de Tampico es cliente nuestro. Tenemos REPSE {datos.REPSE} y facturamos {datos.FACTURA}; los "
     "requisitos de tu convocatoria (padrón de proveedores, fianzas o actas) los revisamos contigo al cotizar."),
)

PASOS = (
    {"titulo": "Nos mandas tu lista", "quien": "tu", "cuando": "Para empezar",
     "texto": "Especies, alturas y cantidades (o el plano del proyecto), la ubicación de la obra y las fechas."},
    {"titulo": "Cotización por escrito", "quien": "nosotros", "cuando": "Al revisar tu lista",
     "texto": "Precio por especie y altura, total, plazo de entrega y condiciones de pago, por escrito."},
    {"titulo": "Anticipo y calendario", "quien": "juntos", "cuando": "Al confirmar",
     "texto": "Confirmas con un anticipo y fijamos juntos las fechas de entrega según el avance de la obra."},
    {"titulo": "Entrega en obra", "quien": "nosotros", "cuando": "En cada etapa",
     "texto": ("En Tampico, Madero y Altamira la maniobra en obra va incluida; fuera de la zona, el flete se cotiza por "
               "ruta.")},
    {"titulo": "Siembra con garantía", "quien": "nosotros", "cuando": "Si la contratas",
     "texto": ("Si las sembramos nosotros, la garantía de arraigo de 30 días aplica con el riego indicado; te dejamos la "
               "guía de cuidado por escrito.")},
)

FIGURAS = (
    {"src": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961, "numero": 2,
     "alt": "Palmas en costal listas para entrega en el patio del vivero.", "lugar": "Patio del vivero",
     "etapa": "Palmas para entrega"},
    {"src": "/img/especie-coco-plumoso-tampico.webp", "ancho": 466, "alto": 700, "numero": 3,
     "alt": "Coco plumoso (Syagrus romanzoffiana) para proyecto.", "lugar": "Coco plumoso",
     "etapa": f"Desde {DESDE}, tamaño chico"},
    {"src": "/img/especie-palma-areca-tampico.webp", "ancho": 700, "alto": 525, "numero": 4,
     "alt": "Palma areca (Dypsis lutescens) para proyecto.", "lugar": "Palma areca",
     "etapa": f"Desde {DESDE}, tamaño chico"},
)

PAQUETES = (
    {"rotulo": "Paquete 1 · Fraccionamientos", "titulo": "Áreas comunes, camellones y casa muestra",
     "precio_texto": datos.SEGUN_COTIZACION, "detalle": "según especies, alturas y cantidad",
     "puntos": ("Washingtonia y areca para accesos y camellones", "Entregas por etapas: la casa muestra primero",
                "Siembra con nuestra cuadrilla y garantía de 30 días con el riego indicado"),
     "mensaje": ("Hola, quiero cotizar palmas para un fraccionamiento.\nEmpresa: ___\n"
                 "Áreas (accesos, camellones, casa muestra): ___\nEspecies y cantidad: ___\nUbicación: ___\n"
                 "Fecha de entrega: ___")},
    {"rotulo": "Paquete 2 · Hoteles y comercios", "titulo": "Palmas de imagen para hoteles y comercios",
     "precio_texto": datos.SEGUN_COTIZACION, "detalle": "según especies, alturas y cantidad", "rec": True,
     "puntos": ("Palma real, coco plumoso y areca", "Especies para el clima de la costa del Golfo",
                'Diseño del área con el <a href="/diseno-jardines-tampico">Plan Terra</a>, si lo necesitas'),
     "mensaje": ("Hola, quiero cotizar palmas para un hotel o comercio.\nEmpresa: ___\nEspecies y cantidad: ___\n"
                 "Altura aprox.: ___\nUbicación: ___\nFecha de entrega: ___")},
    {"rotulo": "Paquete 3 · Industria y gobierno", "titulo": "Perímetros y áreas públicas de bajo mantenimiento",
     "precio_texto": datos.SEGUN_COTIZACION, "detalle": "según especies, alturas y cantidad",
     "puntos": ("Washingtonia y cycas para perímetros", f"REPSE {datos.REPSE} y factura {datos.FACTURA}",
                '<a href="/mantenimiento-jardines-tampico">Mantenimiento</a> después de la entrega'),
     "mensaje": ("Hola, quiero cotizar palmas para una nave industrial o un área pública.\nEmpresa o institución: ___\n"
                 "Especies y cantidad: ___\nUbicación: ___\nFecha de entrega: ___")},
)

CONTENIDO = {
    "tipo": "b2b",
    "prefijo": "pal",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "nodos": (LOCAL, ESPECIES_LD), "migas": MIGAS_LD,
               "speakable": ("h1", "h2", ".vt-faq summary")},
    # /empresas llega en la Etapa 3: entonces la ruta visible y MIGAS_LD pasan a Inicio › Empresas › Palmas.
    "migas": (("Inicio", "/"), ("Palmas para proyectos", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Constructoras · Hoteles · Gobierno",
        "h1": 'Palmas al mayoreo <span class="vt-serif">para proyectos en Tampico</span>',
        "lede": (f"En Viveros Terra la palma areca y el coco plumoso cuestan desde {DESDE} y la palma real desde {REAL} "
                 "en tamaño chico; el precio sube con la altura. Entregamos en obra en Tampico, Madero y Altamira y, por "
                 f"proyecto, en Tamaulipas, Veracruz y San Luis Potosí, con factura {datos.FACTURA}."),
        "etiqueta": {
            "codigo": "Palmas · 01", "aviso": "Con IVA", "nombre": "Palma areca y coco plumoso",
            "cientifico": "Dypsis lutescens · Syagrus romanzoffiana", "antes": "Tamaño chico · desde", "monto": DESDE,
            "unidad": "c/u",
            "filas": (("Palma real, tamaño chico", f"desde {REAL}"), ("Otras especies y alturas", datos.SEGUN_COTIZACION)),
        },
        "mensaje": MENSAJE,
        "tambien": f'REPSE {datos.REPSE} · factura {datos.FACTURA} · <a href="#precio">arma tu lista de palmas</a>',
        "foto": {"src": "/img/portadas/palmas-reales-mayoreo-vivero-tampico-sm.webp",
                 "srcset": ("/img/portadas/palmas-reales-mayoreo-vivero-tampico-sm.webp 560w, "
                            "/img/portadas/palmas-reales-mayoreo-vivero-tampico.webp 694w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 694, "alto": 1041, "numero": 1,
                 "alt": "Palmas reales en el vivero listas para proyecto", "lugar": "Palmas reales en el vivero",
                 "etapa": "Para proyecto"},
    },
    "prueba": {
        "titulo": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
        "lede": (f"{datos.M2_INSTALADOS} instalados desde {datos.DESDE} en Tamaulipas y la Huasteca: hoteles, "
                 "fraccionamientos, industria y gobierno."),
        "figuras": FIGURAS,
        "nota": ("Si el render pide palmas muy altas de una sola especie, pregúntanos antes de cerrar el plano: a veces "
                 "otra altura u otra especie da el mismo efecto, y te lo decimos al cotizar.", "Al cotizar"),
    },
    "escalas": {
        "titulo": "¿Cuánto cuestan las palmas para proyecto?",
        "lede": (f"Areca y coco plumoso desde {DESDE} y palma real desde {REAL} en tamaño chico, con IVA. El precio sube "
                 "con la altura y se ajusta por cantidad; las demás especies, "
                 f"{datos.SEGUN_COTIZACION.lower()}. Precios {datos.ANIO}."),
        "columnas": ("Especie", "Nombre científico", "Precio"),
        "filas": tuple((n, f"<i>{sci}</i>", f"desde {dinero(p)} · tamaño chico" if p else datos.SEGUN_COTIZACION)
                       for n, sci, p in datos.PALMAS_PROYECTO),
        "caption": ("El precio de cada ejemplar depende de su altura: la cotización por escrito lleva especie, altura, "
                    "cantidad y precio."),
        "titulo_cotizador": "Arma tu lista de palmas",
        "cotizador": "palmas",
    },
    "documentacion": {
        "titulo": "Documentación completa para tu compra empresarial.",
        "lede": "Lo que necesitan compras, finanzas, gobierno y supervisión de obra para liberar el pago.",
        "items": b2b_comun.DOCUMENTACION,
    },
    "paquetes": {
        "titulo": "Empieza con un paquete pre-armado y ajustamos a tu obra.",
        "lede": "Cada paquete es un punto de partida: la cotización final se ajusta a tu plano.",
        "items": PAQUETES,
    },
    "proceso": {"titulo": "Cómo cotizamos tu proyecto de palmas",
                "lede": "De tu lista a la entrega en obra, con precio y plazo por escrito.", "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo de 30 días en las palmas que sembramos.", "grande": "30", "unidad": "días",
        "resumen": datos.GARANTIA_PLANTAS,
        "puntos": (
            ("Si una palma que sembramos no prende en 30 días y se regó como te indicamos, la reponemos sin costo.", True),
            ("Guía de cuidado por escrito al entregar.", True),
            (f"Factura {datos.FACTURA} y REPSE {datos.REPSE}.", True),
            ("No cubre falta o exceso de riego, daños por terceros o por clima extremo, ni palmas que siembra otra "
             "cuadrilla.", False),
        ),
        "pie": '<a href="/politicas#garantia-plantas">Lee las condiciones de la garantía de plantas</a>',
    },
    "faq": {"titulo": "Preguntas frecuentes de compradores B2B.", "preguntas": PREGUNTAS},
    "cobertura": dict(b2b_comun.COBERTURA, titulo="Enviamos palmas a toda la región.",
                      lede=("Entrega en obra en la zona conurbada, con maniobra incluida; en el resto de Tamaulipas, el "
                            "norte de Veracruz y San Luis Potosí, por proyecto y con flete por ruta.")),
    "relacionados": {"titulo": "Otras soluciones para empresas", "items": b2b_comun.relacionados(RUTA)},
    "cierre": {
        "titulo": "Cotiza tu proyecto ahora.",
        "lede": "Mándanos especies, alturas y cantidades, o el plano. Te enviamos precio y plazo por escrito.",
        "mensaje": MENSAJE,
    },
}

PRECIO_VIEJO = ("Precio “desde” por ejemplar de main en tallas de proyecto, sin confirmar por el dueño: queda la decisión "
                "del 2026-11-07 (areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; las demás, "
                "según cotización). Pregunta al dueño en el plan 2d.")
PAQUETE_VIEJO = ("Monto “desde” de un paquete de main que el dueño no confirmó: los 3 paquetes nuevos van “según "
                 "cotización”, cada uno con su mensaje. Pregunta al dueño en el plan 2d.")
RANGO_VIEJO = ("Rango de la calculadora vieja ($180K–$260K) o umbral del pago a crédito ($100K): inventados; el armador de "
               "palmas no muestra total y el pago es anticipo y avances (datos.ANTICIPO_PROYECTOS).")
FAQ_SUMMARY = "La pregunta sigue en el FAQ, ahora como <summary> (la paridad la cuenta en su categoría faq)."
ESPECIE = "La especie sigue como renglón de la tabla de especies (datos.PALMAS_PROYECTO) y en el armador de palmas."
CREDITO = ("Decisión del dueño: no se ofrece crédito ni pago diferido. La pregunta pasa a “¿Cómo se paga un proyecto?” con "
           "el anticipo al confirmar y el resto contra avances de obra (datos.ANTICIPO_PROYECTOS).")
PROYECTO_ANONIMO = ("Proyecto anónimo sin nombre, foto ni permiso verificables: regla del dueño “sin proyectos "
                    "inventados”. Si es real, el dueño lo da con permiso (pregunta del plan 2d).")

PARIDAD = {
    "meta": {"description": (DESCRIPCION, "Decía “12 especies desde $850”: precio sin confirmar; el dueño fijó areca "
                                          "y coco plumoso desde $250 (2026-11-07).")},
    "reemplazos": {
        "Productor directo de palmas para hoteles, fraccionamientos, gobierno e industria": (
            f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B"),
        "12 palmas para proyectos · spec sheet": "¿Cuánto cuestan las palmas para proyecto?",
        "Calcula tu proyecto antes de hablar con ventas.": "Arma tu lista de palmas",
        "Enviamos palmas a toda la región .": "Enviamos palmas a toda la región.",
        "Documentación completa para tu compra empresarial .": "Documentación completa para tu compra empresarial.",
        "CFDI 4.0": f"Factura {datos.FACTURA}",
        "Garantía de arraigo 30 días": "Garantía de arraigo de 30 días en las palmas que sembramos.",
        "Fraccionamiento": "Áreas comunes, camellones y casa muestra",
        "Hotel Boutique": "Palmas de imagen para hoteles y comercios",
        "Parque Industrial": "Perímetros y áreas públicas de bajo mantenimiento",
        "Gobierno / Licitación": "Perímetros y áreas públicas de bajo mantenimiento",
        "Preguntas frecuentes de compradores B2B .": "Preguntas frecuentes de compradores B2B.",
    },
    "retirados": {
        "Por qué arquitectos y compradores corporativos eligen Viveros Terra .": (
            "Diferenciadores sin dato: “productor directo” queda en la descripción; la logística pasa a la cobertura y "
            "al proceso, y la documentación a su sección."),
        "Productor directo": "Queda en la descripción; “capacidad sin agotar stock” no está en datos.py.",
        "Logística regional": ("Pasa a la cobertura y al paso “Entrega en obra” (maniobra incluida en la zona "
                               "conurbada); “transportes propios y red de fleteros” queda como pregunta al dueño."),
        "Documentación B2B": "Pasa a la sección de documentación (CFDI, REPSE, anticipo y avances, entregas).",
        "Hecho para tres tipos de comprador.": (
            "Las tres personas llevaban citas ficticias entre comillas; sus necesidades pasan a los 3 paquetes por obra "
            "y a las preguntas de compras."),
        "Que el ejemplar llegue idéntico al render.": (
            "Cita ficticia; “ficha técnica y foto del ejemplar” no está confirmada (pregunta al dueño). Lo útil pasa a "
            "la nota de campo sobre alturas."),
        "Cumplir auditoría sin retrasos administrativos.": (
            "Cita ficticia; padrón, fianzas y acta de entrega no están confirmados: la pregunta de gobierno los revisa "
            "al cotizar."),
        "No retrasar la fecha de apertura del proyecto.": (
            "Cita ficticia; los plazos “2–5 días” no están en datos.py: el plazo va por escrito en la cotización."),
        **{e: ESPECIE for e in ("Palma Washingtonia", "Palma Real", "Palma Areca", "Palma del Viajero", "Coco Plumoso",
                                "Palma Kerpis", "Cycas Revoluta", "Bambú Tarro", "Yucca Rostrata", "Palma Bambú",
                                "Palma Cola de Zorra", "Palma Triángulo")},
        "Tu proyecto pre-armado": "Resumen de la calculadora vieja; el armador de palmas muestra la lista que se envía.",
        "Nuestras palmas, en foto real .": (
            "La galería de 12 fotos pasa a 3 figuras con pie FIG. en la sección de clientes (peso de la página)."),
        "Algunos proyectos recientes .": PROYECTO_ANONIMO,
        **{t: PROYECTO_ANONIMO for t in ("50 Palma Real + Coco Plumoso", "90 Washingtonia", "Áreas comunes 4 fases",
                                         "Áreas verdes recreativas", "35 Coco Plumoso", "120 plantas + 15 palmas")},
        "Envíos fuera de Tamaulipas": "Pasa a la pregunta “¿Hacen envíos fuera de Tamaulipas?” y a la cobertura.",
        "Licitaciones / gobierno": "Pasa a la pregunta “¿Trabajan con compras de gobierno?”, sin prometer fianzas.",
        **{q: FAQ_SUMMARY for q in ("¿Cuál es el pedido mínimo al mayoreo?", "¿Hacen envíos fuera de Tamaulipas?",
                                    "¿Qué pasa si una palma no arraiga?", "¿Tienen factura?", "¿Cuánto tarda la entrega?",
                                    "¿Pueden hacer instalación llave en mano?", "¿Trabajan con compras de gobierno?")},
        "¿Aceptan pago diferido / a crédito para proyectos?": CREDITO,
        "¿Aceptan pago diferido o a crédito para proyectos?": CREDITO,
        "Formulario de cotización": (
            "El formulario no mandaba correo: armaba un WhatsApp y pedía correo y teléfono obligatorios. Lo sustituyen "
            "el armador de palmas y el CTA final (WhatsApp, como en el resto del sitio; pregunta al dueño)."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” pasa al título de clientes."),
        **{pr: PRECIO_VIEJO for pr in ("$850", "$1,200", "$1,500", "$1,600", "$1,800", "$2,000", "$2,200", "$2,400",
                                       "$2,800", "$3,200", "$4,200")},
        **{pr: PAQUETE_VIEJO for pr in ("$90,000", "$150,000", "$180,000")},
        **{pr: RANGO_VIEJO for pr in ("$100", "$180", "$260")},
    },
}
EOF
git apply <<'EOF'
diff --git a/tools/servicios/pages.py b/tools/servicios/pages.py
index 01bf5e1..66f2eed 100644
--- a/tools/servicios/pages.py
+++ b/tools/servicios/pages.py
@@ -16,8 +16,8 @@ GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
 DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
 VARIEDADES = ("+200", "Variedades en el vivero")
 
-# La home y /pasto-en-rollo-tampico (Etapa 2a), diseño, mantenimiento y riego (Etapa 2c) y mayoreo de pasto (Etapa 2d)
-# salen de tools/site/plantillas/: este script ya no las toca. Quedan palmas para proyectos (2d) y las de 2e a 2g.
+# La home y /pasto-en-rollo-tampico (Etapa 2a), diseño, mantenimiento y riego (Etapa 2c) y mayoreo y palmas para
+# proyectos (Etapa 2d) salen de tools/site/plantillas/: este script ya no las toca. Quedan las de las Etapas 2e a 2g.
 PAGES = {
     "vivero-tampico": dict(
         title="Vivero en Tampico", accent="y Ciudad Madero, desde 2007",
@@ -68,17 +68,6 @@ PAGES = {
         alt="Palma real sembrada en un jardín residencial de Tampico", caption="Palma real en un jardín de Tampico.",
         wa=guided("Hola, quiero cotizar palmas.", "Palma que me interesa", "Altura aprox.", "Colonia de entrega"),
     ),
-    "palmas-mayoreo-proyectos": dict(
-        eyebrow="Constructoras · Hoteles · Gobierno",
-        title="Palmas al mayoreo", accent="para proyectos en Tampico",
-        price_pre="Precio", price="por volumen", price_unit="", price_alt="· según especie, altura y cantidad",
-        lede="Suministro de palmas y árboles para constructoras, desarrolladoras, hoteles y gobierno en Tamaulipas, Veracruz y San Luis Potosí.",
-        facts=[("CFDI 4.0", "Factura emitida el día del pago"), ("3 estados", "Tamaulipas, Veracruz y SLP"), ("30 días", "Garantía de arraigo en siembra propia")],
-        img="/img/palmas-reales-mayoreo-vivero-tampico.webp", img_pos="center 35%",
-        alt="Palmas reales en el vivero listas para proyecto", caption="Palmas en vivero para proyectos.",
-        wa=guided("Hola, necesito palmas al mayoreo para un proyecto.", "Empresa", "Especies y cantidad", "Ubicación de la obra", "Fecha de entrega", foto=False),
-        cta="Cotizar mayoreo",
-    ),
     "arboles-ornamentales-tampico": dict(
         title="Árboles ornamentales", accent="para jardines en Tampico",
         price_pre="Desde", price="$250", price_unit="", price_alt="· flamboyán $250 · crespón $350 · jacaranda $450",
diff --git a/tools/site/generar.py b/tools/site/generar.py
index 4e165a2..747ef4c 100644
--- a/tools/site/generar.py
+++ b/tools/site/generar.py
@@ -29,6 +29,7 @@ PAGINAS = (
      "mantenimiento_jardines"),
     ("/sistema-riego-tampico", "sistema-riego-tampico/index.html", "servicio", "sistema_riego"),
     ("/mayoreo-pasto-tampico", "mayoreo-pasto-tampico/index.html", "b2b", "mayoreo_pasto"),
+    ("/palmas-mayoreo-proyectos", "palmas-mayoreo-proyectos/index.html", "b2b", "palmas_proyectos"),
     ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
     ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
 ) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
EOF
```

- [ ] **Step 4: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /palmas-mayoreo-proyectos
(cd tools/site && python3 -m unittest tests.test_b2b tests.test_generar tests.test_guia_palmas tests.test_reglas tests.test_paridad tests.test_contenido tests.test_consistencia tests.test_enlaces 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
grep -cE "mayoreo-pasto-tampico|palmas-mayoreo-proyectos" tools/servicios/pages.py || true
```

Expected: `plantillas: 1 de 30 páginas escritas` y `shell: 0 de 108`, luego `0 de 30`; `ok` en las seis categorías; `OK`; `OK`; `0`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/contenido/palmas_proyectos.py tools/site/generar.py tools/site/tests/test_b2b.py tools/site/tests/test_generar.py tools/site/tests/test_guia_palmas.py tools/site/tests/test_reglas.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/palmas-mayoreo-proyectos/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(empresas): palmas para proyectos con la plantilla b2b, precios del dueño y armador de palmas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Pruebas en navegador de las páginas para empresas

**Files:**
- Test: `tools/site/tests/test_plantillas_navegador.py`

Las dos páginas entran a las pruebas de plantilla que ya existen (axe de página completa a 375 y 1440, precio y CTA en el primer pantallazo a 375×812, CTA en la primera pantalla a 1024×800, sin desbordar a 320/375/768/1024/1440 y CLS < 0.1) y se agregan cuatro: el cotizador por volumen nunca da $60 con menos de 500 m² y su mensaje lleva m², estimado y empresa; el armador arma un solo mensaje, agrega renglones con labels y foco hasta 8 y no desborda a 375; los clics en `b2b:cotizador`, `b2b:armador` y `b2b:opcion-2` mandan `generate_lead` con `service: "empresas"` y el mensaje firmado; la barra móvil se esconde con el cotizador a la vista.

- [ ] **Step 1: Agregar las pruebas**

```bash
cd ~/dev/viverosterra-e2d
git apply <<'EOF'
diff --git a/tools/site/tests/test_plantillas_navegador.py b/tools/site/tests/test_plantillas_navegador.py
index f57672e..f5e2984 100644
--- a/tools/site/tests/test_plantillas_navegador.py
+++ b/tools/site/tests/test_plantillas_navegador.py
@@ -8,6 +8,7 @@ from urllib.parse import unquote
 sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
 
 import datos  # noqa: E402
+import mensajes_paginas  # noqa: E402
 import servidor  # noqa: E402
 
 try:
@@ -19,7 +20,9 @@ AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
 PAGINAS = ("/", "/pasto-en-rollo-tampico/")
 # Etapa 2c: servicios de jardín con la plantilla de servicio (sin Medidor).
 SERVICIOS = ("/diseno-jardines-tampico/", "/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/")
-CON_PLANTILLA = PAGINAS + SERVICIOS
+# Etapa 2d: páginas para empresas con la plantilla b2b (cotizador por volumen y armador de palmas).
+EMPRESAS = ("/mayoreo-pasto-tampico/", "/palmas-mayoreo-proyectos/")
+CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS
 AXE_PAGINA = """async () => {
   const r = await axe.run(document, { resultTypes: ['violations'] });
   return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
@@ -89,9 +92,10 @@ class PlantillasNavegadorTest(unittest.TestCase):
                 self.assertLessEqual(etiqueta["y"] + etiqueta["height"], alto)
 
     def test_cta_en_la_primera_pantalla_a_1024(self):
-        """Revisión de 2c: a 1024×800 la portada compacta deja el CTA de los servicios de jardín en la primera pantalla."""
+        """Revisión de 2c: a 1024×800 la portada compacta deja el CTA de los servicios de jardín (y, desde 2d, de las
+        páginas para empresas) en la primera pantalla."""
         page = self.pagina(1024, 800)
-        for ruta in SERVICIOS:
+        for ruta in SERVICIOS + EMPRESAS:
             page.goto(self.base + ruta, wait_until="load")
             cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
             with self.subTest(ruta=ruta):
@@ -232,6 +236,79 @@ class PlantillasNavegadorTest(unittest.TestCase):
                 self.assertGreaterEqual(page.locator("[data-sim-list] .sim-plan").count(), 4)
                 self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))
 
+    def mensaje(self, caja):
+        return unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
+
+    def test_cotizador_por_volumen_nunca_da_mayoreo_bajo_500_m2(self):
+        page = self.pagina()
+        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
+        caja = page.locator("[data-vt-volumen]")
+        generico = datos.con_firma(mensajes_paginas.EMPRESAS["/mayoreo-pasto-tampico"])
+        self.assertEqual(self.mensaje(caja), generico)
+        caja.locator('[data-vt-campo="m2"]').fill("320")
+        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$27,200")
+        self.assertIn("Te faltan 180 m²", caja.locator('[data-vt-o="aviso"]').inner_text())
+        self.assertIn("solo el pasto San Agustín", self.mensaje(caja))
+        caja.locator('[data-vt-campo="m2"]').fill("1,200")
+        caja.locator('[data-vt-campo="empresa"]').fill("Mi empresa")
+        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$72,000")
+        self.assertFalse(caja.locator('[data-vt-o="aviso"]').is_visible())
+        mensaje = self.mensaje(caja)
+        self.assertIn("m² totales: 1,200 m²", mensaje)
+        self.assertIn("Estimado de la web: desde $72,000 con IVA (desde $60/m²)", mensaje)
+        self.assertIn("Empresa: Mi empresa", mensaje)
+        caja.locator('[data-vt-campo="m2"]').fill("")
+        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "—")
+        self.assertEqual(self.mensaje(caja), generico)
+
+    def test_armador_de_palmas_arma_un_solo_mensaje(self):
+        page = self.pagina(375, 812)
+        page.goto(self.base + "/palmas-mayoreo-proyectos/", wait_until="load")
+        caja = page.locator("[data-vt-palmas]")
+        self.assertEqual(self.mensaje(caja), datos.con_firma(mensajes_paginas.EMPRESAS["/palmas-mayoreo-proyectos"]))
+        caja.locator("#pal-especie-1").select_option("Palma real")
+        caja.locator("#pal-altura-1").fill("3")
+        caja.locator("#pal-cantidad-1").fill("40")
+        caja.locator("#pal-especie-2").select_option("Coco plumoso")
+        caja.locator("#pal-cantidad-2").fill("20")
+        self.assertEqual(caja.locator('[data-vt-o="resumen"]').inner_text(), "2 especies · 60 piezas")
+        mensaje = self.mensaje(caja)
+        self.assertIn("- 40 × Palma real, altura aprox.: 3 m\n- 20 × Coco plumoso, altura aprox.: ___", mensaje)
+        # "Agregar otra especie" aparece con JS, crea renglones con labels propios y se oculta en el octavo.
+        agregar = caja.locator("[data-vt-agregar]")
+        for n in range(4, 9):
+            agregar.click()
+            self.assertEqual(page.evaluate("() => document.activeElement.id"), f"pal-especie-{n}")
+            self.assertEqual(caja.locator(f'label[for="pal-cantidad-{n}"]').count(), 1)
+        self.assertFalse(agregar.is_visible())
+        self.assertEqual(caja.locator("#pal-especie-8").input_value(), "")
+        sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
+        self.assertLessEqual(sobra, 1)
+
+    def test_clic_en_los_cotizadores_de_empresas_manda_generate_lead(self):
+        for ruta, cta in (("/mayoreo-pasto-tampico/", "b2b:cotizador"), ("/palmas-mayoreo-proyectos/", "b2b:armador"),
+                          ("/palmas-mayoreo-proyectos/", "b2b:opcion-2")):
+            page = self.pagina()
+            page.add_init_script("window.open = () => null;")
+            page.goto(self.base + ruta, wait_until="load")
+            boton = page.locator(f'[data-cta="{cta}"]')
+            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
+            boton.click()
+            eventos = page.evaluate(
+                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
+            with self.subTest(ruta=ruta, cta=cta):
+                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": cta, "service": "empresas"}],
+                              eventos)
+                self.assertTrue(unquote(boton.get_attribute("href").split("text=", 1)[1]).endswith(datos.FIRMA))
+
+    def test_barra_movil_se_esconde_con_el_cotizador_a_la_vista(self):
+        page = self.pagina(375, 812)
+        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
+        page.locator("[data-vt-volumen] .vt-etiqueta").scroll_into_view_if_needed()
+        page.wait_for_function("() => document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
+        page.locator("#vt-h-faq").scroll_into_view_if_needed()
+        page.wait_for_function("() => !document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
+
     def test_cls_bajo_0_1_en_movil(self):
         page = self.pagina(375, 812)
         for ruta in CON_PLANTILLA:
EOF
```

- [ ] **Step 2: Correrlas**

Run: `cd tools/site && python3 -m unittest tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `Ran 19 tests` y `OK`. (Las páginas ya cumplen: en el prototipo, la prueba del armador fue la que encontró el `hidden` que perdía contra `.vt-btn`, corregido en la Tarea 5.)

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2d
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): axe, primer pantallazo, cotizador por volumen, armador de palmas y generate_lead en empresas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Verificación final y puertas de revisión (merge y push los hace el controlador)

**Files:** ninguno nuevo (correcciones de los revisores, cada una con su prueba y su commit).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 30 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 406 tests` y `OK`; `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 47` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas y consistencia a la vista**

```bash
cd ~/dev/viverosterra-e2d
python3 tools/site/paridad.py informe /mayoreo-pasto-tampico /palmas-mayoreo-proyectos
(cd tools/site && python3 -m unittest tests.test_reglas tests.test_consistencia tests.test_paridad tests.test_contenido tests.test_b2b tests.test_b2b_paridad 2>&1 | tail -1)
grep -oiE "oasis|pasto ?plus|\bMSI\b|sin intereses|senasica|sader|fitosanitari|se paga solo|amortiz|pagas cuando|liquida|visita (sin costo|gratis)|gratuit|pago diferido|a cr[eé]dito|lead time|bajo NDA|InStock" public/{mayoreo-pasto-tampico,palmas-mayoreo-proyectos}/index.html | sort | uniq -c
grep -c 'href="/empresas' public/{mayoreo-pasto-tampico,palmas-mayoreo-proyectos}/index.html || true
```

Expected: `ok` en las seis categorías de las dos páginas; `OK`; el `grep` de palabras vacío; `0` y `0` (sin enlace a `/empresas` hasta la Etapa 3).

- [ ] **Step 3: Consola limpia en las 108 páginas y axe**

Run: `cd ~/dev/viverosterra-e2d/tools/site && python3 -m unittest tests.test_navegador tests.test_tienda_navegador tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `OK` (incluye consola sin errores ni `pageerror` en las 108 páginas y axe de página completa en las dos de empresas).

- [ ] **Step 4: Lighthouse móvil en las dos páginas**

```bash
cd ~/dev/viverosterra-e2d
(cd public && python3 -m http.server 8767 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in mayoreo-pasto-tampico palmas-mayoreo-proyectos; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8767/$r/" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2d-lh-$r.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2d-lh-$r.json"
done
pkill -f "http.server 8767"
```

Expected por página: Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s. CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. Si Performance queda abajo por GA4, anota valor y causa (`largest-contentful-paint-element`) para el PR (GA4 diferido es de la Etapa 5).

- [ ] **Step 5: Capturas a 320, 375, 768, 1024 y 1440 con el viewport real de Playwright**

Las capturas se toman con `new_page(viewport=…)` (el ancho real del documento), nunca con `--window-size` de Chromium, que a 375 recorta la página.

```bash
cd ~/dev/viverosterra-e2d/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in ('mayoreo-pasto-tampico', 'palmas-mayoreo-proyectos'):
        for w in (320, 375, 768, 1024, 1440):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}/', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.evaluate("async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } scrollTo(0, 0); }")
            p.screenshot(path=f'/tmp/vt-e2d-{r}-{w}.png', full_page=True)
            p.close()
    b.close()
srv.shutdown()
print('10 capturas')
PY
```

Expected: `10 capturas`. Revisa a mano: una etiqueta amarilla por primer pantallazo móvil con precio y CTA a 375; logos legibles; la tabla de escalas y la de especies como tarjetas a 320/375 y como tabla desde 768; cotizador y armador en una columna en celular y formulario + etiqueta desde 1024; renglones del armador sin cortar el `select`; paquetes en 1 columna a 320/375, 2 a 768 y 3 desde 1024; pies `FIG.`; NOSOTROS / TÚ / JUNTOS; nada que desborde.

- [ ] **Step 6: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega aquí la rama con todo en verde y un resumen (`git log --oneline main..feat/etapa-2d`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2d --stat`, `plantillas/b2b.py`, `contenido/{b2b_comun,mayoreo_pasto,palmas_proyectos}.py`, el bloque nuevo de `componentes.py`, `vt-b2b.js`, el bloque de `terra.css`, la vista previa de Vercel, `/tmp/vt-e2d-*.png`, los JSON de Lighthouse, `paridad.py informe` y el spec (§3.3, §3.4, §4, §5, §6.6, §7.3, §8.3, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta, cuadro de datos, FIG., NOSOTROS/TÚ/JUNTOS), jerarquía de los paquetes (el recomendado se distingue sin depender del color), legibilidad de los logos, tablas a 320, el armador (labels, foco al agregar renglón, objetivos de 44 px) y las capturas.
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta salvo las dos descripciones declaradas, JSON-LD válido en Rich Results Test (`ItemList`, `AggregateOffer` sin `highPrice`, `FAQPage` = lo visible), un H1 por página, respuesta directa citable con precio y mínimo, encabezados en pregunta, enlaces internos entre las páginas B2B, imágenes con `width`/`height` y alt, LCP precargado.
3. **CRO** (`general-purpose` con `page-cro`): recorrido B2B del spec §3.4, plantilla de compras en cada CTA, un mensaje distinto por paquete, cotizador por volumen (aviso bajo 500 m²) y armador (un solo mensaje), objeciones de compras (factura, REPSE, pago, capacidad, plazos, gobierno) y que quitar el formulario no deje a nadie sin camino.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): reglas del dueño, números solo de `datos.py`, ningún precio, plazo, capacidad ni proyecto inventado, `tools/servicios` sin restos de estas páginas, paridad Python–JS, consola limpia y sin `.DS_Store`.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 1 otra vez) y el controlador vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan para el PR.

- [ ] **Step 7: Aprobación del dueño (controlador)**

Comparte la vista previa de Vercel y las capturas, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Si responde con datos (precios de palmas por altura, capacidad, plazos, proyectos con permiso, formulario por correo), van a `datos.py` con su prueba en una tarea nueva antes del merge.

- [ ] **Step 8: Merge, push y despliegue (solo el controlador)**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2d -m "feat: Etapa 2d, mayoreo de pasto y palmas para proyectos con la plantilla b2b" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 30 …`, `shell: 0 de 108 …`, `0`; Vercel despliega `main`.

- [ ] **Step 9: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in mayoreo-pasto-tampico palmas-mayoreo-proyectos; do
  curl -s $W/$r | grep -o "<h1[^>]*>.*</h1>" | head -1
  curl -s $W/$r | grep -cE "fonts.googleapis|tailwind.css|design-system.css|servicios.css"
  curl -s $W/$r | grep -oE 'data-cta="b2b:(opcion-[123]|cotizador|armador)"' | sort -u | wc -l
done
curl -s $W/palmas-mayoreo-proyectos | grep -c '\$850\|\$4,200'
curl -s $W/js/vt-b2b.js | head -1
```

Expected por página: su H1, `0`, `4`; luego `0` y `// public/js/vt-b2b.js`. En Chrome (escritorio y iPhone): consola limpia; el cotizador da $27,200 con 320 m² (y el aviso) y $72,000 con 1,200 m²; el armador manda la lista; cada paquete abre WhatsApp con su plantilla. En GA4 DebugView: `generate_lead` con `cta_id` `b2b:cotizador`, `b2b:armador` y `b2b:opcion-1` y `service` `empresas`.

- [ ] **Step 10: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 11: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2d && git branch -d feat/etapa-2d
```

---

## Correcciones a la hoja de ruta

- `/empresas` no entra en 2d: el spec la pone en la Etapa 3. 2d deja `contenido/b2b_comun.PAGINAS` como su índice y una prueba que impide enlazarla antes de tiempo.
- La paridad de meta era absoluta; 2d agrega `PARIDAD["meta"]` (valor nuevo exacto + motivo) para dos descripciones que no podían seguir publicadas.
- El Instagram "equivocado" de palmas ya está corregido en `main` (`sameAs` = `viverosterramx`); solo el `@id` `#localbusiness` queda para la Etapa 4.
- "Para proyectos solicitamos un anticipo…" pasa a `datos.ANTICIPO_PROYECTOS` y aparece dos veces (FAQ visible y `FAQPage`) en **las dos** páginas, no solo en palmas.
- El "formulario de leads" de palmas no mandaba correo: armaba un WhatsApp. No hay formulario de correo que conservar; si el dueño lo quiere para compras, es una tarea nueva (pregunta 1).
- La plantilla `b2b` no lleva mensualidades con tarjeta: el pago de proyectos es anticipo y avances de obra.
- `llms.txt` enlaza el REPSE en `https://repse.stps.gob.mx/Publico`, que responde 404; las páginas usan la raíz del padrón (200). `llms.txt` se corrige en la Etapa 4.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Quitar precios de palmas por talla de proyecto ($850–$4,200) baja la información para compras | Eran precios sin confirmar que contradicen la decisión del dueño; la tabla dice "desde $250 · tamaño chico" o "Según cotización" y el armador recoge altura y cantidad. Vuelven si el dueño los confirma con altura (pregunta 2). |
| Sin capacidad ni plazos publicados, la objeción "¿tienen volumen para mi obra?" queda abierta | La tabla y la FAQ dicen que van por escrito en la cotización, antes de confirmar; el dueño puede dar cifras (pregunta 3). |
| La coma de miles en m² ("1,200") contra la coma decimal ("12,5") | `leerM2` / `leer_m2` distinguen los dos casos con la misma regla y la prueban en `casos-b2b.json`. |
| `vt-b2b.js` depende de `VTMedidor.calcular` | La plantilla carga `vt-medidor.js` antes (prueba `test_scripts_del_cotizador_en_orden`); sin él, el cotizador queda en su estado inicial con la plantilla de compras (no se rompe). |
| Las fotos `especie-*.webp` podrían no ser del vivero | Pies sin decir "nuestro vivero"; se cambian con la sesión de fotos real tocando solo `src` (pregunta 7). |
| Renault sin logo | Va con su nombre en texto (`componentes.LOGOS`), nunca un logo inventado (pregunta 8). |
| Presupuesto de `terra.css` | 8.74 KB gzip tras 2d; quedan ~1.3 KB para 2e–2i. Las clases nuevas reutilizan las del Medidor. |
| Retirar la galería de 12 especies alarga menos la página pero quita fotos | Se conservan 3 figuras `FIG.` y la tabla de las 12 especies; el catálogo (`/catalogo`, 2e) tiene las fotos por especie. |

## Preguntas al dueño

1. Compras de empresas: ¿siguen solo por WhatsApp (como la home y pasto) o quieren un formulario por correo (a `viverosterra@hotmail.com`) para departamentos de compras que no usan WhatsApp? El de `main` no mandaba correo; 2d lo sustituye por el armador y el CTA.
2. Palmas en tallas de proyecto: los precios de `main` ($850 areca, $1,800 washingtonia, $2,400 coco plumoso, $4,200 palma real, etc.) ¿son reales? ¿A qué altura? Mientras no los confirme, solo se publican areca y coco desde $250 y palma real desde $500 en tamaño chico.
3. Capacidad y tiempos: ¿cuántos m² de pasto pueden entregar por semana y en cuánto tiempo entregan palmas en la zona y fuera? ¿Hay escalas de precio por volumen más allá de "desde $60/m²"?
4. Mínimo de mayoreo de palmas: ¿aplica el "50 ejemplares de la misma especie" que decía `main`?
5. Proyectos B2B con nombre, foto, m² o número de palmas y permiso para publicarlos (los 6 anónimos de `main` no se publican).
6. Logística y gobierno: ¿transportes propios, entrega con grúa, maniobra incluida en la zona conurbada (se conserva), alta en padrones de proveedores, fianzas y acta de entrega-recepción?
7. ¿Las fotos de especies (`/img/especie-*.webp`) son del vivero? Fecha de la sesión de fotos real.
8. Logo de Renault (hoy va en texto) y si se suman más clientes con permiso.
9. ¿Existe una ficha técnica en PDF real para compras? Solo así se publica (spec §3.3).
10. ¿La factura CFDI 4.0 se emite el día del pago en todos los casos (así lo decía `main`)? ¿La lista de 12 especies para proyectos está completa?
