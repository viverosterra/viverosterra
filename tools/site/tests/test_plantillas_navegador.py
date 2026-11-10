"""Páginas con plantilla en Chromium: axe de página completa, primer pantallazo móvil, Medidor, sin desbordar y CLS.
Se saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qsl, unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path: mensualidades)
import datos  # noqa: E402
import mensualidades  # noqa: E402
import mensajes_paginas  # noqa: E402
import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
PAGINAS = ("/", "/pasto-en-rollo-tampico/")
# Etapa 2c: servicios de jardín con la plantilla de servicio (sin Medidor).
SERVICIOS = ("/diseno-jardines-tampico/", "/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/")
# Etapa 2d: páginas para empresas con la plantilla b2b (cotizador por volumen y armador de palmas).
EMPRESAS = ("/mayoreo-pasto-tampico/", "/palmas-mayoreo-proyectos/")
# Etapa 2e: hub y subcategorías con hub_categoria (portada con etiqueta) y el catálogo (sin portada).
PLANTAS = ("/plantas-palmas-arboles-tampico/", "/palmas-tropicales-tampico/", "/plantas-para-jardin-tampico/",
           "/arboles-ornamentales-tampico/", "/arboles-para-banqueta-tampico/", "/plantas-de-interior-tampico/")
# El servidor local no tiene cleanUrls de Vercel: el catálogo se pide como /catalogo.html (como en test_navegador.py).
CATALOGO = "/catalogo.html"
# Etapa 2f: materiales con la plantilla material (portada con o sin foto, calculadora y pedido por correo).
MATERIALES = ("/tierra-negra-vegetal-tampico/", "/tezontle-rojo-tampico/", "/marmol-blanco-tampico/",
              "/piedra-bola-rio-tampico/")
# Etapa 2g: las 6 zonas (plantilla zona) y la lista de precios (plantilla precios, con terra-precios.css).
ZONAS = tuple(f"{ruta}/" for _nombre, ruta in datos.ZONAS)
PRECIOS = "/precios/"
CON_PLANTILLA = PAGINAS + SERVICIOS + EMPRESAS + PLANTAS + MATERIALES + ZONAS + (PRECIOS,)
# El body recorta con overflow-x: clip y scrollWidth no ve lo que se sale: se mide cada caja visible del <main>. Un
# elemento dentro de un contenedor con scroll propio no cuenta (no se corta: se desplaza). Las imágenes de portada a
# sangre y sus marcos sí se miden: si sobresalen, también se cortan.
SALIDOS_DEL_MAIN = """(selector) => {
  const ancho = document.documentElement.clientWidth;
  const conScroll = (e) => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
    if (['auto', 'scroll'].includes(getComputedStyle(p).overflowX)) return true; } return false; };
  return Array.from(document.querySelectorAll(selector)).filter((e) => {
    const c = e.getBoundingClientRect();
    if (!c.width || !c.height || getComputedStyle(e).visibility === 'hidden' || conScroll(e)) return false;
    return c.right > ancho + 0.5 || c.left < -0.5;
  }).map((e) => e.tagName + '.' + e.className + ' [' + Math.round(e.getBoundingClientRect().left) + ', '
    + Math.round(e.getBoundingClientRect().right) + '] ' + e.textContent.trim().slice(0, 40));
}"""
# El texto que se sale de su celda no cambia la caja de la celda: se mide cada renglón de texto contra su th/td.
TEXTO_FUERA_DE_CELDA = """() => {
  const fuera = [];
  const rango = document.createRange();
  document.querySelectorAll('main .vt-tabla th, main .vt-tabla td').forEach((celda) => {
    const caja = celda.getBoundingClientRect();
    const textos = document.createTreeWalker(celda, NodeFilter.SHOW_TEXT);
    while (textos.nextNode()) {
      if (!textos.currentNode.textContent.trim()) continue;
      rango.selectNodeContents(textos.currentNode);
      for (const r of rango.getClientRects()) {
        if (r.width && (r.right > caja.right + 0.5 || r.left < caja.left - 0.5)) fuera.push(textos.currentNode.textContent.trim());
      }
    }
  });
  return fuera;
}"""
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

    def pagina(self, ancho=1440, alto=900, movimiento=False, js=True):
        """Por omisión con prefers-reduced-motion: reduce, para no medir ni revisar contraste a media animación (la
        home se anima al cargar y al desplazar desde la Entrega 2 del hero); movimiento=True lo prueba animado."""
        contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto}, java_script_enabled=js,
                                              reduced_motion="no-preference" if movimiento else "reduce")
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        return contexto.new_page()

    def test_axe_de_pagina_completa_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in CON_PLANTILLA + (CATALOGO,):
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
        """Revisión de 2c: a 1024×800 la portada compacta deja el CTA de los servicios de jardín (y, desde 2d, de las
        páginas para empresas) en la primera pantalla."""
        page = self.pagina(1024, 800)
        for ruta in SERVICIOS + EMPRESAS + MATERIALES + ZONAS + (PRECIOS,):
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

    def test_sin_desbordar_de_320_a_1920(self):
        for ancho in (320, 375, 768, 1024, 1440, 1920):
            page = self.pagina(ancho)
            for ruta in CON_PLANTILLA + (CATALOGO,):
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

    def test_medidor_con_iva_solo_en_modo_instalado(self):
        """Dueño (2026-11-10): el pasto sin instalar no lleva IVA. En la etiqueta, el cálculo y el mensaje del Medidor,
        "con IVA" solo aparece en modo instalado; en solo pasto y mayoreo (también cuando cae a solo pasto), nunca."""
        for ruta in PAGINAS:
            page = self.pagina(375, 812)
            page.goto(self.base + ruta, wait_until="load")
            caja = page.locator("[data-vt-medidor]")
            etiqueta = caja.locator(".vt-medidor__res")
            self.assertIn("con IVA", etiqueta.locator(".vt-etiqueta__precio").inner_text())  # arranca en instalado
            caja.locator('input[value="solo"]').check(force=True)
            self.assertNotIn("IVA", etiqueta.inner_text())  # sin medida todavía
            for largo, ancho, modo, con_iva in ((8, 6, "instalado", True), (8, 6, "solo", False), (10, 10, "mayoreo", False),
                                               (25, 24, "mayoreo", False)):
                caja.locator('[data-vt-campo="largo"]').fill(str(largo))
                caja.locator('[data-vt-campo="ancho"]').fill(str(ancho))
                caja.locator(f'input[value="{modo}"]').check(force=True)
                mensaje = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
                visible = etiqueta.inner_text() + " " + caja.locator(".vt-medidor__form").inner_text()
                with self.subTest(ruta=ruta, modo=modo, largo=largo):
                    self.assertEqual("con IVA" in visible, con_iva)
                    self.assertEqual("con IVA" in mensaje, con_iva)
                    if not con_iva:
                        self.assertIn("(no lleva IVA)", caja.locator('[data-vt-o="calc"]').inner_text())
                        self.assertRegex(mensaje, r"Estimado de la web: (?:desde )?\$[\d,]+ \(no lleva IVA\)")

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

    def test_barra_movil_se_esconde_solo_con_el_boton_del_medidor_a_la_vista(self):
        """Spec del hero (2026-11-09, §4): en la home la barra ya no se oculta en todo el Medidor; solo mientras su
        botón está a la vista. (Antes: se escondía con cualquier parte del Medidor en pantalla.)"""
        page = self.pagina(375, 812)
        page.goto(self.base + "/", wait_until="load")
        oculta = "document.querySelector('[data-vt-bar]').classList.contains('is-oculta')"
        page.locator('[data-vt-medidor] [data-vt-o="cta"]').scroll_into_view_if_needed()
        page.wait_for_function(f"() => {oculta}")
        # Con los campos arriba de la pantalla (y el botón todavía abajo), la barra vuelve.
        page.evaluate("() => scrollTo(0, document.querySelector('[data-vt-medidor]').getBoundingClientRect().top + scrollY - 80)")
        page.wait_for_function(f"() => !{oculta}")
        self.assertGreater(page.locator('[data-vt-medidor] [data-vt-o="cta"]').bounding_box()["y"], 812)
        page.locator("#vt-h-precios").scroll_into_view_if_needed()
        page.wait_for_function(f"() => !{oculta}")

    # ---------- hero nuevo de la home y conversión (spec 2026-11-09, Entrega 1) ----------
    def pagina_a_la_hora(self, ancho, alto, instante):
        page = self.pagina(ancho, alto)
        page.clock.set_fixed_time(instante)
        page.goto(self.base + "/", wait_until="load")
        return page

    def test_home_precio_y_cta_en_la_primera_pantalla_de_celulares(self):
        """Precio y botón de la portada completos en la primera pantalla a 375×812, 375×667, 360×640 y 320×640, aun
        con el prefijo "Abierto ahora" puesto; la barra móvil está oculta y no tapa el precio."""
        for ancho, alto in ((375, 812), (375, 667), (360, 640), (320, 640)):
            page = self.pagina_a_la_hora(ancho, alto, "2026-11-16T16:00:00Z")
            page.wait_for_function("() => document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
            precio = page.locator(".vt-portada .vt-etiqueta__precio").bounding_box()
            cta = page.locator(".vt-portada [data-hero-cta] .vt-btn--wa").bounding_box()
            lede = page.locator(".vt-portada .vt-lede").bounding_box()
            with self.subTest(ancho=ancho, alto=alto):
                self.assertLessEqual(precio["y"] + precio["height"], alto)
                self.assertLessEqual(cta["y"] + cta["height"], alto)
                self.assertGreaterEqual(cta["height"], 62)
                self.assertLess(lede["y"], precio["y"])
                self.assertLess(precio["y"], cta["y"])

    def test_home_precio_y_cta_en_la_primera_pantalla_de_laptops_bajas(self):
        """Revisión de diseño (2026-11-09): en pantallas bajas el hero se compacta; el precio de la etiqueta y el
        botón de WhatsApp quedan completos sin desplazar, y la etiqueta no tapa el pie de la foto."""
        for ancho, alto in ((1280, 620), (1366, 650), (1536, 730), (1440, 780), (1024, 650)):
            page = self.pagina_a_la_hora(ancho, alto, "2026-11-16T16:00:00Z")
            precio = page.locator(".vt-portada .vt-etiqueta__precio").bounding_box()
            cta = page.locator(".vt-portada [data-hero-cta] .vt-btn--wa").bounding_box()
            etiqueta = page.locator(".vt-portada .vt-etiqueta-x").bounding_box()
            marco = page.locator(".vt-portada__foto .vt-fig__marco").bounding_box()
            with self.subTest(ancho=ancho, alto=alto):
                self.assertLessEqual(precio["y"] + precio["height"], alto)
                self.assertLessEqual(cta["y"] + cta["height"], alto)
                self.assertGreaterEqual(cta["height"], 62)
                self.assertLessEqual(marco["y"] + marco["height"], alto)
                self.assertLess(etiqueta["y"] + etiqueta["height"], marco["y"] + marco["height"])
                self.assertGreater(etiqueta["y"], marco["y"])
                self.assertFalse(page.locator(".vt-portada .vt-etiqueta__nombre").is_visible())  # versión compacta

    def test_home_etiqueta_compacta_de_1024_a_1279_tapa_poco_la_foto(self):
        """De 1024 a 1279 px la etiqueta colgada es la compacta (la de celular): cubre a lo más ~20 % de la foto y no
        llega a su tercio superior (donde está el logo de la camisa). Desde 1280 (y con alto de sobra) va completa."""
        for ancho, alto in ((1024, 800), (1100, 900), (1279, 900)):
            page = self.pagina(ancho, alto)
            page.goto(self.base + "/", wait_until="load")
            e = page.locator(".vt-portada .vt-etiqueta-x").bounding_box()
            m = page.locator(".vt-portada__foto .vt-fig__marco").bounding_box()
            solape = (max(0, min(e["x"] + e["width"], m["x"] + m["width"]) - max(e["x"], m["x"]))
                      * max(0, min(e["y"] + e["height"], m["y"] + m["height"]) - max(e["y"], m["y"])))
            with self.subTest(ancho=ancho):
                self.assertFalse(page.locator(".vt-portada .vt-etiqueta__nombre").is_visible())
                self.assertLessEqual(solape / (m["width"] * m["height"]), 0.2)
                self.assertGreater(e["y"], m["y"] + m["height"] / 3)
                self.assertLess(e["y"] + e["height"], m["y"] + m["height"])
                self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, ".vt-portada .vt-etiqueta-x"), [])
        completa = self.pagina(1440, 900)
        completa.goto(self.base + "/", wait_until="load")
        self.assertTrue(completa.locator(".vt-portada .vt-etiqueta__nombre").is_visible())

    def test_home_tableta_boton_con_tope_etiqueta_al_lado_y_foto_que_no_llena_la_pantalla(self):
        for ancho, alto, lado_a_lado in ((560, 800, False), (640, 900, False), (768, 1024, True), (1023, 768, True)):
            page = self.pagina(ancho, alto)
            page.goto(self.base + "/", wait_until="load")
            cta = page.locator(".vt-portada [data-hero-cta] .vt-btn--wa").bounding_box()
            etiqueta = page.locator(".vt-portada .vt-etiqueta-x").bounding_box()
            marco = page.locator(".vt-portada__foto .vt-fig__marco").bounding_box()
            with self.subTest(ancho=ancho):
                self.assertLessEqual(cta["width"], 420)
                self.assertEqual(cta["x"] >= etiqueta["x"] + etiqueta["width"], lado_a_lado)
                if lado_a_lado:
                    self.assertAlmostEqual(cta["y"], etiqueta["y"], delta=2)
                    self.assertLessEqual(marco["height"], alto * 0.8)
                    self.assertAlmostEqual(marco["width"] / marco["height"], 16 / 9, places=1)
                self.assertLessEqual(page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth"), 1)

    def test_home_confianza_con_separadores_en_el_dom_que_no_se_pintan(self):
        # Reloj fijo fuera de horario (domingo 23:00 en México): en horario terra.js antepone "Abierto ahora" y la
        # prueba dependía de la hora en que corría.
        page = self.pagina_a_la_hora(375, 812, "2026-11-16T05:00:00Z")
        self.assertEqual(page.locator(".vt-portada__confianza").evaluate("e => e.textContent"),
                         f"{datos.PROMESA_COMPLETA} · {datos.GOOGLE} · {datos.CLIENTES} clientes")
        self.assertEqual(page.locator(".vt-portada__sep:visible").count(), 0)

    def test_home_filas_de_seccion_esconden_la_barra_y_caben_a_320(self):
        """Revisión de diseño: con una fila de WhatsApp de sección a la vista no hay dos botones iguales (la barra
        fija se esconde) y sus textos largos no ensanchan la página a 320 px."""
        oculta = "document.querySelector('[data-vt-bar]').classList.contains('is-oculta')"
        page = self.pagina(320, 640)
        page.goto(self.base + "/", wait_until="load")
        for seccion in ("opiniones", "proceso", "precios", "faq"):
            boton = page.locator(f'a[data-cta="home:{seccion}"]')
            boton.scroll_into_view_if_needed()
            page.wait_for_function(f"() => {oculta}")
            caja = boton.bounding_box()
            with self.subTest(seccion=seccion):
                self.assertGreaterEqual(caja["x"], 0)
                self.assertLessEqual(caja["x"] + caja["width"], 320)
                self.assertGreaterEqual(caja["height"], 44)
                self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, "main *"), [])
        # Fuera de las filas (en las fotos de obra no hay ningún CTA propio) la barra vuelve.
        page.evaluate("() => scrollTo(0, document.querySelector('.vt-obras').getBoundingClientRect().top + scrollY)")
        page.wait_for_function(f"() => !{oculta}")

    def test_home_medidor_renglon_vivo_barra_con_la_medida_y_garantia_solo_instalado(self):
        """Revisión de diseño: el resultado se lee bajo Largo × Ancho; con medida válida la barra fija manda la misma
        medida ("Enviar mi medida") y vuelve al genérico al borrarla; generate_lead sale una vez con el cta de la barra;
        la garantía de arraigo solo se muestra en modo instalado."""
        page = self.pagina(375, 667)
        page.goto(self.base + "/", wait_until="load")
        caja = page.locator("[data-vt-medidor]")
        vivo, barra, garantia = caja.locator('[data-vt-o="vivo"]'), page.locator("[data-vt-bar] .vt-bar__go"), caja.locator('[data-vt-o="garantia"]')
        generico = barra.get_attribute("href")
        self.assertFalse(vivo.is_visible())
        self.assertEqual(barra.text_content().strip(), "Cotizar por WhatsApp")
        caja.locator('[data-vt-campo="largo"]').fill("8")
        caja.locator('[data-vt-campo="ancho"]').fill("6")
        self.assertEqual(vivo.inner_text(), "48 m² · desde $5,760 con IVA")
        medidas = caja.locator(".vt-medidor__medidas").bounding_box()
        self.assertAlmostEqual(vivo.bounding_box()["y"], medidas["y"] + medidas["height"], delta=24)
        self.assertEqual(barra.text_content().strip(), "Enviar mi medida")
        self.assertEqual(barra.get_attribute("href"), caja.locator('[data-vt-o="cta"]').get_attribute("href"))
        self.assertTrue(garantia.is_visible())
        for modo, texto in (("solo", "48 m² · $4,080"), ("mayoreo", "48 m² · $4,080")):
            caja.locator(f'input[value="{modo}"]').check(force=True)
            with self.subTest(modo=modo):
                self.assertEqual(vivo.inner_text(), texto)
                self.assertNotIn("IVA", vivo.inner_text())
                self.assertFalse(garantia.is_visible())
        caja.locator('input[value="instalado"]').check(force=True)
        self.assertTrue(garantia.is_visible())
        # El clic en la barra con la medida: un solo generate_lead, con el cta de la barra, y el mensaje firmado.
        page.evaluate("() => { window.open = () => null; document.querySelector('[data-vt-bar] .vt-bar__go').addEventListener('click', (e) => e.preventDefault()); }")
        page.evaluate("() => scrollTo(0, document.querySelector('.vt-medidor__medidas').getBoundingClientRect().top + scrollY - 150)")
        page.wait_for_function("() => !document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
        barra.click()
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertEqual(eventos, [["event", "generate_lead", {"method": "whatsapp", "cta_id": "home:barra", "service": "general"}]])
        mensaje = unquote(barra.get_attribute("href").split("text=", 1)[1])
        self.assertIn("Medidas: 8.00 × 6.00 m = 48 m²", mensaje)
        self.assertTrue(mensaje.endswith(datos.FIRMA))
        # Al borrar la medida, la barra vuelve a su enlace y texto genéricos.
        caja.locator('[data-vt-campo="ancho"]').fill("")
        self.assertEqual(barra.text_content().strip(), "Cotizar por WhatsApp")
        self.assertEqual(barra.get_attribute("href"), generico)
        self.assertFalse(vivo.is_visible())
        # En pasto en rollo (sin los opcionales de la home) la barra no cambia.
        otra = self.pagina(375, 667)
        otra.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        otra.locator('[data-vt-campo="largo"]').fill("8")
        otra.locator('[data-vt-campo="ancho"]').fill("6")
        self.assertEqual(otra.locator("[data-vt-bar] .vt-bar__go").text_content().strip(), "Cotizar por WhatsApp")

    def test_home_objetivos_tactiles_del_hero_y_del_indice(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/", wait_until="load")
        for enlace in page.locator(".vt-inicio__enlaces a, .vt-indice__wa, .vt-inicio__fila .vt-btn").all():
            caja = enlace.bounding_box()
            with self.subTest(enlace=enlace.inner_text()):
                self.assertGreaterEqual(caja["height"], 44)

    def test_home_etiqueta_colgada_sobre_la_foto_en_escritorio(self):
        """Desde 1024 px la etiqueta cuelga sobre la esquina inferior izquierda de la foto, siempre derecha, sin tapar
        el pie de la figura ni salirse por abajo. (A 1024×800 la foto ya no es 4:5: en pantallas de 820 px de alto o
        menos toma la altura disponible; se mide con alto de sobra.)"""
        for ancho, alto in ((1024, 900), (1440, 900)):
            page = self.pagina(ancho, alto)
            page.goto(self.base + "/", wait_until="load")
            etiqueta = page.locator(".vt-portada .vt-etiqueta-x").bounding_box()
            marco = page.locator(".vt-portada__foto .vt-fig__marco").bounding_box()
            with self.subTest(ancho=ancho):
                self.assertLess(etiqueta["x"], marco["x"])
                self.assertGreater(etiqueta["x"] + etiqueta["width"], marco["x"])
                self.assertGreater(etiqueta["y"], marco["y"])
                self.assertLess(etiqueta["y"] + etiqueta["height"], marco["y"] + marco["height"])
                self.assertEqual(page.locator(".vt-portada .vt-etiqueta-x").evaluate(
                    "e => { const m = new DOMMatrix(getComputedStyle(e).transform); return [m.a, m.b, m.c, m.d]; }"),
                    [1, 0, 0, 1])
                self.assertAlmostEqual(marco["height"] / marco["width"], 5 / 4, places=1)
                cta = page.locator(".vt-portada [data-hero-cta] .vt-btn--wa").bounding_box()
                self.assertLessEqual(cta["y"] + cta["height"], alto)

    def test_home_abierto_ahora_solo_en_horario(self):
        """En horario, "Abierto ahora · " va antes de la promesa de la portada y del cierre; fuera de horario (y en
        festivo) el texto queda exactamente como en el HTML."""
        promesa = datos.PROMESA_COMPLETA
        casos = (("2026-11-16T16:00:00Z", True), ("2026-11-14T19:59:00Z", True), ("2026-11-14T20:00:00Z", False),
                 ("2026-11-15T18:00:00Z", False), ("2026-12-25T17:00:00Z", False))
        for instante, abierto in casos:
            page = self.pagina_a_la_hora(375, 812, instante)
            textos = page.locator("[data-vt-horario]").all_inner_texts()
            with self.subTest(instante=instante):
                self.assertEqual(textos, [f"Abierto ahora · {promesa}" if abierto else promesa] * 2)
                self.assertEqual(page.locator(".is-abierto").count(), 2 if abierto else 0)
                self.assertEqual(page.locator("main [aria-live]").count(), 0)

    def test_home_sin_javascript_se_lee_completa(self):
        contexto = self.navegador.new_context(viewport={"width": 375, "height": 812}, java_script_enabled=False)
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page = contexto.new_page()
        page.goto(self.base + "/", wait_until="load")
        self.assertEqual(page.locator("[data-vt-horario]").all_inner_texts(), [datos.PROMESA_COMPLETA] * 2)
        self.assertTrue(page.locator(".vt-portada [data-hero-cta] .vt-btn--wa").is_visible())
        self.assertEqual(page.locator('[data-vt-o="cta-texto"]').inner_text(), "Cotizar por WhatsApp")
        self.assertTrue(page.locator(".vt-medidor__garantia").is_visible())

    def test_home_medidor_en_celular_resultado_antes_del_plano_y_boton_con_medida(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/", wait_until="load")
        caja = page.locator("[data-vt-medidor]")
        campos = caja.locator(".vt-medidor__form").bounding_box()
        resultado = caja.locator(".vt-medidor__res").bounding_box()
        plano = caja.locator(".vt-medidor__plano").bounding_box()
        self.assertLess(campos["y"], resultado["y"])
        self.assertLess(resultado["y"] + resultado["height"], plano["y"] + 1)
        boton = caja.locator('[data-vt-o="cta"]')
        self.assertEqual(boton.inner_text().strip().splitlines()[0], "Cotizar por WhatsApp")
        caja.locator('[data-vt-campo="largo"]').fill("8")
        caja.locator('[data-vt-campo="ancho"]').fill("6")
        self.assertEqual(caja.locator('[data-vt-o="cta-texto"]').inner_text(), "Enviar mi medida por WhatsApp")
        self.assertIn("Medidas: 8.00 × 6.00 m = 48 m²", unquote(boton.get_attribute("href").split("text=", 1)[1]))
        ancho = boton.bounding_box()
        self.assertLessEqual(ancho["x"] + ancho["width"], 375)
        self.assertEqual(boton.evaluate("b => b.scrollWidth <= b.clientWidth + 1"), True)
        caja.locator('[data-vt-campo="ancho"]').fill("")
        self.assertEqual(caja.locator('[data-vt-o="cta-texto"]').inner_text(), "Cotizar por WhatsApp")
        # Desde 640 px el plano vuelve a ir antes del resultado (como antes).
        page.set_viewport_size({"width": 1440, "height": 900})
        self.assertLess(caja.locator(".vt-medidor__plano").bounding_box()["x"], caja.locator(".vt-medidor__res").bounding_box()["x"])

    # ---------- Entrega 2 del hero: movimiento, días de preventa, reseñas, menú y medición ----------
    OPACOS = """() => Array.from(document.querySelectorAll('main *')).filter((e) => {
      const c = e.getBoundingClientRect();
      return c.width && c.height && Number(getComputedStyle(e).opacity) < 1 && !e.matches('.vt-opciones input');  // radios ocultos a propósito
    }).map((e) => e.tagName + '.' + e.className + ' ' + getComputedStyle(e).opacity)"""
    RECORRER = """async () => { for (let y = 0; y <= document.documentElement.scrollHeight; y += Math.round(innerHeight / 2)) {
      scrollTo(0, y); await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); } }"""

    def test_home_con_movimiento_reducido_no_anima_nada(self):
        for ancho, alto in ((375, 812), (1440, 900)):
            page = self.pagina(ancho, alto)
            page.goto(self.base + "/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate("() => document.getAnimations().length"), 0)
                self.assertEqual(page.evaluate(self.OPACOS), [])
                page.evaluate(self.RECORRER)
                self.assertEqual(page.evaluate("() => document.getAnimations().length"), 0)
                self.assertEqual(page.evaluate(self.OPACOS), [])

    def test_home_animada_el_precio_el_titular_y_el_cta_se_leen_desde_el_primer_cuadro(self):
        """Con movimiento y sin JavaScript: H1, lede, precio y botón nunca empiezan transparentes ni fuera de pantalla."""
        for ancho, alto, js in ((375, 812, True), (1440, 900, True), (375, 812, False), (1440, 900, False)):
            page = self.pagina(ancho, alto, movimiento=True, js=js)
            page.goto(self.base + "/", wait_until="commit")
            page.wait_for_selector(".vt-portada [data-hero-cta] .vt-btn--wa")
            for selector in ("h1", ".vt-portada .vt-lede", ".vt-portada .vt-etiqueta__precio",
                             ".vt-portada [data-hero-cta] .vt-btn--wa"):
                elemento = page.locator(selector)
                with self.subTest(ancho=ancho, js=js, selector=selector):
                    self.assertTrue(elemento.is_visible())
                    self.assertEqual(elemento.evaluate("""e => { for (let n = e; n; n = n.parentElement) {
                      if (Number(getComputedStyle(n).opacity) < 1) return n.className; } return ''; }"""), "")
                    caja = elemento.bounding_box()
                    self.assertLessEqual(caja["y"] + caja["height"], alto)

    def test_home_animaciones_de_entrada_una_vez_cortas_y_la_etiqueta_termina_derecha(self):
        page = self.pagina(1440, 900, movimiento=True)
        page.goto(self.base + "/", wait_until="load")
        entrada = page.evaluate("""() => document.getAnimations().filter((a) => a instanceof CSSAnimation && a.timeline instanceof DocumentTimeline)
          .map((a) => { const t = a.effect.getComputedTiming(); return [a.animationName, t.duration + t.delay, t.iterations,
            a.effect.getKeyframes().flatMap((k) => Object.keys(k)).filter((p) => !['offset', 'easing', 'composite', 'computedOffset'].includes(p))]; })""")
        self.assertEqual(sorted(a[0] for a in entrada), ["vt-inicio-balanceo", "vt-inicio-foto"])
        for nombre, duracion, veces, propiedades in entrada:
            with self.subTest(animacion=nombre):
                self.assertLessEqual(duracion, 900)
                self.assertEqual(veces, 1)
                self.assertLessEqual(set(propiedades), {"transform", "clipPath", "opacity"})
        page.evaluate("() => Promise.all(document.getAnimations().filter((a) => a instanceof CSSAnimation && a.timeline instanceof DocumentTimeline).map((a) => a.finished))")
        self.assertEqual(page.locator(".vt-portada .vt-etiqueta-x").evaluate(
            "e => { const m = new DOMMatrix(getComputedStyle(e).transform); return [m.a, m.b, m.c, m.d]; }"), [1, 0, 0, 1])
        etiqueta = page.locator(".vt-portada .vt-etiqueta-x").bounding_box()
        marco = page.locator(".vt-portada__foto .vt-fig__marco").bounding_box()
        self.assertLess(etiqueta["y"] + etiqueta["height"], marco["y"] + marco["height"])
        # En celular no hay balanceo ni recorte de la foto.
        movil = self.pagina(375, 812, movimiento=True)
        movil.goto(self.base + "/", wait_until="load")
        self.assertEqual(movil.evaluate(
            "() => document.getAnimations().filter((a) => a instanceof CSSAnimation && a.timeline instanceof DocumentTimeline).length"), 0)

    def test_home_animada_axe_sin_violaciones_serias(self):
        """Con movimiento, lo que aún no entra en pantalla está a medio revelar: debe seguir cumpliendo contraste
        (Lighthouse corre axe así y exige accesibilidad 100)."""
        script = AXE.read_text(encoding="utf-8")
        for ancho, alto in ((375, 812), (1440, 900)):
            page = self.pagina(ancho, alto, movimiento=True)
            page.goto(self.base + "/", wait_until="load")
            page.add_script_tag(content=script)
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_home_animada_nada_queda_atorado_tras_recorrer_la_pagina(self):
        for ancho, alto in ((375, 812), (1440, 900)):
            page = self.pagina(ancho, alto, movimiento=True)
            page.goto(self.base + "/", wait_until="load")
            page.evaluate(self.RECORRER)
            page.evaluate("() => scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(300)
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate(self.OPACOS), [])

    def test_home_animada_el_salto_al_medidor_lo_deja_visible(self):
        for ancho, alto in ((375, 812), (1440, 900)):
            page = self.pagina(ancho, alto, movimiento=True)
            page.goto(self.base + "/", wait_until="load")
            page.click("#vt-calcula-patio")
            page.wait_for_function("() => Math.abs(document.getElementById('medidor').getBoundingClientRect().top) < 120")
            page.wait_for_timeout(200)
            with self.subTest(ancho=ancho):
                self.assertTrue(page.url.endswith("#medidor"))
                self.assertEqual(page.evaluate("""() => Array.from(document.querySelectorAll('#medidor *')).filter((e) => {
                  const c = e.getBoundingClientRect();
                  return c.height && c.top < innerHeight && c.bottom > 0 && Number(getComputedStyle(e).opacity) < 1 && !e.matches('.vt-opciones input');
                }).map((e) => e.tagName + ' ' + getComputedStyle(e).opacity)"""), [])
                self.assertTrue(page.locator('#medidor [data-vt-campo="largo"]').is_visible())

    def test_home_dias_de_preventa_en_el_banner_solo_donde_caben(self):
        """Desde 1024 px el banner agrega los días que faltan al renglón de precios; abajo de eso la frase sustituye a
        los precios (solo si hay texto) y el banner no crece. Con el reloj del cliente antes del build, nada."""
        hasta = datos.NOCHEBUENAS["preventa"]["hasta"]
        precios = "Desde $89 en menudeo y desde $65 por volumen"
        casos = ((f"{hasta}T18:00:00Z", "Último día de preventa"), ("2026-11-09T18:00:00Z", "Preventa: faltan 21 días"),
                 ("2026-11-29T18:00:00Z", "Preventa: falta 1 día"), ("2026-12-05T18:00:00Z", ""),
                 ("2026-10-20T18:00:00Z", ""))
        for instante, texto in casos:
            page = self.pagina_a_la_hora(1440, 900, instante)
            span = page.locator("[data-vt-hasta]")
            with self.subTest(instante=instante):
                self.assertEqual(span.text_content(), texto)
                self.assertEqual(span.is_visible(), bool(texto))
                self.assertEqual(page.locator(".vt-navidad__precios").inner_text(), precios)
                # El " · " entre precios y días lo pone el CSS, solo cuando hay texto.
                self.assertEqual(span.evaluate("e => getComputedStyle(e, '::before').content"),
                                 '" · "' if texto else "none")
        altos = {}
        for ancho in (320, 375, 768):
            for instante in ("2026-11-09T18:00:00Z", "2026-12-05T18:00:00Z"):
                page = self.pagina_a_la_hora(ancho, 812, instante)
                con_dias = instante.startswith("2026-11")
                with self.subTest(ancho=ancho, instante=instante):
                    self.assertEqual(page.locator(".vt-navidad__txt > span").inner_text(),
                                     "Preventa: faltan 21 días" if con_dias else precios)
                    self.assertEqual(page.locator(".vt-navidad__precios").is_visible(), not con_dias)
                altos.setdefault(ancho, []).append(page.locator(".vt-navidad").bounding_box()["height"])
        for ancho, (con_dias, sin_dias) in altos.items():
            self.assertLessEqual(con_dias, sin_dias, ancho)
        escritorio = self.pagina_a_la_hora(1024, 800, "2026-11-09T18:00:00Z")
        sin = self.pagina_a_la_hora(1024, 800, "2026-12-05T18:00:00Z")
        self.assertEqual(escritorio.locator(".vt-navidad").bounding_box()["height"],
                         sin.locator(".vt-navidad").bounding_box()["height"])

    def test_home_resenas_y_medicion_del_banner_y_del_ancla(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/", wait_until="load")
        resenas = page.locator(".vt-inicio__resenas a")
        self.assertEqual(resenas.get_attribute("href"), datos.MAPS_URL)
        self.assertEqual((resenas.get_attribute("target"), resenas.get_attribute("rel")), ("_blank", "noopener"))
        self.assertGreaterEqual(resenas.bounding_box()["height"], 44)
        page.evaluate("() => document.querySelector('.vt-navidad').addEventListener('click', (e) => e.preventDefault())")
        page.click(".vt-navidad")
        page.click("#vt-calcula-patio")
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertEqual(eventos, [["event", "select_content", {"content_type": "cta", "item_id": "home:banner-nochebuenas",
                                                                "cta_id": "home:banner-nochebuenas"}],
                                   ["event", "select_content", {"content_type": "cta", "item_id": "vt-calcula-patio",
                                                                "cta_id": "home:hero"}]])

    def test_menu_movil_con_whatsapp_a_la_vista(self):
        for ruta, tipo in (("/", "home"), ("/pasto-en-rollo-tampico/", "servicio-pasto")):
            page = self.pagina(375, 812)
            page.goto(self.base + ruta, wait_until="load")
            page.click(".vt-burger")
            boton = page.locator(f'#vt-mmenu a[data-cta="{tipo}:menu"][href^="https://wa.me/"]')
            boton.scroll_into_view_if_needed()
            caja = boton.bounding_box()
            with self.subTest(ruta=ruta):
                self.assertTrue(boton.is_visible())
                self.assertGreaterEqual(caja["height"], 44)
                self.assertGreaterEqual(caja["x"], 0)
                self.assertLessEqual(caja["x"] + caja["width"], 375)
                self.assertIn("Cotizar por WhatsApp", boton.inner_text())
                # A todo lo ancho, con 16 px de aire arriba, y la barra fija escondida mientras el menú está abierto.
                self.assertGreaterEqual(caja["width"], 375 - 2 * 16 - 1)
                self.assertEqual(boton.evaluate("b => getComputedStyle(b).marginTop"), "16px")
                self.assertEqual(page.locator("[data-vt-bar]").evaluate("b => getComputedStyle(b).visibility"), "hidden")
                self.assertLessEqual(page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth"), 1)

    def test_home_boton_del_hero_sin_transicion_con_movimiento_reducido(self):
        contexto = self.navegador.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page = contexto.new_page()
        page.goto(self.base + "/", wait_until="load")
        boton = page.locator(".vt-portada [data-hero-cta] .vt-btn--wa")
        self.assertIn(boton.evaluate("b => getComputedStyle(b).transitionDuration"), ("0s", "0s, 0s"))
        boton.focus()
        self.assertNotEqual(boton.evaluate("b => getComputedStyle(b).outlineStyle"), "none")

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

    def mensaje(self, caja):
        return unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])

    def test_cotizador_por_volumen_nunca_da_mayoreo_bajo_500_m2(self):
        page = self.pagina()
        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
        caja = page.locator("[data-vt-volumen]")
        generico = datos.con_firma(mensajes_paginas.EMPRESAS["/mayoreo-pasto-tampico"])
        self.assertEqual(self.mensaje(caja), generico)
        caja.locator('[data-vt-campo="m2"]').fill("320")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$27,200")
        self.assertIn("Te faltan 180 m²", caja.locator('[data-vt-o="aviso"]').inner_text())
        self.assertIn("solo el pasto San Agustín", self.mensaje(caja))
        caja.locator('[data-vt-campo="m2"]').fill("1,200")
        caja.locator('[data-vt-campo="empresa"]').fill("Mi empresa")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$72,000")
        self.assertFalse(caja.locator('[data-vt-o="aviso"]').is_visible())
        mensaje = self.mensaje(caja)
        self.assertIn("m² totales: 1,200 m²", mensaje)
        # Dueño (2026-11-10): el mayoreo (pasto sin instalar) no lleva IVA; antes decía "con IVA".
        self.assertIn("Estimado de la web: desde $72,000 (desde $60/m²; no lleva IVA)", mensaje)
        self.assertIn("Empresa: Mi empresa", mensaje)
        caja.locator('[data-vt-campo="m2"]').fill("")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "—")
        self.assertEqual(self.mensaje(caja), generico)

    def test_armador_de_palmas_arma_un_solo_mensaje(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/palmas-mayoreo-proyectos/", wait_until="load")
        caja = page.locator("[data-vt-palmas]")
        self.assertEqual(self.mensaje(caja), datos.con_firma(mensajes_paginas.EMPRESAS["/palmas-mayoreo-proyectos"]))
        caja.locator("#pal-especie-1").select_option("Palma real")
        caja.locator("#pal-altura-1").fill("3")
        caja.locator("#pal-cantidad-1").fill("40")
        caja.locator("#pal-especie-2").select_option("Coco plumoso")
        caja.locator("#pal-cantidad-2").fill("20")
        self.assertEqual(caja.locator('[data-vt-o="resumen"]').inner_text(), "2 especies · 60 piezas")
        mensaje = self.mensaje(caja)
        self.assertIn("- 40 × Palma real, altura aprox.: 3 m\n- 20 × Coco plumoso, altura aprox.: ___", mensaje)
        # "Agregar otra especie" aparece con JS, crea renglones con labels propios y se oculta en el octavo.
        agregar = caja.locator("[data-vt-agregar]")
        for n in range(4, 9):
            agregar.click()
            self.assertEqual(page.evaluate("() => document.activeElement.id"), f"pal-especie-{n}")
            self.assertEqual(caja.locator(f'label[for="pal-cantidad-{n}"]').count(), 1)
        self.assertFalse(agregar.is_visible())
        self.assertEqual(caja.locator("#pal-especie-8").input_value(), "")
        sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        self.assertLessEqual(sobra, 1)

    def test_clic_en_los_cotizadores_de_empresas_manda_generate_lead(self):
        for ruta, cta in (("/mayoreo-pasto-tampico/", "b2b:cotizador"), ("/palmas-mayoreo-proyectos/", "b2b:armador"),
                          ("/palmas-mayoreo-proyectos/", "b2b:opcion-2")):
            page = self.pagina()
            page.add_init_script("window.open = () => null;")
            page.goto(self.base + ruta, wait_until="load")
            boton = page.locator(f'[data-cta="{cta}"]')
            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
            boton.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            with self.subTest(ruta=ruta, cta=cta):
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": cta, "service": "empresas"}],
                              eventos)
                self.assertTrue(unquote(boton.get_attribute("href").split("text=", 1)[1]).endswith(datos.FIRMA))

    def test_barra_movil_se_esconde_con_el_cotizador_a_la_vista(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
        page.locator("[data-vt-volumen] .vt-etiqueta").scroll_into_view_if_needed()
        page.wait_for_function("() => document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")
        page.locator("#vt-h-faq").scroll_into_view_if_needed()
        page.wait_for_function("() => !document.querySelector('[data-vt-bar]').classList.contains('is-oculta')")

    @staticmethod
    def atrapador(enviados):
        """Responde en lugar de formsubmit y guarda método, URL y cuerpo de cada envío."""
        def atrapar(route):
            enviados.append((route.request.method, route.request.url, route.request.post_data or ""))
            route.fulfill(status=200, content_type="text/html", body="<p>ok</p>")
        return atrapar

    def test_formulario_por_correo_valida_y_envia_a_la_cuenta_oficial(self):
        """Respuesta del dueño (2026-11-08): las páginas B2B conservan la cotización por correo para compras. Sin los
        obligatorios no se envía (mensaje junto a cada campo y foco en el primero); completo, sale por POST a formsubmit
        de viverosterra@hotmail.com con generate_lead method "formulario"."""
        for ruta, clave, cantidad in (("/mayoreo-pasto-tampico/", "mayoreo", "1,200 m²"),
                                      ("/palmas-mayoreo-proyectos/", "palmas", "40 palma real de 3 m")):
            page = self.pagina(375, 812)
            enviados = []

            page.route("https://formsubmit.co/**", self.atrapador(enviados))
            page.goto(self.base + ruta, wait_until="load")
            form = page.locator("form.vt-correo")
            boton = form.locator('button[type="submit"]')
            boton.click()
            with self.subTest(ruta=ruta, paso="vacío"):
                self.assertEqual(enviados, [])
                self.assertEqual(page.evaluate("() => document.activeElement.name"), "empresa")
                for nombre in ("empresa", "nombre", "correo", "proyecto", "cantidad"):
                    self.assertEqual(form.locator(f'[name="{nombre}"]').get_attribute("aria-invalid"), "true")
                    ident = form.locator(f'[name="{nombre}"]').get_attribute("id")
                    self.assertTrue(form.locator(f"#{ident}-error").is_visible())
                self.assertIsNone(form.locator('[name="telefono"]').get_attribute("aria-invalid"))
                self.assertIn("Faltan 5 datos", form.locator('[data-vt-o="correo-estado"]').inner_text())
            form.locator('[name="empresa"]').fill("Constructora Ejemplo")
            form.locator('[name="nombre"]').fill("Compras")
            form.locator('[name="correo"]').fill("compras@")
            form.locator('[name="proyecto"]').fill("Fraccionamiento en Altamira")
            form.locator('[name="cantidad"]').fill(cantidad)
            boton.click()
            with self.subTest(ruta=ruta, paso="correo inválido"):
                self.assertEqual(enviados, [])
                self.assertEqual(page.evaluate("() => document.activeElement.name"), "correo")
            form.locator('[name="correo"]').fill("compras@ejemplo.com")
            # Se detiene el envío una vez para leer el dataLayer antes de salir de la página; luego se envía de verdad.
            page.evaluate("() => document.addEventListener('submit', (e) => e.preventDefault(), { once: true })")
            boton.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            with page.expect_navigation():
                page.evaluate("() => document.querySelector('form.vt-correo').submit()")
            with self.subTest(ruta=ruta, paso="enviado"):
                self.assertEqual(len(enviados), 1)
                metodo, url, cuerpo = enviados[0]
                self.assertEqual((metodo, url), ("POST", f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"))
                campos = dict(parse_qsl(cuerpo, keep_blank_values=True))
                self.assertEqual(campos["empresa"], "Constructora Ejemplo")
                self.assertEqual(campos["cantidad"], cantidad)
                self.assertEqual(campos["_honey"], "")
                self.assertEqual(campos["_next"], f"{datos.SITIO}/gracias")
                self.assertTrue(campos["_subject"].startswith("Cotización empresa · "))
                self.assertIn(["event", "generate_lead", {"method": "formulario", "cta_id": f"{clave}:formulario",
                                                          "service": "empresas"}], eventos)

    def test_cotizador_y_armador_prellenan_el_formulario_por_correo(self):
        page = self.pagina()
        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
        page.locator('[data-vt-volumen] [data-vt-campo="m2"]').fill("1,200")
        campo = page.locator('form.vt-correo [name="cantidad"]')
        self.assertEqual(campo.input_value(), "1,200 m²")
        campo.fill("1,500 m² en dos etapas")
        page.locator('[data-vt-volumen] [data-vt-campo="m2"]').fill("800")
        self.assertEqual(campo.input_value(), "1,500 m² en dos etapas")  # lo que escribe el visitante no se pisa
        # Empresa, obra y fecha del cotizador también pasan al formulario (la obra a "Proyecto y ubicación").
        form = page.locator("form.vt-correo")
        page.locator("#may-empresa").fill("Constructora Norte")
        page.locator("#may-obra").fill("Fraccionamiento en Altamira")
        page.locator("#may-fecha").fill("marzo")
        self.assertEqual([form.locator(f'[name="{n}"]').input_value() for n in ("empresa", "proyecto", "fecha")],
                         ["Constructora Norte", "Fraccionamiento en Altamira", "marzo"])
        form.locator('[name="empresa"]').fill("Constructora Norte SA de CV")
        page.locator("#may-empresa").fill("Otra")
        self.assertEqual(form.locator('[name="empresa"]').input_value(), "Constructora Norte SA de CV")
        self.assertEqual(form.locator('[name="proyecto"]').input_value(), "Fraccionamiento en Altamira")
        page.goto(self.base + "/palmas-mayoreo-proyectos/", wait_until="load")
        page.locator("#pal-especie-1").select_option("Palma real")
        page.locator("#pal-altura-1").fill("3")
        page.locator("#pal-cantidad-1").fill("40")
        page.locator("#pal-obra").fill("Hotel en Madero")
        self.assertEqual(page.locator('form.vt-correo [name="cantidad"]').input_value(),
                         "- 40 × Palma real, altura aprox.: 3 m")
        self.assertEqual(page.locator('form.vt-correo [name="proyecto"]').input_value(), "Hotel en Madero")

    def test_campo_con_error_no_queda_bajo_el_menu(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
        page.locator('form.vt-correo button[type="submit"]').click()
        menu = page.evaluate("() => document.querySelector('.vt-head').getBoundingClientRect().bottom")
        campo = page.evaluate("() => document.activeElement.closest('.vt-campo').getBoundingClientRect().top")
        self.assertEqual(page.evaluate("() => document.activeElement.name"), "empresa")
        self.assertGreaterEqual(campo, menu)

    def test_tabla_de_palmas_en_celular_y_completa_en_escritorio(self):
        visibles = """() => Array.from(document.querySelectorAll('.vt-tabla--especies tbody tr'))
          .filter((tr) => tr.offsetParent !== null).map((tr) => tr.querySelector('b').textContent)"""
        con_precio = [n for n, _c, p in datos.PALMAS_PROYECTO if p is not None]
        otras = len(datos.PALMAS_PROYECTO) - len(con_precio)
        for ancho, esperado in ((375, con_precio + [f"Otras {otras} especies"]),
                                (1440, [n for n, _c, _p in datos.PALMAS_PROYECTO])):
            page = self.pagina(ancho, 900)
            page.goto(self.base + "/palmas-mayoreo-proyectos/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.evaluate(visibles), esperado)

    def test_logos_sin_huerfano_en_celular(self):
        """7 clientes a 375–430 px: 2 columnas y el último a todo lo ancho, sin una celda suelta."""
        for ancho in (375, 430):
            page = self.pagina(ancho, 900)
            page.goto(self.base + "/mayoreo-pasto-tampico/", wait_until="load")
            cajas = page.evaluate("""() => Array.from(document.querySelectorAll('.vt-logos li'))
              .map((li) => { const r = li.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.width)]; })""")
            filas = {}
            for top, w in cajas:
                filas.setdefault(top, []).append(w)
            with self.subTest(ancho=ancho):
                anchos = sorted({sum(ws) for ws in filas.values()})
                self.assertLessEqual(anchos[-1] - anchos[0], 2)  # cada renglón llena el ancho

    def test_catalogo_precio_cta_y_buscador_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        page.goto(self.base + CATALOGO, wait_until="load")
        for selector in (".vt-cat__precios", ".vt-cat__cabeza [data-hero-cta] .vt-btn--wa"):
            caja = page.locator(selector).bounding_box()
            with self.subTest(selector=selector):
                self.assertLessEqual(caja["y"] + caja["height"], 812)
        self.assertLessEqual(page.locator("#vt-cat-q").bounding_box()["y"], 812 * 1.5)

    def test_catalogo_con_teclado_arma_un_solo_mensaje(self):
        page = self.pagina(1440, 900)
        page.goto(self.base + CATALOGO, wait_until="load")
        page.locator("#vt-cat-q").focus()
        page.keyboard.type("palma real")
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), "1 especie")
        self.assertIn("q=palma%20real", page.url)
        boton = page.locator('[data-vt-agregar="palma-real"]')
        boton.focus()
        page.keyboard.press("Enter")
        self.assertTrue(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.evaluate("() => document.activeElement.id"), "vt-agregar-tam")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")  # menos, cantidad, más
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")  # Cancelar, Agregar
        page.keyboard.press("Enter")
        self.assertFalse(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.evaluate("() => document.activeElement.dataset.vtAgregar"), "palma-real")
        page.locator("#vt-cat-q").fill("olivo")
        page.locator('[data-vt-agregar="olivo-negro"]').click()
        page.locator("#vt-agregar-n").fill("10")
        page.locator('#vt-agregar button[value="agregar"]').click()
        self.assertIn("2", page.locator('[data-vt-o="cuenta-lista"]').inner_text())
        page.locator("[data-vt-abrir-lista]").click()
        enviar = page.locator('#vt-lista [data-vt-o="enviar"]')
        mensaje = unquote(enviar.get_attribute("href").split("text=", 1)[1])
        self.assertIn("• Palma Real (", mensaje)
        self.assertIn("• Olivo Negro (", mensaje)
        self.assertIn("Total: 2 variedades, 11 unidades", mensaje)
        self.assertEqual(page.locator('#vt-lista a[href^="https://wa.me/"]').count(), 1)
        page.evaluate("(a) => a.addEventListener('click', (e) => e.preventDefault())", enviar.element_handle())
        enviar.click()
        eventos = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "catalogo:sendWA", "service": "plantas"}],
                      eventos)
        self.assertTrue(unquote(enviar.get_attribute("href")).endswith(datos.FIRMA))

    def test_agregar_desde_una_subcategoria_abre_el_dialogo_y_la_lista_sobrevive_la_recarga(self):
        page = self.pagina(375, 812)
        errores = []
        page.on("pageerror", lambda e: errores.append(str(e)))
        page.goto(self.base + "/palmas-tropicales-tampico/", wait_until="load")
        href = page.locator('.vt-esp__acciones a[href*="add=palma-real"]').get_attribute("href")
        self.assertEqual(href, "/catalogo?q=Palma%20Real&add=palma-real")
        page.goto(self.base + href.replace("/catalogo", CATALOGO, 1), wait_until="load")
        self.assertTrue(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.locator('#vt-agregar [data-vt-o="nombre"]').inner_text(), "Palma Real")
        self.assertNotIn("add=", page.url)
        self.assertIn("q=Palma%20Real", page.url)
        page.locator("#vt-agregar-n").fill("3")
        page.locator('#vt-agregar button[value="agregar"]').click()
        boton = page.locator('[data-vt-agregar="palma-real"]')
        self.assertEqual(boton.text_content(), "✓ En tu lista · editar Palma Real")  # el nombre, solo para lectores
        cabecera = page.locator('.vt-head [data-cta="catalogo:header"]')
        self.assertIn("• Palma Real (", unquote(cabecera.get_attribute("href")))
        page.reload(wait_until="load")
        self.assertFalse(page.locator("#vt-agregar").evaluate("d => d.open"))
        self.assertEqual(page.locator('[data-vt-o="cuenta-lista"]').inner_text(), "1")
        self.assertEqual(page.locator('[data-vt-agregar="palma-real"]').text_content(), "✓ En tu lista · editar Palma Real")
        page.locator("[data-vt-abrir-lista]").click()
        page.once("dialog", lambda d: d.dismiss())
        page.locator("[data-vt-vaciar]").click()
        self.assertEqual(page.locator('[data-vt-o="cuenta-lista"]').inner_text(), "1")  # confirm() cancelado
        page.once("dialog", lambda d: d.accept())
        page.locator("[data-vt-vaciar]").click()
        self.assertTrue(page.locator("[data-vt-barra-lista]").is_hidden())
        self.assertNotIn("text=Hola%20Viveros%20Terra%0A%0AQuisiera", cabecera.get_attribute("href"))
        self.assertEqual(errores, [])

    def test_slug_desconocido_y_almacenamiento_roto_no_rompen_el_catalogo(self):
        page = self.pagina(1440, 900)
        errores = []
        page.on("pageerror", lambda e: errores.append(str(e)))
        page.add_init_script("""sessionStorage.setItem('vt-catalogo-lista', '[{"name":"Inventada","sc":"x","sz":"1 m","qty":2}]');""")
        for consulta in ("?add=__proto__", "?add=no-existe", "?add="):
            page.goto(self.base + CATALOGO + consulta, wait_until="load")
            with self.subTest(consulta=consulta):
                self.assertFalse(page.locator("#vt-agregar").evaluate("d => d.open"))
                self.assertTrue(page.locator("[data-vt-barra-lista]").is_hidden())
                self.assertNotIn("add=", page.url)
        self.assertEqual(errores, [])

    def test_sin_resultados_ofrece_whatsapp_con_lo_buscado(self):
        page = self.pagina(375, 812)
        page.goto(self.base + CATALOGO, wait_until="load")
        page.locator("#vt-cat-q").fill("baobab enano")
        self.assertTrue(page.locator("[data-vt-vacio]").is_visible())
        wa = unquote(page.locator('[data-vt-o="vacio-wa"]').get_attribute("href"))
        self.assertIn("Busco: *baobab enano*", wa)
        self.assertEqual(page.locator("#vt-especial-q").input_value(), "baobab enano")
        self.assertIn("Busco: *baobab enano*", unquote(page.locator('[data-cta="catalogo:solEsp"]').get_attribute("href")))

    def test_filtros_cuentan_los_activos_y_la_etiqueta_muestra_la_especie_en_celular(self):
        page = self.pagina(375, 812)
        page.goto(self.base + CATALOGO + "?luz=sol&uso=salitre", wait_until="load")
        self.assertEqual(page.locator(".vt-buscador__filtros summary").inner_text(), "Filtros (2)")
        page.goto(self.base + "/plantas-palmas-arboles-tampico/", wait_until="load")
        nombre = page.locator(".vt-portada .vt-etiqueta__nombre")
        self.assertTrue(nombre.is_visible())
        self.assertEqual(nombre.inner_text(), "Areca y coco plumoso")

    def test_filtro_del_hub_llega_al_catalogo_con_el_mismo_conteo(self):
        page = self.pagina(1440, 900)
        page.goto(self.base + "/plantas-palmas-arboles-tampico/", wait_until="load")
        enlace = page.locator('a[data-cta="plantas:necesidad-salitre"]')
        conteo = enlace.locator(".vt-necesidad__n").inner_text()
        href = enlace.get_attribute("href")
        self.assertEqual(href, "/catalogo?uso=salitre")
        page.goto(self.base + href.replace("/catalogo", CATALOGO, 1), wait_until="load")
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), conteo)
        self.assertEqual(page.locator('[data-vt-g="uso"][data-vt-v="salitre"]').get_attribute("aria-pressed"), "true")
        page.locator("[data-vt-limpiar]").click()
        self.assertEqual(page.locator('[data-vt-o="cuenta"]').inner_text(), "117 especies")
        self.assertTrue(page.url.endswith(CATALOGO))

    def test_lcp_de_plantas_sin_api_img(self):
        lcp = """() => new Promise((listo) => { let ultimo = null;
          new PerformanceObserver((l) => { const e = l.getEntries(); ultimo = e[e.length - 1]; })
            .observe({ type: 'largest-contentful-paint', buffered: true });
          setTimeout(() => listo(ultimo ? (ultimo.url || ultimo.element.tagName) : ''), 1500); })"""
        page = self.pagina(375, 812)
        for ruta in PLANTAS + (CATALOGO,):
            pedidas = []
            page.on("request", lambda r: pedidas.append(r.url))
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertNotIn("/api/img", page.evaluate(lcp))
                self.assertEqual([u for u in pedidas if "/api/img" in u], [])

    # ---------- Etapa 2f: materiales ----------
    CALCULOS = (
        ("/tierra-negra-vegetal-tampico/", "vt-tierra", "87.5", "0.10", "material:cotizarCalculado", "8.8 m³"),
        ("/tezontle-rojo-tampico/", "vt-tezontle", "50", "0.08", "material:cotizarTezontle", "4 m³"),
        ("/marmol-blanco-tampico/", "vt-marmol", "50", "6", "material:cotizarMarmol", "250 sacos"),
        ("/piedra-bola-rio-tampico/", "vt-piedra", "10", None, "material:cotizarPiedra", "1,200 a 1,500 kg"),
    )

    def test_calculadoras_de_materiales_con_teclado_mensaje_y_generate_lead(self):
        """La calculadora de main, ahora un enlace medido: con teclado da la cantidad de main, el WhatsApp lleva el
        resultado y la firma, y el clic manda generate_lead con el mismo cta_id que medía VTMedicion.whatsapp."""
        for ruta, prefijo, area, capa, cta_id, cantidad in self.CALCULOS:
            page = self.pagina(1440, 900)
            page.goto(self.base + ruta, wait_until="load")
            page.locator(f"#{prefijo}-area").focus()
            page.keyboard.type(area)
            if capa:
                page.locator(f"#{prefijo}-capa").select_option(capa)
            caja = page.locator("[data-vt-material]")
            enlace = caja.locator('[data-vt-o="cta"]')
            mensaje = unquote(enlace.get_attribute("href").split("text=", 1)[1])
            with self.subTest(ruta=ruta):
                self.assertEqual(caja.locator('[data-vt-o="cantidad"]').inner_text(), cantidad)
                self.assertIn(f"Área: {area} m²", mensaje)
                self.assertTrue(mensaje.endswith("Colonia de entrega: ___\n\n¿Me pueden dar precio de entrega a domicilio en "
                                                 "Tampico, Madero o Altamira?"))
                self.assertNotIn("is-vacio", caja.locator(".vt-calc__cantidad").get_attribute("class"))
            page.evaluate("(a) => a.addEventListener('click', (e) => e.preventDefault())", enlace.element_handle())
            enlace.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            with self.subTest(ruta=ruta, paso="clic"):
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": cta_id, "service": "materiales"}],
                              eventos)
                self.assertTrue(unquote(enlace.get_attribute("href")).endswith(datos.FIRMA))

    def test_calculadora_de_materiales_sin_area_manda_el_mensaje_de_la_pagina(self):
        page = self.pagina(375, 812)
        for ruta, prefijo, area, _capa, _cta, _cantidad in self.CALCULOS:
            page.goto(self.base + ruta, wait_until="load")
            campo = page.locator(f"#{prefijo}-area")
            campo.fill(area)
            campo.fill("")
            esperado = datos.con_firma(mensajes_paginas.MATERIALES[ruta.rstrip("/")])
            href = page.locator('[data-vt-material] [data-vt-o="cta"]').get_attribute("href")
            with self.subTest(ruta=ruta):
                self.assertEqual(unquote(href.split("text=", 1)[1]), esperado)
                self.assertEqual(page.locator('[data-vt-material] [data-vt-o="cantidad"]').inner_text(), "Escribe el área")
                self.assertIn("is-vacio", page.locator("[data-vt-material] .vt-calc__cantidad").get_attribute("class"))

    def test_pedido_por_correo_de_materiales_valida_y_envia_los_campos_de_main(self):
        """El formulario de main (nombre, email, detalle) sigue yendo por POST a formsubmit de la cuenta oficial, ahora
        con honeypot, validación junto a cada campo y generate_lead method "formulario"."""
        page = self.pagina(375, 812)
        enviados = []
        page.route("https://formsubmit.co/**", self.atrapador(enviados))
        page.goto(self.base + "/marmol-blanco-tampico/", wait_until="load")
        form = page.locator("#solicitar-pedido form.vt-correo")
        boton = form.locator('button[type="submit"]')
        boton.click()
        self.assertEqual(enviados, [])
        self.assertEqual(page.evaluate("() => document.activeElement.name"), "nombre")
        form.locator('[name="nombre"]').fill("Ana")
        form.locator('[name="email"]').fill("ana@")
        boton.click()
        self.assertEqual(page.evaluate("() => document.activeElement.name"), "email")
        self.assertIn("tu@correo.com", form.locator("#vt-marmol-c-email-error").inner_text())
        form.locator('[name="email"]').fill("ana@ejemplo.com")
        form.locator('[name="detalle"]').fill("36 sacos, entrega en Tampico")
        page.evaluate("() => document.addEventListener('submit', (e) => e.preventDefault(), { once: true })")
        boton.click()
        eventos = page.evaluate("() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        with page.expect_navigation():
            page.evaluate("() => document.querySelector('#solicitar-pedido form').submit()")
        metodo, url, cuerpo = enviados[0]
        campos = dict(parse_qsl(cuerpo, keep_blank_values=True))
        self.assertEqual((metodo, url), ("POST", f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"))
        self.assertEqual({k: campos[k] for k in ("nombre", "email", "detalle", "_subject", "_next", "_honey")},
                         {"nombre": "Ana", "email": "ana@ejemplo.com", "detalle": "36 sacos, entrega en Tampico",
                          "_subject": "Pedido desde sitio web - Viveros Terra", "_next": f"{datos.SITIO}/gracias",
                          "_honey": ""})
        self.assertIn(["event", "generate_lead", {"method": "formulario", "cta_id": "material:formulario",
                                                  "service": "materiales"}], eventos)

    def test_calculadoras_de_materiales_con_resultado_largo_no_se_salen_de_la_pantalla(self):
        """El body recorta con overflow-x: clip, así que scrollWidth no ve lo que se sale: se miden las cajas. El
        resultado más largo de main ("Camión volteo de 8 m³ o más (según cotización)") no ensancha la columna."""
        casos = (("/tierra-negra-vegetal-tampico/", "vt-tierra", "87.5", "0.10"),
                 ("/tierra-negra-vegetal-tampico/", "vt-tierra", "5000", "0.15"),
                 ("/tezontle-rojo-tampico/", "vt-tezontle", "5000", "0.08"),
                 ("/marmol-blanco-tampico/", "vt-marmol", "99999", "6"),
                 ("/piedra-bola-rio-tampico/", "vt-piedra", "99999", None))
        for ancho in (320, 375, 1024):
            page = self.pagina(ancho, 812)
            for ruta, prefijo, area, capa in casos:
                page.goto(self.base + ruta, wait_until="load")
                page.locator(f"#{prefijo}-area").fill(area)
                if capa:
                    page.locator(f"#{prefijo}-capa").select_option(capa)
                fuera = page.evaluate("""() => { const sec = document.querySelector('#calculadora .vt-wrap')
                  .getBoundingClientRect(); return Array.from(document.querySelectorAll('#calculadora .vt-b2b *'))
                  .filter((e) => { const r = e.getBoundingClientRect(); return r.width && (r.right > sec.right + 0.5
                  || r.right > innerWidth); }).map((e) => e.tagName + '.' + e.className).slice(0, 5) }""")
                with self.subTest(ancho=ancho, ruta=ruta, area=area, capa=capa):
                    self.assertEqual(fuera, [])

    def test_fotos_de_materiales_cargan_sin_deformarse(self):
        """Las fotos de main, todas: ninguna rota tras desplazar la página (carga lazy) y ninguna estirada."""
        page = self.pagina(1440, 900)
        for ruta in MATERIALES:
            page.goto(self.base + ruta, wait_until="load")
            page.evaluate("async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) {"
                          " scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } }")
            page.wait_for_load_state("networkidle")
            malas = page.evaluate("""() => Array.from(document.querySelectorAll('main img')).filter((i) =>
              !i.complete || !i.naturalWidth || getComputedStyle(i).objectFit === 'fill').map((i) => i.src)""")
            with self.subTest(ruta=ruta):
                self.assertEqual(malas, [])

    # ---------- Etapa 2g: zonas y precios ----------
    def test_cta_de_zona_manda_su_mensaje_y_generate_lead(self):
        """La portada de cada zona abre el WhatsApp con el mensaje de esa zona (el de main) y lo mide como zona:hero."""
        page = self.pagina(375, 812)
        for ruta in ZONAS:
            page.goto(self.base + ruta, wait_until="load")
            boton = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa')
            page.evaluate("(b) => b.addEventListener('click', (e) => e.preventDefault())", boton.element_handle())
            boton.click()
            eventos = page.evaluate(
                "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
            texto = unquote(boton.get_attribute("href").split("text=", 1)[1])
            with self.subTest(ruta=ruta):
                self.assertEqual(texto, datos.con_firma(mensajes_paginas.ZONAS[ruta.rstrip("/")]))
                self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "zona:hero",
                                                          "service": "jardin"}], eventos)

    def test_etiqueta_de_zona_dice_de_que_es_el_precio_en_celular(self):
        """En celular terra.css oculta el nombre de la etiqueta: el renglón del precio debe decir a qué corresponde."""
        page = self.pagina(375, 812)
        for ruta in ZONAS:
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertFalse(page.locator(".vt-portada .vt-etiqueta__nombre").is_visible())
                self.assertIn("instalado", page.locator(".vt-portada .vt-etiqueta__precio small").inner_text().lower())

    def test_simulador_de_precios_con_la_formula_oficial(self):
        """El simulador de /precios (vt-simulador.js + vt-mensualidades.js) muestra los 4 plazos con el total y la
        mensualidad de tools/pasto/mensualidades.py para el monto de ejemplo."""
        page = self.pagina()
        page.goto(self.base + PRECIOS, wait_until="load")
        monto = int(page.input_value("[data-sim-monto]"))
        texto = page.locator("[data-sim-list]").inner_text()
        for p in mensualidades.planes(monto):
            if p["plazo"] and p["disponible"]:
                with self.subTest(plazo=p["plazo"]):
                    self.assertIn(f"${p['mensualidad']:,}", texto)
                    self.assertIn(f"${p['total']:,}", texto)

    def test_tablas_de_precios_compactas_en_celular(self):
        """Sintético por modelo y mensualidades siguen siendo tabla a 320 px (no una tarjeta por renglón) y no se salen."""
        page = self.pagina(320, 800)
        page.goto(self.base + PRECIOS, wait_until="load")
        for tabla in page.locator(".vt-tabla--compacta").all():
            caja = tabla.bounding_box()
            with self.subTest(tabla=tabla.locator("caption").inner_text()[:30]):
                self.assertEqual(tabla.evaluate("t => getComputedStyle(t).display"), "table")
                self.assertLessEqual(caja["x"] + caja["width"], 320)

    def test_nada_del_main_se_sale_de_la_pantalla_en_celular(self):
        """Medido caja por caja (el overflow-x: clip del body esconde lo que se sale de scrollWidth): cada tabla, celda,
        enlace y texto de /precios y de las 6 zonas cabe en 320 y 375, también con el simulador en su monto más largo."""
        for ancho in (320, 375):
            page = self.pagina(ancho, 800)
            for ruta in ZONAS + (PRECIOS,):
                page.goto(self.base + ruta, wait_until="load")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, "main, main *"), [])
                    self.assertEqual(page.evaluate(TEXTO_FUERA_DE_CELDA), [])
            page.goto(self.base + PRECIOS, wait_until="load")
            page.fill("[data-sim-monto]", "9999999")
            page.locator("[data-sim-monto]").dispatch_event("input")
            with self.subTest(simulador="monto largo", ancho=ancho):
                self.assertEqual(page.evaluate(SALIDOS_DEL_MAIN, "main, main *"), [])

    def test_anclas_de_precios_llevan_a_su_seccion(self):
        """#garantia-plantas y #mensualidades desde otra página: la sección queda a la vista y no bajo el menú."""
        page = self.pagina(375, 812)
        for ancla in ("mensualidades", "garantia-plantas", "pasto"):
            page.goto(f"{self.base}{PRECIOS}#{ancla}", wait_until="load")
            arriba = page.locator(f"#{ancla}").evaluate("e => e.getBoundingClientRect().top")
            menu = page.locator(".vt-head").evaluate("e => e.getBoundingClientRect().bottom")
            with self.subTest(ancla=ancla):
                self.assertGreaterEqual(arriba, menu - 1)
                self.assertLess(arriba, 812)

    def test_cls_bajo_0_1_en_movil(self):
        page = self.pagina(375, 812)
        for ruta in CON_PLANTILLA + (CATALOGO,):
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertLess(page.evaluate(CLS), 0.1)


if __name__ == "__main__":
    unittest.main()
