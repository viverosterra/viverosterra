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

CALLE_CORTA = "Obregón 209 Sur"
CALLE = f"Av. Álvaro {CALLE_CORTA}"
COLONIA = "Col. Ampliación Unidad Nacional"
CP = "89510"
CIUDAD = "Ciudad Madero"
ESTADO = "Tamps."
REFERENCIA = "Frente a Walmart, entrando por Banamex"
DOMICILIO_COMPLETO = f"{CALLE}, {COLONIA}, {CP} {CIUDAD}, {ESTADO}"
DOMICILIO_CORTO = f"{CALLE_CORTA}, Cd. Madero"
GEO = (22.2777575, -97.8433341)
MAPS_URL = "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"

HORARIO = "Lun a vie 9 a 18 h, sáb 9 a 14 h"
# El mismo horario para el JSON-LD (openingHoursSpecification): días en inglés de schema.org, horas de 24 h.
HORARIO_LD = (
    (("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"), "09:00", "18:00"),
    (("Saturday",), "09:00", "14:00"),
)
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
    "flamboyan": 250,
    "palma_desde": 250,
    "tierra_negra_costal": 90,
    "tierra_negra_m3": 1500,
    "tezontle_costal": 200,
}
PODA = ("Desde $500, según cotización: el precio depende del tamaño del árbol o la palma y de los residuos que se "
        "generan. Mándanos fotos y ubicación por WhatsApp.")
GARANTIA_PASTO = ("Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego "
                  "(ver condiciones).")
GARANTIA_PLANTAS = "30 días en las plantas que sembramos nosotros, con el riego indicado (ver condiciones)."
PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."
ARRAIGO = "15 a 20 días"
LLEGADA_PASTO = "una vez por semana, generalmente los viernes"
ANTICIPO = ("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
            "un anticipo.")
# Una sola respuesta a "¿cuánto cuesta el pasto en rollo en Tampico?" en home, servicio y precios (spec §7.3).
RESPUESTA_PRECIO_PASTO = (
    f"En Viveros Terra el pasto San Agustín en rollo cuesta ${PRECIOS['pasto_solo_m2']} por m² solo el pasto y desde "
    f"${PRECIOS['pasto_instalado_m2']} por m² instalado, con IVA incluido. El instalado incluye la preparación básica "
    f"del terreno, la colocación y una garantía de arraigo de {ARRAIGO}. En pedidos de "
    f"{PRECIOS['pasto_mayoreo_minimo_m2']} m² o más, el mayoreo cuesta desde ${PRECIOS['pasto_mayoreo_m2']}/m². "
    f"Precios {ANIO}, con IVA, para Tampico, Ciudad Madero y Altamira."
)

# Permiso del dueño (2026-11-07) para mostrarlos con nombre y logo. Renault (cliente real, permiso del dueño) va con su
# nombre en texto: no hay logo en public/img/clientes y no se inventa uno.
CLIENTES_B2B = ("BMW", "Taghleef Industries", "Gobierno de Tampico", "Grupo Velas", "Velamar", "Flex", "Renault")
# Opiniones reales con nombre, publicadas con permiso del dueño (2026-11-07): las cuatro de la home anterior, textuales.
# (cita, nombre, servicio · lugar). Nunca se agrega ni se edita una opinión sin confirmarla con el dueño.
OPINIONES = (
    ("Renovamos 250 m² de jardín con pasto San Agustín y el resultado fue excelente desde el primer día. El césped llegó "
     "en perfectas condiciones. La asesoría para el riego fue muy útil.",
     "Carlos Herrera", "Instalación pasto en rollo · Tampico"),
    ("El equipo nos ayudó desde el diseño hasta la instalación con plantas, pasto y sistema de riego. Quedó moderno y "
     "fácil de mantener. Superó nuestras expectativas completamente.",
     "María Fernanda Ruiz", "Diseño de jardín residencial · Ciudad Madero"),
    ("Instalamos sistema de riego para un área comercial de 600 m². Proyecto bien planeado, distribución uniforme. "
     "Desde la puesta en marcha funciona perfectamente.",
     "Ing. Raúl Sánchez", "Sistema de riego comercial · Altamira"),
    ("El servicio de mantenimiento ha sido constante y profesional. Poda, fertilización y control de plagas con "
     "puntualidad. Nuestras áreas verdes se mantienen en excelente estado.",
     "Lic. Adriana Morales", "Mantenimiento de áreas verdes · Tampico"),
)
# Otras opiniones reales con nombre, publicadas con permiso del dueño (2026-11-07), textuales, de las páginas anteriores
# a la Etapa 2: la de /pasto-sintetico-tampico y las dos de /pasto-en-rollo-tampico que 2a había retirado.
OPINION_SINTETICO_TAMPICO = (
    ("Instalamos pasto sintético en la terraza de nuestra cafetería. Ya no tenemos que regar nada y siempre está "
     "verde. Los clientes preguntan si es natural.",
     "Sofía R.", "Cafetería en el centro de Tampico"),
)
OPINIONES_PASTO_EN_ROLLO = (
    ("Contraté pasto e instalación para 180 m² en mi jardín de Madero. Llegaron a la hora acordada, prepararon el "
     "terreno y quedó perfecto en un día. A las 3 semanas estaba completamente arraigado. Lo más importante: pagué el "
     "resto hasta que lo vi terminado.",
     "Jorge H.", "Residencial · Ciudad Madero · 180 m²"),
    ("Somos constructora y compramos el pasto para un fraccionamiento en Altamira. Precio de mayoreo muy competitivo, "
     "facturaron sin problema y respetaron el calendario de entrega por etapas. Ya son nuestro proveedor recurrente.",
     "Arq. Patricia L.", "Constructora · Altamira · Proyecto 2,400 m²"),
)
# Zonas con página propia (nombre visible, ruta) y las que se atienden por proyecto.
ZONAS = (
    ("Lomas de Rosales y Vista Hermosa", "/jardineria-lomas-de-rosales-tampico"),
    ("Club Campestre y Country Club", "/jardineria-country-club-tampico"),
    ("Águila, Altavista y Petrolera", "/jardineria-aguila-tampico"),
    ("Lomas del Chairel y San Gerardo", "/jardineria-lomas-del-chairel-tampico"),
    ("Cd. Madero y Playa Miramar", "/jardineria-ciudad-madero"),
    ("Altamira y Lagunas de Miralta", "/jardineria-altamira"),
)
ZONAS_POR_PROYECTO = "Pánuco, Pueblo Viejo, Tuxpan, Cd. Victoria y la Huasteca"
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
