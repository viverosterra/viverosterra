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
    "diseno_completo": 6500,
    "diseno_premium": 18000,
    "diseno_premium_descuento_desde": 150000,
    "riego_m2": (180, 320),
    "sintetico_instalado_m2": (385, 650),
    "sintetico_tienda_m2": 139,
    "poda": 500,
    "flamboyan": 250,
    "palma_desde": 250,
    "palma_real": 500,
    "tierra_negra_costal": 90,
    "tierra_negra_m3": 1500,
    "tierra_preparada_costal": 100,
    "tierra_negra_camion_5m3": 3500,
    "tierra_negra_camion_8m3": 5200,
    "tierra_negra_camion_14m3": 8000,
    "tezontle_costal": 200,
    "marmol_saco": 250,
}
# Materiales: respuestas del dueño (2026-11-08). Tierra preparada a $100 el costal y camiones de tierra negra de 5, 8 y
# 14 m³ a $3,500, $5,200 y $8,000 (nunca "camión desde $5,000": no lo confirmó). Mármol a $250 el saco, IVA incluido,
# con sus palabras: "sujeto a disponibilidad" (solo junto al precio del mármol: test_materiales_reglas.py). El m³ y el
# camión de tezontle y la piedra bola, según cotización. La piedra bola se vende a granel, no por medidas.
TIERRA_CAMIONES = tuple((m3, PRECIOS[f"tierra_negra_camion_{m3}m3"]) for m3 in (5, 8, 14))
MARMOL_CONDICION = "IVA incluido, sujeto a disponibilidad"
PIEDRA_BOLA_VENTA = "a granel"
# Condiciones de compra de materiales (dueño, 2026-11-08): sin mínimo, la entrega se cobra por viaje y todo se factura.
# "Sin mínimo" solo se publica con estas palabras (test_materiales_reglas.py).
SIN_MINIMO = "Sin mínimo de compra."
ENTREGA_COBRO = "La entrega a domicilio se cobra por viaje, según tu colonia."
FACTURACION = "Todas las compras se pueden facturar."
CONDICIONES_MATERIALES = f"{SIN_MINIMO} {ENTREGA_COBRO} {FACTURACION}"
PODA = ("Desde $500, según cotización: el precio depende del tamaño del árbol o la palma y de los residuos que se "
        "generan. Mándanos fotos y ubicación por WhatsApp.")
GARANTIA_PASTO = ("Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego "
                  "(ver condiciones).")
GARANTIA_PLANTAS = "30 días en las plantas que sembramos nosotros, con el riego indicado (ver condiciones)."
PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."
ARRAIGO = "15 a 20 días"
# Decisión del dueño (2026-11-07): la visita para medir y cotizar tiene un costo que depende de la ubicación del
# servicio. Nunca "visita sin costo" ni "gratis" (test_reglas.py); toda mención de la visita lleva una de estas dos.
VISITA_COSTO = ("El costo de la visita para cotizar depende de la ubicación del servicio; te lo confirmamos por "
                "WhatsApp antes de agendar.")
VISITA_COSTO_CORTO = "Visita para medir y cotizar: su costo depende de la ubicación"
# Servicios de jardín (Etapa 2c): ahorro de agua del riego (publicado en main) y frecuencias de mantenimiento según el
# plan y lo que necesita el jardín (decisión del dueño).
RIEGO_AHORRO = "hasta 40%"
FRECUENCIAS_MANTENIMIENTO = ("semanal", "cada 15 días", "cada 21 días", "mensual")
# Una sola forma de decir que un plan se cotiza (premium y empresa de mantenimiento): así, con mayúscula, en la
# etiqueta, las tarjetas y la tabla; en minúscula (SEGUN_COTIZACION.lower()) solo a media frase. Nunca "por cotización".
SEGUN_COTIZACION = "Según cotización"
# El plan de mantenimiento residencial premium se cotiza: no tiene precio "desde" (decisión del dueño, 2026-11-07).
MANTENIMIENTO_PREMIUM = SEGUN_COTIZACION
# Cifras confirmadas por el dueño (2026-11-07). No se publican el registro SENASICA ni "se amortiza en 18–24 meses"
# (test_reglas.py).
SISTEMAS_RIEGO = "+200"
PROYECTOS_B2B = "+200"
# Empresas (Etapa 2d). Cómo se paga un proyecto (decisión del dueño): anticipo al confirmar y el resto contra avances de
# obra, sin porcentaje y sin crédito. La misma frase en mayoreo y en palmas para proyectos (test_consistencia.py).
ANTICIPO_PROYECTOS = ("Para proyectos solicitamos un anticipo al confirmar y el resto se acuerda contra avances de obra; "
                      "te lo detallamos en la cotización.")
# Padrón público del REPSE de la STPS, donde cualquiera consulta el folio. (La ruta /Publico que cita llms.txt responde
# 404: se corrige con llms.txt en la Etapa 4.)
REPSE_PADRON = "https://repse.stps.gob.mx/"
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

# Palmas y especies para proyectos (nombre, nombre científico, precio "desde" o None). Decisión del dueño (2026-11-07):
# areca y coco plumoso desde $250 y palma real desde $500 en su tamaño más chico; el precio sube con la altura. Las demás,
# "según cotización" (SEGUN_COTIZACION): no se inventa ningún precio. Cycas, bambú y yucca se piden junto con las palmas.
PALMAS_PROYECTO = (
    ("Palma areca", "Dypsis lutescens", PRECIOS["palma_desde"]),
    ("Coco plumoso", "Syagrus romanzoffiana", PRECIOS["palma_desde"]),
    ("Palma real", "Roystonea regia", PRECIOS["palma_real"]),
    ("Palma washingtonia", "Washingtonia robusta", None),
    ("Palma del viajero", "Ravenala madagascariensis", None),
    ("Palma cola de zorro", "Wodyetia bifurcata", None),
    ("Palma triángulo", "Dypsis decaryi", None),
    ("Palma kerpis", "Hyophorbe lagenicaulis", None),
    ("Palma bambú", "Chamaedorea seifrizii", None),
    ("Cycas revoluta", "Cycas revoluta", None),
    ("Bambú tarro", "Bambusa vulgaris", None),
    ("Yucca rostrata", "Yucca rostrata", None),
)
# Plantas (Etapa 2e). Los únicos precios de plantas que dio el dueño (2026-11-07): areca y coco plumoso desde $250 y
# palma real desde $500 en su tamaño más chico (el precio sube con la altura) y flamboyán desde $250. Ninguna otra
# especie lleva precio: va SEGUN_COTIZACION (nunca los $850–$4,200 de main ni los "desde" sin confirmar del hub viejo).
# Clave: el nombre de la especie como sale en el catálogo (tools/site/contenido/catalogo_especies.json).
PRECIOS_ESPECIE = {
    "Palma Areca": PRECIOS["palma_desde"],
    "Coco Plumoso": PRECIOS["palma_desde"],
    "Palma Real": PRECIOS["palma_real"],
    "Flamboyán Tabachín": PRECIOS["flamboyan"],
}
PALMAS_PRECIO = (f"Areca y coco plumoso desde ${PRECIOS['palma_desde']}, palma real desde ${PRECIOS['palma_real']} en "
                 "tamaño chico; el precio sube con la altura")
# "Desde" de cada subcategoría de plantas: solo un precio de PRECIOS; None = SEGUN_COTIZACION (no se inventa).
DESDE_PLANTAS = {
    "/palmas-tropicales-tampico": PRECIOS["palma_desde"],
    "/plantas-para-jardin-tampico": None,
    "/arboles-ornamentales-tampico": PRECIOS["flamboyan"],
    "/arboles-para-banqueta-tampico": None,
    "/plantas-de-interior-tampico": None,
}

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
# Opiniones reales con nombre que publicaban en main las páginas de diseño, mantenimiento y riego antes de la Etapa 2c,
# textuales; el dueño confirmó que son reales y que hay permiso (2026-11-07). Nunca se editan ni se inventan otras.
OPINIONES_DISENO = (
    ("Contratamos el Plan Completo para remodelar el jardín de la casa. Hicieron la visita, nos preguntaron qué nos "
     "gustaba y qué no, y la propuesta visual que nos mandaron fue exactamente lo que teníamos en mente. El manual de "
     "cuidados nos ha servido muchísimo.",
     "Daniela M.", "Plan Completo · Residencial Tampico"),
    ("Somos un hotel boutique en Altamira y necesitábamos entregables formales para el proyecto de áreas verdes. El Plan "
     "Premium incluyó planos ejecutivos, render 3D y presentación para la junta. Muy profesional, justo lo que nuestro "
     "comité necesitaba para aprobar.",
     "Ing. Roberto S.", "Plan Premium · Hotel Boutique · Altamira"),
)
OPINIONES_MANTENIMIENTO = (
    ("Tenemos contrato mensual desde hace más de 2 años. Vienen puntuales, el jardín siempre está impecable y me avisan "
     "cuando detectan plagas o alguna planta con problemas. Ya no tengo que estar pendiente de nada.",
     "Carolina R.", "Residencial · Tampico Zona Norte"),
    ("Contratamos a Terra para mantener las áreas verdes de nuestra nave industrial en Altamira. Son más de 3,000 m² y "
     "desde que llegaron se nota la diferencia. Presentan reporte fotográfico de cada visita y facturan puntuales.",
     "Ing. Gerardo M.", "Industrial · Altamira Puerto"),
)
OPINIONES_RIEGO = (
    ("Tenía el jardín seco porque se me olvidaba regar. Terra instaló el sistema en un día, me programaron los horarios "
     "y ahora siempre está perfecto. Mi recibo de agua bajó casi a la mitad.",
     "Roberto C.", "Residencial · Tampico"),
    ("Instalaron el sistema de riego en las áreas verdes de nuestra planta industrial en Altamira. Llegaron a tiempo, el "
     "diseño es eficiente y el equipo de calidad. 100% recomendados.",
     "María V.", "Parque Industrial · Altamira"),
)
# Opiniones reales con nombre de las páginas de materiales de main, textuales; el dueño confirmó que son reales y que hay
# permiso (2026-11-08). Solo texto visible: nunca aggregateRating ni Review con calificación. En la de David M. y la de
# Patricia H., main tenía cruzados el lugar y las iniciales; aquí cada cita va con su nombre y su lugar.
OPINIONES_TIERRA_NEGRA = (
    ("Pedimos tierra negra para nivelar 200 m² antes de instalar pasto. El material llegó en perfectas condiciones, el "
     "camión descargó exactamente donde necesitábamos y el pasto arraigó en menos de 10 días. Resultado excelente.",
     "Ricardo O.", "Administrador de condominio · Altamira"),
    ("Compré costales para mejorar el jardín de mi casa en Madero. La diferencia con la tierra que tenía antes fue "
     "inmediata — las plantas están más verdes y el pasto que pusimos sobre ella arraigó muy rápido. Lo recomiendo.",
     "Laura P.", "Cliente residencial · Ciudad Madero"),
)
OPINIONES_PIEDRA_BOLA = (
    ("Hice un jardín zen en mi terraza usando piedra bola mediana, arena y bambú. Todo lo conseguí en Viveros Terra. La "
     "calidad de la piedra era muy buena y la entrega fue rápida.",
     "Patricia H.", "Residencial · Tampico"),
    ("Usamos piedra bola grande para los bordes de la fuente del hotel. Queda muy natural y elegante. Viveros Terra nos "
     "cotizó bien y coordinaron la entrega en el horario que necesitábamos.",
     "David M.", "Hotel · Altamira"),
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


# Temporada de Nochebuenas: fuente única de la página, su JSON-LD y el cotizador (public/js/vt-nochebuenas.js).
NOCHEBUENAS = {
    "ruta": "/post/nochebuenas-tampico-madero-mayoreo",
    "temporada": 2026,
    "modo": "temporada",  # "preventa" | "temporada" | "postemporada"
    "sheets_endpoint": "",  # URL del Web App de apps-script/nochebuenas-pedidos.gs
    "cortes": (1, 12, 50, 200),
    "nombres_escalon": ("Menudeo", "Mayoreo", "Mayoreo Plus", "Proyecto"),
    "productos": (
        {"clave": "5", "nombre": 'Maceta 5"', "precios": (89, 75, 69, 65)},
        {"clave": "6", "nombre": 'Maceta 6"', "precios": (139, 119, 109, 105)},
        {"clave": "7", "nombre": 'Maceta 7"', "precios": (199, 169, 155, 149)},
        {"clave": "colgante", "nombre": "Colgante", "precios": (339, 279, 259, 249)},
        {"clave": "12", "nombre": 'Macetón 12"', "precios": (1195, 995, 899, 865), "sobre_pedido": True},
    ),
    "variedades": ("Roja", "Rosa", "Jaspeada"),
    "variedades_sobre_pedido": ("Rosa", "Jaspeada"),  # decisión del dueño, 2026-11-09
    "zonas": ("Tampico", "Madero", "Altamira", "Recojo en vivero"),
    "tipos_cliente": ("Hogar", "Empresa/regalo", "Restaurante/hotel", "Comercio/plaza", "Gobierno", "Evento/posada", "Iglesia/escuela"),
    "entrega_incluida_desde": 3500,
    "preventa": {"descuento": 0.05, "hasta": "2026-11-30", "aplica_hasta_escalon": 2},
    "fecha_limite_mayoreo": "2026-11-30",
    "entrega_mayoreo_antes": "2026-12-12",
    "anticipo_pct": 50,  # solo en esta página, por indicación del dueño
    "ultima_actualizacion": "2026-11-08",
}
