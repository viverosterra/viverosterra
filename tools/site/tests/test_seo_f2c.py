"""SEO fase 2c (2026-11-11, docs/superpowers/plans/2026-11-10-seo-aeo-geo.md, Fase 2; mapa de palabras clave §2 G4, G5, G7,
G9-G13): clúster de palmas con pilar único, cinco fusiones del blog con 301, cinco artículos retitulados y las seis
zonas diferenciadas.

- G4: /palmas-tropicales-tampico es el pilar («Venta de palmas en Tampico»); cada una de las 10 fichas de palma lo enlaza
  con el ancla exacta en su primer párrafo; /plantas-para-jardin-tampico y /palmas-mayoreo-proyectos no usan esa frase.
- Fusiones: seis URLs viejas redirigen con 301 a su destino (las dos listas de palmas a una URL nueva sin «mas-vendidas»);
  ninguna sigue en public/, el sitemap, llms.txt o un enlace interno, y el destino tiene lo útil del artículo fusionado.
- G10, G12 y G13: título y descripción del mapa (revisados contra el artículo) y un H1 que es la pregunta, sin
  «Tampico» al inicio y distinto del de su página de servicio o categoría, a la que enlaza.
- G5: descripción propia por zona (ninguna frase con precio se repite), un enfoque propio y menos texto compartido.
  Las fotos no cambian (tests/test_zonas_reglas.py y tests/test_blog_paridad.py lo vigilan)."""
import html as html_mod
import itertools
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402
from contenido import articulo, blog_seo_f2c, zona, zonas  # noqa: E402

PUBLIC = paginas.PUBLIC
RAIZ = PUBLIC.parent
MAPA = (RAIZ / "docs/seo/2026-11/mapa-palabras-clave.md").read_text(encoding="utf-8")
REDIRECTS = {r["source"]: r for r in json.loads((RAIZ / "vercel.json").read_text(encoding="utf-8"))["redirects"]}

PILAR = "/palmas-tropicales-tampico"
ANCLA = "venta de palmas en Tampico"
FICHAS = ("palma-areca-tampico", "palma-bambu-chamaedorea-tampico", "palma-bismarckia-bismarckia-nobilis-tampico",
          "palma-coco-plumoso-tampico", "palma-cola-de-zorro-wodyetia-bifurcata-tampico",
          "palma-kerpis-howea-forsteriana-tampico", "palma-real-roystonea-regia-tampico",
          "palma-triangular-dypsis-decaryi-tampico", "palma-washingtona-tampico", "cuidados-palma-del-viajero-ravenala")
FUSIONES = {
    "/blog/palmas-tropicales-jardin-tampico": "/blog/palmas-para-jardin-tampico",
    "/blog/palmas-mas-vendidas-tampico-precios": "/blog/palmas-para-jardin-tampico",
    "/blog/riego-automatico-tampico-roi": "/blog/sistema-riego-automatizado-tampico",
    "/blog/sistema-riego-automatico-conviene-tampico": "/blog/sistema-riego-automatizado-tampico",
    "/blog/pasto-sintetico-para-perros": "/pasto-sintetico/perros",
    "/blog/jardin-bajo-presupuesto-tampico": "/blog/cuanto-cuesta-jardin-tampico-precios",
}
# Lo útil del artículo fusionado que tiene que estar en el destino.
TRAIDO = {
    "/blog/palmas-para-jardin-tampico": ("Cycas circinalis", "¿Qué palma resiste mejor el viento costero de Tampico?",
                                         "¿Qué palma necesita menos mantenimiento en Tampico?"),
    "/blog/sistema-riego-automatizado-tampico": ("¿Cuándo sí conviene el riego automático y cuándo no?",
                                                 "Errores que ves en Tampico cuando se instala mal",
                                                 "Alternativa económica: kit semi-automático",
                                                 "¿Funciona con baja presión de agua?"),
    "/pasto-sintetico/perros": ("Cómo se limpia: orina, heces y olor", "vinagre blanco", "4 errores a evitar con perros"),
    "/blog/cuanto-cuesta-jardin-tampico-precios": ("¿Qué jardín puedes hacer con $5,000, $20,000 o $50,000?",
                                                    "Subtotal: $18,300", "Cómo elegir tu nivel de inversión"),
}
# Retitulados (mapa §2 G10, G12, G13): título del mapa, descripción (la del mapa o, si el artículo no la sostiene, la
# adaptada con su motivo), H1 nuevo y la página de servicio o categoría que no deben repetir y a la que enlazan.
RETITULADOS = {
    "pasto-san-agustin-instalacion-mantenimiento": ("Cómo Instalar Pasto en Rollo San Agustín | Viveros Terra",
                                                    "Cómo instalar pasto en rollo San Agustín paso a paso",
                                                    "/pasto-en-rollo-tampico"),
    "diseno-jardines-tampico-guia": ("Cómo Diseñar tu Jardín Paso a Paso | Viveros Terra",
                                     "Cómo diseñar tu jardín paso a paso para el clima del Golfo",
                                     "/diseno-jardines-tampico"),
    "plantas-interior-tampico": ("Plantas de Interior Resistentes y Fáciles | Viveros Terra",
                                 "¿Qué plantas de interior resisten el calor y el aire acondicionado?",
                                 "/plantas-de-interior-tampico"),
    "tierra-negra-costal-camion-tampico": ("Tierra Negra: Cuánta Necesitas por m² | Viveros Terra",
                                           "¿Cuánta tierra negra necesitas? Costal o camión según tu jardín",
                                           "/tierra-negra-vegetal-tampico"),
    "tezontle-usos-jardin-tampico": ("Tezontle: Para Qué Sirve y 8 Usos en Jardín | Viveros Terra",
                                     "¿Para qué sirve el tezontle? 8 usos en el jardín", "/tezontle-rojo-tampico"),
}
# La descripción del mapa prometía algo que el artículo no dice: se queda la adaptada (fase 0 o 2c) y aquí, el porqué.
DESCRIPCION_ADAPTADA = {
    "pasto-san-agustin-instalacion-mantenimiento": "el artículo no habla del «primer corte»; dice los primeros 20 días",
    "tezontle-usos-jardin-tampico": "el artículo no trata el tezontle en macetas",
    "tierra-negra-costal-camion-tampico": "el artículo solo da el camión de 8 m³ (no los de 5 y 14)",
}
ZONAS = tuple(r for _n, r in datos.ZONAS)
# Medido el 2026-11-11 sobre el <main> de las seis zonas: antes, el 41% de las frases de cada página (hasta 45%) se
# repetía en otra zona y la similitud media de 8-gramas era de 29.8%; con el enfoque propio, 36% (máximo 40%) y 26.1%.
TOPE_FRASES_COMPARTIDAS = 0.40
TOPE_JACCARD_MEDIO = 0.27
TOCADAS = (PILAR, "/plantas-para-jardin-tampico", "/palmas-mayoreo-proyectos", "/pasto-sintetico/perros", "/blog",
           "/zonas", *ZONAS, *(f"/blog/{s}" for s in (*FICHAS, *RETITULADOS)), *set(FUSIONES.values()))


def html_de(ruta):
    return paginas_html()[ruta]


_CACHE = {}


def paginas_html():
    if not _CACHE:
        _CACHE.update({paginas.ruta_de(p): p.read_text(encoding="utf-8") for p in shell.paginas_html()})
    return _CACHE


def texto(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def main_de(ruta):
    return re.search(r"<main\b.*</main>", html_de(ruta), re.S).group(0)


def titulo(ruta):
    return html_mod.unescape(re.search(r"<title>(.*?)</title>", html_de(ruta)).group(1))


def descripcion(ruta):
    return html_mod.unescape(re.search(r'<meta name="description" content="([^"]*)"', html_de(ruta)).group(1))


def h1(ruta):
    return texto(re.search(r"<h1\b[^>]*>(.*?)</h1>", html_de(ruta), re.S).group(1))


def primer_parrafo(slug):
    """Primer <p> del artículo después de la respuesta directa y del índice móvil."""
    articulo_html = re.search(r'<article class="vt-art__cuerpo".*?</article>', html_de(f"/blog/{slug}"), re.S).group(0)
    sin_cabeza = re.sub(r'<section id="respuesta".*?</section>|<details class="vt-art__toc".*?</details>', "",
                        articulo_html, flags=re.S)
    return re.search(r"<p>(.*?)</p>", sin_cabeza, re.S).group(1)


class PalmasTest(unittest.TestCase):
    def test_pilar_con_titulo_y_h1_de_venta(self):
        self.assertEqual(titulo(PILAR), f"Venta de Palmas en Tampico desde ${datos.PRECIOS['palma_desde']} | Viveros Terra")
        self.assertIn(f"**{titulo(PILAR)}**", MAPA)
        self.assertEqual(h1(PILAR), "Venta de palmas para jardín en Tampico")
        self.assertTrue(descripcion(PILAR).startswith("Venta de palmas para jardín en Tampico"))
        self.assertLessEqual(len(descripcion(PILAR)), 155)

    def test_cada_ficha_enlaza_al_pilar_en_su_primer_parrafo(self):
        self.assertEqual(len(FICHAS), 10)
        for slug in FICHAS:
            with self.subTest(slug=slug):
                self.assertIn(f'<a href="{PILAR}">{ANCLA}</a>', primer_parrafo(slug))

    def test_el_pilar_es_la_unica_con_la_frase_exacta(self):
        for ruta in ("/plantas-para-jardin-tampico", "/palmas-mayoreo-proyectos"):
            with self.subTest(ruta=ruta):
                self.assertNotIn(ANCLA.casefold(), texto(main_de(ruta)).casefold())
                self.assertNotIn(ANCLA.casefold(), titulo(ruta).casefold())
                self.assertNotIn(ANCLA.casefold(), h1(ruta).casefold())
                self.assertIn(f'href="{PILAR}"', main_de(ruta))
        self.assertIn("mayoreo", titulo("/palmas-mayoreo-proyectos").casefold())
        self.assertIn("mayoreo", h1("/palmas-mayoreo-proyectos").casefold())

    def test_lista_unica_de_palmas_sin_mas_vendidas(self):
        ruta = "/blog/palmas-para-jardin-tampico"
        self.assertIn("palmas-para-jardin-tampico", articulo.NUEVOS)
        self.assertIn(f"**{titulo(ruta)}**", MAPA)
        self.assertIn("/blog/palmas-para-jardin-tampico", MAPA)  # la URL que propone el mapa
        self.assertIn(f'<link rel="canonical" href="{datos.SITIO}{ruta}">', html_de(ruta))
        self.assertIn(f'<a href="{PILAR}">{ANCLA}</a>', main_de(ruta))


class FusionesTest(unittest.TestCase):
    def test_seis_origenes_con_301_directo_al_destino(self):
        self.assertEqual(len(FUSIONES), 6)
        for origen, destino in FUSIONES.items():
            with self.subTest(origen=origen):
                self.assertEqual(REDIRECTS[origen]["destination"], destino)
                self.assertIs(REDIRECTS[origen]["permanent"], True)
                self.assertNotIn(destino, REDIRECTS, "cadena de redirecciones")
                self.assertIn(destino, paginas_html())

    def test_ninguna_redireccion_vieja_apunta_a_un_origen_fusionado(self):
        for regla in REDIRECTS.values():
            with self.subTest(origen=regla["source"]):
                self.assertNotIn(regla["destination"], FUSIONES)

    def test_el_origen_ya_no_se_publica(self):
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8") + (PUBLIC / "llms-full.txt").read_text(encoding="utf-8")
        for origen in FUSIONES:
            with self.subTest(origen=origen):
                self.assertFalse((PUBLIC / origen.strip("/")).exists())
                self.assertNotIn(origen, paginas_html())
                self.assertNotIn(origen.removeprefix("/blog/"), articulo.CLAVES)
                self.assertNotIn(f"{datos.SITIO}{origen}<", sitemap)
                self.assertNotIn(f"{datos.SITIO}{origen})", llms)
                self.assertNotIn(f"{datos.SITIO}{origen}\n", llms)
        for destino in set(FUSIONES.values()):
            with self.subTest(destino=destino):
                self.assertEqual(sitemap.count(f"<loc>{datos.SITIO}{destino}</loc>"), 1)

    def test_ningun_enlace_interno_a_una_url_redirigida(self):
        """Ni a las seis de esta entrega ni a ningún origen de vercel.json (los enlaces van directo al destino)."""
        origenes = {o for o in REDIRECTS if ":" not in o and "*" not in o}
        for ruta, html in paginas_html().items():
            hrefs = {h.split("#")[0].split("?")[0].rstrip("/") or "/" for h in re.findall(r'href="(/[^"]*)"', html)}
            with self.subTest(ruta=ruta):
                self.assertEqual(sorted(hrefs & origenes), [])

    def test_el_destino_trae_lo_util_del_fusionado(self):
        for destino, frases in TRAIDO.items():
            cuerpo = texto(main_de(destino))
            for frase in frases:
                with self.subTest(destino=destino, frase=frase):
                    self.assertIn(frase, cuerpo)

    def test_riego_enlaza_al_servicio_con_su_ancla(self):
        main = main_de("/blog/sistema-riego-automatizado-tampico")
        self.assertIn('<a href="/sistema-riego-tampico">instalación de sistema de riego en Tampico</a>', main)
        self.assertNotIn("Tampico", titulo("/blog/sistema-riego-automatizado-tampico"))
        self.assertIn(f"**{titulo('/blog/sistema-riego-automatizado-tampico')}**", MAPA)

    def test_sin_las_cifras_sin_fuente_de_los_fusionados(self):
        """La tarifa de agua, el ahorro en pesos, «50% del agua se evapora» y el plazo de recuperación no se traen."""
        for destino in TRAIDO:
            cuerpo = texto(main_de(destino))
            for frase in ("$50/m³", "Ahorro anual", "50% del agua", "se amortiza", "18–24 meses", "cada 3–4 meses y 2 veces"):
                with self.subTest(destino=destino, frase=frase):
                    self.assertNotIn(frase, cuerpo)

    def test_las_filas_de_correccion_usan_el_texto_de_la_entrega(self):
        from contenido import blog_correcciones as bc
        filas = {c: (a, d) for lista in bc.FILAS.values() for c, a, d, _m in lista}
        self.assertEqual(filas["C305"], (blog_seo_f2c.RIEGO_ANTES, blog_seo_f2c.RIEGO_NUEVO))
        self.assertEqual(filas["C307"], (blog_seo_f2c.COSTOS_ANTES, blog_seo_f2c.COSTOS_NUEVO))
        self.assertEqual(len([c for c in filas if "C308" <= c <= "C316"]), len(FICHAS) - 1)  # la bambú es nueva


class RetituladosTest(unittest.TestCase):
    def test_titulo_del_mapa_y_descripcion_revisada(self):
        for slug, (esperado, _h1, _pagina) in RETITULADOS.items():
            ruta = f"/blog/{slug}"
            with self.subTest(slug=slug):
                self.assertEqual(titulo(ruta), esperado)
                self.assertIn(f"**{esperado}**", MAPA)
                self.assertLessEqual(len(titulo(ruta)), 60)
                self.assertTrue(70 <= len(descripcion(ruta)) <= 155)
                if slug not in DESCRIPCION_ADAPTADA:
                    self.assertIn(f"| {descripcion(ruta)} (", MAPA)

    def test_h1_con_la_pregunta_y_sin_competir_con_su_pagina(self):
        for slug, (_t, esperado, pagina) in RETITULADOS.items():
            ruta = f"/blog/{slug}"
            with self.subTest(slug=slug):
                self.assertEqual(h1(ruta), esperado)
                self.assertFalse(h1(ruta).startswith("Tampico"))
                self.assertFalse(titulo(ruta).startswith("Tampico"))
                self.assertRegex(h1(ruta), r"^(¿|Cómo )")
                self.assertNotEqual(h1(ruta).casefold(), h1(pagina).casefold())
                self.assertIn(f'href="{pagina}"', main_de(ruta))

    def test_diseno_y_riego_enlazan_su_servicio_con_el_ancla_del_mapa(self):
        self.assertIn('<a href="/diseno-jardines-tampico">diseño de jardines en Tampico</a>',
                      main_de("/blog/diseno-jardines-tampico-guia"))
        self.assertIn('<a href="/pasto-en-rollo-tampico">pasto San Agustín instalado</a>',
                      main_de("/blog/pasto-san-agustin-instalacion-mantenimiento"))


def _frases(t):
    return [s.strip().casefold() for s in re.split(r"(?<=[.?!:])\s+", t) if len(s.split()) >= 4]


def _shingles(t, n=8):
    w = re.findall(r"\w+", t.casefold())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


class ZonasTest(unittest.TestCase):
    def setUp(self):
        self.textos = {r: texto(re.sub(r"<(script|style|svg)\b.*?</\1>", " ", main_de(r), flags=re.S)) for r in ZONAS}

    def test_descripcion_propia_sin_frase_de_precio_repetida(self):
        descripciones = [descripcion(r) for r in ZONAS]
        self.assertEqual(len(set(descripciones)), 6)
        con_precio = Counter(f for d in descripciones for f in re.split(r"(?<=\.)\s+", d) if "$" in f)
        self.assertEqual([f for f, n in con_precio.items() if n > 1], [])
        for ruta in ZONAS:
            with self.subTest(ruta=ruta):
                self.assertTrue(70 <= len(descripcion(ruta)) <= 155, descripcion(ruta))

    def test_enfoque_propio_de_cada_zona(self):
        enlaces = {"/jardineria-altamira": ("/empresas", "/mayoreo-pasto-tampico"),
                   "/jardineria-ciudad-madero": ("/vivero-tampico", "/blog/plantas-resistentes-sal-golfo-tampico"),
                   "/jardineria-lomas-del-chairel-tampico": ("/blog/como-evitar-encharcamientos-jardin-tampico",),
                   "/jardineria-aguila-tampico": ("/poda-arboles-tampico",),
                   "/jardineria-country-club-tampico": ("/diseno-jardines-tampico", "/sistema-riego-tampico"),
                   "/jardineria-lomas-de-rosales-tampico": ("/diseno-jardines-tampico", "/sistema-riego-tampico")}
        for ruta, destinos in enlaces.items():
            lede, (ficha, _texto) = zona.ENFOQUE[ruta.strip("/")]
            with self.subTest(ruta=ruta):
                self.assertIn(lede, self.textos[ruta])
                self.assertIn(ficha, self.textos[ruta])
                for destino in destinos:
                    self.assertIn(f'href="{destino}"', main_de(ruta))
        self.assertIn(datos.PODA_PERMISO, self.textos["/jardineria-aguila-tampico"])
        self.assertIn(f"REPSE {datos.REPSE}", self.textos["/jardineria-altamira"])

    def test_menos_texto_compartido_entre_zonas(self):
        frases = {r: _frases(t) for r, t in self.textos.items()}
        cuenta = Counter(f for r in ZONAS for f in set(frases[r]))
        for ruta in ZONAS:
            compartidas = sum(1 for f in frases[ruta] if cuenta[f] > 1) / len(frases[ruta])
            with self.subTest(ruta=ruta):
                self.assertLessEqual(compartidas, TOPE_FRASES_COMPARTIDAS)
        tejas = {r: _shingles(t) for r, t in self.textos.items()}
        pares = [len(tejas[a] & tejas[b]) / len(tejas[a] | tejas[b]) for a, b in itertools.combinations(ZONAS, 2)]
        self.assertLessEqual(sum(pares) / len(pares), TOPE_JACCARD_MEDIO)

    def test_anclas_entrantes_jardineria_en(self):
        for ruta in ZONAS:
            nombre = zona.ZONAS[ruta.strip("/")]["nombre"]
            with self.subTest(ruta=ruta):
                self.assertIn(f'<a href="{ruta}">{zonas.ancla(ruta.strip("/"))}</a>', main_de("/zonas"))
                self.assertEqual(zonas.ancla(ruta.strip("/")), f"Jardinería en {nombre}")
                otra = next(r for r in ZONAS if r != ruta)
                self.assertRegex(main_de(otra), rf'<a href="{re.escape(ruta)}">Jardinería en ')

    def test_sin_casos_inventados(self):
        for ruta in ZONAS:
            with self.subTest(ruta=ruta):
                self.assertNotRegex(self.textos[ruta], r"(?i)caso real|cliente de la colonia|proyecto en la colonia")


def _de_main(ruta_public):
    """El archivo de public/ como está en main (antes de esta entrega)."""
    return subprocess.run(["git", "show", f"main:public/{ruta_public}"], cwd=RAIZ, capture_output=True, text=True,
                          check=True).stdout


def _fotos(html):
    """(src, srcset, alt) de cada <img> del <main>, sin el logo del encabezado ni del pie."""
    m = re.search(r"<main\b.*</main>", html, re.S)
    salida = []
    for img in re.findall(r"<img\b[^>]*>", m.group(0) if m else html):
        attr = dict(re.findall(r'\b(src|srcset|alt)="([^"]*)"', img))
        salida.append((attr.get("src"), attr.get("srcset"), attr.get("alt")))
    return salida


class FotosTest(unittest.TestCase):
    """Regla del dueño: «No elimines o cambies las fotos, déjalas así como están». Las fusiones no quitan ninguna."""

    def test_el_indice_del_blog_conserva_todas_las_fotos_de_main(self):
        viejas = _fotos(_de_main("blog/index.html"))
        nuevas = _fotos(html_de("/blog"))
        self.assertGreater(len(viejas), 30)
        self.assertEqual(sorted(set(viejas) - set(nuevas)), [])
        self.assertEqual([f[0] for f in viejas], [f[0] for f in nuevas])  # mismas fotos, mismo orden

    def test_cada_foto_de_las_paginas_retiradas_sigue_en_public(self):
        todo = "\n".join(paginas_html().values())
        for origen, destino in FUSIONES.items():
            for src, _srcset, _alt in _fotos(_de_main(f"{origen.strip('/')}/index.html")):
                with self.subTest(origen=origen, src=src):
                    self.assertIn(f'src="{src}"', todo)
                    self.assertIn(f'src="{src}"', main_de(destino), "la foto sigue en su tema: en el destino")

    def test_las_fotos_traidas_conservan_archivo_y_alt(self):
        for destino, (src, alt) in {
            "/blog/sistema-riego-automatizado-tampico": ("/img/instalacion-riego-tuberias-jardines-tampico.webp",
                                                         "Instalación de sistema de riego automático con tuberías en jardín de Tampico"),
            "/blog/cuanto-cuesta-jardin-tampico-precios": ("/img/jardin-residencial-plantas-pasto-tampico.webp",
                                                           "Jardín residencial con plantas y pasto en Tampico — proyecto de bajo presupuesto"),
            "/blog/palmas-para-jardin-tampico": ("/img/plantas-tropicales-tampico-viveros.webp",
                                                 "Palmas tropicales disponibles en Viveros Terra Tampico — Washingtona, Areca, Viajero y más"),
        }.items():
            with self.subTest(destino=destino):
                self.assertIn((src, None, alt), _fotos(html_de(destino)))
        perros = [f for f in _fotos(html_de("/pasto-sintetico/perros")) if f[0] == "/img/pasto-sintetico-residencial-tampico.webp"]
        self.assertEqual(perros, [("/img/pasto-sintetico-residencial-tampico.webp",
                                   "/img/pasto-sintetico-residencial-tampico-640.webp 640w, /img/pasto-sintetico-residencial-tampico.webp 1024w",
                                   "Pasto sintético para perros y mascotas")])

    def test_las_tarjetas_de_los_fusionados_llevan_al_apartado_del_destino(self):
        indice = html_de("/blog")
        for href in ("/blog/sistema-riego-automatizado-tampico#cuando-conviene",
                     "/blog/cuanto-cuesta-jardin-tampico-precios#por-presupuesto", "/pasto-sintetico/perros",
                     "/blog/palmas-para-jardin-tampico"):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', indice)
                ruta, _, ancla = href.partition("#")
                if ancla:
                    self.assertIn(f'id="{ancla}"', html_de(ruta))


class ReglasTest(unittest.TestCase):
    def test_sin_palabras_prohibidas_en_las_paginas_tocadas(self):
        for ruta in TOCADAS:
            html = html_de(ruta)
            visible = texto(main_de(ruta)) + " " + titulo(ruta) + " " + descripcion(ruta)
            sin_garantia = visible.replace("la reponemos sin costo", "")
            with self.subTest(ruta=ruta):
                self.assertNotRegex(visible, r"(?i)\bgratis\b|\bgratuit")
                self.assertNotRegex(sin_garantia, r"(?i)\bsin costo\b")
                self.assertNotRegex(visible, r"(?i)m[aá]s\s+vendid")
                self.assertNotRegex(html, r"(?i)mas-vendidas|\bOasis\b")
                self.assertNotRegex(visible, r"(?i)visita sin costo")

    def test_nochebuenas_sigue_en_su_url(self):
        self.assertIn(datos.NOCHEBUENAS["ruta"], paginas_html())
        self.assertEqual(datos.NOCHEBUENAS["ruta"], "/post/nochebuenas-tampico-madero-mayoreo")
        self.assertNotIn(datos.NOCHEBUENAS["ruta"], REDIRECTS)


if __name__ == "__main__":
    unittest.main()
