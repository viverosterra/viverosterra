import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import medicion_js  # noqa: E402

LLAMADA = "window.VTMedicion&&VTMedicion.whatsapp("

CALCULADORA = """<script>
function enviarCalc(tipo){
  gtag('event','uso_calculadora',{'event_category':'engagement','value':m2});
  gtag('event','clic_wa_calculadora',{'event_category':'conversion','event_label':'pasto_calc_wa_'+tipo});
  window.open('https://wa.me/528333268008?text='+encodeURIComponent(msg),'_blank','noopener');
}
function enviarCTA(){
  gtag('event','clic_wa_cta_final',{'event_category':'conversion','event_label':'pasto_cta_final'});
  window.open('https://wa.me/528333268008?text='+encodeURIComponent(msg),'_blank','noopener');
}
</script>"""

SITIOS = """<button onclick="event.stopPropagation();window.open('https://wa.me/528333268008?text=Hola','_blank')">x</button>
<script>
function sendWA(msg){window.open('https://wa.me/528333268008?text='+encodeURIComponent(msg),'_blank','noopener');}
function sendToWhatsApp(){
  const url='https://wa.me/528333268008?text='+encodeURIComponent(msg);
  window.open(url,'_blank','noopener');
}
function buildLink(){ return `https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`; }
cta.addEventListener('click', function(ev){ ev.preventDefault();
  window.open(buildLink(), '_blank', 'noopener');
});
function otra(){ window.open(mapa,'_blank'); window.open('https://maps.app.goo.gl/x'); }
if (ok) window.open('https://wa.me/528333268008','_blank');
</script>"""


class EventosWhatsappTest(unittest.TestCase):
    def setUp(self):
        self.html, self.cuenta = medicion_js.medir_whatsapp_js(CALCULADORA)

    def test_eventos_clic_wa_pasan_al_helper_con_su_etiqueta(self):
        self.assertNotIn("clic_wa_", self.html)
        self.assertIn(LLAMADA + "'calculadora',{label:'pasto_calc_wa_'+tipo});", self.html)
        self.assertIn(LLAMADA + "'cta-final',{label:'pasto_cta_final'});", self.html)
        self.assertIn("gtag('event','uso_calculadora'", self.html)

    def test_sin_doble_medicion_antes_del_window_open(self):
        self.assertEqual(self.html.count(LLAMADA), 2)
        self.assertEqual(self.cuenta, {"eventos": 2, "aperturas": 0, "omitidas": 0})

    def test_idempotente(self):
        self.assertEqual(medicion_js.medir_whatsapp_js(self.html)[0], self.html)


class AperturasWhatsappTest(unittest.TestCase):
    def setUp(self):
        self.html, self.cuenta = medicion_js.medir_whatsapp_js(SITIOS)

    def test_agrega_el_helper_antes_de_cada_apertura_de_whatsapp(self):
        self.assertIn(f"event.stopPropagation();{LLAMADA}'boton');window.open('https://wa.me/", self.html)
        self.assertIn(f"function sendWA(msg){{{LLAMADA}'sendWA');window.open(", self.html)
        self.assertIn(f"  {LLAMADA}'sendToWhatsApp');window.open(url,", self.html)
        self.assertIn(f"  {LLAMADA}'buildLink');window.open(buildLink(),", self.html)

    def test_no_toca_aperturas_que_no_son_whatsapp_ni_las_que_no_son_sentencia(self):
        self.assertIn("function otra(){ window.open(mapa,'_blank'); window.open('https://maps", self.html)
        self.assertIn("if (ok) window.open('https://wa.me/", self.html)
        self.assertEqual(self.cuenta, {"eventos": 0, "aperturas": 4, "omitidas": 1})

    def test_idempotente(self):
        self.assertEqual(medicion_js.medir_whatsapp_js(self.html)[0], self.html)


if __name__ == "__main__":
    unittest.main()
