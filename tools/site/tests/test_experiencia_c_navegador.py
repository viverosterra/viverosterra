"""Entrega C de experiencia (ritmo y movimiento) en Chromium: ningún tramo de más de 6 pantallas del celular sin un
WhatsApp en línea en las plantillas que quedaban (índice y artículos del blog, Nochebuenas, materiales, empresas y
servicios); con movimiento reducido no corre ninguna animación ni queda nada transparente; con movimiento, tras recorrer
la página nada se queda a medio aparecer, con JavaScript apagado todo se ve y axe no encuentra violaciones serias ni a
media animación; la banda de garantía, las filas con desplazamiento y la condición de terreno listo del Medidor.
Todo el tráfico fuera de 127.0.0.1 se bloquea y no hay clics a wa.me ni a tel:. Un navegador a la vez. Se saltan sin
Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import generar  # noqa: E402
import servidor  # noqa: E402
from test_experiencia_b_navegador import CARGAR, TRAMO  # noqa: E402
from test_portada_navegador import AXE, AXE_PAGINA, LECTURA, VENTA  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

ARTICULOS = tuple(r + "/" for r, _a, plantilla, _c in generar.PAGINAS if plantilla == "articulo")
TRAMOS = ("/blog/", datos.NOCHEBUENAS["ruta"] + "/", "/tierra-negra-vegetal-tampico/", "/tezontle-rojo-tampico/",
          "/marmol-blanco-tampico/", "/piedra-bola-rio-tampico/", "/mayoreo-pasto-tampico/", "/palmas-mayoreo-proyectos/",
          "/pasto-en-rollo-tampico/", "/pasto-sintetico-tampico/", "/diseno-jardines-tampico/",
          "/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/")
# Una página por plantilla: las del hero de marca, las de lectura y las utilitarias.
PLANTILLAS = {**VENTA, **LECTURA, "404": "/404.html", "protocolo": "/protocolo-cuidados-pasto-san-agustin.html",
              "políticas": "/politicas/"}
TRANSPARENTES = """() => Array.from(document.querySelectorAll('body *')).filter((e) => {
  const s = getComputedStyle(e); const b = e.getBoundingClientRect();
  return s.display !== 'none' && s.visibility !== 'hidden' && b.width > 0 && b.height > 0 && parseFloat(s.opacity) < 1
    && !e.closest('[hidden], dialog:not([open]), .vt-cierre--foto .vt-cierre__fondo')
    // controles nativos tapados por su diseño (radios y casillas), la trampa de bots, el aviso que espera su turno
    // y lo deshabilitado no son movimiento
    && !e.matches('input, .vt-aviso, .vt-aviso *, [disabled], [aria-disabled="true"], label:has(input:disabled), label:has(input:disabled) *');
}).map((e) => e.tagName + '.' + String(e.className).split(' ')[0] + ' ' + getComputedStyle(e).opacity)"""
# Recorre la página hacia abajo, despacio, y se queda al final.
RECORRER = """async () => { const paso = innerHeight / 3;
  for (let y = 0; y <= document.documentElement.scrollHeight; y += paso) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); }
  scrollTo(0, document.documentElement.scrollHeight); await new Promise((r) => setTimeout(r, 200)); }"""
# Arriba del borde inferior de la ventana: lo que ya se vio al bajar (lo de abajo del todo puede no llegar al 28 %).
ATORADOS = """() => Array.from(document.querySelectorAll('main h2, main .vt-fig__marco')).filter((e) => {
  const b = e.getBoundingClientRect();
  return b.height > 0 && b.bottom < innerHeight * 0.72 && parseFloat(getComputedStyle(e).opacity) < 1;
}).map((e) => e.tagName + ' ' + (e.textContent || '').trim().slice(0, 40) + ' ' + getComputedStyle(e).opacity)"""
SIN_SALIR = """() => { window.open = () => null; document.addEventListener('click', (e) => {
  const a = e.target.closest && e.target.closest('a[href]');
  if (a && /^(https:\\/\\/wa\\.me|tel:)/.test(a.getAttribute('href'))) e.preventDefault(); }); }"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class ExperienciaCNavegadorTest(unittest.TestCase):
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

    def contexto(self, ancho=375, alto=812, movimiento="reduce", js=True):
        contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto}, reduced_motion=movimiento,
                                              java_script_enabled=js)
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        return contexto

    def abrir(self, contexto, ruta):
        page = contexto.new_page()
        page.goto(self.base + ruta, wait_until="load")
        if contexto.pages and page.evaluate("() => typeof window !== 'undefined'"):
            try:
                page.evaluate(SIN_SALIR)
            except Exception:  # sin JavaScript no hay evaluate de página que haga falta
                pass
        return page

    # ---------- 1. CTA en los tramos largos que quedaban ----------
    def test_ningun_tramo_de_mas_de_6_pantallas_en_las_plantillas_de_la_entrega_c(self):
        contexto = self.contexto()
        page = contexto.new_page()
        for ruta in TRAMOS + ARTICULOS:
            with self.subTest(ruta=ruta):
                page.goto(self.base + ruta, wait_until="load")
                page.evaluate(CARGAR)
                self.assertLessEqual(page.evaluate(TRAMO), 6)

    # ---------- 2. banda de garantía ----------
    def test_banda_de_garantia_oscura_con_condiciones_y_cta(self):
        contexto = self.contexto()
        for ruta in ("/pasto-en-rollo-tampico/", "/pasto-sintetico-tampico/", "/diseno-jardines-tampico/"):
            page = self.abrir(contexto, ruta)
            banda = page.locator("section.vt-banda")
            with self.subTest(ruta=ruta):
                self.assertEqual(banda.count(), 1)
                fondos = page.evaluate("""() => [getComputedStyle(document.querySelector('.vt-banda')).backgroundColor,
                    getComputedStyle(document.querySelector('.vt-cierre')).backgroundColor]""")
                self.assertEqual(fondos[0], fondos[1])
                self.assertTrue(banda.locator('a[href*="wa.me"]').first.is_visible())
                self.assertTrue(banda.locator('a[href^="/politicas"], a[href^="/protocolo"]').count())
                # a media página: ni en el primer tercio ni en el último cuarto
                y = page.evaluate("() => document.querySelector('.vt-banda').getBoundingClientRect().top + scrollY")
                total = page.evaluate("() => document.documentElement.scrollHeight")
                self.assertTrue(0.3 < y / total < 0.75, y / total)
        # Plan visual V2: sin garantía en datos.py, la banda es el proceso (nunca la garantía); Nochebuenas no lleva.
        for ruta in ("/mantenimiento-jardines-tampico/", "/sistema-riego-tampico/"):
            with self.subTest(ruta=ruta):
                page = self.abrir(contexto, ruta)
                self.assertEqual(page.locator(".vt-banda").count(), 1)
                self.assertEqual(page.locator(".vt-banda #vt-h-proceso").count(), 1)
        self.assertEqual(self.abrir(contexto, datos.NOCHEBUENAS["ruta"] + "/").locator(".vt-banda").count(), 0)

    # ---------- 3. filas con desplazamiento en celular ----------
    def test_filas_de_celular_se_desplazan_sin_ensanchar_la_pagina(self):
        contexto = self.contexto()
        page = self.abrir(contexto, "/diseno-jardines-tampico/")
        for selector in (".vt-testimonios--fila", ".vt-relacionados--fila", ".vt-modos--fila"):
            with self.subTest(selector=selector):
                fila = page.evaluate(f"""() => {{ const f = document.querySelector('{selector}');
                    return [f.scrollWidth > f.clientWidth, getComputedStyle(f).overflowX]; }}""")
                self.assertEqual(fila, [True, "auto"])
        self.assertLessEqual(page.evaluate("() => document.documentElement.scrollWidth"), 375)
        escritorio = self.abrir(self.contexto(1440, 900), "/diseno-jardines-tampico/")
        self.assertEqual(escritorio.evaluate("() => getComputedStyle(document.querySelector('.vt-modos--fila')).display"), "grid")

    # ---------- 4. movimiento ----------
    def test_con_movimiento_reducido_no_corre_nada_ni_queda_nada_transparente(self):
        contexto = self.contexto()
        page = contexto.new_page()
        for nombre, ruta in PLANTILLAS.items():
            with self.subTest(plantilla=nombre):
                page.goto(self.base + ruta, wait_until="load")
                page.evaluate(CARGAR)
                page.wait_for_timeout(100)
                self.assertEqual(page.evaluate("() => document.getAnimations().length"), 0)
                self.assertEqual(page.evaluate(TRANSPARENTES), [])

    def test_con_movimiento_nada_se_queda_a_medio_aparecer(self):
        for ancho, alto in ((375, 812), (1440, 900)):
            contexto = self.contexto(ancho, alto, movimiento="no-preference")
            page = contexto.new_page()
            for nombre, ruta in PLANTILLAS.items():
                with self.subTest(plantilla=nombre, ancho=ancho):
                    page.goto(self.base + ruta, wait_until="load")
                    page.wait_for_timeout(1000)  # el balanceo de la etiqueta (0.9 s) termina
                    page.evaluate(RECORRER)
                    self.assertEqual(page.evaluate(ATORADOS), [])
                    # lo que no es por scroll terminó y no se repite
                    corriendo = page.evaluate("""() => document.getAnimations().filter((a) => !(a.timeline instanceof
                        (window.ViewTimeline || function () {})) && a.playState === 'running').length""")
                    self.assertEqual(corriendo, 0)

    def test_sin_javascript_todo_se_ve(self):
        contexto = self.contexto(movimiento="no-preference", js=False)
        for nombre in ("servicio", "artículo", "nochebuenas", "inicio"):
            page = contexto.new_page()
            page.goto(self.base + PLANTILLAS[nombre], wait_until="load")
            with self.subTest(plantilla=nombre):
                ocultos = page.evaluate("""() => Array.from(document.querySelectorAll('main h1, main h2, main .vt-lede, main .vt-etiqueta__precio, main .vt-btn'))
                    .filter((e) => { const s = getComputedStyle(e);
                    return e.getClientRects().length && (s.visibility === 'hidden' || parseFloat(s.opacity) < 0.6); }).length""")
                self.assertEqual(ocultos, 0)
            page.close()

    def test_axe_sin_violaciones_serias_con_movimiento_y_a_media_animacion(self):
        contexto = self.contexto(movimiento="no-preference")
        page = contexto.new_page()
        for nombre in ("inicio", "servicio", "sintético en Tampico", "material con foto", "empresas", "nochebuenas",
                       "blog", "artículo"):
            with self.subTest(plantilla=nombre):
                page.goto(self.base + PLANTILLAS[nombre], wait_until="load")
                # el primer encabezado de sección entrando por abajo: a medio revelar
                page.evaluate("""() => { const h = document.querySelector('main .vt-bloque h2, main .vt-art__cuerpo h2');
                    if (h) scrollTo(0, h.getBoundingClientRect().top + scrollY - innerHeight * 0.9); }""")
                page.wait_for_timeout(200)
                page.add_script_tag(path=str(AXE))
                self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_balanceo_de_la_etiqueta_en_escritorio_en_todas_las_portadas_con_etiqueta(self):
        contexto = self.contexto(1440, 900, movimiento="no-preference")
        page = contexto.new_page()
        for nombre in ("inicio", "servicio", "zona", "empresas", "precios", "vivero"):
            with self.subTest(plantilla=nombre):
                page.goto(self.base + PLANTILLAS[nombre], wait_until="load")
                nombres = page.evaluate("""() => document.getAnimations().map((a) => a.animationName)""")
                self.assertIn("vt-balanceo", nombres)
        celular = self.contexto(375, 812, movimiento="no-preference").new_page()
        celular.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        self.assertNotIn("vt-balanceo", celular.evaluate("() => document.getAnimations().map((a) => a.animationName)"))

    # ---------- terreno listo (decisión del dueño, 2026-11-10) ----------
    def test_medidor_dice_la_condicion_en_instalado_y_la_quita_en_solo_pasto(self):
        page = self.abrir(self.contexto(), "/pasto-en-rollo-tampico/")
        caja = page.locator("[data-vt-medidor]")
        terreno = caja.locator('[data-vt-o="terreno"]')
        caja.locator('[data-vt-campo="largo"]').fill("8")
        caja.locator('[data-vt-campo="ancho"]').fill("6")
        self.assertTrue(terreno.is_visible())
        self.assertIn(datos.TERRENO_LISTO_MEDIDOR, terreno.inner_text())
        href = caja.locator('[data-vt-o="cta"]').get_attribute("href")
        self.assertIn("%C2%BFMi%20terreno%20est%C3%A1%20limpio", href)
        caja.locator('input[value="solo"]').check(force=True)
        self.assertTrue(terreno.is_hidden())
        self.assertNotIn("terreno%20est%C3%A1", caja.locator('[data-vt-o="cta"]').get_attribute("href"))

    def test_condicion_corta_visible_en_la_etiqueta_del_hero_en_celular(self):
        contexto = self.contexto()
        for ruta in ("/", "/pasto-en-rollo-tampico/", "/jardineria-altamira/", "/precios/"):
            page = self.abrir(contexto, ruta)
            cond = page.locator(".vt-portada .vt-etiqueta__cond")
            with self.subTest(ruta=ruta):
                self.assertTrue(cond.is_visible())
                self.assertEqual(cond.inner_text(), datos.TERRENO_LISTO_CORTO)
                self.assertLess(cond.bounding_box()["y"] + cond.bounding_box()["height"], 812)


if __name__ == "__main__":
    unittest.main()
