"""terra-plantas.css: hoja de las páginas de plantas (Etapa 2e). Todo bajo .vt-plantas, sin colores literales, [hidden]
gana a los display de las tarjetas, la barra y los botones, y presupuesto propio."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

HOJA = Path(__file__).resolve().parents[3] / "public" / "css" / "terra-plantas.css"


class TerraPlantasCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_plantas(self):
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in selector.split(",") if not p.strip().startswith(".vt-plantas ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        self.assertNotIn("!important", css)

    def test_hidden_gana(self):
        for regla in (".vt-plantas [hidden]{display:none}", ".vt-plantas .vt-esp[hidden]{display:none}",
                      # Entrega B de experiencia: la barra de la lista pasó a ser la del shell con el botón "Mi lista".
                      ".vt-plantas .vt-bar--lista .vt-bar__lista[hidden]{display:none}",
                      ".vt-plantas .vt-cat__fila[hidden]{display:none}"):
            self.assertIn(regla, self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 12 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 4 * 1024)

    def test_marcador_sin_foto_con_la_misma_proporcion_que_las_fotos(self):
        """Las especies sin foto (catalogo_datos.FOTOS_RETIRADAS, hoy vacía) ocuparían el mismo 4:5 que las fotos: sin salto de diseño."""
        self.assertRegex(self.css, r"\.vt-plantas \.vt-esp__sinfoto\{[^}]*aspect-ratio:4/5")
        for clase in ("vt-sinfoto-reja", "vt-sinfoto-letra", "vt-sinfoto-tag", "vt-sinfoto-tagtexto"):
            self.assertIn(f".vt-plantas .vt-esp__sinfoto .{clase}{{", self.css)

    def test_objetivos_de_44_px_y_movimiento_reducido(self):
        self.assertIn("min-height:44px", self.css)
        self.assertIn("@media (prefers-reduced-motion:reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
