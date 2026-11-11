"""Plan visual V1 (2026-11-11, docs/ux/2026-11/plan-mejoras-visuales.md): sin texto repetido de relleno, tablas que
avisan que se deslizan y tarjetas de la tienda sin el botón encima del precio."""
import re
import unittest
from pathlib import Path

import datos

PUBLIC = Path(__file__).resolve().parents[3] / "public"
# Hero (línea de confianza), una herramienta de cotización como máximo, cierre y pie.
PROMESA_MAX = 4


def _visible(html):
    return re.sub(r"<(script|dialog)\b.*?</\1>", "", html, flags=re.S)


class VisualV1Test(unittest.TestCase):
    def test_la_promesa_de_respuesta_no_se_repite_bajo_cada_boton(self):
        for ruta in sorted(PUBLIC.rglob("*.html")):
            with self.subTest(ruta=ruta.relative_to(PUBLIC).as_posix()):
                self.assertLessEqual(_visible(ruta.read_text(encoding="utf-8")).count(datos.PROMESA_COMPLETA), PROMESA_MAX)

    def test_la_garantia_completa_sale_a_lo_mas_dos_veces(self):
        clave = datos.GARANTIA_PASTO[:40]
        for ruta in sorted(PUBLIC.rglob("*.html")):
            texto = re.sub(r"<[^>]+>", "", _visible(ruta.read_text(encoding="utf-8")))
            with self.subTest(ruta=ruta.relative_to(PUBLIC).as_posix()):
                self.assertLessEqual(texto.count(clave), 2)

    def test_tarjetas_de_la_tienda_boton_corto_en_celular_y_sin_nombre_repetido(self):
        html = (PUBLIC / "pasto-sintetico/index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<span class="vt-tarjeta-p__mas"> a mi lista</span>'), 9)
        self.assertNotRegex(html, r'vt-tarjeta-p__hoy">[^<]*Toscana')
        css = (PUBLIC / "css/terra-tienda.css").read_text(encoding="utf-8")
        self.assertIn(".vt-tienda .vt-tarjeta-p__mas{display:none}", css)

    def test_tablas_anchas_avisan_que_se_deslizan(self):
        for archivo, selector in (("terra-blog.css", ".vt-blog .vt-art__tabla::before"), ("terra-tienda.css", ".vt-tienda .vt-tabla-scroll::before")):
            with self.subTest(archivo=archivo):
                css = (PUBLIC / "css" / archivo).read_text(encoding="utf-8")
                self.assertIn(selector + '{content:"Desliza para ver toda la tabla →"', css)


if __name__ == "__main__":
    unittest.main()
