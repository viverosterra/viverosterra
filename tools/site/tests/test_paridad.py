"""Paridad de contenido de las páginas migradas contra su captura anterior (tools/site/tests/paridad/*.json)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402


class ParidadTest(unittest.TestCase):
    def test_cubierto_y_faltantes(self):
        self.assertTrue(paridad.cubierto("Primer riego", ["Primer riego Tú"]))
        self.assertTrue(paridad.cubierto("Pasto Sintético", ["pasto sintético."]))
        self.assertFalse(paridad.cubierto("Riego", ["Riegos"]))
        mapa = {"reemplazos": {"A": "B"}, "retirados": {"C": "motivo largo y claro"}}
        self.assertEqual(paridad.faltantes(["A", "C", "D"], ["B"], mapa), ["D"])
        self.assertEqual(paridad.faltantes(["A"], [], mapa), ["A → B (el reemplazo no está en la página)"])

    def test_extraer(self):
        html = ('<title>T</title><meta name="description" content="D"><main><h2>¿Cuánto?</h2><p>$1,500 y $ 85</p>'
                '<details><summary>¿Pregunta?</summary></details><a href="/x/#a">x</a><a href="//cdn">y</a></main>')
        e = paridad.extraer(html)
        self.assertEqual((e["meta"]["title"], e["meta"]["description"]), ("T", "D"))
        self.assertEqual(e["encabezados"], ["¿Cuánto?"])
        self.assertEqual(e["faq"], ["¿Pregunta?"])
        self.assertEqual(e["precios"], ["$1,500", "$85"])
        self.assertEqual(e["enlaces"], ["/x"])


if __name__ == "__main__":
    unittest.main()
