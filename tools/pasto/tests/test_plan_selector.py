# tools/pasto/tests/test_plan_selector.py
import unittest

from common import plan_selector_html
from data import MODELOS
from ficha import build_ficha
from hub import build_hub
from precios import build_precios
from zonas import ZONAS, build_zona

PROHIBIDAS = ("msi", "sin intereses", "0%", "recargo", "comisión")


class PlanSelectorTest(unittest.TestCase):
    def test_estructura(self):
        html = plan_selector_html("q")
        self.assertIn('role="radiogroup"', html)
        for v in ("0", "3", "6", "9", "12"):
            self.assertIn(f'name="q-plan" value="{v}"', html)
        self.assertIn('value="0" checked', html)
        self.assertIn('id="q-plan-trip"', html)
        self.assertIn('<dt>Contado</dt><dd data-trip-contado>', html)
        self.assertNotIn('data-trip-hoy', html)
        self.assertIn('id="q-plan-rule"', html)
        self.assertIn('/politicas#mensualidades', html)

    def test_sin_palabras_prohibidas(self):
        html = plan_selector_html("q").lower()
        for p in PROHIBIDAS:
            self.assertNotIn(p, html)

    def test_en_hub_y_fichas_con_script(self):
        self.assertIn('name="q-plan"', build_hub())
        f = build_ficha(MODELOS[0])
        self.assertIn('name="q-plan"', f)
        self.assertIn('src="/js/vt-mensualidades.js', f)

    def test_paginas_sin_cotizador_no_cargan_scripts_de_tienda(self):
        slug, zona = next(iter(ZONAS.items()))
        for html in (build_precios(), build_zona(slug, zona)):
            self.assertNotIn("tienda-pasto.js", html)
            self.assertNotIn("vt-mensualidades.js", html)
            self.assertIn("</head>", html)
