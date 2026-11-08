"""Paridad de las fotos y de las anclas de las 6 zonas y de /precios (Etapa 2g).

Regla del dueño: cada foto de main se queda, en el mismo orden, sin quitar, agregar ni cambiar ninguna (el alt y el pie sí
pueden mejorar). paridad.py no ve imágenes ni anclas; aquí se congela, por página, la lista ordenada de las <img> del
<main> (paridad_materiales.fotos: src, srcset y alt, sin logos) y los id de sus <section>, las anclas que otras páginas,
los buscadores o el botón "Ver la lista" pueden enlazar (#pasto, #mensualidades, #precios…; los id de los títulos sí
cambian). tests/test_zonas_reglas.py exige las mismas fotos en el mismo orden y que cada ancla siga existiendo.

Uso: python3 tools/site/paridad_zonas.py capturar   (escribe tests/paridad/zonas-fotos-anclas.json)
"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

RUTAS = ("/jardineria-lomas-de-rosales-tampico", "/jardineria-country-club-tampico", "/jardineria-aguila-tampico",
         "/jardineria-lomas-del-chairel-tampico", "/jardineria-ciudad-madero", "/jardineria-altamira", "/precios")
CAPTURA = paridad.CAPTURAS / "zonas-fotos-anclas.json"
ID_RE = re.compile(r'<section\b[^>]*\sid="([^"]+)"')


def anclas(html):
    """Los id de las <section> del <main>, ordenados."""
    return sorted(set(ID_RE.findall(paridad.principal(html))))


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"fotos": paridad_materiales.fotos(html), "anclas": anclas(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_zonas.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), " ".join(d["anclas"]))
