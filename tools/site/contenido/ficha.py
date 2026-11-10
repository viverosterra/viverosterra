"""Contenido de las 9 fichas /pasto-sintetico/<modelo>. Solo datos: la plantilla es tools/site/plantillas/ficha.py.

Cada ficha sale de tools/pasto/data.py (MODELOS): aquí no se escribe ningún precio ni dato técnico. Título,
descripción, canonical, Open Graph, Product, BreadcrumbList y preguntas son los que publicaba tools/pasto/ficha.py;
FAQPage sale de las preguntas visibles. PARIDAD: tests/test_paridad.py (captura de cada ficha antes de migrar).
"""
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
from componentes import dinero
from contenido import seo
from esquema import breadcrumb_schema, product_schema

CLAVES = tuple(m["slug"] for m in data.MODELOS)
SITE = data.SITE
INSTALAR = ("Sí. Sobre tierra compactada se fija con clavos cada 20 a 30 cm. Sobre concreto se pega con adhesivo de "
            "contacto. Te mandamos la guía de instalación con el pedido.")
DEVOLVER = ("Sí, dentro de 7 días, nuevo y sin cortar. Los cortes a medida no tienen devolución. El envío de regreso lo "
            "paga el cliente.")
ENTREGA = ("Llega en 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo. El mínimo para envío "
           f"nacional es {data.MIN_NACIONAL_M2} m². En el showroom de Cd. Madero puedes comprar desde "
           f"{data.MIN_SHOWROOM_M2} m².")
PASOS = (
    {"titulo": "Cotiza aquí", "quien": "tu", "cuando": "Hoy",
     "texto": "Pon tus m² y tu estado. Mándanos la cotización por WhatsApp."},
    {"titulo": "Confirmamos el flete", "quien": "nosotros", "cuando": "En menos de 1 hora en horario",
     "texto": "Con tu dirección te damos el precio final. Sin sorpresas."},
    {"titulo": "Pagas y facturamos", "quien": "juntos", "cuando": "Al confirmar",
     "texto": f"Transferencia o link de pago con tarjeta. Factura {datos.FACTURA}."},
    {"titulo": "Recibes en 3 a 5 días", "quien": "nosotros", "cuando": "3 a 5 días hábiles",
     "texto": "Llega por paquetería con guía de rastreo y guía de instalación."},
)


def preguntas(m):
    """Las 7 preguntas que publicaba la ficha, con sus enlaces (pares pregunta, respuesta en HTML en línea)."""
    precio = (f"Cuesta ${m['rollo']}/m² en rollo completo de 50 m², ${m['t2']}/m² de 10 a 49 m² y ${m['t1']}/m² en "
              "cortes de 2 a 9 m² en el showroom de Cd. Madero. Los precios incluyen IVA. El envío se cobra por rollo "
              f"según el estado: de {dinero(min(data.ZONAS.values()))} a {dinero(max(data.ZONAS.values()))}.")
    extra = [list(par) for par in m["faq_extra"]]
    if m["slug"] == "viena-30":
        extra[0][1] = extra[0][1].replace("En el blog explicamos cómo manejar el calor.",
                                          'En el blog explicamos <a href="/blog/pasto-sintetico-calor-mexico">cómo '
                                          "manejar el calor</a>.")
    return (
        (f"¿Cuánto cuesta el pasto sintético {m['nombre']}?", precio),
        tuple(extra[0]),
        (f"¿El {m['nombre']} sirve para perros y niños?", m["mascotas"]),
        ("¿Cuánto tarda en llegar y cuál es el pedido mínimo?", ENTREGA),
        tuple(extra[1]),
        ("¿Lo puedo instalar yo?", f'{INSTALAR} Aquí está la <a href="/blog/como-instalar-pasto-sintetico">guía paso a '
                                   "paso</a>."),
        ("¿Puedo devolverlo?", f'{DEVOLVER} Consulta la <a href="/politicas">política de envíos y devoluciones</a>.'),
    )


def _fotos(m):
    """Foto grande de la sección de fotos (instalado o de cerca) y la del rollo, con pie FIG."""
    instaladas = [(i, cap) for i, k, cap in m["gallery"] if k == "instalado"]
    if instaladas:
        idx, cap = instaladas[0]
        titulo, rotulo = f"{m['nombre']} instalado", "Instalado"
        principal = {"src": f"{t.GAL}/{m['slug']}-{idx}.webp", "alt": f"Pasto sintético {m['nombre']} instalado: "
                     f"{cap.lower()}", "lugar": f"{cap}. {m['nombre']} instalado", "etapa": "Foto de producto"}
    else:
        idx = next(i for i, k, _c in m["gallery"] if k == "textura")
        titulo, rotulo = f"{m['nombre']} de cerca", "De cerca"
        principal = {"src": f"{t.GAL}/{m['slug']}-{idx}.webp", "alt": f"Acercamiento a la fibra del pasto sintético "
                     f"{m['nombre']}", "lugar": "Detalle de la fibra, sin retoque", "etapa": "Foto de producto"}
    figuras = (
        dict(principal, ancho=720, alto=960, numero=1),
        {"src": f"{t.GAL}/{m['slug']}-rollo.webp", "ancho": 564, "alto": 452, "numero": 2,
         "alt": f"Rollo de {m['nombre']} abierto sobre el piso antes de instalar",
         "lugar": "Así llega: rollo de 2 m de ancho", "etapa": "Antes de instalar"},
    )
    return {"titulo": titulo, "rotulo": rotulo, "figuras": figuras}


def titulo_y_descripcion(m):
    """Título y descripción de la ficha (SEO fase 0, 2026-11-10): altura en mm en el título («pasto sintético 10 mm» es
    la consulta), sin plazo de entrega (regla del dueño) y con los datos del modelo de tools/pasto/data.py."""
    gar = f"con garantía de {m['garantia']} años" if m["garantia"] else "para uso decorativo"
    modelo = m["nombre"].rsplit(" ", 1)[0]  # "Aruba 10" → "Aruba": la altura va aparte, con su unidad
    titulo = f"Pasto Sintético {m['nombre']} mm desde ${m['rollo']}/m² | Viveros Terra"
    descripcion = (f"Pasto sintético {modelo} de {m['mm']} mm y {m['peso']} g/m², {gar}. Desde ${m['rollo']}/m² en rollo, "
                   "con factura y envío a todo México. Cotiza tus metros.")
    return titulo, descripcion


def _meta(m, url):
    titulo, descripcion = titulo_y_descripcion(m)
    primera = f"{t.GAL}/{m['slug']}-{m['gallery'][0][0]}"
    return {
        "title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
        "canonical": url,
        "og": (("og:type", "product"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
               ("og:description", descripcion), ("og:image", f"{SITE}{primera}.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    }


def contenido(m):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    insignia = f' <span class="vt-ficha__insignia">{m["badge"]}</span>' if m.get("badge") else ""
    gar = f"Garantía de {m['garantia']} años" if m["garantia"] else "Garantía de fábrica"
    return {
        "tipo": "tienda",
        "modelo": m,
        "meta": _meta(m, url),
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", f"{SITE}/pasto-sintetico"),
                                      (m["nombre"], url)]), product_schema(m)),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (m["nombre"], None)),
        "kicker": f"Pasto sintético · N.º {m['n']:02d} de 09",
        "lema": f"{m['tag']}.",  # el rótulo del modelo (tools/pasto/data.py), antes al final del kicker
        "h1": f'<span class="vt-ficha__pre">Pasto sintético</span> {m["nombre"]}{insignia}',
        "lede": m["lede"],
        "etiqueta": {
            "codigo": f"Sintético · {m['n']:02d}/09", "aviso": "Con IVA", "nombre": m["nombre"],
            "antes": f"Rollo de {data.ROLLO_M2} m² · desde", "monto": dinero(m["rollo"]), "unidad": "/m²",
            "filas": (("Envío", "por rollo, según tu estado"), ("Mínimo nacional", f"{data.MIN_NACIONAL_M2} m²"),
                      ("En showroom", f"desde {data.MIN_SHOWROOM_M2} m²")),
            "nota": f'<span data-landed-slug="{m["slug"]}" aria-live="polite"></span>',
        },
        "para_quien": {"titulo": f"Para quién es el {m['nombre']}", "resumen": m["resumen"],
                       "si": m["fit_si"], "no": m["fit_no"], "nota": (m["mascotas"], "Con niños y mascotas")},
        "ficha": {"titulo": f"Ficha técnica del {m['nombre']}"},
        "fotos": _fotos(m),
        "compara": {"titulo": f"Compara el {m['nombre']} con modelos similares",
                    "lede": "Agrega los que quieras a tu lista: van todos en un solo mensaje de WhatsApp."},
        "pedido": {"titulo": f"Cómo comprar el {m['nombre']}", "titulo_envio": "El envío se cobra por rollo, según tu "
                   "estado.", "lede": (f"Un rollo son {data.ROLLO_M2} m²: si pides 100 m² son dos rollos y dos fletes. "
                                       f"Nunca va escondido en el precio: {t.TARIFAS_TEXTO} por rollo. Con tu código "
                                       "postal te damos el precio final antes de pagar."),
                   "pasos": PASOS},
        "garantia": {
            "titulo": f"{gar} en el {m['nombre']}.", "grande": str(m["garantia"]).replace(" a ", "–") if m["garantia"]
            else "—", "unidad": "años" if m["garantia"] else "", "resumen": "Garantía de fábrica; la gestionamos nosotros.",
            "puntos": (("Garantía de fábrica contra defectos del material, gestionada por nosotros.", True),
                       ("Devolución dentro de 7 días, nuevo y sin cortar.", True),
                       (f"Factura {datos.FACTURA} para persona física o moral.", True),
                       ("Los cortes a medida no tienen devolución; el envío de regreso lo paga el cliente.", False)),
            "pie": ('<a href="/politicas#devoluciones">Política de envíos y devoluciones</a> · '
                    '<a href="/politicas">Políticas y garantías</a>')},
        "faq": {"titulo": f"Preguntas sobre el {m['nombre']}", "preguntas": preguntas(m)},
        "cierre": {"titulo": f"Cotiza tu {m['nombre']} con envío a tu estado",
                   "lede": "Mándanos tus metros y tu estado. Te respondemos con el precio final y la fecha de entrega.",
                   "mensaje": f"Hola, quiero cotizar el pasto sintético {m['nombre']}.\nMi estado: ___\nMetros aprox.: ___"},
        "barra": {"nombre": f"{m['nombre']}{' · ' + m['badge'] if m.get('badge') else ''}",
                  "precio": f"Desde ${m['rollo']}/m²", "rollo": m["rollo"]},
    }


def pagina(slug):
    m = data.BY_SLUG[slug]
    return SimpleNamespace(CONTENIDO=contenido(m), PARIDAD={**PARIDAD, "meta": seo.paridad(*titulo_y_descripcion(m))})


M_VENDEDOR = ("SEO fase 1: el vendedor de cada producto es la entidad única #negocio por @id (antes, una Organization suelta "
              "con nombre, URL y teléfono en cada oferta).")
PARIDAD = {"reemplazos": {}, "retirados": {}, "jsonld": {"Organization": M_VENDEDOR},
           "hero": ("Entrega A de experiencia (2026-11-10), hero de marca: el rótulo del modelo pasa del kicker al lema en "
                    "serif; botón de WhatsApp bajo la etiqueta (antes el hero no tenía CTA en celular) con enlace al "
                    "cotizador y al teléfono; la existencia, la entrada y los datos van después del botón (en celular, "
                    "después de la galería); en celular y pantallas bajas la etiqueta muestra una fila.")}
