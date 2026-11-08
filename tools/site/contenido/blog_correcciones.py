"""Correcciones de contenido de los artículos del blog (Etapa 2h): lo único que cambia el texto publicado.

La migración conserva cada palabra; aquí está, por artículo, cada dato que contradice las fuentes oficiales o las reglas
del dueño, con el texto exacto de antes, el de después y el motivo. tools/site/extraer_blog.py las aplica y se detiene si una
no encuentra su texto; tests/test_blog_paridad.py exige que la diferencia entre lo publicado y lo nuevo sea exactamente esta
lista. Los precios de "nuevo" salen de datos.PRECIOS. TODOS se aplica a todos los artículos (los títulos de otros artículos se
repiten en enlaces y relacionados) y no exige coincidencia.

Cada fila es (clave, antes, después, motivo). La clave ("C042", o "T03" en TODOS) es literal y no se renumera: es el nombre con
el que el dueño revisa la fila. Cuando conteste, su respuesta es una línea en DECISIONES y una nueva extracción
(`python3 tools/site/extraer_blog.py escribir`, luego el build). Si la respuesta restituye un precio, va también en datos.PRECIOS
y la especie sale de ESPECIE_SIN_PRECIO_RE: test_blog_reglas lo exige.
"""
import datos
from componentes import dinero

P = datos.PRECIOS
SEGUN = datos.SEGUN_COTIZACION.lower()
CAMION_8 = dinero(P["tierra_negra_camion_8m3"])
R0, R1 = P["riego_m2"]


def riego(m2_a, m2_b=None):
    """Rango instalado de riego para un área, con el precio oficial por m²."""
    return f"{dinero(R0 * m2_a)}–{dinero(R1 * (m2_b or m2_a))}"


M_PLANTA = "Precio sin confirmar por el dueño: solo areca, coco plumoso, palma real y flamboyán tienen precio; lo demás es según cotización."
M_VENDIDA = "\"Más vendida\" es un superlativo sin dato que lo respalde (regla del dueño); la URL no cambia."
M_ESTAD = "Porcentaje sin fuente (no se publican estadísticas inventadas)."
M_GRATIS = "Regla del dueño: sin \"gratis\" ni \"sin costo\", salvo la garantía de pasto aprobada."
M_RIEGO = "Riego instalado: el único precio oficial es $180–$320/m² (datos.py); los rangos se recalculan con él."
M_CASO = "Caso con cliente, cifra e inversión sin verificar: no se publica como real."
M_AHORRO = "El ahorro oficial de agua es \"hasta 40%\" (datos.RIEGO_AHORRO)."
M_PAGO = "Pago: anticipo y avances (datos.ANTICIPO_PROYECTOS), sin crédito propio; mensualidades solo con tarjeta de crédito."
M_TIERRA = "Camión de tierra de 8 m³: $5,200 (datos.py), no $12,000."
M_DISENO = "Diseño: Esencial $3,000, Completo $6,500 y Premium desde $18,000 (datos.py); no son rangos."
M_GARANTIA = "Garantía del sintético: 3 a 8 años según modelo (tools/pasto/data.py: Aruba 10 de 3 a 5, Toscana 5, los demás 8)."
M_DEK = "La entrada era la del artículo de árboles de banqueta (copiada por error)."
M_ENTREGA = "La entrega se cobra por viaje, según la colonia (datos.ENTREGA_COBRO)."
M_VISITA = "Toda mención de la visita lleva su costo (datos.VISITA_COSTO)."

GARANTIA_SINTETICO = "de 3 a 8 años según modelo"
PAGO_RESPUESTA = (f"Viveros Terra no ofrece crédito propio. {datos.ANTICIPO_PROYECTOS} También puedes pagar a mensualidades con "
                  "tarjeta de crédito: <a href=\"/politicas#mensualidades\">ver condiciones</a>.")

REVERTIR = object()  # la fila deja de aplicarse: se queda el texto publicado

# Respuestas del dueño, una línea por fila: clave -> REVERTIR o el texto que sustituye al "después".
DECISIONES = {
    # "C119": REVERTIR,
    # "C120": "<td>Palma del Viajero</td><td>$500</td>",
}

FILAS_TODOS = (
    ("T01", "Las 8 Palmas Más Vendidas en Tampico (con Precios)", "8 Palmas para Jardines en Tampico (con Precios)", M_VENDIDA),
    ("T02", "las 8 palmas más vendidas en Tampico con precios actualizados", "8 palmas para jardines en Tampico con precios actualizados", M_VENDIDA),
    ("T03", "lista de las 8 palmas más vendidas en Tampico", "lista de 8 palmas para jardines en Tampico", M_VENDIDA),
    ("T04", "las palmas más vendidas en Tampico con precios", "las 8 palmas para jardines en Tampico con precios", M_VENDIDA),
    ("T05", "palmas más vendidas en Tampico con precios</a>", "palmas para jardines en Tampico con precios</a>", M_VENDIDA),
    ("T06", "palmas más vendidas en Tampico</a>", "palmas para jardines en Tampico</a>", M_VENDIDA),
    ("T07", "La palma más vendida de la región: crecimiento rápido y precio desde $500.", "Crecimiento rápido y tolerancia al calor y la sequía.", M_VENDIDA),
    ("T08", "La palma más vendida de la región, con su característica faldilla de hojas secas.", "Crecimiento rápido, con su característica faldilla de hojas secas.", M_VENDIDA),
)

_DEK_BANQUETA = "¿Cansado de banquetas destruidas por raíces? Guía de los 7 mejores árboles para banqueta en Tampico: dan sombra real sin dañar el pavimento ni las tuberías. Con tabla comparativa."

FILAS = {
    "/blog": (
        ("C001", "Las 8 palmas más vendidas en Tampico (con precios)", "8 palmas para jardines en Tampico (con precios)", M_VENDIDA),
        ("C002", "Palmas más vendidas Tampico precios", "Palmas para jardines en Tampico", M_VENDIDA),
        ("C003", "La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y precio desde $500.", "Crecimiento rápido y tolerancia total al calor.", M_VENDIDA),
        ("C004", "tolera luz baja, crece lento y tiene precio desde $500.", "tolera luz baja y crece lento.", M_PLANTA),
        ("C005", "tolera sol pleno, sequía y lluvia intensa. Precio desde $500.", f"tolera sol pleno, sequía y lluvia intensa. Precio desde {dinero(P['palma_desde'])}.", "Coco plumoso: desde $250 (datos.py)."),
        ("C006", "de privacidad, con precio desde $300.", f"de privacidad, con precio desde {dinero(P['palma_desde'])}.", "Areca: desde $250 (datos.py)."),
        ("C007", "Cómo Ahorrar Hasta 50% de Agua", "Cómo Ahorrar Hasta 40% de Agua", M_AHORRO),
    ),
    "hongos-plantas-exceso-humedad-tampico": (
        ("C008", "Las tres medidas más efectivas y gratuitas son:", "Las tres medidas más efectivas son:", M_GRATIS),
    ),
    "acolchado-mulch-jardin-tampico": (
        ("C009", "Casi gratis: aprovechas", "Casi sin gasto: aprovechas", M_GRATIS),
    ),
    "arboles-para-sembrar-en-banqueta": (
        ("C010", "Si las aplicas, evitas el 90% de los problemas:", "Si las aplicas, evitas la mayoría de los problemas:", M_ESTAD),
        ("C011", "En Viveros Terra hemos instalado más de 200 árboles de banqueta en Tampico, Madero y Altamira. El 95% de los problemas que vemos", "En las banquetas de Tampico, Madero y Altamira, la mayoría de los problemas que vemos", "Cifra de árboles y porcentaje sin verificar."),
        ("C012", " Tip de experto:", " Tip:", "Sin \"expertos\" (regla de voz)."),
    ),
    "cesped-amarillo-tampico-causas-soluciones": (
        ("C013", "otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo.",
         f"otras veces requiere visita técnica, pero siempre con presupuesto claro antes de cualquier trabajo. {datos.VISITA_COSTO}", M_VISITA),
    ),
    "como-ahorrar-agua-jardin-tampico": (
        ("C014", "reduciendo hasta un 50% el consumo hídrico", f"reduciendo {datos.RIEGO_AHORRO} el consumo hídrico", M_AHORRO),
        ("C015", "para reducir hasta 50% el consumo", f"para reducir {datos.RIEGO_AHORRO} el consumo", M_AHORRO),
        ("C016", "Aprende a reducir hasta 50% el consumo", f"Aprende a reducir {datos.RIEGO_AHORRO} el consumo", M_AHORRO),
        ("C017", "entre 30% y 50% respecto al riego manual", f"{datos.RIEGO_AHORRO} respecto al riego manual", M_AHORRO),
        ("C018", "Clientes de Viveros Terra en Tampico reportan ahorros de entre $150 y $600 pesos mensuales en el recibo de agua después de instalar un sistema automático, dependiendo del tamaño del jardín y la frecuencia de riego anterior.",
         f"Un sistema automático bien programado ahorra {datos.RIEGO_AHORRO} de agua frente a la manguera; lo que baja tu recibo depende del tamaño del jardín y de cuánto riegas hoy.", "Testimonio y cifra sin verificar."),
    ),
    "como-medir-plantas-altura-cepellon": (
        ("C019", "puede orientarte sin costo antes de cotizar", "puede orientarte antes de cotizar", M_GRATIS),
    ),
    "cuando-plantar-pasto-tampico-calendario": (
        ("C020", _DEK_BANQUETA, "Calendario completo para sembrar pasto en Tampico mes a mes: cuál es el mejor mes, qué evitar y por qué septiembre es el mes ideal en clima tropical.", M_DEK),
        ("C021", "<strong>septiembre arraiga el 95% del pasto; julio puede arraigar solo el 60%</strong> por el calor extremo", "<strong>en septiembre el pasto arraiga mucho mejor que en julio</strong>, por el calor extremo", M_ESTAD),
        ("C022", "aporta humedad gratis al suelo", "aporta humedad natural al suelo", M_GRATIS),
        ("C023", "la tasa de mortandad sube al 30–40%", "la mortandad sube mucho", M_ESTAD),
        ("C024", "la tasa de éxito baja al 60% sin riego intensivo", "la tasa de éxito baja sin riego intensivo", M_ESTAD),
        ("C025", "reduce 70% el riego manual", "reduce mucho el riego manual", M_ESTAD),
        ("C026", "puede duplicar la tasa de arraigo del pasto", "mejora el arraigo del pasto", M_ESTAD),
    ),
    "cuando-regar-pasto-san-agustin-tampico": (
        ("C027", "En Viveros Terra instalamos sistemas desde $8,000 pesos; uno bien programado", f"En Viveros Terra instalamos sistemas de {dinero(R0)} a {dinero(R1)} por m²; uno bien programado", M_RIEGO),
        ("C028", "El problema real en el 70% de los casos es el riego", "El problema real, en la mayoría de los casos, es el riego", M_ESTAD),
    ),
    "cuanto-cuesta-jardin-tampico-precios": (
        ("C029", "pasto $85/m², diseño desde $3K, riego, plantas. Cotiza gratis hoy.", "pasto $85/m², diseño desde $3K, riego, plantas. Cotiza por WhatsApp.", M_GRATIS),
        ("C030", "El costo de hacer un jardín en Tampico va desde $5,000 MXN para uno mini residencial hasta $200,000+ para premium.", "Hacer un jardín en Tampico se cotiza según el proyecto; estas son referencias con los precios oficiales.", "Rango total sin confirmar por el dueño."),
        ("C031", "basados en proyectos ejecutados en Tampico, Madero y Altamira durante 2025 y lo que va de 2026. No son precios promedio nacionales: son datos de nuestra zona.", "con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira. El presupuesto final siempre se cotiza.", "Dato sin verificar por el dueño."),
        ("C032", "<li>Palmas grandes ($1,000–$2,000 c/u), árboles ornamentales", f"<li>Palmas grandes ({SEGUN}), árboles ornamentales", M_PLANTA),
        ("C033", "5 a 10 plantas ornamentales básicas: $200–$500 c/u", f"5 a 10 plantas ornamentales básicas: {SEGUN}", M_PLANTA),
        ("C034", "1–3 palmas medianas ($500–$1,500 c/u)", f"1–3 palmas medianas ({SEGUN})", M_PLANTA),
        ("C035", "Riego automatizado completo con programador digital ($15,000–$60,000 según extensión)", f"Riego automatizado completo con programador digital ({dinero(R0)}–{dinero(R1)}/m²)", M_RIEGO),
        ("C036", "Ejemplo real: jardín de 30 m²", "Ejemplo de presupuesto: jardín de 30 m²", M_CASO),
        ("C037", "<li>6 plantas ornamentales × $300 = $1,800</li>\n<li>Mano de obra preparación + instalación = $2,000</li>\n<li><strong>Total estimado: $7,850 MXN</strong></li>", f"<li>6 plantas ornamentales: {SEGUN}</li>\n<li>Mano de obra de preparación e instalación: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_PLANTA),
        ("C038", "Ejemplo real: jardín de 120 m² con riego básico", "Ejemplo de presupuesto: jardín de 120 m² con riego básico", M_CASO),
        ("C039", "<li>15 plantas + 2 palmas = $7,500</li>", f"<li>15 plantas + 2 palmas: {SEGUN}</li>", M_PLANTA),
        ("C040", "<li>Riego básico por aspersores = $6,000</li>\n<li>Mano de obra total = $4,000</li>\n<li><strong>Total estimado: $36,700 MXN</strong></li>", f"<li>Riego básico por aspersores: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_RIEGO),
        ("C041", "<li>Tierra negra 8 m³ = $12,000</li>\n<li>5 palmas grandes + 20 plantas ornamentales = $18,000</li>", f"<li>Tierra negra, camión de 8 m³ = {CAMION_8}</li>\n<li>5 palmas grandes + 20 plantas ornamentales: {SEGUN}</li>", M_TIERRA),
        ("C042", "<li>Riego automatizado completo 250 m² = $40,000</li>\n<li>Tezontle, bordillos y acabados = $12,000</li>\n<li>Mano de obra total = $10,000</li>\n<li><strong>Total: $119,750 MXN</strong></li>", f"<li>Riego automatizado completo 250 m²: {riego(250)}</li>\n<li>Tezontle, bordillos y acabados: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_RIEGO),
        ("C043", "Ejemplo: jardín premium 250 m² → $120,000 MXN", "Ejemplo: jardín premium de 250 m²", M_CASO),
        ("C044", "<td>Pasto San Agustín (instalado)</td><td>$85/m²</td><td>Incluye mano de obra básica</td>", "<td>Pasto San Agustín</td><td>$85/m² solo pasto · desde $120/m² instalado</td><td>El instalado incluye preparación básica y colocación</td>", "Precio oficial: $85 solo pasto y desde $120 instalado."),
        ("C045", "Camión 8 m³ desde $12,000", f"Camión de 8 m³: {CAMION_8}", M_TIERRA),
        ("C046", "<td>Diseño Plan Terra Esencial</td><td>$3,000–$6,000</td>", "<td>Diseño Plan Terra Esencial</td><td>$3,000</td>", M_DISENO),
        ("C047", "<td>Diseño Plan Terra Completo</td><td>$6,500–$18,000</td>", "<td>Diseño Plan Terra Completo</td><td>$6,500</td>", M_DISENO),
        ("C048", "<td>Riego automatizado</td><td>$15,000–$60,000</td><td>Según m² y número de zonas</td>", f"<td>Riego automatizado</td><td>{dinero(R0)}–{dinero(R1)}/m²</td><td>Según m² y número de zonas</td>", M_RIEGO),
        ("C049", "<td>Palmas pequeñas (hasta 1.5 m)</td><td>$250–$600 c/u</td><td>Areca, Kerpis, Cycas pequeñas</td>", "<td>Palmas pequeñas (hasta 1.5 m)</td><td>Desde $250 c/u</td><td>Areca y coco plumoso; palma real desde $500; las demás, según cotización</td>", M_PLANTA),
        ("C050", "<td>Palmas medianas (1.5–3 m)</td><td>$600–$1,200 c/u</td>", f"<td>Palmas medianas (1.5–3 m)</td><td>{SEGUN}</td>", M_PLANTA),
        ("C051", "<td>Palmas grandes (3 m+)</td><td>$1,200–$2,500 c/u</td>", f"<td>Palmas grandes (3 m+)</td><td>{SEGUN}</td>", M_PLANTA),
        ("C052", "<td>Mano de obra general</td><td>~$200/m²</td>", f"<td>Mano de obra general</td><td>{SEGUN}</td>", "Precio sin confirmar."),
        ("C053", "<td>Tezontle decorativo</td><td>$35/kg o $280/costal</td>", f"<td>Tezontle decorativo</td><td>Costal desde {dinero(P['tezontle_costal'])}</td>", "Tezontle: costal desde $200 (datos.py)."),
        ("C054", "3 ejemplos reales de presupuestos", "3 ejemplos de presupuesto", M_CASO),
        ("C055", "Caso A: Jardín residencial de 50 m² → ~$13,500 MXN", "Ejemplo A: jardín residencial de 50 m²", M_CASO),
        ("C056", "Cliente en Ciudad Madero con casa dúplex. Jardín frontal", "Jardín frontal", M_CASO),
        ("C057", "<li>8 plantas × $350 = $2,800</li>\n<li>Mano de obra = $3,000</li>\n<li><strong>Total: $13,050 MXN</strong></li>", f"<li>8 plantas: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong></li>", M_PLANTA),
        ("C058", "Caso B: Jardín de 120 m² con riego básico → ~$35,000 MXN", "Ejemplo B: jardín de 120 m² con riego básico", M_CASO),
        ("C059", "Residencia en fraccionamiento de Tampico. Jardín trasero", "Jardín trasero", M_CASO),
        ("C060", "<li>Diseño + instalación completa = $35,000 MXN aprox.</li>", f"<li>Diseño + instalación completa: {SEGUN}</li>", M_CASO),
        ("C061", "Caso C: Jardín premium 250 m² con diseño Plan Terra Completo → ~$120,000 MXN", "Ejemplo C: jardín premium de 250 m² con diseño Plan Terra Completo", M_CASO),
        ("C062", "Casa en fraccionamiento privado de Altamira. Jardín integral", "Jardín integral", M_CASO),
        ("C063", "<li>Diseño + instalación integral = $120,000 MXN aprox.</li>", f"<li>Diseño + instalación integral: {SEGUN}</li>", M_CASO),
        ("C064", "va desde $750/mes para jardines pequeños hasta $3,500/mes para proyectos grandes.", "va desde $750/mes, según el tamaño del jardín.", "Mantenimiento: solo \"desde $750/mes\" es oficial."),
        ("C065", "Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN previo acuerdo. Muchos clientes financian su jardín a través de créditos personales o de nómina. Para proyectos pequeños de $5,000–$15,000, el pago de contado es habitual.", PAGO_RESPUESTA, M_PAGO),
        ("C066", " y entrega una propuesta en menos de 48 horas.", " y te entrega su propuesta.", "Plazo sin confirmar por el dueño."),
    ),
    "cuanto-cuesta-pasto-sintetico-mexico": (
        ("C067", "es el más vendido: el mejor equilibrio entre precio y realismo", "es un buen equilibrio entre precio y realismo", M_VENDIDA),
        ("C068", "<strong>Garantía (5 a 8 años):</strong>", "<strong>Garantía (3 a 8 años):</strong>", M_GARANTIA),
        ("C069", "Estos son tres ejemplos reales con envío", "Estos son tres ejemplos con envío", M_CASO),
    ),
    "errores-pasto-san-agustin-tampico": (
        ("C070", "Viveros Terra ofrece asesoría técnica gratuita sobre el protocolo correcto al momento de la compra o instalación. Para proyectos con contrato, se incluye una visita de seguimiento a los 30 días. El arraigo exitoso",
         f"{datos.GARANTIA_PASTO} {datos.PRIMER_RIEGO} El arraigo exitoso", "Garantía oficial de arraigo; sin \"gratuita\" ni visita de seguimiento sin confirmar."),
    ),
    "framboyan-delonix-regia-tampico": (
        ("C071", "<td>Ficus benjamina</td><td>$200</td>", f"<td>Ficus benjamina</td><td>{SEGUN}</td>", M_PLANTA),
        ("C072", "<td>Trueno</td><td>$300</td>", f"<td>Trueno</td><td>{SEGUN}</td>", M_PLANTA),
        ("C073", "<td>Neem</td><td>$300</td>", f"<td>Neem</td><td>{SEGUN}</td>", M_PLANTA),
        ("C074", "<td>Tabachín</td><td>$350</td>", f"<td>Tabachín</td><td>{SEGUN}</td>", M_PLANTA),
        ("C075", "<td>Laurel de la India</td><td>$500</td>", f"<td>Laurel de la India</td><td>{SEGUN}</td>", M_PLANTA),
        ("C076", "<td>Tulipán Africano</td><td>$600</td>", f"<td>Tulipán Africano</td><td>{SEGUN}</td>", M_PLANTA),
        ("C077", '<th scope="col">Precio desde</th>', '<th scope="col">Precio</th>', M_PLANTA),
    ),
    "jardin-bajo-presupuesto-tampico": (
        ("C078", "3 paquetes reales con detalle", "3 paquetes de ejemplo con detalle", M_CASO),
        ("C079", "basados en proyectos que ejecutamos regularmente en Tampico, Madero y Altamira, ", "con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira, ", "Dato sin verificar por el dueño."),
        ("C080", "<li>6 plantas × $250 = $1,500</li>\n<li>Mano de obra = $1,800</li>\n<li><em>Total: aprox. $8,525 (ajustable según selección de plantas y área exacta)</em></li>", f"<li>6 plantas: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(ajustable según selección de plantas y área exacta)</em></li>", M_PLANTA),
        ("C081", "<li>12 plantas × $300 + 2 palmas × $600 = $4,800</li>", f"<li>12 plantas + 2 palmas: {SEGUN}</li>", M_PLANTA),
        ("C082", "<li>Riego básico aspersores = $4,500</li>\n<li>Mano de obra general = $3,000</li>\n<li><em>Total: $27,450 (ajustable reduciendo área o número de plantas)</em></li>", f"<li>Riego básico por aspersores: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(ajustable reduciendo área o número de plantas)</em></li>", M_RIEGO),
        ("C083", "3 palmas medianas ($800–$1,500 c/u)", f"3 palmas medianas ({SEGUN})", M_PLANTA),
        ("C084", "<li>Tierra negra 7 m³ = $10,500</li>\n<li>25 plantas + 3 palmas medianas = $13,500</li>", f"<li>Tierra negra 7 m³ = $10,500</li>\n<li>25 plantas + 3 palmas medianas: {SEGUN}</li>", M_PLANTA),
        ("C085", "<li>Riego automatizado = $18,000</li>\n<li>Árbol ornamental + acabados = $5,000</li>\n<li>Mano de obra total = $8,000</li>\n<li><em>Total: $75,100 (el presupuesto de $50K es el punto de entrada, el rango completo va hasta $120K+)</em></li>", f"<li>Riego automatizado: {SEGUN}</li>\n<li>Árbol ornamental + acabados: {SEGUN}</li>\n<li>Mano de obra: {SEGUN}</li>\n<li><strong>Total: {SEGUN}</strong> <em>(el presupuesto de $50K es el punto de entrada)</em></li>", M_RIEGO),
        ("C086", "Según estudios de valuación inmobiliaria aplicados al mercado mexicano, un jardín profesional y en buen estado puede añadir entre el 5% y el 15% al valor de venta o renta de una propiedad residencial.", "Un jardín profesional y en buen estado ayuda a vender o rentar una propiedad residencial.", M_ESTAD),
        ("C087", " Un jardín de $50,000 bien ejecutado en una casa de $1,500,000 puede representar una plusvalía de $75,000 a $225,000, con un ROI que va del 50% al 350% de la inversión original.", "", M_ESTAD),
        ("C088", "Viveros Terra no ofrece financiamiento directo, pero acepta pago en parcialidades para proyectos mayores a $30,000 MXN previo acuerdo. Para confirmar solicitamos un anticipo y el resto se acuerda en la cotización. Muchos clientes financian su jardín a través de créditos personales o de nómina.", PAGO_RESPUESTA, M_PAGO),
    ),
    "jardin-vertical-tampico-guia": (
        ("C089", "Un jardín vertical pequeño puede armarse desde <strong>$1,500 MXN</strong>.", "Su costo depende del tamaño, la estructura y las plantas: se cotiza.", "Precio sin confirmar."),
        ("C090", "puede armarse desde <strong>$1,500 a $3,000 MXN</strong>.", "se cotiza según lo que elijas.", "Precio sin confirmar."),
        ("C091", "puede armarse desde $1,500 a $3,000 MXN.", "se cotiza según lo que elijas.", "Precio sin confirmar."),
    ),
    "palma-areca-tampico": (
        ("C092", "en mata pequeña, y desde $800 MXN en matas grandes y densas.", f"en mata pequeña; las matas grandes y densas, {SEGUN}.", M_PLANTA),
        ("C093", "cuestan desde $800 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("C094", "(desde $800)", f"({SEGUN})", M_PLANTA),
        ("C095", "tienen precio desde <strong>$800 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-coco-plumoso-tampico": (
        ("C096", "para planta pequeña y desde <strong>$1,800 MXN</strong> para ejemplares adultos.", f"para planta pequeña; los ejemplares adultos, <strong>{SEGUN}</strong>.", M_PLANTA),
        ("C097", "cuestan desde $1,800 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("C098", "tienen precio desde <strong>$1,800 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-kerpis-howea-forsteriana-tampico": (
        ("C099", "tamaños y precios desde $500. La palma", "y tamaños. La palma", M_PLANTA),
        ("C100", "tamaños y precios desde $500 para lobbies", "y tamaños para lobbies", M_PLANTA),
        ("C101", "En Viveros Terra el precio va desde <strong>$500 MXN</strong>.", f"En Viveros Terra su precio va <strong>{SEGUN}</strong>.", M_PLANTA),
        ("C102", "esquinas de habitación</td><td>$500 MXN</td>", f"esquinas de habitación</td><td>{SEGUN}</td>", M_PLANTA),
        ("C103", "En Viveros Terra, una Palma Kerpis tiene precio desde $500 MXN. Ejemplares grandes y bien formados, ideales para lobbies o espacios amplios, cuestan desde $1,200 MXN.", f"En Viveros Terra, la Palma Kerpis va {SEGUN}.", M_PLANTA),
        ("C104", "En Viveros Terra el precio de la Palma Kerpis inicia en <strong>$500 MXN</strong>. Ejemplares grandes y bien formados, con varios tallos por maceta y listos para dar presencia inmediata en un lobby u oficina, tienen precio desde <strong>$1,200 MXN</strong>.", f"En Viveros Terra el precio de la Palma Kerpis va <strong>{SEGUN}</strong>, también en ejemplares grandes y bien formados, con varios tallos por maceta.", M_PLANTA),
    ),
    "palma-real-roystonea-regia-tampico": (
        ("C105", "cuestan desde $1,400 MXN.", f"van {SEGUN}.", M_PLANTA),
        ("C106", "tienen precio desde <strong>$1,400 MXN</strong>.", f"van <strong>{SEGUN}</strong>.", M_PLANTA),
    ),
    "palma-washingtona-tampico": (
        ("C107", "y precios desde $500. La palma más vendida de la región.", "y precios. Crecimiento rápido y resistencia al calor.", M_VENDIDA),
        ("C108", "La palma más vendida de la región: crecimiento rápido, tolerancia total al calor y la sequía, y precio desde $500 en Viveros Terra.", "Crecimiento rápido y tolerancia total al calor y la sequía.", M_VENDIDA),
        ("C109", "la Washingtonia robusta es, con diferencia, la palma más vendida en Tampico, Madero y Altamira.", "la Washingtonia robusta es una palma muy común en Tampico, Madero y Altamira.", M_VENDIDA),
        ("C110", "es <strong>la palma más vendida en Tampico</strong>:", "es <strong>una palma muy resistente para Tampico</strong>:", M_VENDIDA),
        ("C111", "En Viveros Terra el precio va desde <strong>$500 MXN</strong> para planta de 0.8–1.2 m.", f"En Viveros Terra su precio va <strong>{SEGUN}</strong>, según la altura.", M_PLANTA),
        ("C112", "En Viveros Terra, una planta de 0.8 a 1.2 m tiene precio desde $500 MXN. Ejemplares de 2 a 3 metros, con tronco ya definido, cuestan desde $1,200 MXN.", f"En Viveros Terra, su precio va {SEGUN}, según la altura.", M_PLANTA),
        ("C113", "En Viveros Terra el precio de la Palma Washingtona inicia en <strong>$500 MXN</strong> para una planta de 0.8 a 1.2 metros. Ejemplares de 2 a 3 metros, con tronco ya definido, tienen precio desde <strong>$1,200 MXN</strong>.", f"En Viveros Terra el precio de la Palma Washingtona va <strong>{SEGUN}</strong>, según la altura.", M_PLANTA),
    ),
    "palmas-mas-vendidas-tampico-precios": (
        ("C114", "Las 8 palmas más vendidas en Tampico con precios 2026: Washingtona desde $500, Viajero $500, Areca $250, Coco, Real, Kerpis y más. Vivero productor.", "8 palmas para jardines en Tampico con precios 2026: Areca y Coco Plumoso desde $250, Real desde $500; las demás, según cotización. Vivero productor.", M_VENDIDA),
        ("C115", "Las 8 palmas más vendidas en Tampico con precios 2026", "8 palmas para jardines en Tampico con precios 2026", M_VENDIDA),
        ("C116", "Las 8 palmas más vendidas en Tampico (con precios actualizados)", "8 palmas para jardines en Tampico (con precios actualizados)", M_VENDIDA),
        ("C117", "Palmas más vendidas Tampico", "8 palmas para Tampico", M_VENDIDA),
        ("C118", "Las 8 palmas más vendidas en Tampico son: Washingtona (desde $500), Palma del Viajero ($500), Areca ($250), Real, Coco Plumoso ($250), Kerpis ($500), Cycas Revoluta ($700), y Bambú ($1,000). Los precios varían según el tamaño.", "Estas 8 palmas funcionan bien en Tampico: Areca y Coco Plumoso desde $250 y Real desde $500 en tamaño chico; Washingtona, Palma del Viajero, Kerpis, Cycas Revoluta y Bambú, según cotización. El precio sube con la altura.", M_PLANTA),
        ("C119", "<td>Washingtona</td><td>$500</td>", f"<td>Washingtona</td><td>{SEGUN}</td>", M_PLANTA),
        ("C120", "<td>Palma del Viajero</td><td>$500</td>", f"<td>Palma del Viajero</td><td>{SEGUN}</td>", M_PLANTA),
        ("C121", "<td>Kerpis (Howea)</td><td>$500</td>", f"<td>Kerpis (Howea)</td><td>{SEGUN}</td>", M_PLANTA),
        ("C122", "<td>Cycas Revoluta</td><td>$700</td>", f"<td>Cycas Revoluta</td><td>{SEGUN}</td>", M_PLANTA),
        ("C123", "<td>Bambú Tarro</td><td>$1,000</td>", f"<td>Bambú Tarro</td><td>{SEGUN}</td>", M_PLANTA),
        ("C124", "<strong>Precio desde:</strong> $500 MXN (planta de 0.8–1.2 m). Ejemplares de 2–3 m desde $1,200.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("C125", "<strong>Precio desde:</strong> $500 MXN (hijuelo pequeño). Plantas de 1.5–2 m desde $1,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("C126", " Matas grandes y densas desde $800.", f" Matas grandes y densas, {SEGUN}.", M_PLANTA),
        ("C127", " Ejemplares de 2 m desde $1,400.", f" Ejemplares de 2 m, {SEGUN}.", M_PLANTA),
        ("C128", " Ejemplares adultos desde $1,800.", f" Ejemplares adultos, {SEGUN}.", M_PLANTA),
        ("C129", "<strong>Precio desde:</strong> $500 MXN. Plantas grandes y bien formadas desde $1,200.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("C130", "<strong>Precio desde:</strong> $700 MXN. Especímenes grandes (múltiples coronas) desde $3,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("C131", "<strong>Precio desde:</strong> $1,000 MXN (mata mediana). Matas grandes y densas desde $2,500.", f"<strong>Precio:</strong> {SEGUN}.", M_PLANTA),
        ("C132", "La Washingtona es con diferencia la palma más vendida en la región.", "La Washingtona es una palma muy común en la región.", M_VENDIDA),
        ("C133", "o contáctanos por WhatsApp para una asesoría sin costo.", "o escríbenos por WhatsApp para asesorarte.", M_GRATIS),
        ("C134", "tienen garantía de arraigo de 30 días: si no prenden y se regaron y cuidaron como indicamos, las reponemos sin costo. No cubre falta de riego, cambio de lugar, daños por mascotas o clima extremo. Si compras la palma y la siembras por tu cuenta, te damos asesoría gratis sobre la plantación.", "tienen garantía de 30 días, con el riego indicado. No cubre falta de riego, cambio de lugar, daños por mascotas o clima extremo. Si compras la palma y la siembras por tu cuenta, te orientamos sobre la plantación.", "Garantía de plantas: 30 días con condiciones (datos.GARANTIA_PLANTAS); \"sin costo\" solo en la de pasto."),
    ),
    "palmas-tropicales-jardin-tampico": (
        ("C135", "Precio aproximado: desde $800 (planta) hasta $4,500 (adulta)", f"Precio: {SEGUN}", M_PLANTA),
        ("C136", "Desde <strong>$800 pesos</strong> para planta pequeña de 40–60 cm, hasta <strong>$4,500+</strong> para ejemplares adultos de 2–3 metros para impacto inmediato.", f"Va <strong>{SEGUN}</strong>, según el tamaño: desde planta pequeña de 40–60 cm hasta ejemplares adultos de 2–3 metros para impacto inmediato.", M_PLANTA),
    ),
    "pasto-sintetico-calor-mexico": (
        ("C137", "(garantías de 5-8 años)", "(garantías de 3 a 8 años según modelo)", M_GARANTIA),
        ("C138", "Por eso podemos dar garantía de 5 a 8 años según modelo.", f"Por eso podemos dar garantía {GARANTIA_SINTETICO}.", M_GARANTIA),
        ("C139", "(por eso ofrecemos garantía de 5 a 8 años según modelo)", f"(por eso ofrecemos garantía {GARANTIA_SINTETICO})", M_GARANTIA),
    ),
    "pasto-sintetico-para-perros": (
        ("C140", "El más vendido para familias: suave", "Para familias: suave", M_VENDIDA),
        ("C141", "(28 mm, el más vendido para familias con mascotas)", "(28 mm, para familias con mascotas)", M_VENDIDA),
        ("C142", "Todos con garantía de 5-8 años y", "Toscana 28, Irlanda 25, Capri 20 y Toscana 18 tienen garantía de 5 a 8 años según modelo y", M_GARANTIA),
        ("C143", "El 90% de los problemas de olor", "La mayoría de los problemas de olor", M_ESTAD),
    ),
    "pasto-sintetico-vs-natural-tampico": (
        ("C144", "<td>Instalación (50 m²)</td><td>~$8,000–$12,000</td><td>~$18,000–$25,000</td>", f"<td>Instalación (50 m²)</td><td>desde {dinero(50 * P['pasto_instalado_m2'])}</td><td>{dinero(50 * P['sintetico_instalado_m2'][0])}–{dinero(50 * P['sintetico_instalado_m2'][1])}</td>", "Instalación con los precios oficiales por m²."),
        ("C145", "<td><strong>~$92,000–$150,000</strong></td><td><strong>~$18,000–$25,000</strong></td>", f"<td><strong>~$94,000–$182,000</strong></td><td><strong>{dinero(50 * P['sintetico_instalado_m2'][0])}–{dinero(50 * P['sintetico_instalado_m2'][1])}</strong></td>", "Suma recalculada con la instalación oficial."),
    ),
    "plantas-resistentes-sal-golfo-tampico": (
        ("C146", _DEK_BANQUETA, "12 especies de plantas que resisten la salinidad del aire marino en Tampico: ideales para jardines costeros, terrazas frente al Golfo y proyectos en zona playa.", M_DEK),
        ("C147", "¿Por qué la sal marina mata el 60% de las plantas?", "¿Por qué la sal marina mata tantas plantas?", M_ESTAD),
        ("C148", "La brisa salina del Golfo mata el 60% de las plantas comunes.", "La brisa salina del Golfo mata muchas plantas comunes.", M_ESTAD),
        ("C149", "a más de 2 km del mar el efecto disminuye 80%", "a más de 2 km del mar el efecto disminuye mucho", M_ESTAD),
        ("C150", "Más de 2 km de la costa el efecto de la sal disminuye 80%.", "A más de 2 km de la costa el efecto de la sal disminuye mucho.", M_ESTAD),
        ("C151", "retiene 50% menos nutrientes", "retiene menos nutrientes", M_ESTAD),
        ("C152", "pierde 80% del follaje", "pierde buena parte del follaje", M_ESTAD),
    ),
    "que-altura-de-pasto-sintetico-elegir": (
        ("C153", "es el más vendido por algo: nadie se arrepiente", "es buena opción por algo: nadie se arrepiente", M_VENDIDA),
        ("C154", "es el modelo más vendido en México para uso residencial", "es una opción muy equilibrada para uso residencial", M_VENDIDA),
        ("C155", "Aquí vive el <strong>90% de los jardines familiares</strong>.", "Aquí cae <strong>la mayoría de los jardines familiares</strong>.", M_ESTAD),
    ),
    "riego-automatico-tampico-roi": (
        ("C156", "casos reales por tamaño de jardín.", "ejemplos por tamaño de jardín.", M_CASO),
        ("C157", "casos reales de jardines en Tampico.", "ejemplos de jardines en Tampico.", M_CASO),
        ("C158", "~12–18 m³ (ahorro 40–60%)", "~18 m³ (ahorro de hasta 40%)", M_AHORRO),
        ("C159", "<td>~$600–$900 MXN</td>", "<td>~$900 MXN</td>", M_AHORRO),
        ("C160", "<td>$15,000–$60,000 MXN</td>", f"<td>{dinero(R0)}–{dinero(R1)}/m²</td>", M_RIEGO),
        ("C161", "<td>$8,000–$15,000</td><td>Aspersores básicos o goteo</td>", f"<td>{riego(30, 60)}</td><td>Aspersores básicos o goteo</td>", M_RIEGO),
        ("C162", "<td>$15,000–$28,000</td><td>Aspersores emergentes + goteo zonas plantas</td>", f"<td>{riego(60, 120)}</td><td>Aspersores emergentes + goteo zonas plantas</td>", M_RIEGO),
        ("C163", "<td>$28,000–$45,000</td><td>Sistema mixto multi-zona con programador</td>", f"<td>{riego(120, 200)}</td><td>Sistema mixto multi-zona con programador</td>", M_RIEGO),
        ("C164", "<td>$45,000–$90,000</td><td>Sistema completo con controlador inteligente</td>", f"<td>{riego(200, 500)}</td><td>Sistema completo con controlador inteligente</td>", M_RIEGO),
        ("C165", "<td>$90,000+</td>", f"<td>{SEGUN}</td>", M_RIEGO),
        ("C166", "3 casos reales de riego automático en Tampico", "3 ejemplos de riego automático en Tampico", M_CASO),
        ("C167", "Caso A: Residencial 80 m² en fraccionamiento de Madero", "Ejemplo A: residencial de 80 m²", M_CASO),
        ("C168", "Caso B: Residencial 200 m² en fraccionamiento privado de Tampico", "Ejemplo B: residencial de 200 m²", M_CASO),
        ("C169", "Caso C: Comercial 500 m² (oficinas corporativas en Altamira)", "Ejemplo C: comercial de 500 m²", M_CASO),
        ("C170", "<li>Inversión: $18,000 MXN</li>", f"<li>Inversión: {riego(80)}</li>", M_RIEGO),
        ("C171", "<li>Inversión: $38,000 MXN</li>", f"<li>Inversión: {riego(200)}</li>", M_RIEGO),
        ("C172", "<li>Inversión: $85,000 MXN</li>", f"<li>Inversión: {SEGUN}</li>", M_RIEGO),
        ("C173", "<li>Consumo después: 10 m³/mes → $500/mes</li>\n<li>Ahorro mensual: $600 MXN</li>\n<li>Ahorro anual: $7,200 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("C174", "<li>Consumo después: 16 m³/mes → $800/mes</li>\n<li>Ahorro mensual: $1,200 MXN</li>\n<li>Ahorro anual: $14,400 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("C175", "<li>Consumo después: 36 m³/mes → $1,800/mes</li>\n<li>Ahorro mensual: $2,700 MXN</li>\n<li>Ahorro anual: $32,400 MXN</li>", "<li>Consumo después: hasta 40% menos de agua</li>", M_AHORRO),
        ("C176", "<li>Consumo automático: 15 m³/mes × $50/m³ = $750/mes</li>\n<li><strong>Ahorro mensual: $750 MXN</strong></li>\n<li>Ahorro anual: $750 × 12 = <strong>$9,000 MXN/año</strong></li>", "<li>Consumo automático: hasta 40% menos (18 m³/mes × $50/m³ = $900/mes)</li>\n<li><strong>Ahorro mensual: $600 MXN</strong></li>\n<li>Ahorro anual: $600 × 12 = <strong>$7,200 MXN/año</strong></li>", M_AHORRO),
    ),
    "sistema-riego-automatico-conviene-tampico": (
        ("C177", _DEK_BANQUETA, "¿Conviene un sistema de riego automático en el clima tropical de Tampico? Guía honesta: cuándo sí, cuándo no y cuánto cuesta.", M_DEK),
        ("C178", "Para un jardín residencial de 100 m² el costo va de $15,000 (goteo simple) a $32,000 (sistema mixto con controlador WiFi). Para áreas comerciales o industriales con más de 500 m² el costo arranca en $80,000.", f"Para un jardín residencial de 100 m² el costo va de {riego(100)}. Para áreas comerciales o industriales con más de 500 m², {SEGUN}.", M_RIEGO),
        ("C179", "Costo en Tampico: $400–$800 por visita.", f"Costo: {SEGUN}.", "Precio sin confirmar."),
        ("C180", "cuesta solo $3,000–$5,000", f"se cotiza aparte", "Precio sin confirmar."),
        ("C181", "el costo del sistema ($15,000–$25,000) pesa más", "el costo del sistema pesa más", M_RIEGO),
        ("C182", "<td>$15,000–$25,000 (100 m²)</td>", f"<td>{riego(100)} (100 m²)</td>", M_RIEGO),
        ("C183", "<td>$8,000–$18,000 (100 m²)</td>", f"<td>{riego(100)} (100 m²)</td>", M_RIEGO),
        ("C184", "<td>$25,000–$45,000 (200 m²)</td>", f"<td>{riego(200)} (200 m²)</td>", M_RIEGO),
        ("C185", "<td>+$4,000 al sistema</td>", f"<td>{SEGUN}</td>", "Precio sin confirmar."),
        ("C186", "Ejemplo real: cuánto se ahorra", "Ejemplo: cuánto se ahorra", M_CASO),
        ("C187", "<p>Cliente típico Viveros Terra (Cd. Madero, casa residencial):</p>", "<p>Ejemplo de una casa residencial:</p>", M_CASO),
        ("C188", "controlador WiFi = <strong>$32,000</strong>", f"controlador WiFi = <strong>{riego(150)}</strong>", M_RIEGO),
        ("C189", "<li><strong>Ahorro mensual:</strong> $130 en agua + $400 en tiempo (regaban 2 hrs/día en verano)</li>\n", "", M_CASO),
        ("C190", "<p>Adicional: el pasto se mantiene 60% más uniforme = no hay que comprar pasto nuevo en 5 años (ahorro $8,000+).</p>", "<p>Adicional: el pasto se mantiene más uniforme.</p>", M_ESTAD),
        ("C191", "reduce el consumo de agua entre 35% y 45%", f"reduce el consumo de agua {datos.RIEGO_AHORRO}", M_AHORRO),
    ),
    "sistema-riego-automatizado-tampico": (
        ("C192", "tiene un costo de instalación de <strong>$8,000 a $25,000 pesos</strong> dependiendo del tipo y complejidad.", f"tiene un costo de instalación de <strong>{dinero(R0)} a {dinero(R1)} por m²</strong>, según el tipo y la complejidad.", M_RIEGO),
        ("C193", "Un <strong>sistema básico de aspersión para 50 m²</strong> cuesta entre $8,000 y $15,000 pesos instalado. Un sistema completo para jardín grande de 100–150 m² puede ir de $15,000 a $28,000.", f"Un <strong>sistema básico de aspersión para 50 m²</strong> cuesta {riego(50)} instalado. Un sistema completo para jardín grande de 100–150 m² puede ir de {riego(100, 150)}.", M_RIEGO),
        ("C194", "Costo aproximado para 50 m²: $8,000–$15,000", f"Costo aproximado para 50 m²: {riego(50)}", M_RIEGO),
        ("C195", "Costo aproximado para 20 plantas: $4,000–$10,000", f"Costo: {SEGUN}", M_RIEGO),
        ("C196", "(ahorro hasta 60%)", f"(ahorro {datos.RIEGO_AHORRO})", M_AHORRO),
        ("C197", "<td>$8,000–$15,000</td><td>$300–$600</td>", f"<td>{riego(50, 80)}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("C198", "<td>$4,000–$10,000</td><td>$200–$400</td>", f"<td>{SEGUN}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("C199", "<td>$15,000–$28,000</td><td>$500–$1,000</td>", f"<td>{riego(100, 150)}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("C200", "<td>$40,000–$150,000</td><td>$2,000–$8,000</td>", f"<td>{SEGUN}</td><td>Hasta 40% menos de agua</td>", M_RIEGO),
        ("C201", "<p>Para un sistema de $12,000 pesos en un jardín residencial de 80 m²:</p>", "<p>En un jardín residencial de 80 m²:</p>", M_RIEGO),
        ("C202", "<li>Ahorro en agua: ~$500/mes = $6,000/año</li>\n<li>Ahorro en jardinero (menos idas para riego manual): ~$300/mes = $3,600/año</li>\n<li>Menor mortalidad de plantas por riego inadecuado: valor estimado ~$2,000/año</li>\n<li><strong>Ahorro total anual: ~$11,600</strong></li>", f"<li>Ahorro en agua: {datos.RIEGO_AHORRO}</li>\n<li>Menos idas del jardinero para riego manual</li>\n<li>Menor mortalidad de plantas por riego inadecuado</li>", M_ESTAD),
        ("C203", "<strong>Visita técnica.</strong> Medimos el área", f"<strong>Visita técnica.</strong> {datos.VISITA_COSTO} Medimos el área", M_VISITA),
    ),
    "tierra-negra-costal-camion-tampico": (
        ("C204", "el camión volteo de 8 m³ a $1,500/m³ es más económico.", f"el camión volteo de 8 m³ en {CAMION_8} es más económico.", M_TIERRA),
        ("C205", "Costo camión 8 m³ ($12,000)", f"Costo camión 8 m³ ({CAMION_8})", M_TIERRA),
        ("C206", "<td>$12,000 (8 m³ completo)</td>", f"<td>{CAMION_8} (8 m³ completo)</td>", M_TIERRA),
        ("C207", "<td>$12,000 (cubre ~80 m²)</td>", f"<td>{CAMION_8} (cubre ~80 m²)</td>", M_TIERRA),
        ("C208", "<td>$12,000–$24,000</td>", f"<td>Desde {CAMION_8}</td>", M_TIERRA),
        ("C209", "se puede incluir en el mismo pedido de plantas sin costo de envío adicional", "se puede incluir en el mismo pedido de plantas", M_ENTREGA),
        ("C210", "Las entregas de camión tienen costo de flete según la distancia. Los costales se pueden incluir en pedidos de plantas o pasto sin costo adicional para órdenes mayores a $3,000 MXN.", datos.ENTREGA_COBRO, M_ENTREGA),
        ("C211", "más del doble que el camión ($1,500/m³)", f"más del doble que el m³ suelto ({dinero(P['tierra_negra_m3'])}/m³)", M_TIERRA),
        ("C212", "Un costal estándar de tierra negra vegetal en Viveros Terra pesa aproximadamente 25–30 kg y tiene un volumen de 25–30 litros (0.025–0.03 m³). Este peso varía ligeramente según el contenido de humedad al momento del llenado.", "No publicamos el peso porque varía con la humedad; un costal estándar de tierra negra vegetal en Viveros Terra tiene un volumen de 25–30 litros (0.025–0.03 m³).", "Sin peso de costal: el dueño no lo tiene."),
    ),
}


def claves():
    """Claves de todas las filas, en orden."""
    return [f[0] for f in FILAS_TODOS] + [f[0] for lista in FILAS.values() for f in lista]


def validar(decisiones):
    """Una decisión con una clave que no existe detiene todo: así nadie cree haber aplicado una respuesta del dueño."""
    desconocidas = sorted(set(decisiones) - set(claves()))
    if desconocidas:
        raise ValueError(f"DECISIONES con claves que no existen: {desconocidas}")


def resolver(filas, decisiones):
    """Tripletas (antes, después, motivo) de las filas, ya con las decisiones del dueño."""
    tripletas = ((viejo, decisiones.get(clave, nuevo), motivo) for clave, viejo, nuevo, motivo in filas)
    return tuple(t for t in tripletas if t[1] is not REVERTIR)


validar(DECISIONES)
TODOS = resolver(FILAS_TODOS, DECISIONES)
CORRECCIONES = {slug: resolver(lista, DECISIONES) for slug, lista in FILAS.items()}


def de(clave):
    return tuple(CORRECCIONES.get(clave, ()))
