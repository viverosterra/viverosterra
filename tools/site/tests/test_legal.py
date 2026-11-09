"""/politicas y /politica-privacidad con la plantilla legal: anclas estables, números de sus fuentes y sin dos H1."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import mensualidades  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402
from componentes_zonas import porcentaje_plazo  # noqa: E402

URLS = {k: f"/x/{k}" for k in ("terra.css", "terra-tienda.css", "terra-plantas.css", "terra-materiales.css", "terra-precios.css",
                               "terra-util.css", "legacy-fixes.css", "terra.js")}


def render(ruta):
    fila = next(f for f in generar.PAGINAS if f[0] == ruta)
    return generar.renderizar(ruta, fila[2], fila[3], URLS)


class PoliticasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = render("/politicas")

    def test_anclas_que_enlazan_otras_paginas(self):
        for ancla in ("envios", "devoluciones", "garantia-plantas", "garantia-pasto", "mensualidades", "facturacion", "privacidad", "contacto"):
            with self.subTest(ancla=ancla):
                self.assertIn(f'<section id="{ancla}"', self.html)
                self.assertIn(f'href="#{ancla}"', self.html)

    def test_carga_la_hoja_util_y_un_solo_h1(self):
        self.assertIn("/x/terra-util.css", self.html)
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)

    def test_numeros_de_sus_fuentes(self):
        for pieza in (f"{data.MIN_NACIONAL_M2} m²", f"desde {data.MIN_SHOWROOM_M2} m²", "$900", "$1,400"):
            self.assertIn(pieza, self.html)
        for plazo in mensualidades.PLAZOS:
            self.assertIn(f"+{porcentaje_plazo(plazo):.1f}%", self.html)

    def test_garantia_de_plantas_sin_prometer_costo_y_con_condiciones(self):
        self.assertIn("30 días de garantía de arraigo", self.html)
        self.assertIn("Nos avisas por WhatsApp con fotos dentro de los 30 días.", self.html)
        self.assertNotIn("asesoría gratis", self.html)

    def test_privacidad_remite_a_los_terceros_del_aviso_integral(self):
        html = render("/politicas")
        self.assertIn("<strong>No vendemos ni compartimos</strong> tu información con terceros distintos a los que indica el "
                      "Aviso Integral.", html)
        self.assertNotIn("terceros ajenos", html)

    def test_contacto_de_datos(self):
        for pieza in (datos.TELEFONO_VISIBLE, datos.CORREO_FORMULARIOS, datos.HORARIO, datos.CALLE):
            self.assertIn(pieza, self.html)

    def test_tipo_utilidad_en_el_shell(self):
        self.assertEqual(paginas.contexto("/politicas")["tipo"], "utilidad")
        self.assertIn('data-cta="utilidad:cierre"', shell.marcar_ctas(self.html, "utilidad"))


class PrivacidadTest(unittest.TestCase):
    def test_conserva_sus_ocho_puntos_y_su_marco_legal(self):
        html = render("/politica-privacidad")
        for titulo in ("1. Datos personales", "2. Finalidad", "3. Transferencia", "4. Derechos ARCO", "5. Uso de cookies",
                       "6. Seguridad", "7. Modificaciones", "8. Aceptación", "LFPDPPP", datos.GA4_ID, "20 días hábiles"):
            with self.subTest(titulo=titulo):
                self.assertIn(titulo, html)

    def test_transferencias_sin_nombrar_a_la_terminal(self):
        html = render("/politica-privacidad")
        self.assertIn("procesador de pagos con tarjeta", html)
        self.assertNotRegex(html.lower(), r"(?<![-.\w])clip(?![-\w:(])")


if __name__ == "__main__":
    unittest.main()
