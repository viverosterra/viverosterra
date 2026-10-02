"""Catálogo de productos para Google Merchant Center (/feed-pasto-sintetico.xml).

Se genera desde data.py para que precios, enlaces y existencias coincidan con la tienda.
Precio por m² con unidad de medida; el envío se declara con la tarifa más alta por rollo
para no mostrar menos de lo que paga el cliente en ningún estado.
"""
from xml.sax.saxutils import escape

from common import GAL, strip_tags
from data import MODELOS, SITE, ZONAS

SHIPPING_MAX = max(ZONAS.values())


def item_xml(m):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    extra_imgs = "\n".join(
        f"    <g:additional_image_link>{SITE}{GAL}/{m['slug']}-{idx}.webp</g:additional_image_link>"
        for idx, _kind, _cap in m["gallery"][:4]
    )
    gar = f", garantía de {m['garantia']} años" if m["garantia"] else ""
    desc = (f"{strip_tags(m['resumen'])} Precio por m² en rollo de 2 m de ancho; compra mínima nacional de 25 m². "
            f"El envío se cobra por rollo según el estado. Factura CFDI 4.0.")
    return f"""  <item>
    <g:id>VT-PST-{m['id'].upper()}</g:id>
    <g:title>{escape(f"Pasto sintético {m['nombre']} de {m['mm']} mm, precio por m²")}</g:title>
    <g:description>{escape(desc)}</g:description>
    <g:link>{url}</g:link>
    <g:image_link>{SITE}/img/pasto-sintetico/{m['slug']}.jpg</g:image_link>
{extra_imgs}
    <g:availability>in_stock</g:availability>
    <g:price>{m['rollo']:.2f} MXN</g:price>
    <g:unit_pricing_measure>1 sqm</g:unit_pricing_measure>
    <g:unit_pricing_base_measure>1 sqm</g:unit_pricing_base_measure>
    <g:brand>Viveros Terra</g:brand>
    <g:condition>new</g:condition>
    <g:identifier_exists>no</g:identifier_exists>
    <g:color>{escape(m['color'])}</g:color>
    <g:product_type>Pasto sintético &gt; {escape(m['nombre'])}</g:product_type>
    <g:google_product_category>Home &amp; Garden &gt; Lawn &amp; Garden &gt; Gardening</g:google_product_category>
    <g:shipping>
      <g:country>MX</g:country>
      <g:service>Paquetería 3 a 5 días hábiles</g:service>
      <g:price>{SHIPPING_MAX:.2f} MXN</g:price>
    </g:shipping>
    <g:min_handling_time>1</g:min_handling_time>
    <g:max_handling_time>2</g:max_handling_time>
  </item>"""


def build_feed():
    items = "\n".join(item_xml(m) for m in MODELOS)
    low = min(m["rollo"] for m in MODELOS)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
<channel>
  <title>Viveros Terra · Pasto sintético</title>
  <link>{SITE}/pasto-sintetico</link>
  <description>Pasto sintético residencial con envío a todo México. 9 modelos desde ${low}/m², factura CFDI 4.0.</description>
{items}
</channel>
</rss>
"""
