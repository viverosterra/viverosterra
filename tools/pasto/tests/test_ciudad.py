# tools/pasto/tests/test_ciudad.py
import json
import re
import unittest

from ciudad import build_ciudad, totales
from ciudades import CIUDADES
from data import MODELOS

MTY = next(c for c in CIUDADES if c["slug"] == "monterrey")


class CiudadTest(unittest.TestCase):
    def test_totales_monterrey_aruba(self):
        aruba = next(m for m in MODELOS if m["slug"] == "aruba-10")
        # 25 m² a precio t2 ($159) + 1 rollo de flete B ($1,150); 50 m² rollo ($139) + 1 flete; 100 m² + 2 fletes
        self.assertEqual(totales(aruba, "B"), [(25, 25 * 159 + 1150), (50, 50 * 139 + 1150), (100, 100 * 139 + 2300)])

    def test_html_basico(self):
        html = build_ciudad(MTY)
        self.assertIn("<h1", html)
        self.assertIn("Monterrey", html)
        self.assertIn("$162", html)
        self.assertIn("/pasto-sintetico?estado=nuevo-leon", html)
        self.assertIn('rel="canonical" href="https://www.viverosterra.com/pasto-sintetico/envio/monterrey"', html)

    def test_jsonld_valido(self):
        html = build_ciudad(MTY)
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(bloque)

    def test_schema_tiene_product_con_envio(self):
        html = build_ciudad(MTY)
        bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
        graph = json.loads(bloque)["@graph"]
        productos = [n for n in graph if n.get("@type") == "Product"]
        self.assertEqual(len(productos), 1)
        self.assertIn("shippingDetails", productos[0]["offers"])
        self.assertTrue(any(n.get("@type") == "FAQPage" for n in graph))
        self.assertTrue(any(n.get("@type") == "BreadcrumbList" for n in graph))
        self.assertIn(MTY["intro"][:40], html)
