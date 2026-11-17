"""Preguntas rápidas antes de abrir WhatsApp (spec docs/superpowers/specs/2026-11-16-whatsapp-primer-mensaje-design.md).

Fuente única de las preguntas y sus opciones; public/js/vt-preguntas.js las pinta y arma el mensaje. Las opciones son
datos ya publicados (data.MODELOS, data.ESTADOS_ORDEN); los rangos de m² los aprobó el dueño el 2026-11-16."""
import json

import componentes  # noqa: F401  (agrega tools/pasto al path)
import data

CORTO_SINTETICO = "Hola, tengo una pregunta sobre pasto sintético."

SINTETICO = {
    "id": "sintetico",
    "titulo": "Cuéntanos qué buscas",
    "preguntas": [
        {"clave": "modelo", "texto": "¿Qué modelo?",
         "opciones": [(m["slug"], m["nombre"]) for m in data.MODELOS] + [("no-se", "No sé, recomiéndenme")]},
        {"clave": "m2", "texto": "¿Cuántos m²?",
         "opciones": [("<25", "Menos de 25"), ("25-50", "25 a 50"), ("50-100", "50 a 100"), (">100", "Más de 100")]},
        {"clave": "destino", "texto": "¿A dónde?",
         "opciones": [("recoger", "Recoger en el vivero (Cd. Madero)"),
                      ("local", "Instalado en Tampico, Madero o Altamira"), ("envio", "Envío a otro estado")]},
    ],
    "estados": data.ESTADOS_ORDEN,
}


def json_pagina(fijo, corto=CORTO_SINTETICO, conjunto=SINTETICO):
    """Bloque JSON para vt-preguntas.js. fijo: lo que la página ya sabe (modelo de la ficha; estado y ciudad de la
    página de envío); esas preguntas no se muestran. corto: el mensaje de «Solo quiero contactarlos»."""
    cuerpo = json.dumps({"conjunto": conjunto, "fijo": fijo, "corto": corto}, ensure_ascii=False, separators=(",", ":"))
    seguro = cuerpo.replace("</", "<\\/")
    return f'<script type="application/json" id="vt-preguntas">{seguro}</script>'


SCRIPT = "/js/vt-preguntas.js"
CLASE = " vt-preguntas"  # <body class="… vt-preguntas">: el shell agrega terra-preguntas.css


def scripts(base_scripts=()):
    """Los scripts de la página más vt-folio.js (folio del mensaje) y vt-preguntas.js, sin repetir y en ese orden."""
    previos = tuple(base_scripts)
    return previos + tuple(s for s in ("/js/vt-folio.js", SCRIPT) if s not in previos)
