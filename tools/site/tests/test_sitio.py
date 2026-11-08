"""Pruebas sobre todo public/: shell canónico sin deriva, landmarks, medición y shell viejo retirado."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402

PUBLIC = paginas.PUBLIC
PAGINAS = {p: p.read_text(encoding="utf-8") for p in shell.paginas_html()}
ENLACE_CONTACTO_RE = re.compile(r'<a\b[^>]*\bhref="(?:https://wa\.me/|https://api\.whatsapp\.com/|tel:)[^"]*"[^>]*>')
VIEJOS = (
    ("menú terra-nav", r'<nav class="terra-nav"'),
    ("header de la tienda", r'<header class="site-header"'),
    ("pie de la tienda", r'class="site-footer"'),
    ("botón flotante", r'class="[^"]*\bwa-float\b'),
    ("botón flotante de plantas", r'<a\b[^>]*class="fab"'),
    ("botón de menú viejo", r'id="menu-btn"'),
    ("barra móvil vieja de la home", r'class="vt-stickybar"'),
    ("nav-scroll.js", r"nav-scroll\.js"),
    ("eventos sueltos clic_*", r"'clic_"),
)


def nombre(path):
    return str(path.relative_to(PUBLIC))


class ShellEnTodoElSitioTest(unittest.TestCase):
    def test_109_paginas_con_contexto(self):
        self.assertEqual(len(PAGINAS), 109)
        for path in PAGINAS:
            paginas.contexto(paginas.ruta_de(path))

    def test_shell_canonico_sin_deriva(self):
        urls = activos.urls()
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(shell.aplicar(html, paginas.ruta_de(path), urls), html)

    def test_un_main_un_skip_link_un_header_del_shell(self):
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(len(re.findall(r"<main\b", html)), 1)
                self.assertIn('<main id="main"', html)
                self.assertEqual(html.count('href="#main"'), 1)
                self.assertEqual(html.count('<header class="vt-head"'), 1)
                self.assertEqual(html.count('<footer class="vt-foot">'), 1)

    def test_gtag_una_sola_vez(self):
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(html.count("googletagmanager.com/gtag/js?id=G-RMZCVJ734M"), 1)
                self.assertEqual(html.count("gtag('config','G-RMZCVJ734M')"), 1)

    def test_shell_viejo_retirado(self):
        for path, html in PAGINAS.items():
            for descripcion, patron in VIEJOS:
                with self.subTest(pagina=nombre(path), viejo=descripcion):
                    self.assertIsNone(re.search(patron, html))

    def test_todo_enlace_de_whatsapp_o_telefono_lleva_data_cta(self):
        for path, html in PAGINAS.items():
            sin_cta = [e for e in ENLACE_CONTACTO_RE.findall(html) if "data-cta=" not in e]
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(sin_cta, [])

    def test_assets_con_hash_existen_y_solo_queda_la_generacion_anterior(self):
        # activos.publicar() conserva la copia actual y la que sirve producción (tools/site/activos.json).
        for url in activos.urls().values():
            self.assertTrue((PUBLIC / url.lstrip("/")).is_file(), url)
        for carpeta, patron in (("css", "terra.*.css"), ("js", "terra.*.js")):
            with self.subTest(patron=patron):
                self.assertLessEqual(len(list((PUBLIC / carpeta).glob(patron))), 2)


if __name__ == "__main__":
    unittest.main()
