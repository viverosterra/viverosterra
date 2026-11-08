"""Plantilla de 404.html (spec §4.x): dice qué pasó, filtra servicios sin salir de la página (vt-404.js; sin JS se ve la
lista completa) y ofrece WhatsApp. El menú y el pie los pone el shell. Vercel sirve 404.html en toda ruta sin archivo."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"
SCRIPTS = ("/js/vt-404.js",)


def render(k):
    filas = "".join(f'<li data-vt-servicio-404><a href="{c.esc(h)}">{t}</a></li>' for t, h in k["servicios"])
    buscador = (f'<section class="vt-bloque" aria-labelledby="vt-h-buscar"><div class="vt-wrap vt-util__estrecho">'
                f'<h2 id="vt-h-buscar">{k["buscar"]["titulo"]}</h2><div class="vt-campo"><label for="vt-buscar-404">'
                f'{k["buscar"]["label"]}</label><div class="vt-control"><input id="vt-buscar-404" type="search" '
                f'autocomplete="off" placeholder="{c.esc(k["buscar"]["placeholder"])}"></div></div>'
                f'<ul class="vt-util__servicios" id="vt-lista-404">{filas}</ul>'
                f'<p class="vt-promesa" id="vt-vacio-404" role="status" hidden>{k["buscar"]["vacio"]}</p></div></section>')
    ci = k["cierre"]
    return base.documento(k["meta"], "\n".join((cu.cabeza(k["cabeza"]), buscador, c.cierre(ci["titulo"], ci["lede"],
                          ci["mensaje"], k["tipo"]))), scripts=SCRIPTS, clase_body=CLASE_BODY)
