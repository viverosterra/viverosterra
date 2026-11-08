import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


class LimpiezaTest(unittest.TestCase):
    def test_raiz_sin_copias_viejas(self):
        for nombre in ("index.html", "catalogo.html", "catalogo", "cuestionario.html", "cuestionario", "scripts", "src",
                       "tailwind.config.js"):
            with self.subTest(nombre=nombre):
                self.assertFalse((RAIZ / nombre).exists())
        sueltas = sorted(p.name for ext in ("png", "jpg", "webp", "svg") for p in RAIZ.glob(f"*.{ext}"))
        self.assertEqual(sueltas, [])

    def test_js_sin_uso_retirado(self):
        self.assertFalse((RAIZ / "public" / "js" / "nav-scroll.js").exists())

    def test_tienda_pasto_css_y_html_de_tools_pasto_retirados(self):
        """Etapa 2g: /precios y las 6 zonas eran las últimas páginas con tienda-pasto.css y con HTML de tools/pasto."""
        self.assertFalse((RAIZ / "public" / "css" / "tienda-pasto.css").exists())
        for modulo in ("common.py", "precios.py", "zonas.py"):
            with self.subTest(modulo=modulo):
                self.assertFalse((RAIZ / "tools" / "pasto" / modulo).exists())
        con_hoja = [str(p.relative_to(RAIZ)) for p in (RAIZ / "public").rglob("*.html")
                    if "tienda-pasto.css" in p.read_text(encoding="utf-8")]
        self.assertEqual(con_hoja, [])

    def test_ds_store_y_pycache_fuera_de_git(self):
        versionados = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
        self.assertNotIn(".DS_Store", versionados)
        self.assertNotIn("__pycache__", versionados)


if __name__ == "__main__":
    unittest.main()
