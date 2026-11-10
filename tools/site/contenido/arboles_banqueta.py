"""Contenido de /arboles-para-banqueta-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Las seis especies de banqueta de main, en su orden y con la foto del catálogo (decisión del dueño, 2026-11-08: las
fotos quedan como están), servida en local. Sin precio propio (datos.DESDE_PLANTAS: según cotización): se
retiran olivo negro $600, polyalthia $400, neem y crespón $350 (sin confirmar; pregunta 1 al dueño) y la "asesoría de
plantación incluida". Título, descripción y Open Graph como estaban (Etapa 3).
"""
import datos
import mensajes_paginas
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc
from contenido import seo

SITE = datos.SITIO
RUTA = "/arboles-para-banqueta-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Árboles para banqueta"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
TITULO = "Árboles para Banqueta en Tampico y Madero | Viveros Terra"
DESCRIPCION = ("Árboles para banqueta que no levantan el concreto ni dañan tuberías: olivo negro, polyalthia, neem, fresno y "
               "crespón. Entrega y siembra en Tampico.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("olivo-negro", "El árbol de banqueta más recomendado en Tampico: raíz profunda, copa amplia y aguanta el salitre.",
     None),
    ("polyalthia", "Columnar: crece hacia arriba sin invadir a los lados; para banquetas angostas y avenidas.", None),
    ("neem", "Crece rápido, con follaje denso; muy resistente al calor y la sequía.", None),
    ("fresno", "Follaje frondoso para sombra; muy usado en banquetas y camellones.", None),
    ("crespon-astronomica", "El más colorido para avenidas: sus racimos cubren la copa en verano; con poda correcta no "
     "daña la banqueta.", None),
    ("tronadora", "Flores amarillas de trompeta casi todo el año; aguanta el calor. Para camellones y banquetas.", None),
)
PREGUNTAS = (
    ("¿Qué árboles son seguros para banquetas en Tampico?",
     "Los árboles más seguros para banquetas en Tampico son: Olivo Negro (el más recomendado), Polyalthia (columnar para "
     "espacios estrechos), Neem (rápido y profundo), Fresno y Crespón Astronómica (florido). Todos tienen raíz profunda "
     "que no levanta concreto ni daña tuberías."),
    ("¿Qué árbol de banqueta da más sombra en Tampico?",
     "El Olivo Negro da la mayor sombra para banquetas en Tampico con copa amplia de hasta 10 metros. Le siguen el Fresno "
     "y el Neem. Para espacios angostos el Polyalthia es columnar y no invade espacio lateral."),
    ("¿Qué árbol florido es bueno para banqueta en Tampico?",
     "El Crespón Astronómica es el árbol florido más recomendado para banquetas en Tampico. Sus flores en rosa, lila o "
     "blanco son espectaculares en verano. La Tronadora es buena opción para camellones con flores amarillas casi todo "
     "el año."),
    ("¿Los árboles de vivero ya están adaptados para banqueta?",
     "En Viveros Terra los árboles para banqueta tienen raíz cultivada en contenedor, lo que facilita la adaptación al "
     "trasplante. Recomendamos plantar en temporada de lluvias (junio-septiembre) y al entregar te decimos cómo "
     "plantarlo y regarlo."),
    ("¿Cuánto cuesta un árbol para banqueta en Tampico?",
     "Depende de la especie y del tamaño del ejemplar: mándanos el ancho de la banqueta y cuántos árboles necesitas y te "
     "cotizamos. Para desarrollos o avenidas cotizamos por volumen."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "cta_texto": "Cotizar mis árboles",  # Entrega B de experiencia: filas de WhatsApp tras las especies, los precios y las preguntas
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "pos": "70% 42%",
        "dato": 'Garantía de 30 días en lo que sembramos, <a href="/politicas#garantia-plantas">con condiciones</a>',
        "enlaces": ((f'Ver los {cd.cuenta({"uso": ["banqueta"]})} árboles de banqueta', "/catalogo?uso=banqueta", "plantas:catalogo"),),
        "lema": "De raíz profunda, para frentes y camellones.",
        "h1": "Árboles para banqueta que no levantan el pavimento",
        "lede": "Olivo negro, neem, fresno, encino y más. Te los llevamos y los sembramos.",
        "etiqueta": {"codigo": "Banqueta", "aviso": f"Precios {datos.ANIO}", "nombre": "Árboles para banqueta",
                     "antes": "Precio", "monto": "Por tamaño", "unidad": datos.SEGUN_COTIZACION.lower(),
                     "nota": "Cotiza con la medida de tu banqueta."},
        "mensaje": MENSAJE,
        "foto": {"src": "/img/portadas/arboles-vivero-tampico-mayoreo-sm.webp",
                 "srcset": ("/img/portadas/arboles-vivero-tampico-mayoreo-sm.webp 560w, "
                            "/img/portadas/arboles-vivero-tampico-mayoreo.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Árboles jóvenes en el vivero listos para sembrar en banqueta",
                 "lugar": "Árboles jóvenes en el vivero", "etapa": "Cd. Madero"},
    },
    "especies": {"titulo": "Las más solicitadas en Tampico", "lede": pc.LEDE_FOTOS, "items": ESPECIES},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Árboles para banqueta en Tampico: lo que más nos preguntan", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de árboles", "items": (
        ("7 árboles para banqueta que no levantan el pavimento", "/blog/arboles-para-sembrar-en-banqueta"),
        ("Poda de árboles y palmas", "/blog/poda-arboles-palmas-tampico-guia"),
        ("Cómo plantar una palma o un árbol", "/blog/como-plantar-palma-arbol-paso-a-paso-tampico"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": pc.otras_subcategorias(RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos el ancho de la banqueta, cuántos árboles y la colonia; te respondemos con precio.",
               "mensaje": MENSAJE},
    "jsonld": {"migas": pc.migas_ld(NOMBRE, RUTA), "nodos": (pc.lista_ld(NOMBRE, [s for s, _t, _a in ESPECIES]),),
               "speakable": (".vt-portada .vt-lede", ".vt-faq details:first-child p")},
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION),
    "jsonld": {
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "Árboles para banqueta tampico — Todo lo que necesitas saber": (
            "Árboles para banqueta en Tampico: lo que más nos preguntan"),
    },
    "retirados": {
        "$350": "Neem y crespón desde $350: precios sin confirmar por el dueño (pregunta 1); van según cotización.",
        "$400,": "Polyalthia desde $400: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
        "$600,": "Olivo negro desde $600: precio sin confirmar por el dueño (pregunta 1); va según cotización.",
    },
    "especies": {
        "reemplazos": {},
        "retirados": {},
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Lema nuevo: «De raíz profunda, para frentes y camellones.» (de la entrada); la garantía de 30 días va en la línea de confianza, con sus condiciones.')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: filas de WhatsApp («Cotizar mis árboles») tras el filtro por necesidad, las subcategorías, las especies (la rejilla larga se parte con una en medio), los precios y las preguntas, con la prueba social (cifras de datos.py y la calificación de Google con su enlace) y la garantía de las plantas que sembramos junto a la primera. Encabezados, precios y enlaces sin cambios.'
