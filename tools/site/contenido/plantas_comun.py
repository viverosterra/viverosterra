"""Lo que comparten las páginas de plantas (Etapa 2e): garantía con condiciones, filtro por necesidad, índice de
subcategorías, preguntas de entrega y pago, migas y nodos de JSON-LD. Solo datos.

Fotos de especie: el hub y las subcategorías usan las fotos locales del catálogo (catalogo_datos.tiene_foto), las mismas
que main, salvo las de FOTOS_SOLO_CATALOGO (hoy ninguna, por decisión del dueño). Ninguna foto se presenta como tomada
en el vivero salvo las de catalogo_datos.FOTOS_VIVERO_CONFIRMADAS (vacía hasta que el dueño confirme)."""
import datos
from contenido import catalogo_datos as cd

SITE = datos.SITIO
HUB = "/plantas-palmas-arboles-tampico"
NEGOCIO = f"{SITE}/#negocio"  # la entidad única de las demás páginas (el nodo completo vive en la home)
# Clave: slug; valor: por qué no va en el hub ni en las subcategorías. Vacía por decisión del dueño (2026-11-08): las
# fotos quedan como en main y los cambios de fotos van en otra etapa (la revisión del lote C marcó coco plumoso, escena
# de hotel con alberca, y palma areca, macetas junto a una alberca de diseño).
FOTOS_SOLO_CATALOGO = {}
LEDE_FOTOS = "Luz, riego y altura de la ficha del catálogo. Fotos de referencia de cada especie."

GARANTIA = {
    "titulo": "Garantía de 30 días en las plantas que sembramos",
    "grande": "30", "unidad": "días",
    "resumen": f'{datos.GARANTIA_PLANTAS} <a href="/politicas#garantia-plantas">Condiciones de la garantía</a>',
    "puntos": (("En las plantas, palmas y árboles que sembramos nosotros", True),
               ("Con el riego y los cuidados que te indicamos al entregar", True),
               ("Te decimos antes de sembrar qué especie va en sol, sombra o cerca del mar", True),
               ("Si te las llevas y las siembras tú, no aplica la garantía de arraigo", False)),
    "pie": (f'Recoges en <a href="/vivero-tampico">el vivero de Cd. Madero</a> ({datos.CALLE_CORTA}) o te las llevamos '
            "en Tampico, Madero y Altamira."),
}

# (clave, título, texto, filtro del catálogo). El conteo lo pone componentes_plantas.necesidades() en el build.
NECESIDADES = (
    ("sol", "Sol directo todo el día", "Florecen y aguantan el calor del mediodía.", {"luz": ["sol"]}),
    ("sombra", "Sombra o media sombra", "Patios techados, interiores y jardines bajo árboles.",
     {"luz": ["media", "sombra"]}),
    ("salitre", "Cerca del mar (salitre)", "Aguantan la brisa salina de Madero y Miramar.", {"uso": ["salitre"]}),
    ("chica", "Chicas: hasta 1.5 m", "Macetas, arriates y bordes.", {"tam": ["chica"]}),
    ("mediana", "Medianas: de 1.5 a 5 m", "Setos, esquinas y jardines medianos.", {"tam": ["mediana"]}),
    ("grande", "Grandes: más de 5 m", "Sombra, banquetas y jardines amplios.", {"tam": ["grande"]}),
)

_PORTADAS = "/img/portadas"
# Índice de subcategorías del hub (y "otras subcategorías" en cada una). El "desde" sale de datos.DESDE_PLANTAS. Las
# fotos son las portadas que ya publicaba cada subcategoría en main (medidas con sips).
SUBCATEGORIAS = (
    {"titulo": "Palmas tropicales", "href": "/palmas-tropicales-tampico",
     "texto": "Areca, coco plumoso, palma real, washingtonia, del viajero y exóticas.",
     "img": f"{_PORTADAS}/palma-real-jardin-residencial-tampico-sm.webp", "ancho": 560, "alto": 996,
     "unidad": "tamaño chico"},
    {"titulo": "Plantas para jardín", "href": "/plantas-para-jardin-tampico",
     "texto": "Ornamentales, tropicales y de cobertura para sol, humedad y salitre.",
     "img": f"{_PORTADAS}/jardin-residencial-tropical-tampico-sm.webp", "ancho": 560, "alto": 373, "unidad": ""},
    {"titulo": "Árboles ornamentales", "href": "/arboles-ornamentales-tampico",
     "texto": "De sombra y de flor: flamboyán, jacaranda, palo de rosa, magnolia y más.",
     "img": f"{_PORTADAS}/arboles-tampico-viveros-terra-sm.webp", "ancho": 560, "alto": 747, "unidad": ""},
    {"titulo": "Árboles para banqueta", "href": "/arboles-para-banqueta-tampico",
     "texto": "Especies de raíz profunda para frentes y camellones.",
     "img": f"{_PORTADAS}/arboles-vivero-tampico-mayoreo-sm.webp", "ancho": 560, "alto": 840, "unidad": ""},
    {"titulo": "Plantas de interior", "href": "/plantas-de-interior-tampico",
     "texto": "Para casas y oficinas con poca luz y aire acondicionado.",
     "img": f"{_PORTADAS}/plantas-ornamentales-tampico-viveros-terra-sm.webp", "ancho": 560, "alto": 840,
     "unidad": ""},
)

# Sin "la Huasteca" ni zonas lejanas: la cobertura de entrega que confirmó el dueño es Tampico, Madero y Altamira.
PREGUNTA_ENTREGA = ("¿Hacen entrega de plantas a domicilio en Tampico?",
                    "Sí. Entregamos plantas, palmas y árboles en Tampico, Ciudad Madero y Altamira; para otra zona, "
                    "pregúntanos por WhatsApp. También puedes recoger en "
                    f"{datos.CALLE}, {datos.CIUDAD} ({datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}).")
PREGUNTA_PAGO = ("¿Cómo se paga un pedido de plantas?",
                 f"{datos.ANTICIPO} Te mandamos la cotización por WhatsApp con el total antes de confirmar.")

LISTA = {"titulo": "Arma tu lista y cotiza en un solo mensaje",
         "texto": (f"En el catálogo están {len(cd.ESPECIES)} especies con luz, riego y altura. Añade las que te "
                   "interesan con su tamaño y piezas, y mándanos la lista completa por WhatsApp en un solo mensaje: te "
                   "respondemos con precio por tamaño.")}


def otras_subcategorias(ruta):
    """Relacionados de una subcategoría: las otras cuatro (sin el "desde", que es del índice del hub)."""
    return tuple({k: s[k] for k in ("titulo", "href", "texto", "img", "ancho", "alto")}
                 for s in SUBCATEGORIAS if s["href"] != ruta)


def migas(nombre=None):
    """Visibles: Inicio › Plantas y palmas (› subcategoría)."""
    if nombre is None:
        return (("Inicio", "/"), ("Plantas y palmas", None))
    return (("Inicio", "/"), ("Plantas y palmas", HUB), (nombre, None))


def migas_ld(nombre=None, ruta=None):
    items = [("Inicio", SITE), ("Plantas y palmas", f"{SITE}{HUB}")] + ([(nombre, f"{SITE}{ruta}")] if nombre else [])
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(items, 1)]}


def lista_ld(nombre, especies_):
    """ItemList de las especies de la página (nombre y científico), sin precios."""
    return {"@type": "ItemList", "name": nombre, "numberOfItems": len(especies_), "itemListElement": [
        {"@type": "ListItem", "position": i, "name": f"{cd.especie(s)['name']} ({cd.especie(s)['sc']})"}
        for i, s in enumerate(especies_, 1)]}

