"""Páginas que salen de plantillas (Etapa 2). Cada entrada es (ruta, archivo en public/, plantilla, contenido): la
plantilla vive en tools/site/plantillas/<plantilla>.py y el contenido en tools/site/contenido/<contenido>.py.

Un módulo de contenido de una sola página expone CONTENIDO y PARIDAD. Uno que arma varias páginas de los mismos datos
(las 9 fichas o las 11 ciudades, desde tools/pasto/data.py) expone CLAVES y pagina(clave), que devuelve un objeto con
CONTENIDO y PARIDAD; en PAGINAS su contenido se escribe "<módulo>:<clave>".

Escribe cada página con el shell ya aplicado y solo si cambia, así una segunda corrida de build.py no toca nada. Para
migrar otro tipo de página: agrega su contenido, su plantilla (o reutiliza una) y su fila aquí.
"""
import importlib
from pathlib import Path

import paginas
import shell


def _varias(modulo, ruta_de, archivo_de, plantilla):
    m = importlib.import_module(f"contenido.{modulo}")
    return tuple((ruta_de(k), archivo_de(k), plantilla, f"{modulo}:{k}") for k in m.CLAVES)


# Etapa 2i: páginas utilitarias (legales, formularios, protocolo, vivero y 404).
UTILITARIAS = (
    ("/politicas", "politicas/index.html", "legal", "politicas"),
    ("/politica-privacidad", "politica-privacidad/index.html", "legal", "politica_privacidad"),
    ("/gracias", "gracias/index.html", "formulario", "gracias"),
    ("/cuestionario", "cuestionario.html", "formulario", "cuestionario"),
    ("/datos-envio", "datos-envio/index.html", "formulario", "datos_envio"),
    ("/protocolo-cuidados-pasto-san-agustin", "protocolo-cuidados-pasto-san-agustin.html", "protocolo", "protocolo"),
    ("/vivero-tampico", "vivero-tampico/index.html", "vivero", "vivero"),
    ("/404", "404.html", "no_encontrada", "no_encontrada"),
)

# SEO fase 2a (2026-11-11): páginas nuevas, sin captura anterior que comparar (tests/test_paridad.py las salta).
SEO_F2A = (
    ("/poda-arboles-tampico", "poda-arboles-tampico/index.html", "servicio", "poda_arboles"),
    ("/empresas", "empresas/index.html", "pilar", "empresas"),
    ("/nosotros", "nosotros/index.html", "pilar", "nosotros"),
    ("/zonas", "zonas/index.html", "pilar", "zonas"),
)
NUEVAS = tuple(ruta for ruta, *_ in SEO_F2A)

PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
    ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
    ("/pasto-sintetico-tampico", "pasto-sintetico-tampico/index.html", "servicio", "sintetico_tampico"),
    ("/diseno-jardines-tampico", "diseno-jardines-tampico/index.html", "servicio", "diseno_jardines"),
    ("/mantenimiento-jardines-tampico", "mantenimiento-jardines-tampico/index.html", "servicio",
     "mantenimiento_jardines"),
    ("/sistema-riego-tampico", "sistema-riego-tampico/index.html", "servicio", "sistema_riego"),
    ("/mayoreo-pasto-tampico", "mayoreo-pasto-tampico/index.html", "b2b", "mayoreo_pasto"),
    ("/palmas-mayoreo-proyectos", "palmas-mayoreo-proyectos/index.html", "b2b", "palmas_proyectos"),
    ("/plantas-palmas-arboles-tampico", "plantas-palmas-arboles-tampico/index.html", "hub_categoria", "plantas_hub"),
    ("/palmas-tropicales-tampico", "palmas-tropicales-tampico/index.html", "hub_categoria", "palmas_tropicales"),
    ("/plantas-para-jardin-tampico", "plantas-para-jardin-tampico/index.html", "hub_categoria", "plantas_jardin"),
    ("/arboles-ornamentales-tampico", "arboles-ornamentales-tampico/index.html", "hub_categoria",
     "arboles_ornamentales"),
    ("/arboles-para-banqueta-tampico", "arboles-para-banqueta-tampico/index.html", "hub_categoria", "arboles_banqueta"),
    ("/plantas-de-interior-tampico", "plantas-de-interior-tampico/index.html", "hub_categoria", "plantas_interior"),
    ("/catalogo", "catalogo.html", "catalogo", "catalogo"),
    ("/tierra-negra-vegetal-tampico", "tierra-negra-vegetal-tampico/index.html", "material", "tierra_negra"),
    ("/tezontle-rojo-tampico", "tezontle-rojo-tampico/index.html", "material", "tezontle_rojo"),
    ("/marmol-blanco-tampico", "marmol-blanco-tampico/index.html", "material", "marmol_blanco"),
    ("/piedra-bola-rio-tampico", "piedra-bola-rio-tampico/index.html", "material", "piedra_bola"),
    ("/precios", "precios/index.html", "precios", "precios"),
    ("/post/nochebuenas-tampico-madero-mayoreo", "post/nochebuenas-tampico-madero-mayoreo/index.html", "nochebuenas",
     "nochebuenas"),
    ("/blog", "blog/index.html", "blog_indice", "blog_indice"),
    ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),
    ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),
) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
    "ciudad", lambda k: f"/pasto-sintetico/envio/{k}", lambda k: f"pasto-sintetico/envio/{k}/index.html", "tienda_guia"
) + _varias("zona", lambda k: f"/{k}", lambda k: f"{k}/index.html", "zona") + UTILITARIAS + _varias(
    "articulo", lambda k: f"/blog/{k}", lambda k: f"blog/{k}/index.html", "articulo") + SEO_F2A


def cargar(contenido):
    """Objeto con CONTENIDO y PARIDAD de la clave "<módulo>" o "<módulo>:<clave>"."""
    nombre, _, clave = contenido.partition(":")
    modulo = importlib.import_module(f"contenido.{nombre}")
    return modulo.pagina(clave) if clave else modulo


def contenido_de(ruta):
    return next(contenido for r, _a, _p, contenido in PAGINAS if r == ruta)


def renderizar(ruta, plantilla, contenido, urls):
    """HTML final de la página: plantilla + contenido + shell."""
    modulo_plantilla = importlib.import_module(f"plantillas.{plantilla}")
    return shell.aplicar(modulo_plantilla.render(cargar(contenido).CONTENIDO), ruta, urls)


def escribir_todo(urls, public=paginas.PUBLIC):
    """Escribe las páginas con plantilla que cambiaron; devuelve cuántas escribió."""
    escritas = 0
    for ruta, salida, plantilla, contenido in PAGINAS:
        path = Path(public) / salida
        html = renderizar(ruta, plantilla, contenido, urls)
        if path.is_file() and path.read_text(encoding="utf-8") == html:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        escritas += 1
    return escritas
