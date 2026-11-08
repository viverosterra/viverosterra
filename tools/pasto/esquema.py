"""Nodos schema.org de la tienda de pasto sintético (Product, BreadcrumbList, envío, devoluciones y vendedor).

Datos, no HTML: los usan las plantillas de tools/site (fichas, hub, ciudades) y las páginas que aún genera
tools/pasto (/precios y zonas, vía common.py) hasta la Etapa 2g.
"""
import re

from data import SITE, WA_NUMBER

GAL = "/img/pasto-sintetico/galeria"


def breadcrumb_schema(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)
        ],
    }


SHIPPING = {
    "@type": "OfferShippingDetails",
    "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX"},
    "deliveryTime": {"@type": "ShippingDeliveryTime",
                     "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
}
RETURNS = {
    "@type": "MerchantReturnPolicy", "applicableCountry": "MX",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 7, "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
}
SELLER = {"@type": "Organization", "name": "Viveros Terra", "url": SITE, "telephone": f"+{WA_NUMBER}"}


def product_schema(m, *, with_id=True):
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
        "offers": {
            "@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(m["rollo"]), "highPrice": str(m["t1"]),
            "offerCount": "3", "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition", "seller": SELLER,
            "shippingDetails": SHIPPING, "hasMerchantReturnPolicy": RETURNS,
        },
    }
    if with_id:
        product["@id"] = f"{url}#producto"
    return product


def strip_tags(html_text):
    return re.sub(r"<[^>]+>", "", html_text)
