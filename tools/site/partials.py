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


def head(urls, legacy):
    """Favicon, CSS del shell (y legacy-fixes en páginas con Tailwind), GA4 una sola vez y terra.js diferido."""
    lineas = ['<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">']
    if legacy:
        lineas.append(f'<link rel="stylesheet" href="{urls["legacy-fixes.css"]}">')
    lineas += [
        f'<link rel="stylesheet" href="{urls["terra.css"]}">',
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
    return f'<details class="vt-acc"{abierto}><summary>{esc(item["texto"])}{nota}</summary><ul>{enlaces}</ul></details>'


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
