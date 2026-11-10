"""Componentes de las utilitarias: etiquetas unidas a su control, grupos con fieldset y documento legal con anclas."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_util as cu  # noqa: E402
import datos  # noqa: E402


class ComponentesUtilTest(unittest.TestCase):
    def test_campo_une_label_y_control(self):
        html = cu.dibujar(cu.campo({"label": "Nombre", "name": "nombre", "id": "nombre", "tipo": "text", "requerido": True}))
        self.assertIn('<label for="nombre">Nombre', html)
        self.assertIn('id="nombre" name="nombre" required', html)

    def test_campo_sin_name_conserva_el_id(self):
        html = cu.dibujar(cu.campo({"label": "Calle", "id": "calle", "tipo": "text", "error": "Escribe la calle."}))
        self.assertNotIn("name=", html)
        self.assertIn('<p class="msg">Escribe la calle.</p>', html)

    def test_lista_con_valor_vacio_y_opciones_sin_value(self):
        html = cu.dibujar(cu.campo({"label": "Origen", "name": "o", "tipo": "lista", "opciones": (("", "Elegir"), (None, "Google"))}))
        self.assertIn('<option value="">Elegir</option><option>Google</option>', html)

    def test_grupo_con_legend_y_valor_distinto_del_texto(self):
        html = cu.dibujar(cu.opciones({"legend": "Uso", "tipo": "checkbox", "name": "uso", "items": (("Juego de niños", "Niños"),)}))
        self.assertIn("<fieldset", html)
        self.assertIn("<legend>Uso</legend>", html)
        self.assertIn('<input type="checkbox" name="uso" value="Juego de niños"><span>Niños</span>', html)

    def test_opcion_con_atributos_extra(self):
        html = cu.dibujar(cu.opciones({"legend": "T", "tipo": "radio", "name": "t", "items": (("Otro", "Otro", (("id", "rb"),)),)}))
        self.assertIn('value="Otro" id="rb">', html)

    def test_documento_legal_con_indice_y_anclas(self):
        html = cu.documento_legal(({"id": "envios", "titulo": "Política de Envíos", "corto": "Envíos",
                                    "bloques": (("p", "Texto"), ("ul", ("a", "b")), ("ol", ("c",)), ("h3", "Sub"))},))
        self.assertIn('<a href="#envios">Envíos</a>', html)
        self.assertIn('<section id="envios"', html)
        for pieza in ("<p>Texto</p>", "<ul><li>a</li><li>b</li></ul>", "<ol><li>c</li></ol>", "<h3>Sub</h3>"):
            self.assertIn(pieza, html)

    def test_cabeza_con_foto_es_la_imagen_prioritaria(self):
        html = cu.cabeza({"kicker": "K", "h1": "T", "lede": "L", "foto": {"src": "/img/a.webp", "ancho": 10, "alto": 5, "alt": ""}})
        self.assertIn('fetchpriority="high"', html)
        self.assertIn('width="10" height="5"', html)
        self.assertIn('id="vt-h1"', html)

    def test_boton_con_texto_propio_firma_el_mensaje(self):
        html = cu.boton_wa_texto("Adelantar por WhatsApp", "Hola", "utilidad:cuerpo")
        self.assertIn('data-cta="utilidad:cuerpo"', html)
        self.assertIn("Adelantar por WhatsApp", html)
        self.assertIn(datos.wa_url(datos.con_firma("Hola")).replace("&", "&amp;"), html)


if __name__ == "__main__":
    unittest.main()
