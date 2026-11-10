"""Plantilla de la home (spec §3.3): portada con precio y CTA en el primer pantallazo móvil → cuadro de datos → qué
hacemos (cada ruta con su precio) → Medidor → obras con pies FIG. y clientes → opiniones con nombre → proceso
NOSOTROS / TÚ → precios → preguntas → cobertura por zona → CTA final. Sin formulario por correo: se cotiza por WhatsApp o con el Medidor. El contenido vive en tools/site/contenido/inicio.py.

Hero y conversión (docs/superpowers/specs/2026-11-09-home-hero-y-conversion-design.md, Entrega 1): la portada, la fila de
WhatsApp de cada sección y el cierre son propios de la home y se visten con public/css/terra-inicio.css (todo bajo
.vt-inicio). Desde la Entrega A de experiencia (2026-11-10) la portada es el componente común c.portada."""
import componentes as c
import datos
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


# Filas de WhatsApp de sección: texto del botón y si llevan la promesa debajo (solo la primera y la última).
_FILAS = {"opiniones": ("Cotizar mi jardín por WhatsApp", True), "proceso": ("Empezar por WhatsApp", False),
          "precios": ("Pedir mi precio por WhatsApp", False), "faq": ("Preguntar por WhatsApp", True)}


def _portada(p):
    """Portada de la home: el hero de marca común (componentes.portada), del que es la referencia. pliegue=False: en
    celular la etiqueta de precio va entre el lede y el botón y la foto al final (diseño aprobado el 2026-11-09); desde
    1024 px terra.css cuelga la etiqueta sobre la esquina de la foto. Un solo botón, dos enlaces de texto y la línea de
    confianza con los clientes atendidos."""
    hero = dict(p, enlaces=(("Calcula tu patio", "#medidor", None, 'id="vt-calcula-patio"'),),
                dato=f"<b>{esc(datos.CLIENTES)}</b> clientes")
    return c.portada(hero, TIPO, pliegue=False)


def _fila_wa(mensaje, seccion):
    """WhatsApp al final de una sección larga (opiniones, proceso, precios y preguntas). data-hero-cta: la barra fija
    de celular se esconde mientras la fila se ve, para no mostrar dos botones iguales."""
    texto, con_promesa = _FILAS[seccion]
    promesa = f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p>' if con_promesa else ""
    return f'<div class="vt-inicio__fila" data-hero-cta>{c.boton_wa(mensaje, f"{TIPO}:{seccion}", texto)}{promesa}</div>'


def _resenas():
    return (f'<p class="vt-inicio__resenas"><a href="{esc(datos.MAPS_URL)}" target="_blank" rel="noopener">'
            'Ver las reseñas en Google</a></p>')


def _cierre(ci):
    """CTA final: lo último antes de los botones es la promesa de respuesta; la garantía de arraigo y el costo de la
    visita van después."""
    return (
        '<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
        f'<h2 id="vt-cierre-titulo">{ci["titulo"]}</h2><p class="vt-lede">{ci["lede"]}</p>'
        f'<p class="vt-promesa">{c.promesa_horario()}</p>'
        f'<div class="vt-cta">{c.boton_wa(ci["mensaje"], f"{TIPO}:cierre")}{c.boton_tel(f"{TIPO}:cierre")}</div>'
        f'<p class="vt-promesa">{c.garantia_pasto("Pasto instalado: ")}</p><p class="vt-promesa">{ci["visita"]}</p></div>'
        f'<p class="vt-cierre__msg"><b>El mensaje que se abre</b>{esc(datos.con_firma(ci["mensaje"]))}</p></div></section>')


def render(k):
    q, m, o, op, pr, pc, f, co, ci = (k[s] for s in ("que_hacemos", "medidor", "obras", "opiniones", "proceso", "precios",
                                                      "faq", "cobertura", "cierre"))
    mensaje = k["portada"]["mensaje"]
    cuerpo = "\n".join((
        _banner_temporada(k["temporada"]),
        _portada(k["portada"]),
        c.respuesta(k.get("respuesta")),
        c.bloque(1, "Qué hacemos", "vt-h-que", q["titulo"], c.indice(q["items"], TIPO), lede=q["lede"]),
        c.bloque(2, "Medidor", "vt-h-medidor", m["titulo"],
                 c.medidor("inicio", TIPO, mensaje=k["portada"]["mensaje"], boton_medida=True, garantia=True,
                           resultado_vivo=True),
                 lede=m["lede"], tinte=True, id_seccion="medidor"),
        c.bloque(3, "Jardines entregados", "vt-h-obras", o["titulo"],
                 c.obras(o["figuras"]) + c.linea_prueba() + f'<h3 class="vt-mt">{o["titulo_clientes"]}</h3>' + c.logos(),
                 lede=o["lede"]),
        c.bloque(4, "Opiniones", "vt-h-opiniones", op["titulo"], c.testimonios(op["items"]) + _resenas() + _fila_wa(mensaje, "opiniones"),
                 lede=op["lede"]),
        c.bloque(5, "Cómo trabajamos", "vt-h-como", pr["titulo"], c.pasos(pr["pasos"]) + _fila_wa(mensaje, "proceso"),
                 lede=pr["lede"], tinte=True),
        c.bloque_dos(6, "Precios", "vt-h-precios", pc["titulo"], f'<p class="vt-lede">{pc["lede"]}</p>' + c.nota(*pc["nota"]),
                     c.tabla_precios(pc["filas"], pc["caption"]) + c.planes_mensualidades() + _fila_wa(mensaje, "precios"),
                     id_seccion="precios"),
        c.bloque_dos(7, "Preguntas", "vt-h-faq", f["titulo"], f'<h3 class="vt-mt">{f["titulo_guias"]}</h3>' + c.guias(f["guias"]),
                     c.faq(f["preguntas"]) + _fila_wa(mensaje, "faq"), tinte=True),
        c.bloque(8, "Cobertura", "vt-h-cobertura", co["titulo"], c.cobertura(co["zonas"], co["por_proyecto"]),
                 lede=co["lede"]),
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
