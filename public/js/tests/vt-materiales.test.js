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

// Igual que agrupar, mensaje_de_main y esperado_de_main de tests/test_materiales_paridad.py.
const agrupar = (t) => t.replace(/(?<![\d.,])\d{4,}/g, (n) => Number(n).toLocaleString('en-US'));
function mensajeDeMain(clave, m, capa) {
  const lineas = m.split('\n').filter((x) => !x.startsWith('Precio estimado: ')).map(agrupar);
  lineas[lineas.length - 1] = M.CIERRE;
  lineas.splice(lineas.length - 2, 0, M.COLONIA);
  if (clave === 'tierra-negra') {
    lineas.splice(lineas.findIndex((x) => x.startsWith('Área: ')) + 1, 0, `Capa: ${Math.round(Number(capa) * 100)} cm`);
  }
  return lineas.join('\n');
}
function esperadoDeMain(clave, { entrada, visibles: v, mensaje }) {
  const m = mensajeDeMain(clave, mensaje, entrada.capa);
  if (clave === 'tierra-negra') {
    return { cantidad: agrupar(v['res-m3']), presentacion: agrupar(v['res-formato'].replace(CAMION_MAIN, CAMION)),
      equivalente: agrupar(v['res-costales']), mensaje: m };
  }
  if (clave === 'tezontle') {
    return { cantidad: agrupar(v['tez-res-m3']), presentacion: agrupar(v['tez-res-formato']),
      equivalente: agrupar(v['tez-res-costales']), mensaje: m };
  }
  return { cantidad: `${agrupar(String(v['res-sacos']))} sacos`, peso: agrupar(v['res-peso']),
    nota: agrupar(v['res-nota'].replace(' sacos cubre ', ' sacos cubren ').replace(' A $250 c/u.', '')), mensaje: m };
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

test('miles con coma en kg, sacos, costales y área, sin redondear decimales', () => {
  assert.deepStrictEqual([999, 1000, 1250.5, 100000, 0.1].map(M.miles), ['999', '1,000', '1,250.5', '100,000', '0.1']);
  const cfg = CFG.marmol;
  const t = M.textos(cfg, 1250, 4, M.calcular(cfg, 1250, 4));
  assert.deepStrictEqual([t.cantidad, t.peso, t.nota], ['3,750 sacos', '75,000 kg', '3,750 sacos cubren 1,250 m² con capa de 4 cm.']);
});

test('con resultado, el mensaje conserva la colonia por llenar y la tierra negra manda la capa', () => {
  for (const cfg of Object.values(CFG)) {
    const capa = cfg.clave === 'marmol' ? 5 : 0.08;
    assert.ok(M.textos(cfg, 30, capa, M.calcular(cfg, 30, capa), 'x').mensaje.endsWith(`\n${M.COLONIA}\n\n${M.CIERRE}`));
  }
  assert.match(M.CIERRE, /Tampico, Madero o Altamira\?$/);
  const cfg = CFG['tierra-negra'];
  assert.match(M.textos(cfg, 30, 0.15, M.calcular(cfg, 30, 0.15)).mensaje, /Área: 30 m²\nCapa: 15 cm\nCantidad: 4.5 m³/);
});
