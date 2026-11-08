# Etapa 2g · Zonas y precios: las 6 `/jardineria-*` con la plantilla `zona` y `/precios` con la plantilla `precios` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Séptimo sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2g; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §5, §6.5, §7.3, §8, §10, §11). Las 6 páginas de zona —`/jardineria-lomas-de-rosales-tampico`, `/jardineria-country-club-tampico`, `/jardineria-aguila-tampico`, `/jardineria-lomas-del-chairel-tampico`, `/jardineria-ciudad-madero` y `/jardineria-altamira`— y `/precios` dejan de salir del HTML viejo de `tools/pasto/zonas.py` y `tools/pasto/precios.py` (Google Fonts Geist/Instrument Serif, `tienda-pasto.css` de 52 KB y precios escritos a mano) y salen de dos plantillas nuevas de `tools/site`: **`zona`** (H1 "Jardinería en {zona}" → servicios con precio → lo que pide un jardín en esa zona → colonias con CP → preguntas → otras zonas → CTA con el mensaje de la zona) y **`precios`** (respuesta directa con vigencia → una tabla por línea con columna Unidad, generada de `datos.py` → mensualidades con la fórmula oficial y el simulador → garantías con anclas estables → preguntas → CTA). Con eso `tienda-pasto.css`, `tools/pasto/common.py`, `zonas.py` y `precios.py` se borran. Se publica como parte del lote 5 de la hoja de ruta (2g + 2h + 2i) o sola, si el dueño la quiere antes.

**Architecture:** Igual que 2a–2f: `contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD` (las zonas, como las 11 ciudades: `CLAVES` y `pagina(slug)`); la plantilla arma la página con `componentes.py`; `generar.py` registra las filas; `build.py` las escribe con el shell solo si cambian. Lo nuevo:
1. **`tools/site/componentes_zonas.py`** (componentes.py ya pasa de 800 renglones): `lista()` (Concepto | Unidad | Precio con precio fijo, "desde", rango o "Según cotización"; el nombre enlaza a la página del servicio), `colonias()`, `tabla_sintetico()` (de `tools/pasto/data.MODELOS`), `porcentaje_plazo()` y `tabla_mensualidades()` (llaman a `tools/pasto/mensualidades.py`; no reimplementan la fórmula) y `garantias()` (con `id` por garantía).
2. **`tools/site/contenido/lista_precios.py`**: los renglones de la lista (pasto, servicios, materiales, plantas y la tabla de las zonas), todos con números de `datos.PRECIOS`; `None` = "Según cotización". Lo usan `/precios` y las 6 zonas: un solo lugar para cada precio.
3. **`tools/site/contenido/zona.py`**: los textos de main de cada zona (de `tools/pasto/zonas.py`), sin "A minutos del vivero", con los precios de `datos.py` y la foto de main con un alt y un pie que no dicen en qué colonia se tomó.
4. **Paridad de fotos y anclas:** `tools/site/paridad_zonas.py` congela la lista ordenada de `<img>` del `<main>` (reutiliza `paridad_materiales.fotos`) y los `id` de las `<section>` de las 7 páginas; `test_zonas_reglas.py` exige las mismas fotos en el mismo orden y que ninguna ancla desaparezca. `test_anclas.py` (nuevo, para todo el sitio) exige que cada `<a href="…#x">` llegue a un `id` que existe.
5. **CSS:** las zonas no necesitan nada nuevo (usan `terra.css`); `/precios` trae **`public/css/terra-precios.css`** (691 B minificada, 315 B con gzip: tablas de varias columnas compactas en celular, precio en el renglón de la unidad y `scroll-margin` de las anclas, porque el menú es fijo), cableada como `terra-materiales.css` (`activos.FUENTES`, `partials.head(precios=True)`, `shell.PRECIOS`, `vercel.json`). `terra.css` no se toca (está a 561 B de su tope).
6. **`tools/pasto/build.py`** queda solo con el feed de Merchant y el sitemap de la tienda; `feed.py` importa de `esquema.py`.

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en las pruebas de navegador; CSS plano; JavaScript sin cambios (`vt-simulador.js` y `vt-mensualidades.js` se reutilizan tal cual; `terra.js` mide los CTA); `node --test` sin `package.json`; Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2g` (rama `feat/etapa-2g`, creada desde `main` en `ba421c7`, con este plan como primer commit). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- **Qué se probó y qué no.** El plan se prototipó sobre `ba421c7` en una copia de trabajo fuera del repo con **todo el código de las Tareas 1–10 tal como está aquí**, y las Tareas 1–9 se repitieron en orden sobre un clon limpio (el `public/` y el `tools/site/` resultantes son idénticos al prototipo): capturas, las 7 páginas migradas con su paridad en `ok` en las seis categorías a la primera, `test_zonas_reglas` (y comprobado que falla en las 7 páginas de main: 2 a 6 reglas cada una), `test_anclas` (pasa en main con los 14 pendientes del blog), `test_componentes_zonas`, `test_zona`, `test_precios_pagina`, `test_terra_precios_css`, `test_paginas`, `test_generar`, `test_partials`, `test_activos`, `test_vercel`, `test_terra_css`, `test_limpieza`, `test_paridad`, `test_contenido`, `test_reglas`, `test_consistencia` y `test_enlaces` en verde; build reproducible (segunda corrida: `0 de 48`); `tools/pasto` con 28 pruebas; `node --test` con 67. Las salidas "Expected" son las de esa corrida. **No** se corrieron Lighthouse ni las capturas de la Tarea 11. Los archivos nuevos van completos; los cambios a archivos existentes van como bloques exactos a insertar o reemplazar con el editor. Si una prueba no da lo que dice el plan, arregla el código (no la prueba) salvo que la prueba contradiga el spec; anota cada desvío en el PR.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests` (≈ 4 min), `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`, incluidas en el `discover`).
- Cuando una tarea agrega `terra-precios.css`, el build publica su copia con hash, reescribe el `<head>` de `/precios` y `tools/site/activos.json` gana una clave: se versiona todo (`git add public tools/site/activos.json`) revisando antes `git status --short | grep -v '\.html$'`.
- **Reglas del dueño en juego** (las prueban `test_reglas.py`, `test_consistencia.py` y la nueva `test_zonas_reglas.py`):
  - **Precios solo de `datos.PRECIOS`** (y, por modelo de sintético, de `tools/pasto/data.MODELOS`; los mínimos por plazo, de `tools/pasto/mensualidades.UMBRALES`). Todo lo demás va **"Según cotización"** (`datos.SEGUN_COTIZACION`, con mayúscula en tablas; minúscula a media frase): tierra preparada (**$100** en main), camión de tierra (**"desde $5,000"**), m³ y camión de tezontle, **mármol ($250 el saco en main)**, piedra bola, árboles que no son el flamboyán y plantas de jardín e interior. El `Offer` del mármol a $250 sale del JSON-LD; el tezontle pasa a "desde $200" (`minPrice`), como en su página desde 2f. `test_precios_pagina.test_ningun_precio_escrito_a_mano_en_el_codigo` revisa las cadenas literales de los 6 archivos nuevos.
  - **Zonas sin doorways:** solo hechos locales reales (colonias y CP de SEPOMEX, la loma, la laguna del Chairel, la brisa de Miramar: los textos de main); **sin casos, opiniones, distancias ni tiempos** ("A minutos del vivero" de Madero pasa a "El vivero está en Ciudad Madero" con la dirección; nada de "llegamos en X minutos"). No hay caso real con permiso: la plantilla no lleva esa sección (pregunta 1). El contenido único por zona es de la Etapa 3; aquí no se agrega texto local nuevo.
  - **Fotos:** las de main, todas y en el mismo orden (una por zona y una en `/precios`): sin agregar, quitar ni cambiar ninguna. El alt y el pie pueden mejorar, nunca con "En nuestro vivero" ni diciendo que la foto es de esa colonia (no se sabe dónde se tomaron: pregunta 2). Por eso la tabla de "otras zonas" va sin miniaturas y los servicios enlazan sin tarjetas con foto.
  - Sin "gratis", "sin costo" ni "sin cargo", salvo la frase de la garantía de pasto que aprobó el dueño ("la reponemos sin costo", siempre con sus condiciones). Sin existencias ni disponibilidad, sin "más vendido", "líder", "el mejor" ni "expertos". Pago = anticipo (`datos.ANTICIPO` en las 7 páginas). La visita nunca es gratis: toda página que la menciona lleva `datos.VISITA_COSTO`. Sin "Oasis", sin el nombre del proveedor de la terminal.
  - **Mensualidades:** "con tarjeta de crédito", nunca "MSI" ni "sin intereses"; los mínimos y el "+%" salen de `tools/pasto/mensualidades.py` y el total y la mensualidad del simulador los calcula `vt-mensualidades.js` (vía `vt-simulador.js`): la fórmula no se reimplementa. PROFECO: "el contado (transferencia, efectivo o **tarjeta en una sola exhibición**) es el precio más bajo"; sin la palabra "recargo".
  - **Títulos y meta:** se quedan como están (`PARIDAD["meta"]` vacío en las 7). La consolidación de títulos y los 301 son de la Etapa 3; aquí no se toca `vercel.json` salvo el patrón de la hoja con hash.
- Dos textos de CTA, como en 2a–2f: "Cotizar por WhatsApp" y "Llamar 833 326 8008". Las zonas medían su portada y su cierre como `zona:cuerpo` (el shell los marcaba así); ahora son `zona:hero` y `zona:cierre`, como las demás plantillas (anótalo en el PR para GA4).

## Cobertura del spec y de la hoja de ruta

| Pide el spec / la hoja de ruta / el dueño | Dónde |
|---|---|
| §3.3 zona: H1 "Jardinería en {zona}" → servicios con precio → caso real (con permiso) → problema local → tiempo desde el vivero → CTA con plantilla de zona → enlaces a servicios | Tarea 6 (`plantillas/zona.py`), `test_zona.test_orden_de_secciones`. Sin caso (ninguno con permiso) ni tiempo (regla del dueño): ver Correcciones |
| §3.3 precios: respuesta directa con vigencia → tablas por servicio con columna Unidad → mensualidades (plazos, mínimos, aviso del banco) → garantías y exclusiones → anclas `#garantia-plantas`, `#mensualidades` | Tarea 8 (`plantillas/precios.py`), `test_precios_pagina` |
| Hoja de ruta 2g: `/precios` sin un solo número escrito a mano | `contenido/lista_precios.py`, `test_precios_pagina.test_ningun_precio_escrito_a_mano_en_el_codigo`, `test_zonas_reglas` (`PERMITIDOS`) |
| Hoja de ruta 2g: misma respuesta de precio de pasto que home y pasto en rollo | Primera pregunta = `datos.RESPUESTA_PRECIO_PASTO`; `test_precios_pagina.test_misma_respuesta_de_pasto_que_home_y_pasto_en_rollo` |
| Hoja de ruta 2g: anclas que hoy enlazan otras páginas no se rompen (`test_enlaces` + prueba de anclas nueva) | Tarea 3 (`test_anclas.py`), `paridad_zonas.py` (ids de las secciones de main), Tarea 10 (navegador) |
| Hoja de ruta 2g: contenido único por zona es Etapa 3; sin doorways nuevos | `contenido/zona.py` conserva los textos de main; `test_zonas_reglas` (`SIN_VERIFICAR`: distancias, tiempos, opiniones) |
| Hoja de ruta 2g: `/precios` es la fuente única que enlazan los blogs de precios | La URL y sus anclas no cambian; los blogs la enlazan en 2h |
| Spec §5.1: datos de `datos.py` y fecha de vigencia de precios | `datos.VIGENCIA_PRECIOS` / `VIGENCIA_PRECIOS_ISO` (Tarea 2; pregunta 3) |
| Spec §6.5: zonas enlazadas entre sí y desde servicios | Bloque "Otras zonas donde trabajamos" (`componentes.cobertura`); `test_zona.test_otras_zonas_y_vivero_enlazados` |
| Pruebas de cada lote: axe, sin desbordar 320–1920, consola limpia, CTA y precio en el primer pantallazo, CLS, Lighthouse, capturas | Tareas 10 y 11 |
| Puertas (spec §11): diseño, SEO/AEO (se toca JSON-LD), CRO, cumplimiento | Tarea 11 |

Fuera de 2g: `/zonas`, títulos nuevos, contenido único por zona y casos reales (Etapa 3); grafo JSON-LD único y `dateModified` de todo el sitio (Etapa 4); `/vivero-tampico` (va en 2i con `tools/servicios`, ver Correcciones); `llms.txt` (Etapa 4: ya enlaza `/precios` y las 6 zonas).

## Inventario de lo que hay en producción (`ba421c7`)

| Página | Sale de | Encabezados h1–h3 | FAQ | Precios distintos | Enlaces internos del `<main>` | Fotos | Anclas de sección | Redirects 301 que llegan |
|---|---|---|---|---|---|---|---|---|
| `/jardineria-lomas-de-rosales-tampico` | `tools/pasto/zonas.py` | 9 | 3 | 7 | 9 | 1 (`diseno-jardines-tampico-proyecto`, 960×1574) | colonias, zona, precios, preguntas | 2 |
| `/jardineria-country-club-tampico` | ídem | 9 | 3 | 7 | 9 | 1 (`jardin-residencial-tropical-tampico`, 960×640) | ídem | 0 |
| `/jardineria-aguila-tampico` | ídem | 9 | 3 | 8 | 9 | 1 (`mantenimiento-jardines-poda-pasto-tampico`, 960×1440) | ídem | 3 |
| `/jardineria-lomas-del-chairel-tampico` | ídem | 9 | 3 | 9 | 9 | 1 (`riego-pro-01`, 960×640) | ídem | 0 |
| `/jardineria-ciudad-madero` | ídem | 9 | 3 | 8 | 9 | 1 (`diseno-jardines-madero-altamira-pasto`, 960×640) | ídem | 4 |
| `/jardineria-altamira` | ídem | 9 | 3 | 7 | 9 | 1 (`jardineria-areas-verdes-tampico`, 793×1190) | ídem | 3 |
| `/precios` | `tools/pasto/precios.py` | 9 | 6 | 36 | 27 | 1 (`precios/pasto-rollo-jardin`, 960×1185) | pasto, servicios, sintetico, materiales, plantas, mensualidades, preguntas | 0 |

Son **6 zonas** (no hay más `/jardineria-*` publicadas; las páginas por colonia de antes ya redirigen: 16 redirects `/jardineria-*`, 12 a una zona, 2 a mantenimiento y 2 a la home) y **1 lista de precios**. Las 7 cargan `tienda-pasto.css` (son sus únicas usuarias) y Google Fonts; las 108 páginas del sitio enlazan a las 7 desde el pie. JSON-LD: las zonas, `BreadcrumbList` + `Service` (con `areaServed` por colonia y `AggregateOffer` desde $120/m²) + `FAQPage`; `/precios`, `BreadcrumbList` + `WebPage` (`dateModified` 2026-09-26) + `OfferCatalog` (12 `Offer`, uno de ellos el mármol a $250) + `FAQPage`. Anclas que otras páginas enlazan hoy: ninguna de `/precios` ni de las zonas (sí `/politicas#garantia-plantas` ×12 páginas, `#mensualidades` ×17 y `#devoluciones` ×9, que no cambian). Anclas rotas en todo el sitio: 14, en los índices de tres artículos del blog (de 2h).

Lo que publicaban y no cumple: `/precios` con tierra preparada **$100**, camión **"desde $5,000"**, mármol **"saco $250"** (y su `Offer`), tezontle "costal $200" (sin "desde") y piedra bola "por medida"; ninguna de las 7 dice el anticipo; Madero con "A minutos del vivero"; los pies de foto dicen "Jardín atendido por Viveros Terra en la zona de Tampico" aunque no se sabe dónde se tomaron; los precios de las zonas y de `/precios` están escritos a mano en `tools/pasto`; el `WebPage` dice 2026-09-26 y la página "Actualizada en septiembre 2026".

## Decisiones de diseño (y por qué)

- **Dos plantillas y una hoja:** la zona cabe en `terra.css` con componentes existentes (`portada`, `bloque`, `fichas`, `tabla_comparativa`, `faq`, `cobertura`, `cierre`) más `componentes_zonas.lista`; `/precios` necesita tablas de 4 columnas que en celular no se vuelvan 9 tarjetas, y eso va en `terra-precios.css` (`terra.css` está a 561 B de su tope).
- **Orden de la zona:** servicios con precio primero (spec), después lo que pide un jardín ahí, colonias, preguntas, otras zonas y CTA. Los `id` de main (`precios`, `zona`, `colonias`, `preguntas`) se quedan en sus secciones. Sin "caso real" (sin permiso) ni "tiempo desde el vivero" (regla del dueño): el cuadro de datos de la portada ya dice dónde está el vivero (Obregón 209 Sur) sin distancia.
- **Una sola lista de precios:** `contenido/lista_precios.py` arma los renglones de `/precios` y la tabla de las zonas; ningún precio se escribe dos veces. La tabla de las zonas suma la **poda** ("desde $500, según cotización", `datos.PODA`): es un servicio real que la zona de Águila ya ofrece en su entrada y no tenía precio; el renglón no enlaza porque su página es de la Etapa 3.
- **Materiales en renglones por unidad:** la columna Unidad separa costal y m³ de tierra negra y pone "Según cotización" donde no hay precio confirmado, igual que las páginas de materiales desde 2f (`materiales_comun` da las medidas).
- **Mensualidades:** se conserva la tabla de main (plazo, mínimo de contado y "+%" del total frente al contado, ahora de `componentes_zonas`, que llama a `mensualidades.total_a_plazos`) y se agrega el simulador de 2c (`vt-simulador.js`, que usa `vt-mensualidades.js`) con el mínimo de 12 mensualidades ($15,000) como ejemplo: así la página muestra total y mensualidad con la fórmula oficial sin reimplementarla. El anticipo va en la misma sección.
- **Garantías con ancla propia:** `#garantia-pasto` y `#garantia-plantas` en `/precios` (spec §3.3), cada una con su condición y su enlace (protocolo de riego, `/politicas#garantia-plantas`). `/politicas` no cambia (2i).
- **Vigencia:** `datos.VIGENCIA_PRECIOS = "noviembre 2026"` y `VIGENCIA_PRECIOS_ISO = "2026-11-08"` (el dueño confirmó los precios oficiales el 7 y los de materiales el 8): la portada dice "vigente desde noviembre 2026", la pregunta "¿Cada cuánto cambian…?" y el `WebPage.dateModified` la usan. Si el dueño prefiere otra fecha, se cambia una línea (pregunta 3).
- **Mensajes:** cada zona usa en portada, cierre, menú, barra y pie el mensaje de su portada en main (`mensajes_paginas.ZONAS`, con colonia, servicio y metros por llenar); hasta hoy el menú, la barra y el pie llevaban el genérico de jardín. `/precios` conserva sus mensajes de menú y pie (`test_paginas` los fija) y su portada agrega colonia y metros.
- **Fotos:** una por página, las de main, con `fetchpriority="high"` y precargadas. Alt y pie: los de la página de servicio que publica esa misma foto (diseño, plantas para jardín, mantenimiento, riego) o el alt de main si solo la usa la zona; el pie (`FIG. 01 · …`) describe lo que se ve, no la colonia. Se pierde el `object-position` de main (45–55 %): el marco de la portada recorta al centro; se revisa en las capturas.
- **JSON-LD:** zonas igual que main (`BreadcrumbList`, `Service` con `provider` `#negocio`, `FAQPage` con lo visible). `/precios`: `WebPage`, `OfferCatalog` con 11 `Offer` de `datos.py` (sin mármol; tezontle con `minPrice`), `FAQPage` y `BreadcrumbList`. Nunca `InStock`.

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{jardineria-lomas-de-rosales-tampico,jardineria-country-club-tampico,jardineria-aguila-tampico,jardineria-lomas-del-chairel-tampico,jardineria-ciudad-madero,jardineria-altamira,precios}.json` | Lo que publicaba cada página antes de migrar (`paridad.py capturar`). |
| `tools/site/paridad_zonas.py`, `tools/site/tests/paridad/zonas-fotos-anclas.json` | Fotos (en orden) y anclas de sección de main. |
| `tools/site/componentes_zonas.py` | Lista de precios, colonias, sintético por modelo, mensualidades y garantías. |
| `tools/site/contenido/lista_precios.py` | Renglones de precios (de `datos.py`) para `/precios` y las zonas. |
| `tools/site/contenido/zona.py` | Las 6 zonas (`CLAVES`, `pagina(slug)`). |
| `tools/site/contenido/precios.py` | `/precios`. |
| `tools/site/plantillas/zona.py`, `tools/site/plantillas/precios.py` | Las plantillas nuevas. |
| `public/css/terra-precios.css` | Hoja de `/precios`. |
| `tools/site/tests/{test_zonas_reglas,test_anclas,test_componentes_zonas,test_zona,test_precios_pagina,test_terra_precios_css}.py` | Pruebas nuevas. |

Se modifican: `tools/site/datos.py`, `mensajes_paginas.py`, `generar.py`, `activos.py`, `partials.py`, `shell.py`, `vercel.json`, `tools/pasto/build.py`, `tools/pasto/feed.py`, `tools/pasto/esquema.py`, `public/sitemap.xml` (lastmod de las 7); pruebas `test_paginas`, `test_generar`, `test_partials`, `test_activos`, `test_vercel`, `test_terra_css`, `test_limpieza`, `test_plantillas_navegador`. Se borran: `tools/pasto/{common,zonas,precios}.py`, `tools/pasto/tests/{test_precios,test_plan_selector,test_shell_regiones}.py` (lo que probaban pasa a `test_componentes_zonas`, `test_precios_pagina` y `test_zona`) y `public/css/tienda-pasto.css`. Regenerados por el build: las 7 páginas, `public/css/terra-precios.<hash>.css` y `tools/site/activos.json`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar el worktree**

```bash
cd ~/dev/viverosterra-e2g && git branch --show-current && git log --oneline -2
```

Expected: `feat/etapa-2g`; arriba el commit de este plan (`docs(plan): etapa 2g zonas y precios`) y debajo `ba421c7 merge: etapa 2f — materiales con plantilla material, calculadoras con paridad y formulario de pedido`. Si no existe: `git -C ~/dev/viverosterra worktree add ~/dev/viverosterra-e2g -b feat/etapa-2g`.

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
```

Expected (verificado en `ba421c7`): `plantillas: 0 de 41 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 568 tests` y `OK` (unos 4 min); `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 67` y `ℹ fail 0`; `playwright ok`.

---

### Task 1: Capturas de paridad, fotos y anclas

**Files:**
- Create: `tools/site/tests/paridad/` (7 capturas), `tools/site/paridad_zonas.py`, `tools/site/tests/paridad/zonas-fotos-anclas.json`

- [ ] **Step 1: Capturar las 7 páginas tal como están**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/paridad.py capturar /jardineria-lomas-de-rosales-tampico /jardineria-country-club-tampico /jardineria-aguila-tampico /jardineria-lomas-del-chairel-tampico /jardineria-ciudad-madero /jardineria-altamira /precios
python3 -c "
import json
for p in ('jardineria-lomas-de-rosales-tampico','jardineria-country-club-tampico','jardineria-aguila-tampico','jardineria-lomas-del-chairel-tampico','jardineria-ciudad-madero','jardineria-altamira','precios'):
    d=json.load(open(f'tools/site/tests/paridad/{p}.json')); print(p, len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']), len(d['jsonld_tipos']))"
```

Expected: siete líneas `captura: …` y luego (verificado):
```
jardineria-lomas-de-rosales-tampico 9 3 7 9 9
jardineria-country-club-tampico 9 3 7 9 9
jardineria-aguila-tampico 9 3 8 9 9
jardineria-lomas-del-chairel-tampico 9 3 9 9 9
jardineria-ciudad-madero 9 3 8 9 9
jardineria-altamira 9 3 7 9 9
precios 9 6 36 27 9
```

- [ ] **Step 2: Escribir `tools/site/paridad_zonas.py`**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/paridad_zonas.py <<'EOF'
"""Paridad de las fotos y de las anclas de las 6 zonas y de /precios (Etapa 2g).

Regla del dueño: cada foto de main se queda, en el mismo orden, sin quitar, agregar ni cambiar ninguna (el alt y el pie sí
pueden mejorar). paridad.py no ve imágenes ni anclas; aquí se congela, por página, la lista ordenada de las <img> del
<main> (paridad_materiales.fotos: src, srcset y alt, sin logos) y los id de sus <section>, las anclas que otras páginas,
los buscadores o el botón "Ver la lista" pueden enlazar (#pasto, #mensualidades, #precios…; los id de los títulos sí
cambian). tests/test_zonas_reglas.py exige las mismas fotos en el mismo orden y que cada ancla siga existiendo.

Uso: python3 tools/site/paridad_zonas.py capturar   (escribe tests/paridad/zonas-fotos-anclas.json)
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

RUTAS = ("/jardineria-lomas-de-rosales-tampico", "/jardineria-country-club-tampico", "/jardineria-aguila-tampico",
         "/jardineria-lomas-del-chairel-tampico", "/jardineria-ciudad-madero", "/jardineria-altamira", "/precios")
CAPTURA = paridad.CAPTURAS / "zonas-fotos-anclas.json"
ID_RE = re.compile(r'<section\b[^>]*\sid="([^"]+)"')


def anclas(html):
    """Los id de las <section> del <main>, ordenados."""
    return sorted(set(ID_RE.findall(paridad.principal(html))))


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"fotos": paridad_materiales.fotos(html), "anclas": anclas(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_zonas.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), " ".join(d["anclas"]))
EOF
python3 tools/site/paridad_zonas.py capturar
```

Expected (verificado):
```
/jardineria-lomas-de-rosales-tampico 1 colonias precios preguntas zona
/jardineria-country-club-tampico 1 colonias precios preguntas zona
/jardineria-aguila-tampico 1 colonias precios preguntas zona
/jardineria-lomas-del-chairel-tampico 1 colonias precios preguntas zona
/jardineria-ciudad-madero 1 colonias precios preguntas zona
/jardineria-altamira 1 colonias precios preguntas zona
/precios 1 materiales mensualidades pasto plantas preguntas servicios sintetico
```

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/site/paridad_zonas.py tools/site/tests/paridad/jardineria-*.json tools/site/tests/paridad/precios.json tools/site/tests/paridad/zonas-fotos-anclas.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de las 6 zonas y de precios, con sus fotos y anclas de main" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Vigencia de la lista y mensaje de WhatsApp de cada zona

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/mensajes_paginas.py`
- Test: `tools/site/tests/test_paginas.py`

- [ ] **Step 1: Prueba en rojo**

En `tools/site/tests/test_paginas.py`, agrega antes de `def test_materiales_con_su_mensaje_en_menu_barra_y_pie(self):`

```python
    def test_zonas_con_su_mensaje_en_menu_barra_y_pie(self):
        """Etapa 2g: cada zona lleva en el menú, la barra y el pie el mensaje de su portada en main (antes, el genérico de
        jardín), con la colonia, el servicio y los metros por llenar; /precios conserva los suyos."""
        for nombre, ruta in datos.ZONAS:
            ctx = paginas.contexto(ruta)
            texto = mensajes_paginas.ZONAS[ruta]
            with self.subTest(ruta=ruta):
                self.assertEqual(ctx["mensaje"], datos.con_firma(texto))
                self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
                self.assertEqual((ctx["tipo"], ctx["servicio"]), ("zona", "jardin"))
                self.assertTrue(texto.startswith("Hola, quiero cotizar jardinería en "))
                for hueco in ("Colonia: ___", "Servicio que necesito: ___", "Metros aprox.: ___"):
                    self.assertIn(hueco, texto)
        self.assertEqual(sorted(mensajes_paginas.ZONAS), sorted(r for _n, r in datos.ZONAS))
        self.assertTrue(mensajes_paginas.PRECIOS.startswith(mensajes_paginas.RUTAS["/precios"][0]))
```

Run: `cd tools/site && python3 -m unittest tests.test_paginas 2>&1 | tail -3`
Expected: `AttributeError: module 'mensajes_paginas' has no attribute 'ZONAS'` (ERROR).

- [ ] **Step 2: Los datos y los mensajes**

En `tools/site/datos.py`, debajo de `ZONAS_POR_PROYECTO = …`, agrega:

```python
# Lista de precios (Etapa 2g): desde cuándo rige. El dueño confirmó los precios oficiales el 2026-11-07 (spec,
# "Decisiones del dueño") y los de materiales el 2026-11-08 (Etapa 2f). /precios la muestra ("Lista vigente desde …") y
# su WebPage la usa como dateModified; cambia solo cuando el dueño vuelve a confirmar la lista.
VIGENCIA_PRECIOS = "noviembre 2026"
VIGENCIA_PRECIOS_ISO = "2026-11-08"
```

En `tools/site/mensajes_paginas.py`, antes de `# Ruta exacta → (mensaje del menú y la barra, …)`, agrega:

```python
# Zonas (Etapa 2g): la plantilla de main de cada zona (tools/pasto/zonas.py, guided()), con los huecos ___. La usan la
# portada y el cierre y, por RUTAS, el menú, la barra móvil y el pie (antes llevaban el genérico de jardín).
_ZONA = "Hola, quiero cotizar jardinería en {}.\nColonia: ___\nServicio que necesito: ___\nMetros aprox.: ___\nLes mando foto del espacio."
ZONAS = {
    "/jardineria-lomas-de-rosales-tampico": _ZONA.format("Lomas de Rosales"),
    "/jardineria-country-club-tampico": _ZONA.format("Club Campestre"),
    "/jardineria-aguila-tampico": _ZONA.format("Águila y Altavista"),
    "/jardineria-lomas-del-chairel-tampico": _ZONA.format("Lomas del Chairel"),
    "/jardineria-ciudad-madero": _ZONA.format("Cd. Madero"),
    "/jardineria-altamira": _ZONA.format("Altamira"),
}
# /precios (Etapa 2g): el mensaje del menú (RUTAS) con los huecos de main ("Mi colonia es: ___ y son aprox. ___ m²").
PRECIOS = "Hola, vi la lista de precios y quiero cotizar.\nColonia: ___\nMetros aprox.: ___"
```

y en `RUTAS`, después de `**{ruta: (texto, None) for ruta, texto in MATERIALES.items()},`, agrega `    **{ruta: (texto, None) for ruta, texto in ZONAS.items()},`.

- [ ] **Step 3: En verde, build y commit**

```bash
cd ~/dev/viverosterra-e2g
(cd tools/site && python3 -m unittest tests.test_paginas tests.test_datos 2>&1 | tail -1)
python3 tools/site/build.py | tail -2
git status --short
```

Expected: `OK`; `plantillas: 0 de 41 páginas escritas` y `shell: 0 de 108 páginas actualizadas` (el contador da 0 porque `tools/pasto/build.py` escribe las zonas y les aplica el shell antes); `git status` con las 6 zonas (el menú, la barra y el pie ya llevan su mensaje), `datos.py`, `mensajes_paginas.py` y `test_paginas.py`.

```bash
git add tools/site/datos.py tools/site/mensajes_paginas.py tools/site/tests/test_paginas.py public/jardineria-*/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(zonas): mensaje de WhatsApp de cada zona en menú, barra y pie, y vigencia de la lista de precios en datos.py" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Reglas de zonas y precios en rojo, y anclas de todo el sitio

**Files:**
- Test: `tools/site/tests/test_zonas_reglas.py`, `tools/site/tests/test_anclas.py`

- [ ] **Step 1: Escribir las pruebas**

`test_zonas_reglas.py` arranca con las 7 páginas en `PENDIENTES` (todavía no salen de su plantilla); cada tarea de migración saca las suyas.

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/tests/test_zonas_reglas.py <<'EOF'
"""Reglas del dueño en las 6 zonas y en /precios (Etapa 2g): precios solo de datos.py (o de tools/pasto/data.py para el
sintético por modelo y de tools/pasto/mensualidades.py para los mínimos por plazo; lo demás "según cotización"), sin
"gratis" ni "sin costo" (salvo la garantía de arraigo que aprobó el dueño), sin existencias, sin distancias ni tiempos
de llegada, sin casos ni opiniones de la zona (ninguno tiene permiso), sin superlativos, pago con anticipo, la visita con
su costo, las mismas fotos de main en su orden y las mismas anclas.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca las
suyas) y al cerrar la Etapa 2g queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al sys.path)
import data  # noqa: E402
import datos  # noqa: E402
import mensualidades  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import paridad_zonas  # noqa: E402
from componentes import dinero  # noqa: E402

PUBLIC = paginas.PUBLIC
ZONAS = tuple(ruta for _nombre, ruta in datos.ZONAS)
PAGINAS = ZONAS + ("/precios",)
PENDIENTES = frozenset(PAGINAS)
CAPTURA = json.loads(paridad_zonas.CAPTURA.read_text(encoding="utf-8"))
PERMITIDOS = ({dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))}
              | {dinero(m[k]) for m in data.MODELOS for k in ("t1", "t2", "rollo")}
              | {dinero(minimo) for minimo, _plazos in mensualidades.UMBRALES})
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Lo que el dueño no confirmó (2f): con un precio cerca es un precio inventado. $250 y $500 sí están en datos.py (palmas,
# flamboyán y poda), así que el mármol a $250 o el camión a $5,000 solo se detectan por cercanía.
SIN_PRECIO_RE = re.compile(r"(?:m[aá]rmol|\bsacos?\b|piedra bola|preparada|cami[oó]n(?:es)?)[^.$]{0,30}\$\s?\d", re.I)
# La única frase con "sin costo" que aprobó el dueño (spec, Decisiones: garantía de pasto ligada a sus condiciones).
GARANTIA_PASTO = "la reponemos sin costo"
SIN_VERIFICAR = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b|\bsin cargo\b"),
    ("existencias o disponibilidad", r"InStock|\bdisponibilidad\b|\ben existencia\b|\bdisponibles? (?:hoy|ya)\b|\bagotad"),
    ("distancia o tiempo de llegada", r"\bminutos?\b|\bllegamos en\b|\b\d+\s?km\b|\bkil[oó]metros?\b|\bcuadras\b"
                                      r"|\bmismo d[ií]a\b|\bhoy mismo\b|entrega inmediata|\ben 24 ?h"),
    ("más vendido o superlativo", r"m[aá]s vendid|\bel mejor\b|\blos mejores\b|\bl[ií]der\b|\bimbatible\b"
                                  r"|m[aá]s popular|\bexpertos\b"),
    ("En nuestro vivero", r"en nuestro vivero"),
    ("nunca Oasis ni MSI", r"\bOasis\b|\bMSI\b|sin intereses|meses sin"),
)


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def visible_y_ld(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    titulo = " ".join(re.findall(r"<title>(.*?)</title>", html))
    return " ".join((paridad.texto(paridad.principal(html)), ld, metas, titulo))


def fallas(ruta):
    """Lista de reglas que rompe la página (vacía si cumple todas)."""
    html = html_de(ruta)
    texto = visible_y_ld(html)
    salida = [f"precio que no está en datos.py: {p}"
              for p in sorted({m.group(0).replace(" ", "") for m in PRECIO_RE.finditer(texto)} - PERMITIDOS)]
    salida += [f"presentación sin precio publicado con precio: …{m.group(0)}…" for m in SIN_PRECIO_RE.finditer(texto)]
    limpio = texto.replace(GARANTIA_PASTO, "")
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, limpio, re.I)]
    cuerpo = paridad.principal(html)
    if re.search(r'class="vt-testimonio|<blockquote', cuerpo):
        salida.append("opinión o caso de la zona sin permiso del dueño")
    if datos.ANTICIPO not in texto:
        salida.append("sin datos.ANTICIPO")
    if "visita" in texto.lower() and datos.VISITA_COSTO not in texto:
        salida.append("habla de la visita sin datos.VISITA_COSTO")
    if 'class="vt-pagina' not in html or "tienda-pasto.css" in html or "fonts.googleapis" in html:
        salida.append("no sale de su plantilla (CSS viejo o Google Fonts)")
    nuevas = paridad_zonas.extraer(ruta)
    if [f["src"] for f in nuevas["fotos"]] != [f["src"] for f in CAPTURA[ruta]["fotos"]]:
        salida.append(f"fotos distintas a las de main o en otro orden: {[f['src'] for f in nuevas['fotos']]}")
    for vieja, nueva in zip(CAPTURA[ruta]["fotos"], nuevas["fotos"]):
        if vieja["srcset"] != nueva["srcset"]:
            salida.append(f"srcset distinto en {vieja['src']}")
        if "en nuestro vivero" in (nueva["alt"] or "").lower():
            salida.append(f"alt con «En nuestro vivero»: {nueva['src']}")
    faltan = sorted(set(CAPTURA[ruta]["anclas"]) - set(nuevas["anclas"]))
    if faltan:
        salida.append(f"anclas de main que ya no existen: {faltan}")
    for img in re.findall(r"<img\b[^>]*>", cuerpo):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    return salida


class ZonasReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(PAGINAS) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_zonas_de_datos_son_las_capturadas(self):
        self.assertEqual(sorted(PAGINAS), sorted(CAPTURA))

    def test_las_reglas_detectan_lo_que_deben(self):
        for frase in ("Cotización gratis", "visita sin costo", "availability InStock", "A minutos del vivero",
                      "llegamos en 30 minutos", "a 5 km del vivero", "el mejor pasto", "En nuestro vivero",
                      "más vendido", "empresa líder", "12 MSI"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        for frase in ("Saco ≈ 20 kg a $250", "camión desde $5,000", "Tierra preparada $100"):
            with self.subTest(frase=frase):
                self.assertTrue(SIN_PRECIO_RE.search(frase))
        for limpio in ("Respondemos en menos de 1 hora en horario", "desde 2007 · 15 a 20 días de arraigo",
                       "Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo"):
            with self.subTest(limpio=limpio):
                texto = limpio.replace(GARANTIA_PASTO, "")
                self.assertFalse(any(re.search(patron, texto, re.I) for _r, patron in SIN_VERIFICAR))


if __name__ == "__main__":
    unittest.main()
EOF
cat > tools/site/tests/test_anclas.py <<'EOF'
"""Anclas: cada enlace <a href="#x"> o "/ruta#x" del sitio llega a un id que existe en esa página (Etapa 2g: la lista de
precios y las zonas cambian de plantilla y otras páginas enlazan /politicas#…, /pasto-sintetico#…). PENDIENTES son los
índices de tres artículos del blog que ya estaban rotos en main; los arregla la Etapa 2h y la lista solo puede encoger."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
SITIO = "https://www.viverosterra.com"
ENLACE_RE = re.compile(r'<a\b[^>]*\shref="([^"]*#[^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')
SCRIPT_RE = re.compile(r"<script\b(?![^>]*ld\+json)[^>]*>.*?</script>", re.S)
PENDIENTES = frozenset(
    f"/blog/{post}#{ancla}"
    for post, anclas in (
        ("cuando-plantar-pasto-tampico-calendario",
         ("como-plantarlos", "el-problema-real", "errores-comunes", "mejores-arboles", "reglas-de-oro")),
        ("plantas-resistentes-sal-golfo-tampico",
         ("como-plantarlos", "el-problema-real", "errores-comunes", "mejores-arboles", "reglas-de-oro")),
        ("sistema-riego-automatico-conviene-tampico",
         ("como-plantarlos", "el-problema-real", "mejores-arboles", "reglas-de-oro")),
    ) for ancla in anclas)


def rotas(public=PUBLIC):
    """{"/ruta#ancla": página que la enlaza} de las anclas que no existen en su página."""
    paginas_html = {paginas.ruta_de(p, public): p.read_text(encoding="utf-8") for p in Path(public).rglob("*.html")}
    ids = {ruta: set(ID_RE.findall(html)) for ruta, html in paginas_html.items()}
    salida = {}
    for ruta, html in paginas_html.items():
        for href in ENLACE_RE.findall(SCRIPT_RE.sub("", html)):
            href = href[len(SITIO):] if href.startswith(SITIO) else href
            if not href.startswith(("#", "/")) or href.startswith("//"):
                continue
            destino, _, ancla = href.partition("#")
            destino = destino.split("?")[0].rstrip("/") or ("/" if destino else ruta)
            if ancla not in ids.get(destino, ()):
                salida.setdefault(f"{destino}#{ancla}", ruta)
    return salida


class AnclasTest(unittest.TestCase):
    def test_toda_ancla_enlazada_existe(self):
        self.assertEqual({k: v for k, v in rotas().items() if k not in PENDIENTES}, {})

    def test_pendientes_siguen_rotas(self):
        self.assertEqual(sorted(PENDIENTES - set(rotas())), [], "ya existen: sácalas de PENDIENTES")


if __name__ == "__main__":
    unittest.main()
EOF
(cd tools/site && python3 -m unittest tests.test_zonas_reglas tests.test_anclas 2>&1 | tail -3)
```

Expected: `Ran 6 tests` y `OK`: las 7 páginas de main fallan las reglas como deben (verificado: las 6 zonas, "sin datos.ANTICIPO" y "no sale de su plantilla"; Madero además "distancia o tiempo de llegada: minutos"; `/precios`, `$100`, "preparada $1…", "camión desde $5…", "saco $2…", sin anticipo y sin plantilla) y las únicas anclas rotas del sitio son las 14 del blog.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/site/tests/test_zonas_reglas.py tools/site/tests/test_anclas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(zonas): reglas del dueño para las 6 zonas y precios (pendientes hasta migrarlas) y anclas de todo el sitio" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: `componentes_zonas.py`

**Files:**
- Create: `tools/site/componentes_zonas.py`
- Test: `tools/site/tests/test_componentes_zonas.py`

- [ ] **Step 1: Prueba en rojo**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/tests/test_componentes_zonas.py <<'EOF'
"""Componentes de las zonas y de /precios (componentes_zonas.py): precios de datos.py, "según cotización" sin número,
sintético de tools/pasto/data.py y mensualidades con la fórmula oficial (tools/pasto/mensualidades.py)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_zonas as cz  # noqa: E402
import data  # noqa: E402
import datos  # noqa: E402
import mensualidades  # noqa: E402

P = datos.PRECIOS


class PrecioTest(unittest.TestCase):
    def test_textos_de_precio(self):
        self.assertEqual(cz.precio_texto(P["pasto_solo_m2"]), "$85")
        self.assertEqual(cz.precio_texto(P["pasto_instalado_m2"], desde=True), "desde $120")
        self.assertEqual(cz.precio_texto(P["riego_m2"]), "$180 a $320")
        self.assertEqual(cz.precio_texto(None), datos.SEGUN_COTIZACION)

    def test_lista_con_unidad_enlace_desde_y_segun_cotizacion(self):
        html = cz.lista((
            {"nombre": "Pasto instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²", "detalle": "x",
             "precio": 120, "desde": True},
            {"nombre": "Poda", "unidad": "árbol o palma", "detalle": "y", "precio": 500, "desde": True, "cotiza": True},
            {"nombre": "Mármol", "unidad": "saco", "detalle": "z", "precio": None},
        ), "Precios 2026 con IVA.")
        self.assertIn('<th scope="col">Unidad</th>', html)
        self.assertIn('<a href="/pasto-en-rollo-tampico">Pasto instalado</a>', html)
        self.assertIn('<td class="vt-tabla__p"><small>desde</small>$120</td>', html)
        self.assertIn("<small>desde</small>$500<small>según cotización</small>", html)
        self.assertIn('<td class="vt-tabla__p vt-tabla__p--cotiza">Según cotización</td>', html)
        self.assertEqual(html.count("<tr>"), 4)


class SinteticoYMensualidadesTest(unittest.TestCase):
    def test_sintetico_por_modelo_de_data(self):
        html = cz.tabla_sintetico()
        self.assertEqual(html.count('<th scope="row">'), len(data.MODELOS))
        m = data.MODELOS[0]
        self.assertIn(f'<td>${m["t1"]}</td><td>${m["t2"]}</td><td><b>${m["rollo"]}</b></td>', html)

    def test_porcentajes_desde_la_formula(self):
        """La tabla que publicaba tools/pasto/precios.py (test_precios.py de tools/pasto, movido aquí en 2g)."""
        esperado = {3: 10.5, 6: 14.9, 9: 20.5, 12: 23.4}
        for plazo, pct in esperado.items():
            self.assertEqual(cz.porcentaje_plazo(plazo), pct)
            self.assertEqual(round((mensualidades.total_a_plazos(100000, plazo) / 100000 - 1) * 100, 1), pct)

    def test_tabla_de_mensualidades(self):
        html = cz.tabla_mensualidades()
        for fila in ('<th scope="row">3 mensualidades</th><td>$2,000</td><td><b>+10.5%</b></td>',
                     '<th scope="row">6 mensualidades</th><td>$5,000</td><td><b>+14.9%</b></td>',
                     '<th scope="row">9 mensualidades</th><td>$15,000</td><td><b>+20.5%</b></td>',
                     '<th scope="row">12 mensualidades</th><td>$15,000</td><td><b>+23.4%</b></td>'):
            self.assertIn(fila, html)
        self.assertNotRegex(html.lower(), r"recargo|comisi[oó]n|intereses|msi")


class GarantiasYColoniasTest(unittest.TestCase):
    def test_garantias_con_ancla(self):
        html = cz.garantias(({"id": "garantia-plantas", "titulo": "Plantas", "texto": "30 días",
                              "enlace": ("Condiciones", "/politicas#garantia-plantas")},))
        self.assertIn('<li class="vt-modo" id="garantia-plantas"><h3>Plantas</h3>', html)
        self.assertIn('href="/politicas#garantia-plantas"', html)

    def test_colonias_con_codigo_postal(self):
        html = cz.colonias((("Águila", "89230"),), "Tampico", "Colonias")
        self.assertIn("Águila<br><small>Tampico</small>", html)
        self.assertRegex(html, r'<td data-col="CÓDIGO POSTAL">89230</td>')


if __name__ == "__main__":
    unittest.main()
EOF
(cd tools/site && python3 -m unittest tests.test_componentes_zonas 2>&1 | tail -3)
```

Expected: `ModuleNotFoundError: No module named 'componentes_zonas'`.

- [ ] **Step 2: Los componentes**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/componentes_zonas.py <<'EOF'
"""Componentes de las 6 zonas y de /precios (Etapa 2g): lista de precios con columna Unidad (precio fijo, "desde",
rango o "según cotización", siempre de datos.py), colonias atendidas, pasto sintético por modelo (tools/pasto/data.py) y
mensualidades por plazo (tools/pasto/mensualidades.py, la misma fórmula de public/js/vt-mensualidades.js: aquí no se
reimplementa, solo se llama). Funciones puras, como componentes.py (que ya pasa de 800 renglones).
"""
import componentes as c
import data
import datos
import mensualidades
from partials import esc

SEGUN = datos.SEGUN_COTIZACION
MUESTRA = 100_000  # contado de referencia para escribir el total a plazos como porcentaje (la tabla de main)


def precio_texto(valor, desde=False):
    """"$85", "desde $120", "$180 a $320" (un par de datos.PRECIOS) o "Según cotización" (None: no se inventa)."""
    if valor is None:
        return SEGUN
    if isinstance(valor, tuple):
        return f"{c.dinero(valor[0])} a {c.dinero(valor[1])}"
    return f"{'desde ' if desde else ''}{c.dinero(valor)}"


def _celda(f):
    valor = f["precio"]
    if valor is None:
        return f'<td class="vt-tabla__p vt-tabla__p--cotiza">{SEGUN}</td>'
    desde = "<small>desde</small>" if f.get("desde") else ""
    cotiza = f"<small>{SEGUN.lower()}</small>" if f.get("cotiza") else ""
    return f'<td class="vt-tabla__p">{desde}{precio_texto(valor)}{cotiza}</td>'


def lista(filas, caption, concepto="Servicio"):
    """Tabla Concepto | Unidad | Precio. filas: nombre, detalle, unidad, precio (número o par de datos.PRECIOS, o None)
    y, opcionales, desde, cotiza (además del "desde", "según cotización" debajo: la poda) y href (el nombre enlaza)."""
    cuerpo = []
    for f in filas:
        nombre = f'<a href="{esc(f["href"])}">{f["nombre"]}</a>' if f.get("href") else f["nombre"]
        cuerpo.append(f'<tr><th scope="row"><b>{nombre}</b><span>{f["detalle"]}</span></th>'
                      f'<td class="vt-tabla__u">{f["unidad"]}</td>{_celda(f)}</tr>')
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            f'<th scope="col">{concepto}</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{"".join(cuerpo)}</tbody></table>')


def colonias(items, municipio, caption):
    """Colonias que se atienden con su código postal (verificados con SEPOMEX, tools/site/contenido/zona.py)."""
    filas = tuple((f"{nombre}<br><small>{municipio}</small>", cp) for nombre, cp in items)
    return c.tabla_comparativa(("Colonia", "Código postal"), filas, caption)


def tabla_sintetico(modelos=None):
    """Precio por m² de cada modelo según cuánto compras (tools/pasto/data.py: t1, t2 y rollo)."""
    filas = "".join(
        f'<tr><th scope="row"><a href="/pasto-sintetico/{esc(m["slug"])}">{esc(m["nombre"])}</a><span>{m["mm"]} mm</span>'
        f'</th><td>{c.dinero(m["t1"])}</td><td>{c.dinero(m["t2"])}</td><td><b>{c.dinero(m["rollo"])}</b></td></tr>'
        for m in modelos or data.MODELOS)
    return ('<table class="vt-tabla vt-tabla--compacta"><caption>Precio por m² con IVA según cuánto compras.</caption>'
            f'<thead><tr><th scope="col">Modelo</th><th scope="col">{c.unidades("2 a 9 m²")}</th>'
            f'<th scope="col">{c.unidades("10 a 49 m²")}</th><th scope="col">{c.unidades("Rollo 50 m²")}</th></tr></thead>'
            f'<tbody>{filas}</tbody></table>')


def porcentaje_plazo(plazo):
    """Cuánto más es el total a plazos que el contado, en %, con la fórmula oficial (10.5 en 3 mensualidades)."""
    return round((mensualidades.total_a_plazos(MUESTRA, plazo) / MUESTRA - 1) * 100, 1)


def tabla_mensualidades():
    """Plazo | Desde (contado) | Total frente a contado: los montos mínimos y la fórmula de tools/pasto/mensualidades.py."""
    filas = "".join(f'<tr><th scope="row">{p} mensualidades</th><td>{c.dinero(mensualidades.minimo_de(p))}</td>'
                    f'<td><b>+{porcentaje_plazo(p):.1f}%</b></td></tr>' for p in mensualidades.PLAZOS)
    return ('<table class="vt-tabla vt-tabla--compacta"><caption>Mensualidades con tarjeta de crédito: monto mínimo de '
            'contado por plazo y cuánto más es el total a plazos.</caption><thead><tr><th scope="col">Plazo</th>'
            '<th scope="col">Desde (contado)</th><th scope="col">Total frente a contado</th></tr></thead>'
            f'<tbody>{filas}</tbody></table>')


def garantias(items):
    """Garantías con su ancla estable (#garantia-pasto, #garantia-plantas). items: id, titulo, texto, enlace (texto,
    href)."""
    filas = "".join(f'<li class="vt-modo" id="{esc(g["id"])}"><h3>{g["titulo"]}</h3><p>{g["texto"]}</p>'
                    f'<p class="vt-promesa"><a href="{esc(g["enlace"][1])}">{g["enlace"][0]}</a></p></li>' for g in items)
    return f'<ul class="vt-modos vt-fichas">{filas}</ul>'
EOF
(cd tools/site && python3 -m unittest tests.test_componentes_zonas 2>&1 | tail -3)
```

Expected: `Ran 7 tests` y `OK`. `test_porcentajes_desde_la_formula` y `test_tabla_de_mensualidades` son los de `tools/pasto/tests/test_precios.py`, que se borra en la Tarea 9.

- [ ] **Step 3: Commit**

```bash
git add tools/site/componentes_zonas.py tools/site/tests/test_componentes_zonas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(zonas): componentes de lista de precios con unidad, colonias, sintético por modelo, mensualidades y garantías" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: La lista de precios en un solo lugar

**Files:**
- Create: `tools/site/contenido/lista_precios.py`

- [ ] **Step 1: Los renglones**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/contenido/lista_precios.py <<'EOF'
"""Renglones de la lista de precios (Etapa 2g): los usan /precios (contenido/precios.py) y la tabla de servicios de las 6
zonas (contenido/zona.py). Solo datos: la tabla la arma componentes_zonas.lista().

Todo precio sale de datos.PRECIOS (o de tools/pasto/data.py para el sintético por modelo); lo que no está ahí va
datos.SEGUN_COTIZACION (precio None): tierra preparada, camión de tierra, m³ y camión de tezontle, mármol, piedra bola,
árboles y plantas que no son el flamboyán (regla del dueño, como en 2e y 2f: no se inventa). Los textos de main se
conservan salvo los precios que el dueño no confirmó.
"""
import componentes as c  # primero: agrega tools/pasto al sys.path (data)
import data
import datos
from contenido import materiales_comun as mc

dinero = c.dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
SINTETICO_MIN = min(m["rollo"] for m in data.MODELOS)

PASTO = (
    {"nombre": "Pasto San Agustín, solo el pasto", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
     "precio": P["pasto_solo_m2"],
     "detalle": "Rollo fresco, cortado para tu pedido. Recoges en el vivero o te lo llevamos."},
    {"nombre": "Pasto San Agustín instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
     "precio": P["pasto_instalado_m2"], "desde": True,
     "detalle": f"Preparación básica del suelo, instalación y garantía de arraigo de {datos.ARRAIGO}."},
    {"nombre": "Mayoreo para constructoras y fraccionamientos", "href": "/mayoreo-pasto-tampico", "unidad": "m²",
     "precio": P["pasto_mayoreo_m2"], "desde": True,
     "detalle": (f"Pedidos de {P['pasto_mayoreo_minimo_m2']} m² o más, con entregas por etapas según el avance de la "
                 "obra y factura.")},
)
MANTENIMIENTO = {"nombre": "Mantenimiento de jardín", "href": "/mantenimiento-jardines-tampico", "unidad": "mes",
                 "precio": P["mantenimiento_mes"], "desde": True,
                 "detalle": "Poda, fertilización y control de plagas. Cada 15 a 21 días en lluvias y cada 30 días en secas."}
RIEGO = {"nombre": "Sistema de riego automático", "href": "/sistema-riego-tampico", "unidad": "m²",
         "precio": P["riego_m2"],
         "detalle": "Aspersión o goteo con programador. Se cotiza después de medir y revisar la presión."}
# Poda de palmas y árboles (decisión del dueño, 2026-11-07): "desde $500, según cotización". Su página es de la Etapa 3,
# así que el renglón no enlaza.
PODA = {"nombre": "Poda de palmas y árboles", "unidad": "árbol o palma", "precio": P["poda"], "desde": True,
        "cotiza": True,
        "detalle": ("El precio depende del tamaño del árbol o la palma y de los residuos que se generan. Mándanos fotos "
                    "y ubicación por WhatsApp.")}
SERVICIOS = (
    MANTENIMIENTO,
    {"nombre": "Diseño de jardín, Plan Terra Esencial", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno"],
     "detalle": "Visita, propuesta de diseño y lista de materiales. Entrega en 3 a 5 días hábiles."},
    {"nombre": "Diseño de jardín, Plan Terra Completo", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno_completo"],
     "detalle": "Diseño detallado, fichas de plantas, cuantificación de materiales y manual de cuidados."},
    {"nombre": "Diseño de jardín, Plan Terra Premium", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno_premium"], "desde": True,
     "detalle": "Proyecto ejecutivo con seguimiento. El costo del diseño se descuenta si contratas la obra."},
    RIEGO,
    PODA,
)
MATERIALES = (
    {"nombre": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico", "unidad": "costal",
     "precio": P["tierra_negra_costal"], "detalle": "Recoges en el vivero o te la llevamos; el costo de entrega va en la cotización."},
    {"nombre": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico", "unidad": "m³",
     "precio": P["tierra_negra_m3"], "detalle": f"A granel; el camión volteo, {SEGUN}."},
    {"nombre": "Tierra preparada", "href": "/tierra-negra-vegetal-tampico", "unidad": "costal", "precio": None,
     "detalle": "Con hojarasca y abono."},
    {"nombre": "Tezontle rojo", "href": "/tezontle-rojo-tampico", "unidad": "costal", "precio": P["tezontle_costal"],
     "desde": True, "detalle": f"Piedra volcánica de {mc.TEZONTLE_MEDIDA}; por m³ o en camión de 14 m³, {SEGUN}."},
    {"nombre": "Mármol blanco decorativo", "href": "/marmol-blanco-tampico", "unidad": "saco", "precio": None,
     "detalle": f"{mc.SACO_MARMOL}; 3 sacos cubren 1 m²."},
    {"nombre": "Piedra bola de río", "href": "/piedra-bola-rio-tampico", "unidad": "costal o camión", "precio": None,
     "detalle": " · ".join(f"{n.lower() if i else n} {m}" for i, (n, m) in enumerate(mc.PIEDRA_BOLA_MEDIDAS)) + "."},
)
PLANTAS = (
    {"nombre": "Palmas", "href": "/palmas-tropicales-tampico", "unidad": "pieza", "precio": P["palma_desde"],
     "desde": True, "detalle": f"{datos.PALMAS_PRECIO}."},
    {"nombre": "Árboles", "href": "/arboles-ornamentales-tampico", "unidad": "pieza", "precio": P["flamboyan"],
     "desde": True,
     "detalle": (f"Flamboyán desde {dinero(P['flamboyan'])}; jacaranda, olivo negro, crespón, guayacán y más, "
                 f"{SEGUN}: el precio depende del tamaño.")},
    {"nombre": "Plantas de jardín e interior", "href": "/plantas-para-jardin-tampico", "unidad": "pieza",
     "precio": None, "detalle": f"Más de {datos.VARIEDADES.lstrip('+')} variedades en el vivero."},
)
# Las 6 zonas: los servicios de jardín de main (tools/pasto/zonas.py) más la poda, con precios de datos.py.
ZONA = (
    {"nombre": "Pasto San Agustín instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
     "precio": P["pasto_instalado_m2"], "desde": True,
     "detalle": f"Preparación básica del suelo y garantía de arraigo de {datos.ARRAIGO}."},
    dict(MANTENIMIENTO, detalle="Poda, fertilización, control de plagas y revisión del riego."),
    {"nombre": "Diseño de jardín", "href": "/diseno-jardines-tampico", "unidad": "proyecto", "precio": P["diseno"],
     "desde": True, "detalle": "Plan Esencial; se descuenta si contratas la obra."},
    dict(RIEGO, nombre="Riego automático", detalle="Aspersión o goteo con programador."),
    {"nombre": "Pasto sintético en Tampico", "href": "/pasto-sintetico-tampico", "unidad": "m² instalado",
     "precio": P["sintetico_instalado_m2"][0], "desde": True,
     "detalle": (f"Venta en showroom desde {data.MIN_SHOWROOM_M2} m² o instalación con material y colocación.")},
    {"nombre": "Palmas", "href": "/palmas-tropicales-tampico", "unidad": "pieza", "precio": P["palma_desde"],
     "desde": True, "detalle": "Areca y coco plumoso en tamaño chico; se cotizan por tamaño y volumen."},
    PODA,
)
EOF
python3 -c "
import sys; sys.path.insert(0, 'tools/site')
from contenido import lista_precios as lp
for nombre in ('PASTO', 'SERVICIOS', 'MATERIALES', 'PLANTAS', 'ZONA'):
    filas = getattr(lp, nombre); print(nombre, len(filas), sum(f['precio'] is None for f in filas))"
```

Expected: `PASTO 3 0`, `SERVICIOS 6 0`, `MATERIALES 6 3`, `PLANTAS 3 1`, `ZONA 7 0` (renglones y cuántos van "Según cotización"). Lo prueban `test_precios_pagina` y `test_zonas_reglas` cuando las páginas lo usan.

- [ ] **Step 2: Commit**

```bash
git add tools/site/contenido/lista_precios.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(precios): renglones de la lista de precios de datos.py, con según cotización donde el dueño no dio precio" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Plantilla `zona` y las 6 zonas

**Files:**
- Create: `tools/site/plantillas/zona.py`, `tools/site/contenido/zona.py`
- Modify: `tools/site/generar.py`, `tools/pasto/build.py`
- Test: `tools/site/tests/test_zona.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_zonas_reglas.py`

- [ ] **Step 1: Pruebas en rojo**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/tests/test_zona.py <<'EOF'
"""Plantilla zona (Etapa 2g): orden de secciones del spec sin caso ni tiempo desde el vivero, anclas de main, precios de
datos.py, mensaje de la zona en portada, cierre, menú, barra y pie, sin CSS viejo, y JSON-LD como el de main."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402

ZONAS = tuple(ruta for _n, ruta in datos.ZONAS)


def html_de(ruta):
    return (paginas.PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


class ZonaTest(unittest.TestCase):
    def test_registradas_con_la_plantilla_zona(self):
        filas = {r: (p, c) for r, _s, p, c in generar.PAGINAS}
        for ruta in ZONAS:
            with self.subTest(ruta=ruta):
                self.assertEqual(filas[ruta], ("zona", f"zona:{ruta.strip('/')}"))

    def test_orden_de_secciones(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', html)
            with self.subTest(ruta=ruta):
                self.assertEqual(ids, ["precios", "zona", "colonias", "preguntas"])
                self.assertLess(html.index('id="vt-h1"'), html.index('id="precios"'))
                self.assertLess(html.index('id="vt-h-zonas"'), html.index('id="vt-cierre-titulo"'))

    def test_sin_css_viejo_ni_google_fonts(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                for viejo in ("tienda-pasto.css", "fonts.googleapis", "Geist", "hub-hero", "terra-precios"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_mensaje_de_la_zona_en_portada_cierre_y_shell(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            esperado = datos.con_firma(mensajes_paginas.ZONAS[ruta])
            mensajes = [unquote(m) for m in re.findall(r'data-cta="zona:(?:hero|cierre|header|barra)"[^>]*href="https://'
                                                       r'wa\.me/\d+\?text=([^"]+)"', html)]
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(len(mensajes), 4)
                self.assertEqual(set(mensajes), {esperado})

    def test_otras_zonas_y_vivero_enlazados(self):
        for ruta in ZONAS:
            main = html_de(ruta).split('<main id="main">', 1)[1].split("</main>", 1)[0]
            with self.subTest(ruta=ruta):
                for _n, otra in datos.ZONAS:
                    if otra != ruta:
                        self.assertIn(f'href="{otra}"', main)
                self.assertIn('href="/vivero-tampico"', main)
                self.assertIn('href="/precios"', main)

    def test_json_ld_con_service_faq_y_migas(self):
        for ruta in ZONAS:
            bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_de(ruta), re.S).group(1)
            grafo = json.loads(bloque)["@graph"]
            with self.subTest(ruta=ruta):
                self.assertEqual([n["@type"] for n in grafo], ["BreadcrumbList", "Service", "FAQPage"])
                self.assertEqual(grafo[1]["provider"], {"@id": f"{datos.SITIO}/#negocio"})
                self.assertEqual(grafo[1]["offers"]["lowPrice"], str(datos.PRECIOS["pasto_instalado_m2"]))


if __name__ == "__main__":
    unittest.main()
EOF
```

En `tools/site/tests/test_generar.py`: debajo de `import componentes  # noqa: E402,F401  (agrega tools/pasto al path)` agrega `import datos  # noqa: E402`, y en `test_paginas_registradas_tienen_contexto` cambia

```python
                     + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
```

por

```python
                     + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
                     + [ruta for _nombre, ruta in datos.ZONAS])
```

En `tools/site/tests/test_zonas_reglas.py` cambia `PENDIENTES = frozenset(PAGINAS)` por `PENDIENTES = frozenset({"/precios"})`.

Run: `cd tools/site && python3 -m unittest tests.test_zona tests.test_generar tests.test_zonas_reglas 2>&1 | tail -3`
Expected: `FAILED` (las zonas aún no están en `generar.PAGINAS` ni cumplen las reglas).

- [ ] **Step 2: La plantilla y el contenido**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/plantillas/zona.py <<'EOF'
"""Plantilla de zona (spec §3.3): ruta visible → H1 "Jardinería en {zona}" con el precio ancla en la etiqueta y CTA con
la plantilla de la zona → servicios con precio (de datos.py, cada uno enlaza a su página) → lo que pide un jardín en
esta zona (el problema local) → colonias atendidas con su código postal → preguntas → otras zonas → CTA final.

Del orden del spec no entran, por regla del dueño: el caso real de la zona (ninguno tiene permiso; se agrega con su
prueba cuando el dueño lo dé) y el tiempo desde el vivero (sin distancias ni tiempos de llegada). Páginas: las 6
/jardineria-* (tools/site/contenido/zona.py). Sin hoja propia: todo sale de terra.css."""
import componentes as c
import componentes_zonas as cz
from plantillas import base

CONTEXTO = "https://schema.org"


def render(k):
    tipo = k["tipo"]
    pr, re_, co, f, cb, ci = (k[x] for x in ("precios", "retos", "colonias", "faq", "cobertura", "cierre"))
    secciones = [
        c.portada(k["portada"], tipo, k["migas"]),
        c.bloque(1, "Precios", "vt-h-precios", pr["titulo"],
                 cz.lista(pr["filas"], pr["caption"]) + f'<p class="vt-promesa">{pr["nota"]}</p>',
                 lede=pr["lede"], tinte=True, id_seccion="precios"),
        c.bloque(2, "Tu jardín", "vt-h-zona", re_["titulo"], c.fichas(re_["items"]), id_seccion="zona"),
        c.bloque(3, "Colonias", "vt-h-colonias", co["titulo"],
                 cz.colonias(co["items"], co["municipio"], "Colonias y códigos postales (SEPOMEX)."),
                 lede=co["lede"], tinte=True, id_seccion="colonias"),
        c.bloque_dos(4, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), id_seccion="preguntas"),
        c.bloque(5, "Zonas", "vt-h-zonas", cb["titulo"], c.cobertura(cb["zonas"], cb["por_proyecto"]), lede=cb["lede"],
                 tinte=True),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    j = k["jsonld"]
    grafo = [j["migas"], j["servicio"], c.faq_jsonld(f["preguntas"])]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),))
EOF
cat > tools/site/contenido/zona.py <<'EOF'
"""Contenido de las 6 páginas de zona /jardineria-*. Solo datos: la plantilla es plantillas/zona.py.

Colonias, municipios y códigos postales verificados con directorios SEPOMEX (septiembre 2026); textos de cada zona
(entrada, lo que pide un jardín ahí y preguntas) los de main (tools/pasto/zonas.py hasta la Etapa 2g), con los precios de
datos.py. Reglas del dueño: solo hechos locales reales; sin casos, opiniones, distancias ni tiempos de llegada inventados
(main decía "A minutos del vivero" en Madero: queda la dirección). Un caso real por zona entra solo con permiso del
dueño (ninguno confirmado). Las fotos son las de main, una por zona, sin cambiar; el pie ya no dice que la foto es de la
zona. El contenido único por zona y la consolidación de títulos son de la Etapa 3. PARIDAD: tests/test_paridad.py.
"""
from types import SimpleNamespace

import datos
import mensajes_paginas
from componentes import dinero
from contenido import lista_precios

P = datos.PRECIOS
SITE = datos.SITIO
TIPO = "zona"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
PORTADAS = "/img/portadas"
INSTALADO = dinero(P["pasto_instalado_m2"])
MANTENIMIENTO = dinero(P["mantenimiento_mes"])
RIEGO = f"{dinero(P['riego_m2'][0])} a {dinero(P['riego_m2'][1])}"

# Las fotos de main (una por zona) con un alt y un pie que no dicen en qué colonia se tomaron (no se sabe): los mismos de
# la página de servicio que publica esa foto, o, si solo la usa la zona, el alt de main. (archivo, ancho, alto, alt,
# lugar, etapa)
FOTOS = {
    "jardineria-lomas-de-rosales-tampico": ("diseno-jardines-tampico-proyecto", 960, 1574,
                                            "Jardín residencial diseñado por Viveros Terra en Tampico", "Tampico",
                                            "Terminado"),
    "jardineria-country-club-tampico": ("jardin-residencial-tropical-tampico", 960, 640,
                                        "Jardín residencial con plantas tropicales en Tampico",
                                        "Jardín con plantas tropicales", "Tampico"),
    "jardineria-aguila-tampico": ("mantenimiento-jardines-poda-pasto-tampico", 960, 1440,
                                  "Jardinero de Viveros Terra podando pasto en un jardín de Tampico", "Poda de pasto",
                                  "Tampico"),
    "jardineria-lomas-del-chairel-tampico": ("riego-pro-01", 960, 640,
                                             "Aspersores de riego automático funcionando en un jardín",
                                             "Sistema de riego por aspersión", "Instalado"),
    "jardineria-ciudad-madero": ("diseno-jardines-madero-altamira-pasto", 960, 640,
                                 "Jardín con pasto San Agustín atendido por Viveros Terra", "Pasto San Agustín",
                                 "Jardín atendido"),
    "jardineria-altamira": ("jardineria-areas-verdes-tampico", 793, 1190,
                            "Jardín con pasto San Agustín atendido por Viveros Terra", "Áreas verdes", "Jardín atendido"),
}

ZONAS = {
    "jardineria-lomas-de-rosales-tampico": dict(
        nombre="Lomas de Rosales", municipio="Tampico", corto="Lomas de Rosales",
        title="Jardinería en Lomas de Rosales, Tampico: pasto, diseño y mantenimiento",
        h1="Jardinería en Lomas de Rosales", accent="y Vista Hermosa, Tampico",
        colonias=(("Lomas de Rosales", "89100"), ("Lomas de la Aurora", "89100"), ("Vista Hermosa", "89119")),
        lede=("Pasto en rollo, diseño, riego y mantenimiento para las casas de Lomas de Rosales, Lomas de la Aurora y "
              "Vista Hermosa, en Tampico."),
        retos=(
            ("Terrenos en pendiente", "En la loma el agua de riego y de lluvia escurre. El riego por goteo y las "
             "jardineras escalonadas evitan que se lave la tierra y el pasto se seque en la parte alta."),
            ("Lotes amplios", "Jardines grandes piden un plan de mantenimiento fijo. Con visitas cada 15 a 21 días en "
             "lluvias y cada 30 en secas, el pasto se mantiene parejo."),
            ("Sol fuerte en la parte alta", "Para las zonas más expuestas conviene pasto San Agustín y palmas de sol "
             "pleno como coco plumoso o washingtonia."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en Lomas de Rosales?",
             "Sí. Atendemos Lomas de Rosales, Lomas de la Aurora y Vista Hermosa en Tampico con instalación de pasto, "
             f"diseño, riego y mantenimiento. Agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}"),
            ("¿Cuánto cuesta el mantenimiento de jardín en Lomas de Rosales?",
             f"Desde {MANTENIMIENTO} al mes. El precio final depende de los metros del jardín y de la frecuencia de "
             "visitas."),
            ("¿Qué riego conviene en un jardín con pendiente?",
             "Goteo en jardineras y aspersión de bajo caudal en el pasto, con zonas separadas para la parte alta y la "
             "baja. Así el agua no escurre y se aprovecha mejor."),
        ),
    ),
    "jardineria-country-club-tampico": dict(
        nombre="Club Campestre y Country Club", municipio="Tampico", corto="Club Campestre",
        title="Jardinería en Club Campestre y Country Club, Tampico",
        h1="Jardinería en Club Campestre", accent="y Country Club, Tampico",
        colonias=(("Club Campestre", "89217"), ("Country Club", "89218"), ("Sierra Morena", "89210")),
        lede=("Instalación de pasto, diseño de jardín, riego automático y mantenimiento para las casas de Club "
              "Campestre, Country Club y Sierra Morena, en Tampico."),
        retos=(
            ("Jardines grandes", "En lotes amplios, el riego automático por zonas ahorra agua y tiempo. Lo diseñamos "
             "según el pasto, las jardineras y la presión de tu casa."),
            ("Pasto parejo todo el año", "El pasto San Agustín necesita poda frecuente en lluvias y fertilización por "
             "temporada. Un plan mensual evita que se amarille en secas."),
            ("Palmas y árboles grandes", "Palmas y árboles de porte con garantía de arraigo de 30 días en los que sembramos "
             'nosotros, con el riego indicado (<a href="/politicas#garantia-plantas">ver condiciones</a>).'),
        ),
        faqs=(
            ("¿Atienden jardines en Club Campestre y Country Club?",
             "Sí. Atendemos Club Campestre, Country Club y Sierra Morena en Tampico con pasto en rollo, diseño, riego "
             "automático y mantenimiento."),
            ("¿Cuánto cuesta un sistema de riego automático?",
             f"De {RIEGO} por m², según el tipo de sistema. Medimos y revisamos la presión en la visita. "
             f"{datos.VISITA_COSTO}"),
            ("¿Pueden encargarse del jardín todo el año?",
             f"Sí. El mantenimiento cuesta desde {MANTENIMIENTO} al mes, con visitas cada 15 a 21 días en lluvias y "
             "cada 30 días en secas."),
        ),
    ),
    "jardineria-aguila-tampico": dict(
        nombre="Águila, Altavista y Petrolera", municipio="Tampico", corto="Águila y Altavista",
        title="Jardinería en Águila, Altavista y Petrolera, Tampico",
        h1="Jardinería en Águila,", accent="Altavista y Petrolera, Tampico",
        colonias=(("Águila", "89230"), ("Altavista", "89240"), ("Petrolera", "89110"), ("Campbell", "89260")),
        lede=("Pasto, poda de árboles, diseño y mantenimiento para las casas de Águila, Altavista, Petrolera y "
              "Campbell, en Tampico."),
        retos=(
            ("Árboles grandes y sombra", "Son colonias con árboles maduros. El pasto San Agustín aguanta media sombra, "
             "pero bajo copas cerradas conviene plantas de sombra o cubresuelos."),
            ("Jardines de frente y patios", "En espacios medianos, un diseño sencillo con pasto, jardineras y dos o "
             "tres palmas da más orden y menos mantenimiento."),
            ("Poda y raíces", "Podamos árboles y palmas con técnica para no dañarlos. Si una raíz levanta la banqueta, "
             "te recomendamos especies de raíz controlada."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en la colonia Águila y Altavista?",
             "Sí. Atendemos Águila, Altavista, Petrolera y Campbell en Tampico con pasto en rollo, poda, diseño y "
             "mantenimiento."),
            ("¿El pasto San Agustín crece en sombra?",
             "Aguanta media sombra, con unas 4 horas de sol directo. Bajo árboles muy cerrados te recomendamos plantas "
             "de sombra o cubresuelos."),
            ("¿Cuánto cuesta poner pasto en el frente de mi casa?",
             f"El pasto San Agustín instalado cuesta desde {INSTALADO}/m² con preparación básica del suelo. Solo el "
             f"pasto cuesta {dinero(P['pasto_solo_m2'])}/m²."),
        ),
    ),
    "jardineria-lomas-del-chairel-tampico": dict(
        nombre="Lomas del Chairel", municipio="Tampico", corto="Lomas del Chairel",
        title="Jardinería en Lomas del Chairel y Colinas de San Gerardo, Tampico",
        h1="Jardinería en Lomas del Chairel", accent="y Colinas de San Gerardo",
        colonias=(("Lomas del Chairel", "89360"), ("Colinas de San Gerardo", "89367"), ("Flamboyanes", "89330")),
        lede=("Pasto en rollo, riego, diseño y mantenimiento para las casas cerca de la laguna del Chairel: Lomas del "
              "Chairel, Colinas de San Gerardo y Flamboyanes."),
        retos=(
            ("Humedad y lluvias", "Cerca de la laguna el suelo tarda más en secar. Un buen drenaje y tierra bien "
             "preparada evitan hongos y encharcamientos en el pasto."),
            ("Casas nuevas", "En fraccionamientos recientes el suelo suele ser de relleno. Antes del pasto conviene una "
             "capa de tierra negra vegetal."),
            ("Mosquitos y agua estancada", "Revisamos que el riego no deje charcos y que las macetas y jardineras "
             "drenen bien."),
        ),
        faqs=(
            ("¿Atienden jardines en Lomas del Chairel y Colinas de San Gerardo?",
             "Sí. Atendemos Lomas del Chairel, Colinas de San Gerardo y Flamboyanes en Tampico con pasto, riego, diseño "
             "y mantenimiento."),
            ("¿Qué hago si mi jardín se encharca?",
             "Revisamos el nivel del terreno y el drenaje. A veces basta con nivelar y mejorar la tierra; en otros "
             f"casos hace falta un dren. Lo revisamos en la visita para medir. {datos.VISITA_COSTO}"),
            ("¿Necesito tierra negra antes de poner pasto?",
             f"En casas nuevas con suelo de relleno, sí. La tierra negra vegetal cuesta "
             f"{dinero(P['tierra_negra_costal'])} el costal o {dinero(P['tierra_negra_m3'])} el m³."),
        ),
    ),
    "jardineria-ciudad-madero": dict(
        nombre="Ciudad Madero", municipio="Ciudad Madero", corto="Cd. Madero",
        title="Jardinería en Ciudad Madero y Playa Miramar: pasto, diseño y mantenimiento",
        h1="Jardinería en Ciudad Madero", accent="y Playa Miramar",
        colonias=(("Playa Miramar", "89506"), ("Jardín 20 de Noviembre", "89440"), ("Residencial del Parque", "89514"),
                  ("Ampliación Unidad Nacional", "89510")),
        lede=("Nuestro vivero está en Ciudad Madero. Instalamos pasto, diseñamos y damos mantenimiento en Playa "
              "Miramar, Jardín 20 de Noviembre y el resto de la ciudad."),
        retos=(
            ("Brisa y salitre cerca de la playa", "En Miramar el viento trae sal. Recomendamos plantas y palmas que la "
             "toleran, como coco plumoso, washingtonia y cubresuelos costeros."),
            ("Suelo arenoso", "La arena retiene poca agua y pocos nutrientes. Mejoramos el suelo con tierra negra y "
             "ajustamos el riego y la fertilización."),
            # Main decía "A minutos del vivero": sin distancias ni tiempos (regla del dueño); queda la dirección.
            ("El vivero está en Ciudad Madero", f"Estamos en {datos.CALLE}, {datos.COLONIA}, frente a Walmart. Puedes "
             "venir a escoger tus plantas."),
        ),
        faqs=(
            ("¿Dónde está el vivero de Viveros Terra en Madero?",
             f"En {datos.CALLE}, {datos.COLONIA}, {datos.CP} Cd. Madero, frente a Walmart. {datos.HORARIO}."),
            ("¿Qué plantas aguantan la brisa de Playa Miramar?",
             "Coco plumoso, washingtonia, uva de mar y plantas de hoja gruesa toleran el salitre. Te decimos cuáles "
             "según qué tan cerca estés del mar."),
            ("¿Cuánto cuesta el pasto en rollo en Madero?",
             f"El pasto San Agustín cuesta {dinero(P['pasto_solo_m2'])}/m² solo el pasto y desde {INSTALADO}/m² "
             f"instalado, con garantía de arraigo de {datos.ARRAIGO}."),
        ),
    ),
    "jardineria-altamira": dict(
        nombre="Altamira", municipio="Altamira", corto="Altamira",
        title="Jardinería en Altamira y Lagunas de Miralta: pasto, diseño y mantenimiento",
        h1="Jardinería en Altamira", accent="y Lagunas de Miralta",
        colonias=(("Residencial Lagunas de Miralta", "89605"), ("Altamira Centro", "89600")),
        lede="Pasto en rollo, diseño, riego y mantenimiento para Residencial Lagunas de Miralta y el resto de Altamira.",
        retos=(
            ("Jardines de fraccionamiento", "En fraccionamientos cerrados coordinamos horarios y acceso con la "
             "administración para instalar y dar mantenimiento."),
            ("Áreas verdes amplias", "Para jardines grandes, el riego automático por zonas y un plan de mantenimiento "
             "mensual mantienen el pasto parejo."),
            ("Casas nuevas", "Si tu casa es nueva, preparamos el suelo con tierra negra antes de instalar el pasto para "
             f"que arraigue en {datos.ARRAIGO}."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en Lagunas de Miralta?",
             "Sí. Atendemos Residencial Lagunas de Miralta y el resto de Altamira con pasto, diseño, riego y "
             f"mantenimiento. {datos.VISITA_COSTO}"),
            ("¿Cuánto cuesta el mantenimiento de jardín en Altamira?",
             f"Desde {MANTENIMIENTO} al mes. El precio depende de los metros y de la frecuencia de visitas."),
            ("¿Atienden empresas en el puerto industrial de Altamira?",
             f"Sí. Tenemos REPSE {datos.REPSE} y factura {datos.FACTURA} para contratos de mantenimiento de áreas "
             'verdes. Ve el <a href="/mantenimiento-jardines-tampico">servicio de mantenimiento</a>.'),
        ),
    ),
}
CLAVES = tuple(ZONAS)


def _foto(slug):
    archivo, ancho, alto, alt, lugar, etapa = FOTOS[slug]
    return {"src": f"{PORTADAS}/{archivo}-sm.webp",
            "srcset": f"{PORTADAS}/{archivo}-sm.webp 560w, {PORTADAS}/{archivo}.webp {ancho}w",
            "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": ancho, "alto": alto, "numero": 1, "alt": alt,
            "lugar": lugar, "etapa": etapa}


def _otras(slug):
    return tuple((nombre, ruta) for nombre, ruta in datos.ZONAS if ruta != f"/{slug}")


def contenido(slug):
    z = ZONAS[slug]
    url = f"{SITE}/{slug}"
    corto = z["corto"]
    mensaje = mensajes_paginas.ZONAS[f"/{slug}"]
    descripcion = (f"{z['lede']} Pasto instalado desde {INSTALADO}/m², mantenimiento desde {MANTENIMIENTO}/mes. "
                   "Cotiza por WhatsApp.")
    titulo = f"{z['title']} · Viveros Terra"
    imagen = f"{SITE}{PORTADAS}/{FOTOS[slug][0]}.webp"
    cps = " · ".join(sorted({cp for _c, cp in z["colonias"]}))
    preguntas = z["faqs"]
    return {
        "tipo": TIPO,
        "meta": {
            "title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
            "canonical": url,
            "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                   ("og:description", descripcion), ("og:image", imagen), ("og:locale", "es_MX")),
            "twitter": (("twitter:card", "summary_large_image"),),
        },
        "migas": (("Inicio", "/"), (f"Jardinería en {z['nombre']}", None)),
        "portada": {
            "compacta": True,
            "kicker": f"{z['municipio']}, Tamaulipas · CP {cps}",
            "h1": f'{z["h1"]} <span class="vt-serif">{z["accent"]}</span>',
            "lede": z["lede"],
            "etiqueta": {"codigo": f"Zona · {corto}", "aviso": "Con IVA", "nombre": "Pasto instalado",
                         "antes": "desde", "monto": INSTALADO, "unidad": "/m²",
                         "filas": (("Mantenimiento", f"desde {MANTENIMIENTO}/mes"),
                                   ("Diseño", f"desde {dinero(P['diseno'])}"))},
            "mensaje": mensaje,
            "tambien": f'{datos.VISITA_COSTO_CORTO} · <a href="#precios">servicios y precios</a>',
            "foto": _foto(slug),
        },
        "precios": {
            "titulo": 'Servicios y precios <span class="vt-serif">con IVA</span>',
            "lede": f"Lo que hacemos en {corto}, con el precio de la lista oficial.",
            "filas": lista_precios.ZONA, "caption": f"Precios {datos.ANIO} con IVA.",
            "nota": f'{datos.ANTICIPO} <a href="/precios">Ver la lista completa</a>.',
        },
        "retos": {"titulo": 'Lo que pide un jardín <span class="vt-serif">en esta zona</span>',
                  "items": tuple({"titulo": t, "texto": x} for t, x in z["retos"])},
        "colonias": {"titulo": f'Colonias que atendemos <span class="vt-serif">en {corto}</span>',
                     "lede": f"{datos.VISITA_COSTO} Si tu colonia está cerca y no aparece, también te atendemos.",
                     "items": z["colonias"], "municipio": z["municipio"]},
        "faq": {"titulo": f'Preguntas frecuentes <span class="vt-serif">en {corto}</span>', "preguntas": preguntas},
        "cobertura": {"titulo": "Otras zonas donde trabajamos",
                      "lede": "Cada zona tiene su página con sus colonias; fuera de ellas atendemos por proyecto.",
                      "zonas": _otras(slug), "por_proyecto": datos.ZONAS_POR_PROYECTO},
        "cierre": {"titulo": f'Cotiza tu jardín <span class="vt-serif">en {corto}</span>',
                   "lede": ("Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. "
                            f"{datos.PROMESA} y, si hace falta, agendamos una visita para medir. {datos.VISITA_COSTO} "
                            'O <a href="/vivero-tampico">visita el vivero</a>.'),
                   "mensaje": mensaje},
        "jsonld": {
            "migas": {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": f"Jardinería en {z['nombre']}", "item": url}]},
            "servicio": {
                "@type": "Service", "@id": f"{url}#servicio", "name": f"Jardinería en {z['nombre']}",
                "serviceType": "Jardinería, pasto en rollo, diseño y mantenimiento de jardines", "provider": NEGOCIO,
                "areaServed": [{"@type": "Place", "name": f"{c}, {z['municipio']}, Tamaulipas",
                                "address": {"@type": "PostalAddress", "addressLocality": z["municipio"],
                                            "postalCode": cp, "addressRegion": "Tamaulipas", "addressCountry": "MX"}}
                               for c, cp in z["colonias"]],
                "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(P["pasto_instalado_m2"]),
                           "unitText": "m²"},
            },
        },
    }


def paridad(slug):
    """Madero: "A minutos del vivero" pasa a "El vivero está en Ciudad Madero" (sin distancias ni tiempos)."""
    reemplazos = {"A minutos del vivero": "El vivero está en Ciudad Madero"} if slug == "jardineria-ciudad-madero" else {}
    return {"reemplazos": reemplazos, "retirados": {}}


def pagina(slug):
    return SimpleNamespace(CONTENIDO=contenido(slug), PARIDAD=paridad(slug))
EOF
```

- [ ] **Step 3: Registrar las zonas y dejar de escribirlas desde `tools/pasto`**

En `tools/site/generar.py`, reemplaza el final de `PAGINAS`

```python
    "ciudad", lambda k: f"/pasto-sintetico/envio/{k}", lambda k: f"pasto-sintetico/envio/{k}/index.html", "tienda_guia")
```

por

```python
    "ciudad", lambda k: f"/pasto-sintetico/envio/{k}", lambda k: f"pasto-sintetico/envio/{k}/index.html", "tienda_guia"
) + _varias("zona", lambda k: f"/{k}", lambda k: f"{k}/index.html", "zona")
```

En `tools/pasto/build.py`, borra la línea `from zonas import ZONAS, build_zona` y, en `main()`, las dos líneas

```python
    for slug, zona in ZONAS.items():
        write(ROOT.parent / slug / "index.html", build_zona(slug, zona))
```

(`zonas.py` se borra en la Tarea 9 con sus pruebas, que todavía lo importan.)

- [ ] **Step 4: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /jardineria-lomas-de-rosales-tampico /jardineria-country-club-tampico /jardineria-aguila-tampico /jardineria-lomas-del-chairel-tampico /jardineria-ciudad-madero /jardineria-altamira | grep -vc ": ok"
(cd tools/site && python3 -m unittest tests.test_zona tests.test_generar tests.test_zonas_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_enlaces tests.test_anclas tests.test_paginas 2>&1 | tail -1)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1)
```

Expected: `plantillas: 6 de 47 páginas escritas`; la segunda corrida `plantillas: 0 de 47 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `6` (solo las líneas `== /ruta`: las seis categorías en `ok` en las 6 zonas, verificado); `OK`; `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/site/plantillas/zona.py tools/site/contenido/zona.py tools/site/generar.py tools/pasto/build.py tools/site/tests/test_zona.py tools/site/tests/test_generar.py tools/site/tests/test_zonas_reglas.py public/jardineria-*/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(zonas): plantilla zona y las 6 /jardineria-* con precios de datos.py, sin distancias y con las fotos de main" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Hoja `terra-precios.css` y su cableado

**Files:**
- Create: `public/css/terra-precios.css`
- Modify: `tools/site/activos.py`, `tools/site/partials.py`, `tools/site/shell.py`, `vercel.json`
- Test: `tools/site/tests/test_terra_precios_css.py`, `tools/site/tests/test_partials.py`, `tools/site/tests/test_activos.py`, `tools/site/tests/test_vercel.py`

- [ ] **Step 1: Pruebas en rojo**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/tests/test_terra_precios_css.py <<'EOF'
"""terra-precios.css: hoja de /precios (Etapa 2g). Todo bajo .vt-precios, sin colores literales ni !important, tablas de
varias columnas compactas en celular y presupuesto propio (terra.css está a ~0.5 KB de su tope)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-precios.css"


class TerraPreciosCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_precios(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-precios ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_tablas_compactas_y_anclas_bajo_el_menu(self):
        self.assertIn(".vt-precios .vt-tabla--compacta td{text-align:right;", self.css)
        self.assertIn(".vt-precios :is(section,li)[id]{scroll-margin-top:72px}", self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 2 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 1024)


if __name__ == "__main__":
    unittest.main()
EOF
```

En `tools/site/tests/test_partials.py`, en `test_paginas_de_plantas_cargan_su_hoja`, agrega `"terra-precios.css": "/css/terra-precios.g.css",` al diccionario `urls` (después de `"terra-materiales.css": …`) y, al final del método:

```python
        self.assertIn('<link rel="stylesheet" href="/css/terra-precios.g.css">', partials.head(urls, False, precios=True))
        self.assertNotIn("terra-precios", partials.head(urls, False, materiales=True))
```

En `tools/site/tests/test_activos.py`, después de la línea que escribe `terra-materiales.css` en `setUp`, agrega `        (self.pub / "css" / "terra-precios.css").write_text(".vt-precios .vt-x{}", encoding="utf-8")`, y en la tupla de hojas de la prueba de minificación agrega `"terra-precios.css"`. En `tools/site/tests/test_vercel.py`, en `HASH`, cambia `terra-materiales|legacy-fixes` por `terra-materiales|terra-precios|legacy-fixes`.

Run: `cd tools/site && python3 -m unittest tests.test_terra_precios_css tests.test_partials tests.test_activos tests.test_vercel 2>&1 | tail -3`
Expected: `FAILED` (no existe la hoja ni el parámetro `precios`).

- [ ] **Step 2: La hoja**

```bash
cd ~/dev/viverosterra-e2g
cat > public/css/terra-precios.css <<'EOF'
/* terra-precios.css: hoja de /precios (Etapa 2g). Solo se carga en <body class="vt-pagina vt-precios"> (shell.py);
   todo bajo .vt-precios y con los tokens de terra.css. */

/* Tablas de varias columnas (pasto sintético por modelo y mensualidades): en celular siguen siendo tabla, compacta, en
   vez de una tarjeta por renglón (9 modelos apilaban ~1,400 px). Los precios a la derecha, con cifras tabulares. */
.vt-precios .vt-tabla--compacta td{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.vt-precios .vt-tabla--compacta thead th:not(:first-child){text-align:right}
.vt-precios .vt-tabla--compacta tbody th a{font-weight:700}
@media (max-width:640px){
  .vt-precios .vt-tabla--compacta :is(th,td){padding:10px 8px;font-size:var(--vt-text-sm)}
  .vt-precios .vt-tabla--compacta thead th{font-size:11px;letter-spacing:.02em}
}

/* Lista de precios: el precio queda en el mismo renglón que la unidad (como en materiales) y el "según cotización" de la
   poda, debajo del precio, sin cortar la columna. */
.vt-precios .vt-tabla--precios :is(th,td){vertical-align:baseline}
@media (max-width:640px){
  .vt-precios .vt-tabla--precios tr{align-items:baseline}
  .vt-precios .vt-tabla--precios td{grid-row:2}
}

/* Anclas (#pasto, #mensualidades, #garantia-plantas…): al llegar desde otra página o desde "Ver la lista", la sección no
   queda bajo el menú fijo. */
.vt-precios :is(section,li)[id]{scroll-margin-top:72px}
EOF
```

- [ ] **Step 3: El cableado (como `terra-materiales.css` en 2f)**

- `tools/site/activos.py`: en `FUENTES`, después de `"terra-materiales.css": "css/terra-materiales.css",`, agrega `    "terra-precios.css": "css/terra-precios.css",`; en el docstring, `terra-materiales.css,\nlegacy-fixes.css` pasa a `terra-materiales.css,\nterra-precios.css, legacy-fixes.css`.
- `tools/site/partials.py`: la firma pasa a `def head(urls, legacy, tienda=False, plantas=False, materiales=False, precios=False):`; al docstring, después de `terra-materiales.css.`, agrega ` Con precios=True\n    (<body class="vt-pagina vt-precios">, Etapa 2g), terra-precios.css.`; después del `if materiales:` agrega

```python
    if precios:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-precios.css"]}">')
```

- `tools/site/shell.py`: debajo de `MATERIALES = '<body class="vt-pagina vt-materiales">'` agrega `PRECIOS = '<body class="vt-pagina vt-precios">'`, y en `aplicar()` la llamada termina `materiales=MATERIALES in html, precios=PRECIOS in html),`.
- `vercel.json`: en la regla de caché inmutable, `terra-plantas|terra-materiales|legacy-fixes` pasa a `terra-plantas|terra-materiales|terra-precios|legacy-fixes`.

- [ ] **Step 4: En verde, build y presupuesto**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
(cd tools/site && python3 -m unittest tests.test_terra_precios_css tests.test_partials tests.test_activos tests.test_vercel tests.test_shell 2>&1 | tail -1)
git status --short | grep -v '\.html$'
```

El build va primero: `test_partials` comprueba que exista la copia con hash, que solo aparece al publicar. Expected: `plantillas: 0 de 47` y `shell: 0 de 108` (ninguna página tiene aún `vt-precios`); `OK`; `public/css/terra-precios.<hash>.css` nuevo y `tools/site/activos.json` con la clave `terra-precios.css`, además de los archivos editados. La hoja minificada pesa 691 B, 315 B con gzip (tope de la prueba: 2 KB y 1 KB).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add public/css/terra-precios.css public/css/terra-precios.*.css tools/site/activos.json tools/site/activos.py tools/site/partials.py tools/site/shell.py vercel.json tools/site/tests/test_terra_precios_css.py tools/site/tests/test_partials.py tools/site/tests/test_activos.py tools/site/tests/test_vercel.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(precios): hoja terra-precios.css con tablas compactas en celular, con hash y caché inmutable" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Plantilla `precios` y `/precios`

**Files:**
- Create: `tools/site/plantillas/precios.py`, `tools/site/contenido/precios.py`
- Modify: `tools/site/generar.py`, `tools/pasto/build.py`
- Test: `tools/site/tests/test_precios_pagina.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_zonas_reglas.py`

- [ ] **Step 1: Pruebas en rojo**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/tests/test_precios_pagina.py <<'EOF'
"""Plantilla precios (Etapa 2g): sin un número escrito a mano, la misma respuesta de pasto que la home y pasto en rollo,
vigencia de datos.py, anclas estables, mensualidades con la fórmula oficial y el simulador, y garantías con condición."""
import ast
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402

HTML = (paginas.PUBLIC / "precios" / "index.html").read_text(encoding="utf-8")
FUENTES = [Path(__file__).resolve().parents[1] / p for p in
           ("contenido/precios.py", "contenido/lista_precios.py", "contenido/zona.py", "plantillas/precios.py",
            "plantillas/zona.py", "componentes_zonas.py")]


def literales(fuente):
    """Cadenas literales del código (sin docstrings, sin comentarios y sin el mapa PARIDAD, que nombra lo retirado)."""
    arbol = ast.parse(fuente.read_text(encoding="utf-8"))
    fuera = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef)) and ast.get_docstring(nodo) is not None:
            fuera.add(id(nodo.body[0].value))
        if isinstance(nodo, ast.Assign) and any(getattr(t, "id", "") == "PARIDAD" for t in nodo.targets):
            fuera.update(id(n) for n in ast.walk(nodo.value))
    return [n.value for n in ast.walk(arbol)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in fuera]


def grafo():
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))["@graph"]


class PreciosTest(unittest.TestCase):
    def test_registrada_con_su_plantilla_y_su_hoja(self):
        self.assertIn(("/precios", "precios/index.html", "precios", "precios"), generar.PAGINAS)
        self.assertIn('<body class="vt-pagina vt-precios">', HTML)
        self.assertIn("/css/terra-precios.", HTML)
        for viejo in ("tienda-pasto.css", "fonts.googleapis", "hub-hero"):
            self.assertNotIn(viejo, HTML)

    def test_ningun_precio_escrito_a_mano_en_el_codigo(self):
        """Aceptación de la hoja de ruta: los números salen de datos.py, data.py o mensualidades.py."""
        for fuente in FUENTES:
            with self.subTest(fuente=fuente.name):
                self.assertEqual([t for t in literales(fuente) if re.search(r"\$\s?\d", t)], [])

    def test_misma_respuesta_de_pasto_que_home_y_pasto_en_rollo(self):
        faq = next(n for n in grafo() if n["@type"] == "FAQPage")
        self.assertEqual(faq["mainEntity"][0]["name"], "¿Cuánto cuesta el pasto en rollo en Tampico?")
        self.assertEqual(faq["mainEntity"][0]["acceptedAnswer"]["text"], datos.RESPUESTA_PRECIO_PASTO)

    def test_vigencia_visible_y_en_el_json_ld(self):
        self.assertIn(f"vigente desde {datos.VIGENCIA_PRECIOS}", paridad.texto(HTML))
        pagina = next(n for n in grafo() if n["@type"] == "WebPage")
        self.assertEqual(pagina["dateModified"], datos.VIGENCIA_PRECIOS_ISO)

    def test_anclas_estables(self):
        for ancla in ("pasto", "servicios", "sintetico", "materiales", "plantas", "mensualidades", "garantias",
                      "garantia-pasto", "garantia-plantas", "preguntas"):
            with self.subTest(ancla=ancla):
                self.assertEqual(HTML.count(f'id="{ancla}"'), 1)
        self.assertIn('href="#pasto"', HTML)

    def test_mensualidades_con_simulador_y_contado_sin_recargo(self):
        self.assertIn("tarjeta en una sola exhibición) es el precio más bajo", HTML)
        self.assertIn('<script src="/js/vt-mensualidades.js" defer></script>', HTML)
        self.assertIn('<script src="/js/vt-simulador.js" defer></script>', HTML)
        self.assertIn('data-simulador data-servicio="mi jardín"', HTML)
        self.assertIn('href="/politicas#mensualidades"', HTML)
        self.assertIn(datos.ANTICIPO, HTML)
        self.assertNotRegex(HTML.lower(), r"\brecargo|meses sin|sin intereses|\bmsi\b")

    def test_catalogo_sin_precios_sin_confirmar(self):
        catalogo = next(n for n in grafo() if n["@type"] == "OfferCatalog")
        nombres = [o["name"] for o in catalogo["itemListElement"]]
        self.assertFalse(any("rmol" in n or "Piedra" in n for n in nombres))
        tezontle = next(o for o in catalogo["itemListElement"] if o["name"].startswith("Tezontle"))
        self.assertEqual(tezontle["priceSpecification"]["minPrice"], datos.PRECIOS["tezontle_costal"])
        self.assertNotIn("InStock", HTML)

    def test_garantias_con_su_condicion(self):
        self.assertIn("en las plantas que sembramos nosotros", HTML)
        self.assertIn("siguiendo el protocolo de riego.<", HTML)


if __name__ == "__main__":
    unittest.main()
EOF
```

En `test_generar.test_paginas_registradas_tienen_contexto`, cambia `"/piedra-bola-rio-tampico", "/pasto-sintetico", "/pasto-sintetico/perros"]` por `"/piedra-bola-rio-tampico", "/precios", "/pasto-sintetico", "/pasto-sintetico/perros"]`. En `test_zonas_reglas.py`, `PENDIENTES = frozenset({"/precios"})` pasa a `PENDIENTES = frozenset()`.

Run: `cd tools/site && python3 -m unittest tests.test_precios_pagina tests.test_generar tests.test_zonas_reglas 2>&1 | tail -3`
Expected: `FAILED` (o `ERROR` por `contenido/precios.py` que falta).

- [ ] **Step 2: La plantilla y el contenido**

```bash
cd ~/dev/viverosterra-e2g
cat > tools/site/plantillas/precios.py <<'EOF'
"""Plantilla de la lista de precios (spec §3.3): ruta visible → H1 con la respuesta directa, la vigencia y el precio
ancla en la etiqueta, y CTA → una tabla por línea (pasto natural, servicios, pasto sintético por modelo, materiales y
plantas), cada una con columna Unidad y generada de datos.py → mensualidades (plazos, mínimos, total frente a contado,
aviso del banco, anticipo y el simulador de vt-simulador.js) → garantías con anclas estables (#garantia-pasto,
#garantia-plantas) → preguntas → CTA final. Las secciones conservan sus id de main (#pasto, #servicios, #sintetico,
#materiales, #plantas, #mensualidades, #preguntas). Página: /precios (tools/site/contenido/precios.py).
<body class="vt-pagina vt-precios">: el shell agrega terra-precios.css."""
import componentes as c
import componentes_zonas as cz
from plantillas import base

CONTEXTO = "https://schema.org"
CLASE_BODY = "vt-pagina vt-precios"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-simulador.js")


def _seccion(s, numero):
    cuerpo = cz.tabla_sintetico() if s.get("modelos") else cz.lista(s["filas"], s["caption"], s["concepto"])
    cuerpo += f'<p class="vt-promesa">{s["nota"]}</p>'
    return c.bloque(numero, s["rotulo"], f"vt-h-{s['id']}", s["titulo"], cuerpo, lede=s.get("lede"),
                    tinte=numero % 2 == 0, id_seccion=s["id"])


def _pago(p, numero, tipo):
    izquierda = (f'<p class="vt-lede">{p["lede"]}</p>{cz.tabla_mensualidades()}'
                 f'<p class="vt-promesa">{p["nota"]}</p><p class="vt-promesa">{p["anticipo"]}</p>')
    derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], tipo)
    return c.bloque_dos(numero, "Formas de pago", "vt-h-pago", p["titulo"], izquierda, derecha, id_seccion="mensualidades")


def render(k):
    tipo = k["tipo"]
    secciones = [c.portada(k["portada"], tipo, k["migas"])]
    numero = 0
    for numero, s in enumerate(k["secciones"], 1):
        secciones.append(_seccion(s, numero))
    g, f, ci = k["garantias"], k["faq"], k["cierre"]
    secciones += [
        _pago(k["pago"], numero + 1, tipo),
        c.bloque(numero + 2, "Garantías", "vt-h-garantias", g["titulo"], cz.garantias(g["items"]), tinte=True,
                 id_seccion="garantias"),
        c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), id_seccion="preguntas"),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    j = k["jsonld"]
    grafo = [j["migas"], j["pagina"], j["catalogo"], c.faq_jsonld(f["preguntas"])]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS,
                          clase_body=CLASE_BODY)
EOF
cat > tools/site/contenido/precios.py <<'EOF'
"""Contenido de /precios: la lista de precios de todo Viveros Terra. Solo datos: la plantilla es plantillas/precios.py.

Ningún número escrito a mano (aceptación de la hoja de ruta 2g): los precios salen de datos.PRECIOS (renglones en
contenido/lista_precios.py), el sintético por modelo de tools/pasto/data.py y las mensualidades de
tools/pasto/mensualidades.py (la fórmula de vt-mensualidades.js). La respuesta a "¿cuánto cuesta el pasto en rollo en
Tampico?" es datos.RESPUESTA_PRECIO_PASTO, la misma de la home y de pasto en rollo (spec §7.3). Lo que el dueño no
confirmó va "según cotización": tierra preparada ($100 en main), camión de tierra ("desde $5,000"), mármol ($250 el
saco) y piedra bola. Título, descripción, canonical y Open Graph como estaban. PARIDAD: tests/test_paridad.py.
"""
import componentes as c  # primero: agrega tools/pasto al sys.path (data y mensualidades)
import data
import datos
import mensajes_paginas
import mensualidades
from contenido import lista_precios as lp

dinero = c.dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/precios"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
IMG = "/img/precios/pasto-rollo-jardin"
SOLO, INSTALADO = dinero(P["pasto_solo_m2"]), dinero(P["pasto_instalado_m2"])
MANTENIMIENTO, DISENO = dinero(P["mantenimiento_mes"]), dinero(P["diseno"])
SINTETICO = dinero(lp.SINTETICO_MIN)
SINT_MIN, SINT_MAX = (dinero(x) for x in P["sintetico_instalado_m2"])
MENSAJE = mensajes_paginas.PRECIOS
TITULO = "Precios de jardinería en Tampico 2026: pasto, diseño y mantenimiento | Viveros Terra"
DESCRIPCION = (f"Pasto San Agustín {SOLO}/m² o instalado desde {INSTALADO}/m², mantenimiento desde {MANTENIMIENTO}/mes, "
               f"diseño desde {DISENO} y pasto sintético desde {SINTETICO}/m². Precios con IVA en Tampico, Madero y "
               "Altamira.")
ENLACES_FAQ = {
    "sintetico": ' Ve los <a href="/pasto-sintetico">9 modelos con precio</a>.',
    "garantia": ' Lee las <a href="/politicas#garantia-plantas">condiciones de la garantía</a>.',
}

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Los precios incluyen IVA?",
     f"Sí. Todos los precios de esta página incluyen IVA. Damos factura {datos.FACTURA} a persona física o moral y "
     f"tenemos registro REPSE {datos.REPSE} para contratos con empresas."),
    ("¿Por qué algunos precios dicen «desde»?",
     "Porque el total depende de los metros, del estado del terreno y del acceso a la obra. En la visita medimos y te "
     f"damos el precio cerrado antes de empezar. {datos.VISITA_COSTO} Lo que dice «según cotización» depende de la "
     "medida, la cantidad o el lugar de entrega: te lo cotizamos por WhatsApp."),
    ("¿Cuánto cuesta el pasto sintético en Tampico?",
     f"El material cuesta desde {SINTETICO}/m² en rollo completo y el pasto instalado de {SINT_MIN} a {SINT_MAX}/m² "
     "según el modelo, con material y colocación. La preparación del terreno se cotiza aparte." + ENLACES_FAQ["sintetico"]),
    ("¿Las plantas y palmas tienen garantía?",
     f"Sí: {datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} No cubre falta de riego, cambio de lugar, daños "
     "por mascotas ni clima extremo." + ENLACES_FAQ["garantia"]),
    ("¿Cada cuánto cambian estos precios?",
     f"Revisamos la lista cada temporada. Esta versión rige desde {datos.VIGENCIA_PRECIOS}. Si algo cambió, vale el "
     "precio que te confirmemos por WhatsApp."),
)


def _oferta(nombre, precio, ruta, unidad=None, desde=False):
    """Offer del catálogo con el seller por @id a #negocio; con unidad, su UnitPriceSpecification (minPrice si es
    "desde"). Solo precios de datos.py: nunca InStock."""
    o = {"@type": "Offer", "name": nombre, "price": str(precio), "priceCurrency": "MXN", "url": f"{SITE}{ruta}",
         "seller": NEGOCIO}
    if unidad:
        spec = {"@type": "UnitPriceSpecification", "priceCurrency": "MXN", "unitText": unidad}
        spec.update({"minPrice": precio} if desde else {"price": str(precio)})
        o["priceSpecification"] = spec
    return o


CATALOGO = {
    "@type": "OfferCatalog", "@id": f"{URL}#lista", "name": "Lista de precios de Viveros Terra",
    "itemListElement": [
        _oferta("Pasto San Agustín en rollo, solo el pasto", P["pasto_solo_m2"], "/pasto-en-rollo-tampico", "m²"),
        _oferta("Pasto San Agustín instalado", P["pasto_instalado_m2"], "/pasto-en-rollo-tampico", "m²"),
        _oferta(f"Pasto San Agustín al mayoreo, desde {P['pasto_mayoreo_minimo_m2']} m²", P["pasto_mayoreo_m2"],
                "/mayoreo-pasto-tampico", "m²"),
        _oferta("Mantenimiento de jardín mensual", P["mantenimiento_mes"], "/mantenimiento-jardines-tampico", "mes"),
        _oferta("Diseño de jardín, Plan Terra Esencial", P["diseno"], "/diseno-jardines-tampico"),
        _oferta("Diseño de jardín, Plan Terra Completo", P["diseno_completo"], "/diseno-jardines-tampico"),
        _oferta("Diseño de jardín, Plan Terra Premium", P["diseno_premium"], "/diseno-jardines-tampico"),
        _oferta("Pasto sintético, material en rollo", lp.SINTETICO_MIN, "/pasto-sintetico", "m²"),
        _oferta("Tierra negra vegetal, costal", P["tierra_negra_costal"], "/tierra-negra-vegetal-tampico"),
        _oferta("Tezontle rojo, costal", P["tezontle_costal"], "/tezontle-rojo-tampico", "costal", desde=True),
        _oferta("Palmas, tamaño chico", P["palma_desde"], "/palmas-tropicales-tampico"),
    ],
}

CONTENIDO = {
    "tipo": "precios",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large",
        "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", f"{SITE}{IMG}.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "migas": (("Inicio", "/"), ("Precios", None)),
    "portada": {
        "compacta": True,
        "kicker": f"Lista de precios · vigente desde {datos.VIGENCIA_PRECIOS}",
        "h1": 'Precios de jardinería en Tampico <span class="vt-serif">2026, con IVA</span>',
        "lede": (f"En Tampico, Madero y Altamira, el pasto San Agustín cuesta {SOLO}/m² solo el pasto y desde "
                 f"{INSTALADO}/m² instalado. El mantenimiento de jardín cuesta desde {MANTENIMIENTO}/mes, el diseño desde "
                 f"{DISENO} y el pasto sintético desde {SINTETICO}/m²."),
        "etiqueta": {"codigo": f"Lista · {datos.VIGENCIA_PRECIOS}", "aviso": "Con IVA", "nombre": "Pasto San Agustín",
                     "antes": "solo el pasto", "monto": SOLO, "unidad": "/m²",
                     "filas": (("Instalado", f"desde {INSTALADO}/m²"), ("Mantenimiento", f"desde {MANTENIMIENTO}/mes"),
                               ("Pasto sintético", f"desde {SINTETICO}/m²"))},
        "mensaje": MENSAJE,
        "tambien": f'<a href="#pasto">Ver la lista</a> · factura {datos.FACTURA} · REPSE {datos.REPSE}',
        "foto": {"src": f"{IMG}-sm.webp", "srcset": f"{IMG}-sm.webp 560w, {IMG}.webp 960w",
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1185, "numero": 1,
                 "alt": "Trabajador de Viveros Terra descargando pasto San Agustín en rollo de la camioneta",
                 "lugar": "Pasto San Agustín en rollo", "etapa": "Recién cortado"},
    },
    "secciones": (
        {"id": "pasto", "rotulo": "Pasto natural", "titulo": 'Pasto San Agustín <span class="vt-serif">en rollo</span>',
         "filas": lp.PASTO, "concepto": "Producto", "caption": f"Precios {datos.ANIO} con IVA.",
         "nota": ("Solo el pasto: recoges en el vivero o se cobra la entrega según tu colonia. "
                  '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de riego y garantía</a>.')},
        {"id": "servicios", "rotulo": "Servicios", "titulo": 'Mantenimiento, diseño <span class="vt-serif">y riego</span>',
         "filas": lp.SERVICIOS, "concepto": "Servicio", "caption": f"Precios {datos.ANIO} con IVA.",
         "nota": f"Cotiza por WhatsApp. Contratos con empresas con factura y REPSE {datos.REPSE}."},
        {"id": "sintetico", "rotulo": "Pasto sintético",
         "titulo": 'Pasto sintético <span class="vt-serif">por modelo</span>', "modelos": True,
         "lede": (f"Material por m² según cuánto compres. Instalado en Tampico, Madero y Altamira de {SINT_MIN} a "
                  f"{SINT_MAX}/m² con material y colocación."),
         "nota": (f"Cortes de {data.MIN_SHOWROOM_M2} a 9 m² solo en el showroom. Envío a todo México desde "
                  f"{data.MIN_NACIONAL_M2} m²; el flete se cobra por rollo según tu estado. "
                  '<a href="/pasto-sintetico">Ver la tienda</a> · <a href="/pasto-sintetico-tampico">Instalación en '
                  "Tampico</a>")},
        {"id": "materiales", "rotulo": "Materiales", "titulo": 'Tierra, tezontle <span class="vt-serif">y piedra</span>',
         "filas": lp.MATERIALES, "concepto": "Material", "caption": f"Precios {datos.ANIO} con IVA.",
         "nota": "Recoges en el vivero de Cd. Madero o te lo llevamos en Tampico, Madero y Altamira."},
        {"id": "plantas", "rotulo": "Vivero", "titulo": 'Plantas, palmas <span class="vt-serif">y árboles</span>',
         "filas": lp.PLANTAS, "concepto": "Planta", "caption": f"Precios {datos.ANIO} con IVA.",
         "nota": ('Arma tu lista en el <a href="/catalogo">catálogo</a> y mándala por WhatsApp. '
                  f"{datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} "
                  '<a href="/politicas#garantia-plantas">Ver condiciones</a>.')},
    ),
    "pago": {
        "titulo": 'Mensualidades <span class="vt-serif">con tarjeta</span>',
        "lede": ("El contado (transferencia, efectivo o tarjeta en una sola exhibición) es el precio más bajo. Con "
                 "tarjeta de crédito puedes pagar en 3, 6, 9 o 12 mensualidades; el total es mayor que el de contado y "
                 "siempre te lo mostramos antes de enviarte el link de pago."),
        "anticipo": datos.ANTICIPO,
        "nota": ("Aplica a pasto sintético, pasto natural instalado, instalación de pasto sintético, diseño de jardines y "
                 "sistemas de riego. No aplica a mantenimiento mensual. Tu banco emisor debe aceptar el plan. "
                 '<a href="/politicas#mensualidades">Ver condiciones</a>.'),
        "titulo_sim": "Calcula tu mensualidad",
        # Monto de ejemplo: el mínimo con el que aplican los 4 plazos (el simulador muestra todos).
        "sim": {"servicio": "mi jardín", "monto": mensualidades.minimo_de(12)},
    },
    "garantias": {
        "titulo": 'Garantías <span class="vt-serif">y condiciones</span>',
        "items": (
            {"id": "garantia-pasto", "titulo": f"Pasto San Agustín: arraigo de {datos.ARRAIGO}",
             "texto": datos.GARANTIA_PASTO.replace(" (ver condiciones)", ""),
             "enlace": ("Protocolo de riego y condiciones", "/protocolo-cuidados-pasto-san-agustin")},
            {"id": "garantia-plantas", "titulo": "Plantas y palmas: 30 días",
             "texto": (f"{datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} No cubre falta de riego, cambio de "
                       "lugar, daños por mascotas ni clima extremo."),
             "enlace": ("Condiciones de la garantía de plantas", "/politicas#garantia-plantas")},
        ),
    },
    "faq": {"titulo": 'Preguntas sobre <span class="vt-serif">precios</span>', "preguntas": PREGUNTAS},
    "cierre": {"titulo": '¿Quieres el precio exacto <span class="vt-serif">de tu jardín?</span>',
               "lede": ("Mándanos tu colonia, los metros aproximados y una foto del espacio. "
                        f"{datos.PROMESA} y, si hace falta, agendamos una visita para medir. {datos.VISITA_COSTO}"),
               "mensaje": ("Hola, quiero el precio exacto de mi jardín.\nColonia: ___\nMetros aprox.: ___\n"
                           "Les mando foto del espacio.")},
    "jsonld": {
        "migas": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Precios", "item": URL}]},
        "pagina": {"@type": "WebPage", "@id": URL, "url": URL, "name": "Precios de jardinería en Tampico 2026",
                   "dateModified": datos.VIGENCIA_PRECIOS_ISO, "about": NEGOCIO, "mainEntity": {"@id": f"{URL}#lista"}},
        "catalogo": CATALOGO,
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {
        "$100": ("Tierra preparada a $100 el costal: no está en datos.PRECIOS (el dueño no la confirmó en 2f); va según "
                 "cotización, como en /tierra-negra-vegetal-tampico."),
    },
    "jsonld": {},
}
EOF
```

- [ ] **Step 3: Registrar `/precios` y dejar de escribirla desde `tools/pasto`**

En `tools/site/generar.py`, antes de `("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),` agrega `    ("/precios", "precios/index.html", "precios", "precios"),`. En `tools/pasto/build.py`, borra `from precios import build_precios` y la línea `write(ROOT.parent / "precios" / "index.html", build_precios())`.

- [ ] **Step 4: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /precios
(cd tools/site && python3 -m unittest tests.test_precios_pagina tests.test_generar tests.test_zonas_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_enlaces tests.test_anclas tests.test_paginas tests.test_partials 2>&1 | tail -1)
```

Expected: `plantillas: 1 de 48 páginas escritas`; luego `plantillas: 0 de 48` y `shell: 0 de 108`; las seis categorías en `ok` (verificado; `$100` retirado con motivo en `PARIDAD`); `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/site/plantillas/precios.py tools/site/contenido/precios.py tools/site/generar.py tools/pasto/build.py tools/site/tests/test_precios_pagina.py tools/site/tests/test_generar.py tools/site/tests/test_zonas_reglas.py public/precios/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(precios): plantilla precios con tablas de datos.py, vigencia, mensualidades con simulador y garantías con ancla" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Retirar el HTML de `tools/pasto` y `tienda-pasto.css`

**Files:**
- Delete: `tools/pasto/{common,zonas,precios}.py`, `tools/pasto/tests/{test_precios,test_plan_selector,test_shell_regiones}.py`, `public/css/tienda-pasto.css`
- Modify: `tools/pasto/build.py`, `tools/pasto/feed.py`, `tools/pasto/esquema.py`
- Test: `tools/site/tests/test_limpieza.py`, `tools/site/tests/test_terra_css.py`

- [ ] **Step 1: Prueba en rojo**

En `tools/site/tests/test_limpieza.py`, antes de `def test_ds_store_y_pycache_fuera_de_git(self):`, agrega:

```python
    def test_tienda_pasto_css_y_html_de_tools_pasto_retirados(self):
        """Etapa 2g: /precios y las 6 zonas eran las últimas páginas con tienda-pasto.css y con HTML de tools/pasto."""
        self.assertFalse((RAIZ / "public" / "css" / "tienda-pasto.css").exists())
        for modulo in ("common.py", "precios.py", "zonas.py"):
            with self.subTest(modulo=modulo):
                self.assertFalse((RAIZ / "tools" / "pasto" / modulo).exists())
        con_hoja = [str(p.relative_to(RAIZ)) for p in (RAIZ / "public").rglob("*.html")
                    if "tienda-pasto.css" in p.read_text(encoding="utf-8")]
        self.assertEqual(con_hoja, [])
```

En `tools/site/tests/test_terra_css.py`, reemplaza `CSS_VIEJOS = ("design-system.css", "tailwind.css", "servicios.css", "tienda-pasto.css")` por

```python
# tienda-pasto.css se borró en la Etapa 2g (sus últimas páginas, /precios y las zonas, ya salen de plantillas).
CSS_VIEJOS = ("design-system.css", "tailwind.css", "servicios.css")
```

Run: `cd tools/site && python3 -m unittest tests.test_limpieza 2>&1 | tail -3`
Expected: `FAILED (failures=1)`.

- [ ] **Step 2: Borrar y reescribir**

```bash
cd ~/dev/viverosterra-e2g
git rm -q tools/pasto/common.py tools/pasto/zonas.py tools/pasto/precios.py tools/pasto/tests/test_precios.py tools/pasto/tests/test_plan_selector.py tools/pasto/tests/test_shell_regiones.py public/css/tienda-pasto.css
sed -i '' 's/^from common import GAL, strip_tags$/from esquema import GAL, strip_tags/' tools/pasto/feed.py
cat > tools/pasto/build.py <<'EOF'
"""Genera el feed de Merchant y las URLs de la tienda en el sitemap. Desde la Etapa 2g ya no escribe páginas: la tienda
(hub, 9 fichas, 11 ciudades, perros y sintético en Tampico, Etapa 2b), /precios y las 6 zonas salen de
tools/site/generar.py con sus plantillas. Este paquete sigue siendo la fuente de modelos, zonas de envío y fletes
(data.py) y de la fórmula de mensualidades (mensualidades.py).

Uso: python3 tools/pasto/build.py   (desde la raíz del repo). Para todo el sitio: python3 tools/site/build.py
"""
from pathlib import Path

from ciudades import CIUDADES
from data import MODELOS, SITE
from feed import build_feed
from sitemap import upsert

PUBLIC = Path(__file__).resolve().parents[2] / "public"


def main():
    (PUBLIC / "feed-pasto-sintetico.xml").write_text(build_feed(), encoding="utf-8")
    upsert([f"{SITE}/pasto-sintetico", f"{SITE}/pasto-sintetico/perros"]
           + [f"{SITE}/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
           + [f"{SITE}/pasto-sintetico/{m['slug']}" for m in MODELOS], conservar=True)


if __name__ == "__main__":
    main()
EOF
```

En `tools/pasto/esquema.py`, el segundo párrafo del docstring pasa a `Datos, no HTML: los usan las plantillas de tools/site (fichas, hub, ciudades) y el feed de Merchant (feed.py).`

- [ ] **Step 3: En verde**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
git status --porcelain | grep -v '^D ' | grep -v '^ M tools/'
(cd tools/site && python3 -m unittest tests.test_limpieza tests.test_terra_css tests.test_tienda tests.test_enlaces 2>&1 | tail -1)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
git diff --stat HEAD -- public/feed-pasto-sintetico.xml public/sitemap.xml | tail -1
```

Expected: `plantillas: 0 de 48` y `shell: 0 de 108`; ningún HTML cambiado; `OK`; `Ran 28 tests` y `OK` (lo que probaban los 3 archivos borrados lo cubren `test_componentes_zonas`, `test_precios_pagina` y `test_zona`); feed y sitemap sin cambios (diff vacío).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/pasto/build.py tools/pasto/feed.py tools/pasto/esquema.py tools/site/tests/test_limpieza.py tools/site/tests/test_terra_css.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "refactor(pasto): tools/pasto ya no escribe HTML; se borran common, zonas, precios y tienda-pasto.css" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Pruebas en navegador de zonas y precios

**Files:**
- Test: `tools/site/tests/test_plantillas_navegador.py`

Las 7 páginas entran a las pruebas de plantilla que ya existen (axe de página completa a 375 y 1440, precio y CTA en el primer pantallazo a 375×812, sin desbordar de 320 a 1920, CLS < 0.1) y a la del CTA a 1024×800. Nuevas: el CTA de cada zona con su mensaje y `generate_lead` `zona:hero`, el simulador de `/precios` con los números de la fórmula oficial, tablas compactas a 320 px y anclas que no quedan bajo el menú.

- [ ] **Step 1: Agregar las pruebas**

En `tools/site/tests/test_plantillas_navegador.py`, reemplaza la línea `import datos  # noqa: E402` por

```python
import componentes  # noqa: E402,F401  (agrega tools/pasto al path: mensualidades)
import datos  # noqa: E402
import mensualidades  # noqa: E402
```

reemplaza `CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS + MATERIALES` por

```python
# Etapa 2g: las 6 zonas (plantilla zona) y la lista de precios (plantilla precios, con terra-precios.css).
ZONAS = tuple(f"{ruta}/" for _nombre, ruta in datos.ZONAS)
PRECIOS = "/precios/"
CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS + MATERIALES + ZONAS + (PRECIOS,)
```

en `test_cta_en_la_primera_pantalla_a_1024` cambia `for ruta in SERVICIOS + EMPRESAS + MATERIALES:` por `for ruta in SERVICIOS + EMPRESAS + MATERIALES + ZONAS + (PRECIOS,):`, y agrega a la clase, antes de `def test_cls_bajo_0_1_en_movil(self):`:

```python
    # ---------- Etapa 2g: zonas y precios ----------
    def test_cta_de_zona_manda_su_mensaje_y_generate_lead(self):
        """La portada de cada zona abre el WhatsApp con el mensaje de esa zona (el de main) y lo mide como zona:hero."""
        page = self.pagina(375, 812)
        for ruta in ZONAS:
            page.goto(self.base + ruta, wait_until="load")
            boton = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa')
            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
            boton.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            texto = unquote(boton.get_attribute("href").split("text=", 1)[1])
            with self.subTest(ruta=ruta):
                self.assertEqual(texto, datos.con_firma(mensajes_paginas.ZONAS[ruta.rstrip("/")]))
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "zona:hero",
                                                          "service": "jardin"}], eventos)

    def test_simulador_de_precios_con_la_formula_oficial(self):
        """El simulador de /precios (vt-simulador.js + vt-mensualidades.js) muestra los 4 plazos con el total y la
        mensualidad de tools/pasto/mensualidades.py para el monto de ejemplo."""
        page = self.pagina()
        page.goto(self.base + PRECIOS, wait_until="load")
        monto = int(page.input_value("[data-sim-monto]"))
        texto = page.locator("[data-sim-list]").inner_text()
        for p in mensualidades.planes(monto):
            if p["plazo"] and p["disponible"]:
                with self.subTest(plazo=p["plazo"]):
                    self.assertIn(f"${p['mensualidad']:,}", texto)
                    self.assertIn(f"${p['total']:,}", texto)

    def test_tablas_de_precios_compactas_en_celular(self):
        """Sintético por modelo y mensualidades siguen siendo tabla a 320 px (no una tarjeta por renglón) y no se salen."""
        page = self.pagina(320, 800)
        page.goto(self.base + PRECIOS, wait_until="load")
        for tabla in page.locator(".vt-tabla--compacta").all():
            caja = tabla.bounding_box()
            with self.subTest(tabla=tabla.locator("caption").inner_text()[:30]):
                self.assertEqual(tabla.evaluate("t => getComputedStyle(t).display"), "table")
                self.assertLessEqual(caja["x"] + caja["width"], 320)

    def test_anclas_de_precios_llevan_a_su_seccion(self):
        """#garantia-plantas y #mensualidades desde otra página: la sección queda a la vista y no bajo el menú."""
        page = self.pagina(375, 812)
        for ancla in ("mensualidades", "garantia-plantas", "pasto"):
            page.goto(f"{self.base}{PRECIOS}#{ancla}", wait_until="load")
            arriba = page.locator(f"#{ancla}").evaluate("e => e.getBoundingClientRect().top")
            menu = page.locator(".vt-head").evaluate("e => e.getBoundingClientRect().bottom")
            with self.subTest(ancla=ancla):
                self.assertGreaterEqual(arriba, menu - 1)
                self.assertLess(arriba, 812)
```

- [ ] **Step 2: Correrlas**

Run: `cd tools/site && python3 -m unittest tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `OK` (verificado: las 7 páginas en axe a 375 y 1440, sin desbordar de 320 a 1920, primer pantallazo y CLS). Los `BrokenPipeError` del servidor local que salen entre las pruebas son ruido.

- [ ] **Step 3: Consola limpia en las 108 páginas y nunca dos barras**

Run: `cd tools/site && python3 -m unittest tests.test_navegador tests.test_tienda_navegador 2>&1 | tail -3`
Expected: `OK` (incluye `test_consola_limpia_en_todas_las_paginas`, el axe del shell en `/precios/` y `/jardineria-altamira/` y `test_nunca_dos_barras_fijas_abajo_a_375`).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2g
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): zonas y precios con axe, desborde, primer pantallazo, mensaje de zona, simulador y anclas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Verificación final y puertas de revisión (merge y push los hace el controlador)

**Files:** `public/sitemap.xml` (lastmod) y las correcciones de los revisores, cada una con su prueba y su commit.

- [ ] **Step 1: `lastmod` de las 7 páginas**

```bash
cd ~/dev/viverosterra-e2g
HOY=$(date +%F)
for r in jardineria-lomas-de-rosales-tampico jardineria-country-club-tampico jardineria-aguila-tampico jardineria-lomas-del-chairel-tampico jardineria-ciudad-madero jardineria-altamira precios; do
  perl -0pi -e "s#(<loc>https://www\.viverosterra\.com/$r</loc>\s*<lastmod>)[^<]*#\${1}$HOY#" public/sitemap.xml
done
git diff --stat public/sitemap.xml
git add public/sitemap.xml
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore(sitemap): lastmod de las 6 zonas y precios" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `1 file changed, 7 insertions(+), 7 deletions(-)`.

- [ ] **Step 2: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 48 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `OK` (`Ran 605 tests` en el prototipo); `Ran 28 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 67` y `ℹ fail 0`.

- [ ] **Step 3: Paridad, reglas y palabras a la vista**

```bash
cd ~/dev/viverosterra-e2g
python3 tools/site/paridad.py informe /jardineria-lomas-de-rosales-tampico /jardineria-country-club-tampico /jardineria-aguila-tampico /jardineria-lomas-del-chairel-tampico /jardineria-ciudad-madero /jardineria-altamira /precios | grep -vc ": ok"
(cd tools/site && python3 -m unittest tests.test_reglas tests.test_consistencia tests.test_paridad tests.test_zonas_reglas tests.test_anclas tests.test_zona tests.test_precios_pagina tests.test_contenido 2>&1 | tail -1)
grep -oiE "oasis|gratis|sin cargo|instock|disponibilidad|minutos del|llegamos en|el mejor|l[ií]der|m[aá]s vendid|en nuestro vivero|\\\$100\b|\\\$5,000 |saco \\\$|tienda-pasto|fonts.googleapis|hub-hero" \
  public/{jardineria-lomas-de-rosales-tampico,jardineria-country-club-tampico,jardineria-aguila-tampico,jardineria-lomas-del-chairel-tampico,jardineria-ciudad-madero,jardineria-altamira,precios}/index.html | sort | uniq -c
```

Expected: `7` (solo las líneas `== /ruta`); `OK`; el `grep` vacío.

- [ ] **Step 4: Lighthouse móvil**

```bash
cd ~/dev/viverosterra-e2g
(cd public && python3 -m http.server 8770 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in jardineria-lomas-de-rosales-tampico jardineria-ciudad-madero jardineria-altamira precios; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8770/$r/" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2g-lh-$r.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2g-lh-$r.json"
done
pkill -f "http.server 8770"
```

Expected por página: Performance ≥ 90, Accessibility ≥ 95 (≥ 98 es la meta del cierre de la Etapa 2 en 2i), CLS < 0.1, LCP < 2.5 s (la foto de portada precargada). CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. Lomas de Rosales y Altamira tienen la foto más alta (960×1574 y 793×1190): si el LCP pasa de 2.5 s, anota valor y causa (regla de fotos: no se recomprimen).

- [ ] **Step 5: Capturas a 320, 375, 768, 1024, 1440 y 1920 con el viewport real de Playwright**

```bash
cd ~/dev/viverosterra-e2g/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
rutas = ('jardineria-lomas-de-rosales-tampico/', 'jardineria-country-club-tampico/', 'jardineria-aguila-tampico/',
         'jardineria-lomas-del-chairel-tampico/', 'jardineria-ciudad-madero/', 'jardineria-altamira/', 'precios/')
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in rutas:
        for w in (320, 375, 768, 1024, 1440, 1920):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.screenshot(path=f"/tmp/vt-e2g-{r.strip('/')}-{w}.png", full_page=True)
            p.close()
    b.close()
srv.shutdown()
print(len(rutas) * 6, 'capturas')
PY
```

Expected: `42 capturas`. Revisa a mano: etiqueta con precio y CTA en el primer pantallazo a 375 (en `/precios` el botón queda justo arriba del borde a 375×812: si se corta, acorta la entrada, no la etiqueta); el recorte de las fotos altas (Lomas de Rosales, Águila, Altamira) sin perder lo importante tras quitar el `object-position` de main; tablas de precios con "Según cotización" en dos renglones a 320; la poda con "desde $500" y "según cotización" debajo; sintético y mensualidades en tabla compacta a 320; el simulador junto a la tabla desde 1024; garantías con su enlace; "Otras zonas" en dos o tres columnas; cierre legible.

- [ ] **Step 6: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega la rama en verde y un resumen (`git log --oneline main..feat/etapa-2g`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2g --stat`, `plantillas/{zona,precios}.py`, `componentes_zonas.py`, `contenido/{zona,precios,lista_precios}.py`, `terra-precios.css`, la vista previa de Vercel, `/tmp/vt-e2g-*.png`, los JSON de Lighthouse, `paridad.py informe` y el spec (§3.3, §5, §6.5, §7.3, §8, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta, pies FIG., cuadro de datos), jerarquía de la lista de precios (que "Según cotización" no parezca un error), tablas compactas legibles a 320, simulador (radios con nombre, foco), foco visible en los enlaces de las tablas y de "Otras zonas", contraste del cierre, y que las 6 zonas no se vean como copias (sin agregar contenido: solo jerarquía).
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta en las 7; un H1; migas visibles = `BreadcrumbList`; `FAQPage` = lo visible; `Service` y `OfferCatalog` válidos en Rich Results Test (sin `InStock`; mármol fuera del catálogo); respuesta directa de pasto idéntica a la home; anclas estables; riesgo de doorway (que nada nuevo sea plantilla genérica por zona) y que nada adelante la Etapa 3 (títulos, `/zonas`, 301) ni la 4 (grafo único).
3. **CRO** (`general-purpose` con `page-cro`): precio y CTA en el primer pantallazo; mensaje de cada zona con colonia, servicio y metros; de la lista de precios al WhatsApp sin callejones (cada renglón enlaza a su página); "Según cotización" con camino claro (CTA y mensaje); el simulador como ayuda y no como distracción.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): reglas del dueño (precios solo de `datos.py`, "según cotización" sin inventar, fotos de main en orden, sin "gratis" salvo la garantía aprobada, sin existencias, sin distancias ni tiempos, sin opiniones, anticipo, visita con costo, mensualidades sin "MSI" ni "recargo" y sin reimplementar la fórmula), paridad y sus motivos, `test_anclas` y sus pendientes, la eliminación de `tools/pasto` sin cambiar el feed ni el sitemap de la tienda, consola limpia y sin `.DS_Store`.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 2 otra vez) y el controlador vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan para el PR.

- [ ] **Step 7: Aprobación del dueño (controlador)**

Comparte la vista previa de Vercel y las capturas, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Si da un caso real con permiso, fotos con su colonia o precios nuevos, van en una tarea nueva antes del merge (dato en `datos.py`, prueba en `test_datos` y en `test_zonas_reglas`).

- [ ] **Step 8: Merge, push y despliegue (solo el controlador)**

Si el lote 5 se publica junto (2g + 2h + 2i), este paso espera a que 2h y 2i estén aprobadas; si el dueño la quiere antes, se publica sola:

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2g -m "merge: etapa 2g — zonas y precios con plantillas, precios de datos.py y sin tienda-pasto.css" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 48 …`, `shell: 0 de 108 …`, `0`; Vercel despliega `main`.

- [ ] **Step 9: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in jardineria-lomas-de-rosales-tampico jardineria-country-club-tampico jardineria-aguila-tampico jardineria-lomas-del-chairel-tampico jardineria-ciudad-madero jardineria-altamira precios; do
  printf "%s " $r; curl -s $W/$r | grep -cE "tienda-pasto.css|fonts.googleapis|minutos del|InStock|gratis|\\\$100"
done
curl -s -o /dev/null -w "%{http_code}\n" $W/css/tienda-pasto.css
curl -s $W/precios | grep -o '/css/terra-precios\.[0-9a-f]*\.css' | head -1 | xargs -I{} curl -s -o /dev/null -w "%{http_code}\n" $W{}
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" $W/jardineria-miramar-madero
```

Expected: `0` en las 7; `404` (la hoja vieja ya no existe); `200`; `308 https://www.viverosterra.com/jardineria-ciudad-madero` (los 301 de main siguen). En Chrome (escritorio y iPhone): consola limpia; "Cotizar por WhatsApp" de Madero abre el mensaje de Cd. Madero con la firma; `/precios#garantia-plantas` llega a su tarjeta; el simulador de `/precios` muestra 4 plazos con $15,000. En GA4 DebugView: `generate_lead` `zona:hero` con `service` `jardin` y `precios:simulador`.

- [ ] **Step 10: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 2.

- [ ] **Step 11: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2g && git branch -d feat/etapa-2g
```

---

## Lotes de ejecución sugeridos

| Lote | Tareas | Qué deja | Revisión intermedia |
|---|---|---|---|
| A · Fundaciones (sin cambiar cómo se ven las páginas) | 0–3 | Capturas de paridad, fotos y anclas; vigencia y mensajes de zona; reglas en rojo y anclas del sitio | Cumplimiento: que las capturas sean de main y las reglas fallen en las 7 por lo que deben |
| B · Piezas | 4–5 | Componentes y la lista de precios de `datos.py` | Código (python-reviewer): que ningún precio se escriba a mano y "según cotización" donde toca |
| C · Páginas | 6–9 | Las 6 zonas, la hoja y `/precios` migradas; `tools/pasto` sin HTML; `tienda-pasto.css` borrado | Paridad e informe por página; reglas en verde; feed y sitemap de la tienda sin cambios |
| D · Cierre | 10–11 | Navegador, Lighthouse, capturas, 4 puertas, aprobación del dueño, merge | Las 4 puertas del spec §11 |

## Correcciones a la hoja de ruta

- **"Tiempo desde el vivero"** (spec §3.3, zona): no se publica. Regla del dueño: sin distancias ni tiempos de llegada (y "A minutos del vivero" de Madero se retira). El dato verificable que queda es la dirección del vivero (cuadro de datos de la portada y la tarjeta de Madero).
- **"Caso real de la zona"**: ninguno tiene permiso del dueño; la plantilla no trae esa sección (no hay hueco vacío ni marcador). Cuando el dueño dé uno, se agrega en una tarea con su dato en `datos.py` (foto, m², fecha, colonia, permiso) y su prueba (pregunta 1).
- **"CTA con plantilla de zona"**: no existía en `datos.MENSAJES`; cada zona usa el mensaje de su portada en main (`mensajes_paginas.ZONAS`), como 2c–2f con sus páginas.
- **"Anclas estables `#garantia-plantas`, `#mensualidades`"**: `#mensualidades` ya existía; `#garantia-plantas` y `#garantia-pasto` son nuevas en `/precios` (dentro de `#garantias`). `/politicas#garantia-plantas` y `#mensualidades`, que enlazan 12 y 17 páginas, no cambian (son de 2i). La "prueba de anclas nueva" es `test_anclas.py`, para todo el sitio, con las 14 anclas rotas del blog como pendientes de 2h.
- **`/vivero-tampico`**: no entra en 2g. Sale de `tools/servicios/pages.py` con `servicios.css` y `design-system.css`, y su papel ("Visítanos", spec §3.5) toca la Etapa 3; va en 2i, que además retira `tools/servicios`.
- **`tienda-pasto.css`** (la hoja de ruta lo retiraba en 2b): seguía vivo porque `/precios` y las zonas, generadas por `tools/pasto`, lo cargaban. Se borra aquí, con `tools/pasto/common.py`, `zonas.py` y `precios.py`; `tools/pasto` queda como fuente de modelos, fletes, mensualidades, feed y sitemap de la tienda.
- **CSS**: las zonas no necesitan hoja; `/precios` trae `terra-precios.css` (691 B) porque `terra.css` está a 561 B de su tope. 2h (artículo) también deberá traer la suya.
- **Poda en la tabla de las zonas y de `/precios`**: no estaba en la hoja de ruta; es un dato oficial de `datos.py` (decisión del dueño del 2026-11-07) y Águila ya la ofrecía en su entrada sin precio.
- **Medición**: los CTA del cuerpo de las zonas pasan de `zona:cuerpo` a `zona:hero` y `zona:cierre`, como en las demás plantillas.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Las zonas parecen doorways (seis copias de la misma plantilla) | Se conserva solo el texto local de main (colonias con CP, problema local, preguntas), sin agregar relleno; la tabla de servicios es la misma porque los precios son los mismos. El contenido único por zona es de la Etapa 3 (spec §3.5: no se agregan zonas sin caso real). La puerta SEO lo revisa. |
| Quitar precios sin confirmar (mármol $250, tierra preparada $100, camión desde $5,000) baja información en `/precios` | Ya se retiraron de sus páginas en 2f; cada uno se declara en `PARIDAD` o queda "Según cotización" con camino al WhatsApp. Vuelven si el dueño los confirma (pregunta 5 y las de 2f). |
| Se rompe un enlace a un ancla | `paridad_zonas.py` congela los `id` de sección de main; `test_anclas.py` revisa todo `<a href="…#x">` del sitio; prueba de navegador llega a `#mensualidades`, `#garantia-plantas` y `#pasto`. |
| El feed de Merchant o el sitemap de la tienda cambian al reescribir `tools/pasto/build.py` | Mismas llamadas (`build_feed`, `upsert(..., conservar=True)`); la Tarea 9 verifica `git diff` vacío en `feed-pasto-sintetico.xml` y `sitemap.xml`. |
| La fórmula de mensualidades se desfasa | Python y JS ya tienen paridad (`test_mensualidades.py`, `vt-mensualidades.test.js`); `/precios` solo llama a `mensualidades.py` y a `vt-simulador.js`; prueba de navegador compara el simulador con `mensualidades.planes()`. |
| Las fotos altas se recortan distinto sin el `object-position` de main | Capturas de la Tarea 11; si se pierde lo importante, se agrega un `object-position` por foto en `componentes.figura` (con su prueba) sin cambiar la foto. |
| `/precios` queda con el CTA justo en el borde del primer pantallazo a 375×812 | `test_precio_y_cta_en_el_primer_pantallazo_movil` la cubre; la entrada ya se acortó en el prototipo (se quitó "Precios de Viveros Terra, con IVA y factura."; factura y REPSE van en la línea de abajo del CTA). |
| La vigencia "noviembre 2026" no es la que el dueño quiere | Una constante en `datos.py` (pregunta 3). |

## Preguntas al dueño

1. **Casos reales por zona:** ¿hay algún jardín terminado en Lomas de Rosales, Club Campestre, Águila/Altavista, Lomas del Chairel, Madero o Lagunas de Miralta que podamos mostrar (foto, m², fecha y colonia) con permiso del cliente? Sin permiso no se publica ninguno; con uno por zona, la Etapa 3 puede darle contenido propio a cada página.
2. **Fotos de las zonas:** cada zona usa una foto de main (Lomas de Rosales: proyecto de diseño; Club Campestre: jardín tropical; Águila: poda de pasto; Lomas del Chairel: aspersores; Madero: `diseno-jardines-madero-altamira-pasto`; Altamira: `jardineria-areas-verdes-tampico`). ¿Sabes en qué colonia o ciudad se tomó cada una? Hoy el pie no lo dice; si son de esa zona, el pie puede decirlo. ¿Alguna no es un trabajo de Viveros Terra? (las dos últimas dicen "jardín atendido por Viveros Terra").
3. **Vigencia de la lista:** `/precios` dirá "Lista de precios · vigente desde noviembre 2026" (confirmaste los precios oficiales el 7 y los de materiales el 8 de noviembre). ¿Está bien esa fecha o prefieres otra? (Antes decía "Actualizada en septiembre 2026".)
4. **Poda en las listas:** agregamos "Poda de palmas y árboles · desde $500 · según cotización" a `/precios` y a la tabla de las 6 zonas. ¿De acuerdo?
5. **Materiales en `/precios`:** siguen "según cotización" la tierra preparada (main: $100 el costal), el camión de tierra (main: desde $5,000), el m³ y el camión de tezontle, el saco de mármol (main: $250) y la piedra bola. Si ya tienes esos precios (preguntas 1–4 de 2f), se publican a la vez en `/precios` y en cada material.
6. **Textos locales de main que se conservan:** ¿son correctos? "Con visitas cada 15 a 21 días en lluvias y cada 30 en secas" (Lomas de Rosales y Club Campestre); "En fraccionamientos cerrados coordinamos horarios y acceso con la administración" (Altamira); "Podamos árboles y palmas con técnica" y "especies de raíz controlada" (Águila); "Coco plumoso, washingtonia, uva de mar" para la brisa de Miramar. Si alguno no aplica, se quita.
7. **Colonias por zona:** las de main (Lomas de Rosales, Lomas de la Aurora, Vista Hermosa; Club Campestre, Country Club, Sierra Morena; Águila, Altavista, Petrolera, Campbell; Lomas del Chairel, Colinas de San Gerardo, Flamboyanes; Playa Miramar, Jardín 20 de Noviembre, Residencial del Parque, Ampliación Unidad Nacional; Lagunas de Miralta, Altamira Centro). ¿Agregamos o quitamos alguna? Solo colonias donde de verdad trabajan.
8. **Mensaje de WhatsApp de cada zona:** el menú, la barra y el pie de cada zona abrirán "Hola, quiero cotizar jardinería en {zona}. Colonia / Servicio que necesito / Metros aprox. / Les mando foto del espacio" (el de su portada en main) en vez del genérico de jardín. ¿De acuerdo?
9. **Diseño en `/precios`:** el Plan Terra Esencial dice "Entrega en 3 a 5 días hábiles" (igual que en `/diseno-jardines-tampico`). ¿Lo mantenemos?
