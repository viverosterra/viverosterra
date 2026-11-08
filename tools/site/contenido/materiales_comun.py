"""Lo que comparten las cuatro páginas de materiales (Etapa 2f): entrega, pedido por correo, otros materiales, migas,
producto del JSON-LD y motivos de paridad repetidos. Solo datos: la plantilla es tools/site/plantillas/material.py.

Precios solo de datos.PRECIOS (respuestas del dueño, 2026-11-08): tierra negra $90 el costal, $1,500 el m³, preparada
$100 y camiones de 5, 8 y 14 m³ a $3,500, $5,200 y $8,000; tezontle desde $200 el costal; mármol $250 el saco, IVA
incluido y sujeto a disponibilidad. El m³ y el camión de tezontle y la piedra bola (a granel, sin medidas) van "según
cotización" (regla del dueño: no se inventa). Sin mínimo de compra, la entrega se cobra por viaje y todo se factura
(datos.CONDICIONES_MATERIALES). Sin plazos de entrega, sin existencias, sin "gratis"; el pago, con anticipo.
"""
import datos
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
SEGUN = datos.SEGUN_COTIZACION.lower()
TIPO = "material"
NEGOCIO = {"@id": f"{SITE}/#negocio"}

# Medidas: una sola fuente para las cuatro páginas (comparativas, etiquetas y usos). La piedra bola se vende a granel,
# sin medidas (dueño, 2026-11-08): no tiene medida publicada.
PIEDRA_BOLA_VENTA = datos.PIEDRA_BOLA_VENTA
TEZONTLE_MEDIDA = "2 a 5 cm"
MARMOL_MEDIDA = "1 a 3 cm"
# Capa de tezontle para control de maleza: la de la calculadora ("Control de maleza (6 cm)" e "intenso (8 cm)").
TEZONTLE_CAPA_MALEZA = "6 a 8 cm"
# El dueño no tiene el peso de los costales (2026-11-08): el "≈ 20 kg" del saco de mármol queda solo en la calculadora
# (componentes_materiales: sacos → kg aproximados). Pregunta pendiente al dueño.
MARMOL_SACO = dinero(P["marmol_saco"])
CAMIONES_TIERRA = " · ".join(f"{m3} m³ {dinero(precio)}" for m3, precio in datos.TIERRA_CAMIONES)

RESUMEN = {
    "/tierra-negra-vegetal-tampico": (f"Costal {dinero(P['tierra_negra_costal'])} · m³ {dinero(P['tierra_negra_m3'])} · "
                                      f"camión de {datos.TIERRA_CAMIONES[0][0]} m³ {dinero(datos.TIERRA_CAMIONES[0][1])}"),
    "/tezontle-rojo-tampico": f"Costal desde {dinero(P['tezontle_costal'])} · m³ y camión de 14 m³ {SEGUN}",
    "/marmol-blanco-tampico": f"Saco {MARMOL_SACO} · 3 sacos por m²",
    "/piedra-bola-rio-tampico": f"A granel · {SEGUN}",
}
NOMBRES = {
    "/tierra-negra-vegetal-tampico": "Tierra negra vegetal",
    "/tezontle-rojo-tampico": "Tezontle rojo",
    "/marmol-blanco-tampico": "Mármol blanco",
    "/piedra-bola-rio-tampico": "Piedra bola de río",
}
# Miniaturas que main ponía en "Otros materiales" (mármol y piedra bola): se quedan donde estaban, sin agrandarse.
MINIATURAS = {
    "/tezontle-rojo-tampico": {"src": "/img/tezontle-rojo-jardin-tampico-sendero.webp", "ancho": 194, "alto": 259},
    "/tierra-negra-vegetal-tampico": {"src": "/img/tierra-negra-camion-volteo-tampico.webp", "ancho": 821, "alto": 471},
}


def otros(ruta, orden, con_miniatura=False):
    """Los otros materiales en el orden de main, cada uno con su resumen de precios de datos.py."""
    return tuple({"titulo": NOMBRES[r], "href": r, "texto": RESUMEN[r],
                  **({"img": MINIATURAS[r]} if con_miniatura and r in MINIATURAS else {})}
                 for r in orden if r != ruta)


def entrega(material):
    """Recoger en el vivero o a domicilio (se cobra por viaje según la colonia), sin mínimo de compra, anticipo y
    factura en todas las compras (datos.CONDICIONES_MATERIALES). Sin plazo: no está en datos.py."""
    return {
        "titulo": f"¿Cómo te entregamos {material}?",
        "lede": f"Lo recoges en el vivero o te lo llevamos. {datos.CONDICIONES_MATERIALES}",
        "items": (
            {"titulo": "Recoges en el vivero",
             "texto": f"En {datos.DOMICILIO_CORTO} ({datos.REFERENCIA}). {datos.HORARIO}."},
            {"titulo": "Te lo llevamos",
             "texto": (f"A Tampico, Ciudad Madero y Altamira; {datos.ZONAS_POR_PROYECTO}, por proyecto. "
                       f"{datos.ENTREGA_COBRO} Te decimos el costo antes de que confirmes.")},
            {"titulo": "Pago y factura",
             "texto": f"{datos.SIN_MINIMO} {datos.ANTICIPO} {datos.FACTURACION} Emitimos factura {datos.FACTURA}."},
        ),
    }


def pregunta_condiciones(material, pregunta=None):
    """Pregunta frecuente de las cuatro páginas con las condiciones del dueño: sin mínimo, entrega por viaje y factura.
    `pregunta` conserva la de main donde ya existía (tierra negra: "¿Dan factura CFDI…?")."""
    return (pregunta or f"¿Hay compra mínima de {material}? ¿Dan factura?",
            f"{datos.FACTURACION} Emitimos factura {datos.FACTURA}: pídela al cotizar con tu RFC y datos fiscales. "
            f"{datos.SIN_MINIMO} {datos.ENTREGA_COBRO}")


def pedido(ejemplo):
    return {
        "titulo": "Escríbenos para cotizar",
        "lede": (f"Si prefieres el correo, mándanos tu pedido y te respondemos en horario de atención ({datos.HORARIO}). "
                 f'También puedes llamar al <a href="tel:{datos.TELEFONO_TEL}" data-cta="material:cuerpo">'
                 f"{datos.TELEFONO_VISIBLE}</a>."),
        "ejemplo": ejemplo,
        "aviso": 'Usamos tus datos solo para responder tu pedido. <a href="/politica-privacidad">Aviso de privacidad</a>.',
    }


def migas(ruta, nombre):
    """Migas visibles y su BreadcrumbList: Inicio › el material (como publicaba main)."""
    visibles = (("Inicio", "/"), (nombre, None))
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": nombre, "item": f"{SITE}{ruta}"}]}
    return visibles, ld


def producto(nombre, descripcion, imagen, sku=None, ofertas=()):
    """Product del JSON-LD con la marca de main y sus ofertas (oferta()). Solo para lo que tiene precio en datos.py:
    sin precio no hay Product (mármol y piedra bola), así no queda un producto sin oferta."""
    nodo = {"@type": "Product", "name": nombre, "description": descripcion,
            "brand": {"@type": "Brand", "name": datos.NOMBRE}, "image": imagen}
    if sku:
        nodo["sku"] = sku
    nodo["offers"] = ofertas[0] if len(ofertas) == 1 else list(ofertas)
    return nodo


def oferta(url, unidad, precio=None, desde=None, nombre=None):
    """Offer con su precio por unidad (UnitPriceSpecification) de datos.py: precio exacto (también como price del Offer)
    o, si es "desde", minPrice. Sin "InStock" (no hay dato de existencias) y con el seller por @id a #negocio."""
    spec = {"@type": "UnitPriceSpecification", "priceCurrency": "MXN", "unitText": unidad}
    spec.update({"price": precio} if desde is None else {"minPrice": desde})
    nodo = {"@type": "Offer", "url": url, "priceCurrency": "MXN"}
    if nombre:
        nodo["name"] = nombre
    if desde is None:
        nodo["price"] = precio
    return {**nodo, "priceSpecification": spec, "seller": NEGOCIO}


SPEAKABLE = ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq summary")

# Motivos de paridad que se repiten en las cuatro páginas.
MOTIVO_PRECIO = ("No está en datos.PRECIOS: el dueño lo dejó “según cotización” (respuestas del 2026-11-08) y nunca "
                 "se inventa.")
MOTIVO_SIN_PRODUCTO = ("Sin precio en datos.py no hay oferta, y un Product sin oferta no sirve: la página queda como "
                       "WebPage ligada a #negocio (el dueño la dejó según cotización, 2026-11-08).")
MOTIVO_LOCALBUSINESS = ("El seller del Product apunta por @id a la entidad única #negocio (el nodo completo vive en la "
                        "home), en vez de un LocalBusiness suelto, como en 2d y 2e.")
MOTIVO_AUTOR = ("Bloque de autor con “+18 años” y “Productor directo” (sin respaldo en datos.py); la entidad y el autor "
                "son de la Etapa 4.")
MOTIVO_PESO_COSTAL = ("Main publicaba dos pesos distintos para el mismo costal y el dueño no tiene el peso de los "
                      "costales (2026-11-08): no se publica ninguno. Las equivalencias de la calculadora no cambian.")
MOTIVO_SIN_MEDIDAS = ("La piedra bola se vende a granel, no por medidas (respuesta del dueño, 2026-11-08): no se "
                      "publican chica, mediana ni grande.")
