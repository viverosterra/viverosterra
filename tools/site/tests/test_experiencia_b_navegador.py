"""Entrega B de experiencia (CTA y recorrido) en Chromium: la barra fija y el encabezado toman el resultado de cada
calculadora y vuelven al genérico al borrarlo; generate_lead sale una vez por clic con su cta_id; ningún tramo de más de 6
pantallas del celular sin un CTA de WhatsApp en línea en tienda, plantas, palmas, catálogo y mantenimiento; avisos de
entrada inválida sin borrar lo escrito; simulador sin monto fantasma; borrador del cuestionario en sessionStorage (sin
enviar nada); menú con vivero y blog sin desbordar; el 404 encuentra "nochebuena". Todo el tráfico fuera de 127.0.0.1 se
bloquea, con movimiento reducido, y ningún clic llega a wa.me ni a tel: (se impide la navegación antes de pulsar). Se
saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
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

BARRA = "[data-vt-bar] .vt-bar__go"
CABEZA = ".vt-head__cta"
# Ningún clic real a WhatsApp ni a teléfono: los enlaces se quedan en la página y window.open no abre nada.
SIN_SALIR = """() => {
  window.open = () => null;
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (a && /^(https:\\/\\/wa\\.me|tel:)/.test(a.getAttribute('href'))) e.preventDefault();
  });
}"""
EVENTOS = "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event' && a[1] === 'generate_lead')"
# Mayor tramo (en pantallas de 812 px) sin un enlace de WhatsApp visible en el <main>, contando desde arriba de la
# página hasta el final del <main>; fuera quedan encabezado, menú, pie, barras fijas, diálogos y lo oculto.
TRAMO = """() => {
  const H = 812;
  const main = document.querySelector('main');
  const fin = main.getBoundingClientRect().bottom + scrollY;
  const fuera = (a) => a.closest('.vt-head, .vt-foot, [data-vt-bar], #buybar, .vt-mmenu, dialog, [hidden]');
  const ys = Array.from(main.querySelectorAll('a[href*="wa.me"]')).filter((a) => !fuera(a)).filter((a) => {
    const c = a.getBoundingClientRect(); return c.width > 0 && c.height > 0 && getComputedStyle(a).visibility !== 'hidden';
  }).map((a) => a.getBoundingClientRect().top + scrollY).sort((x, y) => x - y);
  const puntos = [0, ...ys, fin];
  let mayor = 0;
  for (let i = 1; i < puntos.length; i++) mayor = Math.max(mayor, puntos[i] - puntos[i - 1]);
  return mayor / H;
}"""
CARGAR = """async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) { scrollTo(0, y);
  await new Promise((r) => setTimeout(r, 30)); } scrollTo(0, 0); }"""


def texto(href):
    return unquote(href.split("text=", 1)[1]) if "text=" in href else ""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class ExperienciaBNavegadorTest(unittest.TestCase):
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

    def pagina(self, ruta, ancho=375, alto=812):
        contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto}, reduced_motion="reduce")
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page = contexto.new_page()
        errores = []
        page.on("pageerror", lambda e: errores.append(str(e)))
        self.addCleanup(lambda: self.assertEqual(errores, []))
        page.goto(self.base + ruta, wait_until="load")
        page.evaluate(SIN_SALIR)
        return page

    def barra_y_cabeza(self, page):
        go, cabeza = page.locator(BARRA), page.locator(CABEZA)
        return {"barra": go.text_content().strip() if go.count() else None, "barra_href": go.get_attribute("href") if go.count() else None,
                "cabeza": cabeza.locator(".vt-head__cta-corto").text_content(), "cabeza_largo": cabeza.locator(".vt-head__cta-largo").text_content(),
                "cabeza_href": cabeza.get_attribute("href")}

    def clic_unico(self, page, selector, cta):
        """Un clic en la barra (o el encabezado) con préstamo: un solo generate_lead, con el cta_id de siempre."""
        page.evaluate("() => { window.dataLayer.length = 0; }")
        page.locator(selector).evaluate("(a) => a.click()")
        self.assertEqual([e[2]["cta_id"] for e in page.evaluate(EVENTOS)], [cta])

    def prestada(self, page, boton, texto_barra, tipo, con_barra=True):
        """Con resultado válido: barra y encabezado llevan el enlace del botón de la calculadora; el encabezado del celular
        dice "Enviar" y el de escritorio, el texto de la barra."""
        estado = self.barra_y_cabeza(page)
        href = page.locator(boton).get_attribute("href")
        if con_barra:
            self.assertEqual(estado["barra"], texto_barra)
            self.assertEqual(estado["barra_href"], href)
        self.assertEqual(estado["cabeza_href"], href)
        self.assertEqual(estado["cabeza"], "Enviar")
        self.assertEqual(estado["cabeza_largo"], texto_barra)
        self.clic_unico(page, CABEZA, f"{tipo}:header")
        if con_barra:
            self.clic_unico(page, BARRA, f"{tipo}:barra")

    def generica(self, page, original):
        self.assertEqual(self.barra_y_cabeza(page), original)

    # ---------- 1. la barra fija toma el resultado de cada calculadora ----------
    def test_medidor_de_pasto_en_rollo_presta_su_medida_y_avisa_entradas_invalidas(self):
        page = self.pagina("/pasto-en-rollo-tampico/")
        original = self.barra_y_cabeza(page)
        caja = page.locator("[data-vt-medidor]")
        caja.locator('[data-vt-campo="largo"]').fill("10")
        caja.locator('[data-vt-campo="ancho"]').fill("5")
        self.assertIn("Medidas: 10.00 × 5.00 m = 50 m²", texto(page.locator(BARRA).get_attribute("href")))
        self.assertEqual(caja.locator('[data-vt-o="cta-texto"]').text_content(), "Enviar mi medida por WhatsApp")
        self.prestada(page, '[data-vt-medidor] [data-vt-o="cta"]', "Enviar mi medida", "servicio-pasto")
        error = caja.locator('[data-vt-o="error"]')
        for malo in ("0", "-4", "abc"):
            caja.locator('[data-vt-campo="ancho"]').fill(malo)
            with self.subTest(entrada=malo):
                self.assertTrue(error.is_visible())
                self.assertEqual(error.text_content(), "Escribe el largo y el ancho en metros, solo con números. Ejemplo: 8 y 6.")
                self.assertEqual(caja.locator('[data-vt-campo="ancho"]').input_value(), malo)  # no se borra lo escrito
                self.assertEqual(caja.locator('[data-vt-campo="ancho"]').get_attribute("aria-invalid"), "true")
                self.generica(page, original)
        caja.locator('[data-vt-campo="ancho"]').fill("")
        self.assertTrue(error.is_hidden())
        self.generica(page, original)

    def test_cotizador_de_mayoreo_y_armador_de_palmas_prestan_su_resultado(self):
        page = self.pagina("/mayoreo-pasto-tampico/")
        original = self.barra_y_cabeza(page)
        page.locator('[data-vt-volumen] [data-vt-campo="m2"]').fill("1200")
        self.assertIn("m² totales: 1,200 m²", texto(page.locator(BARRA).get_attribute("href")))
        self.prestada(page, '[data-vt-volumen] [data-vt-o="cta"]', "Enviar mi cálculo", "b2b")
        page.locator('[data-vt-volumen] [data-vt-campo="m2"]').fill("")
        self.generica(page, original)
        page = self.pagina("/palmas-mayoreo-proyectos/")
        original = self.barra_y_cabeza(page)
        page.locator('[data-vt-palmas] select').first.select_option("Palma real")
        page.locator('[data-vt-palmas] [data-vt-campo="cantidad"]').first.fill("40")
        self.assertIn("- 40 × Palma real", texto(page.locator(BARRA).get_attribute("href")))
        self.prestada(page, '[data-vt-palmas] [data-vt-o="cta"]', "Cotizar mis palmas", "b2b")
        page.locator('[data-vt-palmas] select').first.select_option("")
        self.generica(page, original)

    def test_las_cuatro_calculadoras_de_materiales_prestan_su_calculo_y_avisan(self):
        for ruta in ("/tierra-negra-vegetal-tampico/", "/tezontle-rojo-tampico/", "/marmol-blanco-tampico/",
                     "/piedra-bola-rio-tampico/"):
            with self.subTest(ruta=ruta):
                page = self.pagina(ruta)
                original = self.barra_y_cabeza(page)
                area = page.locator('[data-vt-material] [data-vt-campo="area"]')
                area.fill("30")
                self.assertEqual(page.locator('[data-vt-material] [data-vt-o="cta-texto"]').text_content(), "Enviar mi cálculo por WhatsApp")
                self.prestada(page, '[data-vt-material] [data-vt-o="cta"]', "Enviar mi cálculo", "material")
                area.fill("abc")
                self.assertTrue(page.locator('[data-vt-material] [data-vt-o="error"]').is_visible())
                self.assertEqual(area.input_value(), "abc")
                self.generica(page, original)
        tierra = self.pagina("/tierra-negra-vegetal-tampico/")
        tierra.locator('[data-vt-material] [data-vt-campo="area"]').fill("30")
        self.assertEqual(texto(tierra.locator(BARRA).get_attribute("href")),
                         "Hola, quiero cotizar tierra negra vegetal.\nÁrea: 30 m², capa de 8 cm = 2.4 m³ (cálculo de la web)\n"
                         "En costales o a granel: ___\nColonia de entrega: ___\n¿Me dan el total con entrega?")

    def test_simulador_sin_monto_fantasma_y_con_monto_presta_su_plan(self):
        page = self.pagina("/pasto-en-rollo-tampico/")
        original = self.barra_y_cabeza(page)
        wa = page.locator("[data-sim-wa]")
        mensaje = texto(wa.get_attribute("href"))
        self.assertNotIn("$", mensaje)
        self.assertIn("Colonia: ___", mensaje)
        self.assertIn("Metros aprox.: ___", mensaje)
        self.generica(page, original)
        page.locator("[data-sim-monto]").fill("18000")
        self.assertIn("Mi cotización es de $18,000.", texto(wa.get_attribute("href")))
        self.prestada(page, "[data-sim-wa]", "Enviar mi plan de pago", "servicio-pasto")

    def test_nochebuenas_la_barra_manda_el_pedido_sin_el_nombre_del_escalon(self):
        page = self.pagina("/post/nochebuenas-tampico-madero-mayoreo/")
        caja = page.locator("[data-nb-cotizador]")
        caja.locator('[data-nb-campo="cantidad"]').first.fill("12")
        caja.locator('[data-nb-campo="cantidad"]').first.dispatch_event("change")
        page.evaluate("() => document.activeElement && document.activeElement.blur()")
        page.evaluate("() => scrollTo(0, document.getElementById('cotizador').getBoundingClientRect().bottom + scrollY + 400)")
        barra = page.locator("[data-nb-bar] .vt-bar__go")
        page.wait_for_function("() => !document.querySelector('[data-nb-bar]').hidden && document.querySelector('[data-nb-bar] a').textContent.startsWith('Enviar')")
        self.assertTrue(barra.text_content().startswith("Enviar mi pedido · $"))
        mensaje = texto(barra.get_attribute("href"))
        self.assertIn("Total: 12 piezas · Total estimado:", mensaje)
        self.assertNotIn("Escal", mensaje)
        self.assertEqual(page.locator(CABEZA).get_attribute("href"), barra.get_attribute("href"))
        self.assertEqual(page.locator('[data-nb-o="escalon"]').text_content(), "Mayoreo (12 a 49 piezas)")
        self.clic_unico(page, "[data-nb-bar] .vt-bar__go", "nochebuenas:barra")

    def test_tienda_estado_cotizador_y_lista_viajan_a_la_barra_al_hero_y_al_encabezado(self):
        page = self.pagina("/pasto-sintetico/")
        page.evaluate("() => localStorage.removeItem('vt-cotizacion-v1')")
        page.reload(wait_until="load")
        page.evaluate(SIN_SALIR)
        page.locator("#hero-estado").select_option("Nuevo León")
        esperado = ("Hola, quiero cotizar pasto sintético con envío a Nuevo León.\nCiudad: ___\nMetros aprox.: ___\n"
                    "Modelo (si ya lo elegiste): ___")
        for selector in (CABEZA, '.vt-portada-hub [data-hero-cta] a[href*="wa.me"]', "#buybar a"):
            with self.subTest(selector=selector):
                self.assertEqual(texto(page.locator(selector).get_attribute("href")), esperado)
        # La barra de compra aparece al dejar el hero, también con la lista vacía.
        page.evaluate("() => scrollTo(0, document.getElementById('modelos').getBoundingClientRect().top + scrollY)")
        page.wait_for_function("() => document.getElementById('buybar').dataset.visible === 'true'")
        page.locator("#m2").fill("60")
        page.dispatch_event("#m2", "input")
        self.assertEqual(page.locator("#buybar a").text_content().strip(), "Enviar mi cotización")
        self.assertIn("Necesito 60 m².", texto(page.locator(CABEZA).get_attribute("href")))
        page.locator("#m2").fill("0")
        page.dispatch_event("#m2", "input")
        self.assertNotIn("Necesito 0 m²", texto(page.locator("#comprar [data-cta-wa]").get_attribute("href")))
        page.evaluate("() => localStorage.removeItem('vt-cotizacion-v1')")
        # Con modelos en la lista y sin usar el cotizador: la lista completa.
        otra = self.pagina("/pasto-sintetico/")
        otra.locator('.vt-catalogo [data-add="toscana-28"]').click()
        if otra.locator("#vt-agregar-n").count() and otra.locator("dialog[open]").count():
            otra.keyboard.press("Escape")
        self.assertEqual(otra.locator("#buybar a").text_content().strip(), "Cotizar mi lista")
        self.assertIn("• Toscana 28", texto(otra.locator(CABEZA).get_attribute("href")))
        self.assertEqual(otra.locator("#cot-titulo").text_content(), "Mi lista")
        self.assertEqual(otra.locator("#cta-add").text_content(), "Agregar a mi lista")
        otra.evaluate("() => localStorage.removeItem('vt-cotizacion-v1')")

    def test_ficha_cta_con_el_modelo_antes_de_la_pantalla_2_y_barra_de_compra_temprana(self):
        page = self.pagina("/pasto-sintetico/toscana-28/")
        page.evaluate("() => localStorage.removeItem('vt-cotizacion-v1')")
        page.reload(wait_until="load")
        page.evaluate(SIN_SALIR)
        hero = page.locator('.vt-ficha [data-hero-cta] a[href*="wa.me"]')
        self.assertIn("Cotizar Toscana 28", hero.inner_text())
        self.assertLess(hero.bounding_box()["y"], 812)
        self.assertIn("Toscana 28", texto(page.locator(CABEZA).get_attribute("href")))
        page.evaluate("() => scrollTo(0, document.querySelector('.vt-galeria').getBoundingClientRect().top + scrollY)")
        page.wait_for_function("() => document.getElementById('buybar').dataset.visible === 'true'")
        self.assertLess(page.evaluate("() => scrollY") / 812, 2)
        self.clic_unico(page, "#buybar a", "tienda:barra")

    def test_catalogo_la_barra_cotiza_la_lista_directo_y_con_lista_vacia_ofrece_plantas(self):
        page = self.pagina("/catalogo.html")
        page.evaluate("() => sessionStorage.removeItem('vt-catalogo-lista')")
        page.reload(wait_until="load")
        page.evaluate(SIN_SALIR)
        original = self.barra_y_cabeza(page)
        self.assertEqual(original["barra"], "Cotizar plantas")
        self.assertIn("Planta o plantas: ___", texto(original["barra_href"]))
        self.assertIn("Colonia de entrega: ___", texto(original["barra_href"]))
        self.assertTrue(page.locator("[data-vt-abrir-lista]").is_hidden())
        page.locator('[data-vt-agregar="palma-areca"]').click()
        page.locator('#vt-agregar button[value="agregar"]').click()
        mensaje = texto(page.locator(BARRA).get_attribute("href"))
        self.assertIn("• Palma Areca (", mensaje)
        self.assertTrue(mensaje.endswith("Colonia de entrega: ___\n\n¿Me dan precio y disponibilidad?"))
        self.assertEqual(page.locator("[data-vt-abrir-lista]").inner_text().replace("\n", " "), "Mi lista 1 1 variedad · 1 pieza")
        self.prestada(page, '#vt-lista [data-vt-o="enviar"]', "Cotizar mi lista", "catalogo")
        self.assertIn("• Palma Areca (", texto(page.locator('[data-vt-cta-rejilla] a').first.get_attribute("href")))
        page.evaluate("() => sessionStorage.removeItem('vt-catalogo-lista')")

    # ---------- 2. CTA en los tramos vacíos ----------
    def test_ningun_tramo_de_mas_de_6_pantallas_sin_whatsapp_en_linea(self):
        for ruta in ("/pasto-sintetico/", "/pasto-sintetico/toscana-28/", "/pasto-sintetico/envio/monterrey/",
                     "/plantas-palmas-arboles-tampico/", "/palmas-tropicales-tampico/", "/plantas-para-jardin-tampico/",
                     "/arboles-ornamentales-tampico/", "/arboles-para-banqueta-tampico/", "/plantas-de-interior-tampico/",
                     "/catalogo.html", "/mantenimiento-jardines-tampico/"):
            with self.subTest(ruta=ruta):
                page = self.pagina(ruta)
                page.evaluate(CARGAR)
                self.assertLessEqual(page.evaluate(TRAMO), 6)

    def test_catalogo_con_filtro_no_junta_filas_de_whatsapp(self):
        page = self.pagina("/catalogo.html?cat=palmas")
        filas = page.locator("[data-vt-cta-rejilla]:not([hidden])")
        visibles = page.evaluate("() => document.querySelectorAll('[data-vt-esp]:not([hidden])').length")
        self.assertLessEqual(filas.count(), visibles // 12)
        page.locator("[data-vt-limpiar]").click()
        self.assertGreaterEqual(page.locator("[data-vt-cta-rejilla]:not([hidden])").count(), 8)

    def test_tres_tarjetas_de_plan_contiguas_no_dicen_lo_mismo(self):
        for ruta in ("/mantenimiento-jardines-tampico/", "/diseno-jardines-tampico/", "/sistema-riego-tampico/",
                     "/mayoreo-pasto-tampico/", "/palmas-mayoreo-proyectos/"):
            with self.subTest(ruta=ruta):
                page = self.pagina(ruta, 1440, 900)
                textos = page.locator('[data-cta*=":opcion-"]').all_inner_texts()
                self.assertGreaterEqual(len(textos), 3)
                self.assertEqual(len(set(textos)), len(textos))

    # ---------- 6. interacción ----------
    def test_cuestionario_guarda_las_respuestas_al_recargar_sin_enviar_nada(self):
        page = self.pagina("/cuestionario.html")
        enviados = []
        page.on("request", lambda r: enviados.append(r.url) if r.method == "POST" else None)
        page.locator("#nombre").fill("María Prueba")
        page.locator('[name="direccion"]').fill("Lomas de Rosales")
        page.reload(wait_until="load")
        self.assertEqual(page.locator("#nombre").input_value(), "María Prueba")
        self.assertEqual(page.locator('[name="direccion"]').input_value(), "Lomas de Rosales")
        self.assertEqual(enviados, [])
        cuerpo = page.locator("main").text_content()
        for usted in ("¿Cómo nos conoció?", "le atrae", "¿Prefiere ", "4-5 minutos", "le gustan", "su mayor prioridad"):
            self.assertNotIn(usted, cuerpo)
        self.assertIn("Liga o descripción de fotos de referencia", cuerpo)
        page.evaluate("() => sessionStorage.clear()")

    # ---------- 7. menú y 404 ----------
    def test_menu_con_vivero_y_blog_sin_desbordar(self):
        for ancho, alto in ((320, 640), (375, 812), (1024, 768), (1100, 800), (1440, 900)):
            with self.subTest(ancho=ancho):
                page = self.pagina("/precios/", ancho, alto)
                self.assertLessEqual(page.evaluate("() => document.documentElement.scrollWidth"), ancho)
                if ancho >= 1100:
                    cajas = page.evaluate("""() => { const n = document.querySelector('.vt-nav').getBoundingClientRect();
                      const c = document.querySelector('.vt-head__cta').getBoundingClientRect();
                      const l = document.querySelector('.vt-head__logo').getBoundingClientRect();
                      const alto = Math.max(...Array.from(document.querySelectorAll('.vt-nav__item')).map((i) => i.getBoundingClientRect().height));
                      return [n.left >= l.right, n.right <= c.left, alto]; }""")
                    self.assertEqual(cajas[:2], [True, True])
                    self.assertLess(cajas[2], 50)  # una sola línea
                else:
                    page.click(".vt-burger")
                    for nombre in ("Vivero y horario", "Blog", "Servicios de jardín", "Plantas y materiales"):
                        self.assertTrue(page.locator("#vt-mmenu", has_text=nombre).count())
                    self.assertLessEqual(page.evaluate("() => document.documentElement.scrollWidth"), ancho)

    def test_404_encuentra_nochebuenas(self):
        page = self.pagina("/404.html")
        for busqueda in ("nochebuena", "nochebuenas", "palma real"):
            page.locator("#vt-buscar-404").fill(busqueda)
            with self.subTest(busqueda=busqueda):
                self.assertTrue(page.locator("#vt-vacio-404").is_hidden())
                visibles = page.locator("#vt-lista-404 li:not([hidden]) a").all_inner_texts()
                self.assertTrue(visibles)
        page.locator("#vt-buscar-404").fill("nochebuena")
        self.assertIn("Nochebuenas", page.locator("#vt-lista-404 li:not([hidden]) a").all_inner_texts())
        self.assertIn(datos.NOCHEBUENAS["ruta"], page.locator("#vt-lista-404 li:not([hidden]) a").first.get_attribute("href"))


if __name__ == "__main__":
    unittest.main()
