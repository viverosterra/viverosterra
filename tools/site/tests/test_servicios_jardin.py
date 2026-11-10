"""Diseño, mantenimiento y riego salen de la plantilla de servicio (Etapa 2c): secuencia del spec §3.3, un mensaje de
WhatsApp por plan, precios de datos.py, garantía condicionada, visita con su costo según la ubicación y JSON-LD de lo
visible. Cada página migrada agrega su fila a ESPERADO y su clase de pruebas propia."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import componentes  # noqa: E402
import datos  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

P = datos.PRECIOS
# SEO fase 1: el speakable ya no es un nodo suelto (va dentro del WebPage) y entidad.completar cierra el grafo con el
# WebPage y los nodos mínimos del negocio (GardenStore + LocalBusiness) y del sitio.
BASE_LD = {"Service", "FAQPage", "BreadcrumbList", "WebPage", "GardenStore", "LocalBusiness", "WebSite"}
# ruta, secciones propias de la página (entre opciones y la objeción), cifras visibles y tipos del JSON-LD.
ESPERADO = {
    "diseno": {"ruta": "/diseno-jardines-tampico", "extra": (), "ld": BASE_LD,
               "cifras": ("$3,000", "$6,500", "desde $18,000", "en proyectos de más de $150,000")},
    "mantenimiento": {"ruta": "/mantenimiento-jardines-tampico", "extra": ('id="vt-h-incluye"',), "ld": BASE_LD,
                      "cifras": ("$750", datos.SEGUN_COTIZACION)},
    "riego": {"ruta": "/sistema-riego-tampico", "extra": ('id="vt-h-precio"',), "ld": BASE_LD | {"HowTo"},
              "cifras": ("$180", "$320", "$18,000 a $32,000", datos.RIEGO_AHORRO)},
}


def pagina(clave):
    html = (paginas.PUBLIC / ESPERADO[clave]["ruta"].strip("/") / "index.html").read_text(encoding="utf-8")
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
    return html, main, textos_publicos(html), grafo


def mensajes_de(html, patron):
    """Textos de WhatsApp (con la firma) de los enlaces cuyo data-cta coincide con el patrón."""
    return [unquote(t) for t in re.findall(rf'data-cta="{patron}" href="https://wa\.me/\d+\?text=([^"]+)"', html)]


def opiniones_textuales(caso, clave, opiniones):
    _h, main, _t, _g = pagina(clave)
    prueba = main[main.index('id="vt-h-prueba"'):main.index('id="vt-h-opciones"')]
    for cita, nombre, detalle in opiniones:
        with caso.subTest(pagina=clave, nombre=nombre):
            caso.assertIn(f"<p>“{cita}”</p>", prueba)
            caso.assertIn(f"<b>{nombre}</b><span>{detalle}</span>", prueba)


class ComunTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        inicio = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', ':hero"', 'id="vt-h-prueba"', 'id="vt-h-opciones"')
        final = ('id="vt-h-conviene"', 'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-pago"', 'id="vt-h-faq"',
                 'id="vt-h-cobertura"', 'id="vt-h-rel"', 'class="vt-cierre"')
        for clave, e in ESPERADO.items():
            _h, main, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                posiciones = [main.index(m) for m in inicio + e["extra"] + final]
                self.assertEqual(posiciones, sorted(posiciones))
                self.assertEqual(len(re.findall(r"<h1\b", main)), 1)
                self.assertEqual(main.count('class="vt-pasos"'), 1)  # un solo proceso (auditoría 02 en riego)

    def test_sin_css_viejo_formularios_ni_parches_de_servicios(self):
        for clave in ESPERADO:
            html, _m, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertNotRegex(html, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
                for viejo in ("svc-hero", "plan-pay", "<form", "sendWA", "sendRW", "sim-titulo", "<style"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_tres_opciones_cada_una_con_su_mensaje(self):
        for clave, e in ESPERADO.items():
            html, _m, _t, _g = pagina(clave)
            tipo = paginas.contexto(e["ruta"])["tipo"]
            with self.subTest(pagina=clave):
                self.assertEqual(len(set(mensajes_de(html, rf"{tipo}:opcion-\d"))), 3)

    def test_portada_cierre_menu_y_barra_con_el_mensaje_de_la_pagina(self):
        for clave, e in ESPERADO.items():
            html, _m, _t, _g = pagina(clave)
            tipo = paginas.contexto(e["ruta"])["tipo"]
            esperado = datos.con_firma(mensajes_paginas.SERVICIOS[e["ruta"]])
            for seccion in ("hero", "cierre", "barra", "header"):
                with self.subTest(pagina=clave, seccion=seccion):
                    self.assertEqual(mensajes_de(html, f"{tipo}:{seccion}")[0], esperado)

    def test_precios_de_datos(self):
        for clave, e in ESPERADO.items():
            _h, _m, texto, _g = pagina(clave)
            for cifra in e["cifras"]:
                with self.subTest(pagina=clave, cifra=cifra):
                    self.assertIn(cifra, texto)

    def test_copy_del_dueno(self):
        for clave in ESPERADO:
            _h, main, texto, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertIn(datos.PROMESA_COMPLETA, texto)
                self.assertIn(datos.ANTICIPO, texto)
                self.assertIn("mensualidades con tarjeta de crédito", texto)
                self.assertIn('href="/politicas#mensualidades"', main)
                self.assertNotRegex(texto, r"(?i)\bMSI\b|sin intereses|oasis|pagas cuando|liquida|visita\w*\W+"
                                           r"(?:\w+\W+){0,4}?(?:gratis|gratuit|sin costo)")

    def test_cifras_confirmadas_por_el_dueno(self):
        """Respuestas del dueño (2026-11-07): +200 proyectos B2B es cierto y vuelve; SENASICA y la amortización no."""
        for clave in ESPERADO:
            _h, main, texto, _g = pagina(clave)
            prueba = main[main.index('id="vt-h-prueba"'):main.index('id="vt-h-opciones"')]
            with self.subTest(pagina=clave):
                self.assertIn(f"{datos.PROYECTOS_B2B} proyectos B2B", prueba)
                self.assertNotRegex(texto, r"(?i)senasica|amortiza|se paga sol")

    def test_garantia_enlaza_sus_condiciones(self):
        for clave in ESPERADO:
            _h, main, _t, _g = pagina(clave)
            garantia = main[main.index('id="vt-h-garantia"'):main.index('id="vt-h-pago"')]
            with self.subTest(pagina=clave):
                self.assertRegex(garantia, r'href="/politicas(?:#garantia-plantas)?"')

    def test_json_ld_conservado_y_faq_de_lo_visible(self):
        for clave, e in ESPERADO.items():
            _h, main, _t, grafo = pagina(clave)
            nodos = {tipo: n for n in grafo for tipo in ([n["@type"]] if isinstance(n["@type"], str) else n["@type"])}
            visibles = [componentes.texto_plano(s) for s in re.findall(r"<summary>(.*?)</summary>", main)]
            with self.subTest(pagina=clave):
                self.assertEqual(set(nodos), e["ld"])
                self.assertEqual(nodos["WebPage"]["speakable"]["cssSelector"], ["[data-vt-respuesta]", ".vt-faq details p"])
                self.assertEqual(nodos["Service"]["provider"], {"@id": f"{datos.SITIO}/#negocio"})
                self.assertEqual([q["name"] for q in nodos["FAQPage"]["mainEntity"]], visibles)
                self.assertEqual(len(visibles), 8)


class DisenoTest(unittest.TestCase):
    def test_tres_planes_con_su_mensaje_y_mensualidad(self):
        html, main, texto, grafo = pagina("diseno")
        planes = mensajes_de(html, r"servicio-diseno:opcion-\d")
        for plan, precio in (("Esencial", "$3,000"), ("Completo", "$6,500"), ("Premium", "desde $18,000")):
            with self.subTest(plan=plan):
                self.assertTrue(any(m.startswith(f"Hola, me interesa el Plan Terra {plan} ({precio})") for m in planes))
        for linea in ("o en 3 mensualidades de ≈ $1,105 con tarjeta de crédito (total $3,315)",
                      "o en 6 mensualidades de ≈ $1,245 con tarjeta de crédito (total $7,468)",
                      "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)"):
            self.assertIn(linea, texto)
        self.assertEqual(main.count('class="vt-modo__mes"'), 3)
        self.assertIn("Compara los 3 planes en detalle", texto)
        ofertas = next(n for n in grafo if n["@type"] == "Service")["offers"]
        self.assertEqual([o["price"] for o in ofertas], [str(P["diseno"]), str(P["diseno_completo"]),
                                                         str(P["diseno_premium"])])

    def test_garantia_de_plantas_condicionada(self):
        _h, main, texto, _g = pagina("diseno")
        self.assertIn("las plantas que sembramos", main)
        self.assertIn('href="/politicas#garantia-plantas"', main)
        self.assertNotRegex(texto, r"(?i)gratuit")

    def test_opiniones_de_main_textuales(self):
        opiniones_textuales(self, "diseno", datos.OPINIONES_DISENO)

    def test_fotos_de_obras_terminadas(self):
        """Respuesta del dueño (2026-11-07): las fotos de diseño son proyectos de Terra terminados, no referencias."""
        _h, main, _t, _g = pagina("diseno")
        pies = re.findall(r"<figcaption><span><b>Fig\. (\d+)</b> · ([^<]+)</span><span>([^<]+)</span></figcaption>", main)
        self.assertEqual([n for n, _l, _e in pies], [f"{i:02d}" for i in range(1, 13)])
        for _n, _lugar, etapa in pies[:4]:  # las siguientes 8 son del mosaico, cada una con la etapa que capturó el dueño
            self.assertEqual(etapa, "Terminado")
        self.assertNotIn("Proyecto · referencia", main)


class MantenimientoTest(unittest.TestCase):
    def test_un_mensaje_por_plan(self):
        """Auditoría 02: los 4 CTA mandaban el mismo texto; ahora el plan elegido viaja al chat."""
        html, _m, texto, _g = pagina("mantenimiento")
        planes = mensajes_de(html, r"servicio-mantenimiento:opcion-\d")
        self.assertIn(f"Residencial básico (desde ${P['mantenimiento_mes']}/mes)", planes[0])
        # Respuesta del dueño (2026-11-07): el premium se cotiza; no hay "desde $1,800/mes".
        self.assertIn(f"Residencial premium ({datos.SEGUN_COTIZACION.lower()}", planes[1])
        self.assertIn(f"empresa o industria ({datos.SEGUN_COTIZACION.lower()})", planes[2])
        # Una sola redacción para lo que se cotiza: "Según cotización" (minúscula solo a media frase).
        self.assertNotRegex(texto, r"(?i)por cotizaci[oó]n")
        self.assertEqual(texto.count(datos.SEGUN_COTIZACION), 5, "etiqueta (1), tarjetas (2) y tabla (2)")
        self.assertNotIn("1,800", texto)
        self.assertIn("empresa o industria", planes[2])
        self.assertGreaterEqual(len(set(mensajes_de(html, r"servicio-mantenimiento:[a-z0-9-]+"))), 4)
        for frecuencia in datos.FRECUENCIAS_MANTENIMIENTO:
            self.assertIn(frecuencia, texto)

    def test_visita_con_costo_y_jardinero(self):
        _h, main, texto, _g = pagina("mantenimiento")
        self.assertIn('href="/politicas#garantia-plantas"', main)
        self.assertIn(datos.VISITA_COSTO, texto)
        self.assertIn("jardinero", texto.split("Preguntas")[0])  # auditoría 03: "jardinero Tampico"

    def test_opiniones_de_main_textuales(self):
        opiniones_textuales(self, "mantenimiento", datos.OPINIONES_MANTENIMIENTO)


class RiegoTest(unittest.TestCase):
    def test_un_mensaje_por_tipo_de_sistema(self):
        html, _m, texto, grafo = pagina("riego")
        sistemas = mensajes_de(html, r"servicio-riego:opcion-\d")
        self.assertIn("aspersores emergentes", sistemas[0])
        self.assertIn("goteo", sistemas[1])
        self.assertIn("campo deportivo", sistemas[2])
        self.assertNotIn("$15,000", texto)  # 100 m² × $180 = $18,000
        self.assertEqual(len(next(n for n in grafo if n["@type"] == "HowTo")["step"]), 5)

    def test_visita_con_costo_y_campos_deportivos(self):
        _h, _m, texto, _g = pagina("riego")
        self.assertIn(datos.VISITA_COSTO, texto)
        self.assertIn("campos deportivos con pasto natural", texto)  # decisión del dueño: sí es servicio
        # Respuesta del dueño (2026-11-07): "+200 sistemas de riego" es cierto y vuelve.
        self.assertIn(f"{datos.SISTEMAS_RIEGO} sistemas de riego", texto)

    def test_opiniones_de_main_textuales(self):
        opiniones_textuales(self, "riego", datos.OPINIONES_RIEGO)


if __name__ == "__main__":
    unittest.main()
