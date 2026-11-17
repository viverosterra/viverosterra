"""Piezas de /pasto-sintetico/cuantos-rollos (Entrega B del SEO nacional, 2026-11-16): la calculadora de medidas
(public/js/vt-rollos.js), la tabla de medidas comunes y la de envío por estado. El cálculo es tools/pasto/rollos.py;
precios, zonas y fletes, tools/pasto/data.py. Todo sale ya calculado en el HTML: sin JavaScript se lee completo."""
from collections import defaultdict

import componentes as c
import data
import rollos
from ciudades import CIUDADES
from partials import esc

EJEMPLO = (7, 5)
SVG_ANCHO, SVG_ALTO = 320, 180


def num(v):
    """4.3 → «4.3», 20 → «20», 1200 → «1,200» (como toLocaleString('es-MX') del JS)."""
    return f"{v:,.2f}".rstrip("0").rstrip(".")


def _plural(n, uno, varios):
    return f"{num(n)} {uno if n == 1 else varios}"


def tiras_texto(r):
    return f'{_plural(r["tiras"], "tira", "tiras")} de {num(r["largo_tira"])} m'


def rollos_texto(r):
    return _plural(r["rollos"], "rollo", "rollos")


def avisos(r):
    """Las mismas notas que pinta vt-rollos.js bajo el resultado."""
    salida = []
    if r["rollos"] > r["rollos_sin_margen"]:
        salida.append(f'El margen de 10% te pasa a {rollos_texto(r)} de envío: si cortas con cuidado, '
                      f'{num(r["m2_sin_margen"])} m² caben en {_plural(r["rollos_sin_margen"], "rollo", "rollos")}.')
    if r["tira_con_union"]:
        salida.append(f"Cada tira mide más de {rollos.ROLLO_LARGO_M} m, el largo del rollo: lleva una unión a lo ancho.")
    if r["m2"] < data.MIN_NACIONAL_M2:
        salida.append(f"Para envío el mínimo es {data.MIN_NACIONAL_M2} m²; abajo de eso, se recoge en el showroom de "
                      "Cd. Madero.")
    return " ".join(salida)


def _rect(x, y, w, h, clase):
    return f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" class="{clase}"/>'


def plano(r):
    """Croquis inicial (el mismo que dibuja vt-rollos.js): tiras a lo largo y el contorno del espacio encima."""
    total = r["tiras"] * rollos.ROLLO_ANCHO_M
    s = min((SVG_ANCHO - 8) / r["largo_tira"], (SVG_ALTO - 8) / total)
    piezas = []
    for i in range(r["tiras"]):
        y = i * rollos.ROLLO_ANCHO_M
        dentro = min(rollos.ROLLO_ANCHO_M, r["cruzado"] - y)
        piezas.append(_rect(0, y, r["largo_tira"], dentro, f"vt-rollos__tira vt-rollos__tira--{i % 2}"))
        if dentro < rollos.ROLLO_ANCHO_M:
            piezas.append(_rect(0, y + dentro, r["largo_tira"], rollos.ROLLO_ANCHO_M - dentro, "vt-rollos__sobra"))
    piezas.append(_rect(0, 0, r["largo_tira"], r["cruzado"], "vt-rollos__espacio"))
    alto = -(-(total * s + 8) // 1)
    dx = round((SVG_ANCHO - r["largo_tira"] * s) / 2, 2)
    return (f'<svg data-r-plano viewBox="0 0 {SVG_ANCHO} {int(alto)}" role="img" aria-label="Croquis de las tiras de '
            f'pasto sobre tu espacio"><g transform="translate({num(dx)} 4) scale({round(s, 4)})">{"".join(piezas)}</g></svg>')


def _campo(id_, etiqueta, valor):
    return (f'<div class="vt-campo"><label for="{id_}">{etiqueta}</label><div class="vt-control"><input id="{id_}" '
            f'type="number" inputmode="decimal" min="0.5" max="200" step="0.1" value="{num(valor)}" required></div></div>')


def calculadora(largo=EJEMPLO[0], ancho=EJEMPLO[1]):
    r = rollos.corte(largo, ancho)
    filas = (("Pide", "m2", f'{num(r["m2"])} m²', " vt-rollos__clave"),
             ("Área de tu espacio", "area", f'{num(r["area"])} m²', ""),
             ("Corte", "tiras", tiras_texto(r), ""),
             ("Envío", "rollos", rollos_texto(r), ""),
             ("Sobrante", "sobrante", f'{num(r["sobrante"])} m²', ""))
    res = "".join(f'<div class="vt-rollos__dato{clase}"><dt>{t}</dt><dd data-r="{k}">{v}</dd></div>'
                  for t, k, v, clase in filas)
    return (f'<form class="vt-rollos" id="r-calc" data-valido="true" novalidate><div class="vt-rollos__campos">'
            f'{_campo("r-largo", "Largo en metros", largo)}{_campo("r-ancho", "Ancho en metros", ancho)}</div>'
            f'<dl class="vt-rollos__res" aria-live="polite">{res}</dl>'
            f'<p class="vt-rollos__nota" data-r-nota>{esc(avisos(r))}</p>'
            f'<figure class="vt-rollos__plano">{plano(r)}<figcaption>Tiras de {rollos.ROLLO_ANCHO_M} m de ancho, todas '
            'con la fibra en el mismo sentido. Lo claro es lo que se recorta de la última tira.</figcaption></figure>'
            '<button class="vt-btn vt-btn--linea" type="submit">Ver el precio de estos m²</button></form>')


def tabla_medidas():
    filas = tuple((f'{num(f["largo"])} × {num(f["ancho"])} m', f'{num(f["area"])} m²', f'<b>{num(f["m2"])} m²</b>',
                   tiras_texto(f), rollos_texto(f)) for f in rollos.tabla_medidas())
    return c.tabla_comparativa(("Espacio", "Área", "Pide", "Corte", "Envío"), filas,
                               "Metros cuadrados a pedir con tiras de 2 m y 10% para cortes. El envío se cobra por "
                               "rollo de 50 m².")


def _ciudades_por_estado():
    salida = defaultdict(list)
    for x in CIUDADES:
        salida[x["estado"]].append(x)
    return salida


def tabla_estados(m):
    """Los 32 estados: flete por rollo y precio puesto por m² con el modelo m (rollo completo + flete de 1 rollo), con
    enlace a la página de envío de sus ciudades."""
    ciudades = _ciudades_por_estado()
    filas = []
    for estado in data.ESTADOS_ORDEN:
        zona = data.zona_de(estado)
        enlaces = ", ".join(f'<a href="/pasto-sintetico/envio/{x["slug"]}">{esc(x["nombre"])}</a>' for x in ciudades[estado])
        nombre = esc(estado) + (f"<br><small>{enlaces}</small>" if enlaces else "")
        filas.append((nombre, f"<b>{c.dinero(data.ZONAS[zona])}</b>", f"${data.landed_m2(m, zona)}/m²",
                      f"{zona} · {esc(data.ZONA_ESTADOS[zona][0])}"))
    return c.tabla_comparativa(("Estado", "Flete por rollo", "Puesto desde", "Zona"), tuple(filas),
                               f"Flete por rollo de {data.ROLLO_M2} m², con IVA. Precio puesto con {esc(m['nombre'])} en "
                               "rollo completo.")
