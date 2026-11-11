"""Plantilla de ficha de tienda (spec §3.3): ruta visible → nombre, "En existencia" y etiqueta "desde $X/m² · rollo
50 m² · envío por rollo según estado" en el primer pantallazo → galería (foto principal precargada, nunca lazy) →
cotizador (estado, m², precio puesto, mensualidades) → para quién es → ficha técnica → fotos y rollo a escala →
comparativa con 2 vecinos → envío por rollo y cómo comprar → garantía del modelo → preguntas → CTA final.
Contenido: tools/site/contenido/ficha.py (desde tools/pasto/data.py). JS: tienda-pasto.js, vt-landed.js."""
import componentes as c
import datos
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js")


def _portada(k):
    """Cabecera de la ficha con el hero de marca: nombre, lema, etiqueta de precio y un solo botón de WhatsApp (en
    celular todo antes de la galería: antes el hero no tenía CTA); la existencia, la entrada, los datos y la línea de
    confianza van después de la foto."""
    m, tipo = k["modelo"], k["tipo"]
    info = (f'<div class="{c.clase_titular(k["h1"], "vt-ficha__info")}"><p class="vt-kicker">{k["kicker"]}</p>'
            f'<h1 id="vt-h1">{k["h1"]}</h1><p class="vt-portada__lema vt-serif">{k["lema"]}</p>'
            f'{c.etiqueta(k["etiqueta"], cordel=False)}'
            # Reescritura 12 (Entrega B de experiencia): el botón dice qué modelo se cotiza ("por WhatsApp" no cabe a 320 px
            # en el botón alto del hero sin partirse en dos renglones).
            f'<div class="vt-portada__cta" data-hero-cta>{c.boton_wa(k["cierre"]["mensaje"], f"{tipo}:hero", "Cotizar " + c.esc(m["nombre"]))}</div>'
            f'{c.enlaces_portada((("Calcula tu pedido", "#comprar"),), tipo)}</div>')
    mas = (f'<div class="vt-ficha__mas">{t.existencia(m)}<p class="vt-lede">{k["lede"]}</p>{t.datos_modelo(m)}'
           f'{c.confianza()}</div>')
    cotizador = t.cotizador(m, titulo=f"Precio y cotización del {m['nombre']}", tipo=tipo)
    return (f'<section class="vt-ficha" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-ficha__grid">{info}{t.galeria(m)}{mas}{cotizador}</div></div></section>')


def _para_quien(k, n):
    p = k["para_quien"]
    checks = "".join(f"<li><span>{x}</span></li>" for x in p["si"]) + "".join(f'<li class="vt-checks__no"><span>{x}</span></li>' for x in p["no"])
    izquierda = f'<p class="vt-lede">{p["resumen"]}</p>{c.nota(*p["nota"])}'
    return c.bloque_dos(n, "En resumen", "vt-h-resumen", p["titulo"], izquierda,
                        f'<ul class="vt-checks">{checks}</ul>' + _fila(k, "resumen", prueba=True))


def _fotos(k, n):
    f = k["fotos"]
    cuerpo = f'<div class="vt-obras">{"".join(c.figura(x) for x in f["figuras"])}</div>{t.rollo_escala()}'
    return c.bloque(n, f["rotulo"], "vt-h-fotos", f["titulo"], cuerpo)


def _pedido(k, n):
    p = k["pedido"]
    cuerpo = (f'<h3>{p["titulo_envio"]}</h3><p class="vt-lede">{p["lede"]}</p>{t.zonas_envio()}'
              f'{c.pasos(p["pasos"])}')
    return c.bloque(n, "Tu pedido", "vt-h-pedido", p["titulo"], cuerpo + _fila(k, "pedido"), id_seccion="como-funciona")


def _fila(k, seccion, prueba=False):
    """Entrega B de experiencia: WhatsApp en los tramos largos de la ficha (antes, 11.7 pantallas sin CTA), con lo que
    el cliente ya eligió (tienda-pasto.js) y, tras el resumen, la prueba social de la tienda."""
    fila = c.fila_seccion(k["cierre"]["mensaje"], k["tipo"], seccion, f"Cotizar {c.esc(k['modelo']['nombre'])}", contexto=True)
    if not prueba:
        return fila
    return fila + c.prueba_cta(datos.OPINION_SINTETICO_TAMPICO, f"vendemos a todo México desde {datos.SINTETICO_NACIONAL_DESDE}")


def render(k):
    m, f, ci, b = k["modelo"], k["faq"], k["cierre"], k["barra"]
    secciones = (
        _portada(k),
        _para_quien(k, 1),
        c.bloque(2, "Ficha técnica", "vt-h-ficha", k["ficha"]["titulo"], t.ficha_tecnica(m) + _fila(k, "ficha-tecnica"),
                 tinte=True, id_seccion="ficha-tecnica"),
        _fotos(k, 3),
        c.bloque(4, "Compáralo", "vt-h-compara", k["compara"]["titulo"], t.comparativa(m) + _fila(k, "compara"),
                 lede=k["compara"]["lede"], tinte=True),
        _pedido(k, 5),
        # Plan visual V2: la garantía de fábrica es el momento oscuro, con su CTA.
        c.garantia(dict(k["garantia"], numero=6, id_titulo="vt-h-garantia", rotulo="Garantía", banda=True,
                        cta_html=_fila(k, "garantia"))),
        c.bloque_dos(7, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"])),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]),
    )
    grafo = list(k["jsonld"]) + [c.faq_jsonld(f["preguntas"])]
    fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], ci["mensaje"], rollo=b["rollo"])
    return base.documento(base.meta_de(k), t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(t.foto_principal(m)),),
                          head_extra=(t.json_modelo(m), t.SCRIPT_PRECIO_PUESTO), tras_main=fuera, scripts=SCRIPTS,
                          clase_body="vt-pagina vt-tienda")
