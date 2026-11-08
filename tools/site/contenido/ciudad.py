"""Contenido de las 11 páginas /pasto-sintetico/envio/<ciudad>. Solo datos: la plantilla es plantillas/tienda_guia.py.

Textos de cada ciudad (intro, clima, modelos, preguntas) de tools/pasto/ciudades.py; precios, zonas y fletes de
tools/pasto/data.py; mensualidades de tools/pasto/mensualidades.py. Título, descripción, canonical, Open Graph,
Product con envío al estado y migas: los que publicaba tools/pasto/ciudad.py. PARIDAD: tests/test_paridad.py.
"""
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
from ciudades import CIUDADES
from componentes import dinero
from esquema import breadcrumb_schema

CLAVES = tuple(x["slug"] for x in CIUDADES)
POR_SLUG = {x["slug"]: x for x in CIUDADES}
SITE = data.SITE
GAL = t.GAL
FOTO = "obra-proyecto-02"
LLEGADA = (
    {"titulo": "Confirmas y pagas", "quien": "tu", "cuando": "Al confirmar",
     "texto": f"Transferencia o link de pago con tarjeta. Factura {datos.FACTURA}."},
    {"titulo": "Sale en rollo", "quien": "nosotros", "cuando": "1 a 2 días hábiles",
     "texto": "Rollo de 2 m de ancho, enrollado y protegido, con guía de rastreo."},
    {"titulo": "Revisa al recibir", "quien": "tu", "cuando": "Al recibir",
     "texto": ("Que el empaque venga completo y que los metros coincidan con tu pedido. Si algo no está bien, avísanos "
               "por WhatsApp con fotos.")},
)
INSTALACION = ("La instalación profesional es solo en Tampico, Ciudad Madero y Altamira. Un patio de 25 a 50 m² se "
               "instala en un día con dos personas: te mandamos la guía con el pedido "
               '(<a href="/blog/como-instalar-pasto-sintetico">guía de instalación paso a paso</a>).')


def _producto(x, zona, url, desde):
    m = t.barato()
    return {
        "@type": "Product", "name": f"Pasto sintético con envío a {x['nombre_largo']}",
        "brand": {"@type": "Brand", "name": datos.NOMBRE}, "image": [f"{SITE}{GAL}/{FOTO}.webp"],
        "description": f"Pasto sintético en rollo de 50 m² con envío a {x['nombre_largo']}, desde ${desde}/m² puesto en tu casa.",
        "offers": {
            "@type": "Offer", "priceCurrency": "MXN", "price": str(m["rollo"]),
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(m["rollo"]), "priceCurrency": "MXN",
                                   "unitText": "m²"},
            "availability": "https://schema.org/InStock", "url": url,
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": str(data.ZONAS[zona]), "currency": "MXN"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX", "addressRegion": x["estado"]},
                "deliveryTime": {"@type": "ShippingDeliveryTime", "transitTime": {
                    "@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
            },
        },
    }


def _preguntas_envio(x, zona):
    """Encabezados en pregunta (spec §3.3, ciudad): costo, tiempo, mínimo, cómo elegir sin muestra e instalación."""
    n = x["nombre"]
    return (
        (f"¿Cuánto cuesta el envío a {n}?",
         f"{dinero(data.ZONAS[zona])} por rollo de 50 m² ({data.ZONA_ESTADOS[zona][0]}). Si pides de 51 a 100 m² son dos "
         "rollos y dos fletes. El envío nunca va escondido en el precio."),
        (f"¿Cuánto tarda en llegar a {n}?", "De 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo."),
        ("¿Cuál es la compra mínima?",
         "25 m² para envío nacional, medio rollo. Los cortes de 2 a 9 m² son solo en el showroom de Cd. Madero."),
        ("¿Cómo elijo el modelo sin ver una muestra?",
         "Como no ofrecemos muestras físicas, cada ficha tiene fotos de cerca, altura, peso y la comparativa con sus dos "
         "vecinos. Si dudas entre dos, mándanos una foto de tu espacio por WhatsApp y te decimos cuál conviene."),
        ("¿Lo instalo yo o lo instalan ustedes?", INSTALACION),
    )


def contenido(x):
    zona = data.zona_de(x["estado"])
    url = f"{SITE}/pasto-sintetico/envio/{x['slug']}"
    m = t.barato()
    desde = data.landed_m2(m, zona)
    estado = data.estado_slug(x["estado"])
    titulo = f"Pasto sintético en {x['nombre']} con envío · desde ${desde}/m² | Viveros Terra"
    descripcion = (f"Pasto sintético con envío a {x['nombre_largo']} desde ${desde}/m² puesto en tu casa. 9 modelos de "
                   "10 a 35 mm, entrega en 3 a 5 días hábiles y factura.")
    mensaje = f"Hola, quiero cotizar pasto sintético con envío a {x['nombre']}.\nMetros aprox.: ___\nModelo: ___"
    return {
        "tipo": "ciudad",
        "meta": {"title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
                 "canonical": url,
                 "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                        ("og:description", descripcion), ("og:image", f"{SITE}{GAL}/{FOTO}.webp"),
                        ("og:locale", "es_MX")),
                 "twitter": (("twitter:card", "summary_large_image"),)},
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"),
                                      (f"Envío a {x['nombre']}", url)]), _producto(x, zona, url, desde)),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (f"Envío a {x['nombre']}", None)),
        "portada": {
            "kicker": f"Envío a {x['nombre_largo']} · 9 modelos en existencia",
            "h1": f'Pasto sintético en {x["nombre"]} <span class="vt-serif">con envío a tu casa</span>',
            "respuesta": (f"Te enviamos el pasto sintético a {x['nombre_largo']} en 3 a 5 días hábiles. Desde "
                          f"<b>${desde}/m²</b> ya con envío, en rollo de 50 m² con factura. Tú lo instalas con nuestra "
                          "guía."),
            "mensaje": mensaje,
            "href_modelos": f"/pasto-sintetico?estado={estado}#modelos",
            "texto_modelos": "Ver los 9 modelos con precio puesto",
            "foto": {"src": f"{GAL}/{FOTO}-sm.webp", "srcset": f"{GAL}/{FOTO}-sm.webp 560w, {GAL}/{FOTO}.webp 960w",
                     "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                     "alt": "Jardín residencial con pasto sintético de nuestra colección",
                     "lugar": "Jardín residencial", "etapa": "Pasto de la colección instalado"},
            "datos": ((f"Puesto en {x['nombre']}", f"desde ${desde}/m²", f"Con {m['nombre']}"),
                      ("Flete por rollo", dinero(data.ZONAS[zona]), data.ZONA_ESTADOS[zona][0]),
                      ("Entrega", "3 a 5 días", "Hábiles, con guía de rastreo"),
                      ("Compra mínima", "25 m²", "Medio rollo"),
                      ("Factura", datos.FACTURA, "Persona física o moral"),
                      ("Vendemos a todo México", f"Desde {datos.SINTETICO_NACIONAL_DESDE}", f"Showroom en {datos.CALLE_CORTA}")),
        },
        "secciones": (
            {"tipo": "totales", "id": "precios", "rotulo": "Precios", "titulo": f"Cuánto cuesta con envío a {x['nombre']}",
             "lede": x["intro"], "modelo": m, "zona": zona,
             "notas": ("El flete exacto se confirma con tu código postal antes de pagar.",
                       "Mensualidades con tarjeta de crédito; el total en mensualidades es mayor que el de contado. "
                       f'Calcula tu plan en el <a href="/pasto-sintetico?estado={estado}#cotizador">cotizador</a>.')},
            {"tipo": "preguntas", "id": "envio-dudas", "rotulo": "Antes de comprar",
             "titulo": f"Envío a {x['nombre']}: costo, tiempo y mínimo", "items": _preguntas_envio(x, zona)},
            {"tipo": "modelos", "id": "modelos", "rotulo": "Clima", "titulo": f"El pasto que conviene en {x['nombre']}",
             "lede": x["clima"], "items": x["modelos"], "zona": zona, "lugar": x["nombre"]},
            {"tipo": "pasos", "id": "envio", "rotulo": "Envío", "titulo": "Cómo te llega el pedido", "items": LLEGADA},
            {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": f"Preguntas frecuentes en {x['nombre']}",
             "preguntas": tuple(x["faqs"])},
        ),
        "cierre": {"titulo": f"Cotiza tu pedido a {x['nombre']}",
                   "lede": (f"Elige modelo y metros en la tienda: el precio ya incluye el envío a {x['nombre_largo']}. "
                            f'<a href="/pasto-sintetico?estado={estado}#cotizador">Calcular mi pedido</a>.'),
                   "mensaje": mensaje},
    }


def paridad(x):
    """La sección "Instálalo tú" pasa a la pregunta de instalación. En la zona B (Monterrey y Veracruz), 12 mensualidades
    sobre $19,998 son 1,666.5: la página decía $1,666 (round() de Python) y el cotizador cobra $1,667 (Math.round);
    desde 2b Python redondea como el JS."""
    reemplazos = {"Instalarlo tú mismo es sencillo": "¿Lo instalo yo o lo instalan ustedes?"}
    if data.zona_de(x["estado"]) == "B":
        reemplazos["$1,666"] = "$1,667"
    return {"reemplazos": reemplazos, "retirados": {}}


def pagina(slug):
    return SimpleNamespace(CONTENIDO=contenido(POR_SLUG[slug]), PARIDAD=paridad(POR_SLUG[slug]))
