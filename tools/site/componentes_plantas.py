"""Componentes de las páginas de plantas (Etapa 2e): foto de especie con pie FIG., tarjeta de especie, índice
de subcategorías con "desde", filtro por necesidad, buscador y filtros del catálogo, rejilla con botón real y los
diálogos de "Arma tu lista". Funciones puras: los textos de contenido/ son HTML en línea de confianza; los atributos y
los datos de especies se escapan aquí. Precios solo de datos.PRECIOS_ESPECIE y datos.DESDE_PLANTAS. Va aparte de
componentes.py, que ya pasa de 800 renglones.

Fotos: el pie es "Fig. NN · <especie>"; solo las especies de catalogo_datos.FOTOS_VIVERO_CONFIRMADAS (las confirma el
dueño) dicen "En nuestro vivero" en el pie y en el alt. Las de catalogo_datos.FOTOS_RETIRADAS (hoy ninguna, por
decisión del dueño) llevarían un marcador "sin foto" del mismo 4:5: superficie verde clara con la reja del plano, la
inicial y la etiqueta "Foto pendiente"."""
import componentes as c
import datos
from contenido import catalogo_datos as cd
from partials import WA_GLIFO, esc

VIVERO = "En nuestro vivero"
OPCIONES = (
    ("cat", "Tipo", (("arboles", "Árboles"), ("palmas", "Palmas"), ("plantas", "Plantas"))),
    ("luz", "Luz", (("sol", "Sol"), ("media", "Media sombra"), ("sombra", "Sombra"))),
    ("tam", "Tamaño adulto", tuple((k, t) for k, t, _m in cd.TAMANOS)),
    ("riego", "Riego", (("poco", "Poco"), ("moderado", "Moderado"), ("abundante", "Abundante"))),
    ("uso", "Uso", (("banqueta", "Banqueta"), ("interior", "Interior"), ("salitre", "Aguanta salitre"))),
)
OTRO_TAMANO = "Otro tamaño o medida especial"


SIN_FOTO = (480, 600)  # 4:5, como .vt-esp__foto img en terra-plantas.css
# Reja del plano cada 40 px (un solo trazo: sin <pattern>, que pediría un id por tarjeta).
_REJA = "".join(f"M0 {y}H480" for y in range(40, 600, 40)) + "".join(f"M{x} 0V600" for x in range(40, 480, 40))


def alt_especie(e):
    vivero = " en el vivero de Viveros Terra" if cd.foto_del_vivero(e) else ""
    return f"{e['name']} ({e['sc']}){vivero}"


def pie_especie(e, numero):
    vivero = f" · {VIVERO}" if cd.foto_del_vivero(e) else ""
    return f"<figcaption><b>Fig. {numero:02d}</b> · {esc(e['name'])}{vivero}</figcaption>"


def sin_foto(e):
    """Marcador de una especie sin foto publicable: mismo tamaño que la foto, con su nombre para lectores de pantalla."""
    ancho, alto = SIN_FOTO
    inicial = esc(e["name"].strip()[:1].upper())
    return (f'<svg class="vt-esp__sinfoto" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" role="img" '
            f'aria-label="{esc(e["name"])}: sin foto por ahora"><path class="vt-sinfoto-reja" d="{_REJA}"/>'
            f'<text class="vt-sinfoto-letra" x="240" y="350" text-anchor="middle">{inicial}</text>'
            '<rect class="vt-sinfoto-tag" x="130" y="430" width="220" height="44" rx="4"/>'
            '<text class="vt-sinfoto-tagtexto" x="240" y="460" text-anchor="middle">Foto pendiente</text></svg>')


def foto_especie(e, numero, carga="lazy"):
    """carga: "alta" (la primera del catálogo), "eager" o "lazy". Sin foto publicable, el marcador de sin_foto()."""
    if not cd.tiene_foto(e):
        return f'<figure class="vt-esp__foto">{sin_foto(e)}{pie_especie(e, numero)}</figure>'
    loading = "lazy" if carga == "lazy" else "eager"
    prioridad = ' fetchpriority="high"' if carga == "alta" else ""
    return (f'<figure class="vt-esp__foto"><img src="{esc(e["img"])}" width="{e["ancho"]}" height="{e["alto"]}" '
            f'loading="{loading}"{prioridad} decoding="async" alt="{esc(alt_especie(e))}">'
            f'{pie_especie(e, numero)}</figure>')


def datos_especie(e, altura=None):
    filas = (("Luz", e["luz"]), ("Riego", e["agua"]), ("Altura", altura or e["altura"]))
    celdas = "".join(f"<div><dt>{t}</dt><dd>{esc(v)}</dd></div>" for t, v in filas)
    return f'<dl class="vt-esp__datos">{celdas}</dl>'


def precio_especie(e):
    precio = datos.PRECIOS_ESPECIE.get(e["name"])
    if precio is None:
        return ""
    chico = " · tamaño chico" if e["cat"] == "palmas" else ""
    return f'<p class="vt-esp__precio">desde <span class="vt-precio-marca">{c.dinero(precio)}</span>{chico}</p>'


def _cabeza(e, numero, carga="lazy"):
    return (f'{foto_especie(e, numero, carga)}<h3 class="vt-esp__nombre">{esc(e["name"])}</h3>'
            f'<p class="vt-esp__sci"><i>{esc(e["sc"])}</i></p>')


def tarjeta_especie(e, numero, texto, tipo, altura=None):
    """Subcategorías y hub: foto del vivero, nombre, científico, luz/riego/altura, precio solo si datos.py lo tiene,
    texto propio de la página, "Agregar en Arma tu lista" (al catálogo con la especie buscada; terra.js lo mide como
    select_content) y la guía del blog si existe."""
    nombre = esc(e["name"])
    guia = cd.BLOG_ESPECIE.get(e["slug"])
    guia_html = (f'<a href="{esc(guia)}">Guía de cuidados<span class="vt-sr"> de {nombre}</span></a>' if guia else "")
    return (f'<li class="vt-esp">{_cabeza(e, numero)}{datos_especie(e, altura)}{precio_especie(e)}<p>{texto}</p>'
            f'<p class="vt-esp__acciones"><a data-cta="{esc(tipo)}:catalogo" href="{esc(cd.url_catalogo(q=e["name"], agregar=e["slug"]))}">'
            # Un solo <span>: el enlace es inline-flex y cada trozo de texto suelto sería otra columna a 375 px.
            f'<span>Agregar<span class="vt-sr"> {nombre}</span> en Arma tu lista</span></a>{guia_html}</p></li>')


def especies(items, tipo, primero=1):
    """items: (slug, texto, altura propia de la página o None). primero: número de la primera figura (2 si la portada
    ya lleva la Fig. 01)."""
    filas = "".join(tarjeta_especie(cd.especie(s), n, t, tipo, a) for n, (s, t, a) in enumerate(items, primero))
    return f'<ul class="vt-esps">{filas}</ul>'


def indice_subcategorias(items):
    """Hub: foto, título con enlace (toda la fila lo abre, .vt-indice de terra.css), texto y "desde" de
    datos.DESDE_PLANTAS, o "Precio según cotización" si no hay un precio oficial."""
    filas = []
    for n, i in enumerate(items, 1):
        desde = datos.DESDE_PLANTAS[i["href"]]
        precio = (f'desde <span class="vt-precio-marca">{c.dinero(desde)}</span> {i["unidad"]}'.rstrip()
                  if desde is not None else f"Precio {datos.SEGUN_COTIZACION.lower()}")
        filas.append(f'<li><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" loading="lazy" '
                     f'decoding="async"><span class="vt-indice__n" aria-hidden="true">{n:02d}</span>'
                     f'<h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p>'
                     f'<p class="vt-indice__desde">{precio}</p><span class="vt-indice__ir" aria-hidden="true">→</span></li>')
    return f'<ol class="vt-indice">{"".join(filas)}</ol>'


def necesidades(items, tipo):
    """items: (clave, titulo, texto, filtro). Enlaces al catálogo con el filtro puesto y el conteo real del build."""
    filas = "".join(
        f'<li><a data-cta="{esc(tipo)}:necesidad-{esc(clave)}" href="{esc(cd.url_catalogo(filtro))}"><h3>{titulo}</h3>'
        f'<span>{texto}</span><span class="vt-necesidad__n">{cd.cuenta(filtro)} especies</span></a></li>'
        for clave, titulo, texto, filtro in items)
    return f'<ul class="vt-necesidades">{filas}</ul>'


def filtros_catalogo(total):
    grupos = "".join(
        f'<fieldset class="vt-filtro"><legend>{leyenda}</legend>' + "".join(
            f'<button type="button" class="vt-chip-p" data-vt-g="{g}" data-vt-v="{v}" aria-pressed="false">{t}</button>'
            for v, t in opciones) + "</fieldset>"
        for g, leyenda, opciones in OPCIONES)
    # Sin action: test_reglas solo admite formularios a formsubmit. Sin JS, Enter recarga la misma página con ?q=.
    return ('<form class="vt-buscador" role="search" aria-label="Buscar y filtrar plantas" data-vt-filtros>'
            '<div class="vt-campo"><label for="vt-cat-q">Busca por nombre, uso o luz</label>'
            '<div class="vt-control"><input id="vt-cat-q" type="search" name="q" autocomplete="off" '
            'placeholder="Ej. palma, banqueta, sombra"></div></div>'
            '<details class="vt-buscador__filtros" data-vt-plegable><summary><span>Filtros<span data-vt-o="n-filtros">'
            '</span></span></summary>'
            f'<div class="vt-buscador__grupos">{grupos}</div></details>'
            f'<p class="vt-buscador__n"><span data-vt-o="cuenta" aria-live="polite">{total} especies</span>'
            '<button type="button" class="vt-buscador__limpiar" data-vt-limpiar hidden>Quitar filtros</button></p></form>')


def tarjeta_catalogo(e, numero, carga="lazy"):
    f = cd.filtros(e)
    atributos = " ".join(f'data-{g}="{esc(" ".join(f[g]))}"' for g in cd.GRUPOS)
    buscar = cd.normalizar(" ".join((e["name"], e["sc"], e["tipo"], e["luz"])))
    nombre = esc(e["name"])
    guia = cd.BLOG_ESPECIE.get(e["slug"])
    guia_html = f'<p><a href="{esc(guia)}">Guía de cuidados<span class="vt-sr"> de {nombre}</span></a></p>' if guia else ""
    ficha = (f'<details class="vt-esp__ficha"><summary>Ficha<span class="vt-sr"> de {nombre}</span></summary>'
             f'<p>{esc(e["desc"])}</p><p><b>Tamaños:</b> {esc(", ".join(e["sz"]))}. Otras medidas: pregúntanos.</p>'
             f'{guia_html}</details>')
    # id = slug: el ListItem del JSON-LD apunta a /catalogo#<slug> (plantillas/catalogo.py).
    return (f'<li class="vt-esp vt-cat" id="{esc(e["slug"])}" data-vt-esp="{esc(e["slug"])}" {atributos} data-buscar="{esc(buscar)}">'
            f'{_cabeza(e, numero, carga)}{datos_especie(e)}{precio_especie(e)}{ficha}'
            f'<button type="button" class="vt-btn vt-btn--linea vt-cat__add" data-vt-agregar="{esc(e["slug"])}">'
            # Un solo <span>: .vt-btn es inline-flex con gap y, con el vt-sr como hijo directo, se verían dos espacios.
            f'<span>+ Añadir<span class="vt-sr"> {nombre}</span> a mi lista</span></button></li>')


PRIMERAS = 4  # fotos que cargan de inmediato (la primera con prioridad alta: el LCP del catálogo)


def _cargas(lista):
    """Carga de cada tarjeta, contando solo las que tienen foto: un marcador sin foto no gasta la prioridad del LCP."""
    salida, vistas = [], 0
    for e in lista:
        if cd.tiene_foto(e):
            vistas += 1
        salida.append("lazy" if not cd.tiene_foto(e) or vistas > PRIMERAS else "alta" if vistas == 1 else "eager")
    return salida


def rejilla_catalogo(especies_=None, tipo="catalogo"):
    """Rejilla y estado sin resultados: un WhatsApp con mensaje_especial(<lo buscado>), que vt-catalogo.js rellena."""
    lista = especies_ or cd.ORDENADAS
    tarjetas = "".join(tarjeta_catalogo(e, n, carga) for n, (e, carga) in enumerate(zip(lista, _cargas(lista)), 1))
    return (f'<ul class="vt-esps vt-esps--cat" data-vt-rejilla aria-label="Especies del catálogo">'
            f'{tarjetas}</ul>'
            '<div class="vt-cat__vacio" data-vt-vacio hidden><p>No hay especies con esos filtros. Quita alguno o '
            'pregúntanos por la que buscas:</p>'
            f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:solEsp-vacio" data-vt-o="vacio-wa" '
            f'href="{esc(datos.wa_url(mensaje_especial("")))}" target="_blank" rel="noopener">{WA_GLIFO}'
            'Preguntar por WhatsApp</a></div>')


def lista_catalogo(tipo):
    """Diálogo para añadir (tamaño o medida especial y piezas), diálogo de la lista con un solo enlace de WhatsApp
    (data-cta <tipo>:sendWA; vt-catalogo.js le pone el mensaje) y la barra "Mi lista"."""
    return (
        '<dialog class="vt-dialogo" id="vt-agregar" aria-labelledby="vt-agregar-t"><form method="dialog">'
        '<h2 id="vt-agregar-t" data-vt-o="nombre">Añadir a mi lista</h2>'
        '<p class="vt-esp__sci"><i data-vt-o="sci"></i></p>'
        '<div class="vt-campo"><label for="vt-agregar-tam">Tamaño</label><div class="vt-control">'
        '<select id="vt-agregar-tam" data-vt-campo="tam"></select></div></div>'
        f'<div class="vt-campo" data-vt-otro hidden><label for="vt-agregar-otro">{OTRO_TAMANO}</label>'
        '<div class="vt-control"><input id="vt-agregar-otro" type="text" maxlength="60" data-vt-campo="otro" placeholder="Ej. 3.5 m">'
        '</div></div><div class="vt-campo"><label for="vt-agregar-n">Cantidad (piezas)</label>'
        '<div class="vt-cantidad"><button type="button" data-vt-menos aria-label="Una pieza menos">−</button>'
        '<input id="vt-agregar-n" type="number" inputmode="numeric" min="1" max="9999" value="1" data-vt-campo="n">'
        '<button type="button" data-vt-mas aria-label="Una pieza más">+</button></div></div>'
        # Un solo submit: Enter en cantidad o medida usa el primer submit del formulario y debe agregar, no cancelar.
        '<p class="vt-dialogo__botones"><button type="button" class="vt-btn vt-btn--linea" data-vt-cancelar>Cancelar'
        '</button><button type="submit" value="agregar" class="vt-btn vt-btn--tinta">Agregar a mi lista</button></p>'
        '</form></dialog>'
        '<dialog class="vt-dialogo" id="vt-lista" aria-labelledby="vt-lista-t"><div class="vt-dialogo__cabeza">'
        '<h2 id="vt-lista-t">Mi lista para cotizar</h2><button type="button" class="vt-dialogo__x" data-vt-cerrar '
        'aria-label="Cerrar la lista"><span aria-hidden="true">×</span></button></div>'
        '<p class="vt-promesa" data-vt-o="resumen">Tu lista está vacía.</p><ul class="vt-lista" data-vt-o="items"></ul>'
        f'<a class="vt-btn vt-btn--wa vt-lista__enviar" data-cta="{esc(tipo)}:sendWA" data-vt-o="enviar" '
        f'href="{esc(datos.wa_url(""))}" target="_blank" rel="noopener" hidden>{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<p class="vt-dialogo__botones"><button type="button" class="vt-btn vt-btn--linea" data-vt-cerrar>Seguir viendo'
        '</button><button type="button" class="vt-lista__vaciar" data-vt-vaciar>Vaciar lista</button></p>'
        f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p></dialog>'
        '<div class="vt-lista-barra" data-vt-barra-lista hidden><button type="button" class="vt-btn vt-btn--tinta" '
        'data-vt-abrir-lista>Mi lista <b data-vt-o="cuenta-lista">0</b></button>'
        '<p class="vt-sr" role="status" data-vt-o="aviso"></p></div>')


def mensaje_especial(texto):
    """El mensaje de solEsp() de main; con el campo vacío lleva el hueco ___ (igual que mensajeEspecial() del JS)."""
    valor = (texto or "").strip() or "___"
    return f"Hola Viveros Terra\n\nBusco: *{valor}*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?"


def pedido_especial(tipo):
    return ('<div class="vt-especial" data-vt-especial><div class="vt-campo"><label for="vt-especial-q">Planta, árbol, '
            'tamaño o medida que buscas</label><div class="vt-control"><input id="vt-especial-q" type="text" '
            'autocomplete="off" maxlength="120" placeholder="Ej. palma phoenix de 4 m"></div></div>'
            f'<a class="vt-btn vt-btn--wa" data-cta="{esc(tipo)}:solEsp" href="{esc(datos.wa_url(mensaje_especial("")))}" '
            f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→'
            '</span></a></div>')
