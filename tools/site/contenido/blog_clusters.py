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
    return {**base, "tema": tema, "enlaces": enlaces[:3], "landing": LANDING.get(slug, base["landing"]), "lede": LEDE[tema]}
