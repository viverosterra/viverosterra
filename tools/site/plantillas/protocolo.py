"""Plantilla del protocolo de cuidados de pasto San Agustín (spec §3.3, "HowTo visible"): cabecera con la foto de
producción → etapas de riego por días → señales → mantenimiento → condiciones de la garantía (#garantia) → contacto."""
import componentes as c
import componentes_util as cu
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _lista(items):
    return '<ul class="vt-checks">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def _fases(fases):
    filas = "".join(f'<li class="vt-modo"><p class="vt-kicker">{f["dias"]}</p><h3>{f["titulo"]}</h3>{_lista(f["items"])}</li>'
                    for f in fases)
    return f'<ol class="vt-modos vt-fichas vt-util__fases">{filas}</ol>'


def _senales(items):
    return '<ul class="vt-modos vt-fichas">' + "".join(
        f'<li class="vt-modo"><h3>{s["titulo"]}</h3>{_lista(s["items"])}</li>' for s in items) + "</ul>"


def render(k):
    tipo, g, ci = k["tipo"], k["garantia"], k["cierre"]
    bloques = [
        cu.cabeza(k["cabeza"]),
        c.bloque(1, "Plan de cuidados", "vt-h-plan", k["plan"]["titulo"], _fases(k["plan"]["fases"]), lede=k["plan"]["lede"]),
        c.bloque(2, "Señales", "vt-h-senales", k["senales"]["titulo"], _senales(k["senales"]["items"]), tinte=True),
        c.bloque(3, "Después del día 20", "vt-h-mant", k["mantenimiento"]["titulo"], _lista(k["mantenimiento"]["items"])),
        c.bloque(4, "Garantía", "vt-h-garantia", g["titulo"], _lista(g["condiciones"]) + f'<p class="vt-promesa">{g["pie"]}</p>',
                 lede=g["lede"], tinte=True, id_seccion="garantia"),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    return base.documento(k["meta"], "\n".join(bloques), jsonld_bloques=k["jsonld"],
                          precargas=(base.precarga_imagen(k["cabeza"]["foto"]),), clase_body=CLASE_BODY)
