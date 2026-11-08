"""Consistencia de datos en todo lo publicado (spec §5.2, §5.3 y decisiones del dueño del 2026-11-07).

Recorre el texto público de cada página (texto visible, JSON-LD, atributos legibles, mensajes de WhatsApp, scripts y
estilos, con la misma función `textos_publicos` de test_reglas.py) y llms.txt. Los valores esperados salen de
tools/site/datos.py.
"""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

PUBLIC = paginas.PUBLIC
PAGINAS = {p: p.read_text(encoding="utf-8") for p in sorted(PUBLIC.rglob("*.html"))}
TEXTOS = {p: textos_publicos(h) for p, h in PAGINAS.items()}
LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
PRECIOS = datos.PRECIOS
# Páginas que todavía mencionan la visita sin su costo. Debe quedar vacía y solo puede encoger.
VISITA_COSTO_PENDIENTES = frozenset()

PROHIBIDAS = (
    ("promesa de respuesta vieja",
     r"\b(?:te )?respond\w*\s+(?:por WhatsApp\s+)?(?:con [^.·]{0,40}?)?"
     r"(?:en minutos|hoy\b|el mismo día|en menos de (?:[2-9]|\d{2,}) horas)"),
    ("respuesta en un plazo viejo",
     r"\brespuesta\s+(?:a cotización\s+)?(?:hoy\b|el mismo día|en (?:menos de )?\d+ ?(?:h|hrs?|horas)\b)"
     r"|\bmismo día\W+respuesta|\b24 ?h\w*\W+respuesta"),
    ("contacto en 24 horas",
     r"\bcontact\w*(?: contigo)? en (?:menos de )?24 ?(?:h|hrs?|horas)\b|en contacto contigo en menos de 24 horas"
     r"|\bcotización en 24 horas"),
    ("plazo de respuesta viejo",
     r"\ben menos de (?:2|4) horas\b|\b[24] horas hábiles\b|\b\d+ ?h(?:rs?)? hábiles\b|\bEn 24 hrs\b"
     r"|por WhatsApp en minutos|en minutos sabrás"
     r"|(?:disponibilidad|personalizada|precio exacto[^.]{0,40}|diagnóstico y solución) (?:hoy mismo|el mismo día)"
     r"|\bconfirmamos disponibilidad hoy"),
    # La promesa oficial es datos.PROMESA: "menos de 1 hora" siempre lleva "en horario".
    ("1 hora sin \"en horario\"", r"\bmenos de (?:1|una) hora\b(?! en horario)"),
    ("pago al terminar", r"\bpagas\s+(?:cuando|al\s+ver)\b"),
    # Decisión del dueño (2026-11-07): el envío local de sintético en Tampico, Madero y Altamira se cotiza por colonia.
    ("envío local con precio fijo", r"env[ií]o\s+local[^.]{0,40}\$\s?250\b|\blocal desde \$\s?250\b"),
    ("líder", r"\blíder\b"),
    ("expertos", r"\bequipo de expertos\b"),
    ("sintético sobre pedido", r"\bmodelos? sobre pedido\b|\bsobre pedido\b"),
    ("aviso de corte, disponibilidad semanal o temporada",
     r"pr[oó]ximo corte|lote semanal|reservar (?:mi|tu) lote|lote de esta semana|instalaciones esta semana|"
     r"temporada de lluvias — el mejor momento"),
    ("mayoreo desde 200 m²", r"(?:mayoreo|pedidos)[^.]{0,60}\b200 m²"),
    ("mantenimiento desde $500/mes", r"mantenimiento[^.]{0,90}\$500\s?/\s?mes"),
    ("flamboyán a $500", r"f[lr]amboy[aá]n[^.$]{0,40}\$\s?500\b|\$\s?500\b[^.]{0,40}f[lr]amboy[aá]n"),
    # El dueño eligió "flamboyán" (2026-11-07). Los slugs existentes (/blog/framboyan-…) no se tocan.
    ("Framboyán (ortografía)", r"(?<!conocido como )(?<![\w/-])framboy[aá]n(?![\w-])"),
    ("esquema de pago con porcentaje (el dueño solo confirma un anticipo, sin porcentaje)",
     r"\b\d{1,3} ?% (?:de anticipo|restante|al (?:inicio|confirmar|terminar)|a la entrega)|\banticipo del \d"
     r"|\bpagas el \d{1,3} ?%|\bprimer pago[^.]{0,30}\d{1,3} ?%|\b(?:50/50|30/40/30)\b[^.]{0,40}(?:avances?|pago|anticipo)"),
    ("promesa de disponibilidad de visita o agenda",
     r"pr[oó]xima visita t[eé]cnica|visitas? disponibles?|\bhoy o mañana\b|\bmañana disponible\b"
     r"|disponibles? esta semana|agenda abierta|\bcupos? (?:disponibles?|limitados?)|jardín verde, esta semana"),
    ("frescura con fecha de corte", r"(?<!instalas fue )cortado esta semana"),
    ("Plan Terra Completo de $50,000",
     r"Plan Terra Completo (?:de )?\(?\$50,000|\(Plan Terra Completo\)|Plan Terra Completo incluye el primer mes"),
    ("tabla que desacredita el sintético", r"\bPlástico, áspero\b|\(quema\)|residuo plástico"),
    ("reseñas contradictorias", r"\b127 reseñas\b|\+127\b|reseñas verificadas|\b5(?:\.0)? en Google\b"),
    ("clientes contradictorios", r"\b1,500 clientes\b"),
    ("nota interna del blog", r"\bWix\b|\d[\d,]* búsquedas|miles de búsquedas|\b22 artículos\b"),
    ("años de la empresa distintos de 2007",
     r"(?:más de|con|llevamos|\+) ?(?:1[0-7]|[1-9]|2\d)\+? años (?:de experiencia|de trayectoria|en el mercado|en Tampico)"
     r"|\b20\+ Años\b"),
)


def nombre(path):
    return str(path.relative_to(PUBLIC))


def direcciones_ld(html):
    """PostalAddress del JSON-LD de la página que apuntan al vivero (las que llevan streetAddress)."""
    encontradas = []

    def recorrer(nodo):
        if isinstance(nodo, dict):
            if nodo.get("@type") == "PostalAddress" and "streetAddress" in nodo:
                encontradas.append(nodo)
            for valor in nodo.values():
                recorrer(valor)
        elif isinstance(nodo, list):
            for valor in nodo:
                recorrer(valor)

    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        recorrer(json.loads(bloque))
    return encontradas


def _same_as(nodo):
    """Todas las URL de `sameAs` en un bloque JSON-LD."""
    if isinstance(nodo, list):
        return {u for v in nodo for u in _same_as(v)}
    if not isinstance(nodo, dict):
        return set()
    propias = nodo.get("sameAs", [])
    propias = {propias} if isinstance(propias, str) else set(propias)
    return propias | {u for v in nodo.values() for u in _same_as(v)}


class ConsistenciaTest(unittest.TestCase):
    maxDiff = None

    def test_domicilio_siempre_con_209_sur(self):
        sin_sur = [nombre(p) for p, h in PAGINAS.items() if re.search(r"Obreg[oó]n 209(?! Sur)", h)]
        self.assertEqual(sin_sur, [])
        self.assertIsNone(re.search(r"Obreg[oó]n 209(?! Sur)", LLMS))

    def test_domicilio_del_json_ld_oficial(self):
        hallazgos = []
        for path, html in PAGINAS.items():
            for direccion in direcciones_ld(html):
                esperado = (datos.CALLE, datos.CP)
                if (direccion.get("streetAddress"), direccion.get("postalCode")) != esperado:
                    hallazgos.append(f"{nombre(path)} · {direccion}")
        self.assertEqual(hallazgos, [])

    def test_sin_datos_contradictorios_ni_frases_prohibidas(self):
        hallazgos = []
        for path, texto in list(TEXTOS.items()) + [(PUBLIC / "llms.txt", LLMS)]:
            for regla, patron in PROHIBIDAS:
                for m in re.finditer(patron, texto, re.I):
                    hallazgos.append(f"{nombre(path)} · {regla} · …{texto[max(0, m.start() - 50):m.end() + 50]}…")
        self.assertEqual(hallazgos, [])

    def test_sin_banner_de_temporada(self):
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertNotIn("urgencia-banner", html)
                self.assertNotIn("disponibilidad-bar", html)

    def test_garantia_de_plantas_con_condicion(self):
        condicion = re.compile(r"sembr|siembra|riego|condiciones|cuidad", re.I)
        hallazgos = []
        for path, texto in TEXTOS.items():
            for m in re.finditer(r"garant[ií]a[^.]{0,40}\b30 d[ií]as|\b30 d[ií]as[^.]{0,30}garant[ií]a", texto, re.I):
                if "precio" in m.group(0).lower():  # "garantía de precio: cotización respetada 30 días"
                    continue
                if not condicion.search(texto[max(0, m.start() - 120):m.end() + 200]):
                    hallazgos.append(f"{nombre(path)} · …{texto[max(0, m.start() - 60):m.end() + 60]}…")
        self.assertEqual(hallazgos, [])
        for archivo in ("catalogo.html", "diseno-jardines-tampico/index.html"):
            with self.subTest(pagina=archivo):
                self.assertIn("/politicas#garantia-plantas", PAGINAS[PUBLIC / archivo])

    def test_visita_con_costo_segun_la_ubicacion(self):
        """Decisión del dueño (2026-11-07): la visita para medir o cotizar tiene un costo que depende de la ubicación;
        cada mención lo dice cerca (datos.VISITA_COSTO o datos.VISITA_COSTO_CORTO) y nada promete traslado sin cargo."""
        mencion = re.compile(r"\bvisita\s+(?:t[eé]cnica\s+)?para\s+(?:medir|cotizar)", re.I)
        hallazgos = {}
        for path, texto in TEXTOS.items():
            for m in mencion.finditer(texto):
                if "depende de la ubicación" not in texto[max(0, m.start() - 150):m.end() + 200]:
                    hallazgos.setdefault(nombre(path), f"…{texto[max(0, m.start() - 60):m.end() + 60]}…")
            if re.search(r"sin cargo (?:extra )?por traslado", texto, re.I):
                hallazgos.setdefault(nombre(path), "traslado sin cargo")
        self.assertEqual({k: v for k, v in hallazgos.items() if k not in VISITA_COSTO_PENDIENTES}, {})
        self.assertEqual(sorted(VISITA_COSTO_PENDIENTES - set(hallazgos)), [], "ya lo dicen: sácalas de la lista")

    def test_home_con_cifras_oficiales(self):
        home = TEXTOS[PUBLIC / "index.html"]
        self.assertIn(f"{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones", home)
        faq = re.search(r'"name":"¿Cuánto cuesta el pasto en rollo en Tampico\?","acceptedAnswer":\{"@type":"Answer",'
                        r'"text":"([^"]+)"', PAGINAS[PUBLIC / "index.html"]).group(1)
        for cifra in (f"${PRECIOS['pasto_solo_m2']} por m²", f"desde ${PRECIOS['pasto_instalado_m2']} por m²",
                      f"{PRECIOS['pasto_mayoreo_minimo_m2']} m²", f"${PRECIOS['pasto_mayoreo_m2']}/m²"):
            self.assertIn(cifra, faq)

    def test_mayoreo_desde_500_m2(self):
        texto = TEXTOS[PUBLIC / "mayoreo-pasto-tampico" / "index.html"]
        self.assertIn(f"a partir de {PRECIOS['pasto_mayoreo_minimo_m2']} m²", texto)

    def test_flamboyan_desde_250(self):
        texto = TEXTOS[PUBLIC / "arboles-ornamentales-tampico" / "index.html"]
        self.assertIn(f"Flamboyán desde ${PRECIOS['flamboyan']}", texto)

    def test_slugs_de_framboyan_intactos(self):
        self.assertTrue((PUBLIC / "blog" / "framboyan-delonix-regia-tampico" / "index.html").exists())
        self.assertIn("también conocido como framboyán", TEXTOS[PUBLIC / "blog" / "framboyan-delonix-regia-tampico" / "index.html"])

    def test_home_sin_widget_de_disponibilidad(self):
        html = PAGINAS[PUBLIC / "index.html"]
        self.assertNotIn("next-visit-text", html)
        self.assertNotIn("Widget disponibilidad", html)

    def test_pago_de_pasto_y_palmas_sin_porcentaje(self):
        rollo = PAGINAS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"]
        self.assertIn('"text":"No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos '
                      'un anticipo. También puedes pagar en mensualidades con tarjeta de crédito en cotizaciones desde $2,000."',
                      rollo)
        self.assertIn("Recibes el precio del pasto, la entrega y la instalación por separado.",
                      TEXTOS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"])
        self.assertEqual(TEXTOS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"].count("Cortado para tu pedido"), 2)
        palmas = TEXTOS[PUBLIC / "palmas-mayoreo-proyectos" / "index.html"]
        self.assertEqual(palmas.count("Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contra "
                                      "avances de obra; te lo detallamos en la cotización."), 2)

    def test_same_as_igual_a_redes_oficiales(self):
        oficiales = {url for _, url in datos.REDES}
        sociales = re.compile(r"(?:facebook|instagram|tiktok|youtube|linkedin)\.com", re.I)
        hallazgos = []
        for path, html in PAGINAS.items():
            for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                for url in sorted(_same_as(json.loads(bloque))):
                    if sociales.search(url) and url not in oficiales:
                        hallazgos.append(f"{nombre(path)} · {url}")
        self.assertEqual(hallazgos, [])

    def test_mantenimiento_desde_750_en_el_blog_de_precios(self):
        texto = TEXTOS[PUBLIC / "blog" / "cuanto-cuesta-jardin-tampico-precios" / "index.html"]
        self.assertIn(f"desde ${PRECIOS['mantenimiento_mes']}/mes", texto)

    def test_sintetico_en_existencia_y_para_llevar_solo_toscana(self):
        texto = TEXTOS[PUBLIC / "pasto-sintetico-tampico" / "index.html"]
        self.assertIn("los otros 7 modelos también están en existencia", texto)
        for path, t in TEXTOS.items():
            for m in re.finditer(r"\bpara llevar\b", t, re.I):
                with self.subTest(pagina=nombre(path), pos=m.start()):
                    self.assertRegex(t[max(0, m.start() - 300):m.start()], r"Toscana (?:18|28)")

    def test_pasto_en_rollo_con_anticipo(self):
        texto = TEXTOS[PUBLIC / "pasto-en-rollo-tampico" / "index.html"]
        self.assertIn("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
                      "un anticipo", texto)
        self.assertIn("¿Cuál te conviene según tu espacio?", texto)

    def test_conteo_del_blog_sale_del_build(self):
        posts = len(list((PUBLIC / "blog").glob("*/index.html")))
        self.assertIn(f'<span data-vt-conteo="blog">{posts}</span> guías', PAGINAS[PUBLIC / "blog" / "index.html"])

    def test_gracias_con_promesa_unica_y_sin_emojis(self):
        html = PAGINAS[PUBLIC / "gracias" / "index.html"]
        self.assertIn(datos.PROMESA_COMPLETA, html)
        self.assertIn("Adelantar por WhatsApp", html)
        self.assertIsNone(re.search("[\U0001F300-\U0001FAFF]", html))

    def test_poda_con_precio_oficial(self):
        self.assertEqual(PRECIOS["poda"], 500)
        self.assertTrue(datos.PODA.startswith("Desde $500, según cotización"))

    def test_perfiles_oficiales(self):
        for path, html in list(PAGINAS.items()) + [(PUBLIC / "llms.txt", LLMS)]:
            with self.subTest(pagina=nombre(path)):
                self.assertNotIn("il.linkedin.com", html)
                self.assertNotIn("http://www.tiktok.com", html)
                self.assertIsNone(re.search(r"instagram\.com/viverosterra(?!mx)", html))

    def test_llms_con_paginas_y_datos_oficiales(self):
        for texto in ("https://www.viverosterra.com/precios", "https://www.viverosterra.com/vivero-tampico", "209 Sur",
                      "entrando por Banamex", f"desde {datos.SINTETICO_NACIONAL_DESDE}", "en menos de 1 hora en horario",
                      "## Lo que no hacemos", "https://www.instagram.com/viverosterramx"):
            with self.subTest(texto=texto):
                self.assertIn(texto, LLMS)

    def test_las_reglas_detectan_lo_que_deben(self):
        regla = dict(PROHIBIDAS)
        sucios = {
            "promesa de respuesta vieja": ("Respondemos hoy mismo", "respondemos en minutos", "Te respondemos hoy y",
                                           "Respondemos el mismo día ·", "Respondemos en menos de 4 horas hábiles"),
            "respuesta en un plazo viejo": ("Respuesta el mismo día · Tampico", "Mismo día Respuesta a cotización",
                                            "Respuesta en 24h", "Respuesta en menos de 2 horas", "Respuesta hoy · Lun–Sáb"),
            "contacto en 24 horas": ("Te contactamos en 24 hrs", "te contactará en menos de 24 horas"),
            "años de la empresa distintos de 2007": ("20+ Años en Tampico", "más de 15 años de experiencia"),
            "Framboyán (ortografía)": ("Framboyán Tabachín", "un framboyán adulto", "Framboyan en Tampico"),
            "esquema de pago con porcentaje (el dueño solo confirma un anticipo, sin porcentaje)": (
                "El pago es 50% de anticipo al confirmar", "y 50% restante al terminar", "Confirmas con 50% de anticipo",
                "Pagas el 50% restante", "Esquemas típicos: 50/50 o 30/40/30 contra avances",
                "El primer pago suele ser del 50% al inicio"),
            "promesa de disponibilidad de visita o agenda": (
                "Próxima visita técnica: esta semana", "Visitas disponibles desde el Lunes", "hoy o mañana",
                "mañana disponible", "Tu jardín verde, esta semana."),
            "frescura con fecha de corte": ("Pasto cortado esta semana", "Cortado esta semana"),
            "plazo de respuesta viejo": ("Respondemos en menos de 4h hábiles", "Respuesta en 2 h hábiles"),
            "1 hora sin \"en horario\"": ("Respuesta en menos de 1 hora", "respondemos en menos de una hora."),
            "envío local con precio fijo": ("El envío local cuesta desde $250 según el volumen", "Envío local desde $250",
                                            "Local desde $250"),
        }
        for nombre_regla, frases in sucios.items():
            for frase in frases:
                with self.subTest(regla=nombre_regla, frase=frase):
                    self.assertRegex(frase, re.compile(regla[nombre_regla], re.I))
        limpios = ("Respondemos en menos de 1 hora en horario", "Riego abundante el mismo día de la instalación",
                   "humedece el suelo 24 horas antes de instalar", "se enfría en minutos", "Te respondemos con el precio final",
                   "coordinar ambas entregas el mismo día", "Más de 18 años de experiencia", "dura de 8 a 12 años",
                   "/blog/framboyan-delonix-regia-tampico", "también conocido como framboyán", "Flamboyán Tabachín",
                   "proporción 50/50. Agrega compost", "No pedimos el 100% por adelantado", "ahorra entre 30% y 50% de agua",
                   "Lo que instalas fue cortado esta semana", "Lomas del Chairel y Flamboyanes",
                   "Envío local según tu colonia; te lo cotizamos.", "Areca y coco plumoso desde $250")
        for frase in limpios:
            with self.subTest(frase=frase):
                self.assertEqual([r for r, p in PROHIBIDAS if re.search(p, frase, re.I)], [])


if __name__ == "__main__":
    unittest.main()
