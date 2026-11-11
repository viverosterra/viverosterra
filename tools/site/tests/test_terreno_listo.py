"""Regla permanente del dueño (2026-11-10): el precio del pasto San Agustín instalado ("desde $120/m²", con IVA)
considera el terreno listo para instalar: limpio, nivelado y con tierra negra. Si no lo está, la limpieza, el herbicida,
la tierra negra o la nivelación se cotizan por separado. Sustituye a "el instalado incluye la preparación básica del
terreno".

Reglas: (1) ninguna página de public/ (texto visible, JSON-LD y mensajes de WhatsApp) ni llms*.txt afirma que el
instalado incluye la preparación del terreno; (2) cada vez que se muestra el precio del pasto instalado (un renglón, una
frase, una fila o una etiqueta) la condición de terreno listo va cerca (CERCA caracteres de texto, antes o después); (3)
los textos salen de las constantes de datos.py (TERRENO_LISTO_CORTO, TERRENO_LISTO, TERRENO_LISTO_MEDIDOR,
INSTALADO_INCLUYE), nada escrito a mano; (4) cada texto va donde lo pidió el dueño. El pasto sintético no entra: su
preparación "se cotiza aparte" desde antes y su precio no es el del pasto natural."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import shell  # noqa: E402
from contenido import respuestas  # noqa: E402

PUBLIC = paginas.PUBLIC
P = datos.PRECIOS
INSTALADO = P["pasto_instalado_m2"]
# El precio del instalado con su unidad ("$120/m²", "$120 /m²", "$120 por m²"); un "$90–$120 MXN/mes" no es pasto.
PRECIO_RE = re.compile(rf"\${INSTALADO}(?![\d,.])\s*(?:/\s*m²|por m²)")
CONDICION = "terreno listo"  # lo comparten las cuatro constantes
CERCA = 260
# "El instalado incluye la preparación básica del terreno" y sus variantes publicadas antes de la decisión.
PREPARACION_RE = re.compile(
    r"(?i)preparaci[oó]n\s+b[aá]sica|(?:incluye|con)\s+(?:la\s+)?preparaci[oó]n\s+(?:b[aá]sica\s+)?del\s+(?:suelo|terreno)"
    r"|preparamos\s+el\s+(?:suelo|terreno)|incluye\s+(?:la\s+)?mano\s+de\s+obra\s+b[aá]sica"
    r"|nivelamos,\s+retiramos")
WA_RE = re.compile(r'href="(https://wa\.me/[^"]+)"')
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


MEDIDOR_RE = re.compile(r'<div class="vt-medidor" data-vt-medidor.*?</a>(?:<p class="vt-medidor__garantia"[^>]*>.*?</p>)?</div></div></div>', re.S)


def visible(html):
    m = re.search(r"<main\b.*?</main>", html, re.S)
    return paridad.texto(m.group(0)) if m else ""


def visible_sin_medidor(html):
    """El texto visible sin los Medidores: cada uno es un bloque con su propia condición (TERRENO_LISTO_MEDIDOR bajo el
    estimado, que MedidorTest revisa); fuera de él vale la regla de cercanía."""
    return visible(MEDIDOR_RE.sub(" ", html))


def textos_ld(html):
    salida = []

    def recorrer(n):
        if isinstance(n, dict):
            for v in n.values():
                recorrer(v)
        elif isinstance(n, list):
            for v in n:
                recorrer(v)
        elif isinstance(n, str):
            salida.append(n)
    for bloque in LD_RE.findall(html):
        recorrer(json.loads(bloque))
    return " ".join(salida)


def mensajes(html):
    return [unquote(h.split("text=", 1)[1]) for h in WA_RE.findall(html_mod.unescape(html)) if "text=" in h]


def sin_condicion(texto):
    """Fragmentos con el precio del instalado sin "terreno listo" a menos de CERCA caracteres."""
    faltan = []
    for m in PRECIO_RE.finditer(texto):
        ventana = texto[max(0, m.start() - CERCA):m.end() + CERCA]
        if CONDICION not in ventana.lower():
            faltan.append(texto[max(0, m.start() - 80):m.end() + 60])
    return faltan


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


LLMS = [PUBLIC / "llms.txt", PUBLIC / "llms-full.txt"]


class ConstantesTest(unittest.TestCase):
    def test_textos_del_dueno(self):
        self.assertEqual(datos.TERRENO_LISTO_CORTO, "Precio con terreno listo: limpio, nivelado y con tierra negra.")
        self.assertEqual(datos.TERRENO_LISTO, (
            f"El precio de instalación desde ${INSTALADO}/m² considera tu terreno listo para instalar: limpio, nivelado "
            "y con tierra negra. Si no lo está, puede necesitar limpieza, herbicida, tierra negra o nivelación, que se "
            "cotizan por separado. Mándanos una foto por WhatsApp y te decimos antes qué necesita."))
        self.assertEqual(datos.TERRENO_LISTO_MEDIDOR,
                         "Estimado con terreno listo. Limpieza, herbicida, tierra negra o nivelación se cotizan aparte.")
        self.assertEqual(datos.INSTALADO_INCLUYE,
                         "Incluye la colocación del pasto y la garantía de arraigo, con el terreno listo.")
        self.assertEqual(datos.TERRENO_LISTO_PREGUNTA, "¿Mi terreno está limpio, nivelado y con tierra negra?: ___")
        for texto in (datos.TERRENO_LISTO_CORTO, datos.TERRENO_LISTO, datos.TERRENO_LISTO_MEDIDOR, datos.INSTALADO_INCLUYE):
            self.assertIn(CONDICION, texto.lower())

    def test_sin_precios_inventados_de_los_trabajos_previos(self):
        for texto in (datos.TERRENO_LISTO, datos.TERRENO_LISTO_MEDIDOR, datos.TIERRA_NEGRA_CRUZADA):
            precios = re.findall(r"\$\s?\d[\d,]*", texto)
            self.assertLessEqual(set(precios), {f"${INSTALADO}"}, texto)

    def test_el_analizador_ve_el_precio_y_su_condicion(self):
        self.assertEqual(sin_condicion(f"Instalado desde ${INSTALADO}/m². {datos.TERRENO_LISTO_CORTO}"), [])
        self.assertEqual(len(sin_condicion(f"Instalado desde ${INSTALADO}/m², con IVA.")), 1)
        self.assertEqual(sin_condicion("Ahorro: 1,800 L/mes = $90–$120 MXN/mes"), [])
        self.assertIsNotNone(PREPARACION_RE.search("El instalado incluye la preparación básica del terreno"))
        self.assertIsNone(PREPARACION_RE.search("la preparación del terreno se cotiza aparte"))


class SitioTest(unittest.TestCase):
    def test_nadie_afirma_que_el_instalado_incluye_la_preparacion(self):
        for path in shell.paginas_html():
            html = path.read_text(encoding="utf-8")
            textos = [visible(html), textos_ld(html), *mensajes(html)]
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                for t in textos:
                    self.assertIsNone(PREPARACION_RE.search(t), t[:200])
        for path in LLMS:
            with self.subTest(archivo=path.name):
                self.assertIsNone(PREPARACION_RE.search(path.read_text(encoding="utf-8")))

    def test_cada_precio_del_instalado_lleva_cerca_la_condicion(self):
        for path in shell.paginas_html():
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                html = path.read_text(encoding="utf-8")
                for medidor in MEDIDOR_RE.findall(html):
                    self.assertIn(datos.TERRENO_LISTO_MEDIDOR, medidor)
                self.assertEqual(sin_condicion(visible_sin_medidor(html)), [])
        # llms.txt: el renglón del precio. llms-full.txt: cada página (bloque ## …) que muestra el precio lleva la
        # condición; su descripción (la meta de la página, que la Entrega C no cambia) puede ir antes, en el mismo bloque.
        renglones = (PUBLIC / "llms.txt").read_text(encoding="utf-8").splitlines()
        for renglon in (r for r in renglones if PRECIO_RE.search(r)):
            self.assertIn(CONDICION, renglon.lower(), renglon)
        for bloque in re.split(r"\n(?=## )", (PUBLIC / "llms-full.txt").read_text(encoding="utf-8")):
            if PRECIO_RE.search(bloque):
                with self.subTest(bloque=bloque[:60]):
                    self.assertIn(CONDICION, bloque.lower())


REPONE_RE = re.compile(r"(?i)repon\w*\s+sin\s+costo")


def garantias_sin_terreno(texto):
    """Frases de la garantía de pasto ("la reponemos sin costo") sin datos.GARANTIA_TERRENO en los 40 caracteres que
    siguen (decisión del dueño, 2026-11-10: la garantía aplica con el terreno listo o preparado por Terra)."""
    return [texto[max(0, m.start() - 80):m.end() + 140] for m in REPONE_RE.finditer(texto)
            if datos.GARANTIA_TERRENO not in texto[m.end():m.end() + 40 + len(datos.GARANTIA_TERRENO)]]


class GarantiaTest(unittest.TestCase):
    def test_texto_de_la_garantia(self):
        self.assertEqual(datos.GARANTIA_PASTO, (
            f"Si una sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo, siempre que el terreno estuviera "
            "listo (limpio, nivelado y con tierra negra) o lo hayamos preparado nosotros, y se haya seguido el protocolo "
            "de riego (ver condiciones)."))
        self.assertEqual(garantias_sin_terreno(datos.GARANTIA_PASTO), [])
        self.assertEqual(len(garantias_sin_terreno("Si no arraiga, la reponemos sin costo, siguiendo el protocolo.")), 1)

    def test_toda_garantia_de_pasto_con_la_condicion_de_terreno(self):
        for path in shell.paginas_html():
            html = path.read_text(encoding="utf-8")
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                self.assertEqual(garantias_sin_terreno(visible(html)), [])
                self.assertEqual(garantias_sin_terreno(textos_ld(html)), [])
        for path in LLMS:
            with self.subTest(archivo=path.name):
                self.assertEqual(garantias_sin_terreno(path.read_text(encoding="utf-8")), [])

    def test_condiciones_del_protocolo_y_de_politicas(self):
        for ruta in ("/protocolo-cuidados-pasto-san-agustin", "/politicas"):
            with self.subTest(ruta=ruta):
                self.assertIn(datos.GARANTIA_TERRENO, visible(html_de(ruta)))


class LugaresTest(unittest.TestCase):
    def test_etiquetas_de_precio_con_la_condicion_corta(self):
        for ruta in ("/", "/pasto-en-rollo-tampico", "/precios", "/jardineria-ciudad-madero", "/jardineria-altamira"):
            html = html_de(ruta)
            portada = html[html.index('class="vt-portada'):html.index("</section>", html.index('class="vt-portada'))]
            with self.subTest(ruta=ruta):
                self.assertIn(f'<p class="vt-etiqueta__cond">{datos.TERRENO_LISTO_CORTO}</p>', portada)

    def test_faq_de_precio_en_corto_tablas_y_llms_con_la_condicion_larga(self):
        self.assertIn(datos.TERRENO_LISTO, datos.RESPUESTA_PRECIO_PASTO)
        for ruta in ("/", "/pasto-en-rollo-tampico"):
            with self.subTest(ruta=ruta, donde="En corto"):
                self.assertIn(datos.TERRENO_LISTO, respuestas.TEXTOS[ruta])
                self.assertTrue(40 <= len(respuestas.TEXTOS[ruta].split()) <= 60)
        for ruta in ("/", "/pasto-en-rollo-tampico", "/precios"):
            html = html_de(ruta)
            faq = next(n for b in LD_RE.findall(html) for n in json.loads(b).get("@graph", []) if n.get("@type") == "FAQPage")
            precio = next(q for q in faq["mainEntity"] if "cuesta el pasto" in q["name"].lower())
            with self.subTest(ruta=ruta, donde="FAQ"):
                self.assertIn(datos.TERRENO_LISTO, precio["acceptedAnswer"]["text"])
                self.assertIn(datos.TERRENO_LISTO, visible(html))
        for ruta in ("/", "/precios"):
            html = html_de(ruta)
            tablas = " ".join(re.findall(r'<table class="vt-tabla.*?</table>', html, re.S))
            with self.subTest(ruta=ruta, donde="tabla"):
                self.assertIn(datos.TERRENO_LISTO, paridad.texto(tablas))
        for path in LLMS:
            with self.subTest(archivo=path.name):
                self.assertIn(datos.TERRENO_LISTO, path.read_text(encoding="utf-8"))

    def test_venta_cruzada_de_tierra_negra_junto_a_la_condicion(self):
        enlace = f'<a href="{datos.TIERRA_NEGRA_RUTA}">{datos.TIERRA_NEGRA_CRUZADA}</a>'
        self.assertIn(enlace, html_de("/pasto-en-rollo-tampico"))
        self.assertIn(enlace, c.medidor("prueba", "servicio-pasto"))

    def test_filas_de_precio_dicen_lo_que_incluye_el_instalado(self):
        for ruta in ("/", "/pasto-en-rollo-tampico", "/precios"):
            with self.subTest(ruta=ruta):
                self.assertIn(datos.INSTALADO_INCLUYE, visible(html_de(ruta)))


class MedidorTest(unittest.TestCase):
    def test_instalado_con_la_condicion_y_el_renglon_del_terreno(self):
        r = c.calculo_medidor(8, 6, "instalado")
        t = c.textos_medidor(8, 6, r)
        self.assertEqual(t["terreno"], datos.TERRENO_LISTO_MEDIDOR)
        renglones = t["mensaje"].split("\n")
        self.assertIn(datos.TERRENO_LISTO_PREGUNTA, renglones)
        self.assertLess(renglones.index(datos.TERRENO_LISTO_PREGUNTA), renglones.index("Te mando foto del área."))

    def test_solo_pasto_y_mayoreo_sin_la_condicion(self):
        for modo, m2 in (("solo", (8, 6)), ("mayoreo", (40, 30)), ("mayoreo", (8, 6))):
            r = c.calculo_medidor(*m2, modo)
            t = c.textos_medidor(*m2, r)
            with self.subTest(modo=modo, m2=m2):
                self.assertEqual(t["terreno"], "")
                self.assertNotIn(datos.TERRENO_LISTO_PREGUNTA, t["mensaje"])

    def test_html_del_medidor_con_la_condicion_bajo_el_estimado(self):
        html = c.medidor("prueba", "servicio-pasto")
        # bajo el estimado: justo después de la banda del monto, antes del cálculo y del botón
        terreno = html.index('data-vt-o="terreno"')
        self.assertLess(html.index('data-vt-o="monto"'), terreno)
        self.assertLess(terreno, html.index('data-vt-o="calc"'))
        self.assertLess(terreno, html.index('data-vt-o="cta"'))
        self.assertIn(datos.TERRENO_LISTO_MEDIDOR, html)
        solo = c.medidor("prueba", "servicio-pasto", modo="solo")
        self.assertRegex(solo, r'data-vt-o="terreno" hidden')

    def test_mismos_textos_en_el_js(self):
        js = (PUBLIC / "js" / "vt-medidor.js").read_text(encoding="utf-8")
        self.assertEqual(re.search(r"const TERRENO_PREGUNTA = '([^']+)';", js).group(1), datos.TERRENO_LISTO_PREGUNTA)
        self.assertEqual(re.search(r"const TERRENO_MEDIDOR = '([^']+)';", js).group(1), datos.TERRENO_LISTO_MEDIDOR)


if __name__ == "__main__":
    unittest.main()
