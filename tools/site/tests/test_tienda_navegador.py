"""El botón "Agregar" de cada tarjeta del hub de la tienda cabe entero en su tarjeta (A01 P0-1: a 1440 salía "Agre")."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CORTADOS = """() => Array.from(document.querySelectorAll('.spec-card')).map((card) => {
  const boton = card.querySelector('.spec-card__add');
  const c = card.getBoundingClientRect();
  const b = boton.getBoundingClientRect();
  const cortado = b.right > c.right + 0.5 || boton.scrollWidth > boton.clientWidth + 1;
  return cortado ? card.querySelector('.spec-card__name').textContent.trim() : null;
}).filter(Boolean)"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class TiendaHubTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.servidor = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.navegador = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.navegador.close()
        cls.pw.stop()
        cls.servidor.shutdown()
        cls.servidor.server_close()

    def test_boton_agregar_entero_en_las_9_tarjetas(self):
        base = self.base
        for ancho in (1100, 1280, 1440):
            contexto = self.navegador.new_context(viewport={"width": ancho, "height": 900})
            self.addCleanup(contexto.close)
            contexto.route("**/*", lambda route: route.continue_()
                           if route.request.url.startswith(base) and "/api/" not in route.request.url else route.abort())
            page = contexto.new_page()
            page.goto(base + "/pasto-sintetico/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.locator(".spec-card").count(), 9)
                self.assertEqual(page.evaluate(CORTADOS), [])


if __name__ == "__main__":
    unittest.main()
