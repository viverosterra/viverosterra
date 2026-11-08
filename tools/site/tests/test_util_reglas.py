"""Reglas del dueño en las páginas utilitarias (Etapa 2i): sin CSS viejo ni Google Fonts, las mismas fotos, anclas y campos
de main, medición de /gracias intacta y las correcciones de políticas y privacidad (tabla C del plan).

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea saca las suyas) y al
cerrar la Etapa 2i queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paridad  # noqa: E402
import paridad_util  # noqa: E402

CONTRATO = json.loads(paridad_util.CAPTURA.read_text(encoding="utf-8"))
PENDIENTES = frozenset({"/politicas", "/politica-privacidad", "/gracias", "/cuestionario", "/datos-envio",
                        "/protocolo-cuidados-pasto-san-agustin", "/vivero-tampico"})
PAGINAS = tuple(CONTRATO)
GARANTIA_PASTO = "la reponemos sin costo"  # la única frase con "sin costo" que aprobó el dueño
VIEJOS = r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)|<style\b|function sendWA|window\.open"
GENERALES = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b|\bsin cargo\b"),
    ("marca o término prohibido", r"\bOasis\b|\bMSI\b|sin intereses|meses sin|(?<![-.\w])clip(?![-\w:(])"),
    ("pago al terminar", r"\bpagas\s+(?:cuando|al\s+ver)\b|100% por adelantado(?<!No pedimos el 100% por adelantado)"),
    ("sin respaldo", r"\bexpertos?\b|\b18 años\b|\+18\b|\ben stock\b|precios orientativos|productor(?:es)? direct"
                     r"|precios? (?:m[aá]s bajos|m[aá]s accesibles|preferenciales)"),
)
ESPECIFICAS = {
    "/politicas": (
        ("devolución en la meta", lambda h: "devoluciones (7 días)" in h and "(30 días)" not in h),
        ("anticipo", lambda h: datos.ANTICIPO in h and "al confirmarse el pago" not in h),
        ("total y mensualidad antes del link", lambda h: "el total y el monto de cada mensualidad" in h),
        ("efectivo y precio de contado con tarjeta", lambda h: "transferencia bancaria, efectivo" in h
         and "una sola exhibición paga el precio de contado" in h),
        ("tiempo de entrega coherente", lambda h: "1–2 días de preparación" not in h and "1 a 2 días hábiles" in h),
        ("garantía de pasto con ancla", lambda h: 'id="garantia-pasto"' in h and datos.ARRAIGO in h and "antes del día 21" in h),
        ("materiales y factura", lambda h: datos.CONDICIONES_MATERIALES in h and datos.FACTURACION in h),
        ("privacidad igual al aviso integral", lambda h: "promociones" in h and 'href="/politica-privacidad"' in h),
        ("sin Transparencia total", lambda h: "Transparencia total" not in h),
    ),
    "/politica-privacidad": (
        ("transferencias reales", lambda h: "Paqueterías" in h and "procesador de pagos con tarjeta" in h),
    ),
    "/vivero-tampico": (
        ("horario real del sábado", lambda h: "Lun–Sáb" not in h and "9am–6pm horario" not in h),
        ("sin existencias", lambda h: "disponibilidad" not in paridad.texto(paridad.principal(h))),
    ),
    "/protocolo-cuidados-pasto-san-agustin": (
        ("garantía con la frase aprobada", lambda h: "la reponemos sin costo" in h and "sin costo adicional" not in h),
    ),
    "/gracias": (("promesa única", lambda h: datos.PROMESA_COMPLETA.split(" · ")[0] in h and "Adelantar por WhatsApp" in h),),
    "/cuestionario": (
        ("un solo H1", lambda h: len(re.findall(r"<h1\b", h)) == 1),
        ("honeypot", lambda h: 'name="_honey"' in h),
        ("visita con costo", lambda h: datos.VISITA_COSTO_CORTO in h),
    ),
}


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def visible(html):
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    return f"{paridad.texto(paridad.principal(html))} {metas}"


def fallas(ruta):
    html, salida = html_de(ruta), []
    if re.search(VIEJOS, html):
        salida.append(f"viejo: {re.search(VIEJOS, html).group(0)}")
    texto = visible(html).replace(GARANTIA_PASTO, "")
    for regla, patron in GENERALES:
        for m in re.finditer(patron, texto, re.I):
            salida.append(f"{regla}: …{texto[max(0, m.start() - 30):m.end() + 30]}…")
    salida += [regla for regla, ok in ESPECIFICAS.get(ruta, ()) if not ok(html)]
    actual, antes = paridad_util.extraer(ruta), CONTRATO[ruta]
    if actual["fotos"] and [f["src"] for f in actual["fotos"]] != [f["src"] for f in antes["fotos"]]:
        salida.append("fotos distintas de main")
    salida += [f"ancla perdida: {a}" for a in antes["anclas"] if a not in actual["anclas"]]
    return salida


class UtilitariasReglasTest(unittest.TestCase):
    def test_migradas_cumplen(self):
        for ruta in PAGINAS:
            if ruta in PENDIENTES:
                continue
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_siguen_fallando(self):
        for ruta in PENDIENTES:
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_gracias_mide_igual_que_main(self):
        """GA4 cuenta /gracias por su URL y su page_view: una sola configuración, ningún evento propio, mismo data-cta."""
        actual, antes = paridad_util.extraer("/gracias"), CONTRATO["/gracias"]
        self.assertEqual(actual["medicion"], antes["medicion"])
        self.assertEqual(actual["medicion"], {"gtag_config": 1, "gtag_event": 0, "data_cta": ["utilidad:cuerpo"]})

    def test_campos_del_cuestionario_iguales_a_main_mas_honeypot(self):
        quitar_id = lambda c: c if c[0] == "option" else [c[0], c[2], c[3], c[4], c[5]]  # noqa: E731
        antes = [quitar_id(c) for c in CONTRATO["/cuestionario"]["campos"]]
        actual = [quitar_id(c) for c in paridad_util.extraer("/cuestionario")["campos"] if c[2:3] != ["_honey"]]
        self.assertEqual(actual, antes)
        self.assertEqual(paridad_util.extraer("/cuestionario")["form"], CONTRATO["/cuestionario"]["form"])

    def test_controles_de_datos_de_envio_iguales_a_main(self):
        ids = lambda campos: [c[1] for c in campos if c[0] != "option"]  # noqa: E731
        self.assertEqual(ids(paridad_util.extraer("/datos-envio")["campos"]), ids(CONTRATO["/datos-envio"]["campos"]))

    def test_las_noindex_siguen_noindex(self):
        for ruta in ("/gracias", "/cuestionario", "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertRegex(html_de(ruta), r'<meta name="robots" content="noindex, (?:no)?follow">')


if __name__ == "__main__":
    unittest.main()
