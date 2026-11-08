"""Contenido de las 6 páginas de zona /jardineria-*. Solo datos: la plantilla es plantillas/zona.py.

Colonias, municipios y códigos postales verificados con directorios SEPOMEX (septiembre 2026); textos de cada zona
(entrada, lo que pide un jardín ahí y preguntas) los de main (tools/pasto/zonas.py hasta la Etapa 2g), con los precios de
datos.py. Reglas del dueño: solo hechos locales reales; sin casos, opiniones, distancias ni tiempos de llegada inventados
(main decía "A minutos del vivero" en Madero: queda la dirección). Un caso real por zona entra solo con permiso del
dueño (ninguno confirmado). Las frecuencias de visita son las del dueño (datos.FRECUENCIAS_MANTENIMIENTO). Las fotos son las de main, una por zona, sin cambiar; el pie ya no dice que la foto es de la
zona. El contenido único por zona y la consolidación de títulos son de la Etapa 3. PARIDAD: tests/test_paridad.py.
"""
from types import SimpleNamespace

import datos
import mensajes_paginas
from componentes import dinero
from contenido import lista_precios
from contenido import materiales_comun as mc

P = datos.PRECIOS
SITE = datos.SITIO
TIPO = "zona"
NEGOCIO = {"@id": f"{SITE}/#negocio"}
PORTADAS = "/img/portadas"
INSTALADO = dinero(P["pasto_instalado_m2"])
MANTENIMIENTO = dinero(P["mantenimiento_mes"])
RIEGO = f"{dinero(P['riego_m2'][0])} a {dinero(P['riego_m2'][1])}"

# Las fotos de main (una por zona) con un alt y un pie que no dicen en qué colonia se tomaron (no se sabe): los mismos de
# la página de servicio que publica esa foto, o, si solo la usa la zona, el alt de main. (archivo, ancho, alto, alt,
# lugar, etapa)
FOTOS = {
    "jardineria-lomas-de-rosales-tampico": ("diseno-jardines-tampico-proyecto", 960, 1574,
                                            "Jardín residencial diseñado por Viveros Terra en Tampico", "Tampico",
                                            "Terminado"),
    "jardineria-country-club-tampico": ("jardin-residencial-tropical-tampico", 960, 640,
                                        "Jardín residencial con plantas tropicales en Tampico",
                                        "Jardín con plantas tropicales", "Tampico"),
    "jardineria-aguila-tampico": ("mantenimiento-jardines-poda-pasto-tampico", 960, 1440,
                                  "Jardinero de Viveros Terra podando pasto en un jardín de Tampico", "Poda de pasto",
                                  "Tampico"),
    "jardineria-lomas-del-chairel-tampico": ("riego-pro-01", 960, 640,
                                             "Aspersores de riego automático funcionando en un jardín",
                                             "Sistema de riego por aspersión", "Instalado"),
    "jardineria-ciudad-madero": ("diseno-jardines-madero-altamira-pasto", 960, 640,
                                 "Jardín con pasto San Agustín atendido por Viveros Terra", "Pasto San Agustín",
                                 "Jardín atendido"),
    "jardineria-altamira": ("jardineria-areas-verdes-tampico", 793, 1190,
                            "Áreas verdes con pasto San Agustín atendidas por Viveros Terra", "Áreas verdes",
                            "Jardín atendido"),
}

ZONAS = {
    "jardineria-lomas-de-rosales-tampico": dict(
        nombre="Lomas de Rosales", municipio="Tampico", corto="Lomas de Rosales",
        title="Jardinería en Lomas de Rosales, Tampico: pasto, diseño y mantenimiento",
        h1="Jardinería en Lomas de Rosales", accent="y Vista Hermosa, Tampico",
        colonias=(("Lomas de Rosales", "89100"), ("Lomas de la Aurora", "89100"), ("Vista Hermosa", "89119")),
        lede=("Pasto en rollo, diseño, riego y mantenimiento para las casas de Lomas de Rosales, Lomas de la Aurora y "
              "Vista Hermosa, en Tampico."),
        servicios=("pasto", "diseno", "riego", "mantenimiento"),
        retos=(
            ("Terrenos en pendiente", "En la loma el agua de riego y de lluvia escurre. El riego por goteo y las "
             "jardineras escalonadas evitan que se lave la tierra y el pasto se seque en la parte alta."),
            ("Lotes amplios", "Jardines grandes piden un plan de mantenimiento fijo. Con visitas más seguidas en "
             "lluvias y mensuales en secas, el pasto se mantiene parejo."),
            ("Sol fuerte en la parte alta", "Para las zonas más expuestas conviene pasto San Agustín y palmas de sol "
             "pleno como coco plumoso o washingtonia."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en Lomas de Rosales?",
             "Sí. Atendemos Lomas de Rosales, Lomas de la Aurora y Vista Hermosa en Tampico con instalación de pasto, "
             "diseño, riego y mantenimiento. Mándanos tu colonia y los metros aproximados y te cotizamos."),
            ("¿Cuánto cuesta el mantenimiento de jardín en Lomas de Rosales?",
             f"Desde {MANTENIMIENTO} al mes. El precio final depende de los metros del jardín y de la frecuencia de "
             "visitas."),
            ("¿Qué riego conviene en un jardín con pendiente?",
             "Goteo en jardineras y aspersión de bajo caudal en el pasto, con zonas separadas para la parte alta y la "
             "baja. Así el agua no escurre y se aprovecha mejor."),
        ),
    ),
    "jardineria-country-club-tampico": dict(
        nombre="Club Campestre y Country Club", municipio="Tampico", corto="Club Campestre",
        title="Jardinería en Club Campestre y Country Club, Tampico",
        h1="Jardinería en Club Campestre", accent="y Country Club, Tampico",
        colonias=(("Club Campestre", "89217"), ("Country Club", "89218"), ("Sierra Morena", "89210")),
        lede=("Instalación de pasto, diseño de jardín, riego automático y mantenimiento para las casas de Club "
              "Campestre, Country Club y Sierra Morena, en Tampico."),
        servicios=("riego", "pasto", "mantenimiento", "diseno"),
        retos=(
            ("Jardines grandes", "En lotes amplios, el riego automático por zonas ahorra agua y tiempo. Lo diseñamos "
             "según el pasto, las jardineras y la presión de tu casa."),
            ("Pasto parejo todo el año", "El pasto San Agustín necesita poda frecuente en lluvias y fertilización por "
             "temporada. Un plan mensual evita que se amarille en secas."),
            ("Palmas y árboles grandes", "Palmas y árboles de porte con garantía de arraigo de 30 días en los que sembramos "
             'nosotros, con el riego indicado (<a href="/politicas#garantia-plantas">ver condiciones</a>).'),
        ),
        faqs=(
            ("¿Atienden jardines en Club Campestre y Country Club?",
             "Sí. Atendemos Club Campestre, Country Club y Sierra Morena en Tampico con pasto en rollo, diseño, riego "
             "automático y mantenimiento."),
            ("¿Cuánto cuesta un sistema de riego automático?",
             f"De {RIEGO} por m², según el tipo de sistema. Medimos y revisamos la presión en la visita."),
            ("¿Pueden encargarse del jardín todo el año?",
             f"Sí. El mantenimiento cuesta desde {MANTENIMIENTO} al mes; la frecuencia la fijamos contigo según tu plan y "
             f"lo que necesita tu jardín: {lista_precios.FRECUENCIAS}."),
        ),
    ),
    "jardineria-aguila-tampico": dict(
        nombre="Águila, Altavista y Petrolera", municipio="Tampico", corto="Águila y Altavista",
        title="Jardinería en Águila, Altavista y Petrolera, Tampico",
        h1="Jardinería en Águila,", accent="Altavista y Petrolera, Tampico",
        colonias=(("Águila", "89230"), ("Altavista", "89240"), ("Petrolera", "89110"), ("Campbell", "89260")),
        lede=("Pasto, poda de árboles, diseño y mantenimiento para las casas de Águila, Altavista, Petrolera y "
              "Campbell, en Tampico."),
        servicios=("poda", "pasto", "mantenimiento", "diseno"),
        retos=(
            ("Árboles grandes y sombra", "Son colonias con árboles maduros. El pasto San Agustín aguanta media sombra, "
             "pero bajo copas cerradas conviene plantas de sombra o cubresuelos."),
            ("Jardines de frente y patios", "En espacios medianos, un diseño sencillo con pasto, jardineras y dos o "
             "tres palmas da más orden y menos mantenimiento."),
            ("Poda y raíces", "Podamos árboles y palmas con técnica para no dañarlos. Si una raíz levanta la banqueta, "
             "te recomendamos especies de raíz controlada."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en la colonia Águila y Altavista?",
             "Sí. Atendemos Águila, Altavista, Petrolera y Campbell en Tampico con pasto en rollo, poda, diseño y "
             "mantenimiento."),
            ("¿El pasto San Agustín crece en sombra?",
             "Aguanta media sombra, con unas 4 horas de sol directo. Bajo árboles muy cerrados te recomendamos plantas "
             "de sombra o cubresuelos."),
            ("¿Cuánto cuesta poner pasto en el frente de mi casa?",
             f"El pasto San Agustín instalado cuesta desde {INSTALADO}/m² con preparación básica del suelo. Solo el "
             f"pasto cuesta {dinero(P['pasto_solo_m2'])}/m²."),
        ),
    ),
    "jardineria-lomas-del-chairel-tampico": dict(
        nombre="Lomas del Chairel", municipio="Tampico", corto="Lomas del Chairel",
        title="Jardinería en Lomas del Chairel y Colinas de San Gerardo, Tampico",
        h1="Jardinería en Lomas del Chairel", accent="y Colinas de San Gerardo",
        colonias=(("Lomas del Chairel", "89360"), ("Colinas de San Gerardo", "89367"), ("Flamboyanes", "89330")),
        lede=("Pasto en rollo, riego, diseño y mantenimiento para las casas cerca de la laguna del Chairel: Lomas del "
              "Chairel, Colinas de San Gerardo y Flamboyanes."),
        servicios=("riego", "pasto", "diseno", "mantenimiento"),
        retos=(
            ("Humedad y lluvias", "Cerca de la laguna el suelo tarda más en secar. Un buen drenaje y tierra bien "
             "preparada evitan hongos y encharcamientos en el pasto."),
            ("Casas nuevas", "En fraccionamientos recientes el suelo suele ser de relleno. Antes del pasto conviene una "
             "capa de tierra negra vegetal."),
            ("Mosquitos y agua estancada", "Revisamos que el riego no deje charcos y que las macetas y jardineras "
             "drenen bien."),
        ),
        faqs=(
            ("¿Atienden jardines en Lomas del Chairel y Colinas de San Gerardo?",
             "Sí. Atendemos Lomas del Chairel, Colinas de San Gerardo y Flamboyanes en Tampico con pasto, riego, diseño "
             "y mantenimiento."),
            ("¿Qué hago si mi jardín se encharca?",
             "Revisamos el nivel del terreno y el drenaje. A veces basta con nivelar y mejorar la tierra; en otros "
             "casos hace falta un dren. Lo revisamos contigo en tu jardín."),
            ("¿Necesito tierra negra antes de poner pasto?",
             f"En casas nuevas con suelo de relleno, sí. La tierra negra vegetal cuesta "
             f"{dinero(P['tierra_negra_costal'])} el costal o {dinero(P['tierra_negra_m3'])} el m³."),
        ),
    ),
    "jardineria-ciudad-madero": dict(
        nombre="Ciudad Madero", municipio="Ciudad Madero", corto="Cd. Madero",
        title="Jardinería en Ciudad Madero y Playa Miramar: pasto, diseño y mantenimiento",
        h1="Jardinería en Ciudad Madero", accent="y Playa Miramar",
        colonias=(("Playa Miramar", "89506"), ("Jardín 20 de Noviembre", "89440"), ("Residencial del Parque", "89514"),
                  ("Ampliación Unidad Nacional", "89510")),
        lede=("Nuestro vivero está en Ciudad Madero. Instalamos pasto, diseñamos y damos mantenimiento en Playa "
              "Miramar, Jardín 20 de Noviembre y el resto de la ciudad."),
        servicios=("pasto", "palmas", "diseno", "mantenimiento"),
        kicker_sin_cp=True,
        retos=(
            ("Brisa y salitre cerca de la playa", "En Miramar el viento trae sal. Recomendamos plantas y palmas que la "
             "toleran, como coco plumoso, washingtonia y cubresuelos costeros."),
            ("Suelo arenoso", "La arena retiene poca agua y pocos nutrientes. Mejoramos el suelo con tierra negra y "
             "ajustamos el riego y la fertilización."),
            # Main decía "A minutos del vivero": sin distancias ni tiempos (regla del dueño); queda la dirección.
            ("El vivero está en Ciudad Madero", f"Estamos en {datos.CALLE}, {datos.COLONIA}, frente a Walmart. Puedes "
             "venir a escoger tus plantas."),
        ),
        faqs=(
            ("¿Dónde está el vivero de Viveros Terra en Madero?",
             f"En {datos.CALLE}, {datos.COLONIA}, {datos.CP} Cd. Madero, frente a Walmart. {datos.HORARIO}."),
            ("¿Qué plantas aguantan la brisa de Playa Miramar?",
             "Coco plumoso, washingtonia, uva de mar y plantas de hoja gruesa toleran el salitre. Te decimos cuáles "
             "según qué tan cerca estés del mar."),
            ("¿Cuánto cuesta el pasto en rollo en Madero?",
             f"El pasto San Agustín cuesta {dinero(P['pasto_solo_m2'])}/m² solo el pasto y desde {INSTALADO}/m² "
             f"instalado, con garantía de arraigo de {datos.ARRAIGO}."),
        ),
    ),
    "jardineria-altamira": dict(
        nombre="Altamira", municipio="Altamira", corto="Altamira",
        title="Jardinería en Altamira y Lagunas de Miralta: pasto, diseño y mantenimiento",
        h1="Jardinería en Altamira", accent="y Lagunas de Miralta",
        colonias=(("Residencial Lagunas de Miralta", "89605"), ("Altamira Centro", "89600")),
        lede="Pasto en rollo, diseño, riego y mantenimiento para Residencial Lagunas de Miralta y el resto de Altamira.",
        servicios=("pasto", "riego", "mantenimiento", "diseno"),
        retos=(
            ("Jardines de fraccionamiento", "En fraccionamientos cerrados coordinamos horarios y acceso con la "
             "administración para instalar y dar mantenimiento."),
            ("Áreas verdes amplias", "Para jardines grandes, el riego automático por zonas y un plan de mantenimiento "
             "mensual mantienen el pasto parejo."),
            ("Casas nuevas", "Si tu casa es nueva, preparamos el suelo con tierra negra antes de instalar el pasto para "
             f"que arraigue en {datos.ARRAIGO}."),
        ),
        faqs=(
            ("¿Dan servicio de jardinería en Lagunas de Miralta?",
             "Sí. Atendemos Residencial Lagunas de Miralta y el resto de Altamira con pasto, diseño, riego y "
             "mantenimiento."),
            ("¿Cuánto cuesta el mantenimiento de jardín en Altamira?",
             f"Desde {MANTENIMIENTO} al mes. El precio depende de los metros y de la frecuencia de visitas."),
            ("¿Atienden empresas en el puerto industrial de Altamira?",
             f"Sí. Tenemos REPSE {datos.REPSE} y factura {datos.FACTURA} para contratos de mantenimiento de áreas "
             'verdes. Ve el <a href="/mantenimiento-jardines-tampico">servicio de mantenimiento</a>.'),
        ),
    ),
}
CLAVES = tuple(ZONAS)


def _foto(slug):
    archivo, ancho, alto, alt, lugar, etapa = FOTOS[slug]
    return {"src": f"{PORTADAS}/{archivo}-sm.webp",
            "srcset": f"{PORTADAS}/{archivo}-sm.webp 560w, {PORTADAS}/{archivo}.webp {ancho}w",
            "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": ancho, "alto": alto, "numero": 1, "alt": alt,
            "lugar": lugar, "etapa": etapa}


def _otras(slug):
    return tuple((nombre, ruta) for nombre, ruta in datos.ZONAS if ruta != f"/{slug}")


def contenido(slug):
    z = ZONAS[slug]
    url = f"{SITE}/{slug}"
    corto = z["corto"]
    mensaje = mensajes_paginas.ZONAS[f"/{slug}"]
    descripcion = (f"{z['lede']} Pasto instalado desde {INSTALADO}/m², mantenimiento desde {MANTENIMIENTO}/mes. "
                   "Cotiza por WhatsApp.")
    titulo = f"{z['title']} · Viveros Terra"
    imagen = f"{SITE}{PORTADAS}/{FOTOS[slug][0]}.webp"
    cps = " · ".join(sorted({cp for _c, cp in z["colonias"]}))
    preguntas = z["faqs"]
    return {
        "tipo": TIPO,
        "meta": {
            "title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
            "canonical": url,
            "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                   ("og:description", descripcion), ("og:image", imagen), ("og:locale", "es_MX")),
            "twitter": (("twitter:card", "summary_large_image"),),
        },
        "migas": (("Inicio", "/"), (f"Jardinería en {z['nombre']}", None)),
        "portada": {
            "compacta": True,
            "kicker": f"{z['municipio']}, Tamaulipas" + ("" if z.get("kicker_sin_cp") else f" · CP {cps}"),
            "h1": f'{z["h1"]} <span class="vt-serif">{z["accent"]}</span>',
            "lede": z["lede"],
            "etiqueta": {"codigo": f"Zona · {corto}", "aviso": "Con IVA", "nombre": "Pasto instalado",
                         "antes": "San Agustín instalado · desde", "monto": INSTALADO, "unidad": "/m²",
                         "filas": (("Mantenimiento", f"desde {MANTENIMIENTO}/mes"),
                                   ("Diseño", f"desde {dinero(P['diseno'])}"))},
            "mensaje": mensaje,
            "tambien": f'{datos.VISITA_COSTO_CORTO} · <a href="#precios">servicios y precios</a>',
            "foto": _foto(slug),
        },
        "precios": {
            "titulo": 'Servicios y precios <span class="vt-serif">con IVA</span>',
            "lede": f"Lo que hacemos en {corto}, con el precio de la lista oficial.",
            "filas": lista_precios.filas_zona(z["servicios"], f"/{slug}"), "caption": f"Precios {datos.ANIO} con IVA.",
            "cotizar": (f"Cotizar en {corto}", mensaje),
            "nota": datos.ANTICIPO,
        },
        "retos": {"titulo": 'Lo que pide un jardín <span class="vt-serif">en esta zona</span>',
                  "items": tuple({"titulo": t, "texto": x} for t, x in z["retos"])},
        "colonias": {"titulo": f'Colonias que atendemos <span class="vt-serif">en {corto}</span>',
                     "lede": "Si tu colonia está cerca y no aparece, también te atendemos.",
                     "items": z["colonias"], "municipio": z["municipio"]},
        "faq": {"titulo": f'Preguntas frecuentes <span class="vt-serif">en {corto}</span>', "preguntas": preguntas},
        "cobertura": {"titulo": "Otras zonas donde trabajamos",
                      "lede": "También trabajamos en estas zonas.",
                      "zonas": _otras(slug), "por_proyecto": datos.ZONAS_POR_PROYECTO},
        "cierre": {"titulo": f'Cotiza tu jardín <span class="vt-serif">en {corto}</span>',
                   "lede": ("Mándanos tu colonia, el servicio que necesitas, los metros aproximados y una foto. "
                            f"{datos.PROMESA} y, si hace falta, agendamos una visita para medir. {datos.VISITA_COSTO} "
                            'O <a href="/vivero-tampico">visita el vivero</a>.'),
                   "mensaje": mensaje},
        "jsonld": {
            "migas": {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": f"Jardinería en {z['nombre']}", "item": url}]},
            "servicio": {
                "@type": "Service", "@id": f"{url}#servicio", "name": f"Jardinería en {z['nombre']}",
                "serviceType": "Jardinería, pasto en rollo, diseño y mantenimiento de jardines", "provider": NEGOCIO,
                "areaServed": [{"@type": "Place", "name": f"{c}, {z['municipio']}, Tamaulipas",
                                "address": {"@type": "PostalAddress", "addressLocality": z["municipio"],
                                            "postalCode": cp, "addressRegion": "Tamaulipas", "addressCountry": "MX"}}
                               for c, cp in z["colonias"]],
                "offers": mc.oferta(f"{url}#precios", "m²", desde=P["pasto_instalado_m2"],
                                    nombre="Pasto San Agustín instalado"),
            },
        },
    }


MOTIVO_AGGREGATE = ("AggregateOffer no admite unitText: el “desde” por m² pasa a Offer con UnitPriceSpecification y minPrice, "
                    "con el mismo precio de datos.py.")


def paridad(slug):
    """Madero: "A minutos del vivero" pasa a "El vivero está en Ciudad Madero" (sin distancias ni tiempos)."""
    reemplazos = {"A minutos del vivero": "El vivero está en Ciudad Madero"} if slug == "jardineria-ciudad-madero" else {}
    motivo = "Renglón que la zona ya no publica (solo sus 4 servicios principales): sigue en /precios, enlazada desde la tabla."
    servicios = ZONAS[slug]["servicios"]
    fuera = [P["sintetico_instalado_m2"][0]]  # el sintético no es de los 4 de ninguna zona
    fuera += [] if "palmas" in servicios else [P["palma_desde"]]
    fuera += [] if "riego" in servicios else list(P["riego_m2"])
    return {"reemplazos": reemplazos, "retirados": {dinero(n): motivo for n in fuera},
            "jsonld": {"AggregateOffer": MOTIVO_AGGREGATE}}


def pagina(slug):
    return SimpleNamespace(CONTENIDO=contenido(slug), PARIDAD=paridad(slug))
