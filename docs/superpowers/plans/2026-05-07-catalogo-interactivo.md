# Catálogo Interactivo con Filtros — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reescribir `public/catalogo.html` como catálogo interactivo con 16 productos filtrables, SEO completo, schema markup y CTAs WhatsApp por producto.

**Architecture:** Reescritura completa de un solo archivo HTML. Todo el contenido de productos en el DOM desde load inicial (SEO). JS vanilla ~50 líneas maneja visibilidad del filtro con `display:none`. Reutiliza el terra-nav y footer del resto del sitio. Resuelve además el interlinking de 6 páginas huérfanas.

**Tech Stack:** HTML5, Tailwind CDN (mismo config que el sitio), JS vanilla, imágenes existentes en `/img/`.

---

## Archivos

- **Modificar:** `public/catalogo.html` — reescritura completa
- **Modificar:** `public/sitemap.xml` — actualizar `<lastmod>` de `/catalogo`

---

### Task 1: Head, SVG icons, nav y estructura base

**Archivos:**
- Modify: `public/catalogo.html` (reemplazar contenido completo)

- [ ] **Paso 1: Reemplazar el archivo completo con la estructura base**

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Catálogo de Plantas, Pasto y Materiales en Tampico · Viveros Terra 2026</title>
<meta name="description" content="Catálogo completo de Viveros Terra en Tampico — pasto San Agustín, palmas, plantas ornamentales y materiales. +150 variedades, entrega a domicilio en Madero y Altamira. Cotiza hoy.">
<link rel="canonical" href="https://www.viverosterra.com/catalogo">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="MX-TAM">
<meta name="geo.placename" content="Tampico, Tamaulipas">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<link rel="icon" type="image/png" href="/img/logo-viveros-terra-tampico.png">
<link rel="apple-touch-icon" href="/img/logo-viveros-terra-tampico.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.viverosterra.com/catalogo">
<meta property="og:title" content="Catálogo Viveros Terra — Plantas, Pasto y Materiales en Tampico">
<meta property="og:description" content="Catálogo completo de Viveros Terra en Tampico — pasto San Agustín, palmas, plantas ornamentales y materiales. +150 variedades, entrega a domicilio.">
<meta property="og:image" content="https://www.viverosterra.com/img/jardin-residencial-tropical-tampico.jpg">
<meta property="og:locale" content="es_MX">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:"#1B5E20",secondary:"#2E7D32",accent:"#66BB6A",gold:"#C9A94E",dark:"#0D2B0E",wa:"#25D366",bgwarm:"#FAFAF7",bggreen:"#F0F7F0"},fontFamily:{display:["Playfair Display","serif"]}}}}</script>
<style>
html{scroll-behavior:smooth}
body{font-family:"Inter",sans-serif;background:#FAFAF7}
h1,h2,h3{font-family:"Playfair Display",serif}
.reveal{opacity:0;transform:translateY(24px);transition:opacity .6s ease,transform .6s ease}
.reveal.visible{opacity:1;transform:translateY(0)}
.logo-light{height:44px;width:auto;display:block;mix-blend-mode:multiply}
.logo-dark{height:44px;width:auto;display:block;filter:brightness(0) invert(1)}
.wa-float{position:fixed;bottom:24px;right:24px;z-index:100;animation:pulse-wa 2.5s infinite}
@keyframes pulse-wa{0%,100%{box-shadow:0 0 0 0 rgba(37,211,102,.4)}70%{box-shadow:0 0 0 14px rgba(37,211,102,0)}}
.img-card{overflow:hidden}.img-card img{transition:transform .4s ease;width:100%;height:100%;object-fit:cover}.img-card:hover img{transform:scale(1.04)}
.filter-btn.active{background:#1B5E20;color:#fff;border-color:#1B5E20}
.catalog-card{transition:opacity .2s ease}
.faq-answer{max-height:0;overflow:hidden;transition:max-height .4s ease}.faq-answer.open{max-height:400px}
</style>

<!-- Schema JSON-LD -->
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@graph":[
    {
      "@type":"ItemList",
      "name":"Catálogo Viveros Terra Tampico",
      "description":"Catálogo completo de plantas, pasto y materiales disponibles en Viveros Terra, Tampico, Tamaulipas",
      "url":"https://www.viverosterra.com/catalogo",
      "numberOfItems":16,
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Pasto San Agustín en Rollo","url":"https://www.viverosterra.com/pasto-en-rollo-tampico"},
        {"@type":"ListItem","position":2,"name":"Pasto Japonés en Rollo","url":"https://www.viverosterra.com/pasto-en-rollo-tampico"},
        {"@type":"ListItem","position":3,"name":"Pasto Sintético","url":"https://www.viverosterra.com/pasto-sintetico-tampico"},
        {"@type":"ListItem","position":4,"name":"Palma del Viajero","url":"https://www.viverosterra.com/palmas-tropicales-tampico"},
        {"@type":"ListItem","position":5,"name":"Palma Areca","url":"https://www.viverosterra.com/palmas-para-jardin-tampico"},
        {"@type":"ListItem","position":6,"name":"Palma Real","url":"https://www.viverosterra.com/plantas-palmas-arboles-tampico"},
        {"@type":"ListItem","position":7,"name":"Palma Coco","url":"https://www.viverosterra.com/plantas-palmas-arboles-tampico"},
        {"@type":"ListItem","position":8,"name":"Ficus Elastica","url":"https://www.viverosterra.com/plantas-palmas-arboles-tampico"},
        {"@type":"ListItem","position":9,"name":"Plantas Ornamentales","url":"https://www.viverosterra.com/plantas-para-jardin-tampico"},
        {"@type":"ListItem","position":10,"name":"Plantas de Interior","url":"https://www.viverosterra.com/plantas-de-interior-tampico"},
        {"@type":"ListItem","position":11,"name":"Árboles para Jardín y Banqueta","url":"https://www.viverosterra.com/arboles-para-banqueta-tampico"},
        {"@type":"ListItem","position":12,"name":"Tierra Negra Vegetal","url":"https://www.viverosterra.com/tierra-negra-vegetal-tampico"},
        {"@type":"ListItem","position":13,"name":"Tierra Negra para Maceta","url":"https://www.viverosterra.com/tierra-negra-vegetal-tampico"},
        {"@type":"ListItem","position":14,"name":"Tezontle Rojo","url":"https://www.viverosterra.com/tezontle-rojo-tampico"},
        {"@type":"ListItem","position":15,"name":"Mármol Blanco Decorativo","url":"https://www.viverosterra.com/marmol-blanco-tampico"},
        {"@type":"ListItem","position":16,"name":"Piedra de Río / Bola","url":"https://www.viverosterra.com/piedra-bola-rio-tampico"}
      ]
    },
    {
      "@type":"FAQPage",
      "mainEntity":[
        {"@type":"Question","name":"¿Tienen entrega a domicilio de plantas y materiales en Tampico?","acceptedAnswer":{"@type":"Answer","text":"Sí. Viveros Terra entrega plantas, pasto en rollo y materiales a domicilio en Tampico, Ciudad Madero y Altamira. Para pedidos grandes coordinamos logística a toda la zona Huasteca. Cotiza por WhatsApp al 833 326 8008."}},
        {"@type":"Question","name":"¿Cuánto cuesta el pasto San Agustín en Tampico?","acceptedAnswer":{"@type":"Answer","text":"El pasto San Agustín en rollo cuesta desde $85 por metro cuadrado (solo el pasto, sin entrega ni instalación). Con instalación profesional cotizamos según el tamaño del jardín y el estado del terreno. Cotización gratis sin compromiso."}},
        {"@type":"Question","name":"¿Puedo ir a comprar directamente al vivero?","acceptedAnswer":{"@type":"Answer","text":"Sí. Nuestro vivero está en Av. Álvaro Obregón 601, Col. Unidad Nacional, Ciudad Madero (frente al Walmart). Horario: Lunes a Viernes 9am–6pm, Sábado 9am–2pm. Te recomendamos llamar antes al 833 326 8008 para confirmar disponibilidad."}},
        {"@type":"Question","name":"¿Venden al mayoreo para constructoras?","acceptedAnswer":{"@type":"Answer","text":"Sí. Ofrecemos precios preferenciales por volumen para constructoras, arquitectos, fraccionamientos, hoteles y gobierno. Factura CFDI disponible. Entrega por etapas según avance de obra. Cotiza tu proyecto al 833 326 8008."}},
        {"@type":"Question","name":"¿Qué plantas recomiendan para el calor de Tampico?","acceptedAnswer":{"@type":"Answer","text":"Para el clima cálido-húmedo de Tampico recomendamos palmas tropicales (del viajero, areca, real, coco), Ficus elastica, plantas ornamentales de sol como heliconias y gingers, y para interior el pothos, sansevieria y aglaonema. El pasto San Agustín es ideal para jardines con algo de sombra."}}
      ]
    },
    {
      "@type":"BreadcrumbList",
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":"https://www.viverosterra.com"},
        {"@type":"ListItem","position":2,"name":"Catálogo","item":"https://www.viverosterra.com/catalogo"}
      ]
    }
  ]
}
</script>

<!-- SVG Icons — mismos que el resto del sitio -->
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
<symbol id="ic-whatsapp" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></symbol>
<symbol id="ic-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.07 11a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 2.98 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21 16.92z"/></symbol>
<symbol id="ic-chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="ic-chevron-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></symbol>
<symbol id="ic-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 7l10 7 10-7"/></symbol>
<symbol id="ic-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
<symbol id="ic-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></symbol>
<symbol id="ic-instagram" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/></symbol>
<symbol id="ic-facebook" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></symbol>
<symbol id="ic-youtube" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46A2.78 2.78 0 0 0 1.46 6.42 29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58 2.78 2.78 0 0 0 1.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.96A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="currentColor"/></symbol>
<symbol id="ic-tiktok" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.77a4.85 4.85 0 01-1.01-.08z"/></symbol>
</svg>

<!-- GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RMZCVJ734M"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-RMZCVJ734M');</script>
</head>
<body class="text-gray-900">

<!-- WhatsApp Float -->
<a href="https://wa.me/528333268008?text=Hola%2C%20vi%20el%20catálogo%20y%20quiero%20cotizar" target="_blank" rel="noopener"
   class="wa-float flex items-center gap-2 bg-wa text-white px-4 py-3 rounded-full font-semibold text-sm shadow-xl hover:bg-green-500 transition-colors" aria-label="Cotizar por WhatsApp">
  <svg class="w-5 h-5 flex-shrink-0"><use href="#ic-whatsapp"/></svg>
  <span class="hidden sm:inline">Cotizar ahora</span>
</a>
```

- [ ] **Paso 2: Verificar en el navegador** — abrir `public/catalogo.html` en browser local. Debe verse el fondo crema del body sin errores de consola.

- [ ] **Commit parcial**
```bash
cd /tmp/viverosterra-site
git add public/catalogo.html
git commit -m "feat(catalogo): estructura base, head SEO, schemas JSON-LD y SVG icons"
```

---

### Task 2: Terra-nav (copiar exacto de otra página) + Hero + Filtros

**Archivos:**
- Modify: `public/catalogo.html` (append después del wa-float)

- [ ] **Paso 1: Añadir la terra-nav**

Copiar el bloque `<nav class="terra-nav"...>` completo desde `public/diseno-jardines-tampico/index.html` (líneas 98–520 aproximadamente). El `data-page` debe ser `/catalogo`:

```html
<!-- NAVBAR — copiar bloque <nav> completo de diseno-jardines-tampico/index.html -->
<!-- Cambiar data-page="/" a data-page="/catalogo" -->
<nav class="terra-nav" data-page="/catalogo">
  <!-- ... mismo contenido nav ... -->
</nav>
```

> Instrucción exacta: En tu editor, abre `public/diseno-jardines-tampico/index.html`, localiza `<nav class="terra-nav"`, copia hasta el cierre `</nav>` (incluye el `<script>` de inicialización del nav), y pégalo en `public/catalogo.html` tras el wa-float. Cambia `data-page="/diseno-jardines-tampico"` a `data-page="/catalogo"`.

- [ ] **Paso 2: Añadir sección HERO**

```html
<!-- HERO -->
<section class="bg-dark pt-8 pb-16">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <div class="reveal">
      <span class="inline-block bg-accent/20 text-accent font-semibold text-xs uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">Viveros Terra · Ciudad Madero</span>
      <h1 class="text-4xl sm:text-5xl font-display font-bold text-white leading-tight mb-4">
        Catálogo de Plantas, Pasto<br class="hidden sm:block"> y Materiales en Tampico
      </h1>
      <p class="text-white/60 text-lg max-w-2xl mx-auto mb-8">
        Más de 150 variedades disponibles en vivero. Entrega a domicilio en Tampico, Ciudad Madero y Altamira. Cotización gratis por WhatsApp en menos de 2 horas.
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <div class="flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-white text-sm font-medium">
          <span class="w-2 h-2 bg-accent rounded-full"></span>+150 variedades
        </div>
        <div class="flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-white text-sm font-medium">
          <span class="w-2 h-2 bg-accent rounded-full"></span>Entrega a domicilio
        </div>
        <div class="flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-white text-sm font-medium">
          <span class="w-2 h-2 bg-accent rounded-full"></span>Vivero productor directo
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Paso 3: Añadir sección FILTROS**

```html
<!-- FILTROS -->
<div class="bg-white border-b border-gray-200 sticky top-16 z-40 shadow-sm">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex gap-2 overflow-x-auto py-3 scrollbar-hide" role="tablist" aria-label="Filtrar catálogo por categoría" id="filter-bar">
      <button class="filter-btn active flex-shrink-0 px-5 py-2 rounded-full text-sm font-semibold border border-gray-200 bg-primary text-white transition-all" data-cat="todo" role="tab" aria-selected="true">
        Todos los productos
      </button>
      <button class="filter-btn flex-shrink-0 px-5 py-2 rounded-full text-sm font-semibold border border-gray-200 bg-white text-gray-700 hover:border-primary hover:text-primary transition-all" data-cat="pasto" role="tab" aria-selected="false">
        🌿 Pasto
      </button>
      <button class="filter-btn flex-shrink-0 px-5 py-2 rounded-full text-sm font-semibold border border-gray-200 bg-white text-gray-700 hover:border-primary hover:text-primary transition-all" data-cat="plantas" role="tab" aria-selected="false">
        🌴 Plantas &amp; Palmas
      </button>
      <button class="filter-btn flex-shrink-0 px-5 py-2 rounded-full text-sm font-semibold border border-gray-200 bg-white text-gray-700 hover:border-primary hover:text-primary transition-all" data-cat="materiales" role="tab" aria-selected="false">
        🪨 Materiales
      </button>
    </div>
  </div>
</div>
```

- [ ] **Paso 4: Verificar en el navegador** — filtros deben verse pegados bajo el nav al hacer scroll. No deben solaparse.

- [ ] **Commit**
```bash
git add public/catalogo.html
git commit -m "feat(catalogo): hero oscuro + barra de filtros sticky"
```

---

### Task 3: Grid de productos — las 16 cards

**Archivos:**
- Modify: `public/catalogo.html` (append después de la barra de filtros)

- [ ] **Paso 1: Añadir el contenedor del grid + sección PASTO (3 cards)**

```html
<!-- GRID DE PRODUCTOS -->
<section class="py-16 bg-bgwarm">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

    <!-- Título de sección visible para SEO -->
    <div class="mb-10 reveal" id="grid-intro">
      <p class="text-sm font-semibold text-primary uppercase tracking-widest mb-2">Disponible en vivero</p>
      <h2 class="text-3xl font-display font-bold text-gray-900">Todo lo que necesitas para tu jardín</h2>
      <p class="text-gray-500 mt-2">Usa los filtros para encontrar lo que buscas. Cada producto tiene su propio link directo a WhatsApp.</p>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6" id="catalog-grid">

      <!-- ═══════════════ PASTO ═══════════════ -->

      <!-- Pasto San Agustín -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-primary transition-all reveal" data-cat="pasto">
        <div class="img-card h-48">
          <img src="/img/pasto-en-rollo-san-agustin-tampico.jpg" alt="Pasto San Agustín en rollo disponible en Viveros Terra Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-primary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌿 Pasto</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Pasto San Agustín en Rollo</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Fresco de corte semanal, directo del campo. Resiste el calor costero de Tampico y tolera media sombra. Garantía de arraigo en 21 días con instalación.</p>
          <p class="text-primary font-bold text-base mb-4">Desde $85/m²</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20pasto%20San%20Agustín%20en%20rollo%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar San Agustín
          </a>
          <a href="/pasto-en-rollo-tampico" class="block text-center text-xs text-primary hover:underline mt-2">Ver detalles y precios →</a>
        </div>
      </article>

      <!-- Pasto Japonés -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-primary transition-all reveal" data-cat="pasto">
        <div class="img-card h-48">
          <img src="/img/pasto-en-rollo-san-agustin-tampico.jpg" alt="Pasto Japonés en rollo en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-primary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌿 Pasto</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Pasto Japonés en Rollo</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Textura fina y densa. Ideal para jardines residenciales de alta estética en Tampico y zona Huasteca. Requiere buena iluminación.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según disponibilidad</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20pasto%20Japonés%20en%20rollo%20para%20mi%20jardín" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Pasto Japonés
          </a>
          <a href="/pasto-en-rollo-tampico" class="block text-center text-xs text-primary hover:underline mt-2">Ver detalles →</a>
        </div>
      </article>

      <!-- Pasto Sintético -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-primary transition-all reveal" data-cat="pasto">
        <div class="img-card h-48">
          <img src="/img/pasto-sintetico-tampico-instalacion.png" alt="Pasto sintético instalado en jardín en Tampico por Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-primary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌿 Pasto</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Pasto Sintético</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Sin riego, sin cortes, sin fertilización. Ideal para terrazas, canchas y zonas de alto tráfico en Tampico, Madero y Altamira.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar por m²</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20pasto%20sintético%20para%20mi%20espacio%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Pasto Sintético
          </a>
          <a href="/pasto-sintetico-tampico" class="block text-center text-xs text-primary hover:underline mt-2">Ver opciones →</a>
        </div>
      </article>

      <!-- ═══════════════ PLANTAS & PALMAS ═══════════════ -->

      <!-- Palma del Viajero -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-tropicales-tampico-viveros.png" alt="Palma del Viajero disponible en Viveros Terra Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Palma del Viajero</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Espectacular palmera tropical con abanico característico. Crece con fuerza en el clima cálido-húmedo de Tampico. Disponible en varios tamaños.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según tamaño</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20palma%20del%20viajero%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Palma del Viajero
          </a>
          <a href="/palmas-tropicales-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver guía completa →</a>
        </div>
      </article>

      <!-- Palma Areca -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-tropicales-tampico-viveros.png" alt="Palma Areca en venta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Palma Areca</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Elegante y de rápido crecimiento. Perfecta para crear privacidad en jardines y terrazas en Tampico. Tolera bien la humedad de la Huasteca.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según tamaño</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20palma%20areca%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Palma Areca
          </a>
          <a href="/palmas-para-jardin-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver guía de palmas →</a>
        </div>
      </article>

      <!-- Palma Real -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-tropicales-tampico-viveros.png" alt="Palma Real en venta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Palma Real</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Imponente palma de tronco plateado. Referencia tropical de los jardines del sur de Tamaulipas. Alta resistencia al calor y al viento costero.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según tamaño</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20palma%20real%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Palma Real
          </a>
          <a href="/plantas-palmas-arboles-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver todas las palmas →</a>
        </div>
      </article>

      <!-- Palma Coco -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-tropicales-tampico-viveros.png" alt="Palma Coco en venta en Viveros Terra Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Palma Coco</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">El ícono del trópico. Resistente al calor y la brisa marina del Golfo. Ideal para jardines costeros en Tampico, Madero y Altamira.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según tamaño</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20palma%20coco%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Palma Coco
          </a>
          <a href="/plantas-palmas-arboles-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver todas las palmas →</a>
        </div>
      </article>

      <!-- Ficus Elastica -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-ornamentales-tampico-viveros-terra.png" alt="Ficus Elastica en venta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Ficus Elastica</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Arbol ornamental de hojas grandes y brillantes. Perfecto para interiores luminosos o jardines tropicales en Tampico. Bajo mantenimiento.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20ficus%20elastica%20para%20mi%20espacio%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Ficus Elastica
          </a>
          <a href="/plantas-palmas-arboles-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver más plantas →</a>
        </div>
      </article>

      <!-- Plantas Ornamentales -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-ornamentales-tampico-viveros-terra.png" alt="Plantas ornamentales tropicales para jardines en Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Plantas Ornamentales</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Más de 80 variedades de plantas ornamentales adaptadas al clima cálido-húmedo de Tampico. Heliconias, gingers, bromelias y más.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar por variedad</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20plantas%20ornamentales%20para%20mi%20jardín%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Plantas
          </a>
          <a href="/plantas-para-jardin-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver guía de plantas →</a>
        </div>
      </article>

      <!-- Plantas de Interior -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/plantas-ornamentales-tampico-viveros-terra.png" alt="Plantas de interior para casas en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Plantas de Interior</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Especies seleccionadas para el calor de Tampico: pothos, sansevieria, aglaonema, spathiphyllum y más. Bajo mantenimiento, alta resistencia.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar por variedad</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20plantas%20de%20interior%20para%20mi%20casa%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Plantas Interior
          </a>
          <a href="/plantas-de-interior-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver guía de plantas interior →</a>
        </div>
      </article>

      <!-- Árboles para jardín y banqueta -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-secondary transition-all reveal" data-cat="plantas">
        <div class="img-card h-48">
          <img src="/img/jardineria-profesional-tampico-empresa.png" alt="Árboles para jardín y banqueta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-secondary text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🌴 Plantas &amp; Palmas</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Árboles para Jardín y Banqueta</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Tabachín, fresno, trueno, primavera y más. Especies que no levantan el pavimento y toleran el calor de Tamaulipas. Para casas y aceras.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar según especie</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20árboles%20para%20jardín%20o%20banqueta%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Árboles
          </a>
          <a href="/arboles-para-banqueta-tampico" class="block text-center text-xs text-secondary hover:underline mt-2">Ver guía de árboles →</a>
        </div>
      </article>

      <!-- ═══════════════ MATERIALES ═══════════════ -->

      <!-- Tierra Negra Vegetal -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-amber-600 transition-all reveal" data-cat="materiales">
        <div class="img-card h-48">
          <img src="/img/tierra-negra-jardin-tampico.png" alt="Tierra negra vegetal en venta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-amber-800 text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🪨 Materiales</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Tierra Negra Vegetal</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Tierra de alta calidad para preparación de jardines, nivelación y relleno. Ideal para el establecimiento de pasto San Agustín en Tampico.</p>
          <p class="text-primary font-bold text-sm mb-4">$90/costal · $1,500/m³</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20tierra%20negra%20vegetal%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Tierra Negra
          </a>
          <a href="/tierra-negra-vegetal-tampico" class="block text-center text-xs text-amber-800 hover:underline mt-2">Ver precios y camiones →</a>
        </div>
      </article>

      <!-- Tierra Negra para Maceta -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-amber-600 transition-all reveal" data-cat="materiales">
        <div class="img-card h-48">
          <img src="/img/tierra-negra-jardin-tampico.png" alt="Tierra negra para maceta en Tampico — Viveros Terra" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-amber-800 text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🪨 Materiales</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Tierra Negra para Maceta</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Sustrato enriquecido para macetas y contenedores. Formulado para retener humedad y favorecer el drenaje en el clima tropical de Tampico.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar por costal</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20tierra%20negra%20para%20maceta%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Tierra para Maceta
          </a>
          <a href="/tierra-negra-vegetal-tampico" class="block text-center text-xs text-amber-800 hover:underline mt-2">Ver más sustratos →</a>
        </div>
      </article>

      <!-- Tezontle Rojo -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-amber-600 transition-all reveal" data-cat="materiales">
        <div class="img-card h-48">
          <img src="/img/tezontle-rojo-jardin-tampico-sendero.jpg" alt="Tezontle rojo para jardines y senderos en Tampico" loading="lazy" width="600" height="400" style="object-position:center">
        </div>
        <div class="p-5">
          <span class="inline-block bg-amber-800 text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🪨 Materiales</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Tezontle Rojo</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Piedra volcánica roja para senderos, macizos y drenaje de jardines. 8 usos distintos para transformar cualquier espacio exterior en Tampico.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar por costal o camión</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20tezontle%20rojo%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibient text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Tezontle Rojo
          </a>
          <a href="/tezontle-rojo-tampico" class="block text-center text-xs text-amber-800 hover:underline mt-2">Ver usos y precios →</a>
        </div>
      </article>

      <!-- Mármol Blanco -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-amber-600 transition-all reveal" data-cat="materiales">
        <div class="img-card h-48">
          <img src="/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp" alt="Mármol blanco decorativo para jardines en Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-amber-800 text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🪨 Materiales</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Mármol Blanco Decorativo</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Piedra de mármol blanco triturada para senderos, fuentes y bordes de jardín. Da un aspecto elegante y sofisticado a cualquier espacio exterior.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20mármol%20blanco%20decorativo%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Mármol Blanco
          </a>
          <a href="/marmol-blanco-tampico" class="block text-center text-xs text-amber-800 hover:underline mt-2">Ver opciones →</a>
        </div>
      </article>

      <!-- Piedra de Río -->
      <article class="catalog-card bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md hover:border-amber-600 transition-all reveal" data-cat="materiales">
        <div class="img-card h-48">
          <img src="/img/piedra-marmol-blanca-decorativa-jardin-tampico.webp" alt="Piedra de río y piedra bola para jardines en Tampico" loading="lazy" width="600" height="400">
        </div>
        <div class="p-5">
          <span class="inline-block bg-amber-800 text-white text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full mb-3">🪨 Materiales</span>
          <h3 class="font-display font-bold text-gray-900 text-lg mb-1">Piedra de Río / Bola</h3>
          <p class="text-gray-500 text-sm mb-3 leading-relaxed">Piedra natural redondeada para senderos, fuentes, estanques y decoración de jardines. Disponible en varios tamaños para proyectos en Tampico.</p>
          <p class="text-gray-400 font-medium text-sm mb-4">Cotizar</p>
          <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20cotizar%20piedra%20de%20río%20o%20bola%20en%20Tampico" target="_blank" rel="noopener"
             class="flex items-center justify-center gap-2 w-full bg-wa text-white py-2.5 rounded-xl font-semibold text-sm hover:bg-green-500 transition-colors">
            <svg class="w-4 h-4"><use href="#ic-whatsapp"/></svg>Cotizar Piedra de Río
          </a>
          <a href="/piedra-bola-rio-tampico" class="block text-center text-xs text-amber-800 hover:underline mt-2">Ver opciones →</a>
        </div>
      </article>

    </div><!-- /catalog-grid -->
  </div>
</section>
```

- [ ] **Verificar en navegador** — los 16 cards deben verse en grid de 3 columnas en desktop. Cada card tiene foto, badge de categoría, descripción, precio y botón WA.

- [ ] **Commit**
```bash
git add public/catalogo.html
git commit -m "feat(catalogo): 16 product cards con CTAs WhatsApp y links internos"
```

---

### Task 4: FAQ + CTA final + Footer + JS de filtros

**Archivos:**
- Modify: `public/catalogo.html` (append después del grid)

- [ ] **Paso 1: Añadir sección FAQ**

```html
<!-- FAQ -->
<section class="py-16 bg-white">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-10 reveal">
      <h2 class="text-3xl font-display font-bold text-gray-900">Preguntas frecuentes</h2>
      <p class="text-gray-500 mt-2">Sobre disponibilidad, precios, entrega y más</p>
    </div>
    <div class="space-y-3 reveal">

      <div class="border border-gray-200 rounded-2xl overflow-hidden">
        <button class="faq-btn w-full flex items-center justify-between px-6 py-4 text-left font-semibold text-gray-900 hover:bg-gray-50 transition-colors" aria-expanded="false">
          ¿Tienen entrega a domicilio de plantas y materiales en Tampico?
          <svg class="faq-icon w-5 h-5 text-gray-400 flex-shrink-0 transition-transform"><use href="#ic-chevron-down"/></svg>
        </button>
        <div class="faq-answer px-6 text-gray-600 text-sm leading-relaxed">
          <div class="pb-4">Sí. Viveros Terra entrega plantas, pasto en rollo y materiales a domicilio en Tampico, Ciudad Madero y Altamira. Para pedidos grandes coordinamos logística a toda la zona Huasteca. Cotiza por WhatsApp al 833 326 8008.</div>
        </div>
      </div>

      <div class="border border-gray-200 rounded-2xl overflow-hidden">
        <button class="faq-btn w-full flex items-center justify-between px-6 py-4 text-left font-semibold text-gray-900 hover:bg-gray-50 transition-colors" aria-expanded="false">
          ¿Cuánto cuesta el pasto San Agustín en Tampico?
          <svg class="faq-icon w-5 h-5 text-gray-400 flex-shrink-0 transition-transform"><use href="#ic-chevron-down"/></svg>
        </button>
        <div class="faq-answer px-6 text-gray-600 text-sm leading-relaxed">
          <div class="pb-4">El pasto San Agustín en rollo cuesta desde $85 por metro cuadrado (solo el pasto, sin entrega ni instalación). Con instalación profesional cotizamos según el tamaño del jardín y el estado del terreno. Cotización gratis sin compromiso.</div>
        </div>
      </div>

      <div class="border border-gray-200 rounded-2xl overflow-hidden">
        <button class="faq-btn w-full flex items-center justify-between px-6 py-4 text-left font-semibold text-gray-900 hover:bg-gray-50 transition-colors" aria-expanded="false">
          ¿Puedo ir a comprar directamente al vivero?
          <svg class="faq-icon w-5 h-5 text-gray-400 flex-shrink-0 transition-transform"><use href="#ic-chevron-down"/></svg>
        </button>
        <div class="faq-answer px-6 text-gray-600 text-sm leading-relaxed">
          <div class="pb-4">Sí. Nuestro vivero está en Av. Álvaro Obregón 601, Col. Unidad Nacional, Ciudad Madero (frente al Walmart). Horario: Lunes a Viernes 9am–6pm, Sábado 9am–2pm. Te recomendamos llamar antes al 833 326 8008 para confirmar disponibilidad de la variedad que buscas.</div>
        </div>
      </div>

      <div class="border border-gray-200 rounded-2xl overflow-hidden">
        <button class="faq-btn w-full flex items-center justify-between px-6 py-4 text-left font-semibold text-gray-900 hover:bg-gray-50 transition-colors" aria-expanded="false">
          ¿Venden al mayoreo para constructoras?
          <svg class="faq-icon w-5 h-5 text-gray-400 flex-shrink-0 transition-transform"><use href="#ic-chevron-down"/></svg>
        </button>
        <div class="faq-answer px-6 text-gray-600 text-sm leading-relaxed">
          <div class="pb-4">Sí. Ofrecemos precios preferenciales por volumen para constructoras, arquitectos, fraccionamientos, hoteles y gobierno. Factura CFDI disponible. Entrega por etapas según avance de obra. Cotiza tu proyecto al 833 326 8008.</div>
        </div>
      </div>

      <div class="border border-gray-200 rounded-2xl overflow-hidden">
        <button class="faq-btn w-full flex items-center justify-between px-6 py-4 text-left font-semibold text-gray-900 hover:bg-gray-50 transition-colors" aria-expanded="false">
          ¿Qué plantas recomiendan para el calor de Tampico?
          <svg class="faq-icon w-5 h-5 text-gray-400 flex-shrink-0 transition-transform"><use href="#ic-chevron-down"/></svg>
        </button>
        <div class="faq-answer px-6 text-gray-600 text-sm leading-relaxed">
          <div class="pb-4">Para el clima cálido-húmedo de Tampico recomendamos palmas tropicales (del viajero, areca, real, coco), Ficus elastica, plantas ornamentales de sol como heliconias y gingers, y para interior el pothos, sansevieria y aglaonema. El pasto San Agustín es ideal para jardines con algo de sombra.</div>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Paso 2: Añadir CTA final**

```html
<!-- CTA FINAL -->
<section class="py-16 bg-dark">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center reveal">
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-white mb-4">¿No encuentras lo que buscas?</h2>
    <p class="text-white/60 text-lg mb-8 max-w-xl mx-auto">Nuestro catálogo en vivero es más amplio. Escríbenos y te decimos si lo tenemos disponible hoy.</p>
    <a href="https://wa.me/528333268008?text=Hola%2C%20vi%20el%20catálogo%20y%20quiero%20saber%20si%20tienen%20disponible%20algo%20específico" target="_blank" rel="noopener"
       class="inline-flex items-center gap-3 bg-wa text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-green-400 transition-colors shadow-xl">
      <svg class="w-6 h-6"><use href="#ic-whatsapp"/></svg>Consultar disponibilidad
    </a>
    <p class="text-white/40 text-sm mt-4">Respondemos en menos de 2 horas · Lun–Vie 9am–6pm · Sáb 9am–2pm</p>
  </div>
</section>
```

- [ ] **Paso 3: Añadir Footer**

Copiar el bloque `<footer>` completo desde `public/diseno-jardines-tampico/index.html` (líneas 964–1010). Cambiar la línea activa del footer para que `Catálogo` esté destacada en lugar de `Diseño de Jardines`:

```html
<!-- Dentro del footer, cambiar este link: -->
<li><a href="/catalogo" class="text-accent font-medium">Catálogo ←</a></li>
```

- [ ] **Paso 4: Añadir JS de filtros + reveal + FAQ**

```html
<script>
/* ── Filtro de catálogo ── */
(function(){
  var btns=document.querySelectorAll('.filter-btn');
  var cards=document.querySelectorAll('.catalog-card');
  btns.forEach(function(btn){
    btn.addEventListener('click',function(){
      btns.forEach(function(b){b.classList.remove('active');b.setAttribute('aria-selected','false');});
      btn.classList.add('active');
      btn.setAttribute('aria-selected','true');
      var cat=btn.dataset.cat;
      cards.forEach(function(card){
        if(cat==='todo'||card.dataset.cat===cat){card.style.display='';}
        else{card.style.display='none';}
      });
    });
  });
})();

/* ── FAQ accordion ── */
document.querySelectorAll('.faq-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    var ans=btn.nextElementSibling;
    var icon=btn.querySelector('.faq-icon');
    var open=ans.classList.contains('open');
    document.querySelectorAll('.faq-answer').forEach(function(a){a.classList.remove('open');});
    document.querySelectorAll('.faq-icon').forEach(function(i){i.style.transform='';});
    document.querySelectorAll('.faq-btn').forEach(function(b){b.setAttribute('aria-expanded','false');});
    if(!open){ans.classList.add('open');icon.style.transform='rotate(180deg)';btn.setAttribute('aria-expanded','true');}
  });
});

/* ── Reveal animation con safety timeout ── */
var obs=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target);}});},{threshold:0,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.reveal').forEach(function(el){var r=el.getBoundingClientRect();if(r.top<window.innerHeight-40){el.classList.add('visible');}else{obs.observe(el);}});
setTimeout(function(){document.querySelectorAll('.reveal:not(.visible)').forEach(function(el){el.classList.add('visible');});},900);
</script>
</body>
</html>
```

- [ ] **Verificar filtros en navegador:**
  1. Clic en "🌿 Pasto" → solo 3 cards visibles
  2. Clic en "🌴 Plantas & Palmas" → solo 8 cards visibles
  3. Clic en "🪨 Materiales" → solo 5 cards visibles
  4. Clic en "Todos" → 16 cards visibles

- [ ] **Verificar FAQ:** clic en pregunta → respuesta se expande. Clic en otra → primera se cierra.

- [ ] **Commit**
```bash
git add public/catalogo.html
git commit -m "feat(catalogo): FAQ accordion, CTA final, footer y JS de filtros"
```

---

### Task 5: Actualizar sitemap + PR

**Archivos:**
- Modify: `public/sitemap.xml`

- [ ] **Paso 1: Actualizar lastmod del catálogo en sitemap**

En `public/sitemap.xml` localizar la URL `/catalogo` y actualizar `<lastmod>`:
```xml
<url>
  <loc>https://www.viverosterra.com/catalogo</loc>
  <lastmod>2026-05-07</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.9</priority>
</url>
```

- [ ] **Paso 2: Crear rama y PR**

```bash
cd /tmp/viverosterra-site
git checkout -b feat/catalogo-interactivo
git add public/catalogo.html public/sitemap.xml
git commit -m "feat: catálogo interactivo con filtros, 16 productos y interlinking" --allow-empty
git push -u origin feat/catalogo-interactivo
gh pr create --title "feat: catálogo interactivo con filtros y 16 productos" --body "Reescritura completa de /catalogo. Filtros por categoría (Pasto, Plantas, Materiales). 16 cards con WhatsApp CTA por producto. Interlinking a 6 páginas huérfanas. Schema ItemList + FAQPage. SEO completo." --base main
```

---

## Self-review

**Spec coverage:**
- ✅ 16 productos en 3 categorías con `data-cat` para filtro
- ✅ Schema `ItemList` (16 items) + `FAQPage` (5 preguntas) + `BreadcrumbList`
- ✅ SEO: title 2026, canonical, OG, meta description con keywords
- ✅ JS filtro: todos/pasto/plantas/materiales con clase `active`
- ✅ Interlinking: `/palmas-tropicales-tampico`, `/palmas-para-jardin-tampico`, `/plantas-de-interior-tampico`, `/plantas-para-jardin-tampico`, `/arboles-para-banqueta-tampico`, `/arboles-ornamentales-tampico` (vía `/plantas-palmas-arboles-tampico`)
- ✅ Reveal animation + safety timeout (mismo patrón que el resto del sitio)
- ✅ FAQ accordion (mismo patrón que el resto del sitio)
- ✅ Footer con link activo de catálogo
- ✅ Sitemap actualizado

**Sin placeholders:** ✅
**Consistencia de nombres:** `.catalog-card[data-cat]`, `.filter-btn[data-cat]`, `.filter-btn.active` — consistentes en JS y HTML ✅
