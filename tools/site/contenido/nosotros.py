"""Contenido de /nosotros (SEO fase 2a, 2026-11-11; mapa de palabras clave §3a, fila 4): la página de entidad de la
marca. Solo datos: la plantilla es tools/site/plantillas/pilar.py.

Todo de datos.py: fundación (datos.FUNDACION), cifras, REPSE con su padrón, clientes con permiso, el domicilio único del
sitio (datos.CALLE…; el mismo del nodo #negocio), el horario y los perfiles oficiales (entidad.same_as, los mismos del
JSON-LD). Sin nombres de equipo ni historia inventada; la foto es una que el sitio ya publica del vivero, con su alt de
siempre. El JSON-LD es un AboutPage que nombra el negocio por @id (#negocio): no se repite el nodo completo, que vive en
la home y en /vivero-tampico. Página nueva: sin captura de paridad.
"""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from contenido import respuestas

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/nosotros"
URL = f"{SITE}{RUTA}"
MENSAJE = mensajes_paginas.SEO_F2A[RUTA]
FUNDACION = f"{int(datos.FUNDACION[8:])} de {entidad.mes_largo(datos.FUNDACION)}"
PORTADAS = "/img/portadas"

TITULO = f"Nosotros: Vivero y Jardinería desde {datos.DESDE} | {datos.NOMBRE}"
DESCRIPCION = (f"{datos.NOMBRE}: vivero y empresa de jardinería en Cd. Madero desde {datos.DESDE}. {datos.CLIENTES} "
               f"clientes, REPSE {datos.REPSE}, domicilio, horario y perfiles oficiales.")
FOTO = {"src": f"{PORTADAS}/arboles-vivero-tampico-mayoreo-sm.webp",
        "srcset": f"{PORTADAS}/arboles-vivero-tampico-mayoreo-sm.webp 560w, {PORTADAS}/arboles-vivero-tampico-mayoreo.webp 960w",
        "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
        # El alt que la foto ya lleva en /arboles-para-banqueta-tampico.
        "alt": "Árboles jóvenes en el vivero listos para sembrar en banqueta",
        "lugar": "Árboles en el vivero", "etapa": "Viveros Terra"}
META = {
    "title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
    "og": (("og:type", "website"), ("og:title", TITULO), ("og:description", DESCRIPCION),
           ("og:image", f"{SITE}{PORTADAS}/arboles-vivero-tampico-mayoreo.webp"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO),
                ("twitter:description", DESCRIPCION)),
}
CIFRAS = (
    ("Fundación", FUNDACION.removesuffix(f" de {datos.DESDE}"), f"De {datos.DESDE}, en {datos.CIUDAD}"),
    ("Clientes", datos.CLIENTES, "Casas y empresas"),
    ("Instalaciones", datos.INSTALACIONES, "De pasto en rollo"),
    ("Instalado", datos.M2_INSTALADOS, "En Tamaulipas y la Huasteca"),
    ("Variedades", datos.VARIEDADES, "Plantas en el vivero"),
    ("Proyectos B2B", datos.PROYECTOS_B2B, f"REPSE {datos.REPSE}"),
)
HACEMOS = (
    {"titulo": '<a href="/pasto-en-rollo-tampico">Pasto en rollo en Tampico</a>',
     "texto": (f"Pasto San Agustín a {dinero(P['pasto_solo_m2'])}/m² solo el pasto (no lleva IVA) y al mayoreo para obra.")},
    {"titulo": '<a href="/pasto-sintetico">Pasto sintético</a>',
     "texto": f"Instalado en Tampico y con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}."},
    {"titulo": "Servicios de jardín",
     "texto": ('<a href="/diseno-jardines-tampico">Diseño</a>, <a href="/mantenimiento-jardines-tampico">mantenimiento'
               '</a>, <a href="/sistema-riego-tampico">riego automático</a> y <a href="/poda-arboles-tampico">poda de '
               'árboles</a>.')},
    {"titulo": '<a href="/plantas-palmas-arboles-tampico">Plantas, palmas y árboles</a>',
     "texto": (f"{datos.VARIEDADES} variedades en el vivero, y tierra negra, tezontle, mármol y piedra bola para "
               "jardín.")},
    {"titulo": '<a href="/empresas">Áreas verdes para empresas</a>',
     "texto": f"Mantenimiento, pasto, palmas y riego con REPSE {datos.REPSE} y factura {datos.FACTURA}."},
)
DONDE = (
    {"titulo": "Domicilio",
     "texto": (f"{datos.DOMICILIO_COMPLETO}. {datos.REFERENCIA}. "
               f'<a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Abrir en Google Maps</a> · '
               '<a href="/vivero-tampico">vivero en Cd. Madero</a>.')},
    {"titulo": "Horario", "texto": f"{datos.HORARIO}. Domingo cerrado."},
    {"titulo": "Contacto",
     "texto": (f'WhatsApp y teléfono <a href="tel:{datos.TELEFONO_TEL}">{datos.TELEFONO_VISIBLE}</a> · correo '
               f'<a href="mailto:{datos.CORREO_FORMULARIOS}">{datos.CORREO_FORMULARIOS}</a>.')},
)
PERFILES = tuple({"titulo": f'<a href="{url}" target="_blank" rel="noopener">{nombre}</a>',
                  "texto": "Perfil oficial de Viveros Terra."} for nombre, url in datos.REDES) + (
    {"titulo": f'<a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Google Maps</a>',
     "texto": f"Ficha del negocio en Google: {datos.GOOGLE}."},)
PREGUNTAS = (
    ("¿Desde cuándo existe Viveros Terra?",
     f"Desde el {FUNDACION}, en {datos.CIUDAD}, Tamaulipas. Desde {datos.SINTETICO_NACIONAL_DESDE} también envía pasto "
     "sintético a todo México."),
    ("¿Dónde está Viveros Terra?",
     f"En {datos.DOMICILIO_COMPLETO}, {datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}. Es el único domicilio del "
     "negocio."),
    ("¿Viveros Terra y Viveros Terra Tampico son la misma empresa?",
     f"Sí. «{datos.NOMBRE_ALTERNO}» es el nombre con que aparece el mismo negocio en algunos perfiles."),
    ("¿Cuál es el horario?", f"{datos.HORARIO}. Domingo cerrado. {datos.PROMESA}."),
    ("¿Trabajan con empresas?",
     f"Sí. Tenemos REPSE {datos.REPSE}, factura {datos.FACTURA} y {datos.PROYECTOS_B2B} proyectos B2B. Ve las "
     '<a href="/empresas">áreas verdes para empresas</a>.'),
    ("¿Cuáles son sus perfiles oficiales?",
     " · ".join(nombre for nombre, _u in datos.REDES) + " y la ficha de Google Maps. Cualquier otro perfil con otro "
     "domicilio está desactualizado."),
)

CONTENIDO = {
    "respuesta": respuestas.de(RUTA),
    "tipo": "nosotros",
    "meta": META,
    "migas": (("Inicio", "/"), ("Nosotros", None)),
    "portada": {
        "kicker": "Nosotros · Cd. Madero, Tamaulipas",
        "pos": "50% 35%",
        "h1": f"Viveros Terra: vivero y jardinería desde {datos.DESDE}",
        "lema": "Del vivero de Madero a tu jardín.",
        "lede": (f"Vivero, pasto en rollo y jardinería en Tampico, Madero y Altamira, y pasto sintético a todo México "
                 f"desde {datos.SINTETICO_NACIONAL_DESDE}."),
        "mensaje": MENSAJE,
        "enlaces": (("Cómo llegar", datos.MAPS_URL, "nosotros:mapas", 'target="_blank" rel="noopener"'),),
        "dato": f"{datos.CLIENTES} clientes desde {datos.DESDE}",
        "foto": FOTO,
    },
    "secciones": (
        {"clase": "datos", "rotulo": "Historia", "id": "vt-h-historia", "ancla": "historia",
         "titulo": f"Desde {datos.DESDE}, en cifras",
         "lede": f"{datos.NOMBRE} se fundó el {FUNDACION} en {datos.CIUDAD}. Esto llevamos hecho desde entonces.",
         "celdas": CIFRAS},
        {"clase": "fichas", "rotulo": "Qué hacemos", "id": "vt-h-hacemos", "ancla": "que-hacemos",
         "titulo": "Lo que hacemos", "lede": "Cada servicio tiene su página con precios y preguntas.", "items": HACEMOS,
         "cta": (MENSAJE, "Cotizar por WhatsApp")},
        {"clase": "clientes", "rotulo": "Clientes", "id": "vt-h-clientes", "ancla": "clientes",
         "titulo": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
         "lede": "Clientes que nos dieron permiso de mostrar su nombre."},
        {"clase": "fichas", "rotulo": "Dónde estamos", "id": "vt-h-donde", "ancla": "donde",
         "titulo": "Un solo domicilio, en Ciudad Madero", "lede": "El mismo en el sitio, en Google y en los perfiles.",
         "items": DONDE},
        {"clase": "fichas", "rotulo": "Perfiles", "id": "vt-h-perfiles", "ancla": "perfiles",
         "titulo": "Perfiles oficiales", "lede": "Solo estos perfiles son de Viveros Terra.", "items": PERFILES},
    ),
    "faq": {"titulo": "Preguntas sobre Viveros Terra", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿En qué te ayudamos?",
        "lede": ("Escríbenos qué necesitas, tu colonia y los metros aproximados, o "
                 '<a href="/vivero-tampico">visita el vivero</a>.'),
        "mensaje": MENSAJE,
    },
    "jsonld": {
        "speakable": entidad.SPEAKABLE,
        "nodos": ({"@type": "AboutPage", "@id": URL, "url": URL, "name": TITULO, "about": dict(entidad.REF),
                   "mainEntity": dict(entidad.REF)},),
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
    "hero": ("Página nueva (SEO fase 2a, 2026-11-11): hero de marca con un solo botón de WhatsApp, el teléfono y «Cómo "
             "llegar» de enlaces, la línea de confianza con los clientes desde 2007 y sin etiqueta de precio; sin captura "
             "anterior que comparar."),
}
