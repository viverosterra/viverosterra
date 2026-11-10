"""Plantilla de guía de la tienda: envío a una ciudad (/pasto-sintetico/envio/<ciudad>) y pasto para perros.

Ciudad (spec §3.3): respuesta directa con precio puesto y días → tabla 25/50/100 m² con la mensualidad más larga →
encabezados en pregunta (costo, tiempo, mínimo, cómo elegir sin muestra, instalación) → modelos → cómo llega →
preguntas → CTA. Perros: respuesta directa → criterios → modelos → preguntas → CTA. El orden de las secciones lo da el
contenido (k["secciones"]). Sin cotizador en la página: el CTA lleva al de la tienda con el estado elegido y a
WhatsApp; la barra móvil del shell queda (paginas.py). Contenido: contenido/ciudad.py y contenido/perros.py."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js")


def _portada(k):
    """El hero de marca común: la respuesta directa es el lede; la ciudad lleva su precio puesto en la etiqueta."""
    p = k["portada"]
    portada = dict(p, lede=p["respuesta"], enlaces=((p["texto_modelos"], p["href_modelos"]),))
    return c.portada(portada, k["tipo"], k["migas"], datos_html=c.cuadro_datos(p["datos"]), clase="vt-portada-t")


def _cuerpo(s):
    tipo = s["tipo"]
    if tipo == "totales":
        return t.tabla_totales(s["modelo"], s["zona"]) + "".join(f'<p class="vt-promesa">{n}</p>' for n in s["notas"])
    if tipo == "preguntas":
        return t.preguntas_h3(s["items"])
    if tipo == "modelos":
        return t.modelos_recomendados(s["items"], s.get("zona"), s.get("lugar", ""), s.get("estado", ""))
    if tipo == "pasos":
        return c.pasos(s["items"])
    if tipo == "faq":
        return c.faq(s["preguntas"]) + "".join(f'<p class="vt-promesa">{n}</p>' for n in s.get("notas", ()))
    raise ValueError(f"Sección desconocida: {tipo}")


def render(k):
    secciones = [_portada(k)]
    for n, s in enumerate(k["secciones"], 1):
        secciones.append(c.bloque(n, s["rotulo"], f"vt-h-{s['id']}", s["titulo"], _cuerpo(s), lede=s.get("lede"),
                                  tinte=n % 2 == 0, id_seccion=s["id"]))
    ci = k["cierre"]
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]))
    faq = next(s["preguntas"] for s in k["secciones"] if s["tipo"] == "faq")
    grafo = list(k["jsonld"]) + [c.faq_jsonld(faq)]
    return base.documento(base.meta_de(k), t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(), t.SCRIPT_PRECIO_PUESTO), tras_main=t.lista_y_aviso(),
                          scripts=SCRIPTS, clase_body="vt-pagina vt-tienda")
