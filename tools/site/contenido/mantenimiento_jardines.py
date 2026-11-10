"""Contenido de /mantenimiento-jardines-tampico (jardinero y mantenimiento mensual). Solo datos: la plantilla es
tools/site/plantillas/servicio.py, con 3 planes (cada uno con su propio mensaje de WhatsApp: auditoría 02, "el plan
elegido no viaja al chat"), tabla comparativa, lo que incluye cada visita, frecuencia por temporada, proceso, garantía
sin permanencia forzada y pago mensual.

Precios de datos.PRECIOS (desde $750/mes; el residencial premium va "según cotización", datos.MANTENIMIENTO_PREMIUM,
respuesta del dueño del 2026-11-07); frecuencias de
datos.FRECUENCIAS_MANTENIMIENTO; visita con datos.VISITA_COSTO (su costo depende de la ubicación; nunca gratis).
Título y descripción (también en Open Graph y Twitter Card): los de la fase 0 de SEO (contenido/seo.py). Canonical, Service y migas como estaban publicados; FAQPage de las preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/mantenimiento-jardines-tampico"
OBRA = "/img/obra"
BASICO = P["mantenimiento_mes"]
COTIZA = datos.SEGUN_COTIZACION  # premium y empresa: una sola redacción; en minúscula solo a media frase
PREMIUM = datos.MANTENIMIENTO_PREMIUM  # el dueño no da precio "desde" para el premium
FRECUENCIAS = ", ".join(datos.FRECUENCIAS_MANTENIMIENTO[:-1]) + " o " + datos.FRECUENCIAS_MANTENIMIENTO[-1]
MENSAJE = mensajes_paginas.SERVICIOS["/mantenimiento-jardines-tampico"]

TITULO = f"Mantenimiento de Jardines Tampico desde {dinero(BASICO)} | Viveros Terra"
DESCRIPCION = (f"Jardinero y mantenimiento de jardines en Tampico desde {dinero(BASICO)} al mes: poda, fertilización y control de "
               "plagas con visitas programadas. Cotiza por WhatsApp.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", TITULO),
        ("og:description", DESCRIPCION),
        ("og:image", f"{SITE}/img/mantenimiento-jardines-poda-pasto-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}

SERVICIO = {
    "@type": "Service", "serviceType": "Mantenimiento de Jardines", "name": "Mantenimiento de Jardines Tampico",
    "description": ("Servicio profesional de mantenimiento de jardines residenciales, corporativos e industriales en "
                    "Tampico, Ciudad Madero y Altamira. Incluye poda, fertilizacion, control de plagas y revision "
                    f"general. Desde {BASICO} pesos mensuales con cotizacion personalizada segun el espacio."),
    "provider": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
                 "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                             "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}},
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
    "offers": {"@type": "Offer", "priceCurrency": "MXN", "price": str(BASICO),
               "description": (f"Servicio mensual desde {BASICO} pesos con cotizacion personalizada segun tamano, tipo "
                               "y ubicacion del jardin.")},
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Mantenimiento de Jardines Tampico", "item": URL},
]}

PLANES = (
    {"rotulo": "Plan 1 · Hasta 200 m²", "titulo": "Residencial básico", "precio": BASICO, "unidad": "/mes",
     "detalle": "Visita mensual; cada 21 días en lluvias si tu jardín lo pide",
     "puntos": ("Poda de pasto, arbustos y plantas", "Fertilización trimestral", "Control de plagas a solicitud",
                "Limpieza y recolección de residuos", "Reporte con fotos de cada visita"),
     "mensaje": (f"Hola, me interesa el plan de mantenimiento Residencial básico (desde {dinero(BASICO)}/mes).\n"
                 "Colonia: ___\nMetros aprox. del jardín: ___\nFrecuencia que busco (mensual o cada 21 días): ___")},
    {"rotulo": "Plan 2 · 200 a 500 m²", "titulo": "Residencial premium", "precio_texto": PREMIUM,
     "rec": True, "detalle": "Visita cada 15 días",
     "puntos": ("Poda especializada de pasto, arbustos y palmas", "Fertilización mensual",
                "Control de plagas preventivo", "Revisión del sistema de riego", "Reporte con fotos de cada visita"),
     "mensaje": (f"Hola, me interesa el plan de mantenimiento Residencial premium ({PREMIUM.lower()}, visita cada 15 días).\n"
                 "Colonia: ___\nMetros aprox. del jardín: ___\nTengo palmas o sistema de riego: ___")},
    {"rotulo": "Plan 3 · 500 m² o más", "titulo": "Empresa e industria", "precio_texto": COTIZA,
     "detalle": f"Visita semanal con cuadrilla · REPSE {datos.REPSE} y factura {datos.FACTURA}",
     "puntos": ("Poda con cuadrilla", "Fertilización quincenal", "Programa anual de control de plagas",
                "Operación del sistema de riego", "Contrato de servicios y reporte con fotos de cada visita"),
     "mensaje": (f"Hola, me interesa el plan de mantenimiento para empresa o industria ({COTIZA.lower()}).\n"
                 "Empresa: ___\nUbicación: ___\n"
                 f"m² de áreas verdes: ___\nFrecuencia que buscan ({FRECUENCIAS}): ___")},
)

COMPARA = {
    "titulo": "Planes de Mantenimiento — comparativa por tipo de jardín",
    "columnas": ("Plan", "Residencial básico", "Residencial premium", "Empresa e industria"),
    "filas": (
        ("Tamaño ideal", "Hasta 200 m²", "200 a 500 m²", "500 m² o más"),
        ("Frecuencia", "Mensual", "Cada 15 días", "Semanal"),
        ("Poda", "Incluida", "Especializada", "Con cuadrilla"),
        ("Fertilización", "Trimestral", "Mensual", "Quincenal"),
        ("Control de plagas", "A solicitud", "Preventivo", "Programa anual"),
        ("Riego automatizado", "No incluido", "Revisión incluida", "Operación incluida"),
        ("Precio", f"desde {dinero(BASICO)}/mes", PREMIUM, COTIZA),
    ),
    "caption": f"Precios {datos.ANIO} con IVA. La frecuencia final depende de tu plan y de lo que necesita tu jardín.",
}

INCLUYE = (
    {"titulo": "Poda de pasto",
     "texto": ("Corte parejo a la altura de cada variedad. El San Agustín se mantiene entre 5 y 8 cm para conservar la "
               "humedad con el calor.")},
    {"titulo": "Poda de arbustos y plantas",
     "texto": "Poda de formación y sanitaria de arbustos, setos y plantas, con la técnica de cada especie."},
    {"titulo": "Fertilización programada",
     "texto": "Calendario según especies, temporada y tipo de suelo, para que el pasto siga verde todo el año."},
    {"titulo": "Control de plagas",
     "texto": ("Monitoreo y tratamiento preventivo de las plagas de Tampico: gusano del pasto, chinches, hormigas "
               "cortadoras y hongos por exceso de humedad.")},
    {"titulo": "Limpieza y recolección",
     "texto": "Retiro de hojas, ramas y residuos después de cada servicio, y traslado de la basura vegetal."},
    {"titulo": "Revisión general",
     "texto": "El jardinero revisa el pasto, las plantas y el riego, y te reporta cualquier problema con su recomendación."},
)

PREGUNTAS = (
    ("¿Cuánto cuesta el mantenimiento mensual?",
     f"Desde {dinero(BASICO)} al mes en jardines residenciales de hasta 200 m²; los jardines de 200 a 500 m² con visita "
     "cada 15 días (plan premium) se cotizan según el jardín. El precio exacto depende del tamaño, las plantas, el nivel de "
     f"servicio y la ubicación. {datos.VISITA_COSTO}"),
    ("¿Con qué frecuencia vienen al jardín?",
     f"Según tu plan y lo que necesita tu jardín: {FRECUENCIAS}. En temporada de lluvias (junio a septiembre) el pasto "
     "crece rápido y conviene cada 15 o 21 días; en temporada seca (octubre a mayo), mensual."),
    ("¿Qué incluye cada visita?",
     "Poda de pasto y arbustos, fertilización según el calendario, control preventivo de plagas, limpieza y recolección "
     "de residuos, y revisión general del jardín. Si hay sistema de riego, el jardinero revisa que funcione bien."),
    ("¿Puedo contratar sin haber hecho el jardín con Terra?",
     "Sí. Atendemos jardines existentes sin importar quién los instaló. En la visita revisamos el estado actual, "
     f"identificamos problemas y te proponemos el plan mensual adecuado. {datos.VISITA_COSTO}"),
    ("¿Trabajan con empresas, hoteles y parques industriales?",
     "Sí. Atendemos corporativos, hoteles, fraccionamientos, escuelas, parques industriales y gobierno. Emitimos factura "
     f"{datos.FACTURA}, contamos con REPSE {datos.REPSE}, trabajamos con contrato de servicios y adaptamos el calendario "
     "a la operación del cliente."),
    ("¿Hay permanencia forzada o puedo cancelar?",
     "No hay permanencia forzada. El contrato es mensual y renovable, y puedes cancelar con 30 días de aviso."),
    ("¿Qué pasa si detectan una plaga o problema?",
     "Te lo reportamos de inmediato con fotos y una recomendación. Si el tratamiento cabe en tu plan, lo hacemos en la "
     "misma visita; si requiere un tratamiento especializado o materiales adicionales, te mandamos la cotización para "
     "que la autorices."),
    ("¿Hacen mantenimiento correctivo además del preventivo?",
     "Sí. Si el jardín está descuidado, primero hacemos un servicio correctivo para ponerlo en condiciones, que se cotiza "
     "aparte del mantenimiento mensual. Después entramos al ritmo de mantenimiento programado."),
)

PASOS = (
    {"titulo": "Visita inicial", "quien": "nosotros", "cuando": "Antes de cotizar",
     "texto": (f"{datos.VISITA_COSTO_CORTO}. Revisamos el estado del jardín, medimos el área, identificamos las plantas y revisamos "
               "el riego si lo hay.")},
    {"titulo": "Plan personalizado", "quien": "juntos", "cuando": "Al cotizar",
     "texto": (f"Definimos contigo la frecuencia ({FRECUENCIAS}), el alcance (poda, fertilización, plagas, riego) y el "
               "precio mensual fijo.")},
    {"titulo": "Primera visita técnica", "quien": "nosotros", "cuando": "Primera visita",
     "texto": ("Los jardineros llegan a la hora acordada, hacen la primera intervención completa y detectan cualquier "
               "problema de plagas, nutrición o riego.")},
    {"titulo": "Mantenimiento programado", "quien": "nosotros", "cuando": "Según el calendario",
     "texto": "Poda de pasto y arbustos, fertilización, control de plagas, limpieza y revisión del riego en cada visita."},
    {"titulo": "Reportes mensuales con fotos", "quien": "juntos", "cuando": "Después de cada visita",
     "texto": ("Recibes un reporte con fotos de lo realizado y del estado del jardín. Si algo requiere atención "
               "especial, te avisamos antes de actuar.")},
)

FIGURAS = (
    {"src": f"{OBRA}/mantenimiento-jardin-tropical-tampico.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Jardín residencial tropical con pasto y plantas recién podadas.",
     "lugar": "Jardín residencial tropical", "etapa": "Mantenimiento mensual"},
    {"src": f"{OBRA}/mantenimiento-areas-verdes-empresa.webp", "ancho": 640, "alto": 961, "numero": 3,
     "alt": "Áreas verdes de una empresa con pasto cortado y arriates.",
     "lugar": "Áreas verdes de empresa", "etapa": "Mantenimiento programado"},
    {"src": f"{OBRA}/mantenimiento-jardin-residencial-pasto.webp", "ancho": 640, "alto": 961, "numero": 4,
     "alt": "Jardín residencial con pasto parejo y plantas ornamentales.",
     "lugar": "Jardín residencial", "etapa": "Después de la visita"},
)

SECTORES = (
    ("Residenciales", "Casas y privadas"),
    ("Empresas y oficinas", "Contrato de servicios con factura"),
    ("Hoteles y restaurantes", "Jardines de imagen"),
    ("Fraccionamientos", "Áreas comunes"),
    ("Parques industriales", f"REPSE {datos.REPSE}"),
    ("Escuelas e instituciones", "Áreas verdes y patios"),
)

CONTENIDO = {
    "tipo": "servicio-mantenimiento",
    "prefijo": "mantenimiento",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Mantenimiento de jardines", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Jardinería · Tampico, Madero y Altamira",
        "h1": 'Mantenimiento de jardines y jardinero en Tampico <span class="vt-serif">con visitas programadas</span>',
        # Corta para que el precio y el CTA quepan en la primera pantalla del celular; las frecuencias van en la FAQ.
        "lede": "Poda, fertilización, control de plagas y riego para casas y empresas.",
        "etiqueta": {
            "codigo": "Jardín · mensual", "aviso": "Con IVA", "nombre": "Mantenimiento de jardín",
            "antes": "Residencial · desde", "monto": dinero(BASICO), "unidad": "/mes",
            "filas": (("Otros planes", COTIZA),),
        },
        "mensaje": MENSAJE,
        "tambien": (f'REPSE {datos.REPSE} y factura {datos.FACTURA} para empresas · '
                    '<a href="#opciones">elige tu plan</a> · sin permanencia forzada'),
        "foto": {"src": "/img/portadas/mantenimiento-jardines-poda-pasto-tampico-sm.webp",
                 "srcset": ("/img/portadas/mantenimiento-jardines-poda-pasto-tampico-sm.webp 560w, "
                            "/img/portadas/mantenimiento-jardines-poda-pasto-tampico.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Jardinero de Viveros Terra podando pasto en un jardín de Tampico",
                 "lugar": "Poda de pasto", "etapa": "Tampico"},
    },
    "prueba": {
        "titulo": "Jardines que mantenemos en Tampico",
        "lede": "Casas, empresas y áreas verdes de la zona con mantenimiento programado.",
        "figuras": FIGURAS,
        "nota": ("Si tu jardín está muy descuidado, la primera visita no es de mantenimiento: es un correctivo que se "
                 "cotiza aparte. Te lo decimos antes de empezar.", "En la visita inicial"),
        # La opinión de mantenimiento aprobada de la home y las dos que publicaba esta página en main (reales y con
        # permiso, confirmadas por el dueño: datos.OPINIONES_MANTENIMIENTO).
        "titulo_opinion": "Lo que dicen nuestros clientes mensuales",
        "opiniones": datos.OPINIONES[3:4] + datos.OPINIONES_MANTENIMIENTO,
        "titulo_clientes": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
    },
    "opciones": {
        "rotulo": "Planes",
        "titulo": "¿Cuánto cuesta el mantenimiento de jardín en Tampico?",
        "lede": (f"Desde {dinero(BASICO)} al mes en jardines residenciales de hasta 200 m², con poda, fertilización y "
                 "control de plagas; de 200 a 500 m² o con palmas y riego, el plan premium se cotiza según tu jardín. Empresas, "
                 f"fraccionamientos e industria se cotizan con REPSE {datos.REPSE} y factura {datos.FACTURA}. Precios "
                 f'{datos.ANIO} con IVA; lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "items": PLANES,
        "tabla": COMPARA,
        "nota": ("Para jardines de hasta 200 m², el plan básico es suficiente. Si tu jardín tiene palmas grandes o sistema "
                 "de riego, el premium cada 15 días da mejor resultado a largo plazo."),
    },
    "incluye": {
        "titulo": "Servicios de mantenimiento profesional",
        "lede": "Cada visita sigue el mismo protocolo, y el reporte con fotos te dice qué se hizo.",
        "items": INCLUYE,
    },
    "objecion": {
        "rotulo": "Frecuencia",
        "titulo": "Dos temporadas, dos ritmos de mantenimiento",
        "lede": "Ajustamos la frecuencia al ritmo real de crecimiento de tu jardín en Tampico, dentro de tu plan.",
        "comparativa": {
            "columnas": ("Temporada", "Meses", "Qué pasa en el jardín", "Frecuencia recomendada"),
            "filas": (
                ("Temporada de lluvias", "Junio a septiembre",
                 "El pasto y las plantas crecen más rápido con la humedad y el calor.",
                 "Cada 15 o 21 días; semanal en jardines grandes"),
                ("Temporada seca", "Octubre a mayo",
                 "Crece más lento, pero necesita fertilización y revisar el riego para seguir verde.",
                 "Mensual o cada 21 días"),
            ),
            "caption": "Frecuencia según la temporada en Tampico.",
            "cierre": f"La frecuencia final ({FRECUENCIAS}) la fijamos contigo según tu plan y lo que necesita tu jardín.",
        },
    },
    "proceso": {"titulo": "Cómo contratar mantenimiento de jardines en 5 pasos",
                "lede": "Para que tu jardín esté siempre en condiciones sin que tengas que estar pendiente.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Sin permanencia forzada: contrato mensual renovable.", "grande": "30",
        "unidad": "días de aviso para cancelar",
        "resumen": "Te quedas porque el servicio es constante, no porque te obliguemos.",
        "puntos": (
            ("Contrato mensual renovable; puedes cancelar con 30 días de aviso.", True),
            ("Precio mensual fijo según tu plan, sin sorpresas.", True),
            ("Si detectamos una plaga o un problema, te lo reportamos con fotos; si cabe en tu plan, lo atendemos en la "
             "misma visita.", True),
            (f"Factura {datos.FACTURA} y contrato de servicios; REPSE {datos.REPSE} para empresas.", True),
            ("Los tratamientos especializados, los materiales adicionales y el correctivo de un jardín descuidado se "
             "cotizan aparte.", False),
        ),
        "pie": ('<a href="/politicas#garantia-plantas">Las plantas que sembramos nosotros tienen 30 días de garantía de '
                "arraigo, con el riego indicado (ver condiciones)</a>"),
    },
    "pago": {
        "titulo": "Cómo se paga: cada mes, con factura.",
        "lede": (f"{datos.ANTICIPO} Después pagas cada mes el precio fijo de tu plan, por transferencia, efectivo o "
                 "tarjeta."),
        "puntos": (
            "Precio mensual fijo según tu plan y la frecuencia acordada.",
            f"Factura {datos.FACTURA} para persona física o moral.",
            ("El correctivo inicial, una obra de jardín o un sistema de riego se pueden pagar en mensualidades con tarjeta "
             "de crédito: el total a plazos es mayor que el de contado. "
             '<a href="/politicas#mensualidades">Condiciones</a>'),
        ),
    },
    "faq": {"titulo": "Todo sobre mantenimiento de jardines", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Tu jardín necesita mantenimiento profesional?",
        "lede": (f"Dinos tu colonia, los metros de tu jardín y si es casa o empresa. Agendamos una visita para medir y "
                 f"cotizar. {datos.VISITA_COSTO}"),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Jardinero y mantenimiento en Tampico, Madero y Altamira.",
        "lede": "Casas, empresas e industria de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo San Agustín", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"Pasto desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Diseño de Jardines", "href": "/diseno-jardines-tampico",
             "img": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427,
             "texto": f"Plan Terra desde {dinero(P['diseno'])} · Propuesta visual"},
            {"titulo": "Sistema de Riego", "href": "/sistema-riego-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": f"Automatizado · Ahorra {datos.RIEGO_AHORRO} de agua"},
        ),
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION),
    "reemplazos": {
        "Mantenimiento de jardines en Tampico, cada mes": (
            "Mantenimiento de jardines y jardinero en Tampico con visitas programadas"),
        "Atendemos": "Sectores que atendemos",
        "Cuanto cuesta el mantenimiento de jardin en Tampico?": "¿Cuánto cuesta el mantenimiento mensual?",
        "Con que frecuencia se hace el mantenimiento?": "¿Con qué frecuencia vienen al jardín?",
        "Que incluye el servicio de mantenimiento?": "¿Qué incluye cada visita?",
        "Trabajan con empresas, hoteles y fraccionamientos?": "¿Trabajan con empresas, hoteles y parques industriales?",
        "Puedo contratar mantenimiento sin haber hecho el jardin con Viveros Terra?": (
            "¿Puedo contratar sin haber hecho el jardín con Terra?"),
    },
    "retirados": {
        "Cuidado profesional programado para tu jardín": (
            "La definición del servicio queda en la entrada de la portada y en la respuesta directa de los planes."),
        "Temporada de lluvias": "Las dos temporadas pasan a filas de la tabla “Dos temporadas, dos ritmos de mantenimiento”.",
        "Temporada seca": "Las dos temporadas pasan a filas de la tabla “Dos temporadas, dos ritmos de mantenimiento”.",
        "Desde $750/mes": (
            "El precio desde $750/mes y sus factores quedan en la etiqueta de la portada y en los planes ($750 y “Según "
            "cotización”, datos.SEGUN_COTIZACION), una sola sección de precio."),
        "Cotización mensual por WhatsApp": (
            "El formulario que armaba el mensaje (sendWA) se sustituye por un botón con su propio mensaje en cada plan "
            "(auditoría 02: los 4 CTA mandaban el mismo texto) y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” (confirmado por el dueño) "
            "pasa al título de los clientes; la certificación SENASICA no se publica (decisión del dueño)."),
        "$6": "El rango “aprox. $6–$12 por m² al mes” no es dato oficial (datos.py); el precio sale de la visita.",
        "$12": "El rango “aprox. $6–$12 por m² al mes” no es dato oficial (datos.py); el precio sale de la visita.",
        "$1,800": ("Respuesta del dueño (2026-11-07): el plan residencial premium no es “desde $1,800/mes”; va "
                   "“según cotización” (datos.MANTENIMIENTO_PREMIUM)."),
        "$90": "“Complementa tu proyecto” (tierra negra) sale; los materiales siguen en el menú y el pie.",
        "$1,500": "“Complementa tu proyecto” (tierra negra) sale; los materiales siguen en el menú y el pie.",
    },
}
