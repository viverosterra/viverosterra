"""Contenido de /cuestionario, paso 2 del diseño (lo manda el asesor; noindex). Mismo action de formsubmit y mismos name y
value que main (el dueño recibe esos campos: tests/paridad/utilitarias-contrato.json), más el honeypot _honey que tienen
los demás formularios. Dos H1 en main: queda uno. Los rangos de inversión son opciones del cliente, no precios."""
import datos
import mensajes_paginas
import componentes_util as cu

URL = f"{datos.SITIO}/cuestionario"
DESCRIPCION = "Cuéntanos de tu jardín para preparar tu propuesta de diseño. Viveros Terra, Tampico, Madero y Altamira."
_otro = (("id", "rb-otro-esp"),)
_riego = (("class", "riego-trigger"),)


def _radios(legend, name, items, **extra):
    return cu.opciones({"legend": legend, "tipo": "radio", "name": name, "items": items, **extra})


def _casillas(legend, name, items):
    return cu.opciones({"legend": legend, "tipo": "checkbox", "name": name, "items": items})


def _iguales(*textos):
    return tuple((t, t) for t in textos)


PASO_1 = (
    cu.fila(cu.campo({"label": "Nombre completo", "name": "nombre", "id": "nombre", "tipo": "text", "requerido": True,
                      "placeholder": "Ej. María González", "completar": "name"}),
            cu.campo({"label": "WhatsApp", "name": "whatsapp", "id": "whatsapp", "tipo": "tel", "requerido": True,
                      "placeholder": "+52 833 000 0000", "completar": "tel"}), columnas=2),
    cu.fila(cu.campo({"label": "Correo electrónico", "name": "email", "tipo": "email", "placeholder": "correo@ejemplo.com",
                      "completar": "email"}),
            cu.campo({"label": "¿Cómo nos conoció?", "name": "como_nos_conocio", "tipo": "lista",
                      "opciones": (("", "Seleccionar..."), (None, "Página web"), (None, "Instagram / Facebook"),
                                   (None, "Referido de un cliente"), (None, "Google"), (None, "Otro"))}), columnas=2),
    cu.campo({"label": "Colonia / Fraccionamiento", "name": "direccion", "tipo": "text",
              "placeholder": "Ej. Fracc. Las Palmas, Altamira"}),
)
PASO_2 = (
    _radios("Tipo de espacio", "tipo_espacio",
            _iguales("Jardín frontal", "Jardín trasero", "Ambos", "Interior / patio", "Banqueta", "Plaza comercial",
                     "Restaurante") + (("Otro", "Otro", _otro),),
            sub=cu.condicional("otro-esp-wrap", cu.campo({"label": "Especificar tipo de espacio", "name": "tipo_espacio_otro",
                                                           "tipo": "text", "placeholder": "Especificar tipo de espacio..."}))),
    cu.fila(cu.campo({"label": "Área de pasto (m²)", "name": "area_pasto", "id": "area_pasto", "tipo": "number",
                      "placeholder": "Ej. 60", "min": "0", "pista": "Aproximado está bien"}),
            cu.campo({"label": "Área jardinera (m²)", "name": "area_jardinera", "id": "area_jard", "tipo": "number",
                      "placeholder": "Ej. 20", "min": "0"}),
            cu.campo({"label": "Área total (m²)", "name": "area_total", "id": "area_total_input", "tipo": "number",
                      "placeholder": "Ej. 80", "min": "0"}), columnas=3),
    cu.SUMA_AREAS,
    cu.fila(
        _radios("¿Tiene riego instalado?", "riego_instalado",
                (("Sí", "Sí"), ("No", "No", _riego), ("Parcial", "Parcial", _riego)),
                sub=cu.condicional("cond-riego", _radios("¿Considera instalar riego?", "instalar_riego",
                                                          _iguales("Sí, de inmediato", "En un futuro", "No")))),
        _radios("¿Presurizador hidroneumático?", "hidroneumatico", _iguales("Sí", "No", "No sé")), columnas=2),
    cu.campo({"label": "Elementos existentes a considerar", "name": "elementos_existentes", "tipo": "area",
              "placeholder": "Bardas, árboles, construcciones, pendientes del terreno..."}),
)
PASO_3 = (
    _casillas("¿Cómo usará principalmente el jardín?", "uso",
              (("Convivencia familiar", "Convivencia"), ("Descanso", "Descanso"), ("Juego de niños", "Niños"),
               ("Mascotas", "Mascotas"), ("Asados / reuniones", "Asados"), ("Imagen / fachada", "Imagen"),
               ("Solo estético", "Estético"))),
    _casillas("Estilo que le atrae", "estilo",
              (("Tropical", "Tropical"), ("Minimalista", "Minimalista"), ("Mediterráneo", "Mediterráneo"),
               ("Japonés / zen", "Zen"), ("Colorido", "Colorido"), ("Natural", "Natural"),
               ("Sin preferencia", "Sin preferencia"))),
    cu.fila(_radios("¿Prefiere árboles o palmas?", "arboles_palmas", _iguales("Árboles", "Palmas", "Ambos", "Ninguno")),
            _radios("Nivel de mantenimiento", "mantenimiento",
                    (("Bajo mantenimiento", "Fácil"), ("Moderado", "Moderado"), ("Me da igual", "Me da igual"))), columnas=2),
    cu.campo({"label": "Plantas que le gustan o quiere incluir", "name": "plantas_preferencia", "tipo": "area",
              "placeholder": "Ej. buganvilias, helechos, palmeras, cactus — cualquier planta que tenga en mente..."}),
    cu.fila(cu.campo({"label": "Elementos o plantas a conservar", "name": "conservar", "tipo": "area",
                      "placeholder": "Árboles existentes, macetas, fuentes, pérgolas..."}),
            cu.campo({"label": "Fotos de referencia", "name": "referencias", "tipo": "area",
                      "placeholder": "Link de Pinterest / Instagram o descripción de lo que le gustó..."}), columnas=2),
)
PRESUPUESTOS = (("$5,000–$15,000 MXN", "$5,000 – $15,000 MXN", "Proyecto básico con plantas y detalles"),
                ("$15,000–$40,000 MXN", "$15,000 – $40,000 MXN", "Proyecto medio con plantas y piso"),
                ("$40,000–$80,000 MXN", "$40,000 – $80,000 MXN", "Proyecto completo con instalaciones"),
                ("$80,000 MXN+", "$80,000 MXN en adelante", "Proyecto ejecutivo / premium"))
PASO_4 = (
    cu.opciones({"legend": "Inversión aproximada", "tipo": "radio", "name": "presupuesto_ejecucion", "clase_grupo": "vt-pills vt-pills--tarjetas",
                 "items": tuple((v, f"<b>{m}</b><small>{d}</small>") for v, m, d in PRESUPUESTOS)}),
    _radios("¿Cuándo le gustaría iniciar la ejecución?", "fecha_inicio",
            (("Lo antes posible", "Lo antes posible"), ("1–3 meses", "1–3 meses"), ("3–6 meses", "3–6 meses"),
             ("Más de 6 meses", "Más de 6 meses"), ("Solo el diseño por ahora", "Solo el diseño"))),
)
PASO_5 = (
    _radios("¿Cuál es su mayor prioridad?", "prioridad",
            _iguales("Que se vea increíble", "Que sea funcional", "Fácil de mantener", "Valor a la propiedad")),
    cu.campo({"label": "¿Algo más que debamos saber?", "name": "observaciones", "tipo": "area",
              "placeholder": "Ideas especiales, limitaciones del terreno, preguntas... todo suma para el diseño."}),
)
CONTENIDO = {
    "tipo": "utilidad", "vista": "cuestionario", "scripts": ("/js/vt-cuestionario.js",),
    "meta": {"title": "Cuestionario de Proyecto — Viveros Terra", "description": DESCRIPCION, "robots": "noindex, follow",
             "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Diseño de jardines", "h1": 'Tu jardín empieza aquí. <span class="vt-serif">Cuéntanos tu visión.</span>',
               "lede": f"Tómate 4 minutos para contarnos qué necesitas. Nuestro diseñador creará una propuesta hecha exactamente para ti; {datos.PROMESA.lower().replace('respondemos', 'te respondemos')}.",
               "aviso": f"{datos.VISITA_COSTO_CORTO} · Diseño personalizado · 4-5 minutos",
               "foto": {"src": "/img/diseno-jardin-instalacion-plantas-tampico.webp", "ancho": 1400, "alto": 787, "alt": ""}},
    "form": {"accion": f"https://formsubmit.co/ajax/{datos.CORREO_FORMULARIOS}",
             "ocultos": (("_subject", "Nuevo cuestionario de jardín — Viveros Terra"), ("_template", "table"), ("_captcha", "false")),
             "pasos": (
                 {"corto": "Tus datos", "titulo": "Cuéntanos de ti", "pista": "Para coordinar tu visita técnica y enviarte la propuesta de diseño.", "controles": PASO_1},
                 {"corto": "Tu espacio", "titulo": "Tu espacio", "pista": "No te preocupes si no tienes las medidas exactas — las tomamos en la visita.", "controles": PASO_2},
                 {"corto": "Estilo", "titulo": "Tu estilo y gustos", "pista": "Entre más nos cuentes, más personalizado será tu diseño.", "controles": PASO_3},
                 {"corto": "Inversión", "titulo": "Inversión estimada", "pista": "Esta info es solo para proponer opciones reales — no te compromete a nada.", "controles": PASO_4},
                 {"corto": "Final", "titulo": "¡Ya casi! Una última pregunta", "pista": "Esto nos ayuda a priorizar lo que más le importa en el diseño.", "controles": PASO_5},
             )},
    "exito": {"titulo": "¡Gracias por tu información!", "texto": f"Hemos recibido tu cuestionario. Un diseñador de Viveros Terra {datos.PROMESA.lower().replace('respondemos', 'te responde')} para coordinar tu visita técnica. {datos.VISITA_COSTO}",
              "boton": "También puedes escribirnos por WhatsApp", "mensaje": mensajes_paginas.UTILITARIAS["cuestionario_enviado"]},
    "fecha": "14 de mayo, 2026", "fecha_iso": "2026-05-14",
}
PARIDAD = {"reemplazos": {"Tu jardín empieza aquí": "Tu jardín empieza aquí. Cuéntanos tu visión.",
                          "Tu jardín empieza aquí. Cuéntanos tu visión.": "Tu jardín empieza aquí. Cuéntanos tu visión."},
           "retirados": {},
           "meta": {"description": (DESCRIPCION, "La página no tenía descripción y publicaba una meta vacía."),
                    "canonical": (URL, "Spec §3.5: el cuestionario lleva noindex, follow y canonical; no tenía canonical.")},
           "jsonld": {}}
