"""La home publicada sale de su plantilla con la secuencia del spec §3.3 y los datos oficiales."""
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

HTML = (paginas.PUBLIC / "index.html").read_text(encoding="utf-8")
MAIN = re.search(r'<main id="main">(.*)</main>', HTML, re.S).group(1)
TEXTO = textos_publicos(HTML)


def ld(tipo):
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S):
        nodo = json.loads(bloque)
        if nodo.get("@type") == tipo:
            return nodo
    raise AssertionError(tipo)


class InicioTest(unittest.TestCase):
    def test_secuencia_de_la_plantilla(self):
        marcas = ('class="vt-portada"', 'class="vt-datos"', 'id="vt-h-que"', 'data-vt-medidor', 'id="vt-h-obras"',
                  'class="vt-logos"', 'id="vt-h-opiniones"', 'id="vt-h-como"', 'id="vt-h-precios"', 'id="vt-h-faq"', 'id="vt-h-cobertura"', 'class="vt-cierre"')
        posiciones = [MAIN.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_h1_y_un_solo_h1(self):
        self.assertEqual(re.findall(r"<h1\b[^>]*>(.*?)</h1>", HTML, re.S),
                         ["Pasto en rollo, jardines y plantas en Tampico y Madero."])

    def test_portada_con_precio_cta_y_foto_principal(self):
        portada = MAIN[:MAIN.index('id="vt-h-que"')]
        self.assertIn("<b>$120</b><span>/m²</span>", portada)
        self.assertIn("<b>$85 /m²</b>", portada)
        self.assertIn("data-hero-cta", portada)
        self.assertIn('data-cta="home:hero"', portada)
        self.assertIn('href="#medidor"', portada)
        self.assertIn('loading="eager" fetchpriority="high"', portada)
        self.assertIn('<link rel="preload" as="image" href="/img/obra/cuadrilla-tendiendo-pasto-san-agustin.webp"', HTML)

    def test_datos_y_copy_del_dueno(self):
        for frase in (datos.PROMESA_COMPLETA, datos.GOOGLE, datos.M2_INSTALADOS, f"REPSE {datos.REPSE}",
                      "Obregón 209 Sur", datos.LLEGADA_PASTO, datos.ANTICIPO, datos.PRIMER_RIEGO,
                      "la reponemos sin costo", f"{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones"):
            with self.subTest(frase=frase):
                self.assertIn(frase, TEXTO)
        for cliente in datos.CLIENTES_B2B:
            with self.subTest(cliente=cliente):
                if cliente == "Renault":  # sin logo en public/img/clientes: va con su nombre en texto
                    self.assertIn('<li class="vt-logos__nombre">Renault</li>', HTML)
                else:
                    self.assertIn(f'alt="{cliente}"', HTML)
        self.assertIn('href="/politicas"', MAIN)

    def test_sin_css_viejo_ni_google_fonts(self):
        self.assertNotRegex(HTML, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
        self.assertEqual(len(re.findall(r"<style\b", HTML)), 0)

    def test_scripts_del_medidor_en_orden(self):
        self.assertLess(HTML.index('src="/js/vt-mensualidades.js"'), HTML.index('src="/js/vt-medidor.js"'))

    def test_mensajes_de_whatsapp_con_contexto_y_firma(self):
        for cta in ("home:hero", "home:cierre"):
            href = re.search(rf'data-cta="{cta}" href="https://wa\.me/528333268008\?text=([^"]+)"', HTML).group(1)
            texto = unquote(href)
            with self.subTest(cta=cta):
                self.assertTrue(texto.startswith(datos.MENSAJES["general"]))
                self.assertTrue(texto.endswith(datos.FIRMA))

    def test_json_ld_conservado_y_faq_igual_a_la_visible(self):
        self.assertEqual(ld("LocalBusiness")["@id"], f"{datos.SITIO}/#negocio")
        faq = ld("FAQPage")
        visibles = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<summary>(.*?)</summary>", MAIN)]
        self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)
        self.assertEqual(len(visibles), 6)
        self.assertEqual(faq["mainEntity"][0]["acceptedAnswer"]["text"], datos.RESPUESTA_PRECIO_PASTO)
        ld("BreadcrumbList")

    def test_opiniones_reales_con_nombre_publicadas_con_permiso(self):
        """Decisión del dueño (2026-11-07): las cuatro opiniones con nombre de la home son reales y se conservan."""
        opiniones = MAIN[MAIN.index('id="vt-h-opiniones"'):MAIN.index('id="vt-h-como"')]
        self.assertIn("Lo que dicen nuestros clientes en Tampico", opiniones)
        for nombre, inicio_cita in (("Carlos Herrera", "Renovamos 250 m² de jardín con pasto San Agustín"),
                                    ("María Fernanda Ruiz", "El equipo nos ayudó desde el diseño hasta la instalación"),
                                    ("Ing. Raúl Sánchez", "Instalamos sistema de riego para un área comercial de 600 m²"),
                                    ("Lic. Adriana Morales", "El servicio de mantenimiento ha sido constante")):
            with self.subTest(nombre=nombre):
                self.assertIn(f"<b>{nombre}</b>", opiniones)
                self.assertIn(inicio_cita, opiniones)
        self.assertEqual(opiniones.count("<blockquote>"), 4)

    def test_cotizacion_solo_por_whatsapp_y_medidor(self):
        """Decisión del dueño: sin formulario de cotización por correo en la home."""
        self.assertNotIn("<form", HTML)
        self.assertNotIn("formsubmit", HTML)

    def test_sin_prometer_visita_gratis(self):
        self.assertNotRegex(TEXTO, r"(?i)visitas?\W+(?:\w+\W+){0,3}?(?:sin costo|gratis|gratuita)|medir sin costo")

    def test_seo_jardineria_cobertura_twitter_y_hreflang(self):
        h2 = re.findall(r"<h2\b[^>]*>(.*?)</h2>", MAIN, re.S)
        self.assertTrue(any("Jardinería" in t for t in h2), h2)
        cobertura = MAIN[MAIN.index('id="vt-h-cobertura"'):MAIN.index('class="vt-cierre"')]
        for lugar in ("Tampico", "Madero", "Altamira", "Huasteca"):
            self.assertIn(lugar, cobertura)
        for _nombre, href in datos.ZONAS:
            self.assertIn(f'href="{href}"', cobertura)
        for nombre in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
            self.assertIn(f'<meta name="{nombre}" content=', HTML)
        self.assertIn(f'<link rel="alternate" hreflang="es-MX" href="{datos.SITIO}">', HTML)

    def test_una_opinion_destacada_y_tres_compactas(self):
        opiniones = MAIN[MAIN.index('id="vt-h-opiniones"'):MAIN.index('id="vt-h-como"')]
        self.assertEqual(opiniones.count('class="vt-testimonios__dest"'), 1)

    def test_sin_render_de_referencia_y_filas_numeradas(self):
        self.assertNotIn("Proyecto · referencia", MAIN)
        indice = MAIN[MAIN.index('class="vt-indice"'):MAIN.index('data-vt-medidor')]
        self.assertEqual(re.findall(r'class="vt-indice__n" aria-hidden="true">(\d+)<', indice),
                         ["01", "02", "03", "04", "05"])
        self.assertEqual(indice.count('class="vt-indice__ir"'), 5)

    def test_una_sola_etiqueta_de_precio_en_la_portada(self):
        portada = MAIN[:MAIN.index('id="vt-h-que"')]
        self.assertEqual(portada.count('class="vt-etiqueta"'), 1)


if __name__ == "__main__":
    unittest.main()
