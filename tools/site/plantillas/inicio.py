"""Plantilla de la home (spec §3.3): portada con precio y CTA en el primer pantallazo móvil → cuadro de datos → qué
hacemos (cada ruta con su precio) → Medidor → obras con pies FIG. y clientes → opiniones con nombre → proceso
NOSOTROS / TÚ → precios → preguntas → cobertura por zona → CTA final. Sin formulario por correo: se cotiza por WhatsApp o con el Medidor. El contenido vive en tools/site/contenido/inicio.py.

Hero y conversión (docs/superpowers/specs/2026-11-09-home-hero-y-conversion-design.md, Entrega 1): la portada, la fila de
WhatsApp de cada sección y el cierre son propios de la home y se visten con public/css/terra-inicio.css (todo bajo
.vt-inicio). Desde la Entrega A de experiencia (2026-11-10) la portada es el componente común c.portada."""
import componentes as c
import datos
from contenido.inicio import MENSAJES
from partials import esc
from plantillas import base

TIPO = "home"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-medidor.js")
CONTEXTO = "https://schema.org"


# Banner de temporada, pedido del dueño (2026-11-09): rojo navideño con la etiqueta amarilla del sitio (terra-temporada.css).
_FLOR = ('<svg class="vt-navidad__flor" viewBox="-16 -16 32 32" aria-hidden="true" fill="currentColor">'
         + "".join(f'<path transform="rotate({g})" d="M0-1C-5-5-5-12 0-16 5-12 5-5 0-1Z"/>' for g in range(0, 360, 45))
         + '<circle class="vt-navidad__centro" r="2.6"/></svg>')


def _banner_temporada(t):
    """Banner navideño, primero en <main>; todo el banner enlaza a la página de temporada. Vacío fuera de temporada.
    El <span data-vt-hasta> sale vacío: terra.js escribe los días que faltan de preventa (solo días); en celular esa
    frase sustituye al renglón de precios (terra-temporada.css) para que el banner no crezca."""
    if not t:
        return ""
    return (f'<aside class="vt-navidad-x" aria-label="{t["aviso"]}"><a class="vt-navidad" data-cta="{TIPO}:banner-nochebuenas" '
            f'href="{t["href"]}">{_FLOR}<span class="vt-navidad__txt"><b>{t["titulo"]}<span class="vt-navidad__estado"> · '
            f'{t["estado"]}</span></b><span><span class="vt-navidad__precios">{t["texto"]}</span>'
            f'<span class="vt-navidad__hasta" data-vt-hasta="{t["hasta"]}" data-vt-build="{datos.ACTUALIZADO}"></span>'
            f'</span></span><span class="vt-navidad__cta">'
            f'Ver<span class="vt-navidad__mas"> nochebuenas</span><span class="vt-navidad__flecha" aria-hidden="true">→</span>'
            '</span></a></aside>')


# Filas de WhatsApp de sección: texto del botón y si llevan la promesa debajo. Plan visual V1 (2026-11-11): ninguna;
# la promesa va en la línea de confianza del hero y en el cierre.
# Auditoría de la home (2026-11-19, entregas A y B): la galería suma su botón (cerraba un tramo de casi 5 pantallas sin
# CTA), cada texto dice qué se manda y cada fila abre su propio mensaje (contenido/inicio.py, MENSAJES).
_FILAS = {"obras": ("Quiero un jardín así", False), "opiniones": ("Cotizar mi jardín por WhatsApp", False),
          "proceso": ("Mandar mi foto por WhatsApp", False), "precios": ("Pedir mi precio cerrado por WhatsApp", False),
          "faq": ("Preguntar por WhatsApp", False)}

# Entrega A: franja de confianza bajo la portada, con cifras que convencen al dueño de casa (antes: Desde, Instalado,
# Showroom y Factura). La factura y el REPSE siguen en la fila «Empresas y constructoras» y en el pie.
_NOTA, _, _RESENAS = datos.GOOGLE.partition(" ")
DATOS_CONFIANZA = (
    ("Google", _NOTA, _RESENAS.strip("()")),
    ("Instalaciones", datos.INSTALACIONES, f"Desde {datos.DESDE}"),
    ("Pasto instalado", datos.M2_INSTALADOS, "En Tamaulipas y la Huasteca"),
    ("Vivero", datos.CALLE_CORTA, datos.REFERENCIA),
)


def _portada(p):
    """Portada de la home: el hero de marca común (componentes.portada), del que es la referencia. pliegue=False: en
    celular la etiqueta de precio va entre el lede y el botón y la foto al final (diseño aprobado el 2026-11-09); desde
    1024 px terra.css cuelga la etiqueta sobre la esquina de la foto. Un solo botón, dos enlaces de texto y la línea de
    confianza con los clientes atendidos."""
    # Entrega A: junto al botón, las tres dudas que frenan el clic (respuesta, garantía y mensualidades).
    # Entrega B: pliegue=True, como el resto del sitio: en celular la foto de la cuadrilla entra en la primera pantalla.
    hero = dict(p, enlaces=(("Calcular cuánto cuesta mi patio", "#medidor", None, 'id="vt-calcula-patio"'),),
                dato=(f'Garantía de arraigo de {esc(datos.ARRAIGO)} (<a href="{c.CONDICIONES_PASTO}">condiciones</a>)',
                      "Contado o mensualidades con tarjeta"))
    franja = (c.cuadro_datos(DATOS_CONFIANZA, tira=True)
              + f'<div class="vt-inicio__clientes"><p class="vt-inicio__clientes-t">Nos han contratado</p>{c.logos()}</div>')
    return c.portada(hero, TIPO, pliegue=True, datos_html=franja)


def _fila_wa(seccion):
    """WhatsApp al final de una sección larga (opiniones, proceso, precios y preguntas). data-hero-cta: la barra fija
    de celular se esconde mientras la fila se ve, para no mostrar dos botones iguales."""
    texto, con_promesa = _FILAS[seccion]
    mensaje = MENSAJES[seccion]
    promesa = f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p>' if con_promesa else ""
    return f'<div class="vt-inicio__fila" data-hero-cta>{c.boton_wa(mensaje, f"{TIPO}:{seccion}", texto)}{promesa}</div>'


def _resenas():
    total = datos.GOOGLE.partition("(")[2].split()[0]
    return (f'<p class="vt-inicio__resenas"><a href="{esc(datos.MAPS_URL)}" target="_blank" rel="noopener">'
            f'Leer las {esc(total)} reseñas en Google</a></p>')


def _mas_precios(texto, href):
    return f'<p class="vt-inicio__mas"><a href="{esc(href)}">{esc(texto)} <span aria-hidden="true">→</span></a></p>'


def _cierre(ci):
    """CTA final: lo último antes de los botones es la promesa de respuesta; la garantía de arraigo y el costo de la
    visita van después. El recuadro muestra el mensaje tal como se abre (sin las rayas «___», que no se mandan)."""
    return (
        '<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
        f'<h2 id="vt-cierre-titulo">{ci["titulo"]}</h2><p class="vt-lede">{ci["lede"]}</p>'
        f'<p class="vt-promesa">{c.promesa_horario()}</p>'
        f'<div class="vt-cta">{c.boton_wa(ci["mensaje"], f"{TIPO}:cierre", "Mandar medidas y foto por WhatsApp")}{c.boton_tel(f"{TIPO}:cierre")}</div>'
        f'<p class="vt-promesa">{c.garantia_pasto("Pasto instalado: ")}</p><p class="vt-promesa">{ci["visita"]}</p></div>'
        f'<p class="vt-cierre__msg"><b>El mensaje que se abre</b>'
        f'{esc(datos.sin_huecos(datos.con_firma(ci["mensaje"])))}</p></div></section>')


def render(k):
    q, m, o, op, pr, pc, f, co, ci = (k[s] for s in ("que_hacemos", "medidor", "obras", "opiniones", "proceso", "precios",
                                                      "faq", "cobertura", "cierre"))
    # Auditoría de la home (2026-11-19, entrega B): portada con la franja de confianza → «En corto» (SEO fase 1) → qué
    # necesitas → medidor → jardines con su botón → opiniones → cómo trabajamos → precios del pasto → preguntas →
    # cobertura y guías → cierre. De ~22 a ~18 pantallas de celular.
    cuerpo = "\n".join((
        _banner_temporada(k["temporada"]),
        _portada(k["portada"]),
        c.respuesta(k.get("respuesta")),
        c.bloque(1, "Qué hacemos", "vt-h-que", q["titulo"], c.indice(q["items"], TIPO), lede=q["lede"]),
        c.bloque(2, "Medidor", "vt-h-medidor", m["titulo"],
                 c.medidor("inicio", TIPO, mensaje=k["portada"]["mensaje"], boton_medida=True, garantia=True,
                           resultado_vivo=True),
                 lede=m["lede"], tinte=True, id_seccion="medidor"),
        c.bloque(3, "Jardines entregados", "vt-h-obras", o["titulo"], c.obras(o["figuras"], carrusel=True) + _fila_wa("obras"),
                 lede=o["lede"]),
        # Plan visual V2: las opiniones son el momento oscuro a media página; en celular, una junto a otra (fila).
        c.momento(c.bloque(4, "Opiniones", "vt-h-opiniones", op["titulo"],
                           c.testimonios(op["items"], fila=True) + _resenas() + _fila_wa("opiniones"),
                           lede=op["lede"])),
        c.bloque(5, "Cómo trabajamos", "vt-h-como", pr["titulo"], c.pasos(pr["pasos"]) + _fila_wa("proceso"),
                 lede=pr["lede"], tinte=True),
        c.bloque_dos(6, "Precios", "vt-h-precios", pc["titulo"], f'<p class="vt-lede">{pc["lede"]}</p>' + c.nota(*pc["nota"]),
                     c.tabla_precios(pc["filas"], pc["caption"]) + _mas_precios(*pc["mas"]) + c.planes_mensualidades()
                     + _fila_wa("precios"), id_seccion="precios"),
        c.bloque_dos(7, "Preguntas", "vt-h-faq", f["titulo"], "",
                     c.faq(f["preguntas"]) + _fila_wa("faq"), tinte=True),
        c.bloque(8, "Cobertura", "vt-h-cobertura", co["titulo"],
                 c.cobertura(co["zonas"], co["por_proyecto"]) + f'<h3 class="vt-mt">{f["titulo_guias"]}</h3>'
                 + c.guias(f["guias"]), lede=co["lede"]),
        _cierre(ci),
    ))
    j = k["jsonld"]
    # SEO fase 1: un solo @graph con el sitio, el nodo completo del negocio y las preguntas; el WebPage (con su
    # speakable) lo cierra entidad.completar.
    bloques = ({"@context": CONTEXTO, "@graph": [j["sitio"], j["negocio"],
                                                  c.faq_jsonld(f["preguntas"], speakable=j["speakable"])]},)
    return base.documento(base.meta_de(k), cuerpo, jsonld_bloques=bloques,
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS,
                          clase_body="vt-pagina vt-inicio vt-temporada" if k["temporada"] else "vt-pagina vt-inicio")
