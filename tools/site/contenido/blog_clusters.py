"""Tema comercial de cada artículo del blog: a qué landing lleva, qué etiqueta de "producto relacionado" lleva (una sola)
y sus 2–3 enlaces contextuales (spec §3.3 y §6.5). Solo datos; los precios salen de datos.PRECIOS y lo que no tiene precio
confirmado va "Según cotización"."""
import datos
from componentes import dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION
CIUDADES = ("cdmx", "guadalajara", "monterrey", "queretaro", "puebla", "merida")
NOMBRES_CIUDAD = {"cdmx": "CDMX", "guadalajara": "Guadalajara", "monterrey": "Monterrey", "queretaro": "Querétaro",
                  "puebla": "Puebla", "merida": "Mérida"}


def _desde(monto, antes="Desde", unidad=""):
    return {"antes": antes, "monto": monto, "unidad": unidad}


CLUSTERS = {
    "pasto-natural": {
        "landing": ("/pasto-en-rollo-tampico", "Ver pasto en rollo"),
        "titulo": "¿Vas a poner pasto nuevo?",
        "etiqueta": {"nombre": "Pasto San Agustín en rollo", "cientifico": "Stenotaphrum secundatum", "antes": "Instalado · desde",
                     "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m²",
                     "filas": (("Solo el pasto", f"{dinero(P['pasto_solo_m2'])} /m²"),)},
        "enlaces": (("pasto San Agustín en rollo", "/pasto-en-rollo-tampico"),
                    ("protocolo de riego de 20 días", "/protocolo-cuidados-pasto-san-agustin"),
                    ("lista de precios", "/precios")),
    },
    "pasto-sintetico": {
        "landing": ("/pasto-sintetico", "Ver los 9 modelos"),
        "titulo": "¿Ya sabes qué modelo te conviene?",
        "etiqueta": {"nombre": "Pasto sintético en rollo", "antes": "Rollo de 50 m² · desde", "monto": dinero(P["sintetico_tienda_m2"]),
                     "unidad": "/m²", "filas": (("Envío", "por rollo, según estado"),)},
        "enlaces": (("tienda de pasto sintético", "/pasto-sintetico"),
                    ("pasto sintético instalado en Tampico", "/pasto-sintetico-tampico")),
    },
    "riego": {
        "landing": ("/sistema-riego-tampico", "Ver sistema de riego"),
        "titulo": "¿Quieres que tu jardín se riegue solo?",
        "etiqueta": {"nombre": "Sistema de riego automático", "antes": "Instalado", "monto": f"{dinero(P['riego_m2'][0])}–{dinero(P['riego_m2'][1])}",
                     "unidad": "/m²"},
        "enlaces": (("sistema de riego en Tampico", "/sistema-riego-tampico"), ("mantenimiento de jardines", "/mantenimiento-jardines-tampico"),
                    ("lista de precios", "/precios")),
    },
    "diseno": {
        "landing": ("/diseno-jardines-tampico", "Ver diseño de jardines"),
        "titulo": "¿Quieres un plan para tu jardín?",
        "etiqueta": {"nombre": "Diseño de jardín", "antes": "Plan Esencial · desde", "monto": dinero(P["diseno"]), "unidad": ""},
        "enlaces": (("diseño de jardines en Tampico", "/diseno-jardines-tampico"), ("lista de precios", "/precios"),
                    ("plantas para jardín", "/plantas-para-jardin-tampico")),
    },
    "mantenimiento": {
        "landing": ("/mantenimiento-jardines-tampico", "Ver mantenimiento"),
        "titulo": "¿Prefieres que lo hagamos nosotros?",
        "etiqueta": {"nombre": "Mantenimiento de jardines", "antes": "Desde", "monto": dinero(P["mantenimiento_mes"]), "unidad": "/mes"},
        "enlaces": (("mantenimiento de jardines en Tampico", "/mantenimiento-jardines-tampico"), ("lista de precios", "/precios"),
                    ("jardinería en Ciudad Madero", "/jardineria-ciudad-madero")),
    },
    "palmas": {
        "landing": ("/palmas-tropicales-tampico", "Ver palmas"),
        "titulo": "¿Ya elegiste tu palma?",
        "etiqueta": {"nombre": "Palmas tropicales", "antes": "Tamaño chico · desde", "monto": dinero(P["palma_desde"]), "unidad": "",
                     "filas": (("Palma real", f"desde {dinero(P['palma_real'])}"),)},
        "enlaces": (("palmas tropicales en Tampico", "/palmas-tropicales-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("palmas para proyectos", "/palmas-mayoreo-proyectos")),
    },
    "palmas-cotizacion": {
        "landing": ("/palmas-tropicales-tampico", "Ver palmas"),
        "titulo": "¿Ya elegiste tu palma?",
        "etiqueta": {"nombre": "Palmas tropicales", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("palmas tropicales en Tampico", "/palmas-tropicales-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("palmas para proyectos", "/palmas-mayoreo-proyectos")),
    },
    "arboles": {
        "landing": ("/arboles-ornamentales-tampico", "Ver árboles"),
        "titulo": "¿Buscas un árbol para tu jardín?",
        "etiqueta": {"nombre": "Flamboyán", "cientifico": "Delonix regia", "antes": "Ejemplar joven · desde", "monto": dinero(P["flamboyan"]), "unidad": ""},
        "enlaces": (("árboles ornamentales en Tampico", "/arboles-ornamentales-tampico"), ("árboles para banqueta", "/arboles-para-banqueta-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "banqueta": {
        "landing": ("/arboles-para-banqueta-tampico", "Ver árboles para banqueta"),
        "titulo": "¿Buscas un árbol para tu banqueta?",
        "etiqueta": {"nombre": "Árboles para banqueta", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("árboles para banqueta en Tampico", "/arboles-para-banqueta-tampico"), ("árboles ornamentales", "/arboles-ornamentales-tampico"),
                    ("catálogo del vivero", "/catalogo")),
    },
    "plantas": {
        "landing": ("/plantas-para-jardin-tampico", "Ver plantas para jardín"),
        "titulo": "¿Armamos tu lista de plantas?",
        "etiqueta": {"nombre": "Plantas para jardín", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas para jardín en Tampico", "/plantas-para-jardin-tampico"), ("catálogo del vivero", "/catalogo"),
                    ("diseño de jardines", "/diseno-jardines-tampico")),
    },
    "interior": {
        "landing": ("/plantas-de-interior-tampico", "Ver plantas de interior"),
        "titulo": "¿Buscas plantas para adentro?",
        "etiqueta": {"nombre": "Plantas de interior", "antes": "Precio", "monto": SEGUN, "unidad": ""},
        "enlaces": (("plantas de interior en Tampico", "/plantas-de-interior-tampico"), ("catálogo del vivero", "/catalogo")),
    },
    "tierra": {
        "landing": ("/tierra-negra-vegetal-tampico", "Ver tierra negra"),
        "titulo": "¿Cuánta tierra necesitas?",
        "etiqueta": {"nombre": "Tierra negra vegetal", "antes": "Costal", "monto": dinero(P["tierra_negra_costal"]), "unidad": "",
                     "filas": (("Metro cúbico", dinero(P["tierra_negra_m3"])),)},
        "enlaces": (("tierra negra en Tampico", "/tierra-negra-vegetal-tampico"), ("tezontle rojo", "/tezontle-rojo-tampico"), ("lista de precios", "/precios")),
    },
    "tezontle": {
        "landing": ("/tezontle-rojo-tampico", "Ver tezontle"),
        "titulo": "¿Cuánto tezontle necesitas?",
        "etiqueta": {"nombre": "Tezontle rojo", "antes": "Costal · desde", "monto": dinero(P["tezontle_costal"]), "unidad": ""},
        "enlaces": (("tezontle rojo en Tampico", "/tezontle-rojo-tampico"), ("tierra negra", "/tierra-negra-vegetal-tampico"), ("lista de precios", "/precios")),
    },
}

_SINTETICOS = ("como-instalar-pasto-sintetico", "cuanto-cuesta-pasto-sintetico-mexico", "pasto-sintetico-calor-mexico",
               "pasto-sintetico-para-perros", "pasto-sintetico-vs-natural-tampico", "que-altura-de-pasto-sintetico-elegir")
POR_SLUG = (
    ("pasto-sintetico", _SINTETICOS),
    ("pasto-natural", ("cuando-plantar-pasto-tampico-calendario", "pasto-san-agustin-instalacion-mantenimiento",
                       "pasto-san-agustin-vs-japones")),
    ("riego", ("como-ahorrar-agua-jardin-tampico", "riego-automatico-tampico-roi", "sistema-riego-automatico-conviene-tampico",
               "sistema-riego-automatizado-tampico")),
    ("diseno", ("cuanto-cuesta-jardin-tampico-precios", "diseno-jardines-tampico-guia", "jardin-bajo-presupuesto-tampico",
                "jardin-vertical-tampico-guia")),
    ("mantenimiento", ("acolchado-mulch-jardin-tampico", "cesped-amarillo-tampico-causas-soluciones", "como-evitar-encharcamientos-jardin-tampico",
                       "cuando-regar-pasto-san-agustin-tampico", "errores-pasto-san-agustin-tampico",
                       "fertilizacion-jardines-tampico-temporada-lluvias", "hongos-plantas-exceso-humedad-tampico",
                       "jardines-temporada-lluvias-tampico", "nortes-tampico-proteger-plantas-jardin",
                       "plagas-comunes-jardin-tampico", "poda-arboles-palmas-tampico-guia",
                       "temporada-huracanes-proteger-jardin-tampico")),
    ("palmas", ("como-plantar-palma-arbol-paso-a-paso-tampico", "palma-areca-tampico", "palma-coco-plumoso-tampico",
                "palma-real-roystonea-regia-tampico", "palmas-mas-vendidas-tampico-precios", "palmas-tropicales-jardin-tampico")),
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
A_PRECIOS = ("cuanto-cuesta-jardin-tampico-precios", "cuanto-cuesta-pasto-sintetico-mexico", "jardin-bajo-presupuesto-tampico")
# La comparativa con pasto natural es de instalación en Tampico, no de compra en línea.
LANDING = {"pasto-sintetico-vs-natural-tampico": ("/pasto-sintetico-tampico", "Ver pasto sintético en Tampico")}


def de(slug):
    """Copia del tema del artículo con sus enlaces finales (los de sintético rotan una ciudad con página de envío)."""
    tema = TEMA[slug]
    base = CLUSTERS[tema]
    enlaces = tuple(base["enlaces"])
    if tema == "pasto-sintetico":
        c = CIUDADES[_SINTETICOS.index(slug)]
        enlaces += ((f"envío de pasto sintético a {NOMBRES_CIUDAD[c]}", f"/pasto-sintetico/envio/{c}"),)
    if slug in A_PRECIOS and not any(h == "/precios" for _t, h in enlaces):
        enlaces = (("lista de precios vigente", "/precios"),) + enlaces[:2]
    return {**base, "tema": tema, "enlaces": enlaces[:3], "landing": LANDING.get(slug, base["landing"])}
