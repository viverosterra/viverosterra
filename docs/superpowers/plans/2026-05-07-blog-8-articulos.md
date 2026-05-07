# 8 Blog Articles SEO + AEO + AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear 8 artículos de blog standalone optimizados para SEO + AEO (Answer Engine Optimization) + AI search engines, y actualizar el blog index para incluirlos.

**Architecture:** Cada artículo es un archivo HTML independiente bajo `public/blog/[slug]/index.html`, copiando la estructura de un artículo existente como base (`public/blog/pasto-san-agustin-instalacion-mantenimiento/index.html`). Cada artículo recibe contenido único optimizado para citaciones de IA y rich snippets de Google.

**Tech Stack:** HTML estático, Tailwind CSS (build compilado en `/css/tailwind.css`), JSON-LD schemas, fotos existentes en `/img/`.

---

## Mapa de archivos

**Crear (8 artículos):**
1. `public/blog/cuanto-cuesta-jardin-tampico-precios/index.html`
2. `public/blog/cesped-amarillo-tampico-causas-soluciones/index.html`
3. `public/blog/palmas-mas-vendidas-tampico-precios/index.html`
4. `public/blog/jardin-bajo-presupuesto-tampico/index.html`
5. `public/blog/errores-pasto-san-agustin-tampico/index.html`
6. `public/blog/tierra-negra-costal-camion-tampico/index.html`
7. `public/blog/riego-automatico-tampico-roi/index.html`
8. `public/blog/como-medir-plantas-altura-cepellon/index.html`

**Modificar (2):**
- `public/blog/index.html` — añadir 8 cards
- `public/sitemap.xml` — añadir 8 URLs

---

## Estructura común de cada artículo

Todos los artículos siguen este patrón. Usar como base copiando de `public/blog/pasto-san-agustin-instalacion-mantenimiento/index.html`:

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[TÍTULO] · Viveros Terra</title>
  <meta name="description" content="[META DESC 150-160 chars con keyword + Tampico]">
  <link rel="canonical" href="https://www.viverosterra.com/blog/[SLUG]">
  <meta name="robots" content="index, follow">
  <meta name="geo.region" content="MX-TAM">
  <link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://www.viverosterra.com/blog/[SLUG]">
  <meta property="og:title" content="[TÍTULO]">
  <meta property="og:description" content="[META DESC]">
  <meta property="og:image" content="https://www.viverosterra.com/img/[FOTO_HERO]">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_MX">
  <meta property="og:site_name" content="Viveros Terra">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="[TÍTULO]">
  <meta name="twitter:image" content="https://www.viverosterra.com/img/[FOTO_HERO]">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/tailwind.css">
  <style>
    html{scroll-behavior:smooth}
    body{font-family:"Inter",sans-serif;background:#FAFAF7}
    h1,h2,h3,h4{font-family:"Playfair Display",serif}
    .article-prose p{margin-bottom:1.25rem;line-height:1.75;color:#374151}
    .article-prose h2{font-size:1.875rem;font-weight:800;color:#0D2B0E;margin-top:2.5rem;margin-bottom:1rem}
    .article-prose h3{font-size:1.375rem;font-weight:700;color:#1B5E20;margin-top:1.75rem;margin-bottom:0.75rem}
    .article-prose ul{margin-bottom:1.25rem;padding-left:1.5rem;list-style:disc}
    .article-prose li{margin-bottom:0.5rem;line-height:1.7}
    .article-prose table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:0.95rem}
    .article-prose th{background:#F0F7F0;color:#0D2B0E;font-weight:700;text-align:left;padding:0.75rem 1rem;border-bottom:2px solid #1B5E20}
    .article-prose td{padding:0.75rem 1rem;border-bottom:1px solid #e5e7eb}
    .article-prose tr:hover td{background:#FAFAF7}
    .article-prose blockquote{border-left:4px solid #66BB6A;padding:1rem 1.5rem;background:#F0F7F0;margin:1.5rem 0;border-radius:0 0.5rem 0.5rem 0}
    .answer-box{background:linear-gradient(135deg,#1B5E20 0%,#0D2B0E 100%);color:#fff;padding:1.75rem 2rem;border-radius:1rem;margin:1.5rem 0 2rem}
    .answer-box-label{font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#66BB6A;margin-bottom:0.5rem}
    .answer-box p{font-size:1.0625rem;line-height:1.6;margin:0;color:#fff}
    .toc{background:#FAFAF7;border:1px solid #e5e7eb;border-radius:0.75rem;padding:1.25rem 1.5rem;margin:2rem 0}
    .toc-title{font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1B5E20;margin-bottom:0.75rem}
    .toc ol{list-style:decimal;padding-left:1.25rem;margin:0;font-size:0.9375rem}
    .toc li{margin-bottom:0.4rem;line-height:1.5}
    .toc a{color:#374151;text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s}
    .toc a:hover{border-bottom-color:#1B5E20;color:#0D2B0E}
    .faq-block{background:#fff;border:1px solid #e5e7eb;border-radius:0.75rem;padding:1.25rem 1.5rem;margin-bottom:0.75rem}
    .faq-block h3{font-size:1.0625rem;color:#0D2B0E;margin:0 0 0.5rem;font-family:"Inter",sans-serif;font-weight:700}
    .faq-block p{margin:0;line-height:1.6}
    .author-block{display:flex;gap:1rem;align-items:flex-start;background:#F0F7F0;border-left:4px solid #1B5E20;padding:1.25rem 1.5rem;border-radius:0.5rem;margin:2.5rem 0 1.5rem}
    .author-avatar{width:48px;height:48px;background:#1B5E20;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0}
    .author-name{font-weight:700;color:#0D2B0E;margin-bottom:0.25rem}
    .author-bio{font-size:0.875rem;color:#4b5563;line-height:1.5}
    .related-posts{margin-top:3rem;padding-top:2rem;border-top:2px solid #e5e7eb}
    .wa-float{position:fixed;bottom:24px;right:24px;z-index:100;animation:pulse-wa 2.5s infinite}
    @keyframes pulse-wa{0%,100%{box-shadow:0 0 0 0 rgba(37,211,102,.4)}70%{box-shadow:0 0 0 14px rgba(37,211,102,0)}}
  </style>
  
  <!-- Schema JSON-LD: Article + FAQPage + BreadcrumbList -->
  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@graph":[
      {
        "@type":"Article",
        "@id":"https://www.viverosterra.com/blog/[SLUG]#article",
        "headline":"[TÍTULO]",
        "description":"[META DESC]",
        "image":"https://www.viverosterra.com/img/[FOTO_HERO]",
        "datePublished":"2026-05-07",
        "dateModified":"2026-05-07",
        "wordCount":[NUM_PALABRAS],
        "inLanguage":"es-MX",
        "author":{
          "@type":"Organization",
          "name":"Viveros Terra",
          "url":"https://www.viverosterra.com"
        },
        "publisher":{
          "@type":"Organization",
          "name":"Viveros Terra",
          "logo":{"@type":"ImageObject","url":"https://www.viverosterra.com/img/logo-viveros-terra-tampico.png"}
        },
        "mainEntityOfPage":"https://www.viverosterra.com/blog/[SLUG]"
      },
      {
        "@type":"FAQPage",
        "mainEntity":[
          {"@type":"Question","name":"[Q1]","acceptedAnswer":{"@type":"Answer","text":"[A1]"}},
          {"@type":"Question","name":"[Q2]","acceptedAnswer":{"@type":"Answer","text":"[A2]"}},
          {"@type":"Question","name":"[Q3]","acceptedAnswer":{"@type":"Answer","text":"[A3]"}},
          {"@type":"Question","name":"[Q4]","acceptedAnswer":{"@type":"Answer","text":"[A4]"}},
          {"@type":"Question","name":"[Q5]","acceptedAnswer":{"@type":"Answer","text":"[A5]"}}
        ]
      },
      {
        "@type":"BreadcrumbList",
        "itemListElement":[
          {"@type":"ListItem","position":1,"name":"Inicio","item":"https://www.viverosterra.com"},
          {"@type":"ListItem","position":2,"name":"Blog","item":"https://www.viverosterra.com/blog"},
          {"@type":"ListItem","position":3,"name":"[TÍTULO_CORTO]","item":"https://www.viverosterra.com/blog/[SLUG]"}
        ]
      }
    ]
  }
  </script>
  
  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
</head>
<body class="text-gray-900">

<!-- WhatsApp Float -->
<a href="[WA_LINK_CONTEXTUAL]" target="_blank" rel="noopener"
   class="wa-float flex items-center gap-2 bg-wa text-white px-4 py-3 rounded-full font-semibold text-sm shadow-xl hover:bg-green-500 transition-colors" aria-label="Cotizar por WhatsApp">
  <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  <span class="hidden sm:inline">Cotizar ahora</span>
</a>

<!-- TERRA-NAV — copiar el bloque <nav class="terra-nav">...</nav> + script de cualquier página existente como public/blog/pasto-san-agustin-instalacion-mantenimiento/index.html. Ajustar data-page="/blog" -->
[INSERTAR TERRA-NAV con data-page="/blog"]

<!-- ARTÍCULO -->
<article class="bg-white">
  <!-- Hero -->
  <header class="bg-dark py-12 sm:py-16 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <nav aria-label="Breadcrumb" class="text-sm mb-6">
        <ol class="flex items-center gap-2 text-white/60">
          <li><a href="/" class="hover:text-accent">Inicio</a></li>
          <li>/</li>
          <li><a href="/blog" class="hover:text-accent">Blog</a></li>
          <li>/</li>
          <li class="text-white">[CATEGORÍA]</li>
        </ol>
      </nav>
      <span class="inline-block bg-accent/20 text-accent font-semibold text-xs uppercase tracking-widest px-3 py-1 rounded-full mb-4">[CATEGORÍA]</span>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-white leading-tight mb-4">
        [TÍTULO]
      </h1>
      <div class="flex items-center gap-4 text-white/60 text-sm">
        <span>📝 Equipo Técnico Viveros Terra</span>
        <span>·</span>
        <span>📅 7 de mayo de 2026</span>
        <span>·</span>
        <span>⏱️ [TIEMPO_LECTURA] min de lectura</span>
      </div>
    </div>
  </header>

  <!-- Content -->
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    
    <!-- AEO answer box (50 palabras max) -->
    <div class="answer-box">
      <div class="answer-box-label">Respuesta directa</div>
      <p>[RESPUESTA_50_PALABRAS]</p>
    </div>

    <!-- Hero image -->
    <img src="/img/[FOTO_HERO]" alt="[ALT_TEXT]" class="w-full h-64 sm:h-80 object-cover rounded-2xl mb-8" loading="eager">

    <!-- TOC -->
    <nav class="toc" aria-label="Tabla de contenidos">
      <div class="toc-title">En este artículo</div>
      <ol>
        <li><a href="#seccion-1">[SECCIÓN 1]</a></li>
        <li><a href="#seccion-2">[SECCIÓN 2]</a></li>
        <li><a href="#seccion-3">[SECCIÓN 3]</a></li>
        <li><a href="#seccion-4">[SECCIÓN 4]</a></li>
        <li><a href="#faq">Preguntas frecuentes</a></li>
      </ol>
    </nav>

    <!-- Article body -->
    <div class="article-prose">
      [CONTENIDO_PRINCIPAL]
    </div>

    <!-- FAQ -->
    <section id="faq" class="mt-12">
      <h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mb-6">Preguntas frecuentes</h2>
      <div class="faq-block">
        <h3>[Q1]</h3>
        <p>[A1]</p>
      </div>
      <div class="faq-block">
        <h3>[Q2]</h3>
        <p>[A2]</p>
      </div>
      <div class="faq-block">
        <h3>[Q3]</h3>
        <p>[A3]</p>
      </div>
      <div class="faq-block">
        <h3>[Q4]</h3>
        <p>[A4]</p>
      </div>
      <div class="faq-block">
        <h3>[Q5]</h3>
        <p>[A5]</p>
      </div>
    </section>

    <!-- CTA WhatsApp contextual -->
    <div class="bg-dark rounded-2xl p-8 text-center my-10">
      <h3 class="text-2xl font-display font-bold text-white mb-3">[CTA_TITLE]</h3>
      <p class="text-white/70 mb-6 max-w-md mx-auto">[CTA_SUBTITLE]</p>
      <a href="[WA_LINK_CONTEXTUAL]" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-wa text-white px-7 py-3.5 rounded-full font-bold hover:bg-green-400 transition-colors shadow-xl">
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        [CTA_BUTTON]
      </a>
    </div>

    <!-- Author E-E-A-T block -->
    <div class="author-block">
      <div class="author-avatar">🌿</div>
      <div>
        <div class="author-name">Equipo Técnico Viveros Terra</div>
        <div class="author-bio">Jardineros y paisajistas con +20 años de experiencia en el clima tropical de la Huasteca Tamaulipeca. +500,000 m² de pasto instalados y +1,500 jardines diseñados en el sur de Tamaulipas.</div>
      </div>
    </div>

    <!-- Related posts -->
    <div class="related-posts">
      <h3 class="text-xl font-display font-bold text-gray-900 mb-4">Posts relacionados</h3>
      <div class="grid sm:grid-cols-3 gap-4">
        <a href="[REL_1_URL]" class="block p-4 bg-bgwarm rounded-xl hover:shadow-md transition-shadow">
          <div class="text-xs text-primary font-semibold uppercase tracking-wider mb-1">[REL_1_CAT]</div>
          <div class="font-semibold text-gray-900 leading-snug">[REL_1_TITLE]</div>
        </a>
        <a href="[REL_2_URL]" class="block p-4 bg-bgwarm rounded-xl hover:shadow-md transition-shadow">
          <div class="text-xs text-primary font-semibold uppercase tracking-wider mb-1">[REL_2_CAT]</div>
          <div class="font-semibold text-gray-900 leading-snug">[REL_2_TITLE]</div>
        </a>
        <a href="[REL_3_URL]" class="block p-4 bg-bgwarm rounded-xl hover:shadow-md transition-shadow">
          <div class="text-xs text-primary font-semibold uppercase tracking-wider mb-1">[REL_3_CAT]</div>
          <div class="font-semibold text-gray-900 leading-snug">[REL_3_TITLE]</div>
        </a>
      </div>
    </div>

  </div>
</article>

<!-- FOOTER — copiar el bloque <footer>...</footer> de cualquier página existente -->
[INSERTAR FOOTER]

</body>
</html>
```

---

## Briefs detallados por artículo

### Brief 1: ¿Cuánto cuesta hacer un jardín en Tampico? Guía de precios 2026

**Slug:** `cuanto-cuesta-jardin-tampico-precios`
**Foto hero:** `/img/diseno-jardines-tampico-proyecto.jpg`
**Categoría:** Precios
**Tiempo lectura:** 9 min
**Word count:** 2,200
**Meta description:** "¿Cuánto cuesta hacer un jardín en Tampico? Guía de precios 2026 con desglose por servicio: pasto $85/m², diseño $3K, riego, plantas. Cotiza gratis."

**Respuesta directa (50 palabras):** "El costo de hacer un jardín en Tampico va desde $5,000 MXN para un jardín mini residencial hasta más de $200,000 MXN para proyectos premium. El factor más importante es el tamaño del terreno. El pasto en rollo San Agustín cuesta desde $85/m² instalado, y el diseño profesional desde $3,000."

**Estructura de contenido:**
- H2: ¿Cuánto cuesta un jardín pequeño en Tampico? ($5K-$15K)
- H2: ¿Cuánto cuesta un jardín mediano? ($15K-$50K)
- H2: ¿Cuánto cuesta un jardín premium? ($50K-$200K+)
- H2: Desglose por componente (tabla con: Pasto $85/m², Tierra $90/costal, Diseño $3K-$18K, Riego, Plantas, Mano de obra)
- H2: 3 ejemplos reales de presupuestos
- H2 FAQ con: ¿Incluye mantenimiento?, ¿Hay financiamiento?, ¿Cuánto tarda?, ¿Necesito licencia?, ¿Pueden venir a cotizar?

**Internal links a:** /pasto-en-rollo-tampico, /diseno-jardines-tampico, /mantenimiento-jardines-tampico

**WA contextual:** `https://wa.me/528333268008?text=Hola%2C%20vi%20la%20gu%C3%ADa%20de%20precios%20de%20jardines%20y%20quiero%20cotizar%20el%20m%C3%ADo`

**CTA title:** "Cotiza tu jardín en menos de 2 horas"
**CTA button:** "Cotizar mi jardín"

---

### Brief 2: Por qué tu césped se pone amarillo en Tampico (y cómo arreglarlo)

**Slug:** `cesped-amarillo-tampico-causas-soluciones`
**Foto hero:** `/img/instalacion-pasto-san-agustin-jardin-residencial-tampico-madero.webp`
**Categoría:** Pasto
**Tiempo lectura:** 7 min
**Word count:** 1,800

**Meta description:** "Tu césped se pone amarillo en Tampico? Las 5 causas más comunes (riego, plagas, hongos, suelo, sol) y cómo solucionarlas paso a paso. Diagnóstico gratis."

**Respuesta directa:** "Tu césped en Tampico se pone amarillo principalmente por 5 causas: exceso o falta de riego, plagas como gusano del cogollo, hongos por humedad, suelo compactado o pH incorrecto, y exposición solar inadecuada. La solución correcta depende del diagnóstico — los síntomas son distintos para cada causa."

**Estructura:**
- H2: Causa 1 — Riego incorrecto (señales + diagnóstico + fix)
- H2: Causa 2 — Plagas (gusano cogollo, chinche, etc.)
- H2: Causa 3 — Hongos por humedad
- H2: Causa 4 — Suelo compactado o pH
- H2: Causa 5 — Sombra excesiva o sol directo en pasto inapropiado
- H2: ¿Cuándo llamar a un profesional?
- H2 FAQ

**Internal links a:** /pasto-en-rollo-tampico, /mantenimiento-jardines-tampico, /sistema-riego-tampico

---

### Brief 3: Las 8 palmas más vendidas en Tampico (con precios actualizados)

**Slug:** `palmas-mas-vendidas-tampico-precios`
**Foto hero:** `/img/plantas-tropicales-tampico-viveros.png`
**Categoría:** Palmas
**Tiempo lectura:** 10 min
**Word count:** 2,400

**Meta description:** "Las 8 palmas más vendidas en Tampico con precios 2026: Washingtona desde $500, Viajero $500, Areca $300, Coco, Real, Kerpis y más. Vivero productor."

**Respuesta directa:** "Las 8 palmas más vendidas en Tampico son: Washingtona (desde $500), Palma del Viajero ($500), Areca ($300), Real, Coco Plumoso ($500), Kerpis ($500), Cycas Revoluta ($700), y Bambú ($1,000). Los precios varían según el tamaño. Todas se adaptan al clima cálido-húmedo de la Huasteca."

**Estructura:**
- Tabla resumen de las 8 con precio desde
- H2 por cada palma (8 secciones): foto, características, altura adulta, precio, mantenimiento, dónde plantar
- H2: ¿Cuál palma elegir según tu espacio?
- H2: Cuidados básicos comunes en Tampico
- H2 FAQ

**Internal links a:** /palmas-tropicales-tampico, /palmas-para-jardin-tampico, /plantas-palmas-arboles-tampico, /catalogo

---

### Brief 4: Jardín bajo presupuesto en Tampico: cómo gastar $5K, $20K o $50K

**Slug:** `jardin-bajo-presupuesto-tampico`
**Foto hero:** `/img/jardin-residencial-plantas-pasto-tampico.jpg`
**Categoría:** Presupuesto
**Tiempo lectura:** 8 min
**Word count:** 2,000

**Meta description:** "Cómo armar un jardín en Tampico con $5K, $20K o $50K. 3 niveles de inversión con paquetes reales — qué incluye cada uno y cómo elegir."

**Respuesta directa:** "Con $5,000 MXN puedes hacer un jardín mini con pasto + plantas básicas. Con $20,000 MXN obtienes pasto + diseño básico + plantas + tierra. Con $50,000 MXN un proyecto completo con riego automático, palmas y mantenimiento incluido. Todo cotizado por Viveros Terra en Tampico, Madero y Altamira."

**Estructura:**
- Tabla 3 tiers (qué incluye cada uno)
- H2: Paquete $5,000 — qué incluye y para qué tipo de espacio
- H2: Paquete $20,000 — opciones intermedias  
- H2: Paquete $50,000 — premium con Plan Terra
- H2: ROI y valor agregado a la propiedad
- H2 FAQ

**Internal links a:** /diseno-jardines-tampico, /pasto-en-rollo-tampico, /mantenimiento-jardines-tampico

---

### Brief 5: 5 errores que matan tu pasto San Agustín (y cómo evitarlos)

**Slug:** `errores-pasto-san-agustin-tampico`
**Foto hero:** `/img/pasto-en-rollo-san-agustin-tampico.jpg`
**Categoría:** Pasto
**Tiempo lectura:** 7 min
**Word count:** 1,600

**Meta description:** "Los 5 errores más comunes que matan tu pasto San Agustín en Tampico: riego, corte, suelo, fertilización y plagas. Cómo evitarlos con guía paso a paso."

**Respuesta directa:** "Los 5 errores que matan el pasto San Agustín en Tampico son: 1) regar todos los días (causa hongos), 2) cortar muy bajo (debilita la raíz), 3) no airear el suelo compactado, 4) fertilizar en exceso o con producto incorrecto, y 5) ignorar plagas tempranas como el gusano del cogollo."

**Estructura:**
- H2 por cada error (señales + por qué pasa + cómo arreglarlo)
- H2: Calendario de cuidado mensual
- H2 FAQ

**Internal links a:** /pasto-en-rollo-tampico, /mantenimiento-jardines-tampico, /blog/cuando-regar-pasto-san-agustin-tampico

---

### Brief 6: Tierra negra en Tampico: ¿costal o camión?

**Slug:** `tierra-negra-costal-camion-tampico`
**Foto hero:** `/img/tierra-negra-jardin-tampico.png`
**Categoría:** Materiales
**Tiempo lectura:** 5 min
**Word count:** 1,400

**Meta description:** "¿Comprar tierra negra por costal o camión en Tampico? Guía con precios ($90 costal, $1,500 m³), calculadora y cuándo conviene cada opción."

**Respuesta directa:** "Si necesitas menos de 4 m² de tierra negra en Tampico, conviene comprar costales a $90 c/u. Si necesitas más, el camión volteo de 8 m³ a $1,500/m³ es más económico. Para jardines grandes (>15 m²) siempre conviene camión."

**Estructura:**
- Tabla decisión rápida (área vs costo total)
- H2: Cuándo conviene costal
- H2: Cuándo conviene camión
- H2: Calculadora de cuántos costales para X m²
- H2 FAQ

**Internal links a:** /tierra-negra-vegetal-tampico, /tezontle-rojo-tampico, /mayoreo-pasto-tampico

---

### Brief 7: Sistema de riego automático: ¿vale la pena la inversión?

**Slug:** `riego-automatico-tampico-roi`
**Foto hero:** `/img/instalacion-riego-tuberias-jardines-tampico.jpg`
**Categoría:** Riego
**Tiempo lectura:** 8 min
**Word count:** 1,800

**Meta description:** "¿Vale la pena el riego automático en Tampico? Análisis de ROI: ahorro de agua 40-60%, recuperación inversión 18-24 meses. Casos reales por tamaño."

**Respuesta directa:** "Sí, el sistema de riego automático en Tampico vale la pena en la mayoría de los casos. Ahorra entre 40% y 60% de agua vs riego manual, recupera la inversión en 18 a 24 meses, y libera 3-5 horas semanales. Para jardines de más de 50 m² es prácticamente obligatorio si quieres mantener el pasto sano."

**Estructura:**
- Tabla comparativa: manual vs automático (tiempo, agua, costo)
- H2: Costo de instalación por tamaño de jardín
- H2: Cálculo del ahorro real en clima Tampico
- H2: 3 casos reales (residencial chico, mediano, comercial)
- H2 FAQ

**Internal links a:** /sistema-riego-tampico, /pasto-en-rollo-tampico, /blog/como-ahorrar-agua-jardin-tampico

---

### Brief 8: Cómo se miden las plantas: altura, cepellón, ancho de fronda

**Slug:** `como-medir-plantas-altura-cepellon`
**Foto hero:** `/img/plantas-ornamentales-tampico-viveros-terra.png`
**Categoría:** Guías
**Tiempo lectura:** 5 min
**Word count:** 1,200

**Meta description:** "Cómo se mide la altura de una planta: desde la base del cepellón hasta la hoja más alta. Más mediciones que importan: cepellón, ancho fronda, grosor de tallo."

**Respuesta directa:** "La altura de una planta se mide desde la base del cepellón (donde empieza la tierra) hasta la hoja o brote más alto. Pero la altura sola no es suficiente: también importan el tamaño del cepellón, el grosor del tallo y el ancho de la fronda. Cualquier especificación adicional debe mencionarse al cotizar."

**Estructura:**
- H2: Las 4 mediciones que importan al comprar plantas
  - H3: Altura total (con diagrama textual: base del cepellón → punta más alta)
  - H3: Tamaño del cepellón (diámetro y profundidad)
  - H3: Grosor del tallo (DAP — diámetro a la altura del pecho)
  - H3: Ancho de fronda (especialmente palmas)
- H2: Por qué especificar todas las medidas al cotizar
- H2: Ejemplos correctos de especificación
  - "Necesito Palma Real de 2 m" ← incompleto
  - "Necesito Palma Real de 2 m de altura total, cepellón mínimo 40 cm, tallo grosor 8-10 cm" ← correcto
- H2: Cuál medida importa según el uso
  - Palmas → altura + ancho fronda
  - Árboles → altura + grosor tronco
  - Plantas ornamentales → altura + cepellón
- H2 FAQ

**Internal links a:** /catalogo, /palmas-tropicales-tampico, /plantas-palmas-arboles-tampico

**WA contextual:** `https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20una%20planta%20con%20medidas%20espec%C3%ADficas%3A`

**CTA title:** "Especifica medidas para tu cotización"
**CTA button:** "Cotizar con medidas exactas"

---

## Tasks

### Task 1: Artículo "¿Cuánto cuesta hacer un jardín en Tampico?"

**Files:**
- Create: `public/blog/cuanto-cuesta-jardin-tampico-precios/index.html`

- [ ] **Step 1: Crear el directorio**
```bash
mkdir -p /tmp/viverosterra-site/public/blog/cuanto-cuesta-jardin-tampico-precios
```

- [ ] **Step 2: Copiar la base estructural desde un post existente**
```bash
cp /tmp/viverosterra-site/public/blog/pasto-san-agustin-instalacion-mantenimiento/index.html \
   /tmp/viverosterra-site/public/blog/cuanto-cuesta-jardin-tampico-precios/index.html
```

- [ ] **Step 3: Reescribir el archivo completo con el template de arriba + Brief 1**

Usa el template HTML del comienzo del documento, sustituye los placeholders con los valores del Brief 1. Escribe el contenido principal de 2,200 palabras siguiendo la estructura definida (H2 por nivel de presupuesto, tabla de desglose, 3 ejemplos reales, FAQ).

Reglas para el contenido:
- Respuesta directa en `.answer-box` con exactamente 50 palabras
- Cada H2 con keyword variant
- Datos numéricos concretos (precios en MXN)
- Mínimo 1 tabla extraible
- Lista de ejemplos reales (3 casos: $8K, $35K, $120K)
- 5 preguntas FAQ con respuestas en 2-3 oraciones
- Schema JSON-LD con `wordCount: 2200`

- [ ] **Step 4: Commit**
```bash
cd /tmp/viverosterra-site
git add public/blog/cuanto-cuesta-jardin-tampico-precios/
git commit -m "feat(blog): artículo precios jardín Tampico — guía completa 2026"
```

---

### Task 2: Artículo "Por qué tu césped se pone amarillo"

**Files:** Create: `public/blog/cesped-amarillo-tampico-causas-soluciones/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/cesped-amarillo-tampico-causas-soluciones`
- [ ] **Step 2:** Copiar template base como en Task 1
- [ ] **Step 3:** Reescribir aplicando Brief 2 (1,800 palabras, 5 causas con diagnóstico + fix por cada una, schema FAQPage)
- [ ] **Step 4:** Commit con mensaje "feat(blog): artículo césped amarillo Tampico — 5 causas y soluciones"

---

### Task 3: Artículo "Las 8 palmas más vendidas en Tampico"

**Files:** Create: `public/blog/palmas-mas-vendidas-tampico-precios/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/palmas-mas-vendidas-tampico-precios`
- [ ] **Step 2:** Copiar template base
- [ ] **Step 3:** Reescribir aplicando Brief 3 (2,400 palabras, tabla resumen + 8 H2 con cada palma + decisión por espacio + FAQ)
- [ ] **Step 4:** Commit "feat(blog): artículo 8 palmas más vendidas Tampico con precios"

---

### Task 4: Artículo "Jardín bajo presupuesto"

**Files:** Create: `public/blog/jardin-bajo-presupuesto-tampico/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/jardin-bajo-presupuesto-tampico`
- [ ] **Step 2:** Copiar template
- [ ] **Step 3:** Reescribir aplicando Brief 4 (2,000 palabras, 3 tiers de presupuesto con detalle de qué incluye cada uno)
- [ ] **Step 4:** Commit "feat(blog): artículo jardín bajo presupuesto Tampico — $5K/$20K/$50K"

---

### Task 5: Artículo "5 errores que matan tu pasto"

**Files:** Create: `public/blog/errores-pasto-san-agustin-tampico/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/errores-pasto-san-agustin-tampico`
- [ ] **Step 2:** Copiar template
- [ ] **Step 3:** Reescribir aplicando Brief 5 (1,600 palabras, listicle con 5 errores detallados + calendario mensual)
- [ ] **Step 4:** Commit "feat(blog): artículo 5 errores pasto San Agustín Tampico"

---

### Task 6: Artículo "Tierra negra: ¿costal o camión?"

**Files:** Create: `public/blog/tierra-negra-costal-camion-tampico/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/tierra-negra-costal-camion-tampico`
- [ ] **Step 2:** Copiar template
- [ ] **Step 3:** Reescribir aplicando Brief 6 (1,400 palabras, decision guide con tabla y calculadora)
- [ ] **Step 4:** Commit "feat(blog): artículo tierra negra costal vs camión Tampico"

---

### Task 7: Artículo "Sistema de riego automático: ROI"

**Files:** Create: `public/blog/riego-automatico-tampico-roi/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/riego-automatico-tampico-roi`
- [ ] **Step 2:** Copiar template
- [ ] **Step 3:** Reescribir aplicando Brief 7 (1,800 palabras, ROI analysis con tabla comparativa + 3 casos reales)
- [ ] **Step 4:** Commit "feat(blog): artículo riego automático Tampico — análisis de ROI"

---

### Task 8: Artículo "Cómo se miden las plantas"

**Files:** Create: `public/blog/como-medir-plantas-altura-cepellon/index.html`

- [ ] **Step 1:** `mkdir -p /tmp/viverosterra-site/public/blog/como-medir-plantas-altura-cepellon`
- [ ] **Step 2:** Copiar template
- [ ] **Step 3:** Reescribir aplicando Brief 8 (1,200 palabras, technical educational con las 4 mediciones)
- [ ] **Step 4:** Commit "feat(blog): artículo cómo medir altura de plantas — cepellón, fronda, grosor"

---

### Task 9: Actualizar blog index y sitemap

**Files:**
- Modify: `public/blog/index.html`
- Modify: `public/sitemap.xml`

- [ ] **Step 1: Añadir 8 cards al feed del blog index**

Localizar en `public/blog/index.html` el grid de cards de blog posts (busca el patrón existente de cards). Añadir 8 cards nuevas — una por artículo — siguiendo el patrón visual existente. Cada card debe tener:
- Foto hero del artículo
- Categoría badge
- Título (H3) que enlaza al artículo
- Metadata: tiempo de lectura, fecha
- Descripción corta (~120 chars)

Posición: después de la sección "Los más buscados", antes del feed completo.

- [ ] **Step 2: Reemplazar emojis por fotos reales en "Los más buscados"**

Localizar las 3 cards de "Los más buscados" (que actualmente muestran emojis grandes 🌳 🌴 🌿). Reemplazar el área del emoji con una `<img>` de la foto real correspondiente:
- "Árboles para Banqueta" → `/img/jardineria-profesional-tampico-empresa.png`
- "Palma del Viajero" → `/img/plantas-tropicales-tampico-viveros.png`
- "San Agustín vs Japonés" → `/img/pasto-en-rollo-san-agustin-tampico.jpg`

Mantener el badge de búsquedas (2,170 / 1,559 / 935).

- [ ] **Step 3: Añadir las 8 URLs al sitemap**

En `public/sitemap.xml`, añadir antes del cierre `</urlset>`:

```xml
  <url><loc>https://www.viverosterra.com/blog/cuanto-cuesta-jardin-tampico-precios</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://www.viverosterra.com/blog/cesped-amarillo-tampico-causas-soluciones</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://www.viverosterra.com/blog/palmas-mas-vendidas-tampico-precios</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://www.viverosterra.com/blog/jardin-bajo-presupuesto-tampico</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.85</priority></url>
  <url><loc>https://www.viverosterra.com/blog/errores-pasto-san-agustin-tampico</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.viverosterra.com/blog/tierra-negra-costal-camion-tampico</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.viverosterra.com/blog/riego-automatico-tampico-roi</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.viverosterra.com/blog/como-medir-plantas-altura-cepellon</loc><lastmod>2026-05-07</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
```

- [ ] **Step 4: Commit y push final**

```bash
cd /tmp/viverosterra-site
git add public/blog/index.html public/sitemap.xml
git commit -m "feat(blog): añadir 8 nuevos posts al index, fotos reales y sitemap"
git push origin main
```

---

## Self-review

### Spec coverage

- ✅ Los 8 artículos están en Tasks 1-8 con sus briefs detallados
- ✅ El template HTML común está al principio para reutilización
- ✅ Schema markup (Article + FAQPage + BreadcrumbList) en el template
- ✅ Optimización AEO (answer box + H2 preguntas + FAQ schema) en cada artículo
- ✅ Optimización AI (datos específicos, autor, fechas, citas localizadas)
- ✅ Internal links definidos por artículo
- ✅ CTAs WhatsApp con mensajes pre-llenados contextuales
- ✅ Author E-E-A-T en cada artículo
- ✅ Mejoras al blog index (Task 9): nuevas cards, fotos reales, sitemap

### Placeholder scan

- ✅ Sin TBDs ni "implement later"
- ✅ Cada brief tiene meta description, respuesta directa, estructura completa, internal links y CTA específicos
- ✅ Word counts definidos por artículo
- ✅ Comandos exactos con bash y git messages

### Type consistency

- ✅ Slugs consistentes entre tasks, briefs, sitemap y internal links
- ✅ Foto hero referenciada por nombre exacto del archivo en `/img/`
- ✅ URLs de internal links existen en el sitio actual
- ✅ Schema markup props consistentes (datePublished/dateModified, wordCount, author)
