// public/js/tests/vt-b2b.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const { calcular } = require('../vt-medidor.js');
const B = require('../vt-b2b.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-b2b.json'), 'utf8'));

test('cotizador por volumen: mismos resultados que tools/site/componentes.py en casos-b2b.json', () => {
  for (const { entrada, esperado } of CASOS.volumen) {
    const r = calcular(B.leerM2(entrada.texto), 1, 'mayoreo', CASOS.modos);
    const t = B.textosVolumen(r, entrada);
    const obtenido = { m2: r.m2, precio: r.precio, desde: r.desde, total: r.total, rotulo: r.rotulo, aviso: r.aviso, ...t };
    assert.deepStrictEqual(obtenido, esperado, JSON.stringify(entrada));
  }
});

test('lectura de m²: miles con coma, coma decimal y valores inválidos', () => {
  for (const [texto, esperado] of CASOS.lecturas) assert.strictEqual(B.leerM2(texto), esperado, texto);
});

test('con menos de 500 m² nunca sale a precio de mayoreo', () => {
  for (const m2 of [1, 120, 499, 499.9]) {
    const r = calcular(m2, 1, 'mayoreo', CASOS.modos);
    assert.strictEqual(r.precio, CASOS.modos.solo.precio);
    assert.match(B.textosVolumen(r, {}).mensaje, /solo el pasto San Agustín/);
  }
  assert.strictEqual(calcular(500, 1, 'mayoreo', CASOS.modos).precio, CASOS.modos.mayoreo.precio);
});

test('armador de palmas: mismo mensaje y resumen que componentes.py', () => {
  for (const { entrada, esperado } of CASOS.palmas) {
    assert.strictEqual(B.mensajePalmas(entrada.filas, entrada), esperado.mensaje, JSON.stringify(entrada));
    assert.strictEqual(B.resumenPalmas(entrada.filas), esperado.resumen, JSON.stringify(entrada));
  }
});

test('el mensaje de palmas es texto plano: un renglón por especie y los huecos de compras al final', () => {
  const m = B.mensajePalmas([['Palma real', '3', '40'], ['Coco plumoso', '', '']], {});
  const renglones = m.split('\n');
  assert.strictEqual(renglones.length, 6);
  assert.deepStrictEqual(renglones.slice(-3), ['Empresa: ___', 'Obra y ubicación: ___', 'Fecha de entrega: ___']);
  assert.doesNotMatch(m, /</);
});

test('formulario por correo: obligatorios vacíos y correo inválido', () => {
  const requeridos = ['empresa', 'nombre', 'correo', 'proyecto', 'cantidad'];
  const vacio = B.erroresCorreo({}, requeridos);
  assert.deepStrictEqual(Object.keys(vacio), requeridos);
  const malo = B.erroresCorreo({ empresa: 'A', nombre: 'B', correo: 'compras@', proyecto: 'C', cantidad: '1,200 m²' }, requeridos);
  assert.deepStrictEqual(Object.keys(malo), ['correo']);
  assert.match(malo.correo, /correo/);
  const bien = B.erroresCorreo({ empresa: 'A', nombre: 'B', correo: 'compras@empresa.com.mx', proyecto: 'C', cantidad: '3' }, requeridos);
  assert.deepStrictEqual(bien, {});
  assert.deepStrictEqual(B.erroresCorreo({ correo: '  ' }, ['correo']), { correo: B.MENSAJE_REQUERIDO });
});

test('formulario por correo: generate_lead con method formulario', () => {
  assert.deepStrictEqual(B.eventoFormulario('palmas:formulario', 'empresas'),
    { nombre: 'generate_lead', params: { method: 'formulario', cta_id: 'palmas:formulario', service: 'empresas' } });
});

test('prellenado del formulario: m² del cotizador y lista del armador', () => {
  assert.strictEqual(B.prellenadoVolumen(1200), '1,200 m²');
  assert.strictEqual(B.prellenadoVolumen(0), '');
  assert.strictEqual(B.prellenadoPalmas([['Palma real', '3', '40'], ['', '', '']]), '- 40 × Palma real, altura aprox.: 3 m');
  assert.deepStrictEqual(B.prellenadoObra({ empresa: ' Constructora Norte ', obra: 'Fracc. en Altamira', fecha: 'marzo' }),
    { empresa: 'Constructora Norte', proyecto: 'Fracc. en Altamira', fecha: 'marzo' });
  assert.deepStrictEqual(B.prellenadoObra({ empresa: '', obra: '', fecha: '' }), { empresa: '', proyecto: '', fecha: '' });
});
test('pedido de materiales (2f): el campo email se valida con el ejemplo de su placeholder', () => {
  const e = B.erroresCorreo({ nombre: 'Ana', email: 'ana@' }, ['nombre', 'email'], { email: 'tu@correo.com' });
  assert.deepStrictEqual(e, { email: 'Revisa el correo: debe verse como tu@correo.com.' });
  assert.strictEqual(B.erroresCorreo({ correo: 'a@' }, []).correo, 'Revisa el correo: debe verse como compras@tuempresa.com.');
});
