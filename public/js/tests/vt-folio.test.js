const test = require('node:test');
const assert = require('node:assert');
const { folio, leerFolio, codigoModelo, completarModelos, ESTADOS } = require('../vt-folio.js');

const SLUGS = ['aruba-10', 'toscana-18', 'capri-20', 'irlanda-25', 'toscana-28', 'viena-30', 'japones-35',
  'monaco-35', 'bali-35'];

// Claves y precio de rollo como en el cotizador de Netlify (MODELOS[].k y precio[2]).
const COTIZADOR = [
  { k: 'aruba10', rollo: 139 }, { k: 'toscana18', rollo: 149 }, { k: 'capri20', rollo: 209 },
  { k: 'irlanda25', rollo: 209 }, { k: 'toscana28', rollo: 199 }, { k: 'viena30', rollo: 249 },
  { k: 'japones35', rollo: 269 }, { k: 'monaco35', rollo: 299 }, { k: 'bali35', rollo: 299 },
];

test('código de modelo: inicial y altura, igual desde el slug o la clave del cotizador', () => {
  assert.deepStrictEqual(SLUGS.map(codigoModelo), ['A10', 'T18', 'C20', 'I25', 'T28', 'V30', 'J35', 'M35', 'B35']);
  assert.deepStrictEqual(COTIZADOR.map((m) => codigoModelo(m.k)), SLUGS.map(codigoModelo));
  assert.strictEqual(new Set(SLUGS.map(codigoModelo)).size, SLUGS.length);
});

test('folio de un modelo con estado, showroom, local y sin entrega', () => {
  assert.strictEqual(folio([{ slug: 'toscana-28', m2: 40 }], 'Nuevo León'), 'T28-40-NL');
  assert.strictEqual(folio([{ slug: 'toscana-18', m2: 12 }], 'showroom'), 'T18-12-REC');
  assert.strictEqual(folio([{ slug: 'irlanda-25', m2: 30 }], 'local'), 'I25-30-LOC');
  assert.strictEqual(folio([{ slug: 'bali-35', m2: 60 }], ''), 'B35-60');
});

test('folio de una lista une los modelos con +', () => {
  assert.strictEqual(folio([{ slug: 'toscana-28', m2: 40 }, { slug: 'irlanda-25', m2: 30 }], 'Jalisco'),
    'T28-40+I25-30-JAL');
});

test('sin modelos válidos no hay folio', () => {
  assert.strictEqual(folio([], 'Jalisco'), '');
  assert.strictEqual(folio([{ slug: 'toscana-28', m2: NaN }], 'Jalisco'), '');
  assert.strictEqual(folio([{ slug: 'toscana-28', m2: 0 }], 'Jalisco'), '');
});

test('los 32 estados tienen abreviatura única y van y vuelven', () => {
  const nombres = Object.keys(ESTADOS);
  assert.strictEqual(nombres.length, 32);
  assert.strictEqual(new Set(Object.values(ESTADOS)).size, 32);
  nombres.forEach((e) => {
    const f = folio([{ slug: 'viena-30', m2: 50 }], e);
    assert.deepStrictEqual(leerFolio(`Hola\nFolio web: ${f}`), { items: [{ codigo: 'V30', m2: 50 }], entrega: e });
  });
});

test('leer folio dentro de un mensaje de WhatsApp pegado', () => {
  const msg = 'Hola, quiero cotizar el pasto sintético Toscana 28.\nNecesito 40 m².\n¿Me confirman el precio final?\n'
    + 'Folio web: T28-40+I25-30-REC';
  assert.deepStrictEqual(leerFolio(msg), {
    items: [{ codigo: 'T28', m2: 40 }, { codigo: 'I25', m2: 30 }], entrega: 'showroom',
  });
  assert.deepStrictEqual(leerFolio('folio web: i25-30-loc'), { items: [{ codigo: 'I25', m2: 30 }], entrega: 'local' });
  assert.deepStrictEqual(leerFolio('Folio web: B35-60'), { items: [{ codigo: 'B35', m2: 60 }], entrega: '' });
});

test('folio ausente o ilegible da null', () => {
  assert.strictEqual(leerFolio('Hola, quiero pasto'), null);
  assert.strictEqual(leerFolio('Folio web: XYZ'), null);
  assert.strictEqual(leerFolio('Folio web: T28-40-ZZ'), null);
  assert.strictEqual(leerFolio('Folio web: T28-0-NL'), null);
  assert.strictEqual(leerFolio(''), null);
  assert.strictEqual(leerFolio(null), null);
});

test('un modelo se completa con sus vecinos de precio', () => {
  // Orden por rollo: aruba10 139, toscana18 149, toscana28 199, capri20 209, irlanda25 209, viena30 249, ...
  assert.deepStrictEqual(completarModelos(['T28'], COTIZADOR), ['toscana18', 'toscana28', 'capri20']);
  assert.deepStrictEqual(completarModelos(['A10'], COTIZADOR), ['aruba10', 'toscana18', 'toscana28']);
  assert.deepStrictEqual(completarModelos(['B35'], COTIZADOR), ['japones35', 'monaco35', 'bali35']);
});

test('una lista usa sus modelos; con dos se agrega el vecino más cercano; más de tres se recorta', () => {
  assert.deepStrictEqual(completarModelos(['T28', 'I25', 'J35'], COTIZADOR), ['toscana28', 'irlanda25', 'japones35']);
  assert.deepStrictEqual(completarModelos(['T28', 'J35'], COTIZADOR), ['toscana28', 'japones35', 'capri20']);
  assert.deepStrictEqual(completarModelos(['T28', 'I25', 'J35', 'B35'], COTIZADOR), ['toscana28', 'irlanda25', 'japones35']);
  assert.deepStrictEqual(completarModelos(['T28', 'T28'], COTIZADOR), ['toscana18', 'toscana28', 'capri20']);
});

test('códigos desconocidos se ignoran', () => {
  assert.deepStrictEqual(completarModelos(['Z99'], COTIZADOR), []);
  assert.deepStrictEqual(completarModelos(['Z99', 'A10'], COTIZADOR), ['aruba10', 'toscana18', 'toscana28']);
});
