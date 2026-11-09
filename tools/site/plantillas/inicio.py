"""Plantilla de la home (spec §3.3): portada con precio y CTA en el primer pantallazo móvil → cuadro de datos → qué
hacemos (cada ruta con su precio) → Medidor → obras con pies FIG. y clientes → opiniones con nombre → proceso
NOSOTROS / TÚ → precios → preguntas → cobertura por zona → CTA final. Sin formulario por correo: se cotiza por WhatsApp o con el Medidor. El contenido vive en tools/site/contenido/inicio.py."""
import componentes as c
from plantillas import base

TIPO = "home"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-medidor.js")
CONTEXTO = "https://schema.org"


def _franja_temporada(t):
    """Franja de temporada bajo la portada, con clases existentes (terra.css no tiene presupuesto). None: fuera de temporada."""
    if not t:
        return ""
    return (f'<aside class="vt-wrap" aria-label="{t["aviso"]}"><p class="vt-prueba"><span><b>{t["titulo"]}</b></span><span>{t["texto"]}</span>'
            f'<a data-cta="{TIPO}:nochebuenas" href="{t["href"]}">{t["cta"]}</a></p></aside>')


def render(k):
    q, m, o, op, pr, pc, f, co, ci = (k[s] for s in ("que_hacemos", "medidor", "obras", "opiniones", "proceso", "precios",
                                                      "faq", "cobertura", "cierre"))
    cuerpo = "\n".join((
        c.portada(k["portada"], TIPO),
        _franja_temporada(k["temporada"]),
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
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS)
