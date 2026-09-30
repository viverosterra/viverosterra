# Tienda nacional de pasto sintético — plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rediseñar `/pasto-sintetico` alrededor del "precio puesto en tu estado" y agregar 11 páginas de envío por ciudad y una página de pasto para perros.

**Architecture:** HTML estático generado por Python (`tools/pasto/*.py`, entrada `build.py`) y publicado por Vercel desde `public/`. Precios, zonas y fletes viven en `tools/pasto/data.py`; el cálculo del precio puesto existe en Python (build) y en un módulo JS puro (`public/js/vt-landed.js`) que usa la tienda en el navegador. El estado elegido se guarda en el store existente `vt-cotizacion-v1` (campo `estado`) y se acepta por `?estado=`.

**Tech Stack:** Python 3.9 stdlib (`unittest`), JavaScript sin dependencias (Node `node --test` para pruebas puras), CSS propio `public/css/tienda-pasto.css`, Vercel.

**Spec:** `docs/superpowers/specs/2026-09-30-tienda-nacional-pasto-design.md`

**Reglas del proyecto (no negociables):** nunca mencionar al proveedor ni su marca; no usar la palabra "Oasis"; no ofrecer muestras físicas; el envío nunca es gratis (se cobra por rollo); sin modelos deportivos ni pádel; commits en español con prefijo convencional y trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; usar `git add` con rutas explícitas (hay archivos ajenos sin rastrear y archivos " 2.webp" duplicados que no se suben).

---

## Mapa de archivos

| Archivo | Acción | Responsabilidad |
|---|---|---|
| `tools/pasto/data.py` | Modificar | `landed_m2()`, `ESTADOS_ORDEN`, `estado_slug()` |
| `tools/pasto/ciudades.py` | Crear | Datos de las 11 ciudades (clima, modelos, FAQ) |
| `tools/pasto/ciudad.py` | Crear | Plantilla de `/pasto-sintetico/envio/<slug>` |
| `tools/pasto/perros.py` | Crear | Plantilla de `/pasto-sintetico/perros` |
| `tools/pasto/hub.py` | Modificar | Portada con selector, franja de confianza, tarjetas con regla, comparador, ciudades |
| `tools/pasto/ficha.py` | Modificar | Existencia nacional y precio puesto |
| `tools/pasto/common.py` | Modificar | `estado_select_html()`, `height_rule_html()`, `trust_band_html()` |
| `tools/pasto/build.py` | Modificar | Escribir ciudades y perros; actualizar sitemap |
| `tools/pasto/sitemap.py` | Crear | Agregar/actualizar URLs de la tienda en `public/sitemap.xml` |
| `tools/pasto/tests/test_*.py` | Crear | Pruebas `unittest` |
| `public/js/vt-landed.js` | Crear | Cálculo puro del precio puesto (navegador y Node) |
| `public/js/tests/vt-landed.test.js` | Crear | Pruebas `node --test` |
| `public/js/tienda-pasto.js` | Modificar | Exponer `getEstado`/`setEstado` y sincronizar el selector del cotizador |
| `public/js/tienda-hub.js` | Modificar | Selector de la portada, repintar precios, comparador, `?estado=` |
| `public/css/tienda-pasto.css` | Modificar | Selector de portada, regla de altura, franja, comparador, tarjetas de ciudad |
| `public/blog/cuanto-cuesta-pasto-sintetico-mexico/index.html` | Modificar | Tabla de precio puesto por ciudad |
| `public/llms.txt` | Modificar | Entradas de ciudades y perros |

Comandos base (desde la raíz del repo `/Users/luisgovela/Documents/GitHub/viverosterra`):

```bash
cd tools/pasto && python3 -m unittest discover -s tests -v; cd ../..
node --test public/js/tests/
python3 tools/pasto/build.py
```

---

### Task 1: Arnés de pruebas y precio puesto en Python

**Files:**
- Create: `tools/pasto/tests/__init__.py` (vacío)
- Create: `tools/pasto/tests/test_landed.py`
- Modify: `tools/pasto/data.py` (después de `ZONA_ESTADOS`)

- [ ] **Step 1: Escribir la prueba que falla**

```python
# tools/pasto/tests/test_landed.py
import unittest

from data import MODELOS, ZONAS, ZONA_ESTADOS, estado_slug, landed_m2, zona_de


class LandedTest(unittest.TestCase):
    def aruba(self):
        return next(m for m in MODELOS if m["slug"] == "aruba-10")

    def test_landed_por_zona(self):
        self.assertEqual(landed_m2(self.aruba(), "A"), 157)
        self.assertEqual(landed_m2(self.aruba(), "B"), 162)
        self.assertEqual(landed_m2(self.aruba(), "C"), 167)

    def test_zona_de_estado(self):
        self.assertEqual(zona_de("Nuevo León"), "B")
        self.assertEqual(zona_de("CDMX"), "A")
        self.assertIsNone(zona_de("Narnia"))

    def test_estado_slug(self):
        self.assertEqual(estado_slug("Nuevo León"), "nuevo-leon")
        self.assertEqual(estado_slug("Estado de México"), "estado-de-mexico")
        self.assertEqual(estado_slug("CDMX"), "cdmx")

    def test_todas_las_zonas_tienen_tarifa(self):
        self.assertEqual(set(ZONA_ESTADOS), set(ZONAS))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_landed -v; cd ../..`
Expected: `ImportError: cannot import name 'estado_slug'`

- [ ] **Step 3: Implementar en `data.py`** (pegar justo después del bloque `ZONA_ESTADOS`)

```python
import unicodedata

ROLLO_M2 = 50


def zona_de(estado):
    """Zona de envío (A, B o C) del estado, o None si no existe."""
    for zona, (_nombre, estados) in ZONA_ESTADOS.items():
        if estado in estados:
            return zona
    return None


def landed_m2(modelo, zona):
    """Precio por m² puesto en casa: rollo completo + flete de 1 rollo, redondeado."""
    return round(modelo["rollo"] + ZONAS[zona] / ROLLO_M2)


def estado_slug(estado):
    sin_acentos = unicodedata.normalize("NFKD", estado).encode("ascii", "ignore").decode()
    return "-".join(sin_acentos.lower().split())


ESTADOS_ORDEN = sorted((e for _z, (_n, es) in ZONA_ESTADOS.items() for e in es), key=estado_slug)
```

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_landed -v; cd ../..`
Expected: `OK` (4 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/pasto/tests/__init__.py tools/pasto/tests/test_landed.py tools/pasto/data.py
git commit -m "feat(pasto): cálculo de precio puesto por zona con pruebas"
```

---

### Task 2: Paridad de zonas entre Python y JS

**Files:**
- Create: `tools/pasto/tests/test_paridad_js.py`

- [ ] **Step 1: Escribir la prueba**

```python
# tools/pasto/tests/test_paridad_js.py
import re
import unittest
from pathlib import Path

from data import ZONAS, ZONA_ESTADOS

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "tienda-pasto.js"


class ParidadTest(unittest.TestCase):
    def test_estado_zona_igual_en_js(self):
        src = JS.read_text(encoding="utf-8")
        bloque = src[src.index("const ESTADO_ZONA = {"):src.index("};", src.index("const ESTADO_ZONA = {"))]
        js = dict(re.findall(r"'([^']+)':\s*'([ABC])'", bloque))
        py = {e: z for z, (_n, es) in ZONA_ESTADOS.items() for e in es}
        self.assertEqual(js, py)

    def test_tarifas_iguales_en_js(self):
        src = JS.read_text(encoding="utf-8")
        js = {z: int(t) for z, t in re.findall(r"([ABC]):\s*\{\s*tarifa:\s*(\d+)", src)}
        self.assertEqual(js, ZONAS)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr**

Run: `cd tools/pasto && python3 -m unittest tests.test_paridad_js -v; cd ../..`
Expected: `OK` (hoy ya coinciden; la prueba evita que se separen)

- [ ] **Step 3: Commit**

```bash
git add tools/pasto/tests/test_paridad_js.py
git commit -m "test(pasto): paridad de zonas y tarifas entre data.py y tienda-pasto.js"
```

---

### Task 3: Módulo JS puro `vt-landed.js`

**Files:**
- Create: `public/js/vt-landed.js`
- Create: `public/js/tests/vt-landed.test.js`

- [ ] **Step 1: Escribir la prueba que falla**

```js
// public/js/tests/vt-landed.test.js
const test = require('node:test');
const assert = require('node:assert');
const { landedM2, slugEstado, estadoDesdeSlug } = require('../vt-landed.js');

const ZONAS = { A: 900, B: 1150, C: 1400 };
const ESTADO_ZONA = { 'Nuevo León': 'B', CDMX: 'A', 'Yucatán': 'C' };

test('precio puesto por zona', () => {
  assert.strictEqual(landedM2(139, 'Nuevo León', ESTADO_ZONA, ZONAS), 162);
  assert.strictEqual(landedM2(139, 'CDMX', ESTADO_ZONA, ZONAS), 157);
  assert.strictEqual(landedM2(139, 'Yucatán', ESTADO_ZONA, ZONAS), 167);
});

test('estado desconocido devuelve null', () => {
  assert.strictEqual(landedM2(139, 'Narnia', ESTADO_ZONA, ZONAS), null);
});

test('slug ida y vuelta', () => {
  assert.strictEqual(slugEstado('Nuevo León'), 'nuevo-leon');
  assert.strictEqual(estadoDesdeSlug('nuevo-leon', Object.keys(ESTADO_ZONA)), 'Nuevo León');
  assert.strictEqual(estadoDesdeSlug('no-existe', Object.keys(ESTADO_ZONA)), null);
});
```

- [ ] **Step 2: Correr y ver que falla**

Run: `node --test public/js/tests/`
Expected: FAIL `Cannot find module '../vt-landed.js'`

- [ ] **Step 3: Implementar**

```js
// public/js/vt-landed.js
/* Precio puesto en casa por estado. Puro: sin DOM. Se usa en el navegador (window.VTLanded) y en Node (pruebas). */
(function (root) {
  'use strict';
  const ROLLO_M2 = 50;

  function landedM2(precioRollo, estado, estadoZona, zonas) {
    const zona = estadoZona[estado];
    if (!zona || !(zona in zonas)) return null;
    return Math.round(precioRollo + zonas[zona] / ROLLO_M2);
  }

  function slugEstado(estado) {
    return estado.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().trim().split(/\s+/).join('-');
  }

  function estadoDesdeSlug(slug, estados) {
    return estados.find((e) => slugEstado(e) === slug) || null;
  }

  const api = { landedM2, slugEstado, estadoDesdeSlug };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VTLanded = Object.freeze(api);
})(typeof window !== 'undefined' ? window : globalThis);
```

- [ ] **Step 4: Correr y ver que pasa**

Run: `node --test public/js/tests/`
Expected: `pass 3`

- [ ] **Step 5: Commit**

```bash
git add public/js/vt-landed.js public/js/tests/vt-landed.test.js
git commit -m "feat(tienda): módulo JS puro de precio puesto con pruebas"
```

---

### Task 4: `tienda-pasto.js` expone el estado

**Files:**
- Modify: `public/js/tienda-pasto.js` (bloque `window.VTTienda = Object.freeze({...})` al final y `initQuote`)

- [ ] **Step 1: Exportar tablas y estado.** Reemplazar el objeto de `window.VTTienda` por:

```js
    window.VTTienda = Object.freeze({
      models,
      zonas: Object.fromEntries(Object.entries(ZONAS).map(([z, v]) => [z, v.tarifa])),
      estadoZona: ESTADO_ZONA,
      getEstado: () => (memoryState.estado && memoryState.estado !== PICKUP ? memoryState.estado : ''),
      setEstado: (estado) => {
        if (estado && !(estado in ESTADO_ZONA)) return;
        writeStore({ ...memoryState, estado });
        const sel = $('#estado');
        if (sel && sel.value !== estado) { sel.value = estado; sel.dispatchEvent(new Event('change')); }
        document.dispatchEvent(new CustomEvent('vt:estado', { detail: { estado } }));
      },
      addItem: (slug, m2) => {
        const model = models.find((m) => m.slug === slug);
        if (model) addItem(model, m2);
      },
      selectModel: (slug) => { if (quote) quote.selectModel(slug); },
    });
```

- [ ] **Step 2: Avisar cuando cambia en el cotizador.** En `initQuote`, cambiar el listener del selector:

```js
    sel.addEventListener('change', () => {
      writeStore({ ...memoryState, estado: sel.value });
      update();
      document.dispatchEvent(new CustomEvent('vt:estado', { detail: { estado: sel.value === PICKUP ? '' : sel.value } }));
    });
```

- [ ] **Step 3: Verificar sin errores de sintaxis**

Run: `node --check public/js/tienda-pasto.js && cd tools/pasto && python3 -m unittest tests.test_paridad_js; cd ../..`
Expected: sin salida de error; `OK`

- [ ] **Step 4: Commit**

```bash
git add public/js/tienda-pasto.js
git commit -m "feat(tienda): exponer getEstado/setEstado y evento vt:estado"
```

---

### Task 5: Piezas comunes (selector, regla de altura, franja de confianza)

**Files:**
- Modify: `tools/pasto/common.py` (al final)
- Create: `tools/pasto/tests/test_common.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_common.py
import unittest

from common import estado_select_html, height_rule_html, trust_band_html
from data import ESTADOS_ORDEN


class CommonTest(unittest.TestCase):
    def test_selector_tiene_todos_los_estados_y_label(self):
        html = estado_select_html("hero-estado")
        self.assertIn('<label for="hero-estado"', html)
        for e in ESTADOS_ORDEN:
            self.assertIn(f'value="{e}"', html)

    def test_selector_preselecciona(self):
        self.assertIn('value="Nuevo León" selected', estado_select_html("x", selected="Nuevo León"))

    def test_regla_escala(self):
        html = height_rule_html(35)
        self.assertIn('style="--h:100%"', html)
        self.assertIn('aria-label="Altura de fibra: 35 mm"', html)
        self.assertIn('style="--h:29%"', height_rule_html(10))

    def test_franja_confianza(self):
        html = trust_band_html()
        self.assertIn("menos de 1 hora", html)
        self.assertIn("/politicas#devoluciones", html)
        self.assertNotIn("muestra", html.lower())
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_common -v; cd ../..`
Expected: `ImportError: cannot import name 'estado_select_html'`

- [ ] **Step 3: Implementar al final de `common.py`**

```python
from data import ESTADOS_ORDEN

MAX_MM = 35


def estado_select_html(select_id, *, selected="", label="Envíalo a"):
    opts = "\n".join(
        f'            <option value="{esc(e)}"{" selected" if e == selected else ""}>{esc(e)}</option>' for e in ESTADOS_ORDEN
    )
    return f"""<div class="ship-to">
          <label for="{select_id}" class="ship-to__label">{esc(label)}</label>
          <select class="ship-to__select" id="{select_id}" data-estado-select>
            <option value="">Elige tu estado</option>
{opts}
          </select>
        </div>"""


def height_rule_html(mm):
    pct = round(mm / MAX_MM * 100)
    return (f'<div class="hrule" role="img" aria-label="Altura de fibra: {mm} mm">'
            f'<span class="hrule__fiber" style="--h:{pct}%"></span>'
            f'<span class="hrule__scale" aria-hidden="true"><i>35</i><i>25</i><i>15</i><i>0</i></span></div>')


TRUST = [
    ("Respuesta en menos de 1 hora", "Lun a vie 9 a 18 h, sáb 9 a 14 h"),
    ("Garantía de fábrica", "De 3 a 8 años según el modelo"),
    ("Devoluciones en 7 días", '<a href="/politicas#devoluciones">Ver política</a>'),
    ("Factura CFDI 4.0", "Persona física o moral"),
    ("Desde 2007", "Vivero y showroom en Cd. Madero"),
]


def trust_band_html():
    items = "\n".join(f"      <li><strong>{esc(t)}</strong><span>{d}</span></li>" for t, d in TRUST)
    return f"""<section class="trust" aria-label="Por qué comprar con nosotros">
  <ul class="wrap trust__list">
{items}
  </ul>
</section>"""
```

Nota: `esc` ya existe en `common.py`; `data` ya se importa ahí (`from data import ...`), agregar `ESTADOS_ORDEN` a esa línea en lugar de una segunda importación.

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_common -v; cd ../..`
Expected: `OK` (4 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/pasto/common.py tools/pasto/tests/test_common.py
git commit -m "feat(pasto): selector de estado, regla de altura y franja de confianza"
```

---

### Task 6: Datos de las 11 ciudades

**Files:**
- Create: `tools/pasto/ciudades.py`
- Create: `tools/pasto/tests/test_ciudades.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_ciudades.py
import unittest

from ciudades import CIUDADES
from data import MODELOS, zona_de

SLUGS = {m["slug"] for m in MODELOS}


class CiudadesTest(unittest.TestCase):
    def test_once_ciudades(self):
        self.assertEqual(len(CIUDADES), 11)

    def test_estado_valido_y_zona_esperada(self):
        esperado = {"cdmx": "A", "guadalajara": "A", "queretaro": "A", "san-luis-potosi": "A", "leon": "A",
                    "puebla": "A", "monterrey": "B", "veracruz": "B", "merida": "C", "cancun": "C", "villahermosa": "C"}
        for c in CIUDADES:
            self.assertEqual(zona_de(c["estado"]), esperado[c["slug"]], c["slug"])

    def test_modelos_existen(self):
        for c in CIUDADES:
            self.assertEqual(len(c["modelos"]), 3, c["slug"])
            for slug, razon in c["modelos"]:
                self.assertIn(slug, SLUGS)
                self.assertTrue(razon)

    def test_textos_no_se_repiten(self):
        climas = [c["clima"] for c in CIUDADES]
        self.assertEqual(len(climas), len(set(climas)))
        preguntas = [q for c in CIUDADES for q, _a in c["faqs"]]
        self.assertEqual(len(preguntas), len(set(preguntas)))

    def test_sin_palabras_prohibidas(self):
        texto = str(CIUDADES).lower()
        for palabra in ("oasis", "muestra", "gratis", "pádel", "padel"):
            self.assertNotIn(palabra, texto)
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_ciudades -v; cd ../..`
Expected: `ModuleNotFoundError: No module named 'ciudades'`

- [ ] **Step 3: Crear `tools/pasto/ciudades.py`**

```python
"""Datos de las páginas de envío por ciudad (/pasto-sintetico/envio/<slug>).

Texto propio por ciudad: clima, modelos recomendados y preguntas. No repetir textos entre ciudades.
Los precios se calculan en ciudad.py con data.landed_m2; aquí no se escriben precios.
`estado` usa la misma clave que ESTADO_ZONA en public/js/tienda-pasto.js.
"""

CIUDADES = [
    dict(slug="cdmx", nombre="CDMX", nombre_largo="Ciudad de México", estado="CDMX",
         clima="En la Ciudad de México llueve fuerte de junio a septiembre y en invierno hay mañanas frías. Conviene un pasto con base perforada que drene rápido y fibra que recupere su forma en azoteas y patios.",
         modelos=[("toscana-28", "El más vendido: aguanta el uso diario de patio familiar."),
                  ("toscana-18", "Ligero para azoteas y balcones donde importa el peso."),
                  ("irlanda-25", "Fibra resistente para perros y pisoteo diario.")],
         faqs=[("¿Pueden enviarlo a una azotea en la Ciudad de México?", "Enviamos el rollo a tu dirección por paquetería. Subirlo a la azotea corre por tu cuenta; un rollo completo pesa varias decenas de kilos, así que conviene que estén dos personas al recibirlo."),
               ("¿Aguanta las lluvias de verano en la CDMX?", "Sí. La base es perforada y drena el agua. Para que no se encharque, instálalo sobre una capa de grava fina compactada o sobre un piso con desnivel."),
               ("¿Cuánto tarda en llegar a la Ciudad de México?", "De 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo.")]),
    dict(slug="guadalajara", nombre="Guadalajara", nombre_largo="Guadalajara, Jalisco", estado="Jalisco",
         clima="Guadalajara tiene primaveras muy secas y calurosas y un verano de lluvias intensas. El pasto sintético evita regar en la época de escasez de agua y drena bien en temporada de tormentas.",
         modelos=[("toscana-28", "Equilibrio entre precio, volumen y resistencia para jardín."),
                  ("capri-20", "Alta densidad para patios con mucho uso."),
                  ("viena-30", "Más volumen y aspecto natural para jardines de lucimiento.")],
         faqs=[("¿Conviene pasto sintético en Guadalajara por el agua?", "Sí. No necesita riego, solo un enjuague ocasional para quitar polvo. En primavera, cuando el pasto natural sufre, el sintético se mantiene verde."),
               ("¿Envían a Zapopan y Tlaquepaque?", "Sí. Enviamos a toda la zona metropolitana de Guadalajara con el flete de Jalisco."),
               ("¿Qué base necesito en Guadalajara?", "Grava fina o polvo de piedra compactado, de 5 a 8 cm, para que drene en la temporada de lluvias.")]),
    dict(slug="queretaro", nombre="Querétaro", nombre_largo="Querétaro", estado="Querétaro",
         clima="Querétaro es seco la mayor parte del año, con polvo y sol fuerte. El pasto sintético se limpia con una barrida o un enjuague y no se amarilla en la temporada seca.",
         modelos=[("toscana-18", "Económico y fácil de limpiar para patios de casa nueva."),
                  ("toscana-28", "Más volumen para jardines de fraccionamiento."),
                  ("irlanda-25", "Fibra resistente si tienes perros.")],
         faqs=[("¿El polvo de Querétaro ensucia el pasto sintético?", "Se acumula como en cualquier piso exterior. Se quita con escoba de cerdas duras o con un enjuague con manguera."),
               ("¿Sirve para casas nuevas en Querétaro?", "Sí. En casas nuevas el terreno suele ser de relleno: compáctalo y pon una capa de grava fina antes de extender el rollo."),
               ("¿Cuánto tarda en llegar a Querétaro?", "De 3 a 5 días hábiles después de confirmar el pago.")]),
    dict(slug="san-luis-potosi", nombre="San Luis Potosí", nombre_largo="San Luis Potosí", estado="San Luis Potosí",
         clima="San Luis Potosí es semiárido: poca lluvia, sol intenso y noches frescas. Un pasto con protección UV conserva su color y no necesita agua.",
         modelos=[("toscana-28", "El más vendido para jardín familiar."),
                  ("toscana-18", "Opción económica para patios chicos."),
                  ("japones-35", "Máximo volumen para jardines de lucimiento.")],
         faqs=[("¿Se decolora con el sol de San Luis Potosí?", "Todos los modelos tienen protección UV de fábrica para conservar el color. La garantía de fábrica va de 3 a 8 años según el modelo."),
               ("¿Envían a Soledad de Graciano Sánchez?", "Sí, con el mismo flete de San Luis Potosí."),
               ("¿Lo puedo poner sobre tierra?", "Sobre tierra compactada con una capa de grava fina, sí. Sobre tierra suelta se hunde y se hacen charcos.")]),
    dict(slug="leon", nombre="León", nombre_largo="León, Guanajuato", estado="Guanajuato",
         clima="León tiene calor seco en primavera y lluvias en verano. El pasto sintético ahorra agua en los meses secos y drena en temporada de lluvias.",
         modelos=[("toscana-28", "Resistente y con buen volumen para jardín."),
                  ("capri-20", "Denso para patios de juego de niños."),
                  ("toscana-18", "Económico para terrazas y áreas chicas.")],
         faqs=[("¿Envían a otras ciudades de Guanajuato?", "Sí. Enviamos a todo Guanajuato, incluidos Irapuato, Celaya y Silao, con el flete de la zona."),
               ("¿Es seguro para niños?", "Sí. Todos los modelos tienen tratamiento antibacterial y retardante al fuego de fábrica."),
               ("¿Cuánto tarda en llegar a León?", "De 3 a 5 días hábiles después de confirmar el pago.")]),
    dict(slug="puebla", nombre="Puebla", nombre_largo="Puebla", estado="Puebla",
         clima="Puebla es templada, con lluvias de mayo a octubre y mañanas frías en invierno. Conviene un pasto con base que drene y fibra que se vea natural todo el año.",
         modelos=[("toscana-28", "El más vendido para jardines de casa."),
                  ("viena-30", "Aspecto natural premium para jardín frontal."),
                  ("toscana-18", "Ligero para balcones y terrazas.")],
         faqs=[("¿Aguanta las heladas de invierno en Puebla?", "Sí. El pasto sintético no se quema con el frío como el pasto natural y conserva su color."),
               ("¿Envían a Cholula y Atlixco?", "Sí, con el mismo flete de Puebla."),
               ("¿Cuánto tarda en llegar a Puebla?", "De 3 a 5 días hábiles después de confirmar el pago.")]),
    dict(slug="monterrey", nombre="Monterrey", nombre_largo="Monterrey, Nuevo León", estado="Nuevo León",
         clima="Monterrey tiene veranos de calor extremo y temporadas de restricción de agua. El pasto sintético no se seca ni necesita riego; en pleno sol conviene una fibra densa que recupere su forma.",
         modelos=[("irlanda-25", "Fibra resistente para calor y uso diario."),
                  ("toscana-28", "El más vendido: buen volumen y precio."),
                  ("bali-35", "El más completo para jardines de lucimiento.")],
         faqs=[("¿El pasto sintético se calienta con el sol de Monterrey?", "Sí, como cualquier superficie al sol. Un enjuague con manguera antes de usarlo en las horas de más calor baja su temperatura."),
               ("¿Envían a San Pedro, Apodaca y Santa Catarina?", "Sí. Enviamos a toda la zona metropolitana de Monterrey con el flete de Nuevo León."),
               ("¿Conviene en Monterrey por la falta de agua?", "Sí. No necesita riego ni poda, y se mantiene verde en la temporada seca.")]),
    dict(slug="veracruz", nombre="Veracruz", nombre_largo="Veracruz y Boca del Río", estado="Veracruz",
         clima="En Veracruz y Boca del Río hay humedad, salitre y nortes. Conviene un pasto con base perforada que drene rápido y una instalación bien fijada en las orillas para que el viento no la levante.",
         modelos=[("toscana-28", "Resistente para jardines de casa en la costa."),
                  ("capri-20", "Alta densidad para patios con mucho uso."),
                  ("irlanda-25", "Fibra resistente para perros.")],
         faqs=[("¿El salitre daña el pasto sintético?", "No lo pudre como a la madera. Un enjuague con agua dulce de vez en cuando quita la sal acumulada."),
               ("¿Se levanta con los nortes?", "Si las orillas quedan bien fijadas con clavos o adhesivo, no. En la guía de instalación explicamos cómo fijarlas."),
               ("¿Envían a Boca del Río y Xalapa?", "Sí. Enviamos a todo el estado de Veracruz con el flete de la zona.")]),
    dict(slug="merida", nombre="Mérida", nombre_largo="Mérida, Yucatán", estado="Yucatán",
         clima="Mérida tiene calor todo el año, suelo de roca caliza y lluvias fuertes en verano. Sobre piedra, el pasto sintético da un jardín verde sin tierra ni riego; la base debe nivelarse con polvo de piedra para que drene.",
         modelos=[("toscana-28", "El más vendido para patios y jardines."),
                  ("irlanda-25", "Fibra resistente al uso diario y al calor."),
                  ("viena-30", "Más volumen para jardines de lucimiento.")],
         faqs=[("¿Se puede poner pasto sintético sobre el suelo de piedra de Mérida?", "Sí. Nivela con polvo de piedra o grava fina, compacta y extiende el rollo encima. Es una de las ventajas frente al pasto natural."),
               ("¿Aguanta las lluvias de verano en Mérida?", "Sí. La base perforada drena el agua si la base de grava tiene desnivel hacia una salida."),
               ("¿Cuánto tarda en llegar a Mérida?", "De 3 a 5 días hábiles después de confirmar el pago, según la paquetería.")]),
    dict(slug="cancun", nombre="Cancún", nombre_largo="Cancún, Quintana Roo", estado="Quintana Roo",
         clima="Cancún tiene sol intenso, arena, salitre y temporada de huracanes. El pasto sintético con protección UV se mantiene verde junto a albercas y terrazas, y se enjuaga para quitar arena y sal.",
         modelos=[("toscana-28", "Para jardines y áreas de alberca."),
                  ("capri-20", "Denso y resistente para rentas vacacionales con mucho uso."),
                  ("toscana-18", "Ligero para terrazas y roof gardens.")],
         faqs=[("¿Sirve alrededor de la alberca?", "Sí. Drena el agua y no se hace lodo. Enjuágalo de vez en cuando para quitar cloro, arena y sal."),
               ("¿Envían a Playa del Carmen y Tulum?", "Sí. Enviamos a todo Quintana Roo con el flete de la zona; en poblaciones alejadas el flete puede variar y te lo confirmamos."),
               ("¿Qué hago en temporada de huracanes?", "Revisa que las orillas estén bien fijadas. Si el agua arrastra arena o ramas, límpialo con escoba y enjuágalo.")]),
    dict(slug="villahermosa", nombre="Villahermosa", nombre_largo="Villahermosa, Tabasco", estado="Tabasco",
         clima="Villahermosa tiene calor húmedo y lluvias muy intensas buena parte del año. Lo más importante es la base: grava con desnivel para que el agua salga rápido y el pasto no se quede encharcado.",
         modelos=[("toscana-28", "Resistente para jardines con lluvias frecuentes."),
                  ("irlanda-25", "Fibra resistente para perros y uso diario."),
                  ("capri-20", "Alta densidad para patios con mucho paso.")],
         faqs=[("¿Se encharca con las lluvias de Tabasco?", "El pasto drena, pero si el terreno no tiene salida el agua se queda abajo. Por eso la base de grava con desnivel es clave."),
               ("¿Le salen hongos con la humedad?", "El pasto sintético no genera hongos como el natural. Si se acumula materia orgánica, enjuágalo y cepíllalo."),
               ("¿Cuánto tarda en llegar a Villahermosa?", "De 3 a 5 días hábiles después de confirmar el pago.")]),
]
```

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_ciudades -v; cd ../..`
Expected: `OK` (5 tests). Si falla `test_sin_palabras_prohibidas` o `test_textos_no_se_repiten`, corregir el texto, no la prueba.

- [ ] **Step 5: Commit**

```bash
git add tools/pasto/ciudades.py tools/pasto/tests/test_ciudades.py
git commit -m "feat(pasto): datos de 11 ciudades con clima, modelos y preguntas propias"
```

---

### Task 7: Plantilla de página de ciudad

**Files:**
- Create: `tools/pasto/ciudad.py`
- Create: `tools/pasto/tests/test_ciudad.py`
- Modify: `tools/pasto/build.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_ciudad.py
import json
import re
import unittest

from ciudad import build_ciudad, totales
from ciudades import CIUDADES
from data import MODELOS

MTY = next(c for c in CIUDADES if c["slug"] == "monterrey")


class CiudadTest(unittest.TestCase):
    def test_totales_monterrey_aruba(self):
        aruba = next(m for m in MODELOS if m["slug"] == "aruba-10")
        # 25 m² a precio t2 ($159) + 1 rollo de flete B ($1,150); 50 m² rollo ($139) + 1 flete; 100 m² + 2 fletes
        self.assertEqual(totales(aruba, "B"), [(25, 25 * 159 + 1150), (50, 50 * 139 + 1150), (100, 100 * 139 + 2300)])

    def test_html_basico(self):
        html = build_ciudad(MTY)
        self.assertIn("<h1", html)
        self.assertIn("Monterrey", html)
        self.assertIn("$162", html)
        self.assertIn("/pasto-sintetico?estado=nuevo-leon", html)
        self.assertIn('rel="canonical" href="https://www.viverosterra.com/pasto-sintetico/envio/monterrey"', html)

    def test_jsonld_valido(self):
        html = build_ciudad(MTY)
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(bloque)
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_ciudad -v; cd ../..`
Expected: `ModuleNotFoundError: No module named 'ciudad'`

- [ ] **Step 3: Crear `tools/pasto/ciudad.py`**

```python
"""Página /pasto-sintetico/envio/<slug>: pasto sintético con envío a una ciudad."""
from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, faq_html, faq_schema,
                    footer, head, height_rule_html, jsonld, section_open, trust_band_html, wa)
from data import MODELOS, SITE, ZONA_ESTADOS, ZONAS, estado_slug, landed_m2, zona_de

MIN_NACIONAL = 25
ROLLO = 50


def modelo(slug):
    return next(m for m in MODELOS if m["slug"] == slug)


def totales(m, zona):
    """Material + flete para 25, 50 y 100 m² (mismas reglas del cotizador: 25 m² usa precio t2)."""
    out = []
    for m2 in (MIN_NACIONAL, ROLLO, ROLLO * 2):
        precio = m["rollo"] if m2 >= ROLLO else m["t2"]
        rollos = -(-m2 // ROLLO)
        out.append((m2, m2 * precio + rollos * ZONAS[zona]))
    return out


def barato():
    return min(MODELOS, key=lambda m: m["rollo"])


def hero_html(c, zona):
    desde = landed_m2(barato(), zona)
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Envío a {esc(c["nombre_largo"])}</span><span class="stock">9 modelos en existencia</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético en {esc(c["nombre"])} <em>con envío a tu casa</em></h1>
        <p class="summary summary--hero">Te enviamos el pasto sintético a {esc(c["nombre_largo"])} en 3 a 5 días hábiles. Desde <strong>${desde}/m²</strong> ya con envío, en rollo de 50 m² con factura. Tú lo instalas con nuestra guía.</p>
        <dl class="specstrip">
          <div><dt>Puesto en {esc(c["nombre"])}</dt><dd class="num"><small>desde</small> ${desde}<small>/m²</small></dd></div>
          <div><dt>Flete por rollo</dt><dd class="num">${ZONAS[zona]:,}</dd></div>
          <div><dt>Entrega</dt><dd class="num">3–5<small>días</small></dd></div>
          <div><dt>Compra mínima</dt><dd class="num">25<small>m²</small></dd></div>
        </dl>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="/pasto-sintetico?estado={estado_slug(c["estado"])}#modelos">Ver los 9 modelos con precio puesto</a>
          <a class="btn btn--ghost" href="{wa(f"Hola, quiero cotizar pasto sintético con envío a {c['nombre']}. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="{GAL}/obra-proyecto-02-sm.webp" srcset="{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w" sizes="(min-width: 1024px) 560px, 100vw" width="960" height="1280" alt="Jardín residencial con pasto sintético de nuestra colección" fetchpriority="high" decoding="async">
        <figcaption>Pasto sintético de nuestra colección instalado.</figcaption>
      </figure>
    </div>
  </section>"""


def totales_html(zona):
    m = barato()
    rows = "\n".join(
        f'            <tr><th scope="row">{m2} m²</th><td>${total:,}</td><td>${round(total / m2)}/m²</td></tr>'
        for m2, total in totales(m, zona)
    )
    return f"""<p class="section__intro">Ejemplo con {esc(m["nombre"])}, el modelo más económico. Material más flete, IVA incluido.</p>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Totales de ejemplo con envío">
          <table class="compare-table compare-table--compact num">
            <thead><tr><th scope="col">Metros</th><th scope="col">Total con envío</th><th scope="col">Por m²</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="spec-note">El flete exacto se confirma con tu código postal antes de pagar.</p>"""


def modelos_html(c, zona):
    cards = []
    for slug, razon in c["modelos"]:
        m = modelo(slug)
        cards.append(f"""          <article class="city-model">
            {height_rule_html(m["mm"])}
            <div>
              <h3><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a> <span class="num">{m["mm"]} mm</span></h3>
              <p>{esc(razon)}</p>
              <p class="city-model__price num">Desde <strong>${landed_m2(m, zona)}</strong>/m² puesto en {esc(c["nombre"])}</p>
            </div>
          </article>""")
    return f"""<p class="section__intro">{esc(c["clima"])}</p>
        <div class="city-models">
{chr(10).join(cards)}
        </div>"""


def llegada_html():
    return """<ol class="steps">
          <li><h3>Confirmas y pagas</h3><p>Transferencia o link de pago con tarjeta. Factura CFDI 4.0.</p></li>
          <li><h3>Sale en rollo</h3><p>Rollo de 2 m de ancho, enrollado y protegido, con guía de rastreo.</p></li>
          <li><h3>Revisa al recibir</h3><p>Que el empaque venga completo y que los metros coincidan con tu pedido. Si algo no está bien, avísanos por WhatsApp con fotos.</p></li>
        </ol>"""


def diy_html():
    return """<p class="section__intro">Un patio de 25 a 50 m² se instala en un día con dos personas. Te mandamos la guía con el pedido.</p>
        <p class="spec-note">La instalación profesional es solo en Tampico, Ciudad Madero y Altamira. <a href="/blog/como-instalar-pasto-sintetico">Ver la guía de instalación paso a paso</a>.</p>"""


def schema(c, zona, url, faqs):
    m = barato()
    offer = {
        "@type": "Offer", "name": f"Pasto sintético con envío a {c['nombre_largo']}", "priceCurrency": "MXN",
        "price": str(m["rollo"]), "availability": "https://schema.org/InStock", "url": url,
        "shippingDetails": {
            "@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": str(ZONAS[zona]), "currency": "MXN"},
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX", "addressRegion": c["estado"]},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                             "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
        },
    }
    return jsonld([
        breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), (f"Envío a {c['nombre']}", url)]),
        offer, faq_schema(faqs),
    ])


def build_ciudad(c):
    zona = zona_de(c["estado"])
    url = f"{SITE}/pasto-sintetico/envio/{c['slug']}"
    faqs = [(q, a, esc(a)) for q, a in c["faqs"]]
    desde = landed_m2(barato(), zona)
    base = head(
        title=f"Pasto sintético en {c['nombre']} con envío · desde ${desde}/m² | Viveros Terra",
        description=f"Pasto sintético con envío a {c['nombre_largo']} desde ${desde}/m² puesto en tu casa. 9 modelos de 10 a 35 mm, entrega en 3 a 5 días hábiles y factura.",
        canonical=url, og_image=f"{SITE}{GAL}/obra-proyecto-02.webp", og_type="website",
        preload_img=f"{GAL}/obra-proyecto-02-sm.webp", preload_srcset=f"{GAL}/obra-proyecto-02-sm.webp 560w, {GAL}/obra-proyecto-02.webp 960w",
        ld=schema(c, zona, url, faqs),
    )
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#modelos">Ir a los modelos</a>'), f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li><a href="/pasto-sintetico">Pasto sintético</a></li>
        <li aria-current="page">Envío a {esc(c["nombre"])}</li>
      </ol>
    </nav>
  </div>
  {hero_html(c, zona)}
  {trust_band_html()}

  {section_open(1, "Precios", "totales-titulo", f"Cuánto cuesta con envío <em>a {esc(c['nombre'])}</em>", section_id="precios")}
        {totales_html(zona)}{SECTION_CLOSE}
  {section_open(2, "Clima", "modelos-titulo", f"El pasto que conviene <em>en {esc(c['nombre'])}</em>", tint=True, section_id="modelos")}
        {modelos_html(c, zona)}{SECTION_CLOSE}
  {section_open(3, "Envío", "llegada-titulo", "Cómo te llega <em>el pedido</em>", section_id="envio")}
        {llegada_html()}{SECTION_CLOSE}
  {section_open(4, "Instálalo tú", "diy-titulo", "Instalarlo tú mismo <em>es sencillo</em>", tint=True, section_id="instalacion")}
        {diy_html()}{SECTION_CLOSE}
  {section_open(5, "Preguntas", "faq-titulo", f"Preguntas frecuentes <em>en {esc(c['nombre'])}</em>", section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  <section class="closing" aria-labelledby="cierre">
    <div class="wrap">
      <h2 id="cierre">Cotiza tu pedido <em>a {esc(c["nombre"])}</em></h2>
      <p>Elige modelo y metros en la tienda: el precio ya incluye el envío a {esc(c["nombre_largo"])}. Te respondemos por WhatsApp en menos de 1 hora en horario.</p>
      <div class="closing__actions">
        <a class="btn btn--light" href="/pasto-sintetico?estado={estado_slug(c["estado"])}#cotizador">Calcular mi pedido</a>
        <a class="btn btn--ghost" href="{wa(f"Hola, quiero cotizar pasto sintético con envío a {c['nombre']}. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
      </div>
    </div>
  </section>
</main>
""", footer(), buybar(f"Envío a {c['nombre']}", f"Desde ${desde}/m² puesto"), drawer_and_toast()])
```

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_ciudad -v; cd ../..`
Expected: `OK` (3 tests)

- [ ] **Step 5: Escribir las páginas en `build.py`.** Agregar el import y el bucle dentro de `main()`:

```python
from ciudad import build_ciudad
from ciudades import CIUDADES
```

```python
    for c in CIUDADES:
        write(ROOT / "envio" / c["slug"] / "index.html", build_ciudad(c))
```

Run: `python3 tools/pasto/build.py | grep envio`
Expected: 11 líneas `ok pasto-sintetico/envio/<slug>/index.html`

- [ ] **Step 6: Commit**

```bash
git add tools/pasto/ciudad.py tools/pasto/tests/test_ciudad.py tools/pasto/build.py public/pasto-sintetico/envio
git commit -m "feat(pasto): 11 páginas de envío por ciudad con precio puesto"
```

---

### Task 8: Página de pasto sintético para perros

**Files:**
- Create: `tools/pasto/perros.py`
- Create: `tools/pasto/tests/test_perros.py`
- Modify: `tools/pasto/build.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_perros.py
import json
import re
import unittest

from perros import FAQS, RECOMENDADOS, build_perros
from data import MODELOS


class PerrosTest(unittest.TestCase):
    def test_recomendados_existen(self):
        slugs = {m["slug"] for m in MODELOS}
        self.assertEqual(len(RECOMENDADOS), 3)
        for slug, _r in RECOMENDADOS:
            self.assertIn(slug, slugs)

    def test_preguntas_clave(self):
        preguntas = " ".join(q for q, _a in FAQS).lower()
        for palabra in ("calienta", "rasguñ", "huele", "lava"):
            self.assertIn(palabra, preguntas)

    def test_html_y_schema(self):
        html = build_perros()
        self.assertIn('rel="canonical" href="https://www.viverosterra.com/pasto-sintetico/perros"', html)
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(bloque)
        self.assertNotIn("muestra", html.lower())
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_perros -v; cd ../..`
Expected: `ModuleNotFoundError: No module named 'perros'`

- [ ] **Step 3: Crear `tools/pasto/perros.py`**

```python
"""Página /pasto-sintetico/perros: pasto sintético para perros y mascotas.

Solo afirmaciones presentes en las fichas (COMMON_TREATMENTS incluye antibacterial). Sin prometer lo que no está documentado.
"""
from common import (GAL, SECTION_CLOSE, breadcrumb_schema, buybar, drawer_and_toast, esc, faq_html, faq_schema,
                    footer, head, height_rule_html, jsonld, section_open, trust_band_html, wa)
from data import COMMON_TREATMENTS, MODELOS, SITE

URL = f"{SITE}/pasto-sintetico/perros"

RECOMENDADOS = [
    ("irlanda-25", "Fibra más resistente de la colección: aguanta pisoteo y juego diario."),
    ("capri-20", "Alta densidad y fibra corta: fácil de limpiar y de levantar desechos."),
    ("toscana-18", "El más económico para patios chicos o para empezar."),
]

CRITERIOS = [
    ("Fibra resistente y no muy alta", "De 18 a 25 mm es lo más práctico: se limpia fácil y la fibra se recupera con el paso de las patas."),
    ("Base perforada que drene", "La orina tiene que pasar al suelo. Instálalo sobre grava fina compactada, no sobre piso liso sin desnivel."),
    ("Limpieza sencilla", "Levanta los desechos sólidos y enjuaga con manguera. Para el olor, usa un limpiador enzimático para mascotas."),
]

FAQS = [
    ("¿El pasto sintético se calienta con el sol?", "Sí, como cualquier superficie exterior al sol. Enjuágalo con manguera en las horas de más calor y deja una zona de sombra para tu perro."),
    ("¿Mi perro lo puede rasguñar o romper?", "Un perro que escarba puede levantar las orillas si no están bien fijadas. Fija el perímetro con clavos o adhesivo como indica la guía de instalación."),
    ("¿El pasto sintético huele a orina?", "Si la base no drena o no se enjuaga, sí. Con grava que drene, enjuague frecuente y un limpiador enzimático no se queda el olor."),
    ("¿Cómo se lava el pasto sintético con perros?", "Levanta los desechos, enjuaga con manguera una o dos veces por semana y cepilla la fibra de vez en cuando para que quede de pie."),
    ("¿Es seguro para mascotas?", f"Todos nuestros modelos tienen de fábrica estos tratamientos: {COMMON_TREATMENTS}."),
]


def modelo(slug):
    return next(m for m in MODELOS if m["slug"] == slug)


def recomendados_html():
    cards = []
    for slug, razon in RECOMENDADOS:
        m = modelo(slug)
        cards.append(f"""          <article class="city-model">
            {height_rule_html(m["mm"])}
            <div>
              <h3><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a> <span class="num">{m["mm"]} mm</span></h3>
              <p>{esc(razon)}</p>
              <p class="city-model__price num">Desde <strong>${m["rollo"]}</strong>/m² <span data-landed-slug="{m["slug"]}"></span></p>
            </div>
          </article>""")
    return '<div class="city-models">\n' + "\n".join(cards) + "\n        </div>"


def criterios_html():
    items = "\n".join(f"          <li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in CRITERIOS)
    return f'<ol class="steps">\n{items}\n        </ol>'


def build_perros():
    faqs = [(q, a, esc(a)) for q, a in FAQS]
    ld = jsonld([breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), ("Para perros", URL)]),
                 faq_schema(faqs)])
    img = f"{GAL}/obra-proyecto-04"
    base = head(
        title="Pasto sintético para perros: qué modelo elegir y cómo limpiarlo | Viveros Terra",
        description="Pasto sintético para perros con envío a todo México: qué modelo elegir, cómo drena la orina, cómo quitar el olor y cómo limpiarlo. Desde $149/m².",
        canonical=URL, og_image=f"{SITE}{img}.webp", og_type="article",
        preload_img=f"{img}-sm.webp", preload_srcset=f"{img}-sm.webp 560w, {img}.webp 960w", ld=ld,
    )
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#elegir">Ir al contenido</a>'), f"""
<main>
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta de navegación">
      <ol>
        <li><a href="/">Inicio</a></li>
        <li><a href="/pasto-sintetico">Pasto sintético</a></li>
        <li aria-current="page">Para perros</li>
      </ol>
    </nav>
  </div>
  <section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Mascotas · Envío a todo México</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético para perros <em>que drena y se limpia fácil</em></h1>
        <p class="summary summary--hero">Para perros conviene un pasto de 18 a 25 mm con fibra resistente, instalado sobre grava que drene. Se limpia con manguera y un limpiador enzimático. Desde <strong>$149/m²</strong> con Toscana 18.</p>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="/pasto-sintetico#modelos">Ver precios con envío</a>
          <a class="btn btn--ghost" href="{wa("Hola, quiero pasto sintético para mis perros. Metros aprox.: ")}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <img src="{img}-sm.webp" srcset="{img}-sm.webp 560w, {img}.webp 960w" sizes="(min-width: 1024px) 560px, 100vw" width="960" height="1280" alt="Patio con pasto sintético de nuestra colección" fetchpriority="high" decoding="async">
        <figcaption>Pasto sintético de nuestra colección instalado.</figcaption>
      </figure>
    </div>
  </section>
  {trust_band_html()}

  {section_open(1, "Elegir", "elegir-titulo", "Qué pasto sintético <em>conviene para perros</em>", section_id="elegir")}
        {criterios_html()}{SECTION_CLOSE}
  {section_open(2, "Modelos", "modelos-titulo", "Tres modelos <em>para mascotas</em>", tint=True, section_id="modelos")}
        {recomendados_html()}{SECTION_CLOSE}
  {section_open(3, "Preguntas", "faq-titulo", "Preguntas frecuentes <em>con perros</em>", section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
</main>
""", footer(), buybar("Pasto para perros", "Desde $149/m²"), drawer_and_toast()])
```

Nota: si `obra-proyecto-04` no existe en `/img/pasto-sintetico/galeria/`, usar `obra-proyecto-05` (verificar con `ls public/img/pasto-sintetico/galeria/ | grep obra`), y ajustar `width/height` a los de la imagen real (`python3 -c "from PIL import Image;print(Image.open('public/img/pasto-sintetico/galeria/obra-proyecto-04.webp').size)"`).

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_perros -v; cd ../..`
Expected: `OK` (3 tests)

- [ ] **Step 5: Escribir en `build.py`**

```python
from perros import build_perros
```

```python
    write(ROOT / "perros" / "index.html", build_perros())
```

Run: `python3 tools/pasto/build.py | grep perros`
Expected: `ok pasto-sintetico/perros/index.html`

- [ ] **Step 6: Commit**

```bash
git add tools/pasto/perros.py tools/pasto/tests/test_perros.py tools/pasto/build.py public/pasto-sintetico/perros
git commit -m "feat(pasto): página de pasto sintético para perros"
```

---

### Task 9: Tienda — portada con precio puesto, franja, tarjetas con regla, ciudades y comparador

**Files:**
- Modify: `tools/pasto/hub.py` (`hero_html`, `card_html`, `build_hub`; nuevas `ciudades_html`, `comparador_html`)
- Create: `tools/pasto/tests/test_hub.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_hub.py
import unittest

from hub import build_hub


class HubTest(unittest.TestCase):
    def setUp(self):
        self.html = build_hub()

    def test_selector_de_portada(self):
        self.assertIn('id="hero-estado"', self.html)
        self.assertIn('data-landed-hero', self.html)

    def test_existencia_nacional(self):
        self.assertIn("9 modelos en existencia", self.html)
        self.assertNotIn("3 modelos en existencia", self.html)

    def test_reglas_y_precios_puestos(self):
        self.assertEqual(self.html.count('class="hrule"'), 9)
        self.assertEqual(self.html.count("data-landed-slug="), 9)

    def test_ciudades_y_comparador(self):
        self.assertIn('/pasto-sintetico/envio/monterrey', self.html)
        self.assertIn('id="comparador"', self.html)
        self.assertIn('/pasto-sintetico/perros', self.html)
        self.assertIn('src="/js/vt-landed.js', self.html)
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_hub -v; cd ../..`
Expected: FAIL en `test_selector_de_portada`

- [ ] **Step 3: Reemplazar `hero_html()` en `hub.py`**

```python
def hero_html():
    barato = min(MODELOS, key=lambda m: m["rollo"])
    return f"""<section class="hub-hero" aria-labelledby="titulo">
    <div class="wrap hub-hero__grid">
      <div class="hub-hero__copy">
        <p class="eyebrow"><span>Tienda · Envío a todo México</span><span class="stock">9 modelos en existencia</span></p>
        <h1 class="hub-hero__title" id="titulo">Pasto sintético con envío a todo México <em>precio puesto en tu puerta</em></h1>
        {estado_select_html("hero-estado")}
        <p class="landed" data-landed-hero data-rollo="{barato['rollo']}" aria-live="polite">
          <span class="landed__from">Desde</span>
          <strong class="landed__price num" data-landed-value>${barato['rollo']}</strong><span class="landed__unit">/m²</span>
          <span class="landed__note" data-landed-note>+ envío desde $900 por rollo. Elige tu estado para ver el precio puesto.</span>
        </p>
        <div class="hub-hero__actions">
          <a class="btn btn--primary" href="#modelos">Ver modelos con este precio</a>
          <a class="btn btn--ghost" href="#cotizador">Calcular mi pedido</a>
        </div>
      </div>
      <figure class="hub-hero__media">
        <picture>
          <source media="(min-width: 1024px)" srcset="{GAL}/obra-residencial-tampico-sm.webp 560w, {GAL}/obra-residencial-tampico.webp 960w" sizes="560px" width="960" height="1440">
          <img src="{GAL}/obra-proyecto-03-sm.webp" srcset="{GAL}/obra-proyecto-03-sm.webp 560w, {GAL}/obra-proyecto-03.webp 960w" sizes="100vw" width="960" height="1280" alt="Residencia con palmas y jardín de pasto sintético instalado" fetchpriority="high" decoding="async">
        </picture>
        <figcaption>Proyecto real con pasto sintético de nuestra colección.</figcaption>
      </figure>
    </div>
  </section>"""
```

Agregar a la importación de `common`: `estado_select_html, height_rule_html, trust_band_html`.

- [ ] **Step 4: Reemplazar `card_html(m)`** (sin etiqueta de existencia por modelo; regla y precio puesto)

```python
def card_html(m):
    gar = f"{str(m['garantia']).replace(' a ', '–')} años" if m["garantia"] else "Consultar"
    url = f"/pasto-sintetico/{m['slug']}"
    return f"""          <article class="spec-card" data-usos="{' '.join(m['usos'])}" id="m-{m['slug']}">
            <a class="spec-card__media" href="{url}" tabindex="-1" aria-hidden="true">
              <img src="{GAL}/{m['slug']}-2-sm.webp" width="420" height="560" alt="" loading="lazy" decoding="async">
              <span class="spec-card__n num">{m['n']:02d}</span>
            </a>
            <div class="spec-card__body">
              <p class="spec-card__tag">{esc(m['tag'])}</p>
              <h3 class="spec-card__name"><a href="{url}">{esc(m['nombre'])}</a></h3>
              {height_rule_html(m['mm'])}
              <dl class="spec-card__specs num"><div><dt>Altura</dt><dd>{m['mm']} mm</dd></div><div><dt>Peso</dt><dd>{m['peso']} g/m²</dd></div><div><dt>Garantía</dt><dd>{gar}</dd></div></dl>
              <div class="spec-card__foot">
                <p class="spec-card__price num">Desde <strong>${m['rollo']}</strong>/m² <span class="spec-card__landed" data-landed-slug="{m['slug']}"></span></p>
                <button class="spec-card__add" type="button" data-add="{m['slug']}" aria-label="Agregar {esc(m['nombre'])} a mi cotización"><svg class="icon" aria-hidden="true"><use href="#i-plus"/></svg><span>Agregar</span></button>
              </div>
            </div>
          </article>"""
```

- [ ] **Step 5: Agregar `ciudades_html()` y `comparador_html()` en `hub.py`**

```python
from ciudades import CIUDADES
from data import landed_m2, zona_de


def ciudades_html():
    barato = min(MODELOS, key=lambda m: m["rollo"])
    cards = "\n".join(
        f'          <a class="city-card" href="/pasto-sintetico/envio/{c["slug"]}"><strong>{esc(c["nombre"])}</strong>'
        f'<span class="num">desde ${landed_m2(barato, zona_de(c["estado"]))}/m² puesto</span><span>3 a 5 días hábiles</span></a>'
        for c in CIUDADES
    )
    return f"""<p class="section__intro">Precio puesto con el modelo más económico, envío incluido. Enviamos a los 32 estados; estas son las ciudades con guía propia.</p>
        <div class="city-grid">
{cards}
        </div>
        <p class="spec-note">¿Tienes perros? Lee <a href="/pasto-sintetico/perros">qué pasto sintético conviene para mascotas</a>.</p>"""


def comparador_html():
    return """<p class="section__intro">Muchas ofertas anuncian "envío gratis", pero el envío ya viene en el precio. Compara el precio por m² final.</p>
        <form class="comparador" id="comparador" novalidate>
          <div class="field"><label for="cmp-total">Total de la otra oferta, con envío</label><input class="select" id="cmp-total" type="number" inputmode="decimal" min="1" placeholder="Ej. 14899"></div>
          <div class="field"><label for="cmp-m2">Metros cuadrados que incluye</label><input class="select" id="cmp-m2" type="number" inputmode="numeric" min="1" placeholder="Ej. 50"></div>
          <p class="comparador__out" id="cmp-out" aria-live="polite">Escribe el total y los metros para comparar con nuestro precio puesto en tu estado.</p>
        </form>"""
```

- [ ] **Step 6: Reordenar secciones en `build_hub()`.** Sustituir el bloque `<main>…</main>` por este orden (mismas llamadas existentes para las secciones que no cambian) y cargar `vt-landed.js` antes de `tienda-hub.js` en `extra`:

```python
             extra=f'<script type="application/json" id="vt-models">{models_json}</script>\n<script src="/js/vt-landed.js?v={ASSET_VERSION}" defer></script>\n<script src="/js/tienda-hub.js?v={ASSET_VERSION}" defer></script>\n'),
```

```python
  {hero_html()}
  {trust_band_html()}

  {section_open(1, "Colección", "modelos-titulo", "Modelos de pasto sintético <em>de 10 a 35 mm</em>", section_id="modelos")}
        {catalog_html()}{SECTION_CLOSE}
  {section_open(2, "Elegir", "elegir-titulo", "¿Qué pasto sintético <em>te conviene?</em>", tint=True, section_id="elegir")}
        {quiz_html()}{SECTION_CLOSE}
  {section_open(3, "Comparar", "comparar-titulo", "¿Viste otro precio? <em>Compáralo aquí</em>", section_id="comparar")}
        {comparador_html()}{SECTION_CLOSE}
  {section_open(4, "Cotizador", "cotizador-titulo", "Precio del pasto sintético <em>con envío a tu estado</em>", tint=True, section_id="cotizador")}
        {cotizador_html()}{SECTION_CLOSE}
  {section_open(5, "Ciudades", "ciudades-titulo", "Envíos a tu ciudad <em>con precio puesto</em>", section_id="ciudades")}
        {ciudades_html()}{SECTION_CLOSE}
  {section_open(6, "Comparativa", "comparativa-titulo", "Comparativa de modelos <em>por altura, peso y precio</em>", tint=True, section_id="comparativa")}
        {compare_table_html()}{SECTION_CLOSE}
  {section_open(7, "Obras", "obras-titulo", "Pasto sintético instalado <em>en casas reales</em>", section_id="obras")}
        {obras_html()}{SECTION_CLOSE}
  {section_open(8, "Tu pedido", "como-funciona-titulo", "Cómo comprar pasto sintético <em>en línea</em>", tint=True, section_id="como-funciona")}
        {steps_list()}{SECTION_CLOSE}
  {section_open(9, "Instálalo tú", "diy-titulo", "Cómo instalar pasto sintético <em>tú mismo</em>", section_id="instalacion")}
        {diy_html()}{SECTION_CLOSE}
  {section_open(10, "Preguntas", "faq-titulo", "Preguntas frecuentes <em>sobre pasto sintético</em>", tint=True, section_id="preguntas")}
        {faq_html(faqs)}{SECTION_CLOSE}
  {local_band_html()}
```

Importar `ASSET_VERSION` desde `data`. La tabla de envío `envio_table_html()` sigue dentro de `cotizador_html()` (no moverla).

- [ ] **Step 7: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_hub -v; cd ../..`
Expected: `OK` (4 tests)

- [ ] **Step 8: Commit**

```bash
git add tools/pasto/hub.py tools/pasto/tests/test_hub.py
git commit -m "feat(tienda): portada con precio puesto, regla de altura, ciudades y comparador"
```

---

### Task 10: Comportamiento en el navegador (`tienda-hub.js`)

**Files:**
- Modify: `public/js/tienda-hub.js` (agregar al final, antes del cierre del IIFE, y llamar desde el listener `vt:ready` existente)

- [ ] **Step 1: Agregar funciones**

```js
  /* ---------- Precio puesto por estado ---------- */
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');

  function landedFor(t, rollo, estado) {
    return window.VTLanded ? window.VTLanded.landedM2(rollo, estado, t.estadoZona, t.zonas) : null;
  }

  function paintLanded(t, estado) {
    const hero = $('[data-landed-hero]');
    if (hero) {
      const rollo = Number(hero.dataset.rollo);
      const v = estado ? landedFor(t, rollo, estado) : null;
      $('[data-landed-value]', hero).textContent = money(v || rollo);
      $('[data-landed-note]', hero).textContent = v
        ? `puesto en ${estado}, envío incluido · llega en 3 a 5 días hábiles`
        : '+ envío desde $900 por rollo. Elige tu estado para ver el precio puesto.';
      hero.classList.remove('is-updating'); void hero.offsetWidth; hero.classList.add('is-updating');
    }
    $$('[data-landed-slug]').forEach((el) => {
      const m = t.models.find((x) => x.slug === el.dataset.landedSlug);
      const v = m && estado ? landedFor(t, m.rollo, estado) : null;
      el.textContent = v ? `· ${money(v)}/m² puesto en ${estado}` : '';
    });
    const sel = $('#hero-estado');
    if (sel && sel.value !== estado) sel.value = estado;
    paintComparador(t, estado);
  }

  function estadoInicial(t) {
    const slug = new URLSearchParams(location.search).get('estado');
    const desdeUrl = slug && window.VTLanded ? window.VTLanded.estadoDesdeSlug(slug, Object.keys(t.estadoZona)) : null;
    return desdeUrl || t.getEstado();
  }

  function initLanded(t) {
    const sel = $('#hero-estado');
    const inicial = estadoInicial(t);
    if (inicial && inicial !== t.getEstado()) t.setEstado(inicial);
    paintLanded(t, inicial);
    if (sel) sel.addEventListener('change', () => t.setEstado(sel.value));
    document.addEventListener('vt:estado', (e) => paintLanded(t, e.detail.estado || ''));
  }

  /* ---------- Comparador ---------- */
  function paintComparador(t, estado) {
    const out = $('#cmp-out');
    if (!out) return;
    const total = Number($('#cmp-total').value);
    const m2 = Number($('#cmp-m2').value);
    if (!(total > 0 && m2 > 0)) {
      out.textContent = 'Escribe el total y los metros para comparar con nuestro precio puesto en tu estado.';
      return;
    }
    const suyo = total / m2;
    const barato = t.models.reduce((a, b) => (a.rollo <= b.rollo ? a : b));
    const nuestro = estado ? landedFor(t, barato.rollo, estado) : null;
    out.textContent = nuestro
      ? `Esa oferta sale en ${money(suyo)}/m². Con nosotros, desde ${money(nuestro)}/m² puesto en ${estado} (${barato.nombre}).`
      : `Esa oferta sale en ${money(suyo)}/m². Elige tu estado arriba para comparar con nuestro precio puesto.`;
  }

  function initComparador(t) {
    ['#cmp-total', '#cmp-m2'].forEach((id) => {
      const el = $(id);
      if (el) el.addEventListener('input', () => paintComparador(t, t.getEstado()));
    });
  }
```

- [ ] **Step 2: Conectar.** En el listener existente de `vt:ready` (o donde se inicializan filtros y quiz), agregar:

```js
    initLanded(window.VTTienda);
    initComparador(window.VTTienda);
```

- [ ] **Step 3: Verificar sintaxis y pruebas**

Run: `node --check public/js/tienda-hub.js && node --test public/js/tests/`
Expected: sin errores; `pass 3`

- [ ] **Step 4: Verificar en el navegador**

Iniciar vista previa (`preview_start` con nombre `viverosterra`, puerto 8899) y abrir `http://localhost:8899/pasto-sintetico?estado=nuevo-leon`.
Comprobar con JS en la página:

```js
[document.querySelector('[data-landed-value]').textContent,
 document.querySelector('#hero-estado').value,
 document.querySelector('#estado').value,
 document.querySelector('[data-landed-slug="aruba-10"]').textContent]
```

Expected: `["$162", "Nuevo León", "Nuevo León", "· $162/m² puesto en Nuevo León"]`.
Cambiar el selector de la portada a `CDMX` y verificar `$157`; a `Yucatán` y verificar `$167`. `read_console_messages` sin errores.

- [ ] **Step 5: Commit**

```bash
git add public/js/tienda-hub.js
git commit -m "feat(tienda): selector de portada, precio puesto en tarjetas y comparador"
```

---

### Task 11: Estilos de los componentes nuevos

**Files:**
- Modify: `public/css/tienda-pasto.css` (al final)
- Modify: `tools/pasto/data.py` (`ASSET_VERSION = "20260930"`)

- [ ] **Step 1: Agregar CSS**

```css
/* ---------- Precio puesto (portada) ---------- */
.ship-to { display: grid; gap: 6px; margin: 22px 0 10px; max-width: 420px; }
.ship-to__label { font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); }
.ship-to__select {
  min-height: 52px; padding: 0 44px 0 16px; border: 1px solid var(--ink); border-radius: 10px; background: var(--paper);
  font: inherit; font-size: 1.125rem; font-weight: 500; color: var(--ink); appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, var(--ink) 50%), linear-gradient(135deg, var(--ink) 50%, transparent 50%);
  background-position: calc(100% - 22px) 50%, calc(100% - 16px) 50%; background-size: 6px 6px; background-repeat: no-repeat;
}
.ship-to__select:focus-visible { outline: 3px solid var(--green); outline-offset: 2px; }
.landed { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 8px; margin: 6px 0 4px; }
.landed__from { font-size: var(--text-sm); color: var(--ink-2); }
.landed__price { font-size: clamp(2.5rem, 8vw, 3.5rem); font-weight: 600; letter-spacing: -0.04em; line-height: 1; }
.landed__unit { font-size: var(--text-lg); color: var(--ink-2); }
.landed__note { flex-basis: 100%; font-size: var(--text-sm); color: var(--muted); }
.landed.is-updating .landed__price { animation: landed-in 220ms cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes landed-in { from { opacity: 0.2; transform: translateY(6px); } to { opacity: 1; transform: none; } }

/* ---------- Regla de altura ---------- */
.hrule { position: relative; display: flex; align-items: flex-end; gap: 6px; height: 44px; margin: 10px 0 6px; }
.hrule__fiber { width: 10px; height: var(--h); background: repeating-linear-gradient(90deg, var(--green) 0 2px, transparent 2px 3px); border-radius: 2px 2px 0 0; }
.hrule__scale { display: flex; flex-direction: column; justify-content: space-between; height: 100%; border-left: 1px solid var(--line); padding-left: 4px; }
.hrule__scale i { font-style: normal; font-size: 0.625rem; line-height: 1; color: var(--muted); font-variant-numeric: tabular-nums; }
.spec-card__landed { display: block; font-size: var(--text-xs); color: var(--green); font-weight: 600; }

/* ---------- Franja de confianza ---------- */
.trust { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); background: var(--paper-2); }
.trust__list { list-style: none; margin: 0; padding: 16px var(--gutter); display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px 18px; }
.trust__list li { display: flex; flex-direction: column; gap: 2px; font-size: var(--text-sm); }
.trust__list span { color: var(--muted); font-size: var(--text-xs); }
@media (min-width: 1024px) { .trust__list { grid-template-columns: repeat(5, 1fr); } }

/* ---------- Comparador ---------- */
.comparador { display: grid; gap: 14px; max-width: 640px; }
@media (min-width: 768px) { .comparador { grid-template-columns: 1fr 1fr; } .comparador__out { grid-column: 1 / -1; } }
.comparador__out { margin: 0; padding: 14px 16px; border-left: 3px solid var(--green); background: var(--paper); font-size: var(--text-lg); }

/* ---------- Ciudades ---------- */
.city-grid { display: grid; gap: 10px; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
.city-card { display: flex; flex-direction: column; gap: 4px; min-height: 44px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; text-decoration: none; color: var(--ink); transition: border-color 150ms ease, transform 150ms ease; }
.city-card:hover { border-color: var(--ink); transform: translateY(-2px); }
.city-card:focus-visible { outline: 3px solid var(--green); outline-offset: 2px; }
.city-card span { font-size: var(--text-xs); color: var(--muted); }
.city-card span.num { color: var(--green); font-weight: 600; font-size: var(--text-sm); }
.city-models { display: grid; gap: 14px; }
.city-model { display: grid; grid-template-columns: 44px 1fr; gap: 14px; padding: 16px 0; border-top: 1px solid var(--line); }
.city-model h3 { margin: 0 0 4px; font-size: 1.125rem; }
.city-model h3 span { font-size: var(--text-sm); color: var(--muted); font-weight: 400; }
.city-model p { margin: 0 0 6px; color: var(--ink-2); }
.city-model__price strong { font-size: 1.125rem; }

@media (prefers-reduced-motion: reduce) {
  .landed.is-updating .landed__price { animation: none; }
  .city-card { transition: none; }
}
```

- [ ] **Step 2: Subir versión de assets y regenerar**

Cambiar en `data.py`: `ASSET_VERSION = "20260930"`.
Run: `python3 tools/pasto/build.py`
Expected: todas las páginas `ok`, sin errores.

- [ ] **Step 3: Revisar visual en 375, 768, 1024 y 1440**

Con el headless shell de Playwright:

```bash
B=$(ls ~/Library/Caches/ms-playwright/chromium_headless_shell-1228/*/chrome-headless-shell | head -1)
for w in 375 768 1024 1440; do "$B" --headless --hide-scrollbars --window-size=$w,2600 --screenshot=/tmp/hub-$w.png "http://localhost:8899/pasto-sintetico?estado=nuevo-leon"; done
```

Expected: sin desplazamiento horizontal; selector de 52 px de alto; precio puesto visible en la primera pantalla a 375; 9 reglas de altura de distinta altura; franja en 2 columnas en celular y 5 en escritorio.

- [ ] **Step 4: Commit**

```bash
git add public/css/tienda-pasto.css tools/pasto/data.py public/pasto-sintetico public/pasto-sintetico-tampico public/precios public/jardineria-*
git commit -m "feat(tienda): estilos de precio puesto, regla de altura, confianza, comparador y ciudades"
```

---

### Task 12: Fichas con existencia nacional y precio puesto

**Files:**
- Modify: `tools/pasto/ficha.py:250` y la zona de precio de `buy_html`
- Create: `tools/pasto/tests/test_ficha.py`

- [ ] **Step 1: Prueba que falla**

```python
# tools/pasto/tests/test_ficha.py
import unittest

from data import MODELOS
from ficha import build_ficha


class FichaTest(unittest.TestCase):
    def test_todas_en_existencia_y_con_precio_puesto(self):
        for m in MODELOS:
            html = build_ficha(m)
            self.assertIn('<span class="stock">En existencia</span>', html, m["slug"])
            self.assertIn(f'data-landed-slug="{m["slug"]}"', html, m["slug"])
            self.assertIn('src="/js/vt-landed.js', html, m["slug"])
```

- [ ] **Step 2: Correr y ver que falla**

Run: `cd tools/pasto && python3 -m unittest tests.test_ficha -v; cd ../..`
Expected: FAIL (Aruba 10 no tiene "En existencia")

- [ ] **Step 3: Implementar**

En `ficha.py:250` reemplazar la línea de `stock` por:

```python
    stock = '<span class="stock">En existencia</span>'
```

En `buy_html(m)`, justo después del bloque `buy__from` (el precio "Desde $X/m²"), agregar:

```python
            <p class="buy__landed" data-landed-slug="{m['slug']}" aria-live="polite"></p>
```

En `build_ficha`, agregar `vt-landed.js` y un pequeño pintor al `extra` de `head(...)`:

```python
extra=(existing_extra + f'<script src="/js/vt-landed.js?v={ASSET_VERSION}" defer></script>\n'
       '<script>document.addEventListener("vt:ready",function(){var t=window.VTTienda,L=window.VTLanded;if(!t||!L)return;'
       'function p(e){document.querySelectorAll("[data-landed-slug]").forEach(function(el){var m=t.models.find(function(x){return x.slug===el.dataset.landedSlug});'
       'var v=m&&e?L.landedM2(m.rollo,e,t.estadoZona,t.zonas):null;el.textContent=v?"$"+v.toLocaleString("es-MX")+"/m² puesto en "+e:"";});}'
       'p(t.getEstado());document.addEventListener("vt:estado",function(ev){p(ev.detail.estado||"")});});</script>\n')
```

(`existing_extra` es el valor actual del argumento `extra` en `build_ficha`; si no existe, usar cadena vacía.) Agregar a CSS: `.buy__landed { margin: 4px 0 0; color: var(--green); font-weight: 600; font-size: var(--text-sm); }`.

- [ ] **Step 4: Correr y ver que pasa**

Run: `cd tools/pasto && python3 -m unittest tests.test_ficha -v; cd ../.. && python3 tools/pasto/build.py >/dev/null`
Expected: `OK`

- [ ] **Step 5: Verificar en navegador** `http://localhost:8899/pasto-sintetico/toscana-28` tras elegir "Nuevo León" en el cotizador de la ficha: el texto bajo el precio muestra `$222/m² puesto en Nuevo León` (199 + 1150/50 = 222).

- [ ] **Step 6: Commit**

```bash
git add tools/pasto/ficha.py tools/pasto/tests/test_ficha.py public/css/tienda-pasto.css public/pasto-sintetico
git commit -m "feat(fichas): existencia nacional y precio puesto por estado"
```

---

### Task 13: Sitemap, llms.txt y guía de precios

**Files:**
- Create: `tools/pasto/sitemap.py`
- Modify: `tools/pasto/build.py`
- Modify: `public/llms.txt`
- Modify: `public/blog/cuanto-cuesta-pasto-sintetico-mexico/index.html`

- [ ] **Step 1: Crear `sitemap.py`**

```python
"""Agrega o actualiza URLs en public/sitemap.xml sin tocar las demás."""
import re
from datetime import date
from pathlib import Path

SITEMAP = Path(__file__).resolve().parents[2] / "public" / "sitemap.xml"


def upsert(urls, lastmod=None):
    lastmod = lastmod or date.today().isoformat()
    xml = SITEMAP.read_text(encoding="utf-8")
    for url in urls:
        entry = re.compile(r"<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>", re.S)
        block = f"<url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>"
        xml = entry.sub(block, xml) if entry.search(xml) else xml.replace("</urlset>", f"  {block}\n</urlset>")
    SITEMAP.write_text(xml, encoding="utf-8")
```

- [ ] **Step 2: Llamarlo desde `build.py` al final de `main()`**

```python
from sitemap import upsert
```

```python
    upsert([f"{SITE}/pasto-sintetico", f"{SITE}/pasto-sintetico/perros"]
           + [f"{SITE}/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
           + [f"{SITE}/pasto-sintetico/{m['slug']}" for m in MODELOS])
```

(Importar `SITE` y `MODELOS` desde `data` si no están.)

Run: `python3 tools/pasto/build.py >/dev/null && xmllint --noout public/sitemap.xml && grep -c "pasto-sintetico/envio/" public/sitemap.xml`
Expected: `11`

- [ ] **Step 3: llms.txt.** Debajo de la línea de "Envío de pasto sintético por rollo de 50 m²…" agregar:

```text
- Pasto sintético con envío por ciudad (precio puesto con Aruba 10): CDMX, Guadalajara, Querétaro, San Luis Potosí, León y Puebla desde $157/m²; Monterrey y Veracruz desde $162/m²; Mérida, Cancún y Villahermosa desde $167/m². https://www.viverosterra.com/pasto-sintetico/envio/monterrey (cambiar la ciudad en la URL)
- Pasto sintético para perros: qué modelo elegir, drenaje, olor y limpieza. https://www.viverosterra.com/pasto-sintetico/perros
```

- [ ] **Step 4: Guía de precios del blog.** En `public/blog/cuanto-cuesta-pasto-sintetico-mexico/index.html`, antes de la sección de preguntas frecuentes, insertar una tabla generada una vez con este script:

```bash
cd tools/pasto && python3 - <<'EOF'
from ciudades import CIUDADES
from data import MODELOS, landed_m2, zona_de
b = min(MODELOS, key=lambda m: m["rollo"])
rows = "\n".join(f'<tr><td><a href="/pasto-sintetico/envio/{c["slug"]}">{c["nombre"]}</a></td><td>${landed_m2(b, zona_de(c["estado"]))}/m²</td></tr>' for c in CIUDADES)
print(f'<h2 id="precio-por-ciudad">Precio del pasto sintético puesto en tu ciudad</h2>\n<p>Precio por m² del modelo más económico con el envío incluido, en rollo de 50 m².</p>\n<table>\n<thead><tr><th>Ciudad</th><th>Desde, con envío</th></tr></thead>\n<tbody>\n{rows}\n</tbody>\n</table>')
EOF
cd ../..
```

Pegar la salida en el artículo, justo antes del encabezado de preguntas frecuentes (buscar `Preguntas frecuentes` en el archivo).

- [ ] **Step 5: Commit**

```bash
git add tools/pasto/sitemap.py tools/pasto/build.py public/sitemap.xml public/llms.txt public/blog/cuanto-cuesta-pasto-sintetico-mexico/index.html
git commit -m "feat(seo): sitemap, llms.txt y guía de precios con las páginas por ciudad"
```

---

### Task 14: Verificación final y publicación

- [ ] **Step 1: Todas las pruebas**

Run: `cd tools/pasto && python3 -m unittest discover -s tests -v; cd ../.. && node --test public/js/tests/`
Expected: todo `OK` / `pass`.

- [ ] **Step 2: JSON-LD válido en todas las páginas generadas**

```bash
python3 - <<'EOF'
import glob, json, re
for f in glob.glob("public/pasto-sintetico/**/index.html", recursive=True):
    t = open(f).read()
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        json.loads(b)
print("ok")
EOF
```

Expected: `ok`

- [ ] **Step 3: Revisión en navegador.** Para `/pasto-sintetico`, `/pasto-sintetico/envio/merida`, `/pasto-sintetico/perros` y `/pasto-sintetico/toscana-28`: sin errores en consola (`read_console_messages` con `onlyErrors`), sin desplazamiento horizontal a 375 px (`document.documentElement.scrollWidth <= 375`), foco visible con teclado en el selector y las tarjetas de ciudad.

- [ ] **Step 4: Publicar**

```bash
git pull --no-rebase
git push
```

Esperar el despliegue y verificar:

```bash
until curl -s https://www.viverosterra.com/pasto-sintetico/envio/monterrey | grep -q "Monterrey"; do sleep 5; done
curl -s -o /dev/null -w "%{http_code}\n" https://www.viverosterra.com/pasto-sintetico/perros
```

Expected: la primera termina; la segunda imprime `200`.

- [ ] **Step 5: Avisar al dueño** con las 13 URLs nuevas para Search Console (11 ciudades, perros y la tienda) y que el feed de Merchant Center no cambió.
