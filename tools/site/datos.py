"""Fuente única de datos del sitio de Viveros Terra.

Todo dato que se repite en más de una página sale de aquí: contacto, domicilio, horario, promesa de respuesta,
cifras de la empresa, precios oficiales, garantías, decisiones del dueño, perfiles oficiales y mensajes de WhatsApp.
Lo consumen los parciales del shell (tools/site/partials.py) y las pruebas; desde la Etapa 4, también el JSON-LD y
llms.txt. Decisiones del dueño: docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md.
"""
from urllib.parse import quote

SITIO = "https://www.viverosterra.com"
NOMBRE = "Viveros Terra"
GA4_ID = "G-RMZCVJ734M"
ANIO = 2026

TELEFONO_WA = "528333268008"
TELEFONO_TEL = "+528333268008"
TELEFONO_VISIBLE = "833 326 8008"
CORREO_FORMULARIOS = "viverosterra@hotmail.com"

CALLE = "Av. Álvaro Obregón 209 Sur"
COLONIA = "Col. Ampliación Unidad Nacional"
CP = "89510"
CIUDAD = "Ciudad Madero"
ESTADO = "Tamps."
REFERENCIA = "Frente a Walmart, entrando por Banamex"
DOMICILIO_COMPLETO = f"{CALLE}, {COLONIA}, {CP} {CIUDAD}, {ESTADO}"
DOMICILIO_CORTO = "Obregón 209 Sur, Cd. Madero"
GEO = (22.2777575, -97.8433341)
MAPS_URL = "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"

HORARIO = "Lun a vie 9 a 18 h, sáb 9 a 14 h"
PROMESA = "Respondemos en menos de 1 hora en horario"
PROMESA_COMPLETA = f"{PROMESA} · {HORARIO}"

DESDE = 2007
FUNDACION = "2007-12-12"
SINTETICO_NACIONAL_DESDE = 2012
VARIEDADES = "+200"
CLIENTES = "+900"
INSTALACIONES = "+1,500"
M2_INSTALADOS = "+500,000 m²"
REPSE = "773725"
FACTURA = "CFDI 4.0"
GOOGLE = "4.6 en Google (24 reseñas)"

PRECIOS = {
    "pasto_solo_m2": 85,
    "pasto_instalado_m2": 120,
    "pasto_mayoreo_m2": 60,
    "pasto_mayoreo_minimo_m2": 500,
    "mantenimiento_mes": 750,
    "diseno": 3000,
    "riego_m2": (180, 320),
    "sintetico_instalado_m2": (385, 650),
    "sintetico_tienda_m2": 139,
    "poda": 500,
    "framboyan": 250,
}
PODA = ("Desde $500, según cotización: el precio depende del tamaño del árbol o la palma y de los residuos que se "
        "generan. Mándanos fotos y ubicación por WhatsApp.")
GARANTIA_PASTO = ("Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego "
                  "(ver condiciones).")
GARANTIA_PLANTAS = "30 días en las plantas que sembramos nosotros, con el riego indicado (ver condiciones)."
PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."

# Permiso del dueño (2026-11-07) para mostrarlos con nombre y logo.
CLIENTES_B2B = ("BMW", "Taghleef Industries", "Gobierno de Tampico", "Grupo Velas", "Velamar", "Flex")
# Autor del blog: la organización (Organization ligada a #negocio). Nunca una persona inventada.
AUTOR_BLOG = "Equipo técnico de Viveros Terra"
# Decisión del dueño (2026-11-07): nunca se muestra fecha de corte ni disponibilidad semanal.
PROXIMO_CORTE = None

REDES = (
    ("Facebook", "https://www.facebook.com/viverosterra/"),
    ("Instagram", "https://www.instagram.com/viverosterramx"),
    ("TikTok", "https://www.tiktok.com/@viverosterra"),
    ("YouTube", "https://www.youtube.com/@viverosterramx"),
    ("LinkedIn", "https://www.linkedin.com/company/viveros-terra-tampico"),
)

FIRMA = "Vengo de viverosterra.com"
MENSAJES = {
    "general": "Hola, quiero cotizar: ___\nColonia: ___\nMetros aprox.: ___",
    "pasto-natural": "Hola, quiero cotizar pasto San Agustín en rollo.\nColonia: ___\nMetros aprox.: ___\nSolo el pasto o instalado: ___",
    "pasto-sintetico": "Hola, quiero cotizar pasto sintético.\nCiudad o colonia: ___\nMetros aprox.: ___",
    "jardin": "Hola, quiero cotizar diseño, mantenimiento o riego.\nColonia: ___\nMetros aprox. del jardín: ___",
    "plantas": "Hola, quiero cotizar plantas o palmas.\nLo que busco: ___\nColonia de entrega: ___",
    "materiales": "Hola, quiero cotizar material para jardín.\nMaterial y cantidad: ___\nColonia de entrega: ___",
    "empresas": "Hola, quiero cotizar un proyecto.\nEmpresa: ___\nObra y ubicación: ___\nm² o especies: ___\nFecha: ___",
}


def con_firma(texto):
    """Texto de WhatsApp con la firma al final para atribuir el chat."""
    return f"{texto}\n\n{FIRMA}"


def mensaje(servicio):
    """Texto de WhatsApp del servicio, siempre con la firma al final."""
    return con_firma(MENSAJES[servicio])


def wa_url(texto):
    """Enlace wa.me con el texto codificado por completo (espacios como %20, saltos como %0A)."""
    return f"https://wa.me/{TELEFONO_WA}?text={quote(texto, safe='')}"
