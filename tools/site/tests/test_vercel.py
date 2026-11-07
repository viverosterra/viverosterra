import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import paginas  # noqa: E402

VERCEL = paginas.PUBLIC.parent / "vercel.json"
HASH = r"/(css|js)/(terra|legacy-fixes)\.([0-9a-f]+)\.(css|js)"
GENERAL_JS_CSS = r"/(.*)\.(js|css)"


class VercelTest(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(VERCEL.read_text(encoding="utf-8"))

    def cabeceras(self, fuente):
        return {h["key"]: h["value"] for r in self.cfg["headers"] if r["source"] == fuente for h in r["headers"]}

    def test_csp_en_report_only_y_sin_x_xss_protection(self):
        h = self.cabeceras("/(.*)")
        self.assertNotIn("X-XSS-Protection", h)
        self.assertNotIn("Content-Security-Policy", h)
        csp = h["Content-Security-Policy-Report-Only"]
        for directiva in ("default-src 'self'", "https://www.googletagmanager.com", "https://fonts.googleapis.com",
                          "https://formsubmit.co", "frame-ancestors 'none'", "object-src 'none'", "base-uri 'self'"):
            with self.subTest(directiva=directiva):
                self.assertIn(directiva, csp)

    def test_assets_con_hash_inmutables_y_despues_de_la_regla_general(self):
        fuentes = [r["source"] for r in self.cfg["headers"]]
        self.assertLess(fuentes.index(GENERAL_JS_CSS), fuentes.index(HASH))
        self.assertEqual(self.cabeceras(HASH)["Cache-Control"], "public, max-age=31536000, immutable")
        for url in activos.urls().values():
            with self.subTest(url=url):
                self.assertIsNotNone(re.fullmatch(HASH, url))



if __name__ == "__main__":
    unittest.main()
