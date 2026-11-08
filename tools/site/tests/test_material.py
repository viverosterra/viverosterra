"""Plantilla de material (Etapa 2f): orden del spec §3.3, un H1, scripts, JSON-LD con el producto ligado a #negocio y
FAQPage igual a lo visible. MIGRADAS crece con cada tarea de migración hasta tener las cuatro páginas."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402

MIGRADAS = {"/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html",
            "/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",
            "/marmol-blanco-tampico": "marmol-blanco-tampico/index.html",
            "/piedra-bola-rio-tampico": "piedra-bola-rio-tampico/index.html"}
ORDEN = ('id="vt-h1"', 'id="vt-h-precio"', 'id="vt-h-usos"', 'id="vt-h-calc"', 'id="vt-h-entrega"', 'id="vt-h-faq"',
         'id="vt-cierre-titulo"', 'id="vt-h-otros"', 'id="vt-h-correo"')
# Mármol: los otros materiales antes del CTA final (sus miniaturas van antes de la foto del cierre en main).
ORDEN_MARMOL = ORDEN[:6] + ('id="vt-h-otros"', 'id="vt-cierre-titulo"', 'id="vt-h-correo"')
NEGOCIO = {"@id": f"{datos.SITIO}/#negocio"}
SITEMAP = paginas.PUBLIC / "sitemap.xml"


def html_de(ruta):
    return (paginas.PUBLIC / MIGRADAS[ruta]).read_text(encoding="utf-8")


def grafo(html):
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]


class MaterialTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        """Las cuatro: … entrega → (galería) → preguntas → (combinaciones, instalación) → CTA → otros materiales."""
        for ruta in MIGRADAS:
            html = html_de(ruta)
            orden = ORDEN_MARMOL if ruta == "/marmol-blanco-tampico" else ORDEN
            posiciones = [html.find(marca) for marca in orden]
            with self.subTest(ruta=ruta):
                self.assertNotIn(-1, posiciones)
                self.assertEqual(posiciones, sorted(posiciones))
                for extra in ('id="vt-h-combina"', 'id="vt-h-instalacion"'):
                    if extra in html:
                        self.assertLess(html.find('id="vt-h-faq"'), html.find(extra))
                        self.assertLess(html.find(extra), html.find('id="vt-cierre-titulo"'))

    def test_un_h1_sin_css_viejo_y_con_sus_scripts(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(len(re.findall(r"<h1\b", html)), 1)
                for viejo in ("tailwind.css", "design-system.css", "servicios.css", "legacy-fixes", "fonts.googleapis"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<script src="/js/vt-materiales.js" defer></script>', html)
                self.assertIn('<script src="/js/vt-b2b.js" defer></script>', html)

    def test_producto_ligado_al_negocio_sin_existencias(self):
        """Product solo con precio de datos.py (tierra negra y tezontle), con UnitPriceSpecification y seller #negocio;
        mármol y piedra bola, sin Product (no tienen precio)."""
        for ruta in MIGRADAS:
            productos = [n for n in grafo(html_de(ruta)) if n["@type"] == "Product"]
            with self.subTest(ruta=ruta):
                self.assertNotIn("InStock", json.dumps(productos))
                self.assertEqual(len(productos), 0 if ruta in ("/marmol-blanco-tampico", "/piedra-bola-rio-tampico") else 1)
                for producto in productos:
                    ofertas = producto["offers"] if isinstance(producto["offers"], list) else [producto["offers"]]
                    for o in ofertas:
                        self.assertEqual(o["seller"], NEGOCIO)
                        self.assertEqual(o["priceSpecification"]["@type"], "UnitPriceSpecification")
        tierra = next(n for n in grafo(html_de("/tierra-negra-vegetal-tampico")) if n["@type"] == "Product")
        self.assertEqual([(o["priceSpecification"]["price"], o["priceSpecification"]["unitText"]) for o in tierra["offers"]],
                         [(datos.PRECIOS["tierra_negra_costal"], "costal"), (datos.PRECIOS["tierra_negra_m3"], "m³")])
        tezontle = next(n for n in grafo(html_de("/tezontle-rojo-tampico")) if n["@type"] == "Product")["offers"]
        self.assertEqual(tezontle["priceSpecification"], {"@type": "UnitPriceSpecification", "priceCurrency": "MXN",
                                                          "unitText": "costal", "minPrice": datos.PRECIOS["tezontle_costal"]})
        self.assertNotIn("price", tezontle)

    def test_webpage_ligado_al_negocio(self):
        for ruta in MIGRADAS:
            url = f"{datos.SITIO}{ruta}"
            with self.subTest(ruta=ruta):
                self.assertIn({"@type": "WebPage", "@id": url, "url": url, "about": NEGOCIO, "publisher": NEGOCIO},
                              grafo(html_de(ruta)))

    def test_site_name_y_twitter_card(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn('<meta property="og:site_name" content="Viveros Terra">', html)
                self.assertIn('<meta name="twitter:card" content="summary_large_image">', html)
                self.assertNotIn("$250", " ".join(re.findall(r'<meta name="twitter:[^>]*>', html)))
        marmol = html_de("/marmol-blanco-tampico")
        self.assertIn('<meta name="twitter:title" content="Mármol Blanco para Jardín Tampico · Viveros Terra">', marmol)
        self.assertNotIn("gratis", " ".join(re.findall(r'<meta name="twitter:[^>]*>', marmol)))

    def test_sitemap_con_la_fecha_de_la_revision(self):
        mapa = SITEMAP.read_text(encoding="utf-8")
        for ruta in MIGRADAS:
            with self.subTest(ruta=ruta):
                self.assertIn(f"<loc>{datos.SITIO}{ruta}</loc><lastmod>2026-11-08</lastmod>", mapa)

    def test_hoja_de_materiales(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn('<body class="vt-pagina vt-materiales">', html)
                self.assertIn("/css/terra-materiales.", html)

    def test_faqpage_igual_a_lo_visible(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            faq = next(n for n in grafo(html) if n["@type"] == "FAQPage")
            visibles = [paridad.texto(s) for s in re.findall(r"<summary>(.*?)</summary>", paridad.principal(html), re.S)]
            with self.subTest(ruta=ruta):
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)


if __name__ == "__main__":
    unittest.main()
