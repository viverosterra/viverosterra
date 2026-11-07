// public/js/tests/terra.test.js
const test = require('node:test');
const assert = require('node:assert');
const { FIRMA, tipoEnlace, conFirma, evento } = require('../terra.js');

function enlace(atributos) {
  return { getAttribute: (nombre) => (nombre in atributos ? atributos[nombre] : null) };
}

test('reconoce WhatsApp y teléfono', () => {
  assert.strictEqual(tipoEnlace('https://wa.me/528333268008?text=Hola'), 'wa');
  assert.strictEqual(tipoEnlace('https://api.whatsapp.com/send?phone=528333268008'), 'wa');
  assert.strictEqual(tipoEnlace('tel:+528333268008'), 'tel');
  assert.strictEqual(tipoEnlace('/precios'), null);
  assert.strictEqual(tipoEnlace(null), null);
});

test('agrega la firma una sola vez, con %20 y sin +', () => {
  const firmado = conFirma('https://wa.me/528333268008?text=Hola%2C%20quiero%20pasto');
  assert.strictEqual(firmado, 'https://wa.me/528333268008?text=' + encodeURIComponent('Hola, quiero pasto\n\n' + FIRMA));
  assert.strictEqual(conFirma(firmado), firmado);
  assert.ok(!firmado.includes('+'));
});

test('sin texto previo deja solo la firma', () => {
  assert.strictEqual(conFirma('https://wa.me/528333268008'), 'https://wa.me/528333268008?text=' + encodeURIComponent(FIRMA));
});

test('un texto mal codificado se deja igual', () => {
  assert.strictEqual(conFirma('https://wa.me/528333268008?text=%E0%A4%A'), 'https://wa.me/528333268008?text=%E0%A4%A');
});

test('generate_lead lleva cta y servicio; click_to_call lleva cta', () => {
  const ctx = { tipo: 'blog', servicio: 'general' };
  assert.deepStrictEqual(evento(enlace({ href: 'https://wa.me/528333268008?text=a', 'data-cta': 'blog:header' }), ctx), {
    nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: 'blog:header', service: 'general' },
  });
  assert.deepStrictEqual(evento(enlace({ href: 'tel:+528333268008' }), ctx), {
    nombre: 'click_to_call', params: { cta_id: 'blog:sin-etiqueta' },
  });
  assert.strictEqual(evento(enlace({ href: '/precios' }), ctx), null);
});
