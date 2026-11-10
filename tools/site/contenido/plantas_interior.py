"""Contenido de /plantas-de-interior-tampico (subcategoría del hub de plantas). Plantilla: plantillas/hub_categoria.py.

Las seis especies de main, en su orden y con la foto del catálogo (decisión del dueño, 2026-11-08: las fotos quedan
como están), servida en local; la palma areca conserva la altura en interior que publicaba main. Ficus lyrata conserva la altura en interior que publicaba main. Sin
precio propio (datos.DESDE_PLANTAS: según cotización). Salen "más de 30 especies" (cifra sin respaldo: va el conteo real
del catálogo), "entregamos e instalamos… con seguimiento", "todas disponibles" y la lista de químicos que eliminaría cada
planta. Título, descripción y Open Graph como estaban (Etapa 3; la consolidación de plantas de interior también).
"""
import datos
import mensajes_paginas
from contenido import catalogo_datos as cd
from contenido import plantas_comun as pc
from contenido import seo

SITE = datos.SITIO
RUTA = "/plantas-de-interior-tampico"
URL = f"{SITE}{RUTA}"
NOMBRE = "Plantas de interior"
MENSAJE = mensajes_paginas.PLANTAS[RUTA]
DE_INTERIOR = cd.cuenta({"uso": ["interior"]})
TITULO = "Plantas de Interior Tampico: Casa y Oficina | Viveros Terra"
DESCRIPCION = ("Plantas de interior en Tampico: ficus lyrata, monstera, zamioculca, sansevieria y palma areca para casa u oficina. "
               "Entrega en Madero y Altamira. Cotiza.")
META = {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:title", TITULO), ("og:description", DESCRIPCION), ("og:url", URL), ("og:type", "website"))}
ESPECIES = (
    ("ficus-lyrata-pandurata", "Hoja grande de violín: la de diseño moderno para salas y lobbies.", "Hasta 3 m en interior"),
    ("monstera-pinanona", "Hojas grandes y recortadas; tropical y fácil de cuidar.", None),
    ("palma-zz-plant", "Aguanta poca luz y riego cada 2 a 3 semanas.", None),
    ("sansiviera", "Muy resistente: tolera olvidos de riego y el aire acondicionado.", None),
    ("palma-areca", "Palma de interior de tallos múltiples y follaje plumoso para hoteles y oficinas.",
     "Hasta 2 m en interior"),
    ("dracena-compacta", "Follaje denso y de bajo mantenimiento.", None),
)
PREGUNTAS = (
    ("¿Qué plantas de interior son mejores para Tampico?",
     "Las mejores plantas de interior para Tampico son: Ficus Lyrata (diseño moderno), Monstera (tropical), ZZ Plant "
     "(poca luz), Sansiviera (muy resistente), Palma Areca (hoteles y oficinas) y Dracena (bajo mantenimiento). Todas "
     "toleran el aire acondicionado del clima tropical de Tamaulipas."),
    ("¿Qué planta de interior necesita menos cuidado en Tampico?",
     "Las plantas de interior de menor mantenimiento para Tampico son: ZZ Plant (riega cada 2-3 semanas), Sansiviera "
     "(tolera olvidos de riego), Dracena Marginata y Cactus. Son ideales para oficinas y personas con poco tiempo."),
    ("¿Tienen plantas de interior para oficinas y hoteles en Tampico?",
     f"Sí: en el catálogo hay {DE_INTERIOR} especies para interior, para oficinas, hoteles y restaurantes. Para proyectos "
     "comerciales cotizamos por proyecto: escríbenos al 833 326 8008."),
    ("¿Qué planta purifica mejor el aire en interiores de Tampico?",
     "Las que más se piden para eso son Sansiviera, Palma Areca, Clorofito, Ficus Lyrata y ZZ Plant: aguantan el "
     "interior y el aire acondicionado con poco cuidado."),
    ("¿Hacen entrega de plantas de interior en Tampico?",
     "Sí, entregamos plantas de interior en Tampico, Madero y Altamira. Para hoteles, oficinas y restaurantes coordinamos "
     "la entrega por proyecto. Escríbenos al 833 326 8008."),
    pc.PREGUNTA_PAGO,
)

CONTENIDO = {
    "tipo": "plantas",
    "meta": META,
    "migas": pc.migas(NOMBRE),
    "portada": {
        "kicker": "Tampico · Madero · Altamira",
        "pos": "50% 40%",
        "enlaces": ((f"Ver las {DE_INTERIOR} plantas de interior", "/catalogo?uso=interior", "plantas:catalogo"),),
        "lema": "Para el calor, la humedad y el aire acondicionado.",
        "h1": "Plantas de interior para casas y oficinas en Tampico",
        "lede": "Ficus lyrata, monstera, ZZ, sansiviera y más. Te las llevamos a domicilio.",
        "etiqueta": {"codigo": "Interior", "aviso": f"Precios {datos.ANIO}", "nombre": "Plantas de interior",
                     "antes": "Precio", "monto": "Por tamaño", "unidad": datos.SEGUN_COTIZACION.lower(),
                     "nota": "Cotiza con una foto del lugar."},
        "mensaje": MENSAJE,
        "foto": {"src": "/img/portadas/plantas-ornamentales-tampico-viveros-terra-sm.webp",
                 "srcset": ("/img/portadas/plantas-ornamentales-tampico-viveros-terra-sm.webp 560w, "
                            "/img/portadas/plantas-ornamentales-tampico-viveros-terra.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1440, "numero": 1,
                 "alt": "Plantas ornamentales con flor en una jardinera",
                 "lugar": "Plantas ornamentales", "etapa": "Tampico"},
    },
    "especies": {"titulo": "Las más solicitadas en Tampico", "lede": pc.LEDE_FOTOS, "items": ESPECIES},
    "lista": pc.LISTA,
    "garantia": pc.GARANTIA,
    "faq": {"titulo": "Plantas de interior en Tampico: lo que más nos preguntan", "preguntas": PREGUNTAS},
    "guias": {"titulo": "Guías de plantas de interior", "items": (
        ("Plantas de interior para Tampico", "/blog/plantas-interior-tampico"),
        ("Ficus elastica (hule): cuidados", "/blog/ficus-elastica-cuidados-tampico"),
        ("Palma areca en Tampico: cuidados", "/blog/palma-areca-tampico"),
        ("Jardín en macetas para terraza", "/blog/jardin-en-macetas-terraza-tampico-guia"))},
    "relacionados": {"titulo": "Más servicios en Viveros Terra", "items": pc.otras_subcategorias(RUTA)},
    "cierre": {"titulo": "¿Listo para cotizar?",
               "lede": "Dinos si es casa u oficina, cuánta luz tiene y la colonia; te respondemos con precio.",
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
        "Plantas de interior tampico — Todo lo que necesitas saber": (
            "Plantas de interior en Tampico: lo que más nos preguntan"),
    },
    "retirados": {},
    "especies": {
        "reemplazos": {
            "ZZ Plant": ("/plantas-de-interior-tampico", "Palma ZZ Plant"),
        },
        "retirados": {},
    },
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp (alto, con sombra amarilla); el teléfono pasa de botón a enlace de texto; la línea «también» se reparte entre la fila de enlaces y la línea de confianza (promesa con horario, calificación de Google y dato propio); en celular la foto sube a la primera pantalla y la etiqueta muestra una fila (las demás siguen en la sección de precios). Lema nuevo: «Para el calor, la humedad y el aire acondicionado.» (de la entrada).')
