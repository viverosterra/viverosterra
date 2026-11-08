"""/gracias: destino de los 6 formularios; la página cambia de ropa, no de URL ni de medición."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("gracias").CONTENIDO


class GraciasTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)

    def test_archivo_y_meta_de_siempre(self):
        fila = next(f for f in generar.PAGINAS if f[0] == "/gracias")
        self.assertEqual(fila[1], "gracias/index.html")
        self.assertEqual(K["meta"]["title"], "¡Gracias! Tu cotización está en camino · Viveros Terra")
        self.assertEqual(K["meta"]["robots"], "noindex, follow")
        self.assertEqual(K["meta"]["canonical"], f"{datos.SITIO}/gracias")

    def test_promesa_unica_y_visita_con_costo(self):
        self.assertIn(datos.PROMESA, self.html)
        self.assertIn(datos.HORARIO, self.html)
        self.assertIn(datos.VISITA_COSTO, self.html)
        self.assertNotRegex(self.html, r"2 horas|24 h\b|\bhoy\b")

    def test_adelantar_con_el_mensaje_y_la_medicion_de_main(self):
        self.assertIn('data-cta="utilidad:cuerpo"', self.html)
        self.assertIn("Adelantar por WhatsApp", self.html)
        self.assertIn(mensajes_paginas.UTILITARIAS["gracias"], unquote(self.html))

    def test_sin_scripts_propios(self):
        self.assertNotIn("<script src", self.html)


if __name__ == "__main__":
    unittest.main()
