"""Contexto de cada página para el shell: tipo (prefijo de data-cta), sección activa del menú, servicio, barra móvil y
mensajes de WhatsApp (los propios de la página salen de mensajes_paginas.py).

Toda página de public/ debe tener contexto. Si agregas una página, agrégala aquí: el build falla con rutas sin contexto.
"""
from pathlib import Path

import sys

import datos
import mensajes_paginas

PASTO = str(Path(__file__).resolve().parents[1] / "pasto")
if PASTO not in sys.path:
    sys.path.append(PASTO)  # al final, como en componentes.py: tools/pasto también tiene un build.py
import data  # noqa: E402
from ciudades import CIUDADES  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[2] / "public"
SIN_BARRA = {"tienda", "catalogo"}
# Formularios y páginas con su propia barra fija de compra (#buybar): dos barras fijas se tapan en celular.
RUTAS_SIN_BARRA = {"/cuestionario", "/gracias", "/datos-envio", "/pasto-sintetico-tampico",
                   datos.NOCHEBUENAS["ruta"]}
# Páginas de la tienda sin cotizador ni #buybar (Etapa 2b): llevan la barra móvil del shell.
RUTAS_CON_BARRA = {"/pasto-sintetico/perros", "/pasto-sintetico/cuantos-rollos", "/pasto-sintetico/azotea",
                   "/pasto-sintetico/alberca", "/pasto-sintetico/ancho-del-rollo", "/pasto-sintetico/vs-natural"}

_PLANTAS = ("plantas", "plantas", "plantas")
_MATERIAL = ("material", "plantas", "materiales")
_UTILIDAD = ("utilidad", None, "general")

EXACTAS = {
    "/": ("home", None, "general"),
    "/pasto-en-rollo-tampico": ("servicio-pasto", "pasto-natural", "pasto-natural"),
    "/mayoreo-pasto-tampico": ("b2b", "pasto-natural", "empresas"),
    "/protocolo-cuidados-pasto-san-agustin": ("posventa", "pasto-natural", "pasto-natural"),
    "/pasto-sintetico-tampico": ("servicio-sintetico", "pasto-sintetico", "pasto-sintetico"),
    "/pasto-sintetico": ("tienda", "pasto-sintetico", "pasto-sintetico"),
    "/diseno-jardines-tampico": ("servicio-diseno", "jardin", "jardin"),
    "/mantenimiento-jardines-tampico": ("servicio-mantenimiento", "jardin", "jardin"),
    "/sistema-riego-tampico": ("servicio-riego", "jardin", "jardin"),
    # SEO fase 2a (2026-11-11): poda, empresas, nosotros y el índice de zonas.
    "/poda-arboles-tampico": ("servicio-poda", "jardin", "jardin"),
    "/empresas": ("b2b", "empresas", "empresas"),
    "/nosotros": ("nosotros", None, "general"),
    "/zonas": ("zonas", None, "jardin"),
    "/cuestionario": ("utilidad", "jardin", "jardin"),
    "/plantas-palmas-arboles-tampico": _PLANTAS,
    "/palmas-tropicales-tampico": _PLANTAS,
    "/plantas-para-jardin-tampico": _PLANTAS,
    "/arboles-ornamentales-tampico": _PLANTAS,
    "/arboles-para-banqueta-tampico": _PLANTAS,
    "/plantas-de-interior-tampico": _PLANTAS,
    datos.NOCHEBUENAS["ruta"]: ("nochebuenas", "plantas", "plantas"),
    "/catalogo": ("catalogo", "plantas", "plantas"),
    "/tierra-negra-vegetal-tampico": _MATERIAL,
    "/tezontle-rojo-tampico": _MATERIAL,
    "/marmol-blanco-tampico": _MATERIAL,
    "/piedra-bola-rio-tampico": _MATERIAL,
    "/palmas-mayoreo-proyectos": ("b2b", "empresas", "empresas"),
    "/vivero-tampico": ("vivero", None, "general"),
    "/precios": ("precios", "precios", "general"),
    "/blog": ("blog", None, "general"),
    "/politicas": _UTILIDAD,
    "/politica-privacidad": _UTILIDAD,
    "/gracias": _UTILIDAD,
    "/datos-envio": _UTILIDAD,
    "/404": _UTILIDAD,
}
PREFIJOS = (
    ("/pasto-sintetico/envio/", ("ciudad", "pasto-sintetico", "pasto-sintetico")),
    ("/pasto-sintetico/", ("tienda", "pasto-sintetico", "pasto-sintetico")),
    ("/blog/", ("blog", None, "general")),
    ("/jardineria-", ("zona", None, "jardin")),
)


def ruta_de(path, public=PUBLIC):
    """Ruta pública ("/blog/x") del archivo HTML dentro de public/."""
    rel = Path(path).resolve().relative_to(Path(public).resolve()).as_posix()
    if rel == "index.html":
        return "/"
    for sufijo in ("/index.html", ".html"):
        if rel.endswith(sufijo):
            return "/" + rel[: -len(sufijo)]
    raise ValueError(f"No es una página HTML: {rel}")


# Decisión del dueño (2026-11-21): en la tienda de pasto sintético, el «Cotizar» del encabezado y del menú dicen qué
# ficha o qué ciudad está viendo la persona. El de la ficha es, palabra por palabra, el que arma tienda-pasto.js
# (mensajeBase) cuando hay JavaScript: así no se pisan. El hub y las guías siguen con el genérico; la barra fija y el pie
# también (la barra abre el panel de preguntas, que arma su propio mensaje).
CIUDAD_POR_SLUG = {c["slug"]: c["nombre"] for c in CIUDADES}


def mensaje_tienda(ruta):
    """Mensaje del encabezado y del menú para una ficha o una ciudad de la tienda; None en el resto de las rutas."""
    if ruta.startswith("/pasto-sintetico/envio/"):
        ciudad = CIUDAD_POR_SLUG.get(ruta.rsplit("/", 1)[1])
        return ciudad and (f"Hola, quiero cotizar pasto sintético con envío a {ciudad}.\nMetros aprox.: ___\n"
                           "Modelo (si ya lo elegiste): ___")
    modelo = data.BY_SLUG.get(ruta.removeprefix("/pasto-sintetico/")) if ruta.startswith("/pasto-sintetico/") else None
    return modelo and f"Hola, quiero cotizar el pasto sintético {modelo['nombre']}.\nMi estado: ___\nMetros aprox.: ___"


def contexto(ruta):
    """Diccionario nuevo con ruta, tipo, activo, servicio, barra y mensajes de WhatsApp (menú, barra y pie) de la ruta.
    "mensaje" es el del encabezado y el menú; "mensaje_barra" solo difiere en las fichas y ciudades de la tienda."""
    valores = EXACTAS.get(ruta)
    if valores is None:
        valores = next((v for prefijo, v in PREFIJOS if ruta.startswith(prefijo)), None)
    if valores is None:
        raise KeyError(f"Ruta sin contexto en tools/site/paginas.py: {ruta}")
    tipo, activo, servicio = valores
    texto, texto_pie = datos.MENSAJES[servicio], mensajes_paginas.PIE_TIPO.get(tipo)
    slug = ruta[len("/blog/"):] if ruta.startswith("/blog/") else None
    if slug:
        servicio = mensajes_paginas.tema_blog(slug)
        texto = mensajes_paginas.mensaje_blog(slug)
    if ruta in mensajes_paginas.RUTAS:
        texto, texto_pie = mensajes_paginas.RUTAS[ruta]
    if ruta == datos.NOCHEBUENAS["ruta"]:
        texto, texto_pie = mensajes_paginas.NOCHEBUENAS[datos.NOCHEBUENAS["modo"]], None
    return {
        "ruta": ruta,
        "tipo": tipo,
        "activo": activo,
        "servicio": servicio,
        "barra": (tipo not in SIN_BARRA and ruta not in RUTAS_SIN_BARRA) or ruta in RUTAS_CON_BARRA,
        "mensaje": datos.con_firma(mensaje_tienda(ruta) or texto),
        "mensaje_barra": datos.con_firma(texto),
        "mensaje_pie": datos.con_firma(texto_pie or texto),
    }
