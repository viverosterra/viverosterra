"""Contenido de /pasto-sintetico/perros. Solo datos: la plantilla es plantillas/tienda_guia.py.

Solo afirmaciones presentes en las fichas (data.COMMON_TREATMENTS incluye antibacterial); sin prometer lo que no está
documentado. Título, descripción, canonical, Open Graph y migas: los que publicaba tools/pasto/perros.py.
PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero
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
TITULO = "Pasto sintético para perros: qué modelo elegir y cómo limpiarlo | Viveros Terra"
DESCRIPCION = ("Pasto sintético para perros con envío a todo México: qué modelo elegir, cómo drena la orina, cómo quitar "
               f"el olor y cómo limpiarlo. Desde {DESDE}/m².")
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
                      f"Se limpia con manguera y un limpiador enzimático. Desde <b>{DESDE}/m²</b> con "
                      f"{MAS_BARATO['nombre']}."),
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
        {"tipo": "modelos", "id": "modelos", "rotulo": "Modelos", "titulo": "Tres modelos para mascotas",
         "items": RECOMENDADOS},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas frecuentes con perros",
         "preguntas": PREGUNTAS,
         "notas": ('<a href="/blog/pasto-sintetico-para-perros">Lee la guía completa: pasto sintético para perros</a>',)},
    ),
    "cierre": {"titulo": "Cotiza el pasto para tus perros",
               "lede": ("Dinos tus metros y tu estado: te respondemos con el modelo que conviene y el precio puesto en tu "
                        "casa."),
               "mensaje": MENSAJE},
}

PARIDAD = {"reemplazos": {}, "retirados": {}}
