import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import shell  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}
INDICE = """<!DOCTYPE html>
<html><head><title>Blog</title>
<!-- vt:head -->
<!-- /vt:head -->
</head><body>
<!-- vt:header -->
<!-- /vt:header -->
<main id="main"><p><span data-vt-conteo="blog">7</span> guías</p></main>
<!-- vt:footer -->
<!-- /vt:footer -->
</body></html>
"""


class ConteoBlogTest(unittest.TestCase):
    def test_el_build_pone_el_numero_real_de_articulos(self):
        public = Path(tempfile.mkdtemp())
        for slug in ("uno", "dos"):
            (public / "blog" / slug).mkdir(parents=True)
            (public / "blog" / slug / "index.html").write_text("<p>post</p>", encoding="utf-8")
        html = shell.aplicar(INDICE, "/blog", URLS, public=public)
        self.assertIn('<span data-vt-conteo="blog">2</span> guías', html)

    def test_solo_en_el_indice_del_blog(self):
        public = Path(tempfile.mkdtemp())
        html = shell.aplicar(INDICE, "/precios", URLS, public=public)
        self.assertIn('<span data-vt-conteo="blog">7</span> guías', html)


if __name__ == "__main__":
    unittest.main()
