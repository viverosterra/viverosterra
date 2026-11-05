import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import simulador  # noqa: E402

PAGE = """<html><body>
<section class="a"><h2>Precios</h2></section>
<section class="faq"><span>Preguntas frecuentes</span><h2>FAQ</h2></section>
<footer>pie</footer>
<script src="/js/vt-simulador.js?v=old" defer></script>
</body></html>"""


class SimuladorTest(unittest.TestCase):
    def test_inserta_antes_de_preguntas_frecuentes(self):
        html = simulador.apply_html(PAGE, "un sistema de riego", 18000)
        self.assertLess(html.index("data-simulador"), html.index('class="faq"'))
        self.assertGreater(html.index("data-simulador"), html.index('class="a"'))
        self.assertIn('value="18000"', html)

    def test_idempotente(self):
        once = simulador.apply_html(PAGE, "un sistema de riego", 18000)
        twice = simulador.apply_html(once, "un sistema de riego", 18000)
        self.assertEqual(once, twice)
        self.assertEqual(twice.count("data-simulador"), 1)
        self.assertEqual(twice.count("vt-simulador.js"), 1)
        self.assertEqual(twice.count("vt-mensualidades.js"), 1)
        self.assertLess(twice.index("vt-mensualidades.js"), twice.index("vt-simulador.js"))

    def test_sin_faq_va_antes_del_footer(self):
        page = PAGE.replace("Preguntas frecuentes", "Otra cosa")
        html = simulador.apply_html(page, "x", 1000)
        self.assertLess(html.index("data-simulador"), html.index("<footer"))
        self.assertGreater(html.index("data-simulador"), html.index('class="faq"'))

    def test_paginas_reales_tienen_un_simulador(self):
        for slug, _servicio, _monto in simulador.PAGES:
            html = (simulador.ROOT / slug / "index.html").read_text(encoding="utf-8")
            if "data-simulador" not in html:
                self.skipTest("simulador.py aún no se ha corrido")
            self.assertEqual(html.count("data-simulador"), 1, slug)
            self.assertEqual(html.count("vt-simulador.js"), 1, slug)
            self.assertEqual(html.count("vt-mensualidades.js"), 1, slug)


if __name__ == "__main__":
    unittest.main()
