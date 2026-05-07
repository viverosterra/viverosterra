# Catálogo Interactivo con Filtros — Design Spec

**Goal:** Transformar `/catalogo` de brochure PDF sin SEO a landing page de alto valor con filtros interactivos, 16 productos indexables por Google y CTAs de WhatsApp por producto específico.

**Architecture:** HTML/CSS/JS puro. Todo el contenido de productos en el DOM desde el load inicial — Google indexa cada producto. JS solo maneja la visibilidad visual del filtro (`display:none`). Reemplaza `public/catalogo.html` completo.

**Tech Stack:** Tailwind CSS (CDN, igual que el resto del sitio), JS vanilla ~50 líneas, sin dependencias nuevas.

---

## Estructura de página

```
NAV (terra-nav, mismo que todo el sitio)
HERO — H1 + subtítulo con keywords + 2 badges
FILTROS — 4 pills: Todo | Pasto | Plantas & Palmas | Materiales
GRID DE PRODUCTOS — 3 col desktop / 1 col mobile
FAQ — 5 preguntas con schema FAQPage
CTA FINAL — WhatsApp genérico
FOOTER (mismo que todo el sitio)
```

---

## SEO

- **Title:** `Catálogo de Plantas, Pasto y Materiales en Tampico · Viveros Terra 2026`
- **Meta description:** `Catálogo completo de Viveros Terra en Tampico — pasto San Agustín, palmas, plantas ornamentales y materiales. +150 variedades, entrega a domicilio en Madero y Altamira. Cotiza hoy.`
- **H1:** `Catálogo de Plantas, Pasto y Materiales en Tampico`
- **Canonical:** `https://www.viverosterra.com/catalogo`
- **Open Graph:** og:title, og:description, og:image (foto del vivero o jardín), og:url
- **Schema:** `ItemList` (16 productos) + `FAQPage` (5 preguntas)

---

## Productos — 16 total

### 🌿 Pasto (3 productos)
| id | Nombre | Precio visible | Mensaje WhatsApp |
|----|--------|---------------|-----------------|
| pasto | Pasto San Agustín en Rollo | Desde $85/m² | "Hola, quiero cotizar pasto San Agustín en rollo" |
| pasto | Pasto Japonés en Rollo | Cotizar | "Hola, quiero cotizar pasto Japonés en rollo" |
| pasto | Pasto Sintético | Cotizar por m² | "Hola, quiero cotizar pasto sintético" |

### 🌴 Plantas & Palmas (8 productos)
| id | Nombre | Precio visible | Mensaje WhatsApp |
|----|--------|---------------|-----------------|
| plantas | Palma del Viajero | Cotizar | "Hola, quiero cotizar palma del viajero" |
| plantas | Palma Areca | Cotizar | "Hola, quiero cotizar palma areca" |
| plantas | Palma Real | Cotizar | "Hola, quiero cotizar palma real" |
| plantas | Palma Coco | Cotizar | "Hola, quiero cotizar palma coco" |
| plantas | Ficus Elastica | Cotizar | "Hola, quiero cotizar ficus elastica" |
| plantas | Plantas Ornamentales | Cotizar | "Hola, quiero cotizar plantas ornamentales" |
| plantas | Plantas de Interior | Cotizar | "Hola, quiero cotizar plantas de interior" |
| plantas | Árboles para Jardín y Banqueta | Cotizar | "Hola, quiero cotizar árboles para jardín" |

### 🪨 Materiales (5 productos)
| id | Nombre | Precio visible | Mensaje WhatsApp |
|----|--------|---------------|-----------------|
| materiales | Tierra Negra Vegetal | $90/costal · $1,500/m³ | "Hola, quiero cotizar tierra negra vegetal" |
| materiales | Tierra Negra para Maceta | Cotizar | "Hola, quiero cotizar tierra negra para maceta" |
| materiales | Tezontle Rojo | Cotizar | "Hola, quiero cotizar tezontle rojo" |
| materiales | Mármol Blanco Decorativo | Cotizar | "Hola, quiero cotizar mármol blanco" |
| materiales | Piedra de Río / Bola | Cotizar | "Hola, quiero cotizar piedra de río" |

---

## Diseño de card

```
┌─────────────────────────────┐
│  [foto 100% ancho, h-48]    │
│  🌿 PASTO   ← badge color  │
├─────────────────────────────┤
│  Nombre del producto (H3)   │
│  Descripción 2 líneas SEO   │
│  con keywords locales.      │
│                             │
│  Desde $85/m²               │  ← precio o "Cotizar"
│                             │
│  [💬 Cotizar por WhatsApp]  │  ← CTA verde full-width
└─────────────────────────────┘
```

**Colores de badge:**
- Pasto: `bg-primary text-white` (`#1B5E20`)
- Plantas & Palmas: `bg-secondary text-white` (`#2E7D32`)
- Materiales: `bg-amber-800 text-white`

---

## Sistema de filtros

```js
// Al cargar: activar "Todo"
// Al clic en filtro:
//   1. Quitar clase active de todos los botones
//   2. Añadir active al botón clickeado
//   3. Recorrer .catalog-card:
//      - Si data-cat === filtro activo OR filtro === "todo": mostrar
//      - Si no: ocultar con display:none
```

Transición: `transition-opacity duration-200` en los cards para suavizar.

Botón activo: `bg-primary text-white` · Inactivo: `bg-white text-gray-700 border border-gray-200`

---

## Interlinking (doble propósito)

Los cards de Plantas & Palmas enlazan a sus páginas de detalle para resolver el problema de páginas huérfanas:

- Card "Palma del Viajero" → link secundario a `/palmas-tropicales-tampico`
- Card "Árboles para Jardín y Banqueta" → link a `/arboles-para-banqueta-tampico`
- Card "Plantas de Interior" → link a `/plantas-de-interior-tampico`
- Card "Plantas Ornamentales" → link a `/plantas-para-jardin-tampico`

Formato del link secundario (dentro de la card, bajo el CTA):
```html
<a href="/palmas-tropicales-tampico" class="text-xs text-primary hover:underline">
  Ver guía completa →
</a>
```

---

## FAQ (5 preguntas — schema FAQPage)

1. ¿Tienen entrega a domicilio de plantas y materiales en Tampico?
2. ¿Cuánto cuesta el pasto San Agustín en Tampico?
3. ¿Puedo ir a comprar directamente al vivero?
4. ¿Venden al mayoreo para constructoras?
5. ¿Qué plantas recomiendan para el calor de Tampico?

---

## Imágenes de productos

Usar fotos existentes en `/img/` del repo:
- San Agustín: `pasto-en-rollo-san-agustin-tampico.jpg`
- Sintético: `pasto-sintetico-residencial-tampico.png`
- Palmas: `plantas-tropicales-tampico-viveros.png`
- Tierra negra: `tierra-negra-jardin-tampico.png`
- Tezontle: `tezontle-rojo-jardin-tampico-sendero.jpg` (ya en repo)
- Mármol: `piedra-marmol-blanca-decorativa-jardin-tampico.webp`

Para productos sin foto específica usar `plantas-ornamentales-tampico-viveros-terra.png` como fallback.

---

## Implementación — archivo a modificar

- **Modificar:** `public/catalogo.html` (reescritura completa)
- **No crear archivos nuevos**
- **Actualizar sitemap.xml:** cambiar `lastmod` de `/catalogo`

---

## Self-review

- ✅ Sin TBDs ni secciones incompletas
- ✅ 16 productos listados con todos sus campos
- ✅ JS descrito con precisión suficiente para implementar
- ✅ Interlinking resuelve problema de páginas huérfanas en paralelo
- ✅ Scope acotado: un solo archivo HTML
- ✅ Schema types definidos (ItemList + FAQPage)
- ✅ Fotos: todas reutilizadas del repo existente — sin assets nuevos
