const test = require('node:test');
const assert = require('node:assert');
const casos = require('./casos-preguntas.json');
const P = require('../vt-preguntas.js');
const { folio } = require('../vt-folio.js');

const conjunto = { id: 'sintetico', preguntas: [{ clave: 'modelo' }, { clave: 'm2' }, { clave: 'destino' }] };
const modelos = { 'toscana-28': 'Toscana 28', 'irlanda-25': 'Irlanda 25' };

test('armarMensaje: casos compartidos', () => {
  for (const c of casos) {
    const ctx = { fijo: c.fijo, recordado: c.rec, modelos, folio };
    assert.strictEqual(P.armarMensaje(conjunto, c.r, ctx), c.esperado);
  }
});

test('sin rayas ni puntuación rota en ninguna combinación', () => {
  for (const modelo of ['', 'toscana-28', 'no-se']) {
    for (const m2 of ['', '<25', 'exacto']) {
      for (const destino of ['', 'recoger', 'local', 'envio']) {
        const t = P.armarMensaje(conjunto, { modelo, m2, destino, estado: destino === 'envio' ? 'Jalisco' : '' },
          { fijo: {}, recordado: { m2: 40 }, modelos, folio });
        assert.ok(!/___|,,|, \.|\s\./.test(t), t);
      }
    }
  }
});

test('preguntas visibles e iniciales', () => {
  const ctx = { fijo: { modelo: 'toscana-28' }, recordado: { estado: 'Jalisco', m2: 30, modelo: 'irlanda-25' }, modelos };
  assert.deepStrictEqual(P.preguntasVisibles(conjunto, ctx).map((q) => q.clave), ['m2', 'destino']);
  assert.deepStrictEqual(P.respuestasIniciales(conjunto, ctx), { m2: 'exacto', destino: 'envio', estado: 'Jalisco' });
  const ciudad = { fijo: { estado: 'Nuevo León', ciudad: 'Monterrey' }, recordado: { modelo: 'irlanda-25' }, modelos };
  assert.deepStrictEqual(P.preguntasVisibles(conjunto, ciudad).map((q) => q.clave), ['modelo', 'm2']);
  assert.deepStrictEqual(P.respuestasIniciales(conjunto, ciudad), { modelo: 'irlanda-25' });
});

test('memoria de la visita: valida y tolera errores', () => {
  const mem = new Map();
  const storage = { getItem: (k) => mem.get(k) || null, setItem: (k, v) => mem.set(k, v) };
  P.recordar(storage, { modelo: 'toscana-28', m2: 40 });
  P.recordar(storage, { m2: -3, modelo: '<script>' });
  assert.deepStrictEqual(P.leerVisita(storage), { modelo: 'toscana-28', m2: 40 });
  const roto = { getItem() { throw new Error('bloqueado'); }, setItem() { throw new Error('bloqueado'); } };
  assert.deepStrictEqual(P.leerVisita(roto), {});
  assert.doesNotThrow(() => P.recordar(roto, { m2: 10 }));
});
