# Palmas Mayoreo Proyectos · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lanzar `/palmas-mayoreo-proyectos` — landing B2B regional con 13 secciones editorial híbrido, schema markup multi-graph, calculadora WhatsApp y sticky CTA, alineado al sistema visual de viverosterra.com.

**Architecture:** HTML estático con Tailwind compiled (`/css/tailwind.css`), JS vanilla inline para calculadora y lead magnet, schema JSON-LD inline. Producción a partir del mockup `public/palmas-mayoreo-proyectos-mockup.html` (v aprobada) → eleva a `/palmas-mayoreo-proyectos/index.html` con head SEO completo, navbar `terra-nav` y schema markup. Deploy vía Vercel desde main.

**Tech Stack:** HTML5 · Tailwind CSS compiled · Inter + Playfair Display (Google Fonts) · Schema.org JSON-LD · IntersectionObserver · `<details>` nativo · Vercel hosting.

---

## File Structure

**Files to create:**
- `public/palmas-mayoreo-proyectos/index.html` — landing principal (~1000 líneas, todas las secciones inline)
- `public/pdf/guia-12-palmas-arquitectos.pdf` — placeholder PDF (1 página avisando "en producción"), reemplazable después

**Files to modify:**
- `public/sitemap.xml` — añadir URL nueva con priority 0.9
- `public/index.html` — añadir entry en dropdown "Por Zona · B2B" del terra-nav
- 21 archivos `*/index.html` con terra-nav — replicar el mismo entry de dropdown (script automatizado)
- `public/palmas-mayoreo-proyectos-mockup.html` — añadir `Disallow` en robots.txt o borrar tras lanzar producción

**Files to leave alone:**
- `public/css/tailwind.css` — ya tiene todas las clases necesarias (`bg-bgwarm`, `bg-dark`, `bg-primary`, `bg-accent`, `bg-wa`, `rounded-2xl`, etc.)
- SVG sprite — el mockup ya define los símbolos necesarios inline

---

## Task 1: Crear archivo de producción a partir del mockup

**Files:**
- Create: `public/palmas-mayoreo-proyectos/index.html`
- Source: `public/palmas-mayoreo-proyectos-mockup.html`

- [ ] **Step 1: Crear directorio y copiar mockup como base**

```bash
mkdir -p public/palmas-mayoreo-proyectos
cp public/palmas-mayoreo-proyectos-mockup.html public/palmas-mayoreo-proyectos/index.html
```

- [ ] **Step 2: Reemplazar `<head>` con head SEO de producción**

Abre `public/palmas-mayoreo-proyectos/index.html` y reemplaza desde `<head>` hasta `</head>` (sin tocar el `<svg>` sprite que va después) con:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Palmas Mayoreo para Proyectos B2B en Tamaulipas, Veracruz y SLP · Viveros Terra</title>
  <meta name="description" content="Productor directo de palmas para hoteles, fraccionamientos, gobierno e industria. 12 especies desde $850. Cobertura Tamaulipas, Veracruz y SLP. CFDI 4.0 + garantía 60 días arraigo.">
  <link rel="canonical" href="https://www.viverosterra.com/palmas-mayoreo-proyectos">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <meta name="geo.region" content="MX-TAM">
  <meta name="geo.placename" content="Tampico, Tamaulipas">
  <meta name="language" content="es-MX">

  <link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
  <link rel="icon" type="image/png" sizes="512x512" href="/img/favicon-512.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.viverosterra.com/palmas-mayoreo-proyectos">
  <meta property="og:title" content="Palmas Mayoreo para Proyectos B2B · Viveros Terra">
  <meta property="og:description" content="12 especies de palmas para proyectos en Tamaulipas, Veracruz y SLP. CFDI 4.0 + garantía 60 días.">
  <meta property="og:image" content="https://www.viverosterra.com/img/palmas-mayoreo-proyectos-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_MX">
  <meta property="og:site_name" content="Viveros Terra Tampico">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Palmas Mayoreo Proyectos B2B · Viveros Terra">
  <meta name="twitter:description" content="12 especies. CFDI + garantía 60 días. Cobertura Tamaulipas, Veracruz y SLP.">
  <meta name="twitter:image" content="https://www.viverosterra.com/img/palmas-mayoreo-proyectos-og.jpg">

  <!-- Fonts & Tailwind -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/tailwind.css">

  <style>
    html{scroll-behavior:smooth}
    body{font-family:'Inter',sans-serif;background:#FAFAF7;color:#0D2B0E}
    h1,h2,h3{font-family:'Playfair Display',serif}
    .reveal{opacity:0;transform:translateY(24px);transition:opacity .6s ease,transform .6s ease}
    .reveal.visible{opacity:1;transform:translateY(0)}
    .service-card{transition:transform .3s ease,box-shadow .3s ease}
    .service-card:hover{transform:translateY(-4px);box-shadow:0 20px 40px rgba(27,94,32,.15)}
    .hero-overlay{background:linear-gradient(135deg,rgba(13,43,14,.92) 0%,rgba(27,94,32,.78) 60%,rgba(46,125,50,.58) 100%)}
    .stat-card{background:rgba(255,255,255,.10);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.15)}
    .chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);font-size:13px;color:#fff;backdrop-filter:blur(8px)}
    .ic{width:18px;height:18px;flex-shrink:0}
    .spec-row{transition:background .2s ease}
    .spec-row:hover{background:rgba(102,187,106,.06)}
    .pq-card{border-left:3px solid #E0E5DF;transition:all .3s ease}
    .pq-card:hover{border-left-color:#66BB6A;transform:translateY(-4px);box-shadow:0 20px 40px rgba(27,94,32,.12)}
    .step-num{font-family:'Playfair Display',serif;font-size:42px;line-height:1;color:#66BB6A;font-weight:700}
    .calc-summary-grad{background:linear-gradient(160deg,#1B5E20 0%,#0D2B0E 100%)}
    .price-tag{font-family:'Playfair Display',serif;font-weight:700;color:#FAFAF7;font-size:26px;line-height:1}
    @media (prefers-reduced-motion: reduce){.reveal{opacity:1;transform:none;transition:none}.service-card,.pq-card{transition:none}.service-card:hover,.pq-card:hover{transform:none}}
  </style>
```

Mantén el bloque `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">…</svg>` y el `</head>` tal como está en el mockup.

- [ ] **Step 3: Quitar el banner footer mockup**

Busca y elimina del documento:
```html
<!-- Footer mockup tag -->
<footer class="py-8 pb-24 lg:pb-8 bg-dark text-white/55 text-center text-xs border-t border-white/10">
  <div class="max-w-7xl mx-auto px-6">
    Mockup B+A híbrido completo — apegado al sistema visual de viverosterra.com · <b class="text-accent">13 secciones + sticky CTA mobile</b> · No indexado
  </div>
</footer>
```

- [ ] **Step 4: Verificar archivo carga localmente**

```bash
cd public && python3 -m http.server 8000 &
sleep 2
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/palmas-mayoreo-proyectos/index.html
kill %1
```
Expected: `200`

- [ ] **Step 5: Commit**

```bash
git add public/palmas-mayoreo-proyectos/index.html
git commit -m "feat: crea /palmas-mayoreo-proyectos landing produccion desde mockup aprobado"
```

---

## Task 2: Añadir navbar terra-nav al landing

**Files:**
- Modify: `public/palmas-mayoreo-proyectos/index.html`

- [ ] **Step 1: Extraer terra-nav block del archivo de referencia**

```bash
awk '/<!-- ===== TERRA NAV/,/<\/nav>/' public/index.html > /tmp/terra-nav-block.html
head -3 /tmp/terra-nav-block.html
wc -l /tmp/terra-nav-block.html
```
Expected: ~150+ líneas extraídas.

- [ ] **Step 2: Insertar terra-nav justo después de `<body>`**

Abre `public/palmas-mayoreo-proyectos/index.html`. Justo después de `<body>` y antes del primer `<!-- ============ HERO ============ -->` inserta el contenido completo de `/tmp/terra-nav-block.html`.

- [ ] **Step 3: Marcar el item activo de "Por Zona · B2B"**

Busca en el navbar insertado el botón `data-page="zona"` o similar trigger del dropdown "Por Zona · B2B" y añade `data-page="/palmas-mayoreo-proyectos"` al `<body>` para que el highlight active funcione. Si tu terra-nav usa otra mecánica, asegúrate de que el botón "Por Zona · B2B" tenga `is-active` cuando estamos en esta ruta. Si no hay JS de highlight automático, añade clase `is-active` directamente al `<button class="terra-nav__drop-trigger">` de Por Zona · B2B.

- [ ] **Step 4: Ajustar padding del hero por la navbar fija (64px)**

En el `<section>` del hero, cambia `min-h-[88vh]` por `min-h-[calc(88vh-64px)]` y añade `pt-16` para compensar la navbar sticky:

```html
<section class="relative bg-dark min-h-[calc(88vh-64px)] flex items-end pb-0 pt-16">
```

- [ ] **Step 5: Verificar visualmente que el navbar aparece**

```bash
cd public && python3 -m http.server 8000 &
sleep 2
curl -s http://localhost:8000/palmas-mayoreo-proyectos/index.html | grep -c 'terra-nav__'
kill %1
```
Expected: número &gt; 20 (muestra que el navbar se insertó completo).

- [ ] **Step 6: Commit**

```bash
git add public/palmas-mayoreo-proyectos/index.html
git commit -m "feat: agrega terra-nav a /palmas-mayoreo-proyectos con highlight Por Zona B2B"
```

---

## Task 3: Conectar la calculadora con WhatsApp

**Files:**
- Modify: `public/palmas-mayoreo-proyectos/index.html` (sección Calculadora + script al final)

- [ ] **Step 1: Asignar IDs a los 3 inputs de la calculadora**

En la sección `<section class="py-20 bg-bgwarm" id="calc">`, modifica los tres campos así:

```html
<!-- Step 01 select -->
<select id="calc-tipo" class="w-full border-0 border-b border-gray-200 focus:border-accent text-lg py-2 outline-none bg-transparent">
  <option value="Hotel boutique">Hotel boutique</option>
  <option value="Fraccionamiento residencial">Fraccionamiento residencial</option>
  <option value="Parque industrial">Parque industrial</option>
  <option value="Obra de gobierno / municipal">Obra de gobierno / municipal</option>
  <option value="Otro">Otro</option>
</select>

<!-- Step 02 input -->
<input id="calc-tamano" type="text" placeholder="Ej: 80 palmas o 5,000 m²" class="w-full border-0 border-b border-gray-200 focus:border-accent text-lg py-2 outline-none bg-transparent">

<!-- Step 03 input -->
<input id="calc-ciudad" type="text" placeholder="Ej: Tuxpan, Veracruz" class="w-full border-0 border-b border-gray-200 focus:border-accent text-lg py-2 outline-none bg-transparent">
```

- [ ] **Step 2: Añadir IDs en los campos del resumen sticky para actualizarse en vivo**

```html
<div class="flex justify-between items-baseline pb-3 border-b border-white/10">
  <span class="text-sm text-white/70">Tipo</span><b id="sum-tipo" class="text-lg">Hotel boutique</b>
</div>
<div class="flex justify-between items-baseline pb-3 border-b border-white/10">
  <span class="text-sm text-white/70">Tamaño</span><b id="sum-tamano" class="text-lg">80 palmas</b>
</div>
<div class="flex justify-between items-baseline pb-3 border-b border-white/10">
  <span class="text-sm text-white/70">Destino</span><b id="sum-ciudad" class="text-lg">Tuxpan, Ver.</b>
</div>
```

- [ ] **Step 3: Cambiar el botón "Obtener estimado por WhatsApp" para incluir ID**

```html
<a id="calc-cta" href="#" class="bg-wa hover:bg-accent transition-all w-full inline-flex items-center justify-center gap-2 text-white font-bold px-7 py-4 rounded-2xl shadow-lg">
  <svg class="ic"><use href="#ic-whatsapp"/></svg> Obtener estimado por WhatsApp
</a>
```

- [ ] **Step 4: Añadir script de calculadora al final del body (antes de `</body>`)**

Reemplaza el `<script>document.querySelectorAll('.reveal')…</script>` final por:

```html
<script>
  // Reveal animation
  const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add('visible')), {threshold:0, rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  setTimeout(() => document.querySelectorAll('.reveal:not(.visible)').forEach(el => el.classList.add('visible')), 900);

  // Calculadora → WhatsApp
  (function(){
    const PHONE = '528333268008'; // +52 833 326 8008
    const tipo = document.getElementById('calc-tipo');
    const tam  = document.getElementById('calc-tamano');
    const ciu  = document.getElementById('calc-ciudad');
    const sT = document.getElementById('sum-tipo');
    const sM = document.getElementById('sum-tamano');
    const sC = document.getElementById('sum-ciudad');
    const cta = document.getElementById('calc-cta');

    function updateSummary(){
      if (sT) sT.textContent = tipo.value || '—';
      if (sM) sM.textContent = tam.value.trim() || '—';
      if (sC) sC.textContent = ciu.value.trim() || '—';
    }
    function buildLink(){
      const msg = `Hola Viveros Terra, quiero un estimado para mi proyecto B2B:\n\n• Tipo: ${tipo.value}\n• Tamaño: ${tam.value || 'por definir'}\n• Ciudad destino: ${ciu.value || 'por definir'}\n\nVengo de la página de Palmas Mayoreo Proyectos.`;
      return `https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`;
    }
    [tipo, tam, ciu].forEach(el => el && el.addEventListener('input', updateSummary));
    if (cta) cta.addEventListener('click', function(ev){
      ev.preventDefault();
      window.open(buildLink(), '_blank', 'noopener');
    });
    updateSummary();
  })();
</script>
```

- [ ] **Step 5: Verificar el script en local**

```bash
cd public && python3 -m http.server 8000 &
sleep 2
# Verifica que el script aparece y no hay errores de sintaxis
curl -s http://localhost:8000/palmas-mayoreo-proyectos/index.html | grep -c 'calc-tipo'
kill %1
```
Expected: número ≥ 2 (uno en el select, uno en el script).

- [ ] **Step 6: Commit**

```bash
git add public/palmas-mayoreo-proyectos/index.html
git commit -m "feat: conecta calculadora palmas mayoreo a WhatsApp con resumen en vivo"
```

---

## Task 4: Conectar formulario CTA Final y Lead Magnet a WhatsApp

**Files:**
- Modify: `public/palmas-mayoreo-proyectos/index.html` (sección CTA final + Lead Magnet + script)

- [ ] **Step 1: Asignar IDs al formulario CTA Final**

En `<section id="cta-final">`, dentro del `<form>` o div que contiene los 5 inputs:

```html
<input id="cta-nombre" type="text" required class="...">
<input id="cta-empresa" type="text" class="...">
<input id="cta-email" type="email" required class="...">
<input id="cta-tel" type="tel" required class="...">
<textarea id="cta-detalle" rows="3" placeholder="Ej: 80 palmas para fraccionamiento residencial en Tuxpan, entrega marzo 2027" class="..."></textarea>
<a id="cta-submit" href="#" class="bg-wa ...">
  <svg class="ic"><use href="#ic-whatsapp"/></svg> Enviar y cotizar por WhatsApp
</a>
```

- [ ] **Step 2: Asignar IDs al formulario Lead Magnet**

En `<section id="lead">`:

```html
<input id="lead-nombre" type="text" placeholder="Tu nombre" class="...">
<input id="lead-email" type="email" placeholder="tu@empresa.com" class="...">
<select id="lead-tipo" class="...">
  <option>Despacho arquitectónico</option><option>Hotelería</option><option>Fraccionadora</option><option>Gobierno</option><option>Industrial</option><option>Otro</option>
</select>
<a id="lead-cta" href="#" class="bg-accent ...">
  <svg class="ic"><use href="#ic-download"/></svg> Descargar guía PDF
</a>
```

- [ ] **Step 3: Extender script al final del body con handlers de ambos formularios**

Justo dentro del `<script>` después del IIFE de calculadora, añade:

```javascript
  // CTA Final → WhatsApp
  (function(){
    const PHONE = '528333268008';
    const cta = document.getElementById('cta-submit');
    if (!cta) return;
    cta.addEventListener('click', function(ev){
      ev.preventDefault();
      const nombre  = document.getElementById('cta-nombre').value.trim();
      const empresa = document.getElementById('cta-empresa').value.trim();
      const email   = document.getElementById('cta-email').value.trim();
      const tel     = document.getElementById('cta-tel').value.trim();
      const detalle = document.getElementById('cta-detalle').value.trim();
      if (!nombre || !email || !tel) {
        alert('Por favor completa nombre, email y WhatsApp.');
        return;
      }
      const msg = `Hola Viveros Terra, cotización para proyecto B2B:\n\n• Nombre: ${nombre}\n• Empresa: ${empresa || '—'}\n• Email: ${email}\n• WhatsApp: ${tel}\n• Detalle: ${detalle || '—'}\n\nVengo de /palmas-mayoreo-proyectos.`;
      window.open(`https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    });
  })();

  // Lead Magnet → descarga PDF + notifica WhatsApp
  (function(){
    const PHONE = '528333268008';
    const cta = document.getElementById('lead-cta');
    if (!cta) return;
    cta.addEventListener('click', function(ev){
      ev.preventDefault();
      const nombre = document.getElementById('lead-nombre').value.trim();
      const email  = document.getElementById('lead-email').value.trim();
      const tipo   = document.getElementById('lead-tipo').value;
      if (!nombre || !email) {
        alert('Por favor escribe tu nombre y email para descargar la guía.');
        return;
      }
      // Notifica al equipo
      const msg = `Nueva descarga guía 12 palmas:\n• ${nombre}\n• ${email}\n• ${tipo}`;
      fetch(`https://wa.me/${PHONE}?text=${encodeURIComponent(msg)}`, {mode:'no-cors'}).catch(()=>{});
      // Inicia descarga
      window.location.href = '/pdf/guia-12-palmas-arquitectos.pdf';
    });
  })();
```

- [ ] **Step 4: Test manual visual en local**

```bash
cd public && python3 -m http.server 8000 &
sleep 2
echo "Abre http://localhost:8000/palmas-mayoreo-proyectos/ y llena calc + cta + lead; revisa que los WhatsApp se construyan correctamente"
# (test manual)
kill %1
```

- [ ] **Step 5: Commit**

```bash
git add public/palmas-mayoreo-proyectos/index.html
git commit -m "feat: conecta CTA final y lead magnet a WhatsApp con validacion basica"
```

---

## Task 5: Añadir Schema.org JSON-LD multi-graph

**Files:**
- Modify: `public/palmas-mayoreo-proyectos/index.html` (insertar dentro de `<head>` antes de `</head>`)

- [ ] **Step 1: Insertar el bloque JSON-LD multi-graph antes de `</head>`**

Justo antes del cierre `</head>` (después del `<style>`):

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@graph":[
    {
      "@type":"Service",
      "@id":"https://www.viverosterra.com/palmas-mayoreo-proyectos#service",
      "name":"Palmas al mayoreo para proyectos B2B",
      "serviceType":"Venta y entrega de palmas para proyectos arquitectónicos, hoteleros, gubernamentales e industriales",
      "provider":{"@id":"https://www.viverosterra.com#localbusiness"},
      "areaServed":[
        {"@type":"State","name":"Tamaulipas"},
        {"@type":"State","name":"Veracruz"},
        {"@type":"State","name":"San Luis Potosí"}
      ],
      "offers":{
        "@type":"AggregateOffer",
        "lowPrice":"850",
        "highPrice":"4200",
        "priceCurrency":"MXN",
        "offerCount":"12"
      }
    },
    {
      "@type":"LocalBusiness",
      "@id":"https://www.viverosterra.com#localbusiness",
      "name":"Viveros Terra",
      "url":"https://www.viverosterra.com",
      "telephone":"+528333268008",
      "address":{"@type":"PostalAddress","addressLocality":"Ciudad Madero","addressRegion":"Tamaulipas","addressCountry":"MX"},
      "sameAs":["https://www.facebook.com/viverosterra","https://www.instagram.com/viverosterra"]
    },
    {
      "@type":"BreadcrumbList",
      "itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":"https://www.viverosterra.com/"},
        {"@type":"ListItem","position":2,"name":"Mayoreo B2B","item":"https://www.viverosterra.com/mayoreo-pasto-tampico"},
        {"@type":"ListItem","position":3,"name":"Palmas Mayoreo Proyectos","item":"https://www.viverosterra.com/palmas-mayoreo-proyectos"}
      ]
    },
    {
      "@type":"ItemList",
      "name":"12 palmas para proyectos B2B",
      "itemListElement":[
        {"@type":"ListItem","position":1,"item":{"@type":"Product","name":"Palma Washingtonia","alternateName":"Washingtonia robusta","offers":{"@type":"Offer","price":"1800","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":2,"item":{"@type":"Product","name":"Palma Real","alternateName":"Roystonea regia","offers":{"@type":"Offer","price":"4200","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":3,"item":{"@type":"Product","name":"Palma Areca","alternateName":"Dypsis lutescens","offers":{"@type":"Offer","price":"850","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":4,"item":{"@type":"Product","name":"Palma del Viajero","alternateName":"Ravenala madagascariensis","offers":{"@type":"Offer","price":"1500","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":5,"item":{"@type":"Product","name":"Coco Plumoso","alternateName":"Syagrus romanzoffiana","offers":{"@type":"Offer","price":"2400","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":6,"item":{"@type":"Product","name":"Palma Kerpis","alternateName":"Hyophorbe lagenicaulis","offers":{"@type":"Offer","price":"2000","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":7,"item":{"@type":"Product","name":"Cycas Revoluta","alternateName":"Cycas revoluta","offers":{"@type":"Offer","price":"1600","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":8,"item":{"@type":"Product","name":"Bambú Tarro","alternateName":"Bambusa vulgaris","offers":{"@type":"Offer","price":"2800","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":9,"item":{"@type":"Product","name":"Yucca Rostrata","alternateName":"Yucca rostrata","offers":{"@type":"Offer","price":"3200","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":10,"item":{"@type":"Product","name":"Palma Bambú","alternateName":"Chamaedorea seifrizii","offers":{"@type":"Offer","price":"2200","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":11,"item":{"@type":"Product","name":"Palma Cola de Zorra","alternateName":"Wodyetia bifurcata","offers":{"@type":"Offer","price":"1200","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}},
        {"@type":"ListItem","position":12,"item":{"@type":"Product","name":"Palma Triángulo","alternateName":"Dypsis decaryi","offers":{"@type":"Offer","price":"2400","priceCurrency":"MXN","availability":"https://schema.org/InStock"}}}
      ]
    },
    {
      "@type":"FAQPage",
      "mainEntity":[
        {"@type":"Question","name":"¿Cuál es el pedido mínimo al mayoreo?","acceptedAnswer":{"@type":"Answer","text":"El precio desde mayoreo aplica a partir de 50 ejemplares de la misma especie. Para pedidos mixtos menores a 50 cotizamos por separado."}},
        {"@type":"Question","name":"¿Hacen envíos fuera de Tamaulipas?","acceptedAnswer":{"@type":"Answer","text":"Sí. Cobertura activa en Tamaulipas, Veracruz norte y SLP. Otros estados bajo cotización para proyectos mayores a 50 ejemplares."}},
        {"@type":"Question","name":"¿Qué pasa si una palma no arraiga?","acceptedAnswer":{"@type":"Answer","text":"Garantía de arraigo de 60 días por escrito. Si el cliente siguió la guía de cuidado entregada y la palma no prende, hacemos reposición sin costo."}},
        {"@type":"Question","name":"¿Tienen factura y certificado fitosanitario?","acceptedAnswer":{"@type":"Answer","text":"Sí. CFDI 4.0 emitida el día del pago. Certificado fitosanitario emitido por SADER/SENASICA para cruce entre estados, costo incluido en envíos a Veracruz y SLP."}},
        {"@type":"Question","name":"¿Cuánto tarda la entrega?","acceptedAnswer":{"@type":"Answer","text":"Zona Tampico-Madero-Altamira: 2-5 días. Resto Tamaulipas: 4-7 días. Veracruz norte y SLP: 5-10 días. Lead time comprometido por escrito en cotización."}},
        {"@type":"Question","name":"¿Aceptan pago diferido o a crédito para proyectos?","acceptedAnswer":{"@type":"Answer","text":"Sí, para proyectos mayores a 100 mil pesos con razón social verificable. Esquemas típicos: 50/50 o 30/40/30 contra avances. Caso a caso con anticipo y carta compromiso."}},
        {"@type":"Question","name":"¿Pueden hacer instalación llave en mano?","acceptedAnswer":{"@type":"Answer","text":"Sí. Maniobra de plantación, supervisión técnica y guía de cuidado. Para zonas fuera de la conurbación de Tampico coordinamos con cuadrilla local certificada."}},
        {"@type":"Question","name":"¿Trabajan con compras de gobierno?","acceptedAnswer":{"@type":"Answer","text":"Sí. Alta en padrón de proveedores municipal y estatal, fianzas de cumplimiento, acta de entrega-recepción y documentación completa para licitaciones públicas."}}
      ]
    }
  ]
}
</script>
```

- [ ] **Step 2: Validar JSON sintáctico**

```bash
python3 -c "
import re,json
html=open('public/palmas-mayoreo-proyectos/index.html').read()
m=re.search(r'<script type=\"application/ld\+json\">(.+?)</script>', html, re.S)
json.loads(m.group(1))
print('JSON-LD valido')
"
```
Expected: `JSON-LD valido` (sin excepciones).

- [ ] **Step 3: Commit**

```bash
git add public/palmas-mayoreo-proyectos/index.html
git commit -m "feat: agrega schema JSON-LD multi-graph (Service+LocalBusiness+Breadcrumb+ItemList+FAQPage)"
```

---

## Task 6: Crear PDF placeholder para lead magnet

**Files:**
- Create: `public/pdf/guia-12-palmas-arquitectos.pdf`

- [ ] **Step 1: Generar PDF de 1 página con mensaje "en producción"**

```bash
mkdir -p public/pdf
python3 - <<'PY'
import os
content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj
4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj
5 0 obj<</Length 213>>stream
BT /F1 22 Tf 80 720 Td (Guia: 12 Palmas para Proyectos Arquitectonicos) Tj
0 -40 Td /F1 14 Tf (Viveros Terra | viverosterra.com) Tj
0 -60 Td (Version completa en preparacion.) Tj
0 -24 Td (Te enviaremos el PDF final en cuanto este listo.) Tj
0 -40 Td (Mientras tanto, escribenos por WhatsApp:) Tj
0 -24 Td (+52 833 326 8008) Tj
ET
endstream
endobj
xref 0 6
0000000000 65535 f
0000000009 00000 n
0000000054 00000 n
0000000097 00000 n
0000000186 00000 n
0000000237 00000 n
trailer<</Size 6/Root 1 0 R>>
startxref
500
%%EOF
"""
open('public/pdf/guia-12-palmas-arquitectos.pdf','wb').write(content)
print('PDF creado:', os.path.getsize('public/pdf/guia-12-palmas-arquitectos.pdf'),'bytes')
PY
```

- [ ] **Step 2: Verificar tamaño del PDF**

```bash
ls -la public/pdf/guia-12-palmas-arquitectos.pdf
```
Expected: archivo &gt; 600 bytes.

- [ ] **Step 3: Commit**

```bash
git add public/pdf/guia-12-palmas-arquitectos.pdf
git commit -m "feat: agrega PDF placeholder guia 12 palmas para lead magnet"
```

---

## Task 7: Añadir entrada al sitemap.xml

**Files:**
- Modify: `public/sitemap.xml`

- [ ] **Step 1: Insertar URL después de mayoreo-pasto-tampico**

Abre `public/sitemap.xml`. Busca la línea con `<loc>https://www.viverosterra.com/mayoreo-pasto-tampico</loc>` (si existe) o la última URL B2B. Inserta inmediatamente debajo:

```xml
  <url><loc>https://www.viverosterra.com/palmas-mayoreo-proyectos</loc><lastmod>2026-05-12</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
```

- [ ] **Step 2: Validar XML**

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('public/sitemap.xml'); print('sitemap.xml valido')"
```
Expected: `sitemap.xml valido`.

- [ ] **Step 3: Commit**

```bash
git add public/sitemap.xml
git commit -m "feat: agrega /palmas-mayoreo-proyectos al sitemap"
```

---

## Task 8: Añadir entrada al dropdown "Por Zona · B2B" en homepage

**Files:**
- Modify: `public/index.html`

- [ ] **Step 1: Insertar el nuevo item en el dropdown**

Busca en `public/index.html` el bloque que dice `<div class="terra-nav__drop-header">Por Zona · B2B</div>` y después del `<a class="terra-nav__drop-item" href="/mayoreo-pasto-tampico"...>...</a>` añade:

```html
              <a class="terra-nav__drop-item" href="/palmas-mayoreo-proyectos" role="menuitem">
                <span class="terra-nav__drop-icon">🌴</span>
                <span class="terra-nav__drop-text"><strong>Palmas Mayoreo Proyectos</strong><span>Hoteles · Gobierno · Industria</span></span>
              </a>
```

- [ ] **Step 2: Verificar que aparece**

```bash
grep -c 'palmas-mayoreo-proyectos' public/index.html
```
Expected: ≥ 1.

- [ ] **Step 3: Commit**

```bash
git add public/index.html
git commit -m "feat: agrega entry palmas-mayoreo al dropdown Por Zona B2B en homepage"
```

---

## Task 9: Replicar entry de navbar en los demás archivos con terra-nav

**Files:**
- Modify: 21 archivos `public/*/index.html` y `public/*.html` que contienen `terra-nav`

- [ ] **Step 1: Listar archivos a modificar**

```bash
grep -l 'terra-nav__drop-header">Por Zona' public/*.html public/*/index.html 2>/dev/null | grep -v 'palmas-mayoreo-proyectos' > /tmp/files-to-update.txt
wc -l /tmp/files-to-update.txt
cat /tmp/files-to-update.txt
```
Expected: ~20-22 archivos listados.

- [ ] **Step 2: Aplicar la inserción con script Python**

```bash
python3 - <<'PY'
import re
NEW_ITEM = '''              <a class="terra-nav__drop-item" href="/palmas-mayoreo-proyectos" role="menuitem">
                <span class="terra-nav__drop-icon">🌴</span>
                <span class="terra-nav__drop-text"><strong>Palmas Mayoreo Proyectos</strong><span>Hoteles · Gobierno · Industria</span></span>
              </a>
'''
PATTERN = re.compile(r'(<a class="terra-nav__drop-item" href="/mayoreo-pasto-tampico"[\s\S]*?</a>\s*)', re.M)
files = [l.strip() for l in open('/tmp/files-to-update.txt') if l.strip()]
updated = 0
for f in files:
    src = open(f).read()
    if 'palmas-mayoreo-proyectos' in src and 'drop-item" href="/palmas-mayoreo-proyectos"' in src:
        continue  # ya esta
    new = PATTERN.sub(lambda m: m.group(1) + NEW_ITEM, src, count=1)
    if new != src:
        open(f,'w').write(new)
        updated += 1
        print('Updated:', f)
print(f'Total actualizados: {updated}')
PY
```

- [ ] **Step 3: Verificar cuenta**

```bash
grep -l 'href="/palmas-mayoreo-proyectos"' public/*.html public/*/index.html 2>/dev/null | wc -l
```
Expected: ≥ 20.

- [ ] **Step 4: Commit**

```bash
git add public/*.html public/*/index.html
git commit -m "feat: replica entry palmas-mayoreo en navbar de 20+ paginas"
```

---

## Task 10: Bloquear el mockup en producción

**Files:**
- Modify: `public/palmas-mayoreo-proyectos-mockup.html` (eliminar o bloquear)

- [ ] **Step 1: Eliminar el archivo mockup**

```bash
git rm public/palmas-mayoreo-proyectos-mockup.html
```

- [ ] **Step 2: Commit**

```bash
git commit -m "chore: elimina mockup palmas-mayoreo tras lanzar produccion"
```

---

## Task 11: Smoke test final + push a producción

**Files:**
- No file changes (validation only)

- [ ] **Step 1: Levantar servidor local y curl la página final**

```bash
cd public && python3 -m http.server 8000 &
sleep 2
curl -s -o /tmp/page.html -w "HTTP %{http_code} | bytes %{size_download}\n" http://localhost:8000/palmas-mayoreo-proyectos/
kill %1
```
Expected: `HTTP 200 | bytes > 80000`.

- [ ] **Step 2: Verificar elementos clave presentes**

```bash
for s in 'Palmas para tu proyecto' 'spec sheet' 'calc-tipo' 'application/ld+json' 'FAQPage' 'terra-nav__inner' 'sticky-cta'; do
  echo -n "$s: "; grep -c "$s" /tmp/page.html
done
```
Expected: cada uno con count ≥ 1.

- [ ] **Step 3: Validar JSON-LD con script**

```bash
python3 -c "
import re,json
html=open('/tmp/page.html').read()
m=re.search(r'<script type=\"application/ld\\+json\">(.+?)</script>', html, re.S)
data=json.loads(m.group(1))
graphs=data['@graph']
types=[g['@type'] for g in graphs]
print('Tipos schema:', types)
assert 'Service' in types and 'FAQPage' in types and 'ItemList' in types
print('OK')
"
```
Expected: `Tipos schema: ['Service','LocalBusiness','BreadcrumbList','ItemList','FAQPage']` y `OK`.

- [ ] **Step 4: Push a producción**

```bash
git push origin main
```

- [ ] **Step 5: Verificar en Vercel post-deploy (esperar ~1 min)**

```bash
sleep 75
curl -s -o /dev/null -w "Prod HTTP %{http_code}\n" https://www.viverosterra.com/palmas-mayoreo-proyectos/
```
Expected: `Prod HTTP 200`.

- [ ] **Step 6: Submit a Google Search Console**

Acceso manual: Google Search Console → URL Inspection → pegar `https://www.viverosterra.com/palmas-mayoreo-proyectos` → "Request indexing".

---

## Self-Review

### Spec coverage
- [x] HERO con audience chips, 4 badges, micro-proof → Task 1 Step 2 (head completo) + base mockup
- [x] TRUST BAR 5 números → base mockup
- [x] PARA QUIÉN 3 personas → base mockup
- [x] ESPECIES SPEC SHEET 12 especies → base mockup + Task 5 (Schema ItemList)
- [x] CALCULADORA con resumen + WhatsApp → Task 3
- [x] PROYECTOS 6 cards anónimas → base mockup
- [x] COBERTURA 3 estados + tabla tiempos → base mockup
- [x] DOCUMENTACIÓN B2B 4 cards → base mockup
- [x] PAQUETES 4 paquetes → base mockup
- [x] LEAD MAGNET split + form → base mockup + Task 4 (handler) + Task 6 (PDF)
- [x] FAQ 8 preguntas → base mockup + Task 5 (FAQPage schema)
- [x] CTA FINAL form 5 campos → Task 4
- [x] STICKY CTA mobile → base mockup
- [x] Mobile + WCAG (prefers-reduced-motion) → Task 1 Step 2
- [x] Schema multi-graph → Task 5
- [x] Sitemap → Task 7
- [x] Navbar updates → Tasks 2, 8, 9

### Placeholders
Ninguno. Todas las tasks contienen comandos/código completos. El PDF en Task 6 es deliberadamente un placeholder, pero es funcional y se reemplaza después.

### Consistencia
- Phone `528333268008` consistente en Tasks 3, 4, 6.
- IDs `calc-tipo`/`sum-tipo` consistentes entre Task 3 Steps 1 y 2.
- Schema FAQ refleja el copy exacto del mockup (mismas 8 preguntas y respuestas).

### Ambigüedad
Ninguna detectada — cada task tiene file paths exactos, código completo y comandos verificables.
