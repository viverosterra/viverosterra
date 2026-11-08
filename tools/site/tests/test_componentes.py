"""Componentes del cuerpo (tools/site/componentes.py): CTA, etiqueta, datos, figuras, tablas, proceso, FAQ y Medidor."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402


class UtilidadesTest(unittest.TestCase):
    def test_redondeo_igual_que_javascript(self):
        self.assertEqual([c.redondear(x) for x in (1102.5, 1103.5, 0.4)], [1103, 1104, 0])
        self.assertEqual(c.dinero(5760), "$5,760")
        self.assertEqual((c.formato_m2(48.0), c.formato_m2(1234.5)), ("48", "1,234.5"))

    def test_texto_plano_y_etiquetas_permitidas(self):
        self.assertEqual(c.texto_plano('Ver <a href="/x">la &amp; lista</a>\n hoy'), "Ver la & lista hoy")
        self.assertEqual(c.etiquetas_no_permitidas('<b>a</b> <a href="/x">b</a> <i>c</i>'), [])
        self.assertEqual(c.etiquetas_no_permitidas("<div><script>x</script></div>"), ["div", "script"])


class CtaTest(unittest.TestCase):
    def test_fila_de_cta_con_dos_textos_promesa_y_data_cta(self):
        html = c.fila_cta(datos.MENSAJES["general"], "home", "hero", hero=True)
        self.assertIn("data-hero-cta", html)
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["home:hero", "home:hero"])
        self.assertIn("Cotizar por WhatsApp", html)
        self.assertIn(f"Llamar {datos.TELEFONO_VISIBLE}", html)
        self.assertIn(datos.PROMESA_COMPLETA, html)
        texto = unquote(re.search(r'href="https://wa\.me/528333268008\?text=([^"]+)"', html).group(1))
        self.assertTrue(texto.endswith(datos.FIRMA))

    def test_sin_hero_no_marca_la_fila(self):
        self.assertNotIn("data-hero-cta", c.fila_cta("Hola", "home", "cierre"))


class BloquesTest(unittest.TestCase):
    def test_cuadro_de_datos_oficial(self):
        html = c.cuadro_datos()
        for dato in (f"REPSE {datos.REPSE}", datos.FACTURA, str(datos.DESDE), "Obregón 209 Sur", datos.M2_INSTALADOS):
            self.assertIn(dato, html)

    def test_figura_con_pie_y_carga(self):
        f = {"src": "/img/a.webp", "ancho": 10, "alto": 20, "alt": "Foto \"real\"", "numero": 3, "lugar": "Madero",
             "etapa": "Después"}
        self.assertIn('loading="lazy"', c.figura(f))
        principal = c.figura(f, principal=True)
        self.assertIn('loading="eager" fetchpriority="high"', principal)
        self.assertIn("<b>Fig. 03</b> · Madero", principal)
        self.assertIn('alt="Foto &quot;real&quot;"', principal)

    def test_logos_son_los_clientes_autorizados(self):
        self.assertEqual(tuple(n for n, *_ in c.LOGOS), datos.CLIENTES_B2B)
        for _nombre, archivo, _a, _h, _escala in c.LOGOS:
            if archivo is None:
                continue
            self.assertTrue((Path(__file__).resolve().parents[3] / "public" / "img" / "clientes" / f"{archivo}-c.webp")
                            .is_file(), archivo)

    def test_cliente_sin_logo_va_con_su_nombre_en_texto(self):
        html = c.logos()
        self.assertIn('<li class="vt-logos__nombre">Renault</li>', html)
        self.assertNotIn('alt="Renault"', html)
        self.assertEqual(html.count("<img"), 6)

    def test_flex_y_velamar_se_leen(self):
        """Gate de diseño 2a: el logo de Flex va recortado a su palabra y el de Velamar, más alto."""
        flex = next(l for l in c.LOGOS if l[0] == "Flex")
        self.assertGreater(flex[2] / flex[3], 3)
        self.assertIn('<li class="vt-logos--alto"><img src="/img/clientes/logo-velamar-c.webp"', c.logos())

    def test_testimonios_con_nombre_y_servicio(self):
        html = c.testimonios((("Quedó muy bien.", "Ana Pérez", "Pasto · Tampico"),))
        self.assertIn('<blockquote><p>“Quedó muy bien.”</p></blockquote>', html)
        self.assertIn('<li class="vt-testimonios__dest">', html)  # la primera va destacada
        self.assertIn("<figcaption><b>Ana Pérez</b><span>Pasto · Tampico</span></figcaption>", html)

    def test_tabla_de_precios_con_unidad_y_desde(self):
        html = c.tabla_precios([{"nombre": "Pasto", "detalle": "d", "unidad": "/m²", "precio": 120, "desde": True,
                                 "rec": True}], "Precios")
        self.assertIn('<th scope="col">Unidad</th>', html)
        self.assertIn('<td class="vt-tabla__u">/m²</td>', html)
        self.assertIn("<small>desde</small><span>$120</span>", html)

    def test_pasos_con_marcadores(self):
        html = c.pasos([{"titulo": "Riego", "quien": "tu", "cuando": "Día 1", "texto": "t"},
                        {"titulo": "Poda", "quien": "juntos", "cuando": "Día 21", "texto": "t"}])
        self.assertIn('<span class="vt-quien vt-quien--tu">Tú</span>', html)
        self.assertIn('<span class="vt-quien vt-quien--juntos">Juntos</span>', html)

    def test_faq_y_su_json_ld_dicen_lo_mismo(self):
        preguntas = (("¿Uno?", 'Sí, <a href="/x">mira</a>.'), ("¿Dos?", "No."))
        html = c.faq(preguntas)
        self.assertEqual(html.count("<details"), 2)
        self.assertEqual(html.count("<details open>"), 1)
        nodo = c.faq_jsonld(preguntas, speakable=("h1",))
        self.assertEqual(nodo["mainEntity"][0]["acceptedAnswer"]["text"], "Sí, mira.")
        self.assertEqual(nodo["speakable"]["cssSelector"], ["h1"])

    def test_planes_salen_de_la_formula_oficial(self):
        html = c.planes_mensualidades()
        for plazo, minimo in ((3, "$2,000"), (6, "$5,000"), (9, "$15,000"), (12, "$15,000")):
            self.assertIn(f"<dt>{plazo} mensualidades</dt><dd>desde {minimo}</dd>", html)
        self.assertNotRegex(html, r"(?i)sin intereses|\bMSI\b")

    def test_simulador_con_el_marcado_de_vt_simulador(self):
        html = c.simulador("pasto en rollo instalado", 12000, "servicio-pasto")
        for marca in ("data-simulador", "data-sim-monto", "data-sim-list", "data-sim-wa",
                      'data-cta="servicio-pasto:simulador"', 'value="12000"'):
            self.assertIn(marca, html)

    def test_howto_numera_los_pasos(self):
        nodo = c.howto("Cómo", (("Uno", "a"), ("Dos", "b")))
        self.assertEqual([p["position"] for p in nodo["step"]], [1, 2])

    def test_etiqueta_sin_nombre_cientifico_y_opciones_con_su_mensaje(self):
        e = {"codigo": "Sintético · 05/09", "aviso": "Con IVA", "nombre": "Toscana 28", "antes": "desde",
             "monto": "$199", "unidad": "/m²"}
        self.assertNotIn("vt-etiqueta__sci", c.etiqueta(e))
        self.assertIn('<p class="vt-etiqueta__sci">X y</p>', c.etiqueta(dict(e, cientifico="X y")))
        items = ({"rotulo": "Opción 1", "titulo": "A", "precio": 139, "unidad": "/m²", "detalle": "d", "puntos": ("p",),
                  "mensaje": "Hola A"},
                 {"rotulo": "Opción 2", "titulo": "B", "precio": 385, "unidad": "/m²", "detalle": "d", "puntos": ("q",),
                  "mensaje": "Hola B", "rec": True, "nota": "n"})
        html = c.opciones(items, "servicio-sintetico")
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["servicio-sintetico:opcion-1", "servicio-sintetico:opcion-2"])
        self.assertIn('<li class="vt-modo vt-modo--rec">', html)
        self.assertIn('<span class="vt-precio-marca">$385</span>', html)
        self.assertEqual([unquote(t).split("\n")[0] for t in re.findall(r"text=([^\"&]+)", html)], ["Hola A", "Hola B"])


class MedidorTest(unittest.TestCase):
    def test_html_del_medidor(self):
        html = c.medidor("prueba", "home")
        self.assertIn("data-vt-medidor", html)
        self.assertEqual(html.count('name="prueba-modo"'), 3)
        self.assertIn('data-precio="120"', html)
        self.assertIn('data-minimo="500"', html)
        self.assertIn('data-cta="home:medidor"', html)
        self.assertIn('<p class="vt-medidor__aviso" data-vt-o="aviso" hidden>', html)
        self.assertEqual(html.count('name="prueba-plazo"'), 5)
        self.assertIn('value="1" checked', html)
        self.assertIn("data-hero-cta", html)  # la barra móvil se esconde mientras el Medidor está a la vista

    def test_medidor_empieza_vacio_y_no_presenta_el_ejemplo_como_estimado(self):
        html = c.medidor("prueba", "home")
        self.assertIn('placeholder="8"', html)
        self.assertIn('placeholder="6"', html)
        self.assertNotRegex(html, r'data-vt-campo="(?:largo|ancho)"[^>]*value=')
        self.assertIn('<b data-vt-o="monto">—</b>', html)
        self.assertNotIn("$5,760", html)
        cta = re.search(r'data-vt-o="cta" href="https://wa\.me/528333268008\?text=([^"]+)"', html).group(1)
        self.assertEqual(unquote(cta), datos.con_firma(datos.MENSAJES["general"]))
        self.assertIn(f'data-mensaje-mayoreo="{c.esc(datos.con_firma(datos.MENSAJES["empresas"]))}"', html)
        for campo in ("largo", "ancho", "colonia"):
            self.assertIn(f'<label for="prueba-{campo}">', html)
        self.assertNotIn("<form", html)

    def test_medidor_lee_numero_y_mensaje_de_la_pagina_y_anuncia_el_resultado(self):
        html = c.medidor("prueba", "home", mensaje=datos.MENSAJES["pasto-natural"])
        self.assertIn(f'data-wa="{datos.TELEFONO_WA}"', html)
        self.assertIn(f'data-mensaje="{c.esc(datos.con_firma(datos.MENSAJES["pasto-natural"]))}"', html)
        self.assertIn('<div class="vt-etiqueta vt-medidor__res" role="status">', html)
        self.assertEqual(html.count("aria-live"), 0)


class EscapeTest(unittest.TestCase):
    def test_bloque_y_figura_escapan_atributos(self):
        html = c.bloque(1, "R", 'a"b', "T", "", id_seccion='c"d')
        self.assertIn('aria-labelledby="a&quot;b"', html)
        self.assertIn('id="c&quot;d"', html)
        self.assertIn('<h2 id="a&quot;b">', html)
        f = c.figura({"src": "/x.webp", "ancho": '1"', "alto": "<2", "alt": "x", "numero": 1, "lugar": "l", "etapa": "e"})
        self.assertIn('width="1&quot;" height="&lt;2"', f)


if __name__ == "__main__":
    unittest.main()
