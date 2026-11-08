"""/pasto-en-rollo-tampico sale de la plantilla de servicio con la secuencia del spec §3.3 y el copy del dueño."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

HTML = (paginas.PUBLIC / "pasto-en-rollo-tampico" / "index.html").read_text(encoding="utf-8")
MAIN = re.search(r'<main id="main">(.*)</main>', HTML, re.S).group(1)
TEXTO = textos_publicos(HTML)
GRAFO = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))["@graph"]


def nodo(tipo):
    return next(n for n in GRAFO if n["@type"] == tipo)


class PastoEnRolloTest(unittest.TestCase):
    def test_secuencia_de_servicio_local(self):
        marcas = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', 'data-cta="servicio-pasto:hero"',
                  'class="vt-datos"', 'id="vt-h-prueba"', 'id="vt-h-precio"', "data-vt-medidor", 'id="vt-h-conviene"',
                  'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-pago"', "data-simulador", 'id="vt-h-faq"',
                  'id="vt-h-cobertura"', 'id="vt-h-rel"', 'class="vt-cierre"')
        posiciones = [MAIN.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_un_h1_con_beneficio_y_lugar(self):
        h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", HTML, re.S)
        self.assertEqual(len(h1), 1)
        self.assertTrue(h1[0].startswith("Pasto San Agustín en rollo, instalado en un día."))

    def test_copy_del_dueno(self):
        for frase in (datos.ANTICIPO, f"llega del campo {datos.LLEGADA_PASTO}", datos.PRIMER_RIEGO,
                      "si una sección no arraiga en 15 a 20 días, la reponemos sin costo", datos.PROMESA_COMPLETA,
                      "¿Cuál te conviene según tu espacio?", datos.M2_INSTALADOS):
            with self.subTest(frase=frase):
                self.assertIn(frase, TEXTO)
        self.assertEqual(TEXTO.count("Cortado para tu pedido"), 2)
        self.assertIn('href="/politicas"', MAIN)
        self.assertIn('href="/mayoreo-pasto-tampico"', MAIN)
        self.assertIn('href="/protocolo-cuidados-pasto-san-agustin"', MAIN)

    def test_ctas_con_mensaje_de_pasto(self):
        for cta in ("servicio-pasto:hero", "servicio-pasto:cierre"):
            texto = unquote(re.search(rf'data-cta="{cta}" href="https://wa\.me/528333268008\?text=([^"]+)"', HTML)
                            .group(1))
            with self.subTest(cta=cta):
                self.assertTrue(texto.startswith(datos.MENSAJES["pasto-natural"]))
        self.assertIn('data-cta="servicio-pasto:medidor"', MAIN)
        self.assertIn('data-cta="servicio-pasto:simulador"', MAIN)

    def test_prueba_social_cobertura_y_un_solo_bloque_de_mensualidades(self):
        nombre, cita = datos.OPINIONES[0][1], datos.OPINIONES[0][0]
        prueba = MAIN[MAIN.index('id="vt-h-prueba"'):MAIN.index('id="vt-h-precio"')]
        self.assertIn(f"<b>{nombre}</b>", prueba)
        self.assertIn(cita, prueba)
        self.assertIn('class="vt-logos"', prueba)
        self.assertIn("+500,000 m² instalados en Tamaulipas y la Huasteca", TEXTO)
        self.assertIn("Sectores que atendemos", MAIN)
        for _nombre, href in datos.ZONAS:
            self.assertIn(f'href="{href}"', MAIN)
        self.assertEqual(MAIN.count('class="vt-planes"'), 0)  # el simulador ya muestra plazos y mínimos
        self.assertEqual(MAIN.count("data-simulador"), 1)

    def test_paridad_con_las_opiniones_anteriores_a_2a(self):
        # Decisión del dueño (2026-11-07): las dos opiniones que publicaba la página antes de 2a son reales y tienen
        # permiso; vuelven palabra por palabra (citas del cliente, no promesas de la empresa) junto a la de Carlos Herrera.
        prueba = MAIN[MAIN.index('id="vt-h-prueba"'):MAIN.index('id="vt-h-precio"')]
        citas = (
            ("Contraté pasto e instalación para 180 m² en mi jardín de Madero. Llegaron a la hora acordada, prepararon el "
             "terreno y quedó perfecto en un día. A las 3 semanas estaba completamente arraigado. Lo más importante: "
             "pagué el resto hasta que lo vi terminado.", "Jorge H.", "Residencial · Ciudad Madero · 180 m²"),
            ("Somos constructora y compramos el pasto para un fraccionamiento en Altamira. Precio de mayoreo muy "
             "competitivo, facturaron sin problema y respetaron el calendario de entrega por etapas. Ya son nuestro "
             "proveedor recurrente.", "Arq. Patricia L.", "Constructora · Altamira · Proyecto 2,400 m²"),
        )
        for cita, nombre, detalle in citas:
            with self.subTest(nombre=nombre):
                self.assertIn(f"<p>“{cita}”</p>", prueba)
                self.assertIn(f"<b>{nombre}</b><span>{detalle}</span>", prueba)
        self.assertLess(prueba.index("Carlos Herrera"), prueba.index("Jorge H."))

    def test_twitter_card(self):
        for nombre in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
            self.assertIn(f'<meta name="{nombre}" content=', HTML)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', HTML)

    def test_render_rotulado_como_referencia(self):
        self.assertIn("<span>Proyecto · referencia</span>", MAIN)
        self.assertNotIn("<span>Terminado</span>", MAIN)

    def test_sin_css_viejo_ni_scripts_de_servicios(self):
        self.assertNotRegex(HTML, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
        self.assertNotIn("svc-hero", HTML)
        self.assertNotIn("<form", HTML)
        orden = [HTML.index(f'src="/js/{s}"') for s in ("vt-mensualidades.js", "vt-medidor.js", "vt-simulador.js")]
        self.assertEqual(orden, sorted(orden))

    def test_sin_formulario_por_correo_ni_visita_gratis(self):
        """Decisiones del dueño: se cotiza por WhatsApp o con el Medidor; la visita para medir no se promete gratis."""
        self.assertNotIn("formsubmit", HTML)
        self.assertNotRegex(TEXTO, r"(?i)visitas?\W+(?:\w+\W+){0,3}?(?:sin costo|gratis|gratuita)|medir sin costo")

    def test_json_ld_conservado_y_generado_de_lo_visible(self):
        self.assertEqual({n["@type"] for n in GRAFO},
                         {"Product", "FAQPage", "HowTo", "BreadcrumbList", "SpeakableSpecification"})
        visibles = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<summary>(.*?)</summary>", MAIN)]
        self.assertEqual([q["name"] for q in nodo("FAQPage")["mainEntity"]], visibles)
        self.assertEqual(len(visibles), 8)
        # El HowTo es el proceso visible (una sola lista de pasos en la página).
        pasos = nodo("HowTo")["step"]
        proceso = re.search(r'<ol class="vt-pasos">(.*?)</ol>', MAIN).group(1)
        titulos = [re.sub(r"\s*<span.*", "", h) for h in re.findall(r"<li><h3>(.*?)</h3>", proceso)]
        self.assertEqual([p["name"] for p in pasos], titulos)
        self.assertEqual(len(pasos), 5)
        for paso in pasos:
            self.assertIn(paso["text"], TEXTO)
        self.assertEqual(MAIN.count('class="vt-pasos"'), 1)
        self.assertEqual(MAIN.count('class="vt-compra"'), 0)
        self.assertEqual(nodo("Product")["offers"]["price"], str(datos.PRECIOS["pasto_solo_m2"]))


if __name__ == "__main__":
    unittest.main()
