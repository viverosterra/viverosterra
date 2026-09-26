"""Piezas compartidas por el hub y las fichas de la tienda de pasto sintético."""
import json
from html import escape
from urllib.parse import quote

from data import ASSET_VERSION, PHONE_DISPLAY, SITE, UPDATED, WA_NUMBER

GAL = "/img/pasto-sintetico/galeria"


def esc(text):
    return escape(str(text), quote=True)


def money(n):
    return "${:,.0f}".format(n)


def wa(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def jsonld(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(*, title, description, canonical, og_image, og_type, preload_img, preload_srcset, ld, extra=""):
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#F5F3EC">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Viveros Terra">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="es_MX">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{preload_img}" imagesrcset="{preload_srcset}" imagesizes="(min-width: 1024px) 620px, 100vw" fetchpriority="high">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/tienda-pasto.css?v={ASSET_VERSION}">
<script type="application/ld+json">{ld}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
{extra}<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>
</head>
<body>
{SYMBOLS}
<a class="skip-link" href="#comprar">Ir al cotizador</a>
{HEADER}"""


SYMBOLS = """<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <symbol id="i-wa" viewBox="0 0 24 24" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41z"/></symbol>
  <symbol id="i-list" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M1 4h14v12H1zM15 9h4l4 4v3h-8"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></symbol>
  <symbol id="i-store" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l1.5-5h15L21 9M3 9h18v11H3zM9 20v-6h6v6"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
</svg>"""

HEADER = """<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="/" aria-label="Viveros Terra, inicio"><img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="140" height="36"></a>
    <nav class="site-nav" aria-label="Tienda de pasto sintético">
      <a href="/pasto-sintetico#modelos">Los 9 modelos</a>
      <a href="/pasto-sintetico#elegir">¿Cuál me conviene?</a>
      <a href="/pasto-sintetico#como-funciona">Cómo comprar</a>
      <a href="/pasto-sintetico-tampico">Tampico</a>
      <a href="/">Viveros Terra</a>
    </nav>
    <button class="quote-btn" type="button" data-open-cot aria-haspopup="dialog">
      <svg class="icon" aria-hidden="true"><use href="#i-list"/></svg>
      <span>Cotización</span>
      <span class="quote-btn__count num" data-cot-count data-empty="true">0</span>
    </button>
  </div>
</header>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="130" height="34" loading="lazy">
        <p>Pasto sintético con envío a todo México. Vivero, showroom y servicios de jardinería desde 2007.</p>
        <p><a href="https://maps.app.goo.gl/xC4XGL2WeucAjGwAA" target="_blank" rel="noopener">Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, 89510 Cd. Madero, Tamps.</a><br><a href="https://maps.app.goo.gl/xC4XGL2WeucAjGwAA" target="_blank" rel="noopener">Google Maps</a> · <a href="https://maps.apple.com/?daddr=22.2777575,-97.8433341&amp;q=Viveros%20Terra" target="_blank" rel="noopener">Apple Maps</a></p>
      </div>
      <div>
        <h3>Tienda</h3>
        <ul>
          <li><a href="/pasto-sintetico">Los 9 modelos</a></li>
          <li><a href="/blog/cuanto-cuesta-pasto-sintetico-mexico">Cuánto cuesta</a></li>
          <li><a href="/blog/que-altura-de-pasto-sintetico-elegir">Qué altura elegir</a></li>
          <li><a href="/blog/como-instalar-pasto-sintetico">Cómo instalarlo</a></li>
          <li><a href="/politicas">Envíos y devoluciones</a></li>
        </ul>
      </div>
      <div>
        <h3>Viveros Terra</h3>
        <ul>
          <li><a href="/pasto-sintetico-tampico">Pasto sintético en Tampico</a></li>
          <li><a href="/pasto-en-rollo-tampico">Pasto natural en rollo</a></li>
          <li><a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a></li>
          <li><a href="/diseno-jardines-tampico">Diseño de jardines</a></li>
          <li><a href="{wa('Hola, tengo una pregunta sobre pasto sintético')}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li>Lun a vie 9 a 18 h · Sáb 9 a 14 h</li>
        </ul>
      </div>
    </div>
    <p class="site-footer__legal">© 2026 Viveros Terra · Tampico, Tamaulipas, México · Actualizado {UPDATED}</p>
  </div>
</footer>
"""


def buybar(name, price_text):
    return f"""<div class="buybar" id="buybar" data-visible="false">
  <div class="buybar__info">
    <div class="buybar__name">{esc(name)}</div>
    <div class="buybar__price num">{esc(price_text)}</div>
  </div>
  <a class="btn btn--primary" data-cta-wa href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar</a>
</div>
"""


ESTADO_OPTIONS = """<option value="">Selecciona tu estado</option>
                <option value="showroom">Recoger en showroom, Cd. Madero</option>"""


def drawer_and_toast():
    return f"""<dialog class="drawer" id="cotizacion" aria-labelledby="cot-titulo">
  <div class="drawer__inner">
    <div class="drawer__head">
      <h2 id="cot-titulo">Tu cotización</h2>
      <button class="drawer__close" type="button" id="cot-close" aria-label="Cerrar">×</button>
    </div>
    <div class="drawer__body" id="cot-list"></div>
    <div class="drawer__foot" id="cot-foot" hidden>
      <div class="field">
        <label for="cot-estado">Entrega</label>
        <select class="select" id="cot-estado">
          {ESTADO_OPTIONS}
        </select>
      </div>
      <div class="drawer__total num"><span id="cot-total-label">Total estimado del material</span><strong id="cot-total">$0</strong></div>
      <a class="btn btn--primary" id="cot-send" href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Enviar cotización por WhatsApp</a>
      <small>Precio estimado. Confirmamos el flete exacto con tu dirección.</small>
    </div>
  </div>
</dialog>

<div class="toast" id="toast" role="status" data-visible="false">
  <span data-toast-text></span>
  <button type="button" data-open-cot>Ver</button>
</div>
</body>
</html>
"""


def assurances(garantia_text):
    return f"""<ul class="assurances">
          <li><svg class="icon" aria-hidden="true"><use href="#i-truck"/></svg><span><strong>3 a 5 días hábiles</strong>A todo México con guía de rastreo</span></li>
          <li><svg class="icon" aria-hidden="true"><use href="#i-doc"/></svg><span><strong>Factura CFDI 4.0</strong>Para persona física o moral</span></li>
          <li><svg class="icon" aria-hidden="true"><use href="#i-shield"/></svg><span><strong>{esc(garantia_text)}</strong>La gestionamos nosotros</span></li>
          <li><svg class="icon" aria-hidden="true"><use href="#i-store"/></svg><span><strong>Showroom real</strong>Desde 2007 en Tampico y Madero</span></li>
        </ul>"""


def section_open(num, label, heading_id, heading_html, *, tint=False, section_id=None):
    sid = f' id="{section_id}"' if section_id else ""
    cls = "section section--tint" if tint else "section"
    return f"""<section class="{cls}"{sid} aria-labelledby="{heading_id}">
    <div class="wrap section__grid">
      <p class="section__label"><b>{num:02d}</b>{esc(label)}</p>
      <div>
        <h2 id="{heading_id}">{heading_html}</h2>"""


SECTION_CLOSE = """
      </div>
    </div>
  </section>
"""


def steps_list():
    return """<ol class="steps">
          <li><h3>Cotiza aquí</h3><p>Pon tus m² y tu estado. Mándanos la cotización por WhatsApp.</p></li>
          <li><h3>Confirmamos el flete</h3><p>Con tu dirección te damos el precio final. Sin sorpresas.</p></li>
          <li><h3>Pagas y facturamos</h3><p>Transferencia o link de pago con tarjeta. Factura CFDI 4.0.</p></li>
          <li><h3>Recibes en 3 a 5 días</h3><p>Llega por paquetería con guía de rastreo y guía de instalación.</p></li>
        </ol>"""


def faq_html(faqs):
    items = "\n".join(
        f"          <details><summary>{esc(q)}</summary><p>{a_html}</p></details>" for q, _plain, a_html in faqs
    )
    return f'<div class="faq">\n{items}\n        </div>'


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain}}
            for q, plain, _html in faqs
        ],
    }


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
    import re
    return re.sub(r"<[^>]+>", "", html_text)
