"""Reglas del dueño en las páginas de materiales (Etapa 2f): precios solo de datos.py (lo demás "según cotización"), sin
"gratis" ni existencias ni plazos de entrega, sin superlativos ni cifras sin respaldo, sin opiniones sin permiso, sin
"En nuestro vivero" en fotos, sin window.open, las mismas fotos de main en su orden y el formulario de pedido intacto.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca la
suya) y al cerrar la Etapa 2f queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import medicion_js  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import paridad_materiales  # noqa: E402
from componentes import dinero  # noqa: E402

PUBLIC = paginas.PUBLIC
MATERIALES = {
    "/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html",
    "/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",
    "/marmol-blanco-tampico": "marmol-blanco-tampico/index.html",
    "/piedra-bola-rio-tampico": "piedra-bola-rio-tampico/index.html",
}
PENDIENTES = frozenset({"/marmol-blanco-tampico", "/piedra-bola-rio-tampico"})
CAPTURA = json.loads(paridad_materiales.CAPTURA.read_text(encoding="utf-8"))
PERMITIDOS = {dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))
              if isinstance(n, int)}
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Presentaciones sin precio publicado (regla del dueño: "según cotización"). $250 sí está en datos.py (palmas y
# flamboyán), así que el mármol a $250 solo se detecta por cercanía, como las palmas sin precio de 2e.
SIN_PRECIO_RE = re.compile(r"(?:m[aá]rmol|\bsacos?\b|piedra bola|preparada|cami[oó]n(?:es)?)[^.$]{0,30}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b"),
    ("existencias o disponibilidad", r"InStock|\bdisponibilidad\b|\ben existencia\b|\bdisponibles? (?:hoy|ya)\b"
                                     r"|cantidad sin l[ií]mite|\bagotad"),
    ("plazo de entrega", r"entrega inmediata|entrega (?:el )?mismo d[ií]a|\ben 24 ?h|\bhoy mismo\b|entrega r[aá]pida"),
    ("más vendido o superlativo", r"m[aá]s vendid|\+\s?vendid|\bel mejor\b|\bimbatible\b|\bincomparable\b"
                                  r"|\binigualable\b|m[aá]s popular|calidad importada"),
    ("cifras sin respaldo", r"\+\s?500 jardines|\+\s?300 jardines|\+\s?18 años|\b\d{2}\s?% (?:m[aá]s r[aá]pido|de la maleza)"
                            r"|del 60\s?% al 95\s?%|hasta 8\s?°C|productor directo"),
    ("opiniones sin permiso", r"Ricardo O\.|Laura P\.|Patricia H\.|David M\."),
    ("En nuestro vivero", r"en nuestro vivero"),
)


def html_de(ruta):
    return (PUBLIC / MATERIALES[ruta]).read_text(encoding="utf-8")


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
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, texto, re.I)]
    if datos.ANTICIPO not in texto:
        salida.append("sin datos.ANTICIPO")
    if "window.open(" in html or medicion_js.medir_whatsapp_js(html)[1] != {"eventos": 0, "aperturas": 0, "omitidas": 0}:
        salida.append("abre WhatsApp con window.open (debe ser un enlace con data-cta)")
    nuevas = paridad_materiales.extraer(ruta)
    if [f["src"] for f in nuevas["fotos"]] != [f["src"] for f in CAPTURA[ruta]["fotos"]]:
        salida.append(f"fotos distintas a las de main o en otro orden: {[f['src'] for f in nuevas['fotos']]}")
    for vieja, nueva in zip(CAPTURA[ruta]["fotos"], nuevas["fotos"]):
        if vieja["srcset"] and nueva["srcset"] != vieja["srcset"]:
            salida.append(f"srcset distinto en {vieja['src']}")
    for img in re.findall(r"<img\b[^>]*>", paridad.principal(html)):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    esperado = dict(CAPTURA[ruta]["formulario"], _honey="")
    if nuevas["formulario"] != esperado:
        salida.append(f"formulario distinto al de main: {nuevas['formulario']}")
    if f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}"' not in html or 'id="solicitar-pedido"' not in html:
        salida.append("formulario sin la cuenta oficial o sin el ancla #solicitar-pedido")
    return salida


class MaterialesReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(MATERIALES) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_precios_de_tierra_negra_y_tezontle_de_datos(self):
        """Los únicos precios de materiales que dio el dueño (datos.PRECIOS), verificados el 2026-11-08."""
        p = datos.PRECIOS
        self.assertEqual((p["tierra_negra_costal"], p["tierra_negra_m3"], p["tezontle_costal"]), (90, 1500, 200))
        for clave in p:
            with self.subTest(clave=clave):
                self.assertFalse(re.search(r"marmol|piedra|camion", clave), "precio nuevo: confírmalo con el dueño")

    def test_las_reglas_detectan_lo_que_deben(self):
        for frase in ("Cotización gratis", "availability InStock", "Entrega inmediata", "el mejor", "+500 jardines",
                      "Ricardo O.", "En nuestro vivero", "Disponible en cantidad sin límite", "más vendido"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        for frase in ("Saco ≈ 20 kg a $250", "camión desde $5,000", "Tierra preparada $100"):
            with self.subTest(frase=frase):
                self.assertTrue(SIN_PRECIO_RE.search(frase))
        self.assertFalse(any(re.search(patron, "desde 2007 · 15 a 20 días de arraigo", re.I) for _r, patron in SIN_VERIFICAR))


if __name__ == "__main__":
    unittest.main()
