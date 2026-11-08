"""extraer_blog: las tres envolturas del blog se reducen al mismo contenido, y una corrección que no encuentra su texto detiene
la extracción."""
import copy
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extraer_blog as e  # noqa: E402

MODERNO = ('<main><nav class="vt-crumbs"></nav><div class="bg-gradient-to-br"><div><div><span>Palmas</span><span>7 min de lectura</span></div>'
           '<h1>Título</h1><p>Entrada</p></div></div><div class="layout-grid"><article class="prose">'
           '<div class="bg-bggreen border-l-4 border-primary"><h2>Respuesta directa</h2><p>Sí.</p></div>'
           '<h2 id="uno">Uno</h2><p class="x">Texto <a href="/precios" class="y">enlace</a></p><div class="tip-box"><strong>Tip:</strong> nota</div>'
           '<h2 id="preguntas-frecuentes">Preguntas frecuentes</h2><div><button class="faq-btn"><span>¿Q?</span></button>'
           '<div class="faq-answer"><p>R</p></div></div>'
           '<div class="not-prose"><div class="bg-primary"><a href="https://wa.me/1">Cotizar</a></div></div></article>'
           '<aside class="sticky-sidebar"><nav><a href="#uno">Uno</a></nav></aside></div>'
           '<section class="bg-bgwarm"><h2>También</h2><a class="group" href="/blog/x"><span>Cat</span><h4>Otro</h4><p>Txt</p></a></section></main>')


class ExtraerBlogTest(unittest.TestCase):
    def setUp(self):
        self.a = e.Articulo("p", MODERNO)
        self.a.recorrer()

    def test_respuesta_y_portada(self):
        self.assertEqual(self.a.respuesta["parrafos"], ["Sí."])
        self.assertEqual(self.a.kicker(), "Palmas")
        self.assertEqual(self.a.minutos(), 7)

    def test_cuerpo_sin_clases_y_con_enlace(self):
        html = e.serializar(self.a.bloques)
        self.assertIn('<h2 id="uno">Uno</h2>', html)
        self.assertIn('<p>Texto <a href="/precios">enlace</a></p>', html)
        self.assertIn("vt-art__nota--tip", html)
        self.assertNotIn('class="x"', html)

    def test_preguntas_relacionados_y_cta_fuera(self):
        self.assertEqual(self.a.faq, [["¿Q?", "R"]])
        self.assertEqual(self.a.relacionados[0]["href"], "/blog/x")
        self.assertTrue(any("Cotizar" in r for r in self.a.retirado))

    def test_correccion_sin_coincidencia_detiene(self):
        with self.assertRaises(ValueError):
            e.corregir({"slug": "p", "cuerpo": "hola"}, (("adios", "x", "motivo largo de la corrección"),))

    def test_todos_no_exige_coincidencia(self):
        self.assertEqual(e.corregir({"slug": "p", "t": "ab"}, (), (("zz", "y", "m"),))["t"], "ab")

    def test_sin_fecha_confirmada_no_cambia_date_modified(self):
        doc = {"jsonld": {"@graph": [{"@type": "Article", "dateModified": "2026-01-15"}]}}
        with mock.patch.object(e, "FECHA_CORRECCION", None):
            self.assertEqual(e.fecha_actualizada(copy.deepcopy(doc), (("a", "b", "m"),)), doc)

    def test_con_fecha_confirmada_solo_cambian_los_corregidos(self):
        doc = {"jsonld": {"@graph": [{"@type": "Article", "dateModified": "2026-01-15"}]}}
        with mock.patch.object(e, "FECHA_CORRECCION", "2026-12-01"):
            corregido = e.fecha_actualizada(copy.deepcopy(doc), (("a", "b", "m"),))
            intacto = e.fecha_actualizada(copy.deepcopy(doc), ())
        self.assertEqual(corregido["jsonld"]["@graph"][0]["dateModified"], "2026-12-01")
        self.assertEqual(intacto, doc)


if __name__ == "__main__":
    unittest.main()
