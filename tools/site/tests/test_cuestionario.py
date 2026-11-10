"""/cuestionario: un H1, etiqueta en cada control, cinco pasos y medido como los demás formularios (generate_lead y _next a /gracias)."""
import html
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("cuestionario").CONTENIDO
JS = (paginas.PUBLIC / "js" / "vt-cuestionario.js").read_text(encoding="utf-8")


class CuestionarioTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)
        self.main = re.search(r"<main.*</main>", self.html, re.S).group(0)

    def test_destino_y_ocultos(self):
        self.assertIn(f'action="{componentes.FORMULARIO_ACCION}" method="POST"', self.main)
        for nombre, valor in (("_subject", "Nuevo cuestionario de jardín — Viveros Terra"),
                              ("_next", componentes.FORMULARIO_GRACIAS), ("_template", "table"), ("_captcha", "false")):
            self.assertIn(f'<input type="hidden" name="{nombre}" value="{valor}">', self.main)
        self.assertIn('name="_honey"', self.main)

    def test_mide_como_los_demas_formularios(self):
        """Envío nativo: formsubmit redirige a /gracias con _next (por /ajax/ respondería JSON) y el submit manda generate_lead."""
        self.assertIn('data-cta-form="cuestionario:formulario"', self.main)
        self.assertIn("'generate_lead'", JS)
        self.assertIn("method: 'formulario'", JS)
        self.assertNotIn("fetch(", JS)
        self.assertNotIn("success-screen", self.html)

    def test_un_h1_y_noindex(self):
        self.assertEqual(len(re.findall(r"<h1\b", self.html)), 1)
        self.assertEqual(K["meta"]["robots"], "noindex, follow")

    def test_cinco_pasos_y_solo_el_primero_visible(self):
        pasos = re.findall(r'<div class="vt-paso" id="page-\d" data-vt-paso="\d"([^>]*)>', self.main)
        self.assertEqual(pasos, ["", " hidden", " hidden", " hidden", " hidden"])

    def test_todo_control_visible_tiene_nombre_accesible(self):
        ids = set(re.findall(r'<label for="([^"]+)"', self.main))
        for etiqueta in re.findall(r"<(?:input|select|textarea)\b[^>]*>", self.main):
            if re.search(r'type="(?:hidden|radio|checkbox)"|name="_honey"', etiqueta):
                continue
            with self.subTest(control=etiqueta[:70]):
                self.assertIn(re.search(r'id="([^"]+)"', etiqueta).group(1), ids)
        self.assertEqual(self.main.count("<fieldset"), self.main.count("<legend>"))
        self.assertEqual(self.main.count("<fieldset"), 11)

    def test_whatsapp_exige_un_telefono_real(self):
        """El patrón se valida en el navegador al avanzar (test_util_navegador); aquí, que salga en el campo y qué acepta."""
        campo = re.search(r'<input [^>]*name="whatsapp"[^>]*>', self.main).group(0)
        patron = html.unescape(re.search(r'pattern="([^"]+)"', campo).group(1))
        self.assertRegex(campo, r'minlength="10"')
        self.assertRegex(campo, r'title="[^"]+"')
        self.assertIn('required', campo)
        for bueno in ("+52 833 000 0000", "8330000000", "(833) 000-0000"):
            with self.subTest(bueno=bueno):
                self.assertTrue(re.fullmatch(patron, bueno))
        for malo in ("abc", "12345", "----------", "          "):
            with self.subTest(malo=malo):
                self.assertFalse(re.fullmatch(patron, malo))

    def test_areas_aceptan_decimales(self):
        for nombre in ("area_pasto", "area_jardinera", "area_total"):
            with self.subTest(nombre=nombre):
                self.assertIn('step="any"', re.search(rf'<input [^>]*name="{nombre}"[^>]*>', self.main).group(0))

    def test_sin_javascript_ofrece_whatsapp(self):
        aviso = re.search(r"<noscript>(.*?)</noscript>", self.main, re.S).group(1)
        self.assertIn('href="https://wa.me/', aviso)
        self.assertIn('data-cta="cuestionario:sin-js"', aviso)

    def test_cada_seccion_con_su_propio_nombre(self):
        self.assertEqual(self.main.count('aria-labelledby="vt-h1"'), 1)
        self.assertRegex(self.main, r'<section class="vt-bloque" aria-label="[^"]+"><div class="vt-wrap vt-util__estrecho"><noscript>')

    def test_script_propio_sin_inline(self):
        self.assertIn('<script src="/js/vt-cuestionario.js" defer></script>', self.html)
        self.assertNotIn("onclick=", self.html)


if __name__ == "__main__":
    unittest.main()
