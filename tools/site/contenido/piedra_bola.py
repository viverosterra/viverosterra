"""Contenido de /piedra-bola-rio-tampico (piedra bola de río a granel). Solo datos: la plantilla es
tools/site/plantillas/material.py.

El dueño (2026-11-08): se vende a granel, no por medidas; no se publican chica, mediana ni grande (texto, tablas,
calculadora, preguntas y comparativas de las otras páginas). Main no publicaba precio (solo el JSON-LD, con un Offer de
$350 e "InStock" que nadie dio): va "según cotización". Main tampoco tenía calculadora: la nueva multiplica el área por
los 120 a 150 kg por m² que decía su propia pregunta frecuente, sin medida. Las opiniones de Patricia H. y David M.
vuelven textuales (reales y con permiso: datos.OPINIONES_PIEDRA_BOLA), sin calificación en el JSON-LD; main tenía
cruzados su lugar y sus iniciales. Sin mínimo de compra, entrega por viaje y factura en todo. Sin foto de portada (main
no la tenía); sus 3 fotos en su orden. Título, descripción y Open Graph sin “Pequeña, mediana y grande” ni “gratis”.
"""
import datos
import mensajes_paginas
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc
from contenido import seo

SITE = datos.SITIO
RUTA = "/piedra-bola-rio-tampico"
URL = f"{SITE}{RUTA}"
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Piedra bola de río")
TITULO = "Piedra Bola de Río en Tampico a Granel | Viveros Terra"
DESCRIPCION = ("Piedra bola de río natural en Tampico para jardines, senderos y jardines secos. Venta "
               f"{datos.PIEDRA_BOLA_VENTA} con entrega a domicilio; precio {datos.SEGUN_COTIZACION.lower()}. Cotiza.")
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
        ("og:image", f"{SITE}/img/jardin-residencial-plantas-pasto-tampico.webp"),
        ("og:locale", "es_MX"),
        ("og:site_name", datos.NOMBRE),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),  # como estaba publicada en main
}
USOS = (
    {"titulo": "Senderos y caminos", "texto": ("Caminos decorativos de piedra de río: deja pasar el agua, resiste y pide "
     'poco mantenimiento. <a href="/diseno-jardines-tampico">Diseño de jardines en Tampico</a>.'),
     "puntos": ("Capa de 8 a 10 cm: 120 a 150 kg por m²",)},
    {"titulo": "Jardines zen y japoneses", "texto": ("Piedra bola con arena o gravilla y vegetación minimalista. "
     '<a href="/plantas-palmas-arboles-tampico">Plantas, palmas y árboles en Tampico</a>.')},
    {"titulo": "Cubierta decorativa de suelo", "texto": "Sobre camas de plantas y arriates: ayuda contra la maleza, "
     "mejora el drenaje y da un aspecto limpio."},
    {"titulo": "Fuentes y estanques", "texto": "En la base de fuentes, bordes de estanques y elementos de agua."},
    {"titulo": "Borduras y delimitadores", "texto": "Colocada de canto para delimitar zonas, arriates y senderos."},
    {"titulo": "Contraste con tezontle", "texto": ("Piedra bola gris con tezontle rojo, un contraste bicolor para "
     'paisajismo moderno. <a href="/tezontle-rojo-tampico">Tezontle rojo en Tampico</a>.')},
)
PREGUNTAS = (
    ("¿Para qué se usa la piedra bola de río en jardinería?",
     "Para cubrir el suelo de jardines y áreas verdes, hacer senderos y caminos, delimitar arriates, diseñar jardines zen "
     "o japoneses, decorar fuentes y estanques y dar acabados naturales en exteriores."),
    ("¿Cómo se vende la piedra bola de río en Tampico?",
     f"{datos.PIEDRA_BOLA_VENTA.capitalize()}: no se vende por medidas. Dinos el área o los kg que necesitas y tu "
     f"colonia y te mandamos el precio por escrito con la entrega. {datos.SIN_MINIMO}"),
    ("¿La piedra bola de río necesita mantenimiento?",
     "Casi ninguno: limpieza ocasional con agua a presión si junta polvo o lodo y reponer lo que se desplace con las "
     "lluvias o el uso. No pierde su aspecto con el tiempo."),
    ("¿Cuánta cantidad de piedra bola necesito para mi jardín?",
     "Con capa de 8 a 10 cm se usan de 120 a 150 kg por m²: para un sendero de 1 m de ancho por 10 m de largo "
     f"(10 m²), {ejemplo('piedra-bola', 10)}. Usa la calculadora de esta página o mándanos el área."),
    ("¿Se puede combinar piedra bola de río con tezontle y mármol?",
     "Sí. La piedra bola gris con tezontle rojo da un contraste bicolor para jardines zen o contemporáneos, y el mármol "
     "blanco de fondo con borduras de piedra bola también se usa en jardines residenciales de Tampico."),
    ("¿Entregan piedra bola de río a domicilio en Tampico?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto, a granel; "
     f"en camión volteo para obras y proyectos. {datos.ENTREGA_COBRO}"),
    mc.pregunta_condiciones("piedra bola"),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-piedra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "dato": "Te damos el precio por escrito con la entrega",
        "enlaces": (("Calcula cuántos kg necesitas", "#calculadora", "material:calculadora"),),
        "h1": 'Piedra bola de río en Tampico <span class="vt-serif">para jardines y senderos</span>',
        "lede": ("Piedra de río natural, a granel, para senderos, jardines secos y fuentes. El precio se cotiza según "
                 "la cantidad."),
        "etiqueta": {"codigo": "Piedra bola", "aviso": "A granel", "nombre": "Por m²", "antes": "",
                     "monto": "120–150 kg", "unidad": "capa de 8 a 10 cm",
                     "filas": (("Venta", datos.PIEDRA_BOLA_VENTA.capitalize()), ("Precio", SEGUN)),
                     "nota": f"{datos.SIN_MINIMO} Te damos el precio por escrito con la entrega."},
        "mensaje": MENSAJE,
    },
    "que_es": {
        "titulo": "¿Qué es la piedra bola de río y para qué sirve en jardines?",
        "parrafos": (
            ("Es una roca natural de río, ovalada y lisa, pulida por la corriente del agua. En jardinería se usa como "
             "elemento decorativo y como cubierta de suelo que ayuda contra la maleza y mejora el drenaje. Se vende a "
             "granel para casas, comercios y proyectos de paisajismo en Tampico."),
        ),
    },
    "precio": {
        "titulo": "¿Cuánto cuesta la piedra bola de río en Tampico?",
        "lede": "El precio depende de la cantidad: te lo damos por escrito antes de que confirmes.",
        "caption": "Piedra bola de río",
        "filas": (
            {"nombre": "Piedra bola de río", "detalle": "A granel · 120 a 150 kg por m² con capa de 8 a 10 cm",
             "unidad": "a granel", "precio": None},
        ),
        "nota": datos.CONDICIONES_MATERIALES,
    },
    "usos": {"titulo": "¿Cómo se usa la piedra bola de río en Tampico?",
             "lede": "Senderos, jardines secos, fuentes y borduras.", "items": USOS},
    "calculadora": {"clave": "piedra-bola", "nombre": "piedra bola", "titulo": "¿Cuánta piedra bola necesitas?",
                    "lede": "Escribe el área: te damos los kg aproximados con capa de 8 a 10 cm."},
    "entrega": mc.entrega("la piedra bola"),
    "opiniones": {"titulo": "Lo que dicen nuestros clientes", "items": datos.OPINIONES_PIEDRA_BOLA},
    "faq": {"titulo": "Todo sobre piedra bola de río en Tampico", "preguntas": PREGUNTAS},
    "cierre": {"titulo": "¿Qué proyecto tienes en mente con piedra bola de río?",
               "lede": "Dinos el área y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/jardin-residencial-plantas-pasto-tampico.webp", "ancho": 933, "alto": 1400}},
    "otros": {"titulo": "Otros materiales decorativos",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/tierra-negra-vegetal-tampico", "/marmol-blanco-tampico"),
                                con_miniatura=True)},
    "pedido": mc.pedido("Ejemplo: piedra bola de río para 10 m², entrega en Altamira"),
    "jsonld": {
        "negocio": mc.NEGOCIO,
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION, {
        "description": (DESCRIPCION, f"Sin “Pequeña, mediana y grande” ni “Costal”: {mc.MOTIVO_SIN_MEDIDAS}"),
        "og:description": (DESCRIPCION, f"Sin “Pequeña, mediana y grande” ni “gratis”: {mc.MOTIVO_SIN_MEDIDAS}"),
    }),
    "reemplazos": {
        # H1 con «en Tampico» (SEO fase 0, 2026-11-10): la consulta es «piedra bola de río Tampico».
        "Piedra bola de río para jardines y senderos": "Piedra bola de río en Tampico para jardines y senderos",
        "¿En qué tamaños se vende la piedra bola de río en Tampico?": "¿Cómo se vende la piedra bola de río en Tampico?",
    },
    "retirados": {
        "/piedra-bola-rio-tampico": "Era el enlace de la página a sí misma en “Otros materiales”; ahí va el mármol blanco.",
    },
    "jsonld": {
        "Offer": ("El Offer publicaba $350 e “InStock”: ni el precio está en datos.py ni hay dato de existencias. Sin "
                  "oferta no sale el Product: el dueño la dejó según cotización (2026-11-08)."),
        "Product": mc.MOTIVO_SIN_PRODUCTO,
        "Brand": "Iba dentro del Product, que ya no sale (sin precio en datos.py; revisión 2f).",
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). El lema del <h1> va en <span class="vt-serif"> (antes <em>). Entrada recortada: la zona de entrega sigue en «Entrega». Sin foto: no se agrega ninguna.')
