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
    """Nodo del @graph de la home con ese tipo (SEO fase 1: un solo bloque con @graph)."""
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S):
        for nodo in json.loads(bloque).get("@graph", ()):
            if tipo in ([nodo["@type"]] if isinstance(nodo["@type"], str) else nodo["@type"]):
                return nodo
    raise AssertionError(tipo)


class InicioTest(unittest.TestCase):
    def test_banner_de_nochebuenas_es_lo_primero_y_todo_enlaza(self):
        """Pedido del dueño (2026-11-09): algo llamativo por la temporada, arriba de la portada, que lleve a Nochebuenas."""
        ruta = datos.NOCHEBUENAS["ruta"]
        self.assertRegex(MAIN.lstrip(), rf'^<aside class="vt-navidad-x" aria-label="Temporada de Nochebuenas"><a class="vt-navidad" data-cta="home:banner-nochebuenas" href="{ruta}">')
        banner = re.search(r'<a class="vt-navidad".*?</a>', MAIN, re.S).group(0)
        plano = re.sub(r"<[^>]+>", "", banner)
        for frase in ("Nochebuenas 2026", "Pedidos abiertos", "Desde $89 en menudeo y desde $65 por volumen", "Ver nochebuenas"):
            self.assertIn(frase, plano)
        self.assertEqual(MAIN.count(f'href="{ruta}"'), 1, "un solo enlace de temporada en la home: el banner sustituye a la franja")
        self.assertIn('<body class="vt-pagina vt-inicio vt-temporada">', HTML)
        self.assertIn("/css/terra-temporada.", HTML[:HTML.index("</head>")])
        self.assertIn("/css/terra-inicio.", HTML[:HTML.index("</head>")])

    def test_secuencia_de_la_plantilla(self):
        marcas = ('class="vt-portada"', 'class="vt-datos"', 'id="vt-h-que"', 'data-vt-medidor', 'id="vt-h-obras"',
                  'class="vt-logos"', 'id="vt-h-opiniones"', 'id="vt-h-como"', 'id="vt-h-precios"', 'id="vt-h-faq"', 'id="vt-h-cobertura"', 'class="vt-cierre"')
        posiciones = [MAIN.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_h1_y_un_solo_h1(self):
        self.assertEqual(re.findall(r"<h1\b[^>]*>(.*?)</h1>", HTML, re.S),
                         ["Pasto, jardines y plantas en Tampico."])
        self.assertIn('</h1><p class="vt-portada__lema vt-serif">Todo para tu jardín, en un solo lugar.</p>', MAIN)

    def test_portada_con_precio_cta_y_foto_principal(self):
        portada = MAIN[:MAIN.index('id="vt-h-que"')]
        # Dueño (2026-11-10): "con IVA" va ligado al instalado (en su banda), no en la cabecera que cubría también la
        # fila de solo pasto.
        self.assertIn("<b>$120</b><span>/m² con IVA</span>", portada)
        self.assertNotIn("Con IVA", portada)
        self.assertIn(f"<span>Pasto · 01</span><span>Precios {datos.ANIO}</span>", portada)
        self.assertIn("<b>$85 /m²</b>", portada)
        self.assertIn("data-hero-cta", portada)
        self.assertIn('data-cta="home:hero"', portada)
        self.assertIn('href="#medidor"', portada)
        self.assertIn('loading="eager" fetchpriority="high"', portada)
        self.assertIn('<link rel="preload" as="image" href="/img/obra/cuadrilla-tendiendo-pasto-san-agustin.webp"', HTML)

    def test_hero_con_un_solo_boton_dos_enlaces_y_linea_de_confianza(self):
        """Spec del hero (2026-11-09, §1): kicker, lede, un botón de WhatsApp, dos enlaces de texto y confianza."""
        portada = MAIN[MAIN.index('class="vt-portada"'):MAIN.index('id="vt-h-que"')]
        self.assertIn(f'<p class="vt-kicker">Vivero y cuadrilla propia · Desde {datos.DESDE}</p>', portada)
        self.assertIn(f'<p class="vt-lede">Pasto San Agustín en rollo, diseño de jardines y {datos.VARIEDADES} variedades '
                      "de plantas, en Tampico, Madero y Altamira.</p>", portada)
        self.assertEqual(portada.count("vt-btn--wa"), 1)
        self.assertNotIn("vt-btn--linea", portada)
        self.assertRegex(portada, r'<div class="vt-portada__cta" data-hero-cta><a class="vt-btn vt-btn--wa" data-cta="home:hero" ')
        self.assertIn('<a data-cta="home:hero" href="#medidor" id="vt-calcula-patio">Calcula tu patio <span aria-hidden="true">→</span></a>', portada)
        self.assertIn(f'<a data-cta="home:hero" href="tel:{datos.TELEFONO_TEL}">Llamar {datos.TELEFONO_VISIBLE}</a>', portada)
        confianza = re.search(r'<p class="vt-portada__confianza">(.*?)</p>', portada, re.S).group(1)
        plano = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", confianza)).strip()
        # Con separadores reales en el DOM (decorativos: aria-hidden), para que sin CSS no se lea pegado.
        self.assertEqual(plano, f"{datos.PROMESA_COMPLETA} · {datos.GOOGLE} · {datos.CLIENTES} clientes")
        self.assertEqual(confianza.count('<span class="vt-portada__sep" aria-hidden="true"> · </span>'), 2)
        self.assertNotIn("También:", portada)
        self.assertNotIn("vt-portada__tambien", portada)
        # Entrega A de experiencia (2026-11-10): la home usa el componente común, con la foto antes de la etiqueta en el
        # DOM; sin vt-portada--pliegue, terra.css la manda al final en celular (order) y la etiqueta queda, como antes,
        # entre el lede y el botón. El cuadro de datos sigue igual.
        self.assertNotIn("vt-portada--pliegue", portada)
        orden = [portada.index(m) for m in ('class="vt-lede"', 'class="vt-portada__foto"', 'class="vt-etiqueta"', "data-hero-cta",
                                            'class="vt-datos"')]
        self.assertEqual(orden, sorted(orden))

    def test_metas_y_toda_la_home_sin_gratis(self):
        """Spec del hero §2: ni la descripción, ni Open Graph, ni Twitter, ni el resto de la home dicen "gratis"; "sin
        costo" solo en la garantía de arraigo que aprobó el dueño."""
        metas = re.findall(r'<meta (?:name|property)="(?:description|og:description|twitter:description)" content="([^"]*)"', HTML)
        self.assertEqual(len(metas), 3)
        for contenido in metas:
            self.assertNotRegex(contenido, r"(?i)gratis|gratuit|sin costo")
            self.assertIn("Cotiza por WhatsApp: respondemos en menos de 1 hora en horario.", contenido)
        # Revisión (2026-11-09): sin "con IVA" en las metas (el pasto sin instalar no lleva IVA) y description ≤ 155.
        for contenido in metas:
            self.assertNotIn("IVA", contenido)
        self.assertIn("Precios a la vista.", metas[0])
        self.assertLessEqual(len(metas[0]), 155)
        self.assertEqual(metas[0], metas[1])
        self.assertNotRegex(TEXTO, r"(?i)\bgratis\b|\bgratuit\w*|\bsin cargo\b")
        self.assertEqual(len(re.findall(r"(?i)\bsin costo\b", TEXTO)), len(re.findall(r"la reponemos sin costo", TEXTO)))

    def test_abierto_ahora_solo_marca_la_promesa_de_portada_y_cierre(self):
        """Spec del hero §3: el horario y los festivos viajan en data-*; la promesa queda contigua y el HTML no dice
        "Abierto ahora" (lo antepone terra.js en horario). Sin aria-live."""
        marca = f'<span data-vt-horario="{datos.horario_marca()}" data-vt-festivos="{datos.festivos_marca()}" data-vt-build="{datos.ACTUALIZADO}">{datos.PROMESA_COMPLETA}</span>'
        self.assertEqual(MAIN.count(marca), 2)
        self.assertEqual(MAIN.count("data-vt-horario"), 2)
        self.assertIn(marca, MAIN[MAIN.index('class="vt-portada"'):MAIN.index('id="vt-h-que"')])
        self.assertIn(marca, MAIN[MAIN.index('class="vt-cierre"'):])
        self.assertNotIn("Abierto ahora", HTML)
        self.assertNotIn("aria-live", MAIN)

    def test_medidor_boton_que_esconde_la_barra_y_garantia(self):
        medidor = MAIN[MAIN.index("data-vt-medidor"):MAIN.index('id="vt-h-obras"')]
        self.assertNotIn("data-vt-medidor data-hero-cta", MAIN)
        self.assertEqual(medidor.count("data-hero-cta"), 1)
        self.assertIn('data-cta="home:medidor" data-vt-o="cta" data-hero-cta', medidor)
        self.assertIn('<span data-vt-o="cta-texto">Cotizar por WhatsApp</span>', medidor)
        self.assertNotIn("Enviar mi medida por WhatsApp", HTML)  # lo escribe vt-medidor.js cuando hay medida
        garantia = re.search(r'<p class="vt-medidor__garantia" data-vt-o="garantia">(.*?)</p>', medidor).group(1)
        # Plan visual V1: bajo el Medidor va la versión corta; la completa queda en el cierre.
        self.assertEqual(re.sub(r"<[^>]+>", "", garantia), f"Garantía de arraigo de {datos.ARRAIGO} en el pasto instalado (ver condiciones).")
        self.assertIn('<a href="/protocolo-cuidados-pasto-san-agustin#garantia">ver condiciones</a>', garantia)
        self.assertIn('<p class="vt-medidor__vivo" data-vt-o="vivo"></p>', medidor)
        self.assertLess(medidor.index("vt-medidor__medidas"), medidor.index("vt-medidor__vivo"))
        self.assertLess(medidor.index("vt-medidor__vivo"), medidor.index("¿Qué necesitas?"))
        self.assertIn('data-vt-barra="Enviar mi medida"', MAIN)
        self.assertLess(medidor.index('data-vt-o="cta"'), medidor.index("vt-medidor__garantia"))

    def test_cada_servicio_del_indice_con_su_whatsapp(self):
        """Spec del hero §5: cada fila de "Qué hacemos" cotiza su servicio con el mensaje de datos.MENSAJES."""
        indice = MAIN[MAIN.index('class="vt-indice"'):MAIN.index('data-vt-medidor')]
        enlaces = re.findall(r'<a class="vt-indice__wa" data-cta="home:indice-([a-z-]+)" href="https://wa\.me/528333268008\?text=([^"]+)" '
                             r'target="_blank" rel="noopener"><span class="vt-wa-g"><svg aria-hidden="true"><use href="#vt-i-wa"/></svg></span>'
                             r'(Cotizar [^<]+)</a>', indice)
        self.assertEqual([s for s, _t, _r in enlaces], ["pasto-natural", "pasto-sintetico", "jardin", "plantas", "empresas"])
        for servicio, texto, rotulo in enlaces:
            with self.subTest(servicio=servicio):
                self.assertEqual(unquote(texto), datos.mensaje(servicio))
        # Textos cortos (no se parten en celular) y con el glifo de WhatsApp: la flecha es solo la de la fila.
        self.assertEqual([rotulo for _s, _t, rotulo in enlaces],
                         ["Cotizar pasto", "Cotizar sintético", "Cotizar jardín", "Cotizar plantas", "Cotizar proyecto"])
        self.assertEqual(indice.count("→"), 5)

    def test_cta_de_whatsapp_al_final_de_opiniones_proceso_precios_y_preguntas(self):
        """Spec del hero §6: el tramo largo sin CTA ahora tiene uno al final de cada sección."""
        """Revisión de diseño (2026-11-09): cada fila esconde la barra fija mientras se ve (data-hero-cta), su botón
        dice a qué invita. Plan visual V1 (2026-11-11): ninguna lleva la promesa debajo (va en el hero y en el cierre)."""
        limites = (("opiniones", 'id="vt-h-opiniones"', 'id="vt-h-como"', "Cotizar mi jardín por WhatsApp", False),
                   ("proceso", 'id="vt-h-como"', 'id="vt-h-precios"', "Empezar por WhatsApp", False),
                   ("precios", 'id="vt-h-precios"', 'id="vt-h-faq"', "Pedir mi precio por WhatsApp", False),
                   ("faq", 'id="vt-h-faq"', 'id="vt-h-cobertura"', "Preguntar por WhatsApp", False))
        for seccion, inicio, fin, texto, con_promesa in limites:
            tramo = MAIN[MAIN.index(inicio):MAIN.index(fin)]
            with self.subTest(seccion=seccion):
                self.assertEqual(MAIN.count(f'data-cta="home:{seccion}"'), 1)
                boton = re.search(rf'<div class="vt-inicio__fila" data-hero-cta><a class="vt-btn vt-btn--wa" data-cta="home:{seccion}" '
                                  r'href="https://wa\.me/528333268008\?text=([^"]+)" target="_blank" rel="noopener">(.*?)</a>', tramo)
                self.assertEqual(unquote(boton.group(1)), datos.mensaje("general"))
                self.assertEqual(re.sub(r"<[^>]+>", "", boton.group(2)), f"{texto}→")
                cola = tramo[tramo.index(f'data-cta="home:{seccion}"'):]
                self.assertEqual(f'<p class="vt-promesa">{datos.PROMESA_COMPLETA}</p></div>' in cola, con_promesa)
                self.assertNotRegex(cola, r"<(?:table|details|blockquote|ol)\b")

    def test_cierre_promesa_antes_del_boton_garantia_y_costo_de_visita_despues(self):
        """Spec del hero §7: lo último antes del botón es la promesa de respuesta; la garantía y la frase del costo de
        la visita van después."""
        cierre = MAIN[MAIN.index('class="vt-cierre"'):]
        orden = [cierre.index(m) for m in ("data-vt-horario", 'data-cta="home:cierre"', "Pasto instalado: s" + datos.GARANTIA_PASTO[1:40],
                                           "agendamos una visita para medir y cotizar", datos.VISITA_COSTO,
                                           'class="vt-cierre__msg"')]
        self.assertEqual(orden, sorted(orden))
        entre = cierre[cierre.index("</span>", cierre.index("data-vt-horario")):cierre.index('<a class="vt-btn vt-btn--wa" data-cta="home:cierre"')]
        self.assertEqual(re.sub(r"<[^>]+>", "", entre).strip(), "", "nada de texto entre la promesa y el botón")
        self.assertIn('(<a href="/protocolo-cuidados-pasto-san-agustin#garantia">ver condiciones</a>).', cierre)
        self.assertIn(f"Llamar {datos.TELEFONO_VISIBLE}", cierre)

    def test_banner_con_los_dias_de_preventa_vacios_en_el_html(self):
        """Spec del hero §9: el <span> sale vacío con la fecha de datos.py; terra.js escribe los días que faltan."""
        hasta = datos.NOCHEBUENAS["preventa"]["hasta"]
        banner = re.search(r'<a class="vt-navidad".*?</a>', MAIN, re.S).group(0)
        self.assertEqual(banner.count("data-vt-hasta"), 1)
        self.assertIn(f'<span class="vt-navidad__precios">Desde $89 en menudeo y desde $65 por volumen</span>'
                      f'<span class="vt-navidad__hasta" data-vt-hasta="{hasta}" data-vt-build="{datos.ACTUALIZADO}"></span>', banner)
        self.assertNotRegex(re.sub(r"<[^>]+>", "", banner), r"(?i)preventa|faltan")
        self.assertEqual(HTML.count("data-vt-hasta"), 1)

    def test_enlace_a_las_resenas_de_google_en_opiniones(self):
        opiniones = MAIN[MAIN.index('id="vt-h-opiniones"'):MAIN.index('id="vt-h-como"')]
        self.assertIn(f'<p class="vt-inicio__resenas"><a href="{datos.MAPS_URL}" target="_blank" rel="noopener">'
                      "Ver las reseñas en Google</a></p>", opiniones)
        self.assertLess(opiniones.index("</ul>"), opiniones.index("vt-inicio__resenas"))
        self.assertLess(opiniones.index("vt-inicio__resenas"), opiniones.index('data-cta="home:opiniones"'))

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
        # Las tres menciones de la garantía de arraigo enlazan a las condiciones del pasto (antes, a /politicas).
        self.assertEqual(MAIN.count('<a href="/protocolo-cuidados-pasto-san-agustin#garantia">ver condiciones</a>'), 3)
        self.assertNotIn('href="/politicas"', MAIN)
        self.assertTrue((paginas.PUBLIC / "protocolo-cuidados-pasto-san-agustin.html").is_file())

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
        # SEO fase 0 (2026-11-10): la home no es una ruta; su BreadcrumbList enumeraba el menú y Google pintaba
        # "› … › Catálogo" como si fuera la jerarquía de la página.
        self.assertNotIn("BreadcrumbList", HTML)

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

    def test_seo_jardineria_cobertura_twitter_y_sin_hreflang(self):
        h2 = re.findall(r"<h2\b[^>]*>(.*?)</h2>", MAIN, re.S)
        self.assertTrue(any("Jardinería" in t for t in h2), h2)
        cobertura = MAIN[MAIN.index('id="vt-h-cobertura"'):MAIN.index('class="vt-cierre"')]
        for lugar in ("Tampico", "Madero", "Altamira", "Huasteca"):
            self.assertIn(lugar, cobertura)
        for _nombre, href in datos.ZONAS:
            self.assertIn(f'href="{href}"', cobertura)
        for nombre in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
            self.assertIn(f'<meta name="{nombre}" content=', HTML)
        # SEO fase 0 (2026-11-10): el hreflang solo existía en la home y sin pareja (un solo idioma): no dice nada.
        self.assertNotIn("hreflang", HTML)

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
