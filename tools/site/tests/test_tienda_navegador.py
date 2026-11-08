"""La tienda de pasto sintético en Chromium (Etapa 2b): cotizador con los casos de J03 §3, lista que llega entera al
WhatsApp, "Agregar" que cabe en su tarjeta, precio en el primer pantallazo móvil, sin desbordar, axe de página completa,
CLS y una sola barra fija abajo. Se saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
from test_navegador import RECORRER_BARRAS  # noqa: E402
from test_plantillas_navegador import AXE, AXE_PAGINA, CLS  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

PAGINAS = ("/pasto-sintetico/", "/pasto-sintetico/toscana-28/", "/pasto-sintetico/envio/monterrey/",
           "/pasto-sintetico/perros/", "/pasto-sintetico-tampico/")
# Precio visible en el primer pantallazo de cada tipo de página.
PRECIO = {"/pasto-sintetico/": "[data-landed-hero] b", "/pasto-sintetico/toscana-28/": ".vt-ficha .vt-etiqueta__precio",
          "/pasto-sintetico/envio/monterrey/": ".vt-portada .vt-lede b",
          "/pasto-sintetico-tampico/": ".vt-portada .vt-etiqueta__precio"}
CORTADOS = """() => Array.from(document.querySelectorAll('.spec-card')).map((card) => {
  const boton = card.querySelector('.spec-card__add');
  const c = card.getBoundingClientRect();
  const b = boton.getBoundingClientRect();
  const cortado = b.right > c.right + 0.5 || boton.scrollWidth > boton.clientWidth + 1;
  return cortado ? card.querySelector('.spec-card__name').textContent.trim() : null;
}).filter(Boolean)"""
LAZY_EN_PANTALLA = """() => Array.from(document.images).filter((i) => {
  const r = i.getBoundingClientRect();
  return i.loading === 'lazy' && r.top < innerHeight && r.bottom > 0 && r.width > 200;
}).map((i) => i.src)"""


def mensaje(page, selector):
    return unquote(page.locator(selector).first.get_attribute("href").split("text=", 1)[1])


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class TiendaNavegadorTest(unittest.TestCase):
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

    def pagina(self, ancho=1440, alto=900):
        contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto})
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_()
                       if r.request.url.startswith(base) and "/api/" not in r.request.url else r.abort())
        page = contexto.new_page()
        errores = []  # la consola de las 108 páginas la revisa test_navegador; aquí, los errores de JS al interactuar
        page.on("pageerror", lambda e: errores.append(str(e)))
        self.addCleanup(lambda: self.assertEqual(errores, []))
        return page

    def cotizar(self, page, m2, estado):
        page.select_option("#estado", estado)
        page.fill("#m2", str(m2))
        page.dispatch_event("#m2", "input")

    def test_boton_agregar_entero_en_las_9_tarjetas(self):
        for ancho in (320, 1100, 1280, 1440):
            page = self.pagina(ancho)
            page.goto(self.base + "/pasto-sintetico/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.locator(".spec-card").count(), 9)
                self.assertEqual(page.evaluate(CORTADOS), [])

    def test_cotizador_con_los_casos_de_j03(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        casos = ((50, "CDMX", "$10,850", {3: "≈ $3,995 al mes", 6: "≈ $2,078 al mes"}),
                 (30, "Yucatán", "$8,270", {3: "≈ $3,045 al mes", 6: "≈ $1,584 al mes"}),
                 (120, "Tamaulipas", "$27,330", {12: "≈ $2,811 al mes"}),
                 (5, "showroom", "$1,395", {}))
        for m2, estado, total, planes in casos:
            self.cotizar(page, m2, estado)
            with self.subTest(m2=m2, estado=estado):
                self.assertEqual(page.inner_text("#q-total"), total)
                for plazo, texto in planes.items():
                    self.assertEqual(page.inner_text(f'#q-plans .plan[data-plan="{plazo}"] [data-plan-amount]'), texto)
        # $1,395 no llega al mínimo de 3 mensualidades ($2,000): solo queda contado.
        self.assertEqual(page.locator('#q-plans .plan input:not([disabled])').count(), 1)

    def test_envio_nacional_bajo_25_m2_bloquea_total_y_mensualidades(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        self.cotizar(page, 20, "Jalisco")
        self.assertEqual(page.inner_text("#q-total"), "—")
        self.assertIn("mínimo es 25 m²", page.inner_text("#q-error"))
        self.assertTrue(page.locator("#q-plans").is_hidden())
        self.assertNotIn("Total estimado", mensaje(page, ".vt-cotizador [data-cta-wa]"))

    def test_lo_agregado_llega_al_whatsapp_de_la_lista_y_del_cotizador(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/", wait_until="load")
        page.evaluate("() => localStorage.clear()")
        page.reload(wait_until="load")
        self.assertTrue(page.locator(".vt-subnav__n").is_hidden())
        page.click('[data-add="toscana-18"]')
        page.click('[data-add="irlanda-25"]')
        page.click('[data-add="toscana-28"]')
        self.assertEqual(page.inner_text(".vt-subnav__n"), "3")
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        self.cotizar(page, 50, "Nuevo León")
        cotizador = mensaje(page, ".vt-cotizador [data-cta-wa]")
        self.assertIn("Toscana 28", cotizador)
        # El modelo de la ficha no se repite en "También en mi lista" aunque esté en la lista.
        self.assertIn("También en mi lista: Toscana 18 (50 m²), Irlanda 25 (50 m²).", cotizador)
        self.assertEqual(cotizador.count("Toscana 28"), 1)
        page.click('.vt-vecino [data-agregar*="viena-30"]')  # botón de la comparativa con su modelo en data-agregar
        self.assertEqual(page.inner_text(".vt-subnav__n"), "4")
        self.assertIn("También en mi lista: Toscana 18 (50 m²), Irlanda 25 (50 m²), Viena 30 (50 m²).",
                      mensaje(page, ".vt-cotizador [data-cta-wa]"))
        page.click(".vt-subnav__lista")
        lista = mensaje(page, "#cot-send")
        for linea in ("• Toscana 18: 50 m²", "• Irlanda 25: 50 m²", "• Viena 30: 50 m²", "Entrega en Nuevo León."):
            self.assertIn(linea, lista)

    def test_precio_y_cta_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        for ruta, selector in PRECIO.items():
            page.goto(self.base + ruta, wait_until="load")
            caja = page.locator(selector).first.bounding_box()
            with self.subTest(ruta=ruta):
                self.assertLessEqual(caja["y"] + caja["height"], 812)
                self.assertEqual(page.evaluate(LAZY_EN_PANTALLA), [])

    def test_sin_desbordar_en_cuatro_anchos(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(sobra, 1)

    def test_axe_de_pagina_completa_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_una_sola_barra_fija_abajo_y_cls_bajo(self):
        page = self.pagina(375, 812)
        for ruta in PAGINAS:
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertLess(page.evaluate(CLS), 0.1)
                self.assertEqual(page.evaluate(RECORRER_BARRAS), "")


if __name__ == "__main__":
    unittest.main()
