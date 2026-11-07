import unittest

from pathlib import Path

from common import SUBNAV, estado_select_html, height_rule_html, trust_band_html
from data import ESTADOS_ORDEN


class CommonTest(unittest.TestCase):
    def test_selector_tiene_todos_los_estados_y_label(self):
        html = estado_select_html("hero-estado")
        self.assertIn('<label for="hero-estado"', html)
        for e in ESTADOS_ORDEN:
            self.assertIn(f'value="{e}"', html)

    def test_selector_preselecciona(self):
        self.assertIn('value="Nuevo León" selected', estado_select_html("x", selected="Nuevo León"))

    def test_boton_de_la_lista_distinto_del_cotizar_del_menu(self):
        # El menú del shell ya tiene "Cotizar" (WhatsApp); el carrito de la tienda se llama "Mi lista".
        self.assertIn("<span>Mi lista</span>", SUBNAV)
        self.assertNotIn("Cotización<", SUBNAV)

    def test_barra_de_la_tienda_no_se_pega_en_celular(self):
        css = (Path(__file__).resolve().parents[3] / "public" / "css" / "tienda-pasto.css").read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 767px) { .site-header--sub { position: static; } }", css)

    def test_regla_escala(self):
        html = height_rule_html(35)
        self.assertIn('style="--w:100%"', html)
        self.assertIn('aria-label="Altura de fibra: 35 mm"', html)
        self.assertIn('style="--w:29%"', height_rule_html(10))
        self.assertIn('aria-label="Altura de fibra: 10 mm"', height_rule_html(10))

    def test_franja_confianza(self):
        html = trust_band_html()
        self.assertIn("menos de 1 hora", html)
        self.assertIn("/politicas#devoluciones", html)
        self.assertNotIn("muestra", html.lower())
