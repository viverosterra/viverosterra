"""Las filas de .vt-indice (home y hubs) tienen siempre los mismos 6 hijos, en el mismo orden.

Pedido del dueño (2026-11-17): en la home, la condición «Precio con terreno listo…» entraba como un hijo más de la fila,
caía en la columna de la flecha (24 px) y empujaba la flecha a un segundo renglón. El precio y su condición van ahora en
un solo bloque (.vt-indice__precio); esta prueba recorre todo public/ para que no vuelva a pasar en ninguna página.
"""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

ESPERADO = ["img", "span.vt-indice__n", "h3", "p", "div.vt-indice__precio", "span.vt-indice__ir"]


class _Filas(HTMLParser):
    """Junta, por cada <li> hijo directo de <ol class="vt-indice">, la lista de sus hijos directos (etiqueta.clase)."""

    VACIAS = {"img", "br", "hr", "input", "meta", "link", "source", "wbr"}

    def __init__(self):
        super().__init__()
        self.pila, self.filas = [], []

    def handle_starttag(self, tag, attrs):
        clase = dict(attrs).get("class") or ""
        padre = self.pila[-1] if self.pila else None
        if padre and padre[0] == "li" and padre[2]:
            primera = clase.split()[0] if clase else ""
            self.filas[-1].append(f"{tag}.{primera}" if primera else tag)
        en_indice = bool(padre) and padre[0] == "ol" and "vt-indice" in padre[1].split()
        if tag == "li" and en_indice:
            self.filas.append([])
        if tag not in self.VACIAS:
            self.pila.append((tag, clase, tag == "li" and en_indice))

    def handle_endtag(self, tag):
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == tag:
                del self.pila[i:]
                break


class IndiceEstructuraTest(unittest.TestCase):
    def test_cada_fila_del_indice_tiene_los_mismos_seis_hijos(self):
        revisadas = 0
        for archivo in sorted(paginas.PUBLIC.rglob("*.html")):
            html = archivo.read_text(encoding="utf-8")
            if 'class="vt-indice"' not in html:
                continue
            lector = _Filas()
            lector.feed(html)
            ruta = "/" + str(archivo.relative_to(paginas.PUBLIC)).removesuffix("index.html").rstrip("/")
            for n, hijos in enumerate(lector.filas, 1):
                with self.subTest(ruta=ruta, fila=n):
                    self.assertEqual(hijos, ESPERADO)
                revisadas += 1
        self.assertGreater(revisadas, 5, "debe haber filas de índice en la home y en los hubs")

    def test_la_condicion_del_precio_va_dentro_del_bloque_de_precio(self):
        html = (paginas.PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertRegex(html, r'<div class="vt-indice__precio"><p class="vt-indice__desde">.*?</p>'
                               r'<p class="vt-indice__cond">Precio con terreno listo')


if __name__ == "__main__":
    unittest.main()
