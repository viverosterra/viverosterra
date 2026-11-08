"""Contenido de 404.html: lo que sirve Vercel en toda ruta sin archivo (hoy, 79 bytes de texto plano). noindex."""
import datos
import mensajes_paginas

URL = f"{datos.SITIO}/404"
CONTENIDO = {
    "tipo": "utilidad",
    "meta": {"title": "Página no encontrada · Viveros Terra",
             "description": "Esta página no existe. Encuentra pasto, plantas, jardinería y materiales en Viveros Terra.",
             "robots": "noindex, follow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Error 404", "h1": 'No encontramos <span class="vt-serif">esa página.</span>',
               "lede": "Puede que el enlace haya cambiado. Busca lo que necesitas aquí abajo o escríbenos."},
    "buscar": {"titulo": "¿Qué estás buscando?", "label": "Busca un servicio o producto", "placeholder": "Ej. pasto, palmas, riego",
               "vacio": "No hay coincidencias. Escríbenos por WhatsApp y te ayudamos."},
    "servicios": (("Pasto en rollo San Agustín", "/pasto-en-rollo-tampico"), ("Pasto sintético en Tampico", "/pasto-sintetico-tampico"),
                  ("Tienda de pasto sintético", "/pasto-sintetico"), ("Diseño de jardines", "/diseno-jardines-tampico"),
                  ("Mantenimiento de jardines", "/mantenimiento-jardines-tampico"), ("Sistemas de riego", "/sistema-riego-tampico"),
                  ("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico"), ("Arma tu lista de plantas", "/catalogo"),
                  ("Tierra negra", "/tierra-negra-vegetal-tampico"), ("Tezontle rojo", "/tezontle-rojo-tampico"),
                  ("Mármol blanco", "/marmol-blanco-tampico"), ("Piedra bola de río", "/piedra-bola-rio-tampico"),
                  ("Mayoreo de pasto", "/mayoreo-pasto-tampico"), ("Precios", "/precios"), ("Visita el vivero", "/vivero-tampico"), ("Blog", "/blog")),
    "cierre": {"titulo": "¿No lo encuentras?", "lede": "Cuéntanos qué necesitas.", "mensaje": mensajes_paginas.UTILITARIAS["no_encontrada"]},
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
