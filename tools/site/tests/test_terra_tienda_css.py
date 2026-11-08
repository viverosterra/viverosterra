"""terra-tienda.css: hoja de la tienda de pasto sintético. Todo bajo .vt-tienda, sin colores literales, presupuesto
propio y clases sin prefijo solo si las crea o busca el JS de la tienda."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import clases, sin_comentarios, tokens  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"
TIENDA = PUBLIC / "css" / "terra-tienda.css"
# Clases que crean o buscan public/js/tienda-pasto.js y tienda-hub.js (no se reescriben): se estilan solo bajo .vt-tienda.
CLASES_DEL_JS = {"plan", "pay-rule", "buybar__info", "buybar__name", "buybar__price", "buybar__plan", "cot-item",
                 "cot-item__name", "cot-item__meta", "cot-item__m2", "cot-item__remove", "drawer__empty",
                 "gallery__slide", "is-updating", "quiz__pick", "quiz__pick--main", "quiz__label", "quiz__name",
                 "quiz__meta", "quiz__actions", "btn", "btn--primary"}


class TerraTiendaCssTest(unittest.TestCase):
    def setUp(self):
        self.css = TIENDA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_tienda(self):
        css = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}", "", sin_comentarios(self.css))
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", css):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in selector.split(",") if not p.strip().startswith(".vt-tienda ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_y_solo_tokens_de_terra(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        definidos = tokens((PUBLIC / "css" / "terra.css").read_text(encoding="utf-8"))
        usados = set(re.findall(r"var\((--vt-[\w-]+)\)", css))
        self.assertEqual(sorted(usados - set(definidos)), [])

    def test_presupuesto(self):
        publicado = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(gzip.compress(publicado, mtime=0)), 6 * 1024)
        self.assertLess(len(publicado), 24 * 1024)

    def test_clases_sin_prefijo_solo_las_del_js(self):
        propias = {c for c in clases(self.css) if not c.startswith("vt-")}
        self.assertEqual(sorted(propias - CLASES_DEL_JS), [])
        fuentes = "".join(p.read_text(encoding="utf-8") for p in (PUBLIC / "js" / "tienda-pasto.js",
                                                                  PUBLIC / "js" / "tienda-hub.js"))
        for clase in sorted(propias):
            with self.subTest(clase=clase):
                self.assertIn(clase, fuentes)

    def test_movimiento_reducido(self):
        self.assertIn("@media (prefers-reduced-motion:reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
