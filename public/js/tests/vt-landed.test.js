const test = require('node:test');
const assert = require('node:assert');
const { landedM2, slugEstado, estadoDesdeSlug } = require('../vt-landed.js');

const ZONAS = { A: 900, B: 1150, C: 1400 };
const ESTADO_ZONA = { 'Nuevo León': 'B', CDMX: 'A', 'Yucatán': 'C' };

test('precio puesto por zona', () => {
  assert.strictEqual(landedM2(139, 'Nuevo León', ESTADO_ZONA, ZONAS), 162);
  assert.strictEqual(landedM2(139, 'CDMX', ESTADO_ZONA, ZONAS), 157);
  assert.strictEqual(landedM2(139, 'Yucatán', ESTADO_ZONA, ZONAS), 167);
});

test('estado desconocido devuelve null', () => {
  assert.strictEqual(landedM2(139, 'Narnia', ESTADO_ZONA, ZONAS), null);
});

test('slug ida y vuelta', () => {
  assert.strictEqual(slugEstado('Nuevo León'), 'nuevo-leon');
  assert.strictEqual(estadoDesdeSlug('nuevo-leon', Object.keys(ESTADO_ZONA)), 'Nuevo León');
  assert.strictEqual(estadoDesdeSlug('no-existe', Object.keys(ESTADO_ZONA)), null);
});
