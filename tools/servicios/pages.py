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
# proyectos (Etapa 2d), el hub de plantas y sus cinco subcategorías (Etapa 2e) y, desde la Etapa 2f, los cuatro
# materiales salen de tools/site/plantillas/: este script ya no las toca. Queda el vivero (Etapa 3).
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
}
