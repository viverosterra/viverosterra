"""Hero de marca (Entrega A de experiencia, 2026-11-10): un solo componente de portada para todas las plantillas, con
la fórmula de la home. Reglas: un solo botón relleno en el hero, el teléfono como enlace de texto, lema en serif (nunca
<em>), línea de confianza con la promesa única y la calificación de Google, kicker y entrada cortos, una sola escala de
titular y el CSS del hero en terra.css (no en la hoja de la home)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402

CSS = paginas.PUBLIC / "css"
FOTO = {"src": "/img/x.webp", "ancho": 960, "alto": 1280, "alt": "Foto", "numero": 1, "lugar": "Tampico", "etapa": "Obra"}
ETIQUETA = {"codigo": "Pasto · 01", "nombre": "Pasto", "antes": "desde", "monto": "$120", "unidad": "/m²",
            "filas": (("Solo pasto", "$85 /m²"),)}
P = {"kicker": "Kicker", "h1": "Titular corto", "lema": "Un lema.", "lede": "Entrada.", "mensaje": "Hola",
     "etiqueta": ETIQUETA, "foto": FOTO, "pos": "50% 20%", "pos_d": "30% 50%",
     "enlaces": (("Calcula tu patio", "#precio"), ("Arma tu lista", "/catalogo", "plantas:catalogo")),
     "dato": "<b>+900</b> clientes"}
# Plantillas sin hero de venta (utilitarias, legales, protocolo y 404): solo comparten la escala del titular.
SIN_HERO = {"legal", "formulario", "protocolo", "no_encontrada"}
LECTURA = {"articulo", "blog_indice"}
KICKER_MAXIMO = 46   # caracteres que caben en un renglón a 360 px (12 px, mayúsculas)
ES_PORTADA = re.compile(r'<section class="vt-portada[ "]')
ENTRADA_MAXIMA = 130  # caracteres: 2 a 3 renglones en celular (la home, 108)


def texto(fragmento):
    return c.texto_plano(fragmento)


def hero_de(html):
    """El hero: la primera sección (o la cabecera del artículo) del <main>."""
    principal = html[html.index("<main"):]
    inicio = min(i for i in (principal.find("<section"), principal.find("<header")) if i >= 0)
    fin = min(i for i in (principal.find("</section>", inicio), principal.find("</header>", inicio)) if i >= 0)
    return principal[inicio:fin]


def paginas_publicadas():
    for ruta, salida, plantilla, _contenido in generar.PAGINAS:
        yield ruta, plantilla, (paginas.PUBLIC / salida).read_text(encoding="utf-8")


class ComponentePortadaTest(unittest.TestCase):
    def setUp(self):
        self.html = c.portada(P, "servicio-pasto", (("Inicio", "/"), ("Pasto", None)))

    def test_un_solo_boton_relleno_y_el_telefono_de_enlace(self):
        self.assertEqual(self.html.count('class="vt-btn'), 1)
        self.assertRegex(self.html, r'<div class="vt-portada__cta" data-hero-cta><a class="vt-btn vt-btn--wa" '
                                    r'data-cta="servicio-pasto:hero" href="https://wa\.me/')
        self.assertNotIn("vt-btn--linea", self.html)
        self.assertIn(f'<a data-cta="servicio-pasto:hero" href="tel:{datos.TELEFONO_TEL}">Llamar {datos.TELEFONO_VISIBLE}</a>',
                      self.html)

    def test_enlaces_propios_antes_del_telefono_con_su_data_cta(self):
        enlaces = re.search(r'<p class="vt-portada__enlaces">(.*?)</p>', self.html, re.S).group(1)
        self.assertIn('<a data-cta="servicio-pasto:hero" href="#precio">Calcula tu patio <span aria-hidden="true">→</span></a>',
                      enlaces)
        self.assertIn('<a data-cta="plantas:catalogo" href="/catalogo">Arma tu lista', enlaces)
        self.assertLess(enlaces.index("#precio"), enlaces.index("tel:"))

    def test_lema_fuera_del_h1_y_linea_de_confianza(self):
        self.assertIn('<h1 id="vt-h1">Titular corto</h1><p class="vt-portada__lema vt-serif">Un lema.</p>', self.html)
        confianza = re.search(r'<p class="vt-portada__confianza">(.*?)</p>', self.html, re.S).group(1)
        self.assertIn(f'data-vt-horario="{datos.horario_marca()}"', confianza)  # "Abierto ahora" (terra.js)
        self.assertIn(datos.PROMESA_COMPLETA, confianza)
        self.assertEqual(texto(confianza).count(datos.GOOGLE), 1)
        self.assertIn("<span><b>+900</b> clientes</span>", confianza)
        self.assertEqual(confianza.count(c.SEP_CONFIANZA), 2)

    def test_orden_y_variantes(self):
        orden = [self.html.index(m) for m in ('class="vt-crumbs"', 'class="vt-kicker"', "<h1", 'class="vt-lede"',
                                              'class="vt-portada__foto"', 'class="vt-etiqueta"', "data-hero-cta",
                                              "vt-portada__confianza", 'class="vt-datos"')]
        self.assertEqual(orden, sorted(orden))
        self.assertIn('<section class="vt-portada vt-portada--pliegue"', self.html)
        self.assertIn('<div class="vt-portada__foto" style="--vt-fp:50% 20%;--vt-fpd:30% 50%">', self.html)
        sin_foto = c.portada({k: v for k, v in P.items() if k not in ("foto", "pos", "pos_d")}, "material")
        self.assertIn('<section class="vt-portada vt-portada--sinfoto"', sin_foto)
        self.assertNotIn("vt-portada__foto", sin_foto)
        sin_precio = c.portada({k: v for k, v in P.items() if k != "etiqueta"}, "ciudad")
        self.assertIn("vt-portada--sinprecio", sin_precio)
        self.assertNotIn("vt-etiqueta", sin_precio.replace("vt-portada--sinprecio", ""))
        self.assertNotIn("vt-portada--pliegue", c.portada(P, "home", pliegue=False))  # la home: la foto va al final

    def test_escala_larga_por_largo_del_titular_sin_contar_el_lema(self):
        largo = "Mantenimiento de jardines y jardinero en Tampico"
        self.assertFalse(c.titular_largo('Pasto al mayoreo <span class="vt-serif">para obras y fraccionamientos</span>'))
        self.assertTrue(c.titular_largo(f'{largo} <span class="vt-serif">con visitas programadas</span>'))
        self.assertIn("vt-portada--larga", c.portada(dict(P, h1=largo), "servicio"))
        self.assertNotIn("vt-portada--larga", self.html)
        self.assertEqual(c.clase_titular(largo, "vt-art__cabeza"), "vt-art__cabeza vt-titular vt-titular--larga")

    def test_boton_propio_y_sin_telefono(self):
        html = c.portada(dict(P, cta='<a class="vt-btn vt-btn--wa" href="#cotizador">Cotizar mi pedido</a>', telefono=False),
                         "nochebuenas")
        self.assertIn('data-hero-cta><a class="vt-btn vt-btn--wa" href="#cotizador">Cotizar mi pedido</a></div>', html)
        self.assertNotIn("wa.me", html)
        self.assertNotIn("tel:", html)


class HeroEnTodasLasPlantillasTest(unittest.TestCase):
    def test_un_boton_relleno_y_ninguno_de_linea(self):
        for ruta, plantilla, html in paginas_publicadas():
            if plantilla in SIN_HERO:
                continue
            hero = hero_de(html)
            with self.subTest(ruta=ruta):
                self.assertNotIn("vt-btn--linea", hero)
                self.assertEqual(len(re.findall(r'class="vt-btn vt-btn--wa"', hero)), 0 if plantilla in LECTURA else 1)
                self.assertEqual(hero.count("data-hero-cta"), 0 if plantilla in LECTURA else 1)
                self.assertRegex(hero, r'<p class="vt-portada__enlaces">.*?href="tel:')
                self.assertIn(':hero"', hero)  # terra.js esconde la barra fija mientras se ve

    def test_lema_en_serif_en_todas_y_nunca_en_em(self):
        for ruta, plantilla, html in paginas_publicadas():
            h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S).group(1)
            with self.subTest(ruta=ruta):
                self.assertNotIn("<em", h1, "sin Archivo itálica el navegador la inclina: el lema va en .vt-serif")
                if plantilla not in SIN_HERO:
                    hero = hero_de(html)
                    self.assertTrue('class="vt-serif"' in h1 or 'class="vt-portada__lema vt-serif"' in hero)

    def test_linea_de_confianza_en_las_portadas(self):
        for ruta, plantilla, html in paginas_publicadas():
            if not ES_PORTADA.search(html):
                continue
            hero = hero_de(html)
            with self.subTest(ruta=ruta):
                confianza = re.search(r'<p class="vt-portada__confianza">(.*?)</p>', hero, re.S).group(1)
                self.assertIn("data-vt-horario=", confianza)
                self.assertIn(datos.GOOGLE, texto(confianza))

    def test_kicker_de_un_renglon_y_entrada_corta(self):
        for ruta, plantilla, html in paginas_publicadas():
            if not ES_PORTADA.search(html):
                continue
            hero = hero_de(html)
            kicker = texto(re.search(r'<p class="vt-kicker">(.*?)</p>', hero, re.S).group(1))
            entrada = texto(re.search(r'<p class="vt-lede"[^>]*>(.*?)</p>', hero, re.S).group(1))
            with self.subTest(ruta=ruta):
                self.assertLessEqual(len(kicker), KICKER_MAXIMO, kicker)
                self.assertLessEqual(len(entrada), ENTRADA_MAXIMA, entrada)

    def test_cada_pagina_declara_en_paridad_lo_que_cambia_en_su_hero(self):
        for ruta, _salida, plantilla, contenido in generar.PAGINAS:
            if plantilla in SIN_HERO:
                continue
            with self.subTest(ruta=ruta):
                declarado = generar.cargar(contenido).PARIDAD.get("hero", "")
                self.assertIsInstance(declarado, str)
                self.assertGreater(len(declarado), 60)

    def test_fotos_de_portada_con_encuadre_propio(self):
        """Cada foto de portada interior declara su object-position (no se edita ni se cambia ninguna imagen)."""
        for ruta, plantilla, html in paginas_publicadas():
            if "vt-portada--pliegue" not in html:
                continue
            with self.subTest(ruta=ruta):
                self.assertRegex(html, r'<div class="vt-portada__foto" style="--vt-fp:\d+% \d+%(;--vt-fpd:\d+% \d+%)?">')


class HeroCssTest(unittest.TestCase):
    def setUp(self):
        self.terra = re.sub(r"/\*.*?\*/", "", (CSS / "terra.css").read_text(encoding="utf-8"), flags=re.S)

    def test_boton_principal_alto_con_sombra_amarilla_y_estados(self):
        boton = re.search(r"\.vt-portada__cta \.vt-btn\{([^}]*)\}", self.terra).group(1)
        self.assertTrue(60 <= int(re.search(r"min-height:(\d+)px", boton).group(1)) <= 66)
        self.assertRegex(boton, r"box-shadow:\d+px \d+px 0 var\(--vt-tag\)")
        self.assertIn("@media (hover:hover){.vt-portada__cta .vt-btn:hover{", self.terra)
        for estado in (":active", ":focus-visible"):
            self.assertIn(f".vt-portada__cta .vt-btn{estado}{{", self.terra)
        self.assertIn("@media (prefers-reduced-motion:reduce){.vt-portada__cta .vt-btn{transition:none}}", self.terra)
        escritorio = self.terra[self.terra.index("@media (min-width:1024px){\n  .vt-portada{"):]
        self.assertTrue(60 <= int(re.search(r"\.vt-portada__cta \.vt-btn\{[^}]*min-height:(\d+)px", escritorio).group(1)) <= 66)

    def test_enlaces_de_texto_con_objetivo_de_44(self):
        self.assertRegex(self.terra, r"\.vt-portada__enlaces a\{[^}]*min-height:44px")

    def test_el_hero_no_vive_en_la_hoja_de_la_home(self):
        inicio = (CSS / "terra-inicio.css").read_text(encoding="utf-8")
        for clase in ("vt-portada__cta", "vt-portada__enlaces", "vt-portada__confianza", "vt-inicio__cta", "vt-inicio__lema"):
            self.assertNotIn(clase, inicio)
        for viejo in ("vt-portada--compacta", "vt-portada--apaisada", "vt-portada__tambien"):
            self.assertNotIn(viejo, self.terra)

    def test_una_sola_escala_de_titular(self):
        """El tamaño del <h1> solo se define en terra.css (.vt-portada y .vt-titular, con su variante larga): ninguna hoja
        de sección lo vuelve a fijar ni fuerza mayúsculas en el titular."""
        for hoja in sorted(CSS.glob("terra-*.css")):
            if re.fullmatch(r"terra-[a-z]+\.[0-9a-f]{10}\.css", hoja.name):
                continue
            css = re.sub(r"/\*.*?\*/", "", hoja.read_text(encoding="utf-8"), flags=re.S)
            for selector, cuerpo in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
                if re.search(r"\bh1\s*$", selector.strip()) or re.search(r"\bh1\s*,", selector):
                    with self.subTest(hoja=hoja.name, selector=selector.strip()):
                        self.assertNotRegex(cuerpo, r"font-size|text-transform")
        self.assertIn(".vt-pagina main :is(.vt-portada,.vt-titular) h1{font-size:var(--vt-h1)", self.terra)


if __name__ == "__main__":
    unittest.main()
