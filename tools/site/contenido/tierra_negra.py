"""Contenido de /tierra-negra-vegetal-tampico (tierra negra vegetal por costal, m³ o camión). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularTierra) como función pura.

Precios de datos.PRECIOS: costal $90 y m³ $1,500. La tierra preparada ($100), el camión ("desde $5,000") y los camiones de
5, 8 y 14 m³ ($3,500, $5,200, $8,000) no están en datos.py: van "según cotización" (preguntas al dueño). Las 8 fotos de
main, en su orden. Sin “Entrega inmediata”, “+500 jardines”, “40% más rápido” ni “gratis”; las opiniones de Ricardo O.
y Laura P. no tienen permiso del dueño y se retiran. Título, robots y canonical como estaban; la descripción y el Open
Graph pierden los precios que no están en datos.py y el “gratis” (PARIDAD["meta"]). El peso del costal no se publica:
main decía “≈ 20 kg” y “de 30 a 40 kg” (PARIDAD["cifras"], pregunta 5 al dueño).
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/tierra-negra-vegetal-tampico"
URL = f"{SITE}{RUTA}"
COSTAL, M3 = dinero(P["tierra_negra_costal"]), dinero(P["tierra_negra_m3"])
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Tierra negra vegetal")
DESCRIPCION = (f"Tierra negra vegetal en Tampico. Costal {COSTAL} · m³ {M3} · camión volteo según cotización. Entrega a "
               "domicilio en Madero y Altamira. Cotiza por WhatsApp.")
DESCRIPCION_OG = (f"Tierra negra vegetal para jardín y pasto en Tampico. Costal {COSTAL}, m³ {M3} y camión volteo según "
                  "cotización. Cotiza por WhatsApp.")

META = {
    "title": "Tierra Negra Vegetal Tampico · Costal y Camión Volteo",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Tierra Negra Vegetal Tampico · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/camion-tierra-negra-entrega-tampico.webp"),
        ("og:locale", "es_MX"),
        ("og:site_name", datos.NOMBRE),
    ),
    # Twitter Card como estaba publicada en main.
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", "Tierra Negra Vegetal Tampico · Viveros Terra"),
        ("twitter:description", "Tierra negra vegetal para jardín y pasto. Costal o camión volteo. Entrega Tampico, "
                                "Madero, Altamira."),
        ("twitter:image", f"{SITE}/img/camion-tierra-negra-entrega-tampico.webp"),
    ),
}


def _figura(src, ancho, alto, numero, alt, lugar, etapa):
    return {"src": src, "ancho": ancho, "alto": alto, "numero": numero, "alt": alt, "lugar": lugar, "etapa": etapa}


PORTADA_FOTO = {
    "src": "/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp",
    "srcset": ("/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp 560w, "
               "/img/portadas/camion-tierra-negra-entrega-tampico.webp 960w"),
    "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 960, "alto": 640, "numero": 1,
    "alt": "Camión de Viveros Terra entregando tierra negra en Tampico", "lugar": "Entrega de tierra negra",
    "etapa": "Tampico"}
FIGURAS_QUE_ES = (
    _figura("/img/tierra-negra-preparacion-pasto-tampico.webp", 1400, 787, 2,
            "Tierra negra vegetal extendida para instalar pasto en un jardín de Tampico", "Base para pasto", "Preparación"),
    _figura("/img/tierra-negra-camion-volteo-tampico.webp", 821, 471, 3,
            "Entrega de tierra negra en camión volteo en Tampico", "Camión volteo", "Entrega a granel"),
    _figura("/img/tierra-negra-suministro-jardin-tampico.webp", 1400, 787, 4,
            "Tierra negra con materia orgánica para jardines en Tampico", "Tierra negra", "En el jardín"),
)
FIGURAS_GALERIA = (
    _figura("/img/camion-tierra-negra-descarga-tampico.webp", 1053, 1018, 5,
            "Camión de Viveros Terra descargando tierra negra en una obra de jardinería en Tampico", "Descarga en obra",
            "Camión volteo"),
    _figura("/img/tierra-negra-vegetal-costales-tampico.webp", 1400, 933, 6,
            "Costales de tierra negra vegetal de Viveros Terra", "Costales", "Por costal"),
    _figura("/img/tierra-negra-sacos-viveros-terra.webp", 1400, 933, 7, "Tierra negra vegetal en sacos para jardín",
            "Sacos de tierra negra", "Por costal"),
)

USOS = (
    {"titulo": "Preparación para pasto en rollo",
     "texto": ("Una capa de 5 a 10 cm de tierra negra antes de instalar pasto San Agustín: el pasto arraiga parejo y el "
               "suelo no se compacta."),
     "puntos": ("Referencia: 1 m³ por cada 10 a 20 m²",)},
    {"titulo": "Cajetes para árboles y palmas",
     "texto": ("Relleno de cajete con tierra negra para ayudar al arraigo de árboles ornamentales, palmas tropicales y "
               "arbustos recién plantados."),
     "puntos": ("Referencia: 0.1 a 0.3 m³ por árbol",)},
    {"titulo": "Mejora de jardines existentes",
     "texto": ("Aplicación superficial de 3 a 5 cm sobre jardines con suelo pobre o compacto: mejora el color del pasto y "
               "la salud de las plantas sin remover el jardín."),
     "puntos": ("Referencia: 1 m³ por cada 20 a 30 m²",)},
    {"titulo": "Nivelación de terrenos",
     "texto": ("Relleno y nivelación de terrenos irregulares antes de jardines, fraccionamientos u obras, en camiones "
               "volteo coordinados por etapas."),
     "puntos": ("Camiones de 5, 8 y 14 m³",)},
    {"titulo": "Macetas y jardineras grandes",
     "texto": ("Sustrato base para macetones y jardineras: se mezcla con perlita o arena gruesa 70/30 para que drene y no "
               "se encharque."),
     "puntos": ("Por costal",)},
    {"titulo": "Proyectos comerciales e industriales",
     "texto": ("Áreas verdes en fraccionamientos, condominios, parques industriales y escuelas: camiones coordinados por "
               f"etapas con factura {datos.FACTURA}."),
     "puntos": (f"Por camión, {mc.SEGUN}",)},
)

PREGUNTAS = (
    ("¿Cuánto cuesta un camión de tierra negra en Tampico?",
     f"El camión volteo de tierra negra se cotiza según el volumen y la distancia de entrega: escríbenos tu colonia y la "
     f"cantidad y te mandamos el precio por escrito antes de que confirmes. A granel por m³ cuesta {M3} y el costal, "
     f"{COSTAL}."),
    ("¿Para qué sirve la tierra negra vegetal?",
     "Para preparar terrenos antes de instalar pasto en rollo, rellenar cajetes de árboles y palmas, mejorar el suelo "
     "arcilloso de Tampico, nivelar terrenos y como sustrato base en macetas grandes. Aporta materia orgánica, retiene "
     "humedad y mejora la textura del suelo para que las raíces penetren mejor."),
    ("¿Cuánta tierra negra necesito para mi jardín?",
     f"m² del área × grosor de la capa en metros = m³. Por ejemplo, para 100 m² con capa de 8 cm necesitas "
     f"{ejemplo('tierra-negra', 100, 0.08)}. Para preparar pasto se recomiendan de 5 a 10 cm; para cajetes de árboles, "
     "de 0.1 a 0.3 m³ por árbol. Usa la calculadora de esta página o mándanos tus medidas por WhatsApp."),
    ("¿Qué diferencia hay entre tierra negra y tierra común de Tampico?",
     "La tierra arcillosa de Tampico es compacta, pobre en nutrientes y drena mal: cuando llueve se encharca y cuando se "
     "seca se endurece. La tierra negra vegetal tiene más materia orgánica, una textura suelta que deja crecer las raíces "
     "y retiene la humedad que necesitan las plantas."),
    ("¿El pasto arraiga mejor con tierra negra?",
     f"Sí. El pasto San Agustín sobre una capa de 8 cm de tierra negra arraiga más parejo que sobre suelo arcilloso: las "
     f"raíces encuentran suelo suelto y nutrido durante sus {datos.ARRAIGO} de arraigo y el riesgo de que se levante "
     "baja mucho."),
    ("¿Entregan tierra negra a domicilio en toda la zona de Tampico?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto, en camión "
     "volteo con descarga en tu domicilio u obra. Para accesos restringidos coordinamos el horario y la forma de "
     "descarga. El costo de entrega va en la cotización según la distancia."),
    ("¿Se puede usar tierra negra para macetas y jardineras?",
     "Sí, mezclada con perlita o arena gruesa en proporción 70/30: la tierra negra pura en maceta se compacta con el "
     "riego frecuente y se encharca. La mezcla aporta los nutrientes de la tierra negra y el drenaje de la perlita."),
    ("¿Dan factura CFDI por la tierra negra?",
     f"Sí. Emitimos factura {datos.FACTURA}, sobre todo en proyectos comerciales, fraccionamientos y empresas. Pídela al "
     "cotizar con tu RFC y datos fiscales."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-tierra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Tierra negra vegetal <em>por costal o camión</em>",
        "lede": (f"En Viveros Terra la tierra negra vegetal cuesta {COSTAL} el costal y {M3} el m³ a granel; el camión "
                 "volteo se cotiza según el volumen y tu colonia. Para pasto, jardineras y siembra: recoges en el vivero "
                 "o te la llevamos en Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Tierra negra", "aviso": f"Precios {datos.ANIO}", "nombre": "Costal", "antes": "",
                     "monto": COSTAL, "unidad": "por costal",
                     "filas": (("Por m³ a granel", M3), ("Camión volteo", datos.SEGUN_COTIZACION)),
                     "nota": "La entrega se cotiza según tu colonia."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuánta necesitas</a>.',
        "foto": PORTADA_FOTO,
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Por qué el suelo de Tampico necesita tierra negra?",
        "parrafos": (
            ("El suelo natural de Tamaulipas es arcilloso y compacto: retiene agua de más en lluvias y se seca como "
             "piedra en la temporada seca. Las raíces no penetran, el pasto no arraiga y las plantas no crecen."),
            ("La tierra negra vegetal es un sustrato orgánico rico en humus, de materia vegetal descompuesta: airea el "
             "suelo, retiene humedad sin encharcar y aporta los nutrientes básicos que le faltan a la tierra de Tampico."),
        ),
        "puntos": ("Alta materia orgánica: nutrientes naturales", "Retiene humedad: menos riegos",
                   "Textura suelta: las raíces crecen sin obstáculos", "Por costal o en camión volteo"),
        "figuras": FIGURAS_QUE_ES,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta la tierra negra en Tampico?",
        "lede": f"Precios {datos.ANIO}. Lo que no tiene precio publicado se cotiza por escrito antes de que confirmes.",
        "caption": "Tierra negra vegetal por presentación",
        "filas": (
            {"nombre": "Costal de tierra negra", "detalle": "Recoger o a domicilio",
             "unidad": "costal", "precio": P["tierra_negra_costal"]},
            {"nombre": "Tierra negra preparada", "detalle": "Costal con hojarasca y abono, para macetas",
             "unidad": "costal", "precio": None},
            {"nombre": "A granel por m³", "detalle": "Entregada en tu domicilio", "unidad": "m³",
             "precio": P["tierra_negra_m3"]},
            {"nombre": "Camión volteo", "detalle": "8 m³ o más, por etapas y con factura", "unidad": "camión",
             "precio": None},
        ),
        "nota": "El costo de entrega se cotiza según tu colonia y el volumen.",
    },
    "usos": {"titulo": "¿Para qué usas la tierra negra?",
             "lede": "Cada uso tiene su capa y su cantidad de referencia.", "items": USOS},
    "calculadora": {"clave": "tierra-negra", "nombre": "tierra negra", "titulo": "¿Cuánta tierra negra necesitas?",
                    "lede": "Escribe el área y el grosor de la capa: te damos los m³, la presentación y los costales."},
    "entrega": mc.entrega("la tierra negra"),
    "galeria": {"titulo": "Así luce la tierra negra de Viveros Terra", "figuras": FIGURAS_GALERIA},
    "faq": {"titulo": "Todo sobre tierra negra en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales para tu jardín",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico")),
              "enlaces": (("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Plantas y palmas", "/plantas-palmas-arboles-tampico"),
                          ("Arma tu lista de plantas", "/catalogo"), ("Guía de jardines", "/blog/diseno-jardines-tampico-guia"))},
    "cierre": {"titulo": "Cotiza tu tierra negra",
               "lede": "Dinos la cantidad y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/camion-tierra-negra-entrega-tampico.webp", "ancho": 1400, "alto": 933}},
    "pedido": mc.pedido("Ejemplo: 3 m³ de tierra negra, entrega en Ciudad Madero"),
    "jsonld": {
        "producto": mc.producto(
            "Tierra Negra Vegetal en Tampico",
            ("Tierra negra vegetal orgánica para jardines, pasto en rollo y plantas en Tampico. Venta por costal, por m³ y "
             "en camión volteo con entrega a domicilio en Ciudad Madero y Altamira."),
            f"{SITE}/img/camion-tierra-negra-entrega-tampico.jpg",
            ofertas=(mc.oferta(f"{URL}#precio", "costal", precio=P["tierra_negra_costal"]),
                     mc.oferta(f"{URL}#precio", "m³", precio=P["tierra_negra_m3"]))),
        "negocio": mc.NEGOCIO,
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {
        "description": (DESCRIPCION, "Sin la tierra preparada a $100 ni el camión desde $5,000 (no están en datos.py) y "
                                     "sin “gratis” (regla del dueño)."),
        "og:description": (DESCRIPCION_OG, "Sin la tierra preparada a $100 ni el camión desde $5,000 (no están en "
                                           "datos.py) y sin “gratis” (regla del dueño)."),
    },
    "reemplazos": {
        "Elige el formato para tu proyecto": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Costales de tierra negra": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Tierra Negra Preparada": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Por m³": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Camión volteo": "¿Cuánto cuesta la tierra negra en Tampico?",
        "¿Cuánta tierra negra necesito para preparar mi jardín?": "¿Cuánta tierra negra necesito para mi jardín?",
        "¿Entregan tierra negra a domicilio en Tampico?": "¿Entregan tierra negra a domicilio en toda la zona de Tampico?",
    },
    "retirados": {
        "Lo que dicen nuestros clientes": mc.MOTIVO_TESTIMONIOS,
        "$100": mc.MOTIVO_PRECIO,
        "$3,500": mc.MOTIVO_PRECIO,
        "$5,000": mc.MOTIVO_PRECIO,
        "$5,200": mc.MOTIVO_PRECIO,
        "$8,000": mc.MOTIVO_PRECIO,
    },
    "jsonld": {"LocalBusiness": mc.MOTIVO_LOCALBUSINESS,
               "AggregateOffer": ("Pasa a dos Offer con su UnitPriceSpecification (costal $90 y m³ $1,500, de "
                                  "datos.py): cada precio con su unidad, en vez de un rango sin unidad.")},
    # Cifras que main publicaba y no salen (paridad.py no las captura: se declaran aquí).
    "cifras": {"Costal ≈ 20 kg / Costales de 30–40 kg": mc.MOTIVO_PESO_COSTAL},
}
