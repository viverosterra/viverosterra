"""Precio en mensualidades con tarjeta de crédito (Clip).

Misma fórmula que la calculadora de Clip: la comisión del plazo se suma a la estándar
y el IVA se aplica sobre ambas. Viveros Terra recibe el contado íntegro.
Mantener igual a public/js/vt-mensualidades.js (paridad en test_mensualidades.py y vt-mensualidades.test.js, con los
casos de public/js/tests/casos-mensualidades.json).
"""
import math

TASA_BASE = 0.036
IVA = 0.16
TASAS = {3: 0.0457, 6: 0.0757, 9: 0.1107, 12: 0.1277}
PLAZOS = (3, 6, 9, 12)
# (monto mínimo de contado, plazos que aplican desde ese monto), de mayor a menor
UMBRALES = ((15000, (3, 6, 9, 12)), (5000, (3, 6)), (2000, (3,)))


def redondear(x):
    """Igual que Math.round de JavaScript para valores positivos: los .5 suben (round() de Python los lleva al par y
    daba $1 menos que vt-mensualidades.js en mensualidades como 1,666.5)."""
    piso = math.floor(x)
    return int(piso + 1 if x - piso >= 0.5 else piso)  # x - piso es exacto; floor(x + 0.5) falla con 0.49999999999999994


def plazos_disponibles(contado):
    for minimo, plazos in UMBRALES:
        if contado >= minimo:
            return list(plazos)
    return []


def total_a_plazos(contado, plazo):
    return math.ceil(contado / (1 - (TASA_BASE + TASAS[plazo]) * (1 + IVA)))


def planes(contado):
    disponibles = plazos_disponibles(contado)
    out = []
    for plazo in PLAZOS:
        total = total_a_plazos(contado, plazo)
        out.append({"plazo": plazo, "total": total, "mensualidad": redondear(total / plazo),
                    "diferencia": total - math.ceil(contado), "disponible": plazo in disponibles})
    return out


def minimo_de(plazo):
    return min(minimo for minimo, plazos in UMBRALES if plazo in plazos)
