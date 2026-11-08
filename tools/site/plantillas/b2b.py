"""Plantilla para empresas (spec §3.3, B2B): ruta visible → H1 por segmento con el precio por volumen y su mínimo en la
etiqueta → CTA con la plantilla de compras y la promesa → clientes con nombre y logo, REPSE verificable y fotos FIG. →
escalas, capacidad y tiempos con su cotizador (pasto por volumen o armador de palmas) → cotización por correo para
compras (respuesta del dueño, 2026-11-08: además de WhatsApp; el cotizador le prellena m² o la lista) → documentación (CFDI, REPSE,
anticipo y avances, entregas) → paquetes por obra (máx. 3, cada uno con su mensaje) → proceso NOSOTROS / TÚ → garantía
con condiciones → preguntas de compras → cobertura → otras páginas para empresas → CTA final. Sin ficha descargable:
no hay un PDF real (spec §3.3). Páginas: /mayoreo-pasto-tampico (contenido/mayoreo_pasto.py) y
/palmas-mayoreo-proyectos (contenido/palmas_proyectos.py); la página /empresas de la Etapa 3 reutiliza
contenido/b2b_comun.py."""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"
COTIZADORES = {"volumen": c.cotizador_volumen, "palmas": c.armador_palmas}
# vt-b2b.js calcula el volumen con VTMedidor.calcular: vt-medidor.js va antes (sin [data-vt-medidor] no hace nada más).
SCRIPTS = {"volumen": ("/js/vt-medidor.js", "/js/vt-b2b.js"), "palmas": ("/js/vt-b2b.js",)}


def _prueba(k, numero):
    pr = k["prueba"]
    cuerpo = c.logos() + c.repse() + c.obras(pr["figuras"], c.nota(*pr["nota"]))
    if pr.get("opiniones"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_opinion"]}</h3>' + c.testimonios(pr["opiniones"])
    return c.bloque(numero, "Clientes", "vt-h-prueba", pr["titulo"], cuerpo, lede=pr["lede"])


def _escalas(k, numero):
    e = k["escalas"]
    cotizador = COTIZADORES[e["cotizador"]](k["prefijo"], k["tipo"], k["portada"]["mensaje"])
    cuerpo = (c.tabla_comparativa(e["columnas"], e["filas"], e["caption"])
              + f'<h3 class="vt-mt">{e["titulo_cotizador"]}</h3>{cotizador}')
    return c.bloque(numero, "Precio por volumen", "vt-h-precio", e["titulo"], cuerpo, lede=e["lede"], tinte=True,
                    id_seccion="precio")


def _correo(k, numero):
    f = k["formulario"]
    return c.bloque(numero, "Por correo", "vt-h-correo", f["titulo"], c.formulario_correo(k["prefijo"], f),
                    lede=f["lede"], id_seccion="cotizacion-correo")


def _documentacion(k, numero):
    d = k["documentacion"]
    return c.bloque(numero, "Documentación", "vt-h-docs", d["titulo"], c.fichas(d["items"]), lede=d.get("lede"),
                    id_seccion="documentacion")


def _paquetes(k, numero):
    p = k["paquetes"]
    cuerpo = c.opciones(p["items"], k["tipo"]) + (f'<p class="vt-promesa">{p["nota"]}</p>' if p.get("nota") else "")
    return c.bloque(numero, "Paquetes por obra", "vt-h-opciones", p["titulo"], cuerpo, lede=p.get("lede"),
                    id_seccion="paquetes")


def _cobertura(k, numero):
    co = k["cobertura"]
    return c.bloque(numero, "Cobertura", "vt-h-cobertura", co["titulo"],
                    c.cobertura(co["zonas"], co["por_proyecto"], co.get("sectores", ())), lede=co["lede"])


def render(k):
    tipo = k["tipo"]
    p, g, f, r, ci = k["proceso"], k["garantia"], k["faq"], k["relacionados"], k["cierre"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), _prueba(k, 1), _escalas(k, 2), _correo(k, 3),
                 _documentacion(k, 4), _paquetes(k, 5),
                 c.bloque(6, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]),
                 c.garantia(dict(g, numero=7, id_titulo="vt-h-garantia", rotulo="Garantía")),
                 c.bloque_dos(8, "Preguntas de compras", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True),
                 _cobertura(k, 9),
                 c.bloque(10, "Para empresas", "vt-h-rel", r["titulo"], c.relacionados(r["items"]), tinte=True),
                 c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo)]
    j = k["jsonld"]
    speakable = [{"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    grafo = [j["producto"], *j.get("nodos", ()), c.faq_jsonld(f["preguntas"]), j["migas"], *speakable]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          scripts=SCRIPTS[k["escalas"]["cotizador"]])
