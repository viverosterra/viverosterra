"""Contenido de la portada de cada página de servicio o producto.

Precios y datos: ver la memoria de datos oficiales (pasto $85 / $120, mayoreo $60 desde 500 m², palmas desde $250
(areca y coco plumoso) y real desde $500 en tamaño chico, garantía de plantas 30 días con riego y cuidado indicados).
"""


def guided(intro, *fields, foto=True):
    lines = [intro] + [f"{f}: " for f in fields]
    if foto:
        lines.append("Les mando foto del espacio.")
    return "\n".join(lines)


GARANTIA_PLANTAS = ("30 días", "Garantía de arraigo al sembrarlas nosotros")
DESDE_2007 = ("Desde 2007", "Vivero propio en Cd. Madero")
VARIEDADES = ("+200", "Variedades en el vivero")

# La home y /pasto-en-rollo-tampico (Etapa 2a), diseño, mantenimiento y riego (Etapa 2c) y mayoreo y palmas para
# proyectos (Etapa 2d) y, desde la Etapa 2e, el hub de plantas y sus cinco subcategorías salen de tools/site/plantillas/:
# este script ya no las toca. Quedan el vivero (Etapa 3) y los materiales (Etapas 2f y 2g).
PAGES = {
    "vivero-tampico": dict(
        title="Vivero en Tampico", accent="y Ciudad Madero, desde 2007",
        price_pre="Palmas desde", price="$250", price_unit="", price_alt="· pasto $85/m² · plantas por tamaño",
        lede='Pasto, plantas, palmas, árboles y materiales para jardín en Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, Cd. Madero, frente a Walmart.',
        facts=[VARIEDADES, DESDE_2007, GARANTIA_PLANTAS],
        img="/img/arboles-tampico-viveros-terra.webp",
        alt="Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico", caption="Siembra de árboles y plantas en Tampico.",
        wa=guided("Hola, quiero visitar el vivero o cotizar plantas.", "Lo que busco", "Tamaño aprox.", foto=False),
        secondary=("https://maps.app.goo.gl/xC4XGL2WeucAjGwAA", "Cómo llegar"),
    ),
    "marmol-blanco-tampico": dict(
        title="Mármol blanco", accent="para jardines y andadores",
        price_pre="Saco", price="$250", price_unit="", price_alt="· 3 sacos cubren 1 m²",
        lede="Grava de mármol blanco para arriates, andadores y bordes de alberca. Venta por saco o por volumen con entrega en Tampico, Madero y Altamira.",
        facts=[("20 kg", "Por saco aprox."), ("3 sacos", "Por metro cuadrado"), ("Entrega", "Tampico, Madero y Altamira")],
        img="/img/marmol-blanco-alberca-palmera-tampico.webp", img_pos="center 60%",
        alt="Mármol blanco decorativo junto a una alberca con palmera", caption="Mármol blanco junto a alberca en Tampico.",
        wa=guided("Hola, quiero cotizar mármol blanco.", "Metros a cubrir", "Colonia de entrega"),
    ),
    "piedra-bola-rio-tampico": dict(
        title="Piedra bola de río", accent="para jardines y senderos",
        price_pre="Precio", price="por medida", price_unit="", price_alt="· chica, mediana y grande",
        lede="Piedra de río natural para senderos, jardines secos y decoración. Venta por costal o camión con entrega en Tampico y la zona.",
        facts=[("3 medidas", "Chica, mediana y grande"), ("Costal o camión", "Según tu proyecto"), ("Entrega", "Tampico, Madero y Altamira")],
        wa=guided("Hola, quiero cotizar piedra bola de río.", "Medida", "Metros a cubrir", "Colonia de entrega"),
    ),
}
