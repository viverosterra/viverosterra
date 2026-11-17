const test = require('node:test');
const assert = require('node:assert');
const casos = require('./casos-rollos.json');
const { corte, ROLLO_LARGO_M } = require('../vt-rollos.js');

test('mismos casos que tools/pasto/rollos.py', () => {
  for (const [largo, ancho, tiras, largoTira, m2Tiras, m2, rollos, m2Sin, rollosSin] of casos.casos) {
    const r = corte(largo, ancho);
    assert.deepStrictEqual(
      [r.tiras, r.largoTira, r.m2Tiras, r.m2, r.rollos, r.m2SinMargen, r.rollosSinMargen],
      [tiras, largoTira, m2Tiras, m2, rollos, m2Sin, rollosSin], `${largo} × ${ancho}`);
  }
});

test('medidas inválidas devuelven null', () => {
  for (const [largo, ancho] of casos.invalidos) assert.strictEqual(corte(largo, ancho), null, `${largo} × ${ancho}`);
});

test('acepta texto con coma decimal de los campos', () => {
  assert.strictEqual(corte('4,2', '7.1').m2, 34);
  assert.strictEqual(corte('', '3'), null);
});

test('sobrante, uniones y tira con unión', () => {
  const r = corte(7, 5);
  assert.deepStrictEqual([r.area, r.sobrante, r.uniones, r.tiraConUnion], [35, 5, 3, false]);
  assert.strictEqual(corte(30, 2).tiraConUnion, true);
  assert.strictEqual(ROLLO_LARGO_M, 25);
});
