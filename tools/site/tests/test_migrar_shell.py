import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import migrar_shell  # noqa: E402

BLOG = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<title>Post</title>
<meta name="keywords" content="pasto">
<meta name="geo.region" content="MX-TAM">
<link rel="icon" type="image/png" href="/img/logo.png">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RMZCVJ734M');
</script>
</head>
<body class="text-gray-900">
<a href="https://wa.me/528333268008?text=Hola" target="_blank" rel="noopener" class="wa-float flex">WA</a>
<header class="sticky top-0 z-50"><nav class="max-w-6xl"><nav aria-label="Breadcrumb"><a href="/">Inicio</a></nav><button id="menu-btn">m</button></nav></header>
<article class="bg-white"><header class="bg-dark"><h1>Título</h1></header>
<p>Texto <a href="https://wa.me/528333268008"
   onclick="gtag('event','clic_wa_final',{'event_category':'conversion','event_label':'x'})"
   target="_blank">WA</a></p></article>
<footer class="bg-dark"><p>Blog de Jardinería</p></footer>
<script>
  const mb=document.getElementById('menu-btn'),mm=document.getElementById('mobile-menu');
  mb.addEventListener('click',()=>{mm.classList.toggle('hidden');});
  function enviar(t){ gtag('event','clic_wa_calculadora',{'event_category':'conversion','event_label':'a_'+t}); }
</script>
</body>
</html>
"""

TERRA_NAV = """<!DOCTYPE html>
<html><head><title>Home</title>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
<script src="/js/nav-scroll.js?v=1" defer></script>
</head>
<body>
<!-- HEADER -->
<style>
.terra-nav{position:sticky;top:0}
.terra-nav__inner{height:64px}
@media (max-width:900px){.terra-nav__links{display:none}}
</style>
<nav class="terra-nav" data-page="/"><div class="terra-nav__inner"><nav class="sub"></nav></div><div class="terra-nav__drawer" id="terra-nav-drawer"></div></nav>
<section class="vt-hero"><h1>Pasto</h1></section>
<div class="vt-stickybar" role="region"><a href="tel:8333268008">Llamar</a></div>
<footer class="bg-dark">f</footer>
<script>
(function() {
  var nav = document.querySelector('.terra-nav');
  if (!nav) return;
  nav.classList.add('is-scrolled');
})();
</script>
</body></html>
"""

GRACIAS = """<!DOCTYPE html>
<html><head><title>Gracias</title></head>
<body>
<header><nav class="nav"><a href="/">Inicio</a></nav></header>
<main>
<h1>¡Gracias!</h1>
</main>
<footer>© 2026</footer>
</body></html>
"""

CATALOGO = """<!DOCTYPE html>
<html><head><title>Catálogo</title></head>
<body>
<nav class="terra-nav" data-page="/catalogo"></nav>
<nav class="tabs" aria-label="Categorías"><button>Palmas</button></nav>
<main class="grid" id="grid" aria-label="Catálogo de plantas"></main>
<footer style="background:#000">f</footer>
</body></html>
"""


class MigrarBlogTest(unittest.TestCase):
    def setUp(self):
        self.html = migrar_shell.migrar(BLOG)

    def test_quita_shell_viejo_y_deja_el_header_del_articulo(self):
        self.assertNotIn("wa-float", self.html)
        self.assertNotIn('class="sticky', self.html)
        self.assertNotIn('id="menu-btn"', self.html)
        self.assertNotIn("<footer", self.html)
        self.assertIn('<header class="bg-dark"><h1>Título</h1></header>', self.html)

    def test_quita_gtag_meta_iconos_y_eventos_clic(self):
        for viejo in ("googletagmanager", "keywords", "geo.region", 'rel="icon"', "clic_"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, self.html)
        self.assertIn('href="https://wa.me/528333268008"\n   target="_blank">WA</a>', self.html)

    def test_protege_el_script_de_menu_sin_guarda(self):
        self.assertIn("if(mb&&mm)mb.addEventListener('click'", self.html)

    def test_regiones_y_main(self):
        for region in ("head", "header", "footer"):
            self.assertEqual(self.html.count(f"<!-- vt:{region} -->"), 1)
            self.assertEqual(self.html.count(f"<!-- /vt:{region} -->"), 1)
        self.assertEqual(self.html.count('<main id="main">'), 1)
        self.assertLess(self.html.index('<main id="main">'), self.html.index("<article"))
        self.assertIn("</main>\n<!-- vt:footer -->", self.html)
        self.assertLess(self.html.index("<!-- vt:head -->"), self.html.index("</head>"))

    def test_idempotente(self):
        self.assertEqual(migrar_shell.migrar(self.html), self.html)


class MigrarOtrasFamiliasTest(unittest.TestCase):
    def test_terra_nav_y_barra_vieja_de_la_home(self):
        html = migrar_shell.migrar(TERRA_NAV)
        for viejo in ('class="terra-nav"', "terra-nav-drawer", "vt-stickybar", "nav-scroll.js", "googletagmanager", "<footer"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, html)
        self.assertIn('<section class="vt-hero"><h1>Pasto</h1></section>', html)
        self.assertEqual(html.count('<main id="main">'), 1)

    def test_main_existente_recibe_id(self):
        html = migrar_shell.migrar(GRACIAS)
        self.assertNotIn('<nav class="nav"', html)
        self.assertEqual(html.count("<main"), 1)
        self.assertIn('<main id="main">\n<h1>¡Gracias!</h1>', html)

    def test_main_del_catalogo_pasa_a_div(self):
        html = migrar_shell.migrar(CATALOGO)
        self.assertIn('<div role="region" class="grid" id="grid" aria-label="Catálogo de plantas"></div>', html)
        self.assertIn('<nav class="tabs" aria-label="Categorías">', html)
        self.assertEqual(html.count("<main"), 1)
        self.assertIn('<main id="main">', html)


class LimpiezaYMedicionTest(unittest.TestCase):
    def test_quita_css_y_script_huerfanos_del_menu_viejo(self):
        cuenta = {}
        html = migrar_shell.migrar(TERRA_NAV, "/", cuenta)
        self.assertNotIn("terra-nav", html)
        self.assertNotIn("<style>", html)
        self.assertEqual((cuenta["reglas"], cuenta["bloques"], cuenta["scripts"]), (3, 1, 1))

    def test_evento_de_calculadora_pasa_al_helper(self):
        html = migrar_shell.migrar(BLOG, "/blog/post")
        self.assertIn("window.VTMedicion&&VTMedicion.whatsapp('calculadora',{label:'a_'+t});", html)

    def test_boton_flotante_fab_de_las_paginas_de_plantas(self):
        pagina = (
            "<html><head><style>.fab{position:fixed;bottom:20px}\n.fab:hover{transform:scale(1.1)}\n.card{color:red}</style>"
            "</head><body><main><h1>Palmas</h1></main>"
            '<a class="fab" href="https://wa.me/528333268008?text=Hola" target="_blank" rel="noopener" aria-label="WhatsApp">'
            "<svg></svg></a></body></html>"
        )
        cuenta = {}
        html = migrar_shell.migrar(pagina, "/palmas-tropicales-tampico", cuenta)
        self.assertNotIn('class="fab"', html)
        self.assertNotIn(".fab", html)
        self.assertIn(".card{color:red}", html)


class MigasBlogTest(unittest.TestCase):
    def test_articulo_recibe_ruta_visible_al_inicio_del_main(self):
        html = migrar_shell.migrar(BLOG, "/blog/post")
        self.assertIn(
            '<main id="main">\n<nav class="vt-crumbs" aria-label="Ruta de navegación"><ol class="vt-wrap">'
            '<li><a href="/">Inicio</a></li><li><a href="/blog">Blog</a></li><li aria-current="page">Título</li></ol></nav>',
            html,
        )

    def test_sin_ruta_duplicada_ni_fuera_del_blog(self):
        con_migas = BLOG.replace("<article", '<nav aria-label="Breadcrumb"><a href="/">Inicio</a></nav><article', 1)
        self.assertNotIn("vt-crumbs", migrar_shell.migrar(con_migas, "/blog/post"))
        self.assertNotIn("vt-crumbs", migrar_shell.migrar(BLOG, "/blog"))
        self.assertNotIn("vt-crumbs", migrar_shell.migrar(BLOG))

    def test_titulo_sin_etiquetas_y_escapado(self):
        html = BLOG.replace("<h1>Título</h1>", "<h1>Pasto <em>San Agustín</em> &amp; riego</h1>")
        self.assertIn('<li aria-current="page">Pasto San Agustín &amp; riego</li>', migrar_shell.migrar(html, "/blog/x"))


if __name__ == "__main__":
    unittest.main()
