"""terra-precios.css: hoja de /precios (Etapa 2g). Todo bajo .vt-precios, sin colores literales ni !important, tablas de
varias columnas compactas en celular y presupuesto propio (terra.css está a ~0.5 KB de su tope)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-precios.css"


class TerraPreciosCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_precios(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not p.strip().startswith(".vt-precios ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_tablas_compactas_y_anclas_bajo_el_menu(self):
        self.assertIn(".vt-precios .vt-tabla--compacta td{text-align:right;", self.css)
        self.assertIn(".vt-precios :is(section,li)[id]{scroll-margin-top:calc(var(--vt-head-h) + 16px)}", self.css)

    def test_indice_se_desliza_en_celular_y_el_simulador_ocupa_el_ancho(self):
        self.assertRegex(self.css, r"\.vt-saltos ul\{display:flex;[^}]*overflow-x:auto")
        self.assertIn("@media (max-width:640px){.vt-precios .vt-sim .vt-btn{width:100%}}", self.css)

    def test_reglas_compartidas_con_las_zonas_en_terra_css(self):
        """La lista de precios y las anclas también viven en las zonas, que no cargan esta hoja."""
        terra = (HOJA.parent / "terra.css").read_text(encoding="utf-8")
        for regla in (".vt-tabla--lista{max-width:56rem}", ".vt-tabla__p .vt-tabla__desde{display:inline",
                      ".vt-bloque[id]{scroll-margin-top:calc(var(--vt-head-h) + 16px)}",
                      ".vt-colonias li{grid-template-columns:1fr auto"):
            with self.subTest(regla=regla):
                self.assertIn(regla, terra)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 2 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 1024)


if __name__ == "__main__":
    unittest.main()
