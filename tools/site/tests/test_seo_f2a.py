"""SEO fase 2a (2026-11-11, docs/superpowers/plans/2026-11-10-seo-aeo-geo.md): las cuatro páginas nuevas
(/poda-arboles-tampico, /empresas, /nosotros y /zonas) existen con su título, descripción, H1, canonical, sitemap y
llms.txt; la poda dice lo que contestó el dueño (también derribo, según cotización, residuos en partida aparte y el
permiso lo tramita el dueño del predio, nunca Viveros Terra); /empresas tiene el REPSE y el 301 viejo; /nosotros es un
AboutPage que nombra #negocio; /zonas enlaza las 6 zonas con «Jardinería en …»; y las páginas del mapa las enlazan."""
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

PUBLIC = paginas.PUBLIC
NUEVAS = ("/poda-arboles-tampico", "/empresas", "/nosotros", "/zonas")
H1 = {
    "/poda-arboles-tampico": "Poda y derribo de árboles en Tampico",
    "/empresas": "Áreas verdes para empresas e industria",
    "/nosotros": "Viveros Terra: vivero y jardinería desde 2007",
    "/zonas": "Zonas de servicio de jardinería",
}
# Páginas que el mapa (§3a y §4b) pide que enlacen a cada página nueva, desde el contenido (<main>).
ENTRANTES = {
    "/poda-arboles-tampico": ("/blog/poda-arboles-palmas-tampico-guia", "/blog/temporada-huracanes-proteger-jardin-tampico",
                              "/jardineria-aguila-tampico", "/mantenimiento-jardines-tampico", "/precios", "/zonas"),
    "/empresas": ("/mayoreo-pasto-tampico", "/palmas-mayoreo-proyectos", "/mantenimiento-jardines-tampico",
                  "/jardineria-altamira", "/zonas", "/nosotros"),
}
NOSOTROS_TRAMITA_RE = re.compile(r"(?i)\b(?:nosotros\s+tramitamos|tramitamos\s+(?:el|los|tu)\s+permiso|"
                                 r"nos\s+encargamos\s+del\s+permiso|incluye\s+el\s+permiso)")


def html_de(ruta):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def texto(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def main_de(ruta):
    return re.search(r"<main\b.*</main>", html_de(ruta), re.S).group(0)


def grafo(ruta):
    bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_de(ruta), re.S).group(1)
    return json.loads(bloque)["@graph"]


def tipos(nodo):
    t = nodo.get("@type")
    return [t] if isinstance(t, str) else list(t or ())


class PaginasNuevasTest(unittest.TestCase):
    def test_registradas_con_contexto(self):
        self.assertEqual(generar.NUEVAS, NUEVAS)
        for ruta in NUEVAS:
            with self.subTest(ruta=ruta):
                self.assertIn(ruta, [r for r, *_ in generar.PAGINAS])
                paginas.contexto(ruta)

    def test_titulo_descripcion_h1_y_canonical(self):
        for ruta in NUEVAS:
            h = html_de(ruta)
            titulo = html_mod.unescape(re.search(r"<title>(.*?)</title>", h).group(1))
            descripcion = html_mod.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1))
            with self.subTest(ruta=ruta):
                self.assertLessEqual(len(titulo), 60, titulo)
                self.assertTrue(70 <= len(descripcion) <= 155, descripcion)
                self.assertEqual(titulo.count(datos.NOMBRE), 1)
                self.assertEqual(h.count("<h1"), 1)
                self.assertEqual(texto(re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)), H1[ruta])
                self.assertIn(f'<link rel="canonical" href="{datos.SITIO}{ruta}">', h)
                self.assertIn('<meta name="robots" content="index, follow">', h)
                self.assertIn('<p class="vt-portada__lema vt-serif">', h)
                self.assertIn('<nav class="vt-crumbs"', h)
                self.assertIn("data-hero-cta", h)

    def test_whatsapp_con_el_mensaje_propio_de_la_pagina(self):
        import mensajes_paginas
        for ruta in NUEVAS:
            esperado = html_mod.escape(datos.wa_url(datos.con_firma(mensajes_paginas.SEO_F2A[ruta])))
            with self.subTest(ruta=ruta):
                self.assertIn(f'data-cta="{paginas.contexto(ruta)["tipo"]}:hero" href="{esperado}"', html_de(ruta))

    def test_migas_y_breadcrumblist(self):
        for ruta in NUEVAS:
            migas = next(n for n in grafo(ruta) if "BreadcrumbList" in tipos(n))
            with self.subTest(ruta=ruta):
                self.assertEqual(migas["itemListElement"][0]["item"], f"{datos.SITIO}/")
                self.assertEqual(migas["itemListElement"][-1]["item"], f"{datos.SITIO}{ruta}")

    def test_faq_visible_y_faqpage_iguales(self):
        for ruta in NUEVAS:
            visibles = [texto(q) for q in re.findall(r"<summary>(.*?)</summary>", main_de(ruta), re.S)]
            faq = next(n for n in grafo(ruta) if "FAQPage" in tipos(n))
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(len(visibles), 5)
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)

    def test_en_el_sitemap(self):
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        for ruta in NUEVAS:
            with self.subTest(ruta=ruta):
                self.assertEqual(sitemap.count(f"<loc>{datos.SITIO}{ruta}</loc>"), 1)

    def test_en_llms_txt_y_llms_full(self):
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
        full = (PUBLIC / "llms-full.txt").read_text(encoding="utf-8")
        for ruta in NUEVAS:
            with self.subTest(ruta=ruta):
                self.assertIn(f"]({datos.SITIO}{ruta})", llms)
                self.assertIn(f"URL: {datos.SITIO}{ruta}\n", full)

    def test_menu_y_pie_las_enlazan(self):
        pie = partials.footer(paginas.contexto("/"))
        menu = partials.header(paginas.contexto("/"))
        for ruta in NUEVAS:
            with self.subTest(ruta=ruta):
                self.assertIn(f'href="{ruta}"', pie)
        for ruta in ("/poda-arboles-tampico", "/empresas"):
            with self.subTest(menu=ruta):
                self.assertIn(f'href="{ruta}"', menu)


class PodaTest(unittest.TestCase):
    def setUp(self):
        self.main = texto(main_de("/poda-arboles-tampico"))

    def test_derribo_segun_cotizacion_y_desde_500(self):
        self.assertIn("derrib", self.main.lower())
        self.assertIn(datos.DERRIBO, self.main)
        self.assertIn("según cotización", self.main.lower())
        self.assertIn(f"${datos.PRECIOS['poda']}", self.main)

    def test_residuos_en_partida_aparte(self):
        self.assertIn(datos.PODA_RESIDUOS, self.main)
        self.assertIn("partida aparte", datos.PODA)
        self.assertNotIn("y de los residuos que se generan", datos.PODA)
        self.assertTrue(datos.PODA.startswith("Desde $500, según cotización"))
        self.assertIn("Mándanos fotos y ubicación por WhatsApp.", datos.PODA)

    def test_el_permiso_lo_tramita_el_cliente(self):
        self.assertIn("lo tramita el dueño del predio", self.main)
        self.assertIn("Viveros Terra no tramita el permiso", self.main)
        self.assertIsNone(NOSOTROS_TRAMITA_RE.search(self.main))
        self.assertNotIn("nosotros tramitamos", self.main.lower())

    def test_el_permiso_nunca_lo_tramita_terra_en_ninguna_pagina(self):
        for path in PUBLIC.rglob("*.html"):
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                self.assertIsNone(NOSOTROS_TRAMITA_RE.search(texto(path.read_text(encoding="utf-8"))))

    def test_sin_ligas_ni_costos_del_tramite_ni_iva(self):
        h = main_de("/poda-arboles-tampico")
        for href in re.findall(r'href="(https?://[^"]+)"', h):
            with self.subTest(href=href):
                self.assertRegex(href, r"^https://(wa\.me/|maps\.app\.goo\.gl/|repse\.stps\.gob\.mx/)")
        self.assertNotRegex(self.main, r"(?i)\bcon IVA\b|IVA incluido")

    def test_preguntas_de_google(self):
        preguntas = [texto(q) for q in re.findall(r"<summary>(.*?)</summary>", main_de("/poda-arboles-tampico"), re.S)]
        for clave in ("¿Cuánto cuesta podar", "¿Cuánto cobran por derribar", "¿Se necesita permiso", "¿Cuándo conviene"):
            with self.subTest(pregunta=clave):
                self.assertTrue(any(p.startswith(clave) for p in preguntas), preguntas)
        self.assertIn('href="/blog/poda-arboles-palmas-tampico-guia"', main_de("/poda-arboles-tampico"))

    def test_la_lista_de_precios_dice_lo_mismo(self):
        precios = main_de("/precios")
        self.assertIn('<a href="/poda-arboles-tampico">Poda de palmas y árboles</a>', precios)
        self.assertIn("el retiro de residuos va como partida aparte", precios)
        self.assertNotIn("y de los residuos que se generan", texto(precios))


class EmpresasTest(unittest.TestCase):
    def test_repse_con_padron_factura_y_clientes(self):
        h = main_de("/empresas")
        plano = texto(h)
        self.assertIn(f"REPSE {datos.REPSE}", plano)
        self.assertIn(f'href="{datos.REPSE_PADRON}"', h)
        self.assertIn(datos.FACTURA, plano)
        self.assertIn(datos.PROYECTOS_B2B, plano)
        for cliente in datos.CLIENTES_B2B:
            with self.subTest(cliente=cliente):
                self.assertTrue(cliente in plano or f'alt="{cliente}"' in h)

    def test_enlaza_a_sus_hijos(self):
        h = main_de("/empresas")
        for hijo in ("/mayoreo-pasto-tampico", "/palmas-mayoreo-proyectos", "/mantenimiento-jardines-tampico",
                     "/sistema-riego-tampico", "/jardineria-altamira"):
            with self.subTest(hijo=hijo):
                self.assertIn(f'href="{hijo}"', h)

    def test_el_301_viejo_va_a_empresas(self):
        redirects = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        destino = {r["source"]: r["destination"] for r in redirects}
        self.assertEqual(destino["/jardineria-puerto-industrial-altamira"], "/empresas")


class NosotrosTest(unittest.TestCase):
    def test_about_page_que_nombra_el_negocio_sin_repetirlo(self):
        nodos = grafo("/nosotros")
        about = next(n for n in nodos if "AboutPage" in tipos(n))
        self.assertEqual(about["about"], entidad.REF)
        self.assertEqual(about["mainEntity"], entidad.REF)
        self.assertEqual(about["@id"], f"{datos.SITIO}/nosotros")
        negocio = [n for n in nodos if n.get("@id") == entidad.NEGOCIO_ID]
        self.assertEqual(len(negocio), 1)
        self.assertEqual(negocio[0], entidad.negocio_minimo())
        self.assertEqual([n for n in nodos if "WebPage" in tipos(n)], [])

    def test_hechos_de_datos(self):
        plano = texto(main_de("/nosotros"))
        for dato in ("12 de diciembre", str(datos.DESDE), datos.CLIENTES, f"REPSE {datos.REPSE}", datos.DOMICILIO_COMPLETO,
                     datos.HORARIO, datos.NOMBRE_ALTERNO):
            with self.subTest(dato=dato):
                self.assertIn(dato, plano)
        for _nombre, url in datos.REDES:
            with self.subTest(perfil=url):
                self.assertIn(f'href="{url}"', main_de("/nosotros"))

    def test_fotos_que_ya_existen(self):
        for src in re.findall(r'<img src="(/img/[^"]+)"', main_de("/nosotros")):
            with self.subTest(src=src):
                self.assertTrue((PUBLIC / src.lstrip("/")).is_file())


class ZonasTest(unittest.TestCase):
    def test_enlaza_las_6_zonas_con_jardineria_en(self):
        h = main_de("/zonas")
        for _nombre, ruta in datos.ZONAS:
            anclas = [texto(a) for a in re.findall(rf'<a href="{re.escape(ruta)}">(.*?)</a>', h, re.S)]
            with self.subTest(ruta=ruta):
                self.assertTrue(anclas)
                self.assertTrue(all(a.startswith("Jardinería en ") for a in anclas), anclas)

    def test_resume_tampico_madero_y_altamira(self):
        plano = texto(main_de("/zonas"))
        for ciudad in ("Tampico", "Ciudad Madero", "Altamira", datos.ZONAS_POR_PROYECTO):
            with self.subTest(ciudad=ciudad):
                self.assertIn(ciudad, plano)

    def test_el_pie_usa_jardineria_en(self):
        zonas = dict(partials.PIE)["Zonas"]
        for texto_pie, href in zonas:
            if href.startswith("/jardineria-"):
                with self.subTest(href=href):
                    self.assertTrue(texto_pie.startswith("Jardinería en "))
        self.assertEqual({h for _t, h in zonas if h.startswith("/jardineria-")}, {r for _n, r in datos.ZONAS})


class EnlacesEntrantesTest(unittest.TestCase):
    def test_las_paginas_del_mapa_enlazan_desde_el_contenido(self):
        for destino, origenes in ENTRANTES.items():
            for origen in origenes:
                with self.subTest(origen=origen, destino=destino):
                    self.assertIn(f'href="{destino}"', main_de(origen))

    def test_zonas_y_nosotros_enlazadas_desde_el_contenido(self):
        self.assertIn('href="/zonas"', main_de("/poda-arboles-tampico"))
        self.assertIn('href="/nosotros"', partials.footer(paginas.contexto("/")))


if __name__ == "__main__":
    unittest.main()
