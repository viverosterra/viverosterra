"""Simulador de mensualidades con tarjeta en las páginas de servicios locales.

Inserta (o reemplaza) el bloque entre <!-- simulador --> y <!-- /simulador --> justo antes de la sección de
preguntas frecuentes (o antes de <footer si no hay) y asegura los dos scripts antes de </body>, una sola vez.
Idempotente: correrlo dos veces deja exactamente un simulador y un script de cada uno.

Uso: python3 tools/servicios/simulador.py   (desde cualquier carpeta)
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "public"
# /pasto-en-rollo-tampico trae su simulador desde tools/site/plantillas/servicio.py (Etapa 2a).
PAGES = (
    ("sistema-riego-tampico", "un sistema de riego", 18000),
    ("diseno-jardines-tampico", "el diseño de mi jardín", 6500),
)
SCRIPTS = (
    '<script src="/js/vt-mensualidades.js?v=20261104" defer></script>',
    '<script src="/js/vt-simulador.js?v=20261104" defer></script>',
)
BLOCK_RE = re.compile(r"<!-- simulador -->.*?<!-- /simulador -->\n?", re.S)
SECTION_RE = re.compile(r"<section\b.*?</section>", re.S)
LEAD_COMMENT_RE = re.compile(r"<!--(?:(?!-->).)*-->[ \t]*\n?\Z", re.S)


def block_html(servicio, monto):
    return f"""<!-- simulador -->
<section class="sim" data-simulador data-servicio="{escape(servicio)}" aria-labelledby="sim-titulo">
  <div class="sim__wrap">
    <p class="sim__eyebrow">Formas de pago</p>
    <h2 id="sim-titulo">Calcula tus mensualidades con tarjeta</h2>
    <p class="sim__lede">Escribe el monto de tu cotización y compara contado contra 3, 6, 9 o 12 mensualidades con tarjeta de crédito. Contado (transferencia, efectivo o tarjeta en una exhibición) es el precio más bajo.</p>
    <label class="sim__field">Monto de tu cotización <input type="number" inputmode="numeric" min="0" step="100" value="{int(monto)}" data-sim-monto></label>
    <div class="sim__list" role="radiogroup" aria-label="Forma de pago" data-sim-list></div>
    <p class="sim__note">Montos aproximados: tu banco debe aceptar el plan. Disponible en cotizaciones desde $2,000. <a href="/politicas#mensualidades">Condiciones</a></p>
    <a class="sim__cta" data-sim-wa href="https://wa.me/528333268008" target="_blank" rel="noopener">Enviar por WhatsApp</a>
  </div>
</section>
<!-- /simulador -->
"""


def insert_point(html):
    for m in SECTION_RE.finditer(html):
        if "Preguntas frecuentes" in m.group(0):
            # si la sección va precedida de un comentario (<!-- FAQ -->), el simulador va antes del comentario
            head = html[:m.start()]
            lead = LEAD_COMMENT_RE.search(head[-200:])
            return m.start() - len(head[-200:]) + lead.start() if lead else m.start()
    idx = html.find("<footer")
    if idx < 0:
        raise ValueError("no encontré la sección de preguntas frecuentes ni <footer")
    return idx


def ensure_scripts(html):
    for tag in SCRIPTS:
        src = re.search(r'src="([^"?]+)', tag).group(1)
        html = re.sub(rf'<script src="{re.escape(src)}(?:\?[^"]*)?"[^>]*></script>\n?', "", html)
    if "</body>" not in html:
        raise ValueError("no encontré </body>")
    return html.replace("</body>", "\n".join(SCRIPTS) + "\n</body>", 1)


def apply_html(html, servicio, monto):
    block = block_html(servicio, monto)
    if BLOCK_RE.search(html):
        html = BLOCK_RE.sub(lambda _m: block, html, count=1)
    else:
        idx = insert_point(html)
        html = html[:idx] + block + html[idx:]
    return ensure_scripts(html)


def main():
    for slug, servicio, monto in PAGES:
        path = ROOT / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        path.write_text(apply_html(html, servicio, monto), encoding="utf-8")
        print(f"ok {slug}")


if __name__ == "__main__":
    main()
