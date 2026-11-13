# Pasto sintético en Tampico: el material primero (subproyecto 1 de la tienda)

Fecha: 2026-11-12 · Aprobado por el dueño ("si adelante como lo propones").

## Problema
En Google, «pasto sintético tampico» muestra «Pasto Sintético Tampico Instalado desde $446.60/m²». Quien busca
comprar el material para instalarlo él mismo ve primero el precio más alto. La página ya vende material, pero lo
presenta como segunda opción.

## Decisión (opción A)
Una sola página, la misma URL `/pasto-sintetico-tampico`, con el material primero y la instalación como segunda
opción. Sin fotos nuevas, sin precios nuevos, sin plazos nuevos; todo sale de `tools/pasto/data.py` y `datos.py`.

## Cambios
1. **Título** (≤60): `Pasto Sintético Tampico desde $139/m² · Material o Instalado` (139 = rollo más barato de data.MODELOS).
2. **Descripción** (≤155): `Compra pasto sintético en Tampico desde $139/m², cortado a tu medida; Toscana 18 y 28 para
   llevar hoy en Cd. Madero. Instalado desde $446.60/m².` (modelos en existencia y precio instalado calculados).
3. **H1**: `Pasto sintético en Tampico <serif>para llevar o instalado</serif>`.
4. **Lede**: `Llévate el material del showroom en Cd. Madero desde $139/m², cortado a tu medida, o déjanos la
   instalación completa. En la región desde 2007.`
5. **Etiqueta de precio**: monto principal «Solo el material · desde $139 /m²»; filas «Toscana 18 y 28 · para llevar
   hoy» e «Instalado con material y colocación · desde $446.60 /m²».
6. **Respuesta «En corto»** (`respuestas.py`): empieza por el material (dónde, desde $139/m², desde 2 m², existencia
   hoy) y después el instalado de $446.60 a $754/m² con preparación aparte.
7. **Orden de secciones**: portada → En corto → opciones → calculadora → precio → prueba (obras y opiniones) → obras de
   la región → proceso → garantía → pago → preguntas → showroom → cierre nacional. La plantilla acepta un orden propio
   por página (`k["orden"]`); las demás páginas no cambian.
8. **Opciones**: «Compras el material» pasa a ser la recomendada (`rec`); la instalación deja de serlo.
9. **Preguntas**: las de compra primero (dónde, precio por m², mínimo, recoger hoy, envío local, clima); nueva
   «¿Puedo instalarlo yo mismo?» respondida solo con lo que existe: kit (pegamento, cinta, clavos y guía) y el artículo
   `/blog/como-instalar-pasto-sintetico`.
10. **JSON-LD**: además del Service de instalación, un Product «Pasto sintético en rollo (material)» con AggregateOffer de
    $139 a $399/m² (mín. rollo y máx. t1 de data.MODELOS), MXN, vendido por `#negocio`.
11. **Barra de compra**: «Material desde $139/m²».
12. **«Sin costo» en la calculadora** (componentes_tienda.py y tienda-pasto.js, «Recoger en showroom»): pasa a «$0»
    (frase prohibida; afecta también la tienda nacional, donde dice lo mismo).

## Pruebas
Nuevo `tests/test_tampico_material.py`: título, descripción y H1 con el material primero y ≤60/≤155; orden de
secciones (opciones y calculadora antes de la prueba); opción recomendada = material; primera pregunta de compra y la
nueva de instalar uno mismo; Product con AggregateOffer de los datos; «En corto» empieza con el material; ningún
«Sin costo» en el HTML de la tienda. Paridad: cambios de meta declarados en `PARIDAD`. Suite completa + pruebas JS.

## Fuera de alcance
Puente sitio→cotizador (subproyecto 2) y SEO nacional (subproyecto 3).
