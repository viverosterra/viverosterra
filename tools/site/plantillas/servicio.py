"""Plantilla de servicio local (spec §3.3): ruta visible → H1 con beneficio y lugar → precio ancla en la etiqueta → CTA
con plantilla y promesa → prueba (cuadro de datos, fotos FIG., nota de campo, opinión con nombre y clientes) → precio con
Medidor → objeción principal → proceso NOSOTROS / TÚ (también es el HowTo del JSON-LD) → garantía con condiciones →
pago (anticipo y mensualidades con tarjeta de crédito, con su simulador) → preguntas → cobertura → relacionados → CTA
final. Las secciones que el contenido no trae se omiten (diseño, mantenimiento y riego no llevan Medidor de pasto).
Opcionales desde 2b: formas de contratar (máx. 3, cada una con su mensaje), tabla comparativa de precios, cotizador de
la tienda (tienda-pasto.js, con lista de cotización y barra de compra), visita al showroom y pago sin simulador (con
los plazos de mensualidades). Desde 2c: planes con precio cerrado, "por cotización" o sin precio y con línea de
mensualidades, tabla comparativa bajo los planes, "qué incluye" en tarjetas, objeción con una sola tabla y garantía
sin cifra. Páginas: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py), /pasto-sintetico-tampico
(contenido/sintetico_tampico.py), /diseno-jardines-tampico (contenido/diseno_jardines.py),
/mantenimiento-jardines-tampico (contenido/mantenimiento_jardines.py) y /sistema-riego-tampico
(contenido/sistema_riego.py)."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor, el simulador y el cotizador); cada uno solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return (("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ())
            + (("/js/tienda-pasto.js",) if "cotizador" in k else ())
            + (("/js/vt-simulador.js",) if k["pago"].get("sim") else ()))


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
    if "tabla" in p:
        cuerpo = c.tabla_comparativa(p["tabla"]["columnas"], p["tabla"]["filas"], p["caption"])
    else:
        cuerpo = c.tabla_precios(p["filas"], p["caption"], concepto="Forma de compra")
    if p.get("titulo_medidor"):
        cuerpo += f'<h3 class="vt-mt">{p["titulo_medidor"]}</h3>' + c.medidor(k["prefijo"], k["tipo"], mensaje=k["portada"]["mensaje"])
    return c.bloque(numero, "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p["lede"], tinte=True, id_seccion="precio")


def _opciones(k, numero):
    """Formas de contratar o planes (máx. 3), cada uno con su mensaje; opcionales: tabla comparativa y nota debajo."""
    o = k["opciones"]
    cuerpo = c.opciones(o["items"], k["tipo"])
    if o.get("tabla"):
        tb = o["tabla"]
        tabla = c.tabla_comparativa(tb["columnas"], tb["filas"], tb["caption"])
        if tb.get("plegable"):
            # Cerrada en celular para acortar la página; terra.js la abre desde 768 px (data-vt-plegable).
            cuerpo += (f'<details class="vt-plegable vt-mt" data-vt-plegable><summary class="vt-plegable__resumen">'
                       f'<h3>{tb["titulo"]}</h3></summary>{tabla}</details>')
        else:
            cuerpo += f'<h3 class="vt-mt">{tb["titulo"]}</h3>' + tabla
    if o.get("nota"):
        cuerpo += f'<p class="vt-promesa">{o["nota"]}</p>'
    return c.bloque(numero, o.get("rotulo", "Opciones"), "vt-h-opciones", o["titulo"], cuerpo, lede=o.get("lede"),
                    id_seccion="opciones")


def _incluye(k, numero):
    """Qué incluye el servicio, en tarjetas sin precio (mantenimiento: lo que se hace en cada visita)."""
    i = k["incluye"]
    return c.bloque(numero, "Qué incluye", "vt-h-incluye", i["titulo"], c.fichas(i["items"]), lede=i.get("lede"))


def _aparte(items):
    """Columna junto al cotizador: (título, puntos, nota) por bloque."""
    salida = []
    for i, (titulo, puntos, nota) in enumerate(items):
        clase = ' class="vt-mt"' if i else ""
        lista = "".join(f"<li><span>{x}</span></li>" for x in puntos)
        salida.append(f"<h3{clase}>{titulo}</h3>" + (f'<ul class="vt-checks vt-mt-s">{lista}</ul>' if lista else "")
                      + f'<p class="vt-promesa">{nota}</p>')
    return "".join(salida)


def _cotizador(k, numero):
    q = k["cotizador"]
    modelo = t.modelo(q["modelo"])
    calculadora = t.cotizador(modelo, modelos=t.data.MODELOS, m2=q["m2"], showroom=True, local=q.get("local", False),
                              nivel=3, titulo=q["titulo_calc"], tipo=k["tipo"])
    cuerpo = f'<div class="vt-dos">{calculadora}<div>{_aparte(q["aparte"])}</div></div>'
    return c.bloque(numero, "Calculadora", "vt-h-cotizador", q["titulo"], cuerpo, tinte=True, id_seccion="cotizador")


def _visita(k, numero):
    v = k["visita"]
    enlaces = "".join(f'<a class="vt-btn vt-btn--linea" href="{c.esc(h)}" target="_blank" rel="noopener">{x}</a>'
                      for x, h in v["mapas"])
    cuerpo = f'{c.cuadro_datos(v["datos"])}<div class="vt-cta vt-mt-s">{enlaces}{c.boton_tel(k["tipo"] + ":visita")}</div>'
    return c.bloque(numero, "Showroom", "vt-h-visita", v["titulo"], cuerpo, lede=v.get("lede"), id_seccion="showroom")


def _objecion(k, numero):
    """La objeción principal en una tabla con su cierre; una segunda tabla es opcional (pasto en rollo trae dos)."""
    o = k["objecion"]
    a = o["comparativa"]
    cuerpo = c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
    if o.get("comparativa_2"):
        b = o["comparativa_2"]
        cuerpo += f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"])
    return c.bloque(numero, o.get("rotulo", "Cuál te conviene"), "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])


def _pago(k, numero):
    """Un solo bloque de pago: anticipo, contado y mensualidades en tres renglones, y el simulador (los plazos y montos
    mínimos los muestra el propio simulador, sin repetir la tabla de planes)."""
    p = k["pago"]
    puntos = "".join(f"<li><span>{t}</span></li>" for t in p["puntos"])
    izquierda = f'<p class="vt-lede">{p["lede"]}</p><ul class="vt-checks vt-mt-s">{puntos}</ul>'
    if p.get("sim"):
        derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"])
    else:
        derecha = c.planes_mensualidades()
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
    for clave, armar in (("opciones", _opciones), ("incluye", _incluye), ("precio", _precio), ("cotizador", _cotizador),
                         ("objecion", _objecion)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]))
    secciones.append(c.garantia(dict(g, numero=numero + 1, id_titulo="vt-h-garantia", rotulo="Garantía")))
    secciones.append(_pago(k, numero + 2))
    secciones.append(c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    numero += 4
    for clave, armar in (("visita", _visita), ("cobertura", _cobertura), ("relacionados", _relacionados)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))

    j = k["jsonld"]
    pasos_howto = tuple((x["titulo"], x["texto"]) for x in p["pasos"])
    # HowTo y SpeakableSpecification solo si el contenido los pide (pasto en rollo sí; sintético en Tampico no).
    howto = [c.howto(j["howto"], pasos_howto)] if j.get("howto") else []
    speakable = [{"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}] if j.get("speakable") else []
    grafo = [j["producto"], *j.get("nodos", ()), c.faq_jsonld(f["preguntas"]), *howto, j["migas"], *speakable]
    tienda = "cotizador" in k
    fuera = ""
    if tienda:
        b = k["barra"]
        fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], ci["mensaje"])
    return base.documento(k["meta"], (t.subnav() if tienda else "") + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k),
                          head_extra=(t.json_modelos(),) if tienda else (), tras_main=fuera,
                          clase_body="vt-pagina vt-tienda" if tienda else "vt-pagina")
