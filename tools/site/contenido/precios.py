"""Contenido de /precios: la lista de precios de todo Viveros Terra. Solo datos: la plantilla es plantillas/precios.py.

Ningún número escrito a mano (aceptación de la hoja de ruta 2g): los precios salen de datos.PRECIOS (renglones en
contenido/lista_precios.py), el sintético por modelo de tools/pasto/data.py y las mensualidades de
tools/pasto/mensualidades.py (la fórmula de vt-mensualidades.js). La respuesta a "¿cuánto cuesta el pasto en rollo en
Tampico?" es datos.RESPUESTA_PRECIO_PASTO, la misma de la home y de pasto en rollo (spec §7.3). Materiales con las
respuestas del dueño (2026-11-08); lo que dejó sin precio va "según cotización": m³ y camión de tezontle y piedra bola.
La fecha de vigencia queda fuera hasta que el dueño la confirme (ni texto ni dateModified). Título, descripción,
canonical y Open Graph como estaban. PARIDAD: tests/test_paridad.py.
"""
import componentes as c  # primero: agrega tools/pasto al sys.path (data y mensualidades)
import data
import datos
import mensajes_paginas
import mensualidades
from contenido import lista_precios as lp

dinero = c.dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/precios"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
IMG = "/img/precios/pasto-rollo-jardin"
SOLO, INSTALADO = dinero(P["pasto_solo_m2"]), dinero(P["pasto_instalado_m2"])
MANTENIMIENTO, DISENO = dinero(P["mantenimiento_mes"]), dinero(P["diseno"])
SINTETICO = dinero(lp.SINTETICO_MIN)
SINT_MIN, SINT_MAX = (dinero(x) for x in P["sintetico_instalado_m2"])
MENSAJE = mensajes_paginas.PRECIOS
COTIZAR = mensajes_paginas.PRECIOS_SECCIONES
TITULO = "Precios de jardinería en Tampico 2026: pasto, diseño y mantenimiento | Viveros Terra"
DESCRIPCION = (f"Pasto San Agustín {SOLO}/m² o instalado desde {INSTALADO}/m², mantenimiento desde {MANTENIMIENTO}/mes, "
               f"diseño desde {DISENO} y pasto sintético desde {SINTETICO}/m². Precios con IVA en Tampico, Madero y "
               "Altamira.")
ENLACES_FAQ = {
    "sintetico": ' Ve los <a href="/pasto-sintetico">9 modelos con precio</a>.',
    "garantia": ' Lee las <a href="/politicas#garantia-plantas">condiciones de la garantía</a>.',
}

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Los precios incluyen IVA?",
     f"Sí. Todos los precios de esta página incluyen IVA. Damos factura {datos.FACTURA} a persona física o moral y "
     f"tenemos registro REPSE {datos.REPSE} para contratos con empresas."),
    ("¿Por qué algunos precios dicen «desde»?",
     "Porque el total depende de los metros, del estado del terreno y del acceso a la obra. En la visita medimos y te "
     f"damos el precio cerrado antes de empezar. {datos.VISITA_COSTO} Lo que dice «según cotización» depende de la "
     "medida, la cantidad o el lugar de entrega: te lo cotizamos por WhatsApp."),
    ("¿Cuánto cuesta el pasto sintético en Tampico?",
     f"El material cuesta desde {SINTETICO}/m² en rollo completo y el pasto instalado de {SINT_MIN} a {SINT_MAX}/m² "
     "según el modelo, con material y colocación. La preparación del terreno se cotiza aparte." + ENLACES_FAQ["sintetico"]),
    ("¿Las plantas y palmas tienen garantía?",
     f"Sí: {datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} No cubre falta de riego, cambio de lugar, daños "
     "por mascotas ni clima extremo." + ENLACES_FAQ["garantia"]),
    ("¿Cada cuánto cambian estos precios?",
     "Revisamos la lista cada temporada. Si algo cambió, vale el precio que te confirmemos por WhatsApp."),
)


def _oferta(nombre, precio, ruta, unidad=None, desde=False, descripcion=None):
    """Offer del catálogo con el seller por @id a #negocio; con unidad, su UnitPriceSpecification. Si es "desde" el
    precio va solo como minPrice (como materiales_comun.oferta: un price exacto diría otra cosa), así que "desde" pide
    unidad. Solo precios de datos.py: nunca InStock."""
    o = {"@type": "Offer", "name": nombre}
    if not desde:
        o["price"] = str(precio)
    if descripcion:
        o["description"] = descripcion
    o.update({"priceCurrency": "MXN", "url": f"{SITE}{ruta}", "seller": NEGOCIO})
    if unidad:
        spec = {"@type": "UnitPriceSpecification", "priceCurrency": "MXN", "unitText": unidad}
        spec.update({"minPrice": precio} if desde else {"price": str(precio)})
        o["priceSpecification"] = spec
    return o


CATALOGO = {
    "@type": "OfferCatalog", "@id": f"{URL}#lista", "name": "Lista de precios de Viveros Terra",
    "itemListElement": [
        _oferta("Pasto San Agustín en rollo, solo el pasto", P["pasto_solo_m2"], "/pasto-en-rollo-tampico", "m²"),
        _oferta("Pasto San Agustín instalado", P["pasto_instalado_m2"], "/pasto-en-rollo-tampico", "m²", desde=True),
        _oferta(f"Pasto San Agustín al mayoreo, desde {P['pasto_mayoreo_minimo_m2']} m²", P["pasto_mayoreo_m2"],
                "/mayoreo-pasto-tampico", "m²", desde=True),
        _oferta("Mantenimiento de jardín mensual", P["mantenimiento_mes"], "/mantenimiento-jardines-tampico", "mes",
                desde=True),
        _oferta("Diseño de jardín, Plan Terra Esencial", P["diseno"], "/diseno-jardines-tampico"),
        _oferta("Diseño de jardín, Plan Terra Completo", P["diseno_completo"], "/diseno-jardines-tampico"),
        _oferta("Diseño de jardín, Plan Terra Premium", P["diseno_premium"], "/diseno-jardines-tampico", "proyecto",
                desde=True),
        _oferta("Pasto sintético, material en rollo", lp.SINTETICO_MIN, "/pasto-sintetico", "m²", desde=True),
        _oferta("Tierra negra vegetal, costal", P["tierra_negra_costal"], "/tierra-negra-vegetal-tampico"),
        _oferta("Tezontle rojo, costal", P["tezontle_costal"], "/tezontle-rojo-tampico", "costal", desde=True),
        _oferta("Mármol blanco, saco", P["marmol_saco"], "/marmol-blanco-tampico", descripcion=datos.MARMOL_CONDICION),
        _oferta("Palmas, tamaño chico", P["palma_desde"], "/palmas-tropicales-tampico", "pieza", desde=True),
    ],
}

CONTENIDO = {
    "tipo": "precios",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large",
        "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", f"{SITE}{IMG}.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "migas": (("Inicio", "/"), ("Precios", None)),
    "portada": {
        "compacta": True,
        "kicker": f"Lista de precios {datos.ANIO} · Tampico, Madero y Altamira",
        "h1": 'Precios de jardinería en Tampico <span class="vt-serif">2026, con IVA</span>',
        "lede": (f"En Tampico, Madero y Altamira, el pasto San Agustín cuesta {SOLO}/m² solo el pasto y desde "
                 f"{INSTALADO}/m² instalado. El mantenimiento de jardín cuesta desde {MANTENIMIENTO}/mes, el diseño desde "
                 f"{DISENO} y el pasto sintético desde {SINTETICO}/m²."),
        "etiqueta": {"codigo": f"Lista · {datos.ANIO}", "aviso": "Con IVA", "nombre": "Pasto San Agustín",
                     "antes": "solo el pasto", "monto": SOLO, "unidad": "/m²",
                     "filas": (("Instalado", f"desde {INSTALADO}/m²"), ("Mantenimiento", f"desde {MANTENIMIENTO}/mes"),
                               ("Pasto sintético", f"desde {SINTETICO}/m²"))},
        "mensaje": MENSAJE,
        "tambien": (f'<a href="#pasto">Ver la lista</a> · <a href="#mensualidades">Hasta {max(mensualidades.PLAZOS)} '
                    f'mensualidades con tarjeta · ver plazos</a> · factura {datos.FACTURA} · REPSE {datos.REPSE}'),
        "foto": {"src": f"{IMG}-sm.webp", "srcset": f"{IMG}-sm.webp 560w, {IMG}.webp 960w",
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1185, "numero": 1,
                 "alt": "Trabajador de Viveros Terra descargando pasto San Agustín en rollo de la camioneta",
                 "lugar": "Pasto San Agustín en rollo", "etapa": "Recién cortado"},
    },
    "saltos": (("Pasto", "pasto"), ("Servicios", "servicios"), ("Sintético", "sintetico"), ("Materiales", "materiales"),
               ("Plantas", "plantas"), ("Mensualidades", "mensualidades"), ("Garantías", "garantias")),
    "secciones": (
        {"id": "pasto", "rotulo": "Pasto natural", "titulo": 'Pasto San Agustín <span class="vt-serif">en rollo</span>',
         "filas": lp.PASTO, "concepto": "Producto", "caption": f"Precios {datos.ANIO} con IVA.",
         "cotizar": ("Cotizar pasto por WhatsApp", COTIZAR["pasto"]),
         "nota": ("Solo el pasto: recoges en el vivero o se cobra la entrega según tu colonia. "
                  '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de riego y garantía</a>.')},
        {"id": "servicios", "rotulo": "Servicios", "titulo": 'Mantenimiento, diseño <span class="vt-serif">y riego</span>',
         "filas": lp.SERVICIOS, "concepto": "Servicio", "caption": f"Precios {datos.ANIO} con IVA.",
         "cotizar": ("Cotizar un servicio por WhatsApp", COTIZAR["servicios"]),
         "nota": f"Contratos con empresas con factura y REPSE {datos.REPSE}."},
        {"id": "sintetico", "rotulo": "Pasto sintético",
         "titulo": 'Pasto sintético <span class="vt-serif">por modelo</span>', "modelos": True,
         "lede": (f"Material por m² según cuánto compres. Instalado en Tampico, Madero y Altamira de {SINT_MIN} a "
                  f"{SINT_MAX}/m² con material y colocación."),
         "cotizar": ("Cotizar pasto sintético por WhatsApp", COTIZAR["sintetico"]),
         "nota": (f"Cortes de {data.MIN_SHOWROOM_M2} a 9 m² solo en el showroom. Envío a todo México desde "
                  f"{data.MIN_NACIONAL_M2} m²; el flete se cobra por rollo según tu estado. "
                  '<a href="/pasto-sintetico">Ver la tienda</a> · <a href="/pasto-sintetico-tampico">Instalación en '
                  "Tampico</a>")},
        {"id": "materiales", "rotulo": "Materiales", "titulo": 'Tierra, tezontle <span class="vt-serif">y piedra</span>',
         "filas": lp.MATERIALES, "concepto": "Material", "caption": f"Precios {datos.ANIO} con IVA.",
         "cotizar": ("Cotizar materiales por WhatsApp", COTIZAR["materiales"]),
         "nota": ("Recoges en el vivero de Cd. Madero o te lo llevamos en Tampico, Madero y Altamira. "
                  f"{datos.CONDICIONES_MATERIALES}")},
        {"id": "plantas", "rotulo": "Vivero", "titulo": 'Plantas, palmas <span class="vt-serif">y árboles</span>',
         "filas": lp.PLANTAS, "concepto": "Planta", "caption": f"Precios {datos.ANIO} con IVA.",
         "cotizar": ("Cotizar plantas por WhatsApp", COTIZAR["plantas"]),
         "nota": ('Arma tu lista en el <a href="/catalogo">catálogo</a> y mándala por WhatsApp. '
                  f"{datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} "
                  '<a href="/politicas#garantia-plantas">Ver condiciones</a>.')},
    ),
    "pago": {
        "titulo": 'Mensualidades <span class="vt-serif">con tarjeta</span>',
        "lede": ("El contado (transferencia, efectivo o tarjeta en una sola exhibición) es el precio más bajo. Con "
                 "tarjeta de crédito puedes pagar en 3, 6, 9 o 12 mensualidades; el total es mayor que el de contado y "
                 "siempre te lo mostramos antes de enviarte el link de pago."),
        "anticipo": datos.ANTICIPO,
        "nota": ("Aplica a pasto sintético, pasto natural instalado, instalación de pasto sintético, diseño de jardines y "
                 "sistemas de riego. No aplica a mantenimiento mensual. Tu banco emisor debe aceptar el plan. "
                 '<a href="/politicas#mensualidades">Ver condiciones</a>.'),
        "titulo_sim": "Calcula tu mensualidad",
        # Monto de ejemplo: el mínimo con el que aplican los 4 plazos (el simulador muestra todos).
        "sim": {"servicio": "mi jardín", "monto": mensualidades.minimo_de(12)},
    },
    "garantias": {
        "titulo": 'Garantías <span class="vt-serif">y condiciones</span>',
        "items": (
            {"id": "garantia-pasto", "titulo": f"Pasto San Agustín: arraigo de {datos.ARRAIGO}",
             "texto": datos.GARANTIA_PASTO.replace(" (ver condiciones)", ""),
             "enlace": ("Protocolo de riego y condiciones", "/protocolo-cuidados-pasto-san-agustin")},
            {"id": "garantia-plantas", "titulo": "Plantas y palmas: 30 días",
             "texto": (f"{datos.GARANTIA_PLANTAS.replace(' (ver condiciones)', '')} No cubre falta de riego, cambio de "
                       "lugar, daños por mascotas ni clima extremo."),
             "enlace": ("Condiciones de la garantía de plantas", "/politicas#garantia-plantas")},
        ),
    },
    "faq": {"titulo": 'Preguntas sobre <span class="vt-serif">precios</span>', "preguntas": PREGUNTAS},
    "cierre": {"titulo": '¿Quieres el precio exacto <span class="vt-serif">de tu jardín?</span>',
               "lede": ("Mándanos tu colonia, los metros aproximados y una foto del espacio. "
                        f"{datos.PROMESA} y, si hace falta, agendamos una visita para medir. {datos.VISITA_COSTO}"),
               "mensaje": ("Hola, quiero el precio exacto de mi jardín.\nColonia: ___\nMetros aprox.: ___\n"
                           "Les mando foto del espacio.")},
    "jsonld": {
        "migas": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Precios", "item": URL}]},
        "pagina": {"@type": "WebPage", "@id": URL, "url": URL, "name": "Precios de jardinería en Tampico 2026",
                   "about": NEGOCIO, "mainEntity": {"@id": f"{URL}#lista"}},
        "catalogo": CATALOGO,
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
    "jsonld": {},
}
