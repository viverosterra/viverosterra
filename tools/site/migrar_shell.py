"""Migración única de las páginas escritas a mano al shell compartido (Etapa 1).

Quita el menú viejo (terra-nav o header sticky del blog), los pies, el botón flotante de WhatsApp, la barra móvil de
la home, el gtag duplicado, las meta heredadas, los favicons sueltos, nav-scroll.js y los eventos sueltos clic_*;
protege el único script de menú sin guarda; inserta las regiones vacías del shell y envuelve el contenido en
<main id="main">. Después, tools/site/build.py llena las regiones. Las páginas que ya tienen regiones no se tocan.

También quita el CSS y los scripts que solo servían al marcado retirado (huerfanos.py), cambia los eventos clic_wa_*
y los window.open de WhatsApp por VTMedicion.whatsapp (medicion_js.py) y, en los artículos del blog que perdieron su
ruta de navegación con el header viejo, vuelve a poner una visible (Inicio › Blog › título) al inicio del <main>.

Uso: python3 tools/site/migrar_shell.py [--dry-run] [carpeta public]   (una sola vez, desde cualquier carpeta)
"""
import re
import sys
from html import escape, unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import huerfanos  # noqa: E402
import medicion_js  # noqa: E402
import paginas  # noqa: E402
from shell import PUBLIC, fin_elemento, paginas_html  # noqa: E402

GTAG_RE = re.compile(
    r"(?:<!-- Google tag \(gtag\.js\) -->\s*)?"
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-RMZCVJ734M"></script>\s*'
    r"<script>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];.*?"
    r"gtag\(\s*'config'\s*,\s*'G-RMZCVJ734M'\s*\);?\s*</script>[ \t]*\n?",
    re.S,
)
META_RE = re.compile(
    r'[ \t]*<meta name="(?:keywords|geo\.region|geo\.placename|ai-content-declaration|last-modified|language)"[^>]*>[ \t]*\n?'
)
ICONO_RE = re.compile(r'[ \t]*<link rel="(?:icon|shortcut icon)"[^>]*>[ \t]*\n?')
NAV_SCROLL_RE = re.compile(r'[ \t]*<script src="/js/nav-scroll\.js[^"]*"[^>]*></script>[ \t]*\n?')
ONCLICK_CLIC_RE = re.compile(r"""\s+onclick="gtag\('event',\s*'clic_[^"]*\"""")
EVENTO_CLIC_RE = re.compile(r"[ \t]*gtag\('event',\s*'clic_[^']*',\s*\{[^{}]*\}\);?[ \t]*\n?")
MENU_SIN_GUARDA_RE = re.compile(r"^(\s*)mb\.addEventListener\(", re.M)
MIGAS_EN_CUERPO_RE = re.compile(r'aria-label="(?:[Bb]readcrumb|Ruta de navegación)"')


def quitar_elemento(html, patron):
    """Quita el primer elemento cuya etiqueta de apertura coincide con `patron`. Devuelve (html, fragmentos quitados)."""
    m = re.search(patron, html)
    if not m:
        return html, []
    fin = fin_elemento(html, m.start())
    return html[:m.start()] + html[fin:], [html[m.start():fin]]


def quitar_todos(html, patron):
    quitados = []
    while True:
        html, quitado = quitar_elemento(html, patron)
        if not quitado:
            return html, quitados
        quitados += quitado


def quitar_header_viejo(html):
    """Quita el primer <header> con <nav> que aparece antes del primer <main> o <article> (el de los artículos se queda)."""
    limite = re.search(r"<(?:main|article)\b", html)
    tope = limite.start() if limite else len(html)
    for m in re.finditer(r"<header\b", html[:tope]):
        fin = fin_elemento(html, m.start())
        if "<nav" in html[m.start():fin]:
            return html[:m.start()] + html[fin:], [html[m.start():fin]]
    return html, []


def insertar_regiones(html):
    html = html.replace("</head>", "<!-- vt:head -->\n<!-- /vt:head -->\n</head>", 1)
    html = re.sub(r"(<body\b[^>]*>)", r"\1\n<!-- vt:header -->\n<!-- /vt:header -->", html, count=1)
    cierre = html.rindex("</body>")
    return html[:cierre] + "<!-- vt:footer -->\n<!-- /vt:footer -->\n" + html[cierre:]


def envolver_main(html):
    """Deja un solo <main id="main">: reutiliza el que exista o envuelve todo lo que hay entre header y footer."""
    m = re.search(r"<main\b([^>]*)>", html)
    if m and 'id="main"' in m.group(1):
        return html
    if m and "id=" not in m.group(1):
        return html[:m.start()] + f'<main id="main"{m.group(1)}>' + html[m.end():]
    if m:
        # Un <main> con otro id (la rejilla del catálogo) pasa a <div> para poder envolver la página.
        fin = fin_elemento(html, m.start())
        bloque = html[m.start():fin]
        # role="region" conserva el landmark con nombre que daba el <main aria-label>.
        bloque = '<div role="region"' + bloque[len("<main"):-len("</main>")] + "</div>"
        html = html[:m.start()] + bloque + html[fin:]
    html = html.replace("<!-- /vt:header -->", '<!-- /vt:header -->\n<main id="main">', 1)
    return html.replace("<!-- vt:footer -->", "</main>\n<!-- vt:footer -->", 1)


def migas_blog(html):
    """Ruta visible Inicio › Blog › título (el del <h1>) para un artículo del blog."""
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)
    titulo = " ".join(unescape(re.sub(r"<[^>]+>", "", h1.group(1))).split()) if h1 else "Artículo"
    return (
        '<nav class="vt-crumbs" aria-label="Ruta de navegación"><ol class="vt-wrap">'
        '<li><a href="/">Inicio</a></li><li><a href="/blog">Blog</a></li>'
        f'<li aria-current="page">{escape(titulo)}</li></ol></nav>'
    )


def migrar(html, ruta=None, cuenta=None):
    """Página migrada a las regiones del shell. `cuenta` (opcional) acumula lo que quitaron los pasos de limpieza."""
    if "<!-- vt:header -->" in html:
        return html
    quitados = []
    for paso in (
        lambda h: quitar_elemento(h, r'<nav class="terra-nav"'),
        quitar_header_viejo,
        lambda h: quitar_todos(h, r"<footer\b"),
        lambda h: quitar_todos(h, r'<a\b[^>]*class="[^"]*\bwa-float\b'),
        lambda h: quitar_elemento(h, r'<div class="vt-stickybar"'),
    ):
        html, fragmentos = paso(html)
        quitados += fragmentos
    html = GTAG_RE.sub("", html)
    html = META_RE.sub("", html)
    html = ICONO_RE.sub("", html)
    html = NAV_SCROLL_RE.sub("", html)
    html = ONCLICK_CLIC_RE.sub("", html)
    html, medidos = medicion_js.medir_whatsapp_js(html)
    html = EVENTO_CLIC_RE.sub("", html)
    html = MENU_SIN_GUARDA_RE.sub(r"\1if(mb&&mm)mb.addEventListener(", html)
    html, limpios = huerfanos.limpiar(html, quitados)
    if cuenta is not None:
        for clave, valor in {**medidos, **limpios}.items():
            cuenta[clave] = cuenta.get(clave, 0) + valor
    html = envolver_main(insertar_regiones(html))
    if ruta and ruta.startswith("/blog/") and not MIGAS_EN_CUERPO_RE.search(html):
        html = html.replace('<main id="main">', '<main id="main">\n' + migas_blog(html), 1)
    return html


def main(argv=None):
    """Migra las páginas de public/ (o de la carpeta indicada). Con --dry-run solo cuenta, sin escribir."""
    args = list(sys.argv[1:] if argv is None else argv)
    simulacro = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    public = Path(args[0]).resolve() if args else PUBLIC
    migradas, cuenta = 0, {}
    for path in paginas_html(public):
        original = path.read_text(encoding="utf-8")
        nuevo = migrar(original, paginas.ruta_de(path, public), cuenta)
        if nuevo != original:
            migradas += 1
            if not simulacro:
                path.write_text(nuevo, encoding="utf-8")
            print(f"{'migraría' if simulacro else 'migrada'} {path.relative_to(public)}")
    print(f"{migradas} páginas {'por migrar' if simulacro else 'migradas'}")
    print("limpieza: " + ", ".join(f"{clave} {valor}" for clave, valor in sorted(cuenta.items())))


if __name__ == "__main__":
    main()
