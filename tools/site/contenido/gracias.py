"""Contenido de /gracias: destino de los 7 formularios por correo (_next de formsubmit). GA4 la cuenta por su URL y su
page_view; no tiene evento propio. El archivo, la URL, el título, robots, canonical y data-cta no cambian."""
import datos
import mensajes_paginas

URL = f"{datos.SITIO}/gracias"
CONTENIDO = {
    "tipo": "utilidad", "vista": "gracias",
    "meta": {"title": "¡Gracias! Tu cotización está en camino · Viveros Terra",
             "description": "Recibimos tu solicitud. Respondemos en menos de 1 hora en horario con tu cotización detallada por correo y WhatsApp.",
             "robots": "noindex, follow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Solicitud recibida", "h1": "¡Recibimos tu cotización!",
               "lede": f"<strong>{datos.PROMESA}</strong> · {datos.HORARIO}."},
    "siguientes": {"titulo": "Qué sigue ahora", "items": (
        f"<strong>{datos.PROMESA.replace('Respondemos en menos', 'En menos')}</strong> "
        "te escribimos por WhatsApp o correo con tu cotización.",
        f"<strong>Si hace falta,</strong> agendamos contigo una visita para medir. {datos.VISITA_COSTO}",
        "<strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.")},
    "adelanto": {"texto": "¿Prefieres adelantar y hablar ahora?", "mensaje": mensajes_paginas.UTILITARIAS["gracias"]},
    "mientras": ('<strong>Mientras tanto:</strong> revisa nuestro <a href="/catalogo">catálogo de plantas</a> o el '
                 '<a href="/blog">blog</a> con guías para el clima de Tampico.'),
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
