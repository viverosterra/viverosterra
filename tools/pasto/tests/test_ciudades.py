# tools/pasto/tests/test_ciudades.py
import unittest

from ciudades import CIUDADES
from data import MODELOS, zona_de

SLUGS = {m["slug"] for m in MODELOS}


class CiudadesTest(unittest.TestCase):
    def test_once_ciudades(self):
        self.assertEqual(len(CIUDADES), 11)

    def test_estado_valido_y_zona_esperada(self):
        esperado = {"cdmx": "A", "guadalajara": "A", "queretaro": "A", "san-luis-potosi": "A", "leon": "A",
                    "puebla": "A", "monterrey": "B", "veracruz": "B", "merida": "C", "cancun": "C", "villahermosa": "C"}
        for c in CIUDADES:
            self.assertEqual(zona_de(c["estado"]), esperado[c["slug"]], c["slug"])

    def test_modelos_existen(self):
        for c in CIUDADES:
            self.assertEqual(len(c["modelos"]), 3, c["slug"])
            for slug, razon in c["modelos"]:
                self.assertIn(slug, SLUGS)
                self.assertTrue(razon)

    def test_textos_no_se_repiten(self):
        climas = [c["clima"] for c in CIUDADES]
        self.assertEqual(len(climas), len(set(climas)))
        preguntas = [q for c in CIUDADES for q, _a in c["faqs"]]
        self.assertEqual(len(preguntas), len(set(preguntas)))

    def test_sin_palabras_prohibidas(self):
        texto = str(CIUDADES).lower()
        for palabra in ("oasis", "muestra", "gratis", "pádel", "padel"):
            self.assertNotIn(palabra, texto)
