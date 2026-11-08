"""Plantilla de artículo del blog (spec §3.3): migas → H1 → autor y fecha → respuesta directa → cuerpo con columna de margen
(índice) y Notas de campo → preguntas → enlaces contextuales → etiqueta de producto relacionado y CTA a una landing →
relacionados. Los 52 artículos: tools/site/contenido/articulo.py."""
import re

import componentes as c
import componentes_blog as cb
import datos
from plantillas import base

NEGOCIO = {"@id": f"{datos.SITIO}/#negocio"}


def render(k):
    faq = f'<h2 id="preguntas">{k["faq_titulo"]}</h2>{c.faq(k["faq"])}' if k["faq"] else ""
    cuerpo = (f'<div class="vt-wrap vt-art"><article class="vt-art__cuerpo" aria-labelledby="vt-h1">{cb.respuesta(k["respuesta"])}'
              f'{cb.indice_movil(k["indice"])}{_con_cta_medio(k["cuerpo"], cb.cta_medio(k["tema"], k["tipo"]))}{faq}'
              f'{cb.enlaces(k["tema"]["enlaces"])}</article>'
              f'<aside class="vt-art__margen">{cb.indice(k["indice"])}{cb.cta_margen(k["tema"], k["tipo"])}</aside></div>')
    grafo = _grafo(k)
    html = "\n".join((cb.cabeza(k), cuerpo, cb.producto(k["tema"], k["mensaje"], k["tipo"]),
                      cb.relacionados(k["relacionados_titulo"] or "También te puede interesar", k["relacionados"])))
    return base.documento(k["meta"], html, jsonld_bloques=({"@context": "https://schema.org", "@graph": grafo},),
                          precargas=_precarga(k["cuerpo"]), clase_body="vt-pagina vt-blog")


def _con_cta_medio(cuerpo, cta):
    """El CTA va al cerrar la sección del segundo H2 (antes del tercero) para no separar un título de su texto; si el artículo
    tiene menos de tres H2, al final del cuerpo."""
    h2 = [m.start() for m in re.finditer(r"<h2\b", cuerpo)]
    pos = h2[2] if len(h2) > 2 else len(cuerpo)
    return f"{cuerpo[:pos]}{cta}{cuerpo[pos:]}"


def _migas_ld(k):
    """BreadcrumbList con el mismo texto que las migas visibles."""
    elementos = [{"@type": "ListItem", "position": n, "name": c.texto_plano(texto),
                  "item": f'{datos.SITIO}{href.rstrip("/")}' if href else k["meta"]["canonical"]}
                 for n, (texto, href) in enumerate(k["migas"], 1)]
    return {"@type": "BreadcrumbList", "itemListElement": elementos}


def _grafo(k):
    """Grafo del artículo: autor editorial y publisher por @id a #negocio; migas y preguntas salen de lo visible."""
    autor = {"@type": "Organization", "name": datos.AUTOR_BLOG}
    nodos = [{**n, "author": autor, "publisher": NEGOCIO} if n.get("@type") == "Article" else n
             for n in k["jsonld"]["@graph"] if n.get("@type") not in ("FAQPage", "BreadcrumbList")]
    return nodos + [_migas_ld(k)] + ([c.faq_jsonld(k["faq"])] if k["faq"] else [])


def _precarga(cuerpo):
    m = re.search(r'<img src="([^"]+)"', cuerpo)
    return (base.precarga_imagen({"src": m.group(1)}),) if m else ()
