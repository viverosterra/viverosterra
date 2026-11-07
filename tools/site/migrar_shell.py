"""Migración única de las páginas escritas a mano al shell compartido (Etapa 1).

Quita el menú viejo (terra-nav o header sticky del blog), los pies, el botón flotante de WhatsApp, la barra móvil de
la home, el gtag duplicado, las meta heredadas, los favicons sueltos, nav-scroll.js y los eventos sueltos clic_*;
protege el único script de menú sin guarda; inserta las regiones vacías del shell y envuelve el contenido en
<main id="main">. Después, tools/site/build.py llena las regiones. Las páginas que ya tienen regiones no se tocan.

Uso: python3 tools/site/migrar_shell.py   (una sola vez, desde cualquier carpeta)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


def quitar_elemento(html, patron):
    """Quita el primer elemento cuya etiqueta de apertura coincide con `patron`. Devuelve (html, quitados)."""
    m = re.search(patron, html)
    if not m:
        return html, 0
    return html[:m.start()] + html[fin_elemento(html, m.start()):], 1


def quitar_todos(html, patron):
    total = 0
    while True:
        html, quitado = quitar_elemento(html, patron)
        if not quitado:
            return html, total
        total += quitado


def quitar_header_viejo(html):
    """Quita el primer <header> con <nav> que aparece antes del primer <main> o <article> (el de los artículos se queda)."""
    limite = re.search(r"<(?:main|article)\b", html)
    tope = limite.start() if limite else len(html)
    for m in re.finditer(r"<header\b", html[:tope]):
        fin = fin_elemento(html, m.start())
        if "<nav" in html[m.start():fin]:
            return html[:m.start()] + html[fin:], 1
    return html, 0


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
        bloque = "<div" + bloque[len("<main"):-len("</main>")] + "</div>"
        html = html[:m.start()] + bloque + html[fin:]
    html = html.replace("<!-- /vt:header -->", '<!-- /vt:header -->\n<main id="main">', 1)
    return html.replace("<!-- vt:footer -->", "</main>\n<!-- vt:footer -->", 1)


def migrar(html):
    if "<!-- vt:header -->" in html:
        return html
    html, _ = quitar_elemento(html, r'<nav class="terra-nav"')
    html, _ = quitar_header_viejo(html)
    html, _ = quitar_todos(html, r"<footer\b")
    html, _ = quitar_todos(html, r'<a\b[^>]*class="[^"]*\bwa-float\b')
    html, _ = quitar_elemento(html, r'<div class="vt-stickybar"')
    html = GTAG_RE.sub("", html)
    html = META_RE.sub("", html)
    html = ICONO_RE.sub("", html)
    html = NAV_SCROLL_RE.sub("", html)
    html = ONCLICK_CLIC_RE.sub("", html)
    html = EVENTO_CLIC_RE.sub("", html)
    html = MENU_SIN_GUARDA_RE.sub(r"\1if(mb&&mm)mb.addEventListener(", html)
    return envolver_main(insertar_regiones(html))


def main():
    migradas = 0
    for path in paginas_html():
        original = path.read_text(encoding="utf-8")
        nuevo = migrar(original)
        if nuevo != original:
            path.write_text(nuevo, encoding="utf-8")
            migradas += 1
            print(f"migrada {path.relative_to(PUBLIC)}")
    print(f"{migradas} páginas migradas")


if __name__ == "__main__":
    main()
