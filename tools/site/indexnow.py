"""Aviso a los buscadores que usan IndexNow (Bing, y por Bing, ChatGPT y Copilot; también Yandex, Seznam y Naver) de las
páginas que cambiaron. Se corre a mano DESPUÉS de publicar: python3 tools/site/indexnow.py 2026-11-22 (o sin fecha: hoy).
Manda las URLs del sitemap cuyo <lastmod> es de esa fecha o posterior. La llave es el archivo public/<LLAVE>.txt."""
import json
import sys
import urllib.request
from datetime import date

import datos
import paginas
import sitemap_fechas

LLAVE = "7d84a02ce81c4eb2ac4a967dd33f23bc"
DESTINO = "https://api.indexnow.org/indexnow"


def urls_desde(fecha, xml):
    return [url for url, lastmod in sitemap_fechas.ENTRADA_RE.findall(xml) if lastmod >= fecha]


def cuerpo(urls):
    host = datos.SITIO.split("//")[1]
    return {"host": host, "key": LLAVE, "keyLocation": f"{datos.SITIO}/{LLAVE}.txt", "urlList": urls}


def main(argv):
    fecha = argv[1] if len(argv) > 1 else date.today().isoformat()
    urls = urls_desde(fecha, (paginas.PUBLIC / "sitemap.xml").read_text(encoding="utf-8"))
    if not urls:
        print(f"indexnow: ninguna página con fecha {fecha} o posterior")
        return 0
    pedido = urllib.request.Request(DESTINO, data=json.dumps(cuerpo(urls)).encode("utf-8"),
                                    headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(pedido, timeout=30) as respuesta:
        print(f"indexnow: {len(urls)} URLs enviadas, respuesta {respuesta.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
