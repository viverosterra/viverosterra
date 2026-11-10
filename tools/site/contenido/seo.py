"""Títulos y descripciones de la fase 0 de SEO (2026-11-10): lo que comparten los módulos de contenido para declarar
el cambio en PARIDAD["meta"].

Cada página lleva un título de 60 caracteres o menos y una descripción de 70 a 155 (tests/test_titulos.py), tomados de
docs/seo/2026-11/mapa-palabras-clave.md y revisados contra las reglas del dueño: nada inventado, precios solo de
datos.PRECIOS (y de tools/pasto/data.py en la tienda), sin "gratis", "sin costo", "más vendido", plazos de entrega ni
porcentajes de anticipo, y sin "con IVA" junto al pasto sin instalar, las plantas, los árboles o las palmas. El mismo
texto va en el <title>, la descripción, el Open Graph y la Twitter Card de la página.
"""
MOTIVO = ("SEO fase 0 (2026-11-10): título de 60 caracteres o menos y descripción de 155 o menos, del mapa de palabras "
          "clave (docs/seo/2026-11/mapa-palabras-clave.md), revisados contra las reglas del dueño.")
CLAVES = ("title", "description", "og:title", "og:description")


def paridad(titulo, descripcion, anteriores=None, claves=CLAVES):
    """PARIDAD["meta"] de una página con el título y la descripción nuevos: {clave: (valor, motivo)} para el título, la
    descripción y sus pares de Open Graph. `anteriores` es el PARIDAD["meta"] que el módulo ya declaraba: sus otras
    claves (og:image…) se conservan, y el motivo que ya tenían el título o la descripción queda después del nuevo."""
    anteriores = dict(anteriores or {})
    valores = {"title": titulo, "description": descripcion, "og:title": titulo, "og:description": descripcion}
    salida = {clave: valor for clave, valor in anteriores.items() if clave not in claves}
    for clave in claves:
        previo = f" Antes: {anteriores[clave][1]}" if clave in anteriores else ""
        salida[clave] = (valores[clave], f"{MOTIVO}{previo}")
    return salida
