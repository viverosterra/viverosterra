# Etapa 1 · Fundaciones — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sub-plan **1a de 2** de la Etapa 1 de `docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md`: fuente única de datos (`tools/site/datos.py`), shell compartido (head esencial, menú de 6 entradas, pie único y barra fija móvil de WhatsApp) aplicado por el build a las 108 páginas de `public/`, `terra.css` con los tokens del híbrido "Plano + Etiqueta" y fuentes autoalojadas, `terra.js` con eventos GA4 `generate_lead` / `click_to_call` en todas las páginas, `legacy-fixes.css`, arreglos técnicos rápidos (robots, borrador, enlace roto, guía de palmas retirada, CSP en Report-Only, caché inmutable con hash), pruebas del §9 que aplican a esta parte y CI en GitHub Actions. Se publica sola: el sitio queda coherente (un solo menú y un solo pie en todas las páginas) aunque los cuerpos viejos sigan iguales hasta la Etapa 2. **Orden:** 1a primero; 1b (`2026-11-07-etapa-1b-fundaciones-datos.md`: contradicciones de datos, "209 Sur" en los cuerpos, promesa única, reglas de consistencia) después, sobre `main` ya con 1a.

**Architecture:** Un paquete nuevo `tools/site/` (Python estándar, sin dependencias de build) es dueño del shell. Cada página de `public/` lleva tres regiones marcadas con comentarios: `<!-- vt:head -->…<!-- /vt:head -->` (al final del `<head>`), `<!-- vt:header -->…<!-- /vt:header -->` (justo después de `<body>`) y `<!-- vt:footer -->…<!-- /vt:footer -->` (justo antes de `</body>`). `tools/site/shell.py` reemplaza el contenido de esas regiones por los parciales canónicos de `tools/site/partials.py` (que leen `datos.py` y el contexto de cada ruta en `paginas.py`) y marca con `data-cta` los enlaces de WhatsApp y teléfono del cuerpo; es idempotente. Las 30 páginas generadas por `tools/pasto` emiten las regiones vacías y su build les aplica el shell; las 78 páginas a mano reciben las regiones con una migración única (`tools/site/migrar_shell.py`) que quita su menú, pie, botón flotante, gtag duplicado y meta heredadas, y envuelve el contenido en `<main id="main">`. `tools/site/build.py` es el único punto de entrada (genera pasto, publica assets con hash, aplica el shell a todo `public/`), y CI comprueba que el build reproduce `public/` byte por byte. **Convivencia con el CSS viejo:** en la Etapa 1, `terra.css` solo contiene custom properties `--vt-*`, `@font-face` y selectores que empiezan con `.vt-` (nombres verificados para no chocar con los `vt-hero`, `vt-stickybar`, etc. que ya existen); no toca `body`, `h2`, `a` ni ningún elemento suelto, así que los cuerpos viejos se ven igual. Los parciales fijan explícitamente fuente, tamaño, margen y color de cada pieza del shell para que las reglas viejas de elemento (p. ej. `h2{font-family:Playfair…}` en 41 posts, `footer{text-align:center}`) no los alteren. `tailwind.css`, `design-system.css`, `servicios.css` y `tienda-pasto.css` se siguen cargando hasta la Etapa 2; `legacy-fixes.css` (solo en páginas que cargan Tailwind) agrega las 49 utilidades que faltan. **Decisión sobre `content/`:** el spec propone mover los cuerpos a `content/<slug>.html`; en esta etapa el build ya es dueño del shell de las 108 páginas (prueba de deriva + `git diff --exit-code public/` en CI), y la extracción de cuerpos se hace en la Etapa 2, cuando cada tipo de página pasa a su plantilla de `tools/site/plantillas/`; moverlos ahora para reescribirlos semanas después sería doble trabajo y doble riesgo.

**Tech Stack:** Python 3.9+ estándar (local 3.9.6, CI 3.12) para build y pruebas (`unittest`); Playwright para Python 1.48 solo en pruebas de navegador (se saltan si no está instalado); CSS plano; JavaScript vanilla con `node --test`; GitHub Actions; Vercel (`vercel.json`, sin build command: se publica `public/` tal cual).

---

## Cobertura del spec (Etapa 1, §10) y qué queda para después

| Alcance de la Etapa 1 | Dónde |
|---|---|
| 1. Medición: `data-cta` + `terra.js` + gtag en las 11 páginas que faltaban; línea base de 2 semanas | 1a: Tareas 7, 11, 15, 25 (Step 10) |
| 2. `tools/site/` (datos, parciales, build) con todas las páginas pasando por el build | 1a: Tareas 2–3, 8–15. Los cuerpos pasan a `content/`/plantillas en la Etapa 2 (ver Architecture) |
| 3. Tokens y fuentes congelados; `terra.css` | 1a: Tareas 4–5 (componentes del shell; el resto entra con su plantilla en la Etapa 2) |
| 4. Header, pie y barra móvil nuevos en todas las páginas (menú de 6, promesa única, "209 Sur"); `legacy-fixes.css` | 1a: Tareas 6, 9–10, 13, 15 |
| 5. Contradicciones del §5.2; botón "+ Agregar" de la tienda a 1440 | 1b |
| 6. robots (AdsBot, CCBot, bots de búsqueda), apex 308, `noindex` del cuestionario, borrador, enlace roto y PNG, meta heredadas, CSP Report-Only | 1a: Tareas 14, 16, 18, 19, 25 (Step 8); meta heredadas en la Tarea 12 |
| 6. `/precios` y `/vivero-tampico` en `llms.txt`; `sameAs` corregido | 1b (el pie de 1a ya usa los perfiles correctos de `datos.REDES`) |
| 7. Pruebas del §9 y CI; limpieza del repo y de `scripts/` | 1a: Tareas 2–24 (unitarias, deriva, enlaces, reglas, consola, axe del shell, CI) y 21; consistencia de datos en 1b |
| Decisiones del dueño del 2026-11-07 | Datos en `datos.py` (1a, Tarea 2); guía de palmas retirada (1a, Tarea 17); framboyán $250 y "próximo corte" retirado (1b) |

Pruebas del §9 que no entran en la Etapa 1 porque fallarían hasta que su etapa corrija el contenido: SEO on-page estricto (un H1, título ≤ 65, descripción ≤ 160, `og:image`, `width`/`height` en `<img>`) llega con la reescritura de títulos de la Etapa 3; JSON-LD con un solo nodo `#negocio`, en la Etapa 4; comparación visual contra capturas de referencia aprobadas, en la Etapa 2 (cuando existan las plantillas); axe de página completa (no solo del shell), en la Etapa 2.

## Reglas para quien ejecuta

- Trabaja solo en `~/dev/viverosterra-e1` (rama `feat/etapa-1`). Nunca en `~/Documents/GitHub/viverosterra` (iCloud).
- Commits en español, convencionales, con este formato exacto (rutas explícitas en `git add`, nunca `.DS_Store`):
  `git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "<msg>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"`
- Si un build solo cambia `lastmod` en `public/sitemap.xml`, restáuralo con `git checkout -- public/sitemap.xml` antes de hacer commit (desde la Tarea 13 el generador ya no lo toca).
- Pruebas: `cd tools/site && python3 -m unittest discover -s tests`, `cd tools/pasto && python3 -m unittest discover -s tests -t .`, `cd tools/servicios && python3 -m unittest discover -s tests -t tests`, `node --test public/js/tests/*.test.js` (forma con glob; la forma de directorio falla en Node 24).
- Reglas del dueño que ninguna línea nueva puede romper: nunca "Oasis"; nunca marcas de proveedor (PastoPlus); nunca el nombre del proveedor de la terminal en `public/`; nada de "MSI", "sin intereses" ni "0%" en pagos; sin pádel ni canchas para sintético; sin muestras físicas; envío de sintético nunca "gratis"; "para llevar hoy" solo Toscana 18 y 28; el primer riego lo hace el cliente, dicho en positivo; nunca "pagas cuando ves tu jardín terminado"; promesa "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h"; domicilio "Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamps." (frente a Walmart, entrando por Banamex); WhatsApp +52 833 326 8008; desde 2007; REPSE 773725; +500,000 m² instalados; "4.6 en Google (24 reseñas)".

## File structure

Se crean:

| Archivo | Responsabilidad única |
|---|---|
| `tools/site/datos.py` | Fuente única de datos del sitio: contacto, domicilio, horario, promesa, cifras, precios oficiales, garantías, decisiones del dueño, redes y mensajes de WhatsApp. |
| `tools/site/paginas.py` | Contexto por ruta (tipo de página para `data-cta`, sección activa del menú, servicio, si lleva barra móvil); falla con rutas sin contexto. |
| `tools/site/activos.py` | Publica copias con hash de `terra.css`, `terra.js` y `legacy-fixes.css` y borra las viejas. |
| `tools/site/partials.py` | Genera las regiones del shell: head esencial, menú (escritorio y móvil), pie y barra fija móvil. |
| `tools/site/shell.py` | Reemplaza las regiones del shell en cualquier página, marca `data-cta` en el cuerpo, recorre `public/`. |
| `tools/site/migrar_shell.py` | Migración única de las páginas a mano: quita shell viejo e inserta regiones y `<main>`. |
| `tools/site/build.py` | Punto de entrada único del sitio (pasto → assets con hash → shell en todo `public/`). |
| `tools/site/servidor.py` | Servidor HTTP local de `public/` para pruebas de navegador y capturas. |
| `tools/site/capturas.py` | Capturas a 320/375/1440 de 10 páginas y reporte de desbordamiento (verificación manual). |
| `tools/site/vendor/axe.min.js` | axe-core 4.10.2 versionado para las pruebas de accesibilidad. |
| `tools/site/tests/test_datos.py` | Pruebas de `datos.py`. |
| `tools/site/tests/test_paginas.py` | Pruebas de `paginas.py`. |
| `tools/site/tests/test_fuentes.py` | Fuentes autoalojadas presentes e íntegras. |
| `tools/site/tests/test_terra_css.py` | Convivencia (`.vt-` en todo selector), tokens, contraste AA, presupuesto. |
| `tools/site/tests/test_legacy_fixes.py` | Ninguna utilidad de Tailwind usada queda sin definir. |
| `tools/site/tests/test_paridad_terra_js.py` | La firma del mensaje es igual en Python y JS. |
| `tools/site/tests/test_activos.py` | Pruebas de `activos.py`. |
| `tools/site/tests/test_partials.py` | Pruebas del head y del menú. |
| `tools/site/tests/test_partials_pie.py` | Pruebas del pie y de la barra móvil. |
| `tools/site/tests/test_shell.py` | Pruebas de `shell.py`. |
| `tools/site/tests/test_migrar_shell.py` | Pruebas de la migración con una muestra de cada familia de página. |
| `tools/site/tests/test_sitio.py` | Todo `public/`: 108 páginas con contexto, shell sin deriva, un `<main>`, gtag único, shell viejo retirado, `data-cta`, assets con hash. |
| `tools/site/tests/test_borrador.py` | Borrador eliminado y redirigido. |
| `tools/site/tests/test_enlaces.py` | Enlaces y recursos locales existen; redirects sin cadenas; `noindex` en páginas de utilidad. |
| `tools/site/tests/test_guia_palmas.py` | Guía de palmas retirada y su URL redirigida. |
| `tools/site/tests/test_robots.py` | `robots.txt` sin bloqueos y con los bots de búsqueda e IA. |
| `tools/site/tests/test_vercel.py` | CSP Report-Only, sin `X-XSS-Protection`, caché inmutable de assets con hash. |
| `tools/site/tests/test_limpieza.py` | La raíz del repo no vuelve a acumular copias viejas ni `.DS_Store`. |
| `tools/site/tests/test_ci.py` | El workflow corre el build reproducible y todas las suites. |
| `tools/site/tests/test_reglas.py` | Palabras y frases prohibidas por el dueño en todo lo publicado. |
| `tools/site/tests/test_navegador.py` | Playwright: consola limpia en las 108 páginas, axe del shell, menú, barra, eventos GA4, shell sin desbordar. |
| `tools/pasto/tests/test_shell_regiones.py` | Las páginas generadas traen regiones del shell y `<main id="main">`. |
| `public/css/terra.css` | Tokens del híbrido y componentes del shell (fuente; el build publica la copia con hash). |
| `public/css/legacy-fixes.css` | Las 49 utilidades de Tailwind que faltan (se borra al cerrar la Etapa 2). |
| `public/js/terra.js` | Menú, barra móvil y medición GA4 por delegación de clics; firma "Vengo de viverosterra.com". |
| `public/js/tests/terra.test.js` | Pruebas de las funciones puras de `terra.js`. |
| `public/fonts/archivo-latin.woff2`, `public/fonts/fraunces-italic-latin.woff2` | Fuentes del híbrido autoalojadas (subset latin). |
| `public/css/terra.<hash>.css`, `public/css/legacy-fixes.<hash>.css`, `public/js/terra.<hash>.js` | Copias con hash que sirven las páginas (generadas por el build, se versionan). |
| `.github/workflows/sitio.yml` | CI: build reproducible + todas las pruebas en cada push y PR. |
| `docs/diseno/hibrido/` | Copia de la maqueta aprobada (referencia de componentes; no se sirve). |

Se modifican:

| Archivo | Cambio |
|---|---|
| `tools/pasto/build.py` | Registra las páginas escritas, conserva `lastmod` y les aplica el shell al final. |
| `tools/pasto/sitemap.py` | `upsert(..., conservar=True)` no toca `lastmod` de URLs existentes. |
| `tools/pasto/common.py` | `head()` emite regiones vacías y la barra contextual de la tienda; `footer()` emite la región; sin gtag, favicon ni skip-link propios. |
| `tools/pasto/precios.py`, `zonas.py`, `hub.py`, `ficha.py`, `ciudad.py`, `perros.py`, `local.py` | Sin header/footer propios, `<main id="main">`, sin reemplazos de skip-link. |
| `tools/pasto/tests/test_sitemap.py` | Prueba de `conservar`. |
| `public/css/tienda-pasto.css` | Barra contextual de la tienda bajo el menú principal; contador "(0)" oculto. |
| 108 × `public/**/*.html` | Shell nuevo (migración + build). |
| `public/blog/tezontle-usos-jardin-tampico/index.html`, `public/blog/tierra-negra-costal-camion-tampico/index.html` | Enlace roto y PNG inexistente. |
| `public/cuestionario.html` | `noindex, follow`. |
| `public/palmas-mayoreo-proyectos/index.html` | Se retira la guía de palmas (sección, formulario y script). |
| `public/robots.txt` | AdsBot sin bloqueos, CCBot permitido, bots de búsqueda de IA listados. |
| `vercel.json` | Redirects del borrador y del PDF; CSP en Report-Only; sin `X-XSS-Protection`; caché inmutable de assets con hash. |
| `.gitignore` | Ignora `__pycache__/` y `*.pyc` (y `.DS_Store` sale del índice). |

Se borran: `public/preview-mapa-cobertura.html`, `public/pdf/guia-12-palmas-arquitectos.pdf`, `public/js/nav-scroll.js`, y de la raíz del repo (no se sirven, `outputDirectory` es `public`): `index.html`, `catalogo.html`, `catalogo/`, `cuestionario/`, las 20 imágenes sueltas, `logo-viveros-terra-*.svg/png` de la raíz, `scripts/`, `src/`, `tailwind.config.js`.

---

### Task 0: Worktree y línea base

**Files:** ninguno.

- [ ] **Step 1: Crear el worktree desde `main` actualizado**

```bash
cd ~/dev/viverosterra
git checkout main
git pull --ff-only
git worktree add ~/dev/viverosterra-e1 -b feat/etapa-1
cd ~/dev/viverosterra-e1
git log --oneline -1
```

Expected: una línea con el último commit de `main` (el que agrega este plan).

- [ ] **Step 2: Correr las pruebas existentes (línea base)**

```bash
cd ~/dev/viverosterra-e1/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -3
cd ~/dev/viverosterra-e1/tools/servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
cd ~/dev/viverosterra-e1 && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
find public -name '*.html' | wc -l
```

Expected: `Ran 53 tests` + `OK`; `Ran 10 tests` + `OK`; `ℹ pass 6` y `ℹ fail 0`; `109`.

- [ ] **Step 3: Instalar Playwright para las pruebas de navegador (solo local, no es dependencia del build)**

```bash
python3 -m pip install --user playwright==1.48.0
python3 -m playwright install chromium
python3 -c "import playwright; print('playwright ok')"
```

Expected: `playwright ok`. Si la máquina no permite instalarlo, las pruebas de `test_navegador.py` se saltan localmente y corren en CI.

- [ ] **Step 4: Dejar de versionar `.DS_Store` e ignorar `__pycache__/` (las pruebas los crean y varios pasos hacen `git add` de carpetas)**

```bash
cd ~/dev/viverosterra-e1
git rm --cached -q .DS_Store public/.DS_Store
printf '__pycache__/\n*.pyc\n' >> .gitignore
git ls-files | grep -cE "DS_Store|__pycache__"
git add .gitignore
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore: dejar de versionar .DS_Store e ignorar __pycache__" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: `0` (y el commit con `.gitignore` y los 2 `.DS_Store` fuera del índice; siguen en disco e ignorados).

---

### Task 1: Copia de la maqueta aprobada como referencia

**Files:**
- Create: `docs/diseno/hibrido/` (index.html, pasto-en-rollo.html, ficha.html, articulo.html, styles.css, app.js, img/)

- [ ] **Step 1: Copiar la maqueta (sin la carpeta `shots/` de 63 MB)**

```bash
cd ~/dev/viverosterra-e1
SRC=/private/tmp/claude-501/-Users-luisgovela-everything-claude-code--claude-worktrees-elastic-banach-f7746e/febdc456-bc99-4b13-96b9-7a52521ffdab/scratchpad/design/hibrido
if [ -d "$SRC" ]; then
  mkdir -p docs/diseno/hibrido
  cp "$SRC"/index.html "$SRC"/pasto-en-rollo.html "$SRC"/ficha.html "$SRC"/articulo.html "$SRC"/styles.css "$SRC"/app.js docs/diseno/hibrido/
  cp -R "$SRC"/img docs/diseno/hibrido/img
  ls docs/diseno/hibrido | wc -l
else
  echo "maqueta no disponible: se omite la copia (este plan trae todo el CSS necesario)"
fi
```

Expected: `7` (6 archivos + `img`), o el mensaje de omisión. Si se omitió, salta al Task 2 sin commit.

- [ ] **Step 2: Commit**

```bash
git add docs/diseno/hibrido
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "docs: maqueta híbrida Plano + Etiqueta como referencia de componentes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Fuente única de datos (`tools/site/datos.py`)

**Files:**
- Create: `tools/site/datos.py`
- Test: `tools/site/tests/test_datos.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_datos.py`:

```python
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402


class DatosTest(unittest.TestCase):
    def test_domicilio_con_209_sur(self):
        self.assertEqual(
            datos.DOMICILIO_COMPLETO,
            "Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamps.",
        )
        self.assertEqual(datos.DOMICILIO_CORTO, "Obregón 209 Sur, Cd. Madero")
        self.assertEqual(datos.REFERENCIA, "Frente a Walmart, entrando por Banamex")

    def test_contacto(self):
        self.assertEqual(datos.TELEFONO_WA, "528333268008")
        self.assertEqual(datos.TELEFONO_TEL, "+528333268008")
        self.assertEqual(datos.TELEFONO_VISIBLE, "833 326 8008")
        self.assertEqual(datos.CORREO_FORMULARIOS, "viverosterra@hotmail.com")
        self.assertEqual(datos.GA4_ID, "G-RMZCVJ734M")

    def test_promesa_unica(self):
        self.assertEqual(
            datos.PROMESA_COMPLETA,
            "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h",
        )

    def test_cifras_de_empresa(self):
        self.assertEqual(datos.DESDE, 2007)
        self.assertEqual(datos.FUNDACION, "2007-12-12")
        self.assertEqual(datos.REPSE, "773725")
        self.assertEqual(datos.M2_INSTALADOS, "+500,000 m²")
        self.assertEqual(datos.CLIENTES, "+900")
        self.assertEqual(datos.INSTALACIONES, "+1,500")
        self.assertEqual(datos.VARIEDADES, "+200")
        self.assertEqual(datos.GOOGLE, "4.6 en Google (24 reseñas)")
        self.assertEqual(datos.SINTETICO_NACIONAL_DESDE, 2012)

    def test_precios_oficiales(self):
        p = datos.PRECIOS
        self.assertEqual((p["pasto_solo_m2"], p["pasto_instalado_m2"], p["pasto_mayoreo_m2"]), (85, 120, 60))
        self.assertEqual(p["pasto_mayoreo_minimo_m2"], 500)
        self.assertEqual(p["mantenimiento_mes"], 750)
        self.assertEqual(p["diseno"], 3000)
        self.assertEqual(p["riego_m2"], (180, 320))
        self.assertEqual(p["sintetico_instalado_m2"], (385, 650))
        self.assertEqual(p["sintetico_tienda_m2"], 139)

    def test_decisiones_del_dueno_2026_11_07(self):
        self.assertEqual(datos.PRECIOS["poda"], 500)
        self.assertTrue(datos.PODA.startswith("Desde $500, según cotización"))
        self.assertEqual(datos.PRECIOS["framboyan"], 250)
        self.assertEqual(len(datos.CLIENTES_B2B), 6)
        self.assertEqual(datos.AUTOR_BLOG, "Equipo técnico de Viveros Terra")
        self.assertIsNone(datos.PROXIMO_CORTE)

    def test_textos_de_garantia_y_riego(self):
        self.assertIn("15 a 20 días", datos.GARANTIA_PASTO)
        self.assertIn("sembramos nosotros", datos.GARANTIA_PLANTAS)
        self.assertEqual(datos.PRIMER_RIEGO, "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días.")

    def test_mensajes_terminan_con_la_firma(self):
        for servicio in datos.MENSAJES:
            with self.subTest(servicio=servicio):
                self.assertTrue(datos.mensaje(servicio).endswith("\n\nVengo de viverosterra.com"))

    def test_wa_url_codifica_todo(self):
        url = datos.wa_url("Hola, ñ\nColonia: ___")
        self.assertTrue(url.startswith("https://wa.me/528333268008?text="))
        self.assertNotIn(" ", url)
        self.assertEqual(unquote(url.split("text=", 1)[1]), "Hola, ñ\nColonia: ___")

    def test_redes_con_https_y_sin_subdominio_de_pais(self):
        for nombre, url in datos.REDES:
            with self.subTest(red=nombre):
                self.assertTrue(url.startswith("https://www."))
                self.assertNotIn("il.linkedin", url)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'datos'` y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar `tools/site/datos.py`**

```python
"""Fuente única de datos del sitio de Viveros Terra.

Todo dato que se repite en más de una página sale de aquí: contacto, domicilio, horario, promesa de respuesta,
cifras de la empresa, precios oficiales, garantías, decisiones del dueño, perfiles oficiales y mensajes de WhatsApp.
Lo consumen los parciales del shell (tools/site/partials.py) y las pruebas; desde la Etapa 4, también el JSON-LD y
llms.txt. Decisiones del dueño: docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md.
"""
from urllib.parse import quote

SITIO = "https://www.viverosterra.com"
NOMBRE = "Viveros Terra"
GA4_ID = "G-RMZCVJ734M"
ANIO = 2026

TELEFONO_WA = "528333268008"
TELEFONO_TEL = "+528333268008"
TELEFONO_VISIBLE = "833 326 8008"
CORREO_FORMULARIOS = "viverosterra@hotmail.com"

CALLE = "Av. Álvaro Obregón 209 Sur"
COLONIA = "Col. Ampliación Unidad Nacional"
CP = "89510"
CIUDAD = "Ciudad Madero"
ESTADO = "Tamps."
REFERENCIA = "Frente a Walmart, entrando por Banamex"
DOMICILIO_COMPLETO = f"{CALLE}, {COLONIA}, {CP} {CIUDAD}, {ESTADO}"
DOMICILIO_CORTO = "Obregón 209 Sur, Cd. Madero"
GEO = (22.2777575, -97.8433341)
MAPS_URL = "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"

HORARIO = "Lun a vie 9 a 18 h, sáb 9 a 14 h"
PROMESA = "Respondemos en menos de 1 hora en horario"
PROMESA_COMPLETA = f"{PROMESA} · {HORARIO}"

DESDE = 2007
FUNDACION = "2007-12-12"
SINTETICO_NACIONAL_DESDE = 2012
VARIEDADES = "+200"
CLIENTES = "+900"
INSTALACIONES = "+1,500"
M2_INSTALADOS = "+500,000 m²"
REPSE = "773725"
FACTURA = "CFDI 4.0"
GOOGLE = "4.6 en Google (24 reseñas)"

PRECIOS = {
    "pasto_solo_m2": 85,
    "pasto_instalado_m2": 120,
    "pasto_mayoreo_m2": 60,
    "pasto_mayoreo_minimo_m2": 500,
    "mantenimiento_mes": 750,
    "diseno": 3000,
    "riego_m2": (180, 320),
    "sintetico_instalado_m2": (385, 650),
    "sintetico_tienda_m2": 139,
    "poda": 500,
    "framboyan": 250,
}
PODA = ("Desde $500, según cotización: el precio depende del tamaño del árbol o la palma y de los residuos que se "
        "generan. Mándanos fotos y ubicación por WhatsApp.")
GARANTIA_PASTO = ("Si una sección no arraiga en 15 a 20 días, la reponemos sin costo, siguiendo el protocolo de riego "
                  "(ver condiciones).")
GARANTIA_PLANTAS = "30 días en las plantas que sembramos nosotros, con el riego indicado (ver condiciones)."
PRIMER_RIEGO = "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días."

# Permiso del dueño (2026-11-07) para mostrarlos con nombre y logo.
CLIENTES_B2B = ("BMW", "Taghleef Industries", "Gobierno de Tampico", "Grupo Velas", "Velamar", "Flex")
# Autor del blog: la organización (Organization ligada a #negocio). Nunca una persona inventada.
AUTOR_BLOG = "Equipo técnico de Viveros Terra"
# Decisión del dueño (2026-11-07): nunca se muestra fecha de corte ni disponibilidad semanal.
PROXIMO_CORTE = None

REDES = (
    ("Facebook", "https://www.facebook.com/viverosterra/"),
    ("Instagram", "https://www.instagram.com/viverosterramx"),
    ("TikTok", "https://www.tiktok.com/@viverosterra"),
    ("YouTube", "https://www.youtube.com/@viverosterramx"),
    ("LinkedIn", "https://www.linkedin.com/company/viveros-terra-tampico"),
)

FIRMA = "Vengo de viverosterra.com"
MENSAJES = {
    "general": "Hola, quiero cotizar: ___\nColonia: ___\nMetros aprox.: ___",
    "pasto-natural": "Hola, quiero cotizar pasto San Agustín en rollo.\nColonia: ___\nMetros aprox.: ___\nSolo el pasto o instalado: ___",
    "pasto-sintetico": "Hola, quiero cotizar pasto sintético.\nCiudad o colonia: ___\nMetros aprox.: ___",
    "jardin": "Hola, quiero cotizar diseño, mantenimiento o riego.\nColonia: ___\nMetros aprox. del jardín: ___",
    "plantas": "Hola, quiero cotizar plantas o palmas.\nLo que busco: ___\nColonia de entrega: ___",
    "materiales": "Hola, quiero cotizar material para jardín.\nMaterial y cantidad: ___\nColonia de entrega: ___",
    "empresas": "Hola, quiero cotizar un proyecto.\nEmpresa: ___\nObra y ubicación: ___\nm² o especies: ___\nFecha: ___",
}


def mensaje(servicio):
    """Texto de WhatsApp del servicio, siempre con la firma al final para atribuir el chat."""
    return f"{MENSAJES[servicio]}\n\n{FIRMA}"


def wa_url(texto):
    """Enlace wa.me con el texto codificado por completo (espacios como %20, saltos como %0A)."""
    return f"https://wa.me/{TELEFONO_WA}?text={quote(texto, safe='')}"
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 10 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/datos.py tools/site/tests/test_datos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): fuente única de datos del sitio" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Contexto por ruta (`tools/site/paginas.py`)

**Files:**
- Create: `tools/site/paginas.py`
- Test: `tools/site/tests/test_paginas.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_paginas.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402


class RutaTest(unittest.TestCase):
    def test_ruta_de_archivos(self):
        base = Path(tempfile.mkdtemp())
        casos = {
            "index.html": "/",
            "catalogo.html": "/catalogo",
            "blog/index.html": "/blog",
            "blog/palma-areca-tampico/index.html": "/blog/palma-areca-tampico",
            "protocolo-cuidados-pasto-san-agustin.html": "/protocolo-cuidados-pasto-san-agustin",
            "pasto-sintetico/envio/cdmx/index.html": "/pasto-sintetico/envio/cdmx",
        }
        for rel, ruta in casos.items():
            with self.subTest(rel=rel):
                self.assertEqual(paginas.ruta_de(base / rel, public=base), ruta)

    def test_ruta_de_rechaza_lo_que_no_es_html(self):
        base = Path(tempfile.mkdtemp())
        with self.assertRaises(ValueError):
            paginas.ruta_de(base / "robots.txt", public=base)


class ContextoTest(unittest.TestCase):
    def test_servicio_de_pasto(self):
        ctx = paginas.contexto("/pasto-en-rollo-tampico")
        self.assertEqual((ctx["tipo"], ctx["activo"], ctx["servicio"]), ("servicio-pasto", "pasto-natural", "pasto-natural"))
        self.assertTrue(ctx["barra"])
        self.assertEqual(ctx["mensaje"], datos.mensaje("pasto-natural"))

    def test_prefijos(self):
        self.assertEqual(paginas.contexto("/pasto-sintetico/envio/cdmx")["tipo"], "ciudad")
        self.assertEqual(paginas.contexto("/pasto-sintetico/toscana-28")["tipo"], "tienda")
        self.assertEqual(paginas.contexto("/blog/palma-areca-tampico")["tipo"], "blog")
        self.assertEqual(paginas.contexto("/jardineria-altamira")["servicio"], "jardin")

    def test_sin_barra_en_tienda_catalogo_y_formularios(self):
        for ruta in ("/pasto-sintetico", "/pasto-sintetico/perros", "/pasto-sintetico/envio/cdmx", "/catalogo",
                     "/cuestionario", "/gracias", "/datos-envio"):
            with self.subTest(ruta=ruta):
                self.assertFalse(paginas.contexto(ruta)["barra"])

    def test_ruta_desconocida_falla(self):
        with self.assertRaises(KeyError):
            paginas.contexto("/no-existe")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'paginas'` y `FAILED`.

- [ ] **Step 3: Implementar `tools/site/paginas.py`**

```python
"""Contexto de cada página para el shell: tipo (prefijo de data-cta), sección activa del menú, servicio y barra móvil.

Toda página de public/ debe tener contexto. Si agregas una página, agrégala aquí: el build falla con rutas sin contexto.
"""
from pathlib import Path

import datos

PUBLIC = Path(__file__).resolve().parents[2] / "public"
SIN_BARRA = {"tienda", "ciudad", "catalogo"}
RUTAS_SIN_BARRA = {"/cuestionario", "/gracias", "/datos-envio"}

_PLANTAS = ("plantas", "plantas", "plantas")
_MATERIAL = ("material", "plantas", "materiales")
_UTILIDAD = ("utilidad", None, "general")

EXACTAS = {
    "/": ("home", None, "general"),
    "/pasto-en-rollo-tampico": ("servicio-pasto", "pasto-natural", "pasto-natural"),
    "/mayoreo-pasto-tampico": ("b2b", "pasto-natural", "empresas"),
    "/protocolo-cuidados-pasto-san-agustin": ("posventa", "pasto-natural", "pasto-natural"),
    "/pasto-sintetico-tampico": ("servicio-sintetico", "pasto-sintetico", "pasto-sintetico"),
    "/pasto-sintetico": ("tienda", "pasto-sintetico", "pasto-sintetico"),
    "/diseno-jardines-tampico": ("servicio-diseno", "jardin", "jardin"),
    "/mantenimiento-jardines-tampico": ("servicio-mantenimiento", "jardin", "jardin"),
    "/sistema-riego-tampico": ("servicio-riego", "jardin", "jardin"),
    "/cuestionario": ("utilidad", "jardin", "jardin"),
    "/plantas-palmas-arboles-tampico": _PLANTAS,
    "/palmas-tropicales-tampico": _PLANTAS,
    "/plantas-para-jardin-tampico": _PLANTAS,
    "/arboles-ornamentales-tampico": _PLANTAS,
    "/arboles-para-banqueta-tampico": _PLANTAS,
    "/plantas-de-interior-tampico": _PLANTAS,
    "/catalogo": ("catalogo", "plantas", "plantas"),
    "/tierra-negra-vegetal-tampico": _MATERIAL,
    "/tezontle-rojo-tampico": _MATERIAL,
    "/marmol-blanco-tampico": _MATERIAL,
    "/piedra-bola-rio-tampico": _MATERIAL,
    "/palmas-mayoreo-proyectos": ("b2b", "empresas", "empresas"),
    "/vivero-tampico": ("vivero", None, "general"),
    "/precios": ("precios", "precios", "general"),
    "/blog": ("blog", None, "general"),
    "/politicas": _UTILIDAD,
    "/politica-privacidad": _UTILIDAD,
    "/gracias": _UTILIDAD,
    "/datos-envio": _UTILIDAD,
}
PREFIJOS = (
    ("/pasto-sintetico/envio/", ("ciudad", "pasto-sintetico", "pasto-sintetico")),
    ("/pasto-sintetico/", ("tienda", "pasto-sintetico", "pasto-sintetico")),
    ("/blog/", ("blog", None, "general")),
    ("/jardineria-", ("zona", None, "jardin")),
)


def ruta_de(path, public=PUBLIC):
    """Ruta pública ("/blog/x") del archivo HTML dentro de public/."""
    rel = Path(path).resolve().relative_to(Path(public).resolve()).as_posix()
    if rel == "index.html":
        return "/"
    for sufijo in ("/index.html", ".html"):
        if rel.endswith(sufijo):
            return "/" + rel[: -len(sufijo)]
    raise ValueError(f"No es una página HTML: {rel}")


def contexto(ruta):
    """Diccionario nuevo con ruta, tipo, activo, servicio, barra y mensaje de WhatsApp de la ruta."""
    valores = EXACTAS.get(ruta)
    if valores is None:
        valores = next((v for prefijo, v in PREFIJOS if ruta.startswith(prefijo)), None)
    if valores is None:
        raise KeyError(f"Ruta sin contexto en tools/site/paginas.py: {ruta}")
    tipo, activo, servicio = valores
    return {
        "ruta": ruta,
        "tipo": tipo,
        "activo": activo,
        "servicio": servicio,
        "barra": tipo not in SIN_BARRA and ruta not in RUTAS_SIN_BARRA,
        "mensaje": datos.mensaje(servicio),
    }
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 16 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/paginas.py tools/site/tests/test_paginas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): contexto del shell por ruta" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Fuentes autoalojadas (Archivo + Fraunces itálica)

**Files:**
- Create: `public/fonts/archivo-latin.woff2`, `public/fonts/fraunces-italic-latin.woff2`
- Test: `tools/site/tests/test_fuentes.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_fuentes.py`:

```python
import hashlib
import unittest
from pathlib import Path

FUENTES = Path(__file__).resolve().parents[3] / "public" / "fonts"
ESPERADAS = {
    "archivo-latin.woff2": "4c98b9d490d1698ec95f2ff17a6c7d0e72691864c0c5d7bc2a2c161b45afe5ad",
    "fraunces-italic-latin.woff2": "a7125f30fe100bbcf48b07996b6cae585afbdaea57fea1c014505793fa8d43a6",
}


class FuentesTest(unittest.TestCase):
    def test_fuentes_presentes_e_integras(self):
        for nombre, sha in ESPERADAS.items():
            with self.subTest(fuente=nombre):
                datos = (FUENTES / nombre).read_bytes()
                self.assertEqual(datos[:4], b"wOF2")
                self.assertEqual(hashlib.sha256(datos).hexdigest(), sha)

    def test_presupuesto_total(self):
        total = sum((FUENTES / n).stat().st_size for n in ESPERADAS)
        self.assertLess(total, 120 * 1024)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `FileNotFoundError` sobre `archivo-latin.woff2` y `FAILED (errors=2)`.

- [ ] **Step 3: Descargar los subsets latin de Google Fonts (Archivo variable wdth 75–100 y wght 400–800; Fraunces itálica 400)**

```bash
cd ~/dev/viverosterra-e1
mkdir -p public/fonts
curl -sSfL -o public/fonts/archivo-latin.woff2 https://fonts.gstatic.com/s/archivo/v25/k3kQo8UDI-1M0wlSfdnoLmvDIaI.woff2
curl -sSfL -o public/fonts/fraunces-italic-latin.woff2 "https://fonts.gstatic.com/s/fraunces/v38/6NVf8FyLNQOQZAnv9ZwNjucMHVn85Ni7emAe9lKqZTnbB-gzTK0K1ChJdt9vIVYX9G37lvd9sPEKsxx664UJf1hLTc7RrU9kMz3lR24.woff2"
shasum -a 256 public/fonts/*.woff2
```

Expected:
```
4c98b9d490d1698ec95f2ff17a6c7d0e72691864c0c5d7bc2a2c161b45afe5ad  public/fonts/archivo-latin.woff2
a7125f30fe100bbcf48b07996b6cae585afbdaea57fea1c014505793fa8d43a6  public/fonts/fraunces-italic-latin.woff2
```

Si Google cambió los archivos (otro sha), obtén las URLs vigentes con
`curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&family=Fraunces:ital,wght@1,400&display=swap"`, toma el `src` del bloque `/* latin */` de cada familia, descarga y actualiza los sha de `ESPERADAS`.

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 18 tests` y `OK`. (Archivo pesa 88 KB: el presupuesto final de ≤ 80 KB se cumple en la Etapa 5 con un subset propio.)

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/fonts/archivo-latin.woff2 public/fonts/fraunces-italic-latin.woff2 tools/site/tests/test_fuentes.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): fuentes Archivo y Fraunces autoalojadas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---
### Task 5: `terra.css` con tokens del híbrido y componentes del shell

**Files:**
- Create: `public/css/terra.css`
- Test: `tools/site/tests/test_terra_css.py`

Valores congelados desde `design/hibrido/styles.css` (spec §4.2): hueso `#FAF7EF`/`#F1ECDF`, tinta `#161A14`, verde campo `#1E4D2B` (hover `#12301B`), amarillo precio `#F2D24B`, café medida `#6B4226`, glifo WhatsApp `#25D366`, radios 2 px y 6 px, Archivo (titulares, texto y cifras `tabular-nums`) + Fraunces itálica (solo nombres científicos y Notas de campo). Sin mono: las cifras van en la sans tabular. En esta etapa solo entran los componentes que usa el shell (botón de WhatsApp, menú con paneles, menú móvil con acordeón, pie con cuadro de datos, barra fija móvil, foco); la etiqueta de precio, el Medidor, el proceso NOSOTROS / TÚ, la Nota de campo, la tabla de precios con Unidad y la figura `FIG.` entran a `terra.css` en la Etapa 2 con la plantilla que los usa por primera vez (referencia: `docs/diseno/hibrido/styles.css`), para no publicar CSS sin uso.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_terra_css.py`:

```python
import re
import unittest
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3] / "public"
TERRA = PUBLIC / "css" / "terra.css"
CSS_VIEJOS = ("design-system.css", "tailwind.css", "servicios.css", "tienda-pasto.css")


def sin_comentarios(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def clases(css):
    """Nombres de clase de una hoja (sin comentarios, sin url(...) y sin números como .8125rem)."""
    limpio = re.sub(r"url\([^)]*\)", "", sin_comentarios(css))
    return {m.replace("\\", "") for m in re.findall(r"\.(-?[_a-zA-Z](?:\\.|[\w-])*)", limpio)}


def tokens(css):
    bloque = re.search(r":root\{(.*?)\}", sin_comentarios(css), re.S).group(1)
    return dict(re.findall(r"(--vt-[\w-]+):\s*([^;]+);", bloque))


def luminancia(hexa):
    canales = [int(hexa.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lineal = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lineal[0] + 0.7152 * lineal[1] + 0.0722 * lineal[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


class TerraCssTest(unittest.TestCase):
    def setUp(self):
        self.css = TERRA.read_text(encoding="utf-8")

    def test_todo_selector_es_del_shell(self):
        css = re.sub(r"@font-face\{[^}]*\}", "", sin_comentarios(self.css))
        ajenos = []
        for selector in re.findall(r"([^{}]+)\{", css):
            selector = selector.strip()
            if selector.startswith("@media") or selector == ":root":
                continue
            ajenos += [p.strip() for p in selector.split(",") if ".vt-" not in p]
        self.assertEqual(ajenos, [])

    def test_sin_colores_literales_fuera_de_root(self):
        css = re.sub(r":root\{[^}]*\}", "", sin_comentarios(self.css))
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css), [])

    def test_tokens_del_hibrido(self):
        t = tokens(self.css)
        esperados = {"--vt-bone": "#FAF7EF", "--vt-bone-2": "#F1ECDF", "--vt-ink": "#161A14", "--vt-field": "#1E4D2B",
                     "--vt-field-deep": "#12301B", "--vt-tag": "#F2D24B", "--vt-soil": "#6B4226", "--vt-wa": "#25D366"}
        for nombre, valor in esperados.items():
            with self.subTest(token=nombre):
                self.assertEqual(t[nombre], valor)

    def test_contraste_aa_por_par_de_tokens(self):
        t = tokens(self.css)
        pares = [("--vt-ink", "--vt-bone"), ("--vt-ink-2", "--vt-bone"), ("--vt-muted", "--vt-bone"),
                 ("--vt-muted", "--vt-card"), ("--vt-field", "--vt-bone"), ("--vt-card", "--vt-field"),
                 ("--vt-on-dark", "--vt-ink"), ("--vt-on-dark-2", "--vt-ink"), ("--vt-tag", "--vt-ink"),
                 ("--vt-tag-ink", "--vt-tag"), ("--vt-field-deep", "--vt-field-100")]
        for texto, fondo in pares:
            with self.subTest(par=(texto, fondo)):
                self.assertGreaterEqual(contraste(t[texto], t[fondo]), 4.5)

    def test_presupuesto(self):
        self.assertLess(len(self.css.encode("utf-8")), 30 * 1024)

    def test_fuentes_referenciadas_existen(self):
        urls = re.findall(r'url\("(/fonts/[^"]+)"\)', self.css)
        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertTrue((PUBLIC / url.lstrip("/")).is_file(), url)

    def test_clases_del_shell_no_chocan_con_las_viejas(self):
        viejas = set()
        for nombre in CSS_VIEJOS:
            viejas |= clases((PUBLIC / "css" / nombre).read_text(encoding="utf-8"))
        for pagina in PUBLIC.rglob("*.html"):
            for estilo in re.findall(r"<style[^>]*>(.*?)</style>", pagina.read_text(encoding="utf-8"), re.S):
                viejas |= clases(estilo)
        self.assertEqual(sorted(clases(self.css) & viejas), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `FileNotFoundError` sobre `terra.css` y `FAILED (errors=7)`.

- [ ] **Step 3: Implementar `public/css/terra.css`**

```css
/* =========================================================
   Viveros Terra · terra.css · Etapa 1 (shell)
   Híbrido "Plano + Etiqueta": tokens y componentes del shell (menú, pie, barra móvil, botones).
   Convivencia con el CSS viejo: todo selector empieza con .vt- y nada toca elementos sueltos
   (body, h2, a...). Las reglas globales llegan en la Etapa 2, al retirar el CSS viejo.
   Ningún color literal fuera de :root.
   ========================================================= */
@font-face{font-family:"Archivo";font-style:normal;font-weight:400 800;font-stretch:75% 100%;font-display:swap;src:url("/fonts/archivo-latin.woff2") format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Fraunces";font-style:italic;font-weight:400;font-display:swap;src:url("/fonts/fraunces-italic-latin.woff2") format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}

:root{
  /* superficies */
  --vt-bone:#FAF7EF; --vt-bone-2:#F1ECDF; --vt-card:#FFFFFF;
  --vt-line:#DDD6C6; --vt-line-strong:#B8AE98;
  /* tinta */
  --vt-ink:#161A14; --vt-ink-2:#2F352B; --vt-muted:#5C6152;
  /* acción y marca */
  --vt-field:#1E4D2B; --vt-field-deep:#12301B; --vt-field-100:#E3EADB;
  --vt-on-dark:#FAF7EF; --vt-on-dark-2:#C9D6C4; --vt-on-dark-line:rgb(250 247 239 / .16);
  /* semánticos: amarillo = precio · café = medida · verde WhatsApp = solo el glifo */
  --vt-tag:#F2D24B; --vt-tag-ink:#161A14;
  --vt-soil:#6B4226;
  --vt-wa:#25D366;
  --vt-scrim:rgb(22 26 20 / .55);
  /* tipografía: 2 familias */
  --vt-font-sans:"Archivo",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  --vt-font-serif:"Fraunces",Georgia,"Times New Roman",serif;
  --vt-text-xs:.8125rem; --vt-text-sm:.9375rem; --vt-text-base:1.0625rem;
  --vt-text-lg:clamp(1.125rem,1.05rem + .35vw,1.3125rem); --vt-text-menu:1.5rem; --vt-text-dato:1.1875rem;
  --vt-wdth-tight:75; --vt-wdth-mid:85;
  /* forma y espacio */
  --vt-radius:2px; --vt-radius-tag:6px;
  --vt-gutter:16px; --vt-maxw:1320px; --vt-head-h:56px; --vt-bar-h:64px;
  --vt-z-head:900; --vt-z-bar:950; --vt-z-skip:1000;
  /* movimiento */
  --vt-ease-out:cubic-bezier(.16,1,.3,1); --vt-duration-fast:150ms; --vt-duration-normal:260ms;
}
@media (min-width:768px){:root{--vt-gutter:32px}}
@media (min-width:1100px){:root{--vt-head-h:68px}}

/* ---------- base del shell ---------- */
.vt-head,.vt-head *,.vt-foot,.vt-foot *,.vt-bar,.vt-bar *,.vt-skip{box-sizing:border-box}
.vt-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.vt-sprite{position:absolute;width:0;height:0;overflow:hidden}
.vt-skip{position:absolute;left:8px;top:-80px;z-index:var(--vt-z-skip);padding:12px 16px;background:var(--vt-ink);color:var(--vt-on-dark);font:600 var(--vt-text-sm)/1.2 var(--vt-font-sans);text-decoration:none}
.vt-skip:focus{top:8px}
.vt-wrap{max-width:var(--vt-maxw);margin-inline:auto;padding-inline:var(--vt-gutter)}
.vt-head :focus-visible,.vt-bar :focus-visible,.vt-skip:focus-visible{outline:2px solid var(--vt-field);outline-offset:2px}
.vt-foot :focus-visible{outline:2px solid var(--vt-tag);outline-offset:2px}

/* ---------- botones (dos textos de CTA: "Cotizar por WhatsApp" y "Llamar 833 326 8008") ---------- */
.vt-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 20px;border:1.5px solid transparent;border-radius:var(--vt-radius);font:600 1rem/1.1 var(--vt-font-sans);letter-spacing:0;text-transform:none;text-decoration:none;white-space:nowrap;cursor:pointer;transition:background-color var(--vt-duration-fast),color var(--vt-duration-fast),transform var(--vt-duration-fast)}
.vt-btn:active{transform:translateY(1px)}
.vt-btn--wa{background:var(--vt-field);color:var(--vt-card)}
.vt-btn--wa:hover{background:var(--vt-field-deep);color:var(--vt-card)}
.vt-wa-g{display:grid;place-items:center;flex:none;width:22px;height:22px;border-radius:50%;background:var(--vt-card)}
.vt-wa-g svg{display:block;width:16px;height:16px;fill:var(--vt-wa)}

/* ---------- menú principal ---------- */
.vt-head{position:sticky;top:0;z-index:var(--vt-z-head);background:var(--vt-bone);border-bottom:1px solid var(--vt-line);font-family:var(--vt-font-sans);font-size:var(--vt-text-base);color:var(--vt-ink);line-height:1.4;text-align:left}
.vt-head__bar{display:flex;align-items:center;gap:8px;max-width:var(--vt-maxw);height:var(--vt-head-h);margin-inline:auto;padding-inline:var(--vt-gutter)}
.vt-head__logo{display:block;flex:none}
.vt-head__logo img{display:block;width:112px;max-width:none;height:auto}
.vt-nav{display:none}
.vt-nav__list{display:flex;gap:22px;margin:0;padding:0;list-style:none}
.vt-nav__item{position:relative;display:flex;align-items:center;gap:2px;margin:0;padding:0}
.vt-nav__top{position:relative;display:inline-flex;align-items:center;gap:4px;margin:0;padding:12px 0;border:0;background:none;font:500 15px/1.2 var(--vt-font-sans);color:var(--vt-ink);text-decoration:none;cursor:pointer}
.vt-nav__top::after{content:"";position:absolute;left:0;right:0;bottom:6px;height:2px;background:var(--vt-field);transform:scaleX(0);transform-origin:left;transition:transform var(--vt-duration-normal) var(--vt-ease-out)}
.vt-nav__top:hover::after,.vt-nav__item.is-activo>.vt-nav__top::after,.vt-nav__top[aria-current="page"]::after{transform:scaleX(1)}
.vt-nav__exp{display:grid;place-items:center;width:24px;height:24px;margin:0;padding:0;border:0;background:none;color:var(--vt-muted);cursor:pointer}
.vt-chev{display:block;width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:transform var(--vt-duration-fast)}
.vt-nav [aria-expanded="true"]>.vt-chev{transform:rotate(180deg)}
.vt-nav__panel{display:none;position:absolute;top:100%;left:-16px;min-width:270px;margin:0;padding:8px 0;list-style:none;background:var(--vt-card);border:1px solid var(--vt-line-strong);border-radius:var(--vt-radius);box-shadow:0 18px 30px -20px var(--vt-scrim)}
.vt-nav__item:hover>.vt-nav__panel,.vt-nav__item:focus-within>.vt-nav__panel,.vt-nav__item>[aria-expanded="true"]~.vt-nav__panel{display:block}
.vt-nav__panel li{margin:0;padding:0}
.vt-nav__panel a{display:block;padding:10px 16px;font:400 var(--vt-text-sm)/1.3 var(--vt-font-sans);color:var(--vt-ink);text-decoration:none}
.vt-nav__panel a:hover,.vt-nav__panel a[aria-current="page"]{background:var(--vt-field-100);color:var(--vt-field-deep)}
.vt-head__meta{display:none;margin:0;font-size:var(--vt-text-xs);line-height:1.25;color:var(--vt-muted);text-align:right}
.vt-head__meta b{display:block;font-weight:600;color:var(--vt-ink)}
.vt-head__cta{margin-left:auto;min-height:44px;padding:0 12px;font-size:15px}
.vt-head__cta-corto{display:none}
@media (max-width:420px){.vt-head__cta-largo{display:none}.vt-head__cta-corto{display:inline}}
@media (max-width:359px){.vt-head__logo img{width:100px}.vt-head__cta{padding:0 10px}}
.vt-burger{display:grid;place-items:center;flex:none;width:44px;height:44px;margin:0;padding:0;border:1px solid var(--vt-line-strong);border-radius:var(--vt-radius);background:none;color:var(--vt-ink);cursor:pointer}
.vt-burger svg{display:block;width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round}
@media (min-width:1100px){
  .vt-head__bar{gap:16px}
  .vt-head__logo img{width:150px}
  .vt-nav{display:block;margin-left:auto}
  .vt-head__cta{margin-left:0;padding:0 14px}
  .vt-burger{display:none}
}
@media (min-width:1360px){.vt-head__meta{display:block}}

/* ---------- menú móvil (acordeón nativo con <details>) ---------- */
.vt-mmenu{max-height:calc(100vh - var(--vt-head-h));overflow-y:auto;padding:4px var(--vt-gutter) 20px;border-top:1px solid var(--vt-line);background:var(--vt-bone)}
.vt-mmenu[hidden]{display:none}
@media (min-width:1100px){.vt-mmenu{display:none}}
.vt-acc{margin:0;border-bottom:1px solid var(--vt-line)}
.vt-acc summary,.vt-mmenu__link{display:flex;justify-content:space-between;align-items:baseline;gap:12px;min-height:52px;padding:12px 0;font:800 var(--vt-text-menu)/1.1 var(--vt-font-sans);font-variation-settings:"wdth" var(--vt-wdth-tight);color:var(--vt-ink);text-decoration:none;list-style:none;cursor:pointer}
.vt-acc summary::-webkit-details-marker{display:none}
.vt-acc small,.vt-mmenu__link small{font:600 var(--vt-text-xs)/1.2 var(--vt-font-sans);font-variation-settings:normal;color:var(--vt-muted)}
.vt-acc ul{margin:0 0 12px;padding:0;list-style:none}
.vt-acc li{margin:0;padding:0}
.vt-acc li a{display:block;padding:10px 0 10px 12px;font:400 var(--vt-text-base)/1.3 var(--vt-font-sans);color:var(--vt-ink-2);text-decoration:none}
.vt-acc li a[aria-current="page"]{color:var(--vt-field);font-weight:600}
.vt-mmenu__link{border-bottom:1px solid var(--vt-line)}
.vt-mmenu__meta{margin:14px 0 0;font-size:var(--vt-text-sm);color:var(--vt-muted)}
.vt-mmenu__meta a{color:var(--vt-field)}

/* ---------- pie único ---------- */
.vt-foot{margin:0;padding:48px 0 calc(32px + var(--vt-bar-h));background:var(--vt-ink);color:var(--vt-on-dark-2);font:400 var(--vt-text-sm)/1.55 var(--vt-font-sans);text-align:left;border:0}
@media (min-width:1024px){.vt-foot{padding-bottom:32px}}
.vt-foot p{margin:0 0 12px}
.vt-foot ul{margin:0;padding:0;list-style:none}
.vt-foot li{margin:0;padding:0}
.vt-foot a{display:inline-block;padding:9px 0;color:var(--vt-on-dark);text-decoration:none}
.vt-foot a:hover{color:var(--vt-on-dark);text-decoration:underline}
.vt-foot__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.vt-foot__about{grid-column:1 / -1}
.vt-foot__about img{display:block;width:150px;height:auto;margin-bottom:12px;filter:brightness(0) invert(1)}
.vt-foot__google{font-weight:600;color:var(--vt-on-dark)}
.vt-foot__h{margin:0 0 6px;padding:0;border:0;background:none;font:700 var(--vt-text-xs)/1.3 var(--vt-font-sans);letter-spacing:.1em;text-transform:uppercase;color:var(--vt-tag);text-align:left}
.vt-foot__promesa{margin-top:8px;color:var(--vt-on-dark-2)}
@media (min-width:700px){.vt-foot__grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1100px){.vt-foot__grid{grid-template-columns:1.6fr repeat(5,minmax(0,1fr))}.vt-foot__about{grid-column:auto}}
.vt-foot__datos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));margin:32px 0 0;border:1px solid var(--vt-on-dark-line)}
.vt-foot__datos>div{min-width:0;padding:12px 14px;border-right:1px solid var(--vt-on-dark-line);border-bottom:1px solid var(--vt-on-dark-line)}
.vt-foot__datos>div:nth-child(2n){border-right:0}
.vt-foot__datos dt{font:600 var(--vt-text-xs)/1.2 var(--vt-font-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--vt-on-dark-2)}
.vt-foot__datos dd{margin:4px 0 0;font:800 var(--vt-text-dato)/1.1 var(--vt-font-sans);font-variation-settings:"wdth" var(--vt-wdth-mid);font-variant-numeric:tabular-nums;color:var(--vt-on-dark);overflow-wrap:anywhere}
.vt-foot__datos dd small{display:block;margin-top:3px;font:400 var(--vt-text-xs)/1.3 var(--vt-font-sans);font-variation-settings:normal;color:var(--vt-on-dark-2)}
@media (min-width:900px){
  .vt-foot__datos{grid-template-columns:repeat(6,minmax(0,1fr))}
  .vt-foot__datos>div{border-bottom:0}
  .vt-foot__datos>div:nth-child(2n){border-right:1px solid var(--vt-on-dark-line)}
  .vt-foot__datos>div:last-child{border-right:0}
}
.vt-foot__legal{display:flex;flex-wrap:wrap;gap:6px 24px;justify-content:space-between;align-items:baseline;margin:20px 0 0;font-size:var(--vt-text-xs)}
.vt-foot__legal p{margin:0}
.vt-foot__redes{display:flex;flex-wrap:wrap;gap:0 16px}

/* ---------- barra fija móvil: [Cotizar por WhatsApp | teléfono] ---------- */
.vt-bar{position:fixed;left:0;right:0;bottom:0;z-index:var(--vt-z-bar);display:flex;gap:8px;align-items:stretch;padding:8px var(--vt-gutter) calc(8px + env(safe-area-inset-bottom));background:var(--vt-card);border-top:3px solid var(--vt-tag);box-shadow:0 -10px 24px -18px var(--vt-scrim);font-family:var(--vt-font-sans);transition:transform var(--vt-duration-normal) var(--vt-ease-out)}
.vt-bar.is-oculta{transform:translateY(110%)}
.vt-bar__go{flex:1;min-height:48px;padding:0 12px;font-size:15px}
.vt-bar__tel{display:grid;place-items:center;flex:none;width:52px;min-height:48px;border:1.5px solid var(--vt-ink);border-radius:var(--vt-radius);color:var(--vt-ink)}
.vt-bar__tel svg{display:block;width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
@media (min-width:1024px){.vt-bar{display:none}}

@media (prefers-reduced-motion:reduce){
  .vt-bar,.vt-nav__top::after,.vt-chev,.vt-btn{transition:none}
}
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 25 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/css/terra.css tools/site/tests/test_terra_css.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): terra.css con tokens del híbrido y componentes del shell" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: `legacy-fixes.css` (las 49 utilidades de Tailwind que faltan)

**Files:**
- Create: `public/css/legacy-fixes.css`
- Test: `tools/site/tests/test_legacy_fixes.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_legacy_fixes.py`:

```python
import re
import unittest
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3] / "public"
HOJAS = ("tailwind.css", "design-system.css", "servicios.css", "legacy-fixes.css")
UTILIDAD = re.compile(
    r"^(?:(?:sm|md|lg|xl|hover|focus|group-hover):)*-?(?:p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|w|h|min-h|max-w|text|bg|"
    r"border|rounded|gap|space|grid|col|row|flex|items|justify|font|leading|tracking|opacity|shadow|z|top|left|right|"
    r"bottom|inset|object|overflow|order|self|place|aspect|ring|translate|scale|duration|transition|from|to|via|divide|"
    r"line|whitespace|truncate|underline|uppercase|italic|block|inline|hidden|absolute|relative|fixed|sticky|shrink|"
    r"grow|basis)(?:-|$)"
)


def clases(css):
    return {m.replace("\\", "") for m in re.findall(r"\.((?:\\.|[\w-])+)", css)}


class LegacyFixesTest(unittest.TestCase):
    def test_ninguna_utilidad_usada_queda_sin_definir(self):
        definidas = set()
        for hoja in HOJAS:
            definidas |= clases((PUBLIC / "css" / hoja).read_text(encoding="utf-8"))
        faltan = {}
        for pagina in PUBLIC.rglob("*.html"):
            html = pagina.read_text(encoding="utf-8")
            if "/css/tailwind.css" not in html:
                continue
            locales = set()
            for estilo in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S):
                locales |= clases(estilo)
            for atributo in re.findall(r'class="([^"]*)"', html):
                for clase in atributo.split():
                    if "{" in clase or clase in definidas or clase in locales or not UTILIDAD.match(clase):
                        continue
                    faltan.setdefault(clase, str(pagina.relative_to(PUBLIC)))
        self.assertEqual(faltan, {})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `FileNotFoundError` sobre `legacy-fixes.css` y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar `public/css/legacy-fixes.css`**

```css
/* legacy-fixes.css · Etapa 1
   Utilidades de Tailwind que usan las páginas viejas y no están en tailwind.css (se compiló con HTML viejo y no hay
   package.json para regenerarlo). Valores de Tailwind 3 y colores de tailwind.config.js (primary #1B5E20,
   accent #66BB6A, wa #25D366). "text-slate" era un error de tipeo en mármol: se fija al slate-600 de Tailwind.
   Se borra junto con tailwind.css al cerrar la Etapa 2. */
.pt-0{padding-top:0}
.pt-4{padding-top:1rem}
.pb-1{padding-bottom:.25rem}
.pb-3{padding-bottom:.75rem}
.pb-6{padding-bottom:1.5rem}
.pl-3{padding-left:.75rem}
.border-0{border-width:0}
.border-t-2{border-top-width:2px}
.border-l-2{border-left-width:2px}
.border-l-4{border-left-width:4px}
.border-accent\/20{border-color:rgb(102 187 106 / .2)}
.divide-gray-100>:not([hidden])~:not([hidden]){border-color:#f3f4f6}
.bg-transparent{background-color:transparent}
.bg-white\/5{background-color:rgb(255 255 255 / .05)}
.bg-white\/8{background-color:rgb(255 255 255 / .08)}
.bg-accent\/15{background-color:rgb(102 187 106 / .15)}
.bg-gray-400{background-color:#9ca3af}
.text-slate{color:#475569}
.text-green-500{color:#22c55e}
.text-white\/90{color:rgb(255 255 255 / .9)}
.opacity-85{opacity:.85}
.w-20{width:5rem}
.h-20{height:5rem}
.aspect-\[4\/3\]{aspect-ratio:4/3}
.left-0{left:0}
.top-8{top:2rem}
.self-start{align-self:flex-start}
.grid-cols-1{grid-template-columns:repeat(1,minmax(0,1fr))}
.hover\:text-slate:hover{color:#475569}
.hover\:bg-green-800:hover{background-color:#166534}
.hover\:bg-accent:hover{background-color:#66BB6A}
.hover\:bg-wa:hover{background-color:#25D366}
.focus\:ring-accent:focus{--tw-ring-color:rgb(102 187 106 / 1)}
.group:hover .group-hover\:bg-primary\/10{background-color:rgb(27 94 32 / .1)}
@media (min-width:640px){
  .sm\:p-5{padding:1.25rem}
  .sm\:p-6{padding:1.5rem}
  .sm\:p-8{padding:2rem}
  .sm\:py-16{padding-top:4rem;padding-bottom:4rem}
  .sm\:gap-4{gap:1rem}
  .sm\:items-center{align-items:center}
  .sm\:w-24{width:6rem}
  .sm\:h-24{height:6rem}
  .sm\:h-80{height:20rem}
  .sm\:text-sm{font-size:.875rem;line-height:1.25rem}
  .sm\:text-base{font-size:1rem;line-height:1.5rem}
  .sm\:text-2xl{font-size:1.5rem;line-height:2rem}
}
@media (min-width:768px){
  .md\:text-5xl{font-size:3rem;line-height:1}
  .md\:col-start-2{grid-column-start:2}
}
@media (min-width:1024px){
  .lg\:hidden{display:none}
}
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 26 tests` y `OK`. Si aparece alguna clase en `faltan` que no está en esta lista (el HTML cambió desde que se escribió el plan), agrégala con su valor de Tailwind 3 y vuelve a correr.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/css/legacy-fixes.css tools/site/tests/test_legacy_fixes.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(css): utilidades de Tailwind que faltaban en las páginas viejas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: `terra.js` (menú, barra móvil y medición GA4)

**Files:**
- Create: `public/js/terra.js`
- Test: `public/js/tests/terra.test.js`, `tools/site/tests/test_paridad_terra_js.py`

- [ ] **Step 1: Escribir las pruebas que fallan**

`public/js/tests/terra.test.js`:

```js
// public/js/tests/terra.test.js
const test = require('node:test');
const assert = require('node:assert');
const { FIRMA, tipoEnlace, conFirma, evento } = require('../terra.js');

function enlace(atributos) {
  return { getAttribute: (nombre) => (nombre in atributos ? atributos[nombre] : null) };
}

test('reconoce WhatsApp y teléfono', () => {
  assert.strictEqual(tipoEnlace('https://wa.me/528333268008?text=Hola'), 'wa');
  assert.strictEqual(tipoEnlace('https://api.whatsapp.com/send?phone=528333268008'), 'wa');
  assert.strictEqual(tipoEnlace('tel:+528333268008'), 'tel');
  assert.strictEqual(tipoEnlace('/precios'), null);
  assert.strictEqual(tipoEnlace(null), null);
});

test('agrega la firma una sola vez, con %20 y sin +', () => {
  const firmado = conFirma('https://wa.me/528333268008?text=Hola%2C%20quiero%20pasto');
  assert.strictEqual(firmado, 'https://wa.me/528333268008?text=' + encodeURIComponent('Hola, quiero pasto\n\n' + FIRMA));
  assert.strictEqual(conFirma(firmado), firmado);
  assert.ok(!firmado.includes('+'));
});

test('sin texto previo deja solo la firma', () => {
  assert.strictEqual(conFirma('https://wa.me/528333268008'), 'https://wa.me/528333268008?text=' + encodeURIComponent(FIRMA));
});

test('un texto mal codificado se deja igual', () => {
  assert.strictEqual(conFirma('https://wa.me/528333268008?text=%E0%A4%A'), 'https://wa.me/528333268008?text=%E0%A4%A');
});

test('generate_lead lleva cta y servicio; click_to_call lleva cta', () => {
  const ctx = { tipo: 'blog', servicio: 'general' };
  assert.deepStrictEqual(evento(enlace({ href: 'https://wa.me/528333268008?text=a', 'data-cta': 'blog:header' }), ctx), {
    nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: 'blog:header', service: 'general' },
  });
  assert.deepStrictEqual(evento(enlace({ href: 'tel:+528333268008' }), ctx), {
    nombre: 'click_to_call', params: { cta_id: 'blog:sin-etiqueta' },
  });
  assert.strictEqual(evento(enlace({ href: '/precios' }), ctx), null);
});
```

`tools/site/tests/test_paridad_terra_js.py`:

```python
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "terra.js"


class ParidadTerraJsTest(unittest.TestCase):
    def test_firma_igual_en_js_y_python(self):
        firma = re.search(r"const FIRMA = '([^']+)';", JS.read_text(encoding="utf-8")).group(1)
        self.assertEqual(firma, datos.FIRMA)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr las pruebas (deben fallar)**

Run: `cd ~/dev/viverosterra-e1 && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"; cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1`
Expected: `ℹ pass 6` y `ℹ fail 1` (el archivo `terra.test.js` no carga: `Cannot find module '../terra.js'`); y `FAILED (errors=1)`.

- [ ] **Step 3: Implementar `public/js/terra.js`**

```js
/* Viveros Terra · terra.js · shell compartido (Etapa 1).
   - Mide por delegación cada clic en WhatsApp (generate_lead) y teléfono (click_to_call) con data-cta.
   - Firma los mensajes de WhatsApp con "Vengo de viverosterra.com" para atribuir el chat.
   - Abre y cierra el menú (paneles de escritorio y menú móvil) y oculta la barra móvil mientras el CTA del hero se ve.
   Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const FIRMA = 'Vengo de viverosterra.com';
  // La tienda ya manda sus propios generate_lead (tienda-pasto.js): aquí solo se firman.
  const OMITIR_EVENTO = '[data-cta-wa], #cot-send';

  function tipoEnlace(href) {
    if (!href) return null;
    if (/^tel:/i.test(href)) return 'tel';
    if (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(href)) return 'wa';
    return null;
  }

  function conFirma(href) {
    const partes = href.match(/^([^?#]*)(?:\?([^#]*))?(#.*)?$/);
    const base = partes[1];
    const consulta = partes[2] ? partes[2].split('&') : [];
    const ancla = partes[3] || '';
    const i = consulta.findIndex((p) => p.split('=')[0] === 'text');
    let actual = '';
    if (i >= 0) {
      try {
        actual = decodeURIComponent(consulta[i].slice(5).replace(/\+/g, ' '));
      } catch (error) {
        // Texto mal codificado: no se toca el enlace para no romper el mensaje que armó la página.
        return href;
      }
    }
    if (/viverosterra\.com/i.test(actual)) return href;
    const nuevo = 'text=' + encodeURIComponent(actual ? actual + '\n\n' + FIRMA : FIRMA);
    if (i >= 0) consulta[i] = nuevo;
    else consulta.push(nuevo);
    return base + '?' + consulta.join('&') + ancla;
  }

  function evento(a, contexto) {
    const tipo = tipoEnlace(a.getAttribute('href'));
    if (!tipo) return null;
    const cta = a.getAttribute('data-cta') || contexto.tipo + ':sin-etiqueta';
    if (tipo === 'tel') return { nombre: 'click_to_call', params: { cta_id: cta } };
    return { nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: cta, service: contexto.servicio } };
  }

  function contextoPagina(doc) {
    const head = doc.querySelector('.vt-head');
    return {
      tipo: (head && head.getAttribute('data-vt-tipo')) || 'desconocido',
      servicio: (head && head.getAttribute('data-vt-servicio')) || 'general',
    };
  }

  function medir(doc, win) {
    doc.addEventListener('click', (e) => {
      const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      const href = a.getAttribute('href');
      if (tipoEnlace(href) === 'wa') a.setAttribute('href', conFirma(href));
      if (a.matches(OMITIR_EVENTO)) return;
      const ev = evento(a, contextoPagina(doc));
      if (ev && typeof win.gtag === 'function') win.gtag('event', ev.nombre, ev.params);
    }, true);
  }

  function menu(doc) {
    const burger = doc.querySelector('.vt-burger');
    const movil = doc.getElementById('vt-mmenu');
    if (burger && movil) {
      burger.addEventListener('click', () => {
        const abierto = burger.getAttribute('aria-expanded') === 'true';
        burger.setAttribute('aria-expanded', String(!abierto));
        movil.hidden = abierto;
      });
    }
    const botones = Array.from(doc.querySelectorAll('.vt-nav [aria-controls]'));
    const cerrar = (excepto) => botones.forEach((b) => { if (b !== excepto) b.setAttribute('aria-expanded', 'false'); });
    botones.forEach((b) => b.addEventListener('click', (e) => {
      e.stopPropagation();
      const abierto = b.getAttribute('aria-expanded') === 'true';
      cerrar(b);
      b.setAttribute('aria-expanded', String(!abierto));
    }));
    doc.addEventListener('click', (e) => {
      if (!e.target.closest || !e.target.closest('.vt-nav')) cerrar(null);
    });
    doc.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const abierto = botones.find((b) => b.getAttribute('aria-expanded') === 'true');
      cerrar(null);
      if (abierto) abierto.focus();
    });
  }

  function barra(doc, win) {
    const bar = doc.querySelector('[data-vt-bar]');
    const hero = doc.querySelector('[data-hero-cta], .svc-hero__ctas');
    if (!bar || !hero || !('IntersectionObserver' in win)) return;
    new win.IntersectionObserver(([entrada]) => bar.classList.toggle('is-oculta', entrada.isIntersecting)).observe(hero);
  }

  const api = { FIRMA, tipoEnlace, conFirma, evento };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTTerra = Object.freeze(api);
  medir(document, root);
  const iniciar = () => { menu(document); barra(document, root); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
```

- [ ] **Step 4: Correr las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1 && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"; cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ℹ pass 11`, `ℹ fail 0`; `Ran 27 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/js/terra.js public/js/tests/terra.test.js tools/site/tests/test_paridad_terra_js.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): terra.js con menú, barra móvil y eventos de WhatsApp y teléfono" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Assets con hash (`tools/site/activos.py`)

**Files:**
- Create: `tools/site/activos.py`
- Test: `tools/site/tests/test_activos.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_activos.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402


class ActivosTest(unittest.TestCase):
    def setUp(self):
        self.pub = Path(tempfile.mkdtemp())
        (self.pub / "css").mkdir()
        (self.pub / "js").mkdir()
        (self.pub / "css" / "terra.css").write_text(".vt-a{}", encoding="utf-8")
        (self.pub / "css" / "legacy-fixes.css").write_text(".pt-0{}", encoding="utf-8")
        (self.pub / "js" / "terra.js").write_text("void 0;", encoding="utf-8")

    def test_urls_con_hash_de_10(self):
        urls = activos.urls(self.pub)
        self.assertRegex(urls["terra.css"], r"^/css/terra\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["legacy-fixes.css"], r"^/css/legacy-fixes\.[0-9a-f]{10}\.css$")
        self.assertRegex(urls["terra.js"], r"^/js/terra\.[0-9a-f]{10}\.js$")

    def test_publicar_copia_y_borra_las_viejas(self):
        viejo = self.pub / "css" / "terra.0000000000.css"
        viejo.write_text("viejo", encoding="utf-8")
        urls = activos.publicar(self.pub)
        self.assertFalse(viejo.exists())
        self.assertEqual((self.pub / urls["terra.css"].lstrip("/")).read_text(encoding="utf-8"), ".vt-a{}")
        self.assertTrue((self.pub / "css" / "terra.css").exists())
        self.assertEqual(len(list((self.pub / "css").glob("terra.*.css"))), 1)

    def test_hash_cambia_con_el_contenido(self):
        antes = activos.urls(self.pub)["terra.css"]
        (self.pub / "css" / "terra.css").write_text(".vt-b{}", encoding="utf-8")
        self.assertNotEqual(antes, activos.urls(self.pub)["terra.css"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'activos'` y `FAILED`.

- [ ] **Step 3: Implementar `tools/site/activos.py`**

```python
"""Copias con hash de los assets del shell, para servirlas con caché inmutable de un año.

La fuente vive sin hash (public/css/terra.css, public/css/legacy-fixes.css, public/js/terra.js) y el build publica
<nombre>.<10 hex>.<ext> al lado, borrando las copias viejas. Las páginas solo enlazan la copia con hash.
"""
import hashlib
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / "public"
FUENTES = {
    "terra.css": "css/terra.css",
    "legacy-fixes.css": "css/legacy-fixes.css",
    "terra.js": "js/terra.js",
}


def _con_hash(rel, contenido):
    raiz, ext = rel.rsplit(".", 1)
    return f"{raiz}.{hashlib.sha256(contenido).hexdigest()[:10]}.{ext}"


def urls(public=PUBLIC):
    """URL pública con hash de cada asset del shell, sin escribir nada."""
    public = Path(public)
    return {clave: "/" + _con_hash(rel, (public / rel).read_bytes()) for clave, rel in FUENTES.items()}


def publicar(public=PUBLIC):
    """Escribe las copias con hash que falten, borra las viejas y devuelve las URLs."""
    public = Path(public)
    resultado = urls(public)
    for clave, rel in FUENTES.items():
        fuente = public / rel
        destino = public / resultado[clave].lstrip("/")
        patron = re.compile(rf"{re.escape(fuente.stem)}\.[0-9a-f]{{10}}{re.escape(fuente.suffix)}")
        for viejo in fuente.parent.glob(f"{fuente.stem}.*{fuente.suffix}"):
            if viejo != destino and patron.fullmatch(viejo.name):
                viejo.unlink()
        if not destino.exists():
            destino.write_bytes(fuente.read_bytes())
    return resultado
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 30 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/activos.py tools/site/tests/test_activos.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): assets del shell con hash en el nombre" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---
### Task 9: Parciales del head y del menú (`tools/site/partials.py`, parte 1)

**Files:**
- Create: `tools/site/partials.py`
- Test: `tools/site/tests/test_partials.py`

Menú aprobado (spec §3.1): Pasto natural · Pasto sintético · Jardín · Plantas y palmas · Empresas · Precios + CTA "Cotizar por WhatsApp". "Jardín" y "Empresas" solo abren su panel (la página `/empresas` y la de poda llegan en la Etapa 3; entonces "Empresas" recibe su `href` y "Jardín" suma "Poda"). Sin JS, los paneles abren con `:hover` y `:focus-within`; con JS, con `aria-expanded`. En móvil, acordeón nativo con `<details>` (la sección activa abierta).

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_partials.py`:

```python
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}


def existe(href):
    archivo = paginas.PUBLIC / href.lstrip("/")
    return archivo.is_file() or (archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file()


class HeadTest(unittest.TestCase):
    def test_region_con_gtag_unico_y_assets_con_hash(self):
        h = partials.head(URLS, legacy=False)
        self.assertTrue(h.startswith("<!-- vt:head -->\n") and h.endswith("\n<!-- /vt:head -->"))
        self.assertEqual(h.count("googletagmanager.com/gtag/js?id=G-RMZCVJ734M"), 1)
        self.assertEqual(h.count("gtag('config','G-RMZCVJ734M')"), 1)
        self.assertIn('<link rel="stylesheet" href="/css/terra.0123456789.css">', h)
        self.assertIn('<script src="/js/terra.0123456789.js" defer></script>', h)
        self.assertNotIn("legacy-fixes", h)

    def test_legacy_fixes_solo_con_tailwind_y_antes_de_terra(self):
        h = partials.head(URLS, legacy=True)
        self.assertLess(h.index("legacy-fixes.0123456789.css"), h.index("terra.0123456789.css"))


class HeaderTest(unittest.TestCase):
    def setUp(self):
        self.ctx = paginas.contexto("/pasto-en-rollo-tampico")
        self.h = partials.header(self.ctx)

    def test_menu_de_seis_entradas_en_orden(self):
        textos = re.findall(r'class="vt-nav__top"[^>]*>([^<]+)', self.h)
        self.assertEqual(textos, ["Pasto natural", "Pasto sintético", "Jardín", "Plantas y palmas", "Empresas", "Precios"])

    def test_seccion_activa_y_pagina_actual(self):
        self.assertEqual(self.h.count("vt-nav__item is-activo"), 1)
        self.assertIn('<li class="vt-nav__item is-activo"><a class="vt-nav__top" href="/pasto-en-rollo-tampico">Pasto natural</a>', self.h)
        self.assertIn('<a href="/pasto-en-rollo-tampico" aria-current="page">Pasto en rollo</a>', self.h)
        self.assertIn('<details class="vt-acc" open><summary>Pasto natural<small>desde $85/m²</small></summary>', self.h)

    def test_cta_con_mensaje_del_servicio(self):
        self.assertIn('data-cta="servicio-pasto:header"', self.h)
        self.assertIn(datos.wa_url(datos.mensaje("pasto-natural")), self.h)
        self.assertIn('data-vt-tipo="servicio-pasto" data-vt-servicio="pasto-natural"', self.h)

    def test_paneles_con_ids_existentes(self):
        controles = re.findall(r'aria-controls="([^"]+)"', self.h)
        self.assertEqual(len(controles), 6)
        for control in controles:
            self.assertIn(f'id="{control}"', self.h)

    def test_precios_es_enlace_actual_en_su_pagina(self):
        h = partials.header(paginas.contexto("/precios"))
        self.assertIn('<a class="vt-nav__top" href="/precios" aria-current="page">Precios</a>', h)

    def test_enlaces_del_menu_existen(self):
        for item in partials.MENU:
            for href in ([item["href"]] if item["href"] else []) + [h for _t, h in item["items"]]:
                with self.subTest(href=href):
                    self.assertTrue(existe(href))

    def test_skip_link_y_menu_movil_oculto(self):
        self.assertIn('<a class="vt-skip" href="#main">Saltar al contenido</a>', self.h)
        self.assertIn('<nav class="vt-mmenu" id="vt-mmenu" aria-label="Principal, móvil" hidden>', self.h)
        self.assertIn('aria-controls="vt-mmenu"', self.h)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'partials'` y `FAILED`.

- [ ] **Step 3: Implementar `tools/site/partials.py` (head y menú)**

```python
"""Parciales del shell compartido: <head> esencial, menú, pie y barra fija móvil.

Cada función devuelve su región completa, con los marcadores <!-- vt:x --> y <!-- /vt:x -->, para que
tools/site/shell.py la reemplace en cualquier página. Todos los datos salen de datos.py.
"""
from html import escape

import datos

LOGO = "/img/logo-viveros-terra-tampico.svg"
P = datos.PRECIOS

MENU = (
    {"id": "pasto-natural", "texto": "Pasto natural", "href": "/pasto-en-rollo-tampico",
     "nota": f"desde ${P['pasto_solo_m2']}/m²",
     "items": (("Pasto en rollo", "/pasto-en-rollo-tampico"),
               (f"Mayoreo ({P['pasto_mayoreo_minimo_m2']} m² o más)", "/mayoreo-pasto-tampico"),
               ("Protocolo de riego", "/protocolo-cuidados-pasto-san-agustin"))},
    {"id": "pasto-sintetico", "texto": "Pasto sintético", "href": "/pasto-sintetico-tampico",
     "nota": f"desde ${P['sintetico_tienda_m2']}/m²",
     "items": (("Instalado en Tampico", "/pasto-sintetico-tampico"),
               ("Tienda con envío a todo México", "/pasto-sintetico"),
               ("Para perros", "/pasto-sintetico/perros"))},
    {"id": "jardin", "texto": "Jardín", "href": None,
     "nota": f"desde ${P['mantenimiento_mes']}/mes",
     "items": (("Diseño de jardines", "/diseno-jardines-tampico"),
               ("Mantenimiento", "/mantenimiento-jardines-tampico"),
               ("Riego automático", "/sistema-riego-tampico"))},
    {"id": "plantas", "texto": "Plantas y palmas", "href": "/plantas-palmas-arboles-tampico",
     "nota": f"{datos.VARIEDADES} variedades",
     "items": (("Todo el vivero", "/plantas-palmas-arboles-tampico"),
               ("Palmas", "/palmas-tropicales-tampico"),
               ("Plantas para jardín", "/plantas-para-jardin-tampico"),
               ("Árboles ornamentales", "/arboles-ornamentales-tampico"),
               ("Árboles para banqueta", "/arboles-para-banqueta-tampico"),
               ("Plantas de interior", "/plantas-de-interior-tampico"),
               ("Arma tu lista (catálogo)", "/catalogo"),
               ("Tierra negra", "/tierra-negra-vegetal-tampico"),
               ("Tezontle rojo", "/tezontle-rojo-tampico"),
               ("Mármol blanco", "/marmol-blanco-tampico"),
               ("Piedra bola de río", "/piedra-bola-rio-tampico"))},
    {"id": "empresas", "texto": "Empresas", "href": None,
     "nota": f"REPSE · {datos.FACTURA}",
     "items": (("Mayoreo de pasto", "/mayoreo-pasto-tampico"),
               ("Palmas para proyectos", "/palmas-mayoreo-proyectos"),
               ("Mantenimiento de áreas verdes", "/mantenimiento-jardines-tampico"))},
    {"id": "precios", "texto": "Precios", "href": "/precios", "nota": "con IVA", "items": ()},
)

SPRITE = """<svg class="vt-sprite" width="0" height="0" aria-hidden="true" focusable="false">
<symbol id="vt-i-wa" viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></symbol>
<symbol id="vt-i-tel" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></symbol>
<symbol id="vt-i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h11"/></symbol>
<symbol id="vt-i-chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
</svg>"""
CHEV = '<svg class="vt-chev" aria-hidden="true"><use href="#vt-i-chev"/></svg>'
WA_GLIFO = '<span class="vt-wa-g"><svg aria-hidden="true"><use href="#vt-i-wa"/></svg></span>'


def esc(texto):
    return escape(str(texto), quote=True)


def region(nombre, cuerpo):
    return f"<!-- vt:{nombre} -->\n{cuerpo}\n<!-- /vt:{nombre} -->"


def head(urls, legacy):
    """Favicon, CSS del shell (y legacy-fixes en páginas con Tailwind), GA4 una sola vez y terra.js diferido."""
    lineas = ['<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">']
    if legacy:
        lineas.append(f'<link rel="stylesheet" href="{urls["legacy-fixes.css"]}">')
    lineas += [
        f'<link rel="stylesheet" href="{urls["terra.css"]}">',
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={datos.GA4_ID}"></script>',
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        f"gtag('js',new Date());gtag('config','{datos.GA4_ID}');</script>",
        f'<script src="{urls["terra.js"]}" defer></script>',
    ]
    return region("head", "\n".join(lineas))


def _enlace(texto, href, ruta):
    actual = ' aria-current="page"' if href == ruta else ""
    return f'<li><a href="{href}"{actual}>{esc(texto)}</a></li>'


def _item_escritorio(item, ctx):
    clase = "vt-nav__item is-activo" if item["id"] == ctx["activo"] else "vt-nav__item"
    if not item["items"]:
        actual = ' aria-current="page"' if item["href"] == ctx["ruta"] else ""
        return f'<li class="{clase}"><a class="vt-nav__top" href="{item["href"]}"{actual}>{esc(item["texto"])}</a></li>'
    panel = f"vt-panel-{item['id']}"
    if item["href"]:
        cabeza = (f'<a class="vt-nav__top" href="{item["href"]}">{esc(item["texto"])}</a>'
                  f'<button class="vt-nav__exp" type="button" aria-expanded="false" aria-controls="{panel}">'
                  f'<span class="vt-sr">Submenú de {esc(item["texto"])}</span>{CHEV}</button>')
    else:
        cabeza = (f'<button class="vt-nav__top" type="button" aria-expanded="false" aria-controls="{panel}">'
                  f'{esc(item["texto"])}{CHEV}</button>')
    enlaces = "".join(_enlace(t, h, ctx["ruta"]) for t, h in item["items"])
    return f'<li class="{clase}">{cabeza}<ul class="vt-nav__panel" id="{panel}">{enlaces}</ul></li>'


def _item_movil(item, ctx):
    nota = f'<small>{esc(item["nota"])}</small>'
    if not item["items"]:
        actual = ' aria-current="page"' if item["href"] == ctx["ruta"] else ""
        return f'<a class="vt-mmenu__link" href="{item["href"]}"{actual}>{esc(item["texto"])}{nota}</a>'
    abierto = " open" if item["id"] == ctx["activo"] else ""
    enlaces = "".join(_enlace(t, h, ctx["ruta"]) for t, h in item["items"])
    return f'<details class="vt-acc"{abierto}><summary>{esc(item["texto"])}{nota}</summary><ul>{enlaces}</ul></details>'


def header(ctx):
    """Skip-link, íconos, menú de 6 entradas con paneles, CTA de WhatsApp con el mensaje del servicio y menú móvil."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje"]))
    escritorio = "\n".join(_item_escritorio(item, ctx) for item in MENU)
    movil = "\n".join(_item_movil(item, ctx) for item in MENU)
    cuerpo = f"""<a class="vt-skip" href="#main">Saltar al contenido</a>
{SPRITE}
<header class="vt-head" data-vt-tipo="{tipo}" data-vt-servicio="{ctx['servicio']}">
<div class="vt-head__bar">
<a class="vt-head__logo" href="/"><img src="{LOGO}" alt="Viveros Terra, inicio" width="150" height="41"></a>
<nav class="vt-nav" aria-label="Principal">
<ul class="vt-nav__list">
{escritorio}
</ul>
</nav>
<p class="vt-head__meta"><b>{datos.DOMICILIO_CORTO}</b>{datos.HORARIO}</p>
<a class="vt-btn vt-btn--wa vt-head__cta" data-cta="{tipo}:header" href="{wa}" target="_blank" rel="noopener">{WA_GLIFO}<span class="vt-head__cta-largo">Cotizar por WhatsApp</span><span class="vt-head__cta-corto">Cotizar</span></a>
<button class="vt-burger" type="button" aria-expanded="false" aria-controls="vt-mmenu"><svg aria-hidden="true"><use href="#vt-i-menu"/></svg><span class="vt-sr">Menú</span></button>
</div>
<nav class="vt-mmenu" id="vt-mmenu" aria-label="Principal, móvil" hidden>
{movil}
<p class="vt-mmenu__meta">{datos.CALLE}, Cd. Madero · <a data-cta="{tipo}:menu" href="tel:{datos.TELEFONO_TEL}">{datos.TELEFONO_VISIBLE}</a></p>
</nav>
</header>"""
    return region("header", cuerpo)
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 39 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/partials.py tools/site/tests/test_partials.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): parciales del head esencial y del menú de 6 entradas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Parciales del pie único y la barra fija móvil (`partials.py`, parte 2)

**Files:**
- Modify: `tools/site/partials.py` (se agrega al final)
- Test: `tools/site/tests/test_partials_pie.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_partials_pie.py`:

```python
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402
import paginas  # noqa: E402
import partials  # noqa: E402


def existe(href):
    archivo = paginas.PUBLIC / href.lstrip("/")
    return archivo.is_file() or (archivo / "index.html").is_file() or archivo.with_suffix(".html").is_file()


class PieTest(unittest.TestCase):
    def setUp(self):
        self.f = partials.footer(paginas.contexto("/blog"))

    def test_datos_del_pie(self):
        for texto in (datos.CALLE, datos.COLONIA, "Frente a Walmart", "Entrando por Banamex", datos.REPSE,
                      datos.PROMESA_COMPLETA, datos.GOOGLE, "desde 2012", datos.M2_INSTALADOS):
            with self.subTest(texto=texto):
                self.assertIn(texto, self.f)
        self.assertIn('data-cta="blog:footer" href="tel:+528333268008"', self.f)

    def test_barra_segun_contexto(self):
        self.assertIn("data-vt-bar", self.f)
        self.assertIn('data-cta="blog:barra"', self.f)
        for ruta in ("/pasto-sintetico", "/catalogo", "/gracias"):
            with self.subTest(ruta=ruta):
                self.assertNotIn("data-vt-bar", partials.footer(paginas.contexto(ruta)))

    def test_columnas_con_enlaces_existentes(self):
        for _titulo, enlaces in partials.PIE:
            for _texto, href in enlaces:
                with self.subTest(href=href):
                    self.assertTrue(existe(href))

    def test_sin_textos_viejos(self):
        for viejo in ("Blog de Jardinería", "líder", "Oasis", "Obregón 209,"):
            self.assertNotIn(viejo, self.f)

    def test_externos_con_noopener(self):
        html = partials.header(paginas.contexto("/")) + self.f
        for etiqueta in re.findall(r"<a\b[^>]*>", html):
            if 'target="_blank"' in etiqueta:
                self.assertIn('rel="noopener"', etiqueta)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `AttributeError: module 'partials' has no attribute 'footer'` (y `PIE`) y `FAILED (errors=5)`.

- [ ] **Step 3: Agregar al final de `tools/site/partials.py`**

```python
PIE = (
    ("Servicios", (("Pasto en rollo", "/pasto-en-rollo-tampico"),
                   ("Mayoreo de pasto", "/mayoreo-pasto-tampico"),
                   ("Pasto sintético en Tampico", "/pasto-sintetico-tampico"),
                   ("Tienda de pasto sintético", "/pasto-sintetico"),
                   ("Diseño de jardines", "/diseno-jardines-tampico"),
                   ("Mantenimiento", "/mantenimiento-jardines-tampico"),
                   ("Riego automático", "/sistema-riego-tampico"))),
    ("Plantas y materiales", (("Plantas, palmas y árboles", "/plantas-palmas-arboles-tampico"),
                              ("Palmas para proyectos", "/palmas-mayoreo-proyectos"),
                              ("Arma tu lista", "/catalogo"),
                              ("Tierra negra", "/tierra-negra-vegetal-tampico"),
                              ("Tezontle rojo", "/tezontle-rojo-tampico"),
                              ("Mármol blanco", "/marmol-blanco-tampico"),
                              ("Piedra bola de río", "/piedra-bola-rio-tampico"))),
    ("Zonas", (("Lomas de Rosales", "/jardineria-lomas-de-rosales-tampico"),
               ("Country Club", "/jardineria-country-club-tampico"),
               ("Águila y Altavista", "/jardineria-aguila-tampico"),
               ("Lomas del Chairel", "/jardineria-lomas-del-chairel-tampico"),
               ("Ciudad Madero", "/jardineria-ciudad-madero"),
               ("Altamira", "/jardineria-altamira"))),
    ("Viveros Terra", (("Visítanos", "/vivero-tampico"),
                       ("Precios", "/precios"),
                       ("Blog", "/blog"),
                       ("Políticas y garantías", "/politicas"),
                       ("Aviso de privacidad", "/politica-privacidad"))),
)
DATOS_PIE = (
    ("Domicilio", datos.CALLE, f"{datos.COLONIA}, {datos.CIUDAD}"),
    ("Referencia", "Frente a Walmart", "Entrando por Banamex"),
    ("Horario", "Lun a vie 9 a 18 h", "Sábado 9 a 14 h"),
    ("REPSE", datos.REPSE, "Padrón de la STPS"),
    ("Factura", datos.FACTURA, "Persona física o moral"),
    ("Desde", str(datos.DESDE), f"{datos.M2_INSTALADOS} instalados"),
)


def _columna(titulo, enlaces):
    items = "".join(f'<li><a href="{href}">{esc(texto)}</a></li>' for texto, href in enlaces)
    return f'<div class="vt-foot__col"><h2 class="vt-foot__h">{esc(titulo)}</h2><ul>{items}</ul></div>'


def barra(ctx):
    """Barra fija móvil [Cotizar por WhatsApp | teléfono]; terra.js la oculta mientras el CTA del hero se ve."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje"]))
    return f"""<div class="vt-bar" data-vt-bar role="region" aria-label="Contacto rápido">
<a class="vt-btn vt-btn--wa vt-bar__go" data-cta="{tipo}:barra" href="{wa}" target="_blank" rel="noopener">{WA_GLIFO}Cotizar por WhatsApp</a>
<a class="vt-bar__tel" data-cta="{tipo}:barra" href="tel:{datos.TELEFONO_TEL}" aria-label="Llamar {datos.TELEFONO_VISIBLE}"><svg aria-hidden="true"><use href="#vt-i-tel"/></svg></a>
</div>"""


def footer(ctx):
    """Pie único con columnas, contacto, promesa, cuadro de datos y redes; incluye la barra móvil si el contexto la pide."""
    tipo = ctx["tipo"]
    wa = esc(datos.wa_url(ctx["mensaje"]))
    columnas = "\n".join(_columna(titulo, enlaces) for titulo, enlaces in PIE)
    celdas = "".join(f"<div><dt>{esc(t)}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>" for t, v, s in DATOS_PIE)
    redes = "".join(f'<a href="{url}" target="_blank" rel="noopener">{esc(nombre)}</a>' for nombre, url in datos.REDES)
    contacto = (
        '<div class="vt-foot__col"><h2 class="vt-foot__h">Contacto</h2><ul>'
        f'<li><a data-cta="{tipo}:footer" href="{wa}" target="_blank" rel="noopener">WhatsApp {datos.TELEFONO_VISIBLE}</a></li>'
        f'<li><a data-cta="{tipo}:footer" href="tel:{datos.TELEFONO_TEL}">Llamar {datos.TELEFONO_VISIBLE}</a></li>'
        f'<li><a href="{datos.MAPS_URL}" target="_blank" rel="noopener">Cómo llegar</a></li></ul>'
        f'<p class="vt-foot__promesa">{esc(datos.PROMESA_COMPLETA)}</p></div>'
    )
    pie = f"""<footer class="vt-foot">
<div class="vt-wrap">
<div class="vt-foot__grid">
<div class="vt-foot__about"><img src="{LOGO}" alt="Viveros Terra" width="150" height="41" loading="lazy"><p>Vivero, pasto en rollo y jardinería en Tampico, Madero y Altamira desde {datos.DESDE}. Pasto sintético con envío a todo México desde {datos.SINTETICO_NACIONAL_DESDE}.</p><p class="vt-foot__google">{esc(datos.GOOGLE)}</p></div>
{columnas}
{contacto}
</div>
<dl class="vt-foot__datos">{celdas}</dl>
<div class="vt-foot__legal"><p>© {datos.ANIO} {datos.NOMBRE} · {datos.CIUDAD}, Tamaulipas · Precios {datos.ANIO} con IVA incluido</p><p class="vt-foot__redes">{redes}</p></div>
</div>
</footer>"""
    cuerpo = pie + ("\n" + barra(ctx) if ctx["barra"] else "")
    return region("footer", cuerpo)
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 44 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/partials.py tools/site/tests/test_partials_pie.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): pie único con 209 Sur y promesa única, y barra fija móvil de WhatsApp" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Aplicador del shell (`tools/site/shell.py`)

**Files:**
- Create: `tools/site/shell.py`
- Test: `tools/site/tests/test_shell.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_shell.py`:

```python
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import shell  # noqa: E402

URLS = {"terra.css": "/css/terra.0123456789.css", "terra.js": "/js/terra.0123456789.js",
        "legacy-fixes.css": "/css/legacy-fixes.0123456789.css"}
PAGINA = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<title>Prueba</title>
<link rel="stylesheet" href="/css/tailwind.css?v=20260706">
<!-- vt:head -->
<!-- /vt:head -->
</head>
<body>
<!-- vt:header -->
<!-- /vt:header -->
<main id="main">
<!-- svc-hero --><a class="x" href="https://wa.me/528333268008?text=Hola">Hero</a><!-- /svc-hero -->
<p><a href="https://wa.me/528333268008?text=Hola">WhatsApp</a> <a href="tel:8333268008">Tel</a> <a href="/precios">Precios</a></p>
</main>
<!-- vt:footer -->
<!-- /vt:footer -->
</body>
</html>
"""


class ShellTest(unittest.TestCase):
    def test_llena_las_tres_regiones(self):
        html = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertIn('<header class="vt-head" data-vt-tipo="blog"', html)
        self.assertIn('<footer class="vt-foot">', html)
        self.assertIn("/css/legacy-fixes.0123456789.css", html)
        self.assertEqual(html.count("googletagmanager.com/gtag/js"), 1)

    def test_idempotente(self):
        una = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertEqual(shell.aplicar(una, "/blog/palma-areca-tampico", URLS), una)

    def test_marca_ctas_del_hero_y_del_cuerpo(self):
        html = shell.aplicar(PAGINA, "/blog/palma-areca-tampico", URLS)
        self.assertIn('<a data-cta="blog:hero" class="x" href="https://wa.me/528333268008?text=Hola">', html)
        self.assertIn('<a data-cta="blog:cuerpo" href="https://wa.me/528333268008?text=Hola">WhatsApp</a>', html)
        self.assertIn('<a data-cta="blog:cuerpo" href="tel:8333268008">Tel</a>', html)
        self.assertIn('<a href="/precios">Precios</a>', html)

    def test_falla_sin_regiones(self):
        with self.assertRaises(ValueError):
            shell.aplicar("<html><head></head><body></body></html>", "/", URLS)

    def test_fin_elemento_cuenta_anidados(self):
        html = '<nav class="a"><nav class="b"></nav></nav>resto'
        self.assertEqual(shell.fin_elemento(html, 0), html.index("resto"))

    def test_aplicar_archivo_solo_escribe_si_cambia(self):
        public = Path(tempfile.mkdtemp())
        pagina = public / "blog" / "palma-areca-tampico" / "index.html"
        pagina.parent.mkdir(parents=True)
        pagina.write_text(PAGINA, encoding="utf-8")
        self.assertTrue(shell.aplicar_archivo(pagina, URLS, public=public))
        self.assertFalse(shell.aplicar_archivo(pagina, URLS, public=public))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'shell'` y `FAILED`.

- [ ] **Step 3: Implementar `tools/site/shell.py`**

```python
"""Aplica el shell compartido (head esencial, menú, pie y barra móvil) a cualquier página de public/.

Cada página lleva tres regiones marcadas: <!-- vt:head -->, <!-- vt:header --> y <!-- vt:footer -->. Este módulo
reemplaza su contenido por los parciales canónicos y marca con data-cta los enlaces de WhatsApp y teléfono del cuerpo
("<tipo>:hero" dentro de la portada, "<tipo>:cuerpo" en el resto). Es idempotente.
"""
import re
from pathlib import Path

import paginas
import partials

PUBLIC = paginas.PUBLIC
REGION_RE = re.compile(r"<!-- vt:(head|header|footer) -->.*?<!-- /vt:\1 -->", re.S)
ENLACE_RE = re.compile(
    r'<a\b(?![^>]*\bdata-cta=)([^>]*\bhref="(?:https://wa\.me/|https://api\.whatsapp\.com/|tel:)[^"]*"[^>]*)>'
)
SVC_HERO_RE = re.compile(r"<!-- svc-hero -->.*?<!-- /svc-hero -->", re.S)
VT_HERO_RE = re.compile(r'<section\b[^>]*class="vt-hero\b')


def fin_elemento(html, inicio):
    """Índice justo después del cierre del elemento que abre en `inicio` (cuenta anidados del mismo nombre)."""
    nombre = re.match(r"<([a-zA-Z][a-zA-Z0-9]*)", html[inicio:]).group(1).lower()
    etiqueta = re.compile(rf"<(/?){nombre}\b[^>]*>", re.I)
    nivel = 0
    for m in etiqueta.finditer(html, inicio):
        nivel += -1 if m.group(1) else 1
        if nivel == 0:
            return m.end()
    raise ValueError(f"<{nombre}> sin cierre desde la posición {inicio}")


def _zonas_hero(html):
    zonas = [(m.start(), m.end()) for m in SVC_HERO_RE.finditer(html)]
    vt_hero = VT_HERO_RE.search(html)
    if vt_hero:
        zonas.append((vt_hero.start(), fin_elemento(html, vt_hero.start())))
    return sorted(zonas)


def _marcar(fragmento, tipo, seccion):
    return ENLACE_RE.sub(lambda m: f'<a data-cta="{tipo}:{seccion}"{m.group(1)}>', fragmento)


def marcar_ctas(html, tipo):
    """Agrega data-cta a los enlaces wa.me y tel: que no lo tienen."""
    salida, cursor = [], 0
    for inicio, fin in _zonas_hero(html):
        if inicio < cursor:
            continue
        salida.append(_marcar(html[cursor:inicio], tipo, "cuerpo"))
        salida.append(_marcar(html[inicio:fin], tipo, "hero"))
        cursor = fin
    salida.append(_marcar(html[cursor:], tipo, "cuerpo"))
    return "".join(salida)


def aplicar(html, ruta, urls):
    """Página con el shell canónico de su ruta. Falla si no tiene exactamente una región de cada tipo."""
    ctx = paginas.contexto(ruta)
    encontradas = sorted(m.group(1) for m in REGION_RE.finditer(html))
    if encontradas != ["footer", "head", "header"]:
        raise ValueError(f"{ruta}: regiones del shell {encontradas}; debe haber head, header y footer, una de cada una")
    partes = {
        "head": partials.head(urls, legacy="/css/tailwind.css" in html),
        "header": partials.header(ctx),
        "footer": partials.footer(ctx),
    }
    html = REGION_RE.sub(lambda m: partes[m.group(1)], html)
    return marcar_ctas(html, ctx["tipo"])


def paginas_html(public=PUBLIC):
    return sorted(Path(public).rglob("*.html"))


def aplicar_archivo(path, urls, public=PUBLIC):
    """Aplica el shell al archivo; escribe solo si cambia. Devuelve True si lo escribió."""
    path = Path(path)
    original = path.read_text(encoding="utf-8")
    nuevo = aplicar(original, paginas.ruta_de(path, public), urls)
    if nuevo == original:
        return False
    path.write_text(nuevo, encoding="utf-8")
    return True


def aplicar_todo(urls, public=PUBLIC):
    """Aplica el shell a todas las páginas de public/; devuelve cuántas cambiaron."""
    return sum(aplicar_archivo(p, urls, public) for p in paginas_html(public))
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 50 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/shell.py tools/site/tests/test_shell.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): aplicador idempotente del shell con data-cta en el cuerpo" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 12: Migración única de las páginas a mano (`tools/site/migrar_shell.py`)

**Files:**
- Create: `tools/site/migrar_shell.py`
- Test: `tools/site/tests/test_migrar_shell.py`

Familias que cubre (A05 §1.2): `terra-nav` (22 páginas: home, blog/index, catálogo, cuestionario, servicios, plantas, materiales), header sticky de Tailwind (53 posts y `politicas`), header simple con `nav.nav` (`gracias`, `datos-envio`, `politica-privacidad`) y sin header (`palmas-mayoreo-proyectos` usa `terra-nav`; `protocolo` también). Todos los scripts viejos de menú tienen guarda (`if(mb)`, `if(hamburger && drawer)`) salvo uno en `sistema-riego-tampico`, que la migración protege; la prueba de consola de la Tarea 22 confirma que nada truena.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_migrar_shell.py`:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import migrar_shell  # noqa: E402

BLOG = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<title>Post</title>
<meta name="keywords" content="pasto">
<meta name="geo.region" content="MX-TAM">
<link rel="icon" type="image/png" href="/img/logo.png">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RMZCVJ734M');
</script>
</head>
<body class="text-gray-900">
<a href="https://wa.me/528333268008?text=Hola" target="_blank" rel="noopener" class="wa-float flex">WA</a>
<header class="sticky top-0 z-50"><nav class="max-w-6xl"><nav aria-label="Breadcrumb"><a href="/">Inicio</a></nav><button id="menu-btn">m</button></nav></header>
<article class="bg-white"><header class="bg-dark"><h1>Título</h1></header>
<p>Texto <a href="https://wa.me/528333268008"
   onclick="gtag('event','clic_wa_final',{'event_category':'conversion','event_label':'x'})"
   target="_blank">WA</a></p></article>
<footer class="bg-dark"><p>Blog de Jardinería</p></footer>
<script>
  const mb=document.getElementById('menu-btn'),mm=document.getElementById('mobile-menu');
  mb.addEventListener('click',()=>{mm.classList.toggle('hidden');});
  function enviar(t){ gtag('event','clic_wa_calculadora',{'event_category':'conversion','event_label':'a_'+t}); }
</script>
</body>
</html>
"""

TERRA_NAV = """<!DOCTYPE html>
<html><head><title>Home</title>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
<script src="/js/nav-scroll.js?v=1" defer></script>
</head>
<body>
<!-- HEADER -->
<nav class="terra-nav" data-page="/"><div class="terra-nav__inner"><nav class="sub"></nav></div><div class="terra-nav__drawer" id="terra-nav-drawer"></div></nav>
<section class="vt-hero"><h1>Pasto</h1></section>
<div class="vt-stickybar" role="region"><a href="tel:8333268008">Llamar</a></div>
<footer class="bg-dark">f</footer>
</body></html>
"""

GRACIAS = """<!DOCTYPE html>
<html><head><title>Gracias</title></head>
<body>
<header><nav class="nav"><a href="/">Inicio</a></nav></header>
<main>
<h1>¡Gracias!</h1>
</main>
<footer>© 2026</footer>
</body></html>
"""

CATALOGO = """<!DOCTYPE html>
<html><head><title>Catálogo</title></head>
<body>
<nav class="terra-nav" data-page="/catalogo"></nav>
<nav class="tabs" aria-label="Categorías"><button>Palmas</button></nav>
<main class="grid" id="grid" aria-label="Catálogo de plantas"></main>
<footer style="background:#000">f</footer>
</body></html>
"""


class MigrarBlogTest(unittest.TestCase):
    def setUp(self):
        self.html = migrar_shell.migrar(BLOG)

    def test_quita_shell_viejo_y_deja_el_header_del_articulo(self):
        self.assertNotIn("wa-float", self.html)
        self.assertNotIn('class="sticky', self.html)
        self.assertNotIn('id="menu-btn"', self.html)
        self.assertNotIn("<footer", self.html)
        self.assertIn('<header class="bg-dark"><h1>Título</h1></header>', self.html)

    def test_quita_gtag_meta_iconos_y_eventos_clic(self):
        for viejo in ("googletagmanager", "keywords", "geo.region", 'rel="icon"', "clic_"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, self.html)
        self.assertIn('href="https://wa.me/528333268008"\n   target="_blank">WA</a>', self.html)

    def test_protege_el_script_de_menu_sin_guarda(self):
        self.assertIn("if(mb&&mm)mb.addEventListener('click'", self.html)

    def test_regiones_y_main(self):
        for region in ("head", "header", "footer"):
            self.assertEqual(self.html.count(f"<!-- vt:{region} -->"), 1)
            self.assertEqual(self.html.count(f"<!-- /vt:{region} -->"), 1)
        self.assertEqual(self.html.count('<main id="main">'), 1)
        self.assertLess(self.html.index('<main id="main">'), self.html.index("<article"))
        self.assertIn("</main>\n<!-- vt:footer -->", self.html)
        self.assertLess(self.html.index("<!-- vt:head -->"), self.html.index("</head>"))

    def test_idempotente(self):
        self.assertEqual(migrar_shell.migrar(self.html), self.html)


class MigrarOtrasFamiliasTest(unittest.TestCase):
    def test_terra_nav_y_barra_vieja_de_la_home(self):
        html = migrar_shell.migrar(TERRA_NAV)
        for viejo in ('class="terra-nav"', "terra-nav-drawer", "vt-stickybar", "nav-scroll.js", "googletagmanager", "<footer"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, html)
        self.assertIn('<section class="vt-hero"><h1>Pasto</h1></section>', html)
        self.assertEqual(html.count('<main id="main">'), 1)

    def test_main_existente_recibe_id(self):
        html = migrar_shell.migrar(GRACIAS)
        self.assertNotIn('<nav class="nav"', html)
        self.assertEqual(html.count("<main"), 1)
        self.assertIn('<main id="main">\n<h1>¡Gracias!</h1>', html)

    def test_main_del_catalogo_pasa_a_div(self):
        html = migrar_shell.migrar(CATALOGO)
        self.assertIn('<div class="grid" id="grid" aria-label="Catálogo de plantas"></div>', html)
        self.assertIn('<nav class="tabs" aria-label="Categorías">', html)
        self.assertEqual(html.count("<main"), 1)
        self.assertIn('<main id="main">', html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'migrar_shell'` y `FAILED`.

- [ ] **Step 3: Implementar `tools/site/migrar_shell.py`**

```python
"""Migración única de las páginas escritas a mano al shell compartido (Etapa 1).

Quita el menú viejo (terra-nav o header sticky del blog), los pies, el botón flotante de WhatsApp, la barra móvil de
la home, el gtag duplicado, las meta heredadas, los favicons sueltos, nav-scroll.js y los eventos sueltos clic_*;
protege el único script de menú sin guarda; inserta las regiones vacías del shell y envuelve el contenido en
<main id="main">. Después, tools/site/build.py llena las regiones. Las páginas que ya tienen regiones no se tocan.

Uso: python3 tools/site/migrar_shell.py   (una sola vez, desde cualquier carpeta)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from shell import PUBLIC, fin_elemento, paginas_html  # noqa: E402

GTAG_RE = re.compile(
    r"(?:<!-- Google tag \(gtag\.js\) -->\s*)?"
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-RMZCVJ734M"></script>\s*'
    r"<script>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];.*?"
    r"gtag\(\s*'config'\s*,\s*'G-RMZCVJ734M'\s*\);?\s*</script>[ \t]*\n?",
    re.S,
)
META_RE = re.compile(
    r'[ \t]*<meta name="(?:keywords|geo\.region|geo\.placename|ai-content-declaration|last-modified|language)"[^>]*>[ \t]*\n?'
)
ICONO_RE = re.compile(r'[ \t]*<link rel="(?:icon|shortcut icon)"[^>]*>[ \t]*\n?')
NAV_SCROLL_RE = re.compile(r'[ \t]*<script src="/js/nav-scroll\.js[^"]*"[^>]*></script>[ \t]*\n?')
ONCLICK_CLIC_RE = re.compile(r"""\s+onclick="gtag\('event',\s*'clic_[^"]*\"""")
EVENTO_CLIC_RE = re.compile(r"[ \t]*gtag\('event',\s*'clic_[^']*',\s*\{[^{}]*\}\);?[ \t]*\n?")
MENU_SIN_GUARDA_RE = re.compile(r"^(\s*)mb\.addEventListener\(", re.M)


def quitar_elemento(html, patron):
    """Quita el primer elemento cuya etiqueta de apertura coincide con `patron`. Devuelve (html, quitados)."""
    m = re.search(patron, html)
    if not m:
        return html, 0
    return html[:m.start()] + html[fin_elemento(html, m.start()):], 1


def quitar_todos(html, patron):
    total = 0
    while True:
        html, quitado = quitar_elemento(html, patron)
        if not quitado:
            return html, total
        total += quitado


def quitar_header_viejo(html):
    """Quita el primer <header> con <nav> que aparece antes del primer <main> o <article> (el de los artículos se queda)."""
    limite = re.search(r"<(?:main|article)\b", html)
    tope = limite.start() if limite else len(html)
    for m in re.finditer(r"<header\b", html[:tope]):
        fin = fin_elemento(html, m.start())
        if "<nav" in html[m.start():fin]:
            return html[:m.start()] + html[fin:], 1
    return html, 0


def insertar_regiones(html):
    html = html.replace("</head>", "<!-- vt:head -->\n<!-- /vt:head -->\n</head>", 1)
    html = re.sub(r"(<body\b[^>]*>)", r"\1\n<!-- vt:header -->\n<!-- /vt:header -->", html, count=1)
    cierre = html.rindex("</body>")
    return html[:cierre] + "<!-- vt:footer -->\n<!-- /vt:footer -->\n" + html[cierre:]


def envolver_main(html):
    """Deja un solo <main id="main">: reutiliza el que exista o envuelve todo lo que hay entre header y footer."""
    m = re.search(r"<main\b([^>]*)>", html)
    if m and 'id="main"' in m.group(1):
        return html
    if m and "id=" not in m.group(1):
        return html[:m.start()] + f'<main id="main"{m.group(1)}>' + html[m.end():]
    if m:
        # Un <main> con otro id (la rejilla del catálogo) pasa a <div> para poder envolver la página.
        fin = fin_elemento(html, m.start())
        bloque = html[m.start():fin]
        bloque = "<div" + bloque[len("<main"):-len("</main>")] + "</div>"
        html = html[:m.start()] + bloque + html[fin:]
    html = html.replace("<!-- /vt:header -->", '<!-- /vt:header -->\n<main id="main">', 1)
    return html.replace("<!-- vt:footer -->", "</main>\n<!-- vt:footer -->", 1)


def migrar(html):
    if "<!-- vt:header -->" in html:
        return html
    html, _ = quitar_elemento(html, r'<nav class="terra-nav"')
    html, _ = quitar_header_viejo(html)
    html, _ = quitar_todos(html, r"<footer\b")
    html, _ = quitar_todos(html, r'<a\b[^>]*class="[^"]*\bwa-float\b')
    html, _ = quitar_elemento(html, r'<div class="vt-stickybar"')
    html = GTAG_RE.sub("", html)
    html = META_RE.sub("", html)
    html = ICONO_RE.sub("", html)
    html = NAV_SCROLL_RE.sub("", html)
    html = ONCLICK_CLIC_RE.sub("", html)
    html = EVENTO_CLIC_RE.sub("", html)
    html = MENU_SIN_GUARDA_RE.sub(r"\1if(mb&&mm)mb.addEventListener(", html)
    return envolver_main(insertar_regiones(html))


def main():
    migradas = 0
    for path in paginas_html():
        original = path.read_text(encoding="utf-8")
        nuevo = migrar(original)
        if nuevo != original:
            path.write_text(nuevo, encoding="utf-8")
            migradas += 1
            print(f"migrada {path.relative_to(PUBLIC)}")
    print(f"{migradas} páginas migradas")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 58 tests` y `OK`. (Todavía no se corre sobre `public/`: eso es la Tarea 15.)

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/migrar_shell.py tools/site/tests/test_migrar_shell.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): migración de las páginas a mano a las regiones del shell" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 13: El generador de pasto emite las regiones del shell

**Files:**
- Modify: `tools/pasto/common.py`, `tools/pasto/precios.py`, `tools/pasto/zonas.py`, `tools/pasto/ciudad.py`, `tools/pasto/perros.py`, `tools/pasto/hub.py`, `tools/pasto/local.py`, `tools/pasto/ficha.py`, `tools/pasto/sitemap.py`, `tools/pasto/build.py`, `public/css/tienda-pasto.css`
- Test: `tools/pasto/tests/test_shell_regiones.py`, `tools/pasto/tests/test_sitemap.py`
- Regenerated: las 30 páginas de pasto, `public/css/terra.*.css`, `public/css/legacy-fixes.*.css`, `public/js/terra.*.js`

- [ ] **Step 1: Escribir las pruebas que fallan**

`tools/pasto/tests/test_shell_regiones.py`:

```python
import unittest

from data import MODELOS
from ficha import build_ficha
from hub import build_hub
from precios import build_precios
from zonas import ZONAS, build_zona


def paginas():
    slug, zona = next(iter(ZONAS.items()))
    return {"hub": build_hub(), "ficha": build_ficha(MODELOS[0]), "precios": build_precios(), "zona": build_zona(slug, zona)}


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
                for viejo in ('class="site-footer"', "googletagmanager", 'class="skip-link"', '<header class="site-header">'):
                    self.assertNotIn(viejo, html)

    def test_barra_de_la_tienda_solo_en_la_tienda(self):
        p = paginas()
        self.assertIn("site-header--sub", p["hub"])
        self.assertIn("site-header--sub", p["ficha"])
        self.assertNotIn("site-header--sub", p["precios"])
        self.assertNotIn("site-header--sub", p["zona"])


if __name__ == "__main__":
    unittest.main()
```

Agregar al final de la clase `SitemapTest` en `tools/pasto/tests/test_sitemap.py` (antes de `if __name__ == "__main__":`):

```python
    def test_conservar_no_toca_lastmod_existente(self):
        sitemap.upsert(["https://x.com/a", "https://x.com/c"], lastmod="2026-10-05", conservar=True)
        xml = self.tmp.read_text(encoding="utf-8")
        self.assertIn("<loc>https://x.com/a</loc><lastmod>2020-01-01</lastmod>", xml)
        self.assertIn("<loc>https://x.com/c</loc><lastmod>2026-10-05</lastmod>", xml)
```

- [ ] **Step 2: Correr las pruebas (deben fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -3`
Expected: `Ran 57 tests` y `FAILED (failures=3, errors=1)` (las 3 de regiones fallan; `conservar` da `TypeError: upsert() got an unexpected keyword argument 'conservar'`).

- [ ] **Step 3: Aplicar los cambios de `sitemap.py`**

Cambio 1 en `tools/pasto/sitemap.py`. Reemplazar exactamente:

```python
def upsert(urls, lastmod=None, changefreq="monthly", priority="0.8"):
    """Actualiza lastmod de las URLs que ya existen y agrega las que faltan."""
```

por:

```python
def upsert(urls, lastmod=None, changefreq="monthly", priority="0.8", conservar=False):
    """Agrega las URLs que faltan; actualiza lastmod de las que ya existen salvo con conservar=True."""
```

Cambio 2 en `tools/pasto/sitemap.py`. Reemplazar exactamente:

```python
        if entry.search(xml):
            xml = entry.sub(lambda m: m.group(1) + lastmod + m.group(2), xml, count=1)
            continue
```

por:

```python
        if entry.search(xml):
            if not conservar:
                xml = entry.sub(lambda m: m.group(1) + lastmod + m.group(2), xml, count=1)
            continue
```

- [ ] **Step 4: Aplicar los cambios de los generadores (head con regiones vacías, sin header ni pie propios, `<main id="main">`)**

Cambio 1 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
from data import ASSET_VERSION, ESTADOS_ORDEN, PHONE_DISPLAY, SITE, UPDATED, WA_NUMBER
```

por:

```python
from data import ASSET_VERSION, ESTADOS_ORDEN, SITE, WA_NUMBER
```

Cambio 2 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
def head(*, title, description, canonical, og_image, og_type, preload_img, preload_srcset, ld, extra=""):
    return f"""<!DOCTYPE html>
```

por:

```python
def head(*, title, description, canonical, og_image, og_type, preload_img, preload_srcset, ld, extra="", subnav=True):
    """<head> y apertura de <body> con las regiones vacías del shell; con subnav, la barra contextual de la tienda."""
    barra_tienda = SUBNAV if subnav else ""
    return f"""<!DOCTYPE html>
```

Cambio 3 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">
```

por:

```python
<meta name="twitter:card" content="summary_large_image">
```

Cambio 4 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
<script type="application/ld+json">{ld}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
{extra}<script src="/js/vt-mensualidades.js?v={ASSET_VERSION}" defer></script>
<script src="/js/tienda-pasto.js?v={ASSET_VERSION}" defer></script>
</head>
<body>
{SYMBOLS}
<a class="skip-link" href="#comprar">Ir al cotizador</a>
{HEADER}"""
```

por:

```python
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
{barra_tienda}"""
```

Cambio 5 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
HEADER = """<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="/" aria-label="Viveros Terra, inicio"><img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="140" height="36"></a>
    <nav class="site-nav" aria-label="Tienda de pasto sintético">
      <a href="/pasto-sintetico#modelos">Los 9 modelos</a>
      <a href="/pasto-sintetico#elegir">¿Cuál me conviene?</a>
      <a href="/pasto-sintetico#como-funciona">Cómo comprar</a>
      <a href="/pasto-sintetico-tampico">Tampico</a>
      <a href="/">Viveros Terra</a>
    </nav>
    <button class="quote-btn" type="button" data-open-cot aria-haspopup="dialog">
```

por:

```python
# Barra contextual de la tienda, debajo del menú principal del shell (spec §3.1).
SUBNAV = """<div class="site-header site-header--sub">
  <div class="wrap site-header__bar">
    <nav class="site-nav" aria-label="Tienda de pasto sintético">
      <a href="/pasto-sintetico#modelos">Los 9 modelos</a>
      <a href="/pasto-sintetico#elegir">¿Cuál me conviene?</a>
      <a href="/pasto-sintetico#como-funciona">Cómo comprar</a>
    </nav>
    <button class="quote-btn" type="button" data-open-cot aria-haspopup="dialog">
```

Cambio 6 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
      <span class="quote-btn__count num" data-cot-count data-empty="true">0</span>
    </button>
  </div>
</header>
"""
```

por:

```python
      <span class="quote-btn__count num" data-cot-count data-empty="true">0</span>
    </button>
  </div>
</div>
"""
```

Cambio 7 en `tools/pasto/common.py`. Reemplazar exactamente:

```python
def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="130" height="34" loading="lazy">
        <p>Pasto sintético con envío a todo México. Vivero, showroom y servicios de jardinería desde 2007.</p>
        <p><a href="https://maps.app.goo.gl/xC4XGL2WeucAjGwAA" target="_blank" rel="noopener">Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, 89510 Cd. Madero, Tamps.</a><br><a href="https://maps.app.goo.gl/xC4XGL2WeucAjGwAA" target="_blank" rel="noopener">Google Maps</a> · <a href="https://maps.apple.com/?daddr=22.2777575,-97.8433341&amp;q=Viveros%20Terra" target="_blank" rel="noopener">Apple Maps</a></p>
      </div>
      <div>
        <h3>Tienda</h3>
        <ul>
          <li><a href="/pasto-sintetico">Los 9 modelos</a></li>
          <li><a href="/blog/cuanto-cuesta-pasto-sintetico-mexico">Cuánto cuesta</a></li>
          <li><a href="/blog/que-altura-de-pasto-sintetico-elegir">Qué altura elegir</a></li>
          <li><a href="/blog/como-instalar-pasto-sintetico">Cómo instalarlo</a></li>
          <li><a href="/politicas">Envíos y devoluciones</a></li>
        </ul>
      </div>
      <div>
        <h3>Viveros Terra</h3>
        <ul>
          <li><a href="/pasto-sintetico-tampico">Pasto sintético en Tampico</a></li>
          <li><a href="/pasto-en-rollo-tampico">Pasto natural en rollo</a></li>
          <li><a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a></li>
          <li><a href="/diseno-jardines-tampico">Diseño de jardines</a></li>
          <li><a href="{wa('Hola, tengo una pregunta sobre pasto sintético')}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li>Lun a vie 9 a 18 h · Sáb 9 a 14 h</li>
        </ul>
      </div>
    </div>
    <p class="site-footer__legal">© 2026 Viveros Terra · Tampico, Tamaulipas, México · Actualizado {UPDATED}</p>
  </div>
</footer>
"""
```

por:

```python
def footer():
    """Región vacía del pie: tools/site/shell.py la llena con el pie único y la barra móvil."""
    return "<!-- vt:footer -->\n<!-- /vt:footer -->\n"
```

Cambio 8 en `tools/pasto/precios.py`. Reemplazar exactamente:

```python
HEADER = """<header class="site-header">
  <div class="wrap site-header__bar">
    <a class="site-header__logo" href="/" aria-label="Viveros Terra, inicio"><img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="140" height="36"></a>
    <nav class="site-nav" aria-label="Principal">
      <a href="/pasto-en-rollo-tampico">Pasto en rollo</a>
      <a href="/pasto-sintetico">Pasto sintético</a>
      <a href="/plantas-palmas-arboles-tampico">Plantas y palmas</a>
      <a href="/diseno-jardines-tampico">Diseño</a>
      <a href="/mantenimiento-jardines-tampico">Mantenimiento</a>
    </nav>
    <a class="quote-btn" href="{wa}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-wa"/></svg><span>Cotizar</span></a>
  </div>
</header>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" width="130" height="34" loading="lazy">
        <p>Vivero, pasto en rollo y servicios de jardinería en Tampico, Madero y Altamira desde 2007.</p>
        <p><a href="{MAPS}" target="_blank" rel="noopener">Av. Álvaro Obregón 209, Col. Ampliación Unidad Nacional, 89510 Cd. Madero, Tamps.</a><br><a href="{MAPS}" target="_blank" rel="noopener">Google Maps</a> · <a href="{APPLE_MAPS}" target="_blank" rel="noopener">Apple Maps</a></p>
      </div>
      <div>
        <h3>Servicios</h3>
        <ul>
          <li><a href="/pasto-en-rollo-tampico">Pasto en rollo</a></li>
          <li><a href="/mantenimiento-jardines-tampico">Mantenimiento</a></li>
          <li><a href="/diseno-jardines-tampico">Diseño de jardines</a></li>
          <li><a href="/sistema-riego-tampico">Riego automático</a></li>
          <li><a href="/pasto-sintetico-tampico">Pasto sintético en Tampico</a></li>
        </ul>
      </div>
      <div>
        <h3>Contacto</h3>
        <ul>
          <li><a href="{wa('Hola, tengo una pregunta sobre precios')}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li><a href="tel:+528333268008">Llamar {PHONE_DISPLAY}</a></li>
          <li>Lun a vie 9 a 18 h · Sáb 9 a 14 h</li>
          <li><a href="/politicas">Envíos, devoluciones y garantías</a></li>
        </ul>
      </div>
    </div>
    <p class="site-footer__legal">© 2026 Viveros Terra · Cd. Madero, Tamaulipas, México · Actualizado {UPDATED}</p>
  </div>
</footer>
"""
```

por nada (se borra el bloque completo).

Cambio 9 en `tools/pasto/precios.py`. Reemplazar exactamente:

```python
from common import (SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, head, jsonld, section_open, wa)
```

por:

```python
from common import (SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, footer, head, jsonld, section_open, wa)
```

Cambio 10 en `tools/pasto/precios.py`. Reemplazar exactamente:

```python
MAPS = "https://maps.app.goo.gl/xC4XGL2WeucAjGwAA"
APPLE_MAPS = "https://maps.apple.com/?daddr=22.2777575,-97.8433341&amp;q=Viveros%20Terra"
```

por nada (se borra el bloque completo).

Cambio 11 en `tools/pasto/precios.py`. Reemplazar exactamente:

```python
        preload_img=f"{IMG}-sm.webp", preload_srcset=f"{IMG}-sm.webp 560w, {IMG}.webp 960w", ld=schema(faqs),
    )
    base = (base.split('<script src="/js/vt-mensualidades.js')[0]
            + base.split('<script src="/js/tienda-pasto.js', 1)[1].split("defer></script>", 1)[1])
    base = base.split('<header class="site-header">')[0].replace(
        '<a class="skip-link" href="#comprar">Ir al cotizador</a>', '<a class="skip-link" href="#pasto">Ir a la lista de precios</a>')
    base += HEADER.format(wa=wa("Hola, vi la lista de precios y quiero cotizar"))
    return "".join([base, f"""
<main>
```

por:

```python
        preload_img=f"{IMG}-sm.webp", preload_srcset=f"{IMG}-sm.webp 560w, {IMG}.webp 960w", ld=schema(faqs),
        subnav=False,
    )
    base = (base.split('<script src="/js/vt-mensualidades.js')[0]
            + base.split('<script src="/js/tienda-pasto.js', 1)[1].split("defer></script>", 1)[1])
    return "".join([base, f"""
<main id="main">
```

Cambio 12 en `tools/pasto/zonas.py`. Reemplazar exactamente:

```python
from common import SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, head, jsonld, section_open, wa
from data import SITE
from precios import HEADER, footer
```

por:

```python
from common import SECTION_CLOSE, breadcrumb_schema, esc, faq_html, faq_schema, footer, head, jsonld, section_open, wa
from data import SITE
```

Cambio 13 en `tools/pasto/zonas.py`. Reemplazar exactamente:

```python
/img/portadas/{img}.webp {z['img'][1]}w", ld=ld)
    base = (base.split('<script src="/js/vt-mensualidades.js')[0]
            + base.split('<script src="/js/tienda-pasto.js', 1)[1].split("defer></script>", 1)[1])
    base = base.split('<header class="site-header">')[0].replace(
        '<a class="skip-link" href="#comprar">Ir al cotizador</a>', '<a class="skip-link" href="#colonias">Ir al contenido</a>')
    base += HEADER.format(wa=wa(guided(z["corto"])))
    return "".join([base, f"""
<main>
```

por:

```python
/img/portadas/{img}.webp {z['img'][1]}w", ld=ld, subnav=False)
    base = (base.split('<script src="/js/vt-mensualidades.js')[0]
            + base.split('<script src="/js/tienda-pasto.js', 1)[1].split("defer></script>", 1)[1])
    return "".join([base, f"""
<main id="main">
```

Cambio 14 en `tools/pasto/ciudad.py`. Reemplazar exactamente:

```python
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#modelos">Ir a los modelos</a>'), f"""
<main>
```

por:

```python
    return "".join([base, f"""
<main id="main">
```

Cambio 15 en `tools/pasto/perros.py`. Reemplazar exactamente:

```python
    return "".join([base.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                 '<a class="skip-link" href="#elegir">Ir al contenido</a>'), f"""
<main>
```

por:

```python
    return "".join([base, f"""
<main id="main">
```

Cambio 16 en `tools/pasto/hub.py`. Reemplazar exactamente:

```python
/js/tienda-hub.js?v={ASSET_VERSION}" defer></script>\n'),
        f"""
<main>
```

por:

```python
/js/tienda-hub.js?v={ASSET_VERSION}" defer></script>\n'),
        f"""
<main id="main">
```

Cambio 17 en `tools/pasto/hub.py`. Reemplazar exactamente:

```python
    return "".join(parts).replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                                  '<a class="skip-link" href="#modelos">Ir a los modelos</a>')
```

por:

```python
    return "".join(parts)
```

Cambio 18 en `tools/pasto/local.py`. Reemplazar exactamente:

```python
id="vt-models">{models_json}</script>\n'),
        f"""
<main>
```

por:

```python
id="vt-models">{models_json}</script>\n'),
        f"""
<main id="main">
```

Cambio 19 en `tools/pasto/local.py`. Reemplazar exactamente:

```python
    return html.replace('<a class="skip-link" href="#comprar">Ir al cotizador</a>',
                        '<a class="skip-link" href="#opciones">Ir a precios y opciones</a>')
```

por:

```python
    return html
```

Cambio 20 en `tools/pasto/ficha.py`. Reemplazar exactamente:

```python
extra=(f'<script type="application/json" id="vt-model">{model_json}</script>\n' + LANDED_SCRIPTS)),
        f"""
<main>
```

por:

```python
extra=(f'<script type="application/json" id="vt-model">{model_json}</script>\n' + LANDED_SCRIPTS)),
        f"""
<main id="main">
```

- [ ] **Step 5: Reemplazar `tools/pasto/build.py` completo (registra lo escrito, conserva `lastmod`, aplica el shell)**

```python
"""Genera el hub, las 9 fichas de pasto sintético, la página local de Tampico, /precios y las 6 zonas,
y les aplica el shell compartido de tools/site (menú, pie, barra móvil y head esencial).

Uso: python3 tools/pasto/build.py   (desde la raíz del repo). Para todo el sitio: python3 tools/site/build.py
"""
import sys
from pathlib import Path

from ciudad import build_ciudad
from ciudades import CIUDADES
from data import MODELOS, SITE
from feed import build_feed
from ficha import build_ficha
from hub import build_hub
from local import build_local
from perros import build_perros
from precios import build_precios
from sitemap import upsert
from zonas import ZONAS, build_zona

ROOT = Path(__file__).resolve().parents[2] / "public" / "pasto-sintetico"
HERRAMIENTAS_SITIO = Path(__file__).resolve().parents[1] / "site"
ESCRITAS = []


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    ESCRITAS.append(path)
    print(f"ok {path.relative_to(ROOT.parent)} ({len(html) // 1024} KB)")


def aplicar_shell(paths):
    """Llena las regiones del shell de las páginas recién escritas (mismo resultado que tools/site/build.py)."""
    if str(HERRAMIENTAS_SITIO) not in sys.path:
        sys.path.insert(0, str(HERRAMIENTAS_SITIO))
    import activos
    import shell
    urls = activos.publicar()
    for path in paths:
        shell.aplicar_archivo(path, urls)


def main():
    ESCRITAS.clear()
    write(ROOT / "index.html", build_hub())
    write(ROOT.parent / "pasto-sintetico-tampico" / "index.html", build_local())
    write(ROOT.parent / "precios" / "index.html", build_precios())
    for slug, zona in ZONAS.items():
        write(ROOT.parent / slug / "index.html", build_zona(slug, zona))
    for m in MODELOS:
        write(ROOT / m["slug"] / "index.html", build_ficha(m))
    for c in CIUDADES:
        write(ROOT / "envio" / c["slug"] / "index.html", build_ciudad(c))
    write(ROOT / "perros" / "index.html", build_perros())
    (ROOT.parent / "feed-pasto-sintetico.xml").write_text(build_feed(), encoding="utf-8")
    upsert([f"{SITE}/pasto-sintetico", f"{SITE}/pasto-sintetico/perros"]
           + [f"{SITE}/pasto-sintetico/envio/{c['slug']}" for c in CIUDADES]
           + [f"{SITE}/pasto-sintetico/{m['slug']}" for m in MODELOS], conservar=True)
    aplicar_shell(ESCRITAS)


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Barra contextual de la tienda bajo el menú principal: agregar al final de `public/css/tienda-pasto.css`**

```css

/* Etapa 1: barra contextual de la tienda debajo del menú principal del shell (terra.css). */
.site-header--sub { top: var(--vt-head-h, 56px); z-index: 800; }
.site-header--sub .site-header__bar { height: 48px; justify-content: flex-end; }
@media (min-width: 1100px) { .site-header--sub .site-header__bar { justify-content: space-between; } }
.quote-btn__count[data-empty="true"] { display: none; }
```

- [ ] **Step 7: Correr las pruebas de pasto (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -3`
Expected: `Ran 57 tests` y `OK`.

- [ ] **Step 8: Regenerar las 30 páginas de pasto con el shell**

```bash
cd ~/dev/viverosterra-e1
python3 tools/pasto/build.py | tail -1
grep -c '<header class="vt-head"' public/pasto-sintetico/index.html public/precios/index.html public/jardineria-altamira/index.html
git diff --quiet -- public/sitemap.xml && echo "sitemap sin cambios"
ls public/css/terra.*.css public/css/legacy-fixes.*.css public/js/terra.*.js
```

Expected: `ok pasto-sintetico/perros/index.html (… KB)`; `1` por cada una de las tres páginas; `sitemap sin cambios`; un archivo con hash de cada asset.

- [ ] **Step 9: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/pasto public/css/tienda-pasto.css public/css public/js public/pasto-sintetico public/pasto-sintetico-tampico public/precios public/jardineria-aguila-tampico public/jardineria-altamira public/jardineria-ciudad-madero public/jardineria-country-club-tampico public/jardineria-lomas-de-rosales-tampico public/jardineria-lomas-del-chairel-tampico public/feed-pasto-sintetico.xml
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(pasto): páginas generadas con el shell compartido y barra contextual de la tienda" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 14: Retirar el borrador publicado `preview-mapa-cobertura.html`

**Files:**
- Delete: `public/preview-mapa-cobertura.html`
- Modify: `vercel.json` (2 redirects)
- Test: `tools/site/tests/test_borrador.py`

Va antes de la migración porque el build falla con rutas sin contexto y el borrador no debe tenerlo.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_borrador.py`:

```python
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402


class BorradorTest(unittest.TestCase):
    def test_borrador_eliminado_y_redirigido_a_la_home(self):
        self.assertFalse((paginas.PUBLIC / "preview-mapa-cobertura.html").exists())
        redirects = json.loads((paginas.PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        destinos = {r["source"]: r["destination"] for r in redirects}
        self.assertEqual(destinos.get("/preview-mapa-cobertura"), "/")
        self.assertEqual(destinos.get("/preview-mapa-cobertura.html"), "/")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 59 tests` y `FAILED (failures=1)`.

- [ ] **Step 3: Borrar el archivo y agregar los redirects**

```bash
cd ~/dev/viverosterra-e1
git rm -q public/preview-mapa-cobertura.html
python3 - <<'EOF'
import json
from pathlib import Path

p = Path("vercel.json")
cfg = json.loads(p.read_text(encoding="utf-8"))
cfg["redirects"] += [
    {"source": "/preview-mapa-cobertura", "destination": "/", "permanent": True},
    {"source": "/preview-mapa-cobertura.html", "destination": "/", "permanent": True},
]
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
git diff --stat vercel.json
```

Expected: `vercel.json | 10 ++++++++++`.

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 59 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add vercel.json tools/site/tests/test_borrador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(seo): retirar el borrador preview-mapa-cobertura con 301 a la home" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 15: Migración de las 78 páginas a mano y build de todo el sitio

**Files:**
- Create: `tools/site/build.py`
- Test: `tools/site/tests/test_sitio.py`
- Modify: las 78 páginas a mano de `public/` (migración + shell)

- [ ] **Step 1: Escribir la prueba de todo el sitio (falla)**

`tools/site/tests/test_sitio.py`:

```python
"""Pruebas sobre todo public/: shell canónico sin deriva, landmarks, medición y shell viejo retirado."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import paginas  # noqa: E402
import shell  # noqa: E402

PUBLIC = paginas.PUBLIC
PAGINAS = {p: p.read_text(encoding="utf-8") for p in shell.paginas_html()}
ENLACE_CONTACTO_RE = re.compile(r'<a\b[^>]*\bhref="(?:https://wa\.me/|https://api\.whatsapp\.com/|tel:)[^"]*"[^>]*>')
VIEJOS = (
    ("menú terra-nav", r'<nav class="terra-nav"'),
    ("header de la tienda", r'<header class="site-header"'),
    ("pie de la tienda", r'class="site-footer"'),
    ("botón flotante", r'class="[^"]*\bwa-float\b'),
    ("botón de menú viejo", r'id="menu-btn"'),
    ("barra móvil vieja de la home", r'class="vt-stickybar"'),
    ("nav-scroll.js", r"nav-scroll\.js"),
    ("eventos sueltos clic_*", r"'clic_"),
)


def nombre(path):
    return str(path.relative_to(PUBLIC))


class ShellEnTodoElSitioTest(unittest.TestCase):
    def test_108_paginas_con_contexto(self):
        self.assertEqual(len(PAGINAS), 108)
        for path in PAGINAS:
            paginas.contexto(paginas.ruta_de(path))

    def test_shell_canonico_sin_deriva(self):
        urls = activos.urls()
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(shell.aplicar(html, paginas.ruta_de(path), urls), html)

    def test_un_main_un_skip_link_un_header_del_shell(self):
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(len(re.findall(r"<main\b", html)), 1)
                self.assertIn('<main id="main"', html)
                self.assertEqual(html.count('href="#main"'), 1)
                self.assertEqual(html.count('<header class="vt-head"'), 1)
                self.assertEqual(html.count('<footer class="vt-foot">'), 1)

    def test_gtag_una_sola_vez(self):
        for path, html in PAGINAS.items():
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(html.count("googletagmanager.com/gtag/js?id=G-RMZCVJ734M"), 1)
                self.assertEqual(html.count("gtag('config','G-RMZCVJ734M')"), 1)

    def test_shell_viejo_retirado(self):
        for path, html in PAGINAS.items():
            for descripcion, patron in VIEJOS:
                with self.subTest(pagina=nombre(path), viejo=descripcion):
                    self.assertIsNone(re.search(patron, html))

    def test_todo_enlace_de_whatsapp_o_telefono_lleva_data_cta(self):
        for path, html in PAGINAS.items():
            sin_cta = [e for e in ENLACE_CONTACTO_RE.findall(html) if "data-cta=" not in e]
            with self.subTest(pagina=nombre(path)):
                self.assertEqual(sin_cta, [])

    def test_assets_con_hash_existen_y_no_hay_copias_viejas(self):
        for url in activos.urls().values():
            self.assertTrue((PUBLIC / url.lstrip("/")).is_file(), url)
        self.assertEqual(len(list((PUBLIC / "css").glob("terra.*.css"))), 1)
        self.assertEqual(len(list((PUBLIC / "css").glob("legacy-fixes.*.css"))), 1)
        self.assertEqual(len(list((PUBLIC / "js").glob("terra.*.js"))), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_sitio.py 2>&1 | tail -3`
Expected: `Ran 7 tests` y `FAILED (failures=…, errors=…)` (las páginas a mano no tienen regiones: `ValueError: /: regiones del shell []`).

- [ ] **Step 3: Crear `tools/site/build.py`**

```python
"""Punto de entrada único del sitio: genera las páginas de pasto, publica los assets del shell con hash y aplica el
shell a todas las páginas de public/. CI verifica que correrlo deje public/ sin cambios.

Uso: python3 tools/site/build.py   (desde cualquier carpeta)
"""
import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTO = AQUI.parent / "pasto"
sys.path.insert(0, str(AQUI))

import activos  # noqa: E402
import shell  # noqa: E402


def cargar_pasto():
    """Carga tools/pasto/build.py como módulo "pasto_build" (los dos paquetes tienen un build.py)."""
    sys.path.insert(1, str(PASTO))
    spec = importlib.util.spec_from_file_location("pasto_build", PASTO / "build.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main():
    cargar_pasto().main()
    urls = activos.publicar()
    cambiadas = shell.aplicar_todo(urls)
    print(f"shell: {cambiadas} de {len(shell.paginas_html())} páginas actualizadas")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Migrar las páginas a mano (una sola vez) y construir el sitio**

```bash
cd ~/dev/viverosterra-e1
python3 tools/site/migrar_shell.py | tail -1
python3 tools/site/build.py | tail -1
python3 tools/site/build.py | tail -1
git diff --quiet -- public/sitemap.xml && echo "sitemap sin cambios"
```

Expected, en orden: `78 páginas migradas`; `shell: 78 de 108 páginas actualizadas`; `shell: 0 de 108 páginas actualizadas` (el build es reproducible); `sitemap sin cambios`.

- [ ] **Step 5: Correr todas las pruebas (deben pasar)**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3
cd ~/dev/viverosterra-e1/tools/pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ~/dev/viverosterra-e1 && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `Ran 66 tests` + `OK`; `OK`; `ℹ pass 11` y `ℹ fail 0`.

- [ ] **Step 6: Revisión visual rápida antes del commit (3 páginas, 2 anchos)**

```bash
cd ~/dev/viverosterra-e1/public && python3 -m http.server 8765
```

Abre en el navegador `http://127.0.0.1:8765/`, `http://127.0.0.1:8765/blog/cuando-regar-pasto-san-agustin-tampico/` y `http://127.0.0.1:8765/pasto-sintetico/toscana-28/` a 375 px y a 1440 px. Esperado: un solo menú (el nuevo, color hueso) arriba, el cuerpo viejo igual que antes, un solo pie oscuro con "Av. Álvaro Obregón 209 Sur" y, a 375 px, la barra amarilla/blanca de WhatsApp abajo (no en la ficha de la tienda, que conserva su barra de compra). Detén el servidor con Ctrl+C. Si algo del cuerpo viejo se ve roto por el shell, corrígelo en `terra.css` (nunca en el cuerpo) y vuelve al Step 4.

- [ ] **Step 7: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public tools/site/build.py tools/site/tests/test_sitio.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): menú, pie y barra móvil únicos en las 108 páginas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(`public/.DS_Store` ya no está versionado desde la Tarea 0, así que `git add public` no lo incluye.)

---

### Task 16: Enlace roto, PNG inexistente y `noindex` del cuestionario

**Files:**
- Modify: `public/blog/tezontle-usos-jardin-tampico/index.html`, `public/blog/tierra-negra-costal-camion-tampico/index.html`, `public/cuestionario.html`
- Test: `tools/site/tests/test_enlaces.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_enlaces.py`:

```python
"""Enlaces internos, imágenes y assets locales existen; los redirects apuntan a páginas reales y sin cadenas."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
REDIRECTS = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
ORIGENES = {r["source"] for r in REDIRECTS}
SITIO = "https://www.viverosterra.com"
ATRIBUTO_RE = re.compile(r'\b(href|src|srcset|imagesrcset|content)="([^"]+)"')
IMAGEN_RE = re.compile(r"\.(png|jpe?g|webp|svg|gif)$", re.I)
SCRIPT_RE = re.compile(r"<script\b(?![^>]*ld\+json)[^>]*>.*?</script>", re.S)


def existe(ruta):
    ruta = unquote(ruta).rstrip("/") or "/"
    if ruta == "/" or ruta in ORIGENES or ruta.startswith("/api/"):
        return True
    archivo = PUBLIC / ruta.lstrip("/")
    return archivo.is_file() or archivo.with_suffix(".html").is_file() or (archivo / "index.html").is_file()


def referencias(html):
    """Rutas locales que la página enlaza o carga (sin scripts que arman HTML, con JSON-LD)."""
    html = SCRIPT_RE.sub("", html)
    for atributo, valor in ATRIBUTO_RE.findall(html):
        candidatos = [c.strip().split(" ")[0] for c in valor.split(",")] if atributo.endswith("srcset") else [valor]
        for candidato in candidatos:
            if candidato.startswith(SITIO):
                candidato = candidato[len(SITIO):] or "/"
            if not candidato.startswith("/") or candidato.startswith("//"):
                continue
            if atributo == "content" and not IMAGEN_RE.search(candidato):
                continue
            yield urlsplit(candidato).path
    for url in re.findall(r'"(https://www\.viverosterra\.com/[^"]+\.(?:png|jpe?g|webp))"', html):
        yield url[len(SITIO):]


class EnlacesTest(unittest.TestCase):
    def test_enlaces_y_recursos_locales_existen(self):
        rotos = {}
        for path in PUBLIC.rglob("*.html"):
            for ruta in referencias(path.read_text(encoding="utf-8")):
                if not existe(ruta):
                    rotos.setdefault(ruta, str(path.relative_to(PUBLIC)))
        self.assertEqual(rotos, {})

    def test_redirects_a_paginas_reales_sin_cadenas(self):
        for r in REDIRECTS:
            destino = r["destination"]
            with self.subTest(origen=r["source"]):
                self.assertNotIn(destino, ORIGENES)
                if destino.startswith("/"):
                    ruta = destino.split("#")[0].split("?")[0]
                    archivo = PUBLIC / ruta.strip("/")
                    self.assertTrue(ruta == "/" or archivo.is_file() or archivo.with_suffix(".html").is_file()
                                    or (archivo / "index.html").is_file(), destino)


class IndexacionTest(unittest.TestCase):
    def test_paginas_de_utilidad_con_noindex(self):
        for archivo in ("cuestionario.html", "gracias/index.html", "datos-envio/index.html"):
            with self.subTest(pagina=archivo):
                html = (PUBLIC / archivo).read_text(encoding="utf-8")
                self.assertIsNotNone(re.search(r'<meta name="robots" content="noindex, (?:no)?follow">', html))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_enlaces.py 2>&1 | grep -E "^- |^AssertionError: None|^Ran|FAILED"`
Expected: los dos rotos (`/blog/tierra-negra-tampico-guia` en el blog de tezontle y `/img/tierra-negra-jardin-tampico.png` en el de tierra negra), el `noindex` faltante del cuestionario y `FAILED (failures=2)`.

- [ ] **Step 3: Corregir los tres archivos**

```bash
cd ~/dev/viverosterra-e1
python3 - <<'EOF'
from pathlib import Path

CAMBIOS = (
    ("public/blog/tezontle-usos-jardin-tampico/index.html",
     '<a href="/blog/tierra-negra-tampico-guia" class="group',
     '<a href="/blog/tierra-negra-costal-camion-tampico" class="group'),
    ("public/blog/tierra-negra-costal-camion-tampico/index.html",
     '"image":"https://www.viverosterra.com/img/tierra-negra-jardin-tampico.png"',
     '"image":"https://www.viverosterra.com/img/tierra-negra-jardin-tampico.jpg"'),
    ("public/cuestionario.html",
     '  <meta name="robots" content="index, follow">',
     '  <meta name="robots" content="noindex, follow">'),
)
for ruta, viejo, nuevo in CAMBIOS:
    archivo = Path(ruta)
    texto = archivo.read_text(encoding="utf-8")
    assert texto.count(viejo) == 1, (ruta, texto.count(viejo))
    archivo.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    print("ok", ruta)
EOF
```

Expected: tres líneas `ok …`.

- [ ] **Step 4: Correr la prueba (debe pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 69 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/blog/tezontle-usos-jardin-tampico/index.html public/blog/tierra-negra-costal-camion-tampico/index.html public/cuestionario.html tools/site/tests/test_enlaces.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(seo): enlace roto de tezontle, imagen inexistente y noindex del cuestionario" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 17: Retirar la guía de palmas en PDF (decisión del dueño 2026-11-07)

**Files:**
- Modify: `public/palmas-mayoreo-proyectos/index.html` (sección `#lead`, formulario y script), `vercel.json`
- Delete: `public/pdf/guia-12-palmas-arquitectos.pdf`
- Test: `tools/site/tests/test_guia_palmas.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_guia_palmas.py`:

```python
"""La guía de palmas en PDF se retiró por decisión del dueño (2026-11-07): sin oferta, sin PDF y con 301."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC


class GuiaPalmasTest(unittest.TestCase):
    def test_oferta_y_pdf_retirados(self):
        html = (PUBLIC / "palmas-mayoreo-proyectos" / "index.html").read_text(encoding="utf-8")
        for viejo in ('id="lead"', "lead-cta", "lead-email", "Guía gratuita", "Descargar guía", "Lead Magnet"):
            with self.subTest(viejo=viejo):
                self.assertNotIn(viejo, html)
        self.assertIn("Sección 11 · Preguntas frecuentes", html)
        self.assertFalse((PUBLIC / "pdf" / "guia-12-palmas-arquitectos.pdf").exists())

    def test_ninguna_pagina_enlaza_la_guia(self):
        for path in PUBLIC.rglob("*.html"):
            with self.subTest(pagina=str(path.relative_to(PUBLIC))):
                self.assertNotIn("guia-12-palmas", path.read_text(encoding="utf-8"))

    def test_la_url_del_pdf_redirige_a_palmas(self):
        redirects = json.loads((PUBLIC.parent / "vercel.json").read_text(encoding="utf-8"))["redirects"]
        destinos = {r["source"]: (r["destination"], r["permanent"]) for r in redirects}
        self.assertEqual(destinos.get("/pdf/guia-12-palmas-arquitectos.pdf"), ("/palmas-tropicales-tampico", True))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_guia_palmas.py 2>&1 | tail -1`
Expected: `FAILED (failures=3)`.

- [ ] **Step 3: Quitar la sección, el script y el PDF; renumerar las secciones siguientes; redirigir la URL**

```bash
cd ~/dev/viverosterra-e1
python3 - <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, "tools/site")
from shell import fin_elemento  # noqa: E402

pagina = Path("public/palmas-mayoreo-proyectos/index.html")
html = pagina.read_text(encoding="utf-8")
comentario = "<!-- ============ LEAD MAGNET (DARK) ============ -->\n"
inicio = html.index(comentario)
seccion = html.index('<section class="py-20 bg-dark text-white" id="lead">', inicio)
html = html[:inicio] + html[fin_elemento(html, seccion):].lstrip("\n")
inicio = html.index("  // Lead Magnet → descarga PDF + notifica WhatsApp\n")
fin = html.index("  })();\n", inicio) + len("  })();\n")
html = html[:inicio] + html[fin:]
html = html.replace("Sección 12 · Preguntas frecuentes", "Sección 11 · Preguntas frecuentes", 1)
html = html.replace("Sección 13 · Cotiza tu proyecto", "Sección 12 · Cotiza tu proyecto", 1)
pagina.write_text(html, encoding="utf-8")
print("guía retirada")
EOF
git rm -q public/pdf/guia-12-palmas-arquitectos.pdf
python3 - <<'EOF'
import json
from pathlib import Path

p = Path("vercel.json")
cfg = json.loads(p.read_text(encoding="utf-8"))
cfg["redirects"].append({"source": "/pdf/guia-12-palmas-arquitectos.pdf", "destination": "/palmas-tropicales-tampico", "permanent": True})
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
python3 tools/site/build.py | tail -1
```

Expected: `guía retirada` y `shell: 0 de 108 páginas actualizadas`.

- [ ] **Step 4: Correr las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 72 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/palmas-mayoreo-proyectos/index.html vercel.json tools/site/tests/test_guia_palmas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(contenido): retirar la guía de palmas en PDF y redirigir su URL a palmas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 18: `robots.txt` (AdsBot sin bloqueos, CCBot permitido, bots de búsqueda de IA)

**Files:**
- Modify: `public/robots.txt`
- Test: `tools/site/tests/test_robots.py`

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_robots.py`:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

ROBOTS = paginas.PUBLIC / "robots.txt"
BOTS = ("OAI-SearchBot", "ChatGPT-User", "GPTBot", "Claude-SearchBot", "Claude-User", "ClaudeBot", "PerplexityBot",
        "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot")


def grupos(texto):
    """Bloques separados por líneas en blanco, sin comentarios."""
    bloques = [[ln for ln in b.splitlines() if ln and not ln.startswith("#")] for b in texto.split("\n\n")]
    return [b for b in bloques if b]


class RobotsTest(unittest.TestCase):
    def setUp(self):
        self.texto = ROBOTS.read_text(encoding="utf-8")

    def test_sin_bloqueos_ni_reglas_para_adsbot(self):
        self.assertNotIn("Disallow:", self.texto)
        self.assertNotIn("User-agent: AdsBot", self.texto)

    def test_bots_de_busqueda_e_ia_con_permiso_explicito(self):
        for bot in BOTS:
            grupo = next((g for g in grupos(self.texto) if f"User-agent: {bot}" in g), None)
            with self.subTest(bot=bot):
                self.assertIsNotNone(grupo)
                self.assertIn("Allow: /", grupo)

    def test_sitemap_declarado(self):
        self.assertIn("Sitemap: https://www.viverosterra.com/sitemap.xml", self.texto)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_robots.py 2>&1 | tail -1`
Expected: `FAILED (failures=2)` (hay `Disallow` de AdsBot y CCBot; faltan OAI-SearchBot, Claude-SearchBot, Claude-User, Perplexity-User y Applebot-Extended).

- [ ] **Step 3: Reemplazar `public/robots.txt` completo**

```text
# robots.txt de www.viverosterra.com
# Todo el sitio es público (precios y servicios). Las páginas de utilidad llevan noindex en su HTML.

User-agent: *
Allow: /

# Buscadores y asistentes de IA: citación en respuestas y conocimiento de la marca
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: ClaudeBot
User-agent: anthropic-ai
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Bingbot
User-agent: CCBot
Allow: /

# Google Ads (AdsBot) rastrea todo el sitio para revisar las landings de los anuncios.
# La exclusión de servicios en Google Shopping se hace en el feed y en Merchant Center, no aquí.

# Resumen para asistentes de IA: https://www.viverosterra.com/llms.txt
Sitemap: https://www.viverosterra.com/sitemap.xml
```

- [ ] **Step 4: Correr las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 75 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add public/robots.txt tools/site/tests/test_robots.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "fix(seo): robots sin bloqueos a AdsBot, CCBot permitido y bots de búsqueda de IA" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 19: Cabeceras en `vercel.json` (CSP en Report-Only, sin `X-XSS-Protection`, caché inmutable con hash)

**Files:**
- Modify: `vercel.json`
- Test: `tools/site/tests/test_vercel.py`

HSTS con `includeSubDomains; preload` y la CSP en enforce son de la Etapa 5 (spec §8.4 y §10).

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_vercel.py`:

```python
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import activos  # noqa: E402
import paginas  # noqa: E402

VERCEL = paginas.PUBLIC.parent / "vercel.json"
HASH = r"/(css|js)/(terra|legacy-fixes)\.([0-9a-f]+)\.(css|js)"
GENERAL_JS_CSS = r"/(.*)\.(js|css)"


class VercelTest(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(VERCEL.read_text(encoding="utf-8"))

    def cabeceras(self, fuente):
        return {h["key"]: h["value"] for r in self.cfg["headers"] if r["source"] == fuente for h in r["headers"]}

    def test_csp_en_report_only_y_sin_x_xss_protection(self):
        h = self.cabeceras("/(.*)")
        self.assertNotIn("X-XSS-Protection", h)
        self.assertNotIn("Content-Security-Policy", h)
        csp = h["Content-Security-Policy-Report-Only"]
        for directiva in ("default-src 'self'", "https://www.googletagmanager.com", "https://fonts.googleapis.com",
                          "https://formsubmit.co", "frame-ancestors 'none'", "object-src 'none'", "base-uri 'self'"):
            with self.subTest(directiva=directiva):
                self.assertIn(directiva, csp)

    def test_assets_con_hash_inmutables_y_despues_de_la_regla_general(self):
        fuentes = [r["source"] for r in self.cfg["headers"]]
        self.assertLess(fuentes.index(GENERAL_JS_CSS), fuentes.index(HASH))
        self.assertEqual(self.cabeceras(HASH)["Cache-Control"], "public, max-age=31536000, immutable")
        for url in activos.urls().values():
            with self.subTest(url=url):
                self.assertIsNotNone(re.fullmatch(HASH, url))



if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_vercel.py 2>&1 | tail -1`
Expected: `FAILED (failures=1, errors=1)`.

- [ ] **Step 3: Actualizar las cabeceras**

```bash
cd ~/dev/viverosterra-e1
python3 - <<'EOF'
import json
from pathlib import Path

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; "
       "img-src 'self' data: https://www.google-analytics.com https://*.google-analytics.com "
       "https://www.googletagmanager.com https://lh3.googleusercontent.com; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
       "https://www.googletagmanager.com https://formsubmit.co; form-action 'self' https://formsubmit.co; "
       "frame-ancestors 'none'; base-uri 'self'; object-src 'none'")
HASH = "/(css|js)/(terra|legacy-fixes)\\.([0-9a-f]+)\\.(css|js)"

p = Path("vercel.json")
cfg = json.loads(p.read_text(encoding="utf-8"))
general = next(r for r in cfg["headers"] if r["source"] == "/(.*)")
general["headers"] = [h for h in general["headers"] if h["key"] != "X-XSS-Protection"]
general["headers"].append({"key": "Content-Security-Policy-Report-Only", "value": CSP})
i = next(i for i, r in enumerate(cfg["headers"]) if r["source"] == "/(.*)\\.(js|css)")
cfg["headers"].insert(i + 1, {"source": HASH, "headers": [
    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]})
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("vercel.json actualizado")
EOF
```

Expected: `vercel.json actualizado`.

- [ ] **Step 4: Correr las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 77 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git add vercel.json tools/site/tests/test_vercel.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(seguridad): CSP en Report-Only, sin X-XSS-Protection y caché inmutable de assets con hash" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 20: Prueba de reglas permanentes del dueño (palabras prohibidas)

**Files:**
- Test: `tools/site/tests/test_reglas.py`

Esta prueba cubre las reglas que ya cumple el sitio al cerrar 1a (Etapa 0 limpió pádel, canchas y el proveedor). Las reglas de datos que hoy fallan ("pagas cuando", "sobre pedido", "líder", promesas viejas, "209" sin "Sur", framboyán, mayoreo 200 m²…) llegan en 1b con `test_consistencia.py`, junto con su corrección.

- [ ] **Step 1: Escribir la prueba**

`tools/site/tests/test_reglas.py`:

```python
"""Reglas permanentes del dueño sobre todo lo publicado en public/: texto visible, JSON-LD, atributos legibles
(content, alt, title, aria-label, placeholder) y mensajes de WhatsApp prellenados. Los .js, .txt y .xml se revisan
completos para las reglas de marcas y pagos."""
import html as html_mod
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

PUBLIC = paginas.PUBLIC
PERMITIDAS = ('anuncian "envío gratis"',)  # el hub explica que "envío gratis" de otros ya viene en el precio
PROHIBIDAS = (
    ("Oasis", r"\bOasis\b"),
    ("marca de proveedor de pasto sintético", r"\bPasto\s?Plus\b"),
    ("nombre del proveedor de la terminal", r"(?<![-.\w])clip(?![-\w:(])"),
    ("MSI", r"\bMSI\b"),
    ("sin intereses", r"\bsin intereses\b"),
    ("0 % en pagos", r"(?<![\d.,])0\s?%"),
    ("muestras gratis o físicas", r"(?<!no ofrecemos )(?<!no enviamos )(?<!sin )\bmuestras?\s+(?:gratis|f[ií]sicas?)\b"),
    ("envío gratis", r"(?:env[ií]os?|flete)\W+(?:\w+\W+){0,3}gratis\b|\bgratis\W+(?:\w+\W+){0,3}(?:env[ií]os?|flete)"),
)
DEPORTES_RE = re.compile(r"p[aá]del|canchas?", re.I)


def textos_publicos(html):
    ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    atributos = " ".join(re.findall(r'\b(?:content|alt|title|aria-label|placeholder)="([^"]*)"', html))
    mensajes = " ".join(unquote(t) for t in re.findall(r'https://wa\.me/\d+\?text=([^"\'&\s<]*)', html))
    cuerpo = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", html, flags=re.S | re.I)
    cuerpo = re.sub(r"<!--.*?-->", " ", cuerpo, flags=re.S)
    cuerpo = re.sub(r"<[^>]+>", " ", cuerpo)
    texto = re.sub(r"\s+", " ", html_mod.unescape(" ".join([cuerpo, ld, atributos, mensajes])))
    for permitida in PERMITIDAS:
        texto = texto.replace(permitida, "")
    return texto


def publicados():
    for path in sorted(PUBLIC.rglob("*.html")):
        yield path, textos_publicos(path.read_text(encoding="utf-8"))
    for ext in ("js", "txt", "xml"):
        for path in sorted(PUBLIC.rglob(f"*.{ext}")):
            if "/tests/" not in path.as_posix():
                yield path, path.read_text(encoding="utf-8")


class ReglasDelDuenoTest(unittest.TestCase):
    def test_sin_palabras_prohibidas(self):
        hallazgos = []
        for path, texto in publicados():
            for regla, patron in PROHIBIDAS:
                for m in re.finditer(patron, texto, re.I):
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · {regla} · …{texto[max(0, m.start() - 40):m.end() + 40]}…")
        self.assertEqual(hallazgos, [])

    def test_sin_padel_ni_canchas_en_pasto_sintetico(self):
        hallazgos = []
        for path, texto in publicados():
            for m in DEPORTES_RE.finditer(texto):
                ventana = texto[max(0, m.start() - 150):m.end() + 150].lower()
                if re.search(r"sint[eé]tic", ventana) and "natural" not in ventana:
                    hallazgos.append(f"{path.relative_to(PUBLIC)} · …{ventana}…")
        self.assertEqual(hallazgos, [])

    def test_las_reglas_detectan_lo_que_deben(self):
        texto = textos_publicos(
            '<p>Pasto Oasis</p><p>Paga con Clip</p><p>12 MSI</p><p>meses sin intereses</p><p>0% de interés</p>'
            '<p>Envío gratis a todo México</p><p>Pide tus muestras gratis</p>'
            '<p>Ahorra 40% de agua; total 100%; aumento de +10.5%</p><p>clip-path</p>'
        )
        detectadas = {regla for regla, patron in PROHIBIDAS if re.search(patron, texto, re.I)}
        self.assertEqual(detectadas, {regla for regla, _ in PROHIBIDAS} - {"marca de proveedor de pasto sintético"})
        self.assertIsNone(re.search(PROHIBIDAS[5][1], textos_publicos("<p>40% de agua, 100% natural, +10.5%</p>")))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Comprobar que la prueba detecta violaciones (debe fallar con un caso plantado)**

```bash
cd ~/dev/viverosterra-e1
cp public/precios/index.html /tmp/precios-respaldo.html
python3 -c "
from pathlib import Path
p = Path('public/precios/index.html')
p.write_text(p.read_text(encoding='utf-8').replace('</main>', '<p>12 MSI con envío gratis</p></main>', 1), encoding='utf-8')"
cd tools/site && python3 -m unittest tests/test_reglas.py 2>&1 | grep -E "MSI|envío gratis|FAILED"
cp /tmp/precios-respaldo.html ~/dev/viverosterra-e1/public/precios/index.html
```

Expected: dos hallazgos (`MSI` y `envío gratis`) en `precios/index.html` y `FAILED (failures=1)`; después se restaura el archivo.

- [ ] **Step 3: Correr las pruebas sobre el sitio real (deben pasar)**

Run: `cd ~/dev/viverosterra-e1 && git diff --quiet -- public/precios/index.html && echo restaurado; cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `restaurado`; `Ran 80 tests` y `OK`. Si aparece un hallazgo real, corrige el texto en su fuente (generador o página) siguiendo las reglas del dueño y vuelve a correr.

- [ ] **Step 4: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/tests/test_reglas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(site): reglas permanentes del dueño sobre todo lo publicado" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 21: Limpieza del repo (copias viejas de la raíz, scripts obsoletos, JS sin uso)

**Files:**
- Delete: `index.html`, `catalogo.html`, `catalogo/`, `cuestionario.html`, `cuestionario/`, las 23 imágenes y logos sueltos de la raíz, `scripts/`, `src/`, `tailwind.config.js`, `public/js/nav-scroll.js`
- Test: `tools/site/tests/test_limpieza.py`

Nada de esto se sirve (`outputDirectory: public`) y `nav-scroll.js` solo actuaba sobre el `terra-nav` retirado.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_limpieza.py`:

```python
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


class LimpiezaTest(unittest.TestCase):
    def test_raiz_sin_copias_viejas(self):
        for nombre in ("index.html", "catalogo.html", "catalogo", "cuestionario.html", "cuestionario", "scripts", "src",
                       "tailwind.config.js"):
            with self.subTest(nombre=nombre):
                self.assertFalse((RAIZ / nombre).exists())
        sueltas = sorted(p.name for ext in ("png", "jpg", "webp", "svg") for p in RAIZ.glob(f"*.{ext}"))
        self.assertEqual(sueltas, [])

    def test_js_sin_uso_retirado(self):
        self.assertFalse((RAIZ / "public" / "js" / "nav-scroll.js").exists())

    def test_ds_store_y_pycache_fuera_de_git(self):
        versionados = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
        self.assertNotIn(".DS_Store", versionados)
        self.assertNotIn("__pycache__", versionados)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_limpieza.py 2>&1 | tail -1`
Expected: `FAILED (failures=2)` (raíz y `nav-scroll.js`; `.DS_Store` y `__pycache__` ya quedaron fuera en la Tarea 0).

- [ ] **Step 3: Borrar**

```bash
cd ~/dev/viverosterra-e1
git rm -r -q index.html catalogo.html catalogo cuestionario.html cuestionario scripts src tailwind.config.js public/js/nav-scroll.js $(git ls-files -- '*.png' '*.jpg' '*.webp' '*.svg' | grep -v /)
git status --short | grep -c "^D"
```

Expected: `33` archivos borrados (9 de las 8 rutas de la raíz, 23 imágenes y logos sueltos y `nav-scroll.js`; si el número difiere, revisa que ninguno esté bajo `public/`, `tools/` o `docs/`).

- [ ] **Step 4: Correr todas las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 83 tests` y `OK`.

- [ ] **Step 5: Commit**

```bash
cd ~/dev/viverosterra-e1
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "chore: borrar copias viejas de la raíz, scripts obsoletos y nav-scroll.js" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git add tools/site/tests/test_limpieza.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(site): el repo no vuelve a acumular copias viejas" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 22: Pruebas en navegador (consola, axe del shell, menú, barra, GA4, desbordamiento)

**Files:**
- Create: `tools/site/servidor.py`, `tools/site/vendor/axe.min.js`
- Test: `tools/site/tests/test_navegador.py`

- [ ] **Step 1: Escribir la prueba (falla: falta `servidor.py`)**

`tools/site/tests/test_navegador.py`:

```python
"""Pruebas en navegador con Playwright: consola limpia en las 108 páginas, accesibilidad del shell con axe, menú,
barra móvil, eventos de GA4 y shell sin desbordar. Se saltan si Playwright no está instalado (en CI sí lo está)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import servidor  # noqa: E402
import shell  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

AXE = Path(__file__).resolve().parents[1] / "vendor" / "axe.min.js"
REPRESENTATIVAS = ("/", "/pasto-en-rollo-tampico/", "/pasto-sintetico/", "/pasto-sintetico/toscana-28/",
                   "/diseno-jardines-tampico/", "/plantas-palmas-arboles-tampico/", "/catalogo.html", "/blog/",
                   "/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/", "/jardineria-altamira/", "/gracias/")
AXE_SHELL = """async () => {
  const incluir = ['.vt-head', '.vt-foot', '.vt-bar'].filter((s) => document.querySelector(s)).map((s) => [s]);
  const r = await axe.run({ include: incluir }, { resultTypes: ['violations'] });
  return r.violations.filter((v) => ['serious', 'critical'].includes(v.impact))
    .map((v) => v.id + ': ' + v.nodes.map((n) => n.target.join(' ')).join(', '));
}"""
BORDE_DERECHO = """() => Math.max(...Array.from(document.querySelectorAll('.vt-head__bar, .vt-foot, [data-vt-bar]'))
  .map((e) => e.getBoundingClientRect().right)) - document.documentElement.clientWidth"""


@unittest.skipIf(sync_playwright is None, "Playwright no está instalado: python3 -m pip install playwright==1.48.0")
class NavegadorTest(unittest.TestCase):
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

        def enrutar(route):
            url = route.request.url
            if url.startswith(base) and "/api/" not in url:
                route.continue_()
            else:
                route.abort()

        contexto.route("**/*", enrutar)
        return contexto.new_page()

    def test_consola_limpia_en_todas_las_paginas(self):
        errores = []
        page = self.pagina()
        page.on("pageerror", lambda error: errores.append(f"{page.url} · pageerror · {error}"))
        page.on("console", lambda msg: errores.append(f"{page.url} · consola · {msg.text}")
                if msg.type == "error" and not msg.text.startswith("Failed to load resource") else None)
        page.on("response", lambda r: errores.append(f"{r.url} · HTTP {r.status}") if r.status >= 400 else None)
        for path in shell.paginas_html():
            page.goto(self.base + servidor.url_de(path), wait_until="load")
        self.assertEqual(errores, [])

    def test_shell_sin_violaciones_serias_de_axe(self):
        script = AXE.read_text(encoding="utf-8")
        for ancho in (375, 1440):
            page = self.pagina(ancho)
            for ruta in REPRESENTATIVAS:
                page.goto(self.base + ruta, wait_until="load")
                page.add_script_tag(content=script)
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertEqual(page.evaluate(AXE_SHELL), [])

    def test_menu_movil_y_barra(self):
        page = self.pagina(375, 812)
        page.goto(self.base + "/blog/cuando-regar-pasto-san-agustin-tampico/", wait_until="load")
        self.assertTrue(page.locator("#vt-mmenu").is_hidden())
        page.click(".vt-burger")
        self.assertTrue(page.locator("#vt-mmenu").is_visible())
        self.assertEqual(page.get_attribute(".vt-burger", "aria-expanded"), "true")
        self.assertTrue(page.locator("[data-vt-bar]").is_visible())

    def test_panel_de_jardin_en_escritorio(self):
        page = self.pagina(1440)
        page.goto(self.base + "/", wait_until="load")
        boton = page.locator('.vt-nav button[aria-controls="vt-panel-jardin"]')
        boton.click()
        self.assertEqual(boton.get_attribute("aria-expanded"), "true")
        self.assertTrue(page.locator("#vt-panel-jardin").is_visible())
        page.keyboard.press("Escape")
        self.assertEqual(boton.get_attribute("aria-expanded"), "false")

    def test_eventos_de_ga4_y_firma(self):
        page = self.pagina(1440)
        page.goto(self.base + "/pasto-en-rollo-tampico/", wait_until="load")
        page.click(".vt-head__cta")
        page.click('.vt-foot a[href^="tel:"]')
        eventos = page.evaluate(
            "() => Array.from(window.dataLayer).map((a) => Array.from(a)).filter((a) => a[0] === 'event')")
        self.assertIn(["event", "generate_lead", {"method": "whatsapp", "cta_id": "servicio-pasto:header",
                                                  "service": "pasto-natural"}], eventos)
        self.assertIn(["event", "click_to_call", {"cta_id": "servicio-pasto:footer"}], eventos)
        self.assertEqual(page.get_attribute(".vt-head__cta", "href").count("viverosterra.com"), 1)

    def test_shell_sin_desbordar(self):
        for ancho in (320, 375, 768, 1440):
            page = self.pagina(ancho)
            for ruta in REPRESENTATIVAS:
                page.goto(self.base + ruta, wait_until="load")
                with self.subTest(ruta=ruta, ancho=ancho):
                    self.assertLessEqual(page.evaluate(BORDE_DERECHO), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_navegador.py 2>&1 | tail -3`
Expected: `ModuleNotFoundError: No module named 'servidor'` y `FAILED (errors=1)`.

- [ ] **Step 3: Crear `tools/site/servidor.py`**

```python
"""Servidor HTTP local de public/ (127.0.0.1, puerto libre) para las pruebas de navegador y las capturas."""
import functools
import http.server
import threading

import paginas


class _Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def iniciar(public=paginas.PUBLIC):
    """Arranca el servidor en un hilo; devuelve (url_base, servidor). Al terminar: shutdown() y server_close()."""
    manejador = functools.partial(_Silencioso, directory=str(public))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{servidor.server_address[1]}", servidor


def url_de(path, public=paginas.PUBLIC):
    """URL local de un archivo de public/ (las carpetas con index.html terminan en /)."""
    rel = path.relative_to(public).as_posix()
    return "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
```

- [ ] **Step 4: Versionar axe-core 4.10.2**

```bash
cd ~/dev/viverosterra-e1
mkdir -p tools/site/vendor
curl -sSfL -o tools/site/vendor/axe.min.js https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js
shasum -a 256 tools/site/vendor/axe.min.js
head -c 16 tools/site/vendor/axe.min.js; echo
```

Expected: `b511cd9dec01c76f4b2ad1723b66b6db37d4c2eb4ed199076e1829d9ee7b75e3  tools/site/vendor/axe.min.js` y `/*! axe v4.10.2`.

- [ ] **Step 5: Correr las pruebas de navegador (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_navegador.py -v 2>&1 | tail -10`
Expected: 6 pruebas `ok` y `OK` (tarda 1–3 minutos). Sin Playwright: `OK (skipped=6)`; en ese caso estas pruebas se validan en CI (Tarea 24) antes del merge.

Si falla:
- `test_consola_limpia…` con un `pageerror`: busca en esa página el script que usa un elemento retirado y ponle guarda (`if (el) …`) en la página; vuelve a correr `python3 tools/site/build.py` y las pruebas.
- `test_shell_sin_violaciones…`: corrige en `terra.css` o en `partials.py` (nunca en el cuerpo de la página).
- `test_shell_sin_desbordar` a 320 px: reduce en `terra.css` el ancho del logo o el padding del CTA dentro de `@media (max-width:359px)`.

- [ ] **Step 6: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/servidor.py tools/site/vendor/axe.min.js tools/site/tests/test_navegador.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "test(site): consola, axe del shell, menú, barra móvil y eventos GA4 en navegador" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 23: Script de capturas para la verificación

**Files:**
- Create: `tools/site/capturas.py`

- [ ] **Step 1: Crear `tools/site/capturas.py`**

```python
"""Capturas de verificación de la Etapa 1: 10 páginas a 320, 375 y 1440 px (página completa) y reporte de
desbordamiento horizontal. El desbordamiento del cuerpo viejo se anota para la Etapa 2; el del shell no se acepta.

Uso: python3 tools/site/capturas.py <carpeta-de-salida>
Requiere Playwright: python3 -m pip install playwright==1.48.0 && python3 -m playwright install chromium
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import servidor  # noqa: E402

PAGINAS = ("/", "/pasto-en-rollo-tampico/", "/pasto-sintetico/", "/pasto-sintetico/toscana-28/",
           "/diseno-jardines-tampico/", "/plantas-palmas-arboles-tampico/", "/catalogo.html", "/blog/",
           "/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/")
ANCHOS = (320, 375, 1440)


def nombre_archivo(ruta, ancho):
    limpio = ruta.strip("/").replace("/", "_").replace(".html", "") or "inicio"
    return f"{limpio}-{ancho}.png"


def main(salida):
    from playwright.sync_api import sync_playwright

    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    base, srv = servidor.iniciar()
    desbordes = []
    try:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            for ancho in ANCHOS:
                contexto = navegador.new_context(viewport={"width": ancho, "height": 900})
                contexto.route("**/*", lambda route: route.continue_()
                               if route.request.url.startswith(base) and "/api/" not in route.request.url
                               else route.abort())
                page = contexto.new_page()
                for ruta in PAGINAS:
                    page.goto(base + ruta, wait_until="load")
                    page.screenshot(path=str(salida / nombre_archivo(ruta, ancho)), full_page=True)
                    sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    if sobra > 1:
                        desbordes.append(f"{ruta} a {ancho}px: {sobra}px de más")
                contexto.close()
            navegador.close()
    finally:
        srv.shutdown()
        srv.server_close()
    print(f"{len(PAGINAS) * len(ANCHOS)} capturas en {salida}")
    print("desbordamiento horizontal:" if desbordes else "sin desbordamiento horizontal")
    for linea in desbordes:
        print(" -", linea)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 tools/site/capturas.py <carpeta-de-salida>")
    main(sys.argv[1])
```

- [ ] **Step 2: Probarlo**

Run: `cd ~/dev/viverosterra-e1 && python3 tools/site/capturas.py /tmp/vt-e1a-capturas | head -3 && ls /tmp/vt-e1a-capturas | wc -l`
Expected: `30 capturas en /tmp/vt-e1a-capturas`, la línea de desbordamiento (con la lista de páginas si las hay) y `30`. (Sin Playwright: `ModuleNotFoundError: No module named 'playwright'`; instálalo como en la Tarea 0.)

- [ ] **Step 3: Commit**

```bash
cd ~/dev/viverosterra-e1
git add tools/site/capturas.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "feat(site): capturas a 320, 375 y 1440 con reporte de desbordamiento" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 24: CI en GitHub Actions

**Files:**
- Create: `.github/workflows/sitio.yml`
- Test: `tools/site/tests/test_ci.py`

El repo no tiene `package.json` y no se le agrega: Node solo corre `node --test`. Pillow se instala solo porque las pruebas de `tools/servicios` importan `hero.py`.

- [ ] **Step 1: Escribir la prueba que falla**

`tools/site/tests/test_ci.py`:

```python
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[3] / ".github" / "workflows" / "sitio.yml"


class CiTest(unittest.TestCase):
    def test_workflow_con_build_reproducible_y_todas_las_pruebas(self):
        yml = WORKFLOW.read_text(encoding="utf-8")
        for paso in ("python tools/site/build.py", "git diff --exit-code -- public",
                     'test -z "$(git status --porcelain -- public)"', "playwright install --with-deps chromium",
                     "python -m unittest discover -s tests -v", "python -m unittest discover -s tests -t .",
                     "python -m unittest discover -s tests -t tests", "node --test public/js/tests/*.test.js"):
            with self.subTest(paso=paso):
                self.assertIn(paso, yml)
        self.assertNotIn("npm ", yml)
        self.assertNotIn("package.json", yml)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Correr la prueba (debe fallar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_ci.py 2>&1 | tail -1`
Expected: `FAILED (errors=1)` (`FileNotFoundError`).

- [ ] **Step 3: Crear `.github/workflows/sitio.yml`**

```yaml
name: sitio

on:
  push:
  pull_request:

jobs:
  pruebas:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: Dependencias de prueba (Playwright; Pillow para tools/servicios)
        run: |
          python -m pip install --upgrade pip
          python -m pip install playwright==1.48.0 pillow==10.4.0
          python -m playwright install --with-deps chromium

      - name: El build reproduce public/ sin cambios
        run: |
          python tools/site/build.py
          git status --porcelain -- public
          git diff --exit-code -- public
          test -z "$(git status --porcelain -- public)"

      - name: Pruebas del sitio (incluye navegador)
        working-directory: tools/site
        run: python -m unittest discover -s tests -v

      - name: Pruebas del generador de pasto
        working-directory: tools/pasto
        run: python -m unittest discover -s tests -t .

      - name: Pruebas de servicios
        working-directory: tools/servicios
        run: python -m unittest discover -s tests -t tests

      - name: Pruebas de JS
        run: node --test public/js/tests/*.test.js
```

- [ ] **Step 4: Correr las pruebas (deben pasar)**

Run: `cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest discover -s tests 2>&1 | tail -3`
Expected: `Ran 90 tests` y `OK` (o `OK (skipped=6)` sin Playwright local).

- [ ] **Step 5: Commit y primera corrida de CI en la rama**

```bash
cd ~/dev/viverosterra-e1
git add .github/workflows/sitio.yml tools/site/tests/test_ci.py
git -c user.name=viverosterra -c user.email=viverosterra@gmail.com commit -m "ci: build reproducible y todas las pruebas del sitio en cada push y PR" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -u origin feat/etapa-1
gh run watch --exit-status $(gh run list --branch feat/etapa-1 --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: la corrida termina en verde (`✓ pruebas`). Si falla el paso del build reproducible, corre `python3 tools/site/build.py` local, revisa `git diff` y haz commit de lo que falte.

---

### Task 25: Verificación final, puertas de revisión, merge y producción

**Files:** ninguno nuevo (correcciones que pidan los revisores).

- [ ] **Step 1: Todas las pruebas y build reproducible**

```bash
cd ~/dev/viverosterra-e1
python3 tools/site/build.py | tail -1
git status --porcelain
cd tools/site && python3 -m unittest discover -s tests 2>&1 | tail -1
cd ../pasto && python3 -m unittest discover -s tests -t . 2>&1 | tail -1
cd ../servicios && python3 -m unittest discover -s tests -t tests 2>&1 | tail -1
cd ../.. && node --test public/js/tests/*.test.js 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `shell: 0 de 108 páginas actualizadas`; `git status` vacío; `OK` tres veces; `ℹ pass 11` y `ℹ fail 0`.

- [ ] **Step 2: Grep de palabras prohibidas (respaldo manual de `test_reglas.py`)**

```bash
cd ~/dev/viverosterra-e1
grep -rniE "oasis|pasto ?plus|\bMSI\b|sin intereses|p[aá]del" public --include='*.html' --include='*.js' --include='*.txt' --include='*.xml' | wc -l
grep -rnoiE "(^|[^-.a-z])clip([^-a-z:(]|$)" public --include='*.html' --include='*.js' --include='*.txt' --include='*.xml' | wc -l
```

Expected: `0` y `0`.

- [ ] **Step 3: Consola sin errores en las 108 páginas y capturas**

```bash
cd ~/dev/viverosterra-e1/tools/site && python3 -m unittest tests/test_navegador.py -v 2>&1 | tail -3
cd ~/dev/viverosterra-e1 && python3 tools/site/capturas.py /tmp/vt-e1a-capturas
```

Expected: `OK` (6 pruebas, sin `skipped`); `30 capturas …`. Revisa a mano las 30 capturas: un solo menú y un solo pie, "209 Sur" en el pie, barra móvil a 320/375 (no en la tienda ni en el catálogo), nada del cuerpo viejo tapado por el header pegajoso. Anota en el resumen del PR las páginas que desbordan por su cuerpo viejo (se corrigen en la Etapa 2, J03); el shell no puede desbordar (lo garantiza `test_shell_sin_desbordar`).

- [ ] **Step 4: Abrir el PR con resumen y capturas**

```bash
cd ~/dev/viverosterra-e1
gh pr create --base main --head feat/etapa-1 --title "Etapa 1a · Fundaciones: shell único, medición y CI" --body "$(cat <<'EOF'
## Qué cambia
- `tools/site/`: fuente única de datos, contexto por ruta, parciales, aplicador del shell, migración única y build del sitio.
- Las 108 páginas tienen un solo menú (6 entradas + "Cotizar por WhatsApp"), un solo pie (209 Sur, promesa única, REPSE, 4.6 en Google) y barra fija móvil de WhatsApp; los cuerpos siguen iguales hasta la Etapa 2.
- `terra.css` (tokens del híbrido, solo selectores `.vt-`), fuentes Archivo y Fraunces autoalojadas, `legacy-fixes.css` con las 49 utilidades que faltaban.
- `terra.js`: `generate_lead` y `click_to_call` con `data-cta` en todas las páginas; firma "Vengo de viverosterra.com".
- robots (AdsBot sin bloqueos, CCBot y bots de búsqueda de IA), borrador retirado, enlace roto, guía de palmas retirada, `noindex` del cuestionario, CSP en Report-Only, caché inmutable con hash, limpieza del repo, CI.

## Verificación
- [ ] CI en verde (build reproducible + 4 suites + navegador)
- [ ] Capturas a 320/375/1440 revisadas (ver comentario con las imágenes)
- [ ] Puertas: diseño, SEO/AEO, CRO, cumplimiento/QA
- [ ] Vista previa de Vercel aprobada por el dueño

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
gh pr view --json url --jq .url
```

Expected: la URL del PR. Vercel comenta la URL de la vista previa en el PR; anótala para los revisores.

- [ ] **Step 5: Puertas de revisión en paralelo (spec §11)**

Lanza los cuatro revisores a la vez (una sola respuesta con cuatro llamadas a agentes). A cada uno dale: el diff (`git diff main...feat/etapa-1 --stat` y los archivos clave), la URL de la vista previa, la carpeta `/tmp/vt-e1a-capturas`, el spec (`docs/superpowers/specs/2026-11-07-mejora-integral-sitio-design.md` §3.1, §4, §5.3, §6.2, §8.3, §9, §10 Etapa 1, §11) y la instrucción de clasificar cada hallazgo como crítico, alto, medio o bajo, con archivo y línea.

1. **Diseño** (`design:design-critique` + `a11y-architect`): fidelidad al híbrido (tokens, Archivo, etiqueta y cuadro de datos del pie, radios), jerarquía del menú y del pie, foco visible ≥ 3:1, objetivos táctiles ≥ 44 px en CTA y pie, menú móvil y paneles con teclado, que el shell no rompa ningún cuerpo viejo en las 30 capturas.
2. **SEO/AEO** (`seo-specialist` con las skills `seo-audit`, `ai-seo`, `schema-markup`): `robots.txt`, head (sin meta heredadas, un gtag, canonical intacto), `noindex` del cuestionario, 301 del borrador y del PDF, enlaces del menú y del pie (todas las money pages a ≤ 1 clic, 6 zonas enlazadas desde el pie), que la migración no haya tocado títulos, descripciones, canonical ni JSON-LD de ninguna página (`git diff main...feat/etapa-1 -- public | grep -E '^[-+].*(<title>|name="description"|rel="canonical"|ld\+json)'` debe salir vacío salvo el PNG corregido).
3. **CRO** (`general-purpose` con la skill `page-cro`): CTA del menú y de la barra móvil (texto, mensaje prellenado por servicio, firma), la barra no tapa CTAs del cuerpo, `data-cta` en cada enlace de WhatsApp y teléfono, eventos `generate_lead` / `click_to_call` con `cta_id` y `service`, promesa única visible en el pie.
4. **Cumplimiento y QA** (`code-reviewer` + `python-reviewer` + `e2e-runner`): reglas del dueño, datos oficiales en `datos.py`, calidad y pruebas de `tools/site/`, consola, CI, CSP Report-Only sin romper nada, que no se versionó `.DS_Store`.

Corrige en la rama todo hallazgo crítico o alto (con su prueba, commit y nueva corrida de CI) y vuelve a pedir revisión al revisor que lo levantó; los medios se corrigen o se anotan en el PR con su motivo.

- [ ] **Step 6: Aprobación del dueño**

Comparte la URL de la vista previa de Vercel y la carpeta de capturas con el dueño. No hagas merge sin su "sí" explícito.

- [ ] **Step 7: Merge a `main` y despliegue a producción**

```bash
cd ~/dev/viverosterra
git checkout main
git pull --ff-only
git merge --no-ff feat/etapa-1 -m "feat: etapa 1a, shell único, medición y CI" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push origin main
gh run watch --exit-status $(gh run list --branch main --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: CI en verde en `main`; Vercel despliega producción desde `main` (revisa en Vercel > Deployments que el último esté `Ready`).

- [ ] **Step 8: El dueño cambia el apex a 308 (Vercel > Domains)**

En Vercel > Project > Settings > Domains, el dominio `viverosterra.com` debe redirigir a `www.viverosterra.com` con **308 Permanent Redirect** (hoy 307). Lo hace el dueño (es su cuenta). Después:

Run: `curl -sI https://viverosterra.com/ | grep -iE "^HTTP|^location"`
Expected: `HTTP/2 308` y `location: https://www.viverosterra.com/`.

- [ ] **Step 9: Verificación en vivo**

```bash
W=https://www.viverosterra.com
curl -s $W/ | grep -c '<header class="vt-head"'
curl -s $W/blog/cuando-regar-pasto-san-agustin-tampico | grep -c "Av. Álvaro Obregón 209 Sur"
curl -sI $W/ | grep -iE "content-security-policy-report-only|x-xss-protection" | cut -c1-60
CSS=$(curl -s $W/ | grep -oE '/css/terra\.[0-9a-f]{10}\.css' | head -1); curl -sI $W$CSS | grep -i "cache-control"
curl -s $W/robots.txt | grep -cE "^Disallow"
curl -sI $W/preview-mapa-cobertura | grep -iE "^HTTP|^location"
curl -sI $W/pdf/guia-12-palmas-arquitectos.pdf | grep -iE "^HTTP|^location"
curl -s $W/cuestionario | grep -o '<meta name="robots" content="[^"]*">'
```

Expected, en orden: `1`; `1` o más; solo la línea `content-security-policy-report-only: default-src 'self'; …` (sin `x-xss-protection`); `cache-control: public, max-age=31536000, immutable`; `0`; `HTTP/2 308` + `location: /`; `HTTP/2 308` + `location: /palmas-tropicales-tampico`; `<meta name="robots" content="noindex, follow">`.

Abre en Chrome (escritorio y emulación de iPhone) la home, `/pasto-en-rollo-tampico`, `/pasto-sintetico/toscana-28`, un post del blog y `/catalogo`: consola sin errores (los avisos `[Report Only]` de CSP se anotan para la Etapa 5, no bloquean), menú, paneles, menú móvil y barra funcionando.

- [ ] **Step 10: Medición en GA4 (con el dueño)**

1. En `https://tagassistant.google.com` conecta `https://www.viverosterra.com`, haz clic en el CTA del menú de la home, en el teléfono del pie de `/pasto-en-rollo-tampico`, en la barra móvil de un post (emulación móvil) y en "Enviar cotización por WhatsApp" de la tienda.
2. En GA4 > Admin > DebugView confirma `generate_lead` con `method=whatsapp`, `cta_id` (`home:header`, `blog:barra`…) y `service`, `click_to_call` con `cta_id`, y los eventos propios de la tienda.
3. En GA4 > Admin > Events marca `generate_lead` como evento clave.
4. Anota la fecha de hoy como inicio de la línea base de 2 semanas (spec §1) en el PR.

- [ ] **Step 11: Si algo crítico falla en vivo**

Vercel > Deployments > el despliegue anterior > "Instant Rollback", o `git revert -m 1 <sha-del-merge> && git push origin main`. Corrige en una rama nueva desde `main` y repite desde el Step 1.

- [ ] **Step 12: Preparar 1b**

```bash
cd ~/dev/viverosterra-e1
git fetch origin
git checkout -b feat/etapa-1b origin/main
git log --oneline -1
```

Expected: el merge de 1a. Sigue con `docs/superpowers/plans/2026-11-07-etapa-1b-fundaciones-datos.md`.
