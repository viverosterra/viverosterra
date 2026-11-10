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

    def test_como_llegar_es_boton_junto_a_whatsapp(self):
        fila = re.search(r'<div class="vt-cta" data-hero-cta>(.*?)</div>', self.html, re.S).group(1)
        boton = re.search(r'<a class="vt-btn vt-btn--linea" data-cta="vivero:mapas" href="([^"]+)"[^>]*>(.*?)</a>', fila)
        self.assertEqual(boton.group(1), datos.MAPS_URL)
        self.assertIn("Cómo llegar", boton.group(2))
        self.assertLess(fila.index("vt-btn--wa"), fila.index("vivero:mapas"))
        self.assertLess(fila.index("vivero:mapas"), fila.index("tel:"))
        self.assertNotIn("vt-portada__tambien", self.html)

    def test_enlaces_a_mapas_etiquetados(self):
        for cta, texto in (("vivero:mapas-google", "Abrir en Google Maps"), ("vivero:mapas-apple", "Apple Maps")):
            with self.subTest(cta=cta):
                self.assertRegex(self.html, rf'<a [^>]*data-cta="{cta}"[^>]*>{texto}</a>')

    def test_una_sola_foto_de_main(self):
        self.assertEqual(re.findall(r'<img src="([^"]+)"', re.search(r"<main.*</main>", self.html, re.S).group(0)),
                         ["/img/portadas/arboles-tampico-viveros-terra-sm.webp"])


if __name__ == "__main__":
    unittest.main()
