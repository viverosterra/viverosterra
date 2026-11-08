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
PERMITIDAS = ()  # 2b: el hub ya no cita el "envío gratis" de otras ofertas; no se agregan excepciones
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
# Decisión del dueño (2026-11-07): no le gusta "liquidas el saldo según lo acordado"; no se escribe ninguna frase sobre
# liquidar el saldo o el resto (el pago se explica con el anticipo y las formas de pago). Las citas de clientes no cuentan.
SALDO_RE = re.compile(r"\bliquid(?:as|a|amos|ar|es)\s+el\s+(?:saldo|resto)\b|\bel\s+(?:saldo|resto)\s+se\s+liquida\b", re.I)
# Decisión del dueño (2026-11-07): no se ofrece crédito a clientes (ni a instaladores ni a constructoras recurrentes).
CREDITO_CLIENTES_RE = re.compile(r"\bcr[eé]dito\s+(?:para|a)\s+(?:(?:los|sus|nuestros)\s+)?clientes\b", re.I)
# Decisión del dueño (2026-11-07): la visita para medir tiene costo o depende; nunca "visita sin costo", "visita
# gratis", "visita gratuita", "la visita no tiene costo", "sin cargo" ni "no cuesta" (tampoco "vamos a medir sin costo").
GRATIS = (r"(?:sin\s+(?:costo|cargo)|gratis|gratuit(?:[ao]s?|amente)|no\s+(?:tiene\s+(?:ning[uú]n\s+)?costo|cuesta"
          r"|se\s+cobra|cobramos|te\s+cobramos))")
VISITA_GRATIS_RE = re.compile(
    rf"\bvisit\w*\b\W+(?:\w+\W+){{0,4}}?{GRATIS}\b|\b(?:medir|medimos|medici[oó]n|diagn[oó]sticos?)\W+(?:\w+\W+){{0,2}}?{GRATIS}\b"
    rf"|\b{GRATIS}\W+(?:\w+\W+){{0,2}}?visitas?\b", re.I)
# Páginas que todavía lo dicen. Debe quedar vacía: ninguna página pública promete la visita, la medición ni el
# diagnóstico gratis. Esta lista solo puede encoger; no se agregan páginas nuevas.
VISITA_PENDIENTES = frozenset()
# Decisión del dueño (2026-11-07): no se publica el registro o certificación SENASICA ni que el riego "se amortiza" o
# "se paga solo en 18–24 meses". Las páginas que todavía lo dicen salen de su plantilla o se corrigen en su etapa
# (diseño, mantenimiento y riego en la 2c; mayoreo, vivero y materiales en la 2d–2g; los blogs de riego en la Etapa 3;
# el certificado fitosanitario SADER/SENASICA de palmas lo confirma el dueño). Solo puede encoger.
SENASICA_RE = re.compile(r"\bSENASICA\b", re.I)
AMORTIZA_RE = re.compile(r"\bse\s+(?:amortiza|paga\s+sol[oa])\s+en\s+(?:\d+\s*(?:–|-|a)\s*)?\d+\s+meses\b", re.I)
SENASICA_PENDIENTES = frozenset({
    "sistema-riego-tampico/index.html", "mayoreo-pasto-tampico/index.html", "vivero-tampico/index.html",
    "marmol-blanco-tampico/index.html", "tezontle-rojo-tampico/index.html", "palmas-mayoreo-proyectos/index.html",
})
AMORTIZA_PENDIENTES = frozenset({
    "sistema-riego-tampico/index.html", "blog/sistema-riego-automatico-conviene-tampico/index.html",
    "blog/sistema-riego-automatizado-tampico/index.html",
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

    def test_sin_liquidar_el_saldo(self):
        hallazgos = []
        for path, texto in publicados():
            for m in SALDO_RE.finditer(texto):
                hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

    def test_liquidar_el_saldo_se_detecta(self):
        for sucio in ("Liquidas el saldo según lo acordado en tu cotización", "El resto se liquida según lo acordado",
                      "liquidamos el saldo", "el saldo se liquida al terminar"):
            self.assertTrue(SALDO_RE.search(sucio), sucio)
        for limpio in ("Pagué el resto hasta que lo vi terminado", "Puedes pagar de contado o en mensualidades",
                       "Liquidambar styraciflua"):
            self.assertIsNone(SALDO_RE.search(limpio), limpio)

    def test_sin_credito_para_clientes(self):
        hallazgos = []
        for path, texto in publicados():
            for m in CREDITO_CLIENTES_RE.finditer(texto):
                hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

    def test_credito_y_pago_al_terminar_se_detectan_sin_tocar_citas_de_clientes(self):
        for sucio in ("crédito para clientes recurrentes", "Crédito a clientes recurrentes", "crédito a nuestros clientes"):
            self.assertRegex(sucio, CREDITO_CLIENTES_RE)
        for limpio in ("mensualidades con tarjeta de crédito", "tarjeta de débito o crédito para tu compra"):
            self.assertNotRegex(limpio, CREDITO_CLIENTES_RE)
        # La regla mira lo que promete la empresa ("pagas cuando ves"), no las palabras de un cliente real.
        self.assertIsNone(PAGO_AL_TERMINAR_RE.search("Lo más importante: pagué el resto hasta que lo vi terminado."))

    def test_nunca_visita_gratis(self):
        con = {}
        for path, texto in publicados():
            for m in VISITA_GRATIS_RE.finditer(texto):
                con.setdefault(path.relative_to(PUBLIC).as_posix(), f"…{texto[max(0, m.start() - 40):m.end() + 20]}…")
        self.assertEqual({k: v for k, v in con.items() if k not in VISITA_PENDIENTES}, {})
        self.assertEqual(sorted(VISITA_PENDIENTES - set(con)), [], "ya no lo dicen: sácalas de VISITA_PENDIENTES")

    def test_sin_senasica_ni_amortizacion_del_riego(self):
        for regla, patron, pendientes in (("SENASICA", SENASICA_RE, SENASICA_PENDIENTES),
                                          ("amortización", AMORTIZA_RE, AMORTIZA_PENDIENTES)):
            con = {}
            for path, texto in publicados():
                for m in patron.finditer(texto):
                    con.setdefault(path.relative_to(PUBLIC).as_posix(), f"…{texto[max(0, m.start() - 40):m.end() + 20]}…")
            with self.subTest(regla=regla):
                self.assertEqual({k: v for k, v in con.items() if k not in pendientes}, {})
                self.assertEqual(sorted(pendientes - set(con)), [], "ya no lo dicen: sácalas de la lista")

    def test_senasica_y_amortizacion_se_detectan(self):
        for sucio in ("Certificación SENASICA", "registro Senasica", "se amortiza en 18–24 meses",
                      "Se paga solo en 18-24 meses", "se paga sola en 24 meses", "se amortiza en 18 a 24 meses"):
            self.assertTrue(SENASICA_RE.search(sucio) or AMORTIZA_RE.search(sucio), sucio)
        for limpio in ("Ahorra hasta 40% de agua", "se paga en mensualidades con tarjeta de crédito"):
            self.assertFalse(SENASICA_RE.search(limpio) or AMORTIZA_RE.search(limpio), limpio)

    def test_visita_gratis_se_detecta(self):
        for sucio in ("Agendamos una visita sin costo", "Visita técnica gratuita", "vamos a medir sin costo",
                      "Visita y medición Sin costo", "visita gratis",
                      "ofrece visita de diagnóstico y cotización gratuita", "visita el terreno gratuitamente",
                      "La visita para medir no tiene costo", "La visita no tiene costo", "la visita no cuesta",
                      "visita de diagnóstico sin cargo", "medir no te cobramos", "Sin cargo, una visita",
                      "diagnóstico gratuito", "una visita de diagnóstico sin costo", "diagnósticos de pasto sin costo"):
            self.assertRegex(sucio, VISITA_GRATIS_RE)
        for limpio in ("Agendamos una visita para medir y cotizar", "Cotización gratis por WhatsApp",
                       "El costo de la visita para cotizar depende de la ubicación del servicio",
                       "Visita para medir y cotizar: su costo depende de la ubicación",
                       "la reponemos sin costo", "Visítanos en el vivero",
                       "el resto de Altamira, sin cargo extra por traslado", "no cuesta como un pasto de lujo"):
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
