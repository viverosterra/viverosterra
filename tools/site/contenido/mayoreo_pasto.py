"""Contenido de /mayoreo-pasto-tampico (pasto San Agustín al mayoreo para obras). Solo datos: la plantilla es
tools/site/plantillas/b2b.py, con el cotizador de pasto por volumen (componentes.cotizador_volumen: la regla del
Medidor, así que con menos de 500 m² nunca sale a $60), clientes con nombre y logo, REPSE verificable, la opinión real
de una constructora (datos.OPINIONES_PASTO_EN_ROLLO, con permiso del dueño) y 3 paquetes con su mensaje.

Precios de datos.PRECIOS ($60 desde 500 m², $85 solo pasto, desde $120 instalado). La capacidad por entrega y los plazos
no están en datos.py: la tabla dice que van por escrito en la cotización (hoja de ruta 2d: el dueño los da o no se
publican). Título, canonical, robots, Open Graph y Service como estaban publicados; la descripción y su og:description
corrigen el "Factura CFDI, factura CFDI" repetido (PARIDAD["meta"]). Revisión 2d: el Service apunta a la entidad única
#negocio (PARIDAD["jsonld"]) y las migas del JSON-LD son las visibles. FAQPage de las preguntas visibles.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import b2b_comun

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/mayoreo-pasto-tampico"
URL = f"{SITE}{RUTA}"
OBRA = "/img/obra"
MAYOREO, MINIMO, SOLO, INSTALADO = (P["pasto_mayoreo_m2"], P["pasto_mayoreo_minimo_m2"], P["pasto_solo_m2"],
                                    P["pasto_instalado_m2"])
MENSAJE = mensajes_paginas.EMPRESAS[RUTA]
DESCRIPCION = (f"Pasto San Agustín en rollo al mayoreo desde ${MAYOREO}/m² en pedidos de {MINIMO} m² o más, para "
               f"constructoras y proyectos en Tampico. Factura {datos.FACTURA} y entrega por etapas. Viveros Terra, desde "
               f"{datos.DESDE}.")
DESCRIPCION_OG = (f"Pasto San Agustín en rollo al mayoreo desde ${MAYOREO}/m² en pedidos de {MINIMO} m² o más, para "
                  f"constructoras y proyectos en Tampico. Factura {datos.FACTURA} y entrega por etapas.")

META = {
    "title": f"Pasto al mayoreo en Tampico desde ${MAYOREO}/m² para constructoras · Viveros Terra",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Pasto al Mayoreo en Tampico para Constructoras · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/pasto-en-rollo-san-agustin-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}
SERVICIO = {
    "@type": "Service", "serviceType": "Suministro de Pasto al Mayoreo",
    "name": "Pasto al Mayoreo en Tampico para Constructoras",
    "description": ("Suministro de pasto San Agustín en rollo al mayoreo para constructoras, arquitectos, fraccionamientos, "
                    "hoteles y empresas en Tampico, Ciudad Madero y Altamira. Precio preferencial por volumen, factura "
                    "CFDI 4.0 y entrega por etapas según avance de obra."),
    "provider": {"@id": f"{SITE}/#negocio"},  # la entidad de las demás páginas (el nodo completo vive en la home)
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
}
# Las mismas migas que se ven (CONTENIDO["migas"]).
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
    {"@type": "ListItem", "position": 2, "name": "Pasto en rollo", "item": f"{SITE}/pasto-en-rollo-tampico"},
    {"@type": "ListItem", "position": 3, "name": "Mayoreo", "item": URL},
]}

PREGUNTAS = (
    ("¿Cuál es el pedido mínimo para mayoreo de pasto en Tampico?",
     f"Para precios de mayoreo manejamos pedidos a partir de {MINIMO} m²: desde {dinero(MAYOREO)}/m² solo pasto (no lleva IVA). "
     f"Con menos de {MINIMO} m² también te atendemos, a {dinero(SOLO)}/m² solo pasto o desde {dinero(INSTALADO)}/m² "
     'instalado (<a href="/pasto-en-rollo-tampico">pasto en rollo</a>).'),
    ("¿Facturan CFDI para constructoras?",
     f"Sí, emitimos factura {datos.FACTURA} para constructoras, empresas y cualquier cliente que requiera comprobante "
     "fiscal. Solo necesitamos tu RFC y datos fiscales al momento de la compra."),
    ("¿Pueden entregar pasto fuera de Tampico?",
     f"Sí. Además de Tampico, Ciudad Madero y Altamira, atendemos proyectos en {datos.ZONAS_POR_PROYECTO}. Para "
     "proyectos fuera del área metropolitana cotizamos el flete por separado según la distancia y el volumen."),
    ("¿Cómo funciona la entrega por etapas para obras?",
     "Coordinamos la entrega de pasto según el avance de tu obra. Puedes hacer un pedido global y programar las entregas "
     "parciales en las fechas que necesitas, para que cada etapa reciba pasto fresco. Esto evita que el material se "
     "dañe si no se instala de inmediato."),
    ("¿Cuánto pasto pueden surtir por entrega?",
     "Depende de tu calendario: el volumen de cada entrega y sus fechas van por escrito en la cotización, antes de que "
     f"confirmes. El pasto llega del campo {datos.LLEGADA_PASTO} y se corta para tu pedido."),
    ("¿También instalan el pasto en la obra?",
     "Sí, con nuestra cuadrilla. La instalación en obra se cotiza según el terreno y el volumen, e incluye la garantía de "
     f"arraigo de {datos.ARRAIGO} siguiendo el protocolo de riego. Si lo instala tu cuadrilla, te entregamos el pasto "
     "fresco y el protocolo por escrito."),
    b2b_comun.PREGUNTA_PAGO,
    b2b_comun.PREGUNTA_REPSE,
)

PASOS = (
    {"titulo": "Contáctanos por WhatsApp", "quien": "tu", "cuando": "Para empezar",
     "texto": ("Cuéntanos tu proyecto: superficie en m², ubicación de la obra y fecha de inicio de la instalación. Si "
               "tienes plano, mándalo.")},
    {"titulo": "Cotización por escrito", "quien": "nosotros", "cuando": "Al revisar tu proyecto",
     "texto": "Te enviamos precio por m², costo total, condiciones de pago y el calendario de entregas por etapas."},
    {"titulo": "Anticipo y calendario", "quien": "juntos", "cuando": "Al confirmar",
     "texto": "Confirmas con un anticipo y fijamos juntos las fechas de cada entrega según el avance de la obra."},
    {"titulo": "Entregas por etapas", "quien": "nosotros", "cuando": "En cada etapa",
     "texto": f"El pasto llega del campo {datos.LLEGADA_PASTO} y se corta para tu pedido: cada entrega llega fresca."},
    {"titulo": "Factura y siguiente etapa", "quien": "juntos", "cuando": "Contra avance",
     "texto": f"Cada pago lleva su factura {datos.FACTURA}; los siguientes se acuerdan contra avances de obra."},
)

FIGURAS = (
    {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 2,
     "alt": "Rollos de pasto San Agustín recién cortados en la camioneta de reparto.",
     "lugar": "Rollos recién cortados", "etapa": "En la camioneta de reparto"},
    {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp", "ancho": 640, "alto": 960, "numero": 3,
     "alt": "Cuadrilla de Viveros Terra tendiendo pasto San Agustín en rollo.", "lugar": "Cuadrilla tendiendo pasto",
     "etapa": "Instalación"},
    {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 4,
     "alt": "Pasto San Agustín recién instalado junto a un andador.", "lugar": "Después", "etapa": "Día de instalación"},
)

PAQUETES = (
    {"rotulo": "Paquete 1 · Solo pasto", "titulo": "Pasto de mayoreo para tu cuadrilla", "precio": MAYOREO,
     "unidad": "/m²", "detalle": f"en pedidos de {MINIMO} m² o más",
     "puntos": ("Pasto San Agustín cortado para tu pedido", "Entregas parciales según el avance de la obra",
                f"Factura {datos.FACTURA} para persona física o moral"),
     "mensaje": ("Hola, quiero cotizar pasto San Agustín al mayoreo (solo pasto).\nEmpresa: ___\nObra y ubicación: ___\n"
                 "m² totales: ___\nEntregas (fechas o etapas): ___")},
    {"rotulo": "Paquete 2 · Instalado", "titulo": "Pasto instalado en obra", "precio_texto": datos.SEGUN_COTIZACION,
     "detalle": "según el terreno y el volumen", "rec": True,
     "puntos": ("Preparación básica del terreno y colocación con nuestra cuadrilla",
                f"Garantía de arraigo de {datos.ARRAIGO} siguiendo el protocolo de riego",
                f"REPSE {datos.REPSE} para trabajar dentro de tu obra"),
     "mensaje": ("Hola, quiero cotizar pasto instalado en una obra.\nEmpresa: ___\nObra y ubicación: ___\n"
                 "m² totales: ___\nEstado del terreno (nivelado, con tierra, con escombro): ___")},
    {"rotulo": "Paquete 3 · Áreas verdes", "titulo": "Pasto, palmas y riego para la obra",
     "precio_texto": datos.SEGUN_COTIZACION, "detalle": "con un solo proveedor",
     "puntos": ('Pasto, <a href="/palmas-mayoreo-proyectos">palmas para proyectos</a> y árboles',
                '<a href="/sistema-riego-tampico">Riego automático</a> para grandes áreas',
                '<a href="/mantenimiento-jardines-tampico">Mantenimiento</a> después de la entrega'),
     "mensaje": ("Hola, quiero cotizar las áreas verdes de una obra (pasto, palmas y riego).\nEmpresa: ___\n"
                 "Obra y ubicación: ___\nm² de áreas verdes: ___\nFecha de entrega: ___")},
)

CONTENIDO = {
    "tipo": "b2b",
    "prefijo": "may",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    # /empresas llega en la Etapa 3: entonces se inserta ("Empresas", "/empresas") aquí y en MIGAS_LD.
    "migas": (("Inicio", "/"), ("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Mayoreo", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Constructoras · Fraccionamientos · Industria",
        "h1": 'Pasto al mayoreo <span class="vt-serif">para obras y fraccionamientos</span>',
        "lede": (f"En Viveros Terra el pasto San Agustín al mayoreo cuesta desde {dinero(MAYOREO)}/m² (solo pasto) en "
                 f"pedidos de {MINIMO} m² o más, con factura {datos.FACTURA}; el pasto sin instalar no lleva IVA. Entregamos por etapas según el "
                 "avance de tu obra en Tampico, Madero y Altamira; fuera de la zona, por proyecto."),
        "etiqueta": {
            "codigo": "Mayoreo · 01", "aviso": "Solo pasto", "nombre": "Pasto San Agustín para obra",
            "cientifico": "Stenotaphrum secundatum", "antes": "Mayoreo · desde", "monto": dinero(MAYOREO),
            "unidad": "/m²",
            "filas": (("Pedido mínimo", f"{MINIMO} m²"), (f"Con menos de {MINIMO} m²", f"{dinero(SOLO)}/m² solo pasto")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'REPSE {datos.REPSE} · factura {datos.FACTURA} · <a href="#precio">calcula tu obra por m²</a>'),
        "foto": {"src": "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp",
                 "srcset": ("/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp 560w, "
                            "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Cuadrilla instalando pasto San Agustín en rollo", "lugar": "Pasto San Agustín para obra",
                 "etapa": "Instalación"},
    },
    "prueba": {
        "titulo": "Clientes que confían en Viveros Terra",
        "lede": (f"{datos.PROYECTOS_B2B} proyectos B2B y {datos.M2_INSTALADOS} instalados en Tamaulipas y la Huasteca, "
                 f"desde {datos.DESDE}: constructoras, fraccionamientos, hoteles, industria y gobierno."),
        "figuras": FIGURAS,
        "nota": (f'Si tu obra necesita menos de {MINIMO} m², el mayoreo no aplica: te conviene el '
                 f'<a href="/pasto-en-rollo-tampico">pasto en rollo</a> a {dinero(SOLO)}/m², con el mismo pasto y la '
                 "misma entrega.", "Al cotizar"),
        "titulo_opinion": "Lo que dice una constructora",
        "opiniones": datos.OPINIONES_PASTO_EN_ROLLO[1:],
    },
    "escalas": {
        "titulo": "¿Cuánto cuesta el pasto en rollo al mayoreo?",
        "lede": (f"Desde {dinero(MAYOREO)}/m² solo pasto en pedidos de {MINIMO} m² o más; con menos, {dinero(SOLO)}/m². "
                 f"La instalación en obra, {datos.SEGUN_COTIZACION.lower()}. Precios {datos.ANIO}: el pasto sin instalar no lleva IVA; lista "
                 'completa en <a href="/precios">viverosterra.com/precios</a>.'),
        # La unidad va con el precio ("$85/m²"): sin columna Unidad, la tarjeta de celular tiene una línea menos.
        "columnas": ("Volumen", "Precio", "Entrega"),
        "filas": (
            (f"Menos de {MINIMO} m²", f"{dinero(SOLO)}/m² solo pasto", "Se cotiza según tu obra"),
            (f"{MINIMO} m² o más", f"desde {dinero(MAYOREO)}/m² solo pasto", "Por etapas, según el avance de obra"),
            ("Pasto instalado en obra", f"desde {dinero(INSTALADO)}/m² instalado, con IVA", "Con nuestra cuadrilla"),
            ("Capacidad y calendario", "Por escrito en tu cotización, por entrega",
             f"El pasto llega del campo {datos.LLEGADA_PASTO}"),
        ),
        "caption": (f"{datos.PASTO_SIN_IVA}. El cotizador estima solo el pasto; la entrega y la instalación se cotizan "
                    "con tu obra."),
        "titulo_cotizador": "Calcula tu obra por m²",
        "cotizador": "volumen",
    },
    "formulario": {
        "titulo": "¿Compras prefiere correo? Pide la cotización por escrito",
        "lede": b2b_comun.LEDE_CORREO,
        "pagina": "Mayoreo de pasto", "cta": "mayoreo:formulario",
        "cantidad": ("m² totales de la obra", "Ej. 1,200 m²", False, "decimal"),
        "aviso": b2b_comun.AVISO_PRIVACIDAD,
    },
    "documentacion": {
        "titulo": "Documentación para compras",
        "lede": "Lo que piden compras, finanzas y supervisión de obra para liberar el pago.",
        "items": b2b_comun.DOCUMENTACION,
    },
    "paquetes": {
        "titulo": "Paquetes por tipo de obra",
        "lede": "Cada botón abre WhatsApp con la plantilla de ese paquete.",
        "items": PAQUETES,
        "nota": (f'¿Menos de {MINIMO} m²? <a href="/pasto-en-rollo-tampico">Pasto en rollo</a> a {dinero(SOLO)}/m² solo '
                 f"pasto o desde {dinero(INSTALADO)}/m² instalado."),
    },
    "proceso": {"titulo": "Proceso de cotización", "lede": "De tu mensaje a la última entrega, todo por escrito.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo cuando instalamos nosotros.", "grande": "15–20", "unidad": "días",
        "resumen": f"Garantía de arraigo de {datos.ARRAIGO} con instalación contratada.",
        "puntos": (
            ("Si contratas la instalación y se sigue el protocolo de riego de 20 días, garantizamos el arraigo: si una "
             f"sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo.", True),
            (f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}; cada entrega por etapas llega fresca.", True),
            ("Protocolo de riego por escrito para quien riega la obra.", True),
            ("En mayoreo solo pasto, la instalación es de tu cuadrilla: la garantía de arraigo no aplica, pero te "
             "entregamos el protocolo de riego.", False),
        ),
        "pie": ('<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a> · '
                '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de cuidados de 20 días</a>'),
    },
    "faq": {"titulo": "Preguntas de compras sobre pasto al mayoreo", "preguntas": PREGUNTAS},
    "cobertura": dict(b2b_comun.COBERTURA, titulo="Pasto para obras en Tampico, Madero, Altamira y la región.",
                      lede="Entregamos en la zona conurbada y, por proyecto, en el resto de la región; el flete se cotiza "
                           "por distancia y volumen."),
    "relacionados": {"titulo": "Otras soluciones para empresas", "items": b2b_comun.relacionados(RUTA)},
    "cierre": {
        "titulo": "¿Listo para cotizar tu obra?",
        "lede": ("Mándanos los m² totales, la ubicación y la fecha de la primera entrega. Te enviamos precio por m², "
                 "calendario y condiciones por escrito."),
        "mensaje": MENSAJE,
    },
}

PARIDAD = {
    "meta": {
        "description": (DESCRIPCION, "Corrige el “Factura CFDI, factura CFDI” repetido de main; el resto queda igual."),
        "og:description": (DESCRIPCION_OG, "Corrige el “Factura CFDI, factura CFDI” repetido de main; el resto queda igual."),
    },
    "reemplazos": {
        "Ventajas para tu empresa u obra": "Documentación para compras",
        "Precio preferencial por volumen": "¿Cuánto cuesta el pasto en rollo al mayoreo?",
        "Entrega por etapas según obra": "Entregas por etapas",
        "Preguntas frecuentes — Mayoreo B2B": "Preguntas de compras sobre pasto al mayoreo",
    },
    "retirados": {
        "Pasto en rollo al mayoreo para constructoras y proyectos": (
            "La definición pasa a la entrada de la portada como respuesta directa (spec §7.3), con precio, mínimo, "
            "factura y cobertura de datos.py."),
        "Pasto fresco garantizado": (
            "Pasa a la garantía (“Cortado para tu pedido: llega del campo…”) y al paso “Entregas por etapas”; “entrega "
            "con grúa” no está en datos.py y queda como pregunta al dueño."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” (confirmado por el dueño) "
            "pasa a la entrada de la sección de clientes."),
    },
    # Tipos del JSON-LD que ya no salen, con su motivo (paridad.comparar).
    "jsonld": {
        "LocalBusiness": ("El provider del Service apunta por @id a la entidad única #negocio de las demás páginas (el "
                          "nodo completo vive en la home), en vez de un LocalBusiness suelto. Revisión 2d."),
        "PostalAddress": "Iba dentro del LocalBusiness suelto del provider; la dirección completa es del nodo #negocio.",
    },
}
