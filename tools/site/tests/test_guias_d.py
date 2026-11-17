"""Entrega D del SEO nacional (2026-11-16): guías de la tienda (azotea, alberca, ancho del rollo, sintético o natural)."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import rollos  # noqa: E402
from contenido import blog_clusters  # noqa: E402
from contenido import guias_tienda as g  # noqa: E402

PUBLIC = Path(paginas.PUBLIC)
RUTAS = tuple(f"/pasto-sintetico/{k}" for k in g.CLAVES)


def html(ruta):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def plano(texto):
    principal = re.search(r"<main\b.*?</main>", texto, re.S).group(0)
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", principal)))


class GuiasTest(unittest.TestCase):
    def test_paginas_nuevas_registradas(self):
        rutas = {r for r, *_ in generar.PAGINAS}
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
        hub = html("/pasto-sintetico")
        for ruta in RUTAS:
            with self.subTest(ruta=ruta):
                self.assertIn(ruta, rutas)
                self.assertIn(ruta, generar.NUEVAS)
                self.assertIn(f"https://www.viverosterra.com{ruta}</loc>", sitemap)
                self.assertIn(ruta, llms)
                self.assertIn(f'href="{ruta}"', hub)

    def test_titulos_descripciones_y_sin_palabras_prohibidas(self):
        for ruta in RUTAS:
            texto = html(ruta)
            titulo = html_mod.unescape(re.search(r"<title>(.*?)</title>", texto).group(1))
            descripcion = html_mod.unescape(re.search(r'name="description" content="([^"]*)"', texto).group(1))
            with self.subTest(ruta=ruta):
                self.assertLessEqual(len(titulo), 60)
                self.assertLessEqual(len(descripcion), 155)
                self.assertNotRegex(plano(texto).lower(), r"gratis|sin costo|más vendid|oasis")
                self.assertNotIn("Cafetería en el centro de Tampico", texto)
                self.assertIn('id="vt-preguntas"', texto)

    def test_azotea_con_el_peso_de_cada_ficha(self):
        cuerpo = plano(html("/pasto-sintetico/azotea"))
        for m in data.MODELOS:
            with self.subTest(modelo=m["slug"]):
                self.assertIn(f"{m['nombre']} {m['mm']} mm {m['peso']} g/m² {g.num(m['peso_num'] * 50 / 1000)} kg", cuerpo)
        self.assertIn("Toscana 18 18 mm 950 g/m² 47.5 kg", cuerpo)
        self.assertIn("Pesa de 0.95 a 2.1 kg por m²", cuerpo)
        self.assertIn("pesa de 47.5 kg (Toscana 18) a 105 kg (Mónaco 35 y Bali 35)", cuerpo)

    def test_ancho_calculado_como_la_calculadora(self):
        for largo, ancho in rollos.MEDIDAS_COMUNES:
            r = rollos.corte(largo, ancho)
            with self.subTest(medida=(largo, ancho)):
                self.assertEqual(g.tiras(largo, ancho, 2), (r["tiras"], r["m2_tiras"]))
        cuerpo = plano(html("/pasto-sintetico/ancho-del-rollo"))
        self.assertIn("8 × 6 m 48 m² 48 m² · 2 uniones 58.56 m² · 1 unión", cuerpo)
        self.assertIn("En 6 de las 7 medidas, el rollo de 3.66 m deja menos juntas", cuerpo)
        self.assertIn("En 5 de las 7 medidas sobra menos con el de 2 m", cuerpo)
        self.assertNotIn("3.7 m", cuerpo)

    def test_sin_promesas_sin_dato(self):
        alberca = plano(html("/pasto-sintetico/alberca"))
        self.assertIn("Las fichas no traen una prueba de cloro, así que no te lo prometemos", alberca)
        azotea = plano(html("/pasto-sintetico/azotea"))
        self.assertIn("no lo podemos saber a distancia", azotea)
        self.assertNotRegex(azotea, r"\d+ ?kg/m²")  # nunca la carga que aguanta una azotea

    def test_vs_natural_con_garantias_y_precio_de_los_datos(self):
        cuerpo = plano(html("/pasto-sintetico/vs-natural"))
        self.assertIn("Garantía de fábrica de 3 a 8 años según el modelo", cuerpo)
        self.assertIn(f"Desde ${data.landed_m2(min(data.MODELOS, key=lambda m: m['rollo']), 'A')}/m² puesto", cuerpo)
        self.assertIn('href="/blog/pasto-sintetico-vs-natural-tampico"', html("/pasto-sintetico/vs-natural"))

    def test_los_articulos_de_sintetico_enlazan_su_guia(self):
        for slug, (_texto, ruta) in blog_clusters.GUIA_D.items():
            with self.subTest(slug=slug):
                self.assertIn(f'href="{ruta}"', html(f"/blog/{slug}"))

    def test_faq_en_json_ld(self):
        for ruta in RUTAS:
            grafo = [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html(ruta), re.S)
                     for n in json.loads(b).get("@graph", [])]
            with self.subTest(ruta=ruta):
                self.assertTrue(any(n.get("@type") == "FAQPage" for n in grafo))


if __name__ == "__main__":
    unittest.main()
