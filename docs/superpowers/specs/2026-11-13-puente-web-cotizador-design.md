# Puente web → cotizador (tienda de pasto sintético, subproyecto 2)

Aprobado por el dueño el 2026-11-13.

## Objetivo

El cliente manda su cálculo de la web por WhatsApp sin escribir nada; el equipo pega ese mensaje en el cotizador de
Netlify y la cotización se llena sola (entrega, m² y 3 modelos).

## Lado del cliente (web)

- Sin casillas nuevas: WhatsApp ya trae nombre y número; la ciudad y la dirección se piden después, con el formulario de
  datos de envío del cotizador (cuando el cliente ya dijo que sí).
- Al final del mensaje: `Folio web: <folio>`. El resto del mensaje no cambia.
- Bajo el botón del cotizador, cuando hay folio y entrega elegida: "Ya tienes todo listo, solo falta mandarlo · Tu
  folio: <b>T28-40-NL</b>" y "Te respondemos con tu cotización formal en PDF. Sin compromiso y sin llenar
  formularios." El botón cambia a "Enviar mi cotización por WhatsApp".
- Aplica al cotizador de ficha, hub y Tampico, a la barra fija (usa el mismo mensaje) y a la lista ("Mi lista").
- Psicología aplicada (ética): energía de activación mínima (mensaje ya escrito), una acción principal, cierre de lo
  empezado (resumen + "solo falta mandarlo"), aversión al arrepentimiento ("sin compromiso"), reciprocidad (PDF formal),
  folio como algo propio. Sin urgencia falsa ni palabras prohibidas.

## Folio

- Modelo: inicial del slug + altura (A10, T18, C20, I25, T28, V30, J35, M35, B35); se deriva igual de la clave del
  cotizador (`toscana28` → T28).
- `<modelo>-<m²>`; varios modelos unidos con `+`; al final la entrega: abreviatura del estado (NL, JAL, CDMX…),
  `REC` (recoge en showroom) o `LOC` (envío local Tampico/Madero/Altamira). Sin entrega elegida, sin sufijo.
- Ejemplos: `T28-40-NL`, `T28-40+I25-30-JAL`, `T18-12-REC`, `B35-60`.
- Código en `public/js/vt-folio.js` (puro, Node y navegador): `folio`, `leerFolio`, `completarModelos`.

## Lado del equipo (cotizador de Netlify)

- Recuadro "Pegar mensaje de la web" + botón "Rellenar" al inicio de la tarjeta 1.
- Llena entrega (`showroom`, `local` o `<zona>|<estado>`), m² y 3 modelos.
- Un modelo: se completan con sus vecinos de precio (rollo); si es el más barato, los dos siguientes; si es el más
  caro, los dos anteriores. Lista: se usan sus modelos (máximo 3); si son 2, se agrega el vecino más cercano.
- m² distintos en la lista: se toma el mayor y se avisa.
- Sin folio o folio ilegible: no cambia nada y lo dice.
- Toscana 28: la etiqueta "El más vendido" (prohibida) pasa a "Uso familiar diario" (la de la web).
- El lector es el mismo `vt-folio.js` incrustado tal cual. Entrega: zip nuevo que el dueño sube a Netlify.

## Pruebas

- `public/js/tests/vt-folio.test.js`: folio de todos los modelos y estados, ida y vuelta, vecinos, errores.
- Python: los 9 modelos de `tools/pasto/data.py` dan códigos únicos; los 32 estados de la tienda tienen abreviatura.
- Navegador (solo localhost): cotizar en la web, copiar el mensaje, pegarlo en el cotizador y comparar. Sin abrir
  WhatsApp ni enviar nada.

## Fuera de alcance

Ciudad/C.P. en la web, enlaces al cotizador en el mensaje, cambios al resto del mensaje.
