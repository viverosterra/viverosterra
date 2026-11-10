# Estrategia y plan SEO / AEO / GEO — viverosterra.com

Fecha: 2026-11-10. Insumos (misma fecha): `docs/seo/2026-11/mapa-palabras-clave.md` (título, descripción y palabra clave por
página, canibalización, huecos, SEO local), `docs/seo/2026-11/auditoria-aeo-geo.md` (entidad, respuestas, llms.txt, plan de
menciones, consultas de prueba) y la auditoría técnica (resumida aquí). Sin acceso a Search Console: la demanda es estimada.

## Diagnóstico
- Base técnica sana: 108 URLs indexables, 200, canónica propia, 0 enlaces rotos, Lighthouse SEO 100, CLS 0.
- Ya es n.º 1 en "pasto en rollo tampico", "vivero tampico", "mantenimiento de jardines tampico", "sistema de riego tampico".
- Frenos: (1) tres domicilios en circulación (Faja de Oro 805, Obregón 601, y el vigente Obregón 209 Sur) y casi ninguna
  mención externa; (2) Google muestra páginas equivocadas (privacidad para "vivero ciudad madero", `/precios` para
  "jardinería tampico"); (3) 38 URLs heredadas de Wix redirigen a destinos genéricos; (4) entidad del negocio partida y
  Product sin `price`/`image`; (5) títulos largos (74 de 108 > 60) y páginas dinero poco enlazadas; (6) dos dominios
  propios compiten (pastosanagustin.mx) con datos distintos; (7) sitio viejo vivo en `mail.viverosterra.com`.

## Estrategia
1. Una sola entidad, un solo domicilio, en todos lados (sitio, redes, directorios, mapas).
2. Cada consulta con una sola página dueña: título, H1, primer párrafo con la respuesta y el dato, y enlaces internos con
   ancla descriptiva.
3. Ganar lo que nadie disputa en Tampico con sitio web: tierra negra, tezontle, piedra, poda, áreas verdes para industria.
4. Ser la fuente local citable de precios y cuidados (tablas con fecha, respuestas de 40–60 palabras, llms.txt exacto).
5. Reseñas y ficha de Google como palanca principal del mapa local (24 → 60 reseñas en 90 días).

## Fase 0 — Correcciones rápidas en el sitio (1 entrega)
- [ ] Títulos (≤ 60) y descripciones (≤ 155) del mapa en las páginas que no son blog; H1 de materiales con "en Tampico".
- [ ] `/politica-privacidad` a noindex y sin domicilio viejo; revisar que ningún HTML diga "Obregón 601" ni "Faja de Oro".
- [ ] `vercel.json`: destinos correctos de las 9 redirecciones de la tabla técnica; `/members`, `/profile/*`,
      `/preview-mapa-cobertura*` sin redirección (404); quitar reglas con barra final o `.html` que agregan saltos.
- [ ] `public/404.html` con la plantilla; favicon cuadrado (`favicon-192.png`, SVG y `/favicon.ico`).
- [ ] Home sin `BreadcrumbList` falso; protocolo con un solo H1 y JSON-LD; `priceValidUntil` renovado.
- [ ] Reglas del dueño que siguen rotas: "gratis" en og de diseño y mantenimiento y en `/politicas`; "más vendido" en
      toscana-28, irlanda-25 y viena-30; H1 de `/precios` "con IVA"; pie y menú "Precios con IVA"; 3 etiquetas del blog.
- [ ] Enlazado: `/vivero-tampico` y `/pasto-en-rollo-tampico` con más enlaces y anclas descriptivas; los 4 artículos con
      un solo enlace; anclas "Ver X →" con el nombre del servicio.
- [ ] Sacar `public/js/tests/` y `api/img.js` del despliegue si nada los usa.

## Fase 1 — Entidad, datos estructurados y respuestas (1 entrega)
- [ ] `/#negocio` único como `GardenStore` completo (logo, 6 `sameAs`, `hasMap`, `areaServed` como ciudades, REPSE,
      `knowsAbout`) en home y `/vivero-tampico`; nodo mínimo inline en las demás; `WebSite` en la home; sin
      `AggregateRating` propio.
- [ ] Product con `AggregateOffer` (`lowPrice`) e `image`; donde no hay precio real, `Service`/`ItemList`.
- [ ] Article completo en los 14 artículos (imagen, `mainEntityOfPage`, descripción, `dateModified`); `lastmod` del
      sitemap desde la fecha real; fecha de actualización visible en páginas de precio.
- [ ] Párrafo de respuesta directa (40–60 palabras, con precio, unidad y zona) al inicio de las 10 páginas del informe.
- [ ] `llms.txt` nuevo (formato llmstxt.org, sin "gratis", REPSE correcto, IVA correcto, solo datos de `datos.py`) y
      `llms-full.txt`.
- [ ] Open Graph completo (og:image en JPG, `og:site_name`, Twitter Card) en las páginas que faltan.

## Fase 2 — Arquitectura y contenido (por entregas)
- [ ] Páginas nuevas, en este orden: `/poda-arboles-tampico`, `/empresas`, `/nosotros`, `/zonas`.
- [ ] Migrar `/vivero-tampico` a la plantilla nueva (hoy rendimiento 81) y hacerla la página del perfil de Google.
- [ ] Clúster de palmas con pilar único; 5 fusiones del blog con 301; 5 artículos retitulados; diferenciar las 6 zonas.
- [ ] Recuperar como artículos los temas de Wix sin equivalente (monstera, ficus lyrata, coquillo y manchas del pasto,
      rosa del desierto, plantas nativas).
- [ ] 8 artículos nuevos que responden preguntas que Google ya muestra (lista en el mapa).
- [ ] `srcset` de 640 px en tarjetas del blog y zonas; describir las 47 miniaturas de modelos de sintético.
- Nochebuenas: se queda en su URL heredada por decisión del dueño (el mapa sugería moverla; no se hace).

## Fase 3 — Fuera del sitio (lo hace el dueño, con guía)
- [ ] Domicilio vigente en Instagram, Facebook, Cosmos y demás directorios.
- [ ] Ficha de Google: enlace a `/vivero-tampico`, categorías, 8 servicios, 11 productos con precio, fotos reales,
      publicación semanal, preguntas.
- [ ] Programa de reseñas: de 24 a 60 en 90 días (enlace directo y mensaje tras cada entrega).
- [ ] Bing Places y Apple Business Connect.
- [ ] `mail.viverosterra.com`: retirar el sitio viejo (cPanel). Apex a 308 en Vercel → Domains.
- [ ] pastosanagustin.mx: rol (mayoreo por tráiler), mismos datos (mínimo de mayoreo, horario, correo) y enlace cruzado.
- [ ] Dar acceso a Search Console y Bing Webmaster.

## Fase 4 — Medición (mensual)
- [ ] 15 consultas fijas en Google, Bing, ChatGPT y Perplexity (lista en la auditoría AEO), con captura.
- [ ] GA4: `generate_lead` por página de entrada y referidos de chatgpt.com, perplexity.ai, gemini, copilot.
- [ ] Search Console: impresiones y posición de las consultas objetivo; cobertura de las URLs de Wix.

## Preguntas abiertas al dueño
Rancho propio en Veracruz (lo afirma pastosanagustin.mx); mínimo de mayoreo 500 o 1,000 m²; horario desde 8 o 9;
correo oficial; especie de la palma kerpis; si vende frutales, macetas o control de plagas.
