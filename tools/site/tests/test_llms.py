"""llms.txt y llms-full.txt (SEO fase 1, 2026-11-10): se generan en el build desde datos.py y el contenido de las páginas.

Reglas: el archivo publicado es el que el generador produce (nunca editado a mano); formato de llmstxt.org (H1, cita y
secciones H2 solo con listas de enlaces); cada enlace es una página que existe; cada precio citado sale de
datos.PRECIOS, datos.NOCHEBUENAS, tools/pasto/data.py o mensualidades.py; sin las frases que el dueño prohíbe.
"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import llms  # noqa: E402
import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
FULL = (PUBLIC / "llms-full.txt").read_text(encoding="utf-8")
P = datos.PRECIOS
NB = datos.NOCHEBUENAS
ENLACE_RE = re.compile(r"^- \[([^\]]+)\]\((https://[^)\s]+)\): (.+)$")
PRECIO_RE = re.compile(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?")


def precios_oficiales():
    """Toda cifra en pesos que llms.txt puede citar, como texto ("$1,500", "$446.60")."""
    valores = set()
    for clave, valor in P.items():
        if clave.endswith(("_minimo_m2",)):
            continue
        valores.update(valor if isinstance(valor, tuple) else (valor,))
    for producto in NB["productos"]:
        valores.update(producto["precios"])
    valores.update(llms.data.ZONAS.values())
    valores.update(m["rollo"] for m in llms.data.MODELOS)
    valores.update(minimo for minimo, _plazos in llms.mensualidades.UMBRALES)
    return {llms._dinero(v) for v in valores}


class GeneradoTest(unittest.TestCase):
    def test_los_archivos_publicados_son_los_que_genera_el_build(self):
        self.assertEqual(LLMS, llms.llms())
        self.assertEqual(FULL, llms.llms_full())
        self.assertEqual(llms.escribir(), 0, "una segunda corrida no escribe nada")

    def test_un_enlace_a_una_pagina_inexistente_detiene_el_build(self):
        with self.assertRaises(ValueError):
            llms._validar_rutas(["/precios", "/pagina-que-no-existe"])


class FormatoTest(unittest.TestCase):
    def test_h1_cita_y_secciones_solo_con_listas_de_enlaces(self):
        lineas = LLMS.split("\n")
        self.assertEqual(lineas[0], f"# {datos.NOMBRE}")
        self.assertTrue(lineas[2].startswith("> "))
        self.assertEqual(len([l for l in lineas if l.startswith("# ")]), 1)
        primer_h2 = next(i for i, l in enumerate(lineas) if l.startswith("## "))
        secciones = 0
        for linea in lineas[primer_h2:]:
            if not linea:
                continue
            if linea.startswith("## "):
                secciones += 1
                continue
            self.assertRegex(linea, ENLACE_RE)
        self.assertEqual(secciones, len(llms.SECCIONES))
        self.assertEqual(lineas[primer_h2:].count("## Optional"), 1)

    def test_cada_enlace_es_una_pagina_del_sitio(self):
        rutas = {ruta for ruta, _a, _p, _c in generar.PAGINAS}
        archivos = {ruta: salida for ruta, salida, _p, _c in generar.PAGINAS}
        enlaces = re.findall(r"\]\((https://[^)\s]+)\)", LLMS)
        self.assertGreater(len(enlaces), 40)
        for url in enlaces:
            ruta = url.removeprefix(datos.SITIO) or "/"
            with self.subTest(url=url):
                self.assertIn(ruta, rutas)
                self.assertTrue((PUBLIC / archivos[ruta]).is_file())

    def test_las_url_sueltas_tambien_existen(self):
        for texto in (LLMS, FULL):
            for url in set(re.findall(rf"{re.escape(datos.SITIO)}[^\s)]*", texto)):
                ruta = url.removeprefix(datos.SITIO).split("#")[0].rstrip(".,;") or "/"
                with self.subTest(url=url):
                    if ruta.endswith(".txt"):
                        self.assertTrue((PUBLIC / ruta.lstrip("/")).is_file())
                    else:
                        self.assertIn(ruta, {r for r, _a, _p, _c in generar.PAGINAS})

    def test_enlaza_el_texto_completo(self):
        self.assertIn(f"{datos.SITIO}/llms-full.txt", LLMS)
        self.assertIn(f"{datos.SITIO}/llms.txt", FULL)


class DatosTest(unittest.TestCase):
    def test_cada_precio_citado_es_un_precio_oficial(self):
        oficiales = precios_oficiales()
        # Monto de proyecto desde el que se descuenta el diseño Premium y pedido con entrega incluida de Nochebuenas.
        oficiales |= {llms._dinero(P["diseno_premium_descuento_desde"])}
        ajenos = sorted(set(PRECIO_RE.findall(LLMS)) - oficiales)
        self.assertEqual(ajenos, [])

    def test_precios_vigentes(self):
        minimo, maximo = P["sintetico_instalado_m2"]
        for frase in (
            f"solo el pasto: ${P['pasto_solo_m2']} por m² (no lleva IVA)",
            f"instalado: desde ${P['pasto_instalado_m2']} por m², con IVA incluido",
            f"mayoreo: desde ${P['pasto_mayoreo_m2']} por m², solo el pasto, en pedidos de {P['pasto_mayoreo_minimo_m2']} m² o más (no lleva IVA)",
            f"desde ${P['mantenimiento_mes']} al mes",
            "Esencial $3,000, Completo $6,500 y Premium desde $18,000",
            f"de ${P['riego_m2'][0]} a ${P['riego_m2'][1]} por m²",
            f"de ${minimo:.2f} a ${maximo} por m², con IVA",
            f"desde ${P['sintetico_tienda_m2']} por m² en rollo de 50 m²",
            "$900 (zona A), $1,150 (zona B) o $1,400 (zona C)",
            f"costal ${P['tierra_negra_costal']}", "a granel $1,500 por m³",
            "camión de 5 m³ $3,500, camión de 8 m³ $5,200, camión de 14 m³ $8,000",
            f"${P['marmol_saco']} el saco, {datos.MARMOL_CONDICION}",
            f"maceta de 5\" a ${NB['productos'][0]['precios'][0]} por pieza al menudeo y desde "
            f"${NB['productos'][0]['precios'][-1]} en pedidos de {NB['cortes'][-1]} piezas o más",
            "Precio de preventa: 5% menos en pedidos de menos de 200 piezas confirmados a más tardar el 30 de noviembre de 2026",
        ):
            with self.subTest(frase=frase):
                self.assertIn(frase, LLMS)

    def test_datos_del_negocio(self):
        for frase in (
            f"{datos.CALLE}, {datos.COLONIA}, {datos.CP} {datos.CIUDAD}, Tamaulipas, México",
            "entrando por Banamex", datos.MAPS_URL, f"+52 {datos.TELEFONO_VISIBLE}", datos.CORREO_FORMULARIOS,
            "lunes a viernes de 9:00 a 18:00; sábado de 9:00 a 14:00; domingo cerrado",
            "en menos de 1 hora en horario", f"Registro REPSE (STPS): {datos.REPSE}, consultable en {datos.REPSE_PADRON}",
            datos.FACTURA, datos.GOOGLE, f"fundada el 12 de diciembre de {datos.DESDE}",
            f"desde {datos.SINTETICO_NACIONAL_DESDE}", f"Por proyecto: {datos.ZONAS_POR_PROYECTO}",
            f"Actualizado: {datos.PRECIOS_ACTUALIZADOS}",
        ):
            with self.subTest(frase=frase):
                self.assertIn(frase, LLMS)
        for cliente in datos.CLIENTES_B2B:
            self.assertIn(cliente, LLMS)
        for _nombre, perfil in datos.REDES:
            self.assertIn(perfil, LLMS)

    def test_mensualidades_de_la_formula(self):
        """Los porcentajes salen de mensualidades.py: $10,000 de contado a 3 y a 12 mensualidades."""
        m = llms.mensualidades
        menor = m.total_a_plazos(100000, 3) / 1000 - 100
        mayor = m.total_a_plazos(100000, 12) / 1000 - 100
        self.assertIn(f"(+{menor:.1f}% a +{mayor:.1f}% según el plazo)", LLMS)
        self.assertIn("3 mensualidades desde $2,000; 6 mensualidades desde $5,000; 9 mensualidades desde $15,000; "
                      "12 mensualidades desde $15,000", LLMS)

    def test_sin_lo_que_el_dueno_prohibe(self):
        for texto in (LLMS, FULL):
            for patron in (r"(?i)\bgratis\b", r"(?i)\bgratuit", r"(?i)m[aá]s vendid", r"\bOasis\b", r"SENASICA",
                           r"\bMSI\b", r"repse\.stps\.gob\.mx/Publico", r"(?i)pr[oó]ximo corte",
                           r"Ciudad Mante|\bAldama\b|\bNaranjos\b|Cerro Azul|\bTempoal\b|El Higo",
                           r"Obreg[oó]n 601|Faja de Oro"):
                with self.subTest(patron=patron):
                    self.assertIsNone(re.search(patron, texto), patron)
        # Sin plazos de entrega en lo que llms.txt afirma por su cuenta (llms-full.txt copia las preguntas publicadas).
        for patron in (r"(?i)mismo d[ií]a", r"\d+\s*[–-]\s*\d+\s*hrs?\b", r"(?i)d[ií]as h[aá]biles", r"(?i)\bentrega en \d"):
            with self.subTest(patron=patron):
                self.assertIsNone(re.search(patron, LLMS), patron)
        # "sin costo" solo en la garantía de arraigo del pasto.
        for linea in LLMS.split("\n"):
            if re.search(r"sin costo", linea, re.I):
                self.assertIn("Garantía del pasto instalado", linea)
        # El anticipo, sin porcentaje (el 50% es solo de la página de Nochebuenas).
        self.assertIsNone(re.search(r"\d+\s*% de anticipo|anticipo del? \d+", LLMS))

    def test_iva_solo_donde_va(self):
        for linea in LLMS.split("\n"):
            if "solo el pasto" in linea or "Palmas:" in linea or "Flamboyán" in linea:
                with self.subTest(linea=linea[:60]):
                    self.assertIn("no lleva", linea)
                    self.assertNotRegex(linea, r"con IVA|IVA incluido")


class TextoCompletoTest(unittest.TestCase):
    def test_trae_las_paginas_que_venden_con_su_respuesta_y_sus_preguntas(self):
        for ruta in llms.PAGINAS_FULL:
            with self.subTest(ruta=ruta):
                self.assertIn(f"URL: {datos.SITIO}{ruta if ruta != '/' else '/'}\n", FULL)
        self.assertIn(datos.RESPUESTA_PRECIO_PASTO, FULL)
        self.assertGreater(FULL.count("\n### ¿"), 80)
        self.assertNotRegex(FULL, r"<[a-z][^>]*>")

    def test_trae_precios_garantias_cobertura_y_como_cotizar(self):
        for titulo in ("## Datos del negocio", "## Lista de precios", "## Garantías y condiciones", "## Cobertura",
                       "## Cómo cotizar"):
            self.assertIn(titulo, FULL)
        for renglon in llms.precios() + llms.condiciones():
            self.assertIn(renglon, FULL)


if __name__ == "__main__":
    unittest.main()
