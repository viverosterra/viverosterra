"""Documento de una página con plantilla: <head> propio (título, descripción, robots, canonical, Open Graph, precargas y
JSON-LD), regiones vacías del shell (las llena tools/site/shell.py) y <main id="main"> con el cuerpo.

Sin Google Fonts ni CSS viejo: las fuentes y terra.css llegan con la región vt:head del shell.
"""
import json
from html import escape

import entidad


def jsonld(bloque):
    """<script> de JSON-LD compacto; "</" se escapa para que el texto nunca cierre el script."""
    texto = json.dumps(bloque, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + texto.replace("</", "<\\/") + "</script>"


def meta_de(k):
    """La meta del contenido con sus migas visibles (k["migas"]), para que documento arme el BreadcrumbList de ellas, y
    (las utilitarias las traen en k["cabeza"]) y con la fecha de su respuesta directa (k["respuesta"]["fecha"]) como dateModified del WebPage."""
    modificado = (k.get("respuesta") or {}).get("fecha") or k["meta"].get("modificado")
    migas = k.get("migas") or (k.get("cabeza") or {}).get("migas")
    return {**k["meta"], "migas": migas, "modificado": modificado}


def imagen_de(foto):
    """Ruta de la versión más grande de la foto principal (la última del srcset o su src), para el og:image de las
    páginas que no declaran uno: siempre una foto real que la página ya muestra."""
    if foto.get("srcset"):
        return foto["srcset"].split(",")[-1].split()[0]
    return foto["src"]


def precarga_imagen(f):
    """<link rel="preload"> de la imagen principal (nunca lazy; spec §3.3)."""
    extra = f' imagesrcset="{escape(f["srcset"])}" imagesizes="{escape(f["sizes"])}"' if f.get("srcset") else ""
    return f'<link rel="preload" as="image" href="{escape(f["src"])}"{extra} fetchpriority="high">'


# Plan visual V3 (2026-11-11): la línea de negocio de la página (por su ruta) da el tinte de las secciones y el dibujo
# de línea de las bandas oscuras: pasto (hoja de San Agustín), plantas (fronda de palma) y tierra (raíz). Las demás
# páginas (inicio, servicios, colonias, blog) quedan con el tinte hueso y la hoja.
LINEAS = (
    ("tierra", ("/tierra-negra", "/piedra-bola", "/marmol-blanco", "/tezontle-rojo")),
    ("plantas", ("/plantas-", "/palmas-", "/arboles-", "/vivero-tampico", "/catalogo", "/post/nochebuenas")),
    ("pasto", ("/pasto-", "/mayoreo-pasto", "/protocolo-cuidados-pasto")),
)


def linea_de(canonical):
    ruta = "/" + canonical.split("://", 1)[-1].split("/", 1)[-1] if "://" in canonical else canonical
    return next((nombre for nombre, prefijos in LINEAS if ruta.startswith(prefijos)), None)


def atributo_linea(canonical):
    linea = linea_de(canonical)
    return f' data-linea="{linea}"' if linea else ""


def documento(meta, cuerpo, *, jsonld_bloques=(), precargas=(), scripts=(), head_extra=(), tras_main="",
              clase_body="vt-pagina", imagen=None):
    """meta: title, description, robots, canonical, og (pares en el orden publicado) y, opcionales, alternos
    (hreflang, href) y twitter (pares name/content de la Twitter Card). head_extra: líneas después del JSON-LD (datos
    para el JS de la tienda). tras_main: marcado fijo fuera de <main> (lista de cotización, aviso y barra de compra).
    clase_body "vt-pagina vt-tienda" hace que el shell agregue terra-tienda.css. meta["modificado"] (AAAA-MM-DD,
    opcional) es el dateModified del WebPage. imagen: ruta de la foto principal de la página, para el og:image de las
    que no declaran uno. meta["migas"] (opcional, lo pone meta_de): las migas visibles, para que el BreadcrumbList del
    JSON-LD diga lo mismo. El grafo se cierra con entidad.completar y la meta social con entidad.meta_social."""
    jsonld_bloques = entidad.completar(jsonld_bloques, meta, cuerpo, meta.get("migas"))
    meta = entidad.meta_social(meta, imagen)
    lineas = [
        "<!DOCTYPE html>",
        f'<html lang="es-MX"{atributo_linea(meta["canonical"])}>',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{escape(meta['title'], quote=False)}</title>",
        f'<meta name="description" content="{escape(meta["description"])}">',
        f'<meta name="robots" content="{escape(meta["robots"])}">',
        f'<link rel="canonical" href="{escape(meta["canonical"])}">',
    ]
    lineas += [f'<link rel="alternate" hreflang="{escape(h)}" href="{escape(u)}">' for h, u in meta.get("alternos", ())]
    lineas += [f'<meta property="{escape(p)}" content="{escape(v)}">' for p, v in meta["og"]]
    lineas += [f'<meta name="{escape(n)}" content="{escape(v)}">' for n, v in meta.get("twitter", ())]
    lineas.append('<link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">')
    lineas += list(precargas)
    lineas += [jsonld(b) for b in jsonld_bloques]
    lineas += list(head_extra)
    lineas += [
        "<!-- vt:head -->", "<!-- /vt:head -->", "</head>", f'<body class="{escape(clase_body)}">',
        "<!-- vt:header -->", "<!-- /vt:header -->", '<main id="main">', cuerpo, "</main>",
        "<!-- vt:footer -->", "<!-- /vt:footer -->",
    ]
    if tras_main:
        lineas.append(tras_main)
    lineas += [f'<script src="{escape(s)}" defer></script>' for s in scripts]
    lineas += ["</body>", "</html>", ""]
    return "\n".join(lineas)
