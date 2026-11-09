# Registro de Nochebuenas en Google Sheets

Con esto, cada vez que alguien manda su cotización de Nochebuenas por WhatsApp desde la página, se agrega un renglón a una hoja de cálculo de Google.

**Qué significa cada renglón:** la persona le dio clic a enviar. **No es un pedido confirmado.** El pedido real es el que se cierra por WhatsApp.

**Importante:** cualquiera que tenga la URL puede escribir en la hoja. Toma cada renglón como una señal de interés y **no prepares nada sin confirmarlo por WhatsApp**.

**Qué se guarda:** fecha y hora, qué plantas cotizó, piezas, total, zona, fecha deseada, tipo de cliente, si pidió factura y de qué anuncio o página llegó. **No se guarda nombre ni teléfono.**

Son unos 10 minutos y solo se hace una vez. Usa la cuenta de Google del vivero, porque los renglones se guardarán en esa cuenta.

## Primera vez: instalarlo

### A. Crear la hoja

1. Entra a [sheets.google.com](https://sheets.google.com) con la cuenta del vivero.
2. Abre una hoja de cálculo en blanco.
3. Arriba a la izquierda, donde dice "Hoja de cálculo sin título", escribe `Pedidos Nochebuenas`.

### B. Pegar el código

4. En el menú de arriba, da clic en **Extensiones** y luego en **Apps Script**. Se abre otra pestaña con un editor.
5. Borra todo lo que aparezca escrito en el editor.
6. Abre el archivo `nochebuenas-pedidos.gs` que está en esta misma carpeta (si no lo tienes a la mano, pídeselo a Claude). Copia todo su contenido y pégalo en el editor.
7. Da clic en el ícono de disquete (**Guardar proyecto**), arriba.

### C. Publicarlo

8. Arriba a la derecha, da clic en el botón azul **Implementar** y luego en **Nueva implementación**.
9. Junto a "Seleccionar tipo", da clic en el engrane y elige **Aplicación web**.
10. Llena las opciones así:
    - **Descripción:** `Nochebuenas 2026`
    - **Ejecutar como:** **Yo** (aparece tu correo)
    - **Quién tiene acceso:** **Cualquier persona** (puede aparecer como "Cualquier usuario"). No elijas la opción que dice "con cuenta de Google", porque el registro no funcionaría.
11. Da clic en **Implementar**.
12. Google te va a pedir permiso. Da clic en **Autorizar acceso** y elige la cuenta del vivero.
13. Si sale un aviso de "Google no ha verificado esta aplicación", es normal, porque el programa es tuyo y no de una empresa externa. Da clic en **Configuración avanzada**, luego en **Ir a...** (el nombre de tu proyecto) y al final en **Permitir**.

### D. Mandar la URL

14. Al terminar aparece un recuadro con una **URL de aplicación web**, una dirección larga que termina en `/exec`. Da clic en **Copiar**.
15. **Mándale esa URL a Claude** y dile que es para pegarla en el sitio de Nochebuenas. Mientras no se pegue, la página funciona normal, pero no se registra nada.

Si abres esa URL en tu navegador vas a ver un mensaje de error. Es normal: la dirección solo sirve para recibir datos de la página.

### E. Comprobar que funciona

16. Cuando Claude te avise que ya quedó, entra a la página de Nochebuenas, arma una cotización y da clic en enviar por WhatsApp. No hace falta que mandes el mensaje.
17. Abre tu hoja de cálculo. Abajo debe aparecer una pestaña nueva, **Pedidos Nochebuenas 2026**, con los títulos y un renglón. Esa pestaña se crea sola.

La primera pestaña, "Hoja 1", se queda vacía. Puedes ignorarla.

## Si un día cambia el código

Si Claude te da una versión nueva del archivo, pegarla y guardarla **no basta**: la página seguirá usando la versión anterior hasta que publiques una nueva.

1. En la hoja, entra a **Extensiones** y luego a **Apps Script**.
2. Borra todo, pega el código nuevo y da clic en **Guardar proyecto**.
3. Da clic en **Implementar** y luego en **Gestionar implementaciones**.
4. Da clic en el ícono de lápiz (**Editar**), arriba a la derecha.
5. En **Versión**, elige **Nueva versión**.
6. Da clic en **Implementar**.

Así la URL sigue siendo la misma y no hay que cambiar nada en el sitio. No uses "Nueva implementación" para esto, porque crea una URL distinta. Si por error ya la usaste, manda la URL nueva a Claude.

## Si no llegan filas

Si pasan 2 días con visitas y no llegan filas, entra a **Extensiones**, luego **Apps Script** y, en el menú de la izquierda, a **Ejecuciones**. Ahí se ve si hubo errores. También puede ser un límite: el registro ignora más de 30 clics por minuto o 2,000 por día, y deja de escribir cuando la hoja pasa de 5,000 renglones.

## Si quieres cambiar la URL

Hazlo si la dirección se filtró o si la hoja empieza a llenarse de renglones raros.

1. En Apps Script, da clic en **Implementar** y luego en **Nueva implementación**. Repite los pasos 9 a 11 y copia la URL nueva.
2. Manda la URL nueva a Claude para pegarla en el sitio.
3. Cuando el sitio ya use la nueva, entra a **Implementar**, **Gestionar implementaciones**, y archiva la anterior. Así la URL vieja deja de escribir en la hoja.

## No hagas esto en la hoja

- No le cambies el nombre a la pestaña **Pedidos Nochebuenas 2026**. Si lo haces, se crea otra pestaña vacía y los renglones nuevos se van para allá.
- No borres ni muevas la primera fila, la de los títulos.

Puedes agregar filtros, colores o columnas a la derecha de la última columna sin problema.
