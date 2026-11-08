"""Componentes de la tienda (tools/site/componentes_tienda.py): marcado que leen tienda-pasto.js y tienda-hub.js,
números de tools/pasto/data.py y mensualidades con la fórmula oficial."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_tienda as t  # noqa: E402
import data  # noqa: E402
import datos  # noqa: E402

JS = Path(__file__).resolve().parents[3] / "public" / "js"
T28 = data.BY_SLUG["toscana-28"]


def ids(html):
    return set(re.findall(r'\bid="([^"]+)"', html))


class CotizadorTest(unittest.TestCase):
    def test_trae_cada_id_que_busca_tienda_pasto_js(self):
        js = (JS / "tienda-pasto.js").read_text(encoding="utf-8")
        html = (t.cotizador(T28) + t.lista_y_aviso() + t.barra_compra("X", "Desde $1/m²", "Hola", rollo=199)
                + t.json_modelo(T28) + t.json_modelos())
        buscados = set(re.findall(r"\$\('#([\w-]+)'\)", js)) - {"modelo", "gal-track", "gal-count"}
        self.assertEqual(sorted(buscados - ids(html)), [])
        for atributo in ("data-cta-wa", "data-plans", "data-plan-amount", "data-plan-total", "data-trip-contado",
                         "data-trip-mes", "data-trip-total", "data-plan-save", "data-cot-count", "data-toast-text",
                         "data-landed-bar"):
            with self.subTest(atributo=atributo):
                self.assertIn(atributo, html + t.subnav())

    def test_precios_y_estado_inicial_desde_data(self):
        html = t.cotizador(T28)
        self.assertIn('<td id="tier-rollo">$199/m²</td>', html)
        self.assertIn('<td id="tier-t2">$229/m²</td>', html)
        self.assertIn('<td id="tier-t1">$279/m²</td>', html)
        self.assertIn('<b id="q-material">$9,950</b>', html)
        self.assertIn('data-m2="50" aria-pressed="true"', html)
        tampico = t.cotizador(T28, modelos=data.MODELOS, m2=20, showroom=True, nivel=3)
        self.assertIn('<b id="q-material">$4,580</b>', tampico)
        self.assertIn('<option value="showroom" selected>', tampico)
        self.assertEqual(tampico.count('<option value="'), 2 + len(data.MODELOS))
        self.assertIn('<h3 class="vt-cotizador__t"', tampico)

    def test_whatsapp_con_mensaje_y_firma_sin_js(self):
        href = re.search(r'data-cta-wa data-cta="tienda:cotizador" href="([^"]+)"', t.cotizador(T28)).group(1)
        texto = unquote(href.split("text=", 1)[1])
        self.assertTrue(texto.startswith("Hola, quiero cotizar el pasto sintético Toscana 28."))
        self.assertTrue(texto.endswith(datos.FIRMA))

    def test_minimos_de_data_para_el_js_y_error_anunciado_una_vez(self):
        html = t.cotizador(T28)
        self.assertIn(f'data-min-nacional="{data.MIN_NACIONAL_M2}" data-min-showroom="{data.MIN_SHOWROOM_M2}"', html)
        self.assertIn('<p class="vt-cuenta__error" id="q-error"></p>', html)  # ya dentro de un aria-live
        self.assertNotIn('role="alert"', html)

    def test_textos_escapados(self):
        self.assertIn("<h2 class=\"vt-cotizador__t\" id=\"vt-h-cotizar\">A &amp; B &lt;x&gt;</h2>",
                      t.cotizador(T28, titulo="A & B <x>"))
        self.assertEqual(t.preguntas_h3((("¿<b>?", 'Ver <a href="/x">guía</a>'),)),
                         '<ul class="vt-recomendados"><li class="vt-recomendado"><h3>¿&lt;b&gt;?</h3><p>Ver '
                         '<a href="/x">guía</a></p></li></ul>')

    def test_forma_de_pago_con_los_plazos_oficiales(self):
        html = t.planes_cotizador("q")
        self.assertNotIn('role="radiogroup"', html)  # el fieldset con legend ya agrupa los radios
        for v in ("0", "3", "6", "9", "12"):
            self.assertIn(f'name="q-plan" value="{v}"', html)
        self.assertIn('value="0" checked', html)
        self.assertIn("/politicas#mensualidades", html)
        for prohibida in ("msi", "sin intereses", "0%", "recargo", "comisión"):
            self.assertNotIn(prohibida, html.lower())


class ListaYBarraTest(unittest.TestCase):
    def test_mi_lista_esconde_el_cero(self):
        self.assertIn('data-cot-count data-empty="true">0</span>', t.subnav())
        css = (JS.parent / "css" / "terra-tienda.css").read_text(encoding="utf-8")
        self.assertIn('.vt-tienda .vt-subnav__n[data-empty="true"]{display:none}', css)

    def test_barra_con_precio_puesto_solo_con_rollo(self):
        self.assertIn('data-landed-bar data-rollo="149"', t.barra_compra("T18", "Desde $149/m²", "Hola", rollo=149))
        self.assertNotIn("data-landed-bar", t.barra_compra("Tampico", "Instalado desde $385/m²", "Hola"))
        texto = unquote(re.search(r'href="[^"]+text=([^"]+)"', t.barra_compra("X", "Y", "Hola")).group(1))
        self.assertEqual(texto, datos.con_firma("Hola"))


class CatalogoTest(unittest.TestCase):
    def test_nueve_tarjetas_con_lo_que_lee_tienda_hub(self):
        html = t.catalogo()
        self.assertEqual(html.count('class="spec-card vt-tarjeta-p"'), 9)
        self.assertEqual(html.count("data-add="), 9)
        self.assertEqual(html.count("data-landed-slug="), 9)
        self.assertEqual(html.count('class="vt-regla"'), 9)
        self.assertEqual(html.count('class="vt-tarjeta-p__pago"'), 9)
        self.assertIn('id="filters-count"', html)
        self.assertEqual(html.count("data-filter="), len(data.USO_FILTERS))

    def test_para_llevar_hoy_solo_en_toscana_18_y_28(self):
        hoy = re.findall(r'<span class="vt-tarjeta-p__hoy">([^<]+)</span>', t.catalogo())
        self.assertEqual(hoy, [f"Toscana 18 para llevar hoy · {datos.CALLE_CORTA}",
                               f"Toscana 28 para llevar hoy · {datos.CALLE_CORTA}"])

    def test_regla_de_altura(self):
        self.assertIn('style="--w:100%"', t.regla_altura(35))
        self.assertIn('style="--w:29%"', t.regla_altura(10))
        self.assertIn('aria-label="Altura de fibra: 10 mm"', t.regla_altura(10))

    def test_selector_de_estados_completo(self):
        html = t.selector_estado("hero-estado")
        self.assertIn('<label for="hero-estado"', html)
        for e in data.ESTADOS_ORDEN:
            self.assertIn(f'value="{e}"', html)

    def test_selector_y_comparador(self):
        self.assertIn('id="quiz-result"', t.selector_modelo())
        self.assertEqual(t.selector_modelo().count('type="radio"'), 10)
        for i in ("comparador", "cmp-total", "cmp-m2", "cmp-out"):
            self.assertIn(f'id="{i}"', t.comparador())


class FichaTest(unittest.TestCase):
    def test_galeria_principal_nunca_lazy(self):
        html = t.galeria(T28)
        primera = re.search(r"<img [^>]+>", html).group(0)
        self.assertIn('loading="eager" fetchpriority="high"', primera)
        self.assertEqual(html.count("gallery__slide"), len(T28["gallery"]))
        self.assertIn("<b>Fig. 01</b>", html)
        self.assertEqual(t.foto_principal(T28)["src"], re.search(r'src="([^"]+)"', primera).group(1))

    def test_vecinos_y_agregar_con_sus_precios(self):
        html = t.comparativa(T28)
        self.assertEqual([m["slug"] for m in t.vecinos(T28)], ["irlanda-25", "viena-30"])
        self.assertEqual([m["slug"] for m in t.vecinos(data.MODELOS[0])], ["toscana-18", "capri-20"])
        agregar = [json.loads(b.replace("&quot;", '"')) for b in re.findall(r'data-agregar="([^"]+)"', html)]
        self.assertEqual([a["slug"] for a in agregar], ["irlanda-25", "toscana-28", "viena-30"])
        self.assertEqual(agregar[1], t.datos_modelo_js(T28))
        self.assertIn('aria-current="page"', html)

    def test_rollo_a_escala_de_50_m2(self):
        html = t.rollo_escala()
        for cota in ("25 m", "2 m", "50 m²"):
            self.assertIn(f">{cota}</text>", html)

    def test_existencia_nacional_y_para_llevar_hoy(self):
        for m in data.MODELOS:
            html = t.existencia(m)
            with self.subTest(modelo=m["slug"]):
                self.assertIn("En existencia", html)
                self.assertEqual("para llevar hoy" in html, m["slug"] in ("toscana-18", "toscana-28"))


class CiudadTest(unittest.TestCase):
    def test_totales_25_50_100_con_las_reglas_del_cotizador(self):
        aruba = data.BY_SLUG["aruba-10"]
        self.assertEqual(t.totales(aruba, "B"), [(25, 25 * 159 + 1150), (50, 50 * 139 + 1150), (100, 100 * 139 + 2300)])

    def test_mensualidad_maxima_con_la_formula_oficial(self):
        self.assertEqual(t.mensualidad_maxima(16200), "12 × ≈ $1,667")
        self.assertEqual(t.mensualidad_maxima(5125), "6 × ≈ $981")
        self.assertEqual(t.mensualidad_maxima(1500), "—")
        html = t.tabla_totales(t.barato(), "B")
        self.assertIn("$16,200", html)
        self.assertIn("$162/m²", html)
        self.assertIn("En mensualidades", html)


if __name__ == "__main__":
    unittest.main()
