"""Las calculadoras de materiales dan lo mismo que en main (calcularTierra, calcularTezontle y calcularMarmol, congeladas
en public/js/tests/casos-materiales.json ejecutando el JS de main) en Python (componentes_materiales.py) y en JavaScript
(public/js/vt-materiales.js; vt-materiales.test.js corre los mismos casos). Las únicas diferencias con main son las que
pide el dueño y se aplican aquí a lo que publicaba main antes de comparar (esperado_de_main)."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_materiales as cm  # noqa: E402
import datos  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-materiales.json")
                   .read_text(encoding="utf-8"))
CAMION_MAIN = "Camión volteo 8m³+ (~desde $5,000)"


GRUPO_RE = re.compile(r"(?<![\d.,])\d{4,}")


def agrupar(texto):
    """Miles con coma en lo que publicaba main ("~4286 costales" → "~4,286 costales"); los precios ya la traían."""
    return GRUPO_RE.sub(lambda m: f"{int(m.group(0)):,}", texto)


def mensaje_de_main(clave, mensaje, capa):
    """El mensaje de main con los cambios declarados: miles con coma, sin "Precio estimado" (mármol), la capa en el de
    tierra negra, la colonia por llenar antes de la pregunta y la pregunta de cierre con Madero y Altamira."""
    lineas = [agrupar(x) for x in mensaje.split("\n") if not x.startswith("Precio estimado: ")]
    lineas[-1] = cm.CIERRE_MENSAJE
    lineas.insert(len(lineas) - 2, cm.COLONIA)
    if clave == "tierra-negra":
        area = next(i for i, x in enumerate(lineas) if x.startswith("Área: "))
        lineas.insert(area + 1, f"Capa: {round(float(capa) * 100)} cm")
    return "\n".join(lineas)


def esperado_de_main(clave, caso):
    """Lo que mostraba y mandaba main, con los cambios declarados: el camión de tierra negra sin el "desde $5,000" (no
    está en datos.py), el mármol sin "$250 c/u" ni "Precio estimado" (no está en datos.py), "cubren" en vez de "cubre",
    miles con coma en área, kg, sacos y costales (revisión 2f) y el mensaje de mensaje_de_main. Los números no cambian."""
    v, capa = caso["visibles"], caso["entrada"]["capa"]
    m = mensaje_de_main(clave, caso["mensaje"], capa)
    if clave == "tierra-negra":
        return {"cantidad": agrupar(v["res-m3"]),
                "presentacion": agrupar(v["res-formato"].replace(CAMION_MAIN, cm.CAMION_TIERRA)),
                "equivalente": agrupar(v["res-costales"]), "mensaje": m}
    if clave == "tezontle":
        return {"cantidad": agrupar(v["tez-res-m3"]), "presentacion": agrupar(v["tez-res-formato"]),
                "equivalente": agrupar(v["tez-res-costales"]), "mensaje": m}
    return {"cantidad": f"{v['res-sacos']:,} sacos", "peso": agrupar(v["res-peso"]),
            "nota": agrupar(v["res-nota"].replace(" sacos cubre ", " sacos cubren ").replace(" A $250 c/u.", "")),
            "mensaje": m}


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

    def test_son_los_195_casos_de_main(self):
        self.assertEqual(sum(len(c["casos"]) for c in CASOS["calculadoras"].values()), 195)

    def test_miles_con_coma_en_lo_visible_y_en_el_mensaje(self):
        """Revisión 2f: "3,750 sacos" y "75,000 kg" en vez de "3750 sacos" y "75000 kg"; los decimales no se redondean."""
        t = cm.textos("marmol", 1250, 4, cm.calculo("marmol", 1250, 4))
        self.assertEqual((t["cantidad"], t["peso"]), ("3,750 sacos", "75,000 kg"))
        self.assertEqual(t["nota"], "3,750 sacos cubren 1,250 m² con capa de 4 cm.")
        self.assertIn("Área: 1,250 m²\nCapa: 4 cm\nCantidad: 3,750 sacos", t["mensaje"])
        t = cm.textos("tezontle", 5000, 0.08, cm.calculo("tezontle", 5000, 0.08), "x")
        self.assertEqual((t["cantidad"], t["equivalente"]), ("400 m³", "~14,815 costales"))
        self.assertEqual([cm.miles(x) for x in (999, 1000, 1250.5, 100000, 0.1)],
                         ["999", "1,000", "1,250.5", "100,000", "0.1"])

    def test_mensaje_con_la_colonia_y_cierre_de_la_zona(self):
        """Los cuatro mensajes con resultado conservan "Colonia de entrega: ___" (como el de la página) antes de la
        pregunta, que nombra Tampico, Madero y Altamira; el de tierra negra lleva también la capa."""
        for clave, capa in (("tierra-negra", 0.08), ("tezontle", 0.06), ("marmol", 5), ("piedra-bola", 0)):
            mensaje = cm.textos(clave, 30, capa, cm.calculo(clave, 30, capa), "Control de maleza (6 cm)")["mensaje"]
            with self.subTest(clave=clave):
                self.assertTrue(mensaje.endswith(f"\n{cm.COLONIA}\n\n{cm.CIERRE_MENSAJE}"))
                self.assertIn("en Tampico, Madero o Altamira?", mensaje)
        tierra = cm.textos("tierra-negra", 30, 0.15, cm.calculo("tierra-negra", 30, 0.15))["mensaje"]
        self.assertIn("Área: 30 m²\nCapa: 15 cm\nCantidad: 4.5 m³", tierra)

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
