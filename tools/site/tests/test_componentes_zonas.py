"""Componentes de las zonas y de /precios (componentes_zonas.py): precios de datos.py, "según cotización" sin número,
sintético de tools/pasto/data.py y mensualidades con la fórmula oficial (tools/pasto/mensualidades.py)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_zonas as cz  # noqa: E402
import data  # noqa: E402
import datos  # noqa: E402
import mensualidades  # noqa: E402

P = datos.PRECIOS


class PrecioTest(unittest.TestCase):
    def test_textos_de_precio(self):
        self.assertEqual(cz.precio_texto(P["pasto_solo_m2"]), "$85")
        self.assertEqual(cz.precio_texto(P["pasto_instalado_m2"], desde=True), "desde $120")
        self.assertEqual(cz.precio_texto(P["riego_m2"]), "$180 a $320")
        self.assertEqual(cz.precio_texto(None), datos.SEGUN_COTIZACION)

    def test_lista_con_unidad_enlace_desde_y_segun_cotizacion(self):
        html = cz.lista((
            {"nombre": "Pasto instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²", "detalle": "x",
             "precio": 120, "desde": True},
            {"nombre": "Poda", "unidad": "árbol o palma", "detalle": "y", "precio": 500, "desde": True, "cotiza": True},
            {"nombre": "Mármol", "unidad": "saco", "detalle": "z", "precio": None},
        ), "Precios 2026 con IVA.")
        self.assertIn('<th scope="col">Unidad</th>', html)
        self.assertIn('<a href="/pasto-en-rollo-tampico">Pasto instalado</a>', html)
        self.assertIn('<td class="vt-tabla__p"><small class="vt-tabla__desde">desde</small>$120</td>', html)
        self.assertIn('<small class="vt-tabla__desde">desde</small>$500<small>según cotización</small>', html)
        self.assertIn('<td class="vt-tabla__p vt-tabla__p--cotiza">Según cotización</td>', html)
        self.assertEqual(html.count("<tr>"), 4)


class SinteticoYMensualidadesTest(unittest.TestCase):
    def test_sintetico_por_modelo_de_data(self):
        html = cz.tabla_sintetico()
        self.assertEqual(html.count('<th scope="row">'), len(data.MODELOS))
        m = data.MODELOS[0]
        self.assertIn(f'<td>${m["t1"]}</td><td>${m["t2"]}</td><td><b>${m["rollo"]}</b></td>', html)

    def test_porcentajes_desde_la_formula(self):
        """La tabla que publicaba tools/pasto/precios.py (test_precios.py de tools/pasto, movido aquí en 2g)."""
        esperado = {3: 10.5, 6: 14.9, 9: 20.5, 12: 23.4}
        for plazo, pct in esperado.items():
            self.assertEqual(cz.porcentaje_plazo(plazo), pct)
            self.assertEqual(round((mensualidades.total_a_plazos(100000, plazo) / 100000 - 1) * 100, 1), pct)

    def test_tabla_de_mensualidades(self):
        html = cz.tabla_mensualidades()
        for fila in ('<th scope="row">3 mensualidades</th><td>$2,000</td><td><b>+10.5%</b></td>',
                     '<th scope="row">6 mensualidades</th><td>$5,000</td><td><b>+14.9%</b></td>',
                     '<th scope="row">9 mensualidades</th><td>$15,000</td><td><b>+20.5%</b></td>',
                     '<th scope="row">12 mensualidades</th><td>$15,000</td><td><b>+23.4%</b></td>'):
            self.assertIn(fila, html)
        self.assertNotRegex(html.lower(), r"recargo|comisi[oó]n|intereses|msi")


class GarantiasYColoniasTest(unittest.TestCase):
    def test_garantias_con_ancla(self):
        html = cz.garantias(({"id": "garantia-plantas", "titulo": "Plantas", "texto": "30 días",
                              "enlace": ("Condiciones", "/politicas#garantia-plantas")},))
        self.assertIn('<li class="vt-modo" id="garantia-plantas"><h3>Plantas</h3>', html)
        self.assertIn('href="/politicas#garantia-plantas"', html)

    def test_colonias_con_codigo_postal(self):
        html = cz.colonias((("Águila", "89230"),), "Colonias de Tampico")
        self.assertIn("<li><b>Águila</b><span>CP 89230</span></li>", html)
        self.assertIn("Colonias de Tampico", html)
        self.assertNotIn("<small>", html)


if __name__ == "__main__":
    unittest.main()
