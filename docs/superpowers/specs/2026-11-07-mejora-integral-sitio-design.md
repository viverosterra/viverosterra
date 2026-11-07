# Mejora integral de viverosterra.com: estrategia y diseño

Fecha: 2026-11-07 · Estado: estrategia aprobada por el dueño en conversación (enfoque A), pendiente de revisión escrita.
Insumos: 5 auditorías y 3 jurados de diseño del 6 y 7 nov 2026, guardados en el scratchpad de la sesión
(`.../scratchpad/audit/01-diseno-identidad.md`, `02-conversion-recorrido.md`, `03-seo-tecnico-keywords.md`,
`04-aeo-geo-llms.md`, `05-codigo-rendimiento-a11y.md`; `.../scratchpad/design/00-direcciones.md` y
`design/jurado/01-conversion.md`, `02-diseno.md`, `03-calidad-cumplimiento.md`). En este documento se citan como
A01–A05, D00 y J01–J03. Maqueta híbrida de referencia: `.../scratchpad/design/hibrido/` (en construcción; los
tokens y fuentes definitivos se fijan desde ella en la Etapa 1).

## Decisiones del dueño (vinculantes)

| Tema | Decisión |
|---|---|
| Enfoque | A: por etapas. Cada etapa la revisan agentes especialistas (diseño, SEO/AEO, CRO, cumplimiento/QA) y se publica a producción cuando se aprueba. |
| Dirección visual | Híbrido "Plano + Etiqueta": estructura, Medidor de m², cuadro de datos y pies `FIG.` de Plano de Obra; la etiqueta amarilla de precio como objeto de marca de Etiqueta de Vivero; tono honesto, marcadores NOSOTROS / TÚ y plantilla de artículo de Libreta de Campo. |
| Domicilio | Av. Álvaro Obregón 209 Sur, Col. Ampliación Unidad Nacional, 89510 Ciudad Madero, Tamps. (frente a Walmart, entrando por Banamex). Hoy todas las páginas dicen "209" sin "Sur": se corrige en todas. |
| Cifras | "+500,000 m² instalados" es real y se puede usar. |
| Garantía de pasto | Se permite "Si una sección no arraiga, la reponemos sin costo", siempre ligada a la garantía de arraigo de 15–20 días y a sus condiciones. Prohibido "pagas cuando ves tu jardín terminado". |
| Deportes | La regla de no deportes aplica solo al pasto sintético. Pasto natural y riego para campos deportivos es un servicio real y se queda. |

### Reglas permanentes (se prueban en automático, ver §9)

- Nunca "Oasis". Nunca nombres de marcas de proveedor de pasto sintético. No se ofrecen muestras físicas.
- Envío de sintético por rollo, nunca gratis. Los 9 modelos en existencia nacional; "para llevar hoy" solo Toscana 18 y Toscana 28.
- El primer riego lo hace el cliente, dicho en positivo: "te enseñamos cómo y te dejamos el protocolo de 20 días".
- "Mensualidades con tarjeta de crédito"; nunca "MSI", "meses sin intereses" ni "sin intereses". Nunca el nombre del proveedor de la terminal en `public/`. La fórmula de mensualidades es la de `tools/pasto/mensualidades.py` / `public/js/vt-mensualidades.js` y no se reimplementa.
- Reseñas de Google en pausa: solo la línea estática "4.6 en Google (24 reseñas)", sin widgets ni marcado `aggregateRating`.

### Datos oficiales

| Dato | Valor |
|---|---|
| Pasto San Agustín | $85/m² solo pasto · desde $120/m² instalado · mayoreo desde $60/m² (500 m² o más) |
| Servicios | Mantenimiento desde $750/mes · diseño desde $3,000 · riego $180–$320/m² · sintético Tampico $385–$650/m² instalado · tienda de sintético desde $139/m² |
| Garantías | Arraigo de pasto 15–20 días · plantas 30 días con condiciones (solo las que siembra el equipo, con riego indicado) |
| Empresa | Desde 2007 (12 dic 2007) · +200 variedades · +900 clientes · +1,500 instalaciones · +500,000 m² · REPSE 773725 · CFDI 4.0 |
| Contacto | WhatsApp y teléfono +52 833 326 8008 · lun a vie 9 a 18 h, sáb 9 a 14 h · formularios a viverosterra@hotmail.com |

---

## 1. Objetivo y métricas de éxito

**Objetivo:** que cada visita relevante termine en un WhatsApp con contexto (servicio, m², colonia, plan o modelo),
con un solo sistema visual, datos sin contradicciones y autoridad local en Google y en asistentes de IA.

| Métrica | Cómo se mide | Línea base | Meta |
|---|---|---|---|
| Leads de WhatsApp por página | GA4 `generate_lead` (método `whatsapp`) por `page_path` y `cta_id` | Se toma en las 2 semanas posteriores a instalar la medición (Etapa 1) | +30 % de leads totales 8 semanas después de la Etapa 3, a tráfico comparable |
| Tasa de conversión | `generate_lead` / sesiones, por tipo de página | Igual | Servicio ≥ 4 %, tienda ≥ 3 %, blog ≥ 0.8 % (se ajustan con la línea base) |
| Llamadas | GA4 `click_to_call` (enlaces `tel:`) | Igual | Se reporta, sin meta |
| Core Web Vitals | Search Console (CrUX p75, móvil) y Lighthouse móvil por plantilla | LCP 5.3–7.3 s, Perf 63–76 (A05 §2.1) | LCP < 2.5 s, INP < 200 ms, CLS < 0.1; Lighthouse Perf ≥ 90 en cada plantilla |
| Accesibilidad | axe-core por plantilla | Botón WA 1.98:1, 75 páginas sin `<main>` (A05 §3) | 0 violaciones serias o críticas; Lighthouse A11y ≥ 98 |
| Posiciones | Search Console, consultas del mapa de palabras clave (§6.6) | Se exporta al obtener acceso | Top 3 en las 8 consultas locales principales a 6 meses |
| Citas en IA | Panel manual mensual de 10 consultas fijas en ChatGPT Search, Perplexity, Gemini y AI Overviews | Aparece solo en consultas de marca (A04 §5) | Citado (sitio o perfil propio) en ≥ 4 de 10 a 6 meses |

**Medición que existe hoy:** GA4 `G-RMZCVJ734M` en 98 de 109 páginas (faltan 11, entre ellas plantas, palmas y
`palmas-mayoreo-proyectos`; A05 §1.3). La tienda manda `add_to_cart`, `view_cart` y `generate_lead` desde
`public/js/tienda-pasto.js`. Fuera de la tienda solo hay eventos sueltos con nombres propios (`clic_wa_float`,
`clic_wa_mayoreo`, `clic_planta`…) en 2 páginas. No se mide qué CTA ni qué página genera chats.

**Medición nueva (Etapa 1):**
- Cada enlace `wa.me` y `tel:` lleva `data-cta="<tipo-página>:<sección>"` (p. ej. `servicio-pasto:hero`).
- Un script compartido (`terra.js`) escucha clics por delegación y manda `generate_lead` con
  `{method:"whatsapp", cta_id, service}` o `click_to_call` con `{cta_id}`. La tienda conserva sus eventos.
- `generate_lead` se marca como evento clave en GA4. Se retiran los eventos sueltos `clic_*`.
- El texto del mensaje termina con "Vengo de viverosterra.com" para atribuir en el chat sin exponer códigos.

---

## 2. Diagnóstico resumido

| Área | Hallazgos principales | Evidencia |
|---|---|---|
| Identidad | 3 generaciones visuales vivas más 1 huérfana; 5 familias tipográficas; 3 verdes de acción; patrones "de plantilla IA" (chips pastel, tarjetas de cristal, Playfair itálica verde) | A01 §1, §3; J02 |
| Conversión | Home sin bifurcación por cliente y con CTA genérico; 6 promesas de respuesta distintas; mantenimiento manda el mismo mensaje en 4 planes; precio bajo el pliegue en fichas móviles; mayoreo sin prueba B2B ni escalas | A02 §0, §2, §3 |
| Datos | Contradicciones: reseñas (+127 contra 24; 4.6 contra 5), clientes (900 contra 1,500), mayoreo (200 contra 500 m²), años (10/12/15 contra 18), framboyán ($250 contra $500), "sobre pedido", banner de lluvias, nota interna del blog, "22 artículos", tabla "plástico, áspero" | A01 §2–3; A02 §4.2; A04 §2.2 |
| Arquitectura | Dos menús y dos "catálogos"; 5 páginas de plantas compiten; 6 zonas casi huérfanas (1 enlace entrante); `cuestionario` huérfano; borrador `preview-mapa-cobertura` publicado | A02 §1; A03 §1 |
| SEO técnico | 71 de 109 títulos > 60 caracteres; canibalización (riego ×4, perros, banqueta, interior, palmas); apex 307; 404 sin diseño; `lastmod` masivo; AdsBot bloqueado en diseño, mantenimiento y riego | A03 §2–3; A02 §4.6 |
| AEO / entidad | ~140 entidades "Viveros Terra" anónimas y un segundo `@id`; sin Nosotros ni autor; FAQ que responden "escríbenos"; `llms.txt` sin `/precios`; CCBot bloqueado; directorios con datos viejos (Cosmos, Cronoshare) | A04 §1–4 |
| Código | Solo 30 de 109 páginas salen del generador; 76 variantes de `<nav>` y 34 de `<footer>`; Tailwind desfasado con 50 clases inexistentes y sin `package.json`; CSS/JS sin caché larga; `/api/img` proxy abierto | A05 §1, §2.6, §4 |
| Rendimiento | Google Fonts bloquea ~920 ms en 108 páginas; 309 `<img>` sin dimensiones; 115 imágenes sin uso (26 MB); 511 KB de `<style>` inline | A05 §2; A03 §5 |
| Accesibilidad | Botón WhatsApp 1.98:1 (234 usos); 75 páginas sin `<main>`, 79 sin skip-link; 65 inputs sin label; foco de servicios 2.5:1 | A05 §3 |
| Seguridad | Sin CSP; HSTS sin `includeSubDomains`/`preload`; `/api/img` sirve cualquier archivo público de Drive | A05 §4 |
| Calidad | Sin CI ni pruebas sobre las ~79 páginas a mano (así pasaron los `SyntaxError`, el número falso y las clases faltantes) | A05 §5.5 |

---

## 3. Arquitectura de información

### 3.1 Menú principal (6 entradas + CTA)

| Entrada | Destino | Desplegable (escritorio) / acordeón (móvil) |
|---|---|---|
| Pasto natural | `/pasto-en-rollo-tampico` | Pasto en rollo · Mayoreo (500 m²+) · Protocolo de riego |
| Pasto sintético | `/pasto-sintetico-tampico` | Instalado en Tampico · Tienda con envío a todo México · Para perros |
| Jardín | — (solo abre el panel) | Diseño · Mantenimiento · Riego automático · Poda (si se aprueba, §3.5) |
| Plantas y palmas | `/plantas-palmas-arboles-tampico` | Palmas · Plantas para jardín · Árboles ornamentales · Árboles para banqueta · Interior · Arma tu lista (catálogo) · Materiales |
| Empresas | `/empresas` (nueva) | Mayoreo de pasto · Palmas para proyectos · Mantenimiento de áreas verdes |
| Precios | `/precios` | — |

CTA fijo del menú: "Cotizar por WhatsApp". Zonas, Materiales (además del panel), Blog, Nosotros, Visítanos
(`/vivero-tampico`) y políticas van en el pie. La tienda conserva una segunda barra contextual:
"Los 9 modelos · ¿Cuál me conviene? · Cómo comprar · Cotización (n)". El "(n)" se oculta con la lista vacía.

### 3.2 Mapa del sitio

```text
/                                      Inicio: bifurcación por cliente + Medidor
├── Pasto natural
│   ├── /pasto-en-rollo-tampico        residencial
│   ├── /mayoreo-pasto-tampico         empresas, 500 m² o más
│   └── /protocolo-cuidados-pasto-san-agustin   posventa (riego a cargo del cliente)
├── Pasto sintético
│   ├── /pasto-sintetico-tampico       instalación local y venta en Obregón 209 Sur
│   └── /pasto-sintetico               tienda nacional
│       ├── /{9 modelos}   /perros   /envio/{11 ciudades}
├── Jardín
│   ├── /diseno-jardines-tampico  →  /cuestionario (paso 2, noindex)
│   ├── /mantenimiento-jardines-tampico
│   ├── /sistema-riego-tampico         incluye riego de campos deportivos (pasto natural)
│   └── /poda-palmas-arboles-tampico   NUEVA, condicionada (§3.5)
├── Plantas y palmas
│   ├── /plantas-palmas-arboles-tampico   HUB
│   │   ├── /palmas-tropicales-tampico  /plantas-para-jardin-tampico  /arboles-ornamentales-tampico
│   │   ├── /arboles-para-banqueta-tampico  /plantas-de-interior-tampico (o el blog ganador, §3.4)
│   ├── /catalogo                      herramienta "Arma tu lista"
│   └── Materiales: /tierra-negra-vegetal-tampico /tezontle-rojo-tampico /marmol-blanco-tampico /piedra-bola-rio-tampico
├── /empresas                          NUEVA: índice B2B (mayoreo, palmas, mantenimiento, REPSE)
│   └── /palmas-mayoreo-proyectos
├── /zonas                             NUEVA: áreas de servicio → 6 /jardineria-*
├── /precios
├── /vivero-tampico                    "Visítanos": dirección, horario, cómo llegar
├── /nosotros                          NUEVA: página de entidad (§7.4)
├── /blog  →  /blog/{posts}
└── Utilidad: /politicas /politica-privacidad /gracias /datos-envio (noindex) /404
```

### 3.3 Plantillas por tipo de página (orden de secciones)

| Plantilla | Secuencia |
|---|---|
| **Home** | Menú → hero (qué vendemos + dónde + $85/$120 + CTA en el primer pantallazo móvil) → cuadro de datos → "¿Qué necesitas?" (Pasto natural · Pasto sintético · Diseño · Mantenimiento y riego · Empresas, cada uno con su etiqueta de precio) → Medidor de m² → proyectos con pies `FIG.` → logos de clientes → lista de precios resumida → proceso NOSOTROS / TÚ → FAQ (6) → CTA final → pie |
| **Servicio local** (pasto, diseño, mantenimiento, riego, sintético Tampico, poda) | Breadcrumb → H1 beneficio + lugar → precio ancla y qué incluye → CTA con plantilla + promesa única → prueba (cuadro de datos y 3 fotos `FIG.`) → opciones/planes (máx. 3, cada uno con su mensaje) → objeción principal → proceso en 5 pasos (una sola sección) → garantía con condiciones → mensualidades con tarjeta de crédito → FAQ (6–8) → CTA final → servicios relacionados y zonas |
| **B2B** (empresas, mayoreo, palmas para proyectos) | H1 por segmento + precio por volumen con mínimo → CTA "Cotizar proyecto" (Empresa, obra, m² o especies, fecha) → clientes con nombre y REPSE verificable → tabla de escalas, capacidad y tiempos → documentación (CFDI, REPSE) → paquetes por obra → ficha descargable (solo si existe el PDF real) → FAQ de compras → CTA |
| **Ficha de tienda** | Breadcrumb → nombre, "En existencia" y etiqueta "desde $X/m² · rollo 50 m² · envío por rollo según estado" en el primer pantallazo → galería (imagen principal precargada, nunca `lazy`) → cotizador (estado, m², precio puesto, mensualidades) → para quién es → ficha técnica en cuadro de datos → rollo a escala → comparativa con 2 vecinos → envío por rollo → garantía del modelo → FAQ |
| **Hub de categoría** (plantas, materiales) | H1 + filtro por necesidad (sol/sombra, salitre, tamaño) → subcategorías con "desde $" → "Arma tu lista" (un solo mensaje) → garantía condicionada y siembra → FAQ → CTA |
| **Material** | H1 + precio por presentación (costal / m³ / camión) → usos → calculadora de cantidad → entrega → FAQ → CTA |
| **Ciudad** (envío nacional) | Respuesta directa (precio puesto y días) → tabla 25/50/100 m² con mensualidad máxima → encabezados en pregunta (costo, tiempo, mínimo, cómo elegir sin muestra, instalación) → modelos → CTA |
| **Zona** (6 locales) | H1 "Jardinería en {zona}" → servicios con precio → caso real de la zona (foto, m², fecha, con permiso) → problema local (salitre, suelo) → tiempo desde el vivero → CTA con plantilla de zona → enlaces a servicios |
| **Catálogo** | Buscador y filtros arriba → una sola rejilla (foto, nombre, nombre científico, luz/riego/altura, "+ Añadir a mi lista") → lista con un solo mensaje → garantía condicionada |
| **Artículo de blog** | Respuesta directa (snippet) → autor y fecha de actualización → cuerpo con columna de margen y Notas de campo → 2–3 enlaces contextuales a money pages → etiqueta de "producto relacionado" (una sola) → CTA a una landing (no WhatsApp genérico) → relacionados |
| **Precios / políticas** | Respuesta directa con fecha de vigencia → tablas por servicio con columna Unidad → mensualidades (plazos, mínimos, aviso del banco) → garantías y exclusiones → anclas estables (`#garantia-plantas`, `#mensualidades`) |

### 3.4 Recorridos por tipo de cliente

| Cliente | Entrada | Recorrido objetivo |
|---|---|---|
| Dueño de casa en Tampico | Google "pasto en rollo tampico", Meta | Landing → precio en el hero → Medidor → WhatsApp con m², colonia y tipo → visita |
| Constructora / B2B | Google "pasto mayoreo", referidos | `/empresas` o mayoreo → clientes con nombre + REPSE → escalas → WhatsApp con plantilla de compras |
| Comprador nacional de sintético | Shopping, "pasto sintético {ciudad}" | Ciudad o ficha → cotizador por estado → lista → WhatsApp con modelo, m², estado, total y mensualidad |
| Diseño de jardín | Google, Instagram | Diseño → plan → WhatsApp → `/cuestionario` (enviado por el asesor) → visita |
| Mantenimiento / empresa recurrente | Google, recomendación | Mantenimiento → plan → WhatsApp "Plan X, m², casa/empresa" |

### 3.5 Consolidaciones, 301 y páginas nuevas

| Grupo | Decisión | Redirección |
|---|---|---|
| Plantas | Hub = `/plantas-palmas-arboles-tampico`; `/catalogo` = herramienta "Arma tu lista" (título sin "con precio" mientras no muestre precios); `plantas-para-jardin` y `arboles-ornamentales` = subcategorías con breadcrumb al hub; `/vivero-tampico` = Visítanos (deja de competir por "plantas"). Un solo conteo: "+200 variedades". | Sin 301; se reescriben títulos y enlaces |
| Perros | Destino comercial: `/pasto-sintetico/perros` (absorbe la tabla y lo útil del blog). | `/blog/pasto-sintetico-para-perros` → `/pasto-sintetico/perros` |
| Árboles de banqueta | Destino: `/arboles-para-banqueta-tampico` (absorbe la lista de 7 especies). | `/blog/arboles-para-sembrar-en-banqueta` → `/arboles-para-banqueta-tampico` |
| Plantas de interior | Se queda la URL con más clics en Search Console (90 días); la otra absorbe y redirige. Si no hay acceso a Search Console, gana `/blog/plantas-interior-tampico` (27 redirects históricos ya apuntan ahí) y la página de servicio pasa a 301. Los 27 redirects viejos se reescriben al destino final (sin cadenas). | Según la regla |
| Riego (4 URLs) | `/sistema-riego-tampico` es el destino transaccional. Se fusionan `conviene` y `roi` en una guía; `sistema-riego-automatizado-tampico` se reenfoca a "tipos y costos: aspersión contra goteo". | `/blog/riego-automatico-tampico-roi` → `/blog/sistema-riego-automatico-conviene-tampico` |
| Palmas (blogs) | Se fusionan `palmas-mas-vendidas-tampico-precios` y `palmas-tropicales-jardin-tampico` (mismo tema: 8 palmas). Las fichas de especie enlazan a `/palmas-tropicales-tampico` con la especie como ancla. | `/blog/palmas-tropicales-jardin-tampico` → `/blog/palmas-mas-vendidas-tampico-precios` |
| Pasto San Agustín (blog) | Se retitula `pasto-san-agustin-instalacion-mantenimiento` como guía ("Cómo instalar y mantener pasto San Agustín") sin competir por la transaccional. | Sin 301 |
| Diseño (blog) | Retitular `diseno-jardines-tampico-guia` como "cómo diseñar tu jardín paso a paso". | Sin 301 |
| Precios (blogs) | `cuanto-cuesta-jardin-tampico-precios`, `cuanto-cuesta-pasto-sintetico-mexico` y `jardin-bajo-presupuesto-tampico` enlazan a `/precios` como fuente única; el "Plan Terra Completo ($50,000+)" se renombra "Proyecto completo". | Sin 301 |
| Borrador | Se elimina `preview-mapa-cobertura.html`. | → `/` |
| Cuestionario | `noindex, follow`, canonical, un solo H1; enlazado como paso 2 desde diseño. | Sin 301 |

**Páginas nuevas** (solo las que justifican las auditorías):

| Página | Justificación | Condición |
|---|---|---|
| `/nosotros` | Página de entidad para E-E-A-T y LLMs (A04 §2.4, P1-9) | Ninguna; fotos reales recomendadas |
| `/empresas` | Bifurcación B2B y menú de 6 (A02 §6.2, §7) | Ninguna |
| `/zonas` | Da enlaces entrantes a las 6 zonas y evita doorways por colonia (A03 §3.4, §4.2) | Ninguna; no se agregan zonas nuevas sin caso real |
| `/poda-palmas-arboles-tampico` | Hueco de intención local "poda de palmas/árboles Tampico" (A03 §3.4) | Solo si el dueño confirma que es servicio real y da un precio "desde" |
| `/404` | Hoy 79 bytes sin diseño (A03 §2) | Ninguna |
| `llms-full.txt` | Hoy 404 (A04 §3.3) | Generado, nunca a mano |

No se crean páginas nuevas de ciudades de envío ni de colonias sin datos de impresiones en Search Console.

---

## 4. Sistema de diseño

### 4.1 Dirección híbrida "Plano + Etiqueta"

| Viene de | Se toma | No se toma |
|---|---|---|
| Plano de Obra | Retícula de 12 columnas, secciones numeradas, **Medidor de m²** (largo × ancho a escala → m² → precio → WhatsApp), **cuadro de datos** (Empresa · REPSE · CFDI · Desde · Domicilio · Google), pies `FIG. 0X · LUGAR · ETAPA`, columna "Unidad" en precios, rollo a escala en fichas | Coordenadas, "HOJA 0X/08", retícula sobre fotos, cotas sobre personas o "medidas de ejemplo", mono en antetítulos y botones |
| Etiqueta de Vivero | La **etiqueta amarilla de precio** como objeto de marca; nombre científico en itálica; cierre del pie con etiqueta | Rotaciones (el precio siempre va derecho; balanceo máximo de 1–2° en hover y nunca con movimiento reducido), más de 1 etiqueta por pantalla en móvil, etiquetas en el blog salvo la de producto relacionado |
| Libreta de Campo | Voz honesta ("sin letra chica", "dos pasos son tuyos"), **Notas de campo**, marcadores **NOSOTROS / TÚ / JUNTOS** en procesos, plantilla de artículo con columna de margen, tabla de mensualidades | Geist + Instrument Serif, renglones del hero, "status pill" |

### 4.2 Tokens (roles fijos; valores se congelan en la Etapa 1 desde `design/hibrido/`)

| Rol | Uso exclusivo | Valor candidato (de las maquetas) |
|---|---|---|
| Superficie | Fondo base y alterno | hueso `#FAF7EF` / `#F1ECDF` |
| Tinta | Texto | `#161A14`; secundaria con ≥ 4.5:1 sobre la superficie |
| Acción / marca | Botones, enlaces, foco | verde campo `#1E4D2B`, hover `#12301B` |
| Precio | Solo la etiqueta de precio y su banda | amarillo `#F2D24B` con tinta encima (11.8:1) |
| Medida | Solo cotas, m² y unidades | café tierra `#6B4226` (no un cuarto acento naranja) |
| WhatsApp | Solo el glifo, nunca fondo de botón con texto blanco | `#25D366` |
| Forma | Radios bajos (0–6 px); sin sombras genéricas | 2 px general, 6 px etiqueta |

Reglas: máximo 2 familias tipográficas (candidata: Archivo para titulares y texto con cifras `tabular-nums`, y
Fraunces itálica solo para nombres científicos y Notas de campo). Si el híbrido usa una mono para cifras y unidades,
cuenta como tercera familia y solo se acepta si entra en el presupuesto de fuentes (§8.1); si no, las cifras van en la
sans tabular. Mono, si se queda, nunca menor a 11 px. Escala tipográfica con tokens `--text-*` (no tamaños literales,
J03 §5). Contraste AA verificado por par de tokens en una prueba (§9).

### 4.3 Componentes

Menú y desplegables · barra fija móvil [Cotizar por WhatsApp | teléfono] (56 px + área segura; se oculta mientras el
CTA del hero está en pantalla; en la tienda [Cotización (n) · total | Enviar por WhatsApp]) · hero · cuadro de datos ·
etiqueta de precio (S, M, L) · Medidor · tarjeta de servicio · tabla de precios con Unidad · proceso NOSOTROS / TÚ ·
Nota de campo · figura con pie `FIG.` · FAQ con `<details>` · breadcrumb visible · pie único · formulario con labels ·
estados `:focus-visible` (2 px, separación 2 px, ≥ 3:1). Dos textos de CTA y nada más: "Cotizar por WhatsApp" y
"Llamar 833 326 8008". Debajo, la promesa única (§5.3). Se elimina `wa-float`.

El Medidor y los cotizadores reutilizan la lógica existente (cotizador de la home, `vt-simulador.js`,
`vt-mensualidades.js`, `tienda-pasto.js`): mayoreo con menos de 500 m² calcula a $85 (solo pasto) y lo avisa; envío
nacional bajo 25 m² bloquea total y mensualidades (J03 §3).

### 4.4 Una hoja de estilos y parciales compartidos

- **`terra.css` único** (meta < 30 KB, < 10 KB gzip) reemplaza `design-system.css`, `tailwind.css`, `servicios.css` y
  `tienda-pasto.css`. Mientras dura la migración, los componentes nuevos van con prefijo `vt-` para convivir con lo viejo.
- **Tailwind se retira, no se reconstruye.** No se introduce Node ni `package.json`. Para que las páginas viejas se vean
  bien mientras migran, la Etapa 1 agrega `legacy-fixes.css` con las 50 utilidades que faltan (lista de A05 §1.5); se
  borra junto con `tailwind.css` al cerrar la Etapa 2.
- **Generador para todo el sitio.** Nuevo paquete `tools/site/` (promueve lo que hoy hace `tools/pasto/common.py`):
  - `datos.py`: fuente única (§5.1).
  - `partials.py`: `head(meta)`, `header(activo)`, `footer()`, `barra_movil(cta)`, `analytics()`, `jsonld(nodos)`.
  - Páginas a mano pasan a `content/<slug>.html` con un bloque de metadatos y solo el contenido de `<main>`; el build
    las envuelve con los parciales. `tools/pasto` y `tools/servicios` usan los mismos parciales. Se retiran los parches
    por regex de `tools/servicios` (frágiles, A05 §1.1).
  - Assets con hash en el nombre (`terra.<hash>.css`, `terra.<hash>.js`) inyectados por el parcial.
- **Prueba de deriva:** falla si el `<nav>`, el `<footer>` o la barra móvil de cualquier HTML de `public/` difiere del
  parcial canónico, o si una página no sale del build.

---

## 5. Contenido y datos

### 5.1 Fuente única de verdad

`tools/site/datos.py` concentra NAP, horario, teléfono (formatos `wa.me` y visible), correo de formularios, cifras de
empresa, precios oficiales, garantías, promesa de respuesta, perfiles `sameAs`, fecha de vigencia de precios y versión
de assets. `tools/pasto/data.py` sigue siendo la fuente de modelos, zonas y fletes, e importa lo común de `datos.py`.
Lo consumen todos los parciales, todas las páginas, el JSON-LD, `llms.txt` y `llms-full.txt`. La paridad JS ↔ Python
que ya existe (`test_paridad_js.py`) se extiende a las constantes nuevas.

### 5.2 Contradicciones a corregir

| Dónde | Dice hoy | Queda |
|---|---|---|
| Home | "+127 reseñas verificadas" | "4.6 en Google (24 reseñas)" (y 4.6, no 5, en `plantas-palmas-arboles-tampico`) |
| Home cotizador | "Más de 1,500 clientes han calculado su jardín" | "+900 clientes · +1,500 instalaciones" |
| `mayoreo-pasto-tampico` FAQ | "a partir de 200 m²" | 500 m² |
| Blogs (`palma-coco-plumoso`, `sistema-riego-automatizado`, `cuidados-palma-del-viajero`, `pasto-sintetico-vs-natural`) | 10, 12 o 15 años (de la empresa) | "desde 2007"; se revisan una por una para no tocar las de vida útil del producto |
| `blog/framboyan-delonix-regia-tampico` y `arboles-ornamentales-tampico` | $250 contra $500; "Framboyán" y "Flamboyán" | Un solo precio por tamaño (confirma el dueño) y una ortografía |
| Todo el sitio | 6 promesas de respuesta | Una sola (§5.3) |
| `pasto-sintetico-tampico` | "los otros 7 modelos sobre pedido" | "Los 9 modelos en existencia; Toscana 18 y 28 para llevar hoy en Obregón 209 Sur" |
| Home | Banner "Temporada de lluvias" fijo | Se elimina; si vuelve, sale de un calendario en `datos.py` con fecha de inicio y fin |
| `blog/index.html` | "Recuperados del Wix con miles de búsquedas", etiquetas de "búsquedas", "22 artículos" | Sin nota interna ni métricas; el conteo sale del build |
| `pasto-en-rollo-tampico` | Tabla con sintético "plástico, áspero", "quema" | "¿Cuál te conviene según tu espacio?" sin desacreditar un producto propio |
| `blog/cuanto-cuesta-jardin-tampico-precios` | Mantenimiento desde $500/mes | Desde $750/mes |
| Home FAQ | "¿Cuánto cuesta el pasto?" sin precio | Bloque A de A04 §7 ($85 / desde $120 / mayoreo desde $60, vigencia) |
| `catalogo.html` y `diseno-jardines-tampico` | "Garantía 30 días" sin condición | "En plantas que sembramos nosotros · ver condiciones" |
| `catalogo.html` (tarjeta sintético) | "Terrazas, canchas y áreas secas" | "Terrazas, azoteas y áreas sin riego" |
| Todas | "Av. Álvaro Obregón 209" | "Av. Álvaro Obregón 209 Sur…" (§ decisiones) |
| Pie de `politicas/` | "Blog de Jardinería" | Pie único |
| `gracias/` | 3 compromisos manuales (2 horas, hoy, 24 h) y emojis | Promesa única + resumen de lo calculado + "Adelantar por WhatsApp" |
| Varios | "Empresa líder", "equipo de expertos" | Hechos: desde 2007, REPSE, +1,500 instalaciones |

### 5.3 Reglas de voz

- Número antes que adjetivo; precio "desde" con IVA y unidad; vigencia visible ("Lista vigente: nov 2026").
- Una admisión honesta por página (Nota de campo): cuándo no conviene comprar.
- Promesa única: "Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h" (decisión del dueño
  2026-09-30; sustituye "en minutos", "hoy mismo", "< 2 horas", "24 h", "4 horas hábiles").
- Riego: "El primer riego lo haces tú: te enseñamos cómo y te dejamos el protocolo de 20 días".
- Garantía de pasto: "Si una sección no arraiga en 15–20 días, la reponemos sin costo, siguiendo el protocolo de riego
  (ver condiciones)". Nunca promesas de pago al terminar.
- Sin escasez inventada: nada de "corte de esta semana disponible" fijo. Un "Próximo corte: viernes {fecha}" solo si el
  dueño lo mantiene desde `datos.py`.
- Superlativos fuera ("el mejor", "líder"). Los LLMs los descartan.

---

## 6. SEO técnico y local

### 6.1 Títulos y descripciones
Keyword + calificador local en los primeros 55–60 caracteres; descripción ≤ 155; sin sufijo de marca en el blog si
no cabe; precio en el título de las transaccionales (p. ej. "Pasto San Agustín en Rollo desde $85/m² · Tampico");
"jardinero" en mantenimiento. Un solo H1 por página. El build falla si un título pasa 65 o una descripción 160.

### 6.2 Rastreo e indexación
- `robots.txt`: quitar los `Disallow` de AdsBot (la exclusión de Shopping va en el feed y Merchant Center); permitir
  CCBot; listar OAI-SearchBot, Claude-SearchBot, Claude-User, Perplexity-User y Applebot-Extended (bloque de A04 §3.1).
- Apex `viverosterra.com` de 307 a 308 en Vercel > Domains.
- `404.html` con menú, buscador de servicios y CTA.
- Eliminar `preview-mapa-cobertura.html`; `noindex` en `/cuestionario`, `/gracias`, `/datos-envio`.
- `sitemap.xml` con `lastmod` real (último commit por archivo), generado por el build para todo el sitio.
- Quitar meta heredadas (`keywords`, `geo.*`, `ai-content-declaration`, `last-modified`) en el parcial de head.
- Bing Webmaster Tools + IndexNow en cada deploy.

### 6.3 Imágenes
`width`/`height` en todas; `srcset`/`sizes` y WebP a ancho real (≤ 1200 px, calidad ~80); hero con `fetchpriority`
y el resto `lazy`; alt descriptivo en fotos de producto; borrar las 115 imágenes sin uso (26 MB) y los PNG/JPG
duplicados; `svgo` al logo (27 KB → ~7 KB). Sin renders presentados como obra real; las fotos que se quedan llevan pie
`FIG.`. El catálogo deja `/api/img` (ver §8.4).

### 6.4 Caché
CSS y JS con hash en el nombre y `public, max-age=31536000, immutable`. Imágenes sin hash: `max-age=604800,
stale-while-revalidate` (o hash si se reemplazan seguido). HTML `max-age=0`.

### 6.5 Enlazado interno
- Blog: 2–3 enlaces contextuales dentro del texto, con anclas variadas, a la money page de su clúster; se elimina el
  bloque idéntico de 6–7 enlaces. Los blogs de precios enlazan a `/precios`; los de sintético, a las 11 ciudades.
- Zonas: enlazadas desde `/zonas`, `/vivero-tampico`, mantenimiento, diseño y los blogs de lluvias y nortes.
- Servicios: bloque "Dónde trabajamos" con las 6 zonas; CTA de mayoreo de `pasto-en-rollo` lleva a la página B2B.
- Breadcrumb visible en todas las páginas de nivel 2–3.
- El build falla con cualquier enlace interno roto o recurso local inexistente.

### 6.6 Mapa de palabras clave

| Página | Principal | Secundarias |
|---|---|---|
| `/` | jardinería en Tampico | viveros terra, vivero Tampico Madero |
| `/pasto-en-rollo-tampico` | pasto en rollo Tampico | pasto San Agustín precio, precio pasto m² Tampico |
| `/mayoreo-pasto-tampico` | pasto en rollo mayoreo | pasto para fraccionamientos, pasto por m² obra |
| `/pasto-sintetico-tampico` | pasto sintético Tampico | pasto sintético instalado, pasto sintético Madero/Altamira |
| `/pasto-sintetico` | comprar pasto sintético con envío | pasto sintético precio m² México |
| `/pasto-sintetico/envio/{ciudad}` | pasto sintético {ciudad} | precio con envío {ciudad} |
| `/pasto-sintetico/perros` | pasto sintético para perros | olor, limpieza, altura recomendada |
| `/diseno-jardines-tampico` | diseño de jardines Tampico | paisajismo Tampico, diseño de jardines Madero |
| `/mantenimiento-jardines-tampico` | mantenimiento de jardines Tampico | jardinero Tampico, mantenimiento de áreas verdes |
| `/sistema-riego-tampico` | riego automático Tampico | riego por aspersión, riego para campos deportivos |
| `/poda-palmas-arboles-tampico` | poda de palmas Tampico | poda de árboles Tampico |
| `/plantas-palmas-arboles-tampico` | vivero de plantas Tampico | plantas, palmas y árboles |
| `/palmas-tropicales-tampico` | venta de palmas Tampico | palma real, coco plumoso precio |
| `/arboles-para-banqueta-tampico` | árboles para banqueta | árboles que no dañan el pavimento |
| `/catalogo` | catálogo de plantas Tampico | arma tu lista de plantas |
| Materiales (4) | {material} Tampico | {material} por camión / costal |
| `/precios` | precios de jardinería Tampico 2026 | cuánto cuesta el pasto, cuánto cuesta un jardín |
| `/vivero-tampico` | vivero en Tampico | vivero Ciudad Madero, horario, cómo llegar |
| `/empresas` | jardinería para empresas Tampico | REPSE jardinería, áreas verdes industriales |
| `/jardineria-{zona}` (6) | jardinería en {zona} | pasto y diseño en {zona} |
| `/nosotros` | Viveros Terra | vivero desde 2007 Ciudad Madero |

---

## 7. AEO / GEO / LLMs

### 7.1 Grafo JSON-LD único
- Un nodo `["LocalBusiness","GardenStore"]` con `@id https://www.viverosterra.com/#negocio` (NAP con "209 Sur" y CP
  89510, `geo`, `openingHoursSpecification`, `areaServed`, `hasMap`, `logo`, `identifier` REPSE 773725, `knowsAbout`,
  `foundingDate` 2007-12-12, `hasOfferCatalog` → `/precios`) y un `WebSite` `#sitio`. Nodo completo en la home y en
  `/nosotros`; en el resto, solo `{"@id": ".../#negocio"}` como `provider`, `seller`, `publisher` y `author`.
- Se eliminan: el `@id` `#localbusiness` de `palmas-mayoreo-proyectos` (y su Instagram equivocado), los
  `LocalBusiness` parciales de servicios y plantas, el `url` de subpágina en `vivero-tampico`, el `SELLER` anónimo de
  `tools/pasto/common.py`, el breadcrumb falso de la home y `aggregateRating` (ya retirado).
- Corregir acentos del JSON-LD de diseño y mantenimiento; `HowTo` + `WebPage` en el protocolo de riego. `FAQPage` se
  mantiene (sirve a LLMs), sin esperar rich results.
- Lo genera `partials.jsonld()` desde `datos.py`; una prueba valida que solo exista un nodo de negocio por `@id`.

### 7.2 `sameAs`
Facebook, Instagram `viverosterramx`, LinkedIn `https://www.linkedin.com/company/viveros-terra-tampico` (sin `il.`),
TikTok `https://www.tiktok.com/@viverosterra` (con https), YouTube `https://www.youtube.com/@viverosterramx`, URL del
Perfil de Negocio de Google y, cuando exista, Wikidata.

### 7.3 Respuesta directa y FAQ
- Cada página de venta abre con una frase citable: entidad + precio + condición + lugar + vigencia (bloques A–H de
  A04 §7 como base, ajustados a "209 Sur").
- Encabezados en forma de pregunta en ciudades, fichas y mayoreo.
- Ninguna respuesta dice solo "escríbenos": siempre un rango o un "desde" (palmas: duranta, bismarckia, cola de zorro,
  triangular; tezontle por camión). El dueño da los precios faltantes.
- Una respuesta idéntica para "¿cuánto cuesta el pasto en rollo en Tampico?" en home, servicio y precios.
- Sección "Lo que no hacemos" (muestras físicas, envío de pasto natural fuera de la región).

### 7.4 E-E-A-T
- `/nosotros` con el párrafo de entidad (bloque B de A04 §7, con "209 Sur" y "+500,000 m²"), historia desde el
  12 dic 2007, REPSE con enlace al padrón, clientes con nombre (si el dueño lo autoriza), fotos reales del vivero.
- Autor `Person` con nombre y página de autor para el blog técnico (lo nombra el dueño).
- `dateModified` y "Actualizado: mes año" visible en servicios, materiales, mayoreo y vivero; las 8 fechas que faltan
  en el blog.

### 7.5 `llms.txt` y `llms-full.txt`
Ambos generados por el build desde `datos.py` y `data.py`: fecha de actualización, párrafo de entidad sin "líder",
perfiles oficiales, `/precios`, `/vivero-tampico`, las 9 fichas, las 11 ciudades, políticas, protocolo, páginas de
plantas y materiales, y los 5–10 artículos más citables. `llms-full.txt` (25–40 KB) añade tablas de precios, fichas,
envío por estado, políticas resumidas, protocolo de 20 días y FAQ deduplicadas.

### 7.6 Tareas fuera del sitio (dueño, con guía)
1. Perfil de Negocio de Google completo (categoría principal "Vivero"; secundarias jardinería, paisajista, proveedor
   de césped; productos con precio; fotos; enlace a `/vivero-tampico`), sin campaña de reseñas.
2. Bing Places y Apple Business Connect.
3. Directorios: Cosmos (dirección vieja "Faja de Oro 805, Loma de Rosales" → Obregón 209 Sur), Cronoshare ("más de 15
   años" → desde 2007; agregar web y teléfono), Sección Amarilla, jardineros.mx. NAP idéntico al sitio.
4. Facebook: datos, horario, web y dirección iguales al sitio.
5. Wikidata: ítem "Viveros Terra" (fundación 2007-12-12, sede Ciudad Madero, web, perfiles); luego su Q-id al `sameAs`.
6. 2–4 notas en medios locales como fuente experta (siembra, nortes) y casos B2B publicados con permiso.

---

## 8. Rendimiento, accesibilidad y seguridad

### 8.1 Fuentes
≤ 2 familias autoalojadas en WOFF2 con subset latin, `font-display: swap`, `preload` de un solo archivo (el peso del
H1). Ejes variables limitados al rango usado (el híbrido con Archivo completo + Fraunces pesó 130 KB, J03 §1; meta
≤ 80 KB en total). Se elimina Google Fonts (~920 ms de bloqueo, A05 §2.3).

### 8.2 Presupuestos
CSS < 30 KB (meta < 10 KB gzip); JS propio < 30 KB gzip por página (tienda incluida); sin `<style>` ni `<script>`
grandes inline salvo CSS crítico del primer pantallazo; GA4 diferido a después de `load`; HTML de la home < 60 KB.

### 8.3 Accesibilidad (WCAG 2.2 AA)
Botón WhatsApp con texto blanco sobre verde campo y glifo `#25D366` (sustituye 1.98:1); tinta secundaria ≥ 4.5:1; foco
≥ 3:1; `<main>`, landmarks y skip-link desde los parciales; labels en los 65 controles; `aria-label` en `#menu-btn` y en
enlaces de íconos; un H1 y sin saltos de encabezado; tarjetas del catálogo como `<button>` reales; listas con scroll
horizontal enfocables; objetivos táctiles ≥ 24 px (meta 44 px en CTA y pie); hero visible sin animación;
`prefers-reduced-motion` respetado; solo se animan `opacity` y `transform`.

### 8.4 Seguridad
- Cabeceras en `vercel.json`: CSP primero en `Report-Only` (Etapa 1) y en enforce cuando el JS inline salga a archivos
  (Etapa 5), con hashes para el JSON-LD; HSTS `max-age=63072000; includeSubDomains; preload`; quitar
  `X-XSS-Protection`; `frame-ancestors 'none'`.
- `/api/img`: las ~118 fotos del catálogo y las 17 de plantas se descargan una vez a `/img/catalogo/<especie>-tampico.webp`
  con dimensiones y alt; el proxy se elimina. Si algo depende de Drive mientras tanto, allowlist de IDs y errores
  registrados (sin `catch {}` vacíos).
- `rel="noopener"` en `target="_blank"` desde los parciales; enlaces de TikTok con https.

---

## 9. Calidad

| Prueba | Qué verifica | Herramienta |
|---|---|---|
| Unitarias del generador | `datos.py`, parciales, JSON-LD, sitemap, llms, Medidor y mensualidades (paridad con `vt-mensualidades.js`) | `python3 -m unittest` (como `tools/pasto/tests`) |
| Consistencia de datos | Recorre todo `public/**/*.html`, `llms*.txt` y JSON-LD: teléfono, domicilio con "209 Sur", precios oficiales, años, clientes, mínimo de mayoreo, conteo de variedades y de artículos, promesa única | Python |
| Palabras prohibidas | "Oasis", marcas de proveedor, nombre del proveedor de la terminal, "MSI", "sin intereses", "muestra(s) gratis", "envío gratis" y "gratis" junto a envío, "pádel"/"cancha" en contexto de sintético, "líder", "pagas cuando", "sobre pedido" en sintético | Python |
| Deriva de parciales | `<nav>`, `<footer>`, barra móvil y head idénticos al canónico; toda página sale del build | Python |
| Enlaces y recursos | Enlaces internos, imágenes y assets existentes; redirects sin cadenas ni destinos rotos | Python |
| SEO on-page | Un H1, canonical, título ≤ 65, descripción ≤ 160, `og:image`, gtag, `width`/`height` en `<img>` | Python |
| JSON-LD | Parseo, un solo nodo `#negocio`, sin `aggregateRating`, referencias por `@id` válidas | Python |
| Consola | 0 `pageerror` ni errores de consola en todas las páginas | Playwright (paquete Python) |
| Accesibilidad | axe-core sobre una página por plantilla: 0 serias/críticas | Playwright + `axe.min.js` versionado en `tools/site/vendor/` |
| Visual | Capturas a 320, 375, 768 y 1440 por plantilla; sin desbordamiento horizontal; comparación contra referencia aprobada | Playwright |
| JS existente | `node --test` archivo por archivo de `public/js/tests` | Node del runner (sin `package.json`) |

**CI:** `.github/workflows/sitio.yml` en cada push y PR: instala Python 3.12 y `playwright` con pip, corre el build,
verifica que `git diff --exit-code public/` quede limpio (el HTML publicado es el que sale del build), luego todas las
pruebas. El repo no tiene `package.json` y no se le agrega: Node solo se usa para `node --test`. Un solo punto de
entrada local: `python3 tools/site/build.py && python3 -m unittest discover -s tools -t .`.

---

## 10. Plan por etapas

Cada etapa se trabaja en una rama, pasa las puertas de revisión (§11) y se publica a producción al aprobarse.

### Etapa 0 · Arreglos urgentes (hecho y en producción)
Mensajes de WhatsApp del catálogo sin SVG · número real en el cuestionario · todos los formularios a
viverosterra@hotmail.com (formsubmit) · `SyntaxError` corregido en 2 posts del blog · pádel y canchas retirados del
contenido de sintético · feed de actividad inventada eliminado · `aggregateRating` autodeclarado retirado del JSON-LD
(queda visible "4.6 en Google (24 reseñas)").

### Etapa 1 · Fundaciones
- **Alcance:**
  1. Medición: `data-cta` + `terra.js` + gtag en las 11 páginas que faltan; línea base de 2 semanas.
  2. `tools/site/` (datos, parciales, build) con todas las páginas pasando por el build (contenido a `content/`).
  3. Tokens y fuentes congelados desde `design/hibrido/`; `terra.css` con los componentes del §4.3.
  4. Header, pie y barra móvil nuevos en las 109 páginas (menú de 6, promesa única, "209 Sur"); `legacy-fixes.css`.
  5. Contradicciones de §5.2 corregidas; botón "+ Agregar" de la tienda dentro de la tarjeta a 1440.
  6. Arreglos técnicos rápidos: AdsBot, CCBot y bots de búsqueda en `robots.txt`; apex 308; `noindex` en
     cuestionario; borrar `preview-mapa-cobertura`; enlace roto de tezontle y PNG faltante; `/precios` y
     `/vivero-tampico` en `llms.txt`; `sameAs` corregido; meta heredadas fuera; CSP en `Report-Only`.
  7. Pruebas del §9 y CI; limpieza de la raíz del repo y de `scripts/` obsoletos.
- **Entregables:** `tools/site/`, `content/`, `terra.css`, `terra.js`, `legacy-fixes.css`, `.github/workflows/sitio.yml`,
  maqueta de referencia de componentes, reporte de línea base.
- **Revisores:** diseño, cumplimiento/QA, SEO/AEO (robots, head, llms), CRO (barra móvil, CTA, medición).
- **Definición de terminado:** 109/109 páginas salen del build; prueba de deriva y de consistencia en verde; 0 palabras
  prohibidas; 0 errores de consola; eventos `generate_lead` y `click_to_call` visibles en GA4 DebugView desde cada tipo
  de página; `curl -I https://viverosterra.com/` responde 308; capturas a 320–1440 sin desbordamiento.
- **Riesgos:** regresión visual al envolver páginas viejas con el header nuevo (mitigación: prefijo `vt-`, capturas
  antes/después por página); deriva de datos durante la migración (mitigación: la prueba de consistencia bloquea).
- **El dueño aporta:** acceso a GA4 y a Vercel > Domains; confirmación de la promesa única; precio del framboyán.

### Etapa 2 · Plantillas y migración por tipo de página (orden por impacto en leads)
- **Alcance, en este orden:**
  1. Home (bifurcación, Medidor, hero con precio y CTA en el primer pantallazo móvil, CTA del hero al Medidor).
  2. Pasto en rollo (una sección de precio y una de proceso; garantía con reposición condicionada).
  3. Sintético Tampico + hub y fichas de la tienda (precio en el primer pantallazo; imagen principal precargada).
  4. Diseño, mantenimiento (un mensaje por plan) y riego.
  5. Mayoreo y palmas para proyectos con plantilla B2B (escalas, clientes, documentación).
  6. Plantas: hub, subcategorías con foto real obligatoria, catálogo con filtros y lista unificada; fotos de `/api/img` a local.
  7. Materiales. 8. Zonas y precios. 9. Blog (índice y 53 posts) con plantilla de artículo. 10. Gracias, políticas,
     cuestionario, protocolo.
  Se publica por lotes (1–2, 3, 4–5, 6–7, 8–10). Al cerrar se borran `tailwind.css`, `design-system.css`,
  `servicios.css`, `tienda-pasto.css` y `legacy-fixes.css`.
- **Entregables:** plantillas del §3.3 en `tools/site/plantillas/`, páginas migradas, capturas de referencia aprobadas.
- **Revisores:** diseño, CRO, cumplimiento/QA en cada lote; SEO/AEO en home, servicios y blog.
- **Definición de terminado:** Lighthouse móvil ≥ 90 Perf y ≥ 98 A11y por plantilla; axe 0 serias; CLS < 0.1; un solo
  `terra.css`; cada CTA con plantilla y `data-cta`; cotizadores dan los mismos totales que `data.py` y
  `vt-mensualidades.js` en los casos de J03 §3.
- **Riesgos:** fotos generadas o retocadas que restan confianza (mitigación: pies `FIG.`, recorte documental, sesión real);
  pérdida de contenido al migrar posts (mitigación: diff de texto visible antes/después).
- **El dueño aporta:** **sesión de fotos real de medio día (muy recomendada)**: corte del viernes, camión cargado,
  cuadrilla instalando en una colonia reconocible, vivero y punto de venta de Obregón 209 Sur; permiso para publicar
  clientes con nombre; precios "desde" de palmas faltantes.

### Etapa 3 · Arquitectura y contenido
- **Alcance:** consolidaciones y 301 del §3.5; páginas nuevas `/nosotros`, `/empresas`, `/zonas`, `/404` y, si se
  confirma, `/poda-palmas-arboles-tampico`; contenido único por zona; reescritura de títulos y H1; enlazado contextual
  del §6.5; breadcrumbs; PDF real de la guía de palmas o retiro de la promesa.
- **Entregables:** redirects en `vercel.json` generados desde `datos.py`, páginas nuevas, mapa de enlaces antes/después.
- **Revisores:** SEO/AEO (canibalización, 301), CRO (recorridos), diseño (páginas nuevas), cumplimiento/QA.
- **Definición de terminado:** 0 redirects en cadena; cada zona con ≥ 3 enlaces entrantes contextuales; cada post con
  ≥ 2 enlaces contextuales a su money page; títulos ≤ 65; cero páginas huérfanas indexables.
- **Riesgos:** pérdida temporal de posiciones por 301 (mitigación: decidir con datos de Search Console, fusionar
  contenido, no solo redirigir).
- **El dueño aporta:** acceso a Search Console; confirmación y precio del servicio de poda; historia y fotos para
  Nosotros; nombre del autor técnico del blog.

### Etapa 4 · SEO, AEO y entidad
- **Alcance:** grafo JSON-LD único (§7.1); `sameAs`; respuesta directa y FAQ con rangos (§7.3); fechas y autor; `llms.txt`
  y `llms-full.txt` generados; `sitemap` con `lastmod` real; Bing Webmaster + IndexNow; guía paso a paso para las tareas
  fuera del sitio del §7.6; primer panel de citas en IA.
- **Revisores:** SEO/AEO (principal), cumplimiento/QA (validación JSON-LD), CRO (que las respuestas no quiten CTA).
- **Definición de terminado:** un solo nodo `#negocio` en todo el sitio; Rich Results Test sin errores en una página por
  plantilla; `llms-full.txt` publicado y probado; Search Console sin errores de datos estructurados.
- **Riesgos:** los directorios externos tardan en actualizarse (no bloquea la etapa).
- **El dueño aporta:** Perfil de Negocio de Google, accesos a Cosmos, Cronoshare y Facebook; datos para Wikidata.

### Etapa 5 · Rendimiento, seguridad y medición final
- **Alcance:** fuentes autoalojadas y presupuesto final; CSS crítico inline; JS inline a archivos; GA4 diferido; imágenes
  (`srcset`, compresión, borrado de 26 MB sin uso, logo optimizado); caché con hash; CSP en enforce, HSTS con preload;
  `/api/img` eliminado; reporte de métricas contra la línea base.
- **Revisores:** cumplimiento/QA (principal), SEO/AEO (CWV), diseño (regresión visual).
- **Definición de terminado:** CWV en verde en Search Console (p75 móvil) o, si aún no hay datos de campo, Lighthouse
  ≥ 90 en todas las plantillas; 0 violaciones de CSP en una semana de `Report-Only` antes de enforce; reporte con leads
  por página, conversión, posiciones y citas en IA frente a la línea base.
- **Riesgos:** la CSP en enforce rompe un script olvidado (mitigación: una semana en `Report-Only` y prueba de consola).
- **El dueño aporta:** revisión del reporte final y decisión de siguientes pasos.

---

## 11. Agentes y gobernanza

| Rol | Agente | Etapas | Revisa |
|---|---|---|---|
| Constructor | `general-purpose` / `tdd-guide` (pruebas primero) | 1–5 | Implementa con pruebas; no publica |
| Revisor de diseño | `design:design-critique` + `a11y-architect` | 1–3, 5 | Fidelidad al híbrido, jerarquía, contraste, foco, capturas 320–1440 |
| Revisor SEO/AEO | `seo-specialist` (con las skills `seo-audit`, `ai-seo`, `schema-markup`) | 1–5 | Títulos, robots, canibalización, 301, JSON-LD, llms, enlazado |
| Revisor CRO | `general-purpose` con la skill `page-cro` | 1–4 | Primer pantallazo móvil, CTA y plantillas de WhatsApp, recorridos, objeciones |
| Revisor de cumplimiento y QA | `code-reviewer` + `python-reviewer` + `e2e-runner` | 1–5 | Reglas del dueño, datos oficiales, pruebas, consola, CI, seguridad (`security-reviewer` en la Etapa 5 y en `/api/img`) |

**Puertas por etapa:**
1. El constructor entrega rama con CI en verde y un resumen de cambios con capturas.
2. Los revisores de la etapa trabajan en paralelo y clasifican hallazgos (crítico, alto, medio, bajo).
3. Críticos y altos se corrigen y se vuelven a revisar; medios se corrigen o se registran con motivo.
4. El dueño ve la vista previa de Vercel y aprueba.
5. Se publica a producción y se verifica en vivo (curl, consola, GA4 DebugView). Si falla algo crítico, se revierte el deploy.

---

## 12. Riesgos, decisiones pendientes y fuera de alcance

**Riesgos:** migración grande de páginas a mano (mitigado por etapas, pruebas de deriva y diff de texto); dependencia de
fotos generadas (mitigado por la sesión real y el tratamiento documental); caída temporal de posiciones por
consolidaciones (mitigado por datos de Search Console); deriva de datos entre Python y JS (paridad probada).

**Decisiones pendientes del dueño:**
1. (Resuelta) Promesa única de respuesta: "menos de 1 hora en horario", decidida por el dueño el 2026-09-30.
2. ¿La poda de palmas y árboles es servicio real? Precio "desde".
3. Precio único del framboyán y precios "desde" de palmas sin precio publicado.
4. Permiso para publicar clientes con nombre y logos (BMW, Taghleef, Gobierno de Tampico, Grupo Velas, Velamar, Flex).
5. Nombre del autor técnico del blog.
6. Año de inicio de la tienda nacional de sintético (para el párrafo de entidad).
7. PDF real de la guía de palmas o retiro de la promesa.
8. ¿Mantendrá una fecha de "próximo corte"? Si no, no se muestra.
9. Correo con dominio propio para el sitio (opcional; los formularios siguen en viverosterra@hotmail.com).

**Fuera de alcance:** checkout o pago en línea; campaña de reseñas de Google; nuevas páginas de ciudades o colonias sin
datos; cambio de framework (Astro/Next); Meta Pixel u otros terceros; rediseño del logo; publicación en Mercado Libre y
Amazon (se menciona como oportunidad).

---

## Anexo · Trazabilidad hallazgo → etapa

| Fuente | Hallazgo (P0/P1 o alto) | Etapa |
|---|---|---|
| A01 P0-1 | Botón "+ Agregar" cortado en el hub a 1440 | 1 |
| A01 P0-2 | Nota "Wix", etiquetas de búsquedas y "22 artículos" en el blog | 1 |
| A01 P0-3 | Banner de lluvias; hero animado que oculta H1 y CTA | 1 (banner) · 2 (hero) |
| A01 P0-4 | Reseñas 4.6 contra 5 | 1 |
| A01 P0-5 | Pie de `politicas` con "Blog de Jardinería" | 1 |
| A01 P0-6 | "Pádel" en blog de sintético | 0 |
| A01 P0-7 | Tabla "plástico, áspero" en pasto en rollo | 1 |
| A01 P1 | Home, servicios, materiales/plantas con foto real, catálogo, blog y gracias en el sistema único; menú y pie únicos | 1 (menú/pie) · 2 |
| A02 QW1–3 | WhatsApp del catálogo con SVG; número falso del cuestionario; actividad inventada | 0 |
| A02 QW4 | Prueba social contradictoria en la home | 1 |
| A02 QW5 | Mayoreo 200 contra 500 m², sin clientes con nombre | 1 (dato) · 2 (plantilla B2B) |
| A02 QW6 | AdsBot bloqueado en diseño, mantenimiento y riego | 1 |
| A02 QW7–8 | Banner estacional; 6 promesas de respuesta | 1 |
| A02 QW9–10 | "Sobre pedido" en sintético Tampico; garantía de plantas sin condición | 1 |
| A02 QW11 | Blog: pádel ($500/mes y "Plan Terra Completo" en Etapa 1) | 0 · 1 |
| A02 QW12–13 | Mensaje por plan en mantenimiento; CTA del hero al cotizador | 2 |
| A02 QW14–15 | Enlace roto y borrador publicado; palmas mayoreo fuera del menú móvil | 1 |
| A02 E1 | Un solo sistema de navegación y breadcrumbs | 1 · 3 |
| A02 E2 | Bifurcación por cliente en la home | 2 |
| A02 E3 | Consolidar plantas | 3 |
| A02 E4–5 | Mayoreo al nivel de palmas; lista unificada de plantas y materiales | 2 |
| A02 E6–7 | Recortar pasto y riego; precio arriba en fichas | 2 |
| A02 E8 | Medición por CTA | 1 |
| A03 HIGH | Cuestionario: número (0) e indexación | 0 · 1 |
| A03 HIGH | LocalBusiness fragmentado | 4 |
| A03 HIGH | `aggregateRating` autodeclarado | 0 |
| A03 HIGH | 71 títulos > 60 caracteres | 3 |
| A03 HIGH | Apex 307 | 1 |
| A03 HIGH | CLS por imágenes y Google Fonts bloqueante | 2 · 5 |
| A03 MED | Borrador publicado; enlace roto y PNG; meta heredadas | 1 |
| A03 MED | `lastmod` masivo; HowTo/FAQ | 4 |
| A03 MED | 404 sin diseño | 3 |
| A03 MED | `alt=""` en fotos de producto | 2 |
| A03 §3.2 | Canibalización (riego, perros, banqueta, interior, palmas, San Agustín, diseño, precios) | 3 |
| A03 §3.4 | Brechas locales (poda, jardinero, precio en título) | 3 |
| A03 §4 | NAP (CP, formato), zonas sin contenido único, enlazado a zonas | 1 (NAP) · 3 |
| A03 §4.3 | Perfil de Negocio de Google | 4 |
| A04 P0-1 | `aggregateRating` | 0 |
| A04 P0-2 | FAQ de la home sin precio | 1 |
| A04 P0-3 | "Pádel" (0) y "canchas" en catálogo (1) | 0 · 1 |
| A04 P0-4 | Framboyán $250 contra $500 | 1 |
| A04 P0-5 | `/precios` y `/vivero-tampico` fuera de `llms.txt`; "líder" | 1 |
| A04 P0-6 | CCBot bloqueado; bots de búsqueda sin entrada | 1 |
| A04 P0-7 | `sameAs` (LinkedIn `il.`, TikTok, YouTube, Instagram de palmas) | 1 |
| A04 P1-8 | Grafo de entidad único | 4 |
| A04 P1-9 | Página Nosotros | 3 |
| A04 P1-10 | `dateModified` y fecha visible | 4 |
| A04 P1-11 | Respuesta directa en mayoreo, fichas y ciudades | 2 · 4 |
| A04 P1-12 | FAQ con "escríbenos" en vez de rango | 4 |
| A04 P1-13 | Acentos del JSON-LD; breadcrumb falso de la home | 4 |
| A04 P1-14 | `llms-full.txt` | 4 |
| A04 P1-15 | HowTo en el protocolo de riego | 4 |
| A04 P2 | Directorios, Wikidata, Bing/Apple, medios, autor | 4 |
| A05 #1–4 | `SyntaxError`, número falso, formularios a 3 destinos, actividad inventada | 0 |
| A05 #5 | Contraste del botón WhatsApp, `--ink-muted`, foco | 1 (componentes) · 2 |
| A05 #6 | gtag en 11 páginas | 1 |
| A05 #7 | Tailwind desfasado sin `package.json` | 1 (`legacy-fixes.css`) · 2 (retiro) |
| A05 #8 | Fuentes autoalojadas, ≤ 2 familias | 1 (decisión) · 5 |
| A05 #9 | `/api/img` proxy abierto y LCP del catálogo | 2 (fotos locales) · 5 (retiro) |
| A05 #10 | Labels, `aria-label`, `<main>`, skip-link | 1 (parciales) · 2 |
| A05 #11 | PDF placeholder de palmas | 3 |
| A05 #12 | Parciales y prueba de paridad | 1 |
| A05 #13 | Assets con hash e `immutable` | 1 · 5 |
| A05 #14 | Imágenes sin dimensiones, pesadas o sin uso | 2 · 5 |
| A05 #15 | CSP, HSTS, `X-XSS-Protection` | 1 (Report-Only) · 5 |
| A05 #16 | GA4 diferido | 5 |
| A05 #17 | Smoke tests, axe y CI | 1 |
| A05 #18–19 | Limpieza del repo; logo con svgo | 1 · 5 |
| J01 | H1 que diga qué se vende; ejemplo de precio sin ambigüedad; plantilla en todos los CTA | 2 |
| J01/J03 | Mensualidades solo con la fórmula oficial; lista de la tienda llega al mensaje; "(0)" oculto | 1 (regla y prueba) · 2 |
| J02 | Etiquetas derechas, máx. 1 por pantalla móvil, cotas solo con medida real, mono ≥ 11 px, sin renders como obra | 1 (tokens) · 2 |
| J03 | CLS del hero; LCP `lazy` en fichas; desbordamiento a 320; mayoreo a $85 bajo 500 m²; bloqueo bajo 25 m²; "gratis" | 2 (y pruebas en 1) |
