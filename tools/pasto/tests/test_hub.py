import unittest

from hub import build_hub


class HubTest(unittest.TestCase):
    def setUp(self):
        self.html = build_hub()

    def test_selector_de_portada(self):
        self.assertIn('id="hero-estado"', self.html)
        self.assertIn('data-landed-hero', self.html)

    def test_existencia_nacional(self):
        self.assertIn("9 modelos en existencia", self.html)
        self.assertNotIn("3 modelos en existencia", self.html)

    def test_reglas_y_precios_puestos(self):
        self.assertEqual(self.html.count('class="hrule"'), 9)
        self.assertEqual(self.html.count("data-landed-slug="), 9)

    def test_ciudades_y_comparador(self):
        self.assertIn('/pasto-sintetico/envio/monterrey', self.html)
        self.assertIn('id="comparador"', self.html)
        self.assertIn('/pasto-sintetico/perros', self.html)
        self.assertIn('src="/js/vt-landed.js', self.html)
