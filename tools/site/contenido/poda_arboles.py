"""Contenido de /poda-arboles-tampico (SEO fase 2a, 2026-11-11; mapa de palabras clave §3a, fila 1): poda de árboles y
palmas y derribo de árboles completos. Solo datos: la plantilla es tools/site/plantillas/servicio.py, sin garantía ni
pago (datos.py no tiene garantía ni mensualidades para la poda).

Respuestas del dueño (2026-11-11), en datos.py: también derriban árboles completos (datos.DERRIBO); poda y derribo van
según cotización, la poda desde datos.PRECIOS["poda"] (datos.PODA); el retiro de los residuos va como partida aparte en
la cotización (datos.PODA_RESIDUOS); el permiso municipal lo tramita el dueño del predio (datos.PODA_PERMISO). No se
inventan costos, ligas ni pasos del trámite, y no se dice que Viveros Terra lo tramita. Sin IVA en el texto: el dueño no
lo ha dicho para la poda. La época de poda remite a la guía del blog. Página nueva: sin captura de paridad.
"""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from contenido import respuestas

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/poda-arboles-tampico"
URL = f"{SITE}{RUTA}"
OBRA = "/img/obra"
TERRA = "/img/obra/terra"
GUIA = "/blog/poda-arboles-palmas-tampico-guia"
MENSAJE = mensajes_paginas.SEO_F2A[RUTA]
PODA = dinero(P["poda"])
SEGUN = datos.SEGUN_COTIZACION

TITULO = f"Poda y Derribo de Árboles en Tampico | {datos.NOMBRE}"
DESCRIPCION = (f"Poda de árboles y palmas desde {PODA} y derribo según cotización en Tampico, Madero y Altamira. "
               "Retiro de residuos aparte. Mándanos fotos por WhatsApp.")
FOTO = {"src": f"{TERRA}/mantenimiento-jardines-02-recorte-de-seto-a-mano-640.webp",
        "srcset": (f"{TERRA}/mantenimiento-jardines-02-recorte-de-seto-a-mano-640.webp 640w, "
                   f"{TERRA}/mantenimiento-jardines-02-recorte-de-seto-a-mano.webp 973w"),
        "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 973, "alto": 1200, "numero": 1,
        # El alt y el pie de la foto en el mosaico de mantenimiento (fotos_obra.json): es un seto, no un árbol.
        "alt": "Colaborador de Viveros Terra de espaldas, con chaleco de la marca, recortando un seto con tijeras de mano.",
        "lugar": "Recorte de seto a mano", "etapa": "Mantenimiento"}
META = {
    "title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
    "og": (("og:type", "website"), ("og:title", TITULO), ("og:description", DESCRIPCION),
           ("og:image", f"{SITE}{TERRA}/mantenimiento-jardines-02-recorte-de-seto-a-mano.webp"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO),
                ("twitter:description", DESCRIPCION)),
}
SERVICIO = {
    "@type": "Service", "@id": f"{URL}#servicio", "name": "Poda y derribo de árboles y palmas",
    "serviceType": "Poda de árboles, poda de palmas y derribo de árboles",
    "description": (f"Poda de árboles y palmas desde {PODA}, según cotización, y derribo de árboles completos, según "
                    f"cotización, en Tampico, Ciudad Madero y Altamira. {datos.PODA_RESIDUOS}"),
    "provider": entidad.REF,
    "areaServed": [{"@type": "City", "name": ciudad} for ciudad in entidad.CIUDADES],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": []}  # entidad.completar lo arma de las migas visibles

OPCIONES = (
    {"rotulo": "Opción 1 · Árboles", "titulo": "Poda de árboles", "precio": P["poda"], "unidad": "por árbol",
     "detalle": SEGUN.lower(), "cta": "Cotizar la poda de un árbol",
     "puntos": ("Ramas secas, bajas o que tocan la casa", "Con técnica para no dañar el árbol",
                "El precio depende del tamaño del árbol"),
     "mensaje": ("Hola, quiero cotizar la poda de un árbol.\nColonia: ___\nCuántos árboles: ___\n"
                 "Les mando fotos y la ubicación.")},
    {"rotulo": "Opción 2 · Palmas", "titulo": "Poda de palmas", "precio": P["poda"], "unidad": "por palma",
     "detalle": SEGUN.lower(), "cta": "Cotizar la poda de palmas",
     "puntos": ("Solo hojas secas o amarillas", "Sin «poda huracán»: no se cortan hojas verdes",
                "El precio depende del tamaño de la palma"),
     "mensaje": ("Hola, quiero cotizar la poda de palmas.\nColonia: ___\nCuántas palmas: ___\n"
                 "Les mando fotos y la ubicación.")},
    {"rotulo": "Opción 3 · Derribo", "titulo": "Derribo de árboles", "precio_texto": SEGUN,
     "cta": "Cotizar un derribo",
     "puntos": ("Árboles completos que hay que quitar", "Se cotiza con fotos y la ubicación",
                "Si el municipio pide permiso, lo tramitas tú antes"),
     "mensaje": ("Hola, quiero cotizar el derribo de un árbol.\nColonia: ___\nCuántos árboles: ___\n"
                 "Les mando fotos y la ubicación.")},
)

PERMISO = (f"{datos.PODA_PERMISO} Viveros Terra no tramita el permiso: revísalo con tu municipio antes de agendar el "
           "trabajo.")
PREGUNTAS = (
    ("¿Cuánto cuesta podar un árbol en Tampico?",
     f"Desde {PODA}, según cotización: el precio depende del tamaño del árbol o la palma. {datos.PODA_RESIDUOS} "
     f"Mándanos fotos y la ubicación por WhatsApp al {datos.TELEFONO_VISIBLE} y te cotizamos."),
    ("¿Cuánto cobran por derribar un árbol?",
     f"El derribo de un árbol completo va {SEGUN.lower()}. Para cotizarlo necesitamos fotos del árbol y la ubicación. "
     f"{datos.PODA_RESIDUOS}"),
    ("¿Se necesita permiso para podar o derribar un árbol?", PERMISO),
    ("¿Cuándo conviene podar árboles y palmas en Tampico?",
     "Al final de la temporada seca (febrero y marzo), antes del nuevo crecimiento de primavera; conviene evitar podas "
     "fuertes en pleno calor (junio a agosto). En palmas solo se cortan hojas secas o amarillas. Lo explicamos en la "
     f'<a href="{GUIA}">guía de poda de árboles y palmas</a>.'),
    ("¿También derriban árboles completos?", f"Sí. {datos.DERRIBO} {datos.PODA_RESIDUOS}"),
    ("¿Cómo se paga?", f"{datos.ANTICIPO} Te damos factura {datos.FACTURA} si la necesitas."),
    ("¿En qué zonas trabajan?",
     f"En Tampico, Ciudad Madero y Altamira; {datos.ZONAS_POR_PROYECTO}, por proyecto."),
)

PASOS = (
    {"titulo": "Fotos y ubicación", "quien": "tu", "cuando": "Antes de cotizar",
     "texto": "Nos mandas por WhatsApp fotos del árbol o la palma y la ubicación, y nos dices si buscas poda o derribo."},
    {"titulo": "Cotización", "quien": "nosotros", "cuando": "Al cotizar",
     "texto": (f"Te mandamos la cotización de la poda o el derribo. {datos.PODA_RESIDUOS} Si hace falta verlo en "
               f"persona, agendamos una visita. {datos.VISITA_COSTO}")},
    {"titulo": "Permiso, si aplica", "quien": "tu", "cuando": "Antes del trabajo",
     "texto": datos.PODA_PERMISO},
    {"titulo": "Poda o derribo", "quien": "nosotros", "cuando": "El día acordado",
     "texto": "Hacemos el trabajo cotizado, con técnica para no dañar el árbol ni la palma que se queda."},
    {"titulo": "Retiro de residuos", "quien": "nosotros", "cuando": "Al terminar",
     "texto": "Retiramos los residuos que se generan, según la partida de la cotización."},
)

# Fotos reales que el sitio ya publica, con su alt y su pie de siempre (no son de una poda en particular).
FIGURAS = (
    {"src": f"{OBRA}/mantenimiento-jardin-tropical-tampico.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Jardín residencial tropical con pasto y plantas recién podadas.",
     "lugar": "Jardín residencial tropical", "etapa": "Mantenimiento mensual"},
    {"src": f"{TERRA}/palmas-tropicales-01-grupo-de-palmas.webp",
     "srcset": f"{TERRA}/palmas-tropicales-01-grupo-de-palmas-640.webp 640w, {TERRA}/palmas-tropicales-01-grupo-de-palmas.webp 1050w",
     "sizes": "(min-width: 900px) 33vw, 100vw", "ancho": 1050, "alto": 1200, "numero": 3,
     "alt": "Jardinera con un grupo de palmas sobre tierra negra, junto a un muro blanco.",
     "lugar": "Grupo de palmas", "etapa": "En instalación"},
)

CONTENIDO = {
    "respuesta": respuestas.de(RUTA),
    "tipo": "servicio-poda",
    "prefijo": "poda",
    "ctas": {"opciones": (MENSAJE, "Cotizar poda o derribo"), "faq": (MENSAJE, "Preguntar por WhatsApp")},
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": entidad.SPEAKABLE},
    "migas": (("Inicio", "/"), ("Poda de árboles", None)),
    "portada": {
        "kicker": "Poda · Tampico, Madero y Altamira",
        "pos": "50% 30%",
        "h1": "Poda y derribo de árboles en Tampico",
        "lema": "Para árboles y palmas que ya crecieron de más.",
        "lede": "Podamos árboles y palmas de casas, comercios y empresas, y derribamos árboles completos cuando hace falta.",
        "etiqueta": {
            "codigo": "Poda · 01", "aviso": SEGUN, "nombre": "Poda de árboles y palmas",
            "antes": "Por árbol o palma · desde", "monto": PODA, "unidad": "",
            "filas": (("Derribo", SEGUN.lower()), ("Retiro de residuos", "partida aparte")),
        },
        "mensaje": MENSAJE,
        "enlaces": (("Precios", "#precio"),),
        "dato": "Fotos y ubicación por WhatsApp para cotizar",
        "foto": FOTO,
    },
    "prueba": {
        "titulo": "Poda con técnica, sin dañar la planta",
        "lede": ("Cortamos lo que hace falta y nada más: en árboles, ramas secas, bajas o que estorban; en palmas, solo "
                 "las hojas secas o amarillas. Si una raíz levanta la banqueta, te recomendamos especies de raíz "
                 'controlada (<a href="/arboles-para-banqueta-tampico">árboles para banqueta</a>).'),
        "figuras": FIGURAS,
        "nota": (PERMISO, "Antes de agendar"),
        "titulo_clientes": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
    },
    "opciones": {
        "rotulo": "Servicios",
        "titulo": "Poda de árboles, poda de palmas o derribo",
        "lede": "Dinos qué necesitas y mándanos fotos: cada trabajo se cotiza por separado.",
        "fila": True,
        "items": OPCIONES,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta podar o derribar un árbol en Tampico?",
        "lede": f"{datos.PODA.removesuffix(' Mándanos fotos y ubicación por WhatsApp.')} {datos.DERRIBO}",
        "tabla": {"columnas": ("Concepto", "Unidad", "Precio"),
                  "filas": (("Poda de árbol o palma", "por árbol o palma", f"desde {PODA}, {SEGUN.lower()}"),
                            ("Derribo de árbol completo", "por árbol", SEGUN),
                            ("Retiro de residuos", "partida aparte", SEGUN))},
        "caption": ('El precio cerrado sale de las fotos y la ubicación. Lista completa en '
                    '<a href="/precios">viverosterra.com/precios</a>.'),
    },
    "incluye": {
        "rotulo": "Antes de agendar",
        "titulo": "Permiso, residuos y época de poda",
        "lede": "Lo que conviene saber antes de podar o derribar.",
        "items": (
            {"titulo": "Permiso municipal: lo tramitas tú", "texto": PERMISO},
            {"titulo": "Residuos: partida aparte", "texto": datos.PODA_RESIDUOS},
            {"titulo": "Cuándo podar",
             "texto": ("Al final de la temporada seca, antes de la primavera. Detalle por especie en la "
                       f'<a href="{GUIA}">guía de poda de árboles y palmas</a>.')},
        ),
    },
    "proceso": {"titulo": "Cómo trabajamos una poda o un derribo",
                "lede": "De las fotos por WhatsApp al trabajo terminado, con cada paso claro.",
                "pasos": PASOS},
    "faq": {"titulo": "Preguntas sobre poda y derribo en Tampico", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Tienes un árbol o una palma que podar?",
        "lede": ("Mándanos fotos del árbol o la palma y la ubicación, y dinos si buscas poda o derribo. Te cotizamos con "
                 "el retiro de residuos aparte."),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Poda de árboles en Tampico, Madero y Altamira.",
        "lede": 'Casas, comercios y empresas de la zona conurbada; ve todas las <a href="/zonas">zonas de servicio</a>.',
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Mantenimiento de jardines", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": f"Desde {dinero(P['mantenimiento_mes'])}/mes · Poda, fertilización y cuidados"},
            {"titulo": "Árboles para banqueta", "href": "/arboles-para-banqueta-tampico",
             "img": "/img/portadas/arboles-vivero-tampico-mayoreo-sm.webp", "ancho": 560, "alto": 840,
             "texto": "Especies que no levantan el pavimento"},
            {"titulo": "Áreas verdes para empresas", "href": "/empresas",
             "img": f"{OBRA}/mantenimiento-areas-verdes-empresa.webp", "ancho": 640, "alto": 961,
             "texto": f"REPSE {datos.REPSE} y factura {datos.FACTURA}"},
        ),
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
    "hero": ("Página nueva (SEO fase 2a, 2026-11-11): hero de marca como las demás páginas de servicio, con un solo botón "
             "de WhatsApp, el teléfono de enlace, la línea de confianza y la etiqueta con la poda desde $500 según "
             "cotización; sin captura anterior que comparar."),
}
