"""Tema comercial de cada artículo del blog: a qué landing lleva (con un ancla que nombra el servicio y la ciudad, no
"Ver X": SEO fase 0, 2026-11-10), qué etiqueta de "producto relacionado" lleva (una sola)
y sus 2–3 enlaces contextuales (spec §3.3 y §6.5). Solo datos; los precios salen de datos.PRECIOS y lo que no tiene precio
confirmado va "Según cotización"."""
import datos
from componentes import dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION
# Las anclas de "landing" son el botón del artículo: hasta 30 caracteres, o se sale de la pantalla a 320 px
# (tests/test_blog_navegador.py).
# Encabezado de la etiqueta cuando "Con IVA" no aplica a todos sus renglones (regla del dueño, 2026-11-10): el pasto sin
# instalar, las palmas y los árboles no llevan IVA.
PRECIOS_ANIO = f"Precios {datos.ANIO}"
# Enlazado interno (SEO fase 0, 2026-11-10): las dos páginas que menos enlaces recibían para lo que valen. Los artículos
# de plantas mandan al vivero; los de cuidado del pasto (tema "mantenimiento") y la comparativa con el sintético, al
# pasto en rollo, además de su landing.
VIVERO = ("vivero en Cd. Madero", "/vivero-tampico")
PASTO_EN_ROLLO = ("pasto en rollo en Tampico", "/pasto-en-rollo-tampico")
DE_PASTO = ("cesped-amarillo-tampico-causas-soluciones", "cuando-regar-pasto-san-agustin-tampico",
            "errores-pasto-san-agustin-tampico", "pasto-sintetico-vs-natural-tampico")
CIUDADES = ("cdmx", "guadalajara", "monterrey", "queretaro", "puebla", "merida")
NOMBRES_CIUDAD = {"cdmx": "CDMX", "guadalajara": "Guadalajara", "monterrey": "Monterrey", "queretaro": "Querétaro",
                  "puebla": "Puebla", "merida": "Mérida"}


# Texto del cierre de cada artículo (Entrega B de experiencia): el precio "desde" de su tema y la garantía si aplica,
# todo de datos.py. El pasto sin instalar, las plantas, los árboles y las palmas no llevan IVA.
_PLANTAS_IVA = "Plantas, palmas y árboles no llevan IVA."
_GARANTIA_PLANTAS = f"Garantía de {datos.GARANTIA_PLANTAS[0].lower()}{datos.GARANTIA_PLANTAS[1:]}".replace(
    "(ver condiciones)", '(<a href="/politicas#garantia-plantas">ver condiciones</a>)')
_COTIZA = "El precio depende de la especie y el tamaño: te lo damos por WhatsApp."
LEDE = {
    "pasto-natural": (f"Pasto San Agustín a {dinero(P['pasto_solo_m2'])}/m² solo el pasto (no lleva IVA) y desde "
                      f"{dinero(P['pasto_instalado_m2'])}/m² instalado, con IVA, con garantía de arraigo de {datos.ARRAIGO} si "
                      f"lo instalamos nosotros. {datos.TERRENO_LISTO_CORTO}"),
    "pasto-sintetico": (f"Desde {dinero(P['sintetico_tienda_m2'])}/m² en rollo de 50 m²; el envío se cobra por rollo según "
                        "tu estado."),
    "riego": f"Riego automático instalado de {dinero(P['riego_m2'][0])} a {dinero(P['riego_m2'][1])}/m², según el sistema.",
    "diseno": (f"Plan Esencial de {dinero(P['diseno'])} y Plan Completo de {dinero(P['diseno_completo'])}; el Premium, "
               f"desde {dinero(P['diseno_premium'])}."),
    "mantenimiento": f"Mantenimiento de jardín desde {dinero(P['mantenimiento_mes'])} al mes.",
    "palmas": f"{datos.PALMAS_PRECIO}. {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "palmas-cotizacion": f"{_COTIZA} {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "arboles": f"Flamboyán desde {dinero(P['flamboyan'])} en ejemplar joven. {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "banqueta": f"{_COTIZA} {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "plantas": f"{_COTIZA} {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "interior": f"{_COTIZA} {_PLANTAS_IVA} {_GARANTIA_PLANTAS}",
    "tierra": (f"Costal de tierra negra a {dinero(P['tierra_negra_costal'])} y metro cúbico a {dinero(P['tierra_negra_m3'])}. "
               f"{datos.SIN_MINIMO}"),
    "tezontle": f"Costal de tezontle rojo desde {dinero(P['tezontle_costal'])}. {datos.SIN_MINIMO}",
}


# Auditoría por página del blog (2026-11-20): el botón de WhatsApp dice qué pasa al tocarlo (antes «Cotizar por WhatsApp» y
# «Preguntar por WhatsApp» en los 49) y la línea entre secciones pide lo que sirve para el tema (antes «colonia y los metros»
# también en palmas y plantas). El menú, la barra y el pie siguen con «Cotizar por WhatsApp».
_EXISTENCIA = ("Preguntar existencia y precio",
               "¿No sabes qué tamaño te conviene? Dinos dónde la vas a poner y te mandamos fotos y precio:")
_FOTOS = ("Mandar fotos por WhatsApp", "¿Tu jardín ya tiene el problema? Mándanos fotos y te decimos qué hacer:")
_MEDIDAS = ("Mandar medidas y fotos", "¿Ya tienes los metros? Mándanos medidas y fotos y te damos un precio:")
_PEDIDO = ("Calcular mi pedido por WhatsApp", "¿No sabes cuánto pedir? Dinos los metros y te calculamos costales o camión:")
WA = {
    "pasto-natural": ("Pedir mi precio por WhatsApp", "¿Ya tienes los metros? Te damos el precio de tu pasto, solo o instalado:"),
    "pasto-sintetico": ("Pedir precio con envío", "¿Ya tienes los metros? Te damos el precio con envío a tu ciudad:"),
    "riego": _MEDIDAS, "diseno": _MEDIDAS, "mantenimiento": _FOTOS,
    "palmas": _EXISTENCIA, "palmas-cotizacion": _EXISTENCIA, "arboles": _EXISTENCIA, "banqueta": _EXISTENCIA,
    "plantas": _EXISTENCIA, "interior": _EXISTENCIA, "tierra": _PEDIDO, "tezontle": _PEDIDO,
}


def _desde(monto, antes="Desde", unidad=""):
    return {"antes": antes, "monto": monto, "unidad": unidad}


CLUSTERS = {
    "pasto-natural": {
        "landing": ("/pasto-en-rollo-tampico", "Pasto en rollo en Tampico"),
        "titulo": "¿Vas a poner pasto nuevo?",
        # Como en la home: "con IVA" solo en el renglón del instalado; el pasto solo no lleva IVA (test_iva_pasto.py).
        "etiqueta": {"nombre": "Pasto San Agustín en rollo", "cientifico": "Stenotaphrum secundatum", "antes": "Instalado · desde",
                     "aviso": PRECIOS_ANIO, "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m² con IVA",
                     "cond": datos.TERRENO_LISTO_CORTO,  # decisión del dueño (2026-11-10)
                     "filas": (("Solo el pasto", f"{dinero(P['pasto_solo_m2'])} /m²"),)},
        # SEO fase 2c (mapa §2 G10): los artículos de pasto natural enlazan el servicio con «pasto San Agustín instalado».
        "enlaces": (("pasto San Agustín instalado", "/pasto-en-rollo-tampico"),
                    ("protocolo de riego de 20 días", "/protocolo-cuidados-pasto-san-agustin"),
                    ("lista de precios", "/precios")),
    },
    "pasto-sintetico": {
        "landing": ("/pasto-sintetico", "Pasto sintético: los 9 modelos"),
        "titulo": "¿Ya sabes qué modelo te conviene?",
        "etiqueta": {"nombre": "Pasto sintético en rollo", "antes": "Rollo de 50 m² · desde", "monto": dinero(P["sintetico_tienda_m2"]),
                     "unidad": "/m²", "filas": (("Envío", "por rollo, según estado"),)},
        "enlaces": (("tienda de pasto sintético", "/pasto-sintetico"),
                    ("pasto sintético instalado en Tampico", "/pasto-sintetico-tampico")),
    },
    "riego": {
        "landing": ("/sistema-riego-tampico", "Sistema de riego en Tampico"),
        "titulo": "¿Quieres que tu jardín se riegue solo?",
        "etiqueta": {"nombre": "Sistema de riego automático", "antes": "Instalado", "monto": f"{dinero(P['riego_m2'][0])}–{dinero(P['riego_m2'][1])}",
                     "unidad": "/m²"},
        "enlaces": (("sistema de riego en Tampico", "/sistema-riego-tampico"), ("mantenimiento de jardines", "/mantenimiento-jardines-tampico"),
                    ("lista de precios", "/precios")),
    },
    "diseno": {
        "landing": ("/diseno-jardines-tampico", "Diseño de jardines en Tampico"),
        "titulo": "¿Quieres un plan para tu jardín?",
        "etiqueta": {"nombre": "Diseño de jardín", "antes": "Plan Esencial · desde", "monto": dinero(P["diseno"]), "unidad": ""},
        "enlaces": (("diseño de jardines en Tampico", "/diseno-jardines-tampico"), ("lista de precios", "/precios"),
                    ("plantas para jardín", "/plantas-para-jardin-tampico")),
    },
    "mantenimiento": {
        "landing": ("/mantenimiento-jardines-tampico", "Mantenimiento de jardines"),
        "titulo": "¿Prefieres que lo hagamos nosotros?",
        "etiqueta": {"nombre": "Mantenimiento de jardines", "antes": "Desde", "monto": dinero(P["mantenimiento_mes"]), "unidad": "/mes"},
        "enlaces": (("mantenimiento de jardines en Tampico", "/mantenimiento-jardines-tampico"), ("lista de precios", "/precios"),
                    ("jardinería en Ciudad Madero", "/jardineria-ciudad-madero")),
    },
    "palmas": {
        "landing": ("/palmas-tropicales-tampico", "Venta de palmas en Tampico"),
        "titulo": "¿Ya elegiste tu palma?",
        "etiqueta": {"nombre": "Palmas tropicales", "antes": "Tamaño chico · desde", "monto": dinero(P["palma_desde"]), "unidad": "",
                     "aviso": PRECIOS_ANIO,
                     "filas": (("Palma real", f"desde {dinero(P['palma_real'])}"),)},
        "enlaces": (("palmas tropicales en Tampico", "/palmas-tropicales-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("palmas para proyectos", "/palmas-mayoreo-proyectos")),
    },
    "palmas-cotizacion": {
        "landing": ("/palmas-tropicales-tampico", "Venta de palmas en Tampico"),
        "titulo": "¿Ya elegiste tu palma?",
        "etiqueta": {"nombre": "Palmas tropicales", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("palmas tropicales en Tampico", "/palmas-tropicales-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("palmas para proyectos", "/palmas-mayoreo-proyectos")),
    },
    "arboles": {
        "landing": ("/arboles-ornamentales-tampico", "Árboles ornamentales"),
        "titulo": "¿Buscas un árbol para tu jardín?",
        "etiqueta": {"nombre": "Flamboyán", "cientifico": "Delonix regia", "antes": "Ejemplar joven · desde", "monto": dinero(P["flamboyan"]), "unidad": "",
                     "aviso": PRECIOS_ANIO},
        "enlaces": (("árboles ornamentales en Tampico", "/arboles-ornamentales-tampico"), ("árboles para banqueta", "/arboles-para-banqueta-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "banqueta": {
        "landing": ("/arboles-para-banqueta-tampico", "Árboles para banqueta"),
        "titulo": "¿Buscas un árbol para tu banqueta?",
        "etiqueta": {"nombre": "Árboles para banqueta", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("árboles para banqueta en Tampico", "/arboles-para-banqueta-tampico"), ("árboles ornamentales", "/arboles-ornamentales-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "plantas": {
        "landing": ("/plantas-para-jardin-tampico", "Plantas para jardín en Tampico"),
        "titulo": "¿Armamos tu lista de plantas?",
        "etiqueta": {"nombre": "Plantas para jardín", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas para jardín en Tampico", "/plantas-para-jardin-tampico"), ("catálogo del vivero", "/catalogo"),
                    VIVERO),
    },
    "interior": {
        "landing": ("/plantas-de-interior-tampico", "Plantas de interior en Tampico"),
        "titulo": "¿Buscas plantas para adentro?",
        "etiqueta": {"nombre": "Plantas de interior", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas de interior en Tampico", "/plantas-de-interior-tampico"), ("catálogo del vivero", "/catalogo"),
                    VIVERO),
    },
    "tierra": {
        "landing": ("/tierra-negra-vegetal-tampico", "Tierra negra en Tampico"),
        "titulo": "¿Cuánta tierra necesitas?",
        "etiqueta": {"nombre": "Tierra negra vegetal", "antes": "Costal", "monto": dinero(P["tierra_negra_costal"]), "unidad": "",
                     "filas": (("Metro cúbico", dinero(P["tierra_negra_m3"])),)},
        "enlaces": (("tierra negra en Tampico", "/tierra-negra-vegetal-tampico"), ("tezontle rojo", "/tezontle-rojo-tampico"), ("lista de precios", "/precios")),
    },
    "tezontle": {
        "landing": ("/tezontle-rojo-tampico", "Tezontle rojo en Tampico"),
        "titulo": "¿Cuánto tezontle necesitas?",
        "etiqueta": {"nombre": "Tezontle rojo", "antes": "Costal · desde", "monto": dinero(P["tezontle_costal"]), "unidad": ""},
        "enlaces": (("tezontle rojo en Tampico", "/tezontle-rojo-tampico"), ("tierra negra", "/tierra-negra-vegetal-tampico"), ("lista de precios", "/precios")),
    },
}

# SEO fase 2c: el artículo de perros se fusionó con /pasto-sintetico/perros (301); los demás conservan su ciudad de envío.
_SINTETICOS = ("como-instalar-pasto-sintetico", "cuanto-cuesta-pasto-sintetico-mexico", "pasto-sintetico-calor-mexico",
               None, "pasto-sintetico-vs-natural-tampico", "que-altura-de-pasto-sintetico-elegir")
POR_SLUG = (
    ("pasto-sintetico", tuple(s for s in _SINTETICOS if s)),
    ("pasto-natural", ("cuando-plantar-pasto-tampico-calendario", "pasto-san-agustin-instalacion-mantenimiento",
                       "pasto-san-agustin-vs-japones")),
    ("riego", ("como-ahorrar-agua-jardin-tampico", "sistema-riego-automatizado-tampico")),
    ("diseno", ("cuanto-cuesta-jardin-tampico-precios", "diseno-jardines-tampico-guia", "jardin-vertical-tampico-guia")),
    ("mantenimiento", ("acolchado-mulch-jardin-tampico", "cesped-amarillo-tampico-causas-soluciones", "como-evitar-encharcamientos-jardin-tampico",
                       "cuando-regar-pasto-san-agustin-tampico", "errores-pasto-san-agustin-tampico",
                       "fertilizacion-jardines-tampico-temporada-lluvias", "hongos-plantas-exceso-humedad-tampico",
                       "jardines-temporada-lluvias-tampico", "nortes-tampico-proteger-plantas-jardin",
                       "plagas-comunes-jardin-tampico", "poda-arboles-palmas-tampico-guia",
                       "temporada-huracanes-proteger-jardin-tampico")),
    ("palmas", ("como-plantar-palma-arbol-paso-a-paso-tampico", "palma-areca-tampico", "palma-coco-plumoso-tampico",
                "palma-real-roystonea-regia-tampico", "palmas-para-jardin-tampico")),
    ("palmas-cotizacion", ("cuidados-palma-del-viajero-ravenala", "palma-bismarckia-bismarckia-nobilis-tampico",
                           "palma-cola-de-zorro-wodyetia-bifurcata-tampico", "palma-kerpis-howea-forsteriana-tampico", "palma-bambu-chamaedorea-tampico",
                           "palma-triangular-dypsis-decaryi-tampico", "palma-washingtona-tampico")),
    ("arboles", ("framboyan-delonix-regia-tampico",)),
    ("banqueta", ("arboles-para-sembrar-en-banqueta",)),
    ("plantas", ("buganvilia-tampico-cuidados-floracion", "como-medir-plantas-altura-cepellon", "duranta-erecta-tampico-cuidados-seto",
                 "jardin-en-macetas-terraza-tampico-guia", "plantas-resistentes-sal-golfo-tampico",
                 "plantas-seguras-mascotas-jardin-tampico")),
    ("interior", ("ficus-elastica-cuidados-tampico", "plantas-interior-tampico")),
    ("tierra", ("tierra-negra-costal-camion-tampico",)),
    ("tezontle", ("tezontle-usos-jardin-tampico",)),
)
TEMA = {slug: tema for tema, slugs in POR_SLUG for slug in slugs}
# Los blogs de precios enlazan a /precios como fuente única (spec §3.5).
A_PRECIOS = ("cuanto-cuesta-jardin-tampico-precios", "cuanto-cuesta-pasto-sintetico-mexico")
# La comparativa con pasto natural es de instalación en Tampico, no de compra en línea.
LANDING = {"pasto-sintetico-vs-natural-tampico": ("/pasto-sintetico-tampico", "Pasto sintético en Tampico"),
           # SEO fase 2a (2026-11-11): la guía de poda y la de huracanes (poda preventiva) llevan a la página de poda.
           "poda-arboles-palmas-tampico-guia": ("/poda-arboles-tampico", "Poda de árboles en Tampico"),
           "temporada-huracanes-proteger-jardin-tampico": ("/poda-arboles-tampico", "Poda de árboles en Tampico")}
# Los mismos dos artículos abren sus enlaces finales con la página de poda (mapa §4b, clúster de clima).
A_PODA = ("poda-arboles-palmas-tampico-guia", "temporada-huracanes-proteger-jardin-tampico")
PODA = ("poda de árboles en Tampico", "/poda-arboles-tampico")


# Entrega D del SEO nacional (2026-11-16): cada artículo de sintético enlaza la guía de la tienda de su tema.
GUIA_D = {"como-instalar-pasto-sintetico": ("rollo de 2 m o de 3.66 m", "/pasto-sintetico/ancho-del-rollo"),
          "cuanto-cuesta-pasto-sintetico-mexico": ("cuántos rollos necesitas y envío por estado",
                                                   "/pasto-sintetico/cuantos-rollos"),
          "pasto-sintetico-calor-mexico": ("pasto sintético para alberca", "/pasto-sintetico/alberca"),
          "pasto-sintetico-vs-natural-tampico": ("pasto sintético o natural en todo México", "/pasto-sintetico/vs-natural"),
          "que-altura-de-pasto-sintetico-elegir": ("pasto sintético en azotea: peso por m²", "/pasto-sintetico/azotea")}


def de(slug):
    """Copia del tema del artículo con sus enlaces finales (los de sintético rotan una ciudad con página de envío)."""
    tema = TEMA[slug]
    base = CLUSTERS[tema]
    enlaces = tuple(base["enlaces"])
    if tema == "pasto-sintetico":
        c = CIUDADES[_SINTETICOS.index(slug)]
        enlaces += ((f"envío de pasto sintético a {NOMBRES_CIUDAD[c]}", f"/pasto-sintetico/envio/{c}"),)
    if slug in DE_PASTO:
        enlaces = enlaces[:2] + (PASTO_EN_ROLLO,)
    if slug in A_PODA:
        enlaces = (PODA,) + enlaces[:2]
    if slug in A_PRECIOS and not any(h == "/precios" for _t, h in enlaces):
        enlaces = (("lista de precios vigente", "/precios"),) + enlaces[:2]
    if slug in GUIA_D:  # la guía va en lugar del enlace a Tampico (sigue en el CTA, el menú y el pie): máximo 3
        enlaces = (enlaces[0], GUIA_D[slug]) + enlaces[2:]
    boton, lectura = WA[tema]
    return {**base, "tema": tema, "enlaces": enlaces[:3], "landing": LANDING.get(slug, base["landing"]), "lede": LEDE[tema],
            "boton": boton, "lectura": lectura}


# Auditoría por página del blog (2026-11-20): el mensaje de los botones del artículo (portada, líneas de lectura, media
# lectura y cierre) dice qué quiere el cliente y qué va a mandar (antes «leí su artículo "<título>" y quiero cotizar»).
# El menú, la barra y el pie siguen con el de mensajes_paginas.BLOG.
MENSAJES = {
    "acolchado-mulch-jardin-tampico": "Hola, leí su guía de acolchado (mulch). Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "arboles-para-sembrar-en-banqueta": "Hola, leí la guía de árboles para banqueta. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "buganvilia-tampico-cuidados-floracion": "Hola, leí la guía de la buganvilia. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "cesped-amarillo-tampico-causas-soluciones": "Hola, mi césped se está poniendo amarillo y necesito diagnóstico",
    "como-ahorrar-agua-jardin-tampico": "Hola, leí la guía para ahorrar agua en el jardín y quiero cotizar riego automático; les paso los m² y mi colonia.",
    "como-evitar-encharcamientos-jardin-tampico": "Hola, leí su guía de encharcamientos y drenaje. Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "como-instalar-pasto-sintetico": "Hola, leí la guía para instalar pasto sintético. Quiero precio con envío; les digo metros y ciudad.",
    "como-medir-plantas-altura-cepellon": "Hola, leí la guía para medir plantas. Les paso la planta, la altura y el cepellón que busco para que me den precio.",
    "como-plantar-palma-arbol-paso-a-paso-tampico": "Hola, leí la guía para plantar una palma o árbol y quiero cotizar la plantación; les digo cuál y mi colonia.",
    "cuando-plantar-pasto-tampico-calendario": "Hola, leí el calendario para plantar pasto. Quiero precio del pasto en rollo; les mando metros, colonia y si lo quiero instalado.",
    "cuando-regar-pasto-san-agustin-tampico": "Hola, leí la guía de riego del pasto San Agustín. Les mando fotos de mi pasto para que me digan qué tiene y cuánto cuesta atenderlo.",
    "cuanto-cuesta-jardin-tampico-precios": "Hola, leí la guía de precios de jardines y quiero un precio para el mío; les mando metros, fotos y colonia.",
    "cuanto-cuesta-pasto-sintetico-mexico": "Hola, leí la guía de precios del pasto sintético. Quiero precio con envío; les digo metros y ciudad.",
    "cuidados-palma-del-viajero-ravenala": "Hola, leí la guía de la Palma del Viajero. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "diseno-jardines-tampico-guia": "Hola, leí la guía de diseño de jardines. Me interesa el Plan Terra; les mando fotos y metros de mi jardín.",
    "duranta-erecta-tampico-cuidados-seto": "Hola, leí la guía de la duranta para seto. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "errores-pasto-san-agustin-tampico": "Hola, leí la guía de errores del pasto San Agustín. Les mando fotos de mi pasto para que me digan qué tiene y cuánto cuesta el mantenimiento.",
    "fertilizacion-jardines-tampico-temporada-lluvias": "Hola, leí su guía de fertilización. Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "ficus-elastica-cuidados-tampico": "Hola, leí la guía del Ficus Elastica. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "framboyan-delonix-regia-tampico": "Hola, leí la guía del Flamboyán. Quiero precio y existencia; les digo el tamaño que busco y mi colonia.",
    "hongos-plantas-exceso-humedad-tampico": "Hola, leí su guía de hongos en plantas. Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "jardin-en-macetas-terraza-tampico-guia": "Hola, leí la guía de jardín en macetas y terrazas. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "jardin-vertical-tampico-guia": "Hola, leí la guía de jardín vertical y quiero cotizar el mío; les mando medidas y fotos del muro.",
    "jardines-temporada-lluvias-tampico": "Hola, leí su guía de jardines en temporada de lluvias. Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "nortes-tampico-proteger-plantas-jardin": "Hola, leí su guía de nortes. Les mando fotos de mi jardín para que me digan qué tiene y cuánto cuesta atenderlo.",
    "palma-areca-tampico": "Hola, leí la guía de la Palma Areca. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-bambu-chamaedorea-tampico": "Hola, leí la guía de la Palma Bambú. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-bismarckia-bismarckia-nobilis-tampico": "Hola, leí la guía de la Palma Bismarckia. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-coco-plumoso-tampico": "Hola, leí la guía de la Palma Coco Plumoso. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-cola-de-zorro-wodyetia-bifurcata-tampico": "Hola, leí la guía de la Palma Cola de Zorro. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-kerpis-howea-forsteriana-tampico": "Hola, leí la guía de la Palma Kerpis. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-real-roystonea-regia-tampico": "Hola, leí la guía de la Palma Real. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-triangular-dypsis-decaryi-tampico": "Hola, leí la guía de la Palma Triangular. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palma-washingtona-tampico": "Hola, leí la guía de la Palma Washingtona. Quiero precio y existencia; les digo la altura que busco y mi colonia.",
    "palmas-para-jardin-tampico": "Hola, leí la guía de 8 palmas para jardín. Quiero precio y existencia; les digo cuál, la altura y mi colonia.",
    "pasto-san-agustin-instalacion-mantenimiento": "Hola, leí la guía para instalar pasto San Agustín. Quiero precio del pasto en rollo; les mando metros, colonia y si lo quiero instalado.",
    "pasto-san-agustin-vs-japones": "Hola, leí la comparativa de pasto San Agustín y japonés. Quiero precio del pasto en rollo; les mando metros, colonia y si lo quiero instalado.",
    "pasto-sintetico-calor-mexico": "Hola, leí la guía del pasto sintético en el calor. Quiero precio con envío; les digo metros y ciudad.",
    "pasto-sintetico-vs-natural-tampico": "Hola, leí la comparativa de pasto sintético y natural. Quiero precio instalado en mi casa; les digo metros y colonia.",
    "plagas-comunes-jardin-tampico": "Hola, leí su guía de plagas del jardín. Les mando fotos de mis plantas para que me digan qué tienen y cuánto cuesta atenderlas.",
    "plantas-interior-tampico": "Hola, leí la guía de plantas de interior. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "plantas-resistentes-sal-golfo-tampico": "Hola, leí la guía de plantas resistentes a la sal. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "plantas-seguras-mascotas-jardin-tampico": "Hola, leí la guía de plantas seguras para mascotas. Quiero precio y existencia; les digo tamaño, cuántas y mi colonia.",
    "poda-arboles-palmas-tampico-guia": "Hola, leí su guía de poda y quiero cotizar la poda de mis árboles o palmas; les mando fotos y ubicación.",
    "que-altura-de-pasto-sintetico-elegir": "Hola, leí la guía de alturas de pasto sintético. Quiero que me recomienden modelo y precio; les digo metros, ciudad y para qué lo uso.",
    "sistema-riego-automatizado-tampico": "Hola, leí la guía de riego automático y quiero cotizar el riego de mi jardín; les paso los m² y mi colonia.",
    "temporada-huracanes-proteger-jardin-tampico": "Hola, leí su guía de huracanes y quiero cotizar una poda preventiva; les mando fotos y ubicación.",
    "tezontle-usos-jardin-tampico": "Hola, leí la guía del tezontle. Quiero precio por costal; les digo cuántos y mi colonia.",
    "tierra-negra-costal-camion-tampico": "Hola, leí la guía de tierra negra y quiero saber si me conviene costal o camión; les paso metros y colonia.",
}
