"""Los 52 artículos del blog (Etapa 2h). El cuerpo vive en contenido/blog/<slug>.html (HTML con un comentario de metadatos
en JSON: la excepción a "contenido en .py", justificada por el volumen de prosa). Aquí se arma lo que la plantilla
tools/site/plantillas/articulo.py necesita: portada, autor y fecha, índice (de los <h2> del cuerpo, así nunca apunta a un
id que no existe), preguntas, etiqueta de producto, CTA y relacionados. El autor es datos.AUTOR_BLOG."""
import json
import re
from pathlib import Path

import datos
import paginas
from contenido import blog_clusters

DIR = Path(__file__).resolve().parent / "blog"
CLAVES = tuple(sorted(p.stem for p in DIR.glob("*.html")))
# Artículos escritos directamente en este formato (sin página anterior que comparar): quedan fuera de las pruebas de paridad.
NUEVOS = ("palma-bambu-chamaedorea-tampico", "plantas-seguras-mascotas-jardin-tampico")
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
         "diciembre")
M_LOGO = "Era el logo del publisher; ahora el publisher es una referencia por @id a la entidad única #negocio."
M_AUTOR = ("SEO fase 1: autor y publisher del Article son la entidad única #negocio por @id (antes, una Organization "
           "suelta); la firma visible sigue siendo el equipo técnico.")
H2_RE = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)


def leer(slug):
    """(metadatos, cuerpo HTML) del artículo."""
    texto = (DIR / f"{slug}.html").read_text(encoding="utf-8")
    cabeza, _, cuerpo = texto.partition("\n-->\n")
    return json.loads(cabeza.removeprefix("<!--vt:meta\n")), cuerpo


def fecha_larga(iso):
    a, m, d = (int(x) for x in iso[:10].split("-"))
    return f"{d} de {MESES[m - 1]} de {a}"


def sin_etiquetas(fragmento):
    return re.sub(r"<[^>]+>", "", fragmento)


def indice(cuerpo, faq, titulo_faq, respuesta):
    items = [("respuesta", respuesta["titulo"])] if respuesta else []
    items += [(i, sin_etiquetas(t)) for i, t in H2_RE.findall(cuerpo)]
    if faq:
        items.append(("preguntas", titulo_faq))
    return tuple(items)


def fechas(jsonld):
    articulo = next(n for n in jsonld["@graph"] if n.get("@type") == "Article")
    publicado, modificado = articulo.get("datePublished"), articulo.get("dateModified")
    return publicado, modificado or publicado


# Lo que cambia en la cabecera de cada artículo (Entrega A de experiencia, 2026-11-10).
HERO = ("Hero de lectura: titular en la escala común del sitio, lema en serif («Jardinería para el clima de Tampico.», "
        "el mismo en todos) y WhatsApp y teléfono como enlaces de texto bajo la fecha (antes, sin CTA en la cabecera); "
        "sin botón grande ni imagen nueva.")


class _Pagina:
    def __init__(self, slug):
        doc, cuerpo = leer(slug)
        ruta = f"/blog/{slug}"
        publicado, modificado = fechas(doc["jsonld"])
        tema = blog_clusters.de(slug)
        self.CONTENIDO = {
            "meta": doc["meta"], "jsonld": doc["jsonld"], "tipo": "blog", "slug": slug,
            "migas": (("Inicio", "/"), ("Blog", "/blog"), (doc["h1"], None)),
            "kicker": doc["kicker"], "h1": doc["h1"], "dek": doc["dek"], "minutos": doc["minutos"],
            "autor": datos.AUTOR_BLOG, "publicado": fecha_larga(publicado), "publicado_iso": publicado,
            "actualizado": fecha_larga(modificado), "actualizado_iso": modificado,
            "respuesta": doc["respuesta"], "cuerpo": cuerpo, "faq_titulo": doc["faq_titulo"],
            "faq": tuple(tuple(p) for p in doc["faq"]), "indice": indice(cuerpo, doc["faq"], doc["faq_titulo"], doc["respuesta"]),
            "tema": tema, "mensaje": paginas.contexto(ruta)["mensaje"].rsplit("\n\n", 1)[0],
            "relacionados_titulo": doc["relacionados_titulo"], "relacionados": tuple(doc["relacionados"]),
        }
        self.PARIDAD = {**(doc.get("paridad") or {"reemplazos": {}, "retirados": {}}), "jsonld": {"Organization": M_AUTOR, **({"ImageObject": M_LOGO} if "ImageObject" in json.dumps(doc["jsonld"]) else {})},
                        "hero": HERO}


def pagina(slug):
    return _Pagina(slug)
