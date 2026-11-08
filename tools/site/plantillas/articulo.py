"""Plantilla de artículo del blog (spec §3.3): migas → H1 → autor y fecha → respuesta directa → cuerpo con columna de margen
(índice) y Notas de campo → preguntas → enlaces contextuales → etiqueta de producto relacionado y CTA a una landing →
relacionados. Los 52 artículos: tools/site/contenido/articulo.py."""
import re

import componentes as c
import componentes_blog as cb
from plantillas import base


def render(k):
    faq = f'<h2 id="preguntas">{k["faq_titulo"]}</h2>{c.faq(k["faq"])}' if k["faq"] else ""
    cuerpo = (f'<div class="vt-wrap vt-art"><article class="vt-art__cuerpo" aria-labelledby="vt-h1">{cb.respuesta(k["respuesta"])}'
              f'{k["cuerpo"]}{faq}{cb.enlaces(k["tema"]["enlaces"])}</article>'
              f'<aside class="vt-art__margen">{cb.indice(k["indice"])}</aside></div>')
    grafo = [n for n in k["jsonld"]["@graph"] if n.get("@type") != "FAQPage"]
    if k["faq"]:
        grafo.append(c.faq_jsonld(k["faq"]))
    html = "\n".join((cb.cabeza(k), cuerpo, cb.producto(k["tema"], k["mensaje"], k["tipo"]),
                      cb.relacionados(k["relacionados_titulo"] or "También te puede interesar", k["relacionados"])))
    return base.documento(k["meta"], html, jsonld_bloques=({"@context": "https://schema.org", "@graph": grafo},),
                          precargas=_precarga(k["cuerpo"]), clase_body="vt-pagina vt-blog")


def _precarga(cuerpo):
    m = re.search(r'<img src="([^"]+)"', cuerpo)
    return (base.precarga_imagen({"src": m.group(1)}),) if m else ()
