"""Contenido de /palmas-mayoreo-proyectos (palmas al mayoreo para hoteles, fraccionamientos, industria y gobierno).
Solo datos: la plantilla es tools/site/plantillas/b2b.py, con la tabla de las 12 especies de datos.PALMAS_PROYECTO y
el armador de palmas (componentes.armador_palmas: especie, altura y cantidad → un solo WhatsApp), clientes con nombre y
logo, REPSE verificable y 3 paquetes por tipo de obra con su mensaje.

Precios (decisión del dueño, 2026-11-07): areca y coco plumoso desde $250 y palma real desde $500 en tamaño chico; el
precio sube con la altura; las demás especies, según cotización. Se retiran los precios “desde” de main ($850 a
$4,200 por ejemplar), los paquetes con monto, los proyectos anónimos, los plazos de entrega, las alturas y los “lead
time” por especie, la calculadora de rangos ($180K–$260K) y el pago “a crédito”: nada de eso está en datos.py ni lo
confirmó el dueño (preguntas al final del plan 2d). Título, canonical, robots, Open Graph (salvo la descripción, que
decía “desde $850”: PARIDAD["meta"]), Twitter Card, Service, el nodo LocalBusiness #localbusiness (se va con el grafo
único de la Etapa 4) y migas como estaban publicados; ItemList y AggregateOffer con los precios nuevos.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import b2b_comun

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/palmas-mayoreo-proyectos"
URL = f"{SITE}{RUTA}"
OBRA = "/img/obra"
DESDE, REAL = dinero(P["palma_desde"]), dinero(P["palma_real"])
# Respuesta del dueño (2026-11-08): los precios por talla de proyecto de main ($850–$4,200) no son reales. Solo se publican
# areca y coco plumoso desde $250 y palma real desde $500 en tamaño chico; todo lo demás, con esta frase.
SEGUN_ALTURA = "Según cotización por altura y volumen"
MENSAJE = mensajes_paginas.EMPRESAS[RUTA]
OG_IMAGEN = f"{SITE}/img/jardin-diseno-paisajismo-pasto-san-agustin-tampico-og.webp"
DESCRIPCION = (f"Productor directo de palmas para proyectos B2B. 12 especies; areca y coco plumoso desde {DESDE}. "
               f"Cobertura Tamaulipas, Veracruz y SLP. {datos.FACTURA} y garantía de arraigo de 30 días en siembra propia.")

META = {
    "title": "Palmas Mayoreo para Proyectos B2B en Tamaulipas, Veracruz y SLP · Viveros Terra",
    "description": DESCRIPCION,
    "robots": "index, follow, max-snippet:-1, max-image-preview:large",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", "Palmas Mayoreo para Proyectos B2B · Viveros Terra"),
        ("og:description", ("12 especies de palmas para proyectos en Tamaulipas, Veracruz y SLP. CFDI 4.0 y garantía de "
                            "arraigo de 30 días en siembra propia.")),
        ("og:image", OG_IMAGEN),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:locale", "es_MX"),
        ("og:site_name", "Viveros Terra Tampico"),
    ),
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", "Palmas Mayoreo Proyectos B2B · Viveros Terra"),
        ("twitter:description", ("12 especies. CFDI y garantía de arraigo de 30 días en siembra propia. Cobertura "
                                 "Tamaulipas, Veracruz y SLP.")),
        ("twitter:image", OG_IMAGEN),
    ),
}
NEGOCIO = f"{SITE}#localbusiness"  # @id de main; el grafo único con #negocio es de la Etapa 4
SERVICIO = {
    "@type": "Service", "@id": f"{URL}#service", "name": "Palmas al mayoreo para proyectos B2B",
    "serviceType": ("Venta y entrega de palmas para proyectos arquitectónicos, hoteleros, gubernamentales e "
                    "industriales"),
    "provider": {"@id": NEGOCIO},
    "areaServed": [{"@type": "State", "name": n} for n in ("Tamaulipas", "Veracruz", "San Luis Potosí")],
    "offers": {"@type": "AggregateOffer", "lowPrice": str(P["palma_desde"]), "priceCurrency": "MXN",
               "offerCount": str(len(datos.PALMAS_PROYECTO))},
}
LOCAL = {
    "@type": "LocalBusiness", "@id": NEGOCIO, "name": datos.NOMBRE, "url": SITE, "telephone": datos.TELEFONO_TEL,
    "address": {"@type": "PostalAddress", "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas",
                "addressCountry": "MX"},
    "sameAs": ["https://www.facebook.com/viverosterra/", "https://www.instagram.com/viverosterramx"],
}


def _producto(nombre, cientifico, precio):
    producto = {"@type": "Product", "name": nombre, "alternateName": cientifico}
    if precio is not None:
        producto["offers"] = {"@type": "Offer", "price": str(precio), "priceCurrency": "MXN",
                              "description": "Tamaño chico; el precio sube con la altura."}
    return producto


ESPECIES_LD = {"@type": "ItemList", "name": "12 palmas para proyectos B2B", "itemListElement": [
    {"@type": "ListItem", "position": i, "item": _producto(*e)} for i, e in enumerate(datos.PALMAS_PROYECTO, 1)]}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
    {"@type": "ListItem", "position": 2, "name": "Mayoreo B2B", "item": f"{SITE}/mayoreo-pasto-tampico"},
    {"@type": "ListItem", "position": 3, "name": "Palmas Mayoreo Proyectos", "item": URL},
]}

PREGUNTAS = (
    ("¿Cuál es el pedido mínimo al mayoreo?",
     "El precio por volumen depende de la especie, la altura y la cantidad de cada una: con tu lista te damos el precio "
     f"por escrito. Como referencia, la areca y el coco plumoso cuestan desde {DESDE} y la palma real desde {REAL} en "
     "su tamaño más chico."),
    ("¿Hacen envíos fuera de Tamaulipas?",
     f"Sí, por proyecto. Además de Tampico, Madero y Altamira, atendemos {datos.ZONAS_POR_PROYECTO}, y obras en el resto "
     "de Tamaulipas, el norte de Veracruz y San Luis Potosí. El flete se cotiza por ruta y volumen."),
    ("¿Qué pasa si una palma no arraiga?",
     "Las palmas que sembramos nosotros tienen garantía de arraigo de 30 días: si se regaron como te indicamos y no "
     "prende, la reponemos sin costo. No cubre falta o exceso de riego, daños por terceros ni clima extremo. "
     '<a href="/politicas#garantia-plantas">Ver condiciones</a>.'),
    ("¿Tienen factura?",
     f"Sí. {datos.FACTURA} para persona física o moral, con tus datos fiscales validados "
     "antes de la entrega."),
    ("¿Cuánto tarda la entrega?",
     "Depende de la especie, la altura y el destino: el plazo va por escrito en la cotización, con el calendario de "
     "entregas si la obra avanza por etapas."),
    b2b_comun.PREGUNTA_PAGO,
    ("¿Pueden hacer instalación llave en mano?",
     "Sí: maniobra de plantación con nuestra cuadrilla, supervisión y guía de cuidado. La garantía de 30 días aplica a "
     "las palmas que sembramos nosotros. Fuera de la zona conurbada de Tampico, la siembra se cotiza por proyecto."),
    ("¿Trabajan con compras de gobierno?",
     f"Sí: el Gobierno de Tampico es cliente nuestro. Tenemos REPSE {datos.REPSE} y facturamos {datos.FACTURA}; los "
     "requisitos de tu convocatoria (padrón de proveedores, fianzas o actas) los revisamos contigo al cotizar."),
)

PASOS = (
    {"titulo": "Nos mandas tu lista", "quien": "tu", "cuando": "Para empezar",
     "texto": "Especies, alturas y cantidades (o el plano del proyecto), la ubicación de la obra y las fechas."},
    {"titulo": "Cotización por escrito", "quien": "nosotros", "cuando": "Al revisar tu lista",
     "texto": "Precio por especie y altura, total, plazo de entrega y condiciones de pago, por escrito."},
    {"titulo": "Anticipo y calendario", "quien": "juntos", "cuando": "Al confirmar",
     "texto": "Confirmas con un anticipo y fijamos juntos las fechas de entrega según el avance de la obra."},
    {"titulo": "Entrega en obra", "quien": "nosotros", "cuando": "En cada etapa",
     "texto": ("Entregamos en obra en Tampico, Madero y Altamira; fuera de la zona, el flete se cotiza por ruta. La "
               "maniobra y las fechas te las confirmamos por escrito con la cotización.")},
    {"titulo": "Siembra con garantía", "quien": "nosotros", "cuando": "Si la contratas",
     "texto": ("Si las sembramos nosotros, la garantía de arraigo de 30 días aplica con el riego indicado; te dejamos la "
               "guía de cuidado por escrito.")},
)

FIGURAS = (
    {"src": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961, "numero": 2,
     "alt": "Palmas en costal listas para entrega en el patio del vivero.", "lugar": "Patio del vivero",
     "etapa": "Palmas para entrega"},
    {"src": "/img/especie-coco-plumoso-tampico.webp", "ancho": 466, "alto": 700, "numero": 3,
     "alt": "Coco plumoso (Syagrus romanzoffiana) en nuestro vivero.", "lugar": "Coco plumoso",
     "etapa": "En nuestro vivero"},
    {"src": "/img/especie-palma-areca-tampico.webp", "ancho": 700, "alto": 525, "numero": 4,
     "alt": "Palma areca (Dypsis lutescens) en nuestro vivero.", "lugar": "Palma areca",
     "etapa": "En nuestro vivero"},
)

PAQUETES = (
    {"rotulo": "Paquete 1 · Fraccionamientos", "titulo": "Áreas comunes, camellones y casa muestra",
     "precio_texto": SEGUN_ALTURA, "detalle": "según especies, alturas y cantidad",
     "puntos": ("Washingtonia y areca para accesos y camellones", "Entregas por etapas: la casa muestra primero",
                "Siembra con nuestra cuadrilla y garantía de 30 días con el riego indicado"),
     "mensaje": ("Hola, quiero cotizar palmas para un fraccionamiento.\nEmpresa: ___\n"
                 "Áreas (accesos, camellones, casa muestra): ___\nEspecies y cantidad: ___\nUbicación: ___\n"
                 "Fecha de entrega: ___")},
    {"rotulo": "Paquete 2 · Hoteles y comercios", "titulo": "Palmas de imagen para hoteles y comercios",
     "precio_texto": SEGUN_ALTURA, "detalle": "según especies, alturas y cantidad", "rec": True,
     "puntos": ("Palma real, coco plumoso y areca", "Especies para el clima de la costa del Golfo",
                'Diseño del área con el <a href="/diseno-jardines-tampico">Plan Terra</a>, si lo necesitas'),
     "mensaje": ("Hola, quiero cotizar palmas para un hotel o comercio.\nEmpresa: ___\nEspecies y cantidad: ___\n"
                 "Altura aprox.: ___\nUbicación: ___\nFecha de entrega: ___")},
    {"rotulo": "Paquete 3 · Industria y gobierno", "titulo": "Perímetros y áreas públicas de bajo mantenimiento",
     "precio_texto": SEGUN_ALTURA, "detalle": "según especies, alturas y cantidad",
     "puntos": ("Washingtonia y cycas para perímetros", f"REPSE {datos.REPSE} y factura {datos.FACTURA}",
                '<a href="/mantenimiento-jardines-tampico">Mantenimiento</a> después de la entrega'),
     "mensaje": ("Hola, quiero cotizar palmas para una nave industrial o un área pública.\nEmpresa o institución: ___\n"
                 "Especies y cantidad: ___\nUbicación: ___\nFecha de entrega: ___")},
)

CONTENIDO = {
    "tipo": "b2b",
    "prefijo": "pal",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "nodos": (LOCAL, ESPECIES_LD), "migas": MIGAS_LD,
               "speakable": ("h1", "h2", ".vt-faq summary")},
    # /empresas llega en la Etapa 3: entonces la ruta visible y MIGAS_LD pasan a Inicio › Empresas › Palmas.
    "migas": (("Inicio", "/"), ("Palmas para proyectos", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Constructoras · Hoteles · Gobierno",
        "h1": 'Palmas al mayoreo <span class="vt-serif">para proyectos en Tampico</span>',
        "lede": (f"En Viveros Terra la palma areca y el coco plumoso cuestan desde {DESDE} y la palma real desde {REAL} "
                 "en tamaño chico; el precio sube con la altura. Entregamos en obra en Tampico, Madero y Altamira y, por "
                 f"proyecto, en Tamaulipas, Veracruz y San Luis Potosí, con factura {datos.FACTURA}."),
        "etiqueta": {
            "codigo": "Palmas · 01", "aviso": "Con IVA", "nombre": "Palma areca y coco plumoso",
            "cientifico": "Dypsis lutescens · Syagrus romanzoffiana", "antes": "Tamaño chico · desde", "monto": DESDE,
            "unidad": "c/u",
            "filas": (("Palma real, tamaño chico", f"desde {REAL}"), ("Otras especies y alturas", "Según cotización")),
        },
        "mensaje": MENSAJE,
        "tambien": f'REPSE {datos.REPSE} · factura {datos.FACTURA} · <a href="#precio">arma tu lista de palmas</a>',
        "foto": {"src": "/img/portadas/palmas-reales-mayoreo-vivero-tampico-sm.webp",
                 "srcset": ("/img/portadas/palmas-reales-mayoreo-vivero-tampico-sm.webp 560w, "
                            "/img/portadas/palmas-reales-mayoreo-vivero-tampico.webp 694w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 694, "alto": 1041, "numero": 1,
                 "alt": "Palmas reales en el vivero listas para proyecto", "lugar": "Palmas reales en el vivero",
                 "etapa": "Para proyecto"},
    },
    "prueba": {
        "titulo": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
        "lede": (f"{datos.M2_INSTALADOS} instalados desde {datos.DESDE} en Tamaulipas y la Huasteca: hoteles, "
                 "fraccionamientos, industria y gobierno."),
        "figuras": FIGURAS,
        "nota": ("Si el render pide palmas muy altas de una sola especie, pregúntanos antes de cerrar el plano: a veces "
                 "otra altura u otra especie da el mismo efecto, y te lo decimos al cotizar.", "Al cotizar"),
    },
    "escalas": {
        "titulo": "¿Cuánto cuestan las palmas para proyecto?",
        "lede": (f"Areca y coco plumoso desde {DESDE} y palma real desde {REAL} en tamaño chico, con IVA. El precio sube "
                 f"con la altura; las demás especies, {SEGUN_ALTURA.lower()}. Precios {datos.ANIO}."),
        "columnas": ("Especie", "Nombre científico", "Precio"),
        "filas": tuple((n, f"<i>{sci}</i>", f"desde {dinero(p)} · tamaño chico" if p else SEGUN_ALTURA)
                       for n, sci, p in datos.PALMAS_PROYECTO),
        "caption": ("El precio de cada ejemplar depende de su altura: la cotización por escrito lleva especie, altura, "
                    "cantidad y precio."),
        "titulo_cotizador": "Arma tu lista de palmas",
        "cotizador": "palmas",
    },
    "formulario": {
        "titulo": "¿Compras prefiere correo? Manda tu lista de palmas",
        "lede": b2b_comun.LEDE_CORREO,
        "pagina": "Palmas para proyectos", "cta": "palmas:formulario",
        "cantidad": ("Lista de palmas (especie, altura y cantidad)", "Ej. 40 palma real de 3 m, 120 areca", True),
    },
    "documentacion": {
        "titulo": "Documentación completa para tu compra empresarial.",
        "lede": "Lo que necesitan compras, finanzas, gobierno y supervisión de obra para liberar el pago.",
        "items": b2b_comun.DOCUMENTACION,
    },
    "paquetes": {
        "titulo": "Empieza con un paquete pre-armado y ajustamos a tu obra.",
        "lede": "Cada paquete es un punto de partida: la cotización final se ajusta a tu plano.",
        "items": PAQUETES,
    },
    "proceso": {"titulo": "Cómo cotizamos tu proyecto de palmas",
                "lede": "De tu lista a la entrega en obra, con precio y plazo por escrito.", "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo de 30 días en las palmas que sembramos.", "grande": "30", "unidad": "días",
        "resumen": datos.GARANTIA_PLANTAS,
        "puntos": (
            ("Si una palma que sembramos no prende en 30 días y se regó como te indicamos, la reponemos sin costo.", True),
            ("Guía de cuidado por escrito al entregar.", True),
            (f"Factura {datos.FACTURA} y REPSE {datos.REPSE}.", True),
            ("No cubre falta o exceso de riego, daños por terceros o por clima extremo, ni palmas que siembra otra "
             "cuadrilla.", False),
        ),
        "pie": '<a href="/politicas#garantia-plantas">Lee las condiciones de la garantía de plantas</a>',
    },
    "faq": {"titulo": "Preguntas frecuentes de compradores B2B.", "preguntas": PREGUNTAS},
    "cobertura": dict(b2b_comun.COBERTURA, titulo="Enviamos palmas a toda la región.",
                      lede=("Entrega en obra en la zona conurbada; en el resto de Tamaulipas, el "
                            "norte de Veracruz y San Luis Potosí, por proyecto y con flete por ruta.")),
    "relacionados": {"titulo": "Otras soluciones para empresas", "items": b2b_comun.relacionados(RUTA)},
    "cierre": {
        "titulo": "Cotiza tu proyecto ahora.",
        "lede": "Mándanos especies, alturas y cantidades, o el plano. Te enviamos precio y plazo por escrito.",
        "mensaje": MENSAJE,
    },
}

PRECIO_VIEJO = ("Precio “desde” por ejemplar de main en tallas de proyecto, sin confirmar por el dueño: queda la decisión "
                "del 2026-11-07 (areca y coco plumoso desde $250, palma real desde $500 en tamaño chico; las demás, "
                "según cotización). Pregunta al dueño en el plan 2d.")
PAQUETE_VIEJO = ("Monto “desde” de un paquete de main que el dueño no confirmó: los 3 paquetes nuevos van “según "
                 "cotización”, cada uno con su mensaje. Pregunta al dueño en el plan 2d.")
RANGO_VIEJO = ("Rango de la calculadora vieja ($180K–$260K) o umbral del pago a crédito ($100K): inventados; el armador de "
               "palmas no muestra total y el pago es anticipo y avances (datos.ANTICIPO_PROYECTOS).")
FAQ_SUMMARY = "La pregunta sigue en el FAQ, ahora como <summary> (la paridad la cuenta en su categoría faq)."
ESPECIE = "La especie sigue como renglón de la tabla de especies (datos.PALMAS_PROYECTO) y en el armador de palmas."
CREDITO = ("Decisión del dueño: no se ofrece crédito ni pago diferido. La pregunta pasa a “¿Cómo se paga un proyecto?” con "
           "el anticipo al confirmar y el resto contra avances de obra (datos.ANTICIPO_PROYECTOS).")
PROYECTO_ANONIMO = ("Proyecto anónimo sin nombre, foto ni permiso verificables: regla del dueño “sin proyectos "
                    "inventados”. Si es real, el dueño lo da con permiso (pregunta del plan 2d).")

PARIDAD = {
    "meta": {"description": (DESCRIPCION, "Decía “12 especies desde $850”: precio sin confirmar; el dueño fijó areca "
                                          "y coco plumoso desde $250 (2026-11-07).")},
    "reemplazos": {
        "Productor directo de palmas para hoteles, fraccionamientos, gobierno e industria": (
            f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B"),
        "12 palmas para proyectos · spec sheet": "¿Cuánto cuestan las palmas para proyecto?",
        "Calcula tu proyecto antes de hablar con ventas.": "Arma tu lista de palmas",
        "Enviamos palmas a toda la región .": "Enviamos palmas a toda la región.",
        "Documentación completa para tu compra empresarial .": "Documentación completa para tu compra empresarial.",
        "CFDI 4.0": f"Factura {datos.FACTURA}",
        "Garantía de arraigo 30 días": "Garantía de arraigo de 30 días en las palmas que sembramos.",
        "Fraccionamiento": "Áreas comunes, camellones y casa muestra",
        "Hotel Boutique": "Palmas de imagen para hoteles y comercios",
        "Parque Industrial": "Perímetros y áreas públicas de bajo mantenimiento",
        "Gobierno / Licitación": "Perímetros y áreas públicas de bajo mantenimiento",
        "Preguntas frecuentes de compradores B2B .": "Preguntas frecuentes de compradores B2B.",
    },
    "retirados": {
        "Por qué arquitectos y compradores corporativos eligen Viveros Terra .": (
            "Diferenciadores sin dato: “productor directo” queda en la descripción; la logística pasa a la cobertura y "
            "al proceso, y la documentación a su sección."),
        "Productor directo": "Queda en la descripción; “capacidad sin agotar stock” no está en datos.py.",
        "Logística regional": ("Pasa a la cobertura y al paso “Entrega en obra”; la maniobra, “transportes propios y "
                               "red de fleteros” quedan por escrito en la cotización (el dueño no los publicó)."),
        "Documentación B2B": "Pasa a la sección de documentación (CFDI, REPSE, anticipo y avances, entregas).",
        "Hecho para tres tipos de comprador.": (
            "Las tres personas llevaban citas ficticias entre comillas; sus necesidades pasan a los 3 paquetes por obra "
            "y a las preguntas de compras."),
        "Que el ejemplar llegue idéntico al render.": (
            "Cita ficticia; “ficha técnica y foto del ejemplar” no está confirmada (pregunta al dueño). Lo útil pasa a "
            "la nota de campo sobre alturas."),
        "Cumplir auditoría sin retrasos administrativos.": (
            "Cita ficticia; padrón, fianzas y acta de entrega no están confirmados: la pregunta de gobierno los revisa "
            "al cotizar."),
        "No retrasar la fecha de apertura del proyecto.": (
            "Cita ficticia; los plazos “2–5 días” no están en datos.py: el plazo va por escrito en la cotización."),
        **{e: ESPECIE for e in ("Palma Washingtonia", "Palma Real", "Palma Areca", "Palma del Viajero", "Coco Plumoso",
                                "Palma Kerpis", "Cycas Revoluta", "Bambú Tarro", "Yucca Rostrata", "Palma Bambú",
                                "Palma Cola de Zorra", "Palma Triángulo")},
        "Tu proyecto pre-armado": "Resumen de la calculadora vieja; el armador de palmas muestra la lista que se envía.",
        "Nuestras palmas, en foto real .": (
            "La galería de 12 fotos pasa a 3 figuras con pie FIG. en la sección de clientes (peso de la página)."),
        "Algunos proyectos recientes .": PROYECTO_ANONIMO,
        **{t: PROYECTO_ANONIMO for t in ("50 Palma Real + Coco Plumoso", "90 Washingtonia", "Áreas comunes 4 fases",
                                         "Áreas verdes recreativas", "35 Coco Plumoso", "120 plantas + 15 palmas")},
        "Envíos fuera de Tamaulipas": "Pasa a la pregunta “¿Hacen envíos fuera de Tamaulipas?” y a la cobertura.",
        "Licitaciones / gobierno": "Pasa a la pregunta “¿Trabajan con compras de gobierno?”, sin prometer fianzas.",
        **{q: FAQ_SUMMARY for q in ("¿Cuál es el pedido mínimo al mayoreo?", "¿Hacen envíos fuera de Tamaulipas?",
                                    "¿Qué pasa si una palma no arraiga?", "¿Tienen factura?", "¿Cuánto tarda la entrega?",
                                    "¿Pueden hacer instalación llave en mano?", "¿Trabajan con compras de gobierno?")},
        "¿Aceptan pago diferido / a crédito para proyectos?": CREDITO,
        "¿Aceptan pago diferido o a crédito para proyectos?": CREDITO,
        "Formulario de cotización": (
            "El formulario no mandaba correo: armaba un WhatsApp. Lo sustituyen el armador de palmas y, por respuesta del "
            "dueño (2026-11-08), la cotización por correo para compras (formsubmit, como los materiales)."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” pasa al título de clientes."),
        **{pr: PRECIO_VIEJO for pr in ("$850", "$1,200", "$1,500", "$1,600", "$1,800", "$2,000", "$2,200", "$2,400",
                                       "$2,800", "$3,200", "$4,200")},
        **{pr: PAQUETE_VIEJO for pr in ("$90,000", "$150,000", "$180,000")},
        **{pr: RANGO_VIEJO for pr in ("$100", "$180", "$260")},
    },
}
