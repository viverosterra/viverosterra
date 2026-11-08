"""Paridad de las fotos y del formulario de pedido de las páginas de materiales (Etapa 2f).

Regla del dueño: cada foto de main se queda, en el mismo orden, sin quitar ni cambiar ninguna (el alt y el pie sí pueden
mejorar). paridad.py no ve imágenes; aquí se congela, por página, la lista ordenada de las <img> del <main> (sin logos)
con su src, srcset y alt, y los nombres y valores del formulario por correo a formsubmit (el dueño recibe esos campos).
tests/test_materiales_paridad.py exige que las páginas nuevas publiquen las mismas fotos en el mismo orden y el mismo
formulario (más el honeypot).

Uso: python3 tools/site/paridad_materiales.py capturar   (escribe tests/paridad/materiales-fotos.json)
"""
import html as html_mod
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402

RUTAS = ("/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico")
CAPTURA = paridad.CAPTURAS / "materiales-fotos.json"
IMG_RE = re.compile(r"<img\b[^>]*>")
FORM_RE = re.compile(r'<form\b[^>]*action="https://formsubmit\.co/[^"]*"[^>]*>(.*?)</form>', re.S)
CAMPO_RE = re.compile(r'<(?:input|textarea|select)\b[^>]*\bname="([^"]+)"[^>]*>')


def atributo(etiqueta, nombre):
    m = re.search(rf'\s{nombre}="([^"]*)"', etiqueta)
    return html_mod.unescape(m.group(1)) if m else None


def fotos(html):
    """[{src, srcset, alt}] de las <img> del <main>, en orden, sin los logos."""
    salida = []
    for etiqueta in IMG_RE.findall(paridad.principal(html)):
        src = atributo(etiqueta, "src")
        if src and not src.startswith("/img/logo"):
            salida.append({"src": src, "srcset": atributo(etiqueta, "srcset"), "alt": atributo(etiqueta, "alt")})
    return salida


def formulario(html):
    """{name: value} de los campos del formulario a formsubmit ("" si no lleva value)."""
    m = FORM_RE.search(html)
    if not m:
        return {}
    return {atributo(c, "name"): atributo(c, "value") or "" for c in (x.group(0) for x in CAMPO_RE.finditer(m.group(1)))}


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    return {"fotos": fotos(html), "formulario": formulario(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_materiales.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), sorted(d["formulario"]))
