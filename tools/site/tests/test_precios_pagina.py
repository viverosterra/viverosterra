"""Plantilla precios (Etapa 2g): sin un número escrito a mano, la misma respuesta de pasto que la home y pasto en rollo,
materiales con las respuestas del dueño (2026-11-08), sin fecha de vigencia hasta que el dueño la confirme, anclas
estables, mensualidades con la fórmula oficial y el simulador, y garantías con condición."""
import ast
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402
import data  # noqa: E402  (tools/pasto, en sys.path gracias a componentes)

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
        """Pregunta pendiente al dueño: ni "vigente desde" ni el "septiembre 2026" de main. SEO fase 1 (2026-11-10): la
        página sí dice cuándo se revisaron los precios por última vez ("Actualizado: noviembre de 2026" y dateModified),
        con un dato versionado (datos.PRECIOS_ACTUALIZADOS), que no es una fecha de vigencia."""
        self.assertNotRegex(paridad.texto(HTML), r"(?i)vigente desde|actualizada en|(?:septiembre|noviembre) 2026")
        pagina = next(n for n in grafo() if n["@type"] == "WebPage")
        self.assertEqual(pagina["dateModified"], datos.PRECIOS_ACTUALIZADOS)
        self.assertEqual(datos.PRECIOS_ACTUALIZADOS, "2026-11-10")
        self.assertIn(f'<p class="vt-promesa">Actualizado: <time datetime="{datos.PRECIOS_ACTUALIZADOS}">noviembre de 2026'
                      "</time></p>", HTML)

    def test_materiales_con_las_respuestas_del_dueno(self):
        """Tierra preparada, camiones de 5, 8 y 14 m³ y mármol con el precio de datos.py; piedra bola a granel según
        cotización; condiciones de compra del dueño; sin las medidas ni el peso que publicaba main."""
        seccion = HTML.split('id="materiales"', 1)[1].split('id="plantas"', 1)[0]
        for m3, precio in datos.TIERRA_CAMIONES:
            with self.subTest(camion=m3):
                self.assertRegex(seccion, rf'Tierra negra vegetal · camión de {m3} m³</a>.{{0,200}}'
                                 rf'camión</td><td class="vt-tabla__p">{re.escape(dinero(precio))}</td>')
        self.assertRegex(seccion, r'Tierra preparada.{0,200}costal</td><td class="vt-tabla__p">'
                         + re.escape(dinero(P["tierra_preparada_costal"])))
        self.assertRegex(seccion, re.escape(datos.MARMOL_CONDICION) + r'.{0,120}saco</td><td class="vt-tabla__p">'
                         + re.escape(dinero(P["marmol_saco"])))
        self.assertIn('<td class="vt-tabla__u">a granel</td><td class="vt-tabla__p vt-tabla__p--cotiza">'
                      f'{datos.SEGUN_COTIZACION}</td>', seccion)
        self.assertRegex(seccion, r'Tezontle rojo.{0,200}costal</td><td class="vt-tabla__p"><small class="vt-tabla__desde">desde</small>'
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
        self.assertEqual(marmol["description"], datos.MARMOL_CONDICION)
        tezontle = next(o for o in catalogo["itemListElement"] if o["name"].startswith("Tezontle"))
        self.assertEqual(tezontle["priceSpecification"]["minPrice"], datos.PRECIOS["tezontle_costal"])
        self.assertNotIn("InStock", HTML)

    def test_lo_que_es_desde_va_con_minprice_y_sin_price(self):
        """Un price exacto en una oferta "desde" le diría a Google un precio cerrado que no existe."""
        catalogo = next(n for n in grafo() if n["@type"] == "OfferCatalog")
        ofertas = {o["name"]: o for o in catalogo["itemListElement"]}
        desde = {"Pasto San Agustín instalado": P["pasto_instalado_m2"], "Mantenimiento de jardín mensual": P["mantenimiento_mes"],
                 f"Pasto San Agustín al mayoreo, desde {P['pasto_mayoreo_minimo_m2']} m²": P["pasto_mayoreo_m2"],
                 "Diseño de jardín, Plan Terra Premium": P["diseno_premium"],
                 "Pasto sintético, material en rollo": min(m["rollo"] for m in data.MODELOS),
                 "Tezontle rojo, costal": P["tezontle_costal"], "Palmas, tamaño chico": P["palma_desde"]}
        for nombre, precio in desde.items():
            with self.subTest(nombre=nombre):
                self.assertNotIn("price", ofertas[nombre])
                self.assertEqual(ofertas[nombre]["priceSpecification"]["minPrice"], precio)
                self.assertNotIn("price", ofertas[nombre]["priceSpecification"])
        for nombre in ("Pasto San Agustín en rollo, solo el pasto", "Diseño de jardín, Plan Terra Esencial"):
            with self.subTest(nombre=nombre):
                self.assertIn("price", ofertas[nombre])

    def test_planes_de_diseno_dicen_lo_que_incluyen(self):
        """Plan Esencial: remoto, sin visita. Premium: se descuenta solo en proyectos grandes, con el umbral de datos.py."""
        seccion = paridad.texto(HTML.split('id="servicios"', 1)[1].split('id="sintetico"', 1)[0])
        self.assertIn("Propuesta visual remota con tus fotos y lista de plantas. Entrega en 3 a 5 días hábiles.", seccion)
        self.assertNotIn("Visita, propuesta", seccion)
        self.assertIn(f"Se descuenta en proyectos de más de {dinero(P['diseno_premium_descuento_desde'])}.", seccion)

    def test_indice_con_las_anclas_de_cada_seccion(self):
        nav = re.search(r'<nav class="vt-saltos".*?</nav>', HTML, re.S).group(0)
        self.assertEqual(re.findall(r'href="#([^"]+)"', nav),
                         ["pasto", "servicios", "sintetico", "materiales", "plantas", "mensualidades", "garantias"])
        self.assertLess(HTML.index('id="vt-h1"'), HTML.index('class="vt-saltos"'))
        self.assertLess(HTML.index('class="vt-saltos"'), HTML.index('id="pasto"'))

    def test_cada_seccion_cotiza_con_su_mensaje_y_se_mide(self):
        for seccion, siguiente in (("pasto", "servicios"), ("servicios", "sintetico"), ("sintetico", "materiales"),
                                   ("materiales", "plantas"), ("plantas", "mensualidades")):
            bloque = HTML.split(f'id="{seccion}"', 1)[1].split(f'id="{siguiente}"', 1)[0]
            mensajes = re.findall(rf'data-cta="precios:{seccion}"[^>]*href="https://wa\.me/\d+\?text=([^"]+)"', bloque)
            with self.subTest(seccion=seccion):
                self.assertEqual([unquote(m) for m in mensajes], [datos.con_firma(mensajes_paginas.PRECIOS_SECCIONES[seccion])])
        self.assertEqual(len(set(mensajes_paginas.PRECIOS_SECCIONES.values())), len(mensajes_paginas.PRECIOS_SECCIONES))

    def test_poda_pide_fotos_con_su_mensaje(self):
        m = re.search(r'data-cta="precios:poda"[^>]*href="https://wa\.me/\d+\?text=([^"]+)"[^>]*>Mándanos fotos', HTML)
        self.assertEqual(unquote(m.group(1)), datos.con_firma(mensajes_paginas.PRECIOS_SECCIONES["poda"]))

    def test_menu_y_barra_con_el_mensaje_de_la_portada(self):
        esperado = datos.con_firma(mensajes_paginas.PRECIOS)
        for lugar in ("hero", "header", "barra"):
            with self.subTest(lugar=lugar):
                m = re.search(rf'data-cta="precios:{lugar}"[^>]*href="https://wa\.me/\d+\?text=([^"]+)"', HTML)
                self.assertEqual(unquote(m.group(1)), esperado)

    def test_portada_enlaza_a_mensualidades_y_tabla_dice_compra_minima(self):
        self.assertIn('<a href="#mensualidades">Hasta 12 mensualidades con tarjeta · ver plazos</a>', HTML)
        self.assertIn('<th scope="col">Compra mínima</th>', HTML)
        self.assertNotIn("Desde (contado)", HTML)

    def test_garantias_con_su_condicion(self):
        self.assertIn("en las plantas que sembramos nosotros", HTML)
        self.assertIn("siguiendo el protocolo de riego.<", HTML)


if __name__ == "__main__":
    unittest.main()
