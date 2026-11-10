"""Contenido de /arboles-ornamentales-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Las seis especies de main, en su orden, con la foto del catálogo (contenido/catalogo_especies.json; decisión del dueño,
2026-11-08: las fotos quedan como están); luz, riego y altura salen de ahí, igual que en el catálogo. Precio: solo "Flamboyán desde $250" (datos.PRECIOS_ESPECIE);
crespón $350, jacaranda $450 y olivo negro $600 de main se retiran (sin confirmar; pregunta 1 al dueño). "Instalación con
grúa" se retira de la respuesta de entrega hasta que el dueño la confirme (pregunta 9). Título, descripción y Open Graph
como estaban (Etapa 3).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import plantas_comun as pc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/arboles-ornamentales-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Árboles ornamentales"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
FLAMBOYAN = f"Flamboyán desde {dinero(P['flamboyan'])}"
TITULO = f"Árboles Ornamentales en Tampico desde {dinero(P['flamboyan'])} | Viveros Terra"
DESCRIPCION = (f"Árboles ornamentales para jardín en Tampico: flamboyán desde {dinero(P['flamboyan'])}, jacaranda, crespón y guayacán. "
               "Con entrega y siembra en Madero y Altamira. Cotiza hoy.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("flamboyan-tabachin", "El más espectacular del trópico: flores rojo-naranja que cubren la copa y sombra abundante.",
     None),
    ("crespon-astronomica", "Floración en verano con racimos rosa, lila o blanco; muy usado en jardines y avenidas.",
     None),
    ("palo-de-rosa-guayacan", "Flores rosa brillante que cubren el árbol antes que las hojas.", None),
    ("jacaranda", "Floración morada única para jardines amplios.", None),
    ("lluvia-de-oro", "Racimos de flores amarillas que cubren el árbol en primavera; para jardines y camellones.", None),
    ("olivo-negro", "Sombra amplia y resistente al calor y al salitre; también va en banqueta.", None),
)
PREGUNTAS = (
    ("¿Qué árboles ornamentales son mejores para Tampico?",
     "Flamboyán (floración roja espectacular), crespón (florido y bueno para banqueta), jacaranda (morado), palo de "
     "rosa (rosa brillante), lluvia de oro (amarillo) y olivo negro (sombra resistente). Todos se adaptan al clima del "
     "sur de Tamaulipas."),
    ("¿Cuánto cuesta un árbol ornamental en Tampico?",
     f"{FLAMBOYAN}. Los demás árboles se cotizan según la especie y el tamaño del ejemplar: mándanos cuál te interesa y "
     "la altura por WhatsApp."),
    ("¿Qué árbol florido es mejor para un jardín en Tampico?",
     "Flamboyán (rojo-naranja, el más espectacular), crespón (rosa-lila, floración larga), palo de rosa (rosa intenso) "
     "y lluvia de oro (amarillo brillante)."),
    ("¿Qué árboles son buenos para banquetas en Tampico sin dañar el concreto?",
     "Olivo negro, polyalthia (columnar), neem, fresno y crespón podado: raíz profunda que no levanta la banqueta. "
     "Están en <a href=\"/arboles-para-banqueta-tampico\">árboles para banqueta</a>."),
    ("¿Hacen entrega de árboles grandes en Tampico?",
     "Sí, entregamos árboles de todos los tamaños en Tampico, Madero y Altamira. Los que sembramos nosotros tienen "
     "garantía de arraigo de 30 días, con condiciones: el riego que te indicamos."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "cta_texto": "Cotizar mis árboles",  # Entrega B de experiencia: filas de WhatsApp tras las especies, los precios y las preguntas
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "pos": "50% 66%",
        "dato": 'Garantía de 30 días en lo que sembramos, <a href="/politicas#garantia-plantas">con condiciones</a>',
        "enlaces": (("Ver los 25 árboles del catálogo", "/catalogo?cat=arboles", "plantas:catalogo"),),
        "lema": "De sombra y de flor, para el clima de Tamaulipas.",
        "h1": "Árboles ornamentales para jardines en Tampico",
        "lede": f"{FLAMBOYAN}. Te los llevamos y los sembramos.",
        "etiqueta": {"codigo": "Árboles", "aviso": f"Precios {datos.ANIO}", "nombre": "Flamboyán",
                     "cientifico": "Delonix regia", "antes": "desde", "monto": dinero(P["flamboyan"]), "unidad": "",
                     "nota": "Los demás árboles, según especie y tamaño."},
        "mensaje": MENSAJE,
        "foto": {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/arboles-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Equipo de Viveros Terra sembrando un árbol ornamental en Tampico",
                 "lugar": "Siembra de un árbol ornamental", "etapa": "Tampico"},
    },
    "especies": {"titulo": "Las más solicitadas en Tampico", "lede": pc.LEDE_FOTOS, "items": ESPECIES},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Árboles ornamentales en Tampico: lo que más nos preguntan", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de árboles", "items": (
        ("Flamboyán en Tampico: cuidados y floración", "/blog/framboyan-delonix-regia-tampico"),
        ("7 árboles para banqueta que no levantan el pavimento", "/blog/arboles-para-sembrar-en-banqueta"),
        ("Poda de árboles y palmas", "/blog/poda-arboles-palmas-tampico-guia"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": pc.otras_subcategorias(RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos qué árbol buscas, la altura y la colonia; te respondemos con precio por tamaño.",
               "mensaje": MENSAJE},
    "jsonld": {"migas": pc.migas_ld(NOMBRE, RUTA), "nodos": (pc.lista_ld(NOMBRE, [s for s, _t, _a in ESPECIES]),),
               "speakable": (".vt-portada .vt-lede", ".vt-faq details:first-child p")},
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION),
    "jsonld": {
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "Árboles ornamentales tampico — Todo lo que necesitas saber": (
            "Árboles ornamentales en Tampico: lo que más nos preguntan"),
    },
    "retirados": {
        "$350": "Crespón desde $350: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
        "$350,": "Crespón desde $350 (con coma en el texto): precio sin confirmar por el dueño (pregunta 1).",
        "$450": "Jacaranda desde $450: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
        "$250,": "Era «$250,» dentro de una lista de precios sin confirmar; $250 sigue como «Flamboyán desde $250».",
        "$600": "Olivo negro desde $600: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
    },
    "especies": {
        "reemplazos": {},
        "retirados": {},
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Lema nuevo: «De sombra y de flor, para el clima de Tamaulipas.» (de la entrada); la garantía de 30 días va en la línea de confianza, con sus condiciones.')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: filas de WhatsApp («Cotizar mis árboles») tras el filtro por necesidad, las subcategorías, las especies (la rejilla larga se parte con una en medio), los precios y las preguntas, con la prueba social (cifras de datos.py y la calificación de Google con su enlace) y la garantía de las plantas que sembramos junto a la primera. Encabezados, precios y enlaces sin cambios.'
