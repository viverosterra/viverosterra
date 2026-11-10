"""Copias con hash de los assets del shell, para servirlas con caché inmutable de un año.

La fuente vive sin hash (public/css/terra.css, terra-tienda.css, terra-plantas.css, terra-materiales.css,
terra-precios.css, terra-nochebuenas.css, terra-temporada.css, terra-inicio.css, legacy-fixes.css, public/js/terra.js) y el build
publica <nombre>.<10 hex>.<ext> al lado; las hojas CSS van minificadas (sin comentarios ni sangría). Se conservan dos
copias por asset: la actual y la que sirve producción (la que enlazan las páginas de `main`), para que el HTML que quedó
en caché justo después de un deploy no pida un archivo borrado. Cuáles son se guarda en tools/site/activos.json
({clave: [actual, servida]}), versionado: así el build no depende de fechas de archivo (cambian con cada checkout o
merge) y una segunda corrida no borra nada. Solo al cambiar la fuente se rota: la nueva pasa a "actual" y "servida" se
toma de lo que enlaza `main` (o HEAD, o el HTML en disco si no hay git). Las demás copias con hash se borran.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / "public"
REGISTRO = Path(__file__).resolve().parent / "activos.json"
FUENTES = {
    "terra.css": "css/terra.css",
    "terra-tienda.css": "css/terra-tienda.css",
    "terra-plantas.css": "css/terra-plantas.css",
    "terra-materiales.css": "css/terra-materiales.css",
    "terra-precios.css": "css/terra-precios.css",
    "terra-blog.css": "css/terra-blog.css",
    "terra-obras.css": "css/terra-obras.css",
    "terra-nochebuenas.css": "css/terra-nochebuenas.css",
    "terra-temporada.css": "css/terra-temporada.css",
    "terra-inicio.css": "css/terra-inicio.css",
    "legacy-fixes.css": "css/legacy-fixes.css",
    "terra.js": "js/terra.js",
}


def minificar_css(texto):
    """Sin comentarios, sin sangría ni renglones vacíos. No toca nada dentro de una regla: es seguro con cadenas,
    url(), calc() y valores con espacios, y no necesita dependencias."""
    sin_comentarios = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
    return "".join(linea.strip() + "\n" for linea in sin_comentarios.splitlines() if linea.strip())


def publicado(rel, bruto):
    """Bytes de la copia con hash: las hojas CSS van minificadas; el JS va tal cual."""
    return minificar_css(bruto.decode("utf-8")).encode("utf-8") if rel.endswith(".css") else bruto


def _con_hash(rel, contenido):
    raiz, ext = rel.rsplit(".", 1)
    return f"{raiz}.{hashlib.sha256(contenido).hexdigest()[:10]}.{ext}"


def _patron(rel):
    raiz, ext = rel.rsplit(".", 1)
    return re.compile(rf"/{re.escape(raiz)}\.[0-9a-f]{{10}}\.{re.escape(ext)}")


def urls(public=PUBLIC):
    """URL pública con hash de cada asset del shell, sin escribir nada."""
    public = Path(public)
    return {clave: "/" + _con_hash(rel, publicado(rel, (public / rel).read_bytes())) for clave, rel in FUENTES.items()}


REFS_PRODUCCION = ("origin/main", "main", "HEAD")


def _html_de_main(public):
    """HTML de la home y del índice del blog (entre los dos enlazan los tres assets) en `origin/main` (lo que sirve
    producción aunque el `main` local esté atrasado), en `main`, en HEAD o, sin git, en disco."""
    rutas = ("public/index.html", "public/blog/index.html")
    raiz = Path(public).resolve().parent
    for ref in REFS_PRODUCCION:
        try:
            return "".join(subprocess.run(["git", "show", f"{ref}:{r}"], cwd=raiz, capture_output=True, text=True,
                                          check=True).stdout for r in rutas)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return "".join((Path(public) / r.split("/", 1)[1]).read_text(encoding="utf-8")
                   for r in rutas if (Path(public) / r.split("/", 1)[1]).is_file())


def servida(rel, html):
    """Copia con hash de `rel` que enlaza el HTML dado, o None."""
    m = _patron(rel).search(html)
    return m.group(0) if m else None


def generaciones(anteriores, nuevas, html_main):
    """Registro nuevo: sin cambio de fuente se conserva tal cual; con cambio, [nueva, la que sirve main]."""
    salida = {}
    for clave, rel in FUENTES.items():
        previas = anteriores.get(clave, [])
        if previas and previas[0] == nuevas[clave]:
            salida[clave] = previas
            continue
        en_main = servida(rel, html_main)
        salida[clave] = [nuevas[clave]] + ([en_main] if en_main and en_main != nuevas[clave] else [])
    return salida


def publicar(public=PUBLIC, registro=REGISTRO):
    """Escribe la copia actual si falta, borra las que no están en el registro y devuelve las URLs."""
    public, registro = Path(public), Path(registro)
    resultado = urls(public)
    anteriores = json.loads(registro.read_text(encoding="utf-8")) if registro.is_file() else {}
    cambia = any(anteriores.get(c, [None])[0] != u for c, u in resultado.items())
    nuevas = generaciones(anteriores, resultado, _html_de_main(public) if cambia else "")
    for clave, rel in FUENTES.items():
        fuente = public / rel
        destino = public / resultado[clave].lstrip("/")
        conservar = {public / u.lstrip("/") for u in nuevas[clave]}
        patron = re.compile(rf"{re.escape(fuente.stem)}\.[0-9a-f]{{10}}{re.escape(fuente.suffix)}")
        for copia in fuente.parent.glob(f"{fuente.stem}.*{fuente.suffix}"):
            if patron.fullmatch(copia.name) and copia not in conservar:
                copia.unlink()
        if not destino.exists():
            destino.write_bytes(publicado(rel, fuente.read_bytes()))
    if nuevas != anteriores:
        registro.write_text(json.dumps(nuevas, indent=1) + "\n", encoding="utf-8")
    return resultado
