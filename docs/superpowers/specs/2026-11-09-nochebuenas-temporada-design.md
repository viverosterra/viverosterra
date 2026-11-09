# Página de temporada de Nochebuenas: diseño

Fecha: 2026-11-09. Fuente: prompt del dueño del 2026-11-09 y sus respuestas del mismo día. Rama: `feat/nochebuenas`, desde
`main` e independiente de la etapa 2i.

## 1. Objetivo

Publicar en `https://www.viverosterra.com/post/nochebuenas-tampico-madero-mayoreo` una página permanente que informe,
cotice por volumen y lleve el pedido a WhatsApp, con un registro de cada clic de envío en Google Sheets. La URL se reutiliza
cada año: nunca se borra, redirige ni lleva noindex.

## 2. Arquitectura

Página generada por el build de `tools/site/`, con plantilla y hoja de estilos propias. Sin frameworks ni dependencias.

**Fuente única.** El bloque `NOCHEBUENAS` de `datos.py` sustituye al `NB_CONFIG` del prompt, con los mismos valores:
`temporada` 2026, `modo` "temporada", `cortes` (1, 12, 50, 200), `nombres_escalon` (Menudeo, Mayoreo, Mayoreo Plus, Proyecto),
`productos`, `variedades` (Roja, Rosa, Jaspeada), `entrega_incluida_desde` 3500, `preventa` (5%, hasta 2026-11-20, hasta el
escalón índice 2, es decir, nunca Proyecto), `fecha_limite_mayoreo` 2026-11-30 y `ultima_actualizacion` 2026-11-08.

| Producto | Menudeo | Mayoreo | Mayoreo Plus | Proyecto |
|---|---|---|---|---|
| Maceta 5" | 89 | 75 | 69 | 65 |
| Maceta 6" | 139 | 119 | 109 | 105 |
| Maceta 7" | 199 | 169 | 155 | 149 |
| Colgante | 339 | 279 | 259 | 249 |
| Macetón 12" (sobre pedido) | 1195 | 995 | 899 | 865 |

El build usa ese bloque para la tabla estática, el JSON-LD, los metadatos y un JSON incrustado que lee el cotizador. El
modo se decide al construir, porque también cambia HTML y schema: cambiarlo requiere publicar. Los precios son finales y
las plantas no llevan IVA: nunca aparece "con IVA" en esta página.

## 3. Reglas de cálculo (`public/js/vt-nochebuenas.js`, funciones puras con `node --test`)

1. Piezas = suma de todas las líneas. Escalón = el mayor corte alcanzado. Todas las líneas se recalculan a ese escalón.
2. Total, subtotal por línea, escalón y "Ahorras $X vs. menudeo".
3. **Nudge**: si faltan 4 piezas o menos para el siguiente corte. Las piezas faltantes se calculan con el producto de la
   última línea: "Te faltan 2 piezas para precio Mayoreo: por $38 más te llevas 12 y ahorras $240". El ahorro compara las
   piezas objetivo a precio actual contra precio siguiente. Si el pedido completo resulta más barato, dice "y pagas $X menos".
4. **Preventa**: fecha de America/Mexico_City ≤ 2026-11-20 inclusive y escalón ≤ 2: −5% sobre el total, redondeado al peso,
   con la etiqueta "Precio preventa: apartando con 50% de anticipo". El 50% se publica solo en esta página y por indicación
   del dueño.
5. **Entrega**: total final ≥ $3,500 en Tampico, Madero o Altamira: "Entrega incluida". Debajo: "Te faltan $X para entrega
   incluida. Entrega según tu ubicación o colonia; te la cotizamos por WhatsApp." Con "Recojo en vivero" no se muestra.
6. Macetón: "Sobre pedido · sujeto a disponibilidad". 200 piezas o más: "Precio proyecto: te confirmamos disponibilidad y
   fecha de entrega".
7. Casos obligatorios: 10×6" = $1,390 con nudge de 2 piezas; 12×6" = $1,428; 16×6" + 4×7" + 6 colgantes = $4,254 en Mayoreo
   (sin preventa).

**Envío.** En el mismo clic: `navigator.sendBeacon` en `text/plain` al endpoint, sin esperar respuesta, y apertura de
`wa.me` con el mensaje del prompt. Si la preventa aplica, el mensaje lo indica. Endpoint vacío, ausente o con error: WhatsApp
abre igual y no se avisa al cliente. No se piden nombre ni teléfono.

**Medición.** GA4: `nb_cotizador_uso`, `nb_nudge_visto` y `nb_whatsapp_click` (total y escalón), sin perder la conversión
actual de WhatsApp (`VTMedicion`).

## 4. Contenido, en este orden

1. **Hero**: etiqueta "Temporada 2026 · Pedidos abiertos", H1 "Nochebuenas 2026 en Tampico: menudeo y mayoreo", subtítulo
   del prompt, CTA "Cotizar mi pedido" y WhatsApp. Franja: desde 2007, 4.6 en Google (24 reseñas), CFDI 4.0, entrega a domicilio.
2. **Cotizador**: tamaño, variedad y cantidad con − / +, varias líneas; fecha, zona, tipo de cliente y factura opcionales.
3. **Tabla de precios** en HTML estático, con la nota de escalones del prompt.
4. **¿Para quién?**: las 6 tarjetas del prompt; todas con mínimo sugerido de 12 piezas, "pide antes del 30 de noviembre" y
   WhatsApp con mensaje propio.
5. **Galería** (§6).
6. **Confianza**: calificación de Google, logos de clientes bajo un rótulo general y CFDI 4.0. Sin decir que esos clientes
   compraron nochebuenas. Sin las 4 opiniones con nombre, que son de otros servicios. **Sin garantía**.
7. **Cómo funciona tu pedido**: 3 pasos, con 50% de anticipo en mayoreo y fechas límite visibles. Cada fecha se oculta al
   pasar.
8. **Cuidados en clima de Tampico**: textos del prompt.
9. **Preguntas frecuentes**: las del prompt, con "200 piezas o más". Ninguna habla de garantía.
10. **Datos de la nochebuena**: originaria de México; 8 de diciembre, Día Nacional; Morelos, principal productor del país
    con fuente enlazada y sin porcentaje.
11. **CTA final**: WhatsApp, dirección, mapa, horario y "Última actualización: 8 de noviembre de 2026".

**CTA fijo móvil**: "Cotizar · $total", que sustituye en esta página a la barra móvil del shell y se oculta mientras el
cotizador o su botón están a la vista.

**Reglas de copy**: las del prompt y las del sitio (sin "gratis", "sin costo", "Oasis", "más vendido"; sin emojis en la
interfaz; el 🌺 solo en el mensaje de WhatsApp). Ninguna mención de garantía o reposición en esta página.

## 5. SEO y schema

- Título: "Nochebuenas en Tampico desde $65 · Mayoreo 2026 | Viveros Terra".
- Descripción: 'Nochebuena roja, rosa y jaspeada en 5", 6", 7", colgante y macetón. Precio por volumen, factura y entrega en
  Tampico, Madero y Altamira.'
- Canonical a sí misma, `index, follow`, `geo.region` MX-TAM, `geo.placename` Tampico, Open Graph con la foto principal.
  Sin `ai-content-declaration`, retirada de todo el sitio en la etapa 1a.
- JSON-LD: referencia a la ficha única `/#negocio`; `Product` por tamaño con `AggregateOffer` (low = Proyecto, high =
  Menudeo, MXN); availability InStock en temporada, macetón PreOrder, PreOrder en modo preventa y OutOfStock en postemporada;
  `FAQPage` igual a lo visible; `BreadcrumbList`; `dateModified`.

**URL y enlaces.** En `vercel.json` se elimina la redirección de esta URL, y `/nochebuenas-mayoreo-tampico` y
`/post/productores-de-nochebuenas-mayoreo` pasan a apuntar aquí. Se agrega a `sitemap.xml` y `llms.txt`. "Nochebuenas" entra
en "Plantas y palmas" del menú y en el pie. Franja nueva en la home y enlace en el hub de plantas: el banner de temporada
anterior ya no existe.

## 6. Fotos

Solo las de la carpeta del dueño (`Fotos Plantas/Nochebuenas`, 6 archivos de 2023); no hay más. No se usa el anuncio
`Tamanos Nochebuenas.png`. Se recorta para retirar personas y distracciones; nada generado con IA. WebP sin GPS, con 800w y
1600w solo si el original lo permite, sin ampliar. Se rotula únicamente lo que se ve: las zonas crema y amarilla se recortan
porque esos colores no están en la oferta. Las de empaque kraft se rotulan como pedidos de volumen listos para entregar. Sin
foto de rosa ni jaspeada: esas variedades se ofrecen en texto.

## 7. Modos

- `temporada`: todo lo anterior.
- `postemporada`: banner "Temporada 2026 cerrada · Gracias"; sin cotizador ni CTA fijo; quedan cuidados, FAQ, galería y
  "Avísame en la próxima temporada"; OutOfStock.
- `preventa`: "Aparta tus Nochebuenas [año] para tu empresa", cotizador en modo apartado, precios rotulados como referencia;
  PreOrder.
- En los tres: misma URL, indexable, en sitemap y en el pie. Recordatorio programado para el 2026-12-25.

## 8. Google Sheets

`apps-script/nochebuenas-pedidos.gs`, fuera de `public/`, con instrucciones. `doPost` agrega una fila en "Pedidos
Nochebuenas 2026" con las columnas del prompt. La hoja registra clics de envío, no pedidos confirmados. Como el endpoint es
público: valida forma y longitud, acepta solo valores conocidos en los campos cerrados y neutraliza fórmulas (`=`, `+`, `-`,
`@`). Lo despliega el dueño desde su cuenta. `connect-src` de la CSP incorpora `https://script.google.com`.

## 9. Archivos

Nuevos: `tools/site/plantillas/nochebuenas.py`, `tools/site/contenido/nochebuenas.py`, `public/js/vt-nochebuenas.js` y su
prueba, `public/css/terra-nochebuenas.css`, `public/img/nochebuenas/`, `apps-script/nochebuenas-pedidos.gs`,
`tools/site/tests/test_nochebuenas.py` y su prueba de navegador. Modificados: `vercel.json`, `tools/site/datos.py`,
`paginas.py`, `build.py`, `partials.py`, home, hub de plantas, `sitemap.xml`, `llms.txt`, `activos.json` y las páginas
regeneradas por el menú y el pie.

## 10. Verificación

Las tres suites del sitio, build idempotente y los casos de §3 en `node --test`. Navegador a 360, 768 y 1440 sin scroll
horizontal, con el CTA fijo sin tapar contenido y el mensaje de WhatsApp completo con el endpoint fallando; todo tráfico que
no sea localhost se bloquea por defecto. Pruebas de los tres modos. Lighthouse móvil: rendimiento ≥ 85, accesibilidad ≥ 90,
SEO 100. JSON-LD validado. En producción: 200 sin redirección. Revisores independientes de diseño móvil, SEO y schema,
cumplimiento de reglas y seguridad antes de publicar.
