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
                self.assertEqual(grafo[1]["offers"]["lowPrice"], str(datos.PRECIOS["pasto_instalado_m2"]))


if __name__ == "__main__":
    unittest.main()
