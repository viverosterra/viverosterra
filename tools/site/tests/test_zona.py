"""Plantilla zona (Etapa 2g): orden de secciones del spec sin caso ni tiempo desde el vivero, anclas de main, precios de
datos.py, mensaje de la zona en portada, cierre, menú, barra y pie, sin CSS viejo, y JSON-LD como el de main."""
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

ZONAS = tuple(ruta for _n, ruta in datos.ZONAS)


def html_de(ruta):
    return (paginas.PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


class ZonaTest(unittest.TestCase):
    def test_registradas_con_la_plantilla_zona(self):
        filas = {r: (p, c) for r, _s, p, c in generar.PAGINAS}
        for ruta in ZONAS:
            with self.subTest(ruta=ruta):
                self.assertEqual(filas[ruta], ("zona", f"zona:{ruta.strip('/')}"))

    def test_orden_de_secciones(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', html)
            with self.subTest(ruta=ruta):
                self.assertEqual(ids, ["precios", "zona", "colonias", "preguntas"])
                self.assertLess(html.index('id="vt-h1"'), html.index('id="precios"'))
                self.assertLess(html.index('id="vt-h-zonas"'), html.index('id="vt-cierre-titulo"'))

    def test_sin_css_viejo_ni_google_fonts(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                for viejo in ("tienda-pasto.css", "fonts.googleapis", "Geist", "hub-hero", "terra-precios"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_mensaje_de_la_zona_en_portada_cierre_y_shell(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            esperado = datos.con_firma(mensajes_paginas.ZONAS[ruta])
            mensajes = [unquote(m) for m in re.findall(r'data-cta="zona:(?:hero|cierre|header|barra)"[^>]*href="https://'
                                                       r'wa\.me/\d+\?text=([^"]+)"', html)]
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(len(mensajes), 4)
                self.assertEqual(set(mensajes), {esperado})

    def test_otras_zonas_y_vivero_enlazados(self):
        for ruta in ZONAS:
            main = html_de(ruta).split('<main id="main">', 1)[1].split("</main>", 1)[0]
            with self.subTest(ruta=ruta):
                for _n, otra in datos.ZONAS:
                    if otra != ruta:
                        self.assertIn(f'href="{otra}"', main)
                self.assertIn('href="/vivero-tampico"', main)
                self.assertIn('href="/precios"', main)

    def test_json_ld_con_service_faq_y_migas(self):
        for ruta in ZONAS:
            bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_de(ruta), re.S).group(1)
            grafo = json.loads(bloque)["@graph"]
            with self.subTest(ruta=ruta):
                self.assertEqual([n["@type"] for n in grafo], ["BreadcrumbList", "Service", "FAQPage"])
                self.assertEqual(grafo[1]["provider"], {"@id": f"{datos.SITIO}/#negocio"})
                oferta = grafo[1]["offers"]
                self.assertEqual(oferta["@type"], "Offer")
                self.assertNotIn("price", oferta)
                self.assertEqual(oferta["priceSpecification"],
                                 {"@type": "UnitPriceSpecification", "priceCurrency": "MXN", "unitText": "m²",
                                  "minPrice": datos.PRECIOS["pasto_instalado_m2"]})

    def test_cuatro_renglones_en_el_orden_de_la_zona(self):
        primero = {"/jardineria-aguila-tampico": "Poda de palmas", "/jardineria-country-club-tampico": "Riego automático",
                   "/jardineria-lomas-del-chairel-tampico": "Riego automático",
                   "/jardineria-lomas-de-rosales-tampico": "Pasto San Agustín instalado",
                   "/jardineria-ciudad-madero": "Pasto San Agustín instalado",
                   "/jardineria-altamira": "Pasto San Agustín instalado"}
        for ruta, nombre in primero.items():
            seccion = html_de(ruta).split('id="precios"', 1)[1].split('id="zona"', 1)[0]
            filas = re.findall(r'<th scope="row"><b>(.*?)</b>', seccion)
            with self.subTest(ruta=ruta):
                self.assertEqual(len(filas), 4)
                self.assertIn(nombre, filas[0])
                self.assertIn('href="/precios">Ver la lista completa</a>', seccion)

    def test_cotizar_en_la_zona_y_poda_con_su_mensaje(self):
        for ruta in ZONAS:
            m = re.search(r'data-cta="zona:precios"[^>]*href="https://wa\.me/\d+\?text=([^"]+)"[^>]*>Cotizar en ', html_de(ruta))
            with self.subTest(ruta=ruta):
                self.assertEqual(unquote(m.group(1)), datos.con_firma(mensajes_paginas.ZONAS[ruta]))
        ruta = "/jardineria-aguila-tampico"
        m = re.search(r'data-cta="zona:poda"[^>]*href="https://wa\.me/\d+\?text=([^"]+)"[^>]*>Mándanos fotos', html_de(ruta))
        self.assertEqual(unquote(m.group(1)), datos.con_firma(mensajes_paginas.PODA_ZONAS[ruta]))
        self.assertIn("en Águila y Altavista", unquote(m.group(1)))

    def test_costo_de_la_visita_corto_arriba_y_completo_solo_en_el_cierre(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(html.count(datos.VISITA_COSTO), 1)
                self.assertGreater(html.index(datos.VISITA_COSTO), html.index('id="vt-cierre-titulo"'))
                self.assertIn(datos.VISITA_COSTO_CORTO, html.split('id="precios"', 1)[0])

    def test_colonias_sin_municipio_por_renglon_y_madero_sin_cp_en_el_kicker(self):
        for ruta in ZONAS:
            seccion = html_de(ruta).split('id="colonias"', 1)[1].split('id="preguntas"', 1)[0]
            with self.subTest(ruta=ruta):
                self.assertIn('class="vt-sectores vt-colonias"', seccion)
                self.assertNotIn("<small>", seccion)
        madero = re.search(r'<p class="vt-kicker">(.*?)</p>', html_de("/jardineria-ciudad-madero")).group(1)
        self.assertEqual(madero, "Ciudad Madero, Tamaulipas")

    def test_otras_zonas_sin_la_frase_que_se_contradecia(self):
        for ruta in ZONAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn("También trabajamos en estas zonas.", html)
                self.assertNotIn("fuera de ellas", html)


if __name__ == "__main__":
    unittest.main()
