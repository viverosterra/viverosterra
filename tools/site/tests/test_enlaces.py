"""Enlaces internos, imágenes y assets locales existen; los redirects apuntan a páginas reales y sin cadenas."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
REDIRECTS = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
ORIGENES = {r["source"] for r in REDIRECTS}
SITIO = "https://www.viverosterra.com"
ATRIBUTO_RE = re.compile(r'\b(href|src|srcset|imagesrcset|content)="([^"]+)"')
IMAGEN_RE = re.compile(r"\.(png|jpe?g|webp|svg|gif)$", re.I)
SCRIPT_RE = re.compile(r"<script\b(?![^>]*ld\+json)[^>]*>.*?</script>", re.S)


def existe(ruta):
    ruta = unquote(ruta).rstrip("/") or "/"
    if ruta == "/" or ruta in ORIGENES or ruta.startswith("/api/"):
        return True
    archivo = PUBLIC / ruta.lstrip("/")
    return archivo.is_file() or archivo.with_suffix(".html").is_file() or (archivo / "index.html").is_file()


def referencias(html):
    """Rutas locales que la página enlaza o carga (sin scripts que arman HTML, con JSON-LD)."""
    html = SCRIPT_RE.sub("", html)
    for atributo, valor in ATRIBUTO_RE.findall(html):
        candidatos = [c.strip().split(" ")[0] for c in valor.split(",")] if atributo.endswith("srcset") else [valor]
        for candidato in candidatos:
            if candidato.startswith(SITIO):
                candidato = candidato[len(SITIO):] or "/"
            if not candidato.startswith("/") or candidato.startswith("//"):
                continue
            if atributo == "content" and not IMAGEN_RE.search(candidato):
                continue
            yield urlsplit(candidato).path
    for url in re.findall(r'"(https://www\.viverosterra\.com/[^"]+\.(?:png|jpe?g|webp))"', html):
        yield url[len(SITIO):]


class EnlacesTest(unittest.TestCase):
    def test_enlaces_y_recursos_locales_existen(self):
        rotos = {}
        for path in PUBLIC.rglob("*.html"):
            for ruta in referencias(path.read_text(encoding="utf-8")):
                if not existe(ruta):
                    rotos.setdefault(ruta, str(path.relative_to(PUBLIC)))
        self.assertEqual(rotos, {})

    def test_redirects_a_paginas_reales_sin_cadenas(self):
        for r in REDIRECTS:
            destino = r["destination"]
            with self.subTest(origen=r["source"]):
                self.assertNotIn(destino, ORIGENES)
                if destino.startswith("/"):
                    ruta = destino.split("#")[0].split("?")[0]
                    archivo = PUBLIC / ruta.strip("/")
                    self.assertTrue(ruta == "/" or archivo.is_file() or archivo.with_suffix(".html").is_file()
                                    or (archivo / "index.html").is_file(), destino)


class IndexacionTest(unittest.TestCase):
    def test_paginas_de_utilidad_con_noindex(self):
        for archivo in ("cuestionario.html", "gracias/index.html", "datos-envio/index.html"):
            with self.subTest(pagina=archivo):
                html = (PUBLIC / archivo).read_text(encoding="utf-8")
                self.assertIsNotNone(re.search(r'<meta name="robots" content="noindex, (?:no)?follow">', html))


if __name__ == "__main__":
    unittest.main()
