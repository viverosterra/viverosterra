"""El contenido de las páginas con plantilla es solo HTML en línea permitido y no rompe las reglas del dueño."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402


def cadenas(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from cadenas(v)
    elif isinstance(valor, (list, tuple)):
        for v in valor:
            yield from cadenas(v)


class ContenidoTest(unittest.TestCase):
    def modulos(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            yield ruta, generar.cargar(contenido)

    def test_solo_marcado_en_linea_permitido(self):
        for ruta, modulo in self.modulos():
            for texto in cadenas({k: v for k, v in modulo.CONTENIDO.items() if k not in ("meta", "jsonld", "cuerpo")}):
                with self.subTest(ruta=ruta, texto=texto[:60]):
                    self.assertEqual(componentes.etiquetas_no_permitidas(texto), [])

    def test_tipo_del_contenido_igual_al_de_paginas(self):
        for ruta, modulo in self.modulos():
            if "tipo" in modulo.CONTENIDO:
                with self.subTest(ruta=ruta):
                    self.assertEqual(modulo.CONTENIDO["tipo"], paginas.contexto(ruta)["tipo"])

    def test_paridad_con_motivos_escritos(self):
        for ruta, modulo in self.modulos():
            for viejo, motivo in modulo.PARIDAD["retirados"].items():
                with self.subTest(ruta=ruta, retirado=viejo):
                    self.assertGreater(len(motivo), 20)


if __name__ == "__main__":
    unittest.main()
