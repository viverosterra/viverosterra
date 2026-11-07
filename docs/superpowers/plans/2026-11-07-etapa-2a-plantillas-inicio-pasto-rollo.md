# Etapa 2a · Plantillas: sistema de componentes, inicio y pasto en rollo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Primer sub-plan de la Etapa 2 de `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` (§10, puntos 1 y 2): un sistema de componentes de cuerpo del híbrido "Plano + Etiqueta" (etiqueta de precio, Medidor de m², cuadro de datos, figuras con pie `FIG.`, proceso NOSOTROS / TÚ / JUNTOS, nota de campo, tabla de precios con Unidad, mensualidades con tarjeta de crédito, FAQ, CTA final) en `terra.css` y `tools/site/componentes.py`; la home (`/`) y `/pasto-en-rollo-tampico` pasan a salir de plantillas con su contenido en datos, sin CSS viejo ni Google Fonts, con una prueba de paridad de contenido contra lo que estaba publicado. Se publica sola (lote 1–2 del spec). Las demás páginas no cambian, salvo el hash de `terra.css` en su `<head>`. Hoja de ruta del resto de la Etapa 2: `docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`.

**Architecture:** Decisión central de la Etapa 2: **el cuerpo de cada tipo de página sale de una plantilla Python y su contenido vive en un módulo de datos**. `tools/site/plantillas/<tipo>.py` expone `render(contenido) -> html` y arma la página con funciones puras de `tools/site/componentes.py`; `tools/site/contenido/<pagina>.py` expone `CONTENIDO` (diccionarios y tuplas de textos, fotos, preguntas) y `PARIDAD`. El contenido es Python y no JSON porque así cada número oficial se escribe una sola vez (`f"{dinero(P['pasto_instalado_m2'])}"` lee `datos.py`); un JSON obligaría a repetir precios o a inventar un mini-lenguaje de sustitución. Los textos son HTML en línea de confianza con una lista cerrada de etiquetas (`a, b, i, em, strong, br, small, span`, verificada por `test_contenido.py`); los atributos se escapan en los componentes. `tools/site/plantillas/base.py` escribe el documento completo: `<head>` con título, descripción, robots, canonical y Open Graph exactamente como estaban publicados, precarga de la imagen principal y JSON-LD compacto; las tres regiones vacías del shell; `<main id="main">` con el cuerpo; los scripts propios de la página. `tools/site/generar.py` registra `(ruta, archivo, plantilla, contenido)`, aplica `shell.aplicar()` y escribe solo si cambia; `build.py` lo llama entre `activos.publicar()` y `shell.aplicar_todo()`, así el build sigue siendo reproducible byte a byte. **CSS:** un solo sistema; `terra.css` crece con los componentes del cuerpo, todos con prefijo `.vt-` y la base de elementos (`h1`, `a`, `p`) solo bajo `<body class="vt-pagina">`, que únicamente tienen las páginas con plantilla: las páginas viejas no cambian. Las páginas migradas dejan de cargar `tailwind.css`, `design-system.css`, `servicios.css`, `legacy-fixes.css` y Google Fonts; cada archivo viejo se borra cuando su último usuario migra (lo controla la hoja de ruta). El presupuesto de `terra.css` pasa de "< 30 KB sin comprimir" a la meta real del spec §8.2, **< 10 KB con gzip** (y < 48 KB sin comprimir), porque ahora sustituye unos 70 KB de CSS viejo por página. **JS:** se reutiliza lo que funciona: `vt-mensualidades.js` (la fórmula, nunca reimplementada), `vt-simulador.js` (mismo marcado `data-sim-*`) y `terra.js` (medición `generate_lead` con `data-cta`, firma, barra móvil oculta con `data-hero-cta`). Lo único nuevo es `public/js/vt-medidor.js`, que no contiene precios: los lee de los `data-*` que escribe `componentes.medidor()` desde `datos.py`, y su cálculo es idéntico al de Python (paridad con `public/js/tests/casos-medidor.json`, corrida por `node --test` y por `unittest`). **SEO:** URL, título, descripción, canonical, Open Graph y tipos de JSON-LD no cambian (los títulos son de la Etapa 3 y el grafo único de la Etapa 4); el `FAQPage` se genera de las preguntas visibles y el `HowTo` de pasto en rollo, de la lista visible "De la cotización a tu jardín verde en 5 pasos", para que el marcado diga lo mismo que la página. **Paridad de contenido:** antes de migrar, `tools/site/paridad.py capturar` congela de cada página su meta, tipos de JSON-LD, encabezados h1–h3, preguntas, precios y enlaces internos; `tests/test_paridad.py` exige que cada elemento siga en la página nueva o que `PARIDAD` diga a qué elemento nuevo pasó o por qué se retiró.

**Tech Stack:** Python 3.9+ estándar (local 3.9.6) y `unittest`; Playwright para Python 1.48 en las pruebas de navegador (se saltan sin él); CSS plano; JavaScript vanilla con `node --test` (sin `package.json`); Lighthouse 12 con `npx` solo para la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2a` (rama `feat/etapa-2a`, Tarea 0). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales: `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` (forma con glob) y las de navegador (`tests/test_navegador.py`, `tests/test_tienda_navegador.py`, `tests/test_plantillas_navegador.py`).
- Cuando una tarea cambia `terra.css`, el build cambia el hash y reescribe el `<head>` de las 108 páginas: es esperado, se versionan todas (`git add public`), revisando antes con `git status --short | grep -v '\.html$'` que no haya nada ajeno.
- Reglas del dueño que ninguna línea nueva rompe (las prueban `test_reglas.py` y `test_consistencia.py`): nunca "Oasis"; nunca marcas de proveedor (PastoPlus); nunca el nombre del proveedor de la terminal en `public/`; solo "mensualidades con tarjeta de crédito" (nunca "MSI", "meses sin intereses" ni "sin intereses"); sin pádel ni canchas para sintético (campos deportivos con pasto natural o riego sí); sin muestras físicas; envío de sintético por rollo, nunca gratis; los 9 modelos de sintético en existencia nacional y "para llevar hoy" solo Toscana 18 y 28; el primer riego lo hace el cliente, dicho en positivo ("te enseñamos cómo"); nunca "pagas cuando ves…"; sin fechas de corte ni disponibilidad ("lote semanal", "cortado esta semana" y "próximo corte" están prohibidos); sin testimonios ni nombres inventados; ortografía "flamboyán" en texto nuevo. Copy obligatorio de 2a: H1 de la home "Pasto en rollo, jardines y plantas en Tampico y Madero."; promesa "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h"; "No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos un anticipo."; el pasto llega "una vez por semana, generalmente los viernes"; "Cortado para tu pedido"; "Si una sección no arraiga en 15 a 20 días, la reponemos sin costo", siempre ligada al protocolo de riego y a `/politicas`; "+500,000 m²"; "4.6 en Google (24 reseñas)" estático; clientes BMW, Taghleef Industries, Gobierno de Tampico, Grupo Velas, Velamar y Flex con nombre y logo.
- Dos textos de CTA y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008" (spec §4.3). La maqueta decía "Mandar esta etiqueta" en el Medidor; aquí también es "Cotizar por WhatsApp".

## Cobertura del spec y qué queda fuera

| Pide el spec | Dónde |
|---|---|
| §10 Etapa 2.1 Home: bifurcación, Medidor, hero con precio y CTA en el primer pantallazo móvil, CTA del hero al Medidor | Tareas 5, 8, 11 (`#medidor` desde la portada; prueba del primer pantallazo a 375 × 812) |
| §10 Etapa 2.2 Pasto en rollo: una sección de precio y una de proceso; garantía con reposición condicionada | Tareas 9, 11 |
| §3.3 Secuencias de Home y Servicio local | `plantillas/inicio.py`, `plantillas/servicio.py`; pruebas de secuencia en `test_inicio.py` y `test_pasto_en_rollo.py` |
| §4.1–4.3 Componentes (etiqueta, Medidor, cuadro de datos, FIG., NOSOTROS/TÚ, nota de campo, tabla con Unidad, FAQ con `<details>`, breadcrumb, CTA y promesa) | Tareas 4–6 |
| §4.3 Medidor: mayoreo bajo 500 m² calcula a $85 y lo avisa; fórmula de mensualidades oficial | Tarea 6 (casos de paridad Python ↔ JS) |
| §4.4 Una hoja de estilos; CSS viejo fuera de las páginas migradas | Tareas 4, 8, 9 (pruebas "sin CSS viejo ni Google Fonts") |
| §5.3 Voz: número antes que adjetivo, una nota de campo honesta por página, promesa única, riego en positivo, sin escasez inventada | Contenido de las Tareas 8 y 9; `test_reglas.py`, `test_consistencia.py` |
| §7.3 Una respuesta idéntica a "¿cuánto cuesta el pasto en rollo en Tampico?" | `datos.RESPUESTA_PRECIO_PASTO` (Tarea 2), usada en home y pasto en rollo |
| §8.3 Accesibilidad: un H1, labels en los controles, axe de página completa | Tarea 11 (axe de página completa a 375 y 1440) |
| §10 DoD: Lighthouse móvil ≥ 90 Perf, CLS < 0.1; axe 0 serias; un solo `terra.css`; cada CTA con plantilla y `data-cta`; cotizadores con los totales oficiales | Tareas 6, 11, 13 |
| Riesgo §10: pérdida de contenido al migrar | Tareas 1 y 10 (capturas y paridad) |

Fuera de 2a a propósito: títulos y descripciones nuevos (Etapa 3), grafo JSON-LD único y retiro del breadcrumb falso de la home (Etapa 4), fuentes con subset final, CSS crítico en línea y GA4 diferido (Etapa 5), `/empresas` y `/zonas` (Etapa 3: mientras tanto la home enlaza a `/mayoreo-pasto-tampico` y el pie a las 6 zonas). La meta de Accesibilidad de Lighthouse en esta verificación es ≥ 95 (la de ≥ 98 del spec se exige al cerrar la Etapa 2, cuando ya no quede CSS viejo).

## File structure

Se crean:

| Archivo | Responsabilidad única |
|---|---|
| `tools/site/paridad.py` | Congela lo que publicaba una página (`capturar`) y compara contra la página nueva (`comparar`, `informe`). |
| `tools/site/tests/paridad/index.json`, `tools/site/tests/paridad/pasto-en-rollo-tampico.json` | Capturas congeladas antes de migrar (las genera `paridad.py capturar`). |
| `tools/site/componentes.py` | Componentes del cuerpo como funciones puras (CTA, etiqueta, datos, figuras, tablas, proceso, garantía, FAQ, cierre, mensualidades, simulador, Medidor, portada). |
| `tools/site/plantillas/__init__.py`, `tools/site/plantillas/base.py` | Documento base: `<head>` propio, regiones del shell vacías, `<main>`, scripts. |
| `tools/site/plantillas/inicio.py` | Plantilla de la home. |
| `tools/site/plantillas/servicio.py` | Plantilla de servicio local (primera página: pasto en rollo; la reutilizan diseño, mantenimiento y riego en 2c). |
| `tools/site/contenido/__init__.py`, `tools/site/contenido/inicio.py`, `tools/site/contenido/pasto_en_rollo.py` | Contenido (`CONTENIDO`) y mapa de paridad (`PARIDAD`) de cada página. |
| `tools/site/generar.py` | Registro de páginas con plantilla; las escribe con el shell, solo si cambian. |
| `public/js/vt-medidor.js` | Medidor de m² en el navegador (sin precios propios; mensualidades de `VTMensualidades`). |
| `public/js/tests/vt-medidor.test.js`, `public/js/tests/casos-medidor.json` | Pruebas del Medidor y casos de paridad Python ↔ JS. |
| `public/img/obra/*.webp` (9) y `public/img/clientes/logo-*-c.webp` (6) | Fotos documentales y logos de clientes de la maqueta aprobada, a su tamaño. |
| `tools/site/tests/test_componentes.py`, `test_medidor_paridad.py`, `test_plantilla_base.py`, `test_inicio.py`, `test_pasto_en_rollo.py`, `test_generar.py`, `test_contenido.py`, `test_paridad.py`, `test_plantillas_navegador.py` | Pruebas de lo anterior. |

Se modifican:

| Archivo | Cambio |
|---|---|
| `tools/site/datos.py` | Precios de palma, tierra negra y tezontle; `ARRAIGO`, `LLEGADA_PASTO`, `ANTICIPO`, `VIGENCIA`, `RESPUESTA_PRECIO_PASTO`. |
| `tools/site/tests/test_datos.py` | Prueba de los datos nuevos. |
| `public/css/terra.css` | Tokens de escala (`--vt-text-h1…`, `--vt-space-section`) y componentes del cuerpo. |
| `tools/site/tests/test_terra_css.py` | Presupuesto con gzip, pares de contraste nuevos, clases del simulador acotadas a `.vt-sim`. |
| `tools/site/build.py` | Llama a `generar.escribir_todo(urls)`. |
| `tools/site/capturas.py` | Agrega el ancho 768. |
| `tools/servicios/pages.py`, `tools/servicios/simulador.py`, `tools/servicios/tests/test_pagos.py` | Pasto en rollo sale de los parches de `tools/servicios` (ya no inyectan portada ni simulador en una página con plantilla). |
| `public/index.html`, `public/pasto-en-rollo-tampico/index.html` | Regenerados por la plantilla. |
| 106 × `public/**/*.html`, `public/css/terra.<hash>.css` | Nuevo hash de `terra.css` en el `<head>` (build). |

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Crear el worktree desde `main` actualizado**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git worktree add ~/dev/viverosterra-e2a -b feat/etapa-2a
cd ~/dev/viverosterra-e2a && git log --oneline -1
```

Expected: el último commit de `main` (el que agrega este plan).

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/build.py | tail -1
git status --porcelain | wc -l
cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK"
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK"
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
```

Expected: `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 182 tests` + `OK`; `Ran 59 tests` + `OK`; `Ran 10 tests` + `OK`; `ℹ pass 29` y `ℹ fail 0`; `playwright ok` (si falta: `python3 -m pip install --user playwright==1.48.0 && python3 -m playwright install chromium`).

---

### Task 1: Capturas de paridad antes de migrar (`tools/site/paridad.py`)

**Files:**
- Create: `tools/site/paridad.py`, `tools/site/tests/test_paridad.py`, `tools/site/tests/paridad/index.json`, `tools/site/tests/paridad/pasto-en-rollo-tampico.json`

- [ ] **Step 1: Escribir la prueba de las funciones puras**

`tools/site/tests/test_paridad.py`:

```python
"""Paridad de contenido de las páginas migradas contra su captura anterior (tools/site/tests/paridad/*.json)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paridad  # noqa: E402


class ParidadTest(unittest.TestCase):
    def test_cubierto_y_faltantes(self):
        self.assertTrue(paridad.cubierto("Primer riego", ["Primer riego Tú"]))
        self.assertTrue(paridad.cubierto("Pasto Sintético", ["pasto sintético."]))
        self.assertFalse(paridad.cubierto("Riego", ["Riegos"]))
        mapa = {"reemplazos": {"A": "B"}, "retirados": {"C": "motivo largo y claro"}}
        self.assertEqual(paridad.faltantes(["A", "C", "D"], ["B"], mapa), ["D"])
        self.assertEqual(paridad.faltantes(["A"], [], mapa), ["A → B (el reemplazo no está en la página)"])

    def test_extraer(self):
        html = ('<title>T</title><meta name="description" content="D"><main><h2>¿Cuánto?</h2><p>$1,500 y $ 85</p>'
                '<details><summary>¿Pregunta?</summary></details><a href="/x/#a">x</a><a href="//cdn">y</a></main>')
        e = paridad.extraer(html)
        self.assertEqual((e["meta"]["title"], e["meta"]["description"]), ("T", "D"))
        self.assertEqual(e["encabezados"], ["¿Cuánto?"])
        self.assertEqual(e["faq"], ["¿Pregunta?"])
        self.assertEqual(e["precios"], ["$1,500", "$85"])
        self.assertEqual(e["enlaces"], ["/x"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrla y ver que falla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_paridad.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'paridad'` y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar `tools/site/paridad.py`**

```python
"""Paridad de contenido al migrar una página a su plantilla (Etapa 2).

Antes de migrar se congela lo que la página publicaba (`capturar`): meta (título, descripción, robots, canonical, Open
Graph), tipos del JSON-LD, encabezados h1–h3, preguntas frecuentes, precios y enlaces internos del <main>. Después,
tests/test_paridad.py exige que cada elemento siga en la página nueva o que el contenido diga a dónde fue
(PARIDAD["reemplazos"]) o por qué se retiró (PARIDAD["retirados"]).

Uso:
  python3 tools/site/paridad.py capturar /pasto-en-rollo-tampico   (congela tests/paridad/pasto-en-rollo-tampico.json)
  python3 tools/site/paridad.py informe /pasto-en-rollo-tampico    (lista lo que falta, para revisar a mano)
"""
import html as html_mod
import importlib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import paginas  # noqa: E402

CAPTURAS = AQUI / "tests" / "paridad"
CATEGORIAS = ("encabezados", "faq", "precios", "enlaces")


def texto(fragmento):
    s = re.sub(r"<(script|style|svg|template)\b.*?</\1>", " ", fragmento, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def principal(html):
    m = re.search(r"<main\b[^>]*>(.*)</main>", html, re.S)
    return m.group(1) if m else html


def _unicos(items):
    vistos, salida = set(), []
    for item in items:
        if item and item not in vistos:
            vistos.add(item)
            salida.append(item)
    return salida


def _recorrer(nodo, tipos, preguntas):
    if isinstance(nodo, dict):
        tipo = nodo.get("@type")
        tipos.update([tipo] if isinstance(tipo, str) else tipo or [])
        if tipo == "Question" and "name" in nodo:
            preguntas.append(nodo["name"].strip())
        for valor in nodo.values():
            _recorrer(valor, tipos, preguntas)
    elif isinstance(nodo, list):
        for valor in nodo:
            _recorrer(valor, tipos, preguntas)


def enlaces(fragmento):
    """Rutas internas enlazadas, sin consulta ni ancla y sin barra final."""
    return sorted({re.sub(r"[?#].*$", "", h).rstrip("/") or "/" for h in re.findall(r'href="(/(?!/)[^"]*)"', fragmento)})


def extraer(html):
    meta = {"title": "", "description": "", "robots": "", "canonical": ""}
    titulo = re.search(r"<title>(.*?)</title>", html, re.S)
    meta["title"] = html_mod.unescape(titulo.group(1).strip()) if titulo else ""
    for nombre in ("description", "robots"):
        m = re.search(rf'<meta name="{nombre}" content="([^"]*)"', html)
        meta[nombre] = html_mod.unescape(m.group(1)) if m else ""
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    meta["canonical"] = canonical.group(1) if canonical else ""
    for propiedad, valor in re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', html):
        meta[propiedad] = html_mod.unescape(valor)
    tipos, preguntas = set(), []
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        _recorrer(json.loads(bloque), tipos, preguntas)
    cuerpo = principal(html)
    encabezados = _unicos(texto(h) for _, h in re.findall(r"<(h[1-3])\b[^>]*>(.*?)</\1>", cuerpo, re.S))
    visibles = [texto(s) for s in re.findall(r"<summary\b[^>]*>(.*?)</summary>", cuerpo, re.S)]
    visibles += [texto(b) for b in re.findall(r'<button\b[^>]*class="[^"]*faq-btn[^"]*"[^>]*>(.*?)</button>', cuerpo, re.S)]
    precios = sorted({p.replace(" ", "") for p in re.findall(r"\$\s?\d[\d,]*", texto(cuerpo))})
    return {"meta": meta, "jsonld_tipos": sorted(tipos), "encabezados": encabezados,
            "faq": _unicos(preguntas + visibles), "precios": precios, "enlaces": enlaces(cuerpo)}


def normalizar(t):
    t = re.sub(r"[\"“”«»]", "", t)
    return re.sub(r"\s+", " ", t).strip().rstrip(".").casefold()


def cubierto(viejo, nuevos):
    """El elemento viejo sigue igual (sin importar mayúsculas, comillas ni el punto final) o como inicio de uno nuevo
    ("Primer riego" cubre "Primer riego Tú", el encabezado con su marcador)."""
    v = normalizar(viejo)
    return any(n == v or n.startswith(v + " ") for n in map(normalizar, nuevos))


def faltantes(viejos, nuevos, mapa):
    """Elementos de la captura que no están en la página nueva ni tienen reemplazo vigente o motivo de retiro."""
    salida = []
    for viejo in viejos:
        if cubierto(viejo, nuevos):
            continue
        if viejo in mapa["reemplazos"]:
            if not cubierto(mapa["reemplazos"][viejo], nuevos):
                salida.append(f"{viejo} → {mapa['reemplazos'][viejo]} (el reemplazo no está en la página)")
            continue
        if not mapa["retirados"].get(viejo):
            salida.append(viejo)
    return salida


def nombre_captura(ruta):
    return "index" if ruta == "/" else ruta.strip("/").replace("/", "_")


def archivo(ruta, public=paginas.PUBLIC):
    for candidato in (Path(public) / ruta.strip("/") / "index.html", Path(public) / f"{ruta.strip('/')}.html"):
        if candidato.is_file():
            return candidato
    raise FileNotFoundError(ruta)


def capturar(ruta, public=paginas.PUBLIC, destino=CAPTURAS):
    datos = extraer(archivo(ruta, public).read_text(encoding="utf-8"))
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / f"{nombre_captura(ruta)}.json"
    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return salida


def comparar(ruta, mapa, public=paginas.PUBLIC, capturas=CAPTURAS):
    """Diccionario categoría → lista de faltantes (vacío si todo está cubierto). Los enlaces nuevos se buscan en toda la
    página (el menú y el pie también enlazan)."""
    viejo = json.loads((Path(capturas) / f"{nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
    html = archivo(ruta, public).read_text(encoding="utf-8")
    nuevo = extraer(html)
    nuevo["enlaces"] = enlaces(html)
    resultado = {c: faltantes(viejo[c], nuevo[c], mapa) for c in CATEGORIAS}
    resultado["meta"] = [f"{k}: {v!r} → {nuevo['meta'].get(k)!r}" for k, v in viejo["meta"].items()
                         if nuevo["meta"].get(k) != v]
    resultado["jsonld_tipos"] = sorted(set(viejo["jsonld_tipos"]) - set(nuevo["jsonld_tipos"]))
    return resultado


def main(argv):
    if len(argv) != 3 or argv[1] not in ("capturar", "informe"):
        raise SystemExit("Uso: python3 tools/site/paridad.py capturar|informe <ruta>")
    ruta = argv[2]
    if argv[1] == "capturar":
        print(f"captura: {capturar(ruta).relative_to(AQUI.parents[1])}")
        return
    import generar  # noqa: E402  (solo aquí: generar importa las plantillas)
    modulo = importlib.import_module(f"contenido.{generar.contenido_de(ruta)}")
    for categoria, lista in comparar(ruta, modulo.PARIDAD).items():
        print(f"{categoria}: {'ok' if not lista else ''}")
        for item in lista:
            print(f"  - {item}")


if __name__ == "__main__":
    main(sys.argv)
```

- [ ] **Step 4: Correr la prueba**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_paridad.py -v 2>&1 | tail -3`
Expected: `Ran 2 tests` y `OK`.

- [ ] **Step 5: Congelar las dos páginas tal como están publicadas hoy**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/paridad.py capturar /
python3 tools/site/paridad.py capturar /pasto-en-rollo-tampico
python3 -c "import json; d=json.load(open('tools/site/tests/paridad/index.json')); print(len(d['encabezados']), len(d['faq']), d['precios'], len(d['enlaces']))"
python3 -c "import json; d=json.load(open('tools/site/tests/paridad/pasto-en-rollo-tampico.json')); print(len(d['encabezados']), len(d['faq']), d['precios'], len(d['enlaces']))"
```

Expected: `captura: tools/site/tests/paridad/index.json` y `captura: tools/site/tests/paridad/pasto-en-rollo-tampico.json`; luego `44 8 ['$0', '$1,500', '$120', '$200', '$3,000', '$60', '$750', '$85', '$90'] 25` y `36 10 ['$1,500', '$120', '$2,000', '$385', '$60', '$750', '$85', '$90'] 9`. Si los números no coinciden, `main` cambió después de escribir este plan: ajusta en las Tareas 8 y 9 las entradas de `PARIDAD` que `paridad.py informe` reporte, nunca la captura.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/paridad.py tools/site/tests/test_paridad.py tools/site/tests/paridad/index.json tools/site/tests/paridad/pasto-en-rollo-tampico.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de la home y pasto en rollo antes de migrarlas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Datos nuevos en `datos.py`

**Files:**
- Modify: `tools/site/datos.py`, `tools/site/tests/test_datos.py`

- [ ] **Step 1: Escribir la prueba**

En `tools/site/tests/test_datos.py`, agrega este método a `DatosTest` justo antes de `test_mensajes_terminan_con_la_firma`:

```python
    def test_datos_de_las_plantillas_etapa_2a(self):
        p = datos.PRECIOS
        self.assertEqual((p["palma_desde"], p["tierra_negra_costal"], p["tierra_negra_m3"], p["tezontle_costal"]),
                         (250, 90, 1500, 200))
        self.assertEqual(datos.LLEGADA_PASTO, "una vez por semana, generalmente los viernes")
        self.assertTrue(datos.ANTICIPO.startswith("No pedimos el 100% por adelantado: para confirmar tu pedido o "
                                                  "agendar el servicio solicitamos un anticipo"))
        self.assertEqual(datos.ARRAIGO, "15 a 20 días")
        for cifra in ("$85 por m²", "desde $120 por m²", "500 m²", "$60/m²", "noviembre de 2026"):
            self.assertIn(cifra, datos.RESPUESTA_PRECIO_PASTO)
```

- [ ] **Step 2: Correrla y ver que falla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_datos.py 2>&1 | tail -3`
Expected: `KeyError: 'palma_desde'` y `FAILED (errors=1)`.

- [ ] **Step 3: Agregar los datos**

En `tools/site/datos.py`, reemplaza:

```python
    "flamboyan": 250,
}
```

por:

```python
    "flamboyan": 250,
    "palma_desde": 250,
    "tierra_negra_costal": 90,
    "tierra_negra_m3": 1500,
    "tezontle_costal": 200,
}
```

y, justo después de la línea `PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."`, agrega:

```python
ARRAIGO = "15 a 20 días"
LLEGADA_PASTO = "una vez por semana, generalmente los viernes"
ANTICIPO = ("No pedimos el 100% por adelantado: para confirmar tu pedido o agendar el servicio solicitamos "
            "un anticipo.")
VIGENCIA = f"noviembre de {ANIO}"
# Una sola respuesta a "¿cuánto cuesta el pasto en rollo en Tampico?" en home, servicio y precios (spec §7.3).
RESPUESTA_PRECIO_PASTO = (
    f"En Viveros Terra el pasto San Agustín en rollo cuesta ${PRECIOS['pasto_solo_m2']} por m² solo el pasto y desde "
    f"${PRECIOS['pasto_instalado_m2']} por m² instalado, con IVA incluido. El instalado incluye la preparación básica "
    f"del terreno, la colocación y una garantía de arraigo de {ARRAIGO}. En pedidos de "
    f"{PRECIOS['pasto_mayoreo_minimo_m2']} m² o más, el mayoreo cuesta desde ${PRECIOS['pasto_mayoreo_m2']}/m². "
    f"Precios vigentes en {VIGENCIA} para Tampico, Ciudad Madero y Altamira."
)
```

(Es, palabra por palabra, la respuesta que hoy publica la home en su JSON-LD; `test_consistencia.test_home_con_cifras_oficiales` la sigue encontrando.)

- [ ] **Step 4: Correr la prueba**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_datos.py 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/datos.py tools/site/tests/test_datos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(datos): respuesta única de precio de pasto, anticipo, llegada semanal y precios de materiales" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Fotos documentales y logos de clientes

**Files:**
- Create: `public/img/obra/*.webp` (9), `public/img/clientes/logo-*-c.webp` (6)

Son las versiones ya recortadas y optimizadas de la maqueta aprobada (`docs/diseno/hibrido/img/`), con nombres descriptivos. Las fotos llevan pie `FIG.` en la página; la del jardín residencial es la que el jurado marcó como "la que más huele a render" y se sustituye con la sesión de fotos real (ver riesgos).

- [ ] **Step 1: Copiar**

```bash
cd ~/dev/viverosterra-e2a
H=docs/diseno/hibrido/img; O=public/img/obra; mkdir -p $O
cp $H/cuadrilla-rollos.webp $O/cuadrilla-tendiendo-pasto-san-agustin.webp
cp $H/cuadrilla-640.webp $O/cuadrilla-tendiendo-pasto-san-agustin-640.webp
cp $H/rollos-camioneta.webp $O/rollos-pasto-san-agustin-camioneta.webp
cp $H/jardin-residencial.webp $O/jardin-residencial-pasto-san-agustin.webp
cp $H/despues.webp $O/pasto-san-agustin-recien-instalado.webp
cp $H/riego-equipo.webp $O/instalacion-tuberia-riego-jardin.webp
cp $H/palmas.webp $O/palmas-en-costal-vivero.webp
cp $H/riego-borde.webp $O/riego-aspersor-borde-pasto.webp
cp $H/mantenimiento.webp $O/mantenimiento-jardin-poda-tampico.webp
for l in bmw taghleef gobierno-tampico grupo-velas velamar flex; do cp $H/logo-$l-c.webp public/img/clientes/logo-$l-c.webp; done
ls $O | wc -l; ls public/img/clientes/*-c.webp | wc -l
python3 -c "
from pathlib import Path
import struct
for p in sorted(Path('public/img/obra').glob('*.webp')): print(p.name, p.stat().st_size // 1024, 'KB')"
```

Expected: `9`; `6`; nueve líneas, ninguna mayor de 180 KB.

- [ ] **Step 2: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add public/img/obra public/img/clientes/logo-bmw-c.webp public/img/clientes/logo-taghleef-c.webp public/img/clientes/logo-gobierno-tampico-c.webp public/img/clientes/logo-grupo-velas-c.webp public/img/clientes/logo-velamar-c.webp public/img/clientes/logo-flex-c.webp
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(img): fotos de obra y logos de clientes de la maqueta aprobada" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Componentes del cuerpo en `terra.css`

**Files:**
- Modify: `public/css/terra.css`, `tools/site/tests/test_terra_css.py`

- [ ] **Step 1: Ajustar la prueba (presupuesto con gzip, contraste de los pares nuevos, clases del simulador)**

En `tools/site/tests/test_terra_css.py`:

1. Cambia la primera línea `import re` por:

```python
import gzip
import re
```

2. Debajo de `CSS_VIEJOS = (…)` agrega:

```python
# Clases que crea public/js/vt-simulador.js (las mismas en servicios.css). En terra.css solo aparecen bajo .vt-sim, que
# ninguna página vieja tiene, así que no pueden alterar el simulador viejo.
CLASES_DEL_SIMULADOR = {"sim-plan", "sim-plan__name", "sim-plan__amt", "sim-plan__sep", "sim-plan__more", "is-selected",
                        "is-disabled"}
```

3. En `test_contraste_aa_por_par_de_tokens`, reemplaza `("--vt-tag-ink", "--vt-tag"), ("--vt-field-deep", "--vt-field-100")]` por:

```python
                 ("--vt-tag-ink", "--vt-tag"), ("--vt-field-deep", "--vt-field-100"),
                 # componentes del cuerpo (Etapa 2)
                 ("--vt-soil", "--vt-bone"), ("--vt-soil", "--vt-bone-2"), ("--vt-soil", "--vt-card"),
                 ("--vt-muted", "--vt-bone-2"), ("--vt-ink-2", "--vt-bone-2"), ("--vt-card", "--vt-soil"),
                 ("--vt-on-dark-2", "--vt-field-deep"), ("--vt-tag", "--vt-field-deep"), ("--vt-ink", "--vt-field-100")]
```

4. Reemplaza `test_presupuesto` completo por:

```python
    def test_presupuesto(self):
        # Spec §8.2: meta de 10 KB con gzip. Desde la Etapa 2 terra.css también trae los componentes del cuerpo y
        # sustituye, en cada página migrada, ~70 KB de CSS viejo (tailwind, design-system, servicios y <style>).
        datos = self.css.encode("utf-8")
        self.assertLess(len(gzip.compress(datos, mtime=0)), 10 * 1024)
        self.assertLess(len(datos), 48 * 1024)
```

5. En `test_clases_del_shell_no_chocan_con_las_viejas`, reemplaza la última línea `self.assertEqual(sorted(clases(self.css) & viejas), [])` por:

```python
        self.assertEqual(sorted((clases(self.css) - CLASES_DEL_SIMULADOR) & viejas), [])
        for regla in re.findall(r"([^{}]+)\{", sin_comentarios(self.css)):
            if re.search(r"\.(?:sim-plan|is-selected|is-disabled)\b", regla):
                with self.subTest(selector=regla.strip()):
                    self.assertTrue(all(".vt-sim " in parte for parte in regla.split(",")))
```

Agrega además esta prueba nueva al final de `TerraCssTest`:

```python
    def test_componentes_del_cuerpo_presentes(self):
        for selector in (".vt-pagina", ".vt-portada", ".vt-etiqueta", ".vt-datos", ".vt-medidor", ".vt-tabla",
                         ".vt-pasos", ".vt-nota", ".vt-faq summary", ".vt-cierre", ".vt-sim .sim-plan"):
            with self.subTest(selector=selector):
                self.regla(selector)
        for token in ("--vt-text-h1", "--vt-text-h2", "--vt-text-h3", "--vt-text-precio", "--vt-space-section"):
            self.assertIn(token, tokens(self.css))
```

- [ ] **Step 2: Correrla y ver que falla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_terra_css.py 2>&1 | tail -3`
Expected: `FAILED (failures=12)`: los 11 selectores de `test_componentes_del_cuerpo_presentes` y su primer token no existen todavía; el resto pasa.

- [ ] **Step 3: Tokens de escala**

En `public/css/terra.css`, dentro de `:root`, reemplaza la línea:

```css
  --vt-text-lg:clamp(1.125rem,1.05rem + .35vw,1.3125rem); --vt-text-menu:1.5rem; --vt-text-dato:1.1875rem;
```

por:

```css
  --vt-text-lg:clamp(1.125rem,1.05rem + .35vw,1.3125rem); --vt-text-menu:1.5rem; --vt-text-dato:1.1875rem;
  --vt-text-h3:clamp(1.25rem,1.1rem + .6vw,1.625rem); --vt-text-h2:clamp(2rem,1.35rem + 2.6vw,3.5rem);
  --vt-text-h1:clamp(2.5rem,1.45rem + 4.2vw,5.25rem); --vt-text-precio:clamp(2.75rem,2rem + 3vw,4.25rem);
  --vt-space-section:clamp(3.5rem,2.4rem + 4.4vw,7.5rem);
```

- [ ] **Step 4: Componentes del cuerpo**

Agrega al final de `public/css/terra.css` (después del bloque `@media (prefers-reduced-motion:reduce){…}` del shell):

```css
/* =========================================================
   Etapa 2 · componentes del cuerpo (páginas que salen de tools/site/plantillas/)
   Solo aplican dentro de <body class="vt-pagina">: las páginas viejas no cargan nada de esto.
   ========================================================= */
.vt-pagina{margin:0;background:var(--vt-bone);color:var(--vt-ink);font:400 var(--vt-text-base)/1.55 var(--vt-font-sans);-webkit-text-size-adjust:100%;overflow-x:clip}
.vt-pagina *,.vt-pagina *::before,.vt-pagina *::after{box-sizing:border-box}
.vt-pagina img{display:block;max-width:100%;height:auto}
.vt-pagina main a:not(.vt-btn){color:var(--vt-field);text-underline-offset:3px;text-decoration-thickness:1px}
.vt-pagina main a:not(.vt-btn):hover{color:var(--vt-field-deep)}
.vt-pagina main :focus-visible{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-pagina main h1,.vt-pagina main h2,.vt-pagina main h3{margin:0;font-weight:800;line-height:1.02;letter-spacing:-.012em;font-variation-settings:"wdth" var(--vt-wdth-tight);text-wrap:balance}
.vt-pagina main p{margin:0 0 1em}
.vt-pagina main ul,.vt-pagina main ol{margin:0;padding:0}
.vt-serif{font-family:var(--vt-font-serif);font-style:italic;font-weight:400;font-variation-settings:normal;letter-spacing:0}
.vt-lede{max-width:58ch;font-size:var(--vt-text-lg);color:var(--vt-ink-2)}
.vt-btn--linea{background:transparent;color:var(--vt-ink);border-color:var(--vt-ink)}
.vt-btn--linea:hover{background:var(--vt-ink);color:var(--vt-on-dark)}
.vt-ico{flex:none;width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.vt-flecha{transition:transform var(--vt-duration-fast)}
.vt-btn:hover .vt-flecha{transform:translateX(3px)}
.vt-cta{display:flex;flex-wrap:wrap;gap:10px;min-height:106px;align-content:flex-start}
.vt-cta .vt-btn{flex:1 1 240px;min-height:52px}
.vt-promesa{margin:12px 0 0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-pagina main .vt-mt{margin-top:48px}
.vt-precio-marca{padding:0 .22em;background:linear-gradient(transparent 12%,var(--vt-tag) 12%,var(--vt-tag) 92%,transparent 92%);color:var(--vt-tag-ink);font-weight:800;font-variant-numeric:tabular-nums}
@media (min-width:560px){.vt-cta{min-height:52px}}

/* ---------- secciones numeradas ---------- */
.vt-bloque{padding-block:var(--vt-space-section);border-top:1px solid var(--vt-line)}
.vt-bloque--tinte{background:var(--vt-bone-2)}
.vt-bloque__no{display:flex;align-items:center;gap:12px;margin:0 0 18px;font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
.vt-bloque__no b{font-size:15px;letter-spacing:0;color:var(--vt-ink);font-variant-numeric:tabular-nums}
.vt-bloque__no::after{content:"";flex:1;height:1px;background:var(--vt-line-strong)}
.vt-bloque__cabeza{display:grid;gap:14px;margin-bottom:clamp(2rem,1.4rem + 2vw,3.25rem)}
.vt-pagina main .vt-bloque__cabeza h2,.vt-pagina main .vt-dos h2,.vt-pagina main .vt-cierre h2{font-size:var(--vt-text-h2)}
.vt-pagina main .vt-bloque h3{font-size:var(--vt-text-h3)}
.vt-bloque__cabeza .vt-lede{margin:0}
.vt-dos{display:grid;gap:32px}
@media (min-width:1024px){.vt-bloque__cabeza{grid-template-columns:7fr 5fr;gap:48px;align-items:end}.vt-dos{grid-template-columns:5fr 7fr;gap:56px;align-items:start}}

/* ---------- portada ---------- */
.vt-portada{padding-block:22px 0}
.vt-portada__grid{display:grid;gap:28px}
.vt-kicker{margin:0 0 10px;font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-soil)}
.vt-pagina main .vt-portada h1{font-size:var(--vt-text-h1);line-height:.95;letter-spacing:-.018em}
.vt-portada h1 .vt-serif{display:block;margin-top:.18em;font-size:.6em;line-height:1.15;color:var(--vt-field)}
.vt-portada .vt-lede{margin:14px 0 0}
.vt-portada__trato{display:grid;gap:18px;margin-top:18px}
.vt-portada__tambien{margin:14px 0 0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-pagina main .vt-portada__tambien a{color:var(--vt-ink-2)}
.vt-portada__foto .vt-fig__marco{aspect-ratio:4/3}
.vt-portada .vt-datos{margin-top:28px}
.vt-portada .vt-crumbs{margin:-22px calc(var(--vt-gutter) * -1) 16px;background:transparent}
@media (min-width:1024px){
  .vt-portada{padding-top:48px}
  .vt-portada__grid{grid-template-columns:7fr 5fr;gap:48px;align-items:start}
  .vt-portada__trato{grid-template-columns:290px minmax(0,1fr);gap:32px;margin-top:44px}
  .vt-portada__trato .vt-cta{flex-direction:column;min-height:0}
  .vt-portada__trato .vt-cta .vt-btn{flex:0 0 auto}
  .vt-portada__foto .vt-fig__marco{aspect-ratio:4/5}
  .vt-portada .vt-crumbs{margin-top:-48px}
}

/* ---------- etiqueta de precio (objeto de marca: siempre derecha, solo con precio) ---------- */
.vt-etiqueta{position:relative;width:min(340px,100%);padding:40px 20px 18px;border:1px solid var(--vt-line-strong);border-radius:var(--vt-radius-tag);background:var(--vt-card);box-shadow:0 12px 24px -18px var(--vt-scrim)}
.vt-etiqueta::before{content:"";position:absolute;left:50%;top:13px;width:14px;height:14px;transform:translateX(-50%);border-radius:50%;border:2px solid var(--vt-line-strong);background:var(--vt-bone)}
.vt-etiqueta__cod{display:flex;justify-content:space-between;gap:8px;margin:0 0 8px;font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
.vt-pagina main .vt-etiqueta p{margin:0}
.vt-etiqueta__nombre{font-size:22px;font-weight:800;line-height:1.05;font-variation-settings:"wdth" var(--vt-wdth-mid)}
.vt-pagina main .vt-etiqueta__sci{margin-top:2px;font-family:var(--vt-font-serif);font-style:italic;font-size:15px;color:var(--vt-ink-2)}
.vt-pagina main .vt-etiqueta__precio{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 .3em;margin:14px -20px 0;padding:10px 20px 11px;background:var(--vt-tag);color:var(--vt-tag-ink);font-weight:800;font-variant-numeric:tabular-nums;line-height:1}
.vt-etiqueta__precio small{flex-basis:100%;margin-bottom:4px;font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.vt-etiqueta__precio b{font-size:var(--vt-text-precio);letter-spacing:-.02em;font-variation-settings:"wdth" 80}
.vt-etiqueta__precio span{font-size:16px;font-weight:600}
.vt-pagina main .vt-etiqueta__fila{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:9px 0;border-bottom:1px dashed var(--vt-line-strong);font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-etiqueta__fila b{color:var(--vt-ink);font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.vt-etiqueta__fila:last-of-type{border-bottom:0}
.vt-pagina main .vt-etiqueta__nota{margin-top:10px;font-size:var(--vt-text-xs);line-height:1.45;color:var(--vt-muted)}
@media (max-width:1023px){
  .vt-portada .vt-etiqueta{padding:14px 16px 12px 46px}
  .vt-portada .vt-etiqueta::before{left:22px;top:19px;transform:none;width:16px;height:16px}
  .vt-pagina main .vt-portada .vt-etiqueta__precio{margin:8px -16px 0 -46px;padding:8px 16px 9px 46px}
  .vt-portada .vt-etiqueta__precio b{font-size:34px}
  .vt-portada .vt-etiqueta__nombre,.vt-pagina main .vt-portada .vt-etiqueta__sci,.vt-pagina main .vt-portada .vt-etiqueta__nota{display:none}
}

/* ---------- cuadro de datos ---------- */
.vt-datos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));margin:0;border:1px solid var(--vt-ink);background:var(--vt-card)}
.vt-datos>div{min-width:0;padding:12px 14px;border-right:1px solid var(--vt-line);border-bottom:1px solid var(--vt-line)}
.vt-datos>div:nth-child(2n){border-right:0}
.vt-datos dt{font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-muted)}
.vt-datos dd{margin:4px 0 0;font-size:var(--vt-text-dato);font-weight:800;line-height:1.1;font-variation-settings:"wdth" var(--vt-wdth-mid);font-variant-numeric:tabular-nums}
.vt-datos dd small{display:block;margin-top:3px;font-size:var(--vt-text-xs);font-weight:400;color:var(--vt-muted);font-variation-settings:"wdth" 100}
@media (min-width:900px){.vt-datos{grid-template-columns:repeat(6,minmax(0,1fr))}.vt-datos>div{border-bottom:0}.vt-datos>div:nth-child(2n){border-right:1px solid var(--vt-line)}.vt-datos>div:last-child{border-right:0}}

/* ---------- figura documental: FIG. 0X · lugar · etapa ---------- */
.vt-fig{margin:0}
.vt-fig__marco{position:relative;overflow:hidden;border:1px solid var(--vt-line);background:var(--vt-bone-2)}
.vt-pagina .vt-fig__marco img{width:100%;height:100%;object-fit:cover}
.vt-fig figcaption{display:flex;flex-wrap:wrap;justify-content:space-between;gap:2px 10px;padding-top:8px;font-size:var(--vt-text-xs);font-weight:500;letter-spacing:.02em;color:var(--vt-muted)}
.vt-fig figcaption b{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--vt-ink)}
.vt-obras{display:grid;gap:20px}
.vt-obras .vt-fig__marco{aspect-ratio:4/3}
.vt-obras>:first-child .vt-fig__marco{aspect-ratio:16/9}
@media (min-width:900px){
  .vt-obras{grid-template-columns:repeat(6,minmax(0,1fr));gap:24px}
  .vt-obras>*{grid-column:span 2}
  .vt-obras>:first-child{grid-column:span 4}
  .vt-obras>:first-child .vt-fig__marco,.vt-obras>:nth-child(2) .vt-fig__marco{aspect-ratio:auto;height:420px}
}
.vt-prueba{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:28px;padding-top:20px;border-top:1px solid var(--vt-line);font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-prueba b{color:var(--vt-ink)}
.vt-logos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:24px;list-style:none;border-top:1px solid var(--vt-line);border-left:1px solid var(--vt-line)}
.vt-logos li{display:grid;place-items:center;height:84px;padding:14px;border-right:1px solid var(--vt-line);border-bottom:1px solid var(--vt-line);background:var(--vt-card)}
.vt-pagina .vt-logos img{width:auto;max-height:34px;filter:grayscale(1)}
@media (min-width:900px){.vt-logos{grid-template-columns:repeat(6,minmax(0,1fr))}.vt-pagina .vt-logos img{max-height:40px}}

/* ---------- índice de servicios con su precio ---------- */
.vt-indice{list-style:none;border-top:1px solid var(--vt-ink)}
.vt-indice li{display:grid;grid-template-columns:72px minmax(0,1fr);gap:4px 16px;align-items:center;padding:16px 0;border-bottom:1px solid var(--vt-line)}
.vt-pagina .vt-indice img{grid-row:1 / span 3;width:72px;height:90px;object-fit:cover;border:1px solid var(--vt-line)}
.vt-pagina main .vt-indice h3 a{color:var(--vt-ink);text-decoration:none}
.vt-pagina main .vt-indice h3 a:hover{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
.vt-pagina main .vt-indice p{margin:0;font-size:var(--vt-text-sm);line-height:1.45;color:var(--vt-ink-2)}
.vt-indice__desde{grid-column:2}
.vt-indice__desde .vt-pagina main .vt-mt{margin-top:48px}
.vt-precio-marca{font-size:20px}
@media (min-width:900px){
  .vt-indice li{grid-template-columns:120px minmax(0,1.1fr) minmax(0,1.3fr) 190px;gap:24px;padding:20px 0}
  .vt-pagina .vt-indice img{grid-row:auto;width:120px;height:80px}
  .vt-indice__desde{grid-column:auto;text-align:right}
}

/* ---------- Medidor de m² (largo × ancho → m² → precio en la etiqueta → WhatsApp) ---------- */
.vt-medidor{display:grid;gap:24px}
.vt-medidor__form{display:grid;gap:16px;align-content:start}
.vt-medidor__medidas{display:grid;grid-template-columns:1fr auto 1fr;align-items:end;gap:10px}
.vt-medidor__x{padding-bottom:14px;font-size:22px;font-weight:700;color:var(--vt-soil)}
.vt-campo{display:grid;gap:6px;min-width:0}
.vt-campo>label,.vt-opciones legend{font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-ink)}
.vt-control{display:flex;align-items:center;min-height:52px;border:1.5px solid var(--vt-ink);border-radius:var(--vt-radius);background:var(--vt-card)}
.vt-control:focus-within{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-control input{flex:1;width:100%;min-width:0;height:50px;padding:0 12px;border:0;background:transparent;font:700 20px var(--vt-font-sans);font-variant-numeric:tabular-nums;color:var(--vt-ink)}
.vt-control input:focus{outline:none}
.vt-control input[type="text"]{font-size:16px;font-weight:500}
.vt-control span{padding-right:12px;font-weight:700;color:var(--vt-soil)}
.vt-opciones{display:grid;gap:8px;margin:0;padding:0;border:0}
.vt-opciones label{position:relative;display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:48px;padding:10px 14px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);font-size:15px;font-weight:600;cursor:pointer}
.vt-opciones small{font-weight:700;font-variant-numeric:tabular-nums;color:var(--vt-ink-2)}
.vt-opciones input{position:absolute;opacity:0;pointer-events:none}
.vt-opciones label:has(input:checked){border-color:var(--vt-field);background:var(--vt-field-100);box-shadow:inset 0 0 0 1px var(--vt-field)}
.vt-opciones label:has(input:focus-visible){outline:2px solid var(--vt-field);outline-offset:2px}
.vt-medidor__plano{padding:14px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-pagina .vt-medidor__plano svg{display:block;width:100%;height:auto}
.vt-plano-relleno{fill:var(--vt-field-100)}
.vt-plano-borde{fill:none;stroke:var(--vt-ink);stroke-width:1.5}
.vt-cota{fill:none;stroke:var(--vt-soil);stroke-width:1.2}
.vt-cota-t{fill:var(--vt-soil);font:700 15px var(--vt-font-sans);font-variant-numeric:tabular-nums}
.vt-cota-a{fill:var(--vt-soil);font:800 26px var(--vt-font-sans)}
.vt-pagina main .vt-medidor__aviso{padding:10px 12px;border-left:3px solid var(--vt-soil);background:var(--vt-bone-2);font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-soil)}
.vt-medidor__aviso[hidden]{display:none}
.vt-pagina main .vt-medidor__calc,.vt-pagina main .vt-medidor__plan{margin-top:8px;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-medidor .vt-btn{width:100%;margin-top:14px}
.vt-medidor .vt-etiqueta{width:100%}
@media (min-width:1024px){.vt-medidor{grid-template-columns:4fr 4fr 4fr;gap:32px;align-items:start}}

/* ---------- precios con columna Unidad y mensualidades ---------- */
.vt-tabla{width:100%;border-collapse:collapse;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tabla th,.vt-tabla td{padding:14px 16px;border-bottom:1px solid var(--vt-line);text-align:left;vertical-align:top}
.vt-tabla thead th{background:var(--vt-bone-2);font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-muted)}
.vt-tabla tbody th{font-weight:400}
.vt-tabla tbody th b{display:block;font-size:17px;font-weight:700}
.vt-tabla tbody th span{display:block;margin-top:2px;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-tabla__u{white-space:nowrap;font-size:var(--vt-text-sm);font-weight:700;color:var(--vt-soil)}
.vt-tabla__p{text-align:right;white-space:nowrap;font-size:22px;font-weight:800;font-variant-numeric:tabular-nums}
.vt-tabla .vt-tabla__p{text-align:right}
.vt-tabla__p small{display:block;font-size:var(--vt-text-xs);font-weight:500;color:var(--vt-muted)}
.vt-tabla__rec .vt-tabla__p span{padding:2px 6px;background:var(--vt-tag);color:var(--vt-tag-ink)}
.vt-tabla caption{caption-side:bottom;padding-top:10px;text-align:left;font-size:var(--vt-text-xs);color:var(--vt-muted)}
@media (max-width:640px){
  .vt-tabla--precios thead{display:none}
  .vt-tabla--precios tr{display:grid;grid-template-columns:1fr auto;border-bottom:1px solid var(--vt-line)}
  .vt-tabla--precios th,.vt-tabla--precios td{border:0}
  .vt-tabla--precios tbody th{grid-column:1 / -1;padding-bottom:4px}
  .vt-tabla--precios .vt-tabla__p{padding-top:0}
}
.vt-desliza{overflow-x:auto}
.vt-planes{margin-top:24px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-planes__cabeza{display:grid;gap:4px;padding:14px 16px;border-bottom:1px solid var(--vt-line)}
.vt-planes__cabeza span,.vt-planes dd{font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-planes dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));margin:0}
.vt-planes dl>div{padding:12px 16px;border-right:1px solid var(--vt-line);border-bottom:1px solid var(--vt-line)}
.vt-planes dl>div:nth-child(2n){border-right:0}
.vt-planes dt{font-weight:700}
.vt-planes dd{margin:2px 0 0;font-variant-numeric:tabular-nums}
.vt-pagina main .vt-planes p{margin:0;padding:12px 16px;font-size:var(--vt-text-xs);color:var(--vt-muted)}
@media (min-width:768px){.vt-planes dl{grid-template-columns:repeat(4,minmax(0,1fr))}.vt-planes dl>div,.vt-planes dl>div:nth-child(2n){border-right:1px solid var(--vt-line);border-bottom:0}.vt-planes dl>div:last-child{border-right:0}}
.vt-sim{margin-top:24px;padding:20px 16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-sim .vt-control{max-width:280px}
.vt-sim__lista{display:grid;gap:8px;margin:16px 0}
.vt-sim .sim-plan{display:grid;grid-template-columns:20px minmax(0,1fr);gap:2px 10px;align-items:center;padding:12px 14px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);cursor:pointer}
.vt-sim .sim-plan input{grid-row:span 2;margin:0;accent-color:var(--vt-field)}
.vt-sim .sim-plan__name{font-weight:600}
.vt-sim .sim-plan__amt{font-size:var(--vt-text-sm);color:var(--vt-ink-2);font-variant-numeric:tabular-nums}
.vt-sim .sim-plan__sep{display:none}
.vt-sim .sim-plan__more{display:block;color:var(--vt-muted)}
.vt-sim .sim-plan.is-selected{border-color:var(--vt-field);background:var(--vt-field-100)}
.vt-sim .sim-plan.is-disabled{opacity:.55;cursor:not-allowed}

/* ---------- proceso NOSOTROS / TÚ / JUNTOS ---------- */
.vt-pasos{counter-reset:paso;display:grid;list-style:none;border-top:1px solid var(--vt-ink)}
.vt-pasos li{counter-increment:paso;display:grid;grid-template-columns:44px minmax(0,1fr);gap:4px 14px;padding:18px 0;border-bottom:1px solid var(--vt-line)}
.vt-pasos li::before{content:counter(paso,decimal-leading-zero);grid-row:1 / span 3;font-size:24px;font-weight:800;font-variant-numeric:tabular-nums;font-variation-settings:"wdth" var(--vt-wdth-tight)}
.vt-pagina main .vt-pasos h3{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.vt-pagina main .vt-pasos p{margin:0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-pagina main .vt-pasos .vt-pasos__cuando{font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.04em;color:var(--vt-soil)}
.vt-quien{display:inline-block;padding:3px 8px 2px;border-radius:var(--vt-radius);background:var(--vt-field);color:var(--vt-card);font-size:12px;font-weight:700;line-height:1.3;letter-spacing:.12em;text-transform:uppercase;font-variation-settings:"wdth" 100}
.vt-quien--tu{background:var(--vt-soil)}
.vt-quien--juntos{background:var(--vt-card);color:var(--vt-ink);box-shadow:inset 0 0 0 1.5px var(--vt-ink)}
@media (min-width:1024px){
  .vt-pasos{grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:0 24px;border-top:0}
  .vt-pasos li{grid-template-columns:1fr;align-content:start;padding:16px 0 0;border-bottom:0;border-top:2px solid var(--vt-ink)}
  .vt-pasos li::before{grid-row:auto}
}

/* ---------- nota de campo, garantía, FAQ y cierre ---------- */
.vt-nota{margin:0;padding:14px 16px 14px 18px;border-left:3px solid var(--vt-soil);background:var(--vt-card)}
.vt-nota__t{display:block;margin-bottom:4px;font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-soil)}
.vt-pagina main .vt-nota p{margin:0;font-family:var(--vt-font-serif);font-style:italic;font-size:18px;line-height:1.4;color:var(--vt-ink-2)}
.vt-nota__firma{display:block;margin-top:6px;font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-grande{margin:0;font-size:clamp(4rem,3rem + 4vw,7rem);font-weight:800;line-height:.9;font-variant-numeric:tabular-nums;font-variation-settings:"wdth" var(--vt-wdth-tight)}
.vt-grande small{font-size:.32em;font-weight:700;color:var(--vt-soil)}
.vt-checks{display:grid;gap:10px;list-style:none}
.vt-checks li{display:grid;grid-template-columns:22px 1fr;gap:10px;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-checks li::before{content:"";width:18px;height:18px;margin-top:2px;border-radius:50%;background:var(--vt-field-100);box-shadow:inset 0 0 0 5px var(--vt-field)}
.vt-checks .vt-checks__no::before{background:var(--vt-bone-2);box-shadow:inset 0 0 0 5px var(--vt-soil)}
.vt-faq{border-top:1px solid var(--vt-ink)}
.vt-faq details{border-bottom:1px solid var(--vt-line)}
.vt-faq summary{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:56px;padding:14px 0;font-size:18px;font-weight:600;list-style:none;cursor:pointer}
.vt-faq summary::-webkit-details-marker{display:none}
.vt-faq summary::after{content:"+";flex:none;font-size:26px;font-weight:400;color:var(--vt-field);transition:transform var(--vt-duration-normal) var(--vt-ease-out)}
.vt-faq details[open] summary::after{transform:rotate(45deg)}
.vt-pagina main .vt-faq details p{max-width:66ch;margin:0 0 18px;color:var(--vt-ink-2)}
.vt-pagina main .vt-compra{display:grid;gap:8px;margin:12px 0 24px;padding-left:1.4em;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-guias{margin-top:24px;list-style:none}
.vt-guias li{border-bottom:1px solid var(--vt-line)}
.vt-pagina main .vt-guias a{display:block;padding:12px 0;font-weight:600}
.vt-cierre{padding-block:var(--vt-space-section);background:var(--vt-field-deep);color:var(--vt-on-dark)}
.vt-cierre__grid{display:grid;gap:24px}
.vt-pagina main .vt-cierre .vt-lede,.vt-cierre .vt-promesa{color:var(--vt-on-dark-2)}
.vt-cierre .vt-lede{margin-top:14px}
.vt-cierre .vt-cta{margin-top:24px}
.vt-pagina main .vt-cierre .vt-btn--wa{background:var(--vt-on-dark);color:var(--vt-field-deep)}
.vt-pagina main .vt-cierre .vt-btn--wa:hover{background:var(--vt-card)}
.vt-pagina main .vt-cierre .vt-btn--linea{color:var(--vt-on-dark);border-color:var(--vt-on-dark)}
.vt-pagina main .vt-cierre .vt-btn--linea:hover{background:var(--vt-on-dark);color:var(--vt-field-deep)}
.vt-pagina main .vt-cierre :focus-visible{outline-color:var(--vt-tag)}
.vt-cierre__msg{padding:16px;border:1px dashed var(--vt-on-dark-line);font-size:var(--vt-text-sm);color:var(--vt-on-dark-2);white-space:pre-line}
.vt-cierre__msg b{display:block;margin-bottom:4px;font-size:var(--vt-text-xs);letter-spacing:.1em;text-transform:uppercase;color:var(--vt-tag)}
.vt-relacionados{display:grid;gap:16px;list-style:none}
.vt-relacionados li{padding:16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-pagina main .vt-relacionados p{margin:4px 0 0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
@media (min-width:768px){.vt-relacionados{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1024px){.vt-cierre__grid{grid-template-columns:7fr 4fr;gap:64px;align-items:end}}
@media (prefers-reduced-motion:reduce){.vt-flecha,.vt-faq summary::after{transition:none}}
```

- [ ] **Step 5: Correr la prueba y medir**

```bash
cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_terra_css.py 2>&1 | tail -1
cd ~/dev/viverosterra-e2a && wc -c public/css/terra.css && gzip -c public/css/terra.css | wc -c
```

Expected: `OK`; unos 38,900 bytes y unos 9,000 con gzip.

- [ ] **Step 6: Build (nuevo hash en las 108 páginas) y suite**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/build.py | tail -1
git status --short | grep -v '\.html$'
cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1
```

Expected: `shell: 78 de 108 páginas actualizadas` (las 30 de `tools/pasto` ya salen con el hash nuevo de su propio build); solo `M public/css/terra.css`, `?? public/css/terra.<hash>.css` y, si había dos generaciones, `D public/css/terra.<hash-viejo>.css`; `OK`. Las páginas viejas se ven igual: ningún selector nuevo aplica fuera de `<body class="vt-pagina">` o de clases `.vt-` que solo emiten las plantillas.

- [ ] **Step 7: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add public/css tools/site/tests/test_terra_css.py public
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(css): componentes del cuerpo del híbrido en terra.css" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Componentes en Python (`tools/site/componentes.py`)

**Files:**
- Create: `tools/site/componentes.py`, `tools/site/tests/test_componentes.py`

- [ ] **Step 1: Escribir la prueba**

`tools/site/tests/test_componentes.py`:

```python
"""Componentes del cuerpo (tools/site/componentes.py): CTA, etiqueta, datos, figuras, tablas, proceso, FAQ y Medidor."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402


class UtilidadesTest(unittest.TestCase):
    def test_redondeo_igual_que_javascript(self):
        self.assertEqual([c.redondear(x) for x in (1102.5, 1103.5, 0.4)], [1103, 1104, 0])
        self.assertEqual(c.dinero(5760), "$5,760")
        self.assertEqual((c.formato_m2(48.0), c.formato_m2(1234.5)), ("48", "1,234.5"))

    def test_texto_plano_y_etiquetas_permitidas(self):
        self.assertEqual(c.texto_plano('Ver <a href="/x">la &amp; lista</a>\n hoy'), "Ver la & lista hoy")
        self.assertEqual(c.etiquetas_no_permitidas('<b>a</b> <a href="/x">b</a> <i>c</i>'), [])
        self.assertEqual(c.etiquetas_no_permitidas("<div><script>x</script></div>"), ["div", "script"])


class CtaTest(unittest.TestCase):
    def test_fila_de_cta_con_dos_textos_promesa_y_data_cta(self):
        html = c.fila_cta(datos.MENSAJES["general"], "home", "hero", hero=True)
        self.assertIn("data-hero-cta", html)
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["home:hero", "home:hero"])
        self.assertIn("Cotizar por WhatsApp", html)
        self.assertIn(f"Llamar {datos.TELEFONO_VISIBLE}", html)
        self.assertIn(datos.PROMESA_COMPLETA, html)
        texto = unquote(re.search(r'href="https://wa\.me/528333268008\?text=([^"]+)"', html).group(1))
        self.assertTrue(texto.endswith(datos.FIRMA))

    def test_sin_hero_no_marca_la_fila(self):
        self.assertNotIn("data-hero-cta", c.fila_cta("Hola", "home", "cierre"))


class BloquesTest(unittest.TestCase):
    def test_cuadro_de_datos_oficial(self):
        html = c.cuadro_datos()
        for dato in (f"REPSE {datos.REPSE}", datos.FACTURA, str(datos.DESDE), "Obregón 209 Sur", datos.M2_INSTALADOS):
            self.assertIn(dato, html)

    def test_figura_con_pie_y_carga(self):
        f = {"src": "/img/a.webp", "ancho": 10, "alto": 20, "alt": "Foto \"real\"", "numero": 3, "lugar": "Madero",
             "etapa": "Después"}
        self.assertIn('loading="lazy"', c.figura(f))
        principal = c.figura(f, principal=True)
        self.assertIn('loading="eager" fetchpriority="high"', principal)
        self.assertIn("<b>Fig. 03</b> · Madero", principal)
        self.assertIn('alt="Foto &quot;real&quot;"', principal)

    def test_logos_son_los_clientes_autorizados(self):
        self.assertEqual(tuple(n for n, *_ in c.LOGOS), datos.CLIENTES_B2B)
        for _nombre, archivo, _a, _h in c.LOGOS:
            self.assertTrue((Path(__file__).resolve().parents[3] / "public" / "img" / "clientes" / f"{archivo}-c.webp")
                            .is_file(), archivo)

    def test_tabla_de_precios_con_unidad_y_desde(self):
        html = c.tabla_precios([{"nombre": "Pasto", "detalle": "d", "unidad": "/m²", "precio": 120, "desde": True,
                                 "rec": True}], "Precios")
        self.assertIn('<th scope="col">Unidad</th>', html)
        self.assertIn('<td class="vt-tabla__u">/m²</td>', html)
        self.assertIn("<small>desde</small><span>$120</span>", html)

    def test_pasos_con_marcadores(self):
        html = c.pasos([{"titulo": "Riego", "quien": "tu", "cuando": "Día 1", "texto": "t"},
                        {"titulo": "Poda", "quien": "juntos", "cuando": "Día 21", "texto": "t"}])
        self.assertIn('<span class="vt-quien vt-quien--tu">Tú</span>', html)
        self.assertIn('<span class="vt-quien vt-quien--juntos">Juntos</span>', html)

    def test_faq_y_su_json_ld_dicen_lo_mismo(self):
        preguntas = (("¿Uno?", 'Sí, <a href="/x">mira</a>.'), ("¿Dos?", "No."))
        html = c.faq(preguntas)
        self.assertEqual(html.count("<details"), 2)
        self.assertEqual(html.count("<details open>"), 1)
        nodo = c.faq_jsonld(preguntas, speakable=("h1",))
        self.assertEqual(nodo["mainEntity"][0]["acceptedAnswer"]["text"], "Sí, mira.")
        self.assertEqual(nodo["speakable"]["cssSelector"], ["h1"])

    def test_planes_salen_de_la_formula_oficial(self):
        html = c.planes_mensualidades()
        for plazo, minimo in ((3, "$2,000"), (6, "$5,000"), (9, "$15,000"), (12, "$15,000")):
            self.assertIn(f"<dt>{plazo} mensualidades</dt><dd>desde {minimo}</dd>", html)
        self.assertNotRegex(html, r"(?i)sin intereses|\bMSI\b")

    def test_simulador_con_el_marcado_de_vt_simulador(self):
        html = c.simulador("pasto en rollo instalado", 12000, "servicio-pasto")
        for marca in ("data-simulador", "data-sim-monto", "data-sim-list", "data-sim-wa",
                      'data-cta="servicio-pasto:simulador"', 'value="12000"'):
            self.assertIn(marca, html)

    def test_howto_numera_los_pasos(self):
        nodo = c.howto("Cómo", (("Uno", "a"), ("Dos", "b")))
        self.assertEqual([p["position"] for p in nodo["step"]], [1, 2])


class MedidorTest(unittest.TestCase):
    def test_html_del_medidor(self):
        html = c.medidor("prueba", "home")
        self.assertIn("data-vt-medidor", html)
        self.assertEqual(html.count('name="prueba-modo"'), 3)
        self.assertIn('data-precio="120"', html)
        self.assertIn('data-minimo="500"', html)
        self.assertIn('<b data-vt-o="monto">$5,760</b>', html)
        self.assertIn('data-cta="home:medidor"', html)
        self.assertIn('<p class="vt-medidor__aviso" data-vt-o="aviso" hidden>', html)
        for campo in ("largo", "ancho", "colonia"):
            self.assertIn(f'<label for="prueba-{campo}">', html)
        self.assertNotIn("<form", html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrla y ver que falla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_componentes.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'componentes'`.

- [ ] **Step 3: Implementar `tools/site/componentes.py`**

```python
"""Componentes del cuerpo de página del híbrido "Plano + Etiqueta" (Etapa 2).

Funciones puras que devuelven HTML para las plantillas de tools/site/plantillas/. Los textos que llegan de
tools/site/contenido/ son HTML en línea de confianza (solo las etiquetas de ETIQUETAS_PERMITIDAS; test_contenido.py lo
verifica); los atributos (href, src, alt, data-*) se escapan aquí. Todo número oficial sale de datos.py y la fórmula de
mensualidades es la de tools/pasto/mensualidades.py (la misma de public/js/vt-mensualidades.js): aquí no se reimplementa.
"""
import html as html_mod
import math
import re
import sys
from pathlib import Path

PASTO = str(Path(__file__).resolve().parents[1] / "pasto")
if PASTO not in sys.path:
    sys.path.append(PASTO)  # al final: tools/pasto también tiene un build.py

import datos  # noqa: E402
import mensualidades  # noqa: E402
from partials import WA_GLIFO, esc  # noqa: E402

P = datos.PRECIOS
ETIQUETAS_PERMITIDAS = frozenset({"a", "b", "i", "em", "strong", "br", "small", "span"})


# ---------- utilidades ----------
def redondear(x):
    """Igual que Math.round de JavaScript para valores positivos (round() de Python lleva los .5 al par)."""
    return int(math.floor(x + 0.5))


def dinero(n):
    return f"${redondear(n):,}"


def formato_m2(x):
    """Como x.toLocaleString('es-MX', {maximumFractionDigits: 1}): 48 → "48", 1234.5 → "1,234.5"."""
    texto = f"{x:,.1f}"
    return texto[:-2] if texto.endswith(".0") else texto


def texto_plano(fragmento):
    """Texto sin etiquetas ni entidades, con espacios normalizados (para el JSON-LD)."""
    sin_etiquetas = re.sub(r"<[^>]+>", "", fragmento)
    return re.sub(r"\s+", " ", html_mod.unescape(sin_etiquetas)).strip()


def etiquetas_no_permitidas(fragmento):
    """Nombres de etiqueta del fragmento que no están en ETIQUETAS_PERMITIDAS, ordenados."""
    return sorted({t.lower() for t in re.findall(r"</?([a-zA-Z][\w-]*)", fragmento)} - ETIQUETAS_PERMITIDAS)


# ---------- CTA (dos textos y nada más: "Cotizar por WhatsApp" y "Llamar 833 326 8008") ----------
def boton_wa(mensaje, cta):
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<a class="vt-btn vt-btn--wa" data-cta="{esc(cta)}" href="{href}" target="_blank" rel="noopener">'
            f'{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→</span></a>')


def boton_tel(cta):
    return (f'<a class="vt-btn vt-btn--linea" data-cta="{esc(cta)}" href="tel:{datos.TELEFONO_TEL}">'
            f'<svg class="vt-ico" aria-hidden="true"><use href="#vt-i-tel"/></svg>Llamar {datos.TELEFONO_VISIBLE}</a>')


def fila_cta(mensaje, tipo, seccion, hero=False):
    """WhatsApp + teléfono + promesa única. Con hero=True, terra.js oculta la barra móvil mientras se ve."""
    cta = f"{tipo}:{seccion}"
    marca = " data-hero-cta" if hero else ""
    return (f'<div class="vt-cta"{marca}>{boton_wa(mensaje, cta)}{boton_tel(cta)}</div>'
            f'<p class="vt-promesa">{esc(datos.PROMESA_COMPLETA)}</p>')


# ---------- estructura ----------
def migas(items):
    """Ruta visible: [(texto, href), …, (texto, None)]; el último es la página actual."""
    partes = [f'<li aria-current="page">{texto}</li>' if href is None else f'<li><a href="{esc(href)}">{texto}</a></li>'
              for texto, href in items]
    return f'<nav class="vt-crumbs" aria-label="Ruta de navegación"><ol>{"".join(partes)}</ol></nav>'


def bloque(numero, rotulo, id_titulo, titulo, cuerpo, lede=None, tinte=False, id_seccion=None):
    """Sección numerada con encabezado a dos columnas (título y entrada)."""
    clase = "vt-bloque vt-bloque--tinte" if tinte else "vt-bloque"
    ident = f' id="{id_seccion}"' if id_seccion else ""
    entrada = f'<p class="vt-lede">{lede}</p>' if lede else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{id_titulo}"><div class="vt-wrap">'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p>'
            f'<div class="vt-bloque__cabeza"><h2 id="{id_titulo}">{titulo}</h2>{entrada}</div>{cuerpo}</div></section>')


def bloque_dos(numero, rotulo, id_titulo, titulo, izquierda, derecha, tinte=False, id_seccion=None):
    """Sección numerada a dos columnas: título y apoyo a la izquierda, contenido a la derecha."""
    clase = "vt-bloque vt-bloque--tinte" if tinte else "vt-bloque"
    ident = f' id="{id_seccion}"' if id_seccion else ""
    return (f'<section class="{clase}"{ident} aria-labelledby="{id_titulo}"><div class="vt-wrap vt-dos"><div>'
            f'<p class="vt-bloque__no"><b>{numero:02d}</b>{rotulo}</p><h2 id="{id_titulo}">{titulo}</h2>{izquierda}</div>'
            f'<div>{derecha}</div></div></section>')


# ---------- etiqueta de precio y cuadro de datos ----------
def etiqueta(e):
    """Etiqueta amarilla de precio. e: codigo, aviso, nombre, cientifico, antes, monto, unidad, filas, nota."""
    filas = "".join(f'<p class="vt-etiqueta__fila"><span>{t}</span><b>{v}</b></p>' for t, v in e.get("filas", ()))
    nota = f'<p class="vt-etiqueta__nota">{e["nota"]}</p>' if e.get("nota") else ""
    return (f'<div class="vt-etiqueta"><p class="vt-etiqueta__cod"><span>{e["codigo"]}</span><span>{e["aviso"]}</span></p>'
            f'<p class="vt-etiqueta__nombre">{e["nombre"]}</p><p class="vt-etiqueta__sci">{e["cientifico"]}</p>'
            f'<p class="vt-etiqueta__precio"><small>{e["antes"]}</small><b>{e["monto"]}</b><span>{e["unidad"]}</span></p>'
            f'{filas}{nota}</div>')


DATOS_EMPRESA = (
    ("Empresa", datos.NOMBRE, "Vivero, pasto y jardinería"),
    ("Registro", f"REPSE {datos.REPSE}", "Contratos con empresas"),
    ("Facturación", datos.FACTURA, "Persona física o moral"),
    ("Desde", str(datos.DESDE), "En Cd. Madero y Tampico"),
    ("Showroom", "Obregón 209 Sur", datos.REFERENCIA),
    ("Instalado", datos.M2_INSTALADOS, "En Tamaulipas y la Huasteca"),
)


def cuadro_datos(celdas=DATOS_EMPRESA):
    cuerpo = "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>" for t, v, s in celdas)
    return f'<dl class="vt-datos">{cuerpo}</dl>'


# ---------- fotos documentales, prueba y clientes ----------
def figura(f, principal=False):
    """Foto con pie FIG. f: src, ancho, alto, alt, numero, lugar, etapa y opcionales srcset y sizes. Solo la imagen
    principal carga con prioridad; las demás son lazy."""
    carga = 'loading="eager" fetchpriority="high"' if principal else 'loading="lazy"'
    srcset = f' srcset="{esc(f["srcset"])}" sizes="{esc(f["sizes"])}"' if f.get("srcset") else ""
    return (f'<figure class="vt-fig"><div class="vt-fig__marco"><img src="{esc(f["src"])}"{srcset} width="{f["ancho"]}" '
            f'height="{f["alto"]}" {carga} decoding="async" alt="{esc(f["alt"])}"></div>'
            f'<figcaption><span><b>Fig. {f["numero"]:02d}</b> · {f["lugar"]}</span><span>{f["etapa"]}</span></figcaption>'
            f'</figure>')


def obras(figuras, nota_html=""):
    return f'<div class="vt-obras">{"".join(figura(f) for f in figuras)}{nota_html}</div>'


def nota(texto, firma):
    return (f'<aside class="vt-nota" aria-label="Nota de campo"><span class="vt-nota__t">Nota de campo</span>'
            f'<p>{texto}</p><span class="vt-nota__firma">{firma}</span></aside>')


def linea_prueba():
    return (f'<p class="vt-prueba"><span><b>{esc(datos.GOOGLE)}</b></span>'
            f'<span><b>{datos.M2_INSTALADOS}</b> instalados en Tamaulipas y la Huasteca</span>'
            f'<span><b>{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones</b> desde {datos.DESDE}</span></p>')


# Nombre (igual que datos.CLIENTES_B2B), archivo en /img/clientes/<archivo>-c.webp, ancho y alto.
LOGOS = (
    ("BMW", "logo-bmw", 120, 120),
    ("Taghleef Industries", "logo-taghleef", 584, 120),
    ("Gobierno de Tampico", "logo-gobierno-tampico", 198, 120),
    ("Grupo Velas", "logo-grupo-velas", 229, 120),
    ("Velamar", "logo-velamar", 188, 120),
    ("Flex", "logo-flex", 120, 120),
)


def logos():
    items = "".join(f'<li><img src="/img/clientes/{archivo}-c.webp" width="{ancho}" height="{alto}" alt="{esc(nombre)}" '
                    f'loading="lazy" decoding="async"></li>' for nombre, archivo, ancho, alto in LOGOS)
    return f'<ul class="vt-logos" aria-label="Clientes de Viveros Terra">{items}</ul>'


# ---------- índice de servicios, tablas y relacionados ----------
def indice(items):
    """Filas tipo índice: foto, título con enlace, qué incluye y "desde" con la marca amarilla."""
    filas = "".join(
        f'<li><img src="{esc(i["img"])}" width="{i["ancho"]}" height="{i["alto"]}" alt="" loading="lazy" decoding="async">'
        f'<h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p>'
        f'<p class="vt-indice__desde">desde <span class="vt-precio-marca">{i["desde"]}</span> {i["unidad"]}</p></li>'
        for i in items)
    return f'<ol class="vt-indice">{filas}</ol>'


def tabla_precios(filas, caption, concepto="Concepto"):
    """Lista de precios con columna Unidad. filas: nombre, detalle, unidad, precio (número), desde, rec (recomendado)."""
    cuerpo = []
    for f in filas:
        clase = ' class="vt-tabla__rec"' if f.get("rec") else ""
        desde = "<small>desde</small>" if f.get("desde") else ""
        precio = f"<span>{dinero(f['precio'])}</span>" if f.get("rec") else dinero(f["precio"])
        cuerpo.append(f'<tr{clase}><th scope="row"><b>{f["nombre"]}</b><span>{f["detalle"]}</span></th>'
                      f'<td class="vt-tabla__u">{f["unidad"]}</td><td class="vt-tabla__p">{desde}{precio}</td></tr>')
    return (f'<table class="vt-tabla vt-tabla--precios"><caption>{caption}</caption><thead><tr>'
            f'<th scope="col">{concepto}</th><th scope="col">Unidad</th><th scope="col" class="vt-tabla__p">Precio</th>'
            f'</tr></thead><tbody>{"".join(cuerpo)}</tbody></table>')


def tabla_comparativa(columnas, filas, caption):
    """Tabla de comparación: la primera columna es el encabezado de cada fila. Se desliza en celular si no cabe."""
    cabeza = "".join(f'<th scope="col">{c}</th>' for c in columnas)
    cuerpo = "".join(f'<tr><th scope="row">{f[0]}</th>{"".join(f"<td>{v}</td>" for v in f[1:])}</tr>' for f in filas)
    return (f'<div class="vt-desliza" role="region" aria-label="{esc(texto_plano(caption))}" tabindex="0">'
            f'<table class="vt-tabla"><caption>{caption}</caption><thead><tr>{cabeza}</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table></div>')


def relacionados(items):
    filas = "".join(f'<li><h3><a href="{esc(i["href"])}">{i["titulo"]}</a></h3><p>{i["texto"]}</p></li>' for i in items)
    return f'<ul class="vt-relacionados">{filas}</ul>'


def guias(items, href_todas="/blog"):
    filas = "".join(f'<li><a href="{esc(href)}">{texto}</a></li>' for texto, href in items)
    return f'<ul class="vt-guias">{filas}<li><a href="{esc(href_todas)}">Ver todas las guías</a></li></ul>'


# ---------- proceso, garantía, FAQ y cierre ----------
QUIEN = {"nosotros": ("Nosotros", ""), "tu": ("Tú", " vt-quien--tu"), "juntos": ("Juntos", " vt-quien--juntos")}


def pasos(items):
    """Proceso con marcadores NOSOTROS / TÚ / JUNTOS. items: titulo, quien, cuando, texto."""
    filas = "".join(
        f'<li><h3>{p["titulo"]} <span class="vt-quien{QUIEN[p["quien"]][1]}">{QUIEN[p["quien"]][0]}</span></h3>'
        f'<p class="vt-pasos__cuando">{p["cuando"]}</p><p>{p["texto"]}</p></li>' for p in items)
    return f'<ol class="vt-pasos">{filas}</ol>'


def pasos_compra(items):
    """Lista breve "de la cotización a tu jardín" (la misma que el HowTo del JSON-LD). items: (nombre, texto)."""
    filas = "".join(f"<li><b>{nombre}.</b> {texto}</li>" for nombre, texto in items)
    return f'<ol class="vt-compra">{filas}</ol>'


def howto(nombre, items):
    return {"@type": "HowTo", "name": nombre,
            "step": [{"@type": "HowToStep", "position": i, "name": texto_plano(n), "text": texto_plano(t)}
                     for i, (n, t) in enumerate(items, 1)]}


def garantia(g):
    """g: titulo, id_titulo, numero, rotulo, grande, unidad, resumen, puntos (texto, si_aplica), pie."""
    no_aplica = ' class="vt-checks__no"'
    puntos = "".join(f'<li{"" if ok else no_aplica}>{t}</li>' for t, ok in g["puntos"])
    return (f'<section class="vt-bloque vt-bloque--tinte" aria-labelledby="{g["id_titulo"]}"><div class="vt-wrap vt-dos">'
            f'<div><p class="vt-bloque__no"><b>{g["numero"]:02d}</b>{g["rotulo"]}</p><h2 id="{g["id_titulo"]}">'
            f'{g["titulo"]}</h2><p class="vt-grande">{g["grande"]}<small> {g["unidad"]}</small></p>'
            f'<p class="vt-promesa">{g["resumen"]}</p></div><div><ul class="vt-checks">{puntos}</ul>'
            f'<p class="vt-promesa">{g["pie"]}</p></div></div></section>')


def faq(preguntas):
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
                    for i, (q, a) in enumerate(preguntas))
    return f'<div class="vt-faq">{items}</div>'


def faq_jsonld(preguntas, speakable=None):
    """FAQPage con las mismas preguntas y respuestas visibles (en texto plano)."""
    nodo = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": texto_plano(q), "acceptedAnswer": {"@type": "Answer", "text": texto_plano(a)}}
        for q, a in preguntas]}
    if speakable:
        nodo["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": list(speakable)}
    return nodo


def cierre(titulo, lede, mensaje, tipo):
    """CTA final en verde profundo, con el mensaje que se abre a la vista."""
    return (f'<section class="vt-cierre" aria-labelledby="vt-cierre-titulo"><div class="vt-wrap vt-cierre__grid"><div>'
            f'<h2 id="vt-cierre-titulo">{titulo}</h2><p class="vt-lede">{lede}</p>{fila_cta(mensaje, tipo, "cierre")}</div>'
            f'<p class="vt-cierre__msg"><b>El mensaje que se abre</b>{esc(datos.con_firma(mensaje))}</p></div></section>')


# ---------- mensualidades con tarjeta de crédito ----------
def planes_mensualidades():
    """Plazos y montos mínimos de tools/pasto/mensualidades.py (los mismos de vt-mensualidades.js)."""
    celdas = "".join(f"<div><dt>{p} mensualidades</dt><dd>desde {dinero(mensualidades.minimo_de(p))}</dd></div>"
                     for p in mensualidades.PLAZOS)
    return ('<div class="vt-planes"><div class="vt-planes__cabeza"><b>Mensualidades con tarjeta de crédito</b>'
            '<span>El contado (transferencia, efectivo o tarjeta en una exhibición) es el precio más bajo.</span></div>'
            f'<dl>{celdas}</dl><p>Montos mínimos de cotización por plazo. El total a plazos es mayor que el de contado y '
            'te lo mostramos antes de enviarte el link de pago. Tu banco debe aceptar el plan. '
            '<a href="/politicas#mensualidades">Condiciones</a></p></div>')


def simulador(servicio, monto, tipo):
    """Marcado que espera public/js/vt-simulador.js ([data-simulador], [data-sim-monto], [data-sim-list], [data-sim-wa])."""
    return (f'<div class="vt-sim" data-simulador data-servicio="{esc(servicio)}"><div class="vt-campo">'
            '<label for="vt-sim-monto">Monto de tu cotización</label><div class="vt-control">'
            f'<input id="vt-sim-monto" type="number" inputmode="numeric" min="0" step="100" value="{int(monto)}" '
            'data-sim-monto><span>MXN</span></div></div>'
            '<div class="vt-sim__lista" role="radiogroup" aria-label="Forma de pago" data-sim-list></div>'
            '<p class="vt-promesa">Montos aproximados: tu banco debe aceptar el plan. Disponible en cotizaciones desde '
            f'{dinero(mensualidades.minimo_de(3))}.</p><a class="vt-btn vt-btn--wa" data-cta="{tipo}:simulador" '
            f'data-sim-wa href="https://wa.me/{datos.TELEFONO_WA}" target="_blank" rel="noopener">{WA_GLIFO}'
            'Cotizar por WhatsApp</a></div>')


# ---------- Medidor de m² (mismo cálculo que public/js/vt-medidor.js; paridad en casos-medidor.json) ----------
MINIMO_MAYOREO = P["pasto_mayoreo_minimo_m2"]
MODOS_MEDIDOR = {
    "instalado": {"precio": P["pasto_instalado_m2"], "desde": True, "texto": "pasto San Agustín instalado",
                  "rotulo": "Instalado · desde", "opcion": "Pasto instalado"},
    "solo": {"precio": P["pasto_solo_m2"], "desde": False, "texto": "solo el pasto San Agustín (yo lo instalo)",
             "rotulo": "Solo pasto", "opcion": "Solo el pasto, yo lo instalo"},
    "mayoreo": {"precio": P["pasto_mayoreo_m2"], "desde": True, "minimo": MINIMO_MAYOREO,
                "texto": "pasto San Agustín de mayoreo (solo pasto)", "rotulo": "Mayoreo · desde",
                "opcion": f"Mayoreo, {MINIMO_MAYOREO} m² o más"},
}
PLANO = {"ancho": 360, "alto": 190, "x": 44, "y": 56, "minimo": 24}


def calculo_medidor(largo, ancho, modo):
    """m², precio por m², total y aviso. El mayoreo es solo pasto: con menos del mínimo calcula a precio de solo pasto
    y lo avisa (J03 §3)."""
    m = MODOS_MEDIDOR[modo]
    m2 = redondear(largo * ancho * 10) / 10
    precio, desde, texto, rotulo, aviso = m["precio"], m["desde"], m["texto"], m["rotulo"], ""
    minimo = m.get("minimo")
    if minimo and m2 < minimo:
        solo = MODOS_MEDIDOR["solo"]
        precio, desde, texto = solo["precio"], False, solo["texto"]
        rotulo = f"Solo pasto (mayoreo desde {minimo} m²)"
        aviso = (f"El mayoreo aplica desde {minimo} m². Te faltan {math.ceil(minimo - m2)} m²; mientras, calculamos "
                 f"a ${precio}/m² (solo pasto).")
    return {"m2": m2, "precio": precio, "desde": desde, "texto": texto, "rotulo": rotulo, "aviso": aviso,
            "total": redondear(m2 * precio)}


def textos_medidor(largo, ancho, r, colonia=""):
    """Textos de la etiqueta y mensaje de WhatsApp para el resultado `r` de calculo_medidor."""
    medida = f"{largo:.2f} × {ancho:.2f} m = {formato_m2(r['m2'])} m²"
    desde = "desde " if r["desde"] else ""
    disponibles = mensualidades.plazos_disponibles(r["total"])
    if disponibles:
        ultimo = disponibles[-1]
        total = mensualidades.total_a_plazos(r["total"], ultimo)
        plan = (f"O {ultimo} mensualidades de {dinero(total / ultimo)} con tarjeta de crédito "
                f"(total {dinero(total)}).")
    else:
        plan = f"Mensualidades con tarjeta de crédito en cotizaciones desde {dinero(mensualidades.minimo_de(3))}."
    cierre_calc = "Al medir te damos el precio cerrado." if r["desde"] else "La entrega se cotiza según tu colonia."
    mensaje = "\n".join((f"Hola, quiero cotizar {r['texto']}.", f"Medidas: {medida}",
                         f"Estimado de la web: {desde}{dinero(r['total'])} con IVA", f"Colonia: {colonia or '___'}",
                         "Te mando foto del área."))
    return {"medida": medida, "monto": dinero(r["total"]),
            "calc": f"{formato_m2(r['m2'])} m² × {desde}${r['precio']}/m², con IVA. {cierre_calc}",
            "plan": plan, "mensaje": mensaje}


def plano_medidor(largo, ancho):
    """Rectángulo del patio a escala dentro del plano de 480 × 300 (mismo cálculo que vt-medidor.js)."""
    escala = min(PLANO["ancho"] / largo, PLANO["alto"] / ancho)
    w, h = max(PLANO["minimo"], largo * escala), max(PLANO["minimo"], ancho * escala)
    return {"x": PLANO["x"] + (PLANO["ancho"] - w) / 2, "y": PLANO["y"] + (PLANO["alto"] - h) / 2, "w": w, "h": h}


def _n(v):
    return f"{v:.1f}"


def svg_plano(largo, ancho, m2):
    g = plano_medidor(largo, ancho)
    x, y, w, h = g["x"], g["y"], g["w"], g["h"]
    lado = x + w + 22
    rect = f'x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}"'
    area_visible = "" if w > 96 and h > 34 else ' style="display:none"'
    return (
        '<svg viewBox="0 0 480 300" role="img" aria-label="Tu patio dibujado a escala, visto desde arriba">'
        f'<rect class="vt-plano-relleno" data-vt-plano {rect}/><rect class="vt-plano-borde" data-vt-plano {rect}/>'
        f'<path class="vt-cota" data-vt-cota="arriba" d="M{_n(x)} {_n(y - 26)} v14 M{_n(x + w)} {_n(y - 26)} v14 '
        f'M{_n(x)} {_n(y - 19)} H{_n(x + w)}"/>'
        f'<text class="vt-cota-t" data-vt-texto="arriba" x="{_n(x + w / 2)}" y="{_n(y - 32)}" text-anchor="middle">'
        f'{largo:.2f} m</text>'
        f'<path class="vt-cota" data-vt-cota="lado" d="M{_n(lado - 7)} {_n(y)} h14 M{_n(lado - 7)} {_n(y + h)} h14 '
        f'M{_n(lado)} {_n(y)} V{_n(y + h)}"/>'
        f'<text class="vt-cota-t" data-vt-texto="lado" text-anchor="middle" '
        f'transform="translate({_n(lado + 20)} {_n(y + h / 2)}) rotate(-90)">{ancho:.2f} m</text>'
        f'<text class="vt-cota-a" data-vt-texto="area" x="{_n(x + w / 2)}" y="{_n(y + h / 2 + 9)}" '
        f'text-anchor="middle"{area_visible}>{formato_m2(m2)} m²</text></svg>')


def _opcion_medidor(prefijo, clave, m, elegido):
    marcado = " checked" if clave == elegido else ""
    minimo = f' data-minimo="{m["minimo"]}"' if m.get("minimo") else ""
    precio = f'{"desde " if m["desde"] else ""}${m["precio"]}/m²'
    return (f'<label><span>{m["opcion"]}</span><small>{precio}</small><input type="radio" name="{prefijo}-modo" '
            f'value="{clave}" data-precio="{m["precio"]}" data-desde="{1 if m["desde"] else 0}" '
            f'data-texto="{esc(m["texto"])}" data-rotulo="{esc(m["rotulo"])}"{minimo}{marcado}></label>')


def medidor(prefijo, tipo, largo=8, ancho=6, modo="instalado"):
    """Medidor: largo × ancho → plano a escala → etiqueta con el estimado y mensualidades → WhatsApp con la medida.
    Sin JavaScript queda el cálculo inicial y un enlace válido. vt-medidor.js lo actualiza con los data-* de cada
    opción: los precios no viven en el JS."""
    r = calculo_medidor(largo, ancho, modo)
    t = textos_medidor(largo, ancho, r)
    opciones = "".join(_opcion_medidor(prefijo, k, m, modo) for k, m in MODOS_MEDIDOR.items())
    campo = ('<div class="vt-campo"><label for="{p}-{n}">{t}</label><div class="vt-control"><input id="{p}-{n}" '
             'data-vt-campo="{n}" inputmode="decimal" value="{v}" autocomplete="off"><span>m</span></div></div>')
    return (
        f'<div class="vt-medidor" data-vt-medidor><div class="vt-medidor__form" role="group" aria-label="Medidor de pasto">'
        f'<div class="vt-medidor__medidas">{campo.format(p=prefijo, n="largo", t="Largo", v=largo)}'
        f'<span class="vt-medidor__x" aria-hidden="true">×</span>{campo.format(p=prefijo, n="ancho", t="Ancho", v=ancho)}'
        f'</div><fieldset class="vt-opciones"><legend>¿Qué necesitas?</legend>{opciones}</fieldset>'
        f'<div class="vt-campo"><label for="{prefijo}-colonia">Colonia (opcional)</label><div class="vt-control">'
        f'<input type="text" id="{prefijo}-colonia" data-vt-campo="colonia" placeholder="Ej. Lomas de Rosales" '
        f'autocomplete="off"></div></div></div>'
        f'<figure class="vt-fig vt-medidor__plano">{svg_plano(largo, ancho, r["m2"])}<figcaption><span><b>Vista en planta'
        f'</b> · escala ajustada a tu medida</span><span>Cotas en metros</span></figcaption></figure>'
        f'<div class="vt-etiqueta vt-medidor__res"><p class="vt-etiqueta__cod"><span>Tu etiqueta</span><span>Estimado'
        f'</span></p><p class="vt-etiqueta__nombre" data-vt-o="m2">{t["medida"]}</p><p class="vt-etiqueta__sci">'
        f'Stenotaphrum secundatum</p><p class="vt-etiqueta__precio" aria-live="polite"><small data-vt-o="rotulo">'
        f'{r["rotulo"]}</small><b data-vt-o="monto">{t["monto"]}</b><span>con IVA</span></p>'
        f'<p class="vt-medidor__calc" data-vt-o="calc">{t["calc"]}</p>'
        f'<p class="vt-medidor__aviso" data-vt-o="aviso"{"" if r["aviso"] else " hidden"}>{r["aviso"]}</p>'
        f'<p class="vt-medidor__plan" data-vt-o="plan">{t["plan"]}</p>'
        f'<a class="vt-btn vt-btn--wa" data-cta="{tipo}:medidor" data-vt-o="cta" href="{esc(datos.wa_url(t["mensaje"]))}" '
        f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp<span class="vt-flecha" aria-hidden="true">→'
        f'</span></a></div></div>')


# ---------- portada (primer pantallazo: qué, dónde, precio y CTA) ----------
def portada(p, tipo, migas_items=None):
    """p: kicker, h1, lede, etiqueta, mensaje, tambien y foto. Con migas_items, la ruta visible va arriba."""
    ruta = migas(migas_items) if migas_items else ""
    return (f'<section class="vt-portada" aria-labelledby="vt-h1"><div class="vt-wrap">{ruta}<div class="vt-portada__grid">'
            f'<div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1><p class="vt-lede">{p["lede"]}</p>'
            f'<div class="vt-portada__trato">{etiqueta(p["etiqueta"])}<div>{fila_cta(p["mensaje"], tipo, "hero", hero=True)}'
            f'<p class="vt-portada__tambien">{p["tambien"]}</p></div></div></div>'
            f'<div class="vt-portada__foto">{figura(p["foto"], principal=True)}</div></div>{cuadro_datos()}</div></section>')
```

Notas: `textos_medidor` redondea la mensualidad con `redondear(total / plazo)`, igual que `Math.round` de `vt-mensualidades.js`; no usa `mensualidades.planes()` porque su `round()` lleva los `.5` al par (ver riesgos). El Medidor no lleva `<form>` (sin envío accidental y sin JS en línea para la CSP).

- [ ] **Step 4: Correr la prueba**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_componentes.py -v 2>&1 | tail -3`
Expected: `Ran 14 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/componentes.py tools/site/tests/test_componentes.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantillas): componentes del cuerpo como funciones puras" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Medidor en el navegador (`public/js/vt-medidor.js`) con paridad Python ↔ JS

**Files:**
- Create: `public/js/tests/casos-medidor.json`, `public/js/tests/vt-medidor.test.js`, `public/js/vt-medidor.js`, `tools/site/tests/test_medidor_paridad.py`

- [ ] **Step 1: Casos de paridad**

`public/js/tests/casos-medidor.json` (los mismos números que hoy da la fórmula oficial; 48 m² instalados = $5,760 y 6 mensualidades de $1,103, como la maqueta):

```json
{
  "modos": {
    "instalado": {
      "precio": 120,
      "desde": true,
      "texto": "pasto San Agustín instalado",
      "rotulo": "Instalado · desde"
    },
    "solo": {
      "precio": 85,
      "desde": false,
      "texto": "solo el pasto San Agustín (yo lo instalo)",
      "rotulo": "Solo pasto"
    },
    "mayoreo": {
      "precio": 60,
      "desde": true,
      "minimo": 500,
      "texto": "pasto San Agustín de mayoreo (solo pasto)",
      "rotulo": "Mayoreo · desde"
    }
  },
  "casos": [
    {
      "entrada": {
        "largo": 8,
        "ancho": 6,
        "modo": "instalado",
        "colonia": ""
      },
      "esperado": {
        "m2": 48.0,
        "precio": 120,
        "desde": true,
        "total": 5760,
        "rotulo": "Instalado · desde",
        "aviso": "",
        "medida": "8.00 × 6.00 m = 48 m²",
        "monto": "$5,760",
        "calc": "48 m² × desde $120/m², con IVA. Al medir te damos el precio cerrado.",
        "plan": "O 6 mensualidades de $1,103 con tarjeta de crédito (total $6,618).",
        "mensaje": "Hola, quiero cotizar pasto San Agustín instalado.\nMedidas: 8.00 × 6.00 m = 48 m²\nEstimado de la web: desde $5,760 con IVA\nColonia: ___\nTe mando foto del área."
      }
    },
    {
      "entrada": {
        "largo": 10,
        "ancho": 10,
        "modo": "mayoreo",
        "colonia": "Lomas de Rosales"
      },
      "esperado": {
        "m2": 100.0,
        "precio": 85,
        "desde": false,
        "total": 8500,
        "rotulo": "Solo pasto (mayoreo desde 500 m²)",
        "aviso": "El mayoreo aplica desde 500 m². Te faltan 400 m²; mientras, calculamos a $85/m² (solo pasto).",
        "medida": "10.00 × 10.00 m = 100 m²",
        "monto": "$8,500",
        "calc": "100 m² × $85/m², con IVA. La entrega se cotiza según tu colonia.",
        "plan": "O 6 mensualidades de $1,628 con tarjeta de crédito (total $9,766).",
        "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo).\nMedidas: 10.00 × 10.00 m = 100 m²\nEstimado de la web: $8,500 con IVA\nColonia: Lomas de Rosales\nTe mando foto del área."
      }
    },
    {
      "entrada": {
        "largo": 5,
        "ancho": 4,
        "modo": "solo",
        "colonia": ""
      },
      "esperado": {
        "m2": 20.0,
        "precio": 85,
        "desde": false,
        "total": 1700,
        "rotulo": "Solo pasto",
        "aviso": "",
        "medida": "5.00 × 4.00 m = 20 m²",
        "monto": "$1,700",
        "calc": "20 m² × $85/m², con IVA. La entrega se cotiza según tu colonia.",
        "plan": "Mensualidades con tarjeta de crédito en cotizaciones desde $2,000.",
        "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo).\nMedidas: 5.00 × 4.00 m = 20 m²\nEstimado de la web: $1,700 con IVA\nColonia: ___\nTe mando foto del área."
      }
    },
    {
      "entrada": {
        "largo": 25,
        "ancho": 24,
        "modo": "mayoreo",
        "colonia": ""
      },
      "esperado": {
        "m2": 600.0,
        "precio": 60,
        "desde": true,
        "total": 36000,
        "rotulo": "Mayoreo · desde",
        "aviso": "",
        "medida": "25.00 × 24.00 m = 600 m²",
        "monto": "$36,000",
        "calc": "600 m² × desde $60/m², con IVA. Al medir te damos el precio cerrado.",
        "plan": "O 12 mensualidades de $3,703 con tarjeta de crédito (total $44,439).",
        "mensaje": "Hola, quiero cotizar pasto San Agustín de mayoreo (solo pasto).\nMedidas: 25.00 × 24.00 m = 600 m²\nEstimado de la web: desde $36,000 con IVA\nColonia: ___\nTe mando foto del área."
      }
    },
    {
      "entrada": {
        "largo": 12.5,
        "ancho": 8.3,
        "modo": "instalado",
        "colonia": "Altavista"
      },
      "esperado": {
        "m2": 103.8,
        "precio": 120,
        "desde": true,
        "total": 12456,
        "rotulo": "Instalado · desde",
        "aviso": "",
        "medida": "12.50 × 8.30 m = 103.8 m²",
        "monto": "$12,456",
        "calc": "103.8 m² × desde $120/m², con IVA. Al medir te damos el precio cerrado.",
        "plan": "O 6 mensualidades de $2,385 con tarjeta de crédito (total $14,311).",
        "mensaje": "Hola, quiero cotizar pasto San Agustín instalado.\nMedidas: 12.50 × 8.30 m = 103.8 m²\nEstimado de la web: desde $12,456 con IVA\nColonia: Altavista\nTe mando foto del área."
      }
    },
    {
      "entrada": {
        "largo": 30,
        "ancho": 20,
        "modo": "solo",
        "colonia": ""
      },
      "esperado": {
        "m2": 600.0,
        "precio": 85,
        "desde": false,
        "total": 51000,
        "rotulo": "Solo pasto",
        "aviso": "",
        "medida": "30.00 × 20.00 m = 600 m²",
        "monto": "$51,000",
        "calc": "600 m² × $85/m², con IVA. La entrega se cotiza según tu colonia.",
        "plan": "O 12 mensualidades de $5,246 con tarjeta de crédito (total $62,955).",
        "mensaje": "Hola, quiero cotizar solo el pasto San Agustín (yo lo instalo).\nMedidas: 30.00 × 20.00 m = 600 m²\nEstimado de la web: $51,000 con IVA\nColonia: ___\nTe mando foto del área."
      }
    }
  ]
}
```

- [ ] **Step 2: Escribir las pruebas (Node y Python)**

`public/js/tests/vt-medidor.test.js`:

```js
// public/js/tests/vt-medidor.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const M = require('../vt-mensualidades.js');
const { numero, calcular, textos, plano } = require('../vt-medidor.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-medidor.json'), 'utf8'));

test('mismos resultados que tools/site/componentes.py en cada caso de casos-medidor.json', () => {
  for (const { entrada, esperado } of CASOS.casos) {
    const r = calcular(entrada.largo, entrada.ancho, entrada.modo, CASOS.modos);
    const t = textos(entrada.largo, entrada.ancho, r, entrada.colonia, M);
    const obtenido = { m2: r.m2, precio: r.precio, desde: r.desde, total: r.total, rotulo: r.rotulo, aviso: r.aviso, ...t };
    assert.deepStrictEqual(obtenido, esperado, JSON.stringify(entrada));
  }
});

test('mayoreo con menos de 500 m² calcula a precio de solo pasto y lo avisa', () => {
  const r = calcular(10, 10, 'mayoreo', CASOS.modos);
  assert.strictEqual(r.precio, CASOS.modos.solo.precio);
  assert.strictEqual(r.desde, false);
  assert.match(r.aviso, /Te faltan 400 m²/);
});

test('numero acepta coma decimal y rechaza vacíos, negativos y medidas absurdas', () => {
  assert.strictEqual(numero('8,5'), 8.5);
  assert.strictEqual(numero(''), 0);
  assert.strictEqual(numero('-3'), 0);
  assert.strictEqual(numero('1200'), 0);
});

test('el plano conserva la proporción y nunca dibuja menos de 24 unidades', () => {
  const g = plano(8, 6);
  assert.ok(Math.abs(g.w / g.h - 8 / 6) < 1e-9);
  const angosto = plano(100, 1);
  assert.strictEqual(angosto.h, 24);
});

test('el mensaje es texto plano de cinco renglones y termina pidiendo la foto', () => {
  const r = calcular(8, 6, 'instalado', CASOS.modos);
  const renglones = textos(8, 6, r, '', M).mensaje.split('\n');
  assert.strictEqual(renglones.length, 5);
  assert.strictEqual(renglones[4], 'Te mando foto del área.');
});
```

`tools/site/tests/test_medidor_paridad.py`:

```python
"""El Medidor da lo mismo en Python (componentes.py, HTML inicial) y en JavaScript (public/js/vt-medidor.js).
Los casos viven en public/js/tests/casos-medidor.json; node --test los corre contra el JS."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes as c  # noqa: E402
import datos  # noqa: E402

CASOS = json.loads((Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-medidor.json")
                   .read_text(encoding="utf-8"))


class MedidorParidadTest(unittest.TestCase):
    def test_mismos_resultados_que_el_js(self):
        for caso in CASOS["casos"]:
            e = caso["entrada"]
            r = c.calculo_medidor(e["largo"], e["ancho"], e["modo"])
            t = c.textos_medidor(e["largo"], e["ancho"], r, e["colonia"])
            obtenido = {k: r[k] for k in ("m2", "precio", "desde", "total", "rotulo", "aviso")}
            obtenido.update(t)
            with self.subTest(entrada=e):
                self.assertEqual(obtenido, caso["esperado"])

    def test_modos_del_json_son_los_de_datos(self):
        self.assertEqual(CASOS["modos"], {k: {kk: v for kk, v in m.items() if kk != "opcion"}
                                          for k, m in c.MODOS_MEDIDOR.items()})
        self.assertEqual(c.MODOS_MEDIDOR["instalado"]["precio"], datos.PRECIOS["pasto_instalado_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["solo"]["precio"], datos.PRECIOS["pasto_solo_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["mayoreo"]["precio"], datos.PRECIOS["pasto_mayoreo_m2"])
        self.assertEqual(c.MODOS_MEDIDOR["mayoreo"]["minimo"], datos.PRECIOS["pasto_mayoreo_minimo_m2"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Correrlas y ver que fallan**

```bash
cd ~/dev/viverosterra-e2a && node --test public/js/tests/vt-medidor.test.js 2>&1 | grep -E "^ℹ (pass|fail)|Cannot find"
cd tools/site && python3 -m unittest tests/test_medidor_paridad.py 2>&1 | tail -1
```

Expected: `Cannot find module '../vt-medidor.js'` y `ℹ fail 1`; la de Python pasa (`OK`): confirma que `casos-medidor.json` es lo que calcula `componentes.py`.

- [ ] **Step 4: Implementar `public/js/vt-medidor.js`**

```js
// public/js/vt-medidor.js
/* Medidor de m² del híbrido (Etapa 2): largo × ancho → m² → precio en la etiqueta → WhatsApp con la medida.
   Precios y textos llegan en los data-* de cada opción, que escribe tools/site/componentes.py desde datos.py: aquí no
   vive ningún precio. Las mensualidades salen de vt-mensualidades.js (window.VTMensualidades), nunca de una fórmula
   propia. Mismo cálculo que componentes.calculo_medidor / textos_medidor (paridad en tests/casos-medidor.json).
   Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const WA = 'https://wa.me/528333268008?text=';
  const PLANO = { ancho: 360, alto: 190, x: 44, y: 56, minimo: 24 };

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const formatoM2 = (x) => x.toLocaleString('es-MX', { maximumFractionDigits: 1 });
  const n1 = (v) => v.toFixed(1);

  function numero(valor) {
    const n = parseFloat(String(valor == null ? '' : valor).replace(',', '.'));
    return n > 0 && n < 1000 ? n : 0;
  }

  // modos: { instalado: {precio, desde, texto, rotulo}, solo: {...}, mayoreo: {..., minimo} }
  function calcular(largo, ancho, modo, modos) {
    const m = modos[modo];
    const m2 = Math.round(largo * ancho * 10) / 10;
    let precio = m.precio;
    let desde = m.desde;
    let texto = m.texto;
    let rotulo = m.rotulo;
    let aviso = '';
    if (m.minimo && m2 < m.minimo) {
      precio = modos.solo.precio;
      desde = false;
      texto = modos.solo.texto;
      rotulo = `Solo pasto (mayoreo desde ${m.minimo} m²)`;
      aviso = `El mayoreo aplica desde ${m.minimo} m². Te faltan ${Math.ceil(m.minimo - m2)} m²; mientras, calculamos a $${precio}/m² (solo pasto).`;
    }
    return { m2, precio, desde, texto, rotulo, aviso, total: Math.round(m2 * precio) };
  }

  function textos(largo, ancho, r, colonia, M) {
    const medida = `${largo.toFixed(2)} × ${ancho.toFixed(2)} m = ${formatoM2(r.m2)} m²`;
    const desde = r.desde ? 'desde ' : '';
    const disponibles = M.plazosDisponibles(r.total);
    let plan = `Mensualidades con tarjeta de crédito en cotizaciones desde ${dinero(M.minimoDe(3))}.`;
    if (disponibles.length) {
      const ultimo = disponibles[disponibles.length - 1];
      const total = M.totalAPlazos(r.total, ultimo);
      plan = `O ${ultimo} mensualidades de ${dinero(total / ultimo)} con tarjeta de crédito (total ${dinero(total)}).`;
    }
    const cierre = r.desde ? 'Al medir te damos el precio cerrado.' : 'La entrega se cotiza según tu colonia.';
    const mensaje = [`Hola, quiero cotizar ${r.texto}.`, `Medidas: ${medida}`,
      `Estimado de la web: ${desde}${dinero(r.total)} con IVA`, `Colonia: ${colonia || '___'}`,
      'Te mando foto del área.'].join('\n');
    return { medida, monto: dinero(r.total), calc: `${formatoM2(r.m2)} m² × ${desde}$${r.precio}/m², con IVA. ${cierre}`,
      plan, mensaje };
  }

  function plano(largo, ancho) {
    const escala = Math.min(PLANO.ancho / largo, PLANO.alto / ancho);
    const w = Math.max(PLANO.minimo, largo * escala);
    const h = Math.max(PLANO.minimo, ancho * escala);
    return { x: PLANO.x + (PLANO.ancho - w) / 2, y: PLANO.y + (PLANO.alto - h) / 2, w, h };
  }

  function dibujar(svg, largo, ancho, m2) {
    const { x, y, w, h } = plano(largo, ancho);
    const lado = x + w + 22;
    svg.querySelectorAll('[data-vt-plano]').forEach((r) => {
      r.setAttribute('x', n1(x)); r.setAttribute('y', n1(y)); r.setAttribute('width', n1(w)); r.setAttribute('height', n1(h));
    });
    svg.querySelector('[data-vt-cota="arriba"]').setAttribute('d',
      `M${n1(x)} ${n1(y - 26)} v14 M${n1(x + w)} ${n1(y - 26)} v14 M${n1(x)} ${n1(y - 19)} H${n1(x + w)}`);
    const arriba = svg.querySelector('[data-vt-texto="arriba"]');
    arriba.setAttribute('x', n1(x + w / 2)); arriba.setAttribute('y', n1(y - 32)); arriba.textContent = `${largo.toFixed(2)} m`;
    svg.querySelector('[data-vt-cota="lado"]').setAttribute('d',
      `M${n1(lado - 7)} ${n1(y)} h14 M${n1(lado - 7)} ${n1(y + h)} h14 M${n1(lado)} ${n1(y)} V${n1(y + h)}`);
    const costado = svg.querySelector('[data-vt-texto="lado"]');
    costado.setAttribute('transform', `translate(${n1(lado + 20)} ${n1(y + h / 2)}) rotate(-90)`);
    costado.textContent = `${ancho.toFixed(2)} m`;
    const area = svg.querySelector('[data-vt-texto="area"]');
    area.setAttribute('x', n1(x + w / 2)); area.setAttribute('y', n1(y + h / 2 + 9));
    area.textContent = `${formatoM2(m2)} m²`;
    area.style.display = w > 96 && h > 34 ? '' : 'none';
  }

  function leerModos(caja) {
    const modos = {};
    caja.querySelectorAll('input[type="radio"][data-precio]').forEach((i) => {
      modos[i.value] = { precio: Number(i.dataset.precio), desde: i.dataset.desde === '1', texto: i.dataset.texto,
        rotulo: i.dataset.rotulo, minimo: Number(i.dataset.minimo) || 0 };
    });
    return modos;
  }

  function iniciar(caja, M) {
    const campo = (nombre) => caja.querySelector(`[data-vt-campo="${nombre}"]`);
    const salida = (nombre) => caja.querySelector(`[data-vt-o="${nombre}"]`);
    const svg = caja.querySelector('svg');
    const modos = leerModos(caja);
    function actualizar() {
      const largo = numero(campo('largo').value);
      const ancho = numero(campo('ancho').value);
      const elegido = caja.querySelector('input[type="radio"]:checked');
      if (!largo || !ancho || !elegido) {
        salida('monto').textContent = '—';
        salida('calc').textContent = 'Escribe el largo y el ancho de tu patio.';
        salida('plan').textContent = '';
        salida('aviso').hidden = true;
        return;
      }
      const r = calcular(largo, ancho, elegido.value, modos);
      const t = textos(largo, ancho, r, campo('colonia').value.trim(), M);
      dibujar(svg, largo, ancho, r.m2);
      salida('m2').textContent = t.medida;
      salida('rotulo').textContent = r.rotulo;
      salida('monto').textContent = t.monto;
      salida('calc').textContent = t.calc;
      salida('plan').textContent = t.plan;
      salida('aviso').textContent = r.aviso;
      salida('aviso').hidden = !r.aviso;
      salida('cta').setAttribute('href', WA + encodeURIComponent(t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { numero, calcular, textos, plano };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMedidor = Object.freeze(api);
  const arrancar = () => {
    if (!root.VTMensualidades) return; // sin la fórmula oficial no se calcula nada: queda el estimado del HTML
    document.querySelectorAll('[data-vt-medidor]').forEach((caja) => iniciar(caja, root.VTMensualidades));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
```

- [ ] **Step 5: Correr las pruebas**

```bash
cd ~/dev/viverosterra-e2a && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
cd tools/site && python3 -m unittest tests/test_medidor_paridad.py tests/test_reglas.py 2>&1 | tail -1
```

Expected: `ℹ pass 34` y `ℹ fail 0`; `OK` (el JS nuevo no tiene palabras prohibidas).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add public/js/vt-medidor.js public/js/tests/vt-medidor.test.js public/js/tests/casos-medidor.json tools/site/tests/test_medidor_paridad.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(medidor): vt-medidor.js con la fórmula oficial y paridad con Python" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Documento base (`tools/site/plantillas/base.py`)

**Files:**
- Create: `tools/site/plantillas/__init__.py`, `tools/site/plantillas/base.py`, `tools/site/contenido/__init__.py`, `tools/site/tests/test_plantilla_base.py`

- [ ] **Step 1: Escribir la prueba**

`tools/site/tests/test_plantilla_base.py`:

```python
"""Documento base de las páginas con plantilla."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plantillas import base  # noqa: E402

META = {"title": "Título & más", "description": "Descripción \"citada\"", "robots": "index, follow",
        "canonical": "https://www.viverosterra.com/x", "og": (("og:type", "website"), ("og:title", "T"))}


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.html = base.documento(META, "<p>cuerpo</p>", jsonld_bloques=({"@type": "Thing", "name": "a</script>b"},),
                                   precargas=('<link rel="preload" as="image" href="/a.webp">',),
                                   scripts=("/js/a.js",))

    def test_head_con_meta_en_orden_y_regiones_vacias(self):
        h = self.html
        self.assertTrue(h.startswith('<!DOCTYPE html>\n<html lang="es-MX">'))
        self.assertIn("<title>Título &amp; más</title>", h)
        self.assertIn('content="Descripción &quot;citada&quot;"', h)
        self.assertLess(h.index('property="og:type"'), h.index('property="og:title"'))
        for region in ("head", "header", "footer"):
            self.assertIn(f"<!-- vt:{region} -->\n<!-- /vt:{region} -->", h)
        self.assertIn('<body class="vt-pagina">', h)
        self.assertIn('<main id="main">\n<p>cuerpo</p>\n</main>', h)
        self.assertLess(h.index("<!-- /vt:footer -->"), h.index('<script src="/js/a.js" defer></script>'))

    def test_sin_css_viejo_ni_google_fonts(self):
        self.assertNotRegex(self.html, r"fonts\.googleapis|tailwind\.css|design-system\.css|servicios\.css")

    def test_json_ld_compacto_y_seguro(self):
        bloque = re.search(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S).group(1)
        self.assertNotIn("</script>b", bloque)
        self.assertEqual(json.loads(bloque)["name"], "a</script>b")
        self.assertIn('{"@type":"Thing"', bloque)

    def test_precarga_de_imagen_con_srcset(self):
        link = base.precarga_imagen({"src": "/a.webp", "srcset": "/a-640.webp 640w, /a.webp 1024w", "sizes": "100vw"})
        self.assertIn('imagesrcset="/a-640.webp 640w, /a.webp 1024w"', link)
        self.assertIn('fetchpriority="high"', link)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrla y ver que falla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_plantilla_base.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'plantillas'`.

- [ ] **Step 3: Implementar**

`tools/site/plantillas/__init__.py`:

```python
"""Plantillas por tipo de página (spec §3.3). Cada módulo expone render(contenido) -> HTML completo sin el shell."""
```

`tools/site/contenido/__init__.py`:

```python
"""Contenido de las páginas con plantilla: solo datos (textos, fotos, preguntas). Cada módulo expone CONTENIDO y PARIDAD."""
```

`tools/site/plantillas/base.py`:

```python
"""Documento de una página con plantilla: <head> propio (título, descripción, robots, canonical, Open Graph, precargas y
JSON-LD), regiones vacías del shell (las llena tools/site/shell.py) y <main id="main"> con el cuerpo.

Sin Google Fonts ni CSS viejo: las fuentes y terra.css llegan con la región vt:head del shell.
"""
import json
from html import escape


def jsonld(bloque):
    """<script> de JSON-LD compacto; "</" se escapa para que el texto nunca cierre el script."""
    texto = json.dumps(bloque, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + texto.replace("</", "<\\/") + "</script>"


def precarga_imagen(f):
    """<link rel="preload"> de la imagen principal (nunca lazy; spec §3.3)."""
    extra = f' imagesrcset="{escape(f["srcset"])}" imagesizes="{escape(f["sizes"])}"' if f.get("srcset") else ""
    return f'<link rel="preload" as="image" href="{escape(f["src"])}"{extra} fetchpriority="high">'


def documento(meta, cuerpo, *, jsonld_bloques=(), precargas=(), scripts=()):
    """meta: title, description, robots, canonical y og (pares en el orden publicado)."""
    lineas = [
        "<!DOCTYPE html>",
        '<html lang="es-MX">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{escape(meta['title'], quote=False)}</title>",
        f'<meta name="description" content="{escape(meta["description"])}">',
        f'<meta name="robots" content="{escape(meta["robots"])}">',
        f'<link rel="canonical" href="{escape(meta["canonical"])}">',
    ]
    lineas += [f'<meta property="{escape(p)}" content="{escape(v)}">' for p, v in meta["og"]]
    lineas.append('<link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">')
    lineas += list(precargas)
    lineas += [jsonld(b) for b in jsonld_bloques]
    lineas += [
        "<!-- vt:head -->", "<!-- /vt:head -->", "</head>", '<body class="vt-pagina">',
        "<!-- vt:header -->", "<!-- /vt:header -->", '<main id="main">', cuerpo, "</main>",
        "<!-- vt:footer -->", "<!-- /vt:footer -->",
    ]
    lineas += [f'<script src="{escape(s)}" defer></script>' for s in scripts]
    lineas += ["</body>", "</html>", ""]
    return "\n".join(lineas)
```

- [ ] **Step 4: Correr la prueba**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_plantilla_base.py 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/plantillas/__init__.py tools/site/plantillas/base.py tools/site/contenido/__init__.py tools/site/tests/test_plantilla_base.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(plantillas): documento base con head propio y regiones del shell" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: La home sale de su plantilla

**Files:**
- Create: `tools/site/plantillas/inicio.py`, `tools/site/contenido/inicio.py`, `tools/site/generar.py`, `tools/site/tests/test_inicio.py`, `tools/site/tests/test_generar.py`
- Modify: `tools/site/build.py`, `public/index.html`

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_inicio.py`:

```python
"""La home publicada sale de su plantilla con la secuencia del spec §3.3 y los datos oficiales."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

HTML = (paginas.PUBLIC / "index.html").read_text(encoding="utf-8")
MAIN = re.search(r'<main id="main">(.*)</main>', HTML, re.S).group(1)
TEXTO = textos_publicos(HTML)


def ld(tipo):
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S):
        nodo = json.loads(bloque)
        if nodo.get("@type") == tipo:
            return nodo
    raise AssertionError(tipo)


class InicioTest(unittest.TestCase):
    def test_secuencia_de_la_plantilla(self):
        marcas = ('class="vt-portada"', 'class="vt-datos"', 'id="vt-h-que"', 'data-vt-medidor', 'id="vt-h-obras"',
                  'class="vt-logos"', 'id="vt-h-como"', 'id="vt-h-precios"', 'id="vt-h-faq"', 'class="vt-cierre"')
        posiciones = [MAIN.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_h1_y_un_solo_h1(self):
        self.assertEqual(re.findall(r"<h1\b[^>]*>(.*?)</h1>", HTML, re.S),
                         ["Pasto en rollo, jardines y plantas en Tampico y Madero."])

    def test_portada_con_precio_cta_y_foto_principal(self):
        portada = MAIN[:MAIN.index('id="vt-h-que"')]
        self.assertIn("<b>$120</b><span>/m²</span>", portada)
        self.assertIn("<b>$85 /m²</b>", portada)
        self.assertIn("data-hero-cta", portada)
        self.assertIn('data-cta="home:hero"', portada)
        self.assertIn('href="#medidor"', portada)
        self.assertIn('loading="eager" fetchpriority="high"', portada)
        self.assertIn('<link rel="preload" as="image" href="/img/obra/cuadrilla-tendiendo-pasto-san-agustin.webp"', HTML)

    def test_datos_y_copy_del_dueno(self):
        for frase in (datos.PROMESA_COMPLETA, datos.GOOGLE, datos.M2_INSTALADOS, f"REPSE {datos.REPSE}",
                      "Obregón 209 Sur", datos.LLEGADA_PASTO, datos.ANTICIPO, datos.PRIMER_RIEGO,
                      "la reponemos sin costo", f"{datos.CLIENTES} clientes · {datos.INSTALACIONES} instalaciones"):
            with self.subTest(frase=frase):
                self.assertIn(frase, TEXTO)
        for cliente in datos.CLIENTES_B2B:
            self.assertIn(f'alt="{cliente}"', HTML)
        self.assertIn('href="/politicas"', MAIN)

    def test_sin_css_viejo_ni_google_fonts(self):
        self.assertNotRegex(HTML, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
        self.assertEqual(len(re.findall(r"<style\b", HTML)), 0)

    def test_scripts_del_medidor_en_orden(self):
        self.assertLess(HTML.index('src="/js/vt-mensualidades.js"'), HTML.index('src="/js/vt-medidor.js"'))

    def test_mensajes_de_whatsapp_con_contexto_y_firma(self):
        for cta in ("home:hero", "home:cierre"):
            href = re.search(rf'data-cta="{cta}" href="https://wa\.me/528333268008\?text=([^"]+)"', HTML).group(1)
            texto = unquote(href)
            with self.subTest(cta=cta):
                self.assertTrue(texto.startswith(datos.MENSAJES["general"]))
                self.assertTrue(texto.endswith(datos.FIRMA))

    def test_json_ld_conservado_y_faq_igual_a_la_visible(self):
        self.assertEqual(ld("LocalBusiness")["@id"], f"{datos.SITIO}/#negocio")
        faq = ld("FAQPage")
        visibles = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<summary>(.*?)</summary>", MAIN)]
        self.assertEqual([q["name"] for q in faq["mainEntity"]], visibles)
        self.assertEqual(len(visibles), 6)
        self.assertEqual(faq["mainEntity"][0]["acceptedAnswer"]["text"], datos.RESPUESTA_PRECIO_PASTO)
        ld("BreadcrumbList")

    def test_una_sola_etiqueta_de_precio_en_la_portada(self):
        portada = MAIN[:MAIN.index('id="vt-h-que"')]
        self.assertEqual(portada.count('class="vt-etiqueta"'), 1)


if __name__ == "__main__":
    unittest.main()
```

`tools/site/tests/test_generar.py` (versión de esta tarea: solo la home registrada; la Tarea 9 agrega pasto en rollo):

```python
"""generar.py escribe las páginas con plantilla ya con el shell, y solo si cambian."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402


class GenerarTest(unittest.TestCase):
    def test_paginas_registradas_tienen_contexto(self):
        self.assertEqual([r for r, *_ in generar.PAGINAS], ["/"])
        for ruta, salida, _p, _c in generar.PAGINAS:
            paginas.contexto(ruta)
            self.assertEqual(paginas.ruta_de(paginas.PUBLIC / salida), ruta)

    def test_lo_publicado_es_lo_que_sale_de_la_plantilla(self):
        urls = activos.urls()
        for ruta, salida, plantilla, contenido in generar.PAGINAS:
            with self.subTest(ruta=ruta):
                publicado = (paginas.PUBLIC / salida).read_text(encoding="utf-8")
                self.assertEqual(generar.renderizar(ruta, plantilla, contenido, urls), publicado)
                self.assertEqual(shell.aplicar(publicado, ruta, urls), publicado)

    def test_escribe_solo_si_cambia(self):
        urls = activos.urls()
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            self.assertEqual(generar.escribir_todo(urls, destino), len(generar.PAGINAS))
            self.assertEqual(generar.escribir_todo(urls, destino), 0)
            for _r, salida, _p, _c in generar.PAGINAS:
                self.assertEqual((destino / salida).read_text(encoding="utf-8"),
                                 (paginas.PUBLIC / salida).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrlas y ver que fallan**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_inicio.py tests/test_generar.py 2>&1 | tail -3`
Expected: errores (`ModuleNotFoundError: No module named 'generar'` y fallas de `test_inicio`, porque la home publicada aún es la vieja: `test_h1_y_un_solo_h1` muestra `Jardinería en Tampico, …`).

- [ ] **Step 3: Contenido de la home**

`tools/site/contenido/inicio.py` (copy de `docs/diseno/hibrido/index.html` con datos vivos; `PARIDAD` dice a dónde fue cada elemento de la captura de la Tarea 1):

```python
"""Contenido de la home (/). Solo datos: la plantilla es tools/site/plantillas/inicio.py.

Copy de la maqueta aprobada (docs/diseno/hibrido/index.html) con los datos vivos de datos.py. Título, descripción,
canonical, Open Graph y JSON-LD de negocio y migas se conservan como estaban publicados (los títulos se reescriben en la
Etapa 3 y el grafo único llega en la Etapa 4). PARIDAD dice a dónde fue cada encabezado, pregunta, precio o enlace de la
página anterior que ya no aparece igual (prueba: tools/site/tests/test_paridad.py).
"""
import datos
from componentes import dinero

P = datos.PRECIOS
MINIMO = P["pasto_mayoreo_minimo_m2"]
EMPRESAS = f"{', '.join(datos.CLIENTES_B2B[:-1])} y {datos.CLIENTES_B2B[-1]}"
DESCRIPCION = (f"Pasto San Agustín desde ${P['pasto_solo_m2']}/m², diseño de jardines y mantenimiento en Tampico. "
               f"+18 años · {datos.CLIENTES} clientes · Cotización gratis hoy.")

META = {
    "title": "Viveros Terra · Jardinería, Pasto en Rollo y Paisajismo en Tampico",
    "description": DESCRIPCION,
    "robots": "index, follow",
    "canonical": f"{datos.SITIO}/",
    "og": (
        ("og:type", "website"),
        ("og:url", datos.SITIO),
        ("og:title", "Viveros Terra · Jardinería y Pasto en Rollo en Tampico"),
        ("og:description", DESCRIPCION),
        ("og:image", f"{datos.SITIO}/img/jardin-diseno-paisajismo-pasto-san-agustin-tampico-og.webp"),
        ("og:image:width", "1200"),
        ("og:image:height", "630"),
        ("og:locale", "es_MX"),
        ("og:site_name", "Viveros Terra Tampico"),
    ),
}

NEGOCIO = {
    "@type": "LocalBusiness",
    "@id": f"{datos.SITIO}/#negocio",
    "foundingDate": datos.FUNDACION,
    "name": datos.NOMBRE,
    "hasMap": datos.MAPS_URL,
    "description": ("Especialistas en pasto en rollo San Agustín, venta e instalación de pasto sintético, diseño de "
                    "jardines, sistemas de riego y mantenimiento de áreas verdes en Tampico, Ciudad Madero y Altamira, "
                    "Tamaulipas."),
    "url": datos.SITIO,
    "telephone": datos.TELEFONO_TEL,
    "email": datos.CORREO_FORMULARIOS,
    "image": f"{datos.SITIO}/img/jardineria-areas-verdes-tampico.jpg",
    "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE, "addressLocality": datos.CIUDAD,
                "addressRegion": "Tamaulipas", "postalCode": datos.CP, "addressCountry": "MX"},
    "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "09:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"},
    ],
    "sameAs": ["https://www.facebook.com/viverosterra/", "https://www.instagram.com/viverosterramx",
               "https://www.linkedin.com/company/viveros-terra-tampico"],
    "priceRange": "$$",
    "areaServed": ["Tampico", "Ciudad Madero", "Altamira", "Pánuco", "Tuxpan", "Victoria", "Tampico Centro",
                   "Madero Norte", "Madero Sur", "Altamira Industrial"],
}

MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": i, "name": nombre, "item": f"{datos.SITIO}{ruta}"}
    for i, (nombre, ruta) in enumerate((("Inicio", ""), ("Pasto en Rollo Tampico", "/pasto-en-rollo-tampico"),
                                         ("Plantas y Palmas", "/plantas-palmas-arboles-tampico"),
                                         ("Diseño de Jardines", "/diseno-jardines-tampico"),
                                         ("Catálogo", "/catalogo")), 1)]}

OBRA = "/img/obra"

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Dónde comprar pasto en rollo en Tampico?",
     f"En Viveros Terra: {datos.DOMICILIO_COMPLETO}, {datos.REFERENCIA[0].lower()}{datos.REFERENCIA[1:]}. Somos vivero "
     f"productor de pasto San Agustín en la zona conurbada de Tampico desde {datos.DESDE}, con {datos.INSTALACIONES} "
     "instalaciones. Entregamos en Tampico, Madero y Altamira."),
    ("¿Qué pasto es mejor para el clima de Tampico?",
     "El pasto San Agustín (<i>Stenotaphrum secundatum</i>): resiste el calor y la humedad del Golfo, tolera media "
     "sombra y pide poco mantenimiento. Para jardines finos conviene el japonés y para alto tráfico, el Bermuda."),
    ("¿Cuánto cuesta el mantenimiento de jardín en Tampico?",
     f"Los planes inician desde ${P['mantenimiento_mes']}/mes para jardines residenciales. El precio depende del "
     "tamaño y la frecuencia, e incluye poda, fertilización y control de plagas. "
     '<a href="/mantenimiento-jardines-tampico">Ver los planes de mantenimiento</a>.'),
    ("¿El diseño de jardín tiene costo?",
     f"El Plan Terra de diseño cuesta desde {dinero(P['diseno'])}. En los planes Esencial y Completo, el costo del diseño "
     "se descuenta íntegramente si contratas la ejecución con nosotros. "
     '<a href="/diseno-jardines-tampico">Ver los planes de diseño</a>.'),
    ("¿Trabajan con empresas e industria?",
     f"Sí. Tenemos registro REPSE {datos.REPSE}, facturamos {datos.FACTURA} y entregamos por etapas según el avance de "
     f"obra. Nos han contratado {EMPRESAS}. "
     f'<a href="/mayoreo-pasto-tampico">Mayoreo de pasto</a> desde {MINIMO} m².'),
)

CONTENIDO = {
    "meta": META,
    "jsonld": {"negocio": NEGOCIO, "migas": MIGAS_LD, "speakable": ("h1", "h2", ".vt-faq summary")},
    "portada": {
        "kicker": "Vivero y jardinería · Tampico, Madero y Altamira",
        "h1": "Pasto en rollo, jardines y plantas en Tampico y Madero.",
        "lede": (f"Somos vivero y cuadrilla en Cd. Madero desde {datos.DESDE}. Vendemos pasto San Agustín en rollo, "
                 f"diseñamos y cuidamos jardines, y tenemos {datos.VARIEDADES} variedades de plantas. "
                 "El precio va por delante."),
        "etiqueta": {
            "codigo": "Pasto · 01", "aviso": "Con IVA", "nombre": "Pasto San Agustín",
            "cientifico": "Stenotaphrum secundatum", "antes": "San Agustín instalado · desde",
            "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m²",
            "filas": (("Solo pasto, tú lo instalas", f"{dinero(P['pasto_solo_m2'])} /m²"),),
            "nota": (f"Ejemplo: 8 × 6 m = 48 m² instalado × {dinero(P['pasto_instalado_m2'])} = "
                     f"{dinero(48 * P['pasto_instalado_m2'])}."),
        },
        "mensaje": datos.MENSAJES["general"],
        "tambien": ('<a href="#medidor">Calcula tu patio</a> · También: <a href="/diseno-jardines-tampico">diseño</a> · '
                    '<a href="/mantenimiento-jardines-tampico">mantenimiento</a> · '
                    '<a href="/sistema-riego-tampico">riego</a> · <a href="/palmas-tropicales-tampico">palmas</a> · '
                    '<a href="/mayoreo-pasto-tampico">empresas</a> · '
                    '<a href="/pasto-sintetico">pasto sintético con envío</a>'),
        "foto": {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin.webp",
                 "srcset": (f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp 640w, "
                            f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin.webp 1024w"),
                 "sizes": "(min-width:1024px) 40vw, 100vw", "ancho": 1024, "alto": 1536,
                 "alt": "Integrante de la cuadrilla de Viveros Terra tendiendo rollos de pasto San Agustín en un jardín.",
                 "numero": 1, "lugar": "Zona Tampico–Madero · tendido de tepes", "etapa": "Tepe de 40 × 60 cm"},
    },
    "que_hacemos": {
        "titulo": "Cinco formas de trabajar con nosotros, cada una con su precio.",
        "lede": ("Para que llegues a la plática sabiendo cuánto cuesta. Donde dice “desde”, el total depende de tus "
                 "metros y del terreno."),
        "items": (
            {"titulo": "Pasto natural", "href": "/pasto-en-rollo-tampico",
             "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
             "texto": (f"San Agustín en rollo, cortado para tu pedido. {dinero(P['pasto_solo_m2'])}/m² solo pasto; "
                       "instalado en un día."),
             "desde": dinero(P["pasto_instalado_m2"]), "unidad": "/m² instalado"},
            {"titulo": "Pasto sintético", "href": "/pasto-sintetico",
             "img": "/img/pasto-sintetico/galeria/toscana-28-1-sm.webp", "ancho": 420, "alto": 560,
             "texto": (f"9 modelos con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}. El envío se cobra por "
                       'rollo, según tu estado. ¿En Tampico? <a href="/pasto-sintetico-tampico">Lo instalamos</a>.'),
             "desde": dinero(P["sintetico_tienda_m2"]), "unidad": "/m² material"},
            {"titulo": "Diseño, mantenimiento y riego", "href": "/mantenimiento-jardines-tampico",
             "img": f"{OBRA}/mantenimiento-jardin-poda-tampico.webp", "ancho": 640, "alto": 960,
             "texto": (f'Plan Terra de <a href="/diseno-jardines-tampico">diseño</a> desde {dinero(P["diseno"])}. '
                       "Mantenimiento con poda, fertilización y control de plagas. "
                       f'<a href="/sistema-riego-tampico">Riego automático</a> desde {dinero(P["riego_m2"][0])}/m².'),
             "desde": dinero(P["mantenimiento_mes"]), "unidad": "/mes"},
            {"titulo": "Plantas y palmas", "href": "/plantas-palmas-arboles-tampico",
             "img": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961,
             "texto": (f"{datos.VARIEDADES} variedades en el vivero. Las que sembramos nosotros llevan 30 días de "
                       "garantía de arraigo, con el riego indicado."),
             "desde": dinero(P["palma_desde"]), "unidad": "palma chica"},
            {"titulo": "Empresas y constructoras", "href": "/mayoreo-pasto-tampico",
             "img": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600,
             "texto": (f"Mayoreo de pasto (solo pasto) desde {MINIMO} m², "
                       '<a href="/palmas-mayoreo-proyectos">palmas para proyectos</a>, mantenimiento recurrente y '
                       f"entrega por etapas. REPSE {datos.REPSE} y {datos.FACTURA}."),
             "desde": dinero(P["pasto_mayoreo_m2"]), "unidad": "/m² mayoreo"},
        ),
    },
    "medidor": {
        "titulo": "Mide tu patio. Te decimos cuánto cuesta.",
        "lede": ("Escribe el largo y el ancho, como si caminaras el jardín con una cinta. El cálculo se llena en la "
                 "etiqueta y viaja contigo al WhatsApp: no lo tienes que explicar dos veces."),
    },
    "obras": {
        "titulo": "Fotos de obra, no de catálogo.",
        "lede": "Cada foto lleva su pie: dónde y en qué etapa. Así ves lo que entregamos, no una promesa.",
        "figuras": (
            {"src": f"{OBRA}/jardin-residencial-pasto-san-agustin.webp", "ancho": 1280, "alto": 720, "numero": 2,
             "alt": "Jardín residencial con pasto San Agustín recién instalado.",
             "lugar": "Zona Tampico–Madero · jardín residencial", "etapa": "Pasto natural"},
            {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 3,
             "alt": "Pasto San Agustín recién instalado junto a un andador.", "lugar": "Después",
             "etapa": "Día de instalación"},
            {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 4,
             "alt": "Rollos de pasto San Agustín recién cortados en la camioneta de reparto.",
             "lugar": "Rollos recién cortados", "etapa": "En la camioneta de reparto"},
            {"src": f"{OBRA}/instalacion-tuberia-riego-jardin.webp", "ancho": 900, "alto": 600, "numero": 5,
             "alt": "Cuadrilla de Viveros Terra instalando tubería de riego en un jardín.", "lugar": "Riego automático",
             "etapa": "Instalación de tubería"},
            {"src": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961, "numero": 6,
             "alt": "Palmas en costal listas para entrega en el patio del vivero.", "lugar": "Patio del vivero",
             "etapa": "Palmas para entrega"},
        ),
        "titulo_clientes": "Empresas que nos han contratado",
    },
    "proceso": {
        "titulo": "Cuatro pasos. Cada quien sabe qué le toca.",
        "lede": ("Lo que hace que un jardín se logre es repartir bien el trabajo. Por eso cada paso dice de quién es."),
        "pasos": (
            {"titulo": "Nos mandas medidas y foto", "quien": "tu", "cuando": "Día 0 · por WhatsApp",
             "texto": f"Tu colonia, los metros aproximados y una foto del espacio. {datos.PROMESA}."},
            {"titulo": "Medimos y decidimos", "quien": "juntos", "cuando": "Visita sin costo",
             "texto": ("Recorremos el espacio contigo. Si hace falta tierra negra o nivelación, te decimos cuánto cuesta "
                       f"antes de empezar. {datos.ANTICIPO}")},
            {"titulo": "Instalamos en un día", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": f"El pasto llega del campo {datos.LLEGADA_PASTO}, se corta para tu pedido y va directo a tu jardín."},
            {"titulo": "El primer riego", "quien": "tu", "cuando": "Días 1 a 20",
             "texto": (f"{datos.PRIMER_RIEGO} Si una sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo, "
                       'siguiendo el protocolo de riego (<a href="/politicas">ver condiciones</a>).')},
        ),
    },
    "precios": {
        "titulo": "Lista de precios, sin letra chica.",
        "lede": ("Con IVA. Donde dice “desde”, el total depende de tus metros y del terreno: al medir te damos el precio "
                 "cerrado."),
        "nota": ("En sombra profunda el San Agustín no prende. Si es tu caso, te lo decimos al medir, antes de cobrarte "
                 "nada.", "Desde el vivero, Obregón 209 Sur"),
        "filas": (
            {"nombre": "Pasto San Agustín instalado", "unidad": "/m²", "precio": P["pasto_instalado_m2"], "desde": True,
             "rec": True, "detalle": (f"Preparación básica del suelo, tendido en un día y garantía de arraigo de "
                                      f"{datos.ARRAIGO}.")},
            {"nombre": "Pasto San Agustín, solo el pasto", "unidad": "/m²", "precio": P["pasto_solo_m2"],
             "detalle": "Se corta para tu pedido. Recoges en el vivero o te lo llevamos."},
            {"nombre": "Mayoreo de pasto, solo pasto", "unidad": "/m²", "precio": P["pasto_mayoreo_m2"], "desde": True,
             "detalle": f"Pedidos de {MINIMO} m² o más, con entregas por etapas y factura {datos.FACTURA}."},
            {"nombre": "Pasto sintético, material", "unidad": "/m²", "precio": P["sintetico_tienda_m2"], "desde": True,
             "detalle": "9 modelos en rollos de 50 m². Envío a todo México, cobrado por rollo según tu estado."},
            {"nombre": "Mantenimiento de jardín", "unidad": "/mes", "precio": P["mantenimiento_mes"], "desde": True,
             "detalle": "Poda, fertilización y control de plagas. Residencial e industrial."},
            {"nombre": "Diseño de jardín, Plan Terra", "unidad": "/proyecto", "precio": P["diseno"], "desde": True,
             "detalle": "Visita, propuesta de diseño y lista de materiales."},
            {"nombre": "Tierra negra vegetal", "unidad": "/costal", "precio": P["tierra_negra_costal"],
             "detalle": f"También por m³ ({dinero(P['tierra_negra_m3'])}) y en camión volteo."},
            {"nombre": "Tezontle rojo", "unidad": "/costal", "precio": P["tezontle_costal"], "desde": True,
             "detalle": "También por m³ y en camión volteo de 14 m³."},
        ),
        "caption": (f'Precios {datos.ANIO} con IVA incluido. Lista completa en '
                    '<a href="/precios">viverosterra.com/precios</a>.'),
    },
    "faq": {
        "titulo": "Lo que nos preguntan antes de empezar.",
        "preguntas": PREGUNTAS,
        "titulo_guias": "Guías para el clima de Tampico",
        "guias": (
            ("7 árboles para banqueta que no levantan el pavimento", "/blog/arboles-para-sembrar-en-banqueta"),
            ("Palma del viajero: guía de cuidados en Tampico", "/blog/cuidados-palma-del-viajero-ravenala"),
            ("Pasto San Agustín o japonés: cuál conviene en Tampico", "/blog/pasto-san-agustin-vs-japones"),
            ("Cuándo plantar pasto en Tampico: calendario mes a mes", "/blog/cuando-plantar-pasto-tampico-calendario"),
            ("12 plantas resistentes a la sal del Golfo en Tampico", "/blog/plantas-resistentes-sal-golfo-tampico"),
            ("¿Conviene el riego automático en Tampico?", "/blog/sistema-riego-automatico-conviene-tampico"),
        ),
    },
    "cierre": {
        "titulo": "Mándanos tus medidas y una foto del espacio.",
        "lede": "Tu colonia, los metros aproximados y qué quieres hacer. Si hace falta, vamos a medir sin costo.",
        "mensaje": datos.MENSAJES["general"],
    },
}

# Elemento de la home anterior → elemento nuevo que lo cubre, o motivo de su retiro (tests/paridad/index.json).
SERVICIOS_EN_INDICE = "Ahora es una fila del índice “Cinco formas de trabajar con nosotros”, con su precio."
GUIA_EN_LISTA = "Sigue enlazada desde la lista “Guías para el clima de Tampico”, con el mismo texto de enlace."
PASOS_VIEJOS = "Los 5 pasos genéricos se reemplazan por los 4 pasos con NOSOTROS / TÚ / JUNTOS (spec §4.1)."
PARIDAD = {
    "reemplazos": {
        "Jardinería en Tampico, pasto en rollo y vivero desde 2007.": "Pasto en rollo, jardines y plantas en Tampico y Madero.",
        "¿Cuánto cuesta tu jardín?": "Mide tu patio. Te decimos cuánto cuesta.",
        "Todo lo que tu jardín necesita, en un solo lugar": "Cinco formas de trabajar con nosotros, cada una con su precio.",
        "Pasto en Rollo San Agustín": "Pasto natural",
        "Diseño de Jardines": "Diseño, mantenimiento y riego",
        "Sistema de riego automatizado": "Diseño, mantenimiento y riego",
        "Mantenimiento Profesional": "Diseño, mantenimiento y riego",
        "Plantas, palmas y árboles": "Plantas y palmas",
        "Empresa / Comercial": "Empresas y constructoras",
        "Proyecto B2B": "Empresas y constructoras",
        "¿Proyecto grande o mayoreo?": "Empresas y constructoras",
        "Jardines que hemos hecho en Tampico": "Fotos de obra, no de catálogo.",
        "Así de fácil es trabajar con nosotros": "Cuatro pasos. Cada quien sabe qué le toca.",
        "Nos escribes": "Nos mandas medidas y foto",
        "Preguntas frecuentes sobre pasto y jardinería en Tampico": "Lo que nos preguntan antes de empezar.",
        "Tu jardín ideal está a un mensaje de distancia": "Mándanos tus medidas y una foto del espacio.",
        "Cotización por WhatsApp": "Mándanos tus medidas y una foto del espacio.",
    },
    "retirados": {
        "Viveros Terra: vivero y empresa de jardinería en Tampico y Madero desde 2007": (
            "El párrafo de entidad pasa al lede de la portada y al cuadro de datos; la página de entidad es /nosotros "
            "(Etapa 3)."),
        "Residencial": "La bifurcación por cliente es ahora el índice de cinco rutas con precio (spec §3.3).",
        "Antes y después de instalar pasto en Tampico": (
            "El deslizador y su contador “Respondemos en 2:00 hrs” (promesa vieja) se retiran; el después queda como "
            "Fig. 03."),
        "Cotización rápida": PASOS_VIEJOS,
        "Agendamos": PASOS_VIEJOS,
        "Instalación": PASOS_VIEJOS,
        "Jardín listo": PASOS_VIEJOS,
        "¿Por qué elegir Viveros Terra?": "Sus cifras quedan en el cuadro de datos y en la línea de prueba (desde 2007, "
                                          "+1,500 instalaciones, 4.6 en Google).",
        "Conocimiento del clima local": "Queda en la respuesta “¿Qué pasto es mejor para el clima de Tampico?”.",
        "Servicio integral, una sola empresa": "Lo dice el índice de cinco rutas.",
        "Respuesta en menos de 1 hora en horario": "Es la promesa única debajo de cada CTA.",
        "Materiales para jardín en Tampico": "Tierra negra y tezontle van en la lista de precios; los cuatro materiales "
                                             "siguen en el menú y en el pie.",
        "Pasto San Agustín": SERVICIOS_EN_INDICE,
        "Tierra Negra Vegetal": "Fila “Tierra negra vegetal” de la lista de precios.",
        "Tezontle Rojo": "Fila “Tezontle rojo” de la lista de precios.",
        "Mármol y Piedra": "Mármol blanco y piedra bola siguen en el menú y en el pie.",
        "Lo que dicen nuestros clientes en Tampico": (
            "Testimonios con nombre sin verificar: la regla del dueño prohíbe testimonios inventados. Queda la línea "
            "estática “4.6 en Google (24 reseñas)” y los clientes B2B autorizados."),
        "Cobertura de Servicio en Tamaulipas y Veracruz": "Las 6 zonas siguen enlazadas desde el pie; /zonas llega en la "
                                                          "Etapa 3.",
        "7 árboles para banqueta que no levantan el pavimento": GUIA_EN_LISTA,
        "Palma del viajero: guía de cuidados en Tampico": GUIA_EN_LISTA,
        "Pasto San Agustín o japonés: cuál conviene en Tampico": GUIA_EN_LISTA,
        "Cuándo plantar pasto en Tampico: calendario mes a mes": GUIA_EN_LISTA,
        "12 plantas resistentes a la sal del Golfo en Tampico": GUIA_EN_LISTA,
        "¿Conviene el riego automático en Tampico?": GUIA_EN_LISTA,
        "¿Cuánto ahorra un sistema de riego automatizado?": "Vive en /sistema-riego-tampico; la home deja 6 preguntas "
                                                            "(spec §3.3).",
        "¿Hacen envíos de pasto fuera de Tampico?": "Respondida en /pasto-en-rollo-tampico (“¿Hacen entrega fuera de "
                                                    "Tampico?”).",
        "$0": "Era el marcador vacío del cotizador viejo (“$0 – $0”).",
    },
}
```

- [ ] **Step 4: Plantilla de la home**

`tools/site/plantillas/inicio.py`:

```python
"""Plantilla de la home (spec §3.3): portada con precio y CTA en el primer pantallazo móvil → cuadro de datos → qué
hacemos (cada ruta con su precio) → Medidor → obras con pies FIG. y clientes → proceso NOSOTROS / TÚ → precios →
preguntas → CTA final. El contenido vive en tools/site/contenido/inicio.py."""
import componentes as c
from plantillas import base

TIPO = "home"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/vt-medidor.js")
CONTEXTO = "https://schema.org"


def render(k):
    q, m, o, pr, pc, f, ci = (k[s] for s in ("que_hacemos", "medidor", "obras", "proceso", "precios", "faq", "cierre"))
    cuerpo = "\n".join((
        c.portada(k["portada"], TIPO),
        c.bloque(1, "Qué hacemos", "vt-h-que", q["titulo"], c.indice(q["items"]), lede=q["lede"]),
        c.bloque(2, "Medidor", "vt-h-medidor", m["titulo"], c.medidor("inicio", TIPO), lede=m["lede"], tinte=True,
                 id_seccion="medidor"),
        c.bloque(3, "Jardines entregados", "vt-h-obras", o["titulo"],
                 c.obras(o["figuras"]) + c.linea_prueba() + f'<h3 class="vt-mt">{o["titulo_clientes"]}</h3>' + c.logos(),
                 lede=o["lede"]),
        c.bloque(4, "Cómo trabajamos", "vt-h-como", pr["titulo"], c.pasos(pr["pasos"]), lede=pr["lede"], tinte=True),
        c.bloque_dos(5, "Precios", "vt-h-precios", pc["titulo"], f'<p class="vt-lede">{pc["lede"]}</p>' + c.nota(*pc["nota"]),
                     c.tabla_precios(pc["filas"], pc["caption"]) + c.planes_mensualidades(), id_seccion="precios"),
        c.bloque_dos(6, "Preguntas", "vt-h-faq", f["titulo"], f'<h3 class="vt-mt">{f["titulo_guias"]}</h3>' + c.guias(f["guias"]),
                     c.faq(f["preguntas"]), tinte=True),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], TIPO),
    ))
    j = k["jsonld"]
    bloques = (
        {"@context": CONTEXTO, **j["negocio"]},
        {"@context": CONTEXTO, **c.faq_jsonld(f["preguntas"], speakable=j["speakable"])},
        {"@context": CONTEXTO, **j["migas"]},
    )
    return base.documento(k["meta"], cuerpo, jsonld_bloques=bloques,
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=SCRIPTS)
```

- [ ] **Step 5: Registro de páginas con plantilla**

`tools/site/generar.py` (versión de esta tarea):

```python
"""Páginas que salen de plantillas (Etapa 2). Cada entrada es (ruta, archivo en public/, plantilla, contenido): la
plantilla vive en tools/site/plantillas/<plantilla>.py y el contenido en tools/site/contenido/<contenido>.py.

Escribe cada página con el shell ya aplicado y solo si cambia, así una segunda corrida de build.py no toca nada. Para
migrar otro tipo de página: agrega su contenido, su plantilla (o reutiliza una) y su fila aquí.
"""
import importlib
from pathlib import Path

import paginas
import shell

PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
)


def contenido_de(ruta):
    return next(contenido for r, _a, _p, contenido in PAGINAS if r == ruta)


def renderizar(ruta, plantilla, contenido, urls):
    """HTML final de la página: plantilla + contenido + shell."""
    modulo_plantilla = importlib.import_module(f"plantillas.{plantilla}")
    modulo_contenido = importlib.import_module(f"contenido.{contenido}")
    return shell.aplicar(modulo_plantilla.render(modulo_contenido.CONTENIDO), ruta, urls)


def escribir_todo(urls, public=paginas.PUBLIC):
    """Escribe las páginas con plantilla que cambiaron; devuelve cuántas escribió."""
    escritas = 0
    for ruta, salida, plantilla, contenido in PAGINAS:
        path = Path(public) / salida
        html = renderizar(ruta, plantilla, contenido, urls)
        if path.is_file() and path.read_text(encoding="utf-8") == html:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        escritas += 1
    return escritas
```

- [ ] **Step 6: El build escribe las páginas con plantilla**

En `tools/site/build.py`:
1. Reemplaza el docstring del módulo por:

```python
"""Punto de entrada único del sitio: genera las páginas de pasto, publica los assets del shell con hash, escribe las
páginas con plantilla (tools/site/generar.py) y aplica el shell a todas las páginas de public/. CI verifica que
correrlo deje public/ sin cambios.

Uso: python3 tools/site/build.py   (desde cualquier carpeta)
"""
```

2. Debajo de `import activos  # noqa: E402` agrega `import generar  # noqa: E402`.
3. En `main()`, entre `urls = activos.publicar()` y `cambiadas = shell.aplicar_todo(urls)`, agrega:

```python
    escritas = generar.escribir_todo(urls)
    print(f"plantillas: {escritas} de {len(generar.PAGINAS)} páginas escritas")
```

- [ ] **Step 7: Build dos veces, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /
cd tools/site && python3 -m unittest tests/test_inicio.py tests/test_generar.py tests/test_consistencia.py tests/test_reglas.py tests/test_enlaces.py tests/test_sitio.py 2>&1 | tail -1
```

Expected: `plantillas: 1 de 1 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; luego `plantillas: 0 de 1 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; el informe dice `ok` en `encabezados`, `faq`, `precios`, `enlaces`, `meta` y `jsonld_tipos`; `OK`.

- [ ] **Step 8: Revisión visual rápida**

```bash
cd ~/dev/viverosterra-e2a && python3 tools/site/capturas.py /tmp/vt-e2a-t8 | tail -4
```

Expected: `30 capturas …` y ningún `/ a …px` en el reporte de desbordamiento. Abre `/tmp/vt-e2a-t8/inicio-375.png` e `/tmp/vt-e2a-t8/inicio-1440.png`: H1, etiqueta amarilla con $120 y el botón verde dentro del primer pantallazo a 375; foto con pie `FIG. 01` a la derecha a 1440.

- [ ] **Step 9: Commit**

```bash
cd ~/dev/viverosterra-e2a
git status --short
git add tools/site/plantillas/inicio.py tools/site/contenido/inicio.py tools/site/generar.py tools/site/build.py tools/site/tests/test_inicio.py tools/site/tests/test_generar.py public/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(inicio): la home sale de su plantilla con Medidor, precio y CTA en el primer pantallazo" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Pasto en rollo sale de la plantilla de servicio

**Files:**
- Create: `tools/site/plantillas/servicio.py`, `tools/site/contenido/pasto_en_rollo.py`, `tools/site/tests/test_pasto_en_rollo.py`
- Modify: `tools/site/generar.py`, `tools/site/tests/test_generar.py`, `tools/servicios/pages.py`, `tools/servicios/simulador.py`, `tools/servicios/tests/test_pagos.py`, `public/pasto-en-rollo-tampico/index.html`

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_pasto_en_rollo.py`:

```python
"""/pasto-en-rollo-tampico sale de la plantilla de servicio con la secuencia del spec §3.3 y el copy del dueño."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import datos  # noqa: E402
import paginas  # noqa: E402
from test_reglas import textos_publicos  # noqa: E402

HTML = (paginas.PUBLIC / "pasto-en-rollo-tampico" / "index.html").read_text(encoding="utf-8")
MAIN = re.search(r'<main id="main">(.*)</main>', HTML, re.S).group(1)
TEXTO = textos_publicos(HTML)
GRAFO = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1))["@graph"]


def nodo(tipo):
    return next(n for n in GRAFO if n["@type"] == tipo)


class PastoEnRolloTest(unittest.TestCase):
    def test_secuencia_de_servicio_local(self):
        marcas = ('class="vt-crumbs"', "<h1", 'class="vt-etiqueta"', 'data-cta="servicio-pasto:hero"',
                  'class="vt-datos"', 'id="vt-h-prueba"', 'id="vt-h-precio"', "data-vt-medidor", 'id="vt-h-conviene"',
                  'id="vt-h-proceso"', 'id="vt-h-garantia"', 'id="vt-h-pago"', "data-simulador", 'id="vt-h-faq"',
                  'class="vt-cierre"', 'id="vt-h-rel"')
        posiciones = [MAIN.index(m) for m in marcas]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_un_h1_con_beneficio_y_lugar(self):
        h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", HTML, re.S)
        self.assertEqual(len(h1), 1)
        self.assertTrue(h1[0].startswith("Pasto San Agustín en rollo, instalado en un día."))

    def test_copy_del_dueno(self):
        for frase in (datos.ANTICIPO, f"llega del campo {datos.LLEGADA_PASTO}", datos.PRIMER_RIEGO,
                      "si una sección no arraiga en 15 a 20 días, la reponemos sin costo", datos.PROMESA_COMPLETA,
                      "¿Cuál te conviene según tu espacio?", datos.M2_INSTALADOS):
            with self.subTest(frase=frase):
                self.assertIn(frase, TEXTO)
        self.assertEqual(TEXTO.count("Cortado para tu pedido"), 2)
        self.assertIn('href="/politicas"', MAIN)
        self.assertIn('href="/mayoreo-pasto-tampico"', MAIN)
        self.assertIn('href="/protocolo-cuidados-pasto-san-agustin"', MAIN)

    def test_ctas_con_mensaje_de_pasto(self):
        for cta in ("servicio-pasto:hero", "servicio-pasto:cierre"):
            texto = unquote(re.search(rf'data-cta="{cta}" href="https://wa\.me/528333268008\?text=([^"]+)"', HTML)
                            .group(1))
            with self.subTest(cta=cta):
                self.assertTrue(texto.startswith(datos.MENSAJES["pasto-natural"]))
        self.assertIn('data-cta="servicio-pasto:medidor"', MAIN)
        self.assertIn('data-cta="servicio-pasto:simulador"', MAIN)

    def test_sin_css_viejo_ni_scripts_de_servicios(self):
        self.assertNotRegex(HTML, r"fonts\.googleapis|/css/(?:tailwind|design-system|servicios|legacy-fixes)")
        self.assertNotIn("svc-hero", HTML)
        self.assertNotIn("<form", HTML)
        orden = [HTML.index(f'src="/js/{s}"') for s in ("vt-mensualidades.js", "vt-medidor.js", "vt-simulador.js")]
        self.assertEqual(orden, sorted(orden))

    def test_json_ld_conservado_y_generado_de_lo_visible(self):
        self.assertEqual({n["@type"] for n in GRAFO},
                         {"Product", "FAQPage", "HowTo", "BreadcrumbList", "SpeakableSpecification"})
        visibles = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<summary>(.*?)</summary>", MAIN)]
        self.assertEqual([q["name"] for q in nodo("FAQPage")["mainEntity"]], visibles)
        self.assertEqual(len(visibles), 8)
        pasos = nodo("HowTo")["step"]
        self.assertEqual(len(pasos), 5)
        self.assertEqual(pasos[2]["text"], "Confirmas con un anticipo y coordinamos la entrega.")
        for paso in pasos:
            self.assertIn(f"<b>{paso['name']}.</b> {paso['text']}", MAIN)
        self.assertEqual(nodo("Product")["offers"]["price"], str(datos.PRECIOS["pasto_solo_m2"]))


if __name__ == "__main__":
    unittest.main()
```

En `tools/site/tests/test_generar.py`, reemplaza `self.assertEqual([r for r, *_ in generar.PAGINAS], ["/"])` por `self.assertEqual([r for r, *_ in generar.PAGINAS], ["/", "/pasto-en-rollo-tampico"])`.

En `tools/servicios/tests/test_pagos.py`, reemplaza el método `test_solo_tres_paginas_con_pago_nota` completo por:

```python
    def test_solo_dos_paginas_con_pago_nota(self):
        con = sorted(slug for slug, cfg in PAGES.items() if cfg.get("pago_nota"))
        self.assertEqual(con, ["diseno-jardines-tampico", "sistema-riego-tampico"])

    def test_paginas_con_plantilla_fuera_de_los_parches(self):
        self.assertNotIn("pasto-en-rollo-tampico", PAGES)
```

- [ ] **Step 2: Correrlas y ver que fallan**

```bash
cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_pasto_en_rollo.py tests/test_generar.py 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
```

Expected: `FAILED (failures=…)` (la página publicada es la vieja: no hay `vt-crumbs`, ni Medidor, ni `HowTo` generado); `FAILED (failures=2)`.

- [ ] **Step 3: `tools/servicios` deja de parchar pasto en rollo**

En `tools/servicios/pages.py`, borra la entrada `"pasto-en-rollo-tampico": dict(…),` completa (de `    "pasto-en-rollo-tampico": dict(` hasta el `),` que cierra antes de `    "mayoreo-pasto-tampico": dict(`) y, justo antes de `PAGES = {`, agrega:

```python
# /pasto-en-rollo-tampico y la home salen de tools/site/plantillas/ desde la Etapa 2a: este script ya no las toca.
```

En `tools/servicios/simulador.py`, borra la línea `    ("pasto-en-rollo-tampico", "pasto en rollo instalado", 12000),` y, justo antes de `PAGES = (`, agrega:

```python
# /pasto-en-rollo-tampico trae su simulador desde tools/site/plantillas/servicio.py (Etapa 2a).
```

- [ ] **Step 4: Contenido de pasto en rollo**

`tools/site/contenido/pasto_en_rollo.py`:

```python
"""Contenido de /pasto-en-rollo-tampico. Solo datos: la plantilla es tools/site/plantillas/servicio.py.

Copy de la maqueta aprobada (docs/diseno/hibrido/pasto-en-rollo.html) con los datos vivos de datos.py y el copy
corregido en la Etapa 1b (anticipo sin porcentaje, "Cortado para tu pedido", llegada semanal sin fecha de corte).
Título, descripción, canonical, Open Graph, Product, HowTo y migas del JSON-LD se conservan como estaban publicados;
FAQPage sale de las mismas preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import datos
from componentes import dinero, mensualidades

P = datos.PRECIOS
MINIMO = P["pasto_mayoreo_minimo_m2"]
OBRA = "/img/obra"
DESDE_MENSUALIDADES = dinero(mensualidades.minimo_de(3))
URL = f"{datos.SITIO}/pasto-en-rollo-tampico"

META = {
    "title": "Pasto en Rollo San Agustín · Tampico",
    "description": (f"Pasto San Agustín en rollo en Tampico desde ${P['pasto_solo_m2']}/m², instalado desde "
                    f"${P['pasto_instalado_m2']}/m² con garantía de arraigo. Entrega Tampico, Madero y Altamira. "
                    "Cotización en 1 hora."),
    "robots": "index, follow",
    "canonical": URL,
    "og": (
        ("og:type", "website"),
        ("og:url", URL),
        ("og:title", f"Pasto en Rollo San Agustín · Tampico desde ${P['pasto_solo_m2']}/m²"),
        ("og:description", (f"Pasto fresco cortado semanalmente. Desde ${P['pasto_solo_m2']}/m². Instalación con "
                            "garantía de arraigo. Esquema de pago flexible. Sin sorpresas.")),
        ("og:image", f"{datos.SITIO}/img/despues-instalacion-pasto-san-agustin-tampico.webp"),
        ("og:locale", "es_MX"),
    ),
}

PRODUCTO = {
    "@type": "Product",
    "name": "Pasto en Rollo San Agustín Tampico",
    "description": (f"Pasto San Agustín fresco cortado semanalmente para jardines en Tampico. Desde "
                    f"${P['pasto_solo_m2']}/m² solo el pasto e instalado desde ${P['pasto_instalado_m2']}/m², con "
                    "garantía de arraigo."),
    "brand": {"@type": "Brand", "name": datos.NOMBRE},
    "offers": {"@type": "Offer", "priceCurrency": "MXN", "price": str(P["pasto_solo_m2"]),
               "priceValidUntil": f"{datos.ANIO}-12-31", "availability": "https://schema.org/InStock",
               "seller": {"@type": "LocalBusiness", "name": datos.NOMBRE, "telephone": datos.TELEFONO_TEL}},
}

MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": datos.SITIO},
    {"@type": "ListItem", "position": 2, "name": "Pasto en Rollo Tampico", "item": URL},
]}

ZONAS = " · ".join(f'<a href="{href}">{nombre}</a>' for nombre, href in (
    ("Lomas de Rosales", "/jardineria-lomas-de-rosales-tampico"), ("Country Club", "/jardineria-country-club-tampico"),
    ("Águila y Altavista", "/jardineria-aguila-tampico"), ("Lomas del Chairel", "/jardineria-lomas-del-chairel-tampico"),
    ("Ciudad Madero", "/jardineria-ciudad-madero"), ("Altamira", "/jardineria-altamira")))

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto en rollo en Tampico?", datos.RESPUESTA_PRECIO_PASTO),
    ("¿Cuándo llega el pasto fresco al vivero?",
     f"El pasto llega {datos.LLEGADA_PASTO}, directo del campo. Nunca lo almacenamos más de una semana: se corta para "
     "tu pedido y va del campo a tu jardín en el menor tiempo posible, con las raíces activas para arraigar."),
    ("¿Cuánto tiempo tarda en arraigar el pasto San Agustín?",
     f"En el clima cálido y húmedo de Tampico arraiga en {datos.ARRAIGO} con riego abundante y diario. "
     f"{datos.PRIMER_RIEGO} Con instalación contratada, si una sección no arraiga en ese plazo, la reponemos sin costo, "
     'siguiendo el protocolo de riego (<a href="/politicas">ver condiciones</a>).'),
    ("¿Cómo se paga el pasto en rollo?",
     f"{datos.ANTICIPO} También puedes pagar en mensualidades con tarjeta de crédito en cotizaciones desde "
     f"{DESDE_MENSUALIDADES}."),
    ("¿Qué diferencia hay entre pasto de vivero y pasto de mercado?",
     "El pasto de vivero se corta fresco y va directo al jardín, con las raíces activas. El de mercado puede llevar días "
     f"en una bodega sin agua, perdiendo humedad. En el clima de Tampico se nota: el nuestro arraiga en {datos.ARRAIGO} "
     "y, si lo instalamos, tiene garantía; el de mercado puede tardar más o no arraigar."),
    ("¿Qué variedad de pasto es mejor para Tampico?",
     "El San Agustín (<i>Stenotaphrum secundatum</i>): resiste el calor intenso y la humedad del clima costero, y tolera "
     "sombra parcial mejor que otras variedades. Es el pasto más usado en jardines, áreas comerciales y parques "
     'industriales del sur de Tamaulipas. <a href="/blog/pasto-san-agustin-vs-japones">San Agustín o japonés: la '
     "comparativa</a>."),
    ("¿Hacen entrega fuera de Tampico?",
     "Sí. Entregamos en Tampico, Ciudad Madero y Altamira, y por proyecto en Pánuco, Ciudad Victoria, Tuxpan y la "
     "Huasteca. El costo de entrega depende de la distancia y el volumen; en proyectos grandes coordinamos la logística "
     "por etapas."),
    ("¿Tienen precio de mayoreo para constructoras?",
     f"Sí: desde ${P['pasto_mayoreo_m2']}/m² (solo pasto) en pedidos de {MINIMO} m² o más, con factura {datos.FACTURA}, "
     f"registro REPSE {datos.REPSE} y entregas por etapas según el avance de obra. "
     '<a href="/mayoreo-pasto-tampico">Ver mayoreo para obras</a>.'),
)

COMPRA = (
    ("Cotización inicial", "Envía por WhatsApp la dirección y los metros cuadrados aproximados."),
    ("Precio transparente", "Recibes el precio del pasto, entrega e instalación por separado."),
    ("Anticipo y coordinación", "Confirmas con un anticipo y coordinamos la entrega."),
    ("Instalación en un día", "El pasto va directo del campo a tu jardín. Instalación completa en un día."),
    ("Pago final y arraigo", ("Liquidas el saldo según lo acordado en tu cotización. Te explicamos cómo dar el primer "
                              "riego y te dejamos el protocolo de riego de 20 días.")),
)

CONTENIDO = {
    "tipo": "servicio-pasto",
    "prefijo": "pasto",
    "meta": META,
    "jsonld": {"producto": PRODUCTO, "migas": MIGAS_LD, "howto": "Cómo comprar e instalar pasto en rollo en Tampico",
               "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Pasto en rollo", None)),
    "portada": {
        "kicker": "Pasto natural · Tampico, Madero y Altamira",
        "h1": ('Pasto San Agustín en rollo, instalado en un día. '
               '<span class="vt-serif">Del campo a tu jardín, sin pasar por bodega.</span>'),
        "lede": (f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}. Preparamos el suelo, tendemos tepes "
                 "de 40 × 60 cm y te enseñamos a regarlo."),
        "etiqueta": {
            "codigo": "Pasto · 01", "aviso": "Tepe 40 × 60 cm", "nombre": "Pasto San Agustín",
            "cientifico": "Stenotaphrum secundatum", "antes": "Instalado · desde",
            "monto": dinero(P["pasto_instalado_m2"]), "unidad": "/m²",
            "filas": (("Solo pasto, tú lo instalas", f"{dinero(P['pasto_solo_m2'])} /m²"),
                      (f"Mayoreo, solo pasto, {MINIMO} m² o más", f"desde {dinero(P['pasto_mayoreo_m2'])} /m²")),
        },
        "mensaje": datos.MENSAJES["pasto-natural"],
        "tambien": (f'Garantía de arraigo de {datos.ARRAIGO} con instalación · <a href="#precio">calcula tu patio</a> · '
                    f'<a href="#mensualidades">mensualidades con tarjeta de crédito</a> desde {DESDE_MENSUALIDADES}'),
        "foto": {"src": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111, "numero": 1,
                 "alt": "Rollos de pasto San Agustín recién cortados, cargados en la camioneta de reparto.",
                 "lugar": "Rollos recién cortados · en la camioneta de reparto", "etapa": "Cd. Madero"},
    },
    "prueba": {
        "titulo": "Lo que entregamos, documentado.",
        "lede": ('<i class="vt-serif">Stenotaphrum secundatum</i> es la variedad que mejor aguanta el calor y la '
                 "humedad del Golfo. Así se ve en cada etapa."),
        "figuras": (
            {"src": f"{OBRA}/jardin-residencial-pasto-san-agustin.webp", "ancho": 1280, "alto": 720, "numero": 2,
             "alt": "Jardín residencial con pasto San Agustín ya instalado.",
             "lugar": "Zona Tampico–Madero · jardín residencial", "etapa": "Terminado"},
            {"src": f"{OBRA}/cuadrilla-tendiendo-pasto-san-agustin-640.webp", "ancho": 640, "alto": 960, "numero": 3,
             "alt": "Integrante de la cuadrilla tendiendo tepes de pasto San Agustín.", "lugar": "Tendido de tepes",
             "etapa": "Día de instalación"},
            {"src": f"{OBRA}/pasto-san-agustin-recien-instalado.webp", "ancho": 640, "alto": 960, "numero": 4,
             "alt": "Pasto recién instalado con el borde recortado contra el andador.", "lugar": "Después",
             "etapa": "Borde recortado"},
            {"src": f"{OBRA}/riego-aspersor-borde-pasto.webp", "ancho": 700, "alto": 875, "numero": 5,
             "alt": "Aspersor regando el borde de un jardín con pasto San Agustín.", "lugar": "Riego de arraigo",
             "etapa": "Aspersión en el borde"},
        ),
        "nota": ("En sombra profunda el San Agustín no prende. Ahí va otra solución, y te lo decimos antes de cobrarte.",
                 "Al medir, en tu jardín"),
    },
    "precio": {
        "titulo": "¿Cuánto cuesta el pasto San Agustín en Tampico?",
        "lede": (f"Desde {dinero(P['pasto_instalado_m2'])}/m² instalado en Tampico, Madero y Altamira, con preparación "
                 f"básica del suelo y garantía de arraigo de {datos.ARRAIGO}; {dinero(P['pasto_solo_m2'])}/m² solo el "
                 f"pasto, y desde {dinero(P['pasto_mayoreo_m2'])}/m² en mayoreo de {MINIMO} m² o más con factura "
                 f"{datos.FACTURA}. Precios {datos.ANIO} con IVA."),
        "filas": (
            {"nombre": "Pasto con instalación", "unidad": "/m²", "precio": P["pasto_instalado_m2"], "desde": True,
             "rec": True, "detalle": (f"Preparación básica del suelo, tendido en un día, garantía de arraigo de "
                                      f"{datos.ARRAIGO} y protocolo de riego.")},
            {"nombre": "Solo el pasto", "unidad": "/m²", "precio": P["pasto_solo_m2"],
             "detalle": ("Tú lo instalas. Recoges en el vivero de Obregón 209 Sur o te lo llevamos (la entrega se "
                         "cotiza según tu colonia).")},
            {"nombre": "Mayoreo, solo pasto", "unidad": "/m²", "precio": P["pasto_mayoreo_m2"], "desde": True,
             "detalle": (f"Desde {MINIMO} m². Entregas por etapas según avance de obra, factura {datos.FACTURA} y REPSE "
                         f'{datos.REPSE}. <a href="/mayoreo-pasto-tampico">Ver mayoreo para obras</a>.')},
        ),
        "caption": (f"Precios {datos.ANIO} con IVA incluido. Donde dice “desde”, al medir te damos el precio cerrado. "
                    'Lista completa en <a href="/precios">viverosterra.com/precios</a>.'),
        "titulo_medidor": "Calcula el tuyo",
    },
    "objecion": {
        "titulo": "¿Cuál te conviene según tu espacio?",
        "lede": ("Vendemos e instalamos los dos en Tampico. Esta tabla te ayuda a elegir según tu espacio, tu presupuesto "
                 "y el tiempo que quieras dedicarle."),
        "comparativa": {
            "columnas": ("Característica", "Pasto San Agustín (natural)", "Pasto sintético"),
            "filas": (
                ("Precio instalado", f"desde {dinero(P['pasto_instalado_m2'])}/m²",
                 f"desde {dinero(P['sintetico_instalado_m2'][0])}/m²"),
                ("Vida útil", "15+ años con cuidado", "8-10 años"),
                ("Mantenimiento", "Riego + poda quincenal", "Cepillado mensual"),
                ("Riego", "Diario al instalar; después, según el clima", "Sin riego; solo un enjuague ocasional"),
                ("Ideal para", "Jardines residenciales con sombra parcial",
                 "Terrazas, azoteas, áreas sin riego y zonas para mascotas"),
            ),
            "caption": "Pasto natural o sintético, según tu espacio.",
            "cierre": ("Si tu jardín tiene tierra y puedes regarlo, el San Agustín cuesta menos por metro y dura más. Si "
                       "es una terraza, una azotea o un área sin riego, te conviene el sintético: también lo vendemos e "
                       'instalamos en Tampico (<a href="/pasto-sintetico-tampico">ver pasto sintético</a>).'),
        },
        "titulo_2": "Pasto de vivero vs pasto de mercado",
        "comparativa_2": {
            "columnas": ("Característica", "Viveros Terra", "Pasto de mercado"),
            "filas": (
                ("Frescura", "Se corta para tu pedido y va directo a tu jardín", "Puede llevar días en bodega sin agua"),
                ("Arraigo en Tampico", f"{datos.ARRAIGO}, con garantía si lo instalamos", "Variable, sin garantía"),
                ("Forma de pago", "Anticipo para confirmar; contado o mensualidades con tarjeta de crédito",
                 "Normalmente todo por adelantado"),
                ("Después de instalar", "Protocolo de riego de 20 días por escrito", "Sin seguimiento"),
                ("Factura", datos.FACTURA, "Rara vez"),
            ),
            "caption": "Lo que cambia entre el pasto de vivero y el de mercado.",
        },
    },
    "proceso": {
        "titulo": "Cómo se instala el pasto en rollo: cinco pasos, dos son tuyos.",
        "lede": ("Lo que hace que el pasto arraigue es el agua de las primeras semanas. Por eso te lo explicamos ahí "
                 "mismo, en tu jardín."),
        "pasos": (
            {"titulo": "Preparación del suelo", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": ("Nivelamos, retiramos piedras grandes y agregamos 3 a 5 cm de tierra negra si hace falta. Nunca "
                       "te cobramos preparación sin avisarte antes.")},
            {"titulo": "Tendido de los tepes", "quien": "nosotros", "cuando": "Día de instalación",
             "texto": ("Tepes de 40 × 60 cm en patrón de ladrillo, uniones desfasadas y sin huecos, presionados para que "
                       "la raíz toque el suelo.")},
            {"titulo": "Primer riego", "quien": "tu", "cuando": "Primeras 2 horas",
             "texto": ("El primer riego lo haces tú: riega hasta que el agua atraviese el tepe. Te enseñamos cuánta agua "
                       "darle antes de irnos.")},
            {"titulo": "Riego diario", "quien": "tu", "cuando": "Días 1 a 20",
             "texto": ("Abundante, de preferencia mañana y tarde, siguiendo el "
                       '<a href="/protocolo-cuidados-pasto-san-agustin">protocolo de 20 días</a> que te dejamos por '
                       "escrito. Después, una vez al día por un mes y luego 3 veces por semana.")},
            {"titulo": "Primera poda", "quien": "juntos", "cuando": "Día 21",
             "texto": ("A 4 o 5 cm de altura, cuando ya arraigó. Te decimos cuándo; si tienes "
                       '<a href="/mantenimiento-jardines-tampico">mantenimiento</a> con nosotros, la hacemos.')},
        ),
    },
    "garantia": {
        "titulo": f"Garantía de arraigo de {datos.ARRAIGO}: si no arraiga, lo reponemos.",
        "grande": "15–20", "unidad": "días",
        "resumen": "Garantía de arraigo con instalación contratada.",
        "puntos": (
            ("Si contratas la instalación y sigues el protocolo de riego de 20 días, garantizamos el arraigo: si una "
             f"sección no arraiga en {datos.ARRAIGO}, la reponemos sin costo.", True),
            (f"Cortado para tu pedido: llega del campo {datos.LLEGADA_PASTO}; no son rollos viejos de bodega.", True),
            ("Protocolo por escrito: qué hacer cada día y qué señales revisar.", True),
            (f"Factura {datos.FACTURA} para persona física o moral.", True),
            ("Si el área tiene sombra profunda, te lo decimos al medir: ahí el San Agustín no es la opción y no lo "
             "instalamos con garantía.", False),
        ),
        "pie": ('<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a> · '
                '<a href="/protocolo-cuidados-pasto-san-agustin">Protocolo de cuidados de 20 días</a>'),
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} El resto se liquida según lo acordado en tu cotización, de contado o en "
                 f"mensualidades con tarjeta de crédito desde {DESDE_MENSUALIDADES}."),
        "titulo_compra": "De la cotización a tu jardín verde en 5 pasos",
        "compra": COMPRA,
        "titulo_sim": "Calcula tus mensualidades con tarjeta",
        "sim": {"servicio": "pasto en rollo instalado", "monto": 12000},
    },
    "faq": {"titulo": "Todo sobre el pasto en rollo en Tampico", "preguntas": PREGUNTAS},
    "cierre": {
        "titulo": "Tu jardín verde, instalado en un día.",
        "lede": ("Dinos si lo quieres solo pasto o instalado, tu colonia y tus metros, y mándanos una foto. Si hace falta, "
                 "vamos a medir sin costo."),
        "mensaje": datos.MENSAJES["pasto-natural"],
    },
    "relacionados": {
        "titulo": "Complementa tu jardín",
        "items": (
            {"titulo": "Tierra negra vegetal", "href": "/tierra-negra-vegetal-tampico",
             "texto": (f"La base ideal antes de instalar pasto. Costal {dinero(P['tierra_negra_costal'])} · m³ "
                       f"{dinero(P['tierra_negra_m3'])}.")},
            {"titulo": "Sistema de riego automático", "href": "/sistema-riego-tampico",
             "texto": "Para que tu pasto siempre esté verde sin esfuerzo. Ahorra hasta 40% de agua."},
            {"titulo": "Mantenimiento mensual", "href": "/mantenimiento-jardines-tampico",
             "texto": (f"¿Ya tienes tu pasto? Que nunca se vea descuidado. Desde {dinero(P['mantenimiento_mes'])}/mes.")},
        ),
        "zonas": (f"Instalamos en {ZONAS}. También en Pánuco, Ciudad Victoria, Tuxpan y la Huasteca, por proyecto."),
    },
}

OBJECIONES = "Las objeciones de la página anterior quedan en las preguntas, el Medidor, el pago y la garantía."
PARIDAD = {
    "reemplazos": {
        "Pasto San Agustín en rollo, instalado en un día": (
            "Pasto San Agustín en rollo, instalado en un día. Del campo a tu jardín, sin pasar por bodega."),
        "¿Cuánto cuesta ponerle pasto a mi jardín?": "Calcula el tuyo",
        "Tres formas de tener tu jardín verde": "¿Cuánto cuesta el pasto San Agustín en Tampico?",
        "Cómo instalar pasto en rollo San Agustín en 5 pasos": (
            "Cómo se instala el pasto en rollo: cinco pasos, dos son tuyos."),
        "Colocación de los tepes": "Tendido de los tepes",
        "Primer riego (lo haces tú)": "Primer riego",
        "Riego abundante y diario los primeros 15 a 20 días": "Riego diario",
        "Primera poda a los 21 días": "Primera poda",
        "Jardines con pasto San Agustín en Tampico": "Lo que entregamos, documentado.",
        "Protocolo de Cuidados Garantía de arraigo en 15 a 20 días": (
            "Garantía de arraigo de 15 a 20 días: si no arraiga, lo reponemos."),
        "¿Puedo pagar en partes?": "¿Cómo se paga el pasto en rollo?",
        "¿Cuánto tiempo tarda en arraigar?": "¿Cuánto tiempo tarda en arraigar el pasto San Agustín?",
    },
    "retirados": {
        "Pasto natural premium cultivado para el clima del Golfo": (
            "Su contenido queda en la respuesta “¿Qué variedad de pasto es mejor para Tampico?” y en la entrada de la "
            "prueba; sus cifras, en el cuadro de datos."),
        "Solo Pasto": "Es la fila “Solo el pasto” de la tabla de precios.",
        "Pasto + Instalación": "Es la fila “Pasto con instalación” de la tabla de precios.",
        "Mayoreo / Proyectos": "Es la fila “Mayoreo, solo pasto” de la tabla, con enlace a /mayoreo-pasto-tampico.",
        "\"¿Cuánto me va a costar exactamente?\"": OBJECIONES,
        "\"¿Tengo que pagar todo antes?\"": OBJECIONES,
        "\"¿Mi terreno está muy mal para pasto?\"": OBJECIONES,
        "\"¿El pasto llegará fresco?\"": OBJECIONES,
        "\"¿Y si el pasto no arraiga?\"": OBJECIONES,
        "+500,000 m² instalados en Tamaulipas y zona Huasteca": "La cifra va en el cuadro de datos (Instalado).",
        "Lo que dicen quienes ya tienen su jardín": (
            "Testimonios con nombre sin verificar (uno decía “pagué el resto hasta que lo vi terminado”): la regla del "
            "dueño prohíbe testimonios inventados y el pago al ver el jardín terminado."),
        "Su vivero de confianza en Tamaulipas": (
            "El bloque B2B pasa a /mayoreo-pasto-tampico (enlazado en la tabla de precios y en la pregunta de mayoreo); "
            "decía “Más de 18 años”."),
        "Viveros Terra · Tampico": (
            "Caja de autor de la página de servicio; la entidad va a /nosotros (Etapa 3). “Certificación SENASICA” y "
            "“+200 proyectos B2B” no están en datos.py."),
        "Escríbenos para cotizar": (
            "Formulario de pedido por correo retirado: la plantilla de servicio tiene un solo canal, WhatsApp o "
            "teléfono con la promesa única (spec §3.3, §4.3). Pendiente de confirmar con el dueño."),
    },
}
```

- [ ] **Step 5: Plantilla de servicio local**

`tools/site/plantillas/servicio.py`:

```python
"""Plantilla de servicio local (spec §3.3): ruta visible → H1 con beneficio y lugar → precio ancla en la etiqueta → CTA
con plantilla y promesa → prueba (cuadro de datos, fotos FIG. y nota de campo) → precio con Medidor → objeción
principal → proceso NOSOTROS / TÚ → garantía con condiciones → pago (anticipo y mensualidades con tarjeta de crédito)
→ preguntas → CTA final → relacionados y zonas. Las secciones que el contenido no trae se omiten (diseño, mantenimiento
y riego no llevan Medidor de pasto). Primera página: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py)."""
import componentes as c
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor y el simulador); el Medidor solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return ("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ()) + ("/js/vt-simulador.js",)


def _precio(k, numero):
    p = k["precio"]
    cuerpo = c.tabla_precios(p["filas"], p["caption"], concepto="Forma de compra")
    if p.get("titulo_medidor"):
        cuerpo += f'<h3 class="vt-mt">{p["titulo_medidor"]}</h3>' + c.medidor(k["prefijo"], k["tipo"])
    return c.bloque(numero, "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p["lede"], tinte=True, id_seccion="precio")


def _objecion(k, numero):
    o = k["objecion"]
    a, b = o["comparativa"], o["comparativa_2"]
    cuerpo = (c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
              + f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"]))
    return c.bloque(numero, "Cuál te conviene", "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])


def _pago(k, numero):
    p = k["pago"]
    derecha = (f'<h3>{p["titulo_compra"]}</h3>' + c.pasos_compra(p["compra"]) + c.planes_mensualidades()
               + f'<h3 class="vt-mt">{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"]))
    return c.bloque_dos(numero, "Pago", "vt-h-pago", p["titulo"], f'<p class="vt-lede">{p["lede"]}</p>', derecha,
                        id_seccion="mensualidades")


def _relacionados(k, numero):
    r = k["relacionados"]
    return c.bloque(numero, "Relacionados", "vt-h-rel", r["titulo"],
                    c.relacionados(r["items"]) + f'<p class="vt-promesa">{r["zonas"]}</p>')


def render(k):
    tipo = k["tipo"]
    pr, g, f, ci = k["prueba"], k["garantia"], k["faq"], k["cierre"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]),
                 c.bloque(1, "Prueba", "vt-h-prueba", pr["titulo"], c.obras(pr["figuras"], c.nota(*pr["nota"])),
                          lede=pr["lede"])]
    numero = 2
    for clave, armar in (("precio", _precio), ("objecion", _objecion)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    p = k["proceso"]
    secciones.append(c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]))
    secciones.append(c.garantia(dict(g, numero=numero + 1, id_titulo="vt-h-garantia", rotulo="Garantía")))
    secciones.append(_pago(k, numero + 2))
    secciones.append(c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))
    secciones.append(_relacionados(k, numero + 4))

    j = k["jsonld"]
    grafo = [j["producto"], c.faq_jsonld(f["preguntas"]), c.howto(j["howto"], k["pago"]["compra"]), j["migas"],
             {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    return base.documento(k["meta"], "\n".join(secciones), jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k))
```

- [ ] **Step 6: Registrar la página**

En `tools/site/generar.py`, reemplaza:

```python
PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
)
```

por:

```python
PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
    ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
)
```

- [ ] **Step 7: Build dos veces, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/build.py | tail -2
python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /pasto-en-rollo-tampico
cd tools/site && python3 -m unittest tests/test_pasto_en_rollo.py tests/test_generar.py tests/test_consistencia.py tests/test_reglas.py tests/test_enlaces.py tests/test_sitio.py 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
```

Expected: `plantillas: 1 de 2 páginas escritas` y `shell: 0 de 108 …`; luego `plantillas: 0 de 2 …` y `shell: 0 de 108 …`; el informe dice `ok` en las seis categorías; `OK`; `OK`. `test_consistencia` sigue encontrando el `"text":"No pedimos el 100% por adelantado…"` del FAQ, el `"Confirmas con un anticipo y coordinamos la entrega."` del HowTo, "¿Cuál te conviene según tu espacio?" y exactamente dos "Cortado para tu pedido".

- [ ] **Step 8: Commit**

```bash
cd ~/dev/viverosterra-e2a
git status --short
git add tools/site/plantillas/servicio.py tools/site/contenido/pasto_en_rollo.py tools/site/generar.py tools/site/tests/test_pasto_en_rollo.py tools/site/tests/test_generar.py tools/servicios/pages.py tools/servicios/simulador.py tools/servicios/tests/test_pagos.py public/pasto-en-rollo-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(pasto-en-rollo): plantilla de servicio local con precio, Medidor, proceso, garantía y pago" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Paridad y contenido como pruebas permanentes

**Files:**
- Create: `tools/site/tests/test_contenido.py`
- Modify: `tools/site/tests/test_paridad.py`

- [ ] **Step 1: Escribir las pruebas**

`tools/site/tests/test_contenido.py`:

```python
"""El contenido de las páginas con plantilla es solo HTML en línea permitido y no rompe las reglas del dueño."""
import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402


def cadenas(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from cadenas(v)
    elif isinstance(valor, (list, tuple)):
        for v in valor:
            yield from cadenas(v)


class ContenidoTest(unittest.TestCase):
    def modulos(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            yield ruta, importlib.import_module(f"contenido.{contenido}")

    def test_solo_marcado_en_linea_permitido(self):
        for ruta, modulo in self.modulos():
            for texto in cadenas({k: v for k, v in modulo.CONTENIDO.items() if k not in ("meta", "jsonld")}):
                with self.subTest(ruta=ruta, texto=texto[:60]):
                    self.assertEqual(componentes.etiquetas_no_permitidas(texto), [])

    def test_tipo_del_contenido_igual_al_de_paginas(self):
        for ruta, modulo in self.modulos():
            if "tipo" in modulo.CONTENIDO:
                with self.subTest(ruta=ruta):
                    self.assertEqual(modulo.CONTENIDO["tipo"], paginas.contexto(ruta)["tipo"])

    def test_paridad_con_motivos_escritos(self):
        for ruta, modulo in self.modulos():
            for viejo, motivo in modulo.PARIDAD["retirados"].items():
                with self.subTest(ruta=ruta, retirado=viejo):
                    self.assertGreater(len(motivo), 20)


if __name__ == "__main__":
    unittest.main()
```

`tools/site/tests/test_paridad.py` (versión completa: agrega la comparación de cada página migrada y la detección de entradas viejas en el mapa):

```python
"""Paridad de contenido de las páginas migradas contra su captura anterior (tools/site/tests/paridad/*.json)."""
import importlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generar  # noqa: E402
import paridad  # noqa: E402


class ParidadTest(unittest.TestCase):
    def test_nada_se_pierde_sin_motivo(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            mapa = importlib.import_module(f"contenido.{contenido}").PARIDAD
            for categoria, faltantes in paridad.comparar(ruta, mapa).items():
                with self.subTest(ruta=ruta, categoria=categoria):
                    self.assertEqual(faltantes, [])

    def test_el_mapa_no_tiene_entradas_viejas(self):
        for ruta, _salida, _plantilla, contenido in generar.PAGINAS:
            mapa = importlib.import_module(f"contenido.{contenido}").PARIDAD
            captura = json.loads((paridad.CAPTURAS / f"{paridad.nombre_captura(ruta)}.json").read_text(encoding="utf-8"))
            conocidos = {item for c in paridad.CATEGORIAS for item in captura[c]}
            for viejo in list(mapa["reemplazos"]) + list(mapa["retirados"]):
                with self.subTest(ruta=ruta, entrada=viejo):
                    self.assertIn(viejo, conocidos)

    def test_cubierto_y_faltantes(self):
        self.assertTrue(paridad.cubierto("Primer riego", ["Primer riego Tú"]))
        self.assertTrue(paridad.cubierto("Pasto Sintético", ["pasto sintético."]))
        self.assertFalse(paridad.cubierto("Riego", ["Riegos"]))
        mapa = {"reemplazos": {"A": "B"}, "retirados": {"C": "motivo largo y claro"}}
        self.assertEqual(paridad.faltantes(["A", "C", "D"], ["B"], mapa), ["D"])
        self.assertEqual(paridad.faltantes(["A"], [], mapa), ["A → B (el reemplazo no está en la página)"])

    def test_extraer(self):
        html = ('<title>T</title><meta name="description" content="D"><main><h2>¿Cuánto?</h2><p>$1,500 y $ 85</p>'
                '<details><summary>¿Pregunta?</summary></details><a href="/x/#a">x</a><a href="//cdn">y</a></main>')
        e = paridad.extraer(html)
        self.assertEqual((e["meta"]["title"], e["meta"]["description"]), ("T", "D"))
        self.assertEqual(e["encabezados"], ["¿Cuánto?"])
        self.assertEqual(e["faq"], ["¿Pregunta?"])
        self.assertEqual(e["precios"], ["$1,500", "$85"])
        self.assertEqual(e["enlaces"], ["/x"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Comprobar que las pruebas detectan lo que deben**

```bash
cd ~/dev/viverosterra-e2a/tools/site
python3 -m unittest tests/test_contenido.py tests/test_paridad.py 2>&1 | tail -1
cp contenido/inicio.py /tmp/vt-inicio.py.bak
python3 -c "from pathlib import Path; p = Path('contenido/inicio.py'); p.write_text(p.read_text(encoding='utf-8').replace('        \"Nos escribes\": \"Nos mandas medidas y foto\",\n', ''), encoding='utf-8')"
python3 -m unittest tests/test_paridad.py 2>&1 | grep -E "Nos escribes|FAILED"
cp /tmp/vt-inicio.py.bak contenido/inicio.py
python3 -m unittest tests/test_paridad.py 2>&1 | tail -1
```

Expected: `OK`; con la entrada borrada, la falla muestra `'Nos escribes'` y `FAILED (failures=1)`; al restaurar, `OK`.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2a
git status --short
git add tools/site/tests/test_contenido.py tools/site/tests/test_paridad.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): nada del contenido anterior se pierde sin motivo escrito" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Pruebas en navegador de las páginas con plantilla

**Files:**
- Create: `tools/site/tests/test_plantillas_navegador.py`

- [ ] **Step 1: Escribir la prueba**

`tools/site/tests/test_plantillas_navegador.py`:

```python
"""Páginas con plantilla en Chromium: axe de página completa, primer pantallazo móvil, Medidor, sin desbordar y CLS.
Se saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
PAGINAS = ("/", "/pasto-en-rollo-tampico/")
AXE_PAGINA = """async () => {
  const r = await axe.run(document, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
CLS = """() => new Promise((listo) => {
  let total = 0;
  new PerformanceObserver((lista) => { lista.getEntries().forEach((e) => { if (!e.hadRecentInput) total += e.value; }); })
    .observe({ type: 'layout-shift', buffered: true });
  setTimeout(() => listo(total), 1500);
})"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class PlantillasNavegadorTest(unittest.TestCase):
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

    def pagina(self, ancho=1440, alto=900):
        contexto = self.navegador.new_context(viewport={"width": ancho, "height": alto})
        self.addCleanup(contexto.close)
        base = self.base
        contexto.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        return contexto.new_page()

    def test_axe_de_pagina_completa_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_precio_y_cta_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        for ruta in PAGINAS:
            page.goto(self.base + ruta, wait_until="load")
            precio = page.locator(".vt-portada .vt-etiqueta__precio").bounding_box()
            cta = page.locator('.vt-portada [data-hero-cta] .vt-btn--wa').bounding_box()
            with self.subTest(ruta=ruta):
                self.assertLessEqual(precio["y"] + precio["height"], 812)
                self.assertLessEqual(cta["y"] + cta["height"], 812)

    def test_sin_desbordar_en_cuatro_anchos(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(sobra, 1)

    def test_estado_inicial_del_medidor_igual_al_html(self):
        for ruta in PAGINAS:
            page = self.pagina()
            page.add_init_script("window.__antes = null; document.addEventListener('readystatechange', () => {"
                                 " if (document.readyState === 'interactive' && !window.__antes) window.__antes ="
                                 " document.querySelector('[data-vt-medidor] .vt-medidor__res').innerText; });")
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertEqual(page.evaluate("() => window.__antes"),
                                 page.locator("[data-vt-medidor] .vt-medidor__res").inner_text())

    def test_medidor_calcula_avisa_y_arma_el_mensaje(self):
        page = self.pagina()
        page.goto(self.base + "/", wait_until="load")
        caja = page.locator("[data-vt-medidor]")
        caja.locator('[data-vt-campo="largo"]').fill("10")
        caja.locator('[data-vt-campo="ancho"]').fill("10")
        caja.locator('input[value="mayoreo"]').check(force=True)
        caja.locator('[data-vt-campo="colonia"]').fill("Lomas de Rosales")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "$8,500")
        self.assertTrue(caja.locator('[data-vt-o="aviso"]').is_visible())
        self.assertIn("Te faltan 400 m²", caja.locator('[data-vt-o="aviso"]').inner_text())
        mensaje = unquote(caja.locator('[data-vt-o="cta"]').get_attribute("href").split("text=", 1)[1])
        self.assertIn("Medidas: 10.00 × 10.00 m = 100 m²", mensaje)
        self.assertIn("Colonia: Lomas de Rosales", mensaje)
        caja.locator('[data-vt-campo="ancho"]').fill("")
        self.assertEqual(caja.locator('[data-vt-o="monto"]').inner_text(), "—")

    def test_clic_en_el_medidor_manda_generate_lead(self):
        page = self.pagina()
        page.add_init_script("window.open = () => null;")
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        page.evaluate("() => document.querySelector('[data-vt-o=\"cta\"]').addEventListener('click', (e) => e.preventDefault())")
        page.click('[data-vt-o="cta"]')
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "servicio-pasto:medidor",
                                                  "service": "pasto-natural"}], eventos)

    def test_simulador_de_pasto_en_rollo_funciona(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        self.assertEqual(page.locator("[data-sim-list] .sim-plan").count(), 5)
        self.assertIn("text=", page.get_attribute("[data-sim-wa]", "href"))

    def test_cls_bajo_0_1_en_movil(self):
        page = self.pagina(375, 812)
        for ruta in PAGINAS:
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertLess(page.evaluate(CLS), 0.1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrla**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_plantillas_navegador.py -v 2>&1 | tail -3`
Expected: `Ran 8 tests` y `OK` (sin `skipped`). Si `test_cls_bajo_0_1_en_movil` falla por el cambio de fuente, cambia en el `@font-face` de Archivo de `terra.css` `font-display:swap` por `font-display:optional`, corre el build y repite (la fuente ya va precargada; con `optional` no hay reacomodo).

- [ ] **Step 3: Las pruebas de navegador existentes siguen en verde**

Run: `cd ~/dev/viverosterra-e2a/tools/site && python3 -m unittest tests/test_navegador.py tests/test_tienda_navegador.py 2>&1 | tail -1`
Expected: `OK` (consola limpia en las 108 páginas, axe del shell, una sola barra fija abajo, eventos GA4; los `BrokenPipeError` que imprime el servidor local al cortar descargas no son fallas).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/tests/test_plantillas_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(navegador): axe de página completa, primer pantallazo, Medidor y CLS en las plantillas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Capturas también a 768

**Files:**
- Modify: `tools/site/capturas.py`

- [ ] **Step 1: Cambiar los anchos**

En `tools/site/capturas.py`, reemplaza `"""Capturas de verificación de la Etapa 1: 10 páginas a 320, 375 y 1440 px` por `"""Capturas de verificación: 10 páginas a 320, 375, 768 y 1440 px` y `ANCHOS = (320, 375, 1440)` por `ANCHOS = (320, 375, 768, 1440)`.

- [ ] **Step 2: Correr**

Run: `cd ~/dev/viverosterra-e2a && python3 tools/site/capturas.py /tmp/vt-e2a-capturas | head -2`
Expected: `40 capturas en /tmp/vt-e2a-capturas` y `sin desbordamiento horizontal` (si reaparece el conocido de `/pasto-sintetico/` a 320, se anota: lo corrige 2b).

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2a
git add tools/site/capturas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore(capturas): agrega el ancho de 768 px" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: Verificación final, puertas de revisión, merge y producción

**Files:** ninguno nuevo (correcciones que pidan los revisores, cada una con su prueba).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `plantillas: 0 de 2 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 237 tests` y `OK`; `OK` (59); `Ran 11 tests` y `OK`; `ℹ pass 34` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas y consistencia a la vista**

```bash
cd ~/dev/viverosterra-e2a
python3 tools/site/paridad.py informe / ; python3 tools/site/paridad.py informe /pasto-en-rollo-tampico
cd tools/site && python3 -m unittest tests/test_reglas.py tests/test_consistencia.py tests/test_paridad.py tests/test_contenido.py -v 2>&1 | tail -3
cd ../.. && grep -rnoiE "oasis|pasto ?plus|\bMSI\b|sin intereses|p[aá]del|lote semanal|cortado esta semana|pagas cuando" public/index.html public/pasto-en-rollo-tampico/index.html public/js/vt-medidor.js | wc -l
```

Expected: `ok` en las seis categorías de cada página; `OK`; `0`.

- [ ] **Step 3: Lighthouse móvil en la home y en pasto en rollo**

```bash
cd ~/dev/viverosterra-e2a
(cd public && python3 -m http.server 8765 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in "" "pasto-en-rollo-tampico/"; do
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8765/$r" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2a-lh-${r%/}.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2a-lh-${r%/}.json"
done
pkill -f "http.server 8765"
```

Expected (por página): Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1 y LCP < 2.5 s. Si Performance queda abajo por GA4 o por la imagen de la portada, anota el valor y la causa principal (`a['largest-contentful-paint-element']`) en el PR; GA4 diferido es de la Etapa 5 y no se adelanta aquí. CLS ≥ 0.1 sí bloquea: aplica el cambio de `font-display` de la Tarea 11, Step 2.

- [ ] **Step 4: Capturas finales a 320, 375, 768 y 1440**

Run: `cd ~/dev/viverosterra-e2a && python3 tools/site/capturas.py /tmp/vt-e2a-capturas | head -3`
Expected: `40 capturas …`. Revisa a mano `inicio-*.png` y `pasto-en-rollo-tampico-*.png`: una sola etiqueta amarilla en el primer pantallazo móvil, precio derecho (sin rotación), pies `FIG.` en cada foto, marcadores NOSOTROS / TÚ / JUNTOS, tabla de precios legible a 320 (en celular la unidad y el precio van bajo el concepto), la barra móvil oculta mientras se ve el CTA de la portada.

- [ ] **Step 5: Abrir el PR**

```bash
cd ~/dev/viverosterra-e2a
git push -u origin feat/etapa-2a
gh pr create --base main --head feat/etapa-2a --title "Etapa 2a · Plantillas: componentes, inicio y pasto en rollo" --body "$(cat <<'EOF'
## Qué cambia
- `tools/site/componentes.py`, `plantillas/` y `contenido/`: el cuerpo de la home y de `/pasto-en-rollo-tampico` sale de plantillas con su contenido en datos; los números salen de `datos.py`.
- `terra.css` trae los componentes del híbrido (etiqueta, Medidor, cuadro de datos, FIG., NOSOTROS/TÚ, nota de campo, precios con Unidad, mensualidades, FAQ, cierre). Las dos páginas ya no cargan Tailwind, design-system, servicios ni Google Fonts.
- `vt-medidor.js`: largo × ancho → m² → precio → WhatsApp con la medida; mensualidades con `vt-mensualidades.js`; mayoreo bajo 500 m² calcula a $85 y avisa.
- Título, descripción, canonical, Open Graph y tipos de JSON-LD intactos; FAQPage y HowTo salen de lo visible.
- Paridad de contenido: cada encabezado, pregunta, precio y enlace anterior sigue o tiene su motivo en `PARIDAD`.

## Verificación
- [ ] Build reproducible y 4 suites en verde (237 + 59 + 11 + 34)
- [ ] Lighthouse móvil (anotar Perf, A11y, CLS, LCP de las dos páginas)
- [ ] Capturas a 320/375/768/1440 (comentario con imágenes)
- [ ] Puertas: diseño, SEO/AEO, CRO, cumplimiento/QA
- [ ] Vista previa de Vercel aprobada por el dueño

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
gh pr view --json url --jq .url
```

Expected: la URL del PR; Vercel comenta la vista previa.

- [ ] **Step 6: Puertas de revisión en paralelo (spec §11)**

Lanza los cuatro revisores a la vez (una respuesta con cuatro llamadas). A cada uno: `git diff main...feat/etapa-2a --stat`, los archivos de `tools/site/componentes.py`, `plantillas/`, `contenido/`, `public/js/vt-medidor.js`, el bloque nuevo de `terra.css`, la URL de la vista previa, `/tmp/vt-e2a-capturas`, los JSON de Lighthouse, la salida de `paridad.py informe`, la maqueta `docs/diseno/hibrido/` y el spec (§3.3, §4, §5.3, §6, §7.3, §8.3, §10 Etapa 2, §11). Cada hallazgo se clasifica crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (etiqueta derecha y una por pantalla móvil, cuadro de datos, pies `FIG.`, Archivo + Fraunces itálica solo en nombres científicos y notas), jerarquía y ritmo, foco ≥ 3:1, objetivos táctiles ≥ 44 px en CTA, Medidor operable con teclado (radios con foco visible en la etiqueta), contraste, capturas 320–1440, que las páginas viejas no cambiaron (compara 3 capturas viejas antes/después).
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): `git diff main...feat/etapa-2a -- public/index.html public/pasto-en-rollo-tampico/index.html | grep -E '^[-+].*(<title>|name="description"|rel="canonical"|property="og:)'` debe salir vacío; JSON-LD válido (Rich Results Test sobre la vista previa); un H1; la respuesta directa de precio idéntica en home y pasto en rollo; enlaces internos conservados (paridad) y enlace de mayoreo a `/mayoreo-pasto-tampico`; imágenes con `width`/`height` y alt; LCP precargado.
3. **CRO** (`general-purpose` con `page-cro`): primer pantallazo móvil (qué, dónde, $85/$120 y CTA), CTA del hero al Medidor, mensaje de WhatsApp de cada CTA (hero, Medidor, simulador, cierre) con contexto y firma, `data-cta` y `generate_lead` del Medidor, objeciones (pago con anticipo, garantía condicionada, riego a cargo del cliente en positivo, sombra profunda), que retirar los formularios de correo no deja al visitante sin camino.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): reglas del dueño, datos oficiales solo desde `datos.py`, paridad Python ↔ JS del Medidor, calidad de `tools/site/`, consola limpia, que `tools/servicios` ya no toca pasto en rollo, que no se versionó `.DS_Store`.

Corrige en la rama todo crítico o alto (prueba, commit, nueva corrida del Step 1) y vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan en el PR con su motivo.

- [ ] **Step 7: Aprobación del dueño**

Comparte la vista previa y las capturas. No hagas merge sin su "sí" explícito. Pídele en el mismo mensaje lo que aparece en "Lo que aporta el dueño".

- [ ] **Step 8: Merge, push y despliegue**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2a -m "feat: etapa 2a, plantillas de inicio y pasto en rollo" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 2 …`, `shell: 0 de 108 …` y `0`; Vercel despliega `main` (Deployments → `Ready`).

- [ ] **Step 9: Verificación en vivo**

```bash
W=https://www.viverosterra.com
curl -s $W/ | grep -o "<h1[^>]*>[^<]*</h1>"
curl -s $W/ | grep -c 'data-vt-medidor'
curl -s $W/ | grep -cE "fonts.googleapis|tailwind.css|design-system.css"
curl -s $W/pasto-en-rollo-tampico | grep -o "<title>[^<]*</title>"
curl -s $W/pasto-en-rollo-tampico | grep -c "No pedimos el 100% por adelantado"
curl -sI $W/js/vt-medidor.js | grep -iE "^HTTP|content-type"
curl -s $W/ | grep -oE '/css/terra\.[0-9a-f]{10}\.css' | head -1 | xargs -I{} curl -sI $W{} | grep -i cache-control
```

Expected: `<h1 id="vt-h1">Pasto en rollo, jardines y plantas en Tampico y Madero.</h1>`; `1`; `0`; `<title>Pasto en Rollo San Agustín · Tampico</title>`; `2` o más; `HTTP/2 200` y `application/javascript`; `cache-control: public, max-age=31536000, immutable`. En Chrome (escritorio y emulación de iPhone): consola sin errores, Medidor (10 × 10 en mayoreo muestra el aviso y $8,500), simulador, menú y barra. En GA4 DebugView: `generate_lead` con `cta_id` `home:medidor`, `home:hero` y `servicio-pasto:medidor`.

- [ ] **Step 10: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`. Corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 11: Limpiar y preparar 2b**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2a && git branch -d feat/etapa-2a
```

El siguiente sub-plan (2b, sintético) se escribe completo con lo que 2a dejó (`docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`).

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Fotos que parecen generadas (`jardin-residencial-pasto-san-agustin.webp` sobre todo) | Pie `FIG.` documental; se sustituyen con la sesión real sin tocar plantillas (solo `src` en el contenido). |
| Retirar los formularios de correo de la home y de pasto en rollo | La plantilla tiene un solo canal (WhatsApp o teléfono con promesa). Se registra en `PARIDAD` y el dueño lo confirma en la aprobación; si quiere conservarlo, se agrega un componente `formulario()` con labels en 2i (gracias). |
| Testimonios con nombre retirados | No hay prueba de que sean reales (regla del dueño); quedan la línea estática de Google y los clientes B2B autorizados. |
| `tools/pasto/mensualidades.py` usa `round()` (redondeo al par) para la mensualidad y el JS `Math.round`: en mensualidades terminadas en ,50 difieren $1 | El Medidor ya no usa esa función; se corrige en 2b con su prueba (la tienda usa la misma fórmula). |
| El presupuesto de 10 KB gzip se acerca al límite (9 KB hoy) cuando entren tienda, catálogo y artículo | En 2b se agrega minificación sin dependencias en `activos.publicar()` (quitar comentarios y espacios en la copia con hash) y se retira CSS de componentes que ya no use nadie. |
| La meta de 30 KB sin comprimir del spec no se cumple | Se documenta el cambio a la métrica de transferencia (gzip), que es la que mide el spec en §8.2; cada página migrada baja de ~95 KB a ~39 KB de CSS. |

## Lo que aporta el dueño

1. Confirmar que se retiran los formularios de correo de la home y de pasto en rollo (o pedir que se conserven).
2. Confirmar "Visita sin costo" para medir (hoy ya aparece en el sitio como "visita técnica gratuita").
3. Fecha para la sesión de fotos real de medio día (corte del viernes, camión, cuadrilla, vivero de Obregón 209 Sur).
4. Si los testimonios retirados eran reales, nombre y permiso por escrito de cada cliente para reponerlos.
