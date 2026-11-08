"""Piezas del HTML viejo que todavía usan /precios y las 6 zonas (tools/pasto/precios.py y zonas.py).

La tienda (hub, fichas, ciudades, perros y sintético en Tampico) sale de tools/site desde la Etapa 2b;
este módulo se borra en la Etapa 2g, cuando /precios y las zonas pasen a sus plantillas.
"""
import json
from html import escape
from urllib.parse import quote

from data import ASSET_VERSION, ESTADOS_ORDEN, SITE, WA_NUMBER

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
    """<head> y apertura de <body> con las regiones vacías del shell."""
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{preload_img}" imagesrcset="{preload_srcset}" imagesizes="(min-width: 1024px) 620px, 100vw" fetchpriority="high">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/tienda-pasto.css?v={ASSET_VERSION}">
<script type="application/ld+json">{ld}</script>
{extra}<script src="/js/vt-mensualidades.js?v={ASSET_VERSION}" defer></script>
<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>
<!-- vt:head -->
<!-- /vt:head -->
</head>
<body>
{SYMBOLS}
<!-- vt:header -->
<!-- /vt:header -->
"""


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

def footer():
    """Región vacía del pie: tools/site/shell.py la llena con el pie único y la barra móvil."""
    return "<!-- vt:footer -->\n<!-- /vt:footer -->\n"


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


from esquema import RETURNS, SELLER, SHIPPING, breadcrumb_schema, product_schema, strip_tags  # noqa: E402,F401
