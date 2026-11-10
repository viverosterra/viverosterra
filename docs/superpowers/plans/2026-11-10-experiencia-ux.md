# Plan de experiencia (UX) — viverosterra.com

Fecha: 2026-11-10. Insumos en `docs/ux/2026-11/`: `auditoria-diseno-visual.md` (22 páginas, ranking de héroes, hero de marca
propuesto), `auditoria-fotos.md` (519 imágenes, lista de tomas), `auditoria-recorrido-textos.md` (10 recorridos, tabla de CTA,
20 reescrituras). Regla vigente del dueño: no se cambia ninguna foto sin su visto bueno.

## Diagnóstico
- Base sana: sin scroll lateral, CLS ≈ 0, contraste AA, foco y radios consistentes, precio a la vista, mensajes de WhatsApp
  por contexto.
- La home quedó por delante del resto: su botón alto con sombra amarilla, el lema serif, la etiqueta colgada y la línea de
  confianza no existen en las otras 20 plantillas.
- En móvil ningún hero interior muestra foto (empieza entre 800 y 1,030 px) y en pantallas bajas el CTA queda fuera en 12 de
  19 plantillas (ledes de 4–7 renglones).
- Tramos largos sin CTA: tienda (12 pantallas), plantas/palmas/catálogo (15–39), mantenimiento (14.5).
- Las calculadoras no pasan su resultado a la barra fija (ya resuelto en la home, no en las demás).
- Prueba social ausente en tienda, plantas, catálogo y Nochebuenas.
- Fotos: varias portadas con aspecto de render; dos de tierra negra con texto ilegible; fotos que no corresponden (vivero,
  interior, piedra bola, tezontle a 194 px); catálogo con 24 marcas de agua; 152 archivos sin uso (31 MB).

## Entrega A — Hero de marca en todas las plantillas (mayor impacto)
- [ ] Componente único de portada con la fórmula de la home: kicker de 1 renglón, titular, lema serif siempre, lede de 2
      renglones, botón de 60–64 px con sombra amarilla, fila de enlaces de texto (el teléfono deja de ser botón), línea de
      confianza con `datos.GOOGLE`, etiqueta colgada sobre la foto en escritorio.
- [ ] Móvil: foto a sangre 16:10 dentro de la primera pantalla con la etiqueta compacta montada sobre su borde; foto, precio y
      botón dentro de 664 px útiles. `object-position` por foto para no cortar cabezas ni logos.
- [ ] Variantes: servicio, hub, material, zona, precios, empresas, ciudad, artículo (con imagen y CTA en el hero), ficha.
- [ ] Mover el CSS del hero de `terra-inicio.css` a la hoja común (presupuesto de `terra.css`) y unificar el sistema de
      botones de la tienda.
- [ ] Corregir el lema de materiales (`<em>` → `vt-serif`). Escala única de h1; sin Title Case en blog y catálogo.

## Entrega B — CTA y recorrido
- [ ] La barra fija toma el resultado de cada calculadora (pasto en rollo, materiales, mayoreo, Nochebuenas, tienda).
- [ ] CTA en los tramos vacíos: tienda (hub y ficha), plantas, palmas, catálogo ("Cotizar mi lista" directo en la barra),
      mantenimiento.
- [ ] Texto de botón específico por contexto, con `/precios` como modelo; las 20 reescrituras del informe.
- [ ] Prueba social cerca del CTA donde falta (solo opiniones y cifras reales ya publicadas).
- [ ] Mensajes de WhatsApp del blog con colonia y medida; cierre de artículo con precio y garantía.
- [ ] Medidor con aviso en entradas inválidas; simulador sin monto fantasma; nombres únicos para "Mi lista"; conteo real del
      catálogo; cuestionario con un solo trato (tú), un solo tiempo estimado y respuestas guardadas en la sesión.
- [ ] Menú: entrada a vivero/horario y blog; materiales fuera de "Plantas y palmas"; búsqueda del 404 con Nochebuenas.

## Entrega C — Ritmo y movimiento
- [ ] Banda oscura de garantía a media página en servicios; variar el relleno entre secciones; recortar secciones redundantes
      en las páginas de 23+ pantallas.
- [ ] Llevar el movimiento sobrio de la home (revelado por scroll, estado activo del botón) a todas las plantillas.
- [ ] Amarillo reservado al precio y al CTA.

## Entrega D — Fotos (requiere al dueño)
- [ ] Decisión del dueño sobre las portadas con aspecto de render y las dos de tierra negra con texto ilegible.
- [ ] Usar más las fotos reales ya publicadas como portada (alberca frente a la laguna, terraza con sintético, recorte de seto
      con chaleco, invernadero de nochebuenas), con su visto bueno.
- [ ] Lista de 15 tomas con celular (cuadrilla con uniforme, fachada y pasillos del vivero, tezontle, camión y costales reales,
      antes/después, nochebuena rosa y jaspeada).
- [ ] Técnico: `srcset` en 474 imágenes, 106 de más de 200 KB, `og:image` horizontal, retirar 152 archivos sin uso.
- [ ] Catálogo: sustituir las 24 con marca de agua y la de la universidad conforme haya foto propia.

## Medición
`generate_lead` por `cta_id` y por página de entrada, 2–4 semanas antes y después de cada entrega; clics al hero frente a la
barra; proporción de mensajes con medida.

## Preguntas al dueño
¿Las portadas son render/IA o fotos? ¿Se retiran los plazos ya publicados ("3 a 5 días hábiles", "instalado en un día",
"propuesta en 3 a 5 días")? ¿Autoriza cambiar portadas por fotos reales ya publicadas?
