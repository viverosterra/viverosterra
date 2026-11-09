"""Plantilla de las páginas de formulario, todas noindex (spec §3.3): /gracias (promesa única, qué sigue y "Adelantar por
WhatsApp"; GA4 la cuenta por su URL y su page_view), /cuestionario (paso 2 del diseño: 5 pasos a formsubmit y de ahí a /gracias) y
/datos-envio (arma el mensaje de WhatsApp en el navegador). La misma cabecera; el cuerpo sale de k["vista"]."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _gracias(k):
    pasos = "".join(f"<li>{x}</li>" for x in k["siguientes"]["items"])
    return (f'<section class="vt-bloque" aria-labelledby="vt-h-sigue"><div class="vt-wrap vt-util__estrecho">'
            f'<h2 id="vt-h-sigue">{k["siguientes"]["titulo"]}</h2><ol class="vt-util__lista">{pasos}</ol>'
            f'<p class="vt-util__adelanto">{k["adelanto"]["texto"]}</p>'
            f'<div class="vt-cta">{cu.boton_wa_texto("Adelantar por WhatsApp", k["adelanto"]["mensaje"], k["tipo"] + ":cuerpo")}</div>'
            f'<p class="vt-promesa">{k["mientras"]}</p><p class="vt-promesa"><a href="/">← Volver al inicio</a></p>'
            f'</div></section>')


def _paso(n, p, total):
    oculto = "" if n == 1 else " hidden"
    controles = cu.dibujar_todos(p["controles"])
    return (f'<div class="vt-paso" id="page-{n}" data-vt-paso="{n}"{oculto}><h2 tabindex="-1">{p["titulo"]}</h2>'
            f'<p class="vt-util__pista">{p["pista"]}</p>{controles}'
            f'</div>')


def _cuestionario(k):
    f = k["form"]
    total = len(f["pasos"])
    ocultos = "".join(f'<input type="hidden" name="{c.esc(n)}" value="{c.esc(v)}">' for n, v in f["ocultos"])
    miel = '<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
    pasos = "".join(_paso(i, p, total) for i, p in enumerate(f["pasos"], 1))
    nav = "".join(f'<li data-vt-marca="{i}"{" aria-current=step" if i == 1 else ""}><b>{i}</b><span>{p["corto"]}</span></li>'
                  for i, p in enumerate(f["pasos"], 1))
    return (
        f'<section class="vt-bloque" aria-label="Formulario del cuestionario"><div class="vt-wrap vt-util__estrecho">'
        f'<noscript><p class="vt-util__pista">{k["sin_js"]["texto"]}</p>'
        f'<div class="vt-cta">{c.boton_wa(k["sin_js"]["mensaje"], "cuestionario:sin-js")}</div></noscript>'
        f'<ol class="vt-wizard" aria-label="Pasos del cuestionario">{nav}</ol>'
        f'<div class="vt-progreso" aria-hidden="true"><span id="prog"></span></div>'
        f'<form id="mainForm" class="vt-util__form" action="{c.esc(f["accion"])}" method="POST" data-cta-form="{c.esc(f["cta"])}">'
        f'{ocultos}{miel}{pasos}'
        f'<div class="vt-util__pie" id="main-footer"><button type="button" class="vt-btn vt-btn--linea" id="btn-prev" hidden>'
        f'← Anterior</button><p class="vt-util__cuenta" id="step-counter" role="status">Paso 1 de {total}</p>'
        f'<button type="button" class="vt-btn vt-btn--tinta" id="btn-next">Siguiente →</button>'
        f'<button type="submit" class="vt-btn vt-btn--tinta" id="submit-btn" hidden>Enviar cuestionario</button></div>'
        f'</form>'
        f'<p class="vt-promesa">Última actualización: <time datetime="{k["fecha_iso"]}">{k["fecha"]}</time></p>'
        f'</div></section>')


def _datos_envio(k):
    tarjetas = "".join(
        f'<section class="vt-util__tarjeta" aria-labelledby="{t["id"]}"><h2 id="{t["id"]}">{t["titulo"]}</h2>'
        f'{cu.dibujar_todos(t["controles"])}</section>' for t in k["tarjetas"])
    return (
        f'<section class="vt-bloque"><div class="vt-wrap vt-util__estrecho"><div id="form">'
        f'<div class="vt-util__orden" id="order" hidden><div><b id="oProd"></b><small id="oFolio"></small></div>'
        f'<div class="vt-util__total" id="oTot"></div></div>{tarjetas}'
        f'<section class="vt-util__tarjeta" aria-label="Factura"><label class="vt-util__casilla"><input type="checkbox" id="quiere">'
        f'Requiero factura</label><div id="fact" hidden>{cu.dibujar_todos(k["factura"])}</div></section>'
        f'<p class="vt-util__error" id="err" role="alert" hidden>Revisa los campos marcados en rojo.</p>'
        f'<button type="button" class="vt-btn vt-btn--wa" id="enviar">Enviar mis datos por WhatsApp</button>'
        f'<p class="vt-promesa">{k["nota"]}</p></div>'
        f'<div class="vt-util__tarjeta" id="done" hidden><h2>¡Listo!</h2><p>Solo falta que toques <b>Enviar</b> en WhatsApp. '
        f'Si no se abrió, <a href="#" id="again">toca aquí</a>.</p></div></div></section>')


VISTAS = {"gracias": _gracias, "cuestionario": _cuestionario, "datos_envio": _datos_envio}


def render(k):
    cuerpo = cu.cabeza(k["cabeza"]) + "\n" + VISTAS[k["vista"]](k)
    foto = k["cabeza"].get("foto")
    precargas = (base.precarga_imagen(foto),) if foto else ()
    return base.documento(k["meta"], cuerpo, jsonld_bloques=k.get("jsonld", ()), precargas=precargas,
                          scripts=k.get("scripts", ()), clase_body=CLASE_BODY)
