"""Las calculadoras de materiales dan lo mismo que en main (calcularTierra, calcularTezontle y calcularMarmol, congeladas
en public/js/tests/casos-materiales.json ejecutando el JS de main) en Python (componentes_materiales.py) y en JavaScript
(public/js/vt-materiales.js; vt-materiales.test.js corre los mismos casos). Las únicas diferencias con main son las que
pide el dueño y se aplican aquí a lo que publicaba main antes de comparar (esperado_de_main)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_materiales as cm  # noqa: E402
import datos  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-materiales.json")
                   .read_text(encoding="utf-8"))
CAMION_MAIN = "Camión volteo 8m³+ (~desde $5,000)"


def esperado_de_main(clave, caso):
    """Lo que mostraba y mandaba main, con los cambios declarados: el camión de tierra negra sin el "desde $5,000" (no
    está en datos.py), el mármol sin "$250 c/u" ni "Precio estimado" (no está en datos.py), "cubren" en vez de "cubre"
    y la pregunta de cierre del mármol igual a la de los otros dos (sin "confirmar disponibilidad")."""
    v, m = caso["visibles"], caso["mensaje"]
    if clave == "tierra-negra":
        return {"cantidad": v["res-m3"], "presentacion": v["res-formato"].replace(CAMION_MAIN, cm.CAMION_TIERRA),
                "equivalente": v["res-costales"], "mensaje": m}
    if clave == "tezontle":
        return {"cantidad": v["tez-res-m3"], "presentacion": v["tez-res-formato"], "equivalente": v["tez-res-costales"],
                "mensaje": m}
    lineas = [x for x in m.split("\n") if not x.startswith("Precio estimado: ")]
    lineas[-1] = cm.CIERRE_MENSAJE
    return {"cantidad": f"{v['res-sacos']} sacos", "peso": v["res-peso"],
            "nota": v["res-nota"].replace(" sacos cubre ", " sacos cubren ").replace(" A $250 c/u.", ""),
            "mensaje": "\n".join(lineas)}


class MaterialesParidadTest(unittest.TestCase):
    def test_mismos_resultados_que_main(self):
        for clave, calc in CASOS["calculadoras"].items():
            usos = {o["value"]: o["text"] for o in calc["capas"]}
            for caso in calc["casos"]:
                area, capa = caso["entrada"]["area"], float(caso["entrada"]["capa"])
                r = cm.calculo(clave, area, capa)
                with self.subTest(clave=clave, entrada=caso["entrada"]):
                    self.assertEqual(cm.textos(clave, area, capa, r, usos[caso["entrada"]["capa"]]),
                                     esperado_de_main(clave, caso))

    def test_capas_de_main(self):
        """Mismos valores que los <select> de main y, en tezontle, el mismo texto (va en el mensaje como "Uso: …")."""
        for clave, calc in CASOS["calculadoras"].items():
            capas = cm.CALCULADORAS[clave]["capas"]
            with self.subTest(clave=clave):
                self.assertEqual([v for v, _t in capas], [o["value"] for o in calc["capas"]])
        self.assertEqual([t for _v, t in cm.CALCULADORAS["tezontle"]["capas"]],
                         [o["text"] for o in CASOS["calculadoras"]["tezontle"]["capas"]])

    def test_casos_con_los_redondeos_de_main(self):
        """7 m² × 10 cm daba 0.8 m³ en main (7 × 0.1 × 10 = 7.000000000000001 y Math.ceil sube): se conserva igual."""
        self.assertEqual(cm.calculo("tierra-negra", 7, 0.1)["m3"], 0.8)
        self.assertEqual(cm.calculo("tezontle", 333, 0.1)["m3"], 33.4)

    def test_piedra_bola_con_la_regla_de_su_pregunta(self):
        """Piedra bola no tenía calculadora: su pregunta frecuente decía 1,200 a 1,500 kg para 10 m² (120 a 150 kg/m²)."""
        t = cm.textos("piedra-bola", 10, 0, cm.calculo("piedra-bola", 10))
        self.assertEqual(t["cantidad"], "1,200 a 1,500 kg")
        self.assertTrue(t["mensaje"].endswith(cm.CIERRE_MENSAJE))

    def test_precios_de_la_calculadora_salen_de_datos(self):
        self.assertEqual(cm.CALCULADORAS["tierra-negra"]["precio_costal"], datos.PRECIOS["tierra_negra_costal"])
        self.assertEqual(cm.CALCULADORAS["tierra-negra"]["precio_m3"], datos.PRECIOS["tierra_negra_m3"])
        for clave in ("tezontle", "marmol", "piedra-bola"):
            with self.subTest(clave=clave):
                self.assertFalse([k for k in cm.CALCULADORAS[clave] if k.startswith("precio")])

    def test_numero_y_area_como_javascript(self):
        self.assertEqual([cm.numero_js(x) for x in (8.0, 0.1, 87.5, 1000)], ["8", "0.1", "87.5", "1000"])
        self.assertEqual([cm.leer_area(x) for x in ("1,200", "12,5", "80 m²", "", "-3", "200000")],
                         [1200, 12.5, 80, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
