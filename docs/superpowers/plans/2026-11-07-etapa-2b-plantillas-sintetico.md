# Etapa 2b · Plantillas: pasto sintético (tienda, fichas, ciudades, perros, Tampico) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Segundo lote de la Etapa 2 (`docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §10, punto 3; hoja de ruta `docs/superpowers/plans/2026-11-07-etapa-2-hoja-de-ruta.md`, 2b): las 25 páginas de pasto sintético (`/pasto-sintetico-tampico`, el hub `/pasto-sintetico`, las 9 fichas, las 11 ciudades `/pasto-sintetico/envio/*` y `/pasto-sintetico/perros`) pasan del estilo "Libreta" (Geist + Instrument Serif, `tienda-pasto.css`, Google Fonts) al sistema híbrido de 2a (Archivo + Fraunces, etiqueta amarilla, cuadro de datos, pies `FIG.`, NOSOTROS / TÚ / JUNTOS) sin perder nada de lo que funciona: selector de estado con precio puesto, cotizador con lista y mensaje de WhatsApp, forma de pago (contado, 3, 6, 9 y 12 mensualidades con la fórmula oficial), barra de compra, comparador "¿Viste otro precio?", filtros, regla de altura, tablas de las ciudades con su columna de mensualidades, feed de Merchant y sitemap. De paso: `activos.py` deja de decidir por fecha de archivo qué copia con hash conserva (el deploy anterior borró la que servía producción), la mensualidad de Python redondea igual que `Math.round` del JS, lo que se agrega a la lista llega también al WhatsApp del cotizador, la ficha muestra "desde $X/m² · rollo 50 m² · envío por rollo según estado" en el primer pantallazo móvil con la foto principal precargada (nunca `lazy`), y el hub deja de desbordar a 320 px. Se publica en un solo lote (spec §10, lote 2).

**Architecture:** Se sigue la decisión de 2a (plantilla Python + contenido en datos + componentes puros + `generar.PAGINAS`), con **`tools/pasto` como capa de datos y lógica y `tools/site` como única capa de HTML** para la tienda: `tools/pasto/data.py` (modelos, zonas, fletes, `landed_m2`), `ciudades.py` (textos por ciudad), `mensualidades.py` (fórmula), `feed.py` y `sitemap.py` se quedan; los nodos schema.org de la tienda salen de `common.py` a `tools/pasto/esquema.py` (datos, sin HTML); `ficha.py`, `hub.py`, `ciudad.py`, `perros.py` y `local.py` se borran y `common.py` se reduce a lo que aún usan `/precios` y las 6 zonas (se van en 2g). No se migra todo a `tools/site` porque `data.py` es la fuente de modelos y fletes que leen el feed de Merchant, el sitemap, `/precios`, las zonas, las pruebas de paridad JS (`test_paridad_js.py` contra `tienda-pasto.js`) y, desde 2b, las plantillas; moverla rompería todo eso sin ganar nada (spec §5.1 la deja ahí). Lo nuevo: `tools/site/componentes_tienda.py` (cotizador, forma de pago, lista, barra de compra, tarjetas, galería, ficha técnica, rollo a escala, comparativa con 2 vecinos, tablas de envío y de totales) con **el marcado que leen `tienda-pasto.js` y `tienda-hub.js` intacto** (mismos `id`, `data-*` y las clases que el JS crea o busca); tres plantillas nuevas (`ficha`, `tienda_hub`, `tienda_guia` para ciudades y perros) y `servicio` (2a) extendida con opciones, tabla comparativa de precios, cotizador de la tienda y visita al showroom para `/pasto-sintetico-tampico`. Un módulo de contenido puede armar varias páginas (`CLAVES` + `pagina(clave)`, en `PAGINAS` como `"ficha:toscana-28"`), así las 9 fichas y las 11 ciudades salen de los mismos datos sin 20 archivos. **CSS:** `terra.css` ya está en 10.2 KB gzip (el límite era 10 KB): las copias con hash se publican **minificadas sin dependencias** (sin comentarios ni sangría: 8.3 KB gzip) y el presupuesto se mide sobre lo que se transfiere; los componentes de la tienda van a una hoja por tipo de página, **`terra-tienda.css`** (todo bajo `body.vt-tienda`, solo tokens de `terra.css`, < 6 KB gzip, hoy 3.8 KB), que el shell agrega solo a `<body class="vt-pagina vt-tienda">`. Así la home y los servicios no pagan el CSS de la tienda, y cada página de la tienda baja de ~10.5 KB (`tienda-pasto.css`) + Google Fonts a 8.3 + 3.8 KB sin fuentes externas. `tienda-pasto.css` se queda solo para `/precios` y las 6 zonas y se borra en 2g. **JS:** `tienda-pasto.js`, `tienda-hub.js`, `vt-landed.js` y `vt-mensualidades.js` no se reescriben; `tienda-pasto.js` recibe dos cambios chicos con prueba de navegador (botones `data-agregar` de la comparativa y "También en mi lista" en el mensaje del cotizador). **SEO:** título, descripción, robots, canonical, Open Graph y tipos de JSON-LD de las 25 páginas no cambian (paridad); los encabezados se conservan palabra por palabra salvo donde `PARIDAD` dice a dónde fueron; `FAQPage` sale de las preguntas visibles y Tampico gana un `HowTo` de sus 5 pasos.

**Tech Stack:** Python 3.9+ estándar (local 3.9.6) y `unittest`; Playwright para Python 1.48 en las pruebas de navegador (se saltan sin él); CSS plano; JavaScript vanilla con `node --test` (sin `package.json`); Lighthouse 12 con `npx` solo para la verificación manual.

---

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e2b` (rama `feat/etapa-2b`, Tarea 0). Nunca en `~/Documents/GitHub/viverosterra` (iCloud) ni en `~/dev/viverosterra-hdr` (otro agente).
- Commits en español, convencionales: `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`. `git add` siempre con rutas explícitas; nunca `.DS_Store`. Si un build solo cambia `lastmod` de `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml`.
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js`. Las de navegador (`test_navegador.py`, `test_plantillas_navegador.py`, `test_tienda_navegador.py`) corren dentro de la suite de `tools/site` si Playwright está instalado.
- Cuando una tarea cambia una hoja CSS o `terra.js`, el build cambia el hash y reescribe el `<head>` de las páginas que la enlazan: es esperado, se versionan (`git add public`), revisando antes con `git status --short | grep -v '\.html$'` que no haya nada ajeno. También se versiona `tools/site/activos.json` (Tarea 1) cada vez que cambie.
- Reglas del dueño que ninguna línea nueva rompe (las prueban `test_reglas.py` y `test_consistencia.py`): nunca "Oasis"; nunca marcas de proveedor (PastoPlus); nunca el nombre del proveedor de la terminal en `public/`; solo "mensualidades con tarjeta de crédito" (nunca "MSI", "meses sin intereses" ni "sin intereses"); sin pádel ni canchas para sintético; sin muestras físicas ("cómo elegir sin muestra" sí); envío por rollo, nunca gratis ni la palabra "gratis" junto a envío; los 9 modelos en existencia nacional y "para llevar hoy" solo Toscana 18 y 28 en el showroom de Obregón 209 Sur (`data.MODELOS[...]["stock"]`); "Vendemos pasto sintético a todo México desde 2012" (`datos.SINTETICO_NACIONAL_DESDE`); promesa "Respondemos en menos de 1 hora en horario"; anticipo sin porcentaje (`datos.ANTICIPO`); sin fechas de disponibilidad ni "próximo corte"; nunca "visita sin costo"; sin testimonios inventados (el de "Sofía R." de Tampico se retira: no está en `datos.OPINIONES`).
- Dos textos de CTA y nada más en botones de contacto: "Cotizar por WhatsApp" y "Llamar 833 326 8008" (la barra de compra dice "Cotizar", como hoy). Los demás botones son navegación o acciones de la tienda ("Agregar a mi cotización", "Ver los 9 modelos…", "Cómo llegar con Google Maps").
- La fórmula de mensualidades es la de `tools/pasto/mensualidades.py` / `public/js/vt-mensualidades.js`; aquí solo se corrige el redondeo de Python para que sea igual al del JS (Tarea 3).

## Cobertura del spec y qué queda fuera

| Pide el spec / la hoja de ruta | Dónde |
|---|---|
| §3.3 Ficha de tienda: nombre, "En existencia" y etiqueta "desde $X/m² · rollo 50 m² · envío por rollo según estado" en el primer pantallazo → galería precargada → cotizador → para quién → ficha técnica → rollo a escala → comparativa con 2 vecinos → envío por rollo → garantía → FAQ | Tareas 7 y 9; `test_tienda.py` (secuencia) y `test_tienda_navegador.py` (primer pantallazo a 375 × 812, imagen principal no `lazy`) |
| §3.3 Ciudad: respuesta directa (precio puesto y días) → tabla 25/50/100 m² con mensualidad máxima → encabezados en pregunta (costo, tiempo, mínimo, cómo elegir sin muestra, instalación) → modelos → CTA | Tarea 11 |
| §3.3 Servicio local (sintético Tampico): precio ancla, opciones (máx. 3, cada una con su mensaje), proceso en 5 pasos, garantía con condiciones, mensualidades, FAQ | Tarea 12 |
| §4.3 Envío nacional bajo 25 m² bloquea total y mensualidades (J03 §3); fórmula oficial | `tienda-pasto.js` ya lo hace; se prueba en navegador con los casos de J03 §3 (Tarea 14) |
| J01: "Agregar" debe llegar al WhatsApp; "(0)" oculto con la lista vacía | Tareas 7, 8 y 14 |
| J03: LCP de la ficha en una imagen `lazy`; desborde a 320 px | Tareas 7, 9, 10 y 14 |
| Hoja de ruta: corregir `round()` de `mensualidades.py` con prueba | Tarea 3 (casos en `.5` exacto, Python ↔ JS) |
| Hoja de ruta: minificación sin dependencias de la copia con hash para seguir < 10 KB gzip | Tarea 5 |
| Coordinador: `activos.py` conserva la copia que sirve producción, no la de fecha más nueva | Tarea 1 |
| Feed de Merchant sin cambios de precio; sitemap igual | `feed.py` y `sitemap.py` no cambian; `test_tienda.test_feed_de_merchant_sin_cambios_de_precio` |

Fuera de 2b a propósito: `/precios` y las 6 zonas (2g; siguen en `tools/pasto` con `tienda-pasto.css`, que se borra entonces), títulos y descripciones nuevos (Etapa 3), grafo JSON-LD único (Etapa 4), `<script>` en línea del precio puesto a archivo (Etapa 5, con la CSP), fotos reales de la sesión del dueño (solo cambian `src` en el contenido). La meta de Accesibilidad de Lighthouse en este lote es ≥ 95 (≥ 98 al cerrar la Etapa 2).

## File structure

Se crean:

| Archivo | Responsabilidad única |
|---|---|
| `tools/site/activos.json` | Qué copias con hash se conservan por asset: `[actual, la que sirve producción]`. |
| `public/js/tests/casos-mensualidades.json` | Casos de paridad de la mensualidad Python ↔ JS (incluye `.5` exacto). |
| `tools/site/tests/paridad/pasto-sintetico*.json` (23) | Capturas de las páginas de sintético antes de migrar (`/pasto-en-rollo-tampico` y la home ya existen). |
| `tools/pasto/esquema.py` | Nodos schema.org de la tienda (Product, BreadcrumbList, envío, devoluciones, vendedor). |
| `public/css/terra-tienda.css` | Hoja de la tienda (solo en `body.vt-tienda`). |
| `tools/site/componentes_tienda.py` | Componentes de la tienda con el marcado de `tienda-pasto.js` y `tienda-hub.js`. |
| `tools/site/plantillas/ficha.py`, `tienda_hub.py`, `tienda_guia.py` | Plantillas de ficha, hub y guía (ciudades y perros). |
| `tools/site/contenido/ficha.py`, `tienda.py`, `ciudad.py`, `perros.py`, `sintetico_tampico.py` | Contenido (desde `tools/pasto/data.py` y `ciudades.py`) y `PARIDAD`. |
| `tools/site/tests/test_componentes_tienda.py`, `test_terra_tienda_css.py`, `test_tienda.py` | Pruebas de lo anterior. |

Se modifican:

| Archivo | Cambio |
|---|---|
| `tools/site/activos.py`, `tools/site/tests/test_activos.py`, `tools/site/tests/test_sitio.py` | Generaciones por registro, no por fecha (T1); minificación de CSS y `terra-tienda.css` (T5). |
| `tools/site/paridad.py` | `capturar` / `informe` aceptan varias rutas; `informe` usa `generar.cargar`. |
| `tools/pasto/mensualidades.py`, `tools/pasto/tests/test_mensualidades.py`, `public/js/tests/vt-mensualidades.test.js`, `tools/site/componentes.py` | `redondear()` igual a `Math.round`; paridad con los casos compartidos. |
| `tools/site/generar.py`, `tests/test_generar.py`, `tests/test_paridad.py`, `tests/test_contenido.py` | Contenido de varias páginas (`cargar`) y las 23 filas nuevas. |
| `tools/site/partials.py`, `tools/site/shell.py`, `vercel.json`, `tests/test_vercel.py`, `tests/test_terra_css.py` | `terra-tienda.css` en el head de la tienda, caché inmutable, presupuesto sobre la copia publicada. |
| `public/css/terra.css` | `.vt-modos` (formas de contratar) y enlaces legibles dentro del cierre verde. |
| `tools/site/componentes.py` | Etiqueta sin nombre científico opcional; `opciones()`. |
| `public/js/tienda-pasto.js` | `data-agregar` y "También en mi lista" en el mensaje del cotizador. |
| `tools/site/plantillas/base.py`, `tools/site/plantillas/servicio.py` | `head_extra`, `tras_main`, `clase_body`; opciones, tabla comparativa, cotizador, visita y pago sin simulador. |
| `tools/site/paginas.py`, `tests/test_paginas.py` | Ciudades y perros con la barra móvil del shell. |
| `tools/pasto/build.py`, `common.py`, `precios.py`, `zonas.py` y sus pruebas | Ya no generan la tienda; `common.py` reducido. |
| `tools/site/tests/test_tienda_navegador.py`, `tools/site/capturas.py`, `tests/test_reglas.py` | Pruebas de navegador de la tienda; capturas de 13 páginas a 5 anchos; sin la excepción del "envío gratis". |
| `public/pasto-sintetico/**`, `public/pasto-sintetico-tampico/index.html`, ~80 × `public/**/*.html`, `public/css/*.<hash>.css` | Regenerados (25 por plantilla; el resto, solo el hash del CSS). |

Se borran: `tools/pasto/{ficha,hub,ciudad,perros,local}.py` y `tools/pasto/tests/test_{buybar,ciudad,ficha,hub,lineas_pago,perros,common}.py` (sus casos pasan a `test_componentes_tienda.py`, `test_tienda.py` y `test_tienda_navegador.py`).

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Crear el worktree desde `main` actualizado**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git worktree add ~/dev/viverosterra-e2b -b feat/etapa-2b
cd ~/dev/viverosterra-e2b && git log --oneline -1
```

Expected: el último commit de `main` (el que agrega este plan, sobre `2fd51f7 fix: encabezado cabe entre 1100 y 1199 px`).

- [ ] **Step 2: Pruebas y build en verde antes de empezar**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
cd tools/site && python3 -m unittest discover -s tests 2>&1 | grep -E "^Ran|^OK|FAILED"
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK"
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK"
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
python3 -c "import playwright; print('playwright ok')"
grep -o '/css/terra\.[0-9a-f]\{10\}\.css' public/index.html
```

Expected: `plantillas: 0 de 2 páginas escritas` y `shell: 0 de 108 páginas actualizadas`; `0`; `Ran 260 tests` y `OK`; `Ran 59 tests` y `OK`; `Ran 11 tests` y `OK`; `ℹ pass 39` y `ℹ fail 0`; `playwright ok`; `/css/terra.ed57f9f3b4.css`. Si `main` avanzó y el hash es otro, usa el que salga en la Tarea 1 (Step 3).

---

### Task 1: `activos.py` conserva la copia que sirve producción (no la de fecha más nueva)

El deploy de la corrección del encabezado conservó `terra.73fd9d1d2c.css` y borró `terra.3eaa08fd32.css`, la que enlazaba el HTML que producción servía: `publicar()` elegía "la anterior" por `mtime`, y un checkout o un merge cambia esas fechas. Ahora la lista de copias a conservar vive en `tools/site/activos.json` (versionado): mientras la fuente no cambie, el build la respeta tal cual (una segunda corrida no borra nada, ni en CI); cuando la fuente cambia, la nueva pasa a "actual" y la que se conserva es la que enlazan las páginas de `main` (lo que está en producción), aunque en la rama la hoja cambie varias veces. Esta tarea no cambia ninguna página: si el controlador quiere reponer ya `terra.3eaa08fd32.css` en producción, puede llevar este commit solo a `main` (cherry-pick) antes del lote.

**Files:**
- Modify: `tools/site/activos.py`, `tools/site/tests/test_activos.py`, `tools/site/tests/test_sitio.py`
- Create: `tools/site/activos.json`, `public/css/terra.3eaa08fd32.css` (restaurada de git)

- [ ] **Step 1: Escribir las pruebas**

Reemplaza todo `tools/site/tests/test_activos.py` por:

```python
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pub = Path(tmp.name) / "public"
        (self.pub / "css").mkdir(parents=True)
        (self.pub / "js").mkdir()
        (self.pub / "blog").mkdir()
        self.registro = Path(tmp.name) / "activos.json"
        self.escribir(".vt-a{}")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def escribir(self, css):
        (self.pub / "css" / "terra.css").write_text(css, encoding="utf-8")

    def publicar(self):
        return activos.publicar(self.pub, self.registro)

    def copias(self):
        return sorted(p.name for p in (self.pub / "css").glob("terra.*.css"))

    def copia(self, nombre, mtime=1_000_000_000):
        path = self.pub / "css" / nombre
        path.write_text("viejo", encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    def pagina_enlaza(self, nombre):
        """Simula el HTML publicado antes del build (sin git, publicar lo lee de disco)."""
        (self.pub / "index.html").write_text(f'<link rel="stylesheet" href="/css/{nombre}">', encoding="utf-8")

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_la_fuente(self):
        urls = self.publicar()
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}")
        self.assertTrue((self.pub / "css" / "terra.css").exists())

    def test_conserva_la_que_enlazan_las_paginas_aunque_sea_la_mas_vieja(self):
        # El caso del deploy del 2026-11-07: la copia servida tenía el mtime más viejo y se borró.
        servida = self.copia("terra.3eaa08fd32.css", mtime=1_000_000_000)
        reciente = self.copia("terra.73fd9d1d2c.css", mtime=2_000_000_000)
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.assertTrue(servida.exists())
        self.assertFalse(reciente.exists())
        self.assertEqual(self.copias(), sorted([servida.name, Path(urls["terra.css"]).name]))
        self.assertEqual(json.loads(self.registro.read_text(encoding="utf-8"))["terra.css"],
                         [urls["terra.css"], f"/css/{servida.name}"])

    def test_segunda_corrida_no_borra_la_servida(self):
        # Tras la primera corrida las páginas ya enlazan la copia nueva: el registro recuerda la servida.
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.pagina_enlaza(Path(urls["terra.css"]).name)
        registro = self.registro.read_text(encoding="utf-8")
        self.assertEqual(self.publicar(), urls)
        self.assertTrue(servida.exists())
        self.assertEqual(self.registro.read_text(encoding="utf-8"), registro)

    def test_varios_cambios_en_la_rama_siguen_guardando_la_de_produccion(self):
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        self.publicar()
        self.escribir(".vt-b{}")
        segunda = self.publicar()["terra.css"]
        self.escribir(".vt-c{}")
        tercera = self.publicar()["terra.css"]
        self.assertEqual(self.copias(), sorted([servida.name, Path(tercera).name]))
        self.assertFalse((self.pub / segunda.lstrip("/")).exists())

    def test_sin_registro_ni_paginas_deja_solo_la_actual(self):
        self.copia("terra.0000000000.css")
        urls = self.publicar()
        self.assertEqual(self.copias(), [Path(urls["terra.css"]).name])

    def test_no_toca_archivos_que_no_son_copias(self):
        ajeno = self.pub / "css" / "terra.min.css"
        ajeno.write_text("x", encoding="utf-8")
        self.publicar()
        self.assertTrue(ajeno.exists())

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_mismo_contenido_mismo_hash(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.escribir(".vt-a{}")
        self.assertEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_registro_del_repo_coincide_con_lo_publicado(self):
        registro = json.loads(activos.REGISTRO.read_text(encoding="utf-8"))
        urls = activos.urls()
        for clave, rel in activos.FUENTES.items():
            with self.subTest(asset=clave):
                self.assertEqual(registro[clave][0], urls[clave])
                for url in registro[clave]:
                    self.assertTrue((activos.PUBLIC / url.lstrip("/")).is_file(), url)
                copias = {"/" + p.relative_to(activos.PUBLIC).as_posix()
                          for p in (activos.PUBLIC / rel).parent.glob(f"{Path(rel).stem}.*{Path(rel).suffix}")
                          if activos._patron(rel).fullmatch("/" + p.relative_to(activos.PUBLIC).as_posix())}
                self.assertEqual(copias, set(registro[clave]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correrlas y ver que fallan**

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_activos.py 2>&1 | tail -3`
Expected: `TypeError: publicar() takes from 0 to 1 positional arguments but 2 were given` en varias y `FAILED (errors=…)`.

- [ ] **Step 3: Implementar el registro de generaciones**

Reemplaza todo `tools/site/activos.py` por:

```python
"""Copias con hash de los assets del shell, para servirlas con caché inmutable de un año.

La fuente vive sin hash (public/css/terra.css, public/css/legacy-fixes.css, public/js/terra.js) y el build publica
<nombre>.<10 hex>.<ext> al lado. Se conservan dos
copias por asset: la actual y la que sirve producción (la que enlazan las páginas de `main`), para que el HTML que quedó
en caché justo después de un deploy no pida un archivo borrado. Cuáles son se guarda en tools/site/activos.json
({clave: [actual, servida]}), versionado: así el build no depende de fechas de archivo (cambian con cada checkout o
merge) y una segunda corrida no borra nada. Solo al cambiar la fuente se rota: la nueva pasa a "actual" y "servida" se
toma de lo que enlaza `main` (o HEAD, o el HTML en disco si no hay git). Las demás copias con hash se borran.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / "public"
REGISTRO = Path(__file__).resolve().parent / "activos.json"
FUENTES = {
    "terra.css": "css/terra.css",
    "legacy-fixes.css": "css/legacy-fixes.css",
    "terra.js": "js/terra.js",
}


def _con_hash(rel, contenido):
    raiz, ext = rel.rsplit(".", 1)
    return f"{raiz}.{hashlib.sha256(contenido).hexdigest()[:10]}.{ext}"


def _patron(rel):
    raiz, ext = rel.rsplit(".", 1)
    return re.compile(rf"/{re.escape(raiz)}\.[0-9a-f]{{10}}\.{re.escape(ext)}")


def urls(public=PUBLIC):
    """URL pública con hash de cada asset del shell, sin escribir nada."""
    public = Path(public)
    return {clave: "/" + _con_hash(rel, (public / rel).read_bytes()) for clave, rel in FUENTES.items()}


def _html_de_main(public):
    """HTML de la home y del índice del blog (entre los dos enlazan los tres assets) en `main`, en HEAD o, sin git, en
    disco."""
    rutas = ("public/index.html", "public/blog/index.html")
    raiz = Path(public).resolve().parent
    for ref in ("main", "HEAD"):
        try:
            return "".join(subprocess.run(["git", "show", f"{ref}:{r}"], cwd=raiz, capture_output=True, text=True,
                                          check=True).stdout for r in rutas)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return "".join((Path(public) / r.split("/", 1)[1]).read_text(encoding="utf-8")
                   for r in rutas if (Path(public) / r.split("/", 1)[1]).is_file())


def servida(rel, html):
    """Copia con hash de `rel` que enlaza el HTML dado, o None."""
    m = _patron(rel).search(html)
    return m.group(0) if m else None


def generaciones(anteriores, nuevas, html_main):
    """Registro nuevo: sin cambio de fuente se conserva tal cual; con cambio, [nueva, la que sirve main]."""
    salida = {}
    for clave, rel in FUENTES.items():
        previas = anteriores.get(clave, [])
        if previas and previas[0] == nuevas[clave]:
            salida[clave] = previas
            continue
        en_main = servida(rel, html_main)
        salida[clave] = [nuevas[clave]] + ([en_main] if en_main and en_main != nuevas[clave] else [])
    return salida


def publicar(public=PUBLIC, registro=REGISTRO):
    """Escribe la copia actual si falta, borra las que no están en el registro y devuelve las URLs."""
    public, registro = Path(public), Path(registro)
    resultado = urls(public)
    anteriores = json.loads(registro.read_text(encoding="utf-8")) if registro.is_file() else {}
    cambia = any(anteriores.get(c, [None])[0] != u for c, u in resultado.items())
    nuevas = generaciones(anteriores, resultado, _html_de_main(public) if cambia else "")
    for clave, rel in FUENTES.items():
        fuente = public / rel
        destino = public / resultado[clave].lstrip("/")
        conservar = {public / u.lstrip("/") for u in nuevas[clave]}
        patron = re.compile(rf"{re.escape(fuente.stem)}\.[0-9a-f]{{10}}{re.escape(fuente.suffix)}")
        for copia in fuente.parent.glob(f"{fuente.stem}.*{fuente.suffix}"):
            if patron.fullmatch(copia.name) and copia not in conservar:
                copia.unlink()
        if not destino.exists():
            destino.write_bytes(fuente.read_bytes())
    if nuevas != anteriores:
        registro.write_text(json.dumps(nuevas, indent=1) + "\n", encoding="utf-8")
    return resultado
```

Restaura la copia que borró el deploy y escribe el registro con lo que hoy sirve producción (actual) y la copia anterior de cada asset que ya está en el repo:

```bash
cd ~/dev/viverosterra-e2b
git show 0216599^:public/css/terra.3eaa08fd32.css > public/css/terra.3eaa08fd32.css
for f in index.html blog/index.html; do grep -oE '/(css|js)/(terra|legacy-fixes)\.[0-9a-f]{10}\.(css|js)' public/$f; done | sort -u
ls public/css public/js | grep -E '\.[0-9a-f]{10}\.'
```

Expected: `/css/legacy-fixes.6fb87ff99e.css`, `/css/terra.ed57f9f3b4.css`, `/js/terra.fb37c1434f.js`; y en disco `legacy-fixes.6fb87ff99e.css`, `legacy-fixes.9bebda7992.css`, `terra.3eaa08fd32.css`, `terra.73fd9d1d2c.css`, `terra.ed57f9f3b4.css`, `terra.0dbc7510a5.js`, `terra.fb37c1434f.js`. Crea `tools/site/activos.json` (si `main` avanzó, la primera de cada lista es la que salió arriba):

```json
{
 "terra.css": [
  "/css/terra.ed57f9f3b4.css",
  "/css/terra.3eaa08fd32.css"
 ],
 "legacy-fixes.css": [
  "/css/legacy-fixes.6fb87ff99e.css",
  "/css/legacy-fixes.9bebda7992.css"
 ],
 "terra.js": [
  "/js/terra.fb37c1434f.js",
  "/js/terra.0dbc7510a5.js"
 ]
}
```

En `tools/site/tests/test_sitio.py`, cambia el comentario `# activos.publicar() conserva la copia actual y la generación anterior (caché de HTML tras un deploy).` por `# activos.publicar() conserva la copia actual y la que sirve producción (tools/site/activos.json).`

- [ ] **Step 4: Build y pruebas**

```bash
cd ~/dev/viverosterra-e2b && python3 tools/site/build.py | tail -2 && git status --short
cd tools/site && python3 -m unittest tests/test_activos.py tests/test_sitio.py tests/test_vercel.py 2>&1 | tail -1
```

(El build va primero: `test_registro_del_repo_coincide_con_lo_publicado` exige que en disco queden exactamente las copias del registro.) Expected: `plantillas: 0 de 2 …`, `shell: 0 de 108 …`; `OK`; en `git status` solo `D public/css/terra.73fd9d1d2c.css`, ` M tools/site/activos.py`, ` M tools/site/tests/test_activos.py`, ` M tools/site/tests/test_sitio.py`, `?? public/css/terra.3eaa08fd32.css` y `?? tools/site/activos.json` (el registro dice que se conservan `ed57…` y `3eaa…`: la de fecha más nueva, `73fd…`, sale).

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/activos.py tools/site/activos.json tools/site/tests/test_activos.py tools/site/tests/test_sitio.py public/css/terra.3eaa08fd32.css public/css/terra.73fd9d1d2c.css
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(activos): conservar la copia con hash que sirve producción, no la de fecha más nueva" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Capturas de paridad de las 23 páginas de sintético antes de migrar

**Files:**
- Modify: `tools/site/paridad.py`
- Create: `tools/site/tests/paridad/pasto-sintetico*.json` (23)

- [ ] **Step 1: `capturar` e `informe` con varias rutas**

En `tools/site/paridad.py`, reemplaza la función `main` completa por:

```python
def main(argv):
    if len(argv) < 3 or argv[1] not in ("capturar", "informe"):
        raise SystemExit("Uso: python3 tools/site/paridad.py capturar|informe <ruta> [<ruta> …]")
    if argv[1] == "capturar":
        for ruta in argv[2:]:
            print(f"captura: {capturar(ruta).relative_to(AQUI.parents[1])}")
        return
    import generar  # noqa: E402  (solo aquí: generar importa las plantillas)
    for ruta in argv[2:]:
        print(f"== {ruta}")
        modulo = generar.cargar(generar.contenido_de(ruta))
        for categoria, lista in comparar(ruta, modulo.PARIDAD).items():
            print(f"{categoria}: {'ok' if not lista else ''}")
            for item in lista:
                print(f"  - {item}")
```

(`generar.cargar` llega en la Tarea 4; `informe` no se usa antes.) Borra la línea `import importlib` del principio del archivo (ya no se usa).

- [ ] **Step 2: Congelar las 23 páginas tal como están publicadas hoy**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/paridad.py capturar $(python3 -c "
import sys; sys.path[:0] = ['tools/pasto']
from data import MODELOS; from ciudades import CIUDADES
print(' '.join(['/pasto-sintetico-tampico', '/pasto-sintetico', '/pasto-sintetico/perros']
               + ['/pasto-sintetico/' + m['slug'] for m in MODELOS] + ['/pasto-sintetico/envio/' + c['slug'] for c in CIUDADES]))")
ls tools/site/tests/paridad | wc -l
cd tools/site/tests/paridad && python3 -c "
import json, glob
for f in sorted(glob.glob('pasto-sintetico*.json')):
    d = json.load(open(f)); print(f[:-5], len(d['encabezados']), len(d['faq']), len(d['precios']), len(d['enlaces']))"
```

(`$(…)` sin comillas: zsh y bash lo dividen en palabras; una variable `$RUTAS` en zsh no.) Expected: 23 líneas `captura: …`; `25`; y:

```
pasto-sintetico-tampico 19 10 20 12
pasto-sintetico 33 9 20 26
pasto-sintetico_aruba-10 17 7 8 6
pasto-sintetico_bali-35 20 7 8 6
pasto-sintetico_capri-20 20 7 7 6
pasto-sintetico_envio_cancun 13 3 12 7
pasto-sintetico_envio_cdmx 13 3 12 7
pasto-sintetico_envio_guadalajara 13 3 12 7
pasto-sintetico_envio_leon 13 3 12 7
pasto-sintetico_envio_merida 13 3 12 7
pasto-sintetico_envio_monterrey 13 3 12 7
pasto-sintetico_envio_puebla 13 3 12 7
pasto-sintetico_envio_queretaro 13 3 12 7
pasto-sintetico_envio_san-luis-potosi 13 3 12 7
pasto-sintetico_envio_veracruz 13 3 11 7
pasto-sintetico_envio_villahermosa 13 3 11 7
pasto-sintetico_irlanda-25 20 7 7 6
pasto-sintetico_japones-35 17 7 7 6
pasto-sintetico_monaco-35 17 7 7 6
pasto-sintetico_perros 10 5 2 8
pasto-sintetico_toscana-18 20 7 8 6
pasto-sintetico_toscana-28 20 7 8 6
pasto-sintetico_viena-30 20 7 8 7
```

Si un número no coincide, `main` cambió después de escribir este plan: sigue y ajusta en las Tareas 9–12 lo que `paridad.py informe` reporte, nunca la captura. Comprueba que las de Monterrey y Veracruz traen `"$1,666"` (lo corrige la Tarea 3): `grep -c '"\$1,666"' tools/site/tests/paridad/pasto-sintetico_envio_{monterrey,veracruz}.json` → `1` y `1`.

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/paridad.py tools/site/tests/paridad/pasto-sintetico*.json
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(paridad): capturas de las 23 páginas de pasto sintético antes de migrarlas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: La mensualidad de Python redondea como `Math.round` del JS

`round()` de Python lleva los `.5` al par: en 12 mensualidades de $19,998 (100 m² de Aruba 10 a la zona B) la página de Monterrey dice $1,666 y el cotizador, $1,667. Se corrige en `mensualidades.py`, con casos compartidos que corren Python y Node.

**Files:**
- Create: `public/js/tests/casos-mensualidades.json`
- Modify: `tools/pasto/mensualidades.py`, `tools/pasto/tests/test_mensualidades.py`, `public/js/tests/vt-mensualidades.test.js`, `tools/site/componentes.py`

- [ ] **Step 1: Casos compartidos y pruebas**

`public/js/tests/casos-mensualidades.json` (calculados con `vt-mensualidades.js`):

```json
{
 "nota": "Paridad de la mensualidad entre public/js/vt-mensualidades.js y tools/pasto/mensualidades.py: [contado, plazo, total, mensualidad]. Los cuatro primeros caen en .5 exacto (Math.round lo sube; round() de Python lo llevaba al par). Los demás son los casos de J03 §3 y la calculadora del procesador.",
 "casos": [
  [5005, 6, 5751, 959],
  [15014, 12, 18534, 1545],
  [16200, 12, 19998, 1667],
  [2007, 12, 2478, 207],
  [11100, 12, 13702, 1142],
  [10850, 3, 11986, 3995],
  [10850, 6, 12466, 2078],
  [8270, 3, 9136, 3045],
  [8270, 6, 9502, 1584],
  [27330, 12, 33737, 2811]
 ]
}
```

Al final de `public/js/tests/vt-mensualidades.test.js` agrega:

```js
test('paridad con Python en los casos compartidos (incluye .5 exacto)', () => {
  const { casos } = JSON.parse(require('node:fs').readFileSync(require('node:path').join(__dirname, 'casos-mensualidades.json'), 'utf8'));
  for (const [contado, plazo, total, mensualidad] of casos) {
    const p = planes(contado).find((x) => x.plazo === plazo);
    assert.deepStrictEqual([p.total, p.mensualidad], [total, mensualidad], `${contado} a ${plazo}`);
  }
});
```

En `tools/pasto/tests/test_mensualidades.py`, cambia el encabezado de imports por:

```python
import json
import unittest
from pathlib import Path

from mensualidades import PLAZOS, planes, plazos_disponibles, redondear
```

y agrega al final:

```python


class ParidadConJavaScriptTest(unittest.TestCase):
    """Mismos casos que public/js/tests/vt-mensualidades.test.js (casos-mensualidades.json)."""

    def test_mensualidad_igual_a_math_round(self):
        ruta = Path(__file__).resolve().parents[3] / "public" / "js" / "tests" / "casos-mensualidades.json"
        for contado, plazo, total, mensualidad in json.loads(ruta.read_text(encoding="utf-8"))["casos"]:
            p = next(x for x in planes(contado) if x["plazo"] == plazo)
            with self.subTest(contado=contado, plazo=plazo):
                self.assertEqual((p["total"], p["mensualidad"]), (total, mensualidad))

    def test_redondear_sube_los_medios(self):
        self.assertEqual([redondear(x) for x in (958.5, 1666.5, 2.5, 0.49)], [959, 1667, 3, 0])
```

- [ ] **Step 2: Correrlas y ver que fallan**

```bash
cd ~/dev/viverosterra-e2b
node --test public/js/tests/vt-mensualidades.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
cd tools/pasto && python3 -m unittest tests.test_mensualidades 2>&1 | tail -3
```

Expected: `ℹ pass 4` y `ℹ fail 0` (el JS ya redondea así); en Python `ImportError: cannot import name 'redondear'` y `FAILED (errors=1)`.

- [ ] **Step 3: Corregir `mensualidades.py`**

En `tools/pasto/mensualidades.py`, justo antes de `def plazos_disponibles(contado):`, agrega:

```python
def redondear(x):
    """Igual que Math.round de JavaScript para valores positivos: los .5 suben (round() de Python los lleva al par y
    daba $1 menos que vt-mensualidades.js en mensualidades como 1,666.5)."""
    return int(math.floor(x + 0.5))


```

cambia `"mensualidad": round(total / plazo),` por `"mensualidad": redondear(total / plazo),` y, en el docstring, `Mantener igual a public/js/vt-mensualidades.js (prueba de paridad en test_mensualidades.py).` por:

```
Mantener igual a public/js/vt-mensualidades.js (paridad en test_mensualidades.py y vt-mensualidades.test.js, con los
casos de public/js/tests/casos-mensualidades.json).
```

En `tools/site/componentes.py`, reemplaza la función `redondear` completa (3 líneas) por una sola, para que haya una sola implementación:

```python
redondear = mensualidades.redondear  # Math.round de JavaScript: la misma función que usan las mensualidades
```

- [ ] **Step 4: Pruebas y build**

```bash
cd ~/dev/viverosterra-e2b/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../site && python3 -m unittest tests/test_componentes.py tests/test_medidor_paridad.py 2>&1 | tail -1
cd ../.. && python3 tools/site/build.py | tail -1 && git status --short public
git diff public/pasto-sintetico/envio | grep '^[-+][^-+]' | grep -o '12 × ≈ \$[0-9,]*'
```

Expected: `OK` (61 pruebas); `OK`; `shell: 0 de 108 …`; ` M public/pasto-sintetico/envio/monterrey/index.html` y ` M public/pasto-sintetico/envio/veracruz/index.html`; y `12 × ≈ $1,666` / `12 × ≈ $1,667` dos veces (antes y después). Nada más cambia: las demás mensualidades publicadas no caían en `.5`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/pasto/mensualidades.py tools/pasto/tests/test_mensualidades.py public/js/tests/casos-mensualidades.json public/js/tests/vt-mensualidades.test.js tools/site/componentes.py public/pasto-sintetico/envio/monterrey/index.html public/pasto-sintetico/envio/veracruz/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(mensualidades): Python redondea la mensualidad como Math.round del cotizador" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Un módulo de contenido puede armar varias páginas

Las 9 fichas y las 11 ciudades salen de los mismos datos: el módulo expone `CLAVES` y `pagina(clave)` (objeto con `CONTENIDO` y `PARIDAD`) y en `generar.PAGINAS` su contenido se escribe `"<módulo>:<clave>"`.

**Files:**
- Modify: `tools/site/generar.py`, `tools/site/tests/test_paridad.py`, `tools/site/tests/test_contenido.py`, `tools/site/tests/test_generar.py`

- [ ] **Step 1: Las pruebas cargan el contenido con `generar.cargar`**

En `tools/site/tests/test_paridad.py`: borra `import importlib`; cambia las dos apariciones de `mapa = importlib.import_module(f"contenido.{contenido}").PARIDAD` por `mapa = generar.cargar(contenido).PARIDAD` y `mapa = importlib.import_module("contenido.inicio").PARIDAD` por `mapa = generar.cargar("inicio").PARIDAD`.

En `tools/site/tests/test_contenido.py`: borra `import importlib` y cambia `yield ruta, importlib.import_module(f"contenido.{contenido}")` por `yield ruta, generar.cargar(contenido)`.

En `tools/site/tests/test_generar.py`, `self.assertEqual([r for r, *_ in generar.PAGINAS], ["/", "/pasto-en-rollo-tampico"])` pasa a `self.assertEqual([r for r, *_ in generar.PAGINAS][:2], ["/", "/pasto-en-rollo-tampico"])` (las páginas de sintético se agregan en las Tareas 9–12; la Tarea 12 fija la lista completa).

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_paridad.py tests/test_contenido.py 2>&1 | tail -3`
Expected: `AttributeError: module 'generar' has no attribute 'cargar'` y `FAILED`.

- [ ] **Step 2: `generar.cargar` y `_varias`**

Reemplaza todo `tools/site/generar.py` por:

```python
"""Páginas que salen de plantillas (Etapa 2). Cada entrada es (ruta, archivo en public/, plantilla, contenido): la
plantilla vive en tools/site/plantillas/<plantilla>.py y el contenido en tools/site/contenido/<contenido>.py.

Un módulo de contenido de una sola página expone CONTENIDO y PARIDAD. Uno que arma varias páginas de los mismos datos
(las 9 fichas o las 11 ciudades, desde tools/pasto/data.py) expone CLAVES y pagina(clave), que devuelve un objeto con
CONTENIDO y PARIDAD; en PAGINAS su contenido se escribe "<módulo>:<clave>".

Escribe cada página con el shell ya aplicado y solo si cambia, así una segunda corrida de build.py no toca nada. Para
migrar otro tipo de página: agrega su contenido, su plantilla (o reutiliza una) y su fila aquí.
"""
import importlib
from pathlib import Path

import paginas
import shell


def _varias(modulo, ruta_de, archivo_de, plantilla):
    m = importlib.import_module(f"contenido.{modulo}")
    return tuple((ruta_de(k), archivo_de(k), plantilla, f"{modulo}:{k}") for k in m.CLAVES)


PAGINAS = (
    ("/", "index.html", "inicio", "inicio"),
    ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
)


def cargar(contenido):
    """Objeto con CONTENIDO y PARIDAD de la clave "<módulo>" o "<módulo>:<clave>"."""
    nombre, _, clave = contenido.partition(":")
    modulo = importlib.import_module(f"contenido.{nombre}")
    return modulo.pagina(clave) if clave else modulo


def contenido_de(ruta):
    return next(contenido for r, _a, _p, contenido in PAGINAS if r == ruta)


def renderizar(ruta, plantilla, contenido, urls):
    """HTML final de la página: plantilla + contenido + shell."""
    modulo_plantilla = importlib.import_module(f"plantillas.{plantilla}")
    return shell.aplicar(modulo_plantilla.render(cargar(contenido).CONTENIDO), ruta, urls)


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

- [ ] **Step 3: Correr**

```bash
cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_paridad.py tests/test_contenido.py tests/test_generar.py 2>&1 | tail -1
cd ../.. && python3 tools/site/build.py | tail -2
```

Expected: `OK`; `plantillas: 0 de 2 …` y `shell: 0 de 108 …`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/generar.py tools/site/tests/test_paridad.py tools/site/tests/test_contenido.py tools/site/tests/test_generar.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(generar): un módulo de contenido puede armar varias páginas con sus claves" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: CSS minificado al publicar y hoja de la tienda (`terra-tienda.css`)

`terra.css` mide 10,211 B gzip (el límite es 10,240) y la tienda necesita ~4 KB más de componentes. Dos decisiones: (1) la copia con hash se publica minificada sin dependencias (sin comentarios ni sangría; nada dentro de las reglas cambia), y el presupuesto se mide sobre lo que se transfiere: 8.3 KB gzip; (2) los componentes de la tienda van en `terra-tienda.css`, que solo cargan las páginas `<body class="vt-pagina vt-tienda">`: la home y los servicios no pagan ese CSS. Presupuesto propio: < 6 KB gzip y < 24 KB sin comprimir. Dos agregados chicos a `terra.css` que reutilizarán 2c (planes de mantenimiento) y todas las plantillas: `.vt-modos` (formas de contratar) y los enlaces del cierre verde en tinta clara (axe marcaba contraste).

**Files:**
- Create: `public/css/terra-tienda.css`, `tools/site/tests/test_terra_tienda_css.py`
- Modify: `tools/site/activos.py`, `tools/site/activos.json` (lo reescribe el build), `tools/site/tests/test_activos.py`, `tools/site/tests/test_terra_css.py`, `tools/site/partials.py`, `tools/site/shell.py`, `vercel.json`, `tools/site/tests/test_vercel.py`, `public/css/terra.css`

- [ ] **Step 1: Pruebas**

`tools/site/tests/test_terra_tienda_css.py`:

```python
"""terra-tienda.css: hoja de la tienda de pasto sintético. Todo bajo .vt-tienda, sin colores literales, presupuesto
propio y clases sin prefijo solo si las crea o busca el JS de la tienda."""
import gzip
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import activos  # noqa: E402
from test_terra_css import clases, sin_comentarios, tokens  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[3] / "public"
TIENDA = PUBLIC / "css" / "terra-tienda.css"
# Clases que crean o buscan public/js/tienda-pasto.js y tienda-hub.js (no se reescriben): se estilan solo bajo .vt-tienda.
CLASES_DEL_JS = {"plan", "pay-rule", "buybar__info", "buybar__name", "buybar__price", "buybar__plan", "cot-item",
                 "cot-item__name", "cot-item__meta", "cot-item__m2", "cot-item__remove", "drawer__empty",
                 "gallery__slide", "is-updating", "quiz__pick", "quiz__pick--main", "quiz__label", "quiz__name",
                 "quiz__meta", "quiz__actions", "btn", "btn--primary"}


class TerraTiendaCssTest(unittest.TestCase):
    def setUp(self):
        self.css = TIENDA.read_text(encoding="utf-8")

    def test_todo_selector_bajo_vt_tienda(self):
        css = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}", "", sin_comentarios(self.css))
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", css):
            selector = selector.strip()
            if selector.startswith("@media"):
                continue
            ajenos += [p.strip() for p in selector.split(",") if not p.strip().startswith(".vt-tienda ")]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_y_solo_tokens_de_terra(self):
        css = sin_comentarios(self.css)
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])
        definidos = tokens((PUBLIC / "css" / "terra.css").read_text(encoding="utf-8"))
        usados = set(re.findall(r"var\((--vt-[\w-]+)\)", css))
        self.assertEqual(sorted(usados - set(definidos)), [])

    def test_presupuesto(self):
        publicado = activos.minificar_css(self.css).encode("utf-8")
        self.assertLess(len(gzip.compress(publicado, mtime=0)), 6 * 1024)
        self.assertLess(len(publicado), 24 * 1024)

    def test_clases_sin_prefijo_solo_las_del_js(self):
        propias = {c for c in clases(self.css) if not c.startswith("vt-")}
        self.assertEqual(sorted(propias - CLASES_DEL_JS), [])
        fuentes = "".join(p.read_text(encoding="utf-8") for p in (PUBLIC / "js" / "tienda-pasto.js",
                                                                  PUBLIC / "js" / "tienda-hub.js"))
        for clase in sorted(propias):
            with self.subTest(clase=clase):
                self.assertIn(clase, fuentes)

    def test_movimiento_reducido(self):
        self.assertIn("@media (prefers-reduced-motion:reduce)", self.css)


if __name__ == "__main__":
    unittest.main()
```

En `tools/site/tests/test_terra_css.py`: agrega `import sys` después de `import re`; después de `from pathlib import Path` agrega

```python

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
```

y en `test_presupuesto` cambia `datos = self.css.encode("utf-8")` por:

```python
        # Se mide la copia publicada (activos.minificar_css: sin comentarios ni sangría), que es la que se transfiere.
        datos = activos.minificar_css(self.css).encode("utf-8")
```

Reemplaza todo `tools/site/tests/test_activos.py` por (respecto de la Tarea 1: `setUp` crea también `terra-tienda.css`, la copia publicada de CSS termina en salto de renglón y hay una prueba de la minificación):

```python
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pub = Path(tmp.name) / "public"
        (self.pub / "css").mkdir(parents=True)
        (self.pub / "js").mkdir()
        (self.pub / "blog").mkdir()
        self.registro = Path(tmp.name) / "activos.json"
        self.escribir(".vt-a{}")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "css" / "terra-tienda.css").write_text(".vt-tienda .vt-x{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def escribir(self, css):
        (self.pub / "css" / "terra.css").write_text(css, encoding="utf-8")

    def publicar(self):
        return activos.publicar(self.pub, self.registro)

    def copias(self):
        return sorted(p.name for p in (self.pub / "css").glob("terra.*.css"))

    def copia(self, nombre, mtime=1_000_000_000):
        path = self.pub / "css" / nombre
        path.write_text("viejo", encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    def pagina_enlaza(self, nombre):
        """Simula el HTML publicado antes del build (sin git, publicar lo lee de disco)."""
        (self.pub / "index.html").write_text(f'<link rel="stylesheet" href="/css/{nombre}">', encoding="utf-8")

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_la_fuente(self):
        urls = self.publicar()
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}\n")
        self.assertTrue((self.pub / "css" / "terra.css").exists())

    def test_conserva_la_que_enlazan_las_paginas_aunque_sea_la_mas_vieja(self):
        # El caso del deploy del 2026-11-07: la copia servida tenía el mtime más viejo y se borró.
        servida = self.copia("terra.3eaa08fd32.css", mtime=1_000_000_000)
        reciente = self.copia("terra.73fd9d1d2c.css", mtime=2_000_000_000)
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.assertTrue(servida.exists())
        self.assertFalse(reciente.exists())
        self.assertEqual(self.copias(), sorted([servida.name, Path(urls["terra.css"]).name]))
        self.assertEqual(json.loads(self.registro.read_text(encoding="utf-8"))["terra.css"],
                         [urls["terra.css"], f"/css/{servida.name}"])

    def test_segunda_corrida_no_borra_la_servida(self):
        # Tras la primera corrida las páginas ya enlazan la copia nueva: el registro recuerda la servida.
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        urls = self.publicar()
        self.pagina_enlaza(Path(urls["terra.css"]).name)
        registro = self.registro.read_text(encoding="utf-8")
        self.assertEqual(self.publicar(), urls)
        self.assertTrue(servida.exists())
        self.assertEqual(self.registro.read_text(encoding="utf-8"), registro)

    def test_varios_cambios_en_la_rama_siguen_guardando_la_de_produccion(self):
        servida = self.copia("terra.3eaa08fd32.css")
        self.pagina_enlaza(servida.name)
        self.publicar()
        self.escribir(".vt-b{}")
        segunda = self.publicar()["terra.css"]
        self.escribir(".vt-c{}")
        tercera = self.publicar()["terra.css"]
        self.assertEqual(self.copias(), sorted([servida.name, Path(tercera).name]))
        self.assertFalse((self.pub / segunda.lstrip("/")).exists())

    def test_sin_registro_ni_paginas_deja_solo_la_actual(self):
        self.copia("terra.0000000000.css")
        urls = self.publicar()
        self.assertEqual(self.copias(), [Path(urls["terra.css"]).name])

    def test_no_toca_archivos_que_no_son_copias(self):
        ajeno = self.pub / "css" / "terra.min.css"
        ajeno.write_text("x", encoding="utf-8")
        self.publicar()
        self.assertTrue(ajeno.exists())

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_mismo_contenido_mismo_hash(self):
        antes = activos.urls(self.pub)["terra.css"]
        self.escribir(".vt-b{}")
        self.escribir(".vt-a{}")
        self.assertEqual(antes, activos.urls(self.pub)["terra.css"])

    def test_css_publicado_sin_comentarios_ni_sangria_y_con_las_mismas_reglas(self):
        css = "/* nota */\n.vt-a{\n  content:\"a  b\";\n  margin:0 auto}\n\n@media (min-width:768px){\n  .vt-b{x:y}\n}\n"
        self.assertEqual(activos.minificar_css(css),
                         '.vt-a{\ncontent:"a  b";\nmargin:0 auto}\n@media (min-width:768px){\n.vt-b{x:y}\n}\n')
        terra = (activos.PUBLIC / "css" / "terra.css").read_text(encoding="utf-8")

        def reglas(texto):
            return [r.strip() for r in re.findall(r"[^{}]+\{", re.sub(r"/\*.*?\*/", "", texto, flags=re.S))]
        self.assertEqual(reglas(activos.minificar_css(terra)), reglas(terra))

    def test_registro_del_repo_coincide_con_lo_publicado(self):
        registro = json.loads(activos.REGISTRO.read_text(encoding="utf-8"))
        urls = activos.urls()
        for clave, rel in activos.FUENTES.items():
            with self.subTest(asset=clave):
                self.assertEqual(registro[clave][0], urls[clave])
                for url in registro[clave]:
                    self.assertTrue((activos.PUBLIC / url.lstrip("/")).is_file(), url)
                copias = {"/" + p.relative_to(activos.PUBLIC).as_posix()
                          for p in (activos.PUBLIC / rel).parent.glob(f"{Path(rel).stem}.*{Path(rel).suffix}")
                          if activos._patron(rel).fullmatch("/" + p.relative_to(activos.PUBLIC).as_posix())}
                self.assertEqual(copias, set(registro[clave]))


if __name__ == "__main__":
    unittest.main()
```

En `tools/site/tests/test_vercel.py`, `HASH = r"/(css|js)/(terra|legacy-fixes)\.([0-9a-f]+)\.(css|js)"` pasa a `HASH = r"/(css|js)/(terra|terra-tienda|legacy-fixes)\.([0-9a-f]+)\.(css|js)"`.

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest discover -s tests -p "test_*css*.py" 2>&1 | tail -3; python3 -m unittest tests/test_activos.py 2>&1 | tail -1`
Expected: `FileNotFoundError` de `terra-tienda.css` / `AttributeError: module 'activos' has no attribute 'minificar_css'` y `FAILED`.

- [ ] **Step 2: Minificar al publicar y registrar la hoja nueva**

En `tools/site/activos.py`:

1. En el docstring, `La fuente vive sin hash (public/css/terra.css, public/css/legacy-fixes.css, public/js/terra.js) y el build publica\n<nombre>.<10 hex>.<ext> al lado. Se conservan dos` pasa a `La fuente vive sin hash (public/css/terra.css, terra-tienda.css, legacy-fixes.css, public/js/terra.js) y el build\npublica <nombre>.<10 hex>.<ext> al lado; las hojas CSS van minificadas (sin comentarios ni sangría). Se conservan dos`.
2. En `FUENTES`, después de `"terra.css": "css/terra.css",` agrega `"terra-tienda.css": "css/terra-tienda.css",`.
3. Antes de `def _con_hash(rel, contenido):` agrega:

```python
def minificar_css(texto):
    """Sin comentarios, sin sangría ni renglones vacíos. No toca nada dentro de una regla: es seguro con cadenas,
    url(), calc() y valores con espacios, y no necesita dependencias."""
    sin_comentarios = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
    return "".join(linea.strip() + "\n" for linea in sin_comentarios.splitlines() if linea.strip())


def publicado(rel, bruto):
    """Bytes de la copia con hash: las hojas CSS van minificadas; el JS va tal cual."""
    return minificar_css(bruto.decode("utf-8")).encode("utf-8") if rel.endswith(".css") else bruto


```

4. En `urls()`, `_con_hash(rel, (public / rel).read_bytes())` pasa a `_con_hash(rel, publicado(rel, (public / rel).read_bytes()))`; en `publicar()`, `destino.write_bytes(fuente.read_bytes())` pasa a `destino.write_bytes(publicado(rel, fuente.read_bytes()))`.

En `vercel.json`, la fuente de la regla de caché inmutable `"/(css|js)/(terra|legacy-fixes)\\.([0-9a-f]+)\\.(css|js)"` pasa a `"/(css|js)/(terra|terra-tienda|legacy-fixes)\\.([0-9a-f]+)\\.(css|js)"`.

- [ ] **Step 3: El shell agrega la hoja a las páginas de la tienda**

En `tools/site/partials.py`, la firma `def head(urls, legacy):` pasa a `def head(urls, legacy, tienda=False):`; en su docstring, `GA4 una sola vez y terra.js diferido. Las meta keywords, last-modified, ai-content-declaration y language ya no se\n    usan: no se reponen."""` pasa a:

```python
    GA4 una sola vez y terra.js diferido. Con tienda=True (páginas <body class="vt-pagina vt-tienda">), también
    terra-tienda.css. Las meta keywords, last-modified, ai-content-declaration y language ya no se usan: no se
    reponen."""
```

y reemplaza

```python
    lineas += [
        f'<link rel="stylesheet" href="{urls["terra.css"]}">',
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={datos.GA4_ID}"></script>',
```

por

```python
    lineas += [
        f'<link rel="stylesheet" href="{urls["terra.css"]}">',
    ]
    if tienda:
        lineas.append(f'<link rel="stylesheet" href="{urls["terra-tienda.css"]}">')
    lineas += [
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={datos.GA4_ID}"></script>',
```

En `tools/site/shell.py`, antes de `CONTEO_BLOG_RE =` agrega `TIENDA = '<body class="vt-pagina vt-tienda">'` y en `aplicar()` cambia `"head": partials.head(urls, legacy="/css/tailwind.css" in html),` por `"head": partials.head(urls, legacy="/css/tailwind.css" in html, tienda=TIENDA in html),`.

- [ ] **Step 4: La hoja de la tienda y los dos agregados de `terra.css`**

`public/css/terra-tienda.css`:

```css
/* Viveros Terra · terra-tienda.css · Etapa 2b
   Hoja de la tienda de pasto sintético (hub, fichas, ciudades, perros y sintético en Tampico). Solo la cargan las páginas
   <body class="vt-pagina vt-tienda">, después de terra.css, y usa sus tokens: ningún color literal. Todo selector empieza
   con .vt-tienda; las clases sin prefijo vt- (plan, buybar__*, cot-item*, quiz__*, btn, spec-card*, gallery__slide,
   pay-rule, drawer__empty, is-updating) son las que crean o buscan tienda-pasto.js y tienda-hub.js, que no se reescriben. */
.vt-tienda main{font-variant-numeric:tabular-nums}
.vt-tienda .vt-subnav{border-bottom:1px solid var(--vt-line);background:var(--vt-bone-2)}
.vt-tienda .vt-subnav__bar{display:flex;flex-wrap:wrap;align-items:center;gap:4px 18px;min-height:48px}
.vt-tienda main .vt-subnav a{font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-ink);text-decoration:none}
.vt-tienda .vt-subnav__lista{display:inline-flex;align-items:center;gap:6px;min-height:44px;margin-left:auto;padding:0 14px;border:1.5px solid var(--vt-ink);border-radius:var(--vt-radius);background:var(--vt-card);font:600 var(--vt-text-sm) var(--vt-font-sans);color:var(--vt-ink);cursor:pointer}
.vt-tienda .vt-subnav__n{min-width:22px;padding:1px 6px;border-radius:var(--vt-radius);background:var(--vt-tag);color:var(--vt-tag-ink);font-weight:800}
.vt-tienda .vt-subnav__n[data-empty="true"]{display:none}
@media (max-width:767px){.vt-tienda .vt-subnav__bar a{display:none}.vt-tienda .vt-subnav__lista{margin-left:0}}
/* portada de la ficha: info, galería y cotizador */
.vt-tienda .vt-ficha{padding:20px 0 var(--vt-space-section)}
.vt-tienda .vt-ficha__grid{display:grid;gap:28px;margin-top:16px}
.vt-tienda .vt-ficha__grid>*,.vt-tienda .vt-portada__grid>*{min-width:0}
.vt-tienda main .vt-ficha h1{font-size:var(--vt-text-h1);line-height:.95}
.vt-tienda .vt-ficha__pre{display:block;font-size:var(--vt-text-h3);font-weight:600;letter-spacing:0;color:var(--vt-ink-2)}
.vt-tienda .vt-ficha__insignia{margin-left:.2em;padding:2px 8px;vertical-align:middle;border:1px solid var(--vt-field);font-size:var(--vt-text-xs);font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-field)}
.vt-tienda main .vt-existencia{display:flex;flex-wrap:wrap;gap:4px 14px;margin:12px 0 16px;font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-field)}
.vt-tienda .vt-existencia span::before{content:"● ";color:var(--vt-field)}
.vt-tienda .vt-ficha .vt-etiqueta-x{max-width:420px}
.vt-tienda .vt-ficha .vt-lede{margin-top:16px}
@media (min-width:1024px){
  .vt-tienda .vt-ficha__grid{grid-template-columns:7fr 5fr;grid-template-areas:"gal info" "gal cot";align-items:start;column-gap:48px}
  .vt-tienda .vt-ficha__info{grid-area:info}.vt-tienda .vt-galeria{grid-area:gal;position:sticky;top:calc(var(--vt-head-h) + 16px)}.vt-tienda .vt-ficha .vt-cotizador{grid-area:cot}
}
/* galería */
.vt-tienda .vt-galeria__pista{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;scrollbar-width:none}
.vt-tienda .vt-galeria__pista::-webkit-scrollbar{display:none}
.vt-tienda .vt-galeria__pista:focus-visible{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-tienda .gallery__slide{flex:0 0 100%;scroll-snap-align:start;margin:0}
.vt-tienda .gallery__slide .vt-fig__marco{position:relative;aspect-ratio:3/4}
.vt-tienda .vt-galeria__meta{display:flex;align-items:center;gap:14px;margin-top:10px}
.vt-tienda .vt-galeria__n{font-size:var(--vt-text-xs);font-weight:700;color:var(--vt-muted)}
.vt-tienda .vt-galeria__minis{display:flex;gap:8px;overflow-x:auto}
.vt-tienda .vt-galeria__mini{flex:none;width:52px;height:52px;padding:0;border:1.5px solid var(--vt-line);border-radius:var(--vt-radius);background:none;cursor:pointer}
.vt-tienda .vt-galeria__mini[aria-current="true"]{border-color:var(--vt-field)}
.vt-tienda .vt-galeria__mini img{display:block;width:100%;height:100%;object-fit:cover}
.vt-tienda .vt-chip-mm{position:absolute;left:12px;top:12px;padding:4px 8px;background:var(--vt-ink);color:var(--vt-on-dark);font-weight:800;font-size:var(--vt-text-sm);line-height:1}
.vt-tienda .vt-chip-mm small{margin-left:2px;font-size:.75em;font-weight:600}
/* cotizador (marcado de tienda-pasto.js) */
.vt-tienda .vt-dos>*,.vt-tienda .vt-cotizador>*{min-width:0}
.vt-tienda .vt-cotizador{display:grid;min-width:0;gap:16px;padding:20px 16px;border:1.5px solid var(--vt-ink);background:var(--vt-card)}
.vt-tienda main .vt-cotizador__t{font-size:var(--vt-text-h3)}
.vt-tienda main .vt-cotizador__desde{margin:0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-tienda .vt-cotizador__desde b{padding:1px 5px;background:var(--vt-tag);color:var(--vt-tag-ink);font-size:1.15em}
.vt-tienda .vt-stepper{display:grid;grid-template-columns:48px 1fr 48px;min-height:52px;border:1.5px solid var(--vt-ink);border-radius:var(--vt-radius);background:var(--vt-card)}
.vt-tienda .vt-stepper button{border:0;background:var(--vt-bone-2);font:700 22px var(--vt-font-sans);color:var(--vt-ink);cursor:pointer}
.vt-tienda .vt-stepper input{min-width:0;border:0;text-align:center;font:800 22px var(--vt-font-sans);font-variant-numeric:tabular-nums;color:var(--vt-ink);background:transparent}
.vt-tienda .vt-stepper:focus-within{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-tienda .vt-control select{flex:1;width:100%;min-width:0;height:50px;padding:0 12px;border:0;background:transparent;font:600 16px var(--vt-font-sans);color:var(--vt-ink)}
.vt-tienda .vt-control select:focus{outline:none}
.vt-tienda .vt-chips,.vt-tienda .vt-filtros{display:flex;flex-wrap:wrap;gap:8px}
.vt-tienda .vt-chip{min-height:44px;padding:0 14px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);font:600 var(--vt-text-sm) var(--vt-font-sans);color:var(--vt-ink);cursor:pointer}
.vt-tienda .vt-chip[aria-pressed="true"]{border-color:var(--vt-field);background:var(--vt-field-100);box-shadow:inset 0 0 0 1px var(--vt-field)}
.vt-tienda .vt-tiers{width:100%;border-collapse:collapse;font-size:var(--vt-text-sm)}
.vt-tienda .vt-tiers caption{padding-bottom:6px;text-align:left;font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-muted)}
.vt-tienda .vt-tiers th,.vt-tienda .vt-tiers td{padding:8px 0;border-bottom:1px dashed var(--vt-line-strong);text-align:left;font-weight:600}
.vt-tienda .vt-tiers th span{display:block;font-weight:400;color:var(--vt-muted)}
.vt-tienda .vt-tiers td{text-align:right;white-space:nowrap}
.vt-tienda .vt-tiers tr[data-active="true"] td{color:var(--vt-field);font-weight:800}
.vt-tienda .vt-tiers tr[data-active="true"] th{box-shadow:inset 3px 0 0 var(--vt-field);padding-left:10px}
.vt-tienda .vt-cuenta{padding-top:6px;border-top:1px solid var(--vt-line)}
.vt-tienda main .vt-cuenta p{margin:0}
.vt-tienda .vt-cuenta__fila,.vt-tienda .vt-cuenta__total{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:6px 0;font-size:var(--vt-text-sm)}
.vt-tienda .vt-cuenta__total{margin-top:6px;padding:10px 12px;background:var(--vt-tag);color:var(--vt-tag-ink);font-weight:700}
.vt-tienda .vt-cuenta__total b{font-size:var(--vt-text-h3);font-weight:800}
.vt-tienda .vt-cuenta__puesto,.vt-tienda .vt-cuenta__pista{font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-tienda .vt-cuenta__error:not(:empty){margin-top:8px;padding:8px 12px;border-left:3px solid var(--vt-soil);background:var(--vt-bone-2);font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-soil)}
.vt-tienda .vt-planes-t{display:grid;gap:10px;margin:0;padding:0;border:0}
.vt-tienda .vt-planes-t[hidden]{display:none}
.vt-tienda .vt-planes-t legend{margin-bottom:6px;font-size:var(--vt-text-sm);font-weight:600}
.vt-tienda .vt-planes-t__trip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:0;border:1px solid var(--vt-line)}
.vt-tienda .vt-planes-t__trip div{padding:8px 10px;border-right:1px solid var(--vt-line)}
.vt-tienda .vt-planes-t__trip div:last-child{border-right:0}
.vt-tienda .vt-planes-t__trip dt{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .vt-planes-t__trip dd{margin:0;font-weight:800}
.vt-tienda .vt-planes-t__lista{display:grid;gap:6px}
.vt-tienda .plan{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:4px 10px;min-height:48px;padding:8px 12px;border:1.5px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:var(--vt-card);cursor:pointer}
.vt-tienda .plan:has(input:checked){border-color:var(--vt-field);background:var(--vt-field-100)}
.vt-tienda .plan:has(input:focus-visible){outline:2px solid var(--vt-field);outline-offset:2px}
.vt-tienda .plan[data-disabled="true"]{border-style:dashed;color:var(--vt-muted);cursor:not-allowed}
.vt-tienda .plan input{accent-color:var(--vt-field)}
.vt-tienda .vt-plan__n{font-weight:700;font-size:var(--vt-text-sm)}
.vt-tienda .vt-plan__n small{display:block;font-weight:400;color:var(--vt-muted)}
.vt-tienda .vt-plan__monto{font-size:var(--vt-text-sm);font-weight:800;text-align:right;white-space:nowrap}
.vt-tienda .vt-plan__total{grid-column:2 / -1;font-size:var(--vt-text-xs);color:var(--vt-muted);text-align:right}
.vt-tienda .vt-plan__total:empty,.vt-tienda .pay-rule{display:none}
.vt-tienda main .vt-planes-t__ahorro{margin:0;font-size:var(--vt-text-sm);font-weight:600;color:var(--vt-field)}
.vt-tienda main .vt-planes-t__nota{margin:0;font-size:var(--vt-text-xs);line-height:1.45;color:var(--vt-muted)}
.vt-tienda .vt-cotizador__acciones{display:grid;gap:10px}
.vt-tienda .vt-cotizador__acciones .vt-btn{width:100%}
.vt-tienda .vt-campo--ancho{grid-column:1 / -1}
/* lista de cotización, aviso y barra de compra */
.vt-tienda .vt-lista{width:min(100% - 24px,460px);max-height:calc(100dvh - 24px);margin:auto 0 auto auto;padding:0;border:0;background:var(--vt-bone);color:var(--vt-ink);font-family:var(--vt-font-sans)}
.vt-tienda .vt-lista::backdrop{background:var(--vt-scrim)}
.vt-tienda .vt-lista__in{display:grid;gap:14px;padding:20px}
.vt-tienda .vt-lista__cabeza{display:flex;justify-content:space-between;align-items:center}
.vt-tienda .vt-lista h2{margin:0;font-size:var(--vt-text-h3);font-weight:800}
.vt-tienda .vt-lista__cerrar{width:44px;height:44px;border:1px solid var(--vt-line-strong);background:var(--vt-card);font-size:24px;cursor:pointer}
.vt-tienda .vt-lista__pie{display:grid;gap:12px}
.vt-tienda .vt-lista__pie[hidden]{display:none}
.vt-tienda .vt-lista :focus-visible{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-tienda .cot-item{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:start;padding:12px 0;border-bottom:1px solid var(--vt-line)}
.vt-tienda .cot-item__name{font-weight:700}
.vt-tienda .cot-item__meta{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .cot-item__m2 input{width:84px;min-height:40px;margin-top:6px;padding:0 8px;border:1.5px solid var(--vt-ink);font:700 16px var(--vt-font-sans)}
.vt-tienda .cot-item__remove{min-height:40px;border:0;background:none;color:var(--vt-soil);font-weight:600;text-decoration:underline;cursor:pointer}
.vt-tienda .drawer__empty{color:var(--vt-ink-2)}
.vt-tienda .vt-aviso{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom));z-index:var(--vt-z-bar);display:flex;align-items:center;gap:14px;padding:10px 12px 10px 16px;background:var(--vt-ink);color:var(--vt-on-dark);font:600 var(--vt-text-sm) var(--vt-font-sans);transform:translate(-50%,24px);opacity:0;pointer-events:none;transition:opacity var(--vt-duration-normal),transform var(--vt-duration-normal) var(--vt-ease-out)}
.vt-tienda .vt-aviso[data-visible="true"]{transform:translate(-50%,0);opacity:1;pointer-events:auto}
.vt-tienda .vt-aviso button{min-height:40px;padding:0 12px;border:1px solid var(--vt-on-dark);background:none;color:var(--vt-on-dark);font-weight:700;cursor:pointer}
.vt-tienda .vt-compra{position:fixed;left:0;right:0;bottom:0;z-index:var(--vt-z-bar);display:flex;align-items:center;gap:12px;min-height:var(--vt-bar-h);padding:8px var(--vt-gutter) calc(8px + env(safe-area-inset-bottom));border-top:1px solid var(--vt-line);background:var(--vt-bone);font-family:var(--vt-font-sans);transform:translateY(110%);visibility:hidden;transition:transform var(--vt-duration-normal) var(--vt-ease-out),visibility 0s var(--vt-duration-normal)}
.vt-tienda .vt-compra[data-visible="true"]{transform:none;visibility:visible;transition-delay:0s}
.vt-tienda .buybar__info{flex:1;min-width:0}
.vt-tienda .buybar__name{font-size:var(--vt-text-xs);font-weight:600;color:var(--vt-muted)}
.vt-tienda .buybar__price{font-weight:800}
.vt-tienda .buybar__plan{font-size:var(--vt-text-xs);color:var(--vt-ink-2)}
@media (min-width:1024px){.vt-tienda .vt-compra{display:none}}
/* catálogo del hub */
.vt-tienda .vt-catalogo{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:20px;margin-top:20px}
.vt-tienda .vt-tarjeta-p{display:flex;flex-direction:column;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .vt-tarjeta-p[hidden]{display:none}
.vt-tienda .vt-tarjeta-p__foto{position:relative;display:block;aspect-ratio:3/4;overflow:hidden}
.vt-tienda .vt-tarjeta-p__foto img,.vt-tienda .vt-vecino__foto img{display:block;width:100%;height:100%;object-fit:cover}
.vt-tienda .vt-tarjeta-p__hoy{position:absolute;left:12px;bottom:12px;padding:4px 8px;background:var(--vt-tag);color:var(--vt-tag-ink);font-size:var(--vt-text-xs);font-weight:700}
.vt-tienda .vt-tarjeta-p__cuerpo{display:grid;gap:8px;flex:1;padding:16px}
.vt-tienda main .vt-tarjeta-p p{margin:0}
.vt-tienda .vt-tarjeta-p__tag,.vt-tienda .vt-vecino__tag{font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--vt-muted)}
.vt-tienda main .vt-tarjeta-p h3 a,.vt-tienda main .vt-vecino h3 a,.vt-tienda main .vt-recomendado h3 a{color:var(--vt-ink);text-decoration:none}
.vt-tienda .vt-tarjeta-p__datos,.vt-tienda .vt-vecino dl{display:flex;gap:16px;margin:0;font-size:var(--vt-text-sm)}
.vt-tienda .vt-tarjeta-p__datos dt,.vt-tienda .vt-vecino dt{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .vt-tarjeta-p__datos dd,.vt-tienda .vt-vecino dd{margin:0;font-weight:700}
.vt-tienda .vt-tarjeta-p__precio b,.vt-tienda .vt-vecino__precio b,.vt-tienda .vt-recomendado__precio b{padding:0 4px;background:var(--vt-tag);color:var(--vt-tag-ink);font-size:1.25em}
.vt-tienda .vt-tarjeta-p__puesto{display:block;font-size:var(--vt-text-xs);color:var(--vt-field)}
.vt-tienda main .vt-tarjeta-p__pago{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .vt-tarjeta-p .vt-btn,.vt-tienda .vt-vecino .vt-btn{width:100%;margin-top:auto}
.vt-tienda .vt-filtros__n{margin:10px 0 0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-tienda .vt-regla{display:flex;align-items:center;gap:10px}
.vt-tienda .vt-regla__pista{flex:1;height:6px;background:var(--vt-bone-2)}
.vt-tienda .vt-regla__fill{display:block;width:var(--w);height:100%;background:var(--vt-soil)}
.vt-tienda .vt-regla__val{font-weight:800;color:var(--vt-soil)}
.vt-tienda .vt-regla__val small{margin-left:2px;font-size:.75em}
/* selector, comparador y portada del hub */
.vt-tienda .vt-quiz{display:grid;gap:18px}
@media (min-width:768px){.vt-tienda .vt-quiz{grid-template-columns:repeat(3,1fr)}.vt-tienda .vt-quiz>p,.vt-tienda .vt-quiz__res{grid-column:1 / -1}}
.vt-tienda .vt-quiz__res{display:grid;gap:12px}
@media (min-width:768px){.vt-tienda .vt-quiz__res{grid-template-columns:1fr 1fr}}
.vt-tienda .quiz__pick{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:14px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .quiz__pick--main{border:1.5px solid var(--vt-field)}
.vt-tienda .quiz__pick img{width:96px;height:96px;object-fit:cover}
.vt-tienda main .quiz__label,.vt-tienda main .quiz__meta{margin:0;font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda main .quiz__name{font-size:var(--vt-text-h3);font-weight:800;color:var(--vt-ink)}
.vt-tienda .quiz__actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.vt-tienda .quiz__actions .btn{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1.5px solid var(--vt-field);border-radius:var(--vt-radius);background:var(--vt-card);font:600 var(--vt-text-sm) var(--vt-font-sans);color:var(--vt-field);text-decoration:none;cursor:pointer}
.vt-tienda main .quiz__actions .btn--primary{background:var(--vt-field);color:var(--vt-card)}
.vt-tienda .vt-comparador{display:grid;gap:14px;max-width:640px}
.vt-tienda main .vt-comparador__res{margin:0;padding:12px 14px;border-left:3px solid var(--vt-field);background:var(--vt-card);font-weight:600}
.vt-tienda .vt-portada-t .vt-cta .vt-btn{white-space:normal;text-align:center}
.vt-tienda .vt-portada-t .vt-campo{max-width:420px;margin-top:18px}
.vt-tienda main .vt-precio-puesto{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px;margin:14px 0 0}
.vt-tienda .vt-precio-puesto b{padding:2px 8px;background:var(--vt-tag);color:var(--vt-tag-ink);font-size:var(--vt-text-precio);font-weight:800;line-height:1}
.vt-tienda .vt-precio-puesto small{flex-basis:100%;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-tienda .is-updating b{animation:vt-pulso .6s var(--vt-ease-out)}
@keyframes vt-pulso{from{opacity:.4}to{opacity:1}}
@media (prefers-reduced-motion:reduce){.vt-tienda .is-updating b{animation:none}.vt-tienda .vt-aviso,.vt-tienda .vt-compra{transition:none}}
/* ficha: técnica, vecinos, envío; ciudades y recomendados */
.vt-tienda .vt-tecnica{display:grid;gap:20px}
@media (min-width:768px){.vt-tienda .vt-tecnica{grid-template-columns:repeat(2,1fr)}}
.vt-tienda .vt-tecnica__g{padding:16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .vt-tecnica dl,.vt-tienda .vt-glosario{margin:10px 0 0}
.vt-tienda .vt-tecnica dl div{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px dashed var(--vt-line);font-size:var(--vt-text-sm)}
.vt-tienda .vt-tecnica dt small{display:block;font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .vt-tecnica dd{margin:0;font-weight:700;text-align:right}
.vt-tienda .vt-glosario{display:grid;gap:12px;margin-top:20px}
@media (min-width:768px){.vt-tienda .vt-glosario{grid-template-columns:repeat(4,1fr)}}
.vt-tienda .vt-glosario dt{font-weight:700}
.vt-tienda .vt-glosario dd{margin:2px 0 0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-tienda .vt-rollo{margin-top:24px;padding:14px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .vt-rollo svg{display:block;width:100%;height:auto}
.vt-tienda .vt-vecinos,.vt-tienda .vt-recomendados{display:grid;gap:20px;list-style:none}
@media (min-width:768px){.vt-tienda .vt-vecinos,.vt-tienda .vt-recomendados{grid-template-columns:repeat(3,1fr)}}
.vt-tienda .vt-vecino{display:grid;gap:8px;padding:14px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .vt-vecino--actual{border:1.5px solid var(--vt-field)}
.vt-tienda .vt-vecino__foto{position:relative;aspect-ratio:4/3;overflow:hidden}
.vt-tienda main .vt-vecino p{margin:0}
.vt-tienda .vt-zonas-envio{display:grid;gap:12px;margin:20px 0 32px}
@media (min-width:768px){.vt-tienda .vt-zonas-envio{grid-template-columns:repeat(3,1fr)}}
.vt-tienda .vt-zonas-envio div{padding:16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda .vt-zonas-envio dt{font-size:var(--vt-text-h3);font-weight:800;color:var(--vt-soil)}
.vt-tienda .vt-zonas-envio dt small{font-size:var(--vt-text-sm);font-weight:600}
.vt-tienda .vt-zonas-envio dd{margin:6px 0 0;font-size:var(--vt-text-sm);color:var(--vt-ink-2)}
.vt-tienda .vt-recomendado{display:grid;gap:8px;padding:16px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-tienda main .vt-recomendado p{margin:0;font-size:var(--vt-text-sm)}
.vt-tienda .vt-ciudades{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;list-style:none}
.vt-tienda main .vt-ciudades a{display:grid;gap:2px;min-height:44px;padding:12px 14px;border:1px solid var(--vt-line);background:var(--vt-card);color:var(--vt-ink);text-decoration:none}
.vt-tienda .vt-ciudades span{font-size:var(--vt-text-xs);color:var(--vt-muted)}
.vt-tienda .vt-ciudades a:hover{border-color:var(--vt-field)}
```

En `public/css/terra.css`, después de `.vt-pagina main a:not(.vt-btn):hover{color:var(--vt-field-deep)}` agrega:

```css
.vt-pagina main .vt-cierre a:not(.vt-btn){color:var(--vt-on-dark)}
```

y antes de `/* ---------- proceso NOSOTROS / TÚ / JUNTOS ---------- */` agrega:

```css
/* ---------- formas de contratar (máx. 3, cada una con su mensaje) ---------- */
.vt-modos{display:grid;gap:20px;list-style:none}
@media (min-width:768px){.vt-modos{grid-template-columns:repeat(auto-fit,minmax(0,1fr))}}
.vt-modo{display:grid;gap:14px;align-content:start;padding:24px 20px;border:1px solid var(--vt-line);background:var(--vt-card)}
.vt-modo--rec{border:1.5px solid var(--vt-field)}
.vt-pagina main .vt-modo p{margin:0}
.vt-pagina main .vt-modo__n{font-size:var(--vt-text-xs);font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--vt-muted)}
.vt-modo__precio small{display:block;margin-top:4px;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-modo .vt-btn{width:100%}

```

- [ ] **Step 5: Pruebas, presupuesto y build**

```bash
cd ~/dev/viverosterra-e2b && python3 tools/site/build.py | tail -2 && cat tools/site/activos.json && git status --short | grep -v '\.html$'
cd tools/site && python3 -m unittest discover -s tests -p "test_*css*.py" 2>&1 | tail -1
python3 -m unittest tests/test_activos.py tests/test_vercel.py tests/test_sitio.py tests/test_shell.py tests/test_partials.py 2>&1 | tail -1
python3 -c "
import gzip, activos
for r in ('css/terra.css', 'css/terra-tienda.css'):
    b = activos.publicado(r, (activos.PUBLIC / r).read_bytes()); print(r, len(b), len(gzip.compress(b, mtime=0)))"
```

(El build va primero: el registro y las copias en disco tienen que coincidir antes de `test_activos`.) Expected: `plantillas: 2 de 2 …` y `shell: 76 de 108 …` (todas cambian de hash de `terra.css`: las 30 que genera `tools/pasto` reciben el shell en su propio build y las 2 con plantilla las escribe `generar`); el registro con `terra.css: [nueva, "/css/terra.ed57f9f3b4.css"]` (la que sirve producción, leída de `main`: `3eaa…` sale), `terra-tienda.css: [nueva]` y `legacy-fixes.css: [nueva, "/css/legacy-fixes.6fb87ff99e.css"]`; fuera de HTML: `public/css/terra.css`, `public/css/terra-tienda.css`, las copias con hash nuevas y borradas, `tools/site/activos.json`, `vercel.json` y los `.py` (ninguna página enlaza todavía `terra-tienda.css`); luego `OK`; `OK`; y `css/terra.css 42… 83…` (≈ 8.3 KB gzip) y `css/terra-tienda.css 19… 38…` (≈ 3.8 KB).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add public tools/site/activos.py tools/site/activos.json tools/site/partials.py tools/site/shell.py vercel.json tools/site/tests/test_activos.py tools/site/tests/test_terra_css.py tools/site/tests/test_terra_tienda_css.py tools/site/tests/test_vercel.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(css): copias minificadas al publicar y terra-tienda.css solo en las páginas de la tienda" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Nodos schema.org de la tienda a `tools/pasto/esquema.py`

Refactor puro: `breadcrumb_schema`, `SHIPPING`, `RETURNS`, `SELLER`, `product_schema` y `strip_tags` salen del módulo de HTML viejo a un módulo de datos que leen las plantillas nuevas. `common.py` los reexporta para `feed.py`, `precios.py` y `zonas.py` (sin cambio en su salida).

**Files:**
- Create: `tools/pasto/esquema.py`
- Modify: `tools/pasto/common.py`

- [ ] **Step 1: Crear `tools/pasto/esquema.py`**

```python
"""Nodos schema.org de la tienda de pasto sintético (Product, BreadcrumbList, envío, devoluciones y vendedor).

Datos, no HTML: los usan las plantillas de tools/site (fichas, hub, ciudades) y las páginas que aún genera
tools/pasto (/precios y zonas, vía common.py) hasta la Etapa 2g.
"""
import re

from data import SITE, WA_NUMBER

GAL = "/img/pasto-sintetico/galeria"


def breadcrumb_schema(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)
        ],
    }


SHIPPING = {
    "@type": "OfferShippingDetails",
    "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX"},
    "deliveryTime": {"@type": "ShippingDeliveryTime",
                     "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
}
RETURNS = {
    "@type": "MerchantReturnPolicy", "applicableCountry": "MX",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 7, "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
}
SELLER = {"@type": "Organization", "name": "Viveros Terra", "url": SITE, "telephone": f"+{WA_NUMBER}"}


def product_schema(m, *, with_id=True):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    props = [
        {"@type": "PropertyValue", "name": "Altura de fibra", "value": m["mm"], "unitText": "mm"},
        {"@type": "PropertyValue", "name": "Peso total", "value": m["peso_num"], "unitText": "g/m²"},
        {"@type": "PropertyValue", "name": "Medida del rollo", "value": "2 × 25 m (50 m²)"},
    ]
    if m["garantia"]:
        props.append({"@type": "PropertyValue", "name": "Garantía", "value": m["garantia"], "unitText": "años"})
    for label, value, unit in m["specstrip"]:
        if label in ("Puntadas por m²", "Dtex"):
            props.append({"@type": "PropertyValue", "name": label, "value": int(value.replace(",", ""))})
    images = [f"{SITE}{GAL}/{m['slug']}-{idx}.webp" for idx, _k, _c in m["gallery"]]
    images.append(f"{SITE}/img/pasto-sintetico/{m['slug']}.jpg")
    desc_plain = strip_tags(m["resumen"])
    product = {
        "@type": "Product", "name": f"Pasto Sintético {m['nombre']}", "sku": f"VT-PST-{m['id'].upper()}",
        "category": "Pasto sintético residencial", "description": desc_plain, "image": images,
        "brand": {"@type": "Brand", "name": "Viveros Terra"}, "color": m["color"], "url": url,
        "additionalProperty": props,
        "offers": {
            "@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(m["rollo"]), "highPrice": str(m["t1"]),
            "offerCount": "3", "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition", "seller": SELLER,
            "shippingDetails": SHIPPING, "hasMerchantReturnPolicy": RETURNS,
        },
    }
    if with_id:
        product["@id"] = f"{url}#producto"
    return product


def strip_tags(html_text):
    return re.sub(r"<[^>]+>", "", html_text)
```

- [ ] **Step 2: `common.py` los toma de ahí**

En `tools/pasto/common.py` borra desde `def breadcrumb_schema(items):` hasta justo antes de `MAX_MM = 35` (las definiciones de `breadcrumb_schema`, `SHIPPING`, `RETURNS`, `SELLER`, `product_schema` y `strip_tags`) y en su lugar escribe:

```python
from esquema import RETURNS, SELLER, SHIPPING, breadcrumb_schema, product_schema, strip_tags  # noqa: E402,F401


```

- [ ] **Step 3: Pruebas y build sin cambios**

```bash
cd ~/dev/viverosterra-e2b/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../.. && python3 tools/site/build.py | tail -2 && git status --porcelain public | wc -l
```

Expected: `OK`; `plantillas: 0 de 2 …`, `shell: 0 de 108 …`; `0` (el HTML publicado no cambia).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/pasto/esquema.py tools/pasto/common.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "refactor(pasto): nodos schema.org de la tienda en esquema.py, sin HTML" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Componentes de la tienda (`componentes_tienda.py`) y dos ajustes en `componentes.py`

**Files:**
- Create: `tools/site/componentes_tienda.py`, `tools/site/tests/test_componentes_tienda.py`
- Modify: `tools/site/componentes.py`, `tools/site/tests/test_componentes.py`

- [ ] **Step 1: Pruebas**

`tools/site/tests/test_componentes_tienda.py`:

```python
"""Componentes de la tienda (tools/site/componentes_tienda.py): marcado que leen tienda-pasto.js y tienda-hub.js,
números de tools/pasto/data.py y mensualidades con la fórmula oficial."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes_tienda as t  # noqa: E402
import data  # noqa: E402
import datos  # noqa: E402

JS = Path(__file__).resolve().parents[3] / "public" / "js"
T28 = data.BY_SLUG["toscana-28"]


def ids(html):
    return set(re.findall(r'\bid="([^"]+)"', html))


class CotizadorTest(unittest.TestCase):
    def test_trae_cada_id_que_busca_tienda_pasto_js(self):
        js = (JS / "tienda-pasto.js").read_text(encoding="utf-8")
        html = (t.cotizador(T28) + t.lista_y_aviso() + t.barra_compra("X", "Desde $1/m²", "Hola", rollo=199)
                + t.json_modelo(T28) + t.json_modelos())
        buscados = set(re.findall(r"\$\('#([\w-]+)'\)", js)) - {"modelo", "gal-track", "gal-count"}
        self.assertEqual(sorted(buscados - ids(html)), [])
        for atributo in ("data-cta-wa", "data-plans", "data-plan-amount", "data-plan-total", "data-trip-contado",
                         "data-trip-mes", "data-trip-total", "data-plan-save", "data-cot-count", "data-toast-text",
                         "data-landed-bar"):
            with self.subTest(atributo=atributo):
                self.assertIn(atributo, html + t.subnav())

    def test_precios_y_estado_inicial_desde_data(self):
        html = t.cotizador(T28)
        self.assertIn('<td id="tier-rollo">$199/m²</td>', html)
        self.assertIn('<td id="tier-t2">$229/m²</td>', html)
        self.assertIn('<td id="tier-t1">$279/m²</td>', html)
        self.assertIn('<b id="q-material">$9,950</b>', html)
        self.assertIn('data-m2="50" aria-pressed="true"', html)
        tampico = t.cotizador(T28, modelos=data.MODELOS, m2=20, showroom=True, nivel=3)
        self.assertIn('<b id="q-material">$4,580</b>', tampico)
        self.assertIn('<option value="showroom" selected>', tampico)
        self.assertEqual(tampico.count('<option value="'), 2 + len(data.MODELOS))
        self.assertIn('<h3 class="vt-cotizador__t"', tampico)

    def test_whatsapp_con_mensaje_y_firma_sin_js(self):
        href = re.search(r'data-cta-wa data-cta="tienda:cotizador" href="([^"]+)"', t.cotizador(T28)).group(1)
        texto = unquote(href.split("text=", 1)[1])
        self.assertTrue(texto.startswith("Hola, quiero cotizar el pasto sintético Toscana 28."))
        self.assertTrue(texto.endswith(datos.FIRMA))

    def test_forma_de_pago_con_los_plazos_oficiales(self):
        html = t.planes_cotizador("q")
        self.assertIn('role="radiogroup"', html)
        for v in ("0", "3", "6", "9", "12"):
            self.assertIn(f'name="q-plan" value="{v}"', html)
        self.assertIn('value="0" checked', html)
        self.assertIn("/politicas#mensualidades", html)
        for prohibida in ("msi", "sin intereses", "0%", "recargo", "comisión"):
            self.assertNotIn(prohibida, html.lower())


class ListaYBarraTest(unittest.TestCase):
    def test_mi_lista_esconde_el_cero(self):
        self.assertIn('data-cot-count data-empty="true">0</span>', t.subnav())
        css = (JS.parent / "css" / "terra-tienda.css").read_text(encoding="utf-8")
        self.assertIn('.vt-tienda .vt-subnav__n[data-empty="true"]{display:none}', css)

    def test_barra_con_precio_puesto_solo_con_rollo(self):
        self.assertIn('data-landed-bar data-rollo="149"', t.barra_compra("T18", "Desde $149/m²", "Hola", rollo=149))
        self.assertNotIn("data-landed-bar", t.barra_compra("Tampico", "Instalado desde $385/m²", "Hola"))
        texto = unquote(re.search(r'href="[^"]+text=([^"]+)"', t.barra_compra("X", "Y", "Hola")).group(1))
        self.assertEqual(texto, datos.con_firma("Hola"))


class CatalogoTest(unittest.TestCase):
    def test_nueve_tarjetas_con_lo_que_lee_tienda_hub(self):
        html = t.catalogo()
        self.assertEqual(html.count('class="spec-card vt-tarjeta-p"'), 9)
        self.assertEqual(html.count("data-add="), 9)
        self.assertEqual(html.count("data-landed-slug="), 9)
        self.assertEqual(html.count('class="vt-regla"'), 9)
        self.assertEqual(html.count('class="vt-tarjeta-p__pago"'), 9)
        self.assertIn('id="filters-count"', html)
        self.assertEqual(html.count("data-filter="), len(data.USO_FILTERS))

    def test_para_llevar_hoy_solo_en_toscana_18_y_28(self):
        hoy = re.findall(r'<span class="vt-tarjeta-p__hoy">([^<]+)</span>', t.catalogo())
        self.assertEqual(hoy, [f"Toscana 18 para llevar hoy · {datos.CALLE_CORTA}",
                               f"Toscana 28 para llevar hoy · {datos.CALLE_CORTA}"])

    def test_regla_de_altura(self):
        self.assertIn('style="--w:100%"', t.regla_altura(35))
        self.assertIn('style="--w:29%"', t.regla_altura(10))
        self.assertIn('aria-label="Altura de fibra: 10 mm"', t.regla_altura(10))

    def test_selector_de_estados_completo(self):
        html = t.selector_estado("hero-estado")
        self.assertIn('<label for="hero-estado"', html)
        for e in data.ESTADOS_ORDEN:
            self.assertIn(f'value="{e}"', html)

    def test_selector_y_comparador(self):
        self.assertIn('id="quiz-result"', t.selector_modelo())
        self.assertEqual(t.selector_modelo().count('type="radio"'), 10)
        for i in ("comparador", "cmp-total", "cmp-m2", "cmp-out"):
            self.assertIn(f'id="{i}"', t.comparador())


class FichaTest(unittest.TestCase):
    def test_galeria_principal_nunca_lazy(self):
        html = t.galeria(T28)
        primera = re.search(r"<img [^>]+>", html).group(0)
        self.assertIn('loading="eager" fetchpriority="high"', primera)
        self.assertEqual(html.count("gallery__slide"), len(T28["gallery"]))
        self.assertIn("<b>Fig. 01</b>", html)
        self.assertEqual(t.foto_principal(T28)["src"], re.search(r'src="([^"]+)"', primera).group(1))

    def test_vecinos_y_agregar_con_sus_precios(self):
        html = t.comparativa(T28)
        self.assertEqual([m["slug"] for m in t.vecinos(T28)], ["irlanda-25", "viena-30"])
        self.assertEqual([m["slug"] for m in t.vecinos(data.MODELOS[0])], ["toscana-18", "capri-20"])
        agregar = [json.loads(b.replace("&quot;", '"')) for b in re.findall(r'data-agregar="([^"]+)"', html)]
        self.assertEqual([a["slug"] for a in agregar], ["irlanda-25", "toscana-28", "viena-30"])
        self.assertEqual(agregar[1], t.datos_modelo_js(T28))
        self.assertIn('aria-current="page"', html)

    def test_rollo_a_escala_de_50_m2(self):
        html = t.rollo_escala()
        for cota in ("25 m", "2 m", "50 m²"):
            self.assertIn(f">{cota}</text>", html)

    def test_existencia_nacional_y_para_llevar_hoy(self):
        for m in data.MODELOS:
            html = t.existencia(m)
            with self.subTest(modelo=m["slug"]):
                self.assertIn("En existencia", html)
                self.assertEqual("para llevar hoy" in html, m["slug"] in ("toscana-18", "toscana-28"))


class CiudadTest(unittest.TestCase):
    def test_totales_25_50_100_con_las_reglas_del_cotizador(self):
        aruba = data.BY_SLUG["aruba-10"]
        self.assertEqual(t.totales(aruba, "B"), [(25, 25 * 159 + 1150), (50, 50 * 139 + 1150), (100, 100 * 139 + 2300)])

    def test_mensualidad_maxima_con_la_formula_oficial(self):
        self.assertEqual(t.mensualidad_maxima(16200), "12 × ≈ $1,667")
        self.assertEqual(t.mensualidad_maxima(5125), "6 × ≈ $981")
        self.assertEqual(t.mensualidad_maxima(1500), "—")
        html = t.tabla_totales(t.barato(), "B")
        self.assertIn("$16,200", html)
        self.assertIn("$162/m²", html)
        self.assertIn("En mensualidades", html)


if __name__ == "__main__":
    unittest.main()
```

En `tools/site/tests/test_componentes.py`, agrega a la clase `BloquesTest`:

```python
    def test_etiqueta_sin_nombre_cientifico_y_opciones_con_su_mensaje(self):
        e = {"codigo": "Sintético · 05/09", "aviso": "Con IVA", "nombre": "Toscana 28", "antes": "desde",
             "monto": "$199", "unidad": "/m²"}
        self.assertNotIn("vt-etiqueta__sci", c.etiqueta(e))
        self.assertIn('<p class="vt-etiqueta__sci">X y</p>', c.etiqueta(dict(e, cientifico="X y")))
        items = ({"rotulo": "Opción 1", "titulo": "A", "precio": 139, "unidad": "/m²", "detalle": "d", "puntos": ("p",),
                  "mensaje": "Hola A"},
                 {"rotulo": "Opción 2", "titulo": "B", "precio": 385, "unidad": "/m²", "detalle": "d", "puntos": ("q",),
                  "mensaje": "Hola B", "rec": True, "nota": "n"})
        html = c.opciones(items, "servicio-sintetico")
        self.assertEqual(re.findall(r'data-cta="([^"]+)"', html), ["servicio-sintetico:opcion-1", "servicio-sintetico:opcion-2"])
        self.assertIn('<li class="vt-modo vt-modo--rec">', html)
        self.assertIn('<span class="vt-precio-marca">$385</span>', html)
        self.assertEqual([unquote(t).split("\n")[0] for t in re.findall(r"text=([^\"&]+)", html)], ["Hola A", "Hola B"])
```

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_componentes_tienda.py tests/test_componentes.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'componentes_tienda'` y `FAILED`.

- [ ] **Step 2: `componentes.py`: etiqueta sin científico y `opciones()`**

En `etiqueta()`, después de la línea `nota = …` agrega `sci = f'<p class="vt-etiqueta__sci">{e["cientifico"]}</p>' if e.get("cientifico") else ""` y cambia `f'<p class="vt-etiqueta__nombre">{e["nombre"]}</p><p class="vt-etiqueta__sci">{e["cientifico"]}</p>'` por `f'<p class="vt-etiqueta__nombre">{e["nombre"]}</p>{sci}'` (el pasto sintético no tiene nombre científico y Fraunces es solo para eso).

Antes de `def relacionados(items):` agrega:

```python
def opciones(items, tipo):
    """Formas de contratar (máx. 3, spec §3.3), cada una con su precio "desde", lo que incluye, su nota y su propio
    mensaje de WhatsApp. items: rotulo, titulo, precio (número), unidad, detalle, puntos, nota, mensaje, rec."""
    filas = []
    for i, o in enumerate(items, 1):
        clase = "vt-modo vt-modo--rec" if o.get("rec") else "vt-modo"
        puntos = "".join(f"<li>{x}</li>" for x in o["puntos"])
        nota_html = f'<p class="vt-promesa">{o["nota"]}</p>' if o.get("nota") else ""
        filas.append(f'<li class="{clase}"><p class="vt-modo__n">{o["rotulo"]}</p><h3>{o["titulo"]}</h3>'
                     f'<p class="vt-modo__precio">desde <span class="vt-precio-marca">{dinero(o["precio"])}</span> '
                     f'{o["unidad"]} <small>{o["detalle"]}</small></p><ul class="vt-checks">{puntos}</ul>{nota_html}'
                     f'{boton_wa(o["mensaje"], f"{tipo}:opcion-{i}")}</li>')
    return f'<ul class="vt-modos">{"".join(filas)}</ul>'


```

- [ ] **Step 3: Crear `tools/site/componentes_tienda.py`**

```python
"""Componentes de la tienda de pasto sintético (Etapa 2b): cotizador por estado, forma de pago, lista de cotización,
barra de compra, tarjetas del catálogo, galería, ficha técnica, rollo a escala, comparativa y tablas de envío.

El marcado conserva los id, clases y data-* que leen public/js/tienda-pasto.js y public/js/tienda-hub.js (esos dos
archivos no se reescriben): #m2, #estado, #modelo, #cta-add, [data-cta-wa], #q-*, [data-plans], #cotizacion,
#cot-send, #toast, #buybar, .spec-card, [data-add], [data-filter], #quiz, #comparador, [data-landed-*]. Todo número
sale de tools/pasto/data.py (modelos, zonas y fletes) o de datos.py; la fórmula de mensualidades es la de
tools/pasto/mensualidades.py. Las clases propias llevan prefijo vt-; las que crea o busca el JS se estilan solo bajo
body.vt-tienda (public/css/terra-tienda.css).
"""
import json

import componentes as c
import datos
import data
import mensualidades
from partials import WA_GLIFO, esc

GAL = "/img/pasto-sintetico/galeria"
MAX_MM = 35
ROLLO_M2 = data.ROLLO_M2
MIN_NACIONAL = 25
MIN_SHOWROOM = 2
TIERS = (("rollo", "Rollo completo", f"{ROLLO_M2} m² o más"), ("t2", "Corte mediano", "10 a 49 m²"),
         ("t1", "Corte chico", "2 a 9 m², solo en showroom"))
NOTA_FLETE = "Te confirmamos el flete exacto a tu dirección antes de pagar."
TARIFAS = tuple(data.ZONAS[z] for z in sorted(data.ZONAS))
TARIFAS_TEXTO = f"{c.dinero(TARIFAS[0])}, {c.dinero(TARIFAS[1])} o {c.dinero(TARIFAS[2])}"


def modelo(slug):
    return data.BY_SLUG[slug]


def barato(modelos=None):
    return min(modelos or data.MODELOS, key=lambda m: m["rollo"])


def garantia_texto(m):
    return f"{str(m['garantia']).replace(' a ', '–')} años" if m["garantia"] else "Consultar"


def img_textura(m):
    return f"{GAL}/{m['slug']}-2-sm.webp"


# ---------- datos para el JS ----------
def datos_modelo_js(m):
    """Lo que tienda-pasto.js necesita de un modelo para cotizarlo y agregarlo a la lista."""
    return {"slug": m["slug"], "nombre": m["nombre"], "img": img_textura(m), "t1": m["t1"], "t2": m["t2"],
            "rollo": m["rollo"]}


def json_modelo(m):
    """<script type="application/json" id="vt-model"> de la ficha (tienda-pasto.js lo lee)."""
    return (f'<script type="application/json" id="vt-model">{json.dumps(datos_modelo_js(m), ensure_ascii=False)}'
            "</script>")


def json_modelos(modelos=None, completo=False):
    """id="vt-models" del hub (con scores, tag y mm para el selector) o de la página de Tampico."""
    filas = []
    for m in modelos or data.MODELOS:
        fila = {"slug": m["slug"]}
        if completo:
            fila["id"] = m["id"]
        fila.update({"nombre": m["nombre"], "img": img_textura(m), "t1": m["t1"], "t2": m["t2"], "rollo": m["rollo"]})
        if completo:
            fila.update({"scores": m["scores"], "tag": m["tag"], "mm": m["mm"]})
        filas.append(fila)
    return f'<script type="application/json" id="vt-models">{json.dumps(filas, ensure_ascii=False)}</script>'


# El mismo script en línea que publicaba tools/pasto/ficha.py: pinta [data-landed-slug] con el precio puesto del estado.
SCRIPT_PRECIO_PUESTO = (
    '<script>document.addEventListener("vt:ready",function(){var t=window.VTTienda,L=window.VTLanded;if(!t||!L)return;'
    'function p(e){document.querySelectorAll("[data-landed-slug]").forEach(function(el){var m=t.models.find(function(x){return x.slug===el.dataset.landedSlug});'
    'var v=m&&e?L.landedM2(m.rollo,e,t.estadoZona,t.zonas):null;el.textContent=v?"$"+v.toLocaleString("es-MX")+"/m² puesto en "+e:"";});}'
    'p(t.getEstado());document.addEventListener("vt:estado",function(ev){p(ev.detail.estado||"")});});</script>')


# ---------- piezas pequeñas ----------
def regla_altura(mm):
    """Altura de fibra contra el máximo de la colección (35 mm)."""
    pct = c.redondear(mm / MAX_MM * 100)
    return (f'<div class="vt-regla" role="img" aria-label="Altura de fibra: {mm} mm"><span class="vt-regla__pista">'
            f'<span class="vt-regla__fill" style="--w:{pct}%"></span></span><span class="vt-regla__val">{mm}'
            f'<small>mm</small></span></div>')


def chip_mm(mm):
    return f'<span class="vt-chip-mm" aria-hidden="true">{mm}<small>mm</small></span>'


def existencia(m):
    """Línea de existencia: los 9 en existencia nacional; para llevar hoy solo Toscana 18 y 28 (stock en data.py)."""
    hoy = (f'<span>{esc(m["nombre"])} para llevar hoy en el showroom de {datos.CALLE_CORTA}</span>'
           if m["stock"] else "")
    return f'<p class="vt-existencia"><span>En existencia · envío a todo México en 3 a 5 días hábiles</span>{hoy}</p>'


def subnav():
    """Barra de la tienda bajo el menú: atajos y "Mi lista (n)"; el (0) no se ve con la lista vacía."""
    return ('<nav class="vt-subnav" aria-label="Tienda de pasto sintético"><div class="vt-wrap vt-subnav__bar">'
            '<a href="/pasto-sintetico#modelos">Los 9 modelos</a><a href="/pasto-sintetico#elegir">¿Cuál me conviene?</a>'
            '<a href="/pasto-sintetico#como-funciona">Cómo comprar</a>'
            '<button class="vt-subnav__lista" type="button" data-open-cot aria-haspopup="dialog">Mi lista '
            '<span class="vt-subnav__n" data-cot-count data-empty="true">0</span></button></div></nav>')


def selector_estado(id_select, etiqueta="Envíalo a"):
    """Select de estados (orden de data.ESTADOS_ORDEN); tienda-hub.js lo sincroniza con el cotizador."""
    opciones = "".join(f'<option value="{esc(e)}">{esc(e)}</option>' for e in data.ESTADOS_ORDEN)
    return (f'<div class="vt-campo"><label for="{esc(id_select)}">{esc(etiqueta)}</label><div class="vt-control">'
            f'<select id="{esc(id_select)}" data-estado-select><option value="">Elige tu estado</option>{opciones}'
            '</select></div></div>')


# ---------- cotizador (marcado de tienda-pasto.js) ----------
def tabla_tiers(m):
    filas = "".join(f'<tr data-tier="{k}"><th scope="row">{t}<span>{d}</span></th><td id="tier-{k}">'
                    f'{c.dinero(m[k])}/m²</td></tr>' for k, t, d in TIERS)
    return f'<table class="vt-tiers"><caption>Precio por volumen</caption><tbody>{filas}</tbody></table>'


def planes_cotizador(prefijo):
    """Forma de pago: contado o 3, 6, 9 y 12 mensualidades con tarjeta de crédito. tienda-pasto.js llena montos y
    disponibilidad con VTMensualidades (fórmula oficial)."""
    opciones = [("0", "Contado", "Transferencia, efectivo o tarjeta en una exhibición")] + [
        (str(n), f"{n} mensualidades", "Con tarjeta de crédito") for n in mensualidades.PLAZOS]
    filas = "".join(
        f'<label class="plan" data-plan="{v}"><input type="radio" name="{prefijo}-plan" value="{v}"'
        f'{" checked" if v == "0" else ""}><span class="vt-plan__n">{esc(n)}<small>{esc(s)}</small></span>'
        f'<span class="vt-plan__monto" data-plan-amount></span><span class="vt-plan__total" data-plan-total></span></label>'
        for v, n, s in opciones)
    return (f'<fieldset class="vt-planes-t" id="{prefijo}-plans" data-plans><legend id="{prefijo}-plans-legend">'
            '¿Cómo prefieres pagar?</legend>'
            f'<dl class="vt-planes-t__trip" id="{prefijo}-plan-trip" aria-live="polite"><div><dt>Contado</dt>'
            '<dd data-trip-contado>—</dd></div><div><dt>Al mes</dt><dd data-trip-mes>—</dd></div><div><dt>Total</dt>'
            f'<dd data-trip-total>—</dd></div></dl><div class="pay-rule" id="{prefijo}-plan-rule" aria-hidden="true"></div>'
            f'<div class="vt-planes-t__lista" role="radiogroup" aria-labelledby="{prefijo}-plans-legend">{filas}</div>'
            '<p class="vt-planes-t__ahorro" data-plan-save></p>'
            '<p class="vt-planes-t__nota">Precio en mensualidades con tarjeta de crédito. Contado (transferencia, '
            'efectivo o tarjeta en una exhibición) es el precio más bajo. Montos aproximados: tu banco debe aceptar el '
            'plan. Te confirmamos el total antes de enviarte el link de pago. <a href="/politicas#mensualidades">'
            'Condiciones</a></p></fieldset>')


def _selector_modelo(modelos, elegido):
    opciones = "".join(f'<option value="{m["slug"]}"{" selected" if m is elegido else ""}>{esc(m["nombre"])} · '
                       f'desde ${m["rollo"]}/m²</option>' for m in modelos)
    return (f'<div class="vt-campo vt-campo--ancho"><label for="modelo">Modelo</label><div class="vt-control">'
            f'<select id="modelo">{opciones}</select></div></div>')


def cotizador(m, *, modelos=None, m2=ROLLO_M2, showroom=False, titulo="Cotiza tu corte", id_titulo="vt-h-cotizar",
              nivel=2, mensaje=None, tipo="tienda"):
    """Cotizador de tienda-pasto.js. m: modelo inicial; con `modelos`, agrega el selector #modelo (hub y Tampico).
    showroom=True preselecciona "Recoger en showroom" (Tampico). Envío nacional bajo 25 m²: el JS bloquea total y
    mensualidades (J03 §3). El botón de WhatsApp lleva desde el HTML un mensaje con firma (sin JS no queda vacío)."""
    pm2 = m["rollo"] if m2 >= ROLLO_M2 else (m["t2"] if m2 >= 10 else m["t1"])
    material = pm2 * m2
    texto = mensaje or (f"Hola, quiero cotizar el pasto sintético {m['nombre']}.\nNecesito ___ m².\n"
                        "Mi estado: ___")
    href = esc(datos.wa_url(datos.con_firma(texto)))
    chips = "".join(f'<button class="vt-chip" type="button" data-m2="{n}" aria-pressed="{"true" if n == m2 else "false"}">'
                    f'{n} m²</button>' for n in (MIN_NACIONAL, ROLLO_M2, ROLLO_M2 * 2))
    sel_showroom = " selected" if showroom else ""
    selector = _selector_modelo(modelos, m) if modelos else ""
    return (
        f'<section class="vt-cotizador" id="comprar" aria-labelledby="{id_titulo}"><h{nivel} class="vt-cotizador__t" '
        f'id="{id_titulo}">{titulo}</h{nivel}>'
        f'<p class="vt-cotizador__desde">Desde <b id="buy-price">{c.dinero(m["rollo"])}</b>/m² · rollo de {ROLLO_M2} m², '
        'IVA incluido · envío por rollo según tu estado</p>'
        f'{selector}<div class="vt-campo"><label for="m2">Metros cuadrados</label><div class="vt-stepper">'
        '<button type="button" id="m2-minus" aria-label="Restar 5 m²">−</button><input id="m2" type="number" '
        f'inputmode="numeric" min="{MIN_SHOWROOM}" max="5000" step="1" value="{m2}">'
        '<button type="button" id="m2-plus" aria-label="Sumar 5 m²">+</button></div>'
        f'<div class="vt-chips" role="group" aria-label="Medidas rápidas">{chips}</div></div>'
        '<div class="vt-campo"><label for="estado">Entrega</label><div class="vt-control"><select id="estado">'
        f'<option value="">Selecciona tu estado</option><option value="showroom"{sel_showroom}>Recoger en showroom, '
        'Cd. Madero</option></select></div></div>'
        f'{tabla_tiers(m)}'
        '<div class="vt-cuenta" aria-live="polite">'
        f'<p class="vt-cuenta__fila"><span>Precio aplicado</span><b id="q-pm2">{c.dinero(pm2)}/m²</b></p>'
        f'<p class="vt-cuenta__fila"><span>Material</span><b id="q-material">{c.dinero(material)}</b></p>'
        '<p class="vt-cuenta__fila"><span id="q-envio-label">Envío</span><b id="q-envio">Elige tu estado</b></p>'
        f'<p class="vt-cuenta__total"><span id="q-total-label">Total estimado</span><b id="q-total">'
        f'{c.dinero(material)}</b></p><p class="vt-cuenta__puesto" id="q-landed"></p>'
        '<p class="vt-cuenta__pista" id="q-hint"></p><p class="vt-cuenta__error" id="q-error" role="alert"></p></div>'
        f'{planes_cotizador("q")}'
        f'<div class="vt-cotizador__acciones"><a class="vt-btn vt-btn--wa" data-cta-wa data-cta="{tipo}:cotizador" '
        f'href="{href}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<button class="vt-btn vt-btn--linea" type="button" id="cta-add">Agregar a mi cotización</button>'
        f'<p class="vt-promesa">{NOTA_FLETE} {esc(datos.PROMESA_COMPLETA)}.</p></div></section>')


# ---------- lista de cotización, aviso y barra de compra ----------
def lista_y_aviso():
    """<dialog id="cotizacion"> (tienda-pasto.js arma los renglones y el mensaje con todos los modelos de la lista) y
    el aviso "<modelo> en tu lista · Ver"."""
    return (
        '<dialog class="vt-lista" id="cotizacion" aria-labelledby="cot-titulo"><div class="vt-lista__in">'
        '<div class="vt-lista__cabeza"><h2 id="cot-titulo">Tu lista</h2><button class="vt-lista__cerrar" type="button" '
        'id="cot-close" aria-label="Cerrar">×</button></div><div class="vt-lista__cuerpo" id="cot-list"></div>'
        '<div class="vt-lista__pie" id="cot-foot" hidden><div class="vt-campo"><label for="cot-estado">Entrega</label>'
        '<div class="vt-control"><select id="cot-estado"><option value="">Selecciona tu estado</option>'
        '<option value="showroom">Recoger en showroom, Cd. Madero</option></select></div></div>'
        '<p class="vt-cuenta__total"><span id="cot-total-label">Total estimado del material</span><b id="cot-total">$0</b>'
        f'</p><a class="vt-btn vt-btn--wa" id="cot-send" data-cta="tienda:lista" href="https://wa.me/{datos.TELEFONO_WA}" '
        f'target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>'
        '<p class="vt-promesa">Precio estimado. Confirmamos el flete exacto con tu dirección.</p></div></div></dialog>'
        '<div class="vt-aviso" id="toast" role="status" data-visible="false"><span data-toast-text></span>'
        '<button type="button" data-open-cot>Ver</button></div>')


def barra_compra(nombre, precio, mensaje, *, rollo=None):
    """#buybar fija en celular mientras el cotizador (#comprar) queda arriba. Con rollo, tienda-pasto.js cambia el
    precio al puesto en el estado elegido."""
    puesto = f' data-landed-bar data-rollo="{rollo}"' if rollo else ""
    href = esc(datos.wa_url(datos.con_firma(mensaje)))
    return (f'<div class="vt-compra" id="buybar" data-visible="false"{puesto}><div class="buybar__info">'
            f'<div class="buybar__name">{esc(nombre)}</div><div class="buybar__price">{esc(precio)}</div></div>'
            f'<a class="vt-btn vt-btn--wa" data-cta-wa data-cta="tienda:barra" href="{href}" target="_blank" '
            f'rel="noopener">{WA_GLIFO}Cotizar</a></div>')


# ---------- catálogo del hub ----------
def tarjeta(m):
    """Tarjeta del catálogo: foto con la altura, etiqueta S con el precio, regla de altura, precio puesto y Agregar."""
    url = f"/pasto-sintetico/{m['slug']}"
    hoy = (f'<span class="vt-tarjeta-p__hoy">{esc(m["nombre"])} para llevar hoy · {datos.CALLE_CORTA}</span>'
           if m["stock"] else "")
    return (
        f'<article class="spec-card vt-tarjeta-p" data-usos="{" ".join(m["usos"])}" id="m-{m["slug"]}">'
        f'<a class="vt-tarjeta-p__foto" href="{url}" tabindex="-1" aria-hidden="true"><img src="{img_textura(m)}" '
        f'width="420" height="560" alt="" loading="lazy" decoding="async">{chip_mm(m["mm"])}{hoy}</a>'
        f'<div class="vt-tarjeta-p__cuerpo"><p class="vt-tarjeta-p__tag">N.º {m["n"]:02d} · {esc(m["tag"])}</p>'
        f'<h3 class="spec-card__name"><a href="{url}">{esc(m["nombre"])}</a></h3>{regla_altura(m["mm"])}'
        f'<dl class="vt-tarjeta-p__datos"><div><dt>Peso</dt><dd>{m["peso"]} g/m²</dd></div><div><dt>Garantía</dt>'
        f'<dd>{garantia_texto(m)}</dd></div></dl>'
        f'<p class="vt-tarjeta-p__precio">Desde <b>${m["rollo"]}</b>/m² <span class="vt-tarjeta-p__puesto" '
        f'data-landed-slug="{m["slug"]}"></span></p>'
        '<p class="vt-tarjeta-p__pago">Paga en mensualidades con tarjeta de crédito</p>'
        f'<button class="spec-card__add vt-btn vt-btn--linea" type="button" data-add="{m["slug"]}" '
        f'aria-label="Agregar {esc(m["nombre"])} a mi cotización">+ Agregar</button></div></article>')


def filtros(opciones=data.USO_FILTERS):
    chips = "".join(f'<button class="vt-chip" type="button" data-filter="{k}" '
                    f'aria-pressed="{"true" if k == "todos" else "false"}">{esc(t)}</button>' for k, t in opciones)
    return (f'<div class="vt-filtros" role="group" aria-label="Filtrar por uso">{chips}</div>'
            f'<p class="vt-filtros__n" id="filters-count" aria-live="polite">{len(data.MODELOS)} modelos</p>')


def catalogo(modelos=None):
    return f'{filtros()}<div class="vt-catalogo">{"".join(tarjeta(m) for m in modelos or data.MODELOS)}</div>'


QUIZ = (
    ("donde", "¿Dónde va?", (("jardin", "Jardín"), ("terraza", "Terraza o balcón"), ("patio", "Patio o alberca"))),
    ("uso", "¿Quién lo pisa?", (("familia", "La familia, a diario"), ("perros", "Perros"),
                                ("poco", "Casi nadie, es decorativo"), ("intenso", "Mucha gente, uso intenso"))),
    ("prioridad", "¿Qué te importa más?", (("equilibrio", "Equilibrio"), ("precio", "El mejor precio"),
                                           ("realismo", "Que se vea lo más natural"))),
)


def selector_modelo():
    """#quiz de tienda-hub.js: tres preguntas y dos recomendaciones."""
    grupos = "".join(
        f'<fieldset class="vt-opciones"><legend>{esc(leyenda)}</legend>'
        + "".join(f'<label><span>{esc(t)}</span><input type="radio" name="{nombre}" value="{v}"'
                  f'{" checked" if i == 0 else ""}></label>' for i, (v, t) in enumerate(ops))
        + "</fieldset>" for nombre, leyenda, ops in QUIZ)
    return (f'<form class="vt-quiz" id="quiz" aria-describedby="quiz-help"><p class="vt-lede" id="quiz-help">Tres '
            'preguntas y te recomendamos dos modelos. Cambia las respuestas y la recomendación se actualiza.</p>'
            f'{grupos}<div class="vt-quiz__res" id="quiz-result" aria-live="polite"></div></form>')


def comparador():
    """#comparador de tienda-hub.js: precio por m² de otra oferta contra el puesto en tu estado."""
    return ('<form class="vt-comparador" id="comparador" novalidate><div class="vt-campo"><label for="cmp-total">Total '
            'de la otra oferta, con envío</label><div class="vt-control"><input id="cmp-total" type="number" '
            'inputmode="decimal" min="1" placeholder="Ej. 14899"><span>MXN</span></div></div><div class="vt-campo">'
            '<label for="cmp-m2">Metros cuadrados que incluye</label><div class="vt-control"><input id="cmp-m2" '
            'type="number" inputmode="numeric" min="1" placeholder="Ej. 50"><span>m²</span></div></div>'
            '<p class="vt-comparador__res" id="cmp-out" aria-live="polite">Escribe el total y los metros para comparar '
            'con nuestro precio puesto en tu estado.</p></form>')


def tabla_modelos(modelos=None):
    filas = tuple((f'<a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}</a><br><small>{esc(m["tag"])}</small>',
                   f'{m["mm"]} mm', m["peso"], garantia_texto(m), f'<b>${m["rollo"]}</b>', esc(m["ideal"]))
                  for m in modelos or data.MODELOS)
    return c.tabla_comparativa(("Modelo", "Altura", "Peso g/m²", "Garantía", "Rollo /m²", "Ideal para"), filas,
                               "Los 9 modelos por altura, peso, garantía y precio por rollo.")


def tabla_envio():
    """Flete por zona: 1 y 2 rollos (data.ZONA_ESTADOS y data.ZONAS)."""
    filas = tuple((f"Zona {z}<br><small>{esc(nombre)}</small>", esc(", ".join(estados)),
                   f"<b>{c.dinero(data.ZONAS[z])}</b>", c.dinero(data.ZONAS[z] * 2))
                  for z, (nombre, estados) in data.ZONA_ESTADOS.items())
    return c.tabla_comparativa(("Zona", "Estados", "1 rollo", "2 rollos"), filas,
                               "Costo de envío de pasto sintético por estado, con IVA.")


def zonas_envio():
    """Las tres tarifas por rollo, cada una con sus estados principales (bloque de envío de la ficha)."""
    celdas = "".join(f'<div><dt>{c.dinero(data.ZONAS[z])}<small> /rollo</small></dt><dd><b>{esc(nombre)}.</b> '
                     f'{esc(", ".join(estados[:6]))} y más.</dd></div>' for z, (nombre, estados) in data.ZONA_ESTADOS.items())
    return f'<dl class="vt-zonas-envio">{celdas}</dl>'


# ---------- ficha ----------
ALT = {
    "rollo": "Rollo de pasto sintético {n} desenrollado, con la base arriba y la fibra {color}",
    "textura": "Acercamiento a la fibra del pasto sintético {n} de {mm} mm en {color}",
    "base": "Base del pasto sintético {n} junto a la fibra, vista a ras de suelo",
    "instalado": "Pasto sintético {n} instalado: {caption}",
}


def foto_principal(m):
    """La primera foto de la galería: se precarga y nunca es lazy (J03)."""
    base = f"{GAL}/{m['slug']}-{m['gallery'][0][0]}"
    return {"src": f"{base}-sm.webp", "srcset": f"{base}-sm.webp 420w, {base}.webp 720w",
            "sizes": "(min-width: 1024px) 620px, 100vw"}


def galeria(m):
    """Galería con scroll y miniaturas (#gal-track, .gallery__slide, [data-gal-idx], #gal-count de tienda-pasto.js);
    cada foto con pie FIG."""
    total = len(m["gallery"])
    diapos, minis = [], []
    for i, (idx, tipo, pie) in enumerate(m["gallery"]):
        base = f"{GAL}/{m['slug']}-{idx}"
        alt = ALT[tipo].format(n=m["nombre"], color=m["color"].lower(), mm=m["mm"], caption=pie.lower())
        carga = 'loading="eager" fetchpriority="high"' if i == 0 else 'loading="lazy"'
        diapos.append(f'<figure class="gallery__slide vt-fig"><div class="vt-fig__marco"><img src="{base}-sm.webp" '
                      f'srcset="{base}-sm.webp 420w, {base}.webp 720w" sizes="(min-width: 1024px) 620px, 100vw" '
                      f'width="720" height="960" alt="{esc(alt)}" {carga} decoding="async">'
                      f'{chip_mm(m["mm"]) if i == 0 else ""}</div><figcaption><span><b>Fig. {i + 1:02d}</b> · '
                      f'{esc(pie)}</span><span>Foto de producto</span></figcaption></figure>')
        minis.append(f'<button class="vt-galeria__mini" type="button" data-gal-idx="{i}" aria-label="Ver foto '
                     f'{i + 1}: {esc(pie.lower())}"><img src="{base}-sm.webp" alt="" width="64" height="64" '
                     'loading="lazy"></button>')
    return (f'<section class="vt-galeria" aria-label="Fotos del {esc(m["nombre"])}"><div class="vt-galeria__pista" '
            f'id="gal-track" tabindex="0">{"".join(diapos)}</div><div class="vt-galeria__meta"><span '
            f'class="vt-galeria__n" id="gal-count" aria-live="polite">01 / {total:02d}</span><div '
            f'class="vt-galeria__minis">{"".join(minis)}</div></div></section>')


def datos_modelo(m):
    """Cuadro de datos con las cuatro cifras de la ficha (specstrip de data.py)."""
    return c.cuadro_datos(tuple((t, v, u) for t, v, u in m["specstrip"]))


GLOSARIO = (
    ("Dtex", "Grosor del hilo. A más Dtex, fibra más gruesa y resistente al pisoteo."),
    ("Puntadas por m²", "Cuántos mechones hay en cada metro. A más puntadas, menos se ve la base."),
    ("Fibra de soporte", "El rizo café de abajo. Mantiene de pie la fibra verde y da el look natural."),
    ("Base", "Malla y látex que sujetan cada mechón. Una base más pesada alarga la vida del pasto."),
)
NOTA_FICHA = ("Datos de la ficha técnica del fabricante. Entre paréntesis va la norma con la que se mide cada dato. "
              "Las tolerancias son las de fábrica.")


def ficha_tecnica(m):
    grupos = "".join(
        f'<div class="vt-tecnica__g"><h3>{esc(titulo)}</h3><dl>'
        + "".join(f'<div><dt>{esc(e)}{f"<small>{esc(n)}</small>" if n else ""}</dt><dd>{esc(v)}</dd></div>'
                  for e, n, v in filas) + "</dl></div>" for titulo, filas in m["specs"])
    nota = m.get("specs_note") or NOTA_FICHA
    glosario = "" if m.get("specs_note") else (
        '<dl class="vt-glosario">' + "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in GLOSARIO) + "</dl>")
    return f'<div class="vt-tecnica">{grupos}</div><p class="vt-promesa">{esc(nota)}</p>{glosario}'


def rollo_escala():
    """Un rollo dibujado a escala: 25 m × 2 m = 50 m² (cotas solo donde hay medida real)."""
    return ('<figure class="vt-fig vt-rollo"><svg viewBox="0 0 480 120" role="img" aria-label="Un rollo de pasto '
            'sintético a escala: 25 metros de largo por 2 de ancho, 50 metros cuadrados">'
            '<rect class="vt-plano-relleno" x="40" y="52" width="400" height="32"/>'
            '<rect class="vt-plano-borde" x="40" y="52" width="400" height="32"/>'
            '<path class="vt-cota" d="M40 26 v14 M440 26 v14 M40 33 H440"/>'
            '<text class="vt-cota-t" x="240" y="22" text-anchor="middle">25 m</text>'
            '<path class="vt-cota" d="M452 52 h14 M452 84 h14 M459 52 V84"/>'
            '<text class="vt-cota-t" x="472" y="104" text-anchor="end">2 m</text>'
            '<text class="vt-cota-a" x="240" y="74" text-anchor="middle">50 m²</text></svg>'
            '<figcaption><span><b>Así llega</b> · rollo de 2 m de ancho</span><span>Cotas en metros</span>'
            '</figcaption></figure>')


def vecinos(m):
    """Dos modelos vecinos por altura (los mismos que publicaba tools/pasto/ficha.py)."""
    i = data.MODELOS.index(m)
    if i == 0:
        return [data.MODELOS[1], data.MODELOS[2]]
    if i == len(data.MODELOS) - 1:
        return [data.MODELOS[i - 2], data.MODELOS[i - 1]]
    return [data.MODELOS[i - 1], data.MODELOS[i + 1]]


def comparativa(m):
    """El modelo y sus dos vecinos, cada uno con su etiqueta S y su botón Agregar (data-add: van en el mismo mensaje)."""
    tarjetas = []
    for x in sorted([m] + vecinos(m), key=lambda z: z["n"]):
        actual = x is m
        actual_attr = ' aria-current="page"' if actual else ""
        nombre = f'<a href="/pasto-sintetico/{x["slug"]}"{actual_attr}>{esc(x["nombre"])}</a>'
        tarjetas.append(
            f'<article class="vt-vecino{" vt-vecino--actual" if actual else ""}"><div class="vt-vecino__foto"><img '
            f'src="{img_textura(x)}" width="420" height="560" alt="Textura del pasto sintético {esc(x["nombre"])}" '
            f'loading="lazy" decoding="async">{chip_mm(x["mm"])}</div>'
            f'<p class="vt-vecino__tag">{"Estás viendo" if actual else esc(x["tag"])}</p><h3>{nombre}</h3>'
            f'<dl><div><dt>Altura</dt><dd>{x["mm"]} mm</dd></div><div><dt>Peso</dt><dd>{x["peso"]} g/m²</dd></div>'
            f'<div><dt>Garantía</dt><dd>{garantia_texto(x)}</dd></div></dl>'
            f'<p class="vt-vecino__precio">Desde <b>${x["rollo"]}</b>/m²</p><button class="vt-btn vt-btn--linea" '
            f'type="button" data-agregar="{esc(json.dumps(datos_modelo_js(x), ensure_ascii=False))}">+ Agregar · '
            '1 rollo</button></article>')
    return (f'<div class="vt-vecinos">{"".join(tarjetas)}</div>'
            '<p class="vt-promesa"><a href="/pasto-sintetico#modelos">Ver los 9 modelos</a></p>')


# ---------- ciudades ----------
def totales(m, zona):
    """Material + flete para 25, 50 y 100 m² (reglas del cotizador: 25 m² usa el precio de corte mediano)."""
    salida = []
    for m2 in (MIN_NACIONAL, ROLLO_M2, ROLLO_M2 * 2):
        precio = m["rollo"] if m2 >= ROLLO_M2 else m["t2"]
        rollos = -(-m2 // ROLLO_M2)
        salida.append((m2, m2 * precio + rollos * data.ZONAS[zona]))
    return salida


def mensualidad_maxima(total):
    """El plazo más largo que aplica al total y su mensualidad (fórmula oficial), o "—"."""
    disponibles = [p for p in mensualidades.planes(total) if p["disponible"]]
    if not disponibles:
        return "—"
    p = disponibles[-1]
    return f'{p["plazo"]} × ≈ {c.dinero(p["mensualidad"])}'


def tabla_totales(m, zona):
    filas = tuple((f"{m2} m²", c.dinero(total), f"{c.dinero(total / m2)}/m²", mensualidad_maxima(total))
                  for m2, total in totales(m, zona))
    return c.tabla_comparativa(("Metros", "Total con envío", "Por m²", "En mensualidades"), filas,
                               f"Ejemplo con {esc(m['nombre'])}, el modelo más económico. Material más flete, IVA "
                               "incluido.")


def modelos_recomendados(items, zona=None, lugar=""):
    """Tres modelos con su regla de altura y la razón; con zona, el precio puesto en la ciudad; sin zona, el precio
    del rollo y el puesto según el estado elegido (data-landed-slug)."""
    tarjetas = []
    for slug, razon in items:
        m = modelo(slug)
        if zona:
            precio = f'Desde <b>${data.landed_m2(m, zona)}</b>/m² puesto en {esc(lugar)}'
        else:
            precio = f'Desde <b>${m["rollo"]}</b>/m² <span data-landed-slug="{m["slug"]}"></span>'
        tarjetas.append(f'<li class="vt-recomendado"><h3><a href="/pasto-sintetico/{m["slug"]}">{esc(m["nombre"])}'
                        f'</a></h3>{regla_altura(m["mm"])}<p>{esc(razon)}</p><p class="vt-recomendado__precio">'
                        f'{precio}</p></li>')
    return f'<ul class="vt-recomendados">{"".join(tarjetas)}</ul>'


def ciudades_destacadas(ciudades):
    m = barato()
    filas = "".join(f'<li><a href="/pasto-sintetico/envio/{x["slug"]}"><b>{esc(x["nombre"])}</b><span>desde '
                    f'${data.landed_m2(m, data.zona_de(x["estado"]))}/m² puesto</span><span>3 a 5 días hábiles</span>'
                    '</a></li>' for x in ciudades)
    return f'<ul class="vt-ciudades">{filas}</ul>'


def preguntas_h3(items):
    """Encabezados en pregunta con su respuesta corta (h3 + párrafo): costo, tiempo, mínimo, cómo elegir sin muestra
    e instalación en las ciudades; criterios en la página de perros."""
    filas = "".join(f'<li class="vt-recomendado"><h3>{q}</h3><p>{a}</p></li>' for q, a in items)
    return f'<ul class="vt-recomendados">{filas}</ul>'
```

(`data-agregar` lo atiende `tienda-pasto.js` desde la Tarea 8; hasta entonces el botón no hace nada, pero ninguna página lo publica todavía.)

- [ ] **Step 4: Correr**

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_componentes_tienda.py tests/test_componentes.py tests/test_terra_tienda_css.py 2>&1 | tail -1`
Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/componentes_tienda.py tools/site/componentes.py tools/site/tests/test_componentes_tienda.py tools/site/tests/test_componentes.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(tienda): componentes con el marcado de tienda-pasto.js y tienda-hub.js" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: `tienda-pasto.js`: lo agregado viaja también en el WhatsApp del cotizador

J01: lo que se agrega desde las tarjetas no llegaba al mensaje del botón del cotizador (solo al de la lista, `#cot-send`). Dos cambios chicos y nada más del archivo: (1) los botones `data-agregar` (comparativa de la ficha, cada uno con su modelo en JSON) agregan a la lista; (2) cada escritura de la lista avisa con `vt:lista` y el cotizador rehace su mensaje con "También en mi lista: …". Se prueba en navegador en la Tarea 14 (el archivo no tiene pruebas de Node porque depende del DOM).

**Files:**
- Modify: `public/js/tienda-pasto.js`

- [ ] **Step 1: Avisar cuando cambia la lista**

En `writeStore`, después de `renderCount();` agrega `document.dispatchEvent(new CustomEvent('vt:lista'));` (queda dentro de la función, antes de su `}`).

- [ ] **Step 2: Botones `data-agregar`**

Antes de `  /* ---------- Quote module (ficha y hub) ---------- */` agrega:

```js
  /* Botones "+ Agregar" de la comparativa de la ficha: cada uno trae su modelo en data-agregar (JSON). */
  function initAgregar() {
    $$('[data-agregar]').forEach((btn) => btn.addEventListener('click', () => {
      try {
        const model = JSON.parse(btn.dataset.agregar);
        if (isValidModel(model)) addItem(model, ROLLO_M2);
        else console.error('[tienda] Botón de agregar sin precios completos:', btn.dataset.agregar);
      } catch (err) {
        console.error('[tienda] Botón de agregar con datos inválidos:', err.message);
      }
    }));
  }

```

y en el `DOMContentLoaded`, después de `initBuybar();`, agrega `initAgregar();`.

- [ ] **Step 3: "También en mi lista" en el mensaje del cotizador**

En `update()` de `initQuote`, reemplaza

```js
      const msg = [
        `Hola, quiero cotizar el pasto sintético ${model.nombre}.`,
        Number.isFinite(m2) ? `Necesito ${m2} m².` : '',
```

por

```js
      const otros = memoryState.items.filter((it) => it.slug !== model.slug);
      const msg = [
        `Hola, quiero cotizar el pasto sintético ${model.nombre}.`,
        Number.isFinite(m2) ? `Necesito ${m2} m².` : '',
        otros.length ? `También en mi lista: ${otros.map((it) => `${it.nombre} (${it.m2} m²)`).join(', ')}.` : '',
```

y después de `    initPlanInputs(update);` agrega:

```js
    // Lo que se agrega a la lista (tarjetas, vecinos, selector) viaja también en el mensaje del cotizador.
    document.addEventListener('vt:lista', update);
```

- [ ] **Step 4: Sintaxis, pruebas que ya existen y commit**

```bash
cd ~/dev/viverosterra-e2b
node --check public/js/tienda-pasto.js && echo sintaxis-ok
cd tools/pasto && python3 -m unittest tests.test_paridad_js 2>&1 | tail -1
cd ../site && python3 -m unittest tests/test_navegador.py 2>&1 | tail -1
cd ../.. && git add public/js/tienda-pasto.js
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(tienda): lo que se agrega a la lista viaja también en el WhatsApp del cotizador" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `sintaxis-ok`; `OK`; `OK` (incluye `test_cotizador_de_la_tienda_manda_el_lead_con_cta_y_servicio` y la consola limpia en las 108 páginas).

---

### Task 9: Las 9 fichas salen de su plantilla

**Files:**
- Modify: `tools/site/plantillas/base.py`, `tools/site/generar.py`, `tools/pasto/build.py`
- Create: `tools/site/plantillas/ficha.py`, `tools/site/contenido/ficha.py`, `tools/site/tests/test_tienda.py`
- Regenerate: `public/pasto-sintetico/<modelo>/index.html` (9)

- [ ] **Step 1: Pruebas de las fichas publicadas**

`tools/site/tests/test_tienda.py` (crece en las Tareas 10–12):

```python
"""Las 25 páginas de pasto sintético publicadas desde sus plantillas: secuencia del spec §3.3, sin CSS viejo, scripts de
la tienda, precio en el primer pantallazo, existencia, JSON-LD y reglas del dueño en lo que cambió en 2b."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
import data  # noqa: E402
import datos  # noqa: E402
import generar  # noqa: E402
import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
TIENDA = [r for r, _a, p, _c in generar.PAGINAS if r.startswith("/pasto-sintetico")]
VIEJOS = ("tienda-pasto.css", "fonts.googleapis", "tailwind.css", "design-system.css", "legacy-fixes", "Geist",
          "Instrument Serif")


def html(ruta):
    return (PUBLIC / ruta.strip("/") / "index.html").read_text(encoding="utf-8")


def principal(texto):
    return re.search(r"<main\b[^>]*>(.*)</main>", texto, re.S).group(1)


def grafo(texto):
    return [n for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', texto, re.S)
            for n in json.loads(b)["@graph"]]


class TiendaPublicadaTest(unittest.TestCase):
    def test_sin_css_viejo_con_terra_tienda(self):
        for ruta in TIENDA:
            texto = html(ruta)
            with self.subTest(ruta=ruta):
                for viejo in VIEJOS:
                    self.assertNotIn(viejo, texto)
                self.assertIn('<body class="vt-pagina vt-tienda">', texto)
                self.assertRegex(texto, r'<link rel="stylesheet" href="/css/terra-tienda\.[0-9a-f]{10}\.css">')
                self.assertNotIn("<style", texto)

    def test_ficha_con_etiqueta_existencia_y_galeria_precargada(self):
        for m in data.MODELOS:
            texto = html(f"/pasto-sintetico/{m['slug']}")
            cuerpo = principal(texto)
            with self.subTest(modelo=m["slug"]):
                self.assertIn(f"Rollo de 50 m² · desde</small><b>${m['rollo']}</b>", cuerpo)
                self.assertIn("por rollo, según tu estado", cuerpo)
                self.assertIn("En existencia", cuerpo)
                self.assertEqual("para llevar hoy" in cuerpo, bool(m["stock"]))
                primera = f"/img/pasto-sintetico/galeria/{m['slug']}-{m['gallery'][0][0]}-sm.webp"
                self.assertIn(f'<link rel="preload" as="image" href="{primera}"', texto)
                self.assertRegex(cuerpo, rf'<img src="{re.escape(primera)}"[^>]*loading="eager" fetchpriority="high"')
                self.assertLess(cuerpo.index("vt-etiqueta__precio"), cuerpo.index("vt-galeria"))
                self.assertIn(f'data-landed-slug="{m["slug"]}"', cuerpo)

    def test_secuencia_de_la_ficha(self):
        cuerpo = principal(html("/pasto-sintetico/toscana-28"))
        orden = ['id="vt-h1"', 'class="vt-galeria"', 'id="comprar"', "Para quién es el Toscana 28",
                 "Ficha técnica del Toscana 28", 'class="vt-fig vt-rollo"', "Compara el Toscana 28",
                 "El envío se cobra por rollo", "Garantía de 5 años en el Toscana 28", "Preguntas sobre el Toscana 28",
                 "vt-cierre"]
        posiciones = [cuerpo.index(x) for x in orden]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_feed_de_merchant_sin_cambios_de_precio(self):
        feed = (PUBLIC / "feed-pasto-sintetico.xml").read_text(encoding="utf-8")
        for m in data.MODELOS:
            self.assertIn(f"<g:link>{data.SITE}/pasto-sintetico/{m['slug']}</g:link>", feed)
            self.assertIn(f"<g:price>{m['rollo']:.2f} MXN</g:price>", feed)

    def test_scripts_de_la_ficha_en_orden(self):
        self.assertEqual(re.findall(r'<script src="/js/([\w-]+)\.js" defer>', html("/pasto-sintetico/toscana-28")),
                         ["vt-mensualidades", "tienda-pasto", "vt-landed"])


if __name__ == "__main__":
    unittest.main()
```

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -3`
Expected: `FAILED` (las fichas todavía cargan `tienda-pasto.css` y no tienen `vt-tienda`; `TIENDA` está vacía, así que solo fallan las pruebas de ficha).

- [ ] **Step 2: Documento base con datos para el JS, marcado fuera de `<main>` y clase del body**

En `tools/site/plantillas/base.py`, reemplaza la firma y el docstring de `documento` por:

```python
def documento(meta, cuerpo, *, jsonld_bloques=(), precargas=(), scripts=(), head_extra=(), tras_main="",
              clase_body="vt-pagina"):
    """meta: title, description, robots, canonical, og (pares en el orden publicado) y, opcionales, alternos
    (hreflang, href) y twitter (pares name/content de la Twitter Card). head_extra: líneas después del JSON-LD (datos
    para el JS de la tienda). tras_main: marcado fijo fuera de <main> (lista de cotización, aviso y barra de compra).
    clase_body "vt-pagina vt-tienda" hace que el shell agregue terra-tienda.css."""
```

después de `lineas += [jsonld(b) for b in jsonld_bloques]` agrega `lineas += list(head_extra)`; cambia `'<body class="vt-pagina">',` por `f'<body class="{escape(clase_body)}">',`; y después de la lista que termina en `"<!-- vt:footer -->", "<!-- /vt:footer -->",\n    ]` agrega:

```python
    if tras_main:
        lineas.append(tras_main)
```

- [ ] **Step 3: Contenido y plantilla de la ficha**

`tools/site/contenido/ficha.py`:

```python
"""Contenido de las 9 fichas /pasto-sintetico/<modelo>. Solo datos: la plantilla es tools/site/plantillas/ficha.py.

Cada ficha sale de tools/pasto/data.py (MODELOS): aquí no se escribe ningún precio ni dato técnico. Título,
descripción, canonical, Open Graph, Product, BreadcrumbList y preguntas son los que publicaba tools/pasto/ficha.py;
FAQPage sale de las preguntas visibles. PARIDAD: tests/test_paridad.py (captura de cada ficha antes de migrar).
"""
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
from componentes import dinero
from esquema import breadcrumb_schema, product_schema

CLAVES = tuple(m["slug"] for m in data.MODELOS)
SITE = data.SITE
INSTALAR = ("Sí. Sobre tierra compactada se fija con clavos cada 20 a 30 cm. Sobre concreto se pega con adhesivo de "
            "contacto. Te mandamos la guía de instalación con el pedido.")
DEVOLVER = ("Sí, dentro de 7 días, nuevo y sin cortar. Los cortes a medida no tienen devolución. El envío de regreso lo "
            "paga el cliente.")
ENTREGA = ("Llega en 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo. El mínimo para envío "
           "nacional es 25 m². En el showroom de Cd. Madero puedes comprar desde 2 m².")
PASOS = (
    {"titulo": "Cotiza aquí", "quien": "tu", "cuando": "Hoy",
     "texto": "Pon tus m² y tu estado. Mándanos la cotización por WhatsApp."},
    {"titulo": "Confirmamos el flete", "quien": "nosotros", "cuando": "En menos de 1 hora en horario",
     "texto": "Con tu dirección te damos el precio final. Sin sorpresas."},
    {"titulo": "Pagas y facturamos", "quien": "juntos", "cuando": "Al confirmar",
     "texto": f"Transferencia o link de pago con tarjeta. Factura {datos.FACTURA}."},
    {"titulo": "Recibes en 3 a 5 días", "quien": "nosotros", "cuando": "3 a 5 días hábiles",
     "texto": "Llega por paquetería con guía de rastreo y guía de instalación."},
)


def preguntas(m):
    """Las 7 preguntas que publicaba la ficha, con sus enlaces (pares pregunta, respuesta en HTML en línea)."""
    precio = (f"Cuesta ${m['rollo']}/m² en rollo completo de 50 m², ${m['t2']}/m² de 10 a 49 m² y ${m['t1']}/m² en "
              "cortes de 2 a 9 m² en el showroom de Cd. Madero. Los precios incluyen IVA. El envío se cobra por rollo "
              f"según el estado: de {dinero(min(data.ZONAS.values()))} a {dinero(max(data.ZONAS.values()))}.")
    extra = [list(par) for par in m["faq_extra"]]
    if m["slug"] == "viena-30":
        extra[0][1] = extra[0][1].replace("En el blog explicamos cómo manejar el calor.",
                                          'En el blog explicamos <a href="/blog/pasto-sintetico-calor-mexico">cómo '
                                          "manejar el calor</a>.")
    return (
        (f"¿Cuánto cuesta el pasto sintético {m['nombre']}?", precio),
        tuple(extra[0]),
        (f"¿El {m['nombre']} sirve para perros y niños?", m["mascotas"]),
        ("¿Cuánto tarda en llegar y cuál es el pedido mínimo?", ENTREGA),
        tuple(extra[1]),
        ("¿Lo puedo instalar yo?", f'{INSTALAR} Aquí está la <a href="/blog/como-instalar-pasto-sintetico">guía paso a '
                                   "paso</a>."),
        ("¿Puedo devolverlo?", f'{DEVOLVER} Consulta la <a href="/politicas">política de envíos y devoluciones</a>.'),
    )


def _fotos(m):
    """Foto grande de la sección de fotos (instalado o de cerca) y la del rollo, con pie FIG."""
    instaladas = [(i, cap) for i, k, cap in m["gallery"] if k == "instalado"]
    if instaladas:
        idx, cap = instaladas[0]
        titulo, rotulo = f"{m['nombre']} instalado", "Instalado"
        principal = {"src": f"{t.GAL}/{m['slug']}-{idx}.webp", "alt": f"Pasto sintético {m['nombre']} instalado: "
                     f"{cap.lower()}", "lugar": f"{cap}. {m['nombre']} instalado", "etapa": "Foto de producto"}
    else:
        idx = next(i for i, k, _c in m["gallery"] if k == "textura")
        titulo, rotulo = f"{m['nombre']} de cerca", "De cerca"
        principal = {"src": f"{t.GAL}/{m['slug']}-{idx}.webp", "alt": f"Acercamiento a la fibra del pasto sintético "
                     f"{m['nombre']}", "lugar": "Detalle de la fibra, sin retoque", "etapa": "Foto de producto"}
    figuras = (
        dict(principal, ancho=720, alto=960, numero=1),
        {"src": f"{t.GAL}/{m['slug']}-rollo.webp", "ancho": 564, "alto": 452, "numero": 2,
         "alt": f"Rollo de {m['nombre']} abierto sobre el piso antes de instalar",
         "lugar": "Así llega: rollo de 2 m de ancho", "etapa": "Antes de instalar"},
    )
    return {"titulo": titulo, "rotulo": rotulo, "figuras": figuras}


def _meta(m, url):
    gar = f"garantía de {m['garantia']} años" if m["garantia"] else "uso decorativo"
    titulo = f"Pasto Sintético {m['nombre']} desde ${m['rollo']}/m² · Envío a Todo México"
    descripcion = (f"{m['nombre']}: {m['mm']} mm, {m['peso']} g/m² y {gar}. Desde ${m['rollo']}/m² en rollo, con factura "
                   "y envío a todo México en 3 a 5 días.")
    primera = f"{t.GAL}/{m['slug']}-{m['gallery'][0][0]}"
    return {
        "title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
        "canonical": url,
        "og": (("og:type", "product"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
               ("og:description", descripcion), ("og:image", f"{SITE}{primera}.webp"), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    }


def contenido(m):
    url = f"{SITE}/pasto-sintetico/{m['slug']}"
    insignia = f' <span class="vt-ficha__insignia">{m["badge"]}</span>' if m.get("badge") else ""
    gar = f"Garantía de {m['garantia']} años" if m["garantia"] else "Garantía de fábrica"
    return {
        "tipo": "tienda",
        "modelo": m,
        "meta": _meta(m, url),
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", f"{SITE}/pasto-sintetico"),
                                      (m["nombre"], url)]), product_schema(m)),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (m["nombre"], None)),
        "kicker": f"Pasto sintético · N.º {m['n']:02d} de 09 · {m['tag']}",
        "h1": f'<span class="vt-ficha__pre">Pasto sintético</span> {m["nombre"]}{insignia}',
        "lede": m["lede"],
        "etiqueta": {
            "codigo": f"Sintético · {m['n']:02d}/09", "aviso": "Con IVA", "nombre": m["nombre"],
            "antes": f"Rollo de {data.ROLLO_M2} m² · desde", "monto": dinero(m["rollo"]), "unidad": "/m²",
            "filas": (("Envío", "por rollo, según tu estado"), ("Mínimo nacional", "25 m²"),
                      ("En showroom", "desde 2 m²")),
            "nota": f'<span data-landed-slug="{m["slug"]}" aria-live="polite"></span>',
        },
        "para_quien": {"titulo": f"Para quién es el {m['nombre']}", "resumen": m["resumen"],
                       "si": m["fit_si"], "no": m["fit_no"], "nota": (m["mascotas"], "Con niños y mascotas")},
        "ficha": {"titulo": f"Ficha técnica del {m['nombre']}"},
        "fotos": _fotos(m),
        "compara": {"titulo": f"Compara el {m['nombre']} con modelos similares",
                    "lede": "Agrega los que quieras a tu lista: van todos en un solo mensaje de WhatsApp."},
        "pedido": {"titulo": f"Cómo comprar el {m['nombre']}", "titulo_envio": "El envío se cobra por rollo, según tu "
                   "estado.", "lede": (f"Un rollo son {data.ROLLO_M2} m²: si pides 100 m² son dos rollos y dos fletes. "
                                       f"Nunca va escondido en el precio: {t.TARIFAS_TEXTO} por rollo. Con tu código "
                                       "postal te damos el precio final antes de pagar."),
                   "pasos": PASOS},
        "garantia": {
            "titulo": f"{gar} en el {m['nombre']}.", "grande": str(m["garantia"]).replace(" a ", "–") if m["garantia"]
            else "—", "unidad": "años" if m["garantia"] else "", "resumen": "Garantía de fábrica; la gestionamos nosotros.",
            "puntos": (("Garantía de fábrica contra defectos del material, gestionada por nosotros.", True),
                       ("Devolución dentro de 7 días, nuevo y sin cortar.", True),
                       (f"Factura {datos.FACTURA} para persona física o moral.", True),
                       ("Los cortes a medida no tienen devolución; el envío de regreso lo paga el cliente.", False)),
            "pie": ('<a href="/politicas#devoluciones">Política de envíos y devoluciones</a> · '
                    '<a href="/politicas">Políticas y garantías</a>')},
        "faq": {"titulo": f"Preguntas sobre el {m['nombre']}", "preguntas": preguntas(m)},
        "cierre": {"titulo": f"Cotiza tu {m['nombre']} con envío a tu estado",
                   "lede": "Mándanos tus metros y tu estado. Te respondemos con el precio final y la fecha de entrega.",
                   "mensaje": f"Hola, quiero cotizar el pasto sintético {m['nombre']}.\nMi estado: ___\nMetros aprox.: ___"},
        "barra": {"nombre": f"{m['nombre']}{' · ' + m['badge'] if m.get('badge') else ''}",
                  "precio": f"Desde ${m['rollo']}/m²", "rollo": m["rollo"]},
    }


def pagina(slug):
    return SimpleNamespace(CONTENIDO=contenido(data.BY_SLUG[slug]), PARIDAD=PARIDAD)


PARIDAD = {"reemplazos": {}, "retirados": {}}
```

`tools/site/plantillas/ficha.py`:

```python
"""Plantilla de ficha de tienda (spec §3.3): ruta visible → nombre, "En existencia" y etiqueta "desde $X/m² · rollo
50 m² · envío por rollo según estado" en el primer pantallazo → galería (foto principal precargada, nunca lazy) →
cotizador (estado, m², precio puesto, mensualidades) → para quién es → ficha técnica → fotos y rollo a escala →
comparativa con 2 vecinos → envío por rollo y cómo comprar → garantía del modelo → preguntas → CTA final.
Contenido: tools/site/contenido/ficha.py (desde tools/pasto/data.py). JS: tienda-pasto.js, vt-landed.js."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js")


def _portada(k):
    m = k["modelo"]
    info = (f'<div class="vt-ficha__info"><p class="vt-kicker">{k["kicker"]}</p><h1 id="vt-h1">{k["h1"]}</h1>'
            f'{t.existencia(m)}{c.etiqueta(k["etiqueta"], cordel=False)}<p class="vt-lede">{k["lede"]}</p>'
            f'{t.datos_modelo(m)}</div>')
    cotizador = t.cotizador(m, titulo=f"Precio y cotización del {m['nombre']}", tipo=k["tipo"])
    return (f'<section class="vt-ficha" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-ficha__grid">{info}{t.galeria(m)}{cotizador}</div></div></section>')


def _para_quien(k, n):
    p = k["para_quien"]
    checks = "".join(f"<li>{x}</li>" for x in p["si"]) + "".join(f'<li class="vt-checks__no">{x}</li>' for x in p["no"])
    izquierda = f'<p class="vt-lede">{p["resumen"]}</p>{c.nota(*p["nota"])}'
    return c.bloque_dos(n, "En resumen", "vt-h-resumen", p["titulo"], izquierda, f'<ul class="vt-checks">{checks}</ul>')


def _fotos(k, n):
    f = k["fotos"]
    cuerpo = f'<div class="vt-obras">{"".join(c.figura(x) for x in f["figuras"])}</div>{t.rollo_escala()}'
    return c.bloque(n, f["rotulo"], "vt-h-fotos", f["titulo"], cuerpo)


def _pedido(k, n):
    p = k["pedido"]
    cuerpo = (f'<h3>{p["titulo_envio"]}</h3><p class="vt-lede">{p["lede"]}</p>{t.zonas_envio()}'
              f'{c.pasos(p["pasos"])}')
    return c.bloque(n, "Tu pedido", "vt-h-pedido", p["titulo"], cuerpo, id_seccion="como-funciona")


def render(k):
    m, f, ci, b = k["modelo"], k["faq"], k["cierre"], k["barra"]
    secciones = (
        _portada(k),
        _para_quien(k, 1),
        c.bloque(2, "Ficha técnica", "vt-h-ficha", k["ficha"]["titulo"], t.ficha_tecnica(m), tinte=True,
                 id_seccion="ficha-tecnica"),
        _fotos(k, 3),
        c.bloque(4, "Compáralo", "vt-h-compara", k["compara"]["titulo"], t.comparativa(m), lede=k["compara"]["lede"],
                 tinte=True),
        _pedido(k, 5),
        c.garantia(dict(k["garantia"], numero=6, id_titulo="vt-h-garantia", rotulo="Garantía")),
        c.bloque_dos(7, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"])),
        c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]),
    )
    grafo = list(k["jsonld"]) + [c.faq_jsonld(f["preguntas"])]
    fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], ci["mensaje"], rollo=b["rollo"])
    return base.documento(k["meta"], t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(t.foto_principal(m)),),
                          head_extra=(t.json_modelo(m), t.SCRIPT_PRECIO_PUESTO), tras_main=fuera, scripts=SCRIPTS,
                          clase_body="vt-pagina vt-tienda")
```

- [ ] **Step 4: Registrar las fichas y dejar de generarlas en `tools/pasto`**

En `tools/site/generar.py`, el cierre de `PAGINAS`

```python
    ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
)
```

pasa a

```python
    ("/pasto-en-rollo-tampico", "pasto-en-rollo-tampico/index.html", "servicio", "pasto_en_rollo"),
) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha")
```

En `tools/pasto/build.py` borra `from ficha import build_ficha` y las dos líneas `for m in MODELOS:` / `write(ROOT / m["slug"] / "index.html", build_ficha(m))`.

- [ ] **Step 5: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2 && python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe $(python3 -c "import sys; sys.path[:0]=['tools/pasto']; from data import MODELOS; print(' '.join('/pasto-sintetico/'+m['slug'] for m in MODELOS))") | grep -vc ": ok"
cd tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1
python3 -m unittest tests/test_paridad.py tests/test_contenido.py tests/test_generar.py tests/test_reglas.py tests/test_consistencia.py tests/test_sitio.py 2>&1 | tail -1
```

Expected: primera corrida `plantillas: 9 de 11 páginas escritas`; segunda `plantillas: 0 de 11 …` y `shell: 0 de 108 …`; `9` (solo las 9 líneas `== /pasto-sintetico/…`: las seis categorías en `ok` en todas; `PARIDAD` de las fichas va vacío porque cada encabezado, pregunta, precio y enlace se conservó); `OK`; `OK`.

Revisa a mano a 375 y 1440 (`python3 -m http.server -d public 8765`): kicker, H1 "Pasto sintético / Toscana 28 REFORZADO", existencia (y "para llevar hoy" solo en Toscana 18 y 28), etiqueta con "Rollo de 50 m² · desde $199 /m²" y envío por rollo en el primer pantallazo móvil; galería con pie `FIG. 01`; cotizador; a 1440 la galería a la izquierda (fija al bajar) y la info y el cotizador a la derecha.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2b
git status --short | grep -v '\.html$'
git add tools/site/plantillas/base.py tools/site/plantillas/ficha.py tools/site/contenido/ficha.py tools/site/generar.py tools/site/tests/test_tienda.py tools/pasto/build.py public/pasto-sintetico
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(ficha): las 9 fichas de sintético salen de su plantilla con etiqueta, galería precargada y comparativa" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: El hub `/pasto-sintetico` sale de su plantilla

**Files:**
- Create: `tools/site/plantillas/tienda_hub.py`, `tools/site/contenido/tienda.py`
- Modify: `tools/site/generar.py`, `tools/pasto/build.py`, `tools/site/tests/test_tienda.py`, `tools/site/tests/test_reglas.py`
- Regenerate: `public/pasto-sintetico/index.html`

- [ ] **Step 1: Pruebas del hub**

Agrega a `TiendaPublicadaTest` en `tools/site/tests/test_tienda.py`:

```python
    def test_hub_con_precio_puesto_catalogo_y_lista(self):
        texto = html("/pasto-sintetico")
        cuerpo = principal(texto)
        self.assertIn('data-landed-hero data-rollo="139"', cuerpo)
        self.assertIn('id="hero-estado"', cuerpo)
        self.assertEqual(cuerpo.count('class="spec-card vt-tarjeta-p"'), 9)
        self.assertIn('id="vt-models"', texto)
        self.assertIn('<dialog class="vt-lista" id="cotizacion"', texto)
        self.assertNotIn("gratis", cuerpo.lower())
        lista = next(n for n in grafo(texto) if n["@type"] == "ItemList")
        self.assertEqual(len(lista["itemListElement"]), 9)

    def test_vendemos_a_todo_mexico_desde_2012(self):
        self.assertIn(f"desde {datos.SINTETICO_NACIONAL_DESDE}", principal(html("/pasto-sintetico")))
```

En `tools/site/tests/test_reglas.py`, `PERMITIDAS = ('anuncian "envío gratis"',)  # …` pasa a:

```python
PERMITIDAS = ()  # 2b: el hub ya no cita el "envío gratis" de otras ofertas; no se agregan excepciones
```

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1; python3 -m unittest tests/test_reglas.py 2>&1 | tail -1`
Expected: `FAILED` en las dos (el hub viejo no tiene `data-landed-hero data-rollo="139"` en `<p class="vt-precio-puesto"…>` ni `<dialog class="vt-lista"`, y todavía dice "envío gratis").

- [ ] **Step 2: Contenido y plantilla del hub**

`tools/site/contenido/tienda.py`:

```python
"""Contenido del hub /pasto-sintetico (tienda nacional). Solo datos: la plantilla es tools/site/plantillas/tienda_hub.py.

Modelos, zonas y fletes salen de tools/pasto/data.py y las ciudades de tools/pasto/ciudades.py. Título, descripción,
canonical, Open Graph, ItemList de Product y migas son los que publicaba tools/pasto/hub.py; FAQPage sale de las
preguntas visibles. PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from ciudades import CIUDADES
from componentes import dinero
from contenido.ficha import PASOS
from esquema import breadcrumb_schema, product_schema

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico"
BARATO = t.barato()
DEFAULT = data.BY_SLUG["toscana-28"]
DESDE = dinero(BARATO["rollo"])
FLETE_MIN = dinero(min(data.ZONAS.values()))
TITULO = f"Pasto Sintético con Envío a Todo México · Desde {DESDE}/m² | Viveros Terra"
DESCRIPCION = (f"Pasto sintético con envío a todo México desde {DESDE}/m². 9 modelos residenciales de 10 a 35 mm, factura "
               f"{datos.FACTURA} y entrega en 3 a 5 días hábiles.")
GAL = t.GAL

PREGUNTAS = (
    ("¿Cuánto cuesta el pasto sintético con envío?",
     f"El material cuesta de {DESDE} a {dinero(max(m['rollo'] for m in data.MODELOS))}/m² en rollo, según el modelo. El "
     f"envío se suma por rollo según tu estado: {dinero(data.ZONAS['A'])} en Centro y Occidente, "
     f"{dinero(data.ZONAS['B'])} en Norte, Golfo y Sur, y {dinero(data.ZONAS['C'])} en Sureste y fronteras. El cotizador "
     'de esta página calcula tu total estimado. Más detalle en la <a href="/blog/cuanto-cuesta-pasto-sintetico-mexico">'
     "guía de precios</a>."),
    ("¿Cuál es la compra mínima?",
     "Para envío nacional el mínimo es 25 m², medio rollo. En el showroom de Cd. Madero puedes comprar desde 2 m² sin "
     "flete."),
    ("¿Cuánto tarda el envío?",
     "De 3 a 5 días hábiles después de confirmar tu pago, según el destino. Te compartimos la guía de rastreo."),
    ("¿Cómo pago?",
     "Por transferencia bancaria o con link de pago con tarjeta de débito o crédito. El pedido se embarca al confirmar el "
     "pago."),
    ("¿Dan factura?", f"Sí. Emitimos factura {datos.FACTURA} para persona física o moral en todos los pedidos."),
    ("¿Qué modelo me conviene?",
     "Toscana 28 es el más vendido para jardines familiares. Para poco uso o presupuesto ajustado, Toscana 18. Para "
     "perros y pisoteo diario, Irlanda 25 o Capri 20. Para el look más natural, los de 35 mm: Japonés, Mónaco y Bali."),
    ("¿Puedo instalarlo yo mismo?",
     "Sí. Un jardín de 25 a 50 m² se instala en un día. Te mandamos la guía de instalación con el pedido. En Tampico, "
     "Madero y Altamira también ofrecemos instalación profesional. Aquí está la "
     '<a href="/blog/como-instalar-pasto-sintetico">guía paso a paso</a>.'),
    ("¿Qué incluye un rollo?",
     "Un rollo mide 2 m de ancho por 25 m de largo: 50 m². Puedes pedir desde 25 m² y te enviamos el corte."),
    ("¿Hacen instalación fuera de Tampico?",
     "A nivel nacional enviamos solo el material, con guía de instalación. La instalación profesional es solo en "
     "Tampico, Ciudad Madero y Altamira."),
)

DIY = (
    {"titulo": "Nivela y compacta", "quien": "tu", "cuando": "Paso 1",
     "texto": "Retira el pasto viejo, empareja el terreno y compáctalo."},
    {"titulo": "Base drenante", "quien": "tu", "cuando": "Paso 2",
     "texto": "Extiende y compacta grava fina o polvo de piedra para que drene."},
    {"titulo": "Extiende y clava", "quien": "tu", "cuando": "Paso 3",
     "texto": "Coloca el rollo, déjalo reposar, corta a medida y fija el perímetro."},
    {"titulo": "Une los tramos", "quien": "tu", "cuando": "Paso 4",
     "texto": "Junta los rollos con cinta de unión y adhesivo, con la fibra en la misma dirección."},
    {"titulo": "Cepilla", "quien": "tu", "cuando": "Paso 5",
     "texto": "Cepilla a contrapelo para levantar la fibra y darle aspecto natural."},
)

OBRAS = tuple({"src": f"{GAL}/{n}-sm.webp", "srcset": f"{GAL}/{n}-sm.webp 560w, {GAL}/{n}.webp 960w",
               "sizes": "(min-width: 1024px) 400px, 80vw", "ancho": w, "alto": h, "alt": alt, "numero": i,
               "lugar": cap, "etapa": "Obra con pasto sintético"}
              for i, (n, w, h, alt, cap) in enumerate(data.OBRAS, 2))

CONTENIDO = {
    "tipo": "tienda",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large", "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", f"{SITE}{GAL}/obra-residencial-tampico.webp"),
               ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "jsonld": (
        breadcrumb_schema([("Inicio", SITE), ("Pasto Sintético", URL)]),
        {"@type": "ItemList", "name": "Modelos de pasto sintético residencial con envío a todo México",
         "numberOfItems": len(data.MODELOS),
         "itemListElement": [{"@type": "ListItem", "position": i, "item": product_schema(m)}
                             for i, m in enumerate(data.MODELOS, 1)]},
    ),
    "migas": (("Inicio", "/"), ("Pasto sintético", None)),
    "portada": {
        "kicker": "Tienda · Envío a todo México",
        "existencia": f"{len(data.MODELOS)} modelos en existencia · vendemos a todo México desde "
                      f"{datos.SINTETICO_NACIONAL_DESDE}",
        "h1": 'Pasto sintético <span class="vt-serif">con envío a todo México</span>',
        "rotulo_estado": "Precio puesto en tu puerta",
        "rollo": BARATO["rollo"],
        "nota_precio": f"+ envío desde {FLETE_MIN} por rollo. Elige tu estado para ver el precio puesto.",
        "mensualidades": 'Paga en mensualidades con tarjeta de crédito. <a href="#cotizador">Calcula tu plan</a>',
        "foto": {"src": f"{GAL}/obra-proyecto-03-sm.webp", "srcset": f"{GAL}/obra-proyecto-03-sm.webp 560w, "
                 f"{GAL}/obra-proyecto-03.webp 960w", "sizes": "(min-width: 1024px) 620px, 100vw", "ancho": 960,
                 "alto": 1280, "numero": 1, "alt": "Residencia con palmas y jardín de pasto sintético instalado",
                 "lugar": "Residencia con palmas", "etapa": "Proyecto con pasto de la colección"},
        "datos": (("Respuesta", "Menos de 1 hora", datos.HORARIO), ("Garantía", "3 a 8 años", "De fábrica, según el modelo"),
                  ("Devoluciones", "7 días", "Nuevo y sin cortar"), ("Factura", datos.FACTURA, "Persona física o moral"),
                  ("Envío nacional", f"Desde {datos.SINTETICO_NACIONAL_DESDE}", "3 a 5 días hábiles"),
                  ("Showroom", datos.CALLE_CORTA, f"Vivero desde {datos.DESDE}")),
        "mensaje": datos.MENSAJES["pasto-sintetico"],
    },
    "modelos": {"titulo": "Modelos de pasto sintético de 10 a 35 mm",
                "lede": ("Ordenados por altura. A más altura y peso, más volumen y realismo. Todos se venden por rollo de "
                         "2 × 25 m con envío a todo México.")},
    "elegir": {"titulo": "¿Qué pasto sintético te conviene?"},
    "comparar": {"titulo": "¿Viste otro precio? Compáralo aquí",
                 "lede": ("Hay ofertas que esconden el flete en el precio por m². Compara el precio final, puesto en tu "
                          "casa, contra el nuestro en tu estado.")},
    "cotizador": {"titulo": "Precio del pasto sintético con envío a tu estado", "titulo_cotizador": "Cotizador",
                  "titulo_calculo": "Cómo se calcula",
                  "calculo": ("Material: m² por el precio del volumen que pidas",
                              f"Envío por rollo: {t.TARIFAS_TEXTO} según tu estado",
                              "Con 50 m² o más pagas precio de rollo completo",
                              "El flete exacto se confirma con tu dirección"),
                  "titulo_envio": "Costo de envío por estado",
                  "lede_envio": ("El envío se cobra por rollo de 50 m². Un pedido de 25 a 50 m² viaja en 1 rollo; de 51 a "
                                 "100 m², en 2. En Tampico, Madero y Altamira puedes recoger en el showroom sin flete."),
                  "nota_envio": "Te confirmamos el costo exacto con tu código postal antes de pagar."},
    "ciudades": {"titulo": "Envíos a tu ciudad con precio puesto", "items": CIUDADES,
                 "lede": ("Precio puesto con el modelo más económico, envío incluido. Enviamos a los 32 estados; estas son "
                          "las ciudades con guía propia."),
                 "perros": ('¿Tienes perros? Lee <a href="/pasto-sintetico/perros">qué pasto sintético conviene para '
                            "mascotas</a>.")},
    "comparativa": {"titulo": "Comparativa de modelos por altura, peso y precio",
                    "nota": ("Rollos de 2 m de ancho, 50 m² por rollo. Precios por rollo completo con IVA incluido. El "
                             "envío se suma según tu estado.")},
    "obras": {"titulo": "Pasto sintético instalado en casas reales", "figuras": OBRAS,
              "nota": ("Con sombra total o donde se estanca el agua, primero hay que resolver el drenaje: si no, el "
                       "pasto sintético se ve mal en pocos meses. Te lo decimos antes de venderte.",
                       "Antes de comprar")},
    "pedido": {"titulo": "Cómo comprar pasto sintético en línea", "pasos": PASOS},
    "instalar": {"titulo": "Cómo instalar pasto sintético tú mismo", "pasos": DIY,
                 "lede": "Un jardín de 25 a 50 m² se instala en un día. Estos son los cinco pasos básicos.",
                 "guia": '<a href="/blog/como-instalar-pasto-sintetico">Ver la guía completa paso a paso</a>'},
    "faq": {"titulo": "Preguntas frecuentes sobre pasto sintético", "preguntas": PREGUNTAS},
    "cierre": {"titulo": "¿Estás en Tampico, Madero o Altamira?",
               "lede": (f'Visita el showroom en {datos.CALLE_CORTA}, Cd. Madero. Vendemos desde 2 m² sin flete e '
                        'instalamos en Tampico, Madero y Altamira: <a href="/pasto-sintetico-tampico">venta e '
                        'instalación en Tampico</a> · <a href="/pasto-sintetico-tampico#showroom">cómo llegar al '
                        "showroom</a>."),
               "mensaje": datos.MENSAJES["pasto-sintetico"]},
    "barra": {"nombre": "Pasto sintético · 9 modelos", "precio": f"Desde {DESDE}/m²", "rollo": BARATO["rollo"]},
    "default": DEFAULT,
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
}
```

`tools/site/plantillas/tienda_hub.py`:

```python
"""Plantilla del hub de la tienda (/pasto-sintetico): portada con el precio puesto por estado y la foto principal
precargada → cuadro de datos → catálogo con filtros y Agregar → selector "¿cuál te conviene?" → comparador de otra
oferta → cotizador con envío y tabla de fletes → ciudades → comparativa de los 9 → obras con pies FIG. → cómo comprar
(TÚ / NOSOTROS / JUNTOS) → instálalo tú → preguntas → CTA final (Tampico). Contenido: tools/site/contenido/tienda.py.
JS: tienda-pasto.js (cotizador y lista), tienda-hub.js (filtros, selector, precio puesto, comparador), vt-landed.js."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js", "/js/tienda-hub.js")


def _portada(k):
    p = k["portada"]
    precio = (f'<p class="vt-precio-puesto" data-landed-hero data-rollo="{p["rollo"]}" aria-live="polite"><span>Desde'
              f'</span><b data-landed-value>${p["rollo"]}</b><span>/m²</span><small data-landed-note>{p["nota_precio"]}'
              '</small></p>')
    copia = (f'<div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1>'
             f'<p class="vt-existencia"><span>{p["existencia"]}</span></p><p class="vt-lede">{p["rotulo_estado"]}</p>'
             f'{t.selector_estado("hero-estado")}{precio}<p class="vt-promesa">{p["mensualidades"]}</p>'
             f'{c.fila_cta(p["mensaje"], k["tipo"], "hero", hero=True)}</div>')
    return (f'<section class="vt-portada vt-portada-t" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-portada__grid">{copia}<div class="vt-portada__foto">{c.figura(p["foto"], principal=True)}'
            f'</div></div>{c.cuadro_datos(p["datos"])}</div></section>')


def _cotizador(k):
    q = k["cotizador"]
    calculo = "".join(f"<li>{x}</li>" for x in q["calculo"])
    cuerpo = (f'<div class="vt-dos">{t.cotizador(k["default"], modelos=t.data.MODELOS, titulo=q["titulo_cotizador"], nivel=3, tipo=k["tipo"])}'
              f'<div><h3>{q["titulo_calculo"]}</h3><ul class="vt-checks vt-mt-s">{calculo}</ul></div></div>'
              f'<h3 class="vt-mt" id="envio">{q["titulo_envio"]}</h3><p class="vt-lede">{q["lede_envio"]}</p>'
              f'{t.tabla_envio()}<p class="vt-promesa">{q["nota_envio"]}</p>')
    return c.bloque(4, "Cotizador", "vt-h-cotizador", q["titulo"], cuerpo, tinte=True, id_seccion="cotizador")


def render(k):
    mo, el, co, ci, cp, ob, pe, ins, f, cie, b = (k[s] for s in ("modelos", "elegir", "comparar", "ciudades",
                                                                 "comparativa", "obras", "pedido", "instalar", "faq",
                                                                 "cierre", "barra"))
    secciones = (
        _portada(k),
        c.bloque(1, "Colección", "vt-h-modelos", mo["titulo"], t.catalogo(), lede=mo["lede"], id_seccion="modelos"),
        c.bloque(2, "Elegir", "vt-h-elegir", el["titulo"], t.selector_modelo(), tinte=True, id_seccion="elegir"),
        c.bloque(3, "Comparar", "vt-h-comparar", co["titulo"], t.comparador(), lede=co["lede"], id_seccion="comparar"),
        _cotizador(k),
        c.bloque(5, "Ciudades", "vt-h-ciudades", ci["titulo"],
                 t.ciudades_destacadas(ci["items"]) + f'<p class="vt-promesa">{ci["perros"]}</p>', lede=ci["lede"],
                 id_seccion="ciudades"),
        c.bloque(6, "Comparativa", "vt-h-comparativa", cp["titulo"],
                 t.tabla_modelos() + f'<p class="vt-promesa">{cp["nota"]}</p>', tinte=True, id_seccion="comparativa"),
        c.bloque(7, "Obras", "vt-h-obras", ob["titulo"], c.obras(ob["figuras"], c.nota(*ob["nota"])), id_seccion="obras"),
        c.bloque(8, "Tu pedido", "vt-h-pedido", pe["titulo"], c.pasos(pe["pasos"]), tinte=True,
                 id_seccion="como-funciona"),
        c.bloque(9, "Instálalo tú", "vt-h-diy", ins["titulo"], c.pasos(ins["pasos"]) +
                 f'<p class="vt-promesa">{ins["guia"]}</p>', lede=ins["lede"], id_seccion="instalacion"),
        c.bloque_dos(10, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True,
                     id_seccion="preguntas"),
        c.cierre(cie["titulo"], cie["lede"], cie["mensaje"], k["tipo"]),
    )
    grafo = [k["jsonld"][0], c.faq_jsonld(f["preguntas"]), k["jsonld"][1]]
    fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], cie["mensaje"], rollo=b["rollo"])
    return base.documento(k["meta"], t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(completo=True),), tras_main=fuera, scripts=SCRIPTS,
                          clase_body="vt-pagina vt-tienda")
```

- [ ] **Step 3: Registrar el hub y dejar de generarlo en `tools/pasto`**

En `tools/site/generar.py`, después de la fila de `/pasto-en-rollo-tampico` agrega `    ("/pasto-sintetico", "pasto-sintetico/index.html", "tienda_hub", "tienda"),`. En `tools/pasto/build.py` borra `from hub import build_hub` y `    write(ROOT / "index.html", build_hub())`.

- [ ] **Step 4: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2 && python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /pasto-sintetico
cd tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1
python3 -m unittest tests/test_reglas.py tests/test_consistencia.py tests/test_paridad.py tests/test_contenido.py 2>&1 | tail -1
```

Expected: `plantillas: 1 de 12 …`; luego `0 de 12` y `shell: 0 de 108 …`; las seis categorías en `ok`; `OK`; `OK`. A 320 px: los chips de filtro se acomodan en renglones (antes desbordaban), el selector de estado y el precio puesto quedan en el primer pantallazo, "+ Agregar" cabe en cada tarjeta y el `(0)` de "Mi lista" no se ve con la lista vacía.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/plantillas/tienda_hub.py tools/site/contenido/tienda.py tools/site/generar.py tools/site/tests/test_tienda.py tools/site/tests/test_reglas.py tools/pasto/build.py public/pasto-sintetico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(tienda): el hub sale de su plantilla con precio puesto, catálogo, selector, comparador y cotizador" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Las 11 ciudades y `/pasto-sintetico/perros` salen de la plantilla de guía

**Files:**
- Create: `tools/site/plantillas/tienda_guia.py`, `tools/site/contenido/ciudad.py`, `tools/site/contenido/perros.py`
- Modify: `tools/site/generar.py`, `tools/site/paginas.py`, `tools/site/tests/test_paginas.py`, `tools/site/tests/test_tienda.py`, `tools/pasto/build.py`
- Regenerate: `public/pasto-sintetico/envio/*/index.html` (11), `public/pasto-sintetico/perros/index.html`

Ciudades y perros no tienen cotizador ni `#buybar` (ya no los traían: su barra de compra nunca aparecía porque no hay `#comprar`), así que llevan la barra móvil del shell para no quedarse sin CTA fijo en celular.

- [ ] **Step 1: Pruebas**

Agrega a `TiendaPublicadaTest` en `tools/site/tests/test_tienda.py`:

```python
    def test_ciudad_con_respuesta_tabla_y_encabezados_en_pregunta(self):
        texto = html("/pasto-sintetico/envio/monterrey")
        cuerpo = principal(texto)
        for pregunta in ("¿Cuánto cuesta el envío a Monterrey?", "¿Cuánto tarda en llegar a Monterrey?",
                         "¿Cuál es la compra mínima?", "¿Cómo elijo el modelo sin ver una muestra?",
                         "¿Lo instalo yo o lo instalan ustedes?"):
            self.assertIn(f"<h3>{pregunta}</h3>", cuerpo)
        self.assertIn("<b>$162/m²</b>", cuerpo)
        self.assertIn("12 × ≈ $1,667", cuerpo)
        self.assertIn('href="/pasto-sintetico?estado=nuevo-leon#cotizador"', cuerpo)
        productos = [n for n in grafo(texto) if n["@type"] == "Product"]
        self.assertEqual(productos[0]["offers"]["shippingDetails"]["shippingRate"]["value"], "1150")

    def test_perros_sin_el_precio_del_aruba(self):
        cuerpo = principal(html("/pasto-sintetico/perros"))
        self.assertIn("<b>$149/m²</b> con Toscana 18", cuerpo)
        self.assertNotIn("$139", cuerpo)
        self.assertNotIn("muestra", cuerpo.lower())
        self.assertIn('href="/blog/pasto-sintetico-para-perros"', cuerpo)
```

En `tools/site/tests/test_paginas.py`, reemplaza el cuerpo de `test_sin_barra_en_tienda_catalogo_y_formularios` y agrega la prueba nueva:

```python
    def test_sin_barra_en_tienda_catalogo_y_formularios(self):
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/toscana-28", "/catalogo", "/cuestionario", "/gracias",
                     "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertFalse(paginas.contexto(ruta)["barra"])

    def test_paginas_de_la_tienda_sin_cotizador_llevan_la_barra_del_shell(self):
        # Desde 2b ciudades y perros no tienen #buybar: sin la barra móvil se quedaban sin CTA fijo en celular.
        for ruta in ("/pasto-sintetico/perros", "/pasto-sintetico/envio/cdmx"):
            with self.subTest(ruta=ruta):
                self.assertTrue(paginas.contexto(ruta)["barra"])
```

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests/test_paginas.py 2>&1 | tail -1; python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1`
Expected: `FAILED` en las dos.

- [ ] **Step 2: Barra del shell en ciudades y perros**

En `tools/site/paginas.py`: `SIN_BARRA = {"tienda", "ciudad", "catalogo"}` pasa a `SIN_BARRA = {"tienda", "catalogo"}`; después de `RUTAS_SIN_BARRA = {…}` agrega

```python
# Páginas de la tienda sin cotizador ni #buybar (Etapa 2b): llevan la barra móvil del shell.
RUTAS_CON_BARRA = {"/pasto-sintetico/perros"}
```

y en `contexto()` la línea `"barra": tipo not in SIN_BARRA and ruta not in RUTAS_SIN_BARRA,` pasa a `"barra": (tipo not in SIN_BARRA and ruta not in RUTAS_SIN_BARRA) or ruta in RUTAS_CON_BARRA,`.

- [ ] **Step 3: Plantilla y contenido**

`tools/site/plantillas/tienda_guia.py`:

```python
"""Plantilla de guía de la tienda: envío a una ciudad (/pasto-sintetico/envio/<ciudad>) y pasto para perros.

Ciudad (spec §3.3): respuesta directa con precio puesto y días → tabla 25/50/100 m² con la mensualidad más larga →
encabezados en pregunta (costo, tiempo, mínimo, cómo elegir sin muestra, instalación) → modelos → cómo llega →
preguntas → CTA. Perros: respuesta directa → criterios → modelos → preguntas → CTA. El orden de las secciones lo da el
contenido (k["secciones"]). Sin cotizador en la página: el CTA lleva al de la tienda con el estado elegido y a
WhatsApp; la barra móvil del shell queda (paginas.py). Contenido: contenido/ciudad.py y contenido/perros.py."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"
SCRIPTS = ("/js/vt-mensualidades.js", "/js/tienda-pasto.js", "/js/vt-landed.js")


def _portada(k):
    p = k["portada"]
    acciones = (f'<div class="vt-cta" data-hero-cta>{c.boton_wa(p["mensaje"], k["tipo"] + ":hero")}'
                f'<a class="vt-btn vt-btn--linea" href="{p["href_modelos"]}">{p["texto_modelos"]}</a></div>'
                f'<p class="vt-promesa">{c.esc(t.datos.PROMESA_COMPLETA)}</p>')
    copia = (f'<div><p class="vt-kicker">{p["kicker"]}</p><h1 id="vt-h1">{p["h1"]}</h1><p class="vt-lede">'
             f'{p["respuesta"]}</p>{acciones}</div>')
    return (f'<section class="vt-portada vt-portada-t" aria-labelledby="vt-h1"><div class="vt-wrap">{c.migas(k["migas"])}'
            f'<div class="vt-portada__grid">{copia}<div class="vt-portada__foto">{c.figura(p["foto"], principal=True)}'
            f'</div></div>{c.cuadro_datos(p["datos"])}</div></section>')


def _cuerpo(s):
    tipo = s["tipo"]
    if tipo == "totales":
        return t.tabla_totales(s["modelo"], s["zona"]) + "".join(f'<p class="vt-promesa">{n}</p>' for n in s["notas"])
    if tipo == "preguntas":
        return t.preguntas_h3(s["items"])
    if tipo == "modelos":
        return t.modelos_recomendados(s["items"], s.get("zona"), s.get("lugar", ""))
    if tipo == "pasos":
        return c.pasos(s["items"])
    if tipo == "faq":
        return c.faq(s["preguntas"]) + "".join(f'<p class="vt-promesa">{n}</p>' for n in s.get("notas", ()))
    raise ValueError(f"Sección desconocida: {tipo}")


def render(k):
    secciones = [_portada(k)]
    for n, s in enumerate(k["secciones"], 1):
        secciones.append(c.bloque(n, s["rotulo"], f"vt-h-{s['id']}", s["titulo"], _cuerpo(s), lede=s.get("lede"),
                                  tinte=n % 2 == 0, id_seccion=s["id"]))
    ci = k["cierre"]
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], k["tipo"]))
    faq = next(s["preguntas"] for s in k["secciones"] if s["tipo"] == "faq")
    grafo = list(k["jsonld"]) + [c.faq_jsonld(faq)]
    return base.documento(k["meta"], t.subnav() + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),),
                          head_extra=(t.json_modelos(), t.SCRIPT_PRECIO_PUESTO), tras_main=t.lista_y_aviso(),
                          scripts=SCRIPTS, clase_body="vt-pagina vt-tienda")
```

`tools/site/contenido/ciudad.py`:

```python
"""Contenido de las 11 páginas /pasto-sintetico/envio/<ciudad>. Solo datos: la plantilla es plantillas/tienda_guia.py.

Textos de cada ciudad (intro, clima, modelos, preguntas) de tools/pasto/ciudades.py; precios, zonas y fletes de
tools/pasto/data.py; mensualidades de tools/pasto/mensualidades.py. Título, descripción, canonical, Open Graph,
Product con envío al estado y migas: los que publicaba tools/pasto/ciudad.py. PARIDAD: tests/test_paridad.py.
"""
from types import SimpleNamespace

import componentes_tienda as t
import data
import datos
from ciudades import CIUDADES
from componentes import dinero
from esquema import breadcrumb_schema

CLAVES = tuple(x["slug"] for x in CIUDADES)
POR_SLUG = {x["slug"]: x for x in CIUDADES}
SITE = data.SITE
GAL = t.GAL
FOTO = "obra-proyecto-02"
LLEGADA = (
    {"titulo": "Confirmas y pagas", "quien": "tu", "cuando": "Al confirmar",
     "texto": f"Transferencia o link de pago con tarjeta. Factura {datos.FACTURA}."},
    {"titulo": "Sale en rollo", "quien": "nosotros", "cuando": "1 a 2 días hábiles",
     "texto": "Rollo de 2 m de ancho, enrollado y protegido, con guía de rastreo."},
    {"titulo": "Revisa al recibir", "quien": "tu", "cuando": "Al recibir",
     "texto": ("Que el empaque venga completo y que los metros coincidan con tu pedido. Si algo no está bien, avísanos "
               "por WhatsApp con fotos.")},
)
INSTALACION = ("La instalación profesional es solo en Tampico, Ciudad Madero y Altamira. Un patio de 25 a 50 m² se "
               "instala en un día con dos personas: te mandamos la guía con el pedido "
               '(<a href="/blog/como-instalar-pasto-sintetico">guía de instalación paso a paso</a>).')


def _producto(x, zona, url, desde):
    m = t.barato()
    return {
        "@type": "Product", "name": f"Pasto sintético con envío a {x['nombre_largo']}",
        "brand": {"@type": "Brand", "name": datos.NOMBRE}, "image": [f"{SITE}{GAL}/{FOTO}.webp"],
        "description": f"Pasto sintético en rollo de 50 m² con envío a {x['nombre_largo']}, desde ${desde}/m² puesto en tu casa.",
        "offers": {
            "@type": "Offer", "priceCurrency": "MXN", "price": str(m["rollo"]),
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(m["rollo"]), "priceCurrency": "MXN",
                                   "unitText": "m²"},
            "availability": "https://schema.org/InStock", "url": url,
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": str(data.ZONAS[zona]), "currency": "MXN"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MX", "addressRegion": x["estado"]},
                "deliveryTime": {"@type": "ShippingDeliveryTime", "transitTime": {
                    "@type": "QuantitativeValue", "minValue": 3, "maxValue": 5, "unitCode": "DAY"}},
            },
        },
    }


def _preguntas_envio(x, zona):
    """Encabezados en pregunta (spec §3.3, ciudad): costo, tiempo, mínimo, cómo elegir sin muestra e instalación."""
    n = x["nombre"]
    return (
        (f"¿Cuánto cuesta el envío a {n}?",
         f"{dinero(data.ZONAS[zona])} por rollo de 50 m² ({data.ZONA_ESTADOS[zona][0]}). Si pides de 51 a 100 m² son dos "
         "rollos y dos fletes. El envío nunca va escondido en el precio."),
        (f"¿Cuánto tarda en llegar a {n}?", "De 3 a 5 días hábiles después de confirmar el pago, con guía de rastreo."),
        ("¿Cuál es la compra mínima?",
         "25 m² para envío nacional, medio rollo. Los cortes de 2 a 9 m² son solo en el showroom de Cd. Madero."),
        ("¿Cómo elijo el modelo sin ver una muestra?",
         "Como no ofrecemos muestras físicas, cada ficha tiene fotos de cerca, altura, peso y la comparativa con sus dos "
         "vecinos. Si dudas entre dos, mándanos una foto de tu espacio por WhatsApp y te decimos cuál conviene."),
        ("¿Lo instalo yo o lo instalan ustedes?", INSTALACION),
    )


def contenido(x):
    zona = data.zona_de(x["estado"])
    url = f"{SITE}/pasto-sintetico/envio/{x['slug']}"
    m = t.barato()
    desde = data.landed_m2(m, zona)
    estado = data.estado_slug(x["estado"])
    titulo = f"Pasto sintético en {x['nombre']} con envío · desde ${desde}/m² | Viveros Terra"
    descripcion = (f"Pasto sintético con envío a {x['nombre_largo']} desde ${desde}/m² puesto en tu casa. 9 modelos de "
                   "10 a 35 mm, entrega en 3 a 5 días hábiles y factura.")
    mensaje = f"Hola, quiero cotizar pasto sintético con envío a {x['nombre']}.\nMetros aprox.: ___\nModelo: ___"
    return {
        "tipo": "ciudad",
        "meta": {"title": titulo, "description": descripcion, "robots": "index, follow, max-image-preview:large",
                 "canonical": url,
                 "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", url), ("og:title", titulo),
                        ("og:description", descripcion), ("og:image", f"{SITE}{GAL}/{FOTO}.webp"),
                        ("og:locale", "es_MX")),
                 "twitter": (("twitter:card", "summary_large_image"),)},
        "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"),
                                      (f"Envío a {x['nombre']}", url)]), _producto(x, zona, url, desde)),
        "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), (f"Envío a {x['nombre']}", None)),
        "portada": {
            "kicker": f"Envío a {x['nombre_largo']} · 9 modelos en existencia",
            "h1": f'Pasto sintético en {x["nombre"]} <span class="vt-serif">con envío a tu casa</span>',
            "respuesta": (f"Te enviamos el pasto sintético a {x['nombre_largo']} en 3 a 5 días hábiles. Desde "
                          f"<b>${desde}/m²</b> ya con envío, en rollo de 50 m² con factura. Tú lo instalas con nuestra "
                          "guía."),
            "mensaje": mensaje,
            "href_modelos": f"/pasto-sintetico?estado={estado}#modelos",
            "texto_modelos": "Ver los 9 modelos con precio puesto",
            "foto": {"src": f"{GAL}/{FOTO}-sm.webp", "srcset": f"{GAL}/{FOTO}-sm.webp 560w, {GAL}/{FOTO}.webp 960w",
                     "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                     "alt": "Jardín residencial con pasto sintético de nuestra colección",
                     "lugar": "Jardín residencial", "etapa": "Pasto de la colección instalado"},
            "datos": ((f"Puesto en {x['nombre']}", f"desde ${desde}/m²", f"Con {m['nombre']}"),
                      ("Flete por rollo", dinero(data.ZONAS[zona]), data.ZONA_ESTADOS[zona][0]),
                      ("Entrega", "3 a 5 días", "Hábiles, con guía de rastreo"),
                      ("Compra mínima", "25 m²", "Medio rollo"),
                      ("Factura", datos.FACTURA, "Persona física o moral"),
                      ("Vendemos a todo México", f"Desde {datos.SINTETICO_NACIONAL_DESDE}", f"Showroom en {datos.CALLE_CORTA}")),
        },
        "secciones": (
            {"tipo": "totales", "id": "precios", "rotulo": "Precios", "titulo": f"Cuánto cuesta con envío a {x['nombre']}",
             "lede": x["intro"], "modelo": m, "zona": zona,
             "notas": ("El flete exacto se confirma con tu código postal antes de pagar.",
                       "Mensualidades con tarjeta de crédito; el total en mensualidades es mayor que el de contado. "
                       f'Calcula tu plan en el <a href="/pasto-sintetico?estado={estado}#cotizador">cotizador</a>.')},
            {"tipo": "preguntas", "id": "envio-dudas", "rotulo": "Antes de comprar",
             "titulo": f"Envío a {x['nombre']}: costo, tiempo y mínimo", "items": _preguntas_envio(x, zona)},
            {"tipo": "modelos", "id": "modelos", "rotulo": "Clima", "titulo": f"El pasto que conviene en {x['nombre']}",
             "lede": x["clima"], "items": x["modelos"], "zona": zona, "lugar": x["nombre"]},
            {"tipo": "pasos", "id": "envio", "rotulo": "Envío", "titulo": "Cómo te llega el pedido", "items": LLEGADA},
            {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": f"Preguntas frecuentes en {x['nombre']}",
             "preguntas": tuple(x["faqs"])},
        ),
        "cierre": {"titulo": f"Cotiza tu pedido a {x['nombre']}",
                   "lede": (f"Elige modelo y metros en la tienda: el precio ya incluye el envío a {x['nombre_largo']}. "
                            f'<a href="/pasto-sintetico?estado={estado}#cotizador">Calcular mi pedido</a>.'),
                   "mensaje": mensaje},
    }


def paridad(x):
    """La sección "Instálalo tú" pasa a la pregunta de instalación. En la zona B (Monterrey y Veracruz), 12 mensualidades
    sobre $19,998 son 1,666.5: la página decía $1,666 (round() de Python) y el cotizador cobra $1,667 (Math.round);
    desde 2b Python redondea como el JS."""
    reemplazos = {"Instalarlo tú mismo es sencillo": "¿Lo instalo yo o lo instalan ustedes?"}
    if data.zona_de(x["estado"]) == "B":
        reemplazos["$1,666"] = "$1,667"
    return {"reemplazos": reemplazos, "retirados": {}}


def pagina(slug):
    return SimpleNamespace(CONTENIDO=contenido(POR_SLUG[slug]), PARIDAD=paridad(POR_SLUG[slug]))
```

`tools/site/contenido/perros.py`:

```python
"""Contenido de /pasto-sintetico/perros. Solo datos: la plantilla es plantillas/tienda_guia.py.

Solo afirmaciones presentes en las fichas (data.COMMON_TREATMENTS incluye antibacterial); sin prometer lo que no está
documentado. Título, descripción, canonical, Open Graph y migas: los que publicaba tools/pasto/perros.py.
PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero
from esquema import breadcrumb_schema

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico/perros"
GAL = t.GAL
FOTO = "obra-proyecto-02"
RECOMENDADOS = (
    ("irlanda-25", "Fibra más resistente de la colección: aguanta pisoteo y juego diario."),
    ("capri-20", "Alta densidad y fibra corta: fácil de limpiar y de levantar desechos."),
    ("toscana-18", "El más económico para patios chicos o para empezar."),
)
MAS_BARATO = min((data.BY_SLUG[s] for s, _r in RECOMENDADOS), key=lambda m: m["rollo"])
DESDE = dinero(MAS_BARATO["rollo"])
GUIA = '<a href="/blog/como-instalar-pasto-sintetico">guía de instalación</a>'
CRITERIOS = (
    ("Fibra resistente y no muy alta", "De 18 a 25 mm es lo más práctico: se limpia fácil y aguanta el paso diario."),
    ("Base perforada que drene", "La orina tiene que pasar al suelo. Instálalo sobre grava fina compactada, no sobre "
                                 "piso liso sin desnivel."),
    ("Limpieza sencilla", "Levanta los desechos sólidos y enjuaga con manguera. Para el olor, usa un limpiador enzimático "
                          "para mascotas."),
)
PREGUNTAS = (
    ("¿El pasto sintético se calienta con el sol?", "Sí, como cualquier superficie exterior al sol. Enjuágalo con "
     "manguera en las horas de más calor y deja una zona de sombra para tu perro."),
    ("¿Mi perro lo puede rasguñar o romper?", "Un perro que escarba puede levantar las orillas si no están bien fijadas. "
     f"Fija el perímetro con clavos o adhesivo como indica la {GUIA}."),
    ("¿El pasto sintético huele a orina?", "Si la base no drena o no se enjuaga, sí. Con grava que drene, enjuague "
     "frecuente y un limpiador enzimático se controla el olor."),
    ("¿Cómo se lava el pasto sintético con perros?", "Levanta los desechos, enjuaga con manguera una o dos veces por "
     "semana y cepilla la fibra de vez en cuando para que quede de pie."),
    ("¿Qué tratamientos tiene el pasto?", f"Todos nuestros modelos tienen de fábrica estos tratamientos: "
     f"{data.COMMON_TREATMENTS}."),
)
TITULO = "Pasto sintético para perros: qué modelo elegir y cómo limpiarlo | Viveros Terra"
DESCRIPCION = ("Pasto sintético para perros con envío a todo México: qué modelo elegir, cómo drena la orina, cómo quitar "
               f"el olor y cómo limpiarlo. Desde {DESDE}/m².")
MENSAJE = "Hola, quiero pasto sintético para mis perros.\nMetros aprox.: ___\nMi estado: ___"

CONTENIDO = {
    "tipo": "tienda",
    "meta": {"title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large",
             "canonical": URL,
             "og": (("og:type", "article"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
                    ("og:description", DESCRIPCION), ("og:image", f"{SITE}{GAL}/{FOTO}.webp"), ("og:locale", "es_MX")),
             "twitter": (("twitter:card", "summary_large_image"),)},
    "jsonld": (breadcrumb_schema([("Inicio", SITE), ("Pasto sintético", f"{SITE}/pasto-sintetico"), ("Para perros", URL)]),),
    "migas": (("Inicio", "/"), ("Pasto sintético", "/pasto-sintetico"), ("Para perros", None)),
    "portada": {
        "kicker": "Mascotas · Envío a todo México",
        "h1": 'Pasto sintético para perros <span class="vt-serif">que drena y se limpia fácil</span>',
        "respuesta": ("Para perros conviene un pasto de 18 a 25 mm con fibra resistente, instalado sobre grava que drene. "
                      f"Se limpia con manguera y un limpiador enzimático. Desde <b>{DESDE}/m²</b> con "
                      f"{MAS_BARATO['nombre']}."),
        "mensaje": MENSAJE,
        "href_modelos": "/pasto-sintetico#modelos",
        "texto_modelos": "Ver precios con envío",
        "foto": {"src": f"{GAL}/{FOTO}-sm.webp", "srcset": f"{GAL}/{FOTO}-sm.webp 560w, {GAL}/{FOTO}.webp 960w",
                 "sizes": "(min-width: 1024px) 620px, 100vw", "ancho": 960, "alto": 1280, "numero": 1,
                 "alt": "Patio con pasto sintético de nuestra colección", "lugar": "Patio residencial",
                 "etapa": "Pasto de la colección instalado"},
        "datos": (("Altura ideal", "18 a 25 mm", "Fácil de limpiar"), ("Base", "Perforada", "Drena la orina"),
                  ("Tratamientos", "Antibacterial", "UV y retardante al fuego"), ("Desde", f"{DESDE}/m²", MAS_BARATO["nombre"]),
                  ("Entrega", "3 a 5 días", "A todo México"), ("Factura", datos.FACTURA, "Persona física o moral")),
    },
    "secciones": (
        {"tipo": "preguntas", "id": "elegir", "rotulo": "Elegir", "titulo": "Qué pasto sintético conviene para perros",
         "items": CRITERIOS},
        {"tipo": "modelos", "id": "modelos", "rotulo": "Modelos", "titulo": "Tres modelos para mascotas",
         "items": RECOMENDADOS},
        {"tipo": "faq", "id": "preguntas", "rotulo": "Preguntas", "titulo": "Preguntas frecuentes con perros",
         "preguntas": PREGUNTAS,
         "notas": ('<a href="/blog/pasto-sintetico-para-perros">Lee la guía completa: pasto sintético para perros</a>',)},
    ),
    "cierre": {"titulo": "Cotiza el pasto para tus perros",
               "lede": ("Dinos tus metros y tu estado: te respondemos con el modelo que conviene y el precio puesto en tu "
                        "casa."),
               "mensaje": MENSAJE},
}

PARIDAD = {"reemplazos": {}, "retirados": {}}
```

- [ ] **Step 4: Registrar y dejar de generarlas en `tools/pasto`**

En `tools/site/generar.py`: después de la fila del hub agrega `    ("/pasto-sintetico/perros", "pasto-sintetico/perros/index.html", "tienda_guia", "perros"),`, y al final de `PAGINAS`, `+ _varias("ficha", …, "ficha")` pasa a:

```python
) + _varias("ficha", lambda k: f"/pasto-sintetico/{k}", lambda k: f"pasto-sintetico/{k}/index.html", "ficha") + _varias(
    "ciudad", lambda k: f"/pasto-sintetico/envio/{k}", lambda k: f"pasto-sintetico/envio/{k}/index.html", "tienda_guia")
```

En `tools/pasto/build.py` borra `from ciudad import build_ciudad`, `from perros import build_perros`, las dos líneas `for c in CIUDADES:` / `write(ROOT / "envio" / c["slug"] / "index.html", build_ciudad(c))` y `write(ROOT / "perros" / "index.html", build_perros())`.

- [ ] **Step 5: Build, paridad y pruebas**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2 && python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /pasto-sintetico/perros $(python3 -c "import sys; sys.path[:0]=['tools/pasto']; from ciudades import CIUDADES; print(' '.join('/pasto-sintetico/envio/'+c['slug'] for c in CIUDADES))") | grep -v ": ok" | grep -v "^=="
cd tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1
python3 -m unittest tests/test_paginas.py tests/test_reglas.py tests/test_consistencia.py tests/test_paridad.py tests/test_contenido.py 2>&1 | tail -1
```

Expected: `plantillas: 12 de 24 …`; luego `0 de 24` y `shell: 0 de 108 …`; vacío (todas las categorías en `ok`: "Instalarlo tú mismo es sencillo" pasa a "¿Lo instalo yo o lo instalan ustedes?" y, en Monterrey y Veracruz, `$1,666` a `$1,667`, ambos declarados en `contenido/ciudad.paridad()`); `OK`; `OK`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/plantillas/tienda_guia.py tools/site/contenido/ciudad.py tools/site/contenido/perros.py tools/site/generar.py tools/site/paginas.py tools/site/tests/test_paginas.py tools/site/tests/test_tienda.py tools/pasto/build.py public/pasto-sintetico/envio public/pasto-sintetico/perros/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(ciudades): envío por ciudad y perros con respuesta directa, tabla 25/50/100 y encabezados en pregunta" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: `/pasto-sintetico-tampico` sale de la plantilla de servicio

La plantilla de servicio de 2a gana cinco piezas opcionales que también usará 2c: formas de contratar (máx. 3, cada una con su mensaje), tabla comparativa de precios, el cotizador de la tienda (con lista y barra de compra; la página se vuelve `vt-tienda`), visita al showroom y el bloque de pago sin simulador (muestra los plazos y mínimos de `planes_mensualidades()`). `/pasto-en-rollo-tampico` no cambia.

**Files:**
- Modify: `tools/site/plantillas/servicio.py`, `tools/site/generar.py`, `tools/site/tests/test_generar.py`, `tools/site/tests/test_tienda.py`, `tools/pasto/build.py`
- Create: `tools/site/contenido/sintetico_tampico.py`
- Regenerate: `public/pasto-sintetico-tampico/index.html`

- [ ] **Step 1: Pruebas**

Agrega a `TiendaPublicadaTest` en `tools/site/tests/test_tienda.py`:

```python
    def test_veinticinco_paginas_de_sintetico_con_plantilla(self):
        self.assertEqual(len(TIENDA), 1 + 1 + 1 + len(data.MODELOS) + 11)

    def test_scripts_en_orden(self):
        esperado = {"/pasto-sintetico": ["vt-mensualidades", "tienda-pasto", "vt-landed", "tienda-hub"],
                    "/pasto-sintetico/toscana-28": ["vt-mensualidades", "tienda-pasto", "vt-landed"],
                    "/pasto-sintetico/envio/cdmx": ["vt-mensualidades", "tienda-pasto", "vt-landed"],
                    "/pasto-sintetico-tampico": ["vt-mensualidades", "tienda-pasto"]}
        for ruta, scripts in esperado.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(re.findall(r'<script src="/js/([\w-]+)\.js" defer>', html(ruta)), scripts)

    def test_tampico_con_opciones_cotizador_y_showroom(self):
        texto = html("/pasto-sintetico-tampico")
        cuerpo = principal(texto)
        self.assertIn("los otros 7 modelos también están en existencia", cuerpo)
        self.assertIn('id="showroom"', cuerpo)
        self.assertIn('<option value="showroom" selected>', cuerpo)
        self.assertEqual(cuerpo.count('<li class="vt-modo'), 2)
        self.assertNotIn("Sofía", cuerpo)
        tipos = {t for n in grafo(texto) for t in ([n["@type"]] if isinstance(n["@type"], str) else n["@type"])}
        self.assertTrue({"LocalBusiness", "Store", "Service", "FAQPage", "HowTo", "BreadcrumbList"} <= tipos)

    def test_barras_fijas_que_no_se_tapan(self):
        for ruta in TIENDA:
            texto = html(ruta)
            buybar, barra = 'id="buybar"' in texto, "data-vt-bar" in texto
            with self.subTest(ruta=ruta):
                self.assertFalse(buybar and barra)
                self.assertTrue(buybar or barra)
```

(Borra `test_scripts_de_la_ficha_en_orden` de la Tarea 9: `test_scripts_en_orden` la incluye.)

En `tools/site/tests/test_generar.py`: después de `import activos  # noqa: E402` agrega

```python
import componentes  # noqa: E402,F401  (agrega tools/pasto al path)
```

y después de `import generar  # noqa: E402` agrega

```python
from ciudades import CIUDADES  # noqa: E402
from data import MODELOS  # noqa: E402
```

cambia `self.assertEqual([r for r, *_ in generar.PAGINAS][:2], ["/", "/pasto-en-rollo-tampico"])` (Tarea 4) por

```python
        esperadas = (["/", "/pasto-en-rollo-tampico", "/pasto-sintetico-tampico", "/pasto-sintetico",
                      "/pasto-sintetico/perros"] + [f"/pasto-sintetico/{m['slug']}" for m in MODELOS]
                     + [f"/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES])
        self.assertEqual([r for r, *_ in generar.PAGINAS], esperadas)
```

y agrega antes de `test_lo_publicado_es_lo_que_sale_de_la_plantilla`:

```python
    def test_cargar_paginas_de_un_modulo_con_varias(self):
        ficha = generar.cargar("ficha:toscana-28")
        self.assertEqual(ficha.CONTENIDO["modelo"]["slug"], "toscana-28")
        self.assertIn("reemplazos", ficha.PARIDAD)
        self.assertIs(generar.cargar("inicio").CONTENIDO, generar.cargar("inicio").CONTENIDO)
        self.assertEqual(generar.contenido_de("/pasto-sintetico/envio/cdmx"), "ciudad:cdmx")
```

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest discover -s tests -p "test_tienda.py" 2>&1 | tail -1; python3 -m unittest tests/test_generar.py 2>&1 | tail -1`
Expected: `FAILED` en las dos.

- [ ] **Step 2: Plantilla de servicio extendida**

Reemplaza todo `tools/site/plantillas/servicio.py` por:

```python
"""Plantilla de servicio local (spec §3.3): ruta visible → H1 con beneficio y lugar → precio ancla en la etiqueta → CTA
con plantilla y promesa → prueba (cuadro de datos, fotos FIG., nota de campo, opinión con nombre y clientes) → precio con
Medidor → objeción principal → proceso NOSOTROS / TÚ (también es el HowTo del JSON-LD) → garantía con condiciones →
pago (anticipo y mensualidades con tarjeta de crédito, con su simulador) → preguntas → cobertura → relacionados → CTA
final. Las secciones que el contenido no trae se omiten (diseño, mantenimiento y riego no llevan Medidor de pasto).
Opcionales desde 2b: formas de contratar (máx. 3, cada una con su mensaje), tabla comparativa de precios, cotizador de
la tienda (tienda-pasto.js, con lista de cotización y barra de compra), visita al showroom y pago sin simulador (con
los plazos de mensualidades). Páginas: /pasto-en-rollo-tampico (contenido/pasto_en_rollo.py) y
/pasto-sintetico-tampico (contenido/sintetico_tampico.py)."""
import componentes as c
import componentes_tienda as t
from plantillas import base

CONTEXTO = "https://schema.org"


def _scripts(k):
    """vt-mensualidades.js primero (lo usan el Medidor, el simulador y el cotizador); cada uno solo si la página lo trae."""
    con_medidor = bool(k.get("precio", {}).get("titulo_medidor"))
    return (("/js/vt-mensualidades.js",) + (("/js/vt-medidor.js",) if con_medidor else ())
            + (("/js/tienda-pasto.js",) if "cotizador" in k else ())
            + (("/js/vt-simulador.js",) if k["pago"].get("sim") else ()))


def _prueba(k, numero):
    pr = k["prueba"]
    cuerpo = c.obras(pr["figuras"], c.nota(*pr["nota"]))
    if pr.get("opiniones"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_opinion"]}</h3>' + c.testimonios(pr["opiniones"])
    if pr.get("titulo_clientes"):
        cuerpo += f'<h3 class="vt-mt">{pr["titulo_clientes"]}</h3>' + c.logos()
    return c.bloque(numero, "Prueba", "vt-h-prueba", pr["titulo"], cuerpo, lede=pr["lede"])


def _precio(k, numero):
    p = k["precio"]
    if "tabla" in p:
        cuerpo = c.tabla_comparativa(p["tabla"]["columnas"], p["tabla"]["filas"], p["caption"])
    else:
        cuerpo = c.tabla_precios(p["filas"], p["caption"], concepto="Forma de compra")
    if p.get("titulo_medidor"):
        cuerpo += f'<h3 class="vt-mt">{p["titulo_medidor"]}</h3>' + c.medidor(k["prefijo"], k["tipo"], mensaje=k["portada"]["mensaje"])
    return c.bloque(numero, "Precio", "vt-h-precio", p["titulo"], cuerpo, lede=p["lede"], tinte=True, id_seccion="precio")


def _opciones(k, numero):
    o = k["opciones"]
    return c.bloque(numero, "Opciones", "vt-h-opciones", o["titulo"], c.opciones(o["items"], k["tipo"]), lede=o.get("lede"),
                    id_seccion="opciones")


def _aparte(items):
    """Columna junto al cotizador: (título, puntos, nota) por bloque."""
    salida = []
    for i, (titulo, puntos, nota) in enumerate(items):
        clase = ' class="vt-mt"' if i else ""
        lista = "".join(f"<li>{x}</li>" for x in puntos)
        salida.append(f"<h3{clase}>{titulo}</h3>" + (f'<ul class="vt-checks vt-mt-s">{lista}</ul>' if lista else "")
                      + f'<p class="vt-promesa">{nota}</p>')
    return "".join(salida)


def _cotizador(k, numero):
    q = k["cotizador"]
    modelo = t.modelo(q["modelo"])
    calculadora = t.cotizador(modelo, modelos=t.data.MODELOS, m2=q["m2"], showroom=True, nivel=3, titulo=q["titulo_calc"],
                              tipo=k["tipo"])
    cuerpo = f'<div class="vt-dos">{calculadora}<div>{_aparte(q["aparte"])}</div></div>'
    return c.bloque(numero, "Calculadora", "vt-h-cotizador", q["titulo"], cuerpo, tinte=True, id_seccion="cotizador")


def _visita(k, numero):
    v = k["visita"]
    enlaces = "".join(f'<a class="vt-btn vt-btn--linea" href="{c.esc(h)}" target="_blank" rel="noopener">{x}</a>'
                      for x, h in v["mapas"])
    cuerpo = f'{c.cuadro_datos(v["datos"])}<div class="vt-cta vt-mt-s">{enlaces}{c.boton_tel(k["tipo"] + ":visita")}</div>'
    return c.bloque(numero, "Showroom", "vt-h-visita", v["titulo"], cuerpo, lede=v.get("lede"), id_seccion="showroom")


def _objecion(k, numero):
    o = k["objecion"]
    a, b = o["comparativa"], o["comparativa_2"]
    cuerpo = (c.tabla_comparativa(a["columnas"], a["filas"], a["caption"]) + f'<p class="vt-promesa">{a["cierre"]}</p>'
              + f'<h3 class="vt-mt">{o["titulo_2"]}</h3>' + c.tabla_comparativa(b["columnas"], b["filas"], b["caption"]))
    return c.bloque(numero, "Cuál te conviene", "vt-h-conviene", o["titulo"], cuerpo, lede=o["lede"])


def _pago(k, numero):
    """Un solo bloque de pago: anticipo, contado y mensualidades en tres renglones, y el simulador (los plazos y montos
    mínimos los muestra el propio simulador, sin repetir la tabla de planes)."""
    p = k["pago"]
    puntos = "".join(f"<li>{t}</li>" for t in p["puntos"])
    izquierda = f'<p class="vt-lede">{p["lede"]}</p><ul class="vt-checks vt-mt-s">{puntos}</ul>'
    if p.get("sim"):
        derecha = f'<h3>{p["titulo_sim"]}</h3>' + c.simulador(p["sim"]["servicio"], p["sim"]["monto"], k["tipo"])
    else:
        derecha = c.planes_mensualidades()
    return c.bloque_dos(numero, "Pago", "vt-h-pago", p["titulo"], izquierda, derecha, id_seccion="mensualidades")


def _cobertura(k, numero):
    co = k["cobertura"]
    return c.bloque(numero, "Cobertura", "vt-h-cobertura", co["titulo"],
                    c.cobertura(co["zonas"], co["por_proyecto"], co.get("sectores", ())), lede=co["lede"])


def _relacionados(k, numero):
    r = k["relacionados"]
    return c.bloque(numero, "Relacionados", "vt-h-rel", r["titulo"], c.relacionados(r["items"]), tinte=True)


def render(k):
    tipo = k["tipo"]
    g, f, ci, p = k["garantia"], k["faq"], k["cierre"], k["proceso"]
    secciones = [c.portada(k["portada"], tipo, k["migas"]), _prueba(k, 1)]
    numero = 2
    for clave, armar in (("opciones", _opciones), ("precio", _precio), ("cotizador", _cotizador),
                         ("objecion", _objecion)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.bloque(numero, "Proceso", "vt-h-proceso", p["titulo"], c.pasos(p["pasos"]), lede=p["lede"]))
    secciones.append(c.garantia(dict(g, numero=numero + 1, id_titulo="vt-h-garantia", rotulo="Garantía")))
    secciones.append(_pago(k, numero + 2))
    secciones.append(c.bloque_dos(numero + 3, "Preguntas", "vt-h-faq", f["titulo"], "", c.faq(f["preguntas"]), tinte=True))
    numero += 4
    for clave, armar in (("visita", _visita), ("cobertura", _cobertura), ("relacionados", _relacionados)):
        if clave in k:
            secciones.append(armar(k, numero))
            numero += 1
    secciones.append(c.cierre(ci["titulo"], ci["lede"], ci["mensaje"], tipo))

    j = k["jsonld"]
    pasos_howto = tuple((x["titulo"], x["texto"]) for x in p["pasos"])
    grafo = [j["producto"], *j.get("nodos", ()), c.faq_jsonld(f["preguntas"]), c.howto(j["howto"], pasos_howto),
             j["migas"], {"@type": "SpeakableSpecification", "cssSelector": list(j["speakable"])}]
    tienda = "cotizador" in k
    fuera = ""
    if tienda:
        b = k["barra"]
        fuera = t.lista_y_aviso() + t.barra_compra(b["nombre"], b["precio"], ci["mensaje"])
    return base.documento(k["meta"], (t.subnav() if tienda else "") + "\n".join(secciones),
                          jsonld_bloques=({"@context": CONTEXTO, "@graph": grafo},),
                          precargas=(base.precarga_imagen(k["portada"]["foto"]),), scripts=_scripts(k),
                          head_extra=(t.json_modelos(),) if tienda else (), tras_main=fuera,
                          clase_body="vt-pagina vt-tienda" if tienda else "vt-pagina")
```

- [ ] **Step 3: Contenido de Tampico**

`tools/site/contenido/sintetico_tampico.py`:

```python
"""Contenido de /pasto-sintetico-tampico (venta en showroom e instalación en Tampico, Madero y Altamira). Solo datos:
la plantilla es tools/site/plantillas/servicio.py (la de pasto en rollo, con opciones, tabla de modelos, cotizador de la
tienda y visita al showroom).

Modelos y precios de tools/pasto/data.py; instalado de datos.PRECIOS["sintetico_instalado_m2"]; domicilio, horario y
promesa de datos.py. Título, descripción, canonical, Open Graph, LocalBusiness/Store, Service y migas: los que
publicaba tools/pasto/local.py; FAQPage de las preguntas visibles y HowTo de los 5 pasos visibles. Los 9 modelos en
existencia; para llevar hoy solo Toscana 18 y 28 (data.MODELOS[...]["stock"]). PARIDAD: tests/test_paridad.py.
"""
import componentes_tienda as t
import data
import datos
from componentes import dinero

SITE = data.SITE
URL = f"{SITE}/pasto-sintetico-tampico"
GAL = t.GAL
NEGOCIO = f"{SITE}/#negocio"
INST_MIN, INST_MAX = datos.PRECIOS["sintetico_instalado_m2"]
MIN_RETAIL = min(m["rollo"] for m in data.MODELOS)
STOCK = [m for m in data.MODELOS if m["stock"]]
HOY = " y ".join(m["nombre"] for m in STOCK)
T18, T28 = data.BY_SLUG["toscana-18"], data.BY_SLUG["toscana-28"]
APPLE_MAPS = f"https://maps.apple.com/?daddr={datos.GEO[0]},{datos.GEO[1]}&q=Viveros%20Terra"
DOMICILIO = f"{datos.CALLE}, {datos.COLONIA}, {datos.CP} Cd. Madero, frente a Walmart"
TITULO = "Pasto Sintético en Tampico: Venta e Instalación | Viveros Terra"
DESCRIPCION = (f"Venta e instalación de pasto sintético en Tampico, Madero y Altamira. Showroom en Cd. Madero, material "
               f"desde ${MIN_RETAIL}/m² e instalado desde ${INST_MIN}/m².")
OG_IMG = f"{SITE}{GAL}/obra-residencial-tampico.webp"
MENSAJE = datos.MENSAJES["pasto-sintetico"]

PREGUNTAS = (
    ("¿Dónde comprar pasto sintético en Tampico?",
     f"En Viveros Terra, en {datos.CALLE}, {datos.COLONIA}, Cd. Madero, frente a Walmart. Tenemos {HOY} en existencia "
     "para llevar hoy; los otros 7 modelos también están en existencia y llegan en 3 a 5 días. Atendemos de lunes a "
     "viernes de 9 a 18 h y sábado de 9 a 14 h."),
    ("¿Cuánto cuesta instalar pasto sintético en Tampico?",
     f"La instalación cuesta desde ${INST_MIN}/m² y hasta ${INST_MAX}/m² en modelos premium. Incluye el material, la "
     "colocación, las uniones, las orillas y el cepillado. Si tu espacio necesita retiro de lo existente, nivelación o "
     "base drenante, lo revisamos en la visita y te lo cotizamos aparte antes de empezar."),
    ("¿Cuánto cuesta el pasto sintético por m² en Tampico?",
     f"Solo el material cuesta desde ${MIN_RETAIL}/m² en rollo completo. Toscana 18 va de ${T18['rollo']}/m² en rollo a "
     f"${T18['t1']}/m² en cortes de 2 a 9 m². Toscana 28 va de ${T28['rollo']}/m² a ${T28['t1']}/m². Los precios "
     "incluyen IVA."),
    ("¿Cuál es la compra mínima?",
     "En el showroom vendemos desde 2 m². El rollo mide 2 m de ancho, así que los cortes van de 2 en 2 m²."),
    ("¿Puedo recogerlo el mismo día?",
     f"Sí, si es {HOY}. Te recomendamos confirmar existencia por WhatsApp antes de pasar. Los demás modelos llegan en 3 "
     "a 5 días hábiles. Los pedimos en cuanto confirmas tu pedido con el pago."),
    ("¿Hacen envío dentro de Tampico, Madero y Altamira?",
     "Sí. El envío local cuesta desde $250 según el volumen y la zona. Te lo cotizamos por WhatsApp."),
    ("¿Qué pasto sintético conviene para el clima de Tampico?",
     "Uno con base perforada que drene rápido, porque de junio a septiembre llueve mucho. Para jardín familiar, Toscana "
     "28. Para perros o mucho uso, Irlanda 25 o Capri 20. Para terrazas y balcones, Aruba 10 o Toscana 18. Compara los "
     'modelos en la <a href="/pasto-sintetico#comparativa">tabla de la colección</a>.'),
    ("¿Cuánto dura el pasto sintético?",
     "Bien instalado dura de 8 a 12 años en uso residencial. La garantía de fábrica va de 3 a 8 años según el modelo."),
    ("¿Cómo se paga y dan factura?",
     f"Aceptamos efectivo, transferencia y tarjeta de débito o crédito. {datos.ANTICIPO} Emitimos factura "
     f"{datos.FACTURA} para persona física o moral."),
    ("¿Venden fuera de Tampico?",
     "Sí. Enviamos el material a todo México en 3 a 5 días hábiles. La instalación es solo en Tampico, Madero y "
     'Altamira. Ve la <a href="/pasto-sintetico">tienda con envío nacional</a>.'),
)

PASOS = (
    {"titulo": "Visita y medición", "quien": "nosotros", "cuando": "Antes de cotizar",
     "texto": "Medimos el área, revisamos el terreno y te recomendamos el modelo según el uso."},
    {"titulo": "Preparación del terreno", "quien": "nosotros", "cuando": "Si hace falta",
     "texto": ("Si hace falta, retiramos lo existente, nivelamos y ponemos grava fina para que drene. Se cotiza aparte "
               "según tu espacio.")},
    {"titulo": "Colocación", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Extendemos el rollo, cortamos al perímetro y unimos los tramos con cinta y adhesivo."},
    {"titulo": "Orillas y acabados", "quien": "nosotros", "cuando": "Día de instalación",
     "texto": "Fijamos las orillas para que no se levanten y cuidamos los bordes con andadores y jardineras."},
    {"titulo": "Cepillado y entrega", "quien": "juntos", "cuando": "Al terminar",
     "texto": "Cepillamos la fibra para que quede de pie, limpiamos y revisamos contigo el área antes de irnos."},
)


def _fila_precio(m):
    disponible = "Para llevar hoy" if m["stock"] else "3 a 5 días"
    return (f'<a href="/pasto-sintetico/{m["slug"]}">{m["nombre"]}</a><br><small>{m["mm"]} mm · {disponible}</small>',
            f"${m['t1']}", f"${m['t2']}", f"<b>${m['rollo']}</b>")


SERVICIO = {
    "@type": "Service", "@id": f"{URL}#instalacion", "name": "Instalación de pasto sintético en Tampico",
    "serviceType": "Instalación de pasto sintético", "provider": {"@id": NEGOCIO},
    "areaServed": [{"@type": "City", "name": c} for c in ("Tampico", "Ciudad Madero", "Altamira")],
    "offers": {"@type": "AggregateOffer", "priceCurrency": "MXN", "lowPrice": str(INST_MIN), "highPrice": str(INST_MAX),
               "unitText": "m²"},
}
NEGOCIO_LD = {
    "@type": ["LocalBusiness", "Store"], "@id": NEGOCIO, "name": datos.NOMBRE, "url": SITE,
    "telephone": datos.TELEFONO_TEL, "priceRange": "$$", "foundingDate": datos.FUNDACION,
    "address": {"@type": "PostalAddress", "streetAddress": datos.CALLE,
                "addressLocality": datos.CIUDAD, "addressRegion": "Tamaulipas", "postalCode": datos.CP,
                "addressCountry": "MX"},
    "geo": {"@type": "GeoCoordinates", "latitude": datos.GEO[0], "longitude": datos.GEO[1]},
    "hasMap": datos.MAPS_URL,
    "knowsAbout": ["Pasto sintético", "Instalación de pasto sintético", "Pasto en rollo", "Jardinería"],
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@id": f"{SITE}/pasto-sintetico/{m['slug']}#producto"}}
                   for m in data.MODELOS] + [{"@type": "Offer", "itemOffered": {"@id": f"{URL}#instalacion"}}],
}
MIGAS_LD = {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
    {"@type": "ListItem", "position": 2, "name": "Pasto sintético en Tampico", "item": URL},
]}
OBRAS = tuple({"src": f"{GAL}/{n}-sm.webp", "srcset": f"{GAL}/{n}-sm.webp 560w, {GAL}/{n}.webp 960w",
               "sizes": "(min-width: 1024px) 400px, 80vw", "ancho": w, "alto": h, "alt": alt, "numero": i,
               "lugar": cap, "etapa": "Obra en la región"}
              for i, (n, w, h, alt, cap) in enumerate(data.OBRAS, 2))

CONTENIDO = {
    "tipo": "servicio-sintetico",
    "prefijo": "sintetico",
    "meta": {
        "title": TITULO, "description": DESCRIPCION, "robots": "index, follow, max-image-preview:large", "canonical": URL,
        "og": (("og:type", "website"), ("og:site_name", datos.NOMBRE), ("og:url", URL), ("og:title", TITULO),
               ("og:description", DESCRIPCION), ("og:image", OG_IMG), ("og:locale", "es_MX")),
        "twitter": (("twitter:card", "summary_large_image"),),
    },
    "jsonld": {"producto": NEGOCIO_LD, "nodos": (SERVICIO,), "migas": MIGAS_LD,
               "howto": "Cómo instalamos pasto sintético en Tampico", "speakable": ("h1", "h2", ".vt-faq summary")},
    "migas": (("Inicio", "/"), ("Pasto sintético en Tampico", None)),
    "portada": {
        "kicker": "Pasto sintético · Tampico, Madero y Altamira",
        "h1": 'Pasto sintético en Tampico <span class="vt-serif">venta e instalación</span>',
        "lede": (f"Llévate el material desde nuestro showroom en Cd. Madero o déjanos la instalación completa. Vendemos e "
                 f"instalamos en la región desde {datos.DESDE} y enviamos a todo México desde "
                 f"{datos.SINTETICO_NACIONAL_DESDE}."),
        "etiqueta": {
            "codigo": "Sintético · Tampico", "aviso": "Con IVA", "nombre": "Pasto sintético instalado",
            "antes": "Material y colocación · desde", "monto": dinero(INST_MIN), "unidad": "/m²",
            "filas": (("Solo el material, en showroom", f"desde {dinero(MIN_RETAIL)} /m²"),
                      ("Toscana 18 y 28", "para llevar hoy")),
        },
        "mensaje": MENSAJE,
        "tambien": (f'Los 9 modelos en existencia · <a href="#cotizador">calcula tu material</a> · '
                    '<a href="#showroom">cómo llegar al showroom</a>'),
        "foto": {"src": f"{GAL}/obra-proyecto-02-sm.webp", "srcset": f"{GAL}/obra-proyecto-02-sm.webp 560w, "
                 f"{GAL}/obra-proyecto-02.webp 960w", "sizes": "(min-width: 1024px) 560px, 100vw", "ancho": 960,
                 "alto": 1280, "numero": 1, "alt": "Residencia moderna con escalones de piedra y pasto sintético hasta el deck",
                 "lugar": "Residencia con deck", "etapa": "Obra de Viveros Terra"},
    },
    "prueba": {
        "titulo": "Pasto sintético instalado en la región",
        "lede": "Obras con pasto de nuestra colección en casas de Tampico, Madero y Altamira.",
        "figuras": OBRAS,
        "nota": ("Si el terreno no drena, el pasto sintético se encharca y huele en pocos meses. Por eso revisamos la "
                 "base en la visita y, si hace falta grava, te la cotizamos aparte antes de empezar.", "En la visita"),
    },
    "opciones": {
        "titulo": "Compra el material o te lo instalamos",
        "items": (
            {"rotulo": "Opción 1", "titulo": "Compras el material", "precio": MIN_RETAIL, "unidad": "/m²",
             "detalle": "Material con IVA, cortado a tu medida",
             "puntos": ("Desde 2 m², cortado a tu medida", f"{HOY} para llevar hoy",
                        "Kit de pegamento, cinta y clavos", "Envío local desde $250"),
             "mensaje": "Hola, quiero comprar pasto sintético en el showroom. ¿Tienen existencia?\nModelo: ___\nMetros: ___"},
            {"rotulo": "Opción 2", "titulo": "Nosotros lo instalamos", "precio": INST_MIN, "unidad": "/m²",
             "detalle": "Material y colocación", "rec": True,
             "puntos": ("Visita y cotización sin compromiso", "Colocación, uniones, orillas y cepillado",
                        "Material con garantía de fábrica"),
             "nota": ("Cada terreno es distinto. Si el tuyo necesita retiro, nivelación o base drenante, lo vemos en la "
                      "visita y te lo cotizamos aparte, antes de empezar y sin sorpresas."),
             "mensaje": ("Hola, quiero cotizar la instalación de pasto sintético. ¿Pueden venir a medir?\nColonia: ___\n"
                         "Metros aprox.: ___")},
        ),
    },
    "precio": {
        "titulo": "Precio del pasto sintético en Tampico",
        "lede": (f"Precio por m² del material, con IVA. Entre más metros, menor precio. Instalación con material y "
                 f"colocación de ${INST_MIN} a ${INST_MAX}/m² según el modelo."),
        "tabla": {"columnas": ("Modelo", "2 a 9 m²", "10 a 49 m²", "Rollo 50 m²"),
                  "filas": tuple(_fila_precio(m) for m in data.MODELOS)},
        "caption": ("Si el modelo no está en el showroom, llega en 3 a 5 días hábiles. Lo enviamos en cuanto confirmas tu "
                    f"pedido con el pago. Precios vigentes en {datos.ANIO}."),
    },
    "cotizador": {
        "titulo": "Calcula tu material y llévatelo", "titulo_calc": "Calculadora de material", "modelo": "toscana-28",
        "m2": 20,
        "aparte": (
            ("Kit para instalarlo tú", ("Pegamento de contacto industrial, 4 L", "Cinta de unión profesional, 100 m",
                                       "Clavos de fijación de 2″, caja de 5 kg", "Guía de instalación paso a paso"),
             "Un litro de pegamento rinde para unos 6 m de unión. Te ayudamos a calcular cuánto necesitas."),
            ("¿Instalas o construyes?", (),
             "Instaladores y constructoras tienen precio por volumen, existencia prioritaria y crédito para clientes "
             "recurrentes. Escríbenos por WhatsApp con tus metros por obra."),
        ),
    },
    "proceso": {"titulo": "Cómo instalamos en Tampico y Madero",
                "lede": "Cotizamos después de ver el terreno, porque la base es lo que decide cuánto dura el pasto.",
                "pasos": PASOS},
    "garantia": {
        "titulo": "Garantía de fábrica de 3 a 8 años, según el modelo.", "grande": "3–8", "unidad": "años",
        "resumen": "La gestionamos nosotros, con el material que instalamos o que compras en el showroom.",
        "puntos": (("Garantía de fábrica de 3 a 8 años según el modelo; la gestionamos nosotros.", True),
                   ("Bien instalado dura de 8 a 12 años en uso residencial.", True),
                   ("Si tu terreno necesita retiro, nivelación o base drenante, te lo cotizamos aparte antes de empezar.",
                    True),
                   (f"Factura {datos.FACTURA} para persona física o moral.", True),
                   ("Los cortes a medida no tienen devolución.", False)),
        "pie": '<a href="/politicas">Lee las condiciones completas en Políticas y garantías</a>',
    },
    "pago": {
        "titulo": "Cómo se paga: anticipo y mensualidades con tarjeta de crédito.",
        "lede": (f"{datos.ANTICIPO} El resto se liquida según lo acordado en tu cotización, de contado o en mensualidades "
                 "con tarjeta de crédito."),
        "puntos": ("Recibes el precio del material, la instalación y la preparación del terreno por separado.",
                   "Contado (transferencia, efectivo o tarjeta en una exhibición): el precio más bajo.",
                   ("Mensualidades con tarjeta de crédito: el total a plazos es mayor que el de contado y te lo mostramos "
                    'antes de enviarte el link de pago. <a href="/politicas#mensualidades">Condiciones</a>')),
    },
    "faq": {"titulo": "Preguntas frecuentes en Tampico", "preguntas": PREGUNTAS},
    "visita": {
        "titulo": "Visítanos en Cd. Madero",
        "lede": f"{datos.REFERENCIA}. Toscana 18 y Toscana 28 para llevar hoy; confirma existencia por WhatsApp antes de pasar.",
        "datos": (("Dirección", datos.CALLE, f"{datos.COLONIA}, {datos.CP} Cd. Madero"),
                  ("Horario", "Lun a vie 9 a 18 h", "Sábado 9 a 14 h"),
                  ("Instalación", "Tampico, Madero", "y Altamira"),
                  ("Envío del material", "Local desde $250", "Nacional en 3 a 5 días hábiles")),
        "mapas": (("Cómo llegar con Google Maps", datos.MAPS_URL), ("Abrir en Apple Maps", APPLE_MAPS)),
    },
    "cierre": {
        "titulo": "¿No estás en Tampico? Enviamos a todo México",
        "lede": ("Los mismos 9 modelos llegan a cualquier estado en 3 a 5 días hábiles, con factura: "
                 '<a href="/pasto-sintetico">ver la tienda nacional</a>. En Tampico, Madero y Altamira, escríbenos y '
                 "cotizamos la instalación."),
        "mensaje": MENSAJE,
    },
    "barra": {"nombre": "Pasto sintético en Tampico", "precio": f"Instalado desde ${INST_MIN}/m²"},
}

PARIDAD = {
    "reemplazos": {},
    "retirados": {},
}
```

(El testimonio "Sofía R. · Cafetería en el centro de Tampico" no se repone: no está en `datos.OPINIONES` ni hay permiso registrado; no es encabezado, así que la paridad no lo lista. "Visita y cotización sin compromiso" se conserva: no promete visita gratis.)

- [ ] **Step 4: Registrar y dejar de generarla en `tools/pasto`**

En `tools/site/generar.py`, antes de la fila del hub agrega `    ("/pasto-sintetico-tampico", "pasto-sintetico-tampico/index.html", "servicio", "sintetico_tampico"),`. En `tools/pasto/build.py` borra `from local import build_local` y `    write(ROOT.parent / "pasto-sintetico-tampico" / "index.html", build_local())`.

- [ ] **Step 5: Build, paridad y todas las pruebas de `tools/site`**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2 && python3 tools/site/build.py | tail -2
python3 tools/site/paridad.py informe /pasto-sintetico-tampico /pasto-en-rollo-tampico
cd tools/site && python3 -m unittest discover -s tests 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|FAILED"
```

Expected: `plantillas: 1 de 25 …` (solo Tampico; pasto en rollo sale igual); luego `0 de 25` y `shell: 0 de 108 …`; las seis categorías en `ok` en las dos; las pruebas en `OK` (la vieja `test_tienda_navegador.py` todavía pasa: sigue habiendo `.spec-card__add` dentro de cada `.spec-card`).

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/plantillas/servicio.py tools/site/contenido/sintetico_tampico.py tools/site/generar.py tools/site/tests/test_generar.py tools/site/tests/test_tienda.py tools/pasto/build.py public/pasto-sintetico-tampico/index.html
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(sintetico-tampico): venta e instalación desde la plantilla de servicio con opciones, cotizador y showroom" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: Retirar los generadores viejos de la tienda

**Files:**
- Delete: `tools/pasto/{ficha,hub,ciudad,perros,local}.py`, `tools/pasto/tests/test_{buybar,ciudad,ficha,hub,lineas_pago,perros,common}.py`
- Modify: `tools/pasto/common.py`, `tools/pasto/precios.py`, `tools/pasto/zonas.py`, `tools/pasto/build.py`, `tools/pasto/tests/test_plan_selector.py`, `tools/pasto/tests/test_shell_regiones.py`

Lo que probaban los archivos borrados ya lo prueban `test_componentes_tienda.py` (regla de altura, selector de estados, barra con precio puesto, totales de ciudad, forma de pago), `test_tienda.py` (existencia, precio puesto, scripts, JSON-LD, perros) y `test_tienda_navegador.py` (Agregar, cotizador). `common.py` se queda solo con lo que usan `/precios` y las zonas hasta 2g; su `head()` deja de pintar la barra de la tienda (esas dos páginas ya pasaban `subnav=False`).

- [ ] **Step 1: Borrar y reescribir las dos pruebas que quedan**

```bash
cd ~/dev/viverosterra-e2b/tools/pasto
git rm -q ficha.py hub.py ciudad.py perros.py local.py tests/test_buybar.py tests/test_ciudad.py tests/test_ficha.py tests/test_hub.py tests/test_lineas_pago.py tests/test_perros.py tests/test_common.py
```

`tools/pasto/tests/test_plan_selector.py`:

```python
# tools/pasto/tests/test_plan_selector.py
"""/precios y las zonas (las únicas páginas que aún genera tools/pasto) no cargan los scripts de la tienda. El selector
de forma de pago de la tienda se prueba en tools/site/tests/test_componentes_tienda.py."""
import unittest

from precios import build_precios
from zonas import ZONAS, build_zona


class SinScriptsDeTiendaTest(unittest.TestCase):
    def test_paginas_sin_cotizador_no_cargan_scripts_de_tienda(self):
        slug, zona = next(iter(ZONAS.items()))
        for html in (build_precios(), build_zona(slug, zona)):
            self.assertNotIn("tienda-pasto.js", html)
            self.assertNotIn("vt-mensualidades.js", html)
            self.assertIn("</head>", html)


if __name__ == "__main__":
    unittest.main()
```

`tools/pasto/tests/test_shell_regiones.py`:

```python
import unittest

from precios import build_precios
from zonas import ZONAS, build_zona


def paginas():
    slug, zona = next(iter(ZONAS.items()))
    return {"precios": build_precios(), "zona": build_zona(slug, zona)}


class RegionesDelShellTest(unittest.TestCase):
    def test_cada_pagina_trae_una_region_de_cada_tipo(self):
        for nombre, html in paginas().items():
            for region in ("head", "header", "footer"):
                with self.subTest(pagina=nombre, region=region):
                    self.assertEqual(html.count(f"<!-- vt:{region} -->"), 1)
                    self.assertEqual(html.count(f"<!-- /vt:{region} -->"), 1)

    def test_main_con_id_y_sin_shell_propio(self):
        for nombre, html in paginas().items():
            with self.subTest(pagina=nombre):
                self.assertEqual(html.count('<main id="main">'), 1)
                for viejo in ('class="site-footer"', "googletagmanager", 'class="skip-link"', '<header class="site-header">',
                              "site-header--sub"):
                    self.assertNotIn(viejo, html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: `common.py` reducido**

Reemplaza todo `tools/pasto/common.py` por:

```python
"""Piezas del HTML viejo que todavía usan /precios y las 6 zonas (tools/pasto/precios.py y zonas.py).

La tienda (hub, fichas, ciudades, perros y sintético en Tampico) sale de tools/site desde la Etapa 2b;
este módulo se borra en la Etapa 2g, cuando /precios y las zonas pasen a sus plantillas.
"""
import json
from html import escape
from urllib.parse import quote

from data import ASSET_VERSION, ESTADOS_ORDEN, SITE, WA_NUMBER

GAL = "/img/pasto-sintetico/galeria"


def esc(text):
    return escape(str(text), quote=True)


def money(n):
    return "${:,.0f}".format(n)


def wa(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def jsonld(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def head(*, title, description, canonical, og_image, og_type, preload_img, preload_srcset, ld, extra=""):
    """<head> y apertura de <body> con las regiones vacías del shell."""
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#F5F3EC">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Viveros Terra">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="es_MX">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{preload_img}" imagesrcset="{preload_srcset}" imagesizes="(min-width: 1024px) 620px, 100vw" fetchpriority="high">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/tienda-pasto.css?v={ASSET_VERSION}">
<script type="application/ld+json">{ld}</script>
{extra}<script src="/js/vt-mensualidades.js?v={ASSET_VERSION}" defer></script>
<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>
<!-- vt:head -->
<!-- /vt:head -->
</head>
<body>
{SYMBOLS}
<!-- vt:header -->
<!-- /vt:header -->
"""


SYMBOLS = """<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <symbol id="i-wa" viewBox="0 0 24 24" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41z"/></symbol>
  <symbol id="i-list" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M1 4h14v12H1zM15 9h4l4 4v3h-8"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M8 13h8M8 17h5"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></symbol>
  <symbol id="i-store" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l1.5-5h15L21 9M3 9h18v11H3zM9 20v-6h6v6"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
</svg>"""

def footer():
    """Región vacía del pie: tools/site/shell.py la llena con el pie único y la barra móvil."""
    return "<!-- vt:footer -->\n<!-- /vt:footer -->\n"


def section_open(num, label, heading_id, heading_html, *, tint=False, section_id=None):
    sid = f' id="{section_id}"' if section_id else ""
    cls = "section section--tint" if tint else "section"
    return f"""<section class="{cls}"{sid} aria-labelledby="{heading_id}">
    <div class="wrap section__grid">
      <p class="section__label"><b>{num:02d}</b>{esc(label)}</p>
      <div>
        <h2 id="{heading_id}">{heading_html}</h2>"""


SECTION_CLOSE = """
      </div>
    </div>
  </section>
"""


def faq_html(faqs):
    items = "\n".join(
        f"          <details><summary>{esc(q)}</summary><p>{a_html}</p></details>" for q, _plain, a_html in faqs
    )
    return f'<div class="faq">\n{items}\n        </div>'


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain}}
            for q, plain, _html in faqs
        ],
    }


from esquema import RETURNS, SELLER, SHIPPING, breadcrumb_schema, product_schema, strip_tags  # noqa: E402,F401
```

En `tools/pasto/precios.py` borra la línea `        subnav=False,` y en `tools/pasto/zonas.py` cambia `ld=ld, subnav=False)` por `ld=ld)`. Reemplaza el docstring de `tools/pasto/build.py` por:

```python
"""Genera /precios, las 6 zonas, el feed de Merchant y las URLs de la tienda en el sitemap, y aplica el shell compartido
de tools/site a las páginas que escribe. La tienda (hub, 9 fichas, 11 ciudades, perros y sintético en Tampico) sale de
tools/site/generar.py desde la Etapa 2b; /precios y las zonas pasan a sus plantillas en la 2g.

Uso: python3 tools/pasto/build.py   (desde la raíz del repo). Para todo el sitio: python3 tools/site/build.py
"""
```

- [ ] **Step 3: Pruebas y build sin cambios en lo publicado**

```bash
cd ~/dev/viverosterra-e2b/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK"
cd ../.. && python3 tools/site/build.py | tail -2 && git status --porcelain public | wc -l
grep -rln "tienda-pasto.css" public --include='*.html' | sort | tr '\n' ' '
```

Expected: `Ran 32 tests` y `OK`; `plantillas: 0 de 25 …`, `shell: 0 de 108 …`; `0`; solo `public/jardineria-*/index.html` (6) y `public/precios/index.html`.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/pasto/common.py tools/pasto/precios.py tools/pasto/zonas.py tools/pasto/build.py tools/pasto/tests/test_plan_selector.py tools/pasto/tests/test_shell_regiones.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "refactor(pasto): fuera los generadores viejos de la tienda; common.py solo para precios y zonas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 14: Pruebas en navegador de la tienda y capturas a cinco anchos

**Files:**
- Modify: `tools/site/tests/test_tienda_navegador.py`, `tools/site/capturas.py`

- [ ] **Step 1: Reemplazar `tools/site/tests/test_tienda_navegador.py`**

```python
"""La tienda de pasto sintético en Chromium (Etapa 2b): cotizador con los casos de J03 §3, lista que llega entera al
WhatsApp, "Agregar" que cabe en su tarjeta, precio en el primer pantallazo móvil, sin desbordar, axe de página completa,
CLS y una sola barra fija abajo. Se saltan sin Playwright (python3 -m pip install playwright==1.48.0)."""
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
from test_navegador import RECORRER_BARRAS  # noqa: E402
from test_plantillas_navegador import AXE, AXE_PAGINA, CLS  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

PAGINAS = ("/pasto-sintetico/", "/pasto-sintetico/toscana-28/", "/pasto-sintetico/envio/monterrey/",
           "/pasto-sintetico/perros/", "/pasto-sintetico-tampico/")
# Precio visible en el primer pantallazo de cada tipo de página.
PRECIO = {"/pasto-sintetico/": "[data-landed-hero] b", "/pasto-sintetico/toscana-28/": ".vt-ficha .vt-etiqueta__precio",
          "/pasto-sintetico/envio/monterrey/": ".vt-portada .vt-lede b",
          "/pasto-sintetico-tampico/": ".vt-portada .vt-etiqueta__precio"}
CORTADOS = """() => Array.from(document.querySelectorAll('.spec-card')).map((card) => {
  const boton = card.querySelector('.spec-card__add');
  const c = card.getBoundingClientRect();
  const b = boton.getBoundingClientRect();
  const cortado = b.right > c.right + 0.5 || boton.scrollWidth > boton.clientWidth + 1;
  return cortado ? card.querySelector('.spec-card__name').textContent.trim() : null;
}).filter(Boolean)"""
LAZY_EN_PANTALLA = """() => Array.from(document.images).filter((i) => {
  const r = i.getBoundingClientRect();
  return i.loading === 'lazy' && r.top < innerHeight && r.bottom > 0 && r.width > 200;
}).map((i) => i.src)"""


def mensaje(page, selector):
    return unquote(page.locator(selector).first.get_attribute("href").split("text=", 1)[1])


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class TiendaNavegadorTest(unittest.TestCase):
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
        contexto.route("**/*", lambda r: r.continue_()
                       if r.request.url.startswith(base) and "/api/" not in r.request.url else r.abort())
        page = contexto.new_page()
        errores = []  # la consola de las 108 páginas la revisa test_navegador; aquí, los errores de JS al interactuar
        page.on("pageerror", lambda e: errores.append(str(e)))
        self.addCleanup(lambda: self.assertEqual(errores, []))
        return page

    def cotizar(self, page, m2, estado):
        page.select_option("#estado", estado)
        page.fill("#m2", str(m2))
        page.dispatch_event("#m2", "input")

    def test_boton_agregar_entero_en_las_9_tarjetas(self):
        for ancho in (320, 1100, 1280, 1440):
            page = self.pagina(ancho)
            page.goto(self.base + "/pasto-sintetico/", wait_until="load")
            with self.subTest(ancho=ancho):
                self.assertEqual(page.locator(".spec-card").count(), 9)
                self.assertEqual(page.evaluate(CORTADOS), [])

    def test_cotizador_con_los_casos_de_j03(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        casos = ((50, "CDMX", "$10,850", {3: "≈ $3,995 al mes", 6: "≈ $2,078 al mes"}),
                 (30, "Yucatán", "$8,270", {3: "≈ $3,045 al mes", 6: "≈ $1,584 al mes"}),
                 (120, "Tamaulipas", "$27,330", {12: "≈ $2,811 al mes"}),
                 (5, "showroom", "$1,395", {}))
        for m2, estado, total, planes in casos:
            self.cotizar(page, m2, estado)
            with self.subTest(m2=m2, estado=estado):
                self.assertEqual(page.inner_text("#q-total"), total)
                for plazo, texto in planes.items():
                    self.assertEqual(page.inner_text(f'#q-plans .plan[data-plan="{plazo}"] [data-plan-amount]'), texto)
        # $1,395 no llega al mínimo de 3 mensualidades ($2,000): solo queda contado.
        self.assertEqual(page.locator('#q-plans .plan input:not([disabled])').count(), 1)

    def test_envio_nacional_bajo_25_m2_bloquea_total_y_mensualidades(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        self.cotizar(page, 20, "Jalisco")
        self.assertEqual(page.inner_text("#q-total"), "—")
        self.assertIn("mínimo es 25 m²", page.inner_text("#q-error"))
        self.assertTrue(page.locator("#q-plans").is_hidden())
        self.assertNotIn("Total estimado", mensaje(page, ".vt-cotizador [data-cta-wa]"))

    def test_lo_agregado_llega_al_whatsapp_de_la_lista_y_del_cotizador(self):
        page = self.pagina()
        page.goto(self.base + "/pasto-sintetico/", wait_until="load")
        page.evaluate("() => localStorage.clear()")
        page.reload(wait_until="load")
        self.assertTrue(page.locator(".vt-subnav__n").is_hidden())
        page.click('[data-add="toscana-18"]')
        page.click('[data-add="irlanda-25"]')
        self.assertEqual(page.inner_text(".vt-subnav__n"), "2")
        page.goto(self.base + "/pasto-sintetico/toscana-28/", wait_until="load")
        self.cotizar(page, 50, "Nuevo León")
        cotizador = mensaje(page, ".vt-cotizador [data-cta-wa]")
        self.assertIn("Toscana 28", cotizador)
        self.assertIn("También en mi lista: Toscana 18 (50 m²), Irlanda 25 (50 m²).", cotizador)
        page.click('.vt-vecino [data-agregar*="viena-30"]')
        page.click(".vt-subnav__lista")
        lista = mensaje(page, "#cot-send")
        for linea in ("• Toscana 18: 50 m²", "• Irlanda 25: 50 m²", "• Viena 30: 50 m²", "Entrega en Nuevo León."):
            self.assertIn(linea, lista)

    def test_precio_y_cta_en_el_primer_pantallazo_movil(self):
        page = self.pagina(375, 812)
        for ruta, selector in PRECIO.items():
            page.goto(self.base + ruta, wait_until="load")
            caja = page.locator(selector).first.bounding_box()
            with self.subTest(ruta=ruta):
                self.assertLessEqual(caja["y"] + caja["height"], 812)
                self.assertEqual(page.evaluate(LAZY_EN_PANTALLA), [])

    def test_sin_desbordar_en_cuatro_anchos(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(sobra, 1)

    def test_axe_de_pagina_completa_sin_violaciones_serias(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in PAGINAS:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_PAGINA), [])

    def test_una_sola_barra_fija_abajo_y_cls_bajo(self):
        page = self.pagina(375, 812)
        for ruta in PAGINAS:
            page.goto(self.base + ruta, wait_until="load")
            with self.subTest(ruta=ruta):
                self.assertLess(page.evaluate(CLS), 0.1)
                self.assertEqual(page.evaluate(RECORRER_BARRAS), "")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr**

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest discover -s tests -p "test_tienda_navegador.py" 2>&1 | grep -E "^(FAIL|ERROR):|AssertionError|^Ran|^OK"`
Expected: `Ran 8 tests` y `OK`. Casos de J03 §3 con la fórmula oficial: 50 m² CDMX $10,850 (3 × $3,995, 6 × $2,078), 30 m² Yucatán $8,270 (3 × $3,045, 6 × $1,584), 120 m² Tamaulipas $27,330 (12 × $2,811), 5 m² showroom $1,395 sin plazos; 20 m² Jalisco bloquea total y mensualidades. Si una aserción de desborde falla a 320, la causa suele ser un hijo de grid sin `min-width:0` o un botón con `white-space:nowrap`: corrígelo en `terra-tienda.css` y vuelve a correr.

- [ ] **Step 3: Capturas de 13 páginas a 320, 375, 768, 1024 y 1440**

En `tools/site/capturas.py`: la primera línea del docstring pasa a `"""Capturas de verificación: 13 páginas a 320, 375, 768, 1024 y 1440 px (página completa) y reporte de`; `PAGINAS` y `ANCHOS` pasan a

```python
PAGINAS = ("/", "/pasto-en-rollo-tampico/", "/pasto-sintetico/", "/pasto-sintetico/toscana-28/",
           "/pasto-sintetico/envio/monterrey/", "/pasto-sintetico/perros/", "/pasto-sintetico-tampico/",
           "/diseno-jardines-tampico/", "/plantas-palmas-arboles-tampico/", "/catalogo.html", "/blog/",
           "/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/")
ANCHOS = (320, 375, 768, 1024, 1440)
```

y `CONOCIDOS = {…}` (el desborde de los chips del hub ya no existe) pasa a `CONOCIDOS = {}`.

Run: `cd ~/dev/viverosterra-e2b && python3 tools/site/capturas.py /tmp/vt-e2b-capturas | head -3`
Expected: `65 capturas en /tmp/vt-e2b-capturas` y `sin desbordamiento horizontal` (o solo páginas viejas que no son de 2b, ya conocidas).

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e2b
git add tools/site/tests/test_tienda_navegador.py tools/site/capturas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(tienda): cotizador con los casos de J03, lista al WhatsApp, primer pantallazo, axe y desborde en la tienda" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 15: Verificación final, puertas de revisión, merge y producción

**Files:** ninguno nuevo (correcciones que pidan los revisores, cada una con su prueba).

- [ ] **Step 1: Todas las suites y build reproducible**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/build.py | tail -2 && python3 tools/site/build.py | tail -2
git status --porcelain | wc -l
cd tools/site && python3 -m unittest discover -s tests 2>&1 | grep -E "^Ran|^OK|FAILED"
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | grep -E "^Ran|^OK"
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | grep -E "^Ran|^OK"
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: las dos corridas con `plantillas: 0 de 25 páginas escritas` y `shell: 0 de 108 páginas actualizadas` (la segunda prueba que el build es reproducible); `0`; `Ran 306 tests` y `OK`; `Ran 32 tests` y `OK`; `Ran 11 tests` y `OK`; `ℹ pass 40` y `ℹ fail 0`.

- [ ] **Step 2: Paridad, reglas, consistencia, feed y presupuestos a la vista**

```bash
cd ~/dev/viverosterra-e2b
python3 tools/site/paridad.py informe $(python3 -c "import sys; sys.path[:0]=['tools/site']; import generar; print(' '.join(r for r, *_ in generar.PAGINAS))") | grep -v ": ok" | grep -vc "^=="
cd tools/site && python3 -m unittest tests/test_reglas.py tests/test_consistencia.py tests/test_paridad.py tests/test_contenido.py tests/test_tienda.py tests/test_terra_css.py tests/test_terra_tienda_css.py 2>&1 | tail -1
cd ../.. && git diff main -- public/feed-pasto-sintetico.xml | wc -l
git diff main -- public/sitemap.xml | wc -l
grep -rniE "oasis|pasto ?plus|\bMSI\b|sin intereses|p[aá]del|gratis|muestras? (gratis|f[ií]sicas?)|visita sin costo|pr[oó]ximo corte" public/pasto-sintetico public/pasto-sintetico-tampico public/js/tienda-pasto.js public/css/terra-tienda.css | grep -v "no ofrecemos muestras f" | wc -l
```

Expected: `0` (todas las rutas con plantilla en `ok`); `OK`; `0` (feed sin cambios); `0` (sitemap sin cambios); `0`.

- [ ] **Step 3: Consola limpia en todas las páginas**

Run: `cd ~/dev/viverosterra-e2b/tools/site && python3 -m unittest tests.test_navegador 2>&1 | tail -1`
Expected: `OK` (incluye 0 `pageerror` y 0 errores de consola en las 108 páginas, y una sola barra fija a la vez).

- [ ] **Step 4: Lighthouse móvil en hub, ficha, ciudad y Tampico**

```bash
cd ~/dev/viverosterra-e2b
(cd public && python3 -m http.server 8765 >/dev/null 2>&1 &) ; sleep 1
export CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()")
for r in pasto-sintetico/ pasto-sintetico/toscana-28/ pasto-sintetico/envio/monterrey/ pasto-sintetico-tampico/; do
  n=$(echo "$r" | tr '/' '_')
  npx -y lighthouse@12.2.1 "http://127.0.0.1:8765/$r" --form-factor=mobile --only-categories=performance,accessibility \
    --chrome-flags="--headless=new" --output=json --output-path="/tmp/vt-e2b-lh-$n.json" --quiet
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); c=d['categories']; a=d['audits']; print(sys.argv[1], round(c['performance']['score']*100), round(c['accessibility']['score']*100), a['cumulative-layout-shift']['numericValue'], a['largest-contentful-paint']['displayValue'])" "/tmp/vt-e2b-lh-$n.json"
done
pkill -f "http.server 8765"
```

Expected (por página): Performance ≥ 90, Accessibility ≥ 95, CLS < 0.1, LCP < 2.5 s. Si Performance queda abajo, anota la causa (`a['largest-contentful-paint-element']`, `a['render-blocking-resources']`) en el PR: GA4 diferido y CSS crítico en línea son de la Etapa 5 y no se adelantan. CLS ≥ 0.1 o un LCP en imagen `lazy` sí bloquean: corrige y vuelve al Step 1.

- [ ] **Step 5: Capturas finales**

Run: `cd ~/dev/viverosterra-e2b && python3 tools/site/capturas.py /tmp/vt-e2b-capturas | head -3`
Expected: `65 capturas …`. Revisa a mano las de `pasto-sintetico*`: una sola etiqueta amarilla en el primer pantallazo móvil y derecha; precio "desde $X/m² · rollo 50 m² · envío por rollo" visible a 375 sin bajar; pies `FIG.` en cada foto; NOSOTROS / TÚ / JUNTOS en "Cómo comprar"; rollo a escala con cotas 25 m × 2 m; "(0)" invisible; nada cortado a 320; a 1024 la ficha a dos columnas sin huecos; la barra de compra solo en celular y nunca junto a la del shell.

- [ ] **Step 6: Abrir el PR**

```bash
cd ~/dev/viverosterra-e2b
git push -u origin feat/etapa-2b
gh pr create --base main --head feat/etapa-2b --title "Etapa 2b · Plantillas: pasto sintético (tienda, fichas, ciudades, perros, Tampico)" --body "$(cat <<'EOF'
## Qué cambia
- Las 25 páginas de sintético salen de `tools/site` (plantillas `ficha`, `tienda_hub`, `tienda_guia` y `servicio`); `tools/pasto` queda como capa de datos (modelos, zonas, fletes, ciudades, mensualidades, feed, sitemap, `esquema.py`).
- Sistema híbrido (Archivo + Fraunces, etiqueta, cuadro de datos, `FIG.`, NOSOTROS/TÚ/JUNTOS); fuera Geist, Instrument Serif, Google Fonts y `tienda-pasto.css` en estas páginas (queda solo en /precios y zonas hasta 2g).
- `terra-tienda.css` (3.8 KB gzip) solo en la tienda; copias CSS minificadas al publicar (`terra.css` 8.3 KB gzip).
- Ficha: etiqueta "desde $X/m² · rollo 50 m² · envío por rollo" en el primer pantallazo, foto principal precargada (nunca lazy), rollo a escala, 2 vecinos con Agregar.
- Lo que se agrega a la lista llega también al WhatsApp del cotizador; "(0)" oculto; hub sin desborde a 320.
- Ciudades: respuesta directa, tabla 25/50/100 con mensualidad, encabezados en pregunta; barra móvil del shell.
- `mensualidades.py` redondea como `Math.round` (Monterrey y Veracruz: 12 × $1,667, antes $1,666).
- `activos.py` conserva la copia con hash que sirve producción (registro `activos.json`), no la de fecha más nueva.
- Título, descripción, canonical, Open Graph y tipos de JSON-LD intactos (paridad); feed de Merchant y sitemap sin cambios.

## Verificación
- [ ] Build reproducible y 4 suites en verde (306 + 32 + 11 + 40)
- [ ] Lighthouse móvil (hub, ficha, ciudad, Tampico: Perf, A11y, CLS, LCP)
- [ ] Capturas a 320/375/768/1024/1440 (comentario con imágenes)
- [ ] Puertas: diseño, SEO/AEO, CRO, cumplimiento/QA
- [ ] Vista previa de Vercel aprobada por el dueño

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
gh pr view --json url --jq .url
```

Expected: la URL del PR; Vercel comenta la vista previa.

- [ ] **Step 7: Puertas de revisión en paralelo (spec §11)**

Lanza los cuatro revisores a la vez (una respuesta con cuatro llamadas). A cada uno: `git diff main...feat/etapa-2b --stat`, `tools/site/componentes_tienda.py`, `plantillas/{ficha,tienda_hub,tienda_guia,servicio}.py`, `contenido/{ficha,tienda,ciudad,perros,sintetico_tampico}.py`, `public/css/terra-tienda.css`, el diff de `public/js/tienda-pasto.js`, la URL de la vista previa, `/tmp/vt-e2b-capturas`, los JSON de Lighthouse, la salida de `paridad.py informe`, la referencia `docs/diseno/hibrido/ficha.html`, las notas del jurado (`…/scratchpad/design/jurado/01-conversion.md`, `02-diseno.md`, `03-calidad-cumplimiento.md`) y el spec (§3.3, §4, §5, §6, §7.3, §8, §10, §11). Cada hallazgo se clasifica crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido y a `ficha.html` (etiqueta derecha y una por pantalla móvil; Fraunces solo en notas y en la frase en itálica del H1; regla de altura y rollo a escala en café de medida; amarillo solo en precio), jerarquía de la ficha a 375 y 1440, foco ≥ 3:1 en chips, planes, stepper y miniaturas, objetivos ≥ 44 px, `dialog` de la lista operable con teclado (Escape cierra, foco vuelve), contraste en el cierre verde, que las páginas viejas no cambiaron (3 capturas antes/después de páginas fuera de 2b).
2. **SEO/AEO** (`seo-specialist` con `seo-audit`, `ai-seo`, `schema-markup`): `git diff main...feat/etapa-2b -- 'public/pasto-sintetico*' | grep -E '^[-+].*(<title>|name="description"|rel="canonical"|property="og:)'` vacío; JSON-LD válido (Rich Results Test sobre la vista previa de ficha, hub, ciudad y Tampico: Product con `shippingDetails` y `hasMerchantReturnPolicy`, ItemList, FAQPage, HowTo, LocalBusiness/Store); un H1 por página y orden h1 → h2 → h3 (el cotizador de la ficha es h2 dentro de la portada; en hub y Tampico, h3); encabezados en pregunta de las ciudades; enlazado interno conservado (paridad); feed de Merchant intacto.
3. **CRO** (`general-purpose` con `page-cro`): primer pantallazo móvil de cada tipo (qué, precio "desde", envío por rollo, CTA); flujo Agregar → lista → WhatsApp con todos los modelos, estado y total; mensaje del cotizador con "También en mi lista"; bloqueo bajo 25 m² explicado; barra de compra con precio puesto; ciudades con CTA fijo (barra del shell) y botón al cotizador con el estado; Tampico con dos opciones y un mensaje cada una; `generate_lead` (`whatsapp_cotizador`, `whatsapp_lista`) y `add_to_cart` en DebugView de la vista previa.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `typescript-reviewer` para el JS + `e2e-runner`): reglas del dueño (Step 2), datos solo de `data.py` / `datos.py`, fórmula de mensualidades sin reimplementar (Python ↔ JS con `casos-mensualidades.json`), `activos.json` coherente con lo que hay en disco y con lo que sirve `main`, calidad de `tools/site/` (funciones < 50 líneas, archivos < 800), que `tools/pasto` ya no genera la tienda, que no se versionó `.DS_Store`.

Corrige en la rama todo crítico o alto (prueba, commit, nueva corrida del Step 1) y vuelve a pedir revisión a quien lo levantó; los medios se corrigen o se anotan en el PR con su motivo.

- [ ] **Step 8: Aprobación del dueño**

Comparte la vista previa y las capturas. No hagas merge sin su "sí" explícito. Pídele en el mismo mensaje lo que aparece en "Lo que aporta el dueño".

- [ ] **Step 9: Merge, push y despliegue (lo hace el controlador)**

```bash
cd ~/dev/viverosterra
git checkout -- .DS_Store 2>/dev/null; git checkout main && git pull --ff-only
git merge --no-ff feat/etapa-2b -m "feat: etapa 2b, plantillas de pasto sintético" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
python3 tools/site/build.py | tail -2 && git status --porcelain | wc -l
git push origin main
```

Expected: `plantillas: 0 de 25 …`, `shell: 0 de 108 …` y `0` (en `main`, el registro de `activos.json` ya coincide con lo publicado: no rota nada); Vercel despliega `main` (Deployments → `Ready`).

- [ ] **Step 10: Verificación en vivo**

```bash
W=https://www.viverosterra.com
curl -s $W/pasto-sintetico/toscana-28 | grep -o "<title>[^<]*</title>"
curl -s $W/pasto-sintetico/toscana-28 | grep -cE "tienda-pasto.css|fonts.googleapis|Geist"
curl -s $W/pasto-sintetico/toscana-28 | grep -oE '/css/terra-tienda\.[0-9a-f]{10}\.css' | head -1 | xargs -I{} curl -sI $W{} | grep -iE "^HTTP|cache-control"
curl -s $W/pasto-sintetico/envio/monterrey | grep -o "12 × ≈ \$1,667"
curl -s $W/pasto-sintetico-tampico | grep -c "los otros 7 modelos también están en existencia"
curl -s $W/feed-pasto-sintetico.xml | grep -c "<g:price>"
for u in $(python3 -c "import json; print(' '.join(v for vs in json.load(open('tools/site/activos.json')).values() for v in vs))"); do curl -s -o /dev/null -w "%{http_code} $u\n" $W$u; done
```

Expected: `<title>Pasto Sintético Toscana 28 desde $199/m² · Envío a Todo México</title>`; `0`; `HTTP/2 200` y `cache-control: public, max-age=31536000, immutable`; `12 × ≈ $1,667`; `1`; `9`; `200` en cada copia del registro (la actual y la que servía producción antes del deploy). En Chrome (escritorio y emulación de iPhone): consola sin errores; en una ficha, CDMX con 50 m² da $10,850; "+ Agregar" de un vecino suma a "Mi lista" y el WhatsApp del cotizador dice "También en mi lista"; el hub con `?estado=nuevo-leon` muestra precios puestos. En GA4 DebugView: `add_to_cart`, `view_cart` y `generate_lead` con `whatsapp_cotizador` y `whatsapp_lista`.

- [ ] **Step 11: Si algo crítico falla en vivo**

Vercel → Deployments → el anterior → "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`. Corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 12: Limpiar**

```bash
cd ~/dev/viverosterra && git worktree remove ~/dev/viverosterra-e2b && git branch -d feat/etapa-2b
```

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Romper `tienda-pasto.js` / `tienda-hub.js` al cambiar el marcado | `test_componentes_tienda.test_trae_cada_id_que_busca_tienda_pasto_js` compara cada `$('#…')` del JS con los `id` del marcado; pruebas de navegador del cotizador, la lista, Agregar y el selector; consola limpia en las 108 páginas. |
| `activos.json` desalineado (alguien borra o agrega copias a mano) | `test_activos.test_registro_del_repo_coincide_con_lo_publicado` exige que las copias en disco sean exactamente las del registro y que la primera sea la de la fuente actual. Sin git (zip), se toma lo que enlaza el HTML en disco. |
| La minificación cambia el hash de todas las hojas y la copia `terra.3eaa08fd32.css` restaurada en la Tarea 1 sale con la 2b | Es lo esperado: al desplegar 2b se conserva la que sirve producción en ese momento (`ed57…`). Si se quiere reponer `3eaa…` ya, el commit de la Tarea 1 se lleva solo a `main` antes del lote. |
| Presupuesto de `terra.css` otra vez al límite en 2c–2i | La copia publicada mide 8.3 KB gzip (1.9 KB de margen); los componentes de un solo tipo de página van a su hoja (`terra-<tipo>.css`) con el mismo mecanismo (`clase_body` + `shell.TIENDA`). |
| Lighthouse Performance < 90 en la ficha por la galería y GA4 | La foto principal es la `-sm` (420 px) precargada y la única no `lazy`; si aún queda abajo, se documenta y se resuelve en la Etapa 5 (GA4 diferido, CSS crítico). |
| `<script>` en línea del precio puesto (ficha y guías) con la CSP en enforce | Es el mismo que ya publicaba la ficha; la CSP sigue en Report-Only hasta la Etapa 5, que lo pasa a archivo con hash. |
| Fotos de producto y de obra que parecen render | Pies `FIG.` con "Foto de producto" / "Obra con pasto sintético"; se sustituyen con la sesión real cambiando solo `src` en el contenido. |
| `/precios` y las 6 zonas siguen con `tienda-pasto.css` y `common.py` | Fuera de 2b a propósito (2g); `test_shell_regiones.py` y `test_plan_selector.py` los mantienen sanos hasta entonces. |

## Lo que aporta el dueño

1. Confirmar si el testimonio "Sofía R. · Cafetería en el centro de Tampico" era real; si lo es, nombre y permiso por escrito para reponerlo en `datos.OPINIONES` (hoy se retira).
2. Confirmar que se mantienen "crédito para clientes recurrentes" (instaladores y constructoras) y "Envío local desde $250" en Tampico, que ya publicaba la página.
3. Fotos reales de la sesión de medio día con pasto sintético instalado en Tampico (sustituyen las de obra con pie "Obra con pasto sintético").
4. Aprobación de la vista previa antes del merge.
