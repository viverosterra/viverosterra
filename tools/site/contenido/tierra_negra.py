"""Contenido de /tierra-negra-vegetal-tampico (tierra negra vegetal por costal, m³ o camión). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularTierra) como función pura.

Precios de datos.PRECIOS (dueño, 2026-11-08): costal $90, tierra preparada $100, m³ $1,500 y camiones de 5, 8 y 14 m³ a
$3,500, $5,200 y $8,000 (la tabla de camiones; nunca el "camión desde $5,000" de main, que no confirmó). Las 8 fotos de
main, en su orden. Sin “Entrega inmediata”, “+500 jardines”, “40% más rápido” ni “gratis”; las opiniones de Ricardo O.
y Laura P. vuelven textuales (reales y con permiso: datos.OPINIONES_TIERRA_NEGRA), sin calificación en el JSON-LD.
Sin mínimo de compra, entrega por viaje y factura en todo (datos.CONDICIONES_MATERIALES). Título, robots y canonical
como estaban; la descripción y el Open Graph pierden el camión "desde $5,000" y el “gratis” (PARIDAD["meta"]). El peso
del costal no se publica: main decía “≈ 20 kg” y “de 30 a 40 kg” y el dueño no lo tiene (PARIDAD["cifras"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/tierra-negra-vegetal-tampico"
URL = f"{SITE}{RUTA}"
COSTAL, M3 = dinero(P["tierra_negra_costal"]), dinero(P["tierra_negra_m3"])
PREPARADA = dinero(P["tierra_preparada_costal"])
CAMIONES = datos.TIERRA_CAMIONES
CAMIONES_TEXTO = ", ".join(f"{m3} m³ a {dinero(precio)}" for m3, precio in CAMIONES[:-1]) + \
    f" y {CAMIONES[-1][0]} m³ a {dinero(CAMIONES[-1][1])}"
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Tierra negra vegetal")
TITULO = f"Tierra Negra en Tampico: Costal {COSTAL} y Camión | Viveros Terra"
DESCRIPCION = (f"Tierra negra vegetal en Tampico: costal {COSTAL}, preparada {PREPARADA}, m³ {M3} y camión de {CAMIONES[0][0]} m³ "
               f"{dinero(CAMIONES[0][1])}. Entrega a domicilio en Madero y Altamira. Pide hoy.")

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
        ("og:image", f"{SITE}/img/camion-tierra-negra-entrega-tampico.webp"),
        ("og:locale", "es_MX"),
        ("og:site_name", datos.NOMBRE),
    ),
    # Twitter Card con el mismo título y la misma descripción (SEO fase 0, 2026-11-10).
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", TITULO),
        ("twitter:description", DESCRIPCION),
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
     "puntos": (f"Camiones de {CAMIONES_TEXTO}",)},
    {"titulo": "Macetas y jardineras grandes",
     "texto": ("Sustrato base para macetones y jardineras: se mezcla con perlita o arena gruesa 70/30 para que drene y no "
               "se encharque."),
     "puntos": ("Por costal",)},
    {"titulo": "Proyectos comerciales e industriales",
     "texto": ("Áreas verdes en fraccionamientos, condominios, parques industriales y escuelas: camiones coordinados por "
               f"etapas con factura {datos.FACTURA}."),
     "puntos": ("Por camión de 5, 8 o 14 m³",)},
)

PREGUNTAS = (
    ("¿Cuánto cuesta un camión de tierra negra en Tampico?",
     f"El camión volteo de tierra negra cuesta según su tamaño: {CAMIONES_TEXTO}. {datos.ENTREGA_COBRO} A granel por m³ "
     f"cuesta {M3}; el costal, {COSTAL}, y la tierra preparada, {PREPARADA} el costal. Escríbenos tu colonia y la "
     "cantidad y te mandamos el total por escrito antes de que confirmes."),
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
    mc.pregunta_condiciones("tierra negra", "¿Dan factura CFDI por la tierra negra?"),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-tierra",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "pos_d": "88% 50%",
        "pos": "50% 55%",
        "dato": "La entrega se cotiza según tu colonia",
        "enlaces": (("Calcula cuánta necesitas", "#calculadora", "material:calculadora"),),
        "h1": 'Tierra negra en Tampico <span class="vt-serif">por costal, m³ o camión</span>',
        "lede": (f"La tierra negra vegetal cuesta {COSTAL} el costal y {M3} el m³ a granel. Recoges en el vivero o te la "
                 "llevamos."),
        "etiqueta": {"codigo": "Tierra negra", "aviso": f"Precios {datos.ANIO}", "nombre": "Costal", "antes": "",
                     "monto": COSTAL, "unidad": "por costal",
                     "filas": (("Por m³ a granel", M3), (f"Camión volteo {CAMIONES[0][0]} m³", dinero(CAMIONES[0][1]))),
                     "nota": "La entrega se cotiza según tu colonia."},
        "mensaje": MENSAJE,
        "foto": PORTADA_FOTO,
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
        "lede": f"Precios {datos.ANIO}, con IVA. {datos.SIN_MINIMO} Te mandamos el total por escrito antes de que confirmes.",
        "caption": "Tierra negra vegetal por presentación",
        "filas": (
            {"nombre": "Costal de tierra negra", "detalle": "Recoger o a domicilio",
             "unidad": "costal", "precio": P["tierra_negra_costal"]},
            {"nombre": "Tierra negra preparada", "detalle": "Costal con hojarasca y abono, para macetas",
             "unidad": "costal", "precio": P["tierra_preparada_costal"]},
            {"nombre": "A granel por m³", "detalle": "Entregada en tu domicilio", "unidad": "m³",
             "precio": P["tierra_negra_m3"]},
            *({"nombre": f"Camión volteo de {m3} m³", "detalle": "Descarga en tu domicilio u obra", "unidad": "camión",
               "precio": precio} for m3, precio in CAMIONES),
        ),
        "nota": f"{datos.ENTREGA_COBRO} {datos.FACTURACION}",
    },
    "usos": {"titulo": "¿Para qué usas la tierra negra?",
             "lede": "Cada uso tiene su capa y su cantidad de referencia.", "items": USOS},
    "calculadora": {"clave": "tierra-negra", "nombre": "tierra negra", "titulo": "¿Cuánta tierra negra necesitas?",
                    "lede": "Escribe el área y el grosor de la capa: te damos los m³, la presentación y los costales."},
    "entrega": mc.entrega("la tierra negra"),
    "galeria": {"titulo": "Así luce la tierra negra de Viveros Terra", "figuras": FIGURAS_GALERIA},
    "opiniones": {"titulo": "Lo que dicen nuestros clientes", "items": datos.OPINIONES_TIERRA_NEGRA},
    "faq": {"titulo": "Todo sobre tierra negra en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales para tu jardín",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico")),
              "enlaces": (("Pasto en rollo en Tampico", "/pasto-en-rollo-tampico"), ("Plantas y palmas", "/plantas-palmas-arboles-tampico"),
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
            ofertas=(mc.oferta(f"{URL}#precio", "costal", precio=P["tierra_negra_costal"], nombre="Costal de tierra negra"),
                     mc.oferta(f"{URL}#precio", "costal", precio=P["tierra_preparada_costal"],
                               nombre="Costal de tierra negra preparada"),
                     mc.oferta(f"{URL}#precio", "m³", precio=P["tierra_negra_m3"], nombre="Tierra negra a granel por m³"),
                     *(mc.oferta(f"{URL}#precio", "camión", precio=precio, nombre=f"Camión volteo de {m3} m³")
                       for m3, precio in CAMIONES))),
        "negocio": mc.NEGOCIO,
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION, {
        "description": (DESCRIPCION, "Sin el camión desde $5,000 (el dueño no lo confirmó: va el camión de 5 m³ de su "
                                     "tabla) y sin “gratis” (regla del dueño)."),
        "og:description": (DESCRIPCION, "Sin el camión desde $5,000 (el dueño no lo confirmó: va el camión de 5 m³ de "
                                           "su tabla) y sin “gratis” (regla del dueño)."),
    }),
    "reemplazos": {
        # Reescritura 16 (Entrega B de experiencia): el formulario pide una cotización, no un pedido en firme.
        "Escríbenos para cotizar": "¿Prefieres correo? Pide tu cotización aquí",
        # H1 con «en Tampico» (SEO fase 0, 2026-11-10): la consulta es «tierra negra Tampico».
        "Tierra negra vegetal por costal o camión": "Tierra negra en Tampico por costal, m³ o camión",
        "Elige el formato para tu proyecto": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Costales de tierra negra": "¿Cuánto cuesta la tierra negra en Tampico?",
        "Tierra Negra Preparada": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Por m³": "¿Cuánto cuesta la tierra negra en Tampico?",
        "A granel — Camión volteo": "¿Cuánto cuesta la tierra negra en Tampico?",
        "¿Cuánta tierra negra necesito para preparar mi jardín?": "¿Cuánta tierra negra necesito para mi jardín?",
        "¿Entregan tierra negra a domicilio en Tampico?": "¿Entregan tierra negra a domicilio en toda la zona de Tampico?",
    },
    "retirados": {
        "$5,000": ("El “camión desde $5,000” no lo confirmó el dueño (2026-11-08): va la tabla de camiones de 5, 8 y "
                   "14 m³ de datos.py."),
    },
    "jsonld": {"AggregateOffer": ("Pasa a un Offer por presentación con su UnitPriceSpecification (costal, preparada, "
                                  "m³ y los tres camiones, de datos.py): cada precio con su unidad, en vez de un rango "
                                  "sin unidad y sin InStock.")},
    # Cifras que main publicaba y no salen (paridad.py no las captura: se declaran aquí).
    "cifras": {"Costal ≈ 20 kg / Costales de 30–40 kg": mc.MOTIVO_PESO_COSTAL},
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). El lema del <h1> va en <span class="vt-serif"> (antes <em>: cursiva sintética). Entrada recortada: los precios del camión (5, 8 y 14 m³) salen del hero y siguen en la tabla de presentaciones; la foto apaisada se recorta a 4:5 en escritorio con su encuadre.')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: con un resultado válido, la barra fija y el «Cotizar» del encabezado llevan el enlace de la calculadora y un texto corto; al borrarlo vuelven al genérico; aviso de área inválida; mensaje del cálculo con costales o a granel y colonia (reescritura 15); formulario de correo «Pedir cotización por correo» (reescritura 16).'

# Lo que cambia por la Entrega C de experiencia (ritmo y movimiento).
PARIDAD["ritmo"] = 'Entrega C de experiencia (2026-11-10), ritmo y movimiento: filas de WhatsApp «Cotizar <material>» tras el precio y «Preguntar por WhatsApp» tras las preguntas (antes, 7.4 a 8.5 pantallas sin CTA); revelado por scroll de encabezados y figuras y balanceo de la etiqueta en escritorio.'
