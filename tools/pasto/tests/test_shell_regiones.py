import unittest

from precios import build_precios
from zonas import ZONAS, build_zona


def paginas():
    slug, zona = next(iter(ZONAS.items()))
    return {"precios": build_precios(), "zona": build_zona(slug, zona)}


class RegionesDelShellTest(unittest.TestCase):
    def test_cada_pagina_trae_una_region_de_cada_tipo(self):
        for nombre, html in paginas().items():
            for region in ("head", "header", "footer"):
                with self.subTest(pagina=nombre, region=region):
                    self.assertEqual(html.count(f"<!-- vt:{region} -->"), 1)
                    self.assertEqual(html.count(f"<!-- /vt:{region} -->"), 1)

    def test_main_con_id_y_sin_shell_propio(self):
        for nombre, html in paginas().items():
            with self.subTest(pagina=nombre):
                self.assertEqual(html.count('<main id="main">'), 1)
                for viejo in ('class="site-footer"', "googletagmanager", 'class="skip-link"', '<header class="site-header">',
                              "site-header--sub"):
                    self.assertNotIn(viejo, html)


if __name__ == "__main__":
    unittest.main()
