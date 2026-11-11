"""Movimiento del sitio (spec del hero, 2026-11-09, §8; desde la Entrega C de experiencia, 2026-11-10, el balanceo de la
etiqueta y el revelado por scroll son de todas las plantillas y viven en terra.css; la foto que se descubre sigue solo en
la home) en terra.css, terra-inicio.css, terra-temporada.css y terra-blog.css: solo transform,
opacity y clip-path; toda animación dentro de prefers-reduced-motion:no-preference; una vez y de 900 ms o menos; sin
will-change ni bucles; el balanceo y la foto solo desde 1024 px; el revelado por scroll bajo @supports y nunca sobre
el titular, el lede, los precios, el Medidor ni los botones; los hovers con transform solo donde hay hover."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_terra_css import sin_comentarios  # noqa: E402

CSS = Path(__file__).resolve().parents[3] / "public" / "css"
HOJAS = ("terra.css", "terra-inicio.css", "terra-temporada.css", "terra-blog.css")
PERMITIDAS = {"transform", "opacity", "clip-path"}
SIN_MOVIMIENTO = "@media (prefers-reduced-motion:no-preference)"
INTOCABLES = re.compile(r"h1|vt-lede|precio|etiqueta|medidor|vt-btn|vt-cta|vt-(?:inicio|portada)__(?:cta|trato|lema|titulo)|vt-tabla")


def reglas(css):
    """[(contextos, selector, cuerpo)] de una hoja: contextos son los @media/@supports/@keyframes que envuelven."""
    salida, pila, i, css = [], [], 0, sin_comentarios(css)
    while i < len(css):
        abre, cierra = css.find("{", i), css.find("}", i)
        if cierra != -1 and (abre == -1 or cierra < abre):
            pila.pop()
            i = cierra + 1
            continue
        if abre == -1:
            break
        cabeza = css[i:abre].strip()
        if cabeza.startswith("@"):
            pila.append(cabeza)
            i = abre + 1
            continue
        fin = css.index("}", abre)
        salida.append((tuple(pila), cabeza, css[abre + 1:fin]))
        i = fin + 1
    return salida


def declaraciones(cuerpo):
    return dict(d.split(":", 1) for d in cuerpo.split(";") if ":" in d)


class MovimientoCssTest(unittest.TestCase):
    def setUp(self):
        self.hojas = {n: reglas((CSS / n).read_text(encoding="utf-8")) for n in HOJAS}
        self.todas = [(n, *r) for n, rs in self.hojas.items() for r in rs]

    def test_el_analizador_ve_contextos_anidados(self):
        r = reglas("@media (a){@supports (b){.x{c:d}}.y{e:f}}@keyframes k{from{opacity:0}to{opacity:1}}.z{g:h}")
        self.assertEqual(r, [(("@media (a)", "@supports (b)"), ".x", "c:d"), (("@media (a)",), ".y", "e:f"),
                             (("@keyframes k",), "from", "opacity:0"), (("@keyframes k",), "to", "opacity:1"),
                             ((), ".z", "g:h")])

    def test_keyframes_solo_con_transform_opacity_y_clip_path(self):
        cuadros = [(n, ctx, cuerpo) for n, ctx, _sel, cuerpo in self.todas if any(c.startswith("@keyframes") for c in ctx)]
        self.assertTrue(cuadros, "la home tiene animaciones")
        for hoja, ctx, cuerpo in cuadros:
            with self.subTest(hoja=hoja, keyframes=ctx[-1]):
                self.assertLessEqual(set(declaraciones(cuerpo)), PERMITIDAS)

    def test_toda_animacion_dentro_de_no_preference_una_vez_y_de_900_ms_o_menos(self):
        animadas = [(n, ctx, sel, declaraciones(cuerpo)) for n, ctx, sel, cuerpo in self.todas
                    if re.search(r"(?:^|;)animation", cuerpo)]
        self.assertTrue(animadas)
        for hoja, ctx, sel, d in animadas:
            with self.subTest(hoja=hoja, selector=sel):
                self.assertIn(SIN_MOVIMIENTO, ctx)
                valor = d.get("animation", "")
                self.assertNotIn("infinite", valor)
                self.assertNotIn("alternate", valor)
                if "animation-timeline" in d:  # por scroll: no tiene duración, avanza con la página
                    self.assertTrue(any(c.startswith("@supports (animation-timeline:view())") for c in ctx))
                    self.assertEqual(d["animation-timeline"], "view()")
                else:
                    segundos = [float(s) for s in re.findall(r"(?<![\w.])(\d*\.?\d+)s\b", valor)]
                    self.assertTrue(segundos and sum(segundos) <= 0.9, valor)
        for hoja, _ctx, sel, cuerpo in self.todas:
            with self.subTest(hoja=hoja, selector=sel):
                self.assertNotIn("will-change", cuerpo)

    def test_balanceo_de_la_etiqueta_y_foto_solo_desde_1024(self):
        """Entrega C: el balanceo es de toda portada con etiqueta colgada (no la de sin foto, que no lleva el
        translateY); la foto que se descubre, solo en la home."""
        for hoja, nombre, selector in (
                ("terra.css", "vt-balanceo", ".vt-pagina .vt-portada:not(.vt-portada--sinfoto) .vt-etiqueta-x"),
                ("terra-inicio.css", "vt-inicio-foto", ".vt-inicio .vt-portada__foto .vt-fig__marco")):
            usos = [(ctx, sel, cuerpo) for n, ctx, sel, cuerpo in self.todas if f"animation:{nombre} " in cuerpo]
            with self.subTest(animacion=nombre):
                self.assertEqual([sel for _c, sel, _b in usos], [selector])
                self.assertIn("@media (min-width:1024px)", usos[0][0])
                self.assertTrue(any(f"animation:{nombre} " in c for _x, s_, c in self.hojas[hoja] if s_ == selector))
        balanceo = [cuerpo for _n, ctx, _sel, cuerpo in self.todas if ctx == ("@keyframes vt-balanceo",)]
        self.assertEqual(re.findall(r"rotate\((-?[\d.]+)deg\)", "".join(balanceo)), ["4", "-2", ".8"])
        self.assertTrue(all("opacity" not in c for c in balanceo), "el precio se lee desde el primer cuadro")
        origen = next(cuerpo for _n, _c, sel, cuerpo in self.todas if "animation:vt-balanceo " in cuerpo)
        self.assertIn("transform-origin:50% -40px", origen)  # donde nace el cordel
        foto = "".join(cuerpo for _n, ctx, _sel, cuerpo in self.todas if ctx == ("@keyframes vt-inicio-foto",))
        self.assertIn("clip-path", foto)
        self.assertNotIn("opacity", foto)

    def test_revelado_por_scroll_solo_en_encabezados_y_figuras(self):
        revelados = [(sel, cuerpo) for _n, ctx, sel, cuerpo in self.todas if "animation-timeline" in cuerpo]
        self.assertEqual(sorted(sel for sel, _c in revelados),
                         [".vt-pagina main :is(.vt-bloque,.vt-art__cuerpo) h2:not(.vt-art__respuesta-t)",
                          ".vt-pagina main :is(.vt-obras,.vt-mosaico,.vt-nb-galeria) .vt-fig__marco"])
        for selector, _cuerpo in revelados:
            self.assertIsNone(INTOCABLES.search(selector))
        # Las fotos parten de opacity .25 (se anima el marco: el pie conserva su contraste). Los encabezados parten de
        # .6 y no de .25: axe revisa también lo que aún no entra en pantalla, y a .25 un h2 no cumple 3:1 (Lighthouse
        # bajaba accesibilidad de 100 a 97). A .6 la tinta sobre hueso queda arriba de 3:1.
        for nombre, opacidad in (("vt-sube", ".25"), ("vt-titulo", ".6")):
            cuadros = "".join(c for _n, ctx, _s, c in self.todas if ctx == (f"@keyframes {nombre}",))
            with self.subTest(keyframes=nombre):
                self.assertIn(f"opacity:{opacidad}", cuadros)
                self.assertIn("translateY(16px)", cuadros)
        self.assertIn("animation:vt-titulo ", next(c for s, c in revelados if " h2" in s))

    def test_la_home_ya_no_repite_lo_que_es_de_todo_el_sitio(self):
        inicio = (CSS / "terra-inicio.css").read_text(encoding="utf-8")
        for nombre in ("vt-inicio-balanceo", "vt-inicio-titulo", "vt-inicio-sube", "animation-timeline"):
            self.assertNotIn(nombre, sin_comentarios(inicio))

    def test_nada_anima_la_opacidad_del_titular_el_lede_el_precio_ni_el_cta(self):
        """Medido: la opacidad sobre el contenido de la primera pantalla retrasa el LCP móvil 300 ms."""
        con_opacidad = {ctx[-1].split()[1] for _n, ctx, _s, cuerpo in self.todas
                        if ctx and ctx[-1].startswith("@keyframes") and "opacity" in cuerpo}
        for hoja, _ctx, sel, cuerpo in self.todas:
            usa = re.search(r"animation:([\w-]+)", cuerpo)
            if usa and usa.group(1) in con_opacidad:
                with self.subTest(hoja=hoja, selector=sel):
                    self.assertIsNone(INTOCABLES.search(sel))

    def test_hovers_con_transform_solo_donde_hay_hover(self):
        for hoja, ctx, sel, cuerpo in self.todas:
            if ":hover" in sel and "transform:" in cuerpo and "transform:none" not in cuerpo:
                with self.subTest(hoja=hoja, selector=sel):
                    self.assertIn("@media (hover:hover)", ctx)


if __name__ == "__main__":
    unittest.main()
