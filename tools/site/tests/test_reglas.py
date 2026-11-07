"""Reglas permanentes del dueño sobre todo lo publicado en public/: texto visible, JSON-LD, atributos legibles
(content, alt, title, aria-label, placeholder) y mensajes de WhatsApp prellenados. Los .js, .txt y .xml se revisan
completos para las reglas de marcas y pagos."""
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
# Pendiente con fecha: la Etapa 1b (test_consistencia.py, plan 2026-11-07-etapa-1b) reescribe estas frases con su
# texto aprobado. Cualquier página nueva con "pagas cuando…" falla desde ya.
PAGO_AL_TERMINAR_PENDIENTE_1B = {"pasto-en-rollo-tampico/index.html"}


def textos_publicos(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    atributos = " ".join(re.findall(r'\b(?:content|alt|title|aria-label|placeholder)="([^"]*)"', html))
    mensajes = " ".join(unquote(t) for t in re.findall(r'https://wa\.me/\d+\?text=([^"\'&\s<]*)', html))
    cuerpo = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", html, flags=re.S | re.I)
    cuerpo = re.sub(r"<!--.*?-->", " ", cuerpo, flags=re.S)
    cuerpo = re.sub(r"<[^>]+>", " ", cuerpo)
    texto = re.sub(r"\s+", " ", html_mod.unescape(" ".join([cuerpo, ld, atributos, mensajes])))
    for permitida in PERMITIDAS:
        texto = texto.replace(permitida, "")
    return texto


def publicados():
    for path in sorted(PUBLIC.rglob("*.html")):
        yield path, textos_publicos(path.read_text(encoding="utf-8"))
    for ext in ("js", "txt", "xml"):
        for path in sorted(PUBLIC.rglob(f"*.{ext}")):
            if "/tests/" not in path.as_posix():
                yield path, path.read_text(encoding="utf-8")


class ReglasDelDuenoTest(unittest.TestCase):
    def test_sin_palabras_prohibidas(self):
        hallazgos = []
        for path, texto in publicados():
            for regla, patron in PROHIBIDAS:
                for m in re.finditer(patron, texto, re.I):
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {regla} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
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
            if path.relative_to(PUBLIC).as_posix() in PAGO_AL_TERMINAR_PENDIENTE_1B:
                continue
            for m in PAGO_AL_TERMINAR_RE.finditer(texto):
                hallazgos.append(f"{path.relative_to(PUBLIC)} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

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
        js = "el.style.clip = 'auto'; ctx.clip(); x.clipPath"
        self.assertIsNone(re.search(regla["nombre del proveedor de la terminal"], js, re.I))
        self.assertIsNotNone(re.search(regla["muestras gratis o físicas"], "Te enviamos muestras a domicilio", re.I))


if __name__ == "__main__":
    unittest.main()
