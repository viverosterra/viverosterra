"""public/llms.txt y public/llms-full.txt, generados en el build desde datos.py, tools/pasto/data.py y el contenido de las
páginas (SEO fase 1, 2026-11-10). Antes llms.txt se mantenía a mano y se desfasaba (IVA, REPSE, zonas y plazos que el
sitio no respalda).

llms.txt sigue el formato de llmstxt.org: H1, resumen en cita, datos sin encabezado y secciones H2 que solo contienen
listas de enlaces `- [Título](URL): descripción`. llms-full.txt es el texto esencial de las páginas que venden: la
respuesta directa, las condiciones y las preguntas frecuentes de cada una, tal como se publican.

Reglas: cada cifra sale de datos.PRECIOS, datos.NOCHEBUENAS, data.py o mensualidades.py (tests/test_llms.py lo exige);
el pasto sin instalar y las plantas no llevan IVA; sin plazos de entrega, sin porcentajes de anticipo y sin la palabra
"gratis"; "sin costo" solo en la garantía de arraigo del pasto; cada enlace es una página que el build genera.
"""
import sys
from pathlib import Path

import componentes as c
import datos
import entidad
import generar
import paginas

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "pasto"))
import data  # noqa: E402  (tools/pasto)
import mensualidades  # noqa: E402  (tools/pasto)

P = datos.PRECIOS
NB = datos.NOCHEBUENAS
SITIO = datos.SITIO
DIAS = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", "Thursday": "jueves", "Friday": "viernes",
        "Saturday": "sábado"}
RESUMEN = (
    f"{datos.NOMBRE} es un vivero y empresa de jardinería con sede en {datos.CIUDAD}, {entidad.ESTADO}, México, fundada "
    f"el {int(datos.FUNDACION[8:])} de {entidad.mes_largo(datos.FUNDACION)}. Atiende Tampico, Ciudad Madero y Altamira: "
    "vende e instala pasto San Agustín en rollo y pasto sintético, diseña jardines, instala riego automático, da "
    "mantenimiento a áreas verdes y vende plantas, palmas, árboles y materiales para jardín. Envía pasto sintético a "
    f"todo México desde {datos.SINTETICO_NACIONAL_DESDE}.")
REGLA_IVA = ("Regla de IVA: el pasto San Agustín sin instalar (menudeo y mayoreo) y las plantas, palmas y árboles no "
             "llevan IVA. El pasto instalado, el pasto sintético, los materiales y los servicios ya incluyen IVA.")

# Secciones de enlaces de llms.txt: (título, ((nombre, ruta, descripción), …)). Cada ruta debe estar en generar.PAGINAS.
SECCIONES = (
    ("Precios y empresa", (
        ("Lista de precios", "/precios", "todos los precios vigentes en tablas, con la regla de IVA"),
        ("Vivero en Tampico y Ciudad Madero", "/vivero-tampico", "dirección, horario y cómo llegar"),
        ("Nosotros", "/nosotros", f"historia desde {datos.DESDE}, cifras, REPSE, clientes y perfiles oficiales"),
        ("Áreas verdes para empresas", "/empresas",
         f"mantenimiento, pasto al mayoreo, palmas y riego con REPSE {datos.REPSE} y factura {datos.FACTURA}"),
        ("Políticas y garantías", "/politicas", "garantía de pasto y de plantas, mensualidades, anticipos y devoluciones"),
        ("Inicio", "/", "resumen de servicios y cotizador por m²"),
    )),
    ("Pasto natural", (
        ("Pasto San Agustín en rollo", "/pasto-en-rollo-tampico",
         "precio por m², qué incluye la instalación, pasos y garantía de arraigo"),
        ("Pasto al mayoreo", "/mayoreo-pasto-tampico",
         f"desde {P['pasto_mayoreo_minimo_m2']} m², entrega por etapas para obras y fraccionamientos"),
        ("Protocolo de cuidados del pasto San Agustín", "/protocolo-cuidados-pasto-san-agustin",
         "riego de los primeros 20 días y condiciones de la garantía"),
        ("Cuándo plantar pasto en Tampico", "/blog/cuando-plantar-pasto-tampico-calendario", "calendario mes a mes"),
        ("San Agustín o japonés", "/blog/pasto-san-agustin-vs-japones", "comparativa con tabla"),
        ("Guía de instalación y mantenimiento", "/blog/pasto-san-agustin-instalacion-mantenimiento",
         "del suelo al primer corte"),
    )),
    ("Servicios de jardín", (
        ("Diseño de jardines", "/diseno-jardines-tampico", "Plan Terra en tres niveles y qué entrega cada uno"),
        ("Sistema de riego automático", "/sistema-riego-tampico", "tipos de sistema, precio por m² y pasos de instalación"),
        ("Mantenimiento de jardines", "/mantenimiento-jardines-tampico", "planes, frecuencias y qué incluyen"),
        ("Poda y derribo de árboles y palmas", "/poda-arboles-tampico",
         "precio desde, derribo, retiro de residuos aparte y quién tramita el permiso"),
        ("Cuánto cuesta un jardín en Tampico", "/blog/cuanto-cuesta-jardin-tampico-precios",
         "ejemplos de presupuesto con los precios oficiales"),
    )),
    ("Pasto sintético", (
        ("Pasto sintético en Tampico", "/pasto-sintetico-tampico", "venta en showroom e instalación local"),
        ("Tienda con envío a todo México", "/pasto-sintetico",
         f"{len(data.MODELOS)} modelos, fichas técnicas, cotizador y tabla de envío"),
        ("Pasto sintético para perros", "/pasto-sintetico/perros", "modelo, drenaje, olor y limpieza"),
        ("Cuánto cuesta el pasto sintético en México", "/blog/cuanto-cuesta-pasto-sintetico-mexico",
         "precios por modelo y por ciudad"),
        ("Sintético o natural", "/blog/pasto-sintetico-vs-natural-tampico", "comparativa para el clima de Tampico"),
    )),
    ("Plantas, palmas y árboles", (
        ("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico", "categorías del vivero"),
        ("Catálogo", "/catalogo", f"{datos.VARIEDADES} variedades con cotizador"),
        ("Palmas tropicales", "/palmas-tropicales-tampico", "especies y precios «desde»"),
        ("Palmas al mayoreo para proyectos", "/palmas-mayoreo-proyectos", "especies con nombre científico"),
        ("Árboles ornamentales", "/arboles-ornamentales-tampico", "especies para jardín"),
        ("Árboles para banqueta", "/arboles-para-banqueta-tampico", "especies para la banqueta"),
        ("Plantas para jardín", "/plantas-para-jardin-tampico", "sol, sombra y cubresuelos"),
        ("Plantas de interior", "/plantas-de-interior-tampico", "especies para casa y oficina"),
        (f"Nochebuenas {NB['temporada']}", NB["ruta"], "precios por tamaño y por volumen, menudeo y mayoreo"),
    )),
    ("Materiales", (
        ("Tierra negra vegetal", "/tierra-negra-vegetal-tampico", "costal, m³ y camión"),
        ("Tezontle rojo", "/tezontle-rojo-tampico", "usos y presentaciones"),
        ("Mármol blanco", "/marmol-blanco-tampico", "saco y usos"),
        ("Piedra bola de río", "/piedra-bola-rio-tampico", f"venta {datos.PIEDRA_BOLA_VENTA}"),
    )),
    ("Zonas", (("Zonas de servicio", "/zonas", "índice de cobertura en Tampico, Ciudad Madero y Altamira"),
               *((nombre, ruta, "jardinería en la zona") for nombre, ruta in datos.ZONAS))),
    # Lo que conviene que un asistente no prometa en nombre del negocio; cada punto enlaza la página que lo explica.
    ("Lo que no hacemos", (
        ("Pasto sintético sin muestras físicas", "/pasto-sintetico",
         "no ofrecemos muestras físicas; el modelo se elige con las fichas técnicas y las fotos"),
        ("Envío de pasto natural fuera de la región", "/pasto-en-rollo-tampico",
         "el pasto natural solo se entrega en Tampico, Madero, Altamira y, por proyecto, la zona cercana"),
        ("Fechas de corte o disponibilidad semanal", "/pasto-en-rollo-tampico",
         f"no se publican; el pasto llega del campo {datos.LLEGADA_PASTO}"),
        ("Garantía en Nochebuenas", NB["ruta"], "las Nochebuenas se venden sin garantía ni reposición"),
    )),
    ("Optional", (
        ("Blog", "/blog", "guías de jardinería para el clima de Tampico"),
        ("Plantas resistentes a la sal del Golfo", "/blog/plantas-resistentes-sal-golfo-tampico",
         "especies para la costa"),
        ("Cómo proteger el jardín de los nortes", "/blog/nortes-tampico-proteger-plantas-jardin", "frentes fríos"),
        ("Jardín y temporada de huracanes", "/blog/temporada-huracanes-proteger-jardin-tampico",
         "preparación y recuperación"),
        ("Cuándo regar el pasto San Agustín", "/blog/cuando-regar-pasto-san-agustin-tampico", "frecuencia por temporada"),
    )),
)
# Páginas de llms-full.txt, en orden: las que venden y las de condiciones.
PAGINAS_FULL = ("/", "/precios", "/pasto-en-rollo-tampico", "/mayoreo-pasto-tampico", "/pasto-sintetico-tampico",
                "/pasto-sintetico", "/diseno-jardines-tampico", "/sistema-riego-tampico",
                "/mantenimiento-jardines-tampico", "/poda-arboles-tampico", "/empresas", "/vivero-tampico",
                "/nosotros", "/zonas", "/palmas-tropicales-tampico",
                "/palmas-mayoreo-proyectos", "/tierra-negra-vegetal-tampico", "/tezontle-rojo-tampico",
                "/marmol-blanco-tampico", "/piedra-bola-rio-tampico", NB["ruta"])


def url(ruta):
    return f"{SITIO}{ruta}"


def _dinero(n):
    return c.dinero(n) if float(n).is_integer() else c.dinero_exacto(n)


def horario():
    """ "lunes a viernes de 9:00 a 18:00; sábado de 9:00 a 14:00; domingo cerrado", de datos.HORARIO_LD."""
    tramos = []
    for dias, abre, cierra in datos.HORARIO_LD:
        nombre = DIAS[dias[0]] if len(dias) == 1 else f"{DIAS[dias[0]]} a {DIAS[dias[-1]]}"
        tramos.append(f"{nombre} de {abre.lstrip('0')} a {cierra}")
    return "; ".join(tramos) + "; domingo cerrado"


def negocio():
    """Datos del negocio, uno por renglón."""
    clientes = f"{', '.join(datos.CLIENTES_B2B[:-1])} y {datos.CLIENTES_B2B[-1]}"
    referencia = f"{datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}"
    promesa = datos.PROMESA.removeprefix("Respondemos ")
    return (
        f"Nombre: {datos.NOMBRE} (también aparece como «{datos.NOMBRE_ALTERNO}»)",
        (f"Dirección única: {datos.CALLE}, {datos.COLONIA}, {datos.CP} {datos.CIUDAD}, {entidad.ESTADO}, México "
         f"({referencia}). Cualquier otra dirección publicada en directorios está desactualizada"),
        f"Coordenadas: {datos.GEO[0]}, {datos.GEO[1]}",
        f"Google Maps: {datos.MAPS_URL}",
        f"Teléfono y WhatsApp: +52 {datos.TELEFONO_VISIBLE}",
        f"Correo: {datos.CORREO_FORMULARIOS}",
        f"Horario: {horario()}",
        f"Respuesta por WhatsApp: {promesa}",
        f"Registro REPSE (STPS): {datos.REPSE}, consultable en {datos.REPSE_PADRON}",
        f"Facturación: {datos.FACTURA}",
        f"Calificación: {datos.GOOGLE}",
        (f"Trayectoria: {datos.INSTALACIONES} instalaciones de pasto, {datos.CLIENTES} clientes, {datos.M2_INSTALADOS} "
         f"instalados, {datos.SISTEMAS_RIEGO} sistemas de riego y {datos.VARIEDADES} variedades de plantas"),
        f"Clientes empresariales: {clientes}",
        "Perfiles oficiales: " + " · ".join(u for _n, u in datos.REDES),
    )


def _mensualidades():
    """Plazos, montos mínimos y sobreprecio de tools/pasto/mensualidades.py (los mismos de vt-mensualidades.js)."""
    sobre = sorted(((mensualidades.TASA_BASE + tasa) * (1 + mensualidades.IVA) / (1 - (mensualidades.TASA_BASE + tasa)
                    * (1 + mensualidades.IVA))) * 100 for tasa in mensualidades.TASAS.values())
    minimos = {}
    for minimo, plazos in mensualidades.UMBRALES:
        for plazo in plazos:
            minimos[plazo] = min(minimo, minimos.get(plazo, minimo))
    desde = "; ".join(f"{plazo} mensualidades desde {_dinero(minimos[plazo])}" for plazo in mensualidades.PLAZOS)
    return (f"Pago en mensualidades con tarjeta de crédito: {', '.join(str(p) for p in mensualidades.PLAZOS[:-1])} o "
            f"{mensualidades.PLAZOS[-1]} mensualidades. El precio en mensualidades es mayor que el de contado "
            f"(+{sobre[0]:.1f}% a +{sobre[-1]:.1f}% según el plazo) y el total se muestra antes de pagar. Montos mínimos de "
            f"contado: {desde}")


def precios():
    """Precios de referencia, uno por renglón, con su regla de IVA."""
    riego, sintetico = P["riego_m2"], P["sintetico_instalado_m2"]
    barato = min(m["rollo"] for m in data.MODELOS)
    camiones = ", ".join(f"camión de {m3} m³ {_dinero(precio)}" for m3, precio in datos.TIERRA_CAMIONES)
    menudeo, volumen = NB["productos"][0]["precios"][0], NB["productos"][0]["precios"][-1]
    preventa = NB["preventa"]
    limite = f"{int(preventa['hasta'][8:])} de {entidad.mes_largo(preventa['hasta'])}"
    return (
        f"Pasto San Agustín en rollo, solo el pasto: {_dinero(P['pasto_solo_m2'])} por m² (no lleva IVA)",
        # Decisión del dueño (2026-11-10): el instalado considera el terreno listo; lo que falte se cotiza aparte.
        (f"Pasto San Agustín instalado: desde {_dinero(P['pasto_instalado_m2'])} por m², con IVA incluido, con "
         f"colocación y garantía de arraigo con condiciones. {datos.TERRENO_LISTO}"),
        (f"Pasto San Agustín al mayoreo: desde {_dinero(P['pasto_mayoreo_m2'])} por m², solo el pasto, en pedidos de "
         f"{P['pasto_mayoreo_minimo_m2']} m² o más (no lleva IVA)"),
        (f"Mantenimiento de jardines: desde {_dinero(P['mantenimiento_mes'])} al mes en el plan residencial; los planes "
         f"premium y para empresas, {datos.SEGUN_COTIZACION.lower()}"),
        (f"Diseño de jardines (Plan Terra): Esencial {_dinero(P['diseno'])}, Completo {_dinero(P['diseno_completo'])} y "
         f"Premium desde {_dinero(P['diseno_premium'])}. En Esencial y Completo el diseño se descuenta al contratar la "
         f"obra; en Premium, en proyectos de más de {_dinero(P['diseno_premium_descuento_desde'])}"),
        (f"Sistema de riego automático instalado: de {_dinero(riego[0])} a {_dinero(riego[1])} por m²; ahorra "
         f"{datos.RIEGO_AHORRO} de agua"),
        (f"Pasto sintético instalado en Tampico, Madero y Altamira: de {_dinero(sintetico[0])} a {_dinero(sintetico[1])} "
         "por m², con IVA, material y colocación; la preparación del terreno se cotiza aparte"),
        (f"Pasto sintético con envío a todo México: desde {_dinero(barato)} por m² en rollo de {data.ROLLO_M2} m², con "
         f"IVA; envío por rollo de {_dinero(data.ZONAS['A'])} (zona A), {_dinero(data.ZONAS['B'])} (zona B) o "
         f"{_dinero(data.ZONAS['C'])} (zona C); pedido mínimo de {data.MIN_NACIONAL_M2} m²"),
        (f"Poda de árboles y palmas: desde {_dinero(P['poda'])}, según cotización y el tamaño; el derribo de árboles "
         f"completos, {datos.SEGUN_COTIZACION.lower()}. {datos.PODA_RESIDUOS} El permiso municipal, si se necesita, lo "
         "tramita el dueño del predio con su ayuntamiento"),
        (f"Palmas: areca y coco plumoso desde {_dinero(P['palma_desde'])} y palma real desde {_dinero(P['palma_real'])}, "
         "en tamaño chico; el precio sube con la altura (no llevan IVA)"),
        (f"Flamboyán: desde {_dinero(P['flamboyan'])} (no lleva IVA). Las demás especies, "
         f"{datos.SEGUN_COTIZACION.lower()}"),
        (f"Tierra negra vegetal: costal {_dinero(P['tierra_negra_costal'])}; tierra preparada, costal "
         f"{_dinero(P['tierra_preparada_costal'])}; a granel {_dinero(P['tierra_negra_m3'])} por m³; {camiones}"),
        (f"Tezontle rojo: costal desde {_dinero(P['tezontle_costal'])}; m³ y camión, "
         f"{datos.SEGUN_COTIZACION.lower()}"),
        f"Mármol blanco: {_dinero(P['marmol_saco'])} el saco, {datos.MARMOL_CONDICION}",
        f"Piedra bola de río: {datos.PIEDRA_BOLA_VENTA}, {datos.SEGUN_COTIZACION.lower()}",
        f"Materiales: {datos.CONDICIONES_MATERIALES}".rstrip("."),
        (f"Nochebuenas {NB['temporada']}: maceta de 5\" a {_dinero(menudeo)} por pieza al menudeo y desde "
         f"{_dinero(volumen)} en pedidos de {NB['cortes'][-1]} piezas o más. Precio de preventa: "
         f"{round(preventa['descuento'] * 100)}% menos en pedidos de menos de {NB['cortes'][-1]} piezas confirmados a "
         f"más tardar el {limite}. Sin garantía ni reposición"),
    )


def condiciones():
    garantia_pasto = datos.GARANTIA_PASTO.replace("la reponemos", "se repone").replace(" (ver condiciones).", "")
    garantia_plantas = datos.GARANTIA_PLANTAS.replace("sembramos nosotros", f"siembra el equipo de {datos.NOMBRE}")
    return (
        f"Garantía del pasto instalado: {garantia_pasto[0].lower()}{garantia_pasto[1:]}. Condiciones: "
        f"{url(c.CONDICIONES_PASTO)}",
        f"Garantía de plantas: {garantia_plantas.replace(' (ver condiciones).', '')}. Condiciones: "
        f"{url('/politicas#garantia-plantas')}",
        datos.PRIMER_RIEGO.replace("lo haces tú: te enseñamos cómo y te dejamos",
                                   f"lo hace el cliente: {datos.NOMBRE} explica cómo y entrega").rstrip("."),
        f"El pasto llega del campo {datos.LLEGADA_PASTO}",
        datos.VISITA_COSTO.replace("te lo confirmamos", "se confirma").rstrip("."),
        datos.ANTICIPO.replace("No pedimos", "No se pide").replace("tu pedido", "un pedido")
        .replace("solicitamos", "se solicita").rstrip("."),
        f"{_mensualidades()}. Condiciones: {url('/politicas#mensualidades')}",
    )


def cobertura():
    return (
        "Zona de servicio: Tampico, Ciudad Madero y Altamira, Tamaulipas",
        f"Por proyecto: {datos.ZONAS_POR_PROYECTO}",
        "Pasto sintético: envío a todo México",
        "Pasto natural: no se envía fuera de la región",
    )


def _lista(renglones):
    return [f"- {r}" for r in renglones]


def _cabeza():
    return [f"# {datos.NOMBRE}", "", f"> {RESUMEN}", "",
            f"Precios en pesos mexicanos (MXN), vigentes en {datos.ANIO}. Actualizado: {datos.PRECIOS_ACTUALIZADOS}.", "",
            REGLA_IVA, ""]


def rutas_enlazadas():
    return [ruta for _titulo, enlaces in SECCIONES for _n, ruta, _d in enlaces]


def _validar_rutas(rutas):
    conocidas = {ruta for ruta, _a, _p, _c in generar.PAGINAS}
    faltan = sorted(set(rutas) - conocidas)
    if faltan:
        raise ValueError(f"llms: enlaces a páginas que el build no genera: {faltan}")


def llms():
    """Texto de public/llms.txt."""
    _validar_rutas(rutas_enlazadas())
    lineas = _cabeza()
    for titulo, renglones in (("Datos del negocio:", negocio()), ("Precios de referencia:", precios()),
                              ("Condiciones:", condiciones()), ("Cobertura:", cobertura())):
        lineas += [titulo, "", *_lista(renglones), ""]
    lineas += [f"Texto completo de las páginas principales: {url('/llms-full.txt')}", ""]
    for titulo, enlaces in SECCIONES:
        lineas += [f"## {titulo}", "", *[f"- [{n}]({url(ruta)}): {d}" for n, ruta, d in enlaces], ""]
    return "\n".join(lineas)


def _respuesta_de(k):
    """La respuesta directa de la página (data-vt-respuesta): la propia o, si la portada ya responde, su entrada."""
    if (k.get("respuesta") or {}).get("texto"):
        return c.texto_plano(k["respuesta"]["texto"])
    portada = k.get("portada", {})
    return c.texto_plano(portada["lede"]) if portada.get("respuesta") else ""


def _preguntas_de(k):
    faq = k.get("faq") or {}
    return faq.get("preguntas", ()) if isinstance(faq, dict) else faq


def _pagina(ruta):
    k = generar.cargar(generar.contenido_de(ruta)).CONTENIDO
    meta = k["meta"]
    lineas = [f"## {meta['title']}", "", f"URL: {meta['canonical']}", "", meta["description"], ""]
    respuesta = _respuesta_de(k)
    if respuesta:
        lineas += [respuesta, ""]
    for pregunta, texto in _preguntas_de(k):
        lineas += [f"### {c.texto_plano(pregunta)}", "", c.texto_plano(texto), ""]
    return lineas


def llms_full():
    """Texto de public/llms-full.txt."""
    _validar_rutas(PAGINAS_FULL)
    lineas = _cabeza()
    lineas += [f"Este archivo reúne el texto esencial de las páginas principales de {SITIO}. Índice con enlaces: "
               f"{url('/llms.txt')}", ""]
    for titulo, renglones in (("Datos del negocio", negocio()), ("Lista de precios", precios()),
                              ("Garantías y condiciones", condiciones()), ("Cobertura", cobertura())):
        lineas += [f"## {titulo}", "", *_lista(renglones), ""]
    lineas += ["## Cómo cotizar", "",
               (f"Por WhatsApp al +52 {datos.TELEFONO_VISIBLE} ({datos.PROMESA[0].lower()}{datos.PROMESA[1:]}; "
                f"{horario()}), con la colonia y los metros aproximados; o con los cotizadores de {url('/')} (pasto por "
                f"m²), {url('/pasto-sintetico')} (pasto sintético con envío) y {url('/catalogo')} (plantas). "
                f"{datos.VISITA_COSTO}"), ""]
    for ruta in PAGINAS_FULL:
        lineas += _pagina(ruta)
    return "\n".join(lineas)


def escribir(public=paginas.PUBLIC):
    """Escribe los dos archivos solo si cambian; devuelve cuántos escribió."""
    escritos = 0
    for nombre, texto in (("llms.txt", llms()), ("llms-full.txt", llms_full())):
        path = Path(public) / nombre
        if path.is_file() and path.read_text(encoding="utf-8") == texto:
            continue
        path.write_text(texto, encoding="utf-8")
        escritos += 1
    return escritos
