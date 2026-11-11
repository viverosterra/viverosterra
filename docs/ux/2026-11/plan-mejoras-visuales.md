# Plan de mejoras visuales · viverosterra.com

Fecha: 2026-11-11. Revisión de 14 páginas completas, en celular (375 px) y en computadora (1440 px): inicio, pasto en rollo,
tienda y ficha de sintético, plantas, mantenimiento, diseño, precios, blog, un artículo, Nochebuenas, tierra negra y
Altamira. Complementa `auditoria-diseno-visual.md` (2026-11-10), que se centró en el hero; ese trabajo ya se publicó en las
entregas A, B y C.

## Público y dirección

- **Quién compra:** familias de Tampico, Madero y Altamira con patio o frente. También empresas, fraccionadoras y
  gobierno que compran por volumen. La mayoría entra desde el celular y decide por WhatsApp.
- **Qué debe sentir:** que es un vivero de verdad, con cuadrilla propia y precios claros. Debe verse cuidado, no como una
  plantilla.
- **Dirección (se mantiene y se lleva más lejos): «cuaderno de campo del vivero».** El sitio ya tiene las piezas: la etiqueta
  de precio colgada, los pies de foto «FIG. 01», la «Nota de campo», la regla de altura, la serif verde en cursiva y la
  condensada negra. El plan no cambia de estilo. Usa esas piezas en todas las páginas y les suma gráficos propios.
- **Regla de color (se conserva):** verde para el campo y la acción, amarillo solo para el precio, café para la tierra y
  las medidas, hueso de fondo.

## Lo que está bien (no se toca)

- La combinación de letras (Archivo condensada + Fraunces cursiva).
- La etiqueta de precio y el hero unificado.
- Los testimonios en serif.
- La banda verde del cierre con «El mensaje que se abre».
- El contraste (todo pasa AA) y los focos visibles.
- Cero desbordes y cero brincos de diseño.

## Hallazgos, de mayor a menor impacto

### 1. Defectos visibles (arreglo rápido)

1. **Tienda de sintético, tarjetas de modelo:** en celular el botón «Agregar a mi lista» tapa el «/m²» del precio. Pasa en
   las 9 tarjetas.
2. **Tablas comparativas cortadas:** en la tienda y en los artículos la tabla se sale a la derecha y no avisa que se
   desliza. Se ve el inicio de la columna siguiente cortado («GA», «J»).
3. **Texto repetido que ensucia:**
   - «Respondemos en menos de 1 hora en horario…» sale debajo de cada botón: 8 veces en Plantas y 6 en la tienda.
   - Las condiciones de la garantía de arraigo se repiten completas 4 o 5 veces en Inicio y en Pasto en rollo.
   - Son párrafos grises de 13 px que alargan la página sin dar nada nuevo.
4. **Tarjeta de modelo:** «Toscana 18 para llevar hoy · Obregón 209 Sur» repite el nombre que está justo arriba.

### 2. Secuencia y ritmo

5. **Todo es hueso hasta el pie.**
   - La única franja oscura es el cierre.
   - En celular son 17 a 26 pantallas del mismo fondo, con el mismo esqueleto: número, rótulo, título, párrafo y tarjetas blancas.
   - **Propuesta:** a media página, un «momento» por página. Puede ser una banda verde oscuro con la garantía y una cifra
     grande, o una franja de fotos a todo lo ancho.
6. **Dos bloques de texto seguidos debajo del hero, en todas las páginas.**
   - Son «En corto» (un párrafo gris largo) y la tabla de datos de la empresa.
   - En computadora «En corto» ocupa media pantalla y deja la otra mitad vacía.
   - **Propuesta:**
     - Volver «En corto» una tarjeta tipo «Nota de campo», con borde y rótulo.
     - Convertir la tabla de datos en una tira delgada de 1 renglón con 4 datos.
     - Que la primera sección con fotos suba.
7. **Páginas largas en celular:**
   - La tienda tiene las listas de estados por zona como párrafos largos.
   - En Plantas, la ficha de cada especie repite Luz, Riego y Altura en texto.
   - **Propuesta:**
     - Estados en acordeón, abiertos solo para la zona elegida.
     - Fichas más compactas (punto 8).
8. **En computadora el contenido no aprovecha el ancho:** el texto va en la mitad izquierda y la foto del hero mide
   ~30 % del ancho. **Propuesta:** rejilla editorial asimétrica. El título de la sección va a la izquierda y se queda fijo
   al bajar, y el contenido va a la derecha. Una foto grande por página.

### 3. Gráficos propios (lo que hace que se vea «diseñado»)

9. **Íconos de cultivo en lugar de texto:**
   - Luz, riego y altura en Plantas y en el catálogo: sol, gota y regla, como chips con el valor.
   - Mismo trazo que los íconos actuales. SVG en línea, sin imágenes nuevas.
10. **Pasto sintético, para distinguir los 9 modelos:**
    - Hoy las 9 miniaturas son cuadros verdes casi iguales.
    - **Propuesta:** una gráfica de «altura de fibra» con los 9 modelos uno junto al otro (10 a 35 mm) y su peso. Es la regla
      que ya existe, en grande y como parte del diseño.
    - En cada tarjeta, la altura en grande y un punto de color del tono.
11. **Cifras con carácter:** «30 días», «+500,000 m²», «desde 2007», «15 a 20 días», en Fraunces grande, como en un
    cuaderno. Hoy los números van en la misma letra que el texto, salvo los precios.
12. **Atmósfera:**
    - Un grano de papel muy suave en el fondo hueso.
    - Dibujos de línea botánicos como separadores: hoja de San Agustín, fronda de palma y raíz. Son SVG propios y ligeros.
    - Nada generado con IA como foto.
13. **Color semántico por línea de negocio:**
    - Fondo café claro (`--vt-soil-100`, ya existe) en las secciones de tierra y materiales.
    - Verde claro en pasto y plantas.
    - Así se sabe en qué parte del sitio estás sin leer.

### 4. Fotos (necesita tu visto bueno; no se cambia ninguna foto sin permiso)

14. **Artículos del blog sin ninguna imagen:** 54 páginas de puro texto. El índice del blog ya tiene una foto por
    artículo. **Propuesta:** usar esa misma foto como portada del artículo. Es una foto que ya publicaste, no una nueva.
15. **Estilos de foto mezclados en Plantas y en el catálogo:**
    - Hay de tres tipos: plantas recortadas sobre blanco, escenas de playa y alberca, y fotos reales del vivero.
    - **Propuesta:** el mismo marco para todas (fondo hueso, misma proporción, pie «FIG.»), sin editar los archivos.
    - Las de playa y alberca (Palma Kerpis, Coco plumoso, Palma Areca) parecen de banco de imágenes: ¿son tuyas?
16. **Foto más grande en computadora** (punto 8). Es solo tamaño y recorte, la foto no cambia.

## Plan por etapas

Cada etapa va en una rama aparte. Antes de pedirte el visto bueno para publicar, en cada una:

- Reviso a 320, 375, 768, 1024 y 1440 px.
- Corro Lighthouse sin que baje.
- Mantengo terra.css dentro del tope (60 KB / 12 KB comprimido).
- Agrego una prueba automática por regla nueva.

| Etapa | Qué incluye | Puntos | Tamaño |
|---|---|---|---|
| **V1 · Defectos y limpieza** | Botón que tapa el precio, tablas con aviso de deslizar, texto repetido una sola vez por página (la garantía completa una vez y luego «ver condiciones»), nombre repetido en la tarjeta. | 1–4 | 1 día |
| **V2 · Ritmo y secuencia** | «En corto» como Nota de campo, tira de datos delgada, un momento oscuro o de fotos a media página, acordeón de estados, rejilla editorial en computadora. | 5–8 | 2–3 días |
| **V3 · Gráficos propios** | Íconos de luz, riego y altura, gráfica de altura de los 9 sintéticos, cifras en Fraunces, grano de papel, dibujos botánicos de línea, color por línea de negocio. | 9–13 | 3–4 días |
| **V4 · Fotos** (con tu permiso) | Portada en los 54 artículos con la foto que ya tienen en el blog, marco único para las fotos de plantas, foto más grande en computadora. Se junta con la entrega D (las 15 fotos nuevas). | 14–16 | 1–2 días |

Orden recomendado: V1 → V2 → V3 → V4. V1 se nota de inmediato y no cambia el estilo.

## Respuestas del dueño (2026-11-11)

1. Sí: cada artículo lleva la foto que ya tiene en el índice del blog.
2. Las fotos de playa y alberca de Plantas son suyas (no son de banco).
3. Sí a los dibujos de línea botánicos en SVG.

## Preguntas que se hicieron

1. ¿Puedo poner en cada artículo la foto que ya tiene en el índice del blog?
2. Las fotos de playa y alberca en Plantas (Palma Kerpis, Coco plumoso, Palma Areca): ¿son tuyas o de banco de imágenes?
3. ¿Te parecen bien los dibujos de línea botánicos (hoja, palma, raíz)? Los hago yo en SVG, no son fotos.

## Estado de V2 (2026-11-11, rama feat/visual-v2, sin publicar)

- **«En corto»** es ahora una tarjeta tipo Nota de campo, con el rótulo en serif a la izquierda en computadora.
- **Tira de datos:** pasa de 6 cuadros a 4 datos (desde 2007, +500,000 m², showroom y factura con el REPSE). En
  celular baja de unos 270 a unos 120 px.
- **Momento oscuro a media página** en 26 páginas, siempre con contenido real:
  - opiniones en Inicio, tierra negra y piedra bola;
  - la garantía de plantas (datos.py) en las 6 páginas de plantas;
  - la garantía de fábrica en las 9 fichas de sintético;
  - el proceso en Mantenimiento, Riego, Mayoreo y Palmas para proyectos (su garantía no está en datos.py);
  - «Tu pedido» en la tienda.
  - Quedan sin momento las colonias, mármol, tezontle, vivero, precios y la guía de perros, porque no tienen una
    sección que funcione en oscuro. Se cubren en V4 con fotos.
- **Tienda:** el envío por zona pasa a acordeón; al elegir un estado se abre su zona.
- **Computadora:** el título de las secciones a dos columnas se queda fijo al bajar, desde 1200 px.
- **Revisión:**
  - Sin desbordes a 320, 768, 1024 y 1440 px.
  - Contraste AA en las bandas.
  - Lighthouse sin cambios: Inicio 99, Mantenimiento 93, tienda 89; accesibilidad y SEO en 100.
  - terra.css: 12 KB comprimido (sin cambio de tope); el tope del archivo sin comprimir sube de 60 a 62 KB.
- **Prueba:** tests/test_visual_v2.py.
