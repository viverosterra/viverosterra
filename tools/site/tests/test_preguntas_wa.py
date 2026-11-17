"""Preguntas rápidas del WhatsApp (spec del primer mensaje, 2026-11-16)."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import preguntas_wa as p  # noqa: E402
from contenido import blog_clusters  # noqa: E402

SINTETICO = ([r for r, *_ in generar.PAGINAS if r.startswith("/pasto-sintetico")] + ["/pasto-sintetico-tampico"]
             + [f"/blog/{s}" for s in blog_clusters._SINTETICOS if s])


def leer(ruta):
    return (Path(paginas.PUBLIC) / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def fijo(ruta):
    return json.loads(re.search(r'id="vt-preguntas">(.*?)</script>', leer(ruta)).group(1))["fijo"]


class ConjuntoSinteticoTest(unittest.TestCase):
    def test_modelos_reales_y_no_se(self):
        modelo = p.SINTETICO["preguntas"][0]
        self.assertEqual(modelo["clave"], "modelo")
        self.assertEqual([o[0] for o in modelo["opciones"]], [m["slug"] for m in data.MODELOS] + ["no-se"])

    def test_rangos_y_destinos(self):
        self.assertEqual([q["clave"] for q in p.SINTETICO["preguntas"]], ["modelo", "m2", "destino"])
        self.assertEqual([o[0] for o in p.SINTETICO["preguntas"][1]["opciones"]], ["<25", "25-50", "50-100", ">100"])
        self.assertEqual([o[0] for o in p.SINTETICO["preguntas"][2]["opciones"]], ["recoger", "local", "envio"])
        self.assertEqual(p.SINTETICO["estados"], data.ESTADOS_ORDEN)

    def test_json_de_pagina(self):
        bloque = p.json_pagina({"modelo": "toscana-28"})
        self.assertTrue(bloque.startswith('<script type="application/json" id="vt-preguntas">'))
        cuerpo = json.loads(bloque.split(">", 1)[1].rsplit("</script>", 1)[0])
        self.assertEqual(cuerpo["fijo"], {"modelo": "toscana-28"})
        self.assertEqual(cuerpo["corto"], "Hola, tengo una pregunta sobre pasto sintético.")
        self.assertEqual(cuerpo["conjunto"]["id"], "sintetico")
        self.assertNotIn("</", bloque.split(">", 1)[1].rsplit("</script>", 1)[0])


class PaginasConPreguntasTest(unittest.TestCase):
    def test_paginas_de_sintetico_llevan_panel(self):
        for ruta in SINTETICO:
            html = leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(html.count('id="vt-preguntas"'), 1)
                self.assertRegex(html, r'<body class="[^"]*\bvt-preguntas\b')
                self.assertIn("/js/vt-preguntas.js", html)
                self.assertIn("terra-preguntas", html)

    def test_lo_fijo_de_cada_pagina(self):
        self.assertEqual(fijo("/pasto-sintetico/toscana-28"), {"modelo": "toscana-28"})
        self.assertEqual(fijo("/pasto-sintetico/envio/monterrey"), {"estado": "Nuevo León", "ciudad": "Monterrey"})
        self.assertEqual(fijo("/pasto-sintetico"), {})
        self.assertEqual(fijo("/pasto-sintetico-tampico"), {})

    def test_otras_paginas_sin_panel(self):
        for ruta in ("/", "/jardineria-altamira", "/blog/palma-areca-tampico", "/plantas-palmas-arboles-tampico"):
            with self.subTest(ruta=ruta):
                self.assertNotIn('id="vt-preguntas"', leer(ruta))
                self.assertNotIn("terra-preguntas", leer(ruta))


SERVICIOS = {"/pasto-en-rollo-tampico": "pasto", "/mantenimiento-jardines-tampico": "mantenimiento",
             "/poda-arboles-tampico": "poda", "/sistema-riego-tampico": "riego", "/diseno-jardines-tampico": "diseno"}


def datos_de(ruta):
    return json.loads(re.search(r'id="vt-preguntas">(.*?)</script>', leer(ruta)).group(1))


class ServiciosTest(unittest.TestCase):
    """Entrega 2 (spec del primer mensaje, 2026-11-16): los 5 servicios de Tampico."""

    def test_los_casos_de_node_usan_las_mismas_preguntas(self):
        fixture = Path(paginas.PUBLIC) / "js" / "tests" / "conjuntos-servicios.json"
        self.assertEqual(json.loads(fixture.read_text(encoding="utf-8")),
                         json.loads(json.dumps(p.SERVICIOS, ensure_ascii=False)))

    def test_frecuencias_de_datos(self):
        frecuencia = next(q for q in p.SERVICIOS["mantenimiento"]["preguntas"] if q["clave"] == "frecuencia")
        self.assertEqual([o[0] for o in frecuencia["opciones"]], list(p.datos.FRECUENCIAS_MANTENIMIENTO) + ["no-se"])

    def test_cada_servicio_con_su_panel_y_su_mensaje_general(self):
        for ruta, clave in SERVICIOS.items():
            html = leer(ruta)
            d = datos_de(ruta)
            with self.subTest(ruta=ruta):
                self.assertEqual(d["conjunto"]["id"], clave)
                self.assertTrue(d["corto"].startswith("Hola, tengo una pregunta sobre"))
                self.assertRegex(html, r'<body class="[^"]*\bvt-preguntas\b')
                self.assertIn("/js/vt-preguntas.js", html)
                hero = re.search(r'data-cta="servicio-[a-z]+:hero" href="https://wa\.me/\d+\?text=([^"]+)"', html).group(1)
                from urllib.parse import unquote
                self.assertEqual(unquote(hero), d["generico"] + "\n\n" + p.datos.FIRMA)


if __name__ == "__main__":
    unittest.main()
