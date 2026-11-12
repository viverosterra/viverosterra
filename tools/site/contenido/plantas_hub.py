"""Contenido de /plantas-palmas-arboles-tampico (hub de plantas). Plantilla: plantillas/hub_categoria.py.

Precios (decisión del dueño, 2026-11-07): palmas con datos.PALMAS_PRECIO y flamboyán desde $250; nada más. Se retiran los
"desde" sin confirmar de main (washingtonia, viajero y kerpis $500, cycas $700, palma bambú $1,000, cola de zorro $1,500,
ficus $200, neem y trueno $300, tabachín $350, laurel $500, tulipán africano $600; preguntas 1–3 al dueño), las dos
opiniones sin permiso (Martha R., Constructora Arce; pregunta 8), "asesoría sin costo", "más de 18 años" y la entrega en la
Huasteca. Las tarjetas de especie son las de main con la misma foto (decisión del dueño, 2026-11-08), servida en local desde
contenido/catalogo_especies.json en vez de /api/img, y no se presentan como tomadas en el vivero. Título,
robots y canonical como estaban (los títulos son de la Etapa 3); la descripción de Open Graph decía "Desde $200"
(PARIDAD["meta"]).
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = pc.HUB
URL = f"{SITE}{RUTA}"
TIPO = "plantas"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
FLAMBOYAN = f"Flamboyán desde {dinero(P['flamboyan'])}"
PALMAS_EN_CATALOGO = cd.cuenta({"cat": ["palmas"]})
RIEGO = P["riego_m2"]

TITULO = "Plantas, Palmas y Árboles en Tampico | Viveros Terra"
DESCRIPCION = ("Más de 200 variedades de plantas, palmas y árboles para el clima de Tampico: sol, sombra o salitre. Con entrega y "
               "siembra. Arma tu lista y cotiza.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (("og:type", "website"), ("og:url", URL),
           ("og:title", TITULO),
           ("og:description", DESCRIPCION),
           ("og:image", f"{SITE}/img/paisajismo-alberca-plantas-tampico.webp"), ("og:locale", "es_MX")),
}
# Las tarjetas de especie del hub de main, en su orden y con su foto (decisión del dueño, 2026-11-08: las fotos quedan
# como están). Sin los "desde" sin confirmar; tabachín, trueno y tulipán africano siguen fuera (sus tarjetas solo
# afirmaban precios sin confirmar; preguntas 1–3 al dueño).
DESTACADAS = (
    ("palma-washingtona", "Gana altura rápido y aguanta el viento del Golfo; para entradas y banquetas.", None),
    ("palma-viajera-ravenala", "Abanico de alto impacto para entradas, hoteles y jardines de diseño.", None),
    ("palma-areca", "Para interior y semisombra: oficinas, lobbies y jardines residenciales.", None),
    ("palma-cica-revoluta", "Muy longeva y de poco mantenimiento; va en maceta o en jardín formal.", None),
    ("palma-kerpis", "Elegante y resistente, para jardines residenciales con sombra parcial.", None),
    ("coco-plumoso", "Follaje plumoso arqueado para jardines amplios y entradas.", None),
    ("palma-seifrixi-bambu", "Para interior y semisombra en espacios grandes: efecto tropical.", None),
    ("palma-cola-de-zorra", "Especie de alto impacto visual para jardines exclusivos.", None),
    ("ficus-benjamin", "Árbol de sombra y de seto; se forma con poda y va en jardineras.", None),
    ("flamboyan-tabachin", "Floración rojo-naranja y sombra abundante.", None),
    ("neem", "Sombra rápida, muy resistente y de bajo mantenimiento.", None),
    ("laurel-de-la-india-formado", "Sombra abundante y crecimiento rápido; muy ornamental.", None),
    ("ave-de-paraiso", "Flor naranja y azul de máximo impacto para jardines y hoteles.", None),
    ("duranta-cubana", "Setos vivos que crecen rápido; muy resistente al calor.", None),
    ("bugambilea-envarada", "Para bardas y enredaderas; florece casi todo el año con muy poca agua.", None),
    ("croto-petra", "Color intenso todo el año para orlas, arriates y jardines tropicales.", None),
)
PREGUNTAS = (
    ("¿Cuánto cuestan las palmas en Tampico?",
     f"{datos.PALMAS_PRECIO}. Las demás palmas (washingtonia, del viajero, kerpis, cola de zorro, cycas, palma bambú y "
     "las exóticas) se cotizan según su altura: mándanos la que buscas y la altura por WhatsApp."),
    ("¿Cuánto cuestan los árboles en Tampico?",
     f"{FLAMBOYAN}. Los demás árboles (neem, ficus, laurel de la India, olivo negro, jacaranda y más) se cotizan según "
     "la especie y el tamaño del ejemplar."),
    ("¿Qué palmas crecen mejor en Tampico?",
     "Las mejor adaptadas al clima cálido y húmedo de Tampico son la washingtonia, la palma del viajero, la cycas "
     "revoluta y la palma areca para semisombra."),
    pc.PREGUNTA_ENTREGA,
    ("¿Qué palmas crecen mejor en el calor de Tampico?",
     "La washingtonia (crece rápido y tolera el viento del Golfo), la palma del viajero (resiste el calor intenso), la "
     f"cycas revoluta (muy longeva y de poco mantenimiento) y la areca en semisombra. En el catálogo hay "
     f"{PALMAS_EN_CATALOGO} especies de palmas."),
    ("¿Tienen catálogo para ver antes de llamar?",
     f"Sí: en <a href=\"/catalogo\">Arma tu lista</a> están {len(cd.ESPECIES)} especies con luz, riego y altura. "
     "Añades las que te interesan con su tamaño y piezas y nos mandas la lista en un solo mensaje de WhatsApp; te "
     "respondemos con el precio por tamaño."),
    ("¿Tienen precio de mayoreo para proyectos grandes?",
     "Sí, para constructoras, arquitectos, hoteles, fraccionamientos y gobierno, con factura CFDI 4.0 y entrega por "
     "etapas. Las palmas para obra tienen su página: <a href=\"/palmas-mayoreo-proyectos\">palmas para proyectos</a>."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": TIPO,
    "meta": META,
    "migas": pc.migas(),
    "portada": {
        "kicker": f"Vivero en Cd. Madero · desde {datos.DESDE}",
        "pos": "50% 66%",
        "dato": 'Garantía de 30 días en lo que sembramos, <a href="/politicas#garantia-plantas">con condiciones</a>',
        "enlaces": (("Arma tu lista", "/catalogo", "plantas:catalogo"),),
        "lema": f"Más de {datos.VARIEDADES.lstrip('+')} plantas que sí se dan en Tampico.",
        "h1": "Plantas, palmas y árboles de nuestro vivero en Tampico",
        "lede": ("Te decimos cuáles van en sol o sombra, cuáles aguantan salitre y cuánto crecen. Te las llevamos y, si "
                 "quieres, las sembramos."),
        "etiqueta": {"codigo": "Vivero", "aviso": f"Precios {datos.ANIO}", "nombre": "Areca y coco plumoso", "antes": "desde",
                     "monto": dinero(P["palma_desde"]), "unidad": "tamaño chico",
                     # Flamboyán antes que palma real: "$500 … Flamboyán" lo marcaría test_consistencia ("flamboyán a $500").
                     "filas": (("Flamboyán", f"desde {dinero(P['flamboyan'])}"),
                               ("Palma real", f"desde {dinero(P['palma_real'])}")),
                     "nota": "El precio sube con la altura; las demás especies, según cotización."},
        "mensaje": MENSAJE,
        "foto": {"src": "/img/portadas/arboles-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/arboles-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/arboles-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Equipo de Viveros Terra sembrando un árbol en un jardín de Tampico",
                 "lugar": "Siembra de un árbol", "etapa": "Tampico"},
    },
    "necesidad": {"titulo": "¿Qué necesita tu jardín?",
                  "lede": "Elige por sol, salitre o tamaño y te llevamos al catálogo con el filtro puesto.",
                  "items": pc.NECESIDADES},
    "subcategorias": {"titulo": "Palmas, árboles y plantas para Tampico",
                      "lede": "Cada página dice qué especies van en sol, sombra o cerca del mar.",
                      "items": pc.SUBCATEGORIAS},
    "destacadas": {"titulo": "Palmas, árboles y plantas con su ficha", "id": "vt-h-destacadas", "rotulo": "Especies",
                   "lede": pc.LEDE_FOTOS, "items": DESTACADAS},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Todo sobre plantas y palmas en Tampico", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Explora por tipo de planta", "items": (
        ("8 palmas para jardín con precios", "/blog/palmas-para-jardin-tampico"),
        ("Cómo plantar una palma o un árbol", "/blog/como-plantar-palma-arbol-paso-a-paso-tampico"),
        ("Plantas que resisten la sal del Golfo", "/blog/plantas-resistentes-sal-golfo-tampico"))},
    "relacionados": {"titulo": "Complementa tu proyecto", "items": (
        {"titulo": "Nochebuenas de temporada", "href": datos.NOCHEBUENAS["ruta"],
         "texto": "Roja, rosa y jaspeada, en menudeo y mayoreo.",
         "img": "/img/nochebuenas/nochebuena-roja-tres-plantas-tampico-800.webp", "ancho": 800, "alto": 600},
        {"titulo": "Pasto en rollo", "href": "/pasto-en-rollo-tampico",
         "texto": f"San Agustín desde {dinero(P['pasto_solo_m2'])}/m².",
         "img": "/img/portadas/instalacion-pasto-rollo-san-agustin-tampico-sm.webp", "ancho": 560, "alto": 840},
        {"titulo": "Diseño de jardines", "href": "/diseno-jardines-tampico",
         "texto": f"Proyecto desde {dinero(P['diseno'])}.",
         "img": "/img/portadas/diseno-jardines-tampico-proyecto-sm.webp", "ancho": 560, "alto": 918},
        {"titulo": "Riego automático", "href": "/sistema-riego-tampico",
         "texto": f"Instalado desde {dinero(RIEGO[0])}/m².",
         "img": "/img/portadas/riego-pro-01-sm.webp", "ancho": 560, "alto": 373},
        {"titulo": "Tierra negra", "href": "/tierra-negra-vegetal-tampico",
         "texto": f"Costal {dinero(P['tierra_negra_costal'])} · m³ {dinero(P['tierra_negra_m3'])}.",
         "img": "/img/portadas/camion-tierra-negra-entrega-tampico-sm.webp", "ancho": 560, "alto": 373},
        {"titulo": "Palmas para proyectos", "href": "/palmas-mayoreo-proyectos",
         "texto": "Hoteles, fraccionamientos, industria y gobierno: volumen, CFDI 4.0 y entrega por etapas.",
         "img": "/img/portadas/palmas-reales-mayoreo-vivero-tampico-sm.webp", "ancho": 560, "alto": 841})},
    "cierre": {"titulo": "¿Ya sabes qué quieres sembrar?",
               "lede": "Mándanos qué buscas, el tamaño y la colonia; te respondemos con precio por tamaño.",
               "mensaje": MENSAJE},
    "jsonld": {
        "migas": pc.migas_ld(),
        "nodos": ({"@type": "ItemList", "name": "Plantas, palmas y árboles por subcategoría", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": s["titulo"], "url": f"{SITE}{s['href']}"}
            for i, s in enumerate(pc.SUBCATEGORIAS, 1)]},),
        "speakable": (".vt-portada .vt-lede", ".vt-faq details:first-child p"),
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION, {"og:description": (DESCRIPCION, "Decía «Desde $200»: precio sin confirmar (el dueño solo fijó palmas desde "
                                                "$250, palma real $500 y flamboyán $250, 2026-11-07).")}),
    "jsonld": {
        "PostalAddress": "Iba dentro del LocalBusiness recortado de main; la dirección es del nodo #negocio de la home.",
    },
    "reemplazos": {
        "¿Tienen catálogo con precios para ver antes de llamar?": "¿Tienen catálogo para ver antes de llamar?",
        "¿Cuál es la planta ideal para tu proyecto?": "¿Qué necesita tu jardín?",
        "Bajo mantenimiento": "¿Qué necesita tu jardín?",
        "Industria y banquetas": "Árboles para banqueta",
        "Hotel y comercio": "Palmas para proyectos",
        "Jardín residencial": "Plantas para jardín",
        "No sé cuál elegir": "¿Ya sabes qué quieres sembrar?",
        "El vivero de confianza para proyectos grandes en Tamaulipas": "Palmas para proyectos",
        "¿Cuál es tu planta?": "¿Ya sabes qué quieres sembrar?",
        # tarjetas de especie (h3) que siguen en el hub con el nombre del catálogo
        "Palma del Viajero": "Palma Viajera Ravenala",
        "Bugambilia": "Bugambilea Envarada",
        "Cycas Revoluta": "Palma Cica Revoluta",
        "Ficus benjamina": "Ficus Benjamin",
        "Flamboyán": "Flamboyán Tabachín",
        "Palma Coco Plumoso": "Coco Plumoso",
        "Palma Bambú": "Palma Seifrixi Bambú",
        "Laurel de la India": "Laurel de la India Formado",
        "Ave del Paraíso": "Ave de Paraíso",
        "Croton": "Croto Petra",
    },
    "retirados": {
        "+20 árboles más": "Tarjeta que solo enlazaba el catálogo; la cubre «Arma tu lista» (los 25 árboles del catálogo).",
        "Tabachín": ("Usaba la foto de la Tronadora y el catálogo llama tabachín al flamboyán; no se publica como "
                     "especie aparte hasta que el dueño diga cuál es (pregunta 2)."),
        "Trueno": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        "Tulipán Africano": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        "$500,": ("Era «$500,» dentro de la lista de palmas sin confirmar; $500 sigue como el precio de la palma real "
                  "(datos.PRECIOS_ESPECIE)."),
        "Lo que dicen quienes ya tienen su jardín": ("Las dos opiniones (Martha R., Constructora Arce) no están en "
                                                      "datos.OPINIONES ni tienen permiso confirmado (pregunta 8)."),
        "Jardines con plantas de Viveros Terra": ("Galería sin pies ni datos; las especies con foto, luz, riego y altura "
                                                  "van en «Palmas, árboles y plantas con su ficha»."),
        "Variedades seleccionadas para el clima de Tampico": ("Sección de beneficios genéricos («asesoría sin costo», "
                                                              "«más de 18 años»); lo útil va al filtro por necesidad."),
        "$1,000": "Palma bambú desde $1,000: precio sin confirmar; las palmas sin precio del dueño van según cotización.",
        "$200": "Ficus benjamina desde $200: precio sin confirmar (pregunta 1 al dueño).",
        "$200,": "Ficus benjamina desde $200 (con coma en el texto): precio sin confirmar (pregunta 1 al dueño).",
        "$300": "Neem y trueno desde $300: precios sin confirmar (pregunta 1 al dueño).",
        "$300,": "Neem y trueno desde $300 (con coma en el texto): precios sin confirmar (pregunta 1 al dueño).",
        "$350": "Tabachín desde $350: precio sin confirmar y especie dudosa (preguntas 1 y 2 al dueño).",
        "$350,": "Tabachín desde $350 (con coma en el texto): precio sin confirmar (preguntas 1 y 2 al dueño).",
        "$600": "Tulipán africano desde $600: precio sin confirmar y especie fuera del catálogo (pregunta 3).",
        "$700": "Cycas revoluta desde $700: palma sin precio del dueño; va según cotización.",
        "$700,": "Cycas revoluta desde $700 (con coma en el texto): palma sin precio del dueño; va según cotización.",
    },
    "especies": {
        "reemplazos": {
            "Palma del Viajero": ("/plantas-palmas-arboles-tampico", "Palma Viajera Ravenala"),
            "Palma Coco Plumoso": ("/plantas-palmas-arboles-tampico", "Coco Plumoso"),
            "Flamboyán": ("/plantas-palmas-arboles-tampico", "Flamboyán Tabachín"),
            "Cycas Revoluta": ("/plantas-palmas-arboles-tampico", "Palma Cica Revoluta"),
            "Palma Bambú": ("/plantas-palmas-arboles-tampico", "Palma Seifrixi Bambú"),
            "Ficus benjamina": ("/plantas-palmas-arboles-tampico", "Ficus Benjamin"),
            "Laurel de la India": ("/plantas-palmas-arboles-tampico", "Laurel de la India Formado"),
            "Ave del Paraíso": ("/plantas-palmas-arboles-tampico", "Ave de Paraíso"),
            "Bugambilia": ("/plantas-palmas-arboles-tampico", "Bugambilea Envarada"),
            "Croton": ("/plantas-palmas-arboles-tampico", "Croto Petra"),
        },
        "retirados": {
            "Tabachín": ("Usaba la foto de la Tronadora y el catálogo llama tabachín al flamboyán; no se publica como "
                         "especie aparte hasta que el dueño diga cuál es (pregunta 2)."),
            "Trueno": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
            "Tulipán Africano": "No está en el catálogo (sin foto ni nombre científico); pregunta 3 al dueño.",
        },
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Lema nuevo: «Más de 200 plantas que sí se dan en Tampico.» (elegido por el dueño el 2026-11-10, en palabras del cliente).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: filas de WhatsApp («Cotizar mis plantas») tras el filtro por necesidad, las subcategorías, las especies (la rejilla larga se parte con una en medio), los precios y las preguntas, con la prueba social (cifras de datos.py y la calificación de Google con su enlace) y la garantía de las plantas que sembramos junto a la primera. Encabezados, precios y enlaces sin cambios.'
