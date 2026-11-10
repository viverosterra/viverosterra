# Auditoría de recorrido, textos y CTA — viverosterra.com (fuera de la home)

Fecha: 2026-11-10 · Producción, solo lectura (GET) · Playwright/Chromium con UA de iPhone, 375×812 y 375×667, y 1440×900 · Todo dominio ajeno bloqueado · Ningún clic en wa.me/tel ni envío de formularios (los mensajes se leyeron del `href`; los formularios, del DOM y de `vt-cuestionario.js` / `vt-datos-envio.js`).

Convención: **[M]** = hecho medido en esta sesión · **[H]** = hipótesis o juicio experto, sin dato de comportamiento real.
"Pantalla" = 812 px de alto a 375 px de ancho, salvo que se indique 667.

Evidencia en esta carpeta: `*_375.json` (perfil por página), `*_375_top.png / _mid.png / _full.jpg`, `txt_*.txt` (texto visible), capturas `A*` (pasto), `B*` (tienda), `C*` (catálogo), `D/E*` (tierra, mayoreo), `F*` (cuestionario, gracias, datos de envío), `G*` (Nochebuenas), `N*` (navegación, 404, escritorio). Scripts: `perfil.py`, `h.py`, `a_pasto.py`, `b_tienda.py`, `c_cat.py`, `d_varios.py`, `n_nav.py`, `res2.py`.

---

## (a) Resumen ejecutivo

El sitio está por encima del promedio en lo que más pesa para vender por WhatsApp: precio visible en el primer pantallazo, mensajes prellenados distintos por contexto, vista previa de "El mensaje que se abre", barra fija móvil que se oculta cuando ya hay un CTA a la vista, `data-cta` en todos los enlaces y accesibilidad básica correcta (enlace de salto, foco visible, etiquetas, objetivos táctiles ≥ 44 px). No hay que rehacer nada; lo que queda son fugas concretas:

1. **Las calculadoras no "le pasan la estafeta" a la barra fija ni al encabezado.** [M] En `/pasto-en-rollo-tampico`, después de calcular 10 × 5 m, el botón del medidor lleva el mensaje completo (medidas, estimado, forma de pago, colonia), pero la barra fija y el "Cotizar" del encabezado siguen abriendo el mensaje genérico con tres huecos. El cliente que calculó y sigue leyendo pierde su cálculo al tocar el CTA que tiene a la mano. Mismo patrón en mayoreo, tierra y en el hub de la tienda (elegir estado en el hero no cambia el mensaje del CTA del hero).
2. **La tienda de pasto sintético tiene los tramos más largos sin CTA y sin barra.** [M] Hub: ninguna barra fija en todo el recorrido hasta que se agrega un modelo; 12.1 pantallas seguidas sin CTA de WhatsApp (de la 9.3 a la 21.4). Ficha: el primer CTA de WhatsApp está en la pantalla 3.5; la barra de compra aparece hasta ~pantalla 7; el "Cotizar" del encabezado no lleva el modelo.
3. **Las páginas de plantas dependen de dos CTA en 18–23 pantallas** (hero y cierre) más la barra; el catálogo mide 43.8 pantallas con CTA solo en la 0.6 y la 39.7, y su mensaje del hero no pide ningún dato ("vi el catálogo y quiero cotizar una planta").
4. **El texto del botón es casi siempre "Cotizar por WhatsApp →"**, incluso en tres tarjetas de plan contiguas con mensajes distintos. El mensaje sí cambia; el botón no lo dice. [M] 9 de 9 CTA en línea de mantenimiento/diseño/riego usan el mismo texto.
5. **Prueba social desigual.** [M] Tienda (hub, ficha, páginas de ciudad), plantas, palmas, catálogo y Nochebuenas no muestran ningún testimonio; la calificación "4.6 en Google (24 reseñas)" solo aparece en el pie y en el hero de Nochebuenas. Para el comprador de Monterrey, que paga por adelantado a un vivero de otra ciudad, es la mayor carencia de confianza.
6. **Los blogs (entrada desde Google) convierten con el mensaje más pobre del sitio**: "leí su artículo … y quiero cotizar", sin colonia ni metros, y el primer enlace al servicio llega en la pantalla 3.2 de 11.6.
7. **Cuestionario**: funciona y valida, pero mezcla "tú" y "usted", promete "4 minutos" y "4-5 minutos" en la misma pantalla, el campo "Fotos de referencia" es una caja de texto, y se pierden las respuestas al recargar. Ni `/cuestionario` ni `/datos-envio` tienen enlaces entrantes (se envían por WhatsApp): correcto, pero conviene que la página de diseño diga en qué momento llega.
8. **Navegación**: el menú móvil no tiene entrada para "Vivero / cómo llegar / horario" ni "Blog"; "Jardín" es una etiqueta ambigua; tierra, tezontle y piedra viven dentro de "Plantas y palmas". La búsqueda del 404 no encuentra "nochebuena".

Un aviso de cumplimiento, sin propuesta de mi parte: el sitio ya publica plazos ("envío en 3 a 5 días hábiles", "instalado en un día", "propuesta visual · 3 a 5 días", "instalación residencial 1 a 2 días"). Si la regla de "sin plazos de entrega" aplica también a lo ya publicado, eso lo decide el dueño; ninguna reescritura de este informe agrega plazos.

---

## (b) Recorridos

### 1. "Quiero pasto para mi patio" → `/pasto-en-rollo-tampico`

26.1 pantallas · 2,123 palabras · 4 CTA de WhatsApp en línea + encabezado + barra + pie.

**Funciona** [M]
- Primer pantallazo: titular, etiqueta con $120 instalado / $85 solo pasto / desde $60 mayoreo, y la barra fija visible desde el scroll 0 en 667 px (el CTA del hero queda en y=738–790, bajo el pliegue; la barra lo suple y se oculta cuando el CTA del hero entra a la vista).
- Bajo el CTA: "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h" y "Garantía de arraigo de 15 a 20 días con instalación".
- Medidor: teclado decimal (`inputmode=decimal`), acepta coma (10,5 → 10.50), tope de 1,000 m por lado con mensaje útil, y arma un mensaje sin huecos salvo la colonia: `Medidas: 10.00 × 5.00 m = 50 m² / Estimado de la web: desde $6,000 con IVA / Me interesa: 3 mensualidades de $2,210 … / Colonia: Lomas de Rosales / Te mando foto del área.`
- IVA explicado tres veces sin contradicción (instalado con IVA; solo pasto y mayoreo no llevan IVA). Garantía con condiciones y enlace a políticas. Visita con costo, dicha en el cierre.

**Fricciones**
1. **El cálculo no viaja a la barra fija ni al encabezado.** [M] Tras calcular, `servicio-pasto:barra` y `servicio-pasto:header` siguen con `Colonia: ___ / Metros aprox.: ___ / Solo el pasto o instalado: ___`. Tampoco se guarda: al recargar, largo/ancho vuelven vacíos (sin `localStorage`). *Arreglo*: cuando el medidor tenga resultado válido, usar ese mismo mensaje en barra, encabezado y cierre, y guardar largo/ancho/modo en `sessionStorage`.
2. **9.7 pantallas entre el CTA del hero (0.9) y el del medidor (10.6); la explicación de precio empieza en la 7.9 y el medidor en la 9.1.** [M] El enlace "calcula tu patio" bajo el hero existe, pero es texto pequeño en una línea con otros dos enlaces. *Arreglo* [H]: convertir "calcula tu patio" en botón secundario del hero ("Calcular mi patio") y poner un CTA de WhatsApp al terminar los testimonios (pantalla ~5.4).
3. **Entradas inválidas sin aviso.** [M] Con "abc", "0" o "-4" el resultado vuelve a "Escribe tus medidas", sin `aria-invalid` ni texto de error, y el croquis conserva la medida anterior (10.50 × 5.00). El simulador de mensualidades abre por omisión "Mi cotización es de $12,000. Pagaría de contado." aunque el cliente no haya escrito nada: el vendedor recibe una cifra que el cliente no dio. *Arreglo*: mensaje de error en línea (texto en la sección d, n.º 2) y, si el monto no se tocó, mensaje del simulador sin cifra (d, n.º 3).

Menor [M]: "tepes" aparece en el hero sin explicación y "Stenotaphrum secundatum" ocupa una línea de la etiqueta de precio; el modo "Mayoreo" con 50 m² cambia en silencio a "solo pasto $85" (el aviso existe, pero abajo).

### 2. "Quiero pasto sintético y vivo en Monterrey" → `/pasto-sintetico`, ficha, lista, `/envio/monterrey`, `/datos-envio`

**Funciona** [M]
- Precio final claro: al elegir Nuevo León, el hero pasa a "Desde $162/m² puesto en Nuevo León, envío incluido" y cada tarjeta muestra "$222/m² puesto en Nuevo León". El cotizador desglosa material, flete por rollo y total (`50 m² → $9,950 + $1,150 = $11,100`; `60 m² → 2 rollos, $2,300 de flete`), y dice el recargo de las mensualidades ("Pagando de contado te ahorras $1,653").
- El estado elegido viaja: de la página de Monterrey (`?estado=nuevo-leon#modelos`) al hub, del hub a la ficha y a la lista (`localStorage: vt-cotizacion-v1`). La lista sobrevive al cambio de página.
- Mínimo nacional bien explicado: con 7 m² y envío, "Para envío nacional el mínimo es 25 m² (medio rollo)".
- Mensaje de la lista sin huecos: modelo, m², precio, estado, flete, total, forma de pago, "¿Me confirman el precio final con envío a mi dirección?".
- "Cómo comprar … en línea" en 4 pasos con quién hace qué; página de Monterrey responde costo, mínimo, quién instala y "no ofrecemos muestras físicas".
- `/datos-envio`: teclado numérico en C.P. y teléfono, valida 5 y 10 dígitos, RFC con patrón, y al terminar muestra "¡Listo! Solo falta que toques Enviar en WhatsApp".

**Fricciones**
1. **Tramos sin CTA y sin barra.** [M] Hub: la barra fija nunca aparece (scroll 0 a fin) mientras la lista esté vacía; 12.1 pantallas sin CTA de WhatsApp entre el cotizador (9.3) y el cierre (21.4). Ficha: primer CTA de WhatsApp en la 3.5; 11.7 pantallas sin CTA entre la 3.5 y la 15.2; la barra `vt-compra` aparece hasta ~6,000 px y mide 130 px (16 % de 812, 19 % de 667). En escritorio, el CTA de la ficha está en y=2,386 (2.6 pantallas de 900). *Arreglo*: en la ficha, un CTA bajo la etiqueta de precio ("Cotizar Toscana 28 por WhatsApp", con el mensaje del cierre); mostrar la barra de compra desde que el cotizador sale de la vista hacia arriba **o** desde que el hero sale, y reducirla a una línea.
2. **Los CTA genéricos no llevan lo que el cliente ya eligió.** [M] Tras elegir Nuevo León en el hero del hub, `tienda:hero` y `tienda:header` siguen con `Ciudad o colonia: ___ / Metros aprox.: ___`. En la ficha, `tienda:header` no menciona "Toscana 28". Con m²=0 el mensaje dice "Necesito 0 m²." *Arreglo*: inyectar estado y modelo en hero/encabezado; con m² vacío o 0, omitir la línea.
3. **Tres nombres para lo mismo y cero prueba social.** [M] "Mi lista" (botón), "Tu lista" (título del panel), "Agregar a mi cotización" (cotizador), "+ Agregar" (tarjetas), "+ Agregar · 1 rollo" (comparativa). Ninguna de las tres plantillas de tienda muestra un testimonio ni la calificación de Google fuera del pie; la página de Monterrey no menciona la garantía de fábrica (0 apariciones de "garantía") aunque el hub publica "3 a 8 años, según el modelo" y "Devoluciones 7 días · nuevo y sin cortar". *Arreglo*: unificar a "Agregar a mi lista" / "Mi lista"; llevar la tira de confianza del hub (garantía, devoluciones, factura, "vendemos a todo México desde 2012") y "4.6 en Google (24 reseñas)" junto al CTA del cotizador y a las páginas de ciudad.

Menor [M]: `/datos-envio` muestra un único error genérico ("Revisa los campos marcados en rojo.") y sus campos no tienen `autocomplete` (calle, C.P., nombre, teléfono), así que el teléfono no se autocompleta; `/pasto-sintetico/mi-lista` no existe (404), la lista solo vive en el panel.

### 3. "Busco palmas" → `/plantas-palmas-arboles-tampico`, `/palmas-tropicales-tampico`, `/catalogo`

**Funciona** [M]
- Mensajes del hero con 3 campos + foto, distintos por página (plantas: "Plantas que busco / Tamaño aprox. / Colonia de entrega"; palmas: "Palma que me interesa / Altura aprox. / Colonia de entrega").
- Entrada por necesidad (sol, sombra, salitre, tamaño) que lleva al catálogo con el filtro puesto; las tarjetas de palmas abren el catálogo con el diálogo de esa especie ya abierto (`/catalogo?q=Palma%20Areca&add=palma-areca`, verificado).
- Catálogo: filtros en la URL (`?cat=palmas`), contador en vivo ("22 especies"), estado vacío con salida ("No hay especies con esos filtros… Preguntar por WhatsApp" y el término buscado dentro del mensaje), diálogo con tamaño y piezas, y mensaje de lista limpio: `• Palma Areca (1-2 m) × 1 … ¿Pueden darme precio y disponibilidad?`. La lista sobrevive a una recarga.
- Precios publicados donde los hay (areca y coco plumoso desde $250, palma real desde $500) y "según cotización" en lo demás, sin inventar.

**Fricciones**
1. **Muy pocos CTA para tanto scroll.** [M] Plantas: 2 CTA en línea en 23 pantallas (19.5 seguidas sin CTA). Palmas: 2 en 18.5 (15.0 sin CTA). Catálogo: 43.8 pantallas, CTA en la 0.6 y la 39.7, sin barra fija hasta que se agrega algo. La barra `vt-bar` cubre el hueco en plantas/palmas, pero con el mensaje genérico. *Arreglo* [H]: CTA en línea después de la rejilla de especies y después de "¿Cuánto cuesta una palma?"; en el catálogo, mostrar la barra desde el inicio con "Arma tu lista: añade plantas y cotiza en un mensaje" cuando esté vacía.
2. **La barra de la lista no cotiza: obliga a dos toques y no dice qué sigue.** [M] Con 1 artículo la barra dice "Mi lista 1" (tras el aviso temporal); hay que abrirla para encontrar "Cotizar por WhatsApp". El mensaje del hero del catálogo es el más pobre del sitio: "Hola, vi el catálogo y quiero cotizar una planta" (0 campos). El mensaje de la lista no pide colonia de entrega. *Arreglo*: barra con dos zonas ("Mi lista · 2 variedades · 4 piezas" + botón "Cotizar"), y añadir "Colonia de entrega: ___" al mensaje de la lista y campos al del hero (d, n.º 6 y 7).
3. **Ninguna prueba social ni garantía cerca del CTA.** [M] 0 testimonios en plantas, palmas y catálogo; la garantía de 30 días aparece en la pantalla 14.3 (plantas) y 10.5 (palmas), lejos de ambos CTA. Además, "Ficha" en cada tarjeta del catálogo saca al cliente hacia un artículo del blog. Dato inconsistente: el catálogo anuncia "117 especies" y el DOM tiene 120 tarjetas; vivero y hero dicen "+200 variedades". *Arreglo*: una línea bajo el CTA del hero ("Garantía de 30 días en las plantas que sembramos nosotros · ver condiciones") y renombrar "Ficha" a "Guía de cuidados" (como ya dice la página de palmas).

### 4. "Necesito tierra/tezontle" → `/tierra-negra-vegetal-tampico`

**Funciona** [M]
- Precio completo en la pantalla 3.9: costal $90, preparada $100, m³ $1,500, camiones de 5/8/14 m³; "Sin mínimo de compra"; "La entrega a domicilio se cobra por viaje, según tu colonia".
- Calculadora con opción recomendada ("8 cm · preparación para pasto"), resultado útil (30 m² → 2.4 m³, ~$3,600, ~69 costales; 0.5 m² → 3 costales, $270) y mensaje con área, capa y cantidad.
- Dos testimonios y formulario de correo como alternativa, con honeypot y aviso de privacidad.

**Fricciones**
1. **7.6 pantallas del hero (0.8) a la calculadora (8.5)** y la calculadora llega después de dos secciones de contenido educativo. [M] *Arreglo* [H]: subir la calculadora a continuación de la lista de precios.
2. **El mensaje calculado no pregunta lo que el vendedor necesita para cerrar**: falta "Costales o a granel" y cierra con una pregunta larga; el genérico sí lo pide. [M] Entradas inválidas ("abc") no muestran error. *Arreglo*: ver d, n.º 13.
3. **El formulario de correo compite con el cierre.** [M] Aparece después del CTA final (pantalla 15.7) con botón "Enviar solicitud de pedido", que suena a compra en firme para algo que es una solicitud de cotización. *Arreglo*: d, n.º 14.

### 5. "Soy de una empresa" → `/mayoreo-pasto-tampico`, `/palmas-mayoreo-proyectos`

**Funciona** [M]
- REPSE 773725 con enlace al padrón de la STPS, CFDI 4.0, logotipos y testimonio de constructora antes del precio; tres paquetes con mensajes distintos que piden lo correcto (empresa, obra, m², etapas, estado del terreno).
- Cotizador de mayoreo honesto: 300 m² → "$25,500 (300 × $85; no lleva IVA)", 1,200 m² → "desde $72,000". Los datos opcionales (empresa, obra) entran al mensaje **y** prellenan el formulario de correo.
- Formulario con `autocomplete` correcto (organization, name, email, tel) y teléfono opcional. Armador de palmas: lista de especies, altura y cantidad, y mensaje `- 40 × Coco plumoso, altura aprox.: 3 m`.

**Fricciones**
1. **El titular del formulario habla raro**: "¿Compras prefiere correo? Pide la cotización por escrito". [M] *Arreglo*: d, n.º 15.
2. **6 a 7 CTA con el mismo texto** ("Cotizar por WhatsApp →") en tres paquetes consecutivos; el comprador no sabe que cada botón abre un mensaje distinto. [M] *Arreglo*: d, n.º 5.
3. **El armador de palmas no da ninguna referencia de precio** (dice, correctamente, que depende de especie y altura), pero la página de palmas al menudeo sí publica "desde $250 / desde $500 en tamaño chico". [M] *Arreglo* [H]: una línea que remita a esas referencias ya publicadas, aclarando que el volumen se cotiza por escrito.

### 6. "Quiero mantenimiento/diseño/riego" → las tres páginas y `/cuestionario`

**Funciona** [M]
- Precio en el hero de las tres (desde $750/mes; $3,000 / $6,500 / desde $18,000; $180–$320/m²) y "Nota de campo" que desaconseja el servicio cuando no hace falta, una señal de honestidad poco común.
- Tarjetas de plan con mensaje propio (plan, precio y campos pertinentes). Diseño responde la objeción clave ("¿Y si al final no contratas la obra?").
- Cuestionario: 5 pasos, 65 controles, solo 2 obligatorios (nombre y WhatsApp); "Siguiente" valida el paso y enfoca el campo vacío; patrón de teléfono con `title` en español; Enter avanza en vez de enviar; `/gracias` explica qué sigue, repite que la visita tiene costo y ofrece "Adelantar por WhatsApp".

**Fricciones**
1. **Mantenimiento: 14.5 pantallas sin CTA en línea** (de la 9.3 a la 23.8, justo donde están "qué incluye", proceso, garantía y preguntas). Diseño: 7.8; riego: 6.9. [M] *Arreglo*: CTA tras "Qué incluye" y tras las preguntas frecuentes, con el mensaje del plan básico.
2. **Cuestionario con tono y promesas inconsistentes.** [M] "Tómate 4 minutos" y, dos líneas abajo, "4-5 minutos"; la introducción tutea y las preguntas hablan de usted ("¿Cómo nos conoció?", "¿Cómo usará…?", "Estilo que le atrae", "¿Cuál es su mayor prioridad?"); "Fotos de referencia" es un `textarea`; "Última actualización: 14 de mayo, 2026" queda suelta bajo los botones; las respuestas se pierden al recargar (sin almacenamiento); el paso 1 pide "visita técnica" antes de explicar que tiene costo (sí lo dice el encabezado). *Arreglo*: d, n.º 16 y 17; guardar el borrador en `sessionStorage`.
3. **La página de diseño no dice cuándo llega el cuestionario.** [M] El proceso menciona "Estudio de gustos y preferencias", pero no hay enlace a `/cuestionario` en diseño, mantenimiento, riego ni home (0 enlaces entrantes; tampoco está en el sitemap). [H] Está bien que no sea la puerta de entrada (el WhatsApp convierte mejor que 65 controles), pero una frase evita la sorpresa: d, n.º 18.

### 7. "Vengo de Google a un artículo" → `/blog/pasto-san-agustin-vs-japones`, `/blog`

**Funciona** [M]
- "Respuesta directa" en la pantalla 0.7, autoría y fecha, tabla comparativa, barra fija visible desde el inicio con el título del artículo dentro del mensaje, enlace al servicio a media lectura (pantalla 3.2, `blog:medio`) y bloque de cierre.

**Fricciones**
1. **El mensaje del blog no pide nada.** [M] "Hola, leí su artículo "…" y quiero cotizar." sin colonia, metros ni tipo de pasto: el vendedor empieza de cero. El índice del blog dice "vi el blog de Viveros Terra y quiero cotizar". *Arreglo*: d, n.º 8 y 9.
2. **El bloque de cierre no vende.** [M] "¿Vas a poner pasto nuevo?" + dos botones, sin precio ni garantía, cuando el artículo acaba de recomendar San Agustín. Primer CTA en línea de WhatsApp: pantalla 8.0 de 11.6. *Arreglo*: d, n.º 8.
3. **Índice del blog: 28.5 pantallas, 54 guías, sin buscador ni filtros por tema** y 25.6 pantallas sin CTA en línea. [M] *Arreglo* [H]: chips por categoría (ya existen las etiquetas "PASTO Y CÉSPED", "PALMAS", "ÁRBOLES") y un bloque de servicio cada 10–12 artículos.

### 8. "¿Dónde están y a qué hora?" → `/vivero-tampico`, `/precios`

**Funciona** [M]
- Vivero: dirección completa y "frente a Walmart" en el primer párrafo; "Cómo llegar" en el hero; Google Maps y Apple Maps; horario; entrega con costo según colonia. En escritorio, dirección y horario viven en el encabezado.
- Precios: la mejor página del sitio en CTA: 9 en línea, cada sección con botón propio y texto específico ("Cotizar pasto por WhatsApp", "Cotizar materiales por WhatsApp", "Mándanos fotos y ubicación por WhatsApp"), 10 mensajes distintos, mayor tramo sin CTA de 2.7 pantallas, ancla por categoría.

**Fricciones**
1. **El menú móvil no lleva al vivero.** [M] Sus entradas son Pasto natural, Pasto sintético, Jardín, Plantas y palmas, Empresas, Precios; la dirección aparece como texto al fondo del panel, sin enlace a `/vivero-tampico` ni a mapas, y el horario no aparece. *Arreglo*: d, n.º 19.
2. **El horario del vivero está en la pantalla ~4.5** (la línea bajo el CTA lo dice como horario de respuesta, no de apertura). [M] *Arreglo*: en la etiqueta del hero del vivero, sustituir una de las tres filas de precio por "Abierto: Lun a vie 9 a 18 h, sáb 9 a 14 h".
3. **Mensaje del hero del vivero roto respecto al patrón.** [M] `Lo que busco: ` y `Tamaño aprox.: ` van sin `___` (todos los demás mensajes del sitio lo usan); el del cierre no pide nada. *Arreglo*: d, n.º 10.

### 9. Nochebuenas → `/post/nochebuenas-tampico-madero-mayoreo`

**Funciona** [M]
- Tabla de escalones en el hero ($89 / $75 / $65), calificación de Google y CFDI arriba, cotizador con etiquetas accesibles por línea, total con preventa, "Te faltan $3,368 para entrega incluida", aviso "Se abre WhatsApp con tu pedido escrito. Tú decides si lo envías." y CTA deshabilitado con "Agrega al menos 1 pieza" cuando hay 0. Seis segmentos con mensaje propio. "50% de anticipo" solo aquí, como permite la regla.

**Fricciones**
1. **La barra fija aparece tarde.** [M] No está en scroll 0, 900 ni 2,500; aparece a ~6,000 px (pantalla 7), ya pasado el cotizador y los segmentos. Entre la 6.0 y la 14.5 no hay CTA en línea (8.5 pantallas). *Arreglo*: mostrarla en cuanto el cotizador sale de la vista y que lleve el pedido armado ("Enviar mi pedido · 60 pzas · $6,213").
2. **Botón secundario del hero: "WhatsApp"**, sin verbo, junto a "Cotizar mi pedido →". [M] Compiten dos acciones sin que se entienda la diferencia. *Arreglo*: d, n.º 20.
3. **"Escalón: Menudeo / Mayoreo Plus" es vocabulario interno** y entra al mensaje del cliente. Y falta garantía/condiciones: 0 apariciones de "garantía" en la página. [M] *Arreglo* [H]: "Precio de menudeo (1 a 11 piezas)"; una pregunta frecuente "¿Qué pasa si una llega dañada?" con la respuesta que el dueño defina (no la invento).

### 10. Navegación, pie, migas, 404, búsqueda

**Funciona** [M]
- Menú móvil: botón de 44 × 44 con `aria-expanded` y `aria-controls`, se cierra con Escape, cada grupo muestra un dato ("desde $85/m²", "+200 variedades", "REPSE · CFDI 4.0") y trae "Cotizar por WhatsApp" dentro. Cerrado mide 656 px: cabe sin scroll.
- Migas en todas las plantillas (`nav[aria-label="Ruta de navegación"]`). Pie completo: servicios, materiales, zonas, vivero, contacto, domicilio, horario, REPSE, redes.
- 404 real (estado 404), con buscador, 18 destinos, CTA con mensaje propio ("busqué una página en su sitio y no la encontré. Necesito: ___") y barra fija. `/sistemas-riego-tampico` (plural) cae aquí y "Sistemas de riego" está en la lista.

**Fricciones**
1. **Agrupación.** [M] "Plantas y palmas" contiene 12 enlaces, entre ellos tierra, tezontle, mármol, piedra y Nochebuenas; "Jardín" (diseño, mantenimiento, riego) no dice que son servicios; "Mantenimiento" aparece en dos grupos; no hay "Vivero", "Blog" ni "Contacto". En escritorio "Jardín" y "Empresas" son solo botón (sin página propia), mientras los otros tres grupos son enlace + botón: comportamiento desigual. *Arreglo*: d, n.º 19.
2. **Búsqueda del 404 limitada a la lista visible.** [M] "riego" y "cesped" encuentran; "nochebuena" y "palma real" no (Nochebuenas no está entre los 18 destinos). *Arreglo*: añadir Nochebuenas, Palmas, Catálogo y Mayoreo de palmas, con sinónimos (nochebuena, flor de pascua, zacate, grava).
3. **Siete enlaces de salida en el pie** (Maps, Facebook, Instagram, TikTok, YouTube, LinkedIn) en todas las páginas. [H] En el pie el riesgo es bajo; no los movería más arriba. El único enlace de salida en el cuerpo de páginas dinero es el padrón REPSE de la STPS (mayoreo, 3 veces): aporta confianza, pero conviene abrirlo en pestaña nueva [no verifiqué el `target` en todos].

---

## (c) CTA por plantilla (móvil 375 px) [M]

"En línea" excluye encabezado, menú, pie y barra. "Mensajes" = mensajes prellenados distintos en la página. Hero ≤ 667/812 = el CTA del hero queda completo dentro del primer pantallazo.

| Plantilla (página medida) | Pantallas | WA en línea | `data-cta` (prefijo: sufijos) | Texto del botón | Mensajes | Hero ≤667 / ≤812 | Mayor tramo sin CTA en línea | Barra fija | Tel. visibles |
|---|---|---|---|---|---|---|---|---|---|
| Servicio pasto (`/pasto-en-rollo-tampico`) | 26.1 | 4 | `servicio-pasto`: header, menu, hero, medidor, simulador, cierre, footer, barra | "Cotizar por WhatsApp →" ×4 | 2 (+ dinámicos) | no / sí | 9.7 (0.9→10.6) | sí, genérica | 3 |
| Servicio mantenimiento | 26.6 | 5 | `servicio-mantenimiento`: hero, opcion-1..3, cierre, barra | idéntico ×5 | 4 | sí / sí | **14.5** (9.3→23.8) | sí | 3 |
| Servicio diseño | 23.7 | 6 | `servicio-diseno`: hero, opcion-1..3, simulador, cierre, barra | idéntico ×6 | 5 | no / sí | 7.8 | sí | 3 |
| Servicio riego | 22.9 | 6 | `servicio-riego`: ídem | idéntico ×6 | 5 | no / sí | 6.9 | sí | 3 |
| Sintético local (`/pasto-sintetico-tampico`) | 22.7 | 5 | `servicio-sintetico`: hero, opcion-1..2, cotizador, cierre, visita (tel) + `tienda:lista`, `tienda:barra` | idéntico ×5 | 4 | no / sí | 7.4 | de compra, tardía | 4 |
| Tienda hub (`/pasto-sintetico`) | 24.1 | 3 | `tienda`: header, hero, cotizador, cierre, lista, barra | "Cotizar por WhatsApp" ×3 | 3 | no / sí | **12.1** (9.3→21.4) | **no aparece** con lista vacía | 3 |
| Tienda ficha (`/toscana-28`) | 17.9 | 2 | `tienda`: header, cotizador, cierre, lista, barra | ídem | 4 | **no / no** (primer CTA en 3.5) | **11.7** | de compra desde ~pantalla 7, 130 px | 2 |
| Tienda ciudad (`/envio/monterrey`) | 10.7 | 2 | `ciudad`: header, hero, cierre, barra | ídem | 3 | sí / sí | 7.4 | sí | 2 |
| Plantas hub | 23.0 | 2 | `plantas`: header, hero, cierre, barra, catalogo (enlace) | ídem | 1 | no / sí | **19.5** | sí | 3 |
| Plantas categoría (palmas) | 18.5 | 2 | `plantas`: ídem | ídem | 1 | no / sí | **15.0** | sí | 3 |
| Catálogo | 43.8 | 2 | `catalogo`: header, hero, solEsp, solEsp-vacio, sendWA | "Cotizar por WhatsApp →", "Preguntar por WhatsApp" | 2 (+ lista) | sí / sí | **39.1** | solo "Mi lista" tras agregar | 2 |
| Material (tierra, tezontle) | 18.5–19.0 | 3 | `material`: header, hero, cotizarCalculado, cierre, cuerpo (tel), barra | idéntico ×3 | 1 (+ dinámico) | no / sí | 7.6–8.0 | sí | 4 |
| B2B (mayoreo pasto, palmas) | 21.7–22.2 | 6 | `b2b`: header, hero, cotizador/armador, opcion-1..3, cierre, barra | idéntico ×6 | 4 | no / sí | 7.1–7.3 | sí | 3 |
| Zona (`/jardineria-ciudad-madero`) | 9.8 | 3 | `zona`: header, hero, precios, cierre, barra | "Cotizar por WhatsApp →", "Cotizar en Cd. Madero" | 1 | sí / sí | 4.1 | sí | 3 |
| Vivero | 8.7 | 2 | `vivero`: header, hero, cierre, barra | idéntico ×2 | 3 | sí / sí | 5.3 | sí | 3 |
| Precios | 17.1 | **9** | `precios`: header, hero, pasto, poda, servicios, sintetico, materiales, plantas, simulador, cierre, barra | **específico por sección** | **10** | no / sí | **2.7** | sí | 3 |
| Nochebuenas | 17.2 | 9 | `nochebuenas`: header, hero, cotizador, para-empresas/hoteles/comercios/gobierno/posadas/iglesias, cierre | específico por segmento; "WhatsApp" en hero | 8 | no / sí | 8.5 (6.0→14.5) | tardía (~pantalla 7), "Cotizar mi pedido" | 2 |
| Blog artículo | 11.6 | 1 | `blog`: header, medio, margen, landing (enlaces al servicio), cierre, barra | "Cotizar por WhatsApp →" | 1 (0 campos) | — (primer CTA en 8.0) | 8.0 | sí, desde el inicio | 2 |
| Blog índice | 28.5 | 2 | `blog`: header, hero, cierre, barra | ídem | 1 (0 campos) | sí / sí | **25.6** | sí | 3 |
| Políticas | 11.1 | 1 | `utilidad` | ídem | 2 | — | 8.4 | sí | 3 |
| 404 | 4.6 | 1 | `utilidad`: header, cierre, barra | ídem | 2 | — | 2.7 | sí | 3 |
| Cuestionario / Datos de envío | 3.9 / 4.1 | 0 | `utilidad:header` | "Cotizar" | 1 | — | — | no (correcto) | 1 |

Observaciones transversales [M]:
- El "Cotizar" del encabezado está en todas las páginas y siempre lleva el mensaje genérico de la plantilla, nunca el contexto elegido.
- CTA que compiten: en todos los heros, WhatsApp (sólido) + "Llamar 833 326 8008" (contorno): jerarquía correcta. En Nochebuenas compiten "Cotizar mi pedido →" (ancla) y "WhatsApp". En la ficha de tienda, "Cotizar por WhatsApp" y "Agregar a mi cotización" van juntos con el mismo peso visual aproximado [H: revisar en captura `B6_ficha_cot_NL7.png`].
- La barra `vt-bar` mide 56 px (7–8 % del alto) y no tapa contenido en las capturas revisadas; la de compra de la ficha mide 130 px.

---

## (d) Las 20 reescrituras

Todas respetan las reglas del dueño: sin cifras nuevas, sin "gratis"/"sin costo" (salvo la garantía de arraigo, que no se toca), sin "más vendido", sin plazos de entrega, sin porcentajes de anticipo fuera de Nochebuenas, "menos de 1 hora" siempre con "en horario", visita con costo, IVA como lo publica el sitio.

| # | Página · elemento | Antes | Después |
|---|---|---|---|
| 1 | `/pasto-en-rollo-tampico` · botón del medidor (y de las calculadoras de tierra y mayoreo) cuando ya hay resultado | "Cotizar por WhatsApp →" | "Enviar mi cálculo por WhatsApp →" (sin resultado: "Cotizar sin medidas por WhatsApp →") |
| 2 | Ídem · aviso de error del medidor (hoy no existe; con 0, negativo o letras solo vuelve a "Escribe tus medidas") | — | "Escribe el largo y el ancho en metros, solo con números. Ejemplo: 8 y 6." |
| 3 | Simulador de mensualidades (pasto, diseño, riego, precios) · mensaje cuando el cliente no cambió el monto | "Hola, quiero cotizar pasto en rollo instalado. / Mi cotización es de $12,000. / Pagaría de contado." | "Hola, quiero cotizar pasto en rollo instalado y me interesa pagar con tarjeta en mensualidades. / Colonia: ___ / Metros aprox.: ___ / / Vengo de viverosterra.com" (si escribió un monto, conservar la línea del monto y añadir "Colonia: ___") |
| 4 | Barra fija y "Cotizar" del encabezado después de usar una calculadora | "Cotizar por WhatsApp" (mensaje genérico con huecos) | "Enviar mi cálculo" (mismo mensaje que el botón de la calculadora) |
| 5 | Mantenimiento, diseño, riego, mayoreo · botones de las tarjetas de plan | "Cotizar por WhatsApp →" en las tres | Mantenimiento: "Cotizar el plan básico →" / "Cotizar el plan premium →" / "Cotizar para mi empresa →". Diseño: "Quiero el Esencial ($3,000) →" / "Quiero el Completo ($6,500) →" / "Cotizar el Premium →". Riego: "Cotizar aspersores →" / "Cotizar goteo →" / "Cotizar un área grande →". Mayoreo: "Cotizar solo el pasto →" / "Cotizar pasto instalado →" / "Cotizar pasto, palmas y riego →" |
| 6 | `/catalogo` · mensaje del CTA del hero | "Hola, vi el catálogo y quiero cotizar una planta / / Vengo de viverosterra.com" | "Hola, vi el catálogo y quiero cotizar plantas. / Planta o plantas: ___ / Tamaño aprox.: ___ / Piezas: ___ / Colonia de entrega: ___ / / Vengo de viverosterra.com" |
| 7 | `/catalogo` · barra de la lista y mensaje de la lista | Barra: "Mi lista 1". Mensaje: "…Total: 1 variedad, 1 unidad / ¿Pueden darme precio y disponibilidad?" | Barra: "Mi lista · 1 variedad · 1 pieza" + botón "Cotizar". Mensaje: añadir antes de la pregunta "Colonia de entrega: ___" y cerrar con "¿Me dan precio y disponibilidad?" |
| 8 | Artículos del blog · bloque de cierre y mensaje | Título "¿Vas a poner pasto nuevo?" + botones. Mensaje: "Hola, leí su artículo "…" y quiero cotizar." | Título: "¿Vas a poner pasto nuevo?" Texto: "Pasto San Agustín a $85/m² solo el pasto y desde $120/m² instalado, con garantía de arraigo de 15 a 20 días si lo instalamos." Mensaje: "Hola, leí su artículo "…" y quiero cotizar pasto. / Colonia: ___ / Metros aprox.: ___ / Solo el pasto o instalado: ___ / / Vengo de viverosterra.com" (en artículos de otros temas, los campos de la página de servicio correspondiente) |
| 9 | `/blog` · mensaje del hero y del cierre | "Hola, vi el blog de Viveros Terra y quiero cotizar" | "Hola, quiero cotizar: ___ / Colonia: ___ / Metros aprox.: ___ / / Vengo de viverosterra.com" |
| 10 | `/vivero-tampico` · mensaje del hero y botón del cierre | "Hola, quiero visitar el vivero o cotizar plantas. / Lo que busco: / Tamaño aprox.: " (sin `___`). Cierre: "Cotizar por WhatsApp →" | "Hola, quiero visitar el vivero o cotizar plantas. / Lo que busco: ___ / Tamaño aprox.: ___ / Colonia: ___ / / Vengo de viverosterra.com". Botón del cierre: "Preguntar si la tienen →" |
| 11 | `/pasto-sintetico` · mensaje de hero y encabezado después de elegir estado | "Hola, quiero cotizar pasto sintético. / Ciudad o colonia: ___ / Metros aprox.: ___" | "Hola, quiero cotizar pasto sintético con envío a Nuevo León. / Ciudad: ___ / Metros aprox.: ___ / Modelo (si ya lo elegiste): ___ / / Vengo de viverosterra.com" |
| 12 | Fichas de la tienda · CTA nuevo bajo la etiqueta de precio y mensaje del encabezado | No hay CTA de WhatsApp hasta la pantalla 3.5; el encabezado abre el mensaje genérico | Botón: "Cotizar Toscana 28 por WhatsApp →". Mensaje (el que ya usa el cierre): "Hola, quiero cotizar el pasto sintético Toscana 28. / Mi estado: ___ / Metros aprox.: ___ / / Vengo de viverosterra.com" |
| 13 | Tienda · nombres de la lista | "Mi lista" / "Tu lista" / "Agregar a mi cotización" / "+ Agregar" / "+ Agregar · 1 rollo" | Botón y título: "Mi lista". Acciones: "Agregar a mi lista" (tarjetas y cotizador) y "Agregar 1 rollo a mi lista" (comparativa). Aviso: "Toscana 28 · 50 m² en tu lista · Ver" (se queda) |
| 14 | Tienda · aviso de mínimo en el cotizador | "Para envío nacional el mínimo es 25 m² (medio rollo)." | "Para envío nacional el mínimo es 25 m² (medio rollo). Sube a 25 m² o elige "Recoger en showroom, Cd. Madero", donde vendemos desde 2 m²." |
| 15 | `/tierra-negra-vegetal-tampico` · mensaje de la calculadora | "…Resultado de la calculadora: / Área: 30 m² / Capa: 8 cm / Cantidad: 2.4 m³ / Colonia de entrega: ___ / / ¿Me pueden dar precio de entrega a domicilio en Tampico, Madero o Altamira?" | "Hola, quiero cotizar tierra negra. / Área: 30 m², capa de 8 cm = 2.4 m³ (cálculo de la web) / En costales o a granel: ___ / Colonia de entrega: ___ / ¿Me dan el total con entrega? / / Vengo de viverosterra.com" |
| 16 | Tierra/tezontle y mayoreo · bloque de correo | Tierra: "Escríbenos para cotizar" + botón "Enviar solicitud de pedido". Mayoreo: "¿Compras prefiere correo? Pide la cotización por escrito" | Tierra: "¿Prefieres correo? Pide tu cotización aquí" + botón "Pedir cotización por correo". Mayoreo: "¿Tu área de compras pide la cotización por correo? Solicítala aquí" (botón "Enviar solicitud por correo" se queda) |
| 17 | `/cuestionario` · introducción y línea de datos | "Tómate 4 minutos para contarnos qué necesitas. Nuestro diseñador creará una propuesta hecha exactamente para ti; te respondemos en menos de 1 hora en horario." + "Visita para medir y cotizar: su costo depende de la ubicación · Diseño personalizado · 4-5 minutos" | "Son 5 pasos y toma de 4 a 5 minutos. Solo tu nombre y tu WhatsApp son obligatorios; lo demás nos ayuda a proponerte un diseño a tu medida. Al enviarlo te escribimos por WhatsApp en menos de 1 hora en horario." + "Si hace falta una visita para medir, su costo depende de la ubicación y te lo confirmamos antes de agendar." |
| 18 | `/cuestionario` · preguntas en "usted", campo de fotos y botón final | "¿Cómo nos conoció?" · "¿Cómo usará principalmente el jardín?" · "Estilo que le atrae" · "¿Prefiere árboles o palmas?" · "Plantas que le gustan o quiere incluir" · "¿Cuándo le gustaría iniciar la ejecución?" · "¿Cuál es su mayor prioridad?" · "Fotos de referencia" · "Enviar cuestionario" | "¿Cómo nos conociste?" · "¿Cómo vas a usar el jardín?" · "Estilo que te atrae" · "¿Prefieres árboles o palmas?" · "Plantas que te gustan o quieres incluir" · "¿Cuándo te gustaría empezar la obra?" · "¿Qué es lo más importante para ti?" · "Referencias: pega un enlace de Pinterest o Instagram, o descríbelo. Las fotos de tu jardín nos las mandas por WhatsApp." · "Enviar mis respuestas" |
| 19 | `/diseno-jardines-tampico` · paso "Estudio de gustos y preferencias" del proceso (añadir una frase) y menú | Paso sin mención del cuestionario. Menú: "Jardín · desde $750/mes"; sin entrada al vivero | Frase: "Después de tu primer mensaje te mandamos por WhatsApp un cuestionario de 5 pasos para conocer tus gustos." Menú: "Servicios de jardín · desde $750/mes"; nueva entrada "Vivero y horario" (a `/vivero-tampico`) y "Blog"; mover tierra, tezontle, mármol y piedra a un grupo "Tierra y piedra" |
| 20 | Nochebuenas · botón secundario del hero y "escalón" | "WhatsApp" · "Escalón Menudeo" / "Escalón: Mayoreo Plus" | "Preguntar por WhatsApp" · "Precio de menudeo (1 a 11 piezas)" / "Precio de mayoreo plus (50 a 199 piezas)"; en el mensaje: "Precio aplicado: mayoreo plus" |

Textos menores, fuera de las 20 [M sobre el "antes"]:
- Titulares que no dicen nada: "Lo que entregamos, documentado." → "Así queda el pasto, etapa por etapa"; "Servicios de mantenimiento profesional" → "Qué hacemos en cada visita"; "Resultados comprobados en Tampico" (riego) → "Lo que dicen quienes ya tienen riego automático"; "Otros servicios de Viveros Terra" → "Lo que suele seguir después del pasto / del diseño / del riego".
- Jerga: "+200 proyectos B2B" → "+200 proyectos para empresas"; "tendemos tepes de 40 × 60 cm" → "colocamos los rollos (tepes) de 40 × 60 cm"; "Stenotaphrum secundatum" en la etiqueta de precio → quitarlo de la etiqueta y dejarlo en el párrafo de variedad; "2 a 4 bar" (riego) sin explicación.
- `/datos-envio`: "Revisa los campos marcados en rojo." → un mensaje por campo: "Falta el código postal (5 dígitos).", "Escribe nombre y apellido de quien recibe.", "El teléfono debe tener 10 dígitos.", "Revisa el RFC: 12 o 13 caracteres, sin espacios."
- Tarjetas de palmas: "Agregar Palma Areca en Arma tu lista" → "Añadir Palma Areca a mi lista". Catálogo: "Ficha" → "Guía de cuidados".
- 404, sin coincidencias: "No hay coincidencias. Escríbenos por WhatsApp y te ayudamos." → "No encontramos eso en el sitio. Dinos qué buscas por WhatsApp y te decimos si lo manejamos."

---

## (e) Top 15 de mejoras por impacto esperado en clics a WhatsApp

Impacto y esfuerzo son estimaciones [H]. Medición con lo que ya existe: `generate_lead` (`method: whatsapp|formulario`, `cta_id`, `service`), `click_to_call`, `select_content`. Comparar siempre por página: `generate_lead` / sesiones de esa página, 2–4 semanas antes y después, y vigilar que el total de la página suba (no solo que se muevan clics de un `cta_id` a otro).

| # | Mejora | Impacto | Esfuerzo | Cómo medir |
|---|---|---|---|---|
| 1 | Barra fija y encabezado heredan el mensaje de la calculadora (pasto, tierra, mayoreo, simulador) y el estado/modelo en tienda | Alto | Medio (JS compartido) | Añadir sufijo al `cta_id` cuando el mensaje va enriquecido (p. ej. `servicio-pasto:barra-calc`); tasa de `…:barra*` + `…:header*` por sesión, y % de leads "con cálculo" |
| 2 | Ficha de tienda: CTA de WhatsApp bajo la etiqueta de precio con el modelo en el mensaje; barra de compra más temprana y de una línea | Alto | Bajo-medio | Nuevo `tienda:ficha-hero`; `generate_lead` por sesión en `/pasto-sintetico/*`; reparto frente a `tienda:cotizador` y `tienda:barra` |
| 3 | Hub de tienda: barra fija también con la lista vacía y CTA tras "¿Qué pasto te conviene?" y tras la comparativa | Alto | Bajo | `tienda:barra` y nuevos `tienda:quiz`, `tienda:comparativa` |
| 4 | Catálogo: barra de lista con botón "Cotizar" directo, barra visible desde el inicio y mensaje con colonia | Alto | Medio | `catalogo:sendWA` por sesión; razón `sendWA` / sesiones con ≥ 1 artículo (hoy medible con el evento de agregar, si existe; si no, añadirlo) |
| 5 | Texto de botón específico en tarjetas de plan (reescritura 5) | Medio-alto | Bajo (solo texto) | `…:opcion-1/2/3` por sesión en mantenimiento, diseño, riego, mayoreo |
| 6 | Plantas y palmas: CTA en línea tras la rejilla de especies y tras "¿Cuánto cuesta una palma?"; garantía de 30 días bajo el CTA del hero | Medio-alto | Bajo | Nuevos `plantas:especies`, `plantas:precio`; total `plantas:*` por sesión |
| 7 | Mantenimiento: CTA tras "Qué incluye" y tras preguntas (hoy 14.5 pantallas sin CTA en línea) | Medio | Bajo | Nuevos `servicio-mantenimiento:incluye`, `:faq` |
| 8 | Blog: mensaje con campos por tema y bloque de cierre con precio y garantía (reescrituras 8 y 9) | Medio (mucho tráfico de entrada) | Bajo-medio (plantilla + mapa tema→servicio) | `blog:cierre`, `blog:barra` por sesión de `/blog/*`; `select_content` de `blog:medio/landing` hacia el servicio |
| 9 | Prueba social en tienda, plantas y Nochebuenas: "4.6 en Google (24 reseñas)" y tira de garantía/devoluciones junto al CTA del cotizador y en páginas de ciudad | Medio | Bajo | `tienda:cotizador`, `ciudad:hero`, `ciudad:cierre` por sesión |
| 10 | Pasto en rollo: "Calcular mi patio" como botón secundario del hero y CTA tras testimonios | Medio | Bajo | `select_content` del ancla al medidor; `servicio-pasto:medidor` por sesión |
| 11 | Nochebuenas: barra temprana con el pedido armado y botón secundario con verbo | Medio (temporada en curso) | Bajo | `nochebuenas:cotizador` + `nochebuenas:barra` (hoy la barra es ancla: darle `data-cta`) |
| 12 | Mensajes del catálogo-hero, vivero y simulador con campos correctos (reescrituras 3, 6, 10) | Medio-bajo en clics, alto en calidad del lead | Bajo | No cambia el clic; medir en WhatsApp: % de primeros mensajes que llegan con colonia y metros (muestreo manual semanal) |
| 13 | Menú: "Vivero y horario", "Servicios de jardín", grupo "Tierra y piedra" | Medio-bajo | Bajo | `…:menu` por sesión; páginas vistas de `/vivero-tampico` desde menú; `click_to_call` y clics a Maps |
| 14 | Avisos de error en calculadoras y errores por campo en `/datos-envio`; `autocomplete` en dirección y teléfono | Bajo-medio | Bajo | Proporción de sesiones que interactúan con el medidor y terminan en `…:medidor`; en datos de envío, tasa de finalización (añadir evento al mostrar `#done`) |
| 15 | Cuestionario: unificar tono, texto de introducción, borrador en `sessionStorage` | Bajo en clics; mejora de finalización | Bajo-medio | `generate_lead` con `method: formulario` / vistas de `/cuestionario`; añadir evento por paso para ver dónde abandonan |

---

## (f) Qué no hacer

- **No poner un carrito ni pago en línea en la tienda.** El flujo "cotiza → confirmamos flete → pagas" está bien explicado y el mensaje de la lista llega completo; un carrito añadiría un paso que hoy no existe y rompería el cierre por WhatsApp.
- **No convertir el cuestionario en puerta de entrada** ni enlazarlo desde los heros: 65 controles frente a un mensaje de 3 huecos. Su lugar es después del primer contacto.
- **No añadir ventanas emergentes, chat flotante ni un segundo botón flotante de WhatsApp.** Ya hay encabezado fijo + barra; un tercero taparía contenido en 667 px.
- **No quitar la vista previa "El mensaje que se abre"** ni el aviso "Tú decides si lo envías": reducen el miedo a tocar el botón.
- **No recortar el contenido largo de las páginas de servicio** para "acortar el scroll": responde objeciones reales (precio, IVA, garantía, pago). El problema es la distancia entre CTA, no la longitud.
- **No añadir urgencia** ("últimos rollos", cuentas regresivas en Nochebuenas), ni "gratis", ni plazos, ni porcentajes de anticipo fuera de Nochebuenas, ni "más vendido" para destacar modelos; usar "el que más recomendamos en…" solo donde ya está publicado.
- **No reducir los mensajes prellenados a una sola línea** para que "se vean cortos": los huecos `___` son lo que hace cotizable el primer mensaje. Tampoco pasar de 4–5 huecos.
- **No mover las redes sociales ni los enlaces externos hacia arriba**; en el pie no estorban.
- **No cambiar los `data-cta` existentes** al renombrar botones: se perdería la serie histórica. Los CTA nuevos llevan sufijos nuevos.
- **No tocar el texto, los emojis ni el bloque `#VT1` del mensaje de `/datos-envio`**: el propio script indica que lo lee un sistema del dueño.

---

## (g) Lo que no pude verificar

- **Comportamiento real de los usuarios**: no tuve acceso a GA4 ni a las conversaciones de WhatsApp. Todo lo marcado [H], los impactos y el orden del top 15 son estimaciones; no sé qué `cta_id` genera hoy más leads.
- **Apertura real de WhatsApp y llamadas**: no hice clic en wa.me/tel. No comprobé cómo se ve el mensaje en la app, si los saltos de línea y los `___` llegan bien, ni el comportamiento en escritorio sin WhatsApp instalado.
- **Envío de formularios**: no envié el cuestionario ni los formularios de correo (formsubmit). No verifiqué el correo que recibe el negocio, el antispam, la redirección real a `/gracias` ni qué pasa si el servicio externo falla. `/gracias` la vi entrando directo. El botón de `/datos-envio` no se pulsó: su validación y su mensaje se leyeron del código.
- **Safari iOS y Android reales**: usé Chromium con UA de iPhone. No verifiqué la barra fija con la barra de direcciones dinámica de Safari, el zoom al enfocar campos, los teclados reales, ni Firefox/Safari de escritorio. Los mensajes de validación nativos los vi en inglés por el navegador de prueba; en un teléfono en español salen en español.
- **Contenido de terceros**: bloqueé todo lo que no fuera viverosterra.com, así que no vi fuentes externas, mapas incrustados, analítica ni ningún widget externo si lo hay.
- **Imágenes**: en las capturas de página completa muchas aparecen en blanco por carga diferida; no evalué fotos ni su peso.
- **Lector de pantalla y contraste**: revisé etiquetas, roles, foco, enlace de salto y tamaño de objetivos por DOM; no usé VoiceOver/TalkBack ni medí contraste de color.
- **Escritorio**: a 1440×900 revisé navegación, hero de pasto, ficha de tienda, catálogo y precios; no repetí cada recorrido completo.
- **Cobertura**: medí 28 URL de las 107 del sitemap (una o dos por plantilla). No revisé las 8 fichas restantes de la tienda, las otras 10 páginas de ciudad, 53 artículos del blog, 5 páginas de zona, mármol/piedra, `/pasto-sintetico/perros`, `/protocolo-cuidados-pasto-san-agustin` ni `/politica-privacidad`; asumo que heredan su plantilla.
- **Veracidad del contenido**: no validé precios, testimonios, cifras ("+500,000 m²", "+200 proyectos", "117 especies" frente a 120 tarjetas y "+200 variedades") ni si los plazos publicados chocan con la regla del dueño; solo los señalo.
- **Persistencia de la lista del catálogo**: sobrevive a una recarga, pero no determiné con certeza el mecanismo (el `localStorage` leído salió vacío) ni si sobrevive al cerrar la pestaña.
