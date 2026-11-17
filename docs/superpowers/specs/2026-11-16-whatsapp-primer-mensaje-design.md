# WhatsApp: que el primer mensaje diga qué quiere el cliente (2026-11-16)

Aprobado por el dueño el 2026-11-16 (opción 1 + 2). Va antes de la entrega D del SEO nacional.

## Problema (auditoría del 2026-11-16)
- 100 botones en 34 páginas mandan solo «Hola, quiero cotizar pasto sintético.» y 31 «tengo una pregunta sobre pasto
  sintético» si el cliente no usó antes el cotizador: no llegan modelo, m² ni destino.
- 44 mensajes en 9 páginas llevan rayas «___» (p. ej. «Hola, quiero cotizar: ___», «Metros aprox.: ___») que el
  cliente casi nunca llena.
- Mantenimiento, poda, riego, diseño y pasto en rollo nombran el servicio pero no los datos que el asesor pregunta
  después (tamaño, frecuencia, colonia/ciudad).
- El sitio no recuerda entre páginas el modelo visto, el estado elegido ni los m² calculados.

## Solución
1. **Contexto automático (sin preguntar):** el mensaje usa lo que la página y la visita ya saben: modelo de la ficha,
   ciudad/estado de la página o del cotizador, m² de la calculadora o el cotizador, folio web (vt-folio.js) y la firma
   «Vengo de viverosterra.com» (terra.js). Memoria solo de la visita (sessionStorage): modelo, estado y m²; nunca nombre
   ni teléfono.
2. **Panel de preguntas rápidas** en los botones de cotizar de las secciones donde el dato cambia la cotización. Una
   sola pantalla, 2–3 grupos de opciones de un toque, el mensaje visible mientras se arma, botón «Abrir WhatsApp»
   (funciona sin contestar nada) y enlace «Solo quiero contactarlos» (mensaje corto de la página). Una pregunta cuya
   respuesta ya se conoce no se muestra.

## Preguntas por sección (opciones = datos ya publicados en el sitio)
| Sección | Preguntas |
|---|---|
| Pasto sintético (tienda, fichas, Tampico, ciudades, guías) | Modelo (9 + «No sé, recomiéndenme») · m² (menos de 25 / 25 a 50 / 50 a 100 / más de 100) · Destino (Tampico, Madero o Altamira: recoger o con instalación / otro estado: los 32) |
| Pasto en rollo San Agustín | Solo el pasto / instalado · m² (menos de 50 / 50 a 200 / 200 a 500 / 500 o más, mayoreo) · Tampico / Madero / Altamira / otro |
| Mantenimiento | Tamaño (chico, menos de 50 m² / mediano, 50 a 200 / grande, más de 200) · Frecuencia (datos.FRECUENCIAS_MANTENIMIENTO + «No sé») · Tampico / Madero / Altamira |
| Poda y derribo | Árbol / palma / varios · Poda / derribo / que lo revisen · Tampico / Madero / Altamira |
| Riego automático | Pasto (aspersores) / plantas (goteo) / las dos / no sé · Tamaño · Tampico / Madero / Altamira |
| Diseño de jardines | Plan (Esencial / Completo / Premium / no sé) · Tamaño |
| Plantas, palmas, árboles y materiales | Sin preguntas (la lista del catálogo ya manda productos y cantidades); solo se quitan las rayas |
| Empresas y mayoreo | Sin preguntas |
| Encabezado, pie, «Llamar» | Sin preguntas: «Hola, quiero información» + la página |

Ejemplo: «Hola, quiero cotizar pasto sintético Toscana 28, entre 25 y 50 m², con envío a Jalisco. Folio web: T28-…»

## Arquitectura
- **Una sola fuente de preguntas** en Python (tools/site/preguntas_wa.py): conjuntos por sección; las plantillas marcan
  el botón con `data-vt-preguntas="<conjunto>"` y la página lleva el JSON del conjunto (como json_modelos).
- **public/js/vt-preguntas.js** (UMD): `armarMensaje(conjunto, respuestas, contexto)` pura y probada en Node; en el
  navegador abre un `<dialog>` (hoja inferior en celular, centrado en escritorio), actualiza el `href` del enlace final
  en cada toque y deja que el cliente lo toque (sin window.open). Sin JS el botón conserva su `href` actual.
- **Memoria de la visita:** sessionStorage con try/catch; tienda-pasto.js, vt-rollos.js y las fichas escriben modelo,
  estado y m²; vt-preguntas.js los lee para omitir preguntas y llenar el mensaje.
- **Compatibilidad:** el folio y la firma no cambian (el cotizador de Netlify sigue leyendo «Folio web:»).
- **Medición:** generate_lead con `preguntas` = respondidas / omitidas / solo-contacto.

## Accesibilidad y rendimiento
Foco al abrir y regreso al botón al cerrar, Esc y ✕, grupos con `role="radiogroup"`/botones con `aria-pressed`,
objetivos de 44 px, prefers-reduced-motion, sin desborde a 320–1440 px; script diferido y pequeño, CSS dentro de los
presupuestos existentes (hoja propia si hace falta, como terra-calculadora.css).

## Pruebas (sin mandar mensajes reales)
Node: armarMensaje con cada conjunto y combinaciones (texto exacto, sin «___», sin preguntas ya conocidas). Python: los
conjuntos usan solo datos de datos.py/data.py; ninguna página publicada con «___» en un enlace de WhatsApp; cada botón
marcado tiene su conjunto. Playwright: abre el panel, toca opciones y lee el `href` sin navegar; teclado, Esc y foco;
anchos 320/375/768/1440. Nunca se toca un enlace wa.me.

## Entregas
1. Pasto sintético completo + quitar «___» en todo el sitio.
2. Servicios de Tampico: pasto en rollo, mantenimiento, poda, riego y diseño.
Cada una se publica solo con «publícala» del dueño. La entrega D del SEO nacional espera.
