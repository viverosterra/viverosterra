"""Regla permanente (SEO fase 0, 2026-11-10): toda página indexable tiene un <title> de 60 caracteres o menos y una
descripción de 70 a 155, y ninguno de los dos se repite en otra página del sitio. Google corta lo que pasa de esas
medidas y, si dos páginas se presentan igual, elige una. Los textos salen de docs/seo/2026-11/mapa-palabras-clave.md,
revisados contra las reglas del dueño (tests/test_reglas.py, tests/test_iva_pasto.py).

EXCEPCIONES_LARGO es corta y solo puede encoger: cada ruta dice por qué sigue fuera de medida y la prueba falla si una
excepción ya cumple (para que se borre de la lista)."""
import html as html_mod
import re
import sys
import unittest
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402

TITULO_MAX = 60
DESCRIPCION_MIN, DESCRIPCION_MAX = 70, 155
_APROBADO = "Título y descripción aprobados por el dueño (semana del 2026-11-09): no se tocan en la fase 0."
_ETAPA_2I = "La rehace la rama feat/etapa-2i (plantilla nueva): su título y descripción del mapa se aplican ahí."
_FUSION = ("Artículo marcado para fusionar con 301 en la fase 2 del plan SEO (mapa §3c): no se retitula una URL que va "
           "a desaparecer.")
EXCEPCIONES_LARGO = {
    "/": _APROBADO,
    datos.NOCHEBUENAS["ruta"]: _APROBADO,
    "/vivero-tampico": _ETAPA_2I,
    "/politicas": _ETAPA_2I,
    "/protocolo-cuidados-pasto-san-agustin": _ETAPA_2I,
    "/blog/jardin-bajo-presupuesto-tampico": _FUSION,
    "/blog/palmas-mas-vendidas-tampico-precios": _FUSION,
    "/blog/pasto-sintetico-para-perros": _FUSION,
    "/blog/riego-automatico-tampico-roi": _FUSION,
    "/blog/sistema-riego-automatico-conviene-tampico": _FUSION,
}
MATERIALES_H1 = {
    "/tierra-negra-vegetal-tampico": "Tierra negra en Tampico por costal, m³ o camión",
    "/tezontle-rojo-tampico": "Tezontle rojo en Tampico por costal, m³ o camión",
    "/marmol-blanco-tampico": "Mármol blanco para jardín en Tampico",
    "/piedra-bola-rio-tampico": "Piedra bola de río en Tampico para jardines y senderos",
}


def _meta(html, patron):
    m = re.search(patron, html, re.S)
    return html_mod.unescape(re.sub(r"\s+", " ", m.group(1)).strip()) if m else ""


def leer():
    """{ruta: (título, descripción)} de las páginas indexables."""
    salida = {}
    for path in shell.paginas_html():
        html = path.read_text(encoding="utf-8")
        if "noindex" in _meta(html, r'<meta name="robots" content="([^"]*)"'):
            continue
        salida[paginas.ruta_de(path)] = (_meta(html, r"<title>(.*?)</title>"),
                                         _meta(html, r'<meta name="description" content="([^"]*)"'))
    return salida


def fuera_de_medida(titulo, descripcion):
    faltas = []
    if not titulo or len(titulo) > TITULO_MAX:
        faltas.append(f"título de {len(titulo)}")
    if not DESCRIPCION_MIN <= len(descripcion) <= DESCRIPCION_MAX:
        faltas.append(f"descripción de {len(descripcion)}")
    return faltas


PAGINAS = leer()


class TitulosYDescripcionesTest(unittest.TestCase):
    maxDiff = None

    def test_se_revisan_las_paginas_indexables(self):
        self.assertGreater(len(PAGINAS), 100)
        for ruta in ("/cuestionario", "/gracias", "/datos-envio"):
            self.assertNotIn(ruta, PAGINAS)

    def test_titulo_hasta_60_y_descripcion_de_70_a_155(self):
        malas = {ruta: faltas for ruta, (t, d) in PAGINAS.items()
                 if (faltas := fuera_de_medida(t, d)) and ruta not in EXCEPCIONES_LARGO}
        self.assertEqual(malas, {})

    def test_las_excepciones_son_pocas_tienen_motivo_y_siguen_haciendo_falta(self):
        self.assertLessEqual(len(EXCEPCIONES_LARGO), 10, "la lista solo puede encoger")
        for ruta, motivo in EXCEPCIONES_LARGO.items():
            with self.subTest(ruta=ruta):
                self.assertIn(ruta, PAGINAS)
                self.assertGreater(len(motivo), 40)
                self.assertTrue(fuera_de_medida(*PAGINAS[ruta]), "ya cumple: bórrala de EXCEPCIONES_LARGO")

    def test_titulos_y_descripciones_unicos_en_el_sitio(self):
        for indice, nombre in ((0, "título"), (1, "descripción")):
            rutas = defaultdict(list)
            for ruta, par in PAGINAS.items():
                rutas[par[indice].casefold()].append(ruta)
            with self.subTest(meta=nombre):
                self.assertEqual({texto: lista for texto, lista in rutas.items() if len(lista) > 1}, {})

    def test_titulo_con_la_marca_una_sola_vez(self):
        for ruta, (titulo, _d) in PAGINAS.items():
            with self.subTest(ruta=ruta):
                self.assertLessEqual(titulo.count(datos.NOMBRE), 1)

    def test_h1_de_los_materiales_con_en_tampico(self):
        for ruta, h1 in MATERIALES_H1.items():
            html = (paginas.PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")
            encontrados = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()
                           for t in re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)]
            with self.subTest(ruta=ruta):
                self.assertEqual(encontrados, [h1])

    def test_la_medida_detecta_lo_que_debe(self):
        self.assertEqual(fuera_de_medida("Pasto en Rollo Tampico | Viveros Terra", "x" * 120), [])
        self.assertEqual(fuera_de_medida("x" * 61, "x" * 69), ["título de 61", "descripción de 69"])
        self.assertEqual(fuera_de_medida("", "x" * 156), ["título de 0", "descripción de 156"])
        self.assertEqual(fuera_de_medida("x" * 60, "x" * 155), [])


if __name__ == "__main__":
    unittest.main()
