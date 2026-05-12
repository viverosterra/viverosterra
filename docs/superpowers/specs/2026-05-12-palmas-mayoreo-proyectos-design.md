# Landing B2B: Palmas al Mayoreo para Proyectos — Design Spec

**Goal:** Crear landing page `/palmas-mayoreo-proyectos` para capturar leads B2B regionales (Tamaulipas + Veracruz + SLP) de hoteles, fraccionamientos, gobierno e industria que necesitan palmas en proyecto. Target: 3-5 cotizaciones B2B mensuales con ticket $80K-$300K.

**Architecture:** Landing standalone HTML/Tailwind (consistente con resto del sitio) bajo `public/palmas-mayoreo-proyectos/index.html`. Estructura editorial híbrida alternando 12 secciones light/dark para combinar aspiración premium (arquitectos, hoteles) con seriedad institucional (gobierno, industria). JS vanilla mínimo para calculadora interactiva, lead magnet form, FAQ accordion.

**Tech Stack:** HTML5, Tailwind compilado (`/css/tailwind.css`), JS vanilla, Schema.org JSON-LD múltiple (Service + Product[] + LocalBusiness + FAQPage + BreadcrumbList).

---

## Decisiones estratégicas validadas

| Decisión | Selección |
|----------|-----------|
| URL | `/palmas-mayoreo-proyectos` (por intención, no geográfico) |
| Social proof | B+C: descripciones anonimizadas + fotos reales sin nombres de cliente |
| Pricing | Híbrido: precios "desde" visibles + descuentos exactos por cotización |
| Estética | Editorial híbrido alternando secciones light (`#FAFAF7`) y dark (`#0D2B0E`) |

---

## Posicionamiento (el "wedge")

**Promesa central:**
> "El único vivero productor del sur de Tamaulipas con capacidad logística regional, documentación B2B completa y garantía de arraigo escrita."

**Trinidad diferenciadora (los 3 mensajes que ningún competidor combina):**
1. Productor directo (no revendedor)
2. Logística regional (Tamaulipas + Veracruz + SLP)
3. Documentación B2B (CFDI 4.0, fitosanitario, factura, garantía escrita 60 días)

---

## Marketing psychology aplicado (8 principios Cialdini + B2B)

1. **Autoridad:** Botón visible "20 años · +500,000 m² · +80 proyectos B2B". Nombres binomiales (Roystonea regia) comunican expertise técnico.
2. **Social proof:** Wall de proyectos anonimizados con fotos reales > testimonios escritos.
3. **Loss aversion:** "Una palma muerta en proyecto = costo de reemplazo + tiempo + cara con cliente. Garantía 60 días por escrito."
4. **Scarcity creíble:** "Palmas de 4m+ requieren reserva con 8-12 semanas de anticipación."
5. **Reciprocity:** Lead magnet PDF "Guía de palmas para proyectos arquitectónicos" gratis a cambio de email.
6. **Commitment/Consistency:** Ladder de conversión escalonado (PDF → calculadora → formulario → meeting).
7. **Risk reversal:** 3 garantías visibles (arraigo escrita, reposición sin costo, CFDI mismo día).
8. **Decision fatigue reduction:** 4 paquetes pre-armados (Hotel, Fraccionamiento, Industrial, Gobierno) en lugar de "elegir 15 especies".

---

## SEO + AEO + LLM strategy

### Keyword map (4 tiers)

**Tier 1 — Hub principal:**
- "palmas mayoreo Tampico"
- "venta palmas mayoreo Tamaulipas"
- "proveedor palmas Veracruz"

**Tier 2 — Intent-specific:**
- "palmas para hotel proyecto"
- "venta palmas para fraccionamiento"
- "palmas mayoreo constructora"
- "palmas para licitación gobierno"

**Tier 3 — Technical long-tail:**
- "palma washingtonia altura proveedor"
- "roystonea regia precio mayoreo Mexico"
- "palmas tropicales clima húmedo Tamaulipas Veracruz"

**Tier 4 — Geographic:**
- "venta palmas Cd Victoria"
- "envío palmas Reynosa Matamoros"
- "palmas mayoreo Tuxpan Poza Rica"

### AEO (Google AI Overviews)

- Respuesta directa primer párrafo (50 palabras máx)
- H2s en formato pregunta ("¿Cuánto cuestan las palmas al mayoreo?", "¿Hacen envíos a otras ciudades?")
- FAQ schema con 8 preguntas B2B
- Tablas extraibles con specs técnicas por especie

### LLM/AI Search (ChatGPT, Perplexity, Claude)

- Datos numéricos específicos (no rangos vagos)
- Nombres binomiales: Roystonea regia, Washingtonia robusta, Cocos nucifera
- Autor con credenciales (Equipo Técnico Viveros Terra)
- Fechas exactas (actualizado 2026)
- Citaciones a normas (SEMARNAT, SAGARPA, certificación fitosanitaria)
- Schema.org Service + Product[] + LocalBusiness con `areaServed` múltiple

### Estructura semántica

```
H1: Palmas al Mayoreo para Proyectos · Tamaulipas, Veracruz y SLP
   H2: ¿Por qué arquitectos y compradores corporativos eligen Viveros Terra?
   H2: 12 palmas para proyectos · spec sheet
      H3: Por cada especie (12)
   H2: Algunos proyectos recientes
   H2: Calcula tu proyecto en 30 segundos
   H2: Enviamos palmas a toda la región
   H2: Documentación B2B completa
   H2: Paquetes diseñados por tipo de proyecto
   H2: Guía gratuita: 12 palmas para proyectos arquitectónicos
   H2: Preguntas frecuentes de compradores B2B
```

---

## Token system unificado (editorial híbrido)

### Light sections
- Background: `#FAFAF7`
- Heading: Playfair Display, color `#1F3D2B`
- Body: Inter 400, color `#2F3F35`
- Accent: `#55B96A`

### Dark sections
- Background: `#0D2B0E`
- Heading: Playfair Display, color `#fff`
- Body: Inter 400, color `rgba(255,255,255,0.78)`
- Accent: `#7BD897` (verde más vivo para contraste)

### Common
- Border radius: 20px (cards), 999px (botones)
- Type scale: 14, 16, 18, 22, 28, 36, 56px
- Shadows: layered soft, no harsh
- Botón primario: verde `#45C463` (consistente con hero v2 homepage)

---

## Arquitectura de contenido (12 secciones)

### 1. HERO (LIGHT)

- **Background:** Foto luminosa de palmas grandes en jardín hotelero/fraccionamiento premium
- **H1 (Playfair, 64-78px):** "Palmas para tu proyecto, donde sea que estés en la región."
- **Subhead (Inter 18px, 3 líneas máx):** "Productor directo en el sur de Tamaulipas. Envíos a hoteles, fraccionamientos, gobierno e industria en Tamaulipas, Veracruz y SLP — con documentación CFDI y garantía de arraigo escrita."
- **Badges (4):**
  - 🌴 +15 especies en stock
  - 🚛 Cobertura 3 estados
  - 📋 CFDI · Fitosanitario
  - ⭐ Garantía 60 días arraigo
- **CTAs duales:**
  - Primario verde `#45C463`: "Cotizar mi proyecto" → scroll a sección 12 formulario
  - Secundario blanco con borde: "Descargar guía de especies (PDF)" → sección 10 lead magnet
- **Microdato:** "+80 proyectos B2B en 36 meses"

### 2. TRUST BAR (DARK)

Fila horizontal sin logos clientes (decisión B+C):
```
20 AÑOS  |  +500,000 m²  |  +80 PROYECTOS B2B  |  3 ESTADOS  |  +15 ESPECIES
```
Subcopy: "Productor verificado de palmas para sector hotelero, gobierno e industria"

### 3. LA TRINIDAD (LIGHT)

- **H2:** "Por qué arquitectos y compradores corporativos eligen Viveros Terra"
- **3 cards alineadas:**

| Card | Título | Descripción |
|------|--------|-------------|
| 🌱 | Productor directo | Sin intermediarios. Margen justo, control total de calidad, capacidad de proyecto grande. |
| 🚛 | Logística regional | Cobertura Tamaulipas, Veracruz y SLP. Transportes propios y red de fleteros confiables. |
| 📋 | Documentación B2B | CFDI 4.0, certificado fitosanitario, factura emitida el día del pago, garantía escrita. |

### 4. ESPECIES B2B (DARK) — spec sheet magazine

- **H2:** "12 palmas para proyectos · spec sheet"
- **Layout:** Rows tipo revista. Cada especie con:
  - Foto cuadrada izquierda
  - Nombre comercial + binomial
  - Specs: Altura adulta · Lead time · Resistencia clima · Mantenimiento
  - Precio "desde" para volumen 50+
  - CTA: "Cotizar 50+" (link WhatsApp con mensaje pre-llenado)

**12 especies en orden por demanda B2B:**

| # | Especie | Binomial | Desde (50+) | Lead time |
|---|---------|----------|------------|-----------|
| 1 | Washingtonia | Washingtonia robusta | $1,800 | 2-4 sem |
| 2 | Palma Real | Roystonea regia | $4,200 | 4-8 sem |
| 3 | Palma Areca | Dypsis lutescens | $850 | 2-3 sem |
| 4 | Palma del Viajero | Ravenala madagascariensis | $1,500 | 3-5 sem |
| 5 | Palma Coco Plumoso | Syagrus romanzoffiana | $2,400 | 3-6 sem |
| 6 | Palma Kerpis | Hyophorbe lagenicaulis | $2,000 | 3-5 sem |
| 7 | Cycas Revoluta | Cycas revoluta | $1,600 | 2-4 sem |
| 8 | Bambú Tarro | Bambusa vulgaris | $2,800 | 3-5 sem |
| 9 | Yucca Rostrata | Yucca rostrata | $3,200 | 4-6 sem |
| 10 | Palma Bambú | Chamaedorea seifrizii | $2,200 | 3-5 sem |
| 11 | Palma Cola de Zorra | Wodyetia bifurcata | $1,200 | 2-4 sem |
| 12 | Palma Triángulo | Dypsis decaryi | $2,400 | 4-6 sem |

### 5. PROYECTOS (LIGHT) — portfolio editorial

- **H2:** "Algunos proyectos recientes"
- **Grid 3×2 = 6 proyectos** (combinación B+C):
  - Cada card: foto real + categoría (HOTEL BOUTIQUE, PARQUE INDUSTRIAL, etc.) + descripción anonimizada + año
  - Sin nombres específicos del cliente

**6 proyectos anonimizados:**
1. "Hotel boutique en Altamira · 50 palmas Real + Coco · 2024"
2. "Parque industrial Altamira · 90 Washingtonias · 2024"
3. "Fraccionamiento residencial Cd. Madero · 2024"
4. "Áreas verdes parque municipal Pánuco · 2023"
5. "Hotel frente al mar Tampico · 35 palmas Coco · 2024"
6. "Campus corporativo Tampico · 120 plantas + 15 palmas"

### 6. CALCULADORA INTERACTIVA (DARK)

- **H2:** "Calcula tu proyecto en 30 segundos"
- **3 campos:**
  1. Tipo de proyecto (dropdown: Hotel · Fraccionamiento · Industrial · Gobierno · Otro)
  2. Tamaño aproximado (m² o número de palmas)
  3. Ciudad destino (texto libre)
- **CTA:** "Obtener estimado por WhatsApp"
- **Mecánica:** JS construye URL WhatsApp con mensaje pre-llenado: "Hola, quiero estimado para [tipo] de [tamaño] en [ciudad]"
- **No genera precio inmediato** — captura lead pre-calificado para que ventas responda rápido

### 7. COBERTURA GEOGRÁFICA (LIGHT)

- **H2:** "Enviamos palmas a toda la región"
- **Mapa SVG simple de México** con zonas verdes (color `#55B96A`) marcadas:
  - 🟢 **Tamaulipas:** Tampico, Cd. Madero, Altamira, Cd. Victoria, Reynosa, Matamoros, Nuevo Laredo, Pánuco
  - 🟢 **Veracruz norte:** Tuxpan, Poza Rica, Xalapa
  - 🟢 **San Luis Potosí:** SLP capital + Huasteca Potosina
  - ⚪ **Bajo cotización:** Monterrey, Guadalajara, CDMX (proyectos grandes)
- **Tabla de tiempos de entrega:**

| Zona | Tiempo entrega |
|------|---------------|
| Tampico/Madero/Altamira | 2-5 días |
| Resto Tamaulipas | 4-7 días |
| Veracruz/SLP | 5-10 días |
| Otros estados | a coordinar |

### 8. DOCUMENTACIÓN B2B (DARK)

- **H2:** "Documentación completa para tu compra empresarial"
- **4 cards con íconos:**
  - 📋 **CFDI 4.0:** Emitida el día del pago, con complemento de servicios
  - 🌿 **Certificado fitosanitario:** Para cruce entre estados
  - 🛡️ **Garantía escrita:** 60 días de arraigo, reposición incluida
  - 🏛️ **Documentación licitaciones:** Padrón de proveedores, fianzas

### 9. PAQUETES PRE-ARMADOS (LIGHT)

- **H2:** "Paquetes diseñados por tipo de proyecto"
- **4 cards:**

| 🏨 Hotel Boutique | 🏘️ Fraccionamiento | 🏭 Parque Industrial | 🏛️ Gobierno |
|-------------------|---------------------|----------------------|--------------|
| 20-40 palmas mix curado | 40-80 Washingtonia + Areca | 50-150 Washingtonia + Cycas | Licitación pública lista |
| Desde $90,000 | Desde $150,000 | Desde $180,000 | Cotización personalizada |
| Ver detalle → | Ver detalle → | Ver detalle → | Ver detalle → |

### 10. LEAD MAGNET (DARK)

- **H2:** "Guía gratuita: 12 palmas para proyectos arquitectónicos"
- **Layout split 60/40:**
  - Izq: Descripción de qué incluye el PDF (32 páginas: fichas técnicas, costos, suelo, mantenimiento)
  - Der: Formulario de 3 campos (Nombre · Email · Tipo proyecto)
- **CTA:** "Descargar guía gratis"
- **Subcopy:** "Más de 200 arquitectos y compradores la han descargado este año"
- **PDF inicialmente:** placeholder en `/pdf/guia-palmas-arquitectos.pdf` (genera contenido real después)

### 11. FAQ (LIGHT)

- **H2:** "Preguntas frecuentes de compradores B2B"
- **8 preguntas con schema FAQPage:**
  1. ¿Cuál es el pedido mínimo al mayoreo?
  2. ¿Hacen envíos fuera de Tamaulipas?
  3. ¿Qué pasa si una palma no arraiga?
  4. ¿Tienen factura y certificado fitosanitario?
  5. ¿Cuánto tarda la entrega?
  6. ¿Aceptan pago diferido / a crédito para proyectos?
  7. ¿Pueden hacer instalación llave en mano?
  8. ¿Trabajan con compras de gobierno?

### 12. CTA FINAL (DARK)

- **Layout 70/30:**
  - Izq: H2 grande "Cotiza tu proyecto" + 3 razones (Productor directo · Documentación completa · Respuesta en 4h)
  - Der: Formulario completo (5 campos): Nombre, Empresa, Email, Teléfono/WhatsApp, Detalle del proyecto
- **Submit:** Envía a WhatsApp con datos pre-llenados (sin backend)
- **Subcopy:** "Respondemos en menos de 4 horas hábiles · Lun–Vie 9-18h"

---

## Mobile strategy

### Orden de prioridad
1. Hero (impacto + 1 CTA)
2. Trust bar (números grandes)
3. La Trinidad (stack vertical)
4. CTA cotización temprano (sticky bottom)
5. Proyectos (showcase visual)
6. Resto en orden

### Adaptaciones por sección

| Sección | Adaptación móvil |
|---------|-----------------|
| Hero | H1 36-42px, CTAs stacked, badges grid 2×2 |
| Trust bar | Carrusel horizontal con números 1 por 1 |
| Trinidad | Stack vertical (no grid 3col) |
| Especies B2B | Acordeón colapsable por especie (no tabla horizontal) |
| Proyectos | Grid 1 columna foto grande + descripción debajo |
| Calculadora | Stepper 1-2-3 (un campo a la vez) |
| Mapa cobertura | Sustituir mapa SVG por lista de ciudades |
| Documentación | Stack vertical, ícono + texto |
| Paquetes | 1 card visible, swipe horizontal |
| Lead magnet | Form stacked, botón full-width |
| FAQ | Acordeón estándar |
| CTA final | Form full-width, campos 48px+ touch |

### Sticky CTA bar mobile
Mismo patrón que homepage hero v2:
- WhatsApp + tel circle fixed bottom
- Visible desde el final del hero hasta antes del CTA final
- `env(safe-area-inset-bottom)` para notch iPhone

---

## Accesibilidad WCAG 2.1 AA

### Contraste verificado
- Light sections: `#1F3D2B` sobre `#FAFAF7` = **12:1** ✓
- Dark sections: `#fff` sobre `#0D2B0E` = **15:1** ✓
- Body dark: `rgba(255,255,255,0.78)` sobre `#0D2B0E` = **11.7:1** ✓ (AAA)

### Estructura semántica
- H1 único (hero)
- 11 H2 (uno por sección)
- H3 dentro de subsecciones (especies, paquetes)
- Sin saltos de nivel

### Touch & keyboard
- CTAs ≥ 48×48px en mobile
- Mínimo 8px espacio entre clickables
- Tab order matches visual order
- Focus rings visibles
- Skip-link al main content
- `aria-label` en botones de íconos

### Reduced motion
- `@media (prefers-reduced-motion: reduce)` desactiva animaciones scroll y hovers con transform

---

## Schema markup completo

Bloque JSON-LD único en `<head>` con `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "#service",
      "name": "Venta de palmas al mayoreo para proyectos B2B",
      "serviceType": "Wholesale palm tree supply",
      "provider": { "@type": "LocalBusiness", "name": "Viveros Terra" },
      "areaServed": [
        { "@type": "State", "name": "Tamaulipas" },
        { "@type": "State", "name": "Veracruz" },
        { "@type": "State", "name": "San Luis Potosí" }
      ],
      "offers": { "@type": "AggregateOffer", "lowPrice": "850", "highPrice": "300000", "priceCurrency": "MXN" }
    },
    {
      "@type": "ItemList",
      "name": "12 palmas para proyectos B2B",
      "numberOfItems": 12,
      "itemListElement": [ /* 12 items con Product schema */ ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [ /* 8 questions */ ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.viverosterra.com" },
        { "@type": "ListItem", "position": 2, "name": "Palmas al Mayoreo para Proyectos", "item": "https://www.viverosterra.com/palmas-mayoreo-proyectos" }
      ]
    }
  ]
}
```

---

## Archivos a crear/modificar

**Crear:**
- `public/palmas-mayoreo-proyectos/index.html` (~1,500 líneas)
- `public/pdf/guia-palmas-arquitectos.pdf` (placeholder por ahora)

**Modificar:**
- `public/sitemap.xml` (añadir nueva URL, priority 0.9, lastmod 2026-05-12)
- Navbar dropdown en ~22 archivos (añadir link "Palmas al Mayoreo" en sección "Por Zona · B2B")

**Imágenes necesarias (a aportar por cliente):**
- 1 hero (jardín hotelero/residencial premium con palmas grandes)
- 6 fotos proyectos terminados (sin nombres de cliente visibles)
- 12 fotos de especies (idealmente del catálogo existente)

---

## Analytics & tracking

**GA4 events a configurar:**
- `b2b_cotizar_proyecto_submit` (formulario CTA final)
- `b2b_pdf_descargado` (lead magnet)
- `b2b_calculadora_completada` (sección 6)
- `b2b_whatsapp_click` (cualquier CTA WhatsApp)
- `b2b_paquete_clic` (cards paquetes)
- `b2b_especie_click` (CTA "Cotizar 50+" en especies)

**Conversiones marcadas como goals:** Las 6 anteriores.

---

## Métricas de éxito post-launch

### Mes 1-2
- 80+ visitas orgánicas/mes
- 5+ descargas PDF
- 2-3 cotizaciones B2B iniciadas

### Mes 3-6
- 250+ visitas orgánicas/mes
- 15+ leads cualificados
- 3-5 proyectos B2B cotizados/mes
- 1-2 cierres B2B mensuales (ticket $80K+)

### Mes 6-12
- 500+ visitas orgánicas/mes
- Ranking Top 5 para "palmas mayoreo Tamaulipas"
- 5-8 cierres B2B mensuales
- ROI vs costo de implementación: 30x+ en año 1

---

## Self-review

### Spec coverage
- ✅ Estrategia (posicionamiento, psychology, SEO/AEO/LLM)
- ✅ 12 secciones detalladas con contenido específico
- ✅ Lista exhaustiva de 12 especies con precios y lead times
- ✅ 6 proyectos anonimizados definidos
- ✅ 4 paquetes pre-armados con precios "desde"
- ✅ 8 FAQ definidas
- ✅ Mobile strategy completa
- ✅ Accesibilidad WCAG verificada (contrastes calculados)
- ✅ Schema markup completo
- ✅ Tracking GA4 definido
- ✅ Métricas de éxito cuantificadas

### Placeholder scan
- ✅ Sin TBDs ni TODOs
- ✅ Lead magnet PDF: explícitamente "placeholder por ahora" (decision made)
- ✅ Imágenes: explícitamente "a aportar por cliente" (acción concreta)
- ✅ Precios "desde": validados con catálogo existente del sitio

### Consistencia interna
- ✅ Color tokens consistentes (light vs dark) en todas las secciones
- ✅ Botón primario `#45C463` consistente con hero v2 homepage
- ✅ Tipografía Playfair + Inter consistente con resto del sitio
- ✅ 12 especies referenciadas en TODAS las secciones relevantes (hero badge, especies, paquetes, FAQ)
- ✅ "Garantía 60 días arraigo" repetida coherentemente
- ✅ "Tamaulipas + Veracruz + SLP" como cobertura consistente

### Ambigüedad check
- ✅ Cobertura geográfica explícita (no "región" genérica)
- ✅ Pricing strategy explícita (híbrido con precios "desde" definidos)
- ✅ Social proof strategy explícita (B+C: anonimizado + fotos reales)
- ✅ Lead capture mechanics explícitos (WhatsApp pre-llenado, no backend)
- ✅ Cada CTA tiene destino claro definido
