import unittest

from mensualidades import PLAZOS, planes, plazos_disponibles


class MensualidadesTest(unittest.TestCase):
    def test_totales_igual_a_calculadora_clip(self):
        p = {x["plazo"]: x for x in planes(11100)}
        self.assertEqual(p[3]["total"], 12263)
        self.assertEqual(p[6]["total"], 12753)
        self.assertEqual(p[9]["total"], 13377)
        self.assertEqual(p[12]["total"], 13702)
        self.assertEqual(p[6]["diferencia"], 12753 - 11100)
        self.assertEqual(p[12]["mensualidad"], 1142)

    def test_umbrales(self):
        self.assertEqual(plazos_disponibles(1999), [])
        self.assertEqual(plazos_disponibles(2000), [3])
        self.assertEqual(plazos_disponibles(4999), [3])
        self.assertEqual(plazos_disponibles(5000), [3, 6])
        self.assertEqual(plazos_disponibles(14999), [3, 6])
        self.assertEqual(plazos_disponibles(15000), [3, 6, 9, 12])

    def test_planes_marca_disponibles(self):
        disp = {x["plazo"]: x["disponible"] for x in planes(6000)}
        self.assertEqual(disp, {3: True, 6: True, 9: False, 12: False})
        self.assertEqual([x["plazo"] for x in planes(6000)], list(PLAZOS))

    def test_total_redondea_hacia_arriba(self):
        for x in planes(2500):
            self.assertIsInstance(x["total"], int)
            self.assertGreaterEqual(x["total"] * (1 - (0.036 + {3: .0457, 6: .0757, 9: .1107, 12: .1277}[x["plazo"]]) * 1.16), 2500 - 0.5)
