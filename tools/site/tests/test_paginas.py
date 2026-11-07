import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402


class RutaTest(unittest.TestCase):
    def test_ruta_de_archivos(self):
        base = Path(tempfile.mkdtemp())
        casos = {
            "index.html": "/",
            "catalogo.html": "/catalogo",
            "blog/index.html": "/blog",
            "blog/palma-areca-tampico/index.html": "/blog/palma-areca-tampico",
            "protocolo-cuidados-pasto-san-agustin.html": "/protocolo-cuidados-pasto-san-agustin",
            "pasto-sintetico/envio/cdmx/index.html": "/pasto-sintetico/envio/cdmx",
        }
        for rel, ruta in casos.items():
            with self.subTest(rel=rel):
                self.assertEqual(paginas.ruta_de(base / rel, public=base), ruta)

    def test_ruta_de_rechaza_lo_que_no_es_html(self):
        base = Path(tempfile.mkdtemp())
        with self.assertRaises(ValueError):
            paginas.ruta_de(base / "robots.txt", public=base)


class ContextoTest(unittest.TestCase):
    def test_servicio_de_pasto(self):
        ctx = paginas.contexto("/pasto-en-rollo-tampico")
        self.assertEqual((ctx["tipo"], ctx["activo"], ctx["servicio"]), ("servicio-pasto", "pasto-natural", "pasto-natural"))
        self.assertTrue(ctx["barra"])
        self.assertEqual(ctx["mensaje"], datos.mensaje("pasto-natural"))

    def test_prefijos(self):
        self.assertEqual(paginas.contexto("/pasto-sintetico/envio/cdmx")["tipo"], "ciudad")
        self.assertEqual(paginas.contexto("/pasto-sintetico/toscana-28")["tipo"], "tienda")
        self.assertEqual(paginas.contexto("/blog/palma-areca-tampico")["tipo"], "blog")
        self.assertEqual(paginas.contexto("/jardineria-altamira")["servicio"], "jardin")

    def test_sin_barra_en_tienda_catalogo_y_formularios(self):
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/perros", "/pasto-sintetico/envio/cdmx", "/catalogo",
                     "/cuestionario", "/gracias", "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertFalse(paginas.contexto(ruta)["barra"])

    def test_ruta_desconocida_falla(self):
        with self.assertRaises(KeyError):
            paginas.contexto("/no-existe")


if __name__ == "__main__":
    unittest.main()
