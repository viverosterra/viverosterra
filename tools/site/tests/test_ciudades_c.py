"""Entrega C del SEO nacional (2026-11-16): ciudades diferenciadas y 8 nuevas."""
import html as html_mod
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import rollos  # noqa: E402
from ciudades import CIUDADES, NUEVAS  # noqa: E402
from contenido import ciudad  # noqa: E402

PUBLIC = Path(paginas.PUBLIC)
ESPERADAS = ("saltillo", "torreon", "chihuahua", "hermosillo", "tijuana", "aguascalientes", "toluca", "morelia")


def html(ruta):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def principal(texto):
    return re.search(r"<main\b.*?</main>", texto, re.S).group(0)


def plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento)))


class CiudadesNuevasTest(unittest.TestCase):
    def test_las_8_ciudades_nuevas_con_pagina_y_sin_captura(self):
        self.assertEqual(NUEVAS, ESPERADAS)
        self.assertEqual(len(CIUDADES), 19)
        rutas = {r for r, *_ in generar.PAGINAS}
        for slug in ESPERADAS:
            with self.subTest(slug=slug):
                self.assertIn(f"/pasto-sintetico/envio/{slug}", rutas)
                self.assertIn(f"/pasto-sintetico/envio/{slug}", generar.NUEVAS)

    def test_su_estado_tiene_flete(self):
        for x in CIUDADES:
            with self.subTest(slug=x["slug"]):
                self.assertIsNotNone(data.zona_de(x["estado"]))

    def test_aparecen_en_hub_sitemap_llms_y_tabla_de_estados(self):
        hub = html("/pasto-sintetico")
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
        tabla = html("/pasto-sintetico/cuantos-rollos")
        for slug in ESPERADAS:
            ruta = f"/pasto-sintetico/envio/{slug}"
            with self.subTest(slug=slug):
                self.assertIn(f'href="{ruta}"', hub)
                self.assertIn(f"https://www.viverosterra.com{ruta}</loc>", sitemap)
                self.assertIn(ruta, llms)
                self.assertIn(f'href="{ruta}"', tabla)


class CiudadesDiferenciadasTest(unittest.TestCase):
    def test_sin_la_opinion_de_tampico(self):
        for x in CIUDADES:
            with self.subTest(slug=x["slug"]):
                self.assertNotIn("Cafetería en el centro de Tampico", html(f"/pasto-sintetico/envio/{x['slug']}"))
        # La página de perros la conserva.
        self.assertIn("Cafetería en el centro de Tampico", html("/pasto-sintetico/perros"))

    def test_textos_propios_no_se_repiten(self):
        for campo in ("intro", "clima", "terreno"):
            with self.subTest(campo=campo):
                valores = [x[campo] for x in CIUDADES]
                self.assertEqual(len(set(valores)), len(valores))
        preguntas = [q for x in CIUDADES for q, _a in x["faqs"]]
        self.assertEqual(len(set(preguntas)), len(preguntas))

    def test_modelos_recomendados_existen(self):
        slugs = {m["slug"] for m in data.MODELOS}
        for x in CIUDADES:
            with self.subTest(slug=x["slug"]):
                self.assertEqual(len(x["modelos"]), 3)
                self.assertTrue({s for s, _r in x["modelos"]} <= slugs)
                self.assertTrue(set(x["ejemplo"][3:]) <= slugs)

    def test_seccion_antes_de_instalar(self):
        for x in CIUDADES:
            cuerpo = principal(html(f"/pasto-sintetico/envio/{x['slug']}"))
            with self.subTest(slug=x["slug"]):
                self.assertIn(f"Antes de instalar en {x['nombre']}", cuerpo)
                self.assertIn(f"<h3>¿Cómo preparo el terreno en {x['nombre']}?</h3>", cuerpo)
                self.assertIn('href="/pasto-sintetico/cuantos-rollos"', cuerpo)
                self.assertIn('href="/pasto-sintetico/cuantos-rollos#envio-por-estado"', cuerpo)

    def test_ejemplo_con_la_calculadora_y_las_reglas_del_cotizador(self):
        # Monterrey, 12 × 7 m con Irlanda 25: 84 m²; 6 tiras de 7 m = 84 m², así que manda el 10%: 93 m², 2 rollos;
        # 93 × $209 + 2 × $1,150 = $21,737.
        r = rollos.corte(12, 7)
        self.assertEqual((r["m2"], r["rollos"]), (93, 2))
        cuerpo = plano(principal(html("/pasto-sintetico/envio/monterrey")))
        self.assertIn("¿Cuánto pido para un patio trasero de 12 × 7 m?", cuerpo)
        self.assertIn("pide 93 m² , que viajan en 2 rollos. Con Irlanda 25 salen en $21,737 con envío a Monterrey.",
                      cuerpo)

    def test_aviso_de_rollo_completo_cuando_conviene(self):
        # Aguascalientes, 8 × 5 m con Toscana 28: 44 m² × $229 + $900 = $10,976; 50 m² × $199 + $900 = $10,850.
        cuerpo = plano(principal(html("/pasto-sintetico/envio/aguascalientes")))
        self.assertIn("salen en $10,976 con envío a Aguascalientes. Un rollo completo de 50 m² sale en $10,850: te "
                      "conviene más.", cuerpo)
        self.assertNotIn("te conviene más", plano(principal(html("/pasto-sintetico/envio/monterrey"))))

    def test_azotea_de_cdmx_con_el_modelo_ligero(self):
        cuerpo = plano(principal(html("/pasto-sintetico/envio/cdmx")))
        self.assertIn("¿Cuánto pido para una azotea de 6 × 4 m?", cuerpo)
        self.assertIn("Con Toscana 18 salen en", cuerpo)

    def test_enlaza_tres_ciudades_cercanas_distintas(self):
        for x in CIUDADES:
            cerca = ciudad.cercanas(x)
            cuerpo = principal(html(f"/pasto-sintetico/envio/{x['slug']}"))
            with self.subTest(slug=x["slug"]):
                self.assertEqual(len({y["slug"] for y in cerca}), 3)
                self.assertNotIn(x["slug"], {y["slug"] for y in cerca})
                for y in cerca:
                    self.assertIn(f'href="/pasto-sintetico/envio/{y["slug"]}"', cuerpo)
        self.assertEqual([y["slug"] for y in ciudad.cercanas(ciudad.POR_SLUG["torreon"])][:1], ["saltillo"])
        self.assertIn("toluca", {y["slug"] for y in ciudad.cercanas(ciudad.POR_SLUG["cdmx"])})


if __name__ == "__main__":
    unittest.main()
