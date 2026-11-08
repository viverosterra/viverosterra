"""Anclas: cada enlace <a href="#x"> o "/ruta#x" del sitio llega a un id que existe en esa página (Etapa 2g: la lista de
precios y las zonas cambian de plantilla y otras páginas enlazan /politicas#…, /pasto-sintetico#…). PENDIENTES son los
índices de tres artículos del blog que ya estaban rotos en main; los arregla la Etapa 2h y la lista solo puede encoger."""
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
PENDIENTES = frozenset(
    f"/blog/{post}#{ancla}"
    for post, anclas in (
        ("cuando-plantar-pasto-tampico-calendario",
         ("como-plantarlos", "el-problema-real", "errores-comunes", "mejores-arboles", "reglas-de-oro")),
        ("plantas-resistentes-sal-golfo-tampico",
         ("como-plantarlos", "el-problema-real", "errores-comunes", "mejores-arboles", "reglas-de-oro")),
        ("sistema-riego-automatico-conviene-tampico",
         ("como-plantarlos", "el-problema-real", "mejores-arboles", "reglas-de-oro")),
    ) for ancla in anclas)


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
        self.assertEqual({k: v for k, v in rotas().items() if k not in PENDIENTES}, {})

    def test_pendientes_siguen_rotas(self):
        self.assertEqual(sorted(PENDIENTES - set(rotas())), [], "ya existen: sácalas de PENDIENTES")


if __name__ == "__main__":
    unittest.main()
