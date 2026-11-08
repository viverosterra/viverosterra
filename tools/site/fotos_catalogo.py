"""Fotos del catálogo en local (Etapa 2e): baja una vez de Google Drive la foto de cada especie y la publica como
public/img/catalogo/<slug>-tampico.webp (480 px de ancho o el de la foto si es más chica, WebP calidad 72), con su ancho
y alto en contenido/catalogo_especies.json. Sustituye al proxy /api/img en el catálogo y el hub (el proxy se borra en la
Etapa 5). Una foto chica nunca se agranda: las que miden menos de 480 px están en catalogo_datos.FOTOS_CHICAS. Las de
catalogo_datos.FOTOS_RETIRADAS no se bajan ni se publican: quedan con img, ancho y alto en null (hoy ninguna: el dueño
pidió dejar las fotos como en main, 2026-11-08).

Uso (una vez; requiere red y Pillow): python3 tools/site/fotos_catalogo.py
No reescribe las fotos que ya existen (solo vuelve a leer su tamaño). Cada descarga se valida: respuesta 200 de
lh3.googleusercontent.com (el mismo origen que usaba /api/img), tipo image/*, a lo más 15 MB, una imagen que Pillow
abre y de al menos 120 px de ancho (menos sería un ícono o una página de error). Los bytes descargados nunca se guardan
tal cual: se decodifican y se vuelven a codificar en WebP (con su transparencia, si la tienen). Si una especie falla, se detiene y dice cuál.
tests/test_fotos_catalogo.py prueba las funciones sin red y que cada especie tenga su foto local.
"""
import io
import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

DESTINO = paginas.PUBLIC / "img" / "catalogo"
ANCHO = 480
CALIDAD = 72
MINIMO = 120
MAXIMO_BYTES = 15 * 1024 * 1024
ORIGEN = "https://lh3.googleusercontent.com/d/{id}=w1200"
ID_RE = re.compile(r"[\w-]{20,60}")


def url_origen(drive_id):
    if not isinstance(drive_id, str) or not ID_RE.fullmatch(drive_id):
        raise ValueError(f"id de Drive inválido: {drive_id!r}")
    return ORIGEN.format(id=drive_id)


def ruta_local(slug):
    return f"/img/catalogo/{slug}-tampico.webp"


def validar(tipo, cuerpo):
    if not (tipo or "").startswith("image/"):
        raise ValueError(f"no es una imagen: {tipo!r}")
    if len(cuerpo) > MAXIMO_BYTES:
        raise ValueError("la imagen pesa más de 15 MB")
    return cuerpo


def descargar(url):
    peticion = urllib.request.Request(url, headers={"User-Agent": "ViverosTerra-fotos/1.0"})
    with urllib.request.urlopen(peticion, timeout=30) as respuesta:
        if respuesta.status != 200:
            raise ValueError(f"HTTP {respuesta.status}")
        return validar(respuesta.headers.get("Content-Type", ""), respuesta.read(MAXIMO_BYTES + 1))


def a_webp(cuerpo):
    from PIL import Image, ImageOps

    with Image.open(io.BytesIO(cuerpo)) as original:
        im = ImageOps.exif_transpose(original)
        # Un PNG o WebP con fondo transparente conserva su alfa (convertirlo a RGB lo aplanaba a negro).
        transparente = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
        im = im.convert("RGBA" if transparente else "RGB")
    if im.width < MINIMO:
        raise ValueError(f"foto de {im.width} px de ancho: menos de {MINIMO}")
    ancho = min(ANCHO, im.width)  # nunca se agranda una foto chica
    alto = round(im.height * ancho / im.width)
    salida = io.BytesIO()
    im.resize((ancho, alto), Image.LANCZOS).save(salida, "WEBP", quality=CALIDAD, method=6)
    return salida.getvalue()


def dimensiones_webp(datos):
    """(ancho, alto) de un WebP (VP8, VP8L o VP8X) sin Pillow."""
    if datos[:4] != b"RIFF" or datos[8:12] != b"WEBP":
        raise ValueError("no es WebP")
    tipo = datos[12:16]
    if tipo == b"VP8 ":
        ancho, alto = struct.unpack("<HH", datos[26:30])
        return ancho & 0x3FFF, alto & 0x3FFF
    if tipo == b"VP8L":
        bits = int.from_bytes(datos[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if tipo == b"VP8X":
        return int.from_bytes(datos[24:27], "little") + 1, int.from_bytes(datos[27:30], "little") + 1
    raise ValueError(f"WebP desconocido: {tipo!r}")


def actualizar(especies, destino=DESTINO, bajar=descargar, convertir=a_webp, retiradas=None):
    """Lista nueva de especies con img, ancho y alto (no muta la de entrada) y cuántas fotos se bajaron. Las retiradas
    (por omisión catalogo_datos.FOTOS_RETIRADAS) quedan sin foto y no se bajan."""
    retiradas = cd.FOTOS_RETIRADAS if retiradas is None else retiradas
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    salida, nuevas = [], 0
    for e in especies:
        if e["slug"] in retiradas:
            salida.append({**e, "img": None, "ancho": None, "alto": None})
            continue
        archivo = destino / f"{e['slug']}-tampico.webp"
        if not archivo.exists():
            try:
                archivo.write_bytes(convertir(bajar(url_origen(e["drive"]))))
            except (OSError, ValueError) as error:
                raise SystemExit(f"{e['slug']}: {error}") from error
            nuevas += 1
        ancho, alto = dimensiones_webp(archivo.read_bytes())
        salida.append({**e, "img": ruta_local(e["slug"]), "ancho": ancho, "alto": alto})
    return salida, nuevas


def main():
    especies, nuevas = actualizar(cd.cargar())
    cd.ARCHIVO.write_text(json.dumps(especies, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    con_foto = sum(1 for e in especies if e["img"])
    print(f"{nuevas} fotos nuevas · {con_foto} de {len(especies)} especies con foto local en public/img/catalogo")


if __name__ == "__main__":
    main()
