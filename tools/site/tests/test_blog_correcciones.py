"""blog_correcciones: cada fila tiene una clave literal que no se renumera, y una respuesta del dueño es una línea en DECISIONES."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contenido import blog_correcciones as bc  # noqa: E402

FILAS = (("C900", "antes uno", "después uno", "motivo"), ("C901", "antes dos", "después dos", "motivo"))


class BlogCorreccionesTest(unittest.TestCase):
    def test_cada_fila_tiene_clave_unica(self):
        claves = bc.claves()
        self.assertEqual(len(claves), len(set(claves)))
        self.assertEqual([c for c in claves if not re.fullmatch(r"C\d{3}|T\d{2}", c)], [])

    def test_las_claves_no_se_renumeran(self):
        filas = {f[0]: f for lista in bc.FILAS.values() for f in lista} | {f[0]: f for f in bc.FILAS_TODOS}
        self.assertEqual(filas["C001"][1], "Las 8 palmas más vendidas en Tampico (con precios)")
        self.assertEqual(filas["T01"][1], "Las 8 Palmas Más Vendidas en Tampico (con Precios)")

    def test_sin_decisiones_quedan_las_tripletas(self):
        self.assertEqual(bc.resolver(FILAS, {}), (("antes uno", "después uno", "motivo"), ("antes dos", "después dos", "motivo")))

    def test_revertir_quita_solo_esa_fila(self):
        self.assertEqual(bc.resolver(FILAS, {"C900": bc.REVERTIR}), (("antes dos", "después dos", "motivo"),))

    def test_una_decision_con_texto_cambia_solo_el_despues(self):
        self.assertEqual(bc.resolver(FILAS, {"C901": "otro"})[1], ("antes dos", "otro", "motivo"))

    def test_clave_desconocida_detiene(self):
        with self.assertRaises(ValueError):
            bc.validar({"C999": bc.REVERTIR})

    def test_no_hay_decisiones_con_el_dueno_pendiente(self):
        self.assertEqual(bc.DECISIONES, {})


if __name__ == "__main__":
    unittest.main()
