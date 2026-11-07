"""Contexto de cada página para el shell: tipo (prefijo de data-cta), sección activa del menú, servicio, barra móvil y
mensajes de WhatsApp (los propios de la página salen de mensajes_paginas.py).

Toda página de public/ debe tener contexto. Si agregas una página, agrégala aquí: el build falla con rutas sin contexto.
"""
from pathlib import Path

import datos
import mensajes_paginas

PUBLIC = Path(__file__).resolve().parents[2] / "public"
SIN_BARRA = {"tienda", "ciudad", "catalogo"}
# Formularios y páginas con su propia barra fija de compra (#buybar): dos barras fijas se tapan en celular.
RUTAS_SIN_BARRA = {"/cuestionario", "/gracias", "/datos-envio", "/pasto-sintetico-tampico"}

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
    "/cuestionario": ("utilidad", "jardin", "jardin"),
    "/plantas-palmas-arboles-tampico": _PLANTAS,
    "/palmas-tropicales-tampico": _PLANTAS,
    "/plantas-para-jardin-tampico": _PLANTAS,
    "/arboles-ornamentales-tampico": _PLANTAS,
    "/arboles-para-banqueta-tampico": _PLANTAS,
    "/plantas-de-interior-tampico": _PLANTAS,
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


def contexto(ruta):
    """Diccionario nuevo con ruta, tipo, activo, servicio, barra y mensajes de WhatsApp (menú/barra y pie) de la ruta."""
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
        texto = mensajes_paginas.BLOG.get(slug, texto)
    if ruta in mensajes_paginas.RUTAS:
        texto, texto_pie = mensajes_paginas.RUTAS[ruta]
    return {
        "ruta": ruta,
        "tipo": tipo,
        "activo": activo,
        "servicio": servicio,
        "barra": tipo not in SIN_BARRA and ruta not in RUTAS_SIN_BARRA,
        "mensaje": datos.con_firma(texto),
        "mensaje_pie": datos.con_firma(texto_pie or texto),
    }
