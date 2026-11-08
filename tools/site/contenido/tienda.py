"""Contenido del hub /pasto-sintetico (tienda nacional). Solo datos: la plantilla es tools/site/plantillas/tienda_hub.py.

Modelos, zonas y fletes salen de tools/pasto/data.py y las ciudades de tools/pasto/ciudades.py. Título, descripción,
canonical, Open Graph, ItemList de Product y migas son los que publicaba tools/pasto/hub.py; FAQPage sale de las
preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from ciudades import CIUDADES
from componentes import dinero
from contenido.ficha import PASOS
from esquema import breadcrumb_schema, product_schema

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico"
BARATO = t.barato()
DEFAULT = data.BY_SLUG["toscana-28"]
DESDE = dinero(BARATO["rollo"])
FLETE_MIN = dinero(min(data.ZONAS.values()))
TITULO = f"Pasto Sintético con Envío a Todo México · Desde {DESDE}/m² | Viveros Terra"
DESCRIPCION = (f"Pasto sintético con envío a todo México desde {DESDE}/m². 9 modelos residenciales de 10 a 35 mm, factura "
               f"{datos.FACTURA} y entrega en 3 a 5 días hábiles.")
GAL = t.GAL

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto sintético con envío?",
     f"El material cuesta de {DESDE} a {dinero(max(m['rollo'] for m in data.MODELOS))}/m² en rollo, según el modelo. El "
     f"envío se suma por rollo según tu estado: {dinero(data.ZONAS['A'])} en Centro y Occidente, "
     f"{dinero(data.ZONAS['B'])} en Norte, Golfo y Sur, y {dinero(data.ZONAS['C'])} en Sureste y fronteras. El cotizador "
     'de esta página calcula tu total estimado. Más detalle en la <a href="/blog/cuanto-cuesta-pasto-sintetico-mexico">'
     "guía de precios</a>."),
    ("¿Cuál es la compra mínima?",
     "Para envío nacional el mínimo es 25 m², medio rollo. En el showroom de Cd. Madero puedes comprar desde 2 m² sin "
     "flete."),
    ("¿Cuánto tarda el envío?",
     "De 3 a 5 días hábiles después de confirmar tu pago, según el destino. Te compartimos la guía de rastreo."),
    ("¿Cómo pago?",
     "Por transferencia bancaria o con link de pago con tarjeta de débito o crédito. El pedido se embarca al confirmar el "
     "pago."),
    ("¿Dan factura?", f"Sí. Emitimos factura {datos.FACTURA} para persona física o moral en todos los pedidos."),
    ("¿Qué modelo me conviene?",
     "Toscana 28 es el más vendido para jardines familiares. Para poco uso o presupuesto ajustado, Toscana 18. Para "
     "perros y pisoteo diario, Irlanda 25 o Capri 20. Para el look más natural, los de 35 mm: Japonés, Mónaco y Bali."),
    ("¿Puedo instalarlo yo mismo?",
     "Sí. Un jardín de 25 a 50 m² se instala en un día. Te mandamos la guía de instalación con el pedido. En Tampico, "
     "Madero y Altamira también ofrecemos instalación profesional. Aquí está la "
     '<a href="/blog/como-instalar-pasto-sintetico">guía paso a paso</a>.'),
    ("¿Qué incluye un rollo?",
     "Un rollo mide 2 m de ancho por 25 m de largo: 50 m². Puedes pedir desde 25 m² y te enviamos el corte."),
    ("¿Hacen instalación fuera de Tampico?",
     "A nivel nacional enviamos solo el material, con guía de instalación. La instalación profesional es solo en "
     "Tampico, Ciudad Madero y Altamira."),
)

DIY = (
    {"titulo": "Nivela y compacta", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira el pasto viejo, empareja el terreno y compáctalo."},
    {"titulo": "Base drenante", "quien": "tu", "cuando": "Paso 2",
     "texto": "Extiende y compacta grava fina o polvo de piedra para que drene."},
    {"titulo": "Extiende y clava", "quien": "tu", "cuando": "Paso 3",
     "texto": "Coloca el rollo, déjalo reposar, corta a medida y fija el perímetro."},
    {"titulo": "Une los tramos", "quien": "tu", "cuando": "Paso 4",
     "texto": "Junta los rollos con cinta de unión y adhesivo, con la fibra en la misma dirección."},
    {"titulo": "Cepilla", "quien": "tu", "cuando": "Paso 5",
     "texto": "Cepilla a contrapelo para levantar la fibra y darle aspecto natural."},
)

OBRAS = tuple({"src": f"{GAL}/{n}-sm.webp", "srcset": f"{GAL}/{n}-sm.webp 560w, {GAL}/{n}.webp 960w",
               "sizes": "(min-width: 1024px) 400px, 80vw", "ancho": w, "alto": h, "alt": alt, "numero": i,
               "lugar": cap, "etapa": "Obra con pasto sintético"}
              for i, (n, w, h, alt, cap) in enumerate(data.OBRAS, 2))

CONTENIDO = {
    "tipo": "tienda",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large", "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", f"{SITE}{GAL}/obra-residencial-tampico.webp"),
               ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "jsonld": (
        breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", URL)]),
        {"@type": "ItemList", "name": "Modelos de pasto sintético residencial con envío a todo México",
         "numberOfItems": len(data.MODELOS),
         "itemListElement": [{"@type": "ListItem", "position": i, "item": product_schema(m)}
                             for i, m in enumerate(data.MODELOS, 1)]},
    ),
    "migas": (("Inicio", "/"), ("Pasto sintético", None)),
    "portada": {
        "kicker": "Tienda · Envío a todo México",
        "existencia": f"{len(data.MODELOS)} modelos en existencia · vendemos a todo México desde "
                      f"{datos.SINTETICO_NACIONAL_DESDE}",
        "h1": 'Pasto sintético <span class="vt-serif">con envío a todo México</span>',
        "rotulo_estado": "Precio puesto en tu puerta",
        "rollo": BARATO["rollo"],
        "nota_precio": f"+ envío desde {FLETE_MIN} por rollo. Elige tu estado para ver el precio puesto.",
        "mensualidades": 'Paga en mensualidades con tarjeta de crédito. <a href="#cotizador">Calcula tu plan</a>',
        "foto": {"src": f"{GAL}/obra-proyecto-03-sm.webp", "srcset": f"{GAL}/obra-proyecto-03-sm.webp 560w, "
                 f"{GAL}/obra-proyecto-03.webp 960w", "sizes": "(min-width: 1024px) 620px, 100vw", "ancho": 960,
                 "alto": 1280, "numero": 1, "alt": "Residencia con palmas y jardín de pasto sintético instalado",
                 "lugar": "Residencia con palmas", "etapa": "Proyecto con pasto de la colección"},
        "datos": (("Respuesta", "Menos de 1 hora", datos.HORARIO), ("Garantía", "3 a 8 años", "De fábrica, según el modelo"),
                  ("Devoluciones", "7 días", "Nuevo y sin cortar"), ("Factura", datos.FACTURA, "Persona física o moral"),
                  ("Envío nacional", f"Desde {datos.SINTETICO_NACIONAL_DESDE}", "3 a 5 días hábiles"),
                  ("Showroom", datos.CALLE_CORTA, f"Vivero desde {datos.DESDE}")),
        "mensaje": datos.MENSAJES["pasto-sintetico"],
    },
    "modelos": {"titulo": "Modelos de pasto sintético de 10 a 35 mm",
                "lede": ("Ordenados por altura. A más altura y peso, más volumen y realismo. Todos se venden por rollo de "
                         "2 × 25 m con envío a todo México.")},
    "elegir": {"titulo": "¿Qué pasto sintético te conviene?"},
    "comparar": {"titulo": "¿Viste otro precio? Compáralo aquí",
                 "lede": ("Hay ofertas que esconden el flete en el precio por m². Compara el precio final, puesto en tu "
                          "casa, contra el nuestro en tu estado.")},
    "cotizador": {"titulo": "Precio del pasto sintético con envío a tu estado", "titulo_cotizador": "Cotizador",
                  "titulo_calculo": "Cómo se calcula",
                  "calculo": ("Material: m² por el precio del volumen que pidas",
                              f"Envío por rollo: {t.TARIFAS_TEXTO} según tu estado",
                              "Con 50 m² o más pagas precio de rollo completo",
                              "El flete exacto se confirma con tu dirección"),
                  "titulo_envio": "Costo de envío por estado",
                  "lede_envio": ("El envío se cobra por rollo de 50 m². Un pedido de 25 a 50 m² viaja en 1 rollo; de 51 a "
                                 "100 m², en 2. En Tampico, Madero y Altamira puedes recoger en el showroom sin flete."),
                  "nota_envio": "Te confirmamos el costo exacto con tu código postal antes de pagar."},
    "ciudades": {"titulo": "Envíos a tu ciudad con precio puesto", "items": CIUDADES,
                 "lede": ("Precio puesto con el modelo más económico, envío incluido. Enviamos a los 32 estados; estas son "
                          "las ciudades con guía propia."),
                 "perros": ('¿Tienes perros? Lee <a href="/pasto-sintetico/perros">qué pasto sintético conviene para '
                            "mascotas</a>.")},
    "comparativa": {"titulo": "Comparativa de modelos por altura, peso y precio",
                    "nota": ("Rollos de 2 m de ancho, 50 m² por rollo. Precios por rollo completo con IVA incluido. El "
                             "envío se suma según tu estado.")},
    "obras": {"titulo": "Pasto sintético instalado en casas reales", "figuras": OBRAS,
              "nota": ("Con sombra total o donde se estanca el agua, primero hay que resolver el drenaje: si no, el "
                       "pasto sintético se ve mal en pocos meses. Te lo decimos antes de venderte.",
                       "Antes de comprar")},
    "pedido": {"titulo": "Cómo comprar pasto sintético en línea", "pasos": PASOS},
    "instalar": {"titulo": "Cómo instalar pasto sintético tú mismo", "pasos": DIY,
                 "lede": "Un jardín de 25 a 50 m² se instala en un día. Estos son los cinco pasos básicos.",
                 "guia": '<a href="/blog/como-instalar-pasto-sintetico">Ver la guía completa paso a paso</a>'},
    "faq": {"titulo": "Preguntas frecuentes sobre pasto sintético", "preguntas": PREGUNTAS},
    "cierre": {"titulo": "¿Estás en Tampico, Madero o Altamira?",
               "lede": (f'Visita el showroom en {datos.CALLE_CORTA}, Cd. Madero. Vendemos desde 2 m² sin flete e '
                        'instalamos en Tampico, Madero y Altamira: <a href="/pasto-sintetico-tampico">venta e '
                        'instalación en Tampico</a> · <a href="/pasto-sintetico-tampico#showroom">cómo llegar al '
                        "showroom</a>."),
               "mensaje": datos.MENSAJES["pasto-sintetico"]},
    "barra": {"nombre": "Pasto sintético · 9 modelos", "precio": f"Desde {DESDE}/m²", "rollo": BARATO["rollo"]},
    "default": DEFAULT,
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
}
