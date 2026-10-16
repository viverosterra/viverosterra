import unittest

from common import buybar
from data import MODELOS
from ficha import build_ficha
from hub import build_hub
from local import build_local
from perros import build_perros


class BuybarTest(unittest.TestCase):
    def test_sin_rollo_no_cambia(self):
        self.assertNotIn("data-landed-bar", buybar("X", "Desde $1/m²"))

    def test_paginas_nacionales_llevan_precio_puesto(self):
        self.assertIn('data-landed-bar data-rollo="139"', build_hub())
        self.assertIn('data-landed-bar data-rollo="149"', build_perros())
        m = next(x for x in MODELOS if x["slug"] == "toscana-28")
        self.assertIn(f'data-landed-bar data-rollo="{m["rollo"]}"', build_ficha(m))

    def test_tampico_no_cambia(self):
        self.assertNotIn("data-landed-bar", build_local())
