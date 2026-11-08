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

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/arboles-ornamentales-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Árboles ornamentales"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
FLAMBOYAN = f"Flamboyán desde {dinero(P['flamboyan'])}"
TITULO = "Árboles Ornamentales en Tampico — Viveros Terra | 25 Especies"
DESCRIPCION = ("Árboles ornamentales para jardines en Tampico, Madero y Altamira. Flamboyán, Jacaranda, Ficus, Crespón, "
               "Guayacán y más. Entrega a domicilio · 833 326 8008.")
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
     "garantía de arraigo de 30 días con el riego que te indicamos."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Árboles ornamentales para jardines en Tampico",
        "lede": (f"{FLAMBOYAN}. Árboles de sombra y de flor elegidos para el clima de Tamaulipas: te los llevamos y los "
                 "sembramos con garantía de arraigo."),
        "etiqueta": {"codigo": "Árboles", "aviso": f"Precios {datos.ANIO}", "nombre": "Flamboyán",
                     "cientifico": "Delonix regia", "antes": "desde", "monto": dinero(P["flamboyan"]), "unidad": "",
                     "nota": "Los demás árboles, según especie y tamaño."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="/catalogo?cat=arboles" data-cta="plantas:catalogo">ve los 25 árboles del catálogo</a>.',
        "foto": {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/arboles-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Equipo de Viveros Terra sembrando un árbol ornamental en Tampico",
                 "lugar": "Siembra de un árbol ornamental", "etapa": "Tampico"},
        "compacta": True,
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
               "speakable": ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq details:first-child")},
}

PARIDAD = {
    "jsonld": {
        "LocalBusiness": ("Nodo recortado de main; las páginas apuntan a la entidad única #negocio de la home (como 2d); "
                          "el grafo completo es de la Etapa 4."),
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
