"""Utilitarias en Chromium (Etapa 2i): axe de página completa, sin desbordar, consola limpia, y los flujos que el dueño
recibe: el cuestionario a formsubmit y a /gracias (interceptado: nunca sale un correo real), datos de envío a WhatsApp y el filtro de 404.
Se saltan sin Playwright."""
import base64
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qsl, unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
RUTAS = ("/politicas/", "/politica-privacidad/", "/gracias/", "/cuestionario.html", "/datos-envio/",
         "/protocolo-cuidados-pasto-san-agustin.html", "/vivero-tampico/", "/404.html")
AXE_TODO = """async () => {
  const r = await axe.run(document, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
SALIDOS = """() => { const w = document.documentElement.clientWidth;
  return Array.from(document.querySelectorAll('main *')).filter((e) => { const c = e.getBoundingClientRect();
    return c.width && c.height && getComputedStyle(e).visibility !== 'hidden' && (c.right > w + 0.5 || c.left < -0.5)
      && e.name !== '_honey'; }).map((e) => e.tagName + '.' + e.className); }"""


@unittest.skipIf(sync_playwright is None, "sin Playwright")
class UtilitariasNavegadorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.srv = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.nav = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.nav.close()
        cls.pw.stop()
        cls.srv.shutdown()
        cls.srv.server_close()

    def pagina(self, ancho=375):
        page = self.nav.new_page(viewport={"width": ancho, "height": 812})
        page.route("**googletagmanager.com/**", lambda r: r.abort())
        self.addCleanup(page.close)
        return page

    def test_axe_sin_serias(self):
        for ruta in RUTAS:
            with self.subTest(ruta=ruta):
                page = self.pagina(1440)
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(path=str(AXE))
                self.assertEqual(page.evaluate(AXE_TODO), [])

    def test_sin_desbordar(self):
        for ancho in (320, 375, 768, 1024, 1440, 1920):
            page = self.pagina(ancho)
            for ruta in RUTAS:
                with self.subTest(ruta=ruta, ancho=ancho):
                    page.goto(self.base + ruta, wait_until="load")
                    self.assertEqual(page.evaluate(SALIDOS), [])

    def test_consola_limpia(self):
        for ruta in RUTAS:
            page = self.pagina()
            errores = []
            page.on("pageerror", lambda e: errores.append(str(e)))
            page.on("console", lambda m: errores.append(m.text) if m.type == "error" and "ERR_FAILED" not in m.text else None)
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertEqual(errores, [])

    def test_gracias_manda_page_view_una_vez_y_ningun_evento(self):
        page = self.pagina(1440)
        page.goto(self.base + "/gracias/", wait_until="load")
        capa = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a))")
        self.assertEqual([a[:2] for a in capa if a[:1] == ["config"]], [["config", datos.GA4_ID]])
        self.assertEqual([a for a in capa if a[:1] == ["event"]], [])

    def _cuestionario(self):
        """El POST nativo a formsubmit se intercepta (ningún correo real): se contesta con el HTML que lleva a `_next`, como
        hace formsubmit, y /gracias se sirve desde public/ sin salir a producción."""
        page = self.pagina(1440)
        enviados = []
        def formsubmit(route):
            pedido = route.request
            enviados.append((pedido.method, pedido.url, pedido.headers.get("content-type"), pedido.post_data or ""))
            destino = dict(parse_qsl(pedido.post_data or "")).get("_next", "")
            route.fulfill(status=200, content_type="text/html",
                          body=f'<!doctype html><meta http-equiv="refresh" content="0;url={destino}">')
        def produccion(route):
            if route.request.url == f"{datos.SITIO}/gracias":
                route.fulfill(status=200, content_type="text/html", path=str(paginas.PUBLIC / "gracias" / "index.html"))
            else:
                route.abort()
        page.route("https://formsubmit.co/**", formsubmit)
        page.route(f"{datos.SITIO}/**", produccion)
        page.goto(self.base + "/cuestionario.html", wait_until="load")
        return page, enviados

    def _hasta_el_final(self, page):
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        for _ in range(4):
            page.click("#btn-next")

    def test_no_avanza_sin_los_obligatorios(self):
        page, _ = self._cuestionario()
        page.click("#btn-next")
        self.assertTrue(page.locator("#page-1").is_visible())
        self.assertFalse(page.locator("#page-2").is_visible())

    def test_solo_se_ve_un_paso(self):
        page, _ = self._cuestionario()
        self.assertEqual(page.locator("[data-vt-paso]:visible").count(), 1)
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.click("#btn-next")
        self.assertEqual(page.locator("[data-vt-paso]:visible").count(), 1)
        self.assertEqual(page.locator("#step-counter").inner_text(), "Paso 2 de 5")

    def test_enter_a_medio_camino_no_envia(self):
        page, enviados = self._cuestionario()
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.press("#whatsapp", "Enter")
        self.assertEqual(enviados, [])
        self.assertTrue(page.locator("#page-2").is_visible())

    def test_envio_a_formsubmit_y_aviso_en_la_pagina(self):
        page, enviados = self._cuestionario()
        self._hasta_el_final(page)
        page.check('input[name="prioridad"][value="Fácil de mantener"]', force=True)
        # Se detiene el envío una vez para leer el dataLayer antes de salir de la página; luego se envía de verdad.
        page.evaluate("() => document.addEventListener('submit', (e) => e.preventDefault(), { once: true })")
        page.click("#submit-btn")
        eventos = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertEqual(enviados, [])
        with page.expect_navigation(url=f"{datos.SITIO}/gracias"):
            page.evaluate("() => document.getElementById('mainForm').submit()")
        self.assertEqual(len(enviados), 1)
        metodo, url, tipo, cuerpo = enviados[0]
        self.assertEqual((metodo, url), ("POST", f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"))
        self.assertEqual(tipo, "application/x-www-form-urlencoded")
        campos = dict(parse_qsl(cuerpo, keep_blank_values=True))
        self.assertEqual(campos["nombre"], "María Ejemplo")
        self.assertEqual(campos["prioridad"], "Fácil de mantener")
        self.assertEqual(campos["_next"], f"{datos.SITIO}/gracias")
        self.assertEqual(campos["_honey"], "")
        self.assertIn("_subject", campos)
        self.assertEqual(eventos, [["event", "generate_lead", {"method": "formulario", "cta_id": "cuestionario:formulario",
                                                               "service": "jardin"}]])
        self.assertEqual(page.url, f"{datos.SITIO}/gracias")
        self.assertEqual(page.locator("h1").inner_text(), "¡Recibimos tu información!")

    def test_riego_y_otro_condicionales_y_suma_de_areas(self):
        page, _ = self._cuestionario()
        page.fill("#nombre", "María Ejemplo")
        page.fill("#whatsapp", "8330000000")
        page.click("#btn-next")
        self.assertFalse(page.locator("#cond-riego").is_visible())
        page.check('input[name="riego_instalado"][value="No"]', force=True)
        self.assertTrue(page.locator("#cond-riego").is_visible())
        page.check('input[name="riego_instalado"][value="Sí"]', force=True)
        self.assertFalse(page.locator("#cond-riego").is_visible())
        page.check("#rb-otro-esp", force=True)
        self.assertTrue(page.locator("#otro-esp-wrap").is_visible())
        page.fill("#area_pasto", "60")
        page.fill("#area_jard", "20")
        self.assertEqual(page.input_value("#area_total_input"), "80")

    def _envio(self, query=""):
        page = self.pagina()
        destino = []
        page.route("https://wa.me/**", lambda r: (destino.append(r.request.url), r.abort()))
        page.goto(self.base + "/datos-envio/" + query, wait_until="load")
        return page, destino

    def test_datos_de_envio_arma_el_mismo_mensaje_que_main(self):
        carga = {"n": "Ana López", "p": "Toscana 28", "f": "VT-1", "t": "$7,000", "s": "Jalisco", "c": "Zapopan", "z": "45000"}
        d = base64.urlsafe_b64encode(json.dumps(carga).encode()).decode().rstrip("=")
        page, destino = self._envio("?d=" + d)
        self.assertEqual(page.locator("#hola").inner_text(), "Hola Ana, ¿a dónde te lo enviamos?")
        self.assertTrue(page.locator("#order").is_visible())
        self.assertEqual(page.input_value("#estado"), "Jalisco")
        for campo, valor in (("#calle", "Hidalgo 1"), ("#colonia", "Centro"), ("#ref", "Frente a la farmacia"), ("#tel", "3310000000")):
            page.fill(campo, valor)
        with page.expect_request("https://wa.me/**"):
            page.click("#enviar")
        texto = unquote(destino[0])
        self.assertTrue(destino[0].startswith("https://wa.me/528333268008?text="))
        for pieza in ("Hola, aquí están mis datos de envío para el pedido VT-1:", "📍 *Dirección de entrega*", "Calle y número: Hidalgo 1",
                      "Municipio: Zapopan", "Código Postal: 45000", "📦 *Recibe*", "Nombre: Ana López", "🧾 Factura: no", "#VT1:"):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, texto)

    def test_datos_de_envio_marca_errores_y_no_abre_whatsapp(self):
        page, destino = self._envio()
        self.assertFalse(page.locator("#order").is_visible())
        page.click("#enviar")
        self.assertTrue(page.locator("#err").is_visible())
        self.assertTrue(page.locator("#calle.bad").count() == 1)
        self.assertTrue(page.locator("#calle ~ .msg, .vt-campo:has(#calle) .msg").first.is_visible())
        self.assertEqual(destino, [])

    def test_factura_se_despliega(self):
        page, _ = self._envio()
        self.assertFalse(page.locator("#fact").is_visible())
        page.check("#quiere")
        self.assertTrue(page.locator("#fact").is_visible())

    def test_filtro_de_404(self):
        page = self.pagina()
        page.goto(self.base + "/404.html", wait_until="load")
        total = page.locator("[data-vt-servicio-404]:visible").count()
        page.fill("#vt-buscar-404", "tezontle")
        self.assertEqual(page.locator("[data-vt-servicio-404]:visible").count(), 1)
        page.fill("#vt-buscar-404", "zzzz")
        self.assertTrue(page.locator("#vt-vacio-404").is_visible())
        page.fill("#vt-buscar-404", "")
        self.assertEqual(page.locator("[data-vt-servicio-404]:visible").count(), total)

    def test_anclas_de_politicas_llegan_bajo_el_menu(self):
        page = self.pagina(1440)
        for ancla in ("garantia-plantas", "garantia-pasto", "mensualidades", "devoluciones"):
            with self.subTest(ancla=ancla):
                page.goto(f"{self.base}/politicas/#{ancla}", wait_until="load")
                self.assertTrue(page.evaluate(
                    "(id) => { const c = document.getElementById(id).getBoundingClientRect(); return c.top >= 0 && c.top < 400; }", ancla))


if __name__ == "__main__":
    unittest.main()
