"""Plantilla de artículo (Etapa 2h): orden de la spec, sin marcado viejo, índice que llega a ids reales, una sola etiqueta de
producto y un CTA a una landing."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402
from contenido import articulo, blog_clusters  # noqa: E402

VIEJO = ("/css/tailwind.css", "/css/design-system.css", "fonts.googleapis", "sendWA", "window.open(", "faq-btn", "<style")


def html_de(slug):
    return paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8")


class ArticuloTest(unittest.TestCase):
    def test_un_h1_y_sin_marcado_viejo(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            with self.subTest(slug=slug):
                self.assertEqual(len(re.findall(r"<h1\b", paridad.principal(html))), 1)
                for viejo in VIEJO:
                    self.assertNotIn(viejo, html)

    def test_orden_de_secciones(self):
        html = html_de("palma-areca-tampico")
        orden = ['id="vt-h1"', "vt-art__meta", 'id="respuesta"', 'id="que-es"', 'id="preguntas"', "vt-art__sigue",
                 "vt-art__producto", "vt-art__rel"]
        posiciones = [html.index(s) for s in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_indice_llega_a_ids_del_articulo(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            ids = set(re.findall(r'\sid="([^"]+)"', html))
            indice = re.search(r'<nav class="vt-art__indice".*?</nav>', html, re.S).group(0)
            enlaces = re.findall(r'href="#([^"]+)"', indice)
            with self.subTest(slug=slug):
                self.assertGreater(len(enlaces), 1)
                self.assertEqual([e for e in enlaces if e not in ids], [])

    def test_una_etiqueta_y_cta_a_landing(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            landing = blog_clusters.de(slug)["landing"][0]
            with self.subTest(slug=slug):
                self.assertEqual(html.count('class="vt-etiqueta"'), 1)
                self.assertIn(f'data-cta="blog:landing" href="{landing}"', html)

    def test_dos_o_tres_enlaces_contextuales_a_money_pages(self):
        for slug in articulo.CLAVES:
            enlaces = blog_clusters.de(slug)["enlaces"]
            with self.subTest(slug=slug):
                self.assertIn(len(enlaces), (2, 3))
                self.assertEqual(len({h for _t, h in enlaces}), len(enlaces))

    def test_faqpage_igual_a_lo_visible(self):
        for slug in articulo.CLAVES:
            doc = articulo.pagina(slug).CONTENIDO
            html = html_de(slug)
            with self.subTest(slug=slug):
                self.assertEqual(paridad.principal(html).count("<summary>"), len(doc["faq"]))
                self.assertEqual(html.count('"@type":"Question"'), len(doc["faq"]))

    def test_blogs_de_precios_enlazan_a_precios(self):
        for slug in blog_clusters.A_PRECIOS:
            with self.subTest(slug=slug):
                self.assertTrue(any(h == "/precios" for _t, h in blog_clusters.de(slug)["enlaces"]))

    def test_todo_articulo_tiene_tema(self):
        self.assertEqual(sorted(blog_clusters.TEMA), sorted(articulo.CLAVES))


if __name__ == "__main__":
    unittest.main()
