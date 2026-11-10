import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import shell  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}
PAGINA = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<title>Prueba</title>
<link rel="stylesheet" href="/css/tailwind.css?v=20260706">
<!-- vt:head -->
<!-- /vt:head -->
</head>
<body>
<!-- vt:header -->
<!-- /vt:header -->
<main id="main">
<!-- svc-hero --><a class="x" href="https://wa.me/528333268008?text=Hola">Hero</a><!-- /svc-hero -->
<p><a href="https://wa.me/528333268008?text=Hola">WhatsApp</a> <a href="tel:8333268008">Tel</a> <a href="/precios">Precios</a></p>
</main>
<!-- vt:footer -->
<!-- /vt:footer -->
</body>
</html>
"""


class ShellTest(unittest.TestCase):
    def test_llena_las_tres_regiones(self):
        html = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertIn('<header class="vt-head" data-vt-tipo="blog"', html)
        self.assertIn('<footer class="vt-foot">', html)
        self.assertEqual(html.count("googletagmanager.com/gtag/js"), 1)

    def test_idempotente(self):
        una = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertEqual(shell.aplicar(una, "/blog/palma-areca-tampico", URLS), una)

    def test_marca_ctas_del_hero_y_del_cuerpo(self):
        html = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertIn('<a data-cta="blog:hero" class="x" href="https://wa.me/528333268008?text=Hola">', html)
        self.assertIn('<a data-cta="blog:cuerpo" href="https://wa.me/528333268008?text=Hola">WhatsApp</a>', html)
        self.assertIn('<a data-cta="blog:cuerpo" href="tel:8333268008">Tel</a>', html)
        self.assertIn('<a href="/precios">Precios</a>', html)

    def test_hojas_por_clase_del_body_en_cualquier_orden(self):
        """La home lleva vt-inicio siempre y vt-temporada solo en temporada: cada hoja se decide por su clase, no por
        la cadena exacta del <body>."""
        urls = dict(URLS, **{f"terra-{n}.css": f"/css/terra-{n}.0123456789.css" for n in (
            "tienda", "plantas", "materiales", "precios", "util", "blog", "obras", "nochebuenas", "temporada", "inicio")})

        def hojas(clases):
            html = shell.aplicar(PAGINA.replace("<body>", f'<body class="{clases}">'), "/", urls)
            return sorted(re.findall(r'href="/css/(terra-[a-z]+)\.', html))

        self.assertEqual(hojas("vt-pagina vt-inicio vt-temporada"), ["terra-inicio", "terra-temporada"])
        self.assertEqual(hojas("vt-pagina vt-inicio"), ["terra-inicio"])
        self.assertEqual(hojas("vt-pagina vt-temporada"), ["terra-temporada"])
        self.assertEqual(hojas("vt-pagina vt-tienda"), ["terra-tienda"])
        self.assertEqual(hojas("vt-pagina vt-nochebuenas"), ["terra-nochebuenas"])
        self.assertEqual(hojas("vt-pagina vt-util"), ["terra-util"])  # etapa 2i: convive con las hojas de main
        self.assertEqual(hojas("vt-util vt-pagina vt-temporada"), ["terra-temporada", "terra-util"])
        self.assertEqual(hojas("vt-pagina vt-inicio-otra"), [])
        self.assertEqual(hojas("vt-pagina"), [])

    def test_falla_sin_regiones(self):
        with self.assertRaises(ValueError):
            shell.aplicar("<html><head></head><body></body></html>", "/", URLS)

    def test_fin_elemento_cuenta_anidados(self):
        html = '<nav class="a"><nav class="b"></nav></nav>resto'
        self.assertEqual(shell.fin_elemento(html, 0), html.index("resto"))

    def test_aplicar_archivo_solo_escribe_si_cambia(self):
        public = Path(tempfile.mkdtemp())
        pagina = public / "blog" / "palma-areca-tampico" / "index.html"
        pagina.parent.mkdir(parents=True)
        pagina.write_text(PAGINA, encoding="utf-8")
        self.assertTrue(shell.aplicar_archivo(pagina, URLS, public=public))
        self.assertFalse(shell.aplicar_archivo(pagina, URLS, public=public))


if __name__ == "__main__":
    unittest.main()
