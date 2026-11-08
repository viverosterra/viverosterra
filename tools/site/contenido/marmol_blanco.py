"""Contenido de /marmol-blanco-tampico (mármol blanco triturado por saco o por volumen). Solo datos: la plantilla es
tools/site/plantillas/material.py, con la calculadora de main (calcularMarmol) como función pura, sin su precio.

El saco a $250 (y el $750–$1,250 por m²) no está en datos.py: el precio va "según cotización" en la etiqueta, la tabla,
la calculadora, el JSON-LD (sin Offer) y el título (pregunta 1 al dueño). La comparativa pierde el tezontle a $120 (en
datos.py es desde $200) y los precios por m²; la FAQ ya no dice que el tezontle es "más barato" (el precio del
mármol no está en datos.py). Sin “Calidad importada”, “premium”, “hasta 8°C”, “cantidad sin límite”,
“el mejor” ni “gratis”. Las 8 fotos de main, en su orden (el alt del saco ya no dice $250). Título, descripción y Open
Graph sin el $250 ni el “gratis” (PARIDAD["meta"]); HowTo de los 4 pasos como estaba.
"""
import datos
import mensajes_paginas
from componentes import dinero
from componentes_materiales import ejemplo
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/marmol-blanco-tampico"
URL = f"{SITE}{RUTA}"
SEGUN = datos.SEGUN_COTIZACION
MENSAJE = mensajes_paginas.MATERIALES[RUTA]
MIGAS, MIGAS_LD = mc.migas(RUTA, "Mármol blanco")
TITULO = "Mármol Blanco para Jardín Tampico · Saco de 20 kg"
DESCRIPCION = ("Mármol blanco decorativo en Tampico. Saco ≈ 20 kg · 3 sacos = 1 m² · Entrega en Madero y Altamira. "
               "Senderos, albercas y arriates. Cotiza hoy.")
DESCRIPCION_OG = ("Piedra mármol blanca decorativa en Tampico. Saco ≈ 20 kg; 3 sacos = 1 m². Entrega a domicilio. "
                  "Cotiza por WhatsApp.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Mármol Blanco para Jardín Tampico · Viveros Terra"),
        ("og:description", DESCRIPCION_OG),
        ("og:image", f"{SITE}/img/marmol-blanco-alberca-palmera-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}
PORTADA_FOTO = {
    "src": "/img/portadas/marmol-blanco-alberca-palmera-tampico-sm.webp",
    "srcset": ("/img/portadas/marmol-blanco-alberca-palmera-tampico-sm.webp 560w, "
               "/img/portadas/marmol-blanco-alberca-palmera-tampico.webp 900w"),
    "sizes": "(min-width: 1024px) 540px, 100vw", "ancho": 900, "alto": 1200, "numero": 1,
    "alt": "Mármol blanco decorativo junto a una alberca con palmera", "lugar": "Mármol junto a la alberca",
    "etapa": "Tampico"}
FIGURAS = (
    {"src": "/img/marmol-blanco-alberca-palmera-tampico.webp", "ancho": 900, "alto": 1200, "numero": 2,
     "alt": "Mármol blanco decorativo alrededor de una alberca con palmera en Tampico", "lugar": "Borde de alberca",
     "etapa": "Con palmera"},
    {"src": "/img/marmol-blanco-arriate-suculentas-tampico.webp", "ancho": 1200, "alto": 1200, "numero": 3,
     "alt": "Mármol blanco como borde decorativo con suculentas en un jardín", "lugar": "Arriate", "etapa": "Suculentas"},
    {"src": "/img/marmol-blanco-maceta-decorativa-tampico.webp", "ancho": 1200, "alto": 1180, "numero": 4,
     "alt": "Mármol blanco en una maceta decorativa con suculenta", "lugar": "Maceta", "etapa": "Capa decorativa"},
)
FIGURA_SACO = {"src": "/img/marmol-blanco-saco-costal-tampico.webp", "ancho": 1024, "alto": 1536, "numero": 5,
               "alt": "Saco de red con unos 20 kg de mármol blanco", "lugar": "Saco de mármol blanco", "etapa": "≈ 20 kg"}
USOS = (
    {"titulo": "Senderos y caminos", "texto": "Caminos firmes y permeables dentro del jardín, con un brillo natural que se "
     "luce de noche con iluminación.", "puntos": ("4 a 5 sacos por m² (capa de 5 a 6 cm)",)},
    {"titulo": "Arriates de plantas", "texto": "Cubierta blanca alrededor de arbustos, helechos y plantas ornamentales: "
     "contrasta con el verde.", "puntos": ("3 sacos por m² (capa estándar)",)},
    {"titulo": "Borde y zona de alberca", "texto": "Alrededor de la alberca refleja la luz del agua y se siente fresco.",
     "puntos": ("3 a 4 sacos por m² (capa de 4 a 5 cm)",)},
    {"titulo": "Terrazas y azoteas", "texto": "Jardín seco de bajo mantenimiento para azoteas y terrazas, sobre membrana.",
     "puntos": ("3 sacos por m² (capa de 3 a 4 cm)",)},
    {"titulo": "Cajetes de palmas y árboles", "texto": "Cubierta alrededor del tronco de palmeras y árboles: protege las "
     "raíces y conserva la humedad.", "puntos": ("2 a 3 sacos por árbol (radio de 60 cm)",)},
    {"titulo": "Proyectos de paisajismo", "texto": "Hoteles, condominios, oficinas y fraccionamientos lo usan en áreas de "
     "imagen. Cotizamos por volumen.", "puntos": ("Por volumen, según cotización",)},
)
COMBINACIONES = (
    {"titulo": "Mármol + Pasto San Agustín", "texto": ("Un sendero de mármol blanco que atraviesa el pasto verde. "
     '<a href="/pasto-en-rollo-tampico">Pasto en rollo San Agustín</a>.')},
    {"titulo": "Mármol + Tezontle Rojo", "texto": ("Zonas blancas de mármol y zonas rojas de tezontle: diseños bicolor "
     'para paisajismo residencial y hotelero. <a href="/tezontle-rojo-tampico">Ver tezontle rojo</a>.')},
    {"titulo": "Mármol + palmas tropicales", "texto": ("Mármol blanco alrededor de palmas reales y árboles de ornato. "
     '<a href="/plantas-palmas-arboles-tampico">Ver plantas y palmas</a>.')},
    {"titulo": "Mármol + Tierra Negra", "texto": ("Primero se prepara el arriate con tierra negra para plantar y luego se "
     'cubre con mármol. <a href="/tierra-negra-vegetal-tampico">Ver tierra negra</a>.')},
    {"titulo": "Mármol + Riego automático", "texto": ("Goteo bajo el mármol, oculto: el mármol conserva la humedad y "
     'protege la manguera del sol. <a href="/sistema-riego-tampico">Ver sistema de riego</a>.')},
    {"titulo": "Mármol + Diseño de jardín", "texto": ("¿Un proyecto completo con pasto, plantas, mármol y riego? Planes "
     f'de diseño desde {dinero(P["diseno"])}. <a href="/diseno-jardines-tampico">Ver diseño de jardines</a>.')},
)
PASOS = (
    {"titulo": "Limpia el área", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira la maleza con raíz y nivela el suelo; si hay mucha irregularidad, agrega tierra para nivelar."},
    {"titulo": "Membrana antigerminante", "quien": "tu", "cuando": "Paso 2",
     "texto": "Coloca la membrana sin huecos y fija los bordes; en arriates, haz cortes en X donde van las plantas."},
    {"titulo": "Vierte el mármol", "quien": "tu", "cuando": "Paso 3",
     "texto": "Distribúyelo con rastrillo hasta el grosor que elegiste (3 a 6 cm según el uso)."},
    {"titulo": "Define los bordes", "quien": "tu", "cuando": "Paso 4",
     "texto": "Bordillo de piedra, metal o ladrillo para contener el mármol y dar un acabado limpio."},
)
PREGUNTAS = (
    ("¿Cuánto cuesta el mármol blanco para jardín en Tampico?",
     "El precio del saco de mármol blanco (unos 20 kg) y el de los pedidos por volumen se cotizan: escríbenos los m² y tu "
     "colonia y te mandamos el precio con la entrega, por escrito. Con 3 sacos se cubre 1 m² con capa de 3 a 4 cm; con "
     "capa de 5 a 6 cm, de 4 a 5 sacos por m²."),
    ("¿Cuántos sacos de mármol blanco necesito para 1 m²?",
     f"Para 1 m² con capa de 3 a 4 cm, {ejemplo('marmol', 1, 4)} (de unos 20 kg cada uno); para senderos o zonas de "
     "tránsito con capa de 5 a 6 cm, de 4 a 5 sacos por m². Regla rápida: tus m² por 3 dan el mínimo de sacos. La "
     "calculadora de esta página te da el número exacto."),
    ("¿Para qué sirve el mármol blanco en jardinería?",
     "Para senderos y caminos, arriates alrededor de plantas y arbustos, bordes de alberca, cubierta decorativa en "
     "terrazas y azoteas, cajetes alrededor de árboles y palmas y proyectos de paisajismo. Contrasta con la vegetación."),
    ("¿El mármol blanco se mancha o pierde su color con el tiempo?",
     "No pierde su color con el sol ni con las lluvias de Tampico. Con el tiempo junta polvo o tierra, que se quita con "
     "agua de la manguera; no necesita productos especiales ni selladores."),
    ("¿El mármol blanco controla la maleza?",
     "Sí, con membrana antigerminante debajo: la capa de 4 a 6 cm sobre la membrana tapa la luz que necesitan las "
     "semillas. Sin membrana ayuda, pero en el clima húmedo de Tampico no elimina toda la maleza."),
    ("¿Cuánto dura el mármol blanco instalado en un jardín?",
     "Es piedra natural: no se degrada. En senderos de mucho tránsito las piedras se dispersan; se resuelve con bordillos "
     "y rastrillado ocasional."),
    ("¿Entregan mármol blanco a domicilio en Tampico?",
     f"Sí, en Tampico, Ciudad Madero y Altamira. También puedes recogerlo en el vivero, {datos.CALLE}, Cd. Madero "
     f"({datos.REFERENCIA}). Para 20 sacos o más, coordinamos la entrega por WhatsApp o al {datos.TELEFONO_VISIBLE}."),
    ("¿Mármol blanco o tezontle rojo? ¿Cuál es mejor?",
     "Depende del objetivo. Mármol blanco para zona de alberca, terraza o un contraste luminoso con las plantas; "
     f"tezontle rojo (desde {dinero(P['tezontle_costal'])} el costal) si buscas más control de maleza por ser poroso o "
     "el contraste rojo y verde. "
     "Muchos jardines combinan los dos en zonas distintas."),
)

CONTENIDO = {
    "tipo": mc.TIPO,
    "prefijo": "vt-marmol",
    "meta": META,
    "migas": MIGAS,
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "h1": "Mármol blanco <em>para jardines y andadores</em>",
        "lede": ("Grava de mármol blanco triturado de 1 a 3 cm para arriates, andadores y bordes de alberca: 3 sacos de "
                 "unos 20 kg cubren 1 m². El precio por saco o por volumen se cotiza con la entrega a tu colonia en "
                 "Tampico, Madero y Altamira."),
        "etiqueta": {"codigo": "Mármol blanco", "aviso": "1 a 3 cm", "nombre": "Saco ≈ 20 kg", "antes": "cubren 1 m²",
                     "monto": "3 sacos", "unidad": "capa de 3 a 4 cm",
                     "filas": (("Precio por saco", SEGUN), ("20 sacos o más", "por volumen")),
                     "nota": "Te damos el precio por escrito con la entrega."},
        "mensaje": MENSAJE,
        "tambien": 'O <a href="#calculadora" data-cta="material:calculadora">calcula cuántos sacos necesitas</a>.',
        "foto": PORTADA_FOTO,
        "compacta": True,
    },
    "que_es": {
        "titulo": "¿Por qué el mármol blanco transforma cualquier jardín?",
        "subtitulo": "Mármol blanco triturado para senderos y bordes de jardín",
        "parrafos": (
            ("El mármol blanco triturado es piedra natural para senderos, bordes de arriate y caminerías: contrasta con "
             "el pasto San Agustín, refleja la luz y da sensación de amplitud. Tamaños de 1 a 3 cm, por saco o por "
             "volumen."),
            ("En el clima de Tampico no pierde su color con el sol ni con las lluvias de temporada y no necesita "
             "mantenimiento especial."),
        ),
        "puntos": ("Conserva su color con sol y lluvia", "Drenaje natural: deja pasar el agua",
                   "Contraste: blanco con verde", "Con membrana, ayuda contra la maleza"),
        "figuras": FIGURAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "lede": "Una sola presentación: el saco de red de unos 20 kg. Su precio y el de volumen te los damos por escrito.",
        "caption": "Mármol blanco por presentación",
        "figura": FIGURA_SACO,
        "filas": (
            {"nombre": "Saco de mármol blanco", "detalle": "Saco de red ≈ 20 kg, piedra lavada y calibrada · sin mínimo",
             "unidad": "saco", "precio": None},
            {"nombre": "1 m² con capa de 3 a 4 cm", "detalle": "3 sacos", "unidad": "m²", "precio": None},
            {"nombre": "Pedidos de 20 sacos o más", "detalle": "Se cotizan por volumen", "unidad": "volumen",
             "precio": None},
        ),
        "nota": "Recoges en el vivero o te lo llevamos; la entrega se cotiza según tu colonia.",
        "tablas": (
            {"titulo": "Guía rápida de sacos por uso", "caption": "Sacos por m² según el uso y la capa",
             "columnas": ("Uso", "Capa", "Sacos por m²"),
             "filas": (("Macetas o decorativo", "3 cm", "3 sacos"), ("Arriates (estándar)", "4 cm", "3 a 4 sacos"),
                       ("Alberca o terraza", "5 cm", "4 sacos"), ("Sendero transitado", "6 cm", "4 a 5 sacos"))},
            {"titulo": "Mármol blanco, tezontle o piedra bola", "caption": "¿Cuál elegir?",
             "columnas": ("Característica", "Mármol blanco", "Tezontle rojo", "Piedra bola"),
             "filas": (("Precio por saco o costal", SEGUN, f"desde {dinero(P['tezontle_costal'])}", SEGUN),
                       ("Estilo", "Luminoso", "Vibrante", "Natural"),
                       ("Control de maleza", "Con membrana", "Excelente", "Parcial"),
                       ("Mantenimiento", "Lavado ocasional", "Rastrillado", "Mínimo"),
                       ("Al sol de Tampico", "No se decolora", "No se decolora", "No se decolora"))},
        ),
    },
    "usos": {"titulo": "¿Dónde lo quieres instalar?",
             "lede": "Cada uso tiene su capa y sus sacos por m² de referencia.", "items": USOS},
    "calculadora": {"clave": "marmol", "nombre": "mármol blanco", "titulo": "¿Cuántos sacos necesitas?",
                    "lede": "Escribe el área y el grosor de la capa: te damos los sacos y el peso aproximado."},
    "entrega": mc.entrega("el mármol blanco"),
    "combinaciones": {"titulo": "El mármol blanco combina con todo", "items": COMBINACIONES},
    "instalacion": {"titulo": "Cómo instalar mármol blanco en 4 pasos", "pasos": PASOS,
                    "howto": "Cómo instalar mármol blanco en tu jardín",
                    "nota": "¿Prefieres que lo instalemos nosotros? Lo cotizamos junto con el material."},
    "faq": {"titulo": "Todo sobre mármol blanco en Tampico", "preguntas": PREGUNTAS},
    "otros": {"titulo": "Otros materiales decorativos",
              "items": mc.otros(RUTA, ("/tezontle-rojo-tampico", "/tierra-negra-vegetal-tampico",
                                       "/piedra-bola-rio-tampico"), con_miniatura=True),
              "enlaces": (("Arma tu lista de plantas", "/catalogo"),)},
    "cierre": {"titulo": "Cotiza tu mármol blanco",
               "lede": "Dinos los m² y tu colonia y te mandamos el precio con la entrega.",
               "fondo": {"src": "/img/jardin-residencial-pasto-san-agustin-tampico.webp", "ancho": 1280, "alto": 720}},
    "pedido": mc.pedido("Ejemplo: 36 sacos de mármol blanco, entrega en Tampico"),
    "jsonld": {
        "producto": mc.producto(
            "Mármol Blanco Decorativo para Jardín en Tampico",
            ("Piedra mármol blanca decorativa para jardines en Tampico. Saco de aproximadamente 20 kg; con 3 sacos se "
             "cubre 1 m² con capa estándar de 3 a 4 cm. Entrega a domicilio en Tampico, Ciudad Madero y Altamira."),
            f"{SITE}/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp"),
        "migas": MIGAS_LD,
        "speakable": mc.SPEAKABLE,
    },
}

PARIDAD = {
    "meta": {
        "title": (TITULO, "Sin el $250 por saco: no está en datos.py (regla del dueño); el resto del título queda igual."),
        "description": (DESCRIPCION, "Sin el $250 por saco: no está en datos.py (regla del dueño)."),
        "og:description": (DESCRIPCION_OG, "Sin el $250 por saco (no está en datos.py) y sin “gratis” (regla del dueño)."),
    },
    "reemplazos": {
        "Una sola presentación, precio claro": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "Saco de Mármol Blanco": "¿Cuánto cuesta el mármol blanco en Tampico?",
        "¿Para qué se usa el mármol blanco en jardinería?": "¿Para qué sirve el mármol blanco en jardinería?",
        "¿Cuánto dura el mármol blanco en el jardín?": "¿Cuánto dura el mármol blanco instalado en un jardín?",
    },
    "retirados": {
        "Viveros Terra · Tampico": mc.MOTIVO_AUTOR,
        "$0": "Era el estado vacío del “Total orientativo” de la calculadora, que ya no da precio (no está en datos.py).",
        "$250": mc.MOTIVO_PRECIO,
        "$750": mc.MOTIVO_PRECIO,
        "$1,250": mc.MOTIVO_PRECIO,
        "$120": "El tezontle a $120 contradecía datos.py (desde $200 el costal): la comparativa usa el de datos.py.",
        "$360": mc.MOTIVO_PRECIO,
        "$600": mc.MOTIVO_PRECIO,
    },
    "jsonld": {
        "Offer": ("El Offer publicaba el saco a $250, que no está en datos.py: el Product queda sin oferta hasta que el "
                  "dueño confirme el precio (pregunta 1)."),
        "LocalBusiness": mc.MOTIVO_LOCALBUSINESS,
    },
}
