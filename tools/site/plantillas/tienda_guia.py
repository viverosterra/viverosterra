"""Plantilla de guía de la tienda: envío a una ciudad (/pasto-sintetico/envio/<ciudad>) y pasto para perros.

Ciudad (spec §3.3): respuesta directa con precio puesto y días → tabla 25/50/100 m² con la mensualidad más larga →
encabezados en pregunta (costo, tiempo, mínimo, cómo elegir sin muestra, instalación) → modelos → cómo llega →
preguntas → CTA. Perros: respuesta directa → criterios → modelos → preguntas → CTA. El orden de las secciones lo da el
contenido (k["secciones"]). Sin cotizador en la página: el CTA lleva al de la tienda con el estado elegido y a
WhatsApp; la barra móvil del shell queda (paginas.py). Contenido: contenido/ciudad.py y contenido/perros.py."""
import componentes as c
import componentes_rollos as cr
import datos
import componentes_tienda as t
import preguntas_wa as pw
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-folio.js", "/js/tienda-pasto.js", "/js/vt-landed.js")


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
    # Entrega B del SEO nacional (2026-11-16): /pasto-sintetico/cuantos-rollos, la única guía con cotizador.
    if tipo == "calculadora":
        return cr.calculadora()
    if tipo == "cotizar":
        return t.cotizador(s["modelo"], modelos=t.data.MODELOS, m2=s["m2"], titulo="Cotiza los m² que calculaste",
                           id_titulo="vt-h-cotizador", nivel=3, calculadora=False)
    if tipo == "medidas":
        return cr.tabla_medidas()
    if tipo == "estados":
        # Auditoría por página (2026-11-20): las tres zonas a la vista y los 32 estados plegados (antes, unas 9
        # pantallas del celular sin botón). Las 32 filas siguen en el HTML.
        return t.zonas_acordeon() + c.plegable("Flete y precio puesto en los 32 estados", cr.tabla_estados(s["modelo"]))
    # Entrega D del SEO nacional (2026-11-16): tabla de las guías (pesos por modelo, anchos, sintético contra natural).
    if tipo == "tabla":
        return c.tabla_comparativa(s["cabeza"], s["filas"], s["nota"])
    if tipo == "faq":
        return c.faq(s["preguntas"]) + "".join(f'<p class="vt-promesa">{n}</p>' for n in s.get("notas", ()))
    raise ValueError(f"Sección desconocida: {tipo}")


def _fila(k):
    """Entrega B de experiencia: tras los modelos recomendados, WhatsApp con el mensaje de la página y la prueba social
    de la tienda (la opinión real de pasto sintético y la calificación de Google con su enlace). En las ciudades no va
    la opinión: es de un cliente de Tampico (Entrega C del SEO nacional, 2026-11-16)."""
    opiniones = () if k["tipo"] == "ciudad" or k.get("sin_opinion") else datos.OPINION_SINTETICO_TAMPICO
    return (c.fila_seccion(k["cierre"]["mensaje"], k["tipo"], "modelos", "Cotizar mi pedido", contexto=True)
            + c.prueba_cta(opiniones, f"vendemos a todo México desde {datos.SINTETICO_NACIONAL_DESDE}"))


def _fila_seccion(k, s):
    """Auditoría por página (2026-11-20): WhatsApp al final de las secciones largas que no tenían botón (tablas de las
    guías, totales de la ciudad, cómo se calcula): ningún tramo de más de ~3 pantallas del celular sin botón. Lleva el
    mensaje de la página y, como las demás filas de la tienda, lo que el cliente ya eligió (data-vt-ctx)."""
    if not s.get("fila"):
        return ""
    return c.fila_seccion(k["cierre"]["mensaje"], k["tipo"], s["id"], s["fila"], contexto=True)


def render(k):
    secciones = [_portada(k)]
    for n, s in enumerate(k["secciones"], 1):
        cuerpo = (_cuerpo(s) + (c.figura(s["figura"]) if s.get("figura") else "") + _fila_seccion(k, s)
                  + (_fila(k) if s["tipo"] == "modelos" else ""))
        secciones.append(c.bloque(n, s["rotulo"], f"vt-h-{s['id']}", s["titulo"], cuerpo, lede=s.get("lede"),
                                  tinte=n % 2 == 0, id_seccion=s["id"]))
    ci = k["cierre"]
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]))
    faq = next(s["preguntas"] for s in k["secciones"] if s["tipo"] == "faq")
    grafo = list(k["jsonld"]) + [c.faq_jsonld(faq)]
    return base.documento(base.meta_de(k), t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(), t.SCRIPT_PRECIO_PUESTO, pw.json_pagina(k.get("preguntas_fijo", {}))),
                          tras_main=t.lista_y_aviso(), scripts=pw.scripts(SCRIPTS + tuple(k.get("scripts_extra", ()))),
                          clase_body="vt-pagina vt-tienda" + k.get("clase_extra", "") + pw.CLASE)
