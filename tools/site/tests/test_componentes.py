"""Componentes del cuerpo (tools/site/componentes.py): CTA, etiqueta, datos, figuras, tablas, proceso, FAQ y Medidor."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402


class UtilidadesTest(unittest.TestCase):
    def test_redondeo_igual_que_javascript(self):
        self.assertEqual([c.redondear(x) for x in (1102.5, 1103.5, 0.4)], [1103, 1104, 0])
        self.assertEqual(c.dinero(5760), "$5,760")
        self.assertEqual((c.formato_m2(48.0), c.formato_m2(1234.5)), ("48", "1,234.5"))

    def test_texto_plano_y_etiquetas_permitidas(self):
        self.assertEqual(c.texto_plano('Ver <a href="/x">la &amp; lista</a>\n hoy'), "Ver la & lista hoy")
        self.assertEqual(c.etiquetas_no_permitidas('<b>a</b> <a href="/x">b</a> <i>c</i>'), [])
        self.assertEqual(c.etiquetas_no_permitidas("<div><script>x</script></div>"), ["div", "script"])


class CtaTest(unittest.TestCase):
    def test_fila_de_cta_con_dos_textos_promesa_y_data_cta(self):
        html = c.fila_cta(datos.MENSAJES["general"], "home", "hero", hero=True)
        self.assertIn("data-hero-cta", html)
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["home:hero", "home:hero"])
        self.assertIn("Cotizar por WhatsApp", html)
        self.assertIn(f"Llamar {datos.TELEFONO_VISIBLE}", html)
        self.assertIn(datos.PROMESA_COMPLETA, html)
        texto = unquote(re.search(r'href="https://wa\.me/528333268008\?text=([^"]+)"', html).group(1))
        self.assertTrue(texto.endswith(datos.FIRMA))

    def test_sin_hero_no_marca_la_fila(self):
        self.assertNotIn("data-hero-cta", c.fila_cta("Hola", "home", "cierre"))


class BloquesTest(unittest.TestCase):
    def test_cuadro_de_datos_oficial(self):
        html = c.cuadro_datos()
        for dato in (f"REPSE {datos.REPSE}", datos.FACTURA, str(datos.DESDE), "Obregón 209 Sur", datos.M2_INSTALADOS):
            self.assertIn(dato, html)

    def test_figura_con_pie_y_carga(self):
        f = {"src": "/img/a.webp", "ancho": 10, "alto": 20, "alt": "Foto \"real\"", "numero": 3, "lugar": "Madero",
             "etapa": "Después"}
        self.assertIn('loading="lazy"', c.figura(f))
        principal = c.figura(f, principal=True)
        self.assertIn('loading="eager" fetchpriority="high"', principal)
        self.assertIn("<b>Fig. 03</b> · Madero", principal)
        self.assertIn('alt="Foto &quot;real&quot;"', principal)

    def test_logos_son_los_clientes_autorizados(self):
        self.assertEqual(tuple(n for n, *_ in c.LOGOS), datos.CLIENTES_B2B)
        for _nombre, archivo, _a, _h, _escala in c.LOGOS:
            if archivo is None:
                continue
            self.assertTrue((Path(__file__).resolve().parents[3] / "public" / "img" / "clientes" / f"{archivo}-c.webp")
                            .is_file(), archivo)

    def test_cliente_sin_logo_va_con_su_nombre_en_texto(self):
        html = c.logos()
        self.assertIn('<li class="vt-logos__nombre">Renault</li>', html)
        self.assertNotIn('alt="Renault"', html)
        self.assertEqual(html.count("<img"), 6)

    def test_flex_y_velamar_se_leen(self):
        """Gate de diseño 2a: el logo de Flex va recortado a su palabra y el de Velamar, más alto."""
        flex = next(l for l in c.LOGOS if l[0] == "Flex")
        self.assertGreater(flex[2] / flex[3], 3)
        self.assertIn('<li class="vt-logos--alto"><img src="/img/clientes/logo-velamar-c.webp"', c.logos())

    def test_testimonios_con_nombre_y_servicio(self):
        html = c.testimonios((("Quedó muy bien.", "Ana Pérez", "Pasto · Tampico"),))
        self.assertIn('<blockquote><p>“Quedó muy bien.”</p></blockquote>', html)
        self.assertIn('<li class="vt-testimonios__dest">', html)  # la primera va destacada
        self.assertIn("<figcaption><b>Ana Pérez</b><span>Pasto · Tampico</span></figcaption>", html)

    def test_tabla_de_precios_con_unidad_y_desde(self):
        html = c.tabla_precios([{"nombre": "Pasto", "detalle": "d", "unidad": "/m²", "precio": 120, "desde": True,
                                 "rec": True}], "Precios")
        self.assertIn('<th scope="col">Unidad</th>', html)
        self.assertIn('<td class="vt-tabla__u">/m²</td>', html)
        self.assertIn("<small>desde</small><span>$120</span>", html)

    def test_pasos_con_marcadores(self):
        html = c.pasos([{"titulo": "Riego", "quien": "tu", "cuando": "Día 1", "texto": "t"},
                        {"titulo": "Poda", "quien": "juntos", "cuando": "Día 21", "texto": "t"}])
        self.assertIn('<span class="vt-quien vt-quien--tu">Tú</span>', html)
        self.assertIn('<span class="vt-quien vt-quien--juntos">Juntos</span>', html)
        # El marcador no forma parte del encabezado: el <h3> es solo el paso.
        self.assertIn("<h3>Riego</h3>", html)
        self.assertNotRegex(html, r"<h3>[^<]*<span")

    def test_faq_y_su_json_ld_dicen_lo_mismo(self):
        preguntas = (("¿Uno?", 'Sí, <a href="/x">mira</a>.'), ("¿Dos?", "No."))
        html = c.faq(preguntas)
        self.assertEqual(html.count("<details"), 2)
        self.assertEqual(html.count("<details open>"), 1)
        nodo = c.faq_jsonld(preguntas, speakable=("h1",))
        self.assertEqual(nodo["mainEntity"][0]["acceptedAnswer"]["text"], "Sí, mira.")
        self.assertEqual(nodo["speakable"]["cssSelector"], ["h1"])

    def test_planes_salen_de_la_formula_oficial(self):
        html = c.planes_mensualidades()
        for plazo, minimo in ((3, "$2,000"), (6, "$5,000"), (9, "$15,000"), (12, "$15,000")):
            self.assertIn(f"<dt>{plazo} mensualidades</dt><dd>desde {minimo}</dd>", html)
        self.assertNotRegex(html, r"(?i)sin intereses|\bMSI\b")

    def test_simulador_con_el_marcado_de_vt_simulador(self):
        html = c.simulador("pasto en rollo instalado", 12000, "servicio-pasto")
        for marca in ("data-simulador", "data-sim-monto", "data-sim-list", "data-sim-wa",
                      'data-cta="servicio-pasto:simulador"', 'value="12000"'):
            self.assertIn(marca, html)

    def test_howto_numera_los_pasos(self):
        nodo = c.howto("Cómo", (("Uno", "a"), ("Dos", "b")))
        self.assertEqual([p["position"] for p in nodo["step"]], [1, 2])

    def test_etiqueta_sin_nombre_cientifico_y_opciones_con_su_mensaje(self):
        e = {"codigo": "Sintético · 05/09", "aviso": "Con IVA", "nombre": "Toscana 28", "antes": "desde",
             "monto": "$199", "unidad": "/m²"}
        self.assertNotIn("vt-etiqueta__sci", c.etiqueta(e))
        self.assertIn('<p class="vt-etiqueta__sci">X y</p>', c.etiqueta(dict(e, cientifico="X y")))
        items = ({"rotulo": "Opción 1", "titulo": "A", "precio": 139, "unidad": "/m²", "detalle": "d", "puntos": ("p",),
                  "mensaje": "Hola A"},
                 {"rotulo": "Opción 2", "titulo": "B", "precio": 385, "unidad": "/m²", "detalle": "d", "puntos": ("q",),
                  "mensaje": "Hola B", "rec": True, "nota": "n"})
        html = c.opciones(items, "servicio-sintetico")
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["servicio-sintetico:opcion-1", "servicio-sintetico:opcion-2"])
        self.assertIn('<li class="vt-modo vt-modo--rec">', html)
        self.assertIn('<span class="vt-precio-marca">$385</span>', html)
        self.assertEqual([unquote(t).split("\n")[0] for t in re.findall(r"text=([^\"&]+)", html)], ["Hola A", "Hola B"])


class PlanesTest(unittest.TestCase):
    """Etapa 2c: planes con precio cerrado, por cotización o sin precio, con línea de mensualidades; tarjetas de lo
    que incluye un servicio y garantía sin cifra."""
    BASE = {"rotulo": "Plan 1", "titulo": "Esencial", "unidad": "MXN", "detalle": "d", "puntos": ("p",),
            "mensaje": "Hola, me interesa el Plan Terra Esencial"}

    def test_linea_de_mensualidades_con_el_plazo_mas_largo(self):
        self.assertEqual(c.linea_mensualidad(3000),
                         "o en 3 mensualidades de ≈ $1,105 con tarjeta de crédito (total $3,315)")
        self.assertEqual(c.linea_mensualidad(6500),
                         "o en 6 mensualidades de ≈ $1,245 con tarjeta de crédito (total $7,468)")
        self.assertEqual(c.linea_mensualidad(18000),
                         "o en 12 mensualidades de ≈ $1,852 con tarjeta de crédito (total $22,220)")
        with self.assertRaises(ValueError):
            c.linea_mensualidad(750)  # bajo el mínimo de $2,000 no hay plazos

    def test_precio_cerrado_sin_desde_y_con_mensualidad(self):
        html = c.opciones((dict(self.BASE, precio=3000, desde=False, mensualidad=True),), "servicio-diseno")
        self.assertIn('<p class="vt-modo__precio"><span class="vt-precio-marca">$3,000</span> MXN', html)
        self.assertIn('<small class="vt-modo__mes">o en 3 mensualidades de ≈ $1,105', html)
        self.assertNotIn("desde ", html)

    def test_precio_desde_por_omision_y_sin_mensualidad(self):
        html = c.opciones((dict(self.BASE, precio=18000),), "servicio-diseno")
        self.assertIn('desde <span class="vt-precio-marca">$18,000</span>', html)
        self.assertNotIn("vt-modo__mes", html)

    def test_por_cotizacion_y_sin_precio(self):
        html = c.opciones((dict(self.BASE, precio_texto="Por cotización"), dict(self.BASE, titulo="Goteo")),
                          "servicio-mantenimiento")
        self.assertIn('<p class="vt-modo__precio">Por cotización <small>d</small></p>', html)
        self.assertEqual(html.count('class="vt-modo__precio"'), 1)
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html),
                         ["servicio-mantenimiento:opcion-1", "servicio-mantenimiento:opcion-2"])

    def test_maximo_tres_opciones(self):
        with self.assertRaises(ValueError):
            c.opciones((self.BASE,) * 4, "servicio-diseno")

    def test_fichas_sin_precio_ni_boton(self):
        html = c.fichas(({"titulo": "Poda de pasto", "texto": "Corte parejo."},
                         {"titulo": "Goteo", "texto": "A la raíz.", "puntos": ("Menos agua",)}))
        self.assertTrue(html.startswith('<ul class="vt-modos vt-fichas">'))
        self.assertIn("<h3>Poda de pasto</h3><p>Corte parejo.</p></li>", html)
        self.assertIn('<ul class="vt-checks"><li><span>Menos agua</span></li></ul>', html)
        self.assertNotIn("wa.me", html)

    def test_garantia_con_y_sin_cifra(self):
        g = {"titulo": "Garantía.", "id_titulo": "vt-h-garantia", "numero": 6, "rotulo": "Garantía", "resumen": "r",
             "puntos": (("a", True), ("b", False)), "pie": "p"}
        self.assertNotIn("vt-grande", c.garantia(g))
        self.assertIn('<p class="vt-grande">30<small> días</small></p>', c.garantia(dict(g, grande="30", unidad="días")))


class MedidorTest(unittest.TestCase):
    def test_html_del_medidor(self):
        html = c.medidor("prueba", "home")
        self.assertIn("data-vt-medidor", html)
        self.assertEqual(html.count('name="prueba-modo"'), 3)
        self.assertIn('data-precio="120"', html)
        self.assertIn('data-minimo="500"', html)
        self.assertIn('data-cta="home:medidor"', html)
        self.assertIn('<p class="vt-medidor__aviso" data-vt-o="aviso" hidden>', html)
        self.assertEqual(html.count('name="prueba-plazo"'), 5)
        self.assertIn('value="1" checked', html)
        self.assertIn("data-hero-cta", html)  # la barra móvil se esconde mientras el Medidor está a la vista

    def test_medidor_de_la_home_solo_el_boton_esconde_la_barra_y_cambia_de_texto(self):
        """Spec del hero (2026-11-09, §4): la barra móvil ya no se oculta en todo el Medidor, solo con su botón a la
        vista; el texto del botón va en un span que vt-medidor.js cambia cuando hay medida."""
        html = c.medidor("prueba", "home", boton_medida=True)
        self.assertEqual(html.count("data-hero-cta"), 1)
        self.assertIn('data-cta="home:medidor" data-vt-o="cta" data-hero-cta href="https://wa.me/', html)
        self.assertNotIn("data-vt-medidor data-hero-cta", html)
        self.assertIn('<span data-vt-o="cta-texto">Cotizar por WhatsApp</span>', html)
        self.assertNotIn("cta-texto", c.medidor("prueba", "home"))

    def test_renglon_vivo_bajo_las_medidas_sin_iva_en_solo_pasto_y_mayoreo(self):
        """Revisión de diseño (2026-11-09): el resultado se lee junto a los campos. El pasto sin instalar no lleva IVA:
        "con IVA" solo en modo instalado (los demás textos heredados del Medidor no cambian)."""
        casos = ((8, 6, "instalado", "48 m² · desde $5,760 con IVA"), (5, 4, "solo", "20 m² · $1,700"),
                 (25, 24, "mayoreo", "600 m² · desde $36,000"), (10, 10, "mayoreo", "100 m² · $8,500"))
        for largo, ancho, modo, esperado in casos:
            r = c.calculo_medidor(largo, ancho, modo)
            with self.subTest(modo=modo, largo=largo):
                self.assertEqual(r["iva"], modo == "instalado")
                self.assertEqual(c.textos_medidor(largo, ancho, r)["vivo"], esperado)
        html = c.medidor("prueba", "home", resultado_vivo=True)
        self.assertIn('</div></div><p class="vt-medidor__vivo" data-vt-o="vivo"></p><fieldset class="vt-opciones">', html)
        self.assertNotIn("vt-medidor__vivo", c.medidor("prueba", "home"))

    def test_medidor_de_la_home_presta_su_enlace_a_la_barra(self):
        html = c.medidor("prueba", "home", boton_medida=True)
        self.assertIn(f'data-vt-barra="{c.CTA_MEDIDA_BARRA}"', html)
        self.assertEqual(c.CTA_MEDIDA_BARRA, "Enviar mi medida")
        self.assertNotIn("data-vt-barra", c.medidor("prueba", "home"))

    def test_medidor_con_garantia_bajo_el_resultado(self):
        html = c.medidor("prueba", "home", garantia=True)
        self.assertIn(f'<p class="vt-medidor__garantia" data-vt-o="garantia">{c.garantia_pasto()}</p></div></div></div>', html)
        self.assertNotIn("vt-medidor__garantia", c.medidor("prueba", "home"))

    def test_garantia_de_pasto_con_enlace_a_condiciones(self):
        html = c.garantia_pasto()
        self.assertEqual(c.texto_plano(html), datos.GARANTIA_PASTO)
        # Las condiciones del pasto viven en el protocolo de cuidados (no en /politicas, que es general).
        self.assertIn('(<a href="/protocolo-cuidados-pasto-san-agustin">ver condiciones</a>).', html)
        prefijada = c.garantia_pasto("Pasto instalado: ")
        self.assertTrue(prefijada.startswith("Pasto instalado: si una sección no arraiga"))
        self.assertEqual(c.texto_plano(prefijada), "Pasto instalado: s" + datos.GARANTIA_PASTO[1:])

    def test_promesa_con_horario_para_abierto_ahora(self):
        html = c.promesa_horario()
        self.assertEqual(html, f'<span data-vt-horario="{datos.horario_marca()}" data-vt-festivos="{datos.festivos_marca()}" data-vt-build="{datos.ACTUALIZADO}">'
                               f'{datos.PROMESA_COMPLETA}</span>')
        self.assertNotIn("aria-live", html)
        self.assertNotIn("Abierto", html)

    def test_medidor_empieza_vacio_y_no_presenta_el_ejemplo_como_estimado(self):
        html = c.medidor("prueba", "home")
        self.assertIn('placeholder="8"', html)
        self.assertIn('placeholder="6"', html)
        self.assertNotRegex(html, r'data-vt-campo="(?:largo|ancho)"[^>]*value=')
        self.assertIn('<b data-vt-o="monto">—</b>', html)
        self.assertNotIn("$5,760", html)
        cta = re.search(r'data-vt-o="cta" href="https://wa\.me/528333268008\?text=([^"]+)"', html).group(1)
        self.assertEqual(unquote(cta), datos.con_firma(datos.MENSAJES["general"]))
        self.assertIn(f'data-mensaje-mayoreo="{c.esc(datos.con_firma(datos.MENSAJES["empresas"]))}"', html)
        for campo in ("largo", "ancho", "colonia"):
            self.assertIn(f'<label for="prueba-{campo}">', html)
        self.assertNotIn("<form", html)

    def test_medidor_lee_numero_y_mensaje_de_la_pagina_y_anuncia_el_resultado(self):
        html = c.medidor("prueba", "home", mensaje=datos.MENSAJES["pasto-natural"])
        self.assertIn(f'data-wa="{datos.TELEFONO_WA}"', html)
        self.assertIn(f'data-mensaje="{c.esc(datos.con_firma(datos.MENSAJES["pasto-natural"]))}"', html)
        self.assertIn('<div class="vt-etiqueta vt-medidor__res" role="status">', html)
        self.assertEqual(html.count("aria-live"), 0)


class EmpresasTest(unittest.TestCase):
    def test_cotizador_por_volumen_empieza_vacio_con_los_precios_de_datos(self):
        html = c.cotizador_volumen("may", "b2b", "Hola, quiero cotizar pasto al mayoreo.")
        self.assertIn('data-vt-volumen data-hero-cta', html)  # la barra móvil se esconde con el cotizador a la vista
        self.assertIn('data-cta="b2b:cotizador"', html)
        self.assertIn('<label for="may-m2">m² totales de la obra</label>', html)
        self.assertIn('id="may-m2" data-vt-campo="m2" inputmode="decimal"', html)
        self.assertIn(f">{c.VACIO_VOLUMEN['medida']}<", html)
        self.assertIn('class="vt-etiqueta__precio is-vacio"', html)
        self.assertIn('&quot;mayoreo&quot;:{&quot;precio&quot;:60,&quot;desde&quot;:true,&quot;minimo&quot;:500', html)
        self.assertIn('&quot;solo&quot;:{&quot;precio&quot;:85', html)
        self.assertNotIn("instalado", html.split("data-modos=")[1].split('"')[1])
        enlace = re.search(r'data-vt-o="cta" href="([^"]+)"', html).group(1)
        self.assertTrue(unquote(enlace.split("text=", 1)[1].replace("&amp;", "&")).endswith(datos.FIRMA))
        for campo in ("empresa", "obra", "fecha"):
            self.assertIn(f'data-vt-campo="{campo}" type="text"', html)

    def test_volumen_con_menos_de_500_m2_nunca_a_precio_de_mayoreo(self):
        for m2 in (1, 250, 499.9):
            with self.subTest(m2=m2):
                r = c.calculo_volumen(m2)
                self.assertEqual(r["precio"], datos.PRECIOS["pasto_solo_m2"])
                self.assertIn("Te faltan", r["aviso"])
        self.assertEqual(c.calculo_volumen(500)["precio"], datos.PRECIOS["pasto_mayoreo_m2"])

    def test_armador_de_palmas_con_las_especies_de_datos_y_labels(self):
        html = c.armador_palmas("pal", "b2b", "Hola, quiero cotizar palmas.")
        self.assertEqual(html.count("data-vt-fila>"), c.FILAS_PALMAS)
        for n in range(1, c.FILAS_PALMAS + 1):
            for campo in ("especie", "altura", "cantidad"):
                self.assertIn(f'<label for="pal-{campo}-{n}">', html)
                self.assertIn(f'id="pal-{campo}-{n}"', html)
        for nombre, cientifico, _precio in datos.PALMAS_PROYECTO:
            self.assertIn(f'<option value="{nombre}">{nombre} ({cientifico})</option>', html)
        self.assertIn(c.OTRA_ESPECIE, html)
        self.assertIn('data-vt-palmas data-hero-cta', html)
        self.assertIn('data-vt-agregar hidden', html)  # sin JS no se ofrece un botón que no hace nada
        self.assertIn('data-cta="b2b:armador"', html)
        self.assertNotRegex(html, r"\$\d")  # sin precio total: depende de la altura

    def test_mensaje_y_resumen_de_palmas(self):
        filas = [("Palma real", "3", "40"), ("Coco plumoso", "", ""), ("", "5", "10")]
        self.assertEqual(c.mensaje_palmas(filas, "Mi empresa").split("\n"), [
            "Hola, quiero cotizar palmas para un proyecto.", "- 40 × Palma real, altura aprox.: 3 m",
            "- ___ × Coco plumoso, altura aprox.: ___", "Empresa: Mi empresa", "Obra y ubicación: ___",
            "Fecha de entrega: ___"])
        self.assertEqual(c.resumen_palmas(filas), "2 especies · 40 piezas")
        self.assertEqual(c.mensaje_palmas([("", "", "")]), "")
        self.assertEqual(c.resumen_palmas([("", "", "")]), c.VACIO_PALMAS)

    def test_repse_verificable(self):
        html = c.repse()
        self.assertIn(f"REPSE {datos.REPSE}", html)
        self.assertIn(f'href="{datos.REPSE_PADRON}" target="_blank" rel="noopener"', html)

    def test_puntos_de_paquetes_con_enlace_en_una_sola_celda(self):
        """.vt-checks li es grid: texto y enlace sueltos serían celdas distintas y el renglón se partía palabra por
        palabra (captura de palmas a 1440). Cada punto va en un <span>."""
        html = c.opciones([{"rotulo": "R", "titulo": "T", "puntos": ('<a href="/x">Mantenimiento</a> después',),
                            "mensaje": "Hola", "precio_texto": "Según cotización", "detalle": "d"}], "b2b")
        self.assertIn('<li><span><a href="/x">Mantenimiento</a> después</span></li>', html)

    def test_tabla_de_especies_agrupa_las_que_se_cotizan(self):
        """Revisión 2d: el nombre científico va bajo el común; en celular las que se cotizan van en un renglón."""
        html = c.tabla_especies((("Palma real", "Roystonea regia", "desde $500", False),
                                 ("Cycas revoluta", "Cycas revoluta", "Según cotización", True)), "Cap",
                                ("Otras 1 especies", "Cycas revoluta", "Según cotización"))
        self.assertIn('<tr><th scope="row"><b>Palma real</b><span><i>Roystonea regia</i></span></th>'
                      '<td class="vt-tabla__p">desde $500</td></tr>', html)
        self.assertIn('<tr class="vt-tabla__cotiza"><th scope="row"><b>Cycas revoluta</b>', html)
        self.assertIn('<tr class="vt-tabla__grupo"><th scope="row"><b>Otras 1 especies</b><span>Cycas revoluta</span>',
                      html)
        self.assertEqual(html.count('<th scope="col"'), 2)

    def test_opcion_sin_detalle(self):
        html = c.opciones([{"rotulo": "R", "titulo": "T", "puntos": ("p",), "mensaje": "Hola",
                            "precio_texto": "Según cotización"}], "b2b")
        self.assertIn('<p class="vt-modo__precio">Según cotización</p>', html)

    def test_formulario_por_correo_para_compras(self):
        """Respuesta del dueño (2026-11-08): formulario por correo para compras, además de WhatsApp."""
        f = {"pagina": "Mayoreo de pasto", "cta": "mayoreo:formulario",
             "cantidad": ("m² totales de la obra", "Ej. 1,200 m²", False, "decimal"),
             "aviso": 'Usamos tus datos solo para responder tu cotización. <a href="/politica-privacidad">Aviso</a>.'}
        html = c.formulario_correo("may", f)
        self.assertIn('name="cantidad" type="text" required inputmode="decimal"', html)
        self.assertIn('<button type="submit" class="vt-btn vt-btn--tinta">', html)
        self.assertIn(f'<p class="vt-correo__aviso">{f["aviso"]}</p>', html)
        self.assertIn(f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}" method="POST"', html)
        self.assertIn('data-vt-correo data-hero-cta data-cta-form="mayoreo:formulario"', html)
        self.assertIn('value="Cotización empresa · Mayoreo de pasto"', html)
        self.assertIn(f'name="_next" value="{datos.SITIO}/gracias"', html)
        self.assertIn('name="_honey"', html)
        self.assertIn('<label for="may-c-cantidad">m² totales de la obra</label>', html)
        self.assertIn('<input id="may-c-cantidad" name="cantidad" type="text"', html)
        self.assertIn('aria-describedby="may-c-correo-error"', html)
        self.assertIn('<p class="vt-correo__error" id="may-c-correo-error" hidden></p>', html)
        self.assertIn('<button type="submit"', html)
        self.assertIn('role="status"', html)
        lista = c.formulario_correo("pal", dict(f, cantidad=("Lista de palmas", "Ej. 40 palma real de 3 m", True)))
        self.assertIn('<textarea id="pal-c-cantidad" name="cantidad"', lista)
        self.assertNotIn("inputmode", lista[lista.index('id="pal-c-cantidad"'):lista.index("</textarea>")])
        self.assertEqual(lista.count("<textarea"), 2)


class EscapeTest(unittest.TestCase):
    def test_bloque_y_figura_escapan_atributos(self):
        html = c.bloque(1, "R", 'a"b', "T", "", id_seccion='c"d')
        self.assertIn('aria-labelledby="a&quot;b"', html)
        self.assertIn('id="c&quot;d"', html)
        self.assertIn('<h2 id="a&quot;b">', html)
        f = c.figura({"src": "/x.webp", "ancho": '1"', "alto": "<2", "alt": "x", "numero": 1, "lugar": "l", "etapa": "e"})
        self.assertIn('width="1&quot;" height="&lt;2"', f)


if __name__ == "__main__":
    unittest.main()
