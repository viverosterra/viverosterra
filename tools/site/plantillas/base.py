"""Documento de una página con plantilla: <head> propio (título, descripción, robots, canonical, Open Graph, precargas y
JSON-LD), regiones vacías del shell (las llena tools/site/shell.py) y <main id="main"> con el cuerpo.

Sin Google Fonts ni CSS viejo: las fuentes y terra.css llegan con la región vt:head del shell.
"""
import json
from html import escape


def jsonld(bloque):
    """<script> de JSON-LD compacto; "</" se escapa para que el texto nunca cierre el script."""
    texto = json.dumps(bloque, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + texto.replace("</", "<\\/") + "</script>"


def precarga_imagen(f):
    """<link rel="preload"> de la imagen principal (nunca lazy; spec §3.3)."""
    extra = f' imagesrcset="{escape(f["srcset"])}" imagesizes="{escape(f["sizes"])}"' if f.get("srcset") else ""
    return f'<link rel="preload" as="image" href="{escape(f["src"])}"{extra} fetchpriority="high">'


def documento(meta, cuerpo, *, jsonld_bloques=(), precargas=(), scripts=()):
    """meta: title, description, robots, canonical y og (pares en el orden publicado)."""
    lineas = [
        "<!DOCTYPE html>",
        '<html lang="es-MX">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{escape(meta['title'], quote=False)}</title>",
        f'<meta name="description" content="{escape(meta["description"])}">',
        f'<meta name="robots" content="{escape(meta["robots"])}">',
        f'<link rel="canonical" href="{escape(meta["canonical"])}">',
    ]
    lineas += [f'<meta property="{escape(p)}" content="{escape(v)}">' for p, v in meta["og"]]
    lineas.append('<link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">')
    lineas += list(precargas)
    lineas += [jsonld(b) for b in jsonld_bloques]
    lineas += [
        "<!-- vt:head -->", "<!-- /vt:head -->", "</head>", '<body class="vt-pagina">',
        "<!-- vt:header -->", "<!-- /vt:header -->", '<main id="main">', cuerpo, "</main>",
        "<!-- vt:footer -->", "<!-- /vt:footer -->",
    ]
    lineas += [f'<script src="{escape(s)}" defer></script>' for s in scripts]
    lineas += ["</body>", "</html>", ""]
    return "\n".join(lineas)
