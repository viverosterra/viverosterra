"""Contenido de /vivero-tampico ("Visítanos"). La foto, título, meta, FAQ y JSON-LD de main; precios, horario y domicilio de
datos.py. Fuera (sin respaldo o contra una regla del dueño): "Lun–Sáb 9am–6pm" (el sábado cierra a las 14 h), "Variedades en
stock", "te decimos si la tenemos disponible", "precios orientativos", "precios más bajos" y "+18 años"."""
import datos
import mensajes_paginas
from componentes import boton_mapas, dinero
from componentes_util import META_AUTOR_RETIRADA

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
CONTENIDO = {
    "tipo": "vivero",
    "meta": {"title": "Vivero en Tampico y Cd. Madero: dirección, horario y cómo llegar · Viveros Terra",
             "description": "Visita el vivero de Viveros Terra en Av. Álvaro Obregón 209 Sur, Cd. Madero, frente a Walmart. Más de 200 variedades de plantas, palmas y árboles. Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h.",
             "robots": "index, follow", "canonical": URL,
             "og": (("og:type", "website"), ("og:url", URL),
                    ("og:title", "Vivero en Tampico y Cd. Madero: dirección, horario y cómo llegar · Viveros Terra"),
                    ("og:description", "Vivero en Tampico con +200 variedades de plantas, palmas y árboles. Entrega en Madero y Altamira. Cotiza hoy."),
                    ("og:image", f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "migas": (("Inicio", "/"), ("Vivero en Tampico", None)),
    "portada": {"kicker": "Tampico · Madero · Altamira", "h1": 'Vivero en Tampico <span class="vt-serif">y Ciudad Madero, desde 2007</span>',
                "lede": f"Pasto, plantas, palmas, árboles y materiales para jardín en {datos.CALLE}, {datos.COLONIA}, Cd. Madero, frente a Walmart.",
                "etiqueta": {"codigo": "Vivero", "aviso": "", "nombre": "Palmas", "antes": "desde", "monto": dinero(P["palma_desde"]),
                             "unidad": "", "filas": (("Pasto", f"{dinero(P['pasto_solo_m2'])}/m²"), ("Plantas", "por tamaño"))},
                "mensaje": MENSAJE, "boton_extra": boton_mapas("vivero:mapas"), "foto": FOTO},
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
        {"@type": "LocalBusiness", "name": datos.NOMBRE, "description": f"Vivero en Ciudad Madero con más de 200 variedades de plantas, palmas y árboles. Atendemos Tampico, Madero y Altamira desde {datos.DESDE}.",
         "telephone": datos.TELEFONO_TEL, "url": URL, "image": f"{SITE}/img/plantas-tropicales-tampico-viveros.png",
         "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"},
         "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": list(d), "opens": a, "closes": c} for d, a, c in datos.HORARIO_LD],
         "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Catálogo de plantas, palmas y árboles", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Product", "name": n}} for n in ("Palmas Tropicales", "Plantas Ornamentales", "Árboles para jardín")]}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PREGUNTAS]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                                                        {"@type": "ListItem", "position": 2, "name": "Vivero en Tampico", "item": URL}]},
        {"@type": "SpeakableSpecification", "cssSelector": ["h1", "h2", ".vt-faq summary"]}]},),
}
PARIDAD = {
    "reemplazos": {"Viveros Terra · Tampico": "Viveros Terra en Ciudad Madero, frente a Walmart",
                   "Categorías disponibles en el vivero": "Categorías en el vivero",
                   "Explora el catálogo completo del vivero": "Catálogo completo",
                   "¿Buscas una planta específica?": "¿Buscas una planta específica?"},
    "retirados": {},
    "meta_retirada": META_AUTOR_RETIRADA,
    "meta": {"og:description": (CONTENIDO["meta"]["og"][3][1], "Sin “Productor directo”: el dueño no lo ha confirmado y 2d y 2f ya lo retiraron.")},
    "jsonld": {},
}
