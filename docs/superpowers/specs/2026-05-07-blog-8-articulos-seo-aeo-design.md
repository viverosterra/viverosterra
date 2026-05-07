# 8 Artículos de Blog Optimizados SEO + AEO + AI — Design Spec

**Goal:** Escribir 8 artículos nuevos de blog para viverosterra.com optimizados simultáneamente para SEO tradicional, AEO (Answer Engine Optimization), y AI search engines (ChatGPT, Perplexity, Google AI Overviews). Mejorar también el diseño/UX del blog index.

**Architecture:** Cada artículo es un archivo HTML standalone bajo `public/blog/[slug]/index.html` siguiendo el patrón visual existente del sitio (terra-nav, hero dark, Playfair Display, footer). Cada artículo incluye estructura específica para AEO (respuesta directa en primer párrafo, H2s en formato pregunta, tablas extraibles), Schema.org Article + FAQPage + BreadcrumbList, e interlinking a páginas de servicio relacionadas. El blog index se actualiza para incluir los 8 nuevos posts.

**Tech Stack:** HTML estático, Tailwind CSS (build compilado), JSON-LD para schemas, fotos existentes en `/img/`.

---

## Los 8 artículos

### Artículo 1: ¿Cuánto cuesta hacer un jardín en Tampico? Guía de precios 2026
- **Slug:** `/blog/cuanto-cuesta-jardin-tampico-precios`
- **Score:** 93
- **Tipo:** Pricing guide
- **Palabras:** 2,200
- **Keyword principal:** "cuanto cuesta jardin Tampico"
- **Keywords secundarias:** "precio diseño de jardín Tampico", "cotizar jardín Madero"
- **Estructura:**
  1. H1 + respuesta directa (rango $5K–$200K según tamaño/servicios)
  2. Tabla de precios por tipo (residencial mini, mediano, premium, comercial)
  3. Desglose de componentes (pasto, plantas, riego, mano de obra, materiales)
  4. 3 ejemplos reales de jardines con presupuestos
  5. FAQ (5 preguntas: ¿incluye mantenimiento?, ¿hay financiamiento?, etc.)
  6. CTA: "Cotiza tu jardín en menos de 2 horas"

### Artículo 2: Por qué tu césped se pone amarillo en Tampico (y cómo arreglarlo)
- **Slug:** `/blog/cesped-amarillo-tampico-causas-soluciones`
- **Score:** 92
- **Tipo:** Problem/Solution
- **Palabras:** 1,800
- **Keyword principal:** "cesped amarillo Tampico"
- **Estructura:**
  1. H1 + respuesta directa (top 5 causas: riego, plagas, hongos, suelo, sol)
  2. Diagnóstico paso a paso (5 H2s tipo pregunta)
  3. Soluciones por causa con costo aproximado
  4. Cuándo llamar a un profesional vs DIY
  5. FAQ + CTA

### Artículo 3: Las 8 palmas más vendidas en Tampico (con precios actualizados)
- **Slug:** `/blog/palmas-mas-vendidas-tampico-precios`
- **Score:** 90
- **Tipo:** Listicle con precios
- **Palabras:** 2,400
- **Keyword principal:** "palmas precios Tampico"
- **Estructura:**
  1. H1 + tabla resumen de las 8 palmas con precio desde
  2. Sección por palma: foto, características, precio, mantenimiento, dónde plantar
  3. Cuál elegir según presupuesto/espacio
  4. FAQ (¿cuánto crecen al año?, ¿toleran sol pleno?, etc.)
  5. CTA cotizar

### Artículo 4: Jardín bajo presupuesto en Tampico: cómo gastar $5K, $20K o $50K
- **Slug:** `/blog/jardin-bajo-presupuesto-tampico`
- **Score:** 86
- **Tipo:** Budget tier comparison
- **Palabras:** 2,000
- **Keyword principal:** "jardín económico Tampico"
- **Estructura:**
  1. H1 + tabla de 3 niveles de presupuesto
  2. Sección $5K: qué se puede hacer (pasto + plantas básicas)
  3. Sección $20K: opciones intermedias (riego básico + diseño)
  4. Sección $50K: paquete premium (Plan Terra completo)
  5. ROI/valor de propiedad
  6. FAQ + CTA

### Artículo 5: 5 errores que matan tu pasto San Agustín (y cómo evitarlos)
- **Slug:** `/blog/errores-pasto-san-agustin-tampico`
- **Score:** 85
- **Tipo:** Problem/Solution listicle
- **Palabras:** 1,600
- **Keyword principal:** "pasto san agustin errores"
- **Estructura:**
  1. H1 + respuesta directa (lista de los 5)
  2. Error #1: Riego excesivo (señales + fix)
  3. Error #2: Mal corte de altura
  4. Error #3: Suelo compactado
  5. Error #4: No fertilizar / sobre-fertilizar
  6. Error #5: Ignorar plagas tempranas
  7. FAQ + CTA mantenimiento

### Artículo 6: Tierra negra en Tampico: ¿costal o camión? Guía para elegir
- **Slug:** `/blog/tierra-negra-costal-camion-tampico`
- **Score:** 83
- **Tipo:** Decision guide
- **Palabras:** 1,400
- **Keyword principal:** "tierra negra Tampico precio"
- **Estructura:**
  1. H1 + tabla decisión rápida (m³ vs costo)
  2. Cuándo conviene costal ($90 c/u, hasta 4 m²)
  3. Cuándo conviene camión ($1,500/m³, 8m³+)
  4. Calculadora: cuántos costales para X m²
  5. FAQ + CTA

### Artículo 7: Sistema de riego automático: ¿vale la pena la inversión?
- **Slug:** `/blog/riego-automatico-tampico-roi`
- **Score:** 82
- **Tipo:** ROI analysis
- **Palabras:** 1,800
- **Keyword principal:** "riego automatico Tampico vale la pena"
- **Estructura:**
  1. H1 + respuesta directa (sí, ROI en 18-24 meses)
  2. Comparativa: riego manual vs automático (tabla)
  3. Costo de instalación por tamaño de jardín
  4. Ahorro de agua: % real en clima Tampico
  5. Casos: residencial pequeño, mediano, comercial
  6. FAQ + CTA

### Artículo 8: Cómo se miden las plantas: altura, cepellón, ancho de fronda
- **Slug:** `/blog/como-medir-plantas-altura-cepellon`
- **Score:** 63 (incluido por solicitud específica del cliente)
- **Tipo:** Educational technical
- **Palabras:** 1,200
- **Keyword principal:** "como medir altura plantas"
- **Keywords secundarias:** "tamaño cepellón", "ancho de fronda palmas"
- **Estructura:**
  1. H1 + respuesta directa (altura = base del cepellón a hoja más alta)
  2. Diagrama explicativo (descripción textual de imagen + alt text)
  3. Las 4 mediciones que importan:
     - Altura total (base a punta más alta)
     - Diámetro/grosor de tallo
     - Tamaño del cepellón
     - Ancho de fronda (palmas)
  4. Por qué es importante especificar todas
  5. Ejemplos: "Necesito Palma Real de 2m" vs "Palma Real de 2m con cepellón mínimo de 40cm"
  6. FAQ + CTA "Especifica medidas para tu cotización"

---

## Estructura común a todos los 8 artículos

### HTML Skeleton
```
<head>
  <title>[Título exacto] · Viveros Terra</title>
  <meta description con keyword + Tampico>
  <link canonical>
  <Open Graph + Twitter Card>
  <Schema: Article + FAQPage + BreadcrumbList>
</head>
<body>
  <terra-nav>
  <article>
    <header con breadcrumb, badges, H1>
    <metadatos: autor, fecha, tiempo de lectura, categoría>
    <imagen hero>
    <bloque destacado: respuesta directa en 50 palabras> ← AEO
    <tabla de contenido con anchor links>
    <contenido principal con H2s tipo pregunta>
    <tabla con datos extraibles> ← AI search
    <FAQ con 5 preguntas + schema FAQPage>
    <CTA WhatsApp con mensaje pre-llenado contextual>
    <sección "Posts relacionados" con 3 links internos>
    <footer del autor con E-E-A-T>
  </article>
  <site footer>
  <wa-float>
</body>
```

### Optimización SEO (clásico)
- Title: keyword principal + Tampico + Viveros Terra (≤60 chars)
- Meta description: keyword + diferenciador + CTA (150-160 chars)
- H1 único con keyword principal
- Canonical, robots, geo, OG tags completos
- Internal links a 3-5 páginas relevantes del sitio

### Optimización AEO (Google AI Overviews)
- **Respuesta directa en primer párrafo** (50 palabras máx) — Google AI cita estos
- H2s en formato pregunta ("¿Cómo...?", "¿Cuánto...?")
- Tablas con datos numéricos concretos
- Listas numeradas ordenadas
- Preguntas frecuentes con schema FAQPage

### Optimización AI search (ChatGPT, Perplexity, Claude)
- Author attribution en cada artículo (E-E-A-T)
- Fechas de publicación y actualización
- Citas de fuentes cuando aplique
- Datos específicos con números exactos (precios, %, cantidades)
- Localización contextual (Tampico, Tamaulipas, clima Huasteca)
- Schema Article completo con `wordCount`, `dateModified`, `author.url`

### Optimización LLM (semantic structure)
- Encabezados jerárquicos limpios (H1 → H2 → H3)
- Bullets y listas claras
- Frases cortas y declarativas
- Evita ambigüedad ("aproximadamente" → "entre $X y $Y")

---

## Mejoras al blog index (`public/blog/index.html`)

Adicionalmente al spec de los 8 artículos:

1. **Reemplazar emojis por fotos reales** en las cards de "Los más buscados" y feed general
2. **Añadir filtro por categoría** (Pasto · Palmas · Plantas · Materiales · Riego · Diseño)
3. **Añadir buscador interno del blog** (filtrado client-side por título)
4. **Mostrar metadata visible** en cada card: fecha, tiempo de lectura, categoría
5. **Añadir CTA de WhatsApp en sticky footer** del blog index
6. **Reorganizar feed**: featured (3) + grid completo con filtros

---

## Author E-E-A-T

Cada artículo termina con bloque de autor:
```
Autor: Equipo Técnico Viveros Terra
Jardineros y paisajistas con +20 años de experiencia 
en el clima tropical de la Huasteca Tamaulipeca. 
+500,000 m² de pasto instalados en el sur de Tamaulipas.
```

---

## Archivos a crear/modificar

**Crear (8 archivos):**
- `public/blog/cuanto-cuesta-jardin-tampico-precios/index.html`
- `public/blog/cesped-amarillo-tampico-causas-soluciones/index.html`
- `public/blog/palmas-mas-vendidas-tampico-precios/index.html`
- `public/blog/jardin-bajo-presupuesto-tampico/index.html`
- `public/blog/errores-pasto-san-agustin-tampico/index.html`
- `public/blog/tierra-negra-costal-camion-tampico/index.html`
- `public/blog/riego-automatico-tampico-roi/index.html`
- `public/blog/como-medir-plantas-altura-cepellon/index.html`

**Modificar (2 archivos):**
- `public/blog/index.html` — añadir 8 cards + filtros + buscador + fotos reales
- `public/sitemap.xml` — añadir los 8 nuevos URLs con `lastmod 2026-05-07`

---

## Self-review

- ✅ Sin TBDs ni placeholders
- ✅ 8 artículos con keyword principal, estructura específica y palabras objetivo
- ✅ Optimización SEO + AEO + AI definida con métodos concretos para cada uno
- ✅ Estructura HTML común clara
- ✅ Mejoras al blog index incluidas como sub-tarea
- ✅ Lista exhaustiva de archivos (10 total: 8 nuevos + 2 modificados)
- ✅ Author E-E-A-T contemplado
- ✅ Schema markup específico definido
- ✅ Interlinking a páginas de servicio especificado
