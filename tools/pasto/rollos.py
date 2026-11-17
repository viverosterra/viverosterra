"""¿Cuántos rollos de pasto sintético necesito? (Entrega B del SEO nacional, 2026-11-16.)

El rollo mide 2 × 25 m (ROLLO_M2 = 50 m²) y se vende por m². El espacio se cubre con tiras de 2 m de ancho, todas en
el mismo sentido de la fibra (guía de instalación), del largo completo de un lado: se elige el sentido que gasta menos
material (en empate, el de menos tiras). Se pide lo mayor entre las tiras y el área + 10% para cortes y ajustes (la
misma guía: «súmale un 5-10%», ejemplo 5 × 4 m → 22 m²). El envío se cobra por rollo: ceil(m² / 50), como el
cotizador de public/js/tienda-pasto.js.

Mismo cálculo que public/js/vt-rollos.js; los casos compartidos están en public/js/tests/casos-rollos.json.
"""
import math

from data import ROLLO_M2

ROLLO_ANCHO_M = 2
ROLLO_LARGO_M = ROLLO_M2 // ROLLO_ANCHO_M
MARGEN = 0.10
MAX_M2 = 5000  # el mismo tope del cotizador (input #m2 max="5000")
EPS = 1e-9
MEDIDAS_COMUNES = ((3, 3), (5, 4), (7, 5), (8, 6), (10, 5), (10, 10), (15, 10))


def _numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _limpio(v):
    """Número con 2 decimales y sin el .0 de los enteros (20.0 → 20), igual que JSON en el navegador."""
    v = round(v + 0.0, 2)
    return int(v) if v == int(v) else v


def _tiras(a_lo_largo_de, cruzado):
    tiras = math.ceil(cruzado / ROLLO_ANCHO_M - EPS)
    return tiras, round(tiras * ROLLO_ANCHO_M * a_lo_largo_de, 2)


def corte(largo, ancho):
    """Tiras, m² a pedir y rollos de envío de un espacio rectangular de largo × ancho metros, o None si las medidas
    no son números positivos o el área pasa de MAX_M2."""
    if not (_numero(largo) and _numero(ancho)) or largo <= 0 or ancho <= 0 or largo * ancho > MAX_M2:
        return None
    opciones = [(*_tiras(largo, ancho), largo, ancho), (*_tiras(ancho, largo), ancho, largo)]
    tiras, m2_tiras, largo_tira, cruzado = min(opciones, key=lambda o: (o[1], o[0]))
    area = round(largo * ancho, 2)
    m2_sin_margen = math.ceil(m2_tiras - EPS)
    m2 = math.ceil(max(m2_tiras, area * (1 + MARGEN)) - EPS)
    return {
        "area": _limpio(area), "tiras": tiras, "largo_tira": _limpio(largo_tira), "cruzado": _limpio(cruzado),
        "m2_tiras": _limpio(m2_tiras), "m2": m2, "rollos": math.ceil(m2 / ROLLO_M2),
        "m2_sin_margen": m2_sin_margen, "rollos_sin_margen": math.ceil(m2_sin_margen / ROLLO_M2),
        "sobrante": _limpio(m2 - area), "uniones": tiras - 1, "tira_con_union": largo_tira > ROLLO_LARGO_M,
    }


def tabla_medidas(medidas=MEDIDAS_COMUNES):
    """Renglones de la tabla de medidas comunes (HTML estático: se lee sin JavaScript y lo citan los buscadores)."""
    return [dict(corte(l, a), largo=l, ancho=a) for l, a in medidas]
