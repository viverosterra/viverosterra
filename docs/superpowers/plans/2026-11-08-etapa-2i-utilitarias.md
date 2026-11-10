# Etapa 2i · Utilitarias: políticas, privacidad, gracias, cuestionario, datos de envío, protocolo, vivero y 404 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Último sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2i; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §3.5, §5, §8, §10, §11). Las 7 páginas que siguen hechas a mano fuera del blog —`/politicas`, `/politica-privacidad`, `/gracias`, `/cuestionario`, `/datos-envio`, `/protocolo-cuidados-pasto-san-agustin`, `/vivero-tampico`— salen de cuatro plantillas nuevas de `tools/site` (`legal`, `formulario`, `protocolo`, `vivero`) y se crea `public/404.html` con una quinta (`no_encontrada`). Con eso ninguna página fuera del blog carga Google Fonts, `tailwind.css`, `design-system.css`, `servicios.css`, `legacy-fixes.css` ni `<style>` propios, y se retiran `tools/servicios` y `servicios.css`. La Tarea 13, que corre **solo cuando 2h ya esté en `main`**, borra los CSS viejos que aún necesitan los 53 archivos del blog y cierra la Etapa 2.

**Architecture:** Igual que 2a–2g: `contenido/<pagina>.py` expone `CONTENIDO` y `PARIDAD`; la plantilla arma la página; `generar.UTILITARIAS` registra las filas; `build.py` las escribe con el shell solo si cambian. Lo nuevo:
1. **`tools/site/componentes_util.py`:** cabecera sin etiqueta de precio, documento legal con índice y anclas, y controles reales (`<label for>` y `<fieldset>`/`<legend>`). El contenido describe cada control como dato (`campo()`, `opciones()`, `fila()`, `condicional()`) porque `test_contenido.py` solo admite HTML en línea; `dibujar()` lo vuelve HTML.
2. **`tools/site/paridad_util.py`:** congela, antes de tocar nada, las fotos del `<main>`, las anclas, los controles en orden (el dueño recibe esos `name`/`value` por correo; `datos-envio` arma con esos `id` el mensaje) y la medición de `/gracias`.
3. **JavaScript propio, sin reescribir la lógica:** `vt-cuestionario.js` (el asistente y el `fetch` de main, con dos arreglos), `vt-datos-envio.js` (el script de main casi literal: el texto de WhatsApp, sus emojis y el bloque `#VT1` no cambian) y `vt-404.js` (filtro de servicios).
4. **CSS:** `public/css/terra-util.css` (hoja propia con hash, como `terra-precios.css`, cableada en `activos.FUENTES`, `partials.head(util=True)`, `shell.UTIL` y `vercel.json`). `terra.css` no se toca: le quedan 35 B de presupuesto.
5. **404:** Vercel sirve `public/404.html` en toda ruta sin archivo (guía oficial "custom 404 page"; hoy responde 79 B de texto plano). La guía no dice qué código devuelve: se comprueba en la vista previa (Tarea 12, Step 7), con la alternativa escrita si no fuera 404.

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en las pruebas de navegador (todo envío a `formsubmit.co` y a `wa.me` se intercepta: **ninguna prueba manda un correo real**); CSS plano; JavaScript sin dependencias; `node --test` sin `package.json`; Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2i` (rama `feat/etapa-2i`, creada desde `main` en `db6923e`, con este plan como primer commit). Nunca en `~/Documents/GitHub/viverosterra` (iCloud). No dependas de `feat/etapa-2h` ni la toques (está en `~/dev/viverosterra-e2h` esperando revisión del dueño).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- **Qué se probó y qué no.** Se prototipó sobre `db6923e` en una copia fuera del repo con **todo el código de las Tareas 1–10 tal como está aquí**: paridad en `ok` en las seis categorías de las 7 páginas, `test_util_reglas` (y comprobado contra los HTML de `main`: 1 a 14 fallas por página), las pruebas de cada plantilla, las 15 de navegador (axe sin serias en las 8, sin desbordar de 320 a 1920, cuestionario contra un `formsubmit` falso, datos de envío contra un `wa.me` falso), las suites completas y el build reproducible; contadores abajo. **La Tarea 13 también se ensayó**, en otra copia: fusión real con `feat/etapa-2h`, resolución de sus 7 choques, borrado de los CSS y suites. **No se pudo probar:** el comportamiento real de Vercel con `404.html` (sin despliegue), el correo real de formsubmit con el campo `_honey` por `/ajax/`, ni la configuración de eventos clave de GA4 (no hay acceso a la cuenta).
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests` (≈ 5 min), `cd tools/pasto && python3 -m unittest discover -s tests -t .` y `node --test public/js/tests/*.test.js`. `tools/servicios` se borra en la Tarea 9 y su suite desaparece.
- Cuando una tarea agrega `terra-util.css`, el build publica su copia con hash y `tools/site/activos.json` gana una clave: se versiona (`git add public tools/site/activos.json`) revisando antes `git status --short | grep -v '\.html$'`.
- **Reglas del dueño en juego** (las prueban `test_reglas.py`, `test_consistencia.py` y la nueva `test_util_reglas.py`):
  - **`terra.css` no se toca.** Todo CSS nuevo va en `terra-util.css`, bajo `.vt-util`, con los tokens de `terra.css`.
  - **Precios solo de `datos.PRECIOS`** (fletes y mínimos nacionales de `tools/pasto/data.py`; mensualidades de `tools/pasto/mensualidades.py`). Los rangos de inversión del cuestionario son respuestas del cliente, no precios: se quedan literales porque son `value` que el dueño recibe.
  - **Fotos exactamente las de producción**, mismas y en el mismo orden (3 en total: cuestionario, protocolo y vivero); se corrigen solo `width`/`height`, que en main decían 1920×1080 cuando los archivos miden 1400×787 y 1024×1536. No se rota ninguna (pregunta 6).
  - **Texto legal:** se conserva la sustancia, sin inventar compromisos; solo se aplican las correcciones C1–C11. El marco legal citado en el aviso de privacidad **no se edita** (ver L1).
  - **Pago** = anticipo (`datos.ANTICIPO`), nunca 100% por adelantado, nunca "pagas al ver terminado" y ninguna frase sobre "liquidar el saldo" (`test_reglas.SALDO_RE`). **PROFECO:** contado (transferencia, efectivo o tarjeta en una sola exhibición) es el precio más bajo, sin la palabra "recargo"; en mensualidades, total y monto de cada mensualidad.
  - **Garantías:** plantas 30 días con condiciones; arraigo de pasto `datos.ARRAIGO`; la única frase con "sin costo" es la de `datos.GARANTIA_PASTO`. **Visita** nunca gratis: toda página que la menciona lleva `datos.VISITA_COSTO` o `VISITA_COSTO_CORTO`. **Materiales:** `datos.CONDICIONES_MATERIALES` (sin mínimo, entrega por viaje, todo se factura).
  - Sin "gratis" ni "sin costo" fuera de la garantía aprobada, sin "Oasis", sin el nombre del proveedor de la terminal, sin "MSI", sin "experto", sin "+18 años", sin "productor directo", sin "en stock".
- **Formularios:** `cuestionario` no cambia `action`, `method`, `name` ni `value` (`test_campos_del_cuestionario_iguales_a_main_mas_honeypot`). **Nunca** hagas un envío real a formsubmit desde una prueba o a mano: el dueño recibe esos correos.
- **`/gracias`** conserva archivo, URL, título, robots, canonical y `data-cta` (`test_gracias_mide_igual_que_main`). Dos textos de CTA como en 2a–2g, más "Adelantar por WhatsApp" (hoja de ruta) y "También puedes escribirnos por WhatsApp" (el aviso del cuestionario).

## Cobertura del spec y de la hoja de ruta

| Pide el spec / la hoja de ruta / el dueño | Dónde |
|---|---|
| Hoja de ruta 2i: plantilla `legal` con anclas estables, incluida `#garantia-pasto` | Tarea 4; `test_legal.test_anclas_que_enlazan_otras_paginas`; `paridad_util` congela las 7 de main |
| Hoja de ruta 2i: plantilla `formulario` (labels en todos los controles, `noindex`, formsubmit a `viverosterra@hotmail.com`, gracias con promesa única y "Adelantar por WhatsApp") | Tareas 5–7; `test_cuestionario.test_todo_control_visible_tiene_nombre_accesible`, `test_datos_envio.test_cada_control_con_su_label` |
| Hoja de ruta 2i: plantilla `protocolo` con HowTo visible | Tarea 8 (etapas por días; sin JSON-LD `HowTo` nuevo, ver Correcciones) |
| Hoja de ruta 2i: `404` con menú, buscador de servicios y CTA | Tarea 10 |
| `/vivero-tampico` pasa de 2g a 2i y se retira `tools/servicios` | Tarea 9 |
| Spec §5.2 tabla: `gracias/` con promesa única | Tarea 5 (resumen de lo calculado: ver Correcciones) |
| Spec §3.5: cuestionario `noindex, follow`, canonical, un solo H1 | Tarea 6, `PARIDAD["meta"]` |
| Cierre de la Etapa 2: borrar CSS viejos con prueba que falle si alguna página los referencia; quitar `migrar_shell.py`; "toda página sale de `generar.PAGINAS`"; Lighthouse A11y ≥ 98; capturas | Tarea 13 (bloqueada por 2h) y Tarea 12 |
| Dueño: política sin contradicciones | Tabla C, Tarea 4 |
| Pruebas de lote: axe, sin desbordar 320–1920, consola limpia, CLS, Lighthouse, capturas | Tareas 11 y 12 |
| Puertas (spec §11): diseño, CRO, cumplimiento y SEO/AEO (se toca JSON-LD de vivero) | Tarea 12 |

Fuera de 2i: títulos y consolidación (Etapa 3), grafo JSON-LD único y `@id #negocio` en vivero (Etapa 4), `llms.txt` generado (Etapa 4; aquí solo se corrige una palabra, C3), redirect `/politica-de-privacidad → /` (Etapa 3, L4), borrar imágenes huérfanas (ver Inventario).

## Inventario de producción (`db6923e`)

| Página (ruta exacta) | Archivo | Sale de | Estilos viejos | Scripts propios | Formulario / medición |
|---|---|---|---|---|---|
| `/politicas` | `public/politicas/index.html` | a mano (solo shell) | Google Fonts, `design-system`, `tailwind`, `legacy-fixes`, `<style>` | menú y acordeón muertos; `sendWA` | ninguno; `utilidad:cuerpo` ×3 |
| `/politica-privacidad` | `public/politica-privacidad/index.html` | a mano | Google Fonts, `design-system`, `<style>` | — | `utilidad:cuerpo` |
| `/gracias` | `public/gracias/index.html` | a mano | Google Fonts, `design-system`, `<style>` | — | destino `_next` de 6 formularios |
| `/cuestionario` | `public/cuestionario.html` | a mano | `design-system`, 13 KB de `<style>` | asistente en línea, `onclick` | `POST https://formsubmit.co/ajax/viverosterra@hotmail.com`; 74 controles |
| `/datos-envio` | `public/datos-envio/index.html` | a mano | Google Fonts, `<style>` | script en línea, `onclick`, `onchange` | sin `form`; WhatsApp con `#VT1` |
| `/protocolo-cuidados-pasto-san-agustin` | `public/protocolo-cuidados-pasto-san-agustin.html` | a mano | Google Fonts, `design-system`, 8 KB de `<style>` | — | `posventa:*` |
| `/vivero-tampico` | `public/vivero-tampico/index.html` | `tools/servicios` (hero) | Google Fonts, `design-system`, `tailwind`, `servicios`, `legacy-fixes`, `<style>` | acordeón y `reveal` | `vivero:*` |
| (404) | no existe `public/404.html` | Vercel | — | — | 79 B de texto plano |

Anclas que otras páginas enlazan: `/politicas#mensualidades` (17), `#garantia-plantas` (13), `#devoluciones` (9); `/politicas` y `/politica-privacidad` desde el pie de las 108.

**Tres cosas distintas de lo que dice el encargo:**
- **`/gracias` no dispara ningún evento de GA4.** Solo tiene `gtag('config', …)` (cero `gtag('event'`). La página cuenta por su URL y su `page_view`. El evento clave del spec (§ medición) es `generate_lead`, y lo mandan las páginas de origen al enviar (`vt-b2b.js`, `method: "formulario"`). Se preserva exactamente eso.
- **`/cuestionario` no llega a `/gracias`, no manda `generate_lead` y no tiene honeypot.** Envía por `fetch` a `/ajax/` y muestra el aviso en la misma página; lleva `_captcha=false` y sin `_honey`. Solo los 6 formularios de empresas y materiales usan `_next`. El plan agrega `_honey` y conserva el resto (pregunta 4).
- **El `sendWA` de `/politicas` es código muerto:** se define y nadie lo llama. Se va. Ninguna de las 8 páginas abre WhatsApp con `window.open`.

**Bugs de main que se arreglan al migrar el cuestionario:** dos `<h1>` y un `</div>` huérfano; los campos obligatorios viven en el paso 1, oculto al enviar, así que el navegador bloquea el envío sin avisar; Enter a media captura dispara el envío; `<label>` sin `for`.

**Estilos viejos después de esta etapa.** Sobre `main` sin 2h, `tailwind.css`, `design-system.css` y `legacy-fixes.css` siguen vivos porque los usan los 53 archivos del blog (55 con `/politicas` y `/vivero-tampico`; 59 con `design-system`). **`legacy-fixes.css` no se puede retirar en esta rama.** `servicios.css` sí: su única usuaria es vivero. Por eso la retirada va en la Tarea 13, condicionada. **Fotos sin referencia:** ~119 archivos de `public/img` (≈ 22.5 MB) no aparecen en ninguna página ni en `tools`; no se borran aquí (regla de fotos y el blog cambia con 2h): va en una lista para la Etapa 5.

## Correcciones a las políticas: contradicciones encontradas y su arreglo

Fuente: `public/politicas/index.html`, `public/politica-privacidad/index.html`, `public/llms.txt`, contra `datos.py` y las reglas del dueño.

| # | Dónde | Dice hoy | Contra qué | Arreglo |
|---|---|---|---|---|
| C1 | `/politicas`, meta description | "devoluciones (30 días)" | Su propio texto y toda la tienda: 7 días naturales | "devoluciones (7 días)"; `PARIDAD["meta"]` (pregunta 2) |
| C2 | `#garantia-plantas` | "la reponemos sin costo" | Solo la garantía de pasto puede decir "sin costo" | "la reponemos" (pregunta 3) |
| C3 | `#garantia-plantas` y `llms.txt:63` | "asesoría gratis" | Sin "gratis" | "te orientamos por WhatsApp para que prendan" |
| C4 | `#mensualidades` | "te mostramos el total" | PROFECO del dueño: total y mensualidad | "el total y el monto de cada mensualidad" |
| C5 | `#facturacion` | "transferencia bancaria y link de pago" | `#mensualidades`: "transferencia, efectivo o tarjeta" | Agrega efectivo y "la tarjeta en una sola exhibición paga el precio de contado" |
| C6 | `#envios` y `#facturacion` | "una vez confirmado el pago", "se embarca al confirmarse el pago" | Nunca 100% por adelantado | `datos.ANTICIPO`, "después de confirmar tu pedido" y "La fecha de embarque te la confirmamos por WhatsApp" (pregunta 1) |
| C7 | `#envios` | "3 a 5 días hábiles (1–2 de preparación + 3–5 de traslado)": suma 4 a 7 | Las ciudades: sale en 1 a 2 y llega de 3 a 5 | La frase de `contenido/ciudad.py` |
| C8 | `/politicas` | La garantía de pasto solo enlaza al protocolo | Arraigo 15–20 días; hoja de ruta pide `#garantia-pasto` | Sección nueva con `datos.GARANTIA_PASTO` y las 5 condiciones del protocolo, palabra por palabra |
| C9 | `#privacidad` | Datos "únicamente" para el pedido, "solo" para seguimiento | El aviso integral lista promociones como finalidad secundaria | Resumen alineado, enlace al aviso integral |
| C10 | Aviso integral §3 | Solo SAT, WhatsApp Business y autoridades | Hay paquetería (lo dice `/politicas`), formsubmit y cobro con tarjeta | Se agregan sin nombrar a la terminal (pregunta 5) |
| C11 | `/politicas` | Nada de materiales ni "todas las compras se pueden facturar" | Reglas del dueño | `datos.CONDICIONES_MATERIALES` en `#envios`; `datos.FACTURACION` en `#facturacion` |

No son contradicciones pero se quitan: "Transparencia total para tu compra" (adjetivo sin dato). **Se conservan, aunque parezcan rozar reglas:** "sujetos a disponibilidad" y "si no hay existencia" en cambios y reposición, porque son condición legal de un cambio, no oferta comercial.

**Para el abogado del dueño (no se editan):**
- **L1.** El aviso cita la LFPDPPP "publicada el 5 de julio de 2010", "los lineamientos del INAI" y el "artículo 32". Hasta donde sé, en marzo de 2025 se publicó una ley nueva y el INAI dejó de existir; artículo y autoridad pueden haber cambiado. Hay que confirmarlo.
- **L2.** Cargo de reposición del 10% y envío de retorno a cargo del cliente: se conservan; vale la pena revisarlos contra la LFPC.
- **L3.** El aviso dice que las cookies de GA4 "son anónimas": no se cambia, revisar.
- **L4.** `/politica-de-privacidad` redirige con 301 a `/` y no a `/politica-privacidad`: Etapa 3.

**También en páginas vecinas:** `/vivero-tampico` publica "Lun–Sáb 9am–6pm" (el sábado cierra a las 14 h), "+18 años", "Variedades en stock", "te decimos si la tenemos disponible", "Preguntar disponibilidad", "precios orientativos", "precios más bajos/accesibles", "precios preferenciales" y "Productor directo": todo fuera. El protocolo dice "repone sin costo adicional" (pasa a la frase aprobada), "Consultar con experto", "18 años" y dos `<h1>`. Fuera de 2i pero anotado para el PR: la tienda (`ficha.py`, `ciudad.py`, `tienda.py`, `data.py`) sigue diciendo "después de confirmar el pago" (pregunta 1).

## Decisiones de diseño (y por qué)

- **Cinco plantillas, una hoja.** `legal` y `formulario` no tienen etiqueta de precio porque no venden: la jerarquía es H1 grande, kicker con la fecha y texto a 68 caracteres; la cabecera `portada` se reserva a vivero, que sí es una página de venta local. `terra-util.css` queda en ≈ 7.0 KB minificada y ≈ 1.8 KB con gzip.
- **Política legible como documento:** índice fijo a la izquierda en escritorio (en celular, enlaces que envuelven), con `scroll-margin-top` porque el menú es fijo. Los `id` de `<section>` son las anclas de main.
- **Cuestionario:** se conservan los 5 pasos, los textos y los valores. El `hidden` va en el HTML para evitar el salto de contenido; un paso con `display:grid` necesita que `.vt-util [hidden]` vaya al final de la hoja (prueba `test_hidden_gana_a_las_reglas_con_display`). La barra de progreso anima `transform`, no `width`.
- **`/gracias` sin resumen de lo calculado** (ver Correcciones) y sin scripts propios: `terra.js` mide el botón por `data-cta`.
- **Datos de envío:** el `.js` conserva el script de main; solo cambia `style.display` por `hidden` y `onclick` por `addEventListener`.
- **Vivero:** sin tarjetas con foto en categorías porque main no tenía fotos ahí y la regla impide agregar. El JSON-LD conserva sus nodos (Etapa 4 los unifica), con el horario de `datos.HORARIO_LD` y sin "18 años".
- **Protocolo sin JSON-LD `HowTo`:** main no lo tenía; el rich result de HowTo ya no se muestra en Google y el grafo es de la Etapa 4. Se cumple "HowTo visible" con las etapas por días.
- **Fechas:** `/politicas` "Actualizado noviembre 2026" y aviso "noviembre de 2026", porque el texto cambia y el propio aviso obliga a poner la fecha de modificación. Cuestionario y protocolo no cambian de contenido legal: el cuestionario conserva su fecha; el protocolo la pierde con los contadores repetidos.

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/{politicas,politica-privacidad,gracias,cuestionario,datos-envio,protocolo-cuidados-pasto-san-agustin,vivero-tampico}.json` y `404.json` | Lo que publicaba cada página (`paridad.py capturar`; el 404 es una captura vacía). |
| `tools/site/paridad_util.py`, `tools/site/tests/paridad/utilitarias-contrato.json` | Fotos, anclas, controles y medición de main. |
| `tools/site/componentes_util.py` | Cabecera, documento legal, controles. |
| `tools/site/plantillas/{legal,formulario,protocolo,vivero,no_encontrada}.py` | Las plantillas nuevas. |
| `tools/site/contenido/{politicas,politica_privacidad,gracias,cuestionario,datos_envio,protocolo,vivero,no_encontrada}.py` | Solo datos. |
| `public/css/terra-util.css` | Hoja de las utilitarias. |
| `public/js/{vt-cuestionario,vt-datos-envio,vt-404}.js` | Comportamiento de cuestionario, envío y 404. |
| `tools/site/tests/{test_util_reglas,test_componentes_util,test_terra_util_css,test_legal,test_gracias,test_cuestionario,test_datos_envio,test_protocolo,test_vivero,test_no_encontrada,test_util_navegador}.py` | Pruebas nuevas. |

Se modifican: `tools/site/{activos,partials,shell,paginas,generar,mensajes_paginas}.py`, `vercel.json`, `tools/site/ci/sitio.yml`, `public/sitemap.xml`, `public/llms.txt`; pruebas `test_activos`, `test_generar`, `test_vercel`, `test_sitio`, `test_migrar_shell`, `test_legacy_fixes`, `test_limpieza`. Se borran: `tools/servicios/` y `public/css/servicios.css`. Regenerados por el build: las 8 páginas, `public/css/terra-util.<hash>.css` y `tools/site/activos.json`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar el worktree**

```bash
cd ~/dev/viverosterra-e2i && git branch --show-current && git log --oneline -2
```

Expected: `feat/etapa-2i`; arriba el commit de este plan (`docs(plan): etapa 2i utilitarias`) y debajo `db6923e merge: etapa 2g — zonas y lista de precios con plantillas`. Si `main` avanzó, trabaja de todos modos sobre esa base y deja la integración para la Tarea 12.

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 48 páginas escritas`, `shell: 0 de 108 páginas actualizadas`, `0`, `OK` en las tres suites de Python y `ℹ fail 0`. Si algo falla en `main`, para y repórtalo: no es de esta rama.

### Task 1: Capturas de paridad y contrato de formularios

**Files:** crear `tools/site/paridad_util.py`, `tools/site/tests/paridad/*.json`.

- [ ] **Step 1: Herramienta de contrato**

Crea `tools/site/paridad_util.py`:

```python
"""Paridad de lo que paridad.py no ve en las páginas utilitarias (Etapa 2i): fotos del <main> en orden, anclas (id de
h2 y section), campos de formulario (el dueño recibe esos nombres y valores por correo; datos-envio arma con esos id el
mensaje de WhatsApp) y la medición de /gracias (GA4 la cuenta por su URL y su page_view: no hay evento propio).

Uso: python3 tools/site/paridad_util.py capturar   (escribe tests/paridad/utilitarias-contrato.json)
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

RUTAS = ("/politicas", "/politica-privacidad", "/gracias", "/cuestionario", "/datos-envio",
         "/protocolo-cuidados-pasto-san-agustin", "/vivero-tampico")
CAPTURA = paridad.CAPTURAS / "utilitarias-contrato.json"
ANCLA_RE = re.compile(r'<(?:h2|section)\b[^>]*\sid="([^"]+)"')
FORM_RE = re.compile(r'<form\b[^>]*\baction="([^"]*)"[^>]*\bmethod="([^"]*)"')
GTAG_CONFIG = "gtag('config','"


class _Campos(HTMLParser):
    """Controles del documento en orden: [etiqueta, id, name, type, value, required] y el texto de cada <option>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.campos, self._opcion = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("input", "select", "textarea"):
            self.campos.append([tag, a.get("id"), a.get("name"), a.get("type"), a.get("value"), "required" in a])
        elif tag == "option":
            self._opcion = [a.get("value"), ""]
            self.campos.append(["option", self._opcion])

    def handle_data(self, data):
        if self._opcion is not None:
            self._opcion[1] += data

    def handle_endtag(self, tag):
        if tag == "option":
            self._opcion[1] = self._opcion[1].strip()
            self._opcion = None


def campos(html):
    p = _Campos()
    p.feed(paridad.principal(html))
    return p.campos


def anclas(html):
    return sorted(set(ANCLA_RE.findall(paridad.principal(html))))


def medicion(html):
    return {"gtag_config": html.count(GTAG_CONFIG), "gtag_event": html.count("gtag('event'"),
            "data_cta": sorted(set(re.findall(r'data-cta="(utilidad:[a-z]+)"', paridad.principal(html))))}


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    m = FORM_RE.search(paridad.principal(html))
    return {"fotos": paridad_materiales.fotos(html), "anclas": anclas(html), "campos": campos(html),
            "form": list(m.groups()) if m else None, "medicion": medicion(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_util.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), len(d["anclas"]), len(d["campos"]), d["form"], d["medicion"])
```

- [ ] **Step 2: Capturar sobre las páginas de main (antes de tocar ninguna)**

```bash
cd ~/dev/viverosterra-e2i/tools/site
for r in /politicas /politica-privacidad /gracias /cuestionario /datos-envio /protocolo-cuidados-pasto-san-agustin /vivero-tampico; do python3 paridad.py capturar $r | tail -1; done
python3 paridad_util.py capturar
printf '{\n "meta": {},\n "jsonld_tipos": [],\n "encabezados": [],\n "faq": [],\n "precios": [],\n "enlaces": []\n}\n' > tests/paridad/404.json
```

Expected del último comando de captura: `/politicas 0 7 0 None {…}`, `/politica-privacidad 0 0 0 None`, `/gracias 0 0 0 None`, `/cuestionario 1 0 74 ['https://formsubmit.co/ajax/viverosterra@hotmail.com', 'POST']`, `/datos-envio 0 0 29 None`, `/protocolo-… 1 0 0 None`, `/vivero-tampico 1 0 0 None`; en todas `'gtag_config': 1, 'gtag_event': 0`. `404.json` va vacía porque la página no existía.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/paridad_util.py tools/site/tests/paridad
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas y contrato de las páginas utilitarias antes de migrar" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Reglas de las utilitarias en rojo

**Files:** crear `tools/site/tests/test_util_reglas.py`.

- [ ] **Step 1: Escribir la prueba**

Crea `tools/site/tests/test_util_reglas.py`:

```python
"""Reglas del dueño en las páginas utilitarias (Etapa 2i): sin CSS viejo ni Google Fonts, las mismas fotos, anclas y campos
de main, medición de /gracias intacta y las correcciones de políticas y privacidad (tabla C del plan).

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea saca las suyas) y al
cerrar la Etapa 2i queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paridad  # noqa: E402
import paridad_util  # noqa: E402

CONTRATO = json.loads(paridad_util.CAPTURA.read_text(encoding="utf-8"))
PENDIENTES = frozenset({"/politicas", "/politica-privacidad", "/gracias", "/cuestionario", "/datos-envio",
                        "/protocolo-cuidados-pasto-san-agustin", "/vivero-tampico"})
PAGINAS = tuple(CONTRATO)
GARANTIA_PASTO = "la reponemos sin costo"  # la única frase con "sin costo" que aprobó el dueño
VIEJOS = r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)|<style\b|function sendWA|window\.open"
GENERALES = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b|\bsin cargo\b"),
    ("marca o término prohibido", r"\bOasis\b|\bMSI\b|sin intereses|meses sin|(?<![-.\w])clip(?![-\w:(])"),
    ("pago al terminar", r"\bpagas\s+(?:cuando|al\s+ver)\b|100% por adelantado(?<!No pedimos el 100% por adelantado)"),
    ("sin respaldo", r"\bexpertos?\b|\b18 años\b|\+18\b|\ben stock\b|precios orientativos|productor(?:es)? direct"
                     r"|precios? (?:m[aá]s bajos|m[aá]s accesibles|preferenciales)"),
)
ESPECIFICAS = {
    "/politicas": (
        ("devolución en la meta", lambda h: "devoluciones (7 días)" in h and "(30 días)" not in h),
        ("anticipo", lambda h: datos.ANTICIPO in h and "al confirmarse el pago" not in h),
        ("total y mensualidad antes del link", lambda h: "el total y el monto de cada mensualidad" in h),
        ("efectivo y precio de contado con tarjeta", lambda h: "transferencia bancaria, efectivo" in h
         and "una sola exhibición paga el precio de contado" in h),
        ("tiempo de entrega coherente", lambda h: "1–2 días de preparación" not in h and "1 a 2 días hábiles" in h),
        ("garantía de pasto con ancla", lambda h: 'id="garantia-pasto"' in h and datos.ARRAIGO in h and "antes del día 21" in h),
        ("materiales y factura", lambda h: datos.CONDICIONES_MATERIALES in h and datos.FACTURACION in h),
        ("privacidad igual al aviso integral", lambda h: "promociones" in h and 'href="/politica-privacidad"' in h),
        ("sin Transparencia total", lambda h: "Transparencia total" not in h),
    ),
    "/politica-privacidad": (
        ("transferencias reales", lambda h: "Paqueterías" in h and "procesador de pagos con tarjeta" in h),
    ),
    "/vivero-tampico": (
        ("horario real del sábado", lambda h: "Lun–Sáb" not in h and "9am–6pm horario" not in h),
        ("sin existencias", lambda h: "disponibilidad" not in paridad.texto(paridad.principal(h))),
    ),
    "/protocolo-cuidados-pasto-san-agustin": (
        ("garantía con la frase aprobada", lambda h: "la reponemos sin costo" in h and "sin costo adicional" not in h),
    ),
    "/gracias": (("promesa única", lambda h: datos.PROMESA_COMPLETA.split(" · ")[0] in h and "Adelantar por WhatsApp" in h),),
    "/cuestionario": (
        ("un solo H1", lambda h: len(re.findall(r"<h1\b", h)) == 1),
        ("honeypot", lambda h: 'name="_honey"' in h),
        ("visita con costo", lambda h: datos.VISITA_COSTO_CORTO in h),
    ),
}


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def visible(html):
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    return f"{paridad.texto(paridad.principal(html))} {metas}"


def fallas(ruta):
    html, salida = html_de(ruta), []
    if re.search(VIEJOS, html):
        salida.append(f"viejo: {re.search(VIEJOS, html).group(0)}")
    texto = visible(html).replace(GARANTIA_PASTO, "")
    for regla, patron in GENERALES:
        for m in re.finditer(patron, texto, re.I):
            salida.append(f"{regla}: …{texto[max(0, m.start() - 30):m.end() + 30]}…")
    salida += [regla for regla, ok in ESPECIFICAS.get(ruta, ()) if not ok(html)]
    actual, antes = paridad_util.extraer(ruta), CONTRATO[ruta]
    if actual["fotos"] and [f["src"] for f in actual["fotos"]] != [f["src"] for f in antes["fotos"]]:
        salida.append("fotos distintas de main")
    salida += [f"ancla perdida: {a}" for a in antes["anclas"] if a not in actual["anclas"]]
    return salida


class UtilitariasReglasTest(unittest.TestCase):
    def test_migradas_cumplen(self):
        for ruta in PAGINAS:
            if ruta in PENDIENTES:
                continue
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_siguen_fallando(self):
        for ruta in PENDIENTES:
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_gracias_mide_igual_que_main(self):
        """GA4 cuenta /gracias por su URL y su page_view: una sola configuración, ningún evento propio, mismo data-cta."""
        actual, antes = paridad_util.extraer("/gracias"), CONTRATO["/gracias"]
        self.assertEqual(actual["medicion"], antes["medicion"])
        self.assertEqual(actual["medicion"], {"gtag_config": 1, "gtag_event": 0, "data_cta": ["utilidad:cuerpo"]})

    def test_campos_del_cuestionario_iguales_a_main_mas_honeypot(self):
        quitar_id = lambda c: c if c[0] == "option" else [c[0], c[2], c[3], c[4], c[5]]  # noqa: E731
        antes = [quitar_id(c) for c in CONTRATO["/cuestionario"]["campos"]]
        actual = [quitar_id(c) for c in paridad_util.extraer("/cuestionario")["campos"] if c[2:3] != ["_honey"]]
        self.assertEqual(actual, antes)
        self.assertEqual(paridad_util.extraer("/cuestionario")["form"], CONTRATO["/cuestionario"]["form"])

    def test_controles_de_datos_de_envio_iguales_a_main(self):
        ids = lambda campos: [c[1] for c in campos if c[0] != "option"]  # noqa: E731
        self.assertEqual(ids(paridad_util.extraer("/datos-envio")["campos"]), ids(CONTRATO["/datos-envio"]["campos"]))

    def test_las_noindex_siguen_noindex(self):
        for ruta in ("/gracias", "/cuestionario", "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertRegex(html_de(ruta), r'<meta name="robots" content="noindex, (?:no)?follow">')


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Comprobar que las 7 páginas fallan por lo que deben**

```bash
cd ~/dev/viverosterra-e2i/tools/site
python3 -m unittest tests.test_util_reglas 2>&1 | tail -3
python3 -c "
import sys; sys.path[:0]=['.','tests']
import test_util_reglas as t
for r in t.PAGINAS: f=t.fallas(r); print(r, len(f), f[:2])"
```

Expected: `OK` (6 pruebas: todas las páginas siguen en `PENDIENTES`) y fallas por página: `/politicas` 11, `/politica-privacidad` 2, `/gracias` 1, `/cuestionario` 4, `/datos-envio` 1, protocolo 5, `/vivero-tampico` 14.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/tests/test_util_reglas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(reglas): reglas del dueño y contrato de las utilitarias, con pendientes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: `terra-util.css`, su cableado y `componentes_util.py`

**Files:** crear `public/css/terra-util.css`, `tools/site/componentes_util.py`, `tools/site/tests/{test_componentes_util,test_terra_util_css}.py`; modificar `tools/site/{activos,partials,shell,paginas,generar,mensajes_paginas}.py`, `vercel.json`, `tools/site/tests/{test_activos,test_vercel,test_generar}.py`.

- [ ] **Step 1: Pruebas en rojo**

Crea `tools/site/tests/test_componentes_util.py`:

```python
"""Componentes de las utilitarias: etiquetas unidas a su control, grupos con fieldset y documento legal con anclas."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_util as cu  # noqa: E402
import datos  # noqa: E402


class ComponentesUtilTest(unittest.TestCase):
    def test_campo_une_label_y_control(self):
        html = cu.dibujar(cu.campo({"label": "Nombre", "name": "nombre", "id": "nombre", "tipo": "text", "requerido": True}))
        self.assertIn('<label for="nombre">Nombre', html)
        self.assertIn('id="nombre" name="nombre" required', html)

    def test_campo_sin_name_conserva_el_id(self):
        html = cu.dibujar(cu.campo({"label": "Calle", "id": "calle", "tipo": "text", "error": "Escribe la calle."}))
        self.assertNotIn("name=", html)
        self.assertIn('<p class="msg">Escribe la calle.</p>', html)

    def test_lista_con_valor_vacio_y_opciones_sin_value(self):
        html = cu.dibujar(cu.campo({"label": "Origen", "name": "o", "tipo": "lista", "opciones": (("", "Elegir"), (None, "Google"))}))
        self.assertIn('<option value="">Elegir</option><option>Google</option>', html)

    def test_grupo_con_legend_y_valor_distinto_del_texto(self):
        html = cu.dibujar(cu.opciones({"legend": "Uso", "tipo": "checkbox", "name": "uso", "items": (("Juego de niños", "Niños"),)}))
        self.assertIn("<fieldset", html)
        self.assertIn("<legend>Uso</legend>", html)
        self.assertIn('<input type="checkbox" name="uso" value="Juego de niños"><span>Niños</span>', html)

    def test_opcion_con_atributos_extra(self):
        html = cu.dibujar(cu.opciones({"legend": "T", "tipo": "radio", "name": "t", "items": (("Otro", "Otro", (("id", "rb"),)),)}))
        self.assertIn('value="Otro" id="rb">', html)

    def test_documento_legal_con_indice_y_anclas(self):
        html = cu.documento_legal(({"id": "envios", "titulo": "Política de Envíos", "corto": "Envíos",
                                    "bloques": (("p", "Texto"), ("ul", ("a", "b")), ("ol", ("c",)), ("h3", "Sub"))},))
        self.assertIn('<a href="#envios">Envíos</a>', html)
        self.assertIn('<section id="envios"', html)
        for pieza in ("<p>Texto</p>", "<ul><li>a</li><li>b</li></ul>", "<ol><li>c</li></ol>", "<h3>Sub</h3>"):
            self.assertIn(pieza, html)

    def test_cabeza_con_foto_es_la_imagen_prioritaria(self):
        html = cu.cabeza({"kicker": "K", "h1": "T", "lede": "L", "foto": {"src": "/img/a.webp", "ancho": 10, "alto": 5, "alt": ""}})
        self.assertIn('fetchpriority="high"', html)
        self.assertIn('width="10" height="5"', html)
        self.assertIn('id="vt-h1"', html)

    def test_boton_con_texto_propio_firma_el_mensaje(self):
        html = cu.boton_wa_texto("Adelantar por WhatsApp", "Hola", "utilidad:cuerpo")
        self.assertIn('data-cta="utilidad:cuerpo"', html)
        self.assertIn("Adelantar por WhatsApp", html)
        self.assertIn(datos.wa_url(datos.con_firma("Hola")).replace("&", "&amp;"), html)


if __name__ == "__main__":
    unittest.main()
```

Crea `tools/site/tests/test_terra_util_css.py`:

```python
"""terra-util.css: hoja de las utilitarias (Etapa 2i). Todo bajo .vt-util, sin colores literales ni !important, solo
transform y opacity en movimiento y presupuesto propio (terra.css está a 35 B de su tope)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-util.css"


class TerraUtilCssTest(unittest.TestCase):
    def setUp(self):
        self.css = sin_comentarios(HOJA.read_text(encoding="utf-8"))

    def test_todo_selector_bajo_vt_util(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", self.css):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-util ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", self.css), [])
        self.assertNotIn("!important", self.css)

    def test_hidden_gana_a_las_reglas_con_display(self):
        """Va al final con la misma especificidad: los pasos, la orden y la suma tienen display propio."""
        ultimo = self.css.rindex(".vt-util [hidden]{display:none}")
        for regla in (".vt-util .vt-paso", ".vt-util .vt-util__orden{", ".vt-util .vt-util__suma{"):
            self.assertLess(self.css.index(regla), ultimo)

    def test_movimiento_solo_compositor(self):
        for transicion in re.findall(r"transition:([^;}]+)", self.css):
            if transicion.strip() == "none":
                continue
            propiedades = {t.strip().split()[0] for t in transicion.split(",")}
            self.assertLessEqual(propiedades, {"transform", "opacity", "background", "color"})

    def test_presupuesto(self):
        datos = activos.minificar_css(HOJA.read_text(encoding="utf-8")).encode("utf-8")
        self.assertLess(len(datos), 9 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 2 * 1024 + 512)


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_componentes_util tests.test_terra_util_css 2>&1 | tail -1
```

Expected: `FAILED (errors=2)` (no existen el módulo ni la hoja).

- [ ] **Step 2: La hoja**

Crea `public/css/terra-util.css`:

```css
/* terra-util.css: hoja de las páginas utilitarias (Etapa 2i: políticas, privacidad, gracias, cuestionario, datos de envío,
   protocolo, vivero y 404). Solo se carga en <body class="vt-pagina vt-util"> (shell.py); todo bajo .vt-util y con los
   tokens de terra.css. Editorial sobre papel: la cabecera sin etiqueta de precio y formularios de línea firme. */
.vt-util .vt-util__cabeza{padding:clamp(20px,3vw,40px) 0 clamp(24px,4vw,48px);border-bottom:1px solid var(--vt-line)}
.vt-util .vt-util__intro{display:grid;gap:24px;align-items:center}
.vt-util .vt-util__foto img{display:block;width:100%;height:clamp(150px,34vw,320px);object-fit:cover;border-radius:var(--vt-radius)}
@media (min-width:900px){.vt-util .vt-util__intro:has(.vt-util__foto){grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)}}
.vt-util .vt-util__estrecho{max-width:760px}
.vt-util .vt-util__lista{display:grid;gap:12px;margin:0 0 24px;padding-left:22px}
.vt-util .vt-util__adelanto{margin:0 0 12px;font-weight:600}
.vt-util .vt-legal{display:grid;gap:24px;padding-block:clamp(28px,4vw,56px)}
@media (min-width:1000px){.vt-util .vt-legal{grid-template-columns:230px minmax(0,1fr);gap:64px;align-items:start}.vt-util .vt-legal__indice{position:sticky;top:calc(var(--vt-head-h) + 24px)}}
.vt-util .vt-legal__indice ol{display:flex;flex-wrap:wrap;gap:4px 16px;margin:0;padding:0;list-style:none}
@media (min-width:1000px){.vt-util .vt-legal__indice ol{display:grid;gap:8px;border-left:2px solid var(--vt-line);padding-left:14px}}
.vt-util .vt-legal__indice a{display:inline-block;padding:6px 0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-util .vt-legal__texto{max-width:68ch}
.vt-util .vt-legal__texto section{scroll-margin-top:calc(var(--vt-head-h) + 16px);padding-block:0 32px}
.vt-util .vt-legal__texto section + section{border-top:1px solid var(--vt-line);padding-top:28px}
.vt-util .vt-legal__texto h2{margin:0 0 14px;font-size:clamp(1.45rem,1.2rem + 1vw,1.9rem);line-height:1.15}
.vt-util .vt-legal__texto h3{margin:20px 0 8px;font-size:var(--vt-text-lg)}
.vt-util .vt-legal__texto p{margin:0 0 12px;line-height:1.65}
.vt-util .vt-legal__texto ul,.vt-util .vt-legal__texto ol{display:grid;gap:8px;margin:0 0 14px;padding-left:20px;line-height:1.6}
.vt-util .vt-req{color:var(--vt-soil)}
.vt-util .vt-util__pista{margin:4px 0 0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-util .vt-util__form,.vt-util .vt-paso,.vt-util .vt-util__tarjeta{display:grid;gap:18px}
.vt-util .vt-paso h2{margin:0;font-size:clamp(1.4rem,1.2rem + .9vw,1.8rem)}
.vt-util .vt-paso h2:focus{outline:none}
.vt-util .vt-util__fila{display:grid;gap:16px}
@media (min-width:640px){.vt-util .vt-util__fila--2{grid-template-columns:repeat(2,minmax(0,1fr))}.vt-util .vt-util__fila--3{grid-template-columns:repeat(3,minmax(0,1fr))}}
.vt-util .vt-control input{font-size:16px;font-weight:500}
.vt-util .vt-control input[type="checkbox"]{flex:none}
.vt-util .vt-util__grupo{min-width:0;margin:0;padding:0;border:0}
.vt-util .vt-util__grupo legend{padding:0;margin-bottom:8px;font-size:var(--vt-text-sm);font-weight:600}
.vt-util .vt-pills{display:flex;flex-wrap:wrap;gap:8px}
.vt-util .vt-pill{position:relative;display:inline-flex;cursor:pointer}
.vt-util .vt-pill input{position:absolute;inset:0;opacity:0;cursor:pointer}
.vt-util .vt-pill span{display:block;min-height:44px;padding:10px 14px;border:1.5px solid var(--vt-line-ui);border-radius:var(--vt-radius);background:var(--vt-card);font-size:var(--vt-text-sm);transition:background var(--vt-duration-fast),color var(--vt-duration-fast)}
.vt-util .vt-pill input:checked + span{border-color:var(--vt-field);background:var(--vt-field);color:var(--vt-on-dark)}
.vt-util .vt-pill input:focus-visible + span{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-util .vt-pills--tarjetas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr))}
.vt-util .vt-pills--tarjetas .vt-pill,.vt-util .vt-pills--tarjetas span{width:100%}
.vt-util .vt-pills--tarjetas small{display:block;font-size:var(--vt-text-xs);opacity:.85}
.vt-util .vt-util__cond{margin-top:12px}
.vt-util .vt-util__suma{display:flex;justify-content:space-between;margin:0;padding:12px 14px;background:var(--vt-field-100)}
.vt-util .vt-wizard{display:flex;justify-content:space-between;gap:6px;margin:0 0 10px;padding:0;list-style:none;font-size:var(--vt-text-xs)}
.vt-util .vt-wizard li{display:grid;justify-items:center;gap:2px;color:var(--vt-muted)}
.vt-util .vt-wizard b{display:grid;place-items:center;width:28px;height:28px;border:1.5px solid var(--vt-line-ui);border-radius:50%}
.vt-util .vt-wizard [aria-current] b,.vt-util .vt-wizard .is-hecho b{border-color:var(--vt-field);background:var(--vt-field);color:var(--vt-on-dark)}
.vt-util .vt-wizard [aria-current]{color:var(--vt-ink)}
.vt-util .vt-progreso{height:3px;margin-bottom:24px;background:var(--vt-line)}
.vt-util .vt-progreso span{display:block;height:100%;background:var(--vt-field);transform:scaleX(.2);transform-origin:left;transition:transform var(--vt-duration-normal) var(--vt-ease-out)}
.vt-util .vt-util__pie{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px}
.vt-util .vt-util__cuenta{margin:0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-util .vt-util__exito h2:focus{outline:none}
.vt-util .vt-util__tarjeta{margin-bottom:16px;padding:20px;border:1px solid var(--vt-line);background:var(--vt-card);box-shadow:var(--vt-sombra-card)}
.vt-util .vt-util__tarjeta h2{margin:0;font-size:var(--vt-text-lg)}
.vt-util .vt-util__orden{display:flex;justify-content:space-between;gap:12px;margin-bottom:16px;padding:14px 16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-util .vt-util__orden small{display:block;font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-util .vt-util__total{font-weight:700;white-space:nowrap}
.vt-util .vt-util__casilla{display:flex;align-items:center;gap:10px;min-height:44px;font-weight:600;cursor:pointer}
.vt-util .vt-util__casilla input{width:22px;height:22px;accent-color:var(--vt-field)}
.vt-util .msg{display:none;margin:4px 0 0;font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-soil)}
.vt-util .vt-campo:has(.bad) .msg{display:block}
.vt-util .vt-control:has(.bad){border-color:var(--vt-soil);border-width:2px;background:var(--vt-soil-100)}
.vt-util .vt-util__error{margin:0 0 12px;padding:11px 13px;border:1px solid var(--vt-soil);background:var(--vt-soil-100);color:var(--vt-soil);font-weight:600}
.vt-util #enviar{width:100%;justify-content:center}
.vt-util .vt-util__datos{display:grid;gap:16px;margin:0}
.vt-util .vt-util__datos dt{font-weight:700}
.vt-util .vt-util__datos dd{margin:2px 0 0;color:var(--vt-ink-2)}
.vt-util .vt-util__servicios{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:4px 24px;margin:20px 0 0;padding:0;list-style:none}
.vt-util .vt-util__servicios a{display:block;padding:10px 0;border-bottom:1px solid var(--vt-line)}
.vt-util .vt-util__cabeza h1{margin:0 0 12px;font-size:clamp(2.25rem,1.5rem + 3vw,4rem);line-height:1.02}
.vt-util .vt-util__cabeza .vt-crumbs{margin-bottom:14px}
.vt-util .vt-util__cabeza + .vt-bloque{padding-top:clamp(24px,3vw,44px)}
/* Al final y con la misma especificidad que las reglas de arriba: un elemento hidden nunca se ve, aunque su regla le dé display. */
.vt-util [hidden]{display:none}
@media (prefers-reduced-motion:reduce){.vt-util .vt-progreso span,.vt-util .vt-pill span{transition:none}}
```

- [ ] **Step 3: Los componentes**

Crea `tools/site/componentes_util.py`:

```python
"""Componentes de las páginas utilitarias (Etapa 2i): cabecera sin etiqueta de precio, documento legal con índice, controles
con <label> o <fieldset> reales para el cuestionario y datos de envío, y botón de WhatsApp con texto propio. Funciones
puras; el texto llega de tools/site/contenido/ (solo HTML en línea permitido) y los atributos se escapan aquí."""
import componentes as c
import datos
from partials import WA_GLIFO, esc


def boton_wa_texto(texto, mensaje, cta):
    """Botón de WhatsApp con un texto que no es "Cotizar por WhatsApp" (Adelantar, Mandar foto…)."""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>')


def cabeza(k):
    """Ruta visible (si la hay), kicker, H1, entrada y, opcional, foto de producción. k: h1, lede, kicker, migas, foto
    (src, ancho, alto, alt), aviso. La foto es la única imagen prioritaria de la página."""
    ruta = c.migas(k["migas"]) if k.get("migas") else ""
    aviso = f'<p class="vt-promesa">{k["aviso"]}</p>' if k.get("aviso") else ""
    extra = k.get("extra", "")
    foto = ""
    if k.get("foto"):
        f = k["foto"]
        foto = (f'<div class="vt-util__foto"><img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" '
                f'alt="{esc(f["alt"])}" loading="eager" fetchpriority="high" decoding="async"></div>')
    return (f'<section class="vt-util__cabeza" aria-labelledby="vt-h1"><div class="vt-wrap">{ruta}'
            f'<div class="vt-util__intro"><div><p class="vt-kicker">{k["kicker"]}</p><h1 id="vt-h1">{k["h1"]}</h1>'
            f'<p class="vt-lede">{k["lede"]}</p>{aviso}{extra}</div>{foto}</div></div></section>')


def _bloque_legal(b):
    tipo, valor = b
    if tipo == "p":
        return f"<p>{valor}</p>"
    if tipo == "h3":
        return f"<h3>{valor}</h3>"
    etiqueta = "ol" if tipo == "ol" else "ul"
    return f"<{etiqueta}>" + "".join(f"<li>{x}</li>" for x in valor) + f"</{etiqueta}>"


def documento_legal(secciones):
    """Índice (con los h2) y artículo; cada sección conserva su id, el ancla que enlazan las otras páginas."""
    enlaces = "".join(f'<li><a href="#{esc(s["id"])}">{s.get("corto", s["titulo"])}</a></li>' for s in secciones)
    cuerpo = "".join(f'<section id="{esc(s["id"])}" aria-labelledby="vt-h-{esc(s["id"])}"><h2 id="vt-h-{esc(s["id"])}">'
                     f'{s["titulo"]}</h2>{"".join(_bloque_legal(b) for b in s["bloques"])}</section>'
                     for s in secciones)
    return (f'<div class="vt-wrap vt-legal"><nav class="vt-legal__indice" aria-label="En esta página"><ol>{enlaces}</ol>'
            f'</nav><article class="vt-legal__texto">{cuerpo}</article></div>')


# ---------- controles ----------
def _req(campo):
    return ' <span class="vt-req" aria-hidden="true">*</span>' if campo.get("requerido") else ""


def _pie(campo):
    return f'<p class="vt-util__pista">{campo["pista"]}</p>' if campo.get("pista") else ""


def _control(campo, ident):
    comunes = f'id="{esc(ident)}"' + (f' name="{esc(campo["name"])}"' if campo.get("name") else "")
    comunes += " required" if campo.get("requerido") else ""
    for atributo, clave in (("autocomplete", "completar"), ("placeholder", "placeholder"), ("min", "min"),
                            ("inputmode", "modo"), ("maxlength", "max")):
        if campo.get(clave) is not None:
            comunes += f' {atributo}="{esc(campo[clave])}"'
    if campo["tipo"] == "area":
        return f"<textarea {comunes}></textarea>"
    if campo["tipo"] == "lista":
        opciones = "".join(f'<option value="{esc(v)}">{t}</option>' if v is not None else f"<option>{t}</option>"
                           for v, t in campo["opciones"])
        return f"<select {comunes}>{opciones}</select>"
    return f'<input {comunes} type="{esc(campo["tipo"])}">'


def _campo(k):
    ident = k.get("id") or f'c-{k["name"]}'
    error = f'<p class="msg">{k["error"]}</p>' if k.get("error") else ""
    return (f'<div class="vt-campo"><label for="{esc(ident)}">{k["label"]}{_req(k)}</label>'
            f'<div class="vt-control">{_control(k, ident)}</div>{error}{_pie(k)}</div>')


def _opciones(k):
    filas = "".join(
        f'<label class="vt-pill"><input type="{k["tipo"]}" name="{esc(k["name"])}" value="{esc(v)}"'
        + "".join(f' {a}="{esc(x)}"' for a, x in (resto[0] if resto else ())) + f'><span>{t}</span></label>'
        for v, t, *resto in k["items"])
    sub = dibujar(k["sub"]) if k.get("sub") else ""
    return (f'<fieldset class="vt-util__grupo"><legend>{k["legend"]}</legend><div class="{k.get("clase_grupo", "vt-pills")}">'
            f'{filas}</div>{sub}</fieldset>')


# El contenido solo puede llevar HTML en línea (test_contenido.py): describe los controles con estos cuatro datos y la
# plantilla los dibuja.
def campo(k):
    """k: label, tipo (text, tel, email, number, area o lista), name o id; opcionales requerido, completar, placeholder,
    min, modo, max, pista, error, opciones."""
    return ("campo", k)


def opciones(k):
    """Radios o casillas en <fieldset>. k: legend, tipo (radio o checkbox), name, items (valor, texto y, opcional,
    atributos extra) y, opcionales, clase_grupo y sub (un condicional)."""
    return ("opciones", k)


def condicional(ident, control):
    return ("condicional", ident, control)


def fila(*controles, columnas=1):
    return ("fila", controles, columnas)


SUMA_AREAS = ("suma",)


def dibujar(control):
    """HTML de un control descrito con campo(), opciones(), condicional() o fila()."""
    tipo = control[0]
    if tipo == "campo":
        return _campo(control[1])
    if tipo == "opciones":
        return _opciones(control[1])
    if tipo == "condicional":
        return f'<div class="vt-util__cond" id="{esc(control[1])}" hidden>{dibujar(control[2])}</div>'
    if tipo == "suma":
        return ('<p class="vt-util__suma" id="area-display" hidden><span>Área total calculada</span>'
                '<strong id="area-total-val">0 m²</strong></p>')
    return (f'<div class="vt-util__fila vt-util__fila--{control[2]}">' + "".join(dibujar(c) for c in control[1]) + "</div>")


def dibujar_todos(controles):
    return "".join(dibujar(c) for c in controles)
```

- [ ] **Step 4: Cableado (seis cambios puntuales)**

`tools/site/activos.py`, en `FUENTES`, después de `terra-precios.css`:

```python
    "terra-util.css": "css/terra-util.css",
```

`tools/site/partials.py`: firma `def head(urls, legacy, tienda=False, plantas=False, materiales=False, precios=False, util=False):`; en el docstring, tras "terra-precios.css.", agrega ` Con util=True (<body class="vt-pagina vt-util">, Etapa 2i), terra-util.css.`; y tras el `if precios:`

```python
    if util:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-util.css"]}">')
```

`tools/site/shell.py`: tras `PRECIOS = …`, agrega `UTIL = '<body class="vt-pagina vt-util">'`; y en `aplicar`, `precios=PRECIOS in html` pasa a `precios=PRECIOS in html, util=UTIL in html`.

`vercel.json` y `tools/site/tests/test_vercel.py` (constante `HASH`): `terra-precios|legacy-fixes` pasa a `terra-precios|terra-util|legacy-fixes`.

`tools/site/paginas.py`, en `EXACTAS`, tras `"/datos-envio": _UTILIDAD,`:

```python
    "/404": _UTILIDAD,
```

`tools/site/generar.py`: antes de `PAGINAS = (` agrega el registro vacío y súmalo al final de `PAGINAS`:

```python
# Etapa 2i: páginas utilitarias (legales, formularios, protocolo, vivero y 404).
UTILITARIAS = (
)

```

```python
) + _varias("zona", lambda k: f"/{k}", lambda k: f"{k}/index.html", "zona") + UTILITARIAS
```

`tools/site/mensajes_paginas.py`, al final del archivo:

```python

# Etapa 2i: mensajes propios de las utilitarias, los de main (la firma la agrega datos.con_firma).
UTILITARIAS = {
    "gracias": "Hola, acabo de enviar una cotización por el cotizador y quiero avanzar",
    "cuestionario": "Hola, quiero empezar un proyecto de jardín en Tampico",
    "cuestionario_enviado": "Hola, acabo de enviar mi cuestionario de diseño de jardín",
    "politicas": "Hola, tengo una duda sobre envíos/devoluciones",
    "privacidad": "Hola, tengo una duda sobre el aviso de privacidad",
    "protocolo": "Hola, tengo dudas sobre el cuidado de mi pasto San Agustín",
    "vivero": "Hola, quiero visitar el vivero o cotizar plantas.\nLo que busco: \nTamaño aprox.: ",
    "vivero_planta": "Hola, estoy buscando una planta en el vivero de Tampico, ¿la tienen?",
    "no_encontrada": "Hola, busqué una página en su sitio y no la encontré. Necesito: ___",
}
```

Pruebas existentes: en `tools/site/tests/test_activos.py`, en `setUp`, tras el fixture de `terra-precios.css`:

```python
        (self.pub / "css" / "terra-util.css").write_text(".vt-util .vt-x{}", encoding="utf-8")
```

Y en `tools/site/tests/test_generar.py`, la lista `esperadas` termina así:

```python
                     + [ruta for _nombre, ruta in datos.ZONAS]
                     + [r for r, *_ in generar.UTILITARIAS])
```

- [ ] **Step 5: Verde y build**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
git status --short | grep -v '\.html$'
cd tools/site && python3 -m unittest tests.test_componentes_util tests.test_terra_util_css tests.test_activos tests.test_partials tests.test_shell tests.test_vercel tests.test_generar tests.test_paginas 2>&1 | tail -1
```

Expected: la segunda corrida `plantillas: 0 de 48`, `shell: 0 de 108`; aparecen `terra-util.css` y su copia con hash y cambia `activos.json`; `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add public/css/terra-util.css public/css/terra-util.*.css tools/site/activos.json tools/site/activos.py tools/site/partials.py tools/site/shell.py tools/site/paginas.py tools/site/generar.py tools/site/mensajes_paginas.py tools/site/componentes_util.py vercel.json tools/site/tests/test_componentes_util.py tools/site/tests/test_terra_util_css.py tools/site/tests/test_activos.py tools/site/tests/test_vercel.py tools/site/tests/test_generar.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(util): hoja terra-util.css con hash y componentes de cabecera, documento legal y controles" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: Plantilla `legal`, `/politicas` y `/politica-privacidad` (correcciones C1–C11)

**Files:** crear `tools/site/plantillas/legal.py`, `tools/site/contenido/{politicas,politica_privacidad}.py`, `tools/site/tests/test_legal.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_util_reglas.py`, `public/llms.txt`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_legal.py`:

```python
"""/politicas y /politica-privacidad con la plantilla legal: anclas estables, números de sus fuentes y sin dos H1."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import mensualidades  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402
from componentes_zonas import porcentaje_plazo  # noqa: E402

URLS = {k: f"/x/{k}" for k in ("terra.css", "terra-tienda.css", "terra-plantas.css", "terra-materiales.css", "terra-precios.css",
                               "terra-util.css", "legacy-fixes.css", "terra.js")}


def render(ruta):
    fila = next(f for f in generar.PAGINAS if f[0] == ruta)
    return generar.renderizar(ruta, fila[2], fila[3], URLS)


class PoliticasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = render("/politicas")

    def test_anclas_que_enlazan_otras_paginas(self):
        for ancla in ("envios", "devoluciones", "garantia-plantas", "garantia-pasto", "mensualidades", "facturacion", "privacidad", "contacto"):
            with self.subTest(ancla=ancla):
                self.assertIn(f'<section id="{ancla}"', self.html)
                self.assertIn(f'href="#{ancla}"', self.html)

    def test_carga_la_hoja_util_y_un_solo_h1(self):
        self.assertIn("/x/terra-util.css", self.html)
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)

    def test_numeros_de_sus_fuentes(self):
        for pieza in (f"{data.MIN_NACIONAL_M2} m²", f"desde {data.MIN_SHOWROOM_M2} m²", "$900", "$1,400"):
            self.assertIn(pieza, self.html)
        for plazo in mensualidades.PLAZOS:
            self.assertIn(f"+{porcentaje_plazo(plazo):.1f}%", self.html)

    def test_garantia_de_plantas_sin_prometer_costo_y_con_condiciones(self):
        self.assertIn("30 días de garantía de arraigo", self.html)
        self.assertIn("Nos avisas por WhatsApp con fotos dentro de los 30 días.", self.html)
        self.assertNotIn("asesoría gratis", self.html)

    def test_contacto_de_datos(self):
        for pieza in (datos.TELEFONO_VISIBLE, datos.CORREO_FORMULARIOS, datos.HORARIO, datos.CALLE):
            self.assertIn(pieza, self.html)

    def test_tipo_utilidad_en_el_shell(self):
        self.assertEqual(paginas.contexto("/politicas")["tipo"], "utilidad")
        self.assertIn('data-cta="utilidad:cierre"', shell.marcar_ctas(self.html, "utilidad"))


class PrivacidadTest(unittest.TestCase):
    def test_conserva_sus_ocho_puntos_y_su_marco_legal(self):
        html = render("/politica-privacidad")
        for titulo in ("1. Datos personales", "2. Finalidad", "3. Transferencia", "4. Derechos ARCO", "5. Uso de cookies",
                       "6. Seguridad", "7. Modificaciones", "8. Aceptación", "LFPDPPP", datos.GA4_ID, "20 días hábiles"):
            with self.subTest(titulo=titulo):
                self.assertIn(titulo, html)

    def test_transferencias_sin_nombrar_a_la_terminal(self):
        html = render("/politica-privacidad")
        self.assertIn("procesador de pagos con tarjeta", html)
        self.assertNotRegex(html.lower(), r"(?<![-.\w])clip(?![-\w:(])")


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_legal 2>&1 | tail -1
```

Expected: `FAILED (errors=…)`: `StopIteration`, la ruta no está en `generar.PAGINAS`.

- [ ] **Step 2: Plantilla**

Crea `tools/site/plantillas/legal.py`:

```python
"""Plantilla de documento legal (spec §3.3): ruta visible → H1 con la fecha de actualización → índice y secciones con
anclas estables (#envios, #devoluciones, #garantia-plantas, #garantia-pasto, #mensualidades…) → CTA final. Páginas:
/politicas y /politica-privacidad. <body class="vt-pagina vt-util">: el shell agrega terra-util.css."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def render(k):
    cuerpo = [cu.cabeza(k["cabeza"]), cu.documento_legal(k["secciones"])]
    if k.get("cierre"):
        ci = k["cierre"]
        cuerpo.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]))
    return base.documento(k["meta"], "\n".join(cuerpo), jsonld_bloques=k["jsonld"], clase_body=CLASE_BODY)
```

- [ ] **Step 3: Contenido**

Crea `tools/site/contenido/politicas.py`:

```python
"""Contenido de /politicas (plantilla legal). Conserva la sustancia de main y sus anclas (#envios, #devoluciones,
#garantia-plantas, #mensualidades, #facturacion, #privacidad, #contacto); #garantia-pasto es nueva y copia las condiciones
del protocolo. Números de tools/pasto (fletes, mínimos, mensualidades) y frases de datos.py: nada a mano. Correcciones
frente a main (cada una en el plan, tabla C1–C12): meta "devoluciones (30 días)" contra 7 días del texto, "sin costo" y
"gratis" en plantas, total sin mensualidad, efectivo omitido en formas de pago, embarque "al confirmarse el pago", tiempo
de entrega que sumaba 4 a 7 días, privacidad sin finalidades secundarias, y condiciones de materiales que faltaban."""
import componentes  # noqa: F401  (agrega tools/pasto al sys.path)
import data
import datos
import mensajes_paginas
import mensualidades
from componentes import dinero
from componentes_zonas import porcentaje_plazo

SITE = datos.SITIO
URL = f"{SITE}/politicas"
FLETE_MIN, FLETE_MAX = dinero(min(data.ZONAS.values())), dinero(max(data.ZONAS.values()))
ACTUALIZADO = "noviembre 2026"
DESCRIPCION = ("Políticas de Viveros Terra: envíos a todo México (3-5 días), devoluciones (7 días), privacidad de datos, "
               "facturación CFDI 4.0 y contacto.")
UMBRALES = "; ".join(
    f"desde {dinero(minimo)}, {' o '.join(', '.join(str(p) for p in plazos).rsplit(', ', 1))}"
    f"{' mensualidades' if i == 0 else ''}" for i, (minimo, plazos) in enumerate(sorted(mensualidades.UMBRALES)))
PORCENTAJES = ", ".join(
    f"{p} {'mensualidades ' if i == 0 else ''}+{porcentaje_plazo(p):.1f}%" for i, p in enumerate(mensualidades.PLAZOS))

SECCIONES = (
    {"id": "envios", "titulo": "Política de Envíos", "corto": "Envíos", "bloques": (
        ("p", "<strong>Cobertura:</strong> enviamos pasto sintético a <strong>todo México</strong> por paquetería."),
        ("ul", (
            "<strong>Tiempo de entrega:</strong> sale de Cd. Madero en 1 a 2 días hábiles y llega de 3 a 5 días hábiles "
            "después de confirmar tu pedido, según el destino.",
            f"<strong>Costo de envío:</strong> se cobra por cada rollo enviado, según el destino. Como referencia, va de "
            f"aproximadamente {FLETE_MIN} a {FLETE_MAX} por rollo. El costo exacto se confirma con tu código postal antes "
            "de pagar.",
            f"<strong>Compra mínima nacional:</strong> {data.MIN_NACIONAL_M2} m². En nuestro showroom de Tampico se vende "
            f"desde {data.MIN_SHOWROOM_M2} m² sin flete.",
            "<strong>Rastreo:</strong> te compartimos guía de rastreo para que sigas tu pedido.",
            "<strong>Presentación:</strong> el pasto se envía en rollo de 2 m de ancho.",
        )),
        ("h3", "Materiales en Tampico, Madero y Altamira"),
        ("p", datos.CONDICIONES_MATERIALES),
    )},
    {"id": "devoluciones", "titulo": "Política de Devoluciones", "corto": "Devoluciones", "bloques": (
        ("ul", (
            "<strong>Ventana de devolución:</strong> 7 días naturales a partir de la recepción del producto.",
            "<strong>Condición:</strong> producto <strong>nuevo, sin usar, sin cortar</strong> y en su empaque original.",
            "<strong>Cortes a medida:</strong> los pedidos cortados a una medida específica <strong>no admiten "
            "devolución</strong> por tratarse de producto personalizado.",
            "<strong>Costo del envío de retorno:</strong> a cargo del cliente.",
            "<strong>Cargo por reposición (restocking):</strong> 10% del valor del producto.",
            "<strong>Reembolso:</strong> se procesa en un máximo de 15 días una vez recibido y revisado el material, por "
            "el mismo medio de pago.",
            "<strong>Cambios:</strong> aceptamos cambios de producto sujetos a disponibilidad.",
            f"<strong>Cómo solicitarla:</strong> escríbenos por WhatsApp al {datos.TELEFONO_VISIBLE} con tu número de "
            "pedido.",
        )),
        ("p", f"<strong>Dirección de retorno:</strong> {datos.CALLE}, {datos.COLONIA}, Cd. Madero, Tamaulipas, C.P. {datos.CP}."),
    )},
    {"id": "garantia-plantas", "titulo": "Garantía de arraigo de plantas y palmas", "corto": "Garantía de plantas", "bloques": (
        ("p", "Las plantas y palmas que <strong>sembramos nosotros</strong> tienen <strong>30 días de garantía de "
              "arraigo</strong>, contados desde el día de la siembra. Si en ese plazo una planta no prende y se cuidó "
              "como te indicamos, la reponemos."),
        ("p", "<strong>Para que aplique:</strong>"),
        ("ul", (
            "La siembra la hizo el equipo de Viveros Terra, en jardín o en maceta.",
            "Se regó como indica la guía de cuidado que te entregamos con tu pedido.",
            "La planta sigue en el lugar donde la sembramos. Una planta de sol necesita sol y una de sombra necesita "
            "sombra; si cambia de lugar, cambia lo que necesita.",
            "Nos avisas por WhatsApp con fotos dentro de los 30 días.",
        )),
        ("p", "<strong>No la cubre:</strong>"),
        ("ul", (
            "Falta o exceso de riego.",
            "Macetas o plantas movidas a otro lugar, sobre todo de sol a sombra o de sombra a sol.",
            "Daños por mascotas, golpes, niños jugando, poda o productos aplicados sin consultarnos.",
            "Clima fuera de lo normal: nortes fuertes, heladas, granizo o inundación.",
            "Plantas que compraste en el vivero y sembraste por tu cuenta. En ese caso te orientamos por WhatsApp para "
            "que prendan.",
        )),
        ("p", "<strong>Cómo funciona:</strong> mándanos fotos de la planta y de dónde está. Si hace falta, vamos a "
              "revisarla. Te decimos el mismo día o al siguiente si aplica, y si aplica te la reponemos. La reposición es "
              "de la misma planta o de una equivalente si no hay existencia."),
    )},
    {"id": "garantia-pasto", "titulo": f"Garantía de arraigo del pasto San Agustín: {datos.ARRAIGO}",
     "corto": "Garantía de pasto", "bloques": (
        ("p", f"{datos.GARANTIA_PASTO.replace(' (ver condiciones)', '')} Aplica cuando:"),
        ("ul", (
            "La instalación fue realizada por el equipo de Viveros Terra.",
            f"Se realizó riego abundante y diario los primeros {datos.ARRAIGO} según el protocolo.",
            "No hubo pisoteo durante los primeros 7 días.",
            "No se aplicaron productos químicos sin autorización previa.",
            "El problema fue reportado antes del día 21.",
        )),
        ("p", f'{datos.PRIMER_RIEGO} Lee el <a href="/protocolo-cuidados-pasto-san-agustin">protocolo de cuidado del pasto</a>.'),
    )},
    {"id": "mensualidades", "titulo": "Pago en mensualidades con tarjeta de crédito", "corto": "Mensualidades", "bloques": (
        ("p", f"Puedes pagar en {' o '.join(', '.join(str(p) for p in mensualidades.PLAZOS).rsplit(', ', 1))} mensualidades "
              "con tarjeta de crédito. El precio en mensualidades es mayor que el de contado; siempre te mostramos el "
              "total y el monto de cada mensualidad antes de enviarte el link de pago."),
        ("ul", (
            "<strong>Contado:</strong> transferencia, efectivo o tarjeta en una sola exhibición. Es el precio más bajo.",
            f"<strong>Plazos por monto de contado:</strong> {UMBRALES}.",
            f"<strong>Total en mensualidades frente a contado:</strong> {PORCENTAJES}.",
            "<strong>Aprobación:</strong> tu banco emisor debe aceptar el plan; el monto de cada mensualidad puede variar "
            "por redondeo del banco.",
            "Aplica a pasto sintético, pasto natural instalado, instalación de pasto sintético, diseño de jardines y "
            "sistemas de riego. No aplica a mantenimiento mensual.",
        )),
    )},
    {"id": "facturacion", "titulo": "Facturación y Pagos", "corto": "Facturación y pagos", "bloques": (
        ("ul", (
            f"{datos.FACTURACION} Emitimos <strong>factura {datos.FACTURA}</strong> para personas físicas y morales.",
            "Formas de pago: transferencia bancaria, efectivo y link de pago (tarjeta de débito o crédito). La tarjeta en "
            "una sola exhibición paga el precio de contado.",
            f"{datos.ANTICIPO} La fecha de embarque te la confirmamos por WhatsApp.",
            "Todos los precios de material incluyen IVA.",
        )),
    )},
    {"id": "privacidad", "titulo": "Aviso de Privacidad", "corto": "Aviso de privacidad", "bloques": (
        ("p", "En Viveros Terra respetamos y protegemos tus datos personales. Este es un resumen; el documento completo es "
              'el <a href="/politica-privacidad">Aviso de Privacidad Integral</a>.'),
        ("ul", (
            "<strong>Datos que recabamos:</strong> nombre, teléfono, correo, dirección y código postal, para cotizar, "
            "procesar y enviar tu pedido y emitir tu factura.",
            "<strong>Uso:</strong> los datos se usan para dar seguimiento a tu compra y atención al cliente y, si no te "
            "das de baja, para enviarte promociones y recordatorios de jardinería. <strong>No vendemos ni compartimos"
            "</strong> tu información con terceros ajenos al envío, el cobro o la facturación.",
            "<strong>Conservación:</strong> conservamos tus datos el tiempo necesario para cumplir obligaciones fiscales y "
            "de garantía.",
            f"<strong>Derechos ARCO:</strong> puedes solicitar acceso, rectificación, cancelación u oposición al uso de tus "
            f"datos escribiendo a {datos.CORREO_FORMULARIOS}.",
        )),
    )},
    {"id": "contacto", "titulo": "Contacto", "corto": "Contacto", "bloques": (
        ("ul", (
            f"<strong>WhatsApp / Tel:</strong> {datos.TELEFONO_VISIBLE}",
            f"<strong>Correo:</strong> {datos.CORREO_FORMULARIOS}",
            f"<strong>Showroom:</strong> {datos.CALLE}, {datos.COLONIA}, Cd. Madero, Tamaulipas",
            f"<strong>Horario:</strong> {datos.HORARIO}",
        )),
    )},
)

CONTENIDO = {
    "tipo": "utilidad",
    "meta": {
        "title": "Políticas de Envío, Devoluciones y Privacidad · Viveros Terra",
        "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:type", "article"), ("og:url", URL), ("og:title", "Políticas · Viveros Terra"),
               ("og:description", "Envíos, devoluciones, garantía de plantas, privacidad, facturación y contacto de Viveros Terra."),
               ("og:image", f"{SITE}/img/pasto-sintetico-residencial-tampico.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "cabeza": {"migas": (("Inicio", "/"), ("Políticas", None)), "kicker": f"Actualizado {ACTUALIZADO}",
               "h1": "Políticas de la Tienda",
               "lede": "Envíos, devoluciones, garantías, mensualidades, privacidad, facturación y contacto de Viveros Terra."},
    "secciones": SECCIONES,
    "cierre": {"titulo": "¿Dudas sobre tu pedido?", "lede": f"Escríbenos: {datos.PROMESA.lower()}.",
               "mensaje": mensajes_paginas.UTILITARIAS["politicas"]},
    "jsonld": ({"@context": "https://schema.org", "@graph": [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Políticas", "item": URL}]}]},),
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {
        "En este artículo": "El índice es de la página, con aria-label “En esta página” y sin título visible.",
        "¿Listo para cotizar?": "La columna lateral duplicaba el CTA; queda un solo CTA final con la promesa única.",
    },
    "meta": {"description": (DESCRIPCION, "Decía devoluciones (30 días); la política publicada y la tienda dicen 7 días naturales.")},
    "jsonld": {},
}
```

Crea `tools/site/contenido/politica_privacidad.py`:

```python
"""Contenido de /politica-privacidad (plantilla legal). El texto legal es el de main, sin suavizarlo ni agregar compromisos;
el domicilio sale de datos.py. Se suman a la sección de transferencias los encargados que ya existen (paquetería, servicio
de formularios, cobro con tarjeta), sin nombrar al proveedor de la terminal: ver C9 del plan. El marco legal citado no se
toca: lo revisa el abogado del dueño."""
import datos
import mensajes_paginas

SITE = datos.SITIO
URL = f"{SITE}/politica-privacidad"
ACTUALIZADO = "noviembre de 2026"
TEL, CORREO = datos.TELEFONO_VISIBLE, datos.CORREO_FORMULARIOS
SECCIONES = (
    {"id": "responsable", "titulo": "Responsable", "bloques": (
        ("p", f"<strong>Responsable:</strong> Viveros Terra, con domicilio en {datos.CALLE}, Cd. Madero, Tamaulipas, México. "
              f"Contacto: {CORREO} · WhatsApp {TEL}."),)},
    {"id": "datos", "titulo": "1. Datos personales que recabamos", "corto": "Datos que recabamos", "bloques": (
        ("p", "En Viveros Terra recabamos los siguientes datos personales únicamente cuando usted nos contacta para "
              "solicitar un servicio o cotización:"),
        ("ul", ("Nombre completo", "Número telefónico (vía WhatsApp o llamada)", "Correo electrónico (si lo proporciona)",
                "Dirección del inmueble donde se prestará el servicio",
                f"Datos fiscales en caso de requerir factura {datos.FACTURA} (RFC, razón social, régimen)")),)},
    {"id": "finalidad", "titulo": "2. Finalidad del tratamiento de datos", "corto": "Finalidad", "bloques": (
        ("p", "Sus datos personales serán utilizados para las siguientes finalidades:"),
        ("ol", ("<strong>Finalidades primarias:</strong> contactarle para responder cotizaciones, agendar visitas técnicas, "
                "ejecutar los servicios contratados, emitir facturación y dar seguimiento postventa.",
                "<strong>Finalidades secundarias:</strong> envío ocasional de promociones, recordatorios estacionales de "
                "mantenimiento y comunicaciones comerciales relacionadas con jardinería.")),
        ("p", f'Si no desea recibir comunicaciones secundarias, puede manifestarlo respondiendo "BAJA" al WhatsApp {TEL}.'),)},
    {"id": "transferencia", "titulo": "3. Transferencia de datos", "corto": "Transferencia", "bloques": (
        ("p", "Viveros Terra <strong>no vende, alquila ni comparte sus datos personales con terceros</strong> con fines "
              "comerciales. Solo compartimos información estrictamente necesaria con:"),
        ("ul", (f"El SAT, cuando se emiten comprobantes fiscales digitales ({datos.FACTURA}).",
                "Proveedores de servicio de mensajería (WhatsApp Business) bajo sus propios términos.",
                "Paqueterías, para entregar su pedido; el servicio que nos hace llegar por correo los formularios de este "
                "sitio; y el procesador de pagos con tarjeta, cuando usted paga con link de pago.",
                "Autoridades cuando exista requerimiento legal fundado.")),)},
    {"id": "arco", "titulo": "4. Derechos ARCO", "corto": "Derechos ARCO", "bloques": (
        ("p", "Usted tiene derecho a <strong>Acceder, Rectificar, Cancelar u Oponerse</strong> al tratamiento de sus datos "
              "personales en cualquier momento. Para ejercer estos derechos:"),
        ("ul", (f'<strong>Correo:</strong> {CORREO} con asunto "Derechos ARCO"',
                f'<strong>WhatsApp:</strong> <a data-cta="utilidad:cuerpo" href="https://wa.me/{datos.TELEFONO_WA}">{TEL}</a>',
                f"<strong>Presencial:</strong> {datos.CALLE}, Cd. Madero, Tamaulipas. Lunes a viernes, 9am–6pm.")),
        ("p", "Responderemos su solicitud en un plazo máximo de 20 días hábiles, conforme al artículo 32 de la LFPDPPP."),)},
    {"id": "cookies", "titulo": "5. Uso de cookies y tecnologías de rastreo", "corto": "Cookies", "bloques": (
        ("p", f"Nuestro sitio web utiliza <strong>Google Analytics 4</strong> (ID: {datos.GA4_ID}) para medir el tráfico y "
              "mejorar la experiencia del usuario. Estas cookies son anónimas y agregadas, no permiten identificarle "
              "personalmente. Puede deshabilitarlas desde la configuración de su navegador o instalando el complemento de "
              "inhabilitación de Google Analytics."),)},
    {"id": "seguridad", "titulo": "6. Seguridad de los datos", "corto": "Seguridad", "bloques": (
        ("p", "Viveros Terra implementa medidas administrativas, técnicas y físicas razonables para proteger sus datos "
              "contra daño, pérdida, alteración o acceso no autorizado. Los datos fiscales se procesan a través de "
              "proveedores certificados por el SAT."),)},
    {"id": "modificaciones", "titulo": "7. Modificaciones al aviso", "corto": "Modificaciones", "bloques": (
        ("p", "Cualquier modificación a esta política será publicada en esta misma página con la fecha de actualización "
              "correspondiente. Le recomendamos revisarla periódicamente."),)},
    {"id": "aceptacion", "titulo": "8. Aceptación", "corto": "Aceptación", "bloques": (
        ("p", "Al contactarnos por cualquier medio (WhatsApp, llamada, correo o formulario web), usted manifiesta que ha "
              "leído, comprende y acepta los términos de este Aviso de Privacidad."),
        ("p", "<strong>Marco legal:</strong> Esta política se rige por la Ley Federal de Protección de Datos Personales en "
              "Posesión de los Particulares (LFPDPPP), publicada el 5 de julio de 2010, y su Reglamento, así como por los "
              "lineamientos del INAI."),)},
)
CONTENIDO = {
    "tipo": "utilidad",
    "meta": {"title": "Política de Privacidad · Viveros Terra Tampico",
             "description": "Política de privacidad y aviso de tratamiento de datos personales de Viveros Terra, empresa de jardinería en Tampico, Cd. Madero y Altamira.",
             "robots": "index, follow", "canonical": URL, "og": ()},
    "cabeza": {"migas": (("Inicio", "/"), ("Aviso de privacidad", None)), "kicker": "Aviso de Privacidad Integral",
               "h1": "Política de Privacidad", "lede": f"Última actualización: {ACTUALIZADO}."},
    "secciones": SECCIONES,
    "cierre": {"titulo": "¿Dudas sobre tus datos?", "lede": f"Escríbenos: {datos.PROMESA.lower()}.",
               "mensaje": mensajes_paginas.UTILITARIAS["privacidad"]},
    "jsonld": (),
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
```

- [ ] **Step 4: Registro, reglas y `llms.txt`**

En `generar.UTILITARIAS`:

```python
    ("/politicas", "politicas/index.html", "legal", "politicas"),
    ("/politica-privacidad", "politica-privacidad/index.html", "legal", "politica_privacidad"),
```

En `tests/test_util_reglas.py` quita `"/politicas"` y `"/politica-privacidad"` de `PENDIENTES`. En `public/llms.txt` (C3), `reciben asesoría gratis, sin garantía de arraigo` pasa a `reciben orientación por WhatsApp, sin garantía de arraigo`.

- [ ] **Step 5: Verde, build y paridad**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /politicas /politica-privacidad | grep -v ": ok"
cd tools/site && python3 -m unittest tests.test_legal tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_anclas tests.test_enlaces 2>&1 | tail -1
```

Expected: `plantillas: 2 de 50`; el `informe` imprime solo las dos líneas `== /ruta`; `OK`. `test_anclas` prueba las 39 entradas que llegan a `#mensualidades`, `#garantia-plantas` y `#devoluciones`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/plantillas/legal.py tools/site/contenido/politicas.py tools/site/contenido/politica_privacidad.py tools/site/generar.py tools/site/tests/test_legal.py tools/site/tests/test_util_reglas.py public/politicas/index.html public/politica-privacidad/index.html public/llms.txt
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(legal): políticas y aviso de privacidad con plantilla, anclas estables y sin contradicciones" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Plantilla `formulario` y `/gracias`

**Files:** crear `tools/site/plantillas/formulario.py`, `tools/site/contenido/gracias.py`, `tools/site/tests/test_gracias.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_util_reglas.py`, `tools/site/tests/test_migrar_shell.py`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_gracias.py`:

```python
"""/gracias: destino de los 6 formularios; la página cambia de ropa, no de URL ni de medición."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("gracias").CONTENIDO


class GraciasTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)

    def test_archivo_y_meta_de_siempre(self):
        fila = next(f for f in generar.PAGINAS if f[0] == "/gracias")
        self.assertEqual(fila[1], "gracias/index.html")
        self.assertEqual(K["meta"]["title"], "¡Gracias! Tu cotización está en camino · Viveros Terra")
        self.assertEqual(K["meta"]["robots"], "noindex, follow")
        self.assertEqual(K["meta"]["canonical"], f"{datos.SITIO}/gracias")

    def test_promesa_unica_y_visita_con_costo(self):
        self.assertIn(datos.PROMESA, self.html)
        self.assertIn(datos.HORARIO, self.html)
        self.assertIn(datos.VISITA_COSTO, self.html)
        self.assertNotRegex(self.html, r"2 horas|24 h\b|\bhoy\b")

    def test_adelantar_con_el_mensaje_y_la_medicion_de_main(self):
        self.assertIn('data-cta="utilidad:cuerpo"', self.html)
        self.assertIn("Adelantar por WhatsApp", self.html)
        self.assertIn(mensajes_paginas.UTILITARIAS["gracias"], unquote(self.html))

    def test_sin_scripts_propios(self):
        self.assertNotIn("<script src", self.html)


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_gracias 2>&1 | tail -1
```

Expected: `FAILED (errors=1)`, no existe `contenido.gracias`.

- [ ] **Step 2: Plantilla (con las tres vistas; las Tareas 6 y 7 solo agregan contenido)**

Crea `tools/site/plantillas/formulario.py`:

```python
"""Plantilla de las páginas de formulario, todas noindex (spec §3.3): /gracias (promesa única, qué sigue y "Adelantar por
WhatsApp"; GA4 la cuenta por su URL y su page_view), /cuestionario (paso 2 del diseño: 5 pasos a formsubmit) y
/datos-envio (arma el mensaje de WhatsApp en el navegador). La misma cabecera; el cuerpo sale de k["vista"]."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _gracias(k):
    pasos = "".join(f"<li>{x}</li>" for x in k["siguientes"]["items"])
    return (f'<section class="vt-bloque" aria-labelledby="vt-h-sigue"><div class="vt-wrap vt-util__estrecho">'
            f'<h2 id="vt-h-sigue">{k["siguientes"]["titulo"]}</h2><ol class="vt-util__lista">{pasos}</ol>'
            f'<p class="vt-util__adelanto">{k["adelanto"]["texto"]}</p>'
            f'<div class="vt-cta">{cu.boton_wa_texto("Adelantar por WhatsApp", k["adelanto"]["mensaje"], k["tipo"] + ":cuerpo")}</div>'
            f'<p class="vt-promesa">{k["mientras"]}</p><p class="vt-promesa"><a href="/">← Volver al inicio</a></p>'
            f'</div></section>')


def _paso(n, p, total):
    oculto = "" if n == 1 else " hidden"
    controles = cu.dibujar_todos(p["controles"])
    return (f'<div class="vt-paso" id="page-{n}" data-vt-paso="{n}"{oculto}><h2 tabindex="-1">{p["titulo"]}</h2>'
            f'<p class="vt-util__pista">{p["pista"]}</p>{controles}'
            f'</div>')


def _cuestionario(k):
    f = k["form"]
    total = len(f["pasos"])
    ocultos = "".join(f'<input type="hidden" name="{c.esc(n)}" value="{c.esc(v)}">' for n, v in f["ocultos"])
    miel = '<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
    pasos = "".join(_paso(i, p, total) for i, p in enumerate(f["pasos"], 1))
    nav = "".join(f'<li data-vt-marca="{i}"{" aria-current=step" if i == 1 else ""}><b>{i}</b><span>{p["corto"]}</span></li>'
                  for i, p in enumerate(f["pasos"], 1))
    ok = k["exito"]
    return (
        f'<section class="vt-bloque" aria-labelledby="vt-h1"><div class="vt-wrap vt-util__estrecho">'
        f'<ol class="vt-wizard" aria-label="Pasos del cuestionario">{nav}</ol>'
        f'<div class="vt-progreso" aria-hidden="true"><span id="prog"></span></div>'
        f'<form id="mainForm" class="vt-util__form" action="{c.esc(f["accion"])}" method="POST">'
        f'{ocultos}{miel}{pasos}'
        f'<div class="vt-util__pie" id="main-footer"><button type="button" class="vt-btn vt-btn--linea" id="btn-prev" hidden>'
        f'← Anterior</button><p class="vt-util__cuenta" id="step-counter" role="status">Paso 1 de {total}</p>'
        f'<button type="button" class="vt-btn vt-btn--tinta" id="btn-next">Siguiente →</button>'
        f'<button type="submit" class="vt-btn vt-btn--tinta" id="submit-btn" hidden>Enviar cuestionario</button></div>'
        f'</form><div class="vt-util__exito" id="success-screen" hidden role="status"><h2 tabindex="-1">{ok["titulo"]}</h2>'
        f'<p>{ok["texto"]}</p><div class="vt-cta">'
        f'{cu.boton_wa_texto(ok["boton"], ok["mensaje"], k["tipo"] + ":cuerpo")}</div></div>'
        f'<p class="vt-promesa">Última actualización: <time datetime="{k["fecha_iso"]}">{k["fecha"]}</time></p>'
        f'</div></section>')


def _datos_envio(k):
    tarjetas = "".join(
        f'<section class="vt-util__tarjeta" aria-labelledby="{t["id"]}"><h2 id="{t["id"]}">{t["titulo"]}</h2>'
        f'{cu.dibujar_todos(t["controles"])}</section>' for t in k["tarjetas"])
    return (
        f'<section class="vt-bloque"><div class="vt-wrap vt-util__estrecho"><div id="form">'
        f'<div class="vt-util__orden" id="order" hidden><div><b id="oProd"></b><small id="oFolio"></small></div>'
        f'<div class="vt-util__total" id="oTot"></div></div>{tarjetas}'
        f'<section class="vt-util__tarjeta" aria-label="Factura"><label class="vt-util__casilla"><input type="checkbox" id="quiere">'
        f'Requiero factura</label><div id="fact" hidden>{cu.dibujar_todos(k["factura"])}</div></section>'
        f'<p class="vt-util__error" id="err" role="alert" hidden>Revisa los campos marcados en rojo.</p>'
        f'<button type="button" class="vt-btn vt-btn--wa" id="enviar">Enviar mis datos por WhatsApp</button>'
        f'<p class="vt-promesa">{k["nota"]}</p></div>'
        f'<div class="vt-util__tarjeta" id="done" hidden><h2>¡Listo!</h2><p>Solo falta que toques <b>Enviar</b> en WhatsApp. '
        f'Si no se abrió, <a href="#" id="again">toca aquí</a>.</p></div></div></section>')


VISTAS = {"gracias": _gracias, "cuestionario": _cuestionario, "datos_envio": _datos_envio}


def render(k):
    cuerpo = cu.cabeza(k["cabeza"]) + "\n" + VISTAS[k["vista"]](k)
    foto = k["cabeza"].get("foto")
    precargas = (base.precarga_imagen(foto),) if foto else ()
    return base.documento(k["meta"], cuerpo, jsonld_bloques=k.get("jsonld", ()), precargas=precargas,
                          scripts=k.get("scripts", ()), clase_body=CLASE_BODY)
```

- [ ] **Step 3: Contenido**

Crea `tools/site/contenido/gracias.py`:

```python
"""Contenido de /gracias: destino de los 6 formularios por correo (_next de formsubmit). GA4 la cuenta por su URL y su
page_view; no tiene evento propio. El archivo, la URL, el título, robots, canonical y data-cta no cambian."""
import datos
import mensajes_paginas

URL = f"{datos.SITIO}/gracias"
CONTENIDO = {
    "tipo": "utilidad", "vista": "gracias",
    "meta": {"title": "¡Gracias! Tu cotización está en camino · Viveros Terra",
             "description": "Recibimos tu solicitud. Respondemos en menos de 1 hora en horario con tu cotización detallada por correo y WhatsApp.",
             "robots": "noindex, follow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Solicitud recibida", "h1": "¡Recibimos tu cotización!",
               "lede": f"<strong>{datos.PROMESA}</strong> · {datos.HORARIO}."},
    "siguientes": {"titulo": "Qué sigue ahora", "items": (
        f"<strong>{datos.PROMESA.replace('Respondemos en menos', 'En menos')}</strong> "
        "te escribimos por WhatsApp o correo con tu cotización.",
        f"<strong>Si hace falta,</strong> agendamos contigo una visita para medir. {datos.VISITA_COSTO}",
        "<strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.")},
    "adelanto": {"texto": "¿Prefieres adelantar y hablar ahora?", "mensaje": mensajes_paginas.UTILITARIAS["gracias"]},
    "mientras": ('<strong>Mientras tanto:</strong> revisa nuestro <a href="/catalogo">catálogo de plantas</a> o el '
                 '<a href="/blog">blog</a> con guías para el clima de Tampico.'),
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
```

- [ ] **Step 4: Registro, reglas y prueba vieja**

En `generar.UTILITARIAS`: `("/gracias", "gracias/index.html", "formulario", "gracias"),`. Quita `"/gracias"` de `PENDIENTES`. En `tests/test_migrar_shell.py` borra `test_gracias_real_sin_reglas_sueltas_de_header_y_footer`: leía el `<style>` del `/gracias` publicado, que ya no existe (el resto de ese archivo prueba con su propio fixture `GRACIAS`).

- [ ] **Step 5: Verde, build y paridad**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /gracias | grep -v ": ok"
cd tools/site && python3 -m unittest tests.test_gracias tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_consistencia tests.test_enlaces tests.test_migrar_shell 2>&1 | tail -1
git -C ../.. diff --stat -- public/mayoreo-pasto-tampico public/tierra-negra-vegetal-tampico | tail -1
```

Expected: `plantillas: 1 de 51`; solo `== /gracias`; `OK`; el último comando vacío (los formularios de origen no cambian y su `_next` sigue en `https://www.viverosterra.com/gracias`).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/plantillas/formulario.py tools/site/contenido/gracias.py tools/site/generar.py tools/site/tests/test_gracias.py tools/site/tests/test_util_reglas.py tools/site/tests/test_migrar_shell.py public/gracias/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(gracias): plantilla formulario; la misma URL, título, robots y medición" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: `/cuestionario`

**Files:** crear `tools/site/contenido/cuestionario.py`, `public/js/vt-cuestionario.js`, `tools/site/tests/test_cuestionario.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_util_reglas.py`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_cuestionario.py`:

```python
"""/cuestionario: un H1, etiqueta en cada control, cinco pasos y el destino de formsubmit de siempre."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("cuestionario").CONTENIDO


class CuestionarioTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)
        self.main = re.search(r"<main.*</main>", self.html, re.S).group(0)

    def test_destino_y_ocultos(self):
        self.assertIn(f'action="https://formsubmit.co/ajax/{datos.CORREO_FORMULARIOS}" method="POST"', self.main)
        for nombre, valor in (("_subject", "Nuevo cuestionario de jardín — Viveros Terra"), ("_template", "table"), ("_captcha", "false")):
            self.assertIn(f'<input type="hidden" name="{nombre}" value="{valor}">', self.main)
        self.assertIn('name="_honey"', self.main)

    def test_un_h1_y_noindex(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)
        self.assertEqual(K["meta"]["robots"], "noindex, follow")

    def test_cinco_pasos_y_solo_el_primero_visible(self):
        pasos = re.findall(r'<div class="vt-paso" id="page-\d" data-vt-paso="\d"([^>]*)>', self.main)
        self.assertEqual(pasos, ["", " hidden", " hidden", " hidden", " hidden"])

    def test_todo_control_visible_tiene_nombre_accesible(self):
        ids = set(re.findall(r'<label for="([^"]+)"', self.main))
        for etiqueta in re.findall(r"<(?:input|select|textarea)\b[^>]*>", self.main):
            if re.search(r'type="(?:hidden|radio|checkbox)"|name="_honey"', etiqueta):
                continue
            with self.subTest(control=etiqueta[:70]):
                self.assertIn(re.search(r'id="([^"]+)"', etiqueta).group(1), ids)
        self.assertEqual(self.main.count("<fieldset"), self.main.count("<legend>"))
        self.assertEqual(self.main.count("<fieldset"), 11)

    def test_script_propio_sin_inline(self):
        self.assertIn('<script src="/js/vt-cuestionario.js" defer></script>', self.html)
        self.assertNotIn("onclick=", self.html)


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_cuestionario 2>&1 | tail -1
```

Expected: `FAILED (errors=1)`.

- [ ] **Step 2: Contenido**

Crea `tools/site/contenido/cuestionario.py`:

```python
"""Contenido de /cuestionario, paso 2 del diseño (lo manda el asesor; noindex). Mismo action de formsubmit y mismos name y
value que main (el dueño recibe esos campos: tests/paridad/utilitarias-contrato.json), más el honeypot _honey que tienen
los demás formularios. Dos H1 en main: queda uno. Los rangos de inversión son opciones del cliente, no precios."""
import datos
import mensajes_paginas
import componentes_util as cu

URL = f"{datos.SITIO}/cuestionario"
DESCRIPCION = "Cuéntanos de tu jardín para preparar tu propuesta de diseño. Viveros Terra, Tampico, Madero y Altamira."
_otro = (("id", "rb-otro-esp"),)
_riego = (("class", "riego-trigger"),)


def _radios(legend, name, items, **extra):
    return cu.opciones({"legend": legend, "tipo": "radio", "name": name, "items": items, **extra})


def _casillas(legend, name, items):
    return cu.opciones({"legend": legend, "tipo": "checkbox", "name": name, "items": items})


def _iguales(*textos):
    return tuple((t, t) for t in textos)


PASO_1 = (
    cu.fila(cu.campo({"label": "Nombre completo", "name": "nombre", "id": "nombre", "tipo": "text", "requerido": True,
                      "placeholder": "Ej. María González", "completar": "name"}),
            cu.campo({"label": "WhatsApp", "name": "whatsapp", "id": "whatsapp", "tipo": "tel", "requerido": True,
                      "placeholder": "+52 833 000 0000", "completar": "tel"}), columnas=2),
    cu.fila(cu.campo({"label": "Correo electrónico", "name": "email", "tipo": "email", "placeholder": "correo@ejemplo.com",
                      "completar": "email"}),
            cu.campo({"label": "¿Cómo nos conoció?", "name": "como_nos_conocio", "tipo": "lista",
                      "opciones": (("", "Seleccionar..."), (None, "Página web"), (None, "Instagram / Facebook"),
                                   (None, "Referido de un cliente"), (None, "Google"), (None, "Otro"))}), columnas=2),
    cu.campo({"label": "Colonia / Fraccionamiento", "name": "direccion", "tipo": "text",
              "placeholder": "Ej. Fracc. Las Palmas, Altamira"}),
)
PASO_2 = (
    _radios("Tipo de espacio", "tipo_espacio",
            _iguales("Jardín frontal", "Jardín trasero", "Ambos", "Interior / patio", "Banqueta", "Plaza comercial",
                     "Restaurante") + (("Otro", "Otro", _otro),),
            sub=cu.condicional("otro-esp-wrap", cu.campo({"label": "Especificar tipo de espacio", "name": "tipo_espacio_otro",
                                                           "tipo": "text", "placeholder": "Especificar tipo de espacio..."}))),
    cu.fila(cu.campo({"label": "Área de pasto (m²)", "name": "area_pasto", "id": "area_pasto", "tipo": "number",
                      "placeholder": "Ej. 60", "min": "0", "pista": "Aproximado está bien"}),
            cu.campo({"label": "Área jardinera (m²)", "name": "area_jardinera", "id": "area_jard", "tipo": "number",
                      "placeholder": "Ej. 20", "min": "0"}),
            cu.campo({"label": "Área total (m²)", "name": "area_total", "id": "area_total_input", "tipo": "number",
                      "placeholder": "Ej. 80", "min": "0"}), columnas=3),
    cu.SUMA_AREAS,
    cu.fila(
        _radios("¿Tiene riego instalado?", "riego_instalado",
                (("Sí", "Sí"), ("No", "No", _riego), ("Parcial", "Parcial", _riego)),
                sub=cu.condicional("cond-riego", _radios("¿Considera instalar riego?", "instalar_riego",
                                                          _iguales("Sí, de inmediato", "En un futuro", "No")))),
        _radios("¿Presurizador hidroneumático?", "hidroneumatico", _iguales("Sí", "No", "No sé")), columnas=2),
    cu.campo({"label": "Elementos existentes a considerar", "name": "elementos_existentes", "tipo": "area",
              "placeholder": "Bardas, árboles, construcciones, pendientes del terreno..."}),
)
PASO_3 = (
    _casillas("¿Cómo usará principalmente el jardín?", "uso",
              (("Convivencia familiar", "Convivencia"), ("Descanso", "Descanso"), ("Juego de niños", "Niños"),
               ("Mascotas", "Mascotas"), ("Asados / reuniones", "Asados"), ("Imagen / fachada", "Imagen"),
               ("Solo estético", "Estético"))),
    _casillas("Estilo que le atrae", "estilo",
              (("Tropical", "Tropical"), ("Minimalista", "Minimalista"), ("Mediterráneo", "Mediterráneo"),
               ("Japonés / zen", "Zen"), ("Colorido", "Colorido"), ("Natural", "Natural"),
               ("Sin preferencia", "Sin preferencia"))),
    cu.fila(_radios("¿Prefiere árboles o palmas?", "arboles_palmas", _iguales("Árboles", "Palmas", "Ambos", "Ninguno")),
            _radios("Nivel de mantenimiento", "mantenimiento",
                    (("Bajo mantenimiento", "Fácil"), ("Moderado", "Moderado"), ("Me da igual", "Me da igual"))), columnas=2),
    cu.campo({"label": "Plantas que le gustan o quiere incluir", "name": "plantas_preferencia", "tipo": "area",
              "placeholder": "Ej. buganvilias, helechos, palmeras, cactus — cualquier planta que tenga en mente..."}),
    cu.fila(cu.campo({"label": "Elementos o plantas a conservar", "name": "conservar", "tipo": "area",
                      "placeholder": "Árboles existentes, macetas, fuentes, pérgolas..."}),
            cu.campo({"label": "Fotos de referencia", "name": "referencias", "tipo": "area",
                      "placeholder": "Link de Pinterest / Instagram o descripción de lo que le gustó..."}), columnas=2),
)
PRESUPUESTOS = (("$5,000–$15,000 MXN", "$5,000 – $15,000 MXN", "Proyecto básico con plantas y detalles"),
                ("$15,000–$40,000 MXN", "$15,000 – $40,000 MXN", "Proyecto medio con plantas y piso"),
                ("$40,000–$80,000 MXN", "$40,000 – $80,000 MXN", "Proyecto completo con instalaciones"),
                ("$80,000 MXN+", "$80,000 MXN en adelante", "Proyecto ejecutivo / premium"))
PASO_4 = (
    cu.opciones({"legend": "Inversión aproximada", "tipo": "radio", "name": "presupuesto_ejecucion", "clase_grupo": "vt-pills vt-pills--tarjetas",
                 "items": tuple((v, f"<b>{m}</b><small>{d}</small>") for v, m, d in PRESUPUESTOS)}),
    _radios("¿Cuándo le gustaría iniciar la ejecución?", "fecha_inicio",
            (("Lo antes posible", "Lo antes posible"), ("1–3 meses", "1–3 meses"), ("3–6 meses", "3–6 meses"),
             ("Más de 6 meses", "Más de 6 meses"), ("Solo el diseño por ahora", "Solo el diseño"))),
)
PASO_5 = (
    _radios("¿Cuál es su mayor prioridad?", "prioridad",
            _iguales("Que se vea increíble", "Que sea funcional", "Fácil de mantener", "Valor a la propiedad")),
    cu.campo({"label": "¿Algo más que debamos saber?", "name": "observaciones", "tipo": "area",
              "placeholder": "Ideas especiales, limitaciones del terreno, preguntas... todo suma para el diseño."}),
)
CONTENIDO = {
    "tipo": "utilidad", "vista": "cuestionario", "scripts": ("/js/vt-cuestionario.js",),
    "meta": {"title": "Cuestionario de Proyecto — Viveros Terra", "description": DESCRIPCION, "robots": "noindex, follow",
             "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Diseño de jardines", "h1": 'Tu jardín empieza aquí. <span class="vt-serif">Cuéntanos tu visión.</span>',
               "lede": f"Tómate 4 minutos para contarnos qué necesitas. Nuestro diseñador creará una propuesta hecha exactamente para ti; {datos.PROMESA.lower().replace('respondemos', 'te respondemos')}.",
               "aviso": f"{datos.VISITA_COSTO_CORTO} · Diseño personalizado · 4-5 minutos",
               "foto": {"src": "/img/diseno-jardin-instalacion-plantas-tampico.webp", "ancho": 1400, "alto": 787, "alt": ""}},
    "form": {"accion": f"https://formsubmit.co/ajax/{datos.CORREO_FORMULARIOS}",
             "ocultos": (("_subject", "Nuevo cuestionario de jardín — Viveros Terra"), ("_template", "table"), ("_captcha", "false")),
             "pasos": (
                 {"corto": "Tus datos", "titulo": "Cuéntanos de ti", "pista": "Para coordinar tu visita técnica y enviarte la propuesta de diseño.", "controles": PASO_1},
                 {"corto": "Tu espacio", "titulo": "Tu espacio", "pista": "No te preocupes si no tienes las medidas exactas — las tomamos en la visita.", "controles": PASO_2},
                 {"corto": "Estilo", "titulo": "Tu estilo y gustos", "pista": "Entre más nos cuentes, más personalizado será tu diseño.", "controles": PASO_3},
                 {"corto": "Inversión", "titulo": "Inversión estimada", "pista": "Esta info es solo para proponer opciones reales — no te compromete a nada.", "controles": PASO_4},
                 {"corto": "Final", "titulo": "¡Ya casi! Una última pregunta", "pista": "Esto nos ayuda a priorizar lo que más le importa en el diseño.", "controles": PASO_5},
             )},
    "exito": {"titulo": "¡Gracias por tu información!", "texto": f"Hemos recibido tu cuestionario. Un diseñador de Viveros Terra {datos.PROMESA.lower().replace('respondemos', 'te responde')} para coordinar tu visita técnica. {datos.VISITA_COSTO}",
              "boton": "También puedes escribirnos por WhatsApp", "mensaje": mensajes_paginas.UTILITARIAS["cuestionario_enviado"]},
    "fecha": "14 de mayo, 2026", "fecha_iso": "2026-05-14",
}
PARIDAD = {"reemplazos": {"Tu jardín empieza aquí": "Tu jardín empieza aquí. Cuéntanos tu visión.",
                          "Tu jardín empieza aquí. Cuéntanos tu visión.": "Tu jardín empieza aquí. Cuéntanos tu visión."},
           "retirados": {},
           "meta": {"description": (DESCRIPCION, "La página no tenía descripción y publicaba una meta vacía."),
                    "canonical": (URL, "Spec §3.5: el cuestionario lleva noindex, follow y canonical; no tenía canonical.")},
           "jsonld": {}}
```

- [ ] **Step 3: JavaScript**

Crea `public/js/vt-cuestionario.js`:

```javascript
// public/js/vt-cuestionario.js
/* Cuestionario de diseño (Etapa 2i): el asistente de 5 pasos de main y su envío a formsubmit por fetch (el action /ajax/
   responde JSON), con el mismo aviso en la misma página al terminar. Dos arreglos: no se avanza con los datos obligatorios
   vacíos (antes el navegador bloqueaba el envío al final, en un paso oculto) y Enter a medio camino avanza en vez de enviar. */
(function () {
  'use strict';
  const form = document.getElementById('mainForm');
  if (!form) return;
  const $ = (id) => document.getElementById(id);
  const pasos = Array.from(form.querySelectorAll('[data-vt-paso]'));
  const total = pasos.length;
  const marcas = Array.from(document.querySelectorAll('[data-vt-marca]'));
  const anterior = $('btn-prev');
  const siguiente = $('btn-next');
  const enviar = $('submit-btn');
  const cuenta = $('step-counter');
  let actual = 1;

  function pintar() {
    pasos.forEach((p, i) => { p.hidden = i + 1 !== actual; });
    marcas.forEach((m, i) => {
      m.classList.toggle('is-hecho', i + 1 < actual);
      if (i + 1 === actual) m.setAttribute('aria-current', 'step'); else m.removeAttribute('aria-current');
    });
    $('prog').style.transform = `scaleX(${actual / total})`;
    anterior.hidden = actual === 1;
    siguiente.hidden = actual === total;
    enviar.hidden = actual !== total;
    cuenta.textContent = `Paso ${actual} de ${total}`;
  }

  function pasoValido() {
    return Array.from(pasos[actual - 1].querySelectorAll('input,select,textarea')).every((c) => c.reportValidity());
  }

  function ir(delta) {
    const destino = actual + delta;
    if (destino < 1 || destino > total || (delta > 0 && !pasoValido())) return;
    actual = destino;
    pintar();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    pasos[actual - 1].querySelector('h2').focus({ preventScroll: true });
  }

  anterior.addEventListener('click', () => ir(-1));
  siguiente.addEventListener('click', () => ir(1));

  // Riego: la pregunta extra aparece con "No" o "Parcial".
  form.querySelectorAll('.riego-trigger').forEach((r) => r.addEventListener('change', () => { $('cond-riego').hidden = false; }));
  const conRiego = form.querySelector('input[name="riego_instalado"][value="Sí"]');
  if (conRiego) conRiego.addEventListener('change', () => { $('cond-riego').hidden = true; });
  // Tipo de espacio "Otro": campo libre.
  form.querySelectorAll('input[name="tipo_espacio"]').forEach((r) => r.addEventListener('change', () => {
    $('otro-esp-wrap').hidden = !$('rb-otro-esp').checked;
  }));

  function calcularTotal() {
    const pasto = parseFloat($('area_pasto').value) || 0;
    const jardinera = parseFloat($('area_jard').value) || 0;
    if (pasto <= 0 && jardinera <= 0) return;
    const suma = Math.round(pasto + jardinera);
    $('area-display').hidden = false;
    $('area-total-val').textContent = `${suma} m²`;
    $('area_total_input').value = suma;
  }
  $('area_pasto').addEventListener('input', calcularTotal);
  $('area_jard').addEventListener('input', calcularTotal);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (actual < total) { ir(1); return; }
    enviar.textContent = 'Enviando...';
    enviar.disabled = true;
    const fallo = () => { enviar.textContent = 'Error — intenta de nuevo'; enviar.disabled = false; };
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      const datos = res.ok ? await res.json().catch(() => ({})) : {};
      if (res.ok && String(datos.success) !== 'false') {
        form.hidden = true;
        document.querySelector('.vt-wizard').hidden = true;
        $('prog').style.transform = 'scaleX(1)';
        const ok = $('success-screen');
        ok.hidden = false;
        ok.querySelector('h2').focus();
      } else {
        fallo();
      }
    } catch (error) {
      fallo();
    }
  });

  pintar();
})();
```

- [ ] **Step 4: Registro y reglas**

En `generar.UTILITARIAS`: `("/cuestionario", "cuestionario.html", "formulario", "cuestionario"),`. Quita `"/cuestionario"` de `PENDIENTES`.

- [ ] **Step 5: Verde, build y paridad**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /cuestionario | grep -v ": ok"
cd tools/site && python3 -m unittest tests.test_cuestionario tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_enlaces 2>&1 | tail -1
```

Expected: `plantillas: 1 de 52`; solo `== /cuestionario`; `OK`. `test_campos_del_cuestionario_iguales_a_main_mas_honeypot` compara los 74 controles en orden: si falla, corrige el contenido, nunca la captura.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/contenido/cuestionario.py public/js/vt-cuestionario.js tools/site/generar.py tools/site/tests/test_cuestionario.py tools/site/tests/test_util_reglas.py public/cuestionario.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(cuestionario): plantilla con etiquetas reales, un H1, honeypot y los mismos campos a formsubmit" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 7: `/datos-envio`

**Files:** crear `tools/site/contenido/datos_envio.py`, `public/js/vt-datos-envio.js`, `tools/site/tests/test_datos_envio.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_util_reglas.py`.

- [ ] **Step 1: JavaScript y prueba en rojo**

Crea `public/js/vt-datos-envio.js`:

```javascript
// public/js/vt-datos-envio.js
/* Datos de envío (Etapa 2i): el script de main sin cambios de fondo. El texto de WhatsApp, sus emojis y el bloque #VT1 los
   lee el sistema del dueño: no se cambian. Solo se pasa de style.display a hidden y de onclick a addEventListener. */
(function () {
'use strict';
const ESTADOS=["Aguascalientes","Baja California","Baja California Sur","Campeche","Chiapas","Chihuahua","CDMX","Coahuila","Colima","Durango","Estado de México","Guanajuato","Guerrero","Hidalgo","Jalisco","Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca","Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa","Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz","Yucatán","Zacatecas"];
const $=id=>document.getElementById(id);
$("estado").innerHTML='<option value="">Elige el estado</option>'+ESTADOS.map(e=>`<option>${e}</option>`).join('');
const b64e=o=>btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
let P={};
try{const d=new URLSearchParams(location.search).get('d');if(d)P=JSON.parse(decodeURIComponent(escape(atob(d.replace(/-/g,'+').replace(/_/g,'/')))));}catch(e){P={};}
if(P.n){$("hola").textContent='Hola '+P.n.split(' ')[0]+', ¿a dónde te lo enviamos?';$("recibe").value=P.n;}
if(P.p){$("order").hidden=false;$("oProd").textContent=P.p;$("oFolio").textContent=P.f?'Pedido '+P.f:'';$("oTot").textContent=P.t||'';}
if(P.s&&ESTADOS.includes(P.s))$("estado").value=P.s;
if(P.c)$("municipio").value=P.c;
if(P.z)$("cp").value=P.z;
const WA=(P.w&&/^\d{10}$/.test(P.w))?P.w:'8333268008';
const dg=s=>(s||'').replace(/\D/g,'');
const v=id=>$(id).value.trim();
function marca(id,ok){$(id).classList.toggle('bad',!ok);return ok;}
function enviar(){
  let ok=true;
  ['calle','colonia','municipio','ref'].forEach(id=>ok=marca(id,v(id).length>=2)&&ok);
  ok=marca('estado',!!v('estado'))&&ok;
  ok=marca('cp',dg(v('cp')).length===5)&&ok;
  ok=marca('recibe',v('recibe').split(/\s+/).length>=2)&&ok;
  ok=marca('tel',dg(v('tel')).slice(-10).length===10)&&ok;
  const fx=$("quiere").checked;
  if(fx){
    ok=marca('rfc',/^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$/.test(v('rfc').toUpperCase()))&&ok;
    ok=marca('fcp',dg(v('fcp')).length===5)&&ok;
    ok=marca('razon',v('razon').length>=3)&&ok;
    ok=marca('regimen',!!v('regimen'))&&ok;ok=marca('uso',!!v('uso'))&&ok;
    ok=marca('correo',/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v('correo')))&&ok;
  }
  $("err").hidden=ok;
  if(!ok){const b=document.querySelector('.bad');if(b){b.scrollIntoView({behavior:'smooth',block:'center'});b.focus();}return;}
  const e={calle:v('calle'),colonia:v('colonia'),municipio:v('municipio'),estado:v('estado'),cp:dg(v('cp')),ref:v('ref'),recibe:v('recibe'),tel:dg(v('tel')).slice(-10)};
  const x=fx?{rfc:v('rfc').toUpperCase(),cp:dg(v('fcp')),razon:v('razon'),regimen:v('regimen'),uso:v('uso'),correo:v('correo')}:null;
  let t=`Hola, aquí están mis datos de envío${P.f?' para el pedido '+P.f:''}:\n\n`;
  t+=`📍 *Dirección de entrega*\nCalle y número: ${e.calle}\nColonia: ${e.colonia}\nMunicipio: ${e.municipio}\nEstado: ${e.estado}\nCódigo Postal: ${e.cp}\nReferencias: ${e.ref}\n\n`;
  t+=`📦 *Recibe*\nNombre: ${e.recibe}\nTeléfono: ${e.tel}\n\n`;
  t+=x?`🧾 *Factura*\nRFC: ${x.rfc}\nRazón social: ${x.razon}\nRégimen: ${x.regimen}\nC.P. fiscal: ${x.cp}\nUso de CFDI: ${x.uso}\nCorreo: ${x.correo}\n\n`:`🧾 Factura: no\n\n`;
  t+=`#VT1:${b64e({f:P.f||'',e,x})}`;
  const url=`https://wa.me/52${WA}?text=${encodeURIComponent(t)}`;
  $("again").href=url;$("form").hidden=true;$("done").hidden=false;window.scrollTo(0,0);
  location.href=url;
}
$("enviar").addEventListener('click',enviar);
$("quiere").addEventListener('change',function(){$("fact").hidden=!this.checked;});
})();
```

Crea `tools/site/tests/test_datos_envio.py`:

```python
"""/datos-envio: la plantilla no toca el contrato con el asesor (?d=…) ni el texto #VT1 que arma el JavaScript."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("datos_envio").CONTENIDO
JS = (paginas.PUBLIC / "js" / "vt-datos-envio.js").read_text(encoding="utf-8")


class DatosEnvioTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)

    def test_noindex_nofollow_y_sin_formulario(self):
        self.assertEqual(K["meta"]["robots"], "noindex, nofollow")
        self.assertNotIn("<form", self.html)

    def test_cada_control_con_su_label(self):
        ids = set(re.findall(r'<label for="([^"]+)"', self.html))
        for etiqueta in re.findall(r"<(?:input|select)\b[^>]*>", self.html):
            if 'type="checkbox"' in etiqueta:
                continue
            with self.subTest(control=etiqueta[:60]):
                self.assertIn(re.search(r'id="([^"]+)"', etiqueta).group(1), ids)

    def test_el_mensaje_de_whatsapp_no_cambia(self):
        for pieza in ("Hola, aquí están mis datos de envío", "📍 *Dirección de entrega*", "📦 *Recibe*", "🧾 *Factura*",
                      "#VT1:${b64e({f:P.f||'',e,x})}", "'8333268008'", "location.href=url"):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, JS)

    def test_sin_manejadores_en_linea(self):
        self.assertNotRegex(self.html, r"\son(?:click|change)=")


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_datos_envio 2>&1 | tail -1
```

Expected: `FAILED (errors=1)`.

- [ ] **Step 2: Contenido**

Crea `tools/site/contenido/datos_envio.py`:

```python
"""Contenido de /datos-envio (noindex, nofollow): el asesor lo manda por WhatsApp con ?d=…; vt-datos-envio.js arma el
mensaje de vuelta. Mismos id que main (el JS y el texto #VT1 dependen de ellos). Sin formsubmit: nada sale de la página."""
import datos
import componentes_util as cu

URL = f"{datos.SITIO}/datos-envio"


def _c(ident, label, error=None, tipo="text", req=True, **extra):
    return cu.campo({"label": label, "id": ident, "tipo": tipo, "requerido": req, "error": error, **extra})


REGIMENES = ("601 · General de Ley Personas Morales", "603 · Personas Morales con Fines no Lucrativos",
             "605 · Sueldos y Salarios e Ingresos Asimilados a Salarios", "606 · Arrendamiento",
             "612 · Personas Físicas con Actividades Empresariales y Profesionales", "616 · Sin obligaciones fiscales",
             "621 · Incorporación Fiscal", "625 · Actividades Empresariales a través de Plataformas Tecnológicas",
             "626 · Régimen Simplificado de Confianza")
USOS = ("G01 · Adquisición de mercancías", "G03 · Gastos en general", "S01 · Sin efectos fiscales")

DIRECCION = (
    _c("calle", "Calle y número", "Escribe la calle y el número.", completar="address-line1",
       placeholder="Ej. Av. Hidalgo 1234, int. 5"),
    cu.fila(_c("colonia", "Colonia", "Escribe la colonia.", completar="address-level3"),
              _c("cp", "Código postal", "Deben ser 5 dígitos.", modo="numeric", max="5", completar="postal-code"),
              _c("municipio", "Municipio", "Escribe el municipio.", completar="address-level2"),
              _c("estado", "Estado", "Elige el estado.", tipo="lista", opciones=(), completar="address-level1"), columnas=2),
    _c("ref", "Referencias", "Las referencias son obligatorias para la paquetería.",
         placeholder="Entre qué calles o un punto de referencia",
         pista="Ej. entre Juárez y Morelos, portón negro frente a la farmacia."),
)
RECIBE = (_c("recibe", "Nombre completo de quien recibe", "Escribe nombre y apellidos.", completar="name"),
          _c("tel", "Teléfono de contacto", "Deben ser 10 dígitos.", tipo="tel", modo="tel", completar="tel",
               placeholder="10 dígitos"),)
FACTURA = (
    cu.fila(_c("rfc", "RFC", "Revisa el RFC (12 o 13 caracteres).", req=False, max="13"),
            _c("fcp", "C.P. fiscal", "Deben ser 5 dígitos.", req=False, modo="numeric", max="5"), columnas=2),
    _c("razon", "Nombre o razón social", "Escribe el nombre o razón social.", req=False,
         pista="Tal como aparece en tu constancia de situación fiscal."),
    _c("regimen", "Régimen fiscal", "Elige tu régimen fiscal.", req=False, tipo="lista",
         opciones=(("", "Elige tu régimen"),) + tuple((None, r) for r in REGIMENES)),
    _c("uso", "Uso de CFDI", "Elige el uso de CFDI.", req=False, tipo="lista",
         opciones=(("", "Elige el uso"),) + tuple((None, u) for u in USOS)),
    _c("correo", "Correo para recibir la factura", "Revisa el correo.", req=False, tipo="email", modo="email", completar="email"),
)

CONTENIDO = {
    "tipo": "utilidad", "vista": "datos_envio", "scripts": ("/js/vt-datos-envio.js",),
    "meta": {"title": "Datos de envío · Viveros Terra",
             "description": "Comparte la dirección de entrega de tu pedido de pasto sintético.",
             "robots": "noindex, nofollow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Tu pedido", "h1": '<span id="hola">Datos para tu envío</span>',
               "lede": "Llénalo en un minuto. Al terminar se abre WhatsApp con tus datos listos para enviárnoslos."},
    "tarjetas": ({"id": "vt-h-direccion", "titulo": "Dirección de entrega", "controles": DIRECCION},
                 {"id": "vt-h-recibe", "titulo": "¿Quién recibe?", "controles": RECIBE}),
    "factura": FACTURA,
    "nota": "Tus datos solo viajan por WhatsApp a Viveros Terra; esta página no los guarda.",
}
PARIDAD = {"reemplazos": {}, "retirados": {},
           "meta": {"canonical": (URL, "Cada página con plantilla lleva canonical; esta noindex no tenía.")},
           "jsonld": {}}
```

- [ ] **Step 3: Registro y reglas**

En `generar.UTILITARIAS`: `("/datos-envio", "datos-envio/index.html", "formulario", "datos_envio"),`. Quita `"/datos-envio"` de `PENDIENTES`.

- [ ] **Step 4: Verde, build y paridad**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /datos-envio | grep -v ": ok"
cd tools/site && python3 -m unittest tests.test_datos_envio tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_enlaces 2>&1 | tail -1
```

Expected: `plantillas: 1 de 53`; solo `== /datos-envio`; `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/contenido/datos_envio.py public/js/vt-datos-envio.js tools/site/generar.py tools/site/tests/test_datos_envio.py tools/site/tests/test_util_reglas.py public/datos-envio/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(datos-envio): plantilla formulario con el mismo mensaje de WhatsApp y bloque VT1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 8: Plantilla `protocolo` y su página

**Files:** crear `tools/site/plantillas/protocolo.py`, `tools/site/contenido/protocolo.py`, `tools/site/tests/test_protocolo.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_util_reglas.py`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_protocolo.py`:

```python
"""Protocolo de pasto: las tres etapas de riego y las condiciones de la garantía, con precios de datos.py."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
from componentes import dinero  # noqa: E402
from plantillas import protocolo  # noqa: E402

K = generar.cargar("protocolo").CONTENIDO


class ProtocoloTest(unittest.TestCase):
    def setUp(self):
        self.html = protocolo.render(K)

    def test_etapas_en_orden(self):
        posiciones = [self.html.index(d) for d in ("Días 1 – 7", "Días 8 – 14", "Días 15 – 20")]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_garantia_con_ancla_y_sus_cinco_condiciones(self):
        self.assertIn('id="garantia"', self.html)
        self.assertEqual(len(K["garantia"]["condiciones"]), 5)
        self.assertIn("El problema fue reportado antes del día 21", self.html)
        self.assertIn("la reponemos sin costo", self.html)

    def test_precios_de_datos(self):
        self.assertIn(f"{dinero(datos.PRECIOS['pasto_solo_m2'])}/m²", self.html)
        self.assertIn(f"{dinero(datos.PRECIOS['mantenimiento_mes'])}/mes", self.html)

    def test_un_h1_y_foto_precargada_de_main(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)
        self.assertIn('rel="preload" as="image" href="/img/instalacion-pasto-rollo-san-agustin-tampico.webp"', self.html)


if __name__ == "__main__":
    unittest.main()
```

Run: `cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_protocolo 2>&1 | tail -1`. Expected: `FAILED (errors=1)`.

- [ ] **Step 2: Plantilla y contenido**

Crea `tools/site/plantillas/protocolo.py`:

```python
"""Plantilla del protocolo de cuidados de pasto San Agustín (spec §3.3, "HowTo visible"): cabecera con la foto de
producción → etapas de riego por días → señales → mantenimiento → condiciones de la garantía (#garantia) → contacto."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _lista(items):
    return '<ul class="vt-checks">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def _fases(fases):
    filas = "".join(f'<li class="vt-modo"><p class="vt-kicker">{f["dias"]}</p><h3>{f["titulo"]}</h3>{_lista(f["items"])}</li>'
                    for f in fases)
    return f'<ol class="vt-modos vt-fichas vt-util__fases">{filas}</ol>'


def _senales(items):
    return '<ul class="vt-modos vt-fichas">' + "".join(
        f'<li class="vt-modo"><h3>{s["titulo"]}</h3>{_lista(s["items"])}</li>' for s in items) + "</ul>"


def render(k):
    tipo, g, ci = k["tipo"], k["garantia"], k["cierre"]
    bloques = [
        cu.cabeza(k["cabeza"]),
        c.bloque(1, "Plan de cuidados", "vt-h-plan", k["plan"]["titulo"], _fases(k["plan"]["fases"]), lede=k["plan"]["lede"]),
        c.bloque(2, "Señales", "vt-h-senales", k["senales"]["titulo"], _senales(k["senales"]["items"]), tinte=True),
        c.bloque(3, "Después del día 20", "vt-h-mant", k["mantenimiento"]["titulo"], _lista(k["mantenimiento"]["items"])),
        c.bloque(4, "Garantía", "vt-h-garantia", g["titulo"], _lista(g["condiciones"]) + f'<p class="vt-promesa">{g["pie"]}</p>',
                 lede=g["lede"], tinte=True, id_seccion="garantia"),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    return base.documento(k["meta"], "\n".join(bloques), jsonld_bloques=k["jsonld"],
                          precargas=(base.precarga_imagen(k["cabeza"]["foto"]),), clase_body=CLASE_BODY)
```

Crea `tools/site/contenido/protocolo.py`:

```python
"""Contenido de /protocolo-cuidados-pasto-san-agustin: el plan de riego por días y las condiciones de la garantía, con las
palabras de main. La garantía usa la frase aprobada por el dueño (datos.GARANTIA_PASTO); $85 y $750 salen de datos.py.
Sin "experto", sin los contadores repetidos del hero y con un solo H1."""
import datos
import mensajes_paginas
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/protocolo-cuidados-pasto-san-agustin"
FOTO = {"src": "/img/instalacion-pasto-rollo-san-agustin-tampico.webp", "ancho": 1024, "alto": 1536, "alt": ""}
MENSAJE = mensajes_paginas.UTILITARIAS["protocolo"]
CONTENIDO = {
    "tipo": "posventa",
    "meta": {"title": "Protocolo de Cuidados · Pasto San Agustín · Viveros Terra",
             "description": "Protocolo completo para pasto San Agustín recién instalado: riego abundante y diario del día 1 al 20, señales de arraigo y condiciones de garantía. Viveros Terra Tampico.",
             "robots": "index, follow", "canonical": URL,
             "og": (("og:title", "Protocolo de Cuidados Pasto San Agustín · Viveros Terra"),
                    ("og:description", "Plan de riego y cuidados para pasto San Agustín recién instalado. Garantía de arraigo en 15 a 20 días. Viveros Terra Tampico."),
                    ("og:url", URL), ("og:type", "article"))},
    "cabeza": {"migas": (("Inicio", "/"), ("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Protocolo de cuidados", None)),
               "kicker": f"Protocolo de Cuidados · arraigo en {datos.ARRAIGO} · pasto desde {dinero(P['pasto_solo_m2'])}/m²",
               "h1": 'Cómo cuidar tu Pasto <span class="vt-serif">San Agustín paso a paso.</span>',
               "lede": ("Protocolo oficial de Viveros Terra para el cuidado del pasto San Agustín recién instalado. Riego, "
                        "fertilización, primera poda y control de plagas adaptados al clima de Tampico y Tamaulipas. El riego "
                        "lo haces tú: al terminar la instalación te explicamos cómo dar el primer riego y aquí tienes el "
                        "plan de los 20 días."),
               "foto": FOTO},
    "plan": {"titulo": 'Plan de Cuidados <span class="vt-serif">por Etapa</span>',
             "lede": (f"El pasto que instalamos fue <strong>cortado para tu pedido directamente del campo</strong>. Seguir este "
                      f"protocolo durante los primeros {datos.ARRAIGO} es lo que asegura que arraigue. <strong>Guarda este "
                      "documento.</strong>"),
             "fases": (
                 {"dias": "Días 1 – 7", "titulo": "Fase crítica de arraigo — la más importante", "items": (
                     "<strong>Riego abundante 2 veces al día:</strong> mañana (7–9am) y tarde (5–7pm). Riega hasta que el suelo esté húmedo a 5 cm de profundidad.",
                     "Aunque llueva, revisa que el suelo siga húmedo a 5 cm. Si no lo está, riega igual.",
                     "<strong>NO pisar el pasto</strong> bajo ninguna circunstancia — las raíces apenas están anclando.",
                     "<strong>NO podar ni cortar</strong> — el pasto necesita toda su energía para arraigar.",
                     "<strong>NO aplicar fertilizante</strong> — puede quemar las raíces nuevas.",
                     "<strong>NO aplicar herbicidas ni insecticidas</strong> sin consultarnos primero.")},
                 {"dias": "Días 8 – 14", "titulo": "Fase de consolidación", "items": (
                     "<strong>Riego abundante y diario</strong>, sin saltarte ningún día. De preferencia por la mañana, antes de las 10am.",
                     "Puedes verificar el arraigo: jala suavemente una esquina del pasto — si resiste y no se levanta, está pegando bien.",
                     "Si ves zonas más claras o amarillas, aumenta el riego en esa zona específica.",
                     "Sigue sin podar ni fertilizar.", "Evita pisoteo frecuente aunque ya haya arraigo parcial.")},
                 {"dias": "Días 15 – 20", "titulo": "Fase de establecimiento", "items": (
                     "<strong>Sigue con riego abundante y diario</strong> hasta el día 20. Es lo que asegura que el pasto termine de arraigar.",
                     "<strong>Primera poda</strong> cuando el pasto supere 8 cm de altura — no cortes más del 30% de la hoja en un solo corte.",
                     "Puedes aplicar fertilizante granulado ligero (triple 17 o similar) después del día 20.",
                     "El pasto ya puede pisarse con normalidad si el arraigo es completo.")},
             )},
    "senales": {"titulo": 'Señales <span class="vt-serif">a Identificar</span>', "items": (
        {"titulo": "Señales de buen arraigo", "items": (
            "Color verde intenso y parejo en toda el área", "Al jalar suavemente, el pasto resiste y no se levanta",
            "Nuevos brotes visibles en los bordes (runners)", "El suelo debajo se ve húmedo pero no encharcado")},
        {"titulo": "Señales de alerta — actúa de inmediato", "items": (
            "<strong>Parches amarillos:</strong> generalmente falta de agua. Aumenta el riego en esa zona y riega profundo.",
            "<strong>Parches café/seco:</strong> puede ser quemadura por sol intenso + calor. Riega de inmediato y considera malla de sombra temporal.",
            "<strong>Bordes que se levantan:</strong> las esquinas necesitan más agua. Riega 20 minutos extra en esa área.")},
        {"titulo": "Señales de problema — llámanos antes de actuar", "items": (
            "<strong>No arraiga después del día 20:</strong> contáctanos antes de hacer cualquier cambio. No apliques nada sin consultarnos.",
            "<strong>Zona completamente café y seca (más de 1 m²):</strong> llámanos ese mismo día con foto.",
            "<strong>Aparición de hongos o manchas oscuras:</strong> puede ser exceso de humedad — reduce el riego y avísanos.")},
    )},
    "mantenimiento": {"titulo": 'Mantenimiento <span class="vt-serif">a partir del día 21</span>', "items": (
        "<strong>Riego:</strong> 2–3 veces por semana en temporada seca. En lluvia, según necesidad.",
        "<strong>Poda:</strong> cada 10–15 días cuando el pasto alcance 8–10 cm. Altura ideal de corte: 4–5 cm.",
        "<strong>Fertilización:</strong> cada 2–3 meses con fertilizante granulado. En temporada de crecimiento (lluvia) puedes fertilizar más seguido.",
        "<strong>Control de maleza:</strong> retira manualmente las malas hierbas en cuanto aparezcan. Evita herbicidas de amplio espectro.",
        f'<strong>Si quieres un mantenimiento sin preocupaciones:</strong> pregúntanos por nuestro <a href="/mantenimiento-jardines-tampico">servicio mensual</a> desde {dinero(P["mantenimiento_mes"])}/mes.')},
    "garantia": {"titulo": 'Garantía de Arraigo <span class="vt-serif">— Condiciones</span>',
                 "lede": "Para que aplique la garantía de arraigo de Viveros Terra, se deben cumplir estas condiciones:",
                 "condiciones": (
                     "La instalación fue realizada por el equipo de Viveros Terra",
                     f"Se realizó riego abundante y diario los primeros {datos.ARRAIGO} según este protocolo",
                     "No hubo pisoteo durante los primeros 7 días",
                     "No se aplicaron productos químicos sin autorización previa",
                     "El problema fue reportado antes del día 21"),
                 "pie": (f"{datos.GARANTIA_PASTO.replace(' (ver condiciones)', '')} En caso de duda sobre si el problema aplica a "
                         f"garantía, contáctanos con foto. {datos.PROMESA}.")},
    "cierre": {"titulo": "¿Tienes dudas? Estamos aquí",
               "lede": (f"Mándanos foto de tu pasto por WhatsApp y te ayudamos con el diagnóstico y la solución. "
                        f"{datos.DOMICILIO_COMPLETO}."),
               "mensaje": MENSAJE},
    "jsonld": (),
}
PARIDAD = {
    "reemplazos": {"Protocolo de Cuidados": "Cómo cuidar tu Pasto San Agustín paso a paso."},
    "retirados": {},
    "jsonld": {},
}
```

- [ ] **Step 3: Registro y reglas**

En `generar.UTILITARIAS`: `("/protocolo-cuidados-pasto-san-agustin", "protocolo-cuidados-pasto-san-agustin.html", "protocolo", "protocolo"),`. Quita la ruta de `PENDIENTES`.

- [ ] **Step 4: Verde, build y paridad**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /protocolo-cuidados-pasto-san-agustin | grep -v ": ok"
cd tools/site && python3 -m unittest tests.test_protocolo tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_pasto_en_rollo 2>&1 | tail -1
```

Expected: `plantillas: 1 de 54`; solo la línea `== /protocolo…`; `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/plantillas/protocolo.py tools/site/contenido/protocolo.py tools/site/generar.py tools/site/tests/test_protocolo.py tools/site/tests/test_util_reglas.py public/protocolo-cuidados-pasto-san-agustin.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(protocolo): plantilla con etapas visibles y la garantía de arraigo aprobada" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 9: Plantilla `vivero`; se retiran `tools/servicios` y `servicios.css`

**Files:** crear `tools/site/plantillas/vivero.py`, `tools/site/contenido/vivero.py`, `tools/site/tests/test_vivero.py`; modificar `tools/site/generar.py`, `tools/site/ci/sitio.yml`, `tools/site/tests/{test_util_reglas,test_legacy_fixes,test_limpieza,test_terra_css,test_ci}.py`; borrar `tools/servicios/`, `public/css/servicios.css`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_vivero.py`:

```python
"""/vivero-tampico: domicilio, horario y precios de datos.py, FAQ visible igual al JSON-LD."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
from plantillas import vivero  # noqa: E402

K = generar.cargar("vivero").CONTENIDO


class ViveroTest(unittest.TestCase):
    def setUp(self):
        self.html = vivero.render(K)

    def test_domicilio_horario_y_mapa(self):
        for pieza in (datos.CALLE, datos.COLONIA, datos.HORARIO, datos.MAPS_URL):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, self.html)

    def test_precios_de_datos(self):
        self.assertIn(f"${datos.PRECIOS['palma_desde']}", self.html)
        self.assertIn(f"${datos.PRECIOS['pasto_solo_m2']}/m²", self.html)

    def test_faq_visible_igual_al_json_ld(self):
        grafo = json.loads(re.search(r'application/ld\+json">(.*?)</script>', self.html, re.S).group(1))["@graph"]
        faq = next(n for n in grafo if n["@type"] == "FAQPage")
        for q in faq["mainEntity"]:
            with self.subTest(pregunta=q["name"]):
                self.assertIn(q["name"], self.html)
                self.assertIn(q["acceptedAnswer"]["text"], self.html)

    def test_horas_del_negocio_de_datos_y_sin_instock(self):
        self.assertIn('"closes":"14:00"', self.html)
        self.assertNotIn("InStock", self.html)

    def test_una_sola_foto_de_main(self):
        self.assertEqual(re.findall(r'<img src="([^"]+)"', re.search(r"<main.*</main>", self.html, re.S).group(0)),
                         ["/img/portadas/arboles-tampico-viveros-terra-sm.webp"])


if __name__ == "__main__":
    unittest.main()
```

Run: `cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_vivero 2>&1 | tail -1`. Expected: `FAILED (errors=1)`.

- [ ] **Step 2: Plantilla y contenido**

Crea `tools/site/plantillas/vivero.py`:

```python
"""Plantilla de /vivero-tampico, "Visítanos" (spec §3.5): portada con la foto de producción y la etiqueta → dónde estamos →
categorías → cómo llegar y horario → buscar una planta → preguntas → CTA final. <body class="vt-pagina vt-util">."""
import componentes as c
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _datos(filas):
    return '<dl class="vt-util__datos">' + "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in filas) + "</dl>"


def render(k):
    tipo, f, ci = k["tipo"], k["faq"], k["cierre"]
    d, ca, l = k["donde"], k["categorias"], k["llegar"]
    bloques = [
        c.portada(k["portada"], tipo, k["migas"]),
        c.bloque(1, "Dónde estamos", "vt-h-donde", d["titulo"], c.fichas(d["hechos"]), lede=d["lede"], id_seccion="donde"),
        c.bloque(2, "Categorías", "vt-h-categorias", ca["titulo"], c.fichas(ca["items"]), lede=ca["lede"], tinte=True),
        c.bloque(3, "Visítanos", "vt-h-llegar", l["titulo"], _datos(l["datos"]), id_seccion="como-llegar"),
        c.bloque_dos(4, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    return base.documento(k["meta"], "\n".join(bloques), jsonld_bloques=k["jsonld"],
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), clase_body=CLASE_BODY)
```

Crea `tools/site/contenido/vivero.py`:

```python
"""Contenido de /vivero-tampico ("Visítanos"). La foto, título, meta, FAQ y JSON-LD de main; precios, horario y domicilio de
datos.py. Fuera (sin respaldo o contra una regla del dueño): "Lun–Sáb 9am–6pm" (el sábado cierra a las 14 h), "Variedades en
stock", "te decimos si la tenemos disponible", "precios orientativos", "precios más bajos" y "+18 años"."""
import datos
import mensajes_paginas
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/vivero-tampico"
FOTO = {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
        "srcset": "/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, /img/portadas/arboles-tampico-viveros-terra.webp 960w",
        "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 960, "alto": 1280,
        "alt": "Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico", "numero": 1,
        "lugar": "Siembra de árboles y plantas en Tampico", "etapa": "Equipo Viveros Terra"}
HORARIO = f"Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h"
DONDE = (f"Viveros Terra tiene su vivero en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero, con {datos.VARIEDADES} variedades "
         "de plantas, palmas, árboles ornamentales y plantas de interior, especies adaptadas al clima cálido-húmedo del Golfo de México.")
PREGUNTAS = (
    ("¿Dónde está el vivero en Tampico?", f"Viveros Terra está en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero — frente al Walmart de Madero. Atendemos de {HORARIO.lower()}."),
    ("¿Cuántas variedades de plantas tienen disponibles?", f"Contamos con más de 200 variedades entre plantas ornamentales, palmas tropicales y árboles para jardín."),
    ("¿Hacen entregas a domicilio en Tampico?", f"Sí, realizamos entregas en toda la zona metropolitana de Tampico, incluyendo Ciudad Madero y Altamira. Contáctanos por WhatsApp para coordinar la entrega y conocer su costo según tu colonia."),
    ("¿Puedo comprar plantas al mayoreo para mi proyecto?", "Sí. Atendemos tanto a clientes particulares como a constructoras, arquitectos, hoteles y empresas. Escríbenos por WhatsApp con tu requerimiento y te cotizamos por volumen."),
)
MENSAJE = mensajes_paginas.UTILITARIAS["vivero"]
CONTENIDO = {
    "tipo": "vivero",
    "meta": {"title": "Vivero en Tampico y Cd. Madero: dirección, horario y cómo llegar · Viveros Terra",
             "description": "Visita el vivero de Viveros Terra en Av. Álvaro Obregón 209 Sur, Cd. Madero, frente a Walmart. Más de 200 variedades de plantas, palmas y árboles. Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h.",
             "robots": "index, follow", "canonical": URL,
             "og": (("og:type", "website"), ("og:url", URL),
                    ("og:title", "Vivero en Tampico y Cd. Madero: dirección, horario y cómo llegar · Viveros Terra"),
                    ("og:description", "Vivero en Tampico con +200 variedades de plantas, palmas y árboles. Entrega en Madero y Altamira. Cotiza hoy."),
                    ("og:image", f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "migas": (("Inicio", "/"), ("Vivero en Tampico", None)),
    "portada": {"kicker": "Tampico · Madero · Altamira", "h1": 'Vivero en Tampico <span class="vt-serif">y Ciudad Madero, desde 2007</span>',
                "lede": f"Pasto, plantas, palmas, árboles y materiales para jardín en {datos.CALLE}, {datos.COLONIA}, Cd. Madero, frente a Walmart.",
                "etiqueta": {"codigo": "Vivero", "aviso": "Con IVA", "nombre": "Palmas", "antes": "desde", "monto": dinero(P["palma_desde"]),
                             "unidad": "", "filas": (("Pasto", f"{dinero(P['pasto_solo_m2'])}/m²"), ("Plantas", "por tamaño"))},
                "mensaje": MENSAJE, "tambien": f'<a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Cómo llegar</a>', "foto": FOTO},
    "donde": {"titulo": 'Viveros Terra en Ciudad Madero, <span class="vt-serif">frente a Walmart</span>', "lede": DONDE,
              "hechos": ({"titulo": f"{datos.VARIEDADES} variedades", "texto": "En el vivero"},
                         {"titulo": str(datos.DESDE), "texto": "Año de fundación"},
                         {"titulo": "30 días de garantía", "texto": f'En las plantas que sembramos nosotros. <a href="/politicas#garantia-plantas">Ver condiciones</a>.'})},
    "categorias": {"titulo": 'Categorías <span class="vt-serif">en el vivero</span>', "lede": "Plantas adaptadas al clima cálido-húmedo de Tampico.",
                   "items": (
                       {"titulo": '<a href="/palmas-tropicales-tampico">Palmas Tropicales</a>', "texto": "Palma del viajero, areca, coco, kentia, washingtonia y más. Adaptadas al clima de Tampico para sobrevivir en la zona costera."},
                       {"titulo": '<a href="/plantas-para-jardin-tampico">Plantas Ornamentales</a>', "texto": "Heliconias, bromelias, crotos, ficus, bugambilias y decenas de especies para jardines, interiores y terrazas."},
                       {"titulo": '<a href="/arboles-ornamentales-tampico">Árboles para Jardín</a>', "texto": "Árboles ornamentales, frutales y de sombra para jardines residenciales, corporativos y banquetas en Tampico."},
                       {"titulo": '<a href="/catalogo">Catálogo completo</a>', "texto": f"{datos.VARIEDADES} variedades con foto y descripción. Agrega lo que te interesa y cotiza todo en un WhatsApp."})},
    "llegar": {"titulo": 'Cómo llegar <span class="vt-serif">al vivero</span>',
               "datos": (("Dirección", f'{datos.CALLE}, {datos.COLONIA}, Ciudad Madero, Tamaulipas. {datos.REFERENCIA}. '
                                       f'<a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Abrir en Google Maps</a> · '
                                       f'<a href="https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&amp;q=Viveros%20Terra" target="_blank" rel="noopener">Apple Maps</a>'),
                         ("Horario de atención", datos.HORARIO),
                         ("Entrega a domicilio", "Entregamos en Tampico, Ciudad Madero y Altamira; te confirmamos el costo por WhatsApp según tu colonia."))},
    "faq": {"titulo": 'Preguntas frecuentes <span class="vt-serif">sobre el vivero</span>', "preguntas": PREGUNTAS},
    "cierre": {"titulo": '¿Buscas una planta <span class="vt-serif">específica?</span>',
               "lede": "Escríbenos con el nombre o una foto y te decimos qué opciones hay para tu espacio y el clima de Tampico.",
               "mensaje": mensajes_paginas.UTILITARIAS["vivero_planta"]},
    "jsonld": ({"@context": "https://schema.org", "@graph": [
        {"@type": "LocalBusiness", "name": datos.NOMBRE, "description": f"Vivero en Ciudad Madero con más de 200 variedades de plantas, palmas y árboles. Atendemos Tampico, Madero y Altamira desde {datos.DESDE}.",
         "telephone": datos.TELEFONO_TEL, "url": URL, "image": f"{SITE}/img/plantas-tropicales-tampico-viveros.png",
         "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"},
         "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": list(d), "opens": a, "closes": c} for d, a, c in datos.HORARIO_LD],
         "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Catálogo de plantas, palmas y árboles", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Product", "name": n}} for n in ("Palmas Tropicales", "Plantas Ornamentales", "Árboles para jardín")]}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PREGUNTAS]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                                                        {"@type": "ListItem", "position": 2, "name": "Vivero en Tampico", "item": URL}]},
        {"@type": "SpeakableSpecification", "cssSelector": ["h1", "h2", ".vt-faq summary"]}]},),
}
PARIDAD = {
    "reemplazos": {"Viveros Terra · Tampico": "Viveros Terra en Ciudad Madero, frente a Walmart",
                   "Categorías disponibles en el vivero": "Categorías en el vivero",
                   "Explora el catálogo completo del vivero": "Catálogo completo",
                   "¿Buscas una planta específica?": "¿Buscas una planta específica?"},
    "retirados": {},
    "meta": {"og:description": (CONTENIDO["meta"]["og"][3][1], "Sin “Productor directo”: el dueño no lo ha confirmado y 2d y 2f ya lo retiraron.")},
    "jsonld": {},
}
```

- [ ] **Step 3: Registro, reglas y build**

En `generar.UTILITARIAS`: `("/vivero-tampico", "vivero-tampico/index.html", "vivero", "vivero"),`. Quita `"/vivero-tampico"` de `PENDIENTES`.

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /vivero-tampico | grep -v ": ok"
grep -rl '/css/servicios' public --include='*.html' | wc -l
```

Expected: `plantillas: 1 de 55`; solo `== /vivero-tampico`; `0`.

- [ ] **Step 4: Retirar `tools/servicios` y `servicios.css`**

```bash
cd ~/dev/viverosterra-e2i
git rm -rq tools/servicios public/css/servicios.css
rm -rf tools/servicios
```

En `tools/site/ci/sitio.yml` borra el paso `Pruebas de servicios` (sus 3 renglones) y cambia el nombre del paso de dependencias a `Dependencias de prueba (Playwright; Pillow)`: Pillow se queda, lo usan `fotos_catalogo.py` y `miniaturas.py`. En `tests/test_ci.py` quita de la tupla `"python -m unittest discover -s tests -t tests", `. En `tests/test_terra_css.py`, `CSS_VIEJOS = ("design-system.css", "tailwind.css")`. En `tests/test_legacy_fixes.py`, `HOJAS = ("tailwind.css", "design-system.css", "legacy-fixes.css")`. En `tests/test_limpieza.py`, antes de `test_ds_store_y_pycache_fuera_de_git`:

```python
    def test_tools_servicios_y_servicios_css_retirados(self):
        """Etapa 2i: /vivero-tampico era la última página que salía de tools/servicios y usaba servicios.css."""
        self.assertFalse((RAIZ / "tools" / "servicios").exists())
        self.assertFalse((RAIZ / "public" / "css" / "servicios.css").exists())

```

`tools/site/corregir_datos.py` y dos comentarios de `mensajes_paginas.py` aún nombran `tools/servicios`: son historia y `corregir_datos` hace `glob` sobre la carpeta, que no falla si no existe. No los toques.

- [ ] **Step 5: Verde**

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_vivero tests.test_util_reglas tests.test_paridad tests.test_contenido tests.test_reglas tests.test_consistencia tests.test_legacy_fixes tests.test_limpieza tests.test_terra_css tests.test_ci tests.test_zona 2>&1 | tail -1
```

Expected: `OK`. En `test_util_reglas`, `PENDIENTES` ya está vacía: déjala como `frozenset()`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/plantillas/vivero.py tools/site/contenido/vivero.py tools/site/generar.py tools/site/ci/sitio.yml tools/site/tests/test_vivero.py tools/site/tests/test_util_reglas.py tools/site/tests/test_legacy_fixes.py tools/site/tests/test_limpieza.py tools/site/tests/test_terra_css.py tools/site/tests/test_ci.py public/vivero-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(vivero): página Visítanos con plantilla; se retiran tools/servicios y servicios.css" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 10: `404.html`

**Files:** crear `tools/site/plantillas/no_encontrada.py`, `tools/site/contenido/no_encontrada.py`, `public/js/vt-404.js`, `tools/site/tests/test_no_encontrada.py`; modificar `tools/site/generar.py`, `tools/site/tests/test_sitio.py`.

- [ ] **Step 1: Prueba en rojo**

Crea `tools/site/tests/test_no_encontrada.py`:

```python
"""404.html: noindex, buscador de servicios y enlaces que existen."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402
from plantillas import no_encontrada  # noqa: E402

K = generar.cargar("no_encontrada").CONTENIDO


class NoEncontradaTest(unittest.TestCase):
    def setUp(self):
        self.html = no_encontrada.render(K)

    def test_archivo_en_la_raiz_de_public_y_noindex(self):
        self.assertEqual(next(f for f in generar.PAGINAS if f[0] == "/404")[1], "404.html")
        self.assertEqual(K["meta"]["robots"], "noindex, follow")

    def test_buscador_con_etiqueta_y_lista_sin_js(self):
        self.assertIn('<label for="vt-buscar-404">', self.html)
        self.assertGreaterEqual(self.html.count("data-vt-servicio-404"), 12)
        self.assertIn('<script src="/js/vt-404.js" defer></script>', self.html)

    def test_todo_servicio_enlaza_a_una_pagina_real(self):
        for _texto, href in K["servicios"]:
            with self.subTest(href=href):
                archivo = paginas.PUBLIC / href.strip("/")
                self.assertTrue((archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file())

    def test_no_entra_al_sitemap(self):
        self.assertNotIn("/404<", (paginas.PUBLIC / "sitemap.xml").read_text(encoding="utf-8"))

    def test_un_h1(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)


if __name__ == "__main__":
    unittest.main()
```

Run: `cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_no_encontrada 2>&1 | tail -1`. Expected: `FAILED (errors=1)`.

- [ ] **Step 2: Plantilla, contenido y JavaScript**

Crea `tools/site/plantillas/no_encontrada.py`:

```python
"""Plantilla de 404.html (spec §4.x): dice qué pasó, filtra servicios sin salir de la página (vt-404.js; sin JS se ve la
lista completa) y ofrece WhatsApp. El menú y el pie los pone el shell. Vercel sirve 404.html en toda ruta sin archivo."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"
SCRIPTS = ("/js/vt-404.js",)


def render(k):
    filas = "".join(f'<li data-vt-servicio-404><a href="{c.esc(h)}">{t}</a></li>' for t, h in k["servicios"])
    buscador = (f'<section class="vt-bloque" aria-labelledby="vt-h-buscar"><div class="vt-wrap vt-util__estrecho">'
                f'<h2 id="vt-h-buscar">{k["buscar"]["titulo"]}</h2><div class="vt-campo"><label for="vt-buscar-404">'
                f'{k["buscar"]["label"]}</label><div class="vt-control"><input id="vt-buscar-404" type="search" '
                f'autocomplete="off" placeholder="{c.esc(k["buscar"]["placeholder"])}"></div></div>'
                f'<ul class="vt-util__servicios" id="vt-lista-404">{filas}</ul>'
                f'<p class="vt-promesa" id="vt-vacio-404" role="status" hidden>{k["buscar"]["vacio"]}</p></div></section>')
    ci = k["cierre"]
    return base.documento(k["meta"], "\n".join((cu.cabeza(k["cabeza"]), buscador, c.cierre(ci["titulo"], ci["lede"],
                          ci["mensaje"], k["tipo"]))), scripts=SCRIPTS, clase_body=CLASE_BODY)
```

Crea `tools/site/contenido/no_encontrada.py`:

```python
"""Contenido de 404.html: lo que sirve Vercel en toda ruta sin archivo (hoy, 79 bytes de texto plano). noindex."""
import datos
import mensajes_paginas

URL = f"{datos.SITIO}/404"
CONTENIDO = {
    "tipo": "utilidad",
    "meta": {"title": "Página no encontrada · Viveros Terra",
             "description": "Esta página no existe. Encuentra pasto, plantas, jardinería y materiales en Viveros Terra.",
             "robots": "noindex, follow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Error 404", "h1": 'No encontramos <span class="vt-serif">esa página.</span>',
               "lede": "Puede que el enlace haya cambiado. Busca lo que necesitas aquí abajo o escríbenos."},
    "buscar": {"titulo": "¿Qué estás buscando?", "label": "Busca un servicio o producto", "placeholder": "Ej. pasto, palmas, riego",
               "vacio": "No hay coincidencias. Escríbenos por WhatsApp y te ayudamos."},
    "servicios": (("Pasto en rollo San Agustín", "/pasto-en-rollo-tampico"), ("Pasto sintético en Tampico", "/pasto-sintetico-tampico"),
                  ("Tienda de pasto sintético", "/pasto-sintetico"), ("Diseño de jardines", "/diseno-jardines-tampico"),
                  ("Mantenimiento de jardines", "/mantenimiento-jardines-tampico"), ("Sistemas de riego", "/sistema-riego-tampico"),
                  ("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico"), ("Arma tu lista de plantas", "/catalogo"),
                  ("Tierra negra", "/tierra-negra-vegetal-tampico"), ("Tezontle rojo", "/tezontle-rojo-tampico"),
                  ("Mármol blanco", "/marmol-blanco-tampico"), ("Piedra bola de río", "/piedra-bola-rio-tampico"),
                  ("Mayoreo de pasto", "/mayoreo-pasto-tampico"), ("Precios", "/precios"), ("Visita el vivero", "/vivero-tampico"), ("Blog", "/blog")),
    "cierre": {"titulo": "¿No lo encuentras?", "lede": "Cuéntanos qué necesitas.", "mensaje": mensajes_paginas.UTILITARIAS["no_encontrada"]},
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
```

Crea `public/js/vt-404.js`:

```javascript
// public/js/vt-404.js
/* 404.html: filtra la lista de servicios mientras se escribe. Sin JS se ve la lista completa. */
(function () {
  'use strict';
  const campo = document.getElementById('vt-buscar-404');
  const lista = document.querySelectorAll('[data-vt-servicio-404]');
  const vacio = document.getElementById('vt-vacio-404');
  if (!campo || !vacio) return;
  const plano = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  campo.addEventListener('input', () => {
    const q = plano(campo.value.trim());
    let visibles = 0;
    lista.forEach((li) => {
      const ver = plano(li.textContent).includes(q);
      li.hidden = !ver;
      if (ver) visibles += 1;
    });
    vacio.hidden = visibles > 0;
  });
})();
```

- [ ] **Step 3: Registro**

En `generar.UTILITARIAS`: `("/404", "404.html", "no_encontrada", "no_encontrada"),`. En `tests/test_sitio.py`, `test_108_paginas_con_contexto` pasa a `test_109_paginas_con_contexto` y el número a `109`.

- [ ] **Step 4: Verde y build**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
cd tools/site && python3 -m unittest tests.test_no_encontrada tests.test_paridad tests.test_contenido tests.test_sitio tests.test_generar tests.test_enlaces 2>&1 | tail -1
```

Expected: `plantillas: 1 de 56`, `shell: 0 de 109` (el shell ya viene aplicado); `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/plantillas/no_encontrada.py tools/site/contenido/no_encontrada.py public/js/vt-404.js tools/site/generar.py tools/site/tests/test_no_encontrada.py tools/site/tests/test_sitio.py public/404.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(404): página con menú, buscador de servicios y WhatsApp" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 11: Pruebas de navegador

**Files:** crear `tools/site/tests/test_util_navegador.py`.

- [ ] **Step 1: Escribir y correr**

Crea `tools/site/tests/test_util_navegador.py`:

```python
"""Utilitarias en Chromium (Etapa 2i): axe de página completa, sin desbordar, consola limpia, y los flujos que el dueño
recibe: el cuestionario a formsubmit (interceptado: nunca sale un correo real), datos de envío a WhatsApp y el filtro de 404.
Se saltan sin Playwright."""
import base64
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
RUTAS = ("/politicas/", "/politica-privacidad/", "/gracias/", "/cuestionario.html", "/datos-envio/",
         "/protocolo-cuidados-pasto-san-agustin.html", "/vivero-tampico/", "/404.html")
AXE_TODO = """async () => {
  const r = await axe.run(document, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
SALIDOS = """() => { const w = document.documentElement.clientWidth;
  return Array.from(document.querySelectorAll('main *')).filter((e) => { const c = e.getBoundingClientRect();
    return c.width && c.height && getComputedStyle(e).visibility !== 'hidden' && (c.right > w + 0.5 || c.left < -0.5)
      && e.name !== '_honey'; }).map((e) => e.tagName + '.' + e.className); }"""


@unittest.skipIf(sync_playwright is None, "sin Playwright")
class UtilitariasNavegadorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.srv = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.nav = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.nav.close()
        cls.pw.stop()
        cls.srv.shutdown()
        cls.srv.server_close()

    def pagina(self, ancho=375):
        page = self.nav.new_page(viewport={"width": ancho, "height": 812})
        page.route("**googletagmanager.com/**", lambda r: r.abort())
        self.addCleanup(page.close)
        return page

    def test_axe_sin_serias(self):
        for ruta in RUTAS:
            with self.subTest(ruta=ruta):
                page = self.pagina(1440)
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(path=str(AXE))
                self.assertEqual(page.evaluate(AXE_TODO), [])

    def test_sin_desbordar(self):
        for ancho in (320, 375, 768, 1024, 1440, 1920):
            page = self.pagina(ancho)
            for ruta in RUTAS:
                with self.subTest(ruta=ruta, ancho=ancho):
                    page.goto(self.base + ruta, wait_until="load")
                    self.assertEqual(page.evaluate(SALIDOS), [])

    def test_consola_limpia(self):
        for ruta in RUTAS:
            page = self.pagina()
            errores = []
            page.on("pageerror", lambda e: errores.append(str(e)))
            page.on("console", lambda m: errores.append(m.text) if m.type == "error" and "ERR_FAILED" not in m.text else None)
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertEqual(errores, [])

    def test_gracias_manda_page_view_una_vez_y_ningun_evento(self):
        page = self.pagina(1440)
        page.goto(self.base + "/gracias/", wait_until="load")
        capa = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a))")
        self.assertEqual([a[:2] for a in capa if a[:1] == ["config"]], [["config", datos.GA4_ID]])
        self.assertEqual([a for a in capa if a[:1] == ["event"]], [])

    def _cuestionario(self, respuesta):
        page = self.pagina(1440)
        enviados = []
        def formsubmit(route):
            enviados.append((route.request.method, route.request.url, route.request.post_data))
            route.fulfill(status=respuesta[0], content_type="application/json", body=respuesta[1])
        page.route("https://formsubmit.co/**", formsubmit)
        page.goto(self.base + "/cuestionario.html", wait_until="load")
        return page, enviados

    def _hasta_el_final(self, page):
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        for _ in range(4):
            page.click("#btn-next")

    def test_no_avanza_sin_los_obligatorios(self):
        page, _ = self._cuestionario((200, '{"success":"true"}'))
        page.click("#btn-next")
        self.assertTrue(page.locator("#page-1").is_visible())
        self.assertFalse(page.locator("#page-2").is_visible())

    def test_solo_se_ve_un_paso(self):
        page, _ = self._cuestionario((200, '{"success":"true"}'))
        self.assertEqual(page.locator("[data-vt-paso]:visible").count(), 1)
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.click("#btn-next")
        self.assertEqual(page.locator("[data-vt-paso]:visible").count(), 1)
        self.assertEqual(page.locator("#step-counter").inner_text(), "Paso 2 de 5")

    def test_enter_a_medio_camino_no_envia(self):
        page, enviados = self._cuestionario((200, '{"success":"true"}'))
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.press("#whatsapp", "Enter")
        self.assertEqual(enviados, [])
        self.assertTrue(page.locator("#page-2").is_visible())

    def test_envio_a_formsubmit_y_aviso_en_la_pagina(self):
        page, enviados = self._cuestionario((200, '{"success":"true"}'))
        self._hasta_el_final(page)
        page.check('input[name="prioridad"][value="Fácil de mantener"]', force=True)
        page.click("#submit-btn")
        page.wait_for_selector("#success-screen:visible")
        self.assertEqual(len(enviados), 1)
        metodo, url, cuerpo = enviados[0]
        self.assertEqual((metodo, url), ("POST", f"https://formsubmit.co/ajax/{datos.CORREO_FORMULARIOS}"))
        for campo in ('name="nombre"', "María Ejemplo", 'name="_honey"', 'name="_subject"', "Fácil de mantener"):
            self.assertIn(campo, cuerpo)
        self.assertFalse(page.locator("#mainForm").is_visible())

    def test_si_falla_se_puede_reintentar(self):
        page, _ = self._cuestionario((500, "{}"))
        self._hasta_el_final(page)
        page.click("#submit-btn")
        page.wait_for_function("() => document.getElementById('submit-btn').textContent.includes('intenta de nuevo')")
        self.assertTrue(page.locator("#submit-btn").is_enabled())

    def test_riego_y_otro_condicionales_y_suma_de_areas(self):
        page, _ = self._cuestionario((200, '{"success":"true"}'))
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.click("#btn-next")
        self.assertFalse(page.locator("#cond-riego").is_visible())
        page.check('input[name="riego_instalado"][value="No"]', force=True)
        self.assertTrue(page.locator("#cond-riego").is_visible())
        page.check('input[name="riego_instalado"][value="Sí"]', force=True)
        self.assertFalse(page.locator("#cond-riego").is_visible())
        page.check("#rb-otro-esp", force=True)
        self.assertTrue(page.locator("#otro-esp-wrap").is_visible())
        page.fill("#area_pasto", "60")
        page.fill("#area_jard", "20")
        self.assertEqual(page.input_value("#area_total_input"), "80")

    def _envio(self, query=""):
        page = self.pagina()
        destino = []
        page.route("https://wa.me/**", lambda r: (destino.append(r.request.url), r.abort()))
        page.goto(self.base + "/datos-envio/" + query, wait_until="load")
        return page, destino

    def test_datos_de_envio_arma_el_mismo_mensaje_que_main(self):
        carga = {"n": "Ana López", "p": "Toscana 28", "f": "VT-1", "t": "$7,000", "s": "Jalisco", "c": "Zapopan", "z": "45000"}
        d = base64.urlsafe_b64encode(json.dumps(carga).encode()).decode().rstrip("=")
        page, destino = self._envio("?d=" + d)
        self.assertEqual(page.locator("#hola").inner_text(), "Hola Ana, ¿a dónde te lo enviamos?")
        self.assertTrue(page.locator("#order").is_visible())
        self.assertEqual(page.input_value("#estado"), "Jalisco")
        for campo, valor in (("#calle", "Hidalgo 1"), ("#colonia", "Centro"), ("#ref", "Frente a la farmacia"), ("#tel", "3310000000")):
            page.fill(campo, valor)
        with page.expect_request("https://wa.me/**"):
            page.click("#enviar")
        texto = unquote(destino[0])
        self.assertTrue(destino[0].startswith("https://wa.me/528333268008?text="))
        for pieza in ("Hola, aquí están mis datos de envío para el pedido VT-1:", "📍 *Dirección de entrega*", "Calle y número: Hidalgo 1",
                      "Municipio: Zapopan", "Código Postal: 45000", "📦 *Recibe*", "Nombre: Ana López", "🧾 Factura: no", "#VT1:"):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, texto)

    def test_datos_de_envio_marca_errores_y_no_abre_whatsapp(self):
        page, destino = self._envio()
        self.assertFalse(page.locator("#order").is_visible())
        page.click("#enviar")
        self.assertTrue(page.locator("#err").is_visible())
        self.assertTrue(page.locator("#calle.bad").count() == 1)
        self.assertTrue(page.locator("#calle ~ .msg, .vt-campo:has(#calle) .msg").first.is_visible())
        self.assertEqual(destino, [])

    def test_factura_se_despliega(self):
        page, _ = self._envio()
        self.assertFalse(page.locator("#fact").is_visible())
        page.check("#quiere")
        self.assertTrue(page.locator("#fact").is_visible())

    def test_filtro_de_404(self):
        page = self.pagina()
        page.goto(self.base + "/404.html", wait_until="load")
        total = page.locator("[data-vt-servicio-404]:visible").count()
        page.fill("#vt-buscar-404", "tezontle")
        self.assertEqual(page.locator("[data-vt-servicio-404]:visible").count(), 1)
        page.fill("#vt-buscar-404", "zzzz")
        self.assertTrue(page.locator("#vt-vacio-404").is_visible())
        page.fill("#vt-buscar-404", "")
        self.assertEqual(page.locator("[data-vt-servicio-404]:visible").count(), total)

    def test_anclas_de_politicas_llegan_bajo_el_menu(self):
        page = self.pagina(1440)
        for ancla in ("garantia-plantas", "garantia-pasto", "mensualidades", "devoluciones"):
            with self.subTest(ancla=ancla):
                page.goto(f"{self.base}/politicas/#{ancla}", wait_until="load")
                self.assertTrue(page.evaluate(
                    "(id) => { const c = document.getElementById(id).getBoundingClientRect(); return c.top >= 0 && c.top < 400; }", ancla))


if __name__ == "__main__":
    unittest.main()
```

```bash
cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_util_navegador 2>&1 | tail -3
```

Expected: `Ran 15 tests` (≈ 70 s) y `OK`.

- [ ] **Step 2: Confirmar que las pruebas detectan el fallo que importan**

La página carga la copia con hash, así que el cambio temporal va ahí:

```bash
cd ~/dev/viverosterra-e2i
sed -i '' 's/\.vt-util \[hidden\]{display:none}//' public/css/terra-util.*.css
(cd tools/site && python3 -m unittest tests.test_util_navegador.UtilitariasNavegadorTest.test_solo_se_ve_un_paso 2>&1 | tail -1)
git checkout -- public/css
```

Expected: `FAILED (failures=1)` y, tras restaurar, `git status --short` sin cambios.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2i
git add tools/site/tests/test_util_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): axe, desborde, cuestionario, datos de envío y 404 con envíos interceptados" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 12: Verificación final y puertas de revisión (merge y push los hace el controlador)

**Files:** `public/sitemap.xml` (lastmod) y las correcciones de los revisores, cada una con su prueba y su commit.

- [ ] **Step 1: `lastmod` de las páginas indexables**

```bash
cd ~/dev/viverosterra-e2i
HOY=$(date +%F)
for r in politicas politica-privacidad protocolo-cuidados-pasto-san-agustin vivero-tampico; do
  perl -0pi -e "s#(<loc>https://www\.viverosterra\.com/$r</loc>\s*<lastmod>)[^<]*#\${1}$HOY#" public/sitemap.xml
done
git diff --stat public/sitemap.xml
git add public/sitemap.xml
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore(sitemap): lastmod de las utilitarias indexables" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `1 file changed, 4 insertions(+), 4 deletions(-)`. `/gracias`, `/cuestionario`, `/datos-envio` y `/404` no entran al sitemap.

- [ ] **Step 2: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 56 páginas escritas` y `shell: 0 de 109 páginas actualizadas`; `0`; `OK` (`Ran 696 tests` en el prototipo; con la máquina muy cargada `test_tienda_navegador.test_aviso_arriba_de_la_barra_y_sin_tapar_los_botones` falló una vez a 320 px y pasó al repetirla sola, en código que 2i no toca: repite con `python3 -m unittest discover -s tests -p "test_tienda_navegador.py"` antes de investigar); `Ran 28 tests` y `OK`; `ℹ pass 67` y `ℹ fail 0`.

- [ ] **Step 3: Paridad, reglas y palabras a la vista**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/paridad.py informe /politicas /politica-privacidad /gracias /cuestionario /datos-envio /protocolo-cuidados-pasto-san-agustin /vivero-tampico | grep -vc ": ok"
grep -oiE "oasis|gratis|sin cargo|\bMSI\b|sin intereses|en stock|productor directo|fonts.googleapis|tailwind|design-system|servicios\.css|legacy-fixes|<style|window\.open|sendWA" \
  public/politicas/index.html public/politica-privacidad/index.html public/gracias/index.html public/cuestionario.html public/datos-envio/index.html public/protocolo-cuidados-pasto-san-agustin.html public/vivero-tampico/index.html public/404.html | sort | uniq -c
grep -rlE '/css/(tailwind|design-system|legacy-fixes)' public --include='*.html' | grep -vc '^public/blog/'
```

Expected: `7`; el `grep` vacío; `0` (lo único que sigue usando CSS viejo es el blog).

- [ ] **Step 4: Lighthouse móvil**

```bash
cd ~/dev/viverosterra-e2i
(cd public && python3 -m http.server 8771 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in politicas/ gracias/ cuestionario.html datos-envio/ protocolo-cuidados-pasto-san-agustin.html vivero-tampico/ 404.html; do
  n=$(echo $r | tr -d '/')
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8771/$r" --form-factor=mobile --only-categories=performance,accessibility --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2i-lh-$n.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2i-lh-$n.json"
done
pkill -f "http.server 8771"
```

Expected: Accessibility ≥ 98 y CLS < 0.1 en las 7 (bloquean). En el prototipo: A11y 100 en las 7, CLS 0; Performance 97–99 y LCP 2.0–2.6 s, salvo cuestionario (84, 4.5 s) y protocolo (87, 4.0 s), medidos con otra suite corriendo a la vez. Esas dos bajan por su foto de producción (1400×787 y 1024×1536 sin `srcset`): anota el valor y la causa, no recomprimas (pregunta 6).

- [ ] **Step 5: Capturas a 320, 375, 768, 1024, 1440 y 1920**

```bash
cd ~/dev/viverosterra-e2i/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
rutas = ('politicas/', 'politica-privacidad/', 'gracias/', 'cuestionario.html', 'datos-envio/', 'protocolo-cuidados-pasto-san-agustin.html', 'vivero-tampico/', '404.html')
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in rutas:
        for w in (320, 375, 768, 1024, 1440, 1920):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.screenshot(path=f"/tmp/vt-e2i-{r.strip('/').replace('.html', '')}-{w}.png", full_page=True)
            p.close()
    b.close()
srv.shutdown()
print(len(rutas) * 6, 'capturas')
PY
```

Expected: `48 capturas`. Revisa a mano: el índice de políticas a 375; la foto del cuestionario (está de lado en el archivo: pregunta 6); los 5 pasos y las píldoras a 320; la orden de datos de envío con `?d=`; el H1 de la cabecera en cada una. Guarda las aprobadas como referencia de regresión (hoja de ruta, cierre de la Etapa 2).

- [ ] **Step 6: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega la rama en verde y un resumen (`git log --oneline main..feat/etapa-2i`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2i --stat`, las plantillas, `componentes_util.py`, los 8 `contenido/`, `terra-util.css`, la vista previa de Vercel, `/tmp/vt-e2i-*.png`, `paridad.py informe` y el spec. Cada hallazgo: crítico, alto o medio, con archivo y arreglo.

1. **Diseño** (`design:design-critique` + `a11y-architect`): jerarquía de documento legal, índice, píldoras (foco y selección), asistente a 320, que `/gracias` se sienta confirmación y no página vacía, y 404 útil.
2. **SEO/AEO** (`seo-specialist` con `schema-markup`): meta intacta salvo las declaradas en `PARIDAD`; un H1; `noindex` en las tres de formulario y en 404; 404 con código 404 en vista previa; `FAQPage` de vivero = lo visible; sin adelantar la Etapa 3 ni la 4.
3. **CRO** (`general-purpose` con `form-cro`): el cuestionario no pierde a nadie (validación por paso, error reintentable, aviso final); `/gracias` deja claro qué sigue; 404 lleva a servicios y a WhatsApp.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): tabla C aplicada una por una; sin compromisos legales nuevos fuera de ella; reglas del dueño; contrato de formularios; `#VT1` intacto; que ninguna prueba toque formsubmit real.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 2 otra vez); los medios se corrigen o se anotan para el PR.

- [ ] **Step 7: Vista previa de Vercel (controlador)**

Con la URL de la vista previa `$P`:

```bash
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" "$P/no-existe-prueba-404"
curl -s "$P/no-existe-prueba-404" | grep -c 'No encontramos'
curl -s -o /dev/null -w "%{http_code}\n" "$P/gracias"
```

Expected: `404 text/html; charset=utf-8`, `1`, `200`. **Si el primero es `200`**, agrega a `vercel.json` una ruta final `{ "src": "/(.*)", "status": 404, "dest": "/404.html" }` con el formato que pida la configuración actual y repite (la guía oficial documenta esa forma para fijar el código). Si el dueño autoriza un envío de prueba, hazlo una sola vez desde el cuestionario y confirma que el correo llega con `_honey` vacío.

- [ ] **Step 8: Aprobación del dueño (controlador)**

Comparte la vista previa, las capturas y la tabla C, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Un cambio de texto legal que pida va en una tarea nueva con su prueba en `test_util_reglas`.

- [ ] **Step 9: Merge, push y despliegue (solo el controlador)**

Si el lote 5 se publica junto (2h + 2i), integra primero 2h con la Tarea 13. Si 2i va antes que 2h:

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2i -m "merge: etapa 2i — utilitarias con plantillas, políticas sin contradicciones y 404" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 56 …`, `shell: 0 de 109 …`, `0`.

- [ ] **Step 10: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in politicas politica-privacidad gracias cuestionario datos-envio protocolo-cuidados-pasto-san-agustin vivero-tampico; do
  printf "%s " $r; curl -s $W/$r | grep -cE "fonts.googleapis|/css/(tailwind|design-system|servicios|legacy-fixes)|<style"
done
curl -s -o /dev/null -w "%{http_code}\n" $W/no-existe-prueba-404
curl -s -o /dev/null -w "%{http_code}\n" $W/css/servicios.css
curl -s $W/politicas | grep -c 'id="garantia-pasto"'
```

Expected: `0` en las 7; `404`; `404`; `1`. En GA4 DebugView: un formulario de materiales o empresas manda `generate_lead` `formulario`, y al llegar a `/gracias` hay un solo `page_view` con esa URL. Confirma también que `/politicas#mensualidades` llega a su sección desde una ficha.

- [ ] **Step 11: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 2.

- [ ] **Step 12: Limpiar**

Solo si la Tarea 13 ya se hizo o no se hará en esta rama: `cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2i && git branch -d feat/etapa-2i`.

### Task 13: Cierre de la Etapa 2 (BLOQUEADA hasta que 2h esté en `main`)

**Precondición:** `git -C ~/dev/viverosterra branch --merged main | grep etapa-2h`. Sin esa línea, no empieces: `tailwind.css`, `design-system.css` y `legacy-fixes.css` siguen sosteniendo los 53 archivos del blog en producción. Se ensayó en una copia: fusión con los 9 choques de abajo, borrado y suites en verde (`727` pruebas de `tools/site`).

**Files:** crear `tools/site/tests/test_cierre_etapa2.py`; modificar `tools/site/{activos,partials,shell}.py`, `tools/site/activos.json`, `vercel.json` y pruebas; borrar `public/css/{tailwind,design-system,legacy-fixes}.css` (y copias con hash), `tools/site/{migrar_shell,huerfanos}.py`, `tools/site/tests/{test_migrar_shell,test_huerfanos,test_legacy_fixes}.py`.

- [ ] **Step 1: Traer `main` a la rama**

Si 2i ya se fusionó, crea una rama nueva desde `main` (`feat/cierre-etapa-2`) y salta al Step 3. Si no:

```bash
cd ~/dev/viverosterra-e2i && git fetch origin && git merge origin/main
```

Son 9 choques, todos del tipo "las dos ramas agregan algo al mismo sitio": `activos.py`, `activos.json`, `generar.py`, `partials.py`, `shell.py`, `tests/test_activos.py`, `tests/test_generar.py`, `tests/test_vercel.py` y `vercel.json`.

- [ ] **Step 2: Resolver los choques**

Guarda en `/tmp/resolver_2h.py` y córrelo desde la raíz del repo:

```python
"""Resuelve los choques de `git merge main` entre 2i y 2h: en los 9 archivos, las dos ramas agregan algo al mismo sitio."""
import re
from pathlib import Path

ARCHIVOS = ("tools/site/activos.py", "tools/site/activos.json", "tools/site/generar.py", "tools/site/partials.py",
            "tools/site/shell.py", "tools/site/tests/test_activos.py", "tools/site/tests/test_generar.py",
            "tools/site/tests/test_vercel.py", "vercel.json")
HUNK = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)


def unir(a, b):
    if "def head(" in a:
        return a.replace("util=False)", "util=False, blog=False)")
    if "util=UTIL in html" in a:
        return a.replace("util=UTIL in html)", "util=UTIL in html, blog=BLOG in html)")
    if "terra-util|legacy-fixes" in a:
        return a.replace("terra-util|legacy-fixes", "terra-util|terra-blog|legacy-fixes")
    if "+ UTILITARIAS" in a:  # generar.py
        return a.rstrip() + " " + b[b.rindex("+ _varias("):]
    if "generar.UTILITARIAS])" in a:  # test_generar.py, las utilitarias antes de los artículos
        return a.replace("UTILITARIAS])", "UTILITARIAS]") + b
    if '"terra-util.css": [' in a:  # activos.json
        return a + " ],\n" + b
    return a + b


for nombre in ARCHIVOS:
    p = Path(nombre)
    p.write_text(HUNK.sub(lambda m: unir(m.group(1), m.group(2)), p.read_text(encoding="utf-8")), encoding="utf-8")
```

```bash
cd ~/dev/viverosterra-e2i
python3 /tmp/resolver_2h.py
grep -rl '<<<<<<<' tools/site vercel.json | wc -l
python3 tools/site/build.py | tail -2
git add -A tools/site vercel.json public
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "merge: main con 2h en etapa 2i" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `0`; `plantillas: 0 de 109`, `shell: 0 de 109`. Si `generar.PAGINAS` no termina en `… + UTILITARIAS + _varias(\n    "articulo", …)`, corrígelo a mano antes del commit.

- [ ] **Step 3: Prueba en rojo**

Crea `tools/site/tests/test_cierre_etapa2.py`:

```python
"""Cierre de la Etapa 2 (2i, Tarea 13): ninguna página carga CSS viejo y toda página de public/ sale de una plantilla."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
SITE = Path(__file__).resolve().parents[1]
VIEJOS = re.compile(r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|tienda-pasto|legacy-fixes)\b|<style\b")


class CierreEtapa2Test(unittest.TestCase):
    def test_ninguna_pagina_carga_estilos_viejos(self):
        con_viejo = {p.relative_to(PUBLIC).as_posix(): VIEJOS.search(p.read_text(encoding="utf-8")).group(0)
                     for p in PUBLIC.rglob("*.html") if VIEJOS.search(p.read_text(encoding="utf-8"))}
        self.assertEqual(con_viejo, {})

    def test_hojas_viejas_borradas(self):
        for hoja in ("tailwind.css", "design-system.css", "servicios.css", "tienda-pasto.css", "legacy-fixes.css"):
            with self.subTest(hoja=hoja):
                self.assertFalse((PUBLIC / "css" / hoja).exists())
        self.assertEqual(list((PUBLIC / "css").glob("legacy-fixes.*.css")), [])

    def test_toda_pagina_sale_de_una_plantilla(self):
        registradas = {salida for _ruta, salida, _plantilla, _contenido in generar.PAGINAS}
        publicadas = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*.html")}
        self.assertEqual(publicadas - registradas, set())

    def test_migrador_del_shell_retirado(self):
        for modulo in ("migrar_shell.py", "huerfanos.py"):
            with self.subTest(modulo=modulo):
                self.assertFalse((SITE / modulo).exists())


if __name__ == "__main__":
    unittest.main()
```

Run: `cd ~/dev/viverosterra-e2i/tools/site && python3 -m unittest tests.test_cierre_etapa2 2>&1 | grep -E "^(FAIL|OK|Ran)"`. Expected: fallan `test_hojas_viejas_borradas` y `test_migrador_del_shell_retirado`; pasan `test_ninguna_pagina_carga_estilos_viejos` y `test_toda_pagina_sale_de_una_plantilla`. **Si esas dos no pasan, no borres nada:** alguna página sigue usando estilos viejos.

- [ ] **Step 4: Retirar**

Guarda en `/tmp/cierre.py` y córrelo desde la raíz:

```python
"""Retira legacy-fixes y el parámetro legacy del shell (Etapa 2i, Tarea 13). Correr desde la raíz del repo."""
import json
import re
from pathlib import Path


def cambia(ruta, *pares):
    p = Path(ruta)
    s = p.read_text(encoding="utf-8")
    for viejo, nuevo in pares:
        assert viejo in s, (ruta, viejo)
        s = s.replace(viejo, nuevo)
    p.write_text(s, encoding="utf-8")


def quita_prueba(ruta, nombre):
    p = Path(ruta)
    s = p.read_text(encoding="utf-8")
    m = re.search(rf"    def {nombre}\(self\):.*?(?=\n    def |\n\nclass |\n\nif __name__)", s, re.S)
    assert m, (ruta, nombre)
    p.write_text(s[:m.start()].rstrip() + "\n" + s[m.end():], encoding="utf-8")


cambia("tools/site/activos.py", ('    "legacy-fixes.css": "css/legacy-fixes.css",\n', ""),
       ("terra-precios.css, legacy-fixes.css, public/js/terra.js", "terra-precios.css, terra-util.css, terra-blog.css, public/js/terra.js"))
registro = Path("tools/site/activos.json")
datos = json.loads(registro.read_text(encoding="utf-8"))
del datos["legacy-fixes.css"]
registro.write_text(json.dumps(datos, indent=1) + "\n", encoding="utf-8")
cambia("tools/site/partials.py", ("def head(urls, legacy, tienda=False", "def head(urls, tienda=False"),
       ("CSS del shell (y legacy-fixes en páginas con Tailwind)", "CSS del shell"),
       ('''    if legacy:\n        lineas.append(f'<link rel="stylesheet" href="{urls["legacy-fixes.css"]}">')\n''', ""))
cambia("tools/site/shell.py", ('partials.head(urls, legacy="/css/tailwind.css" in html, tienda=', "partials.head(urls, tienda="))
cambia("vercel.json", ("terra-blog|legacy-fixes", "terra-blog"))
cambia("tools/site/tests/test_vercel.py", ("terra-blog|legacy-fixes", "terra-blog"))
cambia("tools/site/tests/test_sitio.py", ('("css", "terra.*.css"), ("css", "legacy-fixes.*.css"), ', '("css", "terra.*.css"), '))
cambia("tools/site/tests/test_terra_css.py", ('CSS_VIEJOS = ("design-system.css", "tailwind.css")', "CSS_VIEJOS = ()"))
cambia("tools/site/tests/test_activos.py",
       ('''        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")\n''', ""),
       ('''        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\\.[0-9a-f]{10}\\.css$")\n''', ""))
cambia("tools/site/tests/test_shell.py", ('''        self.assertIn("/css/legacy-fixes.0123456789.css", html)\n''', ""))
quita_prueba("tools/site/tests/test_partials.py", "test_legacy_fixes_solo_con_tailwind_y_antes_de_terra")
s = Path("tools/site/tests/test_partials.py").read_text(encoding="utf-8")
s = s.replace("partials.head(URLS, legacy=False)", "partials.head(URLS)").replace("partials.head(urls, False, ", "partials.head(urls, ")
Path("tools/site/tests/test_partials.py").write_text(s, encoding="utf-8")
```

```bash
cd ~/dev/viverosterra-e2i
python3 /tmp/cierre.py
git rm -q public/css/tailwind.css public/css/design-system.css public/css/legacy-fixes.css public/css/legacy-fixes.*.css tools/site/migrar_shell.py tools/site/huerfanos.py tools/site/tests/test_migrar_shell.py tools/site/tests/test_huerfanos.py tools/site/tests/test_legacy_fixes.py
python3 tools/site/build.py | tail -2
```

`medicion_js.py` se queda: `test_materiales_reglas.py` la usa.

- [ ] **Step 5: Verde, reproducible y commit**

```bash
cd ~/dev/viverosterra-e2i
python3 tools/site/build.py | tail -2
git status --porcelain -- public | grep -vc '^D'
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1)
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ fail"
git add -A tools/site vercel.json public
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore: cierre de la etapa 2, sin tailwind, design-system, legacy-fixes ni migrador del shell" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `plantillas: 0 de 109`, `shell: 0 de 109`, `0` (solo borrados), `OK`, `OK`, `ℹ fail 0`. Repite Task 12 Steps 3–10 sobre esta rama (Lighthouse A11y ≥ 98 por plantilla) con la aprobación del dueño; en vivo, `curl -s -o /dev/null -w "%{http_code}\n" https://www.viverosterra.com/css/tailwind.css` debe dar `404`.

---

## Lotes de ejecución sugeridos

| Lote | Tareas | Qué deja | Revisión intermedia |
|---|---|---|---|
| A · Fundaciones (ninguna página cambia) | 0–3 | Capturas, contrato, reglas en rojo, hoja y componentes | Cumplimiento: que las capturas sean de main y las reglas fallen por lo que deben |
| B · Legal y conversión | 4–5 | Políticas, aviso de privacidad y `/gracias` | Cumplimiento: tabla C una por una; medición de `/gracias` |
| C · Formularios | 6–7 | Cuestionario y datos de envío | QA: 74 controles y mensaje `#VT1` idénticos |
| D · Resto | 8–10 | Protocolo, vivero, 404; fuera `tools/servicios` y `servicios.css` | Paridad e informe por página |
| E · Cierre de 2i | 11–12 | Navegador, Lighthouse, capturas, 4 puertas, aprobación, merge | Las 4 puertas del spec §11 |
| F · Cierre de la Etapa 2 | 13 | Sin Tailwind, `design-system`, `legacy-fixes` ni migrador | **Solo con 2h en `main`**; repite las puertas |

## Correcciones a la hoja de ruta

- **Retirada de CSS:** la hoja de ruta la ponía en "el último commit de 2i". Con 2h sin fusionar no se puede: va en la Tarea 13, condicionada. `tienda-pasto.css` ya no existe (2g); `servicios.css` sí se va aquí.
- **`/gracias` y "resumen de lo calculado" (spec §5.2):** los 6 formularios llegan por `_next` de formsubmit a una URL fija, sin datos; un resumen pediría `sessionStorage` en cada origen por un beneficio menor. No se implementa; queda la promesa única y "Adelantar por WhatsApp".
- **Protocolo "HowTo visible":** etapas por días, sin nodo `HowTo` nuevo (Decisiones).
- **Página `/404` completa con enrutamiento:** no hace falta; Vercel usa `404.html`. El spec la ponía también en la Etapa 3: queda hecha aquí.
- **Honeypot del cuestionario:** la hoja de ruta decía "no cambiar `action` ni nombres". Se agrega `_honey` como en los otros 6 formularios (`test_campos…_mas_honeypot`) porque el encargo lo da por existente y no existía.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Se altera un campo que el dueño recibe | Contrato de 74 controles en `utilitarias-contrato.json` y prueba en orden; prueba de navegador con el cuerpo real del POST |
| `_honey` por `/ajax/` hace que formsubmit rechace el correo | Mismo nombre que los 6 formularios ya en producción, aunque esos no usan `/ajax/`; un envío de prueba autorizado por el dueño (Task 12 Step 7). Si falla, se quita el campo con su prueba |
| El mensaje `#VT1` cambia y el sistema del dueño no lo lee | El JS se copia casi literal; `test_el_mensaje_de_whatsapp_no_cambia` y prueba de navegador con `wa.me` interceptado |
| Se pierde la conversión de `/gracias` | Misma URL, título, canonical, robots y `gtag` único; `test_gracias_mide_igual_que_main`; revisión en DebugView |
| Una corrección legal cambia el sentido de la política | Tabla C limitada a contradicciones; todo lo demás, palabra por palabra; puerta de cumplimiento; aprobación del dueño |
| Vercel responde 200 en la 404 | Se mide en vista previa antes del merge; alternativa escrita |
| 404 suma una página a todos los conteos | `test_sitio` a 109; no entra al sitemap (`test_no_entra_al_sitemap`) |
| Merge con 2h | Ensayado: 9 choques aditivos con script |
| Fotos pesadas bajan Performance en cuestionario y protocolo | Regla de fotos; pregunta 6 |
| Una ancla se rompe | `test_anclas` de todo el sitio y prueba de navegador con el menú fijo |

## Preguntas al dueño

1. **Anticipo en envíos nacionales:** la página decía "se embarca al confirmarse el pago" y toda la tienda dice "después de confirmar el pago". En `/politicas` queda "para confirmar tu pedido… solicitamos un anticipo" y "la fecha de embarque te la confirmamos por WhatsApp". ¿Así funciona en pasto sintético por paquetería, o ahí el embarque sí espera el pago completo? Según la respuesta se ajusta también la tienda.
2. **Devoluciones:** la descripción de Google decía 30 días y el texto 7 días naturales. ¿Son 7?
3. **Plantas:** "la reponemos sin costo" pasa a "la reponemos", porque solo aprobaste "sin costo" para el pasto. ¿Lo dejamos así o apruebas la frase también para plantas?
4. **Cuestionario y medición:** hoy no llega a `/gracias` ni manda `generate_lead`: GA4 no lo cuenta. ¿Prefieres (a) dejarlo igual, (b) que mande `generate_lead` al enviarse, o (c) que al enviarse vaya a `/gracias`? El plan hace (a) y cualquiera de las otras son dos renglones en `vt-cuestionario.js`. También: ¿confirmas el campo honeypot nuevo?
5. **Aviso de privacidad:** se agregan como destinatarios paqueterías, el servicio de formularios y el procesador de pagos con tarjeta, sin nombrarlo. ¿Es correcto? Y recomendamos que tu abogado revise L1–L3 (ley de 2010 e INAI citados, cargo del 10% y cookies).
6. **Fotos:** la del cuestionario está **de lado** en el archivo publicado (hoy casi no se nota porque va de fondo; en la página nueva sí). ¿La rotamos? Y esa y la del protocolo pesan lo suficiente para bajar la velocidad en celular: ¿autorizas una copia más chica de la misma foto, como las `-sm` de las portadas?
7. **Efectivo:** `/politicas` decía efectivo en un lado y no en otro. ¿Aceptan efectivo en todas las ventas?
8. **`/gracias` en GA4:** ¿tienes configurada alguna conversión por visita a `/gracias`, además de `generate_lead`? No la cambiamos, pero conviene saberlo.
9. **Vivero:** ¿dejamos fuera "Productor directo"? No lo has confirmado y ya se quitó en otras páginas. Si lo es, se repone en todas a la vez.
10. **Fecha de las políticas:** dirán "Actualizado noviembre 2026" por los cambios de texto. ¿De acuerdo?
