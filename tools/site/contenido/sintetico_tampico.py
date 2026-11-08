"""Contenido de /pasto-sintetico-tampico (venta en showroom e instalación en Tampico, Madero y Altamira). Solo datos:
la plantilla es tools/site/plantillas/servicio.py (la de pasto en rollo, con opciones, tabla de modelos, cotizador de la
tienda y visita al showroom).

Modelos y precios de tools/pasto/data.py; instalado de datos.PRECIOS["sintetico_instalado_m2"]; domicilio, horario y
promesa de datos.py. Título, descripción, canonical, Open Graph, LocalBusiness/Store, Service y migas: los que
publicaba tools/pasto/local.py; FAQPage de las preguntas visibles y HowTo de los 5 pasos visibles. Los 9 modelos en
existencia; para llevar hoy solo Toscana 18 y 28 (data.MODELOS[...]["stock"]). PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico-tampico"
GAL = t.GAL
NEGOCIO = f"{SITE}/#negocio"
INST_MIN, INST_MAX = datos.PRECIOS["sintetico_instalado_m2"]
MIN_RETAIL = min(m["rollo"] for m in data.MODELOS)
STOCK = [m for m in data.MODELOS if m["stock"]]
HOY = " y ".join(m["nombre"] for m in STOCK)
T18, T28 = data.BY_SLUG["toscana-18"], data.BY_SLUG["toscana-28"]
APPLE_MAPS = f"https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&q=Viveros%20Terra"
DOMICILIO = f"{datos.CALLE}, {datos.COLONIA}, {datos.CP} Cd. Madero, frente a Walmart"
TITULO = "Pasto Sintético en Tampico: Venta e Instalación | Viveros Terra"
DESCRIPCION = (f"Venta e instalación de pasto sintético en Tampico, Madero y Altamira. Showroom en Cd. Madero, material "
               f"desde ${MIN_RETAIL}/m² e instalado desde ${INST_MIN}/m².")
OG_IMG = f"{SITE}{GAL}/obra-residencial-tampico.webp"
MENSAJE = datos.MENSAJES["pasto-sintetico"]

PREGUNTAS = (
    ("¿Dónde comprar pasto sintético en Tampico?",
     f"En Viveros Terra, en {datos.CALLE}, {datos.COLONIA}, Cd. Madero, frente a Walmart. Tenemos {HOY} en existencia "
     "para llevar hoy; los otros 7 modelos también están en existencia y llegan en 3 a 5 días. Atendemos de lunes a "
     "viernes de 9 a 18 h y sábado de 9 a 14 h."),
    ("¿Cuánto cuesta instalar pasto sintético en Tampico?",
     f"La instalación cuesta desde ${INST_MIN}/m² y hasta ${INST_MAX}/m² en modelos premium. Incluye el material, la "
     "colocación, las uniones, las orillas y el cepillado. Si tu espacio necesita retiro de lo existente, nivelación o "
     "base drenante, lo revisamos en la visita y te lo cotizamos aparte antes de empezar."),
    ("¿Cuánto cuesta el pasto sintético por m² en Tampico?",
     f"Solo el material cuesta desde ${MIN_RETAIL}/m² en rollo completo. Toscana 18 va de ${T18['rollo']}/m² en rollo a "
     f"${T18['t1']}/m² en cortes de 2 a 9 m². Toscana 28 va de ${T28['rollo']}/m² a ${T28['t1']}/m². Los precios "
     "incluyen IVA."),
    ("¿Cuál es la compra mínima?",
     "En el showroom vendemos desde 2 m². El rollo mide 2 m de ancho, así que los cortes van de 2 en 2 m²."),
    ("¿Puedo recogerlo el mismo día?",
     f"Sí, si es {HOY}. Te recomendamos confirmar existencia por WhatsApp antes de pasar. Los demás modelos llegan en 3 "
     "a 5 días hábiles. Los pedimos en cuanto confirmas tu pedido con el pago."),
    ("¿Hacen envío dentro de Tampico, Madero y Altamira?",
     "Sí. Envío local según tu colonia; te lo cotizamos."),
    ("¿Qué pasto sintético conviene para el clima de Tampico?",
     "Uno con base perforada que drene rápido, porque de junio a septiembre llueve mucho. Para jardín familiar, Toscana "
     "28. Para perros o mucho uso, Irlanda 25 o Capri 20. Para terrazas y balcones, Aruba 10 o Toscana 18. Compara los "
     'modelos en la <a href="/pasto-sintetico#comparativa">tabla de la colección</a>.'),
    ("¿Cuánto dura el pasto sintético?",
     "Bien instalado dura de 8 a 12 años en uso residencial. La garantía de fábrica va de 3 a 8 años según el modelo."),
    ("¿Cómo se paga y dan factura?",
     f"Aceptamos efectivo, transferencia y tarjeta de débito o crédito. {datos.ANTICIPO} Emitimos factura "
     f"{datos.FACTURA} para persona física o moral."),
    ("¿Venden fuera de Tampico?",
     "Sí. Enviamos el material a todo México en 3 a 5 días hábiles. La instalación es solo en Tampico, Madero y "
     'Altamira. Ve la <a href="/pasto-sintetico">tienda con envío nacional</a>.'),
)

PASOS = (
    {"titulo": "Visita y medición", "quien": "nosotros", "cuando": "Antes de cotizar",
     "texto": "Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso."},
    {"titulo": "Preparación del terreno", "quien": "nosotros", "cuando": "Si hace falta",
     "texto": ("Si hace falta, retiramos lo existente, nivelamos y ponemos grava fina para que drene. Se cotiza aparte "
               "según tu espacio.")},
    {"titulo": "Colocación", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Extendemos el rollo, cortamos al perímetro y unimos los tramos con cinta y adhesivo."},
    {"titulo": "Orillas y acabados", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Fijamos las orillas para que no se levanten y cuidamos los bordes con andadores y jardineras."},
    {"titulo": "Cepillado y entrega", "quien": "juntos", "cuando": "Al terminar",
     "texto": "Cepillamos la fibra para que quede de pie, limpiamos y revisamos contigo el área antes de irnos."},
)


def _fila_precio(m):
    disponible = "Para llevar hoy" if m["stock"] else "3 a 5 días"
    return (f'<a href="/pasto-sintetico/{m["slug"]}">{m["nombre"]}</a><br><small>{m["mm"]} mm · {disponible}</small>',
            f"${m['t1']}", f"${m['t2']}", f"<b>${m['rollo']}</b>")


SERVICIO = {
    "@type": "Service", "@id": f"{URL}#instalacion", "name": "Instalación de pasto sintético en Tampico",
    "serviceType": "Instalación de pasto sintético", "provider": {"@id": NEGOCIO},
    "areaServed": [{"@type": "City", "name": c} for c in ("Tampico", "Ciudad Madero", "Altamira")],
    "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(INST_MIN), "highPrice": str(INST_MAX),
               "unitText": "m²"},
}
NEGOCIO_LD = {
    "@type": ["LocalBusiness", "Store"], "@id": NEGOCIO, "name": datos.NOMBRE, "url": SITE,
    "telephone": datos.TELEFONO_TEL, "priceRange": "$$", "foundingDate": datos.FUNDACION,
    "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE,
                "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas", "postalCode": datos.CP,
                "addressCountry": "MX"},
    "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
    "hasMap": datos.MAPS_URL,
    "knowsAbout": ["Pasto sintético", "Instalación de pasto sintético", "Pasto en rollo", "Jardinería"],
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@id": f"{SITE}/pasto-sintetico/{m['slug']}#producto"}}
                   for m in data.MODELOS] + [{"@type": "Offer", "itemOffered": {"@id": f"{URL}#instalacion"}}],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Pasto sintético en Tampico", "item": URL},
]}
OBRAS = tuple({"src": f"{GAL}/{n}-sm.webp", "srcset": f"{GAL}/{n}-sm.webp 560w, {GAL}/{n}.webp 960w",
               "sizes": "(min-width: 1024px) 400px, 80vw", "ancho": w, "alto": h, "alt": alt, "numero": i,
               "lugar": cap, "etapa": "Obra en la región"}
              for i, (n, w, h, alt, cap) in enumerate(data.OBRAS, 2))

CONTENIDO = {
    "tipo": "servicio-sintetico",
    "prefijo": "sintetico",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large", "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", OG_IMG), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "jsonld": {"producto": NEGOCIO_LD, "nodos": (SERVICIO,), "migas": MIGAS_LD,
               "howto": "Cómo instalamos pasto sintético en Tampico", "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Pasto sintético en Tampico", None)),
    "portada": {
        "kicker": "Pasto sintético · Tampico, Madero y Altamira",
        "h1": 'Pasto sintético en Tampico <span class="vt-serif">venta e instalación</span>',
        "lede": (f"Llévate el material desde nuestro showroom en Cd. Madero o déjanos la instalación completa. Vendemos e "
                 f"instalamos en la región desde {datos.DESDE} y enviamos a todo México desde "
                 f"{datos.SINTETICO_NACIONAL_DESDE}."),
        "etiqueta": {
            "codigo": "Sintético · Tampico", "aviso": "Con IVA", "nombre": "Pasto sintético instalado",
            "antes": "Material y colocación · desde", "monto": dinero(INST_MIN), "unidad": "/m²",
            "filas": (("Solo el material, en showroom", f"desde {dinero(MIN_RETAIL)} /m²"),
                      ("Toscana 18 y 28", "para llevar hoy")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Los 9 modelos en existencia · <a href="#cotizador">calcula tu material</a> · '
                    '<a href="#showroom">cómo llegar al showroom</a>'),
        "foto": {"src": f"{GAL}/obra-proyecto-02-sm.webp", "srcset": f"{GAL}/obra-proyecto-02-sm.webp 560w, "
                 f"{GAL}/obra-proyecto-02.webp 960w", "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960,
                 "alto": 1280, "numero": 1, "alt": "Residencia moderna con escalones de piedra y pasto sintético hasta el deck",
                 "lugar": "Residencia con deck", "etapa": "Obra de Viveros Terra"},
    },
    "prueba": {
        "titulo": "Pasto sintético instalado en la región",
        "lede": "Obras con pasto de nuestra colección en casas de Tampico, Madero y Altamira.",
        "figuras": OBRAS,
        "titulo_opinion": "Lo que dicen nuestros clientes",
        "opiniones": datos.OPINION_SINTETICO_TAMPICO,
        "nota": ("Si el terreno no drena, el pasto sintético se encharca y huele en pocos meses. Por eso revisamos la "
                 "base en la visita y, si hace falta grava, te la cotizamos aparte antes de empezar.", "En la visita"),
    },
    "opciones": {
        "titulo": "Compra el material o te lo instalamos",
        "items": (
            {"rotulo": "Opción 1", "titulo": "Compras el material", "precio": MIN_RETAIL, "unidad": "/m²",
             "detalle": "Material con IVA, cortado a tu medida",
             "puntos": ("Desde 2 m², cortado a tu medida", f"{HOY} para llevar hoy",
                        "Kit de pegamento, cinta y clavos", "Envío local según tu colonia; te lo cotizamos."),
             "mensaje": "Hola, quiero comprar pasto sintético en el showroom. ¿Tienen existencia?\nModelo: ___\nMetros: ___"},
            {"rotulo": "Opción 2", "titulo": "Nosotros lo instalamos", "precio": INST_MIN, "unidad": "/m²",
             "detalle": "Material y colocación", "rec": True,
             "puntos": ("Visita y cotización sin compromiso", "Colocación, uniones, orillas y cepillado",
                        "Material con garantía de fábrica"),
             "nota": ("Cada terreno es distinto. Si el tuyo necesita retiro, nivelación o base drenante, lo vemos en la "
                      "visita y te lo cotizamos aparte, antes de empezar y sin sorpresas."),
             "mensaje": ("Hola, quiero cotizar la instalación de pasto sintético. ¿Pueden venir a medir?\nColonia: ___\n"
                         "Metros aprox.: ___")},
        ),
    },
    "precio": {
        "titulo": "Precio del pasto sintético en Tampico",
        "lede": (f"Precio por m² del material, con IVA. Entre más metros, menor precio. Instalación con material y "
                 f"colocación de ${INST_MIN} a ${INST_MAX}/m² según el modelo."),
        "tabla": {"columnas": ("Modelo", "2 a 9 m²", "10 a 49 m²", "Rollo 50 m²"),
                  "filas": tuple(_fila_precio(m) for m in data.MODELOS)},
        "caption": ("Si el modelo no está en el showroom, llega en 3 a 5 días hábiles. Lo enviamos en cuanto confirmas tu "
                    f"pedido con el pago. Precios vigentes en {datos.ANIO}."),
    },
    "cotizador": {
        "titulo": "Calcula tu material y llévatelo", "titulo_calc": "Calculadora de material", "modelo": "toscana-28",
        "m2": 20,
        "aparte": (
            ("Kit para instalarlo tú", ("Pegamento de contacto industrial, 4 L", "Cinta de unión profesional, 100 m",
                                       "Clavos de fijación de 2″, caja de 5 kg", "Guía de instalación paso a paso"),
             "Un litro de pegamento rinde para unos 6 m de unión. Te ayudamos a calcular cuánto necesitas."),
            ("¿Instalas o construyes?", (),
             "Instaladores y constructoras tienen precio por volumen y existencia prioritaria. Escríbenos por WhatsApp "
             "con tus metros por obra."),
        ),
    },
    "proceso": {"titulo": "Cómo instalamos en Tampico y Madero",
                "lede": "Cotizamos después de ver el terreno, porque la base es lo que decide cuánto dura el pasto.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de fábrica de 3 a 8 años, según el modelo.", "grande": "3–8", "unidad": "años",
        "resumen": "La gestionamos nosotros, con el material que instalamos o que compras en el showroom.",
        "puntos": (("Garantía de fábrica de 3 a 8 años según el modelo; la gestionamos nosotros.", True),
                   ("Bien instalado dura de 8 a 12 años en uso residencial.", True),
                   ("Si tu terreno necesita retiro, nivelación o base drenante, te lo cotizamos aparte antes de empezar.",
                    True),
                   (f"Factura {datos.FACTURA} para persona física o moral.", True),
                   ("Los cortes a medida no tienen devolución.", False)),
        "pie": '<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} El resto se liquida según lo acordado en tu cotización, de contado o en mensualidades "
                 "con tarjeta de crédito."),
        "puntos": ("Recibes el precio del material, la instalación y la preparación del terreno por separado.",
                   "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
                   ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos "
                    'antes de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>')),
    },
    "faq": {"titulo": "Preguntas frecuentes en Tampico", "preguntas": PREGUNTAS},
    "visita": {
        "titulo": "Visítanos en Cd. Madero",
        "lede": f"{datos.REFERENCIA}. Toscana 18 y Toscana 28 para llevar hoy; confirma existencia por WhatsApp antes de pasar.",
        "datos": (("Dirección", datos.CALLE, f"{datos.COLONIA}, {datos.CP} Cd. Madero"),
                  ("Horario", "Lun a vie 9 a 18 h", "Sábado 9 a 14 h"),
                  ("Instalación", "Tampico, Madero", "y Altamira"),
                  ("Envío del material", "Local, por colonia", "Te lo cotizamos · nacional en 3 a 5 días hábiles")),
        "mapas": (("Cómo llegar con Google Maps", datos.MAPS_URL), ("Abrir en Apple Maps", APPLE_MAPS)),
    },
    "cierre": {
        "titulo": "¿No estás en Tampico? Enviamos a todo México",
        "lede": ("Los mismos 9 modelos llegan a cualquier estado en 3 a 5 días hábiles, con factura: "
                 '<a href="/pasto-sintetico">ver la tienda nacional</a>. En Tampico, Madero y Altamira, escríbenos y '
                 "cotizamos la instalación."),
        "mensaje": MENSAJE,
    },
    "barra": {"nombre": "Pasto sintético en Tampico", "precio": f"Instalado desde ${INST_MIN}/m²"},
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {
        "$250": ("Decisión del dueño (2026-11-07): el envío local en Tampico, Madero y Altamira no tiene precio fijo; "
                 "ahora dice “Envío local según tu colonia; te lo cotizamos.”"),
    },
}
# Decisiones del dueño (2026-11-07): el testimonio de Sofía R. es real y se publica con permiso (textual, en
# datos.OPINION_SINTETICO_TAMPICO); no se ofrece financiamiento propio a instaladores; el envío local no tiene precio fijo.
