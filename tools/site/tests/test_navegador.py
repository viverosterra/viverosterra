"""Pruebas en navegador con Playwright: consola limpia en las 108 páginas, accesibilidad del shell con axe, menú,
barra móvil, eventos de GA4 y shell sin desbordar. Se saltan si Playwright no está instalado (en CI sí lo está)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
import shell  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
REPRESENTATIVAS = ("/", "/pasto-en-rollo-tampico/", "/pasto-sintetico/", "/pasto-sintetico/toscana-28/",
                   "/diseno-jardines-tampico/", "/plantas-palmas-arboles-tampico/", "/catalogo.html", "/blog/",
                   "/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/", "/jardineria-altamira/", "/gracias/")
AXE_SHELL = """async () => {
  const incluir = ['.vt-head', '.vt-foot', '.vt-bar'].filter((s) => document.querySelector(s)).map((s) => [s]);
  const r = await axe.run({ include: incluir }, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
BORDE_DERECHO = """() => Math.max(...Array.from(document.querySelectorAll('.vt-head__bar, .vt-foot, [data-vt-bar]'))
  .map((e) => e.getBoundingClientRect().right)) - document.documentElement.clientWidth"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class NavegadorTest(unittest.TestCase):
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

        def enrutar(route):
            url = route.request.url
            if url.startswith(base) and "/api/" not in url:
                route.continue_()
            else:
                route.abort()

        contexto.route("**/*", enrutar)
        return contexto.new_page()

    def test_consola_limpia_en_todas_las_paginas(self):
        errores = []
        page = self.pagina()
        page.on("pageerror", lambda error: errores.append(f"{page.url} · pageerror · {error}"))
        page.on("console", lambda msg: errores.append(f"{page.url} · consola · {msg.text}")
                if msg.type == "error" and not msg.text.startswith("Failed to load resource") else None)
        page.on("response", lambda r: errores.append(f"{r.url} · HTTP {r.status}") if r.status >= 400 else None)
        # Sin colector de reportes: cualquier violación de la CSP en Report-Only (servidor.py manda la misma cabecera
        # que vercel.json) cuenta como error, para que CI la detecte antes de pasar la CSP a obligatoria.
        page.add_init_script(
            "window.__vtCsp = []; document.addEventListener('securitypolicyviolation', (e) => "
            "window.__vtCsp.push(e.violatedDirective + ' · ' + (e.blockedURI || 'inline')));")
        for path in shell.paginas_html():
            page.goto(self.base + servidor.url_de(path), wait_until="load")
            errores.extend(f"{page.url} · CSP · {v}" for v in page.evaluate("() => window.__vtCsp"))
        self.assertEqual(errores, [])

    def test_servidor_local_manda_la_csp_de_vercel(self):
        respuesta = self.pagina().goto(self.base + "/", wait_until="load")
        csp = respuesta.headers.get("content-security-policy-report-only", "")
        self.assertEqual(csp, servidor.cabeceras_globales()["Content-Security-Policy-Report-Only"])

    def test_shell_sin_violaciones_serias_de_axe(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in REPRESENTATIVAS:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_SHELL), [])

    def test_menu_movil_y_barra(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/blog/cuando-regar-pasto-san-agustin-tampico/", wait_until="load")
        self.assertTrue(page.locator("#vt-mmenu").is_hidden())
        page.click(".vt-burger")
        self.assertTrue(page.locator("#vt-mmenu").is_visible())
        self.assertEqual(page.get_attribute(".vt-burger", "aria-expanded"), "true")
        self.assertTrue(page.locator("[data-vt-bar]").is_visible())

    def test_panel_de_jardin_en_escritorio(self):
        page = self.pagina(1440)
        page.goto(self.base + "/", wait_until="load")
        boton = page.locator('.vt-nav button[aria-controls="vt-panel-jardin"]')
        boton.click()
        self.assertEqual(boton.get_attribute("aria-expanded"), "true")
        self.assertTrue(page.locator("#vt-panel-jardin").is_visible())
        page.keyboard.press("Escape")
        self.assertEqual(boton.get_attribute("aria-expanded"), "false")

    def test_eventos_de_ga4_y_firma(self):
        page = self.pagina(1440)
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        page.click(".vt-head__cta")
        page.click('.vt-foot a[href^="tel:"]')
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "servicio-pasto:header",
                                                  "service": "pasto-natural"}], eventos)
        self.assertIn(["event", "click_to_call", {"link_type": "tel", "cta_id": "servicio-pasto:footer",
                                                  "service": "pasto-natural"}], eventos)
        self.assertEqual(page.get_attribute(".vt-head__cta", "href").count("viverosterra.com"), 1)

    def test_shell_sin_desbordar(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in REPRESENTATIVAS:
                page.goto(self.base + ruta, wait_until="load")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(page.evaluate(BORDE_DERECHO), 1)


if __name__ == "__main__":
    unittest.main()
