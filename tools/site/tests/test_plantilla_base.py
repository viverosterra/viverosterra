"""Documento base de las páginas con plantilla."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plantillas import base  # noqa: E402

META = {"title": "Título & más", "description": "Descripción \"citada\"", "robots": "index, follow",
        "canonical": "https://www.viverosterra.com/x", "og": (("og:type", "website"), ("og:title", "T"))}


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.html = base.documento(META, "<p>cuerpo</p>", jsonld_bloques=({"@type": "Thing", "name": "a</script>b"},),
                                   precargas=('<link rel="preload" as="image" href="/a.webp">',),
                                   scripts=("/js/a.js",))

    def test_head_con_meta_en_orden_y_regiones_vacias(self):
        h = self.html
        self.assertTrue(h.startswith('<!DOCTYPE html>\n<html lang="es-MX">'))
        self.assertIn("<title>Título &amp; más</title>", h)
        self.assertIn('content="Descripción &quot;citada&quot;"', h)
        self.assertLess(h.index('property="og:type"'), h.index('property="og:title"'))
        for region in ("head", "header", "footer"):
            self.assertIn(f"<!-- vt:{region} -->\n<!-- /vt:{region} -->", h)
        self.assertIn('<body class="vt-pagina">', h)
        self.assertIn('<main id="main">\n<p>cuerpo</p>\n</main>', h)
        self.assertLess(h.index("<!-- /vt:footer -->"), h.index('<script src="/js/a.js" defer></script>'))

    def test_sin_css_viejo_ni_google_fonts(self):
        self.assertNotRegex(self.html, r"fonts\.googleapis|tailwind\.css|design-system\.css|servicios\.css")

    def test_json_ld_compacto_y_seguro(self):
        bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S).group(1)
        self.assertNotIn("</script>b", bloque)
        self.assertEqual(json.loads(bloque)["name"], "a</script>b")
        self.assertIn('{"@type":"Thing"', bloque)

    def test_precarga_de_imagen_con_srcset(self):
        link = base.precarga_imagen({"src": "/a.webp", "srcset": "/a-640.webp 640w, /a.webp 1024w", "sizes": "100vw"})
        self.assertIn('imagesrcset="/a-640.webp 640w, /a.webp 1024w"', link)
        self.assertIn('fetchpriority="high"', link)


if __name__ == "__main__":
    unittest.main()
