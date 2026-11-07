// public/js/tests/vt-medidor.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const M = require('../vt-mensualidades.js');
const { numero, calcular, textos, plano, enlace } = require('../vt-medidor.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-medidor.json'), 'utf8'));

test('mismos resultados que tools/site/componentes.py en cada caso de casos-medidor.json', () => {
  for (const { entrada, esperado } of CASOS.casos) {
    const r = calcular(entrada.largo, entrada.ancho, entrada.modo, CASOS.modos);
    const t = textos(entrada.largo, entrada.ancho, r, entrada.colonia, M);
    const obtenido = { m2: r.m2, precio: r.precio, desde: r.desde, total: r.total, rotulo: r.rotulo, aviso: r.aviso, ...t };
    assert.deepStrictEqual(obtenido, esperado, JSON.stringify(entrada));
  }
});

test('mayoreo con menos de 500 m² calcula a precio de solo pasto y lo avisa', () => {
  const r = calcular(10, 10, 'mayoreo', CASOS.modos);
  assert.strictEqual(r.precio, CASOS.modos.solo.precio);
  assert.strictEqual(r.desde, false);
  assert.match(r.aviso, /Te faltan 400 m²/);
});

test('numero acepta coma decimal y rechaza vacíos, negativos y medidas absurdas', () => {
  assert.strictEqual(numero('8,5'), 8.5);
  assert.strictEqual(numero(''), 0);
  assert.strictEqual(numero('-3'), 0);
  assert.strictEqual(numero('1200'), 0);
});

test('el plano conserva la proporción y nunca dibuja menos de 24 unidades', () => {
  const g = plano(8, 6);
  assert.ok(Math.abs(g.w / g.h - 8 / 6) < 1e-9);
  const angosto = plano(100, 1);
  assert.strictEqual(angosto.h, 24);
});

test('el mensaje es texto plano de cinco renglones y termina pidiendo la foto', () => {
  const r = calcular(8, 6, 'instalado', CASOS.modos);
  const renglones = textos(8, 6, r, '', M).mensaje.split('\n');
  assert.strictEqual(renglones.length, 5);
  assert.strictEqual(renglones[4], 'Te mando foto del área.');
});

test('enlace arma wa.me con el número que le da la página y codifica todo el texto', () => {
  assert.strictEqual(enlace('528333268008', 'Hola, ñ\nColonia: ___'),
    'https://wa.me/528333268008?text=Hola%2C%20%C3%B1%0AColonia%3A%20___');
});

test('sin número fijo en el archivo: el número llega de data-wa', () => {
  const fuente = fs.readFileSync(path.join(__dirname, '..', 'vt-medidor.js'), 'utf8');
  assert.doesNotMatch(fuente, /\d{10,}/);
  assert.match(fuente, /dataset\.wa/);
  assert.match(fuente, /dataset\.mensaje/);
});

test('hay casos de paridad en la frontera de .5 de la mensualidad (Math.round frente a round de Python)', () => {
  const frontera = CASOS.casos.filter(({ entrada }) => {
    const r = calcular(entrada.largo, entrada.ancho, entrada.modo, CASOS.modos);
    const d = M.plazosDisponibles(r.total);
    if (!d.length) return false;
    const u = d[d.length - 1];
    return (M.totalAPlazos(r.total, u) / u) % 1 === 0.5;
  });
  assert.ok(frontera.length >= 2);
});
