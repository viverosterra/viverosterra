"""Los cotizadores de empresas dan lo mismo en Python (componentes.py, HTML inicial y pruebas) y en JavaScript
(public/js/vt-b2b.js con VTMedidor.calcular). Los casos viven en public/js/tests/casos-b2b.json; node --test los corre
contra el JS."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-b2b.json")
                   .read_text(encoding="utf-8"))


class B2BParidadTest(unittest.TestCase):
    def test_volumen_igual_que_el_js(self):
        for caso in CASOS["volumen"]:
            e = caso["entrada"]
            r = c.calculo_volumen(c.leer_m2(e["texto"]))
            obtenido = {k: r[k] for k in ("m2", "precio", "desde", "total", "rotulo", "aviso")}
            obtenido.update(c.textos_volumen(r, e["empresa"], e["obra"], e["fecha"]))
            with self.subTest(entrada=e):
                self.assertEqual(obtenido, caso["esperado"])

    def test_lecturas_de_m2(self):
        for texto, esperado in CASOS["lecturas"]:
            with self.subTest(texto=texto):
                self.assertEqual(c.leer_m2(texto), esperado)

    def test_palmas_igual_que_el_js(self):
        for caso in CASOS["palmas"]:
            e = caso["entrada"]
            filas = [tuple(f) for f in e["filas"]]
            with self.subTest(entrada=e):
                self.assertEqual(c.mensaje_palmas(filas, e["empresa"], e["obra"], e["fecha"]), caso["esperado"]["mensaje"])
                self.assertEqual(c.resumen_palmas(filas), caso["esperado"]["resumen"])

    def test_modos_del_json_son_los_del_medidor(self):
        self.assertEqual(CASOS["modos"], {k: {kk: v for kk, v in c.MODOS_MEDIDOR[k].items() if kk != "opcion"}
                                          for k in ("mayoreo", "solo")})

    def test_hay_casos_bajo_y_sobre_el_minimo(self):
        precios = {caso["esperado"]["precio"] for caso in CASOS["volumen"]}
        self.assertEqual(precios, {c.P["pasto_mayoreo_m2"], c.P["pasto_solo_m2"]})


if __name__ == "__main__":
    unittest.main()
