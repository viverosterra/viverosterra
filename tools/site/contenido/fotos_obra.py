"""Mosaicos de fotos reales por página. fotos_obra.json lo genera la herramienta de la etapa de fotos a partir de lo que
el dueño eligió en su galería de aprobación; aquí solo se consulta por ruta."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ARCHIVO = Path(__file__).resolve().with_name("fotos_obra.json")
POR_RUTA = json.loads(ARCHIVO.read_text(encoding="utf-8"))


def seccion(ruta_o_url):
    """Datos del mosaico de esa ruta (acepta la URL canónica) o None si la página no lleva."""
    return POR_RUTA.get(urlsplit(ruta_o_url).path)
