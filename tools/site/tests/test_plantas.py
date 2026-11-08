"""Páginas de plantas con plantilla (Etapa 2e): secuencia del spec, precios de datos.py, fotos de especie publicables
(ni FOTOS_RETIRADAS ni las escenas de plantas_comun.FOTOS_SOLO_CATALOGO), mensajes, enlaces y JSON-LD."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import generar  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from contenido import plantas_comun as pc  # noqa: E402

PUBLIC = paginas.PUBLIC


def html(ruta):
    return (PUBLIC / dict((r, s) for r, s, _p, _c in generar.PAGINAS)[ruta]).read_text(encoding="utf-8")


def grafo(h):
    return [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
            for n in json.loads(b).get("@graph", [])]


def mensajes(h):
    return [unquote(t) for t in re.findall(r'href="https://wa\.me/\d+\?text=([^"]*)"', h)]


class HubTest(unittest.TestCase):
    RUTA = "/plantas-palmas-arboles-tampico"

    def setUp(self):
        self.h = html(self.RUTA)

    def test_orden_de_secciones_del_spec(self):
        ids = ["vt-h1", "vt-h-necesidad", "vt-h-subcategorias", "vt-h-destacadas", "vt-h-lista", "vt-h-garantia",
               "vt-h-faq", "vt-cierre-titulo"]
        posiciones = [self.h.index(f'id="{i}"') for i in ids]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_hoja_de_plantas_sin_css_viejo_ni_proxy(self):
        self.assertIn('<body class="vt-pagina vt-plantas">', self.h)
        self.assertIn("/css/terra-plantas.", self.h)
        for viejo in ("tailwind.css", "design-system.css", "servicios.css", "fonts.googleapis", "/api/img"):
            self.assertNotIn(viejo, self.h)

    def test_necesidades_enlazan_el_catalogo_con_filtro(self):
        for filtro in ("luz=sol", "luz=media,sombra", "uso=salitre", "tam=chica", "tam=mediana", "tam=grande"):
            self.assertIn(f'href="/catalogo?{filtro}"', self.h)

    def test_subcategorias_con_desde_de_datos_o_segun_cotizacion(self):
        self.assertIn('href="/palmas-tropicales-tampico"', self.h)
        self.assertEqual(self.h.count("Precio según cotización"), 3)
        self.assertEqual(len(re.findall(r'<p class="vt-indice__desde">desde', self.h)), 2)

    def test_cada_whatsapp_lleva_su_plantilla_y_la_firma(self):
        propios = [m for m in mensajes(self.h) if "Plantas que busco: ___" in m]
        self.assertGreaterEqual(len(propios), 2)  # portada y cierre
        self.assertTrue(all(m.endswith(datos.FIRMA) for m in mensajes(self.h)))

    def test_sin_afirmaciones_que_el_dueno_no_confirmo(self):
        # La Huasteca del cuadro de datos es el pasto instalado; aquí se prueba la entrega que el dueño no confirmó.
        for viejo in ("Huasteca y zonas", "Pánuco", "grúa", "Más vendidas", "más pedidas", "Martha R.", "Constructora Arce", "gratis",
                      "sin costo", "framboyán", "Framboyán"):
            self.assertNotIn(viejo, self.h.replace("/blog/framboyan-", ""))

    def test_sin_escenas_de_resort_en_las_fotos(self):
        for slug in pc.FOTOS_SOLO_CATALOGO:
            self.assertNotIn(f"/img/catalogo/{slug}-tampico.webp", self.h)

    def test_figuras_sin_numero_repetido(self):
        numeros = re.findall(r"<figcaption>(?:<span>)?<b>Fig\. (\d+)</b>", self.h)
        self.assertGreater(len(numeros), 8)
        self.assertEqual(len(numeros), len(set(numeros)))

    def test_json_ld_sin_localbusiness_recortado(self):
        tipos = {n["@type"] for n in grafo(self.h)}
        self.assertTrue({"FAQPage", "BreadcrumbList", "ItemList"} <= tipos)
        self.assertNotIn("LocalBusiness", tipos)


if __name__ == "__main__":
    unittest.main()
