"""Los artículos del blog (Etapa 2h: 52; desde la SEO fase 2c, 49 tras cinco fusiones con 301). El cuerpo vive en contenido/blog/<slug>.html (HTML con un comentario de metadatos
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
NUEVOS = ("palma-bambu-chamaedorea-tampico", "plantas-seguras-mascotas-jardin-tampico",
          # SEO fase 2c (2026-11-11): la lista única de palmas, fusión con 301 de dos artículos (contenido/blog_seo_f2c.py).
          "palmas-para-jardin-tampico")
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
HERO = ("Hero de lectura: titular en la escala común del sitio, lema en serif («Lo que nos preguntan en el vivero, contestado.», "
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
            "portada": PORTADAS.get(slug),
        }
        self.PARIDAD = {**(doc.get("paridad") or {"reemplazos": {}, "retirados": {}}), "jsonld": {"Organization": M_AUTOR, **({"ImageObject": M_LOGO} if "ImageObject" in json.dumps(doc["jsonld"]) else {})},
                        "hero": HERO, "terreno": TERRENO, "ritmo": RITMO, **({"portada": PORTADA} if slug in PORTADAS else {})}


ANCHO_MOVIL = 640  # ancho de la copia
UMBRAL_COPIA = 720  # solo las fotos más anchas llevan copia: las de 720 px o menos ya son ligeras (40–50 KB) y nunca se agrandan


def ruta_movil(src):
    """Copia de 640 px de la foto (tools/site/portadas_blog.py): mismo nombre con -640.webp."""
    return src.rsplit(".", 1)[0] + "-640.webp"


def _con_copia(foto):
    return {**foto, "src_movil": ruta_movil(foto["src"])} if int(foto["ancho"]) > UMBRAL_COPIA else dict(foto)


def _portadas():
    """Plan visual V4 (decisión del dueño del 2026-11-11): cada artículo lleva de portada la foto que ya tiene su tarjeta
    en el índice del blog. No la llevan los que no tienen foto en el índice (nunca una inventada) ni los que ya muestran
    esa misma foto en su cuerpo (no se repite)."""
    from contenido import blog_indice
    fotos = {}
    for s in blog_indice.CONTENIDO["secciones"]:
        for t in s["tarjetas"]:
            if t.get("foto"):
                fotos.setdefault(t["href"].rstrip("/").removeprefix("/blog/"), t["foto"])
    return {slug: _con_copia(fotos[slug]) for slug in CLAVES
            if slug in fotos and fotos[slug]["src"] not in leer(slug)[1]}


PORTADAS = _portadas()
PORTADA = ("Plan visual V4 (decisión del dueño del 2026-11-11): portada con la misma foto de la tarjeta del artículo en el "
           "índice del blog (a la derecha del título en computadora, bajo los enlaces en celular).")

RITMO = ("Entrega C de experiencia (2026-11-10), ritmo y movimiento: WhatsApp de texto junto al CTA de media lectura y una "
         "línea «Preguntar por WhatsApp» cada 3 secciones después (antes, 7.6 pantallas sin WhatsApp en línea); revelado por "
         "scroll de los encabezados.")
# Decisión del dueño del 2026-11-10 (terreno listo y garantía de arraigo), en los artículos que dan el precio del instalado.
TERRENO = ("decisión del dueño 2026-11-10: el instalado considera terreno listo; trabajos previos se cotizan aparte: la etiqueta y la entrada del tema pasto llevan datos.TERRENO_LISTO_CORTO; en «¿Cuánto cuesta hacer un "
           "jardín…?» y «Jardín con bajo presupuesto» las filas del instalado dicen la condición (antes «El instalado "
           "incluye preparación básica»). decisión del dueño 2026-11-10: la garantía de arraigo aplica con terreno listo: en «Errores del pasto San Agustín» la garantía es datos.GARANTIA_PASTO.")


def pagina(slug):
    return _Pagina(slug)
