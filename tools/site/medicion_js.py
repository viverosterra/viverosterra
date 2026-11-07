"""Medición de los WhatsApp que las páginas abren desde JavaScript (calculadoras, formularios, botones).

El oyente delegado de terra.js solo ve clics en enlaces <a href="https://wa.me/...">; un window.open('https://wa.me…')
le es invisible. Este paso, idempotente:
  1. cambia los eventos sueltos gtag('event','clic_wa_<x>',{…}) por VTMedicion.whatsapp('<x>', {label}) (mismo
     generate_lead que un clic en enlace), conservando la etiqueta del evento viejo;
  2. agrega VTMedicion.whatsapp('<función>') justo antes de cada window.open que abre WhatsApp y aún no se mide.
Solo toca aperturas que empiezan una sentencia; las demás (p. ej. `if (x) window.open(…)`) se cuentan como omitidas.
"""
import re

LLAMADA = "window.VTMedicion&&VTMedicion.whatsapp("
EVENTO_WA_RE = re.compile(r"gtag\('event',\s*'clic_wa_([a-z0-9_]+)',\s*\{([^{}]*)\}\);?")
ETIQUETA_RE = re.compile(r"""'event_label'\s*:\s*((?:'[^']*'|[^,'}])+)""")
APERTURA_RE = re.compile(
    r"""window\.open\(\s*(?:(['"`])https://(?:wa\.me|api\.whatsapp\.com)/|(\w+)\s*(\(\s*\))?\s*[,)])"""
)
YA_MEDIDA_RE = re.compile(r"VTMedicion\.whatsapp\([^;]*\);\s*$")
WA_URL = r"""['"`]https://(?:wa\.me|api\.whatsapp\.com)/"""


def _evento(m):
    seccion = m.group(1).replace("_", "-")
    etiqueta = ETIQUETA_RE.search(m.group(2))
    extra = f",{{label:{etiqueta.group(1).strip()}}}" if etiqueta else ""
    return f"{LLAMADA}'{seccion}'{extra});"


def _abre_whatsapp(html, m):
    """La apertura usa un literal wa.me, una variable que lo guarda o una función que lo devuelve."""
    if m.group(1):
        return True
    nombre = m.group(2)
    if m.group(3):
        funcion = re.search(rf"function\s+{re.escape(nombre)}\s*\([^)]*\)\s*\{{", html)
        return bool(funcion and re.search(WA_URL, html[funcion.end():funcion.end() + 600]))
    antes = html[max(0, m.start() - 400):m.start()]
    return re.search(rf"(?:const|let|var)\s+{re.escape(nombre)}\s*=\s*{WA_URL}", antes) is not None


def _inicia_sentencia(antes):
    limpio = antes.rstrip()
    if limpio[-1:] in (";", "{", "}") or re.search(r'\bon\w+="$', limpio):
        return True
    salto = "\n" in antes[len(limpio):]
    return salto and limpio[-1:] not in tuple(")=>:?,(&|+") and not limpio.endswith("else")


def _seccion(html, posicion):
    """Nombre de la última función declarada en el mismo <script>, o 'boton' si la apertura está en un atributo."""
    abre, cierra = html.rfind("<script", 0, posicion), html.rfind("</script>", 0, posicion)
    if abre <= cierra:
        return "boton"
    nombres = re.findall(r"function\s+(\w+)\s*\(", html[abre:posicion])
    return nombres[-1] if nombres else "js"


def medir_whatsapp_js(html):
    """Página con cada WhatsApp abierto desde JS medido por VTMedicion.whatsapp. Devuelve (html, cuenta)."""
    cuenta = {"eventos": 0, "aperturas": 0, "omitidas": 0}
    html, cuenta["eventos"] = EVENTO_WA_RE.subn(_evento, html)
    for m in reversed(list(APERTURA_RE.finditer(html))):
        antes = html[:m.start()]
        if not _abre_whatsapp(html, m) or YA_MEDIDA_RE.search(antes):
            continue
        if not _inicia_sentencia(antes):
            cuenta["omitidas"] += 1
            continue
        html = f"{antes}{LLAMADA}'{_seccion(html, m.start())}');{html[m.start():]}"
        cuenta["aperturas"] += 1
    return html, cuenta
