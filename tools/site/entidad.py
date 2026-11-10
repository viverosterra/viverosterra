"""Entidad única del sitio para el JSON-LD (SEO fase 1, 2026-11-10): el negocio (`/#negocio`) y el sitio (`/#sitio`).

Un solo lugar define el nodo del negocio. El nodo completo (`negocio()`) sale en la home y en /vivero-tampico; las demás
páginas llevan el nodo mínimo (`negocio_minimo()`) dentro de su @graph y lo nombran por @id (`REF`). Todo sale de
datos.py: `sameAs` son todas las redes de datos.REDES más el perfil de Google Maps, nunca una lista escrita a mano. Sin
aggregateRating ni review (Google no acepta reseñas que el negocio publica de sí mismo) y sin paymentAccepted (datos.py
no lista las formas de pago).

`completar()` cierra el grafo de cada página (lo llama plantillas/base.documento, por donde pasan todas): le pone un
WebPage ligado al sitio y al negocio, cuelga de él el `speakable` (ya no va suelto en el @graph ni en el FAQPage) y la
fecha de actualización, y define en la misma página todo @id del negocio o del sitio que se nombre. `meta_social()`
completa Open Graph y Twitter Card en las páginas indexables.
"""
import datos

NEGOCIO_ID = f"{datos.SITIO}/#negocio"
SITIO_ID = f"{datos.SITIO}/#sitio"
REF = {"@id": NEGOCIO_ID}
REF_SITIO = {"@id": SITIO_ID}
# GardenStore es el subtipo exacto (vivero); LocalBusiness se conserva porque lo leen las capturas de paridad y las
# pruebas de las páginas que ya lo publicaban (GardenStore es, además, un LocalBusiness).
TIPO = ["GardenStore", "LocalBusiness"]
URL = f"{datos.SITIO}/"
IDIOMA = "es-MX"
LOGO = f"{datos.SITIO}/img/logo-viveros-terra-tampico.png"
IMAGEN = f"{datos.SITIO}/img/jardineria-areas-verdes-tampico.jpg"
CIUDADES = ("Tampico", "Ciudad Madero", "Altamira")
ESTADO = "Tamaulipas"
DESCRIPCION = (
    f"Vivero y empresa de jardinería en {datos.CIUDAD}, {ESTADO}, fundada en {datos.DESDE}. Vende e instala pasto San "
    "Agustín en rollo y pasto sintético, diseña jardines, instala riego automático, da mantenimiento a áreas verdes y "
    f"vende plantas, palmas, árboles y materiales para jardín en {CIUDADES[0]}, {CIUDADES[1]} y {CIUDADES[2]}.")
# Lo que el negocio hace y vende (cada uno tiene su página y su precio en datos.PRECIOS).
SABE_DE = (
    "Pasto San Agustín en rollo (Stenotaphrum secundatum)", "Instalación de pasto en rollo", "Pasto al mayoreo para obras",
    "Pasto sintético", "Diseño de jardines", "Sistemas de riego automático", "Mantenimiento de jardines y áreas verdes",
    "Poda de árboles y palmas", "Palmas tropicales", "Plantas de jardín y de interior", "Árboles ornamentales",
    "Tierra negra vegetal", "Tezontle rojo", "Mármol blanco", "Piedra bola de río",
)
# Selector estable de la respuesta directa de cada página (componentes.respuesta) y de las respuestas de la FAQ.
ATRIBUTO_RESPUESTA = "data-vt-respuesta"
SEL_RESPUESTA = f"[{ATRIBUTO_RESPUESTA}]"
SEL_FAQ = ".vt-faq details p"
SPEAKABLE = (SEL_RESPUESTA, SEL_FAQ)
TIPOS_PAGINA = ("WebPage", "CollectionPage", "ItemPage", "AboutPage", "ContactPage")
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
         "diciembre")


def mes_largo(iso):
    """"2026-11-10" → "noviembre de 2026" (la fecha visible de las páginas de precio)."""
    anio, mes = iso[:7].split("-")
    return f"{MESES[int(mes) - 1]} de {anio}"


def same_as():
    """Todas las redes oficiales de datos.REDES y el perfil de Google Maps."""
    return [url for _nombre, url in datos.REDES] + [datos.MAPS_URL]


def negocio_minimo():
    """Nodo mínimo del negocio para el @graph de cualquier página: mismo @type, nombre y teléfono que el completo."""
    return {"@type": list(TIPO), "@id": NEGOCIO_ID, "name": datos.NOMBRE, "url": URL, "telephone": datos.TELEFONO_TEL}


def negocio():
    """Nodo completo del negocio (solo en la home y en /vivero-tampico)."""
    return {
        **negocio_minimo(),
        "alternateName": datos.NOMBRE_ALTERNO,
        "description": DESCRIPCION,
        "email": datos.CORREO_FORMULARIOS,
        "logo": LOGO,
        "image": IMAGEN,
        "foundingDate": datos.FUNDACION,
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                    "addressRegion": ESTADO, "postalCode": datos.CP, "addressCountry": "MX"},
        "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
        "hasMap": datos.MAPS_URL,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": list(dias), "opens": abre, "closes": cierra}
            for dias, abre, cierra in datos.HORARIO_LD],
        "areaServed": [{"@type": "City", "name": ciudad, "containedInPlace": {"@type": "State", "name": ESTADO}}
                       for ciudad in CIUDADES],
        "knowsAbout": list(SABE_DE),
        # Folio del REPSE (STPS) y el padrón público donde se consulta; sin fechas ni vigencias que datos.py no tiene.
        "identifier": {"@type": "PropertyValue", "propertyID": "REPSE", "name": "Registro REPSE (STPS)",
                       "value": datos.REPSE, "url": datos.REPSE_PADRON},
        "sameAs": same_as(),
    }


def sitio_minimo():
    return {"@type": "WebSite", "@id": SITIO_ID, "name": datos.NOMBRE, "url": URL}


def sitio():
    """WebSite completo (solo en la home). Sin SearchAction: el sitio no tiene buscador."""
    return {**sitio_minimo(), "alternateName": datos.NOMBRE_ALTERNO, "inLanguage": IDIOMA, "publisher": dict(REF)}


def migas_ld(items, canonical):
    """BreadcrumbList con el mismo texto que las migas visibles (componentes.migas): [(texto, href), …, (texto, None)]."""
    import componentes  # aquí y no arriba: componentes importa este módulo
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n, "name": componentes.texto_plano(texto),
         "item": (URL if href == "/" else f"{datos.SITIO}{href.rstrip('/')}") if href else canonical}
        for n, (texto, href) in enumerate(items, 1)]}


def _con_migas(nodos, migas):
    """Sustituye el BreadcrumbList del grafo por el de las migas visibles (conserva su @id si lo tenía)."""
    return [{**migas, **({"@id": n["@id"]} if "@id" in n else {})} if "BreadcrumbList" in _tipos(n) else n for n in nodos]


def _recorrer(nodo):
    if isinstance(nodo, dict):
        yield nodo
        for valor in nodo.values():
            yield from _recorrer(valor)
    elif isinstance(nodo, list):
        for valor in nodo:
            yield from _recorrer(valor)


def _tipos(nodo):
    tipo = nodo.get("@type")
    return [tipo] if isinstance(tipo, str) else list(tipo or ())


def _es_definicion(nodo):
    """Un nodo con @id y algo más que el @id (una referencia es solo {"@id": …})."""
    return "@id" in nodo and len(nodo) > 1


def _sin_speakable(nodos):
    """(nodos sin SpeakableSpecification sueltos ni `speakable` en el FAQPage, selectores que traían)."""
    selectores, limpios = [], []
    for nodo in nodos:
        if "SpeakableSpecification" in _tipos(nodo):
            selectores += list(nodo.get("cssSelector", ()))
            continue
        if "FAQPage" in _tipos(nodo) and "speakable" in nodo:
            selectores += list(nodo["speakable"].get("cssSelector", ()))
            nodo = {k: v for k, v in nodo.items() if k != "speakable"}
        limpios.append(nodo)
    return limpios, selectores


def _pagina(nodos, meta, selectores, es_articulo):
    """Completa el WebPage de la página (o lo crea) con su sitio, su tema, su fecha y sus respuestas."""
    canonical = meta["canonical"]
    indice = next((i for i, n in enumerate(nodos) if set(_tipos(n)) & set(TIPOS_PAGINA)), None)
    pagina = dict(nodos[indice]) if indice is not None else {"@type": "WebPage", "@id": canonical}
    pagina.setdefault("url", canonical)
    pagina.setdefault("name", meta["title"])
    pagina.setdefault("inLanguage", IDIOMA)
    pagina.setdefault("isPartOf", dict(REF_SITIO))
    if not es_articulo:
        pagina.setdefault("about", dict(REF))
    if meta.get("modificado"):
        pagina["dateModified"] = meta["modificado"]
    if selectores:
        pagina["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": selectores}
    if indice is None:
        return nodos + [pagina]
    return nodos[:indice] + [pagina] + nodos[indice + 1:]


def completar(bloques, meta, cuerpo="", migas=None):
    """Bloques JSON-LD de la página con el grafo cerrado: WebPage con `isPartOf` → sitio y `about` → negocio (en los
    artículos el tema es el Article, no el negocio), `speakable` dentro del WebPage (primero la respuesta directa, si
    la página la trae) y los nodos mínimos del negocio y del sitio cuando se nombran por @id sin estar definidos. Con
    `migas` (las visibles), el BreadcrumbList del grafo se arma de ellas: nunca dice otra cosa que la ruta que se ve."""
    bloques = [dict(b) for b in bloques]
    if migas:
        ld = migas_ld(migas, meta["canonical"])
        bloques = [{**b, "@graph": _con_migas(b["@graph"], ld)} if "@graph" in b else b for b in bloques]
    con_grafo = next((b for b in bloques if "@graph" in b), None)
    if con_grafo is None:
        con_grafo = {"@context": "https://schema.org", "@graph": []}
        bloques.append(con_grafo)
    selectores = []
    for bloque in bloques:
        if "@graph" in bloque:
            bloque["@graph"], encontrados = _sin_speakable(list(bloque["@graph"]))
            selectores += encontrados
    if ATRIBUTO_RESPUESTA in cuerpo and SEL_RESPUESTA not in selectores:
        selectores.insert(0, SEL_RESPUESTA)
    todos = [n for b in bloques for n in (b["@graph"] if "@graph" in b else [b])]
    es_articulo = any("Article" in _tipos(n) for n in todos)
    if any(set(_tipos(n)) & set(TIPOS_PAGINA) for n in todos if n not in con_grafo["@graph"]):
        raise ValueError(f"{meta['canonical']}: el WebPage debe ir en el bloque con @graph")
    con_grafo["@graph"] = _pagina(con_grafo["@graph"], meta, list(dict.fromkeys(selectores)), es_articulo)
    definidos = {n["@id"] for b in bloques for n in _recorrer(b) if _es_definicion(n)}
    nombrados = {n["@id"] for b in bloques for n in _recorrer(b) if "@id" in n}
    for ident, minimo in ((NEGOCIO_ID, negocio_minimo), (SITIO_ID, sitio_minimo)):
        if ident in nombrados and ident not in definidos:
            con_grafo["@graph"] = con_grafo["@graph"] + [minimo()]
    return tuple(bloques)


def meta_social(meta, imagen=None):
    """meta con Open Graph y Twitter Card completos en las páginas indexables: og:url (la canónica), og:image (solo si
    la página trae una imagen real; nunca una genérica), og:locale, og:site_name y twitter:card. Lo que la página ya
    declara no se toca."""
    if "noindex" in meta["robots"]:
        return meta
    og = list(meta["og"])
    puestas = {p for p, _v in og}
    faltan = (("og:url", meta["canonical"]), ("og:image", f"{datos.SITIO}{imagen}" if imagen else None),
              ("og:locale", "es_MX"), ("og:site_name", datos.NOMBRE))
    og += [(p, v) for p, v in faltan if v and p not in puestas]
    twitter = list(meta.get("twitter", ()))
    if "twitter:card" not in {n for n, _v in twitter}:
        con_imagen = any(p == "og:image" for p, _v in og)
        twitter.insert(0, ("twitter:card", "summary_large_image" if con_imagen else "summary"))
    return {**meta, "og": tuple(og), "twitter": tuple(twitter)}
