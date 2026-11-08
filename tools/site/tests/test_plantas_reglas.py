"""Reglas del dueño en las páginas de plantas (Etapa 2e): precios solo de datos.py, regla de palmas, flamboyán, garantía
con condiciones, sin afirmaciones sin verificar, fotos locales con pie y sin /api/img, y "En nuestro vivero" solo en las
fotos que el dueño confirmó (catalogo_datos.FOTOS_VIVERO_CONFIRMADAS).

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca las
suyas) y al cerrar la Etapa 2e queda vacía."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402
from test_b2b import PRECIOS_VIEJOS_PALMAS  # noqa: E402

PUBLIC = paginas.PUBLIC
PLANTAS = {
    "/plantas-palmas-arboles-tampico": "plantas-palmas-arboles-tampico/index.html",
    "/palmas-tropicales-tampico": "palmas-tropicales-tampico/index.html",
    "/plantas-para-jardin-tampico": "plantas-para-jardin-tampico/index.html",
    "/arboles-ornamentales-tampico": "arboles-ornamentales-tampico/index.html",
    "/arboles-para-banqueta-tampico": "arboles-para-banqueta-tampico/index.html",
    "/plantas-de-interior-tampico": "plantas-de-interior-tampico/index.html",
    "/catalogo": "catalogo.html",
}
PENDIENTES = frozenset()
PERMITIDOS = {dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))
              if isinstance(n, int)}
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Palmas sin precio publicado (decisión del dueño): ninguna lleva un monto cerca.
PALMAS_SIN_PRECIO_RE = re.compile(
    r"(?:washington\w*|viajer\w*|ravenala|bismar\w*|kerpis|cola de (?:zorr|pescado)\w*|triang\w*|cycas|cica\b|"
    r"palma bamb[uú]|licuala|mascare\w*|datiler\w*|rubelina|cocotera|palma estrella|cart[oó]n|madagascar)"
    r"[^.$]{0,60}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("productor directo", r"\bproductor(?:es)?\s+direct"),
    ("disponibilidad o existencias", r"disponibilidad real|\ben existencia\b|disponibles? hoy|\bagotad|últimas piezas"),
    ("cifras sin respaldo", r"\+\s?500\s+proyectos|proyectos entregados|\b3 estados\b|\b18 años\b|\+\s?200,000 m²"),
    ("insignia de más vendido sin dato", r"\+\s?vendid"),  # el título del blog "Las palmas más vendidas…" sí va
    ("opiniones sin permiso", r"Martha R\.|Constructora Arce"),
    ("calificaciones", r"★|\b\d(?:\.\d)?\s+estrellas\b"),
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b"),
    ("SENASICA", r"\bSENASICA\b"),
)
FIGURA_CATALOGO_RE = re.compile(r"<figure\b(?:(?!</figure>).)*?/img/catalogo/(?:(?!</figure>).)*?</figure>", re.S)
PIE_RE = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)
PIE_FORMATO_RE = re.compile(r"Fig\. \d{2,3} · (.+?)(?: · (En nuestro vivero))?")


def del_vivero_confirmadas():
    return {cd.especie(s)["name"] for s in cd.FOTOS_VIVERO_CONFIRMADAS}


def html_de(ruta):
    return (PUBLIC / PLANTAS[ruta]).read_text(encoding="utf-8")


def visible_y_ld(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    return paridad.texto(paridad.principal(html)) + " " + ld


def fallas(ruta):
    """Lista de reglas que rompe la página (vacía si cumple todas)."""
    html = html_de(ruta)
    texto = visible_y_ld(html)
    salida = []
    if "/api/img" in html:
        salida.append("usa /api/img")
    for p in sorted({m.group(0).replace(" ", "") for m in PRECIO_RE.finditer(texto)} - PERMITIDOS):
        salida.append(f"precio que no está en datos.py: {p}")
    # $1,500 también es el m³ de tierra negra (oficial): solo cuentan los precios viejos que no son de datos.py.
    salida += [f"precio viejo de palmas: {p}" for p in PRECIOS_VIEJOS_PALMAS if p in texto and p not in PERMITIDOS]
    salida += [f"palma con precio: …{m.group(0)}…" for m in PALMAS_SIN_PRECIO_RE.finditer(texto)]
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, texto, re.I)]
    if datos.GARANTIA_PLANTAS not in texto or "/politicas#garantia-plantas" not in html:
        salida.append("sin datos.GARANTIA_PLANTAS o sin enlace a /politicas#garantia-plantas")
    imagenes = html.count('src="/img/catalogo/')
    figuras = FIGURA_CATALOGO_RE.findall(html)
    if len(figuras) != imagenes:
        salida.append(f"{imagenes - len(figuras)} fotos del catálogo sin <figure>")
    confirmadas = del_vivero_confirmadas()
    for f in figuras:
        pie = paridad.texto(PIE_RE.search(f).group(1)) if PIE_RE.search(f) else ""
        m = PIE_FORMATO_RE.fullmatch(pie)
        if not m:
            salida.append(f"pie de foto fuera de formato: {pie!r}")
        elif m.group(2) and m.group(1) not in confirmadas:
            salida.append(f"«En nuestro vivero» sin foto confirmada por el dueño: {m.group(1)}")
        if "en el vivero" in f and (not m or m.group(1) not in confirmadas):
            salida.append(f"alt que dice «en el vivero» sin foto confirmada: {pie!r}")
    for img in re.findall(r"<img\b[^>]*>", paridad.principal(html)):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    return salida


class PlantasReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(PLANTAS) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_flamboyan_y_palmas_con_la_frase_del_dueno(self):
        flamboyan = f"Flamboyán desde {dinero(datos.PRECIOS['flamboyan'])}"
        for ruta, frases in (("/plantas-palmas-arboles-tampico", (flamboyan, datos.PALMAS_PRECIO)),
                             ("/arboles-ornamentales-tampico", (flamboyan,)),
                             ("/palmas-tropicales-tampico", (datos.PALMAS_PRECIO,))):
            if ruta in PENDIENTES:
                continue
            for frase in frases:
                with self.subTest(ruta=ruta, frase=frase):
                    self.assertIn(frase, visible_y_ld(html_de(ruta)))

    def test_ninguna_pagina_publica_usa_api_img(self):
        """Etapa 2e: el proxy /api/img ya no lo usa ninguna página (se borra en la Etapa 5)."""
        self.assertEqual([str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob("*.html")
                          if "/api/img" in p.read_text(encoding="utf-8")], [])

    def test_hub_explica_el_anticipo(self):
        if "/plantas-palmas-arboles-tampico" not in PENDIENTES:
            self.assertIn(datos.ANTICIPO, visible_y_ld(html_de("/plantas-palmas-arboles-tampico")))


def informe():
    for ruta in PLANTAS:
        print(f"== {ruta}")
        for f in fallas(ruta)[:12]:
            print(f"  - {f}")


if __name__ == "__main__":
    unittest.main()
