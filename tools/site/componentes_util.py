"""Componentes de las páginas utilitarias (Etapa 2i): cabecera sin etiqueta de precio, documento legal con índice, controles
con <label> o <fieldset> reales para el cuestionario y datos de envío, y botón de WhatsApp con texto propio. Funciones
puras; el texto llega de tools/site/contenido/ (solo HTML en línea permitido) y los atributos se escapan aquí."""
import componentes as c
import datos
from partials import WA_GLIFO, esc


# Etiquetas de autor de main que estas páginas ya no publican; paridad.py no las captura, así que el motivo se escribe aquí.
META_AUTOR_RETIRADA = {clave: "No es un artículo: el autor solo se declara en los artículos del blog, como en las páginas migradas antes."
                       for clave in ("author", "article:author", "article:publisher")}


def boton_wa_texto(texto, mensaje, cta):
    """Botón de WhatsApp con un texto que no es "Cotizar por WhatsApp" (Adelantar, Mandar foto…)."""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>')


def cabeza(k):
    """Ruta visible (si la hay), kicker, H1, entrada y, opcional, foto de producción. k: h1, lede, kicker, migas, foto
    (src, ancho, alto, alt), aviso. La foto es la única imagen prioritaria de la página."""
    ruta = c.migas(k["migas"]) if k.get("migas") else ""
    aviso = f'<p class="vt-promesa">{k["aviso"]}</p>' if k.get("aviso") else ""
    extra = k.get("extra", "")
    foto = ""
    if k.get("foto"):
        f = k["foto"]
        foto = (f'<div class="vt-util__foto"><img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" '
                f'alt="{esc(f["alt"])}" loading="eager" fetchpriority="high" decoding="async"></div>')
    return (f'<section class="vt-util__cabeza vt-titular vt-titular--larga" aria-labelledby="vt-h1"><div class="vt-wrap">{ruta}'
            f'<div class="vt-util__intro"><div><p class="vt-kicker">{k["kicker"]}</p><h1 id="vt-h1">{k["h1"]}</h1>'
            f'<p class="vt-lede">{k["lede"]}</p>{aviso}{extra}</div>{foto}</div></div></section>')


def _bloque_legal(b):
    tipo, valor = b
    if tipo == "p":
        return f"<p>{valor}</p>"
    if tipo == "h3":
        return f"<h3>{valor}</h3>"
    etiqueta = "ol" if tipo == "ol" else "ul"
    return f"<{etiqueta}>" + "".join(f"<li>{x}</li>" for x in valor) + f"</{etiqueta}>"


def documento_legal(secciones):
    """Índice (con los h2) y artículo; cada sección conserva su id, el ancla que enlazan las otras páginas."""
    enlaces = "".join(f'<li><a href="#{esc(s["id"])}">{s.get("corto", s["titulo"])}</a></li>' for s in secciones)
    cuerpo = "".join(f'<section id="{esc(s["id"])}" aria-labelledby="vt-h-{esc(s["id"])}"><h2 id="vt-h-{esc(s["id"])}">'
                     f'{s["titulo"]}</h2>{"".join(_bloque_legal(b) for b in s["bloques"])}</section>'
                     for s in secciones)
    return (f'<div class="vt-wrap vt-legal"><nav class="vt-legal__indice" aria-label="En esta página"><ol>{enlaces}</ol>'
            f'</nav><article class="vt-legal__texto">{cuerpo}</article></div>')


# ---------- controles ----------
def _req(campo):
    return ' <span class="vt-req" aria-hidden="true">*</span>' if campo.get("requerido") else ""


def _pie(campo):
    return f'<p class="vt-util__pista">{campo["pista"]}</p>' if campo.get("pista") else ""


def _control(campo, ident):
    comunes = f'id="{esc(ident)}"' + (f' name="{esc(campo["name"])}"' if campo.get("name") else "")
    comunes += " required" if campo.get("requerido") else ""
    for atributo, clave in (("autocomplete", "completar"), ("placeholder", "placeholder"), ("min", "min"),
                            ("inputmode", "modo"), ("maxlength", "max"), ("minlength", "min_largo"), ("pattern", "patron"),
                            ("title", "ayuda"), ("step", "paso")):
        if campo.get(clave) is not None:
            comunes += f' {atributo}="{esc(campo[clave])}"'
    if campo["tipo"] == "area":
        return f"<textarea {comunes}></textarea>"
    if campo["tipo"] == "lista":
        opciones = "".join(f'<option value="{esc(v)}">{t}</option>' if v is not None else f"<option>{t}</option>"
                           for v, t in campo["opciones"])
        return f"<select {comunes}>{opciones}</select>"
    return f'<input {comunes} type="{esc(campo["tipo"])}">'


def _campo(k):
    ident = k.get("id") or f'c-{k["name"]}'
    error = f'<p class="msg">{k["error"]}</p>' if k.get("error") else ""
    return (f'<div class="vt-campo"><label for="{esc(ident)}">{k["label"]}{_req(k)}</label>'
            f'<div class="vt-control">{_control(k, ident)}</div>{error}{_pie(k)}</div>')


def _opciones(k):
    filas = "".join(
        f'<label class="vt-pill"><input type="{k["tipo"]}" name="{esc(k["name"])}" value="{esc(v)}"'
        + "".join(f' {a}="{esc(x)}"' for a, x in (resto[0] if resto else ())) + f'><span>{t}</span></label>'
        for v, t, *resto in k["items"])
    sub = dibujar(k["sub"]) if k.get("sub") else ""
    return (f'<fieldset class="vt-util__grupo"><legend>{k["legend"]}</legend><div class="{k.get("clase_grupo", "vt-pills")}">'
            f'{filas}</div>{sub}</fieldset>')


# El contenido solo puede llevar HTML en línea (test_contenido.py): describe los controles con estos cuatro datos y la
# plantilla los dibuja.
def campo(k):
    """k: label, tipo (text, tel, email, number, area o lista), name o id; opcionales requerido, completar, placeholder,
    min, modo, max, min_largo, patron, ayuda (title), paso (step), pista, error, opciones."""
    return ("campo", k)


def opciones(k):
    """Radios o casillas en <fieldset>. k: legend, tipo (radio o checkbox), name, items (valor, texto y, opcional,
    atributos extra) y, opcionales, clase_grupo y sub (un condicional)."""
    return ("opciones", k)


def condicional(ident, control):
    return ("condicional", ident, control)


def fila(*controles, columnas=1):
    return ("fila", controles, columnas)


SUMA_AREAS = ("suma",)


def dibujar(control):
    """HTML de un control descrito con campo(), opciones(), condicional() o fila()."""
    tipo = control[0]
    if tipo == "campo":
        return _campo(control[1])
    if tipo == "opciones":
        return _opciones(control[1])
    if tipo == "condicional":
        return f'<div class="vt-util__cond" id="{esc(control[1])}" hidden>{dibujar(control[2])}</div>'
    if tipo == "suma":
        return ('<p class="vt-util__suma" id="area-display" hidden><span>Área total calculada</span>'
                '<strong id="area-total-val">0 m²</strong></p>')
    return (f'<div class="vt-util__fila vt-util__fila--{control[2]}">' + "".join(dibujar(c) for c in control[1]) + "</div>")


def dibujar_todos(controles):
    return "".join(dibujar(c) for c in controles)
