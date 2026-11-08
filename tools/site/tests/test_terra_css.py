import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"
TERRA = PUBLIC / "css" / "terra.css"
CSS_VIEJOS = ("design-system.css", "tailwind.css", "servicios.css", "tienda-pasto.css")
# Clases que crea public/js/vt-simulador.js (las mismas en servicios.css). En terra.css solo aparecen bajo .vt-sim, que
# ninguna página vieja tiene, así que no pueden alterar el simulador viejo.
CLASES_DEL_SIMULADOR = {"sim-plan", "sim-plan__name", "sim-plan__amt", "sim-plan__sep", "sim-plan__more", "is-selected",
                        "is-disabled"}


def sin_comentarios(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def clases(css):
    """Nombres de clase de una hoja (sin comentarios, sin url(...) y sin números como .8125rem)."""
    limpio = re.sub(r"url\([^)]*\)", "", sin_comentarios(css))
    return {m.replace("\\", "") for m in re.findall(r"\.(-?[_a-zA-Z](?:\\.|[\w-])*)", limpio)}


def tokens(css):
    bloque = re.search(r":root\{(.*?)\}", sin_comentarios(css), re.S).group(1)
    return dict(re.findall(r"(--vt-[\w-]+):\s*([^;]+);", bloque))


def luminancia(hexa):
    canales = [int(hexa.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lineal = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lineal[0] + 0.7152 * lineal[1] + 0.0722 * lineal[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


class TerraCssTest(unittest.TestCase):
    def setUp(self):
        self.css = TERRA.read_text(encoding="utf-8")

    def test_todo_selector_es_del_shell(self):
        css = re.sub(r"@font-face\{[^}]*\}", "", sin_comentarios(self.css))
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", css):
            selector = selector.strip()
            if selector.startswith("@media") or selector == ":root":
                continue
            ajenos += [p.strip() for p in selector.split(",") if ".vt-" not in p]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_fuera_de_root(self):
        css = re.sub(r":root\{[^}]*\}", "", sin_comentarios(self.css))
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])

    def test_tokens_del_hibrido(self):
        t = tokens(self.css)
        esperados = {"--vt-bone": "#FAF7EF", "--vt-bone-2": "#F1ECDF", "--vt-ink": "#161A14", "--vt-field": "#1E4D2B",
                     "--vt-field-deep": "#12301B", "--vt-tag": "#F2D24B", "--vt-soil": "#6B4226", "--vt-wa": "#25D366"}
        for nombre, valor in esperados.items():
            with self.subTest(token=nombre):
                self.assertEqual(t[nombre], valor)

    def test_contraste_aa_por_par_de_tokens(self):
        t = tokens(self.css)
        pares = [("--vt-ink", "--vt-bone"), ("--vt-ink-2", "--vt-bone"), ("--vt-muted", "--vt-bone"),
                 ("--vt-muted", "--vt-card"), ("--vt-field", "--vt-bone"), ("--vt-card", "--vt-field"),
                 ("--vt-on-dark", "--vt-ink"), ("--vt-on-dark-2", "--vt-ink"), ("--vt-tag", "--vt-ink"),
                 ("--vt-tag-ink", "--vt-tag"), ("--vt-field-deep", "--vt-field-100"),
                 # componentes del cuerpo (Etapa 2)
                 ("--vt-soil", "--vt-bone"), ("--vt-soil", "--vt-bone-2"), ("--vt-soil", "--vt-card"),
                 ("--vt-muted", "--vt-bone-2"), ("--vt-ink-2", "--vt-bone-2"), ("--vt-card", "--vt-soil"),
                 ("--vt-on-dark-2", "--vt-field-deep"), ("--vt-tag", "--vt-field-deep"), ("--vt-ink", "--vt-field-100")]
        for texto, fondo in pares:
            with self.subTest(par=(texto, fondo)):
                self.assertGreaterEqual(contraste(t[texto], t[fondo]), 4.5)

    def test_presupuesto(self):
        # Spec §8.2: meta de 10 KB con gzip. Desde la Etapa 2 terra.css también trae los componentes del cuerpo y
        # sustituye, en cada página migrada, ~70 KB de CSS viejo (tailwind, design-system, servicios y <style>).
        # Se mide la copia publicada (activos.minificar_css: sin comentarios ni sangría), que es la que se transfiere.
        datos = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(gzip.compress(datos, mtime=0)), 10 * 1024)
        self.assertLess(len(datos), 48 * 1024)

    def test_cotizadores_de_empresas(self):
        """Etapa 2d: [hidden] gana a .vt-btn (el botón "Agregar otra especie" sale oculto sin JS) y el select del armador
        de palmas usa el mismo control que los campos."""
        self.assertIn(".vt-b2b [hidden]{display:none}", self.css)
        self.assertIn(".vt-control select{", self.css)
        self.assertIn("@media (min-width:1024px){.vt-b2b{grid-template-columns:7fr 5fr", self.css)

    def test_fuentes_referenciadas_existen(self):
        urls = re.findall(r'url\("(/fonts/[^"]+)"\)', self.css)
        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertTrue((PUBLIC / url.lstrip("/")).is_file(), url)

    def test_clases_del_shell_no_chocan_con_las_viejas(self):
        viejas = set()
        for nombre in CSS_VIEJOS:
            viejas |= clases((PUBLIC / "css" / nombre).read_text(encoding="utf-8"))
        for pagina in PUBLIC.rglob("*.html"):
            for estilo in re.findall(r"<style[^>]*>(.*?)</style>", pagina.read_text(encoding="utf-8"), re.S):
                viejas |= clases(estilo)
        self.assertEqual(sorted((clases(self.css) - CLASES_DEL_SIMULADOR) & viejas), [])
        for regla in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            if re.search(r"\.(?:sim-plan|is-selected|is-disabled)\b", regla):
                with self.subTest(selector=regla.strip()):
                    self.assertTrue(all(".vt-sim " in parte for parte in regla.split(",")))

    def regla(self, selector):
        """Cuerpo de la primera regla cuyo selector es exactamente `selector`."""
        css = sin_comentarios(self.css)
        m = re.search(r"(?:^|[{}\n])" + re.escape(selector) + r"\{([^}]*)\}", css)
        self.assertIsNotNone(m, selector)
        return m.group(1)

    def test_panel_solo_se_muestra_con_aria_expanded(self):
        css = sin_comentarios(self.css)
        for selector in re.findall(r"([^{}]+)\{[^{}]*display:block", css):
            for parte in selector.split(","):
                if parte.strip().endswith(".vt-nav__panel"):
                    with self.subTest(selector=parte.strip()):
                        self.assertIn('[aria-expanded="true"]', parte)
                        self.assertNotIn(":hover", parte)
                        self.assertNotIn(":focus-within", parte)

    def test_barra_oculta_no_se_alcanza_con_tab(self):
        cuerpo = self.regla(".vt-bar.is-oculta")
        self.assertIn("visibility:hidden", cuerpo)
        self.assertIn("visibility 0s", cuerpo)

    def test_borde_del_burger_contrasta_3_a_1(self):
        token = re.search(r"border:1px solid var\((--vt-[\w-]+)\)", self.regla(".vt-burger")).group(1)
        self.assertGreaterEqual(contraste(tokens(self.css)[token], tokens(self.css)["--vt-bone"]), 3)

    def test_menu_movil_usa_dvh_con_respaldo(self):
        cuerpo = self.regla(".vt-mmenu")
        self.assertLess(cuerpo.index("100vh"), cuerpo.index("100dvh"))

    def test_enlace_del_menu_movil_subrayado(self):
        self.assertIn("text-decoration:underline", self.regla(".vt-mmenu__meta a"))

    def test_area_del_boton_de_submenu_de_44(self):
        self.assertIn("inset:-10px -20px -10px 0", self.regla(".vt-nav__exp::before"))

    def test_barra_de_56_mas_area_segura(self):
        self.assertEqual(tokens(self.css)["--vt-bar-h"], "56px")
        self.assertIn("calc(var(--vt-bar-h) + env(safe-area-inset-bottom))", self.regla(".vt-bar"))

    def test_componentes_del_cuerpo_presentes(self):
        for selector in (".vt-pagina", ".vt-portada", ".vt-etiqueta", ".vt-datos", ".vt-medidor", ".vt-tabla",
                         ".vt-pasos", ".vt-nota", ".vt-faq summary", ".vt-cierre", ".vt-sim .sim-plan",
                         ".vt-modo__precio .vt-modo__mes"):
            with self.subTest(selector=selector):
                self.regla(selector)
        for token in ("--vt-text-h1", "--vt-text-h2", "--vt-text-h3", "--vt-text-precio", "--vt-space-section"):
            self.assertIn(token, tokens(self.css))


if __name__ == "__main__":
    unittest.main()
