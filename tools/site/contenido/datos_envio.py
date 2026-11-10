"""Contenido de /datos-envio (noindex, nofollow): el asesor lo manda por WhatsApp con ?d=…; vt-datos-envio.js arma el
mensaje de vuelta. Mismos id que main (el JS y el texto #VT1 dependen de ellos). Sin formsubmit: nada sale de la página."""
import datos
import componentes_util as cu

URL = f"{datos.SITIO}/datos-envio"


def _c(ident, label, error=None, tipo="text", req=True, **extra):
    return cu.campo({"label": label, "id": ident, "tipo": tipo, "requerido": req, "error": error, **extra})


REGIMENES = ("601 · General de Ley Personas Morales", "603 · Personas Morales con Fines no Lucrativos",
             "605 · Sueldos y Salarios e Ingresos Asimilados a Salarios", "606 · Arrendamiento",
             "612 · Personas Físicas con Actividades Empresariales y Profesionales", "616 · Sin obligaciones fiscales",
             "621 · Incorporación Fiscal", "625 · Actividades Empresariales a través de Plataformas Tecnológicas",
             "626 · Régimen Simplificado de Confianza")
USOS = ("G01 · Adquisición de mercancías", "G03 · Gastos en general", "S01 · Sin efectos fiscales")

DIRECCION = (
    _c("calle", "Calle y número", "Escribe la calle y el número.", completar="address-line1",
       placeholder="Ej. Av. Hidalgo 1234, int. 5"),
    cu.fila(_c("colonia", "Colonia", "Escribe la colonia.", completar="address-level3"),
              _c("cp", "Código postal", "Deben ser 5 dígitos.", modo="numeric", max="5", completar="postal-code"),
              _c("municipio", "Municipio", "Escribe el municipio.", completar="address-level2"),
              _c("estado", "Estado", "Elige el estado.", tipo="lista", opciones=(), completar="address-level1"), columnas=2),
    _c("ref", "Referencias", "Las referencias son obligatorias para la paquetería.",
         placeholder="Entre qué calles o un punto de referencia",
         pista="Ej. entre Juárez y Morelos, portón negro frente a la farmacia."),
)
RECIBE = (_c("recibe", "Nombre completo de quien recibe", "Escribe nombre y apellidos.", completar="name"),
          _c("tel", "Teléfono de contacto", "Deben ser 10 dígitos.", tipo="tel", modo="tel", completar="tel",
               placeholder="10 dígitos"),)
FACTURA = (
    cu.fila(_c("rfc", "RFC", "Revisa el RFC (12 o 13 caracteres).", req=False, max="13"),
            _c("fcp", "C.P. fiscal", "Deben ser 5 dígitos.", req=False, modo="numeric", max="5"), columnas=2),
    _c("razon", "Nombre o razón social", "Escribe el nombre o razón social.", req=False,
         pista="Tal como aparece en tu constancia de situación fiscal."),
    _c("regimen", "Régimen fiscal", "Elige tu régimen fiscal.", req=False, tipo="lista",
         opciones=(("", "Elige tu régimen"),) + tuple((None, r) for r in REGIMENES)),
    _c("uso", "Uso de CFDI", "Elige el uso de CFDI.", req=False, tipo="lista",
         opciones=(("", "Elige el uso"),) + tuple((None, u) for u in USOS)),
    _c("correo", "Correo para recibir la factura", "Revisa el correo.", req=False, tipo="email", modo="email", completar="email"),
)

CONTENIDO = {
    "tipo": "utilidad", "vista": "datos_envio", "scripts": ("/js/vt-datos-envio.js",),
    "meta": {"title": "Datos de envío · Viveros Terra",
             "description": "Comparte la dirección de entrega de tu pedido de pasto sintético.",
             "robots": "noindex, nofollow", "canonical": URL, "og": ()},
    "cabeza": {"kicker": "Tu pedido", "h1": '<span id="hola">Datos para tu envío</span>',
               "lede": "Llénalo en un minuto. Al terminar se abre WhatsApp con tus datos listos para enviárnoslos."},
    "tarjetas": ({"id": "vt-h-direccion", "titulo": "Dirección de entrega", "controles": DIRECCION},
                 {"id": "vt-h-recibe", "titulo": "¿Quién recibe?", "controles": RECIBE}),
    "factura": FACTURA,
    "nota": "Tus datos solo viajan por WhatsApp a Viveros Terra; esta página no los guarda.",
}
PARIDAD = {"reemplazos": {}, "retirados": {},
           "meta": {"canonical": (URL, "Cada página con plantilla lleva canonical; esta noindex no tenía.")},
           "jsonld": {}}
