"""Contenido de la home (/). Solo datos: la plantilla es tools/site/plantillas/inicio.py.

Copy de la maqueta aprobada (docs/diseno/hibrido/index.html) con los datos vivos de datos.py. Título, descripción,
canonical, Open Graph y JSON-LD de negocio y migas se conservan como estaban publicados (los títulos se reescriben en la
Etapa 3 y el grafo único llega en la Etapa 4). PARIDAD dice a dónde fue cada encabezado, pregunta, precio o enlace de la
página anterior que ya no aparece igual (prueba: tools/site/tests/test_paridad.py).
"""
import datos
from componentes import dinero

P = datos.PRECIOS
MINIMO = P["pasto_mayoreo_minimo_m2"]
EMPRESAS = f"{', '.join(datos.CLIENTES_B2B[:-1])} y {datos.CLIENTES_B2B[-1]}"
# Spec del hero (2026-11-09, §2): las metas ya no dicen "gratis"; dicen lo que sí pasa (precio a la vista y la promesa).
COTIZA = f"Cotiza por WhatsApp: {datos.PROMESA[0].lower()}{datos.PROMESA[1:]}."
# Revisión (2026-11-09): sin "con IVA" (el pasto sin instalar no lleva IVA) y en 155 caracteres o menos.
DESCRIPCION = (f"Pasto San Agustín desde ${P['pasto_solo_m2']}/m², jardines y mantenimiento en Tampico. "
               f"Precios a la vista. {COTIZA}")

META = {
    "title": "Viveros Terra · Jardinería, Pasto en Rollo y Paisajismo en Tampico",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": f"{datos.SITIO}/",
    "og": (
        ("og:type", "website"),
        ("og:url", datos.SITIO),
        ("og:title", "Viveros Terra · Jardinería y Pasto en Rollo en Tampico"),
        ("og:description", DESCRIPCION),
        ("og:image", f"{datos.SITIO}/img/jardin-diseno-paisajismo-pasto-san-agustin-tampico-og.webp"),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:locale", "es_MX"),
        ("og:site_name", "Viveros Terra Tampico"),
    ),
    "alternos": (("es-MX", datos.SITIO),),
    # Twitter Card como estaba publicada en main, salvo la descripción (sin "gratis").
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", "Viveros Terra | Jardinería y Pasto en Rollo en Tampico"),
        ("twitter:description", f"Pasto en rollo, diseño de jardines y mantenimiento en Tampico. {COTIZA}"),
        ("twitter:image", f"{datos.SITIO}/img/jardineria-areas-verdes-tampico.webp"),
    ),
}

NEGOCIO = {
    "@type": "LocalBusiness",
    "@id": f"{datos.SITIO}/#negocio",
    "foundingDate": datos.FUNDACION,
    "name": datos.NOMBRE,
    "hasMap": datos.MAPS_URL,
    "description": ("Especialistas en pasto en rollo San Agustín, venta e instalación de pasto sintético, diseño de "
                    "jardines, sistemas de riego y mantenimiento de áreas verdes en Tampico, Ciudad Madero y Altamira, "
                    "Tamaulipas."),
    "url": datos.SITIO,
    "telephone": datos.TELEFONO_TEL,
    "email": datos.CORREO_FORMULARIOS,
    "image": f"{datos.SITIO}/img/jardineria-areas-verdes-tampico.jpg",
    "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"},
    "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": list(dias) if len(dias) > 1 else dias[0], "opens": abre,
         "closes": cierra} for dias, abre, cierra in datos.HORARIO_LD],
    "sameAs": ["https://www.facebook.com/viverosterra/", "https://www.instagram.com/viverosterramx",
               "https://www.linkedin.com/company/viveros-terra-tampico"],
    "priceRange": "$$",
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Pánuco", "Tuxpan", "Victoria", "Tampico Centro",
                   "Madero Norte", "Madero Sur", "Altamira Industrial"],
}

MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": i, "name": nombre, "item": f"{datos.SITIO}{ruta}"}
    for i, (nombre, ruta) in enumerate((("Inicio", ""), ("Pasto en Rollo Tampico", "/pasto-en-rollo-tampico"),
                                         ("Plantas y Palmas", "/plantas-palmas-arboles-tampico"),
                                         ("Diseño de Jardines", "/diseno-jardines-tampico"),
                                         ("Catálogo", "/catalogo")), 1)]}

OBRA = "/img/obra"

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Dónde comprar pasto en rollo en Tampico?",
     f"En Viveros Terra: {datos.DOMICILIO_COMPLETO}, {datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}. Somos vivero "
     f"productor de pasto San Agustín en la zona conurbada de Tampico desde {datos.DESDE}, con {datos.INSTALACIONES} "
     "instalaciones. Entregamos en Tampico, Madero y Altamira."),
    ("¿Qué pasto es mejor para el clima de Tampico?",
     "El pasto San Agustín (<i>Stenotaphrum secundatum</i>): resiste el calor y la humedad del Golfo, tolera media "
     "sombra y pide poco mantenimiento. Para jardines finos conviene el japonés y para alto tráfico, el Bermuda."),
    ("¿Cuánto cuesta el mantenimiento de jardín en Tampico?",
     f"Los planes inician desde ${P['mantenimiento_mes']}/mes para jardines residenciales. El precio depende del "
     "tamaño y la frecuencia, e incluye poda, fertilización y control de plagas. "
     '<a href="/mantenimiento-jardines-tampico">Ver los planes de mantenimiento</a>.'),
    ("¿El diseño de jardín tiene costo?",
     f"El Plan Terra de diseño cuesta desde {dinero(P['diseno'])}. En los planes Esencial y Completo, el costo del diseño "
     "se descuenta íntegramente si contratas la ejecución con nosotros. "
     '<a href="/diseno-jardines-tampico">Ver los planes de diseño</a>.'),
    ("¿Trabajan con empresas e industria?",
     f"Sí. Tenemos registro REPSE {datos.REPSE}, facturamos {datos.FACTURA} y entregamos por etapas según el avance de "
     f"obra. Nos han contratado {EMPRESAS}. "
     f'<a href="/mayoreo-pasto-tampico">Mayoreo de pasto</a> desde {MINIMO} m².'),
)

# Opiniones reales con nombre, publicadas con permiso (decisión del dueño, 2026-11-07): viven en datos.OPINIONES.
TESTIMONIOS = datos.OPINIONES

# Franja de temporada bajo la portada: se retira sola en postemporada (spec de Nochebuenas, §7).
_NB = datos.NOCHEBUENAS
TEMPORADA = None if _NB["modo"] == "postemporada" else {
    "aviso": "Temporada de Nochebuenas", "titulo": f"Nochebuenas {_NB['temporada']}", "estado": "Pedidos abiertos",
    "texto": (f"Desde {dinero(_NB['productos'][0]['precios'][0])} en menudeo y desde "
              f"{dinero(min(p['precios'][-1] for p in _NB['productos']))} por volumen"),
    "cta": "Ver nochebuenas", "href": _NB["ruta"], "hasta": _NB["preventa"]["hasta"],
}

CONTENIDO = {
    "meta": META,
    "temporada": TEMPORADA,
    "jsonld": {"negocio": NEGOCIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "portada": {
        "kicker": f"Vivero y cuadrilla propia · Desde {datos.DESDE}",
        "h1": "Pasto, jardines y plantas en Tampico.",
        "lema": "Con el precio por delante.",
        "lede": (f"Pasto San Agustín en rollo, diseño de jardines y {datos.VARIEDADES} variedades de plantas, en Tampico, "
                 "Madero y Altamira."),
        "etiqueta": {
            "codigo": "Pasto · 01", "aviso": f"Precios {datos.ANIO}", "nombre": "Pasto San Agustín",
            "cientifico": "Stenotaphrum secundatum", "antes": "San Agustín instalado · desde",
            # "con IVA" va en la banda del instalado; la fila de solo pasto no lo lleva (dueño, 2026-11-10).
            "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m² con IVA",
            "filas": (("Solo pasto, tú lo instalas", f"{dinero(P['pasto_solo_m2'])} /m²"),),
            "nota": (f"Ejemplo: 8 × 6 m = 48 m² instalado × {dinero(P['pasto_instalado_m2'])} = "
                     f"{dinero(48 * P['pasto_instalado_m2'])}."),
        },
        "mensaje": datos.MENSAJES["general"],
        "foto": {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin.webp",
                 "srcset": (f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp 640w, "
                            f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin.webp 1024w"),
                 "sizes": "(min-width:1024px) 40vw, 100vw", "ancho": 1024, "alto": 1536,
                 "alt": "Integrante de la cuadrilla de Viveros Terra tendiendo rollos de pasto San Agustín en un jardín.",
                 "numero": 1, "lugar": "Zona Tampico–Madero · tendido de tepes", "etapa": "Tepe de 40 × 60 cm"},
    },
    "que_hacemos": {
        "titulo": "Cinco formas de trabajar con nosotros, cada una con su precio.",
        "lede": ("Pasto, jardinería, plantas y obra para empresas: para que llegues a la plática sabiendo cuánto cuesta. "
                 "Donde dice “desde”, el total depende de tus metros y del terreno."),
        "items": (
            {"titulo": "Pasto natural", "servicio": "pasto-natural", "cotizar": "pasto",
             "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"San Agustín en rollo, cortado para tu pedido. {dinero(P['pasto_solo_m2'])}/m² solo pasto; "
                       "instalado en un día."),
             "desde": dinero(P["pasto_instalado_m2"]), "unidad": "/m² instalado"},
            {"titulo": "Pasto sintético", "servicio": "pasto-sintetico", "cotizar": "sintético",
             "href": "/pasto-sintetico",
             "img": "/img/pasto-sintetico/galeria/toscana-28-1-sm.webp", "ancho": 420, "alto": 560,
             "texto": (f"9 modelos con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}. El envío se cobra por "
                       'rollo, según tu estado. ¿En Tampico? <a href="/pasto-sintetico-tampico">Lo instalamos</a>.'),
             "desde": dinero(P["sintetico_tienda_m2"]), "unidad": "/m² material"},
            {"titulo": "Diseño, mantenimiento y riego", "servicio": "jardin", "cotizar": "jardín",
             "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": (f'Plan Terra de <a href="/diseno-jardines-tampico">diseño</a> desde {dinero(P["diseno"])}. '
                       "Mantenimiento con poda, fertilización y control de plagas. "
                       f'<a href="/sistema-riego-tampico">Riego automático</a> desde {dinero(P["riego_m2"][0])}/m².'),
             "desde": dinero(P["mantenimiento_mes"]), "unidad": "/mes"},
            {"titulo": "Plantas y palmas", "servicio": "plantas", "cotizar": "plantas",
             "href": "/plantas-palmas-arboles-tampico",
             "img": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961,
             "texto": (f"{datos.VARIEDADES} variedades en el vivero. Las que sembramos nosotros llevan 30 días de "
                       "garantía de arraigo, con el riego indicado."),
             "desde": dinero(P["palma_desde"]), "unidad": "palma chica"},
            {"titulo": "Empresas y constructoras", "servicio": "empresas", "cotizar": "proyecto",
             "href": "/mayoreo-pasto-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": (f"Mayoreo de pasto (solo pasto) desde {MINIMO} m², "
                       '<a href="/palmas-mayoreo-proyectos">palmas para proyectos</a>, mantenimiento recurrente y '
                       f"entrega por etapas. REPSE {datos.REPSE} y {datos.FACTURA}."),
             "desde": dinero(P["pasto_mayoreo_m2"]), "unidad": "/m² mayoreo"},
        ),
    },
    "medidor": {
        "titulo": "Mide tu patio. Te decimos cuánto cuesta.",
        "lede": ("Escribe el largo y el ancho, como si caminaras el jardín con una cinta. El cálculo se llena en la "
                 "etiqueta y viaja contigo al WhatsApp: no lo tienes que explicar dos veces."),
    },
    "obras": {
        "titulo": "Fotos de obra, no de catálogo.",
        "lede": "Cada foto lleva su pie: dónde y en qué etapa. Así ves lo que entregamos, no una promesa.",
        "figuras": (
            {"src": f"{OBRA}/terra/jardin-residencial-pasto-alberca.webp", "ancho": 1200, "alto": 918, "numero": 2,
             "alt": "Jardín residencial con pasto parejo alrededor de una alberca de forma libre, con palmeras y muro de piedra.",
             "lugar": "Jardín residencial con pasto", "etapa": "Terminado"},
            {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 3,
             "alt": "Pasto San Agustín recién instalado junto a un andador.", "lugar": "Después",
             "etapa": "Día de instalación"},
            {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 4,
             "alt": "Rollos de pasto San Agustín recién cortados en la camioneta de reparto.",
             "lugar": "Rollos recién cortados", "etapa": "En la camioneta de reparto"},
            {"src": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600, "numero": 5,
             "alt": "Cuadrilla de Viveros Terra instalando tubería de riego en un jardín.", "lugar": "Riego automático",
             "etapa": "Instalación de tubería"},
            {"src": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961, "numero": 6,
             "alt": "Palmas en costal listas para entrega en el patio del vivero.", "lugar": "Patio del vivero",
             "etapa": "Palmas para entrega"},
        ),
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "opiniones": {
        "titulo": "Lo que dicen nuestros clientes en Tampico",
        "lede": f"{datos.CLIENTES} familias y empresas en Tamaulipas y Veracruz · {datos.GOOGLE}.",
        "items": TESTIMONIOS,
    },
    "proceso": {
        "titulo": "Cuatro pasos. Cada quien sabe qué le toca.",
        "lede": ("Lo que hace que un jardín se logre es repartir bien el trabajo. Por eso cada paso dice de quién es."),
        "pasos": (
            {"titulo": "Nos mandas medidas y foto", "quien": "tu", "cuando": "Día 0 · por WhatsApp",
             "texto": f"Tu colonia, los metros aproximados y una foto del espacio. {datos.PROMESA}."},
            {"titulo": "Medimos y decidimos", "quien": "juntos", "cuando": "Visita para medir",
             "texto": (f"{datos.VISITA_COSTO_CORTO}. Recorremos el espacio contigo y, si hace falta tierra negra o "
                       f"nivelación, te decimos cuánto cuesta antes de empezar. {datos.ANTICIPO}")},
            {"titulo": "Instalamos en un día", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": f"El pasto llega del campo {datos.LLEGADA_PASTO}, se corta para tu pedido y va directo a tu jardín."},
            {"titulo": "El primer riego", "quien": "tu", "cuando": "Días 1 a 20",
             "texto": (f"{datos.PRIMER_RIEGO} Si una sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo, "
                       'siguiendo el protocolo de riego (<a href="/protocolo-cuidados-pasto-san-agustin">ver condiciones</a>).')},
        ),
    },
    "precios": {
        "titulo": "Lista de precios, sin letra chica.",
        "lede": (f"Precios con IVA, salvo el pasto sin instalar: {datos.PASTO_SIN_IVA[0].lower()}{datos.PASTO_SIN_IVA[1:]}. "
                 "Donde dice “desde”, el total depende de tus metros y del terreno: al medir te damos el precio cerrado."),
        "nota": ("En sombra profunda el San Agustín no prende. Si es tu caso, te lo decimos al medir, antes de cobrarte "
                 "nada.", f"Desde el vivero, {datos.CALLE_CORTA}"),
        "filas": (
            {"nombre": "Pasto San Agustín instalado", "unidad": "/m²", "precio": P["pasto_instalado_m2"], "desde": True,
             "rec": True, "detalle": (f"Preparación básica del suelo, tendido en un día y garantía de arraigo de "
                                      f"{datos.ARRAIGO}.")},
            {"nombre": "Pasto San Agustín, solo el pasto", "unidad": "/m²", "precio": P["pasto_solo_m2"],
             "detalle": "Se corta para tu pedido. Recoges en el vivero o te lo llevamos. No lleva IVA."},
            {"nombre": "Mayoreo de pasto, solo pasto", "unidad": "/m²", "precio": P["pasto_mayoreo_m2"], "desde": True,
             "detalle": f"Pedidos de {MINIMO} m² o más, con entregas por etapas y factura {datos.FACTURA}. No lleva IVA."},
            {"nombre": "Pasto sintético, material", "unidad": "/m²", "precio": P["sintetico_tienda_m2"], "desde": True,
             "detalle": "9 modelos en rollos de 50 m². Envío a todo México, cobrado por rollo según tu estado."},
            {"nombre": "Mantenimiento de jardín", "unidad": "/mes", "precio": P["mantenimiento_mes"], "desde": True,
             "detalle": "Poda, fertilización y control de plagas. Residencial e industrial."},
            {"nombre": "Diseño de jardín, Plan Terra", "unidad": "/proyecto", "precio": P["diseno"], "desde": True,
             "detalle": "Visita, propuesta de diseño y lista de materiales."},
            {"nombre": "Tierra negra vegetal", "unidad": "/costal", "precio": P["tierra_negra_costal"],
             "detalle": f"También por m³ ({dinero(P['tierra_negra_m3'])}) y en camión volteo."},
            {"nombre": "Tezontle rojo", "unidad": "/costal", "precio": P["tezontle_costal"], "desde": True,
             "detalle": "También por m³ y en camión volteo de 14 m³."},
        ),
        "caption": (f'Precios {datos.ANIO}. {datos.PASTO_SIN_IVA}; los demás lo incluyen. Lista completa en '
                    '<a href="/precios">viverosterra.com/precios</a>.'),
    },
    "faq": {
        "titulo": "Lo que nos preguntan antes de empezar.",
        "preguntas": PREGUNTAS,
        "titulo_guias": "Guías para el clima de Tampico",
        "guias": (
            ("7 árboles para banqueta que no levantan el pavimento", "/blog/arboles-para-sembrar-en-banqueta"),
            ("Palma del viajero: guía de cuidados en Tampico", "/blog/cuidados-palma-del-viajero-ravenala"),
            ("Pasto San Agustín o japonés: cuál conviene en Tampico", "/blog/pasto-san-agustin-vs-japones"),
            ("Cuándo plantar pasto en Tampico: calendario mes a mes", "/blog/cuando-plantar-pasto-tampico-calendario"),
            ("12 plantas resistentes a la sal del Golfo en Tampico", "/blog/plantas-resistentes-sal-golfo-tampico"),
            ("¿Conviene el riego automático en Tampico?", "/blog/sistema-riego-automatico-conviene-tampico"),
        ),
    },
    "cobertura": {
        "titulo": "Jardinería en Tampico, Madero, Altamira y la Huasteca.",
        "lede": ("Pasto en rollo, diseño de jardines, riego y mantenimiento en toda la zona conurbada; en la Huasteca, "
                 "por proyecto."),
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO,
    },
    "cierre": {
        "titulo": "Mándanos tus medidas y una foto del espacio.",
        "lede": "Tu colonia, los metros aproximados y qué quieres hacer.",
        "visita": f"Si hace falta, agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}",
        "mensaje": datos.MENSAJES["general"],
    },
}

# Elemento de la home anterior → elemento nuevo que lo cubre, o motivo de su retiro (tests/paridad/index.json).
SERVICIOS_EN_INDICE = "Ahora es una fila del índice “Cinco formas de trabajar con nosotros”, con su precio."
GUIA_EN_LISTA = "Sigue enlazada desde la lista “Guías para el clima de Tampico”, con el mismo texto de enlace."
PASOS_VIEJOS = "Los 5 pasos genéricos se reemplazan por los 4 pasos con NOSOTROS / TÚ / JUNTOS (spec §4.1)."
SIN_GRATIS = ("Decía “Cotización gratis hoy”: la home ya no dice “gratis” (spec del hero, 2026-11-09, §2); ahora dice "
              "“Precios a la vista” (sin “con IVA”: el pasto sin instalar no lo lleva) y la promesa en horario.")
PARIDAD = {
    "meta": {"description": (DESCRIPCION, SIN_GRATIS), "og:description": (DESCRIPCION, SIN_GRATIS)},
    "reemplazos": {
        "Jardinería en Tampico, pasto en rollo y vivero desde 2007.": "Pasto, jardines y plantas en Tampico.",
        "¿Cuánto cuesta tu jardín?": "Mide tu patio. Te decimos cuánto cuesta.",
        "Todo lo que tu jardín necesita, en un solo lugar": "Cinco formas de trabajar con nosotros, cada una con su precio.",
        "Pasto en Rollo San Agustín": "Pasto natural",
        "Diseño de Jardines": "Diseño, mantenimiento y riego",
        "Sistema de riego automatizado": "Diseño, mantenimiento y riego",
        "Mantenimiento Profesional": "Diseño, mantenimiento y riego",
        "Plantas, palmas y árboles": "Plantas y palmas",
        "Empresa / Comercial": "Empresas y constructoras",
        "Proyecto B2B": "Empresas y constructoras",
        "¿Proyecto grande o mayoreo?": "Empresas y constructoras",
        "Jardines que hemos hecho en Tampico": "Fotos de obra, no de catálogo.",
        "Así de fácil es trabajar con nosotros": "Cuatro pasos. Cada quien sabe qué le toca.",
        "Nos escribes": "Nos mandas medidas y foto",
        "Preguntas frecuentes sobre pasto y jardinería en Tampico": "Lo que nos preguntan antes de empezar.",
        "Tu jardín ideal está a un mensaje de distancia": "Mándanos tus medidas y una foto del espacio.",
        "Cotización por WhatsApp": "Mándanos tus medidas y una foto del espacio.",  # sin formulario por correo (dueño)
        "Cobertura de Servicio en Tamaulipas y Veracruz": "Jardinería en Tampico, Madero, Altamira y la Huasteca.",
    },
    "retirados": {
        "Viveros Terra: vivero y empresa de jardinería en Tampico y Madero desde 2007": (
            "El párrafo de entidad pasa al lede de la portada y al cuadro de datos; la página de entidad es /nosotros "
            "(Etapa 3)."),
        "Residencial": "La bifurcación por cliente es ahora el índice de cinco rutas con precio (spec §3.3).",
        "Antes y después de instalar pasto en Tampico": (
            "El deslizador y su contador “Respondemos en 2:00 hrs” (promesa vieja) se retiran; el después queda como "
            "Fig. 03."),
        "Cotización rápida": PASOS_VIEJOS,
        "Agendamos": PASOS_VIEJOS,
        "Instalación": PASOS_VIEJOS,
        "Jardín listo": PASOS_VIEJOS,
        "¿Por qué elegir Viveros Terra?": "Sus cifras quedan en el cuadro de datos y en la línea de prueba (desde 2007, "
                                          "+1,500 instalaciones, 4.6 en Google).",
        "Conocimiento del clima local": "Queda en la respuesta “¿Qué pasto es mejor para el clima de Tampico?”.",
        "Servicio integral, una sola empresa": "Lo dice el índice de cinco rutas.",
        "Respuesta en menos de 1 hora en horario": "Es la promesa única debajo de cada CTA.",
        "Materiales para jardín en Tampico": "Tierra negra y tezontle van en la lista de precios; los cuatro materiales "
                                             "siguen en el menú y en el pie.",
        "Pasto San Agustín": SERVICIOS_EN_INDICE,
        "Tierra Negra Vegetal": "Fila “Tierra negra vegetal” de la lista de precios.",
        "Tezontle Rojo": "Fila “Tezontle rojo” de la lista de precios.",
        "Mármol y Piedra": "Mármol blanco y piedra bola siguen en el menú y en el pie.",
        "7 árboles para banqueta que no levantan el pavimento": GUIA_EN_LISTA,
        "Palma del viajero: guía de cuidados en Tampico": GUIA_EN_LISTA,
        "Pasto San Agustín o japonés: cuál conviene en Tampico": GUIA_EN_LISTA,
        "Cuándo plantar pasto en Tampico: calendario mes a mes": GUIA_EN_LISTA,
        "12 plantas resistentes a la sal del Golfo en Tampico": GUIA_EN_LISTA,
        "¿Conviene el riego automático en Tampico?": GUIA_EN_LISTA,
        "¿Cuánto ahorra un sistema de riego automatizado?": "Vive en /sistema-riego-tampico; la home deja 6 preguntas "
                                                            "(spec §3.3).",
        "¿Hacen envíos de pasto fuera de Tampico?": "Respondida en /pasto-en-rollo-tampico (“¿Hacen entrega fuera de "
                                                    "Tampico?”).",
        "$0": "Era el marcador vacío del cotizador viejo (“$0 – $0”).",
    },
}
