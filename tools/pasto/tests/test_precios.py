import unittest

from mensualidades import total_a_plazos
from precios import build_precios, porcentaje_plazo


class PreciosMensualidadesTest(unittest.TestCase):
    def setUp(self):
        self.html = build_precios()

    def test_porcentajes_desde_la_formula(self):
        esperado = {3: 10.5, 6: 14.9, 9: 20.5, 12: 23.4}
        for plazo, pct in esperado.items():
            self.assertEqual(porcentaje_plazo(plazo), pct)
            self.assertEqual(round((total_a_plazos(100000, plazo) / 100000 - 1) * 100, 1), pct)

    def test_seccion_mensualidades_con_numeros(self):
        self.assertIn('id="mensualidades"', self.html)
        self.assertIn("Mensualidades <em>con tarjeta</em>", self.html)
        for fila in ('<th scope="row">3 mensualidades</th><td>$2,000</td><td><strong>+10.5%</strong></td>',
                     '<th scope="row">6 mensualidades</th><td>$5,000</td><td><strong>+14.9%</strong></td>',
                     '<th scope="row">9 mensualidades</th><td>$15,000</td><td><strong>+20.5%</strong></td>',
                     '<th scope="row">12 mensualidades</th><td>$15,000</td><td><strong>+23.4%</strong></td>'):
            self.assertIn(fila, self.html)
        self.assertIn('href="/politicas#mensualidades"', self.html)
        self.assertIn("No aplica a mantenimiento mensual", self.html)

    def test_sin_palabras_prohibidas(self):
        bajo = self.html.lower()
        for palabra in ("clip", "msi", "sin intereses", "recargo", "comisión", "comision", "oasis", "pastoplus"):
            self.assertNotIn(palabra, bajo.replace("clip-path", ""), palabra)


if __name__ == "__main__":
    unittest.main()
