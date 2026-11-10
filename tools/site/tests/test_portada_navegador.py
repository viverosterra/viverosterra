"""Hero de marca en Chromium (Entrega A de experiencia, 2026-11-10), una página por plantilla: en celulares de 375×667,
360×640 y 375×812 el precio y el botón principal caben completos en la primera pantalla y ninguna barra fija los tapa; a
375×812 la foto de portada asoma; a 1366×650 y 1440×900 precio y botón completos; sin scroll horizontal de 320 a 1920;
el botón principal mide 60 px o más y es el único relleno del hero; axe sin violaciones serias.
Todo lo que no sea el servidor local se bloquea; sin clics. Se salta sin Playwright."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
# Una página por plantilla (o variante) con botón principal en el hero.
VENTA = {
    "inicio": "/", "servicio": "/pasto-en-rollo-tampico/", "servicio de jardín": "/mantenimiento-jardines-tampico/",
    "sintético en Tampico": "/pasto-sintetico-tampico/", "hub de plantas": "/plantas-palmas-arboles-tampico/",
    "subcategoría": "/palmas-tropicales-tampico/", "material con foto": "/tierra-negra-vegetal-tampico/",
    "material sin foto": "/tezontle-rojo-tampico/", "empresas": "/mayoreo-pasto-tampico/", "zona": "/jardineria-altamira/",
    "ciudad": "/pasto-sintetico/envio/monterrey/", "guía de la tienda": "/pasto-sintetico/perros/", "precios": "/precios/",
    "vivero": "/vivero-tampico/", "tienda": "/pasto-sintetico/", "ficha": "/pasto-sintetico/toscana-28/",
    "nochebuenas": datos.NOCHEBUENAS["ruta"] + "/", "catálogo": "/catalogo.html",
}
# Cabeceras de lectura: sin botón grande, con el WhatsApp como enlace de texto.
LECTURA = {"blog": "/blog/", "artículo": "/blog/pasto-san-agustin-vs-japones/"}
# La home conserva su diseño aprobado (2026-11-09): en celular la foto va después del botón y la línea de confianza.
SIN_FOTO_ARRIBA = {"inicio", "material sin foto", "catálogo"}
CELULARES = ((375, 667), (360, 640), (375, 812))
ESCRITORIOS = ((1366, 650), (1440, 900))
ANCHOS = (320, 360, 375, 414, 600, 768, 1024, 1280, 1440, 1920)
ASOMA = 120
# El hero es la primera sección del <main> (o la cabecera del artículo). Devuelve cajas [arriba, abajo] en la ventana.
MEDIR = """() => {
  const caja = (e) => { const b = e.getBoundingClientRect(); return [b.top, b.bottom, b.left, b.right]; };
  const visible = (e) => e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const hero = document.querySelector('main > section, main > header');
  const uno = (s) => { const e = hero.querySelector(s); return visible(e) ? e : null; };
  const boton = uno('[data-hero-cta] .vt-btn');
  const precio = uno('.vt-etiqueta__precio');
  const foto = uno('.vt-portada__foto img') || uno('.vt-galeria img');
  // En la ficha la primera sección trae también la galería y el cotizador (con su propio botón): el hero es su cabecera.
  const cabecera = hero.querySelector('.vt-ficha__info') || hero;
  const rellenos = Array.from(cabecera.querySelectorAll('.vt-btn, button')).filter((e) => visible(e)
    && !['rgba(0, 0, 0, 0)', 'transparent'].includes(getComputedStyle(e).backgroundColor)
    && getComputedStyle(e).backgroundColor === getComputedStyle(boton || e).backgroundColor);
  const fijas = Array.from(document.querySelectorAll('.vt-bar, [data-nb-bar], .vt-compra, .vt-aviso')).filter((e) => {
    const s = getComputedStyle(e); const b = e.getBoundingClientRect();
    return s.position === 'fixed' && s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0'
      && b.height > 0 && b.top < innerHeight;
  }).map(caja);
  const enlaces = Array.from(hero.querySelectorAll('.vt-portada__enlaces a')).filter(visible).map((e) => e.getBoundingClientRect().height);
  return {alto: innerHeight, sobra: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          boton: boton && caja(boton), precio: precio && caja(precio), foto: foto && caja(foto), rellenos: rellenos.length,
          fijas, enlaces, menu: document.querySelector('.vt-head').getBoundingClientRect().bottom};
}"""
AXE_PAGINA = """async () => {
  const r = await axe.run(document, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado")
class PortadaNavegadorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.servidor = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.navegador = cls.pw.chromium.launch()
        cls.medidas, cls.axe = {}, {}
        paginas = {**VENTA, **LECTURA}
        tamanos = set(CELULARES) | set(ESCRITORIOS) | {(ancho, 900) for ancho in ANCHOS}
        for ancho, alto in sorted(tamanos):
            contexto = cls.navegador.new_context(viewport={"width": ancho, "height": alto}, reduced_motion="reduce")
            contexto.route("**/*", lambda ruta: ruta.continue_() if ruta.request.url.startswith(cls.base) else ruta.abort())
            page = contexto.new_page()
            for nombre, ruta in paginas.items():
                page.goto(cls.base + ruta, wait_until="load")
                # terra.js esconde la barra fija con un IntersectionObserver: se espera a que resuelva.
                page.wait_for_timeout(250)
                cls.medidas[nombre, ancho, alto] = page.evaluate(MEDIR)
                if (ancho, alto) == CELULARES[0]:
                    page.add_script_tag(path=str(AXE))
                    cls.axe[nombre] = page.evaluate(AXE_PAGINA)
            contexto.close()

    @classmethod
    def tearDownClass(cls):
        cls.navegador.close()
        cls.pw.stop()
        cls.servidor.shutdown()
        cls.servidor.server_close()

    def completos(self, nombre, tamano):
        m = self.medidas[(nombre, *tamano)]
        tope = min([m["alto"]] + [fija[0] for fija in m["fijas"] if fija[0] > m["alto"] / 2])
        self.assertIsNotNone(m["boton"], "botón principal del hero")
        for parte in ("boton", "precio"):
            if m[parte]:
                arriba, abajo = m[parte][:2]
                self.assertGreaterEqual(arriba, m["menu"] - 0.5, f"{parte} bajo el menú")
                self.assertLessEqual(abajo, tope + 0.5, f"{parte} completo en la primera pantalla y sin barra encima")

    def test_celular_precio_y_boton_completos_y_sin_barra_encima(self):
        for nombre in VENTA:
            for tamano in CELULARES:
                with self.subTest(pagina=nombre, tamano=tamano):
                    self.completos(nombre, tamano)

    def test_escritorio_precio_y_boton_completos(self):
        for nombre in VENTA:
            for tamano in ESCRITORIOS:
                with self.subTest(pagina=nombre, tamano=tamano):
                    self.completos(nombre, tamano)

    def test_la_foto_asoma_en_la_primera_pantalla_del_celular(self):
        for nombre in VENTA:
            m = self.medidas[nombre, 375, 812]
            if nombre in SIN_FOTO_ARRIBA:
                continue
            with self.subTest(pagina=nombre):
                self.assertIsNotNone(m["foto"])
                arriba, abajo = m["foto"][:2]
                self.assertGreaterEqual(min(abajo, m["alto"]) - max(arriba, m["menu"]), ASOMA)

    def test_boton_principal_alto_y_unico_relleno(self):
        for nombre in VENTA:
            for tamano in (CELULARES[0], ESCRITORIOS[1]):
                m = self.medidas[(nombre, *tamano)]
                with self.subTest(pagina=nombre, tamano=tamano):
                    self.assertGreaterEqual(m["boton"][1] - m["boton"][0], 60)
                    self.assertEqual(m["rellenos"], 1)

    def test_enlaces_de_texto_con_objetivo_de_44(self):
        for nombre in {**VENTA, **LECTURA}:
            m = self.medidas[nombre, 375, 667]
            with self.subTest(pagina=nombre):
                self.assertTrue(m["enlaces"], "el hero lleva al menos un enlace de texto (el teléfono)")
                self.assertGreaterEqual(min(m["enlaces"]), 44)

    def test_lectura_sin_boton_grande_y_sin_barra_al_cargar(self):
        for nombre in LECTURA:
            for tamano in CELULARES:
                m = self.medidas[(nombre, *tamano)]
                with self.subTest(pagina=nombre, tamano=tamano):
                    self.assertIsNone(m["boton"])
                    self.assertEqual(m["fijas"], [], "con el enlace del hero a la vista la barra fija no sale")

    def test_sin_scroll_horizontal_de_320_a_1920(self):
        for nombre in {**VENTA, **LECTURA}:
            for ancho in ANCHOS:
                with self.subTest(pagina=nombre, ancho=ancho):
                    self.assertLessEqual(self.medidas[nombre, ancho, 900]["sobra"], 0)

    def test_axe_sin_violaciones_serias(self):
        for nombre, violaciones in self.axe.items():
            with self.subTest(pagina=nombre):
                self.assertEqual(violaciones, [])


if __name__ == "__main__":
    unittest.main()
