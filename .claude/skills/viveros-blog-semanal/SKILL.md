---
name: viveros-blog-semanal
description: Automatización semanal del blog de Viveros Terra (viverosterra.com/blog) — genera 2 artículos nuevos por semana (1 general de horticultura + 1 de planta específica), evita duplicar temas ya publicados o en PRs pendientes, sigue el patrón visual/SEO/AEO/schema del blog existente, publica y verifica en producción. Usar SIEMPRE que la tarea sea "blog semanal", "artículos de blog", "contenido del blog de Viveros Terra", o la tarea programada de automatización de blog.
---

# Blog semanal de Viveros Terra

Automatiza la creación de 2 artículos de blog por semana para viverosterra.com. Este skill existe porque varias corridas seguidas (semanas del 20-jul, 27-jul y 3-ago 2026) escribieron temas duplicados entre sí (Palma Areca dos veces, plagas de jardín dos veces) porque cada corrida solo revisaba el historial de `main` y no las ramas/PRs pendientes de semanas anteriores que nadie había mergeado. **El paso 1 de este workflow existe para que eso no vuelva a pasar.**

## Paso 1 — Inventario de temas ya cubiertos (OBLIGATORIO, antes de elegir tema)

No elijas ningún tema sin completar esto primero:

1. `ls public/blog/` en la rama base (`main`) → lista de slugs ya publicados.
2. `mcp__github__list_pull_requests` con `state: "open"` (con la publicación automática no debería haber PRs de blog pendientes; si hay, publícalos primero portándolos al flujo actual) → **todos** los PRs abiertos, no solo los de blog.
3. Para cada PR abierto, `git fetch origin <rama>` y `git diff --name-status main origin/<rama> -- public/blog` para ver qué slugs propone.
4. Construye una lista única de "temas prohibidos esta semana" = slugs publicados + slugs en cualquier PR abierto (aunque esté en draft, aunque lleve semanas sin revisión — mientras esté abierto, cuenta).
5. Si un PR abierto lleva más de ~2 semanas sin actividad y duplica el tema de otro PR abierto, ciérralo como duplicado (con comentario explicando por qué) antes de continuar — no dejes que el backlog de duplicados siga creciendo semana tras semana.

## Paso 2 — Selección de temas

- **1 artículo general de horticultura**: estacional/evergreen, relevante al clima de Tampico/Tamaulipas (calor, humedad, temporada de lluvias jun-oct, temporada de huracanes jun-nov, temporada seca nov-abr). Valida con WebSearch que el tema tiene intención de búsqueda real.
- **1 artículo de planta/palma específica**: prioriza especies que YA están en el catálogo de Viveros Terra (`public/catalogo.html`) y mencionadas en `public/blog/palmas-mas-vendidas-tampico-precios/index.html` pero que no tienen su propia página de profundidad — mismo patrón que Palma Real, Palma del Viajero, Palma Areca, Palma Washingtona.
- **Precios: nunca inventes cifras.** Usa únicamente precios que ya existen publicados en el sitio (p. ej. la tabla de `palmas-mas-vendidas-tampico-precios`) o en el catálogo. Si no hay precio publicado para la especie elegida, no incluyas un precio específico — usa "cotiza por WhatsApp" en su lugar.

## Paso 3 — Escritura (flujo del generador `tools/site`)

El sitio se genera: **no edites `public/` a mano.** Cada artículo es un archivo `tools/site/contenido/blog/<slug>.html` con un comentario `<!--vt:meta {JSON} -->` (meta, jsonld con `Article` + `FAQPage` + `BreadcrumbList`, kicker, h1, dek, minutos, respuesta directa, 5 preguntas frecuentes, 3 relacionados reales) y debajo el cuerpo en HTML (`<h2 id=…>`, `<h3>`, `<p>`, `<ul>`, tablas `vt-art__tabla`, notas `vt-art__nota--tip`, una `<img>` al inicio con width/height). Copia la estructura de un artículo reciente (p. ej. `palma-rubelina-phoenix-roebelenii-tampico.html` para plantas, `plantas-de-sombra-jardin-tampico.html` para temas generales). Los botones de WhatsApp entre secciones, la etiqueta de producto y el CTA los pone la plantilla: no los escribas.

Reglas que las pruebas exigen: título ≤ 60 caracteres, descripción de 70 a 155; solo precios oficiales (`datos.PRECIOS`, `datos.NOCHEBUENAS`, catálogo) o "según cotización"; sin "más vendido", "respondemos el mismo día" ni "Framboyán"; cada artículo nuevo con ≥ 2 enlaces entrantes (índice + al menos otro artículo).

## Paso 4 — Registro, build y pruebas

1. Registra cada slug en: `contenido/articulo.py` (`NUEVOS` y `TRAS_2C`), `contenido/blog_clusters.py` (`POR_SLUG` y `MENSAJES`), `mensajes_paginas.py` (`BLOG`), `contenido/blog/_indice.json` (tarjeta al inicio de "Nuevos artículos"), `public/sitemap.xml` (URL con `lastmod`), `tests/paridad/blog-fotos.json` (foto de la tarjeta, antes de la de palma bambú) y sube `ENTREGA` en `sitemap_fechas.py` a la fecha del día.
2. Actualiza los conteos de las pruebas (`test_blog_paridad`, `test_entidad`, `test_respuestas`, `test_sitio`).
3. `python3 tools/site/build.py` dos veces (la segunda no debe cambiar nada).
4. Pruebas con Pillow (el Pillow del sistema está roto en el contenedor): `python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pillow==10.4.0`, luego desde `tools/site`: `/tmp/venv/bin/python -m unittest discover -s tests -p 'test_*.py'`. **Todas deben pasar** antes de publicar.

## Paso 5 — Publicación automática y verificación en producción

**Autorización permanente del dueño (2026-11-24): los artículos del blog semanal se publican solos, sin esperar aprobación.** No dejes PRs en borrador esperando revisión: esa fue la causa de que 12 artículos se quedaran sin publicar entre septiembre y noviembre de 2026.

1. Commit + push a la rama de la tarea y abre el PR contra `main` con el checklist de verificación en el body.
2. Si todas las pruebas pasaron: pasa el PR a "ready" y mergéalo (merge commit).
3. Espera a que el deployment de Vercel (proyecto `prj_ceThejPqpBt2CKvP8XwETk5mnBG6`, team `team_Phd8N1AzUdoeyOJMT5upEC43`) quede `READY` con `target: "production"` para ese commit.
4. Verifica con `mcp__Vercel__web_fetch_vercel_url` (el proxy bloquea curl a viverosterra.com) que cada artículo nuevo responda 200 en `https://www.viverosterra.com/blog/<slug>` y que aparezca en `https://www.viverosterra.com/blog`.
5. Notifica al dueño (PushNotification) con los títulos, URLs y la razón de los temas.
6. **Si algo falla** (pruebas rojas, conflicto de merge, deploy en ERROR o páginas que no responden 200): no mergees a ciegas; deja el PR abierto, explica el problema y notifica al dueño de inmediato.
7. El proyecto de Vercel no tiene Web Analytics: no inventes horarios "basados en datos"; se publica el día en que corre la tarea (lunes).
