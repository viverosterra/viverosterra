# Etapa de fotos reales: revelado, limpieza y colocación

Fecha: 2026-11-08 · Estado: enfoque "revelado + limpieza" elegido por el dueño; guía de estilo pendiente de aprobación.

## Objetivo

Sumar al sitio fotos propias de Viveros Terra, tomadas entre 2013 y 2026 con varios iPhone, con un tratamiento
homogéneo y de alta calidad, para reforzar la promesa "Fotos de obra, no de catálogo".

## Insumos

- 88 archivos, 224.8 MB, copiados a `~/viveros-terra-fotos/originales/`. Descargas no se modifica.
- Los originales y las versiones maestras viven fuera del repo. Al repo solo entran WebP finales.
- 53 fotos con lado mayor de 4000 px o más; 20 con menos de 1600 px; 49 con GPS.

## Reglas

1. **Nada inventado.** El revelado solo corrige la imagen. La limpieza con IA solo retira objetos ajenos a la obra
   (mangueras, basura, herramienta olvidada); no agrega plantas, pasto, cielo ni arquitectura.
2. **Procedencia.** Las imágenes con marca de IA (`pomelli_photoshoot-1`, `Del rancho a tu jardin 6`) no se publican
   como obra real. `lirio persa`, `lirio persa monton` y `4.png` quedan fuera hasta que el dueño confirme su origen.
3. **Privacidad.** Toda salida se guarda sin EXIF, y por lo tanto sin GPS. Clientes y domicilios identificables
   requieren permiso del dueño.
4. **Marcas de terceros.** Se recortan o se publican con permiso (ejemplo: Carl's Jr. en `IMG_4144`).
5. **Pies `FIG.`.** Lugar y etapa los confirma el dueño; no se deducen de la imagen.
6. **Publicación.** Ninguna foto se publica sin aprobación en la galería de antes y después.

## Guía de estilo (revelado)

Objetivos medidos en 10 imágenes actuales del sitio, en espacio Lab:

| Medida | Objetivo |
|---|---|
| Luminosidad mediana | acercar 60 % hacia L 50 |
| Tono del verde | acercar 45 % hacia 119° |
| Croma del verde | comprimir por encima de 42 |
| Cielo | anclar a 262° solo en la parte alta, croma comprimido por encima de 34 |
| Neutros (muros, concreto, nubes) | a neutro apenas cálido, b +2.5 |

Las flores y las hojas moradas conservan su color. El balance no usa el follaje como referencia.

## Flujo

1. `herramientas/revelar.py` aplica una receta por foto (`giro`, `fuga`, `recorte`, `ruido`, `sombras`, `altas`,
   `claridad`) definida en un JSON.
2. Ficha por foto: contenido, obra, sección, calidad, recorte y si necesita limpieza.
3. Revelado por lote a un máximo de 2400 px, sin ampliar las fotos chicas.
4. Limpieza local y gratuita con LaMa (IOPaint) en 10 a 15 fotos clave, sin enviar fotos a servicios externos. Se
   marca solo el objeto a retirar y `verificar_limpieza.py` confirma que nada cambió fuera de esa zona.
5. Galería de aprobación con antes y después.
6. Integración en una etapa propia: WebP de hasta 1200 px, `activos.json`, plantillas y pies `FIG.`.

## Colocación preliminar

| Sección | Fotos |
|---|---|
| Catálogo y vivero | 26 |
| Diseño de jardines | 21 |
| Pasto en rollo y áreas verdes de empresas | 17 |
| Pasto sintético | 7 |
| Riego | 6 |
| Mantenimiento y poda | 2 |
| Nosotros | 2 |
| Descartar o confirmar | 7 |

La primera sustitución son las 24 fotos con marca de agua registradas en `FOTOS_POR_REVISAR`, cuando exista la especie
correcta entre las fotos propias. Los renders actuales salen de forma gradual o conservan su pie de referencia.

## Criterios de terminado

- Cada foto publicada tiene aprobación, pie confirmado, `alt` descriptivo y cero metadatos.
- Ningún render o imagen generada aparece como obra real.
- Las páginas tocadas cumplen `width`/`height`, `lazy` y el presupuesto de rendimiento de la Etapa 5.

## Fuera de alcance

Generar fotos nuevas con IA, ampliar artificialmente las fotos chicas y sustituir la sesión de fotos real recomendada
en la mejora integral.
