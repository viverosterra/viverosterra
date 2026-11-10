"""Contenido de /tezontle-rojo-tampico (tezontle rojo por costal, m³ o camión de 14 m³). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularTezontle) como función pura.

Precio de datos.PRECIOS: costal desde $200 (como en la home). El m³ ($3,200) y el camión de 14 m³ no están en datos.py:
"según cotización" (el dueño lo confirmó el 2026-11-08). La comparativa lleva el mármol a $250 el saco de datos.py
(main decía $350 aquí y $250 en la página del mármol) y la piedra de río a granel, sin medidas ni el $280. Sin “+300
jardines”, “3–5 años sin reposición”, “90% de la maleza”, “del 60% al 95%”, “imbatible” ni “gratis”. Sin foto de
portada (main no la tenía); sus 4 fotos, en su orden. Meta como estaba publicada. El peso del costal no se publica:
main decía “15 kg” y “de 25 a 30 kg” y el dueño no lo tiene (PARIDAD["cifras"]). Sin mínimo de compra, entrega por
viaje y factura en todo (datos.CONDICIONES_MATERIALES).
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/tezontle-rojo-tampico"
URL = f"{SITE}{RUTA}"
COSTAL = dinero(P["tezontle_costal"])
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Tezontle rojo")

TITULO = f"Tezontle Rojo en Tampico: Costal desde {COSTAL} | Viveros Terra"
DESCRIPCION = (f"Tezontle rojo en Tampico para decorar y controlar la maleza: costal desde {COSTAL}; m³ y camión "
               f"{SEGUN.lower()}. Entrega en Madero y Altamira. Pide el tuyo.")
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
        ("og:image", f"{SITE}/img/tezontle-rojo-jardin-tampico-sendero.webp"),
        ("og:locale", "es_MX"),
        ("og:site_name", datos.NOMBRE),
    ),
    # Twitter Card con el mismo título y la misma descripción (SEO fase 0, 2026-11-10).
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", TITULO),
        ("twitter:description", DESCRIPCION),
        ("twitter:image", f"{SITE}/img/tezontle-rojo-jardin-tampico-sendero.webp"),
    ),
}
FIGURAS = (
    {"src": "/img/tezontle-rojo-jardin-tampico-sendero.webp", "ancho": 194, "alto": 259, "numero": 1,
     "alt": "Jardín residencial con tezontle rojo y pasto en Tampico", "lugar": "Tezontle y pasto", "etapa": "Jardín"},
    {"src": "/img/tezontle-rojo-jardin-lateral-tampico.webp", "ancho": 259, "alto": 194, "numero": 2,
     "alt": "Sendero lateral de tezontle rojo en un jardín de Tampico", "lugar": "Sendero lateral", "etapa": "Jardín"},
    {"src": "/img/tezontle-rojo-bordillo-jardin-tampico.webp", "ancho": 259, "alto": 195, "numero": 3,
     "alt": "Tezontle rojo con bordillo decorativo en un jardín residencial de Tampico", "lugar": "Con bordillo",
     "etapa": "Arriate"},
)
USOS = (
    {"titulo": "Control de maleza", "texto": (f"Capa de {mc.TEZONTLE_CAPA_MALEZA} sobre membrana antigerminante: ayuda "
                                               "a controlar la maleza sin herbicidas."),
     "puntos": (f"{mc.TEZONTLE_CAPA_MALEZA} de capa",)},
    {"titulo": "Senderos y caminos", "texto": "Caminos decorativos dentro del jardín: permeables, firmes y de aspecto "
     "tropical.", "puntos": ("8 a 10 cm compactado",)},
    {"titulo": "Arriates de plantas", "texto": "Cubierta roja alrededor de arbustos y plantas ornamentales: contrasta con "
     "el verde.", "puntos": ("5 a 6 cm de capa",)},
    {"titulo": "Cajetes de árboles y palmas", "texto": "Protege las raíces superficiales, conserva la humedad y da un "
     "acabado cuidado alrededor del tronco.", "puntos": ("5 a 8 cm, 50 cm de radio",)},
    {"titulo": "Drenaje en suelo arcilloso", "texto": "Mezclado con la tierra de relleno mejora el drenaje en jardines con "
     "suelo compacto y ayuda contra los encharcamientos.", "puntos": ("Mezcla 50/50 con tierra",)},
    {"titulo": "Terrazas y azoteas", "texto": "Cubierta sobre membrana impermeable: jardín seco de bajo mantenimiento "
     "para azoteas en Tampico.", "puntos": ("6 a 8 cm sobre membrana",)},
    {"titulo": "Macetas y jardineras", "texto": "Capa superior decorativa en macetones: reduce la evaporación y evita "
     "salpicaduras al regar.", "puntos": ("3 a 4 cm en superficie",)},
    {"titulo": "Proyectos de paisajismo", "texto": "Hoteles, fraccionamientos y empresas lo usan en áreas verdes de bajo "
     "mantenimiento, por camión volteo.", "puntos": ("Camión volteo 14 m³",)},
)
COMBINACIONES = (
    {"titulo": "Tezontle + Pasto verde", "texto": ("El contraste clásico en Tampico: el rojo del tezontle y el verde del "
     'San Agustín. <a href="/pasto-en-rollo-tampico">Pasto en rollo en Tampico</a>.')},
    {"titulo": "Tezontle + Mármol blanco", "texto": ("Mármol blanco en arriates y tezontle en senderos: un jardín "
     'contemporáneo para residencias y corporativos. <a href="/marmol-blanco-tampico">Mármol blanco para jardín</a>.')},
    {"titulo": "Tezontle + Palmas tropicales", "texto": ("Alrededor de palmas y árboles protege las raíces y conserva la "
     'humedad. <a href="/palmas-tropicales-tampico">Palmas en Tampico</a>.')},
    {"titulo": "Tezontle + Tierra negra", "texto": ("Primero se prepara el terreno con tierra negra y después va el "
     'tezontle encima, para jardines nuevos. <a href="/tierra-negra-vegetal-tampico">Tierra negra en Tampico</a>.')},
    {"titulo": "Tezontle + Piedra bola de río", "texto": ("Para jardines zen o de estilo japonés: el tezontle de relleno y "
     'la piedra bola de borde. <a href="/piedra-bola-rio-tampico">Piedra bola de río</a>.')},
    {"titulo": "Tezontle + Riego automático", "texto": ("El goteo bajo el tezontle queda oculto y el tezontle retiene la "
     'humedad en la temporada seca. <a href="/sistema-riego-tampico">Sistema de riego en Tampico</a>.')},
)
PASOS = (
    {"titulo": "Limpia el área", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira la maleza con todo y raíz y nivela el suelo si hace falta."},
    {"titulo": "Coloca la membrana", "quien": "tu", "cuando": "Paso 2",
     "texto": "Membrana antigerminante sin huecos, con los bordes fijos con piedras o grapas."},
    {"titulo": "Vierte el tezontle", "quien": "tu", "cuando": "Paso 3",
     "texto": "Distribúyelo con rastrillo hasta el grosor que elegiste (5 a 10 cm)."},
    {"titulo": "Define los bordes", "quien": "tu", "cuando": "Paso 4",
     "texto": "Bordillo de piedra, ladrillo o metal para contener el tezontle y separar zonas."},
)
PREGUNTAS = (
    ("¿Cuánto cuesta el tezontle rojo por camión en Tampico?",
     f"El costal de tezontle rojo cuesta desde {COSTAL}. El m³ suelto y el camión volteo de 14 m³ se cotizan según el "
     "volumen y la distancia de entrega: escríbenos tu colonia y la cantidad y te mandamos el precio por escrito antes "
     "de que confirmes."),
    ("¿Para qué sirve el tezontle en un jardín?",
     "Para ayudar a controlar la maleza sin herbicidas, hacer senderos y caminos decorativos, cubrir arriates, mejorar el "
     "drenaje en suelos arcillosos y como acabado decorativo que contrasta con el verde del pasto y las plantas."),
    ("¿Cuántos centímetros de tezontle se ponen?",
     f"De {mc.TEZONTLE_CAPA_MALEZA} para control de maleza y de 5 a 6 cm en arriates; de 8 a 10 cm compactados para "
     "senderos; de 3 a 4 cm como capa en macetas y jardineras. Sobre membrana antigerminante funciona mejor contra la "
     "maleza."),
    ("¿Cuánto dura el tezontle en un jardín?",
     "Es roca volcánica: no se desintegra ni se va con las lluvias de Tampico. Solo requiere rastrillarlo de vez en "
     "cuando para renivelarlo si se desplaza."),
    ("¿El tezontle daña a las plantas?",
     "No: bien colocado conserva la humedad del suelo, baja la temperatura de la tierra en días de calor y protege las "
     "raíces superficiales. Deja de 5 a 10 cm libres alrededor del tallo de las plantas sensibles."),
    ("¿Cuánta cantidad necesito para 50 m²?",
     f"Para 50 m² con capa de 8 cm necesitas {ejemplo('tezontle', 50, 0.08)}; con 6 cm, "
     f"{ejemplo('tezontle', 50, 0.06)}; con 10 cm para sendero, {ejemplo('tezontle', 50, 0.10)}. La fórmula: m² × "
     "grosor en metros = m³. Usa la calculadora de esta página o mándanos tus medidas."),
    ("¿Entregan tezontle a domicilio en Tampico y Altamira?",
     f"Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y en {datos.ZONAS_POR_PROYECTO} por proyecto: por costal en "
     "vehículo de reparto para cantidades chicas y en camión volteo de 14 m³ para proyectos grandes. El costo de entrega "
     "va en la cotización según tu dirección."),
    ("¿Es necesaria la membrana antigerminante con el tezontle?",
     "Para control de maleza, sí: sin membrana el tezontle ayuda, pero las semillas que caen desde arriba pueden germinar "
     "entre las piedras. Para uso decorativo o senderos de mucho tránsito no es indispensable. Te orientamos sobre la "
     "membrana para tu proyecto."),
    mc.pregunta_condiciones("tezontle"),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-tezontle",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "dato": f"Factura {datos.FACTURA}",
        "enlaces": (("Calcula cuánto necesitas", "#calculadora", "material:calculadora"),),
        "h1": 'Tezontle rojo en Tampico <span class="vt-serif">por costal, m³ o camión</span>',
        "lede": (f"El tezontle rojo cuesta desde {COSTAL} el costal; el m³ y el camión de 14 m³ se cotizan según el volumen y "
                 "tu colonia."),
        "etiqueta": {"codigo": "Tezontle rojo", "aviso": f"Precios {datos.ANIO}", "nombre": "Costal", "antes": "desde",
                     "monto": COSTAL, "unidad": "por costal",
                     "filas": (("Por m³", SEGUN), ("Camión volteo 14 m³", SEGUN)),
                     "nota": f"Factura {datos.FACTURA}. La entrega se cotiza según tu colonia."},
        "mensaje": MENSAJE,
    },
    "que_es": {
        "titulo": "¿Por qué el tezontle funciona tan bien en Tampico?",
        "subtitulo": "Tezontle rojo para senderos, bordillos y arriates",
        "parrafos": (
            ("El tezontle rojo es una roca volcánica porosa del centro de México que se usa en los jardines de Tampico "
             "para contrastar con el verde del pasto. Aguanta la intemperie y deja drenar el agua."),
            ("Sus pequeñas cavidades dejan pasar el agua pero no la luz, y eso frena a las semillas de maleza. Con el calor "
             "de Tampico, que reseca otros materiales, y las lluvias de temporada, que arrastran los sustratos finos, el "
             "tezontle no se degrada ni se va."),
        ),
        "puntos": ("Ayuda contra la maleza: tapa la luz al suelo", "Mejora el drenaje: es poroso",
                   "Conserva su color con sol y lluvia", "Acolchado: conserva la humedad del suelo"),
        "figuras": FIGURAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "lede": (f"Precios {datos.ANIO}, con IVA. El m³ y el camión se cotizan por escrito antes de que confirmes."),
        "caption": "Tezontle rojo por presentación",
        "filas": (
            {"nombre": "Por costal", "detalle": "Recoger o a domicilio", "unidad": "costal",
             "precio": P["tezontle_costal"], "desde": True},
            {"nombre": "Por m³ suelto", "detalle": "Entregado en tu domicilio", "unidad": "m³",
             "precio": None},
            {"nombre": "Camión volteo de 14 m³", "detalle": "Descarga en tu domicilio u obra, con factura",
             "unidad": "camión", "precio": None},
        ),
        "nota": datos.CONDICIONES_MATERIALES,
        "tablas": ({
            "titulo": "Tezontle, mármol blanco o piedra de río",
            "caption": "Tres materiales decorativos para senderos, bordes y arriates",
            "columnas": ("Característica", "Tezontle rojo", "Mármol blanco", "Piedra de río"),
            "filas": (("Color", "Rojo terracota", "Blanco", "Gris o beige natural"),
                      ("Origen", "Roca volcánica", "Mármol triturado", "Piedra de río"),
                      ("Tamaño o venta", mc.TEZONTLE_MEDIDA, mc.MARMOL_MEDIDA, mc.PIEDRA_BOLA_VENTA.capitalize()),
                      ("Drenaje", "Excelente (poroso)", "Bueno", "Excelente"),
                      ("Estilo", "Rústico, mexicano", "Minimalista", "Natural, zen"),
                      ("Precio por costal o saco", f"desde {COSTAL}", f"{dinero(P['marmol_saco'])} el saco", SEGUN),
                      ("Mejor uso", "Bordes y arriates", "Senderos formales", "Estanques y decoración")),
        },),
    },
    "usos": {"titulo": "¿Para qué quieres el tezontle?",
             "lede": "Cada uso tiene su capa y su cantidad de referencia.", "items": USOS},
    "calculadora": {"clave": "tezontle", "nombre": "tezontle", "titulo": "¿Cuánto tezontle necesitas?",
                    "lede": "Escribe el área y para qué lo usas: te damos los m³, la presentación y los costales."},
    "entrega": mc.entrega("el tezontle"),
    "combinaciones": {"titulo": "El tezontle combina perfectamente con...", "items": COMBINACIONES},
    "instalacion": {"titulo": "Cómo instalar tezontle en 4 pasos", "pasos": PASOS},
    "faq": {"titulo": "Todo sobre tezontle en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales para tu jardín",
              "items": mc.otros(RUTA, ("/tierra-negra-vegetal-tampico", "/marmol-blanco-tampico",
                                       "/piedra-bola-rio-tampico")),
              "enlaces": (("Pasto en rollo en Tampico", "/pasto-en-rollo-tampico"), ("Plantas y palmas", "/plantas-palmas-arboles-tampico"),
                          ("Arma tu lista de plantas", "/catalogo"), ("Guía del tezontle", "/blog/tezontle-usos-jardin-tampico"))},
    "cierre": {"titulo": "Cotiza tu tezontle rojo",
               "lede": "Dinos la cantidad y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/tezontle-rojo-bordillo-jardin-tampico.webp", "ancho": 259, "alto": 195}},
    "pedido": mc.pedido("Ejemplo: 4 m³ de tezontle rojo, entrega en Altamira"),
    "jsonld": {
        "producto": mc.producto(
            "Tezontle Rojo Decorativo para Jardín Tampico",
            (f"Tezontle rojo volcánico decorativo para jardines en Tampico. Costal desde {COSTAL}. Uso en senderos, "
             "bordes, arriates y macetas. Entrega a domicilio en Tampico, Madero y Altamira."),
            f"{SITE}/img/tezontle-rojo-jardin-tampico-sendero.jpg", sku="VT-TEZ-001",
            ofertas=(mc.oferta(f"{URL}#solicitar-pedido", "costal", desde=P["tezontle_costal"], agregada=True),)),
        "negocio": mc.NEGOCIO,
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION, {
        "og:description": (DESCRIPCION, "Sin “El rojo perfecto para tu jardín”: superlativo sin respaldo (revisión "
                                           "2f); el resto queda igual."),
    }),
    "reemplazos": {
        # Reescritura 16 (Entrega B de experiencia): el formulario pide una cotización, no un pedido en firme.
        "Escríbenos para cotizar": "¿Prefieres correo? Pide tu cotización aquí",
        # H1 con «en Tampico» (SEO fase 0, 2026-11-10): la consulta es «tezontle rojo Tampico».
        "Tezontle rojo por costal, m³ o camión": "Tezontle rojo en Tampico por costal, m³ o camión",
        "Elige el formato para tu proyecto": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Por costal": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Por m³ suelto": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "Camión 14 m³": "¿Cuánto cuesta el tezontle rojo en Tampico?",
        "¿Para qué sirve el tezontle en jardinería?": "¿Para qué sirve el tezontle en un jardín?",
        "¿Cuántos centímetros de tezontle se ponen en un jardín?": "¿Cuántos centímetros de tezontle se ponen?",
        "¿El tezontle dura mucho tiempo en el jardín?": "¿Cuánto dura el tezontle en un jardín?",
    },
    "retirados": {
        "Viveros Terra · Tampico": mc.MOTIVO_AUTOR,
        "$280": mc.MOTIVO_PRECIO,
        "$3,200": mc.MOTIVO_PRECIO,
        "$350": ("Era el mármol a $350 en la comparativa; el dueño confirmó $250 el saco (datos.py) y la comparativa "
                 "usa ese."),
    },
    "jsonld": {"Offer": mc.MOTIVO_OFERTA_DESDE},
    # Cifras que main publicaba y no salen (paridad.py no las captura: se declaran aquí).
    "cifras": {"Costal de 15 kg / Costal de 25–30 kg": mc.MOTIVO_PESO_COSTAL},
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). El lema del <h1> va en <span class="vt-serif"> (antes <em>). Entrada recortada: los usos (drenaje, senderos, control de maleza) siguen en «Usos». Sin foto: no se agrega ninguna.')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: con un resultado válido, la barra fija y el «Cotizar» del encabezado llevan el enlace de la calculadora y un texto corto; al borrarlo vuelven al genérico; aviso de área inválida; formulario de correo «Pedir cotización por correo».'
