"""Nodos schema.org de la tienda de pasto sintético (Product, BreadcrumbList, envío, devoluciones y vendedor).

Datos, no HTML: los usan las plantillas de tools/site (fichas, hub, ciudades) y el feed de Merchant (feed.py).
"""
import re

from data import MIN_SHOWROOM_M2, ROLLO_M2, SITE, ZONA_ESTADOS, ZONAS

GAL = "/img/pasto-sintetico/galeria"


def breadcrumb_schema(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)
        ],
    }


# Códigos ISO 3166-2 de los estados (sin «MX-»), para declarar el flete de cada zona en el Offer.
ESTADO_ISO = {
    "Aguascalientes": "AGU", "Baja California": "BCN", "Baja California Sur": "BCS", "Campeche": "CAM",
    "Chiapas": "CHP", "Chihuahua": "CHH", "CDMX": "CMX", "Coahuila": "COA", "Colima": "COL", "Durango": "DUR",
    "Estado de México": "MEX", "Guanajuato": "GUA", "Guerrero": "GRO", "Hidalgo": "HID", "Jalisco": "JAL",
    "Michoacán": "MIC", "Morelos": "MOR", "Nayarit": "NAY", "Nuevo León": "NLE", "Oaxaca": "OAX", "Puebla": "PUE",
    "Querétaro": "QUE", "Quintana Roo": "ROO", "San Luis Potosí": "SLP", "Sinaloa": "SIN", "Sonora": "SON",
    "Tabasco": "TAB", "Tamaulipas": "TAM", "Tlaxcala": "TLA", "Veracruz": "VER", "Yucatán": "YUC", "Zacatecas": "ZAC",
}
TRANSITO = {"@type": "ShippingDeliveryTime",
            "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}}


def envio(zona, estados=None):
    """Flete por rollo de una zona (data.ZONAS) hacia sus estados, o solo hacia `estados` si se dan."""
    regiones = [ESTADO_ISO[e] for e in (estados or ZONA_ESTADOS[zona][1])]
    return {
        "@type": "OfferShippingDetails",
        "shippingRate": {"@type": "MonetaryAmount", "value": str(ZONAS[zona]), "currency": "MXN"},
        "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX", "addressRegion": regiones},
        "deliveryTime": TRANSITO,
    }


# Entrega A del SEO nacional (2026-11-16): un OfferShippingDetails por zona con su flete, en vez de uno sin tarifa.
SHIPPING = [envio(z) for z in ZONAS]
RETURNS = {
    "@type": "MerchantReturnPolicy", "applicableCountry": "MX",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 7, "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
}
# SEO fase 1: el vendedor es la entidad única del sitio por @id (tools/site/entidad.py define el nodo); antes, una
# Organization suelta en cada producto.
SELLER = {"@id": f"{SITE}/#negocio"}


def product_schema(m, *, with_id=True, envios=None):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    props = [
        {"@type": "PropertyValue", "name": "Altura de fibra", "value": m["mm"], "unitText": "mm"},
        {"@type": "PropertyValue", "name": "Peso total", "value": m["peso_num"], "unitText": "g/m²"},
        {"@type": "PropertyValue", "name": "Medida del rollo", "value": "2 × 25 m (50 m²)"},
    ]
    if m["garantia"]:
        props.append({"@type": "PropertyValue", "name": "Garantía", "value": m["garantia"], "unitText": "años"})
    for label, value, unit in m["specstrip"]:
        if label in ("Puntadas por m²", "Dtex"):
            props.append({"@type": "PropertyValue", "name": label, "value": int(value.replace(",", ""))})
    images = [f"{SITE}{GAL}/{m['slug']}-{idx}.webp" for idx, _k, _c in m["gallery"]]
    images.append(f"{SITE}/img/pasto-sintetico/{m['slug']}.jpg")
    desc_plain = strip_tags(m["resumen"])
    product = {
        "@type": "Product", "name": f"Pasto Sintético {m['nombre']}", "sku": f"VT-PST-{m['id'].upper()}",
        "category": "Pasto sintético residencial", "description": desc_plain, "image": images,
        "brand": {"@type": "Brand", "name": "Viveros Terra"}, "color": m["color"], "url": url,
        "additionalProperty": props,
        "offers": oferta(m, url, envios),
    }
    if with_id:
        product["@id"] = f"{url}#producto"
    return product


def _precio_m2(precio, minimo, maximo=None):
    cantidad = {"@type": "QuantitativeValue", "minValue": minimo, "unitCode": "MTK"}
    if maximo:
        cantidad["maxValue"] = maximo
    return {"@type": "UnitPriceSpecification", "price": str(precio), "priceCurrency": "MXN",
            "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MTK"},
            "eligibleQuantity": cantidad}


def oferta(m, url, envios=None):
    """Entrega A del SEO nacional (2026-11-16): un Offer con precio (el «desde» por m² del rollo completo, el mismo del
    feed de Merchant) en vez de un AggregateOffer; los tres precios por cantidad van como UnitPriceSpecification por m²
    (MTK) y el flete por zona en shippingDetails. Sin priceValidUntil: el negocio no publica vigencia de precios."""
    return {
        "@type": "Offer", "url": url, "priceCurrency": "MXN", "price": str(m["rollo"]),
        "priceSpecification": [_precio_m2(m["rollo"], ROLLO_M2), _precio_m2(m["t2"], 10, ROLLO_M2 - 1),
                               _precio_m2(m["t1"], MIN_SHOWROOM_M2, 9)],
        "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
        "seller": SELLER, "shippingDetails": envios or SHIPPING, "hasMerchantReturnPolicy": RETURNS,
    }


def strip_tags(html_text):
    return re.sub(r"<[^>]+>", "", html_text)
