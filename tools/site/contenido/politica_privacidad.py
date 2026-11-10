"""Contenido de /politica-privacidad (plantilla legal). El texto legal es el de main, sin suavizarlo ni agregar compromisos;
el domicilio sale de datos.py. Se suman a la sección de transferencias los encargados que ya existen (paquetería, servicio
de formularios, cobro con tarjeta), sin nombrar al proveedor de la terminal: ver C10 del plan. El marco legal citado no se
toca: lo revisa el abogado del dueño."""
import datos
import mensajes_paginas
from contenido import seo

SITE = datos.SITIO
URL = f"{SITE}/politica-privacidad"
ACTUALIZADO = "noviembre de 2026"
TEL, CORREO = datos.TELEFONO_VISIBLE, datos.CORREO_FORMULARIOS
SECCIONES = (
    {"id": "responsable", "titulo": "Responsable", "bloques": (
        ("p", f"<strong>Responsable:</strong> Viveros Terra, con domicilio en {datos.CALLE}, Cd. Madero, Tamaulipas, México. "
              f"Contacto: {CORREO} · WhatsApp {TEL}."),)},
    {"id": "datos", "titulo": "1. Datos personales que recabamos", "corto": "Datos que recabamos", "bloques": (
        ("p", "En Viveros Terra recabamos los siguientes datos personales únicamente cuando usted nos contacta para "
              "solicitar un servicio o cotización:"),
        ("ul", ("Nombre completo", "Número telefónico (vía WhatsApp o llamada)", "Correo electrónico (si lo proporciona)",
                "Dirección del inmueble donde se prestará el servicio",
                f"Datos fiscales en caso de requerir factura {datos.FACTURA} (RFC, razón social, régimen)")),)},
    {"id": "finalidad", "titulo": "2. Finalidad del tratamiento de datos", "corto": "Finalidad", "bloques": (
        ("p", "Sus datos personales serán utilizados para las siguientes finalidades:"),
        ("ol", ("<strong>Finalidades primarias:</strong> contactarle para responder cotizaciones, agendar visitas técnicas, "
                "ejecutar los servicios contratados, emitir facturación y dar seguimiento postventa.",
                "<strong>Finalidades secundarias:</strong> envío ocasional de promociones, recordatorios estacionales de "
                "mantenimiento y comunicaciones comerciales relacionadas con jardinería.")),
        ("p", f'Si no desea recibir comunicaciones secundarias, puede manifestarlo respondiendo "BAJA" al WhatsApp {TEL}.'),)},
    {"id": "transferencia", "titulo": "3. Transferencia de datos", "corto": "Transferencia", "bloques": (
        ("p", "Viveros Terra <strong>no vende, alquila ni comparte sus datos personales con terceros</strong> con fines "
              "comerciales. Solo compartimos información estrictamente necesaria con:"),
        ("ul", (f"El SAT, cuando se emiten comprobantes fiscales digitales ({datos.FACTURA}).",
                "Proveedores de servicio de mensajería (WhatsApp Business) bajo sus propios términos.",
                "Paqueterías, para entregar su pedido; el servicio que nos hace llegar por correo los formularios de este "
                "sitio; y el procesador de pagos con tarjeta, cuando usted paga con link de pago.",
                "Autoridades cuando exista requerimiento legal fundado.")),)},
    {"id": "arco", "titulo": "4. Derechos ARCO", "corto": "Derechos ARCO", "bloques": (
        ("p", "Usted tiene derecho a <strong>Acceder, Rectificar, Cancelar u Oponerse</strong> al tratamiento de sus datos "
              "personales en cualquier momento. Para ejercer estos derechos:"),
        ("ul", (f'<strong>Correo:</strong> {CORREO} con asunto "Derechos ARCO"',
                f'<strong>WhatsApp:</strong> <a data-cta="utilidad:cuerpo" href="https://wa.me/{datos.TELEFONO_WA}">{TEL}</a>',
                f"<strong>Presencial:</strong> {datos.CALLE}, Cd. Madero, Tamaulipas. Lunes a viernes, 9am–6pm.")),
        ("p", "Responderemos su solicitud en un plazo máximo de 20 días hábiles, conforme al artículo 32 de la LFPDPPP."),)},
    {"id": "cookies", "titulo": "5. Uso de cookies y tecnologías de rastreo", "corto": "Cookies", "bloques": (
        ("p", f"Nuestro sitio web utiliza <strong>Google Analytics 4</strong> (ID: {datos.GA4_ID}) para medir el tráfico y "
              "mejorar la experiencia del usuario. Estas cookies son anónimas y agregadas, no permiten identificarle "
              "personalmente. Puede deshabilitarlas desde la configuración de su navegador o instalando el complemento de "
              "inhabilitación de Google Analytics."),)},
    {"id": "seguridad", "titulo": "6. Seguridad de los datos", "corto": "Seguridad", "bloques": (
        ("p", "Viveros Terra implementa medidas administrativas, técnicas y físicas razonables para proteger sus datos "
              "contra daño, pérdida, alteración o acceso no autorizado. Los datos fiscales se procesan a través de "
              "proveedores certificados por el SAT."),)},
    {"id": "modificaciones", "titulo": "7. Modificaciones al aviso", "corto": "Modificaciones", "bloques": (
        ("p", "Cualquier modificación a esta política será publicada en esta misma página con la fecha de actualización "
              "correspondiente. Le recomendamos revisarla periódicamente."),)},
    {"id": "aceptacion", "titulo": "8. Aceptación", "corto": "Aceptación", "bloques": (
        ("p", "Al contactarnos por cualquier medio (WhatsApp, llamada, correo o formulario web), usted manifiesta que ha "
              "leído, comprende y acepta los términos de este Aviso de Privacidad."),
        ("p", "<strong>Marco legal:</strong> Esta política se rige por la Ley Federal de Protección de Datos Personales en "
              "Posesión de los Particulares (LFPDPPP), publicada el 5 de julio de 2010, y su Reglamento, así como por los "
              "lineamientos del INAI."),)},
)
# SEO fase 0 (mapa de palabras clave, 2026-11-10): noindex, follow y fuera del sitemap. Google la mostraba para «vivero
# ciudad madero» con un domicilio viejo; un aviso legal no debe competir por consultas locales.
TITULO = f"Aviso de Privacidad | {datos.NOMBRE}"
DESCRIPCION = (f"Aviso de privacidad de {datos.NOMBRE}: qué datos personales recabamos, para qué los usamos y cómo "
               "contactarnos para ejercer tus derechos.")
CONTENIDO = {
    "tipo": "utilidad",
    "meta": {"title": TITULO, "description": DESCRIPCION, "robots": "noindex, follow", "canonical": URL, "og": ()},
    "cabeza": {"migas": (("Inicio", "/"), ("Aviso de privacidad", None)), "kicker": "Aviso de Privacidad Integral",
               "h1": "Política de Privacidad", "lede": f"Última actualización: {ACTUALIZADO}."},
    "secciones": SECCIONES,
    "cierre": {"titulo": "¿Dudas sobre tus datos?", "lede": f"Escríbenos: {datos.PROMESA.lower()}.",
               "mensaje": mensajes_paginas.UTILITARIAS["privacidad"]},
    "jsonld": (),
}
NOINDEX = ("SEO fase 0 (2026-11-10): noindex, follow. Google la mostraba para búsquedas locales del vivero; sigue enlazada "
           "desde el pie y desde /politicas.")
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {},
           "meta": seo.paridad(TITULO, DESCRIPCION, {"robots": ("noindex, follow", NOINDEX)}, claves=("title", "description"))}
