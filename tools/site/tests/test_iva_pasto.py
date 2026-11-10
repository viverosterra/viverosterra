"""Regla permanente del dueño (2026-11-09/10): el pasto natural sin instalar no lleva IVA. "Con IVA" o "IVA incluido"
solo puede acompañar al pasto instalado (que ya lo incluye); nunca al precio de solo pasto ni al de mayoreo.

Se revisan todas las páginas del sitio (desde la fase 0 de SEO, 2026-11-10; antes solo la home, las páginas de pasto
natural y la lista de precios). Además, ningún H1 ni título dice "con IVA" (cubriría toda la página) y el menú y el pie,
que salen en todas las páginas, tampoco: el IVA se explica junto a cada precio. En cada bloque que
menciona el precio de solo pasto o el de mayoreo (un párrafo, un renglón de lista, una etiqueta de precio completa, una
tabla con su leyenda, una respuesta del JSON-LD, una meta o un mensaje de WhatsApp), cada "con IVA" debe estar amarrado
al instalado: lo último que se nombró antes, dentro de su misma frase o renglón, es el instalado o un precio que no es
de pasto sin instalar. Si lo último es el precio de solo pasto o de mayoreo, o si no hay nada antes (un "Con IVA" suelto
que cubre todo el bloque), es una falta. La forma negativa ("no lleva IVA") siempre se permite. Los precios salen de
datos.PRECIOS: nada va escrito a mano. Los textos que arma el JavaScript (Medidor y cotizador por volumen) se revisan en
sus casos de paridad."""
import html as html_mod
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402
import shell  # noqa: E402

PUBLIC = paginas.PUBLIC
PAGINAS = tuple(sorted(str(p.relative_to(PUBLIC)) for p in shell.paginas_html()))
PASTO_BLOG = ("cuando-plantar-pasto-tampico-calendario", "pasto-san-agustin-instalacion-mantenimiento",
              "pasto-san-agustin-vs-japones")
P = datos.PRECIOS
SIN_IVA = tuple(str(P[k]) for k in ("pasto_solo_m2", "pasto_mayoreo_m2"))
PRECIO_RE = re.compile(r"\$\s?(\d[\d,]*)")
POSITIVO_RE = re.compile(r"\bcon IVA\b|\bIVA incluido\b|\bincluyen?\s+(?:el\s+)?IVA\b|\bm[aá]s IVA\b", re.I)
INSTALADO_RE = re.compile(r"instalad\w*|con instalaci[oó]n", re.I)
FRASE_RE = re.compile(r"(?<=[.!?:;])\s+|\n")
CASOS = PUBLIC / "js" / "tests"


def plano(fragmento):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def con_precio_sin_iva(texto):
    return any(m.group(1) in SIN_IVA for m in PRECIO_RE.finditer(texto))


def faltas(piezas):
    """Frases de un bloque donde un "con IVA" queda amarrado al pasto sin instalar o suelto. `piezas` son los renglones
    del bloque; cada uno se parte en frases. Un bloque sin precio de solo pasto ni de mayoreo no se revisa."""
    if not con_precio_sin_iva(" ".join(piezas)):
        return []
    malas = []
    for pieza in piezas:
        for frase in FRASE_RE.split(pieza):
            for m in POSITIVO_RE.finditer(frase):
                antes = frase[:m.start()]
                marcas = [(x.start(), x.group(1) not in SIN_IVA) for x in PRECIO_RE.finditer(antes)]
                marcas += [(x.start(), True) for x in INSTALADO_RE.finditer(antes)]
                if not marcas or not max(marcas)[1]:
                    malas.append(frase.strip())
    return malas


def _cadenas(nodo):
    if isinstance(nodo, str):
        yield nodo
    elif isinstance(nodo, dict):
        for valor in nodo.values():
            yield from _cadenas(valor)
    elif isinstance(nodo, list):
        for valor in nodo:
            yield from _cadenas(valor)


def bloques(html):
    """Bloques de una página: [(nombre, [piezas de texto])]."""
    salida = []
    for contenido in re.findall(r'<meta (?:name|property)="[^"]*description" content="([^"]*)"', html):
        salida.append(("meta", [html_mod.unescape(contenido)]))
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        salida += [("json-ld", [texto]) for texto in _cadenas(json.loads(bloque))]
    for texto in re.findall(r'https://wa\.me/\d+\?text=([^"\'&\s<]*)', html):
        salida.append(("whatsapp", unquote(texto).split("\n")))
    cuerpo = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S).group(1)
    cuerpo = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", cuerpo, flags=re.S)
    for etiqueta in re.findall(r'<div class="vt-etiqueta(?: [^"]*)?"[^>]*>(.*?)</div>', cuerpo, re.S):
        salida.append(("etiqueta", [plano(p) for p in re.findall(r"<p\b[^>]*>(.*?)</p>", etiqueta, re.S)]))
    for tabla in re.findall(r"<table\b.*?</table>", cuerpo, re.S):
        salida.append(("tabla", [plano(x) for x in re.findall(r"<(?:caption|tr)\b[^>]*>(.*?)</(?:caption|tr)>", tabla, re.S)]))
    for _nombre, texto in re.findall(r"<(p|li|dd|summary|figcaption|h[1-6])\b[^>]*>(.*?)</\1>", cuerpo, re.S):
        salida.append(("texto", [plano(texto)]))
    return salida


class IvaDelPastoTest(unittest.TestCase):
    maxDiff = None

    def test_con_iva_nunca_acompana_al_pasto_sin_instalar(self):
        hallazgos = []
        for pagina in PAGINAS:
            for nombre, piezas in bloques((PUBLIC / pagina).read_text(encoding="utf-8")):
                hallazgos += [f"{pagina} · {nombre} · {frase[:160]}" for frase in faltas(piezas)]
        self.assertEqual(sorted(set(hallazgos)), [])

    def test_se_revisa_todo_el_sitio(self):
        self.assertGreater(len(PAGINAS), 100)
        for pagina in ("index.html", "precios/index.html", *(f"blog/{slug}/index.html" for slug in PASTO_BLOG)):
            self.assertIn(pagina, PAGINAS)

    def test_ningun_h1_ni_titulo_dice_con_iva(self):
        """Un "con IVA" en el H1 o en el <title> cubre toda la página, y casi todas citan algún precio que no lo lleva
        (pasto solo, mayoreo, plantas). El H1 de /precios decía "2026, con IVA"."""
        hallazgos = []
        for pagina in PAGINAS:
            html = (PUBLIC / pagina).read_text(encoding="utf-8")
            for etiqueta, texto in re.findall(r"<(h1|title)\b[^>]*>(.*?)</\1>", html, re.S):
                if POSITIVO_RE.search(plano(texto)):
                    hallazgos.append(f"{pagina} · {etiqueta} · {plano(texto)}")
        self.assertEqual(hallazgos, [])
        self.assertIn(f"Precios de jardinería en Tampico {datos.ANIO}</h1>",
                      re.sub(r"</?span[^>]*>", "", (PUBLIC / "precios/index.html").read_text(encoding="utf-8")))

    def test_el_menu_y_el_pie_no_dicen_con_iva(self):
        """El shell sale en todas las páginas: "Precios 2026 con IVA incluido" en el pie y "con IVA" junto a "Precios"
        en el menú de celular cubrían también el pasto sin instalar."""
        for ruta in ("/", "/precios", "/pasto-en-rollo-tampico", "/blog", "/pasto-sintetico", datos.NOCHEBUENAS["ruta"]):
            ctx = paginas.contexto(ruta)
            with self.subTest(ruta=ruta):
                self.assertIsNone(POSITIVO_RE.search(plano(partials.header(ctx))))
                self.assertIsNone(POSITIVO_RE.search(plano(partials.footer(ctx))))
        hallazgos = []
        for pagina in PAGINAS:
            html = (PUBLIC / pagina).read_text(encoding="utf-8")
            fuera = re.sub(r"<main\b.*</main>", " ", html, flags=re.S)
            fuera = re.sub(r"<(script|style|svg|head)\b.*?</\1>", " ", fuera, flags=re.S)
            if POSITIVO_RE.search(plano(fuera)):
                hallazgos.append(pagina)
        self.assertEqual(hallazgos, [])
        self.assertIn(f"Precios {datos.ANIO}</p>", partials.footer(paginas.contexto("/")))
        self.assertIn('href="/precios">Precios</a>', partials.header(paginas.contexto("/")))

    def test_etiqueta_de_los_articulos_de_pasto_como_en_la_home(self):
        """"Producto relacionado · Con IVA" cubría también el renglón "Solo el pasto $85": el IVA va, como en la
        home, solo en el renglón del instalado."""
        for slug in PASTO_BLOG:
            html = (PUBLIC / "blog" / slug / "index.html").read_text(encoding="utf-8")
            etiqueta = re.search(r'<div class="vt-etiqueta">(.*?)</div>', html, re.S).group(1)
            piezas = [plano(p) for p in re.findall(r"<p\b[^>]*>(.*?)</p>", etiqueta, re.S)]
            with self.subTest(slug=slug):
                self.assertEqual(faltas(piezas), [])
                self.assertIsNone(POSITIVO_RE.search(piezas[0]), piezas[0])
                self.assertIn(f"Instalado · desde ${P['pasto_instalado_m2']} /m² con IVA", piezas)
                self.assertIn(f"Solo el pasto ${P['pasto_solo_m2']} /m²", piezas)

    def test_llms_txt(self):
        lineas = (PUBLIC / "llms.txt").read_text(encoding="utf-8").split("\n")
        self.assertEqual([frase for linea in lineas for frase in faltas([linea])], [])
        encabezados = [linea for linea in lineas if linea.startswith("#") and POSITIVO_RE.search(linea)]
        self.assertEqual(encabezados, [], "un encabezado «IVA incluido» cubriría también el pasto sin instalar")

    def test_la_respuesta_oficial_del_precio_del_pasto(self):
        r = datos.RESPUESTA_PRECIO_PASTO
        self.assertEqual(faltas([r]), [])
        self.assertIn(f"${P['pasto_solo_m2']} por m² solo el pasto (no lleva IVA)", r)
        self.assertIn(f"desde ${P['pasto_instalado_m2']} por m² instalado, con IVA incluido", r)
        self.assertRegex(r, rf"mayoreo cuesta desde \${P['pasto_mayoreo_m2']}/m² \([^)]*no lleva IVA\)")
        self.assertNotRegex(r, r"Precios \d{4}, con IVA")

    def test_el_medidor_solo_dice_con_iva_en_modo_instalado(self):
        """Etiqueta, texto del cálculo, plan de mensualidades, renglón vivo y mensaje de WhatsApp, en Python; los mismos
        casos corren contra vt-medidor.js (paridad). El mayoreo que no llega al mínimo cae a solo pasto: tampoco."""
        casos = json.loads((CASOS / "casos-medidor.json").read_text(encoding="utf-8"))["casos"]
        modos = {caso["entrada"]["modo"] for caso in casos}
        self.assertEqual(modos, {"instalado", "solo", "mayoreo"})
        for caso in casos:
            e = caso["entrada"]
            r = c.calculo_medidor(e["largo"], e["ancho"], e["modo"])
            t = c.textos_medidor(e["largo"], e["ancho"], r, e["colonia"], e["plazo"])
            textos = [t[k] for k in ("medida", "calc", "plan", "mensaje", "vivo", "iva")]
            with self.subTest(entrada=e):
                self.assertEqual(t, {k: caso["esperado"][k] for k in t})
                if e["modo"] == "instalado":
                    self.assertEqual(t["iva"], "con IVA")
                    self.assertIn("con IVA", t["calc"])
                    self.assertRegex(t["mensaje"], r"Estimado de la web: desde \$[\d,]+ con IVA\n")
                else:
                    self.assertEqual(t["iva"], "")
                    self.assertEqual([x for x in textos if POSITIVO_RE.search(x)], [])
                    self.assertRegex(t["mensaje"], r"Estimado de la web: (?:desde )?\$[\d,]+ \(no lleva IVA\)\n")

    def test_el_cotizador_por_volumen_nunca_dice_con_iva(self):
        """Mayoreo y, con menos del mínimo, solo pasto: ninguno lleva IVA (Python y casos de vt-b2b.js)."""
        for m2 in (120, P["pasto_mayoreo_minimo_m2"], 1200):
            t = c.textos_volumen(c.calculo_volumen(m2), "Constructora", "Altamira", "marzo")
            with self.subTest(m2=m2):
                self.assertEqual([x for x in t.values() if POSITIVO_RE.search(x)], [])
                self.assertRegex(t["mensaje"], r"Estimado de la web: (?:desde )?\$[\d,]+ \((?:desde )?\$\d+/m²; no lleva IVA\)\n")
        self.assertIsNone(POSITIVO_RE.search(json.dumps(c.VACIO_VOLUMEN, ensure_ascii=False)))
        self.assertIsNone(POSITIVO_RE.search(plano(c.cotizador_volumen("x", "mayoreo", "Hola"))))
        self.assertIsNone(POSITIVO_RE.search((CASOS / "casos-b2b.json").read_text(encoding="utf-8")))

    def test_html_inicial_del_medidor_con_iva_solo_si_arranca_instalado(self):
        self.assertIn('<span data-vt-o="iva">con IVA</span>', c.medidor("p", "home"))
        for modo in ("solo", "mayoreo"):
            self.assertIn('<span data-vt-o="iva"></span>', c.medidor("p", "home", modo=modo))

    def test_la_regla_detecta_lo_que_debe(self):
        solo, mayoreo, instalado = (P[k] for k in ("pasto_solo_m2", "pasto_mayoreo_m2", "pasto_instalado_m2"))
        for sucio in ([f"Mayoreo desde ${mayoreo}/m² solo pasto, con IVA."],
                      [f"${solo} por m² solo el pasto y desde ${instalado} instalado. Precios 2026, con IVA, para Tampico."],
                      ["Pasto · 01 Con IVA", f"Instalado desde ${instalado} /m²", f"Solo pasto ${solo} /m²"],
                      ["Precios 2026 con IVA incluido.", f"Solo el pasto /m² ${solo}"],
                      [f"Hola, quiero cotizar solo el pasto.", f"Solo pasto a ${solo}/m², con IVA"],
                      [f"Instalado desde ${instalado}/m²; solo pasto ${solo}/m², IVA incluido."]):
            with self.subTest(sucio=sucio):
                self.assertTrue(faltas(sucio))
        for limpio in ([f"${solo} por m² solo el pasto (no lleva IVA) y desde ${instalado} por m² instalado, con IVA incluido."],
                       ["Pasto · 01 Precios 2026", f"San Agustín instalado · desde ${instalado} /m² con IVA", f"Solo pasto ${solo} /m²"],
                       ["El instalado incluye IVA; el pasto solo y el mayoreo no llevan IVA.", f"Solo el pasto /m² ${solo}"],
                       ["Precios 2026 con IVA.", "Mantenimiento desde $750/mes"],
                       [f"Mayoreo desde ${mayoreo}/m² (solo pasto; no lleva IVA)."]):
            with self.subTest(limpio=limpio):
                self.assertEqual(faltas(limpio), [])
        self.assertFalse(con_precio_sin_iva(f"${solo}0 y ${mayoreo}5 y $3{solo}"))


if __name__ == "__main__":
    unittest.main()
