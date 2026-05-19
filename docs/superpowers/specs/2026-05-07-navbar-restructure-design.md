# Navbar Restructure (B+ Pattern) — Design Spec

**Goal:** Reorganizar el dropdown "Servicios" del navbar de viverosterra.com para incluir las 17 páginas relevantes agrupadas en 4 secciones temáticas, resolviendo el bug donde "Piedras y Mármol" linkeaba a una sola página específica.

**Architecture:** Mantener el patrón actual del `terra-nav__dropdown` pero ampliar a 720px de ancho con 2 columnas, cada una con 2 secciones temáticas separadas por headers. Reutilizar la lógica JS existente. Mobile drawer mantiene el mismo patrón con sub-toggles colapsables.

**Tech Stack:** HTML/CSS puro inline en cada archivo HTML. Sin nuevas dependencias.

---

## Estructura

### Layout escritorio (≥901px)

Dropdown de 720px ancho con grid de 2 columnas. Cada columna contiene 2 secciones agrupadas con header.

```
COLUMNA 1 (izquierda)        COLUMNA 2 (derecha)
─ SERVICIOS DE JARDINERÍA ─  ─ MATERIALES ─
  Pasto en Rollo               Tierra Negra
  Pasto Sintético              Tezontle Rojo
  Diseño de Jardines           Mármol Blanco
  Mantenimiento                Piedra de Río
  Sistema de Riego

─ PLANTAS Y PALMAS ─         ─ POR ZONA · B2B ─
  Catálogo de Plantas          Vivero en Tampico
  Palmas Tropicales            Jardinería Madero
  Árboles para Banqueta        Jardinería Altamira
  Plantas de Interior          Mayoreo Constructoras
```

### Layout móvil (<901px)

4 sub-toggles colapsables dentro del drawer, cada uno con su título y los items respectivos. Reutiliza el patrón actual `terra-nav__drawer-sub-toggle`.

---

## Items completos con texto y links

### Sección 1: SERVICIOS DE JARDINERÍA

| Ícono | Texto principal | Helper text | URL |
|-------|----------------|-------------|-----|
| 🌿 | Pasto en Rollo San Agustín | Instalación desde $85/m² · Mayoreo | `/pasto-en-rollo-tampico` |
| ♻️ | Pasto Sintético | Verde todo el año, sin mantenimiento | `/pasto-sintetico-tampico` |
| 🏡 | Diseño de Jardines | Plan Terra desde $3,000 | `/diseno-jardines-tampico` |
| ✂️ | Mantenimiento | Desde $750/mes · Residencial e industrial | `/mantenimiento-jardines-tampico` |
| 💧 | Sistema de Riego | Automatizado · Ahorra 40% agua | `/sistema-riego-tampico` |

### Sección 2: PLANTAS Y PALMAS

| Ícono | Texto principal | Helper text | URL |
|-------|----------------|-------------|-----|
| 🌴 | **Catálogo de Plantas** | +118 especies del vivero | `/plantas-palmas-arboles-tampico` |
| 🥥 | Palmas Tropicales | Viajero, Areca, Real, Coco y más | `/palmas-tropicales-tampico` |
| 🌳 | Árboles para Banqueta | 7 especies que no levantan pavimento | `/arboles-para-banqueta-tampico` |
| 🪟 | Plantas de Interior | Pothos, Sansevieria, Aglaonema | `/plantas-de-interior-tampico` |

### Sección 3: MATERIALES

| Ícono | Texto principal | Helper text | URL |
|-------|----------------|-------------|-----|
| 🪴 | Tierra Negra y Sustratos | Costal $90 · Camión volteo | `/tierra-negra-vegetal-tampico` |
| 🟥 | Tezontle Rojo | Costal $120 · Por m³ | `/tezontle-rojo-tampico` |
| ⚪ | Mármol Blanco | Decorativo · Senderos · Bordes | `/marmol-blanco-tampico` |
| 🪨 | Piedra de Río / Bola | Senderos · Estanques · Drenaje | `/piedra-bola-rio-tampico` |

### Sección 4: POR ZONA · B2B

| Ícono | Texto principal | Helper text | URL |
|-------|----------------|-------------|-----|
| 📍 | Vivero en Tampico | +150 variedades en Cd. Madero | `/vivero-tampico` |
| 📍 | Jardinería Ciudad Madero | Local · Sin recargo por zona | `/jardineria-ciudad-madero` |
| 📍 | Jardinería Altamira | Industrial y residencial | `/jardineria-altamira` |
| 🏗️ | Mayoreo Constructoras | Precio por volumen · CFDI | `/mayoreo-pasto-tampico` |

**Total: 17 items en 4 secciones.**

---

## Cambios CSS

### Estilos nuevos a añadir

```css
/* Ampliar dropdown de 580px a 720px */
.terra-nav__dropdown {
  width: 720px;
}

/* Headers de sección */
.terra-nav__drop-section {
  margin-top: 12px;
}
.terra-nav__drop-section:first-of-type {
  margin-top: 0;
}
.terra-nav__drop-header {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #1B5E20;
  padding: 8px 12px 6px;
  border-bottom: 1px solid #e8f0e8;
  margin-bottom: 4px;
}

/* En mobile, ajustar el ancho a 100% */
@media (max-width: 900px) {
  .terra-nav__dropdown {
    width: 100%;
  }
}
```

### Mobile drawer — añadir 4 sub-toggles

Reemplazar el único `<button class="terra-nav__drawer-sub-toggle">🌿 Servicios</button>` por 4 sub-toggles, uno por sección:

- 🌱 Servicios de Jardinería (5 items)
- 🌴 Plantas y Palmas (4 items)
- 🪨 Materiales (4 items)
- 📍 Por Zona y Mayoreo (4 items)

Cada uno con su `terra-nav__drawer-sub` correspondiente.

---

## Top nav (sin cambios)

El top nav mantiene su estructura:
```
[Logo]  Servicios▼  Catálogo  Blog        📞 833 326 8008  [WhatsApp CTA]
```

---

## Archivos a modificar

Todos los archivos HTML que contienen el `terra-nav` actualmente. Cuento aproximado: ~22 archivos:

- `public/index.html`
- `public/catalogo.html`
- `public/pasto-en-rollo-tampico/index.html`
- `public/pasto-sintetico-tampico/index.html`
- `public/diseno-jardines-tampico/index.html`
- `public/mantenimiento-jardines-tampico/index.html`
- `public/sistema-riego-tampico/index.html`
- `public/plantas-palmas-arboles-tampico/index.html`
- `public/tezontle-rojo-tampico/index.html`
- `public/tezontle-tampico/index.html`
- `public/tierra-negra-tampico/index.html`
- `public/tierra-negra-vegetal-tampico/index.html`
- `public/marmol-blanco-tampico/index.html`
- `public/piedra-bola-rio-tampico/index.html`
- `public/palmas-tropicales-tampico/index.html`
- `public/palmas-para-jardin-tampico/index.html`
- `public/arboles-ornamentales-tampico/index.html`
- `public/arboles-para-banqueta-tampico/index.html`
- `public/plantas-de-interior-tampico/index.html`
- `public/plantas-para-jardin-tampico/index.html`
- `public/vivero-tampico/index.html`
- `public/mayoreo-pasto-tampico/index.html`
- `public/jardineria-ciudad-madero/index.html`
- `public/jardineria-altamira/index.html`
- `public/blog/index.html` y posts del blog que tengan terra-nav

---

## Estrategia de implementación

Dado que el navbar HTML es idéntico en ~22 archivos, la implementación debe ser sistemática:

1. Crear un script Python que reemplace el bloque `<nav class="terra-nav">...</nav>` (incluyendo el script de inicialización inmediato) en todos los archivos.
2. El script lee el bloque `<nav>` actual y lo reemplaza con la nueva versión.
3. Para cada archivo, mantener intacto el `data-page="..."` específico de cada página (esto marca el link activo).
4. CSS de la nav también se replica en cada archivo, así que el script debe actualizar tanto el CSS como el HTML del nav.

---

## Self-review

- ✅ Sin TBDs ni placeholders
- ✅ 17 items completamente especificados con ícono, texto, helper y URL
- ✅ 4 secciones con headers definidos visualmente
- ✅ Layout 2×2 cuadrículas claramente especificado
- ✅ Comportamiento mobile contemplado (4 sub-toggles colapsables)
- ✅ Lista exhaustiva de archivos a modificar (~22)
- ✅ Estrategia de implementación sistemática (script Python)
- ✅ CSS específico para los nuevos elementos
- ✅ Top nav sin cambios (Catálogo y Blog quedan como están)
