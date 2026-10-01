import unittest

from data import MODELOS, ZONAS, ZONA_ESTADOS, estado_slug, landed_m2, zona_de


class LandedTest(unittest.TestCase):
    def aruba(self):
        return next(m for m in MODELOS if m["slug"] == "aruba-10")

    def test_landed_por_zona(self):
        self.assertEqual(landed_m2(self.aruba(), "A"), 157)
        self.assertEqual(landed_m2(self.aruba(), "B"), 162)
        self.assertEqual(landed_m2(self.aruba(), "C"), 167)

    def test_zona_de_estado(self):
        self.assertEqual(zona_de("Nuevo León"), "B")
        self.assertEqual(zona_de("CDMX"), "A")
        self.assertIsNone(zona_de("Narnia"))

    def test_estado_slug(self):
        self.assertEqual(estado_slug("Nuevo León"), "nuevo-leon")
        self.assertEqual(estado_slug("Estado de México"), "estado-de-mexico")
        self.assertEqual(estado_slug("CDMX"), "cdmx")

    def test_todas_las_zonas_tienen_tarifa(self):
        self.assertEqual(set(ZONA_ESTADOS), set(ZONAS))


if __name__ == "__main__":
    unittest.main()
