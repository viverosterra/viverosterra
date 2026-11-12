"""SEO fase 2b (2026-11-11, docs/superpowers/plans/2026-11-10-seo-aeo-geo.md; mapa de palabras clave G3 y §4a):
/vivero-tampico pasa a la plantilla pilar en la misma URL, con el título y la descripción del mapa, ~1,200 palabras
hechas solo de datos.py, el WebPage que nombra #negocio, la misma foto de portada que main y enlaces de ida y vuelta con
/jardineria-ciudad-madero y la temporada de Nochebuenas; el pie la enlaza en todas las páginas con el domicilio; y
/politica-privacidad sigue fuera del índice y del sitemap, sin la dirección vieja (Obregón 601)."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import entidad  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402
import shell  # noqa: E402

PUBLIC = paginas.PUBLIC
RUTA = "/vivero-tampico"
URL = f"{datos.SITIO}{RUTA}"
# Del mapa de palabras clave (fila /vivero-tampico).
TITULO = "Vivero en Tampico y Cd. Madero: +200 Plantas | Viveros Terra"
DESCRIPCION = ("Vivero en Cd. Madero, frente a Walmart: más de 200 variedades de plantas, palmas y árboles. Lun a vie 9 a "
               "18 h, sáb 9 a 14 h. Ve cómo llegar y visítanos.")
# La foto de portada tal como estaba en main antes de la migración (regla del dueño: las fotos no se tocan).
FOTO_MAIN = ('<img src="/img/portadas/arboles-tampico-viveros-terra-sm.webp" srcset="/img/portadas/arboles-tampico-viveros-'
             'terra-sm.webp 560w, /img/portadas/arboles-tampico-viveros-terra.webp 960w" sizes="(min-width: 1024px) 540px, '
             '100vw" width="960" height="1280" loading="eager" fetchpriority="high" decoding="async" alt="Equipo de Viveros '
             'Terra sembrando un árbol en un jardín de Tampico">')
CATEGORIAS = ("/palmas-tropicales-tampico", "/plantas-para-jardin-tampico", "/plantas-de-interior-tampico",
              "/arboles-ornamentales-tampico", "/arboles-para-banqueta-tampico", "/catalogo")
PROHIBIDAS_RE = re.compile(r"(?i)\bgratis\b|\bsin costo\b|más vendid[oa]s?|\boasis\b|estacionamiento|"
                           r"\b\d+\s*(?:minutos|min\b|km\b|kilómetros)|visita sin costo|últimas piezas|solo hoy")
DIRECCION_VIEJA_RE = re.compile(r"(?i)obreg[oó]n\s*(?:no\.?\s*)?601")


def archivo(ruta):
    return PUBLIC / ruta.strip("/") / "index.html"


def html_de(ruta):
    return archivo(ruta).read_text(encoding="utf-8")


def texto(fragmento):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", fragmento, flags=re.S)
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def main_de(ruta):
    return re.search(r"<main\b.*</main>", html_de(ruta), re.S).group(0)


def grafo(ruta):
    bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_de(ruta), re.S).group(1)
    return json.loads(bloque)["@graph"]


def tipos(nodo):
    t = nodo.get("@type")
    return [t] if isinstance(t, str) else list(t or ())


class ViveroPilarTest(unittest.TestCase):
    def setUp(self):
        self.html = html_de(RUTA)
        self.main = main_de(RUTA)

    def test_misma_url_con_la_plantilla_pilar(self):
        fila = next(p for p in generar.PAGINAS if p[0] == RUTA)
        self.assertEqual(fila[1:], ("vivero-tampico/index.html", "pilar", "vivero"))
        self.assertFalse((Path(generar.__file__).parent / "plantillas" / "vivero.py").exists())
        self.assertIn(f'<link rel="canonical" href="{URL}">', self.html)
        self.assertIn('<meta name="robots" content="index, follow">', self.html)

    def test_titulo_y_descripcion_del_mapa(self):
        titulo = html_mod.unescape(re.search(r"<title>(.*?)</title>", self.html).group(1))
        descripcion = html_mod.unescape(re.search(r'<meta name="description" content="([^"]*)"', self.html).group(1))
        self.assertEqual(titulo, TITULO)
        self.assertLessEqual(len(titulo), 60)
        self.assertEqual(descripcion, DESCRIPCION)
        self.assertLessEqual(len(descripcion), 155)
        self.assertIn(datos.HORARIO, descripcion)

    def test_unas_1200_palabras_en_el_contenido(self):
        self.assertGreaterEqual(len(texto(self.main).split()), 1100)

    def test_un_solo_h1_y_las_secciones(self):
        self.assertEqual(self.html.count("<h1"), 1)
        for ancla in ("donde", "categorias", "como-llegar", "entregas", "mayoreo", "temporada", "preguntas"):
            with self.subTest(ancla=ancla):
                self.assertIn(f'id="{ancla}"', self.main)

    def test_la_foto_de_portada_es_la_de_main(self):
        self.assertEqual(re.findall(r"<img\b[^>]*>", self.main), [FOTO_MAIN])
        self.assertTrue((PUBLIC / "img/portadas/arboles-tampico-viveros-terra-sm.webp").is_file())
        self.assertTrue((PUBLIC / "img/portadas/arboles-tampico-viveros-terra.webp").is_file())

    def test_hechos_de_datos(self):
        plano = texto(self.main)
        for dato in (datos.CALLE, datos.COLONIA, datos.CP, datos.REFERENCIA, datos.HORARIO,
                     "Lunes a viernes de 9 a 18 h y sábado de 9 a 14 h", "25 de diciembre", "1 de enero",
                     f"${datos.PRECIOS['palma_desde']}", f"${datos.PRECIOS['pasto_solo_m2']}/m²",
                     f"${datos.PRECIOS['pasto_mayoreo_m2']}/m²", datos.LLEGADA_PASTO, datos.ANTICIPO, datos.FACTURA,
                     f"REPSE {datos.REPSE}", "según tu colonia", "Av. Álvaro Obregón", datos.NOMBRE_ALTERNO):
            with self.subTest(dato=dato):
                self.assertIn(dato, plano)
        self.assertTrue(datos.GARANTIA_PLANTAS.startswith("30 días en las plantas que sembramos nosotros"))
        self.assertTrue(datos.GARANTIA_PLANTAS.endswith(" (ver condiciones)."))

    def test_nada_inventado_ni_palabras_vetadas(self):
        plano = texto(self.main)
        self.assertIsNone(PROHIBIDAS_RE.search(plano), PROHIBIDAS_RE.search(plano))
        self.assertNotIn("disponibilidad", plano)
        self.assertNotRegex(plano, r"(?i)en \d+ (?:horas|días hábiles)|el mismo día|al día siguiente")

    def test_enlaza_las_categorias_de_plantas(self):
        for ruta in CATEGORIAS:
            with self.subTest(ruta=ruta):
                self.assertIn(f'href="{ruta}"', self.main)

    def test_enlaza_jardineria_en_madero_y_nochebuenas(self):
        self.assertIn('<a href="/jardineria-ciudad-madero">Jardinería en Ciudad Madero</a>', self.main)
        self.assertIn(f'href="{datos.NOCHEBUENAS["ruta"]}"', self.main)
        self.assertTrue(datos.NOCHEBUENAS["ruta"].startswith("/post/"))

    def test_mapas_sin_eventos_nuevos(self):
        for cta in ("vivero:mapas", "vivero:mapas-google", "vivero:mapas-apple"):
            with self.subTest(cta=cta):
                self.assertIn(f'data-cta="{cta}"', self.main)


class ViveroJsonLdTest(unittest.TestCase):
    def setUp(self):
        self.nodos = grafo(RUTA)

    def test_webpage_que_nombra_el_negocio(self):
        paginas_ld = [n for n in self.nodos if set(tipos(n)) & set(entidad.TIPOS_PAGINA)]
        self.assertEqual(len(paginas_ld), 1)
        pagina = paginas_ld[0]
        self.assertIn(pagina["@type"], entidad.TIPOS_PAGINA)
        self.assertEqual((pagina["@id"], pagina["url"]), (URL, URL))
        self.assertEqual(pagina["about"], entidad.REF)
        self.assertEqual(pagina["mainEntity"], entidad.REF)

    def test_el_negocio_se_define_una_sola_vez(self):
        negocio = [n for n in self.nodos if n.get("@id") == entidad.NEGOCIO_ID]
        self.assertEqual(negocio, [entidad.negocio()])

    def test_itemlist_de_categorias_igual_a_las_visibles(self):
        lista = next(n for n in self.nodos if "ItemList" in tipos(n))
        urls = [i["url"] for i in lista["itemListElement"]]
        main = main_de(RUTA)
        for url in urls:
            with self.subTest(url=url):
                self.assertIn(f'href="{url.removeprefix(datos.SITIO)}"', main)
        self.assertEqual([i["position"] for i in lista["itemListElement"]], list(range(1, len(urls) + 1)))
        self.assertGreaterEqual(len(urls), 6)

    def test_faq_y_migas(self):
        faq = next(n for n in self.nodos if "FAQPage" in tipos(n))
        visibles = [texto(q) for q in re.findall(r"<summary>(.*?)</summary>", main_de(RUTA), re.S)]
        self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)
        self.assertGreaterEqual(len(visibles), 8)
        migas = next(n for n in self.nodos if "BreadcrumbList" in tipos(n))
        self.assertEqual(migas["itemListElement"][-1]["item"], URL)


class EnlacesAlViveroTest(unittest.TestCase):
    def test_el_pie_lleva_el_domicilio(self):
        pie = partials.footer(paginas.contexto("/"))
        self.assertIn(f'<a href="/vivero-tampico">Vivero en Cd. Madero · {datos.CALLE_CORTA}</a>', pie)

    def test_mas_de_30_paginas_la_enlazan(self):
        origenes = [p for p in shell.paginas_html()
                    if paginas.ruta_de(p) != RUTA and 'href="/vivero-tampico"' in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(origenes), 30)
        con_pie = [p for p in shell.paginas_html()
                   if f'<a href="/vivero-tampico">Vivero en Cd. Madero · {datos.CALLE_CORTA}</a>'
                   in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(con_pie), 30)

    def test_y_desde_el_contenido(self):
        con_main = [p for p in shell.paginas_html()
                    if paginas.ruta_de(p) != RUTA and re.search(r'href="/vivero-tampico"', re.search(
                        r"<main\b.*</main>", p.read_text(encoding="utf-8"), re.S).group(0))]
        self.assertGreaterEqual(len(con_main), 30)

    def test_inicio_madero_y_nochebuenas_la_enlazan_con_ancla_descriptiva(self):
        for ruta, ancla in (("/", "vivero en Ciudad Madero"), ("/jardineria-ciudad-madero", "visita el vivero en Madero"),
                            (datos.NOCHEBUENAS["ruta"], "vivero en Cd. Madero")):
            with self.subTest(ruta=ruta):
                self.assertIn(f'<a href="/vivero-tampico">{ancla}</a>', main_de(ruta))

    def test_las_categorias_de_plantas_la_enlazan(self):
        for ruta in CATEGORIAS[:-1]:
            with self.subTest(ruta=ruta):
                self.assertIn('href="/vivero-tampico"', main_de(ruta))


class PrivacidadTest(unittest.TestCase):
    def test_noindex_y_fuera_del_sitemap(self):
        self.assertIn('<meta name="robots" content="noindex, follow">', html_de("/politica-privacidad"))
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn(f"<loc>{datos.SITIO}/politica-privacidad</loc>", sitemap)

    def test_domicilio_actual(self):
        self.assertIn(datos.CALLE, texto(main_de("/politica-privacidad")))

    def test_sin_la_direccion_vieja_en_public(self):
        """«601» solo queda como la clave del régimen fiscal del SAT (601 · General de Ley Personas Morales) en
        /datos-envio, que no es un domicilio."""
        for path in list(PUBLIC.rglob("*.html")) + [PUBLIC / "llms.txt", PUBLIC / "llms-full.txt", PUBLIC / "sitemap.xml"]:
            contenido = path.read_text(encoding="utf-8")
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                self.assertIsNone(DIRECCION_VIEJA_RE.search(contenido))
                sueltos = re.findall(r"(?<![\d.\-/#a-zA-Z_])601(?![\d.\-/a-zA-Z_])", texto(contenido))
                self.assertTrue(all(path.parent.name == "datos-envio" for _ in sueltos), sueltos)


class LlmsTest(unittest.TestCase):
    def test_llms_describe_la_pagina_nueva(self):
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
        self.assertIn(f"]({URL}): qué hay en el vivero", llms)
        self.assertIn(f"URL: {URL}\n", (PUBLIC / "llms-full.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
