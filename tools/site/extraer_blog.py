"""Extracción, de una sola vez, de los 52 artículos del blog hechos a mano a tools/site/contenido/blog/<slug>.html (Etapa 2h).

Cada artículo publicado tiene una de tres envolturas (40 con hero en degradado y barra lateral, 8 con <article data-page>,
4 con hero claro) pero el mismo contenido: portada, respuesta directa, cuerpo, preguntas, CTA y relacionados. Aquí el HTML
se lee con html.parser (biblioteca estándar), se reduce a bloques semánticos sin clases de Tailwind, se le aplican las
correcciones documentadas de contenido/blog_correcciones.py y se escribe un archivo por artículo: un comentario con los
metadatos en JSON y, debajo, el cuerpo en HTML. Lo que no pasa al artículo (índice, CTA, barra lateral) queda anotado en
"retirado", para que tests/test_blog_paridad.py compruebe que no se perdió texto.

Uso: python3 tools/site/extraer_blog.py escribir [<slug> …]   (lee public/blog; solo se corre antes de migrar)
     python3 tools/site/extraer_blog.py informe                (cuenta variantes y lo retirado, sin escribir)
"""
import html as html_mod
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
DESTINO = AQUI / "contenido" / "blog"
VACIAS = {"img", "br", "hr", "input", "meta", "link"}
EN_LINEA = {"a", "strong", "b", "em", "i", "br", "small", "sub", "sup", "code", "span", "u", "mark"}
SE_CONSERVA_TAL_CUAL = {"strong", "em", "br", "sub", "sup"}
RENOMBRA = {"b": "strong", "i": "em"}
NOTAS = ("tip-box", "warn-box", "highlight", "calc-box")
RESPUESTA = ("answer-box", "aeo-box")
BLOQUE_EN_NOTA = {"p", "div", "ul", "ol", "li", "h3", "h4", "h5"}
# Commit de main con los artículos hechos a mano: la extracción siempre lee esa versión, no el public/ ya migrado.
REF = "db6923e"
# dateModified de los artículos cuyo texto cambió en esta etapa. None mientras el dueño no confirme que se muestre
# "Actualizado" (pregunta 12 del plan): con una fecha aquí y una nueva extracción, los corregidos la llevan.
FECHA_CORRECCION = None


class Nodo:
    def __init__(self, tag, attrs=(), padre=None):
        self.tag, self.attrs, self.padre, self.hijos = tag, dict(attrs), padre, []

    @property
    def clases(self):
        return (self.attrs.get("class") or "").split()

    def tiene(self, *clases):
        return any(c in self.clases for c in clases)

    def elementos(self):
        return [h for h in self.hijos if isinstance(h, Nodo)]

    def buscar(self, condicion):
        for h in self.elementos():
            if condicion(h):
                yield h
            yield from h.buscar(condicion)


class Lector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = self.actual = Nodo("raiz")

    def handle_starttag(self, tag, attrs):
        nodo = Nodo(tag, attrs, self.actual)
        self.actual.hijos.append(nodo)
        if tag not in VACIAS:
            self.actual = nodo

    def handle_startendtag(self, tag, attrs):
        self.actual.hijos.append(Nodo(tag, attrs, self.actual))

    def handle_endtag(self, tag):
        nodo = self.actual
        while nodo is not None and nodo.tag != tag:
            nodo = nodo.padre
        if nodo is not None and nodo.padre is not None:
            self.actual = nodo.padre

    def handle_data(self, data):
        self.actual.hijos.append(data)


def leer(fragmento):
    limpio = re.sub(r"<(script|svg|style)\b.*?</\1>", "", fragmento, flags=re.S | re.I)
    limpio = re.sub(r"<!--.*?-->", "", limpio, flags=re.S)
    lector = Lector()
    lector.feed(limpio)
    return lector.raiz


def texto(nodo):
    if isinstance(nodo, str):
        return nodo
    return " ".join(texto(h) for h in nodo.hijos)


def limpio(t):
    return re.sub(r"\s+", " ", t).strip()


def texto_limpio(nodo):
    return limpio(texto(nodo))


def en_linea(nodo):
    """HTML en línea del contenido del nodo: solo enlaces, negritas y cursivas; sin clases."""
    salida = []
    for h in nodo.hijos:
        if isinstance(h, str):
            salida.append(html_mod.escape(re.sub(r"\s+", " ", h), quote=False))
            continue
        tag = RENOMBRA.get(h.tag, h.tag)
        if tag == "a":
            href = (h.attrs.get("href") or "").replace("&", "&amp;") if "&amp;" not in (h.attrs.get("href") or "") else h.attrs["href"]
            salida.append(f'<a href="{href}">{en_linea(h)}</a>')
        elif tag == "br":
            salida.append("<br>")
        elif tag in SE_CONSERVA_TAL_CUAL:
            salida.append(f"<{tag}>{en_linea(h)}</{tag}>")
        elif tag in BLOQUE_EN_NOTA:
            salida.append(f" {en_linea(h)} ")
        else:
            salida.append(en_linea(h))
    return "".join(salida)


def inline(nodo):
    return re.sub(r"\s+", " ", en_linea(nodo)).strip()


def foto(nodo, public=PUBLIC):
    from PIL import Image
    src = nodo.attrs.get("src", "")
    src = "/" + src.lstrip("./") if not src.startswith("/") else src
    with Image.open(Path(public) / src.lstrip("/")) as im:
        ancho, alto = im.size
    return {"tipo": "foto", "src": src, "alt": nodo.attrs.get("alt", ""), "ancho": ancho, "alto": alto}


def slug_de(t):
    t = re.sub(r"[^a-z0-9áéíóúñü ]+", "", t.lower())
    t = t.translate(str.maketrans("áéíóúñü", "aeiounu")).strip()
    return re.sub(r"\s+", "-", " ".join(t.split()[:7]))


class Articulo:
    def __init__(self, slug, html, public=PUBLIC):
        self.slug, self.html, self.public = slug, html, public
        m = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S)
        self.raiz = leer(m.group(1))
        self.bloques, self.faq, self.relacionados, self.retirado, self.respuesta = [], [], [], [], None
        self.ids, self.en_faq = set(), False
        self.faq_titulo, self.rel_titulo = "Preguntas frecuentes", ""

    # ---------- portada ----------
    def h1(self):
        return next(self.raiz.buscar(lambda n: n.tag == "h1"))

    def portada(self):
        """El contenedor de la portada: el padre de <h1>, subiendo lo justo para incluir etiquetas y autor."""
        h1 = self.h1()
        return h1.padre

    def kicker(self):
        cont = self.portada()
        spans = list(cont.buscar(lambda n: n.tag == "span"))
        return texto_limpio(spans[0]) if spans else ""

    def dek(self):
        cont = self.portada()
        for h in cont.elementos():
            if h.tag == "p":
                return inline(h)
        return ""

    def minutos(self):
        m = re.search(r"(\d+) min de lectura", texto_limpio(self.portada()))
        return int(m.group(1)) if m else None

    # ---------- contenido ----------
    def raiz_contenido(self):
        return next(self.raiz.buscar(lambda n: n.tag == "article"))

    def clasificar(self, n):
        """Reparte un elemento en bloques, respuesta, preguntas, relacionados o retirado."""
        if isinstance(n, str):
            if n.strip():
                self.retirado.append(limpio(n))
            return
        t = n.tag
        if t == "section" and self.es_relacionados(n):
            self.tomar_relacionados(n)
        elif t in ("h2", "h3", "h4", "h5"):
            self.bloque_titulo(n)
        elif t == "p" and self.en_faq and self.faq and not self.faq[-1][1]:
            self.faq[-1][1] = inline(n)
        elif t == "p":
            self.bloques.append({"tipo": "p", "html": inline(n)})
        elif t in ("ul", "ol"):
            self.bloques.append({"tipo": t, "items": [inline(li) for li in n.elementos() if li.tag == "li"]})
        elif t == "table":
            self.bloques.append({"tipo": "tabla", "html": self.tabla(n)})
        elif t == "blockquote":
            self.bloques.append({"tipo": "cita", "html": inline(n)})
        elif t == "img":
            self.bloques.append(foto(n, self.public))
        elif t == "hr":
            pass
        elif t in ("nav", "aside") or n.tiene("toc"):
            self.retirar(n)
        elif self.es_cta(n) and (n.tiene("not-prose", "bg-primary", "bg-dark") or t == "section"):
            self.retirar(n)
        elif n.tiene(*RESPUESTA) or self.es_caja_respuesta(n):
            self.tomar_respuesta(n)
        elif n.tiene(*NOTAS) or (n.tiene("bg-bggreen") and n.tag == "div"):
            self.bloques.append({"tipo": "nota", "html": self.nota(n), "clase": "aviso" if n.tiene("warn-box") else "tip"})
        elif n.tiene("faq-btn"):
            pass
        elif n.tiene("faq-block"):
            self.pregunta_bloque(n)
        elif any(True for _ in n.buscar(lambda x: x.tiene("faq-btn"))) and self.es_item_faq(n):
            self.pregunta_boton(n)
        elif self.es_cta(n):
            self.retirar(n)
        else:
            for h in n.hijos:
                self.clasificar(h)

    @staticmethod
    def es_cta(n):
        """Bloque de llamada a la acción: botón de WhatsApp o enlace con forma de botón, y poco texto."""
        boton = any(True for _ in n.buscar(lambda x: x.tag == "a" and ("wa.me" in (x.attrs.get("href") or "")
                                                                         or x.tiene("rounded-full", "rounded-xl"))))
        con_ancla = any(True for _ in n.buscar(lambda x: x.tag == "article" or x.attrs.get("id")))
        return boton and not con_ancla and len(texto_limpio(n)) < 320

    @staticmethod
    def es_caja_respuesta(n):
        return n.tag == "div" and n.tiene("bg-bggreen") and n.tiene("border-primary") and n.tiene("border-l-4")

    @staticmethod
    def es_item_faq(n):
        return len(n.elementos()) >= 2 and n.elementos()[0].tag == "button"

    def tomar_respuesta(self, n):
        if self.respuesta is not None:
            self.bloques.append({"tipo": "nota", "html": self.nota(n), "clase": "tip"})
            return
        cuerpo, titulo, heading = [], "Respuesta directa", False
        for h in n.elementos():
            if h.tag in ("h2", "h3") or h.tiene("answer-box-label"):
                titulo, heading = texto_limpio(h), h.tag in ("h2", "h3")
            elif h.tag == "p":
                cuerpo.append(inline(h))
            else:
                cuerpo.append(inline(h))
        if not cuerpo:
            cuerpo = [inline(n)]
        self.respuesta = {"titulo": titulo, "es_titulo": heading, "parrafos": cuerpo}

    @staticmethod
    def nota(n):
        return inline(n)

    def bloque_titulo(self, n):
        t = texto_limpio(n)
        ident = n.attrs.get("id")
        if n.tag == "h2" and re.fullmatch(r"preguntas frecuentes", t, re.I):
            self.faq_titulo, self.en_faq = t, True
            return
        if self.en_faq and n.tag in ("h3", "h4"):
            self.faq.append([inline(n), ""])
            return
        if n.tag == "h2":
            self.en_faq = False
        if n.tag == "h2" and not ident:
            ident = slug_de(t)
            while ident in self.ids:
                ident += "-2"
        if ident:
            self.ids.add(ident)
        self.bloques.append({"tipo": n.tag, "html": inline(n), "id": ident})

    def tabla(self, n):
        filas = []
        for tr in n.buscar(lambda x: x.tag == "tr"):
            celdas = []
            for c in tr.elementos():
                extra = "".join(f' {a}="{c.attrs[a]}"' for a in ("colspan", "rowspan") if c.attrs.get(a))
                if c.tag == "th":
                    celdas.append(f'<th scope="col"{extra}>{inline(c)}</th>')
                elif c.tag == "td":
                    celdas.append(f"<td{extra}>{inline(c)}</td>")
            filas.append((tr.padre.tag, f"<tr>{''.join(celdas)}</tr>"))
        cabeza = "".join(f for p, f in filas if p == "thead")
        resto = "".join(f for p, f in filas if p != "thead")
        if cabeza:
            return f"<table><thead>{cabeza}</thead><tbody>{resto}</tbody></table>"
        return f"<table><tbody>{resto}</tbody></table>"

    def pregunta_bloque(self, n):
        q = next(h for h in n.elementos() if h.tag in ("h3", "h4", "button"))
        partes = [inline(h) for h in n.elementos() if h is not q]
        self.faq.append([inline(q), "</p><p>".join(partes)])

    def pregunta_boton(self, n):
        boton, resp = n.elementos()[0], n.elementos()[1]
        spans = [h for h in boton.elementos() if h.tag == "span"]
        q = inline(spans[0]) if spans else inline(boton)
        ps = [e for e in resp.buscar(lambda x: x.tag == "p")]
        if ps:
            a = "</p><p>".join(inline(p) for p in ps)
        else:
            a = inline(resp)
        self.faq.append([q, a])

    def retirar(self, n):
        t = texto_limpio(n)
        if t:
            self.retirado.append(t)

    def tomar_relacionados(self, n):
        titulo_h2 = next(n.buscar(lambda x: x.tag == "h2"), None)
        self.rel_titulo = texto_limpio(titulo_h2) if titulo_h2 is not None else ""
        for a in n.buscar(lambda x: x.tag == "a"):
            href = a.attrs.get("href") or ""
            self.retirar(a)  # la tarjeta vuelve con el texto que la plantilla usa; "Leer más" y "Ver todos" no
            if not (href.startswith("/") and a.tiene("group", "block")):
                continue
            spans = [e for e in a.elementos() if e.tag == "span"]
            titulo = next((e for e in a.elementos() if e.tag in ("h3", "h4")), None)
            ps = [e for e in a.elementos() if e.tag == "p"]
            self.relacionados.append({"href": href, "categoria": texto_limpio(spans[0]) if spans else "",
                                      "titulo": texto_limpio(titulo) if titulo is not None else texto_limpio(a),
                                      "texto": texto_limpio(ps[0]) if ps else ""})

    def es_relacionados(self, n):
        return n.tag == "section" and any(True for _ in n.buscar(
            lambda x: x.tag == "a" and (x.attrs.get("href") or "").startswith("/") and x.tiene("group", "block")))

    def recorrer(self):
        self.faq_titulo, self.rel_titulo = "Preguntas frecuentes", ""
        portada = self.portada()

        def bajar(n):
            if isinstance(n, str):
                return
            if n is portada:
                self.retirar(n)
                return
            if n.tag == "section" and self.es_relacionados(n):
                self.tomar_relacionados(n)
                return
            if n.tag == "nav" and n.tiene("vt-crumbs"):
                self.retirar(n)
                return
            if self.contiene(n, portada):
                for h in n.hijos:
                    bajar(h)
                return
            if n.tag == "aside":
                self.retirar(n)
                return
            self.clasificar(n)

        for h in self.raiz.hijos:
            bajar(h)

    @staticmethod
    def contiene(n, objetivo):
        return any(x is objetivo for x in n.buscar(lambda _: True))


def serializar(bloques):
    salida = []
    for b in bloques:
        t = b["tipo"]
        if t in ("h2", "h3", "h4", "h5"):
            ident = f' id="{b["id"]}"' if b.get("id") else ""
            salida.append(f"<{t}{ident}>{b['html']}</{t}>")
        elif t == "p":
            salida.append(f"<p>{b['html']}</p>")
        elif t in ("ul", "ol"):
            salida.append(f"<{t}>\n" + "\n".join(f"<li>{i}</li>" for i in b["items"]) + f"\n</{t}>")
        elif t == "tabla":
            salida.append(f'<div class="vt-art__tabla" tabindex="0" role="region" aria-label="Tabla">{b["html"]}</div>')
        elif t == "cita":
            salida.append(f"<blockquote>{b['html']}</blockquote>")
        elif t == "nota":
            salida.append(f'<aside class="vt-art__nota vt-art__nota--{b["clase"]}"><p>{b["html"]}</p></aside>')
        elif t == "foto":
            salida.append(f'<img src="{b["src"]}" width="{b["ancho"]}" height="{b["alto"]}" alt="{html_mod.escape(b["alt"])}">')
    return "\n".join(salida) + "\n"


def meta_pagina(html):
    meta = {}
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    meta["title"] = html_mod.unescape(t.group(1).strip())
    for nombre, clave in (("description", "description"), ("robots", "robots")):
        m = re.search(rf'<meta name="{nombre}" content="([^"]*)"', html)
        meta[clave] = html_mod.unescape(m.group(1)) if m else ""
    meta["canonical"] = re.search(r'<link rel="canonical" href="([^"]*)"', html).group(1)
    meta["og"] = [[p, html_mod.unescape(v)] for p, v in re.findall(r'<meta property="((?:og|article):[^"]+)" content="([^"]*)"', html)]
    meta["twitter"] = [[p, html_mod.unescape(v)] for p, v in re.findall(r'<meta name="(twitter:[^"]+)" content="([^"]*)"', html)]
    return meta


def jsonld_pagina(html):
    bloques = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return json.loads(bloques[0])


def extraer(slug, public=PUBLIC):
    html = publicado(f"blog/{slug}/index.html")
    a = Articulo(slug, html, public)
    a.recorrer()
    grafo = jsonld_pagina(html)
    return {
        "slug": slug, "meta": meta_pagina(html), "jsonld": grafo, "kicker": a.kicker(), "h1": inline(a.h1()),
        "dek": a.dek(), "minutos": a.minutos(), "respuesta": a.respuesta, "faq_titulo": a.faq_titulo, "faq": a.faq,
        "relacionados_titulo": a.rel_titulo, "relacionados": a.relacionados, "retirado": a.retirado,
        "bloques": a.bloques, "cuerpo": serializar(a.bloques),
    }


def publicado(rel):
    """HTML de public/<rel> en el commit REF."""
    raiz = AQUI.parents[1]
    return subprocess.run(["git", "show", f"{REF}:public/{rel}"], cwd=raiz, capture_output=True, text=True, check=True).stdout


def slugs(public=PUBLIC):
    return sorted(p.parent.name for p in (Path(public) / "blog").glob("*/index.html"))


# ---------- índice del blog ----------
def extraer_indice(public=PUBLIC):
    html = publicado("blog/index.html")
    raiz = leer(re.search(r"<main\b[^>]*>(.*)</main>", html, re.S).group(1))
    hero = next(raiz.buscar(lambda n: n.tiene("vt-hero__bg-img")))
    secciones, actual = [], None

    def recorrer(n):
        nonlocal actual
        for h in n.elementos():
            if h.tag == "h2" and "¿Buscas" not in texto_limpio(h):
                actual = {"titulo": texto_limpio(h), "tarjetas": []}
                secciones.append(actual)
            elif h.tag == "a" and (h.attrs.get("href") or "").startswith("/blog/") and actual is not None:
                actual["tarjetas"].append(tarjeta(h, public))
            elif h.tag == "h2":
                actual = None
            else:
                recorrer(h)

    recorrer(raiz)
    return {"meta": meta_pagina(html), "jsonld": jsonld_pagina(html), "foto": foto(hero, public), "secciones": secciones}


def tarjeta(a, public):
    img = next(a.buscar(lambda n: n.tag == "img"), None)
    titulo = next(a.buscar(lambda n: n.tag in ("h3", "h4")))
    cat = next(a.buscar(lambda n: n.tiene("badge")), None)
    p = next(a.buscar(lambda n: n.tag == "p"), None)
    m = re.search(r"(\d+) min", texto_limpio(a))
    return {"href": a.attrs["href"], "foto": foto(img, public) if img is not None else None,
            "categoria": texto_limpio(cat) if cat is not None else "", "titulo": texto_limpio(titulo),
            "texto": texto_limpio(p) if p is not None else "", "minutos": int(m.group(1)) if m else None}


# ---------- paridad ----------
M_CTA = "Era parte del índice, la barra lateral o un CTA del HTML anterior; la plantilla pone los suyos (spec §3.3)."
M_FAQ_H = "Sigue en la página: las preguntas ahora van en <details> de la sección de preguntas."
M_SOLO_LD = "Pregunta que solo estaba en el JSON-LD, no en la página: FAQPage ahora repite lo visible (spec §7.3)."
M_CIERRE = "El CTA final lo pone la plantilla, con landing y mensaje del artículo."


def _textos(doc):
    faq = [limpio(re.sub(r"<[^>]+>", " ", q)) for q, _a in doc["faq"]]
    titulos = [limpio(re.sub(r"<[^>]+>", " ", doc["h1"]))]
    titulos += [limpio(re.sub(r"<[^>]+>", " ", b)) for b in re.findall(r"<h[23]\b[^>]*>(.*?)</h[23]>", doc["cuerpo"], re.S)]
    titulos += [r["titulo"] for r in doc["relacionados"]]
    if doc["relacionados_titulo"]:
        titulos.append(doc["relacionados_titulo"])
    if doc["respuesta"]:
        titulos.append(doc["respuesta"]["titulo"])
    titulos.append(doc["faq_titulo"])
    return titulos, faq


def _texto_doc(doc):
    return " ".join([doc["cuerpo"], doc["dek"], doc["h1"], " ".join(doc["respuesta"]["parrafos"]) if doc["respuesta"] else "",
                     " ".join(q + " " + a for q, a in doc["faq"]), " ".join(r["titulo"] + " " + r["texto"] for r in doc["relacionados"])])


def paridad_de(html, doc, correcciones):
    """PARIDAD del artículo: qué dejó de estar (y por qué) respecto a lo publicado. Lo que no se pueda explicar detiene la
    extracción."""
    import paridad as par
    viejo = par.extraer(html)
    titulos, faq = _textos(doc)
    retirados, reemplazos = {}, {}
    plano = [(par.texto(v), par.texto(n), m) for v, n, m in correcciones]
    retirado_txt = " ".join(doc["retirado"])
    for h in viejo["encabezados"]:
        if par.cubierto(h, titulos):
            continue
        corr = next(((v, n, m) for v, n, m in plano if v and v in h), None)
        if corr and not par.cubierto(h.replace(corr[0], corr[1]), faq):
            reemplazos[h] = h.replace(corr[0], corr[1])
        elif corr or par.cubierto(h, faq):
            retirados[h] = M_FAQ_H
        elif h in retirado_txt or h in (doc["h1"],):
            retirados[h] = M_CTA
        else:
            retirados[h] = M_CIERRE
    for q in viejo["faq"]:
        if not par.cubierto(q, faq):
            corr = next(((v, n, m) for v, n, m in plano if v and v in q), None)
            if corr:
                reemplazos[q] = q.replace(corr[0], corr[1])
            else:
                retirados[q] = M_SOLO_LD
    nuevo_txt = par.texto(_texto_doc(doc))
    nuevos = {p.replace(" ", "") for p in re.findall(r"\$\s?\d[\d,]*", nuevo_txt)}
    for precio in viejo["precios"]:
        if precio in nuevos:
            continue
        corr = next((m for v, _n, m in plano if precio in v.replace(" ", "")), None)
        retirados[precio] = corr or M_CTA
    meta = {}
    for clave, valor in viejo["meta"].items():
        actual = doc["meta"].get(clave) if not clave.startswith("og:") else dict(doc["meta"]["og"]).get(clave)
        if actual is not None and actual != valor:
            motivo = next((m for v, _n, m in plano if v and v in valor), "Corrección de contenido documentada.")
            meta[clave] = [actual, motivo]
    return {"reemplazos": reemplazos, "retirados": retirados, "meta": meta}


# ---------- escritura ----------
def fragmento(doc):
    meta = {k: v for k, v in doc.items() if k not in ("cuerpo", "bloques")}
    return "<!--vt:meta\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\n-->\n" + doc["cuerpo"]


def _reemplazar(valor, viejo, nuevo, cuenta):
    if isinstance(valor, str):
        cuenta[0] += valor.count(viejo)
        return valor.replace(viejo, nuevo)
    if isinstance(valor, list):
        return [_reemplazar(v, viejo, nuevo, cuenta) for v in valor]
    if isinstance(valor, dict):
        return {k: _reemplazar(v, viejo, nuevo, cuenta) for k, v in valor.items()}
    return valor


def fecha_actualizada(doc, correcciones):
    """dateModified de hoy solo en los artículos cuyo contenido cambió de verdad (no por cambiar la plantilla)."""
    if correcciones and FECHA_CORRECCION:
        articulo = next(n for n in doc["jsonld"]["@graph"] if n.get("@type") == "Article")
        articulo["dateModified"] = FECHA_CORRECCION
    return doc


def corregir(doc, correcciones, todos=()):
    """Copia del documento con cada corrección (viejo, nuevo, motivo) aplicada en todos sus textos. Una corrección que no
    encuentra su texto detiene la extracción: así nadie cree haber corregido algo que no se tocó."""
    for viejo, nuevo, motivo in correcciones:
        cuenta = [0]
        doc = _reemplazar(doc, viejo, nuevo, cuenta)
        if not cuenta[0]:
            raise ValueError(f"{doc['slug']}: la corrección no encontró su texto: {viejo!r} ({motivo})")
    for viejo, nuevo, _motivo in todos:
        doc = _reemplazar(doc, viejo, nuevo, [0])
    return doc


def escribir(lista=None, public=PUBLIC, destino=DESTINO):
    from contenido import blog_correcciones as bc
    destino.mkdir(parents=True, exist_ok=True)
    for slug in lista or slugs(public):
        doc = fecha_actualizada(corregir(extraer(slug, public), bc.de(slug), bc.TODOS), bc.de(slug))
        doc["paridad"] = paridad_de(publicado(f"blog/{slug}/index.html"), doc, bc.de(slug) + bc.TODOS)
        (destino / f"{slug}.html").write_text(fragmento(doc), encoding="utf-8")
    indice = corregir({"slug": "/blog", **extraer_indice(public)}, bc.de("/blog"), bc.TODOS)
    (destino / "_indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:2] != ["escribir"]:
        raise SystemExit("Uso: python3 tools/site/extraer_blog.py escribir [<slug> …]")
    escribir(sys.argv[2:] or None)
    print("listo")
