"""Entrega B de experiencia (CTA y recorrido), sin navegador: textos de botón específicos, filas de CTA de sección,
prueba social solo con datos publicados, mensajes de WhatsApp del blog con los huecos de su tema, cierre del artículo con
precio y garantía, reescrituras del catálogo, el vivero y la tienda, y el menú con vivero y blog."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import mensajes_paginas as mp  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402
from contenido import blog_clusters  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"


def html(ruta):
    rel = ruta.strip("/")
    archivo = PUBLIC / (f"{rel}/index.html" if (PUBLIC / rel).is_dir() else f"{rel}.html")
    return archivo.read_text(encoding="utf-8")


def mensajes_wa(fragmento):
    return [unquote(h.split("text=", 1)[1]) for h in re.findall(r'href="(https://wa\.me/[^"]+)"', fragmento) if "text=" in h]


class TextosDeBotonTest(unittest.TestCase):
    def test_opciones_contiguas_con_el_mismo_texto_no_se_publican(self):
        items = [{"rotulo": "1", "titulo": "A", "puntos": (), "mensaje": "x"},
                 {"rotulo": "2", "titulo": "B", "puntos": (), "mensaje": "y"}]
        with self.assertRaises(ValueError):
            c.opciones(items, "prueba")
        self.assertIn("Cotizar A", c.opciones([dict(items[0], cta="Cotizar A"), dict(items[1], cta="Cotizar B")], "prueba"))

    def test_reescritura_5_en_las_tarjetas_de_plan(self):
        esperados = {
            "/mantenimiento-jardines-tampico": ("Cotizar el plan básico", "Cotizar el plan premium", "Cotizar para mi empresa"),
            "/diseno-jardines-tampico": (f"Quiero el Esencial ({c.dinero(datos.PRECIOS['diseno'])})",
                                         f"Quiero el Completo ({c.dinero(datos.PRECIOS['diseno_completo'])})", "Cotizar el Premium"),
            "/sistema-riego-tampico": ("Cotizar aspersores", "Cotizar goteo", "Cotizar un área grande"),
            "/mayoreo-pasto-tampico": ("Cotizar solo el pasto", "Cotizar pasto instalado", "Cotizar pasto, palmas y riego"),
        }
        for ruta, textos in esperados.items():
            h = html(ruta)
            with self.subTest(ruta=ruta):
                for i, t in enumerate(textos, 1):
                    m = re.search(rf'data-cta="[^"]+:opcion-{i}"[^>]*>.*?</svg></span>([^<]+)<', h)
                    self.assertEqual(m.group(1), t)

    def test_ficha_y_vivero_dicen_que_se_pide(self):
        self.assertIn("Cotizar Toscana 28<span class=\"vt-flecha\"", html("/pasto-sintetico/toscana-28"))
        self.assertIn("Preguntar si la tienen", html("/vivero-tampico"))
        self.assertIn("Pedir cotización por correo", html("/tierra-negra-vegetal-tampico"))
        self.assertIn("¿Prefieres correo? Pide tu cotización aquí", html("/tierra-negra-vegetal-tampico"))
        self.assertIn("¿Tu área de compras pide la cotización por correo? Solicítala aquí", html("/mayoreo-pasto-tampico"))


class FilasYPruebaTest(unittest.TestCase):
    def test_fila_de_seccion_esconde_la_barra_sin_repetir_la_promesa(self):
        fila = c.fila_seccion("Hola", "plantas", "especies", "Cotizar mis plantas")
        self.assertIn('data-hero-cta', fila)
        self.assertIn('data-cta="plantas:especies"', fila)
        self.assertIn("Cotizar mis plantas", fila)
        self.assertNotIn(datos.PROMESA_COMPLETA, fila)  # plan visual V1: va en el hero y en el cierre

    def test_prueba_social_solo_con_datos_publicados_y_enlace_a_las_resenas(self):
        prueba = c.prueba_cta(datos.OPINION_SINTETICO_TAMPICO)
        self.assertIn(datos.MAPS_URL, prueba)
        self.assertIn("Ver las reseñas en Google", prueba)
        self.assertIn(datos.OPINION_SINTETICO_TAMPICO[0][1], prueba)
        nota = datos.GOOGLE.split(" ")[0]
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/toscana-28", "/pasto-sintetico/envio/monterrey",
                     "/plantas-palmas-arboles-tampico", "/palmas-tropicales-tampico", datos.NOCHEBUENAS["ruta"]):
            main = html(ruta).split("<main", 1)[1].split("</main>", 1)[0]
            with self.subTest(ruta=ruta):
                self.assertIn("Ver las reseñas en Google", main)
                self.assertIn(f"<b>{nota}</b>", main)
        # Plantas: sin opinión propia, solo cifras y la garantía de las plantas que sembramos.
        plantas = html("/plantas-palmas-arboles-tampico")
        self.assertIn(f"<b>{datos.CLIENTES}</b> clientes", plantas)
        self.assertNotIn("vt-testimonios", plantas.split("<main", 1)[1].split("vt-cierre", 1)[0])
        # Nochebuenas: sin garantía.
        self.assertNotIn("garant", html(datos.NOCHEBUENAS["ruta"]).split("<main", 1)[1].split("</main>", 1)[0].lower())


class MensajesTest(unittest.TestCase):
    def test_blog_con_los_huecos_de_su_tema(self):
        casos = {"pasto-san-agustin-vs-japones": ("Colonia: ___", "Metros aprox.: ___", "Solo el pasto o instalado: ___"),
                 "palma-areca-tampico": ("Lo que busco: ___", "Colonia de entrega: ___"),
                 "como-instalar-pasto-sintetico": ("Ciudad o colonia: ___", "Metros aprox.: ___"),
                 "tezontle-usos-jardin-tampico": ("Material y cantidad: ___", "Colonia de entrega: ___")}
        for slug, huecos in casos.items():
            m = mp.mensaje_blog(slug)
            with self.subTest(slug=slug):
                self.assertTrue(m.startswith(mp.BLOG[slug]))
                for h in huecos:
                    self.assertIn(h, m)
                self.assertEqual(paginas.contexto(f"/blog/{slug}")["mensaje"], datos.con_firma(m))
        # SEO fase 2c: la guía de riego hereda el mensaje del artículo de ROI fusionado con 301 (ya pide "de ___ m²").
        self.assertNotIn("Metros", mp.mensaje_blog("sistema-riego-automatizado-tampico"))

    def test_cierre_del_articulo_con_precio_y_garantia_de_datos(self):
        pasto = blog_clusters.de("pasto-san-agustin-vs-japones")["lede"]
        for parte in (f"${datos.PRECIOS['pasto_solo_m2']}/m² solo el pasto (no lleva IVA)",
                      f"desde ${datos.PRECIOS['pasto_instalado_m2']}/m² instalado", datos.ARRAIGO):
            self.assertIn(parte, pasto)
        palmas = blog_clusters.de("palma-areca-tampico")["lede"]
        self.assertIn("no llevan IVA", palmas)
        self.assertIn("/politicas#garantia-plantas", palmas)
        self.assertNotIn("garant", blog_clusters.de("como-instalar-pasto-sintetico")["lede"].lower())
        self.assertIn(pasto, html("/blog/pasto-san-agustin-vs-japones"))
        for tema in blog_clusters.LEDE.values():
            self.assertNotRegex(tema.lower(), r"gratis|gratuit|más vendid")

    def test_reescrituras_de_mensajes(self):
        self.assertEqual(mp.RUTAS["/blog"][0], "Hola, quiero cotizar: ___\nColonia: ___\nMetros aprox.: ___")
        self.assertEqual(mp.UTILITARIAS["vivero"],
                         "Hola, quiero visitar el vivero o cotizar plantas.\nLo que busco: ___\nTamaño aprox.: ___\nColonia: ___")
        catalogo = mp.RUTAS["/catalogo"][0]
        for hueco in ("Planta o plantas: ___", "Tamaño aprox.: ___", "Piezas: ___", "Colonia de entrega: ___"):
            self.assertIn(hueco, catalogo)
        vivero = mensajes_wa(html("/vivero-tampico").split('<section class="vt-portada', 1)[1])[0]
        self.assertIn("Lo que busco: ___", vivero)

    def test_catalogo_cuenta_de_los_datos_y_filas_entre_tarjetas(self):
        from contenido import catalogo_datos as cd
        h = html("/catalogo")
        self.assertIn(f"{len(cd.ESPECIES)} especies", h)
        self.assertEqual(h.count("data-vt-cta-rejilla"), (len(cd.ESPECIES) - 1) // 12)


class MenuTest(unittest.TestCase):
    def test_materiales_en_plantas_y_materiales_y_entradas_al_vivero_y_al_blog(self):
        grupo = next(i for i in partials.MENU if i["id"] == "plantas")
        self.assertEqual(grupo["texto"], "Plantas y materiales")
        for href in ("/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico"):
            self.assertIn(href, [h for _t, h in grupo["items"]])
            self.assertNotIn(href, [h for i in partials.MENU if i["id"] == "empresas" for _t, h in i["items"]])
        h = partials.header(paginas.contexto("/precios"))
        self.assertIn('<a class="vt-mmenu__link" href="/vivero-tampico">Vivero y horario', h)
        self.assertIn('<li><a href="/vivero-tampico">Vivero y horario</a></li>', h)
        self.assertIn('<a class="vt-mmenu__link" href="/blog">Blog', h)


if __name__ == "__main__":
    unittest.main()
