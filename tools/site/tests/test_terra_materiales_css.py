"""terra-materiales.css: hoja de las páginas de materiales (Etapa 2f, revisión). Todo bajo .vt-materiales, sin colores
literales ni !important, comparativas compactas en celular, mosaico de tres fotos sin huérfana y presupuesto propio."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-materiales.css"


class TerraMaterialesCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_materiales(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-materiales ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_comparativa_compacta_y_mosaico_sin_huerfana(self):
        self.assertIn(".vt-materiales .vt-tabla--comparar{display:table;", self.css)
        self.assertIn(".vt-materiales .vt-tabla--comparar td::before{content:none}", self.css)
        self.assertIn(".vt-materiales .vt-obras:has(>:nth-child(3):last-child)>*{grid-column:span 2}", self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 4 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 1536)


if __name__ == "__main__":
    unittest.main()
