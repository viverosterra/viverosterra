"""terra-inicio.css: hoja propia de la home (Medidor en celular, WhatsApp por servicio, CTA de sección y movimiento).
Todo bajo .vt-inicio, solo con tokens de terra.css (sin colores literales ni !important) y presupuesto propio. El hero
salió de esta hoja el 2026-11-10 (Entrega A de experiencia): es el componente común y vive en terra.css."""
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

    # Entrega A de experiencia (2026-11-10): el hero es el componente común y su CSS vive en terra.css; sus reglas (botón
    # alto con sombra amarilla y estados, enlaces de 44 px, etiqueta colgada, cortes de la revisión de diseño) se prueban
    # en tests/test_portada.py. Aquí queda lo propio de la home.
    def test_el_hero_ya_no_esta_en_esta_hoja(self):
        css = sin_comentarios(self.css)
        for clase in ("vt-inicio__cta", "vt-inicio__lema", "vt-inicio__trato", "vt-portada__cta", "vt-portada__grid"):
            with self.subTest(clase=clase):
                self.assertNotIn(clase, css)

    def test_objetivos_tactiles_y_solo_transform_en_transiciones(self):
        css = sin_comentarios(self.css)
        self.assertGreaterEqual(css.count("min-height:44px"), 2)  # WhatsApp por servicio y enlace a las reseñas
        # Solo se animan propiedades de composición; nunca layout.
        for transicion in re.findall(r"transition:([^;}]+)", css):
            for propiedad in re.findall(r"(?:^|,)\s*([a-z-]+)", transicion):
                self.assertIn(propiedad, ("transform", "box-shadow", "none"), transicion)

    def test_medidor_reordenado_solo_en_celular_y_etiqueta_siempre_derecha(self):
        css = sin_comentarios(self.css)
        self.assertRegex(css, r"@media \(max-width:639px\)\{[^@]*\.vt-inicio \.vt-medidor__plano\{order:1\}")
        # La etiqueta va siempre derecha: solo gira en el balanceo de entrada (Entrega 2), que termina sin rotación.
        for contextos, selector, cuerpo in reglas(self.css):
            if contextos != ("@keyframes vt-inicio-balanceo",) or selector == "100%":
                self.assertNotIn("rotate(", cuerpo, selector)

    def test_abierto_ahora_con_punto_y_texto(self):
        """El punto verde es decoración de la clase is-abierto, que terra.js solo pone junto con el texto. Desde la
        Entrega A de experiencia la regla es de todo el sitio (terra.css): la línea de confianza va en todos los héroes."""
        terra = (CSS / "terra.css").read_text(encoding="utf-8")
        self.assertIn(".vt-pagina .is-abierto::before{", terra)
        self.assertIn("background:var(--vt-wa)", terra[terra.index(".vt-pagina .is-abierto::before{"):][:200])

    def test_presupuesto(self):
        datos = activos.minificar_css(self.css).encode("utf-8")
        # Con el hero en terra.css (Entrega A de experiencia, 2026-11-10) la hoja baja de 8 KB a menos de 3 KB (antes:
        # tope de 8 KB y 2.5 KB con gzip).
        self.assertLess(len(datos), 3 * 1024)
        self.assertLess(len(gzip.compress(datos, mtime=0)), 1024)

    def test_cortes_de_la_revision_de_diseno_en_terra_css(self):
        """Los cortes de la revisión de diseño del hero (2026-11-09) siguen, ahora en terra.css y para todo el sitio."""
        css = sin_comentarios((CSS / "terra.css").read_text(encoding="utf-8"))
        for corte in ("@media (min-width:1024px) and (max-height:820px){",
                      "@media (min-width:1024px) and (max-width:1279px),(min-width:1024px) and (max-height:820px){",
                      "@media (min-width:768px) and (max-width:1023px){",
                      "@media (max-width:359px),(max-width:559px) and (max-height:660px){",
                      "@media (min-width:560px) and (max-width:1023px){.vt-portada__cta .vt-btn{max-width:420px}}"):
            with self.subTest(corte=corte):
                self.assertIn(corte, css)
        self.assertNotIn(".vt-bar", sin_comentarios(self.css), "la transición de la barra ya se apaga en terra.css para todo el sitio")


if __name__ == "__main__":
    unittest.main()
