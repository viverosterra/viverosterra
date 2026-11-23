"""Fecha de cada artículo del blog en public/sitemap.xml (SEO fase 1, 2026-11-10): el <lastmod> de un artículo es su
dateModified (la fecha del encabezado <!--vt:meta de su fuente, la misma que se ve en la página y que lleva su Article),
no la del último despliegue. Lo corre el build; escribe solo si algo cambia.

Las demás páginas (auditoría de posicionamiento, 2026-11-22): su <lastmod> es el día en que cambió su texto. Antes era una
fecha puesta a mano que se quedaba vieja (el mapa decía 10 de noviembre con páginas corregidas el 21) y los buscadores
conservaban copias de hace meses. sitemap_registro.json guarda, por URL, la huella del texto de su <main> y la fecha: si la
huella cambia, la fecha pasa a ser ENTREGA. Cambiar la plantilla, el menú o el pie no mueve la fecha. El build no lee el
reloj (regla de test_respuestas): ENTREGA se sube a mano al empezar cada entrega que cambia textos."""
import hashlib
import json
import re
from pathlib import Path

import datos
import paginas
from contenido import articulo


def fechas_blog():
    """{URL del artículo: dateModified (o datePublished si no tiene)}."""
    salida = {}
    for slug in articulo.CLAVES:
        doc, _cuerpo = articulo.leer(slug)
        _publicado, modificado = articulo.fechas(doc["jsonld"])
        salida[f"{datos.SITIO}/blog/{slug}"] = modificado[:10]
    return salida


def aplicar(xml, fechas):
    """El sitemap con el <lastmod> de cada URL de `fechas`; falla si una no está (un artículo sin entrada)."""
    for url, fecha in fechas.items():
        entrada = re.compile(r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)")
        xml, cambios = entrada.subn(lambda m: m.group(1) + fecha + m.group(2), xml, count=1)
        if not cambios:
            raise ValueError(f"sitemap.xml: falta la entrada de {url}")
    return xml


# Día de la entrega en curso: la fecha que toma una página cuando cambia su texto. Subirla al empezar cada entrega.
ENTREGA = "2026-11-22"
REGISTRO = Path(__file__).resolve().parent / "sitemap_registro.json"
ENTRADA_RE = re.compile(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]*)</lastmod>")
MAIN_RE = re.compile(r"<main\b.*?</main>", re.S)


def huella(html):
    """Huella del texto visible del <main> (sin etiquetas ni espacios de más); de toda la página si no tiene <main>."""
    main = MAIN_RE.search(html)
    texto = re.sub(r"<(script|style)\b.*?</\1>", " ", main.group(0) if main else html, flags=re.S)
    texto = " ".join(re.sub(r"<[^>]+>", " ", texto).split())
    return hashlib.sha1(texto.encode("utf-8")).hexdigest()[:16]


def archivo_de(url, public):
    ruta = url.removeprefix(datos.SITIO).strip("/")
    base = Path(public) / ruta
    for candidato in (base / "index.html", base.with_suffix(".html") if ruta else base / "index.html", base):
        if candidato.is_file():
            return candidato
    raise ValueError(f"sitemap.xml: {url} no tiene archivo en public/")


def fechas_paginas(xml, registro, public=paginas.PUBLIC, hoy=None):
    """({URL: lastmod} de las páginas que no son artículos, registro al día). Una URL nueva entra con la fecha que ya
    traía el mapa; una cuyo texto cambió, con la de la entrega (ENTREGA)."""
    hoy = hoy or ENTREGA
    blog = f"{datos.SITIO}/blog/"
    fechas, nuevo = {}, {}
    for url, lastmod in ENTRADA_RE.findall(xml):
        if url.startswith(blog):
            continue
        marca = huella(archivo_de(url, public).read_text(encoding="utf-8"))
        anterior = registro.get(url)
        if anterior is None:
            fecha = lastmod
        elif anterior["huella"] != marca:
            fecha = hoy
        else:
            fecha = anterior["fecha"]
        fechas[url] = fecha
        nuevo[url] = {"huella": marca, "fecha": fecha}
    return fechas, nuevo


def leer_registro(path=REGISTRO):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def sincronizar(public=paginas.PUBLIC, registro_path=REGISTRO):
    """Pone las fechas del blog y de las demás páginas en public/sitemap.xml; devuelve True si escribió algo."""
    path = Path(public) / "sitemap.xml"
    actual = path.read_text(encoding="utf-8")
    registro = leer_registro(registro_path)
    fechas, registro_nuevo = fechas_paginas(actual, registro, public)
    nuevo = aplicar(aplicar(actual, fechas_blog()), fechas)
    cambio = False
    if registro_nuevo != registro:
        registro_path.write_text(json.dumps(registro_nuevo, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        cambio = True
    if nuevo != actual:
        path.write_text(nuevo, encoding="utf-8")
        cambio = True
    return cambio
