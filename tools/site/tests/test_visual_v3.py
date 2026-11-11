"""Plan visual V3 (2026-11-11, docs/ux/2026-11/plan-mejoras-visuales.md): gráficos propios. Íconos de luz, riego y
altura en las fichas de plantas, gráfica de altura de los 9 sintéticos, cifras en Fraunces, grano de papel, dibujos de
línea en las bandas oscuras y tinte por línea de negocio."""
import re
import unittest
from pathlib import Path

import componentes_plantas as cp
import componentes_tienda as t
from plantillas import base

PUBLIC = Path(__file__).resolve().parents[3] / "public"
CSS = (PUBLIC / "css" / "terra.css").read_text(encoding="utf-8")


def _html(ruta):
    return (PUBLIC / ruta / "index.html").read_text(encoding="utf-8")


class VisualV3Test(unittest.TestCase):
    def test_chips_con_icono_y_etiqueta_para_lectores(self):
        html = cp.datos_especie({"luz": "Sol", "agua": "Poco", "altura": "1 m"})
        for icono, etiqueta in (("sol", "Luz"), ("gota", "Riego"), ("regla", "Altura")):
            self.assertIn(f'<use href="#vt-i-{icono}"/></svg><span class="vt-sr">{etiqueta}</span></dt>', html)
        pagina = _html("plantas-para-jardin-tampico")
        for icono in ("sol", "gota", "regla"):
            self.assertIn(f'<symbol id="vt-i-{icono}"', pagina)

    def test_grafica_de_alturas_con_los_9_modelos_en_texto(self):
        html = t.grafica_alturas()
        self.assertEqual(html.count("<li>"), len(t.data.MODELOS))
        alturas = [int(x) for x in re.findall(r"<b>(\d+)</b> mm", html)]
        self.assertEqual(alturas, sorted(alturas))
        self.assertIn('class="vt-alturas"', _html("pasto-sintetico"))

    def test_linea_de_negocio_por_ruta(self):
        casos = {"https://www.viverosterra.com/tierra-negra-vegetal-tampico": "tierra",
                 "https://www.viverosterra.com/palmas-tropicales-tampico": "plantas",
                 "https://www.viverosterra.com/pasto-sintetico/bali-35": "pasto",
                 "https://www.viverosterra.com/": None,
                 "https://www.viverosterra.com/mantenimiento-jardines-tampico": None}
        for canonical, linea in casos.items():
            with self.subTest(canonical=canonical):
                self.assertEqual(base.linea_de(canonical), linea)
        self.assertIn('<html lang="es-MX" data-linea="tierra">', _html("tierra-negra-vegetal-tampico"))
        self.assertIn('<html lang="es-MX">', (PUBLIC / "index.html").read_text(encoding="utf-8"))

    def test_cifras_grano_y_dibujos_en_la_hoja(self):
        self.assertIn(".vt-pagina main .vt-grande,.vt-datos--tira dd{font-family:var(--vt-font-serif)", CSS)
        self.assertIn("feTurbulence", CSS)
        self.assertEqual(CSS.count("stroke-opacity='.16'"), 3)  # hoja, palma y raíz
        self.assertIn('[data-linea="tierra"] .vt-bloque--tinte{background-color:var(--vt-soil-100)}', CSS)


if __name__ == "__main__":
    unittest.main()
