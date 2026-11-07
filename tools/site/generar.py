"""Páginas que salen de plantillas (Etapa 2). Cada entrada es (ruta, archivo en public/, plantilla, contenido): la
plantilla vive en tools/site/plantillas/<plantilla>.py y el contenido en tools/site/contenido/<contenido>.py.

Escribe cada página con el shell ya aplicado y solo si cambia, así una segunda corrida de build.py no toca nada. Para
migrar otro tipo de página: agrega su contenido, su plantilla (o reutiliza una) y su fila aquí.
"""
import importlib
from pathlib import Path

import paginas
import shell

PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
)


def contenido_de(ruta):
    return next(contenido for r, _a, _p, contenido in PAGINAS if r == ruta)


def renderizar(ruta, plantilla, contenido, urls):
    """HTML final de la página: plantilla + contenido + shell."""
    modulo_plantilla = importlib.import_module(f"plantillas.{plantilla}")
    modulo_contenido = importlib.import_module(f"contenido.{contenido}")
    return shell.aplicar(modulo_plantilla.render(modulo_contenido.CONTENIDO), ruta, urls)


def escribir_todo(urls, public=paginas.PUBLIC):
    """Escribe las páginas con plantilla que cambiaron; devuelve cuántas escribió."""
    escritas = 0
    for ruta, salida, plantilla, contenido in PAGINAS:
        path = Path(public) / salida
        html = renderizar(ruta, plantilla, contenido, urls)
        if path.is_file() and path.read_text(encoding="utf-8") == html:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        escritas += 1
    return escritas
