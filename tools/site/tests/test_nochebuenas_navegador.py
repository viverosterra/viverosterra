"""Página de Nochebuenas en Chromium: casos del dueño, controles, mensaje de WhatsApp, registro que falla, fechas, barra fija,
desbordes y axe. Todo lo que no sea localhost se bloquea. Se salta sin Playwright."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
import datos  # noqa: E402
import servidor  # noqa: E402
import shell  # noqa: E402
from contenido import nochebuenas as contenido  # noqa: E402
from plantillas import nochebuenas as plantilla  # noqa: E402
from test_plantillas_navegador import AXE, AXE_PAGINA, SALIDOS_DEL_MAIN, TEXTO_FUERA_DE_CELDA  # noqa: E402

try:
    from playwright.sync_api import expect, sync_playwright
except ImportError:
    sync_playwright = None

RUTA = datos.NOCHEBUENAS["ruta"] + "/"
FUERA_DE_PREVENTA = "2026-12-01T18:00:00Z"
EN_PREVENTA = "2026-11-10T18:00:00Z"
ENDPOINT = "https://script.google.com/macros/s/prueba/exec"
RELOJ = """(() => { const R = Date; const fijo = new R('%s').getTime();
  class F extends R { constructor(...a) { if (a.length) super(...a); else super(fijo); } static now() { return fijo; } }
  window.Date = F; })();"""
BEACON_QUE_FALLA = "window.__beacons = 0; navigator.sendBeacon = () => { window.__beacons++; throw new Error('sin red'); };"
CTA = 'a[data-cta="nochebuenas:cotizador"]'


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado")
class NochebuenasNavegadorTest(unittest.TestCase):
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

    def contexto(self, ancho=360, alto=780, hoy=FUERA_DE_PREVENTA):
        ctx = self.navegador.new_context(viewport={"width": ancho, "height": alto})
        self.addCleanup(ctx.close)
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(self.base) else r.abort())
        ctx.add_init_script(RELOJ % hoy)
        return ctx

    def abrir(self, ctx):
        page = ctx.new_page()
        page.goto(self.base + RUTA, wait_until="load")
        page.wait_for_function(f"() => document.querySelector('{CTA}').href.includes('Hola')")
        return page

    def con_html(self, ctx, viejo, nuevo):
        """La página tal cual, con un reemplazo en el HTML (endpoint de prueba o modo), sin tocar datos.py."""
        def cambiar(ruta):
            r = ruta.fetch()
            self.assertIn(viejo, r.text())
            ruta.fulfill(response=r, body=r.text().replace(viejo, nuevo))
        ctx.route(self.base + RUTA, cambiar)

    def servir(self, ctx, documento):
        ctx.route(self.base + RUTA, lambda ruta: ruta.fulfill(body=documento, content_type="text/html; charset=utf-8"))

    def poner(self, page, fila, clave, cantidad, variedad="Roja"):
        linea = page.locator("[data-nb-linea]").nth(fila)
        linea.locator('[data-nb-campo="producto"]').select_option(clave)
        linea.locator('[data-nb-campo="variedad"]').select_option(variedad)
        linea.locator('[data-nb-campo="cantidad"]').fill(str(cantidad))

    def salida(self, page, nombre):
        return page.locator(f'[data-nb-cotizador] [data-nb-o="{nombre}"]').text_content()

    def test_diez_de_seis_con_nudge(self):
        page = self.abrir(self.contexto())
        self.poner(page, 0, "6", 10)
        self.assertEqual(self.salida(page, "total"), "$1,390")
        self.assertEqual(self.salida(page, "nudge"), "Te faltan 2 piezas para precio Mayoreo: por $38 más te llevas 12 y ahorras $240")

    def test_doce_de_seis(self):
        page = self.abrir(self.contexto())
        self.poner(page, 0, "6", 12)
        self.assertEqual(self.salida(page, "total"), "$1,428")
        # Entrega B de experiencia: el ticket dice el precio aplicado con su rango de piezas.
        self.assertEqual(self.salida(page, "escalon"), "Mayoreo (12 a 49 piezas)")
        self.assertFalse(page.locator('[data-nb-o="nudge"]').is_visible())

    def test_pedido_mixto_y_mensaje_completo(self):
        page = self.abrir(self.contexto())
        self.poner(page, 0, "6", 16)
        page.locator('[data-nb-accion="agregar"]').click()
        self.poner(page, 1, "7", 4, "Jaspeada")
        page.locator('[data-nb-accion="agregar"]').click()
        self.poner(page, 2, "colgante", 6, "Rosa")
        page.locator("[data-nb-extras] summary").click()
        page.locator('[data-nb-campo="zona"]').select_option("Madero")
        page.locator('[data-nb-campo="factura"]').check()
        self.assertEqual(self.salida(page, "total"), "$4,254")
        self.assertEqual(self.salida(page, "entrega"), "Entrega incluida")
        href = unquote(page.locator(CTA).get_attribute("href"))
        for parte in ('16 × Maceta 6" Roja', '4 × Maceta 7" Jaspeada', "6 × Colgante Rosa",
                      "Total: 26 piezas · Total estimado: $4,254", "Entrega: Madero · Requiero factura"):
            with self.subTest(parte=parte):
                self.assertIn(parte, href)

    def test_menos_mas_y_quitar_linea(self):
        page = self.abrir(self.contexto())
        fila = page.locator("[data-nb-linea]").first
        self.assertFalse(fila.locator('[data-nb-accion="quitar"]').is_visible())
        fila.locator('[data-nb-accion="mas"]').click()
        self.assertEqual(fila.locator('[data-nb-campo="cantidad"]').input_value(), "2")
        self.assertEqual(self.salida(page, "total"), "$278")
        fila.locator('[data-nb-accion="menos"]').click()
        self.assertEqual(self.salida(page, "total"), "$139")
        page.locator('[data-nb-accion="agregar"]').click()
        self.assertEqual(page.locator("[data-nb-linea]").count(), 2)
        self.assertEqual(self.salida(page, "total"), "$278")
        page.locator("[data-nb-linea]").nth(1).locator('[data-nb-accion="quitar"]').click()
        self.assertEqual(page.locator("[data-nb-linea]").count(), 1)

    def test_sin_piezas_no_se_envia(self):
        page = self.abrir(self.contexto())
        page.locator('[data-nb-campo="cantidad"]').fill("0")
        cta = page.locator(CTA)
        self.assertEqual(cta.get_attribute("aria-disabled"), "true")
        self.assertEqual(cta.get_attribute("aria-describedby"), "nb-aviso-vacio")
        self.assertEqual(page.locator("#nb-aviso-vacio").text_content(), "Agrega al menos 1 pieza")
        self.assertTrue(page.locator("#nb-aviso-vacio").is_visible())
        cta.click(force=True)
        self.assertEqual(len(page.context.pages), 1)

    def test_con_registro_que_falla_whatsapp_abre_igual(self):
        ctx = self.contexto()
        ctx.add_init_script(BEACON_QUE_FALLA)
        self.con_html(ctx, '"sheets_endpoint":""', f'"sheets_endpoint":"{ENDPOINT}"')
        pedidas = []
        ctx.on("request", lambda r: pedidas.append(r.url) if "wa.me" in r.url else None)
        page = self.abrir(ctx)
        self.poner(page, 0, "6", 12)
        with ctx.expect_page() as nueva:
            page.locator(CTA).click()
        nueva.value.wait_for_load_state("domcontentloaded")
        self.assertEqual(page.evaluate("window.__beacons"), 1)
        self.assertEqual(len(pedidas), 1)
        with ctx.expect_page() as segunda:
            page.locator(CTA).click()
        segunda.value.wait_for_load_state("domcontentloaded")
        self.assertEqual(page.evaluate("window.__beacons"), 1)  # clic idéntico en menos de 10 s: no se registra otra vez
        self.assertEqual(len(pedidas), 2)  # WhatsApp sí abre
        self.assertIn("Total estimado: $1,428", unquote(pedidas[0]))
        self.assertIn(datos.FIRMA, unquote(pedidas[0]))

    def test_fechas_vencidas_se_ocultan(self):
        page = self.abrir(self.contexto(hoy=FUERA_DE_PREVENTA))
        for fecha in page.locator('.vt-nb-fechas [data-nb-hasta="2026-11-30"]').all():
            self.assertFalse(fecha.is_visible())
        page = self.abrir(self.contexto(hoy=EN_PREVENTA))
        for fecha in page.locator('.vt-nb-fechas [data-nb-hasta="2026-11-30"]').all():
            self.assertTrue(fecha.is_visible())

    def test_preventa_aplica_y_se_explica(self):
        page = self.abrir(self.contexto(hoy=EN_PREVENTA))
        self.poner(page, 0, "6", 12)
        self.assertEqual(self.salida(page, "total"), "$1,357")
        self.assertEqual(self.salida(page, "preventa"), "Precio preventa: apartando con 50% de anticipo")
        self.assertIn("Precio preventa", unquote(page.locator(CTA).get_attribute("href")))

    def test_modo_preventa_pide_apartar(self):
        ctx = self.contexto()
        self.con_html(ctx, "data-nb-cotizador>", 'data-nb-cotizador data-nb-modo="preventa">')
        self.assertIn("Quiero apartar", unquote(self.abrir(ctx).locator(CTA).get_attribute("href")))

    def ir_a(self, page, selector):
        """Lleva el elemento a media pantalla: scroll_into_view no mueve la página si ya se ve."""
        page.evaluate("(s) => document.querySelector(s).scrollIntoView({block: 'center', behavior: 'instant'})", selector)

    def test_barra_oculta_con_el_cta_del_hero_y_sin_usar_dentro_del_cotizador(self):
        page = self.abrir(self.contexto())
        barra = page.locator("[data-nb-bar]")
        barra.wait_for(state="hidden")
        self.ir_a(page, "#vt-h-para")
        barra.wait_for(state="visible")
        self.assertEqual(barra.locator("a").text_content(), "Cotizar mi pedido")
        self.ir_a(page, "#vt-h-cotizador")
        barra.wait_for(state="hidden")

    def test_barra_tras_usar_el_cotizador(self):
        page = self.abrir(self.contexto(360, 400))  # pantalla baja: se ve la línea y todavía no el ticket
        barra = page.locator("[data-nb-bar]")
        self.poner(page, 0, "6", 12)
        page.locator('[data-nb-campo="cantidad"]').blur()
        self.ir_a(page, "[data-nb-linea]")
        barra.wait_for(state="visible")
        enlace = barra.locator("a")
        expect(enlace).to_have_text("12 piezas · $1,428 · Ver total")  # el observador puede llegar después de mostrarse
        expect(enlace).to_have_attribute("href", "#nb-ticket")
        page.locator('[data-nb-campo="cantidad"]').focus()
        barra.wait_for(state="hidden")
        page.locator('[data-nb-campo="cantidad"]').blur()
        barra.wait_for(state="visible")
        self.ir_a(page, ".vt-nb-enviar")
        barra.wait_for(state="hidden")
        self.ir_a(page, "#vt-h-galeria")
        barra.wait_for(state="visible")
        # Entrega B de experiencia: fuera del cotizador y con pedido, la barra manda el pedido escrito por WhatsApp.
        expect(enlace).to_have_text("Enviar mi pedido · $1,428")
        expect(enlace).to_have_attribute("href", re.compile(r"^https://wa\.me/"))

    def test_enfocar_piezas_selecciona_todo(self):
        page = self.abrir(self.contexto())
        page.locator('[data-nb-campo="cantidad"]').click()
        page.keyboard.type("7")
        self.assertEqual(page.locator('[data-nb-campo="cantidad"]').input_value(), "7")

    def test_maximo_por_linea(self):
        page = self.abrir(self.contexto())
        self.assertFalse(page.locator('[data-nb-o="maximo"]').is_visible())
        self.poner(page, 0, "6", 20000)
        page.locator('[data-nb-campo="cantidad"]').blur()
        self.assertEqual(page.locator('[data-nb-campo="cantidad"]').input_value(), "9999")
        self.assertEqual(self.salida(page, "maximo"), "Máximo 9,999 por línea; para más, escríbenos")

    def test_precio_unitario_bajo_el_subtotal(self):
        page = self.abrir(self.contexto())
        self.poner(page, 0, "6", 12)
        self.assertEqual(page.locator('[data-nb-linea] [data-nb-o="unitario"]').text_content(), "12 × $119")

    def test_boton_del_nudge_sube_al_corte(self):
        page = self.abrir(self.contexto())
        self.poner(page, 0, "6", 10)
        subir = page.locator('[data-nb-accion="subir"]')
        self.assertEqual(subir.text_content(), "Subir a 12 piezas")
        subir.click()
        self.assertEqual(page.locator('[data-nb-campo="cantidad"]').input_value(), "12")
        self.assertEqual(self.salida(page, "total"), "$1,428")
        self.assertFalse(subir.is_visible())

    def test_etiquetas_distintas_por_linea(self):
        page = self.abrir(self.contexto())
        page.locator('[data-nb-accion="agregar"]').click()
        segunda = page.locator("[data-nb-linea]").nth(1)
        self.assertEqual(segunda.locator('[data-nb-campo="producto"]').get_attribute("aria-label"), "Tamaño, línea 2")
        self.assertEqual(segunda.locator('[data-nb-accion="mas"]').get_attribute("aria-label"), "Una pieza más, línea 2")

    def test_tope_de_doce_lineas(self):
        page = self.abrir(self.contexto())
        agregar = page.locator('[data-nb-accion="agregar"]')
        for _ in range(11):
            agregar.click()
        self.assertEqual(page.locator("[data-nb-linea]").count(), 12)
        self.assertTrue(agregar.is_disabled())
        self.assertIn("Máximo 12 líneas", self.salida(page, "tope"))

    def test_fecha_minima_es_hoy(self):
        page = self.abrir(self.contexto())
        self.assertEqual(page.locator('[data-nb-campo="fecha"]').get_attribute("min"), "2026-12-01")

    def test_opcionales_cerrados_en_movil_y_abiertos_en_escritorio(self):
        estado = "document.querySelector('[data-nb-extras]').open"
        self.assertFalse(self.abrir(self.contexto(360, 780)).evaluate(estado))
        self.assertTrue(self.abrir(self.contexto(1440, 900)).evaluate(estado))

    def test_desglose_de_preventa_y_ahorro_sin_descuento(self):
        page = self.abrir(self.contexto(hoy=EN_PREVENTA))
        self.poner(page, 0, "6", 12)
        self.assertEqual(self.salida(page, "desglose"), "Subtotal $1,428 · Preventa −$71")
        self.assertEqual(self.salida(page, "ahorro"), "Ahorras $240 vs. menudeo")

    def test_lista_de_fechas_vencidas_no_deja_hueco(self):
        page = self.abrir(self.contexto(hoy=FUERA_DE_PREVENTA))
        self.assertFalse(page.locator(".vt-nb-fechas").is_visible())

    def test_barra_no_tapa_el_pie_y_no_existe_en_escritorio(self):
        page = self.abrir(self.contexto())
        page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'instant'})")
        barra = page.locator("[data-nb-bar]")
        barra.wait_for(state="visible")
        self.assertLessEqual(page.locator(".vt-foot__legal").bounding_box()["y"] + page.locator(".vt-foot__legal").bounding_box()["height"],
                             barra.bounding_box()["y"])
        self.assertFalse(self.abrir(self.contexto(1440, 900)).locator("[data-nb-bar]").is_visible())

    def test_cta_en_el_primer_pantallazo_movil(self):
        page = self.abrir(self.contexto(375, 812))
        page.locator("[data-nb-bar]").wait_for(state="hidden")
        tope = 812
        for selector in (".vt-portada .vt-etiqueta__precio", '.vt-portada a[href="#cotizador"]'):
            caja = page.locator(selector).bounding_box()
            with self.subTest(selector=selector):
                self.assertLessEqual(caja["y"] + caja["height"], tope)

    def test_sin_desborde(self):
        for ancho in (320, 360, 768, 1024, 1440):
            page = self.abrir(self.contexto(ancho, 800))
            page.locator('[data-nb-accion="agregar"]').click()
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, "main *"), [])
                self.assertEqual(page.evaluate(TEXTO_FUERA_DE_CELDA), [])

    def test_objetivos_tactiles(self):
        page = self.abrir(self.contexto())
        page.locator('[data-nb-accion="agregar"]').click()
        cajas = page.evaluate("""() => Array.from(document.querySelectorAll(
          '[data-nb-cotizador] :is(button,select,input:not([type=checkbox]),a)')).filter((e) => e.offsetParent)
          .map((e) => Math.min(e.getBoundingClientRect().width, e.getBoundingClientRect().height))""")
        self.assertGreaterEqual(min(cajas), 44)

    def test_los_otros_modos_sin_desborde_ni_violaciones(self):
        script = AXE.read_text(encoding="utf-8")
        for modo in ("preventa", "postemporada"):
            documento = shell.aplicar(plantilla.render(contenido.CONTENIDO, modo=modo), datos.NOCHEBUENAS["ruta"], activos.urls())
            for ancho in (360, 1440):
                ctx = self.contexto(ancho, 900)
                self.servir(ctx, documento)
                page = ctx.new_page()
                page.goto(self.base + RUTA, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(modo=modo, ancho=ancho):
                    self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, "main *"), [])
                    self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_axe_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.abrir(self.contexto(ancho, 900))
            self.poner(page, 0, "6", 10)
            page.add_script_tag(content=script)
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate(AXE_PAGINA), [])


if __name__ == "__main__":
    unittest.main()
