"""Las especies del catálogo (Etapa 2e): una sola fuente para /catalogo, el hub y las subcategorías de plantas.

catalogo_especies.json se extrajo una vez del arreglo `plants` de public/catalogo.html de main (plan 2e, Tarea 4) y desde
ahí es la fuente: nombre, nombre científico, tamaños, insignias, luz, riego, altura, flor, mantenimiento, tipo,
descripción y la foto local (img, ancho y alto, que escribe tools/site/fotos_catalogo.py; null en las FOTOS_RETIRADAS, hoy ninguna). `drive` guarda el id de Google
Drive de donde salió la foto: solo lo lee fotos_catalogo.py; ninguna página lo publica. Va en JSON por volumen (117
especies), como los cuerpos del blog de la Etapa 2h.

atributos() es pAttr() del JS de main, línea por línea (los 118 casos están en public/js/tests/casos-catalogo.json).
tamano() agrupa la altura adulta. SALITRE marca las especies que aguantan salitre, cada una con su fuente publicada.
"""
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

ARCHIVO = Path(__file__).resolve().parent / "catalogo_especies.json"
GRUPOS = ("cat", "luz", "tam", "riego", "uso")
# Nombres científicos mal escritos en main (mayúscula en el epíteto o letras cambiadas), corregidos a la forma botánica,
# que es la que ya publicaban las subcategorías. Clave: como estaba publicado; valor: como queda.
CIENTIFICOS_CORREGIDOS = {
    "Bucida Buceras": "Bucida buceras",
    "Quercus Virginiana": "Quercus virginiana",
    "Lagerstroemia Indica": "Lagerstroemia indica",
    "Cassia Fistula": "Cassia fistula",
    "Delonix Regia": "Delonix regia",
    "Jacaranda Mimisfolia": "Jacaranda mimosifolia",
    "Jacaranda mimifolia": "Jacaranda mimosifolia",  # así venía en /arboles-ornamentales-tampico
    "Tabubeia Rosea": "Tabebuia rosea",
    "Tecoma Stans": "Tecoma stans",
    "Ficus Elastica": "Ficus elastica",
    "Bahuinia sp.": "Bauhinia sp.",
    # Revisión 2e: el cultivar va entre comillas simples y sin un «var.» colgando; solo el que el nombre común da.
    "Nerium oleander nana": "Nerium oleander 'Nana'",
    "Schefflera arboricola var.": "Schefflera arboricola 'Gold'",  # Aralia Golden
    "Duranta erecta var.": "Duranta erecta 'Gold'",  # Duranta Golden
}
_SAL = "/blog/plantas-resistentes-sal-golfo-tampico"
# Especies que aguantan salitre, con su fuente publicada (la tabla del artículo o la ficha de main). Pregunta 6 al dueño.
SALITRE = {
    "palma-cocotera": _SAL, "palma-datilera": _SAL, "uva-de-playa": _SAL, "sansiviera": _SAL,
    "sansiviera-variegada": _SAL, "adelfa-enana": _SAL, "bugambilea-mini-morada": _SAL, "bugambilea-envarada": _SAL,
    "croto-petra": _SAL, "croto-tornillo": _SAL,
    "olivo-negro": "Ficha del catálogo de main: «Muy tolerante al calor y sal marina»",
    "casuarina": "Ficha del catálogo de main: «Muy resistente a la sal marina y el viento costero»",
    "arbusto-de-playa": "Ficha del catálogo de main: «Muy resistente a la sal marina, el viento y el calor»",
}
# Guía del blog de la especie, solo cuando el artículo trata de esa especie. Kerpis queda fuera: el artículo es de Howea
# forsteriana y el catálogo dice Chamaedorea sp. (pregunta 4 al dueño).
BLOG_ESPECIE = {
    "palma-areca": "/blog/palma-areca-tampico",
    "palma-bismarkia": "/blog/palma-bismarckia-bismarckia-nobilis-tampico",
    "coco-plumoso": "/blog/palma-coco-plumoso-tampico",
    "palma-cola-de-zorra": "/blog/palma-cola-de-zorro-wodyetia-bifurcata-tampico",
    "palma-real": "/blog/palma-real-roystonea-regia-tampico",
    "palma-triangular": "/blog/palma-triangular-dypsis-decaryi-tampico",
    "palma-washingtona": "/blog/palma-washingtona-tampico",
    "palma-viajera-ravenala": "/blog/cuidados-palma-del-viajero-ravenala",
    "hule": "/blog/ficus-elastica-cuidados-tampico",
    "flamboyan-tabachin": "/blog/framboyan-delonix-regia-tampico",
    "duranta-cubana": "/blog/duranta-erecta-tampico-cuidados-seto",
    "duranta-golden": "/blog/duranta-erecta-tampico-cuidados-seto",
    "duranta-zafiro": "/blog/duranta-erecta-tampico-cuidados-seto",
    "bugambilea-mini-morada": "/blog/buganvilia-tampico-cuidados-floracion",
    "bugambilea-envarada": "/blog/buganvilia-tampico-cuidados-floracion",
}
# Fotos de Drive de menos de 480 px de ancho (medidas en el prototipo del plan 2e, 2026-11-08, y en la descarga real del
# mismo día, que sumó crespón astronómica y flamboyán: su original en Drive mide 400×400): se publican a su tamaño, sin
# agrandar (igual de chicas que con /api/img), y son las primeras a reponer en la sesión de fotos (pregunta 12).
FOTOS_CHICAS = frozenset({
    "sauce-lloron", "liquidambar", "nispero", "eucalipto", "flor-de-mayo", "orquidea-pata-de-vaca", "palma-mascarena",
    "palma-cocotera", "palma-rubelina", "plumbago", "aralia-elegantisima", "beucarnea-soyate", "ficus-lyrata-pandurata",
    "ixora-karla", "limonaria", "papiro-estrella", "pasto-liriope", "palma-carton", "heliconia-baby-enana",
    "lapiz-tirucalli", "petunia-silvestre", "crespon-astronomica", "flamboyan-tabachin",
})
# Fotos de terceros halladas en la revisión del 2026-11-08 (lote A del plan 2e y la hoja de contactos de las 117). Por
# decisión del dueño (2026-11-08: «No elimines o cambies las fotos, déjalas así como están; en otra etapa trabajamos los
# cambios de fotos») siguen publicadas como en main: esta lista es solo el pendiente para la etapa de fotos y no quita
# ninguna. Clave: slug; valor: lo que se vio.
FOTOS_POR_REVISAR = {
    "eucalipto": "Marca de agua de Shutterstock",
    "flor-de-mayo": "Marca de agua de Shutterstock",
    "tronadora": "Marca de agua de Dreamstime",
    "acacia-negra": "Logo de una universidad y licencia Creative Commons sobre la foto",
    "palma-cola-de-pescado": "Captura de Google Imágenes (botón «Visit» y título recortado)",
    "beucarnea-soyate": "Logo de otro vivero sobre la foto",
    "esparrago-meyeri": "Marca de agua de un sitio de venta en línea",
    "clorofito-liston": "Logo de una tienda en línea en la maceta",
    "polyalthia": "Marca de agua de un banco de imágenes en mosaico",
    "wudelia-rastrera": "Marca de agua de otro vivero («redviverista»)",
    "orquidea-pata-de-vaca": "Recorte con el cuadriculado de transparencia falso pegado en la foto",
    "ixora-karla": "Marca de agua de otro vivero («redviverista»)",
    "lluvia-de-oro": "Marca de agua en mosaico diagonal de un banco de imágenes",
    "parota-orejon": "Restos de marca de agua alrededor del recorte",
    "eleagnus": "Logo de otro vivero («Concepto Verde») en la bolsa",
    "crespon-astronomica": "Captura de pantalla: el recorte va dentro de un marco gris",
    # Segunda revisión (2026-11-08, lote C del plan 2e, con el contraste ecualizado): marcas tenues que no se veían.
    "agave-atenuata": "Etiqueta con el logo y el sitio de otro vendedor clavada en la maceta",
    "aralia-elegantisima": "Marca de agua de otro vivero («Concepto Verde») en la bolsa",
    "aralia-shaflera": "Marca de agua de otro vivero («Concepto Verde») en la maceta",
    "floripondio": "Marca de agua de otro vivero («Concepto Verde») en la bolsa",
    "jazmin": "Marca de agua de otro vivero («Concepto Verde») en la bolsa",
    "fornio-phormium": "Marca de agua tenue de otro vivero («Concepto Verde») sobre las hojas",
    "pasto-liriope": "Marca de agua tenue de otro vivero («Concepto Verde») en la bolsa",
    "heliconia-baby-enana": "Marca de agua de otro vivero («redviverista») sobre las hojas",
}
# Fotos que no se publican (el marcador "sin foto" de componentes_plantas y fotos_catalogo.py no las baja). Vacía por
# decisión del dueño (2026-11-08): los cambios de fotos van en otra etapa (FOTOS_POR_REVISAR es el pendiente).
FOTOS_RETIRADAS = {}
# Especies cuya foto el dueño confirmó que se tomó en el vivero: solo ellas llevan "En nuestro vivero" en el pie y en el
# alt. Empieza vacía a propósito (muchas fotos son de estudio o de bancos de imágenes); la llena el dueño, slug por slug.
FOTOS_VIVERO_CONFIRMADAS = frozenset()
# Altura adulta: (clave, etiqueta, máximo en cm o None).
TAMANOS = (("chica", "Hasta 1.5 m", 150), ("mediana", "De 1.5 a 5 m", 500), ("grande", "Más de 5 m", None))


def normalizar(texto):
    """Como normalizar() de vt-catalogo.js: sin acentos, minúsculas y un solo espacio."""
    sin_acentos = "".join(c for c in unicodedata.normalize("NFD", str(texto or "")) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sin_acentos.lower()).strip()


def slug(nombre):
    return re.sub(r"[^a-z0-9]+", "-", normalizar(nombre)).strip("-")


def cargar(archivo=ARCHIVO):
    return tuple(json.loads(Path(archivo).read_text(encoding="utf-8")))


ESPECIES = cargar()
POR_SLUG = {e["slug"]: e for e in ESPECIES}
ORDENADAS = tuple(sorted(ESPECIES, key=lambda e: normalizar(e["name"])))


def especie(clave):
    return POR_SLUG[clave]


def tiene_foto(e):
    return bool(e.get("img")) and e["slug"] not in FOTOS_RETIRADAS


def foto_del_vivero(e):
    return tiene_foto(e) and e["slug"] in FOTOS_VIVERO_CONFIRMADAS


def _sin_etiquetas(texto):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", texto or "")).strip().lower()


def atributos(e):
    """pAttr() de main: luz (sol, media, sombra), riego, flor, mantenimiento y uso (banqueta, interior)."""
    luz = _sin_etiquetas(e["luz"])
    niveles = set()
    if "sol" in luz:
        niveles.add("sol")
    if "media" in luz:
        niveles.add("media")
    if "sombra" in luz and "media" not in luz:
        niveles.add("sombra")
    agua = (e.get("agua") or "").lower()
    riego = "poco" if re.search(r"poco|muy bajo", agua) else "abundante" if "abundante" in agua else "moderado"
    flor = "conflor" if re.match(r"^s[ií]", (e.get("flor") or "").strip().lower()) else "sinflor"
    mant = "bajo" if re.search(r"bajo", e.get("mant") or "", re.I) else "otro"
    tipo = (e.get("tipo") or "").lower()
    uso = set()
    if "banqueta" in tipo:
        uso.add("banqueta")
    if "interior" in tipo or "bi" in (e.get("b") or []):
        uso.add("interior")
    return {"luz": sorted(niveles), "riego": riego, "flor": flor, "mant": mant, "uso": sorted(uso)}


def altura_cm(texto):
    m = re.search(r"(\d[\d.,]*)\s*(m|cm)", texto or "", re.I)
    if not m:
        return None
    n = float(m.group(1).replace(",", "."))
    return n if m.group(2).lower() == "cm" else n * 100


def tamano(e):
    cm = altura_cm(e.get("altura"))
    if cm is None:
        return None
    return next(clave for clave, _t, maximo in TAMANOS if maximo is None or cm <= maximo)


def filtros(e):
    """Valores de cada grupo de filtro (los mismos data-* de la tarjeta que lee vt-catalogo.js)."""
    a = atributos(e)
    t = tamano(e)
    return {"cat": [e["cat"]], "luz": a["luz"], "tam": [t] if t else [], "riego": [a["riego"]],
            "uso": a["uso"] + (["salitre"] if e["slug"] in SALITRE else [])}


def coincide(e, filtro):
    """Como coincide() de vt-catalogo.js: dentro de un grupo basta una opción; entre grupos, todas."""
    valores = filtros(e)
    return all(any(v in valores[g] for v in opciones) for g, opciones in filtro.items() if opciones)


def cuenta(filtro):
    return sum(1 for e in ESPECIES if coincide(e, filtro))


def url_catalogo(filtro=None, q="", agregar=""):
    """/catalogo con el filtro en la URL, en el mismo formato que escribirFiltros() de vt-catalogo.js. agregar: slug de
    la especie cuyo diálogo "Añadir a mi lista" abre vt-catalogo.js al cargar (&add=<slug>)."""
    partes = [f"q={quote(q, safe='')}"] if q else []
    partes += [f"{g}={','.join(quote(v, safe='') for v in (filtro or {})[g])}" for g in GRUPOS
               if (filtro or {}).get(g)]
    partes += [f"add={quote(agregar, safe='')}"] if agregar else []
    return "/catalogo" + ("?" + "&".join(partes) if partes else "")
