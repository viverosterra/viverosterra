"""El Medidor da lo mismo en Python (componentes.py, HTML inicial) y en JavaScript (public/js/vt-medidor.js).
Los casos viven en public/js/tests/casos-medidor.json; node --test los corre contra el JS."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-medidor.json")
                   .read_text(encoding="utf-8"))


class MedidorParidadTest(unittest.TestCase):
    def test_mismos_resultados_que_el_js(self):
        for caso in CASOS["casos"]:
            e = caso["entrada"]
            r = c.calculo_medidor(e["largo"], e["ancho"], e["modo"])
            t = c.textos_medidor(e["largo"], e["ancho"], r, e["colonia"], e["plazo"])
            obtenido = {k: r[k] for k in ("m2", "precio", "desde", "total", "rotulo", "aviso")}
            obtenido.update(t)
            with self.subTest(entrada=e):
                self.assertEqual(obtenido, caso["esperado"])

    def test_hay_casos_con_plazo_elegido_y_con_plazo_que_no_aplica(self):
        pedidos = [(caso["entrada"]["plazo"], caso["esperado"]["plazo"]) for caso in CASOS["casos"]]
        self.assertIn((6, 6), pedidos)
        self.assertIn((12, 1), pedidos)

    def test_modos_del_json_son_los_de_datos(self):
        self.assertEqual(CASOS["modos"], {k: {kk: v for kk, v in m.items() if kk != "opcion"}
                                          for k, m in c.MODOS_MEDIDOR.items()})
        self.assertEqual(c.MODOS_MEDIDOR["instalado"]["precio"], datos.PRECIOS["pasto_instalado_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["solo"]["precio"], datos.PRECIOS["pasto_solo_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["mayoreo"]["precio"], datos.PRECIOS["pasto_mayoreo_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["mayoreo"]["minimo"], datos.PRECIOS["pasto_mayoreo_minimo_m2"])


if __name__ == "__main__":
    unittest.main()
