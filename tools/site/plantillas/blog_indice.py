"""Índice del blog: H1 y conteo del build, las mismas secciones y tarjetas de la página publicada y los servicios."""
import componentes as c
import componentes_blog as cb
import entidad
from partials import esc
from plantillas import base


def blog_ld(publicado):
    """Blog como estaba publicado, con el publisher por @id a la entidad única (SEO fase 1; antes, una Organization
    suelta con su logo)."""
    return {**{clave: valor for clave, valor in publicado.items() if clave != "@context"}, "publisher": entidad.REF}


def lista_ld(secciones):
    """ItemList con cada artículo una sola vez, en el orden de la página."""
    articulos = {}
    for s in secciones:
        for t in s["tarjetas"]:
            articulos.setdefault(t["href"], t["titulo"])
    return {"@type": "ItemList", "name": "Artículos del blog de Viveros Terra",
            "numberOfItems": len(articulos),
            "itemListElement": [{"@type": "ListItem", "position": n, "name": titulo, "url": f"{c.datos.SITIO}{href}"}
                                for n, (href, titulo) in enumerate(articulos.items(), 1)]}


CADA_FILA = 12
FILA_TEXTO = "¿Tienes una duda de tu jardín? Mándanos foto, colonia y metros."


def _fila_wa(k, n):
    """Renglón de la lista con un enlace de WhatsApp de texto: no interrumpe la lectura ni compite con las tarjetas."""
    enlace = c.wa_texto(k["mensaje"], f'{k["tipo"]}:lista-{n}', "Preguntar por WhatsApp")
    return f'<li class="vt-blog-fila" data-hero-cta><p>{FILA_TEXTO} {enlace}</p></li>'


def render(k):
    f = k["foto"]
    # Cabecera de lectura: titular con su lema en serif y el WhatsApp como enlace de texto (sin botón grande).
    portada = (f'<section class="{c.clase_titular(k["h1"], "vt-blog-p")}" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}<div class="vt-blog-p__g"><div>'
               f'<p class="vt-kicker"><span data-vt-conteo="blog">52</span> guías · {c.datos.AUTOR_BLOG}</p><h1 id="vt-h1">{k["h1"]}</h1>'
               f'<p class="vt-lede">{k["lede"]}</p>{c.enlaces_portada((c.enlace_wa(k["mensaje"], k["tipo"] + ":hero"),), k["tipo"])}</div>'
               f'<img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="{esc(f["alt"])}" loading="eager" fetchpriority="high" decoding="async">'
               f'</div></div></section>')
    secciones, contadas = [], 0
    total = sum(len(s["tarjetas"]) for s in k["secciones"])
    for n, s in enumerate(k["secciones"], 1):
        tarjetas = []
        for t in s["tarjetas"]:
            tarjetas.append(cb.tarjeta_indice(t))
            contadas += 1
            # Entrega C de experiencia: una fila discreta de WhatsApp cada CADA_FILA tarjetas (antes, 25 pantallas del
            # celular sin un CTA en línea); no tras la última, que ya tiene la de servicios.
            if contadas % CADA_FILA == 0 and contadas < total:
                tarjetas.append(_fila_wa(k, contadas // CADA_FILA))
        secciones.append(c.bloque(n, "Blog", f"vt-h-b{n}", s["titulo"], f'<ul class="vt-blog-l">{"".join(tarjetas)}</ul>',
                                  tinte=n % 2 == 0))
    servicios = "".join(f'<li><a href="{esc(h)}"><b>{t}</b><span>{d}</span></a></li>' for h, t, d in k["servicios"])
    secciones.append(c.bloque(len(k["secciones"]) + 1, "Servicios", "vt-h-serv", "¿Buscas servicio profesional en Tampico?",
                              f'<ul class="vt-blog-s">{servicios}</ul>' + c.fila_cta(k["mensaje"], k["tipo"], "cierre")))
    return base.documento(base.meta_de(k), portada + "\n".join(secciones), precargas=(base.precarga_imagen({"src": f["src"]}),), jsonld_bloques=({"@context": "https://schema.org", "@graph": [blog_ld(k["jsonld"]), lista_ld(k["secciones"])]},),
                          clase_body="vt-pagina vt-blog")
