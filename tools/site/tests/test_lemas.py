"""Regla permanente (lemas, 2026-11-10): el lema en serif que va debajo del título (.vt-portada__lema) es corto, no
repite el título y no usa palabras que el dueño prohibió. Los lemas vigentes los eligió el dueño de
docs/ux/2026-11/lemas-opciones.md (versión 2): 1A, 2A, 3C, 4C, 5B, 6C, 7C, 8A, 9A, 10B (2026-11-10) y
11B, 12B, 13C, 14B, 15B, 16A, 17A, 18A, 19A, 20A, 21A, 22A (2026-11-11)."""
import re
import unicodedata
import unittest
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3] / "public"
LEMA_MAX = 48
PROHIBIDAS = ("gratis", "más vendido", "oasis", "paraíso", "mágico", "increíble", "espectacular", "sueño", "visión")
ELEGIDOS = {
    "index.html": "Todo para tu jardín, en un solo lugar.",
    "plantas-palmas-arboles-tampico/index.html": "Más de 200 plantas que sí se dan en Tampico.",
    "palmas-tropicales-tampico/index.html": "Para darle a tu casa un aire de playa.",
    "plantas-para-jardin-tampico/index.html": "Las que se dan bien cerca del mar.",
    "plantas-de-interior-tampico/index.html": "Para alegrar tu sala, tu cocina o tu oficina.",
    "arboles-ornamentales-tampico/index.html": "Árboles de sombra y de flor para tu casa.",
    "arboles-para-banqueta-tampico/index.html": "Te decimos cuál plantar frente a tu casa.",
    "catalogo.html": "Escoge, agrega y cotiza por WhatsApp.",
    "post/nochebuenas-tampico-madero-mayoreo/index.html": "Para tu casa, tu negocio o tu posada.",
    "pasto-sintetico/toscana-18/index.html": "Buen pasto sin gastar de más.",
    "pasto-sintetico/aruba-10/index.html": "Para adornar terrazas y balcones.",
    "pasto-sintetico/capri-20/index.html": "Alta densidad, se ve tupido.",
    "pasto-sintetico/irlanda-25/index.html": "Para patios que se usan mucho.",
    "pasto-sintetico/toscana-28/index.html": "Para jugar en el patio todos los días.",
    "pasto-sintetico/viena-30/index.html": "Se ve natural, de calidad premium.",
    "pasto-sintetico/japones-35/index.html": "El que más parece pasto de verdad.",
    "pasto-sintetico/monaco-35/index.html": "Un verde vivo que se nota.",
    "pasto-sintetico/bali-35/index.html": "El más completo de la tienda.",
    "pasto-en-rollo-tampico/index.html": "Recién cortado, del campo a tu jardín.",
}
TITULOS = {  # grupo 2: el lema va dentro del H1
    "precios/index.html": "Precios de jardinería en Tampico y Ciudad Madero",
    "cuestionario.html": "Tu jardín empieza aquí. Cuéntanos qué te gustaría.",
    "pasto-en-rollo-tampico/index.html": "Pasto San Agustín en rollo, instalado en un día.",
}
LEMA_BLOG = "Lo que nos preguntan en el vivero, contestado."
_LEMA = re.compile(r'<p class="vt-portada__lema[^"]*">(.*?)</p>', re.S)
_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)


def _texto(fragmento):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragmento)).strip()


def _normal(texto):
    sin_acentos = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn").strip(" .")


def _lemas():
    for ruta in sorted(PUBLIC.rglob("*.html")):
        html = ruta.read_text(encoding="utf-8")
        lema = _LEMA.search(html)
        if lema:
            h1 = _H1.search(html)
            yield ruta.relative_to(PUBLIC).as_posix(), _texto(lema.group(1)), _texto(h1.group(1)) if h1 else ""


class LemasTest(unittest.TestCase):
    def test_hay_lemas(self):
        self.assertGreater(len(list(_lemas())), 20)

    def test_lema_corto_sin_repetir_titulo_ni_palabras_prohibidas(self):
        for ruta, lema, h1 in _lemas():
            with self.subTest(ruta=ruta):
                self.assertLessEqual(len(lema), LEMA_MAX, lema)
                self.assertNotIn(_normal(lema), _normal(h1))
                for palabra in PROHIBIDAS:
                    self.assertNotIn(palabra, lema.lower())

    def test_lemas_elegidos_por_el_dueno(self):
        vistos = {ruta: lema for ruta, lema, _ in _lemas()}
        for ruta, esperado in ELEGIDOS.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(vistos.get(ruta), esperado)

    def test_titulos_elegidos_por_el_dueno(self):
        for ruta, esperado in TITULOS.items():
            with self.subTest(ruta=ruta):
                html = (PUBLIC / ruta).read_text(encoding="utf-8")
                self.assertEqual(_texto(_H1.search(html).group(1)), esperado)
                self.assertNotIn("visión", html.lower() if ruta == "cuestionario.html" else "")

    def test_blog_usa_el_lema_elegido(self):
        articulos = [lema for ruta, lema, _ in _lemas() if ruta.startswith("blog/") and ruta != "blog/index.html"]
        self.assertGreater(len(articulos), 40)
        for lema in articulos:
            self.assertEqual(lema, LEMA_BLOG)


if __name__ == "__main__":
    unittest.main()
