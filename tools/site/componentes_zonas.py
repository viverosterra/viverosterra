"""Componentes de las 6 zonas y de /precios (Etapa 2g): lista de precios con columna Unidad (precio fijo, "desde",
rango o "según cotización", siempre de datos.py), colonias atendidas, pasto sintético por modelo (tools/pasto/data.py) y
mensualidades por plazo (tools/pasto/mensualidades.py, la misma fórmula de public/js/vt-mensualidades.js: aquí no se
reimplementa, solo se llama). Funciones puras, como componentes.py (que ya pasa de 800 renglones).
"""
import componentes as c
import data
import datos
import mensualidades
from partials import esc

SEGUN = datos.SEGUN_COTIZACION
MUESTRA = 100_000  # contado de referencia para escribir el total a plazos como porcentaje (la tabla de main)


def precio_texto(valor, desde=False):
    """"$85", "desde $120", "$180 a $320" (un par de datos.PRECIOS) o "Según cotización" (None: no se inventa)."""
    if valor is None:
        return SEGUN
    if isinstance(valor, tuple):
        return f"{c.dinero(valor[0])} a {c.dinero(valor[1])}"
    return f"{'desde ' if desde else ''}{c.dinero(valor)}"


def _celda(f):
    valor = f["precio"]
    if valor is None:
        return f'<td class="vt-tabla__p vt-tabla__p--cotiza">{SEGUN}</td>'
    desde = "<small>desde</small>" if f.get("desde") else ""
    cotiza = f"<small>{SEGUN.lower()}</small>" if f.get("cotiza") else ""
    return f'<td class="vt-tabla__p">{desde}{precio_texto(valor)}{cotiza}</td>'


def lista(filas, caption, concepto="Servicio"):
    """Tabla Concepto | Unidad | Precio. filas: nombre, detalle, unidad, precio (número o par de datos.PRECIOS, o None)
    y, opcionales, desde, cotiza (además del "desde", "según cotización" debajo: la poda) y href (el nombre enlaza)."""
    cuerpo = []
    for f in filas:
        nombre = f'<a href="{esc(f["href"])}">{f["nombre"]}</a>' if f.get("href") else f["nombre"]
        cuerpo.append(f'<tr><th scope="row"><b>{nombre}</b><span>{f["detalle"]}</span></th>'
                      f'<td class="vt-tabla__u">{f["unidad"]}</td>{_celda(f)}</tr>')
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            f'<th scope="col">{concepto}</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{"".join(cuerpo)}</tbody></table>')


def colonias(items, municipio, caption):
    """Colonias que se atienden con su código postal (verificados con SEPOMEX, tools/site/contenido/zona.py)."""
    filas = tuple((f"{nombre}<br><small>{municipio}</small>", cp) for nombre, cp in items)
    return c.tabla_comparativa(("Colonia", "Código postal"), filas, caption)


def tabla_sintetico(modelos=None):
    """Precio por m² de cada modelo según cuánto compras (tools/pasto/data.py: t1, t2 y rollo)."""
    filas = "".join(
        f'<tr><th scope="row"><a href="/pasto-sintetico/{esc(m["slug"])}">{esc(m["nombre"])}</a><span>{m["mm"]} mm</span>'
        f'</th><td>{c.dinero(m["t1"])}</td><td>{c.dinero(m["t2"])}</td><td><b>{c.dinero(m["rollo"])}</b></td></tr>'
        for m in modelos or data.MODELOS)
    return ('<table class="vt-tabla vt-tabla--compacta"><caption>Precio por m² con IVA según cuánto compras.</caption>'
            f'<thead><tr><th scope="col">Modelo</th><th scope="col">{c.unidades("2 a 9 m²")}</th>'
            f'<th scope="col">{c.unidades("10 a 49 m²")}</th><th scope="col">{c.unidades("Rollo 50 m²")}</th></tr></thead>'
            f'<tbody>{filas}</tbody></table>')


def porcentaje_plazo(plazo):
    """Cuánto más es el total a plazos que el contado, en %, con la fórmula oficial (10.5 en 3 mensualidades)."""
    return round((mensualidades.total_a_plazos(MUESTRA, plazo) / MUESTRA - 1) * 100, 1)


def tabla_mensualidades():
    """Plazo | Desde (contado) | Total frente a contado: los montos mínimos y la fórmula de tools/pasto/mensualidades.py."""
    filas = "".join(f'<tr><th scope="row">{p} mensualidades</th><td>{c.dinero(mensualidades.minimo_de(p))}</td>'
                    f'<td><b>+{porcentaje_plazo(p):.1f}%</b></td></tr>' for p in mensualidades.PLAZOS)
    return ('<table class="vt-tabla vt-tabla--compacta"><caption>Mensualidades con tarjeta de crédito: monto mínimo de '
            'contado por plazo y cuánto más es el total a plazos.</caption><thead><tr><th scope="col">Plazo</th>'
            '<th scope="col">Desde (contado)</th><th scope="col">Total frente a contado</th></tr></thead>'
            f'<tbody>{filas}</tbody></table>')


def garantias(items):
    """Garantías con su ancla estable (#garantia-pasto, #garantia-plantas). items: id, titulo, texto, enlace (texto,
    href)."""
    filas = "".join(f'<li class="vt-modo" id="{esc(g["id"])}"><h3>{g["titulo"]}</h3><p>{g["texto"]}</p>'
                    f'<p class="vt-promesa"><a href="{esc(g["enlace"][1])}">{g["enlace"][0]}</a></p></li>' for g in items)
    return f'<ul class="vt-modos vt-fichas">{filas}</ul>'
