"""Marcado de los componentes de materiales (Etapa 2f): calculadora, presentaciones, otros materiales, portadas, cierre
con foto y formulario de pedido."""
import json
import re
import sys
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_materiales as cm  # noqa: E402
import datos  # noqa: E402

MENSAJE = "Hola, quiero cotizar tierra negra.\nCantidad: ___\nColonia de entrega: ___"


class CalculadoraTest(unittest.TestCase):
    def setUp(self):
        self.html = cm.calculadora("vt-tierra", "material", "tierra-negra", MENSAJE, "tierra negra")

    def test_empieza_vacia_y_manda_el_mensaje_de_la_pagina_firmado(self):
        self.assertIn('data-vt-o="cantidad">Escribe el área</p>', self.html)
        href = unescape(re.search(r'data-vt-o="cta" href="([^"]*)"', self.html).group(1))
        self.assertEqual(unquote(href.split("text=", 1)[1]), datos.con_firma(MENSAJE))

    def test_cta_con_el_cta_id_que_media_main(self):
        self.assertIn('data-cta="material:cotizarCalculado"', self.html)
        self.assertIn("Cotizar por WhatsApp", self.html)
        self.assertNotIn("window.open", self.html)

    def test_datos_para_el_js_salen_de_datos_py(self):
        cfg = json.loads(unescape(re.search(r'data-material="([^"]*)"', self.html).group(1)))
        self.assertEqual(cfg, {"clave": "tierra-negra", "costal_m3": 0.035, "precio_costal": 90, "precio_m3": 1500,
                               "texto": "tierra negra vegetal"})
        self.assertEqual(cm.datos_js("piedra-bola")["kg_m2"], (120, 150))

    def test_capa_con_label_y_la_de_main_elegida(self):
        self.assertIn('<label for="vt-tierra-capa">', self.html)
        self.assertIn('<option value="0.08" selected>', self.html)
        self.assertNotIn("data-vt-campo=\"capa\"", cm.calculadora("vt-p", "material", "piedra-bola", MENSAJE, "piedra bola"))

    def test_marmol_sin_precio_y_con_peso(self):
        html = cm.calculadora("vt-marmol", "material", "marmol", MENSAJE, "mármol blanco")
        self.assertIn('data-vt-o="peso"', html)
        self.assertNotIn("$", html.split("data-mensaje")[0] + html.split("</select>")[-1].split("href=")[0])


class PresentacionesTest(unittest.TestCase):
    def test_precio_de_datos_o_segun_cotizacion(self):
        html = cm.presentaciones(({"nombre": "Costal", "detalle": "≈ 20 kg", "unidad": "costal", "precio": 90},
                                  {"nombre": "Camión", "detalle": "8 m³", "unidad": "camión", "precio": None},
                                  {"nombre": "Tezontle", "detalle": "", "unidad": "costal", "precio": 200, "desde": True}),
                                 "Presentaciones")
        self.assertIn('<td class="vt-tabla__p">$90</td>', html)
        self.assertIn('<td class="vt-tabla__p vt-tabla__p--cotiza">Según cotización</td>', html)
        self.assertIn(">desde $200<", html)
        self.assertIn('<th scope="col">Unidad</th>', html)


class OtrosTest(unittest.TestCase):
    def test_miniatura_solo_donde_main_la_tenia(self):
        html = cm.otros(({"titulo": "Tezontle rojo", "href": "/tezontle-rojo-tampico", "texto": "Costal desde $200",
                          "img": {"src": "/img/t.webp", "ancho": 194, "alto": 259}},
                         {"titulo": "Piedra bola", "href": "/piedra-bola-rio-tampico", "texto": "Según cotización"}),
                        (("Pasto en rollo", "/pasto-en-rollo-tampico"),))
        self.assertEqual(html.count("<img"), 1)
        self.assertIn('width="194" height="259" alt=""', html)
        self.assertIn('También: <a href="/pasto-en-rollo-tampico">Pasto en rollo</a>.', html)


class PortadaYCierreTest(unittest.TestCase):
    P = {"kicker": "K", "h1": "H", "lede": "L", "mensaje": MENSAJE, "tambien": "T",
         "etiqueta": {"codigo": "C", "aviso": "A", "nombre": "N", "antes": "", "monto": "$90", "unidad": "por costal"}}

    def test_sin_foto_y_apaisada(self):
        sin = cm.portada(self.P, "material", (("Inicio", "/"), ("X", None)))
        self.assertIn('class="vt-portada vt-portada--sinfoto"', sin)
        self.assertNotIn("<img", sin)
        foto = {"src": "/img/a.webp", "ancho": 960, "alto": 640, "numero": 1, "alt": "a", "lugar": "l", "etapa": "e"}
        self.assertIn("vt-portada--apaisada", cm.portada(dict(self.P, foto=foto), "material", (("Inicio", "/"),)))
        vertical = dict(foto, ancho=900, alto=1200)
        self.assertNotIn("vt-portada--", cm.portada(dict(self.P, foto=vertical), "material", (("Inicio", "/"),)))

    def test_cierre_con_foto_de_fondo_decorativa(self):
        html = cm.cierre({"titulo": "T", "lede": "L", "fondo": {"src": "/img/f.webp", "ancho": 1400, "alto": 933}},
                         MENSAJE, "material")
        self.assertIn('<section class="vt-cierre vt-cierre--foto"', html)
        self.assertIn('<img class="vt-cierre__fondo" src="/img/f.webp" width="1400" height="933" alt=""', html)
        self.assertNotIn("vt-cierre--foto", cm.cierre({"titulo": "T", "lede": "L"}, MENSAJE, "material"))


class PedidoTest(unittest.TestCase):
    def test_campos_y_destino_de_main_con_honeypot(self):
        html = cm.formulario_pedido("vt-tierra", "material:formulario", "Ejemplo", "Aviso")
        self.assertIn(f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}" method="POST"', html)
        self.assertEqual(re.findall(r'name="([^"]+)"', html),
                         ["_subject", "_next", "_captcha", "_honey", "nombre", "email", "detalle"])
        self.assertIn('value="Pedido desde sitio web - Viveros Terra"', html)
        self.assertIn(f'value="{datos.SITIO}/gracias"', html)
        self.assertIn('data-cta-form="material:formulario"', html)
        self.assertIn('type="email" required', html)


if __name__ == "__main__":
    unittest.main()
