"""Componentes del cuerpo de página del híbrido "Plano + Etiqueta" (Etapa 2).

Funciones puras que devuelven HTML para las plantillas de tools/site/plantillas/. Los textos que llegan de
tools/site/contenido/ son HTML en línea de confianza (solo las etiquetas de ETIQUETAS_PERMITIDAS; test_contenido.py lo
verifica); los atributos (href, src, alt, data-*) se escapan aquí. Todo número oficial sale de datos.py y la fórmula de
mensualidades es la de tools/pasto/mensualidades.py (la misma de public/js/vt-mensualidades.js): aquí no se reimplementa.
"""
import html as html_mod
import json
import math
import re
import sys
from pathlib import Path

PASTO = str(Path(__file__).resolve().parents[1] / "pasto")
if PASTO not in sys.path:
    sys.path.append(PASTO)  # al final: tools/pasto también tiene un build.py

import datos  # noqa: E402
import entidad  # noqa: E402
import mensualidades  # noqa: E402
from partials import WA_GLIFO, esc  # noqa: E402

P = datos.PRECIOS
ETIQUETAS_PERMITIDAS = frozenset({"a", "b", "i", "em", "strong", "br", "small", "span"})


# ---------- utilidades ----------
redondear = mensualidades.redondear  # Math.round de JavaScript: la misma función que usan las mensualidades


def dinero(n):
    return f"${redondear(n):,}"


def dinero_exacto(n):
    """Como dinero, pero respeta los centavos de un precio oficial: 446.6 → "$446.60", 754 → "$754"."""
    return f"${n:,.2f}" if n != int(n) else f"${int(n):,}"


def formato_m2(x):
    """Como x.toLocaleString('es-MX', {maximumFractionDigits: 1}): 48 → "48", 1234.5 → "1,234.5"."""
    texto = f"{x:,.1f}"
    return texto[:-2] if texto.endswith(".0") else texto


UNIDADES_RE = re.compile(r"(?<![\w/])(?:g/m²|/m²|m²)")


def unidades(fragmento):
    """Envuelve m², /m² y g/m² en <span class="vt-u"> para que los rótulos en mayúsculas no los vuelvan "M²"."""
    return UNIDADES_RE.sub(lambda m: f'<span class="vt-u">{m.group(0)}</span>', fragmento)


def mayusculas_sin_unidades(texto):
    """Mayúsculas para un atributo que CSS muestra tal cual (data-col de las tablas en celular), sin tocar m² y g/m²."""
    partes = UNIDADES_RE.split(texto)
    unidades_ = UNIDADES_RE.findall(texto)
    return "".join(p.upper() + (unidades_[i] if i < len(unidades_) else "") for i, p in enumerate(partes))


def texto_plano(fragmento):
    """Texto sin etiquetas ni entidades, con espacios normalizados (para el JSON-LD)."""
    sin_etiquetas = re.sub(r"<[^>]+>", "", fragmento)
    return re.sub(r"\s+", " ", html_mod.unescape(sin_etiquetas)).strip()


def etiquetas_no_permitidas(fragmento):
    """Nombres de etiqueta del fragmento que no están en ETIQUETAS_PERMITIDAS, ordenados."""
    return sorted({t.lower() for t in re.findall(r"</?([a-zA-Z][\w-]*)", fragmento)} - ETIQUETAS_PERMITIDAS)


# ---------- CTA (dos textos y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008") ----------
CTA_WA = "Cotizar por WhatsApp"
# Única variante, solo en el botón del Medidor cuando ya hay una medida válida (spec del hero, 2026-11-09, §4). El mismo
# texto vive en public/js/vt-medidor.js (paridad en tests/test_medidor_paridad.py).
CTA_MEDIDA = "Enviar mi medida por WhatsApp"
# Con medida válida la barra fija de celular y el encabezado mandan la misma medida (vt-medidor.js lee el texto de
# data-vt-barra; en la home desde la revisión del hero, en todos los medidores desde la Entrega B de experiencia).
CTA_MEDIDA_BARRA = "Enviar mi medida"
# Aviso del Medidor con un lado escrito que no es un número mayor que 0 (reescritura 2 del informe de recorrido). El mismo
# texto vive en public/js/vt-medidor.js (paridad en tests/test_medidor_paridad.py).
ERROR_MEDIDOR = "Escribe el largo y el ancho en metros, solo con números. Ejemplo: 8 y 6."
# Condiciones de la garantía de arraigo del pasto: el protocolo de cuidados (la página no tiene un id en esa sección).
CONDICIONES_PASTO = "/protocolo-cuidados-pasto-san-agustin#garantia"  # sección de condiciones (plantillas/protocolo.py)
CONDICIONES_PLANTAS = "/politicas#garantia-plantas"  # condiciones de la garantía de plantas (contenido/politicas.py)


def boton_wa(mensaje, cta, texto=CTA_WA):
    """Botón de WhatsApp. `texto` solo cambia en las filas de sección de la home (revisión de diseño, 2026-11-09)."""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>')


def promesa_horario():
    """La promesa única dentro de un <span> con el horario y los festivos de datos.py: en horario, terra.js le antepone
    "Abierto ahora · ". Sin JS o fuera de horario se lee tal cual. data-vt-build es la fecha de datos.ACTUALIZADO: un
    cliente con el reloj antes de esa fecha no ve "Abierto ahora"."""
    return (f'<span data-vt-horario="{esc(datos.horario_marca())}" data-vt-festivos="{esc(datos.festivos_marca())}" '
            f'data-vt-build="{esc(datos.ACTUALIZADO)}">{esc(datos.PROMESA_COMPLETA)}</span>')


def garantia_pasto(prefijo=""):
    """datos.GARANTIA_PASTO con "ver condiciones" enlazado al protocolo de cuidados del pasto. Con prefijo ("Pasto
    instalado: "), la frase sigue en minúscula."""
    texto, condiciones = esc(datos.GARANTIA_PASTO), "ver condiciones"
    if texto.count(condiciones) != 1:
        raise ValueError("datos.GARANTIA_PASTO debe decir “ver condiciones” una sola vez")
    if prefijo:
        texto = esc(prefijo) + texto[0].lower() + texto[1:]
    return texto.replace(condiciones, f'<a href="{CONDICIONES_PASTO}">{condiciones}</a>')


def garantia_pasto_corta():
    """Plan visual V1 (2026-11-11): la garantía completa va una vez por página; donde ya se dijo, esta versión corta
    con el mismo enlace a condiciones. Solo usa datos.ARRAIGO: no agrega promesas."""
    return (f'Garantía de arraigo de {esc(datos.ARRAIGO)} en el pasto instalado '
            f'(<a href="{CONDICIONES_PASTO}">ver condiciones</a>).')


def garantia_plantas():
    """datos.GARANTIA_PLANTAS con "ver condiciones" enlazado a la garantía de plantas de Políticas."""
    texto, condiciones = esc(datos.GARANTIA_PLANTAS), "ver condiciones"
    if texto.count(condiciones) != 1:
        raise ValueError("datos.GARANTIA_PLANTAS debe decir “ver condiciones” una sola vez")
    return texto.replace(condiciones, f'<a href="{CONDICIONES_PLANTAS}">{condiciones}</a>')


def tierra_negra_cruzada():
    """Venta cruzada junto a la condición de terreno listo (pasto en rollo y Medidor): solo el enlace."""
    return f'<a href="{datos.TIERRA_NEGRA_RUTA}">{esc(datos.TIERRA_NEGRA_CRUZADA)}</a>'


def boton_tel(cta):
    return (f'<a class="vt-btn vt-btn--linea" data-cta="{esc(cta)}" href="tel:{datos.TELEFONO_TEL}">'
            f'<svg class="vt-ico" aria-hidden="true"><use href="#vt-i-tel"/></svg>Llamar {datos.TELEFONO_VISIBLE}</a>')


def boton_mapas(cta):
    return (f'<a class="vt-btn vt-btn--linea" data-cta="{esc(cta)}" href="{esc(datos.MAPS_URL)}" target="_blank" '
            f'rel="noopener">Cómo llegar</a>')


def fila_cta(mensaje, tipo, seccion, hero=False, extra="", texto=CTA_WA):
    """WhatsApp + extra (otro botón, opcional) + teléfono + promesa única. Con hero=True, terra.js oculta la barra móvil
    mientras se ve. texto: el del botón de WhatsApp (dice qué se pide: Entrega B de experiencia)."""
    cta = f"{tipo}:{seccion}"
    marca = " data-hero-cta" if hero else ""
    return (f'<div class="vt-cta"{marca}>{boton_wa(mensaje, cta, texto)}{extra}{boton_tel(cta)}</div>'
            f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p>')


def fila_seccion(mensaje, tipo, seccion, texto, contexto=False):
    """CTA de WhatsApp al final de una sección larga (Entrega B de experiencia: ningún tramo de más de 6 pantallas del
    celular sin un CTA en línea), como las filas de la home: un solo botón con texto propio (sin la promesa: V1). data-hero-cta:
    la barra fija se esconde mientras se ve, para no mostrar dos botones iguales. contexto=True (tienda): tienda-pasto.js
    le pone el mensaje con lo que el cliente ya eligió (data-vt-ctx)."""
    marca = " data-vt-ctx" if contexto else ""
    # Plan visual V1 (2026-11-11): la promesa de respuesta va una sola vez arriba (línea de confianza del hero) y en el
    # cierre; repetida bajo cada botón de sección eran hasta 8 párrafos iguales por página.
    return f'<div class="vt-cta vt-mt" data-hero-cta{marca}>{boton_wa(mensaje, f"{tipo}:{seccion}", texto)}</div>'


def prueba_cta(opiniones=(), dato=""):
    """Prueba social junto a un CTA (Entrega B de experiencia): solo datos ya publicados en datos.py. Opiniones reales
    del mismo tema (si las hay), la calificación de Google con el enlace a las reseñas y, opcional, una cifra propia."""
    nota, _, resenas = datos.GOOGLE.partition(" ")
    partes = [f"<b>{esc(nota)}</b> {esc(resenas)}"] + ([dato] if dato else [])
    linea = (f'<p class="vt-promesa">{" · ".join(partes)} · <a href="{esc(datos.MAPS_URL)}" target="_blank" '
             'rel="noopener">Ver las reseñas en Google</a></p>')
    return (testimonios(opiniones) if opiniones else "") + linea


# ---------- estructura ----------
def migas(items):
    """Ruta visible: [(texto, href), …, (texto, None)]; el último es la página actual."""
    partes = [f'<li aria-current="page">{texto}</li>' if href is None else f'<li><a href="{esc(href)}">{texto}</a></li>'
              for texto, href in items]
    return f'<nav class="vt-crumbs" aria-label="Ruta de navegación"><ol>{"".join(partes)}</ol></nav>'


def respuesta(r):
    """Respuesta directa de la página, justo después de la portada (SEO fase 1): un párrafo de 40 a 60 palabras con el
    dato en la misma frase (precio, unidad y zona), marcado con data-vt-respuesta para el speakable del JSON-LD, y la
    fecha de la última revisión de precios (datos.PRECIOS_ACTUALIZADOS; nunca la fecha del build). r: texto y fecha,
    los dos opcionales (sin texto, la respuesta es la entrada de la portada y aquí solo va la fecha). Va fuera de la
    portada para no empujar el precio ni el botón de WhatsApp de la primera pantalla."""
    if not r:
        return ""
    texto = (f'<p class="vt-bloque__no"><b>En corto</b></p><p class="vt-lede" {entidad.ATRIBUTO_RESPUESTA}>{r["texto"]}</p>'
             if r.get("texto") else "")
    fecha = (f'<p class="vt-promesa">Actualizado: <time datetime="{esc(r["fecha"])}">{entidad.mes_largo(r["fecha"])}</time></p>'
             if r.get("fecha") else "")
    return f'<section class="vt-respuesta" aria-label="En corto"><div class="vt-wrap">{texto}{fecha}</div></section>'


# Ritmo (Entrega C de experiencia): el relleno vertical de una sección según su papel. "apoyo" (fotos extra, pago,
# preguntas, cobertura, relacionados) va más compacta; "clave" (precio, planes, la banda de garantía) lleva más aire.
RITMOS = {None: "", "apoyo": " vt-bloque--apoyo", "clave": " vt-bloque--clave"}


def _clase_bloque(tinte, ritmo):
    return ("vt-bloque vt-bloque--tinte" if tinte else "vt-bloque") + RITMOS[ritmo]


def bloque(numero, rotulo, id_titulo, titulo, cuerpo, lede=None, tinte=False, id_seccion=None, ritmo=None):
    """Sección numerada con encabezado a dos columnas (título y entrada). ritmo: None, "apoyo" o "clave"."""
    clase = _clase_bloque(tinte, ritmo)
    ident = f' id="{esc(id_seccion)}"' if id_seccion else ""
    entrada = f'<p class="vt-lede">{lede}</p>' if lede else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{esc(id_titulo)}"><div class="vt-wrap">'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p>'
            f'<div class="vt-bloque__cabeza"><h2 id="{esc(id_titulo)}">{titulo}</h2>{entrada}</div>{cuerpo}</div></section>')


def bloque_dos(numero, rotulo, id_titulo, titulo, izquierda, derecha, tinte=False, id_seccion=None, ritmo=None):
    """Sección numerada a dos columnas: título y apoyo a la izquierda, contenido a la derecha."""
    clase = _clase_bloque(tinte, ritmo)
    ident = f' id="{esc(id_seccion)}"' if id_seccion else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{esc(id_titulo)}"><div class="vt-wrap vt-dos"><div>'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p><h2 id="{esc(id_titulo)}">{titulo}</h2>{izquierda}</div>'
            f'<div>{derecha}</div></div></section>')


# ---------- etiqueta de precio y cuadro de datos ----------
def etiqueta(e, cordel=True):
    """Etiqueta amarilla de precio. e: codigo, aviso, nombre, cientifico, antes, monto, unidad, filas, nota y cond. El
    envoltorio lleva la sombra y, con cordel=True, el cordel que cuelga del ojal (solo en escritorio). cond: la condición
    del precio en una línea chica pegada a la banda amarilla, visible también en la etiqueta compacta del celular
    (datos.TERRENO_LISTO_CORTO junto al pasto instalado: decisión del dueño, 2026-11-10)."""
    cond = f'<p class="vt-etiqueta__cond">{esc(e["cond"])}</p>' if e.get("cond") else ""
    filas = [f'<p class="vt-etiqueta__fila"><span>{t}</span><b>{v}</b></p>' for t, v in e.get("filas", ())]
    if cond and e.get("cond_fila"):  # la condición es de una fila (el instalado en /precios): va debajo de ella
        i = e["cond_fila"]
        filas, cond = filas[:i] + [cond] + filas[i:], ""
    filas = "".join(filas)
    nota = f'<p class="vt-etiqueta__nota">{e["nota"]}</p>' if e.get("nota") else ""
    sci = f'<p class="vt-etiqueta__sci">{e["cientifico"]}</p>' if e.get("cientifico") else ""
    aviso = f'<span>{e["aviso"]}</span>' if e.get("aviso") else ""
    return (f'<div class="vt-etiqueta-x{" vt-etiqueta-x--cordel" if cordel else ""}"><div class="vt-etiqueta">'
            f'<p class="vt-etiqueta__cod"><span>{e["codigo"]}</span>{aviso}</p>'
            f'<p class="vt-etiqueta__nombre">{e["nombre"]}</p>{sci}'
            f'<p class="vt-etiqueta__precio"><small>{unidades(e["antes"])}</small><b>{e["monto"]}</b><span>{e["unidad"]}</span></p>'
            f'{cond}{filas}{nota}</div></div>')


DATOS_EMPRESA = (
    ("Empresa", datos.NOMBRE, "Vivero, pasto y jardinería"),
    ("Registro", f"REPSE {datos.REPSE}", "Contratos con empresas"),
    ("Facturación", datos.FACTURA, "Persona física o moral"),
    ("Desde", str(datos.DESDE), "En Cd. Madero y Tampico"),
    ("Showroom", datos.CALLE_CORTA, datos.REFERENCIA),
    ("Instalado", datos.M2_INSTALADOS, "En Tamaulipas y la Huasteca"),
)


def cuadro_datos(celdas=DATOS_EMPRESA):
    cuerpo = "".join(f"<div><dt>{unidades(esc(t))}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>"
                     for t, v, s in celdas)
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


def mosaico(figuras, desde):
    """Mosaico de fotos reales, numeradas desde `desde`. La primera va ancha salvo que el total sea múltiplo de 3 (la
    retícula de 3 columnas quedaría con un hueco); todas cargan diferido porque van debajo de la primera pantalla."""
    plano = " vt-mosaico--plano" if len(figuras) % 3 == 0 else ""
    primera = "(min-width: 900px) 66vw, 100vw"
    resto = "(min-width: 900px) 33vw, 50vw"
    items = "".join(figura(dict(f, numero=desde + i, sizes=primera if i == 0 and not plano else resto))
                    for i, f in enumerate(figuras))
    return f'<div class="vt-mosaico{plano}">{items}</div>'


def bloque_obras(numero, datos_obras, html_previo, ritmo=None):
    """Sección de fotos de obra. La numeración sigue después de las figuras que ya trae la página."""
    desde = html_previo.count("<b>Fig. ") + 1
    return bloque(numero, "Fotos reales", "vt-h-obras", datos_obras["titulo"], mosaico(datos_obras["figuras"], desde),
                  lede=datos_obras["lede"], ritmo=ritmo)


def nota(texto, firma):
    return (f'<aside class="vt-nota" aria-label="Nota de campo"><span class="vt-nota__t">Nota de campo</span>'
            f'<p>{texto}</p><span class="vt-nota__firma">{firma}</span></aside>')


def linea_prueba():
    return (f'<p class="vt-prueba"><span><b>{esc(datos.GOOGLE)}</b></span>'
            f'<span><b>{datos.M2_INSTALADOS}</b> instalados en Tamaulipas y la Huasteca</span>'
            f'<span><b>{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones</b> desde {datos.DESDE}</span></p>')


# Nombre (igual que datos.CLIENTES_B2B), archivo en /img/clientes/<archivo>-c.webp, ancho, alto y escala. Sin archivo,
# el cliente va con su nombre en texto (nunca un logo inventado). Escala "alto": logos con letra chica (Velamar) van más
# altos para que se lean; el de Flex viene recortado a su palabra.
LOGOS = (
    ("BMW", "logo-bmw", 120, 120, ""),
    ("Taghleef Industries", "logo-taghleef", 584, 120, ""),
    ("Gobierno de Tampico", "logo-gobierno-tampico", 198, 120, ""),
    ("Grupo Velas", "logo-grupo-velas", 229, 120, ""),
    ("Velamar", "logo-velamar", 188, 120, "alto"),
    ("Flex", "logo-flex", 119, 34, ""),
    ("Renault", None, 0, 0, ""),
)


def _logo(nombre, archivo, ancho, alto, escala):
    if archivo is None:
        return f'<li class="vt-logos__nombre">{esc(nombre)}</li>'
    clase = f' class="vt-logos--{escala}"' if escala else ""
    return (f'<li{clase}><img src="/img/clientes/{archivo}-c.webp" width="{ancho}" height="{alto}" alt="{esc(nombre)}" '
            f'loading="lazy" decoding="async"></li>')


def logos():
    return f'<ul class="vt-logos" aria-label="Clientes de Viveros Terra">{"".join(_logo(*l) for l in LOGOS)}</ul>'


def testimonios(items, fila=False):
    """Opiniones reales con nombre (publicadas con permiso del dueño). items: (cita, nombre, servicio · lugar). La
    primera va destacada a todo lo ancho; las demás, compactas. fila=True (servicios, Entrega C de experiencia): en
    celular van una junto a otra con desplazamiento horizontal (scroll-snap), en vez de apiladas; la lista se puede
    enfocar para recorrerla con el teclado."""
    destacado = ' class="vt-testimonios__dest"'
    filas = "".join(f'<li{destacado if i == 0 else ""}><figure class="vt-testimonio"><blockquote>'
                    f'<p>“{cita}”</p></blockquote><figcaption><b>{nombre}</b><span>{detalle}</span></figcaption></figure>'
                    f'</li>' for i, (cita, nombre, detalle) in enumerate(items))
    if fila:
        return (f'<ul class="vt-testimonios vt-testimonios--fila" tabindex="0" aria-label="Opiniones de clientes">'
                f'{filas}</ul>')
    return f'<ul class="vt-testimonios">{filas}</ul>'


# ---------- índice de servicios, tablas y relacionados ----------
def _cotizar_servicio(item, tipo):
    """Enlace "Cotizar <servicio>" de una fila del índice, con el glifo de WhatsApp (la flecha es la de la fila) y el
    mensaje de datos.MENSAJES de ese servicio."""
    servicio = item["servicio"]
    return (f'<a class="vt-indice__wa" data-cta="{esc(tipo)}:indice-{esc(servicio)}" '
            f'href="{esc(datos.wa_url(datos.mensaje(servicio)))}" target="_blank" rel="noopener">{WA_GLIFO}'
            f'Cotizar {item["cotizar"]}</a>')


def indice(items, tipo=None):
    """Filas tipo índice: foto, número, título con enlace (toda la fila lo abre), qué incluye, "desde" con la marca
    amarilla y flecha. Las filas con servicio y cotizar (la home, con su tipo) llevan además su enlace de WhatsApp bajo
    el precio."""
    filas = "".join(
        f'<li><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" loading="lazy" decoding="async">'
        f'<span class="vt-indice__n" aria-hidden="true">{n:02d}</span>'
        f'<h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p>'
        f'<p class="vt-indice__desde">desde <span class="vt-precio-marca">{i["desde"]}</span> {i["unidad"]}'
        f'{_cotizar_servicio(i, tipo) if tipo and i.get("servicio") else ""}</p>'
        + (f'<p class="vt-indice__cond">{esc(i["cond"])}</p>' if i.get("cond") else "")
        + '<span class="vt-indice__ir" aria-hidden="true">→</span></li>'
        for n, i in enumerate(items, 1))
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
    """Tabla de comparación: la primera columna es el encabezado de cada fila. En celular cada fila es una tarjeta y
    cada celda lleva el nombre de su columna (data-col); desde 768 px es tabla."""
    cabeza = "".join(f'<th scope="col">{unidades(c)}</th>' for c in columnas)
    celda = '<td data-col="{}">{}</td>'.format
    cuerpo = "".join(f'<tr><th scope="row">{f[0]}</th>'
                     f'{"".join(celda(esc(mayusculas_sin_unidades(texto_plano(c))), v) for c, v in zip(columnas[1:], f[1:]))}'
                     '</tr>' for f in filas)
    return (f'<table class="vt-tabla vt-tabla--comparar"><caption>{caption}</caption><thead><tr>{cabeza}</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table>')


def plegable(titulo, contenido):
    """Contenido cerrado en celular para acortar la página; terra.js lo abre desde 768 px (data-vt-plegable). El
    título queda a la vista como <h3> dentro del <summary>."""
    return (f'<details class="vt-plegable vt-mt" data-vt-plegable><summary class="vt-plegable__resumen">'
            f'<h3>{titulo}</h3></summary>{contenido}</details>')


def tabla_especies(filas, caption, grupo):
    """Especies con su precio: el nombre científico en cursiva bajo el común (sin columna propia). filas: nombre,
    cientifico, precio (texto) y cotiza (True si va "según cotización"). En celular las que se cotizan se juntan en un
    solo renglón (grupo: nombre y precio) para no apilar una tarjeta por especie; desde 768 px la tabla va completa.
    Cada vista oculta la otra con display:none, así el lector de pantalla lee lo mismo que se ve."""
    def fila(clase, nombre, detalle, precio):
        atributo = f' class="{clase}"' if clase else ""
        return (f'<tr{atributo}><th scope="row"><b>{nombre}</b><span>{detalle}</span></th>'
                f'<td class="vt-tabla__p">{precio}</td></tr>')
    cuerpo = "".join(fila("vt-tabla__cotiza" if cotiza else "", nombre, f"<i>{cientifico}</i>", precio)
                     for nombre, cientifico, precio, cotiza in filas)
    cuerpo += fila("vt-tabla__grupo", *grupo)
    return (f'<table class="vt-tabla vt-tabla--especies"><caption>{caption}</caption><thead><tr><th scope="col">Especie'
            '</th><th scope="col" class="vt-tabla__p">Precio</th></tr></thead>'
            f'<tbody>{cuerpo}</tbody></table>')


def linea_mensualidad(contado):
    """Plazo más largo disponible para un precio de contado, con la fórmula oficial (tools/pasto/mensualidades.py, la
    misma de vt-mensualidades.js): "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)"."""
    disponibles = [p for p in mensualidades.planes(contado) if p["disponible"]]
    if not disponibles:
        raise ValueError(f"{dinero(contado)}: no hay plazos de mensualidades para ese monto")
    p = disponibles[-1]
    return (f'o en {p["plazo"]} mensualidades de ≈ {dinero(p["mensualidad"])} con tarjeta de crédito '
            f'(total {dinero(p["total"])})')


def _precio_opcion(o):
    """Renglón de precio de una opción: "desde $X unidad" (o sin "desde"), un texto propio o nada."""
    if "precio" in o:
        desde = "desde " if o.get("desde", True) else ""
        mes = f'<small class="vt-modo__mes">{linea_mensualidad(o["precio"])}</small>' if o.get("mensualidad") else ""
        return (f'<p class="vt-modo__precio">{desde}<span class="vt-precio-marca">{dinero_exacto(o["precio"])}</span> '
                f'{o["unidad"]} <small>{o["detalle"]}</small>{mes}</p>')
    if "precio_texto" in o:
        detalle = f' <small>{o["detalle"]}</small>' if o.get("detalle") else ""
        return f'<p class="vt-modo__precio">{o["precio_texto"]}{detalle}</p>'
    return ""


def opciones(items, tipo, fila=False):
    """Formas de contratar o planes (máx. 3, spec §3.3), cada uno con su propio mensaje de WhatsApp (data-cta
    <tipo>:opcion-<n>). items: rotulo, titulo, puntos, mensaje y, opcionales, precio (número) con unidad y detalle,
    desde (False para un precio cerrado), mensualidad (True: línea con el plazo más largo), precio_texto (en vez de
    precio: "Por cotización"), nota, rec (recomendado) y cta (texto del botón: dice qué se pide; dos opciones no
    pueden decir lo mismo, Entrega B de experiencia)."""
    if len(items) > 3:
        raise ValueError("máximo 3 opciones por página (spec §3.3)")
    filas = []
    for i, o in enumerate(items, 1):
        clase = "vt-modo vt-modo--rec" if o.get("rec") else "vt-modo"
        puntos = "".join(f"<li><span>{x}</span></li>" for x in o["puntos"])  # una celda del grid de .vt-checks
        nota_html = f'<p class="vt-promesa">{o["nota"]}</p>' if o.get("nota") else ""
        filas.append(f'<li class="{clase}"><p class="vt-modo__n">{o["rotulo"]}</p><h3>{o["titulo"]}</h3>'
                     f'{_precio_opcion(o)}<ul class="vt-checks">{puntos}</ul>{nota_html}'
                     f'{boton_wa(o["mensaje"], f"{tipo}:opcion-{i}", o.get("cta", CTA_WA))}</li>')
    textos = [o.get("cta", CTA_WA) for o in items]
    if len(items) > 1 and len(set(textos)) != len(textos):
        raise ValueError(f"opciones contiguas con el mismo texto de botón: {textos} (cada una dice qué se pide)")
    # fila=True (Entrega C de experiencia): en celular, las opciones van una junto a otra con desplazamiento horizontal.
    return f'<ul class="vt-modos{" vt-modos--fila" if fila else ""}">{"".join(filas)}</ul>'


def fichas(items):
    """Tarjetas de lo que incluye un servicio, sin precio ni botón. items: titulo, texto y, opcional, puntos."""
    filas = []
    for f in items:
        puntos = "".join(f"<li><span>{x}</span></li>" for x in f.get("puntos", ()))
        lista = f'<ul class="vt-checks">{puntos}</ul>' if puntos else ""
        filas.append(f'<li class="vt-modo"><h3>{f["titulo"]}</h3><p>{f["texto"]}</p>{lista}</li>')
    return f'<ul class="vt-modos vt-fichas">{"".join(filas)}</ul>'


def relacionados(items, fila=False):
    """Tarjetas del sistema: foto, título con enlace (toda la tarjeta lo abre) y texto. items: titulo, href, texto, img,
    ancho, alto. fila=True (servicios, Entrega C de experiencia): en celular, una junto a otra con desplazamiento
    horizontal."""
    filas = "".join(f'<li class="vt-tarjeta"><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" '
                    f'loading="lazy" decoding="async"><h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3>'
                    f'<p>{i["texto"]}</p></li>' for i in items)
    return f'<ul class="vt-relacionados{" vt-relacionados--fila" if fila else ""}">{filas}</ul>'


def cobertura(zonas, por_proyecto, sectores=()):
    """Zonas con página propia, las que se atienden por proyecto y, si los hay, los sectores (nombre, detalle)."""
    lista = "".join(f'<li><a href="{esc(href)}">{nombre}</a></li>' for nombre, href in zonas)
    html = (f'<h3>Jardinería por zona</h3><ul class="vt-zonas">{lista}</ul>'
            f'<p class="vt-promesa">También atendemos {por_proyecto}, por proyecto.</p>')
    if sectores:
        filas = "".join(f"<li><b>{n}</b><span>{d}</span></li>" for n, d in sectores)
        html += f'<h3 class="vt-mt">Sectores que atendemos</h3><ul class="vt-sectores">{filas}</ul>'
    return html


def guias(items, href_todas="/blog"):
    filas = "".join(f'<li><a href="{esc(href)}">{texto}</a></li>' for texto, href in items)
    return f'<ul class="vt-guias">{filas}<li><a href="{esc(href_todas)}">Ver todas las guías</a></li></ul>'


# ---------- proceso, garantía, FAQ y cierre ----------
QUIEN = {"nosotros": ("Nosotros", ""), "tu": ("Tú", " vt-quien--tu"), "juntos": ("Juntos", " vt-quien--juntos")}


def pasos(items):
    """Proceso con marcadores NOSOTROS / TÚ / JUNTOS. items: titulo, quien, cuando, texto. El marcador va fuera del
    <h3> (en la línea de cuándo), para que el encabezado sea solo el paso."""
    filas = "".join(
        f'<li><h3>{p["titulo"]}</h3><p class="vt-pasos__cuando"><span class="vt-quien{QUIEN[p["quien"]][1]}">'
        f'{QUIEN[p["quien"]][0]}</span> {p["cuando"]}</p><p>{p["texto"]}</p></li>' for p in items)
    return f'<ol class="vt-pasos">{filas}</ol>'


def howto(nombre, items):
    return {"@type": "HowTo", "name": nombre,
            "step": [{"@type": "HowToStep", "position": i, "name": texto_plano(n), "text": texto_plano(t)}
                     for i, (n, t) in enumerate(items, 1)]}


def garantia(g):
    """g: titulo, id_titulo, numero, rotulo, resumen, puntos (texto, si_aplica), pie y, opcionales, grande y unidad (la
    cifra de la garantía; riego no tiene un plazo y la omite), cta_html (fila de CTA bajo el pie) y banda (Entrega C de
    experiencia: la garantía real de datos.py como banda oscura a media página, en verde profundo como el cierre, con
    la cifra grande, sus condiciones enlazadas y un CTA)."""
    no_aplica = ' class="vt-checks__no"'
    cifra = f'<p class="vt-grande">{g["grande"]}<small> {g["unidad"]}</small></p>' if g.get("grande") else ""
    puntos = "".join(f'<li{"" if ok else no_aplica}><span>{t}</span></li>' for t, ok in g["puntos"])
    ident = esc(g["id_titulo"])
    if g.get("banda") and not g.get("cta_html"):
        raise ValueError("la banda de garantía lleva un CTA (cta_html)")
    clase = "vt-bloque vt-banda vt-bloque--clave" if g.get("banda") else "vt-bloque vt-bloque--tinte"
    return (f'<section class="{clase}" aria-labelledby="{ident}"><div class="vt-wrap vt-dos">'
            f'<div><p class="vt-bloque__no"><b>{g["numero"]:02d}</b>{g["rotulo"]}</p><h2 id="{ident}">'
            f'{g["titulo"]}</h2>{cifra}'
            f'<p class="vt-promesa">{g["resumen"]}</p></div><div><ul class="vt-checks">{puntos}</ul>'
            f'<p class="vt-promesa">{g["pie"]}</p>{g.get("cta_html", "")}</div></div></section>')


def faq(preguntas, abierta=True):
    """Preguntas en acordeón; la primera abierta salvo abierta=False (servicios, Entrega C de experiencia: su primera
    respuesta, la del precio, ya está en «En corto» y en la sección de precio)."""
    items = "".join(f'<details{" open" if i == 0 and abierta else ""}><summary>{q}</summary><p>{a}</p></details>'
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


def cierre(titulo, lede, mensaje, tipo, texto=CTA_WA):
    """CTA final en verde profundo, con el mensaje que se abre a la vista. texto: el del botón (dice qué se pide)."""
    return (f'<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
            f'<h2 id="vt-cierre-titulo">{titulo}</h2><p class="vt-lede">{lede}</p>{fila_cta(mensaje, tipo, "cierre", texto=texto)}</div>'
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
IVA_INSTALADO = "con IVA"        # solo junto al pasto instalado (el precio ya lo incluye)
SIN_IVA = "(no lleva IVA)"       # solo pasto y mayoreo: el pasto natural sin instalar no lleva IVA
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
    # iva: solo el pasto instalado lleva IVA; el renglón vivo de la home no dice "con IVA" en solo pasto ni en mayoreo.
    return {"m2": m2, "precio": precio, "desde": desde, "texto": texto, "rotulo": rotulo, "aviso": aviso,
            "total": redondear(m2 * precio), "iva": modo == "instalado"}


def textos_medidor(largo, ancho, r, colonia="", plazo=1):
    """Textos de la etiqueta y mensaje de WhatsApp para el resultado `r` de calculo_medidor. plazo: 1 (contado) o el
    número de mensualidades elegido; si ese plazo no aplica al total, se toma contado. El mensaje dice qué forma de pago
    le interesa al cliente."""
    medida = f"{largo:.2f} × {ancho:.2f} m = {formato_m2(r['m2'])} m²"
    desde = "desde " if r["desde"] else ""
    disponibles = mensualidades.plazos_disponibles(r["total"])
    plazo = plazo if plazo in disponibles else 1
    if plazo > 1:
        total = mensualidades.total_a_plazos(r["total"], plazo)
        detalle = f"{plazo} mensualidades de {dinero(total / plazo)} con tarjeta de crédito (total {dinero(total)})"
        plan, interes = f"{detalle}. Tu banco debe aceptar el plan.", detalle
    elif disponibles:
        ultimo = disponibles[-1]
        total = mensualidades.total_a_plazos(r["total"], ultimo)
        plan = (f"O {ultimo} mensualidades de {dinero(total / ultimo)} con tarjeta de crédito "
                f"(total {dinero(total)}).")
        interes = "contado"
    else:
        plan = f"Mensualidades con tarjeta de crédito en cotizaciones desde {dinero(mensualidades.minimo_de(3))}."
        interes = "contado"
    cierre_calc = "Al medir te damos el precio cerrado." if r["desde"] else "La entrega se cotiza según tu colonia."
    # Decisión del dueño (2026-11-10): el pasto sin instalar (solo pasto y mayoreo) no lleva IVA; "con IVA" solo
    # acompaña al instalado, en la etiqueta, el cálculo, el renglón vivo y el mensaje.
    iva = IVA_INSTALADO if r["iva"] else ""
    # Decisión del dueño (2026-11-10): el instalado considera el terreno listo; en ese modo el estimado lo dice y el
    # mensaje pregunta por el terreno (en solo pasto y mayoreo no aplica).
    terreno = datos.TERRENO_LISTO_MEDIDOR if r["iva"] else ""
    renglones = (f"Hola, quiero cotizar {r['texto']}.", f"Medidas: {medida}",
                 f"Estimado de la web: {desde}{dinero(r['total'])} {iva or SIN_IVA}", f"Me interesa: {interes}",
                 f"Colonia: {colonia or '___'}") + ((datos.TERRENO_LISTO_PREGUNTA,) if terreno else ()) + (
                     "Te mando foto del área.",)
    mensaje = "\n".join(renglones)
    return {"medida": medida, "monto": dinero(r["total"]), "terreno": terreno,
            "calc": f"{formato_m2(r['m2'])} m² × {desde}${r['precio']}/m²{', ' + iva if iva else ' ' + SIN_IVA}. {cierre_calc}",
            "plan": plan, "plazo": plazo, "mensaje": mensaje, "cta": CTA_MEDIDA, "iva": iva,
            "vivo": f"{formato_m2(r['m2'])} m² · {desde}{dinero(r['total'])}{' ' + iva if iva else ''}"}


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


def _opcion_plazo(prefijo, plazo):
    """Contado o N mensualidades. Sin medida, los plazos van deshabilitados con su monto mínimo de cotización."""
    if plazo == 1:
        return (f'<label><span>Contado</span><small data-vt-plazo="1">—</small><input type="radio" '
                f'name="{prefijo}-plazo" value="1" checked></label>')
    return (f'<label><span>{plazo} meses</span><small data-vt-plazo="{plazo}">desde '
            f'{dinero(mensualidades.minimo_de(plazo))}</small><input type="radio" name="{prefijo}-plazo" '
            f'value="{plazo}" disabled></label>')


VACIO_MEDIDOR = {"medida": "Escribe tus medidas", "monto": "—", "calc": "Escribe el largo y el ancho de tu patio."}


def medidor(prefijo, tipo, largo=8, ancho=6, modo="instalado", mensaje=None, boton_medida=False, garantia=False,
            resultado_vivo=False):
    """Medidor: largo × ancho → plano a escala → etiqueta con el estimado y la forma de pago → WhatsApp con la medida.
    Los campos empiezan vacíos (8 y 6 son solo el ejemplo del placeholder y del plano): mientras el visitante no
    escriba, la etiqueta no muestra un estimado ajeno y el botón manda el mensaje genérico de la página (data-mensaje,
    con firma). vt-medidor.js calcula con los data-* de cada opción: los precios no viven en el JS. data-hero-cta: la
    barra móvil se esconde mientras el Medidor está a la vista, para que su CTA no compita. Con boton_medida=True (la
    home) solo el botón esconde la barra. En todos, el texto del botón va en un <span> que vt-medidor.js cambia a
    CTA_MEDIDA cuando hay una medida válida, y la barra móvil y el encabezado toman ese enlace con el texto de
    data-vt-barra; con un lado inválido, el aviso ERROR_MEDIDOR sale bajo los campos. Con garantia=True, la garantía de
    arraigo va bajo el botón, con su enlace a condiciones (vt-medidor.js la esconde fuera del modo instalado). Con
    resultado_vivo=True, un renglón bajo Largo × Ancho repite el resultado (textos_medidor["vivo"])."""
    marca_caja, marca_boton = ("", " data-hero-cta") if boton_medida else (" data-hero-cta", "")
    marca_caja += f' data-vt-barra="{esc(CTA_MEDIDA_BARRA)}"'
    texto_boton = f'<span data-vt-o="cta-texto">{CTA_WA}</span>'
    pie = f'<p class="vt-medidor__garantia" data-vt-o="garantia">{garantia_pasto_corta()}</p>' if garantia else ""
    vivo = '<p class="vt-medidor__vivo" data-vt-o="vivo"></p>' if resultado_vivo else ""
    generico = datos.con_firma(mensaje or datos.MENSAJES["general"])
    mayoreo = datos.con_firma(datos.MENSAJES["empresas"])
    opciones = "".join(_opcion_medidor(prefijo, k, m, modo) for k, m in MODOS_MEDIDOR.items())
    plazos = "".join(_opcion_plazo(prefijo, p) for p in (1,) + tuple(mensualidades.PLAZOS))
    campo = ('<div class="vt-campo"><label for="{p}-{n}">{t}</label><div class="vt-control"><input id="{p}-{n}" '
             'data-vt-campo="{n}" inputmode="decimal" placeholder="{v}" autocomplete="off" aria-describedby="{p}-error">'
             '<span>m</span></div></div>')
    return (
        f'<div class="vt-medidor" data-vt-medidor{marca_caja} data-wa="{esc(datos.TELEFONO_WA)}" '
        f'data-mensaje="{esc(generico)}" data-mensaje-mayoreo="{esc(mayoreo)}">'
        f'<div class="vt-medidor__form" role="group" aria-label="Medidor de pasto">'
        f'<div class="vt-medidor__medidas">{campo.format(p=prefijo, n="largo", t="Largo", v=largo)}'
        f'<span class="vt-medidor__x" aria-hidden="true">×</span>{campo.format(p=prefijo, n="ancho", t="Ancho", v=ancho)}'
        f'</div><p class="vt-correo__error" id="{prefijo}-error" data-vt-o="error" hidden></p>{vivo}'
        f'<fieldset class="vt-opciones"><legend>¿Qué necesitas?</legend>{opciones}</fieldset>'
        f'<div class="vt-campo"><label for="{prefijo}-colonia">Colonia (opcional)</label><div class="vt-control">'
        f'<input type="text" id="{prefijo}-colonia" data-vt-campo="colonia" placeholder="Ej. Lomas de Rosales" '
        f'autocomplete="off"></div></div></div>'
        f'<figure class="vt-fig vt-medidor__plano">{svg_plano(largo, ancho, redondear(largo * ancho * 10) / 10)}'
        f'<figcaption><span><b>Vista en planta</b> · escala ajustada a tu medida</span><span>Cotas en metros</span>'
        f'</figcaption></figure>'
        f'<div class="vt-etiqueta-x"><div class="vt-etiqueta vt-medidor__res" role="status"><p class="vt-etiqueta__cod">'
        f'<span>Tu etiqueta</span><span>Estimado</span></p><p class="vt-etiqueta__nombre" data-vt-o="m2">'
        f'{VACIO_MEDIDOR["medida"]}</p><p class="vt-etiqueta__sci">Stenotaphrum secundatum</p>'
        f'<p class="vt-etiqueta__precio is-vacio"><small data-vt-o="rotulo">{MODOS_MEDIDOR[modo]["rotulo"]}</small>'
        f'<b data-vt-o="monto">{VACIO_MEDIDOR["monto"]}</b>'
        f'<span data-vt-o="iva">{IVA_INSTALADO if modo == "instalado" else ""}</span></p>'
        f'<p class="vt-medidor__terreno" data-vt-o="terreno"{"" if modo == "instalado" else " hidden"}>'
        f'{esc(datos.TERRENO_LISTO_MEDIDOR)} {tierra_negra_cruzada()}</p>'
        f'<p class="vt-medidor__calc" data-vt-o="calc">{VACIO_MEDIDOR["calc"]}</p>'
        f'<p class="vt-medidor__aviso" data-vt-o="aviso" hidden></p>'
        f'<fieldset class="vt-opciones vt-opciones--plazo"><legend>Forma de pago: contado o mensualidades con tarjeta de '
        f'crédito</legend>{plazos}</fieldset>'
        f'<p class="vt-medidor__plan" data-vt-o="plan"></p>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{tipo}:medidor" data-vt-o="cta"{marca_boton} '
        f'href="{esc(datos.wa_url(generico))}" target="_blank" rel="noopener">{WA_GLIFO}{texto_boton}'
        f'<span class="vt-flecha" aria-hidden="true">→</span></a>{pie}</div></div></div>')


# ---------- empresas: cotizador por volumen y armador de palmas (public/js/vt-b2b.js; casos en casos-b2b.json) ----------
M2_MAXIMO = 1_000_000  # más que esto no es una obra: el cotizador vuelve al mensaje de la página
ALTURA_MAXIMA = 40
CANTIDAD_MAXIMA = 100_000
FILAS_PALMAS = 3  # renglones al cargar; vt-b2b.js agrega hasta 8
MILES_RE = re.compile(r"^\d{1,3}(?:,\d{3})+(?:\.\d+)?$")
DECIMAL_RE = re.compile(r"^\d+(?:\.\d+)?$")
ALTURA_RE = re.compile(r"^\s*(\d+(?:[.,]\d+)?)")
CANTIDAD_RE = re.compile(r"^\s*(\d+)")
VACIO_VOLUMEN = {"medida": "Escribe los m² de tu obra", "monto": "—",
                 "calc": (f"Desde {MINIMO_MAYOREO} m², mayoreo desde ${P['pasto_mayoreo_m2']}/m²; con menos, "
                          f"${P['pasto_solo_m2']}/m² (solo pasto). No lleva IVA.")}
VACIO_PALMAS = "Elige especie y cantidad"
OTRA_ESPECIE = "Otra especie (la escribo en el chat)"


def _hueco(valor):
    return (valor or "").strip() or "___"


def leer_m2(texto):
    """m² escritos por el visitante (como leerM2 de vt-b2b.js): "1,200" y "1200" son 1200, "12,5" es 12.5 y "800 m²" es
    800. Devuelve 0 si no es un número mayor que 0 y hasta M2_MAXIMO."""
    t = re.sub(r"\s|m²|m2", "", str(texto or ""), flags=re.I)
    t = t.replace(",", "") if MILES_RE.match(t) else t.replace(",", ".", 1)
    if not DECIMAL_RE.match(t):
        return 0
    n = float(t)
    return n if 0 < n <= M2_MAXIMO else 0


def calculo_volumen(m2):
    """La regla del Medidor para el pasto de obra: mayoreo desde el mínimo y, con menos, solo pasto con su aviso."""
    return calculo_medidor(m2, 1, "mayoreo")


def textos_volumen(r, empresa="", obra="", fecha=""):
    """Etiqueta y mensaje de compras para el resultado `r` de calculo_volumen."""
    desde = "desde " if r["desde"] else ""
    m2 = formato_m2(r["m2"])
    mensaje = "\n".join((f"Hola, quiero cotizar {r['texto']} para un proyecto.", f"m² totales: {m2} m²",
                         f"Estimado de la web: {desde}{dinero(r['total'])} ({desde}${r['precio']}/m²; no lleva IVA)",
                         f"Empresa: {_hueco(empresa)}", f"Obra y ubicación: {_hueco(obra)}",
                         f"Fecha de la primera entrega: {_hueco(fecha)}"))
    return {"medida": f"{m2} m²", "monto": dinero(r["total"]),
            "calc": (f"{m2} m² × {desde}${r['precio']}/m² {SIN_IVA}. Solo pasto: la entrega por etapas y la instalación "
                     "se cotizan con tu obra."),
            "mensaje": mensaje}


def leer_altura(texto):
    m = ALTURA_RE.match(str(texto or ""))
    n = redondear(float(m.group(1).replace(",", ".")) * 10) / 10 if m else 0
    return n if 0 < n <= ALTURA_MAXIMA else 0


def leer_cantidad(texto):
    m = CANTIDAD_RE.match(str(texto or ""))
    n = int(m.group(1)) if m else 0
    return n if 0 < n <= CANTIDAD_MAXIMA else 0


def linea_palma(especie, altura="", cantidad=""):
    """Renglón del mensaje: "- 40 × Palma real, altura aprox.: 3 m"; sin especie no hay renglón."""
    especie = (especie or "").strip()
    if not especie:
        return ""
    n, alto = leer_cantidad(cantidad), leer_altura(altura)
    return f"- {n or '___'} × {especie}, altura aprox.: {f'{formato_m2(alto)} m' if alto else '___'}"


def mensaje_palmas(filas, empresa="", obra="", fecha=""):
    """Un solo mensaje con toda la lista. filas: (especie, altura, cantidad) como los escribió el visitante. Sin
    renglones devuelve "" (el botón se queda con el mensaje de la página)."""
    lineas = [x for x in (linea_palma(*f) for f in filas) if x]
    if not lineas:
        return ""
    return "\n".join(("Hola, quiero cotizar palmas para un proyecto.", *lineas, f"Empresa: {_hueco(empresa)}",
                      f"Obra y ubicación: {_hueco(obra)}", f"Fecha de entrega: {_hueco(fecha)}"))


def resumen_palmas(filas):
    """Lo que dice la etiqueta: "2 especies · 60 piezas" (o "cantidad por definir")."""
    con_especie = [f for f in filas if (f[0] or "").strip()]
    if not con_especie:
        return VACIO_PALMAS
    n = len(con_especie)
    piezas = sum(leer_cantidad(f[2]) for f in con_especie)
    especies = f"{n} {'especie' if n == 1 else 'especies'}"
    return f"{especies} · {piezas:,} piezas" if piezas else f"{especies} · cantidad por definir"


def _campo(ident, campo, etiqueta, placeholder, unidad="", modo=None, error=None):
    """Campo con su label visible; modo="decimal" o "numeric" pone el teclado numérico. error: id del aviso que lo
    describe (aria-describedby)."""
    teclado = f' inputmode="{modo}"' if modo else ' type="text"'
    sufijo = f"<span>{unidad}</span>" if unidad else ""
    describe = f' aria-describedby="{esc(error)}"' if error else ""
    return (f'<div class="vt-campo"><label for="{esc(ident)}">{etiqueta}</label><div class="vt-control"><input '
            f'id="{esc(ident)}" data-vt-campo="{esc(campo)}"{teclado} placeholder="{esc(placeholder)}" '
            f'autocomplete="off"{describe}>{sufijo}</div></div>')


def _datos_obra(prefijo):
    return (_campo(f"{prefijo}-empresa", "empresa", "Empresa (opcional)", "Ej. tu razón social")
            + _campo(f"{prefijo}-obra", "obra", "Obra y ubicación (opcional)", "Ej. fraccionamiento en Altamira")
            + _campo(f"{prefijo}-fecha", "fecha", "Fecha aprox. de entrega (opcional)", "Ej. marzo"))


def _boton_cta(tipo, seccion, mensaje):
    """Botón de los cotizadores de empresas: su texto va en un <span> que vt-b2b.js cambia con un resultado válido."""
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:{seccion}" data-vt-o="cta" '
            f'href="{esc(datos.wa_url(mensaje))}" target="_blank" rel="noopener">{WA_GLIFO}'
            f'<span data-vt-o="cta-texto">{CTA_WA}</span><span class="vt-flecha" aria-hidden="true">→</span></a>')


# Con resultado válido, los cotizadores de empresas prestan su enlace a la barra fija y al encabezado (Entrega B de
# experiencia): botón y barra dicen qué se manda. Los mismos textos viven en public/js/vt-b2b.js.
CTA_VOLUMEN = ("Enviar mi cálculo por WhatsApp", "Enviar mi cálculo")
CTA_PALMAS = ("Cotizar mis palmas por WhatsApp", "Cotizar mis palmas")


def cotizador_volumen(prefijo, tipo, mensaje):
    """Pasto para obra: m² totales → precio por volumen (la regla del Medidor: mayoreo desde el mínimo; con menos, solo
    pasto y el aviso) → etiqueta → WhatsApp con m², estimado, empresa, obra y fecha. Los precios viajan en data-modos
    (de MODOS_MEDIDOR, es decir de datos.py) y vt-b2b.js calcula con VTMedidor.calcular de vt-medidor.js."""
    generico = datos.con_firma(mensaje)
    modos = {k: {kk: v for kk, v in MODOS_MEDIDOR[k].items() if kk != "opcion"} for k in ("mayoreo", "solo")}
    return (
        f'<div class="vt-b2b" data-vt-volumen data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
        f'data-vt-cta="{esc(CTA_VOLUMEN[0])}" data-vt-barra="{esc(CTA_VOLUMEN[1])}" '
        f'data-mensaje="{esc(generico)}" data-modos="{esc(json.dumps(modos, ensure_ascii=False, separators=(",", ":")))}">'
        '<div class="vt-b2b__form" role="group" aria-label="Cotizador de pasto por volumen">'
        f'{_campo(f"{prefijo}-m2", "m2", "m² totales de la obra", "Ej. 1,200", "m²", "decimal")}{_datos_obra(prefijo)}'
        '</div><div class="vt-etiqueta-x"><div class="vt-etiqueta vt-medidor__res" role="status">'
        '<p class="vt-etiqueta__cod"><span>Tu etiqueta</span><span>Estimado</span></p>'
        f'<p class="vt-etiqueta__nombre" data-vt-o="m2">{VACIO_VOLUMEN["medida"]}</p>'
        '<p class="vt-etiqueta__sci">Stenotaphrum secundatum</p>'
        f'<p class="vt-etiqueta__precio is-vacio"><small data-vt-o="rotulo">{MODOS_MEDIDOR["mayoreo"]["rotulo"]}</small>'
        f'<b data-vt-o="monto">{VACIO_VOLUMEN["monto"]}</b></p>'
        f'<p class="vt-medidor__calc" data-vt-o="calc">{VACIO_VOLUMEN["calc"]}</p>'
        '<p class="vt-medidor__aviso" data-vt-o="aviso" hidden></p>'
        f'{_boton_cta(tipo, "cotizador", generico)}</div></div></div>')


def _fila_palma(prefijo, n, especies):
    opciones = "".join(f'<option value="{esc(nombre)}">{nombre} ({cientifico})</option>'
                       for nombre, cientifico, _precio in especies)
    return (f'<li class="vt-b2b__fila" data-vt-fila><div class="vt-campo"><label for="{prefijo}-especie-{n}">Especie'
            f'</label><div class="vt-control"><select id="{prefijo}-especie-{n}" data-vt-campo="especie">'
            f'<option value="">Elige una especie</option>{opciones}<option value="Otra especie">{OTRA_ESPECIE}</option>'
            f'</select></div></div>{_campo(f"{prefijo}-altura-{n}", "altura", "Altura aprox.", "Ej. 3", "m", "decimal")}'
            f'{_campo(f"{prefijo}-cantidad-{n}", "cantidad", "Cantidad", "Ej. 20", "pzas", "numeric")}</li>')


def armador_palmas(prefijo, tipo, mensaje, especies=datos.PALMAS_PROYECTO):
    """Palmas para obra: especie, altura y cantidad por renglón → un solo WhatsApp con la lista, empresa, obra y fecha.
    Sin precio total: depende de la altura de cada ejemplar y se da por escrito en la cotización."""
    generico = datos.con_firma(mensaje)
    filas = "".join(_fila_palma(prefijo, n, especies) for n in range(1, FILAS_PALMAS + 1))
    return (
        f'<div class="vt-b2b" data-vt-palmas data-hero-cta data-wa="{esc(datos.TELEFONO_WA)}" '
        f'data-vt-cta="{esc(CTA_PALMAS[0])}" data-vt-barra="{esc(CTA_PALMAS[1])}" '
        f'data-mensaje="{esc(generico)}">'
        '<div class="vt-b2b__form" role="group" aria-label="Lista de palmas para cotizar">'
        f'<ol class="vt-b2b__filas" data-vt-filas>{filas}</ol>'
        '<button type="button" class="vt-btn vt-btn--linea" data-vt-agregar hidden>Agregar otra especie</button>'
        f'{_datos_obra(prefijo)}</div><div class="vt-etiqueta-x"><div class="vt-etiqueta" role="status">'
        '<p class="vt-etiqueta__cod"><span>Tu lista</span><span>Para cotizar</span></p>'
        f'<p class="vt-etiqueta__nombre" data-vt-o="resumen">{VACIO_PALMAS}</p>'
        '<p class="vt-b2b__msg" data-vt-o="lista"></p>'
        '<p class="vt-medidor__calc">El precio depende de la especie, la altura y la cantidad: te lo damos por escrito '
        'en la cotización.</p>'
        f'{_boton_cta(tipo, "armador", generico)}</div></div></div>')


def repse():
    """REPSE verificable: el folio y el padrón público de la STPS donde se consulta."""
    return (f'<p class="vt-promesa">REPSE {datos.REPSE} · <a href="{esc(datos.REPSE_PADRON)}" target="_blank" '
            'rel="noopener">consulta el folio en el padrón público de la STPS</a></p>')


# ---------- empresas: cotización por correo para compras (respuesta del dueño, 2026-11-08) ----------
# El mismo endpoint de formsubmit que los materiales. vt-b2b.js valida en el navegador (mensajes junto a cada campo),
# manda generate_lead con method "formulario" y prellena m² o la lista desde el cotizador; sin JS, el navegador valida
# los required y el formulario se envía igual.
FORMULARIO_ACCION = f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"
FORMULARIO_GRACIAS = f"{datos.SITIO}/gracias"


def _campo_correo(prefijo, nombre, etiqueta, tipo="text", requerido=True, completar="off", placeholder="",
                  multilinea=False, ancho=False, modo=None):
    ident = f"{prefijo}-c-{nombre}"
    error = f"{ident}-error"
    texto = etiqueta if requerido else f"{etiqueta} (opcional)"
    comunes = (f'id="{esc(ident)}" name="{esc(nombre)}"' + ("" if multilinea else f' type="{tipo}"')
               + (" required" if requerido else "") + (f' inputmode="{modo}"' if modo else "")
               + f' autocomplete="{completar}" placeholder="{esc(placeholder)}" aria-describedby="{esc(error)}"')
    control = f"<textarea {comunes} rows=\"3\"></textarea>" if multilinea else f"<input {comunes}>"
    clase = "vt-campo vt-correo__ancho" if ancho or multilinea else "vt-campo"
    return (f'<div class="{clase}"><label for="{esc(ident)}">{texto}</label><div class="vt-control">{control}</div>'
            f'<p class="vt-correo__error" id="{esc(error)}" hidden></p></div>')


def formulario_correo(prefijo, f):
    """Cotización por correo para departamentos de compras. f: pagina (asunto), cta (cta_id de GA4), cantidad
    (etiqueta, ejemplo, multilínea y, opcional, inputmode) para m² o la lista de palmas, y aviso (privacidad, debajo del
    botón). El cotizador de la página prellena cantidad, empresa, proyecto y fecha."""
    etiqueta, ejemplo, multilinea, *modo = f["cantidad"]
    campos = (
        _campo_correo(prefijo, "empresa", "Empresa", completar="organization", placeholder="Razón social"),
        _campo_correo(prefijo, "nombre", "Nombre", completar="name", placeholder="Quién recibe la cotización"),
        _campo_correo(prefijo, "correo", "Correo", "email", completar="email", placeholder="compras@tuempresa.com"),
        _campo_correo(prefijo, "telefono", "Teléfono", "tel", False, "tel", "833 000 0000"),
        _campo_correo(prefijo, "proyecto", "Proyecto y ubicación", placeholder="Ej. fraccionamiento en Altamira",
                      ancho=True),
        _campo_correo(prefijo, "cantidad", etiqueta, placeholder=ejemplo, multilinea=multilinea, ancho=True,
                      modo=modo[0] if modo else None),
        _campo_correo(prefijo, "fecha", "Fecha estimada de entrega", requerido=False, placeholder="Ej. marzo"),
        _campo_correo(prefijo, "mensaje", "Mensaje", requerido=False, multilinea=True,
                      placeholder="Especificaciones, etapas de la obra o datos de facturación"),
    )
    return (
        f'<form class="vt-correo" action="{esc(FORMULARIO_ACCION)}" method="POST" data-vt-correo data-hero-cta '
        f'data-cta-form="{esc(f["cta"])}">'
        f'<input type="hidden" name="_subject" value="Cotización empresa · {esc(f["pagina"])}">'
        f'<input type="hidden" name="_next" value="{esc(FORMULARIO_GRACIAS)}">'
        '<input type="hidden" name="_captcha" value="false">'
        '<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
        f'<div class="vt-correo__campos">{"".join(campos)}</div>'
        '<div class="vt-correo__pie"><button type="submit" class="vt-btn vt-btn--tinta">Enviar solicitud por correo'
        '</button><p class="vt-correo__estado" role="status" data-vt-o="correo-estado"></p>'
        f'<p class="vt-correo__aviso">{f["aviso"]}</p></div></form>')


# ---------- portada: hero de marca (Entrega A de experiencia, 2026-11-10) ----------
# Un solo componente para todas las plantillas; la home es la referencia. CSS: .vt-portada* en public/css/terra.css.
SEP_CONFIANZA = '<span class="vt-portada__sep" aria-hidden="true"> · </span>'
H1_LARGO = 40  # con más caracteres (sin contar el lema), el titular usa la escala larga (--vt-text-h1-larga)
SERIF_RE = re.compile(r'<span class="vt-serif">.*?</span>', re.S)


def titular_largo(h1):
    """True si el titular, sin su lema en serif, pasa de H1_LARGO caracteres."""
    return len(texto_plano(SERIF_RE.sub("", h1))) > H1_LARGO


def clase_titular(h1, extra=""):
    """Clases de una cabecera que no es portada (artículo, blog, catálogo, ficha) para usar la misma escala de titular."""
    return " ".join(x for x in (extra, "vt-titular", "vt-titular--larga" if titular_largo(h1) else "") if x)


def enlace_tel(cta):
    """El teléfono como enlace de texto (en la portada dejó de ser botón)."""
    return f'<a data-cta="{esc(cta)}" href="tel:{datos.TELEFONO_TEL}">Llamar {datos.TELEFONO_VISIBLE}</a>'


def enlace_wa(mensaje, cta, texto=CTA_WA):
    """WhatsApp como enlace de texto (cabeceras de lectura: artículo e índice del blog), con el mensaje ya firmado."""
    return (texto, datos.wa_url(datos.con_firma(mensaje)), cta, 'target="_blank" rel="noopener"')


def wa_texto(mensaje, cta, texto):
    """WhatsApp como enlace de texto en medio de una lectura (blog, Entrega C de experiencia): el glifo, el texto y la
    flecha, sin botón."""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-wa-texto" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">{WA_GLIFO}'
            f'{texto}<span class="vt-flecha" aria-hidden="true">→</span></a>')


def enlace_portada(enlace, tipo):
    """Enlace de texto de la portada con su flecha. enlace: (texto, href) o (texto, href, data-cta, atributos extra)."""
    texto, href, *resto = enlace
    cta = resto[0] if resto and resto[0] else f"{tipo}:hero"
    extra = f" {resto[1]}" if len(resto) > 1 and resto[1] else ""
    return f'<a data-cta="{esc(cta)}" href="{esc(href)}"{extra}>{texto} <span aria-hidden="true">→</span></a>'


def enlaces_portada(enlaces, tipo, telefono=True):
    """Fila de enlaces de texto bajo el botón: los propios de la página y, al final, el teléfono."""
    partes = [enlace_portada(e, tipo) for e in enlaces] + ([enlace_tel(f"{tipo}:hero")] if telefono else [])
    return f'<p class="vt-portada__enlaces">{"".join(partes)}</p>' if partes else ""


def confianza(dato=""):
    """Línea de confianza: la promesa única (con "Abierto ahora" en horario), la calificación de Google y, si la hay,
    un dato real propio de la página (HTML corto)."""
    nota, _, resenas = datos.GOOGLE.partition(" ")
    partes = [promesa_horario(), f"<span><b>{esc(nota)}</b> {esc(resenas)}</span>"] + ([f"<span>{dato}</span>"] if dato else [])
    return f'<p class="vt-portada__confianza">{SEP_CONFIANZA.join(partes)}</p>'


def estilo_foto(p):
    """Encuadre de la foto de portada (object-position): pos en celular y pos_d en escritorio, si difiere."""
    variables = [f"{nombre}:{p[clave]}" for nombre, clave in (("--vt-fp", "pos"), ("--vt-fpd", "pos_d")) if p.get(clave)]
    return f' style="{esc(";".join(variables))}"' if variables else ""


def clase_portada(p, pliegue=True, extra=""):
    """Clases de la sección: escala larga según el titular, sin foto, y --pliegue (en celular la foto va entre el
    titular y la etiqueta y todo llena la primera pantalla) cuando hay foto."""
    clases = ["vt-portada"] + ([extra] if extra else [])
    if titular_largo(p["h1"]):
        clases.append("vt-portada--larga")
    if not (p.get("etiqueta") or p.get("etiqueta_html")):
        clases.append("vt-portada--sinprecio")
    if not p.get("foto"):
        clases.append("vt-portada--sinfoto")
    elif pliegue:
        clases.append("vt-portada--pliegue")
    return " ".join(clases)


def portada(p, tipo, migas_items=None, pliegue=True, datos_html=None, clase=""):
    """Hero de marca. p: kicker, h1, lede y mensaje; opcionales lema (frase en serif bajo el titular, si el <h1> no la
    trae ya en un <span class="vt-serif">), etiqueta (precio colgado; o etiqueta_html si la página arma la suya), foto con pos y pos_d (object-position), cta (HTML
    del botón principal si no es el WhatsApp de siempre), enlaces (enlace_portada), telefono (False lo quita), dato
    (dato propio para la línea de confianza), medio (HTML entre el lede y la foto: controles propios de la página) y
    respuesta (el lede es la respuesta directa, speakable). pliegue=False solo en la home: en celular la foto va al
    final. Un solo botón relleno; terra.js esconde la barra móvil mientras se ve (data-hero-cta)."""
    ruta = migas(migas_items) if migas_items else ""
    # respuesta=True: la entrada ya es la respuesta directa de la página (precio, unidad y zona) y se marca para speakable.
    marca = f" {entidad.ATRIBUTO_RESPUESTA}" if p.get("respuesta") else ""
    lema = f'<p class="vt-portada__lema vt-serif">{p["lema"]}</p>' if p.get("lema") else ""
    foto = f'<div class="vt-portada__foto"{estilo_foto(p)}>{figura(p["foto"], principal=True)}</div>' if p.get("foto") else ""
    precio = p.get("etiqueta_html") or (etiqueta(p["etiqueta"]) if p.get("etiqueta") else "")
    boton = p.get("cta") or boton_wa(p["mensaje"], f"{tipo}:hero")
    cuadro = cuadro_datos() if datos_html is None else datos_html
    return (
        f'<section class="{clase_portada(p, pliegue, clase)}" aria-labelledby="vt-h1"><div class="vt-wrap">'
        f'<div class="vt-portada__grid"><div class="vt-portada__pliegue">{ruta}'
        f'<div class="vt-portada__titulo"><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1>{lema}'
        f'<p class="vt-lede"{marca}>{p["lede"]}</p>{p.get("medio", "")}</div>{foto}{precio}</div>'
        f'<div class="vt-portada__trato"><div class="vt-portada__cta" data-hero-cta>{boton}</div>'
        f'{enlaces_portada(p.get("enlaces", ()), tipo, p.get("telefono", True))}{confianza(p.get("dato", ""))}</div>'
        f'</div>{cuadro}</div></section>')
