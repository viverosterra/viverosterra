"""Paridad de lo que paridad.py no ve en las páginas utilitarias (Etapa 2i): fotos del <main> en orden, anclas (id de
h2 y section), campos de formulario (el dueño recibe esos nombres y valores por correo; datos-envio arma con esos id el
mensaje de WhatsApp) y la medición de /gracias (GA4 la cuenta por su URL y su page_view: no hay evento propio).

Uso: python3 tools/site/paridad_util.py capturar   (escribe tests/paridad/utilitarias-contrato.json)
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paridad  # noqa: E402
import paridad_materiales  # noqa: E402

RUTAS = ("/politicas", "/politica-privacidad", "/gracias", "/cuestionario", "/datos-envio",
         "/protocolo-cuidados-pasto-san-agustin", "/vivero-tampico")
CAPTURA = paridad.CAPTURAS / "utilitarias-contrato.json"
ANCLA_RE = re.compile(r'<(?:h2|section)\b[^>]*\sid="([^"]+)"')
FORM_RE = re.compile(r'<form\b[^>]*\baction="([^"]*)"[^>]*\bmethod="([^"]*)"')
GTAG_CONFIG = "gtag('config','"


class _Campos(HTMLParser):
    """Controles del documento en orden: [etiqueta, id, name, type, value, required] y el texto de cada <option>."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.campos, self._opcion = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("input", "select", "textarea"):
            self.campos.append([tag, a.get("id"), a.get("name"), a.get("type"), a.get("value"), "required" in a])
        elif tag == "option":
            self._opcion = [a.get("value"), ""]
            self.campos.append(["option", self._opcion])

    def handle_data(self, data):
        if self._opcion is not None:
            self._opcion[1] += data

    def handle_endtag(self, tag):
        if tag == "option":
            self._opcion[1] = self._opcion[1].strip()
            self._opcion = None


def campos(html):
    p = _Campos()
    p.feed(paridad.principal(html))
    return p.campos


def anclas(html):
    return sorted(set(ANCLA_RE.findall(paridad.principal(html))))


def medicion(html):
    return {"gtag_config": html.count(GTAG_CONFIG), "gtag_event": html.count("gtag('event'"),
            "data_cta": sorted(set(re.findall(r'data-cta="(utilidad:[a-z]+)"', paridad.principal(html))))}


def extraer(ruta, public=paridad.paginas.PUBLIC):
    html = paridad.archivo(ruta, public).read_text(encoding="utf-8")
    m = FORM_RE.search(paridad.principal(html))
    return {"fotos": paridad_materiales.fotos(html), "anclas": anclas(html), "campos": campos(html),
            "form": list(m.groups()) if m else None, "medicion": medicion(html)}


def capturar(destino=CAPTURA):
    datos = {ruta: extraer(ruta) for ruta in RUTAS}
    Path(destino).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return datos


if __name__ == "__main__":
    if sys.argv[1:] != ["capturar"]:
        raise SystemExit("Uso: python3 tools/site/paridad_util.py capturar")
    for ruta, d in capturar().items():
        print(ruta, len(d["fotos"]), len(d["anclas"]), len(d["campos"]), d["form"], d["medicion"])
