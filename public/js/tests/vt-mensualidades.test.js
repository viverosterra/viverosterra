// public/js/tests/vt-mensualidades.test.js
const test = require('node:test');
const assert = require('node:assert');
const { planes, plazosDisponibles, totalAPlazos } = require('../vt-mensualidades.js');

test('totales iguales a la calculadora del procesador', () => {
  assert.deepStrictEqual([3, 6, 9, 12].map((p) => totalAPlazos(11100, p)), [12263, 12753, 13377, 13702]);
});

test('umbrales', () => {
  assert.deepStrictEqual(plazosDisponibles(1999), []);
  assert.deepStrictEqual(plazosDisponibles(2000), [3]);
  assert.deepStrictEqual(plazosDisponibles(5000), [3, 6]);
  assert.deepStrictEqual(plazosDisponibles(15000), [3, 6, 9, 12]);
});

test('planes con mensualidad y diferencia', () => {
  const p12 = planes(11100).find((x) => x.plazo === 12);
  assert.strictEqual(p12.mensualidad, 1142);
  assert.strictEqual(p12.diferencia, 2602);
  assert.strictEqual(p12.disponible, false);
});

test('paridad con Python en los casos compartidos (incluye .5 exacto)', () => {
  const { casos } = JSON.parse(require('node:fs').readFileSync(require('node:path').join(__dirname, 'casos-mensualidades.json'), 'utf8'));
  for (const [contado, plazo, total, mensualidad] of casos) {
    const p = planes(contado).find((x) => x.plazo === plazo);
    assert.deepStrictEqual([p.total, p.mensualidad], [total, mensualidad], `${contado} a ${plazo}`);
  }
});
