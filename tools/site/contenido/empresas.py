"""Contenido de /empresas (SEO fase 2a, 2026-11-11; mapa de palabras clave §3a, fila 2, y clúster 6 de §4b): el pilar
de áreas verdes para empresas e industria. Solo datos: la plantilla es tools/site/plantillas/pilar.py.

Solo hechos de datos.py y de las páginas para empresas que ya existen (contenido/b2b_comun.py): REPSE con su padrón
público, factura, +200 proyectos B2B, los clientes con permiso del dueño, el anticipo de proyectos, el plan empresa de
mantenimiento «según cotización» y desde 2007. Las opiniones son las reales de empresas que ya publica el sitio. Sin
plazos, capacidades ni escalas que el dueño no haya dado. Hijos del pilar: mayoreo de pasto, palmas para proyectos,
mantenimiento, riego y la zona Altamira. Página nueva: sin captura de paridad. El 301 viejo
/jardineria-puerto-industrial-altamira apunta aquí (vercel.json).
"""
import datos
import entidad
import mensajes_paginas
from componentes import dinero
from contenido import b2b_comun
from contenido import respuestas

P = datos.PRECIOS
SITE = datos.SITIO
RUTA = "/empresas"
URL = f"{SITE}{RUTA}"
MENSAJE = mensajes_paginas.SEO_F2A[RUTA]
SEGUN = datos.SEGUN_COTIZACION

TITULO = f"Áreas Verdes para Empresas e Industria | {datos.NOMBRE}"
DESCRIPCION = (f"Mantenimiento de áreas verdes, pasto al mayoreo, palmas y riego para empresas en Tampico y Altamira. "
               f"REPSE {datos.REPSE} y factura {datos.FACTURA}.")
FOTO = {"src": "/img/obra/riego-tecnico-sistema-industrial.webp", "ancho": 960, "alto": 640, "numero": 1,
        "sizes": "(min-width: 1024px) 560px, 100vw",
        # El alt y el pie que la foto ya lleva en /sistema-riego-tampico.
        "alt": "Técnico de Viveros Terra revisando aspersores en el área verde de una planta industrial.",
        "lugar": "Riego en una planta industrial", "etapa": "Prueba y calibración"}
META = {
    "title": TITULO, "description": DESCRIPCION, "robots": "index, follow", "canonical": URL,
    "og": (("og:type", "website"), ("og:title", TITULO), ("og:description", DESCRIPCION),
           ("og:image", f"{SITE}{FOTO['src']}"), ("og:locale", "es_MX")),
    "twitter": (("twitter:card", "summary_large_image"), ("twitter:title", TITULO),
                ("twitter:description", DESCRIPCION)),
}
ALTAMIRA = {"titulo": "Jardinería en Altamira", "href": "/jardineria-altamira",
            "img": "/img/portadas/jardineria-areas-verdes-tampico-sm.webp", "ancho": 560, "alto": 840,
            "texto": "Casas y empresas de Altamira y Lagunas de Miralta"}
HIJOS = b2b_comun.PAGINAS + (ALTAMIRA,)
OPINIONES = (datos.OPINIONES_MANTENIMIENTO[1], datos.OPINIONES_RIEGO[1], datos.OPINIONES_PASTO_EN_ROLLO[1])
PREGUNTAS = (
    b2b_comun.PREGUNTA_REPSE,
    ("¿Facturan?", f"Sí: factura {datos.FACTURA} para persona física o moral. Solo necesitamos tu RFC y tus datos fiscales."),
    b2b_comun.PREGUNTA_PAGO,
    ("¿Cuánto cuesta el mantenimiento de áreas verdes para una empresa?",
     f"El plan empresa va {SEGUN.lower()}: depende de los m², la frecuencia y lo que incluye cada visita. Mándanos la "
     "ubicación y los m² aproximados y te mandamos la cotización por escrito."),
    ("¿Atienden empresas del puerto industrial de Altamira?",
     f"Sí. Atendemos empresas en Tampico, Ciudad Madero y Altamira; fuera de la zona, {datos.ZONAS_POR_PROYECTO}, "
     "por proyecto."),
    ("¿Venden pasto y palmas al mayoreo para obra?",
     f"Sí. Pasto San Agustín desde {dinero(P['pasto_mayoreo_m2'])}/m² en pedidos de {b2b_comun.MINIMO} m² o más (solo "
     'pasto; no lleva IVA), en <a href="/mayoreo-pasto-tampico">mayoreo de pasto</a>, y palmas por especie y altura en '
     '<a href="/palmas-mayoreo-proyectos">palmas para proyectos</a>.'),
    ("¿Puedo pedir la cotización por correo?",
     "Sí. Las páginas de mayoreo de pasto y de palmas para proyectos tienen un formulario para departamentos de "
     "compras; también puedes mandarnos el detalle por WhatsApp."),
)

CONTENIDO = {
    "respuesta": respuestas.de(RUTA),
    "tipo": "b2b",
    "meta": META,
    "migas": (("Inicio", "/"), ("Empresas", None)),
    "portada": {
        "kicker": "Empresas · Tampico, Madero y Altamira",
        "pos": "30% 45%", "pos_d": "24% 50%",
        "h1": "Áreas verdes para empresas e industria",
        "lema": "Un solo proveedor, con REPSE y factura.",
        "lede": ("Mantenimiento, pasto al mayoreo, palmas y riego para industria, constructoras, hoteles, comercios y "
                 "gobierno."),
        "mensaje": MENSAJE,
        "enlaces": (("Qué hacemos", "#servicios"),),
        "dato": f"REPSE {datos.REPSE} · {datos.PROYECTOS_B2B} proyectos B2B",
        "foto": FOTO,
    },
    "secciones": (
        {"clase": "tarjetas", "rotulo": "Servicios", "id": "vt-h-servicios", "ancla": "servicios",
         "titulo": "Lo que hacemos para empresas",
         "lede": (f"Un mismo proveedor para el pasto, las palmas, el riego y el mantenimiento. Plan empresa de "
                  f"mantenimiento {SEGUN.lower()}."),
         "items": HIJOS, "cta": (MENSAJE, "Cotizar para mi empresa")},
        {"clase": "clientes", "rotulo": "Clientes", "id": "vt-h-clientes", "ancla": "clientes",
         "titulo": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
         "lede": f"Clientes que nos dieron permiso de mostrar su nombre. Trabajamos con empresas desde {datos.DESDE}.",
         "titulo_opinion": "Lo que dicen las empresas", "opiniones": OPINIONES},
        {"clase": "fichas", "rotulo": "Documentación", "id": "vt-h-docs", "ancla": "documentacion",
         "titulo": "Documentación para compras", "lede": "Lo que suele pedir un departamento de compras.",
         "items": b2b_comun.DOCUMENTACION},
        {"clase": "cobertura", "rotulo": "Cobertura", "id": "vt-h-cobertura",
         "titulo": "Dónde y a quién atendemos",
         "lede": "Tampico, Ciudad Madero y Altamira; fuera de la zona conurbada, por proyecto.",
         **b2b_comun.COBERTURA, "cta": (MENSAJE, "Cotizar mi proyecto")},
    ),
    "faq": {"titulo": "Preguntas de compras", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "Cotiza el proyecto de tu empresa",
        "lede": ("Mándanos la empresa, la ubicación, el servicio y los m² aproximados. Para compras que piden la "
                 'cotización por escrito, hay formulario en <a href="/mayoreo-pasto-tampico#cotizacion-correo">mayoreo '
                 'de pasto</a> y en <a href="/palmas-mayoreo-proyectos#cotizacion-correo">palmas para proyectos</a>.'),
        "mensaje": MENSAJE,
    },
    "jsonld": {
        "speakable": entidad.SPEAKABLE,
        "nodos": (
            {"@type": "Service", "@id": f"{URL}#servicio", "name": "Áreas verdes para empresas e industria",
             "serviceType": "Mantenimiento de áreas verdes, pasto al mayoreo, palmas y riego para empresas",
             "provider": entidad.REF, "audience": {"@type": "BusinessAudience", "name": "Empresas e industria"},
             "areaServed": [{"@type": "City", "name": ciudad} for ciudad in entidad.CIUDADES]},
            {"@type": "ItemList", "name": "Servicios para empresas", "itemListElement": [
                {"@type": "ListItem", "position": n, "name": h["titulo"], "url": f"{SITE}{h['href']}"}
                for n, h in enumerate(HIJOS, 1)]},
        ),
    },
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
    "hero": ("Página nueva (SEO fase 2a, 2026-11-11): hero de marca como las páginas para empresas, con un solo botón de "
             "WhatsApp, el teléfono de enlace, la línea de confianza con el REPSE y sin etiqueta de precio (el plan "
             "empresa va según cotización); sin captura anterior que comparar."),
}
