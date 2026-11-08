"""Paridad de contenido al migrar una página a su plantilla (Etapa 2).

Antes de migrar se congela lo que la página publicaba (`capturar`): meta (título, descripción, robots, canonical, Open
Graph), tipos del JSON-LD, encabezados h1–h3, preguntas frecuentes, precios y enlaces internos del <main>. Después,
tests/test_paridad.py exige que cada elemento siga en la página nueva o que el contenido diga a dónde fue
(PARIDAD["reemplazos"]) o por qué se retiró (PARIDAD["retirados"]). La meta no cambia salvo que el contenido declare el
valor nuevo y el motivo (PARIDAD["meta"]: {clave: (valor nuevo, motivo)}; desde 2d, para no publicar un precio que el
dueño corrigió). Un tipo del JSON-LD solo deja de salir con su motivo (PARIDAD["jsonld"]: {tipo: motivo}; desde la
revisión 2d, cuando un nodo suelto pasa a ser una referencia por @id a la entidad única #negocio).

Uso:
  python3 tools/site/paridad.py capturar /pasto-en-rollo-tampico   (congela tests/paridad/pasto-en-rollo-tampico.json)
  python3 tools/site/paridad.py informe /pasto-en-rollo-tampico    (lista lo que falta, para revisar a mano)
"""
import html as html_mod
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402

CAPTURAS = AQUI / "tests" / "paridad"
CATEGORIAS = ("encabezados", "faq", "precios", "enlaces")


def texto(fragmento):
    s = re.sub(r"<(script|style|svg|template)\b.*?</\1>", " ", fragmento, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def principal(html):
    m = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S)
    return m.group(1) if m else html


def _unicos(items):
    vistos, salida = set(), []
    for item in items:
        if item and item not in vistos:
            vistos.add(item)
            salida.append(item)
    return salida


def _recorrer(nodo, tipos, preguntas):
    if isinstance(nodo, dict):
        tipo = nodo.get("@type")
        tipos.update([tipo] if isinstance(tipo, str) else tipo or [])
        if tipo == "Question" and "name" in nodo:
            preguntas.append(nodo["name"].strip())
        for valor in nodo.values():
            _recorrer(valor, tipos, preguntas)
    elif isinstance(nodo, list):
        for valor in nodo:
            _recorrer(valor, tipos, preguntas)


def enlaces(fragmento):
    """Rutas internas enlazadas, sin consulta ni ancla y sin barra final."""
    return sorted({re.sub(r"[?#].*$", "", h).rstrip("/") or "/" for h in re.findall(r'href="(/(?!/)[^"]*)"', fragmento)})


def extraer(html):
    meta = {"title": "", "description": "", "robots": "", "canonical": ""}
    titulo = re.search(r"<title>(.*?)</title>", html, re.S)
    meta["title"] = html_mod.unescape(titulo.group(1).strip()) if titulo else ""
    for nombre in ("description", "robots"):
        m = re.search(rf'<meta name="{nombre}" content="([^"]*)"', html)
        meta[nombre] = html_mod.unescape(m.group(1)) if m else ""
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    meta["canonical"] = canonical.group(1) if canonical else ""
    for propiedad, valor in re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', html):
        meta[propiedad] = html_mod.unescape(valor)
    tipos, preguntas = set(), []
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        _recorrer(json.loads(bloque), tipos, preguntas)
    cuerpo = principal(html)
    encabezados = _unicos(texto(h) for _, h in re.findall(r"<(h[1-3])\b[^>]*>(.*?)</\1>", cuerpo, re.S))
    visibles = [texto(s) for s in re.findall(r"<summary\b[^>]*>(.*?)</summary>", cuerpo, re.S)]
    visibles += [texto(b) for b in re.findall(r'<button\b[^>]*class="[^"]*faq-btn[^"]*"[^>]*>(.*?)</button>', cuerpo, re.S)]
    precios = sorted({p.replace(" ", "") for p in re.findall(r"\$\s?\d[\d,]*", texto(cuerpo))})
    return {"meta": meta, "jsonld_tipos": sorted(tipos), "encabezados": encabezados,
            "faq": _unicos(preguntas + visibles), "precios": precios, "enlaces": enlaces(cuerpo)}


def normalizar(t):
    t = re.sub(r"[\"“”«»]", "", t)
    return re.sub(r"\s+", " ", t).strip().rstrip(".").casefold()


def cubierto(viejo, nuevos):
    """El elemento viejo sigue igual (sin importar mayúsculas, comillas ni el punto final) o como inicio de uno nuevo
    ("Primer riego" cubre "Primer riego Tú", el encabezado con su marcador)."""
    v = normalizar(viejo)
    return any(n == v or n.startswith(v + " ") for n in map(normalizar, nuevos))


def faltantes(viejos, nuevos, mapa):
    """Elementos de la captura que no están en la página nueva ni tienen reemplazo vigente o motivo de retiro."""
    salida = []
    for viejo in viejos:
        if cubierto(viejo, nuevos):
            continue
        if viejo in mapa["reemplazos"]:
            if not cubierto(mapa["reemplazos"][viejo], nuevos):
                salida.append(f"{viejo} → {mapa['reemplazos'][viejo]} (el reemplazo no está en la página)")
            continue
        if not mapa["retirados"].get(viejo):
            salida.append(viejo)
    return salida


def meta_distinta(viejo, nuevo, cambios=None):
    """Claves de la meta que cambiaron sin un cambio declarado con su valor nuevo exacto y un motivo escrito."""
    cambios = cambios or {}
    salida = []
    for clave, valor in viejo.items():
        actual = nuevo.get(clave)
        if actual == valor:
            continue
        declarado = cambios.get(clave)
        if declarado and declarado[0] == actual and len(declarado[1]) > 20:
            continue
        salida.append(f"{clave}: {valor!r} → {actual!r}")
    return salida


def nombre_captura(ruta):
    return "index" if ruta == "/" else ruta.strip("/").replace("/", "_")


def archivo(ruta, public=paginas.PUBLIC):
    for candidato in (Path(public) / ruta.strip("/") / "index.html", Path(public) / f"{ruta.strip('/')}.html"):
        if candidato.is_file():
            return candidato
    raise FileNotFoundError(ruta)


def capturar(ruta, public=paginas.PUBLIC, destino=CAPTURAS):
    datos = extraer(archivo(ruta, public).read_text(encoding="utf-8"))
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / f"{nombre_captura(ruta)}.json"
    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return salida


def comparar(ruta, mapa, public=paginas.PUBLIC, capturas=CAPTURAS):
    """Diccionario categoría → lista de faltantes (vacío si todo está cubierto). Los enlaces nuevos se buscan en toda la
    página (el menú y el pie también enlazan)."""
    viejo = json.loads((Path(capturas) / f"{nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
    html = archivo(ruta, public).read_text(encoding="utf-8")
    nuevo = extraer(html)
    nuevo["enlaces"] = enlaces(html)
    resultado = {c: faltantes(viejo[c], nuevo[c], mapa) for c in CATEGORIAS}
    resultado["meta"] = meta_distinta(viejo["meta"], nuevo["meta"], mapa.get("meta"))
    resultado["jsonld_tipos"] = tipos_retirados(viejo["jsonld_tipos"], nuevo["jsonld_tipos"], mapa.get("jsonld"))
    return resultado


def tipos_retirados(viejos, nuevos, motivos=None):
    """Tipos del JSON-LD que ya no salen y no tienen un motivo escrito (PARIDAD["jsonld"])."""
    motivos = motivos or {}
    return sorted(t for t in set(viejos) - set(nuevos) if len(motivos.get(t, "")) <= 20)


def main(argv):
    if len(argv) < 3 or argv[1] not in ("capturar", "informe"):
        raise SystemExit("Uso: python3 tools/site/paridad.py capturar|informe <ruta> [<ruta> …]")
    if argv[1] == "capturar":
        for ruta in argv[2:]:
            print(f"captura: {capturar(ruta).relative_to(AQUI.parents[1])}")
        return
    import generar  # noqa: E402  (solo aquí: generar importa las plantillas)
    for ruta in argv[2:]:
        print(f"== {ruta}")
        modulo = generar.cargar(generar.contenido_de(ruta))
        for categoria, lista in comparar(ruta, modulo.PARIDAD).items():
            print(f"{categoria}: {'ok' if not lista else ''}")
            for item in lista:
                print(f"  - {item}")


if __name__ == "__main__":
    main(sys.argv)
