# Etapa 2h · Blog: índice y 52 artículos con plantilla `articulo` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Octavo sub-plan de la Etapa 2 (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, §2h; spec `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §5, §6.5, §7, §8, §10, §11). Los 52 artículos de `/blog/{slug}` y el índice `/blog` dejan el HTML hecho a mano (Tailwind, `design-system.css`, Playfair desde Google Fonts, `<style>` propios, `sendWA`/`window.open`, 6 scripts distintos y tres envolturas) y salen de dos plantillas de `tools/site`: **`articulo`** (migas → H1 → autor y fecha → respuesta directa → cuerpo con índice al margen y Notas de campo → preguntas → enlaces contextuales → una etiqueta de "producto relacionado" → CTA a una landing → relacionados) y **`blog_indice`**. Las URLs, títulos, H1/H2, cuerpo, enlaces internos y fotos se quedan; lo único que cambia del texto es la lista documentada de correcciones (`contenido/blog_correcciones.py`, 212 correcciones en 30 artículos y el índice) para que nada contradiga `tools/site/datos.py` ni las reglas del dueño. Se publica en el lote 5 (2g + 2h + 2i) o sola, si el dueño la quiere antes.

**Architecture:** Igual que 2a–2g (`plantillas/<tipo>.py`, `contenido/<pagina>.py` con `CONTENIDO` y `PARIDAD`, `generar.PAGINAS`, shell solo si cambia), con la excepción que ya prevé la hoja de ruta para el volumen de prosa:
1. **`tools/site/extraer_blog.py`** (se corre **una vez**, lee siempre el commit `db6923e` con `git show`, nunca el `public/` ya migrado): analiza el `<main>` con `html.parser` de la biblioteca estándar, reconoce respuesta, cuerpo, notas, preguntas, CTA y relacionados en las tres envolturas, y escribe `contenido/blog/<slug>.html` (comentario con metadatos en JSON + cuerpo en HTML semántico, sin clases). Aplica las correcciones y se detiene si alguna no encuentra su texto.
2. **`contenido/blog_correcciones.py`**: `(texto exacto de antes, texto de después, motivo)` por artículo; cada precio de "después" sale de `datos.PRECIOS`.
3. **`contenido/articulo.py`** (`CLAVES`, `pagina(slug)`) lee esos archivos; el índice se arma de los `<h2>` del cuerpo, así no puede apuntar a un id inexistente. **`contenido/blog_clusters.py`** da a cada artículo su landing, su etiqueta y 2–3 enlaces contextuales.
4. **`public/css/terra-blog.css`** (5.9 KB, 1.5 KB con gzip), cableada como `terra-precios.css` (`activos.FUENTES`, `partials.head(blog=True)`, `shell.BLOG`, `vercel.json`, copia con hash e inmutable). `terra.css` no se toca (le quedan 35 B).
5. **`paridad_blog.py`** congela el texto visible y las fotos antes de tocar nada; `test_blog_paridad` exige que el artículo nuevo sea ese texto, palabra por palabra, salvo las correcciones.

**Tech Stack:** Python 3.9+ estándar, `unittest` y Pillow (ya en el proyecto, para `width`/`height` de las fotos); Playwright para Python 1.48 en navegador; CSS plano; ningún JavaScript nuevo (se reutiliza `terra.js`; las preguntas son `<details>`); Lighthouse 12 con `npx` solo en la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2h` (rama `feat/etapa-2h`, creada desde `main` en `db6923e`, con este plan como primer commit). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`.
- **Qué se probó y qué no.** El plan se prototipó sobre `db6923e` en un clon fuera del repo con **todo el código de las Tareas 1–8 tal como está aquí**: extracción de los 52 artículos y del índice sin intervención a mano, las 212 correcciones aplicadas sin ninguna sin coincidencia, build reproducible (segunda corrida: `0 de 101`), paridad de las 53 páginas en `ok` en las seis categorías, diff de texto palabra por palabra sin inserciones, y `tools/site` con 655 pruebas en verde (incluidas las 6 suites nuevas y las de navegador; `tools/pasto` con 28). `tools/servicios` y las pruebas de Node no se corrieron porque esta etapa no los toca. **No** se corrieron Lighthouse, las capturas de las seis anchuras ni las puertas de revisión (Tarea 10). Los archivos nuevos van completos; los cambios a archivos existentes van como reemplazos exactos en un script. Si una prueba no da lo que dice el plan, arregla el código (no la prueba) salvo que la prueba contradiga el spec; anota cada desvío en el PR.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests` (≈ 6 min), `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js`.
- `tools/site/extraer_blog.py escribir` **sobrescribe** `contenido/blog/`: después de la Tarea 6 los cambios de contenido van directo a esos archivos o, si la corrección se repite, a `blog_correcciones.py` seguida de una nueva extracción. No edites a mano un archivo y vuelvas a extraer.
- **Reglas del dueño en juego** (las prueban `test_reglas.py`, `test_consistencia.py` y la nueva `test_blog_reglas.py`):
  - **Precios solo de `datos.PRECIOS`** (y, para el sintético por modelo, de `tools/pasto/data.MODELOS`) o una multiplicación de ellos. Lo demás, "según cotización" (`datos.SEGUN_COTIZACION`). Areca y coco plumoso desde $250, palma real desde $500 en tamaño chico, flamboyán desde $250: ningún otro árbol o palma lleva precio. Tierra: costal $90, m³ $1,500, preparada $100, camiones de 5/8/14 m³ a $3,500/$5,200/$8,000. Mármol $250. Piedra bola a granel, sin medidas. `CALCULADOS` en `test_blog_reglas` lista lo que no es precio de Viveros Terra (el presupuesto del lector, la tarifa de agua de un ejemplo, un kit de ferretería) o es una multiplicación; solo puede encoger.
  - **Sin** SENASICA, "Oasis", proveedor de la terminal, "más vendid(a|o)" como afirmación en texto visible (los slugs `palmas-mas-vendidas-…` no cambian), "gratis"/"sin costo" (salvo la garantía de pasto aprobada, siempre con sus condiciones), estadísticas sin fuente, calificaciones inventadas, "En nuestro vivero". Visita nunca gratis y, donde se ofrece, con `datos.VISITA_COSTO`. Pago con anticipo (`datos.ANTICIPO_PROYECTOS`). Arraigo 15–20 días. Plantas: 30 días "con condiciones". Mensualidades "con tarjeta de crédito", nunca "MSI".
  - **Fotos:** las de producción, todas y en el mismo orden, sin agregar, quitar ni cambiar ninguna (20 artículos con una foto y 32 sin foto; 37 en el índice). El alt puede mejorar; nunca "En nuestro vivero". Por eso los 32 artículos sin foto no ganan foto ni las tarjetas de relacionados llevan miniatura.
  - **Autor:** `datos.AUTOR_BLOG` ("Equipo técnico de Viveros Terra"), el nombre editorial que dejó la Etapa 1; el dueño aceptó un nombre inventado, y este no suplanta a una persona. El `Organization` ligado a `#negocio` es de la Etapa 4.
  - **Títulos y meta:** se quedan, salvo las correcciones de arriba (`PARIDAD["meta"]` con motivo). La consolidación de títulos, los 301 y el `dateModified` general son de la Etapa 3/4. Solo los 30 artículos cuyo texto cambió llevan `dateModified` 2026-11-08 (cambiar la plantilla no es actualizar el artículo).
- Dos textos de CTA, como en 2a–2g: "Cotizar por WhatsApp" y "Llamar 833 326 8008"; el del artículo lleva además la landing. El mensaje de WhatsApp es el de `mensajes_paginas.BLOG` para cada artículo.

## Cobertura del spec y de la hoja de ruta

| Pide el spec / la hoja de ruta / el dueño | Dónde |
|---|---|
| §3.3 artículo: respuesta directa → autor y fecha → cuerpo con columna de margen y Notas de campo → 2–3 enlaces contextuales → etiqueta de producto → CTA a landing → relacionados | Tarea 6 (`plantillas/articulo.py`), `test_articulo.test_orden_de_secciones` |
| Hoja de ruta 2h: cuerpos extraídos una vez a `contenido/blog/<slug>.html` por un script con prueba | Tarea 2 (`extraer_blog.py`, `test_extraer_blog`) |
| Hoja de ruta 2h: paridad por post y diff de texto palabra por palabra | Tarea 1 (capturas), Tarea 7 (`test_blog_paridad`) |
| Hoja de ruta 2h: `SyntaxError` de scripts viejos, `h2{font-family:Playfair}` de 41 posts, `sendWA` | Desaparecen con los `<style>` y `<script>` (`test_articulo.VIEJO`) |
| Hoja de ruta 2h: mensajes de `mensajes_paginas.BLOG`; "flamboyán" y slugs `framboyan-…` intactos | `paginas.contexto`, `test_blog_navegador`, `test_consistencia` |
| Hoja de ruta 2h: `test_articulos_del_blog_sin_desbordar_a_375` | Se conserva; `test_blog_navegador` agrega 320 y 768 |
| Hoja de ruta 2h: sin bloque idéntico de 6–7 enlaces, un CTA a landing por post | `blog_clusters.py`, `test_articulo` |
| Spec §6.5: blogs de precios a `/precios`; sintéticos a las ciudades | `blog_clusters.A_PRECIOS`, `CIUDADES`, `test_articulo` |
| Conocido: anclas rotas del índice del artículo | Índice armado de los `<h2>`; `test_anclas` sin pendientes |
| Dueño: artículos con hoja propia, `terra.css` sin margen | Tarea 5 (`terra-blog.css`) |
| Dueño: oferta de la guía de palmas retirada | Ya no hay rastro en el blog (barrido); `test_guia_palmas` sigue |
| Barrido de afirmaciones | Sección de abajo, `blog_correcciones.py`, `test_blog_reglas` |
| Pruebas de lote: axe, sin desbordar 320–1920, consola limpia, Lighthouse, capturas | Tareas 8 y 10 |
| Puertas spec §11: diseño, SEO/AEO, CRO, cumplimiento | Tarea 10 |

Fuera de 2h: 301 y fusiones del spec §3.5 (`pasto-sintetico-para-perros`, `arboles-para-sembrar-en-banqueta`, riego, palmas: Etapa 3), retitular `pasto-san-agustin-instalacion-mantenimiento` y `diseno-jardines-tampico-guia` (Etapa 3), grafo JSON-LD único y `dateModified` de todo el sitio (Etapa 4), borrar `tailwind.css` y `design-system.css` (2i: las últimas páginas que los usan son utilitarias).

## Inventario de lo publicado (`db6923e`)

- **52 artículos + el índice = 53 páginas.** Tres envolturas: **A** (40 posts) hero en degradado, `article.prose` y `aside.sticky-sidebar`; **B** (8) `article[data-page="/blog"]` con `header.bg-dark`, `.answer-box`, `nav.toc`, `.article-prose` y `.faq-block`; **C** (4) hero claro, `article.max-w-3xl` y FAQ en sección aparte.
- **Marcado:** 11 hojas `<style>` distintas (más que variantes por los parches), 6 scripts distintos; `sendWA`/`window.open` en 18 posts; ningún `onclick`, formulario, `iframe` ni video. `style=""` en 23 posts (todos del hero o los CTA). 3 posts con dos `<h1>`.
- **Cuerpo:** 561 párrafos, 269 `<h2>`, 205 `<h3>`, 138 `<ul>`, 22 `<ol>`, 47 tablas, 55 notas (`tip-box`, `warn-box`, `highlight`, `calc-box`), 2 citas. **Preguntas:** 44 posts con 5 y 8 con 4, en tres marcados (`faq-btn`, `faq-block`, `h3`+`p`). El FAQPage del JSON-LD no coincide con lo visible en 74 preguntas (texto distinto o preguntas que no están en la página); 5 posts con FAQ visible no tenían FAQPage y 3 tenían FAQPage sin sección reconocible.
- **Respuesta directa:** 48 (4 de la envoltura C no tienen, y no se inventa). **Entrada (dek):** 44. **Relacionados:** 46 con 3, 5 con 2 y 1 con 1.
- **Fotos:** 20 posts con una, 32 sin ninguna; 37 en el índice. Los 4 de la envoltura C usan `../../img/`.
- **Autor:** 40 "Viveros Terra", 8 "Equipo Técnico Viveros Terra", 4 "Equipo Viveros Terra". **Fechas:** los 52 tienen `datePublished`; 8 no tienen `dateModified`; 12 no muestran fecha visible.
- **JSON-LD:** un bloque por post (`Article` con `Organization` anónima, `BreadcrumbList`, `FAQPage`; un `HowTo`).
- **Enlaces a anclas inexistentes:** 14 en `<a>`, en 3 posts (`cuando-plantar-pasto-tampico-calendario`, `plantas-resistentes-sal-golfo-tampico`, `sistema-riego-automatico-conviene-tampico`), que copiaron el índice del artículo de árboles; en esos mismos 3 la entrada también es la de árboles. Además 8 `<use href="#ic-…">` a símbolos que no existen (`ic-bolt` en 6 posts, `ic-leaf` en 1). Todo desaparece con la plantilla. (La hoja de ruta decía 5 posts: ver Correcciones.)
- **`/blog`:** 3 secciones (Para empezar, Nuevos artículos, Todos los artículos), 75 enlaces a 52 artículos, 37 fotos, métricas "18 años", "+900", "Gratis", botón "Preguntar al experto". 73 redirects de `vercel.json` llegan a artículos del blog; no cambian.

## Decisiones de diseño (y por qué)

- **Extracción a archivos, no plantilla sobre el HTML viejo.** Se consideraron tres caminos. (a) *Un módulo Python por post*: 52 archivos de prosa con comillas escapadas, ilegibles y sin ganancia. (b) *Plantilla que lea el HTML publicado en cada build*: el build sobrescribe `public/`, así que la fuente y el resultado serían el mismo archivo, y cada build arrastraría Tailwind. (c) *Extracción única a HTML semántico + metadatos* (la de la hoja de ruta). **Se elige (c)** porque es la de menor riesgo: la conversión ocurre una vez, el resultado queda en el repo y se puede leer y revisar artículo por artículo; el build deja de depender del HTML viejo; y `git show db6923e` garantiza que la extracción siempre parte de lo publicado. El análisis usa `html.parser` (sin dependencias) y una regla: lo que no se reconoce como envoltura se conserva. El candado es doble: una corrección sin coincidencia detiene todo y `test_blog_paridad` compara palabra por palabra.
- **Correcciones como datos.** Cada cambio de texto es una tripleta auditable. La diferencia entre lo publicado y lo nuevo debe ser exactamente esa lista, y el dueño puede revisarla entera en una página (la tabla del barrido).
- **Índice al margen, Notas de campo en su lugar.** El diseño de referencia tiene las notas en la columna de margen, pero mover esos textos cambiaría el orden de lectura (y en celular quedarían lejos de su contexto). Los 55 avisos se quedan donde estaban, con el tratamiento de Nota de campo; la etiqueta "Nota de campo" sale de CSS (`::before`), así no agrega texto al artículo. La columna de margen lleva el índice fijo.
- **Respuesta directa solo si existe.** Los 4 posts sin ella no la ganan aquí (redactarla es de la Etapa 4); los que decían "Lo más importante primero" conservan su rótulo.
- **FAQPage desde lo visible.** Se regenera de las preguntas de la página (spec §7.3); las que solo estaban en el JSON-LD salen con su motivo en `PARIDAD` y 5 posts ganan FAQPage. El resto del grafo (`Article`, `BreadcrumbList`, `HowTo`) se conserva con sus textos corregidos.
- **Fecha.** "Actualizado" usa `dateModified`; si no lo hay o es igual a la publicación, dice "Publicado". Sube a 2026-11-08 solo en los 30 artículos con correcciones.
- **Relacionados sin foto, índice con sus fotos.** Los relacionados de producción no tenían foto y no la ganan; las tarjetas del índice conservan las 37 en su orden, con `width`/`height` reales (CLS).
- **Etiqueta y CTA por tema.** 12 temas (`blog_clusters.py`). Donde no hay precio confirmado la etiqueta dice "Según cotización". Palma: etiqueta "desde $250" con la fila de palma real; el enlace lleva a la landing, no a un WhatsApp genérico, y el botón de WhatsApp conserva el mensaje del artículo.
- **Hoja propia.** Todo bajo `.vt-blog`. 5.9 KB; `test_terra_blog_css` fija el presupuesto (12 KB / 3 KB gzip).

## Barrido de afirmaciones

Se revisaron los 52 artículos, el índice, sus metas y su JSON-LD con patrones de precio, ahorro, porcentajes, antigüedad, garantías, visitas, pago, disponibilidad, entrega, superlativos, certificaciones y marcas. **Resultado por categoría** (212 correcciones en 30 artículos y el índice; lo que estaba en CTA o barra lateral no cuenta porque la plantilla lo reemplaza, y ahí estaban los 30 "Cotización gratis"):

| Categoría | Correcciones | Artículos |
|---|---|---|
| Precios de plantas sin confirmar → "según cotización" | 57 | 11 |
| Riego: rangos recalculados con $180–$320/m² | 31 | 6 |
| Casos, clientes e inversiones sin verificar → "ejemplo" | 24 | 6 |
| Porcentajes y estadísticas sin fuente | 20 | 9 |
| "Más vendida/o" fuera (slugs intactos) | 17 | 6 |
| Ahorro de agua: "hasta 40%" | 13 | 5 |
| Camión de tierra de 8 m³ a $5,200, no $12,000 | 8 | 2 |
| "Gratis" y "sin costo" | 7 | 7 |
| Garantías (sintético 3–8 años; plantas 30 días con condiciones; arraigo) | 7 | 5 |
| Pago: anticipo y avances, sin parcialidades | 2 | 2 |
| Visita con su costo; plazos y dato sin confirmar | 13 | 6 |
| Diseño, pasto, tezontle y mantenimiento con su precio oficial | 7 | 2 |
| Entrega por viaje; entrada copiada; voz | 6 | 5 |

**Limpio en el barrido:** SENASICA, "Oasis", proveedor de la terminal, MSI / "sin intereses", "En nuestro vivero", pádel, nota interna / Wix, reseñas y calificaciones (las ★ de `plantas-resistentes-sal-golfo-tampico` son la tolerancia a la sal de cada planta y `Toscana 28 ★` marca el modelo recomendado).

**Se deja tal cual, a propósito:**
- Antigüedad "más de 18 años" (3 posts): verdadera desde 2007; `test_consistencia` la permite.
- "+200 sistemas" de riego (`como-ahorrar-agua-jardin-tampico`): `datos.SISTEMAS_RIEGO`.
- Vida útil del producto ("10 a 20 años", "8 a 15 años"), distinta de la garantía.
- Datos de horticultura general: los estudios de la NASA sobre plantas de interior, "la palma de interior más popular del mundo", horas de sol, riegos por temporada, proporciones de sustrato, temperaturas.
- Porcentajes que son instrucciones o umbrales, no estadísticas ("retirar si más del 50% del cepellón quedó expuesto", "60% tierra negra", "poda del 30–40%").
- "Cotiza por WhatsApp para disponibilidad y precio actualizado": no promete existencias. Las afirmaciones concretas de existencia ("Tenemos palma del viajero…", "Tenemos ficus…", "ejemplares de 3 a 5 metros bajo consulta") pasan a la pregunta 9 al dueño.
- Cifras de ahorro y de costo de un ejemplo con su tarifa declarada (`$50/m³`) y artículos de ferretería (kit de pH, programador de manguera): no son precios de Viveros Terra (pregunta 7).
- Rangos de presupuesto ("$5K, $20K o $50K", "$15,000–$50,000"): son el presupuesto del lector; sus desgloses, con lo que no tiene precio confirmado, van "según cotización".

**Cada contradicción y su corrección** (texto reducido; el exacto está en `blog_correcciones.py`, Tarea 3):

| Artículo | Antes | Después | Motivo |
|---|---|---|---|
| `índice` | Las 8 palmas más vendidas en Tampico (con precios) | 8 palmas para jardines en Tampico (con precios) | "Más vendida" es un superlativo sin dato que l |
| `índice` | Palmas más vendidas Tampico precios | Palmas para jardines en Tampico | "Más vendida" es un superlativo sin dato que l |
| `índice` | La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y precio desde $500. | Crecimiento rápido y tolerancia total al calor. | "Más vendida" es un superlativo sin dato que l |
| `índice` | tolera luz baja, crece lento y tiene precio desde $500. | tolera luz baja y crece lento. | Precio sin confirmar por el dueño |
| `índice` | tolera sol pleno, sequía y lluvia intensa. Precio desde $500. | tolera sol pleno, sequía y lluvia intensa. Precio desde $250. | Coco plumoso |
| `índice` | de privacidad, con precio desde $300. | de privacidad, con precio desde $250. | Areca |
| `índice` | Cómo Ahorrar Hasta 50% de Agua | Cómo Ahorrar Hasta 40% de Agua | El ahorro oficial de agua es "hasta 40%" |
| `hongos-plantas-exceso-humedad` | Las tres medidas más efectivas y gratuitas son: | Las tres medidas más efectivas son: | Regla del dueño |
| `acolchado-mulch-jardin` | Casi gratis: aprovechas | Casi sin gasto: aprovechas | Regla del dueño |
| `arboles-para-sembrar-en-banqueta` | Si las aplicas, evitas el 90% de los problemas: | Si las aplicas, evitas la mayoría de los problemas: | Porcentaje sin fuente |
| `arboles-para-sembrar-en-banqueta` | En Viveros Terra hemos instalado más de 200 árboles de banqueta en Tampico, Madero y Altamira. El 95% de los problemas … | En las banquetas de Tampico, Madero y Altamira, la mayoría de los problemas que vemos | Cifra de árboles y porcentaje sin verificar. |
| `arboles-para-sembrar-en-banqueta` | Tip de experto: | Tip: | Sin "expertos" |
| `cesped-amarillo-causas-soluciones` | otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo. | otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo. El costo de la visi… | Toda mención de la visita lleva su costo |
| `como-ahorrar-agua-jardin` | reduciendo hasta un 50% el consumo hídrico | reduciendo hasta 40% el consumo hídrico | El ahorro oficial de agua es "hasta 40%" |
| `como-ahorrar-agua-jardin` | para reducir hasta 50% el consumo | para reducir hasta 40% el consumo | El ahorro oficial de agua es "hasta 40%" |
| `como-ahorrar-agua-jardin` | Aprende a reducir hasta 50% el consumo | Aprende a reducir hasta 40% el consumo | El ahorro oficial de agua es "hasta 40%" |
| `como-ahorrar-agua-jardin` | entre 30% y 50% respecto al riego manual | hasta 40% respecto al riego manual | El ahorro oficial de agua es "hasta 40%" |
| `como-ahorrar-agua-jardin` | Clientes de Viveros Terra en Tampico reportan ahorros de entre $150 y $600 pesos mensuales en el recibo de agua después… | Un sistema automático bien programado ahorra hasta 40% de agua frente a la manguera; lo que baja tu recibo depende del … | Testimonio y cifra sin verificar. |
| `como-medir-plantas-altura-cepellon` | puede orientarte sin costo antes de cotizar | puede orientarte antes de cotizar | Regla del dueño |
| `cuando-plantar-pasto-calendario` | ¿Cansado de banquetas destruidas por raíces? Guía de los 7 mejores árboles para banqueta en Tampico: dan sombra real si… | Calendario completo para sembrar pasto en Tampico mes a mes: cuál es el mejor mes, qué evitar y por qué septiembre es e… | La entrada era la del artículo de árboles de b |
| `cuando-plantar-pasto-calendario` | septiembre arraiga el 95% del pasto; julio puede arraigar solo el 60% por el calor extremo | en septiembre el pasto arraiga mucho mejor que en julio , por el calor extremo | Porcentaje sin fuente |
| `cuando-plantar-pasto-calendario` | aporta humedad gratis al suelo | aporta humedad natural al suelo | Regla del dueño |
| `cuando-plantar-pasto-calendario` | la tasa de mortandad sube al 30–40% | la mortandad sube mucho | Porcentaje sin fuente |
| `cuando-plantar-pasto-calendario` | la tasa de éxito baja al 60% sin riego intensivo | la tasa de éxito baja sin riego intensivo | Porcentaje sin fuente |
| `cuando-plantar-pasto-calendario` | reduce 70% el riego manual | reduce mucho el riego manual | Porcentaje sin fuente |
| `cuando-plantar-pasto-calendario` | puede duplicar la tasa de arraigo del pasto | mejora el arraigo del pasto | Porcentaje sin fuente |
| `cuando-regar-pasto-san-agustin` | En Viveros Terra instalamos sistemas desde $8,000 pesos; uno bien programado | En Viveros Terra instalamos sistemas de $180 a $320 por m²; uno bien programado | Riego instalado |
| `cuando-regar-pasto-san-agustin` | El problema real en el 70% de los casos es el riego | El problema real, en la mayoría de los casos, es el riego | Porcentaje sin fuente |
| `cuanto-cuesta-jardin-precios` | pasto $85/m², diseño desde $3K, riego, plantas. Cotiza gratis hoy. | pasto $85/m², diseño desde $3K, riego, plantas. Cotiza por WhatsApp. | Regla del dueño |
| `cuanto-cuesta-jardin-precios` | El costo de hacer un jardín en Tampico va desde $5,000 MXN para uno mini residencial hasta $200,000+ para premium. | Hacer un jardín en Tampico se cotiza según el proyecto; estas son referencias con los precios oficiales. | Rango total sin confirmar por el dueño. |
| `cuanto-cuesta-jardin-precios` | basados en proyectos ejecutados en Tampico, Madero y Altamira durante 2025 y lo que va de 2026. No son precios promedio… | con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira. El presupuesto final siempre se cotiza. | Dato sin verificar por el dueño. |
| `cuanto-cuesta-jardin-precios` | Palmas grandes ($1,000–$2,000 c/u), árboles ornamentales | Palmas grandes (según cotización), árboles ornamentales | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | 5 a 10 plantas ornamentales básicas: $200–$500 c/u | 5 a 10 plantas ornamentales básicas: según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | 1–3 palmas medianas ($500–$1,500 c/u) | 1–3 palmas medianas (según cotización) | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Riego automatizado completo con programador digital ($15,000–$60,000 según extensión) | Riego automatizado completo con programador digital ($180–$320/m²) | Riego instalado |
| `cuanto-cuesta-jardin-precios` | Ejemplo real: jardín de 30 m² | Ejemplo de presupuesto: jardín de 30 m² | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | 6 plantas ornamentales × $300 = $1,800 Mano de obra preparación + instalación = $2,000 Total estimado: $7,850 MXN | 6 plantas ornamentales: según cotización Mano de obra de preparación e instalación: según cotización Total: según cotiz… | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Ejemplo real: jardín de 120 m² con riego básico | Ejemplo de presupuesto: jardín de 120 m² con riego básico | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | 15 plantas + 2 palmas = $7,500 | 15 plantas + 2 palmas: según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Riego básico por aspersores = $6,000 Mano de obra total = $4,000 Total estimado: $36,700 MXN | Riego básico por aspersores: según cotización Mano de obra: según cotización Total: según cotización | Riego instalado |
| `cuanto-cuesta-jardin-precios` | Tierra negra 8 m³ = $12,000 5 palmas grandes + 20 plantas ornamentales = $18,000 | Tierra negra, camión de 8 m³ = $5,200 5 palmas grandes + 20 plantas ornamentales: según cotización | Camión de tierra de 8 m³ |
| `cuanto-cuesta-jardin-precios` | Riego automatizado completo 250 m² = $40,000 Tezontle, bordillos y acabados = $12,000 Mano de obra total = $10,000 Tota… | Riego automatizado completo 250 m²: $45,000–$80,000 Tezontle, bordillos y acabados: según cotización Mano de obra: segú… | Riego instalado |
| `cuanto-cuesta-jardin-precios` | Ejemplo: jardín premium 250 m² → $120,000 MXN | Ejemplo: jardín premium de 250 m² | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Pasto San Agustín (instalado) $85/m² Incluye mano de obra básica | Pasto San Agustín $85/m² solo pasto · desde $120/m² instalado El instalado incluye preparación básica y colocación | Precio oficial |
| `cuanto-cuesta-jardin-precios` | Camión 8 m³ desde $12,000 | Camión de 8 m³: $5,200 | Camión de tierra de 8 m³ |
| `cuanto-cuesta-jardin-precios` | Diseño Plan Terra Esencial $3,000–$6,000 | Diseño Plan Terra Esencial $3,000 | Diseño |
| `cuanto-cuesta-jardin-precios` | Diseño Plan Terra Completo $6,500–$18,000 | Diseño Plan Terra Completo $6,500 | Diseño |
| `cuanto-cuesta-jardin-precios` | Riego automatizado $15,000–$60,000 Según m² y número de zonas | Riego automatizado $180–$320/m² Según m² y número de zonas | Riego instalado |
| `cuanto-cuesta-jardin-precios` | Palmas pequeñas (hasta 1.5 m) $250–$600 c/u Areca, Kerpis, Cycas pequeñas | Palmas pequeñas (hasta 1.5 m) Desde $250 c/u Areca y coco plumoso; palma real desde $500; las demás, según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Palmas medianas (1.5–3 m) $600–$1,200 c/u | Palmas medianas (1.5–3 m) según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Palmas grandes (3 m+) $1,200–$2,500 c/u | Palmas grandes (3 m+) según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Mano de obra general ~$200/m² | Mano de obra general según cotización | Precio sin confirmar. |
| `cuanto-cuesta-jardin-precios` | Tezontle decorativo $35/kg o $280/costal | Tezontle decorativo Costal desde $200 | Tezontle |
| `cuanto-cuesta-jardin-precios` | 3 ejemplos reales de presupuestos | 3 ejemplos de presupuesto | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Caso A: Jardín residencial de 50 m² → ~$13,500 MXN | Ejemplo A: jardín residencial de 50 m² | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Cliente en Ciudad Madero con casa dúplex. Jardín frontal | Jardín frontal | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | 8 plantas × $350 = $2,800 Mano de obra = $3,000 Total: $13,050 MXN | 8 plantas: según cotización Mano de obra: según cotización Total: según cotización | Precio sin confirmar por el dueño |
| `cuanto-cuesta-jardin-precios` | Caso B: Jardín de 120 m² con riego básico → ~$35,000 MXN | Ejemplo B: jardín de 120 m² con riego básico | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Residencia en fraccionamiento de Tampico. Jardín trasero | Jardín trasero | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Diseño + instalación completa = $35,000 MXN aprox. | Diseño + instalación completa: según cotización | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Caso C: Jardín premium 250 m² con diseño Plan Terra Completo → ~$120,000 MXN | Ejemplo C: jardín premium de 250 m² con diseño Plan Terra Completo | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Casa en fraccionamiento privado de Altamira. Jardín integral | Jardín integral | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | Diseño + instalación integral = $120,000 MXN aprox. | Diseño + instalación integral: según cotización | Caso con cliente, cifra e inversión sin verifi |
| `cuanto-cuesta-jardin-precios` | va desde $750/mes para jardines pequeños hasta $3,500/mes para proyectos grandes. | va desde $750/mes, según el tamaño del jardín. | Mantenimiento |
| `cuanto-cuesta-jardin-precios` | Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN … | Viveros Terra no ofrece crédito propio. Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contr… | Pago |
| `cuanto-cuesta-jardin-precios` | y entrega una propuesta en menos de 48 horas. | y te entrega su propuesta. | Plazo sin confirmar por el dueño. |
| `cuanto-cuesta-pasto-sintetico-mexi` | es el más vendido: el mejor equilibrio entre precio y realismo | es un buen equilibrio entre precio y realismo | "Más vendida" es un superlativo sin dato que l |
| `cuanto-cuesta-pasto-sintetico-mexi` | Garantía (5 a 8 años): | Garantía (3 a 8 años): | Garantía del sintético |
| `cuanto-cuesta-pasto-sintetico-mexi` | Estos son tres ejemplos reales con envío | Estos son tres ejemplos con envío | Caso con cliente, cifra e inversión sin verifi |
| `errores-pasto-san-agustin` | Viveros Terra ofrece asesoría técnica gratuita sobre el protocolo correcto al momento de la compra o instalación. Para … | Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego (ver condiciones). E… | Garantía oficial de arraigo; sin "gratuita" ni |
| `framboyan-delonix-regia` | Ficus benjamina $200 | Ficus benjamina según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Trueno $300 | Trueno según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Neem $300 | Neem según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Tabachín $350 | Tabachín según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Laurel de la India $500 | Laurel de la India según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Tulipán Africano $600 | Tulipán Africano según cotización | Precio sin confirmar por el dueño |
| `framboyan-delonix-regia` | Precio desde | Precio | Precio sin confirmar por el dueño |
| `jardin-bajo-presupuesto` | 3 paquetes reales con detalle | 3 paquetes de ejemplo con detalle | Caso con cliente, cifra e inversión sin verifi |
| `jardin-bajo-presupuesto` | basados en proyectos que ejecutamos regularmente en Tampico, Madero y Altamira, | con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira, | Dato sin verificar por el dueño. |
| `jardin-bajo-presupuesto` | 6 plantas × $250 = $1,500 Mano de obra = $1,800 Total: aprox. $8,525 (ajustable según selección de plantas y área exact… | 6 plantas: según cotización Mano de obra: según cotización Total: según cotización (ajustable según selección de planta… | Precio sin confirmar por el dueño |
| `jardin-bajo-presupuesto` | 12 plantas × $300 + 2 palmas × $600 = $4,800 | 12 plantas + 2 palmas: según cotización | Precio sin confirmar por el dueño |
| `jardin-bajo-presupuesto` | Riego básico aspersores = $4,500 Mano de obra general = $3,000 Total: $27,450 (ajustable reduciendo área o número de pl… | Riego básico por aspersores: según cotización Mano de obra: según cotización Total: según cotización (ajustable reducie… | Riego instalado |
| `jardin-bajo-presupuesto` | 3 palmas medianas ($800–$1,500 c/u) | 3 palmas medianas (según cotización) | Precio sin confirmar por el dueño |
| `jardin-bajo-presupuesto` | Tierra negra 7 m³ = $10,500 25 plantas + 3 palmas medianas = $13,500 | Tierra negra 7 m³ = $10,500 25 plantas + 3 palmas medianas: según cotización | Precio sin confirmar por el dueño |
| `jardin-bajo-presupuesto` | Riego automatizado = $18,000 Árbol ornamental + acabados = $5,000 Mano de obra total = $8,000 Total: $75,100 (el presup… | Riego automatizado: según cotización Árbol ornamental + acabados: según cotización Mano de obra: según cotización Total… | Riego instalado |
| `jardin-bajo-presupuesto` | Según estudios de valuación inmobiliaria aplicados al mercado mexicano, un jardín profesional y en buen estado puede añ… | Un jardín profesional y en buen estado ayuda a vender o rentar una propiedad residencial. | Porcentaje sin fuente |
| `jardin-bajo-presupuesto` | Un jardín de $50,000 bien ejecutado en una casa de $1,500,000 puede representar una plusvalía de $75,000 a $225,000, co… | (se quita) | Porcentaje sin fuente |
| `jardin-bajo-presupuesto` | Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN … | Viveros Terra no ofrece crédito propio. Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contr… | Pago |
| `jardin-vertical-guia` | Un jardín vertical pequeño puede armarse desde $1,500 MXN . | Su costo depende del tamaño, la estructura y las plantas: se cotiza. | Precio sin confirmar. |
| `jardin-vertical-guia` | puede armarse desde $1,500 a $3,000 MXN . | se cotiza según lo que elijas. | Precio sin confirmar. |
| `jardin-vertical-guia` | puede armarse desde $1,500 a $3,000 MXN. | se cotiza según lo que elijas. | Precio sin confirmar. |
| `palma-areca` | en mata pequeña, y desde $800 MXN en matas grandes y densas. | en mata pequeña; las matas grandes y densas, según cotización. | Precio sin confirmar por el dueño |
| `palma-areca` | cuestan desde $800 MXN. | van según cotización. | Precio sin confirmar por el dueño |
| `palma-areca` | (desde $800) | (según cotización) | Precio sin confirmar por el dueño |
| `palma-areca` | tienen precio desde $800 MXN . | van según cotización . | Precio sin confirmar por el dueño |
| `palma-coco-plumoso` | para planta pequeña y desde $1,800 MXN para ejemplares adultos. | para planta pequeña; los ejemplares adultos, según cotización . | Precio sin confirmar por el dueño |
| `palma-coco-plumoso` | cuestan desde $1,800 MXN. | van según cotización. | Precio sin confirmar por el dueño |
| `palma-coco-plumoso` | tienen precio desde $1,800 MXN . | van según cotización . | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | tamaños y precios desde $500. La palma | y tamaños. La palma | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | tamaños y precios desde $500 para lobbies | y tamaños para lobbies | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | En Viveros Terra el precio va desde $500 MXN . | En Viveros Terra su precio va según cotización . | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | esquinas de habitación $500 MXN | esquinas de habitación según cotización | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | En Viveros Terra, una Palma Kerpis tiene precio desde $500 MXN. Ejemplares grandes y bien formados, ideales para lobbie… | En Viveros Terra, la Palma Kerpis va según cotización. | Precio sin confirmar por el dueño |
| `palma-kerpis-howea-forsteriana` | En Viveros Terra el precio de la Palma Kerpis inicia en $500 MXN . Ejemplares grandes y bien formados, con varios tallo… | En Viveros Terra el precio de la Palma Kerpis va según cotización , también en ejemplares grandes y bien formados, con … | Precio sin confirmar por el dueño |
| `palma-real-roystonea-regia` | cuestan desde $1,400 MXN. | van según cotización. | Precio sin confirmar por el dueño |
| `palma-real-roystonea-regia` | tienen precio desde $1,400 MXN . | van según cotización . | Precio sin confirmar por el dueño |
| `palma-washingtona` | y precios desde $500. La palma más vendida de la región. | y precios. Crecimiento rápido y resistencia al calor. | "Más vendida" es un superlativo sin dato que l |
| `palma-washingtona` | La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y la sequía, y precio desde $500 en Vi… | Crecimiento rápido y tolerancia total al calor y la sequía. | "Más vendida" es un superlativo sin dato que l |
| `palma-washingtona` | la Washingtonia robusta es, con diferencia, la palma más vendida en Tampico, Madero y Altamira. | la Washingtonia robusta es una palma muy común en Tampico, Madero y Altamira. | "Más vendida" es un superlativo sin dato que l |
| `palma-washingtona` | es la palma más vendida en Tampico : | es una palma muy resistente para Tampico : | "Más vendida" es un superlativo sin dato que l |
| `palma-washingtona` | En Viveros Terra el precio va desde $500 MXN para planta de 0.8–1.2 m. | En Viveros Terra su precio va según cotización , según la altura. | Precio sin confirmar por el dueño |
| `palma-washingtona` | En Viveros Terra, una planta de 0.8 a 1.2 m tiene precio desde $500 MXN. Ejemplares de 2 a 3 metros, con tronco ya defi… | En Viveros Terra, su precio va según cotización, según la altura. | Precio sin confirmar por el dueño |
| `palma-washingtona` | En Viveros Terra el precio de la Palma Washingtona inicia en $500 MXN para una planta de 0.8 a 1.2 metros. Ejemplares d… | En Viveros Terra el precio de la Palma Washingtona va según cotización , según la altura. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Las 8 palmas más vendidas en Tampico con precios 2026: Washingtona desde $500, Viajero $500, Areca $250, Coco, Real, Ke… | 8 palmas para jardines en Tampico con precios 2026: Areca y Coco Plumoso desde $250, Real desde $500; las demás, según … | "Más vendida" es un superlativo sin dato que l |
| `palmas-mas-vendidas-precios` | Las 8 palmas más vendidas en Tampico con precios 2026 | 8 palmas para jardines en Tampico con precios 2026 | "Más vendida" es un superlativo sin dato que l |
| `palmas-mas-vendidas-precios` | Las 8 palmas más vendidas en Tampico (con precios actualizados) | 8 palmas para jardines en Tampico (con precios actualizados) | "Más vendida" es un superlativo sin dato que l |
| `palmas-mas-vendidas-precios` | Palmas más vendidas Tampico | 8 palmas para Tampico | "Más vendida" es un superlativo sin dato que l |
| `palmas-mas-vendidas-precios` | Las 8 palmas más vendidas en Tampico son: Washingtona (desde $500), Palma del Viajero ($500), Areca ($250), Real, Coco … | Estas 8 palmas funcionan bien en Tampico: Areca y Coco Plumoso desde $250 y Real desde $500 en tamaño chico; Washington… | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Washingtona $500 | Washingtona según cotización | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Palma del Viajero $500 | Palma del Viajero según cotización | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Kerpis (Howea) $500 | Kerpis (Howea) según cotización | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Cycas Revoluta $700 | Cycas Revoluta según cotización | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Bambú Tarro $1,000 | Bambú Tarro según cotización | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Precio desde: $500 MXN (planta de 0.8–1.2 m). Ejemplares de 2–3 m desde $1,200. | Precio: según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Precio desde: $500 MXN (hijuelo pequeño). Plantas de 1.5–2 m desde $1,500. | Precio: según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Matas grandes y densas desde $800. | Matas grandes y densas, según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Ejemplares de 2 m desde $1,400. | Ejemplares de 2 m, según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Ejemplares adultos desde $1,800. | Ejemplares adultos, según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Precio desde: $500 MXN. Plantas grandes y bien formadas desde $1,200. | Precio: según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Precio desde: $700 MXN. Especímenes grandes (múltiples coronas) desde $3,500. | Precio: según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | Precio desde: $1,000 MXN (mata mediana). Matas grandes y densas desde $2,500. | Precio: según cotización. | Precio sin confirmar por el dueño |
| `palmas-mas-vendidas-precios` | La Washingtona es con diferencia la palma más vendida en la región. | La Washingtona es una palma muy común en la región. | "Más vendida" es un superlativo sin dato que l |
| `palmas-mas-vendidas-precios` | o contáctanos por WhatsApp para una asesoría sin costo. | o escríbenos por WhatsApp para asesorarte. | Regla del dueño |
| `palmas-mas-vendidas-precios` | tienen garantía de arraigo de 30 días: si no prenden y se regaron y cuidaron como indicamos, las reponemos sin costo. N… | tienen garantía de 30 días, con el riego indicado. No cubre falta de riego, cambio de lugar, daños por mascotas o clima… | Garantía de plantas |
| `palmas-tropicales-jardin` | Precio aproximado: desde $800 (planta) hasta $4,500 (adulta) | Precio: según cotización | Precio sin confirmar por el dueño |
| `palmas-tropicales-jardin` | Desde $800 pesos para planta pequeña de 40–60 cm, hasta $4,500+ para ejemplares adultos de 2–3 metros para impacto inme… | Va según cotización , según el tamaño: desde planta pequeña de 40–60 cm hasta ejemplares adultos de 2–3 metros para imp… | Precio sin confirmar por el dueño |
| `pasto-sintetico-calor-mexico` | (garantías de 5-8 años) | (garantías de 3 a 8 años según modelo) | Garantía del sintético |
| `pasto-sintetico-calor-mexico` | Por eso podemos dar garantía de 5 a 8 años según modelo. | Por eso podemos dar garantía de 3 a 8 años según modelo. | Garantía del sintético |
| `pasto-sintetico-calor-mexico` | (por eso ofrecemos garantía de 5 a 8 años según modelo) | (por eso ofrecemos garantía de 3 a 8 años según modelo) | Garantía del sintético |
| `pasto-sintetico-para-perros` | El más vendido para familias: suave | Para familias: suave | "Más vendida" es un superlativo sin dato que l |
| `pasto-sintetico-para-perros` | (28 mm, el más vendido para familias con mascotas) | (28 mm, para familias con mascotas) | "Más vendida" es un superlativo sin dato que l |
| `pasto-sintetico-para-perros` | Todos con garantía de 5-8 años y | Toscana 28, Irlanda 25, Capri 20 y Toscana 18 tienen garantía de 5 a 8 años según modelo y | Garantía del sintético |
| `pasto-sintetico-para-perros` | El 90% de los problemas de olor | La mayoría de los problemas de olor | Porcentaje sin fuente |
| `pasto-sintetico-vs-natural` | Instalación (50 m²) ~$8,000–$12,000 ~$18,000–$25,000 | Instalación (50 m²) desde $6,000 $19,250–$32,500 | Instalación con los precios oficiales por m². |
| `pasto-sintetico-vs-natural` | ~$92,000–$150,000 ~$18,000–$25,000 | ~$94,000–$182,000 $19,250–$32,500 | Suma recalculada con la instalación oficial. |
| `plantas-resistentes-sal-golfo` | ¿Cansado de banquetas destruidas por raíces? Guía de los 7 mejores árboles para banqueta en Tampico: dan sombra real si… | 12 especies de plantas que resisten la salinidad del aire marino en Tampico: ideales para jardines costeros, terrazas f… | La entrada era la del artículo de árboles de b |
| `plantas-resistentes-sal-golfo` | ¿Por qué la sal marina mata el 60% de las plantas? | ¿Por qué la sal marina mata tantas plantas? | Porcentaje sin fuente |
| `plantas-resistentes-sal-golfo` | La brisa salina del Golfo mata el 60% de las plantas comunes. | La brisa salina del Golfo mata muchas plantas comunes. | Porcentaje sin fuente |
| `plantas-resistentes-sal-golfo` | a más de 2 km del mar el efecto disminuye 80% | a más de 2 km del mar el efecto disminuye mucho | Porcentaje sin fuente |
| `plantas-resistentes-sal-golfo` | Más de 2 km de la costa el efecto de la sal disminuye 80%. | A más de 2 km de la costa el efecto de la sal disminuye mucho. | Porcentaje sin fuente |
| `plantas-resistentes-sal-golfo` | retiene 50% menos nutrientes | retiene menos nutrientes | Porcentaje sin fuente |
| `plantas-resistentes-sal-golfo` | pierde 80% del follaje | pierde buena parte del follaje | Porcentaje sin fuente |
| `que-altura-de-pasto-sintetico-eleg` | es el más vendido por algo: nadie se arrepiente | es buena opción por algo: nadie se arrepiente | "Más vendida" es un superlativo sin dato que l |
| `que-altura-de-pasto-sintetico-eleg` | es el modelo más vendido en México para uso residencial | es una opción muy equilibrada para uso residencial | "Más vendida" es un superlativo sin dato que l |
| `que-altura-de-pasto-sintetico-eleg` | Aquí vive el 90% de los jardines familiares . | Aquí cae la mayoría de los jardines familiares . | Porcentaje sin fuente |
| `riego-automatico-roi` | casos reales por tamaño de jardín. | ejemplos por tamaño de jardín. | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | casos reales de jardines en Tampico. | ejemplos de jardines en Tampico. | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | ~12–18 m³ (ahorro 40–60%) | ~18 m³ (ahorro de hasta 40%) | El ahorro oficial de agua es "hasta 40%" |
| `riego-automatico-roi` | ~$600–$900 MXN | ~$900 MXN | El ahorro oficial de agua es "hasta 40%" |
| `riego-automatico-roi` | $15,000–$60,000 MXN | $180–$320/m² | Riego instalado |
| `riego-automatico-roi` | $8,000–$15,000 Aspersores básicos o goteo | $5,400–$19,200 Aspersores básicos o goteo | Riego instalado |
| `riego-automatico-roi` | $15,000–$28,000 Aspersores emergentes + goteo zonas plantas | $10,800–$38,400 Aspersores emergentes + goteo zonas plantas | Riego instalado |
| `riego-automatico-roi` | $28,000–$45,000 Sistema mixto multi-zona con programador | $21,600–$64,000 Sistema mixto multi-zona con programador | Riego instalado |
| `riego-automatico-roi` | $45,000–$90,000 Sistema completo con controlador inteligente | $36,000–$160,000 Sistema completo con controlador inteligente | Riego instalado |
| `riego-automatico-roi` | $90,000+ | según cotización | Riego instalado |
| `riego-automatico-roi` | 3 casos reales de riego automático en Tampico | 3 ejemplos de riego automático en Tampico | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | Caso A: Residencial 80 m² en fraccionamiento de Madero | Ejemplo A: residencial de 80 m² | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | Caso B: Residencial 200 m² en fraccionamiento privado de Tampico | Ejemplo B: residencial de 200 m² | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | Caso C: Comercial 500 m² (oficinas corporativas en Altamira) | Ejemplo C: comercial de 500 m² | Caso con cliente, cifra e inversión sin verifi |
| `riego-automatico-roi` | Inversión: $18,000 MXN | Inversión: $14,400–$25,600 | Riego instalado |
| `riego-automatico-roi` | Inversión: $38,000 MXN | Inversión: $36,000–$64,000 | Riego instalado |
| `riego-automatico-roi` | Inversión: $85,000 MXN | Inversión: según cotización | Riego instalado |
| `riego-automatico-roi` | Consumo después: 10 m³/mes → $500/mes Ahorro mensual: $600 MXN Ahorro anual: $7,200 MXN | Consumo después: hasta 40% menos de agua | El ahorro oficial de agua es "hasta 40%" |
| `riego-automatico-roi` | Consumo después: 16 m³/mes → $800/mes Ahorro mensual: $1,200 MXN Ahorro anual: $14,400 MXN | Consumo después: hasta 40% menos de agua | El ahorro oficial de agua es "hasta 40%" |
| `riego-automatico-roi` | Consumo después: 36 m³/mes → $1,800/mes Ahorro mensual: $2,700 MXN Ahorro anual: $32,400 MXN | Consumo después: hasta 40% menos de agua | El ahorro oficial de agua es "hasta 40%" |
| `riego-automatico-roi` | Consumo automático: 15 m³/mes × $50/m³ = $750/mes Ahorro mensual: $750 MXN Ahorro anual: $750 × 12 = $9,000 MXN/año | Consumo automático: hasta 40% menos (18 m³/mes × $50/m³ = $900/mes) Ahorro mensual: $600 MXN Ahorro anual: $600 × 12 = … | El ahorro oficial de agua es "hasta 40%" |
| `sistema-riego-automatico-conviene` | ¿Cansado de banquetas destruidas por raíces? Guía de los 7 mejores árboles para banqueta en Tampico: dan sombra real si… | ¿Conviene un sistema de riego automático en el clima tropical de Tampico? Guía honesta: cuándo sí, cuándo no y cuánto c… | La entrada era la del artículo de árboles de b |
| `sistema-riego-automatico-conviene` | Para un jardín residencial de 100 m² el costo va de $15,000 (goteo simple) a $32,000 (sistema mixto con controlador WiF… | Para un jardín residencial de 100 m² el costo va de $18,000–$32,000. Para áreas comerciales o industriales con más de 5… | Riego instalado |
| `sistema-riego-automatico-conviene` | Costo en Tampico: $400–$800 por visita. | Costo: según cotización. | Precio sin confirmar. |
| `sistema-riego-automatico-conviene` | cuesta solo $3,000–$5,000 | se cotiza aparte | Precio sin confirmar. |
| `sistema-riego-automatico-conviene` | el costo del sistema ($15,000–$25,000) pesa más | el costo del sistema pesa más | Riego instalado |
| `sistema-riego-automatico-conviene` | $15,000–$25,000 (100 m²) | $18,000–$32,000 (100 m²) | Riego instalado |
| `sistema-riego-automatico-conviene` | $8,000–$18,000 (100 m²) | $18,000–$32,000 (100 m²) | Riego instalado |
| `sistema-riego-automatico-conviene` | $25,000–$45,000 (200 m²) | $36,000–$64,000 (200 m²) | Riego instalado |
| `sistema-riego-automatico-conviene` | +$4,000 al sistema | según cotización | Precio sin confirmar. |
| `sistema-riego-automatico-conviene` | Ejemplo real: cuánto se ahorra | Ejemplo: cuánto se ahorra | Caso con cliente, cifra e inversión sin verifi |
| `sistema-riego-automatico-conviene` | Cliente típico Viveros Terra (Cd. Madero, casa residencial): | Ejemplo de una casa residencial: | Caso con cliente, cifra e inversión sin verifi |
| `sistema-riego-automatico-conviene` | controlador WiFi = $32,000 | controlador WiFi = $27,000–$48,000 | Riego instalado |
| `sistema-riego-automatico-conviene` | Ahorro mensual: $130 en agua + $400 en tiempo (regaban 2 hrs/día en verano) | (se quita) | Caso con cliente, cifra e inversión sin verifi |
| `sistema-riego-automatico-conviene` | Adicional: el pasto se mantiene 60% más uniforme = no hay que comprar pasto nuevo en 5 años (ahorro $8,000+). | Adicional: el pasto se mantiene más uniforme. | Porcentaje sin fuente |
| `sistema-riego-automatico-conviene` | reduce el consumo de agua entre 35% y 45% | reduce el consumo de agua hasta 40% | El ahorro oficial de agua es "hasta 40%" |
| `sistema-riego-automatizado` | tiene un costo de instalación de $8,000 a $25,000 pesos dependiendo del tipo y complejidad. | tiene un costo de instalación de $180 a $320 por m² , según el tipo y la complejidad. | Riego instalado |
| `sistema-riego-automatizado` | Un sistema básico de aspersión para 50 m² cuesta entre $8,000 y $15,000 pesos instalado. Un sistema completo para jardí… | Un sistema básico de aspersión para 50 m² cuesta $9,000–$16,000 instalado. Un sistema completo para jardín grande de 10… | Riego instalado |
| `sistema-riego-automatizado` | Costo aproximado para 50 m²: $8,000–$15,000 | Costo aproximado para 50 m²: $9,000–$16,000 | Riego instalado |
| `sistema-riego-automatizado` | Costo aproximado para 20 plantas: $4,000–$10,000 | Costo: según cotización | Riego instalado |
| `sistema-riego-automatizado` | (ahorro hasta 60%) | (ahorro hasta 40%) | El ahorro oficial de agua es "hasta 40%" |
| `sistema-riego-automatizado` | $8,000–$15,000 $300–$600 | $9,000–$25,600 Hasta 40% menos de agua | Riego instalado |
| `sistema-riego-automatizado` | $4,000–$10,000 $200–$400 | según cotización Hasta 40% menos de agua | Riego instalado |
| `sistema-riego-automatizado` | $15,000–$28,000 $500–$1,000 | $18,000–$48,000 Hasta 40% menos de agua | Riego instalado |
| `sistema-riego-automatizado` | $40,000–$150,000 $2,000–$8,000 | según cotización Hasta 40% menos de agua | Riego instalado |
| `sistema-riego-automatizado` | Para un sistema de $12,000 pesos en un jardín residencial de 80 m²: | En un jardín residencial de 80 m²: | Riego instalado |
| `sistema-riego-automatizado` | Ahorro en agua: ~$500/mes = $6,000/año Ahorro en jardinero (menos idas para riego manual): ~$300/mes = $3,600/año Menor… | Ahorro en agua: hasta 40% Menos idas del jardinero para riego manual Menor mortalidad de plantas por riego inadecuado | Porcentaje sin fuente |
| `sistema-riego-automatizado` | Visita técnica. Medimos el área | Visita técnica. El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp… | Toda mención de la visita lleva su costo |
| `tierra-negra-costal-camion` | el camión volteo de 8 m³ a $1,500/m³ es más económico. | el camión volteo de 8 m³ en $5,200 es más económico. | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | Costo camión 8 m³ ($12,000) | Costo camión 8 m³ ($5,200) | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | $12,000 (8 m³ completo) | $5,200 (8 m³ completo) | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | $12,000 (cubre ~80 m²) | $5,200 (cubre ~80 m²) | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | $12,000–$24,000 | Desde $5,200 | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | se puede incluir en el mismo pedido de plantas sin costo de envío adicional | se puede incluir en el mismo pedido de plantas | La entrega se cobra por viaje, según la coloni |
| `tierra-negra-costal-camion` | Las entregas de camión tienen costo de flete según la distancia. Los costales se pueden incluir en pedidos de plantas o… | La entrega a domicilio se cobra por viaje, según tu colonia. | La entrega se cobra por viaje, según la coloni |
| `tierra-negra-costal-camion` | más del doble que el camión ($1,500/m³) | más del doble que el m³ suelto ($1,500/m³) | Camión de tierra de 8 m³ |
| `tierra-negra-costal-camion` | Un costal estándar de tierra negra vegetal en Viveros Terra pesa aproximadamente 25–30 kg y tiene un volumen de 25–30 l… | No publicamos el peso porque varía con la humedad; un costal estándar de tierra negra vegetal en Viveros Terra tiene un… | Sin peso de costal |

Además, en todos los artículos y tarjetas que enlazan la guía de palmas (`TODOS`):

| Antes | Después |
|---|---|
| Las 8 Palmas Más Vendidas en Tampico (con Precios) | 8 Palmas para Jardines en Tampico (con Precios) |
| las 8 palmas más vendidas en Tampico con precios actualizados | 8 palmas para jardines en Tampico con precios actualizados |
| lista de las 8 palmas más vendidas en Tampico | lista de 8 palmas para jardines en Tampico |
| las palmas más vendidas en Tampico con precios | las 8 palmas para jardines en Tampico con precios |
| palmas más vendidas en Tampico con precios | palmas para jardines en Tampico con precios |
| palmas más vendidas en Tampico | palmas para jardines en Tampico |
| La palma más vendida de la región: crecimiento rápido y precio desde $500. | Crecimiento rápido y tolerancia al calor y la sequía. |
| La palma más vendida de la región, con su característica faldilla de hojas secas. | Crecimiento rápido, con su característica faldilla de hojas secas. |

## File structure

Se crean:

| Archivo | Responsabilidad |
|---|---|
| `tools/site/tests/paridad/blog.json`, `blog_<slug>.json` (53) | Captura de `paridad.py` (meta, JSON-LD, encabezados, preguntas, precios, enlaces). |
| `tools/site/paridad_blog.py`, `tools/site/tests/paridad/blog-texto/<slug>.txt` (52), `blog-fotos.json` | Texto visible y fotos en orden, congelados antes de migrar. |
| `tools/site/extraer_blog.py` | Extracción única desde `db6923e`. |
| `tools/site/contenido/blog_correcciones.py` | Las 212 correcciones. |
| `tools/site/contenido/blog_clusters.py` | Tema, landing, etiqueta y enlaces de cada artículo. |
| `tools/site/contenido/articulo.py`, `tools/site/contenido/blog_indice.py` | Contenido de las plantillas. |
| `tools/site/contenido/blog/<slug>.html` (52), `_indice.json` | Lo extraído. |
| `tools/site/componentes_blog.py`, `tools/site/plantillas/articulo.py`, `tools/site/plantillas/blog_indice.py` | Componentes y plantillas. |
| `public/css/terra-blog.css` | Hoja del blog. |
| `tools/site/tests/{test_extraer_blog,test_blog_paridad,test_blog_reglas,test_articulo,test_terra_blog_css,test_blog_navegador}.py` | Pruebas nuevas. |

Se modifican: `tools/site/{activos,partials,shell,generar}.py`, `vercel.json`, `public/sitemap.xml` (lastmod de los corregidos y del índice), `tools/site/capturas.py`; pruebas `test_activos`, `test_partials`, `test_vercel`, `test_generar`, `test_contenido`, `test_anclas`, `test_navegador` (sale `test_window_open_de_whatsapp_sale_firmado`: ya no hay `sendWA` en el sitio). Regenerados por el build: las 53 páginas, `public/css/terra-blog.<hash>.css` y `tools/site/activos.json`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar el worktree**

```bash
cd ~/dev/viverosterra-e2h && git branch --show-current && git log --oneline -2
```

Expected: `feat/etapa-2h`; arriba el commit de este plan (`docs(plan): etapa 2h blog`) y debajo `db6923e merge: etapa 2g — zonas y lista de precios con plantillas`.

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2h
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright, PIL; print('ok')"
```

Expected: `plantillas: 0 de 48 páginas escritas`, `shell: 0 de 108 páginas actualizadas`; `0`; `OK`; `ok`.

---

### Task 1: Capturas de paridad, texto y fotos

**Files:** Create: `tools/site/paridad_blog.py`, `tools/site/tests/paridad/blog*.json`, `tools/site/tests/paridad/blog-texto/*.txt`, `tools/site/tests/paridad/blog-fotos.json`

- [ ] **Step 1: Escribir `tools/site/paridad_blog.py`**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site
cat > tools/site/paridad_blog.py <<'VT_EOF'
"""Paridad del texto y de las fotos del blog (Etapa 2h). paridad.py congela encabezados, preguntas, precios y enlaces, pero
no la prosa ni las imágenes: aquí se guarda el texto visible del <main> de cada artículo tal como se publicaba
(tests/paridad/blog-texto/<slug>.txt) y la lista ordenada de sus <img> (tests/paridad/blog-fotos.json). test_blog_paridad
exige que el texto del artículo nuevo sea el mismo, palabra por palabra, salvo las correcciones documentadas.

Uso: python3 tools/site/paridad_blog.py capturar   (antes de tocar los artículos)
"""
import difflib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

DIR_TEXTO = paridad.CAPTURAS / "blog-texto"
FOTOS = paridad.CAPTURAS / "blog-fotos.json"


def slugs(public=paridad.paginas.PUBLIC):
    return sorted(p.parent.name for p in (Path(public) / "blog").glob("*/index.html"))


def texto_main(html):
    return paridad.texto(paridad.principal(html))


def capturar(public=paridad.paginas.PUBLIC):
    DIR_TEXTO.mkdir(parents=True, exist_ok=True)
    fotos = {"/blog": paridad_materiales.fotos(paridad.archivo("/blog", public).read_text(encoding="utf-8"))}
    for slug in slugs(public):
        html = paridad.archivo(f"/blog/{slug}", public).read_text(encoding="utf-8")
        (DIR_TEXTO / f"{slug}.txt").write_text(texto_main(html) + "\n", encoding="utf-8")
        fotos[f"/blog/{slug}"] = paridad_materiales.fotos(html)
    FOTOS.write_text(json.dumps(fotos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return fotos


def viejo_corregido(slug, correcciones):
    """Texto capturado con las correcciones aplicadas (viejo y nuevo reducidos a texto, igual que la captura)."""
    t = (DIR_TEXTO / f"{slug}.txt").read_text(encoding="utf-8").strip()
    for viejo, nuevo, _motivo in correcciones:
        t = t.replace(paridad.texto(viejo), paridad.texto(nuevo))
    return t


def cuerpo_nuevo(html):
    """Texto del <article> (respuesta, cuerpo y preguntas), sin el bloque "Para seguir" que agrega la plantilla."""
    m = re.search(r'<article class="vt-art__cuerpo".*?</article>', html, re.S)
    sin_sigue = re.sub(r'<nav class="vt-art__sigue".*?</nav>', " ", m.group(0), flags=re.S)
    return paridad.texto(sin_sigue)


def diferencias(viejo, nuevo):
    """(insertado, borrado): tramos de palabras que están solo en el artículo nuevo y solo en el viejo."""
    a, b = viejo.split(), nuevo.split()
    insertado, borrado = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op in ("replace", "delete"):
            borrado.append(" ".join(a[i1:i2]))
        if op in ("replace", "insert"):
            insertado.append(" ".join(b[j1:j2]))
    return insertado, borrado


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_blog.py capturar")
    print(len(capturar()), "páginas")
VT_EOF
```

- [ ] **Step 2: Capturar las 53 páginas tal como están**

```bash
cd ~/dev/viverosterra-e2h
python3 tools/site/paridad.py capturar /blog $(ls public/blog | grep -v index.html | sed 's#^#/blog/#')
python3 tools/site/paridad_blog.py capturar
ls tools/site/tests/paridad | grep -c '^blog'; ls tools/site/tests/paridad/blog-texto | wc -l
```

Expected: 53 líneas `captura: …`, `53 páginas`; `55` (53 capturas + `blog-texto` + `blog-fotos.json`) y `52`.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/paridad_blog.py tools/site/tests/paridad/blog*.json tools/site/tests/paridad/blog-texto
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(blog): capturas de paridad, texto y fotos antes de migrar" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Extractor con prueba

**Files:** Create: `tools/site/tests/test_extraer_blog.py`, `tools/site/extraer_blog.py`

- [ ] **Step 1: Escribir la prueba (RED)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/tests
cat > tools/site/tests/test_extraer_blog.py <<'VT_EOF'
"""extraer_blog: las tres envolturas del blog se reducen al mismo contenido, y una corrección que no encuentra su texto detiene
la extracción."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extraer_blog as e  # noqa: E402

MODERNO = ('<main><nav class="vt-crumbs"></nav><div class="bg-gradient-to-br"><div><div><span>Palmas</span><span>7 min de lectura</span></div>'
           '<h1>Título</h1><p>Entrada</p></div></div><div class="layout-grid"><article class="prose">'
           '<div class="bg-bggreen border-l-4 border-primary"><h2>Respuesta directa</h2><p>Sí.</p></div>'
           '<h2 id="uno">Uno</h2><p class="x">Texto <a href="/precios" class="y">enlace</a></p><div class="tip-box"><strong>Tip:</strong> nota</div>'
           '<h2 id="preguntas-frecuentes">Preguntas frecuentes</h2><div><button class="faq-btn"><span>¿Q?</span></button>'
           '<div class="faq-answer"><p>R</p></div></div>'
           '<div class="not-prose"><div class="bg-primary"><a href="https://wa.me/1">Cotizar</a></div></div></article>'
           '<aside class="sticky-sidebar"><nav><a href="#uno">Uno</a></nav></aside></div>'
           '<section class="bg-bgwarm"><h2>También</h2><a class="group" href="/blog/x"><span>Cat</span><h4>Otro</h4><p>Txt</p></a></section></main>')


class ExtraerBlogTest(unittest.TestCase):
    def setUp(self):
        self.a = e.Articulo("p", MODERNO)
        self.a.recorrer()

    def test_respuesta_y_portada(self):
        self.assertEqual(self.a.respuesta["parrafos"], ["Sí."])
        self.assertEqual(self.a.kicker(), "Palmas")
        self.assertEqual(self.a.minutos(), 7)

    def test_cuerpo_sin_clases_y_con_enlace(self):
        html = e.serializar(self.a.bloques)
        self.assertIn('<h2 id="uno">Uno</h2>', html)
        self.assertIn('<p>Texto <a href="/precios">enlace</a></p>', html)
        self.assertIn("vt-art__nota--tip", html)
        self.assertNotIn('class="x"', html)

    def test_preguntas_relacionados_y_cta_fuera(self):
        self.assertEqual(self.a.faq, [["¿Q?", "R"]])
        self.assertEqual(self.a.relacionados[0]["href"], "/blog/x")
        self.assertTrue(any("Cotizar" in r for r in self.a.retirado))

    def test_correccion_sin_coincidencia_detiene(self):
        with self.assertRaises(ValueError):
            e.corregir({"slug": "p", "cuerpo": "hola"}, (("adios", "x", "motivo largo de la corrección"),))

    def test_todos_no_exige_coincidencia(self):
        self.assertEqual(e.corregir({"slug": "p", "t": "ab"}, (), (("zz", "y", "m"),))["t"], "ab")


if __name__ == "__main__":
    unittest.main()
VT_EOF
(cd tools/site && python3 -m unittest tests.test_extraer_blog 2>&1 | tail -1)
```

Expected: falla con `ModuleNotFoundError: No module named 'extraer_blog'`.

- [ ] **Step 2: Escribir `tools/site/extraer_blog.py` (GREEN)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site
cat > tools/site/extraer_blog.py <<'VT_EOF'
"""Extracción, de una sola vez, de los 52 artículos del blog hechos a mano a tools/site/contenido/blog/<slug>.html (Etapa 2h).

Cada artículo publicado tiene una de tres envolturas (40 con hero en degradado y barra lateral, 8 con <article data-page>,
4 con hero claro) pero el mismo contenido: portada, respuesta directa, cuerpo, preguntas, CTA y relacionados. Aquí el HTML
se lee con html.parser (biblioteca estándar), se reduce a bloques semánticos sin clases de Tailwind, se le aplican las
correcciones documentadas de contenido/blog_correcciones.py y se escribe un archivo por artículo: un comentario con los
metadatos en JSON y, debajo, el cuerpo en HTML. Lo que no pasa al artículo (índice, CTA, barra lateral) queda anotado en
"retirado", para que tests/test_blog_paridad.py compruebe que no se perdió texto.

Uso: python3 tools/site/extraer_blog.py escribir [<slug> …]   (lee public/blog; solo se corre antes de migrar)
     python3 tools/site/extraer_blog.py informe                (cuenta variantes y lo retirado, sin escribir)
"""
import html as html_mod
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
DESTINO = AQUI / "contenido" / "blog"
VACIAS = {"img", "br", "hr", "input", "meta", "link"}
EN_LINEA = {"a", "strong", "b", "em", "i", "br", "small", "sub", "sup", "code", "span", "u", "mark"}
SE_CONSERVA_TAL_CUAL = {"strong", "em", "br", "sub", "sup"}
RENOMBRA = {"b": "strong", "i": "em"}
NOTAS = ("tip-box", "warn-box", "highlight", "calc-box")
RESPUESTA = ("answer-box", "aeo-box")
BLOQUE_EN_NOTA = {"p", "div", "ul", "ol", "li", "h3", "h4", "h5"}
# Commit de main con los artículos hechos a mano: la extracción siempre lee esa versión, no el public/ ya migrado.
REF = "db6923e"
FECHA_CORRECCION = "2026-11-08"  # dateModified de los artículos cuyo texto cambió en esta etapa


class Nodo:
    def __init__(self, tag, attrs=(), padre=None):
        self.tag, self.attrs, self.padre, self.hijos = tag, dict(attrs), padre, []

    @property
    def clases(self):
        return (self.attrs.get("class") or "").split()

    def tiene(self, *clases):
        return any(c in self.clases for c in clases)

    def elementos(self):
        return [h for h in self.hijos if isinstance(h, Nodo)]

    def buscar(self, condicion):
        for h in self.elementos():
            if condicion(h):
                yield h
            yield from h.buscar(condicion)


class Lector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = self.actual = Nodo("raiz")

    def handle_starttag(self, tag, attrs):
        nodo = Nodo(tag, attrs, self.actual)
        self.actual.hijos.append(nodo)
        if tag not in VACIAS:
            self.actual = nodo

    def handle_startendtag(self, tag, attrs):
        self.actual.hijos.append(Nodo(tag, attrs, self.actual))

    def handle_endtag(self, tag):
        nodo = self.actual
        while nodo is not None and nodo.tag != tag:
            nodo = nodo.padre
        if nodo is not None and nodo.padre is not None:
            self.actual = nodo.padre

    def handle_data(self, data):
        self.actual.hijos.append(data)


def leer(fragmento):
    limpio = re.sub(r"<(script|svg|style)\b.*?</\1>", "", fragmento, flags=re.S | re.I)
    limpio = re.sub(r"<!--.*?-->", "", limpio, flags=re.S)
    lector = Lector()
    lector.feed(limpio)
    return lector.raiz


def texto(nodo):
    if isinstance(nodo, str):
        return nodo
    return " ".join(texto(h) for h in nodo.hijos)


def limpio(t):
    return re.sub(r"\s+", " ", t).strip()


def texto_limpio(nodo):
    return limpio(texto(nodo))


def en_linea(nodo):
    """HTML en línea del contenido del nodo: solo enlaces, negritas y cursivas; sin clases."""
    salida = []
    for h in nodo.hijos:
        if isinstance(h, str):
            salida.append(html_mod.escape(re.sub(r"\s+", " ", h), quote=False))
            continue
        tag = RENOMBRA.get(h.tag, h.tag)
        if tag == "a":
            href = (h.attrs.get("href") or "").replace("&", "&amp;") if "&amp;" not in (h.attrs.get("href") or "") else h.attrs["href"]
            salida.append(f'<a href="{href}">{en_linea(h)}</a>')
        elif tag == "br":
            salida.append("<br>")
        elif tag in SE_CONSERVA_TAL_CUAL:
            salida.append(f"<{tag}>{en_linea(h)}</{tag}>")
        elif tag in BLOQUE_EN_NOTA:
            salida.append(f" {en_linea(h)} ")
        else:
            salida.append(en_linea(h))
    return "".join(salida)


def inline(nodo):
    return re.sub(r"\s+", " ", en_linea(nodo)).strip()


def foto(nodo, public=PUBLIC):
    from PIL import Image
    src = nodo.attrs.get("src", "")
    src = "/" + src.lstrip("./") if not src.startswith("/") else src
    with Image.open(Path(public) / src.lstrip("/")) as im:
        ancho, alto = im.size
    return {"tipo": "foto", "src": src, "alt": nodo.attrs.get("alt", ""), "ancho": ancho, "alto": alto}


def slug_de(t):
    t = re.sub(r"[^a-z0-9áéíóúñü ]+", "", t.lower())
    t = t.translate(str.maketrans("áéíóúñü", "aeiounu")).strip()
    return re.sub(r"\s+", "-", " ".join(t.split()[:7]))


class Articulo:
    def __init__(self, slug, html, public=PUBLIC):
        self.slug, self.html, self.public = slug, html, public
        m = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S)
        self.raiz = leer(m.group(1))
        self.bloques, self.faq, self.relacionados, self.retirado, self.respuesta = [], [], [], [], None
        self.ids, self.en_faq = set(), False
        self.faq_titulo, self.rel_titulo = "Preguntas frecuentes", ""

    # ---------- portada ----------
    def h1(self):
        return next(self.raiz.buscar(lambda n: n.tag == "h1"))

    def portada(self):
        """El contenedor de la portada: el padre de <h1>, subiendo lo justo para incluir etiquetas y autor."""
        h1 = self.h1()
        return h1.padre

    def kicker(self):
        cont = self.portada()
        spans = list(cont.buscar(lambda n: n.tag == "span"))
        return texto_limpio(spans[0]) if spans else ""

    def dek(self):
        cont = self.portada()
        for h in cont.elementos():
            if h.tag == "p":
                return inline(h)
        return ""

    def minutos(self):
        m = re.search(r"(\d+) min de lectura", texto_limpio(self.portada()))
        return int(m.group(1)) if m else None

    # ---------- contenido ----------
    def raiz_contenido(self):
        return next(self.raiz.buscar(lambda n: n.tag == "article"))

    def clasificar(self, n):
        """Reparte un elemento en bloques, respuesta, preguntas, relacionados o retirado."""
        if isinstance(n, str):
            if n.strip():
                self.retirado.append(limpio(n))
            return
        t = n.tag
        if t == "section" and self.es_relacionados(n):
            self.tomar_relacionados(n)
        elif t in ("h2", "h3", "h4", "h5"):
            self.bloque_titulo(n)
        elif t == "p" and self.en_faq and self.faq and not self.faq[-1][1]:
            self.faq[-1][1] = inline(n)
        elif t == "p":
            self.bloques.append({"tipo": "p", "html": inline(n)})
        elif t in ("ul", "ol"):
            self.bloques.append({"tipo": t, "items": [inline(li) for li in n.elementos() if li.tag == "li"]})
        elif t == "table":
            self.bloques.append({"tipo": "tabla", "html": self.tabla(n)})
        elif t == "blockquote":
            self.bloques.append({"tipo": "cita", "html": inline(n)})
        elif t == "img":
            self.bloques.append(foto(n, self.public))
        elif t == "hr":
            pass
        elif t in ("nav", "aside") or n.tiene("toc"):
            self.retirar(n)
        elif self.es_cta(n) and (n.tiene("not-prose", "bg-primary", "bg-dark") or t == "section"):
            self.retirar(n)
        elif n.tiene(*RESPUESTA) or self.es_caja_respuesta(n):
            self.tomar_respuesta(n)
        elif n.tiene(*NOTAS) or (n.tiene("bg-bggreen") and n.tag == "div"):
            self.bloques.append({"tipo": "nota", "html": self.nota(n), "clase": "aviso" if n.tiene("warn-box") else "tip"})
        elif n.tiene("faq-btn"):
            pass
        elif n.tiene("faq-block"):
            self.pregunta_bloque(n)
        elif any(True for _ in n.buscar(lambda x: x.tiene("faq-btn"))) and self.es_item_faq(n):
            self.pregunta_boton(n)
        elif self.es_cta(n):
            self.retirar(n)
        else:
            for h in n.hijos:
                self.clasificar(h)

    @staticmethod
    def es_cta(n):
        """Bloque de llamada a la acción: botón de WhatsApp o enlace con forma de botón, y poco texto."""
        boton = any(True for _ in n.buscar(lambda x: x.tag == "a" and ("wa.me" in (x.attrs.get("href") or "")
                                                                         or x.tiene("rounded-full", "rounded-xl"))))
        con_ancla = any(True for _ in n.buscar(lambda x: x.tag == "article" or x.attrs.get("id")))
        return boton and not con_ancla and len(texto_limpio(n)) < 320

    @staticmethod
    def es_caja_respuesta(n):
        return n.tag == "div" and n.tiene("bg-bggreen") and n.tiene("border-primary") and n.tiene("border-l-4")

    @staticmethod
    def es_item_faq(n):
        return len(n.elementos()) >= 2 and n.elementos()[0].tag == "button"

    def tomar_respuesta(self, n):
        if self.respuesta is not None:
            self.bloques.append({"tipo": "nota", "html": self.nota(n), "clase": "tip"})
            return
        cuerpo, titulo, heading = [], "Respuesta directa", False
        for h in n.elementos():
            if h.tag in ("h2", "h3") or h.tiene("answer-box-label"):
                titulo, heading = texto_limpio(h), h.tag in ("h2", "h3")
            elif h.tag == "p":
                cuerpo.append(inline(h))
            else:
                cuerpo.append(inline(h))
        if not cuerpo:
            cuerpo = [inline(n)]
        self.respuesta = {"titulo": titulo, "es_titulo": heading, "parrafos": cuerpo}

    @staticmethod
    def nota(n):
        return inline(n)

    def bloque_titulo(self, n):
        t = texto_limpio(n)
        ident = n.attrs.get("id")
        if n.tag == "h2" and re.fullmatch(r"preguntas frecuentes", t, re.I):
            self.faq_titulo, self.en_faq = t, True
            return
        if self.en_faq and n.tag in ("h3", "h4"):
            self.faq.append([inline(n), ""])
            return
        if n.tag == "h2":
            self.en_faq = False
        if n.tag == "h2" and not ident:
            ident = slug_de(t)
            while ident in self.ids:
                ident += "-2"
        if ident:
            self.ids.add(ident)
        self.bloques.append({"tipo": n.tag, "html": inline(n), "id": ident})

    def tabla(self, n):
        filas = []
        for tr in n.buscar(lambda x: x.tag == "tr"):
            celdas = []
            for c in tr.elementos():
                extra = "".join(f' {a}="{c.attrs[a]}"' for a in ("colspan", "rowspan") if c.attrs.get(a))
                if c.tag == "th":
                    celdas.append(f'<th scope="col"{extra}>{inline(c)}</th>')
                elif c.tag == "td":
                    celdas.append(f"<td{extra}>{inline(c)}</td>")
            filas.append((tr.padre.tag, f"<tr>{''.join(celdas)}</tr>"))
        cabeza = "".join(f for p, f in filas if p == "thead")
        resto = "".join(f for p, f in filas if p != "thead")
        if cabeza:
            return f"<table><thead>{cabeza}</thead><tbody>{resto}</tbody></table>"
        return f"<table><tbody>{resto}</tbody></table>"

    def pregunta_bloque(self, n):
        q = next(h for h in n.elementos() if h.tag in ("h3", "h4", "button"))
        partes = [inline(h) for h in n.elementos() if h is not q]
        self.faq.append([inline(q), "</p><p>".join(partes)])

    def pregunta_boton(self, n):
        boton, resp = n.elementos()[0], n.elementos()[1]
        spans = [h for h in boton.elementos() if h.tag == "span"]
        q = inline(spans[0]) if spans else inline(boton)
        ps = [e for e in resp.buscar(lambda x: x.tag == "p")]
        if ps:
            a = "</p><p>".join(inline(p) for p in ps)
        else:
            a = inline(resp)
        self.faq.append([q, a])

    def retirar(self, n):
        t = texto_limpio(n)
        if t:
            self.retirado.append(t)

    def tomar_relacionados(self, n):
        titulo_h2 = next(n.buscar(lambda x: x.tag == "h2"), None)
        self.rel_titulo = texto_limpio(titulo_h2) if titulo_h2 is not None else ""
        for a in n.buscar(lambda x: x.tag == "a"):
            href = a.attrs.get("href") or ""
            self.retirar(a)  # la tarjeta vuelve con el texto que la plantilla usa; "Leer más" y "Ver todos" no
            if not (href.startswith("/") and a.tiene("group", "block")):
                continue
            spans = [e for e in a.elementos() if e.tag == "span"]
            titulo = next((e for e in a.elementos() if e.tag in ("h3", "h4")), None)
            ps = [e for e in a.elementos() if e.tag == "p"]
            self.relacionados.append({"href": href, "categoria": texto_limpio(spans[0]) if spans else "",
                                      "titulo": texto_limpio(titulo) if titulo is not None else texto_limpio(a),
                                      "texto": texto_limpio(ps[0]) if ps else ""})

    def es_relacionados(self, n):
        return n.tag == "section" and any(True for _ in n.buscar(
            lambda x: x.tag == "a" and (x.attrs.get("href") or "").startswith("/") and x.tiene("group", "block")))

    def recorrer(self):
        self.faq_titulo, self.rel_titulo = "Preguntas frecuentes", ""
        portada = self.portada()

        def bajar(n):
            if isinstance(n, str):
                return
            if n is portada:
                self.retirar(n)
                return
            if n.tag == "section" and self.es_relacionados(n):
                self.tomar_relacionados(n)
                return
            if n.tag == "nav" and n.tiene("vt-crumbs"):
                self.retirar(n)
                return
            if self.contiene(n, portada):
                for h in n.hijos:
                    bajar(h)
                return
            if n.tag == "aside":
                self.retirar(n)
                return
            self.clasificar(n)

        for h in self.raiz.hijos:
            bajar(h)

    @staticmethod
    def contiene(n, objetivo):
        return any(x is objetivo for x in n.buscar(lambda _: True))


def serializar(bloques):
    salida = []
    for b in bloques:
        t = b["tipo"]
        if t in ("h2", "h3", "h4", "h5"):
            ident = f' id="{b["id"]}"' if b.get("id") else ""
            salida.append(f"<{t}{ident}>{b['html']}</{t}>")
        elif t == "p":
            salida.append(f"<p>{b['html']}</p>")
        elif t in ("ul", "ol"):
            salida.append(f"<{t}>\n" + "\n".join(f"<li>{i}</li>" for i in b["items"]) + f"\n</{t}>")
        elif t == "tabla":
            salida.append(f'<div class="vt-art__tabla" tabindex="0" role="region" aria-label="Tabla">{b["html"]}</div>')
        elif t == "cita":
            salida.append(f"<blockquote>{b['html']}</blockquote>")
        elif t == "nota":
            salida.append(f'<aside class="vt-art__nota vt-art__nota--{b["clase"]}"><p>{b["html"]}</p></aside>')
        elif t == "foto":
            salida.append(f'<img src="{b["src"]}" width="{b["ancho"]}" height="{b["alto"]}" alt="{html_mod.escape(b["alt"])}">')
    return "\n".join(salida) + "\n"


def meta_pagina(html):
    meta = {}
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    meta["title"] = html_mod.unescape(t.group(1).strip())
    for nombre, clave in (("description", "description"), ("robots", "robots")):
        m = re.search(rf'<meta name="{nombre}" content="([^"]*)"', html)
        meta[clave] = html_mod.unescape(m.group(1)) if m else ""
    meta["canonical"] = re.search(r'<link rel="canonical" href="([^"]*)"', html).group(1)
    meta["og"] = [[p, html_mod.unescape(v)] for p, v in re.findall(r'<meta property="((?:og|article):[^"]+)" content="([^"]*)"', html)]
    meta["twitter"] = [[p, html_mod.unescape(v)] for p, v in re.findall(r'<meta name="(twitter:[^"]+)" content="([^"]*)"', html)]
    return meta


def jsonld_pagina(html):
    bloques = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return json.loads(bloques[0])


def extraer(slug, public=PUBLIC):
    html = publicado(f"blog/{slug}/index.html")
    a = Articulo(slug, html, public)
    a.recorrer()
    grafo = jsonld_pagina(html)
    return {
        "slug": slug, "meta": meta_pagina(html), "jsonld": grafo, "kicker": a.kicker(), "h1": inline(a.h1()),
        "dek": a.dek(), "minutos": a.minutos(), "respuesta": a.respuesta, "faq_titulo": a.faq_titulo, "faq": a.faq,
        "relacionados_titulo": a.rel_titulo, "relacionados": a.relacionados, "retirado": a.retirado,
        "bloques": a.bloques, "cuerpo": serializar(a.bloques),
    }


def publicado(rel):
    """HTML de public/<rel> en el commit REF."""
    raiz = AQUI.parents[1]
    return subprocess.run(["git", "show", f"{REF}:public/{rel}"], cwd=raiz, capture_output=True, text=True, check=True).stdout


def slugs(public=PUBLIC):
    return sorted(p.parent.name for p in (Path(public) / "blog").glob("*/index.html"))


# ---------- índice del blog ----------
def extraer_indice(public=PUBLIC):
    html = publicado("blog/index.html")
    raiz = leer(re.search(r"<main\b[^>]*>(.*)</main>", html, re.S).group(1))
    hero = next(raiz.buscar(lambda n: n.tiene("vt-hero__bg-img")))
    secciones, actual = [], None

    def recorrer(n):
        nonlocal actual
        for h in n.elementos():
            if h.tag == "h2" and "¿Buscas" not in texto_limpio(h):
                actual = {"titulo": texto_limpio(h), "tarjetas": []}
                secciones.append(actual)
            elif h.tag == "a" and (h.attrs.get("href") or "").startswith("/blog/") and actual is not None:
                actual["tarjetas"].append(tarjeta(h, public))
            elif h.tag == "h2":
                actual = None
            else:
                recorrer(h)

    recorrer(raiz)
    return {"meta": meta_pagina(html), "jsonld": jsonld_pagina(html), "foto": foto(hero, public), "secciones": secciones}


def tarjeta(a, public):
    img = next(a.buscar(lambda n: n.tag == "img"), None)
    titulo = next(a.buscar(lambda n: n.tag in ("h3", "h4")))
    cat = next(a.buscar(lambda n: n.tiene("badge")), None)
    p = next(a.buscar(lambda n: n.tag == "p"), None)
    m = re.search(r"(\d+) min", texto_limpio(a))
    return {"href": a.attrs["href"], "foto": foto(img, public) if img is not None else None,
            "categoria": texto_limpio(cat) if cat is not None else "", "titulo": texto_limpio(titulo),
            "texto": texto_limpio(p) if p is not None else "", "minutos": int(m.group(1)) if m else None}


# ---------- paridad ----------
M_CTA = "Era parte del índice, la barra lateral o un CTA del HTML anterior; la plantilla pone los suyos (spec §3.3)."
M_FAQ_H = "Sigue en la página: las preguntas ahora van en <details> de la sección de preguntas."
M_SOLO_LD = "Pregunta que solo estaba en el JSON-LD, no en la página: FAQPage ahora repite lo visible (spec §7.3)."
M_CIERRE = "El CTA final lo pone la plantilla, con landing y mensaje del artículo."


def _textos(doc):
    faq = [limpio(re.sub(r"<[^>]+>", " ", q)) for q, _a in doc["faq"]]
    titulos = [limpio(re.sub(r"<[^>]+>", " ", doc["h1"]))]
    titulos += [limpio(re.sub(r"<[^>]+>", " ", b)) for b in re.findall(r"<h[23]\b[^>]*>(.*?)</h[23]>", doc["cuerpo"], re.S)]
    titulos += [r["titulo"] for r in doc["relacionados"]]
    if doc["relacionados_titulo"]:
        titulos.append(doc["relacionados_titulo"])
    if doc["respuesta"]:
        titulos.append(doc["respuesta"]["titulo"])
    titulos.append(doc["faq_titulo"])
    return titulos, faq


def _texto_doc(doc):
    return " ".join([doc["cuerpo"], doc["dek"], doc["h1"], " ".join(doc["respuesta"]["parrafos"]) if doc["respuesta"] else "",
                     " ".join(q + " " + a for q, a in doc["faq"]), " ".join(r["titulo"] + " " + r["texto"] for r in doc["relacionados"])])


def paridad_de(html, doc, correcciones):
    """PARIDAD del artículo: qué dejó de estar (y por qué) respecto a lo publicado. Lo que no se pueda explicar detiene la
    extracción."""
    import paridad as par
    viejo = par.extraer(html)
    titulos, faq = _textos(doc)
    retirados, reemplazos = {}, {}
    plano = [(par.texto(v), par.texto(n), m) for v, n, m in correcciones]
    retirado_txt = " ".join(doc["retirado"])
    for h in viejo["encabezados"]:
        if par.cubierto(h, titulos):
            continue
        corr = next(((v, n, m) for v, n, m in plano if v and v in h), None)
        if corr and not par.cubierto(h.replace(corr[0], corr[1]), faq):
            reemplazos[h] = h.replace(corr[0], corr[1])
        elif corr or par.cubierto(h, faq):
            retirados[h] = M_FAQ_H
        elif h in retirado_txt or h in (doc["h1"],):
            retirados[h] = M_CTA
        else:
            retirados[h] = M_CIERRE
    for q in viejo["faq"]:
        if not par.cubierto(q, faq):
            corr = next(((v, n, m) for v, n, m in plano if v and v in q), None)
            if corr:
                reemplazos[q] = q.replace(corr[0], corr[1])
            else:
                retirados[q] = M_SOLO_LD
    nuevo_txt = par.texto(_texto_doc(doc))
    nuevos = {p.replace(" ", "") for p in re.findall(r"\$\s?\d[\d,]*", nuevo_txt)}
    for precio in viejo["precios"]:
        if precio in nuevos:
            continue
        corr = next((m for v, _n, m in plano if precio in v.replace(" ", "")), None)
        retirados[precio] = corr or M_CTA
    meta = {}
    for clave, valor in viejo["meta"].items():
        actual = doc["meta"].get(clave) if not clave.startswith("og:") else dict(doc["meta"]["og"]).get(clave)
        if actual is not None and actual != valor:
            motivo = next((m for v, _n, m in plano if v and v in valor), "Corrección de contenido documentada.")
            meta[clave] = [actual, motivo]
    return {"reemplazos": reemplazos, "retirados": retirados, "meta": meta}


# ---------- escritura ----------
def fragmento(doc):
    meta = {k: v for k, v in doc.items() if k not in ("cuerpo", "bloques")}
    return "<!--vt:meta\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\n-->\n" + doc["cuerpo"]


def _reemplazar(valor, viejo, nuevo, cuenta):
    if isinstance(valor, str):
        cuenta[0] += valor.count(viejo)
        return valor.replace(viejo, nuevo)
    if isinstance(valor, list):
        return [_reemplazar(v, viejo, nuevo, cuenta) for v in valor]
    if isinstance(valor, dict):
        return {k: _reemplazar(v, viejo, nuevo, cuenta) for k, v in valor.items()}
    return valor


def fecha_actualizada(doc, correcciones):
    """dateModified de hoy solo en los artículos cuyo contenido cambió de verdad (no por cambiar la plantilla)."""
    if correcciones:
        articulo = next(n for n in doc["jsonld"]["@graph"] if n.get("@type") == "Article")
        articulo["dateModified"] = FECHA_CORRECCION
    return doc


def corregir(doc, correcciones, todos=()):
    """Copia del documento con cada corrección (viejo, nuevo, motivo) aplicada en todos sus textos. Una corrección que no
    encuentra su texto detiene la extracción: así nadie cree haber corregido algo que no se tocó."""
    for viejo, nuevo, motivo in correcciones:
        cuenta = [0]
        doc = _reemplazar(doc, viejo, nuevo, cuenta)
        if not cuenta[0]:
            raise ValueError(f"{doc['slug']}: la corrección no encontró su texto: {viejo!r} ({motivo})")
    for viejo, nuevo, _motivo in todos:
        doc = _reemplazar(doc, viejo, nuevo, [0])
    return doc


def escribir(lista=None, public=PUBLIC, destino=DESTINO):
    from contenido import blog_correcciones as bc
    destino.mkdir(parents=True, exist_ok=True)
    for slug in lista or slugs(public):
        doc = fecha_actualizada(corregir(extraer(slug, public), bc.de(slug), bc.TODOS), bc.de(slug))
        doc["paridad"] = paridad_de(publicado(f"blog/{slug}/index.html"), doc, bc.de(slug) + bc.TODOS)
        (destino / f"{slug}.html").write_text(fragmento(doc), encoding="utf-8")
    indice = corregir({"slug": "/blog", **extraer_indice(public)}, bc.de("/blog"), bc.TODOS)
    (destino / "_indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:2] != ["escribir"]:
        raise SystemExit("Uso: python3 tools/site/extraer_blog.py escribir [<slug> …]")
    escribir(sys.argv[2:] or None)
    print("listo")
VT_EOF
(cd tools/site && python3 -m unittest tests.test_extraer_blog 2>&1 | tail -1)
```

Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/extraer_blog.py tools/site/tests/test_extraer_blog.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(blog): extractor único de los artículos a contenido semántico" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Correcciones de contenido

**Files:** Create: `tools/site/contenido/blog_correcciones.py`

- [ ] **Step 1: Escribir las correcciones**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/contenido
cat > tools/site/contenido/blog_correcciones.py <<'VT_EOF'
"""Correcciones de contenido de los artículos del blog (Etapa 2h): lo único que cambia el texto publicado.

La migración conserva cada palabra; aquí está, por artículo, cada dato que contradice las fuentes oficiales o las reglas
del dueño, con el texto exacto de antes, el de después y el motivo. tools/site/extraer_blog.py las aplica y se detiene si una
no encuentra su texto; tests/test_blog_paridad.py exige que la diferencia entre lo publicado y lo nuevo sea exactamente esta
lista. Los precios de "nuevo" salen de datos.PRECIOS. TODOS se aplica a todos los artículos (los títulos de otros artículos se
repiten en enlaces y relacionados) y no exige coincidencia.
"""
import datos
from componentes import dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
CAMION_8 = dinero(P["tierra_negra_camion_8m3"])
R0, R1 = P["riego_m2"]


def riego(m2_a, m2_b=None):
    """Rango instalado de riego para un área, con el precio oficial por m²."""
    return f"{dinero(R0 * m2_a)}–{dinero(R1 * (m2_b or m2_a))}"


M_PLANTA = "Precio sin confirmar por el dueño: solo areca, coco plumoso, palma real y flamboyán tienen precio; lo demás es según cotización."
M_VENDIDA = "\"Más vendida\" es un superlativo sin dato que lo respalde (regla del dueño); la URL no cambia."
M_ESTAD = "Porcentaje sin fuente (no se publican estadísticas inventadas)."
M_GRATIS = "Regla del dueño: sin \"gratis\" ni \"sin costo\", salvo la garantía de pasto aprobada."
M_RIEGO = "Riego instalado: el único precio oficial es $180–$320/m² (datos.py); los rangos se recalculan con él."
M_CASO = "Caso con cliente, cifra e inversión sin verificar: no se publica como real."
M_AHORRO = "El ahorro oficial de agua es \"hasta 40%\" (datos.RIEGO_AHORRO)."
M_PAGO = "Pago: anticipo y avances (datos.ANTICIPO_PROYECTOS), sin crédito propio; mensualidades solo con tarjeta de crédito."
M_TIERRA = "Camión de tierra de 8 m³: $5,200 (datos.py), no $12,000."
M_DISENO = "Diseño: Esencial $3,000, Completo $6,500 y Premium desde $18,000 (datos.py); no son rangos."
M_GARANTIA = "Garantía del sintético: 3 a 8 años según modelo (tools/pasto/data.py: Aruba 10 de 3 a 5, Toscana 5, los demás 8)."
M_DEK = "La entrada era la del artículo de árboles de banqueta (copiada por error)."
M_ENTREGA = "La entrega se cobra por viaje, según la colonia (datos.ENTREGA_COBRO)."
M_VISITA = "Toda mención de la visita lleva su costo (datos.VISITA_COSTO)."

GARANTIA_SINTETICO = "de 3 a 8 años según modelo"
PAGO_RESPUESTA = (f"Viveros Terra no ofrece crédito propio. {datos.ANTICIPO_PROYECTOS} También puedes pagar a mensualidades con "
                  "tarjeta de crédito: <a href=\"/politicas#mensualidades\">ver condiciones</a>.")

TODOS = (
    ("Las 8 Palmas Más Vendidas en Tampico (con Precios)", "8 Palmas para Jardines en Tampico (con Precios)", M_VENDIDA),
    ("las 8 palmas más vendidas en Tampico con precios actualizados", "8 palmas para jardines en Tampico con precios actualizados", M_VENDIDA),
    ("lista de las 8 palmas más vendidas en Tampico", "lista de 8 palmas para jardines en Tampico", M_VENDIDA),
    ("las palmas más vendidas en Tampico con precios", "las 8 palmas para jardines en Tampico con precios", M_VENDIDA),
    ("palmas más vendidas en Tampico con precios</a>", "palmas para jardines en Tampico con precios</a>", M_VENDIDA),
    ("palmas más vendidas en Tampico</a>", "palmas para jardines en Tampico</a>", M_VENDIDA),
    ("La palma más vendida de la región: crecimiento rápido y precio desde $500.", "Crecimiento rápido y tolerancia al calor y la sequía.", M_VENDIDA),
    ("La palma más vendida de la región, con su característica faldilla de hojas secas.", "Crecimiento rápido, con su característica faldilla de hojas secas.", M_VENDIDA),
)

_DEK_BANQUETA = "¿Cansado de banquetas destruidas por raíces? Guía de los 7 mejores árboles para banqueta en Tampico: dan sombra real sin dañar el pavimento ni las tuberías. Con tabla comparativa."

CORRECCIONES = {
    "/blog": (
        ("Las 8 palmas más vendidas en Tampico (con precios)", "8 palmas para jardines en Tampico (con precios)", M_VENDIDA),
        ("Palmas más vendidas Tampico precios", "Palmas para jardines en Tampico", M_VENDIDA),
        ("La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y precio desde $500.", "Crecimiento rápido y tolerancia total al calor.", M_VENDIDA),
        ("tolera luz baja, crece lento y tiene precio desde $500.", "tolera luz baja y crece lento.", M_PLANTA),
        ("tolera sol pleno, sequía y lluvia intensa. Precio desde $500.", f"tolera sol pleno, sequía y lluvia intensa. Precio desde {dinero(P['palma_desde'])}.", "Coco plumoso: desde $250 (datos.py)."),
        ("de privacidad, con precio desde $300.", f"de privacidad, con precio desde {dinero(P['palma_desde'])}.", "Areca: desde $250 (datos.py)."),
        ("Cómo Ahorrar Hasta 50% de Agua", "Cómo Ahorrar Hasta 40% de Agua", M_AHORRO),
    ),
    "hongos-plantas-exceso-humedad-tampico": (
        ("Las tres medidas más efectivas y gratuitas son:", "Las tres medidas más efectivas son:", M_GRATIS),
    ),
    "acolchado-mulch-jardin-tampico": (
        ("Casi gratis: aprovechas", "Casi sin gasto: aprovechas", M_GRATIS),
    ),
    "arboles-para-sembrar-en-banqueta": (
        ("Si las aplicas, evitas el 90% de los problemas:", "Si las aplicas, evitas la mayoría de los problemas:", M_ESTAD),
        ("En Viveros Terra hemos instalado más de 200 árboles de banqueta en Tampico, Madero y Altamira. El 95% de los problemas que vemos", "En las banquetas de Tampico, Madero y Altamira, la mayoría de los problemas que vemos", "Cifra de árboles y porcentaje sin verificar."),
        (" Tip de experto:", " Tip:", "Sin \"expertos\" (regla de voz)."),
    ),
    "cesped-amarillo-tampico-causas-soluciones": (
        ("otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo.",
         f"otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo. {datos.VISITA_COSTO}", M_VISITA),
    ),
    "como-ahorrar-agua-jardin-tampico": (
        ("reduciendo hasta un 50% el consumo hídrico", f"reduciendo {datos.RIEGO_AHORRO} el consumo hídrico", M_AHORRO),
        ("para reducir hasta 50% el consumo", f"para reducir {datos.RIEGO_AHORRO} el consumo", M_AHORRO),
        ("Aprende a reducir hasta 50% el consumo", f"Aprende a reducir {datos.RIEGO_AHORRO} el consumo", M_AHORRO),
        ("entre 30% y 50% respecto al riego manual", f"{datos.RIEGO_AHORRO} respecto al riego manual", M_AHORRO),
        ("Clientes de Viveros Terra en Tampico reportan ahorros de entre $150 y $600 pesos mensuales en el recibo de agua después de instalar un sistema automático, dependiendo del tamaño del jardín y la frecuencia de riego anterior.",
         f"Un sistema automático bien programado ahorra {datos.RIEGO_AHORRO} de agua frente a la manguera; lo que baja tu recibo depende del tamaño del jardín y de cuánto riegas hoy.", "Testimonio y cifra sin verificar."),
    ),
    "como-medir-plantas-altura-cepellon": (
        ("puede orientarte sin costo antes de cotizar", "puede orientarte antes de cotizar", M_GRATIS),
    ),
    "cuando-plantar-pasto-tampico-calendario": (
        (_DEK_BANQUETA, "Calendario completo para sembrar pasto en Tampico mes a mes: cuál es el mejor mes, qué evitar y por qué septiembre es el mes ideal en clima tropical.", M_DEK),
        ("<strong>septiembre arraiga el 95% del pasto; julio puede arraigar solo el 60%</strong> por el calor extremo", "<strong>en septiembre el pasto arraiga mucho mejor que en julio</strong>, por el calor extremo", M_ESTAD),
        ("aporta humedad gratis al suelo", "aporta humedad natural al suelo", M_GRATIS),
        ("la tasa de mortandad sube al 30–40%", "la mortandad sube mucho", M_ESTAD),
        ("la tasa de éxito baja al 60% sin riego intensivo", "la tasa de éxito baja sin riego intensivo", M_ESTAD),
        ("reduce 70% el riego manual", "reduce mucho el riego manual", M_ESTAD),
        ("puede duplicar la tasa de arraigo del pasto", "mejora el arraigo del pasto", M_ESTAD),
    ),
    "cuando-regar-pasto-san-agustin-tampico": (
        ("En Viveros Terra instalamos sistemas desde $8,000 pesos; uno bien programado", f"En Viveros Terra instalamos sistemas de {dinero(R0)} a {dinero(R1)} por m²; uno bien programado", M_RIEGO),
        ("El problema real en el 70% de los casos es el riego", "El problema real, en la mayoría de los casos, es el riego", M_ESTAD),
    ),
    "cuanto-cuesta-jardin-tampico-precios": (
        ("pasto $85/m², diseño desde $3K, riego, plantas. Cotiza gratis hoy.", "pasto $85/m², diseño desde $3K, riego, plantas. Cotiza por WhatsApp.", M_GRATIS),
        ("El costo de hacer un jardín en Tampico va desde $5,000 MXN para uno mini residencial hasta $200,000+ para premium.", "Hacer un jardín en Tampico se cotiza según el proyecto; estas son referencias con los precios oficiales.", "Rango total sin confirmar por el dueño."),
        ("basados en proyectos ejecutados en Tampico, Madero y Altamira durante 2025 y lo que va de 2026. No son precios promedio nacionales: son datos de nuestra zona.", "con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira. El presupuesto final siempre se cotiza.", "Dato sin verificar por el dueño."),
        ("<li>Palmas grandes ($1,000–$2,000 c/u), árboles ornamentales", f"<li>Palmas grandes ({SEGUN}), árboles ornamentales", M_PLANTA),
        ("5 a 10 plantas ornamentales básicas: $200–$500 c/u", f"5 a 10 plantas ornamentales básicas: {SEGUN}", M_PLANTA),
        ("1–3 palmas medianas ($500–$1,500 c/u)", f"1–3 palmas medianas ({SEGUN})", M_PLANTA),
        ("Riego automatizado completo con programador digital ($15,000–$60,000 según extensión)", f"Riego automatizado completo con programador digital ({dinero(R0)}–{dinero(R1)}/m²)", M_RIEGO),
        ("Ejemplo real: jardín de 30 m²", "Ejemplo de presupuesto: jardín de 30 m²", M_CASO),
        ("<li>6 plantas ornamentales × $300 = $1,800</li>\n<li>Mano de obra preparación + instalación = $2,000</li>\n<li><strong>Total estimado: $7,850 MXN</strong></li>", f"<li>6 plantas ornamentales: {SEGUN}</li>\n<li>Mano de obra de preparación e instalación: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_PLANTA),
        ("Ejemplo real: jardín de 120 m² con riego básico", "Ejemplo de presupuesto: jardín de 120 m² con riego básico", M_CASO),
        ("<li>15 plantas + 2 palmas = $7,500</li>", f"<li>15 plantas + 2 palmas: {SEGUN}</li>", M_PLANTA),
        ("<li>Riego básico por aspersores = $6,000</li>\n<li>Mano de obra total = $4,000</li>\n<li><strong>Total estimado: $36,700 MXN</strong></li>", f"<li>Riego básico por aspersores: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_RIEGO),
        ("<li>Tierra negra 8 m³ = $12,000</li>\n<li>5 palmas grandes + 20 plantas ornamentales = $18,000</li>", f"<li>Tierra negra, camión de 8 m³ = {CAMION_8}</li>\n<li>5 palmas grandes + 20 plantas ornamentales: {SEGUN}</li>", M_TIERRA),
        ("<li>Riego automatizado completo 250 m² = $40,000</li>\n<li>Tezontle, bordillos y acabados = $12,000</li>\n<li>Mano de obra total = $10,000</li>\n<li><strong>Total: $119,750 MXN</strong></li>", f"<li>Riego automatizado completo 250 m²: {riego(250)}</li>\n<li>Tezontle, bordillos y acabados: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_RIEGO),
        ("Ejemplo: jardín premium 250 m² → $120,000 MXN", "Ejemplo: jardín premium de 250 m²", M_CASO),
        ("<td>Pasto San Agustín (instalado)</td><td>$85/m²</td><td>Incluye mano de obra básica</td>", "<td>Pasto San Agustín</td><td>$85/m² solo pasto · desde $120/m² instalado</td><td>El instalado incluye preparación básica y colocación</td>", "Precio oficial: $85 solo pasto y desde $120 instalado."),
        ("Camión 8 m³ desde $12,000", f"Camión de 8 m³: {CAMION_8}", M_TIERRA),
        ("<td>Diseño Plan Terra Esencial</td><td>$3,000–$6,000</td>", "<td>Diseño Plan Terra Esencial</td><td>$3,000</td>", M_DISENO),
        ("<td>Diseño Plan Terra Completo</td><td>$6,500–$18,000</td>", "<td>Diseño Plan Terra Completo</td><td>$6,500</td>", M_DISENO),
        ("<td>Riego automatizado</td><td>$15,000–$60,000</td><td>Según m² y número de zonas</td>", f"<td>Riego automatizado</td><td>{dinero(R0)}–{dinero(R1)}/m²</td><td>Según m² y número de zonas</td>", M_RIEGO),
        ("<td>Palmas pequeñas (hasta 1.5 m)</td><td>$250–$600 c/u</td><td>Areca, Kerpis, Cycas pequeñas</td>", "<td>Palmas pequeñas (hasta 1.5 m)</td><td>Desde $250 c/u</td><td>Areca y coco plumoso; palma real desde $500; las demás, según cotización</td>", M_PLANTA),
        ("<td>Palmas medianas (1.5–3 m)</td><td>$600–$1,200 c/u</td>", f"<td>Palmas medianas (1.5–3 m)</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Palmas grandes (3 m+)</td><td>$1,200–$2,500 c/u</td>", f"<td>Palmas grandes (3 m+)</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Mano de obra general</td><td>~$200/m²</td>", f"<td>Mano de obra general</td><td>{SEGUN}</td>", "Precio sin confirmar."),
        ("<td>Tezontle decorativo</td><td>$35/kg o $280/costal</td>", f"<td>Tezontle decorativo</td><td>Costal desde {dinero(P['tezontle_costal'])}</td>", "Tezontle: costal desde $200 (datos.py)."),
        ("3 ejemplos reales de presupuestos", "3 ejemplos de presupuesto", M_CASO),
        ("Caso A: Jardín residencial de 50 m² → ~$13,500 MXN", "Ejemplo A: jardín residencial de 50 m²", M_CASO),
        ("Cliente en Ciudad Madero con casa dúplex. Jardín frontal", "Jardín frontal", M_CASO),
        ("<li>8 plantas × $350 = $2,800</li>\n<li>Mano de obra = $3,000</li>\n<li><strong>Total: $13,050 MXN</strong></li>", f"<li>8 plantas: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_PLANTA),
        ("Caso B: Jardín de 120 m² con riego básico → ~$35,000 MXN", "Ejemplo B: jardín de 120 m² con riego básico", M_CASO),
        ("Residencia en fraccionamiento de Tampico. Jardín trasero", "Jardín trasero", M_CASO),
        ("<li>Diseño + instalación completa = $35,000 MXN aprox.</li>", f"<li>Diseño + instalación completa: {SEGUN}</li>", M_CASO),
        ("Caso C: Jardín premium 250 m² con diseño Plan Terra Completo → ~$120,000 MXN", "Ejemplo C: jardín premium de 250 m² con diseño Plan Terra Completo", M_CASO),
        ("Casa en fraccionamiento privado de Altamira. Jardín integral", "Jardín integral", M_CASO),
        ("<li>Diseño + instalación integral = $120,000 MXN aprox.</li>", f"<li>Diseño + instalación integral: {SEGUN}</li>", M_CASO),
        ("va desde $750/mes para jardines pequeños hasta $3,500/mes para proyectos grandes.", "va desde $750/mes, según el tamaño del jardín.", "Mantenimiento: solo \"desde $750/mes\" es oficial."),
        ("Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN previo acuerdo. Muchos clientes financian su jardín a través de créditos personales o de nómina. Para proyectos pequeños de $5,000–$15,000, el pago de contado es habitual.", PAGO_RESPUESTA, M_PAGO),
        (" y entrega una propuesta en menos de 48 horas.", " y te entrega su propuesta.", "Plazo sin confirmar por el dueño."),
    ),
    "cuanto-cuesta-pasto-sintetico-mexico": (
        ("es el más vendido: el mejor equilibrio entre precio y realismo", "es un buen equilibrio entre precio y realismo", M_VENDIDA),
        ("<strong>Garantía (5 a 8 años):</strong>", "<strong>Garantía (3 a 8 años):</strong>", M_GARANTIA),
        ("Estos son tres ejemplos reales con envío", "Estos son tres ejemplos con envío", M_CASO),
    ),
    "errores-pasto-san-agustin-tampico": (
        ("Viveros Terra ofrece asesoría técnica gratuita sobre el protocolo correcto al momento de la compra o instalación. Para proyectos con contrato, se incluye una visita de seguimiento a los 30 días. El arraigo exitoso",
         f"{datos.GARANTIA_PASTO} {datos.PRIMER_RIEGO} El arraigo exitoso", "Garantía oficial de arraigo; sin \"gratuita\" ni visita de seguimiento sin confirmar."),
    ),
    "framboyan-delonix-regia-tampico": (
        ("<td>Ficus benjamina</td><td>$200</td>", f"<td>Ficus benjamina</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Trueno</td><td>$300</td>", f"<td>Trueno</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Neem</td><td>$300</td>", f"<td>Neem</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Tabachín</td><td>$350</td>", f"<td>Tabachín</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Laurel de la India</td><td>$500</td>", f"<td>Laurel de la India</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Tulipán Africano</td><td>$600</td>", f"<td>Tulipán Africano</td><td>{SEGUN}</td>", M_PLANTA),
        ('<th scope="col">Precio desde</th>', '<th scope="col">Precio</th>', M_PLANTA),
    ),
    "jardin-bajo-presupuesto-tampico": (
        ("3 paquetes reales con detalle", "3 paquetes de ejemplo con detalle", M_CASO),
        ("basados en proyectos que ejecutamos regularmente en Tampico, Madero y Altamira, ", "con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira, ", "Dato sin verificar por el dueño."),
        ("<li>6 plantas × $250 = $1,500</li>\n<li>Mano de obra = $1,800</li>\n<li><em>Total: aprox. $8,525 (ajustable según selección de plantas y área exacta)</em></li>", f"<li>6 plantas: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(ajustable según selección de plantas y área exacta)</em></li>", M_PLANTA),
        ("<li>12 plantas × $300 + 2 palmas × $600 = $4,800</li>", f"<li>12 plantas + 2 palmas: {SEGUN}</li>", M_PLANTA),
        ("<li>Riego básico aspersores = $4,500</li>\n<li>Mano de obra general = $3,000</li>\n<li><em>Total: $27,450 (ajustable reduciendo área o número de plantas)</em></li>", f"<li>Riego básico por aspersores: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(ajustable reduciendo área o número de plantas)</em></li>", M_RIEGO),
        ("3 palmas medianas ($800–$1,500 c/u)", f"3 palmas medianas ({SEGUN})", M_PLANTA),
        ("<li>Tierra negra 7 m³ = $10,500</li>\n<li>25 plantas + 3 palmas medianas = $13,500</li>", f"<li>Tierra negra 7 m³ = $10,500</li>\n<li>25 plantas + 3 palmas medianas: {SEGUN}</li>", M_PLANTA),
        ("<li>Riego automatizado = $18,000</li>\n<li>Árbol ornamental + acabados = $5,000</li>\n<li>Mano de obra total = $8,000</li>\n<li><em>Total: $75,100 (el presupuesto de $50K es el punto de entrada, el rango completo va hasta $120K+)</em></li>", f"<li>Riego automatizado: {SEGUN}</li>\n<li>Árbol ornamental + acabados: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(el presupuesto de $50K es el punto de entrada)</em></li>", M_RIEGO),
        ("Según estudios de valuación inmobiliaria aplicados al mercado mexicano, un jardín profesional y en buen estado puede añadir entre el 5% y el 15% al valor de venta o renta de una propiedad residencial.", "Un jardín profesional y en buen estado ayuda a vender o rentar una propiedad residencial.", M_ESTAD),
        (" Un jardín de $50,000 bien ejecutado en una casa de $1,500,000 puede representar una plusvalía de $75,000 a $225,000, con un ROI que va del 50% al 350% de la inversión original.", "", M_ESTAD),
        ("Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN previo acuerdo. Para confirmar solicitamos un anticipo y el resto se acuerda en la cotización. Muchos clientes financian su jardín a través de créditos personales o de nómina.", PAGO_RESPUESTA, M_PAGO),
    ),
    "jardin-vertical-tampico-guia": (
        ("Un jardín vertical pequeño puede armarse desde <strong>$1,500 MXN</strong>.", "Su costo depende del tamaño, la estructura y las plantas: se cotiza.", "Precio sin confirmar."),
        ("puede armarse desde <strong>$1,500 a $3,000 MXN</strong>.", "se cotiza según lo que elijas.", "Precio sin confirmar."),
        ("puede armarse desde $1,500 a $3,000 MXN.", "se cotiza según lo que elijas.", "Precio sin confirmar."),
    ),
    "palma-areca-tampico": (
        ("en mata pequeña, y desde $800 MXN en matas grandes y densas.", f"en mata pequeña; las matas grandes y densas, {SEGUN}.", M_PLANTA),
        ("cuestan desde $800 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("(desde $800)", f"({SEGUN})", M_PLANTA),
        ("tienen precio desde <strong>$800 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-coco-plumoso-tampico": (
        ("para planta pequeña y desde <strong>$1,800 MXN</strong> para ejemplares adultos.", f"para planta pequeña; los ejemplares adultos, <strong>{SEGUN}</strong>.", M_PLANTA),
        ("cuestan desde $1,800 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("tienen precio desde <strong>$1,800 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-kerpis-howea-forsteriana-tampico": (
        ("tamaños y precios desde $500. La palma", "y tamaños. La palma", M_PLANTA),
        ("tamaños y precios desde $500 para lobbies", "y tamaños para lobbies", M_PLANTA),
        ("En Viveros Terra el precio va desde <strong>$500 MXN</strong>.", f"En Viveros Terra su precio va <strong>{SEGUN}</strong>.", M_PLANTA),
        ("esquinas de habitación</td><td>$500 MXN</td>", f"esquinas de habitación</td><td>{SEGUN}</td>", M_PLANTA),
        ("En Viveros Terra, una Palma Kerpis tiene precio desde $500 MXN. Ejemplares grandes y bien formados, ideales para lobbies o espacios amplios, cuestan desde $1,200 MXN.", f"En Viveros Terra, la Palma Kerpis va {SEGUN}.", M_PLANTA),
        ("En Viveros Terra el precio de la Palma Kerpis inicia en <strong>$500 MXN</strong>. Ejemplares grandes y bien formados, con varios tallos por maceta y listos para dar presencia inmediata en un lobby u oficina, tienen precio desde <strong>$1,200 MXN</strong>.", f"En Viveros Terra el precio de la Palma Kerpis va <strong>{SEGUN}</strong>, también en ejemplares grandes y bien formados, con varios tallos por maceta.", M_PLANTA),
    ),
    "palma-real-roystonea-regia-tampico": (
        ("cuestan desde $1,400 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("tienen precio desde <strong>$1,400 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-washingtona-tampico": (
        ("y precios desde $500. La palma más vendida de la región.", "y precios. Crecimiento rápido y resistencia al calor.", M_VENDIDA),
        ("La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y la sequía, y precio desde $500 en Viveros Terra.", "Crecimiento rápido y tolerancia total al calor y la sequía.", M_VENDIDA),
        ("la Washingtonia robusta es, con diferencia, la palma más vendida en Tampico, Madero y Altamira.", "la Washingtonia robusta es una palma muy común en Tampico, Madero y Altamira.", M_VENDIDA),
        ("es <strong>la palma más vendida en Tampico</strong>:", "es <strong>una palma muy resistente para Tampico</strong>:", M_VENDIDA),
        ("En Viveros Terra el precio va desde <strong>$500 MXN</strong> para planta de 0.8–1.2 m.", f"En Viveros Terra su precio va <strong>{SEGUN}</strong>, según la altura.", M_PLANTA),
        ("En Viveros Terra, una planta de 0.8 a 1.2 m tiene precio desde $500 MXN. Ejemplares de 2 a 3 metros, con tronco ya definido, cuestan desde $1,200 MXN.", f"En Viveros Terra, su precio va {SEGUN}, según la altura.", M_PLANTA),
        ("En Viveros Terra el precio de la Palma Washingtona inicia en <strong>$500 MXN</strong> para una planta de 0.8 a 1.2 metros. Ejemplares de 2 a 3 metros, con tronco ya definido, tienen precio desde <strong>$1,200 MXN</strong>.", f"En Viveros Terra el precio de la Palma Washingtona va <strong>{SEGUN}</strong>, según la altura.", M_PLANTA),
    ),
    "palmas-mas-vendidas-tampico-precios": (
        ("Las 8 palmas más vendidas en Tampico con precios 2026: Washingtona desde $500, Viajero $500, Areca $250, Coco, Real, Kerpis y más. Vivero productor.", "8 palmas para jardines en Tampico con precios 2026: Areca y Coco Plumoso desde $250, Real desde $500; las demás, según cotización. Vivero productor.", M_VENDIDA),
        ("Las 8 palmas más vendidas en Tampico con precios 2026", "8 palmas para jardines en Tampico con precios 2026", M_VENDIDA),
        ("Las 8 palmas más vendidas en Tampico (con precios actualizados)", "8 palmas para jardines en Tampico (con precios actualizados)", M_VENDIDA),
        ("Palmas más vendidas Tampico", "8 palmas para Tampico", M_VENDIDA),
        ("Las 8 palmas más vendidas en Tampico son: Washingtona (desde $500), Palma del Viajero ($500), Areca ($250), Real, Coco Plumoso ($250), Kerpis ($500), Cycas Revoluta ($700), y Bambú ($1,000). Los precios varían según el tamaño.", "Estas 8 palmas funcionan bien en Tampico: Areca y Coco Plumoso desde $250 y Real desde $500 en tamaño chico; Washingtona, Palma del Viajero, Kerpis, Cycas Revoluta y Bambú, según cotización. El precio sube con la altura.", M_PLANTA),
        ("<td>Washingtona</td><td>$500</td>", f"<td>Washingtona</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Palma del Viajero</td><td>$500</td>", f"<td>Palma del Viajero</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Kerpis (Howea)</td><td>$500</td>", f"<td>Kerpis (Howea)</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Cycas Revoluta</td><td>$700</td>", f"<td>Cycas Revoluta</td><td>{SEGUN}</td>", M_PLANTA),
        ("<td>Bambú Tarro</td><td>$1,000</td>", f"<td>Bambú Tarro</td><td>{SEGUN}</td>", M_PLANTA),
        ("<strong>Precio desde:</strong> $500 MXN (planta de 0.8–1.2 m). Ejemplares de 2–3 m desde $1,200.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("<strong>Precio desde:</strong> $500 MXN (hijuelo pequeño). Plantas de 1.5–2 m desde $1,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        (" Matas grandes y densas desde $800.", f" Matas grandes y densas, {SEGUN}.", M_PLANTA),
        (" Ejemplares de 2 m desde $1,400.", f" Ejemplares de 2 m, {SEGUN}.", M_PLANTA),
        (" Ejemplares adultos desde $1,800.", f" Ejemplares adultos, {SEGUN}.", M_PLANTA),
        ("<strong>Precio desde:</strong> $500 MXN. Plantas grandes y bien formadas desde $1,200.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("<strong>Precio desde:</strong> $700 MXN. Especímenes grandes (múltiples coronas) desde $3,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("<strong>Precio desde:</strong> $1,000 MXN (mata mediana). Matas grandes y densas desde $2,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("La Washingtona es con diferencia la palma más vendida en la región.", "La Washingtona es una palma muy común en la región.", M_VENDIDA),
        ("o contáctanos por WhatsApp para una asesoría sin costo.", "o escríbenos por WhatsApp para asesorarte.", M_GRATIS),
        ("tienen garantía de arraigo de 30 días: si no prenden y se regaron y cuidaron como indicamos, las reponemos sin costo. No cubre falta de riego, cambio de lugar, daños por mascotas o clima extremo. Si compras la palma y la siembras por tu cuenta, te damos asesoría gratis sobre la plantación.", "tienen garantía de 30 días, con el riego indicado. No cubre falta de riego, cambio de lugar, daños por mascotas o clima extremo. Si compras la palma y la siembras por tu cuenta, te orientamos sobre la plantación.", "Garantía de plantas: 30 días con condiciones (datos.GARANTIA_PLANTAS); \"sin costo\" solo en la de pasto."),
    ),
    "palmas-tropicales-jardin-tampico": (
        ("Precio aproximado: desde $800 (planta) hasta $4,500 (adulta)", f"Precio: {SEGUN}", M_PLANTA),
        ("Desde <strong>$800 pesos</strong> para planta pequeña de 40–60 cm, hasta <strong>$4,500+</strong> para ejemplares adultos de 2–3 metros para impacto inmediato.", f"Va <strong>{SEGUN}</strong>, según el tamaño: desde planta pequeña de 40–60 cm hasta ejemplares adultos de 2–3 metros para impacto inmediato.", M_PLANTA),
    ),
    "pasto-sintetico-calor-mexico": (
        ("(garantías de 5-8 años)", "(garantías de 3 a 8 años según modelo)", M_GARANTIA),
        ("Por eso podemos dar garantía de 5 a 8 años según modelo.", f"Por eso podemos dar garantía {GARANTIA_SINTETICO}.", M_GARANTIA),
        ("(por eso ofrecemos garantía de 5 a 8 años según modelo)", f"(por eso ofrecemos garantía {GARANTIA_SINTETICO})", M_GARANTIA),
    ),
    "pasto-sintetico-para-perros": (
        ("El más vendido para familias: suave", "Para familias: suave", M_VENDIDA),
        ("(28 mm, el más vendido para familias con mascotas)", "(28 mm, para familias con mascotas)", M_VENDIDA),
        ("Todos con garantía de 5-8 años y", "Toscana 28, Irlanda 25, Capri 20 y Toscana 18 tienen garantía de 5 a 8 años según modelo y", M_GARANTIA),
        ("El 90% de los problemas de olor", "La mayoría de los problemas de olor", M_ESTAD),
    ),
    "pasto-sintetico-vs-natural-tampico": (
        ("<td>Instalación (50 m²)</td><td>~$8,000–$12,000</td><td>~$18,000–$25,000</td>", f"<td>Instalación (50 m²)</td><td>desde {dinero(50 * P['pasto_instalado_m2'])}</td><td>{dinero(50 * P['sintetico_instalado_m2'][0])}–{dinero(50 * P['sintetico_instalado_m2'][1])}</td>", "Instalación con los precios oficiales por m²."),
        ("<td><strong>~$92,000–$150,000</strong></td><td><strong>~$18,000–$25,000</strong></td>", f"<td><strong>~$94,000–$182,000</strong></td><td><strong>{dinero(50 * P['sintetico_instalado_m2'][0])}–{dinero(50 * P['sintetico_instalado_m2'][1])}</strong></td>", "Suma recalculada con la instalación oficial."),
    ),
    "plantas-resistentes-sal-golfo-tampico": (
        (_DEK_BANQUETA, "12 especies de plantas que resisten la salinidad del aire marino en Tampico: ideales para jardines costeros, terrazas frente al Golfo y proyectos en zona playa.", M_DEK),
        ("¿Por qué la sal marina mata el 60% de las plantas?", "¿Por qué la sal marina mata tantas plantas?", M_ESTAD),
        ("La brisa salina del Golfo mata el 60% de las plantas comunes.", "La brisa salina del Golfo mata muchas plantas comunes.", M_ESTAD),
        ("a más de 2 km del mar el efecto disminuye 80%", "a más de 2 km del mar el efecto disminuye mucho", M_ESTAD),
        ("Más de 2 km de la costa el efecto de la sal disminuye 80%.", "A más de 2 km de la costa el efecto de la sal disminuye mucho.", M_ESTAD),
        ("retiene 50% menos nutrientes", "retiene menos nutrientes", M_ESTAD),
        ("pierde 80% del follaje", "pierde buena parte del follaje", M_ESTAD),
    ),
    "que-altura-de-pasto-sintetico-elegir": (
        ("es el más vendido por algo: nadie se arrepiente", "es buena opción por algo: nadie se arrepiente", M_VENDIDA),
        ("es el modelo más vendido en México para uso residencial", "es una opción muy equilibrada para uso residencial", M_VENDIDA),
        ("Aquí vive el <strong>90% de los jardines familiares</strong>.", "Aquí cae <strong>la mayoría de los jardines familiares</strong>.", M_ESTAD),
    ),
    "riego-automatico-tampico-roi": (
        ("casos reales por tamaño de jardín.", "ejemplos por tamaño de jardín.", M_CASO),
        ("casos reales de jardines en Tampico.", "ejemplos de jardines en Tampico.", M_CASO),
        ("~12–18 m³ (ahorro 40–60%)", "~18 m³ (ahorro de hasta 40%)", M_AHORRO),
        ("<td>~$600–$900 MXN</td>", "<td>~$900 MXN</td>", M_AHORRO),
        ("<td>$15,000–$60,000 MXN</td>", f"<td>{dinero(R0)}–{dinero(R1)}/m²</td>", M_RIEGO),
        ("<td>$8,000–$15,000</td><td>Aspersores básicos o goteo</td>", f"<td>{riego(30, 60)}</td><td>Aspersores básicos o goteo</td>", M_RIEGO),
        ("<td>$15,000–$28,000</td><td>Aspersores emergentes + goteo zonas plantas</td>", f"<td>{riego(60, 120)}</td><td>Aspersores emergentes + goteo zonas plantas</td>", M_RIEGO),
        ("<td>$28,000–$45,000</td><td>Sistema mixto multi-zona con programador</td>", f"<td>{riego(120, 200)}</td><td>Sistema mixto multi-zona con programador</td>", M_RIEGO),
        ("<td>$45,000–$90,000</td><td>Sistema completo con controlador inteligente</td>", f"<td>{riego(200, 500)}</td><td>Sistema completo con controlador inteligente</td>", M_RIEGO),
        ("<td>$90,000+</td>", f"<td>{SEGUN}</td>", M_RIEGO),
        ("3 casos reales de riego automático en Tampico", "3 ejemplos de riego automático en Tampico", M_CASO),
        ("Caso A: Residencial 80 m² en fraccionamiento de Madero", "Ejemplo A: residencial de 80 m²", M_CASO),
        ("Caso B: Residencial 200 m² en fraccionamiento privado de Tampico", "Ejemplo B: residencial de 200 m²", M_CASO),
        ("Caso C: Comercial 500 m² (oficinas corporativas en Altamira)", "Ejemplo C: comercial de 500 m²", M_CASO),
        ("<li>Inversión: $18,000 MXN</li>", f"<li>Inversión: {riego(80)}</li>", M_RIEGO),
        ("<li>Inversión: $38,000 MXN</li>", f"<li>Inversión: {riego(200)}</li>", M_RIEGO),
        ("<li>Inversión: $85,000 MXN</li>", f"<li>Inversión: {SEGUN}</li>", M_RIEGO),
        ("<li>Consumo después: 10 m³/mes → $500/mes</li>\n<li>Ahorro mensual: $600 MXN</li>\n<li>Ahorro anual: $7,200 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("<li>Consumo después: 16 m³/mes → $800/mes</li>\n<li>Ahorro mensual: $1,200 MXN</li>\n<li>Ahorro anual: $14,400 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("<li>Consumo después: 36 m³/mes → $1,800/mes</li>\n<li>Ahorro mensual: $2,700 MXN</li>\n<li>Ahorro anual: $32,400 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("<li>Consumo automático: 15 m³/mes × $50/m³ = $750/mes</li>\n<li><strong>Ahorro mensual: $750 MXN</strong></li>\n<li>Ahorro anual: $750 × 12 = <strong>$9,000 MXN/año</strong></li>", "<li>Consumo automático: hasta 40% menos (18 m³/mes × $50/m³ = $900/mes)</li>\n<li><strong>Ahorro mensual: $600 MXN</strong></li>\n<li>Ahorro anual: $600 × 12 = <strong>$7,200 MXN/año</strong></li>", M_AHORRO),
    ),
    "sistema-riego-automatico-conviene-tampico": (
        (_DEK_BANQUETA, "¿Conviene un sistema de riego automático en el clima tropical de Tampico? Guía honesta: cuándo sí, cuándo no y cuánto cuesta.", M_DEK),
        ("Para un jardín residencial de 100 m² el costo va de $15,000 (goteo simple) a $32,000 (sistema mixto con controlador WiFi). Para áreas comerciales o industriales con más de 500 m² el costo arranca en $80,000.", f"Para un jardín residencial de 100 m² el costo va de {riego(100)}. Para áreas comerciales o industriales con más de 500 m², {SEGUN}.", M_RIEGO),
        ("Costo en Tampico: $400–$800 por visita.", f"Costo: {SEGUN}.", "Precio sin confirmar."),
        ("cuesta solo $3,000–$5,000", f"se cotiza aparte", "Precio sin confirmar."),
        ("el costo del sistema ($15,000–$25,000) pesa más", "el costo del sistema pesa más", M_RIEGO),
        ("<td>$15,000–$25,000 (100 m²)</td>", f"<td>{riego(100)} (100 m²)</td>", M_RIEGO),
        ("<td>$8,000–$18,000 (100 m²)</td>", f"<td>{riego(100)} (100 m²)</td>", M_RIEGO),
        ("<td>$25,000–$45,000 (200 m²)</td>", f"<td>{riego(200)} (200 m²)</td>", M_RIEGO),
        ("<td>+$4,000 al sistema</td>", f"<td>{SEGUN}</td>", "Precio sin confirmar."),
        ("Ejemplo real: cuánto se ahorra", "Ejemplo: cuánto se ahorra", M_CASO),
        ("<p>Cliente típico Viveros Terra (Cd. Madero, casa residencial):</p>", "<p>Ejemplo de una casa residencial:</p>", M_CASO),
        ("controlador WiFi = <strong>$32,000</strong>", f"controlador WiFi = <strong>{riego(150)}</strong>", M_RIEGO),
        ("<li><strong>Ahorro mensual:</strong> $130 en agua + $400 en tiempo (regaban 2 hrs/día en verano)</li>\n", "", M_CASO),
        ("<p>Adicional: el pasto se mantiene 60% más uniforme = no hay que comprar pasto nuevo en 5 años (ahorro $8,000+).</p>", "<p>Adicional: el pasto se mantiene más uniforme.</p>", M_ESTAD),
        ("reduce el consumo de agua entre 35% y 45%", f"reduce el consumo de agua {datos.RIEGO_AHORRO}", M_AHORRO),
    ),
    "sistema-riego-automatizado-tampico": (
        ("tiene un costo de instalación de <strong>$8,000 a $25,000 pesos</strong> dependiendo del tipo y complejidad.", f"tiene un costo de instalación de <strong>{dinero(R0)} a {dinero(R1)} por m²</strong>, según el tipo y la complejidad.", M_RIEGO),
        ("Un <strong>sistema básico de aspersión para 50 m²</strong> cuesta entre $8,000 y $15,000 pesos instalado. Un sistema completo para jardín grande de 100–150 m² puede ir de $15,000 a $28,000.", f"Un <strong>sistema básico de aspersión para 50 m²</strong> cuesta {riego(50)} instalado. Un sistema completo para jardín grande de 100–150 m² puede ir de {riego(100, 150)}.", M_RIEGO),
        ("Costo aproximado para 50 m²: $8,000–$15,000", f"Costo aproximado para 50 m²: {riego(50)}", M_RIEGO),
        ("Costo aproximado para 20 plantas: $4,000–$10,000", f"Costo: {SEGUN}", M_RIEGO),
        ("(ahorro hasta 60%)", f"(ahorro {datos.RIEGO_AHORRO})", M_AHORRO),
        ("<td>$8,000–$15,000</td><td>$300–$600</td>", f"<td>{riego(50, 80)}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("<td>$4,000–$10,000</td><td>$200–$400</td>", f"<td>{SEGUN}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("<td>$15,000–$28,000</td><td>$500–$1,000</td>", f"<td>{riego(100, 150)}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("<td>$40,000–$150,000</td><td>$2,000–$8,000</td>", f"<td>{SEGUN}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("<p>Para un sistema de $12,000 pesos en un jardín residencial de 80 m²:</p>", "<p>En un jardín residencial de 80 m²:</p>", M_RIEGO),
        ("<li>Ahorro en agua: ~$500/mes = $6,000/año</li>\n<li>Ahorro en jardinero (menos idas para riego manual): ~$300/mes = $3,600/año</li>\n<li>Menor mortalidad de plantas por riego inadecuado: valor estimado ~$2,000/año</li>\n<li><strong>Ahorro total anual: ~$11,600</strong></li>", f"<li>Ahorro en agua: {datos.RIEGO_AHORRO}</li>\n<li>Menos idas del jardinero para riego manual</li>\n<li>Menor mortalidad de plantas por riego inadecuado</li>", M_ESTAD),
        ("<strong>Visita técnica.</strong> Medimos el área", f"<strong>Visita técnica.</strong> {datos.VISITA_COSTO} Medimos el área", M_VISITA),
    ),
    "tierra-negra-costal-camion-tampico": (
        ("el camión volteo de 8 m³ a $1,500/m³ es más económico.", f"el camión volteo de 8 m³ en {CAMION_8} es más económico.", M_TIERRA),
        ("Costo camión 8 m³ ($12,000)", f"Costo camión 8 m³ ({CAMION_8})", M_TIERRA),
        ("<td>$12,000 (8 m³ completo)</td>", f"<td>{CAMION_8} (8 m³ completo)</td>", M_TIERRA),
        ("<td>$12,000 (cubre ~80 m²)</td>", f"<td>{CAMION_8} (cubre ~80 m²)</td>", M_TIERRA),
        ("<td>$12,000–$24,000</td>", f"<td>Desde {CAMION_8}</td>", M_TIERRA),
        ("se puede incluir en el mismo pedido de plantas sin costo de envío adicional", "se puede incluir en el mismo pedido de plantas", M_ENTREGA),
        ("Las entregas de camión tienen costo de flete según la distancia. Los costales se pueden incluir en pedidos de plantas o pasto sin costo adicional para órdenes mayores a $3,000 MXN.", datos.ENTREGA_COBRO, M_ENTREGA),
        ("más del doble que el camión ($1,500/m³)", f"más del doble que el m³ suelto ({dinero(P['tierra_negra_m3'])}/m³)", M_TIERRA),
        ("Un costal estándar de tierra negra vegetal en Viveros Terra pesa aproximadamente 25–30 kg y tiene un volumen de 25–30 litros (0.025–0.03 m³). Este peso varía ligeramente según el contenido de humedad al momento del llenado.", "No publicamos el peso porque varía con la humedad; un costal estándar de tierra negra vegetal en Viveros Terra tiene un volumen de 25–30 litros (0.025–0.03 m³).", "Sin peso de costal: el dueño no lo tiene."),
    ),
}


def de(clave):
    return tuple(CORRECCIONES.get(clave, ()))
VT_EOF
```

- [ ] **Step 2: Extraer los 52 artículos y el índice**

```bash
cd ~/dev/viverosterra-e2h
python3 tools/site/extraer_blog.py escribir
ls tools/site/contenido/blog | wc -l
python3 - <<'PY'
import sys; sys.path.insert(0, 'tools/site')
from contenido import blog_correcciones as bc
print(sum(len(bc.de(k)) for k in bc.CORRECCIONES), sum(1 for k in bc.CORRECCIONES if bc.de(k) and k != '/blog'))
PY
```

Expected: `listo`; `53`; `212 30`. Una corrección que no encuentra su texto detiene la corrida con su slug y su texto: corrige la tripleta, no el extractor.

- [ ] **Step 3: Revisar a mano tres archivos, uno por envoltura**

```bash
cd ~/dev/viverosterra-e2h
sed -n '/^-->/,$p' tools/site/contenido/blog/palma-areca-tampico.html | head -20
sed -n '/^-->/,$p' tools/site/contenido/blog/cuanto-cuesta-jardin-tampico-precios.html | head -20
sed -n '/^-->/,$p' tools/site/contenido/blog/jardines-temporada-lluvias-tampico.html | head -20
```

Expected: HTML sin clases de Tailwind, `h2` con `id`, tablas envueltas en `.vt-art__tabla`, avisos en `<aside class="vt-art__nota …">`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/contenido/blog_correcciones.py tools/site/contenido/blog
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(blog): 52 artículos extraídos con las correcciones del barrido" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Temas y contenido de las plantillas

**Files:** Create: `tools/site/contenido/blog_clusters.py`, `tools/site/contenido/articulo.py`, `tools/site/contenido/blog_indice.py`, `tools/site/componentes_blog.py`

- [ ] **Step 1: Escribir los cuatro archivos**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/contenido
cat > tools/site/contenido/blog_clusters.py <<'VT_EOF'
"""Tema comercial de cada artículo del blog: a qué landing lleva, qué etiqueta de "producto relacionado" lleva (una sola)
y sus 2–3 enlaces contextuales (spec §3.3 y §6.5). Solo datos; los precios salen de datos.PRECIOS y lo que no tiene precio
confirmado va "Según cotización"."""
import datos
from componentes import dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION
CIUDADES = ("cdmx", "guadalajara", "monterrey", "queretaro", "puebla", "merida")
NOMBRES_CIUDAD = {"cdmx": "CDMX", "guadalajara": "Guadalajara", "monterrey": "Monterrey", "queretaro": "Querétaro",
                  "puebla": "Puebla", "merida": "Mérida"}


def _desde(monto, antes="Desde", unidad=""):
    return {"antes": antes, "monto": monto, "unidad": unidad}


CLUSTERS = {
    "pasto-natural": {
        "landing": ("/pasto-en-rollo-tampico", "Ver pasto en rollo"),
        "titulo": "¿Vas a poner pasto nuevo?",
        "etiqueta": {"nombre": "Pasto San Agustín en rollo", "cientifico": "Stenotaphrum secundatum", "antes": "Instalado · desde",
                     "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m²",
                     "filas": (("Solo el pasto", f"{dinero(P['pasto_solo_m2'])} /m²"),)},
        "enlaces": (("pasto San Agustín en rollo", "/pasto-en-rollo-tampico"),
                    ("protocolo de riego de 20 días", "/protocolo-cuidados-pasto-san-agustin"),
                    ("lista de precios", "/precios")),
    },
    "pasto-sintetico": {
        "landing": ("/pasto-sintetico", "Ver los 9 modelos"),
        "titulo": "¿Ya sabes qué modelo te conviene?",
        "etiqueta": {"nombre": "Pasto sintético en rollo", "antes": "Rollo de 50 m² · desde", "monto": dinero(P["sintetico_tienda_m2"]),
                     "unidad": "/m²", "filas": (("Envío", "por rollo, según estado"),)},
        "enlaces": (("tienda de pasto sintético", "/pasto-sintetico"),
                    ("pasto sintético instalado en Tampico", "/pasto-sintetico-tampico")),
    },
    "riego": {
        "landing": ("/sistema-riego-tampico", "Ver sistema de riego"),
        "titulo": "¿Quieres que tu jardín se riegue solo?",
        "etiqueta": {"nombre": "Sistema de riego automático", "antes": "Instalado", "monto": f"{dinero(P['riego_m2'][0])}–{dinero(P['riego_m2'][1])}",
                     "unidad": "/m²"},
        "enlaces": (("sistema de riego en Tampico", "/sistema-riego-tampico"), ("mantenimiento de jardines", "/mantenimiento-jardines-tampico"),
                    ("lista de precios", "/precios")),
    },
    "diseno": {
        "landing": ("/diseno-jardines-tampico", "Ver diseño de jardines"),
        "titulo": "¿Quieres un plan para tu jardín?",
        "etiqueta": {"nombre": "Diseño de jardín", "antes": "Plan Esencial · desde", "monto": dinero(P["diseno"]), "unidad": ""},
        "enlaces": (("diseño de jardines en Tampico", "/diseno-jardines-tampico"), ("lista de precios", "/precios"),
                    ("plantas para jardín", "/plantas-para-jardin-tampico")),
    },
    "mantenimiento": {
        "landing": ("/mantenimiento-jardines-tampico", "Ver mantenimiento"),
        "titulo": "¿Prefieres que lo hagamos nosotros?",
        "etiqueta": {"nombre": "Mantenimiento de jardines", "antes": "Desde", "monto": dinero(P["mantenimiento_mes"]), "unidad": "/mes"},
        "enlaces": (("mantenimiento de jardines en Tampico", "/mantenimiento-jardines-tampico"), ("lista de precios", "/precios"),
                    ("jardinería en Ciudad Madero", "/jardineria-ciudad-madero")),
    },
    "palmas": {
        "landing": ("/palmas-tropicales-tampico", "Ver palmas"),
        "titulo": "¿Ya elegiste tu palma?",
        "etiqueta": {"nombre": "Palmas tropicales", "antes": "Tamaño chico · desde", "monto": dinero(P["palma_desde"]), "unidad": "",
                     "filas": (("Palma real", f"desde {dinero(P['palma_real'])}"),)},
        "enlaces": (("palmas tropicales en Tampico", "/palmas-tropicales-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("palmas para proyectos", "/palmas-mayoreo-proyectos")),
    },
    "arboles": {
        "landing": ("/arboles-ornamentales-tampico", "Ver árboles"),
        "titulo": "¿Buscas un árbol para tu jardín?",
        "etiqueta": {"nombre": "Flamboyán", "cientifico": "Delonix regia", "antes": "Ejemplar joven · desde", "monto": dinero(P["flamboyan"]), "unidad": ""},
        "enlaces": (("árboles ornamentales en Tampico", "/arboles-ornamentales-tampico"), ("árboles para banqueta", "/arboles-para-banqueta-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "banqueta": {
        "landing": ("/arboles-para-banqueta-tampico", "Ver árboles para banqueta"),
        "titulo": "¿Buscas un árbol para tu banqueta?",
        "etiqueta": {"nombre": "Árboles para banqueta", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("árboles para banqueta en Tampico", "/arboles-para-banqueta-tampico"), ("árboles ornamentales", "/arboles-ornamentales-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "plantas": {
        "landing": ("/plantas-para-jardin-tampico", "Ver plantas para jardín"),
        "titulo": "¿Armamos tu lista de plantas?",
        "etiqueta": {"nombre": "Plantas para jardín", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas para jardín en Tampico", "/plantas-para-jardin-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("diseño de jardines", "/diseno-jardines-tampico")),
    },
    "interior": {
        "landing": ("/plantas-de-interior-tampico", "Ver plantas de interior"),
        "titulo": "¿Buscas plantas para adentro?",
        "etiqueta": {"nombre": "Plantas de interior", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas de interior en Tampico", "/plantas-de-interior-tampico"), ("catálogo del vivero", "/catalogo")),
    },
    "tierra": {
        "landing": ("/tierra-negra-vegetal-tampico", "Ver tierra negra"),
        "titulo": "¿Cuánta tierra necesitas?",
        "etiqueta": {"nombre": "Tierra negra vegetal", "antes": "Costal", "monto": dinero(P["tierra_negra_costal"]), "unidad": "",
                     "filas": (("Metro cúbico", dinero(P["tierra_negra_m3"])),)},
        "enlaces": (("tierra negra en Tampico", "/tierra-negra-vegetal-tampico"), ("tezontle rojo", "/tezontle-rojo-tampico"), ("lista de precios", "/precios")),
    },
    "tezontle": {
        "landing": ("/tezontle-rojo-tampico", "Ver tezontle"),
        "titulo": "¿Cuánto tezontle necesitas?",
        "etiqueta": {"nombre": "Tezontle rojo", "antes": "Costal · desde", "monto": dinero(P["tezontle_costal"]), "unidad": ""},
        "enlaces": (("tezontle rojo en Tampico", "/tezontle-rojo-tampico"), ("tierra negra", "/tierra-negra-vegetal-tampico"), ("lista de precios", "/precios")),
    },
}

_SINTETICOS = ("como-instalar-pasto-sintetico", "cuanto-cuesta-pasto-sintetico-mexico", "pasto-sintetico-calor-mexico",
               "pasto-sintetico-para-perros", "pasto-sintetico-vs-natural-tampico", "que-altura-de-pasto-sintetico-elegir")
POR_SLUG = (
    ("pasto-sintetico", _SINTETICOS),
    ("pasto-natural", ("cesped-amarillo-tampico-causas-soluciones", "cuando-plantar-pasto-tampico-calendario",
                       "cuando-regar-pasto-san-agustin-tampico", "errores-pasto-san-agustin-tampico",
                       "pasto-san-agustin-instalacion-mantenimiento", "pasto-san-agustin-vs-japones")),
    ("riego", ("como-ahorrar-agua-jardin-tampico", "riego-automatico-tampico-roi", "sistema-riego-automatico-conviene-tampico",
               "sistema-riego-automatizado-tampico")),
    ("diseno", ("cuanto-cuesta-jardin-tampico-precios", "diseno-jardines-tampico-guia", "jardin-bajo-presupuesto-tampico",
                "jardin-en-macetas-terraza-tampico-guia", "jardin-vertical-tampico-guia")),
    ("mantenimiento", ("acolchado-mulch-jardin-tampico", "como-evitar-encharcamientos-jardin-tampico",
                       "fertilizacion-jardines-tampico-temporada-lluvias", "hongos-plantas-exceso-humedad-tampico",
                       "jardines-temporada-lluvias-tampico", "nortes-tampico-proteger-plantas-jardin",
                       "plagas-comunes-jardin-tampico", "poda-arboles-palmas-tampico-guia",
                       "temporada-huracanes-proteger-jardin-tampico")),
    ("palmas", ("como-medir-plantas-altura-cepellon", "como-plantar-palma-arbol-paso-a-paso-tampico", "cuidados-palma-del-viajero-ravenala",
                "palma-areca-tampico", "palma-bismarckia-bismarckia-nobilis-tampico", "palma-coco-plumoso-tampico",
                "palma-cola-de-zorro-wodyetia-bifurcata-tampico", "palma-kerpis-howea-forsteriana-tampico", "palma-real-roystonea-regia-tampico",
                "palma-triangular-dypsis-decaryi-tampico", "palma-washingtona-tampico", "palmas-mas-vendidas-tampico-precios",
                "palmas-tropicales-jardin-tampico")),
    ("arboles", ("framboyan-delonix-regia-tampico",)),
    ("banqueta", ("arboles-para-sembrar-en-banqueta",)),
    ("plantas", ("buganvilia-tampico-cuidados-floracion", "duranta-erecta-tampico-cuidados-seto", "plantas-resistentes-sal-golfo-tampico")),
    ("interior", ("ficus-elastica-cuidados-tampico", "plantas-interior-tampico")),
    ("tierra", ("tierra-negra-costal-camion-tampico",)),
    ("tezontle", ("tezontle-usos-jardin-tampico",)),
)
TEMA = {slug: tema for tema, slugs in POR_SLUG for slug in slugs}
# Los blogs de precios enlazan a /precios como fuente única (spec §3.5).
A_PRECIOS = ("cuanto-cuesta-jardin-tampico-precios", "cuanto-cuesta-pasto-sintetico-mexico", "jardin-bajo-presupuesto-tampico")


def de(slug):
    """Copia del tema del artículo con sus enlaces finales (los de sintético rotan una ciudad con página de envío)."""
    tema = TEMA[slug]
    base = CLUSTERS[tema]
    enlaces = tuple(base["enlaces"])
    if tema == "pasto-sintetico":
        c = CIUDADES[_SINTETICOS.index(slug)]
        enlaces += ((f"envío de pasto sintético a {NOMBRES_CIUDAD[c]}", f"/pasto-sintetico/envio/{c}"),)
    if slug in A_PRECIOS and not any(h == "/precios" for _t, h in enlaces):
        enlaces = (("lista de precios vigente", "/precios"),) + enlaces[:2]
    return {**base, "tema": tema, "enlaces": enlaces[:3]}
VT_EOF
mkdir -p tools/site/contenido
cat > tools/site/contenido/articulo.py <<'VT_EOF'
"""Los 52 artículos del blog (Etapa 2h). El cuerpo vive en contenido/blog/<slug>.html (HTML con un comentario de metadatos
en JSON: la excepción a "contenido en .py", justificada por el volumen de prosa). Aquí se arma lo que la plantilla
tools/site/plantillas/articulo.py necesita: portada, autor y fecha, índice (de los <h2> del cuerpo, así nunca apunta a un
id que no existe), preguntas, etiqueta de producto, CTA y relacionados. El autor es datos.AUTOR_BLOG."""
import json
import re
from pathlib import Path

import datos
import paginas
from contenido import blog_clusters

DIR = Path(__file__).resolve().parent / "blog"
CLAVES = tuple(sorted(p.stem for p in DIR.glob("*.html")))
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
         "diciembre")
H2_RE = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)


def leer(slug):
    """(metadatos, cuerpo HTML) del artículo."""
    texto = (DIR / f"{slug}.html").read_text(encoding="utf-8")
    cabeza, _, cuerpo = texto.partition("\n-->\n")
    return json.loads(cabeza.removeprefix("<!--vt:meta\n")), cuerpo


def fecha_larga(iso):
    a, m, d = (int(x) for x in iso[:10].split("-"))
    return f"{d} de {MESES[m - 1]} de {a}"


def sin_etiquetas(fragmento):
    return re.sub(r"<[^>]+>", "", fragmento)


def indice(cuerpo, faq, titulo_faq, respuesta):
    items = [("respuesta", respuesta["titulo"])] if respuesta else []
    items += [(i, sin_etiquetas(t)) for i, t in H2_RE.findall(cuerpo)]
    if faq:
        items.append(("preguntas", titulo_faq))
    return tuple(items)


def fechas(jsonld):
    articulo = next(n for n in jsonld["@graph"] if n.get("@type") == "Article")
    publicado, modificado = articulo.get("datePublished"), articulo.get("dateModified")
    return publicado, modificado or publicado


class _Pagina:
    def __init__(self, slug):
        doc, cuerpo = leer(slug)
        ruta = f"/blog/{slug}"
        publicado, modificado = fechas(doc["jsonld"])
        tema = blog_clusters.de(slug)
        self.CONTENIDO = {
            "meta": doc["meta"], "jsonld": doc["jsonld"], "tipo": "blog", "slug": slug,
            "migas": (("Inicio", "/"), ("Blog", "/blog"), (doc["h1"], None)),
            "kicker": doc["kicker"], "h1": doc["h1"], "dek": doc["dek"], "minutos": doc["minutos"],
            "autor": datos.AUTOR_BLOG, "publicado": fecha_larga(publicado), "publicado_iso": publicado,
            "actualizado": fecha_larga(modificado), "actualizado_iso": modificado,
            "respuesta": doc["respuesta"], "cuerpo": cuerpo, "faq_titulo": doc["faq_titulo"],
            "faq": tuple(tuple(p) for p in doc["faq"]), "indice": indice(cuerpo, doc["faq"], doc["faq_titulo"], doc["respuesta"]),
            "tema": tema, "mensaje": paginas.contexto(ruta)["mensaje"].rsplit("\n\n", 1)[0],
            "relacionados_titulo": doc["relacionados_titulo"], "relacionados": tuple(doc["relacionados"]),
        }
        self.PARIDAD = doc.get("paridad") or {"reemplazos": {}, "retirados": {}}


def pagina(slug):
    return _Pagina(slug)
VT_EOF
mkdir -p tools/site/contenido
cat > tools/site/contenido/blog_indice.py <<'VT_EOF'
"""/blog: las secciones y tarjetas salen de contenido/blog/_indice.json, extraído de la página publicada (mismas fotos, en
el mismo orden). El conteo lo pone shell.aplicar en cada <span data-vt-conteo="blog">."""
import json
from pathlib import Path

import datos

_DOC = json.loads((Path(__file__).resolve().parent / "blog" / "_indice.json").read_text(encoding="utf-8"))
CONTENIDO = {
    "meta": _DOC["meta"], "jsonld": _DOC["jsonld"], "tipo": "blog", "foto": _DOC["foto"], "secciones": _DOC["secciones"],
    "migas": (("Inicio", "/"), ("Blog", None)),
    "h1": "Blog de Jardinería <span>para Tampico y Tamaulipas.</span>",
    "lede": ("Guías prácticas, comparativas honestas y consejos de jardinería adaptados al clima cálido-húmedo del sur de "
             f"Tamaulipas. Por el {datos.AUTOR_BLOG[0].lower()}{datos.AUTOR_BLOG[1:]}."),
    "mensaje": "Hola, vi el blog de Viveros Terra y quiero cotizar",
    "servicios": (("/pasto-en-rollo-tampico", "Pasto en Rollo", "San Agustín · Japonés · Bermuda"),
                  ("/pasto-sintetico-tampico", "Pasto Sintético", "Venta e instalación profesional"),
                  ("/plantas-palmas-arboles-tampico", "Plantas, Palmas y Árboles", "Vivero productor directo"),
                  ("/tezontle-rojo-tampico", "Tezontle Rojo", "Costal y camión volteo"),
                  ("/tierra-negra-vegetal-tampico", "Tierra Negra Vegetal", "Costal y camión volteo"),
                  ("/diseno-jardines-tampico", "Diseño de Jardines", "Plan Terra · Desde $3,000")),
}
PARIDAD = {"reemplazos": {"Las 8 palmas más vendidas en Tampico (con precios)": "8 palmas para jardines en Tampico (con precios)",
                          "Cómo Ahorrar Hasta 50% de Agua en Tu Jardín en Tampico": "Cómo Ahorrar Hasta 40% de Agua en Tu Jardín en Tampico"},
           "retirados": {"$300": "La tarjeta de la Palma Areca decía desde $300; el precio oficial es desde $250 (datos.py)."}}
VT_EOF
mkdir -p tools/site
cat > tools/site/componentes_blog.py <<'VT_EOF'
"""Componentes del artículo y del índice del blog (Etapa 2h)."""
import componentes as c
import datos
from partials import esc

P = datos.PRECIOS
PRODUCTO = {"codigo": "Producto relacionado", "aviso": "Con IVA"}


def cabeza(k):
    dek = f'<p class="vt-art__dek">{k["dek"]}</p>' if k["dek"] else ""
    rotulo = "Actualizado" if k["actualizado_iso"] != k["publicado_iso"] else "Publicado"
    fechas = f'<span><b>{rotulo}</b> <time datetime="{esc(k["actualizado_iso"])}">{k["actualizado"]}</time></span>'
    tiempo = f'<span>{k["minutos"]} min de lectura</span>' if k["minutos"] else ""
    return (f'<header class="vt-art__cabeza"><div class="vt-wrap">{c.migas(k["migas"])}<p class="vt-kicker">{k["kicker"]}</p>'
            f'<h1 id="vt-h1">{k["h1"]}</h1>{dek}<p class="vt-art__meta"><span><b>Por</b> {esc(k["autor"])}</span>{fechas}{tiempo}</p>'
            f'</div></header>')


def respuesta(r):
    if not r:
        return ""
    tag = "h2" if r["es_titulo"] else "p"
    clase = ' class="vt-art__respuesta-t"'
    parrafos = "".join(f"<p>{p}</p>" for p in r["parrafos"])
    return f'<section id="respuesta" class="vt-art__respuesta"><{tag}{clase}>{r["titulo"]}</{tag}>{parrafos}</section>'


def indice(items):
    filas = "".join(f'<li><a href="#{esc(i)}"><span aria-hidden="true">{n:02d}</span>{t}</a></li>'
                    for n, (i, t) in enumerate(items))
    return f'<nav class="vt-art__indice" aria-label="En este artículo"><b>En este artículo</b><ol>{filas}</ol></nav>'


def enlaces(items):
    filas = "".join(f'<li><a href="{esc(h)}">{t}</a></li>' for t, h in items)
    return f'<nav class="vt-art__sigue" aria-label="Para seguir"><b>Para seguir</b><ul>{filas}</ul></nav>'


def producto(tema, mensaje, tipo):
    href, texto = tema["landing"]
    return (f'<section class="vt-art__producto" aria-labelledby="vt-art-prod"><div class="vt-wrap vt-art__producto-grid"><div>'
            f'<h2 id="vt-art-prod">{tema["titulo"]}</h2><div class="vt-cta"><a class="vt-btn vt-btn--tinta" '
            f'data-cta="{tipo}:landing" href="{esc(href)}">{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>'
            f'{c.boton_wa(mensaje, f"{tipo}:cierre")}</div><p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p></div>'
            f'{c.etiqueta({**PRODUCTO, **tema["etiqueta"]})}</div></section>')


def relacionados(titulo, items):
    filas = "".join(f'<li><p class="vt-art__rel-c">{esc(i["categoria"])}</p><h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3>'
                    + (f'<p>{i["texto"]}</p>' if i["texto"] else "") + "</li>" for i in items)
    return (f'<section class="vt-art__rel" aria-labelledby="vt-art-rel"><div class="vt-wrap"><h2 id="vt-art-rel">{titulo}</h2>'
            f'<ul>{filas}</ul></div></section>')


def tarjeta_indice(t):
    foto = ""
    if t.get("foto"):
        f = t["foto"]
        foto = (f'<img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="{esc(f["alt"])}" loading="lazy" '
                f'decoding="async">')
    minutos = f'<span>{t["minutos"]} min</span>' if t.get("minutos") else ""
    return (f'<li class="vt-blog-t{" vt-blog-t--foto" if foto else ""}">{foto}<div><p class="vt-art__rel-c">{esc(t["categoria"])}</p>'
            f'<h3><a href="{esc(t["href"])}">{t["titulo"]}</a></h3><p>{t["texto"]}</p>{minutos}</div></li>')
VT_EOF
cd tools/site && python3 -c "
from contenido import articulo, blog_clusters as bc
print(len(articulo.CLAVES), sorted(bc.TEMA) == sorted(articulo.CLAVES))
p = articulo.pagina('palma-areca-tampico').CONTENIDO
print(p['autor'], '|', p['actualizado'], '|', [i for i, _t in p['indice']][:3])"
```

Expected: `52 True` y `Equipo técnico de Viveros Terra | 8 de noviembre de 2026 | ['respuesta', 'que-es', 'cuidados']`.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/contenido/blog_clusters.py tools/site/contenido/articulo.py tools/site/contenido/blog_indice.py tools/site/componentes_blog.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(blog): contenido de artículo e índice y temas comerciales" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Hoja `terra-blog.css` y su cableado

**Files:** Create: `public/css/terra-blog.css`, `tools/site/tests/test_terra_blog_css.py`. Modify: `tools/site/{activos,partials,shell}.py`, `vercel.json`, `tools/site/tests/{test_activos,test_partials,test_vercel}.py`

- [ ] **Step 1: Prueba de la hoja y de su cableado (RED)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/tests
cat > tools/site/tests/test_terra_blog_css.py <<'VT_EOF'
"""terra-blog.css: hoja del blog (Etapa 2h). Todo bajo .vt-blog, sin colores literales ni !important y con presupuesto propio
(terra.css ya no tiene margen)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-blog.css"


class TerraBlogCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_blog(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-blog ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 12 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 3 * 1024)


if __name__ == "__main__":
    unittest.main()
VT_EOF
python3 - <<'PY'
from pathlib import Path
def cambia(ruta, viejo, nuevo):
    t = Path(ruta).read_text(encoding='utf-8'); assert viejo in t, viejo; Path(ruta).write_text(t.replace(viejo, nuevo), encoding='utf-8')
cambia('tools/site/tests/test_vercel.py', 'terra-precios|legacy-fixes', 'terra-precios|terra-blog|legacy-fixes')
cambia('tools/site/tests/test_activos.py', '(self.pub / "css" / "terra-precios.css").write_text(".vt-precios .vt-x{}", encoding="utf-8")',
       '(self.pub / "css" / "terra-precios.css").write_text(".vt-precios .vt-x{}", encoding="utf-8")\n        (self.pub / "css" / "terra-blog.css").write_text(".vt-blog .vt-x{}", encoding="utf-8")')
cambia('tools/site/tests/test_activos.py', '"terra-materiales.css", "terra-precios.css"):', '"terra-materiales.css", "terra-precios.css", "terra-blog.css"):')
cambia('tools/site/tests/test_partials.py', '                "terra-precios.css": "/css/terra-precios.g.css",\n', '                "terra-precios.css": "/css/terra-precios.g.css",\n                "terra-blog.css": "/css/terra-blog.g.css",\n')
cambia('tools/site/tests/test_partials.py', '        self.assertNotIn("terra-precios", partials.head(urls, False, materiales=True))\n',
       '        self.assertNotIn("terra-precios", partials.head(urls, False, materiales=True))\n        self.assertIn(\'<link rel="stylesheet" href="/css/terra-blog.g.css">\', partials.head(urls, False, blog=True))\n        self.assertNotIn("terra-blog", partials.head(urls, False, precios=True))\n')
PY
(cd tools/site && python3 -m unittest tests.test_terra_blog_css tests.test_partials 2>&1 | tail -1)
```

Expected: `FAILED` (no existe la hoja ni el argumento `blog`).

- [ ] **Step 2: Hoja y cableado (GREEN)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p public/css
cat > public/css/terra-blog.css <<'VT_EOF'
/* terra-blog.css: artículo e índice del blog (Etapa 2h). Solo se carga en <body class="vt-pagina vt-blog"> (shell.py); todo
   bajo .vt-blog y con los tokens de terra.css. */
.vt-blog .vt-art__cabeza{padding-block:0 8px}
.vt-blog .vt-art__cabeza h1{font-size:clamp(2rem,1.3rem + 3vw,4rem);max-width:20ch;margin:8px 0 0}
.vt-blog .vt-art__dek{max-width:60ch;margin:16px 0 0;font-size:var(--vt-text-lg);color:var(--vt-ink-2)}
.vt-blog .vt-art__meta{display:flex;flex-wrap:wrap;gap:4px 18px;margin:16px 0 0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-blog .vt-art__meta b{color:var(--vt-ink);font-weight:600}
.vt-blog .vt-art{display:grid;gap:32px;padding-block:24px var(--vt-space-section)}
.vt-blog .vt-art__cuerpo{min-width:0;max-width:68ch}
.vt-blog .vt-art__cuerpo h2{font-size:clamp(1.5rem,1.2rem + 1.2vw,2.25rem);line-height:1.15;margin:2.2em 0 .6em}
.vt-blog .vt-art__cuerpo h3{font-size:1.3125rem;line-height:1.25;margin:1.6em 0 .5em}
.vt-blog .vt-art__cuerpo h4{font-size:1.0625rem;margin:1.4em 0 .4em}
.vt-blog .vt-art__cuerpo :is(h2,h3,[id]){scroll-margin-top:calc(var(--vt-head-h) + 16px)}
.vt-blog .vt-art__cuerpo :is(p,li){color:var(--vt-ink-2);line-height:1.65}
.vt-blog .vt-art__cuerpo p{margin:0 0 1em}
.vt-blog .vt-art__cuerpo :is(ul,ol){display:grid;gap:8px;margin:0 0 1.2em;padding-left:1.2em}
.vt-blog .vt-art__cuerpo li::marker{color:var(--vt-soil)}
.vt-blog .vt-art__cuerpo img{display:block;width:100%;height:auto;margin:24px 0;border:1px solid var(--vt-line)}
.vt-blog .vt-art__respuesta{margin:0 0 28px;padding:16px 18px;border:1.5px solid var(--vt-ink);background:var(--vt-card)}
.vt-blog .vt-art__respuesta-t,.vt-blog .vt-art__cuerpo h2.vt-art__respuesta-t{margin:0 0 6px;font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
.vt-blog .vt-art__respuesta p:last-child{margin:0}
.vt-blog .vt-art__nota{margin:20px 0;padding:14px 16px 14px 18px;border-left:3px solid var(--vt-soil);background:var(--vt-card)}
.vt-blog .vt-art__nota::before{content:"Nota de campo";content:"Nota de campo" / "";display:block;margin-bottom:4px;font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-soil)}
.vt-blog .vt-art__nota p{margin:0}
.vt-blog .vt-art__tabla{overflow-x:auto;margin:20px 0}
.vt-blog .vt-art__cuerpo table{width:100%;min-width:30rem;border-collapse:collapse;background:var(--vt-card);font-size:var(--vt-text-sm)}
.vt-blog .vt-art__cuerpo :is(th,td){padding:10px 12px;border:1px solid var(--vt-line);text-align:left;vertical-align:top}
.vt-blog .vt-art__cuerpo thead th{background:var(--vt-bone-2);font-weight:700}
.vt-blog .vt-art__cuerpo blockquote{margin:20px 0;padding-left:18px;border-left:3px solid var(--vt-line-strong);font-family:var(--vt-font-serif);font-style:italic}
.vt-blog .vt-art__sigue{margin-top:32px;padding-top:16px;border-top:1px solid var(--vt-ink)}
.vt-blog .vt-art__sigue b,.vt-blog .vt-art__indice b{display:block;margin-bottom:8px;font-size:var(--vt-text-xs);letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
.vt-blog .vt-art__sigue ul{list-style:none;padding:0}
.vt-blog .vt-art__sigue li::marker{content:""}
.vt-blog .vt-art__indice ol{list-style:none;margin:0;padding:0;font-size:var(--vt-text-sm)}
.vt-blog .vt-art__indice li{border-bottom:1px solid var(--vt-line)}
.vt-blog main .vt-art__indice a{display:grid;grid-template-columns:28px minmax(0,1fr);padding:8px 0;color:var(--vt-ink-2);text-decoration:none}
.vt-blog main .vt-art__indice a:hover{color:var(--vt-field);text-decoration:underline}
.vt-blog .vt-art__indice span{color:var(--vt-muted);font-variant-numeric:tabular-nums}
.vt-blog .vt-art__producto{padding-block:var(--vt-space-section);background:var(--vt-bone-2)}
.vt-blog .vt-art__producto-grid{display:grid;gap:32px;align-items:center}
.vt-blog .vt-art__rel{padding-block:var(--vt-space-section)}
.vt-blog .vt-art__rel ul,.vt-blog .vt-blog-l,.vt-blog .vt-blog-s{display:grid;gap:20px;margin:24px 0 0;padding:0;list-style:none}
.vt-blog .vt-art__rel li{padding-top:12px;border-top:2px solid var(--vt-ink)}
.vt-blog .vt-art__rel h3,.vt-blog .vt-blog-t h3{margin:4px 0 6px;font-size:1.1875rem;line-height:1.25}
.vt-blog .vt-art__rel-c{margin:0;font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-muted)}
.vt-blog .vt-blog-p{padding-block:0 32px}
.vt-blog .vt-blog-p__g{display:grid;gap:24px;align-items:center}
.vt-blog .vt-blog-p img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.vt-blog .vt-blog-p h1{font-size:clamp(2.25rem,1.4rem + 3.4vw,4.5rem);line-height:1;margin:8px 0 12px}
.vt-blog .vt-blog-p h1 span{display:block}
.vt-blog .vt-blog-t{position:relative;border-top:1px solid var(--vt-line);padding-top:12px}
.vt-blog .vt-blog-t img{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;margin-bottom:10px}
.vt-blog .vt-blog-t a::after{content:"";position:absolute;inset:0}
.vt-blog .vt-blog-t p:not(.vt-art__rel-c){margin:0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-blog .vt-blog-t span{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-blog .vt-blog-s a{display:grid;padding:12px 0;border-bottom:1px solid var(--vt-line);text-decoration:none}
.vt-blog .vt-blog-s span{font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-blog .vt-cta{margin-top:16px}
@media (min-width:640px){.vt-blog .vt-art__rel ul,.vt-blog .vt-blog-l,.vt-blog .vt-blog-s{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1024px){
  .vt-blog .vt-art{grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:56px}
  .vt-blog .vt-art__margen{position:sticky;top:calc(var(--vt-head-h) + 20px);align-self:start;max-height:calc(100vh - var(--vt-head-h) - 40px);overflow-y:auto}
  .vt-blog .vt-art__producto-grid{grid-template-columns:7fr 5fr}
  .vt-blog .vt-art__rel ul,.vt-blog .vt-blog-l,.vt-blog .vt-blog-s{grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
  .vt-blog .vt-blog-p__g{grid-template-columns:7fr 5fr}
}
VT_EOF
python3 - <<'PY'
from pathlib import Path
def cambia(ruta, viejo, nuevo):
    t = Path(ruta).read_text(encoding='utf-8'); assert viejo in t, viejo; Path(ruta).write_text(t.replace(viejo, nuevo), encoding='utf-8')
cambia('tools/site/activos.py', '    "terra-precios.css": "css/terra-precios.css",\n', '    "terra-precios.css": "css/terra-precios.css",\n    "terra-blog.css": "css/terra-blog.css",\n')
cambia('tools/site/partials.py', 'materiales=False, precios=False):', 'materiales=False, precios=False, blog=False):')
cambia('tools/site/partials.py', '''        lineas.append(f'<link rel="stylesheet" href="{urls["terra-precios.css"]}">')\n''',
       '''        lineas.append(f'<link rel="stylesheet" href="{urls["terra-precios.css"]}">')\n    if blog:\n        lineas.append(f'<link rel="stylesheet" href="{urls["terra-blog.css"]}">')\n''')
cambia('tools/site/shell.py', '''PRECIOS = '<body class="vt-pagina vt-precios">'\n''', '''PRECIOS = '<body class="vt-pagina vt-precios">'\nBLOG = '<body class="vt-pagina vt-blog">'\n''')
cambia('tools/site/shell.py', 'materiales=MATERIALES in html, precios=PRECIOS in html)', 'materiales=MATERIALES in html, precios=PRECIOS in html, blog=BLOG in html)')
cambia('vercel.json', 'terra-precios|legacy-fixes', 'terra-precios|terra-blog|legacy-fixes')
PY
python3 tools/site/build.py | tail -2
(cd tools/site && python3 -m unittest tests.test_terra_blog_css tests.test_partials tests.test_activos tests.test_vercel 2>&1 | tail -1)
git status --short | grep -v '\.html$'
```

Expected: `shell: 0 de 108`; `OK`; `git status` con `activos.json`, los `.py`, `vercel.json` y las dos hojas nuevas (`terra-blog.css` y su copia con hash).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add public/css/terra-blog.css public/css/terra-blog.*.css tools/site/activos.py tools/site/activos.json tools/site/partials.py tools/site/shell.py vercel.json tools/site/tests/test_terra_blog_css.py tools/site/tests/test_activos.py tools/site/tests/test_partials.py tools/site/tests/test_vercel.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(blog): hoja terra-blog.css con hash e inmutable, como terra-precios" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Plantillas y migración de las 53 páginas

**Files:** Create: `tools/site/plantillas/articulo.py`, `tools/site/plantillas/blog_indice.py`, `tools/site/tests/test_articulo.py`. Modify: `tools/site/generar.py`, `tools/site/tests/test_generar.py`

- [ ] **Step 1: Prueba de la plantilla (RED)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/tests
cat > tools/site/tests/test_articulo.py <<'VT_EOF'
"""Plantilla de artículo (Etapa 2h): orden de la spec, sin marcado viejo, índice que llega a ids reales, una sola etiqueta de
producto y un CTA a una landing."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402
from contenido import articulo, blog_clusters  # noqa: E402

VIEJO = ("/css/tailwind.css", "/css/design-system.css", "fonts.googleapis", "sendWA", "window.open(", "faq-btn", "<style")


def html_de(slug):
    return paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8")


class ArticuloTest(unittest.TestCase):
    def test_un_h1_y_sin_marcado_viejo(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            with self.subTest(slug=slug):
                self.assertEqual(len(re.findall(r"<h1\b", paridad.principal(html))), 1)
                for viejo in VIEJO:
                    self.assertNotIn(viejo, html)

    def test_orden_de_secciones(self):
        html = html_de("palma-areca-tampico")
        orden = ['id="vt-h1"', "vt-art__meta", 'id="respuesta"', 'id="que-es"', 'id="preguntas"', "vt-art__sigue",
                 "vt-art__producto", "vt-art__rel"]
        posiciones = [html.index(s) for s in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_indice_llega_a_ids_del_articulo(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            ids = set(re.findall(r'\sid="([^"]+)"', html))
            indice = re.search(r'<nav class="vt-art__indice".*?</nav>', html, re.S).group(0)
            enlaces = re.findall(r'href="#([^"]+)"', indice)
            with self.subTest(slug=slug):
                self.assertGreater(len(enlaces), 1)
                self.assertEqual([e for e in enlaces if e not in ids], [])

    def test_una_etiqueta_y_cta_a_landing(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            landing = blog_clusters.de(slug)["landing"][0]
            with self.subTest(slug=slug):
                self.assertEqual(html.count('class="vt-etiqueta"'), 1)
                self.assertIn(f'data-cta="blog:landing" href="{landing}"', html)

    def test_dos_o_tres_enlaces_contextuales_a_money_pages(self):
        for slug in articulo.CLAVES:
            enlaces = blog_clusters.de(slug)["enlaces"]
            with self.subTest(slug=slug):
                self.assertIn(len(enlaces), (2, 3))
                self.assertEqual(len({h for _t, h in enlaces}), len(enlaces))

    def test_faqpage_igual_a_lo_visible(self):
        for slug in articulo.CLAVES:
            doc = articulo.pagina(slug).CONTENIDO
            html = html_de(slug)
            with self.subTest(slug=slug):
                self.assertEqual(paridad.principal(html).count("<summary>"), len(doc["faq"]))
                self.assertEqual(html.count('"@type":"Question"'), len(doc["faq"]))

    def test_blogs_de_precios_enlazan_a_precios(self):
        for slug in blog_clusters.A_PRECIOS:
            with self.subTest(slug=slug):
                self.assertTrue(any(h == "/precios" for _t, h in blog_clusters.de(slug)["enlaces"]))

    def test_todo_articulo_tiene_tema(self):
        self.assertEqual(sorted(blog_clusters.TEMA), sorted(articulo.CLAVES))


if __name__ == "__main__":
    unittest.main()
VT_EOF
(cd tools/site && python3 -m unittest tests.test_articulo 2>&1 | tail -1)
```

Expected: `FAILED` (las páginas siguen siendo las viejas).

- [ ] **Step 2: Plantillas y registro (GREEN)**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/plantillas
cat > tools/site/plantillas/articulo.py <<'VT_EOF'
"""Plantilla de artículo del blog (spec §3.3): migas → H1 → autor y fecha → respuesta directa → cuerpo con columna de margen
(índice) y Notas de campo → preguntas → enlaces contextuales → etiqueta de producto relacionado y CTA a una landing →
relacionados. Los 52 artículos: tools/site/contenido/articulo.py."""
import re

import componentes as c
import componentes_blog as cb
from plantillas import base


def render(k):
    faq = f'<h2 id="preguntas">{k["faq_titulo"]}</h2>{c.faq(k["faq"])}' if k["faq"] else ""
    cuerpo = (f'<div class="vt-wrap vt-art"><article class="vt-art__cuerpo" aria-labelledby="vt-h1">{cb.respuesta(k["respuesta"])}'
              f'{k["cuerpo"]}{faq}{cb.enlaces(k["tema"]["enlaces"])}</article>'
              f'<aside class="vt-art__margen">{cb.indice(k["indice"])}</aside></div>')
    grafo = [n for n in k["jsonld"]["@graph"] if n.get("@type") != "FAQPage"]
    if k["faq"]:
        grafo.append(c.faq_jsonld(k["faq"]))
    html = "\n".join((cb.cabeza(k), cuerpo, cb.producto(k["tema"], k["mensaje"], k["tipo"]),
                      cb.relacionados(k["relacionados_titulo"] or "También te puede interesar", k["relacionados"])))
    return base.documento(k["meta"], html, jsonld_bloques=({"@context": "https://schema.org", "@graph": grafo},),
                          precargas=_precarga(k["cuerpo"]), clase_body="vt-pagina vt-blog")


def _precarga(cuerpo):
    m = re.search(r'<img src="([^"]+)"', cuerpo)
    return (base.precarga_imagen({"src": m.group(1)}),) if m else ()
VT_EOF
mkdir -p tools/site/plantillas
cat > tools/site/plantillas/blog_indice.py <<'VT_EOF'
"""Índice del blog: H1 y conteo del build, las mismas secciones y tarjetas de la página publicada y los servicios."""
import componentes as c
import componentes_blog as cb
from partials import esc
from plantillas import base


def render(k):
    f = k["foto"]
    portada = (f'<section class="vt-blog-p" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}<div class="vt-blog-p__g"><div>'
               f'<p class="vt-kicker"><span data-vt-conteo="blog">52</span> guías · {c.datos.AUTOR_BLOG}</p><h1 id="vt-h1">{k["h1"]}</h1>'
               f'<p class="vt-lede">{k["lede"]}</p>{c.fila_cta(k["mensaje"], k["tipo"], "hero", hero=True)}</div>'
               f'<img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="{esc(f["alt"])}" loading="eager" fetchpriority="high" decoding="async">'
               f'</div></div></section>')
    secciones = []
    for n, s in enumerate(k["secciones"], 1):
        tarjetas = "".join(cb.tarjeta_indice(t) for t in s["tarjetas"])
        secciones.append(c.bloque(n, "Blog", f"vt-h-b{n}", s["titulo"], f'<ul class="vt-blog-l">{tarjetas}</ul>', tinte=n % 2 == 0))
    servicios = "".join(f'<li><a href="{esc(h)}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in k["servicios"])
    secciones.append(c.bloque(len(k["secciones"]) + 1, "Servicios", "vt-h-serv", "¿Buscas servicio profesional en Tampico?",
                              f'<ul class="vt-blog-s">{servicios}</ul>' + c.fila_cta(k["mensaje"], k["tipo"], "cierre")))
    return base.documento(k["meta"], portada + "\n".join(secciones), precargas=(base.precarga_imagen({"src": f["src"]}),), jsonld_bloques=(k["jsonld"],),
                          clase_body="vt-pagina vt-blog")
VT_EOF
python3 - <<'PY'
from pathlib import Path
def cambia(ruta, viejo, nuevo):
    t = Path(ruta).read_text(encoding='utf-8'); assert viejo in t, viejo; Path(ruta).write_text(t.replace(viejo, nuevo), encoding='utf-8')
cambia('tools/site/generar.py', '    ("/precios", "precios/index.html", "precios", "precios"),\n', '    ("/precios", "precios/index.html", "precios", "precios"),\n    ("/blog", "blog/index.html", "blog_indice", "blog_indice"),\n')
cambia('tools/site/generar.py', ') + _varias("zona", lambda k: f"/{k}", lambda k: f"{k}/index.html", "zona")',
       ') + _varias("zona", lambda k: f"/{k}", lambda k: f"{k}/index.html", "zona") + _varias(\n    "articulo", lambda k: f"/blog/{k}", lambda k: f"blog/{k}/index.html", "articulo")')
cambia('tools/site/tests/test_generar.py', '"/piedra-bola-rio-tampico", "/precios", "/pasto-sintetico",', '"/piedra-bola-rio-tampico", "/precios", "/blog", "/pasto-sintetico",')
cambia('tools/site/tests/test_generar.py', '                     + [ruta for _nombre, ruta in datos.ZONAS])', '                     + [ruta for _nombre, ruta in datos.ZONAS]\n                     + [f"/blog/{slug}" for slug in articulo.CLAVES])')
cambia('tools/site/tests/test_generar.py', 'import generar  # noqa: E402\n', 'import generar  # noqa: E402\nfrom contenido import articulo  # noqa: E402\n')
PY
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
(cd tools/site && python3 -m unittest tests.test_articulo tests.test_generar 2>&1 | tail -1)
python3 tools/site/paridad.py informe /blog $(ls public/blog | grep -v index.html | sed 's#^#/blog/#') | grep -vc ": ok"
```

Expected: `plantillas: 53 de 101 páginas escritas`, en la segunda `0 de 101` y `shell: 0 de 108`; `OK`; `53` (solo las líneas `== /ruta`).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/plantillas/articulo.py tools/site/plantillas/blog_indice.py tools/site/generar.py tools/site/tests/test_articulo.py tools/site/tests/test_generar.py public/blog
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(blog): plantilla articulo e índice; los 52 artículos dejan el HTML a mano" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Reglas y paridad palabra por palabra

**Files:** Create: `tools/site/tests/test_blog_paridad.py`, `tools/site/tests/test_blog_reglas.py`. Modify: `tools/site/tests/test_anclas.py`, `tools/site/tests/test_contenido.py`, `tools/site/tests/test_navegador.py`, `public/sitemap.xml`

- [ ] **Step 1: Escribir las pruebas**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/tests
cat > tools/site/tests/test_blog_paridad.py <<'VT_EOF'
"""Paridad de los 52 artículos del blog (Etapa 2h): el texto es el publicado, palabra por palabra, salvo las correcciones
documentadas en contenido/blog_correcciones.py; las fotos son las mismas y en el mismo orden."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402
import paridad_blog  # noqa: E402
import paridad_materiales  # noqa: E402
from contenido import articulo, blog_correcciones as bc  # noqa: E402


def html_de(slug):
    return paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8")


def permitido_borrar(doc):
    partes = list(doc["retirado"]) + [doc["kicker"], doc["h1"], doc["dek"], doc["relacionados_titulo"]]
    partes += [" ".join((r["categoria"], r["titulo"], r["texto"])) for r in doc["relacionados"]]
    return paridad.texto(" ".join(partes))


class BlogParidadTest(unittest.TestCase):
    def test_son_52_articulos(self):
        self.assertEqual(len(articulo.CLAVES), 52)
        self.assertEqual(len(articulo.CLAVES), len(list(paridad_blog.DIR_TEXTO.glob("*.txt"))))

    def test_nada_se_agrega_al_texto_del_articulo(self):
        for slug in articulo.CLAVES:
            viejo = paridad_blog.viejo_corregido(slug, bc.de(slug) + bc.TODOS)
            insertado, _borrado = paridad_blog.diferencias(viejo, paridad_blog.cuerpo_nuevo(html_de(slug)))
            with self.subTest(slug=slug):
                self.assertEqual(insertado, [])

    def test_lo_que_se_borra_es_la_envoltura(self):
        """Solo salen el índice, los CTA y la barra lateral anteriores (anotados por la extracción) y la portada, que la
        plantilla vuelve a poner."""
        for slug in articulo.CLAVES:
            doc, _cuerpo = articulo.leer(slug)
            viejo = paridad_blog.viejo_corregido(slug, bc.de(slug) + bc.TODOS)
            _ins, borrado = paridad_blog.diferencias(viejo, paridad_blog.cuerpo_nuevo(html_de(slug)))
            permitido = " ".join(paridad.texto(" ".join(doc["retirado"])).split() + permitido_borrar(doc).split())
            ajenos = [b for b in borrado if not all(p in permitido for p in b.split())]
            with self.subTest(slug=slug):
                self.assertEqual(ajenos, [])

    def test_mismas_fotos_en_el_mismo_orden(self):
        captura = json.loads(paridad_blog.FOTOS.read_text(encoding="utf-8"))
        for ruta, viejas in captura.items():
            nuevas = paridad_materiales.fotos(paridad.archivo(ruta).read_text(encoding="utf-8"))
            with self.subTest(ruta=ruta):
                self.assertEqual([re.sub(r"^(\.\./)+", "/", f["src"]) for f in viejas], [f["src"] for f in nuevas])

    def test_cada_correccion_tiene_motivo(self):
        for slug, lista in bc.CORRECCIONES.items():
            for viejo, _nuevo, motivo in lista:
                with self.subTest(slug=slug, viejo=viejo[:40]):
                    self.assertGreater(len(motivo), 20)


if __name__ == "__main__":
    unittest.main()
VT_EOF
mkdir -p tools/site/tests
cat > tools/site/tests/test_blog_reglas.py <<'VT_EOF'
"""Reglas del dueño en el blog (Etapa 2h): precios solo de datos.py o calculados con ellos, especies sin precio confirmado
"según cotización", sin "más vendido", sin "gratis" ni "sin costo" (salvo la garantía de pasto aprobada), sin estadísticas sin
fuente, sin SENASICA, "Oasis" ni proveedor de la terminal, autor editorial, mismo autor visible y la visita siempre con su costo."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402
from contenido import articulo  # noqa: E402

PERMITIDOS = ({dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))}
              | {dinero(m[k]) for m in data.MODELOS for k in ("t1", "t2", "rollo")})
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
_RIEGO = {dinero(a * m2) for a in datos.PRECIOS["riego_m2"] for m2 in (30, 50, 60, 80, 100, 120, 150, 200, 250, 500)}
_PRESUPUESTO = {"$5", "$15", "$20", "$50", "$120", "$200"}  # "$5K, $20K, $50K": el presupuesto del lector, no un precio
# Lo que no es un precio de Viveros Terra (presupuesto del lector, cuenta del ejemplo, tarifa de agua, artículo de ferretería)
# o es una multiplicación de un precio oficial. Cada entrada se revisó a mano; la lista solo puede encoger.
CALCULADOS = {
    "": _PRESUPUESTO,  # el índice: "$5K, $20K o $50K"
    "cesped-amarillo-tampico-causas-soluciones": {"$50", "$150"},
    "cuanto-cuesta-jardin-tampico-precios": {"$2,550", "$4,250", "$5,000", "$6,000", "$10,200", "$15,000", "$21,250", "$45,000",
                                             "$50,000", "$80,000", "$200,000", "$3"} | _RIEGO,
    "cuanto-cuesta-pasto-sintetico-mexico": {"$157", "$162", "$167", "$900", "$1,150", "$1,400", "$2,800", "$4,225", "$5,125",
                                             "$9,950", "$11,100", "$29,900", "$32,700"},
    "framboyan-delonix-regia-tampico": _PRESUPUESTO,
    "jardin-bajo-presupuesto-tampico": _PRESUPUESTO | {"$2,250", "$2,975", "$4,500", "$5,000", "$7,650", "$10,500", "$13,600",
                                                        "$15,000", "$20,000", "$25,000", "$35,000", "$50,000"},
    "jardin-vertical-tampico-guia": _PRESUPUESTO,
    "pasto-sintetico-vs-natural-tampico": {"$0", "$1,200", "$2,400", "$4,000", "$4,800", "$6,000", "$9,600", "$19,250", "$32,500",
                                           "$94,000", "$182,000"},
    "riego-automatico-tampico-roi": _RIEGO | {"$0", "$50", "$600", "$900", "$1,100", "$2,000", "$4,500", "$6,000", "$7,200",
                                              "$10,800", "$14,400", "$19,200", "$21,600", "$25,600", "$36,000", "$38,400", "$64,000",
                                              "$160,000"},
    "sistema-riego-automatico-conviene-tampico": _RIEGO | {"$300", "$600", "$800", "$1,200", "$6,000", "$27,000", "$32,000",
                                                           "$36,000", "$48,000", "$64,000"},
    "sistema-riego-automatizado-tampico": _RIEGO | {"$9,000", "$16,000", "$25,600", "$48,000"},
    "tierra-negra-costal-camion-tampico": {"$450", "$900", "$1,350", "$1,800", "$2,160", "$2,250", "$3,330", "$4,500", "$6,660",
                                           "$13,500"},
}
ESPECIE_SIN_PRECIO_RE = re.compile(
    r"(?:washington|kerpis|viajero|cycas|bamb[uú]|bismarckia|cola de zorro|triangular|ficus|trueno|neem|tabach[ií]n|laurel|tulip[aá]n)"
    r"(?:(?!seg[uú]n cotizaci[oó]n)[^.<]){0,50}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("más vendido", r"m[aá]s vendid[ao]s?"),
    ("gratis", r"\bgratis\b|\bgratuit\w*"),
    ("sin costo", r"\bsin costo\b(?! ?, siguiendo)|\bsin cargo\b"),
    ("certificación", r"\bSENASICA\b"),
    ("marca", r"\bOasis\b"),
    ("terminal", r"\bClip\b"),
    ("porcentaje sin fuente", r"el \d{2}% de (?:los|las) (?:problemas|plantas|casos|jardines)|arraiga el \d{2}%"),
    ("cifra de ahorro", r"(?:hasta|entre)[^.]{0,20}(?:50|60)\s?%[^.]{0,40}agua"),
    ("caso sin verificar", r"Ejemplo real|ejemplos? reales|casos? reales|Cliente típico|[Cc]lientes de Viveros Terra"),
    ("en nuestro vivero", r"en nuestro vivero"),
    ("pago en parcialidades", r"parcialidades"),
)
CON_VISITA = ("cesped-amarillo-tampico-causas-soluciones", "cuanto-cuesta-jardin-tampico-precios",
              "sistema-riego-automatizado-tampico")


def publico(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    titulo = " ".join(re.findall(r"<title>(.*?)</title>", html))
    return " ".join((paridad.texto(paridad.principal(html)), ld, metas, titulo))


class BlogReglasTest(unittest.TestCase):
    def rutas(self):
        return [ruta for ruta, _a, _p, _c in generar.PAGINAS if ruta.startswith("/blog")]

    def test_precios_oficiales_o_calculados(self):
        for ruta in self.rutas():
            slug = ruta.removeprefix("/blog").strip("/")
            texto = publico(paridad.archivo(ruta).read_text(encoding="utf-8"))
            sobra = {p.replace(" ", "") for p in PRECIO_RE.findall(texto)} - PERMITIDOS - CALCULADOS.get(slug, set())
            with self.subTest(ruta=ruta):
                self.assertEqual(sorted(sobra), [])

    def test_especies_sin_precio_confirmado(self):
        for ruta in self.rutas():
            with self.subTest(ruta=ruta):
                texto = paridad.texto(paridad.principal(paridad.archivo(ruta).read_text(encoding="utf-8")))
                self.assertIsNone(ESPECIE_SIN_PRECIO_RE.search(texto))

    def test_sin_afirmaciones_prohibidas(self):
        for ruta in self.rutas():
            texto = publico(paridad.archivo(ruta).read_text(encoding="utf-8"))
            for nombre, patron in SIN_VERIFICAR:
                with self.subTest(ruta=ruta, regla=nombre):
                    self.assertIsNone(re.search(patron, texto, re.I), nombre)

    def test_autor_editorial_en_cada_articulo(self):
        for slug in articulo.CLAVES:
            with self.subTest(slug=slug):
                self.assertIn(f"<b>Por</b> {datos.AUTOR_BLOG}", paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8"))

    def test_la_visita_lleva_su_costo(self):
        for slug in CON_VISITA:
            with self.subTest(slug=slug):
                self.assertIn(datos.VISITA_COSTO, paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
VT_EOF
python3 - <<'PY'
from pathlib import Path
p = Path('tools/site/tests/test_anclas.py'); s = p.read_text(encoding='utf-8')
a = s.index('PENDIENTES = frozenset('); b = s.index('def rotas(')
s = s[:a] + '\n\n' + s[b:]
s = s.replace('{k: v for k, v in rotas().items() if k not in PENDIENTES}', 'rotas()')
a = s.index('    def test_pendientes_siguen_rotas'); b = s.index('if __name__')
s = s[:a].rstrip() + '\n\n\n' + s[b:]
s = s.replace('PENDIENTES son los\níndices de tres artículos del blog que ya estaban rotos en main; los arregla la Etapa 2h y la lista solo puede encoger."""', 'Desde la Etapa 2h el índice de cada\nartículo se arma de los <h2> de su cuerpo: no puede apuntar a un id que no existe."""')
p.write_text(s, encoding='utf-8')
p = Path('tools/site/tests/test_contenido.py'); s = p.read_text(encoding='utf-8')
viejo = 'if k not in ("meta", "jsonld")}'; assert viejo in s
p.write_text(s.replace(viejo, 'if k not in ("meta", "jsonld", "cuerpo")}'), encoding='utf-8')
p = Path('tools/site/tests/test_navegador.py'); s = p.read_text(encoding='utf-8')
a = s.index('    def test_window_open_de_whatsapp_sale_firmado'); b = s.index('    def test_cotizador_de_la_tienda_manda_el_lead')
p.write_text(s[:a] + s[b:], encoding='utf-8')
PY
(cd tools/site && python3 -m unittest tests.test_blog_paridad tests.test_blog_reglas tests.test_anclas tests.test_contenido tests.test_paridad tests.test_reglas tests.test_consistencia tests.test_enlaces 2>&1 | tail -1)
```

Expected: `OK`. Para comprobar que las pruebas muerden: quita una tripleta de `blog_correcciones.py`, vuelve a extraer y corre `test_blog_reglas`: debe fallar; restáurala y vuelve a extraer.

- [ ] **Step 2: `lastmod` del índice y de los 30 artículos corregidos**

```bash
cd ~/dev/viverosterra-e2h
python3 - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, 'tools/site')
from contenido import blog_correcciones as bc
p = Path('public/sitemap.xml'); s = p.read_text(encoding='utf-8')
for slug in ['/blog'] + [f'/blog/{k}' for k in bc.CORRECCIONES if bc.de(k) and k != '/blog']:
    s, n = re.subn(rf'(<loc>https://www\.viverosterra\.com{re.escape(slug)}/?</loc>\s*<lastmod>)[^<]+', r'\g<1>2026-11-08', s)
    assert n == 1, slug
p.write_text(s, encoding='utf-8')
PY
python3 tools/site/build.py | tail -2
git diff --stat public/sitemap.xml | tail -1
```

Expected: `0 de 101`, `0 de 108`; `1 file changed, 31 insertions(+), 31 deletions(-)` (si el build de `tools/pasto` lo revierte, corre este paso al final y anótalo en el PR).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/tests/test_blog_paridad.py tools/site/tests/test_blog_reglas.py tools/site/tests/test_anclas.py tools/site/tests/test_contenido.py tools/site/tests/test_navegador.py public/sitemap.xml
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(blog): paridad palabra por palabra, reglas del dueño y anclas sin pendientes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Pruebas en navegador y capturas

**Files:** Create: `tools/site/tests/test_blog_navegador.py`. Modify: `tools/site/capturas.py`

- [ ] **Step 1: Escribir la prueba**

```bash
cd ~/dev/viverosterra-e2h
mkdir -p tools/site/tests
cat > tools/site/tests/test_blog_navegador.py <<'VT_EOF'
"""El blog en un navegador real (Etapa 2h): sin desbordar, consola limpia, preguntas con <details>, índice que lleva a su título y
WhatsApp firmado."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
from contenido import articulo  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

MUESTRA = ("palma-areca-tampico", "cuanto-cuesta-jardin-tampico-precios", "jardines-temporada-lluvias-tampico",
           "cuando-regar-pasto-san-agustin-tampico")


@unittest.skipIf(sync_playwright is None, "sin playwright")
class BlogNavegadorTest(unittest.TestCase):
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

    def test_sin_desbordar_a_320_375_y_768(self):
        anchas = []
        for ancho in (320, 375, 768):
            pagina = self.nav.new_page(viewport={"width": ancho, "height": 800})
            for slug in articulo.CLAVES:
                pagina.goto(f"{self.base}/blog/{slug}/", wait_until="load")
                sobra = pagina.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if sobra > 1:
                    anchas.append(f"{slug}@{ancho}: {sobra}px")
            pagina.close()
        self.assertEqual(anchas, [])

    def test_consola_limpia_en_el_indice_y_la_muestra(self):
        errores = []
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.on("console", lambda m: errores.append(m.text) if m.type == "error" and "googletagmanager" not in m.text else None)
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        for ruta in ("/blog/",) + tuple(f"/blog/{s}/" for s in MUESTRA):
            pagina.goto(self.base + ruta, wait_until="load")
        pagina.close()
        self.assertEqual(errores, [])

    def test_indice_lleva_al_titulo_y_preguntas_abren(self):
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.goto(f"{self.base}/blog/palma-areca-tampico/", wait_until="load")
        pagina.locator('.vt-art__indice a[href="#cuidados"]').click()
        pagina.wait_for_function("() => location.hash === '#cuidados'")
        top = pagina.evaluate("() => document.getElementById('cuidados').getBoundingClientRect().top")
        self.assertGreaterEqual(top, 60)
        segunda = pagina.locator(".vt-faq details").nth(1)
        segunda.locator("summary").click()
        self.assertEqual(segunda.get_attribute("open"), "")
        pagina.close()

    def test_whatsapp_del_cierre_firmado_y_con_el_mensaje_del_articulo(self):
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.goto(f"{self.base}/blog/palma-areca-tampico/", wait_until="load")
        href = pagina.locator('[data-cta="blog:cierre"]').first.get_attribute("href")
        self.assertIn("viverosterra.com", href)
        self.assertIn("Palma%20Areca", href)
        pagina.close()


if __name__ == "__main__":
    unittest.main()
VT_EOF
(cd tools/site && python3 -m unittest tests.test_blog_navegador 2>&1 | tail -1)
```

Expected: `OK`. Si un artículo desborda, la causa casi siempre es una tabla: corrige `terra-blog.css` (la tabla va dentro de `.vt-art__tabla`, con su propio desplazamiento), no el contenido.

- [ ] **Step 2: Agregar a `capturas.py` un artículo por envoltura**

```bash
cd ~/dev/viverosterra-e2h
python3 - <<'PY'
from pathlib import Path
p = Path('tools/site/capturas.py'); s = p.read_text(encoding='utf-8')
viejo = '"/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/")'; assert viejo in s
p.write_text(s.replace(viejo, '"/blog/cuando-regar-pasto-san-agustin-tampico/", "/blog/palma-areca-tampico/",\n           "/blog/cuanto-cuesta-jardin-tampico-precios/", "/blog/jardines-temporada-lluvias-tampico/", "/precios/")'), encoding='utf-8')
PY
```

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2h
git add tools/site/tests/test_blog_navegador.py tools/site/capturas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(blog): navegador de artículos e índice, y capturas por envoltura" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Limpieza de lo que quedó huérfano

**Files:** Modify: ninguno salvo que algo aparezca.

- [ ] **Step 1: Confirmar que nada del blog depende del CSS viejo**

```bash
cd ~/dev/viverosterra-e2h
grep -lE "tailwind\.css|design-system\.css|legacy-fixes|fonts\.googleapis|sendWA" public/blog/*/index.html public/blog/index.html | wc -l
grep -rl "sendWA" public --include='*.html' --include='*.js' | grep -v tests | wc -l
(cd tools/site && python3 -m unittest tests.test_legacy_fixes tests.test_huerfanos tests.test_limpieza 2>&1 | tail -1)
```

Expected: `0`; `0`; `OK`. `tailwind.css`, `design-system.css` y `legacy-fixes.css` no se borran aquí: los usan las utilitarias hasta 2i.

---

### Task 10: Verificación final y puertas de revisión (merge y push los hace el controlador)

- [ ] **Step 1: Suites completas**

```bash
cd ~/dev/viverosterra-e2h
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
(cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3)
(cd tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK")
(cd tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK")
node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `0 de 101` y `0 de 108`; `0`; `OK` (655 en el prototipo); `OK`; `OK`; `ℹ fail 0`.

- [ ] **Step 2: Lighthouse móvil**

```bash
cd ~/dev/viverosterra-e2h
(cd public && python3 -m http.server 8771 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in blog blog/palma-areca-tampico blog/cuanto-cuesta-jardin-tampico-precios blog/jardines-temporada-lluvias-tampico blog/cuando-regar-pasto-san-agustin-tampico; do
  f=/tmp/vt-e2h-lh-$(echo $r | tr '/' '_').json
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8771/$r/" --form-factor=mobile --only-categories=performance,accessibility --chrome-flags="--headless=new" --output=json --output-path="$f" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "$f"
done
pkill -f "http.server 8771"
```

Expected por página: Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s. CLS ≥ 0.1 o A11y < 95 bloquean: corrige con prueba. Las fotos no se recomprimen (regla del dueño): si el LCP pasa de 2.5 s por una foto, anota valor y causa.

- [ ] **Step 3: axe y capturas a 320, 375, 768, 1024, 1440 y 1920**

```bash
cd ~/dev/viverosterra-e2h/tools/site
python3 - <<'PY'
import sys
sys.path.insert(0, '.')
import servidor
from playwright.sync_api import sync_playwright
base, srv = servidor.iniciar()
rutas = ('blog/', 'blog/palma-areca-tampico/', 'blog/cuanto-cuesta-jardin-tampico-precios/', 'blog/jardines-temporada-lluvias-tampico/')
AXE = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for r in rutas:
        for w in (320, 375, 768, 1024, 1440, 1920):
            p = b.new_page(viewport={'width': w, 'height': 812 if w == 375 else 900})
            p.goto(f'{base}/{r}', wait_until='load')
            assert p.evaluate('() => innerWidth') == w
            p.screenshot(path=f"/tmp/vt-e2h-{r.strip('/').replace('/', '_')}-{w}.png", full_page=True)
            if w == 1440:
                p.add_script_tag(url=AXE)
                v = p.evaluate("async () => (await axe.run()).violations.filter(x => ['serious','critical'].includes(x.impact)).map(x => x.id)")
                print(r, v)
            p.close()
    b.close()
srv.shutdown()
PY
```

Expected: `[]` en las cuatro páginas; capturas en `/tmp/vt-e2h-*.png`. Revisa a mano: jerarquía de la portada del artículo sin foto (32 posts arrancan en texto); caja de respuesta; tablas largas a 320 (desplazamiento propio, no de página); Nota de campo dentro del texto; índice fijo que no tape el pie a 1024; etiqueta de "Según cotización" sin parecer un error; índice del blog con sus 37 fotos en orden.

- [ ] **Step 4: Puertas de revisión en paralelo (spec §11; las lanza el controlador)**

El ejecutor entrega la rama en verde y un resumen (`git log --oneline main..feat/etapa-2h`, Lighthouse, capturas). El controlador lanza los cuatro revisores a la vez con `git diff main...feat/etapa-2h --stat`, `plantillas/{articulo,blog_indice}.py`, `componentes_blog.py`, `contenido/{articulo,blog_clusters,blog_correcciones}.py`, `extraer_blog.py`, `terra-blog.css`, la vista previa de Vercel, `/tmp/vt-e2h-*.png`, los JSON de Lighthouse, `paridad.py informe /blog` y el spec (§3.3, §5, §6.5, §7, §8, §10, §11). Cada hallazgo: crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad a `docs/diseno/hibrido/articulo.html`; lectura en celular (68 ch, jerarquía h2/h3); artículos sin foto; foco visible en índice, FAQ y tarjetas; contraste de `.vt-art__rel-c` y del índice; tablas con `tabindex` y `aria-label`.
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): meta intacta salvo lo documentado; un H1; `BreadcrumbList` = migas; `FAQPage` = lo visible; `Article` y `HowTo` válidos; `dateModified` solo donde cambió el texto; índice del artículo como anclas reales; enlaces contextuales (anclas variadas, sin bloque repetido); que nada adelante la Etapa 3 (301, fusiones) ni la 4 (grafo único).
3. **CRO** (`general-purpose` con `page-cro`): CTA a landing y WhatsApp con el mensaje del artículo; etiqueta visible sin competir con la lectura; camino claro desde "Según cotización"; barra móvil.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): barrido completo (cada tripleta contra `datos.py` y contra el texto publicado); `CALCULADOS`; fotos en orden; paridad y sus motivos; nada de texto inventado en el cuerpo; autor; consola limpia; sin `.DS_Store`.

El ejecutor corrige en la rama todo crítico o alto (prueba, commit, Step 1 otra vez) y el controlador vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan para el PR.

- [ ] **Step 5: Aprobación del dueño (controlador)**

Comparte la vista previa de Vercel, las capturas y la tabla del barrido, y pide en el mismo mensaje las respuestas de "Preguntas al dueño". Sin su "sí" explícito no hay merge. Toda respuesta que cambie un dato va a `datos.py` o a `blog_correcciones.py`, seguida de una nueva extracción y de `test_blog_reglas`.

- [ ] **Step 6: Merge, push y despliegue (solo el controlador)**

Si el lote 5 se publica junto (2g + 2h + 2i), este paso espera a 2i; si el dueño la quiere antes, se publica sola:

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2h -m "merge: etapa 2h — blog con plantilla articulo, 52 artículos con paridad y barrido de afirmaciones" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 101`, `shell: 0 de 108`, `0`; Vercel despliega `main`.

- [ ] **Step 7: Verificación en vivo (controlador)**

```bash
W=https://www.viverosterra.com
for r in blog blog/palma-areca-tampico blog/cuanto-cuesta-jardin-tampico-precios blog/palmas-mas-vendidas-tampico-precios blog/framboyan-delonix-regia-tampico; do
  printf "%s " $r; curl -s $W/$r | grep -cE "tailwind\.css|fonts\.googleapis|sendWA|más vendid|gratis"
done
curl -s $W/blog | grep -o '/css/terra-blog\.[0-9a-f]*\.css' | head -1 | xargs -I{} curl -s -o /dev/null -w "%{http_code}\n" $W{}
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" $W/blog-vivero-tampico
```

Expected: `0` en las 5; `200`; `308 https://www.viverosterra.com/blog` (los redirects siguen). En Chrome (escritorio y iPhone): consola limpia; el WhatsApp del cierre abre el mensaje del artículo con la firma; GA4 DebugView: `generate_lead` con `blog:cierre` y clic en `blog:landing`.

- [ ] **Step 8: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 9: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2h && git branch -d feat/etapa-2h
```

---

## Lotes de ejecución sugeridos

| Lote | Tareas | Qué deja | Revisión intermedia |
|---|---|---|---|
| A · Capturas y extractor (sin cambiar el sitio) | 0–2 | Línea base, texto y fotos congelados, extractor con prueba | Cumplimiento: que las capturas sean de `db6923e` y el extractor no pierda bloques |
| B · Contenido | 3–4 | Los 53 archivos extraídos, las 212 correcciones, temas | **Dueño/cumplimiento: tabla del barrido** antes de construir páginas |
| C · Páginas | 5–7 | Hoja, plantillas, 53 páginas migradas, reglas y paridad en verde | Paridad, `test_blog_reglas`, build reproducible |
| D · Cierre | 8–10 | Navegador, Lighthouse, capturas, 4 puertas, aprobación del dueño, merge | Las 4 puertas del spec §11 |

## Correcciones a la hoja de ruta

- **"53 artículos":** son **52 artículos y el índice** (53 páginas). `shell.conteo_blog` y el índice ya dicen 52; "53 guías" solo está en la maqueta del diseño.
- **Anclas rotas:** el encargo decía 5 posts; `test_anclas` encuentra **3 posts y 14 anclas** en `<a>`. Los otros son referencias `<use href="#ic-…">` a símbolos inexistentes (`ic-bolt` en 6 posts, `ic-leaf` en 1): no son enlaces, y también desaparecen.
- **"Diff de texto vacío":** vacío **salvo las correcciones documentadas**, que el dueño ordenó para que nada contradiga los datos oficiales.
- **Notas de campo en la columna de margen:** se quedan en su lugar dentro del cuerpo (mover 55 avisos cambia el orden de lectura); el margen lleva el índice.
- **"Fechas faltantes en 8 posts":** los 52 tienen `datePublished`; a 8 les falta `dateModified` y 12 no mostraban fecha. La plantilla muestra una fecha en los 52.
- **`datos.VIGENCIA_PRECIOS_ISO`:** el plan 2g lo mencionaba pero no quedó en `main`; aquí la fecha es la constante `extraer_blog.FECHA_CORRECCION`.
- **Precios de 2g:** el plan de 2h no retoma "según cotización" para tierra preparada, camión ni mármol: `datos.py` ya los tiene confirmados (2026-11-08).

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El extractor pierde o duplica texto en alguna de las 3 envolturas | `test_blog_paridad` palabra por palabra en los 52; lo no reconocido se conserva; lo retirado queda en `retirado` y se valida. |
| Una corrección deja de aplicar en silencio | `corregir` detiene la extracción si no encuentra su texto. |
| Se reintroduce un precio sin confirmar | `test_blog_reglas`: conjunto cerrado y patrón por especie. |
| Una actualización masiva de fechas parece manipulación | `dateModified` solo en los 30 artículos cuyo texto cambió. |
| Regenerar FAQPage cambia lo que ven los buscadores | Es lo visible (requisito de Google); 74 diferencias de texto eran un defecto. La puerta SEO lo revisa. |
| Quitar "más vendidas" del H1 de `palmas-mas-vendidas…` baja su posición | La URL no cambia; el dueño puede confirmar el dato (pregunta 2) y volver el título con una línea. |
| Artículos sin foto se ven pobres | Regla del dueño; la portada se apoya en tipografía y respuesta directa. La sesión de fotos es del dueño. |
| Tabla ancha desborda a 320 | `.vt-art__tabla` con desplazamiento propio y `test_blog_navegador`. |
| Se borra un `id` enlazado desde fuera | Los `id` existentes se conservan; los `<h2>` sin `id` lo ganan; `test_anclas` revisa todo el sitio. |
| Volver a extraer borra una edición a mano | Regla en "Reglas para quien ejecuta": tras la Tarea 6, o se edita el archivo o se corrige y extrae, nunca ambos. |

## Preguntas al dueño

1. **Autor:** todos los artículos dirán "Por Equipo técnico de Viveros Terra", el nombre editorial que ya usa el sitio desde la Etapa 1. ¿Lo dejamos así o prefieres un nombre inventado de persona? (Recomendamos dejarlo: suena igual de editorial y no finge ser alguien.)
2. **"Más vendida":** ¿tienes datos de venta que confirmen que la Palma Washingtona y el Toscana 28 son los más vendidos? Sin confirmación, el título "Las 8 palmas más vendidas en Tampico" pasa a "8 palmas para jardines en Tampico" (la URL no cambia) y se quitan 17 menciones.
3. **Precios de palmas:** quedan "según cotización" Washingtona, Kerpis y Palma del Viajero (decían $500), Cycas ($700), Bambú ($1,000) y las matas o ejemplares grandes de areca ($800), coco ($1,800), real ($1,400). ¿Confirmas alguno?
4. **Precios de árboles:** la tabla del artículo de flamboyán tenía Ficus $200, Trueno $300, Neem $300, Tabachín $350, Laurel $500 y Tulipán $600. Pasan a "según cotización". ¿Confirmas alguno?
5. **Paquetes $5K / $20K / $50K:** se conservan como guía de presupuesto, con lo no confirmado "según cotización". ¿Es real que el Proyecto completo incluye el primer mes de mantenimiento con 2 visitas? (`cuanto-cuesta-jardin-tampico-precios`, `jardin-bajo-presupuesto-tampico`.)
6. **Riego:** todos los rangos se recalcularon con $180–$320/m². Controlador WiFi, sensor de lluvia, bomba y revisión preventiva quedan "según cotización". ¿Te parece, o hay precios para esos extras?
7. **Ejemplos de ahorro:** ¿dejamos la cuenta con tarifa de $50/m³ de agua (`riego-automatico-tampico-roi`) como ejemplo, y los kits de ferretería que menciona `cesped-amarillo-tampico-causas-soluciones`?
8. **Pago:** se quitó "acepta pago en parcialidades para proyectos mayores a $30,000" y se dice: anticipo, avances de obra y mensualidades con tarjeta de crédito. ¿Correcto?
9. **Existencias concretas:** "Tenemos palma del viajero en tres tamaños", "Tenemos ficus elastica en varios tamaños" y "ejemplares de Washingtona de 3–5 metros bajo consulta" se quedan. ¿Son ciertas, o las quitamos?
10. **Costal de tierra:** se quitó el peso (25–30 kg) porque no lo tienes, y se conserva el volumen de 25–30 litros y la fórmula del artículo. ¿Es correcto ese volumen?
11. **Garantía del sintético:** se cambia "5 a 8 años" por "3 a 8 años según modelo" (el Aruba 10 tiene de 3 a 5). ¿Correcto?
12. **Fecha:** los 30 artículos corregidos mostrarán "Actualizado el 8 de noviembre de 2026". ¿De acuerdo?
13. **"Más de 200 árboles de banqueta":** se retiró del artículo de banquetas por no estar confirmada. ¿La confirmas?
