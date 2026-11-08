"""Componentes de las páginas de materiales (Etapa 2f): calculadora de cantidad, tabla de presentaciones con precio o
"según cotización", otros materiales, portada sin foto o con foto apaisada, cierre con la foto de fondo de main y el
formulario de pedido por correo. Funciones puras, como componentes.py (que ya pasa de 800 renglones).

La calculadora es la de main línea por línea (calcularTierra, calcularTezontle y calcularMarmol, incluidos sus
redondeos): calculo() y textos() dan lo mismo que public/js/vt-materiales.js en los casos congelados de main
(public/js/tests/casos-materiales.json; tests/test_materiales_paridad.py y vt-materiales.test.js). Piedra bola no tenía
calculadora: la suya multiplica el área por los kg por m² que publicaba su propia pregunta frecuente (120 a 150 kg por m²
con piedra mediana y capa de 8 a 10 cm). Los precios salen de datos.PRECIOS; lo que no está ahí va "según cotización".
"""
import json
import math

import componentes as c
import datos
from partials import WA_GLIFO, esc

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
AREA_MAXIMA = 100_000  # m²; más que esto no es un jardín: la calculadora vuelve al mensaje de la página
CIERRE_MENSAJE = "¿Me pueden dar precio de entrega a domicilio en Tampico?"
CAMION_TIERRA = f"Camión volteo de 8 m³ o más ({SEGUN})"

# clave → factores de main, precios de datos.py, texto del mensaje, capas (valor, texto) y la capa elegida al cargar.
# Los textos de las capas de tezontle son los de main tal cual: van en el mensaje ("Uso: …").
CALCULADORAS = {
    "tierra-negra": {
        "texto": "tierra negra vegetal", "costal_m3": 0.035,
        "precio_costal": P["tierra_negra_costal"], "precio_m3": P["tierra_negra_m3"],
        "etiqueta_capa": "Grosor de la capa", "elegida": "0.08",
        "capas": (("0.05", "5 cm · mejora superficial"), ("0.08", "8 cm · preparación para pasto (recomendado)"),
                  ("0.10", "10 cm · preparación profunda"), ("0.15", "15 cm · terreno muy pobre")),
        "cta": "cotizarCalculado",
    },
    "tezontle": {
        "texto": "tezontle rojo", "costal_m3": 0.027, "camion_m3": 14,
        "etiqueta_capa": "¿Para qué lo usas?", "elegida": "0.10",
        "capas": (("0.06", "Control de maleza (6 cm)"), ("0.08", "Control de maleza intenso (8 cm)"),
                  ("0.10", "Senderos transitables (10 cm)"), ("0.05", "Decorativo/arriates (5 cm)"),
                  ("0.04", "Capa en macetas (4 cm)")),
        "cta": "cotizarTezontle",
    },
    "marmol": {
        "texto": "mármol blanco decorativo", "kg_saco": 20,
        "etiqueta_capa": "Grosor de la capa", "elegida": "4",
        "capas": (("3", "3 cm · decorativo o macetas"), ("4", "4 cm · arriates (recomendado)"),
                  ("5", "5 cm · senderos o alberca"), ("6", "6 cm · alta densidad o tráfico")),
        "cta": "cotizarMarmol",
    },
    "piedra-bola": {
        "texto": "piedra bola de río", "kg_m2": (120, 150), "medida": "mediana (capa de 8 a 10 cm)",
        "cta": "cotizarPiedra",
    },
}
# Lo que lee vt-materiales.js en data-material: sin textos de la página ni capas (esas van en el <select>).
PARA_JS = ("costal_m3", "camion_m3", "precio_costal", "precio_m3", "kg_saco", "kg_m2", "medida", "texto")


def numero_js(x):
    """Como String(x) de JavaScript para los números de estas calculadoras: 8.0 → "8", 0.1 → "0.1"."""
    x = float(x)
    return str(int(x)) if x.is_integer() else repr(x)


def leer_area(texto):
    """m² escritos por el visitante (como leerArea de vt-materiales.js y leer_m2 de las empresas): "1,200" y "1200" son
    1200, "12,5" es 12.5 y "80 m²" es 80. Devuelve 0 si no es un número mayor que 0 y hasta AREA_MAXIMA."""
    n = c.leer_m2(texto)
    return n if n <= AREA_MAXIMA else 0


def _m3(area, capa):
    return math.ceil(area * capa * 10) / 10


def calculo(clave, area, capa=0):
    """Resultado de la calculadora de main para `area` m² con la capa `capa` (m en tierra y tezontle, cm en mármol)."""
    cfg = CALCULADORAS[clave]
    if clave == "tierra-negra":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1.5 else "m3" if m3 <= 7 else "camion"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo}
    if clave == "tezontle":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1 else "m3" if m3 <= 5 else "camion" if m3 <= cfg["camion_m3"] else "camiones"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo,
                "camiones": math.ceil(m3 / cfg["camion_m3"])}
    if clave == "marmol":
        por_m2 = 3 if capa <= 4 else 4 if capa <= 5 else 5
        sacos = math.ceil(area * por_m2)
        return {"sacos": sacos, "kg": sacos * cfg["kg_saco"], "por_m2": por_m2}
    minimo, maximo = cfg["kg_m2"]
    return {"kg": (c.redondear(area * minimo), c.redondear(area * maximo))}


def _mensaje(cfg, titulo, lineas):
    return "\n".join((f"Hola, quiero cotizar {cfg['texto']}.", "", titulo, *lineas, "", CIERRE_MENSAJE))


def textos(clave, area, capa, r, uso=""):
    """Lo que muestra la etiqueta y el mensaje de WhatsApp. Iguales a los de main salvo lo que pide el dueño: el camión de
    tierra negra sin el "desde $5,000" que no está en datos.py, el mármol sin el precio de $250 por saco y los tres con
    la misma pregunta de cierre (sin "confirmar disponibilidad")."""
    cfg = CALCULADORAS[clave]
    a = numero_js(area)
    if clave in ("tierra-negra", "tezontle"):
        m3, costales = numero_js(r["m3"]), r["costales"]
        if clave == "tierra-negra":
            presentacion = {"costales": f"{costales} costales ({c.dinero(costales * cfg['precio_costal'])})",
                            "m3": f"{m3} m³ suelto (~{c.dinero(r['m3'] * cfg['precio_m3'])})",
                            "camion": CAMION_TIERRA}[r["tramo"]]
            equivalente = f"{costales} costales" if r["tramo"] == "costales" else f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Cantidad: {m3} m³")
        else:
            presentacion = {"costales": f"{costales} costales", "m3": f"{m3} m³ suelto", "camion": "Camión 14 m³",
                            "camiones": f"{r['camiones']} camiones 14 m³"}[r["tramo"]]
            equivalente = f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Uso: {uso}", f"Cantidad: {m3} m³")
        return {"cantidad": f"{m3} m³", "presentacion": presentacion, "equivalente": equivalente,
                "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}
    if clave == "marmol":
        sacos, g = r["sacos"], numero_js(capa)
        nota = (f"{sacos} sacos cubren {a} m² con capa de {g} cm." if capa <= 4
                else f"{sacos} sacos para {a} m² con capa de {g} cm (alta densidad).")
        lineas = (f"Área: {a} m²", f"Capa: {g} cm", f"Cantidad: {sacos} sacos")
        return {"cantidad": f"{sacos} sacos", "peso": f"{r['kg']} kg", "nota": nota,
                "mensaje": _mensaje(cfg, "Datos de mi proyecto:", lineas)}
    minimo, maximo = r["kg"]
    cantidad = f"{minimo:,} a {maximo:,} kg"
    lineas = (f"Área: {a} m²", f"Medida: {cfg['medida']}", f"Cantidad aprox.: {cantidad}")
    return {"cantidad": cantidad, "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}


def ejemplo(clave, area, capa=0):
    """Cantidad para el texto de una pregunta frecuente ("8 m³", "150 sacos"): sale de la misma calculadora."""
    capa = float(capa)
    return textos(clave, area, capa, calculo(clave, area, capa))["cantidad"]


def datos_js(clave):
    cfg = CALCULADORAS[clave]
    return {"clave": clave, **{k: cfg[k] for k in PARA_JS if k in cfg}}


