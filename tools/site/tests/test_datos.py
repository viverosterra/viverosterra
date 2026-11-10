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
        self.assertEqual(len(datos.CLIENTES_B2B), 7)
        self.assertEqual(datos.CLIENTES_B2B[-1], "Renault")
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
        for cifra in ("$85 por m²", "desde $120 por m²", "500 m²", "$60/m²", f"Precios {datos.ANIO}, con IVA"):
            self.assertIn(cifra, datos.RESPUESTA_PRECIO_PASTO)
        # Sin mes de vigencia: un mes escrito envejece solo (como el aviso de lluvias de antes).
        self.assertNotRegex(datos.RESPUESTA_PRECIO_PASTO, r"(?i)\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
                                                          r"septiembre|octubre|noviembre|diciembre|vigentes)\b")
        self.assertFalse(hasattr(datos, "VIGENCIA"))

    def test_visita_con_costo_segun_la_ubicacion(self):
        """Decisión del dueño (2026-11-07): la visita para cotizar tiene costo y depende de la ubicación del servicio."""
        self.assertEqual(datos.VISITA_COSTO, "El costo de la visita para cotizar depende de la ubicación del servicio; "
                                             "te lo confirmamos por WhatsApp antes de agendar.")
        self.assertEqual(datos.VISITA_COSTO_CORTO, "Visita para medir y cotizar: su costo depende de la ubicación")

    def test_datos_de_servicios_etapa_2c(self):
        p = datos.PRECIOS
        self.assertEqual((p["diseno"], p["diseno_completo"], p["diseno_premium"]), (3000, 6500, 18000))
        self.assertEqual(p["diseno_premium_descuento_desde"], 150000)
        self.assertEqual(p["mantenimiento_mes"], 750)
        # Respuestas del dueño (2026-11-07): el premium se cotiza; +200 sistemas de riego y +200 proyectos B2B.
        self.assertNotIn("mantenimiento_premium_mes", p)
        self.assertEqual(datos.SEGUN_COTIZACION, "Según cotización")
        self.assertEqual(datos.MANTENIMIENTO_PREMIUM, datos.SEGUN_COTIZACION)
        self.assertEqual((datos.SISTEMAS_RIEGO, datos.PROYECTOS_B2B), ("+200", "+200"))
        self.assertEqual(datos.RIEGO_AHORRO, "hasta 40%")
        self.assertEqual(datos.FRECUENCIAS_MANTENIMIENTO, ("semanal", "cada 15 días", "cada 21 días", "mensual"))
        nombres = [n for grupo in (datos.OPINIONES_DISENO, datos.OPINIONES_MANTENIMIENTO, datos.OPINIONES_RIEGO)
                   for _c, n, _d in grupo]
        self.assertEqual(nombres, ["Daniela M.", "Ing. Roberto S.", "Carolina R.", "Ing. Gerardo M.", "Roberto C.",
                                   "María V."])

    def test_datos_de_empresas_etapa_2d(self):
        self.assertEqual(datos.ANTICIPO_PROYECTOS, "Para proyectos solicitamos un anticipo al confirmar y el resto se "
                                                   "acuerda contra avances de obra; te lo detallamos en la cotización.")
        self.assertNotIn("%", datos.ANTICIPO_PROYECTOS)
        self.assertEqual(datos.REPSE_PADRON, "https://repse.stps.gob.mx/")
        self.assertEqual(len(datos.PALMAS_PROYECTO), 12)
        con_precio = {n: p for n, _sci, p in datos.PALMAS_PROYECTO if p is not None}
        self.assertEqual(con_precio, {"Palma areca": 250, "Coco plumoso": 250, "Palma real": 500})
        self.assertEqual((datos.PRECIOS["palma_desde"], datos.PRECIOS["palma_real"]), (250, 500))
        self.assertEqual(len({n for n, _s, _p in datos.PALMAS_PROYECTO}), 12)

    def test_precios_de_plantas_etapa_2e(self):
        """Decisión del dueño (2026-11-07): los únicos precios de plantas; las demás especies, según cotización."""
        self.assertEqual(datos.PRECIOS_ESPECIE, {"Palma Areca": 250, "Coco Plumoso": 250, "Palma Real": 500,
                                                 "Flamboyán Tabachín": 250})
        self.assertEqual(datos.PALMAS_PRECIO, "Areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; "
                                              "el precio sube con la altura")
        proyecto = {n.casefold(): p for n, _s, p in datos.PALMAS_PROYECTO if p is not None}
        for nombre, precio in datos.PRECIOS_ESPECIE.items():
            if nombre.casefold() in proyecto:
                with self.subTest(especie=nombre):
                    self.assertEqual(precio, proyecto[nombre.casefold()])
        oficiales = {v for v in datos.PRECIOS.values() if isinstance(v, int)}
        for ruta, desde in datos.DESDE_PLANTAS.items():
            with self.subTest(ruta=ruta):
                self.assertTrue(desde is None or desde in oficiales)
        self.assertEqual(sorted(r for r, d in datos.DESDE_PLANTAS.items() if d is not None),
                         ["/arboles-ornamentales-tampico", "/palmas-tropicales-tampico"])

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

    def test_nochebuenas_cortes_y_productos(self):
        nb = datos.NOCHEBUENAS
        self.assertEqual(nb["cortes"], (1, 12, 50, 200))
        self.assertEqual(len(nb["nombres_escalon"]), len(nb["cortes"]))
        self.assertEqual([p["clave"] for p in nb["productos"]], ["5", "6", "7", "colgante", "12"])
        for producto in nb["productos"]:
            with self.subTest(producto=producto["clave"]):
                self.assertEqual(len(producto["precios"]), len(nb["cortes"]))
                self.assertEqual(list(producto["precios"]), sorted(producto["precios"], reverse=True))
        self.assertEqual([p["clave"] for p in nb["productos"] if p.get("sobre_pedido")], ["12"])

    def test_festivos_y_horario_para_abierto_ahora(self):
        """terra.js lee el horario y los festivos de los data-* del HTML: salen de aquí, con lunes = 1."""
        self.assertEqual(datos.FESTIVOS, ("12-25", "01-01"))
        self.assertEqual(datos.horario_marca(), "1,2,3,4,5@09:00-18:00;6@09:00-14:00")
        self.assertEqual(datos.festivos_marca(), "12-25,01-01")

    def test_fecha_de_la_version_es_un_dato_fijo_y_no_la_del_dia(self):
        """data-vt-build sale de aquí: si fuera date.today(), el build dejaría de ser idempotente."""
        self.assertRegex(datos.ACTUALIZADO, r"^20\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
        self.assertLessEqual(datos.ACTUALIZADO, datos.NOCHEBUENAS["preventa"]["hasta"])
        fuente = (Path(__file__).resolve().parents[1] / "datos.py").read_text(encoding="utf-8")
        self.assertNotRegex(fuente, r"^\s*(?:import datetime|from datetime)|\.today\(\)(?!:)")


if __name__ == "__main__":
    unittest.main()
