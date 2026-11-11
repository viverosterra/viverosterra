"""Respuestas directas (SEO fase 1, 2026-11-10): las 10 páginas que venden abren su contenido con un párrafo de 40 a 60
palabras que da el dato en la misma frase (precio de datos.py, unidad y zona), marcado con data-vt-respuesta; las páginas
con precio muestran "Actualizado: <mes> de <año>" y llevan dateModified, los dos de datos.PRECIOS_ACTUALIZADOS (nunca la
fecha del build). El sitemap repite la fecha de cada artículo del blog."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import entidad  # noqa: E402
import paridad  # noqa: E402
import sitemap_fechas  # noqa: E402
from contenido import respuestas  # noqa: E402

P = datos.PRECIOS
MARCA_RE = re.compile(r"<p class=\"vt-lede\" data-vt-respuesta>(.*?)</p>", re.S)
FECHA = (f'<p class="vt-promesa">Actualizado: <time datetime="{datos.PRECIOS_ACTUALIZADOS}">'
         f"{entidad.mes_largo(datos.PRECIOS_ACTUALIZADOS)}</time></p>")
# El dato que cada respuesta debe traer en el texto (precio con su unidad) y la zona.
# Decisión del dueño (2026-11-10): "En corto" de la home y de pasto en rollo lleva completa la condición de terreno listo
# (datos.TERRENO_LISTO, con el precio del instalado); en 60 palabras la entrada queda en zona, año y precio de solo pasto.
DATOS = {
    "/": (f"pasto solo a ${P['pasto_solo_m2']}/m², sin IVA", datos.TERRENO_LISTO, "Tampico, Madero y Altamira, desde 2007"),
    "/pasto-en-rollo-tampico": (f"${P['pasto_solo_m2']}/m² solo el pasto, sin IVA", datos.TERRENO_LISTO,
                                "Tampico, Madero y Altamira"),
    "/pasto-sintetico-tampico": ("de $446.60 a $754 por m², con material, colocación e IVA", "desde 2 m²",
                                 "desde $139 por m²", "Tampico, Ciudad Madero y Altamira", "precios 2026"),
    "/pasto-sintetico": ("9 modelos de 10 a 35 mm", "desde $139 por m² en rollo de 50 m², con IVA incluido",
                         "de $900 a $1,400 por rollo", "pedido mínimo es de 25 m²", "todo México"),
    "/sistema-riego-tampico": (f"de ${P['riego_m2'][0]} a ${P['riego_m2'][1]} por m², con IVA",
                               f"ahorra {datos.RIEGO_AHORRO} de agua", "Tampico, Ciudad Madero o Altamira"),
    "/mantenimiento-jardines-tampico": (f"desde ${P['mantenimiento_mes']} al mes, con IVA",
                                        "semanal, cada 15 días, cada 21 días o mensual",
                                        "Tampico, Ciudad Madero y Altamira"),
    "/diseno-jardines-tampico": ("$3,000 en el plan Esencial, $6,500 en el Completo y desde $18,000 en el Premium, con IVA",
                                 "proyectos de más de $150,000", "en Tampico"),
    "/vivero-tampico": (f"{datos.CALLE}, {datos.COLONIA}, {datos.CP} {datos.CIUDAD}", "entrando por Banamex",
                        "de lunes a viernes de 9 a 18 h y sábados de 9 a 14 h", "desde 2007"),
    "/precios": (f"${P['pasto_solo_m2']}/m² solo el pasto", f"desde ${P['pasto_instalado_m2']}/m² instalado",
                 "Tampico, Madero y Altamira"),
    "/mayoreo-pasto-tampico": (f"desde ${P['pasto_mayoreo_m2']}/m² (solo pasto)", f"{P['pasto_mayoreo_minimo_m2']} m² o más",
                               "no lleva IVA", "Tampico, Madero y Altamira"),
}
PROHIBIDO_RE = re.compile(r"(?i)\bgratis\b|gratuit|sin costo|m[aá]s vendid|d[ií]as h[aá]biles|\bMSI\b|anticipo|"
                          r"pr[oó]ximo corte|menos de 1 hora(?! en horario)")


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", "", fragmento))).strip()


def pagina_ld(ruta):
    bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_de(ruta), re.S).group(1)
    return next(n for n in json.loads(bloque)["@graph"] if n["@type"] == "WebPage")


class RespuestasTest(unittest.TestCase):
    def test_son_las_diez_paginas_del_informe(self):
        self.assertEqual(set(respuestas.RUTAS), set(DATOS))
        self.assertEqual(len(respuestas.RUTAS), 10)

    def test_una_respuesta_visible_por_pagina_de_40_a_60_palabras_con_el_dato(self):
        for ruta, datos_esperados in DATOS.items():
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(html.count(" data-vt-respuesta>"), 1)
                texto = plano(MARCA_RE.search(html).group(1))
                if ruta not in ("/precios",):  # /precios ya abría con el dato en 35 palabras y no se reescribe
                    self.assertTrue(40 <= len(texto.split()) <= 60, f"{len(texto.split())} palabras")
                for dato in datos_esperados:
                    self.assertIn(dato, texto)
                self.assertIsNone(PROHIBIDO_RE.search(texto), texto)

    def test_la_respuesta_va_despues_de_la_portada_y_antes_de_la_primera_seccion(self):
        """Fuera de la portada: no empuja el precio ni el botón de WhatsApp de la primera pantalla."""
        for ruta in respuestas.TEXTOS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                portada = html.index('class="vt-portada')
                respuesta = html.index('<section class="vt-respuesta"')
                self.assertLess(portada, respuesta)
                self.assertLess(respuesta, html.index('class="vt-bloque__no"><b>01</b>'))
                hero = html[portada:respuesta]
                self.assertNotIn("data-vt-respuesta", hero)
                self.assertIn("wa.me", hero)
                self.assertIn('<p class="vt-bloque__no"><b>En corto</b></p>', html)

    def test_home_con_el_hero_intacto(self):
        html = html_de("/")
        self.assertIn(f'<p class="vt-lede">Pasto San Agustín en rollo, diseño de jardines y {datos.VARIEDADES} variedades '
                      "de plantas, en Tampico, Madero y Altamira.</p>", html)
        self.assertEqual(html.count("<h1"), 1)

    def test_el_texto_publicado_es_el_de_respuestas(self):
        for ruta, texto in respuestas.TEXTOS.items():
            with self.subTest(ruta=ruta):
                self.assertIn(f"<p class=\"vt-lede\" data-vt-respuesta>{texto}</p>", html_de(ruta))

    def test_fecha_visible_y_date_modified_del_dato_versionado(self):
        self.assertRegex(datos.PRECIOS_ACTUALIZADOS, r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(entidad.mes_largo("2026-11-10"), "noviembre de 2026")
        for ruta in respuestas.RUTAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                if ruta in respuestas.SIN_FECHA:
                    self.assertNotIn("Actualizado:", html)
                    self.assertNotIn("dateModified", pagina_ld(ruta))
                else:
                    self.assertEqual(html.count(FECHA), 1)
                    self.assertEqual(pagina_ld(ruta)["dateModified"], datos.PRECIOS_ACTUALIZADOS)

    def test_el_build_no_usa_la_fecha_de_hoy(self):
        for modulo in ("entidad.py", "llms.py", "sitemap_fechas.py", "contenido/respuestas.py", "plantillas/base.py"):
            fuente = (Path(__file__).resolve().parents[1] / modulo).read_text(encoding="utf-8")
            with self.subTest(modulo=modulo):
                self.assertNotRegex(fuente, r"date\.today\(\)|datetime\.now\(\)|time\.time\(\)")

    def test_componente(self):
        self.assertEqual(c.respuesta(None), "")
        self.assertEqual(c.respuesta({"fecha": "2026-11-10"}),
                         '<section class="vt-respuesta" aria-label="En corto"><div class="vt-wrap"><p class="vt-promesa">'
                         'Actualizado: <time datetime="2026-11-10">noviembre de 2026</time></p></div></section>')
        solo_texto = c.respuesta({"texto": "Cuesta $85 por m²."})
        self.assertIn('<p class="vt-lede" data-vt-respuesta>Cuesta $85 por m².</p>', solo_texto)
        self.assertNotIn("Actualizado", solo_texto)


class SitemapFechasTest(unittest.TestCase):
    XML = ('<urlset>\n  <url><loc>https://x.com/blog/a</loc><lastmod>2026-11-10</lastmod></url>\n'
           '  <url>\n    <loc>https://x.com/blog/b</loc>\n    <lastmod>2026-11-10</lastmod>\n  </url>\n'
           '  <url><loc>https://x.com/otra</loc><lastmod>2026-11-10</lastmod></url>\n</urlset>\n')

    def test_pone_la_fecha_de_cada_url_y_no_toca_las_demas(self):
        nuevo = sitemap_fechas.aplicar(self.XML, {"https://x.com/blog/a": "2026-05-07", "https://x.com/blog/b": "2026-04-20"})
        self.assertIn("<loc>https://x.com/blog/a</loc><lastmod>2026-05-07</lastmod>", nuevo)
        self.assertIn("<loc>https://x.com/blog/b</loc>\n    <lastmod>2026-04-20</lastmod>", nuevo)
        self.assertIn("<loc>https://x.com/otra</loc><lastmod>2026-11-10</lastmod>", nuevo)
        self.assertEqual(sitemap_fechas.aplicar(nuevo, {"https://x.com/blog/a": "2026-05-07"}), nuevo)

    def test_falla_si_un_articulo_no_esta_en_el_sitemap(self):
        with self.assertRaises(ValueError):
            sitemap_fechas.aplicar(self.XML, {"https://x.com/blog/no-esta": "2026-05-07"})

    def test_las_fechas_son_las_del_encabezado_de_cada_fuente(self):
        fechas = sitemap_fechas.fechas_blog()
        self.assertEqual(len(fechas), 54)
        self.assertEqual(fechas[f"{datos.SITIO}/blog/acolchado-mulch-jardin-tampico"], "2026-10-05")
        # Sin dateModified en la fuente, vale la fecha de publicación.
        self.assertEqual(fechas[f"{datos.SITIO}/blog/cuando-regar-pasto-san-agustin-tampico"], "2026-04-20")
        self.assertFalse(sitemap_fechas.sincronizar(), "el sitemap publicado ya trae las fechas")


if __name__ == "__main__":
    unittest.main()
