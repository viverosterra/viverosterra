"""Plantilla del hub /pasto-sintetico: catálogo de la tienda."""
import json

from ciudades import CIUDADES
from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, estado_select_html, faq_html,
                    faq_schema, footer, head, height_rule_html, jsonld, product_schema, section_open, steps_list,
                    strip_tags, trust_band_html)
from data import ASSET_VERSION, ZONA_ESTADOS, ZONAS, MODELOS, OBRAS, SITE, USO_FILTERS, WA_NUMBER, landed_m2, zona_de
from ficha import NOTE_FLETE, calc_html, quote_html, tiers_html

DEFAULT = next(m for m in MODELOS if m["slug"] == "toscana-28")

HUB_FAQS = [
    ("¿Cuánto cuesta el pasto sintético con envío?",
     "El material cuesta de $139 a $299/m² en rollo, según el modelo. El envío se suma por rollo según tu estado: "
     "$900 en Centro y Occidente, $1,150 en Norte, Golfo y Sur, y $1,400 en Sureste y fronteras. El cotizador de "
     "esta página calcula tu total estimado."),
    ("¿Cuál es la compra mínima?",
     "Para envío nacional el mínimo es 25 m², medio rollo. En el showroom de Cd. Madero puedes comprar desde 2 m² "
     "sin flete."),
    ("¿Cuánto tarda el envío?",
     "De 3 a 5 días hábiles después de confirmar tu pago, según el destino. Te compartimos la guía de rastreo."),
    ("¿Cómo pago?",
     "Por transferencia bancaria o con link de pago con tarjeta de débito o crédito. El pedido se embarca al "
     "confirmar el pago."),
    ("¿Dan factura?", "Sí. Emitimos factura CFDI 4.0 para persona física o moral en todos los pedidos."),
    ("¿Qué modelo me conviene?",
     "Toscana 28 es el más vendido para jardines familiares. Para poco uso o presupuesto ajustado, Toscana 18. Para "
     "perros y pisoteo diario, Irlanda 25 o Capri 20. Para el look más natural, los de 35 mm: Japonés, Mónaco y Bali."),
    ("¿Puedo instalarlo yo mismo?",
     "Sí. Un jardín de 25 a 50 m² se instala en un día. Te mandamos la guía de instalación con el pedido. En Tampico, "
     "Madero y Altamira también ofrecemos instalación profesional."),
    ("¿Qué incluye un rollo?",
     "Un rollo mide 2 m de ancho por 25 m de largo: 50 m². Puedes pedir desde 25 m² y te enviamos el corte."),
    ("¿Hacen instalación fuera de Tampico?",
     "A nivel nacional enviamos solo el material, con guía de instalación. La instalación profesional es solo en "
     "Tampico, Ciudad Madero y Altamira."),
]

DIY_STEPS = [
    ("Nivela y compacta", "Retira el pasto viejo, empareja el terreno y compáctalo."),
    ("Base drenante", "Extiende y compacta grava fina o polvo de piedra para que drene."),
    ("Extiende y clava", "Coloca el rollo, déjalo reposar, corta a medida y fija el perímetro."),
    ("Une los tramos", "Junta los rollos con cinta de unión y adhesivo, con la fibra en la misma dirección."),
    ("Cepilla", "Cepilla a contrapelo para levantar la fibra y darle aspecto natural."),
]


def faqs_with_html():
    out = []
    for q, a in HUB_FAQS:
        html = esc(a)
        if q.startswith("¿Puedo instalarlo"):
            html += ' Aquí está la <a href="/blog/como-instalar-pasto-sintetico">guía paso a paso</a>.'
        if q.startswith("¿Cuánto cuesta"):
            html += ' Más detalle en la <a href="/blog/cuanto-cuesta-pasto-sintetico-mexico">guía de precios</a>.'
        out.append((q, a, html))
    return out


def hero_html():
    barato = min(MODELOS, key=lambda m: m["rollo"])
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Tienda · Envío a todo México</span><span class="stock">9 modelos en existencia</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético con envío a todo México <em>precio puesto en tu puerta</em></h1>
        {estado_select_html("hero-estado")}
        <p class="landed" data-landed-hero data-rollo="{barato['rollo']}" aria-live="polite">
          <span class="landed__from">Desde</span>
          <strong class="landed__price num" data-landed-value>${barato['rollo']}</strong><span class="landed__unit">/m²</span>
          <span class="landed__note" data-landed-note>+ envío desde $900 por rollo. Elige tu estado para ver el precio puesto.</span>
        </p>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="#modelos">Ver modelos con este precio</a>
          <a class="btn btn--ghost" href="#cotizador">Calcular mi pedido</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <picture>
          <source media="(min-width: 1024px)" srcset="{GAL}/obra-residencial-tampico-sm.webp 560w, {GAL}/obra-residencial-tampico.webp 960w" sizes="560px" width="960" height="1440">
          <img src="{GAL}/obra-proyecto-03-sm.webp" srcset="{GAL}/obra-proyecto-03-sm.webp 560w, {GAL}/obra-proyecto-03.webp 960w" sizes="100vw" width="960" height="1280" alt="Residencia con palmas y jardín de pasto sintético instalado" fetchpriority="high" decoding="async">
        </picture>
        <figcaption>Proyecto real con pasto sintético de nuestra colección.</figcaption>
      </figure>
    </div>
  </section>"""


def card_html(m):
    gar = f"{str(m['garantia']).replace(' a ', '–')} años" if m["garantia"] else "Consultar"
    url = f"/pasto-sintetico/{m['slug']}"
    return f"""          <article class="spec-card" data-usos="{' '.join(m['usos'])}" id="m-{m['slug']}">
            <a class="spec-card__media" href="{url}" tabindex="-1" aria-hidden="true">
              <img src="{GAL}/{m['slug']}-2-sm.webp" width="420" height="560" alt="" loading="lazy" decoding="async">
              <span class="spec-card__n num">{m['n']:02d}</span>
            </a>
            <div class="spec-card__body">
              <p class="spec-card__tag">{esc(m['tag'])}</p>
              <h3 class="spec-card__name"><a href="{url}">{esc(m['nombre'])}</a></h3>
              {height_rule_html(m['mm'])}
              <dl class="spec-card__specs num"><div><dt>Altura</dt><dd>{m['mm']} mm</dd></div><div><dt>Peso</dt><dd>{m['peso']} g/m²</dd></div><div><dt>Garantía</dt><dd>{gar}</dd></div></dl>
              <div class="spec-card__foot">
                <p class="spec-card__price num">Desde <strong>${m['rollo']}</strong>/m² <span class="spec-card__landed" data-landed-slug="{m['slug']}"></span></p>
                <button class="spec-card__add" type="button" data-add="{m['slug']}" aria-label="Agregar {esc(m['nombre'])} a mi cotización"><svg class="icon" aria-hidden="true"><use href="#i-plus"/></svg><span>Agregar</span></button>
              </div>
            </div>
          </article>"""


def catalog_html():
    chips = "\n".join(
        f'          <button class="chip" type="button" data-filter="{key}" aria-pressed="{"true" if key == "todos" else "false"}">{esc(label)}</button>'
        for key, label in USO_FILTERS
    )
    cards = "\n".join(card_html(m) for m in MODELOS)
    return f"""<p class="section__intro">Ordenados por altura. A más altura y peso, más volumen y realismo. Todos se venden por rollo de 2 × 25 m con envío a todo México.</p>
        <div class="filters" role="group" aria-label="Filtrar por uso">
{chips}
        </div>
        <p class="filters__count" id="filters-count" aria-live="polite">9 modelos</p>
        <div class="catalog">
{cards}
        </div>"""


def quiz_html():
    def group(name, legend, options):
        opts = "\n".join(
            f'            <label class="quiz__opt"><input type="radio" name="{name}" value="{v}"{" checked" if i == 0 else ""}><span>{esc(t)}</span></label>'
            for i, (v, t) in enumerate(options)
        )
        return f'          <fieldset class="quiz__group"><legend>{esc(legend)}</legend>\n{opts}\n          </fieldset>'
    return f"""<form class="quiz" id="quiz" aria-describedby="quiz-help">
          <p class="section__intro" id="quiz-help">Tres preguntas y te recomendamos dos modelos. Cambia las respuestas y la recomendación se actualiza.</p>
{group("donde", "¿Dónde va?", [("jardin", "Jardín"), ("terraza", "Terraza o balcón"), ("patio", "Patio o alberca")])}
{group("uso", "¿Quién lo pisa?", [("familia", "La familia, a diario"), ("perros", "Perros"), ("poco", "Casi nadie, es decorativo"), ("intenso", "Mucha gente, uso intenso")])}
{group("prioridad", "¿Qué te importa más?", [("equilibrio", "Equilibrio"), ("precio", "El mejor precio"), ("realismo", "Que se vea lo más natural")])}
          <div class="quiz__result" id="quiz-result" aria-live="polite"></div>
        </form>"""


def compare_table_html():
    rows = []
    for m in MODELOS:
        gar = f"{str(m['garantia']).replace(' a ', '–')} años" if m["garantia"] else "Consultar"
        rows.append(f"""            <tr><th scope="row"><a href="/pasto-sintetico/{m['slug']}">{esc(m['nombre'])}</a><span>{esc(m['tag'])}</span></th><td>{m['mm']} mm</td><td>{m['peso']}</td><td>{gar}</td><td><strong>${m['rollo']}</strong></td><td>{esc(m['ideal'])}</td></tr>""")
    return f"""<div class="table-scroll" tabindex="0" role="region" aria-label="Comparativa de los 9 modelos">
          <table class="compare-table num">
            <thead><tr><th scope="col">Modelo</th><th scope="col">Altura</th><th scope="col">Peso g/m²</th><th scope="col">Garantía</th><th scope="col">Rollo /m²</th><th scope="col">Ideal para</th></tr></thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
        <p class="spec-note">Rollos de 2 m de ancho, 50 m² por rollo. Precios por rollo completo con IVA incluido. El envío se suma según tu estado.</p>"""


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
    return f"""<div class="hub-quote">
          <section class="buy" id="comprar" aria-labelledby="precio-titulo">
            <h3 class="visually-hidden" id="precio-titulo">Cotizador</h3>
            <div class="buy__from">
              <span class="buy__from-label">Desde</span>
              <span class="buy__price num" id="buy-price">${DEFAULT['rollo']}</span>
              <span class="buy__unit">/m²</span>
            </div>
            <p class="buy__terms">Precio por rollo completo de 50 m², IVA incluido. El envío se suma según tu estado.</p>
{calc_html(select)}
{tiers_html(DEFAULT)}
{quote_html(DEFAULT['rollo'] * 50, DEFAULT['rollo'])}
            <div class="actions">
              <a class="btn btn--primary" data-cta-wa href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar por WhatsApp</a>
              <button class="btn btn--ghost" type="button" id="cta-add">Agregar a mi cotización</button>
              <p class="actions__note">{NOTE_FLETE}</p>
            </div>
          </section>
          <aside class="hub-quote__aside">
            <h3>Cómo se calcula</h3>
            <ul class="fit">
              <li>Material: m² por el precio del volumen que pidas</li>
              <li>Envío por rollo: $900, $1,150 o $1,400 según tu estado</li>
              <li>Con 50 m² o más pagas precio de rollo completo</li>
              <li>El flete exacto se confirma con tu dirección</li>
            </ul>
          </aside>
        </div>
{envio_table_html()}"""


def envio_table_html():
    rows = "\n".join(
        f"""            <tr><th scope="row">Zona {z}<span>{esc(nombre)}</span></th><td>{esc(", ".join(estados))}</td><td><strong>${ZONAS[z]:,}</strong></td><td>${ZONAS[z] * 2:,}</td></tr>"""
        for z, (nombre, estados) in ZONA_ESTADOS.items()
    )
    return f"""        <h3 class="aside-gap" id="envio">Costo de envío por estado</h3>
        <p class="section__intro">El envío se cobra por rollo de 50 m². Un pedido de 25 a 50 m² viaja en 1 rollo; de 51 a 100 m², en 2. En Tampico, Madero y Altamira puedes recoger en el showroom sin flete.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Costo de envío de pasto sintético por estado">
          <table class="compare-table compare-table--compact compare-table--envio num">
            <thead><tr><th scope="col">Zona</th><th scope="col">Estados</th><th scope="col">1 rollo</th><th scope="col">2 rollos</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="spec-note">Precios de flete con IVA. Te confirmamos el costo exacto con tu código postal antes de pagar.</p>"""


def obras_html():
    figs = []
    for i, (name, w, h, alt, cap) in enumerate(OBRAS):
        figs.append(f"""          <figure class="obras__item">
            <img src="{GAL}/{name}-sm.webp" srcset="{GAL}/{name}-sm.webp 560w, {GAL}/{name}.webp 960w" sizes="(min-width: 1024px) 400px, 80vw" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">
            <figcaption>{esc(cap)}</figcaption>
          </figure>""")
    return f"""<div class="obras">
{chr(10).join(figs)}
        </div>"""


def diy_html():
    items = "\n".join(f"          <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in DIY_STEPS)
    return f"""<p class="section__intro">Un jardín de 25 a 50 m² se instala en un día. Estos son los cinco pasos básicos.</p>
        <ol class="steps steps--five">
{items}
        </ol>
        <a class="compare__more" href="/blog/como-instalar-pasto-sintetico">Ver la guía completa paso a paso</a>"""


def ciudades_html():
    barato = min(MODELOS, key=lambda m: m["rollo"])
    cards = "\n".join(
        f'          <a class="city-card" href="/pasto-sintetico/envio/{c["slug"]}"><strong>{esc(c["nombre"])}</strong>'
        f'<span class="num">desde ${landed_m2(barato, zona_de(c["estado"]))}/m² puesto</span><span>3 a 5 días hábiles</span></a>'
        for c in CIUDADES
    )
    return f"""<p class="section__intro">Precio puesto con el modelo más económico, envío incluido. Enviamos a los 32 estados; estas son las ciudades con guía propia.</p>
        <div class="city-grid">
{cards}
        </div>
        <p class="spec-note">¿Tienes perros? Lee <a href="/pasto-sintetico/perros">qué pasto sintético conviene para mascotas</a>.</p>"""


def comparador_html():
    return """<p class="section__intro">Muchas ofertas anuncian "envío gratis", pero el envío ya viene en el precio. Compara el precio por m² final.</p>
        <form class="comparador" id="comparador" novalidate>
          <div class="field"><label for="cmp-total">Total de la otra oferta, con envío</label><input class="select" id="cmp-total" type="number" inputmode="decimal" min="1" placeholder="Ej. 14899"></div>
          <div class="field"><label for="cmp-m2">Metros cuadrados que incluye</label><input class="select" id="cmp-m2" type="number" inputmode="numeric" min="1" placeholder="Ej. 50"></div>
          <p class="comparador__out" id="cmp-out" aria-live="polite">Escribe el total y los metros para comparar con nuestro precio puesto en tu estado.</p>
        </form>"""


def local_band_html():
    return """<section class="closing" id="tampico" aria-labelledby="local">
    <div class="wrap">
      <h2 id="local">¿Estás en Tampico, <em>Madero o Altamira?</em></h2>
      <p>Visita el showroom en Cd. Madero. Vendemos desde 2 m² sin flete e instalamos en Tampico, Madero y Altamira.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="/pasto-sintetico-tampico">Venta e instalación en Tampico</a>
        <a class="btn btn--ghost" href="/pasto-sintetico-tampico#showroom">Cómo llegar al showroom</a>
      </div>
    </div>
  </section>"""


def build_hub():
    url = f"{SITE}/pasto-sintetico"
    faqs = faqs_with_html()
    item_list = {
        "@type": "ItemList", "name": "Modelos de pasto sintético residencial con envío a todo México",
        "numberOfItems": len(MODELOS),
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": product_schema(m)} for i, m in enumerate(MODELOS)],
    }
    ld = jsonld([
        breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", url)]),
        faq_schema(faqs),
        item_list,
    ])
    models_json = json.dumps([
        {"slug": m["slug"], "id": m["id"], "nombre": m["nombre"], "img": f"{GAL}/{m['slug']}-2-sm.webp",
         "t1": m["t1"], "t2": m["t2"], "rollo": m["rollo"], "scores": m["scores"], "tag": m["tag"], "mm": m["mm"]}
        for m in MODELOS
    ], ensure_ascii=False)
    hero_img = f"{GAL}/obra-residencial-tampico"
    parts = [
        head(title="Pasto Sintético con Envío a Todo México · Desde $139/m² | Viveros Terra",
             description="Pasto sintético con envío a todo México desde $139/m². 9 modelos residenciales de 10 a 35 mm, factura CFDI 4.0 y entrega en 3 a 5 días hábiles.",
             canonical=url, og_image=f"{SITE}{hero_img}.webp", og_type="website",
             preload_img=f"{GAL}/obra-proyecto-03-sm.webp", preload_srcset=f"{GAL}/obra-proyecto-03-sm.webp 560w, {GAL}/obra-proyecto-03.webp 960w", ld=ld,
             extra=f'<script type="application/json" id="vt-models">{models_json}</script>\n<script src="/js/vt-landed.js?v={ASSET_VERSION}" defer></script>\n<script src="/js/tienda-hub.js?v={ASSET_VERSION}" defer></script>\n'),
        f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li aria-current="page">Pasto sintético</li>
      </ol>
    </nav>
  </div>
  {hero_html()}
  {trust_band_html()}

  {section_open(1, "Colección", "modelos-titulo", "Modelos de pasto sintético <em>de 10 a 35 mm</em>", section_id="modelos")}
        {catalog_html()}{SECTION_CLOSE}
  {section_open(2, "Elegir", "elegir-titulo", "¿Qué pasto sintético <em>te conviene?</em>", tint=True, section_id="elegir")}
        {quiz_html()}{SECTION_CLOSE}
  {section_open(3, "Comparar", "comparar-titulo", "¿Viste otro precio? <em>Compáralo aquí</em>", section_id="comparar")}
        {comparador_html()}{SECTION_CLOSE}
  {section_open(4, "Cotizador", "cotizador-titulo", "Precio del pasto sintético <em>con envío a tu estado</em>", tint=True, section_id="cotizador")}
        {cotizador_html()}{SECTION_CLOSE}
  {section_open(5, "Ciudades", "ciudades-titulo", "Envíos a tu ciudad <em>con precio puesto</em>", section_id="ciudades")}
        {ciudades_html()}{SECTION_CLOSE}
  {section_open(6, "Comparativa", "comparativa-titulo", "Comparativa de modelos <em>por altura, peso y precio</em>", tint=True, section_id="comparativa")}
        {compare_table_html()}{SECTION_CLOSE}
  {section_open(7, "Obras", "obras-titulo", "Pasto sintético instalado <em>en casas reales</em>", section_id="obras")}
        {obras_html()}{SECTION_CLOSE}
  {section_open(8, "Tu pedido", "como-funciona-titulo", "Cómo comprar pasto sintético <em>en línea</em>", tint=True, section_id="como-funciona")}
        {steps_list()}{SECTION_CLOSE}
  {section_open(9, "Instálalo tú", "diy-titulo", "Cómo instalar pasto sintético <em>tú mismo</em>", section_id="instalacion")}
        {diy_html()}{SECTION_CLOSE}
  {section_open(10, "Preguntas", "faq-titulo", "Preguntas frecuentes <em>sobre pasto sintético</em>", tint=True, section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  {local_band_html()}
</main>
""",
        footer(),
        buybar("Pasto sintético · 9 modelos", "Desde $139/m²"),
        drawer_and_toast(),
    ]
    return "".join(parts).replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                  '<a class="skip-link" href="#modelos">Ir a los modelos</a>')


__all__ = ["build_hub", "strip_tags"]
