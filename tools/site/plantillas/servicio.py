"""Plantilla de servicio local (spec §3.3): ruta visible → H1 con beneficio y lugar → precio ancla en la etiqueta → CTA
con plantilla y promesa → prueba (cuadro de datos, fotos FIG. y nota de campo) → precio con Medidor → objeción
principal → proceso NOSOTROS / TÚ → garantía con condiciones → pago (anticipo y mensualidades con tarjeta de crédito)
→ preguntas → CTA final → relacionados y zonas. Las secciones que el contenido no trae se omiten (diseño, mantenimiento
y riego no llevan Medidor de pasto). Primera página: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py)."""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor y el simulador); el Medidor solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return ("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ()) + ("/js/vt-simulador.js",)


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
    p = k["pago"]
    derecha = (f'<h3>{p["titulo_compra"]}</h3>' + c.pasos_compra(p["compra"]) + c.planes_mensualidades()
               + f'<h3 class="vt-mt">{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"]))
    return c.bloque_dos(numero, "Pago", "vt-h-pago", p["titulo"], f'<p class="vt-lede">{p["lede"]}</p>', derecha,
                        id_seccion="mensualidades")


def _relacionados(k, numero):
    r = k["relacionados"]
    return c.bloque(numero, "Relacionados", "vt-h-rel", r["titulo"],
                    c.relacionados(r["items"]) + f'<p class="vt-promesa">{r["zonas"]}</p>')


def render(k):
    tipo = k["tipo"]
    pr, g, f, ci = k["prueba"], k["garantia"], k["faq"], k["cierre"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]),
                 c.bloque(1, "Prueba", "vt-h-prueba", pr["titulo"], c.obras(pr["figuras"], c.nota(*pr["nota"])),
                          lede=pr["lede"])]
    numero = 2
    for clave, armar in (("precio", _precio), ("objecion", _objecion)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    p = k["proceso"]
    secciones.append(c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]))
    secciones.append(c.garantia(dict(g, numero=numero + 1, id_titulo="vt-h-garantia", rotulo="Garantía")))
    secciones.append(_pago(k, numero + 2))
    secciones.append(c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))
    secciones.append(_relacionados(k, numero + 4))

    j = k["jsonld"]
    grafo = [j["producto"], c.faq_jsonld(f["preguntas"]), c.howto(j["howto"], k["pago"]["compra"]), j["migas"],
             {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k))
