import os
import re
import unittest
import xml.etree.ElementTree as ET

from data import MODELOS
from feed import build_feed

PUBLIC = os.path.join(os.path.dirname(__file__), "..", "..", "..", "public")
G = "{http://base.google.com/ns/1.0}"


class FeedTest(unittest.TestCase):
    def setUp(self):
        self.root = ET.fromstring(build_feed().encode("utf-8"))
        self.items = self.root.findall("./channel/item")

    def test_un_item_por_modelo_con_su_ficha(self):
        self.assertEqual(len(self.items), len(MODELOS))
        for it, m in zip(self.items, MODELOS):
            self.assertEqual(it.find(G + "link").text, f"https://www.viverosterra.com/pasto-sintetico/{m['slug']}")
            self.assertEqual(it.find(G + "price").text, f"{m['rollo']:.2f} MXN")
            self.assertEqual(it.find(G + "unit_pricing_measure").text, "1 sqm")
            self.assertEqual(it.find(G + "availability").text, "in_stock")

    def test_imagenes_existen(self):
        for it in self.items:
            for tag in ("image_link", "additional_image_link"):
                for el in it.findall(G + tag):
                    path = os.path.join(PUBLIC, el.text.replace("https://www.viverosterra.com/", ""))
                    self.assertTrue(os.path.exists(path), el.text)

    def test_envio_nunca_menor_a_la_tarifa_mas_alta(self):
        for it in self.items:
            self.assertEqual(it.find(G + "shipping/" + G + "price").text, "1400.00 MXN")

    def test_sin_palabras_prohibidas(self):
        texto = build_feed().lower()
        for palabra in ("oasis", "pastoplus", "gratis", "muestra"):
            self.assertNotIn(palabra, texto)
