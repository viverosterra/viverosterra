"""Miniaturas de 128 × 128 px de la galería de cada ficha (public/img/pasto-sintetico/galeria/<modelo>-<n>-mini.webp).

Las miniaturas de la galería se ven a 64 px; antes bajaban la copia -sm de 420 × 560 (60–90 KB cada una, cuatro o más
en el primer pantallazo móvil). Recorte cuadrado al centro de la copia -sm, WebP calidad 70 (2–6 KB).

Uso (una vez, cuando llegan fotos nuevas): python3 tools/site/miniaturas.py   — requiere Pillow; el build no lo usa.
No reescribe las que ya existen. tests/test_tienda.py comprueba que cada miniatura enlazada exista.
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import paginas  # noqa: E402

GALERIA = paginas.PUBLIC / "img" / "pasto-sintetico" / "galeria"
LADO = 128
CALIDAD = 70


def ruta_mini(slug, idx):
    return GALERIA / f"{slug}-{idx}-mini.webp"


def generar():
    from PIL import Image

    hechas = 0
    for m in data.MODELOS:
        for idx, _tipo, _pie in m["gallery"]:
            destino = ruta_mini(m["slug"], idx)
            if destino.exists():
                continue
            with Image.open(GALERIA / f"{m['slug']}-{idx}-sm.webp") as im:
                lado = min(im.size)
                x, y = (im.width - lado) // 2, (im.height - lado) // 2
                im.crop((x, y, x + lado, y + lado)).resize((LADO, LADO), Image.LANCZOS).save(
                    destino, "WEBP", quality=CALIDAD, method=6)
            hechas += 1
    return hechas


if __name__ == "__main__":
    print(f"{generar()} miniaturas nuevas en {GALERIA.relative_to(paginas.PUBLIC.parent)}")
