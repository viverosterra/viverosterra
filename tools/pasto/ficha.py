"""Plantilla de ficha de producto por modelo."""
import json

from common import (GAL, SECTION_CLOSE, assurances, breadcrumb_schema, buybar, drawer_and_toast, esc,
                    faq_html, faq_schema, footer, head, jsonld, money, product_schema, section_open, steps_list)
from data import MODELOS, SITE, WA_NUMBER

NOTE_FLETE = "Te confirmamos el flete exacto a tu dirección antes de pagar."

GLOSSARY = """<dl class="glossary">
          <div><dt>Dtex</dt><dd>Grosor del hilo. A más Dtex, fibra más gruesa y resistente al pisoteo.</dd></div>
          <div><dt>Puntadas por m²</dt><dd>Cuántos mechones hay en cada metro. A más puntadas, menos se ve la base.</dd></div>
          <div><dt>Fibra de soporte</dt><dd>El rizo café de abajo. Mantiene de pie la fibra verde y da el look natural.</dd></div>
          <div><dt>Base</dt><dd>Malla y látex que sujetan cada mechón. Una base más pesada alarga la vida del pasto.</dd></div>
        </dl>"""

ALT_BY_KIND = {
    "rollo": "Rollo de pasto sintético {n} desenrollado, con la base arriba y la fibra {color}",
    "textura": "Acercamiento a la fibra del pasto sintético {n} de {mm} mm en {color}",
    "base": "Base del pasto sintético {n} junto a la fibra, vista a ras de suelo",
    "instalado": "Pasto sintético {n} instalado: {caption}",
}


def neighbors(m):
    """Dos modelos vecinos por altura para la comparativa."""
    i = MODELOS.index(m)
    if i == 0:
        return [MODELOS[1], MODELOS[2]]
    if i == len(MODELOS) - 1:
        return [MODELOS[i - 2], MODELOS[i - 1]]
    return [MODELOS[i - 1], MODELOS[i + 1]]


def build_faqs(m):
    price_plain = (f"Cuesta ${m['rollo']}/m² en rollo completo de 50 m², ${m['t2']}/m² de 10 a 49 m² y "
                   f"${m['t1']}/m² en cortes de 2 a 9 m² en el showroom de Cd. Madero. Los precios incluyen IVA. "
                   "El envío se cobra por rollo según el estado: de $900 a $1,400.")
    entrega = ("Llega en 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo. El mínimo para "
               "envío nacional es 25 m². En el showroom de Cd. Madero puedes comprar desde 2 m².")
    instalar_plain = ("Sí. Sobre tierra compactada se fija con clavos cada 20 a 30 cm. Sobre concreto se pega con "
                      "adhesivo de contacto. Te mandamos la guía de instalación con el pedido.")
    devolver_plain = ("Sí, dentro de 7 días, nuevo y sin cortar. Los cortes a medida no tienen devolución. "
                      "El envío de regreso lo paga el cliente.")
    n = m["nombre"]
    faqs = [
        (f"¿Cuánto cuesta el pasto sintético {n}?", price_plain, esc(price_plain)),
        (m["faq_extra"][0][0], m["faq_extra"][0][1], esc(m["faq_extra"][0][1])),
        (f"¿El {n} sirve para perros y niños?", m["mascotas"], esc(m["mascotas"])),
        ("¿Cuánto tarda en llegar y cuál es el pedido mínimo?", entrega, esc(entrega)),
        (m["faq_extra"][1][0], m["faq_extra"][1][1], esc(m["faq_extra"][1][1])),
        ("¿Lo puedo instalar yo?", instalar_plain,
         esc(instalar_plain) + ' Aquí está la <a href="/blog/como-instalar-pasto-sintetico">guía paso a paso</a>.'),
        ("¿Puedo devolverlo?", devolver_plain,
         esc(devolver_plain) + ' Consulta la <a href="/politicas">política de envíos y devoluciones</a>.'),
    ]
    if m["slug"] == "viena-30":
        q, plain, html = faqs[1]
        faqs[1] = (q, plain, html.replace("En el blog explicamos cómo manejar el calor.",
                   'En el blog explicamos <a href="/blog/pasto-sintetico-calor-mexico">cómo manejar el calor</a>.'))
    return faqs


def gallery_html(m):
    slides, thumbs = [], []
    total = len(m["gallery"])
    for i, (idx, kind, caption) in enumerate(m["gallery"]):
        base = f"{GAL}/{m['slug']}-{idx}"
        alt = ALT_BY_KIND[kind].format(n=m["nombre"], color=m["color"].lower(), mm=m["mm"], caption=caption.lower())
        loading = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
        slides.append(f"""          <figure class="gallery__slide">
            <img src="{base}-sm.webp" srcset="{base}-sm.webp 420w, {base}.webp 720w" sizes="(min-width: 1024px) 620px, 100vw" width="720" height="960" alt="{esc(alt)}" {loading} decoding="async">
            <figcaption class="gallery__caption">{esc(caption)}</figcaption>
          </figure>""")
        thumbs.append(f'            <button class="gallery__thumb" type="button" data-gal-idx="{i}" aria-label="Ver foto {i + 1}: {esc(caption.lower())}"><img src="{base}-sm.webp" alt="" width="64" height="64" loading="lazy"></button>')
    return f"""<section class="gallery" aria-label="Fotos del {esc(m['nombre'])}">
        <div class="gallery__track" id="gal-track" tabindex="0">
{chr(10).join(slides)}
        </div>
        <div class="gallery__meta">
          <span class="gallery__count num" id="gal-count" aria-live="polite">01 / {total:02d}</span>
          <div class="gallery__thumbs">
{chr(10).join(thumbs)}
          </div>
        </div>
      </section>"""


def specstrip_html(m):
    cells = "".join(
        f'<div><dt>{esc(label)}</dt><dd class="num">{esc(value)}{f"<small>{esc(unit)}</small>" if unit else ""}</dd></div>'
        for label, value, unit in m["specstrip"]
    )
    return f'<dl class="specstrip">{cells}</dl>'


def buy_html(m):
    return f"""<section class="buy" id="comprar" aria-labelledby="precio-titulo">
          <h2 class="visually-hidden" id="precio-titulo">Precio y cotización</h2>
          <div class="buy__from">
            <span class="buy__from-label">Desde</span>
            <span class="buy__price num">${m['rollo']}</span>
            <span class="buy__unit">/m²</span>
          </div>
          <p class="buy__terms">Precio por rollo completo de 50 m², IVA incluido. El envío se suma según tu estado.</p>
{tiers_html(m)}
{calc_html()}
{quote_html(m['rollo'] * 50, m['rollo'])}
          <div class="actions">
            <a class="btn btn--primary" data-cta-wa href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener">
              <svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar por WhatsApp
            </a>
            <button class="btn btn--ghost" type="button" id="cta-add">Agregar a mi cotización</button>
            <p class="actions__note">{NOTE_FLETE}</p>
          </div>
        </section>"""


def tiers_html(m):
    return f"""          <table class="tiers num">
            <caption>Precio por volumen</caption>
            <tbody>
              <tr data-tier="rollo"><th scope="row">Rollo completo<span>50 m² o más</span></th><td id="tier-rollo">${m['rollo']}/m²</td></tr>
              <tr data-tier="t2"><th scope="row">Corte mediano<span>10 a 49 m²</span></th><td id="tier-t2">${m['t2']}/m²</td></tr>
              <tr data-tier="t1"><th scope="row">Corte chico<span>2 a 9 m², solo en showroom</span></th><td id="tier-t1">${m['t1']}/m²</td></tr>
            </tbody>
          </table>"""


def calc_html(model_select=""):
    from common import ESTADO_OPTIONS
    return f"""          <div class="calc">
{model_select}            <div class="field">
              <label for="m2">Metros cuadrados</label>
              <div class="stepper">
                <button type="button" id="m2-minus" aria-label="Restar 5 m²">−</button>
                <input id="m2" class="num" type="number" inputmode="numeric" min="2" max="5000" step="1" value="50">
                <button type="button" id="m2-plus" aria-label="Sumar 5 m²">+</button>
              </div>
              <div class="chips" role="group" aria-label="Medidas rápidas">
                <button class="chip num" type="button" data-m2="25" aria-pressed="false">25 m²</button>
                <button class="chip num" type="button" data-m2="50" aria-pressed="true">50 m²</button>
                <button class="chip num" type="button" data-m2="100" aria-pressed="false">100 m²</button>
              </div>
            </div>
            <div class="field">
              <label for="estado">Entrega</label>
              <select class="select" id="estado">
                {ESTADO_OPTIONS}
              </select>
            </div>
          </div>"""


def quote_html(material, pm2):
    return f"""          <div class="quote num" aria-live="polite">
            <div class="quote__row"><span>Precio aplicado</span><strong id="q-pm2">{money(pm2)}/m²</strong></div>
            <div class="quote__row"><span>Material</span><strong id="q-material">{money(material)}</strong></div>
            <div class="quote__row"><span id="q-envio-label">Envío</span><strong id="q-envio">Elige tu estado</strong></div>
            <div class="quote__total"><span id="q-total-label">Total estimado</span><strong id="q-total">{money(material)}</strong></div>
            <p class="quote__landed" id="q-landed"></p>
            <p class="quote__hint" id="q-hint"></p>
            <p class="quote__error" id="q-error" role="alert"></p>
          </div>"""


def compare_html(m):
    cards = []
    for x in sorted([m] + neighbors(m), key=lambda z: z["n"]):
        current = x is m
        tag = "Estás viendo" if current else x["tag"]
        gar = f"{x['garantia']} años" if x["garantia"] else "Consultar"
        inner = f"""<img src="{GAL}/{x['slug']}-2-sm.webp" width="420" height="560" alt="Textura del pasto sintético {esc(x['nombre'])}" loading="lazy">
            <span class="compare__tag">{esc(tag)}</span>
            <h3 class="compare__name">{esc(x['nombre'])}</h3>
            <dl><div><dt>Altura</dt><dd>{x['mm']} mm</dd></div><div><dt>Peso</dt><dd>{x['peso']} g/m²</dd></div><div><dt>Garantía</dt><dd>{gar}</dd></div></dl>
            <p class="compare__price">Desde <strong>${x['rollo']}</strong>/m²</p>"""
        if current:
            cards.append(f'          <div class="compare__card" aria-current="page">\n            {inner}\n          </div>')
        else:
            cards.append(f'          <a class="compare__card" href="/pasto-sintetico/{x["slug"]}">\n            {inner}\n          </a>')
    return f"""<div class="compare num">
{chr(10).join(cards)}
        </div>
        <a class="compare__more" href="/pasto-sintetico#modelos">Ver los 9 modelos</a>"""


def spec_sheet_html(m):
    groups = []
    for title, rows in m["specs"]:
        items = "".join(
            f'<div><dt>{esc(label)}{f"<small>{esc(norm)}</small>" if norm else ""}</dt><dd>{esc(value)}</dd></div>'
            for label, norm, value in rows
        )
        groups.append(f'          <div class="spec-group">\n            <h3>{esc(title)}</h3>\n            <dl>{items}</dl>\n          </div>')
    note = m.get("specs_note") or ("Datos de la ficha técnica del fabricante. Entre paréntesis va la norma con la que "
                                   "se mide cada dato. Las tolerancias son las de fábrica.")
    return f"""<div class="spec-sheet num">
{chr(10).join(groups)}
        </div>
        <p class="spec-note">{esc(note)}</p>
        {"" if m.get("specs_note") else GLOSSARY}"""


def photos_section(m):
    installed = [(i, c) for i, k, c in m["gallery"] if k == "instalado"]
    rollo = f"{GAL}/{m['slug']}-rollo.webp"
    if installed:
        idx, cap = installed[0]
        main_src, main_alt, main_cap = f"{GAL}/{m['slug']}-{idx}.webp", f"Pasto sintético {m['nombre']} instalado: {cap.lower()}", f"{cap}. {m['nombre']} instalado."
        title, label = "Así se ve <em>instalado</em>", "Instalado"
    else:
        textura = [i for i, k, _c in m["gallery"] if k == "textura"][0]
        main_src, main_alt, main_cap = f"{GAL}/{m['slug']}-{textura}.webp", f"Acercamiento a la fibra del pasto sintético {m['nombre']}", "Detalle de la fibra, sin retoque."
        title, label = "Así se ve <em>de cerca</em>", "De cerca"
    body = f"""
        <div class="installed">
          <figure class="installed__main">
            <img src="{main_src}" width="720" height="960" alt="{esc(main_alt)}" loading="lazy" decoding="async">
            <figcaption>{esc(main_cap)}</figcaption>
          </figure>
          <figure class="installed__side">
            <img src="{rollo}" width="564" height="452" alt="Rollo de {esc(m['nombre'])} abierto sobre el piso antes de instalar" loading="lazy" decoding="async">
            <figcaption>Así llega: rollo de 2 m de ancho.</figcaption>
          </figure>
        </div>"""
    return label, title, body


def fit_html(m):
    items = [f"<li>{esc(t)}</li>" for t in m["fit_si"]] + [f'<li class="no">{esc(t)}</li>' for t in m["fit_no"]]
    return '<ul class="fit">\n          ' + "\n          ".join(items) + "\n        </ul>"


def build_ficha(m):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    faqs = build_faqs(m)
    gar = f"garantía de {m['garantia']} años" if m["garantia"] else "uso decorativo"
    title = f"Pasto Sintético {m['nombre']} desde ${m['rollo']}/m² · Envío a Todo México"
    desc = f"{m['nombre']}: {m['mm']} mm, {m['peso']} g/m² y {gar}. Desde ${m['rollo']}/m² en rollo, con factura y envío a todo México en 3 a 5 días."
    ld = jsonld([
        breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", f"{SITE}/pasto-sintetico"), (m["nombre"], url)]),
        product_schema(m),
        faq_schema(faqs),
    ])
    first = f"{GAL}/{m['slug']}-{m['gallery'][0][0]}"
    model_json = json.dumps({"slug": m["slug"], "nombre": m["nombre"], "img": f"{GAL}/{m['slug']}-2-sm.webp",
                             "t1": m["t1"], "t2": m["t2"], "rollo": m["rollo"]}, ensure_ascii=False)
    badge = f'<sup title="Versión {esc(m["badge"].lower())}">{esc(m["badge"])}</sup>' if m.get("badge") else ""
    stock = '<span class="stock">En existencia</span>' if m["stock"] else '<span>Envío en 3 a 5 días</span>'
    photos_label, photos_title, photos_body = photos_section(m)
    gar_text = f"Garantía de {m['garantia']} años" if m["garantia"] else "Garantía de fábrica"

    parts = [
        head(title=title, description=desc, canonical=url, og_image=f"{SITE}{first}.webp", og_type="product",
             preload_img=f"{first}-sm.webp", preload_srcset=f"{first}-sm.webp 420w, {first}.webp 720w", ld=ld,
             extra=f'<script type="application/json" id="vt-model">{model_json}</script>\n'),
        f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li><a href="/pasto-sintetico">Pasto sintético</a></li>
        <li aria-current="page">{esc(m['nombre'])}</li>
      </ol>
    </nav>

    <article class="pdp" aria-labelledby="titulo">
      {gallery_html(m)}

      <div class="pdp__info">
        <p class="eyebrow"><span>N.º {m['n']:02d} / 09 · {esc(m['tag'])}</span>{stock}</p>
        <p class="pdp__kicker">Pasto sintético</p>
        <h1 class="pdp__title" id="titulo">{esc(m['nombre'])}{badge}</h1>
        <p class="pdp__lede">{esc(m['lede'])}</p>

        {specstrip_html(m)}

        {buy_html(m)}

        {assurances(gar_text)}
      </div>
    </article>
  </div>

  {section_open(1, "En resumen", "resumen", f"Para quién es el <em>{esc(m['nombre'])}</em>")}
        <p class="summary">{m['resumen']}</p>
        {fit_html(m)}{SECTION_CLOSE}
  {section_open(2, "Ficha técnica", "ficha", "Los datos de fábrica, <em>sin letra chica</em>", tint=True, section_id="ficha-tecnica")}
        {spec_sheet_html(m)}{SECTION_CLOSE}
  {section_open(3, photos_label, "fotos", photos_title)}{photos_body}{SECTION_CLOSE}
  {section_open(4, "Compáralo", "compara", "Sus vecinos <em>en la colección</em>", tint=True)}
        {compare_html(m)}{SECTION_CLOSE}
  {section_open(5, "Tu pedido", "pedido", "Cómo compras, <em>paso a paso</em>")}
        {steps_list()}{SECTION_CLOSE}
  {section_open(6, "Preguntas", "preguntas", "Lo que más nos <em>preguntan</em>", tint=True)}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="cierre">
    <div class="wrap">
      <h2 id="cierre">Tu jardín listo <em>esta misma semana</em></h2>
      <p>Mándanos tus metros y tu estado. Te respondemos con el precio final y la fecha de entrega.</p>
      <div class="closing__actions">
        <a class="btn btn--light" data-cta-wa href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar {esc(m['nombre'])}</a>
        <a class="btn btn--ghost" href="#comprar">Calcular mi pedido</a>
      </div>
    </div>
  </section>
</main>
""",
        footer(),
        buybar(f"{m['nombre']}{' · ' + m['badge'] if m.get('badge') else ''}", f"Desde ${m['rollo']}/m²"),
        drawer_and_toast(),
    ]
    return "".join(parts)
