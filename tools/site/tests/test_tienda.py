"""Las 25 páginas de pasto sintético publicadas desde sus plantillas: secuencia del spec §3.3, sin CSS viejo, scripts de
la tienda, precio en el primer pantallazo, existencia, JSON-LD y reglas del dueño en lo que cambió en 2b."""
import html as html_mod
import itertools
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
                self.assertIn(f'Rollo de 50 <span class="vt-u">m²</span> · desde</small><b>${m["rollo"]}</b>', cuerpo)
                self.assertIn("por rollo, según tu estado", cuerpo)
                self.assertIn("En existencia", cuerpo)
                self.assertEqual("para llevar hoy" in cuerpo, bool(m["stock"]))
                primera = f"/img/pasto-sintetico/galeria/{m['slug']}-{m['gallery'][0][0]}-sm.webp"
                self.assertIn(f'<link rel="preload" as="image" href="{primera}"', texto)
                self.assertRegex(cuerpo, rf'<img src="{re.escape(primera)}"[^>]*loading="eager" fetchpriority="high"')
                self.assertLess(cuerpo.index("vt-etiqueta__precio"), cuerpo.index("vt-galeria"))
                self.assertIn(f'data-landed-slug="{m["slug"]}"', cuerpo)

    def test_miniaturas_de_la_galeria_ligeras_y_publicadas(self):
        # Las miniaturas se ven a 64 px: van las de 128 px de tools/site/miniaturas.py, no la copia -sm de 420 px.
        for m in data.MODELOS:
            minis = re.findall(r'class="vt-galeria__mini"[^>]*><img src="([^"]+)"', principal(html(f"/pasto-sintetico/{m['slug']}")))
            with self.subTest(modelo=m["slug"]):
                self.assertEqual(len(minis), len(m["gallery"]))
                for src in minis:
                    self.assertTrue(src.endswith("-mini.webp"), src)
                    self.assertTrue((PUBLIC / src.lstrip("/")).is_file(), src)

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

    def test_hub_con_precio_puesto_catalogo_y_lista(self):
        texto = html("/pasto-sintetico")
        cuerpo = principal(texto)
        self.assertIn('data-landed-hero data-rollo="139"', cuerpo)
        self.assertIn('id="hero-estado"', cuerpo)
        self.assertEqual(cuerpo.count('class="spec-card vt-tarjeta-p"'), 9)
        self.assertIn('id="vt-models"', texto)
        self.assertIn('<dialog class="vt-lista" id="cotizacion"', texto)
        self.assertNotIn("gratis", cuerpo.lower())
        self.assertIn('<p class="vt-enlace-sec"><a href="#modelos">Ver los 9 modelos</a></p>', cuerpo)
        lista = next(n for n in grafo(texto) if n["@type"] == "ItemList")
        self.assertEqual(len(lista["itemListElement"]), 9)

    def test_vendemos_a_todo_mexico_desde_2012(self):
        self.assertIn(f"desde {datos.SINTETICO_NACIONAL_DESDE}", principal(html("/pasto-sintetico")))
    def test_ciudad_con_respuesta_tabla_y_encabezados_en_pregunta(self):
        texto = html("/pasto-sintetico/envio/monterrey")
        cuerpo = principal(texto)
        for pregunta in ("¿Cuánto cuesta el envío a Monterrey?", "¿Cuánto tarda en llegar a Monterrey?",
                         "¿Cuánto es lo mínimo que puedo pedir a Monterrey?",
                         "¿Cómo elijo el modelo para Monterrey sin ver una muestra?", "¿Quién lo instala en Monterrey?"):
            self.assertIn(f"<h3>{pregunta}</h3>", cuerpo)
        # Los números de la ciudad: flete de su zona, 1 y 2 rollos, su modelo recomendado y el mínimo con envío.
        for dato in ("el flete es de $1,150 por rollo de 50 m²", "$2,300 de flete", "Con Irlanda 25",
                     f"{data.MIN_NACIONAL_M2} m², medio rollo: con Aruba 10"):
            self.assertIn(dato, cuerpo)
        # Las fichas de los modelos recomendados abren con el estado de la ciudad.
        self.assertIn('href="/pasto-sintetico/irlanda-25?estado=nuevo-leon"', cuerpo)
        self.assertIn("<b>$162/m²</b>", cuerpo)
        self.assertIn("12 × ≈ $1,667", cuerpo)
        self.assertIn('href="/pasto-sintetico?estado=nuevo-leon#cotizador"', cuerpo)
        productos = [n for n in grafo(texto) if n["@type"] == "Product"]
        self.assertEqual(productos[0]["offers"]["shippingDetails"]["shippingRate"]["value"], "1150")

    def test_ciudades_sin_casi_duplicados(self):
        """Similitud media de 5-gramas (Jaccard) del texto de <main> entre las 11 ciudades: 0.37 en main, 0.44 antes de
        hacer propias las preguntas de envío; falla arriba de 0.47."""
        def shingles(ruta):
            texto = html_mod.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ",
                                                                      principal(html(ruta)), flags=re.S))).lower()
            palabras = re.findall(r"\w+", texto)
            return {tuple(palabras[i:i + 5]) for i in range(len(palabras) - 4)}

        ciudades = [shingles(r) for r in TIENDA if r.startswith("/pasto-sintetico/envio/")]
        self.assertEqual(len(ciudades), 11)
        pares = [len(a & b) / len(a | b) for a, b in itertools.combinations(ciudades, 2)]
        self.assertLessEqual(sum(pares) / len(pares), 0.47)

    def test_ciudades_sin_pregunta_de_tiempo_repetida(self):
        for ruta in (r for r in TIENDA if r.startswith("/pasto-sintetico/envio/")):
            with self.subTest(ruta=ruta):
                self.assertLessEqual(len(re.findall(r"¿Cuánto tarda en llegar a", principal(html(ruta)))), 1)

    def test_perros_sin_el_precio_del_aruba(self):
        cuerpo = principal(html("/pasto-sintetico/perros"))
        self.assertIn("<b>$149/m²</b> con Toscana 18", cuerpo)
        self.assertNotIn("$139", cuerpo)
        self.assertNotIn("muestra", cuerpo.lower())
        self.assertIn('href="/blog/pasto-sintetico-para-perros"', cuerpo)
    def test_veinticinco_paginas_de_sintetico_con_plantilla(self):
        self.assertEqual(len(TIENDA), 1 + 1 + 1 + len(data.MODELOS) + 11)

    def test_scripts_en_orden(self):
        esperado = {"/pasto-sintetico": ["vt-mensualidades", "tienda-pasto", "vt-landed", "tienda-hub"],
                    "/pasto-sintetico/toscana-28": ["vt-mensualidades", "tienda-pasto", "vt-landed"],
                    "/pasto-sintetico/envio/cdmx": ["vt-mensualidades", "tienda-pasto", "vt-landed"],
                    "/pasto-sintetico-tampico": ["vt-mensualidades", "tienda-pasto"]}
        for ruta, scripts in esperado.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(re.findall(r'<script src="/js/([\w-]+)\.js" defer>', html(ruta)), scripts)

    def test_tampico_con_opciones_cotizador_y_showroom(self):
        texto = html("/pasto-sintetico-tampico")
        cuerpo = principal(texto)
        self.assertIn("los otros 7 modelos también están en existencia", cuerpo)
        self.assertIn('id="showroom"', cuerpo)
        self.assertIn('<option value="showroom" selected>', cuerpo)
        self.assertEqual(cuerpo.count('<li class="vt-modo'), 2)
        # Decisión del dueño (2026-11-07): el testimonio de Sofía R. es real y publicado con permiso; se conserva textual.
        self.assertIn("Los clientes preguntan si es natural.”", cuerpo)
        self.assertIn("<b>Sofía R.</b><span>Cafetería en el centro de Tampico</span>", cuerpo)
        tipos = {t for n in grafo(texto) for t in ([n["@type"]] if isinstance(n["@type"], str) else n["@type"])}
        # Calculadora de venta local: showroom o envío local por colonia, sin los 32 estados ni flete por estado.
        self.assertIn('<select id="estado" data-local>', cuerpo)
        self.assertIn("envío local según tu colonia", cuerpo)
        self.assertIn(f"Material desde <b>${min(m['rollo'] for m in data.MODELOS)}</b>/m²", cuerpo)
        self.assertNotIn("envío por rollo según tu estado", cuerpo)
        # SEO fase 1: el negocio es la entidad única (GardenStore + LocalBusiness, nodo mínimo); ya no un Store propio.
        self.assertTrue({"LocalBusiness", "GardenStore", "Service", "FAQPage", "BreadcrumbList", "WebPage"} <= tipos)
        self.assertNotIn("Store", tipos)
        # Sin HowTo (es del pasto en rollo). Desde la fase 1 el speakable va dentro del WebPage, nunca suelto.
        self.assertFalse({"HowTo", "SpeakableSpecification"} & tipos)
        pagina = next(n for n in grafo(texto) if n["@type"] == "WebPage")
        self.assertEqual(pagina["speakable"]["cssSelector"], ["[data-vt-respuesta]"])

    def test_barras_fijas_que_no_se_tapan(self):
        for ruta in TIENDA:
            texto = html(ruta)
            buybar, barra = 'id="buybar"' in texto, "data-vt-bar" in texto
            with self.subTest(ruta=ruta):
                self.assertFalse(buybar and barra)
                self.assertTrue(buybar or barra)


if __name__ == "__main__":
    unittest.main()
