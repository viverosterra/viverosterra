import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402


def existe(href):
    archivo = paginas.PUBLIC / href.lstrip("/")
    return archivo.is_file() or (archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file()


class PieTest(unittest.TestCase):
    def setUp(self):
        self.f = partials.footer(paginas.contexto("/blog"))

    def test_datos_del_pie(self):
        for texto in (datos.CALLE, datos.COLONIA, "Frente a Walmart", "Entrando por Banamex", datos.REPSE,
                      datos.PROMESA_COMPLETA, datos.GOOGLE, "desde 2012", datos.M2_INSTALADOS):
            with self.subTest(texto=texto):
                self.assertIn(texto, self.f)
        self.assertIn('data-cta="blog:footer" href="tel:+528333268008"', self.f)

    def test_correo_en_contacto(self):
        self.assertEqual(datos.CORREO_FORMULARIOS, "viverosterra@hotmail.com")
        self.assertIn(f'<li><a class="vt-foot__correo" href="mailto:{datos.CORREO_FORMULARIOS}">'
                      f'{datos.CORREO_FORMULARIOS}</a></li>', self.f)

    def test_barra_segun_contexto(self):
        self.assertIn("data-vt-bar", self.f)
        self.assertIn('data-cta="blog:barra"', self.f)
        for ruta in ("/pasto-sintetico", "/catalogo", "/gracias"):
            with self.subTest(ruta=ruta):
                self.assertNotIn("data-vt-bar", partials.footer(paginas.contexto(ruta)))

    def test_columnas_con_enlaces_existentes(self):
        for _titulo, enlaces in partials.PIE:
            for _texto, href in enlaces:
                with self.subTest(href=href):
                    self.assertTrue(existe(href))

    def test_sin_textos_viejos(self):
        for viejo in ("Blog de Jardinería", "líder", "Oasis", "Obregón 209,"):
            self.assertNotIn(viejo, self.f)

    def test_externos_con_noopener(self):
        html = partials.header(paginas.contexto("/")) + self.f
        for etiqueta in re.findall(r"<a\b[^>]*>", html):
            if 'target="_blank"' in etiqueta:
                self.assertIn('rel="noopener"', etiqueta)


if __name__ == "__main__":
    unittest.main()
