"""Contenido de /pasto-en-rollo-tampico. Solo datos: la plantilla es tools/site/plantillas/servicio.py.

Copy de la maqueta aprobada (docs/diseno/hibrido/pasto-en-rollo.html) con los datos vivos de datos.py y el copy
corregido en la Etapa 1b (anticipo sin porcentaje, "Cortado para tu pedido", llegada semanal sin fecha de corte).
Título y descripción (también en Open Graph y Twitter Card): los de la fase 0 de SEO (contenido/seo.py).
Canonical, Product y migas del JSON-LD se conservan como estaban publicados; FAQPage sale de las mismas preguntas visibles y HowTo, de los cinco pasos del proceso visible.
PARIDAD: tests/test_paridad.py.
"""
import datos
import entidad
from componentes import dinero, dinero_exacto, mensualidades
from contenido import seo
from contenido import respuestas

P = datos.PRECIOS
MINIMO = P["pasto_mayoreo_minimo_m2"]
OBRA = "/img/obra"
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
URL = f"{datos.SITIO}/pasto-en-rollo-tampico"

TITULO = f"Pasto en Rollo Tampico: San Agustín ${P['pasto_solo_m2']}/m² | Viveros Terra"
DESCRIPCION = (f"Pasto San Agustín en rollo en Tampico: ${P['pasto_solo_m2']}/m² solo el pasto o desde "
               f"${P['pasto_instalado_m2']}/m² instalado, con garantía de arraigo. Entrega en Madero y Altamira. Cotiza hoy.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", TITULO),
        ("og:description", DESCRIPCION),
        ("og:image", f"{datos.SITIO}/img/despues-instalacion-pasto-san-agustin-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
    # Twitter Card con el mismo título y la misma descripción (SEO fase 0, 2026-11-10).
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", TITULO),
        ("twitter:description", DESCRIPCION),
        ("twitter:image", f"{datos.SITIO}/img/despues-instalacion-pasto-san-agustin-tampico.webp"),
    ),
}

PRODUCTO = {
    "@type": "Product",
    "name": "Pasto en Rollo San Agustín Tampico",
    "description": (f"Pasto San Agustín fresco cortado semanalmente para jardines en Tampico. Desde "
                    f"${P['pasto_solo_m2']}/m² solo el pasto e instalado desde ${P['pasto_instalado_m2']}/m², con "
                    "garantía de arraigo."),
    "brand": {"@type": "Brand", "name": datos.NOMBRE},
    # SEO fase 1: la foto real de la portada y el vendedor por @id a la entidad única (antes, un LocalBusiness suelto).
    "image": f"{datos.SITIO}/img/despues-instalacion-pasto-san-agustin-tampico.webp",
    "offers": {"@type": "Offer", "priceCurrency": "MXN", "price": str(P["pasto_solo_m2"]),
               "priceValidUntil": datos.PRECIOS_VIGENTES_HASTA, "availability": "https://schema.org/InStock",
               "seller": entidad.REF},
}

MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": datos.SITIO},
    {"@type": "ListItem", "position": 2, "name": "Pasto en Rollo Tampico", "item": URL},
]}

# Enlazado interno (SEO fase 0, 2026-11-10): la guía de errores solo recibía un enlace (el índice del blog).
GUIA_ERRORES = "/blog/errores-pasto-san-agustin-tampico"
PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Cuándo llega el pasto fresco al vivero?",
     f"El pasto llega {datos.LLEGADA_PASTO}, directo del campo. Nunca lo almacenamos más de una semana: se corta para "
     "tu pedido y va del campo a tu jardín en el menor tiempo posible, con las raíces activas para arraigar."),
    ("¿Cuánto tiempo tarda en arraigar el pasto San Agustín?",
     f"En el clima cálido y húmedo de Tampico arraiga en {datos.ARRAIGO} con riego abundante y diario. "
     f"{datos.PRIMER_RIEGO} Con instalación contratada, si una sección no arraiga en ese plazo, la reponemos sin costo, "
     'siguiendo el protocolo de riego (<a href="/politicas">ver condiciones</a>). Guía: '
     f'<a href="{GUIA_ERRORES}">los 5 errores que matan el pasto San Agustín</a>.'),
    ("¿Cómo se paga el pasto en rollo?",
     f"{datos.ANTICIPO} También puedes pagar en mensualidades con tarjeta de crédito en cotizaciones desde "
     f"{DESDE_MENSUALIDADES}."),
    ("¿Qué diferencia hay entre pasto de vivero y pasto de mercado?",
     "El pasto de vivero se corta fresco y va directo al jardín, con las raíces activas. El de mercado puede llevar días "
     f"en una bodega sin agua, perdiendo humedad. En el clima de Tampico se nota: el nuestro arraiga en {datos.ARRAIGO} "
     "y, si lo instalamos, tiene garantía; el de mercado puede tardar más o no arraigar."),
    ("¿Qué variedad de pasto es mejor para Tampico?",
     "El San Agustín (<i>Stenotaphrum secundatum</i>): resiste el calor intenso y la humedad del clima costero, y tolera "
     "sombra parcial mejor que otras variedades. Es el pasto más usado en jardines, áreas comerciales y parques "
     'industriales del sur de Tamaulipas. <a href="/blog/pasto-san-agustin-vs-japones">San Agustín o japonés: la '
     "comparativa</a>."),
    ("¿Hacen entrega fuera de Tampico?",
     "Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y por proyecto en Pánuco, Ciudad Victoria, Tuxpan y la "
     "Huasteca. El costo de entrega depende de la distancia y el volumen; en proyectos grandes coordinamos la logística "
     "por etapas."),
    ("¿Tienen precio de mayoreo para constructoras?",
     f"Sí: desde ${P['pasto_mayoreo_m2']}/m² (solo pasto) en pedidos de {MINIMO} m² o más, con factura {datos.FACTURA}, "
     f"registro REPSE {datos.REPSE} y entregas por etapas según el avance de obra. "
     '<a href="/mayoreo-pasto-tampico">Pasto al mayoreo para obras</a>.'),
)

SECTORES = (
    ("Residencial", "Casas y jardines familiares"),
    ("Fraccionamientos", "Áreas verdes de acceso y casas muestra"),
    ("Hoteles y resorts", "Jardines de imagen y áreas exteriores"),
    ("Industria", "Parques industriales, áreas perimetrales y accesos"),
    ("Gobierno y municipios", "Parques, plazas y áreas públicas"),
)

CONTENIDO = {
    "respuesta": respuestas.de("/pasto-en-rollo-tampico"),  # SEO fase 1: respuesta directa bajo la portada
    "tipo": "servicio-pasto",
    "prefijo": "pasto",
    "meta": META,
    "jsonld": {"producto": PRODUCTO, "migas": MIGAS_LD, "howto": "Cómo instalar pasto en rollo San Agustín en Tampico",
               "speakable": entidad.SPEAKABLE},
    "migas": (("Inicio", "/"), ("Pasto en rollo", None)),
    "portada": {
        "kicker": "Pasto natural · Tampico, Madero y Altamira",
        "pos": "50% 4%",
        "dato": f"Garantía de arraigo de {datos.ARRAIGO} con instalación",
        "enlaces": (("Calcula tu patio", "#precio"), ("Mensualidades con tarjeta", "#mensualidades")),
        "h1": ('Pasto San Agustín en rollo, instalado en un día. '
               '<span class="vt-serif">Del campo a tu jardín, sin pasar por bodega.</span>'),
        "lede": f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}.",
        "etiqueta": {
            "codigo": "Pasto · 01", "aviso": "Tepe 40 × 60 cm", "nombre": "Pasto San Agustín",
            "cientifico": "Stenotaphrum secundatum", "antes": "Instalado · desde",
            "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m²",
            "filas": (("Solo pasto, tú lo instalas", f"{dinero(P['pasto_solo_m2'])} /m²"),
                      (f"Mayoreo, solo pasto, {MINIMO} m² o más", f"desde {dinero(P['pasto_mayoreo_m2'])} /m²")),
        },
        "mensaje": datos.MENSAJES["pasto-natural"],
        "foto": {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 1,
                 "alt": "Rollos de pasto San Agustín recién cortados, cargados en la camioneta de reparto.",
                 "lugar": "Rollos recién cortados · en la camioneta de reparto", "etapa": "Cd. Madero"},
    },
    "prueba": {
        "titulo": "Lo que entregamos, documentado.",
        "lede": ('<i class="vt-serif">Stenotaphrum secundatum</i> es la variedad que mejor aguanta el calor y la '
                 "humedad del Golfo. Así se ve en cada etapa."),
        "figuras": (
            {"src": f"{OBRA}/terra/jardin-residencial-pasto-alberca.webp", "ancho": 1200, "alto": 918, "numero": 2,
             "alt": "Jardín residencial con pasto parejo alrededor de una alberca de forma libre, con palmeras y muro de piedra.",
             "lugar": "Jardín residencial con pasto", "etapa": "Terminado"},
            {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp", "ancho": 640, "alto": 960, "numero": 3,
             "alt": "Integrante de la cuadrilla tendiendo tepes de pasto San Agustín.", "lugar": "Tendido de tepes",
             "etapa": "Día de instalación"},
            {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 4,
             "alt": "Pasto recién instalado con el borde recortado contra el andador.", "lugar": "Después",
             "etapa": "Borde recortado"},
            {"src": f"{OBRA}/riego-aspersor-borde-pasto.webp", "ancho": 700, "alto": 875, "numero": 5,
             "alt": "Aspersor regando el borde de un jardín con pasto San Agustín.", "lugar": "Riego de arraigo",
             "etapa": "Aspersión en el borde"},
        ),
        "nota": ("En sombra profunda el San Agustín no prende. Ahí va otra solución, y te lo decimos antes de cobrarte.",
                 "Al medir, en tu jardín"),
        # Prueba social: la opinión aprobada de la home sobre pasto, las dos de esta página anteriores a 2a (reales y con
        # permiso del dueño, 2026-11-07), todas textuales, y los clientes con permiso del dueño.
        "titulo_opinion": "Lo que dicen quienes ya tienen su jardín",
        "opiniones": datos.OPINIONES[:1] + datos.OPINIONES_PASTO_EN_ROLLO,
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el pasto San Agustín en Tampico?",
        "lede": (f"Desde {dinero(P['pasto_instalado_m2'])}/m² instalado (con IVA incluido) en Tampico, Madero y Altamira, con preparación "
                 f"básica del suelo y garantía de arraigo de {datos.ARRAIGO}; {dinero(P['pasto_solo_m2'])}/m² solo el "
                 f"pasto, y desde {dinero(P['pasto_mayoreo_m2'])}/m² en mayoreo de {MINIMO} m² o más con factura "
                 f"{datos.FACTURA}. {datos.PASTO_SIN_IVA}. Precios {datos.ANIO}."),
        "filas": (
            {"nombre": "Pasto con instalación", "unidad": "/m²", "precio": P["pasto_instalado_m2"], "desde": True,
             "rec": True, "detalle": (f"Preparación básica del suelo, tendido en un día, garantía de arraigo de "
                                      f"{datos.ARRAIGO} y protocolo de riego.")},
            {"nombre": "Solo el pasto", "unidad": "/m²", "precio": P["pasto_solo_m2"],
             "detalle": (f"Tú lo instalas. Recoges en el vivero de {datos.CALLE_CORTA} o te lo llevamos (la entrega se "
                         "cotiza según tu colonia).")},
            {"nombre": "Mayoreo, solo pasto", "unidad": "/m²", "precio": P["pasto_mayoreo_m2"], "desde": True,
             "detalle": (f"Desde {MINIMO} m². Entregas por etapas según avance de obra, factura {datos.FACTURA} y REPSE "
                         f'{datos.REPSE}. <a href="/mayoreo-pasto-tampico">Pasto al mayoreo para obras</a>.')},
        ),
        "caption": (f"Precios {datos.ANIO}. El instalado incluye IVA. {datos.PASTO_SIN_IVA}. Donde dice “desde”, al medir te damos el precio cerrado. "
                    'Lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "titulo_medidor": "Calcula el tuyo",
    },
    "objecion": {
        "titulo": "¿Cuál te conviene según tu espacio?",
        "lede": ("Vendemos e instalamos los dos en Tampico. Esta tabla te ayuda a elegir según tu espacio, tu presupuesto "
                 "y el tiempo que quieras dedicarle."),
        "comparativa": {
            "columnas": ("Característica", "Pasto San Agustín (natural)", "Pasto sintético"),
            "filas": (
                ("Precio instalado", f"desde {dinero(P['pasto_instalado_m2'])}/m²",
                 f"desde {dinero_exacto(P['sintetico_instalado_m2'][0])}/m²"),
                ("Vida útil", "15+ años con cuidado", "8-10 años"),
                ("Mantenimiento", "Riego + poda quincenal", "Cepillado mensual"),
                ("Riego", "Diario al instalar; después, según el clima", "Sin riego; solo un enjuague ocasional"),
                ("Ideal para", "Jardines residenciales con sombra parcial",
                 "Terrazas, azoteas, áreas sin riego y zonas para mascotas"),
            ),
            "caption": "Pasto natural o sintético, según tu espacio.",
            "cierre": ("Si tu jardín tiene tierra y puedes regarlo, el San Agustín cuesta menos por metro y dura más. Si "
                       "es una terraza, una azotea o un área sin riego, te conviene el sintético: también lo vendemos e "
                       'instalamos en Tampico (<a href="/pasto-sintetico-tampico">ver pasto sintético</a>).'),
        },
        "titulo_2": "Pasto de vivero vs pasto de mercado",
        "comparativa_2": {
            "columnas": ("Característica", "Viveros Terra", "Pasto de mercado"),
            "filas": (
                ("Frescura", "Se corta para tu pedido y va directo a tu jardín", "Puede llevar días en bodega sin agua"),
                ("Arraigo en Tampico", f"{datos.ARRAIGO}, con garantía si lo instalamos", "Variable, sin garantía"),
                ("Forma de pago", "Anticipo para confirmar; contado o mensualidades con tarjeta de crédito",
                 "Normalmente todo por adelantado"),
                ("Después de instalar", "Protocolo de riego de 20 días por escrito", "Sin seguimiento"),
                ("Factura", datos.FACTURA, "Rara vez"),
            ),
            "caption": "Lo que cambia entre el pasto de vivero y el de mercado.",
        },
    },
    "proceso": {
        "titulo": "Cómo se instala el pasto en rollo: cinco pasos, dos son tuyos.",
        "lede": ("Lo que hace que el pasto arraigue es el agua de las primeras semanas. Por eso te lo explicamos ahí "
                 "mismo, en tu jardín."),
        "pasos": (
            {"titulo": "Preparación del suelo", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": ("Nivelamos, retiramos piedras grandes y agregamos 3 a 5 cm de tierra negra si hace falta. Nunca "
                       "te cobramos preparación sin avisarte antes.")},
            {"titulo": "Tendido de los tepes", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": ("Tepes de 40 × 60 cm en patrón de ladrillo, uniones desfasadas y sin huecos, presionados para que "
                       "la raíz toque el suelo.")},
            {"titulo": "Primer riego", "quien": "tu", "cuando": "Primeras 2 horas",
             "texto": ("El primer riego lo haces tú: riega hasta que el agua atraviese el tepe. Te enseñamos cuánta agua "
                       "darle antes de irnos.")},
            {"titulo": "Riego diario", "quien": "tu", "cuando": "Días 1 a 20",
             "texto": ("Abundante, de preferencia mañana y tarde, siguiendo el "
                       '<a href="/protocolo-cuidados-pasto-san-agustin">protocolo de 20 días</a> que te dejamos por '
                       "escrito. Después, una vez al día por un mes y luego 3 veces por semana.")},
            {"titulo": "Primera poda", "quien": "juntos", "cuando": "Día 21",
             "texto": ("A 4 o 5 cm de altura, cuando ya arraigó. Te decimos cuándo; si tienes "
                       '<a href="/mantenimiento-jardines-tampico">mantenimiento</a> con nosotros, la hacemos.')},
        ),
    },
    "garantia": {
        "titulo": "Si no arraiga, lo reponemos.",
        "grande": "15–20", "unidad": "días",
        "resumen": f"Garantía de arraigo de {datos.ARRAIGO} con instalación contratada.",
        "puntos": (
            ("Si contratas la instalación y sigues el protocolo de riego de 20 días, garantizamos el arraigo: si una "
             f"sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo.", True),
            (f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}; no son rollos viejos de bodega.", True),
            ("Protocolo por escrito: qué hacer cada día y qué señales revisar.", True),
            (f"Factura {datos.FACTURA} para persona física o moral.", True),
            ("Si el área tiene sombra profunda, te lo decimos al medir: ahí el San Agustín no es la opción y no lo "
             "instalamos con garantía.", False),
        ),
        "pie": ('<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a> · '
                '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de cuidados de 20 días</a>'),
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito desde "
                 f"{DESDE_MENSUALIDADES}."),
        "puntos": (
            "Recibes el precio del pasto, la entrega y la instalación por separado.",
            "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
            ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos antes "
             'de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>'),
        ),
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "pasto en rollo instalado", "monto": 12000},
    },
    "faq": {"titulo": "Todo sobre el pasto en rollo en Tampico", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "Tu jardín verde, instalado en un día.",
        "lede": ("Dinos si lo quieres solo pasto o instalado, tu colonia y tus metros, y mándanos una foto. Si hace falta, "
                 f"agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}"),
        "mensaje": datos.MENSAJES["pasto-natural"],
    },
    "cobertura": {
        "titulo": f"{datos.M2_INSTALADOS} instalados en Tamaulipas y la Huasteca.",
        "lede": ("Instalamos pasto en rollo en Tampico, Ciudad Madero y Altamira, para casas, fraccionamientos, hoteles, "
                 "industria y gobierno. Fuera de la zona conurbada, por proyecto."),
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
    },
    "relacionados": {
        "titulo": "Complementa tu jardín",
        "items": (
            {"titulo": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico",
             "img": "/img/tierra-negra-preparacion-pasto-tampico-640.webp", "ancho": 640, "alto": 360,
             "texto": (f"La base ideal antes de instalar pasto. Costal {dinero(P['tierra_negra_costal'])} · m³ "
                       f"{dinero(P['tierra_negra_m3'])}.")},
            {"titulo": "Sistema de riego automático", "href": "/sistema-riego-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": "Para que tu pasto siempre esté verde sin esfuerzo. Ahorra hasta 40% de agua."},
            {"titulo": "Mantenimiento mensual", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": (f"¿Ya tienes tu pasto? Que nunca se vea descuidado. Desde {dinero(P['mantenimiento_mes'])}/mes.")},
        ),
    },
}

OBJECIONES = "Las objeciones de la página anterior quedan en las preguntas, el Medidor, el pago y la garantía."
PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION),
    "reemplazos": {
        "$385": f"${int(P['sintetico_instalado_m2'][0])}",
        "Pasto San Agustín en rollo, instalado en un día": (
            "Pasto San Agustín en rollo, instalado en un día. Del campo a tu jardín, sin pasar por bodega."),
        "¿Cuánto cuesta ponerle pasto a mi jardín?": "Calcula el tuyo",
        "Tres formas de tener tu jardín verde": "¿Cuánto cuesta el pasto San Agustín en Tampico?",
        "Cómo instalar pasto en rollo San Agustín en 5 pasos": (
            "Cómo se instala el pasto en rollo: cinco pasos, dos son tuyos."),
        "Colocación de los tepes": "Tendido de los tepes",
        "Primer riego (lo haces tú)": "Primer riego",
        "Riego abundante y diario los primeros 15 a 20 días": "Riego diario",
        "Primera poda a los 21 días": "Primera poda",
        "Jardines con pasto San Agustín en Tampico": "Lo que entregamos, documentado.",
        "Protocolo de Cuidados Garantía de arraigo en 15 a 20 días": "Si no arraiga, lo reponemos.",
        "+500,000 m² instalados en Tamaulipas y zona Huasteca": "+500,000 m² instalados en Tamaulipas y la Huasteca.",
        "¿Puedo pagar en partes?": "¿Cómo se paga el pasto en rollo?",
        "¿Cuánto tiempo tarda en arraigar?": "¿Cuánto tiempo tarda en arraigar el pasto San Agustín?",
    },
    "retirados": {
        "Pasto natural premium cultivado para el clima del Golfo": (
            "Su contenido queda en la respuesta “¿Qué variedad de pasto es mejor para Tampico?” y en la entrada de la "
            "prueba; sus cifras, en el cuadro de datos."),
        "Solo Pasto": "Es la fila “Solo el pasto” de la tabla de precios.",
        "Pasto + Instalación": "Es la fila “Pasto con instalación” de la tabla de precios.",
        "Mayoreo / Proyectos": "Es la fila “Mayoreo, solo pasto” de la tabla, con enlace a /mayoreo-pasto-tampico.",
        "\"¿Cuánto me va a costar exactamente?\"": OBJECIONES,
        "\"¿Tengo que pagar todo antes?\"": OBJECIONES,
        "\"¿Mi terreno está muy mal para pasto?\"": OBJECIONES,
        "\"¿El pasto llegará fresco?\"": OBJECIONES,
        "\"¿Y si el pasto no arraiga?\"": OBJECIONES,
        "Su vivero de confianza en Tamaulipas": (
            "El bloque B2B pasa a /mayoreo-pasto-tampico (enlazado en la tabla de precios y en la pregunta de mayoreo); "
            "decía “Más de 18 años”."),
        "Viveros Terra · Tampico": (
            "Caja de autor de la página de servicio; la entidad va a /nosotros (Etapa 3). “Certificación SENASICA” y "
            "“+200 proyectos B2B” no están en datos.py."),
        "De la cotización a tu jardín verde en 5 pasos": (
            "Era una segunda lista de cinco pasos junto al proceso: queda una sola (el proceso NOSOTROS / TÚ / JUNTOS, que "
            "también es el HowTo del JSON-LD) y el pago se resume en el bloque “Cómo se paga” (gate de diseño 2a)."),
        "Escríbenos para cotizar": (
            "Formulario de pedido por correo retirado por decisión del dueño (2026-11-07): se cotiza solo por WhatsApp "
            "o con el Medidor, con la promesa única (spec §3.3, §4.3)."),
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Entrada recortada: «Preparamos el suelo, tendemos tepes de 40 × 60 cm y te enseñamos a regarlo» sale del hero (el tepe va en la etiqueta y los pasos, en «Cómo se instala»); «mensualidades… desde $2,000» queda como enlace a #mensualidades, donde está el monto.')
