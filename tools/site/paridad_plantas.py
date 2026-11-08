"""Paridad de especies de las páginas de plantas (Etapa 2e): nombre común, nombre científico y enlaces al blog.

paridad.py congela encabezados h1–h3, preguntas, precios y enlaces del <main>; las tarjetas de especies de estas páginas
no son encabezados (div.ecard-name de las subcategorías, las tarjetas del hub, el arreglo `plants` del catálogo), así que
aquí se congela aparte qué especies publicaba cada página, con su nombre científico, y sus enlaces a /blog/. Las páginas
nuevas marcan cada especie con <h3 class="vt-esp__nombre"> y <p class="vt-esp__sci"><i>…</i></p>.
tests/test_plantas_paridad.py exige que cada especie siga, tenga reemplazo o motivo (PARIDAD["especies"]) y que su nombre
científico sea el mismo o la corrección declarada en contenido/catalogo_datos.CIENTIFICOS_CORREGIDOS.

Uso: python3 tools/site/paridad_plantas.py capturar   (escribe tests/paridad/plantas-especies.json)
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402

RUTAS = ("/plantas-palmas-arboles-tampico", "/palmas-tropicales-tampico", "/plantas-para-jardin-tampico",
         "/arboles-ornamentales-tampico", "/arboles-para-banqueta-tampico", "/plantas-de-interior-tampico", "/catalogo")
CAPTURA = paridad.CAPTURAS / "plantas-especies.json"
SUBCATEGORIA_RE = re.compile(r'class="ecard-name">(.*?)</div>\s*<div class="ecard-sc">(.*?)</div>', re.S)
HUB_RE = re.compile(r'<a\b[^>]*class="service-card[^"]*"[^>]*>.*?<h3\b[^>]*>(.*?)</h3>', re.S)
CATALOGO_RE = re.compile(r"\{cat:'\w+',name:'([^']*)',sc:'([^']*)'")
NUEVA_RE = re.compile(r'<h3 class="vt-esp__nombre">(.*?)</h3>\s*<p class="vt-esp__sci"><i>(.*?)</i></p>', re.S)
BLOG_RE = re.compile(r'href="(/blog/[^"#?]+)"')


def especies(html):
    """Pares (nombre, científico) únicos, en orden de aparición; "" si la página no publicaba el científico."""
    cuerpo = paridad.principal(html)
    pares = [(paridad.texto(n), paridad.texto(s)) for n, s in SUBCATEGORIA_RE.findall(cuerpo)]
    pares += [(paridad.texto(n), "") for n in HUB_RE.findall(cuerpo) if not paridad.texto(n).startswith("+")]
    pares += CATALOGO_RE.findall(html)
    pares += [(paridad.texto(n), paridad.texto(s)) for n, s in NUEVA_RE.findall(cuerpo)]
    vistos, salida = set(), []
    for par in pares:
        if par not in vistos:
            vistos.add(par)
            salida.append(par)
    return salida


def blog(html):
    return sorted(set(BLOG_RE.findall(paridad.principal(html))))


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"especies": [list(p) for p in especies(html)], "blog": blog(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_plantas.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["especies"]), len(d["blog"]))
