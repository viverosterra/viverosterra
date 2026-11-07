import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import huerfanos  # noqa: E402

# Página ya sin el menú viejo: quedan su CSS, su script con guarda y el CSS del botón flotante.
PAGINA = """<html><head>
<style>
/* ── NAVBAR ── */
.terra-nav { position: sticky; top: 0; }
.terra-nav.is-scrolled .terra-nav__inner { height: 58px; }
.terra-nav__links a:hover, .terra-nav__links button:hover { color: #1a5c1a; }
@media (max-width: 900px) {
  .terra-nav__links, .terra-nav__cta { display: none; }
}
</style>
<style>
.hero{color:red}
.wa-float{position:fixed;animation:pulse-wa 2.5s infinite}
@keyframes pulse-wa{0%,100%{opacity:1}70%{opacity:.5}}
@keyframes entra{from{opacity:0}to{opacity:1}}
.card{animation:entra 1s}
.logo-light{height:44px}
.terra-nav__cta, .btn-verde{background:#25d366}
header{background:#fff}
footer{padding:24px 0}
.tabs nav a{color:green}
@media(min-width:1024px){.layout-grid{display:grid}.terra-nav__dropdown{width:720px}}
</style>
</head><body>
<script>
(function() {
  var nav = document.querySelector('.terra-nav');
  if (!nav) return;
  nav.classList.add('is-scrolled');
})();
</script>
<section class="hero"><a class="btn-verde card" href="/">x</a></section>
<div class="tabs"><nav><a href="#a">a</a></nav></div>
<div class="layout-grid"></div>
<script>const mb=document.getElementById('menu-btn');if(mb&&mm)mb.addEventListener('click',()=>{});</script>
</body></html>
"""
QUITADOS = ['<header class="sticky"><nav><img class="logo-light"></nav></header>', '<footer class="bg-dark">f</footer>']


class CssHuerfanoTest(unittest.TestCase):
    def setUp(self):
        self.html, self.cuenta = huerfanos.limpiar(PAGINA, QUITADOS)

    def test_quita_reglas_que_solo_sirven_al_shell_viejo(self):
        for viejo in (".terra-nav {", ".terra-nav.is-scrolled", ".terra-nav__links", ".wa-float", "pulse-wa",
                      ".logo-light", "header{", "footer{", ".terra-nav__dropdown", "NAVBAR"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, self.html)

    def test_conserva_reglas_del_cuerpo_y_listas_mixtas(self):
        for vigente in (".hero{color:red}", "@keyframes entra", ".card{animation:entra 1s}",
                        ".terra-nav__cta, .btn-verde{background:#25d366}", ".tabs nav a{color:green}",
                        "@media(min-width:1024px){.layout-grid{display:grid}}"):
            with self.subTest(vigente=vigente):
                self.assertIn(vigente, self.html)

    def test_quita_bloques_vacios_y_el_script_con_guarda(self):
        self.assertEqual(self.html.count("<style>"), 1)
        self.assertNotIn("querySelector('.terra-nav')", self.html)
        self.assertIn("getElementById('menu-btn')", self.html)

    def test_cuenta_lo_quitado(self):
        self.assertEqual(self.cuenta["reglas"], 9)
        self.assertEqual(self.cuenta["keyframes"], 1)
        self.assertEqual(self.cuenta["bloques"], 1)
        self.assertEqual(self.cuenta["scripts"], 1)

    def test_idempotente(self):
        self.assertEqual(huerfanos.limpiar(self.html, [])[0], self.html)

    def test_header_que_sigue_en_el_cuerpo_conserva_su_regla(self):
        html = "<style>header{color:red}</style><body><article><header>h</header></article></body>"
        self.assertEqual(huerfanos.limpiar(html, ["<header><nav></nav></header>"])[0], html)

    def test_script_con_guarda_y_comentario_inicial(self):
        html = ("<body><script>\n/* ===== TERRA NAV JS ===== */\n(function() {\n  var nav = document.querySelector('.terra-nav');"
                "\n  if (!nav) return;\n  nav.remove();\n})();\n</script>\n<p>x</p></body>")
        self.assertEqual(huerfanos.limpiar(html, [])[0], "<body><p>x</p></body>")

    def test_selector_dentro_de_not_no_cuenta(self):
        html = "<style>a:not(.terra-nav){color:red}</style><body><a>x</a></body>"
        self.assertEqual(huerfanos.limpiar(html, [])[0], html)

    def test_clase_usada_por_un_script_se_conserva(self):
        html = "<style>.wa-float{color:red}</style><body><script>el.className='wa-float'</script></body>"
        self.assertEqual(huerfanos.limpiar(html, [])[0], html)


if __name__ == "__main__":
    unittest.main()
