"""Plantilla de material (Etapa 2f): orden del spec §3.3, un H1, scripts, JSON-LD con el producto ligado a #negocio y
FAQPage igual a lo visible. MIGRADAS crece con cada tarea de migración hasta tener las cuatro páginas."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402

MIGRADAS = {"/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html",
            "/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",
            "/marmol-blanco-tampico": "marmol-blanco-tampico/index.html"}
ORDEN = ('id="vt-h1"', 'id="vt-h-precio"', 'id="vt-h-usos"', 'id="vt-h-calc"', 'id="vt-h-entrega"', 'id="vt-h-faq"',
         'id="vt-cierre-titulo"', 'id="vt-h-correo"')


def html_de(ruta):
    return (paginas.PUBLIC / MIGRADAS[ruta]).read_text(encoding="utf-8")


def grafo(html):
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]


class MaterialTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            posiciones = [html.find(marca) for marca in ORDEN]
            with self.subTest(ruta=ruta):
                self.assertNotIn(-1, posiciones)
                self.assertEqual(posiciones, sorted(posiciones))

    def test_un_h1_sin_css_viejo_y_con_sus_scripts(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(len(re.findall(r"<h1\b", html)), 1)
                for viejo in ("tailwind.css", "design-system.css", "servicios.css", "legacy-fixes", "fonts.googleapis"):
                    self.assertNotIn(viejo, html)
                self.assertIn('<script src="/js/vt-materiales.js" defer></script>', html)
                self.assertIn('<script src="/js/vt-b2b.js" defer></script>', html)

    def test_producto_ligado_al_negocio_sin_existencias(self):
        for ruta in MIGRADAS:
            producto = next(n for n in grafo(html_de(ruta)) if n["@type"] == "Product")
            with self.subTest(ruta=ruta):
                self.assertNotIn("InStock", json.dumps(producto))
                if "offers" in producto:
                    self.assertEqual(producto["offers"]["seller"], {"@id": f"{datos.SITIO}/#negocio"})

    def test_faqpage_igual_a_lo_visible(self):
        for ruta in MIGRADAS:
            html = html_de(ruta)
            faq = next(n for n in grafo(html) if n["@type"] == "FAQPage")
            visibles = [paridad.texto(s) for s in re.findall(r"<summary>(.*?)</summary>", paridad.principal(html), re.S)]
            with self.subTest(ruta=ruta):
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)


if __name__ == "__main__":
    unittest.main()
