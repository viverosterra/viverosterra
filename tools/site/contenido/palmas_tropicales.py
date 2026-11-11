"""Contenido de /palmas-tropicales-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Precio (decisión del dueño, 2026-11-07): datos.PALMAS_PRECIO (areca y coco plumoso desde $250, palma real desde $500 en
tamaño chico; el precio sube con la altura) y las demás palmas "según cotización", en la tabla de precios. Las tarjetas
son las de main, en su orden y con la misma foto (decisión del dueño, 2026-11-08), servida en local. Se agrega la kerpis, que el hub de main mandaba aquí. "Pregunta existencia"
sale de las respuestas (sin afirmaciones de disponibilidad). Título como estaba (Etapa 3); la descripción
suma «con condiciones» a la garantía (PARIDAD["meta"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
FOTO_LD = "/img/portadas/palma-real-jardin-residencial-tampico.webp"  # la foto de la portada (image del Product)
RUTA = "/palmas-tropicales-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Palmas tropicales"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
TITULO = f"Venta de Palmas en Tampico desde {dinero(P['palma_desde'])} | Viveros Terra"
DESCRIPCION = (f"Venta de palmas para jardín en Tampico: areca y coco plumoso desde {dinero(P['palma_desde'])}, palma real "
               f"desde {dinero(P['palma_real'])}. Entrega, siembra y garantía de 30 días con condiciones.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("palma-areca", "Para interiores y semisombra: tallos múltiples y follaje elegante para hoteles, "
     "oficinas y jardines residenciales.", None),
    ("coco-plumoso", "Tronco estilizado y follaje plumoso arqueado; aguanta el calor costero. Para entradas y jardines "
     "amplios.", None),
    ("palma-real", "La de los proyectos grandes y las avenidas: crece alta, recta y rápido.", None),
    ("palma-viajera-ravenala", "Abanico de alto impacto para entradas y jardines de diseño.", None),
    ("palma-washingtona", "La que gana altura más rápido; aguanta el viento del Golfo.", None),
    ("palma-bismarkia", "Hoja plateada en abanico: pieza exclusiva para jardines amplios.", None),
    ("palma-licuala", "Hoja redonda y plisada; va en semisombra.", None),
    ("palma-triangular", "Las hojas salen en tres filas y forman un triángulo; muy decorativa.", None),
    ("palma-cola-de-pescado", "Hojas con forma de cola de pez y folíolos irregulares: textura muy decorativa en jardines "
     "tropicales.", None),
    ("palma-cica-circinalis", "Cica de hojas largas y arqueadas, de poco mantenimiento.", None),
    ("palma-mascarena", "Palma botella: tronco abultado y copa compacta, para jardines chicos.", None),
    ("palma-kerpis", "Elegante y de copa ligera, para jardines residenciales y entradas.", None),
)
# Tabla de precios: las tres con precio del dueño y las demás palmas de la página, "según cotización".
CON_PRECIO = ("Palma Areca", "Coco Plumoso", "Palma Real")
TABLA = ("palma-areca", "coco-plumoso", "palma-real", "palma-viajera-ravenala", "palma-washingtona", "palma-bismarkia",
         "palma-licuala", "palma-triangular", "palma-cola-de-pescado", "palma-cica-circinalis", "palma-mascarena",
         "palma-kerpis")


def _fila(slug):
    e = cd.especie(slug)
    con_precio = e["name"] in CON_PRECIO
    precio = f"desde {dinero(datos.PRECIOS_ESPECIE[e['name']])}" if con_precio else datos.SEGUN_COTIZACION
    return (e["name"], e["sc"], precio, not con_precio)


PREGUNTAS = (
    ("¿Cuánto cuesta una palma en Tampico?",
     f"Depende de la especie y la altura. {datos.PALMAS_PRECIO}. Las exóticas, como bismarckia, licuala, triangular y "
     "mascareña, se cotizan por tamaño. Mándanos la altura que buscas por WhatsApp al 833 326 8008 y te damos el "
     "precio exacto."),
    ("¿Qué palmas son mejores para el clima de Tampico?",
     "Areca para semisombra e interior, coco plumoso para sol pleno, palma real para proyectos grandes, del viajero para "
     "jardines de diseño, bismarckia como pieza exclusiva y washingtonia cuando buscas altura rápido. Todas toleran "
     "calor, humedad y viento del Golfo."),
    ("¿Qué palma crece más rápido en Tampico?",
     "La washingtonia es la que gana altura más rápido. El coco plumoso da volumen en uno o dos años y la palma real "
     "también crece rápido. La areca es rápida en semisombra."),
    ("¿Qué palma necesita menos mantenimiento?",
     "Bismarckia, washingtonia y coco plumoso. Una vez que arraigan, solo necesitan riego ocasional. La areca pide riego "
     "más seguido, sobre todo en interior."),
    ("¿Entregan y siembran palmas a domicilio?",
     "Sí, en Tampico, Ciudad Madero y Altamira. Las palmas que sembramos nosotros tienen 30 días de garantía de arraigo, "
     "con condiciones: el riego y cuidado que te indicamos."),
    ("¿Qué palmas exóticas tienen?",
     "Bismarckia (hoja plateada), licuala (hoja redonda), triangular, cola de pescado, cica circinalis y mascareña o "
     "palma botella. Son difíciles de conseguir en la región: pregúntanos por WhatsApp antes de venir."),
    ("¿Las palmas exóticas sobreviven en Tampico?",
     "Sí. Las que manejamos están elegidas para el clima cálido y húmedo del Golfo. Pregúntanos cuáles van en sol y "
     "cuáles en sombra antes de sembrarlas."),
    ("¿Dónde comprar palmas en Tampico?",
     f"En el vivero de Viveros Terra: {datos.CALLE}, {datos.COLONIA}, {datos.CIUDAD} ({datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}). "
     f"Horario: {datos.HORARIO}. O por WhatsApp al 833 326 8008."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "cta_texto": "Cotizar mis palmas",  # Entrega B de experiencia: filas de WhatsApp tras las especies, los precios y las preguntas
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "pos": "50% 24%",
        "dato": 'Garantía de 30 días en lo que sembramos, <a href="/politicas#garantia-plantas">con condiciones</a>',
        "enlaces": ((f'Ver las {cd.cuenta({"cat": ["palmas"]})} palmas del catálogo', "/catalogo?cat=palmas", "plantas:catalogo"),),
        "lema": "Para darle a tu casa un aire de playa.",
        "h1": "Palmas para jardín en Tampico, tropicales y exóticas",
        "lede": f"{datos.PALMAS_PRECIO}.",
        "etiqueta": {"codigo": "Palmas", "aviso": f"Precios {datos.ANIO}", "nombre": "Areca y coco plumoso", "antes": "desde",
                     "monto": dinero(P["palma_desde"]), "unidad": "tamaño chico",
                     "filas": (("Palma real", f"desde {dinero(P['palma_real'])}"),),
                     "nota": "El precio sube con la altura."},
        "mensaje": MENSAJE,
        "foto": {"src": "/img/portadas/palma-real-jardin-residencial-tampico-sm.webp",
                 "srcset": ("/img/portadas/palma-real-jardin-residencial-tampico-sm.webp 560w, "
                            "/img/portadas/palma-real-jardin-residencial-tampico.webp 900w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 900, "alto": 1600, "numero": 1,
                 "alt": "Palma real sembrada en un jardín residencial de Tampico",
                 "lugar": "Palma real en un jardín", "etapa": "Tampico"},
    },
    "especies": {"titulo": "Palmas de jardín y exóticas en el vivero", "lede": pc.LEDE_FOTOS, "items": ESPECIES},
    "precios": {
        "titulo": "¿Cuánto cuesta una palma en Tampico?",
        "lede": f"{datos.PALMAS_PRECIO}.",
        "caption": "Precio del tamaño más chico en el vivero",
        "filas": tuple(_fila(s) for s in TABLA),
        # En celular, las 9 que se cotizan van en un solo renglón (la tabla completa se ve desde 768 px).
        "grupo": (f"Otras {len(TABLA) - len(CON_PRECIO)} palmas",
                  "Washingtonia, del viajero, bismarckia, licuala, triangular, cola de pescado, cica circinalis, "
                  "mascareña y kerpis", datos.SEGUN_COTIZACION),
        "nota": "El precio sube con la altura. Mándanos la altura que buscas y te damos el precio exacto.",
    },
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Preguntas frecuentes sobre palmas en Tampico", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de palmas", "items": (
        ("Palma areca en Tampico: cuidados", "/blog/palma-areca-tampico"),
        ("Palma real: cuidados y crecimiento", "/blog/palma-real-roystonea-regia-tampico"),
        ("Guía de precios de palmas en Tampico", "/blog/palmas-mas-vendidas-tampico-precios"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": pc.otras_subcategorias(RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos qué palma buscas, la altura y la colonia; te respondemos con precio por tamaño.",
               "mensaje": MENSAJE},
    "jsonld": {
        "migas": pc.migas_ld(NOMBRE, RUTA),
        "nodos": (
            {"@type": "Product", "name": "Palmas para jardín en Tampico", "brand": {"@type": "Brand", "name": datos.NOMBRE},
             "image": f"{SITE}{FOTO_LD}",
             # Precio "desde" del tamaño chico (areca y coco plumoso): AggregateOffer con lowPrice (SEO fase 1), sin
             # tope ni conteo de ofertas porque no existen.
             "offers": {"@type": "AggregateOffer", "lowPrice": P["palma_desde"], "priceCurrency": "MXN",
                        "seller": {"@id": pc.NEGOCIO}}},
            pc.lista_ld(NOMBRE, [s for s, _t, _a in ESPECIES]),
        ),
        "speakable": (".vt-portada .vt-lede", ".vt-faq details:first-child p"),
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION, {clave: (DESCRIPCION, "La garantía de 30 días se publica siempre «con condiciones» (regla del dueño); el "
                                  "resto de la descripción no cambia.") for clave in ("description", "og:description")}),
    "jsonld": {
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "Las palmas tropicales más solicitadas para el clima de Tampico": "Palmas de jardín y exóticas en el vivero",
        "Las 6 palmas más solicitadas en Tampico": "Palmas de jardín y exóticas en el vivero",
    },
    "retirados": {},
    "especies": {
        "reemplazos": {
            "Palma del Viajero": ("/palmas-tropicales-tampico", "Palma Viajera Ravenala"),
        },
        "retirados": {},
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Lema nuevo: «Para darle a tu casa un aire de playa.» (elegido por el dueño el 2026-11-10, en palabras del cliente); la lista de especies y la garantía de 30 días salen de la entrada (la garantía va en la línea de confianza, con sus condiciones).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: filas de WhatsApp («Cotizar mis palmas») tras el filtro por necesidad, las subcategorías, las especies (la rejilla larga se parte con una en medio), los precios y las preguntas, con la prueba social (cifras de datos.py y la calificación de Google con su enlace) y la garantía de las plantas que sembramos junto a la primera. Encabezados, precios y enlaces sin cambios.'
