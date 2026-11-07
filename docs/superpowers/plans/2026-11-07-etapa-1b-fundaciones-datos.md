# Etapa 1 · Fundaciones — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sub-plan **1b de 2** de la Etapa 1 de `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md`: datos sin contradicciones en todo lo publicado. "Av. Álvaro Obregón 209 Sur" en cada página, `llms.txt` y generador; una sola promesa de respuesta ("Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h"); las contradicciones del §5.2 (reseñas, clientes, mayoreo 500 m², mantenimiento $750/mes, "sobre pedido", banner de lluvias, nota interna y conteo del blog, tabla que desacredita el sintético, FAQ de precio de la home, garantía de plantas condicionada, "líder", gracias); las decisiones del dueño del 2026-11-07 que tocan contenido (framboyán desde $250, sin "próximo corte" ni aviso de disponibilidad semanal); "pagas cuando" retirado; perfiles oficiales (`sameAs`) corregidos; `/precios` y `/vivero-tampico` en `llms.txt`; botón "+ Agregar" del hub de la tienda entero a 1440. Todo queda protegido por `tools/site/tests/test_consistencia.py`. **Orden:** se ejecuta después de 1a (`2026-11-07-etapa-1a-fundaciones-shell.md`), sobre `main` con 1a ya en producción. Se publica sola.

**Architecture:** Una prueba de consistencia nueva recorre el texto público de las 108 páginas (texto visible, JSON-LD, atributos legibles y mensajes de WhatsApp, con la misma función `textos_publicos` de `test_reglas.py`) y `llms.txt`, y falla con cada dato contradictorio o frase prohibida. La corrección es un script único e idempotente (`tools/site/corregir_datos.py`) con tres partes: reglas globales sobre todas las páginas, `llms.txt` y las fuentes de `tools/pasto` y `tools/servicios` (domicilio, promesa, perfiles, ortografía de framboyán); reemplazos exactos por archivo (cada uno falla si no encuentra ni el texto viejo ni el corregido, para no corregir a ciegas); y retiro de elementos completos con `shell.fin_elemento` (banner de lluvias, barra "Lote semanal: DISPONIBLE", etiquetas de "búsquedas" del blog). Las páginas generadas se corrigen en su fuente (`tools/pasto/*.py`, `tools/servicios/pages.py` y `hero.py`) y el build las regenera; el conteo de artículos del blog lo pone el build (`shell.py`). El shell, los tokens y la medición de 1a no cambian.

**Tech Stack:** Python 3.9+ estándar y `unittest`; Playwright para Python 1.48 en la prueba del hub de la tienda (se salta sin Playwright; corre en CI); CSS plano.

---

## Reglas para quien ejecuta

- Trabaja en `~/dev/viverosterra-e1`, rama `feat/etapa-1b` (creada en el Step 12 de la Tarea 25 de 1a). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`; `git add` con rutas explícitas; nunca `.DS_Store`; si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js`.
- Reglas del dueño (no se rompen en ninguna línea nueva): nunca "Oasis" ni marcas de proveedor; nunca el nombre del proveedor de la terminal en `public/`; nada de "MSI", "sin intereses" ni "0%" en pagos; sin pádel ni canchas para sintético; sin muestras físicas; envío de sintético nunca "gratis"; "para llevar hoy" solo Toscana 18 y 28; el primer riego lo hace el cliente, en positivo; nunca "pagas cuando ves tu jardín terminado"; garantía de pasto solo como "Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego"; promesa única; desde 2007; REPSE 773725; +500,000 m²; "4.6 en Google (24 reseñas)"; framboyán desde $250; sin fecha de corte ni disponibilidad semanal.
- Lo que este sub-plan no toca a propósito: plantillas y diseño de los cuerpos (Etapa 2), títulos y canibalización (Etapa 3), JSON-LD único y autor "Equipo técnico de Viveros Terra" en el marcado (Etapa 4; el dato ya está en `datos.AUTOR_BLOG`), testimonios con nombre de pasto en rollo y plantas (los revisa el dueño en la Etapa 2: si no son reales, se retiran). La página `/gracias` no recibe el "resumen de lo calculado" del §5.2 porque el formulario no le pasa datos; se agrega cuando el cotizador de la Etapa 2 mande el resumen en la URL.

## File structure

| Archivo | Acción y responsabilidad |
|---|---|
| `tools/site/tests/test_consistencia.py` | Crear: datos oficiales y frases prohibidas en todo lo publicado. |
| `tools/site/corregir_datos.py` | Crear: corrección única e idempotente de los datos contradictorios. |
| `tools/site/tests/test_corregir_datos.py` | Crear: pruebas de las reglas globales y herramientas del corrector. |
| `tools/site/shell.py` | Modificar: el build pone el número real de artículos en el índice del blog. |
| `tools/site/tests/test_conteo_blog.py` | Crear: pruebas del conteo. |
| `tools/site/tests/test_tienda_navegador.py` | Crear: el botón "Agregar" cabe en cada tarjeta del hub a 1100/1280/1440. |
| `public/css/tienda-pasto.css` | Modificar: pie de la tarjeta del hub en dos renglones cuando no cabe. |
| ~75 × `public/**/*.html`, `public/llms.txt` | Modificar: corrección de datos (script) + regeneración (build). |
| `tools/pasto/local.py`, `zonas.py`, `precios.py`, `common.py` y demás con domicilio o promesa | Modificar: fuente de las páginas generadas (script). |
| `tools/servicios/hero.py`, `tools/servicios/pages.py` | Modificar: promesa de la portada de servicios, domicilio y framboyán (script). |

---

### Task 0: Rama y línea base

**Files:** ninguno.

- [ ] **Step 1: Confirmar la rama y que 1a está en `main`**

```bash
cd ~/dev/viverosterra-e1
git status --short | wc -l
git branch --show-current
git log --oneline -3
test -f tools/site/shell.py && echo "1a presente"
```

Expected: `0`; `feat/etapa-1b`; el merge de 1a entre los últimos commits; `1a presente`. Si la rama no existe: `git fetch origin && git checkout -b feat/etapa-1b origin/main`.

- [ ] **Step 2: Pruebas en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
cd ../.. && python3 tools/site/build.py | tail -1
```

Expected: `OK` (o `OK (skipped=6)` sin Playwright) tres veces y `shell: 0 de 108 páginas actualizadas`.

---

### Task 1: Prueba de consistencia de datos (falla con lo que hay hoy)

**Files:**
- Test: `tools/site/tests/test_consistencia.py`

- [ ] **Step 1: Escribir la prueba**

`tools/site/tests/test_consistencia.py`:

```python
"""Consistencia de datos en todo lo publicado (spec §5.2, §5.3 y decisiones del dueño del 2026-11-07)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

PUBLIC = paginas.PUBLIC
PAGINAS = {p: p.read_text(encoding="utf-8") for p in sorted(PUBLIC.rglob("*.html"))}
TEXTOS = {p: textos_publicos(h) for p, h in PAGINAS.items()}
LLMS = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
PROHIBIDAS = (
    ("promesa de respuesta vieja",
     r"\b[Rr]espond\w*\s+(?:por WhatsApp\s+)?(?:en minutos|hoy|el mismo día|en menos de (?:[2-9]|\d{2,}) horas)"),
    ("plazo de respuesta viejo", r"\ben menos de (?:2|4) horas\b|\b2 horas hábiles\b|\bEn 24 hrs\b"),
    ("pago al terminar", r"\bpagas cuando\b"),
    ("líder", r"\blíder\b"),
    ("expertos", r"\bequipo de expertos\b"),
    ("sintético sobre pedido", r"\bmodelos sobre pedido\b"),
    ("aviso de corte o disponibilidad semanal",
     r"pr[oó]ximo corte|lote semanal:\s*disponible|reservar (?:mi|tu) lote|lote de esta semana|instalaciones esta semana|"
     r"temporada de lluvias — el mejor momento"),
    ("mayoreo desde 200 m²", r"(?:mayoreo|pedidos)[^.]{0,60}\b200 m²"),
    ("mantenimiento desde $500/mes", r"mantenimiento[^.]{0,90}desde \$500\s?/\s?mes"),
    ("framboyán a $500", r"framboy[aá]n[^.$]{0,40}\$\s?500\b|\$\s?500\b[^.]{0,40}framboy[aá]n"),
    ("Flamboyán (ortografía)", r"(?<!conocido como )\bflamboyán\b"),
    ("Plan Terra Completo de $50,000", r"Plan Terra Completo (?:de )?\(?\$50,000|\(Plan Terra Completo\)|Plan Terra Completo incluye"),
    ("tabla que desacredita el sintético", r"\báspero\b|\(quema\)"),
    ("reseñas contradictorias", r"\b127 reseñas\b|\b5(?:\.0)? en Google\b"),
    ("clientes contradictorios", r"Más de 1,500 clientes"),
    ("nota interna del blog", r"\bWix\b|\d[\d,]* búsquedas"),
    ("años de la empresa distintos de 2007", r"(?:más de|con|llevamos) (?:1[0-7]|[1-9]) años (?:de experiencia|de trayectoria|en el mercado)"),
)


def nombre(path):
    return str(path.relative_to(PUBLIC))


class ConsistenciaTest(unittest.TestCase):
    maxDiff = None

    def test_domicilio_siempre_con_209_sur(self):
        sin_sur = [nombre(p) for p, h in PAGINAS.items() if re.search(r"Obreg[oó]n 209(?! Sur)", h)]
        self.assertEqual(sin_sur, [])
        self.assertIsNone(re.search(r"Obreg[oó]n 209(?! Sur)", LLMS))

    def test_sin_datos_contradictorios_ni_frases_prohibidas(self):
        hallazgos = []
        for path, texto in list(TEXTOS.items()) + [(PUBLIC / "llms.txt", LLMS)]:
            for regla, patron in PROHIBIDAS:
                for m in re.finditer(patron, texto, re.I):
                    hallazgos.append(f"{nombre(path)} · {regla} · …{texto[max(0, m.start() - 50):m.end() + 50]}…")
        self.assertEqual(hallazgos, [])

    def test_para_llevar_hoy_solo_toscana(self):
        for path, texto in TEXTOS.items():
            for m in re.finditer(r"\bpara llevar\b", texto, re.I):
                with self.subTest(pagina=nombre(path), pos=m.start()):
                    self.assertRegex(texto[max(0, m.start() - 300):m.start()], r"Toscana (?:18|28)")

    def test_garantia_de_plantas_con_condicion(self):
        for archivo in ("catalogo.html", "diseno-jardines-tampico/index.html"):
            texto = TEXTOS[PUBLIC / archivo]
            for m in re.finditer(r"Garantía de arraigo 30 días", texto):
                with self.subTest(pagina=archivo, pos=m.start()):
                    self.assertIn("sembramos nosotros", texto[m.start():m.end() + 160])

    def test_home_con_cifras_oficiales(self):
        home = TEXTOS[PUBLIC / "index.html"]
        self.assertIn("+900 clientes · +1,500 instalaciones", home)
        faq = re.search(r'"name":"¿Cuánto cuesta el pasto en rollo en Tampico\?","acceptedAnswer":\{"@type":"Answer","text":"([^"]+)"',
                        PAGINAS[PUBLIC / "index.html"]).group(1)
        for cifra in ("$85 por m²", "desde $120 por m²", "500 m²", "$60/m²"):
            self.assertIn(cifra, faq)

    def test_framboyan_desde_250(self):
        texto = TEXTOS[PUBLIC / "arboles-ornamentales-tampico" / "index.html"]
        self.assertIn("Framboyán desde $250", texto)

    def test_conteo_del_blog_sale_del_build(self):
        posts = len(list((PUBLIC / "blog").glob("*/index.html")))
        self.assertIn(f'<span data-vt-conteo="blog">{posts}</span> guías', PAGINAS[PUBLIC / "blog" / "index.html"])

    def test_gracias_con_promesa_unica_y_sin_emojis(self):
        html = PAGINAS[PUBLIC / "gracias" / "index.html"]
        self.assertIn(datos.PROMESA_COMPLETA, html)
        self.assertIsNone(re.search("[\U0001F300-\U0001FAFF]", html))

    def test_perfiles_oficiales(self):
        for path, html in list(PAGINAS.items()) + [(PUBLIC / "llms.txt", LLMS)]:
            with self.subTest(pagina=nombre(path)):
                self.assertNotIn("il.linkedin.com", html)
                self.assertNotIn("http://www.tiktok.com", html)
                self.assertIsNone(re.search(r"instagram\.com/viverosterra(?!mx)", html))

    def test_llms_con_paginas_y_datos_oficiales(self):
        for texto in ("https://www.viverosterra.com/precios", "https://www.viverosterra.com/vivero-tampico", "209 Sur",
                      "entrando por Banamex", "desde 2012", "en menos de 1 hora en horario", "## Lo que no hacemos",
                      "https://www.instagram.com/viverosterramx"):
            with self.subTest(texto=texto):
                self.assertIn(texto, LLMS)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_consistencia.py 2>&1 | grep -E "^FAIL:|^Ran|FAILED"`
Expected: `Ran 10 tests` y `FAILED (failures=18)` aproximadamente (fallan 9 de las 10 pruebas, todas salvo `test_para_llevar_hoy_solo_toscana`; las subpruebas suman el resto). En la lista de `test_sin_datos_contradictorios…` aparecen, entre otros: "pagas cuando" en pasto en rollo, "líder" en la home, "+127 reseñas", "Más de 1,500 clientes", "modelos sobre pedido", "Lote semanal: DISPONIBLE", "Temporada de lluvias — el mejor momento", "Wix" y "búsquedas" en el blog, "a partir de 200 m²", "desde $500/mes", "Flamboyán desde $500", "(quema)" y "áspero", "Plan Terra Completo ($50,000+)" y las promesas viejas ("hoy mismo", "en minutos", "el mismo día", "4 horas hábiles", "2 horas", "24 hrs").

- [ ] **Step 3: Commit de la prueba en rojo (documenta el estado de partida)**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/tests/test_consistencia.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(site): consistencia de datos oficiales en todo lo publicado (en rojo)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(CI de la rama queda en rojo hasta la Tarea 4; no se abre PR antes.)

---

### Task 2: Corrector de datos (`tools/site/corregir_datos.py`)

**Files:**
- Create: `tools/site/corregir_datos.py`
- Test: `tools/site/tests/test_corregir_datos.py`

Cada reemplazo por archivo se tomó del HTML real del 2026-11-07. Si alguno ya no coincide (alguien editó la página), el script se detiene con `no encontré el texto a corregir ni su corrección: …`; en ese caso abre el archivo, ubica el texto equivalente, ajusta el par `(viejo, nuevo)` en `POR_ARCHIVO` y vuelve a correr.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_corregir_datos.py`:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import corregir_datos as c  # noqa: E402


class ReglasGlobalesTest(unittest.TestCase):
    def test_domicilio_con_sur_sin_duplicar(self):
        self.assertEqual(c.corregir_texto("Av. Álvaro Obregón 209, Col. Ampliación"), "Av. Álvaro Obregón 209 Sur, Col. Ampliación")
        self.assertEqual(c.corregir_texto("Obregón 209 Sur"), "Obregón 209 Sur")
        self.assertEqual(c.corregir_texto("Av. Alvaro Obregon 209 · Madero"), "Av. Alvaro Obregon 209 Sur · Madero")

    def test_promesa_unica(self):
        casos = {
            "Sin compromiso · Respondemos hoy mismo": "Sin compromiso · Respondemos en menos de 1 hora en horario",
            "— respondemos en minutos": "— respondemos en menos de 1 hora en horario",
            "Te respondemos hoy y, si hace falta": "Te respondemos en menos de 1 hora en horario y, si hace falta",
            "Respondemos el mismo día · Lun a vie 9 a 18 h, sáb 9 a 14 h":
                "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h",
            "Respondemos hoy · Lun–Sáb": "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h",
            "Respondemos en menos de 4 horas hábiles. También": "Respondemos en menos de 1 hora en horario. También",
            "Respondemos con el precio final": "Respondemos con el precio final",
        }
        for viejo, nuevo in casos.items():
            with self.subTest(viejo=viejo):
                self.assertEqual(c.corregir_texto(viejo), nuevo)

    def test_perfiles_y_framboyan(self):
        self.assertEqual(c.corregir_texto("https://il.linkedin.com/company/viveros-terra-tampico"),
                         "https://www.linkedin.com/company/viveros-terra-tampico")
        self.assertEqual(c.corregir_texto("https://www.instagram.com/viverosterra"), "https://www.instagram.com/viverosterramx")
        self.assertEqual(c.corregir_texto("https://www.instagram.com/viverosterramx"), "https://www.instagram.com/viverosterramx")
        self.assertEqual(c.corregir_texto("Flamboyán Tabachín y flamboyán"), "Framboyán Tabachín y framboyán")
        self.assertEqual(c.corregir_texto("también conocido como flamboyán"), "también conocido como flamboyán")
        self.assertEqual(c.corregir_texto("Lomas del Chairel y Flamboyanes"), "Lomas del Chairel y Flamboyanes")


class HerramientasTest(unittest.TestCase):
    def test_quitar_elementos_con_su_linea(self):
        html = '<p>a</p>\n  <div id="urgencia-banner"><span>x</span></div>\n<p>b</p>'
        self.assertEqual(c.quitar_elementos(html, r'<div id="urgencia-banner"'), "<p>a</p>\n<p>b</p>")

    def test_reemplazar_es_idempotente_y_reporta_lo_que_falta(self):
        self.assertEqual(c.reemplazar("x 200 m² y", "200 m²", "500 m²", "f"), "x 500 m² y")
        self.assertEqual(c.reemplazar("x 500 m² y", "200 m²", "500 m²", "f"), "x 500 m² y")
        with self.assertRaises(SystemExit):
            c.reemplazar("nada", "200 m²", "500 m²", "f")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_corregir_datos.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'corregir_datos'` y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar `tools/site/corregir_datos.py`**

```python
"""Corrección única de datos contradictorios (Etapa 1b, spec §5.2 y decisiones del dueño del 2026-11-07).

Reglas globales (todas las páginas, llms.txt y las fuentes de tools/pasto y tools/servicios): domicilio "209 Sur",
promesa única de respuesta, perfiles oficiales y una sola ortografía de framboyán. Cambios por archivo: home, pasto en
rollo, mayoreo, sintético en Tampico, árboles ornamentales, catálogo, diseño, blogs de precios, índice del blog,
gracias y llms.txt. Es idempotente: lo ya corregido se salta; lo que no encuentra y no está corregido lo reporta.

Uso: python3 tools/site/corregir_datos.py   (desde cualquier carpeta; después corre python3 tools/site/build.py)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from shell import fin_elemento  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PUBLIC = RAIZ / "public"
PROMESA = "Respondemos en menos de 1 hora en horario"
HORARIO = "Lun a vie 9 a 18 h, sáb 9 a 14 h"

GLOBALES = (
    ("Cotización gratis, sin compromiso. Respondemos hoy mismo y enviamos precio en menos de 2 horas.",
     f"Cotización gratis, sin compromiso. {PROMESA}."),
    ("Respondemos por WhatsApp hoy mismo.", "Respondemos por WhatsApp en menos de 1 hora en horario."),
    ("Respondemos en minutos por WhatsApp", "Respondemos por WhatsApp en menos de 1 hora en horario"),
    ("Respondemos hoy · Lun–Sáb", f"{PROMESA} · {HORARIO}"),
    ("Respondemos en menos de 4 horas hábiles. Lun–Vie 9–18h, Sáb 9–14h.", f"{PROMESA} · {HORARIO}."),
    ("Respondemos en menos de 4 horas hábiles.", f"{PROMESA}."),
    ("Respondemos el mismo día · Lun a vie", f"{PROMESA} · Lun a vie"),
    ("Respondemos hoy mismo · Lun a vie", f"{PROMESA} · Lun a vie"),
    ("Sin compromiso · Respuesta en menos de 2 horas · Lun–Sáb", f"Sin compromiso · {PROMESA} · {HORARIO}"),
    ("Respuesta en menos de 2 horas · Lun–Sáb", f"{PROMESA} · {HORARIO}"),
    ("Atención directa en menos de 2 horas", "Respuesta en menos de 1 hora en horario"),
    ("Precio claro en menos de 2 horas, sin compromiso", "Precio claro en menos de 1 hora en horario, sin compromiso"),
    ("Cotiza tu jardín en menos de 2 horas", "Cotiza tu jardín: respondemos en menos de 1 hora en horario"),
    ("Cotiza en menos de 2 horas.", f"{PROMESA}."),
    ("En menos de 2 horas hábiles te enviamos cotización detallada por correo y WhatsApp.",
     f"{PROMESA}: te enviamos tu cotización por WhatsApp o correo."),
    ("Te contactamos en 24 hrs", "Te respondemos en menos de 1 hora en horario"),
    ("https://il.linkedin.com/company/viveros-terra-tampico", "https://www.linkedin.com/company/viveros-terra-tampico"),
    ("http://www.tiktok.com/@viverosterra", "https://www.tiktok.com/@viverosterra"),
    ("Flamboyán", "Framboyán"),
    ("Flamboy%C3%A1n", "Framboy%C3%A1n"),
)
REGLAS = (
    (re.compile(r"(Obreg[oó]n 209)(?! Sur)"), r"\1 Sur"),
    (re.compile(r"\b([Rr])espondemos (?:hoy mismo|hoy|el mismo día|en minutos)\b"), r"\1espondemos en menos de 1 hora en horario"),
    (re.compile(r"https://www\.instagram\.com/viverosterra(?!mx)"), "https://www.instagram.com/viverosterramx"),
    (re.compile(r"(?<!conocido como )flamboyán"), "framboyán"),
)

POR_ARCHIVO = (
    # Home: prueba social sin contradicción, FAQ de precio con cifras (A04 §7 bloque A), sin "líder".
    ("public/index.html",
     '<strong style="color:#A5D6A7">Más de 1,500 clientes</strong> han calculado su jardín con nosotros',
     '<strong style="color:#A5D6A7">+900 clientes · +1,500 instalaciones</strong> desde 2007'),
    ("public/index.html",
     '"text":"Cotización inmediata por WhatsApp al 833 326 8008. Varía según tipo y volumen."',
     '"text":"En Viveros Terra el pasto San Agustín en rollo cuesta $85 por m² solo el pasto y desde $120 por m² instalado, '
     'con IVA incluido. El instalado incluye la preparación básica del terreno, la colocación y una garantía de arraigo de '
     '15 a 20 días. En pedidos de 500 m² o más, el mayoreo cuesta desde $60/m². Precios vigentes en noviembre de 2026 para '
     'Tampico, Ciudad Madero y Altamira."'),
    ("public/index.html",
     '<div class="pb-5">El precio varía según tipo y volumen. Te ofrecemos <strong>cotización inmediata por WhatsApp</strong> '
     'al 833 326 8008. En minutos sabrás el costo por m² con o sin instalación.</div>',
     '<div class="pb-5">En Viveros Terra el pasto San Agustín en rollo cuesta <strong>$85 por m² solo el pasto</strong> y '
     '<strong>desde $120 por m² instalado</strong>, con IVA incluido. El instalado incluye la preparación básica del terreno, '
     'la colocación y una garantía de arraigo de 15 a 20 días. En pedidos de 500 m² o más, el mayoreo cuesta desde $60/m². '
     'Precios vigentes en noviembre de 2026 para Tampico, Ciudad Madero y Altamira. <a href="/precios">Ver lista de precios</a></div>'),
    ("public/index.html",
     '<span class="text-primary font-semibold text-sm uppercase tracking-wider">El vivero líder en Tampico</span>',
     '<span class="text-primary font-semibold text-sm uppercase tracking-wider">Vivero en Cd. Madero desde 2007</span>'),
    ("public/index.html",
     '<div class="text-2xl font-display font-bold text-accent">+127</div>\n'
     '            <div class="text-white/55 text-xs mt-1">Reseñas verificadas</div>',
     '<div class="text-2xl font-display font-bold text-accent">+1,500</div>\n'
     '            <div class="text-white/55 text-xs mt-1">Instalaciones desde 2007</div>'),
    ("public/index.html",
     "Viveros Terra es la empresa líder en jardinería y pasto en rollo del sur de Tamaulipas.",
     "Viveros Terra es un vivero y empresa de jardinería de Ciudad Madero, fundada en 2007."),
    # Pasto en rollo: nunca "pagas cuando"; tabla comparativa sin desacreditar el sintético que también vendemos.
    ("public/pasto-en-rollo-tampico/index.html",
     '<div class="text-gray-500 text-sm mt-1">Pagas cuando ves el resultado</div>',
     '<div class="text-gray-500 text-sm mt-1">Contado o mensualidades con tarjeta</div>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '<p class="text-white/75 text-xs">Pagas cuando ves tu jardín listo — sin pago total por adelantado</p>',
     '<p class="text-white/75 text-xs">Contado o mensualidades con tarjeta de crédito</p>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '<span class="text-primary font-bold">Pagas cuando ves el resultado</span>',
     '<span class="text-primary font-bold">Contado o mensualidades con tarjeta</span>'),
    ("public/pasto-en-rollo-tampico/index.html",
     "Pagas cuando ves tu jardín listo</li>",
     "Mensualidades con tarjeta de crédito</li>"),
    ("public/pasto-en-rollo-tampico/index.html",
     "No. <strong>Pagas cuando ves tu jardín terminado.</strong> Sin pago total por adelantado, sin sorpresas. Lo importante "
     "es que empieces con tranquilidad y que confíes en el resultado.",
     "No. No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos un anticipo, y puedes pagar en mensualidades con tarjeta "
     "de crédito en cotizaciones desde $2,000. Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo "
     "el protocolo de riego."),
    ("public/pasto-en-rollo-tampico/index.html",
     '<div class="pb-5">Sí. La idea es sencilla: <strong>pagas cuando ves el resultado.</strong> No pedimos el 100% por '
     "adelantado. Al confirmar tu proyecto coordinamos el esquema contigo directamente — sin letras chicas ni sorpresas. "
     "de pago flexibles</strong> — adaptamos las condiciones a tu proyecto y conveniencia. Lo que no hacemos es pedirte el "
     "100% por adelantado sin haber entregado nada. Pregúntanos al cotizar y te decimos qué opciones hay para tu caso.</div>",
     '<div class="pb-5">Sí. No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos un anticipo, sin '
     "letra chica. También puedes pagar en mensualidades con tarjeta de crédito desde $2,000; los plazos dependen del monto "
     '(<a href="/politicas#mensualidades">ver condiciones</a>).</div>'),
    ("public/pasto-en-rollo-tampico/index.html",
     "Cotización en menos de 1 hora. Sin compromiso. Pagas cuando ves tu jardín listo.",
     "Respondemos en menos de 1 hora en horario. Sin compromiso. Si una sección no arraiga en 15 a 20 días, la reponemos sin costo."),
    ("public/pasto-en-rollo-tampico/index.html",
     '<h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mt-3 mb-3">Pasto San Agustín en rollo o pasto sintético</h2>\n'
     '      <p class="text-gray-700 max-w-2xl mx-auto">Las dos opciones más solicitadas para jardines en Tampico, comparadas en '
     "costo, mantenimiento, durabilidad y estética.</p>",
     '<h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mt-3 mb-3">¿Cuál te conviene según tu espacio?</h2>\n'
     '      <p class="text-gray-700 max-w-2xl mx-auto">Vendemos e instalamos los dos en Tampico. Esta tabla te ayuda a elegir '
     "según tu espacio, tu presupuesto y el tiempo que quieras dedicarle.</p>"),
    ("public/pasto-en-rollo-tampico/index.html",
     '<tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Temperatura al sol</td><td class="py-3 px-4 sm:px-6">'
     '28-32°C (fresco)</td><td class="py-3 px-4 sm:px-6">50-60°C (quema)</td></tr>',
     '<tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Riego</td><td class="py-3 px-4 sm:px-6">Diario al '
     'instalar; después, según el clima</td><td class="py-3 px-4 sm:px-6">Sin riego; solo un enjuague ocasional</td></tr>'),
    ("public/pasto-en-rollo-tampico/index.html",
     '          <tr><td class="py-3 px-4 sm:px-6 font-semibold">Sensación al tacto</td><td class="py-3 px-4 sm:px-6">Natural, '
     'suave</td><td class="py-3 px-4 sm:px-6">Plástico, áspero</td></tr>\n'
     '          <tr class="bg-gray-50"><td class="py-3 px-4 sm:px-6 font-semibold">Reciclable</td><td class="py-3 px-4 sm:px-6">'
     'Sí (compostable)</td><td class="py-3 px-4 sm:px-6">No (residuo plástico)</td></tr>\n',
     ""),
    ("public/pasto-en-rollo-tampico/index.html",
     '<td class="py-3 px-4 sm:px-6">Terrazas sin tierra, pet áreas</td>',
     '<td class="py-3 px-4 sm:px-6">Terrazas, azoteas, áreas sin riego y zonas para mascotas</td>'),
    ("public/pasto-en-rollo-tampico/index.html",
     "Para jardines residenciales en Tampico con clima cálido-húmedo, el pasto natural San Agustín ofrece mejor relación "
     "costo-beneficio a largo plazo (15+ años vs 8-10 años). El sintético tiene sentido solo en terrazas, áticos o zonas sin "
     "tierra disponible.",
     "Si tu jardín tiene tierra y puedes regarlo, el San Agustín cuesta menos por metro y dura más. Si es una terraza, una "
     "azotea o un área sin riego, te conviene el sintético: también lo vendemos e instalamos en Tampico "
     '(<a href="/pasto-sintetico-tampico" class="text-primary font-semibold underline">ver pasto sintético</a>).'),
    # Mayoreo: el mínimo es 500 m².
    ("public/mayoreo-pasto-tampico/index.html", "pedidos a partir de 200 m²", "pedidos a partir de 500 m²"),
    # Sintético en Tampico (fuente: el generador): los 9 modelos en existencia; "para llevar hoy" solo Toscana 18 y 28.
    ("tools/pasto/local.py",
     'existencia para llevar el mismo día, y los otros 7 modelos sobre pedido. Atendemos de lunes a viernes de 9 a 18 h "',
     'existencia para llevar hoy; los otros 7 modelos también están en existencia y llegan en 3 a 5 días. Atendemos de '
     'lunes a viernes de 9 a 18 h "'),
    # Framboyán desde $250 (decisión del dueño 2026-11-07).
    ("public/arboles-ornamentales-tampico/index.html", "Framboyán desde $500", "Framboyán desde $250"),
    ("public/arboles-ornamentales-tampico/index.html",
     'Desde <strong>$350</strong></span><span class="svc-hero__price-alt">crespón $350 · jacaranda $450 · framboyán $500</span>',
     'Desde <strong>$250</strong></span><span class="svc-hero__price-alt">framboyán $250 · crespón $350 · jacaranda $450</span>'),
    ("tools/servicios/pages.py",
     'price_pre="Desde", price="$350", price_unit="", price_alt="· crespón $350 · jacaranda $450 · framboyán $500",',
     'price_pre="Desde", price="$250", price_unit="", price_alt="· framboyán $250 · crespón $350 · jacaranda $450",'),
    # Garantía de plantas siempre con su condición.
    ("public/catalogo.html",
     "</svg>Garantía de arraigo 30 días</span>",
     '</svg>Garantía de arraigo 30 días en plantas que sembramos nosotros · <a href="/politicas#garantia-plantas">ver condiciones</a></span>'),
    ("public/diseno-jardines-tampico/index.html",
     "<strong>Garantía de arraigo 30 días:</strong> reponemos plantas sin costo",
     '<strong>Garantía de arraigo 30 días:</strong> reponemos sin costo las plantas que sembramos nosotros, con el riego '
     'indicado (<a href="/politicas#garantia-plantas">ver condiciones</a>)'),
    # Blogs de precios: mantenimiento desde $750/mes; el paquete de $50,000 es "Proyecto completo".
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "va desde $500/mes para jardines pequeños",
     "va desde $750/mes para jardines pequeños"),
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "Plan Terra Completo de $50,000+",
     "Proyecto completo de $50,000+"),
    ("public/blog/cuanto-cuesta-jardin-tampico-precios/index.html", "Plan Terra Completo ($50,000+)",
     "Proyecto completo ($50,000+)"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "Plan Terra Completo ($50,000+)",
     "Proyecto completo ($50,000+)"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "El paquete de $50,000 (Plan Terra Completo)",
     "El Proyecto completo de $50,000"),
    ("public/blog/jardin-bajo-presupuesto-tampico/index.html", "El Plan Terra Completo incluye el primer mes de mantenimiento",
     "El Proyecto completo incluye el primer mes de mantenimiento"),
    # Índice del blog: sin notas internas ni métricas; el conteo lo pone el build.
    ("public/blog/index.html", "</svg>22 artículos</span>", '</svg><span data-vt-conteo="blog">52</span> guías</span>'),
    ("public/blog/index.html", "Por el equipo de expertos de Viveros Terra.", "Por el equipo técnico de Viveros Terra."),
    ("public/blog/index.html", '<h2 class="text-2xl font-display font-bold text-gray-900">Los más buscados</h2>',
     '<h2 class="text-2xl font-display font-bold text-gray-900">Para empezar</h2>'),
    ("public/blog/index.html", '      <span class="text-gray-400 text-sm">· Recuperados del Wix con miles de búsquedas</span>\n', ""),
    # Gracias: promesa única, pasos sin plazos inventados, sin emojis.
    ("public/gracias/index.html",
     '<p class="subtitle">En menos de <strong>2 horas hábiles</strong> te enviamos el detalle completo a tu correo.</p>',
     f'<p class="subtitle">{PROMESA} · {HORARIO}.</p>'),
    ("public/gracias/index.html",
     "<h3>📋 Qué sigue ahora</h3>\n        <ol>\n"
     "          <li><strong>Hoy mismo</strong> (lun–vie 9am–6pm): te llega correo con cotización detallada por servicio.</li>\n"
     "          <li><strong>En 24 hrs:</strong> te contactamos por WhatsApp para agendar visita técnica gratuita.</li>\n"
     "          <li><strong>En la visita:</strong> medimos exacto, te damos precio cerrado y plan de trabajo.</li>\n"
     "          <li><strong>Si te interesa:</strong> arrancamos el proyecto en 3–10 días.</li>\n        </ol>",
     "<h3>Qué sigue ahora</h3>\n        <ol>\n"
     "          <li><strong>Te escribimos</strong> por WhatsApp o correo con tu cotización.</li>\n"
     "          <li><strong>Si hace falta,</strong> agendamos una visita para medir.</li>\n"
     "          <li><strong>En la visita</strong> te damos el precio cerrado y el plan de trabajo.</li>\n        </ol>"),
    ("public/gracias/index.html", "        Hablar ahora por WhatsApp\n", "        Adelantar por WhatsApp\n"),
    ("public/gracias/index.html", "💡 <strong>Tip:</strong> mientras esperas, revisa nuestro", "<strong>Mientras tanto:</strong> revisa nuestro"),
    # llms.txt: entidad sin "líder", datos y páginas que faltaban, "Lo que no hacemos".
    ("public/llms.txt", "> Empresa de jardinería líder en el sur de Tamaulipas, México, desde 2007.",
     "> Vivero y empresa de jardinería de Ciudad Madero, Tamaulipas, México, fundada el 12 de diciembre de 2007."),
    ("public/llms.txt", "- Fundada: 12 de diciembre de 2007 (más de 18 años en la región)\n",
     "Última actualización: 2026-11-07\n\n- Fundada: 12 de diciembre de 2007 (más de 18 años en la región)\n"
     "- Pasto sintético con envío a todo México desde 2012\n"),
    ("public/llms.txt", "México (frente a Walmart). Google Maps:", "México (frente a Walmart, entrando por Banamex). Google Maps:"),
    ("public/llms.txt", "- Horario: Lunes–Viernes 9am–6pm, Sábado 9am–2pm\n",
     "- Horario: Lunes–Viernes 9am–6pm, Sábado 9am–2pm\n- Respuesta por WhatsApp: en menos de 1 hora en horario\n"
     "- Perfiles oficiales: https://www.facebook.com/viverosterra/ · https://www.instagram.com/viverosterramx · "
     "https://www.tiktok.com/@viverosterra · https://www.youtube.com/@viverosterramx · "
     "https://www.linkedin.com/company/viveros-terra-tampico · https://maps.app.goo.gl/xC4XGL2WeucAjGwAA\n"),
    ("public/llms.txt", "- [Blog](https://www.viverosterra.com/blog): guías de jardinería para el clima de Tampico\n",
     "- [Precios](https://www.viverosterra.com/precios): lista de precios vigente de pasto, diseño, mantenimiento, riego y "
     "pasto sintético, con IVA\n- [Vivero en Tampico](https://www.viverosterra.com/vivero-tampico): dirección, horario y "
     "cómo llegar\n- [Blog](https://www.viverosterra.com/blog): guías de jardinería para el clima de Tampico\n"),
    ("public/llms.txt", "sin garantía de arraigo.\n\n- ¿Cuánto cuesta", "sin garantía de arraigo.\n- ¿Cuánto cuesta"),
    ("public/llms.txt", "- ¿Hacen entregas a domicilio? Sí, en Tampico, Madero y Altamira; mayoreo a toda la Huasteca.\n",
     "- ¿Hacen entregas a domicilio? Sí, en Tampico, Madero y Altamira; mayoreo a toda la Huasteca.\n\n"
     "## Lo que no hacemos\n- No enviamos muestras físicas del pasto sintético: se elige con fichas técnicas y fotos.\n"
     "- No enviamos pasto natural fuera de la región (Tampico, Madero, Altamira y la Huasteca).\n"
     "- No publicamos fechas de corte ni disponibilidad semanal.\n"),
)

ELEMENTOS = (
    ("public/index.html", r'<div id="urgencia-banner"'),
    ("public/pasto-en-rollo-tampico/index.html", r'<div class="disponibilidad-bar\b'),
    ("public/blog/index.html", r'<span class="tag-hot">'),
)
COMENTARIOS = (
    ("public/index.html", "<!-- BANNER URGENCIA ESTACIONAL — actualizar texto según temporada -->\n"),
    ("public/pasto-en-rollo-tampico/index.html", "<!-- ═══ DISPONIBILIDAD SEMANAL — el diferenciador de frescura ═══ -->\n"),
)


def corregir_texto(texto):
    """Aplica las reglas globales (domicilio, promesa, perfiles, framboyán)."""
    for viejo, nuevo in GLOBALES:
        texto = texto.replace(viejo, nuevo)
    for patron, reemplazo in REGLAS:
        texto = patron.sub(reemplazo, texto)
    return texto


def quitar_elementos(texto, patron):
    """Quita todos los elementos que abren con `patron`, con su sangría y su salto de línea."""
    while True:
        m = re.search(patron, texto)
        if not m:
            return texto
        inicio, fin = m.start(), fin_elemento(texto, m.start())
        while inicio > 0 and texto[inicio - 1] in " \t":
            inicio -= 1
        if (inicio == 0 or texto[inicio - 1] == "\n") and texto[fin:fin + 1] == "\n":
            fin += 1
        texto = texto[:inicio] + texto[fin:]


def reemplazar(texto, viejo, nuevo, rel):
    """Reemplaza `viejo` por `nuevo`; si ya está corregido no hace nada; si no encuentra ninguno de los dos, falla."""
    if nuevo and nuevo in texto:
        return texto
    if viejo in texto:
        return texto.replace(viejo, nuevo)
    if not nuevo:
        return texto
    raise SystemExit(f"{rel}: no encontré el texto a corregir ni su corrección: {viejo[:80]}")


def archivos_globales():
    yield from sorted(PUBLIC.rglob("*.html"))
    yield PUBLIC / "llms.txt"
    yield from sorted((RAIZ / "tools" / "pasto").glob("*.py"))
    yield from sorted((RAIZ / "tools" / "servicios").glob("*.py"))


def main():
    cambiados = set()
    for path in archivos_globales():
        original = path.read_text(encoding="utf-8")
        nuevo = corregir_texto(original)
        if nuevo != original:
            path.write_text(nuevo, encoding="utf-8")
            cambiados.add(path)
    for rel, viejo, nuevo in POR_ARCHIVO:
        path = RAIZ / rel
        original = path.read_text(encoding="utf-8")
        texto = reemplazar(original, viejo, nuevo, rel)
        if texto != original:
            path.write_text(texto, encoding="utf-8")
            cambiados.add(path)
    for rel, comentario in COMENTARIOS:
        path = RAIZ / rel
        original = path.read_text(encoding="utf-8")
        if comentario in original:
            path.write_text(original.replace(comentario, ""), encoding="utf-8")
            cambiados.add(path)
    for rel, patron in ELEMENTOS:
        path = RAIZ / rel
        original = path.read_text(encoding="utf-8")
        texto = quitar_elementos(original, patron)
        if texto != original:
            path.write_text(texto, encoding="utf-8")
            cambiados.add(path)
    print(f"{len(cambiados)} archivos corregidos")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_corregir_datos.py 2>&1 | tail -3`
Expected: `Ran 5 tests` y `OK`. (Todavía no se corre sobre el sitio.)

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/corregir_datos.py tools/site/tests/test_corregir_datos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): corrector idempotente de datos contradictorios" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: El build pone el número real de artículos del blog

**Files:**
- Modify: `tools/site/shell.py`
- Test: `tools/site/tests/test_conteo_blog.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_conteo_blog.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import shell  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}
INDICE = """<!DOCTYPE html>
<html><head><title>Blog</title>
<!-- vt:head -->
<!-- /vt:head -->
</head><body>
<!-- vt:header -->
<!-- /vt:header -->
<main id="main"><p><span data-vt-conteo="blog">7</span> guías</p></main>
<!-- vt:footer -->
<!-- /vt:footer -->
</body></html>
"""


class ConteoBlogTest(unittest.TestCase):
    def test_el_build_pone_el_numero_real_de_articulos(self):
        public = Path(tempfile.mkdtemp())
        for slug in ("uno", "dos"):
            (public / "blog" / slug).mkdir(parents=True)
            (public / "blog" / slug / "index.html").write_text("<p>post</p>", encoding="utf-8")
        html = shell.aplicar(INDICE, "/blog", URLS, public=public)
        self.assertIn('<span data-vt-conteo="blog">2</span> guías', html)

    def test_solo_en_el_indice_del_blog(self):
        public = Path(tempfile.mkdtemp())
        html = shell.aplicar(INDICE, "/precios", URLS, public=public)
        self.assertIn('<span data-vt-conteo="blog">7</span> guías', html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_conteo_blog.py 2>&1 | tail -3`
Expected: `TypeError: aplicar() got an unexpected keyword argument 'public'` y `FAILED (errors=2)`.

- [ ] **Step 3: Modificar `tools/site/shell.py`**

Cambio 1 en `tools/site/shell.py`. Reemplazar exactamente:

```python
VT_HERO_RE = re.compile(r'<section\b[^>]*class="vt-hero\b')
```

por:

```python
VT_HERO_RE = re.compile(r'<section\b[^>]*class="vt-hero\b')
CONTEO_BLOG_RE = re.compile(r'(<span data-vt-conteo="blog">)\d+(</span>)')
```

Cambio 2 en `tools/site/shell.py`. Reemplazar exactamente:

```python
def aplicar(html, ruta, urls):
    """Página con el shell canónico de su ruta. Falla si no tiene exactamente una región de cada tipo."""
```

por:

```python
def conteo_blog(public=PUBLIC):
    """Número de artículos publicados en public/blog/<slug>/index.html."""
    return len(list((Path(public) / "blog").glob("*/index.html")))


def aplicar(html, ruta, urls, public=PUBLIC):
    """Página con el shell canónico de su ruta. Falla si no tiene exactamente una región de cada tipo."""
```

Cambio 3 en `tools/site/shell.py`. Reemplazar exactamente:

```python
    html = REGION_RE.sub(lambda m: partes[m.group(1)], html)
    return marcar_ctas(html, ctx["tipo"])
```

por:

```python
    html = REGION_RE.sub(lambda m: partes[m.group(1)], html)
    if ruta == "/blog":
        html = CONTEO_BLOG_RE.sub(lambda m: f"{m.group(1)}{conteo_blog(public)}{m.group(2)}", html)
    return marcar_ctas(html, ctx["tipo"])
```

Cambio 4 en `tools/site/shell.py`. Reemplazar exactamente:

```python
    nuevo = aplicar(original, paginas.ruta_de(path, public), urls)
```

por:

```python
    nuevo = aplicar(original, paginas.ruta_de(path, public), urls, public)
```

- [ ] **Step 4: Correr las pruebas (deben pasar, salvo la de consistencia que sigue en rojo)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_conteo_blog.py tests/test_shell.py tests/test_sitio.py 2>&1 | tail -3`
Expected: `Ran 15 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/shell.py tools/site/tests/test_conteo_blog.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): el conteo de artículos del blog sale del build" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Corregir los datos en todo el sitio y regenerar

**Files:**
- Modify: ~75 páginas de `public/`, `public/llms.txt`, fuentes de `tools/pasto` y `tools/servicios` (por el script)

- [ ] **Step 1: Correr el corrector dos veces (la segunda no debe cambiar nada)**

```bash
cd ~/dev/viverosterra-e1
python3 tools/site/corregir_datos.py
python3 tools/site/corregir_datos.py
```

Expected: primero `73 archivos corregidos` (puede variar en uno o dos si alguien editó páginas después del 2026-11-07); después `0 archivos corregidos`.

- [ ] **Step 2: Regenerar con el build (aplica el shell y el conteo del blog)**

```bash
cd ~/dev/viverosterra-e1
python3 tools/site/build.py | tail -1
python3 tools/site/build.py | tail -1
git diff --quiet -- public/sitemap.xml && echo "sitemap sin cambios"
```

Expected: `shell: 0 de 108 páginas actualizadas` dos veces (el corrector ya escribió 52, que es el número real de artículos; si hubiera otro número de posts, el primer build diría `1 de 108` y pondría el correcto); `sitemap sin cambios`.

- [ ] **Step 3: Correr todas las pruebas (deben pasar)**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `OK` (o `OK (skipped=6)`) tres veces; `ℹ pass 11` y `ℹ fail 0`. Si `test_consistencia` aún reporta algo, el hallazgo dice archivo y contexto: corrígelo agregando el par exacto a `POR_ARCHIVO` (o a `GLOBALES` si se repite en varias páginas), vuelve al Step 1 y anota el caso en el commit.

- [ ] **Step 4: Revisar el diff antes del commit**

```bash
cd ~/dev/viverosterra-e1
git diff --stat | tail -1
git diff -- public/index.html | grep -E "^[-+]" | grep -vE "^(\+\+\+|---)" | cut -c1-160 | head -40
git diff -- public/pasto-en-rollo-tampico/index.html | grep -E "^[-+]" | grep -vE "^(\+\+\+|---)" | cut -c1-160 | head -40
git diff -- public/llms.txt
```

Expected: solo cambios de datos y copy (domicilio, promesa, cifras, framboyán, pagos, tabla, banner y barra retirados); ningún cambio en `<title>`, `canonical`, ni estructura fuera de lo listado en `POR_ARCHIVO` y `ELEMENTOS`.

- [ ] **Step 5: Revisión visual rápida**

```bash
cd ~/dev/viverosterra-e1 && python3 tools/site/capturas.py /tmp/vt-e1b-capturas | head -2
```

Revisa la home (sin banner de lluvias; cuadro "+1,500 Instalaciones desde 2007"; FAQ de precio con cifras), pasto en rollo (sin la barra "Lote semanal"; tabla "¿Cuál te conviene según tu espacio?"), el índice del blog ("52 guías", sin "búsquedas") y gracias.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public tools/pasto tools/servicios
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(datos): 209 Sur, promesa única y contradicciones del sitio corregidas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Botón "+ Agregar" entero en el hub de la tienda

**Files:**
- Modify: `public/css/tienda-pasto.css`
- Test: `tools/site/tests/test_tienda_navegador.py`

Causa (A01 P0-1): a 1100–1440 px el catálogo pone 3 tarjetas por renglón junto al índice lateral, y el pie de la tarjeta (`.spec-card__foot`: precio, "Paga en mensualidades con tarjeta" y botón) no envuelve; el botón se corta por `overflow: hidden`.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_tienda_navegador.py`:

```python
"""El botón "Agregar" de cada tarjeta del hub de la tienda cabe entero en su tarjeta (A01 P0-1: a 1440 salía "Agre")."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CORTADOS = """() => Array.from(document.querySelectorAll('.spec-card')).map((card) => {
  const boton = card.querySelector('.spec-card__add');
  const c = card.getBoundingClientRect();
  const b = boton.getBoundingClientRect();
  const cortado = b.right > c.right + 0.5 || boton.scrollWidth > boton.clientWidth + 1;
  return cortado ? card.querySelector('.spec-card__name').textContent.trim() : null;
}).filter(Boolean)"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class TiendaHubTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base, cls.servidor = servidor.iniciar()
        cls.pw = sync_playwright().start()
        cls.navegador = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.navegador.close()
        cls.pw.stop()
        cls.servidor.shutdown()
        cls.servidor.server_close()

    def test_boton_agregar_entero_en_las_9_tarjetas(self):
        base = self.base
        for ancho in (1100, 1280, 1440):
            contexto = self.navegador.new_context(viewport={"width": ancho, "height": 900})
            self.addCleanup(contexto.close)
            contexto.route("**/*", lambda route: route.continue_()
                           if route.request.url.startswith(base) and "/api/" not in route.request.url else route.abort())
            page = contexto.new_page()
            page.goto(base + "/pasto-sintetico/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.locator(".spec-card").count(), 9)
                self.assertEqual(page.evaluate(CORTADOS), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_tienda_navegador.py 2>&1 | tail -6`
Expected: con Playwright, `AssertionError` con la lista de modelos cortados a 1440 (y posiblemente a 1100/1280) y `FAILED (failures=…)`. Sin Playwright: `OK (skipped=1)`; instálalo (Tarea 0 de 1a) para ver el rojo, porque esta prueba es la única evidencia del arreglo.

- [ ] **Step 3: Agregar al final de `public/css/tienda-pasto.css`**

```css

/* Etapa 1b: el botón "+ Agregar" no se corta en tarjetas angostas (hub a 1100–1440 con índice lateral). */
.spec-card__foot { flex-wrap: wrap; }
.spec-card__price { flex: 1 1 auto; min-width: 0; }
.spec-card__pay { order: 3; flex-basis: 100%; }
.spec-card__add { flex: none; }
```

- [ ] **Step 4: Correr la prueba (debe pasar) y el resto**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_tienda_navegador.py 2>&1 | tail -1
python3 -m unittest discover -s tests 2>&1 | tail -1
```

Expected: `OK`; `OK` (`Ran 108 tests`; sin Playwright, `OK (skipped=7)`).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/css/tienda-pasto.css tools/site/tests/test_tienda_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(tienda): el botón Agregar cabe entero en las tarjetas del hub" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Verificación final, puertas de revisión, merge y producción

**Files:** ninguno nuevo (correcciones que pidan los revisores).

- [ ] **Step 1: Pruebas, build reproducible y CI**

```bash
cd ~/dev/viverosterra-e1
python3 tools/site/build.py | tail -1
git status --porcelain
cd tools/site && python3 -m unittest discover -s tests -v 2>&1 | tail -1
cd ../.. && git push -u origin feat/etapa-1b
gh run watch --exit-status $(gh run list --branch feat/etapa-1b --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: `shell: 0 de 108 páginas actualizadas`; `git status` vacío; `OK`; CI en verde.

- [ ] **Step 2: Grep de respaldo de las reglas de datos**

```bash
cd ~/dev/viverosterra-e1
grep -rhoE "Obreg[oó]n 209.{0,4}" public --include='*.html' --include='*.txt' | grep -vc " Sur"
grep -rnoiE "pagas cuando|modelos sobre pedido|lote semanal: |pr[oó]ximo corte|\blíder\b|127 reseñas|Flamboyán desde \\\$500" public --include='*.html' --include='*.txt' | wc -l
grep -rnoiE "respondemos (hoy|el mismo día|en minutos)|4 horas hábiles|menos de 2 horas" public --include='*.html' --include='*.txt' | wc -l
```

Expected: `0`, `0` y `0`.

- [ ] **Step 3: Consola y capturas**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_navegador.py tests/test_tienda_navegador.py -v 2>&1 | tail -3
cd ~/dev/viverosterra-e1 && python3 tools/site/capturas.py /tmp/vt-e1b-capturas
```

Expected: `OK` (7 pruebas, sin `skipped`); `30 capturas …`.

- [ ] **Step 4: PR**

```bash
cd ~/dev/viverosterra-e1
gh pr create --base main --head feat/etapa-1b --title "Etapa 1b · Fundaciones: datos sin contradicciones" --body "$(cat <<'EOF'
## Qué cambia
- "Av. Álvaro Obregón 209 Sur" en todas las páginas, llms.txt y generadores.
- Una sola promesa: "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h".
- Contradicciones del §5.2 corregidas (reseñas, clientes, mayoreo 500 m², mantenimiento $750/mes, sintético sin "sobre pedido", banner de lluvias, blog sin nota interna y con conteo real, tabla natural/sintético, FAQ de precio de la home, garantía de plantas condicionada, sin "líder", gracias).
- Decisiones del dueño del 2026-11-07: framboyán desde $250; sin "próximo corte" ni "Lote semanal: DISPONIBLE".
- Sin "pagas cuando ves tu jardín…" en pasto en rollo.
- llms.txt con /precios, /vivero-tampico, perfiles oficiales y "Lo que no hacemos"; sameAs corregidos.
- Botón "+ Agregar" entero en el hub de la tienda a 1100–1440.
- `test_consistencia.py` protege todo lo anterior.

## Verificación
- [ ] CI en verde
- [ ] Capturas revisadas
- [ ] Puertas: cumplimiento/QA, CRO, SEO/AEO, diseño
- [ ] Vista previa de Vercel aprobada por el dueño

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: la URL del PR; Vercel comenta la vista previa.

- [ ] **Step 5: Puertas de revisión en paralelo (spec §11)**

Lanza los cuatro revisores a la vez con el diff (`git diff main...feat/etapa-1b`), la vista previa, `/tmp/vt-e1b-capturas` y el spec (§5.2, §5.3, decisiones del dueño, §7.5 para llms):

1. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`, revisor principal de esta parte): cada cambio de copy contra los datos oficiales y las reglas del dueño; que ningún reemplazo haya alterado un sentido (p. ej. vida útil de producto contra años de la empresa, "Flamboyanes" como colonia, "conocido como flamboyán"); calidad y pruebas de `corregir_datos.py`.
2. **CRO** (`general-purpose` con `page-cro`): que la promesa única y los textos de pago nuevos en pasto en rollo sean claros y no quiten confianza; que "Adelantar por WhatsApp" en gracias funcione.
3. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): `llms.txt` (formato, páginas, perfiles, "Lo que no hacemos"), FAQ de la home citable y coherente con `/precios`, `sameAs`, que no cambiaron títulos ni canonical.
4. **Diseño** (`design:design-critique`): home sin banner, tabla de pasto en rollo, índice del blog y gracias en las capturas; tarjetas del hub a 1100/1280/1440.

Corrige críticos y altos (con prueba y nueva corrida de CI) y vuelve a pedir revisión; medios se corrigen o se anotan con motivo en el PR.

- [ ] **Step 6: Aprobación del dueño, merge y producción**

Con el "sí" explícito del dueño sobre la vista previa:

```bash
cd ~/dev/viverosterra
git checkout main
git pull --ff-only
git merge --no-ff feat/etapa-1b -m "fix: etapa 1b, datos sin contradicciones" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push origin main
gh run watch --exit-status $(gh run list --branch main --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: CI en verde y despliegue `Ready` en Vercel.

- [ ] **Step 7: Verificación en vivo**

```bash
W=https://www.viverosterra.com
curl -s $W/ | grep -c "+900 clientes · +1,500 instalaciones"
curl -s $W/ | grep -c "urgencia-banner"
curl -s $W/pasto-en-rollo-tampico | grep -ci "pagas cuando"
curl -s $W/pasto-sintetico-tampico | grep -c "sobre pedido"
curl -s $W/arboles-ornamentales-tampico | grep -c "Framboyán desde \$250"
curl -s $W/blog | grep -o '<span data-vt-conteo="blog">[0-9]*</span> guías'
curl -s $W/llms.txt | grep -cE "viverosterra.com/precios|viverosterra.com/vivero-tampico|209 Sur"
curl -s $W/gracias | grep -c "Respondemos en menos de 1 hora en horario"
```

Expected, en orden: `1` o más; `0`; `0`; `0`; `2`; `<span data-vt-conteo="blog">52</span> guías`; `3` o más; `1` o más. Abre en Chrome la home, pasto en rollo, el hub de la tienda a 1440 y gracias: consola sin errores, botón "Agregar" entero.

- [ ] **Step 8: Si algo crítico falla en vivo**

Vercel > Deployments > despliegue anterior > "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`; corrige en una rama nueva desde `main`.

- [ ] **Step 9: Cierre de la Etapa 1**

```bash
cd ~/dev/viverosterra
git worktree remove ~/dev/viverosterra-e1
git branch -d feat/etapa-1 feat/etapa-1b
```

Expected: worktree y ramas locales borrados (las remotas se borran desde el PR). Avisa al dueño: Etapa 1 completa; la línea base de GA4 corre 2 semanas desde la publicación de 1a; siguiente: plan de la Etapa 2.
