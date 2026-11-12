"""SEO fase 2c (2026-11-11, docs/superpowers/plans/2026-11-10-seo-aeo-geo.md, Fase 2; mapa §2 G4, G9 y G11): el texto que
las fusiones del blog suman a los artículos que se quedan y el enlace al pilar de palmas en el primer párrafo de cada
ficha de palma. Todo sale de los artículos fusionados (que ya publicaba el sitio) o de datos.py; nada nuevo. Las filas de
blog_correcciones.FUSION_2C usan estos textos, así test_blog_paridad sigue exigiendo que lo único que cambia sea esto.

Fusiones con 301 (vercel.json):
- /blog/riego-automatico-tampico-roi y /blog/sistema-riego-automatico-conviene-tampico → /blog/sistema-riego-automatizado-tampico
  (cuándo sí y cuándo no conviene, presión, vida útil, control desde el celular, errores y la alternativa económica).
- /blog/jardin-bajo-presupuesto-tampico → /blog/cuanto-cuesta-jardin-tampico-precios (los tres niveles de presupuesto).
- /blog/palmas-tropicales-jardin-tampico y /blog/palmas-mas-vendidas-tampico-precios → /blog/palmas-para-jardin-tampico
  (artículo nuevo, articulo.NUEVOS: la URL vieja decía «mas-vendidas», frase prohibida).
- /blog/pasto-sintetico-para-perros → /pasto-sintetico/perros (contenido/perros.py: limpieza, olor, drenaje y errores).
De los artículos fusionados no se traen las cifras sin fuente (tarifa de agua, ahorro en pesos, «50% del agua se evapora»),
el plazo de recuperación ni la fertilización «cada 3–4 meses» contra «2 veces al año» (se contradecían).
"""
# ---------- Riego: de riego-automatico-tampico-roi y sistema-riego-automatico-conviene-tampico ----------
RIEGO_ANTES = ("<p>El ahorro real depende del tamaño del jardín y de cómo riegas hoy; un sistema bien programado ahorra hasta "
               "40% de agua frente a la manguera.</p>")
RIEGO_NUEVO = RIEGO_ANTES + """
<h2 id="cuando-conviene">¿Cuándo sí conviene el riego automático y cuándo no?</h2>
<p><strong>El riego automático conviene en Tampico cuando el jardín tiene más de 80 m² de área verde y al menos 4 zonas de plantas distintas.</strong> Para jardines menores a 50 m² o con muchos árboles maduros, regar manual sigue siendo más rentable.</p>
<h3>Cuándo sí conviene</h3>
<ul>
<li><strong>Jardín de más de 80 m²:</strong> el ahorro de tiempo y agua es significativo.</li>
<li><strong>4 o más zonas distintas:</strong> pasto + arbustos + macetas + huerta requieren riego diferenciado.</li>
<li><strong>Vacaciones frecuentes:</strong> nadie tiene que regar mientras estás fuera.</li>
<li><strong>Pasto San Agustín fino:</strong> requiere riego uniforme; manguera deja zonas amarillas.</li>
<li><strong>Casa con segundo piso o terrazas:</strong> imposible regar manual en altura.</li>
<li><strong>Adultos mayores propietarios:</strong> elimina el esfuerzo físico de regar diario.</li>
</ul>
<h3>Cuándo no conviene</h3>
<ul>
<li><strong>Jardín pequeño (menos de 50 m²):</strong> el costo del sistema pesa más que el agua que ahorras. En estos casos, un timer de manguera básico puede dar resultados similares.</li>
<li><strong>Mayoría de árboles maduros:</strong> los árboles grandes necesitan riego profundo manual, no aspersor superficial.</li>
<li><strong>Planes de rediseño en menos de 2 años:</strong> si piensas cambiar el layout del jardín, espera a tener el diseño definitivo antes de instalar el sistema. Las tuberías van bajo tierra y moverlas es costoso.</li>
<li><strong>Renta o vivienda temporal:</strong> la inversión no se recupera si te mudas en menos de 3 años.</li>
<li><strong>Plantas muy variadas con riegos opuestos:</strong> cactus + tropicales en mismo jardín es difícil de programar.</li>
<li><strong>Presupuesto limitado que prioriza la instalación del jardín:</strong> invertirlo en un mejor diseño y plantas de calidad da más retorno a corto plazo. El sistema puede añadirse en una segunda etapa sin problema.</li>
</ul>
<h2 id="presion-y-vida-util">Presión de agua, vida útil y control desde el celular</h2>
<h3>¿Funciona con baja presión de agua?</h3>
<p>Sí, con la configuración correcta. Los sistemas de goteo funcionan con presiones muy bajas (0.5–1 kg/cm²). Los aspersores emergentes requieren 1.5–3 kg/cm². Si la presión domiciliaria es baja, se puede instalar un tanque regulador o bomba de presión, según cotización. En fraccionamientos con cisterna y bomba ya hay presión suficiente.</p>
<h3>¿Cuánto dura un sistema de riego automático?</h3>
<p>Un sistema bien instalado y mantenido tiene una vida útil de 10 a 20 años. Las tuberías de PVC duran 15+ años. Los aspersores emergentes requieren reemplazo cada 5–8 años. El programador electrónico dura 8–12 años.</p>
<h3>¿Se puede controlar desde el celular?</h3>
<p>Sí, con controladores inteligentes WiFi que se gestionan desde una app. Permiten programar zonas, ajustar horarios remotamente y suspender riegos en días de lluvia. El costo adicional sobre un programador básico va según cotización.</p>
<h2 id="errores-comunes">Errores que ves en Tampico cuando se instala mal</h2>
<ol>
<li><strong>Aspersores que riegan la banqueta:</strong> mal calculado el radio. Solución: ajustar boquillas.</li>
<li><strong>Programar riego al mediodía:</strong> buena parte del agua se evapora. Mejor: <strong>5–7 AM y 7–9 PM</strong>.</li>
<li><strong>Mismo tiempo para todas las zonas:</strong> el pasto sol necesita el doble que el pasto sombra.</li>
<li><strong>Sin sensor de lluvia:</strong> sistema riega aunque acabe de llover. El sensor se agrega según cotización.</li>
<li><strong>Tubería barata:</strong> después de 2 años empieza a fugar. Usar polietileno alta densidad.</li>
</ol>
<h2 id="alternativa-economica">Alternativa económica: kit semi-automático</h2>
<p>Si el sistema completo está fuera de presupuesto, hay opciones intermedias en Tampico:</p>
<ul>
<li><strong>Programador de manguera:</strong> se conecta a la llave y abre/cierra solo. Funciona con aspersor fijo o manguera con goteros.</li>
<li><strong>Aspersores oscilantes con timer:</strong> cubren 30–60 m² cada uno.</li>
<li><strong>Goteo manual con cinta perforada:</strong> bajo presupuesto, requiere abrir la llave 2 veces al día.</li>
</ul>"""

RIEGO_SERVICIO_ANTES = ("<p><strong>Servicio Viveros Terra:</strong> Instalamos sistemas de riego automatizado en Tampico, Ciudad "
                        "Madero y Altamira. Cotiza por WhatsApp con las medidas de tu jardín.</p>")
RIEGO_SERVICIO_NUEVO = ("<p><strong>Servicio Viveros Terra:</strong> Instalamos sistemas de riego automatizado en Tampico, Ciudad "
                        "Madero y Altamira; ve la <a href=\"/sistema-riego-tampico\">instalación de sistema de riego en "
                        "Tampico</a>. Cotiza por WhatsApp con las medidas de tu jardín.</p>")

# ---------- Presupuesto: de jardin-bajo-presupuesto-tampico ----------
COSTOS_ANTES = ("<p>Para proyectos de cualquier tamaño, el primer paso es siempre una cotización sin compromiso. El equipo de "
                "Viveros Terra agenda una visita para medir y cotizar en Tampico, Madero y Altamira. El costo de la visita "
                "para cotizar depende de la ubicación del servicio; te lo confirmamos por WhatsApp antes de agendar.</p>")
COSTOS_NUEVO = COSTOS_ANTES + """
<h2 id="por-presupuesto">¿Qué jardín puedes hacer con $5,000, $20,000 o $50,000?</h2>
<p>Si ya tienes un número en mente, estos son tres niveles de inversión con los precios oficiales de Viveros Terra para Tampico, Madero y Altamira, con el desglose de lo que incluye cada uno.</p>
<div class="vt-art__tabla" tabindex="0" role="region" aria-label="Tabla: los 3 niveles de presupuesto"><table><thead><tr><th scope="col">Característica</th><th scope="col">Paquete $5,000</th><th scope="col">Paquete $20,000</th><th scope="col">Paquete $50,000</th></tr></thead><tbody><tr><td>Área aproximada</td><td>25 m²</td><td>80–90 m²</td><td>150–200 m²</td></tr><tr><td>Pasto instalado ($120/m²). Precio con terreno listo: limpio, nivelado y con tierra negra.</td><td>Sí</td><td>Sí</td><td>Sí</td></tr><tr><td>Tierra negra</td><td>1 m³</td><td>3 m³</td><td>Camión de 8 m³</td></tr><tr><td>Plantas ornamentales</td><td>Según cotización, con lo que reste</td><td>Según cotización, con 2 palmas</td><td>Según cotización, con 3 palmas medianas</td></tr><tr><td>Diseño profesional</td><td>No (asesoría básica)</td><td>Plan Terra Esencial</td><td>Plan Terra Completo</td></tr><tr><td>Sistema de riego ($180–$320/m²)</td><td>Se cotiza aparte</td><td>Se cotiza aparte</td><td>Se cotiza aparte</td></tr><tr><td>Árbol ornamental</td><td>No</td><td>Opcional</td><td>1 incluido</td></tr><tr><td>Mantenimiento mes 1</td><td>No</td><td>No</td><td>Sí, incluido</td></tr><tr><td>Tiempo de instalación</td><td>1 día</td><td>2–4 días</td><td>1–3 semanas</td></tr></tbody></table></div>
<h3>Paquete $5,000</h3>
<p>Es un buen punto de entrada para casas de fraccionamiento con lotes compactos o jardines frontales angostos: 25 m² de pasto San Agustín instalado, 1 m³ de tierra negra vegetal y plantas ornamentales básicas de bajo mantenimiento (helechos, croton, ixora, etc.) con lo que reste, según cotización. No incluye diseño profesional, riego automatizado, palmas ni árbol ornamental.</p>
<ul>
<li>Pasto instalado 25 m² × $120 = $3,000</li>
<li>Tierra negra 1 m³ = $1,500</li>
<li><strong>Subtotal: $4,500</strong></li>
<li>Plantas: según cotización, con lo que reste</li>
</ul>
<h3>Paquete $20,000</h3>
<p>Con este presupuesto ya puedes tener un jardín con carácter: diseño básico, plantas con impacto visual y una o dos palmas. El riego por aspersores se cotiza aparte.</p>
<ul>
<li>Pasto instalado 90 m² × $120 = $10,800</li>
<li>Tierra negra 3 m³ = $4,500</li>
<li>Diseño Plan Terra Esencial = $3,000</li>
<li><strong>Subtotal: $18,300</strong></li>
<li>Plantas y 2 palmas (areca o coco plumoso desde $250 c/u): según cotización, con lo que reste</li>
<li>Riego por aspersores: se cotiza aparte ($180–$320/m²)</li>
</ul>
<p>Este presupuesto alcanza para 80–90 m² con diseño. Con más área, cada m² adicional de pasto instalado suma desde $120.</p>
<h3>Paquete $50,000</h3>
<p>Es el presupuesto para quienes quieren un jardín que dure décadas, con palmas de porte real y un diseño completo.</p>
<ul>
<li>Pasto instalado 160 m² × $120 = $19,200</li>
<li>Tierra negra, camión de 8 m³ = $5,200</li>
<li>Diseño Plan Terra Completo = $6,500</li>
<li><strong>Subtotal: $30,900</strong></li>
<li>25 plantas, 3 palmas medianas, árbol ornamental y acabados: según cotización, con lo que reste</li>
<li>Riego automatizado: se cotiza aparte ($180–$320/m²)</li>
</ul>
<h3>¿Puedo empezar con poco y crecer mi jardín después?</h3>
<p>Sí, y es un enfoque muy práctico. Comenzar con pasto y tierra en la primera etapa, luego agregar plantas y palmas en la segunda, y finalmente instalar riego en la tercera es perfectamente viable. Lo importante es que el diseño inicial contemple el estado final para no deshacer trabajo previo.</p>
<h3>Cómo elegir tu nivel de inversión</h3>
<ul>
<li><strong>¿Cuánto tiempo tienes para darle mantenimiento manual?</strong> Si es poco, invierte en riego automatizado aunque eso suba el presupuesto. El jardín sin riego automático en Tampico puede requerir 3–5 horas semanales de atención.</li>
<li><strong>¿Planeas quedarte más de 5 años en la propiedad?</strong> Si sí, la inversión en diseño y materiales de mayor calidad tiene sentido. Si no, el paquete básico da resultados visuales sin comprometer demasiado capital.</li>
<li><strong>¿El jardín es para uso propio o para vender/rentar la propiedad?</strong> Para venta o renta, el impacto visual inmediato pesa más que el diseño optimizado a largo plazo. En esos casos, palmas medianas y pasto verde impecable ofrecen el mejor retorno por peso invertido.</li>
</ul>"""

# ---------- Ficha de palma: el ancla exacta del pilar al final del primer párrafo (mapa §2 G4) ----------
ANCLA_PILAR = "venta de palmas en Tampico"
PILAR_RUTA = "/palmas-tropicales-tampico"
PILAR = ' Más especies y precios por tamaño en nuestra <a href="/palmas-tropicales-tampico">venta de palmas en Tampico</a>.'

# Primer párrafo de cada ficha con captura anterior, tal como se publicaba (la palma bambú es nueva: articulo.NUEVOS).
PRIMER_PARRAFO = {
    'palma-areca-tampico': (
        '<p>La Palma Areca (<em>Dypsis lutescens</em>, antes clasificada como <em>Chrysalidocarpus lutescens</em>) es originaria de Madagascar y se ha adaptado perfectamente al clima cálido-húmedo de Tampico. Se reconoce por sus <strong>múltiples tallos delgados de color amarillo verdoso</strong> que crecen agrupados desde la base, coronados por hojas plumosas arqueadas.</p>'),
    'palma-bismarckia-bismarckia-nobilis-tampico': (
        '<p>La Palma Bismarckia (<em>Bismarckia nobilis</em>) es originaria de Madagascar. Su rasgo más conocido es el color de sus hojas: grandes abanicos de un tono <strong>plateado-azulado</strong> que contrastan con el verde de casi cualquier otra planta del jardín. Es una palma de tronco único, robusto, y de presencia escultórica.</p>'),
    'palma-coco-plumoso-tampico': (
        '<p>La Palma Coco Plumoso (<em>Syagrus romanzoffiana</em>), también conocida como palma reina o pindó, es originaria de Sudamérica y una de las palmas ornamentales más difundidas del mundo por su facilidad de adaptación. Se reconoce por su <strong>tronco liso y esbelto</strong>, ligeramente anillado, coronado por hojas plumosas que se arquean hacia abajo dándole un aspecto más suave y orgánico que otras palmas de la región.</p>'),
    'palma-cola-de-zorro-wodyetia-bifurcata-tampico': (
        '<p>La Palma Cola de Zorro (<em>Wodyetia bifurcata</em>) es una palma originaria del norte de Australia. Su nombre viene de sus hojas: los foliolos salen por todos lados del raquis y le dan al follaje un aspecto <strong>denso y cilíndrico, como una cola de zorro</strong>. Tiene un tronco recto, liso y anillado, de color gris claro, que termina en una corona verde brillante.</p>'),
    'palma-kerpis-howea-forsteriana-tampico': (
        '<p>La Palma Kerpis (<em>Howea forsteriana</em>), conocida también como Kentia, es originaria de la Isla Lord Howe en Australia. A diferencia de la mayoría de las palmas tropicales que exige Tampico —Washingtona, Real, Coco Plumoso—, la Kerpis fue seleccionada por generaciones de diseño de interiores precisamente por lo contrario: <strong>tolera sombra, luz artificial y ambientes cerrados</strong> sin perder su follaje verde oscuro y arqueado.</p>'),
    'palma-real-roystonea-regia-tampico': (
        '<p>La Palma Real (<em>Roystonea regia</em>) es originaria de zonas tropicales del Golfo de México y el Caribe, incluyendo Cuba, Florida y regiones costeras de México. Es fácil de reconocer por su <strong>tronco liso, recto y de color gris plateado</strong>, que se ensancha ligeramente en la base y termina en una corona compacta de hojas pinnadas arqueadas.</p>'),
    'palma-triangular-dypsis-decaryi-tampico': (
        '<p>La Palma Triangular (<em>Dypsis decaryi</em>) es una palma originaria del sur de Madagascar. Su nombre viene de la forma en que crecen sus hojas: se insertan en el tronco en <strong>tres filas verticales</strong>, de modo que, vista desde arriba, la base de la palma dibuja un <strong>triángulo casi perfecto</strong>. Sus hojas son arqueadas, de un verde grisáceo-plateado, y el conjunto da un aspecto escultural y muy ordenado.</p>'),
    'palma-washingtona-tampico': (
        '<p>La Palma Washingtona (<em>Washingtonia robusta</em>, también conocida como Washingtonia filifera en su variante de California) es la especie más plantada en avenidas, camellones y proyectos residenciales de todo el sur de Tamaulipas. Su <strong>tronco delgado y su copa compacta en forma de abanico</strong> la hacen fácil de identificar, y su famosa "faldilla" de hojas secas que cuelgan del tronco es parte de su aspecto característico.</p>'),
    'cuidados-palma-del-viajero-ravenala': (
        '<p>Su nombre dice "palma" pero técnicamente no lo es. La <em>Ravenala madagascariensis</em> pertenece a la familia Strelitziaceae — la misma que las flores de ave del paraíso. Lo que todos llamamos "palma del viajero" es en realidad un árbol tropical con un comportamiento único: sus hojas crecen en un solo plano formando un abanico perfecto que puede llegar a los 3 metros de diámetro.</p>'),
}


def con_pilar(parrafo):
    """El párrafo con el enlace al pilar antes de cerrar."""
    return parrafo.removesuffix("</p>") + PILAR + "</p>"
