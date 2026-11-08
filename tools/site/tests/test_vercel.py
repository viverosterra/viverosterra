import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import paginas  # noqa: E402

VERCEL = paginas.PUBLIC.parent / "vercel.json"
HASH = r"/(css|js)/(terra|terra-tienda|terra-plantas|legacy-fixes)\.([0-9a-f]+)\.(css|js)"
GENERAL_JS_CSS = r"/(.*)\.(js|css)"
IMAGENES = r"/(.*)\.(png|jpg|jpeg|webp|gif|svg|ico)"
FUENTES = r"/(.*)\.(woff2|woff|ttf)"
GA4 = ("https://*.google-analytics.com", "https://*.analytics.google.com", "https://*.g.doubleclick.net",
       "https://www.google.com")


def directiva(csp, nombre):
    return next(d.split()[1:] for d in csp.split(";") if d.split() and d.split()[0] == nombre)


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


    def test_frame_options_deny_igual_que_frame_ancestors(self):
        self.assertEqual(self.cabeceras("/(.*)")["X-Frame-Options"], "DENY")

    def test_csp_permite_los_origenes_de_ga4(self):
        csp = self.cabeceras("/(.*)")["Content-Security-Policy-Report-Only"]
        for nombre in ("connect-src", "img-src"):
            for origen in GA4:
                with self.subTest(directiva=nombre, origen=origen):
                    self.assertIn(origen, directiva(csp, nombre))

    def test_imagenes_sin_hash_una_semana_y_fuentes_inmutables(self):
        self.assertEqual(self.cabeceras(IMAGENES)["Cache-Control"],
                         "public, max-age=604800, stale-while-revalidate=86400")
        self.assertEqual(self.cabeceras(FUENTES)["Cache-Control"], "public, max-age=31536000, immutable")
        inmutables = [r["source"] for r in self.cfg["headers"]
                      if any("immutable" in h["value"] for h in r["headers"] if h["key"] == "Cache-Control")]
        self.assertEqual(sorted(inmutables), sorted([HASH, FUENTES]))
        fuentes = [r["source"] for r in self.cfg["headers"]]
        self.assertEqual(fuentes.index(HASH), len(fuentes) - 1, "la regla de assets con hash va al final y gana")


if __name__ == "__main__":
    unittest.main()
