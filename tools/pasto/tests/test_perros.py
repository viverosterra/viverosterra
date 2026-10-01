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
