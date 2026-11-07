import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402


class DatosTest(unittest.TestCase):
    def test_domicilio_con_209_sur(self):
        self.assertEqual(
            datos.DOMICILIO_COMPLETO,
            "Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamps.",
        )
        self.assertEqual(datos.DOMICILIO_CORTO, "Obregón 209 Sur, Cd. Madero")
        self.assertEqual(datos.REFERENCIA, "Frente a Walmart, entrando por Banamex")

    def test_contacto(self):
        self.assertEqual(datos.TELEFONO_WA, "528333268008")
        self.assertEqual(datos.TELEFONO_TEL, "+528333268008")
        self.assertEqual(datos.TELEFONO_VISIBLE, "833 326 8008")
        self.assertEqual(datos.CORREO_FORMULARIOS, "viverosterra@hotmail.com")
        self.assertEqual(datos.GA4_ID, "G-RMZCVJ734M")

    def test_promesa_unica(self):
        self.assertEqual(
            datos.PROMESA_COMPLETA,
            "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h",
        )

    def test_cifras_de_empresa(self):
        self.assertEqual(datos.DESDE, 2007)
        self.assertEqual(datos.FUNDACION, "2007-12-12")
        self.assertEqual(datos.REPSE, "773725")
        self.assertEqual(datos.M2_INSTALADOS, "+500,000 m²")
        self.assertEqual(datos.CLIENTES, "+900")
        self.assertEqual(datos.INSTALACIONES, "+1,500")
        self.assertEqual(datos.VARIEDADES, "+200")
        self.assertEqual(datos.GOOGLE, "4.6 en Google (24 reseñas)")
        self.assertEqual(datos.SINTETICO_NACIONAL_DESDE, 2012)

    def test_precios_oficiales(self):
        p = datos.PRECIOS
        self.assertEqual((p["pasto_solo_m2"], p["pasto_instalado_m2"], p["pasto_mayoreo_m2"]), (85, 120, 60))
        self.assertEqual(p["pasto_mayoreo_minimo_m2"], 500)
        self.assertEqual(p["mantenimiento_mes"], 750)
        self.assertEqual(p["diseno"], 3000)
        self.assertEqual(p["riego_m2"], (180, 320))
        self.assertEqual(p["sintetico_instalado_m2"], (385, 650))
        self.assertEqual(p["sintetico_tienda_m2"], 139)

    def test_decisiones_del_dueno_2026_11_07(self):
        self.assertEqual(datos.PRECIOS["poda"], 500)
        self.assertTrue(datos.PODA.startswith("Desde $500, según cotización"))
        self.assertEqual(datos.PRECIOS["flamboyan"], 250)
        self.assertEqual(len(datos.CLIENTES_B2B), 6)
        self.assertEqual(datos.AUTOR_BLOG, "Equipo técnico de Viveros Terra")
        self.assertIsNone(datos.PROXIMO_CORTE)

    def test_textos_de_garantia_y_riego(self):
        self.assertIn("15 a 20 días", datos.GARANTIA_PASTO)
        self.assertIn("sembramos nosotros", datos.GARANTIA_PLANTAS)
        self.assertEqual(datos.PRIMER_RIEGO, "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días.")

    def test_datos_de_las_plantillas_etapa_2a(self):
        p = datos.PRECIOS
        self.assertEqual((p["palma_desde"], p["tierra_negra_costal"], p["tierra_negra_m3"], p["tezontle_costal"]),
                         (250, 90, 1500, 200))
        self.assertEqual(datos.LLEGADA_PASTO, "una vez por semana, generalmente los viernes")
        self.assertTrue(datos.ANTICIPO.startswith("No pedimos el 100% por adelantado: para confirmar tu pedido o "
                                                  "agendar el servicio solicitamos un anticipo"))
        self.assertEqual(datos.ARRAIGO, "15 a 20 días")
        for cifra in ("$85 por m²", "desde $120 por m²", "500 m²", "$60/m²", "noviembre de 2026"):
            self.assertIn(cifra, datos.RESPUESTA_PRECIO_PASTO)

    def test_mensajes_terminan_con_la_firma(self):
        for servicio in datos.MENSAJES:
            with self.subTest(servicio=servicio):
                self.assertTrue(datos.mensaje(servicio).endswith("\n\nVengo de viverosterra.com"))

    def test_wa_url_codifica_todo(self):
        url = datos.wa_url("Hola, ñ\nColonia: ___")
        self.assertTrue(url.startswith("https://wa.me/528333268008?text="))
        self.assertNotIn(" ", url)
        self.assertEqual(unquote(url.split("text=", 1)[1]), "Hola, ñ\nColonia: ___")

    def test_redes_con_https_y_sin_subdominio_de_pais(self):
        for nombre, url in datos.REDES:
            with self.subTest(red=nombre):
                self.assertTrue(url.startswith("https://www."))
                self.assertNotIn("il.linkedin", url)


if __name__ == "__main__":
    unittest.main()
