"""Plantilla de documento legal (spec §3.3): ruta visible → H1 con la fecha de actualización → índice y secciones con
anclas estables (#envios, #devoluciones, #garantia-plantas, #garantia-pasto, #mensualidades…) → CTA final. Páginas:
/politicas y /politica-privacidad. <body class="vt-pagina vt-util">: el shell agrega terra-util.css."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def render(k):
    cuerpo = [cu.cabeza(k["cabeza"]), cu.documento_legal(k["secciones"])]
    if k.get("cierre"):
        ci = k["cierre"]
        cuerpo.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]))
    return base.documento(k["meta"], "\n".join(cuerpo), jsonld_bloques=k["jsonld"], clase_body=CLASE_BODY)
