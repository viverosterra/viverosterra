"""Contenido de /politicas (plantilla legal). Conserva la sustancia de main y sus anclas (#envios, #devoluciones,
#garantia-plantas, #mensualidades, #facturacion, #privacidad, #contacto); #garantia-pasto es nueva y copia las condiciones
del protocolo. Números de tools/pasto (fletes, mínimos, mensualidades) y frases de datos.py: nada a mano. Correcciones
frente a main (cada una en el plan, tabla C1–C11): meta "devoluciones (30 días)" contra 7 días del texto, "sin costo" y
"gratis" en plantas, total sin mensualidad, efectivo omitido en formas de pago, embarque "al confirmarse el pago", tiempo
de entrega que sumaba 4 a 7 días, privacidad sin finalidades secundarias, y condiciones de materiales que faltaban."""
import componentes  # noqa: F401  (agrega tools/pasto al sys.path)
import data
import datos
import mensajes_paginas
import mensualidades
from componentes import dinero
from componentes_zonas import porcentaje_plazo
from contenido import seo

SITE = datos.SITIO
URL = f"{SITE}/politicas"
FLETE_MIN, FLETE_MAX = dinero(min(data.ZONAS.values())), dinero(max(data.ZONAS.values()))
ACTUALIZADO = "noviembre 2026"
# SEO fase 0 (mapa de palabras clave, 2026-11-10). La descripción del mapa decía "en 3 a 5 días hábiles" y "devoluciones
# en 30 días": el plazo de entrega no se anuncia (regla del dueño) y la devolución publicada es de 7 días naturales.
TITULO = f"Políticas de Envío, Devolución y Garantías | {datos.NOMBRE}"
DESCRIPCION = (f"Políticas de {datos.NOMBRE}: envíos de pasto sintético a todo México, devoluciones en 7 días naturales, "
               f"garantías de arraigo y facturación {datos.FACTURA}.")
UMBRALES = "; ".join(
    f"desde {dinero(minimo)}, {' o '.join(', '.join(str(p) for p in plazos).rsplit(', ', 1))}"
    f"{' mensualidades' if i == 0 else ''}" for i, (minimo, plazos) in enumerate(sorted(mensualidades.UMBRALES)))
PORCENTAJES = ", ".join(
    f"{p} {'mensualidades ' if i == 0 else ''}+{porcentaje_plazo(p):.1f}%" for i, p in enumerate(mensualidades.PLAZOS))

SECCIONES = (
    {"id": "envios", "titulo": "Política de Envíos", "corto": "Envíos", "bloques": (
        ("p", "<strong>Cobertura:</strong> enviamos pasto sintético a <strong>todo México</strong> por paquetería."),
        ("ul", (
            "<strong>Tiempo de entrega:</strong> sale de Cd. Madero en 1 a 2 días hábiles y llega de 3 a 5 días hábiles "
            "después de confirmar tu pago, según el destino.",
            f"<strong>Costo de envío:</strong> se cobra por cada rollo enviado, según el destino. Como referencia, va de "
            f"aproximadamente {FLETE_MIN} a {FLETE_MAX} por rollo. El costo exacto se confirma con tu código postal antes "
            "de pagar.",
            f"<strong>Compra mínima nacional:</strong> {data.MIN_NACIONAL_M2} m². En nuestro showroom de Tampico se vende "
            f"desde {data.MIN_SHOWROOM_M2} m² sin flete.",
            "<strong>Rastreo:</strong> te compartimos guía de rastreo para que sigas tu pedido.",
            "<strong>Presentación:</strong> el pasto se envía en rollo de 2 m de ancho.",
        )),
        ("h3", "Materiales en Tampico, Madero y Altamira"),
        ("p", datos.CONDICIONES_MATERIALES),
    )},
    {"id": "devoluciones", "titulo": "Política de Devoluciones", "corto": "Devoluciones", "bloques": (
        ("ul", (
            "<strong>Ventana de devolución:</strong> 7 días naturales a partir de la recepción del producto.",
            "<strong>Condición:</strong> producto <strong>nuevo, sin usar, sin cortar</strong> y en su empaque original.",
            "<strong>Cortes a medida:</strong> los pedidos cortados a una medida específica <strong>no admiten "
            "devolución</strong> por tratarse de producto personalizado.",
            "<strong>Costo del envío de retorno:</strong> a cargo del cliente.",
            "<strong>Cargo por reposición (restocking):</strong> 10% del valor del producto.",
            "<strong>Reembolso:</strong> se procesa en un máximo de 15 días una vez recibido y revisado el material, por "
            "el mismo medio de pago.",
            "<strong>Cambios:</strong> aceptamos cambios de producto sujetos a disponibilidad.",
            f"<strong>Cómo solicitarla:</strong> escríbenos por WhatsApp al {datos.TELEFONO_VISIBLE} con tu número de "
            "pedido.",
        )),
        ("p", f"<strong>Dirección de retorno:</strong> {datos.CALLE}, {datos.COLONIA}, Cd. Madero, Tamaulipas, C.P. {datos.CP}."),
    )},
    {"id": "garantia-plantas", "titulo": "Garantía de arraigo de plantas y palmas", "corto": "Garantía de plantas", "bloques": (
        ("p", "Las plantas y palmas que <strong>sembramos nosotros</strong> tienen <strong>30 días de garantía de "
              "arraigo</strong>, contados desde el día de la siembra. Si en ese plazo una planta no prende y se cuidó "
              "como te indicamos, la reponemos."),
        ("p", "<strong>Para que aplique:</strong>"),
        ("ul", (
            "La siembra la hizo el equipo de Viveros Terra, en jardín o en maceta.",
            "Se regó como indica la guía de cuidado que te entregamos con tu pedido.",
            "La planta sigue en el lugar donde la sembramos. Una planta de sol necesita sol y una de sombra necesita "
            "sombra; si cambia de lugar, cambia lo que necesita.",
            "Nos avisas por WhatsApp con fotos dentro de los 30 días.",
        )),
        ("p", "<strong>No la cubre:</strong>"),
        ("ul", (
            "Falta o exceso de riego.",
            "Macetas o plantas movidas a otro lugar, sobre todo de sol a sombra o de sombra a sol.",
            "Daños por mascotas, golpes, niños jugando, poda o productos aplicados sin consultarnos.",
            "Clima fuera de lo normal: nortes fuertes, heladas, granizo o inundación.",
            "Nochebuenas y otras plantas de temporada, aunque las coloquemos nosotros: su cuidado queda fuera de "
            "nuestras manos y su ciclo termina con la temporada.",
            "Plantas que compraste en el vivero y sembraste por tu cuenta. En ese caso te orientamos por WhatsApp para "
            "que prendan.",
        )),
        ("p", "<strong>Cómo funciona:</strong> mándanos fotos de la planta y de dónde está. Si hace falta, vamos a "
              "revisarla. Te decimos el mismo día o al siguiente si aplica, y si aplica te la reponemos. La reposición es "
              "de la misma planta o de una equivalente si no hay existencia."),
    )},
    {"id": "garantia-pasto", "titulo": f"Garantía de arraigo del pasto San Agustín: {datos.ARRAIGO}",
     "corto": "Garantía de pasto", "bloques": (
        ("p", f"{datos.GARANTIA_PASTO.replace(' (ver condiciones)', '')} Aplica cuando:"),
        ("ul", (
            "La instalación fue realizada por el equipo de Viveros Terra.",
            f"Se realizó riego abundante y diario los primeros {datos.ARRAIGO} según el protocolo.",
            "No hubo pisoteo durante los primeros 7 días.",
            "No se aplicaron productos químicos sin autorización previa.",
            "El problema fue reportado antes del día 21.",
        )),
        ("p", f'{datos.PRIMER_RIEGO} Lee el <a href="/protocolo-cuidados-pasto-san-agustin">protocolo de cuidado del pasto</a>.'),
    )},
    {"id": "mensualidades", "titulo": "Pago en mensualidades con tarjeta de crédito", "corto": "Mensualidades", "bloques": (
        ("p", f"Puedes pagar en {' o '.join(', '.join(str(p) for p in mensualidades.PLAZOS).rsplit(', ', 1))} mensualidades "
              "con tarjeta de crédito. El precio en mensualidades es mayor que el de contado; siempre te mostramos el "
              "total y el monto de cada mensualidad antes de enviarte el link de pago."),
        ("ul", (
            "<strong>Contado:</strong> transferencia, efectivo o tarjeta en una sola exhibición. Es el precio más bajo.",
            f"<strong>Plazos por monto de contado:</strong> {UMBRALES}.",
            f"<strong>Total en mensualidades frente a contado:</strong> {PORCENTAJES}.",
            "<strong>Aprobación:</strong> tu banco emisor debe aceptar el plan; el monto de cada mensualidad puede variar "
            "por redondeo del banco.",
            "Aplica a pasto sintético, pasto natural instalado, instalación de pasto sintético, diseño de jardines y "
            "sistemas de riego. No aplica a mantenimiento mensual.",
        )),
    )},
    {"id": "facturacion", "titulo": "Facturación y Pagos", "corto": "Facturación y pagos", "bloques": (
        ("ul", (
            f"{datos.FACTURACION} Emitimos <strong>factura {datos.FACTURA}</strong> para personas físicas y morales.",
            "Formas de pago: transferencia bancaria, efectivo y link de pago (tarjeta de débito o crédito). La tarjeta en "
            "una sola exhibición paga el precio de contado.",
            "<strong>Pasto sintético con envío nacional:</strong> se paga por adelantado, por transferencia, link de pago "
            "con tarjeta o mensualidades. Cuando recibimos tu pago te confirmamos la fecha de embarque por WhatsApp.",
            f"<strong>Demás pedidos y servicios:</strong> {datos.ANTICIPO}",
            "Todos los precios de material incluyen IVA.",
        )),
    )},
    {"id": "privacidad", "titulo": "Aviso de Privacidad", "corto": "Aviso de privacidad", "bloques": (
        ("p", "En Viveros Terra respetamos y protegemos tus datos personales. Este es un resumen; el documento completo es "
              'el <a href="/politica-privacidad">Aviso de Privacidad Integral</a>.'),
        ("ul", (
            "<strong>Datos que recabamos:</strong> nombre, teléfono, correo, dirección y código postal, para cotizar, "
            "procesar y enviar tu pedido y emitir tu factura.",
            "<strong>Uso:</strong> los datos se usan para dar seguimiento a tu compra y atención al cliente y, si no te "
            "das de baja, para enviarte promociones y recordatorios de jardinería. <strong>No vendemos ni compartimos"
            "</strong> tu información con terceros distintos a los que indica el Aviso Integral.",
            "<strong>Conservación:</strong> conservamos tus datos el tiempo necesario para cumplir obligaciones fiscales y "
            "de garantía.",
            f"<strong>Derechos ARCO:</strong> puedes solicitar acceso, rectificación, cancelación u oposición al uso de tus "
            f"datos escribiendo a {datos.CORREO_FORMULARIOS}.",
        )),
    )},
    {"id": "contacto", "titulo": "Contacto", "corto": "Contacto", "bloques": (
        ("ul", (
            f"<strong>WhatsApp / Tel:</strong> {datos.TELEFONO_VISIBLE}",
            f"<strong>Correo:</strong> {datos.CORREO_FORMULARIOS}",
            f"<strong>Showroom:</strong> {datos.CALLE}, {datos.COLONIA}, Cd. Madero, Tamaulipas",
            f"<strong>Horario:</strong> {datos.HORARIO}",
        )),
    )},
)

CONTENIDO = {
    "tipo": "utilidad",
    "meta": {
        "title": TITULO,
        "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
        "og": (("og:type", "article"), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION),
               ("og:image", f"{SITE}/img/pasto-sintetico-residencial-tampico.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "cabeza": {"migas": (("Inicio", "/"), ("Políticas", None)), "kicker": f"Actualizado {ACTUALIZADO}",
               "h1": "Políticas de la Tienda",
               "lede": "Envíos, devoluciones, garantías, mensualidades, privacidad, facturación y contacto de Viveros Terra."},
    "secciones": SECCIONES,
    "cierre": {"titulo": "¿Dudas sobre tu pedido?", "lede": f"Escríbenos: {datos.PROMESA.lower()}.",
               "mensaje": mensajes_paginas.UTILITARIAS["politicas"]},
    "jsonld": ({"@context": "https://schema.org", "@graph": [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": "Políticas", "item": URL}]}]},),
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {
        "En este artículo": "El índice es de la página, con aria-label “En esta página” y sin título visible.",
        "¿Listo para cotizar?": "La columna lateral duplicaba el CTA; queda un solo CTA final con la promesa única.",
    },
    "meta": seo.paridad(TITULO, DESCRIPCION, {"description": (DESCRIPCION, "Decía devoluciones (30 días); la política publicada y la tienda dicen 7 días naturales.")}),
    "jsonld": {},
}
