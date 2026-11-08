"""404.html: noindex, buscador de servicios y enlaces que existen."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402
from plantillas import no_encontrada  # noqa: E402

K = generar.cargar("no_encontrada").CONTENIDO


class NoEncontradaTest(unittest.TestCase):
    def setUp(self):
        self.html = no_encontrada.render(K)

    def test_archivo_en_la_raiz_de_public_y_noindex(self):
        self.assertEqual(next(f for f in generar.PAGINAS if f[0] == "/404")[1], "404.html")
        self.assertEqual(K["meta"]["robots"], "noindex, follow")

    def test_buscador_con_etiqueta_y_lista_sin_js(self):
        self.assertIn('<label for="vt-buscar-404">', self.html)
        self.assertGreaterEqual(self.html.count("data-vt-servicio-404"), 12)
        self.assertIn('<script src="/js/vt-404.js" defer></script>', self.html)

    def test_todo_servicio_enlaza_a_una_pagina_real(self):
        for _texto, href in K["servicios"]:
            with self.subTest(href=href):
                archivo = paginas.PUBLIC / href.strip("/")
                self.assertTrue((archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file())

    def test_no_entra_al_sitemap(self):
        self.assertNotIn("/404<", (paginas.PUBLIC / "sitemap.xml").read_text(encoding="utf-8"))

    def test_un_h1(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)


if __name__ == "__main__":
    unittest.main()
