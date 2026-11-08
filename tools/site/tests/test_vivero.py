"""/vivero-tampico: domicilio, horario y precios de datos.py, FAQ visible igual al JSON-LD."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
from plantillas import vivero  # noqa: E402

K = generar.cargar("vivero").CONTENIDO


class ViveroTest(unittest.TestCase):
    def setUp(self):
        self.html = vivero.render(K)

    def test_domicilio_horario_y_mapa(self):
        for pieza in (datos.CALLE, datos.COLONIA, datos.HORARIO, datos.MAPS_URL):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, self.html)

    def test_precios_de_datos(self):
        self.assertIn(f"${datos.PRECIOS['palma_desde']}", self.html)
        self.assertIn(f"${datos.PRECIOS['pasto_solo_m2']}/m²", self.html)

    def test_faq_visible_igual_al_json_ld(self):
        grafo = json.loads(re.search(r'application/ld\+json">(.*?)</script>', self.html, re.S).group(1))["@graph"]
        faq = next(n for n in grafo if n["@type"] == "FAQPage")
        for q in faq["mainEntity"]:
            with self.subTest(pregunta=q["name"]):
                self.assertIn(q["name"], self.html)
                self.assertIn(q["acceptedAnswer"]["text"], self.html)

    def test_horas_del_negocio_de_datos_y_sin_instock(self):
        self.assertIn('"closes":"14:00"', self.html)
        self.assertNotIn("InStock", self.html)

    def test_una_sola_foto_de_main(self):
        self.assertEqual(re.findall(r'<img src="([^"]+)"', re.search(r"<main.*</main>", self.html, re.S).group(0)),
                         ["/img/portadas/arboles-tampico-viveros-terra-sm.webp"])


if __name__ == "__main__":
    unittest.main()
