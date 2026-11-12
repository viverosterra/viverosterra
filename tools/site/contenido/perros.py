"""Contenido de /pasto-sintetico/perros. Solo datos: la plantilla es plantillas/tienda_guia.py.

Solo afirmaciones presentes en las fichas (data.COMMON_TREATMENTS incluye antibacterial); sin prometer lo que no está
documentado. Título, descripción, canonical, Open Graph y migas: los que publicaba tools/pasto/perros.py.
PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero
from contenido import seo
from esquema import breadcrumb_schema

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico/perros"
GAL = t.GAL
FOTO = "obra-proyecto-02"  # og:image (sin cambio); la portada usa otra obra real para no repetir la de las ciudades
RECOMENDADOS = (
    ("irlanda-25", "Fibra más resistente de la colección: aguanta pisoteo y juego diario."),
    ("capri-20", "Alta densidad y fibra corta: fácil de limpiar y de levantar desechos."),
    ("toscana-18", "El más económico para patios chicos o para empezar."),
)
MAS_BARATO = min((data.BY_SLUG[s] for s, _r in RECOMENDADOS), key=lambda m: m["rollo"])
DESDE = dinero(MAS_BARATO["rollo"])
GUIA = '<a href="/blog/como-instalar-pasto-sintetico">guía de instalación</a>'
CRITERIOS = (
    ("Fibra resistente y no muy alta", "De 18 a 25 mm es lo más práctico: se limpia fácil y aguanta el paso diario."),
    ("Base perforada que drene", "La orina tiene que pasar al suelo. Instálalo sobre grava fina compactada, no sobre "
                                 "piso liso sin desnivel."),
    ("Limpieza sencilla", "Levanta los desechos sólidos y enjuaga con manguera. Para el olor, usa un limpiador enzimático "
                          "para mascotas."),
)
# SEO fase 2c (2026-11-11, mapa §2 G7): lo útil del artículo /blog/pasto-sintetico-para-perros, fusionado aquí con 301
# (limpieza de orina y heces, olor y drenaje, errores). Sin la garantía de «5 a 8 años» ni la arena de sílice del artículo.
LIMPIEZA = (
    ("Orina", "Drena sola por las perforaciones del respaldo hacia la base de grava. Enjuaga con manguera las zonas que tu "
              "perro usa más, 1 o 2 veces por semana; una vez al mes aplica agua con vinagre blanco (50/50) o un limpiador "
              "enzimático para mascotas. En temporada de calor intenso, enjuaga más seguido."),
    ("Heces", "Se recogen igual que en pasto natural, con bolsa o pala: la superficie firme no las absorbe. Después pasa un "
              "enjuague puntual y listo."),
    ("Olor y drenaje", "La mayoría de los problemas de olor vienen de una instalación sin base drenante. Con perros, pide "
                       "grava fina o polvo de piedra compactada (3 a 5 cm), una ligera pendiente (1 a 2%) y pasto con "
                       "respaldo perforado. Sobre concreto sin pendiente ni salidas de agua, la orina se estanca debajo."),
)
# La foto del artículo fusionado (la de su tarjeta del índice del blog, mismo archivo, copia de 640 px y alt): las fotos
# no se quitan (regla del dueño); el pie no dice dónde se tomó.
FOTO_ARTICULO = {"src": "/img/pasto-sintetico-residencial-tampico.webp",
                 "srcset": "/img/pasto-sintetico-residencial-tampico-640.webp 640w, /img/pasto-sintetico-residencial-tampico.webp 1024w",
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 1024, "alto": 1536, "numero": 2,
                 "alt": "Pasto sintético para perros y mascotas", "lugar": "Pasto sintético residencial", "etapa": "Instalado"}
ERRORES = (
    ("No clavar bien el perímetro", "Una orilla suelta es una invitación a jalar y escarbar. Clava cada 15 a 20 cm."),
    ("Elegir fibra muy alta", "La de 35 mm o más se ve más lujosa, pero con orina diaria tarda más en secar."),
    ("Saltarse la base drenante", "Ahorrar en la base es la receta del mal olor."),
    ("Nunca enjuagar", "El pasto no se riega, pero con mascotas sí se enjuaga: 5 minutos a la semana bastan."),
)
PREGUNTAS = (
    ("¿El pasto sintético se calienta con el sol?", "Sí, como cualquier superficie exterior al sol. Enjuágalo con "
     "manguera en las horas de más calor y deja una zona de sombra para tu perro."),
    ("¿Mi perro lo puede rasguñar o romper?", "Un perro que escarba puede levantar las orillas si no están bien fijadas. "
     f"Fija el perímetro con clavos o adhesivo como indica la {GUIA}."),
    ("¿El pasto sintético huele a orina?", "Si la base no drena o no se enjuaga, sí. Con grava que drene, enjuague "
     "frecuente y un limpiador enzimático se controla el olor."),
    ("¿Cómo se lava el pasto sintético con perros?", "Levanta los desechos, enjuaga con manguera una o dos veces por "
     "semana y cepilla la fibra de vez en cuando para que quede de pie."),
    ("¿Qué tratamientos tiene el pasto?", f"Todos nuestros modelos tienen de fábrica estos tratamientos: "
     f"{data.COMMON_TREATMENTS}."),
)
TITULO = f"Pasto Sintético para Perros desde {DESDE}/m² | Viveros Terra"
DESCRIPCION = ("Pasto sintético para perros con buen drenaje: qué modelo elegir, cómo quitar el olor a orina y cómo limpiarlo. "
               f"Desde {DESDE}/m² con envío a todo México.")
MENSAJE = "Hola, quiero pasto sintético para mis perros.\nMetros aprox.: ___\nMi estado: ___"

CONTENIDO = {
    "tipo": "tienda",
    "meta": {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large",
             "canonical": URL,
             "og": (("og:type", "article"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
                    ("og:description", DESCRIPCION), ("og:image", f"{SITE}{GAL}/{FOTO}.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), ("Para perros", URL)]),),
    "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), ("Para perros", None)),
    "portada": {
        "kicker": "Mascotas · Envío a todo México",
        "h1": 'Pasto sintético para perros <span class="vt-serif">que drena y se limpia fácil</span>',
        "respuesta": ("Para perros conviene un pasto de 18 a 25 mm con fibra resistente, instalado sobre grava que drene. "
                      f"Desde <b>{DESDE}/m²</b> con {MAS_BARATO['nombre']}."),
        "pos": "50% 40%",
        "mensaje": MENSAJE,
        "href_modelos": "/pasto-sintetico#modelos",
        "texto_modelos": "Ver precios con envío",
        "foto": t.foto_obra("obra-proyecto-01", "(min-width: 1024px) 620px, 100vw", "Pasto de la colección instalado"),
        "datos": (("Altura ideal", "18 a 25 mm", "Fácil de limpiar"), ("Base", "Perforada", "Drena la orina"),
                  ("Tratamientos", "Antibacterial", "UV y retardante al fuego"), ("Desde", f"{DESDE}/m²", MAS_BARATO["nombre"]),
                  ("Entrega", "3 a 5 días", "A todo México"), ("Factura", datos.FACTURA, "Persona física o moral")),
    },
    "secciones": (
        {"tipo": "preguntas", "id": "elegir", "rotulo": "Elegir", "titulo": "Qué pasto sintético conviene para perros",
         "items": CRITERIOS},
        {"tipo": "preguntas", "id": "limpieza", "rotulo": "Limpieza", "titulo": "Cómo se limpia: orina, heces y olor",
         "items": LIMPIEZA, "figura": FOTO_ARTICULO},
        {"tipo": "modelos", "id": "modelos", "rotulo": "Modelos", "titulo": "Tres modelos para mascotas",
         "items": RECOMENDADOS},
        {"tipo": "preguntas", "id": "errores", "rotulo": "Errores", "titulo": "4 errores a evitar con perros",
         "items": ERRORES},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas frecuentes con perros",
         "preguntas": PREGUNTAS},
    ),
    "cierre": {"titulo": "Cotiza el pasto para tus perros",
               "lede": ("Dinos tus metros y tu estado: te respondemos con el modelo que conviene y el precio puesto en tu "
                        "casa."),
               "mensaje": MENSAJE},
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION), "reemplazos": {},
    "retirados": {"/blog/pasto-sintetico-para-perros": ("SEO fase 2c (2026-11-11, mapa §2 G7): el artículo se fusionó en esta "
                                                        "página con 301; su limpieza, olor y errores ya están aquí.")}}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Entrada recortada: «Se limpia con manguera y un limpiador enzimático» sale del hero (sigue en las preguntas).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: fila de WhatsApp y prueba social tras los modelos recomendados.'
