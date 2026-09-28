"""Páginas locales por zona: 6 zonas de mayor poder adquisitivo en Tampico, Madero y Altamira.

Sustituyen a las 20 páginas por colonia (las demás redirigen en vercel.json).
Colonias, municipios y códigos postales verificados con directorios SEPOMEX (septiembre 2026).
No afirmar obras concretas en una colonia sin foto o dato del dueño.
"""
from common import SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, head, jsonld, section_open, wa
from data import SITE
from precios import HEADER, footer

BUSINESS_ID = f"{SITE}/#negocio"

PRECIOS = [
    ("Pasto San Agustín instalado", "/pasto-en-rollo-tampico", "desde $120/m²", "Preparación básica del suelo y garantía de arraigo de 15 a 20 días."),
    ("Mantenimiento de jardín", "/mantenimiento-jardines-tampico", "desde $750/mes", "Poda, fertilización, control de plagas y revisión del riego."),
    ("Diseño de jardín", "/diseno-jardines-tampico", "desde $3,000", "Plan Esencial; se descuenta si contratas la obra."),
    ("Riego automático", "/sistema-riego-tampico", "$180 a $320/m²", "Aspersión o goteo con programador."),
    ("Palmas", "/palmas-tropicales-tampico", "desde $250", "Areca y coco plumoso en tamaño chico; se cotizan por tamaño y volumen."),
]

ZONAS = {
    "jardineria-lomas-de-rosales-tampico": dict(
        nombre="Lomas de Rosales", municipio="Tampico", corto="Lomas de Rosales",
        title="Jardinería en Lomas de Rosales, Tampico: pasto, diseño y mantenimiento",
        h1="Jardinería en Lomas de Rosales", accent="y Vista Hermosa, Tampico",
        colonias=[("Lomas de Rosales", "89100"), ("Lomas de la Aurora", "89100"), ("Vista Hermosa", "89119")],
        lede="Pasto en rollo, diseño, riego y mantenimiento para las casas de Lomas de Rosales, Lomas de la Aurora y Vista Hermosa, en Tampico.",
        retos=[
            ("Terrenos en pendiente", "En la loma el agua de riego y de lluvia escurre. El riego por goteo y las jardineras escalonadas evitan que se lave la tierra y el pasto se seque en la parte alta."),
            ("Lotes amplios", "Jardines grandes piden un plan de mantenimiento fijo. Con visitas cada 15 a 21 días en lluvias y cada 30 en secas, el pasto se mantiene parejo."),
            ("Sol fuerte en la parte alta", "Para las zonas más expuestas conviene pasto San Agustín y palmas de sol pleno como coco plumoso o washingtonia."),
        ],
        img=("diseno-jardines-tampico-proyecto", 960, 1574, "center 55%"),
        faqs=[
            ("¿Dan servicio de jardinería en Lomas de Rosales?", "Sí. Atendemos Lomas de Rosales, Lomas de la Aurora y Vista Hermosa en Tampico con instalación de pasto, diseño, riego y mantenimiento. La visita para medir no tiene costo."),
            ("¿Cuánto cuesta el mantenimiento de jardín en Lomas de Rosales?", "Desde $750 al mes. El precio final depende de los metros del jardín y de la frecuencia de visitas."),
            ("¿Qué riego conviene en un jardín con pendiente?", "Goteo en jardineras y aspersión de bajo caudal en el pasto, con zonas separadas para la parte alta y la baja. Así el agua no escurre y se aprovecha mejor."),
        ],
    ),
    "jardineria-country-club-tampico": dict(
        nombre="Club Campestre y Country Club", municipio="Tampico", corto="Club Campestre",
        title="Jardinería en Club Campestre y Country Club, Tampico",
        h1="Jardinería en Club Campestre", accent="y Country Club, Tampico",
        colonias=[("Club Campestre", "89217"), ("Country Club", "89218"), ("Sierra Morena", "89210")],
        lede="Instalación de pasto, diseño de jardín, riego automático y mantenimiento para las casas de Club Campestre, Country Club y Sierra Morena, en Tampico.",
        retos=[
            ("Jardines grandes", "En lotes amplios, el riego automático por zonas ahorra agua y tiempo. Lo diseñamos según el pasto, las jardineras y la presión de tu casa."),
            ("Pasto parejo todo el año", "El pasto San Agustín necesita poda frecuente en lluvias y fertilización por temporada. Un plan mensual evita que se amarille en secas."),
            ("Palmas y árboles grandes", "Sembramos palmas y árboles de porte con garantía de arraigo de 30 días, con el riego y cuidado que te indicamos."),
        ],
        img=("jardin-residencial-tropical-tampico", 960, 640, None),
        faqs=[
            ("¿Atienden jardines en Club Campestre y Country Club?", "Sí. Atendemos Club Campestre, Country Club y Sierra Morena en Tampico con pasto en rollo, diseño, riego automático y mantenimiento."),
            ("¿Cuánto cuesta un sistema de riego automático?", "De $180 a $320 por m², según el tipo de sistema. Medimos y revisamos la presión en la visita, sin costo."),
            ("¿Pueden encargarse del jardín todo el año?", "Sí. El mantenimiento cuesta desde $750 al mes, con visitas cada 15 a 21 días en lluvias y cada 30 días en secas."),
        ],
    ),
    "jardineria-aguila-tampico": dict(
        nombre="Águila, Altavista y Petrolera", municipio="Tampico", corto="Águila y Altavista",
        title="Jardinería en Águila, Altavista y Petrolera, Tampico",
        h1="Jardinería en Águila,", accent="Altavista y Petrolera, Tampico",
        colonias=[("Águila", "89230"), ("Altavista", "89240"), ("Petrolera", "89110"), ("Campbell", "89260")],
        lede="Pasto, poda de árboles, diseño y mantenimiento para las casas de Águila, Altavista, Petrolera y Campbell, en Tampico.",
        retos=[
            ("Árboles grandes y sombra", "Son colonias con árboles maduros. El pasto San Agustín aguanta media sombra, pero bajo copas cerradas conviene plantas de sombra o cubresuelos."),
            ("Jardines de frente y patios", "En espacios medianos, un diseño sencillo con pasto, jardineras y dos o tres palmas da más orden y menos mantenimiento."),
            ("Poda y raíces", "Podamos árboles y palmas con técnica para no dañarlos. Si una raíz levanta la banqueta, te recomendamos especies de raíz controlada."),
        ],
        img=("mantenimiento-jardines-poda-pasto-tampico", 960, 1440, "center 45%"),
        faqs=[
            ("¿Dan servicio de jardinería en la colonia Águila y Altavista?", "Sí. Atendemos Águila, Altavista, Petrolera y Campbell en Tampico con pasto en rollo, poda, diseño y mantenimiento."),
            ("¿El pasto San Agustín crece en sombra?", "Aguanta media sombra, con unas 4 horas de sol directo. Bajo árboles muy cerrados te recomendamos plantas de sombra o cubresuelos."),
            ("¿Cuánto cuesta poner pasto en el frente de mi casa?", "El pasto San Agustín instalado cuesta desde $120/m² con preparación básica del suelo. Solo el pasto cuesta $85/m²."),
        ],
    ),
    "jardineria-lomas-del-chairel-tampico": dict(
        nombre="Lomas del Chairel", municipio="Tampico", corto="Lomas del Chairel",
        title="Jardinería en Lomas del Chairel y Colinas de San Gerardo, Tampico",
        h1="Jardinería en Lomas del Chairel", accent="y Colinas de San Gerardo",
        colonias=[("Lomas del Chairel", "89360"), ("Colinas de San Gerardo", "89367"), ("Flamboyanes", "89330")],
        lede="Pasto en rollo, riego, diseño y mantenimiento para las casas cerca de la laguna del Chairel: Lomas del Chairel, Colinas de San Gerardo y Flamboyanes.",
        retos=[
            ("Humedad y lluvias", "Cerca de la laguna el suelo tarda más en secar. Un buen drenaje y tierra bien preparada evitan hongos y encharcamientos en el pasto."),
            ("Casas nuevas", "En fraccionamientos recientes el suelo suele ser de relleno. Antes del pasto conviene una capa de tierra negra vegetal."),
            ("Mosquitos y agua estancada", "Revisamos que el riego no deje charcos y que las macetas y jardineras drenen bien."),
        ],
        img=("riego-pro-01", 960, 640, None),
        faqs=[
            ("¿Atienden jardines en Lomas del Chairel y Colinas de San Gerardo?", "Sí. Atendemos Lomas del Chairel, Colinas de San Gerardo y Flamboyanes en Tampico con pasto, riego, diseño y mantenimiento."),
            ("¿Qué hago si mi jardín se encharca?", "Revisamos el nivel del terreno y el drenaje. A veces basta con nivelar y mejorar la tierra; en otros casos hace falta un dren. Lo vemos en la visita, sin costo."),
            ("¿Necesito tierra negra antes de poner pasto?", "En casas nuevas con suelo de relleno, sí. La tierra negra vegetal cuesta $90 el costal o $1,500 el m³."),
        ],
    ),
    "jardineria-ciudad-madero": dict(
        nombre="Ciudad Madero", municipio="Ciudad Madero", corto="Cd. Madero",
        title="Jardinería en Ciudad Madero y Playa Miramar: pasto, diseño y mantenimiento",
        h1="Jardinería en Ciudad Madero", accent="y Playa Miramar",
        colonias=[("Playa Miramar", "89506"), ("Jardín 20 de Noviembre", "89440"), ("Residencial del Parque", "89514"), ("Ampliación Unidad Nacional", "89510")],
        lede="Nuestro vivero está en Ciudad Madero. Instalamos pasto, diseñamos y damos mantenimiento en Playa Miramar, Jardín 20 de Noviembre y el resto de la ciudad.",
        retos=[
            ("Brisa y salitre cerca de la playa", "En Miramar el viento trae sal. Recomendamos plantas y palmas que la toleran, como coco plumoso, washingtonia y cubresuelos costeros."),
            ("Suelo arenoso", "La arena retiene poca agua y pocos nutrientes. Mejoramos el suelo con tierra negra y ajustamos el riego y la fertilización."),
            ("A minutos del vivero", "Estamos en Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, frente a Walmart. Puedes venir a escoger tus plantas."),
        ],
        img=("diseno-jardines-madero-altamira-pasto", 960, 640, None),
        faqs=[
            ("¿Dónde está el vivero de Viveros Terra en Madero?", "En Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, 89510 Cd. Madero, frente a Walmart. Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h."),
            ("¿Qué plantas aguantan la brisa de Playa Miramar?", "Coco plumoso, washingtonia, uva de mar y plantas de hoja gruesa toleran el salitre. Te decimos cuáles según qué tan cerca estés del mar."),
            ("¿Cuánto cuesta el pasto en rollo en Madero?", "El pasto San Agustín cuesta $85/m² solo el pasto y desde $120/m² instalado, con garantía de arraigo de 15 a 20 días."),
        ],
    ),
    "jardineria-altamira": dict(
        nombre="Altamira", municipio="Altamira", corto="Altamira",
        title="Jardinería en Altamira y Lagunas de Miralta: pasto, diseño y mantenimiento",
        h1="Jardinería en Altamira", accent="y Lagunas de Miralta",
        colonias=[("Residencial Lagunas de Miralta", "89605"), ("Altamira Centro", "89600")],
        lede="Pasto en rollo, diseño, riego y mantenimiento para Residencial Lagunas de Miralta y el resto de Altamira, sin cargo extra por traslado.",
        retos=[
            ("Jardines de fraccionamiento", "En fraccionamientos cerrados coordinamos horarios y acceso con la administración para instalar y dar mantenimiento."),
            ("Áreas verdes amplias", "Para jardines grandes, el riego automático por zonas y un plan de mantenimiento mensual mantienen el pasto parejo."),
            ("Casas nuevas", "Si tu casa es nueva, preparamos el suelo con tierra negra antes de instalar el pasto para que arraigue en 15 a 20 días."),
        ],
        img=("jardineria-areas-verdes-tampico", 793, 1190, "center 45%"),
        faqs=[
            ("¿Dan servicio de jardinería en Lagunas de Miralta?", "Sí. Atendemos Residencial Lagunas de Miralta y el resto de Altamira con pasto, diseño, riego y mantenimiento, sin cargo extra por traslado."),
            ("¿Cuánto cuesta el mantenimiento de jardín en Altamira?", "Desde $750 al mes. El precio depende de los metros y de la frecuencia de visitas."),
            ("¿Atienden empresas en el puerto industrial de Altamira?", 'Sí. Tenemos REPSE 773725 y factura CFDI 4.0 para contratos de mantenimiento de áreas verdes. Ve el <a href="/mantenimiento-jardines-tampico">servicio de mantenimiento</a>.'),
        ],
    ),
}


def guided(nombre):
    return "\n".join([f"Hola, quiero cotizar jardinería en {nombre}.", "Colonia: ", "Servicio que necesito: ", "Metros aprox.: ", "Les mando foto del espacio."])


def hero_html(z):
    img, w, h, pos = z["img"]
    style = f' style="object-position:{pos}"' if pos else ""
    cps = " · ".join(sorted({cp for _c, cp in z["colonias"]}))
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>{esc(z["municipio"])}, Tamaulipas</span><span class="stock">CP {esc(cps)}</span></p>
        <h1 class="hub-hero__title" id="titulo">{esc(z["h1"])} <em>{esc(z["accent"])}</em></h1>
        <p class="summary summary--hero">{esc(z["lede"])} Pasto San Agustín instalado desde <strong>$120/m²</strong> y mantenimiento desde <strong>$750/mes</strong>.</p>
        <dl class="specstrip">
          <div><dt>Pasto instalado</dt><dd class="num"><small>desde</small> $120<small>/m²</small></dd></div>
          <div><dt>Mantenimiento</dt><dd class="num"><small>desde</small> $750<small>/mes</small></dd></div>
          <div><dt>Visita y medición</dt><dd class="num">Sin costo</dd></div>
          <div><dt>Vivero propio</dt><dd class="num"><small>desde</small> 2007</dd></div>
        </dl>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="{wa(guided(z["corto"]))}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg>Cotizar por WhatsApp</a>
          <a class="btn btn--ghost" href="tel:+528333268008">Llamar 833 326 8008</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="/img/portadas/{img}-sm.webp" srcset="/img/portadas/{img}-sm.webp 560w, /img/portadas/{img}.webp {w}w" sizes="(min-width: 1024px) 560px, 100vw" width="{w}" height="{h}" alt="Jardín con pasto San Agustín atendido por Viveros Terra"{style} fetchpriority="high" decoding="async">
        <figcaption>Jardín atendido por Viveros Terra en la zona de Tampico.</figcaption>
      </figure>
    </div>
  </section>"""


def colonias_html(z):
    rows = "\n".join(
        f'            <tr><th scope="row">{esc(c)}<span>{esc(z["municipio"])}</span></th><td><strong>{cp}</strong></td></tr>'
        for c, cp in z["colonias"]
    )
    return f"""<p class="section__intro">Llegamos sin cargo extra por traslado. Si tu colonia está cerca y no aparece, también te atendemos.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Colonias atendidas">
          <table class="compare-table compare-table--prices num">
            <thead><tr><th scope="col">Colonia</th><th scope="col">Código postal</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>"""


def retos_html(z):
    items = "\n".join(f"          <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in z["retos"])
    return f'<ol class="steps">\n{items}\n        </ol>'


def precios_html():
    rows = "\n".join(
        f'            <tr><th scope="row"><a href="{href}">{esc(n)}</a><span>{esc(d)}</span></th><td><strong>{esc(p)}</strong></td></tr>'
        for n, href, p, d in PRECIOS
    )
    return f"""<div class="table-scroll" tabindex="0" role="region" aria-label="Precios de jardinería">
          <table class="compare-table compare-table--prices num">
            <thead><tr><th scope="col">Servicio</th><th scope="col">Precio con IVA</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="spec-note">Precios 2026 con IVA. <a href="/precios">Ver la lista completa</a>.</p>"""


def build_zona(slug, z):
    url = f"{SITE}/{slug}"
    faqs = [(q, a.replace('<a href="/mantenimiento-jardines-tampico">', "").replace("</a>", ""), a) for q, a in z["faqs"]]
    service = {
        "@type": "Service", "@id": f"{url}#servicio", "name": f"Jardinería en {z['nombre']}",
        "serviceType": "Jardinería, pasto en rollo, diseño y mantenimiento de jardines", "provider": {"@id": BUSINESS_ID},
        "areaServed": [{"@type": "Place", "name": f"{c}, {z['municipio']}, Tamaulipas",
                        "address": {"@type": "PostalAddress", "addressLocality": z["municipio"], "postalCode": cp,
                                    "addressRegion": "Tamaulipas", "addressCountry": "MX"}} for c, cp in z["colonias"]],
        "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": "120", "unitText": "m²"},
    }
    ld = jsonld([breadcrumb_schema([("Inicio", SITE), (f"Jardinería en {z['nombre']}", url)]), service, faq_schema(faqs)])
    img = z["img"][0]
    base = head(title=f"{z['title']} · Viveros Terra",
                description=f"{z['lede']} Pasto instalado desde $120/m², mantenimiento desde $750/mes. Visita sin costo.",
                canonical=url, og_image=f"{SITE}/img/portadas/{img}.webp", og_type="website",
                preload_img=f"/img/portadas/{img}-sm.webp", preload_srcset=f"/img/portadas/{img}-sm.webp 560w, /img/portadas/{img}.webp {z['img'][1]}w", ld=ld)
    base = base.split('<script src="/js/tienda-pasto.js')[0] + base.split("defer></script>", 1)[1]
    base = base.split('<header class="site-header">')[0].replace(
        '<a class="skip-link" href="#comprar">Ir al cotizador</a>', '<a class="skip-link" href="#colonias">Ir al contenido</a>')
    base += HEADER.format(wa=wa(guided(z["corto"])))
    return "".join([base, f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li aria-current="page">Jardinería en {esc(z["nombre"])}</li>
      </ol>
    </nav>
  </div>
  {hero_html(z)}

  {section_open(1, "Colonias", "colonias-titulo", f"Colonias que atendemos <em>en {esc(z['corto'])}</em>", section_id="colonias")}
        {colonias_html(z)}{SECTION_CLOSE}
  {section_open(2, "Tu jardín", "retos-titulo", "Lo que pide un jardín <em>en esta zona</em>", tint=True, section_id="zona")}
        {retos_html(z)}{SECTION_CLOSE}
  {section_open(3, "Precios", "precios-titulo", "Servicios y precios <em>con IVA</em>", section_id="precios")}
        {precios_html()}{SECTION_CLOSE}
  {section_open(4, "Preguntas", "faq-titulo", f"Preguntas frecuentes <em>en {esc(z['corto'])}</em>", tint=True, section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="cierre">
    <div class="wrap">
      <h2 id="cierre">Cotiza tu jardín <em>en {esc(z["corto"])}</em></h2>
      <p>Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. Te respondemos hoy y, si hace falta, vamos a medir sin costo.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="{wa(guided(z["corto"]))}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        <a class="btn btn--ghost" href="/vivero-tampico">Visitar el vivero</a>
      </div>
    </div>
  </section>
</main>
""", footer(), "</body>\n</html>\n"])
