"""Plantilla de artículo (Etapa 2h): orden de la spec, sin marcado viejo, índice que llega a ids reales, una sola etiqueta de
producto y un CTA a una landing."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
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

    def grafo(self, slug):
        bloque = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_de(slug), re.S)
        return next(json.loads(b)["@graph"] for b in bloque if "@graph" in b)

    def test_autor_y_publisher_del_jsonld(self):
        for slug in articulo.CLAVES:
            nodo = next(n for n in self.grafo(slug) if n["@type"] == "Article")
            with self.subTest(slug=slug):
                # SEO fase 1: autor y publisher son la entidad única por @id (antes el autor era una Organization
                # suelta con el nombre del equipo); la firma visible sigue siendo datos.AUTOR_BLOG.
                self.assertEqual(nodo["author"], {"@id": f"{datos.SITIO}/#negocio"})
                self.assertEqual(nodo["publisher"], {"@id": f"{datos.SITIO}/#negocio"})
                self.assertIn(f"<b>Por</b> {datos.AUTOR_BLOG}", html_de(slug))

    def test_migas_del_jsonld_iguales_a_las_visibles(self):
        for slug in articulo.CLAVES:
            migas = next((n for n in self.grafo(slug) if n["@type"] == "BreadcrumbList"), None)
            visibles = re.findall(r"<li[^>]*>(?:<a [^>]+>)?(.*?)(?:</a>)?</li>",
                                  re.search(r'<nav class="vt-crumbs".*?</nav>', html_de(slug), re.S).group(0))
            with self.subTest(slug=slug):
                self.assertIsNotNone(migas)
                self.assertEqual([i["name"] for i in migas["itemListElement"]], [paridad.texto(v) for v in visibles])

    def test_indice_movil_cerrado_tras_la_respuesta(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            with self.subTest(slug=slug):
                self.assertEqual(html.count('<details class="vt-art__toc">'), 1)
                inicio = html.index('<details class="vt-art__toc">')
                self.assertLess(inicio, html.index('<h2 id="', inicio))
                if 'id="respuesta"' in html:
                    self.assertLess(html.index('id="respuesta"'), inicio)

    def test_cta_a_media_lectura_una_vez_y_antes_del_tercer_h2(self):
        for slug in articulo.CLAVES:
            html = html_de(slug)
            href = blog_clusters.de(slug)["landing"][0]
            cuerpo = re.search(r'<article class="vt-art__cuerpo".*?</article>', html, re.S).group(0)
            pos = cuerpo.index('class="vt-art__medio"')
            h2 = [m.start() for m in re.finditer(r'<h2 id="(?!preguntas)', cuerpo)]
            with self.subTest(slug=slug):
                self.assertEqual(html.count('data-cta="blog:medio"'), 1)
                self.assertEqual(html.count('data-cta="blog:margen"'), 1)
                self.assertIn(f'data-cta="blog:medio" href="{href}"', html)
                self.assertIn(f'data-cta="blog:margen" href="{href}"', html)
                self.assertGreater(pos, h2[min(1, len(h2) - 1)])
                if len(h2) > 2:
                    self.assertLess(pos, h2[2])

    def test_etiqueta_de_servicio_y_sin_iva_en_cotizacion(self):
        for slug in articulo.CLAVES:
            tema = blog_clusters.de(slug)
            html = html_de(slug)
            codigo = "Servicio relacionado" if tema["tema"] in ("riego", "diseno", "mantenimiento") else "Producto relacionado"
            with self.subTest(slug=slug):
                self.assertIn(f"<span>{codigo}</span>", html)
                # SEO fase 0 (2026-11-10): "Con IVA" en el encabezado de la etiqueta cubre todos sus renglones; no va
                # si alguno es de pasto sin instalar, de palmas o de árboles (no llevan IVA) ni si se cotiza. Etapa 2i
                # (2026-11-08): tampoco en las etiquetas de plantas (palmas por cotización, banqueta, plantas, interior).
                con_iva = (tema["etiqueta"]["monto"] != datos.SEGUN_COTIZACION
                           and tema["tema"] not in ("pasto-natural", "palmas", "palmas-cotizacion", "arboles", "banqueta",
                                                    "plantas", "interior"))
                self.assertEqual("<span>Con IVA</span>" in html, con_iva)
                if tema["tema"] == "pasto-natural":
                    self.assertIn("<small>Instalado · desde</small><b>$120</b><span>/m² con IVA</span>", html)
                    self.assertIn("<span>Solo el pasto</span><b>$85 /m²</b>", html)

    def test_cierre_segun_el_tema_del_articulo(self):
        esperado = {"cesped-amarillo-tampico-causas-soluciones": "mantenimiento", "errores-pasto-san-agustin-tampico": "mantenimiento",
                    "cuando-regar-pasto-san-agustin-tampico": "mantenimiento", "jardin-en-macetas-terraza-tampico-guia": "plantas",
                    "como-medir-plantas-altura-cepellon": "plantas"}
        for slug in ("cuidados-palma-del-viajero-ravenala", "palma-washingtona-tampico", "palma-bismarckia-bismarckia-nobilis-tampico",
                     "palma-kerpis-howea-forsteriana-tampico", "palma-cola-de-zorro-wodyetia-bifurcata-tampico",
                     "palma-triangular-dypsis-decaryi-tampico"):
            esperado[slug] = "palmas-cotizacion"
            self.assertEqual(blog_clusters.de(slug)["etiqueta"]["monto"], datos.SEGUN_COTIZACION)
        for slug, tema in esperado.items():
            self.assertEqual(blog_clusters.de(slug)["tema"], tema, slug)
        self.assertEqual(blog_clusters.de("pasto-sintetico-vs-natural-tampico")["landing"][0], "/pasto-sintetico-tampico")

    def test_tablas_con_nombre_de_su_encabezado(self):
        self.assertIn('aria-label="Tabla: ', html_de("cuanto-cuesta-jardin-tampico-precios"))
        for slug in articulo.CLAVES:
            with self.subTest(slug=slug):
                self.assertNotIn('role="region" aria-label="Tabla"', html_de(slug))

    def test_indice_sin_repetidos_e_itemlist(self):
        html = paridad.archivo("/blog").read_text(encoding="utf-8")
        tarjetas = re.findall(r'<h3><a href="(/blog/[^"]+)"', html)
        self.assertEqual(len(tarjetas), len(set(tarjetas)))
        self.assertEqual(len(tarjetas), 54)
        # SEO fase 1: el Blog y la lista van en un solo @graph.
        lista = next(n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                     for n in json.loads(b).get("@graph", ()) if n.get("@type") == "ItemList")
        self.assertEqual([i["position"] for i in lista["itemListElement"]], list(range(1, 55)))
        self.assertEqual({i["url"] for i in lista["itemListElement"]}, {f"{datos.SITIO}{t}" for t in tarjetas})

    def test_todo_articulo_tiene_tema(self):
        self.assertEqual(sorted(blog_clusters.TEMA), sorted(articulo.CLAVES))


if __name__ == "__main__":
    unittest.main()
