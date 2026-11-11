"""Plantilla del hub de la tienda (/pasto-sintetico): portada con el precio puesto por estado y la foto principal
precargada → cuadro de datos → catálogo con filtros y Agregar → selector "¿cuál te conviene?" → comparador de otra
oferta → cotizador con envío y tabla de fletes → ciudades → comparativa de los 9 → obras con pies FIG. → cómo comprar
(TÚ / NOSOTROS / JUNTOS) → instálalo tú → preguntas → CTA final (Tampico). Contenido: tools/site/contenido/tienda.py.
JS: tienda-pasto.js (cotizador y lista), tienda-hub.js (filtros, selector, precio puesto, comparador), vt-landed.js."""
import componentes as c
import datos
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js", "/js/tienda-hub.js")


def _etiqueta_puesta(p):
    """Etiqueta de precio del hub: el precio puesto cambia con el estado elegido (tienda-hub.js escribe en
    data-landed-value y data-landed-note). Sin JS dice el precio del rollo y que el envío va aparte."""
    return ('<div class="vt-etiqueta-x vt-etiqueta-x--cordel">'
            f'<div class="vt-etiqueta" data-landed-hero data-rollo="{p["rollo"]}" aria-live="polite">'
            f'<p class="vt-etiqueta__cod"><span>{p["codigo"]}</span><span>Con IVA</span></p>'
            f'<p class="vt-etiqueta__nombre">{p["rotulo_estado"]}</p>'
            f'<p class="vt-etiqueta__precio"><small>{c.unidades("Rollo de 50 m² · desde")}</small><b data-landed-value>${p["rollo"]}</b>'
            f'<span>/m²</span></p><p class="vt-etiqueta__fila"><span data-landed-note>{p["nota_precio"]}</span></p></div></div>')


def _portada(k):
    """El hero de marca común: el selector de estado va bajo el lede y el precio puesto, en la etiqueta colgada."""
    p = k["portada"]
    portada = dict(p, lede=p["existencia"], medio=t.selector_estado("hero-estado"), etiqueta_html=_etiqueta_puesta(p),
                   enlaces=((p["texto_modelos"], "#modelos"), ("Mensualidades con tarjeta", "#cotizador")))
    return c.portada(portada, k["tipo"], k["migas"], datos_html=c.cuadro_datos(p["datos"]), clase="vt-portada-t vt-portada-hub")


def _cotizador(k):
    q = k["cotizador"]
    calculo = "".join(f"<li><span>{x}</span></li>" for x in q["calculo"])
    # Junto al CTA del cotizador, la prueba social de la tienda (Entrega B de experiencia): opinión real de pasto sintético
    # y calificación de Google con el enlace a las reseñas.
    prueba = c.prueba_cta(datos.OPINION_SINTETICO_TAMPICO, f"vendemos a todo México desde {datos.SINTETICO_NACIONAL_DESDE}")
    cuerpo = (f'<div class="vt-dos">{t.cotizador(k["default"], modelos=t.data.MODELOS, titulo=q["titulo_cotizador"], nivel=3, tipo=k["tipo"])}'
              f'<div><h3>{q["titulo_calculo"]}</h3><ul class="vt-checks vt-mt-s">{calculo}</ul>{prueba}</div></div>'
              f'<h3 class="vt-mt" id="envio">{q["titulo_envio"]}</h3><p class="vt-lede">{q["lede_envio"]}</p>'
              f'{t.zonas_acordeon()}<p class="vt-promesa">{q["nota_envio"]}</p>')
    return c.bloque(4, "Cotizador", "vt-h-cotizador", q["titulo"], cuerpo, tinte=True, id_seccion="cotizador")


def _fila(k, seccion, texto):
    """Entrega B de experiencia: WhatsApp en los tramos largos del hub (antes, 12 pantallas sin CTA); tienda-pasto.js le
    pone lo que el cliente ya eligió (estado, cotizador o lista)."""
    return c.fila_seccion(k["cierre"]["mensaje"], k["tipo"], seccion, texto, contexto=True)


def render(k):
    mo, el, co, ci, cp, ob, pe, ins, f, cie, b = (k[s] for s in ("modelos", "elegir", "comparar", "ciudades",
                                                                 "comparativa", "obras", "pedido", "instalar", "faq",
                                                                 "cierre", "barra"))
    secciones = (
        _portada(k),
        c.respuesta(k.get("respuesta")),
        c.bloque(1, "Colección", "vt-h-modelos", mo["titulo"], t.catalogo(), lede=mo["lede"], id_seccion="modelos"),
        c.bloque(2, "Elegir", "vt-h-elegir", el["titulo"], t.selector_modelo() + _fila(k, "quiz", "Pedir mi recomendación"),
                 tinte=True, id_seccion="elegir"),
        c.bloque(3, "Comparar", "vt-h-comparar", co["titulo"], t.comparador(), lede=co["lede"], id_seccion="comparar"),
        _cotizador(k),
        c.bloque(5, "Ciudades", "vt-h-ciudades", ci["titulo"],
                 t.ciudades_destacadas(ci["items"]) + f'<p class="vt-promesa">{ci["perros"]}</p>'
                 + _fila(k, "ciudades", "Cotizar con envío a mi ciudad"), lede=ci["lede"], id_seccion="ciudades"),
        c.bloque(6, "Comparativa", "vt-h-comparativa", cp["titulo"],
                 t.tabla_modelos() + f'<p class="vt-promesa">{cp["nota"]}</p>' + _fila(k, "comparativa", "Cotizar mi modelo"),
                 tinte=True, id_seccion="comparativa"),
        c.bloque(7, "Obras", "vt-h-obras", ob["titulo"], c.obras(ob["figuras"], c.nota(*ob["nota"])), id_seccion="obras"),
        c.momento(c.bloque(8, "Tu pedido", "vt-h-pedido", pe["titulo"], c.pasos(pe["pasos"]) + _fila(k, "pedido", "Empezar mi pedido"),
                           id_seccion="como-funciona")),
        c.bloque(9, "Instálalo tú", "vt-h-diy", ins["titulo"], c.pasos(ins["pasos"]) +
                 f'<p class="vt-promesa">{ins["guia"]}</p>', lede=ins["lede"], id_seccion="instalacion"),
        c.bloque_dos(10, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True,
                     id_seccion="preguntas"),
        c.cierre(cie["titulo"], cie["lede"], cie["mensaje"], k["tipo"]),
    )
    grafo = [k["jsonld"][0], c.faq_jsonld(f["preguntas"]), k["jsonld"][1]]
    fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], cie["mensaje"], rollo=b["rollo"])
    return base.documento(base.meta_de(k), t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(completo=True),), tras_main=fuera, scripts=SCRIPTS,
                          clase_body="vt-pagina vt-tienda")
