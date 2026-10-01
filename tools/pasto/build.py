"""Genera el hub, las 9 fichas de pasto sintético, la página local de Tampico y /precios.

Uso: python3 tools/pasto/build.py   (desde la raíz del repo)
"""
from pathlib import Path

from ciudad import build_ciudad
from ciudades import CIUDADES
from data import MODELOS
from ficha import build_ficha
from hub import build_hub
from local import build_local
from precios import build_precios
from zonas import ZONAS, build_zona

ROOT = Path(__file__).resolve().parents[2] / "public" / "pasto-sintetico"


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"ok {path.relative_to(ROOT.parent)} ({len(html) // 1024} KB)")


def main():
    write(ROOT / "index.html", build_hub())
    write(ROOT.parent / "pasto-sintetico-tampico" / "index.html", build_local())
    write(ROOT.parent / "precios" / "index.html", build_precios())
    for slug, zona in ZONAS.items():
        write(ROOT.parent / slug / "index.html", build_zona(slug, zona))
    for m in MODELOS:
        write(ROOT / m["slug"] / "index.html", build_ficha(m))
    for c in CIUDADES:
        write(ROOT / "envio" / c["slug"] / "index.html", build_ciudad(c))


if __name__ == "__main__":
    main()
