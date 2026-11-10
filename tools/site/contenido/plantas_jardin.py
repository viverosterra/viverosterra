"""Contenido de /plantas-para-jardin-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Las seis especies de main, en su orden y con la foto del catálogo (decisión del dueño, 2026-11-08: las fotos quedan
como están), servida en local. Sin precio propio (datos.DESDE_PLANTAS: según
cotización): se retira el "equipar un jardín desde $3,000–$8,000" (estimado sin confirmar por el dueño) y la "cotización
sin costo"; el diseño tiene su precio oficial en /diseno-jardines-tampico. "Todas disponibles" sale (sin afirmaciones de
disponibilidad). Título ("+74 Variedades"), descripción y Open Graph como estaban (Etapa 3).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/plantas-para-jardin-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Plantas para jardín"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
TITULO = "Plantas para Jardín en Tampico: Sol y Sombra | Viveros Terra"
DESCRIPCION = ("Plantas de exterior que aguantan el calor de Tampico: ave del paraíso, bugambilia, crotos y agaves. Te decimos "
               "cuáles van en sol o sombra. Cotiza tu lista.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("ave-de-paraiso", "Florido elegante: flor naranja y azul que dura semanas.", None),
    ("bugambilea-envarada", "Ya formada en vara; florece casi todo el año con poca agua y aguanta el salitre.", None),
    ("duranta-cubana", "La de los setos rápidos: follaje dorado que se forma con poda.", None),
    ("croto-petra", "Hojas de colores todo el año; aguanta el salitre de Madero.", None),
    ("agave-atenuata", "El agave sin espinas, seguro en jardines familiares: rosetas decorativas que aguantan la sequía "
     "y el calor.", None),
    ("plumbago", "Flores azul cielo casi todo el año; buena para bordes y cercas.", None),
)
PREGUNTAS = (
    ("¿Qué plantas son mejores para jardines en Tampico?",
     "Para jardines en Tampico recomendamos: Ave de Paraíso (florido elegante), Bugambilea (todo el año), Duranta Cubana "
     "(setos rápidos), Crotos (coloridos), Agave Atenuata (bajo mantenimiento) y Plumbago (flores azules). Todas "
     "adaptadas al calor y humedad del Golfo."),
    ("¿Qué plantas de jardín necesitan poco riego en Tampico?",
     "Las plantas de jardín con menor consumo de agua en Tampico son: Agave Atenuata, Bugambilea, Duranta, Cactus "
     "Órgano, Sansiviera y Lápiz Tirucalli. Perfectas para jardines sin sistema de riego automático."),
    ("¿Qué plantas florecen todo el año en Tampico?",
     "Las plantas que florecen casi todo el año en Tampico con pleno sol son: Bugambilea (casi 12 meses), Duranta Zafiro "
     "(flores lila), Ixora Karla (naranja-rojo), Wudelia Rastrera (amarillo) y Petunia Silvestre (morada)."),
    ("¿Tienen plantas para jardines pequeños en Tampico?",
     "Sí, manejamos plantas ideales para jardines pequeños en Tampico: Kalanchoe, Adelfa Enana, Box Arrayán Bola, "
     "Bugambilea Mini, Duranta Zafiro e Ixora. Todas de porte compacto y alto impacto visual."),
    ("¿Cuánto cuesta equipar un jardín en Tampico?",
     "Depende del tamaño del jardín y de las especies: mándanos los metros, si es de sol o de sombra y una foto, y te "
     "cotizamos las plantas por tamaño. Si quieres el proyecto completo, el diseño tiene su precio publicado en "
     f"<a href=\"/diseno-jardines-tampico\">diseño de jardines</a> (desde {dinero(P['diseno'])})."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Plantas para jardín que aguantan el calor de Tampico",
        "lede": ("Ornamentales, tropicales y de cobertura elegidas para sol, humedad y salitre. Te decimos cuáles van en "
                 "sol y cuáles en sombra, te las llevamos y, si quieres, las sembramos."),
        "etiqueta": {"codigo": "Jardín", "aviso": f"Precios {datos.ANIO}", "nombre": "Plantas para jardín",
                     "antes": "Precio", "monto": "Por tamaño", "unidad": datos.SEGUN_COTIZACION.lower(),
                     "nota": "Cotiza con una foto de tu espacio."},
        "mensaje": MENSAJE,
        "tambien": ('O <a href="/catalogo?cat=plantas" data-cta="plantas:catalogo">ve las '
                    f'{cd.cuenta({"cat": ["plantas"]})} plantas del catálogo</a>.'),
        "foto": {"src": "/img/portadas/jardin-residencial-tropical-tampico-sm.webp",
                 "srcset": ("/img/portadas/jardin-residencial-tropical-tampico-sm.webp 560w, "
                            "/img/portadas/jardin-residencial-tropical-tampico.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 640, "numero": 1,
                 "alt": "Jardín residencial con plantas tropicales en Tampico",
                 "lugar": "Jardín con plantas tropicales", "etapa": "Tampico"},
        "compacta": True,
    },
    "especies": {"titulo": "Las más solicitadas en Tampico", "lede": pc.LEDE_FOTOS, "items": ESPECIES},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Plantas para jardín en Tampico: lo que más nos preguntan", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de plantas para jardín", "items": (
        ("Plantas que resisten la sal del Golfo", "/blog/plantas-resistentes-sal-golfo-tampico"),
        ("Bugambilia en Tampico: cuidados y floración", "/blog/buganvilia-tampico-cuidados-floracion"),
        ("Duranta: cuidados y setos", "/blog/duranta-erecta-tampico-cuidados-seto"),
        ("Jardín en macetas para terraza", "/blog/jardin-en-macetas-terraza-tampico-guia"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": pc.otras_subcategorias(RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos si el lugar es de sol o de sombra, los metros y la colonia; te respondemos con precio.",
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
        "Plantas para jardín tampico — Todo lo que necesitas saber": (
            "Plantas para jardín en Tampico: lo que más nos preguntan"),
    },
    "retirados": {
        "$3,000": ("Era «equipar un jardín desde $3,000–$8,000»: estimado sin confirmar por el dueño; el diseño tiene su "
                   "precio oficial en /diseno-jardines-tampico."),
        "$8,000": ("Era «equipar un jardín desde $3,000–$8,000»: estimado sin confirmar por el dueño; las plantas van "
                   "según cotización."),
    },
    "especies": {
        "reemplazos": {},
        "retirados": {},
    },
}
