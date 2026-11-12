"""Paridad de contenido de las páginas migradas contra su captura anterior (tools/site/tests/paridad/*.json)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paridad  # noqa: E402
import datos  # noqa: E402
from contenido import articulo  # noqa: E402


def paginas_migradas():
    """Las páginas con captura anterior: los artículos nuevos (articulo.NUEVOS), la página de Nochebuenas, cuya URL
    solo redirigía, y las páginas nuevas de la SEO fase 2a (generar.NUEVAS) no tienen contra qué compararse."""
    return [p for p in generar.PAGINAS
            if p[0].removeprefix("/blog/") not in articulo.NUEVOS and p[0] != datos.NOCHEBUENAS["ruta"]
            and p[0] not in generar.NUEVAS]  # SEO fase 2a: páginas nuevas, sin captura anterior


class ParidadTest(unittest.TestCase):
    def test_nada_se_pierde_sin_motivo(self):
        for ruta, _salida, _plantilla, contenido in paginas_migradas():
            mapa = generar.cargar(contenido).PARIDAD
            for categoria, faltantes in paridad.comparar(ruta, mapa).items():
                with self.subTest(ruta=ruta, categoria=categoria):
                    self.assertEqual(faltantes, [])

    def test_el_mapa_no_tiene_entradas_viejas(self):
        for ruta, _salida, _plantilla, contenido in paginas_migradas():
            mapa = generar.cargar(contenido).PARIDAD
            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
            conocidos = {item for c in paridad.CATEGORIAS for item in captura[c]}
            for viejo in list(mapa["reemplazos"]) + list(mapa["retirados"]):
                with self.subTest(ruta=ruta, entrada=viejo):
                    self.assertIn(viejo, conocidos)

    def test_cambios_de_meta_declarados_son_de_la_captura(self):
        """PARIDAD["meta"] solo nombra claves que la página publicaba, con un valor distinto al de la captura."""
        for ruta, _salida, _plantilla, contenido in paginas_migradas():
            cambios = generar.cargar(contenido).PARIDAD.get("meta", {})
            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
            for clave, (nuevo, _motivo) in cambios.items():
                with self.subTest(ruta=ruta, clave=clave):
                    self.assertIn(clave, captura["meta"])
                    self.assertNotEqual(captura["meta"][clave], nuevo)

    def test_tipos_de_json_ld_retirados_son_de_la_captura(self):
        """PARIDAD["jsonld"] solo nombra tipos que la página publicaba y que ya no salen (si vuelven, sobra el motivo)."""
        for ruta, _salida, _plantilla, contenido in paginas_migradas():
            motivos = generar.cargar(contenido).PARIDAD.get("jsonld", {})
            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
            actuales = paridad.extraer(paridad.archivo(ruta).read_text(encoding="utf-8"))["jsonld_tipos"]
            for tipo in motivos:
                with self.subTest(ruta=ruta, tipo=tipo):
                    self.assertIn(tipo, captura["jsonld_tipos"])
                    self.assertNotIn(tipo, actuales)

    def test_tipos_retirados(self):
        self.assertEqual(paridad.tipos_retirados(["A", "B"], ["A"]), ["B"])
        self.assertEqual(paridad.tipos_retirados(["A", "B"], ["A"], {"B": "pasa a una referencia por @id al nodo"}), [])
        self.assertEqual(paridad.tipos_retirados(["A", "B"], ["A"], {"B": "corto"}), ["B"])

    def test_meta_distinta(self):
        viejo = {"title": "T", "description": "Desde $850"}
        self.assertEqual(paridad.meta_distinta(viejo, dict(viejo)), [])
        nuevo = {"title": "T", "description": "Desde $250"}
        self.assertEqual(paridad.meta_distinta(viejo, nuevo), ["description: 'Desde $850' → 'Desde $250'"])
        motivo = "Precio corregido por el dueño el 2026-11-07"
        self.assertEqual(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $250", motivo)}), [])
        self.assertEqual(len(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $300", motivo)})), 1)
        self.assertEqual(len(paridad.meta_distinta(viejo, nuevo, {"description": ("Desde $250", "corto")})), 1)

    def test_opiniones_de_la_home_se_conservan(self):
        """Decisión del dueño (2026-11-07): las opiniones con nombre de la home son reales; no se pueden retirar."""
        mapa = generar.cargar("inicio").PARIDAD
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
