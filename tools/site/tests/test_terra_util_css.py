"""terra-util.css: hoja de las utilitarias (Etapa 2i). Todo bajo .vt-util, sin colores literales ni !important, solo
transform y opacity en movimiento y presupuesto propio (terra.css está a 35 B de su tope)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-util.css"


class TerraUtilCssTest(unittest.TestCase):
    def setUp(self):
        self.css = sin_comentarios(HOJA.read_text(encoding="utf-8"))

    def test_todo_selector_bajo_vt_util(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", self.css):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-util ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", self.css), [])
        self.assertNotIn("!important", self.css)

    def test_hidden_gana_a_las_reglas_con_display(self):
        """Va al final con la misma especificidad: los pasos, la orden y la suma tienen display propio."""
        ultimo = self.css.rindex(".vt-util [hidden]{display:none}")
        for regla in (".vt-util .vt-paso", ".vt-util .vt-util__orden{", ".vt-util .vt-util__suma{"):
            self.assertLess(self.css.index(regla), ultimo)

    def test_movimiento_solo_compositor(self):
        for transicion in re.findall(r"transition:([^;}]+)", self.css):
            if transicion.strip() == "none":
                continue
            propiedades = {t.strip().split()[0] for t in transicion.split(",")}
            self.assertLessEqual(propiedades, {"transform", "opacity", "background", "color"})

    def test_presupuesto(self):
        datos = activos.minificar_css(HOJA.read_text(encoding="utf-8")).encode("utf-8")
        self.assertLess(len(datos), 9 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 2 * 1024 + 512)


if __name__ == "__main__":
    unittest.main()
