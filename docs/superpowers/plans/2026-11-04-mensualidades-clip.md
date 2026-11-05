# Mensualidades con tarjeta (Clip) — plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mostrar al cliente el precio en 3, 6, 9 y 12 mensualidades con tarjeta de crédito (total y diferencia contra contado) en la tienda de pasto sintético y en los servicios locales, sin llamarlo "MSI".

**Architecture:** Una sola fórmula (la de la calculadora de Clip) implementada en Python (`tools/pasto/mensualidades.py`, para el HTML generado) y en JS puro (`public/js/vt-mensualidades.js`, para el navegador), con prueba de paridad. El cotizador existente (`tienda-pasto.js`) agrega un selector de forma de pago; los servicios usan un simulador independiente (`vt-simulador.js`).

**Tech Stack:** Python 3.9 stdlib + `unittest`; JavaScript sin dependencias + `node --test`; HTML estático en `public/`, CSS propio; Vercel.

**Spec:** `docs/superpowers/specs/2026-11-04-mensualidades-clip-design.md`

**Repo:** `/Users/luisgovela/dev/viverosterra` (NO usar la copia en `~/Documents/GitHub`, está en iCloud). Antes de empezar: `git pull --rebase`. Commits en español, conventional, con trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, `git add` con rutas explícitas, nunca `.DS_Store`.

**Proveedor (obligatorio):** nunca mencionar a "Clip" ni al proveedor de la terminal en nada dentro de `public/` (textos, atributos, comentarios de JS/CSS/HTML). En `tools/` y `docs/` sí se puede. La revisión final incluye `grep -rni clip public/` que debe salir vacío (salvo palabras como "clipboard" o rutas ajenas que no existen hoy).

**Reglas de texto (obligatorias):** nunca "MSI", "meses sin intereses", "sin intereses", "0%", "recargo", "comisión por (pagar con) tarjeta". Usar "mensualidades con tarjeta de crédito", "precio en N mensualidades", "+$X frente a contado", "Pagando de contado te ahorras $X". Contado = transferencia, efectivo o tarjeta en una exhibición.

**Comandos base:**

```bash
cd tools/pasto && python3 -m unittest discover -s tests -v; cd ../..
node --test public/js/tests/*.test.js
python3 tools/pasto/build.py
```

---

## Mapa de archivos

| Archivo | Acción | Responsabilidad |
|---|---|---|
| `tools/pasto/mensualidades.py` | Crear | Constantes y `planes(contado)` en Python |
| `public/js/vt-mensualidades.js` | Crear | Misma fórmula en JS (`window.VTMensualidades`, `module.exports`) |
| `tools/pasto/tests/test_mensualidades.py` | Crear | Montos, umbrales y paridad con el JS |
| `public/js/tests/vt-mensualidades.test.js` | Crear | Pruebas JS |
| `tools/pasto/common.py` | Modificar | `plan_selector_html()`, carga de `vt-mensualidades.js` en `head()` |
| `tools/pasto/ficha.py` | Modificar | `quote_html` incluye el selector |
| `public/js/tienda-pasto.js` | Modificar | Pintar planes, guardar `plan`, WhatsApp, lista, barra |
| `public/css/tienda-pasto.css` | Modificar | Estilos del selector, tríptico y regla de pagos |
| `tools/pasto/hub.py`, `ciudad.py` | Modificar | Línea en tarjetas y portada; columna en ciudades |
| `public/js/vt-simulador.js` | Crear | Simulador para páginas de servicio |
| `tools/servicios/simulador.py` | Crear | Inserta el simulador en 3 páginas de servicio |
| `tools/servicios/hero.py`, `pages.py` | Modificar | Línea "Paga en mensualidades…" en la portada de servicios |
| `public/css/servicios.css` | Modificar | Estilos del simulador |
| `public/diseno-jardines-tampico/index.html` | Modificar | Planes a plazos en las tarjetas de Plan Terra |
| `tools/pasto/precios.py`, `public/politicas/index.html`, `public/llms.txt` | Modificar | Condiciones |
| `docs/plantillas/whatsapp-mensualidades.md` | Crear | Plantilla para cotizaciones formales |

---

### Task 1: Fórmula en Python

**Files:**
- Create: `tools/pasto/mensualidades.py`
- Test: `tools/pasto/tests/test_mensualidades.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_mensualidades.py
import unittest

from mensualidades import PLAZOS, planes, plazos_disponibles


class MensualidadesTest(unittest.TestCase):
    def test_totales_igual_a_calculadora_clip(self):
        p = {x["plazo"]: x for x in planes(11100)}
        self.assertEqual(p[3]["total"], 12262)
        self.assertEqual(p[6]["total"], 12752)
        self.assertEqual(p[9]["total"], 13376)
        self.assertEqual(p[12]["total"], 13702)
        self.assertEqual(p[6]["diferencia"], 12752 - 11100)
        self.assertEqual(p[12]["mensualidad"], 1142)

    def test_umbrales(self):
        self.assertEqual(plazos_disponibles(1999), [])
        self.assertEqual(plazos_disponibles(2000), [3])
        self.assertEqual(plazos_disponibles(4999), [3])
        self.assertEqual(plazos_disponibles(5000), [3, 6])
        self.assertEqual(plazos_disponibles(14999), [3, 6])
        self.assertEqual(plazos_disponibles(15000), [3, 6, 9, 12])

    def test_planes_marca_disponibles(self):
        disp = {x["plazo"]: x["disponible"] for x in planes(6000)}
        self.assertEqual(disp, {3: True, 6: True, 9: False, 12: False})
        self.assertEqual([x["plazo"] for x in planes(6000)], list(PLAZOS))

    def test_total_redondea_hacia_arriba(self):
        for x in planes(2500):
            self.assertIsInstance(x["total"], int)
            self.assertGreaterEqual(x["total"] * (1 - (0.036 + {3: .0457, 6: .0757, 9: .1107, 12: .1277}[x["plazo"]]) * 1.16), 2500 - 0.5)
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_mensualidades -v; cd ../..`
Expected: `ModuleNotFoundError: No module named 'mensualidades'`

- [ ] **Step 3: Implementar**

```python
# tools/pasto/mensualidades.py
"""Precio en mensualidades con tarjeta de crédito (Clip).

Misma fórmula que la calculadora de Clip: la comisión del plazo se suma a la estándar
y el IVA se aplica sobre ambas. Viveros Terra recibe el contado íntegro.
Mantener igual a public/js/vt-mensualidades.js (prueba de paridad en test_mensualidades.py).
"""
import math

TASA_BASE = 0.036
IVA = 0.16
TASAS = {3: 0.0457, 6: 0.0757, 9: 0.1107, 12: 0.1277}
PLAZOS = (3, 6, 9, 12)
# (monto mínimo de contado, plazos que aplican desde ese monto), de mayor a menor
UMBRALES = ((15000, (3, 6, 9, 12)), (5000, (3, 6)), (2000, (3,)))


def plazos_disponibles(contado):
    for minimo, plazos in UMBRALES:
        if contado >= minimo:
            return list(plazos)
    return []


def total_a_plazos(contado, plazo):
    return math.ceil(contado / (1 - (TASA_BASE + TASAS[plazo]) * (1 + IVA)))


def planes(contado):
    disponibles = plazos_disponibles(contado)
    out = []
    for plazo in PLAZOS:
        total = total_a_plazos(contado, plazo)
        out.append({"plazo": plazo, "total": total, "mensualidad": round(total / plazo),
                    "diferencia": total - math.ceil(contado), "disponible": plazo in disponibles})
    return out


def minimo_de(plazo):
    return min(minimo for minimo, plazos in UMBRALES if plazo in plazos)
```

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_mensualidades -v; cd ../..`
Expected: `OK` (4 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/pasto/mensualidades.py tools/pasto/tests/test_mensualidades.py
git commit -m "feat(pagos): fórmula de mensualidades de Clip con pruebas"
```

---

### Task 2: Fórmula en JS y paridad

**Files:**
- Create: `public/js/vt-mensualidades.js`
- Create: `public/js/tests/vt-mensualidades.test.js`
- Modify: `tools/pasto/tests/test_mensualidades.py` (agregar prueba de paridad)

- [ ] **Step 1: Prueba JS que falla**

```js
// public/js/tests/vt-mensualidades.test.js
const test = require('node:test');
const assert = require('node:assert');
const { planes, plazosDisponibles, totalAPlazos } = require('../vt-mensualidades.js');

test('totales iguales a la calculadora de Clip', () => {
  assert.deepStrictEqual([3, 6, 9, 12].map((p) => totalAPlazos(11100, p)), [12262, 12752, 13376, 13702]);
});

test('umbrales', () => {
  assert.deepStrictEqual(plazosDisponibles(1999), []);
  assert.deepStrictEqual(plazosDisponibles(2000), [3]);
  assert.deepStrictEqual(plazosDisponibles(5000), [3, 6]);
  assert.deepStrictEqual(plazosDisponibles(15000), [3, 6, 9, 12]);
});

test('planes con mensualidad y diferencia', () => {
  const p12 = planes(11100).find((x) => x.plazo === 12);
  assert.strictEqual(p12.mensualidad, 1142);
  assert.strictEqual(p12.diferencia, 2602);
  assert.strictEqual(p12.disponible, false);
});
```

- [ ] **Step 2: Correr y ver que falla**

Run: `node --test public/js/tests/*.test.js`
Expected: FAIL `Cannot find module '../vt-mensualidades.js'`

- [ ] **Step 3: Implementar**

```js
// public/js/vt-mensualidades.js
/* Precio en mensualidades con tarjeta de crédito. Misma fórmula que tools/pasto/mensualidades.py:
   la comisión del plazo se suma a la estándar y el IVA va sobre ambas. Sin DOM. */
(function (root) {
  'use strict';
  const TASA_BASE = 0.036;
  const IVA = 0.16;
  const TASAS = Object.freeze({ 3: 0.0457, 6: 0.0757, 9: 0.1107, 12: 0.1277 });
  const PLAZOS = Object.freeze([3, 6, 9, 12]);
  const UMBRALES = Object.freeze([[15000, [3, 6, 9, 12]], [5000, [3, 6]], [2000, [3]]]);

  function plazosDisponibles(contado) {
    const u = UMBRALES.find(([minimo]) => contado >= minimo);
    return u ? u[1].slice() : [];
  }

  function totalAPlazos(contado, plazo) {
    return Math.ceil(contado / (1 - (TASA_BASE + TASAS[plazo]) * (1 + IVA)));
  }

  function planes(contado) {
    const disp = plazosDisponibles(contado);
    return PLAZOS.map((plazo) => {
      const total = totalAPlazos(contado, plazo);
      return { plazo, total, mensualidad: Math.round(total / plazo),
        diferencia: total - Math.ceil(contado), disponible: disp.includes(plazo) };
    });
  }

  function minimoDe(plazo) {
    return Math.min(...UMBRALES.filter(([, ps]) => ps.includes(plazo)).map(([m]) => m));
  }

  const api = { TASA_BASE, IVA, TASAS, PLAZOS, UMBRALES, plazosDisponibles, totalAPlazos, planes, minimoDe };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VTMensualidades = Object.freeze(api);
})(typeof window !== 'undefined' ? window : globalThis);
```

- [ ] **Step 4: Prueba de paridad en Python** (agregar al final de `test_mensualidades.py`)

```python
import re
from pathlib import Path

from mensualidades import IVA, TASA_BASE, TASAS, UMBRALES

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "vt-mensualidades.js"


class ParidadJSTest(unittest.TestCase):
    def test_constantes_iguales(self):
        src = JS.read_text(encoding="utf-8")
        self.assertIn(f"TASA_BASE = {TASA_BASE}", src)
        self.assertIn(f"IVA = {IVA}", src)
        js_tasas = {int(k): float(v) for k, v in re.findall(r"(\d+): (0\.\d+)", src[src.index("TASAS"):src.index("PLAZOS")])}
        self.assertEqual(js_tasas, TASAS)
        for minimo, plazos in UMBRALES:
            self.assertIn(f"[{minimo}, [{', '.join(map(str, plazos))}]]", src)
```

- [ ] **Step 5: Correr todo**

Run: `node --test public/js/tests/*.test.js && cd tools/pasto && python3 -m unittest tests.test_mensualidades -v; cd ../..`
Expected: JS `pass 3` (más las previas); Python `OK` (5 tests)

- [ ] **Step 6: Commit**

```bash
git add public/js/vt-mensualidades.js public/js/tests/vt-mensualidades.test.js tools/pasto/tests/test_mensualidades.py
git commit -m "feat(pagos): mensualidades en JS con paridad contra Python"
```

---

### Task 3: Selector de forma de pago (HTML generado)

**Files:**
- Modify: `tools/pasto/common.py` (nueva función al final; script en `head()`)
- Modify: `tools/pasto/ficha.py` (`quote_html`)
- Test: `tools/pasto/tests/test_plan_selector.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_plan_selector.py
import unittest

from common import plan_selector_html
from data import MODELOS
from ficha import build_ficha
from hub import build_hub

PROHIBIDAS = ("msi", "sin intereses", "0%", "recargo", "comisión")


class PlanSelectorTest(unittest.TestCase):
    def test_estructura(self):
        html = plan_selector_html("q")
        self.assertIn('role="radiogroup"', html)
        for v in ("0", "3", "6", "9", "12"):
            self.assertIn(f'name="q-plan" value="{v}"', html)
        self.assertIn('value="0" checked', html)
        self.assertIn('id="q-plan-trip"', html)
        self.assertIn('id="q-plan-rule"', html)
        self.assertIn('/politicas#mensualidades', html)

    def test_sin_palabras_prohibidas(self):
        html = plan_selector_html("q").lower()
        for p in PROHIBIDAS:
            self.assertNotIn(p, html)

    def test_en_hub_y_fichas_con_script(self):
        self.assertIn('name="q-plan"', build_hub())
        f = build_ficha(MODELOS[0])
        self.assertIn('name="q-plan"', f)
        self.assertIn('src="/js/vt-mensualidades.js', f)
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_plan_selector -v; cd ../..`
Expected: `ImportError: cannot import name 'plan_selector_html'`

- [ ] **Step 3: Implementar `plan_selector_html` al final de `common.py`**

```python
def plan_selector_html(prefix):
    """Forma de pago: contado o mensualidades con tarjeta. tienda-pasto.js llena montos y disponibilidad."""
    opts = [("0", "Contado", "Transferencia, efectivo o tarjeta en una exhibición")] + [
        (str(n), f"{n} mensualidades", "Con tarjeta de crédito") for n in (3, 6, 9, 12)
    ]
    rows = "\n".join(
        f'''          <label class="plan" data-plan="{v}">
            <input type="radio" name="{prefix}-plan" value="{v}"{" checked" if v == "0" else ""}>
            <span class="plan__name">{esc(name)}<small>{esc(sub)}</small></span>
            <span class="plan__amount num" data-plan-amount></span>
            <span class="plan__total num" data-plan-total></span>
          </label>''' for v, name, sub in opts
    )
    return f"""<fieldset class="plans" id="{prefix}-plans" data-plans>
          <legend id="{prefix}-plans-legend">¿Cómo prefieres pagar?</legend>
          <dl class="plan-trip num" id="{prefix}-plan-trip" aria-live="polite">
            <div><dt>Hoy</dt><dd data-trip-hoy>—</dd></div>
            <div><dt>Al mes</dt><dd data-trip-mes>—</dd></div>
            <div><dt>Total</dt><dd data-trip-total>—</dd></div>
          </dl>
          <div class="pay-rule" id="{prefix}-plan-rule" aria-hidden="true"></div>
          <div class="plans__list" role="radiogroup" aria-labelledby="{prefix}-plans-legend">
{rows}
          </div>
          <p class="plans__save" data-plan-save></p>
          <p class="plans__note">Precio en mensualidades con tarjeta de crédito. Contado (transferencia, efectivo o tarjeta en una exhibición) es el precio más bajo. Montos aproximados: tu banco debe aceptar el plan. Te confirmamos el total antes de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a></p>
        </fieldset>"""
```

En `head()` de `common.py`, cargar el módulo antes de `tienda-pasto.js`: reemplazar
`{extra}<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>` por
`{extra}<script src="/js/vt-mensualidades.js?v={ASSET_VERSION}" defer></script>\n<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>`.

- [ ] **Step 4: Insertar en `quote_html` (`ficha.py`)** — agregar al final del `<div class="quote">`, antes de su cierre:

```python
            {plan_selector_html("q")}
```

(importar `plan_selector_html` desde `common`). `quote_html` lo usan hub, fichas y `/pasto-sintetico-tampico`, así que el selector aparece en los tres.

- [ ] **Step 5: Correr y ver que pasa; regenerar**

Run: `cd tools/pasto && python3 -m unittest discover -s tests; cd ../.. && python3 tools/pasto/build.py >/dev/null`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add tools/pasto/common.py tools/pasto/ficha.py tools/pasto/tests/test_plan_selector.py public/pasto-sintetico public/pasto-sintetico-tampico public/precios public/jardineria-*
git commit -m "feat(pagos): selector de forma de pago en el cotizador"
```

---

### Task 4: Comportamiento del selector (`tienda-pasto.js`)

**Files:**
- Modify: `public/js/tienda-pasto.js`

- [ ] **Step 1: Store con `plan`.** En `readStore()` devolver también `plan` validado:

```js
      const plan = [0, 3, 6, 9, 12].includes(raw.plan) ? raw.plan : 0;
      return { items, estado: typeof raw.estado === 'string' ? raw.estado : '', plan };
```

y en el `catch`: `return { items: [], estado: '', plan: 0 };`

- [ ] **Step 2: Pintar planes.** Agregar antes de `/* ---------- Quote list storage ---------- */`:

```js
  /* ---------- Mensualidades ---------- */
  function planesPara(contado) {
    return window.VTMensualidades && contado > 0 ? window.VTMensualidades.planes(contado) : [];
  }

  function planElegido(contado) {
    const p = planesPara(contado).find((x) => x.plazo === memoryState.plan && x.disponible);
    return p || null;
  }

  function renderPlans(root, contado) {
    if (!root) return;
    const planes = planesPara(contado);
    if (memoryState.plan && !planes.some((x) => x.plazo === memoryState.plan && x.disponible)) {
      writeStore({ ...memoryState, plan: 0 });
    }
    root.hidden = planes.length === 0;
    $$('.plan', root).forEach((row) => {
      const v = Number(row.dataset.plan);
      const input = $('input', row);
      const amount = $('[data-plan-amount]', row);
      const total = $('[data-plan-total]', row);
      if (v === 0) {
        amount.textContent = '';
        total.textContent = money(contado);
      } else {
        const p = planes.find((x) => x.plazo === v);
        input.disabled = !p || !p.disponible;
        row.dataset.disabled = String(input.disabled);
        amount.textContent = p && p.disponible ? `≈ ${money(p.mensualidad)} al mes` : `Desde ${money(window.VTMensualidades.minimoDe(v))}`;
        total.textContent = p && p.disponible ? `${money(p.total)} · +${money(p.diferencia)}` : '';
      }
      input.checked = v === memoryState.plan;
    });
    const p = planElegido(contado);
    $('[data-trip-hoy]', root).textContent = p ? '$0' : money(contado);
    $('[data-trip-mes]', root).textContent = p ? `≈ ${money(p.mensualidad)}` : '—';
    $('[data-trip-total]', root).textContent = money(p ? p.total : contado);
    const ahorro = p ? p.diferencia : (planes.filter((x) => x.disponible).pop() || {}).diferencia;
    $('[data-plan-save]', root).textContent = ahorro ? `Pagando de contado te ahorras ${money(ahorro)}.` : '';
    const rule = $('.pay-rule', root);
    if (rule) {
      rule.innerHTML = '';
      const n = p ? p.plazo : 1;
      for (let i = 0; i < n; i += 1) rule.appendChild(document.createElement('i'));
      rule.dataset.plazo = String(n);
    }
  }

  function planLine(contado) {
    const p = planElegido(contado);
    return p
      ? `Forma de pago: ${p.plazo} mensualidades de ≈ ${money(p.mensualidad)} con tarjeta de crédito (total ${money(p.total)}).`
      : 'Forma de pago: contado.';
  }

  function initPlanInputs(onChange) {
    $$('[data-plans] input[type="radio"]').forEach((input) => {
      input.addEventListener('change', () => {
        writeStore({ ...memoryState, plan: Number(input.value) });
        onChange();
      });
    });
  }
```

`rule.innerHTML = ''` solo vacía; no se inserta texto de usuario.

- [ ] **Step 3: Conectar en `initQuote`.** Dentro de `update()`, después de calcular `$('#q-total')`, agregar:

```js
      const contado = error ? 0 : (estado && estado !== PICKUP ? q.total : q.material);
      renderPlans($('#q-plans'), contado);
```

y en el arreglo `msg`, antes de `'¿Me confirman el precio final?'`, agregar `contado ? planLine(contado) : '',`.
Después de `update();` (la primera llamada), agregar `initPlanInputs(update);`.

- [ ] **Step 4: Lista de cotización.** En `listMessage(state)`, después de la línea del total, agregar
`if (complete && total > 0) lines.push(planLine(total));`. En `renderDrawer()`, no hace falta un selector nuevo:
el plan elegido en el cotizador se refleja en el mensaje.

- [ ] **Step 5: Barra fija.** En `paintBuybarLanded` no tocar el precio; agregar una función que, si `#buybar` existe y el
último contado calculado permite planes, ponga en `.buybar__name` el sufijo ` · o hasta N mensualidades`. Implementación:
guardar el último contado en una variable de módulo `lastContado` dentro de `update()` y llamar `paintBuybarPlan()`:

```js
  let lastContado = 0;
  function paintBuybarPlan() {
    const bar = $('#buybar');
    const extra = bar && $('.buybar__plan', bar);
    if (!bar) return;
    const disp = window.VTMensualidades ? window.VTMensualidades.plazosDisponibles(lastContado) : [];
    let el = extra;
    if (!el) { el = document.createElement('div'); el.className = 'buybar__plan'; $('.buybar__info', bar).appendChild(el); }
    el.textContent = disp.length ? `o hasta ${disp[disp.length - 1]} mensualidades con tarjeta` : '';
  }
```

En `update()`: `lastContado = contado; paintBuybarPlan();`.

- [ ] **Step 6: Verificar**

Run: `node --check public/js/tienda-pasto.js && node --test public/js/tests/*.test.js`
Servir `cd public && python3 -m http.server 8920 &` y con el headless shell:

```bash
B=$(ls ~/Library/Caches/ms-playwright/chromium_headless_shell-1228/*/chrome-headless-shell | head -1)
"$B" --headless --disable-gpu --virtual-time-budget=4000 --dump-dom "http://localhost:8920/pasto-sintetico/index.html?estado=nuevo-leon" | grep -o 'data-trip-total="">[^<]*\|data-plan-total="">[^<]*'
```

Expected: con Toscana 28 y 50 m² en Nuevo León, contado `$11,100`; las filas de 3 y 6 muestran `$12,262 · +$1,162` y `$12,752 · +$1,652`; 9 y 12 deshabilitadas (contado < $15,000). Matar el servidor.

- [ ] **Step 7: Commit**

```bash
git add public/js/tienda-pasto.js
git commit -m "feat(pagos): mensualidades en cotizador, WhatsApp, lista y barra fija"
```

---

### Task 5: Estilos (selector, tríptico, regla de pagos)

**Files:**
- Modify: `public/css/tienda-pasto.css` (al final); `tools/pasto/data.py` (`ASSET_VERSION`)

- [ ] **Step 1: CSS** — usar solo tokens existentes en `:root` (leer el bloque primero).

```css
/* ---------- Forma de pago ---------- */
.plans { border: 0; padding: 0; margin: 18px 0 0; display: grid; gap: 10px; }
.plans legend { font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); margin-bottom: 8px; }
.plan-trip { display: grid; grid-template-columns: repeat(3, 1fr); margin: 0; border-top: 1px solid var(--ink); border-bottom: 1px solid var(--line); }
.plan-trip div { padding: 10px 8px 10px 0; display: flex; flex-direction: column-reverse; }
.plan-trip dt { font-size: var(--text-xs); color: var(--muted); }
.plan-trip dd { margin: 0; font-size: 1.25rem; font-weight: 600; letter-spacing: -0.02em; }
.pay-rule { display: flex; gap: 3px; height: 10px; }
.pay-rule i { flex: 1; background: var(--green); border-radius: 1px; }
.pay-rule[data-plazo="1"] i { background: var(--ink); }
.plans__list { display: grid; gap: 8px; }
.plan { display: grid; grid-template-columns: auto 1fr auto; grid-template-areas: "radio name amount" "radio name total"; gap: 2px 12px; align-items: center; min-height: 56px; padding: 10px 14px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--paper); cursor: pointer; }
.plan input { grid-area: radio; width: 20px; height: 20px; accent-color: var(--green); }
.plan__name { grid-area: name; font-weight: 600; display: flex; flex-direction: column; }
.plan__name small { font-weight: 400; color: var(--muted); font-size: var(--text-xs); }
.plan__amount { grid-area: amount; text-align: right; font-weight: 600; }
.plan__total { grid-area: total; text-align: right; font-size: var(--text-xs); color: var(--ink-2); }
.plan:has(input:checked) { border: 2px solid var(--green); padding: 9px 13px; }
.plan:has(input:focus-visible) { outline: 3px solid var(--green); outline-offset: 2px; }
.plan[data-disabled="true"] { opacity: 0.5; cursor: not-allowed; }
.plans__save { margin: 0; color: var(--green); font-weight: 600; font-size: var(--text-sm); }
.plans__note { margin: 0; font-size: var(--text-xs); color: var(--muted); }
.buybar__plan { font-size: var(--text-xs); color: var(--muted); }
@media (prefers-reduced-motion: reduce) { .plan { transition: none; } }
```

- [ ] **Step 2: Subir versión** `ASSET_VERSION = "20261104"` en `data.py`; `python3 tools/pasto/build.py`.

- [ ] **Step 3: Revisión visual** a 375 y 1440 de `/pasto-sintetico/toscana-28/index.html` y del hub con `?estado=nuevo-leon`
(headless shell, `--window-size=375,2600` y `1440,2200`). Revisar: filas de 56 px, montos alineados a la derecha,
tríptico legible, regla de pagos con N barras al elegir un plazo, sin desplazamiento horizontal.

- [ ] **Step 4: Commit**

```bash
git add public/css/tienda-pasto.css tools/pasto/data.py public/pasto-sintetico public/pasto-sintetico-tampico public/precios public/jardineria-*
git commit -m "style(pagos): selector de forma de pago, tríptico y regla de pagos"
```

---

### Task 6: Líneas en tarjetas, portada y páginas de ciudad

**Files:**
- Modify: `tools/pasto/hub.py` (`card_html`, `hero_html`), `tools/pasto/ciudad.py` (`totales_html`)
- Test: `tools/pasto/tests/test_lineas_pago.py`

- [ ] **Step 1: Prueba**

```python
# tools/pasto/tests/test_lineas_pago.py
import unittest

from ciudad import build_ciudad
from ciudades import CIUDADES
from hub import build_hub


class LineasPagoTest(unittest.TestCase):
    def test_hub(self):
        html = build_hub()
        self.assertEqual(html.count('class="spec-card__pay"'), 9)
        self.assertIn("Paga en mensualidades con tarjeta de crédito", html)

    def test_ciudad_columna(self):
        html = build_ciudad(next(c for c in CIUDADES if c["slug"] == "monterrey"))
        self.assertIn("En mensualidades", html)
        self.assertNotIn("sin intereses", html.lower())
```

- [ ] **Step 2: Implementar**
  - `card_html`: debajo de `spec-card__price`, `<p class="spec-card__pay">Paga en mensualidades con tarjeta</p>`.
  - `hero_html` del hub: después del `<p class="landed" …>`, `<p class="spec-note">Paga en mensualidades con tarjeta de crédito. <a href="#cotizador">Calcula tu plan</a></p>`.
  - `ciudad.totales_html`: agregar columna "En mensualidades" con, por fila, el plazo máximo disponible de
    `mensualidades.planes(total)`: `"{plazo} × ≈ ${mensualidad:,}"` o `"—"` si no hay planes. Encabezado `<th scope="col">En mensualidades</th>`.
  - CSS: `.spec-card__pay { margin: 4px 0 0; font-size: var(--text-xs); color: var(--muted); }`.

- [ ] **Step 3: Correr pruebas y build; commit**

```bash
git add tools/pasto/hub.py tools/pasto/ciudad.py tools/pasto/tests/test_lineas_pago.py public/css/tienda-pasto.css public/pasto-sintetico
git commit -m "feat(pagos): mensualidades en tarjetas, portada y páginas de ciudad"
```

---

### Task 7: Simulador para servicios locales

**Files:**
- Create: `public/js/vt-simulador.js`
- Create: `tools/servicios/simulador.py`
- Modify: `public/css/servicios.css`
- Páginas: `public/pasto-en-rollo-tampico/index.html`, `public/sistema-riego-tampico/index.html`, `public/diseno-jardines-tampico/index.html`

- [ ] **Step 1: JS del simulador**

```js
// public/js/vt-simulador.js
/* Simulador de mensualidades para servicios (monto de una cotización). Depende de vt-mensualidades.js. */
(function () {
  'use strict';
  const WA = '528333268008';
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  function init(root) {
    const M = window.VTMensualidades;
    const input = root.querySelector('[data-sim-monto]');
    const list = root.querySelector('[data-sim-list]');
    const wa = root.querySelector('[data-sim-wa]');
    const servicio = root.dataset.servicio || 'un servicio';
    let plan = 0;
    function paint() {
      const contado = Math.max(0, Math.round(Number(input.value) || 0));
      const planes = M && contado > 0 ? M.planes(contado) : [];
      list.textContent = '';
      const filas = [{ plazo: 0, total: contado, disponible: contado > 0 }].concat(planes);
      filas.forEach((p) => {
        const label = document.createElement('label');
        label.className = 'sim-plan';
        const r = document.createElement('input');
        r.type = 'radio'; r.name = 'sim-plan'; r.value = String(p.plazo);
        r.disabled = !p.disponible; r.checked = p.plazo === plan && p.disponible;
        r.addEventListener('change', () => { plan = p.plazo; paint(); });
        const name = document.createElement('span');
        name.textContent = p.plazo ? `${p.plazo} mensualidades` : 'Contado';
        const amt = document.createElement('span');
        amt.className = 'num';
        amt.textContent = !p.disponible ? (p.plazo ? `Desde ${money(M.minimoDe(p.plazo))}` : '')
          : p.plazo ? `≈ ${money(p.mensualidad)} al mes · total ${money(p.total)} (+${money(p.diferencia)})` : money(p.total);
        label.append(r, name, amt);
        list.appendChild(label);
      });
      if (!filas.some((p) => p.plazo === plan && p.disponible)) plan = 0;
      const elegido = planes.find((p) => p.plazo === plan);
      const msg = [`Hola, quiero cotizar ${servicio}.`,
        contado ? `Mi cotización es de ${money(contado)}.` : '',
        elegido ? `Me interesa pagar en ${elegido.plazo} mensualidades con tarjeta de crédito (total ${money(elegido.total)}).` : 'Pagaría de contado.'
      ].filter(Boolean).join('\n');
      wa.href = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
    }
    input.addEventListener('input', paint);
    paint();
  }
  document.addEventListener('DOMContentLoaded', () => document.querySelectorAll('[data-simulador]').forEach(init));
})();
```

- [ ] **Step 2: Insertador** `tools/servicios/simulador.py`: para cada página `(slug, servicio, monto_ejemplo)` =
`("pasto-en-rollo-tampico", "pasto en rollo instalado", 12000)`, `("sistema-riego-tampico", "un sistema de riego", 18000)`,
`("diseno-jardines-tampico", "el diseño de mi jardín", 6500)`, reemplaza entre `<!-- simulador -->` y `<!-- /simulador -->`
si existen; si no, inserta el bloque justo antes del primer `<section` cuyo contenido contenga "Preguntas frecuentes"
(si no se encuentra, antes de `<footer`). Asegura `<script src="/js/vt-mensualidades.js?v=20261104" defer></script>` y
`<script src="/js/vt-simulador.js?v=20261104" defer></script>` antes de `</body>` (una sola vez). Bloque:

```html
<!-- simulador -->
<section class="sim" data-simulador data-servicio="{servicio}" aria-labelledby="sim-titulo">
  <div class="sim__wrap">
    <p class="sim__eyebrow">Formas de pago</p>
    <h2 id="sim-titulo">Calcula tus mensualidades con tarjeta</h2>
    <p class="sim__lede">Escribe el monto de tu cotización y compara contado contra 3, 6, 9 o 12 mensualidades con tarjeta de crédito. Contado (transferencia, efectivo o tarjeta en una exhibición) es el precio más bajo.</p>
    <label class="sim__field">Monto de tu cotización <input type="number" inputmode="numeric" min="0" step="100" value="{monto_ejemplo}" data-sim-monto></label>
    <div class="sim__list" role="radiogroup" aria-label="Forma de pago" data-sim-list></div>
    <p class="sim__note">Montos aproximados: tu banco debe aceptar el plan. Disponible en cotizaciones desde $2,000. <a href="/politicas#mensualidades">Condiciones</a></p>
    <a class="sim__cta" data-sim-wa href="https://wa.me/528333268008" target="_blank" rel="noopener">Enviar por WhatsApp</a>
  </div>
</section>
<!-- /simulador -->
```

Prueba (crear `tools/servicios/tests/test_simulador.py` si no existe la carpeta, o un script de verificación en el paso 4):
tras correr `python3 tools/servicios/simulador.py` dos veces, cada página contiene exactamente un `data-simulador`
y un `vt-simulador.js`.

- [ ] **Step 3: CSS en `servicios.css`** con el lenguaje de `svc-hero` (tokens `--svc-*`): `.sim` con fondo papel y borde
superior, `.sim__wrap` max-width 760px y padding 48px 16px (32px a 768+), `.sim-plan` grid de 3 columnas, alto mínimo 52px,
borde 1px `--svc-line`, seleccionada con borde 2px `--svc-green`, deshabilitada al 50%; `.sim__cta` igual que `.svc-hero__cta--wa`.

- [ ] **Step 4: Verificar** con el headless shell la página de riego a 375: el simulador muestra 5 filas, con $18,000 todas
habilitadas; al cambiar a 4,000 solo contado y 3. Sin errores en consola.

- [ ] **Step 5: Commit**

```bash
git add public/js/vt-simulador.js tools/servicios/simulador.py public/css/servicios.css public/pasto-en-rollo-tampico/index.html public/sistema-riego-tampico/index.html public/diseno-jardines-tampico/index.html
git commit -m "feat(pagos): simulador de mensualidades en servicios locales"
```

---

### Task 8: Portada de servicios y planes de diseño

**Files:**
- Modify: `tools/servicios/hero.py` (render de `pago_nota`), `tools/servicios/pages.py`
- Modify: `public/diseno-jardines-tampico/index.html` (tarjetas de Plan Terra)

- [ ] **Step 1:** En `hero_html(cfg)`, si `cfg.get("pago_nota")`, agregar después de `svc-hero__lede`:
`<p class="svc-hero__pay">{e(cfg["pago_nota"])} <a href="#sim-titulo">Calcula tu plan</a></p>`. En `pages.py` agregar
`pago_nota="Paga en mensualidades con tarjeta de crédito en cotizaciones desde $2,000."` a `pasto-en-rollo-tampico`,
`diseno-jardines-tampico` y `sistema-riego-tampico`. CSS: `.svc-hero__pay { margin: -6px 0 0; font-size: 14px; color: var(--svc-ink-2); }`.
Correr `cd tools/servicios && python3 hero.py`.

- [ ] **Step 2: Planes de diseño.** Con `mensualidades.planes` calcular para $3,000 (3), $6,500 (3 y 6) y $18,000 (3, 6, 9, 12)
y, en cada tarjeta de Plan Terra de `diseno-jardines-tampico`, justo debajo del precio, insertar una línea
`<p class="text-xs text-gray-500 mt-1">o en N mensualidades de ≈ $X con tarjeta (total $Y)</p>` con el plazo máximo
disponible. Localizar cada precio por su texto (`$3,000`, `$6,500`, `$18,000`) dentro del bloque de la tarjeta; insertar una sola vez.

- [ ] **Step 3: Commit**

```bash
git add tools/servicios/hero.py tools/servicios/pages.py public/css/servicios.css public/pasto-en-rollo-tampico/index.html public/sistema-riego-tampico/index.html public/diseno-jardines-tampico/index.html
git commit -m "feat(pagos): mensualidades en portadas de servicio y planes de diseño"
```

---

### Task 9: Condiciones, precios, llms y plantilla de WhatsApp

**Files:**
- Modify: `public/politicas/index.html` (nueva sección `#mensualidades` y enlace en el índice lateral)
- Modify: `tools/pasto/precios.py` (bloque de mensualidades) y regenerar `/precios`
- Modify: `public/llms.txt`
- Create: `docs/plantillas/whatsapp-mensualidades.md`

- [ ] **Step 1: Política** (después de la sección de garantía de plantas):

```html
<h2 id="mensualidades">Pago en mensualidades con tarjeta de crédito</h2>
<p>Puedes pagar en 3, 6, 9 o 12 mensualidades con tarjeta de crédito. El precio en mensualidades es mayor que el de contado; siempre te mostramos el total antes de enviarte el link de pago.</p>
<ul>
  <li><strong>Contado:</strong> transferencia, efectivo o tarjeta en una sola exhibición. Es el precio más bajo.</li>
  <li><strong>Plazos por monto de contado:</strong> desde $2,000, 3 mensualidades; desde $5,000, 3 o 6; desde $15,000, 3, 6, 9 o 12.</li>
  <li><strong>Total en mensualidades frente a contado:</strong> 3 mensualidades +10.5%, 6 +14.9%, 9 +20.5%, 12 +23.4%.</li>
  <li><strong>Aprobación:</strong> tu banco emisor debe aceptar el plan; el monto de cada mensualidad puede variar por redondeo del banco.</li>
  <li>Aplica a pasto sintético, pasto natural instalado, instalación de pasto sintético, diseño de jardines y sistemas de riego. No aplica a mantenimiento mensual.</li>
</ul>
```

Los porcentajes se calculan con `mensualidades.total_a_plazos(100000, n) / 100000 - 1` y se redondean a 1 decimal; verificar que coinciden.

- [ ] **Step 2: /precios.** En `precios.py`, agregar una sección "Mensualidades con tarjeta" (tabla Plazo · Desde (contado) · Total frente a contado),
generada desde `mensualidades.UMBRALES`/`total_a_plazos`, con enlace a `/politicas#mensualidades`. Regenerar.

- [ ] **Step 3: llms.txt.** Una línea en "Servicios y precios": "Pago en mensualidades con tarjeta de crédito: 3, 6, 9 o 12 mensualidades; el precio en mensualidades es mayor que el de contado (+10.5% a +23.4% según plazo) y se muestra el total antes de pagar. Desde $2,000 (3), $5,000 (6), $15,000 (9 y 12). Condiciones: https://www.viverosterra.com/politicas#mensualidades".

- [ ] **Step 4: Plantilla para el equipo** `docs/plantillas/whatsapp-mensualidades.md`:

```markdown
# Cotización con mensualidades (plantilla para WhatsApp)

Tu cotización: **$[CONTADO]** de contado (transferencia, efectivo o tarjeta en una exhibición).

Si prefieres pagar con tarjeta de crédito en mensualidades:
- 3 mensualidades de ≈ $[M3] (total $[T3])
- 6 mensualidades de ≈ $[M6] (total $[T6])
- 9 mensualidades de ≈ $[M9] (total $[T9])
- 12 mensualidades de ≈ $[M12] (total $[T12])

Pagando de contado te ahorras hasta $[AHORRO]. ¿Cuál te acomoda? Te mando el link de pago.

Cómo calcular: usa el simulador de cualquier página de servicio, o `python3 -c "import sys; sys.path.insert(0,'tools/pasto'); from mensualidades import planes; print(planes(CONTADO))"`.
Solo ofrece los plazos que aplican al monto (desde $2,000: 3; desde $5,000: 3 y 6; desde $15,000: los cuatro).
Nunca digas "meses sin intereses".
```

- [ ] **Step 5: Commit**

```bash
git add public/politicas/index.html tools/pasto/precios.py public/precios/index.html public/llms.txt docs/plantillas/whatsapp-mensualidades.md
git commit -m "docs(pagos): condiciones de mensualidades, lista de precios, llms y plantilla"
```

---

### Task 10: Verificación final y publicación

- [ ] **Step 1: Todas las pruebas** — `cd tools/pasto && python3 -m unittest discover -s tests; cd ../.. && node --test public/js/tests/*.test.js`.
- [ ] **Step 2: Palabras prohibidas en todo `public/`** (excluyendo el comparador que cita "envío gratis" de otros):

```bash
grep -rniE "meses sin intereses|sin intereses|\bMSI\b|recargo|comisi[oó]n por (pagar con )?tarjeta|\bclip\b" public --include=*.html | grep -v "envío gratis" || echo "limpio"
```

Expected: `limpio`.
- [ ] **Step 3: Revisión en navegador** (headless): hub con `?estado=nuevo-leon`, ficha Toscana 28, `/pasto-sintetico-tampico`,
riego y diseño; sin errores en consola; montos de la tabla de ejemplo; foco de teclado en las filas.
- [ ] **Step 4: Publicar** — `git pull --rebase && git push`; esperar despliegue y verificar en vivo con dump-dom que el
cotizador muestra `$12,262 · +$1,162` para 3 mensualidades en el ejemplo.
