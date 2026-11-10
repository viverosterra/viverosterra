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
               "vacio": "No encontramos eso en el sitio. Dinos qué buscas por WhatsApp y te decimos si lo manejamos."},
    # (texto, ruta, palabras que también la encuentran en el buscador)
    "servicios": (
        ("Pasto en rollo San Agustín", "/pasto-en-rollo-tampico", "cesped natural jardineria cotizar"),
        ("Pasto sintético en Tampico", "/pasto-sintetico-tampico", "cesped artificial cotizar"),
        ("Tienda de pasto sintético", "/pasto-sintetico", "cesped artificial comprar envio"),
        ("Diseño de jardines", "/diseno-jardines-tampico", "jardineria proyecto paisajismo cotizar"),
        ("Mantenimiento de jardines", "/mantenimiento-jardines-tampico", "jardineria jardinero poda cotizar"),
        ("Jardinería en Altamira", "/jardineria-altamira", "altamira jardinero mantenimiento cotizar"),
        ("Sistemas de riego", "/sistema-riego-tampico", "aspersores goteo jardineria cotizar"),
        ("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico", "vivero ornamentales jardineria"),
        ("Plantas de interior", "/plantas-de-interior-tampico", "interiores casa oficina macetas"),
        ("Arma tu lista de plantas", "/catalogo", "catalogo cotizar vivero"),
        # Entrega B de experiencia: "nochebuena" y "palma real" no encontraban nada (Nochebuenas no estaba en la lista).
        ("Nochebuenas", datos.NOCHEBUENAS["ruta"], "nochebuena nochebuenas flor de pascua navidad temporada mayoreo"),
        ("Palmas tropicales", "/palmas-tropicales-tampico", "palma palmera palma real areca coco plumoso"),
        ("Palmas para proyectos", "/palmas-mayoreo-proyectos", "palmas mayoreo obra empresas"),
        ("Tierra negra", "/tierra-negra-vegetal-tampico", "materiales sustrato abono cotizar"),
        ("Tezontle rojo", "/tezontle-rojo-tampico", "materiales piedra volcanica cotizar"),
        ("Mármol blanco", "/marmol-blanco-tampico", "materiales piedra decorativa cotizar"),
        ("Piedra bola de río", "/piedra-bola-rio-tampico", "materiales canto rodado cotizar"),
        ("Mayoreo de pasto", "/mayoreo-pasto-tampico", "obra constructoras volumen cotizar"),
        ("Precios", "/precios", "costos lista cotizar cuanto cuesta"),
        ("Visita el vivero", "/vivero-tampico", "direccion horario como llegar madero ubicacion"),
        ("Blog", "/blog", "consejos guias cuidados"),
    ),
    "cierre": {"titulo": "¿No lo encuentras?", "lede": "Cuéntanos qué necesitas.", "mensaje": mensajes_paginas.UTILITARIAS["no_encontrada"]},
}
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {}}
# Lo que cambia en los CTA y el recorrido frente a la captura (encabezados, precios y enlaces: tests/test_paridad.py).
PARIDAD["cta"] = 'Entrega B de experiencia (2026-11-10), CTA y recorrido: el buscador encuentra Nochebuenas, palmas y palmas para proyectos; aviso sin coincidencias reescrito.'
