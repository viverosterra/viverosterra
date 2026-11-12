"""Contenido de /vivero-tampico ("Visítanos"; SEO fase 2b, 2026-11-11, mapa de palabras clave G3 y §4a): la página local
del vivero, la del perfil de Google. Solo datos: la plantilla es tools/site/plantillas/pilar.py (antes, la propia
plantillas/vivero.py). La portada es la de siempre (misma foto, srcset y alt: regla del dueño, no se tocan las fotos).

Todo de datos.py y de lo que el sitio ya publica: domicilio, referencia, horario (y los días cerrados de
datos.FESTIVOS), precios de datos.PRECIOS, garantía de plantas, cobertura de entrega (Tampico, Madero y Altamira, con el
costo según la colonia), anticipo, factura, mayoreo de pasto y de palmas, y la temporada de Nochebuenas de
datos.NOCHEBUENAS. Fuera, sin respaldo en el repositorio: estacionamiento, distancias o minutos desde Tampico o
Altamira, avenidas distintas de la Av. Álvaro Obregón, tiempos de entrega y visitas sin costo. Desde la fase 0 quedaron
fuera "Lun–Sáb 9am–6pm" (el sábado cierra a las 14 h), "Variedades en stock", "te decimos si la tenemos disponible",
"precios orientativos", "precios más bajos" y "+18 años".

JSON-LD: el nodo completo del negocio (entidad.negocio(), que según entidad.py vive en la home y aquí) una sola vez, el
WebPage de la página con about y mainEntity → #negocio (por @id, sin repetir el nodo), el ItemList de categorías de la
fase 1, el FAQPage y las migas (los dos de la plantilla).
"""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from componentes_util import META_AUTOR_RETIRADA
from contenido import catalogo_datos
from contenido import respuestas
from contenido import seo

P = datos.PRECIOS
NB = datos.NOCHEBUENAS
SITE = datos.SITIO
RUTA = "/vivero-tampico"
URL = f"{SITE}{RUTA}"
FOTO = {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
        "srcset": "/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, /img/portadas/arboles-tampico-viveros-terra.webp 960w",
        "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 960, "alto": 1280,
        "alt": "Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico", "numero": 1,
        "lugar": "Siembra de árboles y plantas en Tampico", "etapa": "Equipo Viveros Terra"}
HORARIO = "Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h"
MESES = {"12": "diciembre", "01": "enero"}
CERRADO = "El domingo está cerrado, igual que el " + " y el ".join(
    f"{int(f[3:])} de {MESES[f[:2]]}" for f in datos.FESTIVOS) + "."
REFERENCIA = f"{datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}"
MAPAS = (f'<a data-cta="vivero:mapas-google" href="{datos.MAPS_URL}" target="_blank" rel="noopener">Abrir en Google Maps</a> · '
         f'<a data-cta="vivero:mapas-apple" href="https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&amp;q=Viveros%20Terra" '
         'target="_blank" rel="noopener">Apple Maps</a>')
DONDE = (f"Viveros Terra tiene su vivero en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero, con {datos.VARIEDADES} variedades "
         "de plantas, palmas, árboles ornamentales y plantas de interior, especies adaptadas al clima cálido-húmedo del Golfo de México.")
MENSAJE = mensajes_paginas.UTILITARIAS["vivero"]
MENSAJE_PLANTA = mensajes_paginas.UTILITARIAS["vivero_planta"]
ENTREGA = ("Entregamos en Tampico, Ciudad Madero y Altamira; te confirmamos el costo por WhatsApp según tu colonia.")

# SEO fase 1: las categorías del vivero como lista de sus páginas (antes, un OfferCatalog con tres Product sin precio ni
# foto: Google los marca como productos inválidos y no hay un precio real que ponerles). Fase 2b: las mismas que se ven.
CATEGORIAS = (
    ("Palmas Tropicales", "/palmas-tropicales-tampico",
     f"Palma del viajero, areca, coco, kentia, washingtonia y más. {datos.PALMAS_PRECIO}."),
    ("Plantas Ornamentales", "/plantas-para-jardin-tampico",
     "Heliconias, bromelias, crotos, ficus, bugambilias y decenas de especies para jardines, terrazas y arriates de sol "
     "o de sombra."),
    ("Plantas de interior", "/plantas-de-interior-tampico",
     "Ficus lyrata, monstera, zamioculca, sansevieria y palma areca para casas y oficinas con poca luz y aire "
     "acondicionado."),
    ("Árboles para Jardín", "/arboles-ornamentales-tampico",
     f"Árboles ornamentales, frutales y de sombra: flamboyán desde {dinero(P['flamboyan'])}, jacaranda, palo de rosa, "
     "magnolia y más."),
    ("Árboles para banqueta", "/arboles-para-banqueta-tampico",
     "Olivo negro, neem, fresno y otras especies de raíz profunda para frentes, banquetas y camellones."),
    ("Pasto en rollo", "/pasto-en-rollo-tampico",
     f"Pasto San Agustín a {dinero(P['pasto_solo_m2'])}/m² solo el pasto (no lleva IVA). Llega al vivero "
     f"{datos.LLEGADA_PASTO}."),
    ("Materiales para jardín", None,
     '<a href="/tierra-negra-vegetal-tampico">Tierra negra</a>, <a href="/tezontle-rojo-tampico">tezontle rojo</a>, <a href="/marmol-blanco-tampico">mármol '
     'blanco</a> y <a href="/piedra-bola-rio-tampico">piedra bola de río</a> por costal o a granel.'),
    ("Catálogo completo", "/catalogo",
     f"{len(catalogo_datos.ESPECIES)} especies con foto, luz, riego y altura. Agrega lo que te interesa y cotiza todo en "
     "un WhatsApp."),
)
CATEGORIAS_LD = {"@type": "ItemList", "name": "Categorías del vivero", "itemListElement": [
    {"@type": "ListItem", "position": n, "name": nombre, "url": f"{SITE}{ruta}"}
    for n, (nombre, ruta) in enumerate(((nombre, ruta) for nombre, ruta, _t in CATEGORIAS if ruta), 1)]}
# datos.GARANTIA_PLANTAS sin su "(ver condiciones)" final, que aquí va como enlace (tests/test_seo_f2b.py lo amarra).
GARANTIA = datos.GARANTIA_PLANTAS.removesuffix(" (ver condiciones).")

HECHOS = (
    {"titulo": f"{datos.VARIEDADES} variedades", "texto": "Plantas, palmas y árboles en el vivero."},
    {"titulo": str(datos.DESDE), "texto": f"Año de fundación, en {datos.CIUDAD}."},
    {"titulo": "30 días de garantía",
     "texto": 'En las plantas que sembramos nosotros. <a href="/politicas#garantia-plantas">Ver condiciones</a>.'},
    {"titulo": "Domicilio",
     "texto": f"{datos.DOMICILIO_COMPLETO}. {datos.REFERENCIA}. Es el único domicilio del negocio."},
    {"titulo": "Horario", "texto": f"{datos.HORARIO}. {CERRADO}"},
    {"titulo": "Antes de venir",
     "texto": (f"Escríbenos por WhatsApp qué buscas y el tamaño: {datos.PROMESA[0].lower()}{datos.PROMESA[1:]}. "
               f"{datos.GOOGLE}.")},
)
LLEGAR = (
    {"titulo": "Desde Tampico",
     "texto": (f"Ve hacia Ciudad Madero hasta la Av. Álvaro Obregón. El vivero está en el {datos.CALLE_CORTA.split()[1]} "
               f"Sur, {REFERENCIA}. Para la ruta desde tu colonia, ábrelo en el mapa.")},
    {"titulo": "Desde Altamira",
     "texto": (f"Ve hacia Ciudad Madero y busca la Av. Álvaro Obregón; la referencia es la misma: {REFERENCIA}. Si "
               "vienes por pasto o por varias plantas, avísanos antes por WhatsApp.")},
    {"titulo": "En Ciudad Madero",
     "texto": (f"Estamos en la {datos.COLONIA}, {datos.CP}. Si ya conoces el Walmart de Madero, el vivero está "
               "enfrente.")},
    {"titulo": "En el mapa", "texto": f"{datos.CALLE}, {datos.COLONIA}, Ciudad Madero, Tamaulipas. {MAPAS}."},
)
ENTREGAS = (
    {"titulo": "Entrega a domicilio", "texto": ENTREGA},
    {"titulo": "Recoge en el vivero",
     "texto": f"Pasa por tu pedido a {datos.CALLE_CORTA}, {REFERENCIA}, en el horario del vivero."},
    {"titulo": "Siembra con garantía",
     "texto": (f"Garantía de {GARANTIA}. Si te las llevas y las siembras tú, no aplica la garantía de arraigo. "
               '<a href="/politicas#garantia-plantas">Condiciones de la garantía</a>.')},
    {"titulo": "Pago y factura",
     "texto": f"{datos.ANTICIPO} Facturamos con {datos.FACTURA} a persona física o moral."},
)
MAYOREO = (
    {"titulo": '<a href="/palmas-mayoreo-proyectos">Palmas al mayoreo</a>',
     "texto": ("Para desarrollos, hoteles y obra pública en Tamaulipas, el norte de Veracruz y San Luis Potosí, con "
               f"areca desde {dinero(P['palma_desde'])}. El flete se cotiza por ruta y volumen.")},
    {"titulo": '<a href="/mayoreo-pasto-tampico">Pasto al mayoreo</a>',
     "texto": (f"Desde {dinero(P['pasto_mayoreo_m2'])}/m² solo el pasto, en pedidos de {P['pasto_mayoreo_minimo_m2']} m² o "
               "más (no lleva IVA), con entregas por etapas.")},
    {"titulo": '<a href="/empresas">Áreas verdes para empresas</a>',
     "texto": f"Mantenimiento, pasto, palmas y riego con REPSE {datos.REPSE} y factura {datos.FACTURA}."},
)
TEMPORADA = (
    {"titulo": f'<a href="{NB["ruta"]}">Nochebuenas de temporada</a>',
     "texto": (f"En temporada, Nochebuena {', '.join(v.lower() for v in NB['variedades'][:-1])} y "
               f"{NB['variedades'][-1].lower()} en maceta, colgante y macetón, con precio por volumen, factura y entrega "
               "en Tampico, Madero y Altamira.")},
    {"titulo": '<a href="/jardineria-ciudad-madero">Jardinería en Ciudad Madero</a>',
     "texto": ("Desde el vivero instalamos pasto, diseñamos y damos mantenimiento en Playa Miramar y el resto de "
               "Madero.")},
    {"titulo": "Pasto instalado y jardines",
     "texto": (f'<a href="/pasto-en-rollo-tampico">Pasto en rollo instalado</a> desde {dinero(P["pasto_instalado_m2"])}/m², '
               f'<a href="/diseno-jardines-tampico">diseño de jardines</a> desde {dinero(P["diseno"])} y '
               f'<a href="/mantenimiento-jardines-tampico">mantenimiento</a> desde {dinero(P["mantenimiento_mes"])} al mes. '
               f"{datos.TERRENO_LISTO_CORTO}")},
)
PREGUNTAS = (
    ("¿Dónde está el vivero en Tampico?",
     f"Viveros Terra está en {datos.CALLE}, {datos.COLONIA}, Ciudad Madero — frente al Walmart de Madero. Atendemos de "
     f"{HORARIO.lower()}."),
    ("¿Cuántas variedades de plantas tienen disponibles?",
     "Contamos con más de 200 variedades entre plantas ornamentales, palmas tropicales y árboles para jardín."),
    ("¿Hacen entregas a domicilio en Tampico?",
     "Sí, realizamos entregas en toda la zona metropolitana de Tampico, incluyendo Ciudad Madero y Altamira. Contáctanos "
     "por WhatsApp para coordinar la entrega y conocer su costo según tu colonia."),
    ("¿Puedo comprar plantas al mayoreo para mi proyecto?",
     "Sí. Atendemos tanto a clientes particulares como a constructoras, arquitectos, hoteles y empresas. Escríbenos por "
     "WhatsApp con tu requerimiento y te cotizamos por volumen."),
    ("¿Qué horario tiene el vivero?", f"{HORARIO}. {CERRADO}"),
    ("¿Cómo llego al vivero desde Tampico o Altamira?",
     f"Por la Av. Álvaro Obregón, en Ciudad Madero: el vivero está en el número 209 Sur, {REFERENCIA}. En Google Maps "
     "aparece como Viveros Terra."),
    ("¿Las plantas tienen garantía?",
     f'Sí: {GARANTIA} (<a href="/politicas#garantia-plantas">ver condiciones</a>). Si te las llevas y las siembras tú, '
     "no aplica la garantía de arraigo."),
    ("¿Cuánto cuesta el pasto en el vivero?",
     f"El pasto San Agustín cuesta {dinero(P['pasto_solo_m2'])}/m² solo el pasto (no lleva IVA) y desde "
     f"{dinero(P['pasto_instalado_m2'])}/m² instalado ({datos.TERRENO_LISTO_CORTO[0].lower()}"
     f"{datos.TERRENO_LISTO_CORTO[1:-1]}). Llega al vivero {datos.LLEGADA_PASTO}."),
    ("¿Viveros Terra y Viveros Terra Tampico son el mismo vivero?",
     f"Sí. «{datos.NOMBRE_ALTERNO}» es el nombre con que aparece el mismo negocio en algunos perfiles; el domicilio es "
     f"uno solo: {datos.DOMICILIO_COMPLETO}."),
)
# SEO fase 0 (mapa de palabras clave, 2026-11-10): título de 60 y descripción de 153; el mismo texto va en Open Graph.
TITULO = f"Vivero en Tampico y Cd. Madero: {datos.VARIEDADES} Plantas | {datos.NOMBRE}"
DESCRIPCION = ("Vivero en Cd. Madero, frente a Walmart: más de 200 variedades de plantas, palmas y árboles. "
               f"{datos.HORARIO}. Ve cómo llegar y visítanos.")
CONTENIDO = {
    "respuesta": respuestas.de(RUTA),  # SEO fase 1: respuesta directa bajo la portada
    "tipo": "vivero",
    # La etiqueta del hero nombra el producto también en celular (regla de terra-util.css, test_cierre_etapa2).
    "clase_body": "vt-pagina vt-util",
    "meta": {"title": TITULO, "description": DESCRIPCION,
             "robots": "index, follow", "canonical": URL,
             "og": (("og:type", "website"), ("og:url", URL),
                    ("og:title", TITULO), ("og:description", DESCRIPCION),
                    ("og:image", f"{SITE}/img/plantas-tropicales-tampico-viveros.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "migas": (("Inicio", "/"), ("Vivero en Tampico", None)),
    "portada": {"kicker": "Tampico · Madero · Altamira", "h1": 'Vivero en Tampico <span class="vt-serif">y Ciudad Madero, desde 2007</span>',
                "lede": f"Pasto, plantas, palmas, árboles y materiales para jardín en {datos.CALLE_CORTA}, Cd. Madero, frente a Walmart.",
                "etiqueta": {"codigo": "Vivero", "aviso": "", "nombre": "Palmas", "antes": "desde", "monto": dinero(P["palma_desde"]),
                             "unidad": "", "filas": (("Pasto", f"{dinero(P['pasto_solo_m2'])}/m²"), ("Plantas", "por tamaño"))},
                "mensaje": MENSAJE, "foto": FOTO, "pos": "50% 66%",
                "enlaces": (("Cómo llegar", datos.MAPS_URL, "vivero:mapas", 'target="_blank" rel="noopener"'),),
                "dato": f"{datos.VARIEDADES} variedades en el vivero"},
    "secciones": (
        {"clase": "fichas", "rotulo": "Dónde estamos", "id": "vt-h-donde", "ancla": "donde",
         "titulo": 'Viveros Terra en Ciudad Madero, <span class="vt-serif">frente a Walmart</span>', "lede": DONDE,
         "items": HECHOS},
        {"clase": "fichas", "rotulo": "Categorías", "id": "vt-h-categorias", "ancla": "categorias",
         "titulo": 'Categorías <span class="vt-serif">en el vivero</span>',
         "lede": ("Plantas adaptadas al clima cálido-húmedo de Tampico. Cada categoría tiene su página con especies, "
                  "cuidados y precio por tamaño."),
         "items": tuple({"titulo": f'<a href="{ruta}">{nombre}</a>' if ruta else nombre, "texto": texto}
                        for nombre, ruta, texto in CATEGORIAS),
         "cta": (MENSAJE_PLANTA, "Preguntar por una planta")},
        {"clase": "fichas", "rotulo": "Visítanos", "id": "vt-h-llegar", "ancla": "como-llegar",
         "titulo": 'Cómo llegar <span class="vt-serif">al vivero</span>',
         "lede": (f"El vivero está sobre la Av. Álvaro Obregón, en Ciudad Madero, {REFERENCIA}. Abre de "
                  f"{HORARIO[0].lower()}{HORARIO[1:]}."),
         "items": LLEGAR},
        {"clase": "fichas", "rotulo": "Entregas", "id": "vt-h-entregas", "ancla": "entregas",
         "titulo": 'Entrega a domicilio <span class="vt-serif">o recoge en el vivero</span>',
         "lede": "Coordinamos cada entrega por WhatsApp, con su costo según tu colonia.",
         "items": ENTREGAS, "cta": (MENSAJE, "Cotizar por WhatsApp")},
        {"clase": "fichas", "rotulo": "Mayoreo", "id": "vt-h-mayoreo", "ancla": "mayoreo",
         "titulo": 'Mayoreo <span class="vt-serif">para obras y empresas</span>',
         "lede": "Atendemos a constructoras, arquitectos, hoteles y empresas, con cotización por volumen.",
         "items": MAYOREO},
        {"clase": "fichas", "rotulo": "Temporada", "id": "vt-h-temporada", "ancla": "temporada",
         "titulo": 'De temporada <span class="vt-serif">y desde el vivero</span>',
         "lede": "Lo que cambia con la temporada y los servicios que salen del vivero hacia tu jardín.",
         "items": TEMPORADA},
    ),
    "faq": {"titulo": 'Preguntas frecuentes <span class="vt-serif">sobre el vivero</span>', "preguntas": PREGUNTAS},
    "cierre": {"titulo": '¿Buscas una planta <span class="vt-serif">específica?</span>',
               "lede": "Escríbenos con el nombre o una foto y te decimos qué opciones hay para tu espacio y el clima de Tampico.",
               "mensaje": MENSAJE_PLANTA,
               # Reescritura 10 (Entrega B de experiencia): el botón dice qué se pregunta.
               "texto": "Preguntar si la tienen"},
    "jsonld": {
        "speakable": entidad.SPEAKABLE,
        "nodos": (entidad.negocio(), CATEGORIAS_LD,
                  {"@type": "WebPage", "@id": URL, "url": URL, "name": TITULO, "about": dict(entidad.REF),
                   "mainEntity": dict(entidad.REF)}),
    },
}
M_CATALOGO = ("SEO fase 1: el OfferCatalog traía tres Product sin precio ni foto (inválidos para Google) y no hay un precio "
              "real que ponerles; las categorías van como ItemList con el enlace a su página.")
PARIDAD = {
    "reemplazos": {"Viveros Terra · Tampico": "Viveros Terra en Ciudad Madero, frente a Walmart",
                   "Categorías disponibles en el vivero": "Categorías en el vivero",
                   "Explora el catálogo completo del vivero": "Catálogo completo",
                   "¿Buscas una planta específica?": "¿Buscas una planta específica?"},
    "retirados": {},
    "meta_retirada": META_AUTOR_RETIRADA,
    "meta": seo.paridad(TITULO, DESCRIPCION, {"og:description": (DESCRIPCION, "Sin “Productor directo”: el dueño no lo ha confirmado y 2d y 2f ya lo retiraron.")}),
    "jsonld": {tipo: M_CATALOGO for tipo in ("OfferCatalog", "Offer", "Product")},
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). «Cómo llegar» pasa de botón a enlace de texto; la colonia sale de la entrada (sigue en «En corto» y en «Cómo llegar»).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: mensaje del hero con sus huecos ___ y la colonia; botón del cierre «Preguntar si la tienen» (reescritura 10).'
