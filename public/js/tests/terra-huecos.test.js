const test = require('node:test');
const assert = require('node:assert');
const casos = require('./casos-huecos.json');
const { sinHuecos, conFirma } = require('../terra.js');

test('casos compartidos de huecos', () => {
  for (const [entrada, esperado] of casos) assert.strictEqual(sinHuecos(entrada), esperado);
});

test('conFirma limpia aunque el texto ya venga firmado', () => {
  const href = 'https://wa.me/528333268008?text=' + encodeURIComponent('Hola.\nColonia: ___\n\nVengo de viverosterra.com');
  const texto = decodeURIComponent(conFirma(href).split('text=')[1]);
  assert.strictEqual(texto, 'Hola.\n\nVengo de viverosterra.com');
});

test('conFirma firma y limpia un texto sin firma', () => {
  const href = 'https://wa.me/528333268008?text=' + encodeURIComponent('Hola, quiero cotizar: ___');
  assert.strictEqual(decodeURIComponent(conFirma(href).split('text=')[1]), 'Hola, quiero cotizar.\n\nVengo de viverosterra.com');
});
