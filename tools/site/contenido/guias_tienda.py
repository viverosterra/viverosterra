"""Guías de la tienda de pasto sintético (entrega D del SEO nacional, 2026-11-16): azotea, alberca, ancho del rollo y
sintético contra natural. Solo datos: la plantilla es plantillas/tienda_guia.py, como /pasto-sintetico/perros.

Nada inventado: pesos, alturas, garantías y precios salen de data.MODELOS (las fichas); la comparación de anchos se
calcula con el mismo algoritmo de tiras que rollos.corte. No se publica cuánto aguanta una azotea (lo decide quien
conozca la estructura), ni cifras de drenaje o de resistencia al cloro (las fichas no las traen), ni precios de pasto
natural fuera de Tampico. Páginas nuevas: sin captura de paridad (generar.NUEVAS).
"""
import math
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
import rollos
from esquema import breadcrumb_schema

SITE = data.SITE
GAL = t.GAL
ROLLO = data.ROLLO_M2
GUIA = '<a href="/blog/como-instalar-pasto-sintetico">guía de instalación</a>'
CALOR = '<a href="/blog/pasto-sintetico-calor-mexico">cómo mantenerlo fresco</a>'
ANCHO_OTRO = 3.66  # 12 pies: el otro ancho que el cliente encuentra al comparar
HERO = ("Página nueva de la entrega D del SEO nacional (2026-11-16): el hero de marca de las guías de la tienda, con un "
        "solo botón de WhatsApp, la respuesta directa como entrada y el cuadro de datos de la guía.")


def kg_rollo(m):
    """Peso de un rollo completo (50 m²) en kg, con el peso total por m² de la ficha."""
    return m["peso_num"] * ROLLO / 1000


def num(v):
    """Hasta dos decimales, sin ceros de sobra: 47.5, 0.95, 3.66, 105."""
    return f"{v:,.2f}".rstrip("0").rstrip(".")


POR_PESO = sorted(data.MODELOS, key=lambda m: m["peso_num"])
LIGERO, PESADO = POR_PESO[0], POR_PESO[-1]
PESADOS = [m["nombre"] for m in data.MODELOS if m["peso_num"] == PESADO["peso_num"]]


def _y(nombres):
    return nombres[0] if len(nombres) == 1 else ", ".join(nombres[:-1]) + " y " + nombres[-1]


def _modelos(*slugs_razones):
    return tuple(slugs_razones)


def _datos(*filas):
    return tuple(filas)


def _pagina(clave, titulo, descripcion, miga, portada, secciones, cierre, foto):
    url = f"{SITE}/pasto-sintetico/{clave}"
    return {
        "tipo": "tienda",
        "meta": {"title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
                 "canonical": url,
                 "og": (("og:type", "article"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                        ("og:description", descripcion), ("og:image", f"{SITE}{GAL}/{foto}.webp"), ("og:locale", "es_MX")),
                 "twitter": (("twitter:card", "summary_large_image"),)},
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), (miga, url)]),),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (miga, None)),
        "portada": {**portada, "href_modelos": "/pasto-sintetico#modelos", "texto_modelos": "Ver los 9 modelos con precio",
                    "foto": t.foto_obra(foto, "(min-width: 1024px) 620px, 100vw", "Pasto de la colección instalado"),
                    "pos": "50% 45%"},
        "secciones": secciones,
        "cierre": cierre,
        "sin_opinion": True,  # la opinión de la cafetería es de Tampico; las guías son para todo México
    }


# ---------- Azotea ----------
def _tabla_pesos():
    filas = tuple((f'<a href="/pasto-sintetico/{m["slug"]}">{m["nombre"]}</a>', f'{m["mm"]} mm', f'{m["peso"]} g/m²',
                   f"{num(kg_rollo(m))} kg", f"${m['rollo']}/m²") for m in POR_PESO)
    return {"cabeza": ("Modelo", "Altura", "Peso por m²", f"Rollo de {ROLLO} m²", "Precio por rollo"), "filas": filas,
            "nota": "Peso total de la ficha de cada modelo (fibra y base). Precio por m² en rollo completo, con IVA; el "
                    "envío se suma según tu estado."}


AZOTEA_PASOS = (
    {"titulo": "Revisa el impermeabilizante", "quien": "tu", "cuando": "Antes",
     "texto": "Que esté en buen estado y que la azotea tenga desnivel hacia la coladera: el pasto no corrige charcos."},
    {"titulo": "Limpia y deja secar", "quien": "tu", "cuando": "El día de la instalación",
     "texto": "Sin polvo ni piedras sueltas, para que el adhesivo pegue y nada se marque debajo del pasto."},
    {"titulo": "Extiende sin clavar", "quien": "tu", "cuando": "Al instalar",
     "texto": "Todas las tiras con la fibra en el mismo sentido; orillas y uniones con adhesivo y cinta de unión. Sin "
              "clavos ni taladro sobre el impermeabilizante."},
    {"titulo": "Deja libre la coladera", "quien": "tu", "cuando": "Al terminar",
     "texto": "Recorta el pasto alrededor de cada coladera para que el agua de lluvia salga sin obstáculo."},
)
AZOTEA_FAQ = (
    ("¿El pasto sintético daña el impermeabilizante?", "No, si no lo clavas ni lo taladras. En azotea se pega con "
     "adhesivo en las orillas y en las uniones, y el agua corre por las perforaciones de la base hacia la coladera."),
    ("¿Cuánto pesa un rollo de pasto sintético?", f"Un rollo de {ROLLO} m² pesa de {num(kg_rollo(LIGERO))} kg "
     f"({LIGERO['nombre']}) a {num(kg_rollo(PESADO))} kg ({_y(PESADOS)}). Para subirlo a la azotea conviene que estén "
     "dos personas o más."),
    ("¿Cuánto peso aguanta mi azotea?", "Depende de tu construcción y no lo podemos saber a distancia. Si además del "
     "pasto vas a poner macetas grandes, muebles o una capa de grava, consúltalo con un arquitecto o ingeniero."),
    ("¿Qué pasa con la lluvia en la azotea?", "La base del pasto es perforada: el agua pasa a la losa y corre por el "
     "desnivel hacia la coladera. Si hoy se encharca sin pasto, se seguirá encharcando con pasto."),
    ("¿Se calienta en la azotea?", f"Sí, al sol directo se calienta como cualquier superficie. Te explicamos {CALOR}."),
    ("¿Envían a mi ciudad?", f"Sí, a los 32 estados, en rollo de 2 × 25 m con factura {datos.FACTURA}. El envío se "
     'cobra por rollo; consulta la <a href="/pasto-sintetico/cuantos-rollos#envio-por-estado">tabla de envío por '
     "estado</a>."),
)


def _azotea():
    aruba = data.BY_SLUG["aruba-10"]
    respuesta = (f"Sí. Pesa de {num(LIGERO['peso_num'] / 1000)} a {num(PESADO['peso_num'] / 1000)} kg por m² y va "
                 "pegado sobre el impermeabilizante, sin clavos.")
    portada = {"kicker": "Guía · Azotea y roof garden", "respuesta": respuesta, "mensaje": "",
               "h1": 'Pasto sintético en azotea <span class="vt-serif">cuánto pesa y cómo se pone</span>',
               "datos": _datos(("Más ligero", f"{LIGERO['peso']} g/m²", LIGERO["nombre"]),
                               ("Rollo más ligero", f"{num(kg_rollo(LIGERO))} kg", f"{ROLLO} m²"),
                               ("Instalación", "Sin clavos", "Adhesivo y cinta"),
                               ("Desde", f"${aruba['rollo']}/m²", aruba["nombre"]),
                               ("Entrega", "3 a 5 días", "A todo México"),
                               ("Factura", datos.FACTURA, "Persona física o moral"))}
    secciones = (
        {"tipo": "tabla", "id": "peso", "rotulo": "Peso", "titulo": "Cuánto pesa cada modelo por m² y por rollo",
         "fila": "Preguntar qué modelo conviene a mi azotea", **_tabla_pesos()},
        {"tipo": "pasos", "id": "instalar", "rotulo": "Instalar", "titulo": "Cómo se pone en una azotea",
         "items": AZOTEA_PASOS},
        {"tipo": "modelos", "id": "modelos", "rotulo": "Modelos", "titulo": "Tres modelos para azotea",
         "items": _modelos(("toscana-18", f"El más ligero de la colección: {LIGERO['peso']} g/m²."),
                           ("aruba-10", "El más económico, con fibra corta que se ve pareja en espacios chicos."),
                           ("toscana-28", "Más volumen si la azotea es tu jardín y la usas todos los días."))},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas sobre pasto en azotea",
         "preguntas": AZOTEA_FAQ},
    )
    mensaje = "Hola, quiero pasto sintético para mi azotea."
    portada["mensaje"] = mensaje
    titulo = "Pasto Sintético en Azotea: Peso por m² y Cómo Instalarlo"
    descripcion = (f"Pasto sintético para azotea: pesa de {LIGERO['peso']} a {PESADO['peso']} g/m² según el modelo, se pega "
                   "sin clavos sobre el impermeabilizante. Envío a todo México.")
    cierre = {"titulo": "Cotiza el pasto para tu azotea",
              "lede": "Dinos tus metros y tu estado: te decimos qué modelo conviene y el precio puesto en tu casa.",
              "mensaje": mensaje}
    return _pagina("azotea", titulo, descripcion, "En azotea", portada, secciones, cierre, "obra-proyecto-05")


# ---------- Alberca ----------
ALBERCA_CUIDADOS = (
    ("Que el agua se aleje de la alberca", "Dale a la base un desnivel hacia fuera, hacia el jardín o una coladera, para "
     "que el agua que sale de la alberca no regrese ni se quede debajo del pasto."),
    ("Base que drene", "Sobre tierra, grava fina o polvo de piedra compactado. Sobre concreto, un piso con desnivel. La "
     "base del pasto es perforada: el agua pasa, pero necesita por dónde salir."),
    ("Orillas bien fijas", f"Junto al borde de la alberca, con adhesivo; en tierra, con clavos. La {GUIA} explica cómo."),
    ("Enjuague con agua dulce", "De vez en cuando, para quitar cloro, sal y arena; luego cepilla la fibra para que quede "
     "de pie."),
)
ALBERCA_FAQ = (
    ("¿Se puede poner pasto sintético alrededor de la alberca?", "Sí. No se hace lodo ni se mete tierra al agua, y drena "
     "por su base perforada si abajo hay desnivel."),
    ("¿El cloro daña el pasto sintético?", "Las fichas no traen una prueba de cloro, así que no te lo prometemos. Lo que "
     "sí recomendamos es enjuagarlo con agua dulce de vez en cuando para que no se acumulen cloro ni sal."),
    ("¿Se calienta junto a la alberca?", f"Sí, al sol se calienta. Un enjuague antes de usarlo lo refresca; aquí te "
     f"explicamos {CALOR}."),
    ("¿Qué modelo aguanta más paso?", "Capri 20, de alta densidad, para áreas con mucho movimiento; Irlanda 25 si "
     "también hay perros."),
    ("¿Cuánto tarda en llegar?", "De 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo."),
)


def _alberca():
    capri = data.BY_SLUG["capri-20"]
    portada = {"kicker": "Guía · Alberca y terraza", "mensaje": "Hola, quiero pasto sintético para el área de la alberca.",
               "respuesta": ("Sí: drena por su base perforada y no hace lodo. Instálalo con desnivel hacia fuera y "
                             "enjuágalo con agua dulce."),
               "h1": 'Pasto sintético para alberca <span class="vt-serif">que drena y no hace lodo</span>',
               "datos": _datos(("Base", "Perforada", "Drena el agua"), ("Desnivel", "Hacia fuera", "Lejos de la alberca"),
                               ("Cuidado", "Enjuague", "Agua dulce"), ("Mucho paso", capri["nombre"], "Alta densidad"),
                               ("Entrega", "3 a 5 días", "A todo México"),
                               ("Factura", datos.FACTURA, "Persona física o moral"))}
    secciones = (
        {"tipo": "preguntas", "id": "instalar", "rotulo": "Instalar", "titulo": "Cómo instalarlo junto a la alberca",
         "items": ALBERCA_CUIDADOS},
        {"tipo": "modelos", "id": "modelos", "rotulo": "Modelos", "titulo": "Tres modelos para el área de alberca",
         "items": _modelos(("capri-20", "Alta densidad para el área con más paso y juego."),
                           ("toscana-28", "Buen volumen y precio para el jardín alrededor de la alberca."),
                           ("irlanda-25", "Fibra firme si también hay perros."))},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas sobre pasto en la alberca",
         "preguntas": ALBERCA_FAQ},
    )
    titulo = "Pasto Sintético para Alberca: Drenaje y Cuidados"
    descripcion = ("Pasto sintético alrededor de la alberca: cómo instalarlo para que drene, qué modelo aguanta más paso y "
                   "cómo cuidarlo del cloro y la sal. Envío a México.")
    cierre = {"titulo": "Cotiza el pasto para tu alberca",
              "lede": "Dinos los metros alrededor de la alberca y tu estado: te respondemos con el precio puesto en tu casa.",
              "mensaje": portada["mensaje"]}
    return _pagina("alberca", titulo, descripcion, "Para alberca", portada, secciones, cierre, "obra-proyecto-03")


# ---------- Ancho del rollo ----------
def tiras(largo, ancho, w):
    """Tiras de ancho w (sentido que gasta menos, como rollos.corte) y m² que se usan, sin el margen de cortes."""
    opciones = []
    for a_lo_largo, cruzado in ((largo, ancho), (ancho, largo)):
        n = math.ceil(cruzado / w - rollos.EPS)
        opciones.append((round(n * w * a_lo_largo, 2), n))
    m2, n = min(opciones)
    return n, m2


def comparacion():
    filas = []
    for largo, ancho in rollos.MEDIDAS_COMUNES:
        area = largo * ancho
        n2, m2 = tiras(largo, ancho, rollos.ROLLO_ANCHO_M)
        n3, m3 = tiras(largo, ancho, ANCHO_OTRO)
        filas.append({"medida": f"{largo} × {ancho} m", "area": area, "n2": n2, "m2": m2, "n3": n3, "m3": m3})
    return filas


def _union(n):
    u = n - 1
    return "sin uniones" if u == 0 else ("1 unión" if u == 1 else f"{u} uniones")


def _ancho():
    filas = comparacion()
    menos_uniones = sum(f["n3"] < f["n2"] for f in filas)
    menos_sobra = sum(f["m2"] < f["m3"] for f in filas)
    total = len(filas)
    tabla = {"cabeza": ("Espacio", "Área", "Rollo de 2 m", f"Rollo de {num(ANCHO_OTRO)} m"),
             "filas": tuple((f["medida"], f"{f['area']} m²",
                             f"{num(f['m2'])} m² · {_union(f['n2'])}", f"{num(f['m3'])} m² · {_union(f['n3'])}")
                            for f in filas),
             "nota": "m² que se cortan del rollo con tiras del largo completo, en el sentido que gasta menos, sin el 10% "
                     "para cortes. Las uniones son las juntas entre tiras."}
    claves = (
        ("Menos uniones con el rollo ancho", f"En {menos_uniones} de las {total} medidas, el rollo de {num(ANCHO_OTRO)} m "
         "deja menos juntas. En espacios anchos se nota."),
        ("Menos sobrante con el rollo de 2 m", f"En {menos_sobra} de las {total} medidas sobra menos con el de 2 m, porque "
         "los patios suelen medir metros enteros y el 2 cabe justo."),
        ("Una unión bien hecha", f"Con la fibra en el mismo sentido, cinta de unión y adhesivo, como explica la {GUIA}."),
        ("Lo que vendemos", f"Solo rollo de 2 × 25 m ({ROLLO} m²). Calcula tus tiras y m² en la "
         '<a href="/pasto-sintetico/cuantos-rollos">calculadora de rollos</a>.'),
    )
    faq = (
        ("¿De qué ancho es el rollo de pasto sintético de Viveros Terra?", f"De 2 m de ancho por 25 m de largo: {ROLLO} m² "
         "por rollo, en los 9 modelos."),
        (f"¿Cuál conviene, rollo de 2 m o de {num(ANCHO_OTRO)} m?", f"Depende de tu espacio. El de {num(ANCHO_OTRO)} m deja "
         f"menos uniones; el de 2 m desperdicia menos en patios de metros enteros ({menos_sobra} de {total} medidas "
         "comunes)."),
        ("¿Se notan las uniones del pasto sintético?", f"Se disimulan si todas las tiras van con la fibra en el mismo "
         f"sentido y se pegan con cinta y adhesivo. La {GUIA} lo explica paso a paso."),
        ("¿Cuántos rollos necesito?", 'Escribe largo y ancho en la <a href="/pasto-sintetico/cuantos-rollos">calculadora '
         "de rollos</a>: te dice las tiras, los m² a pedir con 10% para cortes y los rollos de envío."),
    )
    ejemplo = next(f for f in filas if f["medida"] == "8 × 6 m")
    portada = {"kicker": "Guía · Ancho del rollo", "mensaje": "Hola, quiero cotizar pasto sintético en rollo de 2 m.",
               "respuesta": (f"El de {num(ANCHO_OTRO)} m deja menos uniones; el de 2 m desperdicia menos en patios de "
                             f"metros enteros. Vendemos solo de 2 m."),
               "h1": f'Rollo de 2 m o de {num(ANCHO_OTRO)} m <span class="vt-serif">cuál te conviene</span>',
               "datos": _datos(("Nuestro rollo", "2 × 25 m", f"{ROLLO} m²"),
                               ("Patio de 8 × 6 m", f"{num(ejemplo['m2'])} m²", f"Con 2 m · {_union(ejemplo['n2'])}"),
                               (f"Con {num(ANCHO_OTRO)} m", f"{num(ejemplo['m3'])} m²", _union(ejemplo["n3"]).capitalize()),
                               ("Calculadora", "Tiras y m²", "Con tus medidas"),
                               ("Entrega", "3 a 5 días", "A todo México"),
                               ("Factura", datos.FACTURA, "Persona física o moral"))}
    secciones = (
        {"tipo": "tabla", "id": "comparar", "rotulo": "Comparar", "titulo": "Cuánto se usa con cada ancho",
         "fila": "Cotizar mi rollo de 2 m", **tabla},
        {"tipo": "preguntas", "id": "claves", "rotulo": "Qué cambia", "titulo": "Lo que cambia con el ancho",
         "items": claves},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas sobre el ancho del rollo",
         "preguntas": faq},
    )
    titulo = f"Rollo de Pasto Sintético: 2 m o {num(ANCHO_OTRO)} m de Ancho"
    descripcion = (f"Rollo de pasto sintético de 2 m o de {num(ANCHO_OTRO)} m: uniones y sobrante en 7 medidas comunes de "
                   "patio, con la calculadora de rollos. Envío a todo México.")
    cierre = {"titulo": "Calcula y cotiza tu pasto",
              "lede": 'Mide tu espacio en la <a href="/pasto-sintetico/cuantos-rollos">calculadora de rollos</a> o '
                      "mándanos tus medidas por WhatsApp.",
              "mensaje": portada["mensaje"]}
    return _pagina("ancho-del-rollo", titulo, descripcion, "Ancho del rollo", portada, secciones, cierre,
                   "obra-proyecto-01")


# ---------- Sintético contra natural ----------
def _vs():
    barato = t.barato()
    garantias = sorted({int(a) for m in data.MODELOS for a in str(m["garantia"]).split(" a ")})
    criterios = {"cabeza": ("Qué comparas", "Pasto sintético", "Pasto natural"),
                 "filas": (("Agua", "No se riega; solo un enjuague de vez en cuando", "Riego frecuente, más en secas y calor"),
                           ("Mantenimiento", "Cepillar y enjuagar", "Podar, fertilizar y controlar plagas"),
                           ("Calor", "Se calienta al sol", "Se mantiene más fresco al tacto"),
                           ("Frío y heladas", "Conserva el color", "Se quema o se pone amarillo"),
                           ("Sombra", "Se ve igual", "Se debilita con poca luz"),
                           ("Mascotas", "Necesita enjuague por la orina", "Se hacen manchas y hoyos"),
                           ("Duración", f"Garantía de fábrica de {garantias[0]} a {garantias[-1]} años según el modelo",
                            "Vive mientras se cuide"),
                           ("Costo inicial", f"Desde ${data.landed_m2(barato, 'A')}/m² puesto en el centro del país",
                            "Menor, pero se suma el agua y el mantenimiento")),
                 "nota": "Precio del sintético con " + barato["nombre"] + " en rollo completo con envío al centro y "
                         "occidente del país; el de tu estado está en la tabla de envío por estado."}
    regiones = (
        ("Norte (Monterrey, Saltillo, Chihuahua, Hermosillo)", "Calor seco y temporadas de poca agua: el sintético no "
         "se seca ni pide riego; conviene enjuagarlo en las horas de más calor."),
        ("Centro (CDMX, Toluca, Puebla, Querétaro)", "Heladas en invierno y lluvias en verano: el sintético conserva el "
         "color y drena si la base tiene desnivel."),
        ("Golfo y sureste (Veracruz, Mérida, Villahermosa, Cancún)", "Humedad y lluvias fuertes: lo que decide es la base "
         "que drena; el sintético no tiene tierra donde salgan hongos."),
    )
    cuando = (
        ("Conviene el sintético", "Si no quieres regar ni podar, si el área tiene poca luz o mucho paso, en azoteas y "
         "terrazas, o donde el agua es escasa."),
        ("Conviene el natural", "Si quieres una superficie fresca al sol, tienes tiempo para cuidarlo y agua para "
         "regarlo. En Tampico, Madero y Altamira vendemos e instalamos pasto San Agustín en rollo."),
    )
    faq = (
        ("¿Qué es mejor, pasto sintético o natural?", "Depende del uso: el sintético ahorra agua y mantenimiento; el "
         "natural es más fresco al sol. La tabla compara los dos punto por punto."),
        ("¿Cuánto dura el pasto sintético?", f"Nuestros modelos tienen garantía de fábrica de {garantias[0]} a "
         f"{garantias[-1]} años según el modelo; la de cada uno está en su ficha."),
        ("¿El pasto sintético ahorra agua?", "Sí: no se riega. Solo se enjuaga de vez en cuando para quitar polvo, o más "
         "seguido si hay mascotas."),
        ("¿Y en Tampico?", 'Tenemos una comparación con precios de Tampico, Madero y Altamira: <a '
         'href="/blog/pasto-sintetico-vs-natural-tampico">pasto sintético o natural en Tampico</a>.'),
    )
    portada = {"kicker": "Guía · Sintético o natural", "mensaje": "Hola, quiero cotizar pasto sintético.",
               "respuesta": ("El sintético no se riega ni se poda y aguanta heladas; el natural es más fresco al sol. "
                             "Depende de tu clima y tu uso."),
               "h1": 'Pasto sintético o natural <span class="vt-serif">cuál conviene en tu ciudad</span>',
               "datos": _datos(("Riego", "Ninguno", "Sintético"), ("Mantenimiento", "Enjuague", "Sintético"),
                               ("Garantía", f"{garantias[0]} a {garantias[-1]} años", "Según el modelo"),
                               ("Desde", f"${data.landed_m2(barato, 'A')}/m²", "Puesto en el centro del país"),
                               ("Entrega", "3 a 5 días", "A todo México"),
                               ("Factura", datos.FACTURA, "Persona física o moral"))}
    secciones = (
        {"tipo": "tabla", "id": "comparar", "rotulo": "Comparar", "titulo": "Sintético contra natural, punto por punto",
         "fila": "Cotizar pasto sintético", **criterios},
        {"tipo": "preguntas", "id": "clima", "rotulo": "Clima", "titulo": "Qué cambia según tu región", "items": regiones},
        {"tipo": "preguntas", "id": "cuando", "rotulo": "Decidir", "titulo": "Cuándo conviene cada uno", "items": cuando},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas frecuentes", "preguntas": faq},
    )
    titulo = "Pasto Sintético o Natural: Cuál Conviene en México"
    descripcion = ("Pasto sintético o natural: agua, mantenimiento, calor, heladas y costo, y qué conviene en el norte, el "
                   "centro y el sureste de México.")
    cierre = {"titulo": "Cotiza tu pasto sintético",
              "lede": "Dinos tus metros y tu estado: te respondemos con el modelo que conviene y el precio puesto.",
              "mensaje": portada["mensaje"]}
    return _pagina("vs-natural", titulo, descripcion, "Sintético o natural", portada, secciones, cierre,
                   "obra-proyecto-02")


GUIAS = {"azotea": _azotea, "alberca": _alberca, "ancho-del-rollo": _ancho, "vs-natural": _vs}
CLAVES = tuple(GUIAS)
NOMBRES = {"azotea": "Pasto sintético en azotea", "alberca": "Pasto sintético para alberca",
           "ancho-del-rollo": "Rollo de 2 m o de 3.66 m", "vs-natural": "Pasto sintético o natural"}


def pagina(clave):
    return SimpleNamespace(CONTENIDO=GUIAS[clave](), PARIDAD={"reemplazos": {}, "retirados": {}, "hero": HERO})
