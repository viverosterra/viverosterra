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
# Elementos fijos que ocupan el fondo de la pantalla y se ven (los ocultos con translateY quedan abajo del viewport).
BARRAS_FIJAS_ABAJO = """() => Array.from(document.querySelectorAll('body *')).filter((e) => {
  const s = getComputedStyle(e);
  if (s.position !== 'fixed' || s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return false;
  const r = e.getBoundingClientRect();
  return r.height > 0 && r.width > innerWidth / 2 && r.top < innerHeight - 1 && r.bottom >= innerHeight - 2;
}).map((e) => e.id ? '#' + e.id : e.className.toString().split(' ')[0])"""
RECORRER_BARRAS = """async () => {
  const barras = """ + BARRAS_FIJAS_ABAJO + """;
  const cuadro = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  for (let y = 0; y <= document.documentElement.scrollHeight; y += innerHeight) {
    scrollTo({ top: y, behavior: 'instant' });
    await cuadro();
    const visibles = barras();
    if (visibles.length > 1) return 'en y=' + y + ': ' + visibles.join(' + ');
  }
  return '';
}"""
QUIETO = """() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(
  () => r(document.getAnimations().every((a) => a.playState !== 'running')))))"""
BORDE_DERECHO = """() => Math.max(...Array.from(document.querySelectorAll('.vt-head__bar, .vt-foot, [data-vt-bar]'))
  .map((e) => e.getBoundingClientRect().right)) - document.documentElement.clientWidth"""
# Encabezado a un ancho dado: lista de problemas (vacía si cabe). El CTA entero dentro de la pantalla, el menú sin
# encimarse con el logo ni con el CTA y cada etiqueta del menú en un solo renglón.
ENCABEZADO_CABE = """() => {
  const vw = document.documentElement.clientWidth, mal = [];
  const caja = (s) => document.querySelector(s).getBoundingClientRect();
  const bar = caja('.vt-head__bar'), cta = caja('.vt-head__cta'), logo = caja('.vt-head__logo');
  if (bar.right > vw + 1) mal.push('barra sale ' + Math.round(bar.right - vw) + 'px');
  if (cta.left < 0 || cta.right > vw + 1) mal.push('CTA sale ' + Math.round(cta.right - vw) + 'px');
  const nav = document.querySelector('.vt-nav');
  if (getComputedStyle(nav).display !== 'none') {
    const n = nav.getBoundingClientRect();
    if (n.left < logo.right - 1 || n.right > cta.left + 1) mal.push('menú encimado');
    const tops = Array.from(nav.querySelectorAll('.vt-nav__top'));
    if (tops.length !== 6) mal.push(tops.length + ' entradas en el menú');
    for (const t of tops) {
      // solo el texto: el chevron SVG del botón tiene otra altura y no cuenta como renglón
      const texto = document.createTreeWalker(t, NodeFilter.SHOW_TEXT).nextNode(), r = document.createRange();
      r.selectNodeContents(texto);
      if (new Set(Array.from(r.getClientRects(), (c) => Math.round(c.top))).size > 1) mal.push(texto.data + ' en 2 renglones');
    }
  }
  return mal;
}"""
ANCHOS_ENCABEZADO = (*range(320, 980, 40), *range(980, 1441, 20), *range(1520, 1921, 80))


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

    def test_nunca_dos_barras_fijas_abajo_a_375(self):
        page = self.pagina(375, 812)
        dobles = []
        for path in shell.paginas_html():
            page.goto(self.base + servidor.url_de(path), wait_until="load")
            # Sin transiciones, y bajando de a una pantalla: los IntersectionObserver de las barras (la de compra
            # aparece al pasar #comprar) solo avisan cuando un elemento cruza el viewport, no si se salta.
            page.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important}")
            barras = page.evaluate(RECORRER_BARRAS)
            if barras:
                dobles.append(f"{servidor.url_de(path)}: {barras}")
        self.assertEqual(dobles, [])

    def test_articulos_del_blog_sin_desbordar_a_375(self):
        page = self.pagina(375, 812)
        anchas = []
        for path in sorted((shell.PUBLIC / "blog").glob("*/index.html")):
            page.goto(self.base + servidor.url_de(path), wait_until="load")
            sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if sobra > 1:
                anchas.append(f"{servidor.url_de(path)}: {sobra}px")
        self.assertEqual(anchas, [])

    def test_window_open_de_whatsapp_sale_firmado(self):
        page = self.pagina(1440)
        page.add_init_script("window.__abiertos = []; window.open = (url) => { window.__abiertos.push(String(url)); return null; };")
        # Diseño sale de su plantilla desde la Etapa 2c (un botón por plan); piedra bola conserva sendWA hasta la 2f.
        page.goto(self.base + "/piedra-bola-rio-tampico/", wait_until="load")
        page.evaluate("() => sendWA('Hola, quiero cotizar piedra bola de río')")
        abiertos = page.evaluate("() => window.__abiertos")
        self.assertEqual(len(abiertos), 1)
        self.assertEqual(abiertos[0].count("viverosterra.com"), 1)
        self.assertTrue(abiertos[0].startswith("https://wa.me/528333268008?text="))

    def test_cotizador_de_la_tienda_manda_el_lead_con_cta_y_servicio(self):
        page = self.pagina(1440)
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        page.locator("[data-cta-wa]:visible").first.click()
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        leads = [e[2] for e in eventos if e[1] == "generate_lead"]
        self.assertEqual(len(leads), 1)
        self.assertEqual({k: leads[0][k] for k in ("method", "cta_id", "service")},
                         {"method": "whatsapp_cotizador", "cta_id": "tienda:cotizador", "service": "pasto-sintetico"})

    def test_menu_movil_abierto_deja_el_telefono_arriba_de_la_barra(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/blog/cuando-regar-pasto-san-agustin-tampico/", wait_until="load")
        page.click(".vt-burger")
        page.evaluate("() => document.querySelectorAll('#vt-mmenu details').forEach((d) => { d.open = true; })")
        page.evaluate("() => { const m = document.getElementById('vt-mmenu'); m.scrollTop = m.scrollHeight; }")
        page.wait_for_function(QUIETO)
        tel = page.locator('.vt-mmenu__meta a[href^="tel:"]').bounding_box()
        barra = page.locator("[data-vt-bar]").bounding_box()
        self.assertLessEqual(tel["y"] + tel["height"], barra["y"])

    def test_shell_sin_desbordar(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in REPRESENTATIVAS:
                page.goto(self.base + ruta, wait_until="load")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(page.evaluate(BORDE_DERECHO), 1)


    def test_encabezado_cabe_en_todos_los_anchos(self):
        # A 1100–1139px el botón "Cotizar por WhatsApp" se salía hasta 30px de la pantalla en las 108 páginas.
        page = self.pagina()
        for ruta in ("/", "/pasto-en-rollo-tampico/"):
            page.goto(self.base + ruta, wait_until="load")
            for ancho in ANCHOS_ENCABEZADO:
                page.set_viewport_size({"width": ancho, "height": 900})
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(ENCABEZADO_CABE), [])

if __name__ == "__main__":
    unittest.main()
