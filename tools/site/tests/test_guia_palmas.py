"""La guía de palmas en PDF se retiró por decisión del dueño (2026-11-07): sin oferta, sin PDF y con 301."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC


class GuiaPalmasTest(unittest.TestCase):
    def test_oferta_y_pdf_retirados(self):
        html = (PUBLIC / "palmas-mayoreo-proyectos" / "index.html").read_text(encoding="utf-8")
        for viejo in ('id="lead"', "lead-cta", "lead-email", "Guía gratuita", "Descargar guía", "Lead Magnet"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, html)
        self.assertIn('id="vt-h-faq"', html)  # la página sigue con sus preguntas (plantilla b2b desde la Etapa 2d)
        self.assertFalse((PUBLIC / "pdf" / "guia-12-palmas-arquitectos.pdf").exists())

    def test_ninguna_pagina_enlaza_la_guia(self):
        for path in PUBLIC.rglob("*.html"):
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                self.assertNotIn("guia-12-palmas", path.read_text(encoding="utf-8"))

    def test_la_url_del_pdf_redirige_a_palmas(self):
        redirects = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        destinos = {r["source"]: (r["destination"], r["permanent"]) for r in redirects}
        self.assertEqual(destinos.get("/pdf/guia-12-palmas-arquitectos.pdf"), ("/palmas-tropicales-tampico", True))


if __name__ == "__main__":
    unittest.main()
