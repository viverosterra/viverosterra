"""Plantilla de /vivero-tampico, "Visítanos" (spec §3.5): portada con la foto de producción y la etiqueta → dónde estamos →
categorías → cómo llegar y horario → buscar una planta → preguntas → CTA final. <body class="vt-pagina vt-util">."""
import componentes as c
from plantillas import base

CLASE_BODY = "vt-pagina vt-util"


def _datos(filas):
    return '<dl class="vt-util__datos">' + "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in filas) + "</dl>"


def render(k):
    tipo, f, ci = k["tipo"], k["faq"], k["cierre"]
    d, ca, l = k["donde"], k["categorias"], k["llegar"]
    bloques = [
        c.portada(k["portada"], tipo, k["migas"]),
        c.respuesta(k.get("respuesta")),
        c.bloque(1, "Dónde estamos", "vt-h-donde", d["titulo"], c.fichas(d["hechos"]), lede=d["lede"], id_seccion="donde"),
        c.bloque(2, "Categorías", "vt-h-categorias", ca["titulo"], c.fichas(ca["items"]), lede=ca["lede"], tinte=True),
        c.bloque(3, "Visítanos", "vt-h-llegar", l["titulo"], _datos(l["datos"]), id_seccion="como-llegar"),
        c.bloque_dos(4, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True),
        # Reescritura 10 (Entrega B de experiencia): el botón dice qué se pregunta.
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo, texto="Preguntar si la tienen"),
    ]
    return base.documento(base.meta_de(k), "\n".join(bloques), jsonld_bloques=k["jsonld"],
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), clase_body=CLASE_BODY)
