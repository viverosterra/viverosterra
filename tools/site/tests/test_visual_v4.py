"""Plan visual V4 (2026-11-11, docs/ux/2026-11/plan-mejoras-visuales.md): fotos. Portada de cada artículo con la foto de
su tarjeta del índice del blog (decisión del dueño), con copia de 640 px para celular, y un solo marco para las fotos de
especie de las páginas de plantas y del catálogo."""
import re
import unittest
from pathlib import Path

from contenido import articulo, blog_indice

PUBLIC = Path(__file__).resolve().parents[3] / "public"


def _articulo(slug):
    return (PUBLIC / "blog" / slug / "index.html").read_text(encoding="utf-8")


def _fotos_indice():
    fotos = {}
    for s in blog_indice.CONTENIDO["secciones"]:
        for t in s["tarjetas"]:
            if t.get("foto"):
                fotos.setdefault(t["href"].rstrip("/").removeprefix("/blog/"), t["foto"]["src"])
    return fotos


class VisualV4Test(unittest.TestCase):
    def test_portada_es_la_foto_del_indice_y_nunca_otra(self):
        fotos = _fotos_indice()
        self.assertGreater(len(articulo.PORTADAS), 15)
        for slug in articulo.CLAVES:
            with self.subTest(slug=slug):
                html = _articulo(slug)
                portada = re.search(r'<figure class="vt-art__portada"><img src="([^"]+)"', html)
                if slug in articulo.PORTADAS:
                    self.assertEqual(portada.group(1), fotos[slug])
                    self.assertEqual(html.count(f'src="{fotos[slug]}"'), 1, "la portada no se repite en el cuerpo")
                else:
                    self.assertIsNone(portada)

    def test_sin_portada_si_no_hay_foto_en_el_indice(self):
        fotos = _fotos_indice()
        for slug in articulo.PORTADAS:
            self.assertIn(slug, fotos)

    def test_portada_es_el_lcp_con_copia_movil(self):
        for slug, f in articulo.PORTADAS.items():
            with self.subTest(slug=slug):
                html = _articulo(slug)
                if f.get("src_movil"):
                    self.assertGreater(int(f["ancho"]), articulo.UMBRAL_COPIA, "nunca se agranda una foto")
                    self.assertTrue((PUBLIC / f["src_movil"].lstrip("/")).exists())
                    self.assertIn(f'<link rel="preload" as="image" href="{f["src"]}" imagesrcset="{f["src_movil"]} 640w', html)
                else:
                    self.assertIn(f'<link rel="preload" as="image" href="{f["src"]}" fetchpriority="high">', html)
                self.assertRegex(html, r'class="vt-art__portada"><img [^>]*alt="" loading="eager" fetchpriority="high"')
                self.assertEqual(html.count('fetchpriority="high"'), 2, "solo la precarga y la portada")

    def test_marco_unico_en_fotos_de_especie(self):
        css = (PUBLIC / "css" / "terra-plantas.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.vt-plantas \.vt-esp__foto\{[^}]*border:1px solid var\(--vt-line\)[^}]*background:var\(--vt-card\)")
        self.assertRegex(css, r"\.vt-plantas \.vt-esp__foto img\{[^}]*aspect-ratio:4/5")


if __name__ == "__main__":
    unittest.main()
