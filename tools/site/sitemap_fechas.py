"""Fecha de cada artículo del blog en public/sitemap.xml (SEO fase 1, 2026-11-10): el <lastmod> de un artículo es su
dateModified (la fecha del encabezado <!--vt:meta de su fuente, la misma que se ve en la página y que lleva su Article),
no la del último despliegue. Lo corre el build; escribe solo si algo cambia. El resto del sitemap no se toca."""
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


def sincronizar(public=paginas.PUBLIC):
    """Pone las fechas del blog en public/sitemap.xml; devuelve True si lo escribió."""
    path = Path(public) / "sitemap.xml"
    actual = path.read_text(encoding="utf-8")
    nuevo = aplicar(actual, fechas_blog())
    if nuevo == actual:
        return False
    path.write_text(nuevo, encoding="utf-8")
    return True
