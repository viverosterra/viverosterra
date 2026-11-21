"""Contenido de las 19 páginas /pasto-sintetico/envio/<ciudad>. Solo datos: la plantilla es plantillas/tienda_guia.py.

Textos de cada ciudad (intro, clima, modelos, preguntas) de tools/pasto/ciudades.py; precios, zonas y fletes de
tools/pasto/data.py; mensualidades de tools/pasto/mensualidades.py. Entrega C del SEO nacional (2026-11-16): sección
«Antes de instalar» propia de cada ciudad (terreno, espacio de ejemplo con la calculadora, ciudades cercanas), textos
fijos más cortos y 8 ciudades nuevas (ciudades.NUEVAS, sin captura de paridad). Título, descripción, canonical, Open Graph,
Product con envío al estado y migas: los que publicaba tools/pasto/ciudad.py. PARIDAD: tests/test_paridad.py.
"""
import math
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
import entidad
import rollos
from ciudades import CIUDADES, NUEVAS
from componentes import dinero
from contenido import seo
from esquema import breadcrumb_schema, envio, product_schema

CLAVES = tuple(x["slug"] for x in CIUDADES)
POR_SLUG = {x["slug"]: x for x in CIUDADES}
SITE = data.SITE
GAL = t.GAL
FOTO = "obra-proyecto-02"  # og:image y Product.image (sin cambio); la foto de la portada cambia por ciudad
# Fotos reales de obras de la colección (data.OBRAS) que se alternan en la portada de las ciudades.
FOTOS_PORTADA = ("obra-proyecto-02", "obra-proyecto-05", "obra-proyecto-03", "obra-proyecto-01")
MIN = data.MIN_NACIONAL_M2
ROLLO = data.ROLLO_M2
TIER2_MIN_M2 = 10  # igual que public/js/tienda-pasto.js
CERCANAS = 3


def _llegada(x):
    return (
        {"titulo": "Confirmas y pagas", "quien": "tu", "cuando": "Al confirmar",
         "texto": f"Transferencia o tarjeta, con factura {datos.FACTURA}."},
        {"titulo": "Sale en rollo", "quien": "nosotros", "cuando": "1 a 2 días hábiles",
         "texto": f"Enrollado y protegido, con guía de rastreo hasta {x['nombre_largo']}."},
        {"titulo": "Revisa al recibir", "quien": "tu", "cuando": "Al recibir",
         "texto": f"Que los metros coincidan con tu pedido; si algo falla, mándanos fotos por WhatsApp."},
    )


def _instalacion(x):
    return (f"Tú o un instalador de {x['nombre']}: nosotros instalamos solo en Tampico, Madero y Altamira. "
            f"{MIN} a {ROLLO} m² se ponen en un día entre dos personas con la "
            '<a href="/blog/como-instalar-pasto-sintetico">guía de instalación</a>.')


def _producto(x, zona, url, desde):
    """Entrega A del SEO nacional (2026-11-16): los 9 modelos reales (los mismos Product de sus fichas, con su Offer y el
    flete solo hacia el estado de la ciudad), en vez de un Product genérico «con envío a …» con AggregateOffer."""
    return {"@type": "ItemList", "name": f"Pasto sintético con envío a {x['nombre_largo']}",
            "numberOfItems": len(data.MODELOS),
            "itemListElement": [{"@type": "ListItem", "position": i,
                                 "item": product_schema(m, with_id=False, envios=[envio(zona, [x["estado"]])])}
                                for i, m in enumerate(data.MODELOS, 1)]}


def _ya_pregunta_el_tiempo(x):
    return any("tarda" in q for q, _a in x["faqs"])


def _preguntas_envio(x, zona):
    """Encabezados en pregunta (spec §3.3, ciudad): costo, tiempo, mínimo, cómo elegir sin muestra e instalación, cada
    uno con los números de la ciudad (flete de su zona, totales de 25 y 50 m² con envío, su modelo recomendado). Si la
    ciudad ya trae su propia pregunta de tiempo en sus FAQ, aquí no se repite."""
    n, largo = x["nombre"], x["nombre_largo"]
    flete = data.ZONAS[zona]
    barato = t.barato()
    total = dict(t.totales(barato, zona))
    rec_slug, rec_razon = x["modelos"][0]
    rec = t.modelo(rec_slug)
    rec_50 = ROLLO * rec["rollo"] + flete
    items = [
        (f"¿Cuánto cuesta el envío a {n}?",
         f"A {largo} el flete es de {dinero(flete)} por rollo de {ROLLO} m² (zona {zona}, "
         f"{data.ZONA_ESTADOS[zona][0]}). Con {rec['nombre']}, el que más recomendamos en {n}, {ROLLO} m² salen en "
         f"{dinero(rec_50)} con envío, {dinero(rec_50 / ROLLO)}/m² puesto. De 51 a 100 m² son dos rollos y "
         f"{dinero(2 * flete)} de flete; nunca va escondido en el precio."),
    ]
    if not _ya_pregunta_el_tiempo(x):
        items.append((f"¿Cuánto tarda en llegar a {n}?",
                      f"Sale de Cd. Madero en 1 a 2 días hábiles y llega a {largo} de 3 a 5 días hábiles después de "
                      "confirmar el pago, con guía de rastreo."))
    items += [
        (f"¿Cuánto es lo mínimo que puedo pedir a {n}?",
         f"{MIN} m², medio rollo: con {barato['nombre']} son {dinero(total[MIN])} con envío a {n}, "
         f"{dinero(total[MIN] / MIN)}/m². Un rollo completo de {ROLLO} m² baja a {dinero(total[ROLLO] / ROLLO)}/m² puesto. "
         f"Los cortes de 2 a 9 m² son solo en el vivero de Cd. Madero."),
        (f"¿Cómo elijo el modelo para {n} sin ver una muestra?",
         f"Sin muestras físicas: cada ficha trae fotos de cerca, altura y peso. Para {n} empieza por {rec['nombre']}: "
         f"{rec_razon[0].lower()}{rec_razon[1:]} Si dudas, mándanos una foto de tu espacio por WhatsApp."),
        (f"¿Quién lo instala en {n}?", _instalacion(x)),
    ]
    return tuple(items)


def _total(m, m2, zona):
    """Material + flete de m2 metros con las reglas del cotizador (tienda-pasto.js: precioM2 y un flete por rollo)."""
    precio = m["rollo"] if m2 >= ROLLO else (m["t2"] if m2 >= TIER2_MIN_M2 else m["t1"])
    return m2 * precio + math.ceil(m2 / ROLLO) * data.ZONAS[zona]


def _rollos_texto(n):
    return "1 rollo" if n == 1 else f"{n} rollos"


def _aviso_rollo(m, m2, total, zona):
    """El mismo aviso del cotizador: si el rollo completo cuesta lo mismo o menos que lo que pides, se dice."""
    if m2 >= ROLLO or _total(m, ROLLO, zona) > total:
        return ""
    return f" Un rollo completo de {ROLLO} m² sale en {dinero(_total(m, ROLLO, zona))}: te conviene más."


def _ejemplo(x, zona):
    """El espacio de ejemplo de la ciudad calculado como la calculadora (rollos.corte) y con su modelo recomendado."""
    espacio, largo, ancho, *modelo = x["ejemplo"]
    r = rollos.corte(largo, ancho)
    rec = t.modelo(modelo[0] if modelo else x["modelos"][0][0])
    total = _total(rec, r["m2"], zona)
    pregunta = f"¿Cuánto pido para {espacio} de {largo} × {ancho} m?"
    respuesta = (f"Son {r['area']} m². Con tiras de 2 m y 10% para cortes pide <b>{r['m2']} m²</b>, que viajan en "
                 f"{_rollos_texto(r['rollos'])}. Con {rec['nombre']} salen en <b>{dinero(total)}</b> con envío a "
                 f"{x['nombre']}.{_aviso_rollo(rec, r['m2'], total, zona)} Prueba tus medidas en la "
                 '<a href="/pasto-sintetico/cuantos-rollos">calculadora de rollos</a>.')
    return pregunta, respuesta


def cercanas(x, n=CERCANAS):
    """Las n ciudades con página más cercanas (distancia aproximada por coordenadas)."""
    lat, lon = x["coords"]
    escala = math.cos(math.radians(lat))

    def distancia(y):
        return math.hypot(y["coords"][0] - lat, (y["coords"][1] - lon) * escala)

    return sorted((y for y in CIUDADES if y["slug"] != x["slug"]), key=distancia)[:n]


def _cercanas(x):
    barato = t.barato()
    enlaces = ", ".join(f'<a href="/pasto-sintetico/envio/{y["slug"]}">{y["nombre"]}</a> '
                        f'(desde ${data.landed_m2(barato, data.zona_de(y["estado"]))}/m²)' for y in cercanas(x))
    return (f"¿Y si estoy en otra ciudad cerca de {x['nombre']}?",
            f"También tienen precio puesto {enlaces}. Los 32 estados están en la "
            '<a href="/pasto-sintetico/cuantos-rollos#envio-por-estado">tabla de envío por estado</a>.')


def _antes_de_instalar(x, zona):
    return ((f"¿Cómo preparo el terreno en {x['nombre']}?", x["terreno"]), _ejemplo(x, zona), _cercanas(x))


# Encuadre de cada foto de portada (object-position; Entrega A de experiencia).
ENCUADRES = {"obra-proyecto-01": "50% 40%", "obra-proyecto-02": "50% 45%", "obra-proyecto-03": "50% 55%",
             "obra-proyecto-05": "50% 50%"}


def _nombre_foto(x):
    return FOTOS_PORTADA[CLAVES.index(x["slug"]) % len(FOTOS_PORTADA)]


def _foto_portada(x):
    nombre = _nombre_foto(x)
    return t.foto_obra(nombre, "(min-width: 1024px) 560px, 100vw", "Pasto de la colección instalado")


def titulo_y_descripcion(x):
    """Título y descripción de la ciudad (SEO fase 0, 2026-11-10): el precio puesto en la ciudad en el título mientras
    quepa en 60 caracteres (si no, «con Envío») y sin plazo de entrega (regla del dueño)."""
    desde = data.landed_m2(t.barato(), data.zona_de(x["estado"]))
    titulo = f"Pasto Sintético en {x['nombre']} desde ${desde}/m² | Viveros Terra"
    if len(titulo) > 60:
        titulo = f"Pasto Sintético en {x['nombre']} con Envío | Viveros Terra"
    descripcion = (f"Pasto sintético con envío a {x['nombre']} desde ${desde}/m² puesto en tu domicilio: 9 modelos de "
                   f"10 a 35 mm, con factura {datos.FACTURA}. Cotiza tu rollo.")
    return titulo, descripcion


def contenido(x):
    zona = data.zona_de(x["estado"])
    url = f"{SITE}/pasto-sintetico/envio/{x['slug']}"
    m = t.barato()
    desde = data.landed_m2(m, zona)
    estado = data.estado_slug(x["estado"])
    titulo, descripcion = titulo_y_descripcion(x)
    mensaje = f"Hola, quiero cotizar pasto sintético con envío a {x['nombre']}.\nMetros aprox.: ___\nModelo: ___"
    return {
        "tipo": "ciudad",
        "preguntas_fijo": {"estado": x["estado"], "ciudad": x["nombre"]},
        "meta": {"title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
                 "canonical": url,
                 "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                        ("og:description", descripcion), ("og:image", f"{SITE}{GAL}/{FOTO}.webp"),
                        ("og:locale", "es_MX")),
                 "twitter": (("twitter:card", "summary_large_image"),)},
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"),
                                      (f"Envío a {x['nombre']}", url)]), _producto(x, zona, url, desde)),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (f"Envío a {x['nombre']}", None)),
        "portada": {
            "kicker": f"Envío a {x['nombre']} · 9 modelos",
            "h1": f'Pasto sintético en {x["nombre"]} <span class="vt-serif">con envío a tu casa</span>',
            "respuesta": (f"Te enviamos el pasto sintético a {x['nombre_largo']}. Desde <b>${desde}/m²</b> ya con envío, "
                          "en rollo de 50 m² con factura."),
            # Precio puesto en la ciudad, en la etiqueta (antes solo iba dentro del párrafo): los mismos datos del cuadro.
            "etiqueta": {"codigo": "Con envío", "aviso": "Con factura", "nombre": m["nombre"],
                         "antes": f"Puesto en {x['nombre']} · desde", "monto": f"${desde}", "unidad": "/m²",
                         "filas": (("Flete por rollo", dinero(data.ZONAS[zona])),)},
            "dato": "9 modelos en existencia",
            "pos": ENCUADRES[_nombre_foto(x)],
            "mensaje": mensaje,
            "href_modelos": f"/pasto-sintetico?estado={estado}#modelos",
            "texto_modelos": "Ver los 9 modelos con precio puesto",
            "foto": _foto_portada(x),
            "datos": ((f"Puesto en {x['nombre']}", f"desde ${desde}/m²", f"Con {m['nombre']}"),
                      ("Flete por rollo", dinero(data.ZONAS[zona]), data.ZONA_ESTADOS[zona][0]),
                      ("Entrega", "3 a 5 días", "Hábiles, con guía de rastreo"),
                      ("Compra mínima", f"{MIN} m²", "Medio rollo"),
                      ("Factura", datos.FACTURA, "Persona física o moral"),
                      ("Vendemos a todo México", f"Desde {datos.SINTETICO_NACIONAL_DESDE}", "Enviamos desde Cd. Madero, Tamps.")),
        },
        "secciones": (
            {"tipo": "totales", "id": "precios", "rotulo": "Precios", "titulo": f"Cuánto cuesta con envío a {x['nombre']}",
             "lede": x["intro"], "modelo": m, "zona": zona, "fila": "Pedir mi total con envío",
             "notas": (f"El flete exacto a {x['nombre_largo']} se confirma con tu código postal antes de pagar.",
                       "Mensualidades con tarjeta de crédito; el total en mensualidades es mayor que el de contado. "
                       f'Calcula tu plan en el <a href="/pasto-sintetico?estado={estado}#cotizador">cotizador</a>.')},
            {"tipo": "preguntas", "id": "envio-dudas", "rotulo": "Antes de comprar",
             "titulo": f"Envío a {x['nombre']}: costo, tiempo y mínimo", "items": _preguntas_envio(x, zona)},
            {"tipo": "modelos", "id": "modelos", "rotulo": "Clima", "titulo": f"El pasto que conviene en {x['nombre']}",
             "lede": x["clima"], "items": x["modelos"], "zona": zona, "lugar": x["nombre"],
             "estado": estado},
            {"tipo": "preguntas", "id": "instalar", "rotulo": "Tu espacio",
             "titulo": f"Antes de instalar en {x['nombre']}", "items": _antes_de_instalar(x, zona)},
            {"tipo": "pasos", "id": "envio", "rotulo": "Envío", "titulo": f"Cómo te llega el pedido a {x['nombre']}",
             "items": _llegada(x)},
            {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": f"Preguntas frecuentes en {x['nombre']}",
             "preguntas": tuple(x["faqs"])},
        ),
        "cierre": {"titulo": f"Cotiza tu pedido a {x['nombre']}",
                   "lede": (f"Elige modelo y metros en la tienda: el precio ya incluye el envío a {x['nombre_largo']}. "
                            f'<a href="/pasto-sintetico?estado={estado}#cotizador">Calcular mi pedido</a>.'),
                   "mensaje": mensaje},
    }


# Entrega A del SEO nacional (2026-11-16): Offer y UnitPriceSpecification vuelven (un Offer por modelo, ver _producto).
M_JSONLD = {}


def paridad(x):
    """La sección "Instálalo tú" pasa a la pregunta de instalación. En la zona B (Monterrey y Veracruz), 12 mensualidades
    sobre $19,998 son 1,666.5: la página decía $1,666 (round() de Python) y el cotizador cobra $1,667 (Math.round);
    desde 2b Python redondea como el JS."""
    reemplazos = {"Instalarlo tú mismo es sencillo": f"¿Quién lo instala en {x['nombre']}?"}
    if data.zona_de(x["estado"]) == "B":
        reemplazos["$1,666"] = "$1,667"
    hero = ("Entrega A de experiencia (2026-11-10), hero de marca: un solo botón de WhatsApp y enlaces de texto; el precio "
            "puesto en la ciudad va en la etiqueta colgada (antes solo en el párrafo); de la entrada salen el plazo de "
            "entrega (sigue en el cuadro de datos y en «¿Cuánto tarda?») y «Tú lo instalas con nuestra guía» (sigue en "
            "«¿Quién lo instala?»); kicker en un renglón.")
    return {"meta": seo.paridad(*titulo_y_descripcion(x)), "reemplazos": reemplazos, "retirados": {}, "jsonld": M_JSONLD,
            "hero": hero}


def pagina(slug):
    if slug in NUEVAS:  # Entrega C (2026-11-16): página nueva, sin captura anterior
        hero = ("Página nueva de la entrega C del SEO nacional (2026-11-16): el mismo hero de marca que las demás ciudades, "
                "con el precio puesto en la ciudad en la etiqueta colgada y un solo botón de WhatsApp.")
        return SimpleNamespace(CONTENIDO=contenido(POR_SLUG[slug]),
                               PARIDAD={"reemplazos": {}, "retirados": {}, "hero": hero})
    return SimpleNamespace(CONTENIDO=contenido(POR_SLUG[slug]), PARIDAD=paridad(POR_SLUG[slug]))
