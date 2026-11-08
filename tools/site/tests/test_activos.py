import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pub = Path(tmp.name) / "public"
        (self.pub / "css").mkdir(parents=True)
        (self.pub / "js").mkdir()
        (self.pub / "blog").mkdir()
        self.registro = Path(tmp.name) / "activos.json"
        self.escribir(".vt-a{}")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "css" / "terra-tienda.css").write_text(".vt-tienda .vt-x{}", encoding="utf-8")
        (self.pub / "css" / "terra-plantas.css").write_text(".vt-plantas .vt-x{}", encoding="utf-8")
        (self.pub / "css" / "terra-materiales.css").write_text(".vt-materiales .vt-x{}", encoding="utf-8")
        (self.pub / "css" / "terra-precios.css").write_text(".vt-precios .vt-x{}", encoding="utf-8")
        (self.pub / "css" / "terra-util.css").write_text(".vt-util .vt-x{}", encoding="utf-8")
        (self.pub / "css" / "terra-blog.css").write_text(".vt-blog .vt-x{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def escribir(self, css):
        (self.pub / "css" / "terra.css").write_text(css, encoding="utf-8")

    def publicar(self):
        return activos.publicar(self.pub, self.registro)

    def copias(self):
        return sorted(p.name for p in (self.pub / "css").glob("terra.*.css"))

    def copia(self, nombre, mtime=1_000_000_000):
        path = self.pub / "css" / nombre
        path.write_text("viejo", encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    def pagina_enlaza(self, nombre):
        """Simula el HTML publicado antes del build (sin git, publicar lo lee de disco)."""
        (self.pub / "index.html").write_text(f'<link rel="stylesheet" href="/css/{nombre}">', encoding="utf-8")

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_la_fuente(self):
        urls = self.publicar()
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}\n")
        self.assertTrue((self.pub / "css" / "terra.css").exists())

    def test_conserva_la_que_enlazan_las_paginas_aunque_sea_la_mas_vieja(self):
        # El caso del deploy del 2026-11-07: la copia servida tenía el mtime más viejo y se borró.
        servida = self.copia("terra.3eaa08fd32.css", mtime=1_000_000_000)
        reciente = self.copia("terra.73fd9d1d2c.css", mtime=2_000_000_000)
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.assertTrue(servida.exists())
        self.assertFalse(reciente.exists())
        self.assertEqual(self.copias(), sorted([servida.name, Path(urls["terra.css"]).name]))
        self.assertEqual(json.loads(self.registro.read_text(encoding="utf-8"))["terra.css"],
                         [urls["terra.css"], f"/css/{servida.name}"])

    def test_segunda_corrida_no_borra_la_servida(self):
        # Tras la primera corrida las páginas ya enlazan la copia nueva: el registro recuerda la servida.
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.pagina_enlaza(Path(urls["terra.css"]).name)
        registro = self.registro.read_text(encoding="utf-8")
        self.assertEqual(self.publicar(), urls)
        self.assertTrue(servida.exists())
        self.assertEqual(self.registro.read_text(encoding="utf-8"), registro)

    def test_varios_cambios_en_la_rama_siguen_guardando_la_de_produccion(self):
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        self.publicar()
        self.escribir(".vt-b{}")
        segunda = self.publicar()["terra.css"]
        self.escribir(".vt-c{}")
        tercera = self.publicar()["terra.css"]
        self.assertEqual(self.copias(), sorted([servida.name, Path(tercera).name]))
        self.assertFalse((self.pub / segunda.lstrip("/")).exists())

    def test_sin_registro_ni_paginas_deja_solo_la_actual(self):
        self.copia("terra.0000000000.css")
        urls = self.publicar()
        self.assertEqual(self.copias(), [Path(urls["terra.css"]).name])

    def test_no_toca_archivos_que_no_son_copias(self):
        ajeno = self.pub / "css" / "terra.min.css"
        ajeno.write_text("x", encoding="utf-8")
        self.publicar()
        self.assertTrue(ajeno.exists())

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_mismo_contenido_mismo_hash(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.escribir(".vt-a{}")
        self.assertEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_css_publicado_sin_comentarios_ni_sangria_y_con_las_mismas_reglas(self):
        css = "/* nota */\n.vt-a{\n  content:\"a  b\";\n  margin:0 auto}\n\n@media (min-width:768px){\n  .vt-b{x:y}\n}\n"
        self.assertEqual(activos.minificar_css(css),
                         '.vt-a{\ncontent:"a  b";\nmargin:0 auto}\n@media (min-width:768px){\n.vt-b{x:y}\n}\n')

        def colapsado(texto):
            """Todo el texto sin comentarios y con los espacios en blanco reducidos a uno: selectores y declaraciones."""
            return " ".join(re.sub(r"/\*.*?\*/", "", texto, flags=re.S).split())
        for hoja in ("terra.css", "terra-tienda.css", "terra-plantas.css", "terra-materiales.css", "terra-precios.css", "terra-blog.css"):
            fuente = (activos.PUBLIC / "css" / hoja).read_text(encoding="utf-8")
            with self.subTest(hoja=hoja):
                self.assertEqual(colapsado(activos.minificar_css(fuente)), colapsado(fuente))

    def test_lee_el_html_de_origin_main_antes_que_main_y_head(self):
        raiz = self.pub.parent

        def git(*args):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=raiz, check=True,
                           capture_output=True)

        def commit(enlace):
            (self.pub / "index.html").write_text(f'<link href="/css/{enlace}">', encoding="utf-8")
            git("add", "public/index.html")
            git("commit", "-q", "-m", enlace)

        git("init", "-q", "-b", "main")
        (self.pub / "blog" / "index.html").write_text("<p>blog</p>", encoding="utf-8")
        git("add", "public/blog/index.html")
        commit("terra.1111111111.css")
        git("update-ref", "refs/remotes/origin/main", "HEAD")  # producción
        commit("terra.2222222222.css")  # main local adelantado
        git("checkout", "-q", "-b", "rama")
        commit("terra.3333333333.css")  # HEAD de la rama
        (self.pub / "index.html").write_text('<link href="/css/terra.4444444444.css">', encoding="utf-8")  # disco
        self.assertEqual(activos.servida("css/terra.css", activos._html_de_main(self.pub)), "/css/terra.1111111111.css")
        git("update-ref", "-d", "refs/remotes/origin/main")
        self.assertEqual(activos.servida("css/terra.css", activos._html_de_main(self.pub)), "/css/terra.2222222222.css")
        git("branch", "-D", "main")
        self.assertEqual(activos.servida("css/terra.css", activos._html_de_main(self.pub)), "/css/terra.3333333333.css")

    def test_registro_del_repo_coincide_con_lo_publicado(self):
        registro = json.loads(activos.REGISTRO.read_text(encoding="utf-8"))
        urls = activos.urls()
        for clave, rel in activos.FUENTES.items():
            with self.subTest(asset=clave):
                self.assertEqual(registro[clave][0], urls[clave])
                for url in registro[clave]:
                    self.assertTrue((activos.PUBLIC / url.lstrip("/")).is_file(), url)
                copias = {"/" + p.relative_to(activos.PUBLIC).as_posix()
                          for p in (activos.PUBLIC / rel).parent.glob(f"{Path(rel).stem}.*{Path(rel).suffix}")
                          if activos._patron(rel).fullmatch("/" + p.relative_to(activos.PUBLIC).as_posix())}
                self.assertEqual(copias, set(registro[clave]))


if __name__ == "__main__":
    unittest.main()
