"""Fotos del catálogo en local (Etapa 2e): funciones puras de fotos_catalogo.py sin red y fotos publicadas."""
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fotos_catalogo as f  # noqa: E402
from contenido import catalogo_datos as cd  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"


def webp_vp8x(ancho, alto):
    return (b"RIFF" + (22).to_bytes(4, "little") + b"WEBP" + b"VP8X" + (10).to_bytes(4, "little") + b"\x00" * 4
            + (ancho - 1).to_bytes(3, "little") + (alto - 1).to_bytes(3, "little"))


def webp_vp8l(ancho, alto):
    bits = (ancho - 1) | ((alto - 1) << 14)
    return b"RIFF" + (13).to_bytes(4, "little") + b"WEBP" + b"VP8L" + (5).to_bytes(4, "little") + b"\x2f" + bits.to_bytes(4, "little")


class FuncionesTest(unittest.TestCase):
    def test_url_de_origen_solo_con_un_id_de_drive_valido(self):
        self.assertEqual(f.url_origen("1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb"),
                         "https://lh3.googleusercontent.com/d/1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb=w1200")
        for malo in ("", "../etc/passwd", "a b", "x" * 10, None):
            with self.subTest(id=malo), self.assertRaises(ValueError):
                f.url_origen(malo)

    def test_valida_tipo_y_tamano(self):
        self.assertEqual(f.validar("image/jpeg", b"x"), b"x")
        with self.assertRaises(ValueError):
            f.validar("text/html; charset=utf-8", b"<html>")
        with self.assertRaises(ValueError):
            f.validar("image/jpeg", b"x" * (f.MAXIMO_BYTES + 1))

    def test_dimensiones_de_webp_sin_pillow(self):
        self.assertEqual(f.dimensiones_webp(webp_vp8x(480, 720)), (480, 720))
        self.assertEqual(f.dimensiones_webp(webp_vp8l(480, 640)), (480, 640))
        with self.assertRaises(ValueError):
            f.dimensiones_webp(b"\xff\xd8\xff\xe0 no es webp")

    def test_actualizar_baja_solo_lo_que_falta_y_no_muta(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            (destino / "uno-tampico.webp").write_bytes(webp_vp8x(480, 600))
            entrada = ({"slug": "uno", "drive": "1" * 33}, {"slug": "dos", "drive": "2" * 33})
            pedidas = []
            salida, nuevas = f.actualizar(entrada, destino, bajar=lambda url: pedidas.append(url) or b"jpg",
                                          convertir=lambda _b: webp_vp8x(480, 720))
            self.assertEqual(nuevas, 1)
            self.assertEqual(pedidas, ["https://lh3.googleusercontent.com/d/" + "2" * 33 + "=w1200"])
            self.assertEqual([(e["img"], e["ancho"], e["alto"]) for e in salida],
                             [("/img/catalogo/uno-tampico.webp", 480, 600), ("/img/catalogo/dos-tampico.webp", 480, 720)])
            self.assertNotIn("img", entrada[0])

    def test_actualizar_no_baja_las_retiradas_y_las_deja_sin_foto(self):
        with tempfile.TemporaryDirectory() as tmp:
            pedidas = []
            salida, nuevas = f.actualizar(({"slug": "fea", "drive": "4" * 33, "img": "/img/catalogo/fea-tampico.webp"},),
                                          Path(tmp), bajar=lambda url: pedidas.append(url) or b"jpg",
                                          convertir=lambda _b: webp_vp8x(480, 720), retiradas={"fea": "marca de agua"})
            self.assertEqual((nuevas, pedidas), (0, []))
            self.assertEqual([(e["img"], e["ancho"], e["alto"]) for e in salida], [(None, None, None)])
            self.assertFalse((Path(tmp) / "fea-tampico.webp").exists())

    def test_un_error_dice_que_especie_fallo(self):
        def falla(_url):
            raise ValueError("HTTP 404")
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(SystemExit) as error:
            f.actualizar(({"slug": "tres", "drive": "3" * 33},), Path(tmp), bajar=falla)
        self.assertIn("tres", str(error.exception))

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Pillow solo hace falta para bajar las fotos")
    def test_fondo_transparente_se_conserva(self):
        """Un PNG con fondo transparente no se aplana a negro: el WebP conserva el canal alfa."""
        from PIL import Image

        original = Image.new("RGBA", (600, 750), (0, 0, 0, 0))
        original.paste((40, 120, 40, 255), (200, 200, 400, 550))
        entrada = io.BytesIO()
        original.save(entrada, "PNG")
        with Image.open(io.BytesIO(f.a_webp(entrada.getvalue()))) as salida:
            self.assertEqual(salida.size, (480, 600))
            self.assertEqual(salida.mode, "RGBA")
            self.assertEqual(salida.getpixel((5, 5))[3], 0)
            self.assertGreater(salida.getpixel((240, 300))[3], 200)


CON_FOTO = tuple(e for e in cd.ESPECIES if e["slug"] not in cd.FOTOS_RETIRADAS)


class FotosPublicadasTest(unittest.TestCase):
    def test_cada_especie_con_su_foto_local(self):
        """480 px de ancho, salvo las fotos chicas declaradas (no se agrandan; pregunta 12 al dueño)."""
        for e in CON_FOTO:
            archivo = PUBLIC / e["img"].lstrip("/") if e["img"] else None
            with self.subTest(especie=e["slug"]):
                self.assertEqual(e["img"], f.ruta_local(e["slug"]))
                self.assertTrue(archivo.is_file())
                self.assertEqual(f.dimensiones_webp(archivo.read_bytes()), (e["ancho"], e["alto"]))
                if e["slug"] in cd.FOTOS_CHICAS:
                    self.assertLess(e["ancho"], f.ANCHO)
                else:
                    self.assertEqual(e["ancho"], f.ANCHO)
                self.assertLessEqual(archivo.stat().st_size, 120 * 1024)

    def test_sin_fotos_sobrantes(self):
        publicadas = {p.name for p in (PUBLIC / "img" / "catalogo").glob("*.webp")}
        self.assertEqual(publicadas, {f"{e['slug']}-tampico.webp" for e in CON_FOTO})

    def test_fotos_retiradas_no_se_publican(self):
        """Fotos de terceros (marca de agua, captura de buscador, logo ajeno): ni archivo, ni ruta en el JSON, ni en una
        página publicada."""
        rutas = {f.ruta_local(s) for s in cd.FOTOS_RETIRADAS}
        for slug in cd.FOTOS_RETIRADAS:
            e = cd.especie(slug)
            with self.subTest(especie=slug):
                self.assertFalse((PUBLIC / f.ruta_local(slug).lstrip("/")).exists())
                self.assertEqual((e["img"], e["ancho"], e["alto"]), (None, None, None))
        for pagina in PUBLIC.rglob("*.html"):
            html = pagina.read_text(encoding="utf-8")
            for ruta in rutas:
                with self.subTest(pagina=str(pagina.relative_to(PUBLIC)), ruta=ruta):
                    self.assertNotIn(ruta, html)


if __name__ == "__main__":
    unittest.main()
