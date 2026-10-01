"""Página /pasto-sintetico/envio/<slug>: pasto sintético con envío a una ciudad."""
from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, faq_html, faq_schema,
                    footer, head, height_rule_html, jsonld, section_open, trust_band_html, wa)
from data import MODELOS, SITE, ZONA_ESTADOS, ZONAS, estado_slug, landed_m2, zona_de

MIN_NACIONAL = 25
ROLLO = 50


def modelo(slug):
    return next(m for m in MODELOS if m["slug"] == slug)


def totales(m, zona):
    """Material + flete para 25, 50 y 100 m² (mismas reglas del cotizador: 25 m² usa precio t2)."""
    out = []
    for m2 in (MIN_NACIONAL, ROLLO, ROLLO * 2):
        precio = m["rollo"] if m2 >= ROLLO else m["t2"]
        rollos = -(-m2 // ROLLO)
        out.append((m2, m2 * precio + rollos * ZONAS[zona]))
    return out


def barato():
    return min(MODELOS, key=lambda m: m["rollo"])


def hero_html(c, zona):
    desde = landed_m2(barato(), zona)
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Envío a {esc(c["nombre_largo"])}</span><span class="stock">9 modelos en existencia</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético en {esc(c["nombre"])} <em>con envío a tu casa</em></h1>
        <p class="summary summary--hero">Te enviamos el pasto sintético a {esc(c["nombre_largo"])} en 3 a 5 días hábiles. Desde <strong>${desde}/m²</strong> ya con envío, en rollo de 50 m² con factura. Tú lo instalas con nuestra guía.</p>
        <dl class="specstrip">
          <div><dt>Puesto en {esc(c["nombre"])}</dt><dd class="num"><small>desde</small> ${desde}<small>/m²</small></dd></div>
          <div><dt>Flete por rollo</dt><dd class="num">${ZONAS[zona]:,}</dd></div>
          <div><dt>Entrega</dt><dd class="num">3–5<small>días</small></dd></div>
          <div><dt>Compra mínima</dt><dd class="num">25<small>m²</small></dd></div>
        </dl>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="/pasto-sintetico?estado={estado_slug(c["estado"])}#modelos">Ver los 9 modelos con precio puesto</a>
          <a class="btn btn--ghost" href="{wa(f"Hola, quiero cotizar pasto sintético con envío a {c['nombre']}. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="{GAL}/obra-proyecto-02-sm.webp" srcset="{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w" sizes="(min-width: 1024px) 560px, 100vw" width="960" height="1280" alt="Jardín residencial con pasto sintético de nuestra colección" fetchpriority="high" decoding="async">
        <figcaption>Pasto sintético de nuestra colección instalado.</figcaption>
      </figure>
    </div>
  </section>"""


def totales_html(zona):
    m = barato()
    rows = "\n".join(
        f'            <tr><th scope="row">{m2} m²</th><td>${total:,}</td><td>${round(total / m2)}/m²</td></tr>'
        for m2, total in totales(m, zona)
    )
    return f"""<p class="section__intro">Ejemplo con {esc(m["nombre"])}, el modelo más económico. Material más flete, IVA incluido.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Totales de ejemplo con envío">
          <table class="compare-table compare-table--compact num">
            <thead><tr><th scope="col">Metros</th><th scope="col">Total con envío</th><th scope="col">Por m²</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="spec-note">El flete exacto se confirma con tu código postal antes de pagar.</p>"""


def modelos_html(c, zona):
    cards = []
    for slug, razon in c["modelos"]:
        m = modelo(slug)
        cards.append(f"""          <article class="city-model">
            {height_rule_html(m["mm"])}
            <div>
              <h3><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a> <span class="num">{m["mm"]} mm</span></h3>
              <p>{esc(razon)}</p>
              <p class="city-model__price num">Desde <strong>${landed_m2(m, zona)}</strong>/m² puesto en {esc(c["nombre"])}</p>
            </div>
          </article>""")
    return f"""<p class="section__intro">{esc(c["clima"])}</p>
        <div class="city-models">
{chr(10).join(cards)}
        </div>"""


def llegada_html():
    return """<ol class="steps">
          <li><h3>Confirmas y pagas</h3><p>Transferencia o link de pago con tarjeta. Factura CFDI 4.0.</p></li>
          <li><h3>Sale en rollo</h3><p>Rollo de 2 m de ancho, enrollado y protegido, con guía de rastreo.</p></li>
          <li><h3>Revisa al recibir</h3><p>Que el empaque venga completo y que los metros coincidan con tu pedido. Si algo no está bien, avísanos por WhatsApp con fotos.</p></li>
        </ol>"""


def diy_html():
    return """<p class="section__intro">Un patio de 25 a 50 m² se instala en un día con dos personas. Te mandamos la guía con el pedido.</p>
        <p class="spec-note">La instalación profesional es solo en Tampico, Ciudad Madero y Altamira. <a href="/blog/como-instalar-pasto-sintetico">Ver la guía de instalación paso a paso</a>.</p>"""


def schema(c, zona, url, faqs):
    m = barato()
    offer = {
        "@type": "Offer", "name": f"Pasto sintético con envío a {c['nombre_largo']}", "priceCurrency": "MXN",
        "price": str(m["rollo"]), "availability": "https://schema.org/InStock", "url": url,
        "shippingDetails": {
            "@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": str(ZONAS[zona]), "currency": "MXN"},
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX", "addressRegion": c["estado"]},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                             "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
        },
    }
    return jsonld([
        breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), (f"Envío a {c['nombre']}", url)]),
        offer, faq_schema(faqs),
    ])


def build_ciudad(c):
    zona = zona_de(c["estado"])
    url = f"{SITE}/pasto-sintetico/envio/{c['slug']}"
    faqs = [(q, a, esc(a)) for q, a in c["faqs"]]
    desde = landed_m2(barato(), zona)
    base = head(
        title=f"Pasto sintético en {c['nombre']} con envío · desde ${desde}/m² | Viveros Terra",
        description=f"Pasto sintético con envío a {c['nombre_largo']} desde ${desde}/m² puesto en tu casa. 9 modelos de 10 a 35 mm, entrega en 3 a 5 días hábiles y factura.",
        canonical=url, og_image=f"{SITE}{GAL}/obra-proyecto-02.webp", og_type="website",
        preload_img=f"{GAL}/obra-proyecto-02-sm.webp", preload_srcset=f"{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w",
        ld=schema(c, zona, url, faqs),
    )
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#modelos">Ir a los modelos</a>'), f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li><a href="/pasto-sintetico">Pasto sintético</a></li>
        <li aria-current="page">Envío a {esc(c["nombre"])}</li>
      </ol>
    </nav>
  </div>
  {hero_html(c, zona)}
  {trust_band_html()}

  {section_open(1, "Precios", "totales-titulo", f"Cuánto cuesta con envío <em>a {esc(c['nombre'])}</em>", section_id="precios")}
        {totales_html(zona)}{SECTION_CLOSE}
  {section_open(2, "Clima", "modelos-titulo", f"El pasto que conviene <em>en {esc(c['nombre'])}</em>", tint=True, section_id="modelos")}
        {modelos_html(c, zona)}{SECTION_CLOSE}
  {section_open(3, "Envío", "llegada-titulo", "Cómo te llega <em>el pedido</em>", section_id="envio")}
        {llegada_html()}{SECTION_CLOSE}
  {section_open(4, "Instálalo tú", "diy-titulo", "Instalarlo tú mismo <em>es sencillo</em>", tint=True, section_id="instalacion")}
        {diy_html()}{SECTION_CLOSE}
  {section_open(5, "Preguntas", "faq-titulo", f"Preguntas frecuentes <em>en {esc(c['nombre'])}</em>", section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="cierre">
    <div class="wrap">
      <h2 id="cierre">Cotiza tu pedido <em>a {esc(c["nombre"])}</em></h2>
      <p>Elige modelo y metros en la tienda: el precio ya incluye el envío a {esc(c["nombre_largo"])}. Te respondemos por WhatsApp en menos de 1 hora en horario.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="/pasto-sintetico?estado={estado_slug(c["estado"])}#cotizador">Calcular mi pedido</a>
        <a class="btn btn--ghost" href="{wa(f"Hola, quiero cotizar pasto sintético con envío a {c['nombre']}. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
      </div>
    </div>
  </section>
</main>
""", footer(), buybar(f"Envío a {c['nombre']}", f"Desde ${desde}/m² puesto"), drawer_and_toast()])
