"""Paridad de especies (Etapa 2e): cada especie que publicaba una página de plantas sigue en ella con su nombre
científico (o la corrección declarada), o su contenido dice a qué página se fue (PARIDAD["especies"]["reemplazos"]:
nombre → (ruta, nombre allá)) o por qué se retiró (PARIDAD["especies"]["retirados"]). Los enlaces al blog no se pierden."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paridad_plantas as pp  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

CAPTURA = json.loads(pp.CAPTURA.read_text(encoding="utf-8"))
MIGRADAS = {r for r, _s, _p, _c in generar.PAGINAS} & set(pp.RUTAS)


def nombres(ruta):
    return {n.casefold(): s for n, s in pp.extraer(ruta)["especies"]}


class PlantasParidadTest(unittest.TestCase):
    def test_cada_especie_sigue_se_mueve_o_se_retira_con_motivo(self):
        for ruta in sorted(MIGRADAS):
            mapa = generar.cargar(generar.contenido_de(ruta)).PARIDAD.get("especies", {"reemplazos": {}, "retirados": {}})
            actuales = nombres(ruta)
            for nombre, cientifico in CAPTURA[ruta]["especies"]:
                with self.subTest(ruta=ruta, especie=nombre):
                    if nombre.casefold() in actuales:
                        if cientifico:
                            self.assertEqual(actuales[nombre.casefold()], cd.CIENTIFICOS_CORREGIDOS.get(cientifico, cientifico))
                    elif nombre in mapa["reemplazos"]:
                        destino, otro = mapa["reemplazos"][nombre]
                        self.assertIn(otro.casefold(), nombres(destino) if destino in MIGRADAS else {otro.casefold()})
                    else:
                        self.assertGreater(len(mapa["retirados"].get(nombre, "")), 20)

    def test_enlaces_al_blog_no_se_pierden(self):
        for ruta in sorted(MIGRADAS):
            with self.subTest(ruta=ruta):
                self.assertLessEqual(set(CAPTURA[ruta]["blog"]), set(pp.extraer(ruta)["blog"]))


if __name__ == "__main__":
    unittest.main()
