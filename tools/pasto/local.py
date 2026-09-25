"""Página local /pasto-sintetico-tampico: venta en showroom e instalación en Tampico, Madero y Altamira.

Sustituye a /venta-pasto-sintetico-tampico, que redirige aquí (vercel.json).
"""
import json

from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, faq_html, faq_schema,
                    footer, head, jsonld, section_open, wa)
from data import MODELOS, OBRAS, SITE, WA_NUMBER
from ficha import NOTE_FLETE, calc_html, quote_html, tiers_html

URL = f"{SITE}/pasto-sintetico-tampico"
BUSINESS_ID = f"{SITE}/#negocio"
ADDRESS = "Av. Álvaro Obregón 601, Cd. Madero, frente a Walmart"
MAPS = "https://maps.google.com/?q=Av+%C3%81lvaro+Obreg%C3%B3n+601+Ciudad+Madero+Tamaulipas"
INSTALADO_MIN, INSTALADO_MAX = 385, 650
MIN_RETAIL = min(m["rollo"] for m in MODELOS)
STOCK = [m for m in MODELOS if m["stock"]]
DEFAULT = next(m for m in MODELOS if m["slug"] == "toscana-28")

FAQS = [
    ("¿Dónde comprar pasto sintético en Tampico?",
     "En Viveros Terra, en Av. Álvaro Obregón 601, Cd. Madero, frente a Walmart. Tenemos Toscana 18 y Toscana 28 en "
     "existencia para llevar el mismo día, y los otros 7 modelos sobre pedido. Atendemos de lunes a viernes de 9 a 18 h "
     "y sábado de 9 a 14 h."),
    ("¿Cuánto cuesta instalar pasto sintético en Tampico?",
     f"La instalación cuesta desde ${INSTALADO_MIN}/m² y hasta ${INSTALADO_MAX}/m² en modelos premium. Incluye el "
     "material, la colocación, las uniones, las orillas y el cepillado. Si tu espacio necesita retiro de lo existente, "
     "nivelación o base drenante, lo revisamos en la visita y te lo cotizamos aparte antes de empezar."),
    ("¿Cuánto cuesta el pasto sintético por m² en Tampico?",
     f"Solo el material cuesta desde ${MIN_RETAIL}/m² en rollo completo. Toscana 18 va de $149/m² en rollo a $199/m² "
     "en cortes de 2 a 9 m². Toscana 28 va de $199/m² a $279/m². Los precios incluyen IVA."),
    ("¿Cuál es la compra mínima?",
     "En el showroom vendemos desde 2 m². El rollo mide 2 m de ancho, así que los cortes van de 2 en 2 m²."),
    ("¿Puedo recogerlo el mismo día?",
     "Sí, si es Toscana 18 o Toscana 28. Te recomendamos confirmar existencia por WhatsApp antes de pasar. Los demás "
     "modelos llegan en 3 a 5 días hábiles. Los pedimos en cuanto confirmas tu pedido con el pago."),
    ("¿Hacen envío dentro de Tampico, Madero y Altamira?",
     "Sí. El envío local cuesta desde $250 según el volumen y la zona. Te lo cotizamos por WhatsApp."),
    ("¿Qué pasto sintético conviene para el clima de Tampico?",
     "Uno con base perforada que drene rápido, porque de junio a septiembre llueve mucho. Para jardín familiar, "
     "Toscana 28. Para perros o mucho uso, Irlanda 25 o Capri 20. Para terrazas y balcones, Aruba 10 o Toscana 18."),
    ("¿Cuánto dura el pasto sintético?",
     "Bien instalado dura de 8 a 12 años en uso residencial. La garantía de fábrica va de 3 a 8 años según el modelo."),
    ("¿Cómo se paga y dan factura?",
     "Aceptamos efectivo, transferencia y tarjeta de débito o crédito. Emitimos factura CFDI 4.0 para persona física o moral."),
    ("¿Venden fuera de Tampico?",
     "Sí. Enviamos el material a todo México en 3 a 5 días hábiles. La instalación es solo en Tampico, Madero y Altamira."),
]

INSTALL_STEPS = [
    ("Visita y medición", "Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso."),
    ("Preparación del terreno", "Si hace falta, retiramos lo existente, nivelamos y ponemos grava fina para que drene. Se cotiza aparte según tu espacio."),
    ("Colocación", "Extendemos el rollo, cortamos al perímetro y unimos los tramos con cinta y adhesivo."),
    ("Orillas y acabados", "Fijamos las orillas para que no se levanten y cuidamos los bordes con andadores y jardineras."),
    ("Cepillado y entrega", "Cepillamos la fibra para que quede de pie, limpiamos y te entregamos el área lista."),
]


def faqs_with_html():
    out = []
    for q, a in FAQS:
        html = esc(a)
        if q.startswith("¿Venden fuera"):
            html += ' Ve la <a href="/pasto-sintetico">tienda con envío nacional</a>.'
        if q.startswith("¿Qué pasto"):
            html += ' Compara los modelos en la <a href="/pasto-sintetico#comparativa">tabla de la colección</a>.'
        out.append((q, a, html))
    return out


def hero_html():
    stock_names = " y ".join(m["nombre"] for m in STOCK)
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Tampico · Madero · Altamira</span><span class="stock">{esc(stock_names)} en existencia</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético en Tampico <em>venta e instalación</em></h1>
        <p class="pdp__lede">Llévate el material desde nuestro showroom en Cd. Madero o déjanos la instalación completa.</p>
        <p class="summary summary--hero">Viveros Terra vende e instala pasto sintético en Tampico, Ciudad Madero y Altamira desde 2006. El showroom está en {esc(ADDRESS)}. El material cuesta desde <strong>${MIN_RETAIL}/m²</strong> y la instalación desde <strong>${INSTALADO_MIN}/m²</strong>, con material y colocación incluidos.</p>
        <dl class="specstrip">
          <div><dt>Material, IVA incluido</dt><dd class="num"><small>desde</small> ${MIN_RETAIL}<small>/m²</small></dd></div>
          <div><dt>Instalado, con material</dt><dd class="num"><small>desde</small> ${INSTALADO_MIN}<small>/m²</small></dd></div>
          <div><dt>Compra mínima</dt><dd class="num">2<small>m²</small></dd></div>
          <div><dt>En la región</dt><dd class="num">20<small>años</small></dd></div>
        </dl>
      </div>
      <figure class="hub-hero__media">
        <picture>
          <source media="(min-width: 1024px)" srcset="{GAL}/obra-residencial-tampico-sm.webp 560w, {GAL}/obra-residencial-tampico.webp 960w" sizes="560px" width="960" height="1440">
          <img src="{GAL}/obra-proyecto-02-sm.webp" srcset="{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w" sizes="100vw" width="960" height="1280" alt="Residencia moderna con escalones de piedra y pasto sintético hasta el deck" fetchpriority="high" decoding="async">
        </picture>
        <figcaption>Obra de Viveros Terra con pasto sintético.</figcaption>
      </figure>
    </div>
  </section>"""


def options_html():
    buy = wa("Hola, quiero comprar pasto sintético en el showroom. ¿Tienen existencia?")
    install = wa("Hola, quiero cotizar la instalación de pasto sintético. ¿Pueden venir a medir?")
    return f"""<div class="options">
          <article class="option">
            <p class="option__label">Opción 1</p>
            <h3>Compras el material</h3>
            <p class="option__price num">desde <strong>${MIN_RETAIL}</strong>/m²</p>
            <ul class="fit">
              <li>Desde 2 m², cortado a tu medida</li>
              <li>Toscana 18 y 28 para llevar hoy</li>
              <li>Kit de pegamento, cinta y clavos</li>
              <li>Envío local desde $250</li>
            </ul>
            <a class="btn btn--ghost" href="{buy}" target="_blank" rel="noopener">Preguntar existencia</a>
          </article>
          <article class="option option--main">
            <p class="option__label">Opción 2</p>
            <h3>Nosotros lo instalamos</h3>
            <p class="option__price num">desde <strong>${INSTALADO_MIN}</strong>/m² <span>material y colocación</span></p>
            <ul class="fit">
              <li>Visita y cotización sin compromiso</li>
              <li>Colocación, uniones, orillas y cepillado</li>
              <li>Material con garantía de fábrica</li>
            </ul>
            <p class="option__note">Cada terreno es distinto. Si el tuyo necesita retiro, nivelación o base drenante, lo vemos en la visita y te lo cotizamos aparte, antes de empezar y sin sorpresas.</p>
            <a class="btn btn--primary" href="{install}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar instalación</a>
          </article>
        </div>"""


def price_table_html():
    rows = []
    for m in MODELOS:
        avail = '<span class="tag-stock">Para llevar hoy</span>' if m["stock"] else '<span class="tag-order">3 a 5 días</span>'
        rows.append(f"""            <tr><th scope="row"><a href="/pasto-sintetico/{m['slug']}">{esc(m['nombre'])}</a><span>{m['mm']} mm</span>{avail}</th><td>${m['t1']}</td><td>${m['t2']}</td><td><strong>${m['rollo']}</strong></td></tr>""")
    return f"""<p class="section__intro">Precio por m² del material, con IVA. Entre más metros, menor precio. Instalación con material y colocación de ${INSTALADO_MIN} a ${INSTALADO_MAX}/m² según el modelo.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Precios de pasto sintético en Tampico">
          <table class="compare-table compare-table--compact num">
            <thead><tr><th scope="col">Modelo</th><th scope="col">2 a 9 m²</th><th scope="col">10 a 49 m²</th><th scope="col">Rollo 50 m²</th></tr></thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
        <p class="spec-note">Si el modelo no está en el showroom, llega en 3 a 5 días hábiles. Lo enviamos en cuanto confirmas tu pedido con el pago. Precios vigentes en 2026.</p>"""


def install_html():
    items = "\n".join(f"          <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in INSTALL_STEPS)
    return f"""<p class="section__intro">Cotizamos después de ver el terreno, porque la base es lo que decide cuánto dura el pasto.</p>
        <ol class="steps steps--five">
{items}
        </ol>
        <blockquote class="quote-card">
          <p>“Instalamos pasto sintético en la terraza de nuestra cafetería. Ya no tenemos que regar nada y siempre está verde. Los clientes preguntan si es natural.”</p>
          <footer>Sofía R. · Cafetería en el centro de Tampico</footer>
        </blockquote>"""


def cotizador_html():
    options = "\n".join(
        f'                <option value="{m["slug"]}"{" selected" if m is DEFAULT else ""}>{esc(m["nombre"])} · desde ${m["rollo"]}/m²</option>'
        for m in MODELOS
    )
    select = f"""            <div class="field field--wide">
              <label for="modelo">Modelo</label>
              <select class="select" id="modelo">
{options}
              </select>
            </div>
"""
    calc = calc_html(select).replace('<option value="showroom">', '<option value="showroom" selected>')
    calc = calc.replace('value="50">', 'value="20">', 1)
    return f"""<div class="hub-quote">
          <section class="buy" id="comprar" aria-labelledby="precio-titulo">
            <h3 class="visually-hidden" id="precio-titulo">Calculadora de material</h3>
            <div class="buy__from">
              <span class="buy__from-label">Desde</span>
              <span class="buy__price num" id="buy-price">${DEFAULT['rollo']}</span>
              <span class="buy__unit">/m²</span>
            </div>
            <p class="buy__terms">Precio del material en rollo completo, IVA incluido. Para instalación, pide visita.</p>
{calc}
{tiers_html(DEFAULT)}
{quote_html(DEFAULT['t2'] * 20, DEFAULT['t2'])}
            <div class="actions">
              <a class="btn btn--primary" data-cta-wa href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Enviar por WhatsApp</a>
              <button class="btn btn--ghost" type="button" id="cta-add">Agregar a mi cotización</button>
              <p class="actions__note">{NOTE_FLETE}</p>
            </div>
          </section>
          <aside class="hub-quote__aside">
            <h3>Kit para instalarlo tú</h3>
            <ul class="fit">
              <li>Pegamento de contacto industrial, 4 L</li>
              <li>Cinta de unión profesional, 100 m</li>
              <li>Clavos de fijación de 2″, caja de 5 kg</li>
              <li>Guía de instalación paso a paso</li>
            </ul>
            <p class="spec-note">Un litro de pegamento rinde para unos 6 m de unión. Te ayudamos a calcular cuánto necesitas.</p>
            <h3 class="aside-gap">¿Instalas o construyes?</h3>
            <p class="spec-note">Instaladores y constructoras tienen precio por volumen, existencia prioritaria y crédito para clientes recurrentes. <a href="{wa('Hola, soy instalador o constructor y quiero precios por volumen de pasto sintético')}" target="_blank" rel="noopener">Pide precios por volumen</a>.</p>
          </aside>
        </div>"""


def obras_html():
    figs = []
    for name, w, h, alt, cap in OBRAS:
        figs.append(f"""          <figure class="obras__item">
            <img src="{GAL}/{name}-sm.webp" srcset="{GAL}/{name}-sm.webp 560w, {GAL}/{name}.webp 960w" sizes="(min-width: 1024px) 400px, 80vw" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">
            <figcaption>{esc(cap)}</figcaption>
          </figure>""")
    return '<div class="obras">\n' + "\n".join(figs) + "\n        </div>"


def showroom_html():
    return f"""<div class="showroom">
          <dl class="showroom__data">
            <div><dt>Dirección</dt><dd>{esc(ADDRESS)}, Tamaulipas</dd></div>
            <div><dt>Horario</dt><dd>Lunes a viernes de 9 a 18 h. Sábado de 9 a 14 h.</dd></div>
            <div><dt>Instalación</dt><dd>Tampico, Ciudad Madero y Altamira</dd></div>
            <div><dt>Envío del material</dt><dd>Local desde $250. Nacional en 3 a 5 días hábiles.</dd></div>
          </dl>
          <div class="showroom__actions">
            <a class="btn btn--primary" href="{MAPS}" target="_blank" rel="noopener">Cómo llegar</a>
            <a class="btn btn--ghost" href="tel:+528333268008">Llamar 833 326 8008</a>
          </div>
        </div>"""


def schema(faqs):
    service = {
        "@type": "Service", "@id": f"{URL}#instalacion", "name": "Instalación de pasto sintético en Tampico",
        "serviceType": "Instalación de pasto sintético", "provider": {"@id": BUSINESS_ID},
        "areaServed": [{"@type": "City", "name": c} for c in ("Tampico", "Ciudad Madero", "Altamira")],
        "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(INSTALADO_MIN),
                   "highPrice": str(INSTALADO_MAX), "unitText": "m²"},
    }
    business = {
        "@type": ["LocalBusiness", "Store"], "@id": BUSINESS_ID, "name": "Viveros Terra", "url": SITE,
        "telephone": f"+{WA_NUMBER}", "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": "Av. Álvaro Obregón 601, Col. Ampliación Unidad Nacional",
                    "addressLocality": "Ciudad Madero", "addressRegion": "Tamaulipas", "postalCode": "89510", "addressCountry": "MX"},
        "geo": {"@type": "GeoCoordinates", "latitude": 22.2722, "longitude": -97.8679},
        "hasMap": MAPS,
        "knowsAbout": ["Pasto sintético", "Instalación de pasto sintético", "Pasto en rollo", "Jardinería"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@id": f"{SITE}/pasto-sintetico/{m['slug']}#producto"}} for m in MODELOS]
                      + [{"@type": "Offer", "itemOffered": {"@id": f"{URL}#instalacion"}}],
    }
    return jsonld([
        breadcrumb_schema([("Inicio", SITE), ("Pasto sintético en Tampico", URL)]),
        business, service, faq_schema(faqs),
    ])


def build_local():
    faqs = faqs_with_html()
    models_json = json.dumps([
        {"slug": m["slug"], "nombre": m["nombre"], "img": f"{GAL}/{m['slug']}-2-sm.webp", "t1": m["t1"], "t2": m["t2"], "rollo": m["rollo"]}
        for m in MODELOS
    ], ensure_ascii=False)
    html = "".join([
        head(title="Pasto Sintético en Tampico: Venta e Instalación | Viveros Terra",
             description=f"Venta e instalación de pasto sintético en Tampico, Madero y Altamira. Showroom en Cd. Madero, material desde ${MIN_RETAIL}/m² e instalado desde ${INSTALADO_MIN}/m².",
             canonical=URL, og_image=f"{SITE}{GAL}/obra-residencial-tampico.webp", og_type="website",
             preload_img=f"{GAL}/obra-proyecto-02-sm.webp", preload_srcset=f"{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w",
             ld=schema(faqs), extra=f'<script type="application/json" id="vt-models">{models_json}</script>\n'),
        f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li aria-current="page">Pasto sintético en Tampico</li>
      </ol>
    </nav>
  </div>
  {hero_html()}

  {section_open(1, "Dos opciones", "opciones-titulo", "Compra el material <em>o te lo instalamos</em>", section_id="opciones")}
        {options_html()}{SECTION_CLOSE}
  {section_open(2, "Precios", "precios-titulo", "Precio del pasto sintético <em>en Tampico</em>", tint=True, section_id="precios")}
        {price_table_html()}{SECTION_CLOSE}
  {section_open(3, "Instalación", "instalacion-titulo", "Cómo instalamos <em>en Tampico y Madero</em>", section_id="instalacion")}
        {install_html()}{SECTION_CLOSE}
  {section_open(4, "Calculadora", "calcula-titulo", "Calcula tu material <em>y llévatelo</em>", tint=True, section_id="cotizador")}
        {cotizador_html()}{SECTION_CLOSE}
  {section_open(5, "Obras", "obras-titulo", "Pasto sintético instalado <em>en la región</em>", section_id="obras")}
        {obras_html()}{SECTION_CLOSE}
  {section_open(6, "Showroom", "showroom-titulo", "Visítanos <em>en Cd. Madero</em>", tint=True, section_id="showroom")}
        {showroom_html()}{SECTION_CLOSE}
  {section_open(7, "Preguntas", "faq-titulo", "Preguntas frecuentes <em>en Tampico</em>", section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="nacional">
    <div class="wrap">
      <h2 id="nacional">¿No estás en Tampico? <em>Enviamos a todo México</em></h2>
      <p>Los mismos 9 modelos llegan a cualquier estado en 3 a 5 días hábiles, con factura.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="/pasto-sintetico">Ver la tienda nacional</a>
        <a class="btn btn--ghost" href="{wa('Hola, quiero cotizar pasto sintético en Tampico')}" target="_blank" rel="noopener">Cotizar en Tampico</a>
      </div>
    </div>
  </section>
</main>
""",
        footer(),
        buybar("Pasto sintético en Tampico", f"Instalado desde ${INSTALADO_MIN}/m²"),
        drawer_and_toast(),
    ])
    return html.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                        '<a class="skip-link" href="#opciones">Ir a precios y opciones</a>')
