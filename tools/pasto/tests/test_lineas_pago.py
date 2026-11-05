import unittest

from ciudad import build_ciudad
from ciudades import CIUDADES
from hub import build_hub


class LineasPagoTest(unittest.TestCase):
    def test_hub(self):
        html = build_hub()
        self.assertEqual(html.count('class="spec-card__pay"'), 9)
        self.assertIn("Paga en mensualidades con tarjeta de crédito", html)

    def test_ciudad_columna(self):
        html = build_ciudad(next(c for c in CIUDADES if c["slug"] == "monterrey"))
        self.assertIn("En mensualidades", html)
        self.assertIn("#cotizador\">cotizador</a>", html)
        self.assertNotIn("sin intereses", html.lower())
