"""Plantilla de la home (spec §3.3): portada con precio y CTA en el primer pantallazo móvil → cuadro de datos → qué
hacemos (cada ruta con su precio) → Medidor → obras con pies FIG. y clientes → opiniones con nombre → proceso
NOSOTROS / TÚ → precios → preguntas → cobertura por zona → CTA final. Sin formulario por correo: se cotiza por WhatsApp o con el Medidor. El contenido vive en tools/site/contenido/inicio.py."""
import componentes as c
from plantillas import base

TIPO = "home"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-medidor.js")
CONTEXTO = "https://schema.org"


# Banner de temporada, pedido del dueño (2026-11-09): rojo navideño con la etiqueta amarilla del sitio (terra-temporada.css).
_FLOR = ('<svg class="vt-navidad__flor" viewBox="-16 -16 32 32" aria-hidden="true" fill="currentColor">'
         + "".join(f'<path transform="rotate({g})" d="M0-1C-5-5-5-12 0-16 5-12 5-5 0-1Z"/>' for g in range(0, 360, 45))
         + '<circle class="vt-navidad__centro" r="2.6"/></svg>')


def _banner_temporada(t):
    """Banner navideño, primero en <main>; todo el banner enlaza a la página de temporada. Vacío fuera de temporada."""
    if not t:
        return ""
    return (f'<aside class="vt-navidad-x" aria-label="{t["aviso"]}"><a class="vt-navidad" data-cta="{TIPO}:banner-nochebuenas" '
            f'href="{t["href"]}">{_FLOR}<span class="vt-navidad__txt"><b>{t["titulo"]}<span class="vt-navidad__estado"> · '
            f'{t["estado"]}</span></b><span>{t["texto"]}</span></span><span class="vt-navidad__cta">'
            f'Ver<span class="vt-navidad__mas"> nochebuenas</span><span class="vt-navidad__flecha" aria-hidden="true">→</span>'
            '</span></a></aside>')


def render(k):
    q, m, o, op, pr, pc, f, co, ci = (k[s] for s in ("que_hacemos", "medidor", "obras", "opiniones", "proceso", "precios",
                                                      "faq", "cobertura", "cierre"))
    cuerpo = "\n".join((
        _banner_temporada(k["temporada"]),
        c.portada(k["portada"], TIPO),
        c.bloque(1, "Qué hacemos", "vt-h-que", q["titulo"], c.indice(q["items"]), lede=q["lede"]),
        c.bloque(2, "Medidor", "vt-h-medidor", m["titulo"], c.medidor("inicio", TIPO, mensaje=k["portada"]["mensaje"]), lede=m["lede"], tinte=True,
                 id_seccion="medidor"),
        c.bloque(3, "Jardines entregados", "vt-h-obras", o["titulo"],
                 c.obras(o["figuras"]) + c.linea_prueba() + f'<h3 class="vt-mt">{o["titulo_clientes"]}</h3>' + c.logos(),
                 lede=o["lede"]),
        c.bloque(4, "Opiniones", "vt-h-opiniones", op["titulo"], c.testimonios(op["items"]), lede=op["lede"]),
        c.bloque(5, "Cómo trabajamos", "vt-h-como", pr["titulo"], c.pasos(pr["pasos"]), lede=pr["lede"], tinte=True),
        c.bloque_dos(6, "Precios", "vt-h-precios", pc["titulo"], f'<p class="vt-lede">{pc["lede"]}</p>' + c.nota(*pc["nota"]),
                     c.tabla_precios(pc["filas"], pc["caption"]) + c.planes_mensualidades(), id_seccion="precios"),
        c.bloque_dos(7, "Preguntas", "vt-h-faq", f["titulo"], f'<h3 class="vt-mt">{f["titulo_guias"]}</h3>' + c.guias(f["guias"]),
                     c.faq(f["preguntas"]), tinte=True),
        c.bloque(8, "Cobertura", "vt-h-cobertura", co["titulo"], c.cobertura(co["zonas"], co["por_proyecto"]),
                 lede=co["lede"]),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], TIPO),
    ))
    j = k["jsonld"]
    bloques = (
        {"@context": CONTEXTO, **j["negocio"]},
        {"@context": CONTEXTO, **c.faq_jsonld(f["preguntas"], speakable=j["speakable"])},
        {"@context": CONTEXTO, **j["migas"]},
    )
    return base.documento(k["meta"], cuerpo, jsonld_bloques=bloques,
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS,
                          clase_body="vt-pagina vt-temporada" if k["temporada"] else "vt-pagina")
