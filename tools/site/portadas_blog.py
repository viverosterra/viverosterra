"""Copias de 640 px de ancho de las fotos de portada de los artículos del blog (plan visual V4, 2026-11-11).

La portada de un artículo es la misma foto que ya tiene su tarjeta en el índice del blog (decisión del dueño del
2026-11-11); en celular baja la copia <nombre>-640.webp en lugar del original de 1536 px (150–360 KB). Es la misma foto,
solo reducida: sin recorte ni retoque. WebP calidad 66. Las fotos de 720 px o menos no
llevan copia (nunca se agrandan).

Uso (una vez, cuando cambian las fotos del índice): python3 tools/site/portadas_blog.py   — requiere Pillow; el build no
lo usa. No reescribe las que ya existen. tests/test_visual_v4.py comprueba que cada copia enlazada exista.
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402
from contenido import articulo  # noqa: E402

ANCHO = articulo.ANCHO_MOVIL
CALIDAD = 66


def generar():
    from PIL import Image

    hechas = 0
    for f in {p["src"]: p for p in articulo.PORTADAS.values() if p.get("src_movil")}.values():
        origen = paginas.PUBLIC / f["src"].lstrip("/")
        destino = paginas.PUBLIC / articulo.ruta_movil(f["src"]).lstrip("/")
        if destino.exists():
            continue
        with Image.open(origen) as im:
            alto = round(im.height * ANCHO / im.width)
            im.convert("RGB").resize((ANCHO, alto), Image.LANCZOS).save(destino, "WEBP", quality=CALIDAD, method=6)
        hechas += 1
    print(f"portadas del blog: {hechas} copias de {ANCHO} px escritas")


# Auditoría por página (2026-11-20): copias de la MISMA foto, sin recorte, para las miniaturas del índice (320 px y 640 px)
# y para las fotos del cuerpo de los artículos (640 px), con calidad 80. No reescribe las que ya existen.
CALIDAD_AUDITORIA = 80


def _fotos_del_blog():
    """(src, ancho) de las fotos del índice y de las del cuerpo de los artículos."""
    import re

    from contenido import blog_indice

    fotos = {blog_indice.CONTENIDO["foto"]["src"]: int(blog_indice.CONTENIDO["foto"]["ancho"])}
    for sec in blog_indice.CONTENIDO["secciones"]:
        for t in sec["tarjetas"]:
            if t.get("foto"):
                fotos[t["foto"]["src"]] = int(t["foto"]["ancho"])
    indice = dict(fotos)
    for slug in articulo.CLAVES:
        for src, ancho in re.findall(r'<img src="([^"]+)" width="(\d+)"', articulo.leer(slug)[1]):
            fotos.setdefault(src, int(ancho))
    return indice, fotos


def copias_auditoria():
    from PIL import Image

    import componentes_blog as cb

    indice, fotos = _fotos_del_blog()
    pedidos = [(src, 320) for src, ancho in indice.items() if ancho > 320]
    pedidos += [(src, 640) for src, ancho in fotos.items() if ancho > cb.UMBRAL_COPIA]
    hechas = 0
    for src, ancho in pedidos:
        destino = paginas.PUBLIC / cb.copia(src, ancho).lstrip("/")
        if destino.exists():
            continue
        with Image.open(paginas.PUBLIC / src.lstrip("/")) as im:
            alto = round(im.height * ancho / im.width)
            im.convert("RGB").resize((ancho, alto), Image.LANCZOS).save(destino, "WEBP", quality=CALIDAD_AUDITORIA,
                                                                        method=6)
        hechas += 1
    print(f"blog: {hechas} copias nuevas de 320 y 640 px escritas")


if __name__ == "__main__":
    generar()
    copias_auditoria()
