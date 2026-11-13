"""Contenido de /pasto-sintetico-tampico (venta en showroom e instalación en Tampico, Madero y Altamira). Solo datos:
la plantilla es tools/site/plantillas/servicio.py (la de pasto en rollo, con opciones, tabla de modelos, cotizador de la
tienda y visita al showroom).

Modelos y precios de tools/pasto/data.py; instalado de datos.PRECIOS["sintetico_instalado_m2"]; domicilio, horario y
promesa de datos.py. Título, descripción, canonical, Open Graph, LocalBusiness/Store, Service y migas: los que
publicaba tools/pasto/local.py; FAQPage de las preguntas visibles (sin HowTo ni SpeakableSpecification, como en
main). Los 9 modelos en existencia; para llevar hoy solo Toscana 18 y 28 (data.MODELOS[...]["stock"]). PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero, dinero_exacto
from contenido import seo
from contenido import respuestas

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico-tampico"
GAL = t.GAL
NEGOCIO = f"{SITE}/#negocio"
INST_MIN, INST_MAX = datos.PRECIOS["sintetico_instalado_m2"]
INST_MIN_TXT, INST_MAX_TXT = dinero_exacto(INST_MIN), dinero_exacto(INST_MAX)
MIN_RETAIL = min(m["rollo"] for m in data.MODELOS)
STOCK = [m for m in data.MODELOS if m["stock"]]
HOY = " y ".join(m["nombre"] for m in STOCK)
T18, T28 = data.BY_SLUG["toscana-18"], data.BY_SLUG["toscana-28"]
APPLE_MAPS = f"https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&q=Viveros%20Terra"
DOMICILIO = f"{datos.CALLE}, {datos.COLONIA}, {datos.CP} Cd. Madero, frente a Walmart"
MAX_RETAIL = max(m["t1"] for m in data.MODELOS)
# Tienda, subproyecto 1 (2026-11-12, docs/superpowers/specs/2026-11-12-tampico-material-primero-design.md): el material
# primero. Antes, «Pasto Sintético Tampico Instalado desde $446.60/m²»: quien busca el material veía el precio más alto.
TITULO = f"Pasto Sintético Tampico desde ${MIN_RETAIL}/m² · Material o Instalado"
DESCRIPCION = (f"Compra pasto sintético en Tampico desde ${MIN_RETAIL}/m², cortado a tu medida; {HOY} para llevar hoy en "
               f"Cd. Madero. Instalado desde {INST_MIN_TXT}/m².")
OG_IMG = f"{SITE}{GAL}/obra-residencial-tampico.webp"
MENSAJE = datos.MENSAJES["pasto-sintetico"]
MENSAJE_MATERIAL = "Hola, quiero comprar pasto sintético en el showroom. ¿Tienen existencia?\nModelo: ___\nMetros: ___"

PREGUNTAS = (
    ("¿Dónde comprar pasto sintético en Tampico?",
     f"En Viveros Terra, en {datos.CALLE}, {datos.COLONIA}, Cd. Madero, frente a Walmart. Tenemos {HOY} en existencia "
     "para llevar hoy; los otros 7 modelos también están en existencia y llegan en 3 a 5 días. Atendemos de lunes a "
     "viernes de 9 a 18 h y sábado de 9 a 14 h."),
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
    ("¿Puedo instalarlo yo mismo?",
     "Sí. Te vendemos el material cortado a tu medida y el kit para instalarlo: pegamento de contacto, cinta de unión, "
     "clavos de fijación y una guía paso a paso. Lee también <a href=\"/blog/como-instalar-pasto-sintetico\">cómo "
     "instalar pasto sintético</a>. Si prefieres que lo hagamos nosotros, cotizamos la instalación."),
    ("¿Cuánto cuesta instalar pasto sintético en Tampico?",
     f"La instalación cuesta desde {INST_MIN_TXT}/m² y hasta {INST_MAX_TXT}/m² en modelos premium. Incluye el material, la "
     "colocación, las uniones, las orillas y el cepillado. Si tu espacio necesita retiro de lo existente, nivelación o "
     "base drenante, lo revisamos en la visita y te lo cotizamos aparte antes de empezar."),
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
     "texto": ("Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso. "
               f"{datos.VISITA_COSTO_CORTO}.")},
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
    "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": f"{INST_MIN:.2f}", "highPrice": f"{INST_MAX:.2f}",
               "unitText": "m²"},
}
MATERIAL = {
    "@type": "Product", "@id": f"{URL}#material", "name": "Pasto sintético en rollo (material) en Tampico",
    "description": (f"{len(data.MODELOS)} modelos de pasto sintético de {data.MODELOS[0]['mm']} a {data.MODELOS[-1]['mm']} mm, "
                    "cortados a tu medida desde 2 m², en el showroom de Cd. Madero."),
    "image": OG_IMG,
    "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": f"{MIN_RETAIL:.2f}",
               "highPrice": f"{MAX_RETAIL:.2f}", "offerCount": len(data.MODELOS), "availability": "https://schema.org/InStock",
               "seller": {"@id": NEGOCIO}, "unitText": "m²"},
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
    # Entrega C de experiencia: CTA de la banda de garantía (antes, 7.4 pantallas del cotizador al cierre sin CTA).
    # Tienda, subproyecto 1: CTA del material tras la tabla de precios (la prueba bajó y dejaba 6.8 pantallas sin CTA).
    "ctas": {"precio": (MENSAJE_MATERIAL, "Cotizar mi material"), "prueba": (MENSAJE, "Cotizar mi pasto sintético"),
             "garantia": (MENSAJE, "Cotizar pasto sintético instalado")},
    "respuesta": respuestas.de("/pasto-sintetico-tampico"),  # SEO fase 1: respuesta directa bajo la portada
    "tipo": "servicio-sintetico",
    "prefijo": "sintetico",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large", "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", OG_IMG), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "jsonld": {"producto": SERVICIO, "nodos": (MATERIAL,), "migas": MIGAS_LD},
    # Tienda, subproyecto 1: el material antes que la prueba (spec 2026-11-12-tampico-material-primero).
    "orden": ("opciones", "cotizador", "precio", "prueba", "obras", "proceso", "garantia", "pago", "faq", "visita"),
    "migas": (("Inicio", "/"), ("Pasto sintético en Tampico", None)),
    "portada": {
        "kicker": "Pasto sintético · Tampico, Madero y Altamira",
        "pos": "50% 62%",
        "dato": "Los 9 modelos en existencia",
        "enlaces": (("Calcula tu material", "#cotizador"), ("Cómo llegar al showroom", "#showroom")),
        "h1": 'Pasto sintético en Tampico <span class="vt-serif">material o instalado</span>',
        "lede": (f"Llévate el material del showroom en Cd. Madero desde {dinero(MIN_RETAIL)}/m² o déjanos la instalación "
                 f"completa. En la región desde {datos.DESDE}."),
        "etiqueta": {
            "codigo": "Sintético · Tampico", "aviso": "Con IVA", "nombre": "Pasto sintético en rollo",
            "antes": "Solo el material · desde", "monto": dinero(MIN_RETAIL), "unidad": "/m²",
            "filas": (("Toscana 18 y 28", "para llevar hoy"),
                      ("Instalado con material y colocación", f"desde {INST_MIN_TXT} /m²")),
        },
        "mensaje": MENSAJE,
        "foto": {"src": f"{GAL}/obra-residencial-tampico-sm.webp", "srcset": f"{GAL}/obra-residencial-tampico-sm.webp "
                 f"560w, {GAL}/obra-residencial-tampico.webp 960w", "sizes": "(min-width: 1024px) 560px, 100vw",
                 "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Losas de piedra con franjas de pasto sintético junto a un muro de piedra iluminado",
                 "lugar": "Patio con losas y pasto sintético", "etapa": "Obra de Viveros Terra"},
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
            {"cta": "Cotizar el material", "rotulo": "Opción 1", "titulo": "Compras el material", "precio": MIN_RETAIL, "unidad": "/m²",
             "detalle": "Material con IVA, cortado a tu medida", "rec": True,
             "puntos": ("Desde 2 m², cortado a tu medida", f"{HOY} para llevar hoy",
                        "Kit de pegamento, cinta y clavos", "Envío local según tu colonia; te lo cotizamos."),
             "mensaje": MENSAJE_MATERIAL},
            {"cta": "Cotizar la instalación", "rotulo": "Opción 2", "titulo": "Nosotros lo instalamos", "precio": INST_MIN, "unidad": "/m²",
             "detalle": "Material y colocación",
             "puntos": (datos.VISITA_COSTO_CORTO, "Colocación, uniones, orillas y cepillado",
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
                 f"colocación de {INST_MIN_TXT} a {INST_MAX_TXT}/m² según el modelo."),
        "tabla": {"columnas": ("Modelo", "2 a 9 m²", "10 a 49 m²", "Rollo 50 m²"),
                  "filas": tuple(_fila_precio(m) for m in data.MODELOS)},
        "caption": ("Si el modelo no está en el showroom, llega en 3 a 5 días hábiles. Lo enviamos en cuanto confirmas tu "
                    f"pedido con el pago. Precios vigentes en {datos.ANIO}."),
    },
    "cotizador": {
        "titulo": "Calcula tu material y llévatelo", "titulo_calc": "Calculadora de material", "modelo": "toscana-28",
        "m2": 20, "local": True,  # venta local: showroom o envío local por colonia, sin flete nacional por estado
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
        "banda": True,  # Entrega C: banda oscura a media página con la garantía de fábrica (tools/pasto/data.py)
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
        "lede": f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito.",
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
    "barra": {"nombre": "Pasto sintético en Tampico", "precio": f"Material desde {dinero(MIN_RETAIL)}/m²"},
}

M_NEGOCIO = ("SEO fase 1: la página ya no redefine el negocio con otros campos (LocalBusiness + Store con dirección, "
             "coordenadas y ofertas que apuntaban a productos de otras páginas): lleva el nodo mínimo de la entidad única "
             "y el Service de instalación con su AggregateOffer; el nodo completo vive en la home y en /vivero-tampico.")
PARIDAD = {
    "jsonld": {tipo: M_NEGOCIO for tipo in ("Store", "PostalAddress", "GeoCoordinates", "Offer")},
    "reemplazos": {"$385": f"${int(INST_MIN)}", "$650": INST_MAX_TXT,  # la captura guarda la parte entera
                   # Tienda, subproyecto 1 (2026-11-12): el H1 nombra primero el material.
                   "Pasto sintético en Tampico venta e instalación": "Pasto sintético en Tampico material o instalado"},  # la captura guarda la parte entera
    "meta": seo.paridad(TITULO, DESCRIPCION, {
        "description": (DESCRIPCION, "Decisión del dueño (2026-11-08): el pasto sintético instalado era más IVA; se publica el precio final con IVA, $446.60 a $754/m²."),
        "og:description": (DESCRIPCION, "Decisión del dueño (2026-11-08): el pasto sintético instalado era más IVA; se publica el precio final con IVA, $446.60 a $754/m².")}),
    "retirados": {
        "$250": ("Decisión del dueño (2026-11-07): el envío local en Tampico, Madero y Altamira no tiene precio fijo; "
                 "ahora dice “Envío local según tu colonia; te lo cotizamos.”"),
    },
}
# Decisiones del dueño (2026-11-07): el testimonio de Sofía R. es real y se publica con permiso (textual, en
# datos.OPINION_SINTETICO_TAMPICO); no se ofrece financiamiento propio a instaladores; el envío local no tiene precio fijo.
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Entrada recortada: «enviamos a todo México desde 2012» sale del hero (está en la tienda /pasto-sintetico, enlazada).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: las dos opciones con texto de botón propio; nombres de la lista unificados («Mi lista», «Agregar a mi lista»).'

# Lo que cambia por la Entrega C de experiencia (ritmo y movimiento).
PARIDAD["ritmo"] = 'Entrega C de experiencia (2026-11-10), ritmo y movimiento: banda oscura de garantía (garantía de fábrica de tools/pasto/data.py) con CTA «Cotizar pasto sintético instalado»; fila «Cotizar mi pasto sintético» tras la prueba (antes, 6 pantallas sin CTA); relleno y fondos alternados; opiniones en fila en celular; primera pregunta cerrada; revelado por scroll de encabezados y figuras y balanceo de la etiqueta en escritorio.'
