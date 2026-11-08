"""Las 25 páginas de pasto sintético publicadas desde sus plantillas: secuencia del spec §3.3, sin CSS viejo, scripts de
la tienda, precio en el primer pantallazo, existencia, JSON-LD y reglas del dueño en lo que cambió en 2b."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
TIENDA = [r for r, _a, p, _c in generar.PAGINAS if r.startswith("/pasto-sintetico")]
VIEJOS = ("tienda-pasto.css", "fonts.googleapis", "tailwind.css", "design-system.css", "legacy-fixes", "Geist",
          "Instrument Serif")


def html(ruta):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def principal(texto):
    return re.search(r"<main\b[^>]*>(.*)</main>", texto, re.S).group(1)


def grafo(texto):
    return [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', texto, re.S)
            for n in json.loads(b)["@graph"]]


class TiendaPublicadaTest(unittest.TestCase):
    def test_sin_css_viejo_con_terra_tienda(self):
        for ruta in TIENDA:
            texto = html(ruta)
            with self.subTest(ruta=ruta):
                for viejo in VIEJOS:
                    self.assertNotIn(viejo, texto)
                self.assertIn('<body class="vt-pagina vt-tienda">', texto)
                self.assertRegex(texto, r'<link rel="stylesheet" href="/css/terra-tienda\.[0-9a-f]{10}\.css">')
                self.assertNotIn("<style", texto)

    def test_ficha_con_etiqueta_existencia_y_galeria_precargada(self):
        for m in data.MODELOS:
            texto = html(f"/pasto-sintetico/{m['slug']}")
            cuerpo = principal(texto)
            with self.subTest(modelo=m["slug"]):
                self.assertIn(f"Rollo de 50 m² · desde</small><b>${m['rollo']}</b>", cuerpo)
                self.assertIn("por rollo, según tu estado", cuerpo)
                self.assertIn("En existencia", cuerpo)
                self.assertEqual("para llevar hoy" in cuerpo, bool(m["stock"]))
                primera = f"/img/pasto-sintetico/galeria/{m['slug']}-{m['gallery'][0][0]}-sm.webp"
                self.assertIn(f'<link rel="preload" as="image" href="{primera}"', texto)
                self.assertRegex(cuerpo, rf'<img src="{re.escape(primera)}"[^>]*loading="eager" fetchpriority="high"')
                self.assertLess(cuerpo.index("vt-etiqueta__precio"), cuerpo.index("vt-galeria"))
                self.assertIn(f'data-landed-slug="{m["slug"]}"', cuerpo)

    def test_secuencia_de_la_ficha(self):
        cuerpo = principal(html("/pasto-sintetico/toscana-28"))
        orden = ['id="vt-h1"', 'class="vt-galeria"', 'id="comprar"', "Para quién es el Toscana 28",
                 "Ficha técnica del Toscana 28", 'class="vt-fig vt-rollo"', "Compara el Toscana 28",
                 "El envío se cobra por rollo", "Garantía de 5 años en el Toscana 28", "Preguntas sobre el Toscana 28",
                 "vt-cierre"]
        posiciones = [cuerpo.index(x) for x in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_feed_de_merchant_sin_cambios_de_precio(self):
        feed = (PUBLIC / "feed-pasto-sintetico.xml").read_text(encoding="utf-8")
        for m in data.MODELOS:
            self.assertIn(f"<g:link>{data.SITE}/pasto-sintetico/{m['slug']}</g:link>", feed)
            self.assertIn(f"<g:price>{m['rollo']:.2f} MXN</g:price>", feed)

    def test_scripts_de_la_ficha_en_orden(self):
        self.assertEqual(re.findall(r'<script src="/js/([\w-]+)\.js" defer>', html("/pasto-sintetico/toscana-28")),
                         ["vt-mensualidades", "tienda-pasto", "vt-landed"])

    def test_hub_con_precio_puesto_catalogo_y_lista(self):
        texto = html("/pasto-sintetico")
        cuerpo = principal(texto)
        self.assertIn('data-landed-hero data-rollo="139"', cuerpo)
        self.assertIn('id="hero-estado"', cuerpo)
        self.assertEqual(cuerpo.count('class="spec-card vt-tarjeta-p"'), 9)
        self.assertIn('id="vt-models"', texto)
        self.assertIn('<dialog class="vt-lista" id="cotizacion"', texto)
        self.assertNotIn("gratis", cuerpo.lower())
        lista = next(n for n in grafo(texto) if n["@type"] == "ItemList")
        self.assertEqual(len(lista["itemListElement"]), 9)

    def test_vendemos_a_todo_mexico_desde_2012(self):
        self.assertIn(f"desde {datos.SINTETICO_NACIONAL_DESDE}", principal(html("/pasto-sintetico")))

if __name__ == "__main__":
    unittest.main()
