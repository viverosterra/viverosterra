"""Reglas permanentes del dueño sobre todo lo publicado en public/: texto visible, JSON-LD, atributos legibles
(content, alt, title, aria-label, placeholder), mensajes de WhatsApp prellenados, scripts y estilos en línea. Los .js,
.css, .txt y .xml se revisan completos para las reglas de marcas y pagos. En CSS, los valores "clip" de propiedades
(text-overflow: clip) no cuentan como el nombre del proveedor de la terminal."""
import html as html_mod
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
PERMITIDAS = ('anuncian "envío gratis"',)  # el hub explica que "envío gratis" de otros ya viene en el precio
PAGOS = r"inter[eé]s|intereses|mensualidad|meses|pagos?|plazos?|tarjeta|comisi[oó]n|enganche|financ|recargo"
PROHIBIDAS = (
    ("Oasis", r"\bOasis\b"),
    ("marca de proveedor de pasto sintético", r"\bPasto\s?Plus\b"),
    ("nombre del proveedor de la terminal", r"(?<![-.\w])clip(?![-\w:(])"),
    ("MSI", r"\bMSI\b"),
    ("sin intereses", r"\bsin intereses\b"),
    # "0%" solo en contexto de pagos: "40% de agua" o "100% natural" no cuentan.
    ("0 % en pagos", rf"(?<![\d.,])0\s?%\W+(?:\w+\W+){{0,4}}?(?:{PAGOS})|(?:{PAGOS})\w*\W+(?:\w+\W+){{0,4}}?(?<![\d.,])0\s?%"),
    ("muestras gratis o físicas", r"(?<!no ofrecemos )(?<!no enviamos )(?<!sin )\bmuestras?\s+(?:gratis|f[ií]sicas?)\b"
                                  r"|\b(?:pide|solicita|te enviamos|te mandamos|enviamos)\s+(?:tus?\s+|unas?\s+)?muestras?\b"),
    ("envío gratis", r"(?:env[ií]os?|flete)\W+(?:\w+\W+){0,3}gratis\b|\bgratis\W+(?:\w+\W+){0,3}(?:env[ií]os?|flete)"),
)
DEPORTES_RE = re.compile(r"p[aá]del|canchas?", re.I)
PAGO_AL_TERMINAR_RE = re.compile(r"\bpagas\s+(?:cuando|al\s+ver)\b", re.I)
# Decisión del dueño (2026-11-07): la visita para medir tiene costo o depende; nunca "visita sin costo", "visita
# gratis" ni "visita gratuita" (tampoco "vamos a medir sin costo").
GRATIS = r"(?:sin\s+costo|gratis|gratuitas?)"
VISITA_GRATIS_RE = re.compile(
    rf"\bvisitas?\b\W+(?:\w+\W+){{0,3}}?{GRATIS}\b|\b(?:medir|medimos|medici[oó]n)\W+(?:\w+\W+){{0,2}}?{GRATIS}\b"
    rf"|\b{GRATIS}\W+(?:\w+\W+){{0,2}}?visitas?\b", re.I)
# Páginas viejas que todavía lo dicen: se corrigen al migrar a su plantilla (o con el copy que defina el dueño). Esta
# lista solo puede encoger: una página nueva o migrada que lo diga falla.
VISITA_PENDIENTES = frozenset({
    "blog/cesped-amarillo-tampico-causas-soluciones/index.html",
    "blog/cuando-regar-pasto-san-agustin-tampico/index.html",
    "blog/sistema-riego-automatizado-tampico/index.html",
    "diseno-jardines-tampico/index.html",
    "jardineria-aguila-tampico/index.html",
    "jardineria-altamira/index.html",
    "jardineria-ciudad-madero/index.html",
    "jardineria-country-club-tampico/index.html",
    "jardineria-lomas-de-rosales-tampico/index.html",
    "jardineria-lomas-del-chairel-tampico/index.html",
    "mantenimiento-jardines-tampico/index.html",
    "precios/index.html",
    "sistema-riego-tampico/index.html",
})


def sin_valores_css(css):
    """CSS sin los valores "clip" de propiedades (text-overflow: clip, clip: rect()), que no son la marca."""
    return re.sub(r":\s*clip\b", ":", css, flags=re.I)


def textos_publicos(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    scripts = " ".join(re.findall(r'<script\b(?![^>]*application/ld\+json)[^>]*>(.*?)</script>', html, re.S | re.I))
    estilos = sin_valores_css(" ".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, re.S | re.I)))
    atributos = " ".join(re.findall(r'\b(?:content|alt|title|aria-label|placeholder)="([^"]*)"', html))
    mensajes = " ".join(unquote(t) for t in re.findall(r'https://wa\.me/\d+\?text=([^"\'&\s<]*)', html))
    cuerpo = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", html, flags=re.S | re.I)
    cuerpo = re.sub(r"<!--.*?-->", " ", cuerpo, flags=re.S)
    cuerpo = re.sub(r"<[^>]+>", " ", cuerpo)
    texto = re.sub(r"\s+", " ", html_mod.unescape(" ".join([cuerpo, ld, atributos, mensajes, scripts, estilos])))
    for permitida in PERMITIDAS:
        texto = texto.replace(permitida, "")
    return texto


def publicados():
    for path in sorted(PUBLIC.rglob("*.html")):
        yield path, textos_publicos(path.read_text(encoding="utf-8"))
    for ext in ("js", "css", "txt", "xml"):
        for path in sorted(PUBLIC.rglob(f"*.{ext}")):
            if "/tests/" not in path.as_posix():
                texto = path.read_text(encoding="utf-8")
                yield path, sin_valores_css(texto) if ext == "css" else texto


def archivos_fuente():
    """HTML y JS publicados (sin las pruebas), completos: para las reglas que miran el código y no solo el texto."""
    for ext in ("html", "js"):
        for path in sorted(PUBLIC.rglob(f"*.{ext}")):
            if "/tests/" not in path.as_posix():
                yield path, path.read_text(encoding="utf-8")


WA_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send\?phone=)/?([^\s\"'`?&<>]*)")
TEXTO_WA_RE = re.compile(r"wa\.me/\d+\?(?:[^\"'`\s<>]*&)?text=([^\"'`\s<>&]*)")
NUMERO = "528333268008"
CORREO_RE = re.compile(r"(?:mailto:|formsubmit\.co/(?:ajax/)?)([\w.+-]+@[\w.-]+)")


class ReglasDelDuenoTest(unittest.TestCase):
    def test_sin_palabras_prohibidas(self):
        hallazgos = []
        for path, texto in publicados():
            for regla, patron in PROHIBIDAS:
                for m in re.finditer(patron, texto, re.I):
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {regla} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

    def test_todo_whatsapp_va_al_numero_real(self):
        hallazgos = []
        for path, fuente in archivos_fuente():
            for m in WA_RE.finditer(fuente):
                destino = m.group(1)
                if destino and set(destino) == {"."}:  # "wa.me/..." en un comentario
                    continue
                if destino.isdigit():
                    ok = destino == NUMERO
                elif destino == "${wa}" and "dataset.wa" in fuente:  # vt-medidor.js: data-wa lo escribe datos.py
                    ok = True
                else:  # wa.me/${PHONE} o wa.me/52${WA}: la constante del archivo debe ser el número real
                    ok = NUMERO[2:] in fuente
                if not ok:
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {fuente[m.start():m.end() + 20]}")
        self.assertEqual(hallazgos, [])

    def test_mensajes_de_whatsapp_sin_marcado(self):
        hallazgos = []
        for path, fuente in archivos_fuente():
            for m in TEXTO_WA_RE.finditer(html_mod.unescape(fuente)):
                texto = unquote(m.group(1))
                if "<" in texto:
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {texto[:80]}")
        self.assertEqual(hallazgos, [])

    def test_sin_aggregate_rating_ni_feed_de_actividad(self):
        hallazgos = [str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob("activity-feed*")]
        for path, fuente in archivos_fuente():
            for patron in (r"aggregateRating", r"activity-feed", r"Actividad t[ií]pica", r"acaba de (?:comprar|cotizar|pedir)"):
                if re.search(patron, fuente, re.I):
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {patron}")
        self.assertEqual(hallazgos, [])

    def test_para_llevar_hoy_solo_toscana_18_y_28(self):
        hallazgos = []
        for path, texto in publicados():
            for m in re.finditer(r"llevar hoy", texto, re.I):
                ventana = texto[max(0, m.start() - 120):m.start()]
                modelos = re.findall(r"\b(Aruba|Bali|Capri|Irlanda|Japon[eé]s|M[oó]naco|Toscana|Viena)\s*(\d+)", ventana, re.I)
                if not modelos or modelos[-1][0].lower() != "toscana" or modelos[-1][1] not in ("18", "28"):
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · …{ventana[-60:]}llevar hoy…")
        self.assertEqual(hallazgos, [])

    def test_primer_riego_nunca_incluido(self):
        hallazgos = [f"{p.relative_to(PUBLIC)}" for p, texto in publicados()
                     if re.search(r"primer riego\W+(?:\w+\W+){0,2}incluido", texto, re.I)]
        self.assertEqual(hallazgos, [])

    def test_formularios_y_correos_a_la_cuenta_oficial(self):
        hallazgos = []
        for path, fuente in archivos_fuente():
            for m in CORREO_RE.finditer(fuente):
                if m.group(1).lower() != "viverosterra@hotmail.com":
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {m.group(0)}")
            for accion in re.findall(r'<form\b[^>]*\baction="([^"]*)"', fuente, re.I):
                if accion and "formsubmit.co" not in accion:
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · form a {accion}")
        self.assertEqual(hallazgos, [])

    def test_sin_padel_ni_canchas_en_pasto_sintetico(self):
        hallazgos = []
        for path, texto in publicados():
            for m in DEPORTES_RE.finditer(texto):
                ventana = texto[max(0, m.start() - 150):m.end() + 150].lower()
                if re.search(r"sint[eé]tic", ventana) and "natural" not in ventana:
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · …{ventana}…")
        self.assertEqual(hallazgos, [])

    def test_sin_pago_al_ver_el_jardin_terminado(self):
        hallazgos = []
        for path, texto in publicados():
            for m in PAGO_AL_TERMINAR_RE.finditer(texto):
                hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

    def test_nunca_visita_gratis(self):
        con = {}
        for path, texto in publicados():
            for m in VISITA_GRATIS_RE.finditer(texto):
                con.setdefault(path.relative_to(PUBLIC).as_posix(), f"…{texto[max(0, m.start() - 40):m.end() + 20]}…")
        self.assertEqual({k: v for k, v in con.items() if k not in VISITA_PENDIENTES}, {})
        self.assertEqual(sorted(VISITA_PENDIENTES - set(con)), [], "ya no lo dicen: sácalas de VISITA_PENDIENTES")

    def test_visita_gratis_se_detecta(self):
        for sucio in ("Agendamos una visita sin costo", "Visita técnica gratuita", "vamos a medir sin costo",
                      "Visita y medición Sin costo", "visita gratis"):
            self.assertRegex(sucio, VISITA_GRATIS_RE)
        for limpio in ("Agendamos una visita para medir y cotizar", "Cotización gratis por WhatsApp",
                       "la reponemos sin costo", "Visítanos en el vivero"):
            self.assertNotRegex(limpio, VISITA_GRATIS_RE)

    def test_deportes_solo_se_marcan_con_sintetico(self):
        def marcado(texto):
            m = DEPORTES_RE.search(texto)
            ventana = texto[max(0, m.start() - 150):m.end() + 150].lower()
            return bool(re.search(r"sint[eé]tic", ventana)) and "natural" not in ventana

        self.assertTrue(marcado("Instalamos pasto sintético para tu cancha de pádel"))
        self.assertFalse(marcado("Riego y pasto natural para canchas de fútbol"))
        self.assertTrue(PAGO_AL_TERMINAR_RE.search("Pagas cuando ves tu jardín terminado"))
        self.assertTrue(PAGO_AL_TERMINAR_RE.search("Pagas al ver el resultado"))

    def test_las_reglas_detectan_lo_que_deben(self):
        texto = textos_publicos(
            '<p>Pasto Oasis</p><p>Paga con Clip</p><p>12 MSI</p><p>meses sin intereses</p><p>0% de interés</p>'
            '<p>Envío gratis a todo México</p><p>Pide tus muestras gratis</p>'
            '<p>Ahorra 40% de agua; total 100%; aumento de +10.5%</p><p>clip-path</p>'
        )
        detectadas = {regla for regla, patron in PROHIBIDAS if re.search(patron, texto, re.I)}
        self.assertEqual(detectadas, {regla for regla, _ in PROHIBIDAS} - {"marca de proveedor de pasto sintético"})
        regla = dict(PROHIBIDAS)
        for limpio in ("<p>40% de agua, 100% natural, +10.5%</p>", "<p>0% químicos en el sustrato</p>",
                       "<p>Paga con tarjeta; ahorra 40% de agua</p>"):
            self.assertIsNone(re.search(regla["0 % en pagos"], textos_publicos(limpio), re.I), limpio)
        for sucio in ("<p>6 meses al 0%</p>", "<p>Mensualidades con 0 % de comisión</p>"):
            self.assertIsNotNone(re.search(regla["0 % en pagos"], textos_publicos(sucio), re.I), sucio)
        for limpio in ("<style>.a{clip-path:inset(0);clip:rect(0,0,0,0)}</style><p>casa muestra</p>",
                       "<p>No ofrecemos muestras físicas</p>"):
            texto = textos_publicos(limpio)
            self.assertEqual([r for r, pat in PROHIBIDAS if re.search(pat, texto, re.I)], [], limpio)
        self.assertEqual([r for r, pat in PROHIBIDAS if re.search(pat, textos_publicos(
            "<script>pagar('Paga con Clip')</script>"), re.I)], ["nombre del proveedor de la terminal"])
        self.assertEqual([r for r, pat in PROHIBIDAS if re.search(pat, sin_valores_css(
            ".a{text-overflow:clip!important;clip: rect(0 0 0 0)}"), re.I)], [])
        self.assertTrue(TEXTO_WA_RE.search('href="https://wa.me/528333268008?text=Hola%3Csvg%3E"'))
        self.assertEqual(WA_RE.search("https://wa.me/5218331234567?text=x").group(1), "5218331234567")
        self.assertEqual(CORREO_RE.search('action="https://formsubmit.co/ajax/otro@gmail.com"').group(1), "otro@gmail.com")
        js = "el.style.clip = 'auto'; ctx.clip(); x.clipPath"
        self.assertIsNone(re.search(regla["nombre del proveedor de la terminal"], js, re.I))
        self.assertIsNotNone(re.search(regla["muestras gratis o físicas"], "Te enviamos muestras a domicilio", re.I))


if __name__ == "__main__":
    unittest.main()
