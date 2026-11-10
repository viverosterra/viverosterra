"""Reglas del dueño en las páginas de materiales (Etapa 2f y respuestas del 2026-11-08): precios solo de datos.py (lo
demás "según cotización"), sin "gratis" ni existencias ni plazos de entrega, sin superlativos ni cifras sin respaldo,
opiniones solo las confirmadas (datos.OPINIONES_TIERRA_NEGRA y OPINIONES_PIEDRA_BOLA, sin calificación en el JSON-LD),
"sujeto a disponibilidad" solo junto al precio del mármol, "sin mínimo" solo como datos.SIN_MINIMO, sin peso de costal
en tierra y tezontle, piedra bola sin medidas, sin "En nuestro vivero" en fotos, sin window.open, las mismas fotos de
main en su orden y el formulario de pedido intacto.

PENDIENTES lista las páginas que todavía no salen de su plantilla: solo puede encoger (cada tarea de migración saca la
suya) y al cerrar la Etapa 2f queda vacía."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import medicion_js  # noqa: E402
import paginas  # noqa: E402
import paridad  # noqa: E402
import paridad_materiales  # noqa: E402
from componentes import dinero  # noqa: E402

PUBLIC = paginas.PUBLIC
MATERIALES = {
    "/tierra-negra-vegetal-tampico": "tierra-negra-vegetal-tampico/index.html",
    "/tezontle-rojo-tampico": "tezontle-rojo-tampico/index.html",
    "/marmol-blanco-tampico": "marmol-blanco-tampico/index.html",
    "/piedra-bola-rio-tampico": "piedra-bola-rio-tampico/index.html",
}
PENDIENTES = frozenset()
CAPTURA = json.loads(paridad_materiales.CAPTURA.read_text(encoding="utf-8"))
# Fotos reales que el dueño aprobó agregar después de la captura de main (las de main siguen iguales y en su orden).
FOTOS_AGREGADAS = {"/marmol-blanco-tampico": ("/img/marmol-blanco-costales-vivero-tampico-1200.webp",)}  # 2026-11-09
# Precios de datos.PRECIOS y, del mármol, el precio por m² que sale del saco (3 a 5 sacos por m²: $750 a $1,250).
PERMITIDOS = ({dinero(n) for v in datos.PRECIOS.values() for n in (v if isinstance(v, tuple) else (v,))
               if isinstance(n, int)} | {dinero(n * datos.PRECIOS["marmol_saco"]) for n in (3, 4, 5)})
PRECIO_RE = re.compile(r"\$\s?\d[\d,]*\d|\$\s?\d")
# Lo que sigue sin precio publicado (dueño, 2026-11-08: "según cotización"): la piedra bola y el m³ y el camión del
# tezontle. Como $200 y $1,500 sí están en datos.py, se detectan por cercanía.
SIN_PRECIO_RE = re.compile(r"piedra bola[^.$]{0,30}\$\s?\d", re.I)
SIN_PRECIO_TEZONTLE_RE = re.compile(r"(?:\bm³|cami[oó]n(?:es)?)[^.$]{0,25}\$\s?\d", re.I)
# Palabras del dueño que solo se publican así (2026-11-08): "sujeto a disponibilidad" junto al precio del mármol y "Sin
# mínimo de compra." (datos.SIN_MINIMO). Se quitan antes de buscar los términos prohibidos.
MARMOL_CONDICION_RE = re.compile(re.escape(datos.MARMOL_CONDICION), re.I)
JUNTO_AL_PRECIO = 120  # caracteres: "sujeto a disponibilidad" va cerca del $250
CALCULADORA_RE = re.compile(r'<div class="vt-b2b" data-vt-material.*?</a></div></div></div>', re.S)
# Peso de costal (el dueño no lo tiene) y medidas de la piedra bola (se vende a granel).
PESO_COSTAL_RE = re.compile(r"\b\d+\s?(?:a|–|-)?\s?\d*\s?kg\b(?![^.]{0,20}por m)", re.I)
MEDIDAS_PIEDRA_RE = re.compile(r"\b(?:chica|peque[ñn]a|mediana|grande)s?\b|tres medidas|\bpor medida\b"
                               r"|\b2 a 5 cm\b|\b6 a 12 cm\b|\b12 a 20 cm\b|\b2 a 20 cm\b", re.I)
SIN_VERIFICAR = (
    ("gratis o sin costo", r"\bgratis\b|\bgratuit\w*|\bsin costo\b"),
    ("existencias o disponibilidad", r"InStock|\bdisponibilidad\b|\ben existencia\b|\bdisponibles? (?:hoy|ya)\b"
                                     r"|cantidad sin l[ií]mite|\bagotad"),
    ("plazo de entrega", r"entrega inmediata|entrega (?:el )?mismo d[ií]a|\ben 24 ?h|\bhoy mismo\b|entrega r[aá]pida"),
    ("más vendido o superlativo", r"m[aá]s vendid|\+\s?vendid|\bel mejor\b|\bimbatible\b|\bincomparable\b"
                                  r"|\binigualable\b|m[aá]s popular|calidad importada"),
    ("cifras sin respaldo", r"\+\s?500 jardines|\+\s?300 jardines|\+\s?18 años|\b\d{2}\s?% (?:m[aá]s r[aá]pido|de la maleza)"
                            r"|del 60\s?% al 95\s?%|hasta 8\s?°C|productor directo"),
    ("calificación de opiniones en el JSON-LD", r"aggregateRating|\"Review\"|reviewRating|ratingValue"),
    ("En nuestro vivero", r"en nuestro vivero"),
    # Revisión 2f: términos comerciales que el dueño no ha confirmado (calidad de la piedra, "desde 1 m³"). "Sin mínimo"
    # solo con las palabras de datos.SIN_MINIMO (se quitan antes) y nunca "camión desde $5,000".
    ("término comercial sin confirmar", r"\bsin m[ií]nimo\b|\b(?:desde|a partir de) 1 m(?:³|3)\b|\blavada\b"
                                        r"|\bcalibrad[ao]\b|saco de red|cami[oó]n[^.]{0,20}desde"),
)


def html_de(ruta):
    return (PUBLIC / MATERIALES[ruta]).read_text(encoding="utf-8")


def visible_y_ld(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    metas = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:[a-z:]+)" content="([^"]*)"', html))
    titulo = " ".join(re.findall(r"<title>(.*?)</title>", html))
    return " ".join((paridad.texto(paridad.principal(html)), ld, metas, titulo))


def sin_opiniones(html):
    """El <main> sin el bloque de opiniones (citas textuales del cliente: pueden nombrar una medida o un peso)."""
    return re.sub(r'<ul class="vt-testimonios">.*?</ul>', " ", html, flags=re.S)


def fallas(ruta):
    """Lista de reglas que rompe la página (vacía si cumple todas)."""
    html = html_de(ruta)
    texto = visible_y_ld(html)
    salida = [f"precio que no está en datos.py: {p}"
              for p in sorted({m.group(0).replace(" ", "") for m in PRECIO_RE.finditer(texto)} - PERMITIDOS)]
    # "Otros materiales" resume los precios de las otras páginas (camión de tierra negra incluido): no cuenta aquí.
    sin_otros = visible_y_ld(re.sub(r'<ul class="vt-otros">.*?</ul>', " ", html, flags=re.S))
    if ruta == "/piedra-bola-rio-tampico":
        salida += [f"piedra bola con precio: …{m.group(0)}…" for m in SIN_PRECIO_RE.finditer(sin_otros)]
    if ruta == "/tezontle-rojo-tampico":
        salida += [f"m³ o camión del tezontle con precio: …{m.group(0)}…"
                   for m in SIN_PRECIO_TEZONTLE_RE.finditer(sin_otros)]
    limpio = texto
    if ruta == "/marmol-blanco-tampico":
        salida += [f"“sujeto a disponibilidad” lejos del precio: …{texto[max(0, m.start() - 40):m.end()]}…"
                   for m in MARMOL_CONDICION_RE.finditer(texto)
                   if not re.search(r'\$250|"price":\s*"?250\b', texto[max(0, m.start() - JUNTO_AL_PRECIO):m.end() + JUNTO_AL_PRECIO])]
        limpio = MARMOL_CONDICION_RE.sub(" ", texto)
    limpio = limpio.replace(datos.SIN_MINIMO, " ")
    salida += [f"{regla}: {m.group(0)}" for regla, patron in SIN_VERIFICAR for m in re.finditer(patron, limpio, re.I)]
    sin_citas = visible_y_ld(sin_opiniones(html))
    if ruta in ("/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico"):
        salida += [f"peso de costal: {m.group(0)}" for m in PESO_COSTAL_RE.finditer(sin_citas)]
    if ruta == "/piedra-bola-rio-tampico":
        salida += [f"medida de piedra bola: {m.group(0)}" for m in MEDIDAS_PIEDRA_RE.finditer(sin_citas)]
    elif re.search(r"piedra (?:bola|de r[ií]o)[^.]{0,120}(?:tres medidas|chica|mediana|grande|2 a 20 cm)", sin_citas,
                   re.I):
        salida.append("la piedra bola con medidas en otra página")
    if ruta == "/marmol-blanco-tampico":
        salida += [f"peso del saco fuera de la calculadora: {m.group(0)}"
                   for m in re.finditer(r"\b20 kg", visible_y_ld(CALCULADORA_RE.sub(" ", html)))]
    if datos.ANTICIPO not in texto:
        salida.append("sin datos.ANTICIPO")
    if "window.open(" in html or medicion_js.medir_whatsapp_js(html)[1] != {"eventos": 0, "aperturas": 0, "omitidas": 0}:
        salida.append("abre WhatsApp con window.open (debe ser un enlace con data-cta)")
    nuevas = paridad_materiales.extraer(ruta)
    nuevas = dict(nuevas, fotos=[f for f in nuevas["fotos"] if f["src"] not in FOTOS_AGREGADAS.get(ruta, ())])
    if [f["src"] for f in nuevas["fotos"]] != [f["src"] for f in CAPTURA[ruta]["fotos"]]:
        salida.append(f"fotos distintas a las de main o en otro orden: {[f['src'] for f in nuevas['fotos']]}")
    for vieja, nueva in zip(CAPTURA[ruta]["fotos"], nuevas["fotos"]):
        if vieja["srcset"] and nueva["srcset"] != vieja["srcset"]:
            salida.append(f"srcset distinto en {vieja['src']}")
    for img in re.findall(r"<img\b[^>]*>", paridad.principal(html)):
        if not all(f' {a}="' in img for a in ("width", "height", "alt")):
            salida.append(f"imagen sin width/height/alt: {img[:80]}")
    esperado = dict(CAPTURA[ruta]["formulario"], _honey="")
    if nuevas["formulario"] != esperado:
        salida.append(f"formulario distinto al de main: {nuevas['formulario']}")
    if f'action="https://formsubmit.co/{datos.CORREO_FORMULARIOS}"' not in html or 'id="solicitar-pedido"' not in html:
        salida.append("formulario sin la cuenta oficial o sin el ancla #solicitar-pedido")
    return salida


class MaterialesReglasTest(unittest.TestCase):
    def test_paginas_migradas_cumplen(self):
        for ruta in sorted(set(MATERIALES) - PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertEqual(fallas(ruta), [])

    def test_pendientes_todavia_fallan(self):
        for ruta in sorted(PENDIENTES):
            with self.subTest(ruta=ruta):
                self.assertNotEqual(fallas(ruta), [], "ya cumple: sácala de PENDIENTES")

    def test_precios_de_materiales_de_datos(self):
        """Los únicos precios de materiales que dio el dueño (datos.PRECIOS, respuestas del 2026-11-08): nada de piedra
        bola, ni m³ ni camión de tezontle, ni el "camión desde $5,000"."""
        p = datos.PRECIOS
        self.assertEqual((p["tierra_negra_costal"], p["tierra_negra_m3"], p["tierra_preparada_costal"],
                          p["tezontle_costal"], p["marmol_saco"]), (90, 1500, 100, 200, 250))
        self.assertEqual(datos.TIERRA_CAMIONES, ((5, 3500), (8, 5200), (14, 8000)))
        materiales = {"tierra_negra_costal", "tierra_negra_m3", "tierra_preparada_costal", "tierra_negra_camion_5m3",
                      "tierra_negra_camion_8m3", "tierra_negra_camion_14m3", "tezontle_costal", "marmol_saco"}
        for clave in set(p) - materiales:
            with self.subTest(clave=clave):
                self.assertFalse(re.search(r"tierra|tezontle|marmol|piedra|camion", clave),
                                 "precio nuevo de material: confírmalo con el dueño")
        self.assertNotIn(5000, [v for k, v in p.items() if k in materiales])

    def test_condiciones_del_dueno_en_las_cuatro(self):
        """Sin mínimo de compra, entrega por viaje y factura en todas las compras (dueño, 2026-11-08), en la sección de
        entrega y en una pregunta frecuente de las cuatro páginas."""
        self.assertEqual(datos.CONDICIONES_MATERIALES, "Sin mínimo de compra. La entrega a domicilio se cobra por viaje, "
                                                       "según tu colonia. Todas las compras se pueden facturar.")
        for ruta in MATERIALES:
            texto = visible_y_ld(html_de(ruta))
            with self.subTest(ruta=ruta):
                for frase in (datos.SIN_MINIMO, datos.ENTREGA_COBRO, datos.FACTURACION):
                    self.assertIn(frase, texto)
                self.assertIn(datos.CONDICIONES_MATERIALES, texto)

    def test_opiniones_confirmadas_sin_calificacion(self):
        """Ricardo O. y Laura P. (tierra negra) y Patricia H. y David M. (piedra bola) vuelven textuales, con permiso del
        dueño (2026-11-08); solo texto visible: sin estrellas, aggregateRating ni Review en el JSON-LD."""
        for ruta, opiniones in (("/tierra-negra-vegetal-tampico", datos.OPINIONES_TIERRA_NEGRA),
                                ("/piedra-bola-rio-tampico", datos.OPINIONES_PIEDRA_BOLA)):
            html = html_de(ruta)
            ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
            texto = paridad.texto(paridad.principal(html))
            with self.subTest(ruta=ruta):
                for cita, nombre, detalle in opiniones:
                    self.assertIn(f"“{cita}”", texto)
                    self.assertIn(f"{nombre} {detalle}", texto)
                self.assertNotRegex(ld, r"Review|Rating|ratingValue")
                self.assertNotIn("ic-star", html)
        for ruta in ("/tezontle-rojo-tampico", "/marmol-blanco-tampico"):
            with self.subTest(ruta=ruta):
                self.assertNotIn("vt-testimonios", html_de(ruta))

    def test_marmol_a_250_con_las_palabras_del_dueno(self):
        """$250 el saco, IVA incluido y "sujeto a disponibilidad" junto al precio; Offer de 250 MXN con seller #negocio
        y sin InStock; el título, la descripción y las tarjetas sociales con el $250 como main."""
        html = html_de("/marmol-blanco-tampico")
        # SEO fase 0 (2026-11-10): título de 60 o menos con la marca; el $250 sigue en título, descripción y tarjetas.
        self.assertIn("<title>Mármol Blanco para Jardín Tampico: Saco $250 | Viveros Terra</title>", html)
        for clave in ("description", "og:title", "og:description", "twitter:title", "twitter:description"):
            with self.subTest(clave=clave):
                self.assertRegex(html, rf'(?:name|property)="{clave}" content="[^"]*\$250')
        texto = paridad.texto(paridad.principal(html))
        self.assertIn(f"$250 el saco, {datos.MARMOL_CONDICION}", texto)
        grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
        producto = next(n for n in grafo if n["@type"] == "Product")
        oferta = producto["offers"]
        self.assertEqual((oferta["price"], oferta["priceCurrency"]), (250, "MXN"))
        self.assertEqual(oferta["priceSpecification"]["price"], 250)
        self.assertEqual(oferta["seller"], {"@id": f"{datos.SITIO}/#negocio"})
        self.assertEqual(oferta["description"], datos.MARMOL_CONDICION)
        self.assertNotIn("availability", oferta)

    def test_tierra_negra_con_preparada_y_camiones(self):
        """Tierra preparada $100 y camiones de 5, 8 y 14 m³ en la tabla y en el JSON-LD (un Offer por presentación con
        su UnitPriceSpecification); nunca el "camión desde $5,000" de main."""
        html = html_de("/tierra-negra-vegetal-tampico")
        texto = visible_y_ld(html)
        self.assertNotIn("$5,000", texto)
        grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))["@graph"]
        ofertas = next(n for n in grafo if n["@type"] == "Product")["offers"]
        self.assertEqual(sorted(o["priceSpecification"]["price"] for o in ofertas), [90, 100, 1500, 3500, 5200, 8000])
        self.assertTrue(all("availability" not in o and o["seller"] == {"@id": f"{datos.SITIO}/#negocio"}
                            for o in ofertas))
        for m3, precio in datos.TIERRA_CAMIONES:
            self.assertIn(f"Camión volteo de {m3} m³", texto)
            self.assertIn(dinero(precio), texto)

    def test_las_reglas_detectan_lo_que_deben(self):
        for frase in ("Cotización gratis", "availability InStock", "Entrega inmediata", "el mejor", "+500 jardines",
                      '"aggregateRating"', "En nuestro vivero", "Disponible en cantidad sin límite", "más vendido",
                      "Precio según disponibilidad", "camión desde $5,000"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        for frase in ("Recoger o a domicilio, sin mínimo", "Desde 1 m³, entregada", "A partir de 1 m³",
                      "piedra lavada y calibrada", "Saco de red ≈ 20 kg"):
            with self.subTest(frase=frase):
                self.assertTrue(any(re.search(patron, frase, re.I) for _r, patron in SIN_VERIFICAR))
        self.assertTrue(SIN_PRECIO_RE.search("Piedra bola $350"))
        self.assertTrue(SIN_PRECIO_TEZONTLE_RE.search("Camión 14 m³ $3,200"))
        self.assertTrue(MEDIDAS_PIEDRA_RE.search("Chica, mediana y grande"))
        self.assertTrue(PESO_COSTAL_RE.search("Costal de 25–30 kg"))
        self.assertTrue(PESO_COSTAL_RE.search("Costal ≈ 20 kg"))
        self.assertFalse(PESO_COSTAL_RE.search("120 a 150 kg por m²"))
        limpio = MARMOL_CONDICION_RE.sub(" ", f"$250 el saco, {datos.MARMOL_CONDICION}.")
        self.assertFalse(any(re.search(patron, limpio, re.I) for _r, patron in SIN_VERIFICAR))
        self.assertFalse(any(re.search(patron, "desde 2007 · 15 a 20 días de arraigo", re.I) for _r, patron in SIN_VERIFICAR))


    def test_guia_del_marmol_con_la_regla_de_la_calculadora(self):
        """La guía rápida y los usos dicen los mismos sacos por m² que calcula la calculadora (3 hasta 4 cm, 4 con 5 cm
        y 5 con 6 cm)."""
        import componentes_materiales as cm
        from contenido import marmol_blanco as mb
        guia = next(t for t in mb.CONTENIDO["precio"]["tablas"] if t["titulo"].startswith("Guía"))
        for _uso, capa, sacos in guia["filas"]:
            with self.subTest(capa=capa):
                self.assertEqual(sacos, f"{cm.calculo('marmol', 1, int(capa.split()[0]))['por_m2']} sacos")
        self.assertEqual([f["nombre"] for f in mb.CONTENIDO["precio"]["filas"]], ["Saco de mármol blanco"])

    def test_medidas_de_una_sola_fuente(self):
        """La piedra de río va "a granel" en su página y en las comparativas del tezontle y el mármol (sin medidas, dueño
        2026-11-08), y la capa contra maleza del tezontle es la de la calculadora (6 a 8 cm) en la tarjeta de uso y en
        la pregunta."""
        tezontle, marmol, piedra = (html_de(r) for r in ("/tezontle-rojo-tampico", "/marmol-blanco-tampico",
                                                         "/piedra-bola-rio-tampico"))
        self.assertIn("A granel", paridad.texto(paridad.principal(tezontle)))
        self.assertIn("A granel, según cotización", paridad.texto(paridad.principal(marmol)))
        for html in (tezontle, marmol, piedra):
            for viejo in ("tres medidas", "2 a 20 cm", "6 a 12 cm", "12 a 20 cm", "5 a 15 cm"):
                self.assertNotIn(viejo, html)
        self.assertNotIn("5 a 8 cm de capa", tezontle)
        self.assertIn("De 6 a 8 cm para control de maleza", tezontle)
        self.assertIn("a granel", paridad.texto(paridad.principal(piedra)))


if __name__ == "__main__":
    unittest.main()
