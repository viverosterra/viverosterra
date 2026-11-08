"""Contenido de /piedra-bola-rio-tampico (piedra bola de río chica, mediana y grande, por costal o camión). Solo datos:
la plantilla es tools/site/plantillas/material.py.

Main no publicaba precio (solo el JSON-LD, con un Offer de $350 e "InStock" que nadie dio): todo va "según cotización".
Main tampoco tenía calculadora: la nueva multiplica el área por los 120 a 150 kg por m² que decía su propia pregunta
frecuente (pregunta 6 al dueño). Las opiniones de Patricia H. y David M. no tienen permiso del dueño y se retiran. Sin
foto de portada (main no la tenía); sus 3 fotos en su orden: la del CTA final y, después, las dos miniaturas de otros
materiales (por eso "otros" va tras el cierre). Título y descripción como estaban; el Open Graph pierde el “gratis”.
"""
import datos
import mensajes_paginas
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

SITE = datos.SITIO
RUTA = "/piedra-bola-rio-tampico"
URL = f"{SITE}{RUTA}"
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Piedra bola de río")
DESCRIPCION_OG = ("Piedra bola de río natural en Tampico para jardines, senderos y decoración. Pequeña, mediana y "
                  "grande. Entrega a domicilio en Madero y Altamira. Cotiza por WhatsApp.")
META = {
    "title": "Piedra Bola de Río Tampico · Jardines y Senderos",
    "description": ("Piedra bola de río natural en Tampico para jardines y senderos. Pequeña, mediana y grande. Costal y "
                    "camión volteo. Entrega a domicilio en Tampico y zona."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Piedra Bola de Río Tampico | Venta para Jardines y Senderos — Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/jardin-residencial-plantas-pasto-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}
USOS = (
    {"titulo": "Senderos y caminos", "texto": "Piedra mediana para caminos decorativos: deja pasar el agua, resiste y pide "
     "poco mantenimiento.", "puntos": ("Mediana, 6 a 12 cm",)},
    {"titulo": "Jardines zen y japoneses", "texto": "Piedra bola mediana con arena o gravilla y vegetación minimalista.",
     "puntos": ("Mediana",)},
    {"titulo": "Cubierta decorativa de suelo", "texto": "Piedra chica sobre camas de plantas y arriates: ayuda contra la "
     "maleza, mejora el drenaje y da un aspecto limpio.", "puntos": ("Chica, 2 a 5 cm",)},
    {"titulo": "Fuentes y estanques", "texto": "Piedra grande en la base de fuentes, bordes de estanques y elementos de "
     "agua.", "puntos": ("Grande, 12 a 20 cm",)},
    {"titulo": "Borduras y delimitadores", "texto": "Piedra grande colocada de canto para delimitar zonas, arriates y "
     "senderos.", "puntos": ("Grande",)},
    {"titulo": "Contraste con tezontle", "texto": ("Piedra bola gris con tezontle rojo, un contraste bicolor para "
     'paisajismo moderno. <a href="/tezontle-rojo-tampico">Ver tezontle rojo</a>.'), "puntos": ("Chica o mediana",)},
)
PREGUNTAS = (
    ("¿Para qué se usa la piedra bola de río en jardinería?",
     "Para cubrir el suelo de jardines y áreas verdes, hacer senderos y caminos, delimitar arriates, diseñar jardines zen "
     "o japoneses, decorar fuentes y estanques y dar acabados naturales en exteriores."),
    ("¿En qué tamaños se vende la piedra bola de río en Tampico?",
     "En tres medidas: chica (2 a 5 cm), para cubrir suelo y borduras; mediana (6 a 12 cm), para senderos y decoración; "
     "y grande (12 a 20 cm), para puntos focales y fuentes. Se pueden combinar en la misma entrega."),
    ("¿La piedra bola de río necesita mantenimiento?",
     "Casi ninguno: limpieza ocasional con agua a presión si junta polvo o lodo y reponer lo que se desplace con las "
     "lluvias o el uso. No pierde su aspecto con el tiempo."),
    ("¿Cuánta cantidad de piedra bola necesito para mi jardín?",
     "Con piedra mediana y capa de 8 a 10 cm se usan de 120 a 150 kg por m²: para un sendero de 1 m de ancho por 10 m de "
     f"largo (10 m²), {ejemplo('piedra-bola', 10)}. Usa la calculadora de esta página o mándanos la medida y el área."),
    ("¿Se puede combinar piedra bola de río con tezontle y mármol?",
     "Sí. La piedra bola gris con tezontle rojo da un contraste bicolor para jardines zen o contemporáneos, y el mármol "
     "blanco de fondo con borduras de piedra bola también se usa en jardines residenciales de Tampico."),
    ("¿Entregan piedra bola de río a domicilio en Tampico?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto: por costal para "
     "cantidades chicas o en camión volteo para proyectos medianos y grandes. El costo de entrega depende del volumen y "
     "la distancia."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-piedra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Piedra bola de río <em>para jardines y senderos</em>",
        "lede": ("Piedra de río natural en tres medidas para senderos, jardines secos y fuentes. Por costal o camión; "
                 "el precio se cotiza según la medida y el volumen, con entrega en Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Piedra bola", "aviso": "Por medida", "nombre": "Chica, mediana y grande", "antes": "",
                     "monto": "3 medidas", "unidad": "costal o camión",
                     "filas": (("Chica", "2 a 5 cm"), ("Mediana", "6 a 12 cm"), ("Grande", "12 a 20 cm"),
                               ("Precio", SEGUN)),
                     "nota": "Te damos el precio por escrito con la entrega."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuántos kg necesitas</a>.',
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Qué es la piedra bola de río y para qué sirve en jardines?",
        "parrafos": (
            ("Es una roca natural de río, ovalada y lisa, pulida por la corriente del agua. En jardinería se usa como "
             "elemento decorativo y como cubierta de suelo que ayuda contra la maleza y mejora el drenaje. La tenemos en "
             "tres medidas para casas, comercios y proyectos de paisajismo en Tampico."),
        ),
    },
    "precio": {
        "titulo": "¿Cuánto cuesta la piedra bola de río en Tampico?",
        "lede": "El precio depende de la medida y del volumen: te lo damos por escrito antes de que confirmes.",
        "caption": "Piedra bola de río por medida",
        "filas": (
            {"nombre": "Chica", "detalle": "2 a 5 cm · cubierta de suelo y borduras", "unidad": "costal o camión",
             "precio": None},
            {"nombre": "Mediana", "detalle": "6 a 12 cm · senderos y decoración", "unidad": "costal o camión",
             "precio": None},
            {"nombre": "Grande", "detalle": "12 a 20 cm · fuentes y puntos focales", "unidad": "costal o camión",
             "precio": None},
        ),
        "nota": "El costo de entrega se cotiza según tu colonia y el volumen.",
    },
    "usos": {"titulo": "¿Cómo se usa la piedra bola de río en Tampico?",
             "lede": "Cada uso con la medida que le va.", "items": USOS},
    "calculadora": {"clave": "piedra-bola", "nombre": "piedra bola", "titulo": "¿Cuánta piedra bola necesitas?",
                    "lede": "Escribe el área: te damos los kg aproximados con piedra mediana y capa de 8 a 10 cm."},
    "entrega": mc.entrega("la piedra bola"),
    "faq": {"titulo": "Todo sobre piedra bola de río en Tampico", "preguntas": PREGUNTAS},
    "cierre": {"titulo": "¿Qué proyecto tienes en mente con piedra bola de río?",
               "lede": "Dinos la medida, el área y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/jardin-residencial-plantas-pasto-tampico.webp", "ancho": 933, "alto": 1400}},
    "otros": {"titulo": "Otros materiales decorativos", "tras_cierre": True,
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/tierra-negra-vegetal-tampico", "/marmol-blanco-tampico"),
                                con_miniatura=True)},
    "pedido": mc.pedido("Ejemplo: piedra bola mediana para 10 m², entrega en Altamira"),
    "jsonld": {
        "producto": mc.producto(
            "Piedra Bola de Río para Jardín Tampico",
            ("Piedra bola de río natural para jardines en Tampico, en medida chica, mediana y grande. Por costal y camión "
             "volteo, con entrega a domicilio en Tampico, Madero y Altamira."),
            f"{SITE}/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp", sku="VT-PIE-001"),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {"og:description": (DESCRIPCION_OG, "Sin “Cotiza gratis” (regla del dueño); el resto queda igual.")},
    "reemplazos": {},
    "retirados": {
        "Lo que dicen nuestros clientes": mc.MOTIVO_TESTIMONIOS,
        "/piedra-bola-rio-tampico": "Era el enlace de la página a sí misma en “Otros materiales”; ahí va el mármol blanco.",
    },
    "jsonld": {
        "Offer": ("El Offer publicaba $350 e “InStock”: ni el precio está en datos.py ni hay dato de existencias. El "
                  "Product queda sin oferta hasta que el dueño dé el precio (pregunta 2)."),
        "LocalBusiness": mc.MOTIVO_LOCALBUSINESS,
    },
}
