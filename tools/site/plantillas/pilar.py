"""Plantilla de página pilar o de entidad (SEO fase 2a, 2026-11-11): ruta visible → hero de marca (componentes.portada)
→ «En corto» (respuesta directa) → secciones numeradas armadas solo con componentes que el sitio ya usa (fichas,
tarjetas, clientes con REPSE, cuadro de datos y cobertura), cada una con su fila de WhatsApp opcional → preguntas (con
su FAQPage) → CTA final. Páginas: /empresas (contenido/empresas.py), /nosotros (contenido/nosotros.py), /zonas
(contenido/zonas.py) y, desde la fase 2b, /vivero-tampico (contenido/vivero.py). Sin hoja propia: todo sale de terra.css
(k["clase_body"], opcional, suma la hoja de una familia: /vivero-tampico conserva la de las utilitarias para su etiqueta).

k["secciones"]: tuple de dicts con clase ("fichas", "tarjetas", "clientes", "datos" o "cobertura"), rotulo, id (del
<h2>), titulo y, opcionales, lede, ancla (id de la sección), cta (mensaje, texto) y momento (banda oscura a media
página, componentes.momento). k["jsonld"]["nodos"]: los nodos propios del @graph (Service, AboutPage, CollectionPage…);
el BreadcrumbList sale de las migas visibles y el WebPage lo cierra entidad.completar.
"""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"


def _cuerpo(s):
    clase = s["clase"]
    if clase == "fichas":
        return c.fichas(s["items"])
    if clase == "tarjetas":
        return c.relacionados(s["items"])
    if clase == "clientes":
        opiniones = c.testimonios(s["opiniones"]) if s.get("opiniones") else ""
        return c.logos() + c.repse() + (f'<h3 class="vt-mt">{s["titulo_opinion"]}</h3>{opiniones}' if opiniones else "")
    if clase == "datos":
        return c.cuadro_datos(s["celdas"])
    if clase == "cobertura":
        return c.cobertura(s["zonas"], s["por_proyecto"], s.get("sectores", ()))
    raise ValueError(f"clase de sección desconocida: {clase}")


def _seccion(s, numero, tinte, tipo):
    cta = c.fila_seccion(s["cta"][0], tipo, s["id"].removeprefix("vt-h-"), s["cta"][1]) if s.get("cta") else ""
    seccion = c.bloque(numero, s["rotulo"], s["id"], s["titulo"], _cuerpo(s) + cta, lede=s.get("lede"),
                       tinte=tinte and not s.get("momento"), id_seccion=s.get("ancla"))
    return c.momento(seccion) if s.get("momento") else seccion


def render(k):
    tipo, f, ci = k["tipo"], k["faq"], k["cierre"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), c.respuesta(k.get("respuesta"))]
    numero = 1
    for numero, s in enumerate(k["secciones"], 1):
        secciones.append(_seccion(s, numero, numero % 2 == 0, tipo))
    secciones.append(c.bloque_dos(numero + 1, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"], abierta=False),
                                  tinte=(numero + 1) % 2 == 0, id_seccion="preguntas", ritmo="apoyo"))
    boton = {"texto": ci["texto"]} if ci.get("texto") else {}  # texto propio del botón (si no, el de siempre)
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo, **boton))
    j = k["jsonld"]
    migas = {"@type": "BreadcrumbList", "itemListElement": []}  # entidad.completar lo arma de las migas visibles
    speakable = [{"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}] if j.get("speakable") else []
    grafo = [*j["nodos"], c.faq_jsonld(f["preguntas"]), migas, *speakable]
    return base.documento(base.meta_de(k), "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          clase_body=k.get("clase_body", "vt-pagina"))
