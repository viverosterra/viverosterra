# Etapa 2 · Plantillas y migración por tipo de página — Hoja de ruta

Spec: `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.3, §4, §5, §10 (Etapa 2) y §11.
Sub-plan detallado en ejecución: `docs/superpowers/plans/2026-11-07-etapa-2a-plantillas-inicio-pasto-rollo.md`.
Cada sub-plan de abajo se escribe completo (tareas TDD, código y comandos) justo antes de ejecutarlo, sobre `main` con lo
anterior ya en producción, y se publica solo. Este documento fija alcance, riesgos y criterios para que no se pierda nada.

## Lo que 2a deja para todos los sub-plans

- **Arquitectura:** `tools/site/plantillas/<tipo>.py` (`render(contenido)`), `tools/site/contenido/<pagina>.py`
  (`CONTENIDO` + `PARIDAD`), `tools/site/componentes.py` (funciones puras, números solo de `datos.py`),
  `tools/site/generar.py` (registro `(ruta, archivo, plantilla, contenido)`; escribe con el shell y solo si cambia).
  Migrar una página = capturar → contenido → plantilla (o reutilizar) → fila en `generar.PAGINAS` → build.
- **Paridad:** `python3 tools/site/paridad.py capturar <ruta>` antes de tocar la página; `test_paridad.py` exige que cada
  encabezado h1–h3, pregunta, precio y enlace interno siga o tenga reemplazo o motivo en `PARIDAD`; meta y tipos de
  JSON-LD idénticos. `test_contenido.py`: solo HTML en línea permitido y `tipo` igual al de `paginas.py`.
- **CSS:** todo componente nuevo en `terra.css`, prefijo `.vt-`, base de elementos solo bajo `body.vt-pagina`;
  presupuesto < 10 KB gzip y < 48 KB sin comprimir (`test_terra_css.py`). Cada página migrada deja de cargar Tailwind,
  design-system, servicios, tienda-pasto, `legacy-fixes.css`, `<style>` propios y Google Fonts.
- **JS reutilizado, nunca reescrito:** `vt-mensualidades.js` (fórmula), `vt-simulador.js`, `vt-landed.js`,
  `tienda-pasto.js`, `tienda-hub.js`, `terra.js` (`data-cta`, `VTMedicion.whatsapp`, firma, `data-hero-cta`),
  el armador de lista del catálogo y las calculadoras de materiales. Los mensajes propios de cada página salen de
  `mensajes_paginas.py` y `datos.MENSAJES`.
- **Pruebas de cada lote:** las cuatro suites, build reproducible (segunda corrida sin cambios), `test_reglas.py`,
  `test_consistencia.py`, paridad, consola limpia en las 108 páginas, axe de página completa (0 serias) en una página
  por plantilla, sin desbordar a 320/375/768/1440, CTA y precio en el primer pantallazo móvil, CLS < 0.1, Lighthouse móvil
  (Perf ≥ 90; A11y ≥ 95 por lote, ≥ 98 al cerrar la Etapa 2), capturas `tools/site/capturas.py`.
- **Puertas (spec §11) en cada lote:** diseño, CRO y cumplimiento/QA; SEO/AEO en 2a, 2c y 2h (y en cualquier lote que
  toque JSON-LD). Aprobación del dueño en la vista previa de Vercel antes del merge.

## Sub-plans

### 2b · Pasto sintético (Tampico, hub, 9 fichas, 11 ciudades, perros)

- **Páginas:** `/pasto-sintetico-tampico`, `/pasto-sintetico` (hub), 9 fichas `/pasto-sintetico/{modelo}`,
  11 `/pasto-sintetico/envio/{ciudad}`, `/pasto-sintetico/perros`, `/pasto-sintetico/precios` y zonas de la tienda que
  hoy genera `tools/pasto`.
- **Plantillas:** `servicio` (Tampico, reutiliza 2a), nuevas `tienda_hub`, `ficha`, `ciudad`. Las fichas, ciudades y el
  hub **siguen generándose desde `tools/pasto/data.py`** (modelos, zonas, fletes): `tools/pasto/*.py` pasa a llamar a
  `componentes` y a las plantillas de `tools/site` en vez de su HTML propio; no se duplica ningún dato.
- **Componentes nuevos:** galería con imagen principal precargada (nunca `lazy`, J03), cotizador por estado (marcado de
  `tienda-pasto.js` intacto: `data-cta-wa`, `#cot-send`, lista "Cotización (n)" con "(0)" oculto), rollo a escala,
  comparativa con 2 vecinos, tabla 25/50/100 m² con mensualidad máxima (ciudades), encabezados en pregunta.
- **Riesgos:** romper `tienda-pasto.js` / `tienda-hub.js` (eventos `add_to_cart`, `view_cart`, `generate_lead` con
  `whatsapp_cotizador`) → pruebas de navegador existentes (`test_tienda_navegador.py`, cotizador de la ficha) más una por
  plantilla; bloqueo de total y mensualidades bajo 25 m² en envío nacional; `#buybar` y barra móvil nunca juntas;
  desborde conocido del hub a 320; `tienda-pasto.css` (53 KB) se retira al terminar el lote; corregir aquí el `round()` de
  `tools/pasto/mensualidades.py` (redondeo al par) para que la mensualidad sea igual a `Math.round` del JS, con prueba;
  minificación sin dependencias de la copia con hash en `activos.py` para mantener < 10 KB gzip.
- **Reglas del dueño en juego:** envío por rollo y nunca gratis; los 9 modelos en existencia nacional; "para llevar hoy"
  solo Toscana 18 y 28 (Obregón 209 Sur); sin pádel ni canchas; sin muestras físicas ("cómo elegir sin muestra");
  nunca marcas de proveedor; "desde 2012".
- **Paridad:** captura de las 24 páginas; modelos, precios por m² y por rollo, fletes por zona, tablas de las ciudades.
- **Aceptación:** precio "desde $X/m² · rollo 50 m² · envío por rollo según estado" en el primer pantallazo de cada ficha;
  totales del cotizador iguales a `data.py` y `vt-mensualidades.js` en los casos de J03 §3; feed de Merchant
  (`feed-pasto-sintetico.xml`) sin cambios de precio; `tienda-pasto.css` borrado.

### 2c · Servicios: diseño, mantenimiento y riego

- **Páginas:** `/diseno-jardines-tampico`, `/mantenimiento-jardines-tampico`, `/sistema-riego-tampico`.
- **Plantilla:** `servicio` de 2a (sin Medidor de pasto; secciones opcionales), con componente nuevo de **planes**
  (máx. 3, cada uno con su mensaje de WhatsApp: QW12, "un mensaje por plan" en mantenimiento) y línea de mensualidades por
  plan (sustituye `tools/servicios/planes_diseno.py`).
- **Riesgos:** `sendWA()` del diseño y su prueba de navegador (`test_window_open_de_whatsapp_sale_firmado`) → el plan
  debe conservar la función o migrar la prueba al marcado nuevo; JSON-LD con acentos rotos (se arreglan solo si la
  Etapa 4 no lo cubre: aquí se conservan); riego para campos deportivos con pasto natural se queda; cuestionario como
  paso 2 desde diseño; `tools/servicios/hero.py`, `simulador.py`, `planes_diseno.py` y `servicios.css` se retiran al
  terminar (ya no queda página que los use).
- **Paridad:** planes y precios (diseño $3,000 / $6,500 / desde $18,000; mantenimiento desde $750/mes; riego
  $180–$320/m²), garantía de plantas condicionada con enlace a `/politicas#garantia-plantas`, FAQ.
- **Aceptación:** un mensaje distinto por plan; garantía de plantas "en las que sembramos nosotros"; AdsBot sin bloqueo;
  `servicios.css` borrado.

### 2d · B2B: mayoreo y palmas para proyectos

- **Páginas:** `/mayoreo-pasto-tampico`, `/palmas-mayoreo-proyectos`.
- **Plantilla nueva `b2b`:** H1 por segmento + precio por volumen con mínimo → CTA "Cotizar proyecto" con plantilla
  `datos.MENSAJES["empresas"]` → clientes con nombre y logo (componente `logos()` de 2a) y REPSE verificable → tabla de
  escalas, capacidad y tiempos → documentación (CFDI 4.0, REPSE) → paquetes por obra → FAQ de compras → CTA.
- **Riesgos:** escalas y capacidades que no estén en `datos.py` (el dueño las da o no se publican); el `@id`
  `#localbusiness` y el Instagram equivocado de palmas se conservan hasta la Etapa 4 (solo se documentan); "Para
  proyectos solicitamos un anticipo al confirmar…" debe aparecer dos veces (`test_consistencia`).
- **Paridad:** especies y precios "desde" de palmas, mínimo de 500 m², FAQ.
- **Aceptación:** mayoreo con menos de 500 m² nunca aparece a $60; sin ficha descargable salvo PDF real.

### 2e · Plantas: hub, subcategorías, catálogo y fichas de plantas

- **Páginas:** `/plantas-palmas-arboles-tampico` (hub), `/palmas-tropicales-tampico`, `/plantas-para-jardin-tampico`,
  `/arboles-ornamentales-tampico`, `/arboles-para-banqueta-tampico`, `/plantas-de-interior-tampico`, `/catalogo`.
- **Plantillas nuevas:** `hub_categoria` (filtro por necesidad: sol/sombra, salitre, tamaño; subcategorías con "desde $")
  y `catalogo` (buscador y filtros arriba, una rejilla, tarjetas como `<button>` reales, "Arma tu lista" con un solo
  mensaje).
- **Riesgos:** **el armador de lista del catálogo** (mensajes sin SVG desde la Etapa 0, medición `select_content` y
  `VTMedicion.whatsapp`) → se conserva su JS y su contrato de datos; las ~118 fotos de `/api/img` pasan a
  `/img/catalogo/<especie>-tampico.webp` con dimensiones y alt (la descarga se hace una vez con un script versionado y su
  prueba; el proxy se elimina en la Etapa 5); foto real obligatoria en subcategorías; framboyán "Flamboyán desde $250"
  (`test_consistencia`); garantía de 30 días siempre condicionada; consolidación de títulos de plantas es Etapa 3.
- **Paridad:** especies, precios, nombres científicos, enlaces a blog.
- **Aceptación:** catálogo operable con teclado; un solo mensaje con toda la lista; LCP sin `/api/img`.

### 2f · Materiales

- **Páginas:** `/tierra-negra-vegetal-tampico`, `/tezontle-rojo-tampico`, `/marmol-blanco-tampico`,
  `/piedra-bola-rio-tampico`.
- **Plantilla nueva `material`:** H1 + precio por presentación (costal / m³ / camión) → usos → calculadora de cantidad
  (se reutiliza la lógica actual de cada página como función pura con casos de paridad, igual que el Medidor) → entrega
  → FAQ → CTA con `datos.MENSAJES["materiales"]`.
- **Riesgos:** precios de mármol y piedra bola y tezontle por camión que no están en `datos.py` (el dueño los confirma
  o se dejan "según cotización" sin inventar); calculadoras con `window.open` medidas por `medicion_js.py`.
- **Aceptación:** precios de `datos.PRECIOS`; calculadora con los mismos resultados que hoy en los casos capturados.

### 2g · Zonas y precios

- **Páginas:** 6 `/jardineria-*` y `/precios` (más `/vivero-tampico` si cabe; si no, va en 2i).
- **Plantillas nuevas:** `zona` (H1 "Jardinería en {zona}", servicios con precio, caso real con permiso, problema local,
  tiempo desde el vivero, CTA con plantilla de zona, enlaces a servicios) y `precios` (respuesta directa con vigencia,
  tablas por servicio con columna Unidad generadas de `datos.PRECIOS`, mensualidades, garantías y anclas estables
  `#garantia-plantas`, `#mensualidades`).
- **Riesgos:** contenido único por zona es Etapa 3 (aquí se conserva el actual, sin doorways nuevos); anclas que hoy
  enlazan otras páginas (`/politicas#mensualidades`, `/precios#…`) no pueden romperse (`test_enlaces` + prueba de anclas
  nueva); `/precios` es la fuente única que enlazan los blogs de precios.
- **Aceptación:** `/precios` sin un solo número escrito a mano (todo de `datos.py`); misma respuesta de precio de pasto
  que home y pasto en rollo.

### 2h · Blog: índice y 53 artículos

- **Páginas:** `/blog` y los 53 `/blog/{slug}`.
- **Plantilla nueva `articulo`:** respuesta directa → autor "Equipo técnico de Viveros Terra" (texto visible; el
  `Organization` ligado a `#negocio` es Etapa 4) y fecha de actualización → cuerpo con columna de margen y Notas de campo
  → 2–3 enlaces contextuales → una etiqueta de "producto relacionado" → CTA a una landing → relacionados. Índice con el
  conteo del build (`data-vt-conteo`).
- **Contenido:** los cuerpos se extraen una sola vez a `tools/site/contenido/blog/<slug>.html` (HTML del artículo con
  bloque de metadatos; para 53 piezas largas un módulo Python por post sería ilegible) por un script de extracción con
  prueba; la plantilla los envuelve. Esta es la única excepción a "contenido en .py", justificada por el volumen de prosa.
- **Riesgos:** pérdida de contenido (53 piezas): paridad por post más un diff de texto visible palabra por palabra
  antes/después (el texto del artículo no cambia en 2h, solo su envoltura); `SyntaxError` de scripts viejos (Etapa 0)
  no debe volver; mensajes de WhatsApp por artículo de `mensajes_paginas.BLOG`; "flamboyán" y slugs `framboyan-…` intactos;
  `h2{font-family:Playfair…}` de 41 posts desaparece con su `<style>`; `test_articulos_del_blog_sin_desbordar_a_375`;
  fechas faltantes en 8 posts (se muestran solo si existen; Etapa 4 las completa).
- **Aceptación:** 53 posts con paridad en verde y diff de texto vacío; sin bloque idéntico de 6–7 enlaces; un CTA a
  landing por post; axe en 3 posts representativos.

### 2i · Utilitarias: políticas, privacidad, gracias, cuestionario, datos de envío, protocolo, vivero y 404

- **Páginas:** `/politicas`, `/politica-privacidad`, `/gracias`, `/cuestionario`, `/datos-envio`,
  `/protocolo-cuidados-pasto-san-agustin`, `/vivero-tampico` (si no entró en 2g) y `404.html`.
- **Plantillas nuevas:** `legal` (políticas y privacidad con anclas estables, incluida `#garantia-pasto` nueva y las
  existentes), `formulario` (gracias, cuestionario, datos de envío: labels en todos los controles, `noindex`, formsubmit a
  `viverosterra@hotmail.com`, gracias con promesa única y "Adelantar por WhatsApp"), `protocolo` (HowTo visible) y `404`
  (menú, buscador de servicios, CTA; la página `/404` completa es de la Etapa 3 si requiere enrutamiento).
- **Riesgos:** formularios (no cambiar `action` ni nombres de campos: el dueño recibe esos correos); el cuestionario es
  el paso 2 del diseño y es `noindex`; enlaces de anclas desde otras páginas.
- **Cierre de la Etapa 2 (último commit de 2i):** borrar `tailwind.css`, `design-system.css`, `servicios.css`,
  `tienda-pasto.css` y `legacy-fixes.css` (y sus copias con hash) con una prueba que falle si alguna página los
  referencia; quitar `tools/site/migrar_shell.py` si ya no hay páginas a mano; una prueba "toda página de `public/` sale
  de `generar.PAGINAS` o de `tools/pasto`"; Lighthouse A11y ≥ 98 por plantilla; capturas de referencia aprobadas
  guardadas para la regresión visual.

## Orden y lotes de publicación (spec §10)

| Lote | Sub-plans | Notas |
|---|---|---|
| 1 | 2a | Home y pasto en rollo (mayor impacto en leads). |
| 2 | 2b | Toda la tienda en un lote: hub, fichas y ciudades comparten JS. |
| 3 | 2c + 2d | Servicios y B2B. |
| 4 | 2e + 2f | Plantas y materiales (catálogo con fotos locales). |
| 5 | 2g + 2h + 2i | Zonas, precios, blog y utilitarias; cierra la Etapa 2. |

## Lo que aporta el dueño (acumulado)

Sesión de fotos real de medio día; precios "desde" de palmas faltantes, mármol, piedra bola y tezontle por camión;
escalas y capacidades de mayoreo; casos reales por zona con permiso; confirmación de los formularios de correo (2a) y,
si eran reales, permiso para reponer testimonios con nombre.
