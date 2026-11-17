# WhatsApp con contexto · Entrega 1 (pasto sintético + sin «___») Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Que el primer WhatsApp de pasto sintético ya diga modelo, m² y destino (por contexto de la visita o con un panel de preguntas de un toque), y que ningún mensaje del sitio lleve rayas «___».

**Architecture:** Una función de limpieza de huecos con casos compartidos Python/JS, aplicada en `datos.wa_url` (enlaces estáticos) y en `terra.js` `conFirma` (enlaces armados por JS). Un archivo de preguntas (`tools/site/preguntas_wa.py`) genera un JSON por página; `public/js/vt-preguntas.js` (UMD) tiene `armarMensaje` pura y el panel `<dialog>` que intercepta los botones de cotizar de las páginas de sintético. Memoria de la visita en sessionStorage (`vt-visita-v1`) escrita por la ficha, el cotizador y la calculadora; el estado se lee del store existente de la tienda (`vt-cotizacion-v1`).

**Tech Stack:** Python 3 (build estático, unittest), JS ES2019 sin build (node --test), Playwright (pruebas de navegador ya existentes), CSS con tokens de terra.css.

**Spec:** `docs/superpowers/specs/2026-11-16-whatsapp-primer-mensaje-design.md`

---

## Mapa de archivos

| Archivo | Acción | Responsabilidad |
|---|---|---|
| `public/js/tests/casos-huecos.json` | Crear | Casos compartidos de la limpieza de «___» |
| `tools/site/datos.py` | Modificar | `sin_huecos(texto)`; `wa_url` la aplica |
| `public/js/terra.js` | Modificar | `sinHuecos(texto)`; `conFirma` limpia siempre |
| `tools/site/preguntas_wa.py` | Crear | Conjunto «sintetico» y `json_pagina(contexto)` |
| `public/js/vt-preguntas.js` | Crear | `armarMensaje`, memoria de la visita, panel |
| `public/js/tests/casos-preguntas.json` | Crear | Casos compartidos de `armarMensaje` |
| `public/css/terra-preguntas.css` | Crear | Estilos del panel bajo `.vt-preguntas` |
| `tools/site/activos.py`, `shell.py`, `partials.py`, `vercel.json` | Modificar | Registrar la hoja (como terra-calculadora.css) |
| `tools/site/plantillas/{tienda_hub,ficha,tienda_guia,servicio,articulo}.py` | Modificar | Clase del body, script y JSON en páginas de sintético |
| `public/js/tienda-pasto.js`, `public/js/vt-rollos.js` | Modificar | Escribir modelo y m² en la memoria de la visita |
| `tools/site/tests/test_huecos.py`, `test_preguntas_wa.py`, `test_preguntas_navegador.py`; `public/js/tests/vt-preguntas.test.js`, `terra-huecos.test.js` | Crear | Pruebas |

---

### Task 1: Limpieza de «___» (Python y JS, casos compartidos)

**Regla:** se procesa línea por línea.
1. Línea cuyo valor es solo el hueco (`^(.*\S)\s*:\s*___\s*$`): si es la primera línea → `"$1."`; si no → se quita la línea.
2. En las demás líneas: se quita `,?\s*[^,:\n]+:\s*___` (p. ej. `, altura aprox.: ___`), luego `___\s*×\s*` (p. ej. `- ___ × Palma` → `- Palma`), luego cualquier `___` restante; espacios dobles a uno y `trim` de fin de línea.
3. Una línea que queda vacía por la limpieza se quita; las líneas vacías originales (separadores, la firma) se respetan.

**Files:** Create `public/js/tests/casos-huecos.json`, `tools/site/tests/test_huecos.py`, `public/js/tests/terra-huecos.test.js`; Modify `tools/site/datos.py`, `public/js/terra.js`.

- [ ] **Step 1: Casos compartidos**

```json
[
  ["Hola, quiero cotizar: ___\nColonia: ___\nMetros aprox.: ___", "Hola, quiero cotizar."],
  ["Hola, quiero cotizar pasto sintético.\nCiudad o colonia: ___\nMetros aprox.: ___", "Hola, quiero cotizar pasto sintético."],
  ["Hola, quiero cotizar tierra negra.\nCostales o camión: ___\nCantidad: 3\nColonia de entrega: ___", "Hola, quiero cotizar tierra negra.\nCantidad: 3"],
  ["Hola, quiero cotizar palmas.\n- ___ × Palma areca, altura aprox.: ___\n- 2 × Palma kerpis, altura aprox.: 1.5 m", "Hola, quiero cotizar palmas.\n- Palma areca\n- 2 × Palma kerpis, altura aprox.: 1.5 m"],
  ["Hola, quiero cotizar una planta con medidas específicas: ___", "Hola, quiero cotizar una planta con medidas específicas."],
  ["¿Mi terreno está limpio, nivelado y con tierra negra?: ___", "¿Mi terreno está limpio, nivelado y con tierra negra?."],
  ["Hola, quiero cotizar mantenimiento.\nColonia: Petrolera\n\nVengo de viverosterra.com", "Hola, quiero cotizar mantenimiento.\nColonia: Petrolera\n\nVengo de viverosterra.com"],
  ["Hola, quiero cotizar pasto.\nColonia: ___\n\nVengo de viverosterra.com", "Hola, quiero cotizar pasto.\n\nVengo de viverosterra.com"]
]
```

Nota: el caso de «¿…?: ___» como primera línea solo ocurre aislado en pruebas; en el sitio siempre es una línea intermedia y se quita.

- [ ] **Step 2: Prueba Python que falla** (`tools/site/tests/test_huecos.py`)

```python
"""Ningún WhatsApp del sitio lleva rayas «___» (spec del primer mensaje, 2026-11-16)."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import html as html_mod

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402

CASOS = json.loads((Path(paginas.PUBLIC) / "js" / "tests" / "casos-huecos.json").read_text(encoding="utf-8"))


class SinHuecosTest(unittest.TestCase):
    def test_casos_compartidos(self):
        for entrada, esperado in CASOS:
            with self.subTest(entrada=entrada):
                self.assertEqual(datos.sin_huecos(entrada), esperado)

    def test_wa_url_limpia(self):
        self.assertNotIn("___", datos.wa_url("Hola, quiero cotizar: ___\nColonia: ___"))

    def test_ningun_enlace_publicado_con_huecos(self):
        for archivo in Path(paginas.PUBLIC).rglob("*.html"):
            for href in re.findall(r'href="(https://wa\.me/[^"]*)"', archivo.read_text(encoding="utf-8")):
                texto = parse_qs(urlparse(html_mod.unescape(href)).query).get("text", [""])[0]
                with self.subTest(archivo=str(archivo)):
                    self.assertNotIn("___", texto)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3:** `cd tools/site && python3 -m unittest tests.test_huecos` → FAIL (`sin_huecos` no existe).

- [ ] **Step 4: Implementación Python** (en `datos.py`, junto a `con_firma`; `import re` arriba si falta)

```python
_HUECO_SOLO = re.compile(r"^(.*\S)\s*:\s*___\s*$")
_HUECO_CAMPO = re.compile(r",?\s*[^,:\n]+:\s*___")
_HUECO_CANTIDAD = re.compile(r"___\s*×\s*")


def sin_huecos(texto):
    """Quita las rayas «___» que el cliente casi nunca llena (spec del primer mensaje, 2026-11-16): una línea que solo
    pide un dato se quita (la primera se vuelve frase: «Hola, quiero cotizar.»); dentro de una línea se quita el campo.
    Mismos casos que terra.js (public/js/tests/casos-huecos.json)."""
    salida = []
    for i, linea in enumerate(texto.split("\n")):
        if "___" not in linea:
            salida.append(linea)
            continue
        solo = _HUECO_SOLO.match(linea)
        if solo:
            if i == 0:
                salida.append(solo.group(1) + ".")
            continue
        limpia = _HUECO_CANTIDAD.sub("", _HUECO_CAMPO.sub("", linea)).replace("___", "")
        limpia = re.sub(r" {2,}", " ", limpia).rstrip()
        if limpia.strip():
            salida.append(limpia)
    return "\n".join(salida)


def wa_url(texto):
    """Enlace wa.me con el texto sin huecos y codificado por completo (espacios como %20, saltos como %0A)."""
    return f"https://wa.me/{TELEFONO_WA}?text={quote(sin_huecos(texto), safe='')}"
```

- [ ] **Step 5: JS** — en `terra.js`, antes de `conFirma`:

```js
  const HUECO_SOLO = /^(.*\S)\s*:\s*___\s*$/;
  const HUECO_CAMPO = /,?\s*[^,:\n]+:\s*___/g;
  const HUECO_CANTIDAD = /___\s*×\s*/g;
  // Mismos casos que datos.sin_huecos (public/js/tests/casos-huecos.json).
  function sinHuecos(texto) {
    const salida = [];
    String(texto).split('\n').forEach((linea, i) => {
      if (linea.indexOf('___') < 0) { salida.push(linea); return; }
      const solo = linea.match(HUECO_SOLO);
      if (solo) { if (i === 0) salida.push(solo[1] + '.'); return; }
      const limpia = linea.replace(HUECO_CAMPO, '').replace(HUECO_CANTIDAD, '').split('___').join('')
        .replace(/ {2,}/g, ' ').replace(/\s+$/, '');
      if (limpia.trim()) salida.push(limpia);
    });
    return salida.join('\n');
  }
```

y en `conFirma` cambiar el final para limpiar siempre (también un texto ya firmado):

```js
    const limpio = sinHuecos(actual);
    if (/viverosterra\.com/i.test(limpio) && limpio === actual) return href;
    const firmado = /viverosterra\.com/i.test(limpio) ? limpio : (limpio ? limpio + '\n\n' + FIRMA : FIRMA);
    const nuevo = 'text=' + encodeURIComponent(firmado);
```

Exportar `sinHuecos` en `api`.

- [ ] **Step 6: Prueba Node** (`public/js/tests/terra-huecos.test.js`)

```js
const test = require('node:test');
const assert = require('node:assert');
const casos = require('./casos-huecos.json');
const { sinHuecos, conFirma } = require('../terra.js');

test('casos compartidos de huecos', () => {
  for (const [entrada, esperado] of casos) assert.strictEqual(sinHuecos(entrada), esperado);
});

test('conFirma limpia aunque el texto ya venga firmado', () => {
  const href = 'https://wa.me/528333268008?text=' + encodeURIComponent('Hola.\nColonia: ___\n\nVengo de viverosterra.com');
  const texto = decodeURIComponent(conFirma(href).split('text=')[1]);
  assert.strictEqual(texto, 'Hola.\n\nVengo de viverosterra.com');
});
```

- [ ] **Step 7:** `python3 tools/site/build.py`, luego `cd tools/site && python3 -m unittest tests.test_huecos` y `node --test public/js/tests/terra-huecos.test.js` → PASS. Corregir las pruebas existentes que esperaban «___» dentro de un `href` publicado (las funciones puras que arman mensajes pueden seguir devolviendo huecos; solo cambia el enlace). Correr `node --test public/js/tests/*.test.js`.

- [ ] **Step 8: Commit** `feat: WhatsApp sin rayas ___ en todo el sitio`

---

### Task 2: Preguntas de pasto sintético (fuente única en Python)

**Files:** Create `tools/site/preguntas_wa.py`, `tools/site/tests/test_preguntas_wa.py`.

- [ ] **Step 1: Prueba que falla**

```python
"""Preguntas rápidas del WhatsApp (spec del primer mensaje, 2026-11-16)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import preguntas_wa as p  # noqa: E402


class ConjuntoSinteticoTest(unittest.TestCase):
    def test_modelos_reales_y_no_se(self):
        modelo = p.SINTETICO["preguntas"][0]
        self.assertEqual(modelo["clave"], "modelo")
        self.assertEqual([o[0] for o in modelo["opciones"]], [m["slug"] for m in data.MODELOS] + ["no-se"])

    def test_rangos_y_destinos(self):
        claves = [q["clave"] for q in p.SINTETICO["preguntas"]]
        self.assertEqual(claves, ["modelo", "m2", "destino"])
        self.assertEqual([o[0] for o in p.SINTETICO["preguntas"][1]["opciones"]], ["<25", "25-50", "50-100", ">100"])
        self.assertEqual([o[0] for o in p.SINTETICO["preguntas"][2]["opciones"]], ["recoger", "local", "envio"])
        self.assertEqual(p.SINTETICO["estados"], data.ESTADOS_ORDEN)

    def test_json_de_pagina(self):
        bloque = p.json_pagina({"modelo": "toscana-28"}, "Hola, tengo una pregunta sobre pasto sintético.")
        self.assertTrue(bloque.startswith('<script type="application/json" id="vt-preguntas">'))
        cuerpo = json.loads(bloque.split(">", 1)[1].rsplit("<", 1)[0])
        self.assertEqual(cuerpo["fijo"], {"modelo": "toscana-28"})
        self.assertEqual(cuerpo["corto"], "Hola, tengo una pregunta sobre pasto sintético.")
        self.assertEqual(cuerpo["conjunto"]["id"], "sintetico")
        self.assertNotIn("</", bloque.split(">", 1)[1].rsplit("</script>", 1)[0])
```

- [ ] **Step 2:** `python3 -m unittest tests.test_preguntas_wa` → FAIL.

- [ ] **Step 3: Implementación** (`tools/site/preguntas_wa.py`)

```python
"""Preguntas rápidas antes de abrir WhatsApp (spec docs/superpowers/specs/2026-11-16-whatsapp-primer-mensaje-design.md).

Fuente única de las preguntas y sus opciones; vt-preguntas.js las pinta y arma el mensaje. Las opciones son datos ya
publicados (data.MODELOS, data.ESTADOS_ORDEN); los rangos de m² los aprobó el dueño el 2026-11-16."""
import json

import componentes  # noqa: F401  (agrega tools/pasto al path)
import data

CORTO_SINTETICO = "Hola, tengo una pregunta sobre pasto sintético."

SINTETICO = {
    "id": "sintetico",
    "titulo": "Cuéntanos qué buscas",
    "preguntas": [
        {"clave": "modelo", "texto": "¿Qué modelo?",
         "opciones": [(m["slug"], m["nombre"]) for m in data.MODELOS] + [("no-se", "No sé, recomiéndenme")]},
        {"clave": "m2", "texto": "¿Cuántos m²?",
         "opciones": [("<25", "Menos de 25"), ("25-50", "25 a 50"), ("50-100", "50 a 100"), (">100", "Más de 100")]},
        {"clave": "destino", "texto": "¿A dónde?",
         "opciones": [("recoger", "Recoger en el vivero (Cd. Madero)"),
                      ("local", "Instalado en Tampico, Madero o Altamira"), ("envio", "Envío a otro estado")]},
    ],
    "estados": data.ESTADOS_ORDEN,
}


def json_pagina(fijo, corto=CORTO_SINTETICO, conjunto=SINTETICO):
    """Bloque JSON para vt-preguntas.js. fijo: lo que la página ya sabe (modelo de la ficha; estado y ciudad de la
    página de envío); esas preguntas no se muestran. corto: el mensaje de «Solo quiero contactarlos»."""
    cuerpo = json.dumps({"conjunto": conjunto, "fijo": fijo, "corto": corto}, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/json" id="vt-preguntas">{cuerpo.replace("</", "<\\/")}</script>'
```

- [ ] **Step 4:** PASS. **Step 5: Commit** `feat: preguntas rápidas de pasto sintético (fuente única)`

---

### Task 3: `armarMensaje` y memoria de la visita (puro, Node)

**Contrato** `armarMensaje(conjunto, respuestas, ctx)` → texto sin firma:
- `ctx = {fijo: {modelo?, estado?, ciudad?}, recordado: {modelo?, estado?, m2?}, modelos: {slug: nombre}, folio?: fn}`.
- Modelo = `respuestas.modelo || fijo.modelo`. `'no-se'` → sin nombre y línea «Quiero que me recomienden el modelo.».
- m²: `'exacto'` → `unos ${recordado.m2} m²`; rangos → «menos de 25 m²», «entre 25 y 50 m²», «entre 50 y 100 m²», «más de 100 m²».
- Destino: con `fijo.estado` → «con envío a <ciudad> (<estado>)» (o solo uno si son iguales); `recoger` → «para recoger en el vivero de Cd. Madero»; `local` → «instalado en Tampico, Madero o Altamira»; `envio` + `respuestas.estado` → «con envío a <estado>».
- Texto: `Hola, quiero cotizar pasto sintético[ <Modelo>][, <m²>][, <destino>].`
- Folio: si hay modelo real, m² exacto y destino → `\nFolio web: ` + `ctx.folio([{slug, m2}], entrega)` (entrega = estado | `showroom` | `local`).
- `respuestasIniciales(conjunto, ctx)`: preselecciona lo recordado (modelo, estado → destino `envio`, m² → `exacto`) salvo lo fijo.
- `preguntasVisibles(conjunto, ctx)`: quita `modelo` si `fijo.modelo`; quita `destino` si `fijo.estado`.
- `leerVisita(storage)` / `recordar(storage, cambios)`: JSON en `vt-visita-v1` con `modelo` (slug) y `m2` (entero 1–5000); try/catch, valores inválidos se ignoran.

**Files:** Create `public/js/vt-preguntas.js` (parte pura), `public/js/tests/casos-preguntas.json`, `public/js/tests/vt-preguntas.test.js`.

- [ ] **Step 1: Casos** (`casos-preguntas.json`; `modelos` de prueba: toscana-28 → «Toscana 28», irlanda-25 → «Irlanda 25»)

```json
[
  {"r": {}, "fijo": {}, "rec": {}, "esperado": "Hola, quiero cotizar pasto sintético."},
  {"r": {"modelo": "toscana-28", "m2": "25-50", "destino": "envio", "estado": "Jalisco"}, "fijo": {}, "rec": {}, "esperado": "Hola, quiero cotizar pasto sintético Toscana 28, entre 25 y 50 m², con envío a Jalisco."},
  {"r": {"m2": "<25", "destino": "recoger"}, "fijo": {"modelo": "irlanda-25"}, "rec": {}, "esperado": "Hola, quiero cotizar pasto sintético Irlanda 25, menos de 25 m², para recoger en el vivero de Cd. Madero."},
  {"r": {"modelo": "no-se", "m2": ">100", "destino": "local"}, "fijo": {}, "rec": {}, "esperado": "Hola, quiero cotizar pasto sintético, más de 100 m², instalado en Tampico, Madero o Altamira.\nQuiero que me recomienden el modelo."},
  {"r": {"modelo": "toscana-28", "m2": "50-100"}, "fijo": {"estado": "Nuevo León", "ciudad": "Monterrey"}, "rec": {}, "esperado": "Hola, quiero cotizar pasto sintético Toscana 28, entre 50 y 100 m², con envío a Monterrey (Nuevo León)."},
  {"r": {"m2": "exacto"}, "fijo": {"modelo": "irlanda-25", "estado": "CDMX", "ciudad": "CDMX"}, "rec": {"m2": 40}, "esperado": "Hola, quiero cotizar pasto sintético Irlanda 25, unos 40 m², con envío a CDMX.\nFolio web: I25-40-CDMX"}
]
```

- [ ] **Step 2: Prueba Node que falla** (`vt-preguntas.test.js`)

```js
const test = require('node:test');
const assert = require('node:assert');
const casos = require('./casos-preguntas.json');
const P = require('../vt-preguntas.js');
const { folio } = require('../vt-folio.js');

const conjunto = { id: 'sintetico', preguntas: [{ clave: 'modelo' }, { clave: 'm2' }, { clave: 'destino' }] };
const modelos = { 'toscana-28': 'Toscana 28', 'irlanda-25': 'Irlanda 25' };

test('armarMensaje: casos compartidos', () => {
  for (const c of casos) {
    const ctx = { fijo: c.fijo, recordado: c.rec, modelos, folio };
    assert.strictEqual(P.armarMensaje(conjunto, c.r, ctx), c.esperado);
  }
});

test('sin rayas ni dobles comas en ninguna combinación', () => {
  for (const modelo of ['', 'toscana-28', 'no-se']) for (const m2 of ['', '<25', 'exacto'])
    for (const destino of ['', 'recoger', 'local', 'envio']) {
      const t = P.armarMensaje(conjunto, { modelo, m2, destino, estado: destino === 'envio' ? 'Jalisco' : '' },
        { fijo: {}, recordado: { m2: 40 }, modelos, folio });
      assert.ok(!/___|,,|, \.|\s\./.test(t), t);
    }
});

test('preguntas visibles e iniciales', () => {
  const ctx = { fijo: { modelo: 'toscana-28' }, recordado: { estado: 'Jalisco', m2: 30, modelo: 'irlanda-25' }, modelos };
  assert.deepStrictEqual(P.preguntasVisibles(conjunto, ctx).map((q) => q.clave), ['m2', 'destino']);
  assert.deepStrictEqual(P.respuestasIniciales(conjunto, ctx), { m2: 'exacto', destino: 'envio', estado: 'Jalisco' });
});

test('memoria de la visita: valida y tolera errores', () => {
  const mem = new Map();
  const storage = { getItem: (k) => mem.get(k) || null, setItem: (k, v) => mem.set(k, v) };
  P.recordar(storage, { modelo: 'toscana-28', m2: 40 });
  P.recordar(storage, { m2: -3 });
  assert.deepStrictEqual(P.leerVisita(storage), { modelo: 'toscana-28', m2: 40 });
  const roto = { getItem() { throw new Error('bloqueado'); }, setItem() { throw new Error('bloqueado'); } };
  assert.deepStrictEqual(P.leerVisita(roto), {});
  assert.doesNotThrow(() => P.recordar(roto, { m2: 10 }));
});
```

- [ ] **Step 3:** `node --test public/js/tests/vt-preguntas.test.js` → FAIL.

- [ ] **Step 4: Implementación pura** (inicio de `public/js/vt-preguntas.js`)

```js
/* Viveros Terra · vt-preguntas.js · preguntas rápidas antes de WhatsApp (spec del primer mensaje, 2026-11-16).
   Puro: armarMensaje, preguntasVisibles, respuestasIniciales, leerVisita, recordar (node --test).
   Navegador: lee #vt-preguntas (JSON de tools/site/preguntas_wa.py), intercepta los botones de cotizar y abre un
   <dialog> con las preguntas; el enlace final lo toca el cliente (sin window.open). */
(function (root) {
  'use strict';
  const CLAVE = 'vt-visita-v1';
  const MAX_M2 = 5000;
  const RANGOS = { '<25': 'menos de 25 m²', '25-50': 'entre 25 y 50 m²', '50-100': 'entre 50 y 100 m²', '>100': 'más de 100 m²' };

  function leerVisita(storage) {
    try {
      const v = JSON.parse((storage && storage.getItem(CLAVE)) || '{}') || {};
      const salida = {};
      if (typeof v.modelo === 'string' && /^[a-z0-9-]+$/.test(v.modelo)) salida.modelo = v.modelo;
      if (Number.isInteger(v.m2) && v.m2 > 0 && v.m2 <= MAX_M2) salida.m2 = v.m2;
      return salida;
    } catch (err) {
      return {};
    }
  }

  function recordar(storage, cambios) {
    const actual = leerVisita(storage);
    const nuevo = { ...actual };
    if (typeof cambios.modelo === 'string' && /^[a-z0-9-]+$/.test(cambios.modelo)) nuevo.modelo = cambios.modelo;
    if (Number.isInteger(cambios.m2) && cambios.m2 > 0 && cambios.m2 <= MAX_M2) nuevo.m2 = cambios.m2;
    try { storage.setItem(CLAVE, JSON.stringify(nuevo)); } catch (err) { /* modo privado: solo no se recuerda */ }
    return nuevo;
  }

  function preguntasVisibles(conjunto, ctx) {
    const fijo = (ctx && ctx.fijo) || {};
    return conjunto.preguntas.filter((q) => !(q.clave === 'modelo' && fijo.modelo) && !(q.clave === 'destino' && fijo.estado));
  }

  function respuestasIniciales(conjunto, ctx) {
    const fijo = ctx.fijo || {};
    const rec = ctx.recordado || {};
    const r = {};
    if (!fijo.modelo && rec.modelo && ctx.modelos && ctx.modelos[rec.modelo]) r.modelo = rec.modelo;
    if (rec.m2) r.m2 = 'exacto';
    if (!fijo.estado && rec.estado) { r.destino = 'envio'; r.estado = rec.estado; }
    return r;
  }

  function destinoTexto(r, fijo) {
    if (fijo.estado) {
      const lugar = fijo.ciudad && fijo.ciudad !== fijo.estado ? `${fijo.ciudad} (${fijo.estado})` : fijo.estado;
      return { texto: `con envío a ${lugar}`, entrega: fijo.estado };
    }
    if (r.destino === 'recoger') return { texto: 'para recoger en el vivero de Cd. Madero', entrega: 'showroom' };
    if (r.destino === 'local') return { texto: 'instalado en Tampico, Madero o Altamira', entrega: 'local' };
    if (r.destino === 'envio' && r.estado) return { texto: `con envío a ${r.estado}`, entrega: r.estado };
    return null;
  }

  function armarMensaje(conjunto, r, ctx) {
    const fijo = ctx.fijo || {};
    const rec = ctx.recordado || {};
    const modelo = r.modelo || fijo.modelo || '';
    const nombre = modelo && modelo !== 'no-se' ? (ctx.modelos || {})[modelo] || '' : '';
    const partes = [];
    const m2 = r.m2 === 'exacto' && rec.m2 ? rec.m2 : 0;
    if (m2) partes.push(`unos ${m2} m²`);
    else if (RANGOS[r.m2]) partes.push(RANGOS[r.m2]);
    const destino = destinoTexto(r, fijo);
    if (destino) partes.push(destino.texto);
    let texto = `Hola, quiero cotizar pasto sintético${nombre ? ' ' + nombre : ''}${partes.length ? ', ' + partes.join(', ') : ''}.`;
    if (modelo === 'no-se') texto += '\nQuiero que me recomienden el modelo.';
    if (nombre && m2 && destino && typeof ctx.folio === 'function') {
      const f = ctx.folio([{ slug: modelo, m2 }], destino.entrega);
      if (f) texto += `\nFolio web: ${f}`;
    }
    return texto;
  }

  const api = { CLAVE, leerVisita, recordar, preguntasVisibles, respuestasIniciales, armarMensaje };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTPreguntas = Object.freeze({ ...api, recordar: (cambios) => recordar(root.sessionStorage, cambios) });
  // (Task 4 agrega aquí el panel.)
})(typeof window !== 'undefined' ? window : globalThis);
```

Nota: el `try` de `recordar` en el navegador debe tolerar que `root.sessionStorage` lance al leerse; envolver en `(() => { try { return root.sessionStorage; } catch (e) { return null; } })()`.

- [ ] **Step 5:** PASS. **Step 6: Commit** `feat: armarMensaje y memoria de la visita de vt-preguntas.js`

---

### Task 4: Panel en el navegador

**Reglas de intercepción** (listener `click` en `window`, fase de captura, para que terra.js no mida el clic original):
- Solo si existe `#vt-preguntas`.
- Enlace `a[href^="https://wa.me/"]` que NO esté dentro de `header`, `footer`, `dialog`, ni sea `#cot-send`, ni tenga `data-vt-sin-preguntas`, ni su texto decodificado contenga `Folio web:` o `Mi lista` (ya trae el contexto del cotizador o de la lista).
- Clic con Ctrl/Cmd/Shift o botón medio: no se intercepta.
- `preventDefault()` + `stopImmediatePropagation()` y se abre el panel con el `data-cta` del botón original.

**Panel** (`<dialog class="vt-wa-panel" aria-labelledby="vt-wa-titulo">` creado una vez):
- Título del conjunto, botón ✕ (`aria-label="Cerrar"`), un `<fieldset>` por pregunta visible con `<legend>` y botones `aria-pressed` (un toque selecciona, otro toque deselecciona). Destino `envio` muestra un `<select>` con los 32 estados.
- Vista del mensaje: `<p class="vt-wa-panel__vista" aria-live="polite">`.
- `<a class="vt-btn vt-btn--wa" data-cta-wa data-cta="<cta>:panel" target="_blank" rel="noopener">Abrir WhatsApp</a>` con `href` = número del enlace original + `?text=` + mensaje + `\n\nVengo de viverosterra.com`, actualizado en cada toque.
- `<a class="vt-wa-panel__corto" data-cta-wa …>Solo quiero contactarlos</a>` con el mensaje corto.
- Al tocar cualquiera de los dos: `VTMedicion.whatsapp(cta, {preguntas: 'respondidas'|'omitidas'|'solo-contacto'})` y se cierra el panel (la navegación sigue: no se impide).
- `showModal()`; Esc, ✕ o clic en el fondo cierran; al cerrar, foco al botón original.
- Sin `HTMLDialogElement.prototype.showModal`: no se intercepta (el enlace original funciona como hoy).

**Files:** Modify `public/js/vt-preguntas.js` (después de `root.VTPreguntas = …`).

- [ ] **Step 1: Código del panel**

```js
  const doc = root.document;
  const datosPagina = (() => {
    try { return JSON.parse((doc.getElementById('vt-preguntas') || {}).textContent || 'null'); } catch (e) { return null; }
  })();
  const sesion = (() => { try { return root.sessionStorage; } catch (e) { return null; } })();
  if (!datosPagina || !root.HTMLDialogElement || !root.HTMLDialogElement.prototype.showModal) return;

  const FIRMA = 'Vengo de viverosterra.com';
  const modelos = Object.fromEntries((datosPagina.conjunto.preguntas[0].opciones || []).map(([v, t]) => [v, t]));
  const textoDe = (href) => { try { return new URL(href).searchParams.get('text') || ''; } catch (e) { return ''; } };
  const numeroDe = (href) => { try { return new URL(href).pathname.replace(/\D/g, ''); } catch (e) { return ''; } };
  const enlace = (numero, texto) => `https://wa.me/${numero}?text=${encodeURIComponent(texto + '\n\n' + FIRMA)}`;

  function estadoTienda() {
    try { return (JSON.parse(root.localStorage.getItem('vt-cotizacion-v1') || '{}') || {}).estado || ''; } catch (e) { return ''; }
  }

  function interceptable(a, e) {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button > 0) return false;
    if (a.closest('header, footer, dialog') || a.id === 'cot-send' || a.hasAttribute('data-vt-sin-preguntas')) return false;
    return !/Folio web:|Mi lista/i.test(textoDe(a.href));
  }

  let panel = null;
  function crearPanel() {
    panel = doc.createElement('dialog');
    panel.className = 'vt-wa-panel';
    panel.setAttribute('aria-labelledby', 'vt-wa-titulo');
    panel.innerHTML = '<div class="vt-wa-panel__caja"><div class="vt-wa-panel__cab"><h2 id="vt-wa-titulo"></h2>'
      + '<button type="button" class="vt-wa-panel__cerrar" aria-label="Cerrar">×</button></div>'
      + '<div class="vt-wa-panel__preguntas"></div><p class="vt-wa-panel__rotulo">El mensaje que se va a enviar</p>'
      + '<p class="vt-wa-panel__vista" aria-live="polite"></p>'
      + '<a class="vt-btn vt-btn--wa vt-wa-panel__abrir" data-cta-wa target="_blank" rel="noopener">Abrir WhatsApp</a>'
      + '<a class="vt-wa-panel__corto" data-cta-wa target="_blank" rel="noopener">Solo quiero contactarlos</a></div>';
    doc.body.appendChild(panel);
    panel.querySelector('.vt-wa-panel__cerrar').addEventListener('click', () => panel.close());
    panel.addEventListener('click', (e) => { if (e.target === panel) panel.close(); });
    return panel;
  }

  function abrir(original) {
    const p = panel || crearPanel();
    const conjunto = datosPagina.conjunto;
    const ctx = { fijo: datosPagina.fijo || {}, modelos, folio: root.VTFolio ? root.VTFolio.folio : null,
                  recordado: { ...leerVisita(sesion), ...(estadoTienda() ? { estado: estadoTienda() } : {}) } };
    const r = respuestasIniciales(conjunto, ctx);
    const numero = numeroDe(original.href);
    const cta = original.getAttribute('data-cta') || 'pagina:wa';
    const vista = p.querySelector('.vt-wa-panel__vista');
    const abrirWa = p.querySelector('.vt-wa-panel__abrir');
    const corto = p.querySelector('.vt-wa-panel__corto');
    p.querySelector('#vt-wa-titulo').textContent = conjunto.titulo;
    const caja = p.querySelector('.vt-wa-panel__preguntas');
    caja.textContent = '';
    const pintar = () => {
      const texto = armarMensaje(conjunto, r, ctx);
      vista.textContent = texto;
      abrirWa.href = enlace(numero, texto);
      caja.querySelectorAll('[data-v]').forEach((b) => b.setAttribute('aria-pressed', String(r[b.dataset.q] === b.dataset.v)));
      const sel = caja.querySelector('select');
      if (sel) { sel.hidden = r.destino !== 'envio'; sel.value = r.estado || ''; }
    };
    preguntasVisibles(conjunto, ctx).forEach((q) => {
      const fs = doc.createElement('fieldset');
      const lg = doc.createElement('legend');
      lg.textContent = q.texto;
      fs.appendChild(lg);
      const opciones = q.clave === 'm2' && ctx.recordado.m2 ? [['exacto', `Unos ${ctx.recordado.m2} m²`], ...q.opciones] : q.opciones;
      opciones.forEach(([v, t]) => {
        const b = doc.createElement('button');
        b.type = 'button'; b.dataset.q = q.clave; b.dataset.v = v; b.textContent = t;
        b.addEventListener('click', () => { r[q.clave] = r[q.clave] === v ? '' : v; pintar(); });
        fs.appendChild(b);
      });
      if (q.clave === 'destino') {
        const sel = doc.createElement('select');
        sel.setAttribute('aria-label', 'Estado');
        sel.innerHTML = '<option value="">Elige tu estado</option>';
        conjunto.estados.forEach((e) => { const o = doc.createElement('option'); o.value = e; o.textContent = e; sel.appendChild(o); });
        sel.addEventListener('change', () => { r.estado = sel.value; pintar(); });
        fs.appendChild(sel);
      }
      caja.appendChild(fs);
    });
    corto.href = enlace(numero, datosPagina.corto);
    const medir = (tipo) => () => {
      if (root.VTMedicion) root.VTMedicion.whatsapp(`${cta}:panel`, { preguntas: tipo === 'abrir' ? (Object.values(r).some(Boolean) ? 'respondidas' : 'omitidas') : 'solo-contacto' });
      p.close();
    };
    abrirWa.onclick = medir('abrir');
    corto.onclick = medir('corto');
    p.onclose = () => original.focus();
    pintar();
    p.showModal();
  }

  root.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('a[href^="https://wa.me/"]') : null;
    if (!a || !interceptable(a, e)) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    abrir(a);
  }, true);
```

(Reemplaza el comentario `// (Task 4 agrega aquí el panel.)`; usar las funciones del mismo cierre.)

- [ ] **Step 2:** `node --test public/js/tests/vt-preguntas.test.js` sigue en PASS (en Node se sale antes por `module.exports`). **Commit** `feat: panel de preguntas rápidas antes de WhatsApp`

---

### Task 5: Hoja `terra-preguntas.css` y su registro

**Files:** Create `public/css/terra-preguntas.css`; Modify `tools/site/activos.py` (`"terra-preguntas.css": "css/terra-preguntas.css"`), `tools/site/shell.py` (`HOJAS_POR_CLASE["preguntas"] = "vt-preguntas"`), `tools/site/partials.py` (parámetro `preguntas=False` y `<link>` como `calculadora`), `vercel.json` y `tools/site/tests/test_vercel.py` (agregar `terra-preguntas` a la regex), `tools/site/tests/test_activos.py` (stub `.vt-preguntas .vt-x{}`).

- [ ] **Step 1: CSS** (solo tokens de terra.css; sin colores literales; movimiento con transform/opacity y `prefers-reduced-motion`)

```css
/* Panel de preguntas rápidas antes de WhatsApp (spec del primer mensaje, 2026-11-16). Solo en <body class="… vt-preguntas">. */
.vt-preguntas .vt-wa-panel{padding:0;border:0;max-width:min(560px,100vw);width:100%;background:transparent;color:var(--vt-ink)}
.vt-preguntas .vt-wa-panel::backdrop{background:rgb(0 0 0/.45)}
.vt-preguntas .vt-wa-panel__caja{background:var(--vt-paper);border-radius:var(--vt-radio-l,16px);padding:20px 16px;display:grid;gap:14px;max-height:90dvh;overflow:auto}
.vt-preguntas .vt-wa-panel__cab{display:flex;justify-content:space-between;align-items:center;gap:12px}
.vt-preguntas .vt-wa-panel__cab h2{margin:0;font-size:1.25rem}
.vt-preguntas .vt-wa-panel__cerrar{min-width:44px;min-height:44px;border:0;background:transparent;font-size:1.75rem;cursor:pointer;color:inherit}
.vt-preguntas .vt-wa-panel fieldset{border:0;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.vt-preguntas .vt-wa-panel legend{font-weight:700;margin-bottom:8px;padding:0}
.vt-preguntas .vt-wa-panel [data-v]{min-height:44px;padding:8px 14px;border:1px solid var(--vt-line);border-radius:999px;background:var(--vt-paper);color:inherit;font:inherit;cursor:pointer}
.vt-preguntas .vt-wa-panel [aria-pressed=true]{background:var(--vt-field-deep);border-color:var(--vt-field-deep);color:var(--vt-on-dark)}
.vt-preguntas .vt-wa-panel [data-v]:focus-visible,.vt-preguntas .vt-wa-panel select:focus-visible{outline:3px solid var(--vt-focus,var(--vt-tag));outline-offset:2px}
.vt-preguntas .vt-wa-panel select{min-height:44px;width:100%;font:inherit;padding:8px}
.vt-preguntas .vt-wa-panel__rotulo{margin:0;font-size:.875rem;color:var(--vt-ink-soft)}
.vt-preguntas .vt-wa-panel__vista{margin:0;padding:12px;border-radius:12px;background:var(--vt-paper-deep);white-space:pre-line}
.vt-preguntas .vt-wa-panel__abrir{justify-content:center}
.vt-preguntas .vt-wa-panel__corto{justify-self:center;min-height:44px;display:inline-flex;align-items:center;color:inherit}
@media (max-width:767px){.vt-preguntas .vt-wa-panel{margin:auto 0 0;max-width:100vw}.vt-preguntas .vt-wa-panel__caja{border-radius:16px 16px 0 0}}
@media (prefers-reduced-motion:no-preference){.vt-preguntas .vt-wa-panel[open] .vt-wa-panel__caja{animation:vt-wa-sube .2s ease-out}}
@keyframes vt-wa-sube{from{transform:translateY(16px);opacity:0}to{transform:none;opacity:1}}
```

Antes de escribirla, confirmar los nombres reales de los tokens en `public/css/terra.css` (`grep -o -- "--vt-[a-z-]*" public/css/terra.css | sort -u`) y ajustar; la prueba de tokens del proyecto rechaza variables inexistentes si la hay.

- [ ] **Step 2:** `python3 tools/site/build.py`; `python3 -m unittest tests.test_activos tests.test_vercel` → PASS. **Commit** `feat: hoja terra-preguntas.css`

---

### Task 6: Activar en las páginas de pasto sintético

Páginas: hub `/pasto-sintetico`, 9 fichas, 19 ciudades, perros, cuántos rollos, `/pasto-sintetico-tampico` y los artículos de `blog_clusters._SINTETICOS`.

**Files:** Modify `tools/site/plantillas/tienda_hub.py`, `ficha.py`, `tienda_guia.py`, `servicio.py`, `articulo.py`.

- [ ] **Step 1: Prueba que falla** (en `tools/site/tests/test_preguntas_wa.py`)

```python
import generar  # noqa: E402
import paginas  # noqa: E402
from contenido import blog_clusters  # noqa: E402

SINTETICO = ([r for r, *_ in generar.PAGINAS if r.startswith("/pasto-sintetico")] + ["/pasto-sintetico-tampico"]
             + [f"/blog/{s}" for s in blog_clusters._SINTETICOS if s])


def leer(ruta):
    return (Path(paginas.PUBLIC) / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


class PaginasConPreguntasTest(unittest.TestCase):
    def test_paginas_de_sintetico_llevan_panel(self):
        for ruta in SINTETICO:
            html = leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn('id="vt-preguntas"', html)
                self.assertRegex(html, r'<body class="[^"]*\bvt-preguntas\b')
                self.assertIn("/js/vt-preguntas.js", html)
                self.assertIn("terra-preguntas", html)

    def test_lo_fijo_de_cada_pagina(self):
        fijo = lambda ruta: json.loads(re.search(r'id="vt-preguntas">(.*?)</script>', leer(ruta)).group(1))["fijo"]
        self.assertEqual(fijo("/pasto-sintetico/toscana-28"), {"modelo": "toscana-28"})
        self.assertEqual(fijo("/pasto-sintetico/envio/monterrey"), {"estado": "Nuevo León", "ciudad": "Monterrey"})
        self.assertEqual(fijo("/pasto-sintetico"), {})

    def test_otras_paginas_sin_panel(self):
        for ruta in ("/", "/mantenimiento-jardines-tampico", "/blog/palma-areca-tampico"):
            with self.subTest(ruta=ruta):
                self.assertNotIn('id="vt-preguntas"', leer(ruta))
```

(agregar `import re` al archivo.)

- [ ] **Step 2:** FAIL. **Step 3: Cambios por plantilla** — patrón común: `preguntas_wa.json_pagina(fijo)` en `head_extra`, `"/js/vt-preguntas.js"` al final de `scripts` (después de `vt-folio.js`), y `" vt-preguntas"` en `clase_body`.
  - `tienda_hub.py`: `fijo={}`.
  - `ficha.py`: `fijo={"modelo": m["slug"]}`.
  - `tienda_guia.py`: ciudad → `fijo={"estado": x["estado"], "ciudad": x["nombre"]}` (llega por `k["preguntas_fijo"]`, que `contenido/ciudad.py` agrega); perros y cuántos rollos → `{}`.
  - `servicio.py`: solo cuando `k.get("preguntas")` (lo pone `contenido/sintetico_tampico.py`: `"preguntas": {}`).
  - `articulo.py`: solo si el slug está en `blog_clusters._SINTETICOS`; agregar `scripts=("/js/vt-folio.js", "/js/vt-preguntas.js")`.

- [ ] **Step 4:** build + PASS; `test_paridad`, `test_portada`, `test_tienda`, `test_generar` en PASS. **Commit** `feat: panel de preguntas en las páginas de pasto sintético`

---

### Task 7: Memoria de la visita desde la ficha, el cotizador y la calculadora

**Files:** Modify `public/js/tienda-pasto.js`, `public/js/vt-rollos.js`.

- [ ] **Step 1:** En `tienda-pasto.js`, en el arranque (`DOMContentLoaded`), si hay `#vt-model`: `window.VTPreguntas && window.VTPreguntas.recordar({ modelo: slugDeFicha })` (leer `slug` del mismo JSON que `modeloDeFicha`). Donde el cotizador recalcula con m² válidos: `window.VTPreguntas && window.VTPreguntas.recordar({ m2 })` y, si hay modelo elegido, `{ modelo: slug }`.
- [ ] **Step 2:** En `vt-rollos.js`, tras calcular un resultado válido: `if (root.VTPreguntas) root.VTPreguntas.recordar({ m2: r.m2 })`.
- [ ] **Step 3:** `node --test public/js/tests/*.test.js` en PASS. **Commit** `feat: la ficha, el cotizador y la calculadora recuerdan modelo y m²`

---

### Task 8: Pruebas de navegador (sin abrir WhatsApp)

**Files:** Create `tools/site/tests/test_preguntas_navegador.py` siguiendo la base de `test_tienda_navegador.py` (servidor local, `self.pagina(ancho)`). Bloquear `wa.me` con `page.route("https://wa.me/**", lambda r: r.abort())` y nunca hacer clic en el enlace final: solo leer su `href`.

- [ ] **Step 1: Pruebas**
  - Hub: clic en el CTA del hero → `dialog[open]`; tocar «Toscana 28», «25 a 50», «Envío a otro estado», elegir «Jalisco» → `href` de `.vt-wa-panel__abrir` decodificado empieza con «Hola, quiero cotizar pasto sintético Toscana 28, entre 25 y 50 m², con envío a Jalisco.» y termina con «Vengo de viverosterra.com».
  - Ficha Toscana 28: el panel no muestra «¿Qué modelo?».
  - Monterrey: no muestra «¿A dónde?» y la vista dice «con envío a Monterrey (Nuevo León)».
  - Calculadora 7 × 5 y luego ficha Irlanda 25: aparece «Unos 40 m²» preseleccionado y la vista lleva «Folio web: I25-40-…» solo si hay destino.
  - Esc cierra y el foco vuelve al botón; `#cot-send` y los enlaces del `footer` no abren el panel.
  - Anchos 320, 375, 768 y 1440: el panel abierto no desborda (`scrollWidth - clientWidth <= 1`).
- [ ] **Step 2:** `python3 -m unittest discover -s tests -p "test_preguntas_navegador.py"` → PASS. **Commit** `test: panel de WhatsApp en navegador`

---

### Task 9: Verificación final

- [ ] `python3 tools/site/build.py` dos veces (la segunda, 0 cambios) y `python3 tools/pasto/build.py`.
- [ ] Suite completa en segundo plano: `cd tools/site && python3 -m unittest discover -s tests`; `cd tools/pasto && python3 -m unittest discover -s tests`; `node --test public/js/tests/*.test.js apps-script/tests/*.test.js`.
- [ ] Vista previa (launch.json «wa», puerto 8886) en celular y escritorio: abrir el panel en hub, ficha, ciudad, Tampico y un artículo; capturas.
- [ ] Revisar que ningún enlace publicado tenga «___» y que el folio siga leyéndose (`VTFolio.leer`) con un mensaje del panel.
- [ ] Spec: anotar en «Resultado» lo publicado. Merge solo con «publícala» del dueño.
