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
# SEO fase 2c (2026-11-11, mapa §2 y §3c): cinco fusiones con 301 y cinco artículos retitulados. Las tarjetas de los
# artículos fusionados con foto se quedan, con su misma foto, y llevan al destino (riego y bajo presupuesto, al apartado
# donde quedó su contenido); las dos sin foto salen; las de los retitulados llevan su título nuevo.
M_FUSIONADO = ("SEO fase 2c: el artículo se fusionó con 301 en otro que sigue en el índice (o en /pasto-sintetico/perros); "
               "su tarjeta sale y la del destino se queda.")
PARIDAD["reemplazos"] |= {
    "Las 8 palmas más vendidas en Tampico (con precios)": "8 palmas para jardín en Tampico, con precios",
    "Pasto sintético para perros: la guía completa": "Pasto sintético para perros: limpieza, olor y modelos",
    "Tierra negra: ¿costal o camión?": "¿Cuánta tierra negra necesitas? Costal o camión",
    "Riego Automático en Tampico: ¿Vale la Pena? Costos Reales": "Riego automático: tipos, costo y cuándo conviene",
    "Cómo Diseñar Tu Jardín en Tampico: Guía Paso a Paso": "Cómo diseñar tu jardín paso a paso",
    "Tezontle Rojo: 8 Usos que Transforman Tu Jardín": "¿Para qué sirve el tezontle? 8 usos en el jardín",
    "Pasto San Agustín: Guía Completa de Instalación y Mantenimiento": "Cómo instalar pasto en rollo San Agustín paso a paso",
    "Plantas de Interior para Casas en Tampico: Las Más Recomendadas":
        "¿Qué plantas de interior resisten el calor y el aire acondicionado?",
    "/blog/palmas-mas-vendidas-tampico-precios": "/blog/palmas-para-jardin-tampico",
    "/blog/palmas-tropicales-jardin-tampico": "/blog/palmas-para-jardin-tampico",
    "/blog/pasto-sintetico-para-perros": "/pasto-sintetico/perros",
    "/blog/riego-automatico-tampico-roi": "/blog/sistema-riego-automatizado-tampico",
    "/blog/sistema-riego-automatico-conviene-tampico": "/blog/sistema-riego-automatizado-tampico",
    "/blog/jardin-bajo-presupuesto-tampico": "/blog/cuanto-cuesta-jardin-tampico-precios",
}
PARIDAD["retirados"] |= {
    "Las 8 Palmas Más Espectaculares para Jardines en Tampico": M_FUSIONADO,
    "¿Conviene el Riego Automático en Tampico? Guía 2026": M_FUSIONADO,
}
# Lo que cambia en el hero frente a la captura (encabezados, precios y enlaces siguen en tests/test_paridad.py).
PARIDAD["hero"] = ('Entrega A de experiencia (2026-11-10), hero de marca: cabecera de lectura: el complemento del <h1> va en serif verde; el WhatsApp y el teléfono pasan de botones a enlaces de texto; «Por el equipo técnico de Viveros Terra» sale de la entrada (el autor ya va en el kicker).')
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: mensaje con qué, colonia y metros (reescritura 9).'

# Lo que cambia por la Entrega C de experiencia (ritmo y movimiento).
PARIDAD["ritmo"] = 'Entrega C de experiencia (2026-11-10), ritmo y movimiento: una fila discreta de WhatsApp («Preguntar por WhatsApp») cada 12 tarjetas (antes, 25.4 pantallas sin CTA); en celular la tarjeta con foto va a dos columnas con la miniatura en su misma proporción; revelado por scroll de encabezados y figuras y balanceo de la etiqueta en escritorio.'
