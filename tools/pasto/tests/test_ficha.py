import unittest

from data import MODELOS
from ficha import build_ficha


class FichaTest(unittest.TestCase):
    def test_todas_en_existencia_y_con_precio_puesto(self):
        for m in MODELOS:
            html = build_ficha(m)
            self.assertIn('<span class="stock">En existencia</span>', html, m["slug"])
            self.assertIn(f'data-landed-slug="{m["slug"]}"', html, m["slug"])
            self.assertIn('src="/js/vt-landed.js', html, m["slug"])
