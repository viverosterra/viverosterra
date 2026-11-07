import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402


class BorradorTest(unittest.TestCase):
    def test_borrador_eliminado_y_redirigido_a_la_home(self):
        self.assertFalse((paginas.PUBLIC / "preview-mapa-cobertura.html").exists())
        redirects = json.loads((paginas.PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        destinos = {r["source"]: r["destination"] for r in redirects}
        self.assertEqual(destinos.get("/preview-mapa-cobertura"), "/")
        self.assertEqual(destinos.get("/preview-mapa-cobertura.html"), "/")


if __name__ == "__main__":
    unittest.main()
