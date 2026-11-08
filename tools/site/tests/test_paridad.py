"""Paridad de contenido de las páginas migradas contra su captura anterior (tools/site/tests/paridad/*.json)."""
import importlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paridad  # noqa: E402


class ParidadTest(unittest.TestCase):
    def test_nada_se_pierde_sin_motivo(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            mapa = importlib.import_module(f"contenido.{contenido}").PARIDAD
            for categoria, faltantes in paridad.comparar(ruta, mapa).items():
                with self.subTest(ruta=ruta, categoria=categoria):
                    self.assertEqual(faltantes, [])

    def test_el_mapa_no_tiene_entradas_viejas(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            mapa = importlib.import_module(f"contenido.{contenido}").PARIDAD
            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
            conocidos = {item for c in paridad.CATEGORIAS for item in captura[c]}
            for viejo in list(mapa["reemplazos"]) + list(mapa["retirados"]):
                with self.subTest(ruta=ruta, entrada=viejo):
                    self.assertIn(viejo, conocidos)

    def test_opiniones_de_la_home_se_conservan(self):
        """Decisión del dueño (2026-11-07): las opiniones con nombre de la home son reales; no se pueden retirar."""
        mapa = importlib.import_module("contenido.inicio").PARIDAD
        titulo = "Lo que dicen nuestros clientes en Tampico"
        self.assertNotIn(titulo, mapa["retirados"])
        self.assertNotIn(titulo, mapa["reemplazos"])
        html = (paridad.paginas.PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertIn(titulo, paridad.extraer(html)["encabezados"])

    def test_cubierto_y_faltantes(self):
        self.assertTrue(paridad.cubierto("Primer riego", ["Primer riego Tú"]))
        self.assertTrue(paridad.cubierto("Pasto Sintético", ["pasto sintético."]))
        self.assertFalse(paridad.cubierto("Riego", ["Riegos"]))
        mapa = {"reemplazos": {"A": "B"}, "retirados": {"C": "motivo largo y claro"}}
        self.assertEqual(paridad.faltantes(["A", "C", "D"], ["B"], mapa), ["D"])
        self.assertEqual(paridad.faltantes(["A"], [], mapa), ["A → B (el reemplazo no está en la página)"])

    def test_extraer(self):
        html = ('<title>T</title><meta name="description" content="D"><main><h2>¿Cuánto?</h2><p>$1,500 y $ 85</p>'
                '<details><summary>¿Pregunta?</summary></details><a href="/x/#a">x</a><a href="//cdn">y</a></main>')
        e = paridad.extraer(html)
        self.assertEqual((e["meta"]["title"], e["meta"]["description"]), ("T", "D"))
        self.assertEqual(e["encabezados"], ["¿Cuánto?"])
        self.assertEqual(e["faq"], ["¿Pregunta?"])
        self.assertEqual(e["precios"], ["$1,500", "$85"])
        self.assertEqual(e["enlaces"], ["/x"])


if __name__ == "__main__":
    unittest.main()
