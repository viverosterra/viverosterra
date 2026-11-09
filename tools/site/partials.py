"""Parciales del shell compartido: <head> esencial, menú, pie y barra fija móvil.

Cada función devuelve su región completa, con los marcadores <!-- vt:x --> y <!-- /vt:x -->, para que
tools/site/shell.py la reemplace en cualquier página. Todos los datos salen de datos.py.
"""
from html import escape

import datos

LOGO = "/img/logo-viveros-terra-tampico.svg"
P = datos.PRECIOS

MENU = (
    {"id": "pasto-natural", "texto": "Pasto natural", "href": "/pasto-en-rollo-tampico",
     "nota": f"desde ${P['pasto_solo_m2']}/m²",
     "items": (("Pasto en rollo", "/pasto-en-rollo-tampico"),
               (f"Mayoreo ({P['pasto_mayoreo_minimo_m2']} m² o más)", "/mayoreo-pasto-tampico"),
               ("Protocolo de riego", "/protocolo-cuidados-pasto-san-agustin"))},
    {"id": "pasto-sintetico", "texto": "Pasto sintético", "href": "/pasto-sintetico-tampico",
     "nota": f"desde ${P['sintetico_tienda_m2']}/m²",
     "items": (("Instalado en Tampico", "/pasto-sintetico-tampico"),
               ("Tienda con envío a todo México", "/pasto-sintetico"),
               ("Para perros", "/pasto-sintetico/perros"))},
    {"id": "jardin", "texto": "Jardín", "href": None,
     "nota": f"desde ${P['mantenimiento_mes']}/mes",
     "items": (("Diseño de jardines", "/diseno-jardines-tampico"),
               ("Mantenimiento", "/mantenimiento-jardines-tampico"),
               ("Riego automático", "/sistema-riego-tampico"))},
    {"id": "plantas", "texto": "Plantas y palmas", "href": "/plantas-palmas-arboles-tampico",
     "nota": f"{datos.VARIEDADES} variedades",
     "items": (("Todo el vivero", "/plantas-palmas-arboles-tampico"),
               ("Palmas", "/palmas-tropicales-tampico"),
               ("Plantas para jardín", "/plantas-para-jardin-tampico"),
               ("Árboles ornamentales", "/arboles-ornamentales-tampico"),
               ("Árboles para banqueta", "/arboles-para-banqueta-tampico"),
               ("Plantas de interior", "/plantas-de-interior-tampico"),
               ("Arma tu lista (catálogo)", "/catalogo"),
               ("Tierra negra", "/tierra-negra-vegetal-tampico"),
               ("Tezontle rojo", "/tezontle-rojo-tampico"),
               ("Mármol blanco", "/marmol-blanco-tampico"),
               ("Piedra bola de río", "/piedra-bola-rio-tampico"))},
    {"id": "empresas", "texto": "Empresas", "href": None,
     "nota": f"REPSE · {datos.FACTURA}",
     "items": (("Mayoreo de pasto", "/mayoreo-pasto-tampico"),
               ("Palmas para proyectos", "/palmas-mayoreo-proyectos"),
               ("Mantenimiento de áreas verdes", "/mantenimiento-jardines-tampico"))},
    {"id": "precios", "texto": "Precios", "href": "/precios", "nota": "con IVA", "items": ()},
)

SPRITE = """<svg class="vt-sprite" width="0" height="0" aria-hidden="true" focusable="false">
<symbol id="vt-i-wa" viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></symbol>
<symbol id="vt-i-tel" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></symbol>
<symbol id="vt-i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h11"/></symbol>
<symbol id="vt-i-chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
</svg>"""
CHEV = '<svg class="vt-chev" aria-hidden="true"><use href="#vt-i-chev"/></svg>'
WA_GLIFO = '<span class="vt-wa-g"><svg aria-hidden="true"><use href="#vt-i-wa"/></svg></span>'


def esc(texto):
    return escape(str(texto), quote=True)


def region(nombre, cuerpo):
    return f"<!-- vt:{nombre} -->\n{cuerpo}\n<!-- /vt:{nombre} -->"


FUENTE_PRINCIPAL = "/fonts/archivo-latin.woff2"


def head(urls, legacy, tienda=False, plantas=False, materiales=False, precios=False, blog=False, obras=False):
    """Favicon, geo de la tienda, fuente principal precargada, CSS del shell (y legacy-fixes en páginas con Tailwind),
    GA4 una sola vez y terra.js diferido. Con tienda=True (páginas <body class="vt-pagina vt-tienda">), también
    terra-tienda.css. Con plantas=True (páginas <body class="vt-pagina vt-plantas">, Etapa 2e), terra-plantas.css. Con
    materiales=True (<body class="vt-pagina vt-materiales">, Etapa 2f), terra-materiales.css. Con precios=True
    (<body class="vt-pagina vt-precios">, Etapa 2g), terra-precios.css.
    Las meta keywords, last-modified, ai-content-declaration y language ya no se usan: no se
    reponen."""
    lineas = [
        '<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">',
        '<meta name="geo.region" content="MX-TAM">',
        f'<meta name="geo.placename" content="{datos.CIUDAD}">',
        f'<link rel="preload" href="{FUENTE_PRINCIPAL}" as="font" type="font/woff2" crossorigin>',
    ]
    if legacy:
        lineas.append(f'<link rel="stylesheet" href="{urls["legacy-fixes.css"]}">')
    lineas += [
        f'<link rel="stylesheet" href="{urls["terra.css"]}">',
    ]
    if tienda:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-tienda.css"]}">')
    if plantas:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-plantas.css"]}">')
    if materiales:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-materiales.css"]}">')
    if precios:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-precios.css"]}">')
    if obras:  # páginas con mosaico de fotos reales (class="vt-mosaico")
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-obras.css"]}">')
    if blog:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-blog.css"]}">')
    lineas += [
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={datos.GA4_ID}"></script>',
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        f"gtag('js',new Date());gtag('config','{datos.GA4_ID}');</script>",
        f'<script src="{urls["terra.js"]}" defer></script>',
    ]
    return region("head", "\n".join(lineas))


def _enlace(texto, href, ruta):
    actual = ' aria-current="page"' if href == ruta else ""
    return f'<li><a href="{href}"{actual}>{esc(texto)}</a></li>'


def _item_escritorio(item, ctx):
    clase = "vt-nav__item is-activo" if item["id"] == ctx["activo"] else "vt-nav__item"
    if not item["items"]:
        actual = ' aria-current="page"' if item["href"] == ctx["ruta"] else ""
        return f'<li class="{clase}"><a class="vt-nav__top" href="{item["href"]}"{actual}>{esc(item["texto"])}</a></li>'
    panel = f"vt-panel-{item['id']}"
    if item["href"]:
        cabeza = (f'<a class="vt-nav__top" href="{item["href"]}">{esc(item["texto"])}</a>'
                  f'<button class="vt-nav__exp" type="button" aria-expanded="false" aria-controls="{panel}">'
                  f'<span class="vt-sr">Submenú de {esc(item["texto"])}</span>{CHEV}</button>')
    else:
        cabeza = (f'<button class="vt-nav__top" type="button" aria-expanded="false" aria-controls="{panel}">'
                  f'{esc(item["texto"])}{CHEV}</button>')
    enlaces = "".join(_enlace(t, h, ctx["ruta"]) for t, h in item["items"])
    return f'<li class="{clase}">{cabeza}<ul class="vt-nav__panel" id="{panel}">{enlaces}</ul></li>'


def _item_movil(item, ctx):
    nota = f'<small>{esc(item["nota"])}</small>'
    if not item["items"]:
        actual = ' aria-current="page"' if item["href"] == ctx["ruta"] else ""
        return f'<a class="vt-mmenu__link" href="{item["href"]}"{actual}>{esc(item["texto"])}{nota}</a>'
    abierto = " open" if item["id"] == ctx["activo"] else ""
    enlaces = "".join(_enlace(t, h, ctx["ruta"]) for t, h in item["items"])
    fin = f'<span class="vt-acc__fin">{nota}{CHEV}</span>'
    return f'<details class="vt-acc"{abierto}><summary>{esc(item["texto"])}{fin}</summary><ul>{enlaces}</ul></details>'


def header(ctx):
    """Skip-link, íconos, menú de 6 entradas con paneles, CTA de WhatsApp con el mensaje del servicio y menú móvil."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje"]))
    escritorio = "\n".join(_item_escritorio(item, ctx) for item in MENU)
    movil = "\n".join(_item_movil(item, ctx) for item in MENU)
    cuerpo = f"""<a class="vt-skip" href="#main">Saltar al contenido</a>
{SPRITE}
<header class="vt-head" data-vt-tipo="{tipo}" data-vt-servicio="{ctx['servicio']}">
<div class="vt-head__bar">
<a class="vt-head__logo" href="/"><img src="{LOGO}" alt="Viveros Terra, inicio" width="150" height="41"></a>
<nav class="vt-nav" aria-label="Principal">
<ul class="vt-nav__list">
{escritorio}
</ul>
</nav>
<p class="vt-head__meta"><b>{datos.DOMICILIO_CORTO}</b>{datos.HORARIO}</p>
<a class="vt-btn vt-btn--wa vt-head__cta" data-cta="{tipo}:header" href="{wa}" target="_blank" rel="noopener">{WA_GLIFO}<span class="vt-head__cta-largo">Cotizar por WhatsApp</span><span class="vt-head__cta-corto">Cotizar</span></a>
<button class="vt-burger" type="button" aria-expanded="false" aria-controls="vt-mmenu"><svg aria-hidden="true"><use href="#vt-i-menu"/></svg><span class="vt-sr">Menú</span></button>
</div>
<nav class="vt-mmenu" id="vt-mmenu" aria-label="Principal, móvil" hidden>
{movil}
<p class="vt-mmenu__meta">{datos.CALLE}, Cd. Madero · <a data-cta="{tipo}:menu" href="tel:{datos.TELEFONO_TEL}">{datos.TELEFONO_VISIBLE}</a></p>
</nav>
</header>"""
    return region("header", cuerpo)


PIE = (
    ("Servicios", (("Pasto en rollo", "/pasto-en-rollo-tampico"),
                   ("Mayoreo de pasto", "/mayoreo-pasto-tampico"),
                   ("Pasto sintético en Tampico", "/pasto-sintetico-tampico"),
                   ("Tienda de pasto sintético", "/pasto-sintetico"),
                   ("Diseño de jardines", "/diseno-jardines-tampico"),
                   ("Mantenimiento", "/mantenimiento-jardines-tampico"),
                   ("Riego automático", "/sistema-riego-tampico"))),
    ("Plantas y materiales", (("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico"),
                              ("Palmas para proyectos", "/palmas-mayoreo-proyectos"),
                              ("Arma tu lista", "/catalogo"),
                              ("Tierra negra", "/tierra-negra-vegetal-tampico"),
                              ("Tezontle rojo", "/tezontle-rojo-tampico"),
                              ("Mármol blanco", "/marmol-blanco-tampico"),
                              ("Piedra bola de río", "/piedra-bola-rio-tampico"))),
    ("Zonas", (("Lomas de Rosales", "/jardineria-lomas-de-rosales-tampico"),
               ("Country Club", "/jardineria-country-club-tampico"),
               ("Águila y Altavista", "/jardineria-aguila-tampico"),
               ("Lomas del Chairel", "/jardineria-lomas-del-chairel-tampico"),
               ("Ciudad Madero", "/jardineria-ciudad-madero"),
               ("Altamira", "/jardineria-altamira"))),
    ("Viveros Terra", (("Visítanos", "/vivero-tampico"),
                       ("Precios", "/precios"),
                       ("Blog", "/blog"),
                       ("Políticas y garantías", "/politicas"),
                       ("Aviso de privacidad", "/politica-privacidad"))),
)
DATOS_PIE = (
    ("Domicilio", datos.CALLE, f"{datos.COLONIA}, {datos.CP} {datos.CIUDAD}, {datos.ESTADO}"),
    ("Referencia", "Frente a Walmart", "Entrando por Banamex"),
    ("Horario", "Lun a vie 9 a 18 h", "Sábado 9 a 14 h"),
    ("REPSE", datos.REPSE, "Padrón de la STPS"),
    ("Factura", datos.FACTURA, "Persona física o moral"),
    ("Desde", str(datos.DESDE), f"{datos.M2_INSTALADOS} instalados"),
)


def _columna(titulo, enlaces):
    items = "".join(f'<li><a href="{href}">{esc(texto)}</a></li>' for texto, href in enlaces)
    return f'<div class="vt-foot__col"><h2 class="vt-foot__h">{esc(titulo)}</h2><ul>{items}</ul></div>'


def barra(ctx):
    """Barra fija móvil [Cotizar por WhatsApp | teléfono]; terra.js la oculta mientras el CTA del hero se ve."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje"]))
    return f"""<div class="vt-bar" data-vt-bar role="region" aria-label="Contacto rápido">
<a class="vt-btn vt-btn--wa vt-bar__go" data-cta="{tipo}:barra" href="{wa}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>
<a class="vt-bar__tel" data-cta="{tipo}:barra" href="tel:{datos.TELEFONO_TEL}" aria-label="Llamar {datos.TELEFONO_VISIBLE}"><svg aria-hidden="true"><use href="#vt-i-tel"/></svg></a>
</div>"""


def footer(ctx):
    """Pie único con columnas, contacto, promesa, cuadro de datos y redes; incluye la barra móvil si el contexto la pide."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje_pie"]))
    columnas = "\n".join(_columna(titulo, enlaces) for titulo, enlaces in PIE)
    celdas = "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>" for t, v, s in DATOS_PIE)
    redes = "".join(f'<a href="{url}" target="_blank" rel="noopener">{esc(nombre)}</a>' for nombre, url in datos.REDES)
    correo_visible = datos.CORREO_FORMULARIOS.replace("@", "@<wbr>")  # a 375 px corta después de la arroba
    tel = f'<span class="vt-nowrap">{datos.TELEFONO_VISIBLE}</span>'
    contacto = (
        '<div class="vt-foot__col vt-foot__contacto"><h2 class="vt-foot__h">Contacto</h2><ul>'
        f'<li><a data-cta="{tipo}:footer" href="{wa}" target="_blank" rel="noopener">WhatsApp {tel}</a></li>'
        f'<li><a data-cta="{tipo}:footer" href="tel:{datos.TELEFONO_TEL}">Llamar {tel}</a></li>'
        f'<li><a class="vt-foot__correo" href="mailto:{datos.CORREO_FORMULARIOS}">{correo_visible}</a></li>'
        f'<li><a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Cómo llegar</a></li></ul>'
        f'<p class="vt-foot__promesa">{esc(datos.PROMESA_COMPLETA)}</p></div>'
    )
    pie = f"""<footer class="vt-foot">
<div class="vt-wrap">
<div class="vt-foot__grid">
<div class="vt-foot__about"><img src="{LOGO}" alt="Viveros Terra" width="150" height="41" loading="lazy"><p>Vivero, pasto en rollo y jardinería en Tampico, Madero y Altamira desde {datos.DESDE}. Pasto sintético con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}.</p><p class="vt-foot__google">{esc(datos.GOOGLE)}</p></div>
{columnas}
{contacto}
</div>
<dl class="vt-foot__datos">{celdas}</dl>
<div class="vt-foot__legal"><p>© {datos.ANIO} {datos.NOMBRE} · {datos.CIUDAD}, Tamaulipas · Precios {datos.ANIO} con IVA incluido</p><p class="vt-foot__redes">{redes}</p></div>
</div>
</footer>"""
    cuerpo = pie + ("\n" + barra(ctx) if ctx["barra"] else "")
    return region("footer", cuerpo)
