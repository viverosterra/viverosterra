import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402


class BorradorTest(unittest.TestCase):
    def test_borrador_eliminado_y_sin_redireccion(self):
        """SEO fase 0 (2026-11-10): el borrador nunca fue contenido; ya no se redirige a la home (era un 301 hacia
        una página sin relación) y responde 404."""
        self.assertFalse((paginas.PUBLIC / "preview-mapa-cobertura.html").exists())
        redirects = json.loads((paginas.PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        origenes = {r["source"] for r in redirects}
        self.assertNotIn("/preview-mapa-cobertura", origenes)
        self.assertNotIn("/preview-mapa-cobertura.html", origenes)


if __name__ == "__main__":
    unittest.main()
