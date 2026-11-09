"""terra-nochebuenas.css: hoja de la página de temporada. Todo bajo .vt-nochebuenas (también la barra, que va fuera de
<main>), sin colores literales ni !important, con estados definidos, movimiento reducido y presupuesto propio."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-nochebuenas.css"
ALCANCE = re.compile(r"\.vt-nochebuenas(?![\w-])")


class TerraNochebuenasCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_nochebuenas(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not ALCANCE.match(p.strip())]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_hidden_oculta_tambien_la_barra_fuera_de_main(self):
        self.assertIn(".vt-nochebuenas [hidden]{display:none}", self.css)
        self.assertIn(".vt-nochebuenas .vt-nb-bar", self.css)

    def test_objetivos_tactiles_y_estados(self):
        for regla in (":hover", ":focus-visible", ":active", "min-height:44px", "@media (prefers-reduced-motion:reduce)"):
            with self.subTest(regla=regla):
                self.assertIn(regla, self.css)

    def test_subtotal_con_ancho_minimo_y_fechas_sin_hueco(self):
        self.assertIn("minmax(104px,auto)", self.css)
        self.assertIn(":not(:has(li:not([hidden]))){display:none}", self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 12 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 4 * 1024)


if __name__ == "__main__":
    unittest.main()
