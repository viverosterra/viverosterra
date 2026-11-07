import re
import unittest
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3] / "public"
TERRA = PUBLIC / "css" / "terra.css"
CSS_VIEJOS = ("design-system.css", "tailwind.css", "servicios.css", "tienda-pasto.css")


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
                 ("--vt-tag-ink", "--vt-tag"), ("--vt-field-deep", "--vt-field-100")]
        for texto, fondo in pares:
            with self.subTest(par=(texto, fondo)):
                self.assertGreaterEqual(contraste(t[texto], t[fondo]), 4.5)

    def test_presupuesto(self):
        self.assertLess(len(self.css.encode("utf-8")), 30 * 1024)

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
        self.assertEqual(sorted(clases(self.css) & viejas), [])


if __name__ == "__main__":
    unittest.main()
