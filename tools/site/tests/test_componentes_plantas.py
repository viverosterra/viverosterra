"""Componentes de las páginas de plantas (Etapa 2e)."""
import re
import sys
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_plantas as cp  # noqa: E402
import datos  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

VIVERO = "En nuestro vivero"


class ComponentesPlantasTest(unittest.TestCase):
    def test_foto_de_especie_con_dimensiones_alt_y_pie_sin_afirmar_el_vivero(self):
        html = cp.foto_especie(cd.especie("palma-real"), 3)
        self.assertIn('src="/img/catalogo/palma-real-tampico.webp" width="480"', html)
        self.assertIn('loading="lazy"', html)
        self.assertIn('alt="Palma Real (Roystonea regia)"', html)
        self.assertIn("<figcaption><b>Fig. 03</b> · Palma Real</figcaption>", html)
        self.assertNotIn("vivero", html)
        self.assertIn('fetchpriority="high"', cp.foto_especie(cd.especie("palma-real"), 1, "alta"))

    def test_en_nuestro_vivero_solo_con_la_foto_confirmada_por_el_dueno(self):
        with mock.patch.object(cd, "FOTOS_VIVERO_CONFIRMADAS", frozenset({"palma-real"})):
            html = cp.foto_especie(cd.especie("palma-real"), 3)
            self.assertIn(f"<figcaption><b>Fig. 03</b> · Palma Real · {VIVERO}</figcaption>", html)
            self.assertIn('alt="Palma Real (Roystonea regia) en el vivero de Viveros Terra"', html)
            rejilla = cp.rejilla_catalogo()
        pies = re.findall(r"<figcaption>(.*?)</figcaption>", rejilla)
        self.assertEqual(len(pies), 117)
        self.assertEqual([p for p in pies if VIVERO in p], [f"<b>Fig. {self._numero('palma-real'):02d}</b> · Palma Real · {VIVERO}"])
        self.assertEqual(rejilla.count("en el vivero de Viveros Terra"), 1)
        self.assertNotIn(VIVERO, cp.rejilla_catalogo())  # la lista del dueño empieza vacía

    @staticmethod
    def _numero(slug):
        return next(n for n, e in enumerate(cd.ORDENADAS, 1) if e["slug"] == slug)

    def test_foto_retirada_lleva_el_marcador_sin_foto(self):
        html = cp.foto_especie(cd.especie("tronadora"), 7)
        self.assertNotIn("<img", html)
        self.assertNotIn("/img/catalogo/", html)
        self.assertIn('<svg class="vt-esp__sinfoto" width="480" height="600" viewBox="0 0 480 600" role="img" '
                      'aria-label="Tronadora: sin foto por ahora"', html)
        self.assertIn('text-anchor="middle">T</text>', html)
        self.assertIn("Foto pendiente", html)
        self.assertIn("<figcaption><b>Fig. 07</b> · Tronadora</figcaption>", html)

    def test_precio_solo_de_datos(self):
        self.assertIn("desde <span class=\"vt-precio-marca\">$500</span> · tamaño chico",
                      cp.precio_especie(cd.especie("palma-real")))
        self.assertIn("$250", cp.precio_especie(cd.especie("flamboyan-tabachin")))
        self.assertNotIn("tamaño chico", cp.precio_especie(cd.especie("flamboyan-tabachin")))
        self.assertEqual(cp.precio_especie(cd.especie("palma-washingtona")), "")

    def test_tarjeta_de_especie_lleva_al_catalogo_y_a_su_guia(self):
        html = cp.especies((("palma-areca", "La más pedida para semisombra.", None),), "plantas")
        self.assertIn('<h3 class="vt-esp__nombre">Palma Areca</h3><p class="vt-esp__sci"><i>Dypsis lutescens</i></p>', html)
        self.assertIn('data-cta="plantas:catalogo" href="/catalogo?q=Palma%20Areca"', html)
        self.assertIn('href="/blog/palma-areca-tampico"', html)
        self.assertIn('<span class="vt-sr"> Palma Areca</span>', html)
        alto = cp.especies((("palma-areca", "En maceta.", "Hasta 2 m en maceta"),), "plantas")
        self.assertIn("<dd>Hasta 2 m en maceta</dd>", alto)

    def test_indice_de_subcategorias_con_desde_o_segun_cotizacion(self):
        items = [dict(titulo="Palmas", href="/palmas-tropicales-tampico", texto="t", img="/img/a.webp", ancho=560, alto=996,
                      unidad="tamaño chico"),
                 dict(titulo="Interior", href="/plantas-de-interior-tampico", texto="t", img="/img/b.webp", ancho=560,
                      alto=840, unidad="")]
        html = cp.indice_subcategorias(items)
        self.assertIn('desde <span class="vt-precio-marca">$250</span> tamaño chico', html)
        self.assertIn("Precio según cotización", html)

    def test_necesidades_con_conteo_real_y_enlace_medido(self):
        html = cp.necesidades((("salitre", "Cerca del mar", "Brisa salina.", {"uso": ["salitre"]}),), "plantas")
        self.assertIn('data-cta="plantas:necesidad-salitre" href="/catalogo?uso=salitre"', html)
        self.assertIn(f"{cd.cuenta({'uso': ['salitre']})} especies", html)

    def test_rejilla_con_117_botones_reales_y_datos_para_filtrar(self):
        html = cp.rejilla_catalogo()
        self.assertEqual(html.count('<button type="button" class="vt-btn vt-btn--linea vt-cat__add"'), 117)
        self.assertEqual(html.count('loading="eager"'), 4)
        self.assertEqual(html.count('fetchpriority="high"'), 1)
        olivo = re.search(r'<li class="vt-esp vt-cat" data-vt-esp="olivo-negro"[^>]*>', html).group(0)
        for attr in ('data-cat="arboles"', 'data-luz="sol"', 'data-tam="grande"', 'data-riego="moderado"',
                     'data-uso="banqueta salitre"', 'data-buscar="olivo negro bucida buceras'):
            self.assertIn(attr, olivo)
        self.assertNotIn("/api/img", html)

    def test_rejilla_sin_fotos_retiradas(self):
        html = cp.rejilla_catalogo()
        self.assertEqual(html.count('<svg class="vt-esp__sinfoto"'), len(cd.FOTOS_RETIRADAS))
        self.assertEqual(html.count('src="/img/catalogo/'), 117 - len(cd.FOTOS_RETIRADAS))
        for slug in cd.FOTOS_RETIRADAS:
            with self.subTest(especie=slug):
                self.assertNotIn(f"/img/catalogo/{slug}-tampico.webp", html)
        prioridad = re.search(r'<img src="([^"]+)"[^>]*fetchpriority="high"', html).group(1)
        self.assertNotIn(prioridad.split("/")[-1].replace("-tampico.webp", ""), cd.FOTOS_RETIRADAS)

    def test_filtros_con_label_y_botones_con_aria_pressed(self):
        html = cp.filtros_catalogo(117)
        self.assertIn('<label for="vt-cat-q">', html)
        self.assertIn('role="search"', html)
        self.assertEqual(html.count('aria-pressed="false"'), 15)
        self.assertIn('data-vt-g="uso" data-vt-v="salitre"', html)
        self.assertIn("117 especies", html)

    def test_lista_en_dialogos_con_un_solo_enlace_de_whatsapp(self):
        html = cp.lista_catalogo("catalogo")
        self.assertEqual(html.count("<dialog"), 2)
        self.assertEqual(html.count("https://wa.me/"), 1)
        self.assertIn('data-cta="catalogo:sendWA" data-vt-o="enviar"', html)
        self.assertIn('<label for="vt-agregar-tam">', html)
        self.assertIn('role="status"', html)

    def test_enter_en_el_dialogo_agrega(self):
        """El envío implícito (Enter en cantidad o medida) usa el primer botón submit: el único es "Agregar"; Cancelar es
        un botón normal que cierra el diálogo."""
        agregar = re.search(r'<dialog class="vt-dialogo" id="vt-agregar".*?</dialog>', cp.lista_catalogo("catalogo"), re.S).group(0)
        self.assertEqual(re.findall(r'<button type="submit"[^>]*>', agregar),
                         ['<button type="submit" value="agregar" class="vt-btn vt-btn--tinta">'])
        self.assertIn('<button type="button" class="vt-btn vt-btn--linea" data-vt-cancelar>Cancelar</button>', agregar)
        self.assertIn('maxlength="60"', agregar)

    def test_pedido_especial_con_el_mensaje_de_main(self):
        html = cp.pedido_especial("catalogo")
        texto = unquote(re.search(r'href="https://wa\.me/\d+\?text=([^"]+)"', html).group(1))
        self.assertEqual(texto, cp.mensaje_especial(""))
        self.assertIn("No lo encontré en el catálogo", texto)
        self.assertIn('data-cta="catalogo:solEsp"', html)


if __name__ == "__main__":
    unittest.main()
