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
(contenido/sistema_riego.py). Desde la SEO fase 2a (2026-11-11), también /poda-arboles-tampico (contenido/poda_arboles.py),
sin garantía ni pago (la poda no tiene garantía ni mensualidades en datos.py) y con rótulo propio en «qué incluye»."""
import componentes as c
import componentes_tienda as t
from contenido import fotos_obra
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor, el simulador y el cotizador); cada uno solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return (("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ())
            + (("/js/vt-folio.js", "/js/tienda-pasto.js") if "cotizador" in k else ())
            + (("/js/vt-simulador.js",) if k.get("pago", {}).get("sim") else ()))


def _cta(k, clave):
    """Fila de CTA al final de una sección larga (Entrega B de experiencia): k["ctas"][clave] = (mensaje, texto)."""
    if clave not in k.get("ctas", {}):
        return ""
    mensaje, texto = k["ctas"][clave]
    return c.fila_seccion(mensaje, k["tipo"], clave, texto)


def _prueba(k, numero, tinte=False):
    pr = k["prueba"]
    cuerpo = c.obras(pr["figuras"], c.nota(*pr["nota"]))
    if pr.get("opiniones"):
        # Entrega C: en celular las opiniones van en fila con desplazamiento horizontal (antes, apiladas: ~1.2 pantallas).
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_opinion"]}</h3>' + c.testimonios(pr["opiniones"], fila=True)
    if pr.get("titulo_clientes"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_clientes"]}</h3>' + c.logos()
    return c.bloque(numero, "Prueba", "vt-h-prueba", pr["titulo"], cuerpo + _cta(k, "prueba"), lede=pr["lede"],
                    tinte=tinte)


def _precio(k, numero, tinte):
    p = k["precio"]
    if "tabla" in p:
        cuerpo = c.tabla_comparativa(p["tabla"]["columnas"], p["tabla"]["filas"], p["caption"])
    else:
        cuerpo = c.tabla_precios(p["filas"], p["caption"], concepto="Forma de compra")
    if p.get("titulo_medidor"):
        cuerpo += f'<h3 class="vt-mt">{p["titulo_medidor"]}</h3>' + c.medidor(k["prefijo"], k["tipo"], mensaje=k["portada"]["mensaje"])
    return c.bloque(numero, "Precio", "vt-h-precio", p["titulo"], cuerpo + _cta(k, "precio"), lede=p["lede"], tinte=tinte,
                    id_seccion="precio", ritmo="clave")


def _opciones(k, numero, tinte):
    """Formas de contratar o planes (máx. 3), cada uno con su mensaje; opcionales: tabla comparativa y nota debajo."""
    o = k["opciones"]
    cuerpo = c.opciones(o["items"], k["tipo"], fila=o.get("fila", False))
    if o.get("tabla"):
        tb = o["tabla"]
        tabla = c.tabla_comparativa(tb["columnas"], tb["filas"], tb["caption"])
        if tb.get("plegable"):
            # Cerrada en celular para acortar la página; terra.js la abre desde 768 px (data-vt-plegable).
            cuerpo += c.plegable(tb["titulo"], tabla)
        else:
            cuerpo += f'<h3 class="vt-mt">{tb["titulo"]}</h3>' + tabla
    if o.get("nota"):
        cuerpo += f'<p class="vt-promesa">{o["nota"]}</p>'
    return c.bloque(numero, o.get("rotulo", "Opciones"), "vt-h-opciones", o["titulo"], cuerpo, lede=o.get("lede"),
                    id_seccion="opciones", tinte=tinte, ritmo="clave")


def _incluye(k, numero, tinte):
    """Qué incluye el servicio, en tarjetas sin precio (mantenimiento: lo que se hace en cada visita)."""
    i = k["incluye"]
    return c.bloque(numero, i.get("rotulo", "Qué incluye"), "vt-h-incluye", i["titulo"], c.fichas(i["items"]) + _cta(k, "incluye"),
                    lede=i.get("lede"), tinte=tinte)


def _aparte(items):
    """Columna junto al cotizador: (título, puntos, nota) por bloque."""
    salida = []
    for i, (titulo, puntos, nota) in enumerate(items):
        clase = ' class="vt-mt"' if i else ""
        lista = "".join(f"<li><span>{x}</span></li>" for x in puntos)
        salida.append(f"<h3{clase}>{titulo}</h3>" + (f'<ul class="vt-checks vt-mt-s">{lista}</ul>' if lista else "")
                      + f'<p class="vt-promesa">{nota}</p>')
    return "".join(salida)


def _cotizador(k, numero, tinte):
    q = k["cotizador"]
    modelo = t.modelo(q["modelo"])
    calculadora = t.cotizador(modelo, modelos=t.data.MODELOS, m2=q["m2"], showroom=True, local=q.get("local", False),
                              nivel=3, titulo=q["titulo_calc"], tipo=k["tipo"])
    cuerpo = f'<div class="vt-dos">{calculadora}<div>{_aparte(q["aparte"])}</div></div>'
    return c.bloque(numero, "Calculadora", "vt-h-cotizador", q["titulo"], cuerpo, tinte=tinte, id_seccion="cotizador",
                    ritmo="clave")


def _visita(k, numero, tinte):
    v = k["visita"]
    enlaces = "".join(f'<a class="vt-btn vt-btn--linea" href="{c.esc(h)}" target="_blank" rel="noopener">{x}</a>'
                      for x, h in v["mapas"])
    cuerpo = f'{c.cuadro_datos(v["datos"])}<div class="vt-cta vt-mt-s">{enlaces}{c.boton_tel(k["tipo"] + ":visita")}</div>'
    return c.bloque(numero, "Showroom", "vt-h-visita", v["titulo"], cuerpo, lede=v.get("lede"), id_seccion="showroom",
                    tinte=tinte, ritmo="apoyo")


def _objecion(k, numero, tinte):
    """La objeción principal en una tabla con su cierre; una segunda tabla es opcional (pasto en rollo trae dos). Entrega C
    de experiencia: una tabla que repite lo que ya dicen otras secciones de la página va plegada en celular
    (comparativa["plegable"]: título del <summary>; o["plegable_2"] para la segunda), con su cierre a la vista."""
    o = k["objecion"]
    a = o["comparativa"]
    tabla = c.tabla_comparativa(a["columnas"], a["filas"], a["caption"])
    cuerpo = (c.plegable(a["plegable"], tabla) if a.get("plegable") else tabla) + f'<p class="vt-promesa">{a["cierre"]}</p>'
    if o.get("comparativa_2"):
        b = o["comparativa_2"]
        tabla_2 = c.tabla_comparativa(b["columnas"], b["filas"], b["caption"])
        cuerpo += (c.plegable(o["titulo_2"], tabla_2) if o.get("plegable_2")
                   else f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + tabla_2)
    return c.bloque(numero, o.get("rotulo", "Cuál te conviene"), "vt-h-conviene", o["titulo"], cuerpo + _cta(k, "objecion"),
                    lede=o["lede"], tinte=tinte)


def _pago(k, numero, tinte):
    """Un solo bloque de pago: anticipo, contado y mensualidades en tres renglones, y el simulador (los plazos y montos
    mínimos los muestra el propio simulador, sin repetir la tabla de planes)."""
    p = k["pago"]
    puntos = "".join(f"<li><span>{t}</span></li>" for t in p["puntos"])
    izquierda = f'<p class="vt-lede">{p["lede"]}</p><ul class="vt-checks vt-mt-s">{puntos}</ul>'
    if p.get("sim"):
        derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"])
    else:
        derecha = c.planes_mensualidades()
    return c.bloque_dos(numero, "Pago", "vt-h-pago", p["titulo"], izquierda, derecha, id_seccion="mensualidades",
                        tinte=tinte, ritmo="apoyo")


def _cobertura(k, numero, tinte):
    co = k["cobertura"]
    return c.bloque(numero, "Cobertura", "vt-h-cobertura", co["titulo"],
                    c.cobertura(co["zonas"], co["por_proyecto"], co.get("sectores", ())), lede=co["lede"], tinte=tinte,
                    ritmo="apoyo")


def _relacionados(k, numero, tinte):
    r = k["relacionados"]
    return c.bloque(numero, "Relacionados", "vt-h-rel", r["titulo"], c.relacionados(r["items"], fila=True), tinte=tinte,
                    ritmo="apoyo")


def _proceso(k, numero, tinte):
    p = k["proceso"]
    seccion = c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]) + _cta(k, "proceso"),
                       lede=p["lede"], tinte=tinte)
    # Plan visual V2: si la garantía no es banda (no está en datos.py), el proceso es el momento oscuro de la página.
    return seccion if k.get("garantia", {}).get("banda") else c.momento(seccion)


def _garantia(k, numero, tinte):
    """Garantía con sus condiciones. Con k["garantia"]["banda"] (la garantía real de datos.py: pasto en rollo, sintético
    y diseño), banda oscura a media página con su CTA (Entrega C de experiencia); si no, sección con tinte o sin él."""
    g = k["garantia"]
    seccion = c.garantia(dict(g, numero=numero, id_titulo="vt-h-garantia", rotulo="Garantía", cta_html=_cta(k, "garantia")))
    return seccion if g.get("banda") or tinte else seccion.replace("vt-bloque vt-bloque--tinte", "vt-bloque", 1)


def _faq(k, numero, tinte):
    f = k["faq"]
    return c.bloque_dos(numero, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"], abierta=False) + _cta(k, "faq"),
                        tinte=tinte, ritmo="apoyo")


# Orden de la página después de la portada y la respuesta. "prueba" y "obras" van en hueso; las demás alternan tinte.
# Una página puede traer su propio orden en k["orden"] (Tampico, 2026-11-12: el material antes que la prueba).
ORDEN = ("prueba", "obras", "opciones", "incluye", "precio", "cotizador", "objecion", "proceso", "garantia", "pago", "faq",
         "visita", "cobertura", "relacionados")
ARMAR = {"opciones": _opciones, "incluye": _incluye, "precio": _precio, "cotizador": _cotizador, "objecion": _objecion,
         "proceso": _proceso, "garantia": _garantia, "pago": _pago, "faq": _faq, "visita": _visita,
         "cobertura": _cobertura, "relacionados": _relacionados}


def render(k):
    tipo = k["tipo"]
    f, ci, p = k["faq"], k["cierre"], k["proceso"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), c.respuesta(k.get("respuesta"))]
    numero = 1
    # Ritmo (Entrega C de experiencia): prueba y fotos de obra en hueso; las demás alternan tinte y hueso sin repetirse;
    # la banda oscura de garantía cuenta como fondo y la sección que la sigue va en hueso.
    # Si la prueba o las fotos van después de otras secciones (orden propio), entran en la alternancia.
    oscuro, en_cuerpo = False, False
    for clave in k.get("orden", ORDEN):
        tinte_prueba = en_cuerpo and not oscuro
        if clave == "prueba":
            secciones.append(_prueba(k, numero, tinte_prueba))
        elif clave == "obras":
            obras = fotos_obra.seccion(k["meta"]["canonical"])
            if not obras:
                continue
            secciones.append(c.bloque_obras(numero, obras, "\n".join(secciones), ritmo="apoyo", tinte=tinte_prueba))
        elif clave in ARMAR and clave in k:
            en_cuerpo = True
            banda = clave == "garantia" and k["garantia"].get("banda")
            tinte = not oscuro and not banda
            secciones.append(ARMAR[clave](k, numero, tinte))
            oscuro = bool(banda) or tinte
            numero += 1
            continue
        else:
            continue
        oscuro = tinte_prueba
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
    return base.documento(base.meta_de(k), (t.subnav() if tienda else "") + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k),
                          head_extra=(t.json_modelos(),) if tienda else (), tras_main=fuera,
                          clase_body="vt-pagina vt-tienda" if tienda else "vt-pagina")
