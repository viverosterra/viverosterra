# Mensualidades con tarjeta (Clip): diseño

Fecha: 2026-11-04 · Estado: estrategia aprobada en conversación (plan B), pendiente de revisión escrita.

## Decisiones del dueño

| Tema | Decisión |
|---|---|
| Modelo | Plan B: mensualidades con el costo de Clip incluido en el precio a plazos. Viveros Terra recibe el total íntegro. |
| Nombre | "Mensualidades con tarjeta de crédito" / "pagos a meses". Nunca "MSI", "meses sin intereses", "sin intereses" ni "0%". |
| Contado | Transferencia, efectivo o tarjeta en una sola exhibición: mismo precio. El 3.6% del pago único con tarjeta lo absorbe Viveros Terra. |
| Comisión de Clip | Se suma a la estándar: 3.6% + tasa del plazo, más IVA sobre ambas (confirmado por el dueño y por la calculadora del distribuidor de Clip). |
| Plazos por monto de contado | Menos de $2,000: sin mensualidades · $2,000 a $4,999: 3 · $5,000 a $14,999: 3 y 6 · $15,000 o más: 3, 6, 9 y 12. Mínimo de Clip: $299. |

## Fórmula (igual a la calculadora de Clip)

```
total_a_plazos = contado / (1 − (0.036 + tasa_plazo) × 1.16)
tasa_plazo: 3 → 0.0457 · 6 → 0.0757 · 9 → 0.1107 · 12 → 0.1277
mensualidad ≈ total_a_plazos / plazo
```

Factor fijo por plazo: 3 → +10.5% · 6 → +14.9% · 9 → +20.5% · 12 → +23.4%.
Redondeo: el total a plazos se redondea hacia arriba al peso; la mensualidad se muestra como aproximada
porque el banco emisor hace la división. Nunca se usa contado × (1 + %): con ese cálculo el negocio recibe menos.

Ejemplo (Toscana 28, 50 m², Nuevo León, contado $11,100):

| Forma de pago | Mensualidad | Total | Diferencia |
|---|---|---|---|
| Contado | — | $11,100 | — |
| 3 mensualidades | ≈ $4,087 | $12,262 | +$1,162 |
| 6 mensualidades | ≈ $2,125 | $12,752 | +$1,652 |
| 9 mensualidades | ≈ $1,486 | $13,376 | +$2,276 |
| 12 mensualidades | ≈ $1,142 | $13,702 | +$2,602 |

## Reglas de comunicación

- El precio de contado es el titular en todas partes; las mensualidades son la alternativa.
- Toda mensualidad va junto a su total y a la diferencia contra contado ("+$X frente a contado").
- Se presenta como precio en mensualidades, no como "comisión" ni "recargo por pagar con tarjeta".
- Texto fijo: "Precio en mensualidades con tarjeta de crédito. Contado (transferencia, efectivo o tarjeta en
  una exhibición) es el precio más bajo. Montos aproximados: el banco emisor debe aceptar el plan y define el
  redondeo. Te confirmamos el total antes de enviarte el link de pago."
- Línea de franqueza: "Pagando de contado te ahorras $X".

## Dónde aparece (tienda nacional de pasto sintético)

1. **Cotizador del hub y de las 9 fichas**: bloque "¿Cómo prefieres pagar?" entre el total y los botones.
   Radio cards apiladas (contado preseleccionado), cada una con mensualidad, total y diferencia; los plazos
   que no aplican por monto se muestran deshabilitados con "desde $X". Encima, el tríptico
   "Hoy · Al mes · Total" y la **regla de pagos** (gemela de la regla de altura: una marca por mes, total al final).
2. **Mensaje de WhatsApp y lista de cotización**: "Forma de pago: 6 mensualidades de ≈ $2,125 con tarjeta de
   crédito (total $12,752)" o "Forma de pago: contado". En la lista, un selector compacto de plan para todo el pedido.
3. **Barra fija en celular**: segunda línea "o hasta N mensualidades con tarjeta" cuando el monto lo permite.
4. **Tarjetas de modelo**: una línea discreta "Paga en mensualidades con tarjeta". Sin montos ni insignias.
5. **Portada de la tienda**: una frase bajo el selector de estado con enlace al cotizador. Sin montos.
6. **Páginas de ciudad**: columna "12 mensualidades" (o el plazo máximo que aplique) en la tabla de 25/50/100 m²,
   calculada en el build.
7. **/precios y /politicas#mensualidades**: tabla de plazos con factor, mínimos por monto y condiciones.

Nunca: mantenimiento mensual, compras de menos de $2,000, ventanas emergentes.

## Dónde aparece (servicios locales en Tampico, Madero y Altamira)

Aprobado por el dueño el 2026-11-04 para pasto natural instalado, pasto sintético instalado, diseño de jardín y riego.
Estos servicios se cotizan después de medir, así que la mensualidad se muestra sobre un monto que el cliente conoce.

8. **Simulador de mensualidades** (componente reutilizable): campo "Monto de tu cotización" con radio cards de
   plazos, el mismo tríptico y la misma regla de pagos. Va en las páginas de pasto en rollo, sintético en Tampico,
   diseño de jardines y riego, después de la sección de precios. Botón "Enviar por WhatsApp" con el plan elegido.
9. **Portada de cada servicio** (tools/servicios): una línea bajo el precio, "Paga en mensualidades con tarjeta de
   crédito en cotizaciones desde $2,000". Sin montos.
10. **Diseño de jardines**: en las tarjetas de los planes de precio fijo, la opción a plazos que aplique por monto
    (Esencial $3,000 → 3; Completo $6,500 → 3 y 6; Premium desde $18,000 → hasta 12), con total y diferencia.
11. **Pasto sintético en Tampico** (/pasto-sintetico-tampico): su cotizador usa el mismo bloque del punto 1.
12. **Mensaje de WhatsApp de la cotización formal**: el equipo incluye la tabla de plazos del monto cotizado
    (plantilla en el plan).

## Datos y código

- Tasas, IVA, umbrales y plazos en `tools/pasto/data.py` (`MENSUALIDADES`) y la misma tabla en
  `public/js/tienda-pasto.js`; una prueba de paridad Python ↔ JS como la de zonas.
- Función pura en `public/js/vt-landed.js` (o un módulo hermano) `planesMensualidades(contado)` →
  lista de {plazo, total, mensualidad, diferencia, disponible}, con pruebas `node --test`.
- El store `vt-cotizacion-v1` guarda `plan` (0 = contado; 3/6/9/12), validado contra la lista permitida.
- Python calcula las columnas de las páginas de ciudad con la misma fórmula (prueba de que JS y Python
  dan el mismo total para los cuatro ejemplos de arriba).

## Pruebas y verificación

- Totales exactos de la tabla de ejemplo en Python y JS.
- Umbrales: $1,999 sin planes; $2,000 solo 3; $5,000 3 y 6; $15,000 los cuatro.
- Ningún texto generado contiene "MSI", "sin intereses", "0%", "recargo" ni "comisión por tarjeta".
- Capturas a 375 y 1440 del cotizador con contado y con 12 mensualidades; foco de teclado en las radio cards.

## Riesgos

- Legal: PROFECO sanciona cobrar extra por pagar con tarjeta. Mitigación: pago único con tarjeta al precio de
  contado, precio a plazos con total y diferencia visibles, sin "sin intereses". El dueño confirmará con Clip por
  escrito que su contrato permite un precio distinto en mensualidades.
- Si Clip cambia tasas, se actualizan en un solo lugar y el build regenera todo.

## Publicidad (fuera del código)

Copys con "hasta 12 mensualidades con tarjeta de crédito; te mostramos el total antes de pagar".
Buen Fin con gancho distinto a "sin intereses"; seguimiento por WhatsApp con la mensualidad y el total.
