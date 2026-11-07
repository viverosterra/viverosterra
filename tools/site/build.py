"""Punto de entrada único del sitio: genera las páginas de pasto, publica los assets del shell con hash y aplica el
shell a todas las páginas de public/. CI verifica que correrlo deje public/ sin cambios.

Uso: python3 tools/site/build.py   (desde cualquier carpeta)
"""
import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTO = AQUI.parent / "pasto"
sys.path.insert(0, str(AQUI))

import activos  # noqa: E402
import shell  # noqa: E402


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
    cambiadas = shell.aplicar_todo(urls)
    print(f"shell: {cambiadas} de {len(shell.paginas_html())} páginas actualizadas")


if __name__ == "__main__":
    main()
