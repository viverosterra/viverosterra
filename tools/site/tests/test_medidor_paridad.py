"""El Medidor da lo mismo en Python (componentes.py, HTML inicial) y en JavaScript (public/js/vt-medidor.js).
Los casos viven en public/js/tests/casos-medidor.json; node --test los corre contra el JS."""
import json
import re
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

    def test_texto_del_boton_igual_en_python_y_js(self):
        """Sin medida, "Cotizar por WhatsApp" (HTML inicial); con medida válida, "Enviar mi medida por WhatsApp"."""
        js = (Path(__file__).resolve().parents[3] / "public" / "js" / "vt-medidor.js").read_text(encoding="utf-8")
        self.assertEqual(re.search(r"const CTA_MEDIDA = '([^']+)';", js).group(1), c.CTA_MEDIDA)
        self.assertEqual(c.CTA_MEDIDA, "Enviar mi medida por WhatsApp")
        self.assertEqual(c.CTA_WA, "Cotizar por WhatsApp")
        html = c.medidor("prueba", "home", boton_medida=True)
        self.assertIn(f'<span data-vt-o="cta-texto">{c.CTA_WA}</span>', html)
        self.assertNotIn(c.CTA_MEDIDA, html)
        self.assertNotIn("Cotizar por WhatsApp", js, "el texto sin medida es el del HTML: no se repite en el JS")

    def test_aviso_de_entrada_invalida_igual_en_python_y_js(self):
        """Entrega B de experiencia: con 0, negativos o letras el Medidor avisa bajo los campos (reescritura 2)."""
        js = (Path(__file__).resolve().parents[3] / "public" / "js" / "vt-medidor.js").read_text(encoding="utf-8")
        self.assertEqual(re.search(r"const ERROR = '([^']+)';", js).group(1), c.ERROR_MEDIDOR)
        html = c.medidor("prueba", "servicio-pasto")
        self.assertIn('aria-describedby="prueba-error"', html)
        self.assertIn('<p class="vt-correo__error" id="prueba-error" data-vt-o="error" hidden></p>', html)

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
