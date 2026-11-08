"""Contenido de /diseno-jardines-tampico (Plan Terra en 3 niveles). Solo datos: la plantilla es
tools/site/plantillas/servicio.py, con planes (cada uno con su mensaje y su línea de mensualidades), tabla comparativa,
objeción "¿y si no contrato la obra?", proceso, garantía de plantas condicionada y simulador.

Precios de datos.PRECIOS (Esencial $3,000, Completo $6,500, Premium desde $18,000 y su descuento en proyectos de más
de $150,000); mensualidades con la fórmula de tools/pasto/mensualidades.py. Título, descripción, canonical, Open Graph,
Twitter Card, Service y migas del JSON-LD como estaban publicados en main (los acentos del JSON-LD los arregla la
Etapa 4); FAQPage sale de las preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
import mensajes_paginas
from componentes import dinero, mensualidades

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/diseno-jardines-tampico"
OBRA = "/img/obra"
ESENCIAL, COMPLETO, PREMIUM = P["diseno"], P["diseno_completo"], P["diseno_premium"]
DESCUENTO_PREMIUM = dinero(P["diseno_premium_descuento_desde"])
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
MENSAJE = mensajes_paginas.SERVICIOS["/diseno-jardines-tampico"]
CONDICIONES = '<a href="/politicas#garantia-plantas">ver condiciones</a>'

META = {
    "title": "Diseño de Jardines Tampico · Plan Terra",
    "description": (f"Diseño profesional de jardines en Tampico. Plan Terra en 3 niveles: Esencial {dinero(ESENCIAL)}, "
                    f"Completo {dinero(COMPLETO)}, Premium desde {dinero(PREMIUM)}. Descuento al contratar."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", f"Diseño de Jardines Tampico | Plan Terra desde {dinero(ESENCIAL)} — Viveros Terra"),
        ("og:description", ("Diseño profesional de jardines en Tampico, Madero y Altamira. Plan Terra en 3 niveles: "
                            f"Esencial desde {dinero(ESENCIAL)}, Completo {dinero(COMPLETO)} y Premium con planos AutoCAD "
                            "y render 3D. Cotiza gratis por WhatsApp.")),
        ("og:image", f"{SITE}/img/diseno-jardines-tampico-viveros-terra.webp"),
        ("og:locale", "es_MX"),
    ),
    "twitter": (("twitter:card", "summary_large_image"),),
}

# Service y migas como estaban publicados (texto sin acentos incluido: el grafo único es de la Etapa 4).
_PROVEEDOR = {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL,
              "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                          "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"}}
SERVICIO = {
    "@type": "Service", "serviceType": "Diseno de Jardines", "name": "Diseno de Jardines Tampico - Plan Terra",
    "description": ("Servicio profesional de diseno de jardines residenciales, corporativos y de desarrollo en Tampico, "
                    "Ciudad Madero y Altamira. Plan Terra con propuesta visual, seleccion de plantas y planos segun el "
                    "nivel contratado."),
    "provider": _PROVEEDOR,
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"],
    "offers": [
        {"@type": "Offer", "name": "Plan Terra Esencial", "price": str(ESENCIAL), "priceCurrency": "MXN",
         "description": ("Propuesta visual con montajes, diseno basado en gustos, lista de plantas, cotizacion y asesoria "
                         "7 dias. Entrega 3 a 5 dias habiles.")},
        {"@type": "Offer", "name": "Plan Terra Completo", "price": str(COMPLETO), "priceCurrency": "MXN",
         "description": ("Visita tecnica, toma de medidas, diseno detallado, fichas de plantas, cuantificacion de "
                         "materiales, manual de cuidados PDF, consulta estacional 6 meses y garantia de arraigo 30 dias "
                         "en las plantas que sembramos, con el riego indicado. Entrega 10 dias habiles.")},
        {"@type": "Offer", "name": "Plan Terra Premium", "price": str(PREMIUM), "priceCurrency": "MXN",
         "description": ("Proyecto ejecutivo con 2 visitas tecnicas, planos AutoCAD, render 3D alta resolucion, plan de "
                         "riego tecnico, plan de mantenimiento 12 meses, arquitecto paisajista asignado, presentacion "
                         "ejecutiva y revision post-ejecucion. Entrega 15 a 21 dias habiles.")},
    ],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Diseno de Jardines Tampico", "item": URL},
]}

PLANES = (
    {"rotulo": "Plan 1 · Remoto", "titulo": "Esencial", "precio": ESENCIAL, "desde": False, "unidad": "MXN",
     "mensualidad": True, "detalle": "Visualiza tu jardín antes de invertir · entrega en 3 a 5 días hábiles",
     "puntos": ("Propuesta visual con montajes fotográficos personalizados",
                "Diseño basado en el estudio de tus gustos y preferencias",
                "Lista de plantas seleccionadas para el clima de Tampico",
                "Cotización detallada del proyecto completo",
                "Asesoría por WhatsApp con el diseñador (7 días)",
                "Garantía de precio: cotización respetada 30 días",
                f"Los {dinero(ESENCIAL)} se descuentan si contratas la obra"),
     "mensaje": (f"Hola, me interesa el Plan Terra Esencial ({dinero(ESENCIAL)}).\nColonia: ___\nMetros aprox.: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Plan 2 · Con visita", "titulo": "Completo", "precio": COMPLETO, "desde": False, "unidad": "MXN",
     "mensualidad": True, "rec": True, "detalle": "Del diseño al jardín terminado · entrega en 10 días hábiles",
     "puntos": ("Todo lo del Esencial",
                "Visita técnica al sitio (1 hora con el diseñador)",
                "Toma de medidas profesional y análisis del terreno",
                "Selección de plantas con la ficha técnica de cada una",
                "Cuantificación completa de materiales",
                "Manual de cuidados personalizado en PDF (10+ páginas)",
                "Consulta estacional de 30 min a los 6 meses y carpeta digital del proyecto",
                # Sin enlace dentro de la lista (vt-checks es grid): las condiciones se enlazan en la garantía.
                "Garantía de arraigo de 30 días en las plantas que sembramos nosotros, con el riego indicado",
                f"Los {dinero(COMPLETO)} se descuentan si contratas la obra"),
     "mensaje": (f"Hola, me interesa el Plan Terra Completo ({dinero(COMPLETO)}).\nColonia: ___\nMetros aprox.: ___\n"
                 "Les mando fotos del espacio.")},
    {"rotulo": "Plan 3 · Proyecto ejecutivo", "titulo": "Premium", "precio": PREMIUM, "unidad": "MXN",
     "mensualidad": True, "detalle": "Hoteles, corporativos, fraccionamientos y desarrollos · entrega en 15 a 21 días hábiles",
     "puntos": ("Todo lo del Completo",
                "2 visitas técnicas (diagnóstico y presentación en sitio)",
                "Planos ejecutivos en AutoCAD (planta, alzados y cortes)",
                "Render 3D profesional en alta resolución",
                "Plan de riego técnico y plan de mantenimiento de 12 meses",
                "Arquitecto paisajista asignado y presentación ejecutiva (PDF y PowerPoint)",
                "Revisión a 1 año: 2 visitas después de la obra",
                f"Factura {datos.FACTURA} con complemento de servicios",
                f"Se descuenta en proyectos de más de {DESCUENTO_PREMIUM}"),
     "mensaje": (f"Hola, me interesa el Plan Terra Premium (desde {dinero(PREMIUM)}).\nEmpresa o tipo de proyecto: ___\n"
                 "Ubicación: ___\nMetros aprox.: ___")},
)

COMPARA = {
    "titulo": "Compara los 3 planes en detalle",
    "plegable": True,  # revisión de 2c: en celular la tabla larga va plegada; desde 768 px se abre
    "columnas": ("Incluye", f"Esencial {dinero(ESENCIAL)}", f"Completo {dinero(COMPLETO)}",
                 f"Premium desde {dinero(PREMIUM)}"),
    "filas": (
        ("Diseño basado en tus gustos", "Sí", "Detallado", "Detallado"),
        ("Lista de plantas", "Básica", "Con fichas técnicas", "Con fichas técnicas"),
        ("Asesoría por WhatsApp", "7 días", "Incluida", "Incluida"),
        ("Visita técnica", "—", "1", "2"),
        ("Manual de cuidados en PDF", "—", "Sí", "Ampliado"),
        ("Cuantificación de materiales", "—", "Sí", "Sí"),
        ("Consulta estacional a los 6 meses", "—", "Sí", "Sí"),
        ("Garantía de arraigo en plantas que sembramos", "—", "30 días", "30 días"),
        ("Planos AutoCAD y render 3D", "—", "—", "Sí"),
        ("Plan de mantenimiento de 12 meses", "—", "—", "Sí"),
        ("Revisión después de la obra (1 año)", "—", "—", "2 visitas"),
        ("Descuento al contratar la obra", "Total", "Total", f"En proyectos de más de {DESCUENTO_PREMIUM}"),
        ("Tiempo de entrega", "3 a 5 días", "10 días", "15 a 21 días"),
    ),
    "caption": f"Precios {datos.ANIO} con IVA. Días hábiles desde que recibimos las fotos.",
}

PREGUNTAS = (
    ("¿Cuánto cuesta el diseño de un jardín en Tampico?",
     f"El Plan Terra tiene 3 niveles: Esencial ({dinero(ESENCIAL)}), Completo ({dinero(COMPLETO)}) y Premium (desde "
     f"{dinero(PREMIUM)}), con IVA. En Esencial y Completo el costo se descuenta completo si contratas la obra con "
     f"Viveros Terra; en el Premium, en proyectos de más de {DESCUENTO_PREMIUM}."),
    ("¿Qué diferencia al Plan Esencial del Completo?",
     "El Esencial es remoto: nos envías fotos y te regresamos la propuesta visual y la cotización en 3 a 5 días hábiles. "
     "El Completo incluye una visita técnica con toma de medidas, cuantificación de materiales, manual de cuidados en PDF "
     "y acompañamiento después de la entrega, con consulta estacional y garantía de arraigo en las plantas que sembramos "
     f"nosotros ({CONDICIONES})."),
    ("¿Cuándo conviene el Plan Premium?",
     "Cuando necesitas entregables técnicos formales para un comité, una junta directiva, inversionistas o una aprobación "
     "corporativa. Incluye planos ejecutivos en AutoCAD, render 3D, plan de mantenimiento a 12 meses y presentación "
     "ejecutiva. Es para hoteles, corporativos, fraccionamientos y desarrollos."),
    ("¿Se descuenta el costo del diseño si contrato la ejecución?",
     "Sí. En los planes Esencial y Completo el monto se descuenta completo. En el Premium aplica a proyectos con "
     f"presupuesto de ejecución de más de {DESCUENTO_PREMIUM}."),
    ("¿Cómo se eligen las plantas para mi jardín?",
     "Con el estudio de tus gustos y preferencias elegimos plantas para el clima cálido y húmedo de Tampico, según el sol "
     "que recibe cada zona, el tipo de suelo, el mantenimiento que puedes darle y el estilo que buscas (tropical, "
     'minimalista, mediterráneo). Puedes ver especies en el <a href="/catalogo">catálogo del vivero</a>.'),
    ("¿Puedo ver ejemplos de diseños anteriores?",
     "Sí. En esta página ves algunos proyectos, y por WhatsApp te enviamos carpetas con casos residenciales, corporativos "
     "y hoteleros parecidos al tuyo para que sepas qué esperar."),
    ("¿Cuánto tiempo tardan en entregar el diseño?",
     "Plan Esencial: 3 a 5 días hábiles desde que recibimos las fotos. Plan Completo: 10 días hábiles. Plan Premium: 15 a "
     "21 días hábiles por los entregables técnicos."),
    ("¿Facturan CFDI 4.0?",
     f"Sí. Emitimos factura {datos.FACTURA} en todos los planes. El Premium incluye factura con complemento de servicios "
     "profesionales para que lo registres como proyecto de inversión."),
)

PASOS = (
    {"titulo": "Envías fotos y cuéntanos tu visión", "quien": "tu", "cuando": "Por WhatsApp",
     "texto": ("Nos mandas fotos del espacio, medidas aproximadas, tu estilo preferido y el uso que le darás al "
               "jardín.")},
    {"titulo": "Estudio de gustos y preferencias", "quien": "juntos", "cuando": "Antes de diseñar",
     "texto": ("Tu asesor te manda un cuestionario breve: colores, texturas, cuánto mantenimiento puedes darle, si hay "
               "mascotas o niños y cuánto sol recibe cada zona.")},
    {"titulo": "Elegimos el Plan Terra correcto para ti", "quien": "nosotros", "cuando": "Al cotizar",
     "texto": ("Te recomendamos Esencial, Completo o Premium según la complejidad del proyecto y si necesitas "
               "entregables técnicos.")},
    {"titulo": "Entrega del diseño", "quien": "nosotros", "cuando": "3 a 21 días hábiles",
     "texto": ("Recibes la propuesta visual, la cotización del proyecto y los entregables de tu plan: 3 a 5 días "
               "(Esencial), 10 días (Completo) o 15 a 21 días (Premium).")},
    {"titulo": "Ejecución del proyecto (opcional)", "quien": "juntos", "cuando": "Cuando tú decidas",
     "texto": ("Si lo ejecutamos nosotros, el costo del diseño se descuenta del proyecto. Si no, el diseño es tuyo para "
               "cuando quieras usarlo.")},
)

# Proyectos de Terra terminados (respuesta del dueño, 2026-11-07): pie "Fig. NN · zona · Terminado".
FIGURAS = (
    {"src": f"{OBRA}/diseno-jardin-alberca-tampico.webp", "ancho": 960, "alto": 640, "numero": 2,
     "alt": "Escalones de concreto entre helechos y plantas tropicales junto a una alberca.",
     "lugar": "Tampico", "etapa": "Terminado"},
    {"src": f"{OBRA}/diseno-jardin-paisajismo-tampico.webp", "ancho": 640, "alto": 427, "numero": 3,
     "alt": "Jardín residencial con pasto, arriates y plantas ornamentales.",
     "lugar": "Tampico", "etapa": "Terminado"},
    {"src": f"{OBRA}/diseno-jardin-pasto-madero.webp", "ancho": 640, "alto": 427, "numero": 4,
     "alt": "Jardín con pasto San Agustín y plantas en Ciudad Madero.",
     "lugar": "Ciudad Madero", "etapa": "Terminado"},
)

CONTENIDO = {
    "tipo": "servicio-diseno",
    "prefijo": "diseno",
    "meta": META,
    "jsonld": {"producto": SERVICIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Diseño de jardines", None)),
    "portada": {
        "compacta": True,  # a 1024–1199 px el CTA queda en la primera pantalla
        "kicker": "Diseño de jardines · Tampico, Madero y Altamira",
        "h1": 'Diseño de jardines en Tampico <span class="vt-serif">con plan y presupuesto claros</span>',
        "lede": ("Te entregamos el diseño, la lista de plantas y materiales y el costo de la obra. Si nos contratas para "
                 f"hacerla, el diseño se descuenta (en el Premium, en proyectos de más de {DESCUENTO_PREMIUM})."),
        "etiqueta": {
            "codigo": "Diseño · Plan Terra", "aviso": "Con IVA", "nombre": "Plan Terra Esencial",
            "antes": "Propuesta visual · 3 a 5 días", "monto": dinero(ESENCIAL), "unidad": "MXN",
            "filas": (("Plan Completo, con visita", dinero(COMPLETO)), ("Plan Premium", f"desde {dinero(PREMIUM)}")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Se descuenta si contratas la obra · <a href="#opciones">compara los 3 planes</a> · '
                    f'<a href="#mensualidades">mensualidades con tarjeta de crédito</a> desde {DESDE_MENSUALIDADES}'),
        "foto": {"src": "/img/portadas/diseno-jardines-tampico-proyecto-sm.webp",
                 "srcset": ("/img/portadas/diseno-jardines-tampico-proyecto-sm.webp 560w, "
                            "/img/portadas/diseno-jardines-tampico-proyecto.webp 960w"),
                 "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1574, "numero": 1,
                 "alt": "Jardín residencial diseñado por Viveros Terra en Tampico",
                 "lugar": "Tampico", "etapa": "Terminado"},
    },
    "prueba": {
        "titulo": "Jardines y paisajismo que hemos diseñado en Tampico",
        "lede": "Jardines terminados del Plan Terra en casas, hoteles y desarrollos de la zona.",
        "figuras": FIGURAS,
        "nota": ("Si ya sabes qué plantas quieres y dónde van, no necesitas un plan de diseño: arma tu lista en el "
                 '<a href="/catalogo">catálogo</a> y te la cotizamos directo.', "Antes de contratar"),
        # La opinión de diseño aprobada de la home y las dos que publicaba esta página en main (reales y con permiso,
        # confirmadas por el dueño: datos.OPINIONES_DISENO).
        "titulo_opinion": "Lo que dicen quienes contrataron diseño",
        "opiniones": datos.OPINIONES[1:2] + datos.OPINIONES_DISENO,
        "titulo_clientes": f"Empresas que nos han contratado · {datos.PROYECTOS_B2B} proyectos B2B",
    },
    "opciones": {
        "rotulo": "Planes",
        "titulo": "¿Cuánto cuesta un diseño de jardín en Tampico?",
        "lede": (f"Desde {dinero(ESENCIAL)} con el Plan Terra, en 3 niveles: Esencial {dinero(ESENCIAL)}, Completo "
                 f"{dinero(COMPLETO)} y Premium desde {dinero(PREMIUM)}, con IVA. Incluye la propuesta de diseño, la "
                 "lista de plantas y materiales y la cotización de la obra; el costo se descuenta si contratas el "
                 f'proyecto. Precios {datos.ANIO}; lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "items": PLANES,
        "tabla": COMPARA,
    },
    "objecion": {
        "rotulo": "Tu diseño",
        "titulo": "¿Y si al final no contratas la obra?",
        "lede": ("El diseño es tuyo: lo puedes ejecutar cuando quieras, con nosotros o por tu cuenta. Si lo hacemos "
                 "nosotros, lo que pagaste se descuenta."),
        "comparativa": {
            "columnas": ("Plan", "Si contratas la obra con nosotros", "Si no la contratas"),
            "filas": (
                (f"Esencial · {dinero(ESENCIAL)}", f"Se descuentan los {dinero(ESENCIAL)}",
                 "Te quedas con la propuesta visual, la lista de plantas y la cotización"),
                (f"Completo · {dinero(COMPLETO)}", f"Se descuentan los {dinero(COMPLETO)}",
                 "Te quedas con el diseño, las fichas de plantas, la cuantificación y el manual de cuidados"),
                (f"Premium · desde {dinero(PREMIUM)}", f"Se descuenta en proyectos de más de {DESCUENTO_PREMIUM}",
                 "Te quedas con los planos, el render, el plan de riego y el plan de mantenimiento"),
            ),
            "caption": "Lo que pasa con el pago del diseño.",
            "cierre": "Garantía de precio: la cotización de la obra se respeta 30 días.",
        },
    },
    "proceso": {"titulo": "Del primer WhatsApp a tu jardín ejecutado",
                "lede": "Cinco pasos; el último solo si decides que ejecutemos la obra.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de arraigo de 30 días en las plantas que sembramos.", "grande": "30", "unidad": "días",
        "resumen": "En las plantas que sembramos nosotros al ejecutar tu proyecto, con el riego indicado.",
        "puntos": (
            ("Si una planta que sembramos no prende en 30 días y se regó como te indicamos, la reponemos sin costo.",
             True),
            ("Garantía de precio: la cotización de la obra se respeta 30 días.", True),
            (f"El costo del diseño se descuenta si contratas la obra (en el Premium, en proyectos de más de "
             f"{DESCUENTO_PREMIUM}).", True),
            (f"Factura {datos.FACTURA} en todos los planes.", True),
            ("No cubre falta o exceso de riego, plantas movidas de lugar ni plantas que siembras por tu cuenta.", False),
        ),
        "pie": '<a href="/politicas#garantia-plantas">Lee las condiciones de la garantía de plantas</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} El diseño y la obra se cotizan por separado; los dos se pueden pagar de contado o "
                 f"en mensualidades con tarjeta de crédito desde {DESDE_MENSUALIDADES}."),
        "puntos": (
            "Cada plan muestra su precio de contado y su plazo más largo con tarjeta de crédito.",
            "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
            ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos antes "
             'de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>'),
        ),
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "el diseño de mi jardín", "monto": COMPLETO},
    },
    "faq": {"titulo": "Todo sobre el Plan Terra", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "¿Listo para ver cómo se vería tu jardín?",
        "lede": ("Envíanos fotos de tu espacio por WhatsApp y dinos qué plan te interesa. Si no estás seguro, te "
                 "recomendamos uno."),
        "mensaje": MENSAJE,
    },
    "cobertura": {
        "titulo": "Diseñamos jardines en Tampico, Madero y Altamira.",
        "lede": "Casas, hoteles, corporativos y desarrollos de la zona conurbada; fuera de ella, por proyecto.",
        "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO,
    },
    "relacionados": {
        "titulo": "Otros servicios de Viveros Terra",
        "items": (
            {"titulo": "Pasto en Rollo San Agustín", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"Pasto desde {dinero(P['pasto_solo_m2'])}/m² · Instalado desde "
                       f"{dinero(P['pasto_instalado_m2'])}/m²")},
            {"titulo": "Sistema de Riego", "href": "/sistema-riego-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": f"Automatizado · Ahorra {datos.RIEGO_AHORRO} de agua"},
            {"titulo": "Mantenimiento de Jardines", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": f"Desde {dinero(P['mantenimiento_mes'])}/mes · Poda y cuidados"},
        ),
    },
}

PARIDAD = {
    "reemplazos": {
        "Diseño de jardines con plan y presupuesto claros": "Diseño de jardines en Tampico con plan y presupuesto claros",
        "Elige el plan que se ajusta a tu proyecto": "¿Cuánto cuesta un diseño de jardín en Tampico?",
        # Revisión de 2c: "paisajismo" vuelve a un H2 (el título y la descripción no cambian).
        "Jardines que hemos diseñado en Tampico": "Jardines y paisajismo que hemos diseñado en Tampico",
        # Las preguntas del JSON-LD sin acentos: el FAQPage sale ahora de las preguntas visibles.
        "Cuanto cuesta el diseno de un jardin en Tampico?": "¿Cuánto cuesta el diseño de un jardín en Tampico?",
        "Que incluye el Plan Terra?": "¿Qué diferencia al Plan Esencial del Completo?",
        "Se descuenta el costo del diseno si contrato la ejecucion?": (
            "¿Se descuenta el costo del diseño si contrato la ejecución?"),
        "Tardan cuanto tiempo en entregar el diseno?": "¿Cuánto tiempo tardan en entregar el diseño?",
        "Como se eligen las plantas para mi jardin?": "¿Cómo se eligen las plantas para mi jardín?",
    },
    "retirados": {
        "Diseño de jardines profesional con acompañamiento": (
            "La definición del Plan Terra queda en la entrada de la portada y en la respuesta directa de los planes."),
        "Cotización Plan Terra": (
            "El formulario que armaba el mensaje con un selector de plan (sendWA) se sustituye por un botón con su "
            "propio mensaje en cada plan (spec §3.3: un mensaje por plan) y el CTA final."),
        "Viveros Terra · Tampico": (
            "Bloque de autor; la entidad y el autor son de la Etapa 4. “+200 proyectos B2B” (confirmado por el dueño) "
            "pasa al título de los clientes; la certificación SENASICA no se publica (decisión del dueño)."),
        "$90": "“Complementa tu proyecto” (tierra negra, mármol, tezontle) sale; los materiales siguen en el menú y el pie.",
        "$1,500": "“Complementa tu proyecto” (tierra negra, mármol, tezontle) sale; los materiales siguen en el menú y el pie.",
        "$150": "“Aplica +$150k” de la tabla de planes ahora se escribe completo: “en proyectos de más de $150,000”.",
    },
}
