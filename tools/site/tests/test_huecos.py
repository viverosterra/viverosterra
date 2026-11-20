"""Ningún WhatsApp del sitio lleva rayas «___» (spec del primer mensaje, 2026-11-16)."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402

CASOS = json.loads((Path(paginas.PUBLIC) / "js" / "tests" / "casos-huecos.json").read_text(encoding="utf-8"))


class SinHuecosTest(unittest.TestCase):
    def test_casos_compartidos(self):
        for entrada, esperado in CASOS:
            with self.subTest(entrada=entrada):
                self.assertEqual(datos.sin_huecos(entrada), esperado)

    def test_wa_url_limpia(self):
        self.assertNotIn("___", datos.wa_url("Hola, quiero cotizar: ___\nColonia: ___"))

    def test_ningun_enlace_publicado_con_huecos(self):
        for archivo in Path(paginas.PUBLIC).rglob("*.html"):
            for href in re.findall(r'href="(https://wa\.me/[^"]*)"', archivo.read_text(encoding="utf-8")):
                texto = parse_qs(urlparse(html_mod.unescape(href)).query).get("text", [""])[0]
                with self.subTest(archivo=str(archivo)):
                    self.assertNotIn("___", texto)

    def test_restos_de_huecos_se_detectan(self):
        # Auditoría por página (2026-11-20): quitar «___» de «Necesito ___ m².» o «Medidas: ___ × ___ m» dejaba restos.
        for sucio in ("Hola.\nNecesito m².", "Hola.\n × m", "Medidas: × m", "Hola.\n× 5 m"):
            with self.subTest(sucio=sucio):
                self.assertTrue(restos(sucio), sucio)
        for limpio in ("Necesito 60 m².", "Precios 2026 por m²", "Medidas: 10.00 × 5.00 m = 50 m²", "- 2 × Palma kerpis, altura aprox.: 1.5 m",
                       "Hola, les mando las medidas de mi espacio para cotizar pasto sintético."):
            with self.subTest(limpio=limpio):
                self.assertEqual(restos(limpio), [], limpio)

    def test_ningun_enlace_de_la_tienda_con_restos_de_huecos(self):
        # La tienda de pasto sintético (hub, fichas, guías y ciudades). Pendiente fuera de la tienda: el artículo
        # /blog/sistema-riego-automatizado-tampico manda «… para mi jardín de m²».
        for archivo in (Path(paginas.PUBLIC) / "pasto-sintetico").rglob("*.html"):
            for href in re.findall(r'href="(https://wa\.me/[^"]*)"', archivo.read_text(encoding="utf-8")):
                texto = parse_qs(urlparse(html_mod.unescape(href)).query).get("text", [""])[0]
                with self.subTest(archivo=str(archivo)):
                    self.assertEqual(restos(texto), [])


# Un número que falta: unidad pegada a una palabra («Necesito m².») o «×» sin número a un lado (« × m», «: × 5 m»).
RESTOS = (re.compile(r"\b(?!por )[^\W\d_]+ m²"), re.compile(r"(?:^|[\n:]) *×", re.M), re.compile(r"×\s*m\b"))


def restos(texto):
    return [m.group(0) for patron in RESTOS for m in patron.finditer(texto)]


if __name__ == "__main__":
    unittest.main()
