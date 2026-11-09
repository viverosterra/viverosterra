"""Mensajes de WhatsApp propios de cada página, recuperados de los botones flotantes que había en main antes del shell.

El shell los usa en el menú, la barra móvil y el pie (paginas.contexto): así el chat llega diciendo qué leyó la persona.
Los textos son los de main; solo se corrigieron dos artículos que decían "Palma Cola de Zorro" por un copiar y pegar
(duranta y nortes) y los huecos vacíos se marcan con ___ como en datos.MENSAJES. La firma se agrega en datos.con_firma.
"""

# Servicios de jardín (Etapa 2c): la plantilla de main de cada portada, con los huecos marcados ___. Lo usan la portada y
# el cierre de la página (tools/site/contenido/) y, por RUTAS, el menú, la barra móvil y el pie.
SERVICIOS = {
    "/diseno-jardines-tampico": ("Hola, me interesa el diseño de mi jardín.\nColonia: ___\nMetros aprox.: ___\n"
                                 "Plan que me interesa: ___\nLes mando fotos del espacio."),
    "/mantenimiento-jardines-tampico": ("Hola, quiero cotizar mantenimiento de jardín.\nColonia: ___\n"
                                        "Metros aprox. del jardín: ___\nCasa o empresa: ___\n"
                                        "Frecuencia (semanal, cada 15 días, cada 21 días o mensual): ___"),
    "/sistema-riego-tampico": ("Hola, quiero cotizar riego automático.\nColonia: ___\nMetros aprox. del jardín: ___\n"
                               "Tengo pasto, plantas o ambos: ___\nLes mando fotos del espacio."),
}

# Empresas (Etapa 2d): la plantilla de compras de cada página B2B (la de main, con los huecos ___). La usan la portada, el
# cierre y los cotizadores mientras no tienen datos y, por RUTAS, el menú, la barra móvil y el pie.
EMPRESAS = {
    "/mayoreo-pasto-tampico": ("Hola, quiero cotizar pasto San Agustín al mayoreo para un proyecto.\nEmpresa: ___\n"
                               "Obra y ubicación: ___\nm² totales: ___\nFecha de la primera entrega: ___"),
    "/palmas-mayoreo-proyectos": ("Hola, quiero cotizar palmas para un proyecto.\nEmpresa: ___\nObra y ubicación: ___\n"
                                  "Especies, altura y cantidad: ___\nFecha de entrega: ___"),
}

# Plantas (Etapa 2e): la plantilla de main de cada portada (tools/servicios/pages.py, guided()), con los huecos ___. La
# usan la portada y el cierre y, por RUTAS, el menú, la barra móvil y el pie. El catálogo conserva su mensaje de RUTAS.
PLANTAS = {
    "/plantas-palmas-arboles-tampico": ("Hola, quiero cotizar plantas o palmas.\nPlantas que busco: ___\n"
                                        "Tamaño aprox.: ___\nColonia de entrega: ___\nLes mando foto del espacio."),
    "/palmas-tropicales-tampico": ("Hola, quiero cotizar palmas.\nPalma que me interesa: ___\nAltura aprox.: ___\n"
                                   "Colonia de entrega: ___\nLes mando foto del espacio."),
    "/plantas-para-jardin-tampico": ("Hola, quiero cotizar plantas para mi jardín.\nEl lugar es de sol o de sombra: ___\n"
                                     "Metros aprox.: ___\nColonia: ___\nLes mando foto del espacio."),
    "/arboles-ornamentales-tampico": ("Hola, quiero cotizar árboles.\nÁrbol que me interesa: ___\nAltura aprox.: ___\n"
                                      "Colonia de entrega: ___\nLes mando foto del espacio."),
    "/arboles-para-banqueta-tampico": ("Hola, quiero árboles para mi banqueta.\nAncho de la banqueta: ___\n"
                                       "Cuántos árboles: ___\nColonia: ___\nLes mando foto del espacio."),
    "/plantas-de-interior-tampico": ("Hola, quiero plantas de interior.\nCasa u oficina: ___\n"
                                     "Luz del lugar (mucha o poca): ___\nColonia: ___\nLes mando foto del espacio."),
}

# Nochebuenas, por modo (datos.NOCHEBUENAS["modo"]): mensaje de la página y del shell; el cotizador lo reemplaza por el pedido
# completo. paginas.contexto elige el del modo vigente.
NOCHEBUENAS = {
    "temporada": "Hola, quiero cotizar Nochebuenas.\nTamaño y cantidad: ___\nColonia de entrega: ___",
    "preventa": "Hola, quiero apartar Nochebuenas.\nTamaño y cantidad: ___\nColonia de entrega: ___",
    "postemporada": "Hola, avísenme cuando abra la próxima temporada de Nochebuenas.",
}

# Materiales (Etapa 2f): la plantilla de main de cada portada (tools/servicios/pages.py, guided()), con los huecos ___:
# el formato de datos.MENSAJES["materiales"] (material, cantidad y colonia de entrega) con el material ya escrito. La usan
# la portada, el cierre y la calculadora mientras no tiene área y, por RUTAS, el menú, la barra móvil y el pie.
MATERIALES = {
    "/tierra-negra-vegetal-tampico": ("Hola, quiero cotizar tierra negra.\nCostales o camión: ___\nCantidad: ___\n"
                                      "Colonia de entrega: ___"),
    "/tezontle-rojo-tampico": ("Hola, quiero cotizar tezontle rojo.\nCostales o camión: ___\nCantidad: ___\n"
                               "Colonia de entrega: ___"),
    "/marmol-blanco-tampico": ("Hola, quiero cotizar mármol blanco.\nMetros a cubrir: ___\nColonia de entrega: ___\n"
                               "Les mando foto del espacio."),
    # Piedra bola: a granel, sin medidas (dueño, 2026-11-08): el mensaje ya no pide "Medida".
    "/piedra-bola-rio-tampico": ("Hola, quiero cotizar piedra bola de río.\nMetros a cubrir: ___\n"
                                 "Colonia de entrega: ___\nLes mando foto del espacio."),
}

# Zonas (Etapa 2g): la plantilla de main de cada zona (tools/pasto/zonas.py, guided()), con los huecos ___. La usan la
# portada y el cierre y, por RUTAS, el menú, la barra móvil y el pie (antes llevaban el genérico de jardín).
_ZONA = "Hola, quiero cotizar jardinería en {}.\nColonia: ___\nServicio que necesito: ___\nMetros aprox.: ___\nLes mando foto del espacio."
ZONAS = {
    "/jardineria-lomas-de-rosales-tampico": _ZONA.format("Lomas de Rosales"),
    "/jardineria-country-club-tampico": _ZONA.format("Club Campestre"),
    "/jardineria-aguila-tampico": _ZONA.format("Águila y Altavista"),
    "/jardineria-lomas-del-chairel-tampico": _ZONA.format("Lomas del Chairel"),
    "/jardineria-ciudad-madero": _ZONA.format("Cd. Madero"),
    "/jardineria-altamira": _ZONA.format("Altamira"),
}
# Poda en la zona: su renglón de la lista pide fotos (el precio depende del tamaño y de los residuos).
_PODA = "Hola, quiero cotizar poda de palmas y árboles{}.\nColonia: ___\nCuántos árboles o palmas: ___\nLes mando fotos."
PODA_ZONAS = {
    "/jardineria-lomas-de-rosales-tampico": _PODA.format(" en Lomas de Rosales"),
    "/jardineria-country-club-tampico": _PODA.format(" en Club Campestre"),
    "/jardineria-aguila-tampico": _PODA.format(" en Águila y Altavista"),
    "/jardineria-lomas-del-chairel-tampico": _PODA.format(" en Lomas del Chairel"),
    "/jardineria-ciudad-madero": _PODA.format(" en Cd. Madero"),
    "/jardineria-altamira": _PODA.format(" en Altamira"),
}
# /precios (Etapa 2g): la portada, el menú y la barra (RUTAS) con los huecos de main ("Mi colonia es: ___ y son aprox. ___
# m²"), y un mensaje por sección de la lista para que el chat llegue diciendo qué se quiere cotizar.
PRECIOS = "Hola, vi la lista de precios y quiero cotizar.\nColonia: ___\nMetros aprox.: ___"
PRECIOS_SECCIONES = {
    "pasto": "Hola, quiero cotizar pasto San Agustín instalado.\nColonia: ___\nMetros aprox.: ___",
    "servicios": ("Hola, quiero cotizar un servicio de jardín.\nMantenimiento, diseño o riego: ___\nColonia: ___\n"
                  "Metros aprox.: ___"),
    "poda": _PODA.format(""),
    "sintetico": "Hola, quiero cotizar pasto sintético.\nModelo: ___\nMetros aprox.: ___\nColonia o ciudad: ___",
    "materiales": "Hola, quiero cotizar materiales.\nMaterial: ___\nCantidad: ___\nColonia de entrega: ___",
    "plantas": ("Hola, quiero cotizar plantas o palmas.\nPlantas que busco: ___\nTamaño aprox.: ___\n"
                "Colonia de entrega: ___"),
}

# Ruta exacta → (mensaje del menú y la barra, mensaje del pie o None para usar el mismo).
RUTAS = {
    "/blog": ("Hola, vi el blog de Viveros Terra y quiero cotizar", None),
    "/catalogo": ("Hola, vi el catálogo y quiero cotizar una planta", None),
    "/precios": (PRECIOS, "Hola, tengo una pregunta sobre precios"),
    **{ruta: (texto, None) for ruta, texto in SERVICIOS.items()},
    **{ruta: (texto, None) for ruta, texto in EMPRESAS.items()},
    **{ruta: (texto, None) for ruta, texto in PLANTAS.items()},
    **{ruta: (texto, None) for ruta, texto in MATERIALES.items()},
    **{ruta: (texto, None) for ruta, texto in ZONAS.items()},
}
# Tienda y páginas de envío: el pie conserva su "pregunta"; el menú usa el mensaje de cotizar pasto sintético.
PIE_TIPO = {
    "tienda": "Hola, tengo una pregunta sobre pasto sintético",
    "ciudad": "Hola, tengo una pregunta sobre pasto sintético",
}

# Artículo del blog (slug) → mensaje.
BLOG = {
    "acolchado-mulch-jardin-tampico": "Hola, vi el artículo de acolchado (mulch) y quiero cotizar",
    "arboles-para-sembrar-en-banqueta": 'Hola, leí su artículo "7 árboles para banqueta que no levantan el pavimento en Tampico" y quiero cotizar.',
    "buganvilia-tampico-cuidados-floracion": 'Hola, leí su artículo "Buganvilia en Tampico: cómo cultivarla y lograr que florezca todo el año" y quiero cotizar.',
    "cesped-amarillo-tampico-causas-soluciones": "Hola, mi césped se está poniendo amarillo y necesito diagnóstico",
    "como-ahorrar-agua-jardin-tampico": 'Hola, leí su artículo "Cómo ahorrar agua en tu jardín en Tampico sin sacrificar la belleza" y quiero cotizar.',
    "como-evitar-encharcamientos-jardin-tampico": "Hola, vi el artículo de drenaje de jardín y quiero cotizar",
    "como-instalar-pasto-sintetico": 'Hola, leí su artículo "Cómo instalar pasto sintético tú mismo: guía paso a paso" y quiero cotizar.',
    "como-medir-plantas-altura-cepellon": "Hola, quiero cotizar una planta con medidas específicas: ___",
    "como-plantar-palma-arbol-paso-a-paso-tampico": "Hola, vi el artículo de cómo plantar una palma o árbol y quiero cotizar plantación",
    "cuando-plantar-pasto-tampico-calendario": 'Hola, leí su artículo "Cuándo plantar pasto en Tampico: calendario de siembra mes a mes" y quiero cotizar.',
    "cuando-regar-pasto-san-agustin-tampico": 'Hola, leí su artículo "¿Cuándo y cuánto regar el pasto San Agustín en Tampico? La guía por temporada" y quiero cotizar.',
    "cuanto-cuesta-jardin-tampico-precios": "Hola, vi la guía de precios de jardines y quiero cotizar el mío",
    "cuanto-cuesta-pasto-sintetico-mexico": 'Hola, leí su artículo "¿Cuánto cuesta el pasto sintético en México? Precios 2026 por m²" y quiero cotizar.',
    "cuidados-palma-del-viajero-ravenala": 'Hola, leí su artículo "Palma del viajero en Tampico: guía completa de cuidados (y por qué aquí crece el doble)" y quiero cotizar.',
    "diseno-jardines-tampico-guia": 'Hola, leí su artículo "Cómo diseñar tu jardín en Tampico: guía paso a paso para el clima del Golfo" y quiero cotizar.',
    "duranta-erecta-tampico-cuidados-seto": 'Hola, leí su artículo "Duranta en Tampico: cuidados, poda y cómo hacer un seto florido" y quiero cotizar.',
    "errores-pasto-san-agustin-tampico": "Hola, vi el artículo de errores del pasto y quiero mantenimiento profesional",
    "fertilizacion-jardines-tampico-temporada-lluvias": 'Hola, leí su artículo "Fertilización de jardines en Tampico: guía completa para la temporada de lluvias" y quiero cotizar.',
    "ficus-elastica-cuidados-tampico": 'Hola, leí su artículo "Ficus Elastica en Tampico: guía completa para no matarlo (y que crezca espectacular)" y quiero cotizar.',
    "framboyan-delonix-regia-tampico": "Hola, vi el artículo de Flamboyán y quiero cotizar",
    "hongos-plantas-exceso-humedad-tampico": 'Hola, leí su artículo "Hongos en plantas por exceso de humedad en Tampico" y quiero cotizar.',
    "jardin-bajo-presupuesto-tampico": "Hola, mi presupuesto para jardín es $___",
    "jardin-en-macetas-terraza-tampico-guia": "Hola, vi el artículo de jardín en macetas y terrazas y quiero cotizar plantas",
    "jardin-vertical-tampico-guia": "Hola, vi el artículo de jardín vertical y quiero cotizar",
    "jardines-temporada-lluvias-tampico": 'Hola, leí su artículo "Jardines en temporada de lluvias en Tampico: guía completa de cuidados" y quiero cotizar.',
    "nortes-tampico-proteger-plantas-jardin": 'Hola, leí su artículo "Nortes en Tampico: cómo proteger tus plantas del viento y el frío" y quiero cotizar.',
    "palma-areca-tampico": "Hola, vi el artículo de Palma Areca y quiero cotizar",
    "palma-bambu-chamaedorea-tampico": "Hola, vi el artículo de Palma Bambú y quiero cotizar",
    "palma-bismarckia-bismarckia-nobilis-tampico": "Hola, vi el artículo de Palma Bismarckia y quiero cotizar",
    "palma-coco-plumoso-tampico": "Hola, vi el artículo de Palma Coco Plumoso y quiero cotizar",
    "palma-cola-de-zorro-wodyetia-bifurcata-tampico": "Hola, vi el artículo de Palma Cola de Zorro y quiero cotizar",
    "palma-kerpis-howea-forsteriana-tampico": "Hola, vi el artículo de Palma Kerpis y quiero cotizar",
    "palma-real-roystonea-regia-tampico": "Hola, vi el artículo de Palma Real y quiero cotizar",
    "palma-triangular-dypsis-decaryi-tampico": "Hola, vi el artículo de Palma Triangular y quiero cotizar",
    "palma-washingtona-tampico": "Hola, vi el artículo de Palma Washingtona y quiero cotizar",
    "palmas-mas-vendidas-tampico-precios": "Hola, vi la guía de palmas y quiero cotizar una específica",
    "palmas-tropicales-jardin-tampico": 'Hola, leí su artículo "Las 8 palmas más espectaculares para jardines en Tampico (y cuál es la correcta para ti)" y quiero cotizar.',
    "pasto-san-agustin-instalacion-mantenimiento": 'Hola, leí su artículo "Pasto San Agustín en Tampico: guía completa de instalación y mantenimiento" y quiero cotizar.',
    "pasto-san-agustin-vs-japones": 'Hola, leí su artículo "Pasto San Agustín vs japonés: la comparativa honesta para jardines en Tampico" y quiero cotizar.',
    "pasto-sintetico-calor-mexico": 'Hola, leí su artículo "¿El pasto sintético aguanta el calor de México?" y quiero cotizar.',
    "pasto-sintetico-para-perros": 'Hola, leí su artículo "Pasto sintético para perros y mascotas" y quiero cotizar.',
    "pasto-sintetico-vs-natural-tampico": 'Hola, leí su artículo "Pasto sintético vs natural en Tampico: cuál conviene" y quiero cotizar.',
    "plagas-comunes-jardin-tampico": 'Hola, leí su artículo "Plagas comunes del jardín en Tampico: cómo identificarlas y controlarlas" y quiero cotizar.',
    "plantas-interior-tampico": 'Hola, leí su artículo "Plantas de interior para casas en Tampico: las más recomendadas" y quiero cotizar.',
    "plantas-seguras-mascotas-jardin-tampico": "Hola, vi el artículo de plantas seguras para mascotas y quiero cotizar plantas",
    "plantas-resistentes-sal-golfo-tampico": 'Hola, leí su artículo "12 plantas resistentes a la sal del Golfo para jardines costeros en Tampico" y quiero cotizar.',
    "poda-arboles-palmas-tampico-guia": "Hola, vi el artículo de poda y necesito ayuda con mi jardín",
    "que-altura-de-pasto-sintetico-elegir": 'Hola, leí su artículo "¿Qué altura de pasto sintético elegir? 10, 18, 28 o 35 mm" y quiero cotizar.',
    "riego-automatico-tampico-roi": "Hola, quiero cotizar riego automático para mi jardín de ___ m²",
    "sistema-riego-automatico-conviene-tampico": 'Hola, leí su artículo "¿Conviene un sistema de riego automático en el clima tropical de Tampico?" y quiero cotizar.',
    "sistema-riego-automatizado-tampico": 'Hola, leí su artículo "Sistema de riego automático en Tampico: ¿vale la pena? Costos, tipos y en cuánto se paga" y quiero cotizar.',
    "temporada-huracanes-proteger-jardin-tampico": "Hola, vi el blog de Viveros Terra y quiero una cotización de poda preventiva",
    "tezontle-usos-jardin-tampico": 'Hola, leí su artículo "Tezontle rojo en el jardín: 8 usos que transforman cualquier espacio en Tampico" y quiero cotizar.',
    "tierra-negra-costal-camion-tampico": "Hola, quiero cotizar tierra negra para ___",
}

# Tema del artículo por palabras del slug, en orden: el primero que coincide da el `service` de GA4.
TEMAS_BLOG = (
    ("pasto-sintetico", ("sintetico", "perros")),
    ("materiales", ("tezontle", "tierra-negra", "mulch", "acolchado")),
    ("jardin", ("riego", "poda")),
    ("plantas", ("palma",)),
    ("pasto-natural", ("pasto", "cesped")),
    ("plantas", ("plantas", "arbol", "ficus", "buganvilia", "duranta", "framboyan")),
    ("jardin", ("jardin",)),
)


def tema_blog(slug):
    """Servicio del artículo según su slug; "general" si no coincide ningún tema."""
    return next((servicio for servicio, claves in TEMAS_BLOG if any(c in slug for c in claves)), "general")
