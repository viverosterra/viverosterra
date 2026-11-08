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
# proyectos (Etapa 2d) y, desde la Etapa 2e, el hub de plantas salen de tools/site/plantillas/: este script ya no las
# toca. Quedan las de las Etapas 2e a 2g.
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
    "plantas-para-jardin-tampico": dict(
        title="Plantas para jardín", accent="que aguantan el calor de Tampico",
        price_pre="Precio", price="por tamaño", price_unit="", price_alt="· cotiza con una foto de tu espacio",
        lede="Ornamentales, tropicales y de cobertura elegidas para sol, humedad y salitre. Te decimos cuáles van en sol y cuáles en sombra.",
        facts=[VARIEDADES, GARANTIA_PLANTAS, ("Asesoría", "Sin costo, por WhatsApp")],
        img="/img/jardin-residencial-tropical-tampico.webp",
        alt="Jardín residencial con plantas tropicales en Tampico", caption="Jardín con plantas tropicales en Tampico.",
        wa=guided("Hola, quiero cotizar plantas para mi jardín.", "El lugar es de sol o de sombra", "Metros aprox.", "Colonia"),
        secondary=("/catalogo", "Ver catálogo"),
    ),
    "plantas-de-interior-tampico": dict(
        title="Plantas de interior", accent="para casas y oficinas en Tampico",
        price_pre="Precio", price="por tamaño", price_unit="", price_alt="· cotiza con una foto del lugar",
        lede="Pothos, sansevieria, aglaonema, monstera y más, adaptadas al calor y la humedad de Tampico. Entrega a domicilio.",
        facts=[VARIEDADES, ("Poca luz", "Opciones para interiores"), ("Entrega", "Tampico, Madero y Altamira")],
        img="/img/plantas-ornamentales-tampico-viveros-terra.webp",
        alt="Plantas de interior en macetas del vivero Viveros Terra", caption="Plantas de interior del vivero.",
        wa=guided("Hola, quiero plantas de interior.", "Casa u oficina", "Luz del lugar (mucha o poca)", "Colonia"),
        secondary=("/catalogo", "Ver catálogo"),
    ),
    "palmas-tropicales-tampico": dict(
        title="Palmas para jardín en Tampico,", accent="tropicales y exóticas",
        price_pre="Desde", price="$250", price_unit="", price_alt="en tamaño chico; el precio sube con la altura",
        lede="Areca y coco plumoso desde $250 y palma real desde $500 en su tamaño más chico. También washingtonia, del viajero, bismarckia y exóticas. Te las llevamos y las sembramos con garantía de arraigo.",
        facts=[GARANTIA_PLANTAS, ("$500", "Palma real desde, tamaño chico"), ("Entrega y siembra", "Tampico, Madero y Altamira")],
        img="/img/palma-real-jardin-residencial-tampico.webp", img_pos="center 30%",
        alt="Palma real sembrada en un jardín residencial de Tampico", caption="Palma real en un jardín de Tampico.",
        wa=guided("Hola, quiero cotizar palmas.", "Palma que me interesa", "Altura aprox.", "Colonia de entrega"),
    ),
    "arboles-ornamentales-tampico": dict(
        title="Árboles ornamentales", accent="para jardines en Tampico",
        price_pre="Desde", price="$250", price_unit="", price_alt="· flamboyán $250 · crespón $350 · jacaranda $450",
        lede="Árboles de sombra y de flor elegidos para el clima de Tamaulipas. Te los llevamos y los sembramos con garantía de arraigo.",
        facts=[GARANTIA_PLANTAS, ("Entrega y siembra", "Tampico, Madero y Altamira"), VARIEDADES],
        img="/img/arboles-tampico-viveros-terra.webp",
        alt="Equipo de Viveros Terra sembrando un árbol ornamental en Tampico", caption="Siembra de un árbol ornamental en Tampico.",
        wa=guided("Hola, quiero cotizar árboles.", "Árbol que me interesa", "Altura aprox.", "Colonia de entrega"),
    ),
    "arboles-para-banqueta-tampico": dict(
        title="Árboles para banqueta", accent="que no levantan el pavimento",
        price_pre="Precio", price="por tamaño", price_unit="", price_alt="· cotiza con la medida de tu banqueta",
        lede="Siete especies de raíz controlada para frentes y camellones: olivo negro, polyalthia, neem, fresno, crespón y más.",
        facts=[("7 especies", "De raíz que no daña la banqueta"), GARANTIA_PLANTAS, ("Entrega y siembra", "Tampico, Madero y Altamira")],
        img="/img/arboles-vivero-tampico-mayoreo.webp", img_pos="center 40%",
        alt="Árboles jóvenes en el vivero listos para sembrar en banqueta", caption="Árboles en el vivero de Viveros Terra.",
        wa=guided("Hola, quiero árboles para mi banqueta.", "Ancho de la banqueta", "Cuántos árboles", "Colonia"),
    ),
    "tierra-negra-vegetal-tampico": dict(
        title="Tierra negra vegetal", accent="por costal o camión",
        price_pre="Costal", price="$90", price_unit="", price_alt="· preparada $100 · m³ $1,500 · camión desde $5,000",
        lede="Tierra negra con materia orgánica para pasto, jardineras y siembra. Recoges en el vivero o te la llevamos en Tampico, Madero y Altamira.",
        facts=[("$1,500", "Por metro cúbico"), ("Desde $5,000", "Camión volteo"), ("Entrega", "Tampico, Madero y Altamira")],
        img="/img/camion-tierra-negra-entrega-tampico.webp",
        alt="Camión de Viveros Terra entregando tierra negra en Tampico", caption="Entrega de tierra negra en Tampico.",
        wa=guided("Hola, quiero cotizar tierra negra.", "Costales o camión", "Cantidad", "Colonia de entrega", foto=False),
    ),
    "tezontle-rojo-tampico": dict(
        title="Tezontle rojo", accent="por costal, m³ o camión",
        price_pre="Costal", price="$200", price_unit="", price_alt="· también por m³ y camión de 14 m³",
        lede="Tezontle volcánico para drenaje de macetas, jardineras y decoración. Recoges en el vivero o te lo llevamos con factura.",
        facts=[("14 m³", "Camión volteo"), ("CFDI 4.0", "Factura disponible"), ("Entrega", "Tampico, Madero y Altamira")],
        wa=guided("Hola, quiero cotizar tezontle rojo.", "Costales o camión", "Cantidad", "Colonia de entrega", foto=False),
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
