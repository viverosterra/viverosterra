"""Páginas de plantas con plantilla (Etapa 2e): secuencia del spec, precios de datos.py, fotos de especie como en main
(decisión del dueño, 2026-11-08: FOTOS_RETIRADAS y plantas_comun.FOTOS_SOLO_CATALOGO vacías), mensajes, enlaces y
JSON-LD."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402
from contenido import plantas_comun as pc  # noqa: E402

PUBLIC = paginas.PUBLIC
# Texto del enlace a la guía del blog (revisión 2e: era «Las palmas más vendidas…»). Es el título de la guía de
# precios, no una afirmación sobre las tarjetas; fuera de ese enlace «más pedidas» sigue sin ir.
GUIA_PALMAS = "Las palmas más pedidas en Tampico: guía de precios"


def html(ruta):
    return (PUBLIC / dict((r, s) for r, s, _p, _c in generar.PAGINAS)[ruta]).read_text(encoding="utf-8")


def grafo(h):
    return [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
            for n in json.loads(b).get("@graph", [])]


def mensajes(h):
    return [unquote(t) for t in re.findall(r'href="https://wa\.me/\d+\?text=([^"]*)"', h)]


class HubTest(unittest.TestCase):
    RUTA = "/plantas-palmas-arboles-tampico"

    def setUp(self):
        self.h = html(self.RUTA)

    def test_orden_de_secciones_del_spec(self):
        ids = ["vt-h1", "vt-h-necesidad", "vt-h-subcategorias", "vt-h-destacadas", "vt-h-lista", "vt-h-garantia",
               "vt-h-faq", "vt-cierre-titulo"]
        posiciones = [self.h.index(f'id="{i}"') for i in ids]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_hoja_de_plantas_sin_css_viejo_ni_proxy(self):
        self.assertIn('<body class="vt-pagina vt-plantas">', self.h)
        self.assertIn("/css/terra-plantas.", self.h)
        for viejo in ("tailwind.css", "design-system.css", "servicios.css", "fonts.googleapis", "/api/img"):
            self.assertNotIn(viejo, self.h)

    def test_necesidades_enlazan_el_catalogo_con_filtro(self):
        for filtro in ("luz=sol", "luz=media,sombra", "uso=salitre", "tam=chica", "tam=mediana", "tam=grande"):
            self.assertIn(f'href="/catalogo?{filtro}"', self.h)

    def test_subcategorias_con_desde_de_datos_o_segun_cotizacion(self):
        self.assertIn('href="/palmas-tropicales-tampico"', self.h)
        self.assertEqual(self.h.count("Precio según cotización"), 3)
        self.assertEqual(len(re.findall(r'<p class="vt-indice__desde">desde', self.h)), 2)

    def test_cada_whatsapp_lleva_su_plantilla_y_la_firma(self):
        propios = [m for m in mensajes(self.h) if "Plantas que busco: ___" in m]
        self.assertGreaterEqual(len(propios), 2)  # portada y cierre
        self.assertTrue(all(m.endswith(datos.FIRMA) for m in mensajes(self.h)))

    def test_sin_afirmaciones_que_el_dueno_no_confirmo(self):
        # La Huasteca del cuadro de datos es el pasto instalado; aquí se prueba la entrega que el dueño no confirmó.
        for viejo in ("Huasteca y zonas", "Pánuco", "grúa", "Más vendidas", "más pedidas", "Martha R.", "Constructora Arce", "gratis",
                      "sin costo", "framboyán", "Framboyán"):
            self.assertNotIn(viejo, self.h.replace("/blog/framboyan-", "").replace(GUIA_PALMAS, ""))

    def test_sin_escenas_de_resort_en_las_fotos(self):
        for slug in pc.FOTOS_SOLO_CATALOGO:
            self.assertNotIn(f"/img/catalogo/{slug}-tampico.webp", self.h)

    # Fotos de Drive de las tarjetas del hub de main (/api/img?id=…), en su orden; la de "Tabachín" (la foto de la
    # tronadora) no va: esa tarjeta solo afirmaba un precio sin confirmar.
    FOTOS_MAIN = ("12Q_2nhBba8CGei_eHrUAUSZognx9OP6O", "157tCw_yF6zs2npPx4BmisT-vMu7-Hca0",
                  "1f9yY6hRqr0lf47QeunWBgNR_RXqZHHZM", "1Pp66DaLg1hg0YvVA6ZUxpT8hkgmCcdKJ",
                  "1rD9tgujODXJ03znMkru4eB1wvMuardSJ", "1VQ2urkzIqBFO4rZeKHQpe-c3X9TViVWJ",
                  "1-FRocM765ANJ2RYgxf7KKoKpno23TwwO", "1kIwetkOcVkm7Wb7xvVaEeMcvAdl_nDMO",
                  "1pqmt1VfOkeKrpoETiYFwsXwA58WHEjdu", "1aSLqV6wIrI5GjRUoKH1WWfrA9LVjNhLC",
                  "1FavAREwVmwV-ePnTOILuldS15VbjNkbj", "1yO3frSlCRK5EfSBueH7_UFE56o6vnL4b",
                  "1AP3FbBUp3js1lZnSHmw8QPFemXzBkXww", "1DaHl79oILg8OBCpYUSTVNAHAP1DH_IQl",
                  "1PQHRsGnbn6G5-0s93wNV9B8iLp_AHf5Y", "1Wg2HzkOME_lMfSEbODYp0P9EAiX0ir08")

    def test_tarjetas_con_las_fotos_de_main_en_su_orden(self):
        """Decisión del dueño (2026-11-08): las fotos de especie quedan como en main (la misma foto de Drive, en local)."""
        por_drive = {e["drive"]: e["slug"] for e in cd.ESPECIES}
        esperadas = [f"/img/catalogo/{por_drive[i]}-tampico.webp" for i in self.FOTOS_MAIN]
        tarjetas = re.findall(r'<li class="vt-esp"><figure class="vt-esp__foto"><img src="([^"]+)"', self.h)
        self.assertEqual(tarjetas, esperadas)

    def test_figuras_sin_numero_repetido(self):
        numeros = re.findall(r"<figcaption>(?:<span>)?<b>Fig\. (\d+)</b>", self.h)
        self.assertGreater(len(numeros), 8)
        self.assertEqual(len(numeros), len(set(numeros)))

    def test_json_ld_sin_localbusiness_recortado(self):
        tipos = {n["@type"] for n in grafo(self.h)}
        self.assertTrue({"FAQPage", "BreadcrumbList", "ItemList"} <= tipos)
        self.assertNotIn("LocalBusiness", tipos)


SUBCATEGORIAS = ("/palmas-tropicales-tampico", "/plantas-para-jardin-tampico", "/arboles-ornamentales-tampico",
                 "/arboles-para-banqueta-tampico", "/plantas-de-interior-tampico")


class SubcategoriasTest(unittest.TestCase):
    def test_migas_al_hub(self):
        for ruta in SUBCATEGORIAS:
            with self.subTest(ruta=ruta):
                self.assertIn('<li><a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a></li>', html(ruta))

    def test_cada_especie_con_foto_publicable(self):
        """Cada especie con su foto local del catálogo (la de main), nunca el marcador «Foto pendiente»; el pie no dice
        «En nuestro vivero» (FOTOS_VIVERO_CONFIRMADAS está vacía hasta que el dueño confirme)."""
        for ruta in SUBCATEGORIAS:
            h = html(ruta)
            tarjetas = re.findall(r'<li class="vt-esp">(.*?)</li>', h, re.S)
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(len(tarjetas), 6)
                self.assertNotIn("Foto pendiente", h)
                for t in tarjetas:
                    src = re.search(r'<img src="(/img/catalogo/([a-z0-9-]+)-tampico\.webp)" width="\d+" height="\d+"', t)
                    self.assertIsNotNone(src)
                    self.assertTrue((PUBLIC / src.group(1).lstrip("/")).exists())
                    self.assertNotIn(src.group(2), pc.FOTOS_SOLO_CATALOGO)
                    self.assertRegex(t, r"<figcaption><b>Fig\. \d{2}</b> · [^<]+</figcaption>")
                    self.assertNotIn("En nuestro vivero", t)

    def test_etiqueta_con_desde_de_datos_o_segun_cotizacion(self):
        for ruta, desde in datos.DESDE_PLANTAS.items():
            etiqueta = re.search(r'<p class="vt-etiqueta__precio">(.*?)</p>', html(ruta), re.S).group(1)
            with self.subTest(ruta=ruta):
                self.assertIn(f"${desde}" if desde else "según cotización", etiqueta.lower())

    def test_palmas_con_la_tabla_del_dueno(self):
        h = html("/palmas-tropicales-tampico")
        self.assertIn(datos.PALMAS_PRECIO, h)
        for nombre, precio in (("Palma Areca", "$250"), ("Coco Plumoso", "$250"), ("Palma Real", "$500")):
            self.assertRegex(h, rf"<b>{nombre}</b>.*?{re.escape(precio)}")
        self.assertIn("Según cotización", h)

    def test_flamboyan_desde_250_en_ornamentales(self):
        self.assertIn("Flamboyán desde $250", html("/arboles-ornamentales-tampico"))

    def test_sin_afirmaciones_que_el_dueno_no_confirmo(self):
        for ruta in SUBCATEGORIAS:
            h = html(ruta)
            for viejo in ("Huasteca y zonas", "Pánuco", "grúa", "Más vendidas", "más pedidas", "gratis", "sin costo",
                          "existencia", "Framboyán", "framboyán"):
                with self.subTest(ruta=ruta, texto=viejo):
                    self.assertNotIn(viejo, h.replace(GUIA_PALMAS, ""))

    def test_mensaje_propio_y_firma(self):
        for ruta in SUBCATEGORIAS:
            ms = mensajes(html(ruta))
            with self.subTest(ruta=ruta):
                self.assertIn(datos.con_firma(mensajes_paginas.PLANTAS[ruta]), ms)
                self.assertTrue(all(m.endswith(datos.FIRMA) for m in ms))


class CatalogoTest(unittest.TestCase):
    def setUp(self):
        self.h = html("/catalogo")

    def test_orden_buscador_rejilla_pedido_garantia(self):
        orden = ['id="vt-h1"', "data-vt-filtros", "data-vt-rejilla", "data-vt-especial", "/politicas#garantia-plantas"]
        posiciones = [self.h.index(x) for x in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_rejilla_completa_sin_proxy_ni_js_en_linea(self):
        self.assertEqual(self.h.count('data-vt-agregar="'), 117)
        self.assertNotIn("/api/img", self.h)
        self.assertNotIn("function sendWA", self.h)
        self.assertNotIn("onclick=", self.h)
        self.assertIn('<script src="/js/vt-catalogo.js" defer></script>', self.h)
        self.assertIn('<script type="application/json" id="vt-catalogo-datos">', self.h)

    def test_datos_del_js_con_el_contrato(self):
        crudo = re.search(r'<script type="application/json" id="vt-catalogo-datos">(.*?)</script>', self.h, re.S).group(1)
        especies = json.loads(crudo)
        self.assertEqual(len(especies), 117)
        self.assertEqual(set(especies["palma-real"]), {"name", "sc", "sz"})

    def test_sin_las_cifras_ni_la_pestana_de_pasto_de_main(self):
        for viejo in ("Productor directo", "disponibilidad real", "Proyectos entregados", "+200,000 m²", "+ Vendido",
                      "setTab(", "Más vendidas", "gratis", "sin costo"):
            self.assertNotIn(viejo, self.h)

    def test_las_117_con_foto_y_sin_decir_del_vivero(self):
        """Decisión del dueño (2026-11-08): ninguna tarjeta queda con «Foto pendiente»."""
        self.assertEqual(self.h.count("Foto pendiente"), 0)
        self.assertEqual(self.h.count('src="/img/catalogo/'), 117)
        self.assertNotIn("En nuestro vivero", self.h)

    def test_json_ld_itemlist_con_117(self):
        lista = next(n for n in grafo(self.h) if n["@type"] == "ItemList")
        self.assertEqual(lista["numberOfItems"], 117)
        elementos = lista["itemListElement"]
        self.assertEqual([e["position"] for e in elementos], list(range(1, 118)))
        for e in elementos:
            ancla = e["url"].split("#", 1)[1]
            with self.subTest(especie=e["name"]):
                self.assertTrue(e["url"].startswith("https://www.viverosterra.com/catalogo#"))
                self.assertIn(f'<li class="vt-esp vt-cat" id="{ancla}" ', self.h)

    def test_meta_sin_disponibles_y_h1_sin_punto(self):
        self.assertIn('<meta property="og:site_name" content="Viveros Terra">', self.h)
        self.assertNotRegex(self.h, r'<meta property="og:description" content="[^"]*disponibles')
        self.assertIn('<h1 id="vt-h1">Catálogo de Plantas, Palmas y Árboles en Tampico</h1>', self.h)


NEGOCIO = "https://www.viverosterra.com/#negocio"


class JsonLdNegocioTest(unittest.TestCase):
    """Revisión 2e: cada página de plantas nombra la entidad única #negocio por @id (el motivo de paridad del
    LocalBusiness de main lo dice), y la oferta de palmas es un mínimo con PriceSpecification y seller."""

    def test_webpage_con_about_y_publisher(self):
        for ruta in ("/plantas-palmas-arboles-tampico", *SUBCATEGORIAS, "/catalogo"):
            pagina = next(n for n in grafo(html(ruta)) if n["@type"] == "WebPage")
            with self.subTest(ruta=ruta):
                self.assertEqual(pagina["@id"], f"https://www.viverosterra.com{ruta}")
                self.assertEqual(pagina["about"], {"@id": NEGOCIO})
                self.assertEqual(pagina["publisher"], {"@id": NEGOCIO})

    def test_oferta_de_palmas_con_minimo_y_vendedor(self):
        producto = next(n for n in grafo(html("/palmas-tropicales-tampico")) if n["@type"] == "Product")
        self.assertEqual(producto["offers"], {
            "@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 250, "priceCurrency": "MXN"},
            "seller": {"@id": NEGOCIO}})

    def test_garantia_de_30_dias_siempre_con_condiciones(self):
        """Toda frase que menciona la garantía de arraigo (visible, meta o JSON-LD) dice «con condiciones» o enlaza
        las condiciones (datos.GARANTIA_PLANTAS dice «ver condiciones»)."""
        for ruta in ("/plantas-palmas-arboles-tampico", *SUBCATEGORIAS):
            h = html(ruta)
            texto = re.sub(r"<[^>]+>", " ", h)
            for frase in re.findall(r"[^.<>\"]*garantía de arraigo[^.<>\"]*[.\"]?", texto):
                with self.subTest(ruta=ruta, frase=frase.strip()[:80]):
                    self.assertRegex(frase, r"condiciones|no aplica")


if __name__ == "__main__":
    unittest.main()
