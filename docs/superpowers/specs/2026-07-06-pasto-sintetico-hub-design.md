# Spec — Hub Nacional de Pasto Sintético (viverosterra.com)

**Fecha:** 2026-07-06 · **Estado:** Aprobado por Luis (Viveros Terra)
**Objetivo:** capturar búsquedas nacionales de pasto sintético y generar ventas directas
(híbrido cotizador → WhatsApp/link de pago) aprovechando capacidad de dropshipping a todo México.

---

## 1. Decisiones aprobadas

| Decisión | Valor |
|---|---|
| Arquitectura | **A — Hub nacional + spokes locales** (ciudades programáticas = fase 2 solo si hay tracción) |
| Modelo de venta | **Híbrido**: cotizador en página → WhatsApp con pedido armado + opción "solicitar link de pago" |
| Oferta nacional | **Solo material (rollos)** — sin instalación fuera de Tampico/Madero/Altamira |
| Catálogo | **Solo 9 modelos residenciales** — deportivos y pádel EXCLUIDOS del sitio por decisión de negocio |
| Precios | Estrategia **"muestra m², vende rollo"** con 3 escalones. IVA incluido, CFDI 4.0 |
| Mínimo nacional | **25 m²** (local desde 2 m² en showroom) |
| Envíos | **Estimados por zona (3 zonas)**; costo FINAL se cotiza por WhatsApp con dirección + CP exactos |
| Origen de embarque | Guadalajara — **NO se menciona públicamente**. Solo "envíos a todo México · 3-5 días hábiles una vez confirmado" |
| Palanca de cierre | "Envío GRATIS a partir de 2 rollos (100 m²)" — aprobada |

## 2. Lista de precios aprobada (IVA incluido, $/m²)

| Modelo | Specs | 1–9 m² | 10–49 m² | Rollo 50 m² |
|---|---|---|---|---|
| Aruba 10 | 10mm · 1,000 g/m² · 5 años | $189 | $159 | **$139** |
| Toscana 18 ⚡stock | 18mm · 1,000 · 5 años | $199 | $169 | **$149** |
| Toscana 28 ⚡🌟más vendido | 28mm · 1,100 · 5 años | $279 | $229 | **$199** |
| Irlanda 25 | 25mm · 1,400 · 8 años | $279 | $239 | **$209** |
| Capri 20 | 20mm · 1,580 · 8 años | $279 | $239 | **$209** |
| Viena 30 | 30mm · 1,800 · 8 años | $339 | $279 | **$249** |
| Japonés 35 | 35mm · 1,800 · 8 años | $359 | $299 | **$269** |
| Mónaco 35 | 35mm · 2,100 · 8 años | $399 | $339 | **$299** |
| Bali 35 | 35mm · 2,100 · 8 años | $399 | $339 | **$299** |

- Rollos de 2 m de ancho (50 m² = 2×25 m)
- Íconos por modelo según catálogo PDF 2026 (mascotas, niños, alto tránsito, suavidad, fuego, antibacterial)
- Costos distribuidor (referencia interna, NO publicar): Aruba/T18 $89 · T28/Irlanda $125 · Capri $129 · Viena $149 · Japonés $159 · Mónaco/Bali $189

## 3. Envío estimado (público como "estimado", nunca como tarifa fija)

| Zona | Estimado por rollo |
|---|---|
| A · Centro-Occidente | ~$900 |
| B · Norte / Sur | ~$1,150 |
| C · Sureste / Fronteras | ~$1,400 |

Copy obligatorio junto a todo estimado: *"Envío estimado — el costo exacto se confirma por
WhatsApp con tu dirección y C.P."* Asignación de estados a zonas: la define Luis al implementar
(default razonable en el plan de implementación, ajustable).

## 4. Página nueva: `/pasto-sintetico` (hub nacional)

Patrón visual del sitio (vt-hero claro, design-system.css, Tailwind compilado). Secciones en orden:

1. **Hero** — H1 "Pasto Sintético con Envío a Todo México — Precio de Productor".
   Badges: Envío nacional 3-5 días · Factura CFDI 4.0 · +500,000 m² instalados · Garantía 5-8 años.
   Métricas vt-hero: 9 modelos / desde $139 m² / 3-5 días entrega / +900 clientes.
2. **Cotizador híbrido** (arriba del fold):
   - Modelo (9 cards con foto+specs) → m² (input + presets 25/50/100) → Estado (dropdown → zona)
   - Output: material (según escalón) + envío estimado + total estimado + ahorro vs corte
   - CTA 1: "Pedir por WhatsApp" (mensaje pre-armado: modelo, m², estado, total estimado)
   - CTA 2: "Solicitar link de pago" (mismo WhatsApp, texto pide link de pago)
   - Nota de estimado obligatoria + mínimo nacional 25 m²
3. **Catálogo de 9 modelos** — cards estilo Plantdex (stat-block: altura, peso, garantía, íconos)
   con precio "desde $X/m² en rollo" + badges EN STOCK / MÁS VENDIDO
4. **Comparativa "¿Cuál pasto es para ti?"** — tabla HTML de los 9 (la del PDF pág. 14) — pieza AEO central
5. **Cómo funciona el envío** — 4 pasos (cotizas → confirmas y pagas → embarcamos → rastreo), 3-5 días,
   rollos 2 m ancho, "gratis desde 2 rollos"
6. **Guía DIY resumida** + link al artículo completo
7. **Prueba social** — proyectos reales; testimonios foráneos conforme lleguen
8. **FAQ nacional** (8-10 Q) con schema FAQPage — precios, mínimos, envío, pago, factura, instalación propia
9. **Banda local** — "¿Estás en Tampico? Showroom e instalación llave en mano →" (2 links locales)

## 5. Ajustes a páginas existentes (quirúrgicos)

- `/venta-pasto-sintetico-tampico`: banda "📦 ¿No estás en Tampico? Enviamos a todo México →" + FAQ envíos
- `/pasto-sintetico-tampico`: banner discreto igual + links a artículos nuevos
- Homepage: card pasto sintético menciona envíos nacionales; catálogo (tab Pasto) enlaza al hub
- `/blog/pasto-sintetico-vs-natural-tampico`: agregar links a hub y a venta
- Regla anti-canibalización: hub targetea keywords SIN ciudad; locales conservan "tampico/madero/altamira"

## 6. Blog cluster (5 artículos, formato answer-first + fecha visible + tablas + números)

| Artículo | Keyword | Prioridad |
|---|---|---|
| ¿Cuánto cuesta el pasto sintético en México? (precios 2026 por m²) | pasto sintético precio m2 | Fase 1 |
| Cómo instalar pasto sintético tú mismo — guía paso a paso | como instalar pasto sintético | Fase 1 |
| ¿18, 28 o 35 mm? Cómo elegir la altura correcta | pasto sintético 28mm | Fase 2 |
| Pasto sintético para mascotas | pasto sintético para perros | Fase 2 |
| ¿El pasto sintético aguanta el calor de México? | pasto sintético desventajas/calor | Fase 2 |

Todos cierran con CTA/cotizador al hub. Interlinking bidireccional hub↔artículos↔locales.

## 7. Capa técnica AEO/Schema

- Hub: Product schema por modelo (offers con precio rollo) + OfferShippingDetails (MX, 3-5 días)
  + FAQPage + BreadcrumbList
- "Actualizado [mes año]" visible en hub y artículos
- robots: verificar que GPTBot/PerplexityBot/ClaudeBot/Google-Extended NO estén bloqueados
- Sitemap + Search Console al publicar
- GBP: dar de alta los 9 modelos como productos (kit aparte, mismo patrón que Toscana ya entregado)

## 8. Fases y medición

- **Fase 1:** hub + cotizador + ajustes a existentes + 2 artículos prioritarios
- **Fase 2 (mes 2):** 3 artículos restantes; evaluar páginas Monterrey/CDMX solo si hay leads foráneos
- **Medición:** parámetro por página en links de WhatsApp; Search Console (queries sin ciudad);
  chequeo mensual manual en ChatGPT/Perplexity/AI Overviews de "¿cuánto cuesta el pasto sintético en México?"

## 9. Fuera de alcance (explícito)

- Deportivos (Monofilamento/Fibrilado/Híbrido) y Pádel: no se publican ni en hub ni en GBP
- Checkout con pasarela de pago automática (el "link de pago" se envía manualmente por WhatsApp)
- Follaje artificial: fuera del hub (posible página propia futura)
- Páginas por ciudad: fase 2 condicionada a tracción
