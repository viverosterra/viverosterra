"""Página /pasto-sintetico/perros: pasto sintético para perros y mascotas.

Solo afirmaciones presentes en las fichas (COMMON_TREATMENTS incluye antibacterial). Sin prometer lo que no está documentado.
"""
from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, faq_html, faq_schema,
                    footer, head, height_rule_html, jsonld, section_open, trust_band_html, wa)
from data import COMMON_TREATMENTS, MODELOS, SITE

URL = f"{SITE}/pasto-sintetico/perros"
# Imagen de obra vertical real: 960x1280 (la versión -sm mide 560x747).
IMG = f"{GAL}/obra-proyecto-02"
IMG_W, IMG_H = 960, 1280

RECOMENDADOS = [
    ("irlanda-25", "Fibra más resistente de la colección: aguanta pisoteo y juego diario."),
    ("capri-20", "Alta densidad y fibra corta: fácil de limpiar y de levantar desechos."),
    ("toscana-18", "El más económico para patios chicos o para empezar."),
]

CRITERIOS = [
    ("Fibra resistente y no muy alta", "De 18 a 25 mm es lo más práctico: se limpia fácil y aguanta el paso diario."),
    ("Base perforada que drene", "La orina tiene que pasar al suelo. Instálalo sobre grava fina compactada, no sobre piso liso sin desnivel."),
    ("Limpieza sencilla", "Levanta los desechos sólidos y enjuaga con manguera. Para el olor, usa un limpiador enzimático para mascotas."),
]

FAQS = [
    ("¿El pasto sintético se calienta con el sol?", "Sí, como cualquier superficie exterior al sol. Enjuágalo con manguera en las horas de más calor y deja una zona de sombra para tu perro."),
    ("¿Mi perro lo puede rasguñar o romper?", "Un perro que escarba puede levantar las orillas si no están bien fijadas. Fija el perímetro con clavos o adhesivo como indica la guía de instalación."),
    ("¿El pasto sintético huele a orina?", "Si la base no drena o no se enjuaga, sí. Con grava que drene, enjuague frecuente y un limpiador enzimático se controla el olor."),
    ("¿Cómo se lava el pasto sintético con perros?", "Levanta los desechos, enjuaga con manguera una o dos veces por semana y cepilla la fibra de vez en cuando para que quede de pie."),
    ("¿Qué tratamientos tiene el pasto?", f"Todos nuestros modelos tienen de fábrica estos tratamientos: {COMMON_TREATMENTS}."),
]


def modelo(slug):
    return next(m for m in MODELOS if m["slug"] == slug)


MAS_BARATO = min((modelo(slug) for slug, _r in RECOMENDADOS), key=lambda m: m["rollo"])
DESDE = MAS_BARATO["rollo"]


def recomendados_html():
    cards = []
    for slug, razon in RECOMENDADOS:
        m = modelo(slug)
        cards.append(f"""          <article class="city-model">
            <div>
              <h3><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a></h3>
              {height_rule_html(m["mm"])}
              <p>{esc(razon)}</p>
              <p class="city-model__price num">Desde <strong>${m["rollo"]}</strong>/m² <span data-landed-slug="{m["slug"]}"></span></p>
            </div>
          </article>""")
    return '<div class="city-models">\n' + "\n".join(cards) + "\n        </div>"


def criterios_html():
    items = "\n".join(f"          <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in CRITERIOS)
    return f'<ol class="steps">\n{items}\n        </ol>'


GUIA_INSTALACION = "guía de instalación"


def a_html(texto):
    """Escapa la respuesta y enlaza la guía de instalación (el texto plano del schema no lleva HTML)."""
    return esc(texto).replace(
        GUIA_INSTALACION, f'<a href="/blog/como-instalar-pasto-sintetico">{GUIA_INSTALACION}</a>')


def build_perros():
    faqs = [(q, a, a_html(a)) for q, a in FAQS]
    ld = jsonld([breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), ("Para perros", URL)]),
                 faq_schema(faqs)])
    base = head(
        title="Pasto sintético para perros: qué modelo elegir y cómo limpiarlo | Viveros Terra",
        description=f"Pasto sintético para perros con envío a todo México: qué modelo elegir, cómo drena la orina, cómo quitar el olor y cómo limpiarlo. Desde ${DESDE}/m².",
        canonical=URL, og_image=f"{SITE}{IMG}.webp", og_type="article",
        preload_img=f"{IMG}-sm.webp", preload_srcset=f"{IMG}-sm.webp 560w, {IMG}.webp 960w", ld=ld,
    )
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#elegir">Ir al contenido</a>'), f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li><a href="/pasto-sintetico">Pasto sintético</a></li>
        <li aria-current="page">Para perros</li>
      </ol>
    </nav>
  </div>
  <section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Mascotas · Envío a todo México</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético para perros <em>que drena y se limpia fácil</em></h1>
        <p class="summary summary--hero">Para perros conviene un pasto de 18 a 25 mm con fibra resistente, instalado sobre grava que drene. Se limpia con manguera y un limpiador enzimático. Desde <strong>${DESDE}/m²</strong> con {esc(MAS_BARATO["nombre"])}.</p>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="/pasto-sintetico#modelos">Ver precios con envío</a>
          <a class="btn btn--ghost" href="{wa("Hola, quiero pasto sintético para mis perros. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="{IMG}-sm.webp" srcset="{IMG}-sm.webp 560w, {IMG}.webp 960w" sizes="(min-width: 1024px) 620px, 100vw" width="{IMG_W}" height="{IMG_H}" alt="Patio con pasto sintético de nuestra colección" fetchpriority="high" decoding="async">
        <figcaption>Pasto sintético de nuestra colección instalado.</figcaption>
      </figure>
    </div>
  </section>
  {trust_band_html()}

  {section_open(1, "Elegir", "elegir-titulo", "Qué pasto sintético <em>conviene para perros</em>", section_id="elegir")}
        {criterios_html()}{SECTION_CLOSE}
  {section_open(2, "Modelos", "modelos-titulo", "Tres modelos <em>para mascotas</em>", tint=True, section_id="modelos")}
        {recomendados_html()}{SECTION_CLOSE}
  {section_open(3, "Preguntas", "faq-titulo", "Preguntas frecuentes <em>con perros</em>", section_id="preguntas")}
        {faq_html(faqs)}
        <p><a href="/blog/pasto-sintetico-para-perros">Lee la guía completa: pasto sintético para perros</a></p>{SECTION_CLOSE}
</main>
""", footer(), buybar("Pasto para perros", f"Desde ${DESDE}/m²"), drawer_and_toast()])
