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
        self.assertIn("Estimado de la web: desde $72,000 (desde $60/m²)", mensaje)
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
