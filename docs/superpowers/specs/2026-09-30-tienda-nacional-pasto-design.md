# Tienda nacional de pasto sintético: diseño

Fecha: 2026-09-30 · Estado: aprobado por el dueño en conversación, pendiente de revisión escrita.

## Objetivo

Convertir `/pasto-sintetico` en la tienda nacional de referencia para búsquedas de precio, ciudad y uso
(no para el término genérico "pasto sintético", dominado por Mercado Libre, Home Depot, Sodimac y Amazon).
Su función es pre-cotizar y generar leads que se cierran por WhatsApp. No hay carrito ni pago en línea.

## Decisiones tomadas

| Tema | Decisión |
|---|---|
| Nueva página o mejorar | Mejorar `/pasto-sintetico` en viverosterra.com (camino A). Sin dominio nuevo. |
| Ciudades (11) | CDMX, Guadalajara, Querétaro, San Luis Potosí, León, Puebla, Monterrey, Veracruz, Mérida, Cancún, Villahermosa |
| Promesa de respuesta | "Respondemos en menos de 1 hora en horario" (lun a vie 9 a 18 h, sáb 9 a 14 h) |
| Precio de portada | Modelo más barato (Aruba 10) puesto en el estado; Toscana 28 destacado como "el más vendido" |
| Estilo | El sistema actual: papel, tinta y verde bosque; Geist + Instrument Serif; editorial suizo |
| Muestras físicas | No se ofrecen (regla del dueño) |
| Reseñas | Fuera de alcance por ahora |
| Existencia | Los 9 modelos en existencia para envío nacional; "para llevar hoy" en showroom solo Toscana 18 y 28 |
| Marcas | Nunca mencionar al proveedor ni competidores por nombre; la comparación es genérica |

## Estructura

```
/pasto-sintetico                     tienda nacional (rediseño)
/pasto-sintetico/<modelo>            9 fichas (ajustes: precio puesto, enlace a su zona)
/pasto-sintetico/perros              nueva
/pasto-sintetico/envio/<ciudad>      11 nuevas
/pasto-sintetico-tampico             sin cambios (venta local e instalación)
/blog/cuanto-cuesta-pasto-sintetico-mexico   agrega tabla por ciudad con enlaces
```

Todo se genera con `python3 tools/pasto/build.py`. Módulos nuevos: `tools/pasto/ciudades.py` (datos y página de
ciudad) y `tools/pasto/perros.py`. Precios, zonas y fletes siguen en `data.py` (`MODELOS`, `ZONAS`,
`ZONA_ESTADOS`); `ZONA_ESTADOS` debe seguir igual a `ESTADO_ZONA` de `public/js/tienda-pasto.js`.

## Idea central: precio puesto en tu puerta

- Selector de estado en la portada: "Envíalo a [estado ▾]".
- Al elegir, se recalcula en toda la página el precio por m² con envío: portada, tarjetas, comparador y cotizador.
- Fórmula (igual al cotizador): precio de rollo + (flete de la zona × 1 rollo) / 50 m².
  Para 25 a 50 m² viaja 1 rollo; se muestra el caso de rollo completo como "desde".
- El estado se guarda en el store existente `vt-cotizacion-v1` (campo `estado`, el mismo del cotizador) y se acepta por URL `?estado=<slug>`.
  Las páginas de ciudad enlazan a la tienda con su estado.
- Sin JavaScript, la portada muestra "desde $139/m² + envío desde $900 por rollo" y el selector enlaza a la tabla de envío.

## Tienda `/pasto-sintetico`: orden de secciones (celular)

1. Portada: H1 "Pasto sintético con envío a todo México" + acento "precio puesto en tu puerta";
   selector de estado; precio puesto y días; CTA "Ver modelos con este precio"; foto de jardín real
   (obra-residencial), no de detalle.
2. Franja de confianza: respuesta en menos de 1 h en horario; garantía de fábrica de 3 a 8 años;
   devoluciones en 7 días (enlace a /politicas); factura CFDI 4.0; desde 2007.
3. Los 9 modelos: tarjeta con foto macro, **regla de altura** (fibra a escala de 10 a 35 mm), precio puesto
   del estado elegido, filtros por uso y "Agregar a cotización". Los 9 modelos se muestran en existencia en la tienda nacional, fichas y schema
   (`InStock`; decisión del dueño 2026-09-30). La portada dice "9 modelos en existencia".
   El campo `stock` de `data.py` solo se usa en /pasto-sintetico-tampico para "para llevar hoy" del showroom.
4. "¿Cuál te conviene?" (selector existente).
5. Comparador "¿Viste otro precio?": el cliente escribe total y m² de otra oferta; se muestra su precio por m²
   contra el nuestro puesto en su estado. Sin nombres de competidores.
6. Cotizador completo (existente), arranca con el estado elegido y envía por WhatsApp.
7. Envíos a tu ciudad: 11 tarjetas con precio puesto y días, enlazan a cada página.
8. Tabla de envío por estado (existente, `#envio`).
9. Obras reales, cómo comprar, instálalo tú, preguntas frecuentes, franja Tampico.
- Barra fija inferior en celular: precio puesto + "Cotizar por WhatsApp".

## Página de ciudad `/pasto-sintetico/envio/<ciudad>`

Datos por ciudad en `ciudades.py`: slug, nombre, estado (con la misma clave que `ESTADO_ZONA` del JS, p. ej. "CDMX"), zona, clima (texto propio), 3 modelos recomendados con
razón, 3 a 4 preguntas frecuentes propias.

| Ciudad | Estado | Zona | Desde puesto (Aruba 10) |
|---|---|---|---|
| CDMX | Ciudad de México | A | $157/m² |
| Guadalajara | Jalisco | A | $157/m² |
| Querétaro | Querétaro | A | $157/m² |
| San Luis Potosí | San Luis Potosí | A | $157/m² |
| León | Guanajuato | A | $157/m² |
| Puebla | Puebla | A | $157/m² |
| Monterrey | Nuevo León | B | $162/m² |
| Veracruz | Veracruz | B | $162/m² |
| Mérida | Yucatán | C | $167/m² |
| Cancún | Quintana Roo | C | $167/m² |
| Villahermosa | Tabasco | C | $167/m² |

Los precios se calculan desde `data.py`, no se escriben a mano.

Secciones: portada con precio puesto y días · totales de ejemplo 25 / 50 / 100 m² (material + flete) ·
modelo según el clima de la ciudad (3 modelos con precio puesto) · cómo llega (paquetería, guía, rollo de 2 m,
qué revisar al recibir) · instálalo tú (resumen + enlace a la guía; aclarar que la instalación es solo en
Tampico, Madero y Altamira) · preguntas frecuentes · CTA a la tienda con `?estado=` y WhatsApp con la ciudad.

Schema: `Offer` con `OfferShippingDetails` al estado, `FAQPage`, `BreadcrumbList`.
Mínimo de contenido propio por ciudad: clima, recomendación y preguntas no se repiten entre ciudades.

## Página `/pasto-sintetico/perros`

Qué elegir (densidad, resistencia de fibra, drenaje de orina, limpieza del olor) · 3 modelos recomendados con
precio puesto · instalación y limpieza para mascotas · preguntas: ¿se calienta?, ¿lo rasguñan?, ¿huele?,
¿cómo se lava? Solo afirmaciones presentes en las fichas técnicas (`COMMON_TREATMENTS` incluye antibacterial).
Sin prometer propiedades no documentadas.

## Fichas de modelo

Agregan el selector de estado y el precio puesto; enlazan a la página de ciudad de la zona elegida cuando exista.

## Diseño visual y calidad

- Sistema existente (`tienda-pasto.css`). Nuevos componentes: selector de estado de la portada, regla de altura,
  comparador, tarjetas de ciudad.
- Movimiento: solo el cambio de precio (150 a 250 ms, opacidad/transform); desactivado con `prefers-reduced-motion`.
- Accesibilidad: contraste AA, objetivos táctiles de 44 px, `label` visible en selector y campos,
  `aria-live="polite"` en el precio recalculado, sin desplazamiento horizontal a 320 px.
- Rendimiento: imágenes WebP con `srcset` y dimensiones, menos de 150 KB por imagen; JS sin dependencias.
- Pruebas: capturas a 375, 768, 1024 y 1440; verificar precio puesto por zona A, B y C contra el cotizador;
  JSON-LD válido; sin errores en consola.

## Fuera de alcance

Carrito y pago en línea · reseñas · dominio nuevo · Mercado Libre / Amazon · muestras físicas ·
Merchant Center (lo conecta el dueño con el feed existente `feed-pasto-sintetico.xml`).

## Riesgos

- Páginas de ciudad percibidas como relleno: mitigado con clima, recomendación y preguntas propias.
- Diferencia entre JS y `data.py` en zonas: mantener una sola lista o verificar en el build.
- Precio puesto "desde" puede diferir del flete exacto: se aclara "te confirmamos el flete con tu código postal".
