import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pub = Path(tmp.name)
        (self.pub / "css").mkdir()
        (self.pub / "js").mkdir()
        self.escribir(".vt-a{}")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def escribir(self, css):
        (self.pub / "css" / "terra.css").write_text(css, encoding="utf-8")

    def copias(self):
        return sorted(p.name for p in (self.pub / "css").glob("terra.*.css"))

    def viejo(self, nombre, mtime):
        path = self.pub / "css" / nombre
        path.write_text("viejo", encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_la_fuente(self):
        urls = activos.publicar(self.pub)
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}")
        self.assertTrue((self.pub / "css" / "terra.css").exists())

    def test_publicar_conserva_la_generacion_anterior(self):
        anterior = self.viejo("terra.1111111111.css", 2_000_000_000)
        mas_vieja = self.viejo("terra.0000000000.css", 1_000_000_000)
        activos.publicar(self.pub)
        self.assertTrue(anterior.exists())
        self.assertFalse(mas_vieja.exists())
        self.assertEqual(len(self.copias()), 2)

    def test_dos_cambios_seguidos_dejan_actual_y_anterior(self):
        primera = activos.publicar(self.pub)["terra.css"]
        os.utime(self.pub / primera.lstrip("/"), (1_000_000_000, 1_000_000_000))
        self.escribir(".vt-b{}")
        segunda = activos.publicar(self.pub)["terra.css"]
        os.utime(self.pub / segunda.lstrip("/"), (2_000_000_000, 2_000_000_000))
        self.escribir(".vt-c{}")
        tercera = activos.publicar(self.pub)["terra.css"]
        self.assertEqual(self.copias(), sorted(Path(u).name for u in (segunda, tercera)))

    def test_publicar_es_idempotente(self):
        self.viejo("terra.1111111111.css", 1_000_000_000)
        primera = activos.publicar(self.pub)
        copias = self.copias()
        self.assertEqual(activos.publicar(self.pub), primera)
        self.assertEqual(self.copias(), copias)

    def test_no_toca_archivos_que_no_son_copias(self):
        ajeno = self.pub / "css" / "terra.min.css"
        ajeno.write_text("x", encoding="utf-8")
        activos.publicar(self.pub)
        self.assertTrue(ajeno.exists())

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_mismo_contenido_mismo_hash(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.escribir(".vt-a{}")
        self.assertEqual(antes, activos.urls(self.pub)["terra.css"])


if __name__ == "__main__":
    unittest.main()
