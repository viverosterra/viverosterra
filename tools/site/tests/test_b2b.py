"""Mayoreo de pasto y palmas para proyectos salen de la plantilla b2b (Etapa 2d): secuencia del spec §3.3, clientes con
nombre y REPSE verificable, un mensaje de compras por paquete, precios de datos.py (mayoreo nunca a $60 con menos de
500 m²; palmas con los precios del dueño y el resto según cotización), anticipo sin porcentaje ni crédito, cotizadores
con su JS y JSON-LD de lo visible. /empresas es de la Etapa 3: mientras tanto nadie la enlaza."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import mensajes_paginas  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

P = datos.PRECIOS
RUTAS = {"mayoreo": "/mayoreo-pasto-tampico", "palmas": "/palmas-mayoreo-proyectos"}
SCRIPTS = {"mayoreo": ["/js/vt-medidor.js", "/js/vt-b2b.js"], "palmas": ["/js/vt-b2b.js"]}
# Respuesta del dueño (2026-11-08): las páginas B2B conservan un formulario por correo para departamentos de compras,
# además de WhatsApp, al mismo endpoint de formsubmit que usan los materiales.
FORMULARIO = f"https://formsubmit.co/{datos.CORREO_FORMULARIOS}"
PAGINA_FORMULARIO = {"mayoreo": "Mayoreo de pasto", "palmas": "Palmas para proyectos"}
# Sin mínimo fijo por especie (respuesta del dueño 3) ni promesas de logística o factura que el dueño no confirmó.
SIN_CONFIRMAR = ("50 por especie", "50 ejemplares", "por especie mínimo", "el día del pago", "maniobra incluida",
                 "maniobra en obra va incluida")
PRECIOS_VIEJOS_PALMAS = ("$850", "$1,200", "$1,500", "$1,600", "$1,800", "$2,000", "$2,200", "$2,400", "$2,800",
                         "$3,200", "$4,200", "$90,000", "$150,000", "$180,000", "$180K", "$260K", "$100K")


def pagina(clave):
    html = (paginas.PUBLIC / RUTAS[clave].strip("/") / "index.html").read_text(encoding="utf-8")
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
    return html, main, textos_publicos(html), grafo


def mensajes_de(html, patron):
    return [unquote(t) for t in re.findall(rf'data-cta="{patron}" href="https://wa\.me/\d+\?text=([^"]+)"', html)]


class ComunTest(unittest.TestCase):
    def test_orden_de_secciones_del_spec(self):
        orden = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', 'data-cta="b2b:hero"', 'id="vt-h-prueba"',
                 'class="vt-logos"', "padrón público de la STPS", 'id="vt-h-precio"', "data-hero-cta data-wa",
                 'id="vt-h-correo"', 'id="vt-h-docs"', 'id="vt-h-opciones"', 'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-faq"',
                 'id="vt-h-cobertura"', 'id="vt-h-rel"', 'class="vt-cierre"')
        for clave in RUTAS:
            _h, main, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                posiciones = [main.index(m) for m in orden]
                self.assertEqual(posiciones, sorted(posiciones))
                self.assertEqual(len(re.findall(r"<h1\b", main)), 1)
                self.assertEqual(main.count('class="vt-pasos"'), 1)

    def test_sin_css_viejo_formularios_ni_parches_de_servicios(self):
        for clave in RUTAS:
            html, _m, _t, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertNotRegex(html, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
                for viejo in ("svc-hero", "<style", "cta-submit", "calc-cta", "window.open", "Sección 1",
                              "sticky-cta", "faq-btn"):
                    self.assertNotIn(viejo, html)
                # Respuesta del dueño (2026-11-08): un solo formulario, el de cotización por correo para compras.
                self.assertEqual(len(re.findall(r"<form\b", html)), 1)
                self.assertIn(f'<form class="vt-correo" action="{FORMULARIO}" method="POST"', html)
                self.assertIn('<body class="vt-pagina">', html)

    def test_scripts_del_cotizador_en_orden(self):
        for clave, esperados in SCRIPTS.items():
            html, _m, _t, _g = pagina(clave)
            propios = [s for s in re.findall(r'<script src="([^"]+)" defer></script>', html) if "/terra." not in s]
            with self.subTest(pagina=clave):
                self.assertEqual(propios, esperados)

    def test_clientes_con_nombre_y_repse_verificable(self):
        for clave in RUTAS:
            _h, main, _t, _g = pagina(clave)
            prueba = main[main.index('id="vt-h-prueba"'):main.index('id="vt-h-precio"')]
            with self.subTest(pagina=clave):
                for cliente in datos.CLIENTES_B2B:
                    self.assertRegex(prueba, rf'alt="{re.escape(cliente)}"|>{re.escape(cliente)}</li>')
                self.assertIn(f'REPSE {datos.REPSE} · <a href="{datos.REPSE_PADRON}"', prueba)

    def test_portada_cierre_y_shell_con_la_plantilla_de_compras(self):
        for clave, ruta in RUTAS.items():
            html, _m, _t, _g = pagina(clave)
            esperado = datos.con_firma(mensajes_paginas.EMPRESAS[ruta])
            with self.subTest(pagina=clave):
                for seccion in ("hero", "cierre", "barra", "footer"):
                    self.assertEqual(set(mensajes_de(html, f"b2b:{seccion}")), {esperado}, seccion)

    def test_tres_paquetes_cada_uno_con_su_mensaje(self):
        for clave in RUTAS:
            html, _m, _t, _g = pagina(clave)
            mensajes = [mensajes_de(html, f"b2b:opcion-{i}") for i in (1, 2, 3)]
            with self.subTest(pagina=clave):
                self.assertTrue(all(len(m) == 1 for m in mensajes))
                planos = [m[0] for m in mensajes]
                self.assertEqual(len(set(planos)), 3)
                for m in planos:
                    self.assertIn("Empresa", m)
                    self.assertTrue(m.endswith(datos.FIRMA))
                self.assertEqual(mensajes_de(html, "b2b:opcion-4"), [])

    def test_anticipo_sin_porcentaje_ni_credito(self):
        for clave in RUTAS:
            _h, _m, texto, _g = pagina(clave)
            with self.subTest(pagina=clave):
                self.assertEqual(texto.count(datos.ANTICIPO_PROYECTOS), 2)  # FAQ visible y FAQPage
                self.assertNotRegex(texto, r"(?i)pago diferido|a crédito|\d+ ?% de anticipo")

    def test_formulario_por_correo_para_compras(self):
        for clave in RUTAS:
            _h, main, _t, _g = pagina(clave)
            form = main[main.index('<form class="vt-correo"'):main.index("</form>") + 7]
            with self.subTest(pagina=clave):
                self.assertIn(f'data-cta-form="{clave}:formulario"', form)
                self.assertIn(f'<input type="hidden" name="_subject" value="Cotización empresa · '
                              f'{PAGINA_FORMULARIO[clave]}">', form)
                self.assertIn(f'<input type="hidden" name="_next" value="{datos.SITIO}/gracias">', form)
                self.assertIn('<input type="hidden" name="_captcha" value="false">', form)
                self.assertRegex(form, r'<input class="vt-correo__miel" type="text" name="_honey" tabindex="-1" '
                                       r'autocomplete="off" aria-hidden="true">')
                campos = re.findall(r'<(?:input|textarea)\b[^>]*\bid="([^"]+)"', form)
                self.assertEqual(len(campos), 8)
                for ident in campos:
                    self.assertIn(f'<label for="{ident}">', form)
                requeridos = re.findall(r'name="(\w+)"[^>]*\brequired', form)
                self.assertEqual(requeridos, ["empresa", "nombre", "correo", "proyecto", "cantidad"])
                self.assertIn('type="email"', form)
                self.assertIn('type="tel"', form)
                self.assertIn('data-hero-cta', form)  # la barra móvil no tapa los campos

    def test_sin_minimo_por_especie_ni_promesas_sin_confirmar(self):
        for clave in RUTAS:
            _h, _m, texto, _g = pagina(clave)
            for frase in SIN_CONFIRMAR:
                with self.subTest(pagina=clave, frase=frase):
                    self.assertNotIn(frase.lower(), texto.lower())

    def test_empresas_todavia_sin_enlace(self):
        """/empresas es de la Etapa 3 (spec §3.5): hasta entonces ninguna página la enlaza."""
        for path in paginas.PUBLIC.rglob("*.html"):
            with self.subTest(pagina=str(path.relative_to(paginas.PUBLIC))):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r'href="/empresas(?:[/"#?])')

    def test_las_paginas_para_empresas_se_enlazan_entre_si(self):
        for clave, ruta in RUTAS.items():
            _h, main, _t, _g = pagina(clave)
            rel = main[main.index('id="vt-h-rel"'):main.index('class="vt-cierre"')]
            otros = [r for r in RUTAS.values() if r != ruta]
            with self.subTest(pagina=clave):
                for destino in otros + ["/mantenimiento-jardines-tampico", "/sistema-riego-tampico"]:
                    self.assertIn(f'href="{destino}"', rel)
                self.assertNotIn(f'href="{ruta}"', rel)

    def test_faq_y_json_ld_dicen_lo_mismo(self):
        for clave in RUTAS:
            _h, main, _t, grafo = pagina(clave)
            visibles = [re.sub(r"<[^>]+>", "", q) for q in re.findall(r"<summary>(.*?)</summary>", main)]
            faq = next(n for n in grafo if n["@type"] == "FAQPage")
            with self.subTest(pagina=clave):
                self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)
                self.assertGreaterEqual(len(visibles), 8)


class MayoreoTest(unittest.TestCase):
    def test_precio_y_minimo_de_datos(self):
        _h, main, texto, _g = pagina("mayoreo")
        portada = main[:main.index('id="vt-h-prueba"')]
        self.assertIn(f"<b>${P['pasto_mayoreo_m2']}</b>", portada)
        self.assertIn(f"{P['pasto_mayoreo_minimo_m2']} m²", portada)
        self.assertIn(f"a partir de {P['pasto_mayoreo_minimo_m2']} m²", texto)

    def test_con_menos_de_500_m2_nunca_a_60(self):
        _h, main, texto, _g = pagina("mayoreo")
        minimo, mayoreo, solo = P["pasto_mayoreo_minimo_m2"], P["pasto_mayoreo_m2"], P["pasto_solo_m2"]
        fila = re.search(rf'<th scope="row">Menos de {minimo} m²</th>(.*?)</tr>', main).group(1)
        self.assertIn(f"${solo}", fila)
        self.assertNotIn(f"${mayoreo}", fila)
        self.assertNotRegex(texto, rf"(?:menos de|bajo) {minimo} m²[^.]{{0,40}}\${mayoreo}\b")
        self.assertIn(f'&quot;minimo&quot;:{minimo}', main)

    def test_opinion_real_de_una_constructora(self):
        _h, main, _t, _g = pagina("mayoreo")
        cita, nombre, detalle = datos.OPINIONES_PASTO_EN_ROLLO[1]
        self.assertIn(f"<p>“{cita}”</p>", main)
        self.assertIn(f"<b>{nombre}</b><span>{detalle}</span>", main)

    def test_json_ld_como_estaba_publicado(self):
        _h, _m, _t, grafo = pagina("mayoreo")
        self.assertEqual([n["@type"] for n in grafo], ["Service", "FAQPage", "BreadcrumbList", "SpeakableSpecification"])
        self.assertEqual(grafo[0]["provider"]["address"]["streetAddress"], datos.CALLE)


class PalmasTest(unittest.TestCase):
    def test_tabla_de_especies_con_los_precios_del_dueno(self):
        _h, main, _t, _g = pagina("palmas")
        tabla = main[main.index('id="vt-h-precio"'):main.index("<h3", main.index('id="vt-h-precio"'))]
        for nombre, cientifico, precio in datos.PALMAS_PROYECTO:
            fila = re.search(rf'<th scope="row">{re.escape(nombre)}</th>(.*?)</tr>', tabla).group(1)
            with self.subTest(especie=nombre):
                self.assertIn(f"<i>{cientifico}</i>", fila)
                esperado = f"desde ${precio:,} · tamaño chico" if precio else "Según cotización por altura y volumen"
                self.assertIn(esperado, fila)

    def test_sin_precios_ni_proyectos_viejos(self):
        _h, _m, texto, _g = pagina("palmas")
        for viejo in PRECIOS_VIEJOS_PALMAS + ("Casos anónimos", "bajo NDA", "Lead time", "spec sheet", "+15",
                                               "fianzas de cumplimiento", "alta en padrón", "80+"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, texto)

    def test_armador_con_todas_las_especies(self):
        _h, main, _t, _g = pagina("palmas")
        armador = main[main.index("data-vt-palmas"):]
        for nombre, _c, _p in datos.PALMAS_PROYECTO:
            self.assertEqual(armador.count(f'<option value="{nombre}">'), 3)
        self.assertIn('data-cta="b2b:armador"', armador)

    def test_fotos_de_especies_del_vivero(self):
        """Respuesta del dueño (2026-11-08): las fotos de especies son de su vivero y el pie lo dice."""
        _h, main, _t, _g = pagina("palmas")
        for especie in ("Coco plumoso", "Palma areca"):
            with self.subTest(especie=especie):
                self.assertRegex(main, rf"<b>Fig\. \d\d</b> · {especie}</span><span>En nuestro vivero</span>")

    def test_precios_de_palmas_solo_los_del_dueno(self):
        """Respuesta del dueño (2026-11-08): los precios por talla de proyecto ($850–$4,200) no son reales."""
        for clave in RUTAS:
            _h, _m, texto, _g = pagina(clave)
            for viejo in PRECIOS_VIEJOS_PALMAS:
                with self.subTest(pagina=clave, viejo=viejo):
                    self.assertNotIn(viejo, texto)
        _h, _m, texto, _g = pagina("palmas")
        self.assertIn("el precio sube con la altura", texto)
        self.assertIn("Según cotización por altura y volumen", texto)

    def test_garantia_de_plantas_condicionada(self):
        _h, main, _t, _g = pagina("palmas")
        garantia = main[main.index('id="vt-h-garantia"'):main.index('id="vt-h-faq"')]
        self.assertIn("/politicas#garantia-plantas", garantia)
        self.assertIn("sembramos", garantia)

    def test_json_ld_con_precios_nuevos(self):
        _h, _m, texto, grafo = pagina("palmas")
        servicio = grafo[0]
        self.assertEqual(servicio["offers"], {"@type": "AggregateOffer", "lowPrice": "250", "priceCurrency": "MXN",
                                              "offerCount": "12"})
        lista = next(n for n in grafo if n["@type"] == "ItemList")["itemListElement"]
        con_precio = {e["item"]["name"]: e["item"]["offers"]["price"] for e in lista if "offers" in e["item"]}
        self.assertEqual(con_precio, {"Palma areca": "250", "Coco plumoso": "250", "Palma real": "500"})
        self.assertEqual(len(lista), 12)
        self.assertNotIn("InStock", texto)
        self.assertEqual([n["@type"] for n in grafo],
                         ["Service", "LocalBusiness", "ItemList", "FAQPage", "BreadcrumbList", "SpeakableSpecification"])


if __name__ == "__main__":
    unittest.main()
