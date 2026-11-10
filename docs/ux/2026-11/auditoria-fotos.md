# Auditoría de imágenes y contenido visual · viverosterra.com

Fecha: 2026-11-10 · Modo: solo lectura (no se editó, borró ni reemplazó nada; sin commits).
Fuentes: repo `~/dev/viverosterra` (rama `main`), `public/` (112 HTML, 671 archivos en `public/img/`), sitio en vivo (solo GET, 12 páginas a 375 px y 1440 px con Playwright, todo lo ajeno a viverosterra.com bloqueado, sin clics).
Método: inventario por script, 24 hojas de contacto revisadas a ojo (todas las imágenes en uso y una muestra de las que no), recortes de detalle y capturas reales.

Grados de certeza usados en este informe: **alta** (hay evidencia visible en la propia imagen), **media** (varios indicios coinciden pero no hay prueba), **baja** (solo una impresión).

---

## (a) Resumen ejecutivo

1. **En celular, la primera pantalla de todas las páginas medidas no tiene ninguna foto.** En las 11 páginas revisadas a 375 × 812 la imagen principal empieza entre los 800 y 1,030 px de altura (en tezontle, a 1,908 px): el visitante ve titular, texto y tarjeta de precio, y la foto queda debajo del pliegue. Para un negocio que vende jardines, es la mayor oportunidad perdida de "impresionar al primer vistazo".
2. **El sitio tiene dos mundos visuales que no se parecen.** Las portadas y `obra/` (17 imágenes) son limpias, de luz de atardecer y con uniforme impecable; `obra/terra/` (63 fotos) son fotos de celular reales con un revelado fuerte (mucha claridad y contraste local). Lado a lado en la misma página se nota el salto.
3. **La mayoría de las imágenes principales parecen render o generadas por IA, y varias llevan pie de foto de obra.** Base: 48 archivos tienen exactamente 1024 × 1536 o 1536 × 1024 px (tamaños nativos de generadores de imagen), logotipos de uniforme perfectos y repetidos, luz de cine, un camión con rótulo ilegible y un costal con el texto "TIERRA VIVEROA NEGRA VEGETAL". El propio repo ya los llama "renders" (commit `fa1db13`, spec de fotos reales). Certeza por imagen en las tablas. El riesgo no es estético sino de confianza: el inicio dice "Fig. 01 · Zona Tampico–Madero · tendido de tepes" bajo una imagen que probablemente no es una obra.
4. **Ya existen fotos reales buenas que podrían encabezar páginas** (alberca frente a la laguna, terraza con pasto sintético, recorte de seto con chaleco Terra, faro de Tampico, invernadero de nochebuenas). Hoy están al fondo, en mosaicos.
5. **El catálogo de plantas (117 fotos) es el punto más débil.** 81 son recortes sobre fondo blanco de otras tiendas, 36 son fotos de exterior; conviven marcas de agua de Shutterstock y Dreamstime, logos de otros viveros, una captura de Google Imágenes y fotos de 146 px de ancho. Las 24 ya registradas en `FOTOS_POR_REVISAR` se confirman a simple vista; encontré algunas más.
6. **Páginas con foto que no corresponde:** `/vivero-tampico` no tiene una sola foto del vivero (1 imagen en toda la página, y es una siembra en casa de cliente); `/plantas-de-interior-tampico` abre con una adelfa de exterior; `/piedra-bola-rio-tampico` abre con un jardín sin piedra; el og de riego se llama "técnico" y no hay técnico; en el blog, 32 de 54 artículos no tienen ninguna imagen en el cuerpo y 10 páginas comparten la misma adelfa rosa.
7. **Técnico:** ancho y alto declarados en el 100 % de las imágenes (bien), WebP casi en todo (bien). Pendiente: 76 % sin `srcset`, 106 imágenes en uso pesan más de 200 KB, 73 de 101 `og:image` son verticales (se recortan mal en WhatsApp y Facebook), 6 páginas indexables sin `og:image`, una foto principal de 194 px, y 152 archivos sin uso (31 MB, incluidas capturas de pantalla del propio sitio) publicados en `/img/`.

---

## 1. Inventario

| Carpeta | Archivos | En uso | Sin uso | Peso total |
|---|---|---|---|---|
| `/img` (raíz) | 196 | 70 | 126 (30.0 MB) | 43.4 MB |
| `/img/obra/terra` | 126 (63 fotos × 2 tamaños) | 125 | 1 | 25.2 MB |
| `/img/pasto-sintetico/galeria` | 132 | 132 | 0 | 12.0 MB |
| `/img/catalogo` | 117 | 117 | 0 | 3.3 MB |
| `/img/portadas` | 29 | 29 | 0 | 2.6 MB |
| `/img/obra` | 18 | 17 | 1 | 1.9 MB |
| `/img/pasto-sintetico` (muestras JPG) | 9 | 9 | 0 | 1.9 MB |
| `/img/nochebuenas` | 12 | 12 | 0 | 1.2 MB |
| `/img/clientes` | 30 | 6 | 24 | 1.0 MB |
| `/img/precios` | 2 | 2 | 0 | 0.2 MB |
| **Total** | **671** | **519** | **152 (31.2 MB, 34 %)** | **92.7 MB** |

Imágenes distintas referenciadas por plantilla (un archivo puede contar en varias): plantas 194, tienda de sintético 155, obras/servicios 98, blog 45, base (zonas y mayoreo) 36, materiales 29, inicio 22, nochebuenas 22, utilitarias 11, precios 6. En total hay 627 etiquetas `<img>` (sin contar el logo SVG). Ningún fondo CSS ni JS arma rutas de imagen: todo está en el HTML.

**Peso muerto (152 archivos, lista completa en `sin-uso.csv`):**
- 51 JPG y 31 PNG que son los originales de WebP ya publicados.
- 28 grupos de duplicados exactos byte a byte. Varios con nombre engañoso: `riego-real-02` a `-05` son fotos de mármol; `riego-real-12/13/14` = `riego-tampico-03/04/05`.
- **Capturas de pantalla del propio sitio y del navegador** servidas públicamente: `riego-real-06.webp` (maqueta de una portada antigua), `riego-real-07/08/09.png`, `riego-tampico-06/07.png`. Conviene retirarlas cuando el dueño lo apruebe.
- 24 variantes de logos de clientes (`-color`, `-gray`) que ninguna página usa.
- `especie-bambu-tarro-tampico.webp` trae incrustados "@viverosterramx" y un número de WhatsApp sobre la foto; sin uso hoy.

---

## (b) Las 25 páginas más importantes: imagen principal y veredicto

Calificación 1–5: **N** nitidez · **E** exposición y color · **C** encuadre · **V** qué tanto vende lo que ofrece la página. "Render/IA" indica mi lectura con su certeza; no es una afirmación de hecho.

| # | Página | Imagen principal (hero) · og:image | N | E | C | V | Observaciones | Veredicto |
|---|---|---|---|---|---|---|---|---|
| 1 | `/` | `obra/cuadrilla-tendiendo-pasto-san-agustin.webp` 1024×1536 · og `jardin-diseno-…-og.webp` 1200×630 | 5 | 4 | 4 escritorio / 2 celular | 5 | Render/IA, certeza media-alta (tamaño nativo de generador, logo perfecto, luz de estudio). En celular el recorte 4:3 corta la cabeza y deja "ERRA Viveros". Pie "Zona Tampico–Madero · tendido de tepes". La comparten `/mayoreo-pasto-tampico` y el protocolo de cuidados. | **Sustituir** por foto real de la cuadrilla (toma 1). Mientras: recortar distinto en celular (anclar arriba). |
| 2 | `/pasto-en-rollo-tampico` | `obra/rollos-pasto-san-agustin-camioneta.webp` 900×1111 · og `despues-instalacion-…webp` 933×1400 | 5 | 4 | 4 / 2 celular (corta cabeza y logo) | 4 | Render/IA, certeza media-alta. La misma imagen es hero de `/precios`. El og sí parece foto real, pero es vertical. | **Sustituir** cuando haya foto real de la camioneta cargada; og: **recortar** a 1200×630. |
| 3 | `/pasto-sintetico-tampico` | `galeria/obra-residencial-tampico.webp` 960×1440 (losas con franjas de pasto) | 5 | 4 | 4 | 5 | Muy atractiva. Pie "Obra de Viveros Terra". El original mide 1024×1536; certeza baja-media de que sea render: el dueño debe confirmar. og vertical. | **Dejar** si el dueño confirma que es obra; og: **recortar** horizontal. |
| 4 | `/pasto-sintetico` (tienda) | `galeria/obra-proyecto-03.webp` 960×1280 | 3 | 4 | 3 | 4 | Foto real de celular; estacas visibles en el pasto, cielo quemado. | **Dejar**; mejor aún, cambiar por `obra/terra/pasto-sintetico-01-terraza-con-alberca`. |
| 5 | `/pasto-sintetico/toscana-28` (y las otras 8 fichas) | `galeria/<modelo>-1.webp` 720×960 | 3 | 4 | 4 | 3 | Reales y muy consistentes (mismo ángulo con el rollo enrollado arriba). En escritorio se muestran a 703 px de ancho desde 720 px: en pantalla retina se ven blandas. Falta el detalle macro. | **Dejar** y sumar macro y perfil (toma 6). |
| 6 | `/diseno-jardines-tampico` | `portadas/diseno-jardines-tampico-proyecto.webp` 960×1574 (hojas de alocasia) · og `diseno-jardines-tampico-viveros-terra.webp` 1536×1024 | 4 | 4 | 3 | 2 | El hero es un acercamiento de follaje: no muestra un jardín diseñado. El og es gente frente a una computadora, oscuro, render/IA certeza media-alta. Hero compartido con `/jardineria-lomas-de-rosales-tampico`. | Hero: **sustituir** por una vista amplia terminada (ya existe: `terra/diseno-jardines-06-escalones-junto-a-alberca`). og: **sustituir**. |
| 7 | `/mantenimiento-jardines-tampico` | `portadas/mantenimiento-jardines-poda-pasto-tampico.webp` 960×1440 | 5 | 4 | 4 / 3 celular | 4 | Render/IA certeza media-alta (mismo uniforme perfecto). Compartida con `/jardineria-aguila-tampico` y 2 artículos. | **Sustituir** por la real `terra/mantenimiento-jardines-02-recorte-de-seto-a-mano` (trabajador con chaleco Terra). |
| 8 | `/sistema-riego-tampico` | `portadas/riego-pro-01.webp` 960×640 · og `tecnico-terra-riego-industrial-tampico.avif` 490×690 | 5 | 4 | 4 | 4 | Hero: render/IA o banco, certeza media-alta (edificio de ladrillo tipo campus de EE. UU., luz dorada). El og **no muestra ningún técnico**, mide 490 px y está en AVIF (WhatsApp y Facebook no lo previsualizan de forma fiable). Hero compartido con `/jardineria-lomas-del-chairel-tampico`. | Hero: **sustituir** (`terra/sistema-riego-04-instalacion-del-controlador` o `-01-aspersores-a-contraluz`). og: **sustituir** ya. |
| 9 | `/vivero-tampico` | `portadas/arboles-tampico-viveros-terra.webp` 960×1280 · og `plantas-tropicales-tampico-viveros.webp` 1024×1536 | 3 | 3 | 3 | 2 | Foto real y valiosa (dos personas sembrando, chaleco Terra), pero es una obra en casa de cliente, **no el vivero**. Es la única imagen de toda la página. La misma foto encabeza `/plantas-palmas-arboles-tampico` y `/arboles-ornamentales-tampico`. | **Sustituir** por fachada y pasillos del vivero (toma 2). Prioridad máxima. |
| 10 | `/plantas-palmas-arboles-tampico` | la misma de #9 · og `paisajismo-alberca-plantas-tampico.webp` 1536×1024 | 3 | 3 | 3 | 3 | Tres páginas con la misma portada. | **Sustituir** por foto de pasillo del vivero con variedad (ya hay: `terra/plantas-palmas-arboles-04-arbustos-con-flor-fucsia`). |
| 11 | `/catalogo.html` | Sin hero. Primera foto visible: `catalogo/acacia-negra-tampico.webp` 480×640 | 3 | 3 | 3 | 2 | La primera imagen que carga (y la de mayor prioridad) lleva el logo de una universidad y el sello Creative Commons. Certeza alta: se lee en la foto. | **Sustituir** esa foto; ver sección 4. |
| 12 | `/palmas-tropicales-tampico` | `portadas/palma-real-jardin-residencial-tampico.webp` 900×1600 · sin og | 5 | 5 | 4 | 4 | Demasiado limpia (cielo perfecto, sin cables ni vecinos): render/IA certeza media. | **Sustituir** cuando haya palma real plantada por Terra; añadir og. |
| 13 | `/arboles-ornamentales-tampico` | la misma de #9 · sin og | 3 | 3 | 3 | 3 | Repetida. | **Recortar distinto** o cambiar por `terra/plantas-palmas-arboles-09-arboles-jovenes`; añadir og. |
| 14 | `/plantas-para-jardin-tampico` | `portadas/jardin-residencial-tropical-tampico.webp` 960×640 · sin og | 4 | 2 | 3 | 3 | **Oscura** (sombras cerradas, un tercio de la imagen casi negro). Original 1536×1024: render/IA certeza media. Compartida con `/jardineria-country-club-tampico` y es og de 5 artículos. | **Sustituir** (`terra/plantas-para-jardin-03-flores-tropicales` o `-04-espigas-amarillas`). |
| 15 | `/plantas-de-interior-tampico` | `portadas/plantas-ornamentales-tampico-viveros-terra.webp` 960×1440 (adelfa rosa en jardinera) · sin og | 5 | 5 | 4 | 1 | **No corresponde**: la adelfa es planta de exterior a pleno sol. Render/IA certeza media. La misma imagen es og o portada de 10 páginas de temas distintos. | **Sustituir** (`terra/plantas-de-interior-03-hoja-ancha-con-brotes-rojos`). |
| 16 | `/arboles-para-banqueta-tampico` | `portadas/arboles-vivero-tampico-mayoreo.webp` 960×1440 · sin og | 5 | 4 | 4 | 4 | Render/IA certeza media-alta (uniforme y logo idénticos al resto de la serie). | **Sustituir** por foto real de árboles en bolsa en el vivero. |
| 17 | `/tierra-negra-vegetal-tampico` | `portadas/camion-tierra-negra-entrega-tampico.webp` 960×640 | 5 | 4 | 4 | 4 | Render/IA **certeza alta**: camión de modelo estadounidense con rótulo "TERRA" y un subtítulo ilegible. En la misma página, Fig. 07 (`tierra-negra-sacos-viveros-terra.webp`) muestra costales con el texto "TIERRA VIVEROA NEGRA VEGETAL". | **Sustituir** ambas (toma 4). La de los costales es la más urgente del sitio. |
| 18 | `/marmol-blanco-tampico` | `portadas/marmol-blanco-alberca-palmera-tampico.webp` 900×1200 | 5 | 5 | 5 | 5 | Excelente imagen. No puedo saber si es obra propia, banco o render (certeza baja en cualquier sentido). La página ya tiene una real: costales en el vivero. | **Dejar** si el dueño confirma el origen. |
| 19 | `/tezontle-rojo-tampico` | `tezontle-rojo-jardin-tampico-sendero.webp` **194×259 px** (también es el og) | 1 | 3 | 2 | 2 | **Pixelada**: se muestra a 401 px en escritorio y a 682 px físicos en celular (3.5× de ampliación). Las otras dos fotos miden 259×194. No hay foto en la primera pantalla ni en escritorio. | **Sustituir** (toma 3). Es la más fácil de resolver con el celular. |
| 20 | `/piedra-bola-rio-tampico` | `jardin-residencial-plantas-pasto-tampico.webp` 933×1400 | 4 | 4 | 4 | 1 | **No corresponde**: es un jardín sin piedra bola a la vista. | **Sustituir** (ya hay: `terra/diseno-jardines-05-jardin-con-piedra-bola`). |
| 21 | `/post/nochebuenas-tampico-madero-mayoreo` | `nochebuenas/nochebuena-roja-tres-plantas-tampico-1600.webp` 1600×1199 | 5 | 5 | 4 | 5 | Real, nítida, color intenso. En escritorio se recorta de horizontal a vertical sin perder el sujeto. og horizontal de 1600 px: correcto. | **Dejar**. Es el estándar a igualar. |
| 22 | `/precios` | `precios/pasto-rollo-jardin.webp` 960×1185 | 5 | 4 | 4 | 3 | La misma imagen (render/IA media-alta) de `/pasto-en-rollo-tampico`. | **Sustituir** junto con #2. |
| 23 | `/mayoreo-pasto-tampico` | `portadas/instalacion-pasto-rollo-san-agustin-tampico.webp` 960×1440 | 5 | 4 | 4 | 3 | La misma del inicio. Para mayoreo vende más la escala: `terra/pasto-en-rollo-01-explanada-de-pasto` o `-07-area-verde-industrial`. | **Sustituir** por foto real de obra grande. |
| 24 | `/palmas-mayoreo-proyectos` | `portadas/palmas-reales-mayoreo-vivero-tampico.webp` 694×1041 · og 1200×630 | 4 | 4 | 4 | 5 | Parece foto real del vivero (palmas en costal blanco, malla sombra). og con proporción correcta. | **Dejar**. |
| 25 | `/jardineria-ciudad-madero` (y las otras 5 páginas de zona) | Una portada distinta por zona, todas de la serie de renders; 1 imagen por página | 5 | 4 | 4 | 2 | Ninguna muestra la colonia o la ciudad de la que habla la página. `/jardineria-altamira` usa un parque con un letrero "Explanada" (origen incierto). | **Sustituir** por una foto real de obra en cada zona (toma 9). |

Otras portadas vistas: `/blog` (jardinero con chaleco de logo verde, 1536×1024, render/IA media-alta).

**Páginas que comparten foto** (hero u og):
- `galeria/obra-proyecto-02.webp`: og de las 11 páginas de envío y de `/pasto-sintetico/perros` (15 usos).
- `plantas-ornamentales-tampico-viveros-terra` (adelfa): 10 páginas (plantas de interior, duranta, ficus elástica, palma viajera, jardín vertical, cómo medir plantas, buganvilia…).
- `pasto-en-rollo-san-agustin-tampico` (camioneta): 7 · `pasto-sintetico-residencial-tampico`: 7 artículos · `plantas-tropicales-tampico-viveros` (alocasia): 6 · `jardin-residencial-plantas-pasto`: 6 · `jardin-residencial-tropical`: 6.
- `portadas/arboles-tampico-viveros-terra`: `/vivero-tampico`, `/plantas-palmas-arboles-tampico`, `/arboles-ornamentales-tampico`.
- `especie-palma-cola-zorra-tampico.webp` y `especie-palma-triangulo-tampico.webp` son **el mismo archivo byte a byte** y encabezan los artículos de dos palmas distintas.
- Tabla completa: `paginas-hero-og.csv`.

**Recorte real medido (Playwright, sitio en vivo):**

| Página | 375 px | 1440 px |
|---|---|---|
| `/` | Foto a 823 px de altura (fuera de la primera pantalla). Caja 341×255 (4:3) sobre foto 2:3, centrada: corta cabeza y logo. | Caja 495×619, recorte leve; bien. |
| `/pasto-en-rollo-tampico` | A 1,023 px. Corta la cabeza; queda media playera. | 501×627 sin recorte; bien. |
| `/pasto-sintetico-tampico` | A 983 px. Recorte limpio. | Bien. |
| `/pasto-sintetico/toscana-28` | A 1,031 px. Bien (etiqueta "28 mm" visible). | 703×938 desde archivo de 720 px: blanda en retina. |
| `/diseno-jardines-tampico` | A 934 px. Solo hojas. | Bien de recorte, flojo de contenido. |
| `/sistema-riego-tampico` | A 883 px. Bien. | Horizontal recortada a vertical: pierde los aspersores del fondo. |
| `/vivero-tampico` | A 849 px. Bien. | Bien. |
| `/mantenimiento-jardines-tampico` | A 802 px. Corta la cabeza. | — |
| `/tezontle-rojo-tampico` | A 1,908 px. Pixelada. | Sin foto arriba; tres fotos chicas borrosas más abajo. |
| `/post/nochebuenas-…` | A 825 px. Bien. | Bien. |
| `/catalogo.html` | Sin foto hasta la cuadrícula. | Primera fila apenas asoma. |
| `/blog/duranta-…` | Sin ninguna imagen. | Sin ninguna imagen. |

Capturas en `capturas/` y montajes en `hojas/cap-movil-*.jpg`, `hojas/cap-desk-*.jpg`, `hojas/cap-hero-movil.jpg`.

---

## 3. Fotos de obra y galerías

**`obra/` (17 imágenes).** Limpias y coherentes entre sí, pero la mayoría parecen render/IA (certeza media-alta para las 6 con persona uniformada: mismo tono de playera, mismo logo, misma luz; `cuadrilla-tendiendo-pasto` mide 1024×1536). Tres sí parecen fotos de celular reales: `riego-aspersor-borde-pasto`, `riego-aspersor-emergente-pasto`, `riego-goteo-philodendron` (640×1423, verticales muy altas, nitidez media). Detalle a corregir: la Fig. 04 de riego dice "Aspersor emergente en jardinera" sobre el archivo `riego-goteo-philodendron`: nombre y pie no coinciden.

**`obra/terra/` (63 fotos reales).**
- **Estilo y revelado:** homogéneo en intención, pero pasado de fuerza. Se ve claridad y contraste local altos, verdes muy saturados y halos alrededor de siluetas (ejemplos: `plantas-palmas-arboles-02`, `-05`, `pasto-en-rollo-01`, `mantenimiento-jardines-06`). Junto a las portadas suaves, se leen como "foto de celular filtrada". Recomiendo bajar claridad y saturación un punto en la siguiente pasada (decisión del dueño).
- **Variedad:** buena. Hay residencial, corporativo, espacio público, vivero y detalle. No se repite el mismo ángulo, salvo las 6 de riego (4 son aspersores sueltos).
- **Personas, cuadrilla y marca:** solo 3 de 63 muestran a alguien trabajando (`mantenimiento-jardines-02` con chaleco Terra, `pasto-sintetico-02-union-de-rollos`, `sistema-riego-04` de espaldas con playera roja sin marca). **Ningún vehículo con marca, ninguna foto de equipo completo, ningún rostro.**
- **Antes y después:** no hay ni un par. Hay "en instalación" y "terminado" de obras distintas.
- **Escala:** bien resuelta en corporativo (`pasto-en-rollo-01`, `-07`); en residencial faltan vistas amplias (casi todo son rincones).
- **Referencias locales (muy valiosas):** `diseno-jardines-02-faro-de-tampico` (letras TAMPICO y faro), `mantenimiento-jardines-06-jardinera-con-escultura` (con el puente al fondo), `jardin-residencial-pasto-alberca` y `pasto-sintetico-01` (laguna).
- **Proporciones:** de 643×1200 a 1200×702; el mosaico las absorbe, pero no sirven tal cual como portada horizontal.

**Galería de pasto sintético (89 imágenes distintas).** Reales, consistentes y honestas. Límites: resolución máxima 720×960; las tomas de "instalado" son pocas (Bali 3, Capri 2, Viena 2, Toscana 1 cada una, Irlanda 1; Aruba, Japonés y Mónaco ninguna); `bali-35-4` y `-6` son nocturnas y oscuras; `irlanda-25-4` muestra una alberca con lona azul y desorden. Las 9 muestras `pasto-sintetico/<modelo>.jpg` (800×800, ~200 KB, JPG) se ven blandas, como ampliadas (certeza media; `aruba-10.jpg` es la más evidente).

**Nochebuenas (10 fotos).** Reales, nítidas, buen color. Todas son rojas: la página ofrece rosa y jaspeada y no hay foto de ninguna.

**Logos de clientes.** `logo-gobierno-tampico-c`, `logo-grupo-velas-c` y `logo-velamar-c` se ven con borde dentado y texto ilegible a 120 px de alto (certeza alta). Taghleef mide 584×120 frente a 120×120 de BMW: pesos visuales disparejos.

---

## 4. Catálogo de plantas (117 fotos)

**Consistencia: baja.**
- Fondo: 81 sobre blanco o claro (recortes de tienda), 36 de exterior o con fondo. 4 son recortes con transparencia y borde dentado (`arbusto-de-playa`, `jacaranda`, `palma-estrella`, `palma-licuala`).
- Proporción: 48 cuadradas, 56 verticales, 13 horizontales; la tarjeta las fuerza a 4:5 con recorte, así que a las horizontales se les cortan los lados.
- Tamaño: 94 miden 480 px de ancho; 13 son más chicas (`eucalipto` 146×280, `ficus-lyrata` 195×259, `liquidambar` 236×315, `flor-de-mayo` 238×280, `palma-cocotera` 266×190, `papiro-estrella` 267×320, y otras).
- Escala del sujeto: se mezclan macetas de 6", árboles adultos de 15 m y palmas de playa; no comunica "así te la entrego".

**Con marca de agua, logo ajeno o captura (certeza alta: se lee en la imagen).** Confirmo a ojo las 24 de `FOTOS_POR_REVISAR`, entre ellas: `eucalipto` y `flor-de-mayo` (Shutterstock, con número), `tronadora` (franja de Dreamstime), `polyalthia` y `lluvia-de-oro` (marca en mosaico), `acacia-negra` (logo de universidad y CC), `palma-cola-de-pescado` (captura de Google con el botón "Visit"), `orquidea-pata-de-vaca` (cuadriculado de transparencia falso), `beucarnea-soyate`, `clorofito-liston`, `wudelia-rastrera` e `ixora-karla` (redviverista), `esparrago-meyeri` (mashrita.com), `eleagnus`, `floripondio`, `aralia-elegantisima`, `aralia-shaflera`, `agave-atenuata`.

**Adicionales que no están en esa lista:**
- `especie-palma-bambu-chamaedorea-tampico.webp` (fuera de `catalogo/`, portada y og del artículo de palma bambú): marca "www.mashrita.com" en la maceta. Certeza alta.
- `sansiviera-tampico` y `sansiviera-variegada-tampico`: la misma foto para dos fichas.
- De banco o de otra tienda por su aspecto (certeza media, sin marca visible): `coco-plumoso` (playa de resort), `palma-kerpis`, `palma-real` (avenida), `palo-de-rosa-guayacan`, `fresno`, `magnolia`, `adenium`, `azalea`, `cuna-de-moises`, `palma-seifrixi-bambu` (interior con mueble), `duranta-cubana`.

**Flojas por calidad:** las 13 chicas, las 4 de borde dentado, `cactus-organo` (2 KB), `bambu-tarro` (3 KB, una vara diminuta), `moneda-enredadera` (4 KB), `uva-de-playa`.

**Las que sí parecen del vivero (certeza media) y marcan el camino:** `ceiba`, `cola-de-caballo`, `palma-cica-revoluta`, `palma-washingtona`, `palma-de-madagascar`, `ficus-benjamin`, `liquidambar` (mala resolución), `olivo-negro`.

---

## 5. Técnico

| Tema | Estado | Dato |
|---|---|---|
| Formato | Bien | 494 WebP en uso, 17 JPG, 5 PNG, 1 AVIF, 2 SVG. Los PNG en uso son og de 3 artículos (273–362 KB cada uno). |
| `width`/`height` | Bien | 627 de 627 `<img>` los declaran y coinciden con la proporción del archivo. |
| `loading` | Bien, con un detalle | 551 `lazy`, 54 `eager`, 22 sin atributo; 51 con `fetchpriority="high"`. En el catálogo la foto prioritaria es la de la acacia con logo ajeno. |
| `srcset`/`sizes` | Pendiente | 474 de 627 (76 %) sin `srcset`. Blog 61 de 61, plantas 203 de 236, materiales 21 de 24, inicio 16 de 17. Ninguna con `srcset` sin `sizes`. |
| Peso | Pendiente | 106 archivos en uso de más de 200 KB (lista con su página en `pesadas-mas-200kb.csv`). |
| Tamaño frente a lo mostrado | Mixto | Miniaturas de 120×80 px que cargan archivos de 560 a 900 px (inicio: 7; plantas: 5). Tezontle 194 px mostrado a 401 px. Fichas de sintético 720 px para 703 px CSS. `obra-proyecto-04-sm` 400 px para una caja de 827 px. |
| `og:image` | Pendiente | 6 páginas indexables sin og (`/arboles-ornamentales-tampico`, `/arboles-para-banqueta-tampico`, `/palmas-tropicales-tampico`, `/plantas-para-jardin-tampico`, `/plantas-de-interior-tampico`, protocolo de cuidados). De 101 con og: 73 verticales, 5 cuadradas, 20 horizontales fuera de proporción y solo 3 en 1.91:1; 83 miden menos de 1,200 px de ancho; 1 en AVIF. |
| `alt` | Mixto | 513 con texto, 114 vacíos. Detalle abajo. |
| Nombres de archivo | Mixto | Detalle abajo. |
| Sitemap | Menor | 107 URL, sin entradas de imagen. |

**Las más pesadas en uso (top 15):**

| KB | Tamaño | Archivo | Página |
|---|---|---|---|
| 521 | 1200×996 | `obra/terra/mantenimiento-jardines-07-area-verde-frente-a-reja.webp` | `/mantenimiento-jardines-tampico` |
| 513 | 787×1400 | `diseno-jardin-instalacion-plantas-tampico.webp` | `/cuestionario.html` |
| 512 | 983×1200 | `obra/terra/plantas-palmas-arboles-08-gramineas-y-arbustos.webp` | `/plantas-palmas-arboles-tampico` |
| 492 | 1200×1200 | `obra/terra/plantas-palmas-arboles-05-gramineas-en-bolsa.webp` | `/plantas-palmas-arboles-tampico` |
| 475 | 1200×1024 | `obra/terra/pasto-en-rollo-02-parterre-circular-sobre-pasto.webp` | `/pasto-en-rollo-tampico` |
| 469 | 1200×1095 | `obra/terra/plantas-de-interior-05-helechos-de-follaje-rizado.webp` | `/plantas-de-interior-tampico` |
| 427 | 1200×1073 | `obra/terra/pasto-en-rollo-07-area-verde-industrial.webp` | `/pasto-en-rollo-tampico` |
| 425 | 1038×1176 | `obra/terra/pasto-sintetico-03-patio-con-pasto-sintetico.webp` | `/pasto-sintetico-tampico` |
| 420 | 1200×848 | `obra/terra/plantas-palmas-arboles-01-lote-de-hoja-variegada.webp` | `/plantas-palmas-arboles-tampico` |
| 419 | 1200×1073 | `obra/terra/sistema-riego-05-aspersor-junto-a-banqueta.webp` | `/sistema-riego-tampico` |
| 413 | 1200×1176 | `obra/terra/pasto-sintetico-01-terraza-con-alberca.webp` | `/pasto-sintetico-tampico` |
| 411 | 1058×1200 | `obra/terra/pasto-sintetico-05-pasto-a-ras-de-piso.webp` | `/pasto-sintetico-tampico` |
| 408 | 1118×1200 | `obra/terra/plantas-palmas-arboles-06-coniferas-en-hilera.webp` | `/plantas-palmas-arboles-tampico` |
| 385 | 933×1400 | `despues-instalacion-pasto-san-agustin-tampico.webp` | `/pasto-en-rollo-tampico` + 1 artículo |
| 376 | 933×1400 | `areas-verdes-paisajismo-tampico.webp` | 1 artículo |

Patrón: 52 de las 106 son de `obra/terra/` a 1200 px. El revelado con mucha claridad genera textura fina que el WebP comprime mal; incluso la variante `-640` de `palmas-tropicales-02` pesa 251 KB. Las 27 de la galería de sintético (720×960, 220–290 KB) son textura pura y también se pueden bajar.

**Texto alternativo (calidad).**
- Bien: `obra/terra/` y nochebuenas describen lo que se ve ("Pasto recién instalado en un parque, con bancas protegidas con plástico…"). Catálogo: "Nombre (científico)", correcto.
- Mal en el blog: el `alt` es el título del artículo sobre una foto genérica que no lo muestra. Ejemplos: "Duranta erecta en Tampico" sobre la adelfa rosa; "Árboles para banqueta en Tampico" y "Jardín en Tampico pensado para perros y gatos" sobre el mismo jardinero con un filodendro; "Cómo medir plantas altura cepellón" sobre la adelfa. Repite palabras clave y no describe.
- 30 imágenes tienen textos distintos según la página; aceptable cuando ambos describen, engañoso en el blog.
- 114 vacíos: la mayoría son miniaturas dentro de tarjetas con texto al lado (válido como decorativas). Conviene revisar los de tienda (46) y plantas (34), porque incluyen fotos de producto que sí informan.
- 92 de 513 mencionan ciudad o marca: sin exceso.

**Nombres de archivo.** Minúsculas con guiones, descriptivos: bien. Detalles: `obra/terra/` es el mejor ejemplo (`servicio-NN-descripción`). El sufijo `-tampico` en las 117 del catálogo y en casi toda la raíz no aporta. Engañosos: `tecnico-terra-riego-industrial-tampico.avif` (no hay técnico ni industria), `riego-goteo-philodendron` (es aspersor), `riego-real-02…05` (mármol), `jardin-fotorealista-residencial-tampico` (delata el render), `obra-proyecto-01…05` (genéricos).

---

## (c) Las 15 imágenes más débiles

| # | Archivo | Dónde | Por qué | Certeza |
|---|---|---|---|---|
| 1 | `tezontle-rojo-jardin-tampico-sendero.webp` (194×259), `-lateral` y `-bordillo` (259×194) | Hero y og de `/tezontle-rojo-tampico` | Pixeladas: ampliadas 2 a 3.5 veces. | Alta (medido) |
| 2 | `tierra-negra-sacos-viveros-terra.webp` | `/tierra-negra-vegetal-tampico`, Fig. 07 | Texto del costal "TIERRA VIVEROA NEGRA VEGETAL": error típico de imagen generada, con la marca encima. | Alta |
| 3 | `camion-tierra-negra-entrega-tampico.webp` (y `portadas/`) | Hero y og de tierra negra | Camión con rótulo ilegible bajo "TERRA"; modelo de camión ajeno al mercado local. Se presenta como "Entrega de tierra negra · Tampico". | Alta |
| 4 | `tecnico-terra-riego-industrial-tampico.avif` | og de `/sistema-riego-tampico` | 490×690, AVIF, vertical, y el contenido no coincide con el nombre. | Alta |
| 5 | `catalogo/eucalipto-tampico.webp`, `flor-de-mayo-tampico.webp` | Catálogo | Marca de agua de Shutterstock legible; 146 y 238 px de ancho. | Alta |
| 6 | `catalogo/tronadora`, `polyalthia`, `lluvia-de-oro` | Catálogo | Franja de Dreamstime y marcas en mosaico. | Alta |
| 7 | `catalogo/acacia-negra-tampico.webp` | Primera foto del catálogo (la prioritaria) | Logo de universidad y sello CC en las esquinas. | Alta |
| 8 | `catalogo/palma-cola-de-pescado-tampico.webp` | Catálogo | Captura de Google Imágenes: se ve el botón "Visit" y un título cortado. | Alta |
| 9 | `catalogo/orquidea-pata-de-vaca-tampico.webp` | Catálogo | Cuadriculado de "transparencia" pegado en la foto. | Alta |
| 10 | `catalogo/arbusto-de-playa`, `palma-estrella`, `palma-licuala`, `jacaranda` | Catálogo | Recortes con borde dentado y pixelado. | Alta |
| 11 | `especie-palma-bambu-chamaedorea-tampico.webp` | Portada y og de su artículo | Marca "mashrita.com" en la maceta. | Alta |
| 12 | `especie-palma-cola-zorra-tampico.webp` = `especie-palma-triangulo-tampico.webp` | og de dos artículos de palmas distintas | Mismo archivo para dos especies; además parece un modelo 3D con sombra artificial. | Alta (duplicado) / media (3D) |
| 13 | `diseno-jardines-tampico-viveros-terra.webp` | og de `/diseno-jardines-tampico` | Oscura, gente frente a una computadora, no muestra un jardín; 1536×1024. | Media-alta (render) |
| 14 | `jardin-residencial-tropical-tampico.webp` (y `portadas/`) | Hero de plantas para jardín y Country Club; og de 5 artículos | Subexpuesta; un tercio en negro. | Alta (exposición) |
| 15 | `plantas-ornamentales-tampico-viveros-terra` (adelfa) | 10 páginas, incluida plantas de interior | Bonita pero usada donde no corresponde, con `alt` de otros temas. | Alta (uso) |

Menciones: `portadas/riego-pro-01` (render o banco con arquitectura ajena); `galeria/obra-proyecto-01` (900×756, 43 KB, blanda, portería de fondo; publicada como "Obra en la región", origen dudoso, certeza media); `bali-35-4` y `-6` (nocturnas); logos de Gobierno de Tampico, Grupo Velas y Velamar (ilegibles).

---

## (d) Las 10 mejores (para usarlas más)

Todas reales según el flujo de la etapa de fotos; ya están publicadas.

1. `nochebuenas/nochebuena-roja-tres-plantas-tampico-1600.webp`: nítida, color pleno; modelo de cómo debe verse un hero.
2. `nochebuenas/nochebuena-roja-invernadero-tampico-1200.webp`: escala de producción; sirve también para `/vivero-tampico` y mayoreo.
3. `obra/terra/jardin-residencial-pasto-alberca.webp`: jardín terminado con alberca y laguna. Candidata a hero de pasto en rollo y a og del inicio.
4. `obra/terra/pasto-sintetico-01-terraza-con-alberca.webp`: terraza con vista al agua; candidata a hero de la tienda de sintético.
5. `obra/terra/diseno-jardines-06-escalones-junto-a-alberca.webp`: diseño con intención; candidata a hero de diseño de jardines.
6. `obra/terra/mantenimiento-jardines-02-recorte-de-seto-a-mano.webp`: la única con trabajador y chaleco Terra legible; candidata a hero de mantenimiento.
7. `obra/terra/diseno-jardines-02-faro-de-tampico.webp`: prueba local inconfundible; para inicio y para la zona Tampico.
8. `obra/terra/pasto-en-rollo-01-explanada-de-pasto.webp` (con `-07-area-verde-industrial`): escala corporativa; para mayoreo y empresas.
9. `obra/terra/pasto-sintetico-02-union-de-rollos.webp`: proceso real con persona; para "cómo instalamos".
10. `portadas/palmas-reales-mayoreo-vivero-tampico.webp` y `portadas/arboles-tampico-viveros-terra.webp`: vivero con existencias y cuadrilla sembrando.

También fuertes: `sistema-riego-01-aspersores-a-contraluz`, `mantenimiento-jardines-06-jardinera-con-escultura`, `plantas-palmas-arboles-04-arbustos-con-flor-fucsia`, `plantas-para-jardin-03-flores-tropicales`.

---

## (e) Lista de tomas para el dueño (con celular), por prioridad

Reglas para todas: limpiar el lente; cámara trasera principal a 1× (evitar el gran angular 0.5×, deforma); sin zoom digital; HDR automático; sin filtros; sostener con las dos manos; 3 disparos por encuadre. Mejor luz: de 7:30 a 9:30 y de 17:00 a 18:30; día nublado claro también sirve. Evitar de 12:00 a 15:00. Enviar los originales (AirDrop, cable o Drive), no por WhatsApp porque comprime. Cada toma en **horizontal y vertical**: la horizontal sirve para escritorio y para compartir en WhatsApp; la vertical para celular.

| Prio | Qué fotografiar | Cómo | Para qué página | Cuántas |
|---|---|---|---|---|
| 1 | **Cuadrilla trabajando con uniforme**: tendiendo pasto, sembrando, podando | Mañana. A la altura del pecho, a 3–4 m, tres cuartos de frente (que se vea la cara o el perfil y el logo). Dejar aire arriba de la cabeza y a un lado para el texto. Con persona. Pedir permiso al trabajador y al cliente. | Hero de `/`, `/pasto-en-rollo-tampico`, `/mantenimiento-jardines-tampico`, `/mayoreo-pasto-tampico`, `/precios` | 12–15 (3 actividades × H y V) |
| 2 | **El vivero: fachada con letrero, entrada, pasillos, mostrador o showroom** | Fachada: desde la acera de enfrente, temprano, sin coches tapando, horizontal y derecha (líneas verticales rectas). Pasillos: a la altura de los ojos, con fuga al fondo, con y sin un cliente o empleado. Una de alguien atendiendo. | `/vivero-tampico` (hoy sin ninguna foto del vivero), `/plantas-palmas-arboles-tampico`, ficha de Google | 10–12 |
| 3 | **Tezontle rojo**: costal, montón, puñado en la mano y un arriate o sendero ya colocado | Nublado o sombra clara para que el rojo no se queme. Detalle a 30–40 cm; aplicación en horizontal a 2–3 m. Mano o pala para dar escala. | `/tezontle-rojo-tampico` (hoy 194 px) | 6 |
| 4 | **Camión o camioneta real descargando tierra negra, y costales reales apilados** | Tres cuartos de frente, a 6–8 m, horizontal, con el vehículo completo y el montón. Si el vehículo tiene rótulo, que se lea. Costales: de frente, a 2 m. | `/tierra-negra-vegetal-tampico` (sustituye las dos imágenes con texto falso), `/marmol-blanco-tampico`, `/piedra-bola-rio-tampico` | 8 |
| 5 | **Antes y después de una misma obra** | Marcar el punto en el suelo y tomar exactamente el mismo encuadre antes, durante y al terminar; horizontal, misma hora si se puede. | `/pasto-en-rollo-tampico`, `/diseno-jardines-tampico`, `/pasto-sintetico-tampico`, inicio | 3 obras × 3 tomas |
| 6 | **Macro de cada modelo de pasto sintético** | Sobre una mesa cerca de una ventana, luz lateral. (a) Perfil de la fibra con una regla o moneda de $10; (b) el respaldo con los drenajes; (c) cenital a 40 cm; (d) una mano peinando la fibra. Tocar la pantalla para enfocar. | Las 9 fichas `/pasto-sintetico/<modelo>` y la tienda | 9 modelos × 4 = 36 |
| 7 | **Nochebuenas rosa y jaspeada**, tamaños de maceta lado a lado, pedido de mayoreo cargado | Dentro del invernadero (luz difusa). Una planta sola a 60 cm con fondo de hileras; las tres variedades juntas; macetas de 5", 6" y 8" en fila con una mano de referencia. | `/post/nochebuenas-tampico-madero-mayoreo` (hoy solo roja). **Es de temporada: hacerla esta semana.** | 8–10 |
| 8 | **Proceso de instalación paso a paso** (pasto en rollo y sintético) | Misma obra, 5 momentos: terreno preparado, tierra nivelada, tendido, juntas o corte, riego o cepillado final. Horizontal, con persona. | Sección "cómo lo hacemos" de ambas páginas; mayoreo | 2 procesos × 5 |
| 9 | **Una obra terminada por zona** (Tampico, Cd. Madero, Altamira; Lomas de Rosales, Chairel, Águila, Country Club) | Vista amplia del jardín desde una esquina, horizontal, luz de tarde. Sin placas, números de casa ni personas ajenas; con permiso del cliente. | Las 6 páginas `/jardineria-…` | 2 por zona = 12–14 |
| 10 | **Riego**: técnico instalando controlador, zanja con tubería, aspersores funcionando a contraluz | Aspersores: en la tarde, con el sol detrás del agua. Técnico: de perfil, manos y equipo visibles. | `/sistema-riego-tampico` (hero y og) | 6 |
| 11 | **Plantas del catálogo, empezando por las 24 con marca de agua** y las 13 chicas | Montar una "esquina de foto" fija en el vivero: pared o lona lisa clara, sombra abierta. La planta en su bolsa o maceta real, centrada, **vertical**, completa con 10 % de aire, siempre desde la misma distancia y altura. Una vara con marcas cada 50 cm da la escala. | `/catalogo.html` y las 6 páginas de plantas | 37 primero; luego las 117 por lotes de 20 |
| 12 | **Palmas y árboles grandes**: hileras en el vivero y carga con grúa o en plataforma | Horizontal, con una persona al lado para la escala. | `/palmas-mayoreo-proyectos`, `/palmas-tropicales-tampico`, `/arboles-para-banqueta-tampico` | 8 |
| 13 | **Equipo completo** frente al vivero o junto al vehículo | Horizontal, sombra pareja, todos con uniforme, a 5–6 m. | Inicio ("vivero y cuadrilla propia"), `/vivero-tampico` | 3–4 |
| 14 | **Video corto** (15–25 s, sin voz): tendido de un rollo, aspersores encendiendo, recorrido por un pasillo del vivero | Horizontal y vertical, 1080p, celular quieto o movimiento lento; grabar 30 s y recortar. | Hero del inicio o sección de proceso; redes | 3 clips |
| 15 | **Plantas de interior en contexto** y **piedra bola de río** en costal y colocada | Interior: junto a una ventana, sin flash. Piedra: como el tezontle. | `/plantas-de-interior-tampico`, `/piedra-bola-rio-tampico` | 6 + 4 |

Sin cámara: un **mapa ilustrado de cobertura** (Tampico, Madero, Altamira y colonias) para las páginas de zona y de envío, y una **foto real de un envío de pasto sintético embalado** para las 11 páginas `/pasto-sintetico/envio/…`, que hoy comparten una sola imagen.

---

## (f) Mejoras técnicas por impacto

Todas requieren visto bueno del dueño cuando impliquen cambiar o recortar una foto.

1. **Subir la foto a la primera pantalla en celular.** Hoy empieza entre 800 y 1,030 px. Opciones: foto antes de la tarjeta de precio, o una franja de 180–220 px bajo el titular. Es el cambio con más efecto en la primera impresión.
2. **Corregir el recorte del hero en celular** en inicio, pasto en rollo y mantenimiento (`object-position` hacia arriba o un recorte horizontal propio vía `<picture>`), para no cortar cabeza ni logo.
3. **Retirar o sustituir lo que daña la confianza:** costales "TIERRA VIVEROA", camión con rótulo falso, tezontle de 194 px, las fotos con marca de agua del catálogo y la de `especie-palma-bambu`. Mientras no haya foto real, ajustar los pies "Fig." de los renders para que no afirmen lugar ni obra.
4. **`og:image` horizontales de 1200×630 en JPG o WebP** para las 25 páginas principales; añadir las 6 que faltan; cambiar el AVIF de riego. Hoy 73 de 101 son verticales.
5. **`srcset` y `sizes` en lo que falta** (474 imágenes): primero blog (61 de 61), fichas de plantas y materiales. Miniaturas de 120×80 con su variante de 240 px.
6. **Bajar peso de `obra/terra/`** (52 archivos de más de 200 KB): recomprimir a calidad 70–75 o servir 960 px; objetivo menor a 180 KB a 1200 px. Igual con las 27 de la galería de sintético.
7. **Variante de 1,440 px para la foto principal de las 9 fichas de sintético** (hoy 720 px para una caja de 703 px CSS).
8. **Blog:** al menos una imagen propia por artículo (32 de 54 no tienen), y `alt` que describa la foto en vez de repetir el título.
9. **Catálogo:** que la primera foto (prioritaria) no sea una con logo ajeno; unificar proporción a 4:5 al fotografiar; las 4 con transparencia, sobre fondo liso.
10. **Limpieza de `/img/`:** 152 archivos sin uso (31 MB), con prioridad a las capturas de pantalla `riego-real-06…09` y `riego-tampico-06/07`. Corregir nombres engañosos al sustituir.
11. **Menores:** imágenes en el sitemap; revisar los 114 `alt` vacíos en tienda y plantas; regenerar los logos de Gobierno de Tampico, Grupo Velas y Velamar desde un original nítido; convertir a WebP las 9 muestras JPG de sintético.

---

## (g) Qué no pude verificar

- **Si una imagen es generada por IA, render o foto real.** Los WebP no traen metadatos y no encontré marcas C2PA. Mis lecturas se basan en indicios visibles (dimensiones nativas de generador, texto deformado, logos idénticos, luz, arquitectura) y en que el repo ya habla de "renders". Solo el dueño puede confirmarlo imagen por imagen. Tienen certeza alta únicamente las que muestran texto deformado o marca de agua legible.
- **Si las 63 fotos de `obra/terra/` y la galería de sintético son obra de Viveros Terra.** Lo asumo por la spec de la etapa de fotos; no hay forma de comprobarlo desde la imagen. Igual con `obra-residencial-tampico` ("Obra de Viveros Terra") y `marmol-blanco-alberca-palmera`.
- **Permisos:** de clientes y domicilios visibles, del uso de logos (BMW, Flex, Taghleef, Gobierno de Tampico, Grupo Velas, Velamar) y de las fotos de catálogo de terceros sin marca visible.
- **Origen exacto de las fotos de catálogo sin marca.** No hice búsqueda inversa (habría implicado enviar imágenes a servicios externos).
- **Vista previa real en WhatsApp, Facebook y Google** de los og verticales, WebP y AVIF: es inferencia a partir de formato y proporción, no una prueba.
- **Otros navegadores y anchos.** Solo Chromium a 375 y 1440 px en 12 páginas; no probé Safari, Firefox, ni 320, 768, 1024 o 1920.
- **Rendimiento medido** (LCP, Lighthouse): no lo corrí para no cargar la máquina; los pesos son de archivo.
- **Nitidez fina de todas las imágenes.** Revisé las 519 en uso en hojas de contacto con miniaturas de 270 a 400 px y a tamaño completo solo una selección; un desenfoque leve puede habérseme pasado.
- **Paridad entre repo y producción.** Los nombres de las imágenes principales en vivo coinciden con `main` en las 12 páginas capturadas; no comparé el resto.
- **Color exacto:** juicio visual sobre miniaturas JPG, sin medición.

---

## Archivos de apoyo (misma carpeta que este informe)

- `hojas/`: hojas de contacto: `heroes-01…05`, `obra-01`, `terra-01…04`, `cat-01…06`, `gal-01…03`, `noche-01`, `cli-01`, `rootused-01`, `rootunused-01…02`, `detalle-01`, y capturas `cap-movil-01…02`, `cap-desk-01…02`, `cap-hero-movil`, `cap-tezontle`.
- `capturas/`: capturas individuales a 375 y 1440 px.
- `paginas-hero-og.csv` (112 páginas con plantilla, hero y og), `pesadas-mas-200kb.csv` (106), `sin-uso.csv` (152).
- `inv.json`, `meta.json`, `render.json`, `alts.json`: datos crudos. Scripts: `inventario.py`, `meta.py`, `sheet.py`, `capturas.py`, `capturas2.py`.
