// public/js/tests/vt-materiales.test.js
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const fs = require('node:fs');
const M = require('../vt-materiales.js');

const CASOS = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-materiales.json'), 'utf8'));
// Lo que escribe componentes_materiales.datos_js(clave) en data-material (test_componentes_materiales lo compara).
const CFG = {
  'tierra-negra': { clave: 'tierra-negra', costal_m3: 0.035, precio_costal: 90, precio_m3: 1500,
    camiones: [[8, 5200], [14, 8000]], texto: 'tierra negra vegetal' },
  tezontle: { clave: 'tezontle', costal_m3: 0.027, camion_m3: 14, texto: 'tezontle rojo' },
  marmol: { clave: 'marmol', kg_saco: 20, precio_saco: 250, texto: 'mármol blanco decorativo' },
  'piedra-bola': { clave: 'piedra-bola', kg_m2: [120, 150], capa_texto: '8 a 10 cm', texto: 'piedra bola de río' },
};
const CAMION_MAIN = 'Camión volteo 8m³+ (~desde $5,000)';
// Igual que camion_tierra() de componentes_materiales.py: el camión de la tabla de datos.py donde cabe la cantidad.
function camion(m3) {
  if (m3 <= 8) return 'Camión volteo de 8 m³ ($5,200)';
  if (m3 <= 14) return 'Camión volteo de 14 m³ ($8,000)';
  return `${Math.ceil(m3 / 14)} camiones volteo de 14 m³ ($8,000 c/u)`;
}

// Igual que agrupar, mensaje_de_main y esperado_de_main de tests/test_materiales_paridad.py.
const agrupar = (t) => t.replace(/(?<![\d.,])\d{4,}/g, (n) => Number(n).toLocaleString('en-US'));
function mensajeDeMain(clave, m, capa) {
  const lineas = m.split('\n').map(agrupar);
  lineas[lineas.length - 1] = M.CIERRE;
  lineas.splice(lineas.length - 2, 0, M.COLONIA);
  if (clave === 'tierra-negra') {
    // Entrega B de experiencia (reescritura 15): el cálculo en un renglón, costales o a granel, la colonia y una pregunta corta.
    const area = lineas.find((x) => x.startsWith('Área: ')).slice('Área: '.length);
    const m3 = lineas.find((x) => x.startsWith('Cantidad: ')).slice('Cantidad: '.length);
    return [lineas[0], `Área: ${area}, capa de ${Math.round(Number(capa) * 100)} cm = ${m3} (cálculo de la web)`,
      'En costales o a granel: ___', M.COLONIA, '¿Me dan el total con entrega?'].join('\n');
  }
  return lineas.join('\n');
}
function esperadoDeMain(clave, { entrada, visibles: v, mensaje }) {
  const m = mensajeDeMain(clave, mensaje, entrada.capa);
  if (clave === 'tierra-negra') {
    return { cantidad: agrupar(v['res-m3']),
      presentacion: agrupar(v['res-formato'].replace(CAMION_MAIN, camion(Number(v['res-m3'].split(' ')[0])))),
      equivalente: agrupar(v['res-costales']), mensaje: m };
  }
  if (clave === 'tezontle') {
    return { cantidad: agrupar(v['tez-res-m3']), presentacion: agrupar(v['tez-res-formato']),
      equivalente: agrupar(v['tez-res-costales']), mensaje: m };
  }
  return { cantidad: `${agrupar(String(v['res-sacos']))} sacos`, total: v['res-precio'], peso: agrupar(v['res-peso']),
    nota: agrupar(v['res-nota'].replace(' sacos cubre ', ' sacos cubren ')), mensaje: m };
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
    // Entrega B de experiencia (reescritura 15): la tierra negra cierra con una pregunta corta.
    assert.ok(t.mensaje.endsWith(cfg.clave === 'tierra-negra' ? '¿Me dan el total con entrega?' : M.CIERRE));
    assert.doesNotMatch(t.mensaje, /<|disponibilidad|chica|mediana|grande/);
  }
});

test('miles con coma en kg, sacos, costales y área, sin redondear decimales', () => {
  assert.deepStrictEqual([999, 1000, 1250.5, 100000, 0.1].map(M.miles), ['999', '1,000', '1,250.5', '100,000', '0.1']);
  const cfg = CFG.marmol;
  const t = M.textos(cfg, 1250, 4, M.calcular(cfg, 1250, 4));
  assert.deepStrictEqual([t.cantidad, t.total, t.peso, t.nota],
    ['3,750 sacos', '$937,500', '75,000 kg', '3,750 sacos cubren 1,250 m² con capa de 4 cm. A $250 c/u.']);
});

test('con resultado, el mensaje conserva la colonia por llenar y la tierra negra manda la capa', () => {
  for (const cfg of Object.values(CFG).filter((x) => x.clave !== 'tierra-negra')) {
    const capa = cfg.clave === 'marmol' ? 5 : 0.08;
    assert.ok(M.textos(cfg, 30, capa, M.calcular(cfg, 30, capa), 'x').mensaje.endsWith(`\n${M.COLONIA}\n\n${M.CIERRE}`));
  }
  assert.match(M.CIERRE, /Tampico, Madero o Altamira\?$/);
  const cfg = CFG['tierra-negra'];
  // Entrega B de experiencia (reescritura 15): cálculo en un renglón, costales o a granel y la colonia.
  assert.strictEqual(M.textos(cfg, 30, 0.15, M.calcular(cfg, 30, 0.15)).mensaje, 'Hola, quiero cotizar tierra negra vegetal.\n'
    + `Área: 30 m², capa de 15 cm = 4.5 m³ (cálculo de la web)\nEn costales o a granel: ___\n${M.COLONIA}\n¿Me dan el total con entrega?`);
});

test('areaInvalida: 0, negativos y letras avisan; vacío no; los textos son los de componentes_materiales.py', () => {
  for (const malo of ['0', '-4', 'abc', '200000']) assert.strictEqual(M.areaInvalida(malo), true, malo);
  for (const bueno of ['', ' ', '30', '1,200', '12,5']) assert.strictEqual(M.areaInvalida(bueno), false, bueno);
  assert.strictEqual(M.CTA_CALCULO, 'Enviar mi cálculo por WhatsApp');
  assert.strictEqual(M.ERROR_AREA, 'Escribe el área en m², solo con números. Ejemplo: 30.');
});
