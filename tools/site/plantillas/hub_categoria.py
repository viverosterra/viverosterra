"""Plantilla de hub de categoría (spec §3.3): ruta visible → H1 con precio "desde" (solo de datos.py) y CTA → filtro
por necesidad (sol/sombra, salitre, tamaño; enlaces al catálogo con el filtro puesto) → subcategorías con "desde $" →
especies con foto → tabla de precios (palmas) → "Arma tu lista" (un solo mensaje) → garantía con condiciones
→ FAQ → guías del blog → relacionados → CTA final. La usan /plantas-palmas-arboles-tampico y sus 5 subcategorías; cada
sección después de la portada es opcional según el contenido (el orden no cambia). Sin JS propio."""
import componentes as c
import componentes_plantas as cp
from contenido import plantas_comun as pc
from contenido import fotos_obra
from plantillas import base

CONTEXTO = "https://schema.org"


def pagina_ld(url):
    """WebPage de la página, ligado por @id a la entidad única #negocio de la home (sin repetir el nodo completo)."""
    return {"@type": "WebPage", "@id": url, "url": url, "about": {"@id": pc.NEGOCIO}, "publisher": {"@id": pc.NEGOCIO}}
# La portada lleva la Fig. 01; las especies siguen desde la 02 (una página nunca repite un número de figura).


def _necesidad(k, n):
    x = k["necesidad"]
    return c.bloque(n, "Por necesidad", "vt-h-necesidad", x["titulo"], cp.necesidades(x["items"], k["tipo"]),
                    lede=x["lede"], tinte=True)


def _subcategorias(k, n):
    x = k["subcategorias"]
    return c.bloque(n, "Subcategorías", "vt-h-subcategorias", x["titulo"], cp.indice_subcategorias(x["items"]),
                    lede=x.get("lede"))


def _especies(k, n):
    x = k["especies"]
    nota = f'<p class="vt-promesa">{x["nota"]}</p>' if x.get("nota") else ""
    return c.bloque(n, x.get("rotulo", "En el vivero"), x.get("id", "vt-h-especies"), x["titulo"],
                    cp.especies(x["items"], k["tipo"], primero=2) + nota, lede=x.get("lede"))


def _precios(k, n):
    x = k["precios"]
    tabla = c.tabla_especies(x["filas"], x["caption"], x["grupo"])
    return c.bloque(n, "Precios", "vt-h-precios", x["titulo"], tabla + f'<p class="vt-promesa">{x["nota"]}</p>',
                    lede=x.get("lede"), tinte=True, id_seccion="precios")


def _lista(k, n):
    x = k["lista"]
    cuerpo = (f'<p>{x["texto"]}</p><p class="vt-cta"><a class="vt-btn vt-btn--tinta" data-cta="{k["tipo"]}:catalogo" '
              f'href="{x.get("href", "/catalogo")}">Arma tu lista<span class="vt-flecha" aria-hidden="true">→</span></a></p>')
    return c.bloque(n, "Arma tu lista", "vt-h-lista", x["titulo"], cuerpo)


def _garantia(k, n):
    return c.garantia(dict(k["garantia"], numero=n, id_titulo="vt-h-garantia", rotulo="Garantía"))


def _faq(k, n):
    x = k["faq"]
    return c.bloque_dos(n, "Preguntas", "vt-h-faq", x["titulo"], "", c.faq(x["preguntas"]), tinte=True)


def _guias(k, n):
    x = k["guias"]
    return c.bloque(n, "Guías", "vt-h-guias", x["titulo"], c.guias(x["items"]))


def _relacionados(k, n):
    x = k["relacionados"]
    return c.bloque(n, "También", "vt-h-rel", x["titulo"], c.relacionados(x["items"]), tinte=True)


SECCIONES = (("necesidad", _necesidad), ("subcategorias", _subcategorias), ("especies", _especies),
             ("destacadas", lambda k, n: _especies(dict(k, especies=k["destacadas"]), n)), ("precios", _precios),
             ("lista", _lista), ("garantia", _garantia), ("faq", _faq), ("guias", _guias),
             ("relacionados", _relacionados))


def render(k):
    tipo = k["tipo"]
    secciones = [c.portada(k["portada"], tipo, k["migas"])]
    obras = fotos_obra.seccion(k["meta"]["canonical"])
    for clave, armar in SECCIONES:
        if k.get(clave):
            secciones.append(armar(k, len(secciones)))
        if clave == "destacadas" and obras:  # las fotos reales van justo después de las especies
            secciones.append(c.bloque_obras(len(secciones), obras, "\n".join(secciones)))
    ci = k["cierre"]
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))
    j = k["jsonld"]
    speakable = {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}
    grafo = [pagina_ld(k["meta"]["canonical"]), *j.get("nodos", ()), c.faq_jsonld(k["faq"]["preguntas"]), j["migas"], speakable]
    return base.documento(base.meta_de(k), "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), clase_body="vt-pagina vt-plantas",
                          imagen=base.imagen_de(k["portada"]["foto"]))
