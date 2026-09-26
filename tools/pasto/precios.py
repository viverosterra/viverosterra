"""Página /precios: lista de precios de todo Viveros Terra con el estilo de la tienda.

Los precios de pasto sintético salen de data.py; el resto son los datos oficiales confirmados por el dueño.
"""
from common import (SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, head, jsonld, section_open, wa)
from data import MODELOS, PHONE_DISPLAY, SITE, UPDATED, WA_NUMBER

URL = f"{SITE}/precios"
BUSINESS_ID = f"{SITE}/#negocio"
IMG = "/img/precios/pasto-rollo-jardin"
MAPS = "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"
APPLE_MAPS = "https://maps.apple.com/?daddr=22.2777575,-97.8433341&amp;q=Viveros%20Terra"

PASTO_M2, PASTO_INSTALADO = 85, 120
MANTENIMIENTO = 750
SINTETICO_MIN = min(m["rollo"] for m in MODELOS)
SINTETICO_INSTALADO = (385, 650)

# (nombre, enlace, precio, detalle)
PASTO = [
    ("Pasto San Agustín, solo el pasto", "/pasto-en-rollo-tampico", f"${PASTO_M2}/m²",
     "Rollo fresco, cortado para tu pedido. Recoges en el vivero o te lo llevamos."),
    ("Pasto San Agustín instalado", "/pasto-en-rollo-tampico", f"desde ${PASTO_INSTALADO}/m²",
     "Preparación básica del suelo, instalación y garantía de arraigo de 15 a 20 días."),
    ("Mayoreo para constructoras y fraccionamientos", "/mayoreo-pasto-tampico", "desde $60/m²",
     "Pedidos de 500 m² o más, con entregas por etapas según el avance de la obra y factura."),
]
SERVICIOS = [
    ("Mantenimiento de jardín", "/mantenimiento-jardines-tampico", f"desde ${MANTENIMIENTO:,}/mes",
     "Poda, fertilización y control de plagas. Cada 15 a 21 días en lluvias y cada 30 días en secas."),
    ("Diseño de jardín, Plan Terra Esencial", "/diseno-jardines-tampico", "$3,000",
     "Visita, propuesta de diseño y lista de materiales. Entrega en 3 a 5 días hábiles."),
    ("Diseño de jardín, Plan Terra Completo", "/diseno-jardines-tampico", "$6,500",
     "Diseño detallado, fichas de plantas, cuantificación de materiales y manual de cuidados."),
    ("Diseño de jardín, Plan Terra Premium", "/diseno-jardines-tampico", "desde $18,000",
     "Proyecto ejecutivo con seguimiento. El costo del diseño se descuenta si contratas la obra."),
    ("Sistema de riego automático", "/sistema-riego-tampico", "$180 a $320/m²",
     "Aspersión o goteo con programador. Se cotiza después de medir y revisar la presión."),
]
MATERIALES = [
    ("Tierra negra vegetal", "/tierra-negra-vegetal-tampico", "costal $90",
     "Tierra preparada $100 el costal · $1,500 el m³ · camión desde $5,000."),
    ("Tezontle rojo", "/tezontle-rojo-tampico", "costal $200", "También por m³ o en camión de 14 m³."),
    ("Mármol blanco decorativo", "/marmol-blanco-tampico", "saco $250", "Saco de unos 20 kg; 3 sacos cubren 1 m²."),
    ("Piedra bola de río", "/piedra-bola-rio-tampico", "por medida", "Chica, mediana y grande, en costal o camión."),
]
PLANTAS = [
    ("Palmas", "/palmas-para-jardin-tampico", "desde $850", "Areca, coco plumoso, real, washingtonia, del viajero y más. El precio sube con la altura."),
    ("Árboles", "/arboles-ornamentales-tampico", "por tamaño", "Framboyán, jacaranda, olivo negro, crespón, guayacán y más."),
    ("Plantas de jardín e interior", "/plantas-para-jardin-tampico", "por tamaño", "Más de 200 variedades en el vivero."),
]

FAQS = [
    ("¿Cuánto cuesta el pasto en rollo en Tampico?",
     f"El pasto San Agustín cuesta ${PASTO_M2}/m² solo el pasto y desde ${PASTO_INSTALADO}/m² instalado, con preparación "
     "básica del suelo y garantía de arraigo de 15 a 20 días. En pedidos de 500 m² o más, el mayoreo cuesta desde $60/m²."),
    ("¿Los precios incluyen IVA?",
     "Sí. Todos los precios de esta página incluyen IVA. Damos factura CFDI 4.0 a persona física o moral y tenemos "
     "registro REPSE 773725 para contratos con empresas."),
    ("¿Por qué algunos precios dicen «desde»?",
     "Porque el total depende de los metros, del estado del terreno y del acceso a la obra. En la visita medimos y te "
     "damos el precio cerrado antes de empezar. La visita no tiene costo."),
    ("¿Cuánto cuesta el pasto sintético en Tampico?",
     f"El material cuesta desde ${SINTETICO_MIN}/m² en rollo completo y el pasto instalado de ${SINTETICO_INSTALADO[0]} "
     f"a ${SINTETICO_INSTALADO[1]}/m² según el modelo, con material y colocación. La preparación del terreno se cotiza aparte."),
    ("¿Las plantas y palmas tienen garantía?",
     "Las que sembramos nosotros tienen 30 días de garantía de arraigo, con el riego y cuidado que te indicamos. "
     "No cubre falta de riego, cambio de lugar, daños por mascotas ni clima extremo."),
    ("¿Cada cuánto cambian estos precios?",
     f"Revisamos la lista cada temporada. Esta versión es de {UPDATED}. Si algo cambió, vale el precio que te "
     "confirmemos por WhatsApp."),
]


def faqs_with_html():
    links = {
        "¿Cuánto cuesta el pasto sintético": ' Ve los <a href="/pasto-sintetico">9 modelos con precio</a>.',
        "¿Las plantas y palmas": ' Lee las <a href="/politicas#garantia-plantas">condiciones de la garantía</a>.',
        "¿Cuánto cuesta el pasto en rollo": ' Más detalles en <a href="/pasto-en-rollo-tampico">pasto en rollo</a>.',
    }
    out = []
    for q, a in FAQS:
        extra = next((v for k, v in links.items() if q.startswith(k)), "")
        out.append((q, a, esc(a) + extra))
    return out


def rows_html(rows):
    return "\n".join(
        f"""            <tr><th scope="row"><a href="{href}">{esc(name)}</a><span>{esc(detail)}</span></th><td><strong>{esc(price)}</strong></td></tr>"""
        for name, href, price, detail in rows
    )


def table_html(label, rows, note=""):
    note_html = f'\n        <p class="spec-note">{note}</p>' if note else ""
    return f"""<div class="table-scroll" tabindex="0" role="region" aria-label="{esc(label)}">
          <table class="compare-table compare-table--prices num">
            <thead><tr><th scope="col">Producto o servicio</th><th scope="col">Precio con IVA</th></tr></thead>
            <tbody>
{rows_html(rows)}
            </tbody>
          </table>
        </div>{note_html}"""


def sintetico_html():
    rows = "\n".join(
        f"""            <tr><th scope="row"><a href="/pasto-sintetico/{m['slug']}">{esc(m['nombre'])}</a><span>{m['mm']} mm</span></th><td>${m['t1']}</td><td>${m['t2']}</td><td><strong>${m['rollo']}</strong></td></tr>"""
        for m in MODELOS
    )
    return f"""<p class="section__intro">Material por m² según cuánto compres. Instalado en Tampico, Madero y Altamira de ${SINTETICO_INSTALADO[0]} a ${SINTETICO_INSTALADO[1]}/m² con material y colocación.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Precios de pasto sintético">
          <table class="compare-table compare-table--compact num">
            <thead><tr><th scope="col">Modelo</th><th scope="col">2 a 9 m²</th><th scope="col">10 a 49 m²</th><th scope="col">Rollo 50 m²</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="spec-note">Cortes de 2 a 9 m² solo en el showroom. Envío a todo México desde 25 m²; el flete se cobra por rollo según tu estado. <a href="/pasto-sintetico">Ver la tienda</a> · <a href="/pasto-sintetico-tampico">Instalación en Tampico</a></p>"""


def hero_html():
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Lista de precios</span><span class="stock">Actualizada en {esc(UPDATED)}</span></p>
        <h1 class="hub-hero__title" id="titulo">Precios de jardinería en Tampico <em>2026, con IVA</em></h1>
        <p class="summary summary--hero">En Tampico, Madero y Altamira, el pasto San Agustín cuesta <strong>${PASTO_M2}/m²</strong> solo el pasto y <strong>desde ${PASTO_INSTALADO}/m²</strong> instalado. El mantenimiento de jardín cuesta desde <strong>${MANTENIMIENTO}/mes</strong>, el diseño desde <strong>$3,000</strong> y el pasto sintético desde <strong>${SINTETICO_MIN}/m²</strong>. Precios de Viveros Terra, con IVA y factura.</p>
        <dl class="specstrip">
          <div><dt>Pasto en rollo</dt><dd class="num">${PASTO_M2}<small>/m²</small></dd></div>
          <div><dt>Pasto instalado</dt><dd class="num"><small>desde</small> ${PASTO_INSTALADO}<small>/m²</small></dd></div>
          <div><dt>Mantenimiento</dt><dd class="num"><small>desde</small> ${MANTENIMIENTO}<small>/mes</small></dd></div>
          <div><dt>Pasto sintético</dt><dd class="num"><small>desde</small> ${SINTETICO_MIN}<small>/m²</small></dd></div>
        </dl>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="{wa('Hola, vi la lista de precios y quiero cotizar. Mi colonia es: ___ y son aprox. ___ m²')}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar por WhatsApp</a>
          <a class="btn btn--ghost" href="#pasto">Ver la lista</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="{IMG}-sm.webp" srcset="{IMG}-sm.webp 560w, {IMG}.webp 960w" sizes="(min-width: 1024px) 560px, 100vw" width="960" height="1185" alt="Trabajador de Viveros Terra descargando pasto San Agustín en rollo de la camioneta" style="object-position:center 35%" fetchpriority="high" decoding="async">
        <figcaption>Pasto San Agustín recién cortado, listo para instalar.</figcaption>
      </figure>
    </div>
  </section>"""


HEADER = """<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="/" aria-label="Viveros Terra, inicio"><img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="140" height="36"></a>
    <nav class="site-nav" aria-label="Principal">
      <a href="/pasto-en-rollo-tampico">Pasto en rollo</a>
      <a href="/pasto-sintetico">Pasto sintético</a>
      <a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a>
      <a href="/diseno-jardines-tampico">Diseño</a>
      <a href="/mantenimiento-jardines-tampico">Mantenimiento</a>
    </nav>
    <a class="quote-btn" href="{wa}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg><span>Cotizar</span></a>
  </div>
</header>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="130" height="34" loading="lazy">
        <p>Vivero, pasto en rollo y servicios de jardinería en Tampico, Madero y Altamira desde 2007.</p>
        <p><a href="{MAPS}" target="_blank" rel="noopener">Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, 89510 Cd. Madero, Tamps.</a><br><a href="{MAPS}" target="_blank" rel="noopener">Google Maps</a> · <a href="{APPLE_MAPS}" target="_blank" rel="noopener">Apple Maps</a></p>
      </div>
      <div>
        <h3>Servicios</h3>
        <ul>
          <li><a href="/pasto-en-rollo-tampico">Pasto en rollo</a></li>
          <li><a href="/mantenimiento-jardines-tampico">Mantenimiento</a></li>
          <li><a href="/diseno-jardines-tampico">Diseño de jardines</a></li>
          <li><a href="/sistema-riego-tampico">Riego automático</a></li>
          <li><a href="/pasto-sintetico-tampico">Pasto sintético en Tampico</a></li>
        </ul>
      </div>
      <div>
        <h3>Contacto</h3>
        <ul>
          <li><a href="{wa('Hola, tengo una pregunta sobre precios')}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li><a href="tel:+528333268008">Llamar {PHONE_DISPLAY}</a></li>
          <li>Lun a vie 9 a 18 h · Sáb 9 a 14 h</li>
          <li><a href="/politicas">Envíos, devoluciones y garantías</a></li>
        </ul>
      </div>
    </div>
    <p class="site-footer__legal">© 2026 Viveros Terra · Cd. Madero, Tamaulipas, México · Actualizado {UPDATED}</p>
  </div>
</footer>
"""


def offer(name, price, url, unit=None):
    o = {"@type": "Offer", "name": name, "price": str(price), "priceCurrency": "MXN", "url": f"{SITE}{url}",
         "seller": {"@id": BUSINESS_ID}}
    if unit:
        o["priceSpecification"] = {"@type": "UnitPriceSpecification", "price": str(price), "priceCurrency": "MXN", "unitText": unit}
    return o


def schema(faqs):
    catalog = {
        "@type": "OfferCatalog", "@id": f"{URL}#lista", "name": "Lista de precios de Viveros Terra",
        "itemListElement": [
            offer("Pasto San Agustín en rollo, solo el pasto", PASTO_M2, "/pasto-en-rollo-tampico", "m²"),
            offer("Pasto San Agustín instalado", PASTO_INSTALADO, "/pasto-en-rollo-tampico", "m²"),
            offer("Pasto San Agustín al mayoreo, desde 500 m²", 60, "/mayoreo-pasto-tampico", "m²"),
            offer("Mantenimiento de jardín mensual", MANTENIMIENTO, "/mantenimiento-jardines-tampico", "mes"),
            offer("Diseño de jardín, Plan Terra Esencial", 3000, "/diseno-jardines-tampico"),
            offer("Diseño de jardín, Plan Terra Completo", 6500, "/diseno-jardines-tampico"),
            offer("Diseño de jardín, Plan Terra Premium", 18000, "/diseno-jardines-tampico"),
            offer("Pasto sintético, material en rollo", SINTETICO_MIN, "/pasto-sintetico", "m²"),
            offer("Tierra negra vegetal, costal", 90, "/tierra-negra-vegetal-tampico"),
            offer("Tezontle rojo, costal", 200, "/tezontle-rojo-tampico"),
            offer("Mármol blanco, saco", 250, "/marmol-blanco-tampico"),
            offer("Palmas", 850, "/palmas-para-jardin-tampico"),
        ],
    }
    page = {"@type": "WebPage", "@id": URL, "url": URL, "name": "Precios de jardinería en Tampico 2026",
            "dateModified": "2026-09-26", "about": {"@id": BUSINESS_ID}, "mainEntity": {"@id": f"{URL}#lista"}}
    return jsonld([breadcrumb_schema([("Inicio", SITE), ("Precios", URL)]), page, catalog, faq_schema(faqs)])


def build_precios():
    faqs = faqs_with_html()
    base = head(
        title="Precios de jardinería en Tampico 2026: pasto, diseño y mantenimiento | Viveros Terra",
        description=f"Pasto San Agustín ${PASTO_M2}/m² o instalado desde ${PASTO_INSTALADO}/m², mantenimiento desde ${MANTENIMIENTO}/mes, "
                    f"diseño desde $3,000 y pasto sintético desde ${SINTETICO_MIN}/m². Precios con IVA en Tampico, Madero y Altamira.",
        canonical=URL, og_image=f"{SITE}{IMG}.webp", og_type="website",
        preload_img=f"{IMG}-sm.webp", preload_srcset=f"{IMG}-sm.webp 560w, {IMG}.webp 960w", ld=schema(faqs),
    )
    base = (base.split('<script src="/js/tienda-pasto.js')[0] + base.split("defer></script>", 1)[1])
    base = base.split('<header class="site-header">')[0].replace(
        '<a class="skip-link" href="#comprar">Ir al cotizador</a>', '<a class="skip-link" href="#pasto">Ir a la lista de precios</a>')
    base += HEADER.format(wa=wa("Hola, vi la lista de precios y quiero cotizar"))
    return "".join([base, f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li aria-current="page">Precios</li>
      </ol>
    </nav>
  </div>
  {hero_html()}

  {section_open(1, "Pasto natural", "pasto-titulo", "Pasto San Agustín <em>en rollo</em>", section_id="pasto")}
        {table_html("Precios de pasto natural", PASTO, 'Solo el pasto: recoges en el vivero o se cobra la entrega según tu colonia. <a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de riego y garantía</a>.')}{SECTION_CLOSE}
  {section_open(2, "Servicios", "servicios-titulo", "Mantenimiento, diseño <em>y riego</em>", tint=True, section_id="servicios")}
        {table_html("Precios de servicios de jardinería", SERVICIOS, "Visita técnica sin costo. Contratos con empresas con factura y REPSE 773725.")}{SECTION_CLOSE}
  {section_open(3, "Pasto sintético", "sintetico-titulo", "Pasto sintético <em>por modelo</em>", section_id="sintetico")}
        {sintetico_html()}{SECTION_CLOSE}
  {section_open(4, "Materiales", "materiales-titulo", "Tierra, tezontle <em>y piedra</em>", tint=True, section_id="materiales")}
        {table_html("Precios de materiales para jardín", MATERIALES, "Recoges en el vivero de Cd. Madero o te lo llevamos en Tampico, Madero y Altamira.")}{SECTION_CLOSE}
  {section_open(5, "Vivero", "plantas-titulo", "Plantas, palmas <em>y árboles</em>", section_id="plantas")}
        {table_html("Precios de plantas y palmas", PLANTAS, 'Arma tu lista en el <a href="/catalogo">catálogo</a> y mándala por WhatsApp. Las plantas y palmas que sembramos tienen 30 días de garantía de arraigo con el riego y cuidado indicados. <a href="/politicas#garantia-plantas">Ver condiciones</a>.')}{SECTION_CLOSE}
  {section_open(6, "Preguntas", "faq-titulo", "Preguntas sobre <em>precios</em>", tint=True, section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="cierre">
    <div class="wrap">
      <h2 id="cierre">¿Quieres el precio exacto <em>de tu jardín?</em></h2>
      <p>Mándanos tu colonia, los metros aproximados y una foto del espacio. Te respondemos hoy y, si hace falta, vamos a medir sin costo.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="{wa('Hola, quiero el precio exacto de mi jardín. Mi colonia es: ___ · Metros aprox.: ___ · Te mando foto del espacio.')}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        <a class="btn btn--ghost" href="tel:+528333268008">Llamar {PHONE_DISPLAY}</a>
      </div>
    </div>
  </section>
</main>
""", footer(), "</body>\n</html>\n"])
