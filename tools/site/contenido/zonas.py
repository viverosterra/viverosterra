"""Contenido de /zonas (SEO fase 2a, 2026-11-11; mapa de palabras clave §3a, fila 5, y §4a): índice de cobertura que
enlaza las 6 páginas de zona con el ancla «Jardinería en <zona>» y resume Tampico, Ciudad Madero y Altamira. Solo
datos: la plantilla es tools/site/plantillas/pilar.py.

Las zonas, sus nombres, entradas y fotos salen de contenido/zona.py y datos.ZONAS (las mismas de cada página de zona);
los precios, de datos.PRECIOS. Sin distancias, tiempos de llegada ni colonias nuevas. Página nueva: sin captura de
paridad.
"""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from contenido import respuestas
from contenido import zona

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/zonas"
URL = f"{SITE}{RUTA}"
MENSAJE = mensajes_paginas.SEO_F2A[RUTA]
PORTADAS = "/img/portadas"


def ancla(slug):
    """«Jardinería en <zona>», con el nombre que usa la propia página de la zona."""
    return f"Jardinería en {zona.ZONAS[slug]['nombre']}"


def _tarjeta(ruta):
    slug = ruta.strip("/")
    foto = zona._foto(slug)
    return {"titulo": ancla(slug), "href": ruta, "img": foto["src"], "ancho": 560,
            "alto": round(560 * foto["alto"] / foto["ancho"]), "texto": zona.ZONAS[slug]["lede"]}


TARJETAS = tuple(_tarjeta(ruta) for _nombre, ruta in datos.ZONAS)
TAMPICO = tuple(r for _n, r in datos.ZONAS if zona.ZONAS[r.strip("/")]["municipio"] == "Tampico")


def _lista(rutas):
    enlaces = [f'<a href="{r}">{ancla(r.strip("/"))}</a>' for r in rutas]
    return ", ".join(enlaces[:-1]) + " y " + enlaces[-1] if len(enlaces) > 1 else enlaces[0]


CIUDADES = (
    {"titulo": "Tampico", "texto": f"Cuatro zonas con página propia: {_lista(TAMPICO)}."},
    {"titulo": "Ciudad Madero",
     "texto": (f"Aquí está el vivero, en {datos.CALLE}, frente a Walmart: "
               f'<a href="/jardineria-ciudad-madero">{ancla("jardineria-ciudad-madero")}</a> y '
               '<a href="/vivero-tampico">vivero en Cd. Madero</a>.')},
    {"titulo": "Altamira",
     "texto": (f'Casas y fraccionamientos en <a href="/jardineria-altamira">{ancla("jardineria-altamira")}</a>; '
               'para empresas del puerto industrial, <a href="/empresas">áreas verdes para empresas</a>.')},
    {"titulo": "Por proyecto", "texto": f"{datos.ZONAS_POR_PROYECTO}: te cotizamos según el proyecto."},
)
SERVICIOS = (
    {"titulo": '<a href="/pasto-en-rollo-tampico">Pasto en rollo</a>',
     "texto": (f"San Agustín desde {dinero(P['pasto_instalado_m2'])}/m² instalado. {datos.TERRENO_LISTO_CORTO}")},
    {"titulo": '<a href="/diseno-jardines-tampico">Diseño de jardines</a>',
     "texto": f"Plan Terra desde {dinero(P['diseno'])}."},
    {"titulo": '<a href="/mantenimiento-jardines-tampico">Mantenimiento</a>',
     "texto": f"Desde {dinero(P['mantenimiento_mes'])} al mes."},
    {"titulo": '<a href="/sistema-riego-tampico">Riego automático</a>',
     "texto": f"De {dinero(P['riego_m2'][0])} a {dinero(P['riego_m2'][1])}/m²."},
    {"titulo": '<a href="/poda-arboles-tampico">Poda de árboles</a>',
     "texto": f"Desde {dinero(P['poda'])}, según cotización; también derribo."},
)

TITULO = f"Zonas de Servicio de Jardinería en Tampico | {datos.NOMBRE}"
DESCRIPCION = ("Jardinería en Lomas de Rosales, Club Campestre, Águila, Lomas del Chairel, Ciudad Madero y Altamira: "
               "pasto, diseño, riego, poda y mantenimiento.")
FOTO = zona._foto("jardineria-ciudad-madero")
META = {
    "title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
    "og": (("og:type", "website"), ("og:title", TITULO), ("og:description", DESCRIPCION),
           ("og:image", f"{SITE}{PORTADAS}/diseno-jardines-madero-altamira-pasto.webp"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO),
                ("twitter:description", DESCRIPCION)),
}
PREGUNTAS = (
    ("¿En qué zonas dan servicio de jardinería?",
     "En Tampico, Ciudad Madero y Altamira. Seis zonas tienen página propia con precios, colonias y preguntas: "
     + ", ".join(nombre for nombre, _r in datos.ZONAS[:-1]) + f" y {datos.ZONAS[-1][0]}."),
    ("Mi colonia no aparece, ¿me atienden?",
     "Si tu colonia está en Tampico, Madero o Altamira, sí. Mándanos la colonia, el servicio y los metros aproximados "
     "por WhatsApp."),
    ("¿Trabajan fuera de Tampico, Madero y Altamira?", f"Sí, por proyecto: {datos.ZONAS_POR_PROYECTO}."),
    ("¿Cuánto cuesta la visita para cotizar?", datos.VISITA_COSTO),
    ("¿Dónde está el vivero?",
     f"En {datos.DOMICILIO_COMPLETO}, {datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}. {datos.HORARIO}."),
)

CONTENIDO = {
    "respuesta": respuestas.de(RUTA),
    "tipo": "zonas",
    "meta": META,
    "migas": (("Inicio", "/"), ("Zonas de servicio", None)),
    "portada": {
        "kicker": "Cobertura · Tampico, Madero y Altamira",
        **zona.ENCUADRES["jardineria-ciudad-madero"],
        "h1": "Zonas de servicio de jardinería",
        "lema": "Busca tu colonia y cotiza por WhatsApp.",
        "lede": "Pasto, diseño, riego, poda y mantenimiento en la zona conurbada. Elige tu zona para ver precios y colonias.",
        "mensaje": MENSAJE,
        "enlaces": (("Ver las 6 zonas", "#zonas"),),
        "dato": datos.VISITA_COSTO_CORTO,
        "foto": FOTO,
    },
    "secciones": (
        {"clase": "tarjetas", "rotulo": "Zonas", "id": "vt-h-zonas", "ancla": "zonas",
         "titulo": "Seis zonas con página propia",
         "lede": "Cada zona tiene sus precios, las colonias que atendemos y sus preguntas frecuentes.",
         "items": TARJETAS, "cta": (MENSAJE, "Cotizar en mi zona")},
        {"clase": "fichas", "rotulo": "Ciudades", "id": "vt-h-ciudades", "ancla": "ciudades",
         "titulo": "Tampico, Ciudad Madero y Altamira", "lede": "Lo que atendemos en cada ciudad.", "items": CIUDADES},
        {"clase": "fichas", "rotulo": "Servicios", "id": "vt-h-servicios", "ancla": "servicios",
         "titulo": "Servicios en todas las zonas", "lede": "Con el precio de la lista oficial.", "items": SERVICIOS},
    ),
    "faq": {"titulo": "Preguntas sobre las zonas de servicio", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "Cotiza el jardín de tu colonia",
        "lede": ("Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. "
                 f"{datos.VISITA_COSTO}"),
        "mensaje": MENSAJE,
    },
    "jsonld": {
        "speakable": entidad.SPEAKABLE,
        "nodos": ({"@type": "CollectionPage", "@id": URL, "url": URL, "name": TITULO, "mainEntity": {
            "@type": "ItemList", "name": "Zonas de servicio de jardinería", "itemListElement": [
                {"@type": "ListItem", "position": n, "name": t["titulo"], "url": f"{SITE}{t['href']}"}
                for n, t in enumerate(TARJETAS, 1)]}},),
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
    "hero": ("Página nueva (SEO fase 2a, 2026-11-11): hero de marca como las zonas, con un solo botón de WhatsApp, el "
             "teléfono de enlace, el costo de la visita en la línea de confianza y sin etiqueta de precio; sin captura "
             "anterior que comparar."),
}
