"""Plantilla del hub de la tienda (/pasto-sintetico): portada con el precio puesto por estado y la foto principal
precargada → cuadro de datos → catálogo con filtros y Agregar → selector "¿cuál te conviene?" → comparador de otra
oferta → cotizador con envío y tabla de fletes → ciudades → comparativa de los 9 → obras con pies FIG. → cómo comprar
(TÚ / NOSOTROS / JUNTOS) → instálalo tú → preguntas → CTA final (Tampico). Contenido: tools/site/contenido/tienda.py.
JS: tienda-pasto.js (cotizador y lista), tienda-hub.js (filtros, selector, precio puesto, comparador), vt-landed.js."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js", "/js/tienda-hub.js")


def _portada(k):
    p = k["portada"]
    precio = (f'<p class="vt-precio-puesto" data-landed-hero data-rollo="{p["rollo"]}" aria-live="polite"><span>Desde'
              f'</span><b data-landed-value>${p["rollo"]}</b><span>/m²</span><small data-landed-note>{p["nota_precio"]}'
              '</small></p>')
    copia = (f'<div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1>'
             f'<p class="vt-existencia"><span>{p["existencia"]}</span></p><p class="vt-lede">{p["rotulo_estado"]}</p>'
             f'{t.selector_estado("hero-estado")}{precio}<p class="vt-promesa">{p["mensualidades"]}</p>'
             f'{c.fila_cta(p["mensaje"], k["tipo"], "hero", hero=True)}'
             f'<p class="vt-enlace-sec"><a href="#modelos">{p["texto_modelos"]}</a></p></div>')
    return (f'<section class="vt-portada vt-portada-t" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-portada__grid">{copia}<div class="vt-portada__foto">{c.figura(p["foto"], principal=True)}'
            f'</div></div>{c.cuadro_datos(p["datos"])}</div></section>')


def _cotizador(k):
    q = k["cotizador"]
    calculo = "".join(f"<li><span>{x}</span></li>" for x in q["calculo"])
    cuerpo = (f'<div class="vt-dos">{t.cotizador(k["default"], modelos=t.data.MODELOS, titulo=q["titulo_cotizador"], nivel=3, tipo=k["tipo"])}'
              f'<div><h3>{q["titulo_calculo"]}</h3><ul class="vt-checks vt-mt-s">{calculo}</ul></div></div>'
              f'<h3 class="vt-mt" id="envio">{q["titulo_envio"]}</h3><p class="vt-lede">{q["lede_envio"]}</p>'
              f'{t.tabla_envio()}<p class="vt-promesa">{q["nota_envio"]}</p>')
    return c.bloque(4, "Cotizador", "vt-h-cotizador", q["titulo"], cuerpo, tinte=True, id_seccion="cotizador")


def render(k):
    mo, el, co, ci, cp, ob, pe, ins, f, cie, b = (k[s] for s in ("modelos", "elegir", "comparar", "ciudades",
                                                                 "comparativa", "obras", "pedido", "instalar", "faq",
                                                                 "cierre", "barra"))
    secciones = (
        _portada(k),
        c.bloque(1, "Colección", "vt-h-modelos", mo["titulo"], t.catalogo(), lede=mo["lede"], id_seccion="modelos"),
        c.bloque(2, "Elegir", "vt-h-elegir", el["titulo"], t.selector_modelo(), tinte=True, id_seccion="elegir"),
        c.bloque(3, "Comparar", "vt-h-comparar", co["titulo"], t.comparador(), lede=co["lede"], id_seccion="comparar"),
        _cotizador(k),
        c.bloque(5, "Ciudades", "vt-h-ciudades", ci["titulo"],
                 t.ciudades_destacadas(ci["items"]) + f'<p class="vt-promesa">{ci["perros"]}</p>', lede=ci["lede"],
                 id_seccion="ciudades"),
        c.bloque(6, "Comparativa", "vt-h-comparativa", cp["titulo"],
                 t.tabla_modelos() + f'<p class="vt-promesa">{cp["nota"]}</p>', tinte=True, id_seccion="comparativa"),
        c.bloque(7, "Obras", "vt-h-obras", ob["titulo"], c.obras(ob["figuras"], c.nota(*ob["nota"])), id_seccion="obras"),
        c.bloque(8, "Tu pedido", "vt-h-pedido", pe["titulo"], c.pasos(pe["pasos"]), tinte=True,
                 id_seccion="como-funciona"),
        c.bloque(9, "Instálalo tú", "vt-h-diy", ins["titulo"], c.pasos(ins["pasos"]) +
                 f'<p class="vt-promesa">{ins["guia"]}</p>', lede=ins["lede"], id_seccion="instalacion"),
        c.bloque_dos(10, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True,
                     id_seccion="preguntas"),
        c.cierre(cie["titulo"], cie["lede"], cie["mensaje"], k["tipo"]),
    )
    grafo = [k["jsonld"][0], c.faq_jsonld(f["preguntas"]), k["jsonld"][1]]
    fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], cie["mensaje"], rollo=b["rollo"])
    return base.documento(k["meta"], t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(completo=True),), tras_main=fuera, scripts=SCRIPTS,
                          clase_body="vt-pagina vt-tienda")
