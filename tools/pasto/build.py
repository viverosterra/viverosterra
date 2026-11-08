"""Genera el feed de Merchant y las URLs de la tienda en el sitemap. Desde la Etapa 2g ya no escribe páginas: la tienda
(hub, 9 fichas, 11 ciudades, perros y sintético en Tampico, Etapa 2b), /precios y las 6 zonas salen de
tools/site/generar.py con sus plantillas. Este paquete sigue siendo la fuente de modelos, zonas de envío y fletes
(data.py) y de la fórmula de mensualidades (mensualidades.py).

Uso: python3 tools/pasto/build.py   (desde la raíz del repo). Para todo el sitio: python3 tools/site/build.py
"""
from pathlib import Path

from ciudades import CIUDADES
from data import MODELOS, SITE
from feed import build_feed
from sitemap import upsert

PUBLIC = Path(__file__).resolve().parents[2] / "public"


def main():
    (PUBLIC / "feed-pasto-sintetico.xml").write_text(build_feed(), encoding="utf-8")
    upsert([f"{SITE}/pasto-sintetico", f"{SITE}/pasto-sintetico/perros"]
           + [f"{SITE}/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
           + [f"{SITE}/pasto-sintetico/{m['slug']}" for m in MODELOS], conservar=True)


if __name__ == "__main__":
    main()
