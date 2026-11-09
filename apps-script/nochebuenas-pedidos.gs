// Registra en Google Sheets cada clic de envío del cotizador de Nochebuenas.
// Son clics, no pedidos confirmados. No guarda nombre ni teléfono.
// Instrucciones de instalación: apps-script/README.md

const HOJA = 'Pedidos Nochebuenas 2026';
const COLUMNAS = ['fecha_hora','lineas','piezas','escalon','total','preventa','zona','fecha_deseada','tipo_cliente','factura','origen','utm_source','utm_medium','utm_campaign'];
const ESCALONES = ['Menudeo','Mayoreo','Mayoreo Plus','Proyecto'];
const ZONAS = ['','Tampico','Madero','Altamira','Recojo en vivero'];
const TIPOS = ['','Hogar','Empresa/regalo','Restaurante/hotel','Comercio/plaza','Gobierno','Evento/posada','Iglesia/escuela'];
const CORTES = [1, 12, 50, 200];
const PRECIO_MAXIMO = 1195;
const MAX_CUERPO = 5000, MAX_LINEAS_TEXTO = 1500, MAX_POR_MINUTO = 30, MAX_POR_DIA = 2000, MAX_FILAS = 5000;
const SEGUNDOS_MAX_CACHE = 21600; // el máximo que admite CacheService: cada escritura renueva el contador del día
const LINEA = /^([1-9]\d{0,3}) × (?:Maceta [567]"|Colgante|Macetón 12") (?:Roja|Rosa|Jaspeada)$/;
const UTM = /^[\w.\-]{0,100}$/;
const FECHA_ISO = /^(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))?$/;

function limpiar(valor, max) {
  // Quita controles y espacios de orilla ANTES de revisar el primer carácter:
  // si no, " =1+1" o "\n=1+1" se saltarían la neutralización de fórmulas.
  const texto = String(valor == null ? '' : valor).replace(/[\u0000-\u001f\u007f]+/g, ' ').trim().slice(0, max);
  return /^[=+\-@]/.test(texto) ? "'" + texto : texto;
}
function numero(valor, max) {
  // Sin Number(): null, '', true y [5] se convertirían en números válidos.
  if (!Number.isFinite(valor) || valor < 0 || valor > max) throw new Error('numero');
  return Math.round(valor);
}
function siNo(valor) {
  // Sin esto, el texto "false" contaría como verdadero.
  if (typeof valor !== 'boolean') throw new Error('booleano');
  return valor ? 'sí' : 'no';
}
function deCatalogo(valor, lista) {
  const v = valor == null ? '' : valor;
  if (lista.indexOf(v) < 0) throw new Error('catalogo');
  return v;
}
function fecha(valor) {
  const v = valor == null ? '' : valor;
  if (typeof v !== 'string' || !FECHA_ISO.test(v)) throw new Error('fecha');
  return v;
}
function lineasValidas(valor, piezas) {
  if (typeof valor !== 'string' || valor.length > MAX_LINEAS_TEXTO) throw new Error('lineas');
  const suma = valor.split(' | ').reduce((total, linea) => {
    const m = LINEA.exec(linea);
    if (!m) throw new Error('lineas');
    return total + Number(m[1]);
  }, 0);
  if (suma !== piezas) throw new Error('piezas');
  return valor;
}
function escalonDe(valor, piezas) {
  const esperado = CORTES.reduce((actual, corte, i) => (piezas >= corte ? i : actual), -1);
  if (deCatalogo(valor, ESCALONES) !== ESCALONES[esperado]) throw new Error('escalon');
  return valor;
}
function utm(valor) {
  const texto = valor == null ? '' : String(valor);
  return UTM.test(texto) ? limpiar(texto, 100) : '';
}
function fila(d, ahora) {
  const piezas = numero(d.piezas, 100000);
  return [ahora, lineasValidas(d.lineas, piezas), piezas, escalonDe(d.escalon, piezas), numero(d.total, piezas * PRECIO_MAXIMO), siNo(d.preventa),
    deCatalogo(d.zona, ZONAS), fecha(d.fecha_deseada), deCatalogo(d.tipo_cliente, TIPOS), siNo(d.factura),
    limpiar(d.origen, 200), utm(d.utm_source), utm(d.utm_medium), utm(d.utm_campaign)];
}
function excedido() {
  // Una clave por minuto: con una sola clave, cada put renovaría la caducidad
  // y el contador nunca volvería a cero mientras llegara un clic por minuto.
  // Se cuenta fuera del candado a propósito: es un freno aproximado y una
  // avalancha no debe formarse a esperar el candado.
  const cache = CacheService.getScriptCache();
  const minuto = contar(cache, 'n' + Math.floor(Date.now() / 60000), 120);
  const dia = contar(cache, 'd' + new Date().toISOString().slice(0, 10), SEGUNDOS_MAX_CACHE);
  return minuto > MAX_POR_MINUTO || dia > MAX_POR_DIA;
}
function contar(cache, clave, segundos) {
  const n = Number(cache.get(clave) || 0) + 1;
  cache.put(clave, String(n), segundos);
  return n;
}
function ignorar(motivo) {
  console.error('nochebuenas ignorado', motivo);
  return 'ignorado';
}
function hoja() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  const h = libro.getSheetByName(HOJA) || libro.insertSheet(HOJA);
  if (h.getLastRow() === 0) h.appendRow(COLUMNAS);
  return h;
}
function registrar(e) {
  const cuerpo = e && e.postData && e.postData.contents || '';
  if (cuerpo.length > MAX_CUERPO) return ignorar('cuerpo');
  // Se valida antes de contar: lo inválido no gasta el cupo de los clics reales.
  const nueva = fila(JSON.parse(cuerpo), new Date());
  if (excedido()) return ignorar('limite');
  const lock = LockService.getScriptLock();
  lock.waitLock(5000);
  // El try empieza después de waitLock: solo se suelta un candado que se tomó.
  try {
    const h = hoja();
    if (h.getLastRow() > MAX_FILAS) return ignorar('hoja llena');
    h.appendRow(nueva);
    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }
  return 'ok';
}
function doPost(e) {
  // Cualquier falla, incluida la de soltar el candado, termina aquí: al
  // cliente solo le llega "error"; el detalle queda en el registro del script.
  try {
    return respuesta(registrar(e));
  } catch (err) {
    console.error('nochebuenas', err && err.message);
    return respuesta('error');
  }
}
function respuesta(texto) { return ContentService.createTextOutput(texto); }
