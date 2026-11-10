"""Plantilla de la página de temporada de Nochebuenas (spec §4): portada → cotizador → tabla de precios → ¿para quién? →
galería → confianza → cómo funciona → cuidados → preguntas → datos de la planta → CTA final, más la barra fija móvil.

render(k, modo) arma los tres modos del spec §7; sin modo usa datos.NOCHEBUENAS["modo"]. public/js/vt-nochebuenas.js lee el
JSON incrustado y los atributos data-nb-*. <body class="vt-pagina vt-nochebuenas">: el shell agrega terra-nochebuenas.css.
"""
import itertools
import json

import componentes as c
import datos
from contenido.nochebuenas_fotos import FOTOS
from partials import WA_GLIFO, esc
from plantillas import base

CONTEXTO = "https://schema.org"
CLASE_BODY = "vt-pagina vt-nochebuenas"
SCRIPTS = ("/js/vt-nochebuenas.js",)
TIPO = "nochebuenas"
NB = datos.NOCHEBUENAS
CANTIDAD_INICIAL = 1
PRODUCTO_INICIAL = "6"
VARIEDAD_INICIAL = "Roja"
SIZES_HERO = "(min-width: 1024px) 560px, 100vw"
# Cuánto ocupa cada foto de la galería en escritorio (plantilla editorial, no rejilla uniforme): ver .vt-nb-galeria.
# Por pares: las fotos impares a 7 de 12 columnas y las pares a 5, un poco más abajo.
SIZES_GALERIA = {"detalle": "(min-width: 1024px) 58vw, 100vw", "grupo": "(min-width: 1024px) 34vw, 100vw",
                 "invernadero": "(min-width: 1024px) 58vw, 100vw", "bracteas": "(min-width: 1024px) 34vw, 100vw",
                 "hileras": "(min-width: 1024px) 58vw, 100vw", "kraft": "(min-width: 1024px) 34vw, 100vw"}
SIN_MODO_COTIZADOR = "postemporada"


def _meta(k, modo):
    return k["meta_postemporada"] if modo == SIN_MODO_COTIZADOR else k["meta"]


def _foto(f, numero, sizes):
    return dict(f, numero=numero, lugar=f["rotulo"], etapa="", sizes=sizes)


def _wa(mensaje):
    return esc(datos.wa_url(datos.con_firma(mensaje)))


def _boton_wa(mensaje, cta, texto, clase="vt-btn vt-btn--linea"):
    return (f'<a class="{clase}" data-cta="{esc(cta)}" href="{_wa(mensaje)}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}{texto}</a>')


def _portada(k, modo):
    p, abierta = k["portadas"][modo], modo != SIN_MODO_COTIZADOR
    hero = next(f for f in FOTOS if f["uso"] == "hero")
    if abierta:
        principal = (f'<a class="vt-btn vt-btn--wa" data-cta="{TIPO}:hero" href="#cotizador">{p["cta"]}'
                     '<span class="vt-flecha" aria-hidden="true">→</span></a>')
        ctas = principal + _boton_wa(k["mensajes"][modo], f"{TIPO}:hero", p["wa"])
        trato = (f'<div class="vt-portada__trato">{c.etiqueta(k["etiquetas"][modo])}<div><div class="vt-cta" data-hero-cta>{ctas}</div>'
                 f'<p class="vt-portada__tambien">{k["mismo_precio"]}</p></div></div>')
    else:
        ctas = _boton_wa(k["mensajes"][modo], f"{TIPO}:hero", k["aviso"], "vt-btn vt-btn--wa")
        trato = f'<div class="vt-portada__trato"><div class="vt-cta" data-hero-cta>{ctas}</div></div>'
    return (f'<section class="vt-portada vt-nb-portada" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-portada__grid"><div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1>'
            f'<p class="vt-lede">{p["lede"]}</p>{trato}</div>'
            f'<div class="vt-portada__foto">{c.figura(_foto(hero, 1, SIZES_HERO), principal=True)}</div></div>'
            f'{c.cuadro_datos(k["franja"])}</div></section>')


def _opciones(pares, elegido=None):
    return "".join(f'<option value="{esc(v)}"{" selected" if v == elegido else ""}>{esc(t)}</option>' for v, t in pares)


def _precio_inicial():
    return next(p["precios"][0] for p in NB["productos"] if p["clave"] == PRODUCTO_INICIAL)


def _linea():
    """Fila inicial que vt-nochebuenas.js clona: los <label> envuelven su control, sin id ni for."""
    productos = _opciones(((p["clave"], p["nombre"]) for p in NB["productos"]), PRODUCTO_INICIAL)
    variedades = _opciones(((v, v) for v in NB["variedades"]), VARIEDAD_INICIAL)
    precio = _precio_inicial()
    return (f'<div class="vt-nb-linea" data-nb-linea><label class="vt-nb-campo"><span>Tamaño</span>'
            f'<select data-nb-campo="producto">{productos}</select></label><label class="vt-nb-campo"><span>Variedad</span>'
            f'<select data-nb-campo="variedad">{variedades}</select></label><div class="vt-nb-cant">'
            '<button type="button" class="vt-nb-paso" data-nb-accion="menos" aria-label="Una pieza menos">−</button>'
            f'<label class="vt-nb-cant__campo"><span>Piezas</span><input type="number" inputmode="numeric" min="0" max="9999" '
            f'data-nb-campo="cantidad" value="{CANTIDAD_INICIAL}"></label>'
            '<button type="button" class="vt-nb-paso" data-nb-accion="mas" aria-label="Una pieza más">+</button></div>'
            f'<p class="vt-nb-linea__sub"><span>Subtotal</span><b data-nb-o="subtotal">{c.dinero(precio * CANTIDAD_INICIAL)}</b>'
            f'<small data-nb-o="unitario">{CANTIDAD_INICIAL} × {c.dinero(precio)}</small></p>'
            '<button type="button" class="vt-nb-quitar" data-nb-accion="quitar" aria-label="Quitar esta línea" hidden>Quitar</button>'
            "</div>")


def _extras():
    zonas = _opciones((("", "Elige tu zona"), *((z, z) for z in NB["zonas"])), "")
    tipos = _opciones((("", "Elige una opción"), *((t, t) for t in NB["tipos_cliente"])), "")
    return ('<details class="vt-nb-extras" data-nb-extras><summary><span aria-hidden="true">▾&nbsp;</span>Para afinar tu cotización (opcional)</summary><div class="vt-nb-extras__rejilla">'
            f'<label class="vt-nb-campo"><span>Zona de entrega</span><select data-nb-campo="zona">{zonas}</select></label>'
            '<label class="vt-nb-campo"><span>Fecha deseada</span><input type="date" data-nb-campo="fecha"></label>'
            f'<label class="vt-nb-campo"><span>Tipo de cliente</span><select data-nb-campo="tipo">{tipos}</select></label>'
            f'<label class="vt-nb-check"><input type="checkbox" data-nb-campo="factura"><span>Requiero factura {datos.FACTURA}</span></label>'
            "</div></details>")


AVISOS = (("ahorro", "ahorro"), ("preventa", "tag"), ("entrega", ""), ("sobre-pedido", ""), ("proyecto", ""), ("maximo", "alerta"))


def _aviso(nombre, tono, extra=""):
    return f'<p class="vt-nb-aviso{f" vt-nb-aviso--{tono}" if tono else ""}"{extra} data-nb-o="{nombre}" hidden></p>'


def _ticket(k, modo):
    inicial = _precio_inicial() * CANTIDAD_INICIAL
    etiqueta = c.etiqueta({
        "codigo": "Tu pedido", "aviso": f'Temporada {NB["temporada"]}', "nombre": '<span data-nb-o="piezas">1 pieza</span>',
        "cientifico": '<span data-nb-o="desglose" hidden></span>',
        "antes": "Total estimado", "monto": f'<span data-nb-o="total">{c.dinero(inicial)}</span>', "unidad": "MXN",
        "filas": (("Escalón", f'<span data-nb-o="escalon">{NB["nombres_escalon"][0]}</span>'),),
    }, cordel=False)
    subir = '<button type="button" class="vt-btn vt-btn--linea vt-nb-subir" data-nb-accion="subir" hidden></button>'
    avisos = _aviso("nudge", "nudge") + subir + "".join(_aviso(nombre, tono) for nombre, tono in AVISOS)
    vacio = _aviso("vacio", "alerta", ' id="nb-aviso-vacio" aria-live="polite"')
    cta = (f'<a class="vt-btn vt-btn--wa vt-nb-enviar" data-cta="{TIPO}:cotizador" href="{_wa(k["mensajes"][modo])}" target="_blank" '
           f'rel="noopener">{WA_GLIFO}{k["cotizador"]["cta"][modo]}</a>')
    return (f'<div class="vt-nb-ticket" id="nb-ticket">{etiqueta}{cta}{vacio}<div class="vt-nb-avisos" aria-live="polite">{avisos}</div>'
            f'<p class="vt-promesa">{k["cotizador"]["nota"]}</p><p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p></div>')


def _cotizador(k, modo, n):
    x = k["cotizador"]
    atributo_modo = ' data-nb-modo="preventa"' if modo == "preventa" else ""
    hoja = (f'<div class="vt-nb-hoja"><p class="vt-nb-hoja__cab"><span>Nota de pedido</span><span>Viveros Terra</span></p>'
            f'<div class="vt-nb-lineas">{_linea()}</div>'
            '<button type="button" class="vt-btn vt-btn--linea vt-nb-agregar" data-nb-accion="agregar">'
            '<span aria-hidden="true">+</span>Agregar otro tamaño o color</button>'
            f'{_aviso("tope", "")}'
            f"{_extras()}</div>")
    cuerpo = f'<div class="vt-nb-nota" data-nb-cotizador{atributo_modo}>{hoja}{_ticket(k, modo)}</div>'
    return c.bloque(next(n), "Cotizador", "vt-h-cotizador", x["titulo"], cuerpo, lede=x["lede"], tinte=True, id_seccion="cotizador")


def _encabezado_escalon(i):
    cortes, nombre = NB["cortes"], NB["nombres_escalon"][i]
    if i == len(cortes) - 1:
        rango = f"{cortes[i]}+"
    else:
        rango = f"{cortes[i]}–{cortes[i + 1] - 1}" + (" pzas" if i == 0 else "")
    return f'<th scope="col">{rango}<small>{nombre}</small></th>'


def _fila_precio(p):
    aviso = "<small>Sobre pedido</small>" if p.get("sobre_pedido") else ""
    celdas = "".join(f"<td>{c.dinero(x)}</td>" for x in p["precios"])
    return f'<tr><th scope="row">{esc(p["nombre"])}{aviso}</th>{celdas}</tr>'


def _tabla(k, modo, n):
    x, referencia = k["tabla"], modo == "preventa"
    titulo, caption = (x["titulo_referencia"], x["caption_referencia"]) if referencia else (x["titulo"], x["caption"])
    columnas = "".join(_encabezado_escalon(i) for i in range(len(NB["cortes"])))
    filas = "".join(_fila_precio(p) for p in NB["productos"])
    tabla = (f'<table class="vt-tabla vt-nb-tabla"><caption>{caption}</caption><thead><tr>'
             f'<th scope="col">Tamaño</th>{columnas}</tr></thead><tbody>{filas}</tbody></table>')
    return c.bloque(next(n), "Precios", "vt-h-precios", titulo, tabla + f'<p class="vt-nb-nota-tabla">{x["nota"]}</p>', id_seccion="precios")


def _item_para(x, i, k):
    p = k["para"]
    limite = NB["fecha_limite_mayoreo"]
    enlace = (f'<a class="vt-nb-para__wa" data-cta="{TIPO}:para-{x["id"]}" href="{_wa(x["mensaje"])}" target="_blank" rel="noopener">'
              f'{WA_GLIFO}Cotizar para {x["corto"]}<span class="vt-flecha" aria-hidden="true">→</span></a>')
    return (f'<li class="vt-nb-para__item"><span class="vt-nb-para__n" aria-hidden="true">{i:02d}</span>'
            f'<div class="vt-nb-para__texto"><h3>{x["titulo"]}</h3><p>{x["detalle"]}</p></div>'
            f'<ul class="vt-nb-para__cond"><li>{p["minimo"]}</li><li data-nb-hasta="{limite}">{p["pide_antes"]}</li></ul>{enlace}</li>')


def _para(k, n):
    x = k["para"]
    filas = "".join(_item_para(item, i, k) for i, item in enumerate(x["items"], 1))
    return c.bloque(next(n), "¿Para quién?", "vt-h-para", x["titulo"], f'<ol class="vt-nb-para">{filas}</ol>')


def _galeria(k, modo, n):
    fotos = [f for f in FOTOS if f["uso"] != "hero"]
    figuras = "".join(f'<div class="vt-nb-galeria__f vt-nb-galeria__f--{f["id"]}">{c.figura(_foto(f, i, SIZES_GALERIA[f["id"]]))}</div>'
                      for i, f in enumerate(fotos, 2))
    x = k["galeria"]
    return c.bloque(next(n), "Fotos", "vt-h-galeria", x["titulo"], f'<div class="vt-nb-galeria">{figuras}</div>',
                    lede=None if modo == SIN_MODO_COTIZADOR else x["lede"], tinte=True)


def _confianza(k, n):
    x = k["confianza"]
    sellos = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in x["sellos"])
    cuerpo = f'<ul class="vt-nb-sellos">{sellos}</ul><h3 class="vt-mt">{x["clientes"]}</h3>{c.logos()}'
    return c.bloque(next(n), "Confianza", "vt-h-confianza", x["titulo"], cuerpo)


def _como(k, n):
    x = k["como"]
    fechas = "".join(f'<li data-nb-hasta="{f}">{t}</li>' for f, t in x["fechas"])
    return c.bloque(next(n), "Tu pedido", "vt-h-como", x["titulo"], c.pasos(x["pasos"]) + f'<ul class="vt-nb-fechas">{fechas}</ul>', tinte=True)


def _cuidados(k, n):
    x = k["cuidados"]
    return c.bloque(next(n), "Cuidados", "vt-h-cuidados", x["titulo"], c.fichas(x["items"]), lede=x["lede"])


def _preguntas_de(k, modo):
    return k["faq"]["por_modo"].get(modo, k["faq"]["preguntas"])


def _faq(k, modo, n):
    filas = "".join(f"<div><h3>{q}</h3><p>{a}</p></div>" for q, a in _preguntas_de(k, modo))
    return c.bloque_dos(next(n), "Preguntas", "vt-h-faq", k["faq"]["titulo"], "", f'<div class="vt-nb-faq">{filas}</div>', tinte=True)


def _datos_planta(k, n):
    x = k["datos_planta"]
    filas = "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in x["items"])
    return c.bloque(next(n), "Dato", "vt-h-datos", x["titulo"], f'<dl class="vt-nb-datos">{filas}</dl>')


def _cierre(k, modo):
    x, cerrada = k["cierre"], modo == SIN_MODO_COTIZADOR
    titulo, lede = (x["titulo_postemporada"], x["lede_postemporada"]) if cerrada else (x["titulo"], x["lede"])
    if cerrada:
        acciones = f'<div class="vt-cta">{_boton_wa(k["mensajes"][modo], f"{TIPO}:cierre", k["aviso"], "vt-btn vt-btn--wa")}</div>'
    elif modo == "preventa":
        acciones = (f'<div class="vt-cta">{_boton_wa(k["mensajes"][modo], f"{TIPO}:cierre", k["portadas"][modo]["wa"], "vt-btn vt-btn--wa")}'
                    f'{c.boton_tel(f"{TIPO}:cierre")}</div>')
    else:
        acciones = c.fila_cta(k["mensajes"][modo], TIPO, "cierre")
    return (f'<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
            f'<h2 id="vt-cierre-titulo">{titulo}</h2><p class="vt-lede">{lede}</p>{acciones}</div>'
            f'<div class="vt-nb-visita"><p><b>Dirección</b>{esc(datos.DOMICILIO_COMPLETO)}</p>'
            f'<p><a href="{esc(datos.MAPS_URL)}" target="_blank" rel="noopener">Ver en el mapa</a></p>'
            f'<p><b>Horario</b>{esc(datos.HORARIO)}</p><p class="vt-nb-visita__fecha">{x["actualizacion"]}</p></div></div></section>')


def _barra(texto):
    """Sale oculta: vt-nochebuenas.js la muestra cuando el CTA del hero y el ticket ya no se ven."""
    return (f'<div class="vt-bar vt-nb-bar" data-nb-bar role="region" aria-label="Ir al cotizador" hidden>'
            f'<a class="vt-btn vt-btn--wa vt-bar__go" data-cta="{TIPO}:barra" href="#cotizador" data-nb-total-barra>'
            f"{texto}</a></div>")


def _disponibilidad(p, modo):
    if modo == "postemporada":
        return "OutOfStock"
    if modo == "preventa" or p.get("sobre_pedido"):
        return "PreOrder"
    return "InStock"


def _cantidad(i):
    """QuantitativeValue del escalón i, en piezas (C62); el último no tiene tope."""
    cortes = NB["cortes"]
    valor = {"@type": "QuantitativeValue", "minValue": cortes[i], "unitCode": "C62"}
    return valor if i == len(cortes) - 1 else {**valor, "maxValue": cortes[i + 1] - 1}


def _producto(p, modo, url, j):
    negocio = {"@id": j["negocio"]}
    disponibilidad = f"{CONTEXTO}/{_disponibilidad(p, modo)}"
    ofertas = [{"@type": "Offer", "price": precio, "priceCurrency": "MXN", "availability": disponibilidad, "url": url,
                "eligibleQuantity": _cantidad(i)} for i, precio in enumerate(p["precios"])]
    return {"@type": "Product", "@id": f'{url}#nochebuena-{p["clave"]}', "name": f'Nochebuena {p["nombre"]}',
            "description": f'Nochebuena {p["nombre"]} en roja, rosa o jaspeada, en Tampico, Madero y Altamira.',
            "image": j["imagen"], "category": "Plantas de temporada",
            "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": p["precios"][-1], "highPrice": p["precios"][0],
                       "offerCount": len(p["precios"]), "availability": disponibilidad, "url": url,
                       "seller": negocio, "offers": ofertas}}


def _grafo(k, modo):
    meta, j = _meta(k, modo), k["jsonld"]
    url, negocio = meta["canonical"], {"@id": j["negocio"]}
    migas, faq = f"{url}#migas", f"{url}#faq"
    # Nodo mínimo: la ficha completa vive en la home; aquí solo se nombra para que el @id resuelva dentro de este grafo.
    empresa = {"@type": "LocalBusiness", "@id": j["negocio"], "name": datos.NOMBRE, "url": datos.SITIO, "telephone": datos.TELEFONO_TEL}
    pagina = {"@type": "WebPage", "@id": url, "url": url, "name": meta["title"], "inLanguage": "es-MX", "about": negocio,
              "publisher": negocio, "dateModified": NB["ultima_actualizacion"], "breadcrumb": {"@id": migas}, "mainEntity": {"@id": faq},
              "primaryImageOfPage": {"@type": "ImageObject", "url": j["imagen"]}}
    return [empresa, pagina, *(_producto(p, modo, url, j) for p in NB["productos"]),
            {**c.faq_jsonld(_preguntas_de(k, modo)), "@id": faq}, {**j["migas"], "@id": migas}]


def _config(modo):
    """JSON que lee el cotizador: el bloque de datos.py y el número de WhatsApp. "<" escapado: nunca cierra el <script>."""
    texto = json.dumps(dict(NB, modo=modo, wa=datos.TELEFONO_WA), ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/json" id="nb-config">' + texto.replace("<", "\\u003c") + "</script>"


def _secciones(k, modo):
    n = itertools.count(1)
    if modo == SIN_MODO_COTIZADOR:
        return (_portada(k, modo), _galeria(k, modo, n), _cuidados(k, n), _faq(k, modo, n), _cierre(k, modo))
    return (_portada(k, modo), _cotizador(k, modo, n), _tabla(k, modo, n), _para(k, n), _galeria(k, modo, n), _confianza(k, n), _como(k, n),
            _cuidados(k, n), _faq(k, modo, n), _datos_planta(k, n), _cierre(k, modo))


def render(k, modo=None):
    modo = modo or NB["modo"]
    abierta = modo != SIN_MODO_COTIZADOR
    hero = _foto(next(f for f in FOTOS if f["uso"] == "hero"), 1, SIZES_HERO)
    return base.documento(_meta(k, modo), "\n".join(_secciones(k, modo)), jsonld_bloques=({"@context": CONTEXTO, "@graph": _grafo(k, modo)},),
                          precargas=(base.precarga_imagen(hero),), scripts=SCRIPTS if abierta else (),
                          head_extra=(_config(modo),) if abierta else (), tras_main=_barra(k["portadas"][modo]["cta"]) if abierta else "", clase_body=CLASE_BODY)
