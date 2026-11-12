"""Paridad de los 52 artículos del blog (Etapa 2h): el texto es el publicado, palabra por palabra, salvo las correcciones
documentadas en contenido/blog_correcciones.py; las fotos son las mismas y en el mismo orden."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402
import paridad_blog  # noqa: E402
import paridad_materiales  # noqa: E402
from contenido import articulo, blog_correcciones as bc  # noqa: E402


def html_de(slug):
    return paridad.archivo(f"/blog/{slug}").read_text(encoding="utf-8")


def permitido_borrar(doc):
    partes = list(doc["retirado"]) + [doc["kicker"], doc["h1"], doc["dek"], doc["relacionados_titulo"]]
    partes += [" ".join((r["categoria"], r["titulo"], r["texto"])) for r in doc["relacionados"]]
    return paridad.texto(" ".join(partes))


class BlogParidadTest(unittest.TestCase):
    def test_son_49_articulos(self):
        # 54 hasta la SEO fase 2c: seis salen con 301 y entra la lista única de palmas (articulo.NUEVOS).
        self.assertEqual(len(articulo.CLAVES), 49)
        self.assertEqual(len(articulo.CLAVES) - len(articulo.NUEVOS), len(list(paridad_blog.DIR_TEXTO.glob("*.txt"))))

    def test_nada_se_agrega_al_texto_del_articulo(self):
        for slug in (s for s in articulo.CLAVES if s not in articulo.NUEVOS):
            viejo = paridad_blog.viejo_corregido(slug, bc.de(slug) + bc.TODOS)
            insertado, _borrado = paridad_blog.diferencias(viejo, paridad_blog.cuerpo_nuevo(html_de(slug)))
            with self.subTest(slug=slug):
                self.assertEqual(insertado, [])

    def test_lo_que_se_borra_es_la_envoltura(self):
        """Solo salen el índice, los CTA y la barra lateral anteriores (anotados por la extracción) y la portada, que la
        plantilla vuelve a poner."""
        for slug in (s for s in articulo.CLAVES if s not in articulo.NUEVOS):
            doc, _cuerpo = articulo.leer(slug)
            viejo = paridad_blog.viejo_corregido(slug, bc.de(slug) + bc.TODOS)
            _ins, borrado = paridad_blog.diferencias(viejo, paridad_blog.cuerpo_nuevo(html_de(slug)))
            permitido = " ".join(paridad.texto(" ".join(doc["retirado"])).split() + permitido_borrar(doc).split())
            ajenos = [b for b in borrado if not all(p in permitido for p in b.split())]
            with self.subTest(slug=slug):
                self.assertEqual(ajenos, [])

    def test_mismas_fotos_en_el_mismo_orden(self):
        captura = json.loads(paridad_blog.FOTOS.read_text(encoding="utf-8"))
        for ruta, viejas in captura.items():
            if ruta.removeprefix("/blog/") in articulo.NUEVOS:
                continue
            nuevas = paridad_materiales.fotos(paridad.archivo(ruta).read_text(encoding="utf-8"))
            portada = articulo.PORTADAS.get(ruta.removeprefix("/blog/"))
            with self.subTest(ruta=ruta):
                if portada:  # plan visual V4: la portada (la foto de su tarjeta del índice) va antes de las de la captura
                    self.assertEqual(nuevas[0]["src"], portada["src"])
                    nuevas = nuevas[1:]
                self.assertEqual([re.sub(r"^(\.\./)+", "/", f["src"]) for f in viejas], [f["src"] for f in nuevas])

    def test_cada_correccion_tiene_motivo(self):
        for slug, lista in bc.CORRECCIONES.items():
            for viejo, _nuevo, motivo in lista:
                with self.subTest(slug=slug, viejo=viejo[:40]):
                    self.assertGreater(len(motivo), 20)


if __name__ == "__main__":
    unittest.main()
