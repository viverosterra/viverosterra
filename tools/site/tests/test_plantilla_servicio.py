"""Plantilla de servicio (tools/site/plantillas/servicio.py): las secciones opcionales que agrega la Etapa 2c."""
import copy
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
from plantillas import servicio  # noqa: E402

BASE = generar.cargar("pasto_en_rollo").CONTENIDO


def main_de(k):
    return re.search(r'<main id="main">(.*)</main>', servicio.render(k), re.S).group(1)


class PlantillaServicioTest(unittest.TestCase):
    def test_objecion_con_una_sola_tabla_y_rotulo_propio(self):
        k = copy.deepcopy(BASE)
        for clave in ("comparativa_2", "titulo_2"):
            del k["objecion"][clave]
        k["objecion"]["rotulo"] = "Frecuencia"
        conviene = main_de(k).split('id="vt-h-conviene"')[0].rsplit("<section", 1)[1]
        self.assertIn("<b>04</b>Frecuencia", conviene)  # 02 es el mosaico de fotos
        cuerpo = main_de(k).split('id="vt-h-conviene"')[1].split("</section>")[0]
        self.assertEqual(cuerpo.count("<table"), 1)

    def test_opciones_con_tabla_nota_y_rotulo(self):
        k = copy.deepcopy(BASE)
        k["opciones"] = {"rotulo": "Planes", "titulo": "¿Cuánto cuesta?", "nota": "Nota de planes.",
                         "items": ({"rotulo": "Plan 1", "titulo": "A", "precio_texto": "Por cotización", "detalle": "d",
                                    "puntos": ("p",), "mensaje": "Hola A"},),
                         "tabla": {"titulo": "Compara", "columnas": ("Plan", "A"), "filas": (("Precio", "x"),),
                                   "caption": "c"}}
        html = main_de(k)
        opciones = html.split('id="vt-h-opciones"')[1].split("</section>")[0]
        self.assertIn('<h3 class="vt-mt">Compara</h3><table class="vt-tabla vt-tabla--comparar">', opciones)
        self.assertIn('<p class="vt-promesa">Nota de planes.</p>', opciones)
        self.assertIn("<b>03</b>Planes", html)  # 02 es el mosaico de fotos

    def test_que_incluye_va_despues_de_las_opciones(self):
        k = copy.deepcopy(BASE)
        k["opciones"] = {"titulo": "Planes", "items": ({"rotulo": "1", "titulo": "A", "puntos": (), "mensaje": "Hola"},)}
        k["incluye"] = {"titulo": "Qué incluye cada visita", "items": ({"titulo": "Poda", "texto": "Corte."},)}
        html = main_de(k)
        self.assertLess(html.index('id="vt-h-opciones"'), html.index('id="vt-h-incluye"'))
        self.assertLess(html.index('id="vt-h-incluye"'), html.index('id="vt-h-precio"'))
        self.assertIn('<ul class="vt-modos vt-fichas">', html)

    def test_las_paginas_de_antes_no_cambian(self):
        """Pasto en rollo y sintético en Tampico salen idénticos (test_generar compara contra public/)."""
        self.assertNotIn("incluye", BASE)
        self.assertIn("comparativa_2", BASE["objecion"])


if __name__ == "__main__":
    unittest.main()
