"""Índice del blog: H1 y conteo del build, las mismas secciones y tarjetas de la página publicada y los servicios."""
import componentes as c
import componentes_blog as cb
from partials import esc
from plantillas import base


def lista_ld(secciones):
    """ItemList con cada artículo una sola vez, en el orden de la página."""
    articulos = {}
    for s in secciones:
        for t in s["tarjetas"]:
            articulos.setdefault(t["href"], t["titulo"])
    return {"@context": "https://schema.org", "@type": "ItemList", "name": "Artículos del blog de Viveros Terra",
            "numberOfItems": len(articulos),
            "itemListElement": [{"@type": "ListItem", "position": n, "name": titulo, "url": f"{c.datos.SITIO}{href}"}
                                for n, (href, titulo) in enumerate(articulos.items(), 1)]}


def render(k):
    f = k["foto"]
    portada = (f'<section class="vt-blog-p" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}<div class="vt-blog-p__g"><div>'
               f'<p class="vt-kicker"><span data-vt-conteo="blog">52</span> guías · {c.datos.AUTOR_BLOG}</p><h1 id="vt-h1">{k["h1"]}</h1>'
               f'<p class="vt-lede">{k["lede"]}</p>{c.fila_cta(k["mensaje"], k["tipo"], "hero", hero=True)}</div>'
               f'<img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="{esc(f["alt"])}" loading="eager" fetchpriority="high" decoding="async">'
               f'</div></div></section>')
    secciones = []
    for n, s in enumerate(k["secciones"], 1):
        tarjetas = "".join(cb.tarjeta_indice(t) for t in s["tarjetas"])
        secciones.append(c.bloque(n, "Blog", f"vt-h-b{n}", s["titulo"], f'<ul class="vt-blog-l">{tarjetas}</ul>', tinte=n % 2 == 0))
    servicios = "".join(f'<li><a href="{esc(h)}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in k["servicios"])
    secciones.append(c.bloque(len(k["secciones"]) + 1, "Servicios", "vt-h-serv", "¿Buscas servicio profesional en Tampico?",
                              f'<ul class="vt-blog-s">{servicios}</ul>' + c.fila_cta(k["mensaje"], k["tipo"], "cierre")))
    return base.documento(k["meta"], portada + "\n".join(secciones), precargas=(base.precarga_imagen({"src": f["src"]}),), jsonld_bloques=(k["jsonld"], lista_ld(k["secciones"])),
                          clase_body="vt-pagina vt-blog")
