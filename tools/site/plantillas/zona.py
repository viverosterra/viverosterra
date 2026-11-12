"""Plantilla de zona (spec §3.3): ruta visible → H1 "Jardinería en {zona}" con el precio ancla en la etiqueta y CTA con
la plantilla de la zona → los 4 servicios que más pide la zona con precio (de datos.py; los demás, en /precios) → lo que pide un jardín en
esta zona (el problema local) → colonias atendidas con su código postal → preguntas → otras zonas → CTA final.

Del orden del spec no entran, por regla del dueño: el caso real de la zona (ninguno tiene permiso; se agrega con su
prueba cuando el dueño lo dé) y el tiempo desde el vivero (sin distancias ni tiempos de llegada). Páginas: las 6
/jardineria-* (tools/site/contenido/zona.py). Sin hoja propia: todo sale de terra.css."""
import componentes as c
import componentes_zonas as cz
from plantillas import base

CONTEXTO = "https://schema.org"
VER_LISTA = ' <a href="/precios">Lista de precios de jardinería en Tampico</a>'


def render(k):
    tipo = k["tipo"]
    pr, re_, co, f, cb, ci = (k[x] for x in ("precios", "retos", "colonias", "faq", "cobertura", "cierre"))
    secciones = [
        c.portada(k["portada"], tipo, k["migas"]),
        c.bloque(1, "Precios", "vt-h-precios", pr["titulo"],
                 cz.lista(pr["filas"], pr["caption"])
                 + cz.cotizar(*pr["cotizar"], f"{tipo}:precios", despues=VER_LISTA) + f'<p class="vt-promesa">{pr["nota"]}</p>',
                 lede=pr["lede"], tinte=True, id_seccion="precios"),
        c.bloque(2, "Tu jardín", "vt-h-zona", re_["titulo"], c.fichas(re_["items"]), lede=re_.get("lede"), id_seccion="zona"),
        c.bloque(3, "Colonias", "vt-h-colonias", co["titulo"],
                 cz.colonias(co["items"], f"Colonias y códigos postales de {co['municipio']} (SEPOMEX)."),
                 lede=co["lede"], tinte=True, id_seccion="colonias"),
        c.bloque_dos(4, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), id_seccion="preguntas"),
        c.bloque(5, "Zonas", "vt-h-zonas", cb["titulo"], c.cobertura(cb["zonas"], cb["por_proyecto"]), lede=cb["lede"],
                 tinte=True),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    j = k["jsonld"]
    grafo = [j["migas"], j["servicio"], c.faq_jsonld(f["preguntas"])]
    return base.documento(base.meta_de(k), "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),))
