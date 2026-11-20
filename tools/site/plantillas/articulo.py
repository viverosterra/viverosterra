"""Plantilla de artículo del blog (spec §3.3): migas → H1 → autor y fecha → respuesta directa → cuerpo con columna de margen
(índice) y Notas de campo → preguntas → enlaces contextuales → etiqueta de producto relacionado y CTA a una landing →
relacionados. Los 52 artículos: tools/site/contenido/articulo.py."""
import re

import componentes as c
import componentes_blog as cb
import datos
import entidad
import preguntas_wa as pw
from contenido import blog_clusters
from plantillas import base

NEGOCIO = entidad.REF


def render(k):
    # Auditoría por página (2026-11-20): una línea de WhatsApp antes de las preguntas cierra el último tramo sin botón
    # (4.3–5 pantallas del celular entre la última línea y el cierre).
    faq = (f'{cb.cta_lectura(k["mensaje"], k["tipo"], "preguntas", k["tema"])}<h2 id="preguntas">{k["faq_titulo"]}</h2>'
           f'{c.faq(k["faq"])}' if k["faq"] else "")
    cuerpo = (f'<div class="vt-wrap vt-art"><article class="vt-art__cuerpo" aria-labelledby="vt-h1">{cb.respuesta(k["respuesta"])}'
              f'{cb.indice_movil(k["indice"])}{cb.fotos_cuerpo(_con_cta_medio(k["cuerpo"], cb.cta_medio(k["tema"], k["tipo"], k["mensaje"]), k))}{faq}'
              f'{cb.enlaces(k["tema"]["enlaces"])}</article>'
              f'<aside class="vt-art__margen">{cb.indice(k["indice"])}{cb.cta_margen(k["tema"], k["tipo"])}</aside></div>')
    grafo = _grafo(k)
    html = "\n".join((cb.cabeza(k), cuerpo, cb.producto(k["tema"], k["mensaje"], k["tipo"]),
                      cb.relacionados(k["relacionados_titulo"] or "También te puede interesar", k["relacionados"])))
    # Spec del primer mensaje de WhatsApp (2026-11-16): las guías de pasto sintético llevan el panel de preguntas.
    sintetico = k.get("slug") in blog_clusters._SINTETICOS
    return base.documento(base.meta_de(k), html, jsonld_bloques=({"@context": "https://schema.org", "@graph": grafo},),
                          precargas=_precarga(k), scripts=pw.scripts() if sintetico else (),
                          head_extra=(pw.json_pagina({}),) if sintetico else (),
                          clase_body="vt-pagina vt-blog" + (pw.CLASE if sintetico else ""))


# Entrega C de experiencia: además del CTA de media lectura, una línea discreta de WhatsApp al empezar una sección (antes
# de un H2 o un H3, nunca a media sección) cada vez que se acumulan unos LECTURA_PESO caracteres de lectura (texto; cada
# imagen y cada tabla cuentan como un tramo de texto), para que ningún tramo del celular pase de 6 pantallas sin un
# WhatsApp en línea. Medido a 375 px: ~1,000 caracteres por pantalla.
# Auditoría por página (2026-11-20): 1,500 (antes 2,400) para no pasar de unas 3 pantallas sin botón.
LECTURA_PESO = 1500
PESO_IMAGEN, PESO_TABLA = 400, 900
# Auditoría por página (2026-11-20): cada renglón de lista o de tabla ocupa al menos un renglón de pantalla aunque traiga
# poco texto (los ejemplos de presupuesto medían 3.5 pantallas con poco peso).
PESO_RENGLON = 80
CORTE_RE = re.compile(r"<h[23]\b")


def _peso(fragmento):
    texto = re.sub(r"<[^>]+>", "", fragmento)
    return (len(texto) + PESO_IMAGEN * fragmento.count("<img") + PESO_TABLA * fragmento.count("<table")
            + PESO_RENGLON * (fragmento.count("<li") + fragmento.count("<tr")))


def _con_cta_medio(cuerpo, cta, k):
    """El CTA va al cerrar la sección del segundo H2 (antes del tercero) para no separar un título de su texto; si el artículo
    tiene menos de tres H2, al final del cuerpo. Las líneas de lectura van antes de los H2 o H3 donde el peso acumulado
    desde el último CTA llega a LECTURA_PESO (no a menos de un tercio de LECTURA_PESO del final)."""
    h2 = [m.start() for m in re.finditer(r"<h2\b", cuerpo)]
    medio = h2[2] if len(h2) > 2 else len(cuerpo)
    precio = _fin_de_precio(cuerpo, h2)
    cortes, previo, n = [], 0, 0
    for pos in sorted({m.start() for m in CORTE_RE.finditer(cuerpo)} | {medio} | ({precio} - {medio, None})):
        if pos == medio:
            cortes.append((pos, cta))
            previo = pos
        elif pos == precio or (_peso(cuerpo[previo:pos]) >= LECTURA_PESO and _peso(cuerpo[pos:]) >= LECTURA_PESO / 3):
            n += 1
            cortes.append((pos, cb.cta_lectura(k["mensaje"], k["tipo"], n, k["tema"])))
            previo = pos
    salida, desde = [], 0
    for pos, html in cortes:
        salida += [cuerpo[desde:pos], html]
        desde = pos
    return "".join(salida) + cuerpo[desde:]


def _fin_de_precio(cuerpo, h2):
    """Auditoría por página (2026-11-20): donde termina la sección «¿Cuánto cuesta…?» (<h2 id="precio">), el siguiente
    <h2>: ahí va siempre una línea de WhatsApp, junto al precio. None si el artículo no tiene esa sección."""
    inicio = cuerpo.find('<h2 id="precio"')
    return next((pos for pos in h2 if pos > inicio), None) if inicio >= 0 else None


def _migas_ld(k):
    """BreadcrumbList con el mismo texto que las migas visibles."""
    elementos = [{"@type": "ListItem", "position": n, "name": c.texto_plano(texto),
                  "item": f'{datos.SITIO}{href.rstrip("/")}' if href else k["meta"]["canonical"]}
                 for n, (texto, href) in enumerate(k["migas"], 1)]
    return {"@type": "BreadcrumbList", "itemListElement": elementos}


def _grafo(k):
    """Grafo del artículo: autor editorial y publisher por @id a #negocio; migas y preguntas salen de lo visible."""
    nodos = [_articulo_ld(k, n) if n.get("@type") == "Article" else n
             for n in k["jsonld"]["@graph"] if n.get("@type") not in ("FAQPage", "BreadcrumbList")]
    return nodos + [_migas_ld(k)] + ([c.faq_jsonld(k["faq"])] if k["faq"] else [])


def _articulo_ld(k, nodo):
    """Article completo (SEO fase 1): autor y publisher son la entidad única por @id (la firma visible sigue siendo
    datos.AUTOR_BLOG); la descripción que falte es la de la página; la imagen que falte es la primera foto del cuerpo
    o, si el artículo no muestra ninguna, la que ya declara en su og:image (nunca una inventada); las fechas son las
    del encabezado de la fuente (sin dateModified, la de publicación); mainEntityOfPage es el WebPage de la página."""
    meta = k["meta"]
    foto = re.search(r'<img src="([^"]+)"', k["cuerpo"])
    imagen = nodo.get("image") or (f"{datos.SITIO}{foto.group(1)}" if foto else dict(meta["og"]).get("og:image"))
    completo = {**nodo, "description": nodo.get("description") or meta["description"],
                "datePublished": k["publicado_iso"], "dateModified": k["actualizado_iso"],
                "mainEntityOfPage": {"@id": meta["canonical"]}, "inLanguage": entidad.IDIOMA,
                "author": NEGOCIO, "publisher": NEGOCIO}
    return {**completo, "image": imagen} if imagen else completo


def _precarga(k):
    f = k.get("portada")
    if f:  # plan visual V4: la portada es la primera imagen y el LCP
        return (base.precarga_imagen({"src": f["src"], "srcset": cb.portada_srcset(f), "sizes": cb.PORTADA_SIZES}),)
    # Auditoría por página (2026-11-20): sin portada no se precarga nada; la primera foto del cuerpo está a unas dos
    # pantallas y competía con el titular.
    return ()
