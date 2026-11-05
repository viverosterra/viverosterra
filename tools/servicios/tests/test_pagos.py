import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hero  # noqa: E402
import planes_diseno  # noqa: E402
from pages import PAGES  # noqa: E402

CARD = """<div class="flex items-baseline gap-2">
            <span class="text-4xl font-display font-bold text-primary">{p}</span>
            <span class="text-gray-400 text-sm">MXN</span>
          </div>
          <p class="text-gray-500 text-xs mt-1">Entrega</p>"""
PAGE = "\n".join(CARD.format(p=p) for p in ("$3,000", "$6,500", "$18,000")) + '\n<span>$3,000</span>'


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

    def test_solo_tres_paginas_con_pago_nota(self):
        con = sorted(slug for slug, cfg in PAGES.items() if cfg.get("pago_nota"))
        self.assertEqual(con, ["diseno-jardines-tampico", "pasto-en-rollo-tampico", "sistema-riego-tampico"])


class PlanesDisenoTest(unittest.TestCase):
    def test_plazo_mas_largo_por_precio(self):
        html = planes_diseno.apply_html(PAGE)
        self.assertIn("o en 3 mensualidades de ≈ $1,105 con tarjeta (total $3,315)", html)
        self.assertIn("o en 6 mensualidades de ≈ $1,245 con tarjeta (total $7,468)", html)
        self.assertIn("o en 12 mensualidades de ≈ $1,852 con tarjeta (total $22,220)", html)

    def test_idempotente(self):
        once = planes_diseno.apply_html(PAGE)
        self.assertEqual(planes_diseno.apply_html(once), once)
        self.assertEqual(once.count("plan-pay"), 3)

    def test_pagina_real_tiene_tres_lineas(self):
        html = planes_diseno.PAGE.read_text(encoding="utf-8")
        self.assertEqual(html.count('class="plan-pay'), 3)


if __name__ == "__main__":
    unittest.main()
