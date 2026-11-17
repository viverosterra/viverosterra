"""/pasto-sintetico/cuantos-rollos (Entrega B del SEO nacional, 2026-11-16): la calculadora sale ya calculada en el HTML
con el mismo cálculo que tools/pasto/rollos.py, llena el cotizador de la tienda, trae la tabla de medidas y los 32
estados con su flete, y queda enlazada desde el menú, la barra de la tienda, los cotizadores, llms.txt y el sitemap."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import componentes_rollos as cr  # noqa: E402
import data  # noqa: E402
import paginas  # noqa: E402
import rollos  # noqa: E402

PUBLIC = paginas.PUBLIC
RUTA = "/pasto-sintetico/cuantos-rollos"


def html(ruta=RUTA):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def principal(texto):
    return re.search(r"<main\b[^>]*>(.*)</main>", texto, re.S).group(1)


def texto_plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento)))


class CalculadoraTest(unittest.TestCase):
    def setUp(self):
        self.pagina = html()
        self.main = principal(self.pagina)

    def test_titulo_y_respuesta_directa(self):
        titulo = re.search(r"<title>(.*?)</title>", self.pagina).group(1)
        self.assertLessEqual(len(html_mod.unescape(titulo)), 60)
        self.assertIn("rollos de pasto sintético", html_mod.unescape(titulo).lower())
        lede = texto_plano(re.search(r'<p class="vt-lede"[^>]*>(.*?)</p>', self.pagina, re.S).group(1))
        self.assertIn("2 × 25 m", lede)
        self.assertIn("40 m²", lede)

    def test_resultado_inicial_igual_al_calculo(self):
        r = rollos.corte(*cr.EJEMPLO)
        for clave, esperado in (("m2", f'{r["m2"]} m²'), ("area", f'{r["area"]} m²'), ("tiras", cr.tiras_texto(r)),
                                ("rollos", cr.rollos_texto(r)), ("sobrante", f'{r["sobrante"]} m²')):
            with self.subTest(clave=clave):
                self.assertIn(f'<dd data-r="{clave}">{esperado}</dd>', self.main)
        self.assertRegex(self.main, rf'<input id="m2"[^>]*value="{r["m2"]}"')

    def test_scripts_en_orden(self):
        scripts = re.findall(r'<script[^>]+src="([^"]+)"', self.pagina)
        nombres = [s.rsplit("/", 1)[-1] for s in scripts]
        self.assertIn("vt-rollos.js", nombres)
        self.assertLess(nombres.index("tienda-pasto.js"), nombres.index("vt-rollos.js"))

    def test_sin_enlace_a_si_misma_desde_su_cotizador(self):
        self.assertNotIn("vt-cotizador__calc", self.main)

    def test_tabla_de_medidas(self):
        for f in rollos.tabla_medidas():
            self.assertIn(f'<b>{f["m2"]} m²</b>', self.main)

    def test_los_32_estados_con_su_flete(self):
        tabla = re.search(r'id="envio-por-estado".*?</table>', self.main, re.S).group(0)
        filas = re.findall(r'<tr><th scope="row">(.*?)</th>(.*?)</tr>', tabla, re.S)
        self.assertEqual(len(filas), 32)
        nombres = [texto_plano(n).split("  ")[0].strip() for n, _ in filas]
        for estado in data.ESTADOS_ORDEN:
            fila = next(celdas for n, celdas in filas if texto_plano(n).strip().startswith(estado))
            self.assertIn(componentes.dinero(data.ZONAS[data.zona_de(estado)]), fila, estado)
        self.assertEqual(len(nombres), 32)
        self.assertIn('href="/pasto-sintetico/envio/monterrey"', tabla)

    def test_faq_en_json_ld(self):
        bloques = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.pagina, re.S)]
        tipos = {t for b in bloques for n in b.get("@graph", [b])
                 for t in (n["@type"] if isinstance(n["@type"], list) else [n["@type"]])}
        self.assertTrue({"BreadcrumbList", "FAQPage"} <= tipos)

    def test_reglas_del_dueno(self):
        plano = texto_plano(self.main).lower()
        for prohibida in ("gratis", "sin costo", "más vendido", "oasis"):
            self.assertNotIn(prohibida, plano)


class EnlacesTest(unittest.TestCase):
    def test_enlazada_desde_menu_subnav_y_cotizadores(self):
        ficha = html("/pasto-sintetico/toscana-28")
        self.assertIn('class="vt-cotizador__calc" href="/pasto-sintetico/cuantos-rollos"', ficha)
        self.assertIn('<a href="/pasto-sintetico/cuantos-rollos">¿Cuántos rollos?</a>', ficha)
        inicio = (PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/pasto-sintetico/cuantos-rollos"', inicio)

    def test_en_llms_y_sitemap(self):
        self.assertIn(f"{data.SITE}{RUTA}", (PUBLIC / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn(RUTA, (PUBLIC / "llms.txt").read_text(encoding="utf-8"))


class PlanoTest(unittest.TestCase):
    def test_un_rectangulo_por_tira_mas_el_contorno(self):
        r = rollos.corte(5, 4)
        self.assertEqual(cr.plano(r).count("vt-rollos__tira "), r["tiras"])
        self.assertIn("vt-rollos__espacio", cr.plano(r))
        self.assertNotIn("vt-rollos__sobra", cr.plano(r))
        self.assertIn("vt-rollos__sobra", cr.plano(rollos.corte(7, 5)))

    def test_numeros_como_el_js(self):
        self.assertEqual([cr.num(v) for v in (5, 60.2, 4.30, 1200, 0)], ["5", "60.2", "4.3", "1,200", "0"])


if __name__ == "__main__":
    unittest.main()
