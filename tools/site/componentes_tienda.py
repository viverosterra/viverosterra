"""Componentes de la tienda de pasto sintético (Etapa 2b): cotizador por estado, forma de pago, lista de cotización,
barra de compra, tarjetas del catálogo, galería, ficha técnica, rollo a escala, comparativa y tablas de envío.

El marcado conserva los id, clases y data-* que leen public/js/tienda-pasto.js y public/js/tienda-hub.js (esos dos
archivos no se reescriben): #m2, #estado, #modelo, #cta-add, [data-cta-wa], #q-*, [data-plans], #cotizacion,
#cot-send, #toast, #buybar, .spec-card, [data-add], [data-filter], #quiz, #comparador, [data-landed-*]. Todo número
sale de tools/pasto/data.py (modelos, zonas y fletes) o de datos.py; la fórmula de mensualidades es la de
tools/pasto/mensualidades.py. Las clases propias llevan prefijo vt-; las que crea o busca el JS se estilan solo bajo
body.vt-tienda (public/css/terra-tienda.css).
"""
import json

import componentes as c
import datos
import data
import mensualidades
from partials import WA_GLIFO, esc

GAL = "/img/pasto-sintetico/galeria"
MAX_MM = 35
ROLLO_M2 = data.ROLLO_M2
MIN_NACIONAL = data.MIN_NACIONAL_M2
MIN_SHOWROOM = data.MIN_SHOWROOM_M2
TIERS = (("rollo", "Rollo completo", f"{ROLLO_M2} m² o más"), ("t2", "Corte mediano", "10 a 49 m²"),
         ("t1", "Corte chico", "2 a 9 m², solo en showroom"))
NOTA_FLETE = "Te confirmamos el flete exacto a tu dirección antes de pagar."
TARIFAS = tuple(data.ZONAS[z] for z in sorted(data.ZONAS))
TARIFAS_TEXTO = f"{c.dinero(TARIFAS[0])}, {c.dinero(TARIFAS[1])} o {c.dinero(TARIFAS[2])}"


def modelo(slug):
    return data.BY_SLUG[slug]


def barato(modelos=None):
    return min(modelos or data.MODELOS, key=lambda m: m["rollo"])


def garantia_texto(m):
    return f"{str(m['garantia']).replace(' a ', '–')} años" if m["garantia"] else "Consultar"


def img_textura(m):
    return f"{GAL}/{m['slug']}-2-sm.webp"


# ---------- datos para el JS ----------
def datos_modelo_js(m):
    """Lo que tienda-pasto.js necesita de un modelo para cotizarlo y agregarlo a la lista."""
    return {"slug": m["slug"], "nombre": m["nombre"], "img": img_textura(m), "t1": m["t1"], "t2": m["t2"],
            "rollo": m["rollo"]}


def json_modelo(m):
    """<script type="application/json" id="vt-model"> de la ficha (tienda-pasto.js lo lee)."""
    return (f'<script type="application/json" id="vt-model">{json.dumps(datos_modelo_js(m), ensure_ascii=False)}'
            "</script>")


def json_modelos(modelos=None, completo=False):
    """id="vt-models" del hub (con scores, tag y mm para el selector) o de la página de Tampico."""
    filas = []
    for m in modelos or data.MODELOS:
        fila = {"slug": m["slug"]}
        if completo:
            fila["id"] = m["id"]
        fila.update({"nombre": m["nombre"], "img": img_textura(m), "t1": m["t1"], "t2": m["t2"], "rollo": m["rollo"]})
        if completo:
            fila.update({"scores": m["scores"], "tag": m["tag"], "mm": m["mm"]})
        filas.append(fila)
    return f'<script type="application/json" id="vt-models">{json.dumps(filas, ensure_ascii=False)}</script>'


# El mismo script en línea que publicaba tools/pasto/ficha.py: pinta [data-landed-slug] con el precio puesto del estado.
SCRIPT_PRECIO_PUESTO = (
    '<script>document.addEventListener("vt:ready",function(){var t=window.VTTienda,L=window.VTLanded;if(!t||!L)return;'
    'function p(e){document.querySelectorAll("[data-landed-slug]").forEach(function(el){var m=t.models.find(function(x){return x.slug===el.dataset.landedSlug});'
    'var v=m&&e?L.landedM2(m.rollo,e,t.estadoZona,t.zonas):null;el.textContent=v?"$"+v.toLocaleString("es-MX")+"/m² puesto en "+e:"";});}'
    'p(t.getEstado());document.addEventListener("vt:estado",function(ev){p(ev.detail.estado||"")});});</script>')


# ---------- piezas pequeñas ----------
def regla_altura(mm):
    """Altura de fibra contra el máximo de la colección (35 mm)."""
    pct = c.redondear(mm / MAX_MM * 100)
    return (f'<div class="vt-regla" role="img" aria-label="Altura de fibra: {mm} mm"><span class="vt-regla__pista">'
            f'<span class="vt-regla__fill" style="--w:{pct}%"></span></span><span class="vt-regla__val">{mm}'
            f'<small>mm</small></span></div>')


def chip_mm(mm):
    return f'<span class="vt-chip-mm" aria-hidden="true">{mm}<small>mm</small></span>'


def existencia(m):
    """Línea de existencia: los 9 en existencia nacional; para llevar hoy solo Toscana 18 y 28 (stock en data.py)."""
    hoy = (f'<span>{esc(m["nombre"])} para llevar hoy en el showroom de {datos.CALLE_CORTA}</span>'
           if m["stock"] else "")
    return f'<p class="vt-existencia"><span>En existencia · envío a todo México en 3 a 5 días hábiles</span>{hoy}</p>'


def subnav():
    """Barra de la tienda bajo el menú: atajos y "Mi lista (n)"; el (0) no se ve con la lista vacía."""
    return ('<nav class="vt-subnav" aria-label="Tienda de pasto sintético"><div class="vt-wrap vt-subnav__bar">'
            '<a href="/pasto-sintetico#modelos">Los 9 modelos</a><a href="/pasto-sintetico#elegir">¿Cuál me conviene?</a>'
            '<a href="/pasto-sintetico#como-funciona">Cómo comprar</a>'
            '<button class="vt-subnav__lista" type="button" data-open-cot aria-haspopup="dialog">Mi lista '
            '<span class="vt-subnav__n" data-cot-count data-empty="true">0</span></button></div></nav>')


def selector_estado(id_select, etiqueta="Envíalo a"):
    """Select de estados (orden de data.ESTADOS_ORDEN); tienda-hub.js lo sincroniza con el cotizador."""
    opciones = "".join(f'<option value="{esc(e)}">{esc(e)}</option>' for e in data.ESTADOS_ORDEN)
    return (f'<div class="vt-campo"><label for="{esc(id_select)}">{esc(etiqueta)}</label><div class="vt-control">'
            f'<select id="{esc(id_select)}" data-estado-select><option value="">Elige tu estado</option>{opciones}'
            '</select></div></div>')


# ---------- cotizador (marcado de tienda-pasto.js) ----------
def tabla_tiers(m):
    filas = "".join(f'<tr data-tier="{k}"><th scope="row">{t}<span>{d}</span></th><td id="tier-{k}">'
                    f'{c.dinero(m[k])}/m²</td></tr>' for k, t, d in TIERS)
    return f'<table class="vt-tiers"><caption>Precio por volumen</caption><tbody>{filas}</tbody></table>'


def planes_cotizador(prefijo):
    """Forma de pago: contado o 3, 6, 9 y 12 mensualidades con tarjeta de crédito. tienda-pasto.js llena montos y
    disponibilidad con VTMensualidades (fórmula oficial)."""
    opciones = [("0", "Contado", "Transferencia, efectivo o tarjeta en una exhibición")] + [
        (str(n), f"{n} mensualidades", "Con tarjeta de crédito") for n in mensualidades.PLAZOS]
    filas = "".join(
        f'<label class="plan" data-plan="{v}"><input type="radio" name="{prefijo}-plan" value="{v}"'
        f'{" checked" if v == "0" else ""}><span class="vt-plan__n">{esc(n)}<small>{esc(s)}</small></span>'
        f'<span class="vt-plan__monto" data-plan-amount></span><span class="vt-plan__total" data-plan-total></span></label>'
        for v, n, s in opciones)
    return (f'<fieldset class="vt-planes-t" id="{prefijo}-plans" data-plans><legend id="{prefijo}-plans-legend">'
            '¿Cómo prefieres pagar?</legend>'
            f'<dl class="vt-planes-t__trip" id="{prefijo}-plan-trip" aria-live="polite"><div><dt>Contado</dt>'
            '<dd data-trip-contado>—</dd></div><div><dt>Al mes</dt><dd data-trip-mes>—</dd></div><div><dt>Total</dt>'
            f'<dd data-trip-total>—</dd></div></dl><div class="pay-rule" id="{prefijo}-plan-rule" aria-hidden="true"></div>'
            f'<div class="vt-planes-t__lista">{filas}</div>'
            '<p class="vt-planes-t__ahorro" data-plan-save></p>'
            '<p class="vt-planes-t__nota">Precio en mensualidades con tarjeta de crédito. Contado (transferencia, '
            'efectivo o tarjeta en una exhibición) es el precio más bajo. Montos aproximados: tu banco debe aceptar el '
            'plan. Te confirmamos el total antes de enviarte el link de pago. <a href="/politicas#mensualidades">'
            'Condiciones</a></p></fieldset>')


def _selector_modelo(modelos, elegido):
    opciones = "".join(f'<option value="{m["slug"]}"{" selected" if m is elegido else ""}>{esc(m["nombre"])} · '
                       f'desde ${m["rollo"]}/m²</option>' for m in modelos)
    return (f'<div class="vt-campo vt-campo--ancho"><label for="modelo">Modelo</label><div class="vt-control">'
            f'<select id="modelo">{opciones}</select></div></div>')


def _entrega(showroom, local):
    """Select #estado. local=True (Tampico): solo showroom o envío local según la colonia, sin los 32 estados ni flete
    nacional (data-local: tienda-pasto.js no agrega los estados)."""
    if local:
        return ('<div class="vt-campo"><label for="estado">Entrega</label><div class="vt-control"><select id="estado" '
                'data-local><option value="showroom" selected>Recoger en showroom, Cd. Madero</option><option value="local">'
                'Envío local en Tampico, Madero o Altamira</option></select></div></div>')
    sel_showroom = " selected" if showroom else ""
    return ('<div class="vt-campo"><label for="estado">Entrega</label><div class="vt-control"><select id="estado">'
            f'<option value="">Selecciona tu estado</option><option value="showroom"{sel_showroom}>Recoger en showroom, '
            'Cd. Madero</option></select></div></div>')


def cotizador(m, *, modelos=None, m2=ROLLO_M2, showroom=False, local=False, titulo="Cotiza tu corte",
              id_titulo="vt-h-cotizar", nivel=2, mensaje=None, tipo="tienda"):
    """Cotizador de tienda-pasto.js. m: modelo inicial; con `modelos`, agrega el selector #modelo (hub y Tampico).
    showroom=True preselecciona "Recoger en showroom". local=True (venta local en Tampico): showroom o envío local
    según la colonia, sin flete por estado, y el "desde" es el material más barato. Envío nacional bajo 25 m²: el JS
    bloquea total y mensualidades (J03 §3). El botón de WhatsApp lleva desde el HTML un mensaje con firma (sin JS no
    queda vacío)."""
    pm2 = m["rollo"] if m2 >= ROLLO_M2 else (m["t2"] if m2 >= 10 else m["t1"])
    material = pm2 * m2
    texto = mensaje or (f"Hola, quiero cotizar el pasto sintético {m['nombre']}.\nNecesito ___ m².\n"
                        + ("Mi colonia: ___" if local else "Mi estado: ___"))
    href = esc(datos.wa_url(datos.con_firma(texto)))
    chips = "".join(f'<button class="vt-chip" type="button" data-m2="{n}" aria-pressed="{"true" if n == m2 else "false"}">'
                    f'{n} m²</button>' for n in (MIN_NACIONAL, ROLLO_M2, ROLLO_M2 * 2))
    selector = _selector_modelo(modelos, m) if modelos else ""
    if local:
        desde = (f'<p class="vt-cotizador__desde">Material desde <b>{c.dinero(barato(modelos)["rollo"])}</b>/m² en rollo, '
                 'IVA incluido · envío local según tu colonia</p>')
        envio = ('<p class="vt-cuenta__fila"><span id="q-envio-label">Recoger en showroom</span><b id="q-envio">Sin costo'
                 '</b></p>')
        nota = "Te cotizamos el envío local según tu colonia antes de pagar."
    else:
        desde = (f'<p class="vt-cotizador__desde">Desde <b id="buy-price">{c.dinero(m["rollo"])}</b>/m² · rollo de '
                 f'{ROLLO_M2} m², IVA incluido · envío por rollo según tu estado</p>')
        envio = '<p class="vt-cuenta__fila"><span id="q-envio-label">Envío</span><b id="q-envio">Elige tu estado</b></p>'
        nota = NOTA_FLETE
    return (
        f'<section class="vt-cotizador" id="comprar" aria-labelledby="{id_titulo}" data-min-nacional="{MIN_NACIONAL}" '
        f'data-min-showroom="{MIN_SHOWROOM}"><h{nivel} class="vt-cotizador__t" id="{id_titulo}">{esc(titulo)}</h{nivel}>'
        f'{desde}{selector}<div class="vt-campo"><label for="m2">Metros cuadrados</label><div class="vt-stepper">'
        '<button type="button" id="m2-minus" aria-label="Restar 5 m²">−</button><input id="m2" type="number" '
        f'inputmode="numeric" min="{MIN_SHOWROOM}" max="5000" step="1" value="{m2}">'
        '<button type="button" id="m2-plus" aria-label="Sumar 5 m²">+</button></div>'
        f'<div class="vt-chips" role="group" aria-label="Medidas rápidas">{chips}</div></div>'
        f'{_entrega(showroom, local)}{tabla_tiers(m)}'
        '<div class="vt-cuenta" aria-live="polite">'
        f'<p class="vt-cuenta__fila"><span>Precio aplicado</span><b id="q-pm2">{c.dinero(pm2)}/m²</b></p>'
        f'<p class="vt-cuenta__fila"><span>Material</span><b id="q-material">{c.dinero(material)}</b></p>'
        f'{envio}<p class="vt-cuenta__total"><span id="q-total-label">Total estimado</span><b id="q-total">'
        f'{c.dinero(material)}</b></p><p class="vt-cuenta__puesto" id="q-landed"></p>'
        '<p class="vt-cuenta__pista" id="q-hint"></p><p class="vt-cuenta__error" id="q-error"></p></div>'
        f'{planes_cotizador("q")}'
        f'<div class="vt-cotizador__acciones"><a class="vt-btn vt-btn--wa" data-cta-wa data-cta="{tipo}:cotizador" '
        f'href="{href}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<button class="vt-btn vt-btn--linea" type="button" id="cta-add">Agregar a mi lista</button>'
        f'<p class="vt-promesa">{nota} {esc(datos.PROMESA_COMPLETA)}.</p></div></section>')


# ---------- lista de cotización, aviso y barra de compra ----------
def lista_y_aviso():
    """<dialog id="cotizacion"> (tienda-pasto.js arma los renglones y el mensaje con todos los modelos de la lista) y
    el aviso "<modelo> en tu lista · Ver"."""
    return (
        '<dialog class="vt-lista" id="cotizacion" aria-labelledby="cot-titulo"><div class="vt-lista__in">'
        '<div class="vt-lista__cabeza"><h2 id="cot-titulo">Mi lista</h2><button class="vt-lista__cerrar" type="button" '
        'id="cot-close" aria-label="Cerrar">×</button></div><div class="vt-lista__cuerpo" id="cot-list"></div>'
        '<div class="vt-lista__pie" id="cot-foot" hidden><div class="vt-campo"><label for="cot-estado">Entrega</label>'
        '<div class="vt-control"><select id="cot-estado"><option value="">Selecciona tu estado</option>'
        '<option value="showroom">Recoger en showroom, Cd. Madero</option></select></div></div>'
        '<p class="vt-cuenta__total"><span id="cot-total-label">Total estimado del material</span><b id="cot-total">$0</b>'
        f'</p><a class="vt-btn vt-btn--wa" id="cot-send" data-cta="tienda:lista" href="https://wa.me/{datos.TELEFONO_WA}" '
        f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<p class="vt-promesa">Precio estimado. Confirmamos el flete exacto con tu dirección.</p></div></div></dialog>'
        '<div class="vt-aviso" id="toast" role="status" data-visible="false"><span data-toast-text></span>'
        '<button type="button" data-open-cot>Ver</button></div>')


def barra_compra(nombre, precio, mensaje, *, rollo=None):
    """#buybar fija en celular mientras el cotizador (#comprar) queda arriba. Con rollo, tienda-pasto.js cambia el
    precio al puesto en el estado elegido."""
    puesto = f' data-landed-bar data-rollo="{rollo}"' if rollo else ""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<div class="vt-compra" id="buybar" data-visible="false"{puesto}><div class="buybar__info">'
            f'<div class="buybar__name">{esc(nombre)}</div><div class="buybar__price">{esc(precio)}</div></div>'
            f'<a class="vt-btn vt-btn--wa" data-cta-wa data-cta="tienda:barra" href="{href}" target="_blank" '
            f'rel="noopener">{WA_GLIFO}Cotizar</a></div>')


# ---------- catálogo del hub ----------
def grafica_alturas(modelos=None):
    """Plan visual V3 (2026-11-11): los modelos uno junto al otro por altura de fibra (la regla de la tarjeta, en
    grande), con su peso. Texto real en el HTML: nombre con enlace a su ficha, milímetros y g/m²."""
    filas = "".join(
        f'<li><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a>'
        f'<span class="vt-alturas__barra" style="--w:{c.redondear(m["mm"] / MAX_MM * 100)}%"></span>'
        f'<span class="vt-alturas__v"><b>{m["mm"]}</b> mm · {m["peso"]} g/m²</span></li>'
        for m in sorted(modelos or data.MODELOS, key=lambda x: (x["mm"], x["peso_num"])))
    return (f'<figure class="vt-alturas"><figcaption>Altura de fibra y peso de los {len(modelos or data.MODELOS)} '
            f'modelos</figcaption><ol>{filas}</ol></figure>')


def tarjeta(m):
    """Tarjeta del catálogo: foto con la altura, "para llevar hoy" (chip verde: el amarillo es solo para precios),
    regla de altura, precio puesto y Agregar. En celular es horizontal (terra-tienda.css)."""
    url = f"/pasto-sintetico/{m['slug']}"
    # Plan visual V1: el nombre ya va en el h3 de arriba; la insignia no lo repite.
    hoy = (f'<p class="vt-tarjeta-p__hoy">Listo para llevar hoy · {datos.CALLE_CORTA}</p>'
           if m["stock"] else "")
    return (
        f'<article class="spec-card vt-tarjeta-p" data-usos="{" ".join(m["usos"])}" id="m-{m["slug"]}">'
        f'<a class="vt-tarjeta-p__foto" href="{url}" tabindex="-1" aria-hidden="true"><img src="{img_textura(m)}" '
        f'width="420" height="560" alt="" loading="lazy" decoding="async">{chip_mm(m["mm"])}</a>'
        f'<div class="vt-tarjeta-p__cuerpo"><p class="vt-tarjeta-p__tag">N.º {m["n"]:02d} · {esc(m["tag"])}</p>'
        f'<h3 class="spec-card__name"><a href="{url}">{esc(m["nombre"])}</a></h3>{hoy}{regla_altura(m["mm"])}'
        f'<dl class="vt-tarjeta-p__datos"><div><dt>Peso</dt><dd>{m["peso"]} g/m²</dd></div><div><dt>Garantía</dt>'
        f'<dd>{garantia_texto(m)}</dd></div></dl>'
        f'<p class="vt-tarjeta-p__precio">Desde <b>${m["rollo"]}</b>/m² <span class="vt-tarjeta-p__puesto" '
        f'data-landed-slug="{m["slug"]}"></span></p>'
        '<p class="vt-tarjeta-p__pago">Paga en mensualidades con tarjeta de crédito</p>'
        f'<button class="spec-card__add vt-btn vt-btn--linea" type="button" data-add="{m["slug"]}" '
        f'aria-label="Agregar a mi lista: {esc(m["nombre"])}">Agregar<span class="vt-tarjeta-p__mas"> a mi lista</span>'
        '</button></div></article>')


def filtros(opciones=data.USO_FILTERS):
    chips = "".join(f'<button class="vt-chip" type="button" data-filter="{k}" '
                    f'aria-pressed="{"true" if k == "todos" else "false"}">{esc(t)}</button>' for k, t in opciones)
    return (f'<div class="vt-filtros" role="group" aria-label="Filtrar por uso">{chips}</div>'
            f'<p class="vt-filtros__n" id="filters-count" aria-live="polite">{len(data.MODELOS)} modelos</p>')


def catalogo(modelos=None):
    return f'{filtros()}<div class="vt-catalogo">{"".join(tarjeta(m) for m in modelos or data.MODELOS)}</div>'


QUIZ = (
    ("donde", "¿Dónde va?", (("jardin", "Jardín"), ("terraza", "Terraza o balcón"), ("patio", "Patio o alberca"))),
    ("uso", "¿Quién lo pisa?", (("familia", "La familia, a diario"), ("perros", "Perros"),
                                ("poco", "Casi nadie, es decorativo"), ("intenso", "Mucha gente, uso intenso"))),
    ("prioridad", "¿Qué te importa más?", (("equilibrio", "Equilibrio"), ("precio", "El mejor precio"),
                                           ("realismo", "Que se vea lo más natural"))),
)


def selector_modelo():
    """#quiz de tienda-hub.js: tres preguntas y dos recomendaciones."""
    grupos = "".join(
        f'<fieldset class="vt-opciones"><legend>{esc(leyenda)}</legend>'
        + "".join(f'<label><span>{esc(t)}</span><input type="radio" name="{nombre}" value="{v}"'
                  f'{" checked" if i == 0 else ""}></label>' for i, (v, t) in enumerate(ops))
        + "</fieldset>" for nombre, leyenda, ops in QUIZ)
    return (f'<form class="vt-quiz" id="quiz" aria-describedby="quiz-help"><p class="vt-lede" id="quiz-help">Tres '
            'preguntas y te recomendamos dos modelos. Cambia las respuestas y la recomendación se actualiza.</p>'
            f'{grupos}<div class="vt-quiz__res" id="quiz-result" aria-live="polite"></div></form>')


def comparador():
    """#comparador de tienda-hub.js: precio por m² de otra oferta contra el puesto en tu estado."""
    return ('<form class="vt-comparador" id="comparador" novalidate><div class="vt-campo"><label for="cmp-total">Total '
            'de la otra oferta, con envío</label><div class="vt-control"><input id="cmp-total" type="number" '
            'inputmode="decimal" min="1" placeholder="Ej. 14899"><span>MXN</span></div></div><div class="vt-campo">'
            '<label for="cmp-m2">Metros cuadrados que incluye</label><div class="vt-control"><input id="cmp-m2" '
            'type="number" inputmode="numeric" min="1" placeholder="Ej. 50"><span>m²</span></div></div>'
            '<p class="vt-comparador__res" id="cmp-out" aria-live="polite">Escribe el total y los metros para comparar '
            'con nuestro precio puesto en tu estado.</p></form>')


def tabla_modelos(modelos=None):
    filas = tuple((f'<a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a><br><small>{esc(m["tag"])}</small>',
                   f'{m["mm"]} mm', m["peso"], garantia_texto(m), f'<b>${m["rollo"]}</b>', esc(m["ideal"]))
                  for m in modelos or data.MODELOS)
    tabla = c.tabla_comparativa(("Modelo", "Altura", "Peso g/m²", "Garantía", "Rollo /m²", "Ideal para"), filas,
                                "Los 9 modelos por altura, peso, garantía y precio por rollo.")
    # En celular es tabla con desplazamiento horizontal (no 9 tarjetas): el catálogo de arriba ya trae cada modelo.
    tabla = tabla.replace('class="vt-tabla vt-tabla--comparar"', 'class="vt-tabla vt-tabla--fija"', 1)
    return (f'<div class="vt-tabla-scroll" role="region" aria-label="Comparativa de los {len(modelos or data.MODELOS)} '
            f'modelos (desliza para ver más columnas)" tabindex="0">{tabla}</div>')


def tabla_envio():
    """Flete por zona: 1 y 2 rollos (data.ZONA_ESTADOS y data.ZONAS)."""
    filas = tuple((f"Zona {z}<br><small>{esc(nombre)}</small>", esc(", ".join(estados)),
                   f"<b>{c.dinero(data.ZONAS[z])}</b>", c.dinero(data.ZONAS[z] * 2))
                  for z, (nombre, estados) in data.ZONA_ESTADOS.items())
    return c.tabla_comparativa(("Zona", "Estados", "1 rollo", "2 rollos"), filas,
                               "Costo de envío de pasto sintético por estado, con IVA.")


def zonas_acordeon():
    """Plan visual V2 (2026-11-11): el flete por zona como acordeón (antes, tabla con los estados en párrafos largos).
    Cada zona muestra en el renglón su costo por 1 y 2 rollos; los estados van dentro. tienda-hub.js abre la zona del
    estado elegido (data-zona)."""
    zonas = "".join(f'<details data-zona="{z}"><summary>Zona {z} <small>{esc(nombre)}</small>'
                    f'<span><b>{c.dinero(data.ZONAS[z])}</b> 1 rollo · {c.dinero(data.ZONAS[z] * 2)} 2 rollos</span></summary>'
                    f'<p>{esc(", ".join(estados))}.</p></details>'
                    for z, (nombre, estados) in data.ZONA_ESTADOS.items())
    return (f'<div class="vt-zonas-acc" role="group" aria-label="Costo de envío de pasto sintético por estado, con IVA">'
            f'{zonas}</div>')


def zonas_envio():
    """Las tres tarifas por rollo, cada una con sus estados principales (bloque de envío de la ficha)."""
    celdas = "".join(f'<div><dt>{c.dinero(data.ZONAS[z])}<small> /rollo</small></dt><dd><b>{esc(nombre)}.</b> '
                     f'{esc(", ".join(estados[:6]))} y más.</dd></div>' for z, (nombre, estados) in data.ZONA_ESTADOS.items())
    return f'<dl class="vt-zonas-envio">{celdas}</dl>'


# ---------- ficha ----------
ALT = {
    "rollo": "Rollo de pasto sintético {n} desenrollado, con la base arriba y la fibra {color}",
    "textura": "Acercamiento a la fibra del pasto sintético {n} de {mm} mm en {color}",
    "base": "Base del pasto sintético {n} junto a la fibra, vista a ras de suelo",
    "instalado": "Pasto sintético {n} instalado: {caption}",
}


def foto_principal(m):
    """La primera foto de la galería: se precarga y nunca es lazy (J03)."""
    base = f"{GAL}/{m['slug']}-{m['gallery'][0][0]}"
    return {"src": f"{base}-sm.webp", "srcset": f"{base}-sm.webp 420w, {base}.webp 720w",
            "sizes": "(min-width: 1024px) 620px, 100vw"}


def galeria(m):
    """Galería con scroll y miniaturas (#gal-track, .gallery__slide, [data-gal-idx], #gal-count de tienda-pasto.js);
    cada foto con pie FIG."""
    total = len(m["gallery"])
    diapos, minis = [], []
    for i, (idx, tipo, pie) in enumerate(m["gallery"]):
        base = f"{GAL}/{m['slug']}-{idx}"
        alt = ALT[tipo].format(n=m["nombre"], color=m["color"].lower(), mm=m["mm"], caption=pie.lower())
        # La segunda foto asoma junto a la principal en la primera pantalla del celular (la galería subió con el hero de
        # marca): no va lazy, pero tampoco con prioridad.
        carga = ('loading="eager" fetchpriority="high"', 'loading="eager"')[i] if i < 2 else 'loading="lazy"'
        # Las diapositivas 2+ están en la pista horizontal y Chrome las baja de inmediato aunque sean lazy: en celular
        # piden la copia de 420 px (no la de 720), así no le quitan ancho de banda a la foto principal ni al texto.
        tamanos = "(min-width: 1024px) 620px, 100vw" if i == 0 else "(min-width: 1024px) 620px, 240px"
        diapos.append(f'<figure class="gallery__slide vt-fig"><div class="vt-fig__marco"><img src="{base}-sm.webp" '
                      f'srcset="{base}-sm.webp 420w, {base}.webp 720w" sizes="{tamanos}" '
                      f'width="720" height="960" alt="{esc(alt)}" {carga} decoding="async">'
                      f'{chip_mm(m["mm"]) if i == 0 else ""}</div><figcaption><span><b>Fig. {i + 1:02d}</b> · '
                      f'{esc(pie)}</span><span>Foto de producto</span></figcaption></figure>')
        minis.append(f'<button class="vt-galeria__mini" type="button" data-gal-idx="{i}" aria-label="Ver foto '
                     f'{i + 1}: {esc(pie.lower())}"><img src="{base}-mini.webp" alt="" width="64" height="64" '
                     'loading="lazy"></button>')
    return (f'<section class="vt-galeria" aria-label="Fotos del {esc(m["nombre"])}"><div class="vt-galeria__pista" '
            f'id="gal-track" tabindex="0">{"".join(diapos)}</div><div class="vt-galeria__meta"><span '
            f'class="vt-galeria__n" id="gal-count" aria-live="polite">01 / {total:02d}</span><div '
            f'class="vt-galeria__minis">{"".join(minis)}</div></div></section>')


def datos_modelo(m):
    """Cuadro de datos con las cuatro cifras de la ficha (specstrip de data.py)."""
    return c.cuadro_datos(tuple((t, v, u) for t, v, u in m["specstrip"]))


GLOSARIO = (
    ("Dtex", "Grosor del hilo. A más Dtex, fibra más gruesa y resistente al pisoteo."),
    ("Puntadas por m²", "Cuántos mechones hay en cada metro. A más puntadas, menos se ve la base."),
    ("Fibra de soporte", "El rizo café de abajo. Mantiene de pie la fibra verde y da el look natural."),
    ("Base", "Malla y látex que sujetan cada mechón. Una base más pesada alarga la vida del pasto."),
)
NOTA_FICHA = ("Datos de la ficha técnica del fabricante. Entre paréntesis va la norma con la que se mide cada dato. "
              "Las tolerancias son las de fábrica.")


def ficha_tecnica(m):
    grupos = "".join(
        f'<div class="vt-tecnica__g"><h3>{esc(titulo)}</h3><dl>'
        + "".join(f'<div><dt>{esc(e)}{f"<small>{esc(n)}</small>" if n else ""}</dt><dd>{esc(v)}</dd></div>'
                  for e, n, v in filas) + "</dl></div>" for titulo, filas in m["specs"])
    nota = m.get("specs_note") or NOTA_FICHA
    glosario = "" if m.get("specs_note") else (
        '<dl class="vt-glosario">' + "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(d)}</dd></div>" for t, d in GLOSARIO) + "</dl>")
    return f'<div class="vt-tecnica">{grupos}</div><p class="vt-promesa">{esc(nota)}</p>{glosario}'


def rollo_escala():
    """Un rollo dibujado a escala: 25 m × 2 m = 50 m² (cotas solo donde hay medida real)."""
    return ('<figure class="vt-fig vt-rollo"><svg viewBox="0 0 480 120" role="img" aria-label="Un rollo de pasto '
            'sintético a escala: 25 metros de largo por 2 de ancho, 50 metros cuadrados">'
            '<rect class="vt-plano-relleno" x="40" y="52" width="400" height="32"/>'
            '<rect class="vt-plano-borde" x="40" y="52" width="400" height="32"/>'
            '<path class="vt-cota" d="M40 26 v14 M440 26 v14 M40 33 H440"/>'
            '<text class="vt-cota-t" x="240" y="22" text-anchor="middle">25 m</text>'
            '<path class="vt-cota" d="M452 52 h14 M452 84 h14 M459 52 V84"/>'
            '<text class="vt-cota-t" x="472" y="104" text-anchor="end">2 m</text>'
            '<text class="vt-cota-a" x="240" y="74" text-anchor="middle">50 m²</text></svg>'
            '<figcaption><span><b>Así llega</b> · rollo de 2 m de ancho</span><span>Cotas en metros</span>'
            '</figcaption></figure>')


def vecinos(m):
    """Dos modelos vecinos por altura (los mismos que publicaba tools/pasto/ficha.py)."""
    i = data.MODELOS.index(m)
    if i == 0:
        return [data.MODELOS[1], data.MODELOS[2]]
    if i == len(data.MODELOS) - 1:
        return [data.MODELOS[i - 2], data.MODELOS[i - 1]]
    return [data.MODELOS[i - 1], data.MODELOS[i + 1]]


def comparativa(m):
    """El modelo y sus dos vecinos, cada uno con su etiqueta S y su botón Agregar (data-add: van en el mismo mensaje)."""
    tarjetas = []
    for x in sorted([m] + vecinos(m), key=lambda z: z["n"]):
        actual = x is m
        actual_attr = ' aria-current="page"' if actual else ""
        nombre = f'<a href="/pasto-sintetico/{x["slug"]}"{actual_attr}>{esc(x["nombre"])}</a>'
        tarjetas.append(
            f'<article class="vt-vecino{" vt-vecino--actual" if actual else ""}"><div class="vt-vecino__foto"><img '
            f'src="{img_textura(x)}" width="420" height="560" alt="Textura del pasto sintético {esc(x["nombre"])}" '
            f'loading="lazy" decoding="async">{chip_mm(x["mm"])}</div>'
            f'<p class="vt-vecino__tag">{"Estás viendo" if actual else esc(x["tag"])}</p><h3>{nombre}</h3>'
            f'<dl><div><dt>Altura</dt><dd>{x["mm"]} mm</dd></div><div><dt>Peso</dt><dd>{x["peso"]} g/m²</dd></div>'
            f'<div><dt>Garantía</dt><dd>{garantia_texto(x)}</dd></div></dl>'
            f'<p class="vt-vecino__precio">Desde <b>${x["rollo"]}</b>/m²</p><button class="vt-btn vt-btn--linea" '
            f'type="button" data-agregar="{esc(json.dumps(datos_modelo_js(x), ensure_ascii=False))}">Agregar 1 rollo a '
            'mi lista</button></article>')
    return (f'<div class="vt-vecinos">{"".join(tarjetas)}</div>'
            '<p class="vt-promesa"><a href="/pasto-sintetico#modelos">Ver los 9 modelos</a></p>')


# ---------- ciudades ----------
def foto_obra(nombre, sizes, etapa, numero=1):
    """Figura de portada con una foto real de obra (data.OBRAS: medidas, alt y pie); se precarga como foto principal."""
    _n, ancho, alto, alt, lugar = next(o for o in data.OBRAS if o[0] == nombre)
    return {"src": f"{GAL}/{nombre}-sm.webp", "srcset": f"{GAL}/{nombre}-sm.webp 560w, {GAL}/{nombre}.webp {ancho}w",
            "sizes": sizes, "ancho": ancho, "alto": alto, "numero": numero, "alt": alt, "lugar": lugar, "etapa": etapa}



def totales(m, zona):
    """Material + flete para 25, 50 y 100 m² (reglas del cotizador: 25 m² usa el precio de corte mediano)."""
    salida = []
    for m2 in (MIN_NACIONAL, ROLLO_M2, ROLLO_M2 * 2):
        precio = m["rollo"] if m2 >= ROLLO_M2 else m["t2"]
        rollos = -(-m2 // ROLLO_M2)
        salida.append((m2, m2 * precio + rollos * data.ZONAS[zona]))
    return salida


def mensualidad_maxima(total):
    """El plazo más largo que aplica al total y su mensualidad (fórmula oficial), o "—"."""
    disponibles = [p for p in mensualidades.planes(total) if p["disponible"]]
    if not disponibles:
        return "—"
    p = disponibles[-1]
    return f'{p["plazo"]} × ≈ {c.dinero(p["mensualidad"])}'


def tabla_totales(m, zona):
    filas = tuple((f"{m2} m²", c.dinero(total), f"{c.dinero(total / m2)}/m²", mensualidad_maxima(total))
                  for m2, total in totales(m, zona))
    return c.tabla_comparativa(("Metros", "Total con envío", "Por m²", "En mensualidades"), filas,
                               f"Ejemplo con {esc(m['nombre'])}, el modelo más económico. Material más flete, IVA "
                               "incluido.")


def modelos_recomendados(items, zona=None, lugar="", estado=""):
    """Tres modelos con su regla de altura y la razón; con zona, el precio puesto en la ciudad; sin zona, el precio
    del rollo y el puesto según el estado elegido (data-landed-slug). Con estado (slug), el enlace a la ficha lleva
    ?estado= y la ficha abre con ese estado elegido (tienda-pasto.js)."""
    tarjetas = []
    consulta = f"?estado={estado}" if estado else ""
    for slug, razon in items:
        m = modelo(slug)
        if zona:
            precio = f'Desde <b>${data.landed_m2(m, zona)}</b>/m² puesto en {esc(lugar)}'
        else:
            precio = f'Desde <b>${m["rollo"]}</b>/m² <span data-landed-slug="{m["slug"]}"></span>'
        tarjetas.append(f'<li class="vt-recomendado"><h3><a href="/pasto-sintetico/{m["slug"]}{consulta}">{esc(m["nombre"])}'
                        f'</a></h3>{regla_altura(m["mm"])}<p>{esc(razon)}</p><p class="vt-recomendado__precio">'
                        f'{precio}</p></li>')
    return f'<ul class="vt-recomendados">{"".join(tarjetas)}</ul>'


def ciudades_destacadas(ciudades):
    m = barato()
    filas = "".join(f'<li><a href="/pasto-sintetico/envio/{x["slug"]}"><b>{esc(x["nombre"])}</b><span>desde '
                    f'${data.landed_m2(m, data.zona_de(x["estado"]))}/m² puesto</span><span>3 a 5 días hábiles</span>'
                    '</a></li>' for x in ciudades)
    return f'<ul class="vt-ciudades">{filas}</ul>'


def preguntas_h3(items):
    """Encabezados en pregunta con su respuesta corta (h3 + párrafo): costo, tiempo, mínimo, cómo elegir sin muestra
    e instalación en las ciudades; criterios en la página de perros. La pregunta se escapa; la respuesta es HTML en
    línea de confianza (constantes de tools/site/contenido con enlaces <a>), nunca texto de usuarios."""
    filas = "".join(f'<li class="vt-recomendado"><h3>{esc(q)}</h3><p>{a}</p></li>' for q, a in items)
    return f'<ul class="vt-recomendados">{filas}</ul>'
