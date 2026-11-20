"""Plantilla de hub de categoría (spec §3.3): ruta visible → H1 con precio "desde" (solo de datos.py) y CTA → filtro
por necesidad (sol/sombra, salitre, tamaño; enlaces al catálogo con el filtro puesto) → subcategorías con "desde $" →
especies con foto → tabla de precios (palmas) → "Arma tu lista" (un solo mensaje) → garantía con condiciones
→ FAQ → guías del blog → relacionados → CTA final. La usan /plantas-palmas-arboles-tampico y sus 5 subcategorías; cada
sección después de la portada es opcional según el contenido (el orden no cambia). Sin JS propio."""
import componentes as c
import componentes_plantas as cp
import datos
import mensajes_paginas as mp
from contenido import plantas_comun as pc
from contenido import fotos_obra
from plantillas import base

CONTEXTO = "https://schema.org"


def pagina_ld(url):
    """WebPage de la página, ligado por @id a la entidad única #negocio de la home (sin repetir el nodo completo)."""
    return {"@type": "WebPage", "@id": url, "url": url, "about": {"@id": pc.NEGOCIO}, "publisher": {"@id": pc.NEGOCIO}}
# La portada lleva la Fig. 01; las especies siguen desde la 02 (una página nunca repite un número de figura).

# Entrega B de experiencia: antes había 15 a 19 pantallas del celular sin CTA entre el hero y el cierre. Tras las
# especies, los precios y las preguntas (y tras el filtro por necesidad y las subcategorías, si la página los trae) va una fila de WhatsApp con el mensaje de la página y, junto a la primera, la
# prueba con cifras ya publicadas (no hay opinión propia de plantas) y la garantía de las plantas que sembramos.
CTA_TEXTO = "Cotizar mis plantas"
MAX_SIN_CTA = 6  # especies (dos por renglón en celular, ~1 pantalla por renglón) antes de partir la rejilla con un CTA


def _mensaje(k, seccion):
    """(mensaje, texto del botón) de la sección (auditoría por página, 2026-11-20: cada fila dice qué leyó la persona;
    antes las 9 filas del hub abrían el mismo mensaje). Sin entrada, el de la página y el texto de siempre."""
    base = seccion.removesuffix("-medio").replace("destacadas", "especies")
    mensaje, texto = mp.PLANTAS_SECCIONES.get(base, (k["portada"]["mensaje"], k.get("cta_texto", CTA_TEXTO)))
    if base == "especies":
        mensaje = mp.PLANTAS_ESPECIES.get(k["meta"]["canonical"].removeprefix(datos.SITIO), mensaje)
    return mensaje, texto


def _fila(k, seccion, prueba=False):
    mensaje, texto = _mensaje(k, seccion)
    fila = c.fila_seccion(mensaje, k["tipo"], seccion, texto)
    if not prueba:
        return fila
    cifras = (f"<b>{c.esc(datos.CLIENTES)}</b> clientes · <b>{c.esc(datos.VARIEDADES)}</b> variedades en el vivero · "
              f"desde {datos.DESDE}")
    garantia = c.esc(datos.GARANTIA_PLANTAS).replace("ver condiciones", '<a href="/politicas#garantia-plantas">ver condiciones</a>')
    garantia = f'<p class="vt-promesa"><b>Garantía:</b> {garantia}</p>'
    return fila + c.prueba_cta(dato=cifras) + garantia


def _necesidad(k, n):
    x = k["necesidad"]
    # La prueba social va en la primera fila de la página (auditoría por página: en el hub llegaba en la pantalla 11).
    return c.bloque(n, "Por necesidad", "vt-h-necesidad", x["titulo"], cp.necesidades(x["items"], k["tipo"]) + _fila(k, "necesidad", prueba=True),
                    lede=x["lede"], tinte=True)


def _subcategorias(k, n):
    x = k["subcategorias"]
    return c.bloque(n, "Subcategorías", "vt-h-subcategorias", x["titulo"],
                    cp.indice_subcategorias(x["items"]) + _fila(k, "subcategorias"), lede=x.get("lede"))


def _especies(k, n):
    x = k["especies"]
    nota = f'<p class="vt-promesa">{x["nota"]}</p>' if x.get("nota") else ""
    seccion = "destacadas" if k.get("_destacadas") else "especies"
    items = tuple(x["items"])
    # Una rejilla larga se parte con una fila de WhatsApp cada MAX_SIN_CTA especies (auditoría por página: partida a
    # la mitad, las 16 del hub dejaban tramos de casi 4 pantallas). El último trozo lleva la fila de la sección.
    trozos = [items[i:i + MAX_SIN_CTA] for i in range(0, len(items), MAX_SIN_CTA)]
    if len(trozos) > 1 and len(trozos[-1]) < MAX_SIN_CTA // 2:  # un resto corto se une al trozo anterior
        trozos[-2:] = [trozos[-2] + trozos[-1]]
    partes, primero = [], 2
    for i, trozo in enumerate(trozos):
        partes.append(cp.especies(trozo, k["tipo"], primero=primero) + (_fila(k, f"{seccion}-medio") if i < len(trozos) - 1 else ""))
        primero += len(trozo)
    rejilla = "".join(partes)
    prueba = not k.get("necesidad") and (seccion == "especies" or k.get("_primera"))
    return c.bloque(n, x.get("rotulo", "En el vivero"), x.get("id", "vt-h-especies"), x["titulo"],
                    rejilla + nota + _fila(k, seccion, prueba=prueba), lede=x.get("lede"))


def _precios(k, n):
    x = k["precios"]
    tabla = c.tabla_especies(x["filas"], x["caption"], x["grupo"])
    return c.bloque(n, "Precios", "vt-h-precios", x["titulo"],
                    tabla + f'<p class="vt-promesa">{x["nota"]}</p>' + _fila(k, "precios"),
                    lede=x.get("lede"), tinte=True, id_seccion="precios")


def _lista(k, n):
    x = k["lista"]
    cuerpo = (f'<p>{x["texto"]}</p><p class="vt-cta"><a class="vt-btn vt-btn--tinta" data-cta="{k["tipo"]}:catalogo" '
              f'href="{x.get("href", "/catalogo")}">Arma tu lista<span class="vt-flecha" aria-hidden="true">→</span></a></p>')
    return c.bloque(n, "Arma tu lista", "vt-h-lista", x["titulo"], cuerpo)


def _garantia(k, n):
    # Plan visual V2: la garantía de plantas (datos.GARANTIA_PLANTAS) es el momento oscuro, con su CTA.
    return c.garantia(dict(k["garantia"], numero=n, id_titulo="vt-h-garantia", rotulo="Garantía", banda=True,
                           cta_html=_fila(k, "garantia")))


def _faq(k, n):
    x = k["faq"]
    return c.bloque_dos(n, "Preguntas", "vt-h-faq", x["titulo"], "", c.faq(x["preguntas"]) + _fila(k, "faq"), tinte=True)


def _guias(k, n):
    x = k["guias"]
    return c.bloque(n, "Guías", "vt-h-guias", x["titulo"], c.guias(x["items"]))


def _relacionados(k, n):
    x = k["relacionados"]
    # En celular, una junto a otra con desplazamiento horizontal (auditoría por página: apiladas eran ~3 pantallas
    # sin botón antes del cierre del hub).
    return c.bloque(n, "También", "vt-h-rel", x["titulo"], c.relacionados(x["items"], fila=True), tinte=True)


SECCIONES = (("necesidad", _necesidad), ("subcategorias", _subcategorias), ("especies", _especies),
             ("destacadas", lambda k, n: _especies(dict(k, especies=k["destacadas"], _destacadas=True, _primera=not k.get("especies")), n)), ("precios", _precios),
             ("lista", _lista), ("garantia", _garantia), ("faq", _faq), ("guias", _guias),
             ("relacionados", _relacionados))


def _con_fila(seccion, fila):
    """La fila de WhatsApp al final del contenido de una sección (antes del cierre de su .vt-wrap)."""
    fin = "</div></section>"
    if not seccion.endswith(fin):
        raise ValueError("sección sin el cierre esperado")
    return seccion[:-len(fin)] + fila + fin


def render(k):
    tipo = k["tipo"]
    secciones = [c.portada(k["portada"], tipo, k["migas"])]
    obras = fotos_obra.seccion(k["meta"]["canonical"])
    for clave, armar in SECCIONES:
        if k.get(clave):
            secciones.append(armar(k, len(secciones)))
        if clave == "destacadas" and obras:  # las fotos reales van justo después de las especies
            # Con su fila de WhatsApp (auditoría por página: tras las fotos venían hasta 3.7 pantallas sin botón).
            secciones.append(_con_fila(c.bloque_obras(len(secciones), obras, "\n".join(secciones)), _fila(k, "obras")))
    ci = k["cierre"]
    boton = {"texto": ci["texto"]} if ci.get("texto") else {}
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo, **boton))
    j = k["jsonld"]
    speakable = {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}
    grafo = [pagina_ld(k["meta"]["canonical"]), *j.get("nodos", ()), c.faq_jsonld(k["faq"]["preguntas"]), j["migas"], speakable]
    return base.documento(base.meta_de(k), "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), clase_body="vt-pagina vt-plantas",
                          imagen=base.imagen_de(k["portada"]["foto"]))
