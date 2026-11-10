// public/js/tests/vt-simulador.test.js
const test = require('node:test');
const assert = require('node:assert');
const { mensaje, BARRA } = require('../vt-simulador.js');

test('sin monto escrito por el cliente el mensaje no lleva ninguna cifra y pide colonia y metros (reescritura 3)', () => {
  assert.strictEqual(mensaje('pasto en rollo instalado', 0, 0, 0),
    'Hola, quiero cotizar pasto en rollo instalado y me interesa pagar con tarjeta en mensualidades.\nColonia: ___\nMetros aprox.: ___');
  const conPlazo = mensaje('pasto en rollo instalado', 0, 6, 13000);
  assert.match(conPlazo, /Me interesa: 6 mensualidades con tarjeta de crédito\./);
  assert.doesNotMatch(conPlazo, /\$/);
});

test('con monto escrito conserva el monto y la forma de pago y añade la colonia', () => {
  assert.strictEqual(mensaje('un sistema de riego', 18000, 0, 0),
    'Hola, quiero cotizar un sistema de riego.\nMi cotización es de $18,000.\nPagaría de contado.\nColonia: ___');
  assert.match(mensaje('mi jardín', 20000, 12, 22220), /Me interesa pagar en 12 mensualidades con tarjeta de crédito \(total \$22,220\)\./);
  assert.strictEqual(BARRA, 'Enviar mi plan de pago');
});
