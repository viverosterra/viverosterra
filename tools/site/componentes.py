"""Componentes del cuerpo de página del híbrido "Plano + Etiqueta" (Etapa 2).

Funciones puras que devuelven HTML para las plantillas de tools/site/plantillas/. Los textos que llegan de
tools/site/contenido/ son HTML en línea de confianza (solo las etiquetas de ETIQUETAS_PERMITIDAS; test_contenido.py lo
verifica); los atributos (href, src, alt, data-*) se escapan aquí. Todo número oficial sale de datos.py y la fórmula de
mensualidades es la de tools/pasto/mensualidades.py (la misma de public/js/vt-mensualidades.js): aquí no se reimplementa.
"""
import html as html_mod
import math
import re
import sys
from pathlib import Path

PASTO = str(Path(__file__).resolve().parents[1] / "pasto")
if PASTO not in sys.path:
    sys.path.append(PASTO)  # al final: tools/pasto también tiene un build.py

import datos  # noqa: E402
import mensualidades  # noqa: E402
from partials import WA_GLIFO, esc  # noqa: E402

P = datos.PRECIOS
ETIQUETAS_PERMITIDAS = frozenset({"a", "b", "i", "em", "strong", "br", "small", "span"})


# ---------- utilidades ----------
def redondear(x):
    """Igual que Math.round de JavaScript para valores positivos (round() de Python lleva los .5 al par)."""
    return int(math.floor(x + 0.5))


def dinero(n):
    return f"${redondear(n):,}"


def formato_m2(x):
    """Como x.toLocaleString('es-MX', {maximumFractionDigits: 1}): 48 → "48", 1234.5 → "1,234.5"."""
    texto = f"{x:,.1f}"
    return texto[:-2] if texto.endswith(".0") else texto


def texto_plano(fragmento):
    """Texto sin etiquetas ni entidades, con espacios normalizados (para el JSON-LD)."""
    sin_etiquetas = re.sub(r"<[^>]+>", "", fragmento)
    return re.sub(r"\s+", " ", html_mod.unescape(sin_etiquetas)).strip()


def etiquetas_no_permitidas(fragmento):
    """Nombres de etiqueta del fragmento que no están en ETIQUETAS_PERMITIDAS, ordenados."""
    return sorted({t.lower() for t in re.findall(r"</?([a-zA-Z][\w-]*)", fragmento)} - ETIQUETAS_PERMITIDAS)


# ---------- CTA (dos textos y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008") ----------
def boton_wa(mensaje, cta):
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→</span></a>')


def boton_tel(cta):
    return (f'<a class="vt-btn vt-btn--linea" data-cta="{esc(cta)}" href="tel:{datos.TELEFONO_TEL}">'
            f'<svg class="vt-ico" aria-hidden="true"><use href="#vt-i-tel"/></svg>Llamar {datos.TELEFONO_VISIBLE}</a>')


def fila_cta(mensaje, tipo, seccion, hero=False):
    """WhatsApp + teléfono + promesa única. Con hero=True, terra.js oculta la barra móvil mientras se ve."""
    cta = f"{tipo}:{seccion}"
    marca = " data-hero-cta" if hero else ""
    return (f'<div class="vt-cta"{marca}>{boton_wa(mensaje, cta)}{boton_tel(cta)}</div>'
            f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p>')


# ---------- estructura ----------
def migas(items):
    """Ruta visible: [(texto, href), …, (texto, None)]; el último es la página actual."""
    partes = [f'<li aria-current="page">{texto}</li>' if href is None else f'<li><a href="{esc(href)}">{texto}</a></li>'
              for texto, href in items]
    return f'<nav class="vt-crumbs" aria-label="Ruta de navegación"><ol>{"".join(partes)}</ol></nav>'


def bloque(numero, rotulo, id_titulo, titulo, cuerpo, lede=None, tinte=False, id_seccion=None):
    """Sección numerada con encabezado a dos columnas (título y entrada)."""
    clase = "vt-bloque vt-bloque--tinte" if tinte else "vt-bloque"
    ident = f' id="{esc(id_seccion)}"' if id_seccion else ""
    entrada = f'<p class="vt-lede">{lede}</p>' if lede else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{esc(id_titulo)}"><div class="vt-wrap">'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p>'
            f'<div class="vt-bloque__cabeza"><h2 id="{esc(id_titulo)}">{titulo}</h2>{entrada}</div>{cuerpo}</div></section>')


def bloque_dos(numero, rotulo, id_titulo, titulo, izquierda, derecha, tinte=False, id_seccion=None):
    """Sección numerada a dos columnas: título y apoyo a la izquierda, contenido a la derecha."""
    clase = "vt-bloque vt-bloque--tinte" if tinte else "vt-bloque"
    ident = f' id="{esc(id_seccion)}"' if id_seccion else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{esc(id_titulo)}"><div class="vt-wrap vt-dos"><div>'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p><h2 id="{esc(id_titulo)}">{titulo}</h2>{izquierda}</div>'
            f'<div>{derecha}</div></div></section>')


# ---------- etiqueta de precio y cuadro de datos ----------
def etiqueta(e):
    """Etiqueta amarilla de precio. e: codigo, aviso, nombre, cientifico, antes, monto, unidad, filas, nota."""
    filas = "".join(f'<p class="vt-etiqueta__fila"><span>{t}</span><b>{v}</b></p>' for t, v in e.get("filas", ()))
    nota = f'<p class="vt-etiqueta__nota">{e["nota"]}</p>' if e.get("nota") else ""
    return (f'<div class="vt-etiqueta"><p class="vt-etiqueta__cod"><span>{e["codigo"]}</span><span>{e["aviso"]}</span></p>'
            f'<p class="vt-etiqueta__nombre">{e["nombre"]}</p><p class="vt-etiqueta__sci">{e["cientifico"]}</p>'
            f'<p class="vt-etiqueta__precio"><small>{e["antes"]}</small><b>{e["monto"]}</b><span>{e["unidad"]}</span></p>'
            f'{filas}{nota}</div>')


DATOS_EMPRESA = (
    ("Empresa", datos.NOMBRE, "Vivero, pasto y jardinería"),
    ("Registro", f"REPSE {datos.REPSE}", "Contratos con empresas"),
    ("Facturación", datos.FACTURA, "Persona física o moral"),
    ("Desde", str(datos.DESDE), "En Cd. Madero y Tampico"),
    ("Showroom", "Obregón 209 Sur", datos.REFERENCIA),
    ("Instalado", datos.M2_INSTALADOS, "En Tamaulipas y la Huasteca"),
)


def cuadro_datos(celdas=DATOS_EMPRESA):
    cuerpo = "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>" for t, v, s in celdas)
    return f'<dl class="vt-datos">{cuerpo}</dl>'


# ---------- fotos documentales, prueba y clientes ----------
def figura(f, principal=False):
    """Foto con pie FIG. f: src, ancho, alto, alt, numero, lugar, etapa y opcionales srcset y sizes. Solo la imagen
    principal carga con prioridad; las demás son lazy."""
    carga = 'loading="eager" fetchpriority="high"' if principal else 'loading="lazy"'
    srcset = f' srcset="{esc(f["srcset"])}" sizes="{esc(f["sizes"])}"' if f.get("srcset") else ""
    return (f'<figure class="vt-fig"><div class="vt-fig__marco"><img src="{esc(f["src"])}"{srcset} width="{esc(f["ancho"])}" '
            f'height="{esc(f["alto"])}" {carga} decoding="async" alt="{esc(f["alt"])}"></div>'
            f'<figcaption><span><b>Fig. {f["numero"]:02d}</b> · {f["lugar"]}</span><span>{f["etapa"]}</span></figcaption>'
            f'</figure>')


def obras(figuras, nota_html=""):
    return f'<div class="vt-obras">{"".join(figura(f) for f in figuras)}{nota_html}</div>'


def nota(texto, firma):
    return (f'<aside class="vt-nota" aria-label="Nota de campo"><span class="vt-nota__t">Nota de campo</span>'
            f'<p>{texto}</p><span class="vt-nota__firma">{firma}</span></aside>')


def linea_prueba():
    return (f'<p class="vt-prueba"><span><b>{esc(datos.GOOGLE)}</b></span>'
            f'<span><b>{datos.M2_INSTALADOS}</b> instalados en Tamaulipas y la Huasteca</span>'
            f'<span><b>{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones</b> desde {datos.DESDE}</span></p>')


# Nombre (igual que datos.CLIENTES_B2B), archivo en /img/clientes/<archivo>-c.webp, ancho y alto. Sin archivo, el
# cliente va con su nombre en texto (nunca un logo inventado).
LOGOS = (
    ("BMW", "logo-bmw", 120, 120),
    ("Taghleef Industries", "logo-taghleef", 584, 120),
    ("Gobierno de Tampico", "logo-gobierno-tampico", 198, 120),
    ("Grupo Velas", "logo-grupo-velas", 229, 120),
    ("Velamar", "logo-velamar", 188, 120),
    ("Flex", "logo-flex", 120, 120),
    ("Renault", None, 0, 0),
)


def _logo(nombre, archivo, ancho, alto):
    if archivo is None:
        return f'<li class="vt-logos__nombre">{esc(nombre)}</li>'
    return (f'<li><img src="/img/clientes/{archivo}-c.webp" width="{ancho}" height="{alto}" alt="{esc(nombre)}" '
            f'loading="lazy" decoding="async"></li>')


def logos():
    return f'<ul class="vt-logos" aria-label="Clientes de Viveros Terra">{"".join(_logo(*l) for l in LOGOS)}</ul>'


def testimonios(items):
    """Opiniones reales con nombre (publicadas con permiso del dueño). items: (cita, nombre, servicio · lugar)."""
    filas = "".join(f'<li><figure class="vt-testimonio"><blockquote><p>“{cita}”</p></blockquote><figcaption>'
                    f'<b>{nombre}</b><span>{detalle}</span></figcaption></figure></li>' for cita, nombre, detalle in items)
    return f'<ul class="vt-testimonios">{filas}</ul>'


# ---------- índice de servicios, tablas y relacionados ----------
def indice(items):
    """Filas tipo índice: foto, título con enlace, qué incluye y "desde" con la marca amarilla."""
    filas = "".join(
        f'<li><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" loading="lazy" decoding="async">'
        f'<h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p>'
        f'<p class="vt-indice__desde">desde <span class="vt-precio-marca">{i["desde"]}</span> {i["unidad"]}</p></li>'
        for i in items)
    return f'<ol class="vt-indice">{filas}</ol>'


def tabla_precios(filas, caption, concepto="Concepto"):
    """Lista de precios con columna Unidad. filas: nombre, detalle, unidad, precio (número), desde, rec (recomendado)."""
    cuerpo = []
    for f in filas:
        clase = ' class="vt-tabla__rec"' if f.get("rec") else ""
        desde = "<small>desde</small>" if f.get("desde") else ""
        precio = f"<span>{dinero(f['precio'])}</span>" if f.get("rec") else dinero(f["precio"])
        cuerpo.append(f'<tr{clase}><th scope="row"><b>{f["nombre"]}</b><span>{f["detalle"]}</span></th>'
                      f'<td class="vt-tabla__u">{f["unidad"]}</td><td class="vt-tabla__p">{desde}{precio}</td></tr>')
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            f'<th scope="col">{concepto}</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{"".join(cuerpo)}</tbody></table>')


def tabla_comparativa(columnas, filas, caption):
    """Tabla de comparación: la primera columna es el encabezado de cada fila. Se desliza en celular si no cabe."""
    cabeza = "".join(f'<th scope="col">{c}</th>' for c in columnas)
    cuerpo = "".join(f'<tr><th scope="row">{f[0]}</th>{"".join(f"<td>{v}</td>" for v in f[1:])}</tr>' for f in filas)
    return (f'<div class="vt-desliza" role="region" aria-label="{esc(texto_plano(caption))}" tabindex="0">'
            f'<table class="vt-tabla"><caption>{caption}</caption><thead><tr>{cabeza}</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table></div>')


def relacionados(items):
    filas = "".join(f'<li><h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p></li>' for i in items)
    return f'<ul class="vt-relacionados">{filas}</ul>'


def guias(items, href_todas="/blog"):
    filas = "".join(f'<li><a href="{esc(href)}">{texto}</a></li>' for texto, href in items)
    return f'<ul class="vt-guias">{filas}<li><a href="{esc(href_todas)}">Ver todas las guías</a></li></ul>'


# ---------- proceso, garantía, FAQ y cierre ----------
QUIEN = {"nosotros": ("Nosotros", ""), "tu": ("Tú", " vt-quien--tu"), "juntos": ("Juntos", " vt-quien--juntos")}


def pasos(items):
    """Proceso con marcadores NOSOTROS / TÚ / JUNTOS. items: titulo, quien, cuando, texto."""
    filas = "".join(
        f'<li><h3>{p["titulo"]} <span class="vt-quien{QUIEN[p["quien"]][1]}">{QUIEN[p["quien"]][0]}</span></h3>'
        f'<p class="vt-pasos__cuando">{p["cuando"]}</p><p>{p["texto"]}</p></li>' for p in items)
    return f'<ol class="vt-pasos">{filas}</ol>'


def pasos_compra(items):
    """Lista breve "de la cotización a tu jardín" (la misma que el HowTo del JSON-LD). items: (nombre, texto)."""
    filas = "".join(f"<li><b>{nombre}.</b> {texto}</li>" for nombre, texto in items)
    return f'<ol class="vt-compra">{filas}</ol>'


def howto(nombre, items):
    return {"@type": "HowTo", "name": nombre,
            "step": [{"@type": "HowToStep", "position": i, "name": texto_plano(n), "text": texto_plano(t)}
                     for i, (n, t) in enumerate(items, 1)]}


def garantia(g):
    """g: titulo, id_titulo, numero, rotulo, grande, unidad, resumen, puntos (texto, si_aplica), pie."""
    no_aplica = ' class="vt-checks__no"'
    puntos = "".join(f'<li{"" if ok else no_aplica}>{t}</li>' for t, ok in g["puntos"])
    ident = esc(g["id_titulo"])
    return (f'<section class="vt-bloque vt-bloque--tinte" aria-labelledby="{ident}"><div class="vt-wrap vt-dos">'
            f'<div><p class="vt-bloque__no"><b>{g["numero"]:02d}</b>{g["rotulo"]}</p><h2 id="{ident}">'
            f'{g["titulo"]}</h2><p class="vt-grande">{g["grande"]}<small> {g["unidad"]}</small></p>'
            f'<p class="vt-promesa">{g["resumen"]}</p></div><div><ul class="vt-checks">{puntos}</ul>'
            f'<p class="vt-promesa">{g["pie"]}</p></div></div></section>')


def faq(preguntas):
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
                    for i, (q, a) in enumerate(preguntas))
    return f'<div class="vt-faq">{items}</div>'


def faq_jsonld(preguntas, speakable=None):
    """FAQPage con las mismas preguntas y respuestas visibles (en texto plano)."""
    nodo = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": texto_plano(q), "acceptedAnswer": {"@type": "Answer", "text": texto_plano(a)}}
        for q, a in preguntas]}
    if speakable:
        nodo["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": list(speakable)}
    return nodo


def cierre(titulo, lede, mensaje, tipo):
    """CTA final en verde profundo, con el mensaje que se abre a la vista."""
    return (f'<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
            f'<h2 id="vt-cierre-titulo">{titulo}</h2><p class="vt-lede">{lede}</p>{fila_cta(mensaje, tipo, "cierre")}</div>'
            f'<p class="vt-cierre__msg"><b>El mensaje que se abre</b>{esc(datos.con_firma(mensaje))}</p></div></section>')


# ---------- mensualidades con tarjeta de crédito ----------
def planes_mensualidades():
    """Plazos y montos mínimos de tools/pasto/mensualidades.py (los mismos de vt-mensualidades.js)."""
    celdas = "".join(f"<div><dt>{p} mensualidades</dt><dd>desde {dinero(mensualidades.minimo_de(p))}</dd></div>"
                     for p in mensualidades.PLAZOS)
    return ('<div class="vt-planes"><div class="vt-planes__cabeza"><b>Mensualidades con tarjeta de crédito</b>'
            '<span>El contado (transferencia, efectivo o tarjeta en una exhibición) es el precio más bajo.</span></div>'
            f'<dl>{celdas}</dl><p>Montos mínimos de cotización por plazo. El total a plazos es mayor que el de contado y '
            'te lo mostramos antes de enviarte el link de pago. Tu banco debe aceptar el plan. '
            '<a href="/politicas#mensualidades">Condiciones</a></p></div>')


def simulador(servicio, monto, tipo):
    """Marcado que espera public/js/vt-simulador.js ([data-simulador], [data-sim-monto], [data-sim-list], [data-sim-wa])."""
    return (f'<div class="vt-sim" data-simulador data-servicio="{esc(servicio)}"><div class="vt-campo">'
            '<label for="vt-sim-monto">Monto de tu cotización</label><div class="vt-control">'
            f'<input id="vt-sim-monto" type="number" inputmode="numeric" min="0" step="100" value="{int(monto)}" '
            'data-sim-monto><span>MXN</span></div></div>'
            '<div class="vt-sim__lista" role="radiogroup" aria-label="Forma de pago" data-sim-list></div>'
            '<p class="vt-promesa">Montos aproximados: tu banco debe aceptar el plan. Disponible en cotizaciones desde '
            f'{dinero(mensualidades.minimo_de(3))}.</p><a class="vt-btn vt-btn--wa" data-cta="{tipo}:simulador" '
            f'data-sim-wa href="https://wa.me/{datos.TELEFONO_WA}" target="_blank" rel="noopener">{WA_GLIFO}'
            'Cotizar por WhatsApp</a></div>')


# ---------- Medidor de m² (mismo cálculo que public/js/vt-medidor.js; paridad en casos-medidor.json) ----------
MINIMO_MAYOREO = P["pasto_mayoreo_minimo_m2"]
MODOS_MEDIDOR = {
    "instalado": {"precio": P["pasto_instalado_m2"], "desde": True, "texto": "pasto San Agustín instalado",
                  "rotulo": "Instalado · desde", "opcion": "Pasto instalado"},
    "solo": {"precio": P["pasto_solo_m2"], "desde": False, "texto": "solo el pasto San Agustín (yo lo instalo)",
             "rotulo": "Solo pasto", "opcion": "Solo el pasto, yo lo instalo"},
    "mayoreo": {"precio": P["pasto_mayoreo_m2"], "desde": True, "minimo": MINIMO_MAYOREO,
                "texto": "pasto San Agustín de mayoreo (solo pasto)", "rotulo": "Mayoreo · desde",
                "opcion": f"Mayoreo, {MINIMO_MAYOREO} m² o más"},
}
PLANO = {"ancho": 360, "alto": 190, "x": 44, "y": 56, "minimo": 24}


def calculo_medidor(largo, ancho, modo):
    """m², precio por m², total y aviso. El mayoreo es solo pasto: con menos del mínimo calcula a precio de solo pasto
    y lo avisa (J03 §3)."""
    m = MODOS_MEDIDOR[modo]
    m2 = redondear(largo * ancho * 10) / 10
    precio, desde, texto, rotulo, aviso = m["precio"], m["desde"], m["texto"], m["rotulo"], ""
    minimo = m.get("minimo")
    if minimo and m2 < minimo:
        solo = MODOS_MEDIDOR["solo"]
        precio, desde, texto = solo["precio"], False, solo["texto"]
        rotulo = f"Solo pasto (mayoreo desde {minimo} m²)"
        aviso = (f"El mayoreo aplica desde {minimo} m². Te faltan {math.ceil(minimo - m2)} m²; mientras, calculamos "
                 f"a ${precio}/m² (solo pasto).")
    return {"m2": m2, "precio": precio, "desde": desde, "texto": texto, "rotulo": rotulo, "aviso": aviso,
            "total": redondear(m2 * precio)}


def textos_medidor(largo, ancho, r, colonia=""):
    """Textos de la etiqueta y mensaje de WhatsApp para el resultado `r` de calculo_medidor."""
    medida = f"{largo:.2f} × {ancho:.2f} m = {formato_m2(r['m2'])} m²"
    desde = "desde " if r["desde"] else ""
    disponibles = mensualidades.plazos_disponibles(r["total"])
    if disponibles:
        ultimo = disponibles[-1]
        total = mensualidades.total_a_plazos(r["total"], ultimo)
        plan = (f"O {ultimo} mensualidades de {dinero(total / ultimo)} con tarjeta de crédito "
                f"(total {dinero(total)}).")
    else:
        plan = f"Mensualidades con tarjeta de crédito en cotizaciones desde {dinero(mensualidades.minimo_de(3))}."
    cierre_calc = "Al medir te damos el precio cerrado." if r["desde"] else "La entrega se cotiza según tu colonia."
    mensaje = "\n".join((f"Hola, quiero cotizar {r['texto']}.", f"Medidas: {medida}",
                         f"Estimado de la web: {desde}{dinero(r['total'])} con IVA", f"Colonia: {colonia or '___'}",
                         "Te mando foto del área."))
    return {"medida": medida, "monto": dinero(r["total"]),
            "calc": f"{formato_m2(r['m2'])} m² × {desde}${r['precio']}/m², con IVA. {cierre_calc}",
            "plan": plan, "mensaje": mensaje}


def plano_medidor(largo, ancho):
    """Rectángulo del patio a escala dentro del plano de 480 × 300 (mismo cálculo que vt-medidor.js)."""
    escala = min(PLANO["ancho"] / largo, PLANO["alto"] / ancho)
    w, h = max(PLANO["minimo"], largo * escala), max(PLANO["minimo"], ancho * escala)
    return {"x": PLANO["x"] + (PLANO["ancho"] - w) / 2, "y": PLANO["y"] + (PLANO["alto"] - h) / 2, "w": w, "h": h}


def _n(v):
    return f"{v:.1f}"


def svg_plano(largo, ancho, m2):
    g = plano_medidor(largo, ancho)
    x, y, w, h = g["x"], g["y"], g["w"], g["h"]
    lado = x + w + 22
    rect = f'x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}"'
    area_visible = "" if w > 96 and h > 34 else ' style="display:none"'
    return (
        '<svg viewBox="0 0 480 300" role="img" aria-label="Tu patio dibujado a escala, visto desde arriba">'
        f'<rect class="vt-plano-relleno" data-vt-plano {rect}/><rect class="vt-plano-borde" data-vt-plano {rect}/>'
        f'<path class="vt-cota" data-vt-cota="arriba" d="M{_n(x)} {_n(y - 26)} v14 M{_n(x + w)} {_n(y - 26)} v14 '
        f'M{_n(x)} {_n(y - 19)} H{_n(x + w)}"/>'
        f'<text class="vt-cota-t" data-vt-texto="arriba" x="{_n(x + w / 2)}" y="{_n(y - 32)}" text-anchor="middle">'
        f'{largo:.2f} m</text>'
        f'<path class="vt-cota" data-vt-cota="lado" d="M{_n(lado - 7)} {_n(y)} h14 M{_n(lado - 7)} {_n(y + h)} h14 '
        f'M{_n(lado)} {_n(y)} V{_n(y + h)}"/>'
        f'<text class="vt-cota-t" data-vt-texto="lado" text-anchor="middle" '
        f'transform="translate({_n(lado + 20)} {_n(y + h / 2)}) rotate(-90)">{ancho:.2f} m</text>'
        f'<text class="vt-cota-a" data-vt-texto="area" x="{_n(x + w / 2)}" y="{_n(y + h / 2 + 9)}" '
        f'text-anchor="middle"{area_visible}>{formato_m2(m2)} m²</text></svg>')


def _opcion_medidor(prefijo, clave, m, elegido):
    marcado = " checked" if clave == elegido else ""
    minimo = f' data-minimo="{m["minimo"]}"' if m.get("minimo") else ""
    precio = f'{"desde " if m["desde"] else ""}${m["precio"]}/m²'
    return (f'<label><span>{m["opcion"]}</span><small>{precio}</small><input type="radio" name="{prefijo}-modo" '
            f'value="{clave}" data-precio="{m["precio"]}" data-desde="{1 if m["desde"] else 0}" '
            f'data-texto="{esc(m["texto"])}" data-rotulo="{esc(m["rotulo"])}"{minimo}{marcado}></label>')


def medidor(prefijo, tipo, largo=8, ancho=6, modo="instalado", mensaje=None):
    """Medidor: largo × ancho → plano a escala → etiqueta con el estimado y mensualidades → WhatsApp con la medida.
    Sin JavaScript queda el cálculo inicial y un enlace válido. vt-medidor.js lo actualiza con los data-* de cada
    opción: los precios no viven en el JS. data-wa (número) y data-mensaje (mensaje genérico de la página, con firma)
    le dan el destino; sin medida válida, el botón manda el genérico y nunca un estimado viejo."""
    generico = datos.con_firma(mensaje or datos.MENSAJES["general"])
    r = calculo_medidor(largo, ancho, modo)
    t = textos_medidor(largo, ancho, r)
    opciones = "".join(_opcion_medidor(prefijo, k, m, modo) for k, m in MODOS_MEDIDOR.items())
    campo = ('<div class="vt-campo"><label for="{p}-{n}">{t}</label><div class="vt-control"><input id="{p}-{n}" '
             'data-vt-campo="{n}" inputmode="decimal" value="{v}" autocomplete="off"><span>m</span></div></div>')
    return (
        f'<div class="vt-medidor" data-vt-medidor data-wa="{esc(datos.TELEFONO_WA)}" data-mensaje="{esc(generico)}">'
        f'<div class="vt-medidor__form" role="group" aria-label="Medidor de pasto">'
        f'<div class="vt-medidor__medidas">{campo.format(p=prefijo, n="largo", t="Largo", v=largo)}'
        f'<span class="vt-medidor__x" aria-hidden="true">×</span>{campo.format(p=prefijo, n="ancho", t="Ancho", v=ancho)}'
        f'</div><fieldset class="vt-opciones"><legend>¿Qué necesitas?</legend>{opciones}</fieldset>'
        f'<div class="vt-campo"><label for="{prefijo}-colonia">Colonia (opcional)</label><div class="vt-control">'
        f'<input type="text" id="{prefijo}-colonia" data-vt-campo="colonia" placeholder="Ej. Lomas de Rosales" '
        f'autocomplete="off"></div></div></div>'
        f'<figure class="vt-fig vt-medidor__plano">{svg_plano(largo, ancho, r["m2"])}<figcaption><span><b>Vista en planta'
        f'</b> · escala ajustada a tu medida</span><span>Cotas en metros</span></figcaption></figure>'
        f'<div class="vt-etiqueta vt-medidor__res" role="status"><p class="vt-etiqueta__cod"><span>Tu etiqueta</span><span>Estimado'
        f'</span></p><p class="vt-etiqueta__nombre" data-vt-o="m2">{t["medida"]}</p><p class="vt-etiqueta__sci">'
        f'Stenotaphrum secundatum</p><p class="vt-etiqueta__precio"><small data-vt-o="rotulo">'
        f'{r["rotulo"]}</small><b data-vt-o="monto">{t["monto"]}</b><span>con IVA</span></p>'
        f'<p class="vt-medidor__calc" data-vt-o="calc">{t["calc"]}</p>'
        f'<p class="vt-medidor__aviso" data-vt-o="aviso"{"" if r["aviso"] else " hidden"}>{r["aviso"]}</p>'
        f'<p class="vt-medidor__plan" data-vt-o="plan">{t["plan"]}</p>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{tipo}:medidor" data-vt-o="cta" href="{esc(datos.wa_url(t["mensaje"]))}" '
        f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→'
        f'</span></a></div></div>')


# ---------- portada (primer pantallazo: qué, dónde, precio y CTA) ----------
def portada(p, tipo, migas_items=None):
    """p: kicker, h1, lede, etiqueta, mensaje, tambien y foto. Con migas_items, la ruta visible va arriba."""
    ruta = migas(migas_items) if migas_items else ""
    return (f'<section class="vt-portada" aria-labelledby="vt-h1"><div class="vt-wrap">{ruta}<div class="vt-portada__grid">'
            f'<div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1><p class="vt-lede">{p["lede"]}</p>'
            f'<div class="vt-portada__trato">{etiqueta(p["etiqueta"])}<div>{fila_cta(p["mensaje"], tipo, "hero", hero=True)}'
            f'<p class="vt-portada__tambien">{p["tambien"]}</p></div></div></div>'
            f'<div class="vt-portada__foto">{figura(p["foto"], principal=True)}</div></div>{cuadro_datos()}</div></section>')
