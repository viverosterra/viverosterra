"""Paridad del texto y de las fotos del blog (Etapa 2h). paridad.py congela encabezados, preguntas, precios y enlaces, pero
no la prosa ni las imágenes: aquí se guarda el texto visible del <main> de cada artículo tal como se publicaba
(tests/paridad/blog-texto/<slug>.txt) y la lista ordenada de sus <img> (tests/paridad/blog-fotos.json). test_blog_paridad
exige que el texto del artículo nuevo sea el mismo, palabra por palabra, salvo las correcciones documentadas.

Uso: python3 tools/site/paridad_blog.py capturar   (antes de tocar los artículos)
"""
import difflib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

DIR_TEXTO = paridad.CAPTURAS / "blog-texto"
FOTOS = paridad.CAPTURAS / "blog-fotos.json"


def slugs(public=paridad.paginas.PUBLIC):
    return sorted(p.parent.name for p in (Path(public) / "blog").glob("*/index.html"))


def texto_main(html):
    return paridad.texto(paridad.principal(html))


def capturar(public=paridad.paginas.PUBLIC):
    DIR_TEXTO.mkdir(parents=True, exist_ok=True)
    fotos = {"/blog": paridad_materiales.fotos(paridad.archivo("/blog", public).read_text(encoding="utf-8"))}
    for slug in slugs(public):
        html = paridad.archivo(f"/blog/{slug}", public).read_text(encoding="utf-8")
        (DIR_TEXTO / f"{slug}.txt").write_text(texto_main(html) + "\n", encoding="utf-8")
        fotos[f"/blog/{slug}"] = paridad_materiales.fotos(html)
    FOTOS.write_text(json.dumps(fotos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return fotos


def viejo_corregido(slug, correcciones):
    """Texto capturado con las correcciones aplicadas (viejo y nuevo reducidos a texto, igual que la captura)."""
    t = (DIR_TEXTO / f"{slug}.txt").read_text(encoding="utf-8").strip()
    for viejo, nuevo, _motivo in correcciones:
        t = t.replace(paridad.texto(viejo), paridad.texto(nuevo))
    return t


def cuerpo_nuevo(html):
    """Texto del <article> (respuesta, cuerpo y preguntas), sin lo que agrega la plantilla (índice móvil, CTA a media lectura y "Para seguir")."""
    m = re.search(r'<article class="vt-art__cuerpo".*?</article>', html, re.S)
    sin_plantilla = m.group(0)
    for agregado in (r'<nav class="vt-art__sigue".*?</nav>', r'<details class="vt-art__toc".*?</details>',
                     r'<aside class="vt-art__medio".*?</aside>'):
        sin_plantilla = re.sub(agregado, " ", sin_plantilla, flags=re.S)
    return paridad.texto(sin_plantilla)


def diferencias(viejo, nuevo):
    """(insertado, borrado): tramos de palabras que están solo en el artículo nuevo y solo en el viejo."""
    a, b = viejo.split(), nuevo.split()
    insertado, borrado = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op in ("replace", "delete"):
            borrado.append(" ".join(a[i1:i2]))
        if op in ("replace", "insert"):
            insertado.append(" ".join(b[j1:j2]))
    return insertado, borrado


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_blog.py capturar")
    print(len(capturar()), "páginas")
