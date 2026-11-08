"""Contenido de /catalogo ("Arma tu lista"). Plantilla: plantillas/catalogo.py; especies: contenido/catalogo_datos.py.

Se retiran de main: la cabecera con "Productor directo", "Actualizado con disponibilidad real del vivero" y las cifras
sin respaldo ("+500 proyectos", "3 estados", "18 años"); la pestaña "Pasto & Tierra" (sus "+200,000 m²" contradicen
datos.M2_INSTALADOS; el pasto y los materiales tienen sus páginas, enlazadas abajo); las colecciones (una segunda
rejilla), el orden "Más vendidas" y la insignia "+ Vendido" (sin dato; pregunta 7); "Cotizar ahora" y "Medida especial"
por tarjeta (un solo mensaje: la medida especial vive en el diálogo de la lista). Las 117
especies llevan la foto de main (decisión del dueño, 2026-11-08), en local. Título y descripción
como estaban: el título dice "con precio" y se reescribe en la Etapa 3 (spec §3.5). La descripción de Open Graph pierde
«disponibles» (PARIDAD["meta"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import plantas_comun as pc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/catalogo"
URL = f"{SITE}{RUTA}"
OG_DESCRIPCION = ("Más de 200 variedades de plantas, palmas y árboles con cotizador integrado, además de pasto y "
                  "materiales para jardines en Tampico, Madero y Altamira.")
TITULO = "Catálogo de plantas con precio en Tampico: arma tu lista y cotiza · Viveros Terra"
IMAGEN = f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"
META = {
    "title": TITULO,
    "description": ("Más de 200 variedades de plantas, palmas, árboles y pasto en Tampico. Cotizador, filtros por categoría "
                    "y entrega a domicilio. Viveros Terra."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (("og:type", "website"), ("og:url", URL), ("og:title", TITULO),
           ("og:description", OG_DESCRIPCION),
           ("og:image", IMAGEN), ("og:image:width", "1200"), ("og:image:height", "630"),
           ("og:site_name", "Viveros Terra"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO), ("twitter:image", IMAGEN)),
}
MENSAJE = mensajes_paginas.RUTAS[RUTA][0]

CONTENIDO = {
    "tipo": "catalogo",
    "meta": META,
    "migas": (("Inicio", "/"), ("Plantas y palmas", pc.HUB), ("Arma tu lista", None)),
    "cabeza": {
        "h1": "Catálogo de Plantas, Palmas y Árboles en Tampico",
        "lede": ("Especies del vivero con luz, riego y altura. Busca o filtra, añade a tu lista con tamaño y piezas, y "
                 "mándala completa en un solo mensaje de WhatsApp."),
        "precios": (f"{datos.PALMAS_PRECIO}. Flamboyán desde {dinero(P['flamboyan'])}. Las demás especies, según "
                    "cotización por tamaño."),
        "mensaje": MENSAJE,
    },
    "rejilla": {"titulo": "Especies del vivero"},
    "pedido": {"titulo": "¿No encontraste lo que buscas?",
               "lede": "Dinos qué planta, árbol, tamaño o medida necesitas y te cotizamos."},
    "relacionados": {"titulo": "¿Buscas pasto o material?", "items": (
        {"titulo": "Pasto en rollo", "href": "/pasto-en-rollo-tampico",
         "texto": f"San Agustín desde {dinero(P['pasto_solo_m2'])}/m².",
         "img": "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp", "ancho": 560, "alto": 840},
        {"titulo": "Pasto sintético", "href": "/pasto-sintetico",
         "texto": f"Envío a todo México desde {dinero(P['sintetico_tienda_m2'])}/m².",
         "img": "/img/pasto-sintetico-proyecto-01.webp", "ancho": 900, "alto": 756},
        {"titulo": "Tierra negra", "href": "/tierra-negra-vegetal-tampico",
         "texto": f"Costal {dinero(P['tierra_negra_costal'])} · m³ {dinero(P['tierra_negra_m3'])}.",
         "img": "/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp", "ancho": 560, "alto": 373})},
    "jsonld": {"nombre": "Catálogo Viveros Terra Tampico",
               "descripcion": "Especies de plantas, palmas y árboles del vivero de Viveros Terra en Tampico, Tamaulipas",
               "url": URL, "migas": pc.migas_ld("Arma tu lista", RUTA)},
}

PARIDAD = {
    "meta": {"og:description": (OG_DESCRIPCION, "Decía «Más de 200 variedades disponibles»: afirmación de existencias "
                                                "sin verificar (el dueño no confirma disponibilidad en línea).")},
    "reemplazos": {
        "Pasto en Rollo Natural": "Pasto en rollo",
        "Materiales & Tierra": "Tierra negra",
        "¿Necesitas pasto o material especial?": "¿Buscas pasto o material?",
    },
    "retirados": {
        "${p.name}": "Era la plantilla del JS de main dentro de un <h3>; ahora cada especie es un <h3> real en el HTML.",
    },
    # El Floripondio duplicado no necesita entrada: la especie sigue (una vez) y la paridad la encuentra.
    "especies": {"reemplazos": {}, "retirados": {}},
}
