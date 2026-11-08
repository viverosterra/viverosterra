"""Páginas con plantilla en Chromium: axe de página completa, primer pantallazo móvil, Medidor, sin desbordar y CLS.
Se saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
PAGINAS = ("/", "/pasto-en-rollo-tampico/")
# Etapa 2c: servicios de jardín con la plantilla de servicio (sin Medidor).
SERVICIOS = ("/diseno-jardines-tampico/", "/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/")
CON_PLANTILLA = PAGINAS + SERVICIOS
AXE_PAGINA = """async () => {
  const r = await axe.run(document, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
CLS = """() => new Promise((listo) => {
  let total = 0;
  new PerformanceObserver((lista) => { lista.getEntries().forEach((e) => { if (!e.hadRecentInput) total += e.value; }); })
    .observe({ type: 'layout-shift', buffered: true });
  setTimeout(() => listo(total), 1500);
})"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class PlantillasNavegadorTest(unittest.TestCase):
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
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        return contexto.new_page()

    def test_axe_de_pagina_completa_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in CON_PLANTILLA:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_precio_y_cta_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        for ruta in CON_PLANTILLA:
            page.goto(self.base + ruta, wait_until="load")
            precio = page.locator(".vt-portada .vt-etiqueta__precio").bounding_box()
            cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
            with self.subTest(ruta=ruta):
                self.assertLessEqual(precio["y"] + precio["height"], 812)
                self.assertLessEqual(cta["y"] + cta["height"], 812)

    def test_barra_no_tapa_la_etiqueta_y_cta_a_la_vista_en_celulares_cortos(self):
        """Revisión de 2c: en mantenimiento, a 375×667 y 320×640 el CTA del hero cabe en la primera pantalla y la barra
        móvil (que se oculta mientras el CTA se ve) no tapa la etiqueta de precio con la página sin desplazar."""
        for ancho, alto in ((375, 667), (320, 640)):
            page = self.pagina(ancho, alto)
            page.goto(self.base + "/mantenimiento-jardines-tampico/", wait_until="load")
            page.wait_for_function("() => document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
            etiqueta = page.locator(".vt-portada .vt-etiqueta").bounding_box()
            cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
            with self.subTest(ancho=ancho, alto=alto):
                self.assertLessEqual(cta["y"] + cta["height"], alto)
                self.assertLessEqual(etiqueta["y"] + etiqueta["height"], alto)

    def test_cta_en_la_primera_pantalla_a_1024(self):
        """Revisión de 2c: a 1024×800 la portada compacta deja el CTA de los servicios de jardín en la primera pantalla."""
        page = self.pagina(1024, 800)
        for ruta in SERVICIOS:
            page.goto(self.base + ruta, wait_until="load")
            cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
            with self.subTest(ruta=ruta):
                self.assertLessEqual(cta["y"] + cta["height"], 800)

    def test_tabla_de_planes_de_diseno_plegada_en_celular_y_abierta_desde_768(self):
        for ancho, abierta in ((375, False), (768, True), (1440, True)):
            page = self.pagina(ancho)
            page.goto(self.base + "/diseno-jardines-tampico/", wait_until="load")
            plegable = page.locator("details[data-vt-plegable]")
            with self.subTest(ancho=ancho):
                self.assertEqual(plegable.evaluate("d => d.open"), abierta)
                self.assertEqual(plegable.locator("table").is_visible(), abierta)
                self.assertEqual(plegable.locator("summary h3").inner_text(), "Compara los 3 planes en detalle")
        page.locator("details[data-vt-plegable] summary").click()
        self.assertFalse(page.locator("details[data-vt-plegable]").evaluate("d => d.open"))

    def test_sin_desbordar_en_cuatro_anchos(self):
        for ancho in (320, 375, 768, 1024, 1440):
            page = self.pagina(ancho)
            for ruta in CON_PLANTILLA:
                page.goto(self.base + ruta, wait_until="load")
                sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(sobra, 1)

    def test_estado_inicial_del_medidor_igual_al_html(self):
        for ruta in PAGINAS:
            page = self.pagina()
            page.add_init_script("window.__antes = null; document.addEventListener('readystatechange', () => {"
                                 " if (document.readyState === 'interactive' && !window.__antes) window.__antes ="
                                 " document.querySelector('[data-vt-medidor] .vt-medidor__res').innerText; });")
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertEqual(page.evaluate("() => window.__antes"),
                                 page.locator("[data-vt-medidor] .vt-medidor__res").inner_text())

    def test_medidor_calcula_avisa_y_arma_el_mensaje(self):
        page = self.pagina()
        page.goto(self.base + "/", wait_until="load")
        caja = page.locator("[data-vt-medidor]")
        caja.locator('[data-vt-campo="largo"]').fill("10")
        caja.locator('[data-vt-campo="ancho"]').fill("10")
        caja.locator('input[value="mayoreo"]').check(force=True)
        caja.locator('[data-vt-campo="colonia"]').fill("Lomas de Rosales")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$8,500")
        self.assertTrue(caja.locator('[data-vt-o="aviso"]').is_visible())
        self.assertIn("Te faltan 400 m²", caja.locator('[data-vt-o="aviso"]').inner_text())
        mensaje = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
        self.assertIn("Medidas: 10.00 × 10.00 m = 100 m²", mensaje)
        self.assertIn("Colonia: Lomas de Rosales", mensaje)
        self.assertIn("Me interesa: contado", mensaje)
        # Con $8,500 aplican 3 y 6 mensualidades; 12 queda deshabilitado. El plan elegido viaja en el mensaje.
        self.assertTrue(caja.locator('input[name="inicio-plazo"][value="12"]').is_disabled())
        caja.locator('input[name="inicio-plazo"][value="6"]').check(force=True)
        mensaje = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
        self.assertRegex(mensaje, r"Me interesa: 6 mensualidades de \$[\d,]+ con tarjeta de crédito \(total \$[\d,]+\)")
        self.assertIn("6 mensualidades de", caja.locator('[data-vt-o="plan"]').inner_text())
        # Un lado de 1,000 m o más: se pide escribirnos y el botón manda el mensaje de proyecto, sin calcular en silencio.
        caja.locator('[data-vt-campo="largo"]').fill("1200")
        self.assertIn("Para áreas tan grandes, escríbenos", caja.locator('[data-vt-o="aviso"]').inner_text())
        grande = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
        self.assertEqual(grande, datos.con_firma(datos.MENSAJES["empresas"]))
        caja.locator('[data-vt-campo="largo"]').fill("10")
        caja.locator('[data-vt-campo="ancho"]').fill("")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "—")
        # Sin medida válida, el botón manda el mensaje genérico de la página y nunca el estimado anterior.
        vacio = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
        self.assertEqual(vacio, datos.con_firma(datos.MENSAJES["general"]))
        self.assertTrue(caja.locator('[data-vt-o="cta"]').get_attribute("href").startswith(
            f"https://wa.me/{datos.TELEFONO_WA}?text="))
        self.assertEqual(caja.locator(".vt-medidor__res").get_attribute("role"), "status")

    def test_medidor_empieza_vacio_y_manda_el_mensaje_generico(self):
        for ruta, mensaje in (("/", datos.MENSAJES["general"]), ("/pasto-en-rollo-tampico/", datos.MENSAJES["pasto-natural"])):
            page = self.pagina()
            page.goto(self.base + ruta, wait_until="load")
            caja = page.locator("[data-vt-medidor]")
            with self.subTest(ruta=ruta):
                self.assertEqual(caja.locator('[data-vt-campo="largo"]').input_value(), "")
                self.assertEqual(caja.locator('[data-vt-campo="largo"]').get_attribute("placeholder"), "8")
                self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "—")
                href = caja.locator('[data-vt-o="cta"]').get_attribute("href")
                self.assertEqual(unquote(href.split("text=", 1)[1]), datos.con_firma(mensaje))

    def test_barra_movil_se_esconde_con_el_medidor_a_la_vista(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/", wait_until="load")
        page.locator("[data-vt-medidor] .vt-medidor__res").scroll_into_view_if_needed()
        page.wait_for_function("() => document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
        page.locator("#vt-h-precios").scroll_into_view_if_needed()
        page.wait_for_function("() => !document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")

    def test_clic_en_el_medidor_manda_generate_lead(self):
        page = self.pagina()
        page.add_init_script("window.open = () => null;")
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        page.evaluate("() => document.querySelector('[data-vt-o=\"cta\"]').addEventListener('click', (e) => e.preventDefault())")
        page.click('[data-vt-o="cta"]')
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "servicio-pasto:medidor",
                                                  "service": "pasto-natural"}], eventos)

    def test_simulador_de_pasto_en_rollo_funciona(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        self.assertEqual(page.locator("[data-sim-list] .sim-plan").count(), 5)
        self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))

    def test_cada_plan_manda_su_mensaje_y_su_generate_lead(self):
        """Etapa 2c (auditoría 02): el plan elegido viaja al chat y a GA4 con su propio cta_id."""
        casos = (("/diseno-jardines-tampico/", "servicio-diseno", 2, "Plan Terra Completo ($6,500)"),
                 ("/mantenimiento-jardines-tampico/", "servicio-mantenimiento", 2, "Residencial premium"),
                 ("/sistema-riego-tampico/", "servicio-riego", 3, "campo deportivo"))
        for ruta, tipo, n, frase in casos:
            page = self.pagina()
            page.add_init_script("window.open = () => null;")
            page.goto(self.base + ruta, wait_until="load")
            boton = page.locator(f'[data-cta="{tipo}:opcion-{n}"]')
            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
            boton.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            with self.subTest(ruta=ruta):
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": f"{tipo}:opcion-{n}",
                                                          "service": "jardin"}], eventos)
                texto = unquote(boton.get_attribute("href").split("text=", 1)[1])
                self.assertIn(frase, texto)
                self.assertTrue(texto.endswith(datos.FIRMA))

    def test_simulador_de_diseno_y_riego_funciona(self):
        for ruta, monto in (("/diseno-jardines-tampico/", "6500"), ("/sistema-riego-tampico/", "18000")):
            page = self.pagina()
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertEqual(page.input_value("[data-sim-monto]"), monto)
                self.assertGreaterEqual(page.locator("[data-sim-list] .sim-plan").count(), 4)
                self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))

    def test_cls_bajo_0_1_en_movil(self):
        page = self.pagina(375, 812)
        for ruta in CON_PLANTILLA:
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertLess(page.evaluate(CLS), 0.1)


if __name__ == "__main__":
    unittest.main()
