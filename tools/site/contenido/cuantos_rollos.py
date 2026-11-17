"""Contenido de /pasto-sintetico/cuantos-rollos (Entrega B del SEO nacional, 2026-11-16). Solo datos: la plantilla es
plantillas/tienda_guia.py y las piezas, componentes_rollos.py.

Responde «¿cuántos rollos de pasto sintético necesito?» para el rollo de 2 × 25 m: calculadora de medidas
(vt-rollos.js) que llena el cotizador de la tienda (precio, flete, folio y WhatsApp de tienda-pasto.js), tabla de
medidas comunes y envío por estado. El 10% para cortes y el sentido de las tiras salen de la guía de instalación
(/blog/como-instalar-pasto-sintetico); precios, mínimos y fletes de tools/pasto/data.py; el plazo de 3 a 5 días hábiles
lo confirmó el dueño (2026-11-16). Página nueva: sin captura anterior (generar.NUEVAS).
"""
import componentes_rollos as cr
import componentes_tienda as t
import data
import datos
import rollos
from componentes import dinero
from contenido import seo
from esquema import breadcrumb_schema

SITE = data.SITE
RUTA = "/pasto-sintetico/cuantos-rollos"
URL = f"{SITE}{RUTA}"
FOTO = "obra-proyecto-05"
TITULO = "¿Cuántos Rollos de Pasto Sintético Necesito? Calculadora"
DESCRIPCION = ("Calcula cuántos m² y rollos de pasto sintético necesitas: escribe largo y ancho y ve el corte en tiras "
               "de 2 m, el envío por rollo a tu estado y el precio.")
BARATO = t.barato()
EJ = rollos.corte(*cr.EJEMPLO)
MIN, ROLLO = data.MIN_NACIONAL_M2, data.ROLLO_M2
GUIA = '<a href="/blog/como-instalar-pasto-sintetico">guía de instalación</a>'
MENSAJE = "Hola, ya calculé mi pasto sintético en la web.\nMedidas: ___ × ___ m\nEstado: ___"

RESPUESTA = (f"Un rollo mide 2 × 25 m ({ROLLO} m²). Un patio de {cr.EJEMPLO[0]} × {cr.EJEMPLO[1]} m "
             f"({cr.num(EJ['area'])} m²) lleva <b>{EJ['m2']} m²</b>: {cr.tiras_texto(EJ)} y {cr.rollos_texto(EJ)} de envío.")

COMO = (
    ("¿Cuánto mide un rollo de pasto sintético?",
     f"2 m de ancho por 25 m de largo: {ROLLO} m². Lo vendemos por metro cuadrado, así que no tienes que comprar rollos "
     f"completos: te cortamos los m² que pidas (para envío, desde {MIN} m²)."),
    ("¿Hacia dónde van las tiras?",
     "Todas en el mismo sentido, para que la fibra se vea pareja y no se noten las uniones. La calculadora prueba las "
     "tiras a lo largo y a lo ancho y se queda con la que gasta menos material; si empatan, con la de menos uniones."),
    ("¿Por qué pedir más que el área?",
     f"Para los cortes de las orillas y los ajustes al unir tramos. Nuestra {GUIA} recomienda sumar de 5 a 10% y la "
     "calculadora usa 10%. Cuando el ancho no es múltiplo de 2 m, la última tira ya deja sobrante y no se agrega más."),
    ("¿Y si mi espacio no es rectangular?",
     "Divídelo en rectángulos, calcula cada uno y suma los m². Si tiene curvas o jardineras, mándanos un croquis con "
     "medidas por WhatsApp y te decimos cuánto pedir."),
)

FAQ = (
    ("¿Cuántos m² trae un rollo de pasto sintético?",
     f"{ROLLO} m²: 2 m de ancho por 25 m de largo. Se vende por m², desde {MIN} m² con envío a todo México y desde "
     f"{data.MIN_SHOWROOM_M2} m² en el showroom de Cd. Madero."),
    ("¿Cuánto cuesta el envío de un rollo?",
     f"Depende de tu estado: {t.TARIFAS_TEXTO} por rollo de {ROLLO} m², con IVA. De {ROLLO + 1} a {ROLLO * 2} m² son dos "
     "rollos. La tabla de arriba trae el flete de cada estado."),
    ("¿Cuánto cuesta el pasto sintético por m²?",
     f"Desde {dinero(BARATO['rollo'])}/m² en rollo completo ({BARATO['nombre']}). De 10 a 49 m² aplica el precio de corte "
     "mediano de cada modelo, y de 2 a 9 m² el de corte chico, solo en el showroom."),
    ("¿Cuánto tarda en llegar?",
     "Sale de Cd. Madero en 1 a 2 días hábiles y llega de 3 a 5 días hábiles después de confirmar el pago, con guía de "
     "rastreo."),
    ("¿Dan factura?", f"Sí, {datos.FACTURA} a persona física o moral."),
)

CONTENIDO = {
    "tipo": "tienda",
    "meta": {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large",
             "canonical": URL,
             "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
                    ("og:description", DESCRIPCION), ("og:image", f"{SITE}{t.GAL}/{FOTO}.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"),
                                  ("¿Cuántos rollos necesito?", URL)]),),
    "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), ("¿Cuántos rollos?", None)),
    "portada": {
        "kicker": "Calculadora · Rollo de 2 × 25 m",
        "h1": '¿Cuántos rollos de pasto sintético <span class="vt-serif">necesito?</span>',
        "respuesta": RESPUESTA,
        "pos": "50% 50%",
        "mensaje": MENSAJE,
        "href_modelos": "#calcular",
        "texto_modelos": "Calcular con mis medidas",
        "foto": t.foto_obra(FOTO, "(min-width: 1024px) 560px, 100vw", "Pasto de la colección instalado"),
        "datos": (("Rollo", "2 × 25 m", f"{ROLLO} m²"), ("Se vende", "Por m²", f"Envío desde {MIN} m²"),
                  ("Para cortes", "+10%", "Como dice la guía"), ("Envío", "Por rollo", t.TARIFAS_TEXTO),
                  ("Entrega", "3 a 5 días", "Hábiles, con guía de rastreo"), ("Factura", datos.FACTURA, "Persona física o moral")),
    },
    "secciones": (
        {"tipo": "calculadora", "id": "calcular", "rotulo": "Calculadora", "titulo": "Calcula los m² de tu espacio",
         "lede": "Escribe el largo y el ancho en metros. Abajo te sale el precio con envío a tu estado."},
        {"tipo": "cotizar", "id": "precio", "rotulo": "Precio", "titulo": "Precio de tus m² con envío",
         "lede": "Ya trae los m² que calculaste. Elige modelo y estado, y mándanos la cotización por WhatsApp.",
         "modelo": BARATO, "m2": EJ["m2"]},
        {"tipo": "medidas", "id": "medidas", "rotulo": "Medidas comunes",
         "titulo": "Cuántos m² pedir para las medidas más comunes"},
        {"tipo": "preguntas", "id": "como-se-calcula", "rotulo": "Cómo se calcula",
         "titulo": "Cómo calcular el pasto sintético que necesitas", "items": COMO},
        {"tipo": "estados", "id": "envio-por-estado", "rotulo": "Envío", "titulo": "Costo de envío por estado",
         "lede": ("El flete se cobra por rollo de 50 m²: hasta 50 m² es un rollo, de 51 a 100 m² son dos. Llega de 3 a 5 "
                  "días hábiles, con guía de rastreo."),
         "modelo": BARATO},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas frecuentes", "preguntas": FAQ},
    ),
    "cierre": {"titulo": "¿Ya tienes tus medidas?",
               "lede": ("Mándanos el largo, el ancho y tu estado: te respondemos con los m² exactos, el modelo que conviene "
                        "y el precio puesto en tu casa."),
               "mensaje": MENSAJE},
    "scripts_extra": ("/js/vt-rollos.js",),
    "clase_extra": " vt-calculadora",  # terra-calculadora.css
}

PARIDAD = {"meta": seo.paridad(TITULO, DESCRIPCION), "reemplazos": {}, "retirados": {},
           "hero": ("Entrega B del SEO nacional (2026-11-16), página nueva sin captura: hero de marca de las guías de la "
                    "tienda con la respuesta directa (rollo de 2 × 25 m y el ejemplo de 7 × 5 m) y el enlace a la "
                    "calculadora; el plazo de entrega va en el cuadro de datos.")}
