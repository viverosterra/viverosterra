# Auditoría visual · viverosterra.com · sistema y héroes por plantilla

Fecha: 2026-11-10 · Producción, solo lectura (GET) · Playwright/Chromium a 375×812 (DSF 2), 1440×900 y 768×1024, más 375×667 y 1366×768 en tres páginas · `reduced_motion="reduce"` · todo host ajeno bloqueado · 22 páginas.

Evidencia en esta misma carpeta: `<pagina>-m-hero.jpg`, `<pagina>-d-hero.jpg`, `<pagina>-m-hoja.jpg` (página completa en columnas), `<pagina>-{m,d,t}.json` (medidas), `heroes-m-1..5.jpg`, `heroes-d-1..11.jpg` (hojas de contacto), `pliegue-667.jpg`, `pliegue-1366.jpg`, `movimiento.json`. Scripts: `auditar.py`, `resumen.py`, `extra.py`.

Convención: **[M]** = hecho medido o leído en CSS/plantilla · **[O]** = opinión de dirección de arte.

---

## (a) Resumen ejecutivo

1. **[M]** El sistema base es sólido y coherente: 0 páginas con scroll horizontal, CLS 0.000 en 21 de 22 (catálogo 0.024 en escritorio), contraste mínimo de texto 5.19:1 (todo pasa AA), un solo radio (2 px; 6 px solo en la etiqueta), una sola sombra de tarjeta, foco visible uniforme (2 px verde, offset 2 px).
2. **[M]** El hero nuevo de la home **no se propagó**: el botón alto con sombra amarilla (62–66 px, `box-shadow:5px 5px 0 #F2D24B`) existe solo en `.vt-inicio`. Las otras 20 plantillas usan el `.vt-btn--wa` plano de 52 px/16 px, sin sombra, seguido de un botón "Llamar" del mismo tamaño.
3. **[M]** En celular **ninguna plantilla interior muestra foto en la primera pantalla** (la foto empieza en y=797–1031 px; el alto útil es 812). El hero interior es: migas + kicker + titular + párrafo + etiqueta + 2 botones. Todo texto.
4. **[M]** En un celular de 667 px de alto útil, el CTA del hero queda fuera de pantalla en 13 de 21 plantillas (p. ej. pasto en rollo: CTA en y=738–790). Lo "rescata" la barra fija inferior, que a esa altura tapa la etiqueta de precio (`pliegue-667.jpg`).
5. **[M]** Las páginas son muy largas en celular: servicios 23–27 pantallas, blog 28.5, catálogo 43.8, tienda 24. Todas las secciones usan el mismo relleno (56/56 px en móvil) y el mismo esqueleto (número + rótulo + h2 + párrafo + tarjetas blancas apiladas).
6. **[M]** Solo la home tiene movimiento de entrada (etiqueta que se balancea, foto que se descubre, h2 y fotos que suben). El resto: cero animaciones; solo `hover` de botón, flecha y `.vt-tarjeta`.
7. **[M]** Hay un defecto tipográfico visible: en materiales (tierra negra, tezontle) el lema del h1 va en `<em>` y se pinta en Archivo 800 **cursiva sintética** negra, no en Fraunces verde como el resto.
8. **[O]** La marca está bien definida, pero fuera de la home se ve "de plantilla": mismo hero 15 veces, sin foto arriba en móvil, CTA sin peso propio y ningún momento oscuro o a sangre hasta el cierre.
9. **[O]** La mejora de mayor retorno es un solo componente de "hero de marca" (sección d) aplicado desde `componentes.py`: botón alto con sombra, foto visible en la primera pantalla móvil con la etiqueta colgada encima y una línea de confianza. Es CSS + una función de plantilla; no requiere fotos nuevas.
10. **[O]** Segundo frente: romper la monotonía con 2 momentos por página (banda oscura de garantía a media página y franja de fotos a sangre) y recortar longitud en móvil con acordeones en tablas comparativas y especies.

---

## (b) Ranking de héroes (mejor a peor)

Criterio: impacto en la primera pantalla móvil y de escritorio, jerarquía, peso del CTA, parecido con el hero de la home. **[O]** salvo las cifras.

| # | Plantilla | Una frase |
|---|-----------|-----------|
| 1 | `/` home | La vara: titular 44.9/92 px, lema serif verde, etiqueta colgada sobre la foto en escritorio, botón 62/66 px con sombra amarilla, línea de confianza con 4.6 en Google; en móvil tampoco muestra foto arriba (y=823). |
| 2 | `/pasto-sintetico/toscana-28` ficha | En escritorio es el único interior con foto dominante (938 px de alto) y etiqueta al lado; en móvil no hay CTA en el hero (primer WhatsApp en y=2881) y depende de la barra de compra. |
| 3 | `/pasto-en-rollo-tampico` | Mejor titular y lema del sitio ("Del campo a tu jardín, sin pasar por bodega"), pero en móvil el CTA cae a y=738 y a 1366×768 el precio queda cortado (`pliegue-1366.jpg`). |
| 4 | `/mantenimiento-jardines-tampico` | Lede corto: etiqueta y CTA (y=540) caben holgados; la foto del jardinero con uniforme es la mejor de los servicios. |
| 5 | `/sistema-riego-tampico` | Lema con cifra ("ahorra hasta 40% de agua") y buena foto; CTA en y=621. |
| 6 | `/jardineria-altamira` zona | Compacto y claro (CTA y=535); foto genérica de paisaje, sin gente ni logo. |
| 7 | `/vivero-tampico` | Correcto, pero la etiqueta dice "Palmas desde $250" en una página cuyo objetivo es "cómo llegar": el precio no es el dato del hero. |
| 8 | `/diseno-jardines-tampico` | Foto de hojas sin jardín terminado; para "diseño" falta el resultado. Lede de 5 renglones en móvil. |
| 9 | `/pasto-sintetico-tampico` | Subnavegación + "Mi lista" + migas consumen 138 px antes del kicker; precio "$446.60" poco redondo; CTA en y=721. |
| 10 | `/plantas-palmas-arboles-tampico` hub | Sin lema serif; titular de 3 renglones; en un vivero de 200 variedades el hero móvil no enseña una sola planta. |
| 11 | `/palmas-tropicales-tampico` | Igual que el hub, con lede de 6 renglones (168 px) que empuja todo. |
| 12 | `/mayoreo-pasto-tampico` | Lede de 7 renglones (196 px) antes del precio; repite la foto de la home. |
| 13 | `/palmas-mayoreo-proyectos` | Mismo patrón que mayoreo; la foto de palmas en bolsa sí comunica volumen. |
| 14 | `/precios` | Lema "2026" suelto en serif (no es un lema); repite la foto de pasto en rollo; CTA en y=719. |
| 15 | `/post/nochebuenas-…` | Dos botones invertidos: el principal "Cotizar mi pedido" no lleva glifo y el secundario "WhatsApp" sí; ancho 194 px en escritorio. Buena foto roja, que en móvil no se ve. |
| 16 | `/pasto-sintetico` tienda | Hero-formulario: selector de estado + precio resaltado + 2 botones + 3 renglones de notas; el precio usa otro lenguaje (resaltador, no etiqueta). Funcional, no impresiona. |
| 17 | `/pasto-sintetico/envio/monterrey` ciudad | Sin etiqueta ni precio destacado (el $162/m² va dentro del párrafo); en escritorio queda un hueco grande bajo los botones. |
| 18 | `/tierra-negra-vegetal-tampico` material | Titular con cursiva sintética negra (defecto); lede de 7 renglones; foto apaisada chica (334 px) que deja media columna vacía en escritorio. |
| 19 | `/cuestionario` | Titular 36/64 px con serif en tinta (no verde); sin CTA de WhatsApp; es un formulario, se entiende, pero la foto es oscura y recortada. |
| 20 | `/blog` | Titular 36/71 px en Title Case, sin lema, foto chica (289 px) flotando a la derecha; los botones de WhatsApp/Llamar aquí son ruido. |
| 21 | `/catalogo` | Titular 32/56 px en Title Case en un renglón, dos párrafos, dos botones a todo lo ancho (623 px cada uno) y luego filtros: cabecera de herramienta, no hero. |
| 22 | `/blog/pasto-san-agustin-vs-japones` artículo | Sin imagen alguna en toda la página (0 `img` en el cuerpo), titular de 4 renglones a 32/64 px, y la barra fija tapa la "respuesta directa" desde la carga en móvil. |

---

## (c) Hallazgos por severidad

### ALTO

**A1. El CTA del hero interior no tiene el tratamiento de la home.**
- **[M]** `home`: `.vt-inicio__cta .vt-btn--wa` 343×62 px, 19 px/600, `box-shadow: 5px 5px 0 rgb(242,210,75)` (móvil); 331×66 px, 20 px (escritorio). Resto (20 plantillas): `.vt-cta .vt-btn--wa` 343×52 px, 16 px, `box-shadow:none`; en escritorio 259×52 px. Regla en `public/css/terra-inicio.css:14-18`, limitada a `.vt-inicio`.
- **[M]** En el hero interior, "Llamar 833 326 8008" (`.vt-btn--linea`) mide lo mismo que el principal (343×52): dos botones del mismo peso apilados.
- **[O]** El verde plano de 52 px sobre hueso compite con la etiqueta amarilla, que es más llamativa. En la home gana el botón; en el resto gana el precio.
- **Arreglo:** mover la regla a `terra.css` como modificador `.vt-btn--principal` (min-height 60 px móvil / 64 px escritorio, 1.1875rem, sombra amarilla 5/5/0, estados hover/active/focus ya escritos en `terra-inicio.css:14-18`) y aplicarlo al primer WhatsApp de `portada()` en `tools/site/componentes.py:899`, `componentes_materiales.py:272`, `plantillas/tienda_hub.py:19`, `tienda_guia.py:21`, `nochebuenas.py:63`. "Llamar" baja a enlace de texto de 44 px (como `.vt-inicio__enlaces`), no botón.

**A2. Móvil: cero fotos en la primera pantalla de las plantillas interiores.**
- **[M]** `heroImg.y` a 375×812: pasto en rollo 1023, diseño 934, mantenimiento 802, riego 883, sintético 983, hub 872, palmas 885, material 917, mayoreo 952, zona 797, precios 981, vivero 849, nochebuenas 825. Solo ciudad (630) y blog (590) asoman foto.
- **[O]** Para un negocio que vende jardines, el primer pantallazo es un documento de texto. La etiqueta "colgada" pierde el cordel en móvil (`terra.css`, `@media (max-width:1023px) .vt-etiqueta-x--cordel::before{display:none}`) y queda como tarjeta blanca.
- **Arreglo:** ver (d). Foto a sangre 16:10 justo bajo el titular con la etiqueta compacta montada sobre su borde inferior.

**A3. El CTA y el precio no caben en la primera pantalla en celulares bajos y laptops.**
- **[M]** A 375 px de ancho, fondo del CTA (y+h): pasto en rollo 790, sintético 773, precios 771, mayoreo 742, nochebuenas 735, material 730, b2b-palmas 722, diseño 701, palmas 699, hub 685, riego 673, tienda 669. Con 664 px útiles (iPhone con barras de Safari) quedan fuera 13 de 21. La home sí cabe (653) porque tiene su media query para pantallas bajas (`terra-inicio.css:47-53`).
- **[M]** A 375×667 la barra fija `.vt-bar` aparece desde la carga y tapa la segunda fila de la etiqueta (`pliegue-667.jpg`).
- **[M]** A 1366×768 en pasto en rollo: el h1 mide 3 renglones + lema de 2; la banda amarilla del precio queda bajo el pliegue (`pliegue-1366.jpg`). La home tiene regla para `max-height:820px` (`terra-inicio.css:85-94`); `.vt-portada` genérica no.
- **Causa [M]:** lede de 112–196 px en móvil (4–7 renglones a 18.1 px) y kicker de 2 renglones antes de la etiqueta.
- **Arreglo:** (1) lede del hero a máx. 2 renglones en móvil (`-webkit-line-clamp:2` o editar contenido; el resto baja a la sección 01); (2) kicker en un renglón (`white-space:nowrap; overflow:hidden; text-overflow:ellipsis` o textos más cortos); (3) copiar a `.vt-portada` las dos media queries de pantallas bajas de la home.

**A4. Cursiva sintética en el h1 de materiales.**
- **[M]** `tools/site/contenido/tierra_negra.py:152` y `tezontle_rojo.py:145`: `"h1": "… <em>por costal, m³ o camión</em>"`. No hay Archivo itálica (`terra.css:9-10` solo carga Archivo normal y Fraunces itálica): el navegador inclina la 800. Medido: `Archivo 800i`, 23 caracteres. La regla del lema es `.vt-portada h1 .vt-serif` (`terra.css:243`).
- **Arreglo:** cambiar `<em>` por `<span class="vt-serif">` en ambos contenidos (y revisar mármol y piedra bola). Blindaje: `.vt-pagina main h1 em{font:inherit;font-style:normal}`.

**A5. Longitud y monotonía en móvil.**
- **[M]** Pantallas de 812 px: catálogo 43.8 · blog 28.5 · mantenimiento 26.6 · pasto en rollo 26.1 · tienda 24.1 · diseño 23.7 · hub 23.0 · riego 22.9 · sintético 22.7 · mayoreo 22.2 · home 21.6. Secciones de más de 3 pantallas: blog "Nuevos artículos" 18.4, hub "con su ficha" 7.3, palmas 5.7, tienda "precio por estado" 4.6, pasto en rollo "Lo que entregamos" 3.8 y "¿Cuál te conviene?" 3.3.
- **[M]** Todas las `.vt-bloque` tienen `padding-block:56px` en móvil y alternan solo hueso `#FAF7EF` y hueso-2 `#F1ECDF` (diferencia de luminancia mínima). El único fondo oscuro es `.vt-cierre` al final.
- **[M]** En pasto en rollo hay WhatsApp en el flujo solo en 4 de 12 secciones (hero, precio, pago, cierre): entre la sección de precio y la de pago hay ~6.5 pantallas sin botón en el contenido (la barra fija sí acompaña).
- **Arreglo:** ver top 12, puntos 5, 6 y 9.

### MEDIO

**M1. Escala de h1 inconsistente entre plantillas.** **[M]**
| Plantilla | h1 móvil | h1 escritorio | line-height |
|---|---|---|---|
| home | 44.9 | 92 | 0.93 |
| servicio, hub, material, zona, b2b, precios, tienda, ficha, ciudad, vivero, nochebuenas | 40 | 83.7 | 0.95 |
| blog | 36 | 71.4 | 1.0 |
| cuestionario | 36 | 64 | 1.02 |
| artículo | 32.05 | 64 | 1.02 |
| catálogo | 32.15 | 56 | 1.02 |
Además: blog y catálogo usan Title Case ("Blog de Jardinería", "Catálogo de Plantas, Palmas y Árboles"), el resto oración. Blog y home cierran con punto; los demás no. **Arreglo:** dos tamaños nada más (`--vt-text-h1` para páginas de venta; `--vt-text-h1-lectura` ≈ 2.25rem/4rem para artículo, catálogo, cuestionario) y regla editorial única de mayúsculas y punto final.

**M2. h3 de nochebuenas fuera de escala.** **[M]** h3 = 28.3 px móvil / 44 px escritorio contra 20/26 en todas las demás (`--vt-text-h3`). Tablas: `th` 12 px mayúsculas y `td` 13 px, contra 15–17 px en el resto; 5 textos a 10 px (`<small>` "Menudeo", "Mayoreo"…). **Arreglo:** usar los tokens en `terra-nochebuenas.css`.

**M3. El lema serif no es universal y a veces no es lema.** **[M]** Con lema: servicios, tienda, ciudad, b2b, zona, vivero, precios. Sin lema: hub, palmas, catálogo, blog, artículo, nochebuenas. Material lo tiene mal (A4). Cuestionario lo pinta en tinta, no verde. En precios el lema es "2026". **[O]** El par Archivo condensada + Fraunces itálica verde es la firma; debe estar en todos o en ninguno.

**M4. El amarillo no está reservado al precio.** **[M]** Usos de `#F2D24B` medidos: banda de la etiqueta y `.vt-precio-marca` (precio, correcto); borde superior de la barra fija (`.vt-bar`, 3 px); rótulos del pie (`.vt-foot__h`, 660 caracteres); rótulo "El mensaje que se abre" en el cierre (748 caracteres en 17 páginas); botón "Ver" del banner de nochebuenas; anillo de foco del pie; sombra del CTA de la home. `terra.css:28` declara "amarillo = precio". **[O]** La sombra del CTA es una excepción defendible (une precio y acción). Los rótulos del pie y del cierre diluyen la regla: pasarlos a `--vt-on-dark-2` o hueso.

**M5. El café "medida" se usa para el kicker.** **[M]** `--vt-soil #6B4226` está definido como "café = medida" pero pinta `.vt-kicker` en las 21 plantillas, "Nota de campo" y las insignias "Tú". **[O]** Funciona visualmente; conviene corregir el comentario del token o reservarlo de verdad.

**M6. Tres lenguajes de precio.** **[M]** (1) etiqueta con banda amarilla (`.vt-etiqueta__precio`, 34–38 px); (2) resaltador (`.vt-precio-marca`) en listas e índice; (3) en la tienda, bloque "Desde $139 /m²" con resaltador gigante dentro del hero, sin etiqueta; (4) en ciudad, precio en negritas dentro del párrafo; (5) tablas de precio de la home y servicios con el precio a la derecha sin resalte salvo la primera fila. **Arreglo:** hero = siempre etiqueta; listas = siempre resaltador; tablas = resaltador en todas las filas o en ninguna.

**M7. Botones: 4 alturas y un sistema paralelo en la tienda.** **[M]** `.vt-btn` a 44 (menú), 48 (por defecto), 52 (`.vt-cta`), 56 (`.vt-nb-enviar`), 62/66 (home). En `/pasto-sintetico` conviven `.btn.btn--primary` y `.btn--ghost` (44 px, 15 px, borde verde) y `.spec-card__add` con el sistema `.vt-btn`. El cuestionario del quiz usa `a.quiz__name` de 22 px de alto. **Arreglo:** tres tamaños nombrados (compacto 44, normal 52, principal 60–66) y retirar `.btn*` de `terra-tienda.css`.

**M8. El cierre no siempre cierra.** **[M]** En material, después de `.vt-cierre` (oscuro) siguen "Otros materiales" y el formulario "Escríbenos para cotizar" (1,373 px más). En artículo, el cierre es `.vt-art__producto` en hueso-2, no la banda verde. En catálogo y blog no hay `.vt-cierre`. **[O]** La banda verde con "El mensaje que se abre" es de lo mejor del sitio; debe ser siempre lo último antes del pie.

**M9. Artículo sin imagen y con barra encima.** **[M]** `/blog/pasto-san-agustin-vs-japones`: 0 imágenes en `header.vt-art__cabeza` y en `.vt-art` (5,816 px de texto, listas y una tabla); primer WhatsApp en y=6480; la `.vt-bar` es visible desde la carga y tapa los últimos renglones de "Respuesta directa" a 812 px. La tabla comparativa se corta a la derecha en móvil (tercera columna fuera; es un contenedor con scroll enfocable `div.vt-art__tabla`). **Arreglo:** foto de portada 16:9 bajo el titular (ya existe por artículo en el índice del blog), una figura "FIG." a media lectura, y sombra/degradado en el borde derecho de la tabla para avisar que se desliza.

**M10. Escritorio: el hero interior desperdicia la foto.** **[M]** Columna de foto 5fr, 4:5, 345×627 px en un lienzo de 1440; la etiqueta va en la columna de texto, bajo el lede, con cordel de 60 px que cuelga del párrafo. En la home la foto mide 340×619 pero la etiqueta se monta sobre ella. En material la foto es apaisada (345×334) y deja ~290 px vacíos bajo el pie de figura. **[O]** El gesto "etiqueta colgada sobre la foto" es lo que hace memorable a la home; en los interiores la etiqueta flota sobre fondo hueso y pierde el efecto objeto.

**M11. Tableta (768): media pantalla vacía.** **[M]** A 768×1024 en pasto en rollo la etiqueta ocupa 340 px y deja ~360 px vacíos a su derecha; los botones van debajo y la foto empieza en y=821. La home ya resuelve 768–1023 con rejilla etiqueta + botón lado a lado (`terra-inicio.css:40-44`). **Arreglo:** misma rejilla para `.vt-portada__trato` desde 768 px.

**M12. Sin movimiento fuera de la home.** **[M]** `movimiento.json`: animaciones solo en `home` (`vt-inicio-balanceo`, `vt-inicio-foto`, `vt-inicio-titulo`, `vt-inicio-sube`). En las demás, `animation: none` en todo el documento. Detalle en la sección de movimiento.

### BAJO

- **B1. [M] Texto menor a 12 px:** nochebuenas 10 px (5 `<small>`), precios 11 px (7 `th` y 3 unidades `.vt-u`), tienda y ficha 11.25 px ("mm" en la insignia de altura, 13 apariciones), home y pasto en rollo 11.67 px ("desde $2,000" en las opciones de mensualidades, 5). Subir a 12 px mínimo (`--vt-text-xs` = 13 px ya existe).
- **B2. [M] Objetivos táctiles:** enlaces del pie 41 px de alto (30 por página), redes sociales 49×38 px, correo 176×41. Logo del encabezado 112×31 (enlace). Botón "Ver" del aviso de lista 40 px. El resto cumple (radios de 13 px van dentro de etiquetas grandes). Subir `.vt-foot a` a `min-height:44px`.
- **B3. [M] Cuerpo dominante a 15 px:** por número de caracteres en móvil, 15 px (98 k) supera a 17 px (52 k) y 13 px suma 39 k. El "cuerpo" real de tarjetas, tablas y listas es `--vt-text-sm`. **[O]** Legible, pero en tarjetas de texto largo (usos de tierra negra, pasos del proceso) conviene 16–17 px.
- **B4. [M] Largo de línea:** móvil 32–43 caracteres por línea (bien); escritorio 63–86 en párrafos de sección (catálogo 86, servicios 79). `.vt-lede` limita a 58ch; los `p` de sección no. Poner `max-width:68ch`.
- **B5. [M] Catálogo:** 315 controles interactivos en móvil, 117 `summary` "Ficha de …" apilados; CLS 0.024 en escritorio (único distinto de 0). 38 pantallas de rejilla sin paginación.
- **B6. [M] `Arial 700`** aparece en 12 caracteres (un control nativo sin `font-family:inherit`).
- **B7. [M] Insignias de la tienda:** subnavegación + "Mi lista" añaden 49 px fijos sobre las migas; en móvil el botón "Mi lista" ocupa una franja completa para un solo control.
- **B8. [O] Iconografía:** un solo estilo (trazo 1.7–2 px, extremos redondos, `currentColor`) más el glifo de WhatsApp relleno en círculo blanco. Consistente. Única rareza: en nochebuenas el glifo de WhatsApp va sin círculo, en verde sobre botón de línea.
- **B9. [M] Banner de temporada:** solo en la home (`.vt-navidad-x`, 67 px); texto blanco sobre degradado rojo, no medible por ser imagen de fondo. **[O]** Se lee bien; ocupa 8% del primer pantallazo móvil.

### Lo que está bien (no tocar)

- **[M]** Contraste: pares más débiles `#5C6152` sobre `#E3EADB` 5.19:1, sobre `#F1ECDF` 5.42:1, sobre `#FAF7EF` 5.97:1; kicker café 8.06:1; blanco sobre verde campo 9.76:1; tinta sobre amarillo 11.83:1. Nada falla AA.
- **[M]** Formas: `border-radius` 2 px en 644 elementos, 50% en 90 (ojales, viñetas), 6 px en 24 (etiquetas). Bordes: 1 px `#DDD6C6` (747), 1 px tinta (304), punteado `#B8AE98` (35). Sombras: una de tarjeta, una de etiqueta.
- **[M]** Foco: `outline:2px solid #1E4D2B; offset 2px` en enlaces, botones, `summary`, controles (los campos lo pintan en el contenedor `.vt-control`). Pie con anillo amarillo.
- **[M]** Pesos: Archivo 400/500/600/700/800 y Fraunces 400 itálica; dos familias. Kicker, migas y pie de figura idénticos en todas las plantillas (13 px; kicker 600 mayúsculas +0.1em; `FIG. 0X` 700).
- **[M]** Elementos fijos: encabezado 56 px (móvil) / 68 px; barra inferior 56 px que se oculta mientras el CTA del hero está a la vista y con el menú abierto. El pie reserva su altura (`padding-bottom` con `--vt-bar-h`).

---

## Sistema visual medido (referencia)

**Escala tipográfica [M]**

| Rol | 375 | 768 | 1440 | Interlineado | Fuente |
|---|---|---|---|---|---|
| h1 venta | 40 (home 44.9) | 55.5 (home 68.5) | 83.7 (home 92) | 0.95 (0.93) | Archivo 800, wdth 75, −0.018em |
| lema | 24 (0.6em) | 33 | 50.2 | 1.15 | Fraunces 400 itálica, verde |
| h2 | 32 | 41.6 | 56 | 1.02 | Archivo 800, wdth 75 |
| h3 | 20 | 22.2 | 26 | 1.02 | Archivo 800, wdth 75 |
| lede | 18.1 | 19.5 | 21 | 1.55 | Archivo 400, `#2F352B`, máx. 58ch |
| cuerpo | 17 | 17 | 17 | 1.55 (artículo 1.65) | Archivo 400 |
| secundario | 15 | 15 | 15 | 1.3–1.55 | Archivo 400/600 |
| pequeño | 13 | 13 | 13 | 1.2–1.45 | Archivo 500/600 |
| precio etiqueta | 34 | 34 | 38 | 1 | Archivo 800, wdth 80, tabular |

Salto h2→h3 en móvil: 32→20 (1.6×); h1→h2: 40→32 (1.25×). **[O]** En móvil el h1 y el h2 quedan demasiado cerca: el titular del hero no "manda" sobre los de sección. La home lo mejora con 44.9.

**Color [M]:** fondos por área: hueso-2 `#F1ECDF`, blanco `#FFFFFF`, tinta `#161A14` (pie), verde profundo `#12301B` (cierre), verde campo `#1E4D2B` (botones), amarillo `#F2D24B`, verde-100 `#E3EADB`. Tintas por volumen: `#2F352B`, `#161A14`, `#5C6152`, y sobre oscuro `#C9D6C4` y `#FAF7EF`. Verde = CTA, enlaces, lema, viñetas, estado "en existencia".

**Espaciado [M]:** `--vt-space-section` = 56 px (375) a 120 px (1440), idéntico arriba y abajo en todas las secciones; hero 22 px arriba / 0 abajo; cabecera de bloque a contenido 32–52 px.

---

## Estructura por plantilla (móvil, pantallas de 812 px) [M]

- **Home (21.6):** banner → hero 1.7 → 5 servicios 2.0 → medidor 2.1 → fotos 2.9 → opiniones 2.0 → proceso 1.5 → precios 2.9 → preguntas 2.1 → cobertura 1.0 → cierre 1.0.
- **Servicio (22.7–26.6):** hero 2.0 → prueba/fotos 3.8 → más fotos 1.8 → precio + calculadora 3.0 → comparativa 3.3 → proceso 1.5 → garantía 0.9 → pago 1.8 → preguntas 1.4 → cobertura 1.6 → relacionados 1.7 → cierre 1.0. **[O]** Dos secciones de fotos seguidas (5.6 pantallas) antes del precio; el precio, que es la promesa de la marca, llega en la pantalla 8.
- **Tienda (24.1):** hero 1.7 → modelos 2.9 → quiz 1.6 → comparador 0.8 → precio por estado 4.6 → ciudades 2.0 → tabla 1.4 → fotos 2.4 → cómo comprar 1.0 → instalar 1.3 → preguntas 1.4 → cierre.
- **Ficha (17.9):** ficha 3.8 (etiqueta, datos, galería, cotizador) → resumen 1.2 → ficha técnica 2.7 → instalado 1.2 → comparar 2.2 → pedido 1.8 → garantía 0.7 → preguntas 1.2 → cierre.
- **Hub plantas (23.0):** hero 1.8 → por necesidad 1.3 → subcategorías 1.4 → especies 7.3 → recorrido 1.7 → arma tu lista 0.6 → garantía 0.9 → preguntas 1.4 → guías 0.5 → complementa 3.0 → cierre. **[O]** "Complementa tu proyecto" (6 tarjetas grandes, 3 pantallas) pesa más que "Arma tu lista", que es la acción propia del hub.
- **Material (18.5):** hero 1.8 → qué es 2.0 → precio 1.5 → usos 2.2 → calculadora 1.1 → entrega 1.4 → fotos 1.3 → opiniones 1.1 → preguntas 1.4 → cierre 0.8 → otros 0.7 → formulario 1.0.
- **B2B (22):** hero 1.8 → clientes 2.9 → precio 2.6 → correo 1.7 → documentación 1.3 → paquetes 1.9 → proceso 1.3 → garantía 0.9 → preguntas 1.3 → cobertura 1.5 → otras 1.7 → cierre.
- **Zona (9.5), vivero (8.7), ciudad (10.7):** las mejor proporcionadas; 6–7 secciones de ~1 pantalla.
- **Precios (17.1):** hero 1.9 → saltos → 6 tablas (1.0–2.3) → garantías → preguntas → cierre. **[O]** En la página de precios el hero gasta 1.9 pantallas antes de la primera tabla; aquí el hero debería ser los saltos + la tabla.
- **Blog (28.5):** portada 0.9 → para empezar 1.7 → nuevos 18.4 (35 tarjetas con foto) → todos 4.0 → servicio 1.2. **Catálogo (43.8):** cabecera 0.8 → rejilla 38.4.
- **Artículo (11.6):** cabecera 0.6 → cuerpo 7.2 → producto 0.8 → relacionados 0.8.

Momentos "wow" ausentes **[O]**: (1) ninguna foto a sangre de borde a borde fuera del hero de la home; (2) ninguna cifra gigante salvo "15–20 días" y "5 años" en garantía, que sí funcionan y podrían ir sobre fondo verde; (3) el antes/después no existe como componente; (4) el dibujo "vista en planta" del medidor es el mejor guiño al "plano de obra" y solo vive en la calculadora.

---

## Movimiento

**Existe [M]** (`terra.css`, `terra-inicio.css`, `movimiento.json`):
- Global: `.vt-btn` (color, fondo, `transform` 150 ms; `:active` baja 1 px), `.vt-flecha` (+3 px en hover), subrayado del menú (`scaleX`), chevrones, `.vt-bar` (entra y sale con `translateY`, 260 ms), `.vt-tarjeta:hover` (−3 px), `.vt-indice__ir` (+4 px), acordeón `summary`.
- Solo home: etiqueta que se balancea al cargar (0.9 s, escritorio), foto que se descubre con `clip-path` (0.7 s), h2 y fotos de obra que suben con `animation-timeline:view()`, CTA que se "hunde" en su sombra (hover 2 px, active 5 px).
- Tienda: pulso de opacidad al recalcular precio. Nochebuenas: estados `:active` en pasos.
- `prefers-reduced-motion` respetado en las hojas que animan.

**Falta frente a la home [M]:** entrada del hero (0 de 20 plantillas), revelado de h2 y figuras (0 de 20), hover en `.vt-fig` (ninguna), hover en filas de tabla de precios (ninguno), estado `:active` propio en `.vt-btn--linea` y chips. En móvil `(hover:hover)` no aplica: el único movimiento que ve el 80% del público es la barra fija.

**Propuestas sobrias [O]** (solo `transform`/`opacity`/`clip-path`, dentro de `@media (prefers-reduced-motion:no-preference)`, sin librerías):

| Propuesta | Dónde | Costo |
|---|---|---|
| Mover a `terra.css` el revelado de h2 y `.vt-fig__marco` (`animation-timeline:view()`, con `@supports`) | todas las `.vt-pagina` | 6 líneas; quitar el prefijo `.vt-inicio`. Bajo |
| Balanceo de la etiqueta al cargar, también en móvil con amplitud menor (2° → 0°, 0.7 s, origen en el ojal) | `.vt-portada .vt-etiqueta-x` | 1 keyframe ya escrito. Bajo. No toca LCP (no anima opacidad) |
| Foto del hero que se descubre con `clip-path` | `.vt-portada__foto .vt-fig__marco` | ya escrito. Bajo |
| CTA principal: hundirse en la sombra en `:active` (ya escrito) y un único "latido" de la sombra amarilla a los 4 s si no hubo scroll (`transform:translate` de la sombra en un `::after`, una sola vez) | `.vt-btn--principal` | 10 líneas. Bajo–medio |
| Fila de precio: al entrar en vista, el resaltador amarillo se pinta de izquierda a derecha (`clip-path:inset(0 100% 0 0)` → `inset(0)` en un `::before`) | `.vt-precio-marca` | 8 líneas; escalonar con `animation-delay` por `:nth-child`. Medio |
| Cifra de garantía ("15–20", "30", "5") sube 12 px con opacidad .6→1 al entrar | la cifra grande de la sección de garantía (clase por confirmar en `componentes.py`) | 3 líneas. Bajo |
| `.vt-fig:hover img{transform:scale(1.03)}` con `overflow:hidden` (ya lo tiene el marco) | figuras | 2 líneas; solo `(hover:hover)`. Bajo |
| Barra fija: al aparecer, el borde amarillo de 3 px crece con `scaleX` de 0 a 1 | `.vt-bar::before` | 5 líneas. Bajo |

No recomiendo: parallax, contadores numéricos animados, carruseles automáticos, ni opacidad sobre titular, lede, precio o botón al cargar (retrasa el LCP; ya lo advierte el comentario de `terra-inicio.css:122`).

---

## Checklist rápido [M]

| Punto | Resultado |
|---|---|
| Objetivos táctiles ≥ 44 px | Cumple en contenido. Fallan: enlaces del pie 41 px (≈30 por página), redes 38 px, logo 31 px de alto, "Ver" de la lista 40 px, `a.quiz__name` 22 px |
| Foco visible | Sí, uniforme: 2 px verde + 2 px de separación; pie en amarillo; campos en el contenedor |
| Scroll horizontal | 0 de 22 páginas a 375, 768 y 1440 (`scrollWidth == innerWidth`) |
| Texto < 12 px | nochebuenas 10 px (5), precios 11 px (10), tienda/ficha 11.25 px (13), home y pasto en rollo 11.67 px (5 c/u) |
| Fijos que tapan contenido | Barra inferior 56 px: correcta en 812 px; a 667 px tapa la etiqueta del hero interior desde la carga; en artículo tapa "Respuesta directa". Barra de compra de la tienda 104–130 px (13–16% del alto) tras el primer scroll |
| CLS | 0.000 en móvil en las 22; escritorio: home 0.002, catálogo 0.024, resto 0.000 (con fuentes propias y terceros bloqueados) |

---

## (d) Propuesta: "hero de marca" unificado

Para servicio, hub, material, zona, b2b, vivero, precios y artículo (con variante). **[O]**, apoyada en las medidas anteriores. Un solo componente `portada()` en `tools/site/componentes.py` con los estilos en `terra.css` (hoy repartidos entre `terra.css` y `terra-inicio.css`).

### Piezas, en orden de lectura

1. **Migas** (13 px, una línea, como hoy).
2. **Kicker** café, 13 px mayúsculas, **un renglón** (máx. ~34 caracteres en 375 px).
3. **Titular** Archivo 800 wdth 75. Móvil `clamp(2.5rem, 1.4rem + 6vw, 5.75rem)` (la fórmula de la home: 44.9 px a 375, 92 px a 1440), `line-height:.93`. Máximo 2 renglones en móvil y 3 en escritorio: los titulares de 3–4 renglones se acortan y la parte SEO pasa al lema.
4. **Lema** Fraunces itálica verde campo, 0.55em del titular (≈24 px móvil / 40 px escritorio), siempre presente, 1 renglón en móvil. Es una promesa, no un dato suelto ("con visitas programadas", no "2026").
5. **Lede** 17–18 px, **máx. 2 renglones en móvil** (≈90 caracteres), 3 en escritorio, `max-width:38ch` en escritorio como la home.
6. **Foto con etiqueta colgada** (el objeto de marca):
   - Móvil: foto **a sangre** (márgenes negativos del gutter), proporción 16:10 (375×234 px), justo bajo el lede. La etiqueta compacta (ojal a la izquierda, código + banda amarilla + 1 fila) se monta sobre el borde inferior de la foto: `margin-top:-56px`, ancho `calc(100% - 32px)`, máx. 340 px, con su sombra `--vt-sombra-tag`. Un cordel de 1.5 px sube 28 px desde el ojal sobre la foto. Pie "FIG. 01 · lugar · etapa" bajo la etiqueta, alineado a la derecha.
   - Escritorio (≥1024): dos columnas `1fr / .74fr`, separación 88 px; foto 4:5 a la derecha; etiqueta completa (272 px, con nombre y nombre científico) colgada sobre la esquina inferior izquierda de la foto, saliendo 76 px hacia el texto. Es la geometría de `terra-inicio.css:58-68`, tal cual.
   - Tableta (768–1023): foto 16:9 a sangre arriba; debajo, rejilla `340px / 1fr` con etiqueta a la izquierda y botón + enlaces a la derecha (`terra-inicio.css:40-44`).
7. **Botón principal** "Cotizar por WhatsApp →": verde campo, glifo en círculo blanco, **60 px de alto en móvil a todo lo ancho, 64–66 px en escritorio con ancho automático**, 19–20 px/600, `box-shadow:5px 5px 0 var(--vt-tag)`; hover se hunde 2 px, active 5 px; foco con `outline-offset:8px`.
8. **Enlaces secundarios** en una fila de texto de 44 px: a la izquierda la acción propia de la página ("Calcula tu patio →", "Arma tu lista →", "Calcula cuánta necesitas →", "Compara los 3 planes →"), a la derecha "Llamar 833 326 8008". Sustituye al botón de línea.
9. **Línea de confianza** con filete superior, 13 px: "Respondemos en menos de 1 hora en horario · **4.6** en Google (24 reseñas) · dato propio de la página" (REPSE 773725 en b2b; "garantía de arraigo 15–20 días" en pasto; "30 días" en plantas). Hoy la calificación de Google solo aparece en la home.
10. **Cuadro de datos** `.vt-datos` (6 celdas) como arranque de la sección siguiente, fuera del primer pantallazo.

### Presupuesto de altura en móvil (375 px de ancho)

| Pieza | Alto |
|---|---|
| Encabezado + migas | 56 + 30 |
| Kicker (1 renglón) | 30 |
| Titular (2 renglones a 44.9 × 0.93) | 84 |
| Lema (1 renglón) | 34 |
| Lede (2 renglones) | 56 + 12 |
| Foto 16:10 | 234 − 56 de traslape |
| Etiqueta compacta (código + banda + 1 fila) | 163 |
| Botón principal | 18 + 60 |
| **Total** | **≈ 651 px** |

Cabe en 664 px (iPhone con barras) con foto, precio y botón visibles; hoy esas tres cosas juntas no caben en ninguna plantilla interior ni a 812. Para pantallas de 640 px o menos: titular a 2.3rem, lede a 1 renglón y foto 2:1 (misma media query que `terra-inicio.css:47-53`).

### Variantes

- **Hub (plantas):** misma estructura; la foto debe enseñar planta (no fachada). Enlace secundario "Arma tu lista →". Bajo la línea de confianza, una fila de 5 fichas de categoría con desplazamiento horizontal (miniatura 64 px + nombre) que hoy está en la sección 02.
- **Material:** foto del camión volteo a sangre (ya existe); etiqueta con "$90 por costal" y fila "m³ a granel $1,500"; enlace "Calcula cuánta necesitas →". En escritorio, foto 4:5 recortada del mismo original en lugar de la apaisada de 334 px.
- **Zona:** kicker con la colonia y CP; etiqueta "San Agustín instalado desde $120"; línea de confianza con "cuadrilla propia en Altamira".
- **Precios:** sin foto grande. Titular + lema + **la etiqueta como índice** (4 filas con ancla a cada tabla) + botón. La primera tabla debe asomar en la primera pantalla.
- **Artículo:** variante de lectura. Titular 2.25rem móvil / 4rem escritorio, sin etiqueta; foto de portada 16:9 a sangre con pie "FIG. 01"; meta en una línea; "Respuesta directa" como tarjeta con filete verde de 3 px; sin botón principal en el hero (la barra fija se muestra hasta pasar la respuesta directa, no desde la carga). La etiqueta de precio aparece una vez, a media lectura, como "producto relacionado" (hoy está al final, en y=6646).
- **Tienda / ficha / ciudad:** conservan su hero funcional (selector de estado, cotizador), pero adoptan el botón principal con sombra y la etiqueta en vez del bloque "Desde $139" resaltado; ciudad gana etiqueta con "$162/m² puesto en Monterrey".

---

## (e) Top 12 de mejoras (por impacto en primera impresión y clics)

| # | Mejora | Impacto | Esfuerzo | Dónde |
|---|---|---|---|---|
| 1 | Botón principal con sombra amarilla (60/64 px) en todos los héroes; "Llamar" pasa a enlace de texto | Clics: muy alto | Bajo (CSS de `terra-inicio.css:14-18` a `terra.css` + clase en 5 plantillas) | A1 |
| 2 | Foto a sangre con la etiqueta colgada encima, visible en la primera pantalla móvil | Primera impresión: muy alto | Medio (reordenar `portada()`; CSS móvil nuevo; sin fotos nuevas) | A2, (d) |
| 3 | Lede a 2 renglones y kicker a 1 en móvil; media queries de pantallas bajas para `.vt-portada` | Clics: alto (CTA y precio dentro del pliegue en 13 plantillas) | Bajo–medio (CSS + recorte de textos en `tools/site/contenido/`) | A3 |
| 4 | Corregir el `<em>` del h1 de materiales a `.vt-serif` | Primera impresión: alto en esas páginas | Mínimo (2 líneas de contenido + 1 regla de blindaje) | A4 |
| 5 | Línea de confianza con "4.6 en Google (24 reseñas)" y dato propio en cada hero | Clics: medio–alto | Bajo (el dato ya existe: `GOOGLE` en `tools/site/datos.py:70`) | (d) 9 |
| 6 | Un momento oscuro a media página: garantía ("15–20 días", "30 días", "5 años") sobre verde profundo, cifra a 96–120 px, a sangre | Primera impresión y ritmo: alto | Bajo (modificador `.vt-bloque--campo` reutilizando colores de `.vt-cierre`) | A5 |
| 7 | Etiqueta colgada sobre la foto en escritorio para todas las portadas (geometría de la home) | Primera impresión escritorio: alto | Medio (CSS; probar 1024–1279 y pantallas bajas) | M10 |
| 8 | Lema serif en todas las plantillas de venta (hub, palmas, nochebuenas, blog) y regla editorial única de titulares (oración, sin Title Case) | Consistencia de marca: medio | Bajo (contenido) | M1, M3 |
| 9 | Acortar móvil: comparativas y especies en acordeón o carrusel con `scroll-snap`, una sola sección de fotos por servicio, precio antes que galería; WhatsApp en línea al final de cada 2–3 secciones | Clics a media página: medio–alto | Medio–alto (plantillas `servicio.py`, `hub_categoria.py`, `blog_indice.py`) | A5 |
| 10 | Llevar el movimiento de la home a todas las plantillas (revelado de h2 y figuras, balanceo de etiqueta, foto que se descubre) | Percepción de calidad: medio | Bajo (quitar el prefijo `.vt-inicio` a 4 reglas y moverlas a `terra.css`) | M12 |
| 11 | Artículo: foto de portada, figura intermedia, etiqueta de producto a media lectura, barra fija que espera a pasar la respuesta directa | Clics desde blog: medio | Medio (`componentes_blog.py`, `terra-blog.css`, `terra.js`) | M9 |
| 12 | Limpieza del sistema: 3 alturas de botón, retirar `.btn*` de la tienda, h3 y tablas de nochebuenas a tokens, textos < 12 px a 13 px, enlaces del pie a 44 px, amarillo fuera de rótulos del pie y del cierre, cierre verde siempre al final | Consistencia y accesibilidad: medio–bajo | Medio (varias hojas, cambios chicos) | M2, M4, M6, M7, M8, B1, B2 |

Orden sugerido de entrega **[O]**: 4 → 1 → 3 → 5 (una tarde, solo CSS y contenido) · luego 2 + 7 (el hero de marca completo) · luego 6, 8, 10 · al final 9, 11, 12.

---

## Límites de esta auditoría

- Un solo motor (Chromium). No se probó Safari ni Firefox; `animation-timeline:view()` no existe en Firefox estable y el CSS ya lo protege con `@supports`.
- CLS y tiempos medidos con terceros bloqueados y sin limitar red: son un piso, no el valor de campo.
- No se hizo clic en `wa.me`/`tel` ni se envió ningún formulario; los estados hover/active se leyeron del CSS, no se capturaron uno por uno.
- El contraste sobre imágenes (banner de nochebuenas, cierre con foto de material) no se calculó.
- En las hojas de página completa algunas imágenes diferidas salen en blanco por la velocidad de la captura; se verificó aparte que el hub de plantas no tiene imágenes rotas (0 de 39).
