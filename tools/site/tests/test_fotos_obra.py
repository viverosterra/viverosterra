"""Mosaico de fotos reales por página (etapa de fotos): datos, archivos sin metadatos y HTML del componente."""
import json
import re
import sys
import unittest
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools" / "site"))

import activos  # noqa: E402
import componentes as c  # noqa: E402
from contenido import fotos_obra  # noqa: E402
from test_terra_css import sin_comentarios  # noqa: E402

PUBLIC = RAIZ / "public"
DATOS = json.loads((RAIZ / "tools" / "site" / "contenido" / "fotos_obra.json").read_text(encoding="utf-8"))


class DatosTest(unittest.TestCase):
    def test_cada_foto_tiene_alt_pie_etapa_y_archivo(self):
        for ruta, pagina in DATOS.items():
            for f in pagina["figuras"]:
                with self.subTest(ruta=ruta, src=f["src"]):
                    self.assertTrue(f["alt"] and f["lugar"] and f["etapa"])
                    self.assertTrue((PUBLIC / f["src"].lstrip("/")).is_file())

    def test_ningun_mosaico_deja_huerfana_en_tres_columnas(self):
        for ruta, pagina in DATOS.items():
            with self.subTest(ruta=ruta):
                self.assertNotEqual(len(pagina["figuras"]) % 3, 1)

    def test_las_fotos_no_llevan_metadatos_ni_rebasan_1200_px(self):
        for f in (PUBLIC / "img" / "obra" / "terra").glob("*.webp"):
            with self.subTest(archivo=f.name), Image.open(f) as img:
                self.assertLessEqual(max(img.size), 1200)
                self.assertFalse(img.info.get("exif") or img.info.get("xmp"))

    def test_no_se_repite_ninguna_foto(self):
        fuentes = [f["src"] for p in DATOS.values() for f in p["figuras"]]
        self.assertEqual(len(fuentes), len(set(fuentes)))


class HojaTest(unittest.TestCase):
    def setUp(self):
        self.css = sin_comentarios((PUBLIC / "css" / "terra-obras.css").read_text(encoding="utf-8"))

    def test_todo_bajo_el_mosaico_sin_colores_ni_important(self):
        for selector in re.findall(r"([^{}]+)\{", self.css):
            if not selector.strip().startswith("@media"):
                for parte in re.split(r",(?![^(]*\))", selector):
                    self.assertTrue(parte.strip().startswith(".vt-mosaico"), parte)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", self.css), [])
        self.assertNotIn("!important", self.css)

    def test_presupuesto(self):
        self.assertLess(len(activos.minificar_css(self.css).encode("utf-8")), 2 * 1024)


class ComponenteTest(unittest.TestCase):
    FIGURAS = tuple({"src": f"/f{i}.webp", "ancho": 800, "alto": 600, "alt": f"Foto {i}", "lugar": "Pie", "etapa": "Terminado"}
                    for i in range(5))

    def test_numera_desde_el_indicado_y_solo_carga_diferida(self):
        html = c.mosaico(self.FIGURAS, desde=7)
        self.assertEqual(re.findall(r"Fig\. (\d+)", html), ["07", "08", "09", "10", "11"])
        self.assertNotIn('loading="eager"', html)

    def test_la_primera_es_ancha_solo_si_llena_la_reticula(self):
        self.assertNotIn("vt-mosaico--plano", c.mosaico(self.FIGURAS, desde=1))
        self.assertIn("vt-mosaico--plano", c.mosaico(self.FIGURAS[:3], desde=1))

    def test_seccion_por_ruta(self):
        self.assertIsNone(fotos_obra.seccion("/no-existe"))
        self.assertEqual(fotos_obra.seccion("https://www.viverosterra.com/diseno-jardines-tampico")["titulo"],
                         DATOS["/diseno-jardines-tampico"]["titulo"])


class PaginasTest(unittest.TestCase):
    def test_cada_pagina_trae_su_mosaico_y_su_hoja(self):
        for ruta, pagina in DATOS.items():
            with self.subTest(ruta=ruta):
                html = (PUBLIC / ruta.lstrip("/") / "index.html").read_text(encoding="utf-8")
                self.assertIn('class="vt-mosaico', html)
                self.assertIn("/css/terra-obras.", html)
                self.assertIn(pagina["figuras"][0]["src"], html)

    def test_las_demas_paginas_no_cargan_la_hoja(self):
        self.assertNotIn("terra-obras", (PUBLIC / "precios" / "index.html").read_text(encoding="utf-8"))

    def test_el_jardin_de_referencia_ya_es_foto_de_obra(self):
        for pagina in ("index.html", "pasto-en-rollo-tampico/index.html"):
            html = (PUBLIC / pagina).read_text(encoding="utf-8")
            self.assertNotIn("Proyecto · referencia", html)
            self.assertIn("/img/obra/terra/jardin-residencial-pasto-alberca.webp", html)


if __name__ == "__main__":
    unittest.main()
