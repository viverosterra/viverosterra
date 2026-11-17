# Tienda SEO nacional · Entrega C: ciudades de verdad (2026-11-16)

## Problema
Las 11 páginas `/pasto-sintetico/envio/<ciudad>` compartían 39 % del texto (Jaccard de 5-gramas; hasta 49 % entre
León y Puebla), traían la opinión de una cafetería de Tampico y no enlazaban entre sí. Faltaban 8 ciudades grandes
cuyo estado ya tenía flete.

## Qué cambia
- `tools/pasto/ciudades.py`: por ciudad, `terreno` (cómo preparar la base con el suelo y clima local, en condicional
  cuando depende del terreno), `ejemplo` (espacio de ejemplo largo × ancho y, opcional, el modelo) y `coords`
  (aproximadas, solo para elegir las cercanas). 8 ciudades nuevas (`NUEVAS`): Saltillo, Torreón, Chihuahua,
  Hermosillo, Tijuana, Aguascalientes, Toluca y Morelia, con intro, clima, 3 modelos y 3 preguntas propias.
- `contenido/ciudad.py`: sección «Antes de instalar en <ciudad>» con tres preguntas: terreno; «¿Cuánto pido para
  <espacio>?» calculado con `rollos.corte` y las reglas de precio del cotizador (aviso de rollo completo cuando cuesta
  lo mismo o menos); «¿Y si estoy en otra ciudad cerca?» con las 3 más cercanas y la tabla de envío por estado.
  Textos fijos (envío, elegir sin muestra, quién instala) más cortos, sin perder los datos.
- `plantillas/tienda_guia.py`: en las ciudades ya no va la opinión de Tampico (sigue en perros); queda la
  calificación de Google.
- `generar.py`: las 8 rutas nuevas entran en `NUEVAS` (sin captura de paridad). Hub, sitemap, llms.txt y la tabla de
  32 estados las toman de `CIUDADES`.

## Reglas respetadas
Nada inventado: sin cifras de clima, sin testimonios, los ejemplos dicen «ejemplo» implícito («¿Cuánto pido para un
patio de…?») y no se presentan como el patio típico. Sin plazos en títulos ni descripciones. Sin palabras prohibidas.

## Resultado
Traslape medio 39 % → 32 % con 19 ciudades (prueba: falla arriba de 0.35). Pruebas: tests/test_ciudades_c.py,
test_tienda (conteos y umbral), tools/pasto/tests/test_ciudades.py.
