import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hero  # noqa: E402
from pages import PAGES  # noqa: E402

# Salen de tools/site/plantillas/ (Etapas 2a y 2c): ningún parche de tools/servicios las toca.
CON_PLANTILLA = ("pasto-en-rollo-tampico", "diseno-jardines-tampico")


class PagoNotaTest(unittest.TestCase):
    def cfg(self, **extra):
        return dict(PAGES["sistema-riego-tampico"], img=None, **extra)

    def test_pago_nota_enlaza_al_simulador(self):
        html = hero.hero_html(self.cfg())
        self.assertIn('class="svc-hero__pay"', html)
        self.assertIn('href="#sim-titulo">Calcula tu plan</a>', html)
        self.assertLess(html.index("svc-hero__lede"), html.index("svc-hero__pay"))

    def test_sin_pago_nota_no_hay_linea(self):
        cfg = {k: v for k, v in self.cfg().items() if k != "pago_nota"}
        self.assertNotIn("svc-hero__pay", hero.hero_html(cfg))

    def test_solo_riego_con_pago_nota(self):
        con = sorted(slug for slug, cfg in PAGES.items() if cfg.get("pago_nota"))
        self.assertEqual(con, ["sistema-riego-tampico"])

    def test_paginas_con_plantilla_fuera_de_los_parches(self):
        for slug in CON_PLANTILLA:
            with self.subTest(slug=slug):
                self.assertNotIn(slug, PAGES)


if __name__ == "__main__":
    unittest.main()
