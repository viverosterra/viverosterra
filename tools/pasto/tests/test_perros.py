import json
import re
import unittest

from perros import FAQS, RECOMENDADOS, build_perros
from data import MODELOS


class PerrosTest(unittest.TestCase):
    def test_recomendados_existen(self):
        slugs = {m["slug"] for m in MODELOS}
        self.assertEqual(len(RECOMENDADOS), 3)
        for slug, _r in RECOMENDADOS:
            self.assertIn(slug, slugs)

    def test_preguntas_clave(self):
        preguntas = " ".join(q for q, _a in FAQS).lower()
        for palabra in ("calienta", "rasguñ", "huele", "lava"):
            self.assertIn(palabra, preguntas)

    def test_html_y_schema(self):
        html = build_perros()
        self.assertIn('rel="canonical" href="https://www.viverosterra.com/pasto-sintetico/perros"', html)
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(bloque)
        self.assertNotIn("muestra", html.lower())

    def test_precio_desde_correcto(self):
        html = build_perros()
        resumen = re.search(r'<p class="summary summary--hero">(.*?)</p>', html, re.S).group(1)
        self.assertIn("$149/m²", resumen)
        self.assertIn("Toscana 18", resumen)
        self.assertNotIn("$139", html)

    def test_enlaces_y_sin_absolutos(self):
        html = build_perros()
        self.assertIn('href="/blog/como-instalar-pasto-sintetico"', html)
        self.assertIn('href="/blog/pasto-sintetico-para-perros"', html)
        self.assertNotIn("no se queda el olor", html)
        self.assertNotIn("se recupera", html)
