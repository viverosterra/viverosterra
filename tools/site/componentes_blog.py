"""Componentes del artículo y del índice del blog (Etapa 2h)."""
import componentes as c
import datos
from partials import esc

P = datos.PRECIOS
SERVICIOS = ("riego", "diseno", "mantenimiento")


def cabeza(k):
    dek = f'<p class="vt-art__dek">{k["dek"]}</p>' if k["dek"] else ""
    rotulo = "Actualizado" if k["actualizado_iso"] != k["publicado_iso"] else "Publicado"
    fechas = f'<span><b>{rotulo}</b> <time datetime="{esc(k["actualizado_iso"])}">{k["actualizado"]}</time></span>'
    tiempo = f'<span>{k["minutos"]} min de lectura</span>' if k["minutos"] else ""
    return (f'<header class="vt-art__cabeza"><div class="vt-wrap">{c.migas(k["migas"])}<p class="vt-kicker">{k["kicker"]}</p>'
            f'<h1 id="vt-h1">{k["h1"]}</h1>{dek}<p class="vt-art__meta"><span><b>Por</b> {esc(k["autor"])}</span>{fechas}{tiempo}</p>'
            f'</div></header>')


def respuesta(r):
    if not r:
        return ""
    tag = "h2" if r["es_titulo"] else "p"
    clase = ' class="vt-art__respuesta-t"'
    parrafos = "".join(f"<p>{p}</p>" for p in r["parrafos"])
    return f'<section id="respuesta" class="vt-art__respuesta"><{tag}{clase}>{r["titulo"]}</{tag}>{parrafos}</section>'


def indice(items):
    filas = "".join(f'<li><a href="#{esc(i)}"><span aria-hidden="true">{n:02d}</span>{t}</a></li>'
                    for n, (i, t) in enumerate(items))
    return f'<nav class="vt-art__indice" aria-label="En este artículo"><b>En este artículo</b><ol>{filas}</ol></nav>'


def indice_movil(items):
    """Índice para pantallas de menos de 1024 px: cerrado y después de la respuesta, así que no repite el enlace a ella."""
    filas = "".join(f'<li><a href="#{esc(i)}"><span aria-hidden="true">{n:02d}</span>{t}</a></li>'
                    for n, (i, t) in enumerate((x for x in items if x[0] != "respuesta"), 1))
    return (f'<details class="vt-art__toc"><summary class="vt-art__toc-t">En este artículo</summary>'
            f'<nav aria-label="En este artículo"><ol>{filas}</ol></nav></details>')


def cta_medio(tema, tipo):
    """CTA de texto a media lectura (solo menos de 1024 px); en escritorio lo sustituye cta_margen, bajo el índice fijo."""
    href, texto = tema["landing"]
    return (f'<aside class="vt-art__medio" aria-label="Siguiente paso"><p>{tema["titulo"]}</p>'
            f'<a data-cta="{tipo}:medio" href="{esc(href)}">{texto}<span class="vt-flecha" aria-hidden="true">→</span></a></aside>')


def cta_margen(tema, tipo):
    href, texto = tema["landing"]
    return (f'<p class="vt-art__margen-cta"><a data-cta="{tipo}:margen" href="{esc(href)}">{texto}'
            f'<span class="vt-flecha" aria-hidden="true">→</span></a></p>')


def enlaces(items):
    filas = "".join(f'<li><a href="{esc(h)}">{t}</a></li>' for t, h in items)
    return f'<nav class="vt-art__sigue" aria-label="Para seguir"><b>Para seguir</b><ul>{filas}</ul></nav>'


def etiqueta_de(tema):
    """"Servicio" en riego, diseño y mantenimiento; "Con IVA" solo si hay un precio al que aplique."""
    return {"codigo": "Servicio relacionado" if tema["tema"] in SERVICIOS else "Producto relacionado",
            "aviso": "" if tema["etiqueta"]["monto"] == datos.SEGUN_COTIZACION else "Con IVA", **tema["etiqueta"]}


def producto(tema, mensaje, tipo):
    href, texto = tema["landing"]
    return (f'<section class="vt-art__producto" aria-labelledby="vt-art-prod"><div class="vt-wrap vt-art__producto-grid"><div>'
            f'<h2 id="vt-art-prod">{tema["titulo"]}</h2><div class="vt-cta"><a class="vt-btn vt-btn--tinta" '
            f'data-cta="{tipo}:landing" href="{esc(href)}">{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>'
            f'{c.boton_wa(mensaje, f"{tipo}:cierre")}</div><p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p></div>'
            f'{c.etiqueta(etiqueta_de(tema))}</div></section>')


def relacionados(titulo, items):
    filas = "".join(f'<li><p class="vt-art__rel-c">{esc(i["categoria"])}</p><h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3>'
                    + (f'<p>{i["texto"]}</p>' if i["texto"] else "") + "</li>" for i in items)
    return (f'<section class="vt-art__rel" aria-labelledby="vt-art-rel"><div class="vt-wrap"><h2 id="vt-art-rel">{titulo}</h2>'
            f'<ul>{filas}</ul></div></section>')


def tarjeta_indice(t):
    foto = ""
    if t.get("foto"):
        f = t["foto"]
        foto = (f'<img src="{esc(f["src"])}" width="{f["ancho"]}" height="{f["alto"]}" alt="{esc(f["alt"])}" loading="lazy" '
                f'decoding="async">')
    minutos = f'<span>{t["minutos"]} min</span>' if t.get("minutos") else ""
    return (f'<li class="vt-blog-t{" vt-blog-t--foto" if foto else ""}">{foto}<div><p class="vt-art__rel-c">{esc(t["categoria"])}</p>'
            f'<h3><a href="{esc(t["href"])}">{t["titulo"]}</a></h3><p>{t["texto"]}</p>{minutos}</div></li>')
