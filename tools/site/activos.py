"""Copias con hash de los assets del shell, para servirlas con caché inmutable de un año.

La fuente vive sin hash (public/css/terra.css, public/css/legacy-fixes.css, public/js/terra.js) y el build publica
<nombre>.<10 hex>.<ext> al lado, borrando las copias viejas. Las páginas solo enlazan la copia con hash.
"""
import hashlib
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / "public"
FUENTES = {
    "terra.css": "css/terra.css",
    "legacy-fixes.css": "css/legacy-fixes.css",
    "terra.js": "js/terra.js",
}


def _con_hash(rel, contenido):
    raiz, ext = rel.rsplit(".", 1)
    return f"{raiz}.{hashlib.sha256(contenido).hexdigest()[:10]}.{ext}"


def urls(public=PUBLIC):
    """URL pública con hash de cada asset del shell, sin escribir nada."""
    public = Path(public)
    return {clave: "/" + _con_hash(rel, (public / rel).read_bytes()) for clave, rel in FUENTES.items()}


def publicar(public=PUBLIC):
    """Escribe las copias con hash que falten, borra las viejas y devuelve las URLs."""
    public = Path(public)
    resultado = urls(public)
    for clave, rel in FUENTES.items():
        fuente = public / rel
        destino = public / resultado[clave].lstrip("/")
        patron = re.compile(rf"{re.escape(fuente.stem)}\.[0-9a-f]{{10}}{re.escape(fuente.suffix)}")
        for viejo in fuente.parent.glob(f"{fuente.stem}.*{fuente.suffix}"):
            if viejo != destino and patron.fullmatch(viejo.name):
                viejo.unlink()
        if not destino.exists():
            destino.write_bytes(fuente.read_bytes())
    return resultado
