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


if __name__ == "__main__":
    unittest.main()
