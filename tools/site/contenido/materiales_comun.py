"""Lo que comparten las cuatro páginas de materiales (Etapa 2f): entrega, pedido por correo, otros materiales, migas,
producto del JSON-LD y motivos de paridad repetidos. Solo datos: la plantilla es tools/site/plantillas/material.py.

Precios solo de datos.PRECIOS (tierra negra $90 el costal y $1,500 el m³; tezontle desde $200 el costal); lo demás —
tierra preparada, camiones, m³ de tezontle, mármol y piedra bola— va "según cotización" (regla del dueño: no se inventa).
Sin plazos de entrega (no están en datos.py), sin existencias ni disponibilidad, sin "gratis"; el pago, con anticipo.
"""
import datos
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
SEGUN = datos.SEGUN_COTIZACION.lower()
TIPO = "material"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
CAMION = f"camión {SEGUN}"

RESUMEN = {
    "/tierra-negra-vegetal-tampico": (f"Costal {dinero(P['tierra_negra_costal'])} · m³ {dinero(P['tierra_negra_m3'])} · "
                                      f"{CAMION}"),
    "/tezontle-rojo-tampico": f"Costal desde {dinero(P['tezontle_costal'])} · m³ y camión de 14 m³ {SEGUN}",
    "/marmol-blanco-tampico": f"Saco de 20 kg {SEGUN} · 3 sacos por m²",
    "/piedra-bola-rio-tampico": f"Chica, mediana y grande · {SEGUN}",
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
    """Recoger en el vivero o a domicilio, costo según la colonia, anticipo y factura. Sin plazo: no está en datos.py."""
    return {
        "titulo": f"¿Cómo te entregamos {material}?",
        "lede": "Lo recoges en el vivero o te lo llevamos. El costo de entrega va en la cotización, antes de que confirmes.",
        "items": (
            {"titulo": "Recoges en el vivero",
             "texto": f"En {datos.DOMICILIO_CORTO} ({datos.REFERENCIA}). {datos.HORARIO}."},
            {"titulo": "Te lo llevamos",
             "texto": (f"A Tampico, Ciudad Madero y Altamira; {datos.ZONAS_POR_PROYECTO}, por proyecto. El costo de "
                       "entrega se cotiza según tu colonia y el volumen.")},
            {"titulo": "Pago y factura", "texto": f"{datos.ANTICIPO} Emitimos factura {datos.FACTURA}."},
        ),
    }


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


def producto(nombre, descripcion, imagen, sku=None, ofertas=None):
    """Product del JSON-LD con la marca de main; las ofertas solo con precios de datos.py y sin "InStock"."""
    nodo = {"@type": "Product", "name": nombre, "description": descripcion,
            "brand": {"@type": "Brand", "name": datos.NOMBRE}, "image": imagen}
    if sku:
        nodo["sku"] = sku
    if ofertas:
        nodo["offers"] = {**ofertas, "priceCurrency": "MXN", "seller": NEGOCIO}
    return nodo


SPEAKABLE = ("#vt-h1", ".vt-portada .vt-lede", ".vt-faq summary")

# Motivos de paridad que se repiten en las cuatro páginas.
MOTIVO_PRECIO = ("No está en datos.PRECIOS: regla del dueño, va “según cotización” y nunca se inventa (pregunta al "
                 "dueño en el plan 2f).")
MOTIVO_LOCALBUSINESS = ("El seller del Product apunta por @id a la entidad única #negocio (el nodo completo vive en la "
                        "home), en vez de un LocalBusiness suelto, como en 2d y 2e.")
MOTIVO_AUTOR = ("Bloque de autor con “+18 años” y “Productor directo” (sin respaldo en datos.py); la entidad y el autor "
                "son de la Etapa 4.")
MOTIVO_PESO_COSTAL = ("Main publicaba dos pesos distintos para el mismo costal: no se publica ninguno hasta que el "
                      "dueño confirme cuánto pesa (pregunta 5 del plan 2f). Las equivalencias de la calculadora "
                      "no cambian.")
MOTIVO_TESTIMONIOS = ("Opiniones sin permiso del dueño: no están en datos.OPINIONES (spec: nunca una opinión sin "
                      "confirmarla). Vuelven si el dueño las confirma.")
