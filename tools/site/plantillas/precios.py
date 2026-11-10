"""Plantilla de la lista de precios (spec §3.3): ruta visible → H1 con la respuesta directa, la vigencia y el precio
ancla en la etiqueta, y CTA → índice de secciones (fichas) → una tabla por línea (pasto natural, servicios, pasto sintético por modelo, materiales y
plantas), cada una con columna Unidad y generada de datos.py → mensualidades (plazos, mínimos, total frente a contado,
aviso del banco, anticipo y el simulador de vt-simulador.js) → garantías con anclas estables (#garantia-pasto,
#garantia-plantas) → preguntas → CTA final. Las secciones conservan sus id de main (#pasto, #servicios, #sintetico,
#materiales, #plantas, #mensualidades, #preguntas). Página: /precios (tools/site/contenido/precios.py).
<body class="vt-pagina vt-precios">: el shell agrega terra-precios.css."""
import componentes as c
import componentes_zonas as cz
from plantillas import base

CONTEXTO = "https://schema.org"
CLASE_BODY = "vt-pagina vt-precios"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-simulador.js")


def _seccion(s, numero, tipo):
    cuerpo = cz.tabla_sintetico() if s.get("modelos") else cz.lista(s["filas"], s["caption"], s["concepto"])
    texto, mensaje = s["cotizar"]
    cuerpo += cz.cotizar(texto, mensaje, f"{tipo}:{s['id']}") + f'<p class="vt-promesa">{s["nota"]}</p>'
    return c.bloque(numero, s["rotulo"], f"vt-h-{s['id']}", s["titulo"], cuerpo, lede=s.get("lede"),
                    tinte=numero % 2 == 0, id_seccion=s["id"])


def _pago(p, numero, tipo):
    izquierda = (f'<p class="vt-lede">{p["lede"]}</p>{cz.tabla_mensualidades()}'
                 f'<p class="vt-promesa">{p["nota"]}</p><p class="vt-promesa">{p["anticipo"]}</p>')
    derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], tipo)
    return c.bloque_dos(numero, "Formas de pago", "vt-h-pago", p["titulo"], izquierda, derecha, id_seccion="mensualidades")


def render(k):
    tipo = k["tipo"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), c.respuesta(k.get("respuesta")), cz.saltos(k["saltos"])]
    numero = 0
    for numero, s in enumerate(k["secciones"], 1):
        secciones.append(_seccion(s, numero, tipo))
    g, f, ci = k["garantias"], k["faq"], k["cierre"]
    secciones += [
        _pago(k["pago"], numero + 1, tipo),
        c.bloque(numero + 2, "Garantías", "vt-h-garantias", g["titulo"], cz.garantias(g["items"]), tinte=True,
                 id_seccion="garantias"),
        c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), id_seccion="preguntas"),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo),
    ]
    j = k["jsonld"]
    grafo = [j["migas"], j["pagina"], j["catalogo"], c.faq_jsonld(f["preguntas"])]
    return base.documento(base.meta_de(k), "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS,
                          clase_body=CLASE_BODY)
