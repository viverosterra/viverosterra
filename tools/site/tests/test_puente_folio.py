"""Tienda, subproyecto 2 (2026-11-13, docs/superpowers/specs/2026-11-13-puente-web-cotizador-design.md): el WhatsApp
de la tienda termina con "Folio web: …" (public/js/vt-folio.js) y el cotizador de Netlify lo lee al pegarlo."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pasto"))

import data  # noqa: E402
import paginas  # noqa: E402

JS = paginas.PUBLIC / "js"
FOLIO_JS = (JS / "vt-folio.js").read_text(encoding="utf-8")
TIENDA_JS = (JS / "tienda-pasto.js").read_text(encoding="utf-8")
PAGINAS = ("pasto-sintetico", "pasto-sintetico/toscana-28", "pasto-sintetico/envio/monterrey",
           "pasto-sintetico-tampico")


def html(ruta):
    return (paginas.PUBLIC / ruta / "index.html").read_text(encoding="utf-8")


def bloque(texto, nombre):
    return re.search(rf"const {nombre} = (?:Object\.freeze\()?\{{(.*?)\}}\)?;", texto, re.S).group(1)


def claves(cuerpo):
    return set(re.findall(r"'([^']+)':", cuerpo))


class Folio(unittest.TestCase):
    def test_codigos_de_modelo_unicos(self):
        codigos = [m["slug"][0].upper() + re.search(r"(\d+)$", m["slug"]).group(1) for m in data.MODELOS]
        self.assertEqual(len(codigos), len(set(codigos)), codigos)

    def test_estados_iguales_a_la_tienda(self):
        self.assertEqual(claves(bloque(FOLIO_JS, "ESTADOS")), claves(bloque(TIENDA_JS, "ESTADO_ZONA")))

    def test_paginas_cargan_el_folio_antes_de_la_tienda(self):
        for ruta in PAGINAS:
            with self.subTest(ruta=ruta):
                h = html(ruta)
                self.assertIn('src="/js/vt-folio.js"', h)
                self.assertLess(h.index("/js/vt-folio.js"), h.index("/js/tienda-pasto.js"))

    def test_caja_del_folio_sobre_el_boton(self):
        for ruta in (r for r in PAGINAS if "/envio/" not in r):  # las de ciudad no traen cotizador
            with self.subTest(ruta=ruta):
                h = html(ruta)
                caja = re.search(r'<div class="vt-folio" id="q-folio" hidden>.*?</div>', h, re.S)
                self.assertIsNotNone(caja)
                self.assertIn("Ya tienes todo listo", caja.group(0))
                self.assertIn("Sin compromiso y sin llenar formularios", caja.group(0))
                self.assertLess(h.index('id="q-folio"'), h.index("data-cta-wa data-cta="))
                self.assertNotRegex(caja.group(0).lower(), r"gratis|sin costo|más vendido")

    def test_mensajes_llevan_el_folio(self):
        self.assertEqual(TIENDA_JS.count("folioLinea("), 2)  # cotizador y lista
        self.assertIn("Enviar mi cotización por WhatsApp", TIENDA_JS)


if __name__ == "__main__":
    unittest.main()
