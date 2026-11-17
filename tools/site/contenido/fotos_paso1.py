"""Paso 1 de la revisión de fotos (aprobado por el dueño el 2026-11-17: «arranca paso 1»).

Seis agentes revisaron las 242 fotos de contexto; el dueño aprobó las correcciones seguras: alts que describen lo que se
ve, quitar fotos de una especie equivocada, mover cada foto a donde corresponde y usar fotos reales que no se usaban.
Las fotos que parecen hechas con IA o de banco de imágenes NO se retiran aquí (paso 2, espera la confirmación del dueño).
La regla «No elimines o cambies las fotos» sigue vigente para todo lo que no está en esta lista; los candados de
paridad la consultan para aceptar solo estos cambios.
"""

MOTIVO = ("Revisión de fotos, paso 1 (dueño, 2026-11-17): la foto no mostraba la especie o el tema del artículo, o el alt "
          "no describía lo que se ve.")

# Tarjetas del índice del blog (= portada del artículo): alt anterior -> (src nuevo o None si se queda sin foto, alt nuevo).
TARJETAS = {'Árboles para banqueta en Tampico': ('/img/jardineria-profesional-tampico-empresa.webp',
                                      'Jardinero arrodillado junto a un filodendro con tijeras de podar'),
 'Palma del Viajero en Tampico': ('/img/especie-palma-viajera-tampico.webp',
                                  'Palma del viajero (Ravenala madagascariensis) con sus hojas en abanico'),
 'Pasto San Agustín vs Japonés en Tampico': ('/img/pasto-en-rollo-san-agustin-tampico.webp',
                                             'Trabajador de Viveros Terra descarga pasto en rollo de una camioneta a '
                                             'una carretilla'),
 'Palma bambú Chamaedorea en Tampico': ('/img/especie-palma-bambu-chamaedorea-tampico.webp',
                                        'Palma bambú (Chamaedorea) en maceta'),
 'Jardín en Tampico pensado para perros y gatos': ('/img/jardineria-profesional-tampico-empresa.webp',
                                                   'Jardinero arrodillado junto a un filodendro con tijeras de '
                                                   'podar'),
 'Palma Bismarckia en Tampico': (None, None),
 'Palma Triangular Dypsis decaryi en Tampico': (None, None),
 'Proteger plantas de los nortes en Tampico': ('/img/plantas-tropicales-tampico-viveros.webp',
                                               'Alocasia de hojas grandes con helechos al pie frente a un muro '
                                               'verde'),
 'Duranta erecta en Tampico': ('/img/obra/terra/mantenimiento-jardines-02-recorte-de-seto-a-mano.webp',
                               'Colaborador de Viveros Terra recortando un seto con tijeras de mano'),
 'Palma Cola de Zorro Wodyetia bifurcata en Tampico': ('/img/especie-palma-cola-zorra-tampico.webp',
                                                       'Ilustración de palma cola de zorro (Wodyetia bifurcata)'),
 'Acolchado mulch en el jardín en Tampico': ('/img/plantacion-arbol-jardin-residencial-tampico.webp',
                                             'Carretilla con mulch y costales apilados'),
 'Cómo evitar encharcamientos en el jardín en Tampico': ('/img/tierra-negra-jardin-tampico.webp',
                                                         'Patio con tierra recién extendida y línea de riego, listo '
                                                         'para jardín'),
 'Palma Kerpis Howea forsteriana en Tampico': (None, None),
 'Palma Coco Plumoso Syagrus romanzoffiana en Tampico': ('/img/especie-coco-plumoso-tampico.webp',
                                                         'Hilera de palmas coco plumoso en bolsa listas para '
                                                         'plantar'),
 'Plagas comunes del jardín en temporada de lluvias en Tampico': ('/img/jardin-residencial-tropical-tampico.webp',
                                                                  'Jardín con plantas de hoja grande, seto y pasto '
                                                                  'junto a una casa moderna'),
 'Hongos en plantas por exceso de humedad en Tampico': ('/img/jardin-residencial-tropical-tampico.webp',
                                                        'Jardín con plantas de hoja grande, seto y pasto junto a una '
                                                        'casa moderna'),
 'Palma Areca Dypsis lutescens en Tampico': ('/img/especie-palma-areca-tampico.webp',
                                             'Palmas areca en jardineras negras junto a un ventanal'),
 'Cómo podar árboles y palmas en Tampico': ('/img/mantenimiento-jardines-poda-pasto-tampico.webp',
                                            'Jardinero con camisa de Viveros Terra cortando el pasto con podadora'),
 'Palma Washingtona Washingtonia robusta en Tampico': ('/img/especie-palma-washingtonia-tampico.webp',
                                                       'Hilera de palmas Washingtonia en maceta en un vivero'),
 'Jardín vertical con plantas ornamentales en Tampico': ('/img/plantas-ornamentales-tampico-viveros-terra.webp',
                                                         'Laurel rosa con flores rosas en una jardinera blanca'),
 'Palma Real Roystonea regia en Tampico': ('/img/palma-real-jardin-residencial-tampico.webp',
                                           'Palma alta de tronco liso en un jardín con pasto y muro blanco'),
 'Proteger jardín en temporada de huracanes Tampico': ('/img/mantenimiento-jardines-poda-pasto-tampico.webp',
                                                       'Jardinero con camisa de Viveros Terra cortando el pasto con '
                                                       'podadora'),
 'Precios pasto sintético México 2026': ('/img/pasto-sintetico/toscana-28.jpg',
                                         'Muestra de pasto sintético Toscana de 28 mm vista de cerca'),
 'Pasto sintético para perros y mascotas': ('/img/obra/terra/pasto-sintetico-03-patio-con-pasto-sintetico.webp',
                                            'Patio con pasto sintético recién instalado por Viveros Terra, con muro '
                                            'blanco y una palma'),
 'Qué altura de pasto sintético elegir': ('/img/pasto-sintetico/japones-35.jpg',
                                          'Muestra de pasto sintético Japonés de 35 mm vista desde arriba'),
 'Cómo instalar pasto sintético tú mismo': ('/img/pasto-sintetico-tampico-instalacion.webp',
                                            'Pasto sintético con cajete de tierra alrededor de un árbol, junto a un '
                                            'muro de piedra'),
 'Pasto sintético y calor en México': ('/img/pasto-sintetico-artificial-casa-tampico.webp',
                                       'Instalación de pasto frente a un edificio moderno con alberca'),
 'Precios jardín Tampico 2026': ('/img/diseno-jardines-tampico-proyecto.webp',
                                 'Jardín de sombra con alocasias, filodendro y helechos junto a un muro de piedra'),
 'Césped amarillo causas y soluciones Tampico': ('/img/instalacion-pasto-san-agustin-jardin-residencial-tampico-madero.webp',
                                                 'Jardín con pasto verde frente a una casa moderna con palmas'),
 'Palmas para jardines en Tampico': ('/img/obra/palmas-en-costal-vivero.webp',
                                     'Palmas con el cepellón envuelto en costal en el patio de Viveros Terra'),
 'Jardín bajo presupuesto Tampico': ('/img/jardin-residencial-plantas-pasto-tampico.webp',
                                     'Jardín residencial con arbustos, cintas variegadas, pasto y un árbol joven'),
 'Errores pasto San Agustín Tampico': ('/img/pasto-en-rollo-san-agustin-tampico.webp',
                                       'Trabajador de Viveros Terra descarga pasto en rollo de una camioneta a una '
                                       'carretilla'),
 'Tierra negra costal o camión Tampico': ('/img/tierra-negra-jardin-tampico.webp',
                                          'Patio con tierra recién extendida y línea de riego, listo para jardín'),
 'Sistema riego automático Tampico ROI': ('/img/instalacion-riego-tuberias-jardines-tampico.webp',
                                          'Cuadrilla con chaleco Terra instalando tubería y conexiones de riego en '
                                          'una zanja'),
 'Cómo medir plantas altura cepellón': ('/img/portadas/palmas-reales-mayoreo-vivero-tampico.webp',
                                        'Palmas con el cepellón envuelto, listas para entrega en el vivero')}

# Fotos del cuerpo de los artículos: ruta -> {src anterior: src nuevo o None si se quitó}.
CUERPO = {'/pasto-sintetico/perros': {'/img/pasto-sintetico-residencial-tampico.webp': '/img/obra/terra/pasto-sintetico-03-patio-con-pasto-sintetico.webp'},
 '/blog/palma-kerpis-howea-forsteriana-tampico': {'/img/especie-palma-kerpis-tampico.webp': None},
 '/blog/palmas-para-jardin-tampico': {'/img/plantas-tropicales-tampico-viveros.webp': '/img/obra/palmas-en-costal-vivero.webp'},
 '/blog/plantas-interior-tampico': {'/img/plantas-ornamentales-tampico-viveros-terra.webp': '/img/obra/terra/plantas-de-interior-03-hoja-ancha-con-brotes-rojos.webp'},
 '/blog/como-medir-plantas-altura-cepellon': {'/img/plantas-ornamentales-tampico-viveros-terra.webp': '/img/portadas/palmas-reales-mayoreo-vivero-tampico.webp'}}

# Alts del cuerpo de los artículos: alt anterior -> alt nuevo.
ALT_CUERPO = {'Palmas tropicales disponibles en Viveros Terra Tampico — Washingtona, Areca, Viajero y más': 'Palmas con el cepellón envuelto en costal en el patio de Viveros Terra',
 'Plantas ornamentales tropicales de interior disponibles en Viveros Terra Tampico': 'Ficus elástica de hojas oscuras con brotes rojos y ficus de hoja de violín al fondo, en bolsas de vivero',
 'Plantas ornamentales en Viveros Terra Tampico — palmas, árboles y plantas de jardín con diferentes medidas': 'Palmas con el cepellón envuelto, listas para entrega en el vivero',
 'Pasto sintético para perros y mascotas': 'Patio con pasto sintético recién instalado por Viveros Terra, con muro blanco y una palma',
 'Jardín vertical con plantas ornamentales en patio de Tampico': 'Laurel rosa con flores rosas en una jardinera '
                                                                 'blanca',
 'Jardín en Tampico pensado para perros y gatos': 'Jardinero arrodillado junto a un filodendro con tijeras de podar',
 'Jardín residencial tropical en Tampico durante temporada de lluvias': 'Jardín con plantas de hoja grande, seto y '
                                                                        'pasto junto a una casa moderna',
 'Jardín residencial tropical en Tampico con plantas de hoja ancha propensas a plagas en temporada de lluvias': 'Jardín '
                                                                                                                'con '
                                                                                                                'plantas '
                                                                                                                'de '
                                                                                                                'hoja '
                                                                                                                'grande, '
                                                                                                                'seto '
                                                                                                                'y '
                                                                                                                'pasto '
                                                                                                                'junto '
                                                                                                                'a '
                                                                                                                'una '
                                                                                                                'casa '
                                                                                                                'moderna',
 'Jardín residencial con plantas y pasto en Tampico — proyecto de bajo presupuesto': 'Jardín residencial con '
                                                                                     'arbustos, cintas variegadas, '
                                                                                     'pasto y un árbol joven',
 'Jardín residencial con pasto verde durante temporada de lluvias en Tampico': 'Jardín residencial con arbustos, '
                                                                               'cintas variegadas, pasto y un árbol '
                                                                               'joven',
 'Instalación de sistema de riego automático con tuberías en jardín de Tampico': 'Cuadrilla con chaleco Terra '
                                                                                 'instalando tubería y conexiones de '
                                                                                 'riego en una zanja',
 'Instalación de pasto San Agustín en jardín residencial en Tampico y Madero': 'Jardín con pasto verde frente a una '
                                                                               'casa moderna con palmas',
 'Palma bambú Chamaedorea seifrizii en maceta en Tampico': 'Palma bambú (Chamaedorea) en maceta',
 'Palma Areca Dypsis lutescens en Tampico': 'Palmas areca en jardineras negras junto a un ventanal',
 'Palma Coco Plumoso (Syagrus romanzoffiana) en jardín residencial en Tampico': 'Hilera de palmas coco plumoso en '
                                                                                'bolsa listas para plantar',
 'Proyecto de diseño de jardín en Tampico — jardín residencial con pasto, plantas y palmas': 'Jardín de sombra con '
                                                                                             'alocasias, filodendro '
                                                                                             'y helechos junto a un '
                                                                                             'muro de piedra',
 'Pasto San Agustín en rollo instalado en jardín de Tampico': 'Trabajador de Viveros Terra descarga pasto en rollo '
                                                              'de una camioneta a una carretilla',
 'Tierra negra vegetal para jardín en Tampico — costales y camión volteo disponibles en Viveros Terra': 'Patio con '
                                                                                                        'tierra '
                                                                                                        'recién '
                                                                                                        'extendida y '
                                                                                                        'línea de '
                                                                                                        'riego, '
                                                                                                        'listo para '
                                                                                                        'jardín',
 'Sistema de riego automatizado eficiente para jardín en Tampico': 'Técnico ajustando un aspersor emergente en un '
                                                                   'pasto con riego automático'}

# og:image e image del artículo (slug -> src): la portada nueva, o una foto real de palmas de Terra si se quedó sin foto.
OG = {'cuidados-palma-del-viajero-ravenala': '/img/especie-palma-viajera-tampico.webp',
 'palmas-para-jardin-tampico': '/img/obra/palmas-en-costal-vivero.webp',
 'duranta-erecta-tampico-cuidados-seto': '/img/obra/terra/mantenimiento-jardines-02-recorte-de-seto-a-mano.webp',
 'como-medir-plantas-altura-cepellon': '/img/portadas/palmas-reales-mayoreo-vivero-tampico.webp',
 'acolchado-mulch-jardin-tampico': '/img/plantacion-arbol-jardin-residencial-tampico.webp',
 'palma-triangular-dypsis-decaryi-tampico': '/img/obra/palmas-en-costal-vivero.webp',
 'palma-kerpis-howea-forsteriana-tampico': '/img/obra/palmas-en-costal-vivero.webp',
 'palma-bismarckia-bismarckia-nobilis-tampico': '/img/obra/palmas-en-costal-vivero.webp',
 'ficus-elastica-cuidados-tampico': '/img/obra/terra/plantas-de-interior-03-hoja-ancha-con-brotes-rojos.webp',
 'buganvilia-tampico-cuidados-floracion': '/img/obra/terra/plantas-palmas-arboles-04-arbustos-con-flor-fucsia.webp',
 'plantas-interior-tampico': '/img/obra/terra/plantas-de-interior-03-hoja-ancha-con-brotes-rojos.webp'}


def tarjeta(src, alt):
    """(src, alt) que debe publicar hoy una tarjeta del índice que en la captura tenía (src, alt); src None = sin foto."""
    return TARJETAS.get(ANTERIORES.get(alt, alt), (src, alt))


# Alts de tarjetas que cambiaron antes de este paso (la captura conserva el de entonces).
ANTERIORES = {"Palmas más vendidas Tampico precios": "Palmas para jardines en Tampico"}


def cuerpo(ruta, src, alt):
    """(src, alt) que debe publicar hoy una foto del cuerpo; src None = se quitó."""
    nuevo = CUERPO.get(ruta, {}).get(src, src)
    return nuevo, ALT_CUERPO.get(alt, alt)
