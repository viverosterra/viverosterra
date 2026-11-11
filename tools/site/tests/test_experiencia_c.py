"""Entrega C de experiencia (ritmo y movimiento), sin navegador: el amarillo (var(--vt-tag)) solo en el precio, en la
sombra del CTA y en el foco sobre fondo oscuro; banda oscura de garantía solo donde la garantía real está en datos.py
(pasto en rollo, sintético y diseño) y nunca en Nochebuenas; relleno vertical variado y fondos que se alternan en los
servicios; tablas redundantes plegadas con su título a la vista; CTA nuevos con texto propio; PARIDAD declarada."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paridad  # noqa: E402
from test_movimiento_css import reglas  # noqa: E402

CSS = Path(__file__).resolve().parents[3] / "public" / "css"
FUENTES = sorted(p for p in CSS.glob("terra*.css") if not re.search(r"\.[0-9a-f]{10}\.css$", p.name))
# Dónde puede ir el amarillo: precios (etiqueta, marca, renglón recomendado, totales de la tienda y Nochebuenas, el
# dibujo de etiqueta de las plantas sin foto) y la sombra del botón principal o el CTA de temporada.
PRECIO = re.compile(r"precio|etiqueta|tabla__rec|cotizador__desde|cuenta__total|nb-tabla td:last-child|sinfoto-tag")
CTA = re.compile(r"vt-portada__cta \.vt-btn|vt-navidad__cta")
# Excepciones que la Entrega C no toca (fuera de su alcance; se reportan): avisos y fechas de entrega de Nochebuenas y
# el filete y la flor del banner de Navidad.
EXCEPCIONES = {".vt-nochebuenas main .vt-nb-aviso--tag", ".vt-nochebuenas .vt-nb-fechas li",
               ".vt-temporada main a.vt-navidad", ".vt-temporada .vt-navidad__flor"}
SERVICIOS = ("/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico",
             "/mantenimiento-jardines-tampico", "/sistema-riego-tampico")
CON_BANDA = ("/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/diseno-jardines-tampico")
SECCION_RE = re.compile(r'<section class="(vt-bloque[^"]*)"')


def html(ruta):
    return paridad.archivo(ruta).read_text(encoding="utf-8")


def main(h):
    return re.search(r"<main\b.*?</main>", h, re.S).group(0)


class AmarilloTest(unittest.TestCase):
    def test_amarillo_solo_en_precio_cta_y_foco(self):
        usos = [(p.name, sel, cuerpo) for p in FUENTES for _ctx, sel, cuerpo in reglas(p.read_text(encoding="utf-8"))
                if "var(--vt-tag)" in cuerpo]
        self.assertTrue(usos)
        for hoja, selector, cuerpo in usos:
            declaraciones = [d for d in cuerpo.split(";") if "var(--vt-tag)" in d]
            solo_foco = all(d.strip().startswith("outline") for d in declaraciones)
            with self.subTest(hoja=hoja, selector=selector):
                self.assertTrue(PRECIO.search(selector) or CTA.search(selector) or solo_foco or selector in EXCEPCIONES,
                                cuerpo)

    def test_pie_cierre_y_barra_sin_amarillo(self):
        terra = {sel: cuerpo for _c, sel, cuerpo in reglas((CSS / "terra.css").read_text(encoding="utf-8"))}
        for selector in (".vt-foot__h", ".vt-cierre__msg b", ".vt-bar"):
            with self.subTest(selector=selector):
                self.assertNotIn("--vt-tag", terra[selector])


class BandaTest(unittest.TestCase):
    def test_banda_donde_la_garantia_es_de_datos(self):
        for ruta in SERVICIOS:
            with self.subTest(ruta=ruta):
                # Plan visual V2: las demás llevan su momento oscuro en el proceso, nunca en la garantía.
                garantia = main(html(ruta)).split('aria-labelledby="vt-h-garantia"', 1)[0].rsplit("<section", 1)[1]
                self.assertEqual("vt-banda" in garantia, ruta in CON_BANDA)
        self.assertIn(c.garantia_pasto(), main(html("/pasto-en-rollo-tampico")))
        self.assertIn(c.garantia_plantas(), main(html("/diseno-jardines-tampico")))

    def test_la_banda_lleva_condiciones_enlazadas_y_un_cta(self):
        for ruta in CON_BANDA:
            h = main(html(ruta))
            inicio = h.index('<section class="vt-bloque vt-banda')
            banda = h[inicio:h.index("</section>", inicio)]
            with self.subTest(ruta=ruta):
                self.assertRegex(banda, r'href="/(politicas|protocolo-cuidados-pasto-san-agustin)')
                self.assertIn('data-cta="servicio-', banda)
                self.assertIn("wa.me", banda)
                self.assertIn('class="vt-grande"', banda)

    def test_sin_cta_no_hay_banda(self):
        g = {"titulo": "t", "id_titulo": "x", "numero": 1, "rotulo": "r", "resumen": "s", "puntos": (), "pie": "",
             "banda": True}
        with self.assertRaises(ValueError):
            c.garantia(g)

    def test_nochebuenas_nunca_lleva_garantia(self):
        h = main(html(datos.NOCHEBUENAS["ruta"]))
        self.assertNotIn("vt-banda", h)
        self.assertIsNone(re.search(r"(?i)garant", paridad.texto(h)))


class RitmoTest(unittest.TestCase):
    def test_relleno_variado_y_fondos_que_se_alternan(self):
        for ruta in SERVICIOS:
            clases = SECCION_RE.findall(main(html(ruta)))
            with self.subTest(ruta=ruta):
                self.assertTrue(any("vt-bloque--apoyo" in x for x in clases))
                self.assertTrue(any("vt-bloque--clave" in x for x in clases))
                # desde la primera sección después de las fotos: nunca dos con tinte seguidas ni dos hueso seguidas
                cuerpo = clases[2:] if "vt-h-obras" in html(ruta) else clases[1:]
                fondos = ["oscuro" if "vt-banda" in x else "tinte" if "vt-bloque--tinte" in x else "hueso" for x in cuerpo]
                for a, b in zip(fondos, fondos[1:]):
                    self.assertNotEqual((a, b), ("tinte", "tinte"), fondos)
                    self.assertNotEqual((a, b), ("hueso", "hueso"), fondos)

    def test_preguntas_de_servicio_empiezan_cerradas(self):
        for ruta in SERVICIOS:
            faq = re.search(r'<div class="vt-faq">(.*?)</div>', html(ruta), re.S).group(1)
            with self.subTest(ruta=ruta):
                self.assertNotIn("<details open", faq)
        self.assertIn("<details open", c.faq((("a", "b"),)))

    def test_tablas_plegadas_conservan_su_titulo_y_su_contenido(self):
        plegadas = {"/pasto-en-rollo-tampico": 2, "/diseno-jardines-tampico": 2, "/mantenimiento-jardines-tampico": 1,
                    "/sistema-riego-tampico": 1}
        for ruta, n in plegadas.items():
            h = main(html(ruta))
            with self.subTest(ruta=ruta):
                self.assertEqual(h.count("<details class=\"vt-plegable vt-mt\" data-vt-plegable>"), n)
                for bloque in re.findall(r'<details class="vt-plegable.*?</details>', h, re.S):
                    self.assertIn("<summary class=\"vt-plegable__resumen\"><h3>", bloque)
                    self.assertIn("<table", bloque)

    def test_ctas_nuevos_con_texto_propio_por_seccion(self):
        for ruta in ("/mayoreo-pasto-tampico", "/palmas-mayoreo-proyectos", "/tierra-negra-vegetal-tampico",
                     datos.NOCHEBUENAS["ruta"], "/sistema-riego-tampico", "/pasto-sintetico-tampico"):
            textos = re.findall(r'<div class="vt-cta vt-mt" data-hero-cta>.*?</svg></span>([^<]+)<', html(ruta), re.S)
            with self.subTest(ruta=ruta):
                self.assertTrue(textos)
                self.assertEqual(len(set(textos)), len(textos))
                self.assertNotIn(c.CTA_WA, textos)

    def test_blog_con_fila_cada_12_tarjetas_y_lineas_de_lectura(self):
        h = main(html("/blog"))
        partes = h.split('<li class="vt-blog-fila"')
        self.assertGreaterEqual(len(partes), 4)
        for previo in partes[1:-1]:
            self.assertEqual(previo.count('<li class="vt-blog-t'), 12)
        articulo = main(html("/blog/pasto-san-agustin-vs-japones"))
        self.assertIn('data-cta="blog:medio-wa"', articulo)


class ParidadTest(unittest.TestCase):
    def test_cada_modulo_tocado_declara_la_entrega_c(self):
        for ruta in SERVICIOS + ("/mayoreo-pasto-tampico", "/palmas-mayoreo-proyectos", "/tierra-negra-vegetal-tampico",
                                 "/tezontle-rojo-tampico", "/marmol-blanco-tampico", "/piedra-bola-rio-tampico",
                                 datos.NOCHEBUENAS["ruta"], "/blog", "/blog/pasto-san-agustin-vs-japones"):
            with self.subTest(ruta=ruta):
                p = generar.cargar(generar.contenido_de(ruta)).PARIDAD
                self.assertIn("Entrega C de experiencia", p.get("ritmo", ""))


if __name__ == "__main__":
    unittest.main()
