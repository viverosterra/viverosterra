"""Contenido de /post/nochebuenas-tampico-madero-mayoreo. Solo datos: la plantilla es plantillas/nochebuenas.py.

Precios, cortes y fechas salen de datos.NOCHEBUENAS. Decisiones del dueño (2026-11-09): sin garantía ni reposición en esta
página, sin opiniones con nombre (son de otros servicios) y sin "con IVA" (las plantas no llevan IVA). 50% de anticipo solo
aquí. Página nueva: sin captura previa, por eso PARIDAD va vacío y test_paridad.py la excluye.
"""
import datos
import mensajes_paginas
from componentes import dinero
from contenido import plantas_comun as pc
from contenido.nochebuenas_fotos import FOTOS

NB = datos.NOCHEBUENAS
RUTA = NB["ruta"]
URL = f"{datos.SITIO}{RUTA}"
TIPO = "nochebuenas"
ANIO = NB["temporada"]
MENSAJES = mensajes_paginas.NOCHEBUENAS
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
         "diciembre")
PRODUCTO_CHICO = NB["productos"][0]
DESDE_MENUDEO = PRODUCTO_CHICO["precios"][0]
DESDE_MAYOREO = PRODUCTO_CHICO["precios"][1]
DESDE_VOLUMEN = min(p["precios"][-1] for p in NB["productos"])
MINIMO_MAYOREO = NB["cortes"][1]
PIEZAS_PROYECTO = NB["cortes"][-1]
ENTREGA_DESDE = dinero(NB["entrega_incluida_desde"])
ANTICIPO = f'{NB["anticipo_pct"]}%'


def fecha_larga(iso, con_anio=False):
    """"2026-11-20" → "20 de noviembre" (con_anio: "20 de noviembre de 2026")."""
    anio, mes, dia = iso.split("-")
    texto = f"{int(dia)} de {MESES[int(mes) - 1]}"
    return f"{texto} de {anio}" if con_anio else texto


LIMITE_PREVENTA = fecha_larga(NB["preventa"]["hasta"])
LIMITE_MAYOREO = fecha_larga(NB["fecha_limite_mayoreo"])
ENTREGA_MAYOREO = fecha_larga(NB["entrega_mayoreo_antes"])
PIDE_ANTES = f"Pide antes del {LIMITE_MAYOREO}"

HERO = next(f for f in FOTOS if f["uso"] == "hero")
GALERIA = tuple(f for f in FOTOS if f["uso"] != "hero")
TITULO = f"Nochebuenas en Tampico desde {dinero(DESDE_VOLUMEN)} · Mayoreo {ANIO} | Viveros Terra"
DESCRIPCION = ('Nochebuena roja, rosa y jaspeada en 5", 6", 7", colgante y macetón. Precio por volumen, factura y entrega en '
               "Tampico, Madero y Altamira.")
SUBTITULO = (f"Desde {dinero(DESDE_VOLUMEN)} por pieza en volumen · Factura CFDI · Entrega en Tampico, Madero y Altamira")

META = {
    "title": TITULO,
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": URL,
    "og": (("og:type", "website"), ("og:url", URL), ("og:title", TITULO), ("og:description", DESCRIPCION),
           ("og:image", datos.SITIO + HERO["src"].replace("-800.webp", "-1600.webp")), ("og:image:width", "1600"),
           ("og:image:height", "1200"), ("og:locale", "es_MX")),
}
_TITULO_POST = "Nochebuenas en Tampico: cuidados y próxima temporada | Viveros Terra"
_DESCRIPCION_POST = (f"Temporada {ANIO} cerrada. Cuidados de la nochebuena en el clima de Tampico, fotos y aviso para la próxima "
                     "temporada.")
META_POSTEMPORADA = dict(META, title=_TITULO_POST, description=_DESCRIPCION_POST, og=(
    ("og:type", "website"), ("og:url", URL), ("og:title", _TITULO_POST), ("og:description", _DESCRIPCION_POST),
    *[par for par in META["og"] if par[0].startswith("og:image") or par[0] == "og:locale"]))
FRANJA = (("Desde", str(datos.DESDE), "En Cd. Madero y Tampico"),
          ("Google", datos.GOOGLE, "Calificación pública"),
          ("Factura", datos.FACTURA, "Persona física o moral"),
          ("Entrega", "A domicilio", "Tampico, Madero y Altamira"))
ETIQUETA = {"codigo": "Nochebuena", "aviso": f"Precios {ANIO}", "nombre": "Por volumen", "antes": "desde",
            "monto": dinero(DESDE_VOLUMEN), "unidad": "por pieza",
            "filas": (('Maceta 5", menudeo', dinero(DESDE_MENUDEO)), (f"Mayoreo, {MINIMO_MAYOREO} piezas", dinero(DESDE_MAYOREO)),
                      (f"{PIEZAS_PROYECTO} piezas o más", dinero(DESDE_VOLUMEN)))}
ETIQUETA_PREVENTA = dict(ETIQUETA, antes="Precio de referencia, desde")
PORTADAS = {
    "temporada": {"kicker": f"Temporada {ANIO} · Pedidos abiertos", "h1": f"Nochebuenas {ANIO} en Tampico: menudeo y mayoreo",
                  "lede": SUBTITULO, "cta": "Cotizar mi pedido", "wa": "WhatsApp"},
    "preventa": {"kicker": f"Preventa {ANIO} · Apartado abierto", "h1": f"Aparta tus Nochebuenas {ANIO} para tu empresa",
                 "lede": ("Precios de referencia por volumen · Factura CFDI · Entrega en Tampico, Madero y Altamira"),
                 "cta": "Apartar mi pedido", "wa": "Apartar por WhatsApp"},
    "postemporada": {"kicker": f"Temporada {ANIO} cerrada · Gracias", "h1": "Nochebuenas en Tampico: cuidados y próxima temporada",
                     "lede": ("Gracias por esta temporada. Aquí siguen los cuidados, las fotos y las preguntas de siempre. "
                              "Te avisamos cuando abra la próxima temporada."),
                     "cta": ""},
}
AVISO = "Avísame en la próxima temporada"

COTIZADOR = {
    "titulo": "Arma tu pedido y mira el total",
    "lede": "Agrega tamaños y colores. El precio baja con el total de piezas.",
    "cta": {"temporada": "Enviar pedido por WhatsApp", "preventa": "Apartar por WhatsApp"},
    "nota": "Se abre WhatsApp con tu pedido escrito. Tú decides si lo envías.",
}
TABLA = {
    "titulo": "Precio por pieza según el total del pedido",
    "titulo_referencia": "Precios de referencia por pieza",
    "caption": f"Nochebuenas {ANIO}: precio por pieza, en pesos, según el total de piezas del pedido.",
    "caption_referencia": f"Precios de referencia {ANIO}, en pesos, según el total de piezas del pedido.",
    "nota": ("Los escalones se calculan con el total del pedido: puedes combinar tamaños y colores. Mismo precio en roja, "
             "rosa y jaspeada. Rosa y jaspeada, sobre pedido."),
}
PARA = (
    {"id": "empresas", "titulo": "Empresas y regalos corporativos", "corto": "tu empresa",
     "detalle": "Empaque kraft, entrega a varios domicilios y CFDI.",
     "mensaje": ("Hola, quiero cotizar Nochebuenas para regalos de mi empresa.\nEmpresa: ___\nPiezas aprox.: ___\n"
                 "Domicilios de entrega: ___\nRequiero CFDI.")},
    {"id": "hoteles", "titulo": "Hoteles y restaurantes", "corto": "tu hotel o restaurante",
     "detalle": "Precio por volumen y CFDI.",
     "mensaje": ("Hola, quiero cotizar Nochebuenas para mi hotel o restaurante.\nNegocio y ubicación: ___\nPiezas aprox.: ___\n"
                 "Fecha de entrega: ___")},
    {"id": "comercios", "titulo": "Plazas y comercios", "corto": "tu plaza o comercio",
     "detalle": "Instalación y mantenimiento disponibles.",
     "mensaje": ("Hola, quiero cotizar Nochebuenas para una plaza o comercio.\nLugar: ___\nPiezas aprox.: ___\n"
                 "¿Necesitan instalación y mantenimiento?: ___")},
    {"id": "gobierno", "titulo": "Gobierno y ayuntamientos", "corto": "tu dependencia",
     "detalle": "Cotización formal con CFDI.",
     "mensaje": ("Hola, necesitamos una cotización formal de Nochebuenas con CFDI.\nDependencia: ___\nPiezas aprox.: ___\n"
                 "Fecha de entrega: ___")},
    {"id": "posadas", "titulo": "Posadas y eventos", "corto": "tu posada o evento",
     "detalle": "Precio por volumen, sumando tamaños y colores.",
     "mensaje": "Hola, quiero cotizar Nochebuenas para una posada o evento.\nFecha: ___\nPiezas aprox.: ___\nColonia: ___"},
    {"id": "iglesias", "titulo": "Iglesias y escuelas", "corto": "tu iglesia o escuela",
     "detalle": "Altares del 12 de diciembre.",
     "mensaje": ("Hola, quiero cotizar Nochebuenas para una iglesia o escuela.\nLugar: ___\nPiezas aprox.: ___\n"
                 "Fecha de entrega: ___")},
)
PARA_TITULO = "¿Para quién es este pedido?"
MINIMO_SUGERIDO = f"Mínimo sugerido: {MINIMO_MAYOREO} piezas"
GALERIA_TEXTO = {"titulo": "Fotos reales de temporadas anteriores", "lede": "Nochebuena roja. Rosa y jaspeada, sobre pedido y al mismo precio."}
CONFIANZA = {"titulo": "Referencias y factura",
             "sellos": ((datos.GOOGLE, "Calificación pública del vivero"), (datos.FACTURA, "Factura para persona física o moral")),
             "clientes": "Empresas e instituciones que han confiado en Viveros Terra"}
COMO = {
    "titulo": "Cómo funciona tu pedido",
    "pasos": (
        {"titulo": "Cotizas en línea", "quien": "tu", "cuando": "En esta página",
         "texto": "Eliges tamaño, color y cantidad. El total se calcula al momento."},
        {"titulo": "Confirmas y apartas por WhatsApp", "quien": "juntos", "cuando": "Al confirmar",
         "texto": f"Revisamos tu pedido contigo y lo apartas con {ANTICIPO} de anticipo en mayoreo y en precio preventa."},
        {"titulo": "Recibes en tu domicilio o recoges en el vivero", "quien": "nosotros", "cuando": "En la fecha acordada",
         "texto": "Tú eliges. Entregamos en Tampico, Madero y Altamira."},
    ),
    "fechas": ((NB["preventa"]["hasta"], f"Precio preventa hasta el {LIMITE_PREVENTA}"),
               (NB["fecha_limite_mayoreo"], f"Mayoreo con entrega antes del {ENTREGA_MAYOREO}: confirma antes del {LIMITE_MAYOREO}")),
}
CUIDADOS = {
    "titulo": "Cuidados en el clima de Tampico",
    "lede": "Con el calor de la costa, cuida la luz y el riego.",
    "items": (
        {"titulo": "Luz", "texto": "Luz brillante indirecta, sin sol directo."},
        {"titulo": "Temperatura", "texto": "Entre 18–24 °C. Lejos del aire acondicionado."},
        {"titulo": "Riego", "texto": "Riega cuando la tierra esté apenas seca, sin agua acumulada en el cubremaceta."},
        {"titulo": "Duración", "texto": "Bien cuidada, te dura hasta febrero."},
    ),
}


def _precios_por_tamano():
    """Frase generada de datos: menudeo y mayoreo de cada tamaño y el macetón sobre pedido."""
    regulares = "; ".join(f'{p["nombre"]} {dinero(p["precios"][0])} y {dinero(p["precios"][1])}'
                          for p in NB["productos"] if not p.get("sobre_pedido"))
    sobre = next(p for p in NB["productos"] if p.get("sobre_pedido"))
    return f'Por tamaño, en menudeo y mayoreo: {regulares}. {sobre["nombre"]} sobre pedido, desde {dinero(sobre["precios"][-1])}.'


_MAYOREO_5, _MAYOREO_6 = (next(p["precios"][1] for p in NB["productos"] if p["clave"] == clave) for clave in ("5", "6"))
RESPUESTA_PRECIO = (f"En Viveros Terra, desde {dinero(DESDE_MENUDEO)} la de 5 pulgadas en menudeo y desde {dinero(DESDE_VOLUMEN)} en "
                    f"pedidos de {PIEZAS_PROYECTO} piezas o más. {_precios_por_tamano()}")
PREGUNTA_PRECIO = "¿Cuánto cuesta una nochebuena en Tampico?"
PREGUNTAS = (
    (PREGUNTA_PRECIO, RESPUESTA_PRECIO),
    ("¿Desde cuántas piezas es mayoreo?",
     f'Desde {MINIMO_MAYOREO} piezas, sumando tamaños y colores. {dinero(_MAYOREO_5)} la de 5" y {dinero(_MAYOREO_6)} la de 6".'),
    ("¿Entregan en Madero y Altamira?",
     f"Sí. La entrega va incluida desde {ENTREGA_DESDE} por pedido. Debajo de ese monto, según tu ubicación o colonia y te la cotizamos por WhatsApp."),
    ("¿Facturan?", f"Sí, con {datos.FACTURA}."),
    ("¿Cuándo debo pedir para empresas o posadas?",
     "Lo antes posible. Confírmanos por WhatsApp y te decimos la fecha de entrega."),
    ("¿Cuánto dura una nochebuena?", "Bien cuidada, hasta febrero."),
    ("¿Cómo la cuido con el calor de Tampico?",
     "Dale luz brillante indirecta, sin sol directo, entre 18–24 °C. Riega cuando la tierra esté apenas seca, sin agua acumulada "
     "en el cubremaceta, y déjala lejos del aire acondicionado."),
    ("¿Es tóxica para perros y gatos?",
     "Puede irritar la boca y el estómago. Mantenla fuera de su alcance. Ante síntomas, consulta al veterinario."),
    ("¿Tienen nochebuena rosa y jaspeada?", "Sí, sobre pedido y al mismo precio que la roja."),
)
# Preventa: la misma respuesta de precio, rotulada como referencia. Postemporada: solo lo que sigue vigente sin oferta.
PREGUNTAS_PREVENTA = tuple((q, f"{a} Son precios de referencia.") if q == PREGUNTA_PRECIO else (q, a) for q, a in PREGUNTAS)
PREGUNTAS_POSTEMPORADA = tuple(p for p in PREGUNTAS if p[0] in (
    "¿Cuánto dura una nochebuena?", "¿Cómo la cuido con el calor de Tampico?", "¿Es tóxica para perros y gatos?"))
FUENTE_MORELOS = ("https://www.elsiglodetorreon.com.mx/noticia/2023/floricultores-alistan-cosecha-de-nochebuena-para-cubrir-"
                  "proxima-demanda-nacional-sader.html")
DATOS_PLANTA = {
    "titulo": "Datos de la nochebuena",
    "items": (
        ("Su origen", "La nochebuena es originaria de México."),
        ("8 de diciembre", "Día Nacional de la Nochebuena."),
        ("Morelos", f'Es el principal productor del país, según datos de la Secretaría de Agricultura citados por <a href="{FUENTE_MORELOS}" target="_blank" rel="noopener">El Siglo de Torreón (2023)</a>.'),
    ),
}
CIERRE = {
    "titulo": "¿Ya tienes tu lista?", "lede": "Mándanos tamaños, colores y fecha. Te confirmamos disponibilidad y entrega.",
    "titulo_postemporada": "Nos vemos la próxima temporada", "lede_postemporada": "Escríbenos y te avisamos cuando abramos pedidos.",
    "actualizacion": f"Última actualización: {fecha_larga(NB['ultima_actualizacion'], con_anio=True)}",
}

CONTENIDO = {
    "tipo": TIPO,
    "meta": META,
    "migas": pc.migas("Nochebuenas"),
    "portadas": PORTADAS,
    "franja": FRANJA,
    "etiquetas": {"temporada": ETIQUETA, "preventa": ETIQUETA_PREVENTA},
    "mensajes": MENSAJES,
    "mismo_precio": "Mismo precio en roja, rosa y jaspeada. Rosa y jaspeada, sobre pedido.",
    "aviso": AVISO,
    "cotizador": COTIZADOR,
    "tabla": TABLA,
    "para": {"titulo": PARA_TITULO, "minimo": MINIMO_SUGERIDO, "pide_antes": PIDE_ANTES, "items": PARA},
    "galeria": GALERIA_TEXTO,
    "meta_postemporada": META_POSTEMPORADA,
    "confianza": CONFIANZA,
    "como": COMO,
    "cuidados": CUIDADOS,
    "faq": {"titulo": "Preguntas frecuentes", "preguntas": PREGUNTAS,
            "por_modo": {"preventa": PREGUNTAS_PREVENTA, "postemporada": PREGUNTAS_POSTEMPORADA}},
    "datos_planta": DATOS_PLANTA,
    "cierre": CIERRE,
    "jsonld": {"migas": pc.migas_ld("Nochebuenas", RUTA), "negocio": pc.NEGOCIO, "imagen": datos.SITIO + HERO["src"]},
}

PARIDAD = {"reemplazos": {}, "retirados": {}}
