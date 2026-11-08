const test = require('node:test');
const assert = require('node:assert/strict');
const c = require('../vt-catalogo.js');
const casos = require('./casos-catalogo.json');

test('el mensaje de la lista es el mismo que armaba sendWA() en main', () => {
  for (const { lista, mensaje } of casos.mensajes) assert.equal(c.mensajeLista(lista), mensaje);
  assert.equal(c.mensajeLista([]), '');
  assert.ok(c.enlaceLista(casos.mensajes[0].lista).startsWith('https://wa.me/528333268008?text=Hola%20Viveros%20Terra'));
});

test('agregar: misma especie y tamaño actualiza la cantidad, otro tamaño es otra línea y no muta', () => {
  const uno = c.agregar([], { name: 'Neem', sc: 'Azadirachta indica', sz: '1 m', qty: 2 });
  const dos = c.agregar(uno, { name: 'Neem', sc: 'Azadirachta indica', sz: '1 m', qty: 5 });
  const tres = c.agregar(dos, { name: 'Neem', sc: 'Azadirachta indica', sz: '2-3 m', qty: 1 });
  assert.deepEqual(uno.map((i) => i.qty), [2]);
  assert.deepEqual(dos.map((i) => i.qty), [5]);
  assert.deepEqual(tres.map((i) => [i.sz, i.qty]), [['1 m', 5], ['2-3 m', 1]]);
  assert.deepEqual(c.cambiar(tres, 1, -1).map((i) => i.qty), [5, 1]);
  assert.deepEqual(c.quitar(tres, 0).map((i) => i.sz), ['2-3 m']);
  assert.equal(c.resumen(tres), '2 variedades · 6 piezas');
});

test('cantidad entre 1 y 9999', () => {
  assert.equal(c.cantidad('0'), 1);
  assert.equal(c.cantidad('abc'), 1);
  assert.equal(c.cantidad('12'), 12);
  assert.equal(c.cantidad(100000), 9999);
});

test('filtros en la URL: ida y vuelta, mismo formato que catalogo_datos.url_catalogo', () => {
  const f = c.leerFiltros('?q=palma%20real&luz=media,sombra&uso=salitre');
  assert.deepEqual(f, { q: 'palma real', cat: [], luz: ['media', 'sombra'], tam: [], riego: [], uso: ['salitre'] });
  assert.equal(c.escribirFiltros(f), '?q=palma%20real&luz=media,sombra&uso=salitre');
  assert.equal(c.escribirFiltros(c.leerFiltros('')), '');
  assert.equal(c.hayFiltros(c.leerFiltros('')), false);
});

test('coincide: O dentro de un grupo, Y entre grupos y búsqueda sin acentos', () => {
  const d = { cat: 'palmas', luz: 'media', tam: 'grande', riego: 'moderado', uso: 'interior salitre', buscar: 'palma areca dypsis lutescens' };
  assert.equal(c.coincide(d, c.leerFiltros('?luz=sol,media')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?luz=sol')), false);
  assert.equal(c.coincide(d, c.leerFiltros('?cat=palmas&uso=banqueta')), false);
  assert.equal(c.coincide(d, c.leerFiltros('?q=Árec')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?q=palma%20lutescens')), true);
  assert.equal(c.coincide(d, c.leerFiltros('?q=olivo')), false);
});

test('mensaje de una especie que no está en el catálogo', () => {
  assert.equal(c.mensajeEspecial('  Palma phoenix 4 m '), 'Hola Viveros Terra\n\nBusco: *Palma phoenix 4 m*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?');
  assert.ok(c.mensajeEspecial('').includes('*___*'));
});

const ESPECIES = {
  neem: { name: 'Neem', sc: 'Azadirachta indica', sz: ['1 m', '2-3 m'] },
  'palma-real': { name: 'Palma Real', sc: 'Roystonea regia', sz: ['1 m'] },
};

function memoria(inicial) {
  const datos = new Map(inicial ? [[c.CLAVE, inicial]] : []);
  return { getItem: (k) => (datos.has(k) ? datos.get(k) : null), setItem: (k, v) => datos.set(k, String(v)), datos };
}

test('validarLista: solo especies del catálogo con tamaño y cantidad válidos; junta repetidos', () => {
  const buena = { name: 'Neem', sc: 'Azadirachta indica', sz: '1 m', qty: 2 };
  assert.deepEqual(c.validarLista([buena], ESPECIES), [buena]);
  assert.deepEqual(c.validarLista({ name: 'Neem' }, ESPECIES), []);
  assert.deepEqual(c.validarLista(null, ESPECIES), []);
  assert.deepEqual(c.validarLista([buena], null), []);
  const malas = [
    null, 'Neem', { ...buena, name: 'Inventada' }, { ...buena, sc: 'Otra cosa' }, { ...buena, sz: '' },
    { ...buena, sz: 'x'.repeat(61) }, { ...buena, sz: 3 }, { ...buena, qty: 0 }, { ...buena, qty: 10000 },
    { ...buena, qty: 1.5 }, { ...buena, qty: '2' }, { ...buena, name: '__proto__' },
  ];
  assert.deepEqual(c.validarLista(malas, ESPECIES), []);
  const juntas = c.validarLista([buena, { ...buena, qty: 7, extra: '<b>' }, { ...buena, sz: ' Medida especial ' }], ESPECIES);
  assert.deepEqual(juntas, [{ ...buena, qty: 7 }, { ...buena, sz: 'Medida especial' }]);
});

test('guardarLista y leerLista: ida y vuelta, y sin romper si el almacenamiento falla o trae basura', () => {
  const m = memoria();
  const lista = [{ name: 'Palma Real', sc: 'Roystonea regia', sz: '1 m', qty: 3 }];
  assert.equal(c.guardarLista(m, lista), true);
  assert.deepEqual(c.leerLista(m, ESPECIES), lista);
  assert.deepEqual(c.leerLista(memoria('{no es json'), ESPECIES), []);
  assert.deepEqual(c.leerLista(memoria('{"name":"Neem"}'), ESPECIES), []);
  assert.deepEqual(c.leerLista(memoria(), ESPECIES), []);
  const roto = { getItem() { throw new Error('SecurityError'); }, setItem() { throw new Error('QuotaExceededError'); } };
  assert.equal(c.guardarLista(roto, lista), false);
  assert.deepEqual(c.leerLista(roto, ESPECIES), []);
  assert.equal(c.guardarLista(null, lista), false);
  assert.deepEqual(c.leerLista(null, ESPECIES), []);
});

test('contarFiltros cuenta las opciones activas (sin la búsqueda) y enLista busca por nombre', () => {
  assert.equal(c.contarFiltros(c.leerFiltros('?q=palma&luz=media,sombra&uso=salitre')), 3);
  assert.equal(c.contarFiltros(c.leerFiltros('?q=palma')), 0);
  assert.equal(c.enLista([{ name: 'Neem' }], 'Neem'), true);
  assert.equal(c.enLista([], 'Neem'), false);
});

test('el código no usa innerHTML, window.open ni console', () => {
  const fuente = require('node:fs').readFileSync(require('node:path').join(__dirname, '..', 'vt-catalogo.js'), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  assert.doesNotMatch(fuente, /innerHTML|outerHTML|insertAdjacentHTML|document\.write/);
  assert.doesNotMatch(fuente, /window\.open|\bconsole\./);
});
