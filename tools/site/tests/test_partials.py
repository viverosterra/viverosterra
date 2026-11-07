import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}


def existe(href):
    archivo = paginas.PUBLIC / href.lstrip("/")
    return archivo.is_file() or (archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file()


class HeadTest(unittest.TestCase):
    def test_region_con_gtag_unico_y_assets_con_hash(self):
        h = partials.head(URLS, legacy=False)
        self.assertTrue(h.startswith("<!-- vt:head -->\n") and h.endswith("\n<!-- /vt:head -->"))
        self.assertEqual(h.count("googletagmanager.com/gtag/js?id=G-RMZCVJ734M"), 1)
        self.assertEqual(h.count("gtag('config','G-RMZCVJ734M')"), 1)
        self.assertIn('<link rel="stylesheet" href="/css/terra.0123456789.css">', h)
        self.assertIn('<script src="/js/terra.0123456789.js" defer></script>', h)
        self.assertNotIn("legacy-fixes", h)

    def test_legacy_fixes_solo_con_tailwind_y_antes_de_terra(self):
        h = partials.head(URLS, legacy=True)
        self.assertLess(h.index("legacy-fixes.0123456789.css"), h.index("terra.0123456789.css"))


class HeaderTest(unittest.TestCase):
    def setUp(self):
        self.ctx = paginas.contexto("/pasto-en-rollo-tampico")
        self.h = partials.header(self.ctx)

    def test_menu_de_seis_entradas_en_orden(self):
        textos = re.findall(r'class="vt-nav__top"[^>]*>([^<]+)', self.h)
        self.assertEqual(textos, ["Pasto natural", "Pasto sintético", "Jardín", "Plantas y palmas", "Empresas", "Precios"])

    def test_seccion_activa_y_pagina_actual(self):
        self.assertEqual(self.h.count("vt-nav__item is-activo"), 1)
        self.assertIn('<li class="vt-nav__item is-activo"><a class="vt-nav__top" href="/pasto-en-rollo-tampico">Pasto natural</a>', self.h)
        self.assertIn('<a href="/pasto-en-rollo-tampico" aria-current="page">Pasto en rollo</a>', self.h)
        self.assertIn('<details class="vt-acc" open><summary>Pasto natural<small>desde $85/m²</small></summary>', self.h)

    def test_cta_con_mensaje_del_servicio(self):
        self.assertIn('data-cta="servicio-pasto:header"', self.h)
        self.assertIn(datos.wa_url(datos.mensaje("pasto-natural")), self.h)
        self.assertIn('data-vt-tipo="servicio-pasto" data-vt-servicio="pasto-natural"', self.h)

    def test_paneles_con_ids_existentes(self):
        controles = re.findall(r'aria-controls="([^"]+)"', self.h)
        self.assertEqual(len(controles), 6)
        for control in controles:
            self.assertIn(f'id="{control}"', self.h)

    def test_precios_es_enlace_actual_en_su_pagina(self):
        h = partials.header(paginas.contexto("/precios"))
        self.assertIn('<a class="vt-nav__top" href="/precios" aria-current="page">Precios</a>', h)

    def test_enlaces_del_menu_existen(self):
        for item in partials.MENU:
            for href in ([item["href"]] if item["href"] else []) + [h for _t, h in item["items"]]:
                with self.subTest(href=href):
                    self.assertTrue(existe(href))

    def test_skip_link_y_menu_movil_oculto(self):
        self.assertIn('<a class="vt-skip" href="#main">Saltar al contenido</a>', self.h)
        self.assertIn('<nav class="vt-mmenu" id="vt-mmenu" aria-label="Principal, móvil" hidden>', self.h)
        self.assertIn('aria-controls="vt-mmenu"', self.h)


if __name__ == "__main__":
    unittest.main()
