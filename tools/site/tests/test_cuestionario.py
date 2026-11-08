"""/cuestionario: un H1, etiqueta en cada control, cinco pasos y medido como los demás formularios (generate_lead y _next a /gracias)."""
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

    def test_script_propio_sin_inline(self):
        self.assertIn('<script src="/js/vt-cuestionario.js" defer></script>', self.html)
        self.assertNotIn("onclick=", self.html)


if __name__ == "__main__":
    unittest.main()
