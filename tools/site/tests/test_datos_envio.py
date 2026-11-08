"""/datos-envio: la plantilla no toca el contrato con el asesor (?d=…) ni el texto #VT1 que arma el JavaScript."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paginas  # noqa: E402
from plantillas import formulario  # noqa: E402

K = generar.cargar("datos_envio").CONTENIDO
JS = (paginas.PUBLIC / "js" / "vt-datos-envio.js").read_text(encoding="utf-8")


class DatosEnvioTest(unittest.TestCase):
    def setUp(self):
        self.html = formulario.render(K)

    def test_noindex_nofollow_y_sin_formulario(self):
        self.assertEqual(K["meta"]["robots"], "noindex, nofollow")
        self.assertNotIn("<form", self.html)

    def test_cada_control_con_su_label(self):
        ids = set(re.findall(r'<label for="([^"]+)"', self.html))
        for etiqueta in re.findall(r"<(?:input|select)\b[^>]*>", self.html):
            if 'type="checkbox"' in etiqueta:
                continue
            with self.subTest(control=etiqueta[:60]):
                self.assertIn(re.search(r'id="([^"]+)"', etiqueta).group(1), ids)

    def test_el_mensaje_de_whatsapp_no_cambia(self):
        for pieza in ("Hola, aquí están mis datos de envío", "📍 *Dirección de entrega*", "📦 *Recibe*", "🧾 *Factura*",
                      "#VT1:${b64e({f:P.f||'',e,x})}", "'8333268008'", "location.href=url"):
            with self.subTest(pieza=pieza):
                self.assertIn(pieza, JS)

    def test_sin_manejadores_en_linea(self):
        self.assertNotRegex(self.html, r"\son(?:click|change)=")


if __name__ == "__main__":
    unittest.main()
