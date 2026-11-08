"""Plantilla de servicio local (spec §3.3): ruta visible → H1 con beneficio y lugar → precio ancla en la etiqueta → CTA
con plantilla y promesa → prueba (cuadro de datos, fotos FIG., nota de campo, opinión con nombre y clientes) → precio con
Medidor → objeción principal → proceso NOSOTROS / TÚ (también es el HowTo del JSON-LD) → garantía con condiciones →
pago (anticipo y mensualidades con tarjeta de crédito, con su simulador) → preguntas → cobertura → relacionados → CTA
final. Las secciones que el contenido no trae se omiten (diseño, mantenimiento y riego no llevan Medidor de pasto).
Primera página: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py)."""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor y el simulador); el Medidor solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return ("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ()) + ("/js/vt-simulador.js",)


def _prueba(k, numero):
    pr = k["prueba"]
    cuerpo = c.obras(pr["figuras"], c.nota(*pr["nota"]))
    if pr.get("opiniones"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_opinion"]}</h3>' + c.testimonios(pr["opiniones"])
    if pr.get("titulo_clientes"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_clientes"]}</h3>' + c.logos()
    return c.bloque(numero, "Prueba", "vt-h-prueba", pr["titulo"], cuerpo, lede=pr["lede"])


def _precio(k, numero):
    p = k["precio"]
    cuerpo = c.tabla_precios(p["filas"], p["caption"], concepto="Forma de compra")
    if p.get("titulo_medidor"):
        cuerpo += f'<h3 class="vt-mt">{p["titulo_medidor"]}</h3>' + c.medidor(k["prefijo"], k["tipo"], mensaje=k["portada"]["mensaje"])
    return c.bloque(numero, "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p["lede"], tinte=True, id_seccion="precio")


def _objecion(k, numero):
    o = k["objecion"]
    a, b = o["comparativa"], o["comparativa_2"]
    cuerpo = (c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
              + f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"]))
    return c.bloque(numero, "Cuál te conviene", "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])


def _pago(k, numero):
    """Un solo bloque de pago: anticipo, contado y mensualidades en tres renglones, y el simulador (los plazos y montos
    mínimos los muestra el propio simulador, sin repetir la tabla de planes)."""
    p = k["pago"]
    puntos = "".join(f"<li>{t}</li>" for t in p["puntos"])
    izquierda = f'<p class="vt-lede">{p["lede"]}</p><ul class="vt-checks vt-mt-s">{puntos}</ul>'
    derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"])
    return c.bloque_dos(numero, "Pago", "vt-h-pago", p["titulo"], izquierda, derecha, id_seccion="mensualidades")


def _cobertura(k, numero):
    co = k["cobertura"]
    return c.bloque(numero, "Cobertura", "vt-h-cobertura", co["titulo"],
                    c.cobertura(co["zonas"], co["por_proyecto"], co.get("sectores", ())), lede=co["lede"])


def _relacionados(k, numero):
    r = k["relacionados"]
    return c.bloque(numero, "Relacionados", "vt-h-rel", r["titulo"], c.relacionados(r["items"]), tinte=True)


def render(k):
    tipo = k["tipo"]
    g, f, ci, p = k["garantia"], k["faq"], k["cierre"], k["proceso"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), _prueba(k, 1)]
    numero = 2
    for clave, armar in (("precio", _precio), ("objecion", _objecion)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]))
    secciones.append(c.garantia(dict(g, numero=numero + 1, id_titulo="vt-h-garantia", rotulo="Garantía")))
    secciones.append(_pago(k, numero + 2))
    secciones.append(c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    numero += 4
    for clave, armar in (("cobertura", _cobertura), ("relacionados", _relacionados)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))

    j = k["jsonld"]
    pasos_howto = tuple((x["titulo"], x["texto"]) for x in p["pasos"])
    grafo = [j["producto"], c.faq_jsonld(f["preguntas"]), c.howto(j["howto"], pasos_howto), j["migas"],
             {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k))
