"""Renglones de la lista de precios (Etapa 2g): los usan /precios (contenido/precios.py) y la tabla de servicios de las 6
zonas (contenido/zona.py). Solo datos: la tabla la arma componentes_zonas.lista().

Todo precio sale de datos.PRECIOS (o de tools/pasto/data.py para el sintético por modelo), con las respuestas del dueño
del 2026-11-08 (tierra preparada, camiones de 5, 8 y 14 m³ y mármol con sus palabras); lo que no está ahí va
datos.SEGUN_COTIZACION (precio None): m³ y camión de tezontle, piedra bola (a granel, sin medidas) y árboles y plantas
que no son el flamboyán (regla del dueño, como en 2e y 2f: no se inventa). Sin pesos de costal.
"""
import componentes as c  # primero: agrega tools/pasto al sys.path (data)
import componentes_zonas as cz
import data
import datos
import mensajes_paginas
from contenido import materiales_comun as mc

dinero = c.dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
SINTETICO_MIN = min(m["rollo"] for m in data.MODELOS)
_F = datos.FRECUENCIAS_MANTENIMIENTO
FRECUENCIAS = ", ".join(_F[:-1]) + " o " + _F[-1]

PASTO = (
    {"nombre": "Pasto San Agustín, solo el pasto", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
     "precio": P["pasto_solo_m2"],
     "detalle": "Rollo fresco, cortado para tu pedido. Recoges en el vivero o te lo llevamos."},
    {"nombre": "Pasto San Agustín instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
     "precio": P["pasto_instalado_m2"], "desde": True,
     "detalle": f"Preparación básica del suelo, instalación y garantía de arraigo de {datos.ARRAIGO}."},
    {"nombre": "Mayoreo para constructoras y fraccionamientos", "href": "/mayoreo-pasto-tampico", "unidad": "m²",
     "precio": P["pasto_mayoreo_m2"], "desde": True,
     "detalle": (f"Pedidos de {P['pasto_mayoreo_minimo_m2']} m² o más, con entregas por etapas según el avance de la "
                 "obra y factura.")},
)
MANTENIMIENTO = {"nombre": "Mantenimiento de jardín", "href": "/mantenimiento-jardines-tampico", "unidad": "mes",
                 "precio": P["mantenimiento_mes"], "desde": True,
                 "detalle": ("Poda, fertilización y control de plagas. Frecuencia según tu plan y tu jardín: "
                            f"{FRECUENCIAS}.")}
RIEGO = {"nombre": "Sistema de riego automático", "href": "/sistema-riego-tampico", "unidad": "m²",
         "precio": P["riego_m2"],
         "detalle": "Aspersión o goteo con programador. Se cotiza después de medir y revisar la presión."}
# Poda de palmas y árboles (decisión del dueño, 2026-11-07): "desde $500, según cotización". Su página es de la Etapa 3,
# así que el renglón no enlaza.
def poda(mensaje, cta):
    """Renglón de la poda con el enlace "mándanos fotos": en cada zona lleva el mensaje de esa zona."""
    enlace = cz.enlace_wa("Mándanos fotos y ubicación por WhatsApp", mensaje, cta)
    return {"nombre": "Poda de palmas y árboles", "unidad": "árbol o palma", "precio": P["poda"], "desde": True,
            "cotiza": True,
            "detalle": f"El precio depende del tamaño del árbol o la palma y de los residuos que se generan. {enlace}."}


SERVICIOS = (
    MANTENIMIENTO,
    {"nombre": "Diseño de jardín, Plan Terra Esencial", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno"],
     "detalle": "Propuesta visual remota con tus fotos y lista de plantas. Entrega en 3 a 5 días hábiles."},
    {"nombre": "Diseño de jardín, Plan Terra Completo", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno_completo"],
     "detalle": "Diseño detallado, fichas de plantas, cuantificación de materiales y manual de cuidados."},
    {"nombre": "Diseño de jardín, Plan Terra Premium", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
     "precio": P["diseno_premium"], "desde": True,
     "detalle": ("Proyecto ejecutivo con seguimiento. Se descuenta en proyectos de más de "
                 f"{dinero(P['diseno_premium_descuento_desde'])}.")},
    RIEGO,
    poda(mensajes_paginas.PRECIOS_SECCIONES["poda"], "precios:poda"),
)
MATERIALES = (
    {"nombre": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico", "unidad": "costal",
     "precio": P["tierra_negra_costal"], "detalle": "Recoges en el vivero o te la llevamos."},
    {"nombre": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico", "unidad": "m³",
     "precio": P["tierra_negra_m3"], "detalle": "A granel."},
    *({"nombre": f"Tierra negra vegetal · camión de {m3} m³", "href": "/tierra-negra-vegetal-tampico",
       "unidad": "camión", "precio": precio, "detalle": "Camión volteo: descarga en tu domicilio u obra."}
      for m3, precio in datos.TIERRA_CAMIONES),
    {"nombre": "Tierra preparada", "href": "/tierra-negra-vegetal-tampico", "unidad": "costal",
     "precio": P["tierra_preparada_costal"], "detalle": "Con hojarasca y abono."},
    {"nombre": "Tezontle rojo", "href": "/tezontle-rojo-tampico", "unidad": "costal", "precio": P["tezontle_costal"],
     "desde": True, "detalle": f"Piedra volcánica de {mc.TEZONTLE_MEDIDA}; por m³ o en camión de 14 m³, {SEGUN}."},
    {"nombre": "Mármol blanco decorativo", "href": "/marmol-blanco-tampico", "unidad": "saco",
     "precio": P["marmol_saco"],
     "detalle": f"{datos.MARMOL_CONDICION}. 3 sacos cubren 1 m²."},
    {"nombre": "Piedra bola de río", "href": "/piedra-bola-rio-tampico", "unidad": datos.PIEDRA_BOLA_VENTA,
     "precio": None,
     "detalle": "Piedra de río natural para senderos, jardines secos y fuentes."},
)
PLANTAS = (
    {"nombre": "Palmas", "href": "/palmas-tropicales-tampico", "unidad": "pieza", "precio": P["palma_desde"],
     "desde": True, "detalle": f"{datos.PALMAS_PRECIO}."},
    {"nombre": "Árboles", "href": "/arboles-ornamentales-tampico", "unidad": "pieza", "precio": P["flamboyan"],
     "desde": True,
     "detalle": (f"Flamboyán desde {dinero(P['flamboyan'])}; jacaranda, olivo negro, crespón, guayacán y más, "
                 f"{SEGUN}: el precio depende del tamaño.")},
    {"nombre": "Plantas de jardín e interior", "href": "/plantas-para-jardin-tampico", "unidad": "pieza",
     "precio": None, "detalle": f"Más de {datos.VARIEDADES.lstrip('+')} variedades en el vivero."},
)
# Las 6 zonas: los servicios de jardín de main (tools/pasto/zonas.py) y la poda, con precios de datos.py. Cada zona publica
# 4 renglones en el orden de lo que pide (contenido/zona.py); la lista completa está en /precios.
FILAS_ZONA = {
    "pasto": {"nombre": "Pasto San Agustín instalado", "href": "/pasto-en-rollo-tampico", "unidad": "m²",
              "precio": P["pasto_instalado_m2"], "desde": True,
              "detalle": f"Preparación básica del suelo y garantía de arraigo de {datos.ARRAIGO}."},
    "mantenimiento": dict(MANTENIMIENTO, detalle="Poda, fertilización, control de plagas y revisión del riego."),
    "diseno": {"nombre": "Diseño de jardín", "href": "/diseno-jardines-tampico", "unidad": "proyecto",
               "precio": P["diseno"], "desde": True, "detalle": "Plan Esencial; se descuenta si contratas la obra."},
    "riego": dict(RIEGO, nombre="Riego automático", detalle="Aspersión o goteo con programador."),
    "palmas": {"nombre": "Palmas", "href": "/palmas-tropicales-tampico", "unidad": "pieza", "precio": P["palma_desde"],
               "desde": True, "detalle": "Areca y coco plumoso en tamaño chico; se cotizan por tamaño y volumen."},
}


def filas_zona(claves, ruta):
    """Los renglones de la zona, en su orden; la poda lleva el mensaje de esa zona."""
    filas = {**FILAS_ZONA, "poda": poda(mensajes_paginas.PODA_ZONAS[ruta], "zona:poda")}
    return tuple(filas[k] for k in claves)
