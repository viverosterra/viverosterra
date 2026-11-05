"""Línea de mensualidades con tarjeta debajo del precio de cada tarjeta del Plan Terra (diseño de jardines).

Usa el plazo más largo disponible para cada precio (tools/pasto/mensualidades.py). Las líneas llevan la
clase plan-pay: si ya existen se reemplazan, así que correrlo varias veces deja una sola por tarjeta.

Uso: python3 tools/servicios/planes_diseno.py   (desde cualquier carpeta)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pasto"))

import mensualidades  # noqa: E402

PAGE = Path(__file__).resolve().parents[2] / "public" / "diseno-jardines-tampico" / "index.html"
PRECIOS = (3000, 6500, 18000)  # Esencial, Completo, Premium (desde)
PAY_RE = r'\s*<p class="plan-pay[^"]*">[^<]*</p>'


def money(n):
    return f"${n:,.0f}"


def linea(contado):
    disponibles = [p for p in mensualidades.planes(contado) if p["disponible"]]
    if not disponibles:
        raise ValueError(f"{contado}: no hay plazos disponibles")
    p = disponibles[-1]
    return (f'<p class="plan-pay text-gray-600 text-xs font-medium mt-2">o en {p["plazo"]} mensualidades de '
            f'≈ {money(p["mensualidad"])} con tarjeta (total {money(p["total"])})</p>')


def price_re(contado):
    # el precio grande de la tarjeta, su "MXN" y el cierre del renglón; luego la línea plan-pay si ya existe
    return re.compile(
        r'(<span class="text-4xl font-display font-bold text-primary">' + re.escape(money(contado))
        + r'</span>\s*<span class="text-gray-400 text-sm">MXN</span>\s*</div>)(?:' + PAY_RE + r')?')


def apply_html(html):
    for contado in PRECIOS:
        rx = price_re(contado)
        found = rx.findall(html)
        if len(found) != 1:
            raise ValueError(f"{money(contado)}: esperaba 1 tarjeta de precio, encontré {len(found)}")
        html = rx.sub(lambda m, c=contado: m.group(1) + "\n          " + linea(c), html, count=1)
    return html


def main():
    html = PAGE.read_text(encoding="utf-8")
    PAGE.write_text(apply_html(html), encoding="utf-8")
    print("ok diseno-jardines-tampico (planes)")


if __name__ == "__main__":
    main()
