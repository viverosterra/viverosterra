"""Preguntas rápidas antes de abrir WhatsApp (spec docs/superpowers/specs/2026-11-16-whatsapp-primer-mensaje-design.md).

Fuente única de las preguntas y sus opciones; public/js/vt-preguntas.js las pinta y arma el mensaje. Las opciones son
datos ya publicados (data.MODELOS, data.ESTADOS_ORDEN); los rangos de m² los aprobó el dueño el 2026-11-16."""
import json

import componentes  # noqa: F401  (agrega tools/pasto al path)
import data
import datos

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


# Entrega 2 (servicios de Tampico): cada opción es (valor, etiqueta, frase). El mensaje es `inicio` + las frases en el
# orden de `orden` (una pregunta sin contestar pone su `defecto`, si lo tiene) + "." + `cola`. Las frases traen su propio
# separador. Rangos y opciones aprobados por el dueño el 2026-11-16; frecuencias de datos.FRECUENCIAS_MANTENIMIENTO.
LUGAR = {"clave": "lugar", "texto": "¿Dónde?",
         "opciones": [("tampico", "Tampico", " en Tampico"), ("madero", "Madero", " en Ciudad Madero"),
                      ("altamira", "Altamira", " en Altamira")]}
TAMANO_JARDIN = [("chico", "Chico (menos de 50 m²)", "chico"), ("mediano", "Mediano (50 a 200 m²)", "mediano"),
                 ("grande", "Grande (más de 200 m²)", "grande")]
_M2_JARDIN = {"chico": "de menos de 50 m²", "mediano": "de 50 a 200 m²", "grande": "de más de 200 m²"}


def _tamano(prefijo):
    return {"clave": "tamano", "texto": "¿Tamaño del jardín?",
            "opciones": [(v, t, f"{prefijo}{_M2_JARDIN[v]}") for v, t, _f in TAMANO_JARDIN]}


_FRECUENCIA = {"semanal": ", cada semana", "cada 15 días": ", cada 15 días", "cada 21 días": ", cada 21 días",
               "mensual": ", cada mes"}

SERVICIOS = {
    "pasto": {
        "id": "pasto", "titulo": "Cuéntanos qué buscas", "inicio": "Hola, quiero cotizar pasto San Agustín en rollo",
        "corto": "Hola, tengo una pregunta sobre pasto en rollo.",
        "preguntas": [
            {"clave": "modo", "texto": "¿Cómo lo quieres?",
             "opciones": [("solo", "Solo el pasto", ", solo el pasto"), ("instalado", "Instalado", ", instalado")]},
            {"clave": "metros", "texto": "¿Cuántos m²?",
             "opciones": [("<50", "Menos de 50", ", menos de 50 m²"), ("50-200", "50 a 200", ", entre 50 y 200 m²"),
                          ("200-500", "200 a 500", ", entre 200 y 500 m²"),
                          (">=500", "500 o más (mayoreo)", ", 500 m² o más (mayoreo)")]},
            {**LUGAR, "opciones": LUGAR["opciones"] + [("otro", "Otro lugar", ", fuera de Tampico, Madero y Altamira")]},
        ],
    },
    "mantenimiento": {
        "id": "mantenimiento", "titulo": "Cuéntanos qué buscas", "inicio": "Hola, quiero cotizar mantenimiento de jardín",
        "corto": "Hola, tengo una pregunta sobre mantenimiento de jardín.",
        "preguntas": [
            _tamano(" "),
            {"clave": "frecuencia", "texto": "¿Cada cuándo?",
             "opciones": [(f, f[0].upper() + f[1:], _FRECUENCIA[f]) for f in datos.FRECUENCIAS_MANTENIMIENTO]
             + [("no-se", "No sé", "")]},
            LUGAR,
        ],
    },
    "poda": {
        "id": "poda", "titulo": "Cuéntanos qué necesitas", "inicio": "Hola, quiero cotizar",
        "corto": "Hola, tengo una pregunta sobre poda o derribo.", "cola": "Les mando fotos y la ubicación.",
        "orden": ["servicio", "que", "lugar"],
        "preguntas": [
            {"clave": "que", "texto": "¿Qué es?", "defecto": " de árboles o palmas",
             "opciones": [("arbol", "Árbol", " de un árbol"), ("palma", "Palma", " de palmas"),
                          ("varios", "Varios", " de varios árboles y palmas")]},
            {"clave": "servicio", "texto": "¿Qué necesitas?", "defecto": " poda o derribo",
             "opciones": [("poda", "Poda", " la poda"), ("derribo", "Derribo", " el derribo"),
                          ("revisar", "No sé, que lo revisen", " una revisión")]},
            LUGAR,
        ],
    },
    "riego": {
        "id": "riego", "titulo": "Cuéntanos qué buscas", "inicio": "Hola, quiero cotizar riego automático",
        "corto": "Hola, tengo una pregunta sobre riego automático.", "cola": "Les mando fotos del espacio.",
        "preguntas": [
            {"clave": "para", "texto": "¿Para qué?",
             "opciones": [("pasto", "Pasto (aspersores)", " con aspersores para el pasto"),
                          ("plantas", "Plantas y jardineras (goteo)", " por goteo para plantas y jardineras"),
                          ("ambos", "Las dos", " para pasto y plantas"), ("no-se", "No sé", "")]},
            _tamano(", jardín "),
            LUGAR,
        ],
    },
    "diseno": {
        "id": "diseno", "titulo": "Cuéntanos qué buscas", "inicio": "Hola, me interesa el diseño de mi jardín",
        "corto": "Hola, tengo una pregunta sobre diseño de jardines.", "cola": "Les mando fotos del espacio.",
        "preguntas": [
            {"clave": "plan", "texto": "¿Qué plan te interesa?",
             "opciones": [("esencial", "Esencial", " con el Plan Terra Esencial"),
                          ("completo", "Completo", " con el Plan Terra Completo"),
                          ("premium", "Premium", " con el Plan Terra Premium"), ("no-se", "No sé", "")]},
            _tamano(", jardín "),
        ],
    },
}


def json_servicio(clave, mensaje_pagina):
    """JSON del panel de un servicio de Tampico. El panel solo se abre en los botones que mandan el mensaje general de
    la página (`generico`); los de cada plan u opción, el medidor y los simuladores ya traen su propio mensaje."""
    conjunto = SERVICIOS[clave]
    return json_pagina({}, conjunto["corto"], conjunto, generico=datos.sin_huecos(mensaje_pagina))


def json_pagina(fijo, corto=CORTO_SINTETICO, conjunto=SINTETICO, generico=None):
    """Bloque JSON para vt-preguntas.js. fijo: lo que la página ya sabe (modelo de la ficha; estado y ciudad de la
    página de envío); esas preguntas no se muestran. corto: el mensaje de «Solo quiero contactarlos». generico: si se
    da, solo los botones con ese mensaje abren el panel."""
    datos_pagina = {"conjunto": conjunto, "fijo": fijo, "corto": corto, **({"generico": generico} if generico else {})}
    cuerpo = json.dumps(datos_pagina, ensure_ascii=False, separators=(",", ":"))
    seguro = cuerpo.replace("</", "<\\/")
    return f'<script type="application/json" id="vt-preguntas">{seguro}</script>'


SCRIPT = "/js/vt-preguntas.js"
CLASE = " vt-preguntas"  # <body class="… vt-preguntas">: el shell agrega terra-preguntas.css


def scripts(base_scripts=()):
    """Los scripts de la página más vt-folio.js (folio del mensaje) y vt-preguntas.js, sin repetir y en ese orden."""
    previos = tuple(base_scripts)
    return previos + tuple(s for s in ("/js/vt-folio.js", SCRIPT) if s not in previos)
