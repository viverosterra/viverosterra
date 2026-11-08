# Etapa 2e · Plantas: hub, subcategorías y catálogo "Arma tu lista" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Quinto sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2e; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.2, §3.3, §3.5, §4, §5, §8.4, §10). Las siete páginas de plantas dejan de ser HTML a mano (seis parchadas por `tools/servicios`, el catálogo con 570 renglones de JS en línea) y salen de dos plantillas nuevas con su contenido en `tools/site/contenido/`: **`hub_categoria`** para `/plantas-palmas-arboles-tampico` y sus cinco subcategorías (`/palmas-tropicales-tampico`, `/plantas-para-jardin-tampico`, `/arboles-ornamentales-tampico`, `/arboles-para-banqueta-tampico`, `/plantas-de-interior-tampico`) y **`catalogo`** para `/catalogo` (`public/catalogo.html`). Secuencia del hub (spec §3.3): H1 con precio "desde" y CTA → filtro por necesidad (sol/sombra, salitre, tamaño) → subcategorías con "desde $" solo de `datos.py` → "Arma tu lista" (un solo mensaje) → garantía condicionada y siembra → FAQ → CTA. Secuencia del catálogo: buscador y filtros arriba → una sola rejilla (foto, nombre, nombre científico, luz/riego/altura, "+ Añadir a mi lista" como `<button>` real) → lista con un solo mensaje → garantía condicionada. Las ~118 fotos que hoy pasan por el proxy `/api/img` (las del catálogo y las 17 del hub, que son las mismas) quedan locales en `public/img/catalogo/<especie>-tampico.webp`, con `width`, `height` y `alt`, por un script de descarga versionado y probado (el proxy se borra en la Etapa 5). Subcategorías con foto real del vivero en cada especie. Se publica en el lote 4 (junto con 2f), con 2d ya en producción.

**Architecture:** Igual que 2a–2d: `contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD`; la plantilla arma la página con `componentes.py`; `generar.py` registra la fila; `build.py` la escribe con el shell solo si cambia. Lo nuevo:
1. **Datos del dueño en `datos.py`:** `PRECIOS_ESPECIE` (areca y coco plumoso $250, palma real $500, flamboyán $250: los únicos precios de plantas que existen), `PALMAS_PRECIO` (la frase exacta del dueño) y `DESDE_PLANTAS` (el "desde" de cada subcategoría o `None` = "Según cotización"). `mensajes_paginas.PLANTAS` lleva la plantilla de WhatsApp de cada página (las de `tools/servicios/pages.py` con huecos `___`).
2. **Una sola fuente de especies:** `contenido/catalogo_especies.json` (117 especies; se extrae una vez del arreglo `plants` del catálogo de `main`, sin el Floripondio duplicado) y `contenido/catalogo_datos.py` (carga, `slug`, `atributos` = `pAttr()` de main línea por línea con los 118 casos congelados, `tamano`, `SALITRE` con la fuente de cada especie, guías del blog por especie y 10 nombres científicos corregidos y declarados). El hub, las subcategorías y el catálogo leen de ahí: una especie dice lo mismo en todas las páginas. Va en JSON por volumen (como los cuerpos del blog de 2h).
3. **Fotos locales:** `tools/site/fotos_catalogo.py` (una vez, con red y Pillow) baja cada foto de Drive (`lh3.googleusercontent.com/d/<id>=w1200`), la valida, la vuelve a codificar a WebP de 480 px y escribe `img`, `ancho` y `alto` en el JSON. Ninguna página usa `/api/img` al terminar (prueba global).
4. **Componentes nuevos en un archivo aparte** (`componentes.py` ya tiene 811 renglones): `tools/site/componentes_plantas.py` (foto de especie con pie "Fig. NN · <especie> · En nuestro vivero", tarjeta de especie, índice de subcategorías con "desde" o "según cotización", filtro por necesidad con conteos reales, buscador y filtros, rejilla del catálogo, diálogos de la lista).
5. **JS del catálogo fuera del HTML:** `public/js/vt-catalogo.js` (vanilla, funciones puras exportadas para `node --test`). Conserva el contrato del armador de lista de main: la lista es `[{name, sc, sz, qty}]`, la misma especie con el mismo tamaño actualiza la cantidad (`confirmAdd()`), y el mensaje es **idéntico** al que armaba `sendWA()` (casos congelados de main antes de borrarlo). Lo que cambia es cómo sale: un `<a data-cta="catalogo:sendWA">` cuyo `href` se recalcula (patrón de 2d), que `terra.js` mide (`generate_lead` con el mismo `cta_id` que `VTMedicion.whatsapp('sendWA')`) y firma; sin `window.open`. Filtros con estado en la URL (`/catalogo?luz=sol`), así el filtro por necesidad del hub son enlaces sin JS.
6. **Hoja propia `terra-plantas.css`** (como `terra-tienda.css`): `terra.css` publicado mide 47,514 B de 49,152 B permitidos; el catálogo no cabe. El shell la agrega en `<body class="vt-pagina vt-plantas">`; copia con hash e inmutable en Vercel.
7. **Paridad de especies:** `tools/site/paridad_plantas.py` congela, además de lo que ya congela `paridad.py`, qué especies publicaba cada página con su nombre científico y sus enlaces al blog; `test_plantas_paridad.py` exige que cada una siga, tenga reemplazo o motivo.

**Tech Stack:** Python 3.9+ estándar y `unittest`; Pillow solo en `fotos_catalogo.py` (no en el build ni en las pruebas); Playwright para Python 1.48 en las pruebas de navegador; CSS plano; JavaScript vanilla (`vt-catalogo.js` nuevo; `terra.js` sin cambios); `node --test` sin `package.json`; Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2e` (rama `feat/etapa-2e`, ya creada desde `main` en `b32e503`). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- **Qué se probó y qué no.** El plan se prototipó sobre `b32e503` en una copia de trabajo (fuera del repo): las Tareas 0–8 completas (capturas, casos de `pAttr`/`sendWA`, datos, reglas en rojo, JSON de especies, **la descarga real de las 117 fotos de Drive**, la hoja `terra-plantas.css` con su cableado, componentes y `vt-catalogo.js`: todo en verde, `node --test` con 56) y, de las Tareas 9–12, el hub, `/arboles-ornamentales-tampico` y `/catalogo` con su paridad en `ok`, `test_plantas*`, `test_reglas`, `test_consistencia`, `test_paridad`, `test_generar` y las pruebas de navegador (axe a 375/1440, sin desbordar de 320 a 1920, primer pantallazo, CLS, LCP sin `/api/img`, catálogo con teclado, filtro del hub, consola limpia en las 108 páginas). Las salidas "Expected" de esas tareas son las de esa corrida. **No** se prototiparon las otras cuatro subcategorías (Tarea 10, Step 4: van como tabla sobre el modelo de árboles ornamentales) ni Lighthouse y capturas (Tarea 13). Los archivos nuevos van completos; los cambios a archivos existentes van como bloques exactos a insertar o reemplazar con el editor. Si una prueba no da lo que dice el plan, arregla el código (no la prueba) salvo que la prueba contradiga el spec; anota cada desvío en el PR.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`).
- Cuando una tarea cambia `terra.css` o `terra-plantas.css`, el build cambia el hash, reescribe el `<head>` de las páginas afectadas y rota las copias (`activos.json` guarda dos): se versiona todo (`git add public tools/site/activos.json`) revisando antes `git status --short | grep -v '\.html$'`.
- **Reglas del dueño en juego** (las prueban `test_reglas.py`, `test_consistencia.py` y la nueva `test_plantas_reglas.py`):
  - Precios de plantas **solo** de `datos.py`: "Flamboyán desde $250" (ortografía flamboyán, nunca framboyán; los slugs `/blog/framboyan-…` no se tocan); palmas: "Areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; el precio sube con la altura" y las demás palmas "según cotización"; nunca los $850–$4,200 de main ni los "desde" sin confirmar del hub (washingtonia, viajero y kerpis $500, cycas $700, bambú $1,000, cola de zorro $1,500, ficus $200, neem $300/$350, tabachín $350, trueno $300, laurel $500, tulipán $600, crespón $350, jacaranda $450, olivo negro $600, polyalthia $400, "jardín desde $3,000–$8,000" y el "Desde $200" del Open Graph del hub).
  - Garantía de plantas: siempre `datos.GARANTIA_PLANTAS` (30 días, solo las que sembramos, con el riego indicado, "ver condiciones") y enlace a `/politicas#garantia-plantas`; nunca incondicional.
  - Sin afirmaciones sin verificar: nada de "productor directo", SENASICA, "disponibilidad real", "en existencia", insignias de disponibilidad o de "+ Vendido", cifras inventadas ("+500 proyectos", "3 estados", "18 años", "+200,000 m²"), calificaciones o estrellas, opiniones sin permiso (Martha R. y Constructora Arce del hub no están en `datos.OPINIONES`), precios inventados, "Oasis", el nombre del proveedor de la terminal, "gratis" o "sin costo". Pago = anticipo (`datos.ANTICIPO`). La visita nunca es gratis (`datos.VISITA_COSTO_CORTO` si se menciona).
  - Fotos de especie: son del vivero (dato del dueño); pie "Fig. NN · <especie> · En nuestro vivero".
  - **Títulos:** la consolidación de títulos y la canibalización de plantas son de la Etapa 3. Título, robots y canonical quedan como están publicados; solo se declara (con `PARIDAD["meta"]`) la descripción de Open Graph del hub, que publica "Desde $200".
- Dos textos de CTA de WhatsApp y teléfono, como en 2a–2d: "Cotizar por WhatsApp" y "Llamar 833 326 8008". "Arma tu lista" es navegación al catálogo, no un CTA de WhatsApp.

## Cobertura del spec y de la hoja de ruta

| Pide el spec / la hoja de ruta / las auditorías | Dónde |
|---|---|
| §3.3 hub: H1 + filtro por necesidad (sol/sombra, salitre, tamaño) → subcategorías con "desde $" → "Arma tu lista" (un solo mensaje) → garantía condicionada y siembra → FAQ → CTA | Tareas 7 y 9 (`componentes_plantas.necesidades`, `indice_subcategorias`, `plantillas/hub_categoria.py`), `test_plantas.HubTest.test_orden_de_secciones_del_spec` |
| §3.3 catálogo: buscador y filtros arriba → una sola rejilla (foto, nombre, nombre científico, luz/riego/altura, "+ Añadir a mi lista") → lista con un solo mensaje → garantía condicionada | Tareas 7, 8 y 11 (`rejilla_catalogo`, `vt-catalogo.js`, `plantillas/catalogo.py`) |
| §3.5 plantas: hub = `/plantas-palmas-arboles-tampico`; `/catalogo` = "Arma tu lista"; subcategorías con breadcrumb al hub; un solo conteo "+200 variedades" | Migas visibles y `BreadcrumbList` "Inicio › Plantas y palmas › …" en las 5 subcategorías y el catálogo; `datos.VARIEDADES`. Títulos nuevos y plantas de interior: Etapa 3 |
| §5.3 catálogo: "Garantía 30 días" sin condición → "En plantas que sembramos nosotros · ver condiciones" | `datos.GARANTIA_PLANTAS` + enlace (`test_consistencia.test_garantia_de_plantas_con_condicion` sigue en verde) |
| §8.4 / A05 #9: `/api/img` del catálogo y del hub → `/img/catalogo/<especie>-tampico.webp` con dimensiones; LCP sin `/api/img` | Tareas 4–5 (`fotos_catalogo.py`), `test_plantas_reglas` y `test_plantillas_navegador.test_lcp_de_plantas_sin_api_img` |
| Hoja de ruta 2e: armador de lista con mensajes sin SVG, `select_content`, `VTMedicion.whatsapp` → se conserva su contrato | Tarea 1 (casos de `sendWA()` y `pAttr()` de main), Tarea 8 (mismo mensaje, mismo `cta_id`), enlaces a `/catalogo` con `data-cta` (`terra.js` manda `select_content`) |
| Hoja de ruta 2e: foto real obligatoria en subcategorías | Tarea 10: cada especie con su foto local; `test_plantas.SubcategoriasTest.test_cada_especie_con_foto_del_vivero` |
| Hoja de ruta 2e: "Flamboyán desde $250"; garantía siempre condicionada | `datos.PRECIOS_ESPECIE`, `test_consistencia.test_flamboyan_desde_250`, `test_plantas_reglas` |
| Paridad: especies, precios, nombres científicos, enlaces a blog | Tarea 1 (`paridad.py` + `paridad_plantas.py`), `test_paridad.py`, `test_plantas_paridad.py` |
| Aceptación: catálogo operable con teclado; un solo mensaje con toda la lista; LCP sin `/api/img` | Tarea 12 (`test_catalogo_con_teclado_arma_un_solo_mensaje`, `test_lcp_de_plantas_sin_api_img`) |
| Pruebas de cada lote: axe, sin desbordar 320–1920, consola limpia, precio y CTA en el primer pantallazo, CLS, Lighthouse, capturas | Tareas 12 y 13 |
| Puertas (spec §11): diseño, SEO/AEO (se toca JSON-LD), CRO, cumplimiento | Tarea 13 |

Fuera de 2e: títulos y H1 nuevos, consolidación de plantas de interior y de árboles de banqueta (301 del blog), `/vivero-tampico` como "Visítanos" (Etapa 3); grafo JSON-LD único (Etapa 4: aquí los nodos `LocalBusiness` recortados se cambian por la referencia `#negocio`, como en 2d); borrar `/api/img` y `api/img.js` (Etapa 5); borrar `servicios.css` y `design-system.css` (2i: aún los usan vivero y materiales).

## Decisiones de diseño (y por qué)

- **El filtro por necesidad del hub son enlaces** (`/catalogo?luz=sol`, `?luz=media,sombra`, `?uso=salitre`, `?tam=chica|mediana|grande`) con el conteo real calculado en el build. Funcionan sin JS, se miden como `select_content` (terra.js ya mide todo enlace a `/catalogo`) y comparten la URL con el estado del catálogo (regla "URL como estado").
- **Salitre** no existe en los datos de main. Se marca solo con fuente publicada: la tabla del artículo `/blog/plantas-resistentes-sal-golfo-tampico` y tres fichas del catálogo que dicen "sal marina" (13 especies, `catalogo_datos.SALITRE`). El dueño la revisa (pregunta 6).
- **Tamaño** = altura adulta de la ficha: hasta 1.5 m, de 1.5 a 5 m, más de 5 m (30 / 29 / 56 especies; 2 sin altura numérica no entran en ningún grupo).
- **Rejilla en el HTML** (117 tarjetas, ~70 KB) en vez de dibujarla con JS: se indexa, se ve sin JS, no hay salto de diseño y el LCP no depende del script. El JS solo oculta tarjetas (`hidden`) y arma la lista.
- **Se retiran del catálogo** la pestaña "Pasto & Tierra" (sus cifras "+200,000 m²" y "+1,500" contradicen `datos.py`; el pasto tiene sus páginas, enlazadas en "¿Buscas pasto o material?"), las colecciones (una segunda rejilla), el orden "Más vendidas" y la insignia "+ Vendido" (sin dato; pregunta 7), el "Cotizar ahora" por tarjeta y "Medida especial" por tarjeta (el spec pide un solo mensaje; la medida especial vive en el diálogo de la lista), la cabecera con "Productor directo", "Actualizado con disponibilidad real", "+500 proyectos", "3 estados" y "18 años".
- **Nombres científicos:** 10 venían mal escritos en el catálogo (`Bucida Buceras`, `Tabubeia Rosea`, `Jacaranda Mimisfolia`, `Bahuinia sp.`…) y uno en la subcategoría (`Jacaranda mimifolia`). Se corrigen a la forma botánica, que es la que ya publicaban las subcategorías, y se declaran en `catalogo_datos.CIENTIFICOS_CORREGIDOS` (la paridad los acepta solo así).
- **Especies que el hub vendía y el catálogo no tiene** (Trueno, Tulipán africano) y "Tabachín" como especie aparte con la foto de la Tronadora: se retiran con motivo hasta que el dueño responda (preguntas 2 y 3).

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{plantas-palmas-arboles-tampico,palmas-tropicales-tampico,plantas-para-jardin-tampico,arboles-ornamentales-tampico,arboles-para-banqueta-tampico,plantas-de-interior-tampico,catalogo}.json` | Lo que publicaba cada página antes de migrar (`paridad.py capturar`). |
| `tools/site/paridad_plantas.py` | Captura y extracción de especies (nombre, científico) y enlaces a `/blog/` de las 7 páginas. |
| `tools/site/tests/paridad/plantas-especies.json` | La captura de especies de main. |
| `public/js/tests/casos-catalogo.json` | `pAttr()` de las 118 especies y dos mensajes de `sendWA()`, ejecutando el JS de main. |
| `tools/site/contenido/catalogo_especies.json` | Las 117 especies (fuente única), con foto local. |
| `tools/site/contenido/catalogo_datos.py` | Carga, slug, atributos (= `pAttr`), tamaño, salitre, guías, correcciones, conteos y URL del catálogo. |
| `tools/site/fotos_catalogo.py` | Descarga única y conversión de las fotos a `public/img/catalogo/`. |
| `public/img/catalogo/<slug>-tampico.webp` (117) | Fotos locales de 480 px. |
| `public/css/terra-plantas.css` | Estilos de las páginas de plantas, todo bajo `.vt-plantas`. |
| `tools/site/componentes_plantas.py` | Componentes de plantas (funciones puras). |
| `public/js/vt-catalogo.js`, `public/js/tests/vt-catalogo.test.js` | Filtros con estado en la URL y "Arma tu lista"; pruebas de `node --test`. |
| `tools/site/plantillas/hub_categoria.py`, `tools/site/plantillas/catalogo.py` | Las dos plantillas nuevas. |
| `tools/site/contenido/plantas_comun.py` | Garantía, necesidades, subcategorías, preguntas y JSON-LD que comparten las páginas de plantas. |
| `tools/site/contenido/{plantas_hub,palmas_tropicales,plantas_jardin,arboles_ornamentales,arboles_banqueta,plantas_interior,catalogo}.py` | Contenido de cada página. |
| `tools/site/tests/{test_plantas_reglas,test_plantas_paridad,test_catalogo_datos,test_fotos_catalogo,test_terra_plantas_css,test_componentes_plantas,test_plantas}.py` | Pruebas nuevas. |

Se modifican: `tools/site/datos.py`, `mensajes_paginas.py`, `activos.py`, `shell.py`, `partials.py`, `generar.py`, `vercel.json`, `tools/servicios/pages.py` y `tools/servicios/tests/test_pagos.py`; pruebas `test_datos`, `test_paginas`, `test_activos`, `test_shell` (o `test_partials`), `test_vercel`, `test_plantillas_navegador`. Regenerados por el build: las 7 páginas, `public/css/terra-plantas.<hash>.css`, `tools/site/activos.json`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar el worktree**

```bash
cd ~/dev/viverosterra-e2e && git branch --show-current && git log --oneline -1
```

Expected: `feat/etapa-2e` y `b32e503 merge: etapa 2d — páginas de empresas (mayoreo de pasto y palmas para proyectos)` (o el commit de `main` que agrega este plan, con padre `b32e503`). Si no existe: `git -C ~/dev/viverosterra worktree add ~/dev/viverosterra-e2e -b feat/etapa-2e`.

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
python3 -c "import PIL; print('PIL', PIL.__version__)"
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" "https://lh3.googleusercontent.com/d/1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb=w800"
```

Expected (verificado en `b32e503`): `plantillas: 0 de 30 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 433 tests` y `OK` (unos 2 min 20 s); `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 50` y `ℹ fail 0`; `playwright ok`; `PIL 11.3.0`; `200 image/jpeg` (la foto del olivo negro en Drive; si no da 200, detente: la Tarea 5 no se puede hacer).

---

### Task 1: Capturas de paridad y casos del JS de main

**Files:**
- Create: `tools/site/tests/paridad/` (7 capturas), `tools/site/paridad_plantas.py`, `tools/site/tests/paridad/plantas-especies.json`, `public/js/tests/casos-catalogo.json`

- [ ] **Step 1: Capturar las 7 páginas tal como están**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/paridad.py capturar /plantas-palmas-arboles-tampico /palmas-tropicales-tampico /plantas-para-jardin-tampico /arboles-ornamentales-tampico /arboles-para-banqueta-tampico /plantas-de-interior-tampico /catalogo
python3 -c "
import json
for p in ('plantas-palmas-arboles-tampico','palmas-tropicales-tampico','plantas-para-jardin-tampico','arboles-ornamentales-tampico','arboles-para-banqueta-tampico','plantas-de-interior-tampico','catalogo'):
    d=json.load(open(f'tools/site/tests/paridad/{p}.json')); print(p, len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']), len(d['jsonld_tipos']))"
```

Expected: siete líneas `captura: …` y luego (verificado):
```
plantas-palmas-arboles-tampico 36 7 18 10 8
palmas-tropicales-tampico 5 8 3 1 11
plantas-para-jardin-tampico 5 5 2 1 8
arboles-ornamentales-tampico 5 5 6 0 8
arboles-para-banqueta-tampico 5 5 3 0 8
plantas-de-interior-tampico 5 5 0 1 8
catalogo 6 0 0 2 3
```

- [ ] **Step 2: Escribir `tools/site/paridad_plantas.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/paridad_plantas.py <<'EOF'
"""Paridad de especies de las páginas de plantas (Etapa 2e): nombre común, nombre científico y enlaces al blog.

paridad.py congela encabezados h1–h3, preguntas, precios y enlaces del <main>; las tarjetas de especies de estas páginas
no son encabezados (div.ecard-name de las subcategorías, las tarjetas del hub, el arreglo `plants` del catálogo), así que
aquí se congela aparte qué especies publicaba cada página, con su nombre científico, y sus enlaces a /blog/. Las páginas
nuevas marcan cada especie con <h3 class="vt-esp__nombre"> y <p class="vt-esp__sci"><i>…</i></p>.
tests/test_plantas_paridad.py exige que cada especie siga, tenga reemplazo o motivo (PARIDAD["especies"]) y que su nombre
científico sea el mismo o la corrección declarada en contenido/catalogo_datos.CIENTIFICOS_CORREGIDOS.

Uso: python3 tools/site/paridad_plantas.py capturar   (escribe tests/paridad/plantas-especies.json)
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402

RUTAS = ("/plantas-palmas-arboles-tampico", "/palmas-tropicales-tampico", "/plantas-para-jardin-tampico",
         "/arboles-ornamentales-tampico", "/arboles-para-banqueta-tampico", "/plantas-de-interior-tampico", "/catalogo")
CAPTURA = paridad.CAPTURAS / "plantas-especies.json"
SUBCATEGORIA_RE = re.compile(r'class="ecard-name">(.*?)</div>\s*<div class="ecard-sc">(.*?)</div>', re.S)
HUB_RE = re.compile(r'<a\b[^>]*class="service-card[^"]*"[^>]*>.*?<h3\b[^>]*>(.*?)</h3>', re.S)
CATALOGO_RE = re.compile(r"\{cat:'\w+',name:'([^']*)',sc:'([^']*)'")
NUEVA_RE = re.compile(r'<h3 class="vt-esp__nombre">(.*?)</h3>\s*<p class="vt-esp__sci"><i>(.*?)</i></p>', re.S)
BLOG_RE = re.compile(r'href="(/blog/[^"#?]+)"')


def especies(html):
    """Pares (nombre, científico) únicos, en orden de aparición; "" si la página no publicaba el científico."""
    cuerpo = paridad.principal(html)
    pares = [(paridad.texto(n), paridad.texto(s)) for n, s in SUBCATEGORIA_RE.findall(cuerpo)]
    pares += [(paridad.texto(n), "") for n in HUB_RE.findall(cuerpo) if not paridad.texto(n).startswith("+")]
    pares += CATALOGO_RE.findall(html)
    pares += [(paridad.texto(n), paridad.texto(s)) for n, s in NUEVA_RE.findall(cuerpo)]
    vistos, salida = set(), []
    for par in pares:
        if par not in vistos:
            vistos.add(par)
            salida.append(par)
    return salida


def blog(html):
    return sorted(set(BLOG_RE.findall(paridad.principal(html))))


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"especies": [list(p) for p in especies(html)], "blog": blog(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_plantas.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["especies"]), len(d["blog"]))
EOF
python3 tools/site/paridad_plantas.py capturar
```

Expected:
```
/plantas-palmas-arboles-tampico 19 0
/palmas-tropicales-tampico 11 0
/plantas-para-jardin-tampico 6 0
/arboles-ornamentales-tampico 6 0
/arboles-para-banqueta-tampico 6 0
/plantas-de-interior-tampico 6 0
/catalogo 117 0
```
(118 entradas en el arreglo, 117 pares únicos: el Floripondio venía dos veces con el mismo nombre científico. Ninguna página enlaza hoy un artículo: los enlaces a guías que agrega 2e son nuevos; la captura asegura que ninguno se pierda en adelante.)

- [ ] **Step 3: Congelar `pAttr()` y `sendWA()` de main ejecutando su JS**

Script de un solo uso (no se versiona): ejecuta el `<script>` del catálogo con un DOM mínimo y escribe los casos.

```bash
cd ~/dev/viverosterra-e2e
node - public/catalogo.html > public/js/tests/casos-catalogo.json <<'EOF'
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const bloque = html.match(/<script>\s*\/\/ Función para construir URL[\s\S]*?<\/script>/)[0].replace(/^<script>|<\/script>$/g, '');
const abiertos = [];
const nodo = () => new Proxy(function () {}, { get: (t, k) => (k === 'value' ? '' : k === 'classList' ? { add() {}, remove() {}, toggle() {} } : nodo()), set: () => true, apply: () => nodo() });
const ctx = { console, encodeURIComponent, CSS: { escape: (s) => s }, confirm: () => true, setTimeout() {},
  document: { getElementById: () => nodo(), querySelectorAll: () => [], querySelector: () => null },
  window: { open: (u) => abiertos.push(u), VTMedicion: { whatsapp() {} } } };
ctx.window.window = ctx.window;
ctx.VTMedicion = ctx.window.VTMedicion;
vm.createContext(ctx);
vm.runInContext(bloque.replace(/^const plants/m, 'var plants').replace(/^let cart = \[\];/m, 'var cart = [];')
  + '\n;this.__p=plants;this.__pAttr=pAttr;this.__send=()=>sendWA();this.__setCart=(c)=>{cart=c;};', ctx);
const atributos = ctx.__p.map((p) => { const a = ctx.__pAttr(p); return { name: p.name, luz: [...a.L].sort(), riego: a.R, flor: a.flor, mant: a.mant, uso: [...a.U].sort() }; });
const listas = [
  [{ name: 'Palma Areca', sc: 'Dypsis lutescens', sz: '1 m', qty: 3 }],
  [{ name: 'Olivo Negro', sc: 'Bucida buceras', sz: '2-3 m', qty: 10 }, { name: 'Duranta Cubana', sc: 'Duranta erecta', sz: 'Medida especial', qty: 1 }],
];
const mensajes = listas.map((l) => { abiertos.length = 0; ctx.__setCart(l); ctx.__send(); return { lista: l, mensaje: decodeURIComponent(abiertos[0].split('text=')[1]) }; });
process.stdout.write(JSON.stringify({ origen: 'public/catalogo.html de main (b32e503), antes de la Etapa 2e', atributos, mensajes }, null, 1) + '\n');
EOF
python3 -c "
import json; d=json.load(open('public/js/tests/casos-catalogo.json'))
print(len(d['atributos']), d['atributos'][0]); print(repr(d['mensajes'][1]['mensaje']))"
```

Expected (verificado):
```
118 {'name': 'Olivo Negro', 'luz': ['sol'], 'riego': 'moderado', 'flor': 'sinflor', 'mant': 'bajo', 'uso': ['banqueta']}
'Hola Viveros Terra\n\nQuisiera cotizar lo siguiente:\n\n• Olivo Negro (2-3 m) × 10\n• Duranta Cubana (Medida especial) × 1\n\nTotal: 2 variedades, 11 unidades\n\n¿Pueden darme precio y disponibilidad?'
```

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/tests/paridad/plantas-palmas-arboles-tampico.json tools/site/tests/paridad/palmas-tropicales-tampico.json \
  tools/site/tests/paridad/plantas-para-jardin-tampico.json tools/site/tests/paridad/arboles-ornamentales-tampico.json \
  tools/site/tests/paridad/arboles-para-banqueta-tampico.json tools/site/tests/paridad/plantas-de-interior-tampico.json \
  tools/site/tests/paridad/catalogo.json tools/site/paridad_plantas.py tools/site/tests/paridad/plantas-especies.json \
  public/js/tests/casos-catalogo.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de las 7 páginas de plantas, sus especies y los casos del armador de lista de main" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Datos de plantas y mensajes de cada página

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/mensajes_paginas.py`
- Test: `tools/site/tests/test_datos.py`, `tools/site/tests/test_paginas.py`

- [ ] **Step 1: Escribir las pruebas**

Agrega a `DatosTest` en `tools/site/tests/test_datos.py` (después de `test_datos_de_empresas_etapa_2d`):

```python
    def test_precios_de_plantas_etapa_2e(self):
        """Decisión del dueño (2026-11-07): los únicos precios de plantas; las demás especies, según cotización."""
        self.assertEqual(datos.PRECIOS_ESPECIE, {"Palma Areca": 250, "Coco Plumoso": 250, "Palma Real": 500,
                                                 "Flamboyán Tabachín": 250})
        self.assertEqual(datos.PALMAS_PRECIO, "Areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; "
                                              "el precio sube con la altura")
        proyecto = {n.casefold(): p for n, _s, p in datos.PALMAS_PROYECTO if p is not None}
        for nombre, precio in datos.PRECIOS_ESPECIE.items():
            if nombre.casefold() in proyecto:
                with self.subTest(especie=nombre):
                    self.assertEqual(precio, proyecto[nombre.casefold()])
        oficiales = {v for v in datos.PRECIOS.values() if isinstance(v, int)}
        for ruta, desde in datos.DESDE_PLANTAS.items():
            with self.subTest(ruta=ruta):
                self.assertTrue(desde is None or desde in oficiales)
        self.assertEqual(sorted(r for r, d in datos.DESDE_PLANTAS.items() if d is not None),
                         ["/arboles-ornamentales-tampico", "/palmas-tropicales-tampico"])
```

Agrega a `ContextoTest` en `tools/site/tests/test_paginas.py` (después de `test_empresas_con_su_mensaje_en_menu_barra_y_pie`):

```python
    def test_plantas_con_su_mensaje_en_menu_barra_y_pie(self):
        """Etapa 2e: el hub y las 5 subcategorías llevan en el menú, la barra y el pie la plantilla de su portada."""
        for ruta, texto in mensajes_paginas.PLANTAS.items():
            ctx = paginas.contexto(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(ctx["mensaje"], datos.con_firma(texto))
                self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
                self.assertIn("___", texto)
        self.assertEqual(sorted(mensajes_paginas.PLANTAS), sorted(["/plantas-palmas-arboles-tampico", *datos.DESDE_PLANTAS]))
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas 2>&1 | grep -E "^(FAIL|ERROR):|FAILED"`
Expected: `ERROR: test_precios_de_plantas_etapa_2e`, `ERROR: test_plantas_con_su_mensaje_en_menu_barra_y_pie` y `FAILED (errors=2)`.

- [ ] **Step 3: Implementar**

En `tools/site/datos.py`, justo después de la tupla `PALMAS_PROYECTO`, agrega:

```python
# Plantas (Etapa 2e). Los únicos precios de plantas que dio el dueño (2026-11-07): areca y coco plumoso desde $250 y
# palma real desde $500 en su tamaño más chico (el precio sube con la altura) y flamboyán desde $250. Ninguna otra
# especie lleva precio: va SEGUN_COTIZACION (nunca los $850–$4,200 de main ni los "desde" sin confirmar del hub viejo).
# Clave: el nombre de la especie como sale en el catálogo (tools/site/contenido/catalogo_especies.json).
PRECIOS_ESPECIE = {
    "Palma Areca": PRECIOS["palma_desde"],
    "Coco Plumoso": PRECIOS["palma_desde"],
    "Palma Real": PRECIOS["palma_real"],
    "Flamboyán Tabachín": PRECIOS["flamboyan"],
}
PALMAS_PRECIO = (f"Areca y coco plumoso desde ${PRECIOS['palma_desde']}, palma real desde ${PRECIOS['palma_real']} en "
                 "tamaño chico; el precio sube con la altura")
# "Desde" de cada subcategoría de plantas: solo un precio de PRECIOS; None = SEGUN_COTIZACION (no se inventa).
DESDE_PLANTAS = {
    "/palmas-tropicales-tampico": PRECIOS["palma_desde"],
    "/plantas-para-jardin-tampico": None,
    "/arboles-ornamentales-tampico": PRECIOS["flamboyan"],
    "/arboles-para-banqueta-tampico": None,
    "/plantas-de-interior-tampico": None,
}
```

En `tools/site/mensajes_paginas.py`, después de `EMPRESAS`, agrega (son los textos de `tools/servicios/pages.py`, con los huecos `___`):

```python
# Plantas (Etapa 2e): la plantilla de main de cada portada (tools/servicios/pages.py, guided()), con los huecos ___. La
# usan la portada y el cierre y, por RUTAS, el menú, la barra móvil y el pie. El catálogo conserva su mensaje de RUTAS.
PLANTAS = {
    "/plantas-palmas-arboles-tampico": ("Hola, quiero cotizar plantas o palmas.\nPlantas que busco: ___\n"
                                        "Tamaño aprox.: ___\nColonia de entrega: ___\nLes mando foto del espacio."),
    "/palmas-tropicales-tampico": ("Hola, quiero cotizar palmas.\nPalma que me interesa: ___\nAltura aprox.: ___\n"
                                   "Colonia de entrega: ___\nLes mando foto del espacio."),
    "/plantas-para-jardin-tampico": ("Hola, quiero cotizar plantas para mi jardín.\nEl lugar es de sol o de sombra: ___\n"
                                     "Metros aprox.: ___\nColonia: ___\nLes mando foto del espacio."),
    "/arboles-ornamentales-tampico": ("Hola, quiero cotizar árboles.\nÁrbol que me interesa: ___\nAltura aprox.: ___\n"
                                      "Colonia de entrega: ___\nLes mando foto del espacio."),
    "/arboles-para-banqueta-tampico": ("Hola, quiero árboles para mi banqueta.\nAncho de la banqueta: ___\n"
                                       "Cuántos árboles: ___\nColonia: ___\nLes mando foto del espacio."),
    "/plantas-de-interior-tampico": ("Hola, quiero plantas de interior.\nCasa u oficina: ___\n"
                                     "Luz del lugar (mucha o poca): ___\nColonia: ___\nLes mando foto del espacio."),
}
```

y en `RUTAS`, después de la línea de `EMPRESAS`:

```python
    **{ruta: (texto, None) for ruta, texto in PLANTAS.items()},
```

- [ ] **Step 4: Verlas pasar y reconstruir**

```bash
cd ~/dev/viverosterra-e2e
(cd tools/site && python3 -m unittest tests.test_datos tests.test_paginas 2>&1 | tail -1)
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
```

Expected: `OK`; `plantillas: 0 de 30 páginas escritas` y `shell: 6 de 108 páginas actualizadas` (el menú, la barra y el pie de las 6 páginas de plantas con su mensaje); el `grep` vacío.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/datos.py tools/site/mensajes_paginas.py tools/site/tests/test_datos.py tools/site/tests/test_paginas.py \
  public/plantas-palmas-arboles-tampico/index.html public/palmas-tropicales-tampico/index.html \
  public/plantas-para-jardin-tampico/index.html public/arboles-ornamentales-tampico/index.html \
  public/arboles-para-banqueta-tampico/index.html public/plantas-de-interior-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(datos): precios de plantas del dueño, desde por subcategoría y mensajes de las páginas de plantas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Reglas de plantas en rojo

**Files:**
- Create: `tools/site/tests/test_plantas_reglas.py`

Las páginas de main rompen varias reglas (precios sin confirmar, `/api/img`, "productor directo", opiniones sin permiso…). La prueba se escribe ahora, con las 7 en `PENDIENTES`; cada tarea de migración saca las suyas y la prueba exige que una pendiente siga fallando (si ya cumple, hay que sacarla). Al cerrar 2e, `PENDIENTES` queda vacío.

- [ ] **Step 1: Escribir la prueba**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_plantas_reglas.py <<'EOF'
"""Reglas del dueño en las páginas de plantas (Etapa 2e): precios solo de datos.py, regla de palmas, flamboyán, garantía
con condiciones, sin afirmaciones sin verificar, fotos locales con pie y sin /api/img.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca las
suyas) y al cerrar la Etapa 2e queda vacía."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402
from test_b2b import PRECIOS_VIEJOS_PALMAS  # noqa: E402

PUBLIC = paginas.PUBLIC
PLANTAS = {
    "/plantas-palmas-arboles-tampico": "plantas-palmas-arboles-tampico/index.html",
    "/palmas-tropicales-tampico": "palmas-tropicales-tampico/index.html",
    "/plantas-para-jardin-tampico": "plantas-para-jardin-tampico/index.html",
    "/arboles-ornamentales-tampico": "arboles-ornamentales-tampico/index.html",
    "/arboles-para-banqueta-tampico": "arboles-para-banqueta-tampico/index.html",
    "/plantas-de-interior-tampico": "plantas-de-interior-tampico/index.html",
    "/catalogo": "catalogo.html",
}
PENDIENTES = frozenset(PLANTAS)
PERMITIDOS = {dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))
              if isinstance(n, int)}
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Palmas sin precio publicado (decisión del dueño): ninguna lleva un monto cerca.
PALMAS_SIN_PRECIO_RE = re.compile(
    r"(?:washington\w*|viajer\w*|ravenala|bismar\w*|kerpis|cola de (?:zorr|pescado)\w*|triang\w*|cycas|cica\b|"
    r"palma bamb[uú]|licuala|mascare\w*|datiler\w*|rubelina|cocotera|palma estrella|cart[oó]n|madagascar)"
    r"[^.$]{0,60}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("productor directo", r"\bproductor(?:es)?\s+direct"),
    ("disponibilidad o existencias", r"disponibilidad real|\ben existencia\b|disponibles? hoy|\bagotad|últimas piezas"),
    ("cifras sin respaldo", r"\+\s?500\s+proyectos|proyectos entregados|\b3 estados\b|\b18 años\b|\+\s?200,000 m²"),
    ("insignia de más vendido sin dato", r"\+\s?vendid"),  # el título del blog "Las palmas más vendidas…" sí va
    ("opiniones sin permiso", r"Martha R\.|Constructora Arce"),
    ("calificaciones", r"★|\b\d(?:\.\d)?\s+estrellas\b"),
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b"),
    ("SENASICA", r"\bSENASICA\b"),
)
FIGURA_CATALOGO_RE = re.compile(r"<figure\b(?:(?!</figure>).)*?/img/catalogo/(?:(?!</figure>).)*?</figure>", re.S)
PIE_RE = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)


def html_de(ruta):
    return (PUBLIC / PLANTAS[ruta]).read_text(encoding="utf-8")


def visible_y_ld(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    return paridad.texto(paridad.principal(html)) + " " + ld


def fallas(ruta):
    """Lista de reglas que rompe la página (vacía si cumple todas)."""
    html = html_de(ruta)
    texto = visible_y_ld(html)
    salida = []
    if "/api/img" in html:
        salida.append("usa /api/img")
    for p in sorted({m.group(0).replace(" ", "") for m in PRECIO_RE.finditer(texto)} - PERMITIDOS):
        salida.append(f"precio que no está en datos.py: {p}")
    # $1,500 también es el m³ de tierra negra (oficial): solo cuentan los precios viejos que no son de datos.py.
    salida += [f"precio viejo de palmas: {p}" for p in PRECIOS_VIEJOS_PALMAS if p in texto and p not in PERMITIDOS]
    salida += [f"palma con precio: …{m.group(0)}…" for m in PALMAS_SIN_PRECIO_RE.finditer(texto)]
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, texto, re.I)]
    if datos.GARANTIA_PLANTAS not in texto or "/politicas#garantia-plantas" not in html:
        salida.append("sin datos.GARANTIA_PLANTAS o sin enlace a /politicas#garantia-plantas")
    imagenes = html.count('src="/img/catalogo/')
    figuras = FIGURA_CATALOGO_RE.findall(html)
    if len(figuras) != imagenes:
        salida.append(f"{imagenes - len(figuras)} fotos del catálogo sin <figure>")
    for f in figuras:
        pie = paridad.texto(PIE_RE.search(f).group(1)) if PIE_RE.search(f) else ""
        if not re.fullmatch(r"Fig\. \d{2,3} · .+ · En nuestro vivero", pie):
            salida.append(f"pie de foto fuera de formato: {pie!r}")
    for img in re.findall(r"<img\b[^>]*>", paridad.principal(html)):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    return salida


class PlantasReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(PLANTAS) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_flamboyan_y_palmas_con_la_frase_del_dueno(self):
        flamboyan = f"Flamboyán desde {dinero(datos.PRECIOS['flamboyan'])}"
        for ruta, frases in (("/plantas-palmas-arboles-tampico", (flamboyan, datos.PALMAS_PRECIO)),
                             ("/arboles-ornamentales-tampico", (flamboyan,)),
                             ("/palmas-tropicales-tampico", (datos.PALMAS_PRECIO,))):
            if ruta in PENDIENTES:
                continue
            for frase in frases:
                with self.subTest(ruta=ruta, frase=frase):
                    self.assertIn(frase, visible_y_ld(html_de(ruta)))

    def test_hub_explica_el_anticipo(self):
        if "/plantas-palmas-arboles-tampico" not in PENDIENTES:
            self.assertIn(datos.ANTICIPO, visible_y_ld(html_de("/plantas-palmas-arboles-tampico")))


def informe():
    for ruta in PLANTAS:
        print(f"== {ruta}")
        for f in fallas(ruta)[:12]:
            print(f"  - {f}")


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Ver que las 7 páginas de main fallan hoy (y por qué)**

```bash
cd ~/dev/viverosterra-e2e/tools/site
python3 -c "import sys; sys.path.insert(0,'tests'); import test_plantas_reglas as t; t.informe()" | head -60
python3 -m unittest tests.test_plantas_reglas 2>&1 | tail -1
```

Expected: cada página con fallas (el hub: `usa /api/img`, `precio que no está en datos.py: $1,000`… y `opiniones sin permiso: Martha R.`; el catálogo: `usa /api/img`, `productor directo`, `cifras sin respaldo`; las subcategorías: precios sin confirmar o falta de `GARANTIA_PLANTAS`); y `OK` (todas pendientes y todas fallan).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/tests/test_plantas_reglas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(plantas): reglas del dueño en las páginas de plantas, con las 7 de main pendientes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Las especies del catálogo como datos

**Files:**
- Create: `tools/site/contenido/catalogo_especies.json`, `tools/site/contenido/catalogo_datos.py`
- Test: `tools/site/tests/test_catalogo_datos.py`

- [ ] **Step 1: Extraer el JSON una sola vez del catálogo de main**

```bash
cd ~/dev/viverosterra-e2e
node - public/catalogo.html > tools/site/contenido/catalogo_especies.json <<'EOF'
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const desde = html.indexOf('const plants = [');
const plants = vm.runInNewContext(html.slice(desde + 'const plants = '.length, html.indexOf('\n];', desde) + 2));
const CORREGIDOS = { 'Bucida Buceras': 'Bucida buceras', 'Quercus Virginiana': 'Quercus virginiana',
  'Lagerstroemia Indica': 'Lagerstroemia indica', 'Cassia Fistula': 'Cassia fistula', 'Delonix Regia': 'Delonix regia',
  'Jacaranda Mimisfolia': 'Jacaranda mimosifolia', 'Tabubeia Rosea': 'Tabebuia rosea', 'Tecoma Stans': 'Tecoma stans',
  'Ficus Elastica': 'Ficus elastica', 'Bahuinia sp.': 'Bauhinia sp.' };
const slug = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const limpio = (t) => String(t || '').replace(/<svg[\s\S]*?<\/svg>/g, '').replace(/\s+/g, ' ').trim();
const vistos = new Set();
const salida = [];
for (const p of plants) {
  const s = slug(p.name);
  if (vistos.has(s)) continue;  // Floripondio venía dos veces (el segundo con un id de Drive truncado)
  vistos.add(s);
  salida.push({ slug: s, cat: p.cat, name: p.name, sc: CORREGIDOS[p.sc] || p.sc, sz: p.sz, b: p.b, luz: limpio(p.luz),
    agua: p.agua, altura: p.altura, flor: p.flor, mant: p.mant, tipo: p.tipo, desc: p.desc, drive: p.img,
    img: null, ancho: null, alto: null });
}
process.stdout.write(JSON.stringify(salida, null, 1) + '\n');
EOF
python3 -c "
import json; d=json.load(open('tools/site/contenido/catalogo_especies.json'))
print(len(d), d[0]['slug'], d[0]['sc'], repr(d[0]['luz']), sum(1 for e in d if e['cat']=='palmas'))"
```

Expected: `117 olivo-negro Bucida buceras 'Pleno Sol' 21`.

- [ ] **Step 2: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_catalogo_datos.py <<'EOF'
"""Las especies del catálogo (Etapa 2e): fuente única, igual a lo que publicaba main y con atributos = pAttr() de main."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contenido import catalogo_datos as cd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[3]
CASOS = json.loads((RAIZ / "public" / "js" / "tests" / "casos-catalogo.json").read_text(encoding="utf-8"))
CAPTURA = json.loads((Path(__file__).resolve().parent / "paridad" / "plantas-especies.json").read_text(encoding="utf-8"))
CLAVES = {"slug", "cat", "name", "sc", "sz", "b", "luz", "agua", "altura", "flor", "mant", "tipo", "desc", "drive", "img",
          "ancho", "alto"}


class CatalogoDatosTest(unittest.TestCase):
    def test_117_especies_con_slug_unico_y_el_contrato_del_js(self):
        self.assertEqual(len(cd.ESPECIES), 117)
        self.assertEqual(len(cd.POR_SLUG), 117)
        for e in cd.ESPECIES:
            with self.subTest(especie=e["name"]):
                self.assertEqual(set(e), CLAVES)
                self.assertRegex(e["slug"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertEqual(e["slug"], cd.slug(e["name"]))
                self.assertIn(e["cat"], ("arboles", "palmas", "plantas"))
                self.assertTrue(e["sz"] and all(isinstance(t, str) for t in e["sz"]))
                self.assertNotIn("<", e["luz"] + e["desc"])

    def test_cada_especie_de_main_sigue_con_su_cientifico_o_la_correccion_declarada(self):
        por_nombre = {e["name"]: e for e in cd.ESPECIES}
        for nombre, cientifico in CAPTURA["/catalogo"]["especies"]:
            with self.subTest(especie=nombre):
                self.assertIn(nombre, por_nombre)
                self.assertEqual(por_nombre[nombre]["sc"], cd.CIENTIFICOS_CORREGIDOS.get(cientifico, cientifico))

    def test_correcciones_solo_las_declaradas(self):
        publicados = {s for _n, s in CAPTURA["/catalogo"]["especies"]}
        for viejo, nuevo in cd.CIENTIFICOS_CORREGIDOS.items():
            with self.subTest(viejo=viejo):
                self.assertNotEqual(viejo, nuevo)
                self.assertRegex(nuevo, r"^[A-Z][a-z]+ (?:[a-z]+|sp\.)$")
        self.assertTrue(set(cd.CIENTIFICOS_CORREGIDOS) - {"Jacaranda mimifolia"} <= publicados)

    def test_atributos_iguales_a_pattr_de_main(self):
        por_nombre = {e["name"]: e for e in cd.ESPECIES}
        for caso in CASOS["atributos"]:
            if caso["name"] not in por_nombre:  # el Floripondio duplicado
                continue
            with self.subTest(especie=caso["name"]):
                esperado = {k: v for k, v in caso.items() if k != "name"}
                self.assertEqual(cd.atributos(por_nombre[caso["name"]]), esperado)

    def test_tamano_por_altura_adulta(self):
        self.assertEqual(cd.tamano({"altura": "Hasta 60 cm"}), "chica")
        self.assertEqual(cd.tamano({"altura": "Hasta 1.5 m"}), "chica")
        self.assertEqual(cd.tamano({"altura": "Hasta 4 m"}), "mediana")
        self.assertEqual(cd.tamano({"altura": "Trepadora hasta 12 m"}), "grande")
        self.assertIsNone(cd.tamano({"altura": "Formado según tamaño"}))

    def test_salitre_y_guias_solo_con_fuente_y_de_especies_que_existen(self):
        for slug, fuente in cd.SALITRE.items():
            with self.subTest(salitre=slug):
                self.assertIn(slug, cd.POR_SLUG)
                self.assertTrue(fuente.startswith("/blog/") or fuente.startswith("Ficha del catálogo de main"))
        for slug, guia in cd.BLOG_ESPECIE.items():
            with self.subTest(guia=slug):
                self.assertIn(slug, cd.POR_SLUG)
                self.assertTrue((RAIZ / "public" / guia.strip("/") / "index.html").is_file())
        self.assertEqual(len(cd.SALITRE), 13)

    def test_filtros_cuentas_y_url_del_catalogo(self):
        self.assertEqual(cd.cuenta({}), 117)
        self.assertEqual(cd.cuenta({"cat": ["palmas"]}), 21)
        self.assertEqual(cd.cuenta({"uso": ["salitre"]}), 13)
        self.assertEqual(cd.cuenta({"tam": ["chica"]}) + cd.cuenta({"tam": ["mediana"]}) + cd.cuenta({"tam": ["grande"]}),
                         115)
        self.assertEqual(cd.url_catalogo({"luz": ["media", "sombra"]}), "/catalogo?luz=media,sombra")
        self.assertEqual(cd.url_catalogo(q="Palma real"), "/catalogo?q=Palma%20real")
        self.assertEqual(cd.normalizar("  Árbol  de Flor "), "arbol de flor")

    def test_ordenadas_como_el_az_de_main(self):
        nombres = [e["name"] for e in cd.ORDENADAS]
        self.assertEqual(nombres, sorted(nombres, key=cd.normalizar))
        self.assertEqual(len(nombres), 117)


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 3: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_catalogo_datos 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'contenido.catalogo_datos'` (error al cargar el módulo de prueba).

- [ ] **Step 4: Implementar `tools/site/contenido/catalogo_datos.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/contenido/catalogo_datos.py <<'EOF'
"""Las especies del catálogo (Etapa 2e): una sola fuente para /catalogo, el hub y las subcategorías de plantas.

catalogo_especies.json se extrajo una vez del arreglo `plants` de public/catalogo.html de main (plan 2e, Tarea 4) y desde
ahí es la fuente: nombre, nombre científico, tamaños, insignias, luz, riego, altura, flor, mantenimiento, tipo,
descripción y la foto local (img, ancho y alto, que escribe tools/site/fotos_catalogo.py). `drive` guarda el id de Google
Drive de donde salió la foto: solo lo lee fotos_catalogo.py; ninguna página lo publica. Va en JSON por volumen (117
especies), como los cuerpos del blog de la Etapa 2h.

atributos() es pAttr() del JS de main, línea por línea (los 118 casos están en public/js/tests/casos-catalogo.json).
tamano() agrupa la altura adulta. SALITRE marca las especies que aguantan salitre, cada una con su fuente publicada.
"""
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

ARCHIVO = Path(__file__).resolve().parent / "catalogo_especies.json"
GRUPOS = ("cat", "luz", "tam", "riego", "uso")
# Nombres científicos mal escritos en main (mayúscula en el epíteto o letras cambiadas), corregidos a la forma botánica,
# que es la que ya publicaban las subcategorías. Clave: como estaba publicado; valor: como queda.
CIENTIFICOS_CORREGIDOS = {
    "Bucida Buceras": "Bucida buceras",
    "Quercus Virginiana": "Quercus virginiana",
    "Lagerstroemia Indica": "Lagerstroemia indica",
    "Cassia Fistula": "Cassia fistula",
    "Delonix Regia": "Delonix regia",
    "Jacaranda Mimisfolia": "Jacaranda mimosifolia",
    "Jacaranda mimifolia": "Jacaranda mimosifolia",  # así venía en /arboles-ornamentales-tampico
    "Tabubeia Rosea": "Tabebuia rosea",
    "Tecoma Stans": "Tecoma stans",
    "Ficus Elastica": "Ficus elastica",
    "Bahuinia sp.": "Bauhinia sp.",
}
_SAL = "/blog/plantas-resistentes-sal-golfo-tampico"
# Especies que aguantan salitre, con su fuente publicada (la tabla del artículo o la ficha de main). Pregunta 6 al dueño.
SALITRE = {
    "palma-cocotera": _SAL, "palma-datilera": _SAL, "uva-de-playa": _SAL, "sansiviera": _SAL,
    "sansiviera-variegada": _SAL, "adelfa-enana": _SAL, "bugambilea-mini-morada": _SAL, "bugambilea-envarada": _SAL,
    "croto-petra": _SAL, "croto-tornillo": _SAL,
    "olivo-negro": "Ficha del catálogo de main: «Muy tolerante al calor y sal marina»",
    "casuarina": "Ficha del catálogo de main: «Muy resistente a la sal marina y el viento costero»",
    "arbusto-de-playa": "Ficha del catálogo de main: «Muy resistente a la sal marina, el viento y el calor»",
}
# Guía del blog de la especie, solo cuando el artículo trata de esa especie. Kerpis queda fuera: el artículo es de Howea
# forsteriana y el catálogo dice Chamaedorea sp. (pregunta 4 al dueño).
BLOG_ESPECIE = {
    "palma-areca": "/blog/palma-areca-tampico",
    "palma-bismarkia": "/blog/palma-bismarckia-bismarckia-nobilis-tampico",
    "coco-plumoso": "/blog/palma-coco-plumoso-tampico",
    "palma-cola-de-zorra": "/blog/palma-cola-de-zorro-wodyetia-bifurcata-tampico",
    "palma-real": "/blog/palma-real-roystonea-regia-tampico",
    "palma-triangular": "/blog/palma-triangular-dypsis-decaryi-tampico",
    "palma-washingtona": "/blog/palma-washingtona-tampico",
    "palma-viajera-ravenala": "/blog/cuidados-palma-del-viajero-ravenala",
    "hule": "/blog/ficus-elastica-cuidados-tampico",
    "flamboyan-tabachin": "/blog/framboyan-delonix-regia-tampico",
    "duranta-cubana": "/blog/duranta-erecta-tampico-cuidados-seto",
    "duranta-golden": "/blog/duranta-erecta-tampico-cuidados-seto",
    "duranta-zafiro": "/blog/duranta-erecta-tampico-cuidados-seto",
    "bugambilea-mini-morada": "/blog/buganvilia-tampico-cuidados-floracion",
    "bugambilea-envarada": "/blog/buganvilia-tampico-cuidados-floracion",
}
# Fotos de Drive de menos de 480 px de ancho (medidas en el prototipo del plan 2e, 2026-11-08): se publican a su tamaño,
# sin agrandar (igual de chicas que con /api/img), y son las primeras a reponer en la sesión de fotos (pregunta 12).
FOTOS_CHICAS = frozenset({
    "sauce-lloron", "liquidambar", "nispero", "eucalipto", "flor-de-mayo", "orquidea-pata-de-vaca", "palma-mascarena",
    "palma-cocotera", "palma-rubelina", "plumbago", "aralia-elegantisima", "beucarnea-soyate", "ficus-lyrata-pandurata",
    "ixora-karla", "limonaria", "papiro-estrella", "pasto-liriope", "palma-carton", "heliconia-baby-enana",
    "lapiz-tirucalli", "petunia-silvestre",
})
# Altura adulta: (clave, etiqueta, máximo en cm o None).
TAMANOS = (("chica", "Hasta 1.5 m", 150), ("mediana", "De 1.5 a 5 m", 500), ("grande", "Más de 5 m", None))


def normalizar(texto):
    """Como normalizar() de vt-catalogo.js: sin acentos, minúsculas y un solo espacio."""
    sin_acentos = "".join(c for c in unicodedata.normalize("NFD", str(texto or "")) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sin_acentos.lower()).strip()


def slug(nombre):
    return re.sub(r"[^a-z0-9]+", "-", normalizar(nombre)).strip("-")


def cargar(archivo=ARCHIVO):
    return tuple(json.loads(Path(archivo).read_text(encoding="utf-8")))


ESPECIES = cargar()
POR_SLUG = {e["slug"]: e for e in ESPECIES}
ORDENADAS = tuple(sorted(ESPECIES, key=lambda e: normalizar(e["name"])))


def especie(clave):
    return POR_SLUG[clave]


def _sin_etiquetas(texto):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", texto or "")).strip().lower()


def atributos(e):
    """pAttr() de main: luz (sol, media, sombra), riego, flor, mantenimiento y uso (banqueta, interior)."""
    luz = _sin_etiquetas(e["luz"])
    niveles = set()
    if "sol" in luz:
        niveles.add("sol")
    if "media" in luz:
        niveles.add("media")
    if "sombra" in luz and "media" not in luz:
        niveles.add("sombra")
    agua = (e.get("agua") or "").lower()
    riego = "poco" if re.search(r"poco|muy bajo", agua) else "abundante" if "abundante" in agua else "moderado"
    flor = "conflor" if re.match(r"^s[ií]", (e.get("flor") or "").strip().lower()) else "sinflor"
    mant = "bajo" if re.search(r"bajo", e.get("mant") or "", re.I) else "otro"
    tipo = (e.get("tipo") or "").lower()
    uso = set()
    if "banqueta" in tipo:
        uso.add("banqueta")
    if "interior" in tipo or "bi" in (e.get("b") or []):
        uso.add("interior")
    return {"luz": sorted(niveles), "riego": riego, "flor": flor, "mant": mant, "uso": sorted(uso)}


def altura_cm(texto):
    m = re.search(r"(\d[\d.,]*)\s*(m|cm)", texto or "", re.I)
    if not m:
        return None
    n = float(m.group(1).replace(",", "."))
    return n if m.group(2).lower() == "cm" else n * 100


def tamano(e):
    cm = altura_cm(e.get("altura"))
    if cm is None:
        return None
    return next(clave for clave, _t, maximo in TAMANOS if maximo is None or cm <= maximo)


def filtros(e):
    """Valores de cada grupo de filtro (los mismos data-* de la tarjeta que lee vt-catalogo.js)."""
    a = atributos(e)
    t = tamano(e)
    return {"cat": [e["cat"]], "luz": a["luz"], "tam": [t] if t else [], "riego": [a["riego"]],
            "uso": a["uso"] + (["salitre"] if e["slug"] in SALITRE else [])}


def coincide(e, filtro):
    """Como coincide() de vt-catalogo.js: dentro de un grupo basta una opción; entre grupos, todas."""
    valores = filtros(e)
    return all(any(v in valores[g] for v in opciones) for g, opciones in filtro.items() if opciones)


def cuenta(filtro):
    return sum(1 for e in ESPECIES if coincide(e, filtro))


def url_catalogo(filtro=None, q=""):
    """/catalogo con el filtro en la URL, en el mismo formato que escribirFiltros() de vt-catalogo.js."""
    partes = [f"q={quote(q, safe='')}"] if q else []
    partes += [f"{g}={','.join(quote(v, safe='') for v in (filtro or {})[g])}" for g in GRUPOS
               if (filtro or {}).get(g)]
    return "/catalogo" + ("?" + "&".join(partes) if partes else "")
EOF
```

- [ ] **Step 5: Verlas pasar**

Run: `cd tools/site && python3 -m unittest tests.test_catalogo_datos 2>&1 | tail -1`
Expected: `OK` (la paridad de `atributos()` contra `pAttr()` dio 0 diferencias en el prototipo).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/contenido/catalogo_especies.json tools/site/contenido/catalogo_datos.py tools/site/tests/test_catalogo_datos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantas): las 117 especies del catálogo como fuente única, con atributos iguales a los de main" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Fotos locales del catálogo

**Files:**
- Create: `tools/site/fotos_catalogo.py`, `public/img/catalogo/*.webp` (117)
- Modify: `tools/site/contenido/catalogo_especies.json` (img, ancho, alto)
- Test: `tools/site/tests/test_fotos_catalogo.py`

- [ ] **Step 1: Escribir las pruebas (sin red)**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_fotos_catalogo.py <<'EOF'
"""Fotos del catálogo en local (Etapa 2e): funciones puras de fotos_catalogo.py sin red y fotos publicadas."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fotos_catalogo as f  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"


def webp_vp8x(ancho, alto):
    return (b"RIFF" + (22).to_bytes(4, "little") + b"WEBP" + b"VP8X" + (10).to_bytes(4, "little") + b"\x00" * 4
            + (ancho - 1).to_bytes(3, "little") + (alto - 1).to_bytes(3, "little"))


def webp_vp8l(ancho, alto):
    bits = (ancho - 1) | ((alto - 1) << 14)
    return b"RIFF" + (13).to_bytes(4, "little") + b"WEBP" + b"VP8L" + (5).to_bytes(4, "little") + b"\x2f" + bits.to_bytes(4, "little")


class FuncionesTest(unittest.TestCase):
    def test_url_de_origen_solo_con_un_id_de_drive_valido(self):
        self.assertEqual(f.url_origen("1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb"),
                         "https://lh3.googleusercontent.com/d/1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb=w1200")
        for malo in ("", "../etc/passwd", "a b", "x" * 10, None):
            with self.subTest(id=malo), self.assertRaises(ValueError):
                f.url_origen(malo)

    def test_valida_tipo_y_tamano(self):
        self.assertEqual(f.validar("image/jpeg", b"x"), b"x")
        with self.assertRaises(ValueError):
            f.validar("text/html; charset=utf-8", b"<html>")
        with self.assertRaises(ValueError):
            f.validar("image/jpeg", b"x" * (f.MAXIMO_BYTES + 1))

    def test_dimensiones_de_webp_sin_pillow(self):
        self.assertEqual(f.dimensiones_webp(webp_vp8x(480, 720)), (480, 720))
        self.assertEqual(f.dimensiones_webp(webp_vp8l(480, 640)), (480, 640))
        with self.assertRaises(ValueError):
            f.dimensiones_webp(b"\xff\xd8\xff\xe0 no es webp")

    def test_actualizar_baja_solo_lo_que_falta_y_no_muta(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            (destino / "uno-tampico.webp").write_bytes(webp_vp8x(480, 600))
            entrada = ({"slug": "uno", "drive": "1" * 33}, {"slug": "dos", "drive": "2" * 33})
            pedidas = []
            salida, nuevas = f.actualizar(entrada, destino, bajar=lambda url: pedidas.append(url) or b"jpg",
                                          convertir=lambda _b: webp_vp8x(480, 720))
            self.assertEqual(nuevas, 1)
            self.assertEqual(pedidas, ["https://lh3.googleusercontent.com/d/" + "2" * 33 + "=w1200"])
            self.assertEqual([(e["img"], e["ancho"], e["alto"]) for e in salida],
                             [("/img/catalogo/uno-tampico.webp", 480, 600), ("/img/catalogo/dos-tampico.webp", 480, 720)])
            self.assertNotIn("img", entrada[0])

    def test_un_error_dice_que_especie_fallo(self):
        def falla(_url):
            raise ValueError("HTTP 404")
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(SystemExit) as error:
            f.actualizar(({"slug": "tres", "drive": "3" * 33},), Path(tmp), bajar=falla)
        self.assertIn("tres", str(error.exception))


class FotosPublicadasTest(unittest.TestCase):
    def test_cada_especie_con_su_foto_local(self):
        """480 px de ancho, salvo las fotos chicas declaradas (no se agrandan; pregunta 12 al dueño)."""
        for e in cd.ESPECIES:
            archivo = PUBLIC / e["img"].lstrip("/") if e["img"] else None
            with self.subTest(especie=e["slug"]):
                self.assertEqual(e["img"], f.ruta_local(e["slug"]))
                self.assertTrue(archivo.is_file())
                self.assertEqual(f.dimensiones_webp(archivo.read_bytes()), (e["ancho"], e["alto"]))
                if e["slug"] in cd.FOTOS_CHICAS:
                    self.assertLess(e["ancho"], f.ANCHO)
                else:
                    self.assertEqual(e["ancho"], f.ANCHO)
                self.assertLessEqual(archivo.stat().st_size, 120 * 1024)

    def test_sin_fotos_sobrantes(self):
        publicadas = {p.name for p in (PUBLIC / "img" / "catalogo").glob("*.webp")}
        self.assertEqual(publicadas, {f"{e['slug']}-tampico.webp" for e in cd.ESPECIES})


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_fotos_catalogo 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'fotos_catalogo'`.

- [ ] **Step 3: Implementar `tools/site/fotos_catalogo.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/fotos_catalogo.py <<'EOF'
"""Fotos del catálogo en local (Etapa 2e): baja una vez de Google Drive la foto de cada especie y la publica como
public/img/catalogo/<slug>-tampico.webp (480 px de ancho o el de la foto si es más chica, WebP calidad 72), con su ancho
y alto en contenido/catalogo_especies.json. Sustituye al proxy /api/img en el catálogo y el hub (el proxy se borra en la
Etapa 5). Una foto chica nunca se agranda: las 21 que miden menos de 480 px están en catalogo_datos.FOTOS_CHICAS.

Uso (una vez; requiere red y Pillow): python3 tools/site/fotos_catalogo.py
No reescribe las fotos que ya existen (solo vuelve a leer su tamaño). Cada descarga se valida: respuesta 200 de
lh3.googleusercontent.com (el mismo origen que usaba /api/img), tipo image/*, a lo más 15 MB, una imagen que Pillow
abre y de al menos 120 px de ancho (menos sería un ícono o una página de error). Los bytes descargados nunca se guardan
tal cual: se decodifican y se vuelven a codificar en WebP. Si una especie falla, se detiene y dice cuál.
tests/test_fotos_catalogo.py prueba las funciones sin red y que cada especie tenga su foto local.
"""
import io
import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

DESTINO = paginas.PUBLIC / "img" / "catalogo"
ANCHO = 480
CALIDAD = 72
MINIMO = 120
MAXIMO_BYTES = 15 * 1024 * 1024
ORIGEN = "https://lh3.googleusercontent.com/d/{id}=w1200"
ID_RE = re.compile(r"[\w-]{20,60}")


def url_origen(drive_id):
    if not isinstance(drive_id, str) or not ID_RE.fullmatch(drive_id):
        raise ValueError(f"id de Drive inválido: {drive_id!r}")
    return ORIGEN.format(id=drive_id)


def ruta_local(slug):
    return f"/img/catalogo/{slug}-tampico.webp"


def validar(tipo, cuerpo):
    if not (tipo or "").startswith("image/"):
        raise ValueError(f"no es una imagen: {tipo!r}")
    if len(cuerpo) > MAXIMO_BYTES:
        raise ValueError("la imagen pesa más de 15 MB")
    return cuerpo


def descargar(url):
    peticion = urllib.request.Request(url, headers={"User-Agent": "ViverosTerra-fotos/1.0"})
    with urllib.request.urlopen(peticion, timeout=30) as respuesta:
        if respuesta.status != 200:
            raise ValueError(f"HTTP {respuesta.status}")
        return validar(respuesta.headers.get("Content-Type", ""), respuesta.read(MAXIMO_BYTES + 1))


def a_webp(cuerpo):
    from PIL import Image, ImageOps

    with Image.open(io.BytesIO(cuerpo)) as original:
        im = ImageOps.exif_transpose(original).convert("RGB")
    if im.width < MINIMO:
        raise ValueError(f"foto de {im.width} px de ancho: menos de {MINIMO}")
    ancho = min(ANCHO, im.width)  # nunca se agranda una foto chica
    alto = round(im.height * ancho / im.width)
    salida = io.BytesIO()
    im.resize((ancho, alto), Image.LANCZOS).save(salida, "WEBP", quality=CALIDAD, method=6)
    return salida.getvalue()


def dimensiones_webp(datos):
    """(ancho, alto) de un WebP (VP8, VP8L o VP8X) sin Pillow."""
    if datos[:4] != b"RIFF" or datos[8:12] != b"WEBP":
        raise ValueError("no es WebP")
    tipo = datos[12:16]
    if tipo == b"VP8 ":
        ancho, alto = struct.unpack("<HH", datos[26:30])
        return ancho & 0x3FFF, alto & 0x3FFF
    if tipo == b"VP8L":
        bits = int.from_bytes(datos[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if tipo == b"VP8X":
        return int.from_bytes(datos[24:27], "little") + 1, int.from_bytes(datos[27:30], "little") + 1
    raise ValueError(f"WebP desconocido: {tipo!r}")


def actualizar(especies, destino=DESTINO, bajar=descargar, convertir=a_webp):
    """Lista nueva de especies con img, ancho y alto (no muta la de entrada) y cuántas fotos se bajaron."""
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    salida, nuevas = [], 0
    for e in especies:
        archivo = destino / f"{e['slug']}-tampico.webp"
        if not archivo.exists():
            try:
                archivo.write_bytes(convertir(bajar(url_origen(e["drive"]))))
            except (OSError, ValueError) as error:
                raise SystemExit(f"{e['slug']}: {error}") from error
            nuevas += 1
        ancho, alto = dimensiones_webp(archivo.read_bytes())
        salida.append({**e, "img": ruta_local(e["slug"]), "ancho": ancho, "alto": alto})
    return salida, nuevas


def main():
    especies, nuevas = actualizar(cd.cargar())
    cd.ARCHIVO.write_text(json.dumps(especies, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{nuevas} fotos nuevas · {len(especies)} especies con foto local en public/img/catalogo")


if __name__ == "__main__":
    main()
EOF
```

- [ ] **Step 4: Bajar las fotos (red) y revisar**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/fotos_catalogo.py
du -sh public/img/catalogo; ls public/img/catalogo | wc -l
python3 -c "
import json,collections; d=json.load(open('tools/site/contenido/catalogo_especies.json'))
print(collections.Counter(e['ancho'] == 480 for e in d), min(e['ancho'] for e in d))"
python3 tools/site/fotos_catalogo.py
```

Expected (verificado en el prototipo del plan: las 117 fotos existen en Drive y bajan en ~1 min): `117 fotos nuevas · 117 especies con foto local en public/img/catalogo`; unos 3.1 MB (mediana 19 KB, la más pesada 99 KB) y `117`; `Counter({True: 96, False: 21}) 146` (96 a 480 px; 21 más chicas, la menor el eucalipto de 146 px: son las de `FOTOS_CHICAS`); la segunda corrida `0 fotos nuevas · 117 …`. Si una especie falla (`SystemExit: <slug>: …`), detente y repórtala (no se inventa ni se usa otra foto). Abre 10 al azar (`open public/img/catalogo/{palma-real,olivo-negro,sansiviera-variegada,palma-cocotera}-tampico.webp`): deben ser plantas, no una página de error. **Sansiviera y Sansiviera Variegada salen de la misma foto de Drive** (pregunta 5); la palma cocotera es horizontal (266×190): el recorte 4:5 de la tarjeta la centra.

- [ ] **Step 5: Verlas pasar**

Run: `cd tools/site && python3 -m unittest tests.test_fotos_catalogo tests.test_catalogo_datos 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/fotos_catalogo.py tools/site/tests/test_fotos_catalogo.py tools/site/contenido/catalogo_especies.json public/img/catalogo
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantas): las 117 fotos del catálogo en local con su ancho y alto (sin /api/img)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Hoja `terra-plantas.css` y su cableado en el shell

**Files:**
- Create: `public/css/terra-plantas.css`, `tools/site/tests/test_terra_plantas_css.py`
- Modify: `tools/site/activos.py`, `tools/site/shell.py`, `tools/site/partials.py`, `vercel.json`
- Test: `tools/site/tests/test_activos.py`, `tools/site/tests/test_shell.py`, `tools/site/tests/test_vercel.py`

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_terra_plantas_css.py`:

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_terra_plantas_css.py <<'EOF'
"""terra-plantas.css: hoja de las páginas de plantas (Etapa 2e). Todo bajo .vt-plantas, sin colores literales, [hidden]
gana a los display de las tarjetas, la barra y los botones, y presupuesto propio."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-plantas.css"


class TerraPlantasCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_plantas(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in selector.split(",") if not p.strip().startswith(".vt-plantas ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_hidden_gana(self):
        for regla in (".vt-plantas [hidden]{display:none}", ".vt-plantas .vt-esp[hidden]{display:none}",
                      ".vt-plantas .vt-lista-barra[hidden]{display:none}"):
            self.assertIn(regla, self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 12 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 4 * 1024)

    def test_objetivos_de_44_px_y_movimiento_reducido(self):
        self.assertIn("min-height:44px", self.css)
        self.assertIn("@media (prefers-reduced-motion:reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
EOF
```

En `tools/site/tests/test_activos.py`, en `setUp`, después de la línea de `terra-tienda.css`:

```python
        (self.pub / "css" / "terra-plantas.css").write_text(".vt-plantas .vt-x{}", encoding="utf-8")
```

y en el bucle `for hoja in ("terra.css", "terra-tienda.css"):` (línea ~123) agrega `"terra-plantas.css"` a la tupla.

En `tools/site/tests/test_partials.py` agrega a `HeadTest` (ya importa `partials`):

```python
    def test_paginas_de_plantas_cargan_su_hoja(self):
        urls = {"terra.css": "/css/terra.a.css", "terra-tienda.css": "/css/terra-tienda.b.css",
                "terra-plantas.css": "/css/terra-plantas.c.css", "legacy-fixes.css": "/css/l.d.css",
                "terra.js": "/js/terra.e.js"}
        self.assertIn('<link rel="stylesheet" href="/css/terra-plantas.c.css">', partials.head(urls, False, plantas=True))
        self.assertNotIn("terra-plantas", partials.head(urls, False))
        self.assertNotIn("terra-tienda", partials.head(urls, False, plantas=True))
```

En `tools/site/tests/test_vercel.py`, cambia la constante:

```python
HASH = r"/(css|js)/(terra|terra-tienda|terra-plantas|legacy-fixes)\.([0-9a-f]+)\.(css|js)"
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_terra_plantas_css tests.test_shell tests.test_vercel tests.test_activos 2>&1 | grep -E "^(FAIL|ERROR):|FAILED|Error"`
Expected: `FileNotFoundError` de `terra-plantas.css`, `TypeError: head() got an unexpected keyword argument 'plantas'`, el `KeyError` de la cabecera inmutable en `test_vercel`.

- [ ] **Step 3: Implementar el cableado**

`tools/site/activos.py`, en `FUENTES` después de `terra-tienda.css`:

```python
    "terra-plantas.css": "css/terra-plantas.css",
```

y en el docstring, "(public/css/terra.css, terra-tienda.css, terra-plantas.css, legacy-fixes.css, public/js/terra.js)".

`tools/site/shell.py`: después de `TIENDA = …` agrega `PLANTAS = '<body class="vt-pagina vt-plantas">'` y en `aplicar` cambia la línea del head por:

```python
        "head": partials.head(urls, legacy="/css/tailwind.css" in html, tienda=TIENDA in html, plantas=PLANTAS in html),
```

`tools/site/partials.py`, en `head`: firma `def head(urls, legacy, tienda=False, plantas=False):`, docstring "Con plantas=True (páginas `<body class="vt-pagina vt-plantas">`, Etapa 2e), terra-plantas.css." y después del bloque `if tienda:`:

```python
    if plantas:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-plantas.css"]}">')
```

`vercel.json`: en la regla de caché inmutable cambia `"source": "/(css|js)/(terra|terra-tienda|legacy-fixes)\\.([0-9a-f]+)\\.(css|js)"` por `"source": "/(css|js)/(terra|terra-tienda|terra-plantas|legacy-fixes)\\.([0-9a-f]+)\\.(css|js)"`.

- [ ] **Step 4: Escribir `public/css/terra-plantas.css`**

```bash
cd ~/dev/viverosterra-e2e
cat > public/css/terra-plantas.css <<'EOF'
/* =========================================================
   Viveros Terra · terra-plantas.css · páginas de plantas (Etapa 2e)
   Hub, subcategorías y catálogo "Arma tu lista". Todo bajo .vt-plantas (<body class="vt-pagina vt-plantas">, el shell
   agrega esta hoja) y solo con tokens de terra.css. [hidden] gana con más especificidad que los display de abajo.
   ========================================================= */
.vt-plantas [hidden]{display:none}

/* filtro por necesidad (hub) */
.vt-plantas .vt-necesidades{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:12px;margin:24px 0 0;padding:0;list-style:none}
.vt-plantas .vt-necesidades a{display:grid;gap:4px;height:100%;min-height:44px;padding:16px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);color:var(--vt-ink);text-decoration:none;transition:border-color var(--vt-duration-fast) var(--vt-ease-out),transform var(--vt-duration-fast) var(--vt-ease-out)}
.vt-plantas .vt-necesidades a:hover{border-color:var(--vt-field);transform:translateY(-2px)}
.vt-plantas .vt-necesidades h3{margin:0;font-size:var(--vt-text-dato);line-height:1.15}
.vt-plantas .vt-necesidades span{color:var(--vt-muted);font-size:var(--vt-text-sm)}
.vt-plantas .vt-necesidades .vt-necesidad__n{margin-top:6px;color:var(--vt-field);font-weight:700}

/* tarjetas de especie (subcategorías, hub y catálogo) */
.vt-plantas .vt-esps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 12px;margin:24px 0 0;padding:0;list-style:none}
@media (min-width:768px){.vt-plantas .vt-esps{grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 20px}}
@media (min-width:1100px){.vt-plantas .vt-esps--cat{grid-template-columns:repeat(4,minmax(0,1fr))}}
.vt-plantas .vt-esp{display:flex;flex-direction:column;gap:6px;min-width:0}
.vt-plantas .vt-esp[hidden]{display:none}
.vt-plantas .vt-esp p{margin:0}
.vt-plantas .vt-esp__foto{margin:0}
.vt-plantas .vt-esp__foto img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:var(--vt-radius);background:var(--vt-bone-2)}
.vt-plantas .vt-esp__foto figcaption{margin-top:6px;font-size:var(--vt-text-xs);letter-spacing:.02em;color:var(--vt-muted)}
.vt-plantas .vt-esp__nombre{margin:4px 0 0;font-size:var(--vt-text-dato);line-height:1.15}
.vt-plantas .vt-esp .vt-esp__sci{font-family:var(--vt-font-serif);font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-plantas .vt-esp__datos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;margin:4px 0 0;padding:8px 0;border-block:1px solid var(--vt-line)}
@media (max-width:479px){.vt-plantas .vt-esp__datos{grid-template-columns:1fr}}
.vt-plantas .vt-esp__datos dt{font-size:var(--vt-text-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--vt-muted)}
.vt-plantas .vt-esp__datos dd{margin:0;font-size:var(--vt-text-xs);font-weight:600;overflow-wrap:anywhere}
.vt-plantas .vt-esp .vt-esp__precio{font-weight:700}
.vt-plantas .vt-esp .vt-esp__acciones{display:flex;flex-wrap:wrap;gap:0 16px;margin-top:auto}
.vt-plantas .vt-esp__acciones a,.vt-plantas .vt-esp__ficha summary{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:var(--vt-field)}
.vt-plantas .vt-esp__ficha summary{cursor:pointer}
.vt-plantas .vt-esp__ficha p{margin:0 0 8px;font-size:var(--vt-text-sm)}

/* catálogo: cabeza, buscador y filtros */
.vt-plantas .vt-bloque.vt-cat__cabeza{padding-block:20px 8px}
.vt-plantas .vt-cat__cabeza h1{margin:12px 0 8px;font-size:clamp(2rem,1.4rem + 2.6vw,3.5rem);line-height:1.02}
.vt-plantas .vt-cat__precios{margin:0 0 12px;font-weight:600}
.vt-plantas .vt-bloque.vt-cat__rejilla{padding-top:8px;padding-bottom:calc(var(--vt-bar-h) + 32px)}
.vt-plantas .vt-buscador{display:grid;gap:12px;margin:0 0 8px}
.vt-plantas .vt-buscador__filtros summary{display:inline-flex;align-items:center;min-height:44px;font-weight:700;cursor:pointer}
.vt-plantas .vt-buscador__grupos{display:grid;gap:12px}
@media (min-width:768px){.vt-plantas .vt-buscador__grupos{grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px 24px}}
.vt-plantas .vt-filtro{display:flex;flex-wrap:wrap;gap:8px;min-width:0;margin:0;padding:0;border:0}
.vt-plantas .vt-filtro legend{width:100%;margin-bottom:6px;padding:0;font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--vt-muted)}
.vt-plantas .vt-chip-p{min-height:44px;padding:0 14px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);color:var(--vt-ink);font:600 var(--vt-text-sm) var(--vt-font-sans);cursor:pointer}
.vt-plantas .vt-chip-p:hover{border-color:var(--vt-field)}
.vt-plantas .vt-chip-p[aria-pressed="true"]{border-color:var(--vt-field);background:var(--vt-field-100);box-shadow:inset 0 0 0 1px var(--vt-field)}
.vt-plantas .vt-buscador__n{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:0;font-weight:700}
.vt-plantas .vt-buscador__limpiar{min-height:44px;padding:0 4px;border:0;background:none;color:var(--vt-field);font:600 var(--vt-text-sm) var(--vt-font-sans);text-decoration:underline;cursor:pointer}
.vt-plantas .vt-cat__add{justify-content:center;width:100%;min-height:44px;margin-top:8px;text-align:center}
.vt-plantas .vt-cat__vacio{margin:24px 0 0;font-weight:600}
.vt-plantas .vt-especial{display:grid;gap:12px;max-width:640px}
.vt-plantas .vt-chip-p:focus-visible,.vt-plantas .vt-necesidades a:focus-visible,.vt-plantas .vt-esp__acciones a:focus-visible,.vt-plantas .vt-esp__ficha summary:focus-visible,.vt-plantas .vt-buscador__limpiar:focus-visible,.vt-plantas .vt-dialogo button:focus-visible{outline:2px solid var(--vt-field);outline-offset:2px}

/* "Arma tu lista": diálogos y barra */
.vt-plantas .vt-dialogo{width:min(100% - 32px,480px);max-height:calc(100dvh - 32px);padding:24px;border:0;border-radius:var(--vt-radius-tag);background:var(--vt-card);color:var(--vt-ink);box-shadow:var(--vt-sombra-card)}
.vt-plantas .vt-dialogo::backdrop{background:var(--vt-scrim)}
.vt-plantas .vt-dialogo h2{margin:0;font-size:var(--vt-text-h3)}
.vt-plantas .vt-dialogo .vt-campo{margin-top:16px}
.vt-plantas .vt-dialogo__botones{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0}
.vt-plantas .vt-cantidad{display:flex;align-items:center;gap:8px}
.vt-plantas .vt-cantidad input{width:7ch;text-align:center}
.vt-plantas .vt-cantidad button,.vt-plantas .vt-lista__ctrl button{min-width:44px;min-height:44px;padding:0 10px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);color:var(--vt-ink);font:700 var(--vt-text-base) var(--vt-font-sans);cursor:pointer}
.vt-plantas .vt-lista{display:grid;gap:12px;margin:16px 0;padding:0;list-style:none}
.vt-plantas .vt-lista li{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;padding-bottom:12px;border-bottom:1px solid var(--vt-line)}
.vt-plantas .vt-lista__item{margin:0}
.vt-plantas .vt-lista__ctrl{display:flex;align-items:center;gap:6px;margin:0}
.vt-plantas .vt-lista-barra{position:fixed;inset:auto 0 0;z-index:var(--vt-z-bar);display:flex;justify-content:center;padding:8px var(--vt-gutter) calc(8px + env(safe-area-inset-bottom));background:var(--vt-bone);box-shadow:0 -1px 0 var(--vt-line)}
.vt-plantas .vt-lista-barra[hidden]{display:none}
.vt-plantas .vt-lista-barra .vt-btn{justify-content:center;width:min(100%,420px)}

@media (prefers-reduced-motion:reduce){.vt-plantas .vt-necesidades a{transition:none}.vt-plantas .vt-necesidades a:hover{transform:none}}
EOF
```

- [ ] **Step 5: Verlas pasar y reconstruir**

```bash
cd ~/dev/viverosterra-e2e
(cd tools/site && python3 -m unittest tests.test_terra_plantas_css tests.test_shell tests.test_partials tests.test_vercel tests.test_activos 2>&1 | tail -1)
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
```

Expected: `OK`; `plantillas: 0 de 30` y `shell: 0 de 108` (ninguna página tiene aún `vt-plantas`); `?? public/css/terra-plantas.<hash>.css` y ` M tools/site/activos.json` (clave nueva con una sola copia).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add public/css/terra-plantas.css public/css/terra-plantas.*.css tools/site/activos.json tools/site/activos.py tools/site/shell.py \
  tools/site/partials.py vercel.json tools/site/tests/test_terra_plantas_css.py tools/site/tests/test_activos.py \
  tools/site/tests/test_shell.py tools/site/tests/test_partials.py tools/site/tests/test_vercel.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(css): hoja terra-plantas.css con copia inmutable, cargada por el shell en las páginas de plantas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Componentes de plantas

**Files:**
- Create: `tools/site/componentes_plantas.py`, `tools/site/tests/test_componentes_plantas.py`

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_componentes_plantas.py <<'EOF'
"""Componentes de las páginas de plantas (Etapa 2e)."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_plantas as cp  # noqa: E402
import datos  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402


class ComponentesPlantasTest(unittest.TestCase):
    def test_foto_de_especie_con_dimensiones_alt_y_pie_del_vivero(self):
        html = cp.foto_especie(cd.especie("palma-real"), 3)
        self.assertIn('src="/img/catalogo/palma-real-tampico.webp" width="480"', html)
        self.assertIn('loading="lazy"', html)
        self.assertIn('alt="Palma Real (Roystonea regia) en el vivero de Viveros Terra"', html)
        self.assertIn("<figcaption><b>Fig. 03</b> · Palma Real · En nuestro vivero</figcaption>", html)
        self.assertIn('fetchpriority="high"', cp.foto_especie(cd.especie("palma-real"), 1, "alta"))

    def test_precio_solo_de_datos(self):
        self.assertIn("desde <span class=\"vt-precio-marca\">$500</span> · tamaño chico",
                      cp.precio_especie(cd.especie("palma-real")))
        self.assertIn("$250", cp.precio_especie(cd.especie("flamboyan-tabachin")))
        self.assertNotIn("tamaño chico", cp.precio_especie(cd.especie("flamboyan-tabachin")))
        self.assertEqual(cp.precio_especie(cd.especie("palma-washingtona")), "")

    def test_tarjeta_de_especie_lleva_al_catalogo_y_a_su_guia(self):
        html = cp.especies((("palma-areca", "La más pedida para semisombra.", None),), "plantas")
        self.assertIn('<h3 class="vt-esp__nombre">Palma Areca</h3><p class="vt-esp__sci"><i>Dypsis lutescens</i></p>', html)
        self.assertIn('data-cta="plantas:catalogo" href="/catalogo?q=Palma%20Areca"', html)
        self.assertIn('href="/blog/palma-areca-tampico"', html)
        self.assertIn('<span class="vt-sr"> Palma Areca</span>', html)
        alto = cp.especies((("palma-areca", "En maceta.", "Hasta 2 m en maceta"),), "plantas")
        self.assertIn("<dd>Hasta 2 m en maceta</dd>", alto)

    def test_indice_de_subcategorias_con_desde_o_segun_cotizacion(self):
        items = [dict(titulo="Palmas", href="/palmas-tropicales-tampico", texto="t", img="/img/a.webp", ancho=560, alto=996,
                      unidad="tamaño chico"),
                 dict(titulo="Interior", href="/plantas-de-interior-tampico", texto="t", img="/img/b.webp", ancho=560,
                      alto=840, unidad="")]
        html = cp.indice_subcategorias(items)
        self.assertIn('desde <span class="vt-precio-marca">$250</span> tamaño chico', html)
        self.assertIn("Precio según cotización", html)

    def test_necesidades_con_conteo_real_y_enlace_medido(self):
        html = cp.necesidades((("salitre", "Cerca del mar", "Brisa salina.", {"uso": ["salitre"]}),), "plantas")
        self.assertIn('data-cta="plantas:necesidad-salitre" href="/catalogo?uso=salitre"', html)
        self.assertIn(f"{cd.cuenta({'uso': ['salitre']})} especies", html)

    def test_rejilla_con_117_botones_reales_y_datos_para_filtrar(self):
        html = cp.rejilla_catalogo()
        self.assertEqual(html.count('<button type="button" class="vt-btn vt-btn--linea vt-cat__add"'), 117)
        self.assertEqual(html.count('loading="eager"'), 4)
        self.assertEqual(html.count('fetchpriority="high"'), 1)
        olivo = re.search(r'<li class="vt-esp vt-cat" data-vt-esp="olivo-negro"[^>]*>', html).group(0)
        for attr in ('data-cat="arboles"', 'data-luz="sol"', 'data-tam="grande"', 'data-riego="moderado"',
                     'data-uso="banqueta salitre"', 'data-buscar="olivo negro bucida buceras'):
            self.assertIn(attr, olivo)
        self.assertNotIn("/api/img", html)

    def test_filtros_con_label_y_botones_con_aria_pressed(self):
        html = cp.filtros_catalogo(117)
        self.assertIn('<label for="vt-cat-q">', html)
        self.assertIn('role="search"', html)
        self.assertEqual(html.count('aria-pressed="false"'), 15)
        self.assertIn('data-vt-g="uso" data-vt-v="salitre"', html)
        self.assertIn("117 especies", html)

    def test_lista_en_dialogos_con_un_solo_enlace_de_whatsapp(self):
        html = cp.lista_catalogo("catalogo")
        self.assertEqual(html.count("<dialog"), 2)
        self.assertEqual(html.count("https://wa.me/"), 1)
        self.assertIn('data-cta="catalogo:sendWA" data-vt-o="enviar"', html)
        self.assertIn('<label for="vt-agregar-tam">', html)
        self.assertIn('role="status"', html)

    def test_pedido_especial_con_el_mensaje_de_main(self):
        html = cp.pedido_especial("catalogo")
        texto = unquote(re.search(r'href="https://wa\.me/\d+\?text=([^"]+)"', html).group(1))
        self.assertEqual(texto, cp.mensaje_especial(""))
        self.assertIn("No lo encontré en el catálogo", texto)
        self.assertIn('data-cta="catalogo:solEsp"', html)


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_componentes_plantas 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'componentes_plantas'`.

- [ ] **Step 3: Implementar `tools/site/componentes_plantas.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/componentes_plantas.py <<'EOF'
"""Componentes de las páginas de plantas (Etapa 2e): foto de especie con pie FIG. del vivero, tarjeta de especie, índice
de subcategorías con "desde", filtro por necesidad, buscador y filtros del catálogo, rejilla con botón real y los
diálogos de "Arma tu lista". Funciones puras: los textos de contenido/ son HTML en línea de confianza; los atributos y
los datos de especies se escapan aquí. Precios solo de datos.PRECIOS_ESPECIE y datos.DESDE_PLANTAS. Va aparte de
componentes.py, que ya pasa de 800 renglones."""
import componentes as c
import datos
from contenido import catalogo_datos as cd
from partials import WA_GLIFO, esc

VIVERO = "En nuestro vivero"
OPCIONES = (
    ("cat", "Tipo", (("arboles", "Árboles"), ("palmas", "Palmas"), ("plantas", "Plantas"))),
    ("luz", "Luz", (("sol", "Sol"), ("media", "Media sombra"), ("sombra", "Sombra"))),
    ("tam", "Tamaño adulto", tuple((k, t) for k, t, _m in cd.TAMANOS)),
    ("riego", "Riego", (("poco", "Poco"), ("moderado", "Moderado"), ("abundante", "Abundante"))),
    ("uso", "Uso", (("banqueta", "Banqueta"), ("interior", "Interior"), ("salitre", "Aguanta salitre"))),
)
OTRO_TAMANO = "Otro tamaño o medida especial"


def alt_especie(e):
    return f"{e['name']} ({e['sc']}) en el vivero de Viveros Terra"


def foto_especie(e, numero, carga="lazy"):
    """carga: "alta" (la primera del catálogo), "eager" o "lazy"."""
    loading = "lazy" if carga == "lazy" else "eager"
    prioridad = ' fetchpriority="high"' if carga == "alta" else ""
    return (f'<figure class="vt-esp__foto"><img src="{esc(e["img"])}" width="{e["ancho"]}" height="{e["alto"]}" '
            f'loading="{loading}"{prioridad} decoding="async" alt="{esc(alt_especie(e))}">'
            f'<figcaption><b>Fig. {numero:02d}</b> · {esc(e["name"])} · {VIVERO}</figcaption></figure>')


def datos_especie(e, altura=None):
    filas = (("Luz", e["luz"]), ("Riego", e["agua"]), ("Altura", altura or e["altura"]))
    celdas = "".join(f"<div><dt>{t}</dt><dd>{esc(v)}</dd></div>" for t, v in filas)
    return f'<dl class="vt-esp__datos">{celdas}</dl>'


def precio_especie(e):
    precio = datos.PRECIOS_ESPECIE.get(e["name"])
    if precio is None:
        return ""
    chico = " · tamaño chico" if e["cat"] == "palmas" else ""
    return f'<p class="vt-esp__precio">desde <span class="vt-precio-marca">{c.dinero(precio)}</span>{chico}</p>'


def _cabeza(e, numero, carga="lazy"):
    return (f'{foto_especie(e, numero, carga)}<h3 class="vt-esp__nombre">{esc(e["name"])}</h3>'
            f'<p class="vt-esp__sci"><i>{esc(e["sc"])}</i></p>')


def tarjeta_especie(e, numero, texto, tipo, altura=None):
    """Subcategorías y hub: foto del vivero, nombre, científico, luz/riego/altura, precio solo si datos.py lo tiene,
    texto propio de la página, "Agregar en Arma tu lista" (al catálogo con la especie buscada; terra.js lo mide como
    select_content) y la guía del blog si existe."""
    nombre = esc(e["name"])
    guia = cd.BLOG_ESPECIE.get(e["slug"])
    guia_html = (f'<a href="{esc(guia)}">Guía de cuidados<span class="vt-sr"> de {nombre}</span></a>' if guia else "")
    return (f'<li class="vt-esp">{_cabeza(e, numero)}{datos_especie(e, altura)}{precio_especie(e)}<p>{texto}</p>'
            f'<p class="vt-esp__acciones"><a data-cta="{esc(tipo)}:catalogo" href="{esc(cd.url_catalogo(q=e["name"]))}">'
            f'Agregar<span class="vt-sr"> {nombre}</span> en Arma tu lista</a>{guia_html}</p></li>')


def especies(items, tipo):
    """items: (slug, texto, altura propia de la página o None)."""
    filas = "".join(tarjeta_especie(cd.especie(s), n, t, tipo, a) for n, (s, t, a) in enumerate(items, 1))
    return f'<ul class="vt-esps">{filas}</ul>'


def indice_subcategorias(items):
    """Hub: foto, título con enlace (toda la fila lo abre, .vt-indice de terra.css), texto y "desde" de
    datos.DESDE_PLANTAS, o "Precio según cotización" si no hay un precio oficial."""
    filas = []
    for n, i in enumerate(items, 1):
        desde = datos.DESDE_PLANTAS[i["href"]]
        precio = (f'desde <span class="vt-precio-marca">{c.dinero(desde)}</span> {i["unidad"]}'.rstrip()
                  if desde is not None else f"Precio {datos.SEGUN_COTIZACION.lower()}")
        filas.append(f'<li><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" loading="lazy" '
                     f'decoding="async"><span class="vt-indice__n" aria-hidden="true">{n:02d}</span>'
                     f'<h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p>'
                     f'<p class="vt-indice__desde">{precio}</p><span class="vt-indice__ir" aria-hidden="true">→</span></li>')
    return f'<ol class="vt-indice">{"".join(filas)}</ol>'


def necesidades(items, tipo):
    """items: (clave, titulo, texto, filtro). Enlaces al catálogo con el filtro puesto y el conteo real del build."""
    filas = "".join(
        f'<li><a data-cta="{esc(tipo)}:necesidad-{esc(clave)}" href="{esc(cd.url_catalogo(filtro))}"><h3>{titulo}</h3>'
        f'<span>{texto}</span><span class="vt-necesidad__n">{cd.cuenta(filtro)} especies</span></a></li>'
        for clave, titulo, texto, filtro in items)
    return f'<ul class="vt-necesidades">{filas}</ul>'


def filtros_catalogo(total):
    grupos = "".join(
        f'<fieldset class="vt-filtro"><legend>{leyenda}</legend>' + "".join(
            f'<button type="button" class="vt-chip-p" data-vt-g="{g}" data-vt-v="{v}" aria-pressed="false">{t}</button>'
            for v, t in opciones) + "</fieldset>"
        for g, leyenda, opciones in OPCIONES)
    # Sin action: test_reglas solo admite formularios a formsubmit. Sin JS, Enter recarga la misma página con ?q=.
    return ('<form class="vt-buscador" role="search" aria-label="Buscar y filtrar plantas" data-vt-filtros>'
            '<div class="vt-campo"><label for="vt-cat-q">Busca por nombre, uso o luz</label>'
            '<div class="vt-control"><input id="vt-cat-q" type="search" name="q" autocomplete="off" '
            'placeholder="Ej. palma, banqueta, sombra"></div></div>'
            '<details class="vt-buscador__filtros" data-vt-plegable><summary>Filtros</summary>'
            f'<div class="vt-buscador__grupos">{grupos}</div></details>'
            f'<p class="vt-buscador__n"><span data-vt-o="cuenta" aria-live="polite">{total} especies</span>'
            '<button type="button" class="vt-buscador__limpiar" data-vt-limpiar hidden>Quitar filtros</button></p></form>')


def tarjeta_catalogo(e, numero):
    f = cd.filtros(e)
    atributos = " ".join(f'data-{g}="{esc(" ".join(f[g]))}"' for g in cd.GRUPOS)
    buscar = cd.normalizar(" ".join((e["name"], e["sc"], e["tipo"], e["luz"])))
    carga = "alta" if numero == 1 else "eager" if numero <= 4 else "lazy"
    nombre = esc(e["name"])
    guia = cd.BLOG_ESPECIE.get(e["slug"])
    guia_html = f'<p><a href="{esc(guia)}">Guía de cuidados<span class="vt-sr"> de {nombre}</span></a></p>' if guia else ""
    ficha = (f'<details class="vt-esp__ficha"><summary>Ficha<span class="vt-sr"> de {nombre}</span></summary>'
             f'<p>{esc(e["desc"])}</p><p><b>Tamaños:</b> {esc(", ".join(e["sz"]))}. Otras medidas: pregúntanos.</p>'
             f'{guia_html}</details>')
    return (f'<li class="vt-esp vt-cat" data-vt-esp="{esc(e["slug"])}" {atributos} data-buscar="{esc(buscar)}">'
            f'{_cabeza(e, numero, carga)}{datos_especie(e)}{precio_especie(e)}{ficha}'
            f'<button type="button" class="vt-btn vt-btn--linea vt-cat__add" data-vt-agregar="{esc(e["slug"])}">'
            f'+ Añadir<span class="vt-sr"> {nombre}</span> a mi lista</button></li>')


def rejilla_catalogo(especies_=None):
    lista = especies_ or cd.ORDENADAS
    return (f'<ul class="vt-esps vt-esps--cat" data-vt-rejilla aria-label="Especies del catálogo">'
            f'{"".join(tarjeta_catalogo(e, n) for n, e in enumerate(lista, 1))}</ul>'
            '<p class="vt-cat__vacio" data-vt-vacio hidden>No hay especies con esos filtros. Quita alguno o pídenos la '
            'que buscas aquí abajo.</p>')


def lista_catalogo(tipo):
    """Diálogo para añadir (tamaño o medida especial y piezas), diálogo de la lista con un solo enlace de WhatsApp
    (data-cta <tipo>:sendWA; vt-catalogo.js le pone el mensaje) y la barra "Mi lista"."""
    return (
        '<dialog class="vt-dialogo" id="vt-agregar" aria-labelledby="vt-agregar-t"><form method="dialog">'
        '<h2 id="vt-agregar-t" data-vt-o="nombre">Añadir a mi lista</h2>'
        '<p class="vt-esp__sci"><i data-vt-o="sci"></i></p>'
        '<div class="vt-campo"><label for="vt-agregar-tam">Tamaño</label><div class="vt-control">'
        '<select id="vt-agregar-tam" data-vt-campo="tam"></select></div></div>'
        f'<div class="vt-campo" data-vt-otro hidden><label for="vt-agregar-otro">{OTRO_TAMANO}</label>'
        '<div class="vt-control"><input id="vt-agregar-otro" type="text" data-vt-campo="otro" placeholder="Ej. 3.5 m">'
        '</div></div><div class="vt-campo"><label for="vt-agregar-n">Cantidad (piezas)</label>'
        '<div class="vt-cantidad"><button type="button" data-vt-menos aria-label="Una pieza menos">−</button>'
        '<input id="vt-agregar-n" type="number" inputmode="numeric" min="1" max="9999" value="1" data-vt-campo="n">'
        '<button type="button" data-vt-mas aria-label="Una pieza más">+</button></div></div>'
        '<p class="vt-dialogo__botones"><button type="submit" value="cancelar" class="vt-btn vt-btn--linea">Cancelar'
        '</button><button type="submit" value="agregar" class="vt-btn vt-btn--tinta">Agregar a mi lista</button></p>'
        '</form></dialog>'
        '<dialog class="vt-dialogo" id="vt-lista" aria-labelledby="vt-lista-t"><h2 id="vt-lista-t">Mi lista para cotizar'
        '</h2><p class="vt-promesa" data-vt-o="resumen">Tu lista está vacía.</p><ul class="vt-lista" data-vt-o="items"></ul>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:sendWA" data-vt-o="enviar" href="{esc(datos.wa_url(""))}" '
        f'target="_blank" rel="noopener" hidden>{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<p class="vt-dialogo__botones"><button type="button" class="vt-btn vt-btn--linea" data-vt-vaciar>Vaciar lista'
        '</button><button type="button" class="vt-btn vt-btn--linea" data-vt-cerrar>Seguir viendo</button></p>'
        f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p></dialog>'
        '<div class="vt-lista-barra" data-vt-barra-lista hidden><button type="button" class="vt-btn vt-btn--tinta" '
        'data-vt-abrir-lista>Mi lista <b data-vt-o="cuenta-lista">0</b></button>'
        '<p class="vt-sr" role="status" data-vt-o="aviso"></p></div>')


def mensaje_especial(texto):
    """El mensaje de solEsp() de main; con el campo vacío lleva el hueco ___ (igual que mensajeEspecial() del JS)."""
    valor = (texto or "").strip() or "___"
    return f"Hola Viveros Terra\n\nBusco: *{valor}*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?"


def pedido_especial(tipo):
    return ('<div class="vt-especial" data-vt-especial><div class="vt-campo"><label for="vt-especial-q">Planta, árbol, '
            'tamaño o medida que buscas</label><div class="vt-control"><input id="vt-especial-q" type="text" '
            'autocomplete="off" placeholder="Ej. palma phoenix de 4 m"></div></div>'
            f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:solEsp" href="{esc(datos.wa_url(mensaje_especial("")))}" '
            f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→'
            '</span></a></div>')
EOF
```

- [ ] **Step 4: Verlas pasar**

Run: `cd tools/site && python3 -m unittest tests.test_componentes_plantas 2>&1 | tail -1`
Expected: `OK`. (Los 15 `aria-pressed` son 3 + 3 + 3 + 3 + 3 botones de `OPCIONES`.)

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/componentes_plantas.py tools/site/tests/test_componentes_plantas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(componentes): foto de especie del vivero, tarjetas, filtro por necesidad, rejilla y lista del catálogo" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: `vt-catalogo.js`: filtros en la URL y "Arma tu lista"

**Files:**
- Create: `public/js/vt-catalogo.js`, `public/js/tests/vt-catalogo.test.js`

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2e
cat > public/js/tests/vt-catalogo.test.js <<'EOF'
const test = require('node:test');
const assert = require('node:assert/strict');
const c = require('../vt-catalogo.js');
const casos = require('./casos-catalogo.json');

test('el mensaje de la lista es el mismo que armaba sendWA() en main', () => {
  for (const { lista, mensaje } of casos.mensajes) assert.equal(c.mensajeLista(lista), mensaje);
  assert.equal(c.mensajeLista([]), '');
  assert.ok(c.enlaceLista(casos.mensajes[0].lista).startsWith('https://wa.me/528333268008?text=Hola%20Viveros%20Terra'));
});

test('agregar: misma especie y tamaño actualiza la cantidad, otro tamaño es otra línea y no muta', () => {
  const uno = c.agregar([], { name: 'Neem', sc: 'Azadirachta indica', sz: '1 m', qty: 2 });
  const dos = c.agregar(uno, { name: 'Neem', sc: 'Azadirachta indica', sz: '1 m', qty: 5 });
  const tres = c.agregar(dos, { name: 'Neem', sc: 'Azadirachta indica', sz: '2-3 m', qty: 1 });
  assert.deepEqual(uno.map((i) => i.qty), [2]);
  assert.deepEqual(dos.map((i) => i.qty), [5]);
  assert.deepEqual(tres.map((i) => [i.sz, i.qty]), [['1 m', 5], ['2-3 m', 1]]);
  assert.deepEqual(c.cambiar(tres, 1, -1).map((i) => i.qty), [5, 1]);
  assert.deepEqual(c.quitar(tres, 0).map((i) => i.sz), ['2-3 m']);
  assert.equal(c.resumen(tres), '2 variedades · 6 piezas');
});

test('cantidad entre 1 y 9999', () => {
  assert.equal(c.cantidad('0'), 1);
  assert.equal(c.cantidad('abc'), 1);
  assert.equal(c.cantidad('12'), 12);
  assert.equal(c.cantidad(100000), 9999);
});

test('filtros en la URL: ida y vuelta, mismo formato que catalogo_datos.url_catalogo', () => {
  const f = c.leerFiltros('?q=palma%20real&luz=media,sombra&uso=salitre');
  assert.deepEqual(f, { q: 'palma real', cat: [], luz: ['media', 'sombra'], tam: [], riego: [], uso: ['salitre'] });
  assert.equal(c.escribirFiltros(f), '?q=palma%20real&luz=media,sombra&uso=salitre');
  assert.equal(c.escribirFiltros(c.leerFiltros('')), '');
  assert.equal(c.hayFiltros(c.leerFiltros('')), false);
});

test('coincide: O dentro de un grupo, Y entre grupos y búsqueda sin acentos', () => {
  const d = { cat: 'palmas', luz: 'media', tam: 'grande', riego: 'moderado', uso: 'interior salitre', buscar: 'palma areca dypsis lutescens' };
  assert.equal(c.coincide(d, c.leerFiltros('?luz=sol,media')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?luz=sol')), false);
  assert.equal(c.coincide(d, c.leerFiltros('?cat=palmas&uso=banqueta')), false);
  assert.equal(c.coincide(d, c.leerFiltros('?q=Árec')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?q=palma%20lutescens')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?q=olivo')), false);
});

test('mensaje de una especie que no está en el catálogo', () => {
  assert.equal(c.mensajeEspecial('  Palma phoenix 4 m '), 'Hola Viveros Terra\n\nBusco: *Palma phoenix 4 m*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?');
  assert.ok(c.mensajeEspecial('').includes('*___*'));
});
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd ~/dev/viverosterra-e2e && node --test public/js/tests/vt-catalogo.test.js 2>&1 | grep -E "Cannot find module|^ℹ fail"`
Expected: `Cannot find module '../vt-catalogo.js'`.

- [ ] **Step 3: Implementar `public/js/vt-catalogo.js`**

```bash
cd ~/dev/viverosterra-e2e
cat > public/js/vt-catalogo.js <<'EOF'
/* Viveros Terra · vt-catalogo.js · "Arma tu lista" del catálogo (Etapa 2e).
   - Filtra la rejilla, que ya viene en el HTML, con el buscador y los botones de filtro. El estado vive en la URL
     (?q=&cat=&luz=&tam=&riego=&uso=): el hub enlaza filtros (/catalogo?luz=sol) y la búsqueda se puede compartir.
   - Arma la lista con <dialog>: tamaño (o medida especial) y piezas por especie. La misma especie con el mismo tamaño
     actualiza la cantidad, como confirmAdd() de main. La lista es [{name, sc, sz, qty}].
   - El enlace "Cotizar por WhatsApp" de la lista lleva un solo mensaje, el mismo que armaba sendWA() en main (casos en
     public/js/tests/casos-catalogo.json), con data-cta="catalogo:sendWA": terra.js lo mide (generate_lead con el mismo
     cta_id que VTMedicion.whatsapp('sendWA') de main) y lo firma al hacer clic. Sin window.open.
   El texto de las especies llega del HTML (data-*) y de #vt-catalogo-datos; nunca se usa innerHTML.
   Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const WA = 'https://wa.me/528333268008?text=';
  const GRUPOS = ['cat', 'luz', 'tam', 'riego', 'uso'];
  const MAXIMO = 9999;
  const OTRO = '__otro__';

  function normalizar(texto) {
    return String(texto || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  }

  function leerFiltros(search) {
    const p = new URLSearchParams(search || '');
    const f = { q: p.get('q') || '' };
    GRUPOS.forEach((g) => { f[g] = (p.get(g) || '').split(',').map((v) => v.trim()).filter(Boolean); });
    return f;
  }

  function escribirFiltros(f) {
    const partes = f.q ? ['q=' + encodeURIComponent(f.q)] : [];
    GRUPOS.forEach((g) => { if (f[g] && f[g].length) partes.push(g + '=' + f[g].map(encodeURIComponent).join(',')); });
    return partes.length ? '?' + partes.join('&') : '';
  }

  function hayFiltros(f) {
    return Boolean(f.q) || GRUPOS.some((g) => f[g].length > 0);
  }

  // d: dataset de la tarjeta. Dentro de un grupo basta una opción; entre grupos, todas (catalogo_datos.coincide).
  function coincide(d, f) {
    const enGrupos = GRUPOS.every((g) => {
      if (!f[g] || !f[g].length) return true;
      const valores = String(d[g] || '').split(' ');
      return f[g].some((v) => valores.indexOf(v) >= 0);
    });
    if (!enGrupos) return false;
    const q = normalizar(f.q);
    return !q || q.split(' ').every((palabra) => String(d.buscar || '').indexOf(palabra) >= 0);
  }

  function cantidad(valor) {
    return Math.max(1, Math.min(MAXIMO, parseInt(valor, 10) || 1));
  }

  function agregar(lista, item) {
    const i = lista.findIndex((x) => x.name === item.name && x.sz === item.sz);
    if (i >= 0) return lista.map((x, j) => (j === i ? { ...x, qty: item.qty } : x));
    return [...lista, item];
  }

  function cambiar(lista, i, delta) {
    return lista.map((x, j) => (j === i ? { ...x, qty: cantidad(x.qty + delta) } : x));
  }

  function quitar(lista, i) {
    return lista.filter((_x, j) => j !== i);
  }

  function plural(n, uno, varios) {
    return n + ' ' + (n === 1 ? uno : varios);
  }

  function resumen(lista) {
    const total = lista.reduce((s, i) => s + i.qty, 0);
    return plural(lista.length, 'variedad', 'variedades') + ' · ' + plural(total, 'pieza', 'piezas');
  }

  function mensajeLista(lista) {
    if (!lista.length) return '';
    const lineas = lista.map((i) => `• ${i.name} (${i.sz}) × ${i.qty}`).join('\n');
    const total = lista.reduce((s, i) => s + i.qty, 0);
    return `Hola Viveros Terra\n\nQuisiera cotizar lo siguiente:\n\n${lineas}\n\nTotal: ${lista.length} variedad${lista.length > 1 ? 'es' : ''}, ${total} unidad${total > 1 ? 'es' : ''}\n\n¿Pueden darme precio y disponibilidad?`;
  }

  function enlaceLista(lista) {
    return WA + encodeURIComponent(mensajeLista(lista));
  }

  function mensajeEspecial(texto) {
    const valor = String(texto || '').trim() || '___';
    return 'Hola Viveros Terra\n\nBusco: *' + valor + '*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?';
  }

  // ---------- DOM ----------
  function filtrar(doc, win) {
    const caja = doc.querySelector('[data-vt-filtros]');
    const rejilla = doc.querySelector('[data-vt-rejilla]');
    if (!caja || !rejilla) return;
    const tarjetas = Array.from(rejilla.querySelectorAll('[data-vt-esp]'));
    const q = caja.querySelector('input[type="search"]');
    const botones = Array.from(caja.querySelectorAll('[data-vt-g]'));
    const cuenta = caja.querySelector('[data-vt-o="cuenta"]');
    const limpiar = caja.querySelector('[data-vt-limpiar]');
    const vacio = doc.querySelector('[data-vt-vacio]');
    let filtros = leerFiltros(win.location.search);

    function aplicar(escribir) {
      let visibles = 0;
      tarjetas.forEach((t) => {
        const ok = coincide(t.dataset, filtros);
        t.hidden = !ok;
        if (ok) visibles += 1;
      });
      cuenta.textContent = plural(visibles, 'especie', 'especies');
      if (vacio) vacio.hidden = visibles > 0;
      limpiar.hidden = !hayFiltros(filtros);
      botones.forEach((b) => b.setAttribute('aria-pressed', String(filtros[b.dataset.vtG].indexOf(b.dataset.vtV) >= 0)));
      if (escribir) win.history.replaceState(null, '', win.location.pathname + escribirFiltros(filtros));
    }

    caja.addEventListener('submit', (e) => e.preventDefault());
    q.addEventListener('input', () => { filtros = { ...filtros, q: q.value }; aplicar(true); });
    botones.forEach((b) => b.addEventListener('click', () => {
      const g = b.dataset.vtG;
      const v = b.dataset.vtV;
      const activos = filtros[g].indexOf(v) >= 0 ? filtros[g].filter((x) => x !== v) : [...filtros[g], v];
      filtros = { ...filtros, [g]: activos };
      aplicar(true);
    }));
    limpiar.addEventListener('click', () => { filtros = leerFiltros(''); q.value = ''; aplicar(true); q.focus(); });
    q.value = filtros.q;
    aplicar(false);
  }

  function fila(doc, it, i) {
    const li = doc.createElement('li');
    const texto = doc.createElement('p');
    texto.className = 'vt-lista__item';
    const nombre = doc.createElement('b');
    nombre.textContent = it.name;
    texto.append(nombre, ' · ' + it.sz);
    const ctrl = doc.createElement('p');
    ctrl.className = 'vt-lista__ctrl';
    const boton = (accion, visible, etiqueta) => {
      const b = doc.createElement('button');
      b.type = 'button';
      b.dataset.accion = accion;
      b.dataset.i = String(i);
      b.textContent = visible;
      b.setAttribute('aria-label', etiqueta);
      return b;
    };
    const n = doc.createElement('span');
    n.textContent = String(it.qty);
    ctrl.append(boton('menos', '−', 'Una pieza menos de ' + it.name), n, boton('mas', '+', 'Una pieza más de ' + it.name),
      boton('quitar', 'Quitar', 'Quitar ' + it.name + ' de la lista'));
    li.append(texto, ctrl);
    return li;
  }

  function armarLista(doc, win) {
    const fuente = doc.getElementById('vt-catalogo-datos');
    const dAgregar = doc.getElementById('vt-agregar');
    const dLista = doc.getElementById('vt-lista');
    const barra = doc.querySelector('[data-vt-barra-lista]');
    if (!fuente || !dAgregar || !dLista || !barra || typeof dAgregar.showModal !== 'function') return;
    const especies = JSON.parse(fuente.textContent);
    const sel = dAgregar.querySelector('[data-vt-campo="tam"]');
    const otro = dAgregar.querySelector('[data-vt-campo="otro"]');
    const cajaOtro = dAgregar.querySelector('[data-vt-otro]');
    const n = dAgregar.querySelector('[data-vt-campo="n"]');
    const enviar = dLista.querySelector('[data-vt-o="enviar"]');
    const items = dLista.querySelector('[data-vt-o="items"]');
    const aviso = barra.querySelector('[data-vt-o="aviso"]');
    let seleccion = [];
    let actual = null;
    let origen = null;

    function pintar() {
      barra.hidden = seleccion.length === 0;
      barra.querySelector('[data-vt-o="cuenta-lista"]').textContent = String(seleccion.length);
      dLista.querySelector('[data-vt-o="resumen"]').textContent = seleccion.length ? resumen(seleccion) : 'Tu lista está vacía.';
      enviar.hidden = seleccion.length === 0;
      enviar.setAttribute('href', enlaceLista(seleccion));
      items.replaceChildren(...seleccion.map((it, i) => fila(doc, it, i)));
    }

    doc.addEventListener('click', (e) => {
      const b = e.target.closest ? e.target.closest('[data-vt-agregar]') : null;
      if (!b || !especies[b.dataset.vtAgregar]) return;
      actual = especies[b.dataset.vtAgregar];
      origen = b;
      const previo = seleccion.find((x) => x.name === actual.name);
      dAgregar.querySelector('[data-vt-o="nombre"]').textContent = actual.name;
      dAgregar.querySelector('[data-vt-o="sci"]').textContent = actual.sc;
      sel.replaceChildren(...actual.sz.map((t) => new win.Option(t, t)), new win.Option('Otro tamaño o medida especial', OTRO));
      sel.value = previo && actual.sz.indexOf(previo.sz) >= 0 ? previo.sz : actual.sz[0];
      n.value = String(previo ? previo.qty : 1);
      otro.value = '';
      cajaOtro.hidden = true;
      dAgregar.returnValue = '';
      dAgregar.showModal();
      sel.focus();
    });
    sel.addEventListener('change', () => { cajaOtro.hidden = sel.value !== OTRO; if (!cajaOtro.hidden) otro.focus(); });
    dAgregar.querySelector('[data-vt-menos]').addEventListener('click', () => { n.value = String(cantidad(cantidad(n.value) - 1)); });
    dAgregar.querySelector('[data-vt-mas]').addEventListener('click', () => { n.value = String(cantidad(cantidad(n.value) + 1)); });
    // El envío del <form method="dialog"> llega antes que el evento close (que va en cola): la lista se actualiza aquí,
    // en el mismo turno del clic o del Enter, y close solo devuelve el foco.
    dAgregar.querySelector('form').addEventListener('submit', (e) => {
      if (!actual || !e.submitter || e.submitter.value !== 'agregar') return;
      const sz = sel.value === OTRO ? (otro.value.trim() || 'Medida especial') : sel.value;
      const qty = cantidad(n.value);
      seleccion = agregar(seleccion, { name: actual.name, sc: actual.sc, sz, qty });
      pintar();
      aviso.textContent = 'Agregaste ' + actual.name + ' (' + sz + ') × ' + qty + '. Llevas ' + resumen(seleccion) + '.';
    });
    dAgregar.addEventListener('close', () => {
      actual = null;
      if (origen) origen.focus();
    });
    barra.querySelector('[data-vt-abrir-lista]').addEventListener('click', () => { pintar(); dLista.showModal(); });
    dLista.querySelector('[data-vt-cerrar]').addEventListener('click', () => dLista.close());
    dLista.querySelector('[data-vt-vaciar]').addEventListener('click', () => { seleccion = []; pintar(); dLista.close(); });
    items.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-accion]');
      if (!b) return;
      const i = Number(b.dataset.i);
      seleccion = b.dataset.accion === 'quitar' ? quitar(seleccion, i) : cambiar(seleccion, i, b.dataset.accion === 'mas' ? 1 : -1);
      pintar();
      if (!seleccion.length) dLista.querySelector('[data-vt-cerrar]').focus();
    });
  }

  function especial(doc) {
    const caja = doc.querySelector('[data-vt-especial]');
    if (!caja) return;
    const campo = caja.querySelector('input');
    const enlace = caja.querySelector('a[data-cta]');
    campo.addEventListener('input', () => enlace.setAttribute('href', WA + encodeURIComponent(mensajeEspecial(campo.value))));
  }

  const api = { GRUPOS, normalizar, leerFiltros, escribirFiltros, hayFiltros, coincide, cantidad, agregar, cambiar,
    quitar, resumen, mensajeLista, enlaceLista, mensajeEspecial };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTCatalogo = Object.freeze(api);
  const iniciar = () => { filtrar(document, root); armarLista(document, root); especial(document); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
EOF
```

- [ ] **Step 4: Verlas pasar**

Run: `cd ~/dev/viverosterra-e2e && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"`
Expected: `ℹ pass 56` y `ℹ fail 0` (50 de antes + 6).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add public/js/vt-catalogo.js public/js/tests/vt-catalogo.test.js
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(catalogo): vt-catalogo.js con filtros en la URL y la lista en un solo mensaje (el mismo de main)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Plantilla `hub_categoria` y el hub de plantas

**Files:**
- Create: `tools/site/plantillas/hub_categoria.py`, `tools/site/contenido/plantas_comun.py`, `tools/site/contenido/plantas_hub.py`, `tools/site/tests/test_plantas.py`, `tools/site/tests/test_plantas_paridad.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `tools/servicios/tests/test_pagos.py`, `tools/site/tests/test_plantas_reglas.py` (`PENDIENTES`)

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_plantas.py` (crece en las Tareas 10 y 11):

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_plantas.py <<'EOF'
"""Páginas de plantas con plantilla (Etapa 2e): secuencia del spec, precios de datos.py, fotos del vivero, mensajes,
enlaces y JSON-LD."""
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

PUBLIC = paginas.PUBLIC


def html(ruta):
    return (PUBLIC / dict((r, s) for r, s, _p, _c in generar.PAGINAS)[ruta]).read_text(encoding="utf-8")


def grafo(h):
    return [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
            for n in json.loads(b).get("@graph", [])]


def mensajes(h):
    return [unquote(t) for t in re.findall(r'href="https://wa\.me/\d+\?text=([^"]*)"', h)]


class HubTest(unittest.TestCase):
    RUTA = "/plantas-palmas-arboles-tampico"

    def setUp(self):
        self.h = html(self.RUTA)

    def test_orden_de_secciones_del_spec(self):
        ids = ["vt-h1", "vt-h-necesidad", "vt-h-subcategorias", "vt-h-destacadas", "vt-h-lista", "vt-h-garantia",
               "vt-h-faq", "vt-cierre-titulo"]
        posiciones = [self.h.index(f'id="{i}"') for i in ids]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_hoja_de_plantas_sin_css_viejo_ni_proxy(self):
        self.assertIn('<body class="vt-pagina vt-plantas">', self.h)
        self.assertIn("/css/terra-plantas.", self.h)
        for viejo in ("tailwind.css", "design-system.css", "servicios.css", "fonts.googleapis", "/api/img"):
            self.assertNotIn(viejo, self.h)

    def test_necesidades_enlazan_el_catalogo_con_filtro(self):
        for filtro in ("luz=sol", "luz=media,sombra", "uso=salitre", "tam=chica", "tam=mediana", "tam=grande"):
            self.assertIn(f'href="/catalogo?{filtro}"', self.h)

    def test_subcategorias_con_desde_de_datos_o_segun_cotizacion(self):
        self.assertIn('href="/palmas-tropicales-tampico"', self.h)
        self.assertEqual(self.h.count("Precio según cotización"), 3)
        self.assertEqual(len(re.findall(r'<p class="vt-indice__desde">desde', self.h)), 2)

    def test_cada_whatsapp_lleva_su_plantilla_y_la_firma(self):
        propios = [m for m in mensajes(self.h) if "Plantas que busco: ___" in m]
        self.assertGreaterEqual(len(propios), 2)  # portada y cierre
        self.assertTrue(all(m.endswith(datos.FIRMA) for m in mensajes(self.h)))

    def test_json_ld_sin_localbusiness_recortado(self):
        tipos = {n["@type"] for n in grafo(self.h)}
        self.assertTrue({"FAQPage", "BreadcrumbList", "ItemList"} <= tipos)
        self.assertNotIn("LocalBusiness", tipos)


if __name__ == "__main__":
    unittest.main()
EOF
```

`tools/site/tests/test_plantas_paridad.py`:

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/tests/test_plantas_paridad.py <<'EOF'
"""Paridad de especies (Etapa 2e): cada especie que publicaba una página de plantas sigue en ella con su nombre
científico (o la corrección declarada), o su contenido dice a qué página se fue (PARIDAD["especies"]["reemplazos"]:
nombre → (ruta, nombre allá)) o por qué se retiró (PARIDAD["especies"]["retirados"]). Los enlaces al blog no se pierden."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paridad_plantas as pp  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

CAPTURA = json.loads(pp.CAPTURA.read_text(encoding="utf-8"))
MIGRADAS = {r for r, _s, _p, _c in generar.PAGINAS} & set(pp.RUTAS)


def nombres(ruta):
    return {n.casefold(): s for n, s in pp.extraer(ruta)["especies"]}


class PlantasParidadTest(unittest.TestCase):
    def test_cada_especie_sigue_se_mueve_o_se_retira_con_motivo(self):
        for ruta in sorted(MIGRADAS):
            mapa = generar.cargar(generar.contenido_de(ruta)).PARIDAD.get("especies", {"reemplazos": {}, "retirados": {}})
            actuales = nombres(ruta)
            for nombre, cientifico in CAPTURA[ruta]["especies"]:
                with self.subTest(ruta=ruta, especie=nombre):
                    if nombre.casefold() in actuales:
                        if cientifico:
                            self.assertEqual(actuales[nombre.casefold()], cd.CIENTIFICOS_CORREGIDOS.get(cientifico, cientifico))
                    elif nombre in mapa["reemplazos"]:
                        destino, otro = mapa["reemplazos"][nombre]
                        self.assertIn(otro.casefold(), nombres(destino) if destino in MIGRADAS else {otro.casefold()})
                    else:
                        self.assertGreater(len(mapa["retirados"].get(nombre, "")), 20)

    def test_enlaces_al_blog_no_se_pierden(self):
        for ruta in sorted(MIGRADAS):
            with self.subTest(ruta=ruta):
                self.assertLessEqual(set(CAPTURA[ruta]["blog"]), set(pp.extraer(ruta)["blog"]))


if __name__ == "__main__":
    unittest.main()
EOF
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_plantas 2>&1 | tail -3`
Expected: `StopIteration` o `KeyError: '/plantas-palmas-arboles-tampico'` (la ruta aún no está en `generar.PAGINAS`).

- [ ] **Step 3: Contenido compartido `tools/site/contenido/plantas_comun.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/contenido/plantas_comun.py <<'EOF'
"""Lo que comparten las páginas de plantas (Etapa 2e): garantía con condiciones, filtro por necesidad, índice de
subcategorías, preguntas de entrega y pago, guías del blog por tema, migas y nodos de JSON-LD. Solo datos."""
import datos
from contenido import catalogo_datos as cd

SITE = datos.SITIO
HUB = "/plantas-palmas-arboles-tampico"
NEGOCIO = f"{SITE}/#negocio"  # la entidad única de las demás páginas (el nodo completo vive en la home)

GARANTIA = {
    "titulo": "Garantía de 30 días en las plantas que sembramos",
    "grande": "30", "unidad": "días",
    "resumen": f'{datos.GARANTIA_PLANTAS} <a href="/politicas#garantia-plantas">Condiciones de la garantía</a>',
    "puntos": (("En las plantas, palmas y árboles que sembramos nosotros", True),
               ("Con el riego y los cuidados que te indicamos al entregar", True),
               ("Te decimos antes de sembrar qué especie va en sol, sombra o cerca del mar", True),
               ("Si te las llevas y las siembras tú, no aplica la garantía de arraigo", False)),
    "pie": f"Recoges en {datos.DOMICILIO_CORTO} o te las llevamos en Tampico, Madero y Altamira.",
}

# (clave, título, texto, filtro del catálogo). El conteo lo pone componentes_plantas.necesidades() en el build.
NECESIDADES = (
    ("sol", "Sol directo todo el día", "Florecen y aguantan el calor del mediodía.", {"luz": ["sol"]}),
    ("sombra", "Sombra o media sombra", "Patios techados, interiores y jardines bajo árboles.",
     {"luz": ["media", "sombra"]}),
    ("salitre", "Cerca del mar (salitre)", "Aguantan la brisa salina de Madero y Miramar.", {"uso": ["salitre"]}),
    ("chica", "Chicas: hasta 1.5 m", "Macetas, arriates y bordes.", {"tam": ["chica"]}),
    ("mediana", "Medianas: de 1.5 a 5 m", "Setos, esquinas y jardines medianos.", {"tam": ["mediana"]}),
    ("grande", "Grandes: más de 5 m", "Sombra, banquetas y jardines amplios.", {"tam": ["grande"]}),
)

_PORTADAS = "/img/portadas"
# Índice de subcategorías del hub (y "otras subcategorías" en cada una). El "desde" sale de datos.DESDE_PLANTAS.
SUBCATEGORIAS = (
    {"titulo": "Palmas tropicales", "href": "/palmas-tropicales-tampico",
     "texto": "Areca, coco plumoso, palma real, washingtonia, del viajero y exóticas.",
     "img": f"{_PORTADAS}/palma-real-jardin-residencial-tampico-sm.webp", "ancho": 560, "alto": 996,
     "unidad": "tamaño chico"},
    {"titulo": "Plantas para jardín", "href": "/plantas-para-jardin-tampico",
     "texto": "Ornamentales, tropicales y de cobertura para sol, humedad y salitre.",
     "img": f"{_PORTADAS}/jardin-residencial-tropical-tampico-sm.webp", "ancho": 560, "alto": 373, "unidad": ""},
    {"titulo": "Árboles ornamentales", "href": "/arboles-ornamentales-tampico",
     "texto": "De sombra y de flor: flamboyán, crespón, jacaranda, palo de rosa y más.",
     "img": f"{_PORTADAS}/arboles-tampico-viveros-terra-sm.webp", "ancho": 560, "alto": 747, "unidad": ""},
    {"titulo": "Árboles para banqueta", "href": "/arboles-para-banqueta-tampico",
     "texto": "Especies de raíz profunda para frentes y camellones.",
     "img": f"{_PORTADAS}/arboles-vivero-tampico-mayoreo-sm.webp", "ancho": 560, "alto": 840, "unidad": ""},
    {"titulo": "Plantas de interior", "href": "/plantas-de-interior-tampico",
     "texto": "Para casas y oficinas con poca luz y aire acondicionado.",
     "img": f"{_PORTADAS}/plantas-ornamentales-tampico-viveros-terra-sm.webp", "ancho": 560, "alto": 840,
     "unidad": ""},
)

PREGUNTA_ENTREGA = ("¿Hacen entrega de plantas a domicilio en Tampico?",
                    "Sí. Entregamos plantas, palmas y árboles en Tampico, Ciudad Madero y Altamira; para Pánuco, la "
                    "Huasteca y zonas alejadas coordinamos la entrega según el volumen. También puedes recoger en "
                    f"{datos.CALLE}, {datos.CIUDAD} ({datos.REFERENCIA.lower()}).")
PREGUNTA_PAGO = ("¿Cómo se paga un pedido de plantas?",
                 f"{datos.ANTICIPO} Te mandamos la cotización por WhatsApp con el total antes de confirmar.")

LISTA = {"titulo": "Arma tu lista y cotiza en un solo mensaje",
         "texto": (f"En el catálogo están {len(cd.ESPECIES)} especies del vivero con foto, luz, riego y altura. Añade las "
                   "que te interesan con su tamaño y piezas, y mándanos la lista completa por WhatsApp en un solo "
                   "mensaje: te respondemos con precio por tamaño.")}


def migas(nombre=None):
    """Visibles: Inicio › Plantas y palmas (› subcategoría)."""
    if nombre is None:
        return (("Inicio", "/"), ("Plantas y palmas", None))
    return (("Inicio", "/"), ("Plantas y palmas", HUB), (nombre, None))


def migas_ld(nombre=None, ruta=None):
    items = [("Inicio", SITE), ("Plantas y palmas", f"{SITE}{HUB}")] + ([(nombre, f"{SITE}{ruta}")] if nombre else [])
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(items, 1)]}


def lista_ld(nombre, especies_):
    """ItemList de las especies de la página (nombre y científico), sin precios."""
    return {"@type": "ItemList", "name": nombre, "numberOfItems": len(especies_), "itemListElement": [
        {"@type": "ListItem", "position": i, "name": f"{cd.especie(s)['name']} ({cd.especie(s)['sc']})"}
        for i, s in enumerate(especies_, 1)]}
EOF
```

- [ ] **Step 4: Plantilla `tools/site/plantillas/hub_categoria.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/plantillas/hub_categoria.py <<'EOF'
"""Plantilla de hub de categoría (spec §3.3): ruta visible → H1 con precio "desde" (solo de datos.py) y CTA → filtro
por necesidad (sol/sombra, salitre, tamaño; enlaces al catálogo con el filtro puesto) → subcategorías con "desde $" →
especies con foto del vivero → tabla de precios (palmas) → "Arma tu lista" (un solo mensaje) → garantía con condiciones
→ FAQ → guías del blog → relacionados → CTA final. La usan /plantas-palmas-arboles-tampico y sus 5 subcategorías; cada
sección después de la portada es opcional según el contenido (el orden no cambia). Sin JS propio."""
import componentes as c
import componentes_plantas as cp
from plantillas import base

CONTEXTO = "https://schema.org"


def _necesidad(k, n):
    x = k["necesidad"]
    return c.bloque(n, "Por necesidad", "vt-h-necesidad", x["titulo"], cp.necesidades(x["items"], k["tipo"]),
                    lede=x["lede"], tinte=True)


def _subcategorias(k, n):
    x = k["subcategorias"]
    return c.bloque(n, "Subcategorías", "vt-h-subcategorias", x["titulo"], cp.indice_subcategorias(x["items"]),
                    lede=x.get("lede"))


def _especies(k, n):
    x = k["especies"]
    nota = f'<p class="vt-promesa">{x["nota"]}</p>' if x.get("nota") else ""
    return c.bloque(n, x.get("rotulo", "En el vivero"), x.get("id", "vt-h-especies"), x["titulo"],
                    cp.especies(x["items"], k["tipo"]) + nota, lede=x.get("lede"))


def _precios(k, n):
    x = k["precios"]
    tabla = c.tabla_especies(x["filas"], x["caption"], x["grupo"])
    return c.bloque(n, "Precios", "vt-h-precios", x["titulo"], tabla + f'<p class="vt-promesa">{x["nota"]}</p>',
                    lede=x.get("lede"), tinte=True, id_seccion="precios")


def _lista(k, n):
    x = k["lista"]
    cuerpo = (f'<p>{x["texto"]}</p><p class="vt-cta"><a class="vt-btn vt-btn--tinta" data-cta="{k["tipo"]}:catalogo" '
              f'href="{x.get("href", "/catalogo")}">Arma tu lista<span class="vt-flecha" aria-hidden="true">→</span></a></p>')
    return c.bloque(n, "Arma tu lista", "vt-h-lista", x["titulo"], cuerpo)


def _garantia(k, n):
    return c.garantia(dict(k["garantia"], numero=n, id_titulo="vt-h-garantia", rotulo="Garantía"))


def _faq(k, n):
    x = k["faq"]
    return c.bloque_dos(n, "Preguntas", "vt-h-faq", x["titulo"], "", c.faq(x["preguntas"]), tinte=True)


def _guias(k, n):
    x = k["guias"]
    return c.bloque(n, "Guías", "vt-h-guias", x["titulo"], c.guias(x["items"]))


def _relacionados(k, n):
    x = k["relacionados"]
    return c.bloque(n, "También", "vt-h-rel", x["titulo"], c.relacionados(x["items"]), tinte=True)


SECCIONES = (("necesidad", _necesidad), ("subcategorias", _subcategorias), ("especies", _especies),
             ("destacadas", lambda k, n: _especies(dict(k, especies=k["destacadas"]), n)), ("precios", _precios),
             ("lista", _lista), ("garantia", _garantia), ("faq", _faq), ("guias", _guias),
             ("relacionados", _relacionados))


def render(k):
    tipo = k["tipo"]
    secciones = [c.portada(k["portada"], tipo, k["migas"])]
    for clave, armar in SECCIONES:
        if k.get(clave):
            secciones.append(armar(k, len(secciones)))
    ci = k["cierre"]
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))
    j = k["jsonld"]
    speakable = {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}
    grafo = [*j.get("nodos", ()), c.faq_jsonld(k["faq"]["preguntas"]), j["migas"], speakable]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), clase_body="vt-pagina vt-plantas")
EOF
```

- [ ] **Step 5: Contenido del hub `tools/site/contenido/plantas_hub.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/contenido/plantas_hub.py <<'EOF'
"""Contenido de /plantas-palmas-arboles-tampico (hub de plantas). Plantilla: plantillas/hub_categoria.py.

Precios (decisión del dueño, 2026-11-07): palmas con datos.PALMAS_PRECIO y flamboyán desde $250; nada más. Se retiran los
"desde" sin confirmar de main (washingtonia, viajero y kerpis $500, cycas $700, palma bambú $1,000, cola de zorro $1,500,
ficus $200, neem y trueno $300, tabachín $350, laurel $500, tulipán africano $600; preguntas 1–3 al dueño), las dos
opiniones sin permiso (Martha R., Constructora Arce; pregunta 8), "asesoría sin costo" y "más de 18 años". Las fotos de
especie dejan /api/img: salen del vivero (contenido/catalogo_especies.json). Título, robots y canonical como estaban
(los títulos son de la Etapa 3); la descripción de Open Graph decía "Desde $200" (PARIDAD["meta"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = pc.HUB
URL = f"{SITE}{RUTA}"
TIPO = "plantas"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
FLAMBOYAN = f"Flamboyán desde {dinero(P['flamboyan'])}"
PALMAS_EN_CATALOGO = cd.cuenta({"cat": ["palmas"]})
OG_DESCRIPCION = ("Más de 200 variedades tropicales adaptadas al clima de Tampico. Palmas desde "
                  f"{dinero(P['palma_desde'])}. Entrega a domicilio en Tampico, Madero y Altamira.")

META = {
    "title": "Plantas, palmas y árboles en Tampico: qué sembrar según tu jardín · Viveros Terra",
    "description": ("Guía de plantas, palmas y árboles para el clima de Tampico: cuáles van en sol o sombra, cuáles "
                    "aguantan salitre y cuánto crecen. Más de 200 variedades con entrega y siembra."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (("og:type", "website"), ("og:url", URL),
           ("og:title", "Plantas, palmas y árboles en Tampico: qué sembrar según tu jardín · Viveros Terra"),
           ("og:description", OG_DESCRIPCION),
           ("og:image", f"{SITE}/img/paisajismo-alberca-plantas-tampico.webp"), ("og:locale", "es_MX")),
}
DESTACADAS = (
    ("palma-areca", "Interior y semisombra; la más pedida para oficinas y lobbies.", None),
    ("coco-plumoso", "Follaje plumoso para jardines amplios a pleno sol.", None),
    ("palma-real", "La de los proyectos grandes: crece alta y recta.", None),
    ("palma-washingtona", "Gana altura rápido y aguanta el viento del Golfo.", None),
    ("palma-viajera-ravenala", "Abanico de alto impacto para entradas y jardines de diseño.", None),
    ("flamboyan-tabachin", "Floración rojo-naranja y sombra abundante.", None),
    ("olivo-negro", "El de banqueta: raíz profunda, copa amplia y aguanta el salitre.", None),
    ("bugambilea-envarada", "Ya formada en vara; florece casi todo el año con poca agua.", None),
)
PREGUNTAS = (
    ("¿Cuánto cuestan las palmas en Tampico?",
     f"{datos.PALMAS_PRECIO}. Las demás palmas (washingtonia, del viajero, kerpis, cola de zorro, cycas, palma bambú y "
     "las exóticas) se cotizan según su altura: mándanos la que buscas y la altura por WhatsApp."),
    ("¿Cuánto cuestan los árboles en Tampico?",
     f"{FLAMBOYAN}. Los demás árboles (neem, ficus, laurel de la India, olivo negro, crespón y más) se cotizan según "
     "la especie y el tamaño del ejemplar."),
    ("¿Qué palmas crecen mejor en Tampico?",
     "Las mejor adaptadas al clima cálido y húmedo de Tampico son la washingtonia, la palma del viajero, la cycas "
     "revoluta y la palma areca para semisombra."),
    ("¿Qué palmas crecen mejor en el calor de Tampico?",
     "La washingtonia (crece rápido y tolera el viento del Golfo), la palma del viajero (resiste el calor intenso), la "
     f"cycas revoluta (muy longeva y de poco mantenimiento) y la areca en semisombra. En el catálogo hay "
     f"{PALMAS_EN_CATALOGO} especies de palmas del vivero."),
    pc.PREGUNTA_ENTREGA,
    ("¿Tienen catálogo para ver antes de llamar?",
     f"Sí: en <a href=\"/catalogo\">Arma tu lista</a> están {len(cd.ESPECIES)} especies con foto del vivero, luz, "
     "riego y altura. Añades las que te interesan con su tamaño y piezas y nos mandas la lista en un solo mensaje "
     "de WhatsApp; te respondemos con el precio por tamaño."),
    ("¿Tienen precio de mayoreo para proyectos grandes?",
     "Sí, para constructoras, arquitectos, hoteles, fraccionamientos y gobierno, con factura CFDI 4.0 y entrega por "
     "etapas. Las palmas para obra tienen su página: <a href=\"/palmas-mayoreo-proyectos\">palmas para proyectos</a>."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": TIPO,
    "meta": META,
    "migas": pc.migas(),
    "portada": {
        "kicker": f"Vivero en Cd. Madero · desde {datos.DESDE}",
        "h1": "Plantas, palmas y árboles de nuestro vivero en Tampico",
        "lede": (f"{datos.VARIEDADES} variedades para el clima del Golfo: te decimos cuáles van en sol o sombra, cuáles "
                 "aguantan salitre y cuánto crecen. Te las llevamos y, si quieres, las sembramos."),
        "etiqueta": {"codigo": "Vivero", "aviso": f"Precios {datos.ANIO}", "nombre": "Palmas", "antes": "desde",
                     "monto": dinero(P["palma_desde"]), "unidad": "tamaño chico",
                     # Flamboyán antes que palma real: "$500 … Flamboyán" lo marcaría test_consistencia ("flamboyán a $500").
                     "filas": (("Flamboyán", f"desde {dinero(P['flamboyan'])}"),
                               ("Palma real", f"desde {dinero(P['palma_real'])}")),
                     "nota": "El precio sube con la altura; las demás especies, según cotización."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="/catalogo" data-cta="plantas:catalogo">arma tu lista</a> y mándala en un solo mensaje.',
        "foto": {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/arboles-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico",
                 "lugar": "Siembra de un árbol", "etapa": "Tampico"},
        "compacta": True,
    },
    "necesidad": {"titulo": "¿Qué necesita tu jardín?",
                  "lede": "Elige por sol, salitre o tamaño y te llevamos al catálogo con el filtro puesto.",
                  "items": pc.NECESIDADES},
    "subcategorias": {"titulo": "Palmas, árboles y plantas para Tampico",
                      "lede": "Cada página dice qué especies van en sol, sombra o cerca del mar.",
                      "items": pc.SUBCATEGORIAS},
    "destacadas": {"titulo": "Las más pedidas en el vivero", "id": "vt-h-destacadas", "rotulo": "Más pedidas",
                   "lede": "Fotos de ejemplares de nuestro vivero.", "items": DESTACADAS},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Todo sobre plantas y palmas en Tampico", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Explora por tipo de planta", "items": (
        ("Las palmas más vendidas en Tampico", "/blog/palmas-mas-vendidas-tampico-precios"),
        ("Cómo plantar una palma o un árbol", "/blog/como-plantar-palma-arbol-paso-a-paso-tampico"),
        ("Plantas que resisten la sal del Golfo", "/blog/plantas-resistentes-sal-golfo-tampico"))},
    "relacionados": {"titulo": "Complementa tu proyecto", "items": (
        {"titulo": "Pasto en rollo", "href": "/pasto-en-rollo-tampico",
         "texto": f"San Agustín desde ${P['pasto_solo_m2']}/m².", "img": "/img/jardin-residencial-plantas-pasto-tampico.webp",
         "ancho": 960, "alto": 640},
        {"titulo": "Diseño de jardines", "href": "/diseno-jardines-tampico",
         "texto": f"Proyecto desde ${P['diseno']:,}.", "img": "/img/diseno-jardin-instalacion-plantas-tampico.webp",
         "ancho": 960, "alto": 640},
        {"titulo": "Tierra negra", "href": "/tierra-negra-vegetal-tampico",
         "texto": f"Costal ${P['tierra_negra_costal']} · m³ ${P['tierra_negra_m3']:,}.",
         "img": "/img/camion-tierra-negra-entrega-tampico.webp", "ancho": 960, "alto": 640},
        {"titulo": "Palmas para proyectos", "href": "/palmas-mayoreo-proyectos",
         "texto": "Hoteles, fraccionamientos, industria y gobierno: volumen, CFDI 4.0 y entrega por etapas.",
         "img": "/img/portadas/arboles-vivero-tampico-mayoreo-sm.webp", "ancho": 560, "alto": 840})},
    "cierre": {"titulo": "¿Ya sabes qué quieres sembrar?",
               "lede": "Mándanos qué buscas, el tamaño y la colonia; te respondemos con precio por tamaño.",
               "mensaje": MENSAJE},
    "jsonld": {
        "migas": pc.migas_ld(),
        "nodos": ({"@type": "ItemList", "name": "Plantas, palmas y árboles por subcategoría", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": s["titulo"], "url": f"{SITE}{s['href']}"}
            for i, s in enumerate(pc.SUBCATEGORIAS, 1)]},),
        "speakable": ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq details:first-child"),
    },
}
EOF
```

Termina el archivo con el mapa de paridad. **Cómo llenarlo:** corre `python3 tools/site/paridad.py informe /plantas-palmas-arboles-tampico` después del Step 7 y declara cada faltante: un reemplazo si su contenido sigue con otro texto (el reemplazo debe estar en la página) o un motivo de más de 20 caracteres. Los que ya se conocen:

```bash
cd ~/dev/viverosterra-e2e
cat >> tools/site/contenido/plantas_hub.py <<'EOF'

# Especies que el hub de main tenía como tarjeta (encabezado h3) y que el hub nuevo no repite: el hub muestra 8 con foto
# y cada una de estas sigue, con foto del vivero, en la página que se indica.
_MOVIDAS = {
    "Cycas Revoluta": "/catalogo (Palma Cica Revoluta)", "Palma Kerpis": "/palmas-tropicales-tampico",
    "Palma Bambú": "/catalogo (Palma Seifrixi Bambú)", "Palma Cola de Zorra": "/catalogo",
    "Ficus benjamina": "/catalogo (Ficus Benjamin)", "Neem": "/arboles-para-banqueta-tampico",
    "Laurel de la India": "/catalogo (Laurel de la India Formado)",
    "Ave del Paraíso": "/plantas-para-jardin-tampico (Ave de Paraíso)", "Duranta Cubana": "/plantas-para-jardin-tampico",
    "Croton": "/plantas-para-jardin-tampico (Croto Petra)",
}

PARIDAD = {
    "meta": {"og:description": (OG_DESCRIPCION, "Decía «Desde $200»: precio sin confirmar (el dueño solo fijó palmas desde "
                                                "$250, palma real $500 y flamboyán $250, 2026-11-07).")},
    "jsonld": {
        "LocalBusiness": ("Nodo recortado de main; las páginas apuntan a la entidad única #negocio de la home (como 2d); "
                          "el grafo completo es de la Etapa 4."),
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "¿Tienen catálogo con precios para ver antes de llamar?": "¿Tienen catálogo para ver antes de llamar?",
        "¿Cuál es la planta ideal para tu proyecto?": "¿Qué necesita tu jardín?",
        "Bajo mantenimiento": "¿Qué necesita tu jardín?",
        "Industria y banquetas": "Árboles para banqueta",
        "Hotel y comercio": "Palmas para proyectos",
        "Jardín residencial": "Plantas para jardín",
        "No sé cuál elegir": "¿Ya sabes qué quieres sembrar?",
        "El vivero de confianza para proyectos grandes en Tamaulipas": "Palmas para proyectos",
        "¿Cuál es tu planta?": "¿Ya sabes qué quieres sembrar?",
        # tarjetas de especie (h3) que siguen en el hub con el nombre del catálogo
        "Palma del Viajero": "Palma Viajera Ravenala",
        "Palma Coco Plumoso": "Coco Plumoso",
        "Bugambilia": "Bugambilea Envarada",
    },
    "retirados": {
        **{n: f"El hub muestra 8 especies con foto; esta sigue en {d}." for n, d in _MOVIDAS.items()},
        "+20 árboles más": "Tarjeta que solo enlazaba el catálogo; la cubre «Arma tu lista» (los 25 árboles con foto).",
        "Tabachín": ("Usaba la foto de la Tronadora y el catálogo llama tabachín al flamboyán; no se publica como "
                     "especie aparte hasta que el dueño diga cuál es (pregunta 2)."),
        "Trueno": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        "Tulipán Africano": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        "$500,": ("Era «$500,» dentro de la lista de palmas sin confirmar; $500 sigue como el precio de la palma real "
                  "(datos.PRECIOS_ESPECIE)."),
        "Lo que dicen quienes ya tienen su jardín": ("Las dos opiniones (Martha R., Constructora Arce) no están en "
                                                      "datos.OPINIONES ni tienen permiso confirmado (pregunta 8)."),
        "Jardines con plantas de Viveros Terra": ("Galería sin pies ni datos; las fotos de especies del vivero con pie "
                                                  "FIG. la sustituyen en «Las más pedidas en el vivero»."),
        "Variedades seleccionadas para el clima de Tampico": ("Sección de beneficios genéricos («asesoría sin costo», "
                                                              "«más de 18 años»); lo útil va al filtro por necesidad."),
        # precios: cada monto de main que no es de datos.py se retira con este motivo (completa la lista con el informe)
        "$1,000": "Palma bambú desde $1,000: precio sin confirmar; las palmas sin precio del dueño van según cotización.",
        "$1,500": ("Cola de zorro desde $1,500 (y m³ de tierra en la tarjeta vieja): el de palmas no está confirmado; la "
                   "tierra sigue en «Complementa tu proyecto» con datos.PRECIOS."),
        "$200": "Ficus benjamina desde $200: precio sin confirmar (pregunta 1 al dueño).",
        "$200,": "Ficus benjamina desde $200 (con coma en el texto): precio sin confirmar (pregunta 1 al dueño).",
        "$300": "Neem y trueno desde $300: precios sin confirmar (pregunta 1 al dueño).",
        "$300,": "Neem y trueno desde $300 (con coma en el texto): precios sin confirmar (pregunta 1 al dueño).",
        "$350": "Tabachín desde $350: precio sin confirmar y especie dudosa (preguntas 1 y 2 al dueño).",
        "$350,": "Tabachín desde $350 (con coma en el texto): precio sin confirmar (preguntas 1 y 2 al dueño).",
        "$600": "Tulipán africano desde $600: precio sin confirmar y especie fuera del catálogo (pregunta 3).",
        "$700": "Cycas revoluta desde $700: palma sin precio del dueño; va según cotización.",
        "$700,": "Cycas revoluta desde $700 (con coma en el texto): palma sin precio del dueño; va según cotización.",
    },
    "especies": {
        "reemplazos": {
            "Palma del Viajero": ("/plantas-palmas-arboles-tampico", "Palma Viajera Ravenala"),
            "Palma Coco Plumoso": ("/plantas-palmas-arboles-tampico", "Coco Plumoso"),
            "Flamboyán": ("/plantas-palmas-arboles-tampico", "Flamboyán Tabachín"),
            "Cycas Revoluta": ("/catalogo", "Palma Cica Revoluta"),
            "Palma Kerpis": ("/palmas-tropicales-tampico", "Palma Kerpis"),
            "Palma Bambú": ("/catalogo", "Palma Seifrixi Bambú"),
            "Palma Cola de Zorra": ("/catalogo", "Palma Cola de Zorra"),
            "Ficus benjamina": ("/catalogo", "Ficus Benjamin"),
            "Neem": ("/arboles-para-banqueta-tampico", "Neem"),
            "Laurel de la India": ("/catalogo", "Laurel de la India Formado"),
            "Ave del Paraíso": ("/plantas-para-jardin-tampico", "Ave de Paraíso"),
            "Duranta Cubana": ("/plantas-para-jardin-tampico", "Duranta Cubana"),
            "Bugambilia": ("/plantas-palmas-arboles-tampico", "Bugambilea Envarada"),
            "Croton": ("/plantas-para-jardin-tampico", "Croto Petra"),
        },
        "retirados": {
            "Tabachín": ("Usaba la foto de la Tronadora y el catálogo llama tabachín al flamboyán; no se publica como "
                         "especie aparte hasta que el dueño diga cuál es (pregunta 2)."),
            "Trueno": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
            "Tulipán Africano": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        },
    },
}
EOF
```

Nota sobre "Palma Kerpis → /palmas-tropicales-tampico": esa página la agrega la Tarea 10 (11 palmas con kerpis en "Las palmas del vivero"). Hasta entonces `test_plantas_paridad` la acepta porque el destino no está migrado.

- [ ] **Step 6: Registrar la página y sacarla de `tools/servicios`**

`tools/site/generar.py`, en `PAGINAS` después de la fila de palmas para proyectos:

```python
    ("/plantas-palmas-arboles-tampico", "plantas-palmas-arboles-tampico/index.html", "hub_categoria", "plantas_hub"),
```

`tools/site/tests/test_generar.py`, en `test_paginas_registradas_tienen_contexto`: en `esperadas`, después de `"/palmas-mayoreo-proyectos",` agrega `"/plantas-palmas-arboles-tampico",` (la lista sigue el orden de `generar.PAGINAS`; las Tareas 10 y 11 agregan ahí mismo las 5 subcategorías y `"/catalogo"`).
`tools/servicios/pages.py`: borra la entrada `"plantas-palmas-arboles-tampico": dict(…),` y actualiza el comentario de arriba de `PAGES` ("…y, desde la Etapa 2e, el hub de plantas…").
`tools/servicios/tests/test_pagos.py`: agrega `"plantas-palmas-arboles-tampico"` a `CON_PLANTILLA` y "2e" al docstring.
`tools/site/tests/test_plantas_reglas.py`: `PENDIENTES = frozenset(PLANTAS) - {"/plantas-palmas-arboles-tampico"}`.

- [ ] **Step 7: Construir, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /plantas-palmas-arboles-tampico
(cd tools/site && python3 -m unittest tests.test_plantas tests.test_plantas_paridad tests.test_plantas_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia 2>&1 | tail -3)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
```

Expected: `plantillas: 1 de 31 páginas escritas`; el informe con `ok` en las seis categorías (si queda un faltante, decláralo en `PARIDAD` con reemplazo o motivo y repite; nunca borres la entrada de la captura); `OK`; `OK`.

- [ ] **Step 8: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/plantillas/hub_categoria.py tools/site/contenido/plantas_comun.py tools/site/contenido/plantas_hub.py \
  tools/site/generar.py tools/site/tests/test_plantas.py tools/site/tests/test_plantas_paridad.py \
  tools/site/tests/test_generar.py tools/site/tests/test_plantas_reglas.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py \
  public/plantas-palmas-arboles-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantas): plantilla hub_categoria y hub de plantas con filtro por necesidad y precios del dueño" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Las cinco subcategorías

**Files:**
- Create: `tools/site/contenido/{palmas_tropicales,plantas_jardin,arboles_ornamentales,arboles_banqueta,plantas_interior}.py`
- Modify: `tools/site/generar.py`, `tools/servicios/pages.py`, `tools/servicios/tests/test_pagos.py`, `tools/site/tests/test_plantas.py`, `tools/site/tests/test_plantas_reglas.py`

Cada subcategoría usa `hub_categoria` con: portada (etiqueta con el "desde" de `datos.DESDE_PLANTAS` o "Según cotización"), `especies` (las de main con su foto del vivero), `precios` solo en palmas, `lista`, `garantia`, `faq` (las preguntas de main; respuestas sin precios que no sean de `datos.py`), `guias`, `relacionados` (las otras 4 subcategorías y el hub) y `cierre`. Sin `necesidad` ni `subcategorias`.

- [ ] **Step 1: Escribir las pruebas**

Agrega a `tools/site/tests/test_plantas.py`:

```python
SUBCATEGORIAS = ("/palmas-tropicales-tampico", "/plantas-para-jardin-tampico", "/arboles-ornamentales-tampico",
                 "/arboles-para-banqueta-tampico", "/plantas-de-interior-tampico")


class SubcategoriasTest(unittest.TestCase):
    def test_migas_al_hub(self):
        for ruta in SUBCATEGORIAS:
            with self.subTest(ruta=ruta):
                self.assertIn('<li><a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a></li>', html(ruta))

    def test_cada_especie_con_foto_del_vivero(self):
        for ruta in SUBCATEGORIAS:
            h = html(ruta)
            tarjetas = re.findall(r'<li class="vt-esp">(.*?)</li>', h, re.S)
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(len(tarjetas), 6)
                for t in tarjetas:
                    self.assertRegex(t, r'<img src="/img/catalogo/[a-z0-9-]+-tampico\.webp" width="\d+" height="\d+"')
                    self.assertIn("· En nuestro vivero</figcaption>", t)

    def test_etiqueta_con_desde_de_datos_o_segun_cotizacion(self):
        for ruta, desde in datos.DESDE_PLANTAS.items():
            etiqueta = re.search(r'<p class="vt-etiqueta__precio">(.*?)</p>', html(ruta), re.S).group(1)
            with self.subTest(ruta=ruta):
                self.assertIn(f"${desde}" if desde else "según cotización", etiqueta.lower())

    def test_palmas_con_la_tabla_del_dueno(self):
        h = html("/palmas-tropicales-tampico")
        self.assertIn(datos.PALMAS_PRECIO, h)
        for nombre, precio in (("Palma Areca", "$250"), ("Coco Plumoso", "$250"), ("Palma Real", "$500")):
            self.assertRegex(h, rf"<b>{nombre}</b>.*?{re.escape(precio)}")
        self.assertIn("Según cotización", h)

    def test_flamboyan_desde_250_en_ornamentales(self):
        self.assertIn("Flamboyán desde $250", html("/arboles-ornamentales-tampico"))

    def test_mensaje_propio_y_firma(self):
        for ruta in SUBCATEGORIAS:
            ms = mensajes(html(ruta))
            with self.subTest(ruta=ruta):
                self.assertIn(datos.con_firma(mensajes_paginas.PLANTAS[ruta]), ms)
                self.assertTrue(all(m.endswith(datos.FIRMA) for m in ms))
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_plantas 2>&1 | grep -E "^(FAIL|ERROR):" | head`
Expected: errores en `SubcategoriasTest` (las rutas aún no están en `generar.PAGINAS`).

- [ ] **Step 3: `tools/site/contenido/arboles_ornamentales.py` (el modelo de las cinco)**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/contenido/arboles_ornamentales.py <<'EOF'
"""Contenido de /arboles-ornamentales-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Las 6 especies de main con su foto del vivero (contenido/catalogo_especies.json); luz, riego y altura salen de ahí, igual
que en el catálogo. Precio: solo "Flamboyán desde $250" (datos.PRECIOS_ESPECIE); crespón $350, jacaranda $450 y olivo
negro $600 de main se retiran (sin confirmar; pregunta 1 al dueño). "Instalación con grúa" se retira de la respuesta de
entrega hasta que el dueño la confirme (pregunta 9). Título, descripción y Open Graph como estaban (Etapa 3).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import plantas_comun as pc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/arboles-ornamentales-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Árboles ornamentales"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
FLAMBOYAN = f"Flamboyán desde {dinero(P['flamboyan'])}"
TITULO = "Árboles Ornamentales en Tampico — Viveros Terra | 25 Especies"
DESCRIPCION = ("Árboles ornamentales para jardines en Tampico, Madero y Altamira. Flamboyán, Jacaranda, Ficus, Crespón, "
               "Guayacán y más. Entrega a domicilio · 833 326 8008.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("flamboyan-tabachin", "El más espectacular del trópico: flores rojo-naranja que cubren la copa y sombra abundante.",
     None),
    ("crespon-astronomica", "Racimos rosa, lila o blanco en verano; muy usado en jardines y avenidas de Tampico.", None),
    ("palo-de-rosa-guayacan", "Flores rosa brillante que cubren el árbol antes que las hojas.", None),
    ("jacaranda", "Floración morada única para jardines amplios.", None),
    ("lluvia-de-oro", "Racimos amarillos colgantes; florece en primavera y verano.", None),
    ("olivo-negro", "Sombra amplia y resistente al calor y al salitre; también va en banqueta.", None),
)
PREGUNTAS = (
    ("¿Qué árboles ornamentales son mejores para Tampico?",
     "Flamboyán (floración roja espectacular), crespón (florido y bueno para banqueta), jacaranda (morado), palo de "
     "rosa (rosa brillante), lluvia de oro (amarillo) y olivo negro (sombra resistente). Todos se adaptan al clima del "
     "sur de Tamaulipas."),
    ("¿Cuánto cuesta un árbol ornamental en Tampico?",
     f"{FLAMBOYAN}. Los demás árboles se cotizan según la especie y el tamaño del ejemplar: mándanos cuál te interesa y "
     "la altura por WhatsApp."),
    ("¿Qué árbol florido es mejor para un jardín en Tampico?",
     "Flamboyán (rojo-naranja, el más espectacular), crespón (rosa-lila, floración larga), palo de rosa (rosa intenso) "
     "y lluvia de oro (amarillo brillante)."),
    ("¿Qué árboles son buenos para banquetas en Tampico sin dañar el concreto?",
     "Olivo negro, polyalthia (columnar), neem, fresno y crespón podado: raíz profunda que no levanta la banqueta. "
     "Están en <a href=\"/arboles-para-banqueta-tampico\">árboles para banqueta</a>."),
    ("¿Hacen entrega de árboles grandes en Tampico?",
     "Sí, entregamos árboles de todos los tamaños en Tampico, Madero y Altamira. Los que sembramos nosotros tienen "
     "garantía de arraigo de 30 días con el riego que te indicamos."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Árboles ornamentales para jardines en Tampico",
        "lede": (f"{FLAMBOYAN}. Árboles de sombra y de flor elegidos para el clima de Tamaulipas: te los llevamos y los "
                 "sembramos con garantía de arraigo."),
        "etiqueta": {"codigo": "Árboles", "aviso": f"Precios {datos.ANIO}", "nombre": "Flamboyán",
                     "cientifico": "Delonix regia", "antes": "desde", "monto": dinero(P["flamboyan"]), "unidad": "",
                     "nota": "Los demás árboles, según especie y tamaño."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="/catalogo?cat=arboles" data-cta="plantas:catalogo">ve los 25 árboles del catálogo</a>.',
        "foto": {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/arboles-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Equipo de Viveros Terra sembrando un árbol ornamental en Tampico",
                 "lugar": "Siembra de un árbol ornamental", "etapa": "Tampico"},
        "compacta": True,
    },
    "especies": {"titulo": "Las más solicitadas en Tampico", "lede": "Ejemplares de nuestro vivero.", "items": ESPECIES},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Árboles ornamentales en Tampico: lo que más nos preguntan", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de árboles", "items": (
        ("Flamboyán en Tampico: cuidados y floración", "/blog/framboyan-delonix-regia-tampico"),
        ("7 árboles para banqueta que no levantan el pavimento", "/blog/arboles-para-sembrar-en-banqueta"),
        ("Poda de árboles y palmas", "/blog/poda-arboles-palmas-tampico-guia"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": tuple(
        {"titulo": s["titulo"], "href": s["href"], "texto": s["texto"], "img": s["img"], "ancho": s["ancho"],
         "alto": s["alto"]} for s in pc.SUBCATEGORIAS if s["href"] != RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos qué árbol buscas, la altura y la colonia; te respondemos con precio por tamaño.",
               "mensaje": MENSAJE},
    "jsonld": {"migas": pc.migas_ld(NOMBRE, RUTA), "nodos": (pc.lista_ld(NOMBRE, [s for s, _t, _a in ESPECIES]),),
               "speakable": ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq details:first-child")},
}

PARIDAD = {
    "jsonld": {
        "LocalBusiness": ("Nodo recortado de main; las páginas apuntan a la entidad única #negocio de la home (como 2d); "
                          "el grafo completo es de la Etapa 4."),
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "Árboles ornamentales tampico — Todo lo que necesitas saber": (
            "Árboles ornamentales en Tampico: lo que más nos preguntan"),
    },
    "retirados": {
        "$350": "Crespón desde $350: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
        "$350,": "Crespón desde $350 (con coma en el texto): precio sin confirmar por el dueño (pregunta 1).",
        "$450": "Jacaranda desde $450: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
        "$250,": "Era «$250,» dentro de una lista de precios sin confirmar; $250 sigue como «Flamboyán desde $250».",
        "$600": "Olivo negro desde $600: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
    },
    "especies": {"reemplazos": {}, "retirados": {}},
}
EOF
```

- [ ] **Step 4: Las otras cuatro con el mismo esqueleto**

Copia `arboles_ornamentales.py` a cada archivo y cambia solo lo de esta tabla (portadas y medidas: Tarea 9, `pc.SUBCATEGORIAS`; FAQ: las preguntas de la captura de cada página, con su respuesta de main sin precios que no sean de `datos.py`, sin "grúa", sin "existencia" y sin "asesoría sin costo"; agrega `pc.PREGUNTA_PAGO` al final):

| Archivo / ruta | `NOMBRE` | Etiqueta | `ESPECIES` (slugs, en este orden) | Altura propia | `guias` | Meta |
|---|---|---|---|---|---|---|
| `palmas_tropicales.py` · `/palmas-tropicales-tampico` | "Palmas tropicales" | nombre "Palmas", antes "desde", monto `dinero(P["palma_desde"])`, unidad "tamaño chico", filas (("Palma real", "desde $500"),), nota "El precio sube con la altura." | palma-areca, coco-plumoso, palma-real, palma-viajera-ravenala, palma-washingtona, palma-bismarkia, palma-licuala, palma-triangular, palma-cola-de-pescado, palma-cica-circinalis, palma-mascarena, palma-kerpis | — | palma-areca, palma-real, palmas-mas-vendidas | la de la captura (título "Palmas en Tampico: areca y coco plumoso desde $250 · Viveros Terra"; descripción y og iguales) |
| `plantas_jardin.py` · `/plantas-para-jardin-tampico` | "Plantas para jardín" | nombre "Plantas para jardín", antes "Precio", monto "Por tamaño", unidad "según cotización" | ave-de-paraiso, bugambilea-envarada, duranta-cubana, croto-petra, agave-atenuata, plumbago | — | plantas-resistentes-sal, buganvilia, duranta | la de la captura (el "+74 Variedades" del título se queda para la Etapa 3) |
| `arboles_banqueta.py` · `/arboles-para-banqueta-tampico` | "Árboles para banqueta" | nombre "Árboles para banqueta", antes "Precio", monto "Por tamaño", unidad "según cotización" | olivo-negro, polyalthia, neem, fresno, crespon-astronomica, tronadora | — | arboles-para-sembrar-en-banqueta, poda, como-plantar | la de la captura |
| `plantas_interior.py` · `/plantas-de-interior-tampico` | "Plantas de interior" | nombre "Plantas de interior", antes "Precio", monto "Por tamaño", unidad "según cotización" | ficus-lyrata-pandurata, monstera-pinanona, palma-zz-plant, sansiviera, palma-areca, dracena-compacta | ficus-lyrata-pandurata "Hasta 3 m en interior"; palma-areca "Hasta 2 m en maceta" (lo que publicaba main en esta página) | plantas-interior-tampico, ficus-elastica, palma-areca | la de la captura |

Palmas lleva además la sección `precios` (tabla de las 3 palmas con precio y las demás en el renglón agrupado), con la frase del dueño:

```python
CON_PRECIO = ("Palma Areca", "Coco Plumoso", "Palma Real")
"precios": {
    "titulo": "¿Cuánto cuesta una palma en Tampico?",
    "lede": f"{datos.PALMAS_PRECIO}.",
    "caption": "Precio del tamaño más chico en el vivero",
    "filas": tuple((cd.especie(s)["name"], cd.especie(s)["sc"],
                    f"desde {dinero(datos.PRECIOS_ESPECIE[cd.especie(s)['name']])}"
                    if cd.especie(s)["name"] in CON_PRECIO else datos.SEGUN_COTIZACION,
                    cd.especie(s)["name"] not in CON_PRECIO) for s, _t, _a in ESPECIES),
    "grupo": ("Washingtonia, del viajero, bismarckia, licuala, triangular, cola de pescado, cica circinalis, "
              "mascareña y kerpis", datos.SEGUN_COTIZACION),
    "nota": "El precio sube con la altura. Mándanos la altura que buscas y te damos el precio exacto.",
},
```

y su `jsonld["nodos"]` conserva `Product` + `Brand` + `AggregateOffer` (tipos de main), con los precios del dueño:

```python
{"@type": "Product", "name": "Palmas para jardín en Tampico", "brand": {"@type": "Brand", "name": datos.NOMBRE},
 "offers": {"@type": "AggregateOffer", "lowPrice": str(P["palma_desde"]), "priceCurrency": "MXN",
            "offerCount": str(len(CON_PRECIO))}},
```

Paridad de cada una: corre `python3 tools/site/paridad.py informe <ruta>` y `python3 -c "import sys; sys.path.insert(0,'tools/site'); import paridad_plantas as p; print(p.extraer('<ruta>'))"`; declara en `PARIDAD` los encabezados viejos ("Las más solicitadas en Tampico" sigue igual; "<Página> tampico — Todo lo que necesitas saber" → el título nuevo del FAQ; "Más servicios en Viveros Terra" y "¿Listo para cotizar?" siguen igual), los precios retirados con motivo (palmas: ninguno; jardín: "$3,000" y "$8,000" de "equipar un jardín desde $3,000–$8,000" → "estimado sin confirmar por el dueño; el diseño tiene su precio oficial en /diseno-jardines-tampico"; banqueta: "$350", "$400,", "$600," → "precios sin confirmar (pregunta 1)") y en `PARIDAD["especies"]`: palmas `"Palma del Viajero": ("/palmas-tropicales-tampico", "Palma Viajera Ravenala")`; interior `"ZZ Plant": ("/plantas-de-interior-tampico", "Palma ZZ Plant")`.

- [ ] **Step 5: Registrar y sacar de `tools/servicios`**

`generar.PAGINAS`, después del hub:

```python
    ("/palmas-tropicales-tampico", "palmas-tropicales-tampico/index.html", "hub_categoria", "palmas_tropicales"),
    ("/plantas-para-jardin-tampico", "plantas-para-jardin-tampico/index.html", "hub_categoria", "plantas_jardin"),
    ("/arboles-ornamentales-tampico", "arboles-ornamentales-tampico/index.html", "hub_categoria",
     "arboles_ornamentales"),
    ("/arboles-para-banqueta-tampico", "arboles-para-banqueta-tampico/index.html", "hub_categoria", "arboles_banqueta"),
    ("/plantas-de-interior-tampico", "plantas-de-interior-tampico/index.html", "hub_categoria", "plantas_interior"),
```

`test_generar.esperadas`: las 5 rutas, en el mismo orden, después de `"/plantas-palmas-arboles-tampico",`. `tools/servicios/pages.py`: borra las 5 entradas (queda `vivero-tampico` y los 4 materiales) y `GARANTIA_PLANTAS` si ya nadie la usa (`vivero-tampico` sí la usa: se queda). `test_pagos.CON_PLANTILLA`: agrega los 5 slugs. `test_plantas_reglas.PENDIENTES = frozenset({"/catalogo"})`.

- [ ] **Step 6: Construir, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /palmas-tropicales-tampico /plantas-para-jardin-tampico /arboles-ornamentales-tampico /arboles-para-banqueta-tampico /plantas-de-interior-tampico
(cd tools/site && python3 -m unittest tests.test_plantas tests.test_plantas_paridad tests.test_plantas_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia tests.test_enlaces 2>&1 | tail -3)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
```

Expected: `plantillas: 5 de 36 páginas escritas`; `ok` en todo el informe; `OK` (incluye `test_consistencia.test_flamboyan_desde_250` y `test_enlaces`: las guías del blog existen); `OK`.

- [ ] **Step 7: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/contenido/palmas_tropicales.py tools/site/contenido/plantas_jardin.py tools/site/contenido/arboles_ornamentales.py \
  tools/site/contenido/arboles_banqueta.py tools/site/contenido/plantas_interior.py tools/site/generar.py \
  tools/site/tests/test_plantas.py tools/site/tests/test_plantas_reglas.py tools/site/tests/test_generar.py \
  tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/palmas-tropicales-tampico/index.html public/plantas-para-jardin-tampico/index.html \
  public/arboles-ornamentales-tampico/index.html public/arboles-para-banqueta-tampico/index.html \
  public/plantas-de-interior-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantas): 5 subcategorías con hub_categoria, foto del vivero en cada especie y migas al hub" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Plantilla `catalogo` y `/catalogo`

**Files:**
- Create: `tools/site/plantillas/catalogo.py`, `tools/site/contenido/catalogo.py`
- Modify: `tools/site/generar.py`, `tools/site/tests/test_plantas.py`, `tools/site/tests/test_plantas_reglas.py`, `public/catalogo.html` (regenerado)

- [ ] **Step 1: Escribir las pruebas**

Agrega a `tools/site/tests/test_plantas.py`:

```python
class CatalogoTest(unittest.TestCase):
    def setUp(self):
        self.h = html("/catalogo")

    def test_orden_buscador_rejilla_pedido_garantia(self):
        orden = ['id="vt-h1"', "data-vt-filtros", "data-vt-rejilla", "data-vt-especial", "/politicas#garantia-plantas"]
        posiciones = [self.h.index(x) for x in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_rejilla_completa_sin_proxy_ni_js_en_linea(self):
        self.assertEqual(self.h.count('data-vt-agregar="'), 117)
        self.assertNotIn("/api/img", self.h)
        self.assertNotIn("function sendWA", self.h)
        self.assertNotIn("onclick=", self.h)
        self.assertIn('<script src="/js/vt-catalogo.js" defer></script>', self.h)
        self.assertIn('<script type="application/json" id="vt-catalogo-datos">', self.h)

    def test_datos_del_js_con_el_contrato(self):
        crudo = re.search(r'<script type="application/json" id="vt-catalogo-datos">(.*?)</script>', self.h, re.S).group(1)
        especies = json.loads(crudo)
        self.assertEqual(len(especies), 117)
        self.assertEqual(set(especies["palma-real"]), {"name", "sc", "sz"})

    def test_sin_las_cifras_ni_la_pestana_de_pasto_de_main(self):
        for viejo in ("Productor directo", "disponibilidad real", "Proyectos entregados", "+200,000 m²", "+ Vendido",
                      "setTab(", "Más vendidas"):
            self.assertNotIn(viejo, self.h)

    def test_json_ld_itemlist_con_117(self):
        lista = next(n for n in grafo(self.h) if n["@type"] == "ItemList")
        self.assertEqual(lista["numberOfItems"], 117)
```

- [ ] **Step 2: Verlas fallar**

Run: `cd tools/site && python3 -m unittest tests.test_plantas.CatalogoTest 2>&1 | tail -3`
Expected: errores (`/catalogo` aún no está en `generar.PAGINAS`).

- [ ] **Step 3: Plantilla `tools/site/plantillas/catalogo.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/plantillas/catalogo.py <<'EOF'
"""Plantilla del catálogo "Arma tu lista" (spec §3.3): ruta visible y H1 → precios publicados (palmas y flamboyán, de
datos.py) y CTA → buscador y filtros arriba (estado en la URL) → una sola rejilla en el HTML (foto del vivero, nombre,
científico, luz/riego/altura, "+ Añadir a mi lista" como <button>) → pedido de una especie que no está → otras páginas
(pasto y materiales) → garantía con condiciones. La lista se arma en <dialog> y sale en un solo WhatsApp
(public/js/vt-catalogo.js, el mismo mensaje que sendWA() de main). Los datos que necesita el JS (nombre, científico y
tamaños por especie) van en <script type="application/json" id="vt-catalogo-datos">."""
import json

import componentes as c
import componentes_plantas as cp
import datos
from contenido import catalogo_datos as cd
from plantillas import base

CONTEXTO = "https://schema.org"


def datos_js():
    lista = {e["slug"]: {"name": e["name"], "sc": e["sc"], "sz": e["sz"]} for e in cd.ORDENADAS}
    texto = json.dumps(lista, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="vt-catalogo-datos">{texto}</script>'


def render(k):
    tipo, ca = k["tipo"], k["cabeza"]
    cabeza = (f'<section class="vt-bloque vt-cat__cabeza" aria-labelledby="vt-h1"><div class="vt-wrap">'
              f'{c.migas(k["migas"])}<h1 id="vt-h1">{ca["h1"]}</h1><p class="vt-lede">{ca["lede"]}</p>'
              f'<p class="vt-cat__precios">{ca["precios"]}</p>{c.fila_cta(ca["mensaje"], tipo, "hero", hero=True)}'
              '</div></section>')
    rejilla = (f'<section class="vt-bloque vt-cat__rejilla" aria-labelledby="vt-h-rejilla"><div class="vt-wrap">'
               f'<h2 id="vt-h-rejilla" class="vt-sr">{k["rejilla"]["titulo"]}</h2>'
               f'{cp.filtros_catalogo(len(cd.ESPECIES))}{cp.rejilla_catalogo()}</div></section>')
    p = k["pedido"]
    pedido = c.bloque(1, "¿No está?", "vt-h-pedido", p["titulo"], cp.pedido_especial(tipo), lede=p["lede"], tinte=True)
    r = k["relacionados"]
    otras = c.bloque(2, "También", "vt-h-rel", r["titulo"], c.relacionados(r["items"]))
    garantia = (f'<section class="vt-bloque" aria-label="Garantía"><div class="vt-wrap"><p class="vt-promesa">'
                f'<b>Garantía:</b> {datos.GARANTIA_PLANTAS} <a href="/politicas#garantia-plantas">Condiciones</a></p>'
                '</div></section>')
    j = k["jsonld"]
    grafo = [{"@type": "ItemList", "name": j["nombre"], "description": j["descripcion"], "url": j["url"],
              "numberOfItems": len(cd.ESPECIES)}, j["migas"]]
    return base.documento(k["meta"], "\n".join((cabeza, rejilla, pedido, otras, garantia)),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},), head_extra=(datos_js(),),
                          tras_main=cp.lista_catalogo(tipo), scripts=("/js/vt-catalogo.js",),
                          clase_body="vt-pagina vt-plantas")
EOF
```

- [ ] **Step 4: Contenido `tools/site/contenido/catalogo.py`**

```bash
cd ~/dev/viverosterra-e2e
cat > tools/site/contenido/catalogo.py <<'EOF'
"""Contenido de /catalogo ("Arma tu lista"). Plantilla: plantillas/catalogo.py; especies: contenido/catalogo_datos.py.

Se retiran de main: la cabecera con "Productor directo", "Actualizado con disponibilidad real del vivero" y las cifras
sin respaldo ("+500 proyectos", "3 estados", "18 años"); la pestaña "Pasto & Tierra" (sus "+200,000 m²" contradicen
datos.M2_INSTALADOS; el pasto y los materiales tienen sus páginas, enlazadas abajo); las colecciones (una segunda
rejilla), el orden "Más vendidas" y la insignia "+ Vendido" (sin dato; pregunta 7); "Cotizar ahora" y "Medida especial"
por tarjeta (un solo mensaje: la medida especial vive en el diálogo de la lista). Título, descripción y Open Graph como
estaban: el título dice "con precio" y se reescribe en la Etapa 3 (spec §3.5).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import plantas_comun as pc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/catalogo"
URL = f"{SITE}{RUTA}"
TITULO = "Catálogo de plantas con precio en Tampico: arma tu lista y cotiza · Viveros Terra"
IMAGEN = f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"
META = {
    "title": TITULO,
    "description": ("Más de 200 variedades de plantas, palmas, árboles y pasto en Tampico. Cotizador, filtros por categoría "
                    "y entrega a domicilio. Viveros Terra."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (("og:type", "website"), ("og:url", URL), ("og:title", TITULO),
           ("og:description", ("Más de 200 variedades disponibles con cotizador integrado. Plantas, palmas, árboles, pasto "
                               "y materiales para jardines en Tampico, Madero y Altamira.")),
           ("og:image", IMAGEN), ("og:image:width", "1200"), ("og:image:height", "630"),
           ("og:site_name", "Viveros Terra"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO), ("twitter:image", IMAGEN)),
}
MENSAJE = mensajes_paginas.RUTAS[RUTA][0]

CONTENIDO = {
    "tipo": "catalogo",
    "meta": META,
    "migas": (("Inicio", "/"), ("Plantas y palmas", pc.HUB), ("Arma tu lista", None)),
    "cabeza": {
        "h1": "Catálogo de Plantas, Palmas y Árboles en Tampico.",
        "lede": ("Especies de nuestro vivero con foto, luz, riego y altura. Busca o filtra, añade a tu lista con tamaño y "
                 "piezas, y mándala completa en un solo mensaje de WhatsApp."),
        "precios": (f"{datos.PALMAS_PRECIO}. Flamboyán desde {dinero(P['flamboyan'])}. Las demás especies, según "
                    "cotización por tamaño."),
        "mensaje": MENSAJE,
    },
    "rejilla": {"titulo": "Especies del vivero"},
    "pedido": {"titulo": "¿No encontraste lo que buscas?",
               "lede": "Dinos qué planta, árbol, tamaño o medida necesitas y te cotizamos."},
    "relacionados": {"titulo": "¿Buscas pasto o material?", "items": (
        {"titulo": "Pasto en rollo", "href": "/pasto-en-rollo-tampico",
         "texto": f"San Agustín desde ${P['pasto_solo_m2']}/m².",
         "img": "/img/jardin-residencial-plantas-pasto-tampico.webp", "ancho": 960, "alto": 640},
        {"titulo": "Pasto sintético", "href": "/pasto-sintetico",
         "texto": f"Envío a todo México desde ${P['sintetico_tienda_m2']}/m².",
         "img": "/img/areas-verdes-paisajismo-tampico.webp", "ancho": 960, "alto": 640},
        {"titulo": "Tierra negra", "href": "/tierra-negra-vegetal-tampico",
         "texto": f"Costal ${P['tierra_negra_costal']} · m³ ${P['tierra_negra_m3']:,}.",
         "img": "/img/camion-tierra-negra-entrega-tampico.webp", "ancho": 960, "alto": 640})},
    "jsonld": {"nombre": "Catálogo Viveros Terra Tampico",
               "descripcion": "Especies de plantas, palmas y árboles del vivero de Viveros Terra en Tampico, Tamaulipas",
               "url": URL, "migas": pc.migas_ld("Arma tu lista", RUTA)},
}

PARIDAD = {
    "reemplazos": {
        "Pasto en Rollo Natural": "Pasto en rollo",
        "Materiales & Tierra": "Tierra negra",
        "¿Necesitas pasto o material especial?": "¿Buscas pasto o material?",
    },
    "retirados": {
        "${p.name}": "Era la plantilla del JS de main dentro de un <h3>; ahora cada especie es un <h3> real en el HTML.",
    },
    # El Floripondio duplicado no necesita entrada: la especie sigue (una vez) y la paridad la encuentra.
    "especies": {"reemplazos": {}, "retirados": {}},
}
EOF
```

Las fotos de `relacionados` (`jardin-residencial-plantas-pasto-tampico.webp`, `areas-verdes-paisajismo-tampico.webp`, `camion-tierra-negra-entrega-tampico.webp`, `diseno-jardin-instalacion-plantas-tampico.webp`) existen en `public/img/`: confirma su ancho y alto real con `sips -g pixelWidth -g pixelHeight <archivo>` y corrige los 960×640 del plan si difieren (también en `plantas_hub.py`).

- [ ] **Step 5: Registrar, construir y probar**

`generar.PAGINAS`, después de las subcategorías:

```python
    ("/catalogo", "catalogo.html", "catalogo", "catalogo"),
```

`test_generar.esperadas`: `"/catalogo",` después de `"/plantas-de-interior-tampico",`. `test_plantas_reglas.PENDIENTES = frozenset()` y agrega al final de la clase:

```python
    def test_ninguna_pagina_publica_usa_api_img(self):
        """Etapa 2e: el proxy /api/img ya no lo usa ninguna página (se borra en la Etapa 5)."""
        self.assertEqual([str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob("*.html")
                          if "/api/img" in p.read_text(encoding="utf-8")], [])
```

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/build.py | tail -2
wc -c public/catalogo.html
python3 tools/site/paridad.py informe /catalogo
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 1 de 37 páginas escritas`; el catálogo de ~190 KB sin comprimir y ~29 KB con gzip (medido en el prototipo: 189,657 B / 28,897 B; antes 187,672 B con 570 renglones de JS en línea y sin rejilla en el HTML); `ok` en todo el informe; `OK` en las cuatro suites de Python (`Ran` = 433 + las pruebas nuevas de este plan; anota el número); `ℹ pass 56`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/plantillas/catalogo.py tools/site/contenido/catalogo.py tools/site/generar.py tools/site/tests/test_plantas.py \
  tools/site/tests/test_plantas_reglas.py tools/site/tests/test_generar.py public/catalogo.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(catalogo): plantilla catalogo con buscador y filtros arriba, una sola rejilla con botones reales y fotos locales" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Pruebas en navegador de las páginas de plantas

**Files:**
- Test: `tools/site/tests/test_plantillas_navegador.py`

Las 6 páginas con portada entran a las pruebas de plantilla que ya existen (axe de página completa a 375 y 1440, precio y CTA en el primer pantallazo a 375×812, sin desbordar, CLS < 0.1); el catálogo entra a axe, desborde y CLS, y lleva su propia prueba de primer pantallazo. Pruebas nuevas: desborde también a 1920; catálogo con teclado (filtros, añadir con Enter, foco de vuelta, un solo mensaje con toda la lista y `generate_lead`); filtros en la URL y conteo igual al del hub; LCP sin `/api/img`.

- [ ] **Step 1: Agregar las pruebas**

En `tools/site/tests/test_plantillas_navegador.py`, debajo de `EMPRESAS`:

```python
# Etapa 2e: hub y subcategorías con hub_categoria (portada con etiqueta) y el catálogo (sin portada).
PLANTAS = ("/plantas-palmas-arboles-tampico/", "/palmas-tropicales-tampico/", "/plantas-para-jardin-tampico/",
           "/arboles-ornamentales-tampico/", "/arboles-para-banqueta-tampico/", "/plantas-de-interior-tampico/")
# El servidor local no tiene cleanUrls de Vercel: el catálogo se pide como /catalogo.html (como en test_navegador.py).
CATALOGO = "/catalogo.html"
CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS
```

En `test_axe_de_pagina_completa_sin_violaciones_serias`, `test_sin_desbordar_en_cuatro_anchos` y `test_cls_bajo_0_1_en_movil`, recorre `CON_PLANTILLA + (CATALOGO,)`; en `test_sin_desbordar_en_cuatro_anchos` agrega `1920` a los anchos (y renómbrala `test_sin_desbordar_de_320_a_1920`). Agrega a la clase:

```python
    def test_catalogo_precio_cta_y_buscador_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        page.goto(self.base + CATALOGO, wait_until="load")
        for selector in (".vt-cat__precios", ".vt-cat__cabeza [data-hero-cta] .vt-btn--wa"):
            caja = page.locator(selector).bounding_box()
            with self.subTest(selector=selector):
                self.assertLessEqual(caja["y"] + caja["height"], 812)
        self.assertLessEqual(page.locator("#vt-cat-q").bounding_box()["y"], 812 * 1.5)

    def test_catalogo_con_teclado_arma_un_solo_mensaje(self):
        page = self.pagina(1440, 900)
        page.goto(self.base + CATALOGO, wait_until="load")
        page.locator("#vt-cat-q").focus()
        page.keyboard.type("palma real")
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), "1 especie")
        self.assertIn("q=palma%20real", page.url)
        boton = page.locator('[data-vt-agregar="palma-real"]')
        boton.focus()
        page.keyboard.press("Enter")
        self.assertTrue(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.evaluate("() => document.activeElement.id"), "vt-agregar-tam")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")  # menos, cantidad, más
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")  # Cancelar, Agregar
        page.keyboard.press("Enter")
        self.assertFalse(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.evaluate("() => document.activeElement.dataset.vtAgregar"), "palma-real")
        page.locator("#vt-cat-q").fill("olivo")
        page.locator('[data-vt-agregar="olivo-negro"]').click()
        page.locator("#vt-agregar-n").fill("10")
        page.locator('#vt-agregar button[value="agregar"]').click()
        self.assertIn("2", page.locator('[data-vt-o="cuenta-lista"]').inner_text())
        page.locator("[data-vt-abrir-lista]").click()
        enviar = page.locator('#vt-lista [data-vt-o="enviar"]')
        mensaje = unquote(enviar.get_attribute("href").split("text=", 1)[1])
        self.assertIn("• Palma Real (", mensaje)
        self.assertIn("• Olivo Negro (", mensaje)
        self.assertIn("Total: 2 variedades, 11 unidades", mensaje)
        self.assertEqual(page.locator('#vt-lista a[href^="https://wa.me/"]').count(), 1)
        page.evaluate("(a) => a.addEventListener('click', (e) => e.preventDefault())", enviar.element_handle())
        enviar.click()
        eventos = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "catalogo:sendWA", "service": "plantas"}],
                      eventos)
        self.assertTrue(unquote(enviar.get_attribute("href")).endswith(datos.FIRMA))

    def test_filtro_del_hub_llega_al_catalogo_con_el_mismo_conteo(self):
        page = self.pagina(1440, 900)
        page.goto(self.base + "/plantas-palmas-arboles-tampico/", wait_until="load")
        enlace = page.locator('a[data-cta="plantas:necesidad-salitre"]')
        conteo = enlace.locator(".vt-necesidad__n").inner_text()
        href = enlace.get_attribute("href")
        self.assertEqual(href, "/catalogo?uso=salitre")
        page.goto(self.base + href.replace("/catalogo", CATALOGO, 1), wait_until="load")
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), conteo)
        self.assertEqual(page.locator('[data-vt-g="uso"][data-vt-v="salitre"]').get_attribute("aria-pressed"), "true")
        page.locator("[data-vt-limpiar]").click()
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), "117 especies")
        self.assertTrue(page.url.endswith(CATALOGO))

    def test_lcp_de_plantas_sin_api_img(self):
        lcp = """() => new Promise((listo) => { let ultimo = null;
          new PerformanceObserver((l) => { const e = l.getEntries(); ultimo = e[e.length - 1]; })
            .observe({ type: 'largest-contentful-paint', buffered: true });
          setTimeout(() => listo(ultimo ? (ultimo.url || ultimo.element.tagName) : ''), 1500); })"""
        page = self.pagina(375, 812)
        for ruta in PLANTAS + (CATALOGO,):
            pedidas = []
            page.on("request", lambda r: pedidas.append(r.url))
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertNotIn("/api/img", page.evaluate(lcp))
                self.assertEqual([u for u in pedidas if "/api/img" in u], [])
```

Nota para quien ejecuta: desde el `select` del diálogo, el orden de foco es −, cantidad, +, Cancelar, Agregar (el campo de medida especial está oculto); si el orden real difiere, ajusta solo los `Tab`, nunca el resto de la prueba.

- [ ] **Step 2: Correrlas**

Run: `cd tools/site && python3 -m unittest tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `OK`. Si axe marca algo serio (contraste del pie de foto sobre `--vt-bone`, nombre accesible de los botones de filtro, `dialog` sin nombre), corrígelo en `terra-plantas.css` o en `componentes_plantas.py` con su prueba, reconstruye y repite.

- [ ] **Step 3: Consola limpia en las 108 páginas y nunca dos barras**

Run: `cd tools/site && python3 -m unittest tests.test_navegador tests.test_tienda_navegador 2>&1 | tail -3`
Expected: `OK` (incluye `test_consola_limpia_en_todas_las_paginas` y `test_nunca_dos_barras_fijas_abajo_a_375`: el catálogo no lleva barra del shell, solo "Mi lista" cuando hay especies).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2e
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): axe, desborde 320–1920, primer pantallazo, catálogo con teclado, filtros del hub y LCP sin /api/img" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: Verificación final y puertas de revisión (merge y push los hace el controlador)

**Files:** ninguno nuevo (correcciones de los revisores, cada una con su prueba y su commit).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 37 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `OK` (anota el `Ran`); `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 56` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas y consistencia a la vista**

```bash
cd ~/dev/viverosterra-e2e
python3 tools/site/paridad.py informe /plantas-palmas-arboles-tampico /palmas-tropicales-tampico /plantas-para-jardin-tampico /arboles-ornamentales-tampico /arboles-para-banqueta-tampico /plantas-de-interior-tampico /catalogo
(cd tools/site && python3 -m unittest tests.test_reglas tests.test_consistencia tests.test_paridad tests.test_plantas_paridad tests.test_plantas_reglas tests.test_plantas tests.test_contenido 2>&1 | tail -1)
grep -oiE "oasis|productor directo|senasica|disponibilidad real|en existencia|\+ ?vendid|gratis|sin costo|framboy[aá]n |\\\$850|\\\$4,200|/api/img|Martha R|Constructora Arce" \
  public/{plantas-palmas-arboles-tampico,palmas-tropicales-tampico,plantas-para-jardin-tampico,arboles-ornamentales-tampico,arboles-para-banqueta-tampico,plantas-de-interior-tampico}/index.html public/catalogo.html | sort | uniq -c
grep -rl "/api/img" public --include=*.html | wc -l
```

Expected: `ok` en las seis categorías de las 7 páginas; `OK`; el `grep` de palabras vacío; `0`.

- [ ] **Step 3: Lighthouse móvil**

```bash
cd ~/dev/viverosterra-e2e
(cd public && python3 -m http.server 8768 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in plantas-palmas-arboles-tampico palmas-tropicales-tampico arboles-ornamentales-tampico catalogo; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8768/$r" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2e-lh-$r.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'], a['largest-contentful-paint-element']['details']['items'][0]['items'][0]['node'].get('snippet','')[:90] if a['largest-contentful-paint-element'].get('details') else '')" "/tmp/vt-e2e-lh-$r.json"
done
pkill -f "http.server 8768"
```

(`python3 -m http.server` sirve `catalogo.html` en `/catalogo.html`; si `/catalogo` responde 404 en local, usa `catalogo.html` en la URL.)

Expected por página: Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s y el elemento LCP sin `/api/img`. CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. Si Performance queda abajo por GA4 o por el peso de la rejilla (117 imágenes; solo 4 cargan de entrada), anota valor y causa para el PR.

- [ ] **Step 4: Capturas a 320, 375, 768, 1024, 1440 y 1920 con el viewport real de Playwright**

```bash
cd ~/dev/viverosterra-e2e/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
rutas = ('plantas-palmas-arboles-tampico/', 'palmas-tropicales-tampico/', 'plantas-para-jardin-tampico/',
         'arboles-ornamentales-tampico/', 'arboles-para-banqueta-tampico/', 'plantas-de-interior-tampico/', 'catalogo.html')
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in rutas:
        for w in (320, 375, 768, 1024, 1440, 1920):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.evaluate("async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); } scrollTo(0, 0); }")
            p.screenshot(path=f"/tmp/vt-e2e-{r.strip('/').replace('.html', '')}-{w}.png", full_page=True)
            p.close()
    b.close()
srv.shutdown()
print(len(rutas) * 6, 'capturas')
PY
```

Expected: `42 capturas`. Revisa a mano: etiqueta amarilla con precio y CTA en el primer pantallazo a 375 en hub y subcategorías; en el catálogo, precios, CTA y buscador arriba; tarjetas en 2 columnas a 320/375, 3 a 768 y 4 desde 1100 en el catálogo; fotos del vivero sin deformar (4:5) con su pie "Fig. NN · … · En nuestro vivero"; filtros plegados en celular y abiertos desde 768; "Mi lista" sin tapar la última fila; diálogos centrados a 320; nada que desborde.

- [ ] **Step 5: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega la rama en verde y un resumen (`git log --oneline main..feat/etapa-2e`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2e --stat`, `plantillas/{hub_categoria,catalogo}.py`, `componentes_plantas.py`, `contenido/{plantas_comun,plantas_hub,palmas_tropicales,plantas_jardin,arboles_ornamentales,arboles_banqueta,plantas_interior,catalogo,catalogo_datos}.py`, `vt-catalogo.js`, `terra-plantas.css`, `fotos_catalogo.py`, la vista previa de Vercel, `/tmp/vt-e2e-*.png`, los JSON de Lighthouse, `paridad.py informe` y el spec (§3.3, §3.5, §4, §5, §8.4, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta, pies FIG., cuadro de datos), jerarquía del hub (necesidades, subcategorías, más pedidas), la rejilla del catálogo a 320 (2 columnas legibles, datos apilados), estados de los filtros (`aria-pressed` sin depender solo del color), diálogos (foco, Esc, retorno del foco, objetivos de 44 px), barra "Mi lista" y movimiento reducido.
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta salvo la descripción de Open Graph del hub (declarada), un H1 por página, migas visibles = `BreadcrumbList`, `FAQPage` = lo visible, `ItemList` de especies y subcategorías válidos en Rich Results Test, `Product`/`AggregateOffer` de palmas sin precios inventados, nombres científicos corregidos, enlaces internos nuevos (guías del blog por especie, filtros del hub), imágenes con `width`/`height`/`alt`, rejilla indexable en el HTML, LCP sin `/api/img`, y que nada adelante la Etapa 3 (títulos, consolidación de interior y banqueta).
3. **CRO** (`general-purpose` con `page-cro`): del hub al catálogo por necesidad, de la subcategoría a la lista, "Arma tu lista" con un solo mensaje que incluye tamaño y piezas, el pedido de una especie que no está, CTA y precio en el primer pantallazo, y que quitar "Cotizar ahora" por tarjeta no deje a nadie sin camino.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `typescript-reviewer` para el JS + `e2e-runner`; `security-reviewer` sobre `fotos_catalogo.py`): reglas del dueño (precios solo de `datos.py`, palmas, flamboyán, garantía condicionada, sin afirmaciones sin verificar, anticipo, visita), sin `innerHTML` con datos, `fotos_catalogo.py` sin rutas ni hosts tomados de los datos (solo ids validados contra `lh3.googleusercontent.com`), paridad, consola limpia y sin `.DS_Store`.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 1 otra vez) y el controlador vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan para el PR.

- [ ] **Step 6: Aprobación del dueño (controlador)**

Comparte la vista previa de Vercel y las capturas, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Si responde con datos (precios "desde" por especie o subcategoría, la lista de salitre, tabachín, kerpis), van a `datos.py` o a `catalogo_datos.py` con su prueba en una tarea nueva antes del merge.

- [ ] **Step 7: Merge, push y despliegue (solo el controlador; lote 4 con 2f)**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2e -m "feat: Etapa 2e, plantas con hub_categoria y catálogo Arma tu lista con fotos locales" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 37 …`, `shell: 0 de 108 …`, `0`; Vercel despliega `main`.

- [ ] **Step 8: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in plantas-palmas-arboles-tampico palmas-tropicales-tampico plantas-para-jardin-tampico arboles-ornamentales-tampico arboles-para-banqueta-tampico plantas-de-interior-tampico catalogo; do
  printf "%s " $r; curl -s $W/$r | grep -cE "/api/img|tailwind.css|design-system.css|servicios.css|fonts.googleapis"
done
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" $W/img/catalogo/palma-real-tampico.webp
curl -sI $W/css/$(curl -s $W/catalogo | grep -oE "terra-plantas\.[0-9a-f]{10}\.css" | head -1) | grep -i cache-control
curl -s $W/js/vt-catalogo.js | head -1
```

Expected: `0` en las 7; `200 image/webp`; `public, max-age=31536000, immutable`; `/* Viveros Terra · vt-catalogo.js …`. En Chrome (escritorio y iPhone): consola limpia; del hub, "Cerca del mar (salitre)" abre el catálogo filtrado con el mismo conteo; en el catálogo, buscar "palma", añadir dos especies con tamaño y piezas y "Cotizar por WhatsApp" abre un solo mensaje con las dos y la firma. En GA4 DebugView: `select_content` (`plantas:necesidad-salitre`) y `generate_lead` (`catalogo:sendWA`, `service` `plantas`).

- [ ] **Step 9: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 10: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2e && git branch -d feat/etapa-2e
```

---

## Lotes de ejecución sugeridos

| Lote | Tareas | Qué deja | Revisión intermedia |
|---|---|---|---|
| A · Fundaciones (sin cambiar cómo se ven las páginas) | 0–6 | Capturas y casos, datos del dueño, reglas en rojo, especies como datos, 117 fotos locales, hoja `terra-plantas.css` cableada | Cumplimiento: datos, reglas y `fotos_catalogo.py` (security-reviewer) |
| B · Piezas | 7–8 | `componentes_plantas.py` y `vt-catalogo.js` con sus pruebas | Código (python-reviewer, typescript-reviewer) |
| C · Páginas | 9–11 | Hub, 5 subcategorías y catálogo migrados | Paridad e informe por página |
| D · Cierre | 12–13 | Navegador, Lighthouse, capturas, 4 puertas, aprobación del dueño, merge con 2f | Las 4 puertas del spec §11 |

## Correcciones a la hoja de ruta

- "Se conserva su JS": el armador de lista conserva su **contrato** (lista `[{name, sc, sz, qty}]`, regla de `confirmAdd()`, mensaje idéntico al de `sendWA()` y el mismo `cta_id` `catalogo:sendWA` en GA4), probado con casos congelados de main; el código sale del HTML a `vt-catalogo.js` porque la rejilla pasa al HTML, las tarjetas pasan a `<button>` real y los diálogos a `<dialog>`. `window.open` se cambia por un enlace con `href` recalculado (patrón de 2d), que `terra.js` mide y firma.
- La lista de especies del catálogo pasa de 118 a 117: el Floripondio venía dos veces (el segundo con un id de Drive truncado).
- Se agrega una hoja `terra-plantas.css`: `terra.css` publicado ya mide 47,514 B de 49,152 B y el catálogo no cabe (2d dejó ~1.3 KB gzip "para 2e–2i").
- "Las ~118 fotos y las 17 de plantas" son el mismo conjunto: las 17 del hub son fotos del catálogo (mismos ids de Drive). Se bajan 117 (una por especie).
- El filtro por necesidad del hub son enlaces al catálogo con el filtro en la URL (no un filtro con JS en el hub).
- Salitre no existía en los datos: se marca solo con fuente publicada (13 especies) y queda como pregunta al dueño.
- `test_consistencia` ya exige "flamboyán" (decisión del dueño); el spec §"Framboyán" dice "framboyán" y está desactualizado: manda la prueba.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Drive deja de servir una foto o devuelve una página de error | `fotos_catalogo.py` valida tipo `image/*`, que Pillow la abra y su ancho; si falla, se detiene diciendo la especie. Las fotos quedan en el repo: después de la Tarea 5 el sitio no depende de Drive. |
| 117 tarjetas pesan en celular | Rejilla en el HTML (~110–140 KB sin comprimir) con solo 4 imágenes de entrada; el resto `lazy` con `width`/`height` (sin CLS). Lighthouse en la Tarea 13. |
| Quitar precios sin confirmar del hub y de las subcategorías baja información | Eran precios que el dueño no dio; cada uno se retira con motivo en `PARIDAD` y vuelve si el dueño lo confirma (pregunta 1). La página dice "según cotización" y "Arma tu lista" recoge tamaño y piezas. |
| Los conteos del hub y del catálogo se desfasan | Una sola lógica de filtros (`catalogo_datos.coincide` = `coincide()` del JS) y prueba en navegador que compara el conteo del enlace con el del catálogo. |
| Foco y teclado en `<dialog>` | `showModal()` atrapa el foco y Esc cierra; el foco vuelve al botón que abrió; prueba de teclado de punta a punta. |
| La corrección de nombres científicos se lee como cambio de contenido | Solo las 11 formas mal escritas, declaradas en `CIENTIFICOS_CORREGIDOS` y aceptadas por la paridad solo así; la puerta SEO las revisa. |
| La foto de la Sansiviera Variegada es la misma que la de la Sansiviera | Se publica igual que en main (mismo id de Drive) y se pregunta (pregunta 5); se cambia tocando solo el archivo. |
| `select_content` y `generate_lead` cambian de origen | terra.js ya mide todo enlace a `/catalogo` y todo `wa.me` con `data-cta`; prueba en navegador del `generate_lead` con `catalogo:sendWA`. |

## Preguntas al dueño

1. **Precios "desde" que no están en `datos.py`** (hoy se retiran y van "según cotización"): ¿hay un "desde" para **plantas para jardín**, **árboles para banqueta** y **plantas de interior** como subcategoría? ¿Son reales algunos de los precios que publicaba el sitio para árboles: ficus benjamina $200, neem $300 (o $350 en otra página), trueno $300, tabachín $350, laurel de la India $500, tulipán africano $600, crespón $350, jacaranda $450, olivo negro $600, polyalthia $400? ¿Y el "equipar un jardín desde $3,000–$8,000 en plantas"? (Las palmas sin precio del dueño —washingtonia, viajero, kerpis, cycas, bambú, cola de zorro y exóticas— siguen "según cotización" por su decisión del 2026-11-07.)
2. **Tabachín:** el hub vendía "Tabachín" aparte del flamboyán (con la foto de la Tronadora) y el catálogo llama "Flamboyán Tabachín" al *Delonix regia*. ¿El tabachín que venden es otra especie (p. ej. *Caesalpinia pulcherrima*)? ¿Tienen foto?
3. **Trueno y tulipán africano** aparecían en el hub pero no están en el catálogo: ¿se venden? Si sí, nombre científico y foto del vivero.
4. **Palma kerpis:** el catálogo dice *Chamaedorea sp.*, la lista de palmas para proyectos *Hyophorbe lagenicaulis* (que en el catálogo es la "Palma Mascareña") y el artículo del blog *Howea forsteriana*. ¿Cuál es la que venden como kerpis?
5. **Sansiviera Variegada:** usa la misma foto que la Sansiviera común. ¿Hay foto de la variegada?
6. **Salitre:** marcamos 13 especies que aguantan salitre (palma cocotera, datilera, uva de playa, sansivieras, adelfa enana, bugambileas, crotos, olivo negro, casuarina y arbusto de playa), tomadas del artículo de plantas resistentes a la sal y de las fichas del catálogo. ¿Está bien la lista? ¿Agregan o quitan alguna?
7. **"+ Vendido" / "Más vendidas":** el catálogo marcaba especies como más vendidas. ¿Sale de datos reales de venta? Mientras no, no se muestra.
8. **Opiniones del hub** ("Martha R.", palmas del viajero en Madero; "Constructora Arce", fraccionamiento en Altamira): ¿son reales y hay permiso para publicarlas? Mientras no, se retiran.
9. **Entrega de árboles grandes con grúa** y entregas a Pánuco/Huasteca "según volumen": ¿se confirman? Mientras no, no se menciona la grúa.
10. **Tamaños a la venta** (`sz` de cada especie, p. ej. palma areca "1 m / 1.5 m…"): ¿siguen vigentes los del catálogo? Son los que aparecen en el diálogo de "Arma tu lista".
11. **¿Se puede decir que la asesoría por WhatsApp para elegir plantas no tiene costo?** El hub decía "asesoría gratis"; se retiró por la regla de no prometer cosas gratis (la visita nunca lo es).
12. **21 fotos de especie miden menos de 480 px en Drive** (algunas muy chicas: eucalipto 146 px, ficus lyrata 195, flor de mayo 238, liquidámbar 236, palma cocotera 266×190): se publican a su tamaño, sin agrandar (igual que hoy con `/api/img`). ¿Hay mejores fotos de estas especies, o entran primero en la sesión de fotos del vivero? Lista exacta en `catalogo_datos.FOTOS_CHICAS`.
