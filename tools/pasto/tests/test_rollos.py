import json
import unittest
from pathlib import Path

from rollos import ROLLO_ANCHO_M, ROLLO_LARGO_M, corte, tabla_medidas

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-rollos.json")
                   .read_text(encoding="utf-8"))


class CorteTest(unittest.TestCase):
    def test_casos_compartidos_con_el_js(self):
        """Mismos casos que public/js/tests/vt-rollos.test.js (casos-rollos.json)."""
        for largo, ancho, tiras, largo_tira, m2_tiras, m2, rollos, m2_sin, rollos_sin in CASOS["casos"]:
            with self.subTest(largo=largo, ancho=ancho):
                r = corte(largo, ancho)
                self.assertEqual((r["tiras"], r["largo_tira"], r["m2_tiras"], r["m2"], r["rollos"], r["m2_sin_margen"],
                                  r["rollos_sin_margen"]), (tiras, largo_tira, m2_tiras, m2, rollos, m2_sin, rollos_sin))

    def test_medidas_invalidas_devuelven_none(self):
        for largo, ancho in CASOS["invalidos"]:
            with self.subTest(largo=largo, ancho=ancho):
                self.assertIsNone(corte(largo, ancho))

    def test_ejemplo_de_la_guia_de_instalacion(self):
        """La guía /blog/como-instalar-pasto-sintetico: 5 × 4 m = 20 m² → pide 22 m²."""
        self.assertEqual(corte(5, 4)["m2"], 22)

    def test_las_tiras_cubren_el_espacio(self):
        for largo, ancho, *_ in CASOS["casos"]:
            r = corte(largo, ancho)
            cruzado = r["cruzado"]
            self.assertGreaterEqual(r["tiras"] * ROLLO_ANCHO_M, cruzado)
            self.assertLess((r["tiras"] - 1) * ROLLO_ANCHO_M, cruzado)
            self.assertGreaterEqual(r["m2"], r["area"])

    def test_sobrante_y_uniones(self):
        r = corte(7, 5)
        self.assertEqual((r["area"], r["sobrante"], r["uniones"]), (35, 5, 3))
        self.assertFalse(r["tira_con_union"])
        self.assertTrue(corte(30, 2)["tira_con_union"])
        self.assertEqual(ROLLO_LARGO_M, 25)


class TablaMedidasTest(unittest.TestCase):
    def test_medidas_comunes(self):
        filas = tabla_medidas()
        self.assertEqual([(f["largo"], f["ancho"]) for f in filas][:2], [(3, 3), (5, 4)])
        self.assertTrue(all(f["m2"] >= f["area"] for f in filas))


if __name__ == "__main__":
    unittest.main()
