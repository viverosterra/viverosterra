"""Contenido de /protocolo-cuidados-pasto-san-agustin: el plan de riego por días y las condiciones de la garantía, con las
palabras de main. La garantía usa la frase aprobada por el dueño (datos.GARANTIA_PASTO); $85 y $750 salen de datos.py.
Sin "experto", sin los contadores repetidos del hero y con un solo H1."""
import datos
import mensajes_paginas
from componentes import dinero

P = datos.PRECIOS
SITE = datos.SITIO
URL = f"{SITE}/protocolo-cuidados-pasto-san-agustin"
FOTO = {"src": "/img/instalacion-pasto-rollo-san-agustin-tampico.webp", "ancho": 1024, "alto": 1536, "alt": ""}
MENSAJE = mensajes_paginas.UTILITARIAS["protocolo"]
CONTENIDO = {
    "tipo": "posventa",
    "meta": {"title": "Protocolo de Cuidados · Pasto San Agustín · Viveros Terra",
             "description": "Protocolo completo para pasto San Agustín recién instalado: riego abundante y diario del día 1 al 20, señales de arraigo y condiciones de garantía. Viveros Terra Tampico.",
             "robots": "index, follow", "canonical": URL,
             "og": (("og:title", "Protocolo de Cuidados Pasto San Agustín · Viveros Terra"),
                    ("og:description", "Plan de riego y cuidados para pasto San Agustín recién instalado. Garantía de arraigo en 15 a 20 días. Viveros Terra Tampico."),
                    ("og:url", URL), ("og:type", "article"))},
    "cabeza": {"migas": (("Inicio", "/"), ("Pasto en rollo", "/pasto-en-rollo-tampico"), ("Protocolo de cuidados", None)),
               "kicker": f"Protocolo de Cuidados · arraigo en {datos.ARRAIGO} · pasto desde {dinero(P['pasto_solo_m2'])}/m²",
               "h1": 'Cómo cuidar tu Pasto <span class="vt-serif">San Agustín paso a paso.</span>',
               "lede": ("Protocolo oficial de Viveros Terra para el cuidado del pasto San Agustín recién instalado. Riego, "
                        "fertilización, primera poda y control de plagas adaptados al clima de Tampico y Tamaulipas. El riego "
                        "lo haces tú: al terminar la instalación te explicamos cómo dar el primer riego y aquí tienes el "
                        "plan de los 20 días."),
               "foto": FOTO},
    "plan": {"titulo": 'Plan de Cuidados <span class="vt-serif">por Etapa</span>',
             "lede": (f"El pasto que instalamos fue <strong>cortado para tu pedido directamente del campo</strong>. Seguir este "
                      f"protocolo durante los primeros {datos.ARRAIGO} es lo que asegura que arraigue. <strong>Guarda este "
                      "documento.</strong>"),
             "fases": (
                 {"dias": "Días 1 – 7", "titulo": "Fase crítica de arraigo — la más importante", "items": (
                     "<strong>Riego abundante 2 veces al día:</strong> mañana (7–9am) y tarde (5–7pm). Riega hasta que el suelo esté húmedo a 5 cm de profundidad.",
                     "Aunque llueva, revisa que el suelo siga húmedo a 5 cm. Si no lo está, riega igual.",
                     "<strong>NO pisar el pasto</strong> bajo ninguna circunstancia — las raíces apenas están anclando.",
                     "<strong>NO podar ni cortar</strong> — el pasto necesita toda su energía para arraigar.",
                     "<strong>NO aplicar fertilizante</strong> — puede quemar las raíces nuevas.",
                     "<strong>NO aplicar herbicidas ni insecticidas</strong> sin consultarnos primero.")},
                 {"dias": "Días 8 – 14", "titulo": "Fase de consolidación", "items": (
                     "<strong>Riego abundante y diario</strong>, sin saltarte ningún día. De preferencia por la mañana, antes de las 10am.",
                     "Puedes verificar el arraigo: jala suavemente una esquina del pasto — si resiste y no se levanta, está pegando bien.",
                     "Si ves zonas más claras o amarillas, aumenta el riego en esa zona específica.",
                     "Sigue sin podar ni fertilizar.", "Evita pisoteo frecuente aunque ya haya arraigo parcial.")},
                 {"dias": "Días 15 – 20", "titulo": "Fase de establecimiento", "items": (
                     "<strong>Sigue con riego abundante y diario</strong> hasta el día 20. Es lo que asegura que el pasto termine de arraigar.",
                     "<strong>Primera poda</strong> cuando el pasto supere 8 cm de altura — no cortes más del 30% de la hoja en un solo corte.",
                     "Puedes aplicar fertilizante granulado ligero (triple 17 o similar) después del día 20.",
                     "El pasto ya puede pisarse con normalidad si el arraigo es completo.")},
             )},
    "senales": {"titulo": 'Señales <span class="vt-serif">a Identificar</span>', "items": (
        {"titulo": "Señales de buen arraigo", "items": (
            "Color verde intenso y parejo en toda el área", "Al jalar suavemente, el pasto resiste y no se levanta",
            "Nuevos brotes visibles en los bordes (runners)", "El suelo debajo se ve húmedo pero no encharcado")},
        {"titulo": "Señales de alerta — actúa de inmediato", "items": (
            "<strong>Parches amarillos:</strong> generalmente falta de agua. Aumenta el riego en esa zona y riega profundo.",
            "<strong>Parches café/seco:</strong> puede ser quemadura por sol intenso + calor. Riega de inmediato y considera malla de sombra temporal.",
            "<strong>Bordes que se levantan:</strong> las esquinas necesitan más agua. Riega 20 minutos extra en esa área.")},
        {"titulo": "Señales de problema — llámanos antes de actuar", "items": (
            "<strong>No arraiga después del día 20:</strong> contáctanos antes de hacer cualquier cambio. No apliques nada sin consultarnos.",
            "<strong>Zona completamente café y seca (más de 1 m²):</strong> llámanos ese mismo día con foto.",
            "<strong>Aparición de hongos o manchas oscuras:</strong> puede ser exceso de humedad — reduce el riego y avísanos.")},
    )},
    "mantenimiento": {"titulo": 'Mantenimiento <span class="vt-serif">a partir del día 21</span>', "items": (
        "<strong>Riego:</strong> 2–3 veces por semana en temporada seca. En lluvia, según necesidad.",
        "<strong>Poda:</strong> cada 10–15 días cuando el pasto alcance 8–10 cm. Altura ideal de corte: 4–5 cm.",
        "<strong>Fertilización:</strong> cada 2–3 meses con fertilizante granulado. En temporada de crecimiento (lluvia) puedes fertilizar más seguido.",
        "<strong>Control de maleza:</strong> retira manualmente las malas hierbas en cuanto aparezcan. Evita herbicidas de amplio espectro.",
        f'<strong>Si quieres un mantenimiento sin preocupaciones:</strong> pregúntanos por nuestro <a href="/mantenimiento-jardines-tampico">servicio mensual</a> desde {dinero(P["mantenimiento_mes"])}/mes.')},
    "garantia": {"titulo": 'Garantía de Arraigo <span class="vt-serif">— Condiciones</span>',
                 "lede": "Para que aplique la garantía de arraigo de Viveros Terra, se deben cumplir estas condiciones:",
                 "condiciones": (
                     "La instalación fue realizada por el equipo de Viveros Terra",
                     f"Se realizó riego abundante y diario los primeros {datos.ARRAIGO} según este protocolo",
                     "No hubo pisoteo durante los primeros 7 días",
                     "No se aplicaron productos químicos sin autorización previa",
                     "El problema fue reportado antes del día 21"),
                 "pie": (f"{datos.GARANTIA_PASTO.replace(' (ver condiciones)', '')} En caso de duda sobre si el problema aplica a "
                         f"garantía, contáctanos con foto. {datos.PROMESA}.")},
    "cierre": {"titulo": "¿Tienes dudas? Estamos aquí",
               "lede": (f"Mándanos foto de tu pasto por WhatsApp y te ayudamos con el diagnóstico y la solución. "
                        f"{datos.DOMICILIO_COMPLETO}."),
               "mensaje": MENSAJE},
    "jsonld": (),
}
PARIDAD = {
    "reemplazos": {"Protocolo de Cuidados": "Cómo cuidar tu Pasto San Agustín paso a paso."},
    "retirados": {},
    "jsonld": {},
}
