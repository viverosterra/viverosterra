"""Genera el hub y las 9 fichas de pasto sintético.

Uso: python3 tools/pasto/build.py   (desde la raíz del repo)
"""
from pathlib import Path

from data import MODELOS
from ficha import build_ficha
from hub import build_hub
from local import build_local

ROOT = Path(__file__).resolve().parents[2] / "public" / "pasto-sintetico"


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"ok {path.relative_to(ROOT.parent)} ({len(html) // 1024} KB)")


def main():
    write(ROOT / "index.html", build_hub())
    write(ROOT.parent / "pasto-sintetico-tampico" / "index.html", build_local())
    for m in MODELOS:
        write(ROOT / m["slug"] / "index.html", build_ficha(m))


if __name__ == "__main__":
    main()
