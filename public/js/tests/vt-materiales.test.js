// public/js/tests/vt-materiales.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const M = require('../vt-materiales.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-materiales.json'), 'utf8'));
// Lo que escribe componentes_materiales.datos_js(clave) en data-material (test_componentes_materiales lo compara).
const CFG = {
  'tierra-negra': { clave: 'tierra-negra', costal_m3: 0.035, precio_costal: 90, precio_m3: 1500, texto: 'tierra negra vegetal' },
  tezontle: { clave: 'tezontle', costal_m3: 0.027, camion_m3: 14, texto: 'tezontle rojo' },
  marmol: { clave: 'marmol', kg_saco: 20, texto: 'mármol blanco decorativo' },
  'piedra-bola': { clave: 'piedra-bola', kg_m2: [120, 150], medida: 'mediana (capa de 8 a 10 cm)', texto: 'piedra bola de río' },
};
const CAMION_MAIN = 'Camión volteo 8m³+ (~desde $5,000)';
const CAMION = 'Camión volteo de 8 m³ o más (según cotización)';

// Igual que esperado_de_main de tests/test_materiales_paridad.py.
function esperadoDeMain(clave, { visibles: v, mensaje: m }) {
  if (clave === 'tierra-negra') {
    return { cantidad: v['res-m3'], presentacion: v['res-formato'].replace(CAMION_MAIN, CAMION), equivalente: v['res-costales'], mensaje: m };
  }
  if (clave === 'tezontle') {
    return { cantidad: v['tez-res-m3'], presentacion: v['tez-res-formato'], equivalente: v['tez-res-costales'], mensaje: m };
  }
  const lineas = m.split('\n').filter((x) => !x.startsWith('Precio estimado: '));
  lineas[lineas.length - 1] = M.CIERRE;
  return { cantidad: `${v['res-sacos']} sacos`, peso: v['res-peso'],
    nota: v['res-nota'].replace(' sacos cubre ', ' sacos cubren ').replace(' A $250 c/u.', ''), mensaje: lineas.join('\n') };
}

test('mismos resultados que main en cada caso de casos-materiales.json', () => {
  for (const [clave, calc] of Object.entries(CASOS.calculadoras)) {
    const usos = Object.fromEntries(calc.capas.map((o) => [o.value, o.text]));
    for (const caso of calc.casos) {
      const capa = Number(caso.entrada.capa);
      const r = M.calcular(CFG[clave], caso.entrada.area, capa);
      assert.deepStrictEqual(M.textos(CFG[clave], caso.entrada.area, capa, r, usos[caso.entrada.capa]),
        esperadoDeMain(clave, caso), `${clave} ${JSON.stringify(caso.entrada)}`);
    }
  }
});

test('piedra bola: 10 m² son 1,200 a 1,500 kg, como decía su pregunta frecuente', () => {
  const cfg = CFG['piedra-bola'];
  assert.strictEqual(M.textos(cfg, 10, 0, M.calcular(cfg, 10, 0)).cantidad, '1,200 a 1,500 kg');
});

test('leerArea acepta miles y coma decimal y rechaza vacíos, negativos y áreas absurdas', () => {
  assert.deepStrictEqual(['1,200', '12,5', '80 m²', '', '-3', '200000'].map(M.leerArea), [1200, 12.5, 80, 0, 0, 0]);
});

test('el mensaje es texto plano y termina con la misma pregunta en las cuatro calculadoras', () => {
  for (const cfg of Object.values(CFG)) {
    const t = M.textos(cfg, 20, cfg.clave === 'marmol' ? 4 : 0.08, M.calcular(cfg, 20, cfg.clave === 'marmol' ? 4 : 0.08), 'x');
    assert.ok(t.mensaje.endsWith(M.CIERRE));
    assert.doesNotMatch(t.mensaje, /<|\$250|disponibilidad/);
  }
});
