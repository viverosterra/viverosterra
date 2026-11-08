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
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/toscana-28", "/catalogo", "/cuestionario", "/gracias",
                     "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertFalse(paginas.contexto(ruta)["barra"])

    def test_paginas_de_la_tienda_sin_cotizador_llevan_la_barra_del_shell(self):
        # Desde 2b ciudades y perros no tienen #buybar: sin la barra móvil se quedaban sin CTA fijo en celular.
        for ruta in ("/pasto-sintetico/perros", "/pasto-sintetico/envio/cdmx"):
            with self.subTest(ruta=ruta):
                self.assertTrue(paginas.contexto(ruta)["barra"])

    def test_sin_barra_del_shell_donde_la_pagina_tiene_su_barra_de_compra(self):
        # /pasto-sintetico-tampico tiene #buybar (precio + Cotizar): dos barras fijas se tapan a 375 px.
        self.assertFalse(paginas.contexto("/pasto-sintetico-tampico")["barra"])

    def test_mensaje_propio_del_articulo_y_tema_por_slug(self):
        ctx = paginas.contexto("/blog/cuando-regar-pasto-san-agustin-tampico")
        self.assertTrue(ctx["mensaje"].startswith('Hola, leí su artículo "¿Cuándo y cuánto regar el pasto San Agustín'))
        self.assertTrue(ctx["mensaje"].endswith("\n\n" + datos.FIRMA))
        self.assertEqual(ctx["servicio"], "pasto-natural")
        self.assertEqual(ctx["mensaje_pie"], ctx["mensaje"])
        temas = {"/blog/pasto-sintetico-para-perros": "pasto-sintetico", "/blog/palma-areca-tampico": "plantas",
                 "/blog/sistema-riego-automatizado-tampico": "jardin", "/blog/tezontle-usos-jardin-tampico": "materiales",
                 "/blog/plantas-interior-tampico": "plantas", "/blog/jardin-vertical-tampico-guia": "jardin"}
        for ruta, servicio in temas.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(paginas.contexto(ruta)["servicio"], servicio)

    def test_todo_articulo_del_blog_tiene_mensaje_propio(self):
        for path in sorted((paginas.PUBLIC / "blog").glob("*/index.html")):
            ruta = paginas.ruta_de(path)
            with self.subTest(ruta=ruta):
                self.assertNotEqual(paginas.contexto(ruta)["mensaje"], datos.mensaje("general"))

    def test_mensajes_de_catalogo_precios_tienda_y_ciudad(self):
        firma = "\n\n" + datos.FIRMA
        self.assertEqual(paginas.contexto("/catalogo")["mensaje"], "Hola, vi el catálogo y quiero cotizar una planta" + firma)
        precios = paginas.contexto("/precios")
        self.assertEqual(precios["mensaje"], "Hola, vi la lista de precios y quiero cotizar" + firma)
        self.assertEqual(precios["mensaje_pie"], "Hola, tengo una pregunta sobre precios" + firma)
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/toscana-28", "/pasto-sintetico/envio/cdmx"):
            with self.subTest(ruta=ruta):
                ctx = paginas.contexto(ruta)
                self.assertEqual(ctx["mensaje"], datos.mensaje("pasto-sintetico"))
                self.assertEqual(ctx["mensaje_pie"], "Hola, tengo una pregunta sobre pasto sintético" + firma)
        self.assertEqual(paginas.contexto("/")["mensaje_pie"], datos.mensaje("general"))

    def test_ruta_desconocida_falla(self):
        with self.assertRaises(KeyError):
            paginas.contexto("/no-existe")


if __name__ == "__main__":
    unittest.main()
