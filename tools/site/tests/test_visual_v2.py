"""Plan visual V2 (2026-11-11, docs/ux/2026-11/plan-mejoras-visuales.md): ritmo y secuencia. «En corto» como nota de
campo, tira de 4 datos bajo el hero, un solo momento oscuro a media página en las páginas comerciales, estados de envío
de la tienda en acordeón y, en computadora, el título de la sección fijo al bajar."""
import re
import unittest
from pathlib import Path

import componentes as c
import datos

PUBLIC = Path(__file__).resolve().parents[3] / "public"
CSS = (PUBLIC / "css" / "terra.css").read_text(encoding="utf-8")
# Páginas con opiniones, pasos o una garantía de datos.py: llevan exactamente un momento oscuro.
CON_MOMENTO = ("index.html", "mantenimiento-jardines-tampico", "sistema-riego-tampico", "diseno-jardines-tampico",
               "pasto-en-rollo-tampico", "pasto-sintetico-tampico", "mayoreo-pasto-tampico", "palmas-mayoreo-proyectos",
               "plantas-palmas-arboles-tampico", "plantas-para-jardin-tampico", "plantas-de-interior-tampico",
               "palmas-tropicales-tampico", "arboles-ornamentales-tampico", "arboles-para-banqueta-tampico",
               "tierra-negra-vegetal-tampico", "piedra-bola-rio-tampico", "pasto-sintetico", "pasto-sintetico/toscana-28")


def _html(ruta):
    archivo = PUBLIC / ruta if ruta.endswith(".html") else PUBLIC / ruta / "index.html"
    return archivo.read_text(encoding="utf-8")


def _secciones(html):
    main = html.split("<main", 1)[1].split("</main>", 1)[0]
    return re.findall(r'<section class="([^"]+)"', main)


class VisualV2Test(unittest.TestCase):
    def test_un_momento_oscuro_a_media_pagina(self):
        for ruta in CON_MOMENTO:
            with self.subTest(ruta=ruta):
                clases = _secciones(_html(ruta))
                momentos = [i for i, x in enumerate(clases) if "vt-banda" in x.split()]
                self.assertEqual(len(momentos), 1)
                # Ni pegado al hero ni al cierre (que ya es verde profundo).
                self.assertGreater(momentos[0], 2)
                cierre = next(i for i, x in enumerate(clases) if x.startswith("vt-cierre"))
                self.assertLess(momentos[0], cierre - 1)

    def test_momento_quita_el_tinte_y_el_apoyo(self):
        seccion = c.bloque(3, "Pasos", "vt-h-x", "Título", "<p>x</p>", tinte=True, ritmo="apoyo")
        self.assertTrue(c.momento(seccion).startswith('<section class="vt-bloque vt-banda vt-bloque--clave"'))
        with self.assertRaises(ValueError):
            c.momento('<div class="vt-bloque"></div>')

    def test_en_corto_como_nota_de_campo(self):
        html = c.respuesta({"texto": "Cuesta $85 por m².", "fecha": "2026-11-10"})
        self.assertIn('<div class="vt-corto"><p class="vt-corto__t">En corto</p>', html)
        self.assertIn(".vt-corto{display:grid", CSS)

    def test_tira_de_cuatro_datos_bajo_el_hero(self):
        self.assertEqual(len(c.DATOS_TIRA), 4)
        html = _html("mantenimiento-jardines-tampico")
        tira = re.search(r'<dl class="vt-datos vt-datos--tira">(.*?)</dl>', html, re.S)
        self.assertIsNotNone(tira)
        self.assertEqual(tira.group(1).count("<dt>"), 4)
        for dato in (str(datos.DESDE), datos.CALLE_CORTA, datos.FACTURA, datos.REPSE):
            self.assertIn(str(dato), tira.group(1))

    def test_estados_de_envio_en_acordeon(self):
        html = _html("pasto-sintetico")
        self.assertEqual(html.count('<details data-zona="'), 3)
        self.assertNotIn("Costo de envío de pasto sintético por estado, con IVA.</caption>", html)
        js = (PUBLIC / "js" / "tienda-hub.js").read_text(encoding="utf-8")
        self.assertIn(".vt-zonas-acc details", js)

    def test_titulo_fijo_solo_en_computadora(self):
        self.assertIn("@media (min-width:1200px){.vt-bloque>.vt-dos>div:first-child{position:sticky", CSS)


if __name__ == "__main__":
    unittest.main()
