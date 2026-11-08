"""Protocolo de pasto: las tres etapas de riego y las condiciones de la garantía, con precios de datos.py."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
from componentes import dinero  # noqa: E402
from plantillas import protocolo  # noqa: E402

K = generar.cargar("protocolo").CONTENIDO


class ProtocoloTest(unittest.TestCase):
    def setUp(self):
        self.html = protocolo.render(K)

    def test_etapas_en_orden(self):
        posiciones = [self.html.index(d) for d in ("Días 1 – 7", "Días 8 – 14", "Días 15 – 20")]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_garantia_con_ancla_y_sus_cinco_condiciones(self):
        self.assertIn('id="garantia"', self.html)
        self.assertEqual(len(K["garantia"]["condiciones"]), 5)
        self.assertIn("El problema fue reportado antes del día 21", self.html)
        self.assertIn("la reponemos sin costo", self.html)

    def test_precios_de_datos(self):
        self.assertIn(f"{dinero(datos.PRECIOS['pasto_solo_m2'])}/m²", self.html)
        self.assertIn(f"{dinero(datos.PRECIOS['mantenimiento_mes'])}/mes", self.html)

    def test_un_h1_y_foto_precargada_de_main(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)
        self.assertIn('rel="preload" as="image" href="/img/instalacion-pasto-rollo-san-agustin-tampico.webp"', self.html)


if __name__ == "__main__":
    unittest.main()
