"""Respuestas directas de las páginas que venden (SEO fase 1, 2026-11-10): un párrafo de 40 a 60 palabras que contesta
la pregunta principal de la página con el dato en la misma frase (precio, unidad, zona y año), justo después de la
portada (componentes.respuesta) y marcado con data-vt-respuesta para el speakable del JSON-LD.

Todas las cifras salen de datos.py (y de tools/pasto/data.py en la tienda). Reglas del dueño: el pasto sin instalar no
lleva IVA; "con IVA" solo en lo instalado, el sintético y los servicios; la garantía del pasto, con condiciones; sin
plazos de entrega ni "gratis". La fecha visible ("Actualizado: noviembre de 2026")
es datos.PRECIOS_ACTUALIZADOS; /vivero-tampico no habla de precios y no la lleva.
"""
import sys
from pathlib import Path

import datos
from componentes import dinero, dinero_exacto

sys.path.insert(1, str(Path(__file__).resolve().parents[2] / "pasto"))
import data  # noqa: E402  (tools/pasto)

P = datos.PRECIOS
ZONA = "Tampico, Ciudad Madero y Altamira"
FECHA = datos.PRECIOS_ACTUALIZADOS
RIEGO_MIN, RIEGO_MAX = P["riego_m2"]
SINT_MIN, SINT_MAX = P["sintetico_instalado_m2"]
ROLLO_MIN = min(m["rollo"] for m in data.MODELOS)
ALTURAS = sorted(m["mm"] for m in data.MODELOS)
FRECUENCIAS = datos.FRECUENCIAS_MANTENIMIENTO
(_SEMANA, _ABRE, _CIERRA), (_SABADO, _ABRE_SAB, _CIERRA_SAB) = datos.HORARIO_LD
HORARIO = (f"de lunes a viernes de {int(_ABRE[:2])} a {int(_CIERRA[:2])} h y sábados de {int(_ABRE_SAB[:2])} a "
           f"{int(_CIERRA_SAB[:2])} h")

TEXTOS = {
    "/": (
        f"{datos.NOMBRE} es un vivero y empresa de jardinería en {datos.CIUDAD}, Tamaulipas, que atiende Tampico, Madero y "
        f"Altamira desde {datos.DESDE}. Vende pasto San Agustín en rollo a {dinero(P['pasto_solo_m2'])} por m² solo el "
        f"pasto (no lleva IVA) e instalado desde {dinero(P['pasto_instalado_m2'])} por m², con IVA; también diseña "
        f"jardines, da mantenimiento desde {dinero(P['mantenimiento_mes'])} al mes y vende plantas y pasto sintético."),
    "/pasto-en-rollo-tampico": (
        f"En {ZONA}, el pasto San Agustín en rollo cuesta {dinero(P['pasto_solo_m2'])} por m² solo el pasto (no lleva "
        f"IVA) y desde {dinero(P['pasto_instalado_m2'])} por m² instalado, con IVA (precios {datos.ANIO}): "
        f"incluye preparación básica del terreno, colocación y garantía de arraigo de {datos.ARRAIGO}, con "
        f"condiciones. Mayoreo, desde {P['pasto_mayoreo_minimo_m2']} m²: desde {dinero(P['pasto_mayoreo_m2'])} por m² "
        "(no lleva IVA)."),
    "/pasto-sintetico-tampico": (
        f"En {ZONA}, el pasto sintético instalado cuesta de {dinero_exacto(SINT_MIN)} a {dinero_exacto(SINT_MAX)} por "
        f"m², con material, colocación e IVA (precios {datos.ANIO}); la preparación del terreno se cotiza aparte. "
        f"{datos.NOMBRE} también vende solo el material, desde 2 m², en su showroom de {datos.CALLE_CORTA}, "
        f"{datos.CIUDAD}, desde {dinero(ROLLO_MIN)} por m²."),
    "/pasto-sintetico": (
        f"{datos.NOMBRE} envía pasto sintético a todo México desde {datos.CIUDAD}, Tamaulipas: {len(data.MODELOS)} "
        f"modelos de {ALTURAS[0]} a {ALTURAS[-1]} mm, desde {dinero(ROLLO_MIN)} por m² en rollo de {data.ROLLO_M2} m², "
        f"con IVA incluido (precios {datos.ANIO}). El envío cuesta de {dinero(min(data.ZONAS.values()))} a "
        f"{dinero(max(data.ZONAS.values()))} por rollo, según el estado, y el pedido mínimo es de "
        f"{data.MIN_NACIONAL_M2} m²."),
    "/sistema-riego-tampico": (
        f"Un sistema de riego automático instalado en Tampico, Ciudad Madero o Altamira cuesta de {dinero(RIEGO_MIN)} a "
        f"{dinero(RIEGO_MAX)} por m², con IVA (precios {datos.ANIO}), según el tipo de sistema: aspersión, goteo o "
        f"microaspersión. {datos.NOMBRE} lo diseña y lo instala con programador; frente al riego manual, ahorra "
        f"{datos.RIEGO_AHORRO} de agua."),
    "/mantenimiento-jardines-tampico": (
        f"El mantenimiento de jardines en {ZONA} cuesta desde {dinero(P['mantenimiento_mes'])} al mes, con IVA, en el "
        f"plan residencial de {datos.NOMBRE} (precios {datos.ANIO}). Incluye poda, fertilización y control de plagas, con "
        f"servicio {FRECUENCIAS[0]}, {FRECUENCIAS[1]}, {FRECUENCIAS[2]} o {FRECUENCIAS[3]}. Los planes premium y para "
        f"empresas van {datos.SEGUN_COTIZACION.lower()}."),
    "/diseno-jardines-tampico": (
        f"El diseño de jardines en Tampico con {datos.NOMBRE} (Plan Terra) cuesta {dinero(P['diseno'])} en el plan "
        f"Esencial, {dinero(P['diseno_completo'])} en el Completo y desde {dinero(P['diseno_premium'])} en el Premium, "
        f"con IVA (precios {datos.ANIO}). En Esencial y Completo, el costo del diseño se descuenta al contratar la obra; "
        f"en Premium, en proyectos de más de {dinero(P['diseno_premium_descuento_desde'])}."),
    "/vivero-tampico": (
        f"{datos.NOMBRE} es un vivero en {datos.CALLE}, {datos.COLONIA}, {datos.CP} {datos.CIUDAD}, Tamaulipas "
        f"({datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}), que atiende Tampico, Madero y Altamira desde "
        f"{datos.DESDE}. Abre {HORARIO}, con más de 200 variedades de plantas, palmas y árboles."),
    # Entrega A de experiencia (2026-11-10): estas dos respuestas eran la entrada de la portada; con el hero de marca
    # la entrada se acorta (2 a 3 renglones en celular) y el mismo texto, sin tocar, pasa al bloque "En corto".
    "/precios": (
        f"En Tampico, Madero y Altamira, el pasto San Agustín cuesta {dinero(P['pasto_solo_m2'])}/m² solo el pasto y desde "
        f"{dinero(P['pasto_instalado_m2'])}/m² instalado. El mantenimiento de jardín cuesta desde "
        f"{dinero(P['mantenimiento_mes'])}/mes, el diseño desde {dinero(P['diseno'])} y el pasto sintético desde "
        f"{dinero(ROLLO_MIN)}/m²."),
    "/mayoreo-pasto-tampico": (
        f"En Viveros Terra el pasto San Agustín al mayoreo cuesta desde {dinero(P['pasto_mayoreo_m2'])}/m² (solo pasto) en "
        f"pedidos de {P['pasto_mayoreo_minimo_m2']} m² o más, con factura {datos.FACTURA}; el pasto sin instalar no lleva "
        "IVA. Entregamos por etapas según el avance de tu obra en Tampico, Madero y Altamira; fuera de la zona, por "
        "proyecto."),
}
SIN_FECHA = ("/vivero-tampico",)
RUTAS = tuple(TEXTOS)


def de(ruta):
    """{"texto": …, "fecha": …} de la página para componentes.respuesta."""
    return {"texto": TEXTOS[ruta], **({} if ruta in SIN_FECHA else {"fecha": FECHA})}
