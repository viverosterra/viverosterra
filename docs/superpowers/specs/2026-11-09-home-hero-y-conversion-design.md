# Home: hero nuevo y mejoras de conversión — diseño

Fecha: 2026-11-09. Aprobado por el dueño ("todo el plan"). Rama `feat/home-hero`. Maqueta de referencia del hero:
`docs/diseno/hero-2026-11/mock.css` y `mock.js` (transformación del DOM actual; es guía visual, no código a copiar tal cual).
Insumos: auditoría de conversión y análisis de movimiento del 2026-11-09 (resumidos aquí).

## Reglas que no cambian
Estilo Plano + Etiqueta; solo tokens de color; nada inventado (cifras solo de `datos.py`); prohibido "gratis", "sin costo"
(salvo la garantía de pasto), "más vendido", visita gratis, porcentajes de anticipo, plazos de entrega, fecha de próximo
corte. `datos.PROMESA_COMPLETA` debe seguir contigua en el HTML ("menos de 1 hora" siempre con "en horario"). Fotos: no se
cambia ninguna. Precio y CTA de WhatsApp de la portada dentro de la primera pantalla a 375×812, 375×667 y 320×640 (el CTA al
menos visible a 320×640 como hoy exige la suite); sin scroll horizontal de 320 a 1920. El contenido se ve completo sin JS.

## Entrega 1

1. **Hero de la home** (solo la home; las demás páginas siguen con `c.portada` actual).
   - Kicker: "Vivero y cuadrilla propia · Desde 2007".
   - H1: "Pasto, jardines y plantas en Tampico." y, debajo, la línea en serif verde "Con el precio por delante." (fuera del
     `<h1>` si la prueba de H1 no admite spans; visualmente pegada).
   - Lede: "Pasto San Agustín en rollo, diseño de jardines y +200 variedades de plantas, en Tampico, Madero y Altamira."
   - Un solo botón: "Cotizar por WhatsApp", más alto (62–66 px), con sombra dura amarilla (`var(--vt-tag)`) y estados
     hover/active/focus. Debajo, dos enlaces de texto: "Calcula tu patio →" (`#medidor`) y "Llamar 833 326 8008".
   - Línea de confianza bajo los enlaces: `datos.PROMESA_COMPLETA`, "4.6 en Google (24 reseñas)" (`datos.GOOGLE`) y
     "+900 clientes" (`datos.CLIENTES`).
   - Etiqueta de precio: en móvil, entre el lede y el botón (versión compacta actual). Desde 1024 px, colgada sobre la esquina
     inferior izquierda de la foto (misma celda de la rejilla, con cordel), siempre derecha.
   - Foto actual: a sangre en móvil (4:3), 4:5 en escritorio. Se retira la fila "También: …" (los servicios están en la
     sección siguiente). Cuadro de datos igual.
   - CSS en una hoja propia de la home (`terra-inicio.css`, registrada como las demás; `terra.css` no tiene presupuesto), con
     su prueba de alcance y presupuesto (< 6 KB).
2. **Metas de la home sin "gratis"**: description, og y twitter, p. ej. "Precios con IVA a la vista. Cotiza por WhatsApp:
   respondemos en menos de 1 hora en horario." Agregar la home a la regla que prohíbe "gratis" si hoy está exenta.
3. **"Abierto ahora"**: función pura `abierto(fecha)` en `terra.js` con `Intl.DateTimeFormat` en America/Mexico_City,
   horario de `datos.HORARIO_LD` (paridad probada) y festivos de `datos.FESTIVOS` (inicial: 12-25 y 01-01, cada año). En
   horario antepone "Abierto ahora · " a la promesa de portada, barra móvil y cierre (elementos marcados con un atributo
   `data-vt-horario`); fuera de horario no cambia nada. El punto verde nunca es la única señal. Sin `aria-live`.
4. **Medidor en móvil**: la etiqueta del resultado sube justo debajo de los campos (antes del plano). Con medida válida el
   botón dice "Enviar mi medida por WhatsApp"; sin medida, "Cotizar por WhatsApp". La barra fija móvil ya no se oculta en
   todo el medidor: solo mientras el botón del medidor está a la vista. Mantener la paridad Python/JS y sus casos.
5. **WhatsApp por servicio en "Qué hacemos"**: en cada fila un enlace "Cotizar <servicio> →" con el mensaje de
   `datos.MENSAJES` de ese servicio y `data-cta="home:indice-<servicio>"`.
6. **CTA en el tramo vacío**: fila de WhatsApp al final de Opiniones, Proceso, Precios y Preguntas, con
   `data-cta="home:opiniones|proceso|precios|faq"`.
7. **Garantía junto al CTA**: `datos.GARANTIA_PASTO` con enlace a condiciones bajo el resultado del medidor y en el cierre.
   En el cierre, lo último antes del botón es la promesa de respuesta; la frase del costo de la visita va después.

## Entrega 2

8. **Movimiento** (solo `transform`, `opacity`, `clip-path`; todo dentro de `prefers-reduced-motion: no-preference`; una vez,
   ≤ 900 ms; nunca `opacity` sobre el H1/lede/precio/CTA al cargar): balanceo único de la etiqueta colgada (≥ 1024 px);
   foto de portada con `clip-path` (≥ 1024 px); encabezados de sección y figuras de obra con
   `animation-timeline: view()` bajo `@supports`; `:active` del botón; hovers con transform solo en `@media (hover:hover)`;
   quitar `visibility` de la transición de `.vt-bar` si no rompe su prueba. Sin count-up, sin pulso infinito.
9. **Días restantes en el banner de Nochebuenas**: `<span data-vt-hasta="AAAA-MM-DD">` con `preventa.hasta`; JS escribe
   " · Preventa: faltan N días" (N ≥ 1; el último día "último día de preventa"); después de la fecha, nada. Solo días.
10. **Reseñas y menú**: enlace "Ver las reseñas en Google" (`datos.MAPS_URL`) en Opiniones; botón de WhatsApp dentro del menú
    móvil (`data-cta="<tipo>:menu"`).
11. **Medición**: el clic del banner y el de "Calcula tu patio" mandan evento GA4 (`select_content` con `cta_id`), sin tocar
    `generate_lead`.

## Verificación
Las tres suites, build idempotente, pruebas nuevas (hero, horario con bordes sáb 13:59/14:00, vie 17:59/18:00, domingo,
festivos y cambio de día UTC; sin JS; movimiento reducido con cero animaciones; recorrido completo sin elementos con opacidad
< 1), capturas a 320/375/768/1024/1440, Lighthouse móvil sin bajar de rendimiento 90 ni accesibilidad 100. Revisión
independiente de diseño y de reglas antes de publicar. Todo tráfico fuera de localhost bloqueado en pruebas.
