"""Reglas del dueño en el blog (Etapa 2h): precios solo de datos.py o calculados con ellos, especies sin precio confirmado
"según cotización", sin "más vendido", sin "gratis" ni "sin costo" (salvo la garantía de pasto aprobada), sin estadísticas sin
fuente, sin SENASICA, "Oasis" ni proveedor de la terminal, autor editorial, mismo autor visible y la visita siempre con su costo."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paridad  # noqa: E402
from componentes import dinero  # noqa: E402
from contenido import articulo  # noqa: E402

PERMITIDOS = ({f"${int(n):,}" for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))}  # parte entera: "$446" de "$446.60"
              | {dinero(m[k]) for m in data.MODELOS for k in ("t1", "t2", "rollo")})
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
_RIEGO = {dinero(a * m2) for a in datos.PRECIOS["riego_m2"] for m2 in (30, 50, 60, 80, 100, 120, 150, 200, 250, 500)}
_PRESUPUESTO = {"$5", "$15", "$20", "$50", "$120", "$200"}  # "$5K, $20K, $50K": el presupuesto del lector, no un precio
# Lo que no es un precio de Viveros Terra (presupuesto del lector, cuenta del ejemplo, tarifa de agua, artículo de ferretería)
# o es una multiplicación de un precio oficial. Cada entrada se revisó a mano; la lista solo puede encoger.
CALCULADOS = {
    "": _PRESUPUESTO,  # el índice: "$5K, $20K o $50K"
    "cesped-amarillo-tampico-causas-soluciones": {"$50", "$150"},
    "cuanto-cuesta-jardin-tampico-precios": {"$2,550", "$4,250", "$6,000", "$10,200", "$21,250", "$45,000",
                                             "$50,000", "$80,000", "$3"} | _RIEGO,
    "cuanto-cuesta-pasto-sintetico-mexico": {"$157", "$162", "$167", "$900", "$1,150", "$1,400", "$2,800", "$4,225", "$5,125",
                                             "$9,950", "$11,100", "$29,900", "$32,700"},
    "framboyan-delonix-regia-tampico": _PRESUPUESTO,
    "jardin-bajo-presupuesto-tampico": _PRESUPUESTO | {"$10,800", "$18,300", "$19,200", "$30,900", "$4,500", "$5,000",
                                                        "$15,000", "$20,000", "$50,000"},
    "jardin-vertical-tampico-guia": _PRESUPUESTO,
    "pasto-sintetico-vs-natural-tampico": {"$0", "$1,200", "$2,400", "$4,000", "$4,800", "$6,000", "$9,600", "$22,330", "$37,700",
                                           "$94,000", "$182,000"},
    "riego-automatico-tampico-roi": _RIEGO | {"$0", "$50", "$600", "$900", "$1,100", "$2,000", "$4,500", "$7,200",
                                              "$10,800", "$14,400", "$19,200", "$21,600", "$25,600", "$36,000", "$38,400", "$64,000",
                                              "$160,000"},
    "sistema-riego-automatico-conviene-tampico": _RIEGO | {"$27,000", "$32,000",
                                                           "$36,000", "$48,000", "$64,000"},
    "sistema-riego-automatizado-tampico": _RIEGO | {"$9,000", "$16,000", "$25,600", "$48,000"},
    "tierra-negra-costal-camion-tampico": {"$450", "$900", "$1,350", "$1,800", "$2,160", "$2,250", "$3,330", "$4,500", "$6,660",
                                           "$13,500"},
}
ESPECIE_SIN_PRECIO_RE = re.compile(
    r"(?:washington|kerpis|viajero|cycas|bamb[uú]|bismarckia|cola de zorro|triangular|ficus|trueno|neem|tabach[ií]n|laurel|tulip[aá]n)"
    r"(?:(?!seg[uú]n cotizaci[oó]n)[^.<]){0,50}\$\s?\d", re.I)
SIN_VERIFICAR = (
    ("más vendido", r"m[aá]s vendid[ao]s?"),
    ("gratis", r"\bgratis\b|\bgratuit\w*"),
    ("sin costo", r"\bsin costo\b(?! ?, siguiendo)|\bsin cargo\b"),
    ("certificación", r"\bSENASICA\b"),
    ("marca", r"\bOasis\b"),
    ("terminal", r"\bClip\b"),
    ("porcentaje sin fuente", r"el \d{2}% de (?:los|las) (?:problemas|plantas|casos|jardines)|arraiga el \d{2}%"),
    ("cifra de ahorro", r"(?:hasta|entre)[^.]{0,20}(?:50|60)\s?%[^.]{0,40}agua"),
    ("caso sin verificar", r"Ejemplo real|ejemplos? reales|casos? reales|Cliente típico|[Cc]lientes de Viveros Terra"),
    ("en nuestro vivero", r"en nuestro vivero"),
    ("pago en parcialidades", r"parcialidades"),
)
_SIN = r"(?:(?!seg[uú]n cotizaci[oó]n)[^.<=]){0,50}\$\s?\d"
# PERMITIDOS compara valores en todo el sitio: "$1,500" pasa como m³ de tierra aunque esté pegado a un sensor. Estas parejas de
# producto y precio se revisan con su contexto (extras de riego, camiones, garantía, ahorro).
PAREJAS_PROHIBIDAS = (
    ("sensor con precio", r"\bsensor(?:es)?\b" + _SIN),
    ("bomba con precio", r"\bbomba\b" + _SIN),
    ("controlador o WiFi con precio", r"(?:\bcontrolador(?:es)?\b|\bWiFi\b)" + _SIN),
    ("programador o timer con precio", r"(?:programador de manguera|programador básico|\btimer\b|cinta perforada)" + _SIN),
    ("camión de tierra al precio del m³ suelto", r"cami[oó]n[^.<]{0,40}\$1,500\b"),
    ("pasto instalado al precio de solo pasto", r"[Pp]asto instalado[^.<]{0,30}\$85\b"),
    ("camión de tezontle con medida", r"[Cc]ami[oó]n volteo (?:de )?(?:5|8|14) m³(?! en \$)"),
    ("garantía del sintético de 5 a 8 años sin modelo", r"garant[ií]a de 5-8"),
    ("ahorro de agua mayor a 40%", r"12[-–]18 m³|30[-–]40\s?% adicional"),
)
CON_VISITA = ("cesped-amarillo-tampico-causas-soluciones", "cuanto-cuesta-jardin-tampico-precios",
              "sistema-riego-automatizado-tampico")


def publico(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+|twitter:[a-z:]+)" content="([^"]*)"', html))
    titulo = " ".join(re.findall(r"<title>(.*?)</title>", html))
    return " ".join((paridad.texto(paridad.principal(html)), ld, metas, titulo))


class BlogReglasTest(unittest.TestCase):
    def rutas(self):
        return [ruta for ruta, _a, _p, _c in generar.PAGINAS if ruta.startswith("/blog")]

    def test_precios_oficiales_o_calculados(self):
        for ruta in self.rutas():
            slug = ruta.removeprefix("/blog").strip("/")
            texto = publico(paridad.archivo(ruta).read_text(encoding="utf-8"))
            sobra = {p.replace(" ", "") for p in PRECIO_RE.findall(texto)} - PERMITIDOS - CALCULADOS.get(slug, set())
            with self.subTest(ruta=ruta):
                self.assertEqual(sorted(sobra), [])

    def test_especies_sin_precio_confirmado(self):
        for ruta in self.rutas():
            with self.subTest(ruta=ruta):
                texto = paridad.texto(paridad.principal(paridad.archivo(ruta).read_text(encoding="utf-8")))
                self.assertIsNone(ESPECIE_SIN_PRECIO_RE.search(texto))

    def test_sin_afirmaciones_prohibidas(self):
        for ruta in self.rutas():
            texto = publico(paridad.archivo(ruta).read_text(encoding="utf-8"))
            for nombre, patron in SIN_VERIFICAR:
                with self.subTest(ruta=ruta, regla=nombre):
                    self.assertIsNone(re.search(patron, texto, re.I), nombre)

    def test_parejas_de_producto_y_precio(self):
        for ruta in self.rutas():
            texto = publico(paridad.archivo(ruta).read_text(encoding="utf-8"))
            for nombre, patron in PAREJAS_PROHIBIDAS:
                with self.subTest(ruta=ruta, regla=nombre):
                    m = re.search(patron, texto)
                    self.assertIsNone(m, m.group(0) if m else "")

    def test_autor_editorial_en_cada_articulo(self):
        for slug in articulo.CLAVES:
            with self.subTest(slug=slug):
                self.assertIn(f"<b>Por</b> {datos.AUTOR_BLOG}", paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8"))

    def test_la_visita_lleva_su_costo(self):
        for slug in CON_VISITA:
            with self.subTest(slug=slug):
                self.assertIn(datos.VISITA_COSTO, paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
