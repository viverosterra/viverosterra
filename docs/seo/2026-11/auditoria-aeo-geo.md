# Auditoría AEO / GEO / LLMO de viverosterra.com

Fecha: 2026-11-09 · Alcance: solo lectura (repo `~/dev/viverosterra`, rama `main` en `db96bab`, un commit detrás de `origin/main`; sitio en vivo por GET).
Los tres HTML que comparé (home, `/pasto-en-rollo-tampico`, `/precios`) y `llms.txt` son idénticos en vivo y en el repo.

Cada hallazgo lleva una etiqueta: **[C]** comprobado (lo vi en el repo, en la respuesta HTTP o en la búsqueda) o **[I]** inferido (criterio profesional, sin medición directa).

---

## 1. Resumen

El sitio está técnicamente listo para que lo lean los asistentes: HTML estático completo, 200 para todos los bots, `robots.txt` abierto, `llms.txt` publicado, 103 de 111 páginas con `FAQPage` y el blog con bloque de "Respuesta directa". El problema no es el rastreo, son cuatro cosas:

1. **Fuera del sitio la marca casi no existe y lo poco que hay dice otra dirección.** En las búsquedas de marca y de categoría que hice, `viverosterra.com` no apareció ni una vez; las fuentes que respondieron fueron Cosmos (con "Faja de Oro 805, Tampico"), Cronoshare y Habitissimo.
2. **El dato del IVA se contradice dentro del propio sitio** (pasto solo y mayoreo: "no llevan IVA" en `/precios`, "con IVA" en home, mayoreo y `llms.txt`). Un modelo que ve dos versiones cita la que le toque o ninguna.
3. **La entidad está partida**: el nodo `/#negocio` de la home es bueno pero incompleto (sin TikTok, YouTube, Maps ni REPSE), y cinco páginas clave declaran otro `LocalBusiness` suelto, sin `@id`.
4. **Las páginas de servicio que más venden no abren con la respuesta.** `/pasto-en-rollo-tampico` empieza con un texto de marca; el precio está en una tarjeta aparte. No hay fecha de actualización visible ni `dateModified` fuera del blog y Nochebuenas.

### Hallazgos priorizados

| # | Prioridad | Hallazgo | Tipo |
|---|-----------|----------|------|
| 1 | ALTO | Dirección vieja "Faja de Oro 805, Col. Loma de Rosales, Tampico" en Cosmos, que es la fuente que más salió en las búsquedas | C |
| 2 | ALTO | `viverosterra.com` no apareció en ninguna de las 10 búsquedas de prueba (marca, categoría, precio) | C |
| 3 | ALTO | Contradicción de IVA en pasto solo y mayoreo entre `/precios`, `datos.RESPUESTA_PRECIO_PASTO`, `/mayoreo-pasto-tampico` y `llms.txt` | C |
| 4 | ALTO | `/#negocio` incompleto: `sameAs` sin TikTok, YouTube ni Maps; sin REPSE, `knowsAbout`, `legalName`, `logo`; `areaServed` con zonas que no existen como lugar | C |
| 5 | ALTO | Cinco páginas declaran un `LocalBusiness` anónimo en vez de referenciar `/#negocio` (pasto en rollo, diseño, riego, mantenimiento, vivero) | C |
| 6 | ALTO | `llms.txt`: enlace del REPSE en 404, palabra "gratis", zonas y plazos que no están en `datos.py`, falta Renault, tierra negra incompleta | C |
| 7 | ALTO | Páginas de servicio sin respuesta directa al inicio (home, pasto en rollo, sintético ×2, riego, mantenimiento, diseño, vivero) | C |
| 8 | MEDIO | Sin fecha visible ni `dateModified` en servicios y precios; `Last-Modified` cambia en cada despliegue | C |
| 9 | MEDIO | `SpeakableSpecification` suelto en el `@graph` (no cuelga de ningún `WebPage`) y apunta a `h1`, `h2` y preguntas, no a las respuestas | C |
| 10 | MEDIO | Sin nodos `WebSite` ni `WebPage` en la home; tres bloques JSON-LD separados y un `BreadcrumbList` que no es una ruta | C |
| 11 | MEDIO | Sin ficha en Wikidata; LinkedIn y Facebook no responden a clientes sin sesión | C |
| 12 | MEDIO | Nombre científico de la palma kerpis en conflicto: `datos.py` dice *Hyophorbe lagenicaulis*, el blog dice *Howea forsteriana* | C |
| 13 | MEDIO | 8 artículos de abril sin `dateModified`, `image` ni `mainEntityOfPage`; autor del blog sin `@id` | C |
| 14 | MEDIO | Sin `llms-full.txt` ni versiones `.md` | C |
| 15 | BAJO | `viverosterra.com` → `www` responde 307 (temporal) en vez de 308 | C |
| 16 | BAJO | `priceValidUntil` solo en una oferta de todo el sitio | C |
| 17 | BAJO | Sitemap sin imágenes; 10 páginas sin `og:image` | C |

---

## 2. Entidad

### 2.1 Dentro del sitio

**Lo que está bien [C]**
- `tools/site/datos.py` es la fuente única y el NAP visible es consistente: "Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero", 833 326 8008, horario L–V 9–18 y sáb 9–14.
- No hay "Obregón 601" ni "Faja de Oro" en ningún HTML de `public/`.
- La home define `LocalBusiness` con `@id` `https://www.viverosterra.com/#negocio`, `foundingDate` 2007-12-12, `geo`, `openingHoursSpecification`, `hasMap`, `telephone`, `email`.
- La mayoría de las plantillas nuevas (hubs de plantas, materiales, zonas, B2B, precios, blog) referencian `{"@id": ".../#negocio"}` como `provider`, `seller`, `publisher` o `about`.

**Lo que falla [C]**

| Problema | Dónde | Evidencia |
|----------|-------|-----------|
| `sameAs` incompleto | `tools/site/contenido/inicio.py:62` | Solo Facebook, Instagram y LinkedIn. `datos.REDES` tiene además TikTok y YouTube, y `datos.MAPS_URL` el perfil de Google. La lista está escrita a mano en vez de salir de `datos.REDES` |
| REPSE ausente del JSON-LD | home | El folio 773725 solo está en texto. Falta `identifier` |
| `areaServed` con lugares inventados como zona | home | `"Tampico Centro", "Madero Norte", "Madero Sur", "Altamira Industrial", "Victoria"`: cadenas de texto, no `City`. `datos.ZONAS_POR_PROYECTO` dice "Pánuco, Pueblo Viejo, Tuxpan, Cd. Victoria y la Huasteca" |
| `LocalBusiness` duplicado sin `@id` | `/pasto-en-rollo-tampico` (`seller`: solo nombre y teléfono), `/diseno-jardines-tampico`, `/sistema-riego-tampico`, `/mantenimiento-jardines-tampico` (`provider` con dirección pero sin `@id`), `/vivero-tampico` (nodo completo con `url` distinta y sin `@id`) | Para un parser son seis negocios distintos con el mismo nombre |
| `/pasto-sintetico-tampico` y Nochebuenas redefinen `/#negocio` con otros campos | plantillas `servicio`/`nochebuenas` | No es un error (mismo `@id`), pero el tipo cambia a `["LocalBusiness","Store"]` y `knowsAbout` solo existe ahí |
| Tienda de sintético: `seller` es un `Organization` sin `@id` | `/pasto-sintetico` y fichas | 9 `Organization` anónimas en el hub |
| Home sin `WebSite` ni `WebPage` | `tools/site/plantillas/inicio.py` | Tres `<script>` independientes; el `FAQPage` no está ligado a la entidad |
| `BreadcrumbList` de la home | home | Lista 5 páginas hermanas (Inicio, Pasto, Plantas, Diseño, Catálogo) como si fueran una ruta. No es una miga |
| Descripción del negocio sin "vivero" | home | Empieza con "Especialistas en pasto en rollo…". No dice qué es la entidad (vivero y empresa de jardinería) ni desde cuándo |
| Tipo genérico | home | `LocalBusiness`. Hay subtipos exactos: `GardenStore` (tienda) y `LandscapingBusiness` no existe; lo correcto es `["GardenStore","HomeAndConstructionBusiness"]` o `["LocalBusiness","GardenStore"]` |

### 2.2 Fuera del sitio

| Fuente | Qué dice | Estado |
|--------|----------|--------|
| Cosmos (`cosmos.com.mx/empresa/viveros-terra-dsc4.html`) | "Faja de Oro 805, Col. Loma de Rosales, 89100 Tampico". Web `http://www.viverosterra.com/`. Sin Cd. Madero. Aparece como proveedor en decenas de páginas de producto (pasto en rollo, pasto sintético, plantas, macetas, riego) | **[C] Dirección vieja. Es la fuente que más devolvió el buscador** |
| Cronoshare (`cronoshare.com.mx/croner-584253-viveros-terra-tampico`) | "Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, Ciudad Madero". Sin teléfono ni URL del sitio. "más de 15 años". Menciona "diseños gratuitos a partir de fotos". 1 reseña (marzo 2026) | [C] Dirección correcta; faltan teléfono y web; el texto contradice la regla de no ofrecer nada gratis |
| Google Maps (`maps.app.goo.gl/xC4XGL2WeucAjGwAA`) | El enlace corto responde 200 | [C] Existe. No pude leer la ficha (nombre, categoría, horario) sin navegador |
| Instagram, TikTok, YouTube | 200. El canal se llama "Viveros Terra Tampico" | [C] Existen |
| Facebook, LinkedIn | 400 y 403 a un cliente sin sesión | [C] No verificable desde fuera; un bot tampoco las lee |
| Wikidata | Búsqueda "Viveros Terra": 0 resultados | [C] No existe |
| Sección Amarilla | Listados de viveros de Tampico sin Viveros Terra en lo que devolvió el buscador | [C] parcial: no revisé todas las páginas |
| "Obregón 601" | No apareció en ninguna búsqueda | [C] No lo encontré; no puedo confirmar dónde sigue publicado |

Observación sobre el nombre **[I]**: fuera del sitio conviven "Viveros Terra", "Viveros Terra Tampico" (Cronoshare, YouTube) y el slug de LinkedIn `viveros-terra-tampico`. Conviene fijar "Viveros Terra" como `name` y declarar "Viveros Terra Tampico" como `alternateName`, porque la sede está en Madero y el apellido "Tampico" empuja a los modelos a ubicarla mal.

### 2.3 Nodo `/#negocio` propuesto

Todo sale de `datos.py`. Los campos marcados con `←` necesitan un dato que hoy no está en `datos.py` y hay que pedir al dueño; si no lo hay, se omiten.

```json
{
  "@type": ["LocalBusiness", "GardenStore"],
  "@id": "https://www.viverosterra.com/#negocio",
  "name": "Viveros Terra",
  "alternateName": "Viveros Terra Tampico",
  "description": "Vivero y empresa de jardinería en Ciudad Madero, Tamaulipas, fundada en 2007. Vende e instala pasto San Agustín en rollo y pasto sintético, diseña jardines, instala riego automático, da mantenimiento a áreas verdes y vende plantas, palmas, árboles y materiales en Tampico, Ciudad Madero y Altamira.",
  "url": "https://www.viverosterra.com/",
  "foundingDate": "2007-12-12",
  "telephone": "+528333268008",
  "email": "viverosterra@hotmail.com",
  "logo": "← URL del logo",
  "image": "https://www.viverosterra.com/img/jardineria-areas-verdes-tampico.jpg",
  "priceRange": "$$",
  "currenciesAccepted": "MXN",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional",
    "addressLocality": "Ciudad Madero",
    "addressRegion": "Tamaulipas",
    "postalCode": "89510",
    "addressCountry": "MX"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": 22.2777575, "longitude": -97.8433341},
  "hasMap": "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA",
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}
  ],
  "identifier": {"@type": "PropertyValue", "propertyID": "REPSE", "name": "Registro REPSE (STPS)", "value": "773725", "url": "https://repse.stps.gob.mx/"},
  "areaServed": [
    {"@type": "City", "name": "Tampico", "containedInPlace": {"@type": "State", "name": "Tamaulipas"}},
    {"@type": "City", "name": "Ciudad Madero", "containedInPlace": {"@type": "State", "name": "Tamaulipas"}},
    {"@type": "City", "name": "Altamira", "containedInPlace": {"@type": "State", "name": "Tamaulipas"}}
  ],
  "knowsAbout": [
    "Pasto San Agustín (Stenotaphrum secundatum)", "Pasto en rollo", "Pasto sintético",
    "Diseño de jardines", "Riego automático", "Mantenimiento de áreas verdes",
    "Palmas tropicales", "Plantas tolerantes a la brisa salina", "Jardinería en clima cálido húmedo del Golfo de México"
  ],
  "sameAs": [
    "https://www.facebook.com/viverosterra/",
    "https://www.instagram.com/viverosterramx",
    "https://www.tiktok.com/@viverosterra",
    "https://www.youtube.com/@viverosterramx",
    "https://www.linkedin.com/company/viveros-terra-tampico",
    "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"
  ],
  "hasOfferCatalog": {"@id": "https://www.viverosterra.com/precios#lista"},
  "contactPoint": {"@type": "ContactPoint", "contactType": "ventas", "telephone": "+528333268008", "availableLanguage": "es", "areaServed": "MX"}
}
```

Regla de implementación: el nodo completo vive **solo en la home**; el resto de las páginas usa `{"@id": "https://www.viverosterra.com/#negocio"}` y nada más. Una prueba en `tools/site/tests` debería fallar si aparece `"@type": "LocalBusiness"` sin ese `@id` en cualquier página que no sea la home, y si `sameAs` no coincide con `datos.REDES` + `datos.MAPS_URL`.

---

## 3. Respuestas extraíbles

### 3.1 Estado de las 15 páginas principales [C]

Criterio: primer párrafo después del `<h1>` con 40–60 palabras, que nombre el sujeto, el dato, la unidad y la zona en la misma frase.

| Página | Primer párrafo (palabras) | ¿Responde con dato? | Tablas / listas ordenadas / FAQ | Fecha visible |
|--------|---------------------------|----------------------|-------------------------------|---------------|
| `/` | 30 | No: "El precio va por delante" y el precio en tarjeta aparte | 1 / 2 / 6 | No |
| `/pasto-en-rollo-tampico` | 29 | No: habla del corte semanal; el precio va en tarjeta | 3 / 2 / 8 | No |
| `/precios` | 35 | **Sí** (falta riego, fecha y la nota de IVA) | 6 / 1 / 6 | Solo "2026" |
| `/pasto-sintetico-tampico` | 29 | No | 2 / 2 / 10 | "vigentes en 2026" |
| `/pasto-sintetico` | 11 | No: precio y envío en fragmentos | 3 / 3 / 9 | No |
| `/mayoreo-pasto-tampico` | 47 | **Sí**, pero dice "con IVA" (contradice `/precios`) | 1 / 2 / 8 | No |
| `/vivero-tampico` | 9 | No: la dirección llega en el 2.º párrafo, sin CP ni horario | 0 / 0 / 0 visibles | No |
| `/diseno-jardines-tampico` | 34 | Parcial: sin precio en la frase | 2 / 2 / 9 | No |
| `/sistema-riego-tampico` | 17 | No | 2 / 2 / 8 | No |
| `/mantenimiento-jardines-tampico` | 11 | No | 2 / 2 / 8 | No |
| `/tierra-negra-vegetal-tampico` | 51 | **Sí**, modelo a seguir | 1 / 1 / 8 | No |
| `/palmas-tropicales-tampico` | 41 | **Sí** | 1 / 1 / 9 | No |
| `/plantas-palmas-arboles-tampico` | 29 | No | 0 / 2 / 8 | No |
| `/post/nochebuenas-…` | 16 | Parcial: frase tipo lema | 1 / 3 / 1 | `dateModified` sí, visible no |
| `/blog/pasto-san-agustin-vs-japones` | 42 (bloque de respuesta) | **Sí** | 1 / 4 / 6 | Sí ("Publicado 20 de abril de 2026") |

Lectura: las plantillas de materiales, B2B y blog ya tienen el patrón correcto ("En Viveros Terra la tierra negra vegetal cuesta $90 el costal y $1,500 el m³…"). Falta llevarlo a `servicio.py`, `inicio.py`, `tienda_hub.py` y `/vivero-tampico`.

Las tablas son `<table>` reales, los pasos son `<ol>` y las preguntas son `<details>` con el texto en el HTML: eso está bien y no hay que tocarlo.

### 3.2 La contradicción del IVA [C] (ALTO)

| Lugar | Texto |
|-------|-------|
| `/precios` (tabla y FAQ) | "El instalado incluye IVA. El pasto solo y el mayoreo no llevan IVA." |
| `datos.RESPUESTA_PRECIO_PASTO` (home, FAQ con JSON-LD) | "$85 por m² solo el pasto y desde $120 por m² instalado, con IVA incluido. […] Precios 2026, con IVA" |
| `/mayoreo-pasto-tampico` (primer párrafo) | "desde $60/m² (solo pasto) en pedidos de 500 m² o más, con IVA y factura CFDI 4.0" |
| `llms.txt` | Encabezado "Servicios y precios (2026, MXN, IVA incluido)" que cubre pasto solo, mayoreo y palmas |

La regla del negocio es que el pasto sin instalar y las plantas no llevan IVA. Hay que corregir la constante en `datos.py` (una sola frase alimenta home, servicio y precios), el párrafo de mayoreo y `llms.txt`. Conviene una prueba que busque "con IVA" a menos de N caracteres de `$85` o `$60`.

### 3.3 Respuestas reescritas (listas para usar)

Todas las cifras salen de `datos.py` (o de `tools/pasto/data.py` en la tienda de sintético). Ninguna usa "gratis" ni "sin costo". Van como primer párrafo bajo el `<h1>`, en una clase estable (por ejemplo `.vt-respuesta`) para poder apuntarla desde `speakable`.

**1. `/` (58 palabras)**
> Viveros Terra es un vivero y empresa de jardinería en Ciudad Madero, Tamaulipas, que atiende Tampico, Madero y Altamira desde 2007. Vende pasto San Agustín en rollo a $85 por m² solo el pasto (no lleva IVA) e instalado desde $120 por m² con IVA, además de diseño, riego, mantenimiento desde $750 al mes, plantas y pasto sintético.

**2. `/pasto-en-rollo-tampico` (60 palabras)**
> En Tampico, Ciudad Madero y Altamira, el pasto San Agustín en rollo cuesta $85 por m² solo el pasto (no lleva IVA) y desde $120 por m² instalado, con IVA incluido (precios 2026). El instalado incluye preparación básica del terreno, colocación y garantía de arraigo de 15 a 20 días. Desde 500 m², el mayoreo cuesta desde $60 por m².

**3. `/precios` (60 palabras)**
> Precios 2026 de Viveros Terra en Tampico, Madero y Altamira: pasto San Agustín a $85 por m² solo el pasto y desde $120 por m² instalado; mantenimiento de jardín desde $750 al mes; diseño desde $3,000; riego automático de $180 a $320 por m²; pasto sintético desde $139 por m² en rollo y de $385 a $650 por m² instalado.

Debajo, en una línea aparte y visible: `Actualizado el <time datetime="AAAA-MM-DD">D de mes de AAAA</time>. Todos los precios incluyen IVA, salvo el pasto sin instalar, el mayoreo de pasto y las plantas, que no lo llevan.` La fecha debe salir de una constante nueva en `datos.py` (por ejemplo `PRECIOS_ACTUALIZADOS`), no de la fecha del build.

**4. `/pasto-sintetico-tampico` (58 palabras)**
> En Tampico, Ciudad Madero y Altamira, el pasto sintético instalado cuesta de $385 a $650 por m², con material, colocación e IVA; la preparación del terreno se cotiza aparte en la visita. También vende solo el material, desde 2 m², en su showroom de Obregón 209 Sur, Ciudad Madero; en rollo de 50 m², desde $139 por m².

**5. `/pasto-sintetico` (58 palabras)**
> Viveros Terra envía pasto sintético a todo México desde Ciudad Madero, Tamaulipas: 9 modelos de 10 a 35 mm, desde $139 por m² en rollo de 50 m², con IVA incluido. El envío cuesta de $900 a $1,400 por rollo según el estado, llega en 3 a 5 días hábiles y el pedido mínimo es de 25 m².

**6. `/mayoreo-pasto-tampico` (60 palabras)**
> El pasto San Agustín en rollo al mayoreo cuesta desde $60 por m², solo el pasto, en pedidos de 500 m² o más en Tampico, Ciudad Madero y Altamira (2026). El pasto sin instalar no lleva IVA y se factura con CFDI 4.0. Viveros Terra entrega por etapas según el avance de la obra; fuera de la zona, por proyecto.

**7. `/sistema-riego-tampico` (51 palabras)**
> Un sistema de riego automático instalado en Tampico, Ciudad Madero o Altamira cuesta de $180 a $320 por m², con IVA, según el tipo de sistema (aspersión, goteo o microaspersión) y el número de zonas. Viveros Terra lo diseña y lo instala con programador; bien programado, ahorra hasta 40% de agua.

**8. `/mantenimiento-jardines-tampico` (56 palabras)**
> El mantenimiento de jardines en Tampico, Ciudad Madero y Altamira cuesta desde $750 al mes, con IVA, en el plan residencial de Viveros Terra. Incluye poda, fertilización y control de plagas en visitas programadas: semanales, cada 15 días, cada 21 días o mensuales. Los planes premium y para empresas se cotizan según el tamaño del jardín.

**Extra A. `/vivero-tampico` (60 palabras)**
> Viveros Terra es un vivero en Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamaulipas (frente a Walmart, entrando por Banamex), que atiende Tampico, Madero y Altamira desde 2007. Abre de lunes a viernes de 9 a 18 h y sábados de 9 a 14 h, con más de 200 variedades de plantas, palmas y árboles.

**Extra B. `/diseno-jardines-tampico` (53 palabras)**
> El diseño de jardines en Tampico con Viveros Terra (Plan Terra) cuesta $3,000 en el plan Esencial, $6,500 en el Completo y $18,000 en el Premium, con IVA. En los planes Esencial y Completo, el costo del diseño se descuenta al contratar la obra; en el Premium, en proyectos de más de $150,000.

Nota: "desde 2 m²" en el showroom y los nombres de plan "Esencial / Completo / Premium" no están en `datos.py`; los comprobé en el HTML publicado de `/pasto-sintetico-tampico` y `/diseno-jardines-tampico`.

### 3.4 Otras mejoras de extracción

- **Encabezados como pregunta [I]**: en las páginas de servicio, al menos un `<h2>` con la pregunta literal ("¿Cuánto cuesta el pasto San Agustín por m² en Tampico?"). Hoy los H1 son de marca ("…instalado en un día. Del campo a tu jardín, sin pasar por bodega"), lo que dificulta el emparejamiento pregunta-respuesta.
- **Tabla con `<caption>` y fecha [I]**: "Precios de pasto San Agustín en Tampico, noviembre de 2026". Los modelos citan tablas con título y unidad en la cabecera.
- **Definiciones [I]**: una frase de definición por término donde aplique ("Un tepe es una pieza de pasto en rollo de 40 × 60 cm"). El dato ya está en la página, solo falta la forma "X es Y".
- **Fecha visible [C]**: solo el blog la muestra. Añadirla a `/precios`, a las páginas de servicio con precio y a Nochebuenas (ya tiene `ultima_actualizacion` en `datos.py`).

---

## 4. `llms.txt`

### 4.1 Diagnóstico [C]

**Estructura frente a llmstxt.org**

| Requisito | Estado |
|-----------|--------|
| `# Título` | Correcto |
| `> resumen` en bloque de cita | Correcto |
| Texto libre sin encabezados antes del primer `##` | Correcto ("Datos clave") |
| Secciones `##` que contienen **listas de enlaces** `- [nombre](url): nota` | **No cumple** en "Servicios y precios", "Zonas de cobertura", "Preguntas frecuentes" y "Lo que no hacemos": son prosa con URLs sueltas. Solo "Páginas principales" sigue el formato |
| Sección `## Optional` para lo prescindible | No existe |
| Enlaces a versiones Markdown | No existen (`/index.md`, `/pasto-en-rollo-tampico.md`: 404) |

**Exactitud contra `datos.py`**

| Línea de `llms.txt` | Problema |
|---------------------|----------|
| "verificable en https://repse.stps.gob.mx/Publico" | 404 comprobado. `datos.REPSE_PADRON` ya tiene la correcta: `https://repse.stps.gob.mx/` (200) |
| "Servicios y precios (2026, MXN, IVA incluido)" | El pasto solo, el mayoreo y las plantas no llevan IVA |
| "Plantas compradas y sembradas por el cliente reciben asesoría gratis" | Palabra prohibida |
| "Cobertura directa (mismo día)", "Cobertura regular (24–72 hrs): Pánuco, Ciudad Victoria, Ciudad Mante, Aldama, Naranjos", "Por proyecto: Tuxpan, Cerro Azul, Tempoal, El Higo…" | Ni los plazos ni Mante, Aldama, Naranjos, Cerro Azul, Tempoal o El Higo están en `datos.py`. `ZONAS_POR_PROYECTO` = "Pánuco, Pueblo Viejo, Tuxpan, Cd. Victoria y la Huasteca" |
| Clientes B2B | Falta Renault (`datos.CLIENTES_B2B` tiene 7) |
| "tierra negra vegetal (costal $90, camión 8m³+)" | Incompleto: faltan m³ a $1,500, tierra preparada a $100 y camiones de 5, 8 y 14 m³ a $3,500, $5,200 y $8,000 |
| "mármol blanco y piedra bola" | Sin precio: el mármol cuesta $250 el saco, IVA incluido, sujeto a disponibilidad |
| "Material desde $139/m² e instalación desde $385/m²" | Se lee como si la instalación fuera aparte; los $385 ya incluyen material |
| "Última actualización: 2026-11-07" | Los materiales se actualizaron el 8 y Nochebuenas el 9 |
| Sin diseño por plan ($6,500 y $18,000), sin poda (desde $500), sin flamboyán (desde $250), sin +200 sistemas de riego | Cobertura incompleta |

El archivo se mantiene a mano. `datos.py` dice en su docstring que desde la Etapa 4 lo consumiría `llms.txt`: eso es lo que hay que hacer, generarlo en `build.py` desde `datos.py` y `tools/pasto/data.py`, con una prueba que falle si aparece una cifra que no esté en esas fuentes.

### 4.2 `llms-full.txt` y versiones `.md`

- **`llms-full.txt`: sí, MEDIO [I].** El sitio es pequeño (unas 100 páginas, 1,500–2,000 palabras cada una). Un solo archivo con el texto limpio de las 20–25 páginas clave (precios, servicios, materiales, tienda de sintético, políticas y 8–10 guías) cabe en el contexto de cualquier modelo y ahorra el ruido del shell. Generarlo desde `tools/site/contenido/*.py`, que ya tiene el contenido estructurado.
- **Versiones `.md`: sí, pero solo de las páginas clave, MEDIO-BAJO [I].** La propuesta de llmstxt.org pide la misma URL con `.md` añadido. En Vercel con `cleanUrls` basta escribir `public/precios.md`, `public/pasto-en-rollo-tampico.md`, etc. Deben llevar `<link rel="canonical">` equivalente por cabecera (`Link: <…>; rel="canonical"`) o `X-Robots-Tag: noindex` en `vercel.json` para no duplicar en Google.
- **Honestidad sobre el efecto [I]:** ningún buscador de IA ha confirmado que use `llms.txt` para ordenar o citar. Su valor comprobable hoy es para agentes que navegan (ChatGPT, Claude y Perplexity cuando un usuario pega la URL o el agente la descubre). Es barato y no hace daño; no es la palanca principal. La palanca principal son los puntos 1 a 5 de la tabla de hallazgos.

### 4.3 Borrador completo de `llms.txt`

Reglas aplicadas: solo cifras de `datos.py` y `tools/pasto/data.py`; sin "gratis" ni "sin costo" salvo en la garantía de pasto; IVA correcto; secciones `##` solo con listas de enlaces; lo demás, antes del primer `##`. Las cifras de mensualidades y los precios por ciudad se conservan tal cual del archivo actual (salen de `tools/pasto/mensualidades.py` y `ciudades.py`; verifiqué las zonas de envío $900/$1,150/$1,400 y el mínimo de 25 m², no recalculé los porcentajes).

```markdown
# Viveros Terra

> Viveros Terra es un vivero y empresa de jardinería con sede en Ciudad Madero, Tamaulipas, México, fundada el 12 de diciembre de 2007. Atiende Tampico, Ciudad Madero y Altamira: vende e instala pasto San Agustín en rollo y pasto sintético, diseña jardines, instala riego automático, da mantenimiento a áreas verdes y vende plantas, palmas, árboles y materiales para jardín. Envía pasto sintético a todo México desde 2012.

Última actualización: 2026-11-09. Precios en pesos mexicanos (MXN), vigentes en 2026.

Regla de IVA: el pasto San Agustín sin instalar (menudeo y mayoreo) y las plantas, palmas y árboles no llevan IVA. Todos los demás precios de este archivo incluyen IVA.

Datos de la empresa:

- Nombre: Viveros Terra (también aparece como "Viveros Terra Tampico")
- Dirección única: Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamaulipas, México. Frente a Walmart, entrando por Banamex. Cualquier otra dirección publicada en directorios (por ejemplo en Tampico) está desactualizada.
- Coordenadas: 22.2777575, -97.8433341
- Google Maps: https://maps.app.goo.gl/xC4XGL2WeucAjGwAA
- Teléfono y WhatsApp: +52 833 326 8008
- Correo: viverosterra@hotmail.com
- Horario: lunes a viernes de 9:00 a 18:00; sábado de 9:00 a 14:00; domingo cerrado
- Respuesta por WhatsApp: en menos de 1 hora dentro del horario
- Registro REPSE (STPS): 773725, consultable en https://repse.stps.gob.mx/
- Facturación: CFDI 4.0
- Calificación: 4.6 en Google (24 reseñas)
- Trayectoria: +1,500 instalaciones de pasto, +900 clientes, +500,000 m² instalados, +200 sistemas de riego, +200 variedades de plantas
- Clientes empresariales: BMW, Taghleef Industries, Gobierno de Tampico, Grupo Velas, Velamar, Flex y Renault
- Perfiles oficiales: https://www.facebook.com/viverosterra/ · https://www.instagram.com/viverosterramx · https://www.tiktok.com/@viverosterra · https://www.youtube.com/@viverosterramx · https://www.linkedin.com/company/viveros-terra-tampico

Precios de referencia:

- Pasto San Agustín en rollo, solo el pasto: $85 por m² (no lleva IVA)
- Pasto San Agustín instalado: desde $120 por m², IVA incluido. Incluye preparación básica del terreno, colocación y garantía de arraigo
- Pasto San Agustín al mayoreo: desde $60 por m² en pedidos de 500 m² o más (no lleva IVA)
- Mantenimiento de jardines: desde $750 al mes en el plan residencial; planes premium y para empresas, según cotización
- Diseño de jardines (Plan Terra): Esencial $3,000, Completo $6,500, Premium $18,000. En Esencial y Completo el diseño se descuenta al contratar la obra; en Premium, en proyectos de más de $150,000
- Sistema de riego automático instalado: de $180 a $320 por m²; ahorra hasta 40% de agua
- Pasto sintético instalado en Tampico, Madero y Altamira: de $385 a $650 por m² con material y colocación; la preparación del terreno se cotiza aparte
- Pasto sintético con envío nacional: desde $139 por m² en rollo de 50 m²; envío de $900 (zona A), $1,150 (zona B) o $1,400 (zona C) por rollo; entrega en 3 a 5 días hábiles; pedido mínimo de 25 m²
- Poda de árboles y palmas: desde $500, según el tamaño y los residuos
- Palmas: areca y coco plumoso desde $250; palma real desde $500, en tamaño chico. El precio sube con la altura
- Flamboyán: desde $250. Las demás especies, según cotización
- Tierra negra vegetal: costal $90; tierra preparada, costal $100; a granel $1,500 por m³; camión de 5 m³ $3,500, de 8 m³ $5,200 y de 14 m³ $8,000
- Tezontle rojo: costal desde $200; m³ y camión, según cotización
- Mármol blanco: $250 el saco, IVA incluido, sujeto a disponibilidad
- Piedra bola de río: a granel, según cotización
- Materiales: sin mínimo de compra; la entrega a domicilio se cobra por viaje, según la colonia
- Nochebuenas 2026: maceta de 5" a $89 por pieza al menudeo y desde $65 en pedidos de 200 piezas o más

Condiciones que conviene citar tal cual:

- Garantía del pasto: si una sección no arraiga en 15 a 20 días, se repone sin costo, siguiendo el protocolo de riego
- Garantía de plantas: 30 días en las plantas que siembra el equipo de Viveros Terra, con el riego indicado. No cubre falta o exceso de riego, cambio de ubicación, daños por mascotas o terceros, ni clima extremo
- El primer riego del pasto lo hace el cliente; Viveros Terra explica cómo y entrega un protocolo de 20 días
- El pasto llega del campo una vez por semana, generalmente los viernes
- La visita para medir y cotizar tiene un costo que depende de la ubicación; se confirma por WhatsApp antes de agendar
- Para confirmar un pedido o agendar un servicio se solicita un anticipo; no se pide el 100% por adelantado
- Pago en mensualidades con tarjeta de crédito: 3, 6, 9 o 12 mensualidades; el precio en mensualidades es mayor que el de contado (+10.5% a +23.4% según el plazo) y el total se muestra antes de pagar. Desde $2,000 (3), $5,000 (6) y $15,000 (9 y 12)

Cobertura:

- Zona de servicio: Tampico, Ciudad Madero y Altamira, Tamaulipas
- Por proyecto: Pánuco, Pueblo Viejo, Tuxpan, Cd. Victoria y la Huasteca
- Pasto sintético: envío a todo México
- Pasto natural: no se envía fuera de la región

Lo que Viveros Terra no hace:

- No ofrece muestras físicas del pasto sintético; se elige con fichas técnicas y fotos
- No publica fechas de corte ni disponibilidad semanal del pasto
- No da precio de plantas sin conocer el tamaño, salvo los precios "desde" de esta lista

## Precios y empresa

- [Lista de precios 2026](https://www.viverosterra.com/precios): todos los precios vigentes en tablas, con la regla de IVA
- [Vivero en Tampico y Ciudad Madero](https://www.viverosterra.com/vivero-tampico): dirección, horario y cómo llegar
- [Políticas y garantías](https://www.viverosterra.com/politicas): garantía de pasto y de plantas, mensualidades, anticipos y devoluciones
- [Inicio](https://www.viverosterra.com/): resumen de servicios y cotizador por m²

## Pasto natural

- [Pasto San Agustín en rollo](https://www.viverosterra.com/pasto-en-rollo-tampico): precio por m², qué incluye la instalación, pasos y garantía de arraigo
- [Pasto al mayoreo](https://www.viverosterra.com/mayoreo-pasto-tampico): desde 500 m², entrega por etapas para obras y fraccionamientos
- [Protocolo de cuidados del pasto San Agustín](https://www.viverosterra.com/protocolo-cuidados-pasto-san-agustin): riego de los primeros 20 días
- [Cuándo plantar pasto en Tampico](https://www.viverosterra.com/blog/cuando-plantar-pasto-tampico-calendario): calendario mes a mes
- [San Agustín o japonés](https://www.viverosterra.com/blog/pasto-san-agustin-vs-japones): comparativa con tabla
- [Guía de instalación y mantenimiento](https://www.viverosterra.com/blog/pasto-san-agustin-instalacion-mantenimiento): del suelo al primer corte

## Servicios de jardín

- [Diseño de jardines](https://www.viverosterra.com/diseno-jardines-tampico): Plan Terra en tres niveles y qué entrega cada uno
- [Sistema de riego automático](https://www.viverosterra.com/sistema-riego-tampico): tipos de sistema, precio por m² y pasos de instalación
- [Mantenimiento de jardines](https://www.viverosterra.com/mantenimiento-jardines-tampico): planes, frecuencias y qué incluyen
- [Cuánto cuesta un jardín en Tampico](https://www.viverosterra.com/blog/cuanto-cuesta-jardin-tampico-precios): ejemplos de presupuesto con los precios oficiales

## Pasto sintético

- [Pasto sintético en Tampico](https://www.viverosterra.com/pasto-sintetico-tampico): venta en showroom e instalación local
- [Tienda con envío a todo México](https://www.viverosterra.com/pasto-sintetico): 9 modelos, fichas técnicas, cotizador y tabla de envío
- [Pasto sintético para perros](https://www.viverosterra.com/pasto-sintetico/perros): modelo, drenaje, olor y limpieza
- [Cuánto cuesta el pasto sintético en México](https://www.viverosterra.com/blog/cuanto-cuesta-pasto-sintetico-mexico): precios por modelo y por ciudad
- [Sintético o natural](https://www.viverosterra.com/blog/pasto-sintetico-vs-natural-tampico): comparativa para el clima de Tampico

## Plantas, palmas y árboles

- [Plantas, palmas y árboles](https://www.viverosterra.com/plantas-palmas-arboles-tampico): categorías del vivero
- [Catálogo](https://www.viverosterra.com/catalogo): +200 variedades con cotizador
- [Palmas tropicales](https://www.viverosterra.com/palmas-tropicales-tampico): especies y precios "desde"
- [Palmas al mayoreo para proyectos](https://www.viverosterra.com/palmas-mayoreo-proyectos): 12 especies con nombre científico
- [Árboles ornamentales](https://www.viverosterra.com/arboles-ornamentales-tampico): especies para jardín
- [Árboles para banqueta](https://www.viverosterra.com/arboles-para-banqueta-tampico): especies que no levantan el pavimento
- [Plantas para jardín](https://www.viverosterra.com/plantas-para-jardin-tampico): sol, sombra y cubresuelos
- [Plantas de interior](https://www.viverosterra.com/plantas-de-interior-tampico): especies para casa y oficina
- [Plantas resistentes a la sal del Golfo](https://www.viverosterra.com/blog/plantas-resistentes-sal-golfo-tampico): especies para Miramar y la costa
- [Nochebuenas 2026](https://www.viverosterra.com/post/nochebuenas-tampico-madero-mayoreo): precios por tamaño y por volumen

## Materiales

- [Tierra negra vegetal](https://www.viverosterra.com/tierra-negra-vegetal-tampico): costal, m³ y camión
- [Tezontle rojo](https://www.viverosterra.com/tezontle-rojo-tampico): usos y presentaciones
- [Mármol blanco](https://www.viverosterra.com/marmol-blanco-tampico): saco y usos
- [Piedra bola de río](https://www.viverosterra.com/piedra-bola-rio-tampico): venta a granel

## Zonas

- [Lomas de Rosales y Vista Hermosa](https://www.viverosterra.com/jardineria-lomas-de-rosales-tampico): jardinería en Tampico
- [Club Campestre y Country Club](https://www.viverosterra.com/jardineria-country-club-tampico): jardinería en Tampico
- [Águila, Altavista y Petrolera](https://www.viverosterra.com/jardineria-aguila-tampico): jardinería en Tampico
- [Lomas del Chairel y San Gerardo](https://www.viverosterra.com/jardineria-lomas-del-chairel-tampico): jardinería en Tampico
- [Ciudad Madero y Playa Miramar](https://www.viverosterra.com/jardineria-ciudad-madero): jardinería en Madero
- [Altamira y Lagunas de Miralta](https://www.viverosterra.com/jardineria-altamira): jardinería en Altamira

## Optional

- [Blog](https://www.viverosterra.com/blog): guías de jardinería para el clima de Tampico
- [Cómo proteger el jardín de los nortes](https://www.viverosterra.com/blog/nortes-tampico-proteger-plantas-jardin): frentes fríos
- [Jardín y temporada de huracanes](https://www.viverosterra.com/blog/temporada-huracanes-proteger-jardin-tampico): preparación y recuperación
- [Cuándo regar el pasto San Agustín](https://www.viverosterra.com/blog/cuando-regar-pasto-san-agustin-tampico): frecuencia por temporada
- [Aviso de privacidad](https://www.viverosterra.com/politica-privacidad): tratamiento de datos
```

Antes de publicar: confirmar que cada URL de blog existe en `public/blog/` (las tomé de `tools/site/contenido/blog/`), y que el precio de la nochebuena de 5" al menudeo ($89) sigue vigente (`datos.NOCHEBUENAS`).

---

## 5. JSON-LD para máquinas

### 5.1 Lo que ya existe [C]

- `@graph` en casi todas las páginas; `FAQPage` en 103 de 111.
- `Service` con `areaServed` como `Place` + `PostalAddress` y `Offer` con `UnitPriceSpecification` en las 6 páginas de zona.
- `OfferCatalog` con 12 ofertas y `seller → /#negocio` en `/precios`.
- `Product` + `AggregateOffer` + `OfferShippingDetails` + `MerchantReturnPolicy` en la tienda de sintético.
- `HowTo` en pasto en rollo, riego y mármol.
- Blog: `Article` con `publisher → /#negocio` y `author` como `Organization`.

### 5.2 Lo que falta

| Prioridad | Qué | Detalle |
|-----------|-----|---------|
| ALTO | Un solo `/#negocio` | Ver 2.3. Sustituir los `LocalBusiness` anónimos de `servicio.py` y `/vivero-tampico` por la referencia |
| ALTO | `WebSite` + `WebPage` en la home, en un solo `@graph` | `WebSite` (`@id` `/#sitio`, `publisher → /#negocio`, `inLanguage` `es-MX`) y `WebPage` (`@id` `/`, `about → /#negocio`, `isPartOf → /#sitio`, `mainEntity → FAQPage`, `dateModified`). Eliminar el `BreadcrumbList` de la home |
| ALTO | `WebPage` con `@id` en las páginas de servicio | Hoy `pasto-en-rollo`, `diseño`, `riego`, `mantenimiento`, `mayoreo` no tienen nodo `WebPage`. Sin él, `speakable`, `dateModified`, `about` y `mainEntity` no tienen dónde colgar |
| ALTO | `Service` completo en servicios | Hoy `/sistema-riego-tampico` y `/mantenimiento-jardines-tampico` tienen `Service` sin `offers` (riego) o sin `@id`. Patrón: `@id` `…#servicio`, `serviceType`, `provider → /#negocio`, `areaServed` con los tres `City`, `offers` con `UnitPriceSpecification` (`minPrice`/`maxPrice`, `unitText`, `valueAddedTaxIncluded`) |
| ALTO | `valueAddedTaxIncluded` en cada `UnitPriceSpecification` | `false` en pasto solo, mayoreo y plantas; `true` en lo demás. Es la forma estructurada de resolver la contradicción de 3.2 |
| MEDIO | `speakable` bien puesto | Moverlo dentro del `WebPage` (`"speakable": {...}`), no como nodo suelto. Selectores: `.vt-respuesta` y `.vt-faq details p` (las respuestas), no `h2` |
| MEDIO | `dateModified` en todas las páginas con precio | Tomado de la constante de `datos.py`. `priceValidUntil: "2026-12-31"` en todas las `Offer` con precio fijo (hoy solo en una) |
| MEDIO | Pasto en rollo: dos ofertas, no una | Hoy `Product` con una `Offer` de $85. Añadir la instalada como `Service` u `Offer` con `minPrice` 120 y la de mayoreo con `eligibleQuantity` (`minValue` 500, `unitCode` `MTK`) |
| MEDIO | `about` / `mentions` en el blog | `about` → `Thing` con `name` y `sameAs` a Wikipedia/Wikidata de la especie (por ejemplo *Stenotaphrum secundatum*, Q-id en Wikidata). `mentions` → `/#negocio` y el `Service`/`Product` relacionado por `@id` |
| MEDIO | Autor del blog | `author`: `{"@type": "Organization", "@id": ".../#equipo-tecnico", "name": "Equipo técnico de Viveros Terra", "parentOrganization": {"@id": ".../#negocio"}}`. Credenciales reales y verificables que ya existen: fundación en 2007, REPSE 773725, +1,500 instalaciones. No añadir títulos ni personas que no se puedan comprobar |
| MEDIO | Artículos de abril | 8 `Article` sin `dateModified`, `image` ni `mainEntityOfPage` |
| MEDIO | `HowTo` | Añadir a mantenimiento (qué pasa en una visita) y a pasto sintético (instalación). Google ya no muestra el resultado enriquecido, pero el marcado sigue describiendo pasos ordenados a cualquier parser |
| BAJO | `Product` de la tienda: `seller → /#negocio` | Sustituir las 9 `Organization` anónimas |
| BAJO | `GeoCircle` o `GeoShape` en `areaServed` | Opcional; con los tres `City` basta |

No recomiendo añadir `aggregateRating` propio al `LocalBusiness`: Google no lo acepta en reseñas que el negocio publica de sí mismo y `datos.py` ya lo prohíbe.

---

## 6. Rastreo por bots de IA

### 6.1 Resultados [C]

Peticiones GET con `curl --compressed` y el user-agent de cada bot, 2026-11-10 05:25 UTC. Bytes comprimidos; TTFB en segundos.

| Ruta | GPTBot | OAI-SearchBot | ChatGPT-User | ClaudeBot | PerplexityBot | Googlebot | Bingbot | Navegador |
|------|--------|---------------|--------------|-----------|---------------|-----------|---------|-----------|
| `/` | 200 · 12,632 · 0.28 | 200 · 0.32 | 200 · 0.29 | 200 · 0.28 | 200 · 0.28 | 200 · 0.40 | 200 · 0.27 | 200 · 0.28 |
| `/pasto-en-rollo-tampico` | 200 · 14,550 · 0.28 | 200 · 0.29 | 200 · 0.29 | 200 · 0.44 | 200 · 0.27 | 200 · 0.40 | 200 · 0.27 | 200 · 0.28 |
| `/precios` | 200 · 9,747 · 0.32 | 200 · 0.29 | 200 · 0.29 | 200 · 0.29 | 200 · 0.28 | 200 · 0.42 | 200 · 0.27 | 200 · 0.27 |
| `/llms.txt` | 200 · 3,758 · 0.41 | 200 · 0.27 | 200 · 0.27 | 200 · 0.29 | 200 · 0.27 | 200 · 0.35 | 200 · 0.26 | 200 · 0.28 |

- Mismo tamaño para todos los agentes: no hay bloqueo, reto ni contenido distinto por user-agent.
- **Sin dependencia de JavaScript**: el HTML crudo de las tres páginas contiene los precios ($85, $120), la dirección y el JSON-LD. Home: unas 2,200 palabras de texto en el HTML servido.
- Cabeceras: `content-type: text/html; charset=utf-8`, `strict-transport-security`, `x-vercel-cache: HIT`, `etag`, sin `X-Robots-Tag`. `<html lang="es-MX">`.
- Google-Extended no tiene user-agent propio: es una directiva de `robots.txt` que rastrea Googlebot. La columna "Googlebot" lo cubre; `robots.txt` lo permite.
- Limitación de la prueba: suplanté el user-agent desde mi IP. Si el cortafuegos de Vercel tuviera una regla por IP o por ASN de los bots reales, esta prueba no la detecta. No hay indicio de que exista (no hay `vercel.json` con reglas de firewall), pero la confirmación definitiva son los registros de Vercel (sección 9).

### 6.2 Observaciones

| Prioridad | Observación |
|-----------|-------------|
| MEDIO | `last-modified` es la hora del despliegue (cambió a 05:24:43 con un despliegue de hace minutos). Todas las páginas parecen "modificadas" en cada push, así que la cabecera no sirve como señal de frescura. La señal fiable tiene que ir en el HTML (`<time>`) y en `dateModified` |
| BAJO | `https://viverosterra.com/` → `https://www.viverosterra.com/` con **307** (temporal). Debe ser 308. Se cambia en el panel de dominios de Vercel |
| BAJO | `content-disposition: inline; filename="pasto-en-rollo-tampico"`: inofensivo |
| BAJO | `/llms-full.txt`, `/index.md`, `/.well-known/ai.txt`: 404 (esperado) |
| BAJO | Sitemap: 108 URL con `lastmod` (41 con 2026-09-26). Sin extensión de imágenes |
| Bien | `robots.txt` nombra a OAI-SearchBot, ChatGPT-User, GPTBot, Claude-SearchBot, Claude-User, ClaudeBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, Bingbot y CCBot. Falta solo, por completitud, `meta-externalagent`, `Amazonbot` y `DuckAssistBot`; con `User-agent: * Allow: /` ya están permitidos |

---

## 7. Autoridad citada (GEO)

### 7.1 Qué citan hoy los buscadores en este nicho [C]

Diez consultas con la herramienta de búsqueda (índice de EE. UU., modo estándar; no es Google México ni reproduce lo que ve un usuario en Tampico).

| Consulta | Fuentes que respondieron | ¿Viveros Terra? |
|----------|--------------------------|-----------------|
| "Viveros Terra" Tampico Ciudad Madero vivero | Cosmos, Sección Amarilla, Milenio | Solo vía Cosmos, sin dirección fiable |
| vivero en Tampico plantas palmas pasto | **Cronoshare (ficha de Viveros Terra)**, Cosmos, Milenio, Habitissimo | Sí, primer resultado, pero por la ficha de Cronoshare, no por el sitio |
| precio pasto en rollo Tampico por m2 | Cronoshare ("$30–$70/m² material, $100–$135 instalado"), Habitissimo ("$140/m²") | No. La respuesta dijo: "No encontré un precio por m² específico para Tampico" |
| cuánto cuesta el pasto San Agustín por m2 instalado México 2026 | sensorautomotriz.com ("$155/m²"), Habitissimo | No |
| pasto sintético Tampico venta instalación precio m2 | **Cosmos (Viveros Terra, "Faja de Oro 805")**, Habitissimo, Mercado Libre | Sí, con la dirección vieja y sin precio |
| mejores viveros en Tampico Madero Altamira | Nada útil (Airbnb, inmuebles) | No. La respuesta recomendó "buscar en Google Maps" |
| "viverosterra" pasto jardinería Tampico | Cronoshare, Cosmos | Sí, sin enlace al sitio |

Conclusiones:
- **[C]** El sitio propio no fue fuente en ninguna consulta. La pregunta "precio pasto en rollo Tampico" quedó sin respuesta local: el hueco existe y `/precios` tiene exactamente el dato que falta.
- **[C]** Los agregadores de cotizaciones (Habitissimo, Cronoshare) son los que alimentan las respuestas de precio en México, con rangos nacionales sin fecha.
- **[I]** La causa probable de la ausencia del sitio no es técnica (el rastreo funciona), sino de autoridad e indexación en índices distintos de Google: casi no hay enlaces de terceros hacia `viverosterra.com` (Cronoshare ni siquiera publica la URL). ChatGPT usa el índice de Bing; Copilot también. No pude comprobar si Bing tiene indexado el sitio: verificarlo en Bing Webmaster Tools es el primer paso.

### 7.2 Fuentes que pesan para un negocio local, en orden

| # | Fuente | Por qué | Estado | Acción |
|---|--------|---------|--------|--------|
| 1 | **Google Business Profile** | Es la fuente de Gemini y de AI Overviews para "cerca de mí" y "vivero en Tampico". 24 reseñas es poco para la categoría | Existe | Revisar categoría principal (Vivero / Centro de jardinería) y secundarias (Paisajista, Tienda de césped), servicios con precio, productos, descripción con las tres ciudades, fotos nuevas, publicaciones semanales, preguntas y respuestas sembradas con las 6 FAQ de la home. Pedir reseña a cada cliente al cerrar la obra: meta realista, 60 reseñas en 6 meses |
| 2 | **Bing Places + Bing Webmaster Tools** | Alimenta ChatGPT Search y Copilot. Se importa desde Google en minutos | No comprobado | Reclamar la ficha, importar desde GBP, enviar el sitemap, activar IndexNow |
| 3 | **Cosmos** | Es el directorio que más salió y tiene la dirección vieja | **Incorrecto** | Corregir la dirección a Obregón 209 Sur, Cd. Madero, y añadir teléfono. Es la corrección externa más urgente |
| 4 | **Apple Business Connect** | Siri y Apple Maps | No comprobado | Reclamar |
| 5 | **Cronoshare, Habitissimo** | Son las fuentes de precio que citan los modelos | Cronoshare existe, incompleta | Completar Cronoshare (teléfono, web, quitar "diseños gratuitos"). Crear perfil en Habitissimo con los mismos datos |
| 6 | **Sección Amarilla, Foursquare, Yelp MX, Infobel, Waze, Facebook (pestaña Información)** | Consistencia de NAP; Foursquare alimenta a varios proveedores de datos de mapas | No comprobado | Alta o corrección con el NAP exacto de `datos.py`. Buscar aquí "Obregón 601" |
| 7 | **YouTube** | Gemini y AI Overviews citan vídeo con frecuencia en consultas de "cómo" | Canal existe | 6–8 vídeos cortos con título en forma de pregunta ("¿Cuánto cuesta el pasto San Agustín en Tampico?"), descripción con la respuesta de 50 palabras, la dirección y el enlace a la página. Capítulos y subtítulos en español |
| 8 | **Prensa local** | Milenio Tamaulipas ya publica sobre viveros; El Sol de Tampico, Expreso, Milenio. Una nota con nombre, dirección y cifra es la mención de mayor peso que puede conseguir un negocio local | Sin menciones encontradas | Dos ganchos reales: temporada de Nochebuenas (ahora) y "cuándo plantar pasto antes de los nortes". Ofrecer el dato y un portavoz, no un anuncio |
| 9 | **Wikidata** | Identificador que usan los grafos de conocimiento | No existe | Crear el elemento cuando haya al menos dos fuentes independientes (nota de prensa + padrón REPSE). Sin fuentes lo borran. Wikipedia no: no hay notabilidad |
| 10 | **LinkedIn de empresa** | Entidad B2B; hoy no la puedo leer sin sesión | Existe | Completar dirección, sitio y REPSE; publicar los proyectos con clientes que ya dieron permiso (BMW, Taghleef, etc.) |
| 11 | **Clientes y proveedores** | Enlace con contexto desde un sitio real de la zona | Sin comprobar | Pedir a constructoras y arquitectos clientes una mención en su página de proveedores o de proyecto |
| 12 | **Reddit, foros, grupos de Facebook** | Perplexity y Google citan Reddit; en Tampico la conversación está en grupos de Facebook, que los bots no leen | — | Bajo retorno. Responder con nombre real cuando alguien pregunte en r/Tampico o r/mexico; nada de cuentas falsas |

### 7.3 Plan de menciones realista

- **Semanas 1–2**: corregir Cosmos; completar Cronoshare; Bing Places y Bing Webmaster; Apple Business Connect; revisar GBP de punta a punta. Hoja de cálculo con cada ficha, su URL, el NAP que muestra y la fecha de corrección.
- **Semanas 3–6**: Habitissimo, Sección Amarilla, Foursquare, Waze; rutina de reseñas en Google (mensaje de WhatsApp al cerrar cada instalación); primeros 3 vídeos.
- **Meses 2–3**: nota de prensa local con la temporada de Nochebuenas o el calendario de siembra; LinkedIn con proyectos; menciones de 3 clientes B2B.
- **Meses 4–6**: Wikidata si ya hay fuentes; segunda nota; revisar la tabla de consultas de prueba.

---

## 8. Contenido propio que los modelos citan

Los modelos citan datos concretos, fechados y con unidad que no están en otra parte. El sitio ya tiene varios y puede publicar más sin inventar nada.

| Prioridad | Pieza | Con qué se hace | Estado |
|-----------|-------|-----------------|--------|
| ALTO | **Tabla de precios por m² con fecha y regla de IVA** | `datos.PRECIOS`. Ya existe en `/precios` (6 tablas) | Falta la fecha visible, `<caption>`, `dateModified` y un párrafo que la presente como "lista oficial de Viveros Terra para Tampico, Madero y Altamira". Es la respuesta a la consulta que hoy nadie contesta |
| ALTO | **Calculadora de pasto**: m² → costo solo, instalado y mayoreo; tepes necesarios (un tepe mide 40 × 60 cm = 0.24 m², unos 4.2 tepes por m²) | `datos.PRECIOS` y la medida del tepe que ya publica la página | La home tiene cotizador en JS. Añadir bajo él una tabla estática con ejemplos (50, 100, 200, 500 m²) para que el dato exista sin ejecutar JS |
| ALTO | **Calculadora de tierra negra**: m³ = m² × espesor. La página ya dice "3 a 5 cm de tierra negra" | `datos.PRECIOS` (m³ $1,500; camiones 5/8/14 m³) | Tabla estática: 100 m² a 3 cm = 3 m³; a 5 cm = 5 m³ = un camión de $3,500 |
| MEDIO | **Calendario de siembra para Tampico** | Ya existe: `/blog/cuando-plantar-pasto-tampico-calendario`, con tabla y respuesta directa | Falta enlazarlo desde `/pasto-en-rollo-tampico` con una frase resumen y revisar `dateModified` (2026-05-15). La afirmación "temperatura de 28 °C" necesita fuente (normales del SMN) o quitarse |
| MEDIO | **Guía de especies tolerantes a salitre** | Ya existe: `/blog/plantas-resistentes-sal-golfo-tampico`, con tabla | Cruzarla con `catalogo_especies.json`: marcar en la tabla cuáles tiene el vivero y enlazar cada una. Una tabla "especie · nombre científico · tolerancia · sol/sombra · disponible en Viveros Terra" es muy citable |
| MEDIO | **Tabla de palmas con nombre científico y precio "desde"** | `datos.PALMAS_PROYECTO` (12 especies) | Ya está en `/palmas-mayoreo-proyectos`. Resolver antes el conflicto de la kerpis |
| MEDIO | **Protocolo de riego de 20 días** como tabla día por día | `/protocolo-cuidados-pasto-san-agustin.html` (880 palabras, sin JSON-LD) | Añadir `HowTo` y `WebPage`; es contenido único |
| MEDIO | **Tabla de envío de pasto sintético por estado** | `tools/pasto/data.py` (`ZONAS`) y `ciudades.py` | Ya existe. Añadir `<caption>` con fecha |
| BAJO | **Cifras propias agregadas** ("+1,500 instalaciones desde 2007", "+500,000 m²") | `datos.py` | Ya se publican. Ganarían con el año de corte: "a noviembre de 2026" |
| BAJO | **Qué pasto para qué uso** (San Agustín / japonés / Bermuda) en tabla | Ya en el blog | Bien resuelto |

**Conflicto a resolver antes de publicar más sobre palmas [C]**: `datos.PALMAS_PROYECTO` dice "Palma kerpis — *Hyophorbe lagenicaulis*"; el artículo `/blog/palma-kerpis-howea-forsteriana-tampico` dice "Palma Kerpis (*Howea forsteriana*, también llamada Kentia)". Son dos especies distintas (palma botella y kentia). En el comercio mexicano "kerpis" suele ser *Adonidia merrillii* **[I]**: hay que preguntarle al dueño qué planta vende con ese nombre y unificar. Un modelo que cruce las dos páginas verá un vivero que no sabe qué vende.

Lo que no conviene publicar: rangos de precio "del mercado" o comparativas con competidores sin fuente, cifras de ahorro o de retorno sin respaldo (`datos.py` ya veta "se amortiza en 18–24 meses"), y temperaturas o lluvias sin citar al SMN o a CONAGUA.

---

## 9. Medición sin herramientas de pago

### 9.1 Consultas de prueba fijas

Quince consultas, las mismas siempre, una vez al mes (primer lunes), en ventana privada y sin sesión cuando se pueda. Motores: ChatGPT (con búsqueda), Perplexity, Gemini, Copilot, Google (AI Overview) y Claude (con búsqueda).

| # | Consulta | Tipo |
|---|----------|------|
| 1 | Viveros Terra Tampico | Marca |
| 2 | ¿Cuál es la dirección y el horario de Viveros Terra? | Marca / NAP |
| 3 | ¿Viveros Terra tiene REPSE? | Marca / B2B |
| 4 | vivero en Tampico | Categoría |
| 5 | mejores viveros en Ciudad Madero | Categoría |
| 6 | ¿dónde comprar pasto en rollo en Tampico? | Categoría |
| 7 | precio del pasto en rollo en Tampico por m2 | Precio |
| 8 | ¿cuánto cuesta el pasto San Agustín instalado por m2? | Precio (nacional) |
| 9 | ¿cuánto cuesta instalar pasto sintético en Tampico? | Precio |
| 10 | pasto sintético con envío a Monterrey precio | Precio (nacional) |
| 11 | ¿cuánto cuesta un sistema de riego automático en Tampico? | Precio |
| 12 | jardinero en Tampico mantenimiento mensual precio | Precio |
| 13 | ¿cuál es el mejor mes para plantar pasto en Tampico? | Informativa |
| 14 | plantas que aguantan el salitre en Tampico | Informativa |
| 15 | proveedor de pasto al mayoreo para fraccionamiento en Altamira | B2B |

Por cada consulta y motor se anota:
- **Mención** (0/1): ¿nombra a Viveros Terra?
- **Cita** (0/1): ¿enlaza `viverosterra.com`? ¿Qué URL?
- **Exactitud**: precio correcto / incorrecto / ausente; dirección correcta / vieja / ausente.
- **Otras fuentes citadas** (dominios): así se ve quién gana y dónde conviene estar.
- Captura de pantalla con fecha.

Las respuestas de los modelos varían entre ejecuciones: una sola medida no significa nada, la tendencia de tres meses sí.

### 9.2 Registros de bots en Vercel

- Panel de Vercel → Observability → Logs, filtro por user-agent: `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-User`, `Claude-SearchBot`, `PerplexityBot`, `Perplexity-User`, `bingbot`, `Googlebot`, `Applebot`.
- La distinción que importa: `GPTBot` y `ClaudeBot` son rastreo para entrenamiento; `ChatGPT-User`, `Claude-User` y `Perplexity-User` son **una persona preguntando en ese momento** y el asistente abriendo la página. Esas visitas son la medida más directa de visibilidad en IA.
- El plan gratuito retiene los registros pocas horas. Opciones sin costo: revisar el mismo día cada semana, o un *log drain* hacia una hoja de cálculo mediante Apps Script (el repo ya tiene `apps-script/`). Vale como muestra, no como censo.
- Anotar por semana: peticiones por bot, URL más pedidas, códigos distintos de 200.

### 9.3 Referidos en GA4

`GA4_ID` = G-RMZCVJ734M.

- Exploración → dimensión "Fuente de la sesión" con filtro de expresión regular:
  `chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|bing\.com/chat|you\.com|phind\.com|duckduckgo\.com`
- Crear un grupo de canales personalizado "Asistentes de IA" con esa misma regla, por encima de "Referral", para que salga en todos los informes.
- ChatGPT añade `utm_source=chatgpt.com` a los enlaces: filtrar también por ese parámetro.
- Métricas: sesiones, página de entrada y clics en WhatsApp (el evento que ya mide `medicion_js.py`).
- Límite: buena parte del tráfico desde aplicaciones móviles llega sin referente y cae en "Directo". GA4 mide el suelo, no el total.

### 9.4 Tablero mínimo

Una hoja de cálculo, una fila por mes.

| Indicador | Fuente | Hoy |
|-----------|--------|-----|
| Consultas con mención (de 15 × 6) | Prueba manual | Sin línea base en los motores reales; en mi prueba de buscador, 3 de 7 con mención y 0 con cita del sitio |
| Consultas con cita de `viverosterra.com` | Prueba manual | 0 |
| Respuestas con precio correcto | Prueba manual | 0 |
| Respuestas con dirección vieja | Prueba manual | 1 (Cosmos) |
| Sesiones desde asistentes de IA | GA4 | Sin medir |
| Clics a WhatsApp desde esas sesiones | GA4 | Sin medir |
| Visitas de `ChatGPT-User` + `Claude-User` + `Perplexity-User` | Vercel | Sin medir |
| Páginas indexadas en Bing | Bing Webmaster | Sin medir |
| Reseñas en Google y calificación | GBP | 24 · 4.6 |
| Fichas externas con NAP correcto / total | Hoja de fichas | 1 de 2 revisadas |
| Menciones de prensa o de terceros con enlace | Manual | 0 encontradas |

---

## 10. Plan de acciones, en orden

### Fase 1 — Correcciones de exactitud (1 a 2 días de trabajo en el repo)

1. **IVA**: corregir `datos.RESPUESTA_PRECIO_PASTO`, el primer párrafo de `/mayoreo-pasto-tampico` y `llms.txt`. Añadir `valueAddedTaxIncluded` a las ofertas. Prueba que impida "con IVA" junto a $85 o $60.
2. **`llms.txt`**: sustituir por el borrador de 4.3 y, enseguida, generarlo desde `datos.py` en `build.py`.
3. **`/#negocio`**: nodo completo de 2.3 en la home, con `sameAs` desde `datos.REDES` + `MAPS_URL` y `identifier` del REPSE.
4. **Quitar los `LocalBusiness` anónimos** de `servicio.py` y `/vivero-tampico`; referenciar `/#negocio`. Prueba que lo vigile.
5. **Palma kerpis**: preguntar al dueño y unificar el nombre científico.

### Fase 2 — Corregir lo de fuera (1 semana, sin código)

6. Corregir la ficha de **Cosmos** (Faja de Oro 805 → Obregón 209 Sur, Cd. Madero).
7. Completar **Cronoshare** (teléfono, web, quitar "diseños gratuitos").
8. **Bing Webmaster Tools + Bing Places**; enviar sitemap; comprobar indexación.
9. Revisión completa de **Google Business Profile** y arranque de la rutina de reseñas.
10. Apple Business Connect; hoja de fichas con NAP.
11. Cambiar el 307 del dominio sin `www` a 308 en Vercel.

### Fase 3 — Respuestas extraíbles (2 a 3 días en el repo)

12. Párrafo de respuesta (`.vt-respuesta`) en las 10 páginas de 3.3.
13. Constante `PRECIOS_ACTUALIZADOS` en `datos.py`; `<time>` visible y `dateModified` en `/precios` y servicios; `priceValidUntil` en todas las ofertas.
14. `WebSite` + `WebPage` en la home; `WebPage` con `@id` en las páginas de servicio; `speakable` dentro del `WebPage` y apuntando a las respuestas.
15. `Service` con `@id`, `areaServed` y `offers` en riego, mantenimiento, diseño y pasto en rollo.
16. Completar los 8 `Article` de abril; `@id` del autor; `about` y `mentions`.

### Fase 4 — Contenido citable (2 a 4 semanas)

17. `<caption>` con fecha en las tablas de precios y de envío.
18. Tablas estáticas de cálculo (pasto y tierra negra) bajo los cotizadores.
19. `HowTo` + `WebPage` en el protocolo de 20 días.
20. Cruzar la guía de salitre con el catálogo.
21. `llms-full.txt` y `.md` de las 20 páginas clave, generados en el build, con `noindex` por cabecera.

### Fase 5 — Autoridad y medición (continuo)

22. Línea base de las 15 consultas en los 6 motores, antes de publicar la Fase 3, para poder comparar.
23. Canal "Asistentes de IA" en GA4 y revisión semanal de bots en Vercel.
24. Habitissimo, Sección Amarilla, Foursquare, Waze.
25. Tres vídeos de YouTube con título-pregunta.
26. Nota de prensa local (Nochebuenas o calendario de siembra).
27. LinkedIn con proyectos B2B; menciones de clientes.
28. Wikidata cuando existan dos fuentes independientes.

---

## 11. Lo que no pude comprobar

- El contenido de la ficha de Google Business Profile (categorías, horario, fotos, preguntas): el enlace corto responde 200 pero no se lee sin navegador.
- Facebook y LinkedIn: 400 y 403 sin sesión.
- Dónde sigue publicado "Obregón 601": no apareció en ninguna búsqueda.
- Si Bing tiene indexado el sitio y cuántas páginas.
- Cómo responden hoy ChatGPT, Perplexity, Gemini y Copilot a las 15 consultas: usé un buscador con índice de EE. UU., no esos productos. La tabla 7.1 es un indicio, no la línea base.
- Si los bots reales (por IP) reciben lo mismo que mi prueba con el user-agent suplantado.
- Los porcentajes de mensualidades y los precios por ciudad del sintético: los conservé del `llms.txt` actual sin recalcularlos.
- El commit `d3980cb` de `origin/main` (fotos de Nochebuenas y mármol) no está en la copia local que leí; los tres HTML que comparé con producción coinciden.

## 12. Fuentes externas consultadas

- https://www.cosmos.com.mx/empresa/viveros-terra-dsc4.html
- https://www.cosmos.com.mx/producto/pasto-en-rollo-g3p3/
- https://www.cosmos.com.mx/producto/plantas-de-sol-y-sombra-43sn/
- https://www.cosmos.com.mx/producto/pasto-sintetico-4gfw/
- https://www.cronoshare.com.mx/croner-584253-viveros-terra-tampico
- https://www.cronoshare.com.mx/cuanto-cuesta/poner-rollos-pasto
- https://www.habitissimo.com.mx/presupuesto/poner-pasto-en-rollo
- https://www.habitissimo.com.mx/presupuesto/jardineros/tamaulipas/tampico
- https://www.habitissimo.com.mx/presupuesto/poner-pasto-sintetico
- https://sensorautomotriz.com/preguntas-frecuentes/cuanto-cobra-un-instalador-de-cesped
- https://www.seccionamarilla.com.mx/resultados/viveros/7
- https://www.milenio.com/temas/viveros
- https://repse.stps.gob.mx/ (200) y https://repse.stps.gob.mx/Publico (404)
- https://llmstxt.org/ (formato de referencia)
