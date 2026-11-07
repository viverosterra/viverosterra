"""Corrección única de datos contradictorios (Etapa 1b, spec §5.2 y decisiones del dueño del 2026-11-07).

Reglas globales (todas las páginas, llms.txt y las fuentes de tools/pasto y tools/servicios): domicilio "209 Sur"
(también en el JSON-LD, con calle y código postal oficiales), promesa única de respuesta, perfiles oficiales y una sola
ortografía de flamboyán. Cambios por archivo: home, pasto en rollo, mayoreo, sintético en Tampico, árboles
ornamentales, catálogo, diseño, materiales, cuestionario, blogs de precios, índice del blog, gracias y llms.txt.
Retira el banner de temporada de la home, la barra "Lote semanal" y las etiquetas de búsquedas del blog. Los valores
salen de tools/site/datos.py. Es idempotente: lo ya corregido se salta; lo que no encuentra y no está corregido lo
reporta y se detiene.

Uso: python3 tools/site/corregir_datos.py   (desde cualquier carpeta; después corre python3 tools/site/build.py)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
from shell import fin_elemento  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PUBLIC = RAIZ / "public"
PROMESA = datos.PROMESA  # "Respondemos en menos de 1 hora en horario"
HORARIO = datos.HORARIO  # "Lun a vie 9 a 18 h, sáb 9 a 14 h"
COMPLETA = datos.PROMESA_COMPLETA
EN_1_HORA = "en menos de 1 hora en horario"
P = datos.PRECIOS
PLANTAS_CONDICION = '(<a href="/politicas#garantia-plantas">ver condiciones</a>)'

GLOBALES = (
    # Promesa única de respuesta (spec §5.3). Primero las frases completas, después las sueltas.
    ("Cotización gratis, sin compromiso. Respondemos hoy mismo y enviamos precio en menos de 2 horas.",
     f"Cotización gratis, sin compromiso. {PROMESA}."),
    ("Respondemos por WhatsApp hoy mismo.", f"Respondemos por WhatsApp {EN_1_HORA}."),
    ("Respondemos en minutos por WhatsApp", f"Respondemos por WhatsApp {EN_1_HORA}"),
    ("Respondemos hoy · Lun–Sáb", COMPLETA),
    ("Respuesta hoy · Lun–Sáb", COMPLETA),
    ("Respondemos en menos de 4 horas hábiles. Lun–Vie 9–18h, Sáb 9–14h.", f"{COMPLETA}."),
    ("Respondemos en menos de 4 horas hábiles.", f"{PROMESA}."),
    ("Respondemos el mismo día · Lun a vie", f"{PROMESA} · Lun a vie"),
    ("Respondemos hoy mismo · Lun a vie", f"{PROMESA} · Lun a vie"),
    ("Te contactamos en 24h · Lun a vie", f"{PROMESA} · Lun a vie"),
    ("Sin compromiso · Respuesta en menos de 2 horas · Lun–Sáb", f"Sin compromiso · {COMPLETA}"),
    ("Respuesta en menos de 2 horas · Lun–Sáb", COMPLETA),
    ("Atención directa en menos de 2 horas", "Respuesta en menos de 1 hora en horario"),
    ("Precio claro en menos de 2 horas, sin compromiso", f"Precio claro {EN_1_HORA}, sin compromiso"),
    ("Cotiza tu jardín en menos de 2 horas", f"Cotiza tu jardín: respondemos {EN_1_HORA}"),
    ("Cotiza en menos de 2 horas.", f"{PROMESA}."),
    ("Te contactamos en 24 hrs", f"Te respondemos {EN_1_HORA}"),
    ("Respuesta en 24h", "Respuesta en menos de 1 hora"),
    ("te respondemos con diagnóstico y solución el mismo día.",
     f"te respondemos {EN_1_HORA} con el diagnóstico y la solución."),
    # Perfiles oficiales y ortografía.
    ("https://il.linkedin.com/company/viveros-terra-tampico", "https://www.linkedin.com/company/viveros-terra-tampico"),
    ("http://www.tiktok.com/@viverosterra", "https://www.tiktok.com/@viverosterra"),
    ("Framboyán", "Flamboyán"),
    ("Framboy%C3%A1n", "Flamboy%C3%A1n"),
)
REGLAS = (
    # Domicilio: siempre "209 Sur"; en el JSON-LD la calle va sola y con su código postal.
    (re.compile(r"(Obreg[oó]n 209)(?! Sur)"), r"\1 Sur"),
    (re.compile(r'("streetAddress":\s*)"Av\. Álvaro Obregón 209 Sur, Col\. Ampliación Unidad Nacional"'),
     rf'\1"{datos.CALLE}"'),
    (re.compile(rf'("streetAddress":"{re.escape(datos.CALLE)}","addressLocality":"Ciudad Madero",'
                r'"addressRegion":"Tamaulipas",)(?!"postalCode")'), rf'\1"postalCode":"{datos.CP}",'),
    # Promesa única.
    (re.compile(r"\b([Rr])espondemos (?:hoy mismo|hoy|el mismo día|en minutos)\b"), rf"\1espondemos {EN_1_HORA}"),
    (re.compile(r"\bRespuesta el mismo día\b"), "Respuesta en menos de 1 hora en horario"),
    (re.compile(r'>Mismo día</div>(\s*<div[^>]*>)Respuesta a cotización<'), r">1 hora</div>\1Respuesta máxima en horario<"),
    (re.compile(r"https://www\.instagram\.com/viverosterra(?!mx)"), "https://www.instagram.com/viverosterramx"),
    (re.compile(r"(?<!conocido como )framboyán"), "flamboyán"),
)

PAGO_ANTICIPO = "No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos un anticipo"
CONTADO = "Contado o mensualidades con tarjeta de crédito"

POR_ARCHIVO = (
    # Home: prueba social sin contradicción, FAQ de precio con cifras (A04 §7 bloque A), sin "líder".
    ("public/index.html",
     '<strong style="color:#A5D6A7">Más de 1,500 clientes</strong> han calculado su jardín con nosotros',
     f'<strong style="color:#A5D6A7">{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones</strong> '
     f"desde {datos.DESDE}"),
    ("public/index.html",
     '"text":"Cotización inmediata por WhatsApp al 833 326 8008. Varía según tipo y volumen."',
     f'"text":"En Viveros Terra el pasto San Agustín en rollo cuesta ${P["pasto_solo_m2"]} por m² solo el pasto y desde '
     f'${P["pasto_instalado_m2"]} por m² instalado, con IVA incluido. El instalado incluye la preparación básica del '
     f'terreno, la colocación y una garantía de arraigo de 15 a 20 días. En pedidos de {P["pasto_mayoreo_minimo_m2"]} m² '
     f'o más, el mayoreo cuesta desde ${P["pasto_mayoreo_m2"]}/m². Precios vigentes en noviembre de 2026 para Tampico, '
     'Ciudad Madero y Altamira."'),
    ("public/index.html",
     '<div class="pb-5">El precio varía según tipo y volumen. Te ofrecemos <strong>cotización inmediata por WhatsApp</strong> '
     'al 833 326 8008. En minutos sabrás el costo por m² con o sin instalación.</div>',
     f'<div class="pb-5">En Viveros Terra el pasto San Agustín en rollo cuesta <strong>${P["pasto_solo_m2"]} por m² solo el '
     f'pasto</strong> y <strong>desde ${P["pasto_instalado_m2"]} por m² instalado</strong>, con IVA incluido. El instalado '
     'incluye la preparación básica del terreno, la colocación y una garantía de arraigo de 15 a 20 días. En pedidos de '
     f'{P["pasto_mayoreo_minimo_m2"]} m² o más, el mayoreo cuesta desde ${P["pasto_mayoreo_m2"]}/m². Precios vigentes en '
     'noviembre de 2026 para Tampico, Ciudad Madero y Altamira. <a href="/precios">Ver lista de precios</a></div>'),
    ("public/index.html",
     '<span class="text-primary font-semibold text-sm uppercase tracking-wider">El vivero líder en Tampico</span>',
     f'<span class="text-primary font-semibold text-sm uppercase tracking-wider">Vivero en Cd. Madero desde {datos.DESDE}</span>'),
    ("public/index.html",
     '<div class="text-2xl font-display font-bold text-accent">+127</div>\n'
     '            <div class="text-white/55 text-xs mt-1">Reseñas verificadas</div>',
     f'<div class="text-2xl font-display font-bold text-accent">{datos.INSTALACIONES}</div>\n'
     f'            <div class="text-white/55 text-xs mt-1">Instalaciones desde {datos.DESDE}</div>'),
    ("public/index.html",
     "Viveros Terra es la empresa líder en jardinería y pasto en rollo del sur de Tamaulipas.",
     f"Viveros Terra es un vivero y empresa de jardinería de Ciudad Madero, fundada en {datos.DESDE}."),
    ("public/index.html", "<!-- BANNER URGENCIA ESTACIONAL — actualizar texto según temporada -->\n", ""),
    # Pasto en rollo: nunca "pagas cuando"; anticipo confirmado por el dueño (sin porcentaje inventado); tabla
    # comparativa sin desacreditar el sintético que también vendemos.
    ("public/pasto-en-rollo-tampico/index.html",
     '<div class="text-gray-500 text-sm mt-1">Pagas cuando ves el resultado</div>',
     f'<div class="text-gray-500 text-sm mt-1">{CONTADO}</div>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '<p class="text-white/75 text-xs">Pagas cuando ves tu jardín listo — sin pago total por adelantado</p>',
     f'<p class="text-white/75 text-xs">{CONTADO}</p>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '<span class="text-primary font-bold">Pagas cuando ves el resultado</span>',
     f'<span class="text-primary font-bold">{CONTADO}</span>'),
    ("public/pasto-en-rollo-tampico/index.html", "Pagas cuando ves tu jardín listo</li>", "Mensualidades con tarjeta de crédito</li>"),
    ("public/pasto-en-rollo-tampico/index.html", "</svg> Pagas al ver el resultado</span>", f"</svg> {CONTADO}</span>"),
    ("public/pasto-en-rollo-tampico/index.html",
     "No. <strong>Pagas cuando ves tu jardín terminado.</strong> Sin pago total por adelantado, sin sorpresas. Lo importante "
     "es que empieces con tranquilidad y que confíes en el resultado.",
     f"No. {PAGO_ANTICIPO}, y puedes pagar en mensualidades con tarjeta de crédito en cotizaciones desde $2,000. Si una "
     "sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego."),
    ("public/pasto-en-rollo-tampico/index.html",
     '<div class="pb-5">Sí. La idea es sencilla: <strong>pagas cuando ves el resultado.</strong> No pedimos el 100% por '
     "adelantado. Al confirmar tu proyecto coordinamos el esquema contigo directamente — sin letras chicas ni sorpresas. "
     "de pago flexibles</strong> — adaptamos las condiciones a tu proyecto y conveniencia. Lo que no hacemos es pedirte el "
     "100% por adelantado sin haber entregado nada. Pregúntanos al cotizar y te decimos qué opciones hay para tu caso.</div>",
     f'<div class="pb-5">Sí. {PAGO_ANTICIPO}, sin letra chica. También puedes pagar en mensualidades con tarjeta de crédito '
     'desde $2,000; los plazos dependen del monto (<a href="/politicas#mensualidades">ver condiciones</a>).</div>'),
    ("public/pasto-en-rollo-tampico/index.html",
     "Cotización en menos de 1 hora. Sin compromiso. Pagas cuando ves tu jardín listo.",
     f"{PROMESA}. Sin compromiso. Si una sección no arraiga en 15 a 20 días, la reponemos sin costo."),
    ("public/pasto-en-rollo-tampico/index.html",
     "La cotización real la hacemos por WhatsApp en minutos.",
     f"Te mandamos la cotización real por WhatsApp {EN_1_HORA}."),
    ("public/pasto-en-rollo-tampico/index.html",
     '<h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mt-3 mb-3">Pasto San Agustín en rollo o pasto sintético</h2>\n'
     '      <p class="text-gray-700 max-w-2xl mx-auto">Las dos opciones más solicitadas para jardines en Tampico, comparadas en '
     "costo, mantenimiento, durabilidad y estética.</p>",
     '<h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mt-3 mb-3">¿Cuál te conviene según tu espacio?</h2>\n'
     '      <p class="text-gray-700 max-w-2xl mx-auto">Vendemos e instalamos los dos en Tampico. Esta tabla te ayuda a elegir '
     "según tu espacio, tu presupuesto y el tiempo que quieras dedicarle.</p>"),
    ("public/pasto-en-rollo-tampico/index.html",
     '<tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Temperatura al sol</td><td class="py-3 px-4 sm:px-6">'
     '28-32°C (fresco)</td><td class="py-3 px-4 sm:px-6">50-60°C (quema)</td></tr>',
     '<tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Riego</td><td class="py-3 px-4 sm:px-6">Diario al '
     'instalar; después, según el clima</td><td class="py-3 px-4 sm:px-6">Sin riego; solo un enjuague ocasional</td></tr>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '          <tr><td class="py-3 px-4 sm:px-6 font-semibold">Sensación al tacto</td><td class="py-3 px-4 sm:px-6">Natural, '
     'suave</td><td class="py-3 px-4 sm:px-6">Plástico, áspero</td></tr>\n'
     '          <tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Reciclable</td><td class="py-3 px-4 sm:px-6">'
     'Sí (compostable)</td><td class="py-3 px-4 sm:px-6">No (residuo plástico)</td></tr>\n',
     ""),
    ("public/pasto-en-rollo-tampico/index.html",
     '<td class="py-3 px-4 sm:px-6">Terrazas sin tierra, pet áreas</td>',
     '<td class="py-3 px-4 sm:px-6">Terrazas, azoteas, áreas sin riego y zonas para mascotas</td>'),
    ("public/pasto-en-rollo-tampico/index.html",
     "Para jardines residenciales en Tampico con clima cálido-húmedo, el pasto natural San Agustín ofrece mejor relación "
     "costo-beneficio a largo plazo (15+ años vs 8-10 años). El sintético tiene sentido solo en terrazas, áticos o zonas sin "
     "tierra disponible.",
     "Si tu jardín tiene tierra y puedes regarlo, el San Agustín cuesta menos por metro y dura más. Si es una terraza, una "
     "azotea o un área sin riego, te conviene el sintético: también lo vendemos e instalamos en Tampico "
     '(<a href="/pasto-sintetico-tampico" class="text-primary font-semibold underline">ver pasto sintético</a>).'),
    ("public/pasto-en-rollo-tampico/index.html",
     "<!-- ═══ DISPONIBILIDAD SEMANAL — el diferenciador de frescura ═══ -->\n", ""),
    ("public/pasto-en-rollo-tampico/index.html", ".disponibilidad-bar{background:linear-gradient(90deg,#064e3b,#065f46)}\n", ""),
    ("public/pasto-en-rollo-tampico/index.html",
     "Lo manejamos con un sistema de lote semanal para garantizar que nunca almacenamos pasto más de una semana.",
     "Así nunca almacenamos pasto más de una semana."),
    # Tierra negra: los años de la empresa salen de la fundación (2007), no "20+".
    ("public/tierra-negra-vegetal-tampico/index.html",
     '<div class="text-3xl font-display font-bold text-primary">20+</div>\n'
     '        <div class="text-gray-500 text-sm mt-1">Años en Tampico</div>',
     '<div class="text-3xl font-display font-bold text-primary">+18</div>\n'
     f'        <div class="text-gray-500 text-sm mt-1">Años en la región (desde {datos.DESDE})</div>'),
    # Mayoreo: el mínimo es 500 m²; la respuesta, la promesa única.
    ("public/mayoreo-pasto-tampico/index.html", "pedidos a partir de 200 m²",
     f"pedidos a partir de {P['pasto_mayoreo_minimo_m2']} m²"),
    ("public/mayoreo-pasto-tampico/index.html", '<div class="font-semibold text-white">Cotización en 24 horas</div>',
     '<div class="font-semibold text-white">Respuesta en menos de 1 hora en horario</div>'),
    # Sintético en Tampico (fuente: el generador): los 9 modelos en existencia; "para llevar hoy" solo Toscana 18 y 28.
    ("tools/pasto/local.py",
     'existencia para llevar el mismo día, y los otros 7 modelos sobre pedido. Atendemos de lunes a viernes de 9 a 18 h "',
     'existencia para llevar hoy; los otros 7 modelos también están en existencia y llegan en 3 a 5 días. Atendemos de '
     'lunes a viernes de 9 a 18 h "'),
    # Flamboyán desde $250 (decisión del dueño 2026-11-07).
    ("public/arboles-ornamentales-tampico/index.html", "Flamboyán desde $500", f"Flamboyán desde ${P['flamboyan']}"),
    ("public/arboles-ornamentales-tampico/index.html",
     'Desde <strong>$350</strong></span><span class="svc-hero__price-alt">crespón $350 · jacaranda $450 · flamboyán $500</span>',
     f'Desde <strong>${P["flamboyan"]}</strong></span><span class="svc-hero__price-alt">flamboyán ${P["flamboyan"]} · '
     'crespón $350 · jacaranda $450</span>'),
    ("tools/servicios/pages.py",
     'price_pre="Desde", price="$350", price_unit="", price_alt="· crespón $350 · jacaranda $450 · flamboyán $500",',
     f'price_pre="Desde", price="${P["flamboyan"]}", price_unit="", price_alt="· flamboyán ${P["flamboyan"]} · crespón $350 '
     '· jacaranda $450",'),
    # Garantía de plantas siempre con su condición.
    ("public/catalogo.html",
     "</svg>Garantía de arraigo 30 días</span>",
     '</svg>Garantía de arraigo 30 días en plantas que sembramos nosotros · <a href="/politicas#garantia-plantas">ver '
     "condiciones</a></span>"),
    ("public/diseno-jardines-tampico/index.html",
     "<strong>Garantía de arraigo 30 días:</strong> reponemos plantas sin costo",
     "<strong>Garantía de arraigo 30 días:</strong> reponemos sin costo las plantas que sembramos nosotros, con el riego "
     f"indicado {PLANTAS_CONDICION}"),
    ("public/diseno-jardines-tampico/index.html", "y garantia de arraigo 30 dias.",
     "y garantia de arraigo 30 dias en las plantas que sembramos, con el riego indicado."),
    ("public/diseno-jardines-tampico/index.html", '<td class="p-3">Garantía de arraigo</td>',
     '<td class="p-3">Garantía de arraigo en plantas que sembramos</td>'),
    ("public/palmas-mayoreo-proyectos/index.html", "CFDI 4.0 y garantía de arraigo de 30 días.\"",
     "CFDI 4.0 y garantía de arraigo de 30 días en siembra propia.\""),
    ("public/palmas-mayoreo-proyectos/index.html", "CFDI y garantía de arraigo de 30 días. Cobertura",
     "CFDI y garantía de arraigo de 30 días en siembra propia. Cobertura"),
    ("public/palmas-mayoreo-proyectos/index.html", "<span>Garantía de arraigo 30 días</span></div>",
     "<span>Garantía de arraigo 30 días en siembra propia</span></div>"),
    # Materiales y servicios: respuesta con la promesa única.
    ("public/blog/palmas-mas-vendidas-tampico-precios/index.html",
     "te confirmamos disponibilidad hoy mismo", f"te confirmamos disponibilidad {EN_1_HORA}"),
    ("public/sistema-riego-tampico/index.html", "Cotización personalizada hoy mismo.",
     f"Te respondemos {EN_1_HORA} con tu cotización."),
    # Cuestionario de diseño: la promesa única en lugar de "24 horas".
    ("public/cuestionario.html",
     "Nuestro diseñador creará una propuesta hecha exactamente para ti y te contactará en menos de 24 horas.",
     f"Nuestro diseñador creará una propuesta hecha exactamente para ti; te respondemos {EN_1_HORA}."),
    ("public/cuestionario.html",
     "Un diseñador de Viveros Terra se pondrá en contacto contigo en menos de 24 horas para coordinar tu visita técnica.",
     f"Un diseñador de Viveros Terra te responde {EN_1_HORA} para coordinar tu visita técnica."),
    # Blogs de precios: mantenimiento desde $750/mes; el paquete de $50,000 es "Proyecto completo" (los planes de diseño
    # son Plan Terra Esencial $3,000, Completo $6,500 y Premium desde $18,000).
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "va desde $500/mes para jardines pequeños",
     f"va desde ${P['mantenimiento_mes']}/mes para jardines pequeños"),
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "Plan Terra Completo de $50,000+",
     "Proyecto completo de $50,000+"),
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "Plan Terra Completo ($50,000+)",
     "Proyecto completo ($50,000+)"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "Plan Terra Completo ($50,000+)",
     "Proyecto completo ($50,000+)"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "El paquete de $50,000 (Plan Terra Completo)",
     "El Proyecto completo de $50,000"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "El Plan Terra Completo incluye el primer mes de mantenimiento",
     "El Proyecto completo incluye el primer mes de mantenimiento"),
    # Índice del blog: sin notas internas ni métricas; el conteo lo pone el build.
    ("public/blog/index.html", "</svg>22 artículos</span>", '</svg><span data-vt-conteo="blog">52</span> guías</span>'),
    ("public/blog/index.html", '<div class="vt-hero__metric-num">52</div>',
     '<div class="vt-hero__metric-num"><span data-vt-conteo="blog">52</span></div>'),
    ("public/blog/index.html",
     '<div class="vt-hero__metric-num">+900</div>\n        <div class="vt-hero__metric-label">Proyectos completados</div>',
     f'<div class="vt-hero__metric-num">{datos.CLIENTES}</div>\n        <div class="vt-hero__metric-label">Clientes</div>'),
    ("public/blog/index.html", "Por el equipo de expertos de Viveros Terra.", "Por el equipo técnico de Viveros Terra."),
    ("public/blog/index.html", '<h2 class="text-2xl font-display font-bold text-gray-900">Los más buscados</h2>',
     '<h2 class="text-2xl font-display font-bold text-gray-900">Para empezar</h2>'),
    ("public/blog/index.html", '      <span class="text-gray-400 text-sm">· Recuperados del Wix con miles de búsquedas</span>\n', ""),
    ("public/blog/index.html",
     ".tag-hot{background:#ff5252;color:#fff;font-size:.65rem;font-weight:700;padding:.15rem .5rem;border-radius:99px;"
     "vertical-align:middle;margin-left:.35rem}\n", ""),
    # Gracias: promesa única, pasos alrededor de la respuesta en menos de 1 hora, sin emojis.
    ("public/gracias/index.html",
     '<p class="subtitle"><strong>Respondemos en menos de 1 hora en horario</strong> (lun a vie 9 a 18 h, sáb 9 a 14 h) y te '
     "enviamos el detalle completo a tu correo.</p>",
     f'<p class="subtitle"><strong>{PROMESA}</strong> · {HORARIO}.</p>'),
    ("public/gracias/index.html",
     "<h3>📋 Qué sigue ahora</h3>\n        <ol>\n"
     "          <li><strong>Hoy mismo</strong> (lun–vie 9am–6pm): te llega correo con cotización detallada por servicio.</li>\n"
     "          <li><strong>En 24 hrs:</strong> te contactamos por WhatsApp para agendar visita técnica gratuita.</li>\n"
     "          <li><strong>En la visita:</strong> medimos exacto, te damos precio cerrado y plan de trabajo.</li>\n"
     "          <li><strong>Si te interesa:</strong> arrancamos el proyecto en 3–10 días.</li>\n        </ol>",
     "<h3>Qué sigue ahora</h3>\n        <ol>\n"
     f"          <li><strong>En menos de 1 hora en horario</strong> te escribimos por WhatsApp o correo con tu cotización.</li>\n"
     "          <li><strong>Si hace falta,</strong> agendamos contigo una visita para medir.</li>\n"
     "          <li><strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.</li>\n        </ol>"),
    ("public/gracias/index.html", "        Hablar ahora por WhatsApp\n", "        Adelantar por WhatsApp\n"),
    ("public/gracias/index.html", "💡 <strong>Tip:</strong> mientras esperas, revisa nuestro", "<strong>Mientras tanto:</strong> revisa nuestro"),
    # llms.txt: entidad sin "líder", datos y páginas que faltaban, "Lo que no hacemos".
    ("public/llms.txt", "> Empresa de jardinería líder en el sur de Tamaulipas, México, desde 2007.",
     "> Vivero y empresa de jardinería de Ciudad Madero, Tamaulipas, México, fundada el 12 de diciembre de 2007."),
    ("public/llms.txt", "Datos clave:\n- Fundada: 12 de diciembre de 2007 (más de 18 años en la región)\n",
     "Última actualización: 2026-11-07\n\nDatos clave:\n- Fundada: 12 de diciembre de 2007 (más de 18 años en la región)\n"
     f"- Pasto sintético con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}\n"),
    ("public/llms.txt", "México (frente a Walmart). Google Maps:", "México (frente a Walmart, entrando por Banamex). Google Maps:"),
    ("public/llms.txt", "- Horario: Lunes–Viernes 9am–6pm, Sábado 9am–2pm\n",
     f"- Horario: Lunes–Viernes 9am–6pm, Sábado 9am–2pm\n- Respuesta por WhatsApp: {EN_1_HORA}\n"
     "- Perfiles oficiales: " + " · ".join(url for _, url in datos.REDES) + f" · {datos.MAPS_URL}\n"),
    ("public/llms.txt", "- [Blog](https://www.viverosterra.com/blog): guías de jardinería para el clima de Tampico\n",
     "- [Precios](https://www.viverosterra.com/precios): lista de precios vigente de pasto, diseño, mantenimiento, riego y "
     "pasto sintético, con IVA\n- [Vivero en Tampico](https://www.viverosterra.com/vivero-tampico): dirección, horario y "
     "cómo llegar\n- [Blog](https://www.viverosterra.com/blog): guías de jardinería para el clima de Tampico\n"),
    ("public/llms.txt", "sin garantía de arraigo.\n\n- ¿Cuánto cuesta", "sin garantía de arraigo.\n- ¿Cuánto cuesta"),
    ("public/llms.txt", "- ¿Hacen entregas a domicilio? Sí, en Tampico, Madero y Altamira; mayoreo a toda la Huasteca.\n",
     "- ¿Hacen entregas a domicilio? Sí, en Tampico, Madero y Altamira; mayoreo a toda la Huasteca.\n\n"
     "## Lo que no hacemos\n- No ofrecemos muestras físicas del pasto sintético: se elige con fichas técnicas y fotos.\n"
     "- No enviamos pasto natural fuera de la región (Tampico, Madero, Altamira y la Huasteca).\n"
     "- No publicamos fechas de corte ni disponibilidad semanal.\n"),
)

ELEMENTOS = (
    ("public/index.html", r'<div id="urgencia-banner"'),
    ("public/pasto-en-rollo-tampico/index.html", r'<div class="disponibilidad-bar\b'),
    ("public/blog/index.html", r'<span class="tag-hot">'),
)


def corregir_texto(texto):
    """Aplica las reglas globales (domicilio, promesa, perfiles, flamboyán)."""
    for viejo, nuevo in GLOBALES:
        texto = texto.replace(viejo, nuevo)
    for patron, reemplazo in REGLAS:
        texto = patron.sub(reemplazo, texto)
    return texto


def quitar_elementos(texto, patron):
    """Quita todos los elementos que abren con `patron`, con su sangría y su salto de línea."""
    while True:
        m = re.search(patron, texto)
        if not m:
            return texto
        inicio, fin = m.start(), fin_elemento(texto, m.start())
        while inicio > 0 and texto[inicio - 1] in " \t":
            inicio -= 1
        if (inicio == 0 or texto[inicio - 1] == "\n") and texto[fin:fin + 1] == "\n":
            fin += 1
        texto = texto[:inicio] + texto[fin:]


def reemplazar(texto, viejo, nuevo, rel):
    """Reemplaza `viejo` por `nuevo`; si ya está corregido no hace nada; si no encuentra ninguno de los dos, falla.

    Cuando `nuevo` contiene a `viejo` (agrega texto después de una línea), "ya corregido" quiere decir que `nuevo` ya está.
    """
    ya_insertado = viejo in nuevo and nuevo in texto
    if viejo in texto and not ya_insertado:
        return texto.replace(viejo, nuevo)
    if not nuevo or nuevo in texto:
        return texto
    raise SystemExit(f"{rel}: no encontré el texto a corregir ni su corrección: {viejo[:80]}")


def archivos_globales():
    yield from sorted(PUBLIC.rglob("*.html"))
    yield PUBLIC / "llms.txt"
    yield from sorted((RAIZ / "tools" / "pasto").glob("*.py"))
    yield from sorted((RAIZ / "tools" / "servicios").glob("*.py"))


def _escribir_si_cambia(path, nuevo, cambiados):
    if nuevo != path.read_text(encoding="utf-8"):
        path.write_text(nuevo, encoding="utf-8")
        cambiados.add(path)


def main():
    cambiados = set()
    for path in archivos_globales():
        _escribir_si_cambia(path, corregir_texto(path.read_text(encoding="utf-8")), cambiados)
    for rel, viejo, nuevo in POR_ARCHIVO:
        path = RAIZ / rel
        _escribir_si_cambia(path, reemplazar(path.read_text(encoding="utf-8"), viejo, nuevo, rel), cambiados)
    for rel, patron in ELEMENTOS:
        path = RAIZ / rel
        _escribir_si_cambia(path, quitar_elementos(path.read_text(encoding="utf-8"), patron), cambiados)
    print(f"{len(cambiados)} archivos corregidos")


if __name__ == "__main__":
    main()
