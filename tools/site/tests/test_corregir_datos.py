import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import corregir_datos as c  # noqa: E402
import datos  # noqa: E402


class ReglasGlobalesTest(unittest.TestCase):
    def test_no_recorre_ni_nombra_la_carpeta_retirada(self):
        self.assertNotIn("tools/servicios", c.__doc__)
        self.assertNotIn('"servicios"', Path(c.__file__).read_text(encoding="utf-8"))

    def test_domicilio_con_sur_sin_duplicar(self):
        self.assertEqual(c.corregir_texto("Av. Álvaro Obregón 209, Col. Ampliación"), "Av. Álvaro Obregón 209 Sur, Col. Ampliación")
        self.assertEqual(c.corregir_texto("Obregón 209 Sur"), "Obregón 209 Sur")
        self.assertEqual(c.corregir_texto("Av. Alvaro Obregon 209 · Madero"), "Av. Alvaro Obregon 209 Sur · Madero")

    def test_domicilio_del_json_ld_con_calle_y_codigo_postal_oficiales(self):
        viejo = ('{"@type":"PostalAddress","streetAddress":"Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional",'
                 '"addressLocality":"Ciudad Madero","addressRegion":"Tamaulipas","addressCountry":"MX"}')
        nuevo = (f'{{"@type":"PostalAddress","streetAddress":"{datos.CALLE}","addressLocality":"Ciudad Madero",'
                 f'"addressRegion":"Tamaulipas","postalCode":"{datos.CP}","addressCountry":"MX"}}')
        self.assertEqual(c.corregir_texto(viejo), nuevo)
        self.assertEqual(c.corregir_texto(nuevo), nuevo)
        con_cp = viejo.replace('"addressCountry"', '"postalCode":"89510","addressCountry"')
        self.assertEqual(c.corregir_texto(con_cp), nuevo)
        python = '"streetAddress": "Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional",'
        self.assertEqual(c.corregir_texto(python), f'"streetAddress": "{datos.CALLE}",')

    def test_promesa_unica(self):
        casos = {
            "Sin compromiso · Respondemos hoy mismo": "Sin compromiso · Respondemos en menos de 1 hora en horario",
            "— respondemos en minutos": "— respondemos en menos de 1 hora en horario",
            "Te respondemos hoy y, si hace falta": "Te respondemos en menos de 1 hora en horario y, si hace falta",
            "Respondemos el mismo día · Lun a vie 9 a 18 h, sáb 9 a 14 h": datos.PROMESA_COMPLETA,
            "Respondemos hoy · Lun–Sáb": datos.PROMESA_COMPLETA,
            "Sin compromiso · Respuesta hoy · Lun–Sáb": f"Sin compromiso · {datos.PROMESA_COMPLETA}",
            "Respondemos en menos de 4 horas hábiles. También": "Respondemos en menos de 1 hora en horario. También",
            "Respuesta el mismo día · Tampico": "Respuesta en menos de 1 hora en horario · Tampico",
            "Sin compromiso · Te contactamos en 24h · Lun a vie 9 a 18 h, sáb 9 a 14 h":
                f"Sin compromiso · {datos.PROMESA_COMPLETA}",
            '>Mismo día</div>\n <div class="x">Respuesta a cotización<':
                '>1 hora</div>\n <div class="x">Respuesta máxima en horario<',
            "Respondemos con el precio final": "Respondemos con el precio final",
            "Riego abundante el mismo día de la instalación": "Riego abundante el mismo día de la instalación",
        }
        for viejo, nuevo in casos.items():
            with self.subTest(viejo=viejo):
                self.assertEqual(c.corregir_texto(viejo), nuevo)

    def test_perfiles_y_flamboyan(self):
        self.assertEqual(c.corregir_texto("https://il.linkedin.com/company/viveros-terra-tampico"),
                         "https://www.linkedin.com/company/viveros-terra-tampico")
        self.assertEqual(c.corregir_texto("https://www.instagram.com/viverosterra"), "https://www.instagram.com/viverosterramx")
        self.assertEqual(c.corregir_texto("https://www.instagram.com/viverosterramx"), "https://www.instagram.com/viverosterramx")
        self.assertEqual(c.corregir_texto("Framboyán Tabachín y framboyán"), "Flamboyán Tabachín y flamboyán")
        self.assertEqual(c.corregir_texto("también conocido como framboyán"), "también conocido como framboyán")
        self.assertEqual(c.corregir_texto("Lomas del Chairel y Flamboyanes"), "Lomas del Chairel y Flamboyanes")

    def test_cada_regla_global_es_idempotente(self):
        for viejo, _ in c.GLOBALES:
            with self.subTest(viejo=viejo):
                una = c.corregir_texto(viejo)
                self.assertEqual(c.corregir_texto(una), una)


class HerramientasTest(unittest.TestCase):
    def test_quitar_elementos_con_su_linea(self):
        html = '<p>a</p>\n  <div id="urgencia-banner"><span>x</span></div>\n<p>b</p>'
        self.assertEqual(c.quitar_elementos(html, r'<div id="urgencia-banner"'), "<p>a</p>\n<p>b</p>")

    def test_reemplazar_es_idempotente_y_reporta_lo_que_falta(self):
        self.assertEqual(c.reemplazar("x 200 m² y", "200 m²", "500 m²", "f"), "x 500 m² y")
        self.assertEqual(c.reemplazar("x 500 m² y", "200 m²", "500 m²", "f"), "x 500 m² y")
        self.assertEqual(c.reemplazar("sin nada", "<tr>vieja</tr>", "", "f"), "sin nada")
        with self.assertRaises(SystemExit):
            c.reemplazar("nada", "200 m²", "500 m²", "f")

    def test_cada_reemplazo_por_archivo_es_idempotente(self):
        for rel, viejo, nuevo in c.POR_ARCHIVO:
            with self.subTest(archivo=rel, viejo=viejo[:60]):
                una = c.reemplazar(f"a {viejo} b", viejo, nuevo, rel)
                self.assertEqual(c.reemplazar(una, viejo, nuevo, rel), una)

    def test_no_toca_paginas_con_plantilla(self):
        """Etapas 2a y 2c: el HTML de esas páginas sale de su contenido; sus reemplazos viejos ya no aplican."""
        fuera = c.con_plantilla()
        for rel in ("public/index.html", "public/pasto-en-rollo-tampico/index.html",
                    "public/diseno-jardines-tampico/index.html", "public/sistema-riego-tampico/index.html"):
            self.assertIn(rel, fuera)
        for rel, *_resto in c.vigentes(c.POR_ARCHIVO) + c.vigentes(c.ELEMENTOS):
            self.assertNotIn(rel, fuera)

    def test_cada_reemplazo_vigente_encuentra_su_texto_o_su_correccion(self):
        for rel, viejo, nuevo in c.vigentes(c.POR_ARCHIVO):
            with self.subTest(archivo=rel, viejo=viejo[:60]):
                c.reemplazar((c.RAIZ / rel).read_text(encoding="utf-8"), viejo, nuevo, rel)


if __name__ == "__main__":
    unittest.main()
