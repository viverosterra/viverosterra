---
name: viveros-blog-semanal
description: Automatización semanal del blog de Viveros Terra (viverosterra.com/blog) — genera 2 artículos nuevos por semana (1 general de horticultura + 1 de planta específica), evita duplicar temas ya publicados o en PRs pendientes, sigue el patrón visual/SEO/AEO/schema del blog existente, publica y verifica en producción. Usar SIEMPRE que la tarea sea "blog semanal", "artículos de blog", "contenido del blog de Viveros Terra", o la tarea programada de automatización de blog.
---

# Blog semanal de Viveros Terra

Automatiza la creación de 2 artículos de blog por semana para viverosterra.com. Este skill existe porque varias corridas seguidas (semanas del 20-jul, 27-jul y 3-ago 2026) escribieron temas duplicados entre sí (Palma Areca dos veces, plagas de jardín dos veces) porque cada corrida solo revisaba el historial de `main` y no las ramas/PRs pendientes de semanas anteriores que nadie había mergeado. **El paso 1 de este workflow existe para que eso no vuelva a pasar.**

## Paso 1 — Inventario de temas ya cubiertos (OBLIGATORIO, antes de elegir tema)

No elijas ningún tema sin completar esto primero:

1. `ls public/blog/` en la rama base (`main`) → lista de slugs ya publicados.
2. `mcp__github__list_pull_requests` con `state: "open"` → **todos** los PRs abiertos, no solo los de blog.
3. Para cada PR abierto, `git fetch origin <rama>` y `git diff --name-status main origin/<rama> -- public/blog` para ver qué slugs propone.
4. Construye una lista única de "temas prohibidos esta semana" = slugs publicados + slugs en cualquier PR abierto (aunque esté en draft, aunque lleve semanas sin revisión — mientras esté abierto, cuenta).
5. Si un PR abierto lleva más de ~2 semanas sin actividad y duplica el tema de otro PR abierto, ciérralo como duplicado (con comentario explicando por qué) antes de continuar — no dejes que el backlog de duplicados siga creciendo semana tras semana.

## Paso 2 — Selección de temas

- **1 artículo general de horticultura**: estacional/evergreen, relevante al clima de Tampico/Tamaulipas (calor, humedad, temporada de lluvias jun-oct, temporada de huracanes jun-nov, temporada seca nov-abr). Valida con WebSearch que el tema tiene intención de búsqueda real.
- **1 artículo de planta/palma específica**: prioriza especies que YA están en el catálogo de Viveros Terra (`public/catalogo.html`) y mencionadas en `public/blog/palmas-mas-vendidas-tampico-precios/index.html` pero que no tienen su propia página de profundidad — mismo patrón que Palma Real, Palma del Viajero, Palma Areca, Palma Washingtona.
- **Precios: nunca inventes cifras.** Usa únicamente precios que ya existen publicados en el sitio (p. ej. la tabla de `palmas-mas-vendidas-tampico-precios`) o en el catálogo. Si no hay precio publicado para la especie elegida, no incluyas un precio específico — usa "cotiza por WhatsApp" en su lugar.

## Paso 3 — Escritura

Copia la estructura HTML completa de un artículo existente reciente (p. ej. `public/blog/palma-real-roystonea-regia-tampico/index.html` para plantas, o `public/blog/fertilizacion-jardines-tampico-temporada-lluvias/index.html` para temas generales) como plantilla — mismo CSS inline, mismo header/footer/nav, mismo patrón de schema JSON-LD (`Article` + `FAQPage` + `BreadcrumbList`), mismo AEO answer-box al inicio, mismas 5 preguntas frecuentes con botón+respuesta, mismo CTA de WhatsApp contextual, misma sección "También te puede interesar" con 3 artículos relacionados reales.

## Paso 4 — Publicar en el índice y sitemap

- `public/blog/index.html`: añade cards en la sección "Nuevos artículos" (actualiza el mes) y en "Todos los artículos", actualiza el contador `vt-hero__metric-num`.
- `public/sitemap.xml`: añade las 2 URLs nuevas con `lastmod`.
- Verifica antes de commitear: tags HTML balanceados, todas las imágenes referenciadas existen en `public/img/`, todos los enlaces internos apuntan a páginas reales, el conteo de slugs únicos en el índice coincide con el nuevo total.

## Paso 5 — PR, merge y verificación en producción

1. Commit + push a la rama de la tarea, abre PR **draft** contra `main` con el checklist de verificación en el body.
2. Este proyecto de Vercel (`prj_ceThejPqpBt2CKvP8XwETk5mnBG6`, team `team_Phd8N1AzUdoeyOJMT5upEC43`) NO tiene Web Analytics habilitado — no hay datos reales de tráfico para el calendario de publicación. Documenta esto explícitamente en el PR en vez de inventar horarios "basados en datos".
3. No mergees a producción sin autorización explícita del usuario en esa sesión — mergear un sitio de negocio real en vivo requiere confirmación, no se asume por la tarea programada sola.
4. Si el usuario autoriza mergear: pasa el PR de draft a ready, mergea, espera a que el deployment de Vercel quede `READY` con `target: "production"`, y verifica con `mcp__Vercel__web_fetch_vercel_url` que las páginas nuevas respondan 200 en `www.viverosterra.com` (no solo en el preview) antes de reportar éxito.
5. Notifica siempre al usuario si detectas PRs de blog abiertos de semanas anteriores sin resolver — ese backlog es la causa raíz de los duplicados y necesita decisión humana (mergear o cerrar) para no seguir acumulándose.
