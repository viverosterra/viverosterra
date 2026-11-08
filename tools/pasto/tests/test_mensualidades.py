import json
import unittest
from pathlib import Path

from mensualidades import PLAZOS, planes, plazos_disponibles, redondear


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


import re
from pathlib import Path

from mensualidades import IVA, TASA_BASE, TASAS, UMBRALES

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "vt-mensualidades.js"


class ParidadJSTest(unittest.TestCase):
    def test_constantes_iguales(self):
        src = JS.read_text(encoding="utf-8")
        self.assertIn(f"TASA_BASE = {TASA_BASE}", src)
        self.assertIn(f"IVA = {IVA}", src)
        js_tasas = {int(k): float(v) for k, v in re.findall(r"(\d+): (0\.\d+)", src[src.index("TASAS"):src.index("PLAZOS")])}
        self.assertEqual(js_tasas, TASAS)
        for minimo, plazos in UMBRALES:
            self.assertIn(f"[{minimo}, [{', '.join(map(str, plazos))}]]", src)


class ParidadConJavaScriptTest(unittest.TestCase):
    """Mismos casos que public/js/tests/vt-mensualidades.test.js (casos-mensualidades.json)."""

    def test_mensualidad_igual_a_math_round(self):
        ruta = Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-mensualidades.json"
        for contado, plazo, total, mensualidad in json.loads(ruta.read_text(encoding="utf-8"))["casos"]:
            p = next(x for x in planes(contado) if x["plazo"] == plazo)
            with self.subTest(contado=contado, plazo=plazo):
                self.assertEqual((p["total"], p["mensualidad"]), (total, mensualidad))

    def test_redondear_sube_los_medios(self):
        self.assertEqual([redondear(x) for x in (958.5, 1666.5, 2.5, 0.49)], [959, 1667, 3, 0])
