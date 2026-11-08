"""tools/servicios ya no toca las páginas que salen de tools/site/plantillas/ (Etapas 2a, 2c, 2d, 2e y 2f)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hero  # noqa: E402
from pages import PAGES  # noqa: E402

CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico", "mantenimiento-jardines-tampico",
                 "sistema-riego-tampico", "mayoreo-pasto-tampico", "palmas-mayoreo-proyectos",
                 "plantas-palmas-arboles-tampico", "palmas-tropicales-tampico", "plantas-para-jardin-tampico",
                 "arboles-ornamentales-tampico", "arboles-para-banqueta-tampico", "plantas-de-interior-tampico",
                 "tierra-negra-vegetal-tampico")


class PaginasConPlantillaTest(unittest.TestCase):
    def test_paginas_con_plantilla_fuera_de_los_parches(self):
        for slug in CON_PLANTILLA:
            with self.subTest(slug=slug):
                self.assertNotIn(slug, PAGES)

    def test_la_portada_ya_no_lleva_linea_de_pago_ni_ancla_al_simulador_viejo(self):
        cfg = dict(PAGES["vivero-tampico"], img=None)
        html = hero.hero_html(cfg)
        self.assertNotIn("svc-hero__pay", html)
        self.assertNotIn("#sim-titulo", html)
        self.assertFalse(any(c.get("pago_nota") for c in PAGES.values()))


if __name__ == "__main__":
    unittest.main()
