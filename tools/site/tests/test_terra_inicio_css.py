"""terra-inicio.css: hoja propia de la home (hero nuevo, Medidor en celular, WhatsApp por servicio y CTA de sección).
Todo bajo .vt-inicio, solo con tokens de terra.css (sin colores literales ni !important), con estados definidos,
movimiento reducido y presupuesto propio (spec del hero, 2026-11-09: menos de 6 KB)."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_movimiento_css import reglas  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

CSS = Path(__file__).resolve().parents[3] / "public" / "css"
HOJA = CSS / "terra-inicio.css"
ALCANCE = re.compile(r"\.vt-inicio(?![\w-])")


class TerraInicioCssTest(unittest.TestCase):
    def setUp(self):
        self.css = HOJA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_inicio(self):
        ajenos = []
        for contextos, selector, _cuerpo in reglas(self.css):
            if any(c.startswith("@keyframes") for c in contextos):  # sus pasos (from, 40%, to) no son selectores
                continue
            ajenos += [p.strip() for p in re.split(r",(?![^(]*\))", selector) if not ALCANCE.match(p.strip())]
        nombres = re.findall(r"@keyframes ([\w-]+)", self.css)
        self.assertEqual([n for n in nombres if not n.startswith("vt-inicio-")], [], "keyframes con prefijo propio")
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_ni_important(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\(", css), [])
        self.assertNotIn("!important", css)

    def test_solo_tokens_que_define_terra_css(self):
        definidos = set(re.findall(r"(--vt-[\w-]+)\s*:", (CSS / "terra.css").read_text(encoding="utf-8")))
        usados = set(re.findall(r"var\((--[\w-]+)", self.css))
        self.assertEqual(sorted(usados - definidos), [])
        self.assertEqual(re.findall(r"[{;]\s*(--[\w-]+)\s*:", sin_comentarios(self.css)), [], "la hoja no define tokens propios")

    def test_boton_del_hero_alto_con_sombra_amarilla_y_estados(self):
        css = sin_comentarios(self.css)
        boton = re.search(r"\.vt-inicio \.vt-inicio__cta \.vt-btn--wa\{([^}]*)\}", css).group(1)
        alto = int(re.search(r"min-height:(\d+)px", boton).group(1))
        self.assertTrue(62 <= alto <= 66, alto)
        self.assertRegex(boton, r"box-shadow:\d+px \d+px 0 var\(--vt-tag\)")
        for estado in (":hover", ":active", ":focus-visible"):
            with self.subTest(estado=estado):
                self.assertIn(f".vt-inicio .vt-inicio__cta .vt-btn--wa{estado}", css)
        escritorio = css[css.index("@media (min-width:1024px)"):]
        alto = int(re.search(r"\.vt-inicio \.vt-inicio__cta \.vt-btn--wa\{[^}]*min-height:(\d+)px", escritorio).group(1))
        self.assertTrue(62 <= alto <= 66, alto)

    def test_objetivos_tactiles_foco_y_movimiento_reducido(self):
        css = sin_comentarios(self.css)
        self.assertGreaterEqual(css.count("min-height:44px"), 2)  # enlaces del hero y WhatsApp por servicio
        self.assertIn("@media (prefers-reduced-motion:reduce)", css)
        reducido = css[css.index("@media (prefers-reduced-motion:reduce)"):]
        self.assertRegex(reducido, r"\.vt-inicio \.vt-inicio__cta \.vt-btn--wa[^{]*\{[^}]*transition:none")
        # Solo se animan propiedades de composición (transform) y la sombra del botón; nunca layout.
        for transicion in re.findall(r"transition:([^;}]+)", css):
            for propiedad in re.findall(r"(?:^|,)\s*([a-z-]+)", transicion):
                self.assertIn(propiedad, ("transform", "box-shadow", "none"), transicion)

    def test_etiqueta_colgada_solo_en_escritorio_y_medidor_reordenado_solo_en_celular(self):
        css = sin_comentarios(self.css)
        self.assertRegex(css, r"@media \(max-width:639px\)\{[^@]*\.vt-inicio \.vt-medidor__plano\{order:1\}")
        escritorio = css[css.index("@media (min-width:1024px)"):]
        self.assertIn(".vt-inicio .vt-portada .vt-etiqueta-x{", escritorio)
        # La etiqueta va siempre derecha: solo gira en el balanceo de entrada (Entrega 2), que termina sin rotación.
        for contextos, selector, cuerpo in reglas(self.css):
            if contextos != ("@keyframes vt-inicio-balanceo",) or selector == "100%":
                self.assertNotIn("rotate(", cuerpo, selector)

    def test_abierto_ahora_con_punto_y_texto(self):
        """El punto verde es decoración de la clase is-abierto, que terra.js solo pone junto con el texto."""
        self.assertIn(".vt-inicio .is-abierto::before{", self.css)
        self.assertIn("var(--vt-wa)", self.css)

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(datos), 6 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 2 * 1024)


if __name__ == "__main__":
    unittest.main()
