"""Página de temporada de Nochebuenas: textos del dueño, tabla estática, marcado que espera vt-nochebuenas.js, JSON-LD, los
tres modos y la configuración de URL (vercel.json, sitemap, llms.txt)."""
import html
import json
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import componentes as c  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402
from contenido import nochebuenas as contenido  # noqa: E402
from contenido.nochebuenas_fotos import FOTOS  # noqa: E402
from plantillas import nochebuenas as plantilla  # noqa: E402

NB = datos.NOCHEBUENAS
RUTA = NB["ruta"]
URL = datos.SITIO + RUTA
RAIZ = paginas.PUBLIC.parent
TITULO = "Nochebuenas en Tampico desde $65 · Mayoreo 2026 | Viveros Terra"
DESCRIPCION = ('Nochebuena roja, rosa y jaspeada en 5", 6", 7", colgante y macetón. Precio por volumen, factura y entrega en '
               "Tampico, Madero y Altamira.")
PROHIBIDAS = ("gratis", "gratuit", "sin costo", "sin cargo", "garantia", "garantía", "garantias", "garantías", "reponemos", "reposición", "con iva", "oasis", "paraíso",
              "mágico", "transformar", "increíble", "espectacular", "sueño", "más vendido")
NOMBRES_OPINIONES = ("Carlos Herrera", "María Fernanda Ruiz", "Raúl Sánchez", "Adriana Morales")


def completa():
    return generar.renderizar(RUTA, "nochebuenas", "nochebuenas", activos.urls())


def modo(nombre):
    return plantilla.render(contenido.CONTENIDO, modo=nombre)


def texto(fragmento):
    limpio = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", fragmento, flags=re.S | re.I)
    limpio = re.sub(r"<!--.*?-->", " ", limpio, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", limpio))).strip()


def cuerpo(pagina):
    return re.search(r"<body\b.*</body>", pagina, re.S).group(0)


def grafo(pagina):
    bloques = re.findall(r'<script type="application/ld\+json">(.*?)</script>', pagina, re.S)
    return [n for b in bloques for n in json.loads(b)["@graph"]]


def productos(pagina):
    return [n for n in grafo(pagina) if n["@type"] == "Product"]


class MetaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = completa()

    def test_titulo_descripcion_y_canonical_exactos(self):
        self.assertIn(f"<title>{TITULO}</title>", self.html)
        self.assertEqual(html.unescape(re.search(r'<meta name="description" content="([^"]*)"', self.html).group(1)), DESCRIPCION)
        self.assertIn(f'<link rel="canonical" href="{URL}">', self.html)
        self.assertIn('<meta name="robots" content="index, follow">', self.html)

    def test_geo_de_tampico_y_sin_declaracion_de_ia(self):
        self.assertEqual(self.html.count('name="geo.region"'), 1)
        self.assertIn('<meta name="geo.region" content="MX-TAM">', self.html)
        self.assertEqual(self.html.count('name="geo.placename"'), 1)
        self.assertIn('<meta name="geo.placename" content="Tampico">', self.html)
        self.assertNotIn("ai-content-declaration", self.html)

    def test_open_graph_con_la_foto_principal(self):
        hero = next(f for f in FOTOS if f["uso"] == "hero")
        imagen = re.search(r'<meta property="og:image" content="([^"]*)"', self.html).group(1)
        self.assertTrue(imagen.startswith(datos.SITIO + "/img/nochebuenas/"))
        self.assertIn(Path(imagen).name.replace("-1600", "-800"), hero["src"])

    def test_hoja_propia_y_script_del_cotizador(self):
        self.assertIn('<body class="vt-pagina vt-nochebuenas">', self.html)
        self.assertIn("/css/terra-nochebuenas.", self.html)
        self.assertIn('<script src="/js/vt-nochebuenas.js" defer></script>', self.html)


class ContenidoVisibleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = completa()
        cls.visible = texto(cuerpo(cls.html))
        cls.main = re.search(r"<main\b.*</main>", cls.html, re.S).group(0)

    def test_hero_literal(self):
        for frase in ("Temporada 2026 · Pedidos abiertos", "Nochebuenas 2026 en Tampico: menudeo y mayoreo",
                      "Desde $65 por pieza en volumen · Factura CFDI · Entrega en Tampico, Madero y Altamira",
                      "Cotizar mi pedido"):
            with self.subTest(frase=frase):
                self.assertIn(frase, self.visible)
        self.assertRegex(self.main, r'<a [^>]*href="#cotizador"[^>]*>Cotizar mi pedido')
        portada = self.main[:self.main.index("</section>")]
        self.assertIn("https://wa.me/", portada)

    def test_franja_de_la_portada(self):
        portada = texto(self.main[:self.main.index("</section>")])
        for dato in (str(datos.DESDE), datos.GOOGLE, datos.FACTURA, "A domicilio"):
            with self.subTest(dato=dato):
                self.assertIn(dato, portada)

    def test_sin_palabras_prohibidas_ni_iva_en_toda_la_pagina(self):
        minusculas = self.visible.lower()
        for palabra in PROHIBIDAS:
            with self.subTest(palabra=palabra):
                self.assertNotIn(palabra, minusculas)

    def test_sin_otros_esquemas_de_pago(self):
        for patron in (r"\b30\s?%", r"\b40\s?%", r"\bresto\b"):
            with self.subTest(patron=patron):
                self.assertIsNone(re.search(patron, self.visible, re.I))

    def test_sin_afirmaciones_retiradas(self):
        for frase in ("Para lobbies, terrazas y mesas", "Para centros de mesa", "pide sombra clara", "Dinos dónde van",
                      "que puedes visitar", "de nuestro vivero", "En nuestro vivero"):
            with self.subTest(frase=frase):
                self.assertNotIn(frase, self.visible)
        self.assertIn("Fotos reales de temporadas anteriores", self.visible)
        self.assertIn("Con el calor de la costa, cuida la luz y el riego.", self.visible)

    def test_etiqueta_del_hero_muestra_la_condicion_en_una_fila(self):
        portada = self.main[:self.main.index("</section>")]
        filas = [texto(f) for f in re.findall(r'<p class="vt-etiqueta__fila">.*?</p>', portada, re.S)]
        self.assertEqual(filas, ['Maceta 5", menudeo $89', "Mayoreo, 12 piezas $75", "200 piezas o más $65"])
        self.assertNotIn("vt-etiqueta__nota", portada)

    def test_sin_opiniones_con_nombre(self):
        for nombre in NOMBRES_OPINIONES:
            self.assertNotIn(nombre, self.visible)

    def test_sin_emojis_en_la_interfaz(self):
        self.assertEqual(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", self.visible), [])

    def test_secciones_en_el_orden_del_spec(self):
        marcas = ('id="cotizador"', "vt-h-precios", "vt-h-para", "vt-h-galeria", "vt-h-confianza", "vt-h-como", "vt-h-cuidados",
                  "vt-h-faq", "vt-h-datos", "vt-cierre-titulo")
        posiciones = [self.main.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_tabla_estatica_generada_de_datos(self):
        tabla = re.search(r"<table\b.*?</table>", self.main, re.S).group(0)
        self.assertIn("<caption>", tabla)
        encabezados = [texto(h) for h in re.findall(r"<thead>.*?</thead>", tabla, re.S)]
        for columna in ("Tamaño", "1–11 pzas", "12–49", "50–199", "200+"):
            self.assertIn(columna, encabezados[0])
        for p in NB["productos"]:
            fila = next(f for f in re.findall(r"<tr>.*?</tr>", tabla, re.S) if html.escape(p["nombre"], quote=True) in f or p["nombre"] in f)
            for precio in p["precios"]:
                self.assertIn(c.dinero(precio), fila)
        self.assertIn("$1,195", texto(tabla))
        self.assertIn("$65", texto(tabla))
        self.assertIn("Los escalones se calculan con el total del pedido: puedes combinar tamaños y colores. Mismo precio en roja, "
                      "rosa y jaspeada.", self.visible)

    def test_preguntas_literales(self):
        for frase in ("En Viveros Terra, desde $89 la de 5 pulgadas en menudeo y desde $65 en pedidos de 200 piezas o más.",
                      "Desde 12 piezas, sumando tamaños y colores. $75 la de 5\" y $119 la de 6\".",
                      'Maceta 5" $89 y $75', 'Maceta 6" $139 y $119', 'Maceta 7" $199 y $169', "Colgante $339 y $279",
                      'Macetón 12" sobre pedido, desde $865', "$3,500", "te la cotizamos por WhatsApp", "CFDI 4.0",
                      "Lo antes posible. Confírmanos por WhatsApp y te decimos la fecha de entrega.",
                      "antes del 30 de noviembre", "antes del 12 de diciembre", "hasta febrero", "18–24 °C",
                      "cubremaceta", "aire acondicionado", "veterinario", "mismo precio que la roja"):
            with self.subTest(frase=frase):
                self.assertIn(frase, self.visible)

    def test_preguntas_visibles_sin_details(self):
        faq = self.main[self.main.index("vt-h-faq"):]
        faq = faq[:faq.index("</section>")]
        self.assertNotIn("<details", faq)
        self.assertEqual(len(re.findall(r"<h3\b", faq)), len(contenido.PREGUNTAS))
        self.assertNotIn("30 de noviembre", texto(faq))

    def test_como_funciona_y_fechas_que_se_ocultan(self):
        for frase in ("Cotizas en línea", "Confirmas y apartas por WhatsApp", "50% de anticipo en mayoreo y en precio preventa",
                      "Recibes en tu domicilio o recoges en el vivero"):
            with self.subTest(frase=frase):
                self.assertIn(frase, self.visible)
        self.assertRegex(self.main, r'data-nb-hasta="2026-11-30"[^>]*>Precio preventa hasta el 30 de noviembre<')
        self.assertRegex(self.main, r'data-nb-hasta="2026-11-30"[^>]*>Mayoreo con entrega antes del 12 de diciembre: confirma antes '
                                    r"del 30 de noviembre<")

    def test_seis_destinatarios_con_cta_propio(self):
        seccion = self.main[self.main.index("vt-h-para"):]
        seccion = seccion[:seccion.index("</section>")]
        self.assertEqual(seccion.count("Mínimo sugerido: 12 piezas"), 6)
        self.assertEqual(seccion.count("Pide antes del 30 de noviembre"), 6)
        enlaces = re.findall(r'<a [^>]*data-cta="(nochebuenas:[^"]+)"[^>]*href="(https://wa\.me/[^"]+)"', seccion)
        self.assertEqual(len(enlaces), 6)
        self.assertEqual(len({cta for cta, _ in enlaces}), 6)
        self.assertEqual(len({href for _, href in enlaces}), 6)
        for titulo in ("Empresas y regalos corporativos", "Hoteles y restaurantes", "Plazas y comercios", "Gobierno y ayuntamientos",
                       "Posadas y eventos", "Iglesias y escuelas"):
            self.assertIn(titulo, seccion)
        for frase in ("empaque kraft", "varios domicilios", "instalación y mantenimiento", "cotización formal", "12 de diciembre"):
            self.assertIn(frase, texto(seccion).lower())

    def test_confianza_sin_decir_que_compraron_nochebuenas(self):
        seccion = self.main[self.main.index("vt-h-confianza"):]
        seccion = seccion[:seccion.index("</section>")]
        plano = texto(seccion)
        self.assertIn(datos.GOOGLE, plano)
        self.assertIn(datos.FACTURA, plano)
        self.assertIn("Empresas e instituciones que han confiado en Viveros Terra", plano)
        self.assertIn('class="vt-logos"', seccion)
        self.assertNotIn("nochebuena", plano.lower().replace("nochebuenas 2026", ""))
        self.assertNotIn("Vivero, pasto en rollo y jardinería", plano)

    def test_datos_de_la_nochebuena(self):
        seccion = self.main[self.main.index("vt-h-datos"):]
        seccion = seccion[:seccion.index("</section>")]
        plano = texto(seccion)
        for frase in ("originaria de México", "8 de diciembre", "Día Nacional de la Nochebuena", "Morelos", "principal productor",
                      "según datos de la Secretaría de Agricultura citados por El Siglo de Torreón (2023)"):
            with self.subTest(frase=frase):
                self.assertIn(frase, plano)
        self.assertNotRegex(plano, r"\d+\s?%")
        self.assertIn("https://www.elsiglodetorreon.com.mx/noticia/2023/floricultores-alistan-cosecha-de-nochebuena-para-cubrir-"
                      "proxima-demanda-nacional-sader.html", seccion)

    def test_cierre_con_contacto_y_actualizacion(self):
        cierre = self.main[self.main.index("vt-cierre-titulo"):]
        plano = texto(cierre)
        for frase in (datos.DOMICILIO_COMPLETO, datos.HORARIO, "Última actualización: 8 de noviembre de 2026"):
            with self.subTest(frase=frase):
                self.assertIn(frase, plano)
        self.assertIn(datos.MAPS_URL, cierre)
        self.assertIn("https://wa.me/", cierre)

    def test_pie_sin_iva_solo_en_esta_pagina(self):
        ctx = paginas.contexto(RUTA)
        self.assertNotIn("con IVA", partials.footer(ctx))
        self.assertNotIn("Precios 2026", partials.footer(ctx))
        # SEO fase 0 (2026-11-10): el pie de las demás páginas dice "Precios 2026" a secas; el IVA se explica junto a
        # cada precio (el pasto sin instalar, las plantas, los árboles y las palmas no lo llevan).
        otro = partials.footer(paginas.contexto("/plantas-palmas-arboles-tampico"))
        self.assertIn(f"Tamaulipas · Precios {datos.ANIO}</p>", otro)
        self.assertNotIn("IVA", otro)

    def test_menu_y_pie_llevan_nochebuenas_en_todo_el_sitio(self):
        ctx = paginas.contexto("/")
        self.assertIn(f'<a href="{RUTA}">Nochebuenas</a>', partials.header(ctx))
        self.assertIn(f'<a href="{RUTA}">Nochebuenas</a>', partials.footer(ctx))


class FotosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = completa()
        cls.main = re.search(r"<main\b.*</main>", cls.html, re.S).group(0)
        cls.imagenes = re.findall(r'<img\b[^>]*src="/img/nochebuenas/[^>]*>', cls.main)

    def test_hero_precargada_y_sin_lazy(self):
        hero = next(f for f in FOTOS if f["uso"] == "hero")
        self.assertRegex(self.html, rf'<link rel="preload" as="image" href="{re.escape(hero["src"])}"')
        etiqueta = next(i for i in self.imagenes if hero["src"] in i)
        self.assertNotIn('loading="lazy"', etiqueta)

    def test_las_demas_lazy_con_srcset_sizes_y_medidas(self):
        hero = next(f for f in FOTOS if f["uso"] == "hero")
        otras = [i for i in self.imagenes if hero["src"] not in i]
        self.assertEqual(len(otras), len(FOTOS) - 1)
        for i in otras:
            for atributo in ('loading="lazy"', "srcset=", "sizes=", "width=", "height="):
                with self.subTest(atributo=atributo, img=i[:60]):
                    self.assertIn(atributo, i)

    def test_rotulos_visibles(self):
        visible = texto(self.main)
        for f in FOTOS:
            with self.subTest(foto=f["id"]):
                self.assertIn(f["rotulo"], visible)
        self.assertIn("Pedido de volumen listo para entregar", visible)


class CotizadorMarcadoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = completa()
        inicio = cls.html.index('data-nb-cotizador')
        cls.caja = cls.html[inicio:cls.html.index("vt-h-precios")]

    def test_sin_form_y_dentro_de_cotizador(self):
        self.assertIn('id="cotizador"', self.html)
        self.assertLess(self.html.index('id="cotizador"'), self.html.index("data-nb-cotizador"))
        self.assertNotIn("<form", self.caja)

    def test_config_incrustada_con_los_datos_y_el_numero(self):
        crudo = re.search(r'<script type="application/json" id="nb-config">(.*?)</script>', self.html, re.S).group(1)
        self.assertNotIn("<", crudo)
        cfg = json.loads(crudo)
        self.assertEqual(cfg["wa"], datos.TELEFONO_WA)
        self.assertEqual(cfg["cortes"], list(NB["cortes"]))
        self.assertEqual([p["clave"] for p in cfg["productos"]], ["5", "6", "7", "8", "colgante", "12"])
        self.assertEqual(cfg["preventa"]["hasta"], NB["preventa"]["hasta"])
        self.assertEqual(cfg["anticipo_pct"], 50)
        self.assertEqual(NB["entrega_mayoreo_antes"], "2026-12-12")

    def test_fila_inicial(self):
        self.assertEqual(self.caja.count("data-nb-linea"), 1)
        fila = self.caja[self.caja.index("data-nb-linea"):]
        fila = fila[:fila.index('data-nb-accion="agregar"')]
        self.assertRegex(fila, r'<select data-nb-campo="producto">')
        self.assertRegex(fila, r'<option value="6" selected>')
        self.assertRegex(fila, r'<select data-nb-campo="variedad">')
        self.assertRegex(fila, r'<option value="Roja" selected>')
        self.assertRegex(fila, r'<input [^>]*type="number"[^>]*data-nb-campo="cantidad"[^>]*value="1"')
        for accion in ("menos", "mas", "quitar"):
            self.assertRegex(fila, rf'<button type="button"[^>]*data-nb-accion="{accion}"[^>]*aria-label="')
        self.assertIn('data-nb-o="subtotal"', fila)
        self.assertNotRegex(fila, r'\b(?:id|for)="')
        for etiqueta in re.findall(r"<label\b.*?</label>", fila, re.S):
            self.assertRegex(etiqueta, r"<(select|input)\b")
            self.assertNotIn("<button", etiqueta)

    def test_controles_opcionales_y_salidas(self):
        for nombre in ("zona", "fecha", "tipo", "factura"):
            self.assertIn(f'data-nb-campo="{nombre}"', self.caja)
        self.assertRegex(self.caja, r'<input [^>]*type="date"[^>]*data-nb-campo="fecha"')
        self.assertRegex(self.caja, r'<input [^>]*type="checkbox"[^>]*data-nb-campo="factura"')
        for salida in ("total", "escalon", "ahorro", "nudge", "preventa", "entrega", "sobre-pedido", "proyecto", "piezas", "desglose",
                       "vacio", "maximo", "tope", "unitario"):
            with self.subTest(salida=salida):
                self.assertIn(f'data-nb-o="{salida}"', self.caja)
        self.assertRegex(self.caja, r'<button type="button"[^>]*data-nb-accion="agregar"')

    def test_campos_opcionales_cerrados_y_selector_sin_aviso(self):
        self.assertRegex(self.caja, r'<details class="vt-nb-extras" data-nb-extras><summary><span aria-hidden="true">▾&nbsp;</span>Para afinar tu cotización \(opcional\)</summary>')
        self.assertNotIn("(sobre pedido)", self.caja)

    def test_avisos_debajo_del_boton_y_ticket_enlazable(self):
        self.assertIn('id="nb-ticket"', self.caja)
        cta = self.caja.index('data-cta="nochebuenas:cotizador"')
        self.assertLess(self.caja.index('data-nb-o="total"'), cta)
        for salida in ("nudge", "ahorro", "preventa", "entrega", "sobre-pedido", "proyecto", "maximo"):
            with self.subTest(salida=salida):
                self.assertGreater(self.caja.index(f'data-nb-o="{salida}"'), cta)
        self.assertRegex(self.caja, r'class="vt-nb-avisos" aria-live="polite"')
        self.assertRegex(self.caja, r'id="nb-aviso-vacio"[^>]*data-nb-o="vacio"')
        self.assertRegex(self.caja, r'<button type="button"[^>]*data-nb-accion="subir"[^>]*hidden')

    def test_enlace_funciona_sin_js(self):
        a = re.search(r'<a [^>]*data-cta="nochebuenas:cotizador"[^>]*>', self.caja).group(0)
        self.assertIn('href="https://wa.me/' + datos.TELEFONO_WA, a)
        self.assertIn(c.esc("Nochebuenas").replace(" ", "%20"), a)

    def test_barra_fuera_de_main(self):
        barra = self.html.index("data-nb-bar")
        self.assertGreater(barra, self.html.index("</main>"))
        self.assertRegex(self.html[barra - 200:barra + 300], r'href="#cotizador"')
        self.assertRegex(self.html[barra:barra + 300], r"data-nb-bar[^>]*hidden")
        self.assertRegex(self.html[barra:barra + 300], r">Cotizar mi pedido</a>")
        self.assertIn("data-nb-total-barra", self.html)
        self.assertNotIn("data-vt-bar", self.html)


class JsonLdTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = completa()
        cls.nodos = grafo(cls.html)

    def test_grafo_completo(self):
        tipos = [n["@type"] for n in self.nodos]
        self.assertEqual(tipos.count("Product"), 6)
        # SEO fase 1: el negocio es la entidad única, de tipo GardenStore + LocalBusiness.
        for tipo in ("WebPage", "FAQPage", "BreadcrumbList", ["GardenStore", "LocalBusiness"]):
            self.assertEqual(tipos.count(tipo), 1)
        pagina = next(n for n in self.nodos if n["@type"] == "WebPage")
        negocio = {"@id": f"{datos.SITIO}/#negocio"}
        self.assertEqual(pagina["about"], negocio)
        self.assertEqual(pagina["publisher"], negocio)
        self.assertEqual(pagina["dateModified"], NB["ultima_actualizacion"])
        self.assertEqual(pagina["url"], URL)
        por_id = {n["@id"]: n["@type"] for n in self.nodos if "@id" in n}
        self.assertEqual(por_id[pagina["breadcrumb"]["@id"]], "BreadcrumbList")
        self.assertEqual(por_id[pagina["mainEntity"]["@id"]], "FAQPage")
        self.assertTrue(pagina["primaryImageOfPage"]["url"].startswith(datos.SITIO + "/img/nochebuenas/"))

    def test_nodo_minimo_del_negocio(self):
        # SEO fase 1: el mismo nodo mínimo de todas las páginas (tools/site/entidad.py), con la URL canónica de la home.
        nodo = next(n for n in self.nodos if "LocalBusiness" in n["@type"])
        self.assertEqual(nodo, {"@type": ["GardenStore", "LocalBusiness"], "@id": f"{datos.SITIO}/#negocio",
                                "name": datos.NOMBRE, "url": f"{datos.SITIO}/", "telephone": datos.TELEFONO_TEL})

    def test_ofertas_por_escalon(self):
        rangos = [(1, 11), (12, 49), (50, 199), (200, None)]
        self.assertEqual([p["@id"] for p in productos(self.html)], [f"{URL}#nochebuena-{p['clave']}" for p in NB["productos"]])
        for producto, datos_p in zip(productos(self.html), NB["productos"]):
            ofertas = producto["offers"]["offers"]
            self.assertEqual([o["price"] for o in ofertas], list(datos_p["precios"]))
            for oferta, (minimo, maximo) in zip(ofertas, rangos):
                with self.subTest(producto=datos_p["clave"], minimo=minimo):
                    self.assertEqual(oferta["@type"], "Offer")
                    self.assertEqual((oferta["priceCurrency"], oferta["url"]), ("MXN", URL))
                    self.assertEqual(oferta["availability"], producto["offers"]["availability"])
                    cantidad = oferta["eligibleQuantity"]
                    self.assertEqual((cantidad["@type"], cantidad["unitCode"], cantidad["minValue"], cantidad.get("maxValue")),
                                     ("QuantitativeValue", "C62", minimo, maximo))
                    self.assertEqual("maxValue" in cantidad, maximo is not None)

    def test_precios_low_y_high(self):
        for producto, datos_p in zip(productos(self.html), NB["productos"]):
            with self.subTest(producto=datos_p["clave"]):
                oferta = producto["offers"]
                self.assertEqual(oferta["@type"], "AggregateOffer")
                self.assertEqual(oferta["priceCurrency"], "MXN")
                self.assertEqual(float(oferta["lowPrice"]), datos_p["precios"][-1])
                self.assertEqual(float(oferta["highPrice"]), datos_p["precios"][0])

    def test_faq_igual_a_lo_visible(self):
        main = re.search(r"<main\b.*</main>", self.html, re.S).group(0)
        faq = next(n for n in self.nodos if n["@type"] == "FAQPage")
        visibles = texto(main)
        self.assertEqual(len(faq["mainEntity"]), len(contenido.PREGUNTAS))
        for q in faq["mainEntity"]:
            with self.subTest(pregunta=q["name"]):
                self.assertIn(q["name"], visibles)
                self.assertIn(q["acceptedAnswer"]["text"], visibles)

    def test_migas(self):
        migas = next(n for n in self.nodos if n["@type"] == "BreadcrumbList")
        self.assertEqual(migas["itemListElement"][-1]["item"], URL)


class ModosTest(unittest.TestCase):
    def disponibilidad(self, nombre):
        return [p["offers"]["availability"].rsplit("/", 1)[1] for p in productos(modo(nombre))]

    def test_temporada_en_stock_y_macetón_sobre_pedido(self):
        self.assertEqual(self.disponibilidad("temporada"), ["InStock", "InStock", "InStock", "InStock", "InStock", "PreOrder"])

    def test_preventa(self):
        pagina = modo("preventa")
        self.assertEqual(set(self.disponibilidad("preventa")), {"PreOrder"})
        self.assertIn("Aparta tus Nochebuenas 2026 para tu empresa", texto(pagina))
        self.assertIn('data-nb-modo="preventa"', pagina)
        self.assertRegex(texto(pagina), r"[Pp]recios de referencia")
        self.assertIn("data-nb-cotizador", pagina)
        main = re.search(r"<main\b.*</main>", pagina, re.S).group(0)
        etiqueta = re.search(r'<p class="vt-etiqueta__precio">.*?</p>', main, re.S).group(0)
        self.assertIn("referencia", texto(etiqueta).lower())
        faq = next(n for n in grafo(pagina) if n["@type"] == "FAQPage")
        self.assertIn("referencia", faq["mainEntity"][0]["acceptedAnswer"]["text"])
        self.assertIn("Apartar por WhatsApp", texto(main[:main.index("</section>")]))
        self.assertRegex(pagina, r"data-nb-bar[^>]*hidden>.*?>Apartar mi pedido</a>")

    def test_postemporada(self):
        pagina = modo("postemporada")
        self.assertEqual(set(self.disponibilidad("postemporada")), {"OutOfStock"})
        self.assertIn("Temporada 2026 cerrada · Gracias", texto(pagina))
        self.assertNotIn("data-nb-cotizador", pagina)
        self.assertNotIn("data-nb-bar", pagina)
        self.assertNotIn("nb-config", pagina)
        self.assertNotIn("vt-nochebuenas.js", pagina)
        self.assertNotIn("data-nb-hasta", pagina)
        for marca in ("vt-h-galeria", "vt-h-cuidados", "vt-h-faq"):
            self.assertIn(marca, pagina)
        self.assertIn("Avísame en la próxima temporada", texto(pagina))
        visible = texto(cuerpo(pagina))
        self.assertIn("Gracias por esta temporada.", visible)
        self.assertNotIn("Gracias por tu pedido", visible)
        self.assertNotIn("Rosa y jaspeada también", visible)

    def test_postemporada_no_vende(self):
        pagina = modo("postemporada")
        titulo = re.search(r"<title>(.*?)</title>", pagina).group(1)
        descripcion = re.search(r'<meta name="description" content="([^"]*)"', pagina).group(1)
        for valor in (titulo, descripcion, re.search(r'property="og:title" content="([^"]*)"', pagina).group(1)):
            with self.subTest(valor=valor):
                self.assertNotIn("$", valor)
                self.assertNotIn("Mayoreo", valor)
        faq = next(n for n in grafo(pagina) if n["@type"] == "FAQPage")
        plano = " ".join(q["name"] + " " + q["acceptedAnswer"]["text"] for q in faq["mainEntity"])
        for palabra in ("$", "mayoreo", "entregan", "facturan", "rosa y jaspeada"):
            with self.subTest(palabra=palabra):
                self.assertNotIn(palabra, plano.lower())

    def test_mensajes_del_shell_siguen_el_modo(self):
        with patch.dict(datos.NOCHEBUENAS, modo="postemporada"):
            ctx = paginas.contexto(RUTA)
        self.assertIn("próxima temporada", ctx["mensaje"])
        self.assertNotIn("cotizar", ctx["mensaje"].lower())
        self.assertIn("próxima temporada", ctx["mensaje_pie"])
        with patch.dict(datos.NOCHEBUENAS, modo="preventa"):
            self.assertIn("apartar", paginas.contexto(RUTA)["mensaje"].lower())

    def test_los_tres_modos_son_indexables_con_el_mismo_canonical(self):
        for nombre in ("temporada", "preventa", "postemporada"):
            pagina = modo(nombre)
            with self.subTest(modo=nombre):
                self.assertIn('<meta name="robots" content="index, follow">', pagina)
                self.assertIn(f'<link rel="canonical" href="{URL}">', pagina)

    def test_modo_por_omision_es_el_de_datos(self):
        self.assertEqual(plantilla.render(contenido.CONTENIDO), modo(NB["modo"]))


class ConfiguracionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vercel = json.loads((RAIZ / "vercel.json").read_text(encoding="utf-8"))

    def destinos(self):
        return {r["source"]: r["destination"] for r in self.vercel["redirects"]}

    def test_la_url_ya_no_redirige(self):
        self.assertNotIn(RUTA, self.destinos())

    def test_las_urls_viejas_apuntan_aqui(self):
        for vieja in ("/nochebuenas-mayoreo-tampico", "/post/productores-de-nochebuenas-mayoreo"):
            with self.subTest(vieja=vieja):
                self.assertEqual(self.destinos()[vieja], RUTA)

    def test_connect_src_admite_el_registro_y_su_redireccion(self):
        csp = next(h["value"] for r in self.vercel["headers"] for h in r["headers"] if h["key"].startswith("Content-Security-Policy"))
        connect = next(d for d in csp.split(";") if d.strip().startswith("connect-src")).split()
        self.assertIn("https://script.google.com", connect)
        self.assertIn("https://script.googleusercontent.com", connect)

    def test_sitemap_con_la_fecha_de_datos(self):
        sitemap = (paginas.PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(f"<loc>{URL}</loc><lastmod>{NB['ultima_actualizacion']}</lastmod>", sitemap)

    def test_llms_txt(self):
        self.assertIn(URL, (paginas.PUBLIC / "llms.txt").read_text(encoding="utf-8"))

    def test_home_y_hub_enlazan_la_pagina(self):
        home = (paginas.PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertIn("Desde $89 en menudeo y desde $65 por volumen", home)
        hub = (paginas.PUBLIC / "plantas-palmas-arboles-tampico" / "index.html").read_text(encoding="utf-8")
        main_home = re.search(r"<main\b.*</main>", home, re.S).group(0)
        main_hub = re.search(r"<main\b.*</main>", hub, re.S).group(0)
        self.assertIn(f'href="{RUTA}"', main_home)
        self.assertIn(f'href="{RUTA}"', main_hub)
        self.assertIn("Nochebuenas de temporada", main_hub)

    def test_contexto_sin_barra_del_shell(self):
        ctx = paginas.contexto(RUTA)
        self.assertEqual((ctx["tipo"], ctx["activo"], ctx["servicio"]), ("nochebuenas", "plantas", "plantas"))
        self.assertFalse(ctx["barra"])


if __name__ == "__main__":
    unittest.main()


class Maceta8Test(unittest.TestCase):
    """Decisión del dueño 2026-11-11: Maceta 8" a $699/$589/$539/$519 (costo $400), en existencia, con sus dos fotos."""

    def test_precio_y_existencia(self):
        p = next(p for p in datos.NOCHEBUENAS["productos"] if p["clave"] == "8")
        self.assertEqual(p["precios"], (699, 589, 539, 519))
        self.assertFalse(p.get("sobre_pedido"))
        self.assertGreater(p["precios"][-1], 400, "el precio de proyecto queda arriba del costo")

    def test_fotos_en_la_galeria(self):
        from contenido.nochebuenas_fotos import FOTOS
        ids = [f["id"] for f in FOTOS if f["uso"] == "galeria"]
        self.assertEqual(ids[:2], ["maceta-8", "maceta-8-hilera"])
        html = (Path(__file__).resolve().parents[3] / "public/post/nochebuenas-tampico-madero-mayoreo/index.html").read_text(encoding="utf-8")
        self.assertIn("<td>$699</td><td>$589</td><td>$539</td><td>$519</td>", html)
        self.assertIn("nochebuena-roja-maceta-8-tampico-800.webp", html)
