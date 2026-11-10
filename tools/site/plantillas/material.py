"""Plantilla de material (spec §3.3): ruta visible → H1 con el precio por presentación en la etiqueta (costal / m³ /
camión, o "según cotización") y CTA con la plantilla de la página → qué es (con las fotos de main) → precio por
presentación → usos → calculadora de cantidad (la de main, como función pura) → entrega (recoger o a domicilio, costo
según la colonia, anticipo y factura) → galería (tierra negra) → opiniones (tierra negra y piedra bola: reales, con
permiso del dueño, solo texto, sin calificación en el JSON-LD) → preguntas → combinaciones e instalación (tezontle y
mármol) → CTA final (con la foto de fondo de main) → otros materiales → pedido por correo (el formulario de main). Las
cuatro páginas siguen ese orden; el mármol pone los otros materiales antes del CTA final porque sus miniaturas van
antes de la foto del cierre en main y el orden de las fotos de main no cambia (regla del dueño; "antes_del_cierre").
Páginas: /tierra-negra-vegetal-tampico, /tezontle-rojo-tampico, /marmol-blanco-tampico y /piedra-bola-rio-tampico
(tools/site/contenido/). <body class="vt-pagina vt-materiales">: el shell agrega terra-materiales.css."""
import componentes as c
import componentes_materiales as cm
from plantillas import base

CONTEXTO = "https://schema.org"
CLASE_BODY = "vt-pagina vt-materiales"
# vt-b2b.js valida el formulario de pedido y manda su generate_lead (el mismo del formulario de empresas).
SCRIPTS = ("/js/vt-materiales.js", "/js/vt-b2b.js")


class _Numero:
    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return self.n


def _que_es(k, n):
    q = k["que_es"]
    cuerpo = "".join(f"<p>{x}</p>" for x in q["parrafos"])
    if q.get("subtitulo"):
        cuerpo = f'<h3>{q["subtitulo"]}</h3>' + cuerpo
    if q.get("puntos"):
        cuerpo += '<ul class="vt-checks vt-mt">' + "".join(f"<li><span>{x}</span></li>" for x in q["puntos"]) + "</ul>"
    if q.get("figuras"):
        cuerpo += c.obras(q["figuras"])
    return c.bloque(n(), "Qué es", "vt-h-que", q["titulo"], cuerpo, lede=q.get("lede"))


def _precio(k, n):
    p = k["precio"]
    cuerpo = cm.presentaciones(p["filas"], p["caption"])
    if p.get("figura"):
        cuerpo = f'<div class="vt-dos"><div>{c.figura(p["figura"])}</div><div>{cuerpo}</div></div>'
    if p.get("nota"):
        cuerpo += f'<p class="vt-promesa">{p["nota"]}</p>'
    for t in p.get("tablas", ()):
        cuerpo += f'<h3 class="vt-mt">{t["titulo"]}</h3>' + c.tabla_comparativa(t["columnas"], t["filas"], t["caption"])
    return c.bloque(n(), "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p.get("lede"), tinte=True,
                    id_seccion="precio")


def _usos(k, n):
    u = k["usos"]
    return c.bloque(n(), "Usos", "vt-h-usos", u["titulo"], c.fichas(u["items"]), lede=u.get("lede"))


def _calculadora(k, n):
    ca = k["calculadora"]
    cuerpo = cm.calculadora(k["prefijo"], k["tipo"], ca["clave"], k["portada"]["mensaje"], ca["nombre"])
    return c.bloque(n(), "Calculadora", "vt-h-calc", ca["titulo"], cuerpo, lede=ca["lede"], tinte=True,
                    id_seccion="calculadora")


def _entrega(k, n):
    e = k["entrega"]
    return c.bloque(n(), "Entrega", "vt-h-entrega", e["titulo"], c.fichas(e["items"]), lede=e.get("lede"),
                    id_seccion="entrega")


def _extra(k, n, clave):
    x = k[clave]
    if clave == "instalacion":
        cuerpo = c.pasos(x["pasos"]) + (f'<p class="vt-promesa">{x["nota"]}</p>' if x.get("nota") else "")
        return c.bloque(n(), "Instalación", "vt-h-instalacion", x["titulo"], cuerpo, lede=x.get("lede"), tinte=True)
    if clave == "galeria":
        return c.bloque(n(), "Fotos", "vt-h-galeria", x["titulo"], c.obras(x["figuras"]), lede=x.get("lede"))
    if clave == "opiniones":
        return c.bloque(n(), "Opiniones", "vt-h-opiniones", x["titulo"], c.testimonios(x["items"]), lede=x.get("lede"))
    # Tras las preguntas (con tinte): combinaciones sin tinte e instalación con tinte, para que no se junten dos iguales.
    return c.bloque(n(), "Combinaciones", "vt-h-combina", x["titulo"], c.fichas(x["items"]), lede=x.get("lede"))


def _otros(k, n):
    o = k["otros"]
    return c.bloque(n(), "Materiales", "vt-h-otros", o["titulo"], cm.otros(o["items"], o.get("enlaces", ())))


def _pedido(k, n):
    f = k["pedido"]
    form = cm.formulario_pedido(k["prefijo"], f"{k['tipo']}:formulario", f["ejemplo"], f["aviso"])
    return c.bloque(n(), "Por correo", "vt-h-correo", f["titulo"], form, lede=f["lede"], id_seccion="solicitar-pedido")


def pagina_ld(url, negocio):
    """WebPage de la página ligado por @id a la entidad única #negocio (como plantillas/hub_categoria.pagina_ld)."""
    return {"@type": "WebPage", "@id": url, "url": url, "about": negocio, "publisher": negocio}


def render(k):
    tipo, n = k["tipo"], _Numero()
    secciones = [cm.portada(k["portada"], tipo, k["migas"])]
    if k.get("que_es"):
        secciones.append(_que_es(k, n))
    secciones += [_precio(k, n), _usos(k, n), _calculadora(k, n), _entrega(k, n)]
    secciones += [_extra(k, n, clave) for clave in ("galeria", "opiniones") if k.get(clave)]
    f = k["faq"]
    secciones.append(c.bloque_dos(n(), "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    secciones += [_extra(k, n, clave) for clave in ("combinaciones", "instalacion") if k.get(clave)]
    ci = k["cierre"]
    cierre = cm.cierre(ci, k["portada"]["mensaje"], tipo)
    otros = _otros(k, n)
    secciones += [otros, cierre] if k["otros"].get("antes_del_cierre") else [cierre, otros]
    secciones.append(_pedido(k, n))
    j = k["jsonld"]
    grafo = [pagina_ld(k["meta"]["canonical"], j["negocio"])]
    grafo += [j["producto"]] if j.get("producto") else []
    grafo += [c.faq_jsonld(f["preguntas"]), j["migas"]]
    if k.get("instalacion") and k["instalacion"].get("howto"):
        grafo.append(c.howto(k["instalacion"]["howto"], [(p["titulo"], p["texto"]) for p in k["instalacion"]["pasos"]]))
    grafo.append({"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])})
    precargas = (base.precarga_imagen(k["portada"]["foto"]),) if k["portada"].get("foto") else ()
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=precargas, scripts=SCRIPTS, clase_body=CLASE_BODY)
