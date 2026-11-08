"""El blog en un navegador real (Etapa 2h): sin desbordar, consola limpia, preguntas con <details>, índice que lleva a su título y
WhatsApp firmado."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
from contenido import articulo  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

MUESTRA = ("palma-areca-tampico", "cuanto-cuesta-jardin-tampico-precios", "jardines-temporada-lluvias-tampico",
           "cuando-regar-pasto-san-agustin-tampico")
# El body recorta con overflow-x y scrollWidth no ve lo que se sale: se mide cada caja visible del <main> y cada renglón de
# texto (una palabra larga se sale de su caja sin agrandarla). Lo que vive dentro de un contenedor con scroll propio no se
# corta, se desplaza; ese contenedor sí se mide.
SALIDOS_DEL_MAIN = """() => {
  const ancho = document.documentElement.clientWidth;
  const conScroll = (e) => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
    if (['auto', 'scroll'].includes(getComputedStyle(p).overflowX)) return true; } return false; };
  const fuera = (c) => c.width > 0 && c.height > 0 && (c.right > ancho + 0.5 || c.left < -0.5);
  const main = document.querySelector('main');
  const salidos = Array.from(main.querySelectorAll('*'))
    .filter((e) => getComputedStyle(e).visibility !== 'hidden' && !conScroll(e) && fuera(e.getBoundingClientRect()))
    .map((e) => e.tagName + '.' + e.className + ' ' + e.textContent.trim().slice(0, 40));
  const rango = document.createRange();
  const textos = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  while (textos.nextNode()) {
    const nodo = textos.currentNode;
    if (!nodo.textContent.trim() || conScroll(nodo.parentElement)) continue;
    rango.selectNodeContents(nodo);
    if (Array.from(rango.getClientRects()).some(fuera)) salidos.push('texto: ' + nodo.textContent.trim().slice(0, 40));
  }
  return salidos;
}"""
# Dentro de su caja: tablas envueltas, cada celda con su texto, y notas, respuesta y CTA sin texto que rebase el recuadro.
TABLAS_Y_RECUADROS = """() => {
  const malos = [];
  const main = document.querySelector('main');
  main.querySelectorAll('table').forEach((t) => {
    const envoltura = t.parentElement;
    if (!envoltura.matches('.vt-art__tabla') || getComputedStyle(envoltura).overflowX !== 'auto') malos.push('tabla sin envoltura');
    if (envoltura.scrollWidth > envoltura.clientWidth + 1 && envoltura.getAttribute('tabindex') !== '0') malos.push('tabla con scroll sin teclado');
  });
  const rango = document.createRange();
  main.querySelectorAll('th, td, .vt-art__nota, .vt-art__respuesta, .vt-art__producto .vt-btn, .vt-etiqueta, .vt-art__rel li').forEach((caja) => {
    const borde = caja.getBoundingClientRect();
    const textos = document.createTreeWalker(caja, NodeFilter.SHOW_TEXT);
    while (textos.nextNode()) {
      if (!textos.currentNode.textContent.trim()) continue;
      rango.selectNodeContents(textos.currentNode);
      for (const r of rango.getClientRects()) {
        if (r.width && (r.right > borde.right + 0.5 || r.left < borde.left - 0.5)) malos.push(caja.tagName + ': ' + textos.currentNode.textContent.trim().slice(0, 40));
      }
    }
  });
  return malos;
}"""


@unittest.skipIf(sync_playwright is None, "sin playwright")
class BlogNavegadorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.srv = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.nav = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.nav.close()
        cls.pw.stop()
        cls.srv.shutdown()

    def test_sin_desbordar_a_320_375_y_768(self):
        anchas = []
        for ancho in (320, 375, 768):
            pagina = self.nav.new_page(viewport={"width": ancho, "height": 800})
            for ruta in ("/blog/",) + tuple(f"/blog/{slug}/" for slug in articulo.CLAVES):
                pagina.goto(f"{self.base}{ruta}", wait_until="load")
                sobra = pagina.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if sobra > 1:
                    anchas.append(f"{ruta}@{ancho}: {sobra}px")
                anchas += [f"{ruta}@{ancho}: {x}" for x in pagina.evaluate(SALIDOS_DEL_MAIN)]
                anchas += [f"{ruta}@{ancho}: {x}" for x in pagina.evaluate(TABLAS_Y_RECUADROS)]
            pagina.close()
        self.assertEqual(anchas, [])

    def test_la_medida_ve_lo_que_el_body_recorta(self):
        pagina = self.nav.new_page(viewport={"width": 320, "height": 800})
        pagina.goto(f"{self.base}/blog/palma-areca-tampico/", wait_until="load")
        self.assertEqual(pagina.evaluate(SALIDOS_DEL_MAIN), [])
        pagina.evaluate("""() => { const p = document.createElement('p'); p.style.whiteSpace = 'nowrap';
          p.textContent = 'renglon que no cabe '.repeat(12); document.querySelector('main article').prepend(p); }""")
        self.assertTrue(pagina.evaluate(SALIDOS_DEL_MAIN))
        pagina.close()

    def test_foto_del_articulo_con_el_recorte_de_produccion(self):
        for ancho, alto in ((375, 256), (768, 320), (1440, 320)):
            pagina = self.nav.new_page(viewport={"width": ancho, "height": 900})
            pagina.goto(f"{self.base}/blog/palmas-mas-vendidas-tampico-precios/", wait_until="load")
            caja = pagina.evaluate("""() => { const i = document.querySelector('.vt-art__cuerpo img');
              return [Math.round(i.getBoundingClientRect().height), getComputedStyle(i).objectFit]; }""")
            self.assertEqual(caja, [alto, "cover"], f"a {ancho}px")
            pagina.close()

    def test_el_cordel_de_la_etiqueta_no_cruza_el_texto(self):
        for ancho in (320, 375, 768):
            pagina = self.nav.new_page(viewport={"width": ancho, "height": 900})
            pagina.goto(f"{self.base}/blog/pasto-san-agustin-instalacion-mantenimiento/", wait_until="load")
            aire = pagina.evaluate("""() => {
              const marco = document.querySelector('.vt-art__producto .vt-etiqueta-x--cordel');
              const cordel = getComputedStyle(marco, '::before');
              const arriba = marco.getBoundingClientRect().bottom - parseFloat(cordel.bottom) - parseFloat(cordel.height);
              return arriba - document.querySelector('.vt-art__producto .vt-promesa').getBoundingClientRect().bottom; }""")
            self.assertGreaterEqual(aire, 8, f"a {ancho}px")
            pagina.close()

    def test_las_migas_no_se_pegan_a_la_etiqueta_de_categoria(self):
        for ruta in ("/blog/", "/blog/palma-areca-tampico/"):
            pagina = self.nav.new_page(viewport={"width": 375, "height": 812})
            pagina.goto(self.base + ruta, wait_until="load")
            aire = pagina.evaluate("""() => document.querySelector('main .vt-kicker').getBoundingClientRect().top
              - document.querySelector('main .vt-crumbs').getBoundingClientRect().bottom""")
            self.assertGreaterEqual(aire, 12, ruta)
            pagina.close()

    def test_consola_limpia_en_el_indice_y_la_muestra(self):
        errores = []
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.on("console", lambda m: errores.append(m.text) if m.type == "error" and "googletagmanager" not in m.text else None)
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        for ruta in ("/blog/",) + tuple(f"/blog/{s}/" for s in MUESTRA):
            pagina.goto(self.base + ruta, wait_until="load")
        pagina.close()
        self.assertEqual(errores, [])

    def test_indice_lleva_al_titulo_y_preguntas_abren(self):
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.goto(f"{self.base}/blog/palma-areca-tampico/", wait_until="load")
        pagina.locator('.vt-art__indice a[href="#cuidados"]').click()
        pagina.wait_for_function("() => location.hash === '#cuidados'")
        top = pagina.evaluate("() => document.getElementById('cuidados').getBoundingClientRect().top")
        self.assertGreaterEqual(top, 60)
        segunda = pagina.locator(".vt-faq details").nth(1)
        segunda.locator("summary").click()
        self.assertEqual(segunda.get_attribute("open"), "")
        pagina.close()

    def test_whatsapp_del_cierre_firmado_y_con_el_mensaje_del_articulo(self):
        pagina = self.nav.new_page(viewport={"width": 1440, "height": 900})
        pagina.goto(f"{self.base}/blog/palma-areca-tampico/", wait_until="load")
        href = pagina.locator('[data-cta="blog:cierre"]').first.get_attribute("href")
        self.assertIn("viverosterra.com", href)
        self.assertIn("Palma%20Areca", href)
        pagina.close()


if __name__ == "__main__":
    unittest.main()
