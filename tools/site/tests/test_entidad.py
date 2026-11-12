"""Entidad única y datos estructurados (SEO fase 1, 2026-11-10). Reglas permanentes sobre las páginas de public/:

- un solo negocio: todo nodo con @id …/#negocio tiene el mismo @type, nombre y teléfono; ningún LocalBusiness, Store u
  Organization del negocio sin ese @id; el nodo completo solo en la home y en /vivero-tampico; sin aggregateRating;
- todo @id que una página nombra está definido en esa misma página;
- todo Product lleva una foto que existe y una oferta con precio (Offer.price o AggregateOffer.lowPrice) y su vendedor;
- los artículos del blog llevan su Article completo y el sitemap repite su dateModified;
- el speakable cuelga del WebPage y apunta a respuestas que existen, nunca a encabezados;
- las migas del JSON-LD son las visibles; la home no tiene BreadcrumbList;
- las páginas indexables llevan Open Graph completo.
"""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import entidad  # noqa: E402
import paginas  # noqa: E402
from contenido import articulo  # noqa: E402

PUBLIC = paginas.PUBLIC
SITIO = datos.SITIO
PAGINAS = {p.relative_to(PUBLIC).as_posix(): p.read_text(encoding="utf-8") for p in sorted(PUBLIC.rglob("*.html"))}
COMPLETO_EN = {"index.html", "vivero-tampico/index.html"}
TIPOS_NEGOCIO = {"LocalBusiness", "Store", "GardenStore", "Organization"}
ENCABEZADO_RE = re.compile(r"(^|[\s,>])h[1-6]\b|#vt-h1|summary")


def bloques(html):
    return [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def recorrer(nodo):
    if isinstance(nodo, dict):
        yield nodo
        for valor in nodo.values():
            yield from recorrer(valor)
    elif isinstance(nodo, list):
        for valor in nodo:
            yield from recorrer(valor)


def nodos(html):
    return [n for b in bloques(html) for n in recorrer(b)]


def tipos(nodo):
    tipo = nodo.get("@type")
    return [tipo] if isinstance(tipo, str) else list(tipo or ())


def de_tipo(html, tipo):
    return [n for n in nodos(html) if tipo in tipos(n)]


def de_pagina(html):
    """Nodos de página: WebPage o sus subtipos (AboutPage, CollectionPage…), como los reconoce entidad.completar."""
    return [n for n in nodos(html) if set(tipos(n)) & set(entidad.TIPOS_PAGINA)]


def plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", "", fragmento))).strip()


def archivo_de(url):
    return PUBLIC / url.removeprefix(SITIO + "/")


def indexable(html):
    return "noindex" not in re.search(r'<meta name="robots" content="([^"]*)"', html).group(1)


class NodoTest(unittest.TestCase):
    def test_same_as_son_todas_las_redes_y_el_mapa(self):
        self.assertEqual(entidad.negocio()["sameAs"], [u for _n, u in datos.REDES] + [datos.MAPS_URL])

    def test_nodo_completo_con_lo_de_datos(self):
        n = entidad.negocio()
        self.assertEqual(n["@type"], ["GardenStore", "LocalBusiness"])
        self.assertEqual((n["@id"], n["name"], n["telephone"], n["email"]),
                         (f"{SITIO}/#negocio", datos.NOMBRE, datos.TELEFONO_TEL, datos.CORREO_FORMULARIOS))
        self.assertEqual(n["address"], {"@type": "PostalAddress", "streetAddress": datos.CALLE,
                                        "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas",
                                        "postalCode": datos.CP, "addressCountry": "MX"})
        self.assertEqual((n["geo"]["latitude"], n["geo"]["longitude"]), datos.GEO)
        self.assertEqual(n["hasMap"], datos.MAPS_URL)
        self.assertEqual(n["foundingDate"], datos.FUNDACION)
        self.assertEqual([(tuple(h["dayOfWeek"]), h["opens"], h["closes"]) for h in n["openingHoursSpecification"]],
                         list(datos.HORARIO_LD))
        self.assertEqual([(a["@type"], a["name"]) for a in n["areaServed"]],
                         [("City", "Tampico"), ("City", "Ciudad Madero"), ("City", "Altamira")])
        self.assertEqual(n["identifier"]["value"], datos.REPSE)
        self.assertEqual(n["identifier"]["url"], datos.REPSE_PADRON)
        for archivo in (n["logo"], n["image"]):
            self.assertTrue(archivo_de(archivo).is_file(), archivo)
        for prohibida in ("aggregateRating", "review", "paymentAccepted"):
            self.assertNotIn(prohibida, n)

    def test_minimo_y_completo_coinciden(self):
        minimo, completo = entidad.negocio_minimo(), entidad.negocio()
        self.assertEqual(set(minimo), {"@type", "@id", "name", "url", "telephone"})
        self.assertEqual(minimo, {clave: completo[clave] for clave in minimo})

    def test_sitio_sin_buscador(self):
        s = entidad.sitio()
        self.assertEqual((s["@type"], s["@id"], s["inLanguage"], s["publisher"]),
                         ("WebSite", f"{SITIO}/#sitio", "es-MX", {"@id": f"{SITIO}/#negocio"}))
        self.assertEqual((s["name"], s["alternateName"], s["url"]), (datos.NOMBRE, datos.NOMBRE_ALTERNO, f"{SITIO}/"))
        self.assertNotIn("potentialAction", s)


class CompletarTest(unittest.TestCase):
    META = {"title": "T", "canonical": f"{SITIO}/x", "robots": "index, follow", "og": ()}

    def grafo(self, nodos_, cuerpo="", meta=None):
        (bloque,) = entidad.completar(({"@context": "https://schema.org", "@graph": nodos_},), meta or self.META, cuerpo)
        return bloque["@graph"]

    def test_pagina_sin_json_ld_recibe_su_webpage_y_las_definiciones(self):
        (bloque,) = entidad.completar((), self.META)
        pagina, negocio, sitio = bloque["@graph"]
        self.assertEqual(pagina, {"@type": "WebPage", "@id": f"{SITIO}/x", "url": f"{SITIO}/x", "name": "T",
                                  "inLanguage": "es-MX", "isPartOf": {"@id": f"{SITIO}/#sitio"},
                                  "about": {"@id": f"{SITIO}/#negocio"}})
        self.assertEqual(negocio, entidad.negocio_minimo())
        self.assertEqual(sitio, entidad.sitio_minimo())

    def test_no_repite_el_nodo_que_la_pagina_ya_define(self):
        grafo = self.grafo([entidad.negocio(), entidad.sitio()])
        self.assertEqual([n["@id"] for n in grafo if n.get("@id", "").endswith(("#negocio", "#sitio"))],
                         [f"{SITIO}/#sitio", f"{SITIO}/#negocio"][::-1])

    def test_speakable_suelto_y_del_faq_pasan_al_webpage_con_la_respuesta_primero(self):
        grafo = self.grafo([{"@type": "FAQPage", "mainEntity": [], "speakable": {"cssSelector": [".vt-faq details p"]}},
                            {"@type": "SpeakableSpecification", "cssSelector": [".vt-portada .vt-lede"]}],
                           cuerpo="<p data-vt-respuesta>x</p>")
        self.assertEqual([n["@type"] for n in grafo][:2], ["FAQPage", "WebPage"])
        self.assertNotIn("speakable", grafo[0])
        self.assertEqual(grafo[1]["speakable"], {"@type": "SpeakableSpecification", "cssSelector": [
            "[data-vt-respuesta]", ".vt-faq details p", ".vt-portada .vt-lede"]})

    def test_fecha_de_actualizacion_y_articulo_sin_about(self):
        grafo = self.grafo([{"@type": "Article", "headline": "h"}], meta={**self.META, "modificado": "2026-11-10"})
        pagina = next(n for n in grafo if n["@type"] == "WebPage")
        self.assertEqual(pagina["dateModified"], "2026-11-10")
        self.assertNotIn("about", pagina)

    def test_conserva_el_webpage_que_la_pagina_trae(self):
        propio = {"@type": "WebPage", "@id": f"{SITIO}/x", "name": "Propio", "about": {"@id": "otro"}}
        grafo = self.grafo([propio])
        self.assertEqual((grafo[0]["name"], grafo[0]["about"]), ("Propio", {"@id": "otro"}))
        self.assertEqual(grafo[0]["isPartOf"], {"@id": f"{SITIO}/#sitio"})

    def test_migas_del_json_ld_iguales_a_las_visibles(self):
        ld = entidad.migas_ld((("Inicio", "/"), ('Pasto <span class="x">sintético</span>', "/pasto-sintetico"),
                               ("Aruba 10", None)), f"{SITIO}/pasto-sintetico/aruba-10")
        self.assertEqual([(i["position"], i["name"], i["item"]) for i in ld["itemListElement"]],
                         [(1, "Inicio", f"{SITIO}/"), (2, "Pasto sintético", f"{SITIO}/pasto-sintetico"),
                          (3, "Aruba 10", f"{SITIO}/pasto-sintetico/aruba-10")])

    def test_meta_social_completa_solo_lo_que_falta_y_solo_en_indexables(self):
        meta = entidad.meta_social({**self.META, "og": (("og:title", "T"),)}, imagen="/img/favicon-192.png")
        self.assertEqual(dict(meta["og"]), {"og:title": "T", "og:url": f"{SITIO}/x", "og:locale": "es_MX",
                                            "og:image": f"{SITIO}/img/favicon-192.png", "og:site_name": datos.NOMBRE})
        self.assertEqual(meta["twitter"], (("twitter:card", "summary_large_image"),))
        propia = entidad.meta_social({**self.META, "og": (("og:site_name", "Otro"), ("og:url", "u"))})
        self.assertEqual(dict(propia["og"])["og:site_name"], "Otro")
        self.assertEqual(dict(propia["og"])["og:url"], "u")
        self.assertNotIn("og:image", dict(propia["og"]))
        self.assertEqual(propia["twitter"], (("twitter:card", "summary"),))
        oculta = {**self.META, "robots": "noindex, follow"}
        self.assertIs(entidad.meta_social(oculta), oculta)


class EntidadEnElSitioTest(unittest.TestCase):
    maxDiff = None

    def test_todas_las_paginas_tienen_json_ld_que_se_lee(self):
        self.assertEqual([p for p, h in PAGINAS.items() if not bloques(h)], [])

    def test_un_solo_negocio_con_el_mismo_tipo_nombre_y_telefono(self):
        esperado = entidad.negocio_minimo()
        fallas = []
        for pagina, html in PAGINAS.items():
            definiciones = [n for n in nodos(html) if n.get("@id") == entidad.NEGOCIO_ID and len(n) > 1]
            if len(definiciones) != 1:
                fallas.append(f"{pagina}: {len(definiciones)} definiciones de #negocio")
            for n in definiciones:
                if {clave: n.get(clave) for clave in esperado} != esperado:
                    fallas.append(f"{pagina}: #negocio distinto")
                if "aggregateRating" in n or "review" in n:
                    fallas.append(f"{pagina}: #negocio con calificación")
                if ("address" in n) != (pagina in COMPLETO_EN):
                    fallas.append(f"{pagina}: nodo completo o mínimo donde no toca")
        self.assertEqual(fallas, [])

    def test_el_nodo_completo_es_el_de_entidad(self):
        for pagina in COMPLETO_EN:
            with self.subTest(pagina=pagina):
                (nodo,) = [n for n in nodos(PAGINAS[pagina]) if n.get("@id") == entidad.NEGOCIO_ID and len(n) > 1]
                self.assertEqual(nodo, entidad.negocio())

    def test_ningun_negocio_sin_id(self):
        sueltos = [f"{pagina}: {tipos(n)} {n.get('name')}" for pagina, html in PAGINAS.items() for n in nodos(html)
                   if set(tipos(n)) & TIPOS_NEGOCIO and n.get("@id") != entidad.NEGOCIO_ID]
        self.assertEqual(sueltos, [])

    def test_sin_calificaciones_propias(self):
        for pagina, html in PAGINAS.items():
            with self.subTest(pagina=pagina):
                self.assertNotRegex(html, r'"aggregateRating"|"review"\s*:|"@type":\s*"Review"')

    def test_todo_id_nombrado_esta_definido_en_la_misma_pagina(self):
        fallas = []
        for pagina, html in PAGINAS.items():
            todos = nodos(html)
            definidos = {n["@id"] for n in todos if "@id" in n and len(n) > 1}
            fallas += [f"{pagina}: {n['@id']}" for n in todos if "@id" in n and len(n) == 1 and n["@id"] not in definidos]
        self.assertEqual(fallas, [])

    def test_home_con_sitio_y_sin_migas(self):
        html = PAGINAS["index.html"]
        (sitio,) = de_tipo(html, "WebSite")
        self.assertEqual(sitio, entidad.sitio())
        self.assertEqual(de_tipo(html, "BreadcrumbList"), [])

    def test_cada_pagina_con_un_webpage_ligado_al_sitio(self):
        for pagina, html in PAGINAS.items():
            with self.subTest(pagina=pagina):
                (nodo,) = [n for n in de_pagina(html) if len(n) > 2]
                self.assertEqual(nodo["isPartOf"], {"@id": entidad.SITIO_ID})
                self.assertEqual(nodo["inLanguage"], "es-MX")
                if "/blog/" not in f"/{pagina}" or pagina == "blog/index.html":
                    self.assertIn("about", nodo)


class ProductosTest(unittest.TestCase):
    def test_todo_producto_con_foto_real_y_oferta_con_precio_y_vendedor(self):
        fallas, total = [], 0
        for pagina, html in PAGINAS.items():
            for p in de_tipo(html, "Product"):
                total += 1
                nombre = f"{pagina} · {p.get('name')}"
                fotos = p.get("image") or []
                fotos = [fotos] if isinstance(fotos, str) else fotos
                if not fotos or not all(archivo_de(f).is_file() for f in fotos):
                    fallas.append(f"{nombre}: sin foto o con una foto que no existe")
                ofertas = p.get("offers") or []
                ofertas = [ofertas] if isinstance(ofertas, dict) else ofertas
                if not ofertas:
                    fallas.append(f"{nombre}: sin oferta")
                for o in ofertas:
                    clave = "lowPrice" if o["@type"] == "AggregateOffer" else "price"
                    if o["@type"] not in ("Offer", "AggregateOffer") or not o.get(clave) or o.get("priceCurrency") != "MXN":
                        fallas.append(f"{nombre}: oferta sin precio en MXN")
                    if o.get("seller") != entidad.REF:
                        fallas.append(f"{nombre}: oferta sin vendedor → #negocio")
        self.assertEqual(fallas, [])
        self.assertGreater(total, 30)

    def test_sin_precio_no_hay_producto(self):
        """Las especies según cotización de /palmas-mayoreo-proyectos y las categorías de /vivero-tampico no son Product."""
        con_precio = {nombre for nombre, _c, precio in datos.PALMAS_PROYECTO if precio is not None}
        productos = {p["name"]: p for p in de_tipo(PAGINAS["palmas-mayoreo-proyectos/index.html"], "Product")}
        self.assertEqual(set(productos), con_precio)
        for nombre, _c, precio in datos.PALMAS_PROYECTO:
            if precio is not None:
                self.assertEqual(productos[nombre]["offers"]["lowPrice"], precio)
                self.assertNotIn("highPrice", productos[nombre]["offers"])
        self.assertEqual(de_tipo(PAGINAS["vivero-tampico/index.html"], "Product"), [])

    def test_precios_desde_como_minimo(self):
        (palmas,) = de_tipo(PAGINAS["palmas-tropicales-tampico/index.html"], "Product")
        self.assertEqual((palmas["offers"]["@type"], palmas["offers"]["lowPrice"]),
                         ("AggregateOffer", datos.PRECIOS["palma_desde"]))
        (tezontle,) = de_tipo(PAGINAS["tezontle-rojo-tampico/index.html"], "Product")
        self.assertEqual((tezontle["offers"]["@type"], tezontle["offers"]["lowPrice"]),
                         ("AggregateOffer", datos.PRECIOS["tezontle_costal"]))
        (pasto,) = de_tipo(PAGINAS["pasto-en-rollo-tampico/index.html"], "Product")
        self.assertEqual((pasto["offers"]["@type"], pasto["offers"]["price"]), ("Offer", str(datos.PRECIOS["pasto_solo_m2"])))


class ArticulosTest(unittest.TestCase):
    def test_los_articulos_llevan_su_article_completo(self):
        self.assertEqual(len(articulo.CLAVES), 54)
        for slug in articulo.CLAVES:
            html = PAGINAS[f"blog/{slug}/index.html"]
            doc, _cuerpo = articulo.leer(slug)
            publicado, modificado = articulo.fechas(doc["jsonld"])
            with self.subTest(slug=slug):
                (nodo,) = de_tipo(html, "Article")
                for clave in ("headline", "description", "image"):
                    self.assertTrue(nodo.get(clave), clave)
                self.assertTrue(archivo_de(nodo["image"]).is_file(), nodo["image"])
                self.assertEqual((nodo["datePublished"], nodo["dateModified"]), (publicado, modificado))
                self.assertEqual(nodo["mainEntityOfPage"], {"@id": f"{SITIO}/blog/{slug}"})
                self.assertEqual((nodo["author"], nodo["publisher"]), (entidad.REF, entidad.REF))
                self.assertEqual(nodo["inLanguage"], "es-MX")
                # La firma visible sigue siendo el equipo técnico; la fecha visible es la del Article.
                self.assertIn(f"<b>Por</b> {datos.AUTOR_BLOG}", html)
                self.assertIn(f'<time datetime="{modificado}">', html)

    def test_el_sitemap_repite_la_fecha_de_cada_articulo(self):
        mapa = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        for slug in articulo.CLAVES:
            doc, _cuerpo = articulo.leer(slug)
            _publicado, modificado = articulo.fechas(doc["jsonld"])
            with self.subTest(slug=slug):
                self.assertRegex(mapa, rf"<loc>{re.escape(SITIO)}/blog/{slug}</loc>\s*<lastmod>{modificado[:10]}</lastmod>")


class SpeakableTest(unittest.TestCase):
    def test_anidado_en_el_webpage_y_apunta_a_respuestas_que_existen(self):
        con_speakable = 0
        for pagina, html in PAGINAS.items():
            with self.subTest(pagina=pagina):
                for bloque in bloques(html):
                    for n in bloque.get("@graph", [bloque]):
                        self.assertNotIn("SpeakableSpecification", tipos(n))
                        if "speakable" in n:
                            self.assertTrue(set(tipos(n)) & set(entidad.TIPOS_PAGINA), tipos(n))
                for espec in de_tipo(html, "SpeakableSpecification"):
                    con_speakable += 1
                    for selector in espec["cssSelector"]:
                        self.assertIsNone(ENCABEZADO_RE.search(selector), selector)
                        for clase in re.findall(r"\.([\w-]+)", selector):
                            self.assertRegex(html, rf'class="[^"]*\b{clase}\b')
                        for atributo in re.findall(r"\[([\w-]+)\]", selector):
                            self.assertRegex(html, rf"<[^>]*\s{atributo}[\s>]")
        self.assertGreaterEqual(con_speakable, 18)

    def test_las_paginas_con_respuesta_la_nombran_primero(self):
        for pagina, html in PAGINAS.items():
            if "data-vt-respuesta" in html:
                with self.subTest(pagina=pagina):
                    (espec,) = de_tipo(html, "SpeakableSpecification")
                    self.assertEqual(espec["cssSelector"][0], "[data-vt-respuesta]")


class MigasTest(unittest.TestCase):
    def test_las_migas_del_json_ld_son_las_visibles(self):
        con_migas = 0
        for pagina, html in PAGINAS.items():
            listas = de_tipo(html, "BreadcrumbList")
            if not listas:
                continue
            con_migas += 1
            with self.subTest(pagina=pagina):
                (lista,) = listas
                visibles = re.search(r'<nav class="vt-crumbs"[^>]*>(.*?)</nav>', html, re.S)
                self.assertIsNotNone(visibles, "BreadcrumbList sin migas visibles")
                textos = [plano(x) for x in re.findall(r"<li\b[^>]*>(.*?)</li>", visibles.group(1), re.S)]
                self.assertEqual([i["name"] for i in lista["itemListElement"]], textos)
                self.assertEqual([i["position"] for i in lista["itemListElement"]], list(range(1, len(textos) + 1)))
                self.assertTrue(all(i["item"].startswith(SITIO) for i in lista["itemListElement"]))
        self.assertGreater(con_migas, 100)


class OpenGraphTest(unittest.TestCase):
    def test_las_indexables_llevan_la_tarjeta_completa_con_una_imagen_que_existe(self):
        for pagina, html in PAGINAS.items():
            if not indexable(html):
                continue
            with self.subTest(pagina=pagina):
                puestas = dict(re.findall(r'<meta (?:property|name)="((?:og|twitter):[^"]+)" content="([^"]*)"', html))
                for clave in ("og:image", "og:locale", "og:url", "og:site_name", "twitter:card"):
                    self.assertTrue(puestas.get(clave), clave)
                self.assertTrue(archivo_de(puestas["og:image"]).is_file(), puestas["og:image"])
                self.assertEqual(puestas["og:locale"], "es_MX")


if __name__ == "__main__":
    unittest.main()
