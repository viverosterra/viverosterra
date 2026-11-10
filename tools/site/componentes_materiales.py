"""Componentes de las páginas de materiales (Etapa 2f): calculadora de cantidad, tabla de presentaciones con precio o
"según cotización", otros materiales, portada sin foto o con foto apaisada, cierre con la foto de fondo de main y el
formulario de pedido por correo. Funciones puras, como componentes.py (que ya pasa de 800 renglones).

La calculadora es la de main línea por línea (calcularTierra, calcularTezontle y calcularMarmol, incluidos sus
redondeos): calculo() y textos() dan lo mismo que public/js/vt-materiales.js en los casos congelados de main
(public/js/tests/casos-materiales.json; tests/test_materiales_paridad.py y vt-materiales.test.js). Piedra bola no tenía
calculadora: la suya multiplica el área por los kg por m² que publicaba su propia pregunta frecuente (120 a 150 kg por m²
con capa de 8 a 10 cm; se vende a granel, sin medidas). Los precios salen de datos.PRECIOS; lo que no está ahí va "según
cotización".
"""
import json
import math
import re

import componentes as c
import datos
from partials import WA_GLIFO, esc

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
AREA_MAXIMA = 100_000  # m²; más que esto no es un jardín: la calculadora vuelve al mensaje de la página
CIERRE_MENSAJE = "¿Me pueden dar precio de entrega a domicilio en Tampico, Madero o Altamira?"
COLONIA = "Colonia de entrega: ___"  # como en el mensaje de cada página: la colonia decide el costo de entrega
# Camiones de tierra negra de datos.TIERRA_CAMIONES (5, 8 y 14 m³). Main sugería "Camión volteo 8m³+ (~desde $5,000)"
# arriba de 7 m³; el "desde $5,000" no lo confirmó el dueño: se sugiere el camión de la tabla donde cabe la cantidad.
CAMIONES_TIERRA = datos.TIERRA_CAMIONES


def camion_tierra(m3):
    """Camión sugerido para m³ de tierra negra (más de 7, el tramo "camion" de main): el de 8 m³, el de 14 o, si no
    cabe en uno, camiones de 14 m³ con su precio de datos.py."""
    for capacidad, precio in CAMIONES_TIERRA[1:]:
        if m3 <= capacidad:
            return f"Camión volteo de {capacidad} m³ ({c.dinero(precio)})"
    capacidad, precio = CAMIONES_TIERRA[-1]
    return f"{miles(math.ceil(m3 / capacidad))} camiones volteo de {capacidad} m³ ({c.dinero(precio)} c/u)"

# clave → factores de main, precios de datos.py, texto del mensaje, capas (valor, texto) y la capa elegida al cargar.
# Los textos de las capas de tezontle son los de main tal cual: van en el mensaje ("Uso: …").
CALCULADORAS = {
    "tierra-negra": {
        "texto": "tierra negra vegetal", "costal_m3": 0.035,
        "precio_costal": P["tierra_negra_costal"], "precio_m3": P["tierra_negra_m3"],
        "camiones": [list(x) for x in datos.TIERRA_CAMIONES[1:]],
        "etiqueta_capa": "Grosor de la capa", "elegida": "0.08",
        "capas": (("0.05", "5 cm · mejora superficial"), ("0.08", "8 cm · preparación para pasto (recomendado)"),
                  ("0.10", "10 cm · preparación profunda"), ("0.15", "15 cm · terreno muy pobre")),
        "cta": "cotizarCalculado",
    },
    "tezontle": {
        "texto": "tezontle rojo", "costal_m3": 0.027, "camion_m3": 14,
        "etiqueta_capa": "¿Para qué lo usas?", "elegida": "0.10",
        "capas": (("0.06", "Control de maleza (6 cm)"), ("0.08", "Control de maleza intenso (8 cm)"),
                  ("0.10", "Senderos transitables (10 cm)"), ("0.05", "Decorativo/arriates (5 cm)"),
                  ("0.04", "Capa en macetas (4 cm)")),
        "cta": "cotizarTezontle",
    },
    "marmol": {
        "texto": "mármol blanco decorativo", "kg_saco": 20, "precio_saco": P["marmol_saco"],
        "etiqueta_capa": "Grosor de la capa", "elegida": "4",
        "capas": (("3", "3 cm · decorativo o macetas"), ("4", "4 cm · arriates (recomendado)"),
                  ("5", "5 cm · senderos o alberca"), ("6", "6 cm · alta densidad o tráfico")),
        "cta": "cotizarMarmol",
    },
    "piedra-bola": {
        "texto": "piedra bola de río", "kg_m2": (120, 150), "capa_texto": "8 a 10 cm",
        "cta": "cotizarPiedra",
    },
}
# Lo que lee vt-materiales.js en data-material: sin textos de la página ni capas (esas van en el <select>).
PARA_JS = ("costal_m3", "camion_m3", "precio_costal", "precio_m3", "camiones", "kg_saco", "precio_saco", "kg_m2",
           "capa_texto", "texto")


def numero_js(x):
    """Como String(x) de JavaScript para los números de estas calculadoras: 8.0 → "8", 0.1 → "0.1"."""
    x = float(x)
    return str(int(x)) if x.is_integer() else repr(x)


_MILES_RE = re.compile(r"\B(?=(\d{3})+(?!\d))")


def miles(x):
    """Como miles() de vt-materiales.js: "3750" → "3,750" y 1250.5 → "1,250.5" (separa miles sin redondear)."""
    entero, punto, decimales = numero_js(x).partition(".")
    return _MILES_RE.sub(",", entero) + (punto + decimales if punto else "")


def leer_area(texto):
    """m² escritos por el visitante (como leerArea de vt-materiales.js y leer_m2 de las empresas): "1,200" y "1200" son
    1200, "12,5" es 12.5 y "80 m²" es 80. Devuelve 0 si no es un número mayor que 0 y hasta AREA_MAXIMA."""
    n = c.leer_m2(texto)
    return n if n <= AREA_MAXIMA else 0


def _m3(area, capa):
    return math.ceil(area * capa * 10) / 10


def calculo(clave, area, capa=0):
    """Resultado de la calculadora de main para `area` m² con la capa `capa` (m en tierra y tezontle, cm en mármol)."""
    cfg = CALCULADORAS[clave]
    if clave == "tierra-negra":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1.5 else "m3" if m3 <= 7 else "camion"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo}
    if clave == "tezontle":
        m3 = _m3(area, capa)
        tramo = "costales" if m3 <= 1 else "m3" if m3 <= 5 else "camion" if m3 <= cfg["camion_m3"] else "camiones"
        return {"m3": m3, "costales": math.ceil(m3 / cfg["costal_m3"]), "tramo": tramo,
                "camiones": math.ceil(m3 / cfg["camion_m3"])}
    if clave == "marmol":
        por_m2 = 3 if capa <= 4 else 4 if capa <= 5 else 5
        sacos = math.ceil(area * por_m2)
        return {"sacos": sacos, "kg": sacos * cfg["kg_saco"], "por_m2": por_m2, "total": sacos * cfg["precio_saco"]}
    minimo, maximo = cfg["kg_m2"]
    return {"kg": (c.redondear(area * minimo), c.redondear(area * maximo))}


def _mensaje(cfg, titulo, lineas):
    return "\n".join((f"Hola, quiero cotizar {cfg['texto']}.", "", titulo, *lineas, COLONIA, "", CIERRE_MENSAJE))


def textos(clave, area, capa, r, uso=""):
    """Lo que muestra la etiqueta y el mensaje de WhatsApp. Iguales a los de main salvo lo que pide el dueño o la
    revisión: el camión de tierra negra con su tamaño y precio de datos.py en vez del "desde $5,000" (camion_tierra),
    miles con coma ("3,750 sacos"), la capa en el mensaje de tierra negra y, en los cuatro, la colonia por llenar y la
    misma pregunta de cierre (sin "confirmar disponibilidad"). El mármol vuelve a dar el total a $250 el saco
    (datos.PRECIOS). Los números son los mismos de main."""
    cfg = CALCULADORAS[clave]
    a = miles(area)
    if clave in ("tierra-negra", "tezontle"):
        m3, costales = miles(r["m3"]), miles(r["costales"])
        if clave == "tierra-negra":
            presentacion = (f"{costales} costales ({c.dinero(r['costales'] * cfg['precio_costal'])})"
                            if r["tramo"] == "costales" else
                            f"{m3} m³ suelto (~{c.dinero(r['m3'] * cfg['precio_m3'])})" if r["tramo"] == "m3" else
                            camion_tierra(r["m3"]))
            equivalente = f"{costales} costales" if r["tramo"] == "costales" else f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Capa: {round(capa * 100)} cm", f"Cantidad: {m3} m³")
        else:
            presentacion = {"costales": f"{costales} costales", "m3": f"{m3} m³ suelto", "camion": "Camión 14 m³",
                            "camiones": f"{miles(r['camiones'])} camiones 14 m³"}[r["tramo"]]
            equivalente = f"~{costales} costales"
            lineas = (f"Área: {a} m²", f"Uso: {uso}", f"Cantidad: {m3} m³")
        return {"cantidad": f"{m3} m³", "presentacion": presentacion, "equivalente": equivalente,
                "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}
    if clave == "marmol":
        sacos, g, total = miles(r["sacos"]), numero_js(capa), c.dinero(r["total"])
        precio = f" A {c.dinero(cfg['precio_saco'])} c/u."
        nota = (f"{sacos} sacos cubren {a} m² con capa de {g} cm.{precio}" if capa <= 4
                else f"{sacos} sacos para {a} m² con capa de {g} cm (alta densidad).{precio}")
        lineas = (f"Área: {a} m²", f"Capa: {g} cm", f"Cantidad: {sacos} sacos", f"Precio estimado: {total}")
        return {"cantidad": f"{sacos} sacos", "total": total, "peso": f"{miles(r['kg'])} kg", "nota": nota,
                "mensaje": _mensaje(cfg, "Datos de mi proyecto:", lineas)}
    minimo, maximo = r["kg"]
    cantidad = f"{miles(minimo)} a {miles(maximo)} kg"
    lineas = (f"Área: {a} m²", f"Capa: {cfg['capa_texto']}", f"Cantidad aprox.: {cantidad}")
    return {"cantidad": cantidad, "mensaje": _mensaje(cfg, "Resultado de la calculadora:", lineas)}


def ejemplo(clave, area, capa=0):
    """Cantidad para el texto de una pregunta frecuente ("8 m³", "150 sacos"): sale de la misma calculadora."""
    capa = float(capa)
    return textos(clave, area, capa, calculo(clave, area, capa))["cantidad"]


def datos_js(clave):
    cfg = CALCULADORAS[clave]
    return {"clave": clave, **{k: cfg[k] for k in PARA_JS if k in cfg}}


VACIO = {"cantidad": "Escribe el área", "fila": "—"}
# Filas de la etiqueta por calculadora: (rótulo, salida). La nota va aparte.
FILAS = {
    "tierra-negra": (("Presentación sugerida", "presentacion"), ("Equivalente en costales", "equivalente")),
    "tezontle": (("Presentación sugerida", "presentacion"), ("Costales equivalentes", "equivalente")),
    "marmol": (("Total orientativo", "total"), ("Peso aproximado", "peso")),
    "piedra-bola": (),
}
NOTAS = {
    "tierra-negra": f"m² × grosor de la capa = m³, redondeado hacia arriba. {datos.ENTREGA_COBRO}",
    "tezontle": "m² × grosor de la capa = m³, redondeado hacia arriba. El m³ y el camión se cotizan según tu colonia.",
    "marmol": (f"3 sacos por m² con capa de 3 a 4 cm; 4 con 5 cm y 5 con 6 cm. Saco a {c.dinero(P['marmol_saco'])}, "
               f"{datos.MARMOL_CONDICION}; la entrega se cobra aparte. Peso con sacos de ≈ 20 kg."),
    "piedra-bola": ("Con capa de 8 a 10 cm se usan de 120 a 150 kg por m². Se vende a granel: mándanos los kg y la "
                    "colonia y te damos el precio con la entrega."),
}


def _select(prefijo, cfg):
    opciones = "".join(f'<option value="{esc(v)}"{" selected" if v == cfg["elegida"] else ""}>{t}</option>'
                       for v, t in cfg["capas"])
    return (f'<div class="vt-campo"><label for="{esc(prefijo)}-capa">{cfg["etiqueta_capa"]}</label>'
            f'<div class="vt-control"><select id="{esc(prefijo)}-capa" data-vt-campo="capa">{opciones}</select></div></div>')


def calculadora(prefijo, tipo, clave, mensaje, nombre):
    """Área (y capa) → etiqueta con la cantidad en banda, la presentación sugerida y su equivalente → WhatsApp con el
    resultado. Solo el resultado (cantidad, filas y nota de mármol) es role="status": la nota fija y el botón no se
    vuelven a leer en cada tecla. Empieza vacía: sin área, el botón manda el mensaje de la página (data-mensaje, con firma). data-cta conserva el
    cta_id que medía main con VTMedicion.whatsapp (p. ej. material:cotizarCalculado)."""
    cfg = CALCULADORAS[clave]
    generico = datos.con_firma(mensaje)
    capa = _select(prefijo, cfg) if "capas" in cfg else ""
    filas = "".join(f'<p class="vt-etiqueta__fila"><span>{rotulo}</span><b data-vt-o="{salida}">{VACIO["fila"]}</b></p>'
                    for rotulo, salida in FILAS[clave])
    nota_dinamica = '<p class="vt-medidor__calc" data-vt-o="nota" hidden></p>' if clave == "marmol" else ""
    return (
        f'<div class="vt-b2b" data-vt-material data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
        f'data-mensaje="{esc(generico)}" data-material="{esc(json.dumps(datos_js(clave), ensure_ascii=False, separators=(",", ":")))}">'
        f'<div class="vt-b2b__form" role="group" aria-label="Calculadora de {esc(nombre)}">'
        f'{c._campo(f"{prefijo}-area", "area", "Área a cubrir", "Ej. 30", "m²", "decimal")}{capa}</div>'
        '<div class="vt-etiqueta-x"><div class="vt-etiqueta vt-medidor__res">'
        '<p class="vt-etiqueta__cod"><span>Tu cálculo</span><span>Aproximado</span></p>'
        '<div class="vt-calc__res" role="status"><p class="vt-etiqueta__precio vt-calc__cantidad is-vacio">'
        f'<small>Necesitas</small><b data-vt-o="cantidad">{VACIO["cantidad"]}</b></p>{filas}{nota_dinamica}</div>'
        f'<p class="vt-medidor__calc">{NOTAS[clave]}</p>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:{cfg["cta"]}" data-vt-o="cta" '
        f'href="{esc(datos.wa_url(generico))}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp'
        '<span class="vt-flecha" aria-hidden="true">→</span></a></div></div></div>')


# ---------- precio por presentación ----------
def precio_texto(precio, desde=False):
    """"$90", "desde $200" o "Según cotización" (None: el precio no está en datos.py)."""
    if precio is None:
        return datos.SEGUN_COTIZACION
    return f"{'desde ' if desde else ''}{c.dinero(precio)}"


def presentaciones(filas, caption):
    """Tabla Presentación | Unidad | Precio. filas: nombre, detalle, unidad, precio (número de datos.PRECIOS o None) y,
    opcional, desde. None se escribe "según cotización": nunca se inventa un precio."""
    cuerpo = "".join(
        f'<tr><th scope="row"><b>{f["nombre"]}</b><span>{f["detalle"]}</span></th><td class="vt-tabla__u">{f["unidad"]}'
        f'</td><td class="vt-tabla__p{"" if f["precio"] else " vt-tabla__p--cotiza"}">{precio_texto(f["precio"], f.get("desde"))}'
        '</td></tr>' for f in filas)
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            '<th scope="col">Presentación</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{cuerpo}</tbody></table>')


# ---------- otros materiales ----------
def otros(items, enlaces=()):
    """Los otros materiales (nombre, precios de datos.py y, solo donde main la tenía, su miniatura) y una línea de enlaces
    a páginas relacionadas. items: titulo, href, texto y, opcional, img (src, ancho, alto)."""
    filas = []
    for i in items:
        foto = (f'<img src="{esc(i["img"]["src"])}" width="{i["img"]["ancho"]}" height="{i["img"]["alto"]}" alt="" '
                'loading="lazy" decoding="async">' if i.get("img") else "")
        filas.append(f'<li>{foto}<div><a href="{esc(i["href"])}">{i["titulo"]}</a><small>{i["texto"]}</small></div></li>')
    linea = ""
    if enlaces:
        partes = " · ".join(f'<a href="{esc(h)}">{t}</a>' for t, h in enlaces)
        linea = f'<p class="vt-promesa vt-mt">También: {partes}.</p>'
    return f'<ul class="vt-otros">{"".join(filas)}</ul>{linea}'


# ---------- portada y cierre ----------
def portada(p, tipo, migas_items):
    """El hero de marca común (componentes.portada). Tezontle y piedra bola no tenían foto de portada en main y no se
    agrega ninguna: salen en la variante sin foto, con la etiqueta en la columna derecha en escritorio."""
    return c.portada(p, tipo, migas_items)


def cierre(ci, mensaje, tipo):
    """CTA final (componentes.cierre) con, si main la tenía, su foto de fondo decorativa (alt="")."""
    html = c.cierre(ci["titulo"], ci["lede"], mensaje, tipo)
    f = ci.get("fondo")
    if not f:
        return html
    fondo = (f'<img class="vt-cierre__fondo" src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="" '
             'loading="lazy" decoding="async">')
    return html.replace('<section class="vt-cierre"', '<section class="vt-cierre vt-cierre--foto"', 1).replace(
        '<div class="vt-wrap vt-cierre__grid">', f'{fondo}<div class="vt-wrap vt-cierre__grid">', 1)


# ---------- pedido por correo (el formulario de main: mismos campos y destino, más honeypot y medición) ----------
ASUNTO = "Pedido desde sitio web - Viveros Terra"  # el de main: el dueño filtra sus correos por él


def formulario_pedido(prefijo, cta, ejemplo_detalle, aviso):
    """Formulario a formsubmit de viverosterra@hotmail.com con los campos de main (nombre, email, detalle), _next a
    /gracias, sin captcha y con honeypot _honey. vt-b2b.js lo valida junto a cada campo y manda generate_lead con method
    "formulario" y cta_id `cta`; sin JS, el navegador valida los required y se envía igual."""
    campos = (
        c._campo_correo(prefijo, "nombre", "Nombre", completar="name", placeholder="Tu nombre"),
        c._campo_correo(prefijo, "email", "Correo", "email", completar="email", placeholder="tu@correo.com"),
        c._campo_correo(prefijo, "detalle", "¿Qué necesitas?", requerido=False, multilinea=True,
                        placeholder=ejemplo_detalle),
    )
    return (
        f'<form class="vt-correo" id="order-form" action="{esc(c.FORMULARIO_ACCION)}" method="POST" data-vt-correo '
        f'data-cta-form="{esc(cta)}"><input type="hidden" name="_subject" value="{esc(ASUNTO)}">'
        f'<input type="hidden" name="_next" value="{esc(c.FORMULARIO_GRACIAS)}">'
        '<input type="hidden" name="_captcha" value="false">'
        '<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
        f'<div class="vt-correo__campos">{"".join(campos)}</div>'
        '<div class="vt-correo__pie"><button type="submit" class="vt-btn vt-btn--tinta">Enviar solicitud de pedido'
        '</button><p class="vt-correo__estado" role="status" data-vt-o="correo-estado"></p>'
        f'<p class="vt-correo__aviso">{aviso}</p></div></form>')
