"""Redirecciones de vercel.json (SEO fase 0, 2026-11-10): cada URL heredada de Wix cae en la página que hoy responde lo
mismo, no en un destino genérico; ningún destino es a su vez origen (sin cadenas) y todos existen en public/. Las URLs
que nunca fueron contenido (/members, /profile/*, el borrador del mapa) no se redirigen: responden 404."""
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
REDIRECTS = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
DESTINO = {r["source"]: r["destination"] for r in REDIRECTS}
RIEGO_CONVIENE = "/blog/sistema-riego-automatico-conviene-tampico"
RIEGO_GUIA = "/blog/sistema-riego-automatizado-tampico"
FERTILIZACION = "/blog/fertilizacion-jardines-tampico-temporada-lluvias"
FICUS = "/blog/ficus-elastica-cuidados-tampico"
DISENO_GUIA = "/blog/diseno-jardines-tampico-guia"
MAYOREO = "/mayoreo-pasto-tampico"
# Origen (como se pide, sin codificar) → destino. Los orígenes con acentos existen codificados (%C3%A1) en vercel.json.
FIJOS = {
    "/post/cuando-es-mejor-regar-mi-pasto-en-rollo-san-agustin-jardin": "/blog/cuando-regar-pasto-san-agustin-tampico",
    "/post/tu-pasto-san-agustin-esta-amarillo": "/blog/cesped-amarillo-tampico-causas-soluciones",
    "/post/como-instalar-pasto-sintetico": "/blog/como-instalar-pasto-sintetico",
    "/post/cuidados-de-los-ficus-elastica-guía-definitiva-para-un-árbol-del-caucho-saludable": FICUS,
    "/post/como-cuidar-de-tu-ficus-elastica-hule-en-tampico-tamaulipas": FICUS,
    "/post/por-qué-es-conveniente-un-sistema-de-riego": RIEGO_CONVIENE,
    "/post/cada-cuánto-hay-que-fertilizar-las-plantas-guía-práctica-para-jardineros-modernos": FERTILIZACION,
    "/post/tienes-problemas-de-hormigas": "/blog/plagas-comunes-jardin-tampico",
    "/post/pasto-en-rollo-por-mayoreo-precio-por-m2": MAYOREO,
    "/post/rancho-productor-de-pasto-en-rollo-san-agustín-mayoreo-mejor-precio-y-envíos-a-todo-méxico": MAYOREO,
    "/venta-palmas-mayoreo-huasteca": "/palmas-mayoreo-proyectos",
    # SEO fase 2a (2026-11-11, mapa §3a): el 301 viejo del puerto industrial cae en el pilar de empresas.
    "/jardineria-puerto-industrial-altamira": "/empresas",
    # Encontrados al revisar el resto de /post/*: una guía cae en la guía del mismo tema, no en la página de servicio.
    "/post/sistemas-de-riego-automatizado-tampico": RIEGO_GUIA,
    "/post/guía-definitiva-del-sistema-de-riego-automático-en-méxico-ahorra-agua-y-optimiza-tu-jardín": RIEGO_GUIA,
    "/post/diseño-de-jardines-en-tampico-madero-y-altamira-tamaulipas-guía-completa-2025": DISENO_GUIA,
    "/post/cómo-diseñar-tu-jardín-en-tampico-tips-consejos-y-preparaciones-clave-de-viveros-terra": DISENO_GUIA,
}
# Variantes del mismo origen que también deben ir al destino nuevo: con barra final o con los acentos mal codificados
# (así los pide algún enlace viejo). Se reconocen por el arranque, que no lleva acentos.
MISMA_FAMILIA = {
    "/post/cuando-es-mejor-regar-mi-pasto": "/blog/cuando-regar-pasto-san-agustin-tampico",
    "/post/cuidados-de-los-ficus-elastica": FICUS,
    "/post/por-qu": RIEGO_CONVIENE,
    "/post/cada-cu": None,  # dos artículos distintos empiezan así (fertilizar y podar): se revisa abajo por palabra
    "/post/rancho-productor": MAYOREO,
}
SIN_REDIRECCION = ("/members", "/profile/:path*", "/preview-mapa-cobertura", "/preview-mapa-cobertura.html")


def existe(destino):
    ruta = destino.split("#")[0].split("?")[0]
    archivo = PUBLIC / ruta.strip("/")
    return ruta == "/" or archivo.is_file() or archivo.with_suffix(".html").is_file() or (archivo / "index.html").is_file()


class RedireccionesTest(unittest.TestCase):
    def test_destinos_fijados(self):
        decodificados = {unquote(origen): destino for origen, destino in DESTINO.items()}
        for origen, destino in FIJOS.items():
            with self.subTest(origen=origen):
                self.assertEqual(decodificados.get(origen), destino)

    def test_las_variantes_del_mismo_origen_van_al_mismo_destino(self):
        for origen, destino in DESTINO.items():
            for arranque, esperado in MISMA_FAMILIA.items():
                if esperado and origen.startswith(arranque) and "amarillas" not in origen:
                    with self.subTest(origen=origen):
                        self.assertEqual(destino, esperado)
            if "fertilizar" in origen:
                with self.subTest(origen=origen):
                    self.assertEqual(destino, FERTILIZACION)

    def test_sin_cadenas_y_con_destino_real(self):
        for origen, destino in DESTINO.items():
            with self.subTest(origen=origen):
                self.assertNotIn(destino, DESTINO, "el destino es a su vez origen: cadena de redirecciones")
                self.assertNotIn(destino.rstrip("/") or "/", DESTINO)
                self.assertTrue(existe(destino), destino)

    def test_un_origen_una_sola_regla(self):
        origenes = [r["source"] for r in REDIRECTS]
        self.assertEqual(sorted({o for o in origenes if origenes.count(o) > 1}), [])

    def test_lo_que_nunca_fue_contenido_responde_404(self):
        for origen in SIN_REDIRECCION:
            with self.subTest(origen=origen):
                self.assertNotIn(origen, DESTINO)
        for ruta in ("members", "profile", "preview-mapa-cobertura"):
            with self.subTest(ruta=ruta):
                self.assertFalse((PUBLIC / ruta).exists())
                self.assertFalse((PUBLIC / f"{ruta}.html").exists())


if __name__ == "__main__":
    unittest.main()
