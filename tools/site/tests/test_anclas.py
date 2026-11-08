"""Anclas: cada enlace <a href="#x"> o "/ruta#x" del sitio llega a un id que existe en esa página (Etapa 2g: la lista de
precios y las zonas cambian de plantilla y otras páginas enlazan /politicas#…, /pasto-sintetico#…). Desde la Etapa 2h el índice de cada
artículo se arma de los <h2> de su cuerpo: no puede apuntar a un id que no existe."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
SITIO = "https://www.viverosterra.com"
ENLACE_RE = re.compile(r'<a\b[^>]*\shref="([^"]*#[^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')
SCRIPT_RE = re.compile(r"<script\b(?![^>]*ld\+json)[^>]*>.*?</script>", re.S)


def rotas(public=PUBLIC):
    """{"/ruta#ancla": página que la enlaza} de las anclas que no existen en su página."""
    paginas_html = {paginas.ruta_de(p, public): p.read_text(encoding="utf-8") for p in Path(public).rglob("*.html")}
    ids = {ruta: set(ID_RE.findall(html)) for ruta, html in paginas_html.items()}
    salida = {}
    for ruta, html in paginas_html.items():
        for href in ENLACE_RE.findall(SCRIPT_RE.sub("", html)):
            href = href[len(SITIO):] if href.startswith(SITIO) else href
            if not href.startswith(("#", "/")) or href.startswith("//"):
                continue
            destino, _, ancla = href.partition("#")
            destino = destino.split("?")[0].rstrip("/") or ("/" if destino else ruta)
            if ancla not in ids.get(destino, ()):
                salida.setdefault(f"{destino}#{ancla}", ruta)
    return salida


class AnclasTest(unittest.TestCase):
    def test_toda_ancla_enlazada_existe(self):
        self.assertEqual(rotas(), {})


if __name__ == "__main__":
    unittest.main()
