"""/blog: las secciones y tarjetas salen de contenido/blog/_indice.json, extraído de la página publicada (mismas fotos, en
el mismo orden); su título y su descripción (también en Open Graph y Twitter), los de la fase 0 de SEO. El conteo lo pone shell.aplicar en cada <span data-vt-conteo="blog">."""
import json
from pathlib import Path

import datos
from contenido import seo

_DOC = json.loads((Path(__file__).resolve().parent / "blog" / "_indice.json").read_text(encoding="utf-8"))


def sin_repetidos(secciones):
    """"Todos los artículos" no repite lo que ya está en "Nuevos artículos"."""
    nuevos = {t["href"] for s in secciones if s["titulo"] == "Nuevos artículos" for t in s["tarjetas"]}
    return [{**s, "tarjetas": [t for t in s["tarjetas"] if t["href"] not in nuevos]} if s["titulo"] == "Todos los artículos" else s
            for s in secciones]


CONTENIDO = {
    "meta": _DOC["meta"], "jsonld": _DOC["jsonld"], "tipo": "blog", "foto": _DOC["foto"], "secciones": sin_repetidos(_DOC["secciones"]),
    "migas": (("Inicio", "/"), ("Blog", None)),
    "h1": 'Blog de Jardinería <span class="vt-serif">para Tampico y Tamaulipas.</span>',
    # El autor ("Por el equipo técnico…") ya va en el kicker, junto al conteo de guías.
    "lede": ("Guías prácticas, comparativas honestas y consejos de jardinería adaptados al clima cálido-húmedo del sur de "
             "Tamaulipas."),
    "mensaje": "Hola, vi el blog de Viveros Terra y quiero cotizar",
    "servicios": (("/pasto-en-rollo-tampico", "Pasto en Rollo", "San Agustín · Japonés · Bermuda"),
                  ("/pasto-sintetico-tampico", "Pasto Sintético", "Venta e instalación profesional"),
                  ("/plantas-palmas-arboles-tampico", "Plantas, Palmas y Árboles", "Vivero productor directo"),
                  ("/tezontle-rojo-tampico", "Tezontle Rojo", "Costal y camión volteo"),
                  ("/tierra-negra-vegetal-tampico", "Tierra Negra Vegetal", "Costal y camión volteo"),
                  ("/diseno-jardines-tampico", "Diseño de Jardines", "Plan Terra · Desde $3,000")),
}
M_REPETIDA = "Era la segunda tarjeta del mismo artículo: \"Todos\" ya no repite lo de \"Nuevos\", donde sigue con su otro título."
M_PUBLISHER = ("SEO fase 1: el publisher del Blog es una referencia por @id a la entidad única #negocio; se retiran la "
               "Organization suelta y su logo (el logo va en el nodo completo de la home).")
PARIDAD = {"jsonld": {"Organization": M_PUBLISHER, "ImageObject": M_PUBLISHER}, "meta": seo.paridad(_DOC["meta"]["title"], _DOC["meta"]["description"]),
           "reemplazos": {"Las 8 palmas más vendidas en Tampico (con precios)": "8 palmas para jardines en Tampico (con precios)",
                          "Cómo Ahorrar Hasta 50% de Agua en Tu Jardín en Tampico": "Cómo Ahorrar Hasta 40% de Agua en Tu Jardín en Tampico"},
           "retirados": {"Cómo Instalar Pasto Sintético Tú Mismo: Paso a Paso": M_REPETIDA,
                         "Pasto Sintético para Perros y Mascotas: Guía Completa": M_REPETIDA,
                         "$300": "La tarjeta de la Palma Areca decía desde $300; el precio oficial es desde $250 (datos.py)."}}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: cabecera de lectura: el complemento del <h1> va en serif verde; el WhatsApp y el teléfono pasan de botones a enlaces de texto; «Por el equipo técnico de Viveros Terra» sale de la entrada (el autor ya va en el kicker).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: mensaje con qué, colonia y metros (reescritura 9).'

# Lo que cambia por la Entrega C de experiencia (ritmo y movimiento).
PARIDAD["ritmo"] = 'Entrega C de experiencia (2026-11-10), ritmo y movimiento: una fila discreta de WhatsApp («Preguntar por WhatsApp») cada 12 tarjetas (antes, 25.4 pantallas sin CTA); en celular la tarjeta con foto va a dos columnas con la miniatura en su misma proporción; revelado por scroll de encabezados y figuras y balanceo de la etiqueta en escritorio.'
