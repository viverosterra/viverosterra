"""Punto de entrada único del sitio: genera las páginas de pasto, publica los assets del shell con hash, escribe las
páginas con plantilla (tools/site/generar.py), aplica el shell a todas las páginas de public/, genera llms.txt y
llms-full.txt (tools/site/llms.py) y pone en el sitemap la fecha de cada artículo del blog (sitemap_fechas.py). CI verifica que
correrlo deje public/ sin cambios.

Uso: python3 tools/site/build.py   (desde cualquier carpeta)
"""
import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTO = AQUI.parent / "pasto"
sys.path.insert(0, str(AQUI))

import activos  # noqa: E402
import generar  # noqa: E402
import llms  # noqa: E402
import shell  # noqa: E402
import sitemap_fechas  # noqa: E402


def cargar_pasto():
    """Carga tools/pasto/build.py como módulo "pasto_build" (los dos paquetes tienen un build.py)."""
    sys.path.insert(1, str(PASTO))
    spec = importlib.util.spec_from_file_location("pasto_build", PASTO / "build.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main():
    cargar_pasto().main()
    urls = activos.publicar()
    escritas = generar.escribir_todo(urls)
    print(f"plantillas: {escritas} de {len(generar.PAGINAS)} páginas escritas")
    cambiadas = shell.aplicar_todo(urls)
    print(f"shell: {cambiadas} de {len(shell.paginas_html())} páginas actualizadas")
    print(f"llms: {llms.escribir()} de 2 archivos escritos")
    print(f"sitemap: {'fechas del blog actualizadas' if sitemap_fechas.sincronizar() else 'sin cambios'}")


if __name__ == "__main__":
    main()
