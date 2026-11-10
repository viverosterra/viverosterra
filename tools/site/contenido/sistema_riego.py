"""Contenido de /sistema-riego-tampico (riego automático para jardines, industria y campos deportivos con pasto
natural). Solo datos: la plantilla es tools/site/plantillas/servicio.py, con los 3 tipos de sistema (cada uno con su
mensaje), una sola sección de precio, la comparativa aspersión / goteo / microaspersión, un solo proceso de 5 pasos
(auditoría 02: antes había dos) y simulador de mensualidades.

Precio de datos.PRECIOS["riego_m2"] ($180 a $320/m²; el ejemplo de 100 m² sale de ahí) y ahorro de datos.RIEGO_AHORRO
("hasta 40%"). Los campos deportivos con pasto natural son un servicio real (decisión del dueño): la regla de no
deportes es solo del sintético. Título y descripción (también en Open Graph y Twitter Card): los de la fase 0 de SEO (contenido/seo.py).
Canonical, Service y migas como estaban publicados; FAQPage de las preguntas visibles y HowTo de los 5 pasos visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero, mensualidades
from contenido import seo

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/sistema-riego-tampico"
OBRA = "/img/obra"
RIEGO_MIN, RIEGO_MAX = P["riego_m2"]
EJEMPLO_M2 = 100
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
MENSAJE = mensajes_paginas.SERVICIOS["/sistema-riego-tampico"]
AHORRO = datos.RIEGO_AHORRO

TITULO = f"Sistema de Riego en Tampico: ${P['riego_m2'][0]} a ${P['riego_m2'][1]}/m² | Viveros Terra"
DESCRIPCION = ("Instalación de riego automático en Tampico, Madero y Altamira: aspersión, goteo o microaspersión con programador, "
               f"de ${P['riego_m2'][0]} a ${P['riego_m2'][1]}/m². Cotiza por WhatsApp.")
META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:title", TITULO),
        ("og:description", DESCRIPCION),
        ("og:image", f"{SITE}/img/tecnico-terra-riego-industrial-tampico.avif"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (
        ("twitter:card", "summary_large_image"),
        ("twitter:title", TITULO),
        ("twitter:description", DESCRIPCION),
        ("twitter:image", f"{SITE}/img/sistema-riego-automatizado-tampico.webp"),
    ),
}

SERVICIO = {
    "@type": "Service", "name": "Sistema de Riego Automático Tampico",
    "description": ("Instalación profesional de sistemas de riego automatizado para jardines residenciales, comerciales e "
                    "industriales en Tampico, Madero y Altamira, Tamaulipas. Aspersores emergentes, riego por goteo y "
                    "programadores digitales."),
    "provider": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
                 "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                             "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}},
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas", "Norte Veracruz"],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Sistema de Riego Tampico", "item": URL},
]}

SISTEMAS = (
    {"rotulo": "Sistema 1 · Pasto", "titulo": "Aspersores emergentes",
     "puntos": ("Cobertura uniforme de 2 a 15 m", "Ideal para pasto San Agustín", "Se ocultan en el suelo cuando no riegan"),
     "nota": "Para áreas de pasto: emergen al regar y cubren toda el área verde de forma pareja.",
     "mensaje": ("Hola, quiero cotizar riego con aspersores emergentes para mi pasto.\nColonia: ___\n"
                 "Metros aprox. del jardín: ___\nLes mando fotos del espacio.")},
    {"rotulo": "Sistema 2 · Plantas", "titulo": "Riego por goteo",
     "puntos": ("Lleva el agua directo a la raíz", "Ideal para plantas, arbustos, árboles y camellones",
                "Menos maleza: solo humedece donde hace falta"),
     "nota": "Para arriates y jardineras: la forma más eficiente de regar plantas ornamentales.",
     "mensaje": ("Hola, quiero cotizar riego por goteo para mis plantas.\nColonia: ___\nMetros aprox. de jardineras: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Sistema 3 · Grandes áreas", "titulo": "Industrial y deportivo",
     "puntos": ("Aspersores de largo alcance", "Controladores con varios programas",
                "De 500 m² hasta campos deportivos completos"),
     "nota": "Para parques industriales, escuelas, áreas de gobierno y campos deportivos con pasto natural.",
     "mensaje": ("Hola, quiero cotizar riego para un área grande.\nEmpresa o institución: ___\nUbicación: ___\n"
                 "m² aprox.: ___\nTipo de área (industrial, escuela, campo deportivo): ___")},
)

PREGUNTAS = (
    ("¿Cuánto cuesta instalar un sistema de riego automático en Tampico?",
     f"Entre {dinero(RIEGO_MIN)} y {dinero(RIEGO_MAX)} por m², según el tamaño del área, el tipo de sistema, el número de "
     f"zonas y la complejidad. Para cotizar, mándanos fotos y medidas aproximadas por WhatsApp al "
     f"{datos.TELEFONO_VISIBLE}; {datos.PROMESA[0].lower()}{datos.PROMESA[1:]}."),
    ("¿Cuánta agua ahorra un sistema de riego automático?",
     f"{AHORRO[0].upper()}{AHORRO[1:]} frente al riego manual. El ahorro viene de regar de madrugada (menos "
     "evaporación), evitar excesos y calibrar cada zona según el tipo de planta y la temporada."),
    ("¿Qué tipo de riego es mejor para jardines en Tampico?",
     "Para pasto San Agustín, los aspersores emergentes, por su cobertura pareja. Para plantas, arbustos y camellones, el "
     "goteo, que lleva el agua directo a la raíz y evapora menos. En jardines mixtos diseñamos sistemas combinados."),
    ("¿Cuánto tiempo tarda la instalación?",
     "Un sistema residencial de hasta 200 m² se instala en 1 a 2 días hábiles. Áreas industriales o campos deportivos "
     "pueden llevar de 3 a 7 días según la extensión. El jardín queda funcionando al terminar."),
    ("¿Funciona con la presión de agua de la red municipal?",
     "Sí. La mayoría de los sistemas residenciales funcionan con la presión normal de la red (1.5 a 4 bar). Si la presión "
     "es baja, se puede incluir una bomba pequeña en el diseño."),
    ("¿Dan garantía en la instalación?",
     "Sí. Garantizamos la instalación y los materiales: fugas o fallas por causas de la instalación, las atendemos. "
     "También damos mantenimiento preventivo y correctivo del sistema ya instalado."),
    ("¿Instalan riego para áreas comerciales e industriales en Tampico?",
     "Sí. Tenemos experiencia en parques industriales, escuelas, áreas verdes de gobierno y campos deportivos con pasto "
     "natural en Tampico, Altamira y Madero, con aspersores de largo alcance para grandes extensiones."),
    ("¿Qué marcas de aspersores y programadores instalan?",
     "Hunter, Rain Bird y Toro, según el presupuesto y las necesidades del proyecto. Son estándares de la industria, con "
     "repuestos en México."),
)

PASOS = (
    {"titulo": "Cotización y visita técnica", "quien": "juntos", "cuando": "Antes de cotizar",
     "texto": ("Nos mandas fotos y medidas del área por WhatsApp o agendamos una visita para medir y cotizar. "
               f"{datos.VISITA_COSTO} Revisamos el área, la fuente de agua y el tipo de plantas.")},
    {"titulo": "Diseño del sistema", "quien": "nosotros", "cuando": "Al cotizar",
     "texto": ("Hacemos el plano con la distribución de aspersores o goteros, el número de zonas y el programador, con el "
               "recorrido de tuberías que menos obra requiere.")},
    {"titulo": "Instalación de tuberías", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Instalamos la red de tuberías subterráneas sin dañar raíces ni áreas del jardín, con conexiones selladas."},
    {"titulo": "Aspersores y programador", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": ("Colocamos aspersores o goteros en su posición final y conectamos el programador que riega solo en los "
               "horarios que elijas.")},
    {"titulo": "Prueba y calibración", "quien": "juntos", "cuando": "Al terminar",
     "texto": ("Probamos todo el sistema, ajustamos la cobertura y programamos horarios para el clima de Tampico. Te "
               "explicamos cómo operarlo y ajustarlo en temporada de lluvias.")},
)

FIGURAS = (
    {"src": f"{OBRA}/riego-tecnico-sistema-industrial.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Técnico de Viveros Terra revisando aspersores en el área verde de una planta industrial.",
     "lugar": "Riego en una planta industrial", "etapa": "Prueba y calibración"},
    {"src": f"{OBRA}/riego-aspersor-emergente-pasto.webp", "ancho": 640, "alto": 1423, "numero": 3,
     "alt": "Aspersor sobre elevador regando philodendron en una jardinera.", "lugar": "Aspersor en jardinera",
     "etapa": "Tampico"},
    {"src": f"{OBRA}/riego-goteo-philodendron.webp", "ancho": 640, "alto": 1423, "numero": 4,
     "alt": "Aspersor emergente regando helechos en una jardinera junto a la banqueta.",
     "lugar": "Aspersor emergente en jardinera",
     "etapa": "Tampico"},
)

SECTORES = (
    ("Residencial", "Casas y jardines familiares"),
    ("Comercios y hoteles", "Jardines de imagen y áreas exteriores"),
    ("Industria", "Parques industriales y áreas perimetrales"),
    ("Escuelas y gobierno", "Patios, parques y áreas públicas"),
    ("Campos deportivos", "Con pasto natural"),
)

CONTENIDO = {
    "tipo": "servicio-riego",
    "prefijo": "riego",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "howto": "Cómo instalar un sistema de riego automático en Tampico",
               "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Riego automático", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Riego automático · Tampico, Madero y Altamira",
        "h1": f'Riego automático para jardines en Tampico <span class="vt-serif">que ahorra {AHORRO} de agua</span>',
        "lede": ("Aspersión, goteo o microaspersión con programador, para casas, fraccionamientos, hoteles, industria y "
                 "campos deportivos con pasto natural."),
        "etiqueta": {
            "codigo": "Riego · 01", "aviso": "Con IVA", "nombre": "Sistema de riego automático",
            "antes": "Instalado · según el sistema", "monto": f"{dinero(RIEGO_MIN)}–{dinero(RIEGO_MAX)}", "unidad": "/m²",
            "filas": ((f"Jardín de {EJEMPLO_M2} m²",
                       f"{dinero(RIEGO_MIN * EJEMPLO_M2)} a {dinero(RIEGO_MAX * EJEMPLO_M2)}"),
                      ("Instalación residencial", "1 a 2 días")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Fotos y medidas por WhatsApp para cotizar · <a href="#mensualidades">mensualidades con tarjeta de '
                    f'crédito</a> desde {DESDE_MENSUALIDADES}'),
        "foto": {"src": "/img/portadas/riego-pro-01-sm.webp",
                 "srcset": "/img/portadas/riego-pro-01-sm.webp 560w, /img/portadas/riego-pro-01.webp 960w",
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 640, "numero": 1,
                 "alt": "Aspersores de riego automático funcionando en un jardín",
                 "lugar": "Sistema de riego por aspersión", "etapa": "Instalado"},
    },
    "prueba": {
        "titulo": "Instalaciones en Tampico y la región",
        # Cifra confirmada por el dueño (2026-11-07): datos.SISTEMAS_RIEGO.
        "lede": (f"{datos.SISTEMAS_RIEGO} sistemas de riego instalados en la región: aspersores, goteo y microaspersión en "
                 "jardines residenciales e industriales de la zona."),
        "figuras": FIGURAS,
        "nota": ("Si tu jardín es chico y tienes tiempo de regar, quizá no necesitas un sistema completo: un programador "
                 "con goteo en las jardineras puede bastar. Te lo decimos al cotizar.", "Al cotizar"),
        # La opinión de riego aprobada de la home y las dos que publicaba esta página en main (reales y con permiso,
        # confirmadas por el dueño: datos.OPINIONES_RIEGO).
        "titulo_opinion": "Resultados comprobados en Tampico",
        "opiniones": datos.OPINIONES[2:3] + datos.OPINIONES_RIEGO,
        "titulo_clientes": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
    },
    "opciones": {
        "rotulo": "Sistemas",
        "titulo": "Tipos de sistema según tu jardín",
        "lede": "Diseñamos el sistema según el tamaño del área, el tipo de plantas y tu presupuesto.",
        "items": SISTEMAS,
    },
    "precio": {
        "titulo": "¿Cuánto cuesta un sistema de riego automático en Tampico?",
        "lede": (f"Entre {dinero(RIEGO_MIN)} y {dinero(RIEGO_MAX)} por m² instalado, según el tipo (aspersores, goteo o "
                 f"mixto), el número de zonas y la fuente de agua. Un jardín residencial de {EJEMPLO_M2} m² queda entre "
                 f"{dinero(RIEGO_MIN * EJEMPLO_M2)} y {dinero(RIEGO_MAX * EJEMPLO_M2)} con programador incluido, y ahorra "
                 f"{AHORRO} de agua frente al riego manual. Precios {datos.ANIO} con IVA."),
        "tabla": {"columnas": ("Concepto", "Unidad", "Precio"),
                  "filas": (("Sistema de riego automático instalado", "/m²",
                             f"{dinero(RIEGO_MIN)} a {dinero(RIEGO_MAX)}"),
                            (f"Jardín residencial de {EJEMPLO_M2} m²", "por jardín",
                             f"{dinero(RIEGO_MIN * EJEMPLO_M2)} a {dinero(RIEGO_MAX * EJEMPLO_M2)}"))},
        "caption": ('El precio cerrado sale de las fotos y medidas o de la visita. Lista completa en '
                    '<a href="/precios">viverosterra.com/precios</a>.'),
    },
    "objecion": {
        "titulo": "Aspersión, goteo o microaspersión",
        "lede": "Los tres sistemas de riego automático más usados en jardines residenciales y comerciales de Tampico.",
        "comparativa": {
            "columnas": ("Característica", "Aspersores emergentes", "Riego por goteo", "Microaspersión"),
            "filas": (
                ("Ideal para", "Pasto y áreas grandes", "Plantas y arriates", "Camellones"),
                ("Cobertura", "2 a 15 m de radio", "Punto por punto", "1 a 3 m de radio"),
                ("Presión requerida", "2 a 4 bar", "1 a 1.5 bar", "1.5 a 2 bar"),
                ("Se ve cuando no riega", "No, se ocultan", "Sí, mangueras", "Sí, estacas"),
            ),
            "caption": "Los tres sistemas, lado a lado.",
            "cierre": ("En jardines mixtos de Tampico (pasto y plantas), lo más eficiente es combinar aspersores en el pasto "
                       "y goteo en los arriates."),
        },
    },
    "proceso": {"titulo": "Cómo instalar un sistema de riego automático en 5 pasos",
                "lede": "De la cotización a tu jardín regándose solo, sin sorpresas en el precio.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía en materiales e instalación.",
        "resumen": "Fugas o fallas por causas de la instalación: las atendemos.",
        "puntos": (
            ("Garantizamos la instalación y los materiales: fugas o fallas por causas de la instalación, las atendemos.",
             True),
            ("Equipo Hunter, Rain Bird y Toro, con repuestos en México.", True),
            ("Programamos en horarios de baja evaporación y te explicamos cómo ajustarlo en temporada de lluvias.", True),
            ("Mantenimiento preventivo y correctivo del sistema ya instalado.", True),
            (f"Factura {datos.FACTURA} para persona física o moral.", True),
        ),
        "pie": '<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} Puedes pagar de contado o en mensualidades con tarjeta de crédito desde "
                 f"{DESDE_MENSUALIDADES}."),
        "puntos": (
            "Recibes el precio del sistema, la instalación y la obra civil por separado.",
            "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
            ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos antes "
             'de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>'),
        ),
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "un sistema de riego", "monto": RIEGO_MIN * EJEMPLO_M2},  # el ejemplo de 100 m²
    },
    "faq": {"titulo": "Todo sobre sistemas de riego en Tampico", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Listo para automatizar el riego de tu jardín?",
        "lede": ("Envíanos fotos y medidas aproximadas, y dinos si tienes pasto, plantas o ambos. Si hace falta, "
                 f"agendamos una visita para medir y cotizar. {datos.VISITA_COSTO}"),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Riego automático en Tampico, Madero y Altamira.",
        "lede": "Casas, comercios, industria y campos deportivos de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"San Agustín desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Diseño de Jardines", "href": "/diseno-jardines-tampico",
             "img": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427,
             "texto": f"Plan Terra desde {dinero(P['diseno'])} · Propuesta visual incluida"},
            {"titulo": "Mantenimiento", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": f"Desde {dinero(P['mantenimiento_mes'])}/mes · Poda, fertilización y cuidados"},
        ),
    },
}

PARIDAD = {
    "meta": seo.paridad(TITULO, DESCRIPCION),
    "reemplazos": {
        "Aspersores Emergentes": "Aspersores emergentes",
        "Riego por Goteo": "Riego por goteo",
        "Industrial y Deportivo": "Industrial y deportivo",
        # La segunda lista de 5 pasos repetía la primera (auditoría 02): queda una sola.
        "Instalación en 5 pasos": "Cómo instalar un sistema de riego automático en 5 pasos",
        "Cotización y diagnóstico": "Cotización y visita técnica",
        "Excavación e instalación de tuberías": "Instalación de tuberías",
        "Instalación de aspersores y programador": "Aspersores y programador",
        "Prueba, calibración y entrega": "Prueba y calibración",
        "¿Cuánto tiempo tarda la instalación de un sistema de riego?": "¿Cuánto tiempo tarda la instalación?",
        "¿El sistema funciona con la presión de agua municipal?": "¿Funciona con la presión de agua de la red municipal?",
        "¿Qué marcas de aspersores instalan?": "¿Qué marcas de aspersores y programadores instalan?",
    },
    "retirados": {
        "La forma más eficiente de mantener tu jardín verde en Tampico": (
            "La definición del sistema queda en la entrada de la portada y en la sección de tipos de sistema."),
        "+200 sistemas instalados en la región": (
            "Cifra confirmada por el dueño (2026-11-07): pasa a la entrada de la prueba (datos.SISTEMAS_RIEGO); sus "
            "garantías pasan a la sección de garantía."),
        "Cotización por WhatsApp": (
            "El formulario que armaba el mensaje (sendRW) se sustituye por un botón con su propio mensaje en cada tipo "
            "de sistema y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” (confirmado por el dueño) "
            "pasa al título de los clientes; la certificación SENASICA no se publica (decisión del dueño)."),
        "$15,000": (f"Error aritmético: {EJEMPLO_M2} m² × ${RIEGO_MIN} = ${RIEGO_MIN * EJEMPLO_M2:,}; el rango del "
                    "ejemplo sale ahora de datos.PRECIOS['riego_m2']."),
    },
}
