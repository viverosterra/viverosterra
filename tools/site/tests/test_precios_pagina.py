"""Plantilla precios (Etapa 2g): sin un número escrito a mano, la misma respuesta de pasto que la home y pasto en rollo,
materiales con las respuestas del dueño (2026-11-08), sin fecha de vigencia hasta que el dueño la confirme, anclas
estables, mensualidades con la fórmula oficial y el simulador, y garantías con condición."""
import ast
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402

P = datos.PRECIOS
HTML = (paginas.PUBLIC / "precios" / "index.html").read_text(encoding="utf-8")
FUENTES = [Path(__file__).resolve().parents[1] / p for p in
           ("contenido/precios.py", "contenido/lista_precios.py", "contenido/zona.py", "plantillas/precios.py",
            "plantillas/zona.py", "componentes_zonas.py")]


def literales(fuente):
    """Cadenas literales del código (sin docstrings, sin comentarios y sin el mapa PARIDAD, que nombra lo retirado)."""
    arbol = ast.parse(fuente.read_text(encoding="utf-8"))
    fuera = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef)) and ast.get_docstring(nodo) is not None:
            fuera.add(id(nodo.body[0].value))
        if isinstance(nodo, ast.Assign) and any(getattr(t, "id", "") == "PARIDAD" for t in nodo.targets):
            fuera.update(id(n) for n in ast.walk(nodo.value))
    return [n.value for n in ast.walk(arbol)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in fuera]


def grafo():
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))["@graph"]


class PreciosTest(unittest.TestCase):
    def test_registrada_con_su_plantilla_y_su_hoja(self):
        self.assertIn(("/precios", "precios/index.html", "precios", "precios"), generar.PAGINAS)
        self.assertIn('<body class="vt-pagina vt-precios">', HTML)
        self.assertIn("/css/terra-precios.", HTML)
        for viejo in ("tienda-pasto.css", "fonts.googleapis", "hub-hero"):
            self.assertNotIn(viejo, HTML)

    def test_ningun_precio_escrito_a_mano_en_el_codigo(self):
        """Aceptación de la hoja de ruta: los números salen de datos.py, data.py o mensualidades.py."""
        for fuente in FUENTES:
            with self.subTest(fuente=fuente.name):
                self.assertEqual([t for t in literales(fuente) if re.search(r"\$\s?\d", t)], [])

    def test_misma_respuesta_de_pasto_que_home_y_pasto_en_rollo(self):
        faq = next(n for n in grafo() if n["@type"] == "FAQPage")
        self.assertEqual(faq["mainEntity"][0]["name"], "¿Cuánto cuesta el pasto en rollo en Tampico?")
        self.assertEqual(faq["mainEntity"][0]["acceptedAnswer"]["text"], datos.RESPUESTA_PRECIO_PASTO)

    def test_sin_fecha_de_vigencia_hasta_que_el_dueno_la_confirme(self):
        """Pregunta pendiente al dueño: ni "vigente desde" ni el "septiembre 2026" de main, tampoco en el JSON-LD."""
        self.assertNotRegex(paridad.texto(HTML), r"(?i)vigente desde|actualizada en|(?:septiembre|noviembre) 2026")
        pagina = next(n for n in grafo() if n["@type"] == "WebPage")
        self.assertNotIn("dateModified", pagina)

    def test_materiales_con_las_respuestas_del_dueno(self):
        """Tierra preparada, camiones de 5, 8 y 14 m³ y mármol con el precio de datos.py; piedra bola a granel según
        cotización; condiciones de compra del dueño; sin las medidas ni el peso que publicaba main."""
        seccion = HTML.split('id="materiales"', 1)[1].split('id="plantas"', 1)[0]
        for m3, precio in datos.TIERRA_CAMIONES:
            with self.subTest(camion=m3):
                self.assertIn(f'<td class="vt-tabla__u">camión de {m3} m³</td><td class="vt-tabla__p">{dinero(precio)}</td>',
                              seccion)
        self.assertRegex(seccion, r'Tierra preparada.{0,200}costal</td><td class="vt-tabla__p">'
                         + re.escape(dinero(P["tierra_preparada_costal"])))
        self.assertRegex(seccion, re.escape(datos.MARMOL_CONDICION) + r'.{0,120}saco</td><td class="vt-tabla__p">'
                         + re.escape(dinero(P["marmol_saco"])))
        self.assertIn('<td class="vt-tabla__u">a granel</td><td class="vt-tabla__p vt-tabla__p--cotiza">'
                      f'{datos.SEGUN_COTIZACION}</td>', seccion)
        self.assertRegex(seccion, r'Tezontle rojo.{0,200}costal</td><td class="vt-tabla__p"><small>desde</small>'
                         + re.escape(dinero(P["tezontle_costal"])))
        self.assertIn(datos.CONDICIONES_MATERIALES, paridad.texto(seccion))
        for retirado in ("Chica, mediana y grande", "Saco de unos 20 kg", "20 kg", "por medida", "camión desde"):
            with self.subTest(retirado=retirado):
                self.assertNotIn(retirado, HTML)

    def test_anclas_estables(self):
        for ancla in ("pasto", "servicios", "sintetico", "materiales", "plantas", "mensualidades", "garantias",
                      "garantia-pasto", "garantia-plantas", "preguntas"):
            with self.subTest(ancla=ancla):
                self.assertEqual(HTML.count(f'id="{ancla}"'), 1)
        self.assertIn('href="#pasto"', HTML)

    def test_mensualidades_con_simulador_y_contado_sin_recargo(self):
        self.assertIn("tarjeta en una sola exhibición) es el precio más bajo", HTML)
        self.assertIn('<script src="/js/vt-mensualidades.js" defer></script>', HTML)
        self.assertIn('<script src="/js/vt-simulador.js" defer></script>', HTML)
        self.assertIn('data-simulador data-servicio="mi jardín"', HTML)
        self.assertIn('href="/politicas#mensualidades"', HTML)
        self.assertIn(datos.ANTICIPO, HTML)
        self.assertNotRegex(HTML.lower(), r"\brecargo|meses sin|sin intereses|\bmsi\b")

    def test_catalogo_sin_precios_sin_confirmar(self):
        catalogo = next(n for n in grafo() if n["@type"] == "OfferCatalog")
        nombres = [o["name"] for o in catalogo["itemListElement"]]
        self.assertFalse(any("Piedra" in n for n in nombres))
        marmol = next(o for o in catalogo["itemListElement"] if o["name"].startswith("Mármol"))
        self.assertEqual(marmol["price"], str(P["marmol_saco"]))
        tezontle = next(o for o in catalogo["itemListElement"] if o["name"].startswith("Tezontle"))
        self.assertEqual(tezontle["priceSpecification"]["minPrice"], datos.PRECIOS["tezontle_costal"])
        self.assertNotIn("InStock", HTML)

    def test_garantias_con_su_condicion(self):
        self.assertIn("en las plantas que sembramos nosotros", HTML)
        self.assertIn("siguiendo el protocolo de riego.<", HTML)


if __name__ == "__main__":
    unittest.main()
