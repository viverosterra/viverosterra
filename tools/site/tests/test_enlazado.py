"""Enlazado interno (SEO fase 0, 2026-11-10): las páginas que valen dinero reciben enlaces desde el contenido con un
ancla que dice qué hay y dónde ("Pasto en rollo en Tampico", "Vivero en Cd. Madero"), no "Ver X →"; y ningún artículo
del blog depende de un solo enlace (el del índice)."""
import html as html_mod
import re
import sys
import unittest
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402
import shell  # noqa: E402
from contenido import blog_clusters  # noqa: E402

ENLACE_RE = re.compile(r'<a\b[^>]*href="(/[^"#?]*)[^"]*"[^>]*>(.*?)</a>', re.S)
# Con un solo enlace entrante antes de la fase 0: ahora, al menos 3 páginas (el índice del blog y dos de su tema).
# (El cuarto, riego-automatico-tampico-roi, se fusionó con 301 en la guía de riego en la SEO fase 2c.)
POCO_ENLAZADOS = ("cuanto-cuesta-jardin-tampico-precios", "errores-pasto-san-agustin-tampico",
                  "jardin-en-macetas-terraza-tampico-guia")


def entrantes():
    """{destino: {página de origen: [anclas]}} de los enlaces internos del <main> de cada página."""
    salida = defaultdict(lambda: defaultdict(list))
    for path in shell.paginas_html():
        origen = paginas.ruta_de(path)
        cuerpo = re.search(r"<main\b.*</main>", path.read_text(encoding="utf-8"), re.S).group(0)
        for href, ancla in ENLACE_RE.findall(cuerpo):
            destino = href.rstrip("/") or "/"
            if destino != origen:
                texto = re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", "", ancla))).strip()
                salida[destino][origen].append(texto)
    return salida


ENTRANTES = entrantes()


class EnlazadoInternoTest(unittest.TestCase):
    def test_articulos_que_solo_enlazaba_el_indice(self):
        for slug in POCO_ENLAZADOS:
            origenes = ENTRANTES[f"/blog/{slug}"]
            with self.subTest(slug=slug):
                self.assertGreaterEqual(len(origenes), 3, sorted(origenes))

    def test_ningun_articulo_indexable_con_un_solo_enlace_entrante(self):
        solos = sorted(d for d, origenes in ENTRANTES.items() if d.startswith("/blog/") and len(origenes) < 2)
        self.assertEqual(solos, [])

    def test_vivero_y_pasto_en_rollo_enlazados_desde_el_contenido(self):
        self.assertGreaterEqual(len(ENTRANTES["/vivero-tampico"]), 20)
        self.assertGreaterEqual(len(ENTRANTES["/pasto-en-rollo-tampico"]), 25)
        pie = partials.footer(paginas.contexto("/"))
        self.assertIn('<a href="/pasto-en-rollo-tampico">Pasto en rollo en Tampico</a>', pie)
        # SEO fase 2b: el ancla del pie lleva el domicilio («Vivero en Cd. Madero · Obregón 209 Sur»).
        self.assertIn(f'<a href="/vivero-tampico">Vivero en Cd. Madero · {datos.CALLE_CORTA}</a>', pie)

    def test_el_cta_de_cada_articulo_nombra_el_servicio(self):
        """Antes: "Ver palmas →", "Ver mantenimiento →"… en 150 enlaces hacia las páginas de servicio."""
        for tema, datos_tema in blog_clusters.CLUSTERS.items():
            _href, texto = datos_tema["landing"]
            with self.subTest(tema=tema):
                self.assertNotRegex(texto, r"^Ver\b")
                self.assertGreaterEqual(len(texto.split()), 2)
                self.assertLessEqual(len(texto), 30, "a 320 px el botón se sale de la pantalla")
        self.assertEqual([t for _h, t in blog_clusters.LANDING.values() if t.startswith("Ver ")], [])

    def test_sin_anclas_ver_x_hacia_servicios_y_categorias(self):
        dinero = {href for _t, enlaces in partials.PIE[:2] for _x, href in enlaces} - {"/pasto-sintetico", "/catalogo"}
        hallazgos = sorted({f"{origen} → {destino} · {ancla}" for destino in dinero
                            for origen, anclas in ENTRANTES[destino].items() if origen != "/"
                            for ancla in anclas if re.match(r"Ver\b", ancla)})
        self.assertEqual(hallazgos, [])


if __name__ == "__main__":
    unittest.main()
