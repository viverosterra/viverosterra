# tools/pasto/tests/test_plan_selector.py
"""/precios y las zonas (las únicas páginas que aún genera tools/pasto) no cargan los scripts de la tienda. El selector
de forma de pago de la tienda se prueba en tools/site/tests/test_componentes_tienda.py."""
import unittest

from precios import build_precios
from zonas import ZONAS, build_zona


class SinScriptsDeTiendaTest(unittest.TestCase):
    def test_paginas_sin_cotizador_no_cargan_scripts_de_tienda(self):
        slug, zona = next(iter(ZONAS.items()))
        for html in (build_precios(), build_zona(slug, zona)):
            self.assertNotIn("tienda-pasto.js", html)
            self.assertNotIn("vt-mensualidades.js", html)
            self.assertIn("</head>", html)


if __name__ == "__main__":
    unittest.main()
