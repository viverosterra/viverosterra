// public/js/tests/vt-cuestionario.test.js
const test = require('node:test');
const assert = require('node:assert');
const b = require('../vt-cuestionario.js');

const campo = (name, type, value, checked) => ({ name, type, value, checked: Boolean(checked) });

test('el borrador guarda lo que escribió el cliente y nunca los campos ocultos ni la trampa _honey', () => {
  const campos = [campo('nombre', 'text', 'María'), campo('_subject', 'hidden', 'x'), campo('_honey', 'text', 'bot'),
    campo('uso', 'checkbox', 'Niños', true), campo('uso', 'checkbox', 'Asados', false), campo('uso', 'checkbox', 'Mascotas', true),
    campo('prioridad', 'radio', 'Fácil', false), campo('prioridad', 'radio', 'Valor', true), campo('email', 'email', '')];
  assert.deepStrictEqual(b.capturar(campos), { nombre: 'María', uso: ['Niños', 'Mascotas'], prioridad: 'Valor' });
});

test('al recargar se recuperan texto, casillas y opciones; lo que no es de fiar se ignora', () => {
  const campos = [campo('nombre', 'text', ''), campo('uso', 'checkbox', 'Niños'), campo('uso', 'checkbox', 'Asados'),
    campo('prioridad', 'radio', 'Fácil'), campo('prioridad', 'radio', 'Valor'), campo('_next', 'hidden', '/gracias')];
  const puestos = b.aplicar(campos, { nombre: 'Ana', uso: ['Asados'], prioridad: 'Valor', _next: 'https://otro', extra: 'x' });
  assert.strictEqual(puestos, 3);
  assert.deepStrictEqual(campos.map((c) => (c.type === 'text' || c.type === 'hidden' ? c.value : c.checked)),
    ['Ana', false, true, false, true, '/gracias']);
  assert.strictEqual(b.aplicar(campos, null), 0);
  assert.strictEqual(b.aplicar([campo('nombre', 'text', '')], { nombre: { malo: 1 } }), 0);
});

test('leer, guardar y borrar no fallan sin almacenamiento o con uno que lanza', () => {
  const memoria = new Map();
  const storage = { getItem: (k) => memoria.get(k) || null, setItem: (k, v) => memoria.set(k, v), removeItem: (k) => memoria.delete(k) };
  assert.strictEqual(b.guardar(storage, { nombre: 'Ana' }), true);
  assert.deepStrictEqual(b.leer(storage), { nombre: 'Ana' });
  b.borrar(storage);
  assert.strictEqual(b.leer(storage), null);
  const roto = { getItem() { throw new Error('x'); }, setItem() { throw new Error('x'); }, removeItem() { throw new Error('x'); } };
  assert.strictEqual(b.leer(roto), null);
  assert.strictEqual(b.guardar(roto, {}), false);
  b.borrar(roto);
  storage.setItem(b.CLAVE, '{roto');
  assert.strictEqual(b.leer(storage), null);
});
