"""Aplica el shell compartido (head esencial, menú, pie y barra móvil) a cualquier página de public/.

Cada página lleva tres regiones marcadas: <!-- vt:head -->, <!-- vt:header --> y <!-- vt:footer -->. Este módulo
reemplaza su contenido por los parciales canónicos y marca con data-cta los enlaces de WhatsApp y teléfono del cuerpo
("<tipo>:hero" dentro de la portada, "<tipo>:cuerpo" en el resto). En el índice del blog pone el número real de
artículos en cada <span data-vt-conteo="blog">. Es idempotente.
"""
import re
from pathlib import Path

import paginas
import partials

PUBLIC = paginas.PUBLIC
REGION_RE = re.compile(r"<!-- vt:(head|header|footer) -->.*?<!-- /vt:\1 -->", re.S)
ENLACE_RE = re.compile(
    r'<a\b(?![^>]*\bdata-cta=)([^>]*\bhref="(?:https://wa\.me/|https://api\.whatsapp\.com/|tel:)[^"]*"[^>]*)>'
)
SVC_HERO_RE = re.compile(r"<!-- svc-hero -->.*?<!-- /svc-hero -->", re.S)
VT_HERO_RE = re.compile(r'<section\b[^>]*class="vt-hero\b')
TIENDA = '<body class="vt-pagina vt-tienda">'
PLANTAS = '<body class="vt-pagina vt-plantas">'
MATERIALES = '<body class="vt-pagina vt-materiales">'
PRECIOS = '<body class="vt-pagina vt-precios">'
UTIL = '<body class="vt-pagina vt-util">'
CONTEO_BLOG_RE = re.compile(r'(<span data-vt-conteo="blog">)\d+(</span>)')


def fin_elemento(html, inicio):
    """Índice justo después del cierre del elemento que abre en `inicio` (cuenta anidados del mismo nombre)."""
    nombre = re.match(r"<([a-zA-Z][a-zA-Z0-9]*)", html[inicio:]).group(1).lower()
    etiqueta = re.compile(rf"<(/?){nombre}\b[^>]*>", re.I)
    nivel = 0
    for m in etiqueta.finditer(html, inicio):
        nivel += -1 if m.group(1) else 1
        if nivel == 0:
            return m.end()
    raise ValueError(f"<{nombre}> sin cierre desde la posición {inicio}")


def _zonas_hero(html):
    zonas = [(m.start(), m.end()) for m in SVC_HERO_RE.finditer(html)]
    vt_hero = VT_HERO_RE.search(html)
    if vt_hero:
        zonas.append((vt_hero.start(), fin_elemento(html, vt_hero.start())))
    return sorted(zonas)


def _marcar(fragmento, tipo, seccion):
    return ENLACE_RE.sub(lambda m: f'<a data-cta="{tipo}:{seccion}"{m.group(1)}>', fragmento)


def marcar_ctas(html, tipo):
    """Agrega data-cta a los enlaces wa.me y tel: que no lo tienen."""
    salida, cursor = [], 0
    for inicio, fin in _zonas_hero(html):
        if inicio < cursor:
            continue
        salida.append(_marcar(html[cursor:inicio], tipo, "cuerpo"))
        salida.append(_marcar(html[inicio:fin], tipo, "hero"))
        cursor = fin
    salida.append(_marcar(html[cursor:], tipo, "cuerpo"))
    return "".join(salida)


def conteo_blog(public=PUBLIC):
    """Número de artículos publicados en public/blog/<slug>/index.html."""
    return len(list((Path(public) / "blog").glob("*/index.html")))


def aplicar(html, ruta, urls, public=PUBLIC):
    """Página con el shell canónico de su ruta. Falla si no tiene exactamente una región de cada tipo."""
    ctx = paginas.contexto(ruta)
    encontradas = sorted(m.group(1) for m in REGION_RE.finditer(html))
    if encontradas != ["footer", "head", "header"]:
        raise ValueError(f"{ruta}: regiones del shell {encontradas}; debe haber head, header y footer, una de cada una")
    partes = {
        "head": partials.head(urls, legacy="/css/tailwind.css" in html, tienda=TIENDA in html, plantas=PLANTAS in html,
                              materiales=MATERIALES in html, precios=PRECIOS in html, util=UTIL in html),
        "header": partials.header(ctx),
        "footer": partials.footer(ctx),
    }
    html = REGION_RE.sub(lambda m: partes[m.group(1)], html)
    if ruta == "/blog":
        html = CONTEO_BLOG_RE.sub(lambda m: f"{m.group(1)}{conteo_blog(public)}{m.group(2)}", html)
    return marcar_ctas(html, ctx["tipo"])


def paginas_html(public=PUBLIC):
    return sorted(Path(public).rglob("*.html"))


def aplicar_archivo(path, urls, public=PUBLIC):
    """Aplica el shell al archivo; escribe solo si cambia. Devuelve True si lo escribió."""
    path = Path(path)
    original = path.read_text(encoding="utf-8")
    nuevo = aplicar(original, paginas.ruta_de(path, public), urls, public)
    if nuevo == original:
        return False
    path.write_text(nuevo, encoding="utf-8")
    return True


def aplicar_todo(urls, public=PUBLIC):
    """Aplica el shell a todas las páginas de public/; devuelve cuántas cambiaron."""
    return sum(aplicar_archivo(p, urls, public) for p in paginas_html(public))
