import re
import unittest
from pathlib import Path

from data import ZONAS, ZONA_ESTADOS

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "tienda-pasto.js"


class ParidadTest(unittest.TestCase):
    def test_estado_zona_igual_en_js(self):
        src = JS.read_text(encoding="utf-8")
        bloque = src[src.index("const ESTADO_ZONA = {"):src.index("};", src.index("const ESTADO_ZONA = {"))]
        js = dict(re.findall(r"'([^']+)':\s*'([ABC])'", bloque))
        py = {e: z for z, (_n, es) in ZONA_ESTADOS.items() for e in es}
        self.assertEqual(js, py)

    def test_tarifas_iguales_en_js(self):
        src = JS.read_text(encoding="utf-8")
        js = {z: int(t) for z, t in re.findall(r"([ABC]):\s*\{\s*tarifa:\s*(\d+)", src)}
        self.assertEqual(js, ZONAS)


if __name__ == "__main__":
    unittest.main()
