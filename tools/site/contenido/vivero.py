"""Contenido de /vivero-tampico ("Visítanos"). La foto, título, meta, FAQ y JSON-LD de main; precios, horario y domicilio de
datos.py. Fuera (sin respaldo o contra una regla del dueño): "Lun–Sáb 9am–6pm" (el sábado cierra a las 14 h), "Variedades en
stock", "te decimos si la tenemos disponible", "precios orientativos", "precios más bajos" y "+18 años"."""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from componentes_util import META_AUTOR_RETIRADA
from contenido import seo
from contenido import respuestas

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/vivero-tampico"
FOTO = {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
        "srcset": "/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, /img/portadas/arboles-tampico-viveros-terra.webp 960w",
        "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 960, "alto": 1280,
        "alt": "Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico", "numero": 1,
        "lugar": "Siembra de árboles y plantas en Tampico", "etapa": "Equipo Viveros Terra"}
HORARIO = f"Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h"
DONDE = (f"Viveros Terra tiene su vivero en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero, con {datos.VARIEDADES} variedades "
         "de plantas, palmas, árboles ornamentales y plantas de interior, especies adaptadas al clima cálido-húmedo del Golfo de México.")
PREGUNTAS = (
    ("¿Dónde está el vivero en Tampico?", f"Viveros Terra está en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero — frente al Walmart de Madero. Atendemos de {HORARIO.lower()}."),
    ("¿Cuántas variedades de plantas tienen disponibles?", f"Contamos con más de 200 variedades entre plantas ornamentales, palmas tropicales y árboles para jardín."),
    ("¿Hacen entregas a domicilio en Tampico?", f"Sí, realizamos entregas en toda la zona metropolitana de Tampico, incluyendo Ciudad Madero y Altamira. Contáctanos por WhatsApp para coordinar la entrega y conocer su costo según tu colonia."),
    ("¿Puedo comprar plantas al mayoreo para mi proyecto?", "Sí. Atendemos tanto a clientes particulares como a constructoras, arquitectos, hoteles y empresas. Escríbenos por WhatsApp con tu requerimiento y te cotizamos por volumen."),
)
MENSAJE = mensajes_paginas.UTILITARIAS["vivero"]
# SEO fase 1: las categorías del vivero como lista de sus páginas (antes, un OfferCatalog con tres Product sin precio ni
# foto: Google los marca como productos inválidos y no hay un precio real que ponerles).
CATEGORIAS_LD = {"@type": "ItemList", "name": "Categorías del vivero", "itemListElement": [
    {"@type": "ListItem", "position": n, "name": nombre, "url": f"{SITE}{ruta}"} for n, (nombre, ruta) in enumerate((
        ("Palmas Tropicales", "/palmas-tropicales-tampico"), ("Plantas Ornamentales", "/plantas-para-jardin-tampico"),
        ("Árboles para Jardín", "/arboles-ornamentales-tampico"), ("Catálogo completo", "/catalogo")), 1)]}
# SEO fase 0 (mapa de palabras clave, 2026-11-10): título de 60 y descripción de 153; el mismo texto va en Open Graph.
TITULO = f"Vivero en Tampico y Cd. Madero: {datos.VARIEDADES} Plantas | {datos.NOMBRE}"
DESCRIPCION = ("Vivero en Cd. Madero, frente a Walmart: más de 200 variedades de plantas, palmas y árboles. "
               f"{datos.HORARIO}. Ve cómo llegar y visítanos.")
CONTENIDO = {
    "respuesta": respuestas.de("/vivero-tampico"),  # SEO fase 1: respuesta directa bajo la portada
    "tipo": "vivero",
    "meta": {"title": TITULO, "description": DESCRIPCION,
             "robots": "index, follow", "canonical": URL,
             "og": (("og:type", "website"), ("og:url", URL),
                    ("og:title", TITULO), ("og:description", DESCRIPCION),
                    ("og:image", f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "migas": (("Inicio", "/"), ("Vivero en Tampico", None)),
    "portada": {"kicker": "Tampico · Madero · Altamira", "h1": 'Vivero en Tampico <span class="vt-serif">y Ciudad Madero, desde 2007</span>',
                "lede": f"Pasto, plantas, palmas, árboles y materiales para jardín en {datos.CALLE_CORTA}, Cd. Madero, frente a Walmart.",
                "etiqueta": {"codigo": "Vivero", "aviso": "", "nombre": "Palmas", "antes": "desde", "monto": dinero(P["palma_desde"]),
                             "unidad": "", "filas": (("Pasto", f"{dinero(P['pasto_solo_m2'])}/m²"), ("Plantas", "por tamaño"))},
                "mensaje": MENSAJE, "foto": FOTO, "pos": "50% 66%",
                "enlaces": (("Cómo llegar", datos.MAPS_URL, "vivero:mapas", 'target="_blank" rel="noopener"'),),
                "dato": f"{datos.VARIEDADES} variedades en el vivero"},
    "donde": {"titulo": 'Viveros Terra en Ciudad Madero, <span class="vt-serif">frente a Walmart</span>', "lede": DONDE,
              "hechos": ({"titulo": f"{datos.VARIEDADES} variedades", "texto": "En el vivero"},
                         {"titulo": str(datos.DESDE), "texto": "Año de fundación"},
                         {"titulo": "30 días de garantía", "texto": f'En las plantas que sembramos nosotros. <a href="/politicas#garantia-plantas">Ver condiciones</a>.'})},
    "categorias": {"titulo": 'Categorías <span class="vt-serif">en el vivero</span>', "lede": "Plantas adaptadas al clima cálido-húmedo de Tampico.",
                   "items": (
                       {"titulo": '<a href="/palmas-tropicales-tampico">Palmas Tropicales</a>', "texto": "Palma del viajero, areca, coco, kentia, washingtonia y más. Adaptadas al clima de Tampico para sobrevivir en la zona costera."},
                       {"titulo": '<a href="/plantas-para-jardin-tampico">Plantas Ornamentales</a>', "texto": "Heliconias, bromelias, crotos, ficus, bugambilias y decenas de especies para jardines, interiores y terrazas."},
                       {"titulo": '<a href="/arboles-ornamentales-tampico">Árboles para Jardín</a>', "texto": "Árboles ornamentales, frutales y de sombra para jardines residenciales, corporativos y banquetas en Tampico."},
                       {"titulo": '<a href="/catalogo">Catálogo completo</a>', "texto": f"{datos.VARIEDADES} variedades con foto y descripción. Agrega lo que te interesa y cotiza todo en un WhatsApp."})},
    "llegar": {"titulo": 'Cómo llegar <span class="vt-serif">al vivero</span>',
               "datos": (("Dirección", f'{datos.CALLE}, {datos.COLONIA}, Ciudad Madero, Tamaulipas. {datos.REFERENCIA}. '
                                       f'<a data-cta="vivero:mapas-google" href="{datos.MAPS_URL}" target="_blank" rel="noopener">Abrir en Google Maps</a> · '
                                       f'<a data-cta="vivero:mapas-apple" href="https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&amp;q=Viveros%20Terra" target="_blank" rel="noopener">Apple Maps</a>'),
                         ("Horario de atención", datos.HORARIO),
                         ("Entrega a domicilio", "Entregamos en Tampico, Ciudad Madero y Altamira; te confirmamos el costo por WhatsApp según tu colonia."))},
    "faq": {"titulo": 'Preguntas frecuentes <span class="vt-serif">sobre el vivero</span>', "preguntas": PREGUNTAS},
    "cierre": {"titulo": '¿Buscas una planta <span class="vt-serif">específica?</span>',
               "lede": "Escríbenos con el nombre o una foto y te decimos qué opciones hay para tu espacio y el clima de Tampico.",
               "mensaje": mensajes_paginas.UTILITARIAS["vivero_planta"]},
    "jsonld": ({"@context": "https://schema.org", "@graph": [
        entidad.negocio(),
        CATEGORIAS_LD,
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PREGUNTAS]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                                                        {"@type": "ListItem", "position": 2, "name": "Vivero en Tampico", "item": URL}]},
        {"@type": "SpeakableSpecification", "cssSelector": list(entidad.SPEAKABLE)}]},),
}
M_CATALOGO = ("SEO fase 1: el OfferCatalog traía tres Product sin precio ni foto (inválidos para Google) y no hay un precio "
              "real que ponerles; las categorías van como ItemList con el enlace a su página.")
PARIDAD = {
    "reemplazos": {"Viveros Terra · Tampico": "Viveros Terra en Ciudad Madero, frente a Walmart",
                   "Categorías disponibles en el vivero": "Categorías en el vivero",
                   "Explora el catálogo completo del vivero": "Catálogo completo",
                   "¿Buscas una planta específica?": "¿Buscas una planta específica?"},
    "retirados": {},
    "meta_retirada": META_AUTOR_RETIRADA,
    "meta": seo.paridad(TITULO, DESCRIPCION, {"og:description": (DESCRIPCION, "Sin “Productor directo”: el dueño no lo ha confirmado y 2d y 2f ya lo retiraron.")}),
    "jsonld": {tipo: M_CATALOGO for tipo in ("OfferCatalog", "Offer", "Product")},
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). «Cómo llegar» pasa de botón a enlace de texto; la colonia sale de la entrada (sigue en «En corto» y en «Cómo llegar»).')
