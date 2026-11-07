import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        self.pub = Path(tempfile.mkdtemp())
        (self.pub / "css").mkdir()
        (self.pub / "js").mkdir()
        (self.pub / "css" / "terra.css").write_text(".vt-a{}", encoding="utf-8")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_y_borra_las_viejas(self):
        viejo = self.pub / "css" / "terra.0000000000.css"
        viejo.write_text("viejo", encoding="utf-8")
        urls = activos.publicar(self.pub)
        self.assertFalse(viejo.exists())
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}")
        self.assertTrue((self.pub / "css" / "terra.css").exists())
        self.assertEqual(len(list((self.pub / "css").glob("terra.*.css"))), 1)

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        (self.pub / "css" / "terra.css").write_text(".vt-b{}", encoding="utf-8")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])


if __name__ == "__main__":
    unittest.main()
