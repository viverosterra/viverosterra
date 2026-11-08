# Etapa 2f · Materiales: tierra negra, tezontle, mármol y piedra bola con la plantilla `material` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sexto sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2f; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §5, §7.3, §8, §10, §11). Las cuatro páginas de materiales —`/tierra-negra-vegetal-tampico`, `/tezontle-rojo-tampico`, `/marmol-blanco-tampico` y `/piedra-bola-rio-tampico` (archivos `public/<ruta>/index.html`)— dejan de ser HTML a mano con Tailwind, `design-system.css`, `servicios.css`, Google Fonts y `<script>` en línea con `window.open`, y salen de una plantilla nueva, **`material`**, con su contenido en `tools/site/contenido/`. Secuencia (spec §3.3): H1 con el precio por presentación en la etiqueta (costal / m³ / camión, o "según cotización") y CTA → qué es (con las fotos de main) → precio por presentación → usos → **calculadora de cantidad** (la de main de cada página, `calcularTierra`, `calcularTezontle` y `calcularMarmol`, portada a una función pura en Python y en JS con casos de paridad congelados ejecutando el JS de main, como el Medidor) → entrega → secciones propias (comparativa, combinaciones, instalación, galería) → FAQ → otros materiales → CTA con la plantilla de la página → pedido por correo (el formulario de main a formsubmit, con honeypot y `generate_lead` `method:'formulario'`). Se publica solo: el lote 4 de la hoja de ruta ya tiene 2e en producción (`4169785`).

**Architecture:** Igual que 2a–2e: `contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD`; la plantilla arma la página con `componentes.py`; `generar.py` registra la fila; `build.py` la escribe con el shell solo si cambia. Lo nuevo:
1. **`tools/site/componentes_materiales.py`** (componentes.py ya pasa de 800 renglones): `calculo()` y `textos()` (las calculadoras de main línea por línea, incluido el redondeo de `Math.ceil` sobre flotantes), `ejemplo()` (las cantidades de las preguntas frecuentes salen de la misma calculadora, no a mano), `calculadora()` (marcado), `presentaciones()` (tabla Presentación | Unidad | Precio con "Según cotización" cuando el precio no está en `datos.PRECIOS`), `otros()`, `portada()` (sin foto o con foto apaisada), `cierre()` (con la foto de fondo de main) y `formulario_pedido()`.
2. **`public/js/vt-materiales.js`** (vanilla, funciones puras exportadas para `node --test`): mismas `calcular`/`textos` que Python; los factores y precios llegan en `data-material`, escrito desde `datos.py`. El botón es un `<a data-cta="material:cotizarCalculado">` (y `cotizarTezontle`, `cotizarMarmol`, `cotizarPiedra`) cuyo `href` se recalcula: `terra.js` lo mide (`generate_lead`, el mismo `cta_id` que mandaba `VTMedicion.whatsapp('cotizarCalculado')` en main) y lo firma. Ningún `window.open` (`medicion_js.medir_whatsapp_js` cuenta 0 en las 4 páginas: prueba).
3. **Paridad Python–JS–main:** `public/js/tests/casos-materiales.json` (195 casos: 15 áreas × las capas de cada `<select>` de main, ejecutando `calcular*()`/`cotizar*()` de main en node); `tests/test_materiales_paridad.py` y `vt-materiales.test.js` exigen el mismo resultado, con las únicas diferencias que pide el dueño aplicadas explícitamente a lo que publicaba main (`esperado_de_main`).
4. **Paridad de fotos y formulario:** `tools/site/paridad_materiales.py` congela la lista ordenada de `<img>` del `<main>` de cada página (src, srcset, alt) y los campos del formulario a formsubmit; `test_materiales_reglas.py` exige las mismas fotos en el mismo orden (regla del dueño) y el mismo formulario más `_honey`.
5. **El formulario de pedido reutiliza `vt-b2b.js`** (validación junto a cada campo, foco en el primero con error, `generate_lead` `method:'formulario'`), con un cambio mínimo: el campo de correo se reconoce por `type="email"` (en materiales se llama `email`, como en main; el dueño recibe esos nombres) y el mensaje de error usa su placeholder.
6. **CSS en `terra.css`** (≈ 975 B minificado: portada sin foto y apaisada, cierre con foto, miniaturas de otros materiales, "Según cotización" en la tabla): queda en 48,489 B de 49,152 permitidos (medido en el prototipo). Sin hoja nueva ni cambios a `shell.py`, `partials.py` o `vercel.json`.

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en las pruebas de navegador; CSS plano; JavaScript vanilla (`vt-materiales.js` nuevo; `vt-b2b.js` con un cambio mínimo; `terra.js` sin cambios); `node --test` sin `package.json`; Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2f` (rama `feat/etapa-2f`, creada desde `main` en `4169785`, con este plan como primer commit). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- **Qué se probó y qué no.** El plan se prototipó sobre `4169785` en una copia de trabajo (fuera del repo) con **todo el código de las Tareas 1–11 tal como está aquí**: capturas, casos de main, las cuatro páginas migradas con su paridad en `ok` en las seis categorías, `test_materiales_reglas`, `test_materiales_paridad`, `test_componentes_materiales`, `test_material`, `test_contenido`, `test_paridad`, `test_generar`, `test_paginas`, `test_terra_css` y las pruebas de navegador nuevas en verde; `node --test` con 65; axe de página completa sin violaciones serias a 375 y 1440, sin desbordar de 320 a 1920, consola limpia, precio y CTA en el primer pantallazo a 375×812, 320×812 y 1024×800. Las salidas "Expected" son las de esa corrida. **No** se corrieron Lighthouse ni las capturas de la Tarea 12. Los archivos nuevos van completos; los cambios a archivos existentes van como bloques exactos a insertar o reemplazar con el editor. Si una prueba no da lo que dice el plan, arregla el código (no la prueba) salvo que la prueba contradiga el spec; anota cada desvío en el PR.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests` (≈ 3 min), `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`, incluidas en el `discover`).
- Cuando una tarea cambia `terra.css`, el build cambia el hash, reescribe el `<head>` de todas las páginas y rota las copias (`activos.json` guarda dos): se versiona todo (`git add public tools/site/activos.json`) revisando antes `git status --short | grep -v '\.html$'`.
- **Reglas del dueño en juego** (las prueban `test_reglas.py`, `test_consistencia.py` y la nueva `test_materiales_reglas.py`):
  - **Precios solo de `datos.PRECIOS`** (verificados el 2026-11-08): tierra negra **$90 el costal** (`tierra_negra_costal`) y **$1,500 el m³** (`tierra_negra_m3`); tezontle **desde $200 el costal** (`tezontle_costal`, "desde" como en la home). Todo lo demás va **"Según cotización"** (con mayúscula en etiqueta y tablas, `datos.SEGUN_COTIZACION`; en minúscula a media frase): tierra preparada ($100 en main), camión de tierra ("desde $5,000"; $3,500 / $5,200 / $8,000 por 5, 8 y 14 m³ en la FAQ), m³ de tezontle ($3,200) y su camión de 14 m³, mármol ($250 el saco, $750–$1,250 por m², el "$120" de tezontle de su comparativa) y piedra bola (el `Offer` de $350 del JSON-LD). Nunca se inventa ni se "estima" un precio; las cantidades de las calculadoras no llevan precio salvo tierra negra con sus dos precios oficiales.
  - **Fotos:** las de main, todas y en el mismo orden (regla del dueño: no se quita ni se cambia ninguna; alt y pie sí pueden mejorar, nunca con "En nuestro vivero"). Por eso "qué es" va antes del precio (en mármol la foto del saco va en el precio, después de las tres de "qué es"), y en piedra bola "otros materiales" va después del CTA final, como en main. Tezontle y piedra bola no tenían foto de portada y no se les agrega ninguna.
  - Sin "gratis", "sin costo", "Cotización gratis" ni "Cotiza gratis" (también en la meta). Sin existencias ni disponibilidad ("InStock" del JSON-LD, "Disponible en cantidad sin límite", "confirmar disponibilidad"). Sin plazos de entrega que no estén en `datos.py` ("Entrega inmediata"). Pago = anticipo (`datos.ANTICIPO`). Sin "Oasis", sin el nombre del proveedor de la terminal, sin "más vendido" ni superlativos ("el mejor", "imbatible", "inigualable", "más popular", "Calidad importada"), sin cifras sin respaldo ("+500 jardines", "+300 jardines", "+18 años", "40% más rápido", "90% de la maleza", "del 60% al 95%", "hasta 8°C", "Productor directo"), sin opiniones sin permiso (Ricardo O., Laura P., Patricia H., David M. no están en `datos.OPINIONES`).
  - El formulario por correo se queda (`test_reglas.CON_FORMULARIO_CORREO` ya lista las 4 páginas): `action` a `formsubmit.co/viverosterra@hotmail.com`, mismos campos de main (`nombre`, `email`, `detalle`) y mismos ocultos (`_subject` "Pedido desde sitio web - Viveros Terra", `_next` `https://www.viverosterra.com/gracias`, `_captcha` false) más `_honey`; ancla `#solicitar-pedido` (la usa el `Offer.url` del JSON-LD de tezontle).
  - **Títulos:** se quedan como están, salvo el de mármol, que publica "$250 por Saco" (declarado en `PARIDAD["meta"]`). La consolidación de títulos es de la Etapa 3.
- Dos textos de CTA de WhatsApp y teléfono, como en 2a–2e: "Cotizar por WhatsApp" y "Llamar 833 326 8008" (el "Cotizar 8.8 m³ por WhatsApp" de main pasa a "Cotizar por WhatsApp": la cantidad ya está en la etiqueta). El botón del formulario conserva "Enviar solicitud de pedido".

## Cobertura del spec y de la hoja de ruta

| Pide el spec / la hoja de ruta / el dueño | Dónde |
|---|---|
| §3.3 material: H1 + precio por presentación (costal / m³ / camión) → usos → calculadora → entrega → FAQ → CTA | Tareas 6–10 (`plantillas/material.py`), `test_material.test_orden_de_secciones_del_spec` |
| Hoja de ruta 2f: la lógica de cada calculadora como función pura con casos de paridad, igual que el Medidor | Tareas 1, 4 y 5 (`casos-materiales.json`, `componentes_materiales.calculo/textos`, `vt-materiales.js`), `test_materiales_paridad`, `vt-materiales.test.js` |
| Hoja de ruta 2f: calculadoras con `window.open` → patrón de enlace medido y firmado (`terra.js`, `medicion_js.py`) | Tarea 6 (`<a data-cta>` con el `cta_id` de main), `test_materiales_reglas` (sin `window.open`, `medir_whatsapp_js` en 0), Tarea 11 (`generate_lead` en navegador) |
| CTA con `datos.MENSAJES["materiales"]` | Tarea 2: `mensajes_paginas.MATERIALES`, en el formato de `MENSAJES["materiales"]` (material, cantidad y "Colonia de entrega: ___") con el material ya escrito; `test_paginas.test_materiales_con_su_mensaje_en_menu_barra_y_pie` |
| Precios de `datos.PRECIOS`; mármol, piedra bola y camiones "según cotización" | `componentes_materiales.presentaciones`, contenidos, `test_materiales_reglas` (`PRECIO_RE`, `SIN_PRECIO_RE`, `test_precios_de_tierra_negra_y_tezontle_de_datos`) |
| Calculadora con los mismos resultados que hoy en los casos capturados | `test_materiales_paridad.test_mismos_resultados_que_main` (195 casos), node |
| Formulario por correo (formsubmit a viverosterra@hotmail.com, honeypot, `_next` a /gracias, `generate_lead` `formulario`) | Tareas 5 y 6 (`formulario_pedido`, `vt-b2b.js`), `test_componentes_materiales.PedidoTest`, Tarea 11 |
| Fotos exactamente como en producción | Tarea 1 (`paridad_materiales.py`), `test_materiales_reglas` (mismo orden, mismos srcset, width/height/alt) y Tarea 11 (ninguna rota) |
| §7.3 respuesta directa; §7.4 "Actualizado" visible | La entrada de cada portada es la respuesta (entidad + precio + condición + lugar). La fecha visible de main ("Última actualización: 14 de mayo, 2026") **no** se reproduce en 2f: `dateModified` y "Actualizado" son de la Etapa 4 (ver Correcciones) |
| Pruebas de cada lote: axe, sin desbordar 320–1920, consola limpia, CTA y precio en el primer pantallazo, CLS, Lighthouse, capturas | Tareas 11 y 12 |
| Puertas (spec §11): diseño, SEO/AEO (se toca JSON-LD), CRO, cumplimiento | Tarea 12 |

Fuera de 2f: títulos nuevos y "{material} por camión / costal" del spec §6 (Etapa 3); grafo JSON-LD único y `dateModified` (Etapa 4: aquí los `LocalBusiness` sueltos del `seller` pasan a la referencia `#negocio`, como en 2d y 2e); `/vivero-tampico` (Etapa 3); borrar `servicios.css`, `design-system.css` y `tools/servicios` (2i: aún los usa el vivero).

## Decisiones de diseño (y por qué)

- **Paridad exacta con main, incluidos sus redondeos.** `Math.ceil(area * capa * 10) / 10` sube con el error de los flotantes: 7 m² × 10 cm da 0.8 m³ en main (7 × 0.1 × 10 = 7.000000000000001), 140 m² × 8 cm da 11.3 m³. Python hace la misma operación en el mismo orden y da lo mismo (comprobado en los 195 casos). Se conserva (la aceptación es "mismos resultados que hoy") y se pregunta al dueño si se corrige (pregunta 8): sobrestima a lo más 0.1 m³.
- **Las diferencias con main son pocas y van escritas en la prueba** (`esperado_de_main`): el camión de tierra negra dice "Camión volteo de 8 m³ o más (según cotización)" en vez de "(~desde $5,000)"; el mármol pierde "Total orientativo", "A $250 c/u." y "Precio estimado"; "2 sacos cubre" pasa a "cubren"; la pregunta final del mármol ("¿Pueden confirmar disponibilidad y precio…?") pasa a la de los otros dos ("¿Me pueden dar precio de entrega a domicilio en Tampico?"). Los textos de las capas de tezontle quedan idénticos a los de main porque van en el mensaje ("Uso: …"); los de tierra y mármol cambian de forma (no van en el mensaje). Las cantidades grandes conservan el formato de main ("~4286 costales", "5000 kg"): la aceptación es exacta.
- **El área se lee como en empresas** (`leer_area` = `leer_m2`): "1,200" es 1200 y "12,5" es 12.5 (main con `parseFloat` leía 1 y 12). Sin área válida la calculadora no inventa un resultado: muestra "Escribe el área" y el botón manda el mensaje de la página (como el Medidor). Ya no hay `alert()`.
- **Piedra bola no tenía calculadora.** La nueva solo multiplica el área por los 120 a 150 kg por m² que publicaba su propia FAQ (piedra mediana, capa de 8 a 10 cm; "10 m² → 1,200 a 1,500 kg" es su caso de paridad). Sin precio. Pregunta 6 al dueño; si no la aprueba, se quita la sección y su FAQ vuelve a ser texto.
- **Presentaciones en tabla, no en tarjetas con botón:** tierra tiene 4 presentaciones y `componentes.opciones` admite 3 (spec §3.3); la tabla con columna Unidad es la de los demás precios del sitio y "Según cotización" cabe a 320 px (`.vt-tabla__p--cotiza`). Un solo CTA por página más el de la calculadora: se retiran los botones por presentación y por uso (los usos de tierra abrían 6 WhatsApp distintos); el uso ya va en el `<select>` de la calculadora.
- **Etiqueta de la portada con número primero (spec §5.3):** tierra "$90 por costal" (m³ $1,500; camión según cotización); tezontle "desde $200 por costal"; mármol "3 sacos cubren 1 m²" con "Precio por saco: Según cotización"; piedra bola "3 medidas" con chica 2–5, mediana 6–12 y grande 12–20 cm y "Precio: Según cotización" (las medidas son las de su FAQ). Así el primer pantallazo lleva precio o "según cotización" y CTA en las cuatro.
- **La foto de portada de tierra negra es 3:2:** `cm.portada` le pone `vt-portada--apaisada` (marco 3:2) en vez de recortarla a 4:5; la de mármol (3:4) usa `componentes.portada` tal cual. Las fotos del CTA final de main (decorativas, `alt=""`, al 15–20 %) se quedan como fondo del cierre al 15 %.
- **Otros materiales:** las miniaturas solo donde main las tenía (mármol y piedra bola: tezontle y tierra negra), a 48 px (son de 194 a 821 px: no se agrandan) y con `alt=""` porque el nombre va al lado. En tierra y tezontle main tenía enlaces de texto: se quedan sin foto. Cada material dice sus precios de `datos.py`.
- **Formulario de pedido con `vt-b2b.js`:** el de empresas ya valida junto a cada campo, lleva el foco al primero con error y manda `generate_lead` `method:'formulario'`; se reutiliza en vez de escribir otro. El cambio es que el campo de correo se busca por `type="email"` (aquí `name="email"`) y su error dice "debe verse como tu@correo.com" (el placeholder). Las páginas B2B no cambian (mismo mensaje, prueba en node).
- **JSON-LD:** `Product` con la marca de main; `offers` solo con precios de `datos.py` (tierra `AggregateOffer` 90–1,500, tezontle `Offer` 200) y `seller` `{"@id": ".../#negocio"}`; mármol y piedra bola sin `Offer` (sus precios no están en `datos.py`); nunca `InStock`. `FAQPage` = preguntas visibles; `BreadcrumbList` = migas visibles (Inicio › material); `HowTo` de mármol como estaba; `SpeakableSpecification` con `#vt-h1`, la entrada y las preguntas.

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{tierra-negra-vegetal-tampico,tezontle-rojo-tampico,marmol-blanco-tampico,piedra-bola-rio-tampico}.json` | Lo que publicaba cada página antes de migrar (`paridad.py capturar`). |
| `tools/site/paridad_materiales.py`, `tools/site/tests/paridad/materiales-fotos.json` | Fotos (en orden) y formulario de main. |
| `public/js/tests/casos-materiales.json` | 195 casos de las tres calculadoras de main, ejecutando su JS. |
| `tools/site/componentes_materiales.py` | Calculadora (lógica y marcado), presentaciones, otros materiales, portada, cierre y pedido. |
| `public/js/vt-materiales.js`, `public/js/tests/vt-materiales.test.js` | Calculadora en el navegador; pruebas de `node --test`. |
| `tools/site/plantillas/material.py` | La plantilla nueva. |
| `tools/site/contenido/materiales_comun.py` | Entrega, pedido, otros materiales, migas, producto y motivos de paridad comunes. |
| `tools/site/contenido/{tierra_negra,tezontle_rojo,marmol_blanco,piedra_bola}.py` | Contenido de cada página. |
| `tools/site/tests/{test_materiales_reglas,test_materiales_paridad,test_componentes_materiales,test_material}.py` | Pruebas nuevas. |

Se modifican: `tools/site/mensajes_paginas.py`, `generar.py`, `public/css/terra.css`, `public/js/vt-b2b.js`, `public/js/tests/vt-b2b.test.js`, `tools/servicios/pages.py`, `tools/servicios/tests/test_pagos.py`; pruebas `test_paginas`, `test_generar`, `test_terra_css`, `test_navegador`, `test_plantillas_navegador`. Regenerados por el build: las 4 páginas, `public/css/terra.<hash>.css`, `tools/site/activos.json` y el `<head>` de todas las páginas.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar el worktree**

```bash
cd ~/dev/viverosterra-e2f && git branch --show-current && git log --oneline -2
```

Expected: `feat/etapa-2f`; arriba el commit de este plan (`docs(plan): etapa 2f materiales`) y debajo `4169785 merge: etapa 2e — plantas: hub, subcategorías y catálogo con fotos locales`. Si no existe: `git -C ~/dev/viverosterra worktree add ~/dev/viverosterra-e2f -b feat/etapa-2f`.

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
```

Expected (verificado en `4169785`): `plantillas: 0 de 37 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 522 tests` y `OK` (unos 3 min); `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 60` y `ℹ fail 0`; `playwright ok`.

---

### Task 1: Capturas de paridad, fotos y casos de las calculadoras de main

**Files:**
- Create: `tools/site/tests/paridad/` (4 capturas), `tools/site/paridad_materiales.py`, `tools/site/tests/paridad/materiales-fotos.json`, `public/js/tests/casos-materiales.json`

- [ ] **Step 1: Capturar las 4 páginas tal como están**

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/paridad.py capturar /tierra-negra-vegetal-tampico /tezontle-rojo-tampico /marmol-blanco-tampico /piedra-bola-rio-tampico
python3 -c "
import json
for p in ('tierra-negra-vegetal-tampico','tezontle-rojo-tampico','marmol-blanco-tampico','piedra-bola-rio-tampico'):
    d=json.load(open(f'tools/site/tests/paridad/{p}.json')); print(p, len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']), len(d['jsonld_tipos']))"
```

Expected: cuatro líneas `captura: …` y luego (verificado):
```
tierra-negra-vegetal-tampico 19 10 7 5 10
tezontle-rojo-tampico 29 11 4 8 10
marmol-blanco-tampico 25 10 11 8 12
piedra-bola-rio-tampico 13 6 3 3 6
```

- [ ] **Step 2: Escribir `tools/site/paridad_materiales.py`**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/paridad_materiales.py <<'EOF'
"""Paridad de las fotos y del formulario de pedido de las páginas de materiales (Etapa 2f).

Regla del dueño: cada foto de main se queda, en el mismo orden, sin quitar ni cambiar ninguna (el alt y el pie sí pueden
mejorar). paridad.py no ve imágenes; aquí se congela, por página, la lista ordenada de las <img> del <main> (sin logos)
con su src, srcset y alt, y los nombres y valores del formulario por correo a formsubmit (el dueño recibe esos campos).
tests/test_materiales_paridad.py exige que las páginas nuevas publiquen las mismas fotos en el mismo orden y el mismo
formulario (más el honeypot).

Uso: python3 tools/site/paridad_materiales.py capturar   (escribe tests/paridad/materiales-fotos.json)
"""
import html as html_mod
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402

RUTAS = ("/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico")
CAPTURA = paridad.CAPTURAS / "materiales-fotos.json"
IMG_RE = re.compile(r"<img\b[^>]*>")
FORM_RE = re.compile(r'<form\b[^>]*action="https://formsubmit\.co/[^"]*"[^>]*>(.*?)</form>', re.S)
CAMPO_RE = re.compile(r'<(?:input|textarea|select)\b[^>]*\bname="([^"]+)"[^>]*>')


def atributo(etiqueta, nombre):
    m = re.search(rf'\s{nombre}="([^"]*)"', etiqueta)
    return html_mod.unescape(m.group(1)) if m else None


def fotos(html):
    """[{src, srcset, alt}] de las <img> del <main>, en orden, sin los logos."""
    salida = []
    for etiqueta in IMG_RE.findall(paridad.principal(html)):
        src = atributo(etiqueta, "src")
        if src and not src.startswith("/img/logo"):
            salida.append({"src": src, "srcset": atributo(etiqueta, "srcset"), "alt": atributo(etiqueta, "alt")})
    return salida


def formulario(html):
    """{name: value} de los campos del formulario a formsubmit ("" si no lleva value)."""
    m = FORM_RE.search(html)
    if not m:
        return {}
    return {atributo(c, "name"): atributo(c, "value") or "" for c in (x.group(0) for x in CAMPO_RE.finditer(m.group(1)))}


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"fotos": fotos(html), "formulario": formulario(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_materiales.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), sorted(d["formulario"]))
EOF
python3 tools/site/paridad_materiales.py capturar
```

Expected (verificado):
```
/tierra-negra-vegetal-tampico 8 ['_captcha', '_next', '_subject', 'detalle', 'email', 'nombre']
/tezontle-rojo-tampico 4 ['_captcha', '_next', '_subject', 'detalle', 'email', 'nombre']
/marmol-blanco-tampico 8 ['_captcha', '_next', '_subject', 'detalle', 'email', 'nombre']
/piedra-bola-rio-tampico 3 ['_captcha', '_next', '_subject', 'detalle', 'email', 'nombre']
```
Las 23 fotos, en orden: tierra = portada (`portadas/camion-tierra-negra-entrega-tampico-sm.webp` con srcset 560/960), 3 de "¿Por qué…?" (`tierra-negra-preparacion-pasto`, `tierra-negra-camion-volteo`, `tierra-negra-suministro-jardin`), 3 de la galería (`camion-tierra-negra-descarga`, `tierra-negra-vegetal-costales`, `tierra-negra-sacos-viveros-terra`) y el fondo del CTA (`camion-tierra-negra-entrega-tampico.webp`, `alt=""`); tezontle = 3 de "¿Por qué…?" (`tezontle-rojo-jardin-tampico-sendero` 194×259, `tezontle-rojo-jardin-lateral` 259×194, `tezontle-rojo-bordillo-jardin` 259×195) y el fondo del CTA (la misma del bordillo); mármol = portada (srcset 560/900), 3 de "¿Por qué…?" (`marmol-blanco-alberca-palmera`, `marmol-blanco-arriate-suculentas`, `marmol-blanco-maceta-decorativa`), el saco (`marmol-blanco-saco-costal`, alt con "$250"), 2 miniaturas de otros materiales (tezontle sendero, tierra camión volteo) y el fondo del CTA (`jardin-residencial-pasto-san-agustin`); piedra bola = fondo del CTA (`jardin-residencial-plantas-pasto`) y las 2 miniaturas.

- [ ] **Step 3: Congelar las calculadoras de main ejecutando su JS**

Script de un solo uso (no se versiona): saca de cada página solo `calcular*()` y `cotizar*()` (en mármol comparten `<script>` con el menú y el FAQ, que piden un DOM real), las corre con un DOM mínimo para 15 áreas × cada capa del `<select>` de main y escribe lo que se veía y el mensaje que abría `window.open`.

```bash
cd ~/dev/viverosterra-e2f
node - > public/js/tests/casos-materiales.json <<'EOF'
const fs = require('fs');
const vm = require('vm');
// (página, función de cálculo, función de cotizar, id del área, id de la capa)
const CALCULADORAS = {
  'tierra-negra': ['public/tierra-negra-vegetal-tampico/index.html', 'calcularTierra', 'cotizarCalculado', 'calc-area', 'calc-grosor'],
  tezontle: ['public/tezontle-rojo-tampico/index.html', 'calcularTezontle', 'cotizarTezontle', 'tez-area', 'tez-uso'],
  marmol: ['public/marmol-blanco-tampico/index.html', 'calcularMarmol', 'cotizarMarmol', 'calc-area', 'calc-grosor'],
};
const AREAS = [0.5, 1, 7, 10, 12.5, 18.75, 30, 50, 80, 87.5, 100, 140, 200, 333, 1000];
const textoOpcion = (s) => s.replace(/<[^>]*>/g, '').replace(/[\t\n\f\r ]+/g, ' ').trim();
function opciones(html, id) {
  const sel = html.match(new RegExp(`<select id="${id}"[^>]*>([\\s\\S]*?)</select>`))[1];
  return [...sel.matchAll(/<option value="([^"]*)"[^>]*>([\s\S]*?)(?=<option|$)/g)]
    .map((m) => ({ value: m[1], text: textoOpcion(m[2].replace(/<\/option>[\s\S]*$/, '')) }));
}
const salida = { origen: 'main (4169785), antes de la Etapa 2f: calcular*() y cotizar*() de cada página, ejecutados en node', calculadoras: {} };
for (const [clave, [archivo, calcular, cotizar, idArea, idCapa]] of Object.entries(CALCULADORAS)) {
  const html = fs.readFileSync(archivo, 'utf8');
  // Solo las dos funciones (en mármol comparten <script> con el menú y el FAQ, que piden un DOM real).
  const funcion = (nombre) => {
    const i = html.indexOf(`function ${nombre}(`);
    let j = html.indexOf('{', i), n = 0;
    do { if (html[j] === '{') n++; else if (html[j] === '}') n--; j++; } while (n);
    return html.slice(i, j);
  };
  const codigo = funcion(calcular) + '\n' + funcion(cotizar);
  const capas = opciones(html, idCapa);
  const els = {};
  const el = (id) => (els[id] = els[id] || { id, value: '', textContent: '', selectedIndex: 0, options: [], classList: { remove() {}, add() {} } });
  const abiertos = [];
  const ctx = { encodeURIComponent, parseFloat, parseInt, Math, alert() {},
    document: { getElementById: el }, window: { open: (u) => abiertos.push(u), VTMedicion: { whatsapp() {} } } };
  ctx.window.window = ctx.window; ctx.VTMedicion = ctx.window.VTMedicion;
  vm.createContext(ctx);
  vm.runInContext(codigo + `\n;this.__calc=${calcular};this.__cot=${cotizar};`, ctx);
  // window._calcM3 etc. viven en ctx.window: el script asigna a window.* y lee window.*.
  const casos = [];
  for (const area of AREAS) {
    capas.forEach((capa, i) => {
      Object.keys(els).forEach((k) => delete els[k]);
      el(idArea).value = String(area);
      Object.assign(el(idCapa), { value: capa.value, selectedIndex: i, options: capas });
      abiertos.length = 0;
      ctx.__calc();
      ctx.__cot();
      const visibles = Object.fromEntries(Object.values(els).filter((e) => e.textContent).map((e) => [e.id, e.textContent]));
      casos.push({ entrada: { area, capa: capa.value }, visibles, mensaje: decodeURIComponent(abiertos[0].split('text=')[1]) });
    });
  }
  salida.calculadoras[clave] = { capas, casos };
}
process.stdout.write(JSON.stringify(salida, null, 1) + '\n');
EOF
python3 -c "
import json; d=json.load(open('public/js/tests/casos-materiales.json'))
print({k: len(v['casos']) for k, v in d['calculadoras'].items()})
c=d['calculadoras']['tierra-negra']['casos'][38]; print(c['entrada'], c['visibles']['res-formato'])
c=d['calculadoras']['marmol']['casos'][0]; print(repr(c['mensaje']))"
```

Expected (verificado):
```
{'tierra-negra': 60, 'tezontle': 75, 'marmol': 60}
{'area': 87.5, 'capa': '0.10'} Camión volteo 8m³+ (~desde $5,000)
'Hola, quiero cotizar mármol blanco decorativo.\n\nDatos de mi proyecto:\nÁrea: 0.5 m²\nCapa: 3 cm\nCantidad: 2 sacos\nPrecio estimado: $500\n\n¿Pueden confirmar disponibilidad y precio de entrega a domicilio en Tampico?'
```

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/tests/paridad/tierra-negra-vegetal-tampico.json tools/site/tests/paridad/tezontle-rojo-tampico.json \
  tools/site/tests/paridad/marmol-blanco-tampico.json tools/site/tests/paridad/piedra-bola-rio-tampico.json \
  tools/site/paridad_materiales.py tools/site/tests/paridad/materiales-fotos.json public/js/tests/casos-materiales.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de los 4 materiales, sus fotos y formulario, y los casos de las calculadoras de main" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Mensaje de WhatsApp de cada material

**Files:**
- Modify: `tools/site/mensajes_paginas.py`
- Test: `tools/site/tests/test_paginas.py`

- [ ] **Step 1: Prueba en rojo**

En `tools/site/tests/test_paginas.py`, antes de `def test_ruta_desconocida_falla(self):`, agrega:

```python
    def test_materiales_con_su_mensaje_en_menu_barra_y_pie(self):
        """Etapa 2f: los cuatro materiales llevan en el menú, la barra y el pie la plantilla de su portada, con la colonia
        de entrega de datos.MENSAJES["materiales"]."""
        colonia = datos.MENSAJES["materiales"].split("\n")[-1]
        for ruta, texto in mensajes_paginas.MATERIALES.items():
            ctx = paginas.contexto(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(ctx["mensaje"], datos.con_firma(texto))
                self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
                self.assertEqual(ctx["servicio"], "materiales")
                self.assertTrue(texto.startswith("Hola, quiero cotizar "))
                self.assertIn(colonia, texto)
        self.assertEqual(sorted(mensajes_paginas.MATERIALES),
                         ["/marmol-blanco-tampico", "/piedra-bola-rio-tampico", "/tezontle-rojo-tampico",
                          "/tierra-negra-vegetal-tampico"])
```

Run: `cd tools/site && python3 -m unittest tests.test_paginas 2>&1 | tail -3`
Expected: `ERROR` (`AttributeError: module 'mensajes_paginas' has no attribute 'MATERIALES'`).

- [ ] **Step 2: Los mensajes**

En `tools/site/mensajes_paginas.py`, después del diccionario `PLANTAS` (antes de `# Ruta exacta → (mensaje del menú…`), agrega (son los textos de `tools/servicios/pages.py`, `guided()`, con los huecos `___`):

```python
# Materiales (Etapa 2f): la plantilla de main de cada portada (tools/servicios/pages.py, guided()), con los huecos ___:
# el formato de datos.MENSAJES["materiales"] (material, cantidad y colonia de entrega) con el material ya escrito. La usan
# la portada, el cierre y la calculadora mientras no tiene área y, por RUTAS, el menú, la barra móvil y el pie.
MATERIALES = {
    "/tierra-negra-vegetal-tampico": ("Hola, quiero cotizar tierra negra.\nCostales o camión: ___\nCantidad: ___\n"
                                      "Colonia de entrega: ___"),
    "/tezontle-rojo-tampico": ("Hola, quiero cotizar tezontle rojo.\nCostales o camión: ___\nCantidad: ___\n"
                               "Colonia de entrega: ___"),
    "/marmol-blanco-tampico": ("Hola, quiero cotizar mármol blanco.\nMetros a cubrir: ___\nColonia de entrega: ___\n"
                               "Les mando foto del espacio."),
    "/piedra-bola-rio-tampico": ("Hola, quiero cotizar piedra bola de río.\nMedida: ___\nMetros a cubrir: ___\n"
                                 "Colonia de entrega: ___\nLes mando foto del espacio."),
}
```

y en `RUTAS`, después de `**{ruta: (texto, None) for ruta, texto in PLANTAS.items()},`:

```python
    **{ruta: (texto, None) for ruta, texto in MATERIALES.items()},
```

Run: `cd tools/site && python3 -m unittest tests.test_paginas tests.test_reglas 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 3: Build y commit**

El menú, la barra móvil y el pie de las 4 páginas (aún a mano) pasan al mensaje de su portada.

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -1
git status --short | grep -v '\.html$'
git add tools/site/mensajes_paginas.py tools/site/tests/test_paginas.py public/tierra-negra-vegetal-tampico/index.html \
  public/tezontle-rojo-tampico/index.html public/marmol-blanco-tampico/index.html public/piedra-bola-rio-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): mensaje de WhatsApp de cada material en menú, barra y pie" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `shell: 4 de 108 páginas actualizadas`; el `grep` solo lista los dos `.py`.

---

### Task 3: Reglas de materiales en rojo

**Files:**
- Create: `tools/site/tests/test_materiales_reglas.py`

Las cuatro páginas empiezan en `PENDIENTES` (hoy rompen las reglas: `test_pendientes_todavia_fallan` lo comprueba) y cada tarea de migración saca la suya.

- [ ] **Step 1: Escribir la prueba**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/tests/test_materiales_reglas.py <<'EOF'
"""Reglas del dueño en las páginas de materiales (Etapa 2f): precios solo de datos.py (lo demás "según cotización"), sin
"gratis" ni existencias ni plazos de entrega, sin superlativos ni cifras sin respaldo, sin opiniones sin permiso, sin
"En nuestro vivero" en fotos, sin window.open, las mismas fotos de main en su orden y el formulario de pedido intacto.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca la
suya) y al cerrar la Etapa 2f queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import medicion_js  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import paridad_materiales  # noqa: E402
from componentes import dinero  # noqa: E402

PUBLIC = paginas.PUBLIC
MATERIALES = {
    "/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html",
    "/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",
    "/marmol-blanco-tampico": "marmol-blanco-tampico/index.html",
    "/piedra-bola-rio-tampico": "piedra-bola-rio-tampico/index.html",
}
PENDIENTES = frozenset({"/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico", "/marmol-blanco-tampico",
                        "/piedra-bola-rio-tampico"})
CAPTURA = json.loads(paridad_materiales.CAPTURA.read_text(encoding="utf-8"))
PERMITIDOS = {dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))
              if isinstance(n, int)}
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Presentaciones sin precio publicado (regla del dueño: "según cotización"). $250 sí está en datos.py (palmas y
# flamboyán), así que el mármol a $250 solo se detecta por cercanía, como las palmas sin precio de 2e.
SIN_PRECIO_RE = re.compile(r"(?:m[aá]rmol|\bsacos?\b|piedra bola|preparada|cami[oó]n(?:es)?)[^.$]{0,30}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b"),
    ("existencias o disponibilidad", r"InStock|\bdisponibilidad\b|\ben existencia\b|\bdisponibles? (?:hoy|ya)\b"
                                     r"|cantidad sin l[ií]mite|\bagotad"),
    ("plazo de entrega", r"entrega inmediata|entrega (?:el )?mismo d[ií]a|\ben 24 ?h|\bhoy mismo\b|entrega r[aá]pida"),
    ("más vendido o superlativo", r"m[aá]s vendid|\+\s?vendid|\bel mejor\b|\bimbatible\b|\bincomparable\b"
                                  r"|\binigualable\b|m[aá]s popular|calidad importada"),
    ("cifras sin respaldo", r"\+\s?500 jardines|\+\s?300 jardines|\+\s?18 años|\b\d{2}\s?% (?:m[aá]s r[aá]pido|de la maleza)"
                            r"|del 60\s?% al 95\s?%|hasta 8\s?°C|productor directo"),
    ("opiniones sin permiso", r"Ricardo O\.|Laura P\.|Patricia H\.|David M\."),
    ("En nuestro vivero", r"en nuestro vivero"),
)


def html_de(ruta):
    return (PUBLIC / MATERIALES[ruta]).read_text(encoding="utf-8")


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
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, texto, re.I)]
    if datos.ANTICIPO not in texto:
        salida.append("sin datos.ANTICIPO")
    if "window.open(" in html or medicion_js.medir_whatsapp_js(html)[1] != {"eventos": 0, "aperturas": 0, "omitidas": 0}:
        salida.append("abre WhatsApp con window.open (debe ser un enlace con data-cta)")
    nuevas = paridad_materiales.extraer(ruta)
    if [f["src"] for f in nuevas["fotos"]] != [f["src"] for f in CAPTURA[ruta]["fotos"]]:
        salida.append(f"fotos distintas a las de main o en otro orden: {[f['src'] for f in nuevas['fotos']]}")
    for vieja, nueva in zip(CAPTURA[ruta]["fotos"], nuevas["fotos"]):
        if vieja["srcset"] and nueva["srcset"] != vieja["srcset"]:
            salida.append(f"srcset distinto en {vieja['src']}")
    for img in re.findall(r"<img\b[^>]*>", paridad.principal(html)):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    esperado = dict(CAPTURA[ruta]["formulario"], _honey="")
    if nuevas["formulario"] != esperado:
        salida.append(f"formulario distinto al de main: {nuevas['formulario']}")
    if f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}"' not in html or 'id="solicitar-pedido"' not in html:
        salida.append("formulario sin la cuenta oficial o sin el ancla #solicitar-pedido")
    return salida


class MaterialesReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(MATERIALES) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_precios_de_tierra_negra_y_tezontle_de_datos(self):
        """Los únicos precios de materiales que dio el dueño (datos.PRECIOS), verificados el 2026-11-08."""
        p = datos.PRECIOS
        self.assertEqual((p["tierra_negra_costal"], p["tierra_negra_m3"], p["tezontle_costal"]), (90, 1500, 200))
        for clave in p:
            with self.subTest(clave=clave):
                self.assertFalse(re.search(r"marmol|piedra|camion", clave), "precio nuevo: confírmalo con el dueño")

    def test_las_reglas_detectan_lo_que_deben(self):
        for frase in ("Cotización gratis", "availability InStock", "Entrega inmediata", "el mejor", "+500 jardines",
                      "Ricardo O.", "En nuestro vivero", "Disponible en cantidad sin límite", "más vendido"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        for frase in ("Saco ≈ 20 kg a $250", "camión desde $5,000", "Tierra preparada $100"):
            with self.subTest(frase=frase):
                self.assertTrue(SIN_PRECIO_RE.search(frase))
        self.assertFalse(any(re.search(patron, "desde 2007 · 15 a 20 días de arraigo", re.I) for _r, patron in SIN_VERIFICAR))


if __name__ == "__main__":
    unittest.main()
EOF
(cd tools/site && python3 -m unittest tests.test_materiales_reglas 2>&1 | tail -1)
(cd tools/site && python3 -c "
import sys; sys.path.insert(0, 'tests'); sys.path.insert(0, '.')
import test_materiales_reglas as t
for r in t.MATERIALES: print(r, len(t.fallas(r)))")
```

Expected: `OK` y, en main (verificado tras la Tarea 2), cuatro rutas con fallas (tierra 45, tezontle 26, mármol 36, piedra bola 12): precios fuera de `datos.py`, "gratis", `InStock`, "más popular", opiniones sin permiso, `window.open`, formulario sin `_honey`. Ninguna en 0.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/tests/test_materiales_reglas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(materiales): reglas del dueño para las 4 páginas (pendientes hasta migrarlas)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Las calculadoras de main como funciones puras en Python

**Files:**
- Create: `tools/site/componentes_materiales.py` (primera parte), `tools/site/tests/test_materiales_paridad.py`

- [ ] **Step 1: Prueba en rojo**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/tests/test_materiales_paridad.py <<'EOF'
"""Las calculadoras de materiales dan lo mismo que en main (calcularTierra, calcularTezontle y calcularMarmol, congeladas
en public/js/tests/casos-materiales.json ejecutando el JS de main) en Python (componentes_materiales.py) y en JavaScript
(public/js/vt-materiales.js; vt-materiales.test.js corre los mismos casos). Las únicas diferencias con main son las que
pide el dueño y se aplican aquí a lo que publicaba main antes de comparar (esperado_de_main)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_materiales as cm  # noqa: E402
import datos  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-materiales.json")
                   .read_text(encoding="utf-8"))
CAMION_MAIN = "Camión volteo 8m³+ (~desde $5,000)"


def esperado_de_main(clave, caso):
    """Lo que mostraba y mandaba main, con los cambios declarados: el camión de tierra negra sin el "desde $5,000" (no
    está en datos.py), el mármol sin "$250 c/u" ni "Precio estimado" (no está en datos.py), "cubren" en vez de "cubre"
    y la pregunta de cierre del mármol igual a la de los otros dos (sin "confirmar disponibilidad")."""
    v, m = caso["visibles"], caso["mensaje"]
    if clave == "tierra-negra":
        return {"cantidad": v["res-m3"], "presentacion": v["res-formato"].replace(CAMION_MAIN, cm.CAMION_TIERRA),
                "equivalente": v["res-costales"], "mensaje": m}
    if clave == "tezontle":
        return {"cantidad": v["tez-res-m3"], "presentacion": v["tez-res-formato"], "equivalente": v["tez-res-costales"],
                "mensaje": m}
    lineas = [x for x in m.split("\n") if not x.startswith("Precio estimado: ")]
    lineas[-1] = cm.CIERRE_MENSAJE
    return {"cantidad": f"{v['res-sacos']} sacos", "peso": v["res-peso"],
            "nota": v["res-nota"].replace(" sacos cubre ", " sacos cubren ").replace(" A $250 c/u.", ""),
            "mensaje": "\n".join(lineas)}


class MaterialesParidadTest(unittest.TestCase):
    def test_mismos_resultados_que_main(self):
        for clave, calc in CASOS["calculadoras"].items():
            usos = {o["value"]: o["text"] for o in calc["capas"]}
            for caso in calc["casos"]:
                area, capa = caso["entrada"]["area"], float(caso["entrada"]["capa"])
                r = cm.calculo(clave, area, capa)
                with self.subTest(clave=clave, entrada=caso["entrada"]):
                    self.assertEqual(cm.textos(clave, area, capa, r, usos[caso["entrada"]["capa"]]),
                                     esperado_de_main(clave, caso))

    def test_capas_de_main(self):
        """Mismos valores que los <select> de main y, en tezontle, el mismo texto (va en el mensaje como "Uso: …")."""
        for clave, calc in CASOS["calculadoras"].items():
            capas = cm.CALCULADORAS[clave]["capas"]
            with self.subTest(clave=clave):
                self.assertEqual([v for v, _t in capas], [o["value"] for o in calc["capas"]])
        self.assertEqual([t for _v, t in cm.CALCULADORAS["tezontle"]["capas"]],
                         [o["text"] for o in CASOS["calculadoras"]["tezontle"]["capas"]])

    def test_casos_con_los_redondeos_de_main(self):
        """7 m² × 10 cm daba 0.8 m³ en main (7 × 0.1 × 10 = 7.000000000000001 y Math.ceil sube): se conserva igual."""
        self.assertEqual(cm.calculo("tierra-negra", 7, 0.1)["m3"], 0.8)
        self.assertEqual(cm.calculo("tezontle", 333, 0.1)["m3"], 33.4)

    def test_piedra_bola_con_la_regla_de_su_pregunta(self):
        """Piedra bola no tenía calculadora: su pregunta frecuente decía 1,200 a 1,500 kg para 10 m² (120 a 150 kg/m²)."""
        t = cm.textos("piedra-bola", 10, 0, cm.calculo("piedra-bola", 10))
        self.assertEqual(t["cantidad"], "1,200 a 1,500 kg")
        self.assertTrue(t["mensaje"].endswith(cm.CIERRE_MENSAJE))

    def test_precios_de_la_calculadora_salen_de_datos(self):
        self.assertEqual(cm.CALCULADORAS["tierra-negra"]["precio_costal"], datos.PRECIOS["tierra_negra_costal"])
        self.assertEqual(cm.CALCULADORAS["tierra-negra"]["precio_m3"], datos.PRECIOS["tierra_negra_m3"])
        for clave in ("tezontle", "marmol", "piedra-bola"):
            with self.subTest(clave=clave):
                self.assertFalse([k for k in cm.CALCULADORAS[clave] if k.startswith("precio")])

    def test_numero_y_area_como_javascript(self):
        self.assertEqual([cm.numero_js(x) for x in (8.0, 0.1, 87.5, 1000)], ["8", "0.1", "87.5", "1000"])
        self.assertEqual([cm.leer_area(x) for x in ("1,200", "12,5", "80 m²", "", "-3", "200000")],
                         [1200, 12.5, 80, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
EOF
(cd tools/site && python3 -m unittest tests.test_materiales_paridad 2>&1 | tail -3)
```

Expected: `ModuleNotFoundError: No module named 'componentes_materiales'`.

- [ ] **Step 2: La lógica**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/componentes_materiales.py <<'EOF'
"""Componentes de las páginas de materiales (Etapa 2f): calculadora de cantidad, tabla de presentaciones con precio o
"según cotización", otros materiales, portada sin foto o con foto apaisada, cierre con la foto de fondo de main y el
formulario de pedido por correo. Funciones puras, como componentes.py (que ya pasa de 800 renglones).

La calculadora es la de main línea por línea (calcularTierra, calcularTezontle y calcularMarmol, incluidos sus
redondeos): calculo() y textos() dan lo mismo que public/js/vt-materiales.js en los casos congelados de main
(public/js/tests/casos-materiales.json; tests/test_materiales_paridad.py y vt-materiales.test.js). Piedra bola no tenía
calculadora: la suya multiplica el área por los kg por m² que publicaba su propia pregunta frecuente (120 a 150 kg por m²
con piedra mediana y capa de 8 a 10 cm). Los precios salen de datos.PRECIOS; lo que no está ahí va "según cotización".
"""
import json
import math

import componentes as c
import datos
from partials import WA_GLIFO, esc

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
AREA_MAXIMA = 100_000  # m²; más que esto no es un jardín: la calculadora vuelve al mensaje de la página
CIERRE_MENSAJE = "¿Me pueden dar precio de entrega a domicilio en Tampico?"
CAMION_TIERRA = f"Camión volteo de 8 m³ o más ({SEGUN})"

# clave → factores de main, precios de datos.py, texto del mensaje, capas (valor, texto) y la capa elegida al cargar.
# Los textos de las capas de tezontle son los de main tal cual: van en el mensaje ("Uso: …").
CALCULADORAS = {
    "tierra-negra": {
        "texto": "tierra negra vegetal", "costal_m3": 0.035,
        "precio_costal": P["tierra_negra_costal"], "precio_m3": P["tierra_negra_m3"],
        "etiqueta_capa": "Grosor de la capa", "elegida": "0.08",
        "capas": (("0.05", "5 cm · mejora superficial"), ("0.08", "8 cm · preparación para pasto (recomendado)"),
                  ("0.10", "10 cm · preparación profunda"), ("0.15", "15 cm · terreno muy pobre")),
        "cta": "cotizarCalculado",
    },
    "tezontle": {
        "texto": "tezontle rojo", "costal_m3": 0.027, "camion_m3": 14,
        "etiqueta_capa": "¿Para qué lo usas?", "elegida": "0.10",
        "capas": (("0.06", "Control de maleza (6 cm)"), ("0.08", "Control de maleza intenso (8 cm)"),
                  ("0.10", "Senderos transitables (10 cm)"), ("0.05", "Decorativo/arriates (5 cm)"),
                  ("0.04", "Capa en macetas (4 cm)")),
        "cta": "cotizarTezontle",
    },
    "marmol": {
        "texto": "mármol blanco decorativo", "kg_saco": 20,
        "etiqueta_capa": "Grosor de la capa", "elegida": "4",
        "capas": (("3", "3 cm · decorativo o macetas"), ("4", "4 cm · arriates (recomendado)"),
                  ("5", "5 cm · senderos o alberca"), ("6", "6 cm · alta densidad o tráfico")),
        "cta": "cotizarMarmol",
    },
    "piedra-bola": {
        "texto": "piedra bola de río", "kg_m2": (120, 150), "medida": "mediana (capa de 8 a 10 cm)",
        "cta": "cotizarPiedra",
    },
}
# Lo que lee vt-materiales.js en data-material: sin textos de la página ni capas (esas van en el <select>).
PARA_JS = ("costal_m3", "camion_m3", "precio_costal", "precio_m3", "kg_saco", "kg_m2", "medida", "texto")


def numero_js(x):
    """Como String(x) de JavaScript para los números de estas calculadoras: 8.0 → "8", 0.1 → "0.1"."""
    x = float(x)
    return str(int(x)) if x.is_integer() else repr(x)


def leer_area(texto):
    """m² escritos por el visitante (como leerArea de vt-materiales.js y leer_m2 de las empresas): "1,200" y "1200" son
    1200, "12,5" es 12.5 y "80 m²" es 80. Devuelve 0 si no es un número mayor que 0 y hasta AREA_MAXIMA."""
    n = c.leer_m2(texto)
    return n if n <= AREA_MAXIMA else 0


def _m3(area, capa):
    return math.ceil(area * capa * 10) / 10


def calculo(clave, area, capa=0):
    """Resultado de la calculadora de main para `area` m² con la capa `capa` (m en tierra y tezontle, cm en mármol)."""
    cfg = CALCULADORAS[clave]
    if clave == "tierra-negra":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1.5 else "m3" if m3 <= 7 else "camion"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo}
    if clave == "tezontle":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1 else "m3" if m3 <= 5 else "camion" if m3 <= cfg["camion_m3"] else "camiones"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo,
                "camiones": math.ceil(m3 / cfg["camion_m3"])}
    if clave == "marmol":
        por_m2 = 3 if capa <= 4 else 4 if capa <= 5 else 5
        sacos = math.ceil(area * por_m2)
        return {"sacos": sacos, "kg": sacos * cfg["kg_saco"], "por_m2": por_m2}
    minimo, maximo = cfg["kg_m2"]
    return {"kg": (c.redondear(area * minimo), c.redondear(area * maximo))}


def _mensaje(cfg, titulo, lineas):
    return "\n".join((f"Hola, quiero cotizar {cfg['texto']}.", "", titulo, *lineas, "", CIERRE_MENSAJE))


def textos(clave, area, capa, r, uso=""):
    """Lo que muestra la etiqueta y el mensaje de WhatsApp. Iguales a los de main salvo lo que pide el dueño: el camión de
    tierra negra sin el "desde $5,000" que no está en datos.py, el mármol sin el precio de $250 por saco y los tres con
    la misma pregunta de cierre (sin "confirmar disponibilidad")."""
    cfg = CALCULADORAS[clave]
    a = numero_js(area)
    if clave in ("tierra-negra", "tezontle"):
        m3, costales = numero_js(r["m3"]), r["costales"]
        if clave == "tierra-negra":
            presentacion = {"costales": f"{costales} costales ({c.dinero(costales * cfg['precio_costal'])})",
                            "m3": f"{m3} m³ suelto (~{c.dinero(r['m3'] * cfg['precio_m3'])})",
                            "camion": CAMION_TIERRA}[r["tramo"]]
            equivalente = f"{costales} costales" if r["tramo"] == "costales" else f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Cantidad: {m3} m³")
        else:
            presentacion = {"costales": f"{costales} costales", "m3": f"{m3} m³ suelto", "camion": "Camión 14 m³",
                            "camiones": f"{r['camiones']} camiones 14 m³"}[r["tramo"]]
            equivalente = f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Uso: {uso}", f"Cantidad: {m3} m³")
        return {"cantidad": f"{m3} m³", "presentacion": presentacion, "equivalente": equivalente,
                "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}
    if clave == "marmol":
        sacos, g = r["sacos"], numero_js(capa)
        nota = (f"{sacos} sacos cubren {a} m² con capa de {g} cm." if capa <= 4
                else f"{sacos} sacos para {a} m² con capa de {g} cm (alta densidad).")
        lineas = (f"Área: {a} m²", f"Capa: {g} cm", f"Cantidad: {sacos} sacos")
        return {"cantidad": f"{sacos} sacos", "peso": f"{r['kg']} kg", "nota": nota,
                "mensaje": _mensaje(cfg, "Datos de mi proyecto:", lineas)}
    minimo, maximo = r["kg"]
    cantidad = f"{minimo:,} a {maximo:,} kg"
    lineas = (f"Área: {a} m²", f"Medida: {cfg['medida']}", f"Cantidad aprox.: {cantidad}")
    return {"cantidad": cantidad, "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}


def ejemplo(clave, area, capa=0):
    """Cantidad para el texto de una pregunta frecuente ("8 m³", "150 sacos"): sale de la misma calculadora."""
    capa = float(capa)
    return textos(clave, area, capa, calculo(clave, area, capa))["cantidad"]


def datos_js(clave):
    cfg = CALCULADORAS[clave]
    return {"clave": clave, **{k: cfg[k] for k in PARA_JS if k in cfg}}


EOF
(cd tools/site && python3 -m unittest tests.test_materiales_paridad 2>&1 | tail -1)
```

Expected: `OK` (6 pruebas; los 195 casos de main dan lo mismo).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/componentes_materiales.py tools/site/tests/test_materiales_paridad.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): calculadoras de main como funciones puras con paridad de 195 casos" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: `vt-materiales.js` y el correo del pedido en `vt-b2b.js`

**Files:**
- Create: `public/js/vt-materiales.js`, `public/js/tests/vt-materiales.test.js`
- Modify: `public/js/vt-b2b.js`, `public/js/tests/vt-b2b.test.js`

- [ ] **Step 1: Pruebas en rojo**

```bash
cd ~/dev/viverosterra-e2f
cat > public/js/tests/vt-materiales.test.js <<'EOF'
// public/js/tests/vt-materiales.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const M = require('../vt-materiales.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-materiales.json'), 'utf8'));
// Lo que escribe componentes_materiales.datos_js(clave) en data-material (test_componentes_materiales lo compara).
const CFG = {
  'tierra-negra': { clave: 'tierra-negra', costal_m3: 0.035, precio_costal: 90, precio_m3: 1500, texto: 'tierra negra vegetal' },
  tezontle: { clave: 'tezontle', costal_m3: 0.027, camion_m3: 14, texto: 'tezontle rojo' },
  marmol: { clave: 'marmol', kg_saco: 20, texto: 'mármol blanco decorativo' },
  'piedra-bola': { clave: 'piedra-bola', kg_m2: [120, 150], medida: 'mediana (capa de 8 a 10 cm)', texto: 'piedra bola de río' },
};
const CAMION_MAIN = 'Camión volteo 8m³+ (~desde $5,000)';
const CAMION = 'Camión volteo de 8 m³ o más (según cotización)';

// Igual que esperado_de_main de tests/test_materiales_paridad.py.
function esperadoDeMain(clave, { visibles: v, mensaje: m }) {
  if (clave === 'tierra-negra') {
    return { cantidad: v['res-m3'], presentacion: v['res-formato'].replace(CAMION_MAIN, CAMION), equivalente: v['res-costales'], mensaje: m };
  }
  if (clave === 'tezontle') {
    return { cantidad: v['tez-res-m3'], presentacion: v['tez-res-formato'], equivalente: v['tez-res-costales'], mensaje: m };
  }
  const lineas = m.split('\n').filter((x) => !x.startsWith('Precio estimado: '));
  lineas[lineas.length - 1] = M.CIERRE;
  return { cantidad: `${v['res-sacos']} sacos`, peso: v['res-peso'],
    nota: v['res-nota'].replace(' sacos cubre ', ' sacos cubren ').replace(' A $250 c/u.', ''), mensaje: lineas.join('\n') };
}

test('mismos resultados que main en cada caso de casos-materiales.json', () => {
  for (const [clave, calc] of Object.entries(CASOS.calculadoras)) {
    const usos = Object.fromEntries(calc.capas.map((o) => [o.value, o.text]));
    for (const caso of calc.casos) {
      const capa = Number(caso.entrada.capa);
      const r = M.calcular(CFG[clave], caso.entrada.area, capa);
      assert.deepStrictEqual(M.textos(CFG[clave], caso.entrada.area, capa, r, usos[caso.entrada.capa]),
        esperadoDeMain(clave, caso), `${clave} ${JSON.stringify(caso.entrada)}`);
    }
  }
});

test('piedra bola: 10 m² son 1,200 a 1,500 kg, como decía su pregunta frecuente', () => {
  const cfg = CFG['piedra-bola'];
  assert.strictEqual(M.textos(cfg, 10, 0, M.calcular(cfg, 10, 0)).cantidad, '1,200 a 1,500 kg');
});

test('leerArea acepta miles y coma decimal y rechaza vacíos, negativos y áreas absurdas', () => {
  assert.deepStrictEqual(['1,200', '12,5', '80 m²', '', '-3', '200000'].map(M.leerArea), [1200, 12.5, 80, 0, 0, 0]);
});

test('el mensaje es texto plano y termina con la misma pregunta en las cuatro calculadoras', () => {
  for (const cfg of Object.values(CFG)) {
    const t = M.textos(cfg, 20, cfg.clave === 'marmol' ? 4 : 0.08, M.calcular(cfg, 20, cfg.clave === 'marmol' ? 4 : 0.08), 'x');
    assert.ok(t.mensaje.endsWith(M.CIERRE));
    assert.doesNotMatch(t.mensaje, /<|\$250|disponibilidad/);
  }
});
EOF
cat >> public/js/tests/vt-b2b.test.js <<'EOF'
test('pedido de materiales (2f): el campo email se valida con el ejemplo de su placeholder', () => {
  const e = B.erroresCorreo({ nombre: 'Ana', email: 'ana@' }, ['nombre', 'email'], { email: 'tu@correo.com' });
  assert.deepStrictEqual(e, { email: 'Revisa el correo: debe verse como tu@correo.com.' });
  assert.strictEqual(B.erroresCorreo({ correo: 'a@' }, []).correo, 'Revisa el correo: debe verse como compras@tuempresa.com.');
});
EOF
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: falla (`Cannot find module '../vt-materiales.js'` y la prueba nueva de `vt-b2b`).

- [ ] **Step 2: `public/js/vt-materiales.js`**

```bash
cd ~/dev/viverosterra-e2f
cat > public/js/vt-materiales.js <<'EOF'
// public/js/vt-materiales.js
/* Calculadoras de cantidad de las páginas de materiales (Etapa 2f): área y capa → cantidad, presentación sugerida y
   equivalente → WhatsApp con el resultado. La lógica es la de main (calcularTierra, calcularTezontle y calcularMarmol,
   que abrían WhatsApp con window.open), línea por línea, incluidos sus redondeos; casos congelados en
   tests/casos-materiales.json y la misma lógica en tools/site/componentes_materiales.py (paridad Python–JS). Los precios
   y los factores llegan en data-material, escrito desde datos.py: aquí no vive ningún precio. El botón es un enlace de
   WhatsApp con data-cta (terra.js lo mide como generate_lead y lo firma al hacer clic); sin área válida manda el mensaje
   de la página (data-mensaje). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const AREA_MAXIMA = 100000;
  const CIERRE = '¿Me pueden dar precio de entrega a domicilio en Tampico?';
  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const miles = (n) => n.toLocaleString('es-MX');
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;

  // "1,200" y "1200" son 1200; "12,5" es 12.5; "80 m²" es 80. 0 si no es un número mayor que 0 y hasta AREA_MAXIMA.
  function leerArea(texto) {
    let t = String(texto == null ? '' : texto).replace(/\s|m²|m2/gi, '');
    t = /^\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(t) ? t.replace(/,/g, '') : t.replace(',', '.');
    if (!/^\d+(?:\.\d+)?$/.test(t)) return 0;
    const n = Number(t);
    return n > 0 && n <= AREA_MAXIMA ? n : 0;
  }

  const m3De = (area, capa) => Math.ceil(area * capa * 10) / 10;

  function calcular(cfg, area, capa) {
    if (cfg.clave === 'tierra-negra') {
      const m3 = m3De(area, capa);
      const tramo = m3 <= 1.5 ? 'costales' : m3 <= 7 ? 'm3' : 'camion';
      return { m3, costales: Math.ceil(m3 / cfg.costal_m3), tramo };
    }
    if (cfg.clave === 'tezontle') {
      const m3 = m3De(area, capa);
      const tramo = m3 <= 1 ? 'costales' : m3 <= 5 ? 'm3' : m3 <= cfg.camion_m3 ? 'camion' : 'camiones';
      return { m3, costales: Math.ceil(m3 / cfg.costal_m3), tramo, camiones: Math.ceil(m3 / cfg.camion_m3) };
    }
    if (cfg.clave === 'marmol') {
      const porM2 = capa <= 4 ? 3 : capa <= 5 ? 4 : 5;
      const sacos = Math.ceil(area * porM2);
      return { sacos, kg: sacos * cfg.kg_saco, por_m2: porM2 };
    }
    return { kg: [Math.round(area * cfg.kg_m2[0]), Math.round(area * cfg.kg_m2[1])] };
  }

  function textos(cfg, area, capa, r, uso) {
    const a = String(area);
    if (cfg.clave === 'tierra-negra' || cfg.clave === 'tezontle') {
      const m3 = String(r.m3);
      const c = r.costales;
      let presentacion;
      let equivalente = `~${c} costales`;
      let lineas;
      if (cfg.clave === 'tierra-negra') {
        presentacion = { costales: `${c} costales (${dinero(c * cfg.precio_costal)})`,
          m3: `${m3} m³ suelto (~${dinero(r.m3 * cfg.precio_m3)})`,
          camion: 'Camión volteo de 8 m³ o más (según cotización)' }[r.tramo];
        if (r.tramo === 'costales') equivalente = `${c} costales`;
        lineas = [`Área: ${a} m²`, `Cantidad: ${m3} m³`];
      } else {
        presentacion = { costales: `${c} costales`, m3: `${m3} m³ suelto`, camion: 'Camión 14 m³',
          camiones: `${r.camiones} camiones 14 m³` }[r.tramo];
        lineas = [`Área: ${a} m²`, `Uso: ${uso}`, `Cantidad: ${m3} m³`];
      }
      const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Resultado de la calculadora:', ...lineas, '', CIERRE].join('\n');
      return { cantidad: `${m3} m³`, presentacion, equivalente, mensaje };
    }
    if (cfg.clave === 'marmol') {
      const g = String(capa);
      const nota = capa <= 4 ? `${r.sacos} sacos cubren ${a} m² con capa de ${g} cm.`
        : `${r.sacos} sacos para ${a} m² con capa de ${g} cm (alta densidad).`;
      const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Datos de mi proyecto:', `Área: ${a} m²`, `Capa: ${g} cm`,
        `Cantidad: ${r.sacos} sacos`, '', CIERRE].join('\n');
      return { cantidad: `${r.sacos} sacos`, peso: `${r.kg} kg`, nota, mensaje };
    }
    const cantidad = `${miles(r.kg[0])} a ${miles(r.kg[1])} kg`;
    const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Resultado de la calculadora:', `Área: ${a} m²`,
      'Medida: mediana (capa de 8 a 10 cm)', `Cantidad aprox.: ${cantidad}`, '', CIERRE].join('\n');
    return { cantidad, mensaje };
  }

  // Estado vacío: el que escribió el HTML (componentes_materiales.VACIO); se lee al arrancar para no repetir textos.
  function iniciar(caja) {
    const cfg = JSON.parse(caja.dataset.material);
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    const area = caja.querySelector('[data-vt-campo="area"]');
    const capa = caja.querySelector('[data-vt-campo="capa"]');
    const nombres = ['cantidad', 'presentacion', 'equivalente', 'peso'].filter((n) => salida(n));
    const vacio = Object.fromEntries(nombres.map((n) => [n, salida(n).textContent]));
    const nota = salida('nota');
    function actualizar() {
      const a = leerArea(area.value);
      if (!a) {
        nombres.forEach((n) => { salida(n).textContent = vacio[n]; });
        if (nota) nota.hidden = true;
        salida('cta').setAttribute('href', enlace(caja.dataset.wa, caja.dataset.mensaje));
        return;
      }
      const g = capa ? Number(capa.value) : 0;
      const uso = capa ? capa.options[capa.selectedIndex].text : '';
      const t = textos(cfg, a, g, calcular(cfg, a, g), uso);
      nombres.forEach((n) => { salida(n).textContent = t[n]; });
      if (nota) { nota.textContent = t.nota; nota.hidden = false; }
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { leerArea, calcular, textos, enlace, CIERRE };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMateriales = Object.freeze(api);
  const arrancar = () => document.querySelectorAll('[data-vt-material]').forEach(iniciar);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
EOF
```

- [ ] **Step 3: `vt-b2b.js` reconoce el correo por `type="email"`**

En `public/js/vt-b2b.js`, reemplaza

```js
  const MENSAJE_CORREO = 'Revisa el correo: debe verse como compras@tuempresa.com.';
```

por

```js
  const EJEMPLO_CORREO = 'compras@tuempresa.com';
  const MENSAJE_CORREO = `Revisa el correo: debe verse como ${EJEMPLO_CORREO}.`;
```

reemplaza la función `erroresCorreo` completa (con su comentario) por

```js
  // valores: {name: texto}; requeridos: names obligatorios en el orden del formulario; correos: {name: ejemplo} de los
  // campos de correo (el ejemplo es su placeholder; sin argumento, el campo "correo" de las páginas para empresas; desde
  // 2f también el "email" del pedido de materiales). Devuelve {name: mensaje}.
  function erroresCorreo(valores, requeridos, correos = { correo: EJEMPLO_CORREO }) {
    const errores = {};
    requeridos.forEach((n) => { if (!String(valores[n] == null ? '' : valores[n]).trim()) errores[n] = MENSAJE_REQUERIDO; });
    Object.keys(correos).forEach((n) => {
      const correo = String(valores[n] == null ? '' : valores[n]).trim();
      if (!errores[n] && correo && !CORREO_RE.test(correo)) errores[n] = `Revisa el correo: debe verse como ${correos[n]}.`;
    });
    return errores;
  }
```

en `iniciarCorreo`, después de `const valores = () => Object.fromEntries(campos.map((c) => [c.name, c.value]));`, agrega

```js
    const correos = Object.fromEntries(campos.filter((c) => c.type === 'email')
      .map((c) => [c.name, c.placeholder || EJEMPLO_CORREO]));
```

y en las dos llamadas de `iniciarCorreo` cambia `erroresCorreo(valores(), requeridos)` por `erroresCorreo(valores(), requeridos, correos)`. Actualiza el comentario de cabecera del archivo: en el renglón de `[data-vt-correo]`, "cotización por correo para compras (formsubmit)" pasa a "cotización por correo para compras y, desde 2f, el pedido de materiales (formsubmit)".

- [ ] **Step 4: En verde**

Run: `node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"`
Expected: `ℹ pass 65` y `ℹ fail 0`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add public/js/vt-materiales.js public/js/tests/vt-materiales.test.js public/js/vt-b2b.js public/js/tests/vt-b2b.test.js
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): vt-materiales.js con la paridad de main y el correo del pedido validado por vt-b2b.js" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Componentes de materiales y su CSS

**Files:**
- Modify: `tools/site/componentes_materiales.py` (segunda parte), `public/css/terra.css`
- Test: `tools/site/tests/test_componentes_materiales.py`, `tools/site/tests/test_terra_css.py`

- [ ] **Step 1: Pruebas en rojo**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/tests/test_componentes_materiales.py <<'EOF'
"""Marcado de los componentes de materiales (Etapa 2f): calculadora, presentaciones, otros materiales, portadas, cierre
con foto y formulario de pedido."""
import json
import re
import sys
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_materiales as cm  # noqa: E402
import datos  # noqa: E402

MENSAJE = "Hola, quiero cotizar tierra negra.\nCantidad: ___\nColonia de entrega: ___"


class CalculadoraTest(unittest.TestCase):
    def setUp(self):
        self.html = cm.calculadora("vt-tierra", "material", "tierra-negra", MENSAJE, "tierra negra")

    def test_empieza_vacia_y_manda_el_mensaje_de_la_pagina_firmado(self):
        self.assertIn('data-vt-o="cantidad">Escribe el área</p>', self.html)
        href = unescape(re.search(r'data-vt-o="cta" href="([^"]*)"', self.html).group(1))
        self.assertEqual(unquote(href.split("text=", 1)[1]), datos.con_firma(MENSAJE))

    def test_cta_con_el_cta_id_que_media_main(self):
        self.assertIn('data-cta="material:cotizarCalculado"', self.html)
        self.assertIn("Cotizar por WhatsApp", self.html)
        self.assertNotIn("window.open", self.html)

    def test_datos_para_el_js_salen_de_datos_py(self):
        cfg = json.loads(unescape(re.search(r'data-material="([^"]*)"', self.html).group(1)))
        self.assertEqual(cfg, {"clave": "tierra-negra", "costal_m3": 0.035, "precio_costal": 90, "precio_m3": 1500,
                               "texto": "tierra negra vegetal"})
        self.assertEqual(cm.datos_js("piedra-bola")["kg_m2"], (120, 150))

    def test_capa_con_label_y_la_de_main_elegida(self):
        self.assertIn('<label for="vt-tierra-capa">', self.html)
        self.assertIn('<option value="0.08" selected>', self.html)
        self.assertNotIn("data-vt-campo=\"capa\"", cm.calculadora("vt-p", "material", "piedra-bola", MENSAJE, "piedra bola"))

    def test_marmol_sin_precio_y_con_peso(self):
        html = cm.calculadora("vt-marmol", "material", "marmol", MENSAJE, "mármol blanco")
        self.assertIn('data-vt-o="peso"', html)
        self.assertNotIn("$", html.split("data-mensaje")[0] + html.split("</select>")[-1].split("href=")[0])


class PresentacionesTest(unittest.TestCase):
    def test_precio_de_datos_o_segun_cotizacion(self):
        html = cm.presentaciones(({"nombre": "Costal", "detalle": "≈ 20 kg", "unidad": "costal", "precio": 90},
                                  {"nombre": "Camión", "detalle": "8 m³", "unidad": "camión", "precio": None},
                                  {"nombre": "Tezontle", "detalle": "", "unidad": "costal", "precio": 200, "desde": True}),
                                 "Presentaciones")
        self.assertIn('<td class="vt-tabla__p">$90</td>', html)
        self.assertIn('<td class="vt-tabla__p vt-tabla__p--cotiza">Según cotización</td>', html)
        self.assertIn(">desde $200<", html)
        self.assertIn('<th scope="col">Unidad</th>', html)


class OtrosTest(unittest.TestCase):
    def test_miniatura_solo_donde_main_la_tenia(self):
        html = cm.otros(({"titulo": "Tezontle rojo", "href": "/tezontle-rojo-tampico", "texto": "Costal desde $200",
                          "img": {"src": "/img/t.webp", "ancho": 194, "alto": 259}},
                         {"titulo": "Piedra bola", "href": "/piedra-bola-rio-tampico", "texto": "Según cotización"}),
                        (("Pasto en rollo", "/pasto-en-rollo-tampico"),))
        self.assertEqual(html.count("<img"), 1)
        self.assertIn('width="194" height="259" alt=""', html)
        self.assertIn('También: <a href="/pasto-en-rollo-tampico">Pasto en rollo</a>.', html)


class PortadaYCierreTest(unittest.TestCase):
    P = {"kicker": "K", "h1": "H", "lede": "L", "mensaje": MENSAJE, "tambien": "T",
         "etiqueta": {"codigo": "C", "aviso": "A", "nombre": "N", "antes": "", "monto": "$90", "unidad": "por costal"}}

    def test_sin_foto_y_apaisada(self):
        sin = cm.portada(self.P, "material", (("Inicio", "/"), ("X", None)))
        self.assertIn('class="vt-portada vt-portada--sinfoto"', sin)
        self.assertNotIn("<img", sin)
        foto = {"src": "/img/a.webp", "ancho": 960, "alto": 640, "numero": 1, "alt": "a", "lugar": "l", "etapa": "e"}
        self.assertIn("vt-portada--apaisada", cm.portada(dict(self.P, foto=foto), "material", (("Inicio", "/"),)))
        vertical = dict(foto, ancho=900, alto=1200)
        self.assertNotIn("vt-portada--", cm.portada(dict(self.P, foto=vertical), "material", (("Inicio", "/"),)))

    def test_cierre_con_foto_de_fondo_decorativa(self):
        html = cm.cierre({"titulo": "T", "lede": "L", "fondo": {"src": "/img/f.webp", "ancho": 1400, "alto": 933}},
                         MENSAJE, "material")
        self.assertIn('<section class="vt-cierre vt-cierre--foto"', html)
        self.assertIn('<img class="vt-cierre__fondo" src="/img/f.webp" width="1400" height="933" alt=""', html)
        self.assertNotIn("vt-cierre--foto", cm.cierre({"titulo": "T", "lede": "L"}, MENSAJE, "material"))


class PedidoTest(unittest.TestCase):
    def test_campos_y_destino_de_main_con_honeypot(self):
        html = cm.formulario_pedido("vt-tierra", "material:formulario", "Ejemplo", "Aviso")
        self.assertIn(f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}" method="POST"', html)
        self.assertEqual(re.findall(r'name="([^"]+)"', html),
                         ["_subject", "_next", "_captcha", "_honey", "nombre", "email", "detalle"])
        self.assertIn('value="Pedido desde sitio web - Viveros Terra"', html)
        self.assertIn(f'value="{datos.SITIO}/gracias"', html)
        self.assertIn('data-cta-form="material:formulario"', html)
        self.assertIn('type="email" required', html)


if __name__ == "__main__":
    unittest.main()
EOF
```

En `tools/site/tests/test_terra_css.py`, antes de `def test_fuentes_referenciadas_existen(self):`, agrega:

```python
    def test_componentes_de_materiales(self):
        """Etapa 2f: portada sin foto y apaisada, cierre con la foto de fondo de main, otros materiales con miniatura y
        "Según cotización" en la tabla sin desbordar a 320 px."""
        for selector in (".vt-portada--sinfoto .vt-portada__grid", ".vt-portada--apaisada .vt-portada__foto .vt-fig__marco",
                         ".vt-cierre--foto", ".vt-otros img", ".vt-tabla__p--cotiza"):
            with self.subTest(selector=selector):
                self.regla(selector)
        self.assertIn("opacity:.15", self.regla(".vt-cierre__fondo"))
        self.assertIn("white-space:normal", self.regla(".vt-tabla__p--cotiza"))
```

Run: `cd tools/site && python3 -m unittest tests.test_componentes_materiales tests.test_terra_css 2>&1 | tail -3`
Expected: `FAILED` (`AttributeError: … has no attribute 'calculadora'` y los selectores que faltan).

- [ ] **Step 2: El marcado**

Agrega al final de `tools/site/componentes_materiales.py`:

```python
VACIO = {"cantidad": "Escribe el área", "fila": "—"}
# Filas de la etiqueta por calculadora: (rótulo, salida). La nota va aparte.
FILAS = {
    "tierra-negra": (("Presentación sugerida", "presentacion"), ("Equivalente en costales", "equivalente")),
    "tezontle": (("Presentación sugerida", "presentacion"), ("Costales equivalentes", "equivalente")),
    "marmol": (("Peso aproximado", "peso"),),
    "piedra-bola": (),
}
NOTAS = {
    "tierra-negra": ("m² × grosor de la capa = m³, redondeado hacia arriba. Costal ≈ 20 kg. El camión volteo y la "
                     "entrega se cotizan según tu colonia."),
    "tezontle": "m² × grosor de la capa = m³, redondeado hacia arriba. El m³ y el camión se cotizan según tu colonia.",
    "marmol": "3 sacos por m² con capa de 3 a 4 cm; 4 con 5 cm y 5 con 6 cm. El precio por saco se cotiza.",
    "piedra-bola": ("Con piedra mediana y capa de 8 a 10 cm se usan de 120 a 150 kg por m². Para chica o grande, "
                    "escríbenos la medida y te calculamos."),
}


def _select(prefijo, cfg):
    opciones = "".join(f'<option value="{esc(v)}"{" selected" if v == cfg["elegida"] else ""}>{t}</option>'
                       for v, t in cfg["capas"])
    return (f'<div class="vt-campo"><label for="{esc(prefijo)}-capa">{cfg["etiqueta_capa"]}</label>'
            f'<div class="vt-control"><select id="{esc(prefijo)}-capa" data-vt-campo="capa">{opciones}</select></div></div>')


def calculadora(prefijo, tipo, clave, mensaje, nombre):
    """Área (y capa) → etiqueta con la cantidad, la presentación sugerida y su equivalente → WhatsApp con el resultado.
    Empieza vacía: sin área, el botón manda el mensaje de la página (data-mensaje, con firma). data-cta conserva el
    cta_id que medía main con VTMedicion.whatsapp (p. ej. material:cotizarCalculado)."""
    cfg = CALCULADORAS[clave]
    generico = datos.con_firma(mensaje)
    capa = _select(prefijo, cfg) if "capas" in cfg else ""
    filas = "".join(f'<p class="vt-etiqueta__fila"><span>{rotulo}</span><b data-vt-o="{salida}">{VACIO["fila"]}</b></p>'
                    for rotulo, salida in FILAS[clave])
    nota_dinamica = '<p class="vt-medidor__calc" data-vt-o="nota" hidden></p>' if clave == "marmol" else ""
    return (
        f'<div class="vt-b2b" data-vt-material data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
        f'data-mensaje="{esc(generico)}" data-material="{esc(json.dumps(datos_js(clave), ensure_ascii=False, separators=(",", ":")))}">'
        f'<div class="vt-b2b__form" role="group" aria-label="Calculadora de {esc(nombre)}">'
        f'{c._campo(f"{prefijo}-area", "area", "Área a cubrir", "Ej. 30", "m²", "decimal")}{capa}</div>'
        '<div class="vt-etiqueta-x"><div class="vt-etiqueta vt-medidor__res" role="status">'
        '<p class="vt-etiqueta__cod"><span>Tu cálculo</span><span>Aproximado</span></p>'
        f'<p class="vt-etiqueta__nombre" data-vt-o="cantidad">{VACIO["cantidad"]}</p>{filas}{nota_dinamica}'
        f'<p class="vt-medidor__calc">{NOTAS[clave]}</p>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:{cfg["cta"]}" data-vt-o="cta" '
        f'href="{esc(datos.wa_url(generico))}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp'
        '<span class="vt-flecha" aria-hidden="true">→</span></a></div></div></div>')


# ---------- precio por presentación ----------
def precio_texto(precio, desde=False):
    """"$90", "desde $200" o "Según cotización" (None: el precio no está en datos.py)."""
    if precio is None:
        return datos.SEGUN_COTIZACION
    return f"{'desde ' if desde else ''}{c.dinero(precio)}"


def presentaciones(filas, caption):
    """Tabla Presentación | Unidad | Precio. filas: nombre, detalle, unidad, precio (número de datos.PRECIOS o None) y,
    opcional, desde. None se escribe "según cotización": nunca se inventa un precio."""
    cuerpo = "".join(
        f'<tr><th scope="row"><b>{f["nombre"]}</b><span>{f["detalle"]}</span></th><td class="vt-tabla__u">{f["unidad"]}'
        f'</td><td class="vt-tabla__p{"" if f["precio"] else " vt-tabla__p--cotiza"}">{precio_texto(f["precio"], f.get("desde"))}'
        '</td></tr>' for f in filas)
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            '<th scope="col">Presentación</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{cuerpo}</tbody></table>')


# ---------- otros materiales ----------
def otros(items, enlaces=()):
    """Los otros materiales (nombre, precios de datos.py y, solo donde main la tenía, su miniatura) y una línea de enlaces
    a páginas relacionadas. items: titulo, href, texto y, opcional, img (src, ancho, alto)."""
    filas = []
    for i in items:
        foto = (f'<img src="{esc(i["img"]["src"])}" width="{i["img"]["ancho"]}" height="{i["img"]["alto"]}" alt="" '
                'loading="lazy" decoding="async">' if i.get("img") else "")
        filas.append(f'<li>{foto}<div><a href="{esc(i["href"])}">{i["titulo"]}</a><small>{i["texto"]}</small></div></li>')
    linea = ""
    if enlaces:
        partes = " · ".join(f'<a href="{esc(h)}">{t}</a>' for t, h in enlaces)
        linea = f'<p class="vt-promesa vt-mt">También: {partes}.</p>'
    return f'<ul class="vt-otros">{"".join(filas)}</ul>{linea}'


# ---------- portada y cierre ----------
def portada(p, tipo, migas_items):
    """Como componentes.portada, con dos variantes: sin foto (tezontle y piedra bola no tenían foto de portada en main y
    no se agrega ninguna) y con foto apaisada (la de tierra negra mide 3:2; se muestra 3:2 y no recortada a 4:5)."""
    if p.get("foto") and p["foto"]["alto"] >= p["foto"]["ancho"]:
        return c.portada(p, tipo, migas_items)
    clases = ["vt-portada"] + (["vt-portada--compacta"] if p.get("compacta") else [])
    clases.append("vt-portada--apaisada" if p.get("foto") else "vt-portada--sinfoto")
    foto = f'<div class="vt-portada__foto">{c.figura(p["foto"], principal=True)}</div>' if p.get("foto") else ""
    return (f'<section class="{" ".join(clases)}" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(migas_items)}'
            f'<div class="vt-portada__grid"><div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1>'
            f'<p class="vt-lede">{p["lede"]}</p><div class="vt-portada__trato">{c.etiqueta(p["etiqueta"])}<div>'
            f'{c.fila_cta(p["mensaje"], tipo, "hero", hero=True)}<p class="vt-portada__tambien">{p["tambien"]}</p></div>'
            f'</div></div>{foto}</div>{c.cuadro_datos()}</div></section>')


def cierre(ci, mensaje, tipo):
    """CTA final (componentes.cierre) con, si main la tenía, su foto de fondo decorativa (alt="")."""
    html = c.cierre(ci["titulo"], ci["lede"], mensaje, tipo)
    f = ci.get("fondo")
    if not f:
        return html
    fondo = (f'<img class="vt-cierre__fondo" src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="" '
             'loading="lazy" decoding="async">')
    return html.replace('<section class="vt-cierre"', '<section class="vt-cierre vt-cierre--foto"', 1).replace(
        '<div class="vt-wrap vt-cierre__grid">', f'{fondo}<div class="vt-wrap vt-cierre__grid">', 1)


# ---------- pedido por correo (el formulario de main: mismos campos y destino, más honeypot y medición) ----------
ASUNTO = "Pedido desde sitio web - Viveros Terra"  # el de main: el dueño filtra sus correos por él


def formulario_pedido(prefijo, cta, ejemplo_detalle, aviso):
    """Formulario a formsubmit de viverosterra@hotmail.com con los campos de main (nombre, email, detalle), _next a
    /gracias, sin captcha y con honeypot _honey. vt-b2b.js lo valida junto a cada campo y manda generate_lead con method
    "formulario" y cta_id `cta`; sin JS, el navegador valida los required y se envía igual."""
    campos = (
        c._campo_correo(prefijo, "nombre", "Nombre", completar="name", placeholder="Tu nombre"),
        c._campo_correo(prefijo, "email", "Correo", "email", completar="email", placeholder="tu@correo.com"),
        c._campo_correo(prefijo, "detalle", "¿Qué necesitas?", requerido=False, multilinea=True,
                        placeholder=ejemplo_detalle),
    )
    return (
        f'<form class="vt-correo" id="order-form" action="{esc(c.FORMULARIO_ACCION)}" method="POST" data-vt-correo '
        f'data-cta-form="{esc(cta)}"><input type="hidden" name="_subject" value="{esc(ASUNTO)}">'
        f'<input type="hidden" name="_next" value="{esc(c.FORMULARIO_GRACIAS)}">'
        '<input type="hidden" name="_captcha" value="false">'
        '<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
        f'<div class="vt-correo__campos">{"".join(campos)}</div>'
        '<div class="vt-correo__pie"><button type="submit" class="vt-btn vt-btn--tinta">Enviar solicitud de pedido'
        '</button><p class="vt-correo__estado" role="status" data-vt-o="correo-estado"></p>'
        f'<p class="vt-correo__aviso">{aviso}</p></div></form>')
```

- [ ] **Step 3: El CSS**

Agrega al final de `public/css/terra.css`:

```css
/* ---------- materiales (Etapa 2f) ---------- */
/* Portada sin foto: tezontle y piedra bola no tienen foto de portada en main y no se agrega ninguna (regla del dueño). */
.vt-portada--sinfoto .vt-portada__grid{grid-template-columns:minmax(0,1fr)}
/* Cierre con la foto que main ponía detrás del CTA final: decorativa (alt=""), al 15 % (en main, del 15 al 20 %). */
.vt-cierre--foto{position:relative;isolation:isolate;overflow:hidden}
.vt-cierre__fondo{position:absolute;inset:0;z-index:-1;width:100%;height:100%;object-fit:cover;opacity:.15}
/* Otros materiales: miniatura de 48 px (las fotos de main miden de 194 a 821 px: no se agrandan), nombre y precios.
   Toda la tarjeta abre el enlace; el foco se marca en la tarjeta. */
.vt-otros{display:flex;flex-wrap:wrap;gap:12px;list-style:none}
.vt-otros li{position:relative;display:flex;align-items:center;gap:12px;min-height:64px;padding:8px 16px 8px 8px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-otros img{width:48px;height:48px;object-fit:cover}
.vt-otros a{color:var(--vt-ink);font-weight:700;text-decoration:none}
.vt-otros a::after{content:"";position:absolute;inset:0}
.vt-otros li:has(a:focus-visible){outline:2px solid var(--vt-field-deep);outline-offset:2px}
.vt-otros small{display:block;font-size:var(--vt-text-sm);color:var(--vt-muted)}
/* Portada con foto apaisada (tierra negra, 3:2): no se recorta a 4:5 en escritorio. */
.vt-portada--apaisada .vt-portada__foto .vt-fig__marco{aspect-ratio:3/2}
/* "Según cotización" en la tabla de presentaciones: más chico y en dos renglones si no cabe a 320 px. */
.vt-tabla__p--cotiza{font-size:17px;white-space:normal}
```

- [ ] **Step 4: En verde, build y presupuesto**

```bash
cd ~/dev/viverosterra-e2f
(cd tools/site && python3 -m unittest tests.test_componentes_materiales tests.test_terra_css 2>&1 | tail -1)
python3 tools/site/build.py | tail -2
(cd tools/site && python3 -c "
import activos, gzip
m = activos.minificar_css(open('../../public/css/terra.css').read()).encode(); print(len(m), len(gzip.compress(m, mtime=0)))")
git status --short | grep -v '\.html$'
```

Expected: `OK`; `plantillas: 37 de 37 páginas escritas` y el shell actualiza el resto de las 108 (el hash nuevo de `terra.css` va en el `<head>` de todas); `48489 9280` (menos de 49,152 y de 10,240); el `grep` lista `terra.css`, la copia con hash nueva y la que se rota, y `activos.json`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/componentes_materiales.py tools/site/tests/test_componentes_materiales.py tools/site/tests/test_terra_css.py public tools/site/activos.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): componentes (calculadora, presentaciones, otros, portada, cierre y pedido) y su CSS" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Plantilla `material` y `/tierra-negra-vegetal-tampico`

**Files:**
- Create: `tools/site/plantillas/material.py`, `tools/site/contenido/materiales_comun.py`, `tools/site/contenido/tierra_negra.py`, `tools/site/tests/test_material.py`
- Modify: `tools/site/generar.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_materiales_reglas.py` (`PENDIENTES`), `tools/servicios/pages.py`, `tools/servicios/tests/test_pagos.py`

- [ ] **Step 1: Prueba de la plantilla en rojo**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/tests/test_material.py <<'EOF'
"""Plantilla de material (Etapa 2f): orden del spec §3.3, un H1, scripts, JSON-LD con el producto ligado a #negocio y
FAQPage igual a lo visible. MIGRADAS crece con cada tarea de migración hasta tener las cuatro páginas."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402

MIGRADAS = {"/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html"}
ORDEN = ('id="vt-h1"', 'id="vt-h-precio"', 'id="vt-h-usos"', 'id="vt-h-calc"', 'id="vt-h-entrega"', 'id="vt-h-faq"',
         'id="vt-cierre-titulo"', 'id="vt-h-correo"')


def html_de(ruta):
    return (paginas.PUBLIC / MIGRADAS[ruta]).read_text(encoding="utf-8")


def grafo(html):
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]


class MaterialTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            posiciones = [html.find(marca) for marca in ORDEN]
            with self.subTest(ruta=ruta):
                self.assertNotIn(-1, posiciones)
                self.assertEqual(posiciones, sorted(posiciones))

    def test_un_h1_sin_css_viejo_y_con_sus_scripts(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(len(re.findall(r"<h1\b", html)), 1)
                for viejo in ("tailwind.css", "design-system.css", "servicios.css", "legacy-fixes", "fonts.googleapis"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<script src="/js/vt-materiales.js" defer></script>', html)
                self.assertIn('<script src="/js/vt-b2b.js" defer></script>', html)

    def test_producto_ligado_al_negocio_sin_existencias(self):
        for ruta in MIGRADAS:
            producto = next(n for n in grafo(html_de(ruta)) if n["@type"] == "Product")
            with self.subTest(ruta=ruta):
                self.assertNotIn("InStock", json.dumps(producto))
                if "offers" in producto:
                    self.assertEqual(producto["offers"]["seller"], {"@id": f"{datos.SITIO}/#negocio"})

    def test_faqpage_igual_a_lo_visible(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            faq = next(n for n in grafo(html) if n["@type"] == "FAQPage")
            visibles = [paridad.texto(s) for s in re.findall(r"<summary>(.*?)</summary>", paridad.principal(html), re.S)]
            with self.subTest(ruta=ruta):
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)


if __name__ == "__main__":
    unittest.main()
EOF
(cd tools/site && python3 -m unittest tests.test_material 2>&1 | tail -1)
```

Expected: `FAILED` (la página de main no tiene `id="vt-h-precio"` ni `vt-materiales.js`).

- [ ] **Step 2: La plantilla**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/plantillas/material.py <<'EOF'
"""Plantilla de material (spec §3.3): ruta visible → H1 con el precio por presentación en la etiqueta (costal / m³ /
camión, o "según cotización") y CTA con la plantilla de la página → qué es (con las fotos de main) → precio por
presentación → usos → calculadora de cantidad (la de main, como función pura) → entrega (recoger o a domicilio, costo
según la colonia, anticipo y factura) → secciones propias de la página (comparativa, combinaciones, instalación,
galería) → preguntas → otros materiales → CTA final (con la foto de fondo de main) → pedido por correo (el formulario de
main). El orden respeta el de las fotos de main (regla del dueño): por eso "qué es" va antes del precio y, en piedra
bola, los otros materiales van después del CTA final, como en main. Páginas: /tierra-negra-vegetal-tampico,
/tezontle-rojo-tampico, /marmol-blanco-tampico y /piedra-bola-rio-tampico (tools/site/contenido/)."""
import componentes as c
import componentes_materiales as cm
from plantillas import base

CONTEXTO = "https://schema.org"
# vt-b2b.js valida el formulario de pedido y manda su generate_lead (el mismo del formulario de empresas).
SCRIPTS = ("/js/vt-materiales.js", "/js/vt-b2b.js")


class _Numero:
    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return self.n


def _que_es(k, n):
    q = k["que_es"]
    cuerpo = "".join(f"<p>{x}</p>" for x in q["parrafos"])
    if q.get("subtitulo"):
        cuerpo = f'<h3>{q["subtitulo"]}</h3>' + cuerpo
    if q.get("puntos"):
        cuerpo += '<ul class="vt-checks vt-mt">' + "".join(f"<li>{x}</li>" for x in q["puntos"]) + "</ul>"
    if q.get("figuras"):
        cuerpo += c.obras(q["figuras"])
    return c.bloque(n(), "Qué es", "vt-h-que", q["titulo"], cuerpo, lede=q.get("lede"))


def _precio(k, n):
    p = k["precio"]
    cuerpo = cm.presentaciones(p["filas"], p["caption"])
    if p.get("figura"):
        cuerpo = f'<div class="vt-dos"><div>{c.figura(p["figura"])}</div><div>{cuerpo}</div></div>'
    if p.get("nota"):
        cuerpo += f'<p class="vt-promesa">{p["nota"]}</p>'
    for t in p.get("tablas", ()):
        cuerpo += f'<h3 class="vt-mt">{t["titulo"]}</h3>' + c.tabla_comparativa(t["columnas"], t["filas"], t["caption"])
    return c.bloque(n(), "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p.get("lede"), tinte=True,
                    id_seccion="precio")


def _usos(k, n):
    u = k["usos"]
    return c.bloque(n(), "Usos", "vt-h-usos", u["titulo"], c.fichas(u["items"]), lede=u.get("lede"))


def _calculadora(k, n):
    ca = k["calculadora"]
    cuerpo = cm.calculadora(k["prefijo"], k["tipo"], ca["clave"], k["portada"]["mensaje"], ca["nombre"])
    return c.bloque(n(), "Calculadora", "vt-h-calc", ca["titulo"], cuerpo, lede=ca["lede"], tinte=True,
                    id_seccion="calculadora")


def _entrega(k, n):
    e = k["entrega"]
    return c.bloque(n(), "Entrega", "vt-h-entrega", e["titulo"], c.fichas(e["items"]), lede=e.get("lede"),
                    id_seccion="entrega")


def _extra(k, n, clave):
    x = k[clave]
    if clave == "instalacion":
        cuerpo = c.pasos(x["pasos"]) + (f'<p class="vt-promesa">{x["nota"]}</p>' if x.get("nota") else "")
        return c.bloque(n(), "Instalación", "vt-h-instalacion", x["titulo"], cuerpo, lede=x.get("lede"))
    if clave == "galeria":
        return c.bloque(n(), "Fotos", "vt-h-galeria", x["titulo"], c.obras(x["figuras"]), lede=x.get("lede"))
    return c.bloque(n(), "Combinaciones", "vt-h-combina", x["titulo"], c.fichas(x["items"]), lede=x.get("lede"),
                    tinte=True)


def _otros(k, n):
    o = k["otros"]
    return c.bloque(n(), "Materiales", "vt-h-otros", o["titulo"], cm.otros(o["items"], o.get("enlaces", ())))


def _pedido(k, n):
    f = k["pedido"]
    form = cm.formulario_pedido(k["prefijo"], f"{k['tipo']}:formulario", f["ejemplo"], f["aviso"])
    return c.bloque(n(), "Por correo", "vt-h-correo", f["titulo"], form, lede=f["lede"], id_seccion="solicitar-pedido")


def render(k):
    tipo, n = k["tipo"], _Numero()
    secciones = [cm.portada(k["portada"], tipo, k["migas"])]
    if k.get("que_es"):
        secciones.append(_que_es(k, n))
    secciones += [_precio(k, n), _usos(k, n), _calculadora(k, n), _entrega(k, n)]
    secciones += [_extra(k, n, clave) for clave in ("combinaciones", "instalacion", "galeria") if k.get(clave)]
    f = k["faq"]
    secciones.append(c.bloque_dos(n(), "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    ci = k["cierre"]
    final = [cm.cierre(ci, k["portada"]["mensaje"], tipo)]
    otros = _otros(k, n)
    secciones += ([] if k["otros"].get("tras_cierre") else [otros]) + final + (
        [otros] if k["otros"].get("tras_cierre") else [])
    secciones.append(_pedido(k, n))
    j = k["jsonld"]
    grafo = [j["producto"], c.faq_jsonld(f["preguntas"]), j["migas"]]
    if k.get("instalacion") and k["instalacion"].get("howto"):
        grafo.append(c.howto(k["instalacion"]["howto"], [(p["titulo"], p["texto"]) for p in k["instalacion"]["pasos"]]))
    grafo.append({"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])})
    precargas = (base.precarga_imagen(k["portada"]["foto"]),) if k["portada"].get("foto") else ()
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=precargas, scripts=SCRIPTS)
EOF
```

- [ ] **Step 3: Lo común de los materiales**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/contenido/materiales_comun.py <<'EOF'
"""Lo que comparten las cuatro páginas de materiales (Etapa 2f): entrega, pedido por correo, otros materiales, migas,
producto del JSON-LD y motivos de paridad repetidos. Solo datos: la plantilla es tools/site/plantillas/material.py.

Precios solo de datos.PRECIOS (tierra negra $90 el costal y $1,500 el m³; tezontle desde $200 el costal); lo demás —
tierra preparada, camiones, m³ de tezontle, mármol y piedra bola— va "según cotización" (regla del dueño: no se inventa).
Sin plazos de entrega (no están en datos.py), sin existencias ni disponibilidad, sin "gratis"; el pago, con anticipo.
"""
import datos
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
SEGUN = datos.SEGUN_COTIZACION.lower()
TIPO = "material"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
CAMION = f"camión {SEGUN}"

RESUMEN = {
    "/tierra-negra-vegetal-tampico": (f"Costal {dinero(P['tierra_negra_costal'])} · m³ {dinero(P['tierra_negra_m3'])} · "
                                      f"{CAMION}"),
    "/tezontle-rojo-tampico": f"Costal desde {dinero(P['tezontle_costal'])} · m³ y camión de 14 m³ {SEGUN}",
    "/marmol-blanco-tampico": f"Saco de 20 kg {SEGUN} · 3 sacos por m²",
    "/piedra-bola-rio-tampico": f"Chica, mediana y grande · {SEGUN}",
}
NOMBRES = {
    "/tierra-negra-vegetal-tampico": "Tierra negra vegetal",
    "/tezontle-rojo-tampico": "Tezontle rojo",
    "/marmol-blanco-tampico": "Mármol blanco",
    "/piedra-bola-rio-tampico": "Piedra bola de río",
}
# Miniaturas que main ponía en "Otros materiales" (mármol y piedra bola): se quedan donde estaban, sin agrandarse.
MINIATURAS = {
    "/tezontle-rojo-tampico": {"src": "/img/tezontle-rojo-jardin-tampico-sendero.webp", "ancho": 194, "alto": 259},
    "/tierra-negra-vegetal-tampico": {"src": "/img/tierra-negra-camion-volteo-tampico.webp", "ancho": 821, "alto": 471},
}


def otros(ruta, orden, con_miniatura=False):
    """Los otros materiales en el orden de main, cada uno con su resumen de precios de datos.py."""
    return tuple({"titulo": NOMBRES[r], "href": r, "texto": RESUMEN[r],
                  **({"img": MINIATURAS[r]} if con_miniatura and r in MINIATURAS else {})}
                 for r in orden if r != ruta)


def entrega(material):
    """Recoger en el vivero o a domicilio, costo según la colonia, anticipo y factura. Sin plazo: no está en datos.py."""
    return {
        "titulo": f"¿Cómo te entregamos {material}?",
        "lede": "Lo recoges en el vivero o te lo llevamos. El costo de entrega va en la cotización, antes de que confirmes.",
        "items": (
            {"titulo": "Recoges en el vivero",
             "texto": f"En {datos.DOMICILIO_CORTO} ({datos.REFERENCIA}). {datos.HORARIO}."},
            {"titulo": "Te lo llevamos",
             "texto": (f"A Tampico, Ciudad Madero y Altamira; {datos.ZONAS_POR_PROYECTO}, por proyecto. El costo de "
                       "entrega se cotiza según tu colonia y el volumen.")},
            {"titulo": "Pago y factura", "texto": f"{datos.ANTICIPO} Emitimos factura {datos.FACTURA}."},
        ),
    }


def pedido(ejemplo):
    return {
        "titulo": "Escríbenos para cotizar",
        "lede": (f"Si prefieres el correo, mándanos tu pedido y te respondemos en horario de atención ({datos.HORARIO}). "
                 f'También puedes llamar al <a href="tel:{datos.TELEFONO_TEL}" data-cta="material:cuerpo">'
                 f"{datos.TELEFONO_VISIBLE}</a>."),
        "ejemplo": ejemplo,
        "aviso": 'Usamos tus datos solo para responder tu pedido. <a href="/politica-privacidad">Aviso de privacidad</a>.',
    }


def migas(ruta, nombre):
    """Migas visibles y su BreadcrumbList: Inicio › el material (como publicaba main)."""
    visibles = (("Inicio", "/"), (nombre, None))
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": nombre, "item": f"{SITE}{ruta}"}]}
    return visibles, ld


def producto(nombre, descripcion, imagen, sku=None, ofertas=None):
    """Product del JSON-LD con la marca de main; las ofertas solo con precios de datos.py y sin "InStock"."""
    nodo = {"@type": "Product", "name": nombre, "description": descripcion,
            "brand": {"@type": "Brand", "name": datos.NOMBRE}, "image": imagen}
    if sku:
        nodo["sku"] = sku
    if ofertas:
        nodo["offers"] = {**ofertas, "priceCurrency": "MXN", "seller": NEGOCIO}
    return nodo


SPEAKABLE = ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq summary")

# Motivos de paridad que se repiten en las cuatro páginas.
MOTIVO_PRECIO = ("No está en datos.PRECIOS: regla del dueño, va “según cotización” y nunca se inventa (pregunta al "
                 "dueño en el plan 2f).")
MOTIVO_LOCALBUSINESS = ("El seller del Product apunta por @id a la entidad única #negocio (el nodo completo vive en la "
                        "home), en vez de un LocalBusiness suelto, como en 2d y 2e.")
MOTIVO_AUTOR = ("Bloque de autor con “+18 años” y “Productor directo” (sin respaldo en datos.py); la entidad y el autor "
                "son de la Etapa 4.")
MOTIVO_TESTIMONIOS = ("Opiniones sin permiso del dueño: no están en datos.OPINIONES (spec: nunca una opinión sin "
                      "confirmarla). Vuelven si el dueño las confirma.")
EOF
```

- [ ] **Step 4: El contenido de tierra negra**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/contenido/tierra_negra.py <<'EOF'
"""Contenido de /tierra-negra-vegetal-tampico (tierra negra vegetal por costal, m³ o camión). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularTierra) como función pura.

Precios de datos.PRECIOS: costal $90 y m³ $1,500. La tierra preparada ($100), el camión ("desde $5,000") y los camiones de
5, 8 y 14 m³ ($3,500, $5,200, $8,000) no están en datos.py: van "según cotización" (preguntas al dueño). Las 8 fotos de
main, en su orden. Sin “Entrega inmediata”, “+500 jardines”, “40% más rápido” ni “gratis”; las opiniones de Ricardo O.
y Laura P. no tienen permiso del dueño y se retiran. Título, robots y canonical como estaban; la descripción y el Open
Graph pierden los precios que no están en datos.py y el “gratis” (PARIDAD["meta"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/tierra-negra-vegetal-tampico"
URL = f"{SITE}{RUTA}"
COSTAL, M3 = dinero(P["tierra_negra_costal"]), dinero(P["tierra_negra_m3"])
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Tierra negra vegetal")
DESCRIPCION = (f"Tierra negra vegetal en Tampico. Costal {COSTAL} · m³ {M3} · camión volteo según cotización. Entrega a "
               "domicilio en Madero y Altamira. Cotiza por WhatsApp.")
DESCRIPCION_OG = (f"Tierra negra vegetal para jardín y pasto en Tampico. Costal {COSTAL}, m³ {M3} y camión volteo según "
                  "cotización. Cotiza por WhatsApp.")

META = {
    "title": "Tierra Negra Vegetal Tampico · Costal y Camión Volteo",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Tierra Negra Vegetal Tampico · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/camion-tierra-negra-entrega-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}


def _figura(src, ancho, alto, numero, alt, lugar, etapa):
    return {"src": src, "ancho": ancho, "alto": alto, "numero": numero, "alt": alt, "lugar": lugar, "etapa": etapa}


PORTADA_FOTO = {
    "src": "/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp",
    "srcset": ("/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp 560w, "
               "/img/portadas/camion-tierra-negra-entrega-tampico.webp 960w"),
    "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 960, "alto": 640, "numero": 1,
    "alt": "Camión de Viveros Terra entregando tierra negra en Tampico", "lugar": "Entrega de tierra negra",
    "etapa": "Tampico"}
FIGURAS_QUE_ES = (
    _figura("/img/tierra-negra-preparacion-pasto-tampico.webp", 1400, 787, 2,
            "Tierra negra vegetal extendida para instalar pasto en un jardín de Tampico", "Base para pasto", "Preparación"),
    _figura("/img/tierra-negra-camion-volteo-tampico.webp", 821, 471, 3,
            "Entrega de tierra negra en camión volteo en Tampico", "Camión volteo", "Entrega a granel"),
    _figura("/img/tierra-negra-suministro-jardin-tampico.webp", 1400, 787, 4,
            "Tierra negra con materia orgánica para jardines en Tampico", "Tierra negra", "En el jardín"),
)
FIGURAS_GALERIA = (
    _figura("/img/camion-tierra-negra-descarga-tampico.webp", 1053, 1018, 5,
            "Camión de Viveros Terra descargando tierra negra en una obra de jardinería en Tampico", "Descarga en obra",
            "Camión volteo"),
    _figura("/img/tierra-negra-vegetal-costales-tampico.webp", 1400, 933, 6,
            "Costales de tierra negra vegetal de Viveros Terra", "Costales", "Por costal"),
    _figura("/img/tierra-negra-sacos-viveros-terra.webp", 1400, 933, 7, "Tierra negra vegetal en sacos para jardín",
            "Sacos de tierra negra", "Por costal"),
)

USOS = (
    {"titulo": "Preparación para pasto en rollo",
     "texto": ("Una capa de 5 a 10 cm de tierra negra antes de instalar pasto San Agustín: el pasto arraiga parejo y el "
               "suelo no se compacta."),
     "puntos": ("Referencia: 1 m³ por cada 10 a 20 m²",)},
    {"titulo": "Cajetes para árboles y palmas",
     "texto": ("Relleno de cajete con tierra negra para ayudar al arraigo de árboles ornamentales, palmas tropicales y "
               "arbustos recién plantados."),
     "puntos": ("Referencia: 0.1 a 0.3 m³ por árbol",)},
    {"titulo": "Mejora de jardines existentes",
     "texto": ("Aplicación superficial de 3 a 5 cm sobre jardines con suelo pobre o compacto: mejora el color del pasto y "
               "la salud de las plantas sin remover el jardín."),
     "puntos": ("Referencia: 1 m³ por cada 20 a 30 m²",)},
    {"titulo": "Nivelación de terrenos",
     "texto": ("Relleno y nivelación de terrenos irregulares antes de jardines, fraccionamientos u obras, en camiones "
               "volteo coordinados por etapas."),
     "puntos": ("Camiones de 5, 8 y 14 m³",)},
    {"titulo": "Macetas y jardineras grandes",
     "texto": ("Sustrato base para macetones y jardineras: se mezcla con perlita o arena gruesa 70/30 para que drene y no "
               "se encharque."),
     "puntos": ("Por costal",)},
    {"titulo": "Proyectos comerciales e industriales",
     "texto": ("Áreas verdes en fraccionamientos, condominios, parques industriales y escuelas: camiones coordinados por "
               f"etapas con factura {datos.FACTURA}."),
     "puntos": (f"Por camión, {mc.SEGUN}",)},
)

PREGUNTAS = (
    ("¿Cuánto cuesta un camión de tierra negra en Tampico?",
     f"El camión volteo de tierra negra se cotiza según el volumen y la distancia de entrega: escríbenos tu colonia y la "
     f"cantidad y te mandamos el precio por escrito antes de que confirmes. A granel por m³ cuesta {M3} y el costal "
     f"(≈ 20 kg), {COSTAL}."),
    ("¿Para qué sirve la tierra negra vegetal?",
     "Para preparar terrenos antes de instalar pasto en rollo, rellenar cajetes de árboles y palmas, mejorar el suelo "
     "arcilloso de Tampico, nivelar terrenos y como sustrato base en macetas grandes. Aporta materia orgánica, retiene "
     "humedad y mejora la textura del suelo para que las raíces penetren mejor."),
    ("¿Cuánta tierra negra necesito para mi jardín?",
     f"m² del área × grosor de la capa en metros = m³. Por ejemplo, para 100 m² con capa de 8 cm necesitas "
     f"{ejemplo('tierra-negra', 100, 0.08)}. Para preparar pasto se recomiendan de 5 a 10 cm; para cajetes de árboles, "
     "de 0.1 a 0.3 m³ por árbol. Usa la calculadora de esta página o mándanos tus medidas por WhatsApp."),
    ("¿Qué diferencia hay entre tierra negra y tierra común de Tampico?",
     "La tierra arcillosa de Tampico es compacta, pobre en nutrientes y drena mal: cuando llueve se encharca y cuando se "
     "seca se endurece. La tierra negra vegetal tiene más materia orgánica, una textura suelta que deja crecer las raíces "
     "y retiene la humedad que necesitan las plantas."),
    ("¿El pasto arraiga mejor con tierra negra?",
     f"Sí. El pasto San Agustín sobre una capa de 8 cm de tierra negra arraiga más parejo que sobre suelo arcilloso: las "
     f"raíces encuentran suelo suelto y nutrido durante sus {datos.ARRAIGO} de arraigo y el riesgo de que se levante "
     "baja mucho."),
    ("¿Entregan tierra negra a domicilio en toda la zona de Tampico?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto, en camión "
     "volteo con descarga en tu domicilio u obra. Para accesos restringidos coordinamos el horario y la forma de "
     "descarga. El costo de entrega va en la cotización según la distancia."),
    ("¿Se puede usar tierra negra para macetas y jardineras?",
     "Sí, mezclada con perlita o arena gruesa en proporción 70/30: la tierra negra pura en maceta se compacta con el "
     "riego frecuente y se encharca. La mezcla aporta los nutrientes de la tierra negra y el drenaje de la perlita."),
    ("¿Dan factura CFDI por la tierra negra?",
     f"Sí. Emitimos factura {datos.FACTURA}, sobre todo en proyectos comerciales, fraccionamientos y empresas. Pídela al "
     "cotizar con tu RFC y datos fiscales."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-tierra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Tierra negra vegetal <em>por costal o camión</em>",
        "lede": (f"En Viveros Terra la tierra negra vegetal cuesta {COSTAL} el costal y {M3} el m³ a granel; el camión "
                 "volteo se cotiza según el volumen y tu colonia. Para pasto, jardineras y siembra: recoges en el vivero "
                 "o te la llevamos en Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Tierra negra", "aviso": f"Precios {datos.ANIO}", "nombre": "Costal ≈ 20 kg", "antes": "",
                     "monto": COSTAL, "unidad": "por costal",
                     "filas": (("Por m³ a granel", M3), ("Camión volteo", datos.SEGUN_COTIZACION)),
                     "nota": "La entrega se cotiza según tu colonia."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuánta necesitas</a>.',
        "foto": PORTADA_FOTO,
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Por qué el suelo de Tampico necesita tierra negra?",
        "parrafos": (
            ("El suelo natural de Tamaulipas es arcilloso y compacto: retiene agua de más en lluvias y se seca como "
             "piedra en la temporada seca. Las raíces no penetran, el pasto no arraiga y las plantas no crecen."),
            ("La tierra negra vegetal es un sustrato orgánico rico en humus, de materia vegetal descompuesta: airea el "
             "suelo, retiene humedad sin encharcar y aporta los nutrientes básicos que le faltan a la tierra de Tampico."),
        ),
        "puntos": ("Alta materia orgánica: nutrientes naturales", "Retiene humedad: menos riegos",
                   "Textura suelta: las raíces crecen sin obstáculos", "Por costal o en camión volteo"),
        "figuras": FIGURAS_QUE_ES,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta la tierra negra en Tampico?",
        "lede": f"Precios {datos.ANIO}. Lo que no tiene precio publicado se cotiza por escrito antes de que confirmes.",
        "caption": "Tierra negra vegetal por presentación",
        "filas": (
            {"nombre": "Costal de tierra negra", "detalle": "≈ 20 kg · recoger o a domicilio, sin mínimo",
             "unidad": "costal", "precio": P["tierra_negra_costal"]},
            {"nombre": "Tierra negra preparada", "detalle": "Costal ≈ 20 kg con hojarasca y abono, para macetas",
             "unidad": "costal", "precio": None},
            {"nombre": "A granel por m³", "detalle": "Desde 1 m³, entregada en tu domicilio", "unidad": "m³",
             "precio": P["tierra_negra_m3"]},
            {"nombre": "Camión volteo", "detalle": "8 m³ o más, por etapas y con factura", "unidad": "camión",
             "precio": None},
        ),
        "nota": "El costo de entrega se cotiza según tu colonia y el volumen.",
    },
    "usos": {"titulo": "¿Para qué usas la tierra negra?",
             "lede": "Cada uso tiene su capa y su cantidad de referencia.", "items": USOS},
    "calculadora": {"clave": "tierra-negra", "nombre": "tierra negra", "titulo": "¿Cuánta tierra negra necesitas?",
                    "lede": "Escribe el área y el grosor de la capa: te damos los m³, la presentación y los costales."},
    "entrega": mc.entrega("la tierra negra"),
    "galeria": {"titulo": "Así luce la tierra negra de Viveros Terra", "figuras": FIGURAS_GALERIA},
    "faq": {"titulo": "Todo sobre tierra negra en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales para tu jardín",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico")),
              "enlaces": (("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Plantas y palmas", "/plantas-palmas-arboles-tampico"),
                          ("Arma tu lista de plantas", "/catalogo"), ("Guía de jardines", "/blog/diseno-jardines-tampico-guia"))},
    "cierre": {"titulo": "Cotiza tu tierra negra",
               "lede": "Dinos la cantidad y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/camion-tierra-negra-entrega-tampico.webp", "ancho": 1400, "alto": 933}},
    "pedido": mc.pedido("Ejemplo: 3 m³ de tierra negra, entrega en Ciudad Madero"),
    "jsonld": {
        "producto": mc.producto(
            "Tierra Negra Vegetal en Tampico",
            ("Tierra negra vegetal orgánica para jardines, pasto en rollo y plantas en Tampico. Venta por costal, por m³ y "
             "en camión volteo con entrega a domicilio en Ciudad Madero y Altamira."),
            f"{SITE}/img/camion-tierra-negra-entrega-tampico.jpg",
            ofertas={"@type": "AggregateOffer", "lowPrice": str(P["tierra_negra_costal"]),
                     "highPrice": str(P["tierra_negra_m3"])}),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {
        "description": (DESCRIPCION, "Sin la tierra preparada a $100 ni el camión desde $5,000 (no están en datos.py) y "
                                     "sin “gratis” (regla del dueño)."),
        "og:description": (DESCRIPCION_OG, "Sin la tierra preparada a $100 ni el camión desde $5,000 (no están en "
                                           "datos.py) y sin “gratis” (regla del dueño)."),
    },
    "reemplazos": {
        "Elige el formato para tu proyecto": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Costales de tierra negra": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Tierra Negra Preparada": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Por m³": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Camión volteo": "¿Cuánto cuesta la tierra negra en Tampico?",
        "¿Cuánta tierra negra necesito para preparar mi jardín?": "¿Cuánta tierra negra necesito para mi jardín?",
        "¿Entregan tierra negra a domicilio en Tampico?": "¿Entregan tierra negra a domicilio en toda la zona de Tampico?",
    },
    "retirados": {
        "Lo que dicen nuestros clientes": mc.MOTIVO_TESTIMONIOS,
        "$100": mc.MOTIVO_PRECIO,
        "$3,500": mc.MOTIVO_PRECIO,
        "$5,000": mc.MOTIVO_PRECIO,
        "$5,200": mc.MOTIVO_PRECIO,
        "$8,000": mc.MOTIVO_PRECIO,
    },
    "jsonld": {"LocalBusiness": mc.MOTIVO_LOCALBUSINESS},
}
EOF
```

- [ ] **Step 5: Registrar la página**

`tools/site/generar.py`, después de `("/catalogo", "catalogo.html", "catalogo", "catalogo"),`:

```python
    ("/tierra-negra-vegetal-tampico", "tierra-negra-vegetal-tampico/index.html", "material", "tierra_negra"),
```

`tools/site/tests/test_generar.py`, en `esperadas`, después de `"/catalogo",`: `"/tierra-negra-vegetal-tampico",` (las Tareas 8–10 agregan las otras tres en el mismo orden).

`tools/site/tests/test_materiales_reglas.py`: `PENDIENTES = frozenset({"/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico"})`.

`tools/servicios/pages.py`: borra la entrada `"tierra-negra-vegetal-tampico": dict(…),`. `tools/servicios/tests/test_pagos.py`: agrega `"tierra-negra-vegetal-tampico"` a `CON_PLANTILLA` y "2f" al docstring ("(Etapas 2a, 2c, 2d, 2e y 2f)").

- [ ] **Step 6: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /tierra-negra-vegetal-tampico
(cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia tests.test_corregir_datos 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
grep -cE "tailwind.css|design-system.css|servicios.css|fonts.googleapis|window.open" public/tierra-negra-vegetal-tampico/index.html
```

Expected: `plantillas: 1 de 38 páginas escritas`; `ok` en las seis categorías; `OK`; `OK`; `0`. (`corregir_datos.py` ya no toca la página: `con_plantilla()` la excluye por estar en `generar.PAGINAS`.)

- [ ] **Step 7: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/plantillas/material.py tools/site/contenido/materiales_comun.py tools/site/contenido/tierra_negra.py \
  tools/site/tests/test_material.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_materiales_reglas.py \
  tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/tierra-negra-vegetal-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): plantilla material y tierra negra con calculadora de main, precios de datos.py y sus 8 fotos" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: `/tezontle-rojo-tampico`

**Files:**
- Create: `tools/site/contenido/tezontle_rojo.py`
- Modify: `tools/site/generar.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_material.py` (`MIGRADAS`), `tools/site/tests/test_materiales_reglas.py` (`PENDIENTES`), `tools/servicios/pages.py`, `tools/servicios/tests/test_pagos.py`

- [ ] **Step 1: Agregarla a las pruebas (rojo)**

`test_material.MIGRADAS`: agrega `"/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",`. `test_materiales_reglas.PENDIENTES = frozenset({"/marmol-blanco-tampico", "/piedra-bola-rio-tampico"})`.

Run: `cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas 2>&1 | tail -1`
Expected: `FAILED`.

- [ ] **Step 2: El contenido**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/contenido/tezontle_rojo.py <<'EOF'
"""Contenido de /tezontle-rojo-tampico (tezontle rojo por costal, m³ o camión de 14 m³). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularTezontle) como función pura.

Precio de datos.PRECIOS: costal desde $200 (como en la home). El m³ ($3,200) y el camión de 14 m³ no están en datos.py:
"según cotización". La comparativa pierde el mármol a $350 y la piedra a $280 (no están en datos.py). Sin “+300
jardines”, “3–5 años sin reposición”, “90% de la maleza”, “del 60% al 95%”, “imbatible” ni “gratis”. Sin foto de
portada (main no la tenía); sus 4 fotos, en su orden. Meta como estaba publicada.
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/tezontle-rojo-tampico"
URL = f"{SITE}{RUTA}"
COSTAL = dinero(P["tezontle_costal"])
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Tezontle rojo")

META = {
    "title": "Tezontle Rojo Tampico · Control de Maleza y Decoración",
    "description": ("Tezontle rojo en Tampico. Costal desde $200 · Por m³ · Camión volteo 14 m³. Control de maleza y "
                    "decoración duradera. Entrega a domicilio. Cotiza hoy."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Tezontle Rojo Tampico · Control de Maleza y Decoración"),
        ("og:description", ("Tezontle rojo volcánico en Tampico. Costal, m³ y camión volteo 14 m³ con entrega a "
                            "domicilio. El rojo perfecto para tu jardín.")),
        ("og:image", f"{SITE}/img/tezontle-rojo-jardin-tampico-sendero.webp"),
        ("og:locale", "es_MX"),
    ),
}
FIGURAS = (
    {"src": "/img/tezontle-rojo-jardin-tampico-sendero.webp", "ancho": 194, "alto": 259, "numero": 1,
     "alt": "Jardín residencial con tezontle rojo y pasto en Tampico", "lugar": "Tezontle y pasto", "etapa": "Jardín"},
    {"src": "/img/tezontle-rojo-jardin-lateral-tampico.webp", "ancho": 259, "alto": 194, "numero": 2,
     "alt": "Sendero lateral de tezontle rojo en un jardín de Tampico", "lugar": "Sendero lateral", "etapa": "Jardín"},
    {"src": "/img/tezontle-rojo-bordillo-jardin-tampico.webp", "ancho": 259, "alto": 195, "numero": 3,
     "alt": "Tezontle rojo con bordillo decorativo en un jardín residencial de Tampico", "lugar": "Con bordillo",
     "etapa": "Arriate"},
)
USOS = (
    {"titulo": "Control de maleza", "texto": "Capa de 6 a 8 cm sobre membrana antigerminante: ayuda a controlar la "
     "maleza sin herbicidas.", "puntos": ("5 a 8 cm de capa",)},
    {"titulo": "Senderos y caminos", "texto": "Caminos decorativos dentro del jardín: permeables, firmes y de aspecto "
     "tropical.", "puntos": ("8 a 10 cm compactado",)},
    {"titulo": "Arriates de plantas", "texto": "Cubierta roja alrededor de arbustos y plantas ornamentales: contrasta con "
     "el verde.", "puntos": ("5 a 6 cm de capa",)},
    {"titulo": "Cajetes de árboles y palmas", "texto": "Protege las raíces superficiales, conserva la humedad y da un "
     "acabado cuidado alrededor del tronco.", "puntos": ("5 a 8 cm, 50 cm de radio",)},
    {"titulo": "Drenaje en suelo arcilloso", "texto": "Mezclado con la tierra de relleno mejora el drenaje en jardines con "
     "suelo compacto y ayuda contra los encharcamientos.", "puntos": ("Mezcla 50/50 con tierra",)},
    {"titulo": "Terrazas y azoteas", "texto": "Cubierta sobre membrana impermeable: jardín seco de bajo mantenimiento "
     "para azoteas en Tampico.", "puntos": ("6 a 8 cm sobre membrana",)},
    {"titulo": "Macetas y jardineras", "texto": "Capa superior decorativa en macetones: reduce la evaporación y evita "
     "salpicaduras al regar.", "puntos": ("3 a 4 cm en superficie",)},
    {"titulo": "Proyectos de paisajismo", "texto": "Hoteles, fraccionamientos y empresas lo usan en áreas verdes de bajo "
     "mantenimiento, por camión volteo.", "puntos": ("Camión volteo 14 m³",)},
)
COMBINACIONES = (
    {"titulo": "Tezontle + Pasto verde", "texto": ("El contraste clásico en Tampico: el rojo del tezontle y el verde del "
     'San Agustín. <a href="/pasto-en-rollo-tampico">Ver pasto en rollo</a>.')},
    {"titulo": "Tezontle + Mármol blanco", "texto": ("Mármol blanco en arriates y tezontle en senderos: un jardín "
     'contemporáneo para residencias y corporativos. <a href="/marmol-blanco-tampico">Ver mármol blanco</a>.')},
    {"titulo": "Tezontle + Palmas tropicales", "texto": ("Alrededor de palmas y árboles protege las raíces y conserva la "
     'humedad. <a href="/palmas-tropicales-tampico">Ver palmas tropicales</a>.')},
    {"titulo": "Tezontle + Tierra negra", "texto": ("Primero se prepara el terreno con tierra negra y después va el "
     'tezontle encima, para jardines nuevos. <a href="/tierra-negra-vegetal-tampico">Ver tierra negra</a>.')},
    {"titulo": "Tezontle + Piedra bola de río", "texto": ("Para jardines zen o de estilo japonés: el tezontle de relleno y "
     'la piedra bola de borde. <a href="/piedra-bola-rio-tampico">Ver piedra bola</a>.')},
    {"titulo": "Tezontle + Riego automático", "texto": ("El goteo bajo el tezontle queda oculto y el tezontle retiene la "
     'humedad en la temporada seca. <a href="/sistema-riego-tampico">Ver sistema de riego</a>.')},
)
PASOS = (
    {"titulo": "Limpia el área", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira la maleza con todo y raíz y nivela el suelo si hace falta."},
    {"titulo": "Coloca la membrana", "quien": "tu", "cuando": "Paso 2",
     "texto": "Membrana antigerminante sin huecos, con los bordes fijos con piedras o grapas."},
    {"titulo": "Vierte el tezontle", "quien": "tu", "cuando": "Paso 3",
     "texto": "Distribúyelo con rastrillo hasta el grosor que elegiste (5 a 10 cm)."},
    {"titulo": "Define los bordes", "quien": "tu", "cuando": "Paso 4",
     "texto": "Bordillo de piedra, ladrillo o metal para contener el tezontle y separar zonas."},
)
PREGUNTAS = (
    ("¿Cuánto cuesta el tezontle rojo por camión en Tampico?",
     f"El costal de tezontle rojo cuesta desde {COSTAL}. El m³ suelto y el camión volteo de 14 m³ se cotizan según el "
     "volumen y la distancia de entrega: escríbenos tu colonia y la cantidad y te mandamos el precio por escrito antes "
     "de que confirmes."),
    ("¿Para qué sirve el tezontle en un jardín?",
     "Para ayudar a controlar la maleza sin herbicidas, hacer senderos y caminos decorativos, cubrir arriates, mejorar el "
     "drenaje en suelos arcillosos y como acabado decorativo que contrasta con el verde del pasto y las plantas."),
    ("¿Cuántos centímetros de tezontle se ponen?",
     "De 5 a 8 cm para control de maleza y arriates; de 8 a 10 cm compactados para senderos; de 3 a 4 cm como capa en "
     "macetas y jardineras. Sobre membrana antigerminante funciona mejor contra la maleza."),
    ("¿Cuánto dura el tezontle en un jardín?",
     "Es roca volcánica: no se desintegra ni se va con las lluvias de Tampico. Solo requiere rastrillarlo de vez en "
     "cuando para renivelarlo si se desplaza."),
    ("¿El tezontle daña a las plantas?",
     "No: bien colocado conserva la humedad del suelo, baja la temperatura de la tierra en días de calor y protege las "
     "raíces superficiales. Deja de 5 a 10 cm libres alrededor del tallo de las plantas sensibles."),
    ("¿Cuánta cantidad necesito para 50 m²?",
     f"Para 50 m² con capa de 8 cm necesitas {ejemplo('tezontle', 50, 0.08)}; con 6 cm, "
     f"{ejemplo('tezontle', 50, 0.06)}; con 10 cm para sendero, {ejemplo('tezontle', 50, 0.10)}. La fórmula: m² × "
     "grosor en metros = m³. Usa la calculadora de esta página o mándanos tus medidas."),
    ("¿Entregan tezontle a domicilio en Tampico y Altamira?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto: por costal en "
     "vehículo de reparto para cantidades chicas y en camión volteo de 14 m³ para proyectos grandes. El costo de entrega "
     "va en la cotización según tu dirección."),
    ("¿Es necesaria la membrana antigerminante con el tezontle?",
     "Para control de maleza, sí: sin membrana el tezontle ayuda, pero las semillas que caen desde arriba pueden germinar "
     "entre las piedras. Para uso decorativo o senderos de mucho tránsito no es indispensable. Te orientamos sobre la "
     "membrana para tu proyecto."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-tezontle",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Tezontle rojo <em>por costal, m³ o camión</em>",
        "lede": (f"En Viveros Terra el tezontle rojo cuesta desde {COSTAL} el costal; el m³ y el camión de 14 m³ se "
                 "cotizan según el volumen y tu colonia. Para drenaje, senderos y control de maleza, con factura."),
        "etiqueta": {"codigo": "Tezontle rojo", "aviso": f"Precios {datos.ANIO}", "nombre": "Costal", "antes": "desde",
                     "monto": COSTAL, "unidad": "por costal",
                     "filas": (("Por m³", SEGUN), ("Camión volteo 14 m³", SEGUN)),
                     "nota": f"Factura {datos.FACTURA}. La entrega se cotiza según tu colonia."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuánto necesitas</a>.',
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Por qué el tezontle funciona tan bien en Tampico?",
        "subtitulo": "Tezontle rojo para senderos, bordillos y arriates",
        "parrafos": (
            ("El tezontle rojo es una roca volcánica porosa del centro de México que se usa en los jardines de Tampico "
             "para contrastar con el verde del pasto. Aguanta la intemperie y deja drenar el agua."),
            ("Sus pequeñas cavidades dejan pasar el agua pero no la luz, y eso frena a las semillas de maleza. Con el calor "
             "de Tampico, que reseca otros materiales, y las lluvias de temporada, que arrastran los sustratos finos, el "
             "tezontle no se degrada ni se va."),
        ),
        "puntos": ("Ayuda contra la maleza: tapa la luz al suelo", "Mejora el drenaje: es poroso",
                   "Conserva su color con sol y lluvia", "Acolchado: conserva la humedad del suelo"),
        "figuras": FIGURAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "lede": f"Precios {datos.ANIO}. Lo que no tiene precio publicado se cotiza por escrito antes de que confirmes.",
        "caption": "Tezontle rojo por presentación",
        "filas": (
            {"nombre": "Por costal", "detalle": "Sin mínimo · recoger o a domicilio", "unidad": "costal",
             "precio": P["tezontle_costal"], "desde": True},
            {"nombre": "Por m³ suelto", "detalle": "A partir de 1 m³, entregado en tu domicilio", "unidad": "m³",
             "precio": None},
            {"nombre": "Camión volteo de 14 m³", "detalle": "Descarga en tu domicilio u obra, con factura",
             "unidad": "camión", "precio": None},
        ),
        "nota": "El costo de entrega se cotiza según tu colonia y el volumen.",
        "tablas": ({
            "titulo": "Tezontle, mármol blanco o piedra de río",
            "caption": "Tres materiales decorativos para senderos, bordes y arriates",
            "columnas": ("Característica", "Tezontle rojo", "Mármol blanco", "Piedra de río"),
            "filas": (("Color", "Rojo terracota", "Blanco", "Gris o beige natural"),
                      ("Origen", "Roca volcánica", "Mármol triturado", "Piedra de río"),
                      ("Tamaño", "2 a 5 cm", "1 a 3 cm", "5 a 15 cm"),
                      ("Drenaje", "Excelente (poroso)", "Bueno", "Excelente"),
                      ("Estilo", "Rústico, mexicano", "Minimalista", "Natural, zen"),
                      ("Precio por costal", f"desde {COSTAL}", SEGUN, SEGUN),
                      ("Mejor uso", "Bordes y arriates", "Senderos formales", "Estanques y decoración")),
        },),
    },
    "usos": {"titulo": "¿Para qué quieres el tezontle?",
             "lede": "Cada uso tiene su capa y su cantidad de referencia.", "items": USOS},
    "calculadora": {"clave": "tezontle", "nombre": "tezontle", "titulo": "¿Cuánto tezontle necesitas?",
                    "lede": "Escribe el área y para qué lo usas: te damos los m³, la presentación y los costales."},
    "entrega": mc.entrega("el tezontle"),
    "combinaciones": {"titulo": "El tezontle combina perfectamente con...", "items": COMBINACIONES},
    "instalacion": {"titulo": "Cómo instalar tezontle en 4 pasos", "pasos": PASOS},
    "faq": {"titulo": "Todo sobre tezontle en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales para tu jardín",
              "items": mc.otros(RUTA, ("/tierra-negra-vegetal-tampico", "/marmol-blanco-tampico",
                                       "/piedra-bola-rio-tampico")),
              "enlaces": (("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Plantas y palmas", "/plantas-palmas-arboles-tampico"),
                          ("Arma tu lista de plantas", "/catalogo"), ("Guía del tezontle", "/blog/tezontle-usos-jardin-tampico"))},
    "cierre": {"titulo": "Cotiza tu tezontle rojo",
               "lede": "Dinos la cantidad y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/tezontle-rojo-bordillo-jardin-tampico.webp", "ancho": 259, "alto": 195}},
    "pedido": mc.pedido("Ejemplo: 4 m³ de tezontle rojo, entrega en Altamira"),
    "jsonld": {
        "producto": mc.producto(
            "Tezontle Rojo Decorativo para Jardín Tampico",
            (f"Tezontle rojo volcánico decorativo para jardines en Tampico. Costal desde {COSTAL}. Uso en senderos, "
             "bordes, arriates y macetas. Entrega a domicilio en Tampico, Madero y Altamira."),
            f"{SITE}/img/tezontle-rojo-jardin-tampico-sendero.jpg", sku="VT-TEZ-001",
            ofertas={"@type": "Offer", "price": str(P["tezontle_costal"]), "url": f"{URL}#solicitar-pedido"}),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "reemplazos": {
        "Elige el formato para tu proyecto": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Por costal": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Por m³ suelto": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Camión 14 m³": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "¿Para qué sirve el tezontle en jardinería?": "¿Para qué sirve el tezontle en un jardín?",
        "¿Cuántos centímetros de tezontle se ponen en un jardín?": "¿Cuántos centímetros de tezontle se ponen?",
        "¿El tezontle dura mucho tiempo en el jardín?": "¿Cuánto dura el tezontle en un jardín?",
    },
    "retirados": {
        "Viveros Terra · Tampico": mc.MOTIVO_AUTOR,
        "$280": mc.MOTIVO_PRECIO,
        "$3,200": mc.MOTIVO_PRECIO,
        "$350": mc.MOTIVO_PRECIO,
    },
    "jsonld": {"LocalBusiness": mc.MOTIVO_LOCALBUSINESS},
}
EOF
```

- [ ] **Step 3: Registrar, build, paridad y pruebas**

`generar.py`: después de la fila de tierra negra, `("/tezontle-rojo-tampico", "tezontle-rojo-tampico/index.html", "material", "tezontle_rojo"),`; `test_generar.esperadas`: `"/tezontle-rojo-tampico",` después de tierra negra. `tools/servicios/pages.py`: borra `"tezontle-rojo-tampico": dict(…),`; `test_pagos.CON_PLANTILLA`: agrega `"tezontle-rojo-tampico"`.

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /tezontle-rojo-tampico
(cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
```

Expected: `plantillas: 1 de 39 páginas escritas`; `ok` en las seis; `OK`; `OK`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/contenido/tezontle_rojo.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_material.py \
  tools/site/tests/test_materiales_reglas.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/tezontle-rojo-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): tezontle rojo con calculadora de main, costal desde \$200 y m³ y camión según cotización" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: `/marmol-blanco-tampico`

**Files:**
- Create: `tools/site/contenido/marmol_blanco.py`
- Modify: los mismos seis de la Tarea 8.

- [ ] **Step 1: Agregarla a las pruebas (rojo)**

`test_material.MIGRADAS`: agrega `"/marmol-blanco-tampico": "marmol-blanco-tampico/index.html",`. `test_materiales_reglas.PENDIENTES = frozenset({"/piedra-bola-rio-tampico"})`.

Run: `cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas 2>&1 | tail -1`
Expected: `FAILED`.

- [ ] **Step 2: El contenido**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/contenido/marmol_blanco.py <<'EOF'
"""Contenido de /marmol-blanco-tampico (mármol blanco triturado por saco o por volumen). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularMarmol) como función pura, sin su precio.

El saco a $250 (y el $750–$1,250 por m²) no está en datos.py: el precio va "según cotización" en la etiqueta, la tabla,
la calculadora, el JSON-LD (sin Offer) y el título (pregunta 1 al dueño). La comparativa pierde el tezontle a $120 (en
datos.py es desde $200) y los precios por m². Sin “Calidad importada”, “premium”, “hasta 8°C”, “cantidad sin límite”,
“el mejor” ni “gratis”. Las 8 fotos de main, en su orden (el alt del saco ya no dice $250). Título, descripción y Open
Graph sin el $250 ni el “gratis” (PARIDAD["meta"]); HowTo de los 4 pasos como estaba.
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/marmol-blanco-tampico"
URL = f"{SITE}{RUTA}"
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Mármol blanco")
TITULO = "Mármol Blanco para Jardín Tampico · Saco de 20 kg"
DESCRIPCION = ("Mármol blanco decorativo en Tampico. Saco ≈ 20 kg · 3 sacos = 1 m² · Entrega en Madero y Altamira. "
               "Senderos, albercas y arriates. Cotiza hoy.")
DESCRIPCION_OG = ("Piedra mármol blanca decorativa en Tampico. Saco ≈ 20 kg; 3 sacos = 1 m². Entrega a domicilio. "
                  "Cotiza por WhatsApp.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Mármol Blanco para Jardín Tampico · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/marmol-blanco-alberca-palmera-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}
PORTADA_FOTO = {
    "src": "/img/portadas/marmol-blanco-alberca-palmera-tampico-sm.webp",
    "srcset": ("/img/portadas/marmol-blanco-alberca-palmera-tampico-sm.webp 560w, "
               "/img/portadas/marmol-blanco-alberca-palmera-tampico.webp 900w"),
    "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 900, "alto": 1200, "numero": 1,
    "alt": "Mármol blanco decorativo junto a una alberca con palmera", "lugar": "Mármol junto a la alberca",
    "etapa": "Tampico"}
FIGURAS = (
    {"src": "/img/marmol-blanco-alberca-palmera-tampico.webp", "ancho": 900, "alto": 1200, "numero": 2,
     "alt": "Mármol blanco decorativo alrededor de una alberca con palmera en Tampico", "lugar": "Borde de alberca",
     "etapa": "Con palmera"},
    {"src": "/img/marmol-blanco-arriate-suculentas-tampico.webp", "ancho": 1200, "alto": 1200, "numero": 3,
     "alt": "Mármol blanco como borde decorativo con suculentas en un jardín", "lugar": "Arriate", "etapa": "Suculentas"},
    {"src": "/img/marmol-blanco-maceta-decorativa-tampico.webp", "ancho": 1200, "alto": 1180, "numero": 4,
     "alt": "Mármol blanco en una maceta decorativa con suculenta", "lugar": "Maceta", "etapa": "Capa decorativa"},
)
FIGURA_SACO = {"src": "/img/marmol-blanco-saco-costal-tampico.webp", "ancho": 1024, "alto": 1536, "numero": 5,
               "alt": "Saco de red con unos 20 kg de mármol blanco", "lugar": "Saco de mármol blanco", "etapa": "≈ 20 kg"}
USOS = (
    {"titulo": "Senderos y caminos", "texto": "Caminos firmes y permeables dentro del jardín, con un brillo natural que se "
     "luce de noche con iluminación.", "puntos": ("4 a 5 sacos por m² (capa de 5 a 6 cm)",)},
    {"titulo": "Arriates de plantas", "texto": "Cubierta blanca alrededor de arbustos, helechos y plantas ornamentales: "
     "contrasta con el verde.", "puntos": ("3 sacos por m² (capa estándar)",)},
    {"titulo": "Borde y zona de alberca", "texto": "Alrededor de la alberca refleja la luz del agua y se siente fresco.",
     "puntos": ("3 a 4 sacos por m² (capa de 4 a 5 cm)",)},
    {"titulo": "Terrazas y azoteas", "texto": "Jardín seco de bajo mantenimiento para azoteas y terrazas, sobre membrana.",
     "puntos": ("3 sacos por m² (capa de 3 a 4 cm)",)},
    {"titulo": "Cajetes de palmas y árboles", "texto": "Cubierta alrededor del tronco de palmeras y árboles: protege las "
     "raíces y conserva la humedad.", "puntos": ("2 a 3 sacos por árbol (radio de 60 cm)",)},
    {"titulo": "Proyectos de paisajismo", "texto": "Hoteles, condominios, oficinas y fraccionamientos lo usan en áreas de "
     "imagen. Cotizamos por volumen.", "puntos": ("Por volumen, según cotización",)},
)
COMBINACIONES = (
    {"titulo": "Mármol + Pasto San Agustín", "texto": ("Un sendero de mármol blanco que atraviesa el pasto verde. "
     '<a href="/pasto-en-rollo-tampico">Pasto en rollo San Agustín</a>.')},
    {"titulo": "Mármol + Tezontle Rojo", "texto": ("Zonas blancas de mármol y zonas rojas de tezontle: diseños bicolor "
     'para paisajismo residencial y hotelero. <a href="/tezontle-rojo-tampico">Ver tezontle rojo</a>.')},
    {"titulo": "Mármol + palmas tropicales", "texto": ("Mármol blanco alrededor de palmas reales y árboles de ornato. "
     '<a href="/plantas-palmas-arboles-tampico">Ver plantas y palmas</a>.')},
    {"titulo": "Mármol + Tierra Negra", "texto": ("Primero se prepara el arriate con tierra negra para plantar y luego se "
     'cubre con mármol. <a href="/tierra-negra-vegetal-tampico">Ver tierra negra</a>.')},
    {"titulo": "Mármol + Riego automático", "texto": ("Goteo bajo el mármol, oculto: el mármol conserva la humedad y "
     'protege la manguera del sol. <a href="/sistema-riego-tampico">Ver sistema de riego</a>.')},
    {"titulo": "Mármol + Diseño de jardín", "texto": ("¿Un proyecto completo con pasto, plantas, mármol y riego? Planes "
     f'de diseño desde {dinero(P["diseno"])}. <a href="/diseno-jardines-tampico">Ver diseño de jardines</a>.')},
)
PASOS = (
    {"titulo": "Limpia el área", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira la maleza con raíz y nivela el suelo; si hay mucha irregularidad, agrega tierra para nivelar."},
    {"titulo": "Membrana antigerminante", "quien": "tu", "cuando": "Paso 2",
     "texto": "Coloca la membrana sin huecos y fija los bordes; en arriates, haz cortes en X donde van las plantas."},
    {"titulo": "Vierte el mármol", "quien": "tu", "cuando": "Paso 3",
     "texto": "Distribúyelo con rastrillo hasta el grosor que elegiste (3 a 6 cm según el uso)."},
    {"titulo": "Define los bordes", "quien": "tu", "cuando": "Paso 4",
     "texto": "Bordillo de piedra, metal o ladrillo para contener el mármol y dar un acabado limpio."},
)
PREGUNTAS = (
    ("¿Cuánto cuesta el mármol blanco para jardín en Tampico?",
     "El precio del saco de mármol blanco (unos 20 kg) y el de los pedidos por volumen se cotizan: escríbenos los m² y tu "
     "colonia y te mandamos el precio con la entrega, por escrito. Con 3 sacos se cubre 1 m² con capa de 3 a 4 cm; con "
     "capa de 5 a 6 cm, de 4 a 5 sacos por m²."),
    ("¿Cuántos sacos de mármol blanco necesito para 1 m²?",
     f"Para 1 m² con capa de 3 a 4 cm, {ejemplo('marmol', 1, 4)} (de unos 20 kg cada uno); para senderos o zonas de "
     "tránsito con capa de 5 a 6 cm, de 4 a 5 sacos por m². Regla rápida: tus m² por 3 dan el mínimo de sacos. La "
     "calculadora de esta página te da el número exacto."),
    ("¿Para qué sirve el mármol blanco en jardinería?",
     "Para senderos y caminos, arriates alrededor de plantas y arbustos, bordes de alberca, cubierta decorativa en "
     "terrazas y azoteas, cajetes alrededor de árboles y palmas y proyectos de paisajismo. Contrasta con la vegetación."),
    ("¿El mármol blanco se mancha o pierde su color con el tiempo?",
     "No pierde su color con el sol ni con las lluvias de Tampico. Con el tiempo junta polvo o tierra, que se quita con "
     "agua de la manguera; no necesita productos especiales ni selladores."),
    ("¿El mármol blanco controla la maleza?",
     "Sí, con membrana antigerminante debajo: la capa de 4 a 6 cm sobre la membrana tapa la luz que necesitan las "
     "semillas. Sin membrana ayuda, pero en el clima húmedo de Tampico no elimina toda la maleza."),
    ("¿Cuánto dura el mármol blanco instalado en un jardín?",
     "Es piedra natural: no se degrada. En senderos de mucho tránsito las piedras se dispersan; se resuelve con bordillos "
     "y rastrillado ocasional."),
    ("¿Entregan mármol blanco a domicilio en Tampico?",
     f"Sí, en Tampico, Ciudad Madero y Altamira. También puedes recogerlo en el vivero, {datos.CALLE}, Cd. Madero "
     f"({datos.REFERENCIA}). Para 20 sacos o más, coordinamos la entrega por WhatsApp o al {datos.TELEFONO_VISIBLE}."),
    ("¿Mármol blanco o tezontle rojo? ¿Cuál es mejor?",
     "Depende del objetivo. Mármol blanco para zona de alberca, terraza o un contraste luminoso con las plantas; "
     "tezontle rojo si buscas un precio más bajo (desde "
     f"{dinero(P['tezontle_costal'])} el costal), más control de maleza por ser poroso o el contraste rojo y verde. "
     "Muchos jardines combinan los dos en zonas distintas."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-marmol",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Mármol blanco <em>para jardines y andadores</em>",
        "lede": ("Grava de mármol blanco triturado de 1 a 3 cm para arriates, andadores y bordes de alberca: 3 sacos de "
                 "unos 20 kg cubren 1 m². El precio por saco o por volumen se cotiza con la entrega a tu colonia en "
                 "Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Mármol blanco", "aviso": "1 a 3 cm", "nombre": "Saco ≈ 20 kg", "antes": "cubren 1 m²",
                     "monto": "3 sacos", "unidad": "capa de 3 a 4 cm",
                     "filas": (("Precio por saco", SEGUN), ("20 sacos o más", "por volumen")),
                     "nota": "Te damos el precio por escrito con la entrega."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuántos sacos necesitas</a>.',
        "foto": PORTADA_FOTO,
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Por qué el mármol blanco transforma cualquier jardín?",
        "subtitulo": "Mármol blanco triturado para senderos y bordes de jardín",
        "parrafos": (
            ("El mármol blanco triturado es piedra natural para senderos, bordes de arriate y caminerías: contrasta con "
             "el pasto San Agustín, refleja la luz y da sensación de amplitud. Tamaños de 1 a 3 cm, por saco o por "
             "volumen."),
            ("En el clima de Tampico no pierde su color con el sol ni con las lluvias de temporada y no necesita "
             "mantenimiento especial."),
        ),
        "puntos": ("Conserva su color con sol y lluvia", "Drenaje natural: deja pasar el agua",
                   "Contraste: blanco con verde", "Con membrana, ayuda contra la maleza"),
        "figuras": FIGURAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "lede": "Una sola presentación: el saco de red de unos 20 kg. Su precio y el de volumen te los damos por escrito.",
        "caption": "Mármol blanco por presentación",
        "figura": FIGURA_SACO,
        "filas": (
            {"nombre": "Saco de mármol blanco", "detalle": "Saco de red ≈ 20 kg, piedra lavada y calibrada · sin mínimo",
             "unidad": "saco", "precio": None},
            {"nombre": "1 m² con capa de 3 a 4 cm", "detalle": "3 sacos", "unidad": "m²", "precio": None},
            {"nombre": "Pedidos de 20 sacos o más", "detalle": "Se cotizan por volumen", "unidad": "volumen",
             "precio": None},
        ),
        "nota": "Recoges en el vivero o te lo llevamos; la entrega se cotiza según tu colonia.",
        "tablas": (
            {"titulo": "Guía rápida de sacos por uso", "caption": "Sacos por m² según el uso y la capa",
             "columnas": ("Uso", "Capa", "Sacos por m²"),
             "filas": (("Macetas o decorativo", "3 cm", "3 sacos"), ("Arriates (estándar)", "4 cm", "3 a 4 sacos"),
                       ("Alberca o terraza", "5 cm", "4 sacos"), ("Sendero transitado", "6 cm", "4 a 5 sacos"))},
            {"titulo": "Mármol blanco, tezontle o piedra bola", "caption": "¿Cuál elegir?",
             "columnas": ("Característica", "Mármol blanco", "Tezontle rojo", "Piedra bola"),
             "filas": (("Precio por saco o costal", SEGUN, f"desde {dinero(P['tezontle_costal'])}", SEGUN),
                       ("Estilo", "Luminoso", "Vibrante", "Natural"),
                       ("Control de maleza", "Con membrana", "Excelente", "Parcial"),
                       ("Mantenimiento", "Lavado ocasional", "Rastrillado", "Mínimo"),
                       ("Al sol de Tampico", "No se decolora", "No se decolora", "No se decolora"))},
        ),
    },
    "usos": {"titulo": "¿Dónde lo quieres instalar?",
             "lede": "Cada uso tiene su capa y sus sacos por m² de referencia.", "items": USOS},
    "calculadora": {"clave": "marmol", "nombre": "mármol blanco", "titulo": "¿Cuántos sacos necesitas?",
                    "lede": "Escribe el área y el grosor de la capa: te damos los sacos y el peso aproximado."},
    "entrega": mc.entrega("el mármol blanco"),
    "combinaciones": {"titulo": "El mármol blanco combina con todo", "items": COMBINACIONES},
    "instalacion": {"titulo": "Cómo instalar mármol blanco en 4 pasos", "pasos": PASOS,
                    "howto": "Cómo instalar mármol blanco en tu jardín",
                    "nota": "¿Prefieres que lo instalemos nosotros? Lo cotizamos junto con el material."},
    "faq": {"titulo": "Todo sobre mármol blanco en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales decorativos",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/tierra-negra-vegetal-tampico",
                                       "/piedra-bola-rio-tampico"), con_miniatura=True),
              "enlaces": (("Arma tu lista de plantas", "/catalogo"),)},
    "cierre": {"titulo": "Cotiza tu mármol blanco",
               "lede": "Dinos los m² y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/jardin-residencial-pasto-san-agustin-tampico.webp", "ancho": 1280, "alto": 720}},
    "pedido": mc.pedido("Ejemplo: 36 sacos de mármol blanco, entrega en Tampico"),
    "jsonld": {
        "producto": mc.producto(
            "Mármol Blanco Decorativo para Jardín en Tampico",
            ("Piedra mármol blanca decorativa para jardines en Tampico. Saco de aproximadamente 20 kg; con 3 sacos se "
             "cubre 1 m² con capa estándar de 3 a 4 cm. Entrega a domicilio en Tampico, Ciudad Madero y Altamira."),
            f"{SITE}/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp"),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {
        "title": (TITULO, "Sin el $250 por saco: no está en datos.py (regla del dueño); el resto del título queda igual."),
        "description": (DESCRIPCION, "Sin el $250 por saco: no está en datos.py (regla del dueño)."),
        "og:description": (DESCRIPCION_OG, "Sin el $250 por saco (no está en datos.py) y sin “gratis” (regla del dueño)."),
    },
    "reemplazos": {
        "Una sola presentación, precio claro": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "Saco de Mármol Blanco": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "¿Para qué se usa el mármol blanco en jardinería?": "¿Para qué sirve el mármol blanco en jardinería?",
        "¿Cuánto dura el mármol blanco en el jardín?": "¿Cuánto dura el mármol blanco instalado en un jardín?",
    },
    "retirados": {
        "Viveros Terra · Tampico": mc.MOTIVO_AUTOR,
        "$0": "Era el estado vacío del “Total orientativo” de la calculadora, que ya no da precio (no está en datos.py).",
        "$250": mc.MOTIVO_PRECIO,
        "$750": mc.MOTIVO_PRECIO,
        "$1,250": mc.MOTIVO_PRECIO,
        "$120": "El tezontle a $120 contradecía datos.py (desde $200 el costal): la comparativa usa el de datos.py.",
        "$360": mc.MOTIVO_PRECIO,
        "$600": mc.MOTIVO_PRECIO,
    },
    "jsonld": {
        "Offer": ("El Offer publicaba el saco a $250, que no está en datos.py: el Product queda sin oferta hasta que el "
                  "dueño confirme el precio (pregunta 1)."),
        "LocalBusiness": mc.MOTIVO_LOCALBUSINESS,
    },
}
EOF
```

- [ ] **Step 3: Registrar, build, paridad y pruebas**

`generar.py`: después de tezontle, `("/marmol-blanco-tampico", "marmol-blanco-tampico/index.html", "material", "marmol_blanco"),`; `test_generar.esperadas`: `"/marmol-blanco-tampico",`. `tools/servicios/pages.py`: borra `"marmol-blanco-tampico": dict(…),`; `test_pagos.CON_PLANTILLA`: agrega `"marmol-blanco-tampico"`.

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /marmol-blanco-tampico
(cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia 2>&1 | tail -1)
grep -c '\$250' public/marmol-blanco-tampico/index.html
```

Expected: `plantillas: 1 de 40 páginas escritas`; `ok` en las seis (incluida la meta: título, descripción y `og:description` declarados); `OK`; `0`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/contenido/marmol_blanco.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_material.py \
  tools/site/tests/test_materiales_reglas.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py public/marmol-blanco-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): mármol blanco con sacos por m² de main y precio según cotización" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: `/piedra-bola-rio-tampico` y la prueba de `window.open` del blog

**Files:**
- Create: `tools/site/contenido/piedra_bola.py`
- Modify: los seis de la Tarea 8 y `tools/site/tests/test_navegador.py`

- [ ] **Step 1: Agregarla a las pruebas (rojo)**

`test_material.MIGRADAS`: agrega `"/piedra-bola-rio-tampico": "piedra-bola-rio-tampico/index.html",`. `test_materiales_reglas.PENDIENTES = frozenset()` (y en su docstring: "al cerrar la Etapa 2f queda vacía" ya se cumple).

`tools/site/tests/test_navegador.py`, en `test_window_open_de_whatsapp_sale_firmado`, reemplaza

```python
        # Diseño sale de su plantilla desde la Etapa 2c (un botón por plan); piedra bola conserva sendWA hasta la 2f.
        page.goto(self.base + "/piedra-bola-rio-tampico/", wait_until="load")
        page.evaluate("() => sendWA('Hola, quiero cotizar piedra bola de río')")
```

por

```python
        # Desde la Etapa 2f ninguna página con plantilla abre WhatsApp con window.open: queda el sendWA(msg) de los
        # artículos del blog hechos a mano (hasta la Etapa 2h).
        page.goto(self.base + "/blog/tezontle-usos-jardin-tampico/", wait_until="load")
        page.evaluate("() => sendWA('Hola, quiero cotizar tezontle rojo')")
```

Run: `cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas 2>&1 | tail -1`
Expected: `FAILED`.

- [ ] **Step 2: El contenido**

```bash
cd ~/dev/viverosterra-e2f
cat > tools/site/contenido/piedra_bola.py <<'EOF'
"""Contenido de /piedra-bola-rio-tampico (piedra bola de río chica, mediana y grande, por costal o camión). Solo datos:
la plantilla es tools/site/plantillas/material.py.

Main no publicaba precio (solo el JSON-LD, con un Offer de $350 e "InStock" que nadie dio): todo va "según cotización".
Main tampoco tenía calculadora: la nueva multiplica el área por los 120 a 150 kg por m² que decía su propia pregunta
frecuente (pregunta 6 al dueño). Las opiniones de Patricia H. y David M. no tienen permiso del dueño y se retiran. Sin
foto de portada (main no la tenía); sus 3 fotos en su orden: la del CTA final y, después, las dos miniaturas de otros
materiales (por eso "otros" va tras el cierre). Título y descripción como estaban; el Open Graph pierde el “gratis”.
"""
import datos
import mensajes_paginas
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

SITE = datos.SITIO
RUTA = "/piedra-bola-rio-tampico"
URL = f"{SITE}{RUTA}"
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Piedra bola de río")
DESCRIPCION_OG = ("Piedra bola de río natural en Tampico para jardines, senderos y decoración. Pequeña, mediana y "
                  "grande. Entrega a domicilio en Madero y Altamira. Cotiza por WhatsApp.")
META = {
    "title": "Piedra Bola de Río Tampico · Jardines y Senderos",
    "description": ("Piedra bola de río natural en Tampico para jardines y senderos. Pequeña, mediana y grande. Costal y "
                    "camión volteo. Entrega a domicilio en Tampico y zona."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Piedra Bola de Río Tampico | Venta para Jardines y Senderos — Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/jardin-residencial-plantas-pasto-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}
USOS = (
    {"titulo": "Senderos y caminos", "texto": "Piedra mediana para caminos decorativos: deja pasar el agua, resiste y pide "
     "poco mantenimiento.", "puntos": ("Mediana, 6 a 12 cm",)},
    {"titulo": "Jardines zen y japoneses", "texto": "Piedra bola mediana con arena o gravilla y vegetación minimalista.",
     "puntos": ("Mediana",)},
    {"titulo": "Cubierta decorativa de suelo", "texto": "Piedra chica sobre camas de plantas y arriates: ayuda contra la "
     "maleza, mejora el drenaje y da un aspecto limpio.", "puntos": ("Chica, 2 a 5 cm",)},
    {"titulo": "Fuentes y estanques", "texto": "Piedra grande en la base de fuentes, bordes de estanques y elementos de "
     "agua.", "puntos": ("Grande, 12 a 20 cm",)},
    {"titulo": "Borduras y delimitadores", "texto": "Piedra grande colocada de canto para delimitar zonas, arriates y "
     "senderos.", "puntos": ("Grande",)},
    {"titulo": "Contraste con tezontle", "texto": ("Piedra bola gris con tezontle rojo, un contraste bicolor para "
     'paisajismo moderno. <a href="/tezontle-rojo-tampico">Ver tezontle rojo</a>.'), "puntos": ("Chica o mediana",)},
)
PREGUNTAS = (
    ("¿Para qué se usa la piedra bola de río en jardinería?",
     "Para cubrir el suelo de jardines y áreas verdes, hacer senderos y caminos, delimitar arriates, diseñar jardines zen "
     "o japoneses, decorar fuentes y estanques y dar acabados naturales en exteriores."),
    ("¿En qué tamaños se vende la piedra bola de río en Tampico?",
     "En tres medidas: chica (2 a 5 cm), para cubrir suelo y borduras; mediana (6 a 12 cm), para senderos y decoración; "
     "y grande (12 a 20 cm), para puntos focales y fuentes. Se pueden combinar en la misma entrega."),
    ("¿La piedra bola de río necesita mantenimiento?",
     "Casi ninguno: limpieza ocasional con agua a presión si junta polvo o lodo y reponer lo que se desplace con las "
     "lluvias o el uso. No pierde su aspecto con el tiempo."),
    ("¿Cuánta cantidad de piedra bola necesito para mi jardín?",
     "Con piedra mediana y capa de 8 a 10 cm se usan de 120 a 150 kg por m²: para un sendero de 1 m de ancho por 10 m de "
     f"largo (10 m²), {ejemplo('piedra-bola', 10)}. Usa la calculadora de esta página o mándanos la medida y el área."),
    ("¿Se puede combinar piedra bola de río con tezontle y mármol?",
     "Sí. La piedra bola gris con tezontle rojo da un contraste bicolor para jardines zen o contemporáneos, y el mármol "
     "blanco de fondo con borduras de piedra bola también se usa en jardines residenciales de Tampico."),
    ("¿Entregan piedra bola de río a domicilio en Tampico?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto: por costal para "
     "cantidades chicas o en camión volteo para proyectos medianos y grandes. El costo de entrega depende del volumen y "
     "la distancia."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-piedra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Piedra bola de río <em>para jardines y senderos</em>",
        "lede": ("Piedra de río natural en tres medidas para senderos, jardines secos y fuentes. Por costal o camión; "
                 "el precio se cotiza según la medida y el volumen, con entrega en Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Piedra bola", "aviso": "Por medida", "nombre": "Chica, mediana y grande", "antes": "",
                     "monto": "3 medidas", "unidad": "costal o camión",
                     "filas": (("Chica", "2 a 5 cm"), ("Mediana", "6 a 12 cm"), ("Grande", "12 a 20 cm"),
                               ("Precio", SEGUN)),
                     "nota": "Te damos el precio por escrito con la entrega."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuántos kg necesitas</a>.',
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Qué es la piedra bola de río y para qué sirve en jardines?",
        "parrafos": (
            ("Es una roca natural de río, ovalada y lisa, pulida por la corriente del agua. En jardinería se usa como "
             "elemento decorativo y como cubierta de suelo que ayuda contra la maleza y mejora el drenaje. La tenemos en "
             "tres medidas para casas, comercios y proyectos de paisajismo en Tampico."),
        ),
    },
    "precio": {
        "titulo": "¿Cuánto cuesta la piedra bola de río en Tampico?",
        "lede": "El precio depende de la medida y del volumen: te lo damos por escrito antes de que confirmes.",
        "caption": "Piedra bola de río por medida",
        "filas": (
            {"nombre": "Chica", "detalle": "2 a 5 cm · cubierta de suelo y borduras", "unidad": "costal o camión",
             "precio": None},
            {"nombre": "Mediana", "detalle": "6 a 12 cm · senderos y decoración", "unidad": "costal o camión",
             "precio": None},
            {"nombre": "Grande", "detalle": "12 a 20 cm · fuentes y puntos focales", "unidad": "costal o camión",
             "precio": None},
        ),
        "nota": "El costo de entrega se cotiza según tu colonia y el volumen.",
    },
    "usos": {"titulo": "¿Cómo se usa la piedra bola de río en Tampico?",
             "lede": "Cada uso con la medida que le va.", "items": USOS},
    "calculadora": {"clave": "piedra-bola", "nombre": "piedra bola", "titulo": "¿Cuánta piedra bola necesitas?",
                    "lede": "Escribe el área: te damos los kg aproximados con piedra mediana y capa de 8 a 10 cm."},
    "entrega": mc.entrega("la piedra bola"),
    "faq": {"titulo": "Todo sobre piedra bola de río en Tampico", "preguntas": PREGUNTAS},
    "cierre": {"titulo": "¿Qué proyecto tienes en mente con piedra bola de río?",
               "lede": "Dinos la medida, el área y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/jardin-residencial-plantas-pasto-tampico.webp", "ancho": 933, "alto": 1400}},
    "otros": {"titulo": "Otros materiales decorativos", "tras_cierre": True,
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/tierra-negra-vegetal-tampico", "/marmol-blanco-tampico"),
                                con_miniatura=True)},
    "pedido": mc.pedido("Ejemplo: piedra bola mediana para 10 m², entrega en Altamira"),
    "jsonld": {
        "producto": mc.producto(
            "Piedra Bola de Río para Jardín Tampico",
            ("Piedra bola de río natural para jardines en Tampico, en medida chica, mediana y grande. Por costal y camión "
             "volteo, con entrega a domicilio en Tampico, Madero y Altamira."),
            f"{SITE}/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp", sku="VT-PIE-001"),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {"og:description": (DESCRIPCION_OG, "Sin “Cotiza gratis” (regla del dueño); el resto queda igual.")},
    "reemplazos": {},
    "retirados": {
        "Lo que dicen nuestros clientes": mc.MOTIVO_TESTIMONIOS,
        "/piedra-bola-rio-tampico": "Era el enlace de la página a sí misma en “Otros materiales”; ahí va el mármol blanco.",
    },
    "jsonld": {
        "Offer": ("El Offer publicaba $350 e “InStock”: ni el precio está en datos.py ni hay dato de existencias. El "
                  "Product queda sin oferta hasta que el dueño dé el precio (pregunta 2)."),
        "LocalBusiness": mc.MOTIVO_LOCALBUSINESS,
    },
}
EOF
```

- [ ] **Step 3: Registrar, build, paridad y pruebas**

`generar.py`: después de mármol, `("/piedra-bola-rio-tampico", "piedra-bola-rio-tampico/index.html", "material", "piedra_bola"),`; `test_generar.esperadas`: `"/piedra-bola-rio-tampico",`. `tools/servicios/pages.py`: borra `"piedra-bola-rio-tampico": dict(…),` (queda solo `vivero-tampico`) y cambia el comentario de arriba de `PAGES` por:

```python
# La home y /pasto-en-rollo-tampico (Etapa 2a), diseño, mantenimiento y riego (Etapa 2c) y mayoreo y palmas para
# proyectos (Etapa 2d), el hub de plantas y sus cinco subcategorías (Etapa 2e) y, desde la Etapa 2f, los cuatro
# materiales salen de tools/site/plantillas/: este script ya no las toca. Queda el vivero (Etapa 3).
```

`test_pagos.CON_PLANTILLA`: agrega `"piedra-bola-rio-tampico"`.

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /tierra-negra-vegetal-tampico /tezontle-rojo-tampico /marmol-blanco-tampico /piedra-bola-rio-tampico
(cd tools/site && python3 -m unittest tests.test_material tests.test_materiales_reglas tests.test_paridad tests.test_contenido tests.test_generar tests.test_reglas tests.test_consistencia tests.test_navegador 2>&1 | tail -1)
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1)
grep -lE "window\.open|VTMedicion\.whatsapp" public/{tierra-negra-vegetal-tampico,tezontle-rojo-tampico,marmol-blanco-tampico,piedra-bola-rio-tampico}/index.html | wc -l
```

Expected: `plantillas: 1 de 41 páginas escritas`; `ok` en las seis categorías de las 4 páginas; `OK`; `OK`; `0`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/contenido/piedra_bola.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_material.py \
  tools/site/tests/test_materiales_reglas.py tools/site/tests/test_navegador.py tools/servicios/pages.py tools/servicios/tests/test_pagos.py \
  public/piedra-bola-rio-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(materiales): piedra bola de río por medida según cotización, con calculadora de kg de su FAQ" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Pruebas en navegador de los materiales

**Files:**
- Test: `tools/site/tests/test_plantillas_navegador.py`

Las 4 páginas entran a las pruebas de plantilla que ya existen (axe de página completa a 375 y 1440, precio y CTA en el primer pantallazo a 375×812, sin desbordar de 320 a 1920, CLS < 0.1) y a la del CTA a 1024×800. Pruebas nuevas: las cuatro calculadoras con teclado (cantidad de main, mensaje con el resultado y la firma, `generate_lead` con el `cta_id` de main), calculadora vacía con el mensaje de la página, pedido por correo (validación, POST con los campos de main y `generate_lead` `formulario`) y fotos de main sin romperse.

- [ ] **Step 1: Agregar las pruebas**

En `tools/site/tests/test_plantillas_navegador.py`, reemplaza `CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS` por

```python
# Etapa 2f: materiales con la plantilla material (portada con o sin foto, calculadora y pedido por correo).
MATERIALES = ("/tierra-negra-vegetal-tampico/", "/tezontle-rojo-tampico/", "/marmol-blanco-tampico/",
              "/piedra-bola-rio-tampico/")
CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS + MATERIALES
```

en `test_cta_en_la_primera_pantalla_a_1024` cambia `for ruta in SERVICIOS + EMPRESAS:` por `for ruta in SERVICIOS + EMPRESAS + MATERIALES:`, y agrega a la clase, antes de `def test_cls_bajo_0_1_en_movil(self):`:

```python
    # ---------- Etapa 2f: materiales ----------
    CALCULOS = (
        ("/tierra-negra-vegetal-tampico/", "vt-tierra", "87.5", "0.10", "material:cotizarCalculado", "8.8 m³"),
        ("/tezontle-rojo-tampico/", "vt-tezontle", "50", "0.08", "material:cotizarTezontle", "4 m³"),
        ("/marmol-blanco-tampico/", "vt-marmol", "50", "6", "material:cotizarMarmol", "250 sacos"),
        ("/piedra-bola-rio-tampico/", "vt-piedra", "10", None, "material:cotizarPiedra", "1,200 a 1,500 kg"),
    )

    def test_calculadoras_de_materiales_con_teclado_mensaje_y_generate_lead(self):
        """La calculadora de main, ahora un enlace medido: con teclado da la cantidad de main, el WhatsApp lleva el
        resultado y la firma, y el clic manda generate_lead con el mismo cta_id que medía VTMedicion.whatsapp."""
        for ruta, prefijo, area, capa, cta_id, cantidad in self.CALCULOS:
            page = self.pagina(1440, 900)
            page.goto(self.base + ruta, wait_until="load")
            page.locator(f"#{prefijo}-area").focus()
            page.keyboard.type(area)
            if capa:
                page.locator(f"#{prefijo}-capa").select_option(capa)
            caja = page.locator("[data-vt-material]")
            enlace = caja.locator('[data-vt-o="cta"]')
            mensaje = unquote(enlace.get_attribute("href").split("text=", 1)[1])
            with self.subTest(ruta=ruta):
                self.assertEqual(caja.locator('[data-vt-o="cantidad"]').inner_text(), cantidad)
                self.assertIn(f"Área: {area} m²", mensaje)
                self.assertTrue(mensaje.endswith("¿Me pueden dar precio de entrega a domicilio en Tampico?"))
            page.evaluate("(a) => a.addEventListener('click', (e) => e.preventDefault())", enlace.element_handle())
            enlace.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            with self.subTest(ruta=ruta, paso="clic"):
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": cta_id, "service": "materiales"}],
                              eventos)
                self.assertTrue(unquote(enlace.get_attribute("href")).endswith(datos.FIRMA))

    def test_calculadora_de_materiales_sin_area_manda_el_mensaje_de_la_pagina(self):
        page = self.pagina(375, 812)
        for ruta, prefijo, area, _capa, _cta, _cantidad in self.CALCULOS:
            page.goto(self.base + ruta, wait_until="load")
            campo = page.locator(f"#{prefijo}-area")
            campo.fill(area)
            campo.fill("")
            esperado = datos.con_firma(mensajes_paginas.MATERIALES[ruta.rstrip("/")])
            href = page.locator('[data-vt-material] [data-vt-o="cta"]').get_attribute("href")
            with self.subTest(ruta=ruta):
                self.assertEqual(unquote(href.split("text=", 1)[1]), esperado)
                self.assertEqual(page.locator('[data-vt-material] [data-vt-o="cantidad"]').inner_text(), "Escribe el área")

    def test_pedido_por_correo_de_materiales_valida_y_envia_los_campos_de_main(self):
        """El formulario de main (nombre, email, detalle) sigue yendo por POST a formsubmit de la cuenta oficial, ahora
        con honeypot, validación junto a cada campo y generate_lead method "formulario"."""
        page = self.pagina(375, 812)
        enviados = []
        page.route("https://formsubmit.co/**", self.atrapador(enviados))
        page.goto(self.base + "/marmol-blanco-tampico/", wait_until="load")
        form = page.locator("#solicitar-pedido form.vt-correo")
        boton = form.locator('button[type="submit"]')
        boton.click()
        self.assertEqual(enviados, [])
        self.assertEqual(page.evaluate("() => document.activeElement.name"), "nombre")
        form.locator('[name="nombre"]').fill("Ana")
        form.locator('[name="email"]').fill("ana@")
        boton.click()
        self.assertEqual(page.evaluate("() => document.activeElement.name"), "email")
        self.assertIn("tu@correo.com", form.locator("#vt-marmol-c-email-error").inner_text())
        form.locator('[name="email"]').fill("ana@ejemplo.com")
        form.locator('[name="detalle"]').fill("36 sacos, entrega en Tampico")
        page.evaluate("() => document.addEventListener('submit', (e) => e.preventDefault(), { once: true })")
        boton.click()
        eventos = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        with page.expect_navigation():
            page.evaluate("() => document.querySelector('#solicitar-pedido form').submit()")
        metodo, url, cuerpo = enviados[0]
        campos = dict(parse_qsl(cuerpo, keep_blank_values=True))
        self.assertEqual((metodo, url), ("POST", f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"))
        self.assertEqual({k: campos[k] for k in ("nombre", "email", "detalle", "_subject", "_next", "_honey")},
                         {"nombre": "Ana", "email": "ana@ejemplo.com", "detalle": "36 sacos, entrega en Tampico",
                          "_subject": "Pedido desde sitio web - Viveros Terra", "_next": f"{datos.SITIO}/gracias",
                          "_honey": ""})
        self.assertIn(["event", "generate_lead", {"method": "formulario", "cta_id": "material:formulario",
                                                  "service": "materiales"}], eventos)

    def test_fotos_de_materiales_cargan_sin_deformarse(self):
        """Las fotos de main, todas: ninguna rota tras desplazar la página (carga lazy) y ninguna estirada."""
        page = self.pagina(1440, 900)
        for ruta in MATERIALES:
            page.goto(self.base + ruta, wait_until="load")
            page.evaluate("async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) {"
                          " scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } }")
            page.wait_for_load_state("networkidle")
            malas = page.evaluate("""() => Array.from(document.querySelectorAll('main img')).filter((i) =>
              !i.complete || !i.naturalWidth || getComputedStyle(i).objectFit === 'fill').map((i) => i.src)""")
            with self.subTest(ruta=ruta):
                self.assertEqual(malas, [])
```

- [ ] **Step 2: Correrlas**

Run: `cd tools/site && python3 -m unittest tests.test_plantillas_navegador 2>&1 | tail -3`
Expected: `OK`. Si axe marca algo serio (contraste del texto sobre la foto del cierre, `select` sin nombre), corrígelo en `terra.css` o en `componentes_materiales.py` con su prueba, reconstruye y repite.

- [ ] **Step 3: Consola limpia en las 108 páginas y nunca dos barras**

Run: `cd tools/site && python3 -m unittest tests.test_navegador tests.test_tienda_navegador 2>&1 | tail -3`
Expected: `OK` (incluye `test_consola_limpia_en_todas_las_paginas`, `test_nunca_dos_barras_fijas_abajo_a_375` y el `window.open` firmado del blog).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2f
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): materiales con axe, desborde, primer pantallazo, calculadoras, pedido por correo y fotos" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Verificación final y puertas de revisión (merge y push los hace el controlador)

**Files:** ninguno nuevo (correcciones de los revisores, cada una con su prueba y su commit).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 41 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `OK` (anota el `Ran`: `Ran 552 tests` en el prototipo); `Ran 34 tests` y `OK`; `Ran 2 tests` y `OK`; `ℹ pass 65` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas y palabras a la vista**

```bash
cd ~/dev/viverosterra-e2f
python3 tools/site/paridad.py informe /tierra-negra-vegetal-tampico /tezontle-rojo-tampico /marmol-blanco-tampico /piedra-bola-rio-tampico
(cd tools/site && python3 -m unittest tests.test_reglas tests.test_consistencia tests.test_paridad tests.test_materiales_reglas tests.test_materiales_paridad tests.test_material tests.test_contenido 2>&1 | tail -1)
grep -oiE "oasis|gratis|sin costo|instock|disponibilidad|entrega inmediata|el mejor|imbatible|m[aá]s popular|m[aá]s vendid|productor directo|\\\$250|\\\$100|\\\$5,000|\\\$3,200|\\\$350|Ricardo O|Laura P|Patricia H|David M|en nuestro vivero|window\.open" \
  public/{tierra-negra-vegetal-tampico,tezontle-rojo-tampico,marmol-blanco-tampico,piedra-bola-rio-tampico}/index.html | sort | uniq -c
```

Expected: `ok` en las seis categorías de las 4 páginas; `OK`; el `grep` vacío.

- [ ] **Step 3: Lighthouse móvil**

```bash
cd ~/dev/viverosterra-e2f
(cd public && python3 -m http.server 8769 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in tierra-negra-vegetal-tampico tezontle-rojo-tampico marmol-blanco-tampico piedra-bola-rio-tampico; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8769/$r/" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2f-lh-$r.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2f-lh-$r.json"
done
pkill -f "http.server 8769"
```

Expected por página: Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s. CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. En tezontle y piedra bola (sin foto de portada) el LCP es texto; en tierra y mármol, la foto de portada precargada. Si Performance queda abajo por GA4 o por las fotos de main que se cargan lazy (las de tierra pesan 140–200 KB y no se recomprimen: regla de fotos), anota valor y causa para el PR.

- [ ] **Step 4: Capturas a 320, 375, 768, 1024, 1440 y 1920 con el viewport real de Playwright**

```bash
cd ~/dev/viverosterra-e2f/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
rutas = ('tierra-negra-vegetal-tampico/', 'tezontle-rojo-tampico/', 'marmol-blanco-tampico/', 'piedra-bola-rio-tampico/')
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in rutas:
        for w in (320, 375, 768, 1024, 1440, 1920):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.evaluate("async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); } scrollTo(0, 0); }")
            p.screenshot(path=f"/tmp/vt-e2f-{r.strip('/')}-{w}.png", full_page=True)
            p.close()
    b.close()
srv.shutdown()
print(len(rutas) * 6, 'capturas')
PY
```

Expected: `24 capturas`. Revisa a mano: etiqueta con precio o "Según cotización" y CTA en el primer pantallazo a 375; portada de tierra en 3:2 sin cortar el camión; tezontle y piedra bola sin hueco donde iría la foto; las 23 fotos de main en su orden y sin deformar (las de tezontle se ven chicas: son de 194–259 px, pregunta 13); la calculadora con su etiqueta al lado desde 1024 y debajo en celular; "Según cotización" en dos renglones a 320; el cierre con la foto de fondo legible; miniaturas de 48 px en mármol y piedra bola; el formulario al final con sus errores junto a cada campo.

- [ ] **Step 5: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega la rama en verde y un resumen (`git log --oneline main..feat/etapa-2f`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2f --stat`, `plantillas/material.py`, `componentes_materiales.py`, `contenido/{materiales_comun,tierra_negra,tezontle_rojo,marmol_blanco,piedra_bola}.py`, `vt-materiales.js`, el diff de `vt-b2b.js` y `terra.css`, la vista previa de Vercel, `/tmp/vt-e2f-*.png`, los JSON de Lighthouse, `paridad.py informe` y el spec (§3.3, §5, §7.3, §8, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta, pies FIG., cuadro de datos), jerarquía de la portada sin foto, la calculadora (campo, `select` con label, etiqueta `role="status"`, objetivos de 44 px), "Según cotización" sin parecer un error, contraste sobre la foto del cierre, miniaturas de otros materiales (foco visible en toda la tarjeta), formulario (errores, foco) y movimiento reducido.
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta salvo lo declarado (mármol: título, descripción y OG; tierra: descripción y OG; piedra bola: OG), un H1 por página, migas visibles = `BreadcrumbList`, `FAQPage` = lo visible, `Product` válido en Rich Results Test sin `InStock` (mármol y piedra bola sin `Offer`: advertencia esperada, no error), `HowTo` de mármol, entrada de portada como respuesta directa, enlaces internos (combinaciones, otros materiales, guías del blog), imágenes con `width`/`height`/`alt`, y que nada adelante la Etapa 3 (títulos) ni la 4 (grafo, `dateModified`).
3. **CRO** (`general-purpose` con `page-cro`): precio o "según cotización" y CTA en el primer pantallazo; de la calculadora al WhatsApp con la cantidad; que quitar los botones por presentación y por uso no deje a nadie sin camino; el pedido por correo como alternativa; mármol y piedra bola sin precio: que el mensaje pida lo necesario para cotizar (m², medida, colonia).
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `typescript-reviewer` para el JS + `e2e-runner`): reglas del dueño (precios solo de `datos.py`, "según cotización" sin inventar, fotos de main en orden, sin "gratis", sin existencias ni plazos, anticipo, opiniones), paridad de las calculadoras (195 casos) y su `esperado_de_main` (que solo aplique los cambios declarados), formulario (mismos campos, `action`, `_next`, `_honey`, `generate_lead`), sin `innerHTML` con datos (`vt-materiales.js` usa `textContent`), el cambio de `vt-b2b.js` sin regresión en empresas, consola limpia y sin `.DS_Store`.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 1 otra vez) y el controlador vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan para el PR.

- [ ] **Step 6: Aprobación del dueño (controlador)**

Comparte la vista previa de Vercel y las capturas, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Si da precios (mármol, piedra bola, m³ y camión de tezontle, camión o tierra preparada), van a `datos.PRECIOS` con su prueba en `test_datos` y `test_materiales_reglas.test_precios_de_tierra_negra_y_tezontle_de_datos` (que hoy impide agregar uno sin confirmarlo), y las filas de `presentaciones` pasan de `None` al precio, en una tarea nueva antes del merge.

- [ ] **Step 7: Merge, push y despliegue (solo el controlador)**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2f -m "feat: Etapa 2f, materiales con la plantilla material, calculadoras de main y precios de datos.py" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 41 …`, `shell: 0 de 108 …`, `0`; Vercel despliega `main`.

- [ ] **Step 8: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in tierra-negra-vegetal-tampico tezontle-rojo-tampico marmol-blanco-tampico piedra-bola-rio-tampico; do
  printf "%s " $r; curl -s $W/$r | grep -cE "tailwind.css|design-system.css|servicios.css|fonts.googleapis|window\.open|InStock|gratis"
done
curl -s $W/js/vt-materiales.js | head -1
curl -s -o /dev/null -w "%{http_code}\n" $W/img/tezontle-rojo-jardin-tampico-sendero.webp
```

Expected: `0` en las 4; `// public/js/vt-materiales.js`; `200`. En Chrome (escritorio y iPhone): consola limpia; en tierra negra, 87.5 m² con 10 cm da "8.8 m³" y "Camión volteo de 8 m³ o más (según cotización)", y "Cotizar por WhatsApp" abre el mensaje con el resultado y la firma; el formulario de mármol, con un correo de prueba del dueño, llega a viverosterra@hotmail.com con el asunto "Pedido desde sitio web - Viveros Terra". En GA4 DebugView: `generate_lead` `material:cotizarCalculado` (y `cotizarTezontle`, `cotizarMarmol`, `cotizarPiedra`) con `service` `materiales`, y `generate_lead` `method` `formulario`, `cta_id` `material:formulario`.

- [ ] **Step 9: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 10: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2f && git branch -d feat/etapa-2f
```

---

## Lotes de ejecución sugeridos

| Lote | Tareas | Qué deja | Revisión intermedia |
|---|---|---|---|
| A · Fundaciones (sin cambiar cómo se ven las páginas) | 0–3 | Capturas de paridad, fotos y casos de main; mensajes por página; reglas en rojo | Cumplimiento: que las capturas sean de main y las reglas detecten lo que deben |
| B · Piezas | 4–6 | Lógica en Python y JS con paridad de 195 casos, `vt-b2b.js`, componentes y CSS | Código (python-reviewer, typescript-reviewer): paridad y `esperado_de_main` |
| C · Páginas | 7–10 | Plantilla y las 4 páginas migradas, una por commit | Paridad e informe por página; reglas en verde |
| D · Cierre | 11–12 | Navegador, Lighthouse, capturas, 4 puertas, aprobación del dueño, merge | Las 4 puertas del spec §11 |

## Correcciones a la hoja de ruta

- "CTA con `datos.MENSAJES["materiales"]`": como en 2c–2e, cada página lleva su plantilla (`mensajes_paginas.MATERIALES`, la de su portada en main) en el formato de `MENSAJES["materiales"]` —material, cantidad y "Colonia de entrega: ___"— con el material ya escrito; el genérico sigue siendo el respaldo del shell. La prueba exige la línea de colonia de `MENSAJES["materiales"]` en las cuatro.
- "Calculadoras con `window.open` medidas por `medicion_js.py`": `medicion_js.py` era el parche de las páginas a mano. Con plantilla, la calculadora es un enlace con `data-cta` (patrón de 2d y 2e) que `terra.js` mide y firma, con el mismo `cta_id` que mandaba main; la prueba usa `medicion_js.medir_whatsapp_js` para comprobar que no queda ninguna apertura por medir (cuenta en 0).
- Orden de la plantilla: "qué es" va antes del precio por presentación (el precio de cada presentación ya está en la etiqueta del primer pantallazo) para respetar el orden de las fotos de main; en piedra bola, "otros materiales" va después del CTA final, como en main.
- Piedra bola no tenía calculadora: la nueva usa solo la regla publicada en su FAQ (pregunta 6).
- El formulario de pedido de main se conserva (no estaba en la hoja de ruta; lo pide el dueño y `test_reglas` ya lo permite) y se mide como el de empresas, reutilizando `vt-b2b.js`.
- La fecha visible "Última actualización: 14 de mayo, 2026" de main no se reproduce: el spec §7.4 la pide para la Etapa 4, con `dateModified` real; publicar una fecha vieja en una página nueva sería falso (no es encabezado ni FAQ: la paridad no la cubre; se anota en el PR).
- Lote 4: 2e ya está en `main` (`4169785`); 2f se publica solo y cierra el lote.
- El CSS cabe en `terra.css` (≈ 975 B): sin hoja `terra-materiales.css`. Deja 663 B para 2g–2i; 2h (artículo) deberá traer su propia hoja.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| La paridad reproduce el redondeo raro de main (7 m² × 10 cm = 0.8 m³) | Es lo que pide la aceptación; documentado en `test_casos_con_los_redondeos_de_main` y pregunta 8. Corregirlo es cambiar una línea en Python y JS y regenerar el esperado con motivo. |
| Python y JS se desfasan en el futuro | Los dos corren los mismos 195 casos de main (`unittest` y `node --test`); `data-material` sale de `datos_js()` y su prueba compara el JSON. |
| Quitar precios sin confirmar baja información (mármol a $250, tezontle $3,200/m³) | Eran precios que no están en `datos.py`; cada uno se retira con motivo en `PARIDAD` y vuelve si el dueño lo confirma (preguntas 1–4). La etiqueta, la tabla y el mensaje dicen "Según cotización" y piden lo necesario para cotizar. |
| `Product` sin `offers` en mármol y piedra bola | Advertencia (no error) en Rich Results Test; mejor que un precio inventado o `InStock` sin dato. Vuelve el `Offer` con el precio del dueño. |
| El cambio de `vt-b2b.js` rompe empresas | Sin argumento, `erroresCorreo` se comporta igual (mismo mensaje de `compras@tuempresa.com`); prueba en node y las de navegador de empresas siguen en el `discover`. |
| Fotos de main chicas o pesadas (tezontle 194–259 px; tierra 140–200 KB) | Regla del dueño: no se cambian. Se cargan lazy con `width`/`height` (sin CLS); Lighthouse lo anota; entran a la sesión de fotos (pregunta 13). |
| `terra.css` queda a 663 B del tope | Medido en el prototipo; 2g–2i lo saben (Correcciones). |
| Un formulario que el dueño usa deja de llegarle | Mismos `action`, campos y `_subject`; prueba de navegador con POST interceptado y verificación en vivo con un correo de prueba (Tarea 12, Step 8). |

## Preguntas al dueño

1. **Mármol blanco:** main publicaba **$250 el saco** (≈ 20 kg), "$750 a $1,250 por m²" y "precio especial en pedidos de 20 sacos o más", pero no está en `datos.py`. ¿Confirmas $250 por saco (con o sin IVA)? ¿Hay precio por volumen desde 20 sacos? Mientras no, va "Según cotización" (también en el título, que decía "$250 por Saco").
2. **Piedra bola de río:** ¿precio por costal y por camión de cada medida (chica 2–5 cm, mediana 6–12, grande 12–20)? El JSON-LD de main decía $350 e "InStock": ¿de dónde salió? Mientras no, todo "Según cotización" y sin `Offer`.
3. **Tezontle rojo:** ¿precio por m³ (main decía "desde $3,200") y del camión de 14 m³ ("Preguntar precio")? ¿El costal de $200 es precio fijo o "desde"? (Hoy va "desde $200", como en la home.)
4. **Tierra negra:** ¿la **tierra preparada** con hojarasca y abono a **$100** el costal es real? ¿El camión volteo "desde $5,000" y los camiones de **5, 8 y 14 m³ a $3,500, $5,200 y $8,000**? ¿Esos tres tamaños de camión existen?
5. **Tamaño de los costales:** tezontle decía "costal de 15 kg" (JSON-LD) y "de 25 a 30 kg" (tarjeta); tierra negra "≈ 20 kg" y "de 30 a 40 kg" (usos). ¿Cuánto pesan? Las calculadoras de main usan 0.035 m³ por costal de tierra y 0.027 m³ por costal de tezontle para "~N costales": ¿son correctos? Mientras no, se publica tierra ≈ 20 kg y tezontle sin peso, y las equivalencias de main sin cambio.
6. **Calculadora de piedra bola:** la nueva usa los **120 a 150 kg por m²** de su FAQ (piedra mediana, capa de 8 a 10 cm). ¿Está bien? ¿Cuánto para chica y grande? Si no, se quita la calculadora de esa página.
7. **Opiniones:** "Ricardo O." (condominio, Altamira) y "Laura P." (Madero) en tierra negra; "Patricia H." (Tampico) y "David M." (hotel, Altamira) en piedra bola. ¿Son reales y hay permiso para publicarlas con nombre? Mientras no, se retiran.
8. **Redondeo de la calculadora:** main da 0.8 m³ para 7 m² con capa de 10 cm (debería ser 0.7) por un detalle de cálculo; sobrestima a lo más 0.1 m³. ¿Lo dejamos igual que hoy o lo corregimos?
9. **Factura:** tierra negra decía "factura CFDI para compras a partir de cierto volumen". ¿Hay un monto mínimo para facturar materiales, o se factura cualquier compra?
10. **Instalación de mármol y tezontle:** main decía "Servicio de instalación disponible". ¿Lo ofrecen? ¿Con qué precio o "según cotización"?
11. **"Sin mínimo"** en costales de tierra, tezontle y sacos de mármol, y entrega por costal a domicilio: ¿se confirma? ¿Hay un mínimo para llevarlo a domicilio?
12. **Precios con IVA:** ¿$90, $1,500 y $200 incluyen IVA? (El pasto sí lo dice; en materiales no se publica hasta confirmarlo.)
13. **Fotos:** las de tezontle miden de 194 a 259 px y se ven borrosas; tezontle y piedra bola no tienen foto de portada; el saco de mármol es la única foto de producto. ¿Entran en la sesión de fotos (tezontle en sendero, piedra bola por medida, costales de tierra y tezontle)? Agregarlas o cambiarlas requiere tu permiso (regla de fotos).
