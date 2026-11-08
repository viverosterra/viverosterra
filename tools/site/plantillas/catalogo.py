"""Plantilla del catálogo "Arma tu lista" (spec §3.3): ruta visible y H1 → precios publicados (palmas y flamboyán, de
datos.py) y CTA → buscador y filtros arriba (estado en la URL) → una sola rejilla en el HTML (foto o marcador «Foto
pendiente», nombre, científico, luz/riego/altura, "+ Añadir a mi lista" como <button>) → pedido de una especie que no
está → otras páginas (pasto y materiales) → garantía con condiciones. La lista se arma en <dialog> y sale en un solo
WhatsApp (public/js/vt-catalogo.js, el mismo mensaje que sendWA() de main). Los datos que necesita el JS (nombre,
científico y tamaños por especie) van en <script type="application/json" id="vt-catalogo-datos">."""
import json

import componentes as c
import componentes_plantas as cp
import datos
from contenido import catalogo_datos as cd
from plantillas import base
from plantillas.hub_categoria import pagina_ld

CONTEXTO = "https://schema.org"


def datos_js():
    lista = {e["slug"]: {"name": e["name"], "sc": e["sc"], "sz": e["sz"]} for e in cd.ORDENADAS}
    texto = json.dumps(lista, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="vt-catalogo-datos">{texto}</script>'


def render(k):
    tipo, ca = k["tipo"], k["cabeza"]
    cabeza = (f'<section class="vt-bloque vt-cat__cabeza" aria-labelledby="vt-h1"><div class="vt-wrap">'
              f'{c.migas(k["migas"])}<h1 id="vt-h1">{ca["h1"]}</h1><p class="vt-lede">{ca["lede"]}</p>'
              f'<p class="vt-cat__precios">{ca["precios"]}</p>{c.fila_cta(ca["mensaje"], tipo, "hero", hero=True)}'
              '</div></section>')
    rejilla = (f'<section class="vt-bloque vt-cat__rejilla" aria-labelledby="vt-h-rejilla"><div class="vt-wrap">'
               f'<h2 id="vt-h-rejilla" class="vt-sr">{k["rejilla"]["titulo"]}</h2>'
               f'{cp.filtros_catalogo(len(cd.ESPECIES))}{cp.rejilla_catalogo(tipo=tipo)}</div></section>')
    p = k["pedido"]
    pedido = c.bloque(1, "¿No está?", "vt-h-pedido", p["titulo"], cp.pedido_especial(tipo), lede=p["lede"], tinte=True)
    r = k["relacionados"]
    otras = c.bloque(2, "También", "vt-h-rel", r["titulo"], c.relacionados(r["items"]))
    garantia = (f'<section class="vt-bloque" aria-label="Garantía"><div class="vt-wrap"><p class="vt-promesa">'
                f'<b>Garantía:</b> {datos.GARANTIA_PLANTAS} <a href="/politicas#garantia-plantas">Condiciones</a></p>'
                '</div></section>')
    j = k["jsonld"]
    # Cada ListItem apunta a su tarjeta (<li id="<slug>"> de componentes_plantas.tarjeta_catalogo).
    elementos = [{"@type": "ListItem", "position": i, "name": e["name"], "url": f'{j["url"]}#{e["slug"]}'}
                 for i, e in enumerate(cd.ORDENADAS, 1)]
    grafo = [pagina_ld(j["url"]),
             {"@type": "ItemList", "name": j["nombre"], "description": j["descripcion"], "url": j["url"],
              "numberOfItems": len(elementos), "itemListElement": elementos}, j["migas"]]
    return base.documento(k["meta"], "\n".join((cabeza, rejilla, pedido, otras, garantia)),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},), head_extra=(datos_js(),),
                          tras_main=cp.lista_catalogo(tipo), scripts=("/js/vt-catalogo.js",),
                          clase_body="vt-pagina vt-plantas")
