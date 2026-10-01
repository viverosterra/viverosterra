import unittest

from common import estado_select_html, height_rule_html, trust_band_html
from data import ESTADOS_ORDEN


class CommonTest(unittest.TestCase):
    def test_selector_tiene_todos_los_estados_y_label(self):
        html = estado_select_html("hero-estado")
        self.assertIn('<label for="hero-estado"', html)
        for e in ESTADOS_ORDEN:
            self.assertIn(f'value="{e}"', html)

    def test_selector_preselecciona(self):
        self.assertIn('value="Nuevo León" selected', estado_select_html("x", selected="Nuevo León"))

    def test_regla_escala(self):
        html = height_rule_html(35)
        self.assertIn('style="--h:100%"', html)
        self.assertIn('aria-label="Altura de fibra: 35 mm"', html)
        self.assertIn('style="--h:29%"', height_rule_html(10))

    def test_franja_confianza(self):
        html = trust_band_html()
        self.assertIn("menos de 1 hora", html)
        self.assertIn("/politicas#devoluciones", html)
        self.assertNotIn("muestra", html.lower())
