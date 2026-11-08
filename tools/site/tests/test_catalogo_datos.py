"""Las especies del catálogo (Etapa 2e): fuente única, igual a lo que publicaba main y con atributos = pAttr() de main."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contenido import catalogo_datos as cd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[3]
CASOS = json.loads((RAIZ / "public" / "js" / "tests" / "casos-catalogo.json").read_text(encoding="utf-8"))
CAPTURA = json.loads((Path(__file__).resolve().parent / "paridad" / "plantas-especies.json").read_text(encoding="utf-8"))
CLAVES = {"slug", "cat", "name", "sc", "sz", "b", "luz", "agua", "altura", "flor", "mant", "tipo", "desc", "drive", "img",
          "ancho", "alto"}


class CatalogoDatosTest(unittest.TestCase):
    def test_117_especies_con_slug_unico_y_el_contrato_del_js(self):
        self.assertEqual(len(cd.ESPECIES), 117)
        self.assertEqual(len(cd.POR_SLUG), 117)
        for e in cd.ESPECIES:
            with self.subTest(especie=e["name"]):
                self.assertEqual(set(e), CLAVES)
                self.assertRegex(e["slug"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertEqual(e["slug"], cd.slug(e["name"]))
                self.assertIn(e["cat"], ("arboles", "palmas", "plantas"))
                self.assertTrue(e["sz"] and all(isinstance(t, str) for t in e["sz"]))
                self.assertNotIn("<", e["luz"] + e["desc"])

    def test_fotos_retiradas_y_confirmadas_declaradas(self):
        """FOTOS_RETIRADAS: especies reales, cada una con su motivo; FOTOS_VIVERO_CONFIRMADAS (las llena el dueño): especies
        reales con foto. Ninguna foto chica está retirada (la lista de chicas es de fotos publicadas)."""
        self.assertIsInstance(cd.FOTOS_VIVERO_CONFIRMADAS, frozenset)
        self.assertLessEqual(set(cd.FOTOS_RETIRADAS), set(cd.POR_SLUG))
        self.assertLessEqual(cd.FOTOS_VIVERO_CONFIRMADAS, set(cd.POR_SLUG) - set(cd.FOTOS_RETIRADAS))
        self.assertFalse(cd.FOTOS_CHICAS & set(cd.FOTOS_RETIRADAS))
        for slug, motivo in cd.FOTOS_RETIRADAS.items():
            with self.subTest(especie=slug):
                self.assertGreater(len(motivo), 10)
                self.assertFalse(cd.tiene_foto(cd.especie(slug)))
        self.assertTrue(cd.tiene_foto(cd.especie("palma-real")))
        for slug in ("eucalipto", "flor-de-mayo", "tronadora", "acacia-negra", "palma-cola-de-pescado", "beucarnea-soyate",
                     "esparrago-meyeri", "clorofito-liston", "polyalthia", "wudelia-rastrera", "orquidea-pata-de-vaca",
                     # lote C: marcas tenues de otros viveros y la etiqueta ajena del agave
                     "agave-atenuata", "aralia-elegantisima", "aralia-shaflera", "floripondio", "jazmin",
                     "fornio-phormium", "pasto-liriope", "heliconia-baby-enana"):
            self.assertIn(slug, cd.FOTOS_RETIRADAS)

    def test_cada_especie_de_main_sigue_con_su_cientifico_o_la_correccion_declarada(self):
        por_nombre = {e["name"]: e for e in cd.ESPECIES}
        for nombre, cientifico in CAPTURA["/catalogo"]["especies"]:
            with self.subTest(especie=nombre):
                self.assertIn(nombre, por_nombre)
                self.assertEqual(por_nombre[nombre]["sc"], cd.CIENTIFICOS_CORREGIDOS.get(cientifico, cientifico))

    def test_correcciones_solo_las_declaradas(self):
        publicados = {s for _n, s in CAPTURA["/catalogo"]["especies"]}
        for viejo, nuevo in cd.CIENTIFICOS_CORREGIDOS.items():
            with self.subTest(viejo=viejo):
                self.assertNotEqual(viejo, nuevo)
                self.assertRegex(nuevo, r"^[A-Z][a-z]+ (?:[a-z]+|sp\.)$")
        self.assertTrue(set(cd.CIENTIFICOS_CORREGIDOS) - {"Jacaranda mimifolia"} <= publicados)

    def test_atributos_iguales_a_pattr_de_main(self):
        por_nombre = {e["name"]: e for e in cd.ESPECIES}
        for caso in CASOS["atributos"]:
            if caso["name"] not in por_nombre:  # el Floripondio duplicado
                continue
            with self.subTest(especie=caso["name"]):
                esperado = {k: v for k, v in caso.items() if k != "name"}
                self.assertEqual(cd.atributos(por_nombre[caso["name"]]), esperado)

    def test_tamano_por_altura_adulta(self):
        self.assertEqual(cd.tamano({"altura": "Hasta 60 cm"}), "chica")
        self.assertEqual(cd.tamano({"altura": "Hasta 1.5 m"}), "chica")
        self.assertEqual(cd.tamano({"altura": "Hasta 4 m"}), "mediana")
        self.assertEqual(cd.tamano({"altura": "Trepadora hasta 12 m"}), "grande")
        self.assertIsNone(cd.tamano({"altura": "Formado según tamaño"}))

    def test_salitre_y_guias_solo_con_fuente_y_de_especies_que_existen(self):
        for slug, fuente in cd.SALITRE.items():
            with self.subTest(salitre=slug):
                self.assertIn(slug, cd.POR_SLUG)
                self.assertTrue(fuente.startswith("/blog/") or fuente.startswith("Ficha del catálogo de main"))
        for slug, guia in cd.BLOG_ESPECIE.items():
            with self.subTest(guia=slug):
                self.assertIn(slug, cd.POR_SLUG)
                self.assertTrue((RAIZ / "public" / guia.strip("/") / "index.html").is_file())
        self.assertEqual(len(cd.SALITRE), 13)

    def test_filtros_cuentas_y_url_del_catalogo(self):
        self.assertEqual(cd.cuenta({}), 117)
        self.assertEqual(cd.cuenta({"cat": ["palmas"]}), 21)
        self.assertEqual(cd.cuenta({"uso": ["salitre"]}), 13)
        self.assertEqual(cd.cuenta({"tam": ["chica"]}) + cd.cuenta({"tam": ["mediana"]}) + cd.cuenta({"tam": ["grande"]}),
                         115)
        self.assertEqual(cd.url_catalogo({"luz": ["media", "sombra"]}), "/catalogo?luz=media,sombra")
        self.assertEqual(cd.url_catalogo(q="Palma real"), "/catalogo?q=Palma%20real")
        self.assertEqual(cd.normalizar("  Árbol  de Flor "), "arbol de flor")

    def test_ordenadas_como_el_az_de_main(self):
        nombres = [e["name"] for e in cd.ORDENADAS]
        self.assertEqual(nombres, sorted(nombres, key=cd.normalizar))
        self.assertEqual(len(nombres), 117)


if __name__ == "__main__":
    unittest.main()
