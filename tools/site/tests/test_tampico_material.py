"""Tienda, subproyecto 1 (2026-11-12, docs/superpowers/specs/2026-11-12-tampico-material-primero-design.md):
/pasto-sintetico-tampico muestra primero el material (desde el rollo más barato) y deja la instalación como segunda
opción, en la misma URL, sin fotos, precios ni plazos nuevos."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pasto"))

import data  # noqa: E402
import datos  # noqa: E402
import paginas  # noqa: E402
from componentes import dinero_exacto  # noqa: E402

HTML = (paginas.PUBLIC / "pasto-sintetico-tampico" / "index.html").read_text(encoding="utf-8")
MIN = min(m["rollo"] for m in data.MODELOS)
MAX = max(m["t1"] for m in data.MODELOS)
INST = dinero_exacto(datos.PRECIOS["sintetico_instalado_m2"][0])


def texto(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def meta(nombre):
    return html_mod.unescape(re.search(rf'name="{nombre}" content="([^"]*)"', HTML).group(1))


def titulos_h2():
    return [texto(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", HTML, re.S)]


class MaterialPrimeroTest(unittest.TestCase):
    def test_titulo_lleva_el_precio_del_material(self):
        titulo = html_mod.unescape(re.search(r"<title>([^<]*)", HTML).group(1))
        self.assertEqual(titulo, f"Pasto Sintético Tampico desde ${MIN}/m² · Material o Instalado")
        self.assertLessEqual(len(titulo), 60)

    def test_descripcion_empieza_por_comprar(self):
        d = meta("description")
        self.assertTrue(d.startswith(f"Compra pasto sintético en Tampico desde ${MIN}/m²"), d)
        self.assertIn(f"Instalado desde {INST}/m²", d)
        self.assertLessEqual(len(d), 155)

    def test_h1_y_etiqueta(self):
        h1 = texto(re.search(r"<h1[^>]*>(.*?)</h1>", HTML, re.S).group(1))
        self.assertEqual(h1, "Pasto sintético en Tampico material o instalado")
        portada = texto(HTML[HTML.find("<h1"):HTML.find("En corto")])
        self.assertLess(portada.find(f"${MIN}"), portada.find(INST), portada)

    def test_en_corto_empieza_con_el_material(self):
        i = HTML.find("En corto")
        corto = texto(HTML[i:i + 1500])
        self.assertLess(corto.find(f"${MIN}"), corto.find(INST))

    def test_opciones_y_calculadora_antes_de_la_prueba(self):
        h2 = titulos_h2()
        orden = [h2.index(x) for x in ("Compra el material o te lo instalamos", "Calcula tu material y llévatelo",
                                        "Precio del pasto sintético en Tampico", "Pasto sintético instalado en la región",
                                        "Cómo instalamos en Tampico y Madero")]
        self.assertEqual(orden, sorted(orden), h2)

    def test_la_recomendada_es_el_material(self):
        rec = re.search(r'class="vt-modo vt-modo--rec".*?</h3>', HTML, re.S)
        self.assertIn("Compras el material", texto(rec.group(0)))

    def test_preguntas_de_compra_primero_y_hazlo_tu(self):
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))
        faq = next(n for n in ld["@graph"] if n["@type"] == "FAQPage")
        nombres = [q["name"] for q in faq["mainEntity"]]
        self.assertEqual(nombres[:2], ["¿Dónde comprar pasto sintético en Tampico?",
                                       "¿Cuánto cuesta el pasto sintético por m² en Tampico?"])
        self.assertIn("¿Puedo instalarlo yo mismo?", nombres)
        self.assertIn('href="/blog/como-instalar-pasto-sintetico"', HTML)

    def test_product_del_material(self):
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))
        prod = next(n for n in ld["@graph"] if n["@type"] == "Product")
        oferta = prod["offers"]
        self.assertEqual((oferta["@type"], oferta["lowPrice"], oferta["highPrice"], oferta["priceCurrency"]),
                         ("AggregateOffer", f"{MIN:.2f}", f"{MAX:.2f}", "MXN"))
        self.assertTrue(any(n["@type"] == "Service" for n in ld["@graph"]))

    def test_sin_frases_prohibidas(self):
        self.assertNotRegex(HTML, r"(?i)sin costo|gratis|más vendid")
        js = (paginas.PUBLIC / "js" / "tienda-pasto.js").read_text(encoding="utf-8")
        self.assertNotIn("Sin costo", js)


if __name__ == "__main__":
    unittest.main()
