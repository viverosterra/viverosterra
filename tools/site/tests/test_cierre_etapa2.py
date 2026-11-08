"""Cierre de la Etapa 2 (2i, Tarea 13): ninguna página carga CSS viejo y toda página de public/ sale de una plantilla."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
SITE = Path(__file__).resolve().parents[1]
VIEJOS = re.compile(r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|tienda-pasto|legacy-fixes)\b|<style\b")


class CierreEtapa2Test(unittest.TestCase):
    def test_ninguna_pagina_carga_estilos_viejos(self):
        con_viejo = {p.relative_to(PUBLIC).as_posix(): VIEJOS.search(p.read_text(encoding="utf-8")).group(0)
                     for p in PUBLIC.rglob("*.html") if VIEJOS.search(p.read_text(encoding="utf-8"))}
        self.assertEqual(con_viejo, {})

    def test_hojas_viejas_borradas(self):
        for hoja in ("tailwind.css", "design-system.css", "servicios.css", "tienda-pasto.css", "legacy-fixes.css"):
            with self.subTest(hoja=hoja):
                self.assertFalse((PUBLIC / "css" / hoja).exists())
        self.assertEqual(list((PUBLIC / "css").glob("legacy-fixes.*.css")), [])

    def test_toda_pagina_sale_de_una_plantilla(self):
        registradas = {salida for _ruta, salida, _plantilla, _contenido in generar.PAGINAS}
        publicadas = {p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*.html")}
        self.assertEqual(publicadas - registradas, set())

    def test_migrador_del_shell_retirado(self):
        for modulo in ("migrar_shell.py", "huerfanos.py"):
            with self.subTest(modulo=modulo):
                self.assertFalse((SITE / modulo).exists())


if __name__ == "__main__":
    unittest.main()
