"""Reglas del dueño en las 6 zonas y en /precios (Etapa 2g): precios solo de datos.py (o de tools/pasto/data.py para el
sintético por modelo y de tools/pasto/mensualidades.py para los mínimos por plazo; lo demás "según cotización"), sin
"gratis" ni "sin costo" (salvo la garantía de arraigo que aprobó el dueño), sin existencias ("sujeto a disponibilidad"
solo junto al precio del mármol), sin distancias ni tiempos de llegada, sin casos ni opiniones de la zona (ninguno tiene
permiso), sin superlativos, sin pesos de costal ni medidas de piedra bola, "sin mínimo" solo como datos.SIN_MINIMO, sin
la fecha de vigencia que el dueño no ha confirmado, pago con anticipo, la visita con su costo, las mismas fotos de main
en su orden y las mismas anclas.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca las
suyas) y al cerrar la Etapa 2g queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al sys.path)
import data  # noqa: E402
import datos  # noqa: E402
import mensualidades  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import paridad_zonas  # noqa: E402
from componentes import dinero  # noqa: E402

PUBLIC = paginas.PUBLIC
ZONAS = tuple(ruta for _nombre, ruta in datos.ZONAS)
PAGINAS = ZONAS + ("/precios",)
PENDIENTES = frozenset()
CAPTURA = json.loads(paridad_zonas.CAPTURA.read_text(encoding="utf-8"))
PERMITIDOS = ({dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))}
              | {dinero(m[k]) for m in data.MODELOS for k in ("t1", "t2", "rollo")}
              | {dinero(minimo) for minimo, _plazos in mensualidades.UMBRALES})
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Lo que el dueño dejó "según cotización" (2026-11-08): la piedra bola y el m³ y el camión del tezontle. Con un precio
# cerca es un precio inventado; como $200 y $1,500 sí están en datos.py, solo se detecta por cercanía.
SIN_PRECIO_RE = re.compile(r"piedra bola[^.$]{0,40}\$\s?\d|tezontle[^.$]{0,60}(?:\bm³|cami[oó]n)[^.$]{0,30}\$\s?\d", re.I)
# Palabras del dueño para el mármol (2026-11-08): "sujeto a disponibilidad" solo junto a su precio, y solo en /precios.
MARMOL_CONDICION_RE = re.compile(re.escape(datos.MARMOL_CONDICION), re.I)
JUNTO_AL_PRECIO = 120  # caracteres
# El precio escrito o, en el Offer del JSON-LD (description junto a price), su price.
MARMOL_PRECIO_RE = re.compile(re.escape(dinero(datos.PRECIOS["marmol_saco"])) + rf'|"price":\s*"?{datos.PRECIOS["marmol_saco"]}\b')
# La única frase con "sin costo" que aprobó el dueño (spec, Decisiones: garantía de pasto ligada a sus condiciones).
GARANTIA_PASTO = "la reponemos sin costo"
SIN_VERIFICAR = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b|\bsin cargo\b"),
    ("existencias o disponibilidad", r"InStock|\bdisponibilidad\b|\ben existencia\b|\bdisponibles? (?:hoy|ya)\b|\bagotad"),
    ("distancia o tiempo de llegada", r"\bminutos?\b|\bllegamos en\b|\b\d+\s?km\b|\bkil[oó]metros?\b|\bcuadras\b"
                                      r"|\bmismo d[ií]a\b|\bhoy mismo\b|entrega inmediata|\ben 24 ?h"),
    ("más vendido o superlativo", r"m[aá]s vendid|\bel mejor\b|\blos mejores\b|\bl[ií]der\b|\bimbatible\b"
                                  r"|m[aá]s popular|\bexpertos\b"),
    ("En nuestro vivero", r"en nuestro vivero"),
    ("nunca Oasis ni MSI", r"\bOasis\b|\bMSI\b|sin intereses|meses sin"),
    # Respuestas del dueño (2026-11-08): sin peso de costal, piedra bola a granel y nunca "camión desde $5,000". "Sin
    # mínimo" solo con las palabras de datos.SIN_MINIMO, que se quitan antes de buscar.
    ("peso o medidas sin confirmar", r"\b\d+\s?kg\b|chica, mediana|tres medidas|\bpor medida\b"),
    ("término comercial sin confirmar", r"\bsin m[ií]nimo\b|cami[oó]n[^.]{0,20}desde"),
    ("fecha de vigencia sin confirmar", r"vigente desde|\bactualizada en\b"),
)


def html_de(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def visible_y_ld(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    titulo = " ".join(re.findall(r"<title>(.*?)</title>", html))
    return " ".join((paridad.texto(paridad.principal(html)), ld, metas, titulo))


def fallas(ruta):
    """Lista de reglas que rompe la página (vacía si cumple todas)."""
    html = html_de(ruta)
    texto = visible_y_ld(html)
    salida = [f"precio que no está en datos.py: {p}"
              for p in sorted({m.group(0).replace(" ", "") for m in PRECIO_RE.finditer(texto)} - PERMITIDOS)]
    salida += [f"presentación sin precio publicado con precio: …{m.group(0)}…" for m in SIN_PRECIO_RE.finditer(texto)]
    limpio = texto.replace(GARANTIA_PASTO, "").replace(datos.SIN_MINIMO, " ")
    if ruta == "/precios":
        salida += [f"“sujeto a disponibilidad” lejos del precio: …{texto[max(0, m.start() - 40):m.end()]}…"
                   for m in MARMOL_CONDICION_RE.finditer(texto)
                   if not MARMOL_PRECIO_RE.search(texto[max(0, m.start() - JUNTO_AL_PRECIO):m.end() + JUNTO_AL_PRECIO])]
        limpio = MARMOL_CONDICION_RE.sub(" ", limpio)
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, limpio, re.I)]
    cuerpo = paridad.principal(html)
    if re.search(r'class="vt-testimonio|<blockquote', cuerpo):
        salida.append("opinión o caso de la zona sin permiso del dueño")
    if datos.ANTICIPO not in texto:
        salida.append("sin datos.ANTICIPO")
    if "visita" in texto.lower() and datos.VISITA_COSTO not in texto:
        salida.append("habla de la visita sin datos.VISITA_COSTO")
    if 'class="vt-pagina' not in html or "tienda-pasto.css" in html or "fonts.googleapis" in html:
        salida.append("no sale de su plantilla (CSS viejo o Google Fonts)")
    nuevas = paridad_zonas.extraer(ruta)
    if [f["src"] for f in nuevas["fotos"]] != [f["src"] for f in CAPTURA[ruta]["fotos"]]:
        salida.append(f"fotos distintas a las de main o en otro orden: {[f['src'] for f in nuevas['fotos']]}")
    for vieja, nueva in zip(CAPTURA[ruta]["fotos"], nuevas["fotos"]):
        if vieja["srcset"] != nueva["srcset"]:
            salida.append(f"srcset distinto en {vieja['src']}")
        if "en nuestro vivero" in (nueva["alt"] or "").lower():
            salida.append(f"alt con «En nuestro vivero»: {nueva['src']}")
    faltan = sorted(set(CAPTURA[ruta]["anclas"]) - set(nuevas["anclas"]))
    if faltan:
        salida.append(f"anclas de main que ya no existen: {faltan}")
    for img in re.findall(r"<img\b[^>]*>", cuerpo):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    return salida


class ZonasReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(PAGINAS) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_zonas_de_datos_son_las_capturadas(self):
        self.assertEqual(sorted(PAGINAS), sorted(CAPTURA))

    def test_las_reglas_detectan_lo_que_deben(self):
        for frase in ("Cotización gratis", "visita sin costo", "availability InStock", "A minutos del vivero",
                      "llegamos en 30 minutos", "a 5 km del vivero", "el mejor pasto", "En nuestro vivero",
                      "más vendido", "empresa líder", "12 MSI", "Saco de unos 20 kg", "Chica, mediana y grande",
                      "camión desde $5,000", "Sin mínimo", "Lista vigente desde noviembre 2026"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        for frase in ("Piedra bola de río, costal $350", "Tezontle por m³ $1,500", "Tezontle en camión $8,000"):
            with self.subTest(frase=frase):
                self.assertTrue(SIN_PRECIO_RE.search(frase))
        for frase in ("Tierra preparada $100", "Saco de mármol $250", "Camión de 8 m³ $5,200"):
            with self.subTest(frase=frase):
                self.assertFalse(SIN_PRECIO_RE.search(frase))
        for limpio in ("Sin mínimo de compra.".replace(datos.SIN_MINIMO, " "), "Respondemos en menos de 1 hora en horario", "desde 2007 · 15 a 20 días de arraigo",
                       "Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo"):
            with self.subTest(limpio=limpio):
                texto = limpio.replace(GARANTIA_PASTO, "")
                self.assertFalse(any(re.search(patron, texto, re.I) for _r, patron in SIN_VERIFICAR))


if __name__ == "__main__":
    unittest.main()
