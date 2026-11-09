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
CREDITO_CLIENTES_RE = re.compile(r"\bcr[eé]dito\s+(?:para|a)\s+(?:(?:los|sus|nuestros)\s+)?clientes\b"
                                 r"|\bpago\s+diferido\b|\ba\s+cr[eé]dito\s+para\s+(?:proyectos|empresas|obras?)\b", re.I)
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
# Decisión del dueño (2026-11-07): Viveros Terra no tiene registro, certificación ni certificado SENASICA en ninguna
# forma; tampoco certificados fitosanitarios ni SADER. En ninguna página, JSON-LD, llms.txt ni blog. Sin excepciones.
# Decisión del dueño (2026-11-08): "sin costo" solo en la garantía de arraigo del pasto (la "sección" que no arraiga);
# en plantas y palmas la garantía dice "la reponemos." a secas.
REPOSICION_SIN_COSTO_RE = re.compile(r"\brepon\w*(?:\s+\w+){0,2}?\s+sin\s+costo", re.I)
CERTIFICACION_RE = re.compile(
    r"\bSENASICA\b|\bSADER\b"
    r"|\b(?:certificad[oa]s?|certificaci[oó]n|registro|constancia|permiso)\W+(?:\w+\W+){0,2}?fitosanitari\w*"
    r"|\bfitosanitari\w*\W+(?:\w+\W+){0,3}?(?:emitid\w*|vigente|oficial|por\s+estado)", re.I)
CERTIFICACION_PENDIENTES = frozenset()
# Tampoco se publica que el riego (ni otro servicio) "se amortiza", "se paga solo", en "cuántos meses se paga", la
# "recuperación de la inversión" ni el "payback". Se habla de lo que se ahorra: "ahorra hasta 40% de agua". Sin excepciones.
AMORTIZA_RE = re.compile(
    r"\bse\s+pagan?\s+sol[oa]s?\b|\bcu[aá]nt[oa]s?\s+(?:meses|años|tiempo)\s+se\s+pagan?\b|\bamortiz\w*"
    r"|\brecupera(?:r|s|n)?\s+(?:la|tu|su)\s+inversi[oó]n\b|\brecuperaci[oó]n\s+(?:de\s+(?:la\s+|tu\s+)?)?inversi[oó]n\b"
    r"|\btiempo\s+de\s+recuperaci[oó]n\b|\bpayback\b", re.I)
AMORTIZA_PENDIENTES = frozenset()
# Decisión del dueño (2026-11-08): la cotización no se anuncia como "gratis"; se dice "Cotiza por WhatsApp."
COTIZA_GRATIS_RE = re.compile(r"\bcotiza\w*\W+(?:\w+\W+){0,4}?(?:gratis|gratuit\w*)\b", re.I)
# Decisión del dueño (2026-11-08): el pasto natural, las plantas, los árboles y las palmas no llevan IVA. Ninguno de sus
# precios va junto a "con IVA" en la misma etiqueta, tabla o frase. No cuentan "salvo las palmas", la poda de palmas (es un
# servicio) ni el pasto sintético. Pendiente de decidir por el dueño: el precio de pasto *instalado* cuando va solo.
IVA_INCLUIDO_RE = re.compile(r"\bcon\s+IVA\b|\bIVA\s+incluido\b(?!\s+cuando\s+aplica)|\bincluyen?\s+(?:el\s+)?IVA\b", re.I)
SIN_IVA_RE = re.compile(r"\bpalmas?\b|\bareca\b|\bcoco\s+plumoso\b|\bpasto\b(?!\s+sint[eé]tico)|\bSan\s+Agust[ií]n\b"
                        r"|\bplantas?\b|\b[aá]rbol(?:es)?\b|\bflamboy[aá]n\b", re.I)
FILA_SIN_IVA_RE = re.compile(r"(?:palmas?|pasto\s+san\s+agust[ií]n(?!\s+instalado)|solo\s+el\s+pasto|mayoreo(?:\s+de\s+pasto)?,?\s+solo"
                             r"|[aá]rboles|plantas)\b", re.I)
PRECIO_RE = re.compile(r"\$\s?\d")
SALVEDAD_RE = re.compile(r"salvo\s+las\s+palmas|poda\s+de\s+palmas", re.I)
INSTALADO_PENDIENTE_RE = re.compile(r"\binstalado\b", re.I)
SOLO_PASTO_RE = re.compile(r"\bsolo\s+(?:el\s+)?pasto\b", re.I)
ETIQUETA_RE = re.compile(r'<div class="vt-etiqueta(?: [^"]*)?"[^>]*>(.*?)</div>', re.S)
TABLA_RE = re.compile(r"<table\b.*?</table>", re.S | re.I)
FILA_RE = re.compile(r"<tr\b.*?</tr>", re.S | re.I)
CAPTION_RE = re.compile(r"<caption\b[^>]*>(.*?)</caption>", re.S | re.I)
BLOQUE_RE = re.compile(r"</?(?:p|li|div|h[1-6]|td|th|tr|caption|ul|ol|section|table|details|summary)\b[^>]*>", re.I)
FRASE_RE = re.compile(r"(?<=[.!?])\s+")


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


def reposiciones_que_no_son_de_pasto(texto):
    """Frases con "repon… sin costo" que no hablan de una sección de pasto: solo esa garantía puede decirlo."""
    salida = []
    for m in REPOSICION_SIN_COSTO_RE.finditer(texto):
        frase = texto[texto.rfind(". ", 0, m.start()) + 1:m.end()].strip()
        if not re.search(r"secci[oó]n", frase, re.I):
            salida.append(frase)
    return salida


def _plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def _anuncia_iva_sin_iva(texto):
    """Dice "con IVA" junto a un precio de pasto natural, planta, árbol o palma (lo solo instalado sigue pendiente)."""
    if not (IVA_INCLUIDO_RE.search(texto) and SIN_IVA_RE.search(texto) and PRECIO_RE.search(texto)):
        return False
    pendiente = INSTALADO_PENDIENTE_RE.search(texto) and not SOLO_PASTO_RE.search(texto)
    return not (SALVEDAD_RE.search(texto) or pendiente)


def iva_en_precios_sin_iva(html):
    """Etiquetas, tablas y frases (visibles, meta y JSON-LD) que presentan con IVA un precio que no lo lleva."""
    salida = [f"etiqueta: {_plano(e)}" for e in ETIQUETA_RE.findall(html) if _anuncia_iva_sin_iva(_plano(e))]
    for tabla in TABLA_RE.findall(html):
        caption = " ".join(CAPTION_RE.findall(tabla))
        filas = [f for f in map(_plano, FILA_RE.findall(tabla)) if FILA_SIN_IVA_RE.match(f) and PRECIO_RE.search(f)]
        if filas and IVA_INCLUIDO_RE.search(caption) and not SALVEDAD_RE.search(caption):
            salida.append(f"tabla: {_plano(caption)} · {filas[0]}")
    principal = re.search(r"<main\b.*?</main>", html, re.S | re.I)
    cuerpo = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", principal.group() if principal else html, flags=re.S | re.I)
    fragmentos = [_plano(b) for b in BLOQUE_RE.split(cuerpo)]
    fragmentos += re.findall(r'<meta\b[^>]*\bcontent="([^"]*)"', html)
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        fragmentos += re.findall(r'"((?:[^"\\]|\\.)*)"', ld)
    salida += [f"frase: {f}" for fragmento in fragmentos for f in FRASE_RE.split(html_mod.unescape(fragmento))
               if _anuncia_iva_sin_iva(f)]
    return salida


def archivos_fuente():
    """HTML y JS publicados (sin las pruebas), completos: para las reglas que miran el código y no solo el texto."""
    for ext in ("html", "js"):
        for path in sorted(PUBLIC.rglob(f"*.{ext}")):
            if "/tests/" not in path.as_posix():
                yield path, path.read_text(encoding="utf-8")


WA_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send\?phone=)/?([^\s\"'`?&<>]*)")
TEXTO_WA_RE = re.compile(r"wa\.me/\d+\?(?:[^\"'`\s<>]*&)?text=([^\"'`\s<>&]*)")
NUMERO = "528333268008"
# Páginas con formulario por correo a formsubmit: cuestionario, materiales y, desde 2d, las dos páginas para empresas.
CON_FORMULARIO_CORREO = ("cuestionario.html", "marmol-blanco-tampico/index.html", "piedra-bola-rio-tampico/index.html",
                         "tezontle-rojo-tampico/index.html", "tierra-negra-vegetal-tampico/index.html",
                         "mayoreo-pasto-tampico/index.html", "palmas-mayoreo-proyectos/index.html")
MINIMO_ESPECIE_RE = re.compile(r"\b50\s+(?:ejemplares|palmas|piezas)?\s*(?:de\s+la\s+misma\s+especie|por\s+especie)\b"
                               r"|\b50\s+por\s+especie\b", re.I)
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

    def test_formularios_por_correo_solo_donde_el_dueno_los_quiere(self):
        """Respuesta del dueño (2026-11-08): las páginas para empresas conservan un formulario por correo para compras
        (además de WhatsApp). La home y pasto en rollo siguen sin formulario (test_inicio, test_pasto_en_rollo)."""
        con_formulario = sorted(str(path.relative_to(PUBLIC)) for path, fuente in archivos_fuente()
                                if path.suffix == ".html" and re.search(r'<form\b[^>]*\baction="https://formsubmit\.co/',
                                                                        fuente))
        self.assertEqual(con_formulario, sorted(CON_FORMULARIO_CORREO))

    def test_sin_minimo_fijo_por_especie(self):
        """Respuesta del dueño (2026-11-08): no hay mínimo fijo por especie (main decía "50 ejemplares")."""
        hallazgos = [f"{p.relative_to(PUBLIC)}" for p, texto in publicados() if MINIMO_ESPECIE_RE.search(texto)]
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
        for sucio in ("crédito para clientes recurrentes", "Crédito a clientes recurrentes", "crédito a nuestros clientes",
                      "¿Aceptan pago diferido o a crédito para proyectos?", "a crédito para empresas"):
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
        for regla, patron, pendientes in (("SENASICA/SADER/fitosanitario", CERTIFICACION_RE, CERTIFICACION_PENDIENTES),
                                          ("amortización", AMORTIZA_RE, AMORTIZA_PENDIENTES)):
            con = {}
            for path, texto in publicados():
                for m in patron.finditer(texto):
                    con.setdefault(path.relative_to(PUBLIC).as_posix(), f"…{texto[max(0, m.start() - 40):m.end() + 20]}…")
            with self.subTest(regla=regla):
                self.assertEqual(pendientes, frozenset(), "sin excepciones: la lista se queda vacía")
                self.assertEqual(con, {})

    def test_senasica_y_amortizacion_se_detectan(self):
        for sucio in ("Certificación SENASICA", "registro Senasica", "Emitido por SADER", "certificado fitosanitario",
                      "Certificado fitosanitario por estado", "certificación fitosanitaria", "fitosanitario emitido",
                      "constancia fitosanitaria", "se amortiza en 18–24 meses", "tarda 4+ años en amortizarse",
                      "Se paga solo en 18-24 meses", "se paga sola en 24 meses", "se amortiza en 18 a 24 meses",
                      "en cuántos meses se paga solo un sistema", "cuándo se paga solo", "sistemas que se pagan solos",
                      "en cuántos meses se paga", "recupera la inversión en 18 a 24 meses",
                      "recuperación inversión 18-24 meses", "Tiempo de recuperación de la inversión: 12–15 meses",
                      "Payback: 30 meses"):
            self.assertTrue(CERTIFICACION_RE.search(sucio) or AMORTIZA_RE.search(sucio), sucio)
        for limpio in ("Ahorra hasta 40% de agua", "se paga en mensualidades con tarjeta de crédito",
                       "cuánto puedes ahorrar en agua", "Factura emitida el día del pago", "la recuperación del pasto",
                       "¿Cuándo se paga el anticipo?"):
            self.assertFalse(CERTIFICACION_RE.search(limpio) or AMORTIZA_RE.search(limpio), limpio)

    def test_reposicion_sin_costo_solo_en_pasto(self):
        hallazgos = [f"{path.relative_to(PUBLIC).as_posix()}: {frase}" for path, texto in publicados()
                     for frase in reposiciones_que_no_son_de_pasto(texto)]
        self.assertEqual(hallazgos, [])

    def test_reposicion_sin_costo_se_detecta(self):
        for sucio in ("Si una planta que sembramos no prende en 30 días, la reponemos sin costo.",
                      "si no prenden y se regaron como indicamos, las reponemos sin costo. No cubre falta de riego",
                      "Garantía de arraigo 30 días: reponemos plantas sin costo",
                      "Garantía de arraigo 30 días: reponemos sin costo las plantas que sembramos"):
            self.assertTrue(reposiciones_que_no_son_de_pasto(sucio), sucio)
        for limpio in ("Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo",
                       "Si una planta que sembramos no prende en 30 días, la reponemos.",
                       "fugas o fallas por causas de la instalación se atienden sin costo adicional"):
            self.assertFalse(reposiciones_que_no_son_de_pasto(limpio), limpio)

    def test_nunca_cotizacion_gratis(self):
        hallazgos = [f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…"
                     for path, texto in publicados() for m in COTIZA_GRATIS_RE.finditer(texto)]
        self.assertEqual(hallazgos, [])

    def test_cotizacion_gratis_se_detecta(self):
        for sucio in ("Cotización gratis hoy.", "Cotiza gratis.", "Cotiza gratis por WhatsApp.", "cotizamos tu jardín gratis",
                      "Cotización 100% gratuita"):
            self.assertRegex(sucio, COTIZA_GRATIS_RE)
        for limpio in ("Cotiza por WhatsApp.", "Recoger en showroom — Sin costo", "te escribimos con tu cotización"):
            self.assertNotRegex(limpio, COTIZA_GRATIS_RE)

    def test_ningun_precio_sin_iva_dice_con_iva(self):
        hallazgos = [f"{path.relative_to(PUBLIC)} · {h}" for path in sorted(PUBLIC.rglob("*.html"))
                     for h in iva_en_precios_sin_iva(path.read_text(encoding="utf-8"))]
        self.assertEqual(hallazgos, [])

    def test_calculadoras_de_pasto_natural_sin_iva(self):
        for nombre in ("vt-medidor.js", "vt-b2b.js"):
            self.assertNotRegex((PUBLIC / "js" / nombre).read_text(encoding="utf-8"), r"(?i)\bcon IVA\b")

    def test_precio_sin_iva_con_iva_se_detecta(self):
        tarjeta = ('<div class="vt-etiqueta"><p class="vt-etiqueta__cod"><span>Vivero</span><span>{}</span></p>'
                   '<p class="vt-etiqueta__nombre">{}</p><p class="vt-etiqueta__precio"><b>$250</b></p></div>')
        tabla = '<table><caption>{}</caption><tr><th scope="row">{}</th><td>pieza</td><td>desde $250</td></tr></table>'
        for sucio in (tarjeta.format("Con IVA", "Palmas"), tarjeta.format("Con IVA", "Pasto San Agustín"),
                      tarjeta.format("Con IVA", "Flamboyán"),
                      tabla.format("Precios 2026 con IVA.", "Palmas"), tabla.format("Precios 2026 con IVA.", "Árboles"),
                      tabla.format("Con IVA.", "Pasto San Agustín, solo el pasto"),
                      "<main><p>Areca y coco plumoso desde $250 y palma real desde $500 en tamaño chico, con IVA.</p></main>",
                      "<main><p>El pasto cuesta $85 por m² solo el pasto y desde $120 por m² instalado, con IVA incluido.</p></main>",
                      '<meta name="description" content="Palma areca desde $250, IVA incluido.">'):
            self.assertTrue(iva_en_precios_sin_iva(sucio), sucio)
        for limpio in (tarjeta.format("", "Palmas"), tarjeta.format("Con IVA", "Pasto instalado"),
                       tarjeta.format("Con IVA", "Pasto sintético"), tarjeta.format("Con IVA", "Tezontle rojo"),
                       tabla.format("Precios 2026 con IVA, salvo las palmas, que no llevan IVA.", "Palmas"),
                       tabla.format("Precios 2026 con IVA.", "Poda de palmas y árboles"),
                       tabla.format("Precios 2026 con IVA.", "Pasto San Agustín instalado"),
                       "<main><p>Areca y coco plumoso desde $250. El pasto sintético cuesta $139/m², con IVA.</p></main>",
                       "<main><p>Precios 2026, IVA incluido cuando aplica; palma areca desde $250.</p></main>"):
            self.assertFalse(iva_en_precios_sin_iva(limpio), limpio)

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
