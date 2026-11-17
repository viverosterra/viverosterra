"""Panel de preguntas rápidas antes de WhatsApp en Chromium (spec del primer mensaje de WhatsApp, 2026-11-16).

Nunca se abre WhatsApp: todo lo que no es el servidor local se aborta y el enlace final solo se lee. Se salta sin
Playwright (python3 -m pip install playwright==1.48.0)."""
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

ABRIR = ".vt-wa-panel__abrir"
VISTA = ".vt-wa-panel__vista"


def texto_de(page, selector):
    return unquote(page.locator(selector).get_attribute("href").split("text=", 1)[1])


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class PreguntasNavegadorTest(unittest.TestCase):
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

    def pagina(self, ancho=1440, alto=900, contexto=None):
        if contexto is None:
            contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto})
            self.addCleanup(contexto.close)
            base = self.base
            contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page = contexto.new_page()
        errores = []
        page.on("pageerror", lambda e: errores.append(str(e)))
        self.addCleanup(lambda: self.assertEqual(errores, []))
        # Si algo abriera una pestaña nueva (WhatsApp), la prueba falla.
        page.context.on("page", lambda p: errores.append(f"se abrió otra pestaña: {p.url}"))
        return page

    def abrir_panel(self, page, ruta, cta):
        page.goto(self.base + ruta, wait_until="load")
        page.locator(f'a[data-cta="{cta}"][href^="https://wa.me/"]').first.click()
        page.wait_for_selector("dialog.vt-wa-panel[open]")

    def toca(self, page, clave, valor):
        page.locator(f'.vt-wa-panel [data-q="{clave}"][data-v="{valor}"]').click()

    def test_hub_arma_el_mensaje_con_modelo_metros_y_estado(self):
        page = self.pagina()
        self.abrir_panel(page, "/pasto-sintetico/", "tienda:hero")
        self.assertEqual(page.locator(".vt-wa-panel legend").all_inner_texts(), ["¿Qué modelo?", "¿Cuántos m²?", "¿A dónde?"])
        self.toca(page, "modelo", "toscana-28")
        self.toca(page, "m2", "25-50")
        self.toca(page, "destino", "envio")
        page.select_option(".vt-wa-panel select", "Jalisco")
        esperado = "Hola, quiero cotizar pasto sintético Toscana 28, entre 25 y 50 m², con envío a Jalisco."
        self.assertEqual(page.locator(VISTA).inner_text(), esperado)
        self.assertEqual(texto_de(page, ABRIR), esperado + "\n\n" + datos.FIRMA)
        self.assertEqual(page.locator('.vt-wa-panel [data-v="toscana-28"]').get_attribute("aria-pressed"), "true")
        self.assertEqual(texto_de(page, ".vt-wa-panel__corto"),
                         "Hola, tengo una pregunta sobre pasto sintético.\n\n" + datos.FIRMA)

    def test_sin_contestar_abre_con_el_mensaje_corto_de_cotizar(self):
        page = self.pagina()
        self.abrir_panel(page, "/pasto-sintetico/", "tienda:hero")
        self.assertEqual(texto_de(page, ABRIR), "Hola, quiero cotizar pasto sintético.\n\n" + datos.FIRMA)
        self.toca(page, "m2", "<25")
        self.toca(page, "m2", "<25")  # un segundo toque quita la opción
        self.assertEqual(page.locator(VISTA).inner_text(), "Hola, quiero cotizar pasto sintético.")

    def test_ficha_no_pregunta_el_modelo_y_ciudad_no_pregunta_el_destino(self):
        page = self.pagina()
        self.abrir_panel(page, "/pasto-sintetico/toscana-28/", "tienda:hero")
        self.assertNotIn("¿Qué modelo?", page.locator(".vt-wa-panel legend").all_inner_texts())
        self.assertTrue(page.locator(VISTA).inner_text().startswith("Hola, quiero cotizar pasto sintético Toscana 28"))
        page.keyboard.press("Escape")
        self.abrir_panel(page, "/pasto-sintetico/envio/monterrey/", "ciudad:hero")
        self.assertNotIn("¿A dónde?", page.locator(".vt-wa-panel legend").all_inner_texts())
        # La ficha que acaba de ver queda propuesta (memoria de la visita) y se puede quitar con otro toque.
        self.assertEqual(page.locator(VISTA).inner_text(),
                         "Hola, quiero cotizar pasto sintético Toscana 28, con envío a Monterrey (Nuevo León).")
        self.toca(page, "modelo", "toscana-28")
        self.assertEqual(page.locator(VISTA).inner_text(),
                         "Hola, quiero cotizar pasto sintético, con envío a Monterrey (Nuevo León).")

    def test_recuerda_la_ficha_y_los_metros_de_la_calculadora(self):
        contexto = self.navegador.new_context(viewport={"width": 1440, "height": 900})
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page = self.pagina(contexto=contexto)
        page.goto(self.base + "/pasto-sintetico/cuantos-rollos/", wait_until="load")
        page.fill("#r-largo", "7")
        page.fill("#r-ancho", "5")
        page.goto(self.base + "/pasto-sintetico/irlanda-25/", wait_until="load")
        self.abrir_panel(page, "/pasto-sintetico/envio/cdmx/", "ciudad:hero")
        self.assertEqual(page.locator('.vt-wa-panel [data-v="exacto"]').inner_text(), "Unos 40 m²")
        self.assertEqual(page.locator('.vt-wa-panel [data-v="exacto"]').get_attribute("aria-pressed"), "true")
        self.assertEqual(page.locator('.vt-wa-panel [data-v="irlanda-25"]').get_attribute("aria-pressed"), "true")
        self.assertEqual(page.locator(VISTA).inner_text(),
                         "Hola, quiero cotizar pasto sintético Irlanda 25, unos 40 m², con envío a CDMX.\n"
                         "Folio web: I25-40-CDMX")

    def test_esc_cierra_y_el_foco_vuelve(self):
        page = self.pagina()
        self.abrir_panel(page, "/pasto-sintetico-tampico/", "servicio-sintetico:hero")
        self.assertTrue(page.locator(".vt-wa-panel__cerrar").is_visible())
        page.keyboard.press("Escape")
        self.assertEqual(page.locator("dialog.vt-wa-panel[open]").count(), 0)
        self.assertEqual(page.evaluate("document.activeElement.getAttribute('data-cta')"), "servicio-sintetico:hero")

    def test_el_encabezado_y_el_pie_no_abren_el_panel(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/", wait_until="load")
        # Se evita la navegación: solo importa que el panel no se abra.
        page.evaluate("document.addEventListener('click', (e) => e.preventDefault())")
        page.locator('footer a[href^="https://wa.me/"]').first.click()
        self.assertEqual(page.locator("dialog.vt-wa-panel[open]").count(), 0)

    def test_medicion_del_panel(self):
        page = self.pagina()
        self.abrir_panel(page, "/blog/cuanto-cuesta-pasto-sintetico-mexico/", "blog:hero")
        page.evaluate("document.querySelector('.vt-wa-panel__abrir').addEventListener('click', (e) => e.preventDefault())")
        self.toca(page, "m2", "50-100")
        page.locator(ABRIR).click()
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer || []).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        # Un solo generate_lead, con el cta_id del botón de siempre y cómo se abrió el WhatsApp.
        self.assertEqual([e for e in eventos if e[1] == "generate_lead"],
                         [["event", "generate_lead", {"method": "whatsapp", "cta_id": "blog:hero",
                                                      "service": "pasto-sintetico", "preguntas": "respondidas"}]])

    def test_no_desborda_en_cuatro_anchos(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho, 800)
            self.abrir_panel(page, "/pasto-sintetico/", "tienda:hero")
            self.toca(page, "destino", "envio")
            sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            caja = page.locator(".vt-wa-panel__caja").bounding_box()
            with self.subTest(ancho=ancho):
                self.assertLessEqual(sobra, 1)
                self.assertLessEqual(caja["x"] + caja["width"], ancho + 0.5)
                self.assertGreaterEqual(caja["x"], -0.5)


    # Entrega 2: servicios de Tampico.
    def test_mantenimiento_arma_tamano_frecuencia_y_lugar(self):
        page = self.pagina(375, 812)
        self.abrir_panel(page, "/mantenimiento-jardines-tampico/", "servicio-mantenimiento:hero")
        self.assertEqual(page.locator(".vt-wa-panel legend").all_inner_texts(),
                         ["¿Tamaño del jardín?", "¿Cada cuándo?", "¿Dónde?"])
        self.toca(page, "tamano", "mediano")
        self.toca(page, "frecuencia", "mensual")
        self.toca(page, "lugar", "tampico")
        esperado = "Hola, quiero cotizar mantenimiento de jardín de 50 a 200 m², cada mes en Tampico."
        self.assertEqual(page.locator(VISTA).inner_text(), esperado)
        self.assertEqual(texto_de(page, ABRIR), esperado + "\n\n" + datos.FIRMA)
        self.assertEqual(texto_de(page, ".vt-wa-panel__corto"),
                         "Hola, tengo una pregunta sobre mantenimiento de jardín.\n\n" + datos.FIRMA)

    def test_poda_con_su_cola(self):
        page = self.pagina()
        self.abrir_panel(page, "/poda-arboles-tampico/", "servicio-poda:hero")
        self.toca(page, "que", "arbol")
        self.toca(page, "servicio", "derribo")
        self.assertEqual(page.locator(VISTA).inner_text(),
                         "Hola, quiero cotizar el derribo de un árbol.\nLes mando fotos y la ubicación.")

    def test_los_botones_de_cada_plan_no_abren_el_panel(self):
        page = self.pagina()
        page.goto(self.base + "/mantenimiento-jardines-tampico/", wait_until="load")
        page.evaluate("document.addEventListener('click', (e) => e.preventDefault())")
        page.locator('a[data-cta="servicio-mantenimiento:opcion-1"]').first.click()
        self.assertEqual(page.locator("dialog.vt-wa-panel[open]").count(), 0)

    def test_pasto_en_rollo_no_trae_lo_recordado_de_la_tienda(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/cuantos-rollos/", wait_until="load")
        page.fill("#r-largo", "7")
        page.fill("#r-ancho", "5")
        self.abrir_panel(page, "/pasto-en-rollo-tampico/", "servicio-pasto:hero")
        self.assertEqual(page.locator('.vt-wa-panel [aria-pressed="true"]').count(), 0)
        self.assertEqual(page.locator(VISTA).inner_text(), "Hola, quiero cotizar pasto San Agustín en rollo.")


if __name__ == "__main__":
    unittest.main()
