"""generar.py escribe las páginas con plantilla ya con el shell, y solo si cambian."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import datos  # noqa: E402
import generar  # noqa: E402
from ciudades import CIUDADES  # noqa: E402
from data import MODELOS  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402


class GenerarTest(unittest.TestCase):
    def test_paginas_registradas_tienen_contexto(self):
        esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
                      "/mantenimiento-jardines-tampico", "/sistema-riego-tampico", "/mayoreo-pasto-tampico",
                      "/palmas-mayoreo-proyectos", "/plantas-palmas-arboles-tampico", "/palmas-tropicales-tampico",
                      "/plantas-para-jardin-tampico", "/arboles-ornamentales-tampico",
                      "/arboles-para-banqueta-tampico", "/plantas-de-interior-tampico", "/catalogo",
                      "/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico", "/marmol-blanco-tampico",
                      "/piedra-bola-rio-tampico", "/pasto-sintetico", "/pasto-sintetico/perros"]
                     + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                     + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
                     + [ruta for _nombre, ruta in datos.ZONAS])
        self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
        for ruta, salida, _p, _c in generar.PAGINAS:
            paginas.contexto(ruta)
            self.assertEqual(paginas.ruta_de(paginas.PUBLIC / salida), ruta)

    def test_cargar_paginas_de_un_modulo_con_varias(self):
        ficha = generar.cargar("ficha:toscana-28")
        self.assertEqual(ficha.CONTENIDO["modelo"]["slug"], "toscana-28")
        self.assertIn("reemplazos", ficha.PARIDAD)
        self.assertIs(generar.cargar("inicio").CONTENIDO, generar.cargar("inicio").CONTENIDO)
        self.assertEqual(generar.contenido_de("/pasto-sintetico/envio/cdmx"), "ciudad:cdmx")

    def test_lo_publicado_es_lo_que_sale_de_la_plantilla(self):
        urls = activos.urls()
        for ruta, salida, plantilla, contenido in generar.PAGINAS:
            with self.subTest(ruta=ruta):
                publicado = (paginas.PUBLIC / salida).read_text(encoding="utf-8")
                self.assertEqual(generar.renderizar(ruta, plantilla, contenido, urls), publicado)
                self.assertEqual(shell.aplicar(publicado, ruta, urls), publicado)

    def test_escribe_solo_si_cambia(self):
        urls = activos.urls()
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            self.assertEqual(generar.escribir_todo(urls, destino), len(generar.PAGINAS))
            self.assertEqual(generar.escribir_todo(urls, destino), 0)
            for _r, salida, _p, _c in generar.PAGINAS:
                self.assertEqual((destino / salida).read_text(encoding="utf-8"),
                                 (paginas.PUBLIC / salida).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
