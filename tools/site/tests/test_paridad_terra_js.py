import json
import re
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "terra.js"
HORARIO = json.loads((JS.parent / "tests" / "casos-horario.json").read_text(encoding="utf-8"))
DIAS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def abierto(instante):
    """El mismo cálculo que abierto() de terra.js, directo de datos.HORARIO_LD y datos.FESTIVOS."""
    local = datetime.fromisoformat(instante.replace("Z", "+00:00")).astimezone(ZoneInfo(HORARIO["zona"]))
    if local.strftime("%m-%d") in datos.FESTIVOS:
        return False
    hora = local.strftime("%H:%M")
    return any(DIAS[local.weekday()] in dias and abre <= hora < cierra for dias, abre, cierra in datos.HORARIO_LD)


class ParidadTerraJsTest(unittest.TestCase):
    def test_firma_igual_en_js_y_python(self):
        firma = re.search(r"const FIRMA = '([^']+)';", JS.read_text(encoding="utf-8")).group(1)
        self.assertEqual(firma, datos.FIRMA)

    def test_horario_y_festivos_de_los_casos_son_los_de_datos(self):
        self.assertEqual(HORARIO["horario"], datos.horario_marca())
        self.assertEqual(HORARIO["festivos"], datos.festivos_marca())
        self.assertRegex(JS.read_text(encoding="utf-8"), rf"const ZONA = '{HORARIO['zona']}';")

    def test_cada_caso_de_horario_coincide_con_datos(self):
        """node --test corre los mismos casos contra terra.js (public/js/tests/terra.test.js)."""
        for caso in HORARIO["casos"]:
            with self.subTest(caso=caso["nota"]):
                self.assertEqual(abierto(caso["instante"]), caso["abierto"])
        notas = " ".join(caso["nota"] for caso in HORARIO["casos"])
        for borde in ("sábado 13:59", "sábado 14:00", "viernes 17:59", "viernes 18:00", "domingo", "25 de diciembre",
                      "1 de enero", "en UTC ya es"):
            self.assertIn(borde, notas)


if __name__ == "__main__":
    unittest.main()
