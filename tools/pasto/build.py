"""Genera el hub, las 9 fichas de pasto sintético, la página local de Tampico, /precios y las 6 zonas,
y les aplica el shell compartido de tools/site (menú, pie, barra móvil y head esencial).

Uso: python3 tools/pasto/build.py   (desde la raíz del repo). Para todo el sitio: python3 tools/site/build.py
"""
import sys
from pathlib import Path

from ciudades import CIUDADES
from data import MODELOS, SITE
from feed import build_feed
from local import build_local
from precios import build_precios
from sitemap import upsert
from zonas import ZONAS, build_zona

ROOT = Path(__file__).resolve().parents[2] / "public" / "pasto-sintetico"
HERRAMIENTAS_SITIO = Path(__file__).resolve().parents[1] / "site"
ESCRITAS = []


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    ESCRITAS.append(path)
    print(f"ok {path.relative_to(ROOT.parent)} ({len(html) // 1024} KB)")


def aplicar_shell(paths):
    """Llena las regiones del shell de las páginas recién escritas (mismo resultado que tools/site/build.py)."""
    if str(HERRAMIENTAS_SITIO) not in sys.path:
        sys.path.insert(0, str(HERRAMIENTAS_SITIO))
    import activos
    import shell
    urls = activos.publicar()
    for path in paths:
        shell.aplicar_archivo(path, urls)


def main():
    ESCRITAS.clear()
    write(ROOT.parent / "pasto-sintetico-tampico" / "index.html", build_local())
    write(ROOT.parent / "precios" / "index.html", build_precios())
    for slug, zona in ZONAS.items():
        write(ROOT.parent / slug / "index.html", build_zona(slug, zona))
    (ROOT.parent / "feed-pasto-sintetico.xml").write_text(build_feed(), encoding="utf-8")
    upsert([f"{SITE}/pasto-sintetico", f"{SITE}/pasto-sintetico/perros"]
           + [f"{SITE}/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
           + [f"{SITE}/pasto-sintetico/{m['slug']}" for m in MODELOS], conservar=True)
    aplicar_shell(ESCRITAS)


if __name__ == "__main__":
    main()
