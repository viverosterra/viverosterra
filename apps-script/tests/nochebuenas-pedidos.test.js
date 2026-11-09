const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const RUTA_GS = path.join(__dirname, '..', 'nochebuenas-pedidos.gs');
const NOMBRE_HOJA = 'Pedidos Nochebuenas 2026';
const INICIO = Date.UTC(2026, 10, 9, 18, 0, 0);
const ENCABEZADOS = ['fecha_hora', 'lineas', 'piezas', 'escalon', 'total', 'preventa', 'zona', 'fecha_deseada',
  'tipo_cliente', 'factura', 'origen', 'utm_source', 'utm_medium', 'utm_campaign'];

const pedido = (cambios = {}) => ({
  lineas: '12 × Maceta 6" Roja | 4 × Maceta 7" Rosa',
  piezas: 16,
  escalon: 'Mayoreo',
  total: 2104,
  preventa: false,
  zona: 'Madero',
  fecha_deseada: '2026-11-28',
  tipo_cliente: 'Restaurante/hotel',
  factura: true,
  origen: '/post/nochebuenas-tampico-madero-mayoreo',
  utm_source: 'facebook',
  utm_medium: 'cpc',
  utm_campaign: 'nochebuenas',
  ...cambios,
});

const sin = (campo) => {
  const { [campo]: _quitado, ...resto } = pedido();
  return resto;
};

function cargar(fallas = {}) {
  const reloj = { ms: INICIO };
  const estado = { hojas: new Map(), cache: new Map(), errores: [], candado: { pedidos: 0, esperas: 0, liberados: 0, tomado: false } };

  class RelojFalso extends Date {
    constructor(...args) {
      if (args.length) super(...args);
      else super(reloj.ms);
    }
    static now() { return reloj.ms; }
  }

  const crearHoja = (nombre) => {
    const hoja = {
      filas: [],
      getLastRow: () => hoja.filas.length,
      appendRow(fila) {
        if (fallas.appendRow) throw new Error(fallas.appendRow);
        hoja.filas.push([...fila]);
      },
    };
    estado.hojas.set(nombre, hoja);
    return hoja;
  };

  const candado = {
    waitLock() {
      estado.candado.esperas += 1;
      if (fallas.waitLock) throw new Error(fallas.waitLock);
      estado.candado.tomado = true;
    },
    releaseLock() {
      if (!estado.candado.tomado) throw new Error('liberado sin haberse tomado');
      if (fallas.releaseLock) throw new Error(fallas.releaseLock);
      estado.candado.tomado = false;
      estado.candado.liberados += 1;
    },
  };

  const contexto = vm.createContext({
    Date: RelojFalso,
    console: { error: (...args) => estado.errores.push(args.join(' ')) },
    SpreadsheetApp: {
      flush() {},
      getActiveSpreadsheet: () => ({
        getSheetByName: (nombre) => estado.hojas.get(nombre) || null,
        insertSheet: crearHoja,
      }),
    },
    CacheService: {
      getScriptCache: () => ({
        get(clave) {
          if (fallas.cache) throw new Error(fallas.cache);
          const dato = estado.cache.get(clave);
          return dato && dato.vence > reloj.ms ? dato.valor : null;
        },
        put(clave, valor, segundos) {
          estado.cache.set(clave, { valor, vence: reloj.ms + segundos * 1000 });
        },
      }),
    },
    LockService: {
      getScriptLock() {
        if (fallas.getScriptLock) throw new Error(fallas.getScriptLock);
        estado.candado.pedidos += 1;
        return candado;
      },
    },
    ContentService: { createTextOutput: (texto) => ({ texto }) },
  });
  vm.runInContext(fs.readFileSync(RUTA_GS, 'utf8'), contexto);

  const enviar = (cuerpo) => contexto.doPost({
    postData: { contents: typeof cuerpo === 'string' ? cuerpo : JSON.stringify(cuerpo) },
  }).texto;
  const filas = () => (estado.hojas.get(NOMBRE_HOJA) || { filas: [] }).filas;
  const datos = () => filas().slice(1);
  return { contexto, enviar, filas, datos, estado, reloj };
}

function assertRechazado(cuerpo) {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(cuerpo), 'error');
  assert.strictEqual(datos().length, 0);
}

test('una fila válida trae las 14 columnas en orden', () => {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido()), 'ok');
  assert.strictEqual(datos().length, 1);
  const [fecha, ...resto] = datos()[0];
  assert.strictEqual(datos()[0].length, 14);
  assert.strictEqual(new Date(fecha).getTime(), INICIO);
  assert.deepStrictEqual(resto, ['12 × Maceta 6" Roja | 4 × Maceta 7" Rosa', 16, 'Mayoreo', 2104, 'no', 'Madero', '2026-11-28',
    'Restaurante/hotel', 'sí', '/post/nochebuenas-tampico-madero-mayoreo', 'facebook', 'cpc', 'nochebuenas']);
});

test('los campos opcionales pueden venir vacíos o no venir', () => {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido({ zona: '', fecha_deseada: '', tipo_cliente: '' })), 'ok');
  assert.strictEqual(enviar(sin('zona')), 'ok');
  assert.strictEqual(enviar(sin('fecha_deseada')), 'ok');
  assert.strictEqual(enviar(sin('tipo_cliente')), 'ok');
  assert.strictEqual(datos().length, 4);
  assert.strictEqual(datos()[1][6], '');
});

test('crea la hoja y escribe los encabezados una sola vez', () => {
  const { enviar, filas, estado } = cargar();
  enviar(pedido());
  enviar(pedido());
  assert.deepStrictEqual([...estado.hojas.keys()], [NOMBRE_HOJA]);
  assert.strictEqual(filas().length, 3);
  assert.deepStrictEqual(filas()[0], ENCABEZADOS);
  assert.strictEqual(filas()[1][0] === 'fecha_hora', false);
});

for (const signo of ['=', '+', '-', '@']) {
  const formula = `${signo}IMPORTXML("https://x.example","//a")`;
  test(`fórmula con ${signo} en origen queda como texto`, () => {
    const { enviar, datos } = cargar();
    assert.strictEqual(enviar(pedido({ origen: formula })), 'ok');
    assert.strictEqual(datos()[0][10], `'${formula}`);
  });
  test(`fórmula con ${signo} en lineas se rechaza`, () => assertRechazado(pedido({ lineas: formula })));
  for (const [campo, columna] of [['utm_source', 11], ['utm_medium', 12], ['utm_campaign', 13]]) {
    test(`fórmula con ${signo} en ${campo} queda vacía`, () => {
      const { enviar, datos } = cargar();
      assert.strictEqual(enviar(pedido({ [campo]: formula })), 'ok');
      assert.strictEqual(datos()[0][columna], '');
    });
  }
}

test('un UTM válido que empieza con guion sigue neutralizado', () => {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido({ utm_source: '-abc.1_x' })), 'ok');
  assert.strictEqual(datos()[0][11], "'-abc.1_x");
});

for (const prefijo of [' ', '   ', '\n', '\t', '\r\n ', '\u0000', ' ']) {
  test(`fórmula tras el prefijo ${JSON.stringify(prefijo)} también queda como texto`, () => {
    const { enviar, datos } = cargar();
    assert.strictEqual(enviar(pedido({ origen: `${prefijo}=1+1` })), 'ok');
    assert.strictEqual(datos()[0][10], "'=1+1");
  });
}

test('recorta el origen largo, aplana sus saltos de línea y vacía el UTM demasiado largo', () => {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido({ origen: 'a\nb'.repeat(300), utm_source: 'x'.repeat(101), utm_medium: 'x'.repeat(100) })), 'ok');
  assert.strictEqual(datos()[0][10].length, 200);
  assert.ok(!/[\r\n\t]/.test(datos()[0][10]));
  assert.strictEqual(datos()[0][11], '');
  assert.strictEqual(datos()[0][12].length, 100);
});

for (const [nombre, lineas, piezas] of [
  ['lineas sin el formato', 'dos plantas rojas', 2],
  ['producto desconocido', '2 × Maceta 9" Roja', 2],
  ['variedad desconocida', '2 × Maceta 6" Azul', 2],
  ['separador equivocado', '1 × Maceta 6" Roja, 1 × Colgante Rosa', 2],
  ['cantidad en cero', '0 × Maceta 6" Roja', 0],
  ['cantidad de cinco cifras', '10000 × Maceta 6" Roja', 10000],
]) {
  test(`rechaza ${nombre}`, () => assertRechazado(pedido({ lineas, piezas, escalon: 'Menudeo', total: 100 })));
}

test('acepta todos los productos y variedades del catálogo', () => {
  const { enviar, datos } = cargar();
  const lineas = '1 × Maceta 5" Roja | 1 × Maceta 7" Jaspeada | 1 × Colgante Rosa | 1 × Macetón 12" Roja';
  assert.strictEqual(enviar(pedido({ lineas, piezas: 4, escalon: 'Menudeo', total: 1822 })), 'ok');
  assert.strictEqual(datos()[0][1], lineas);
});

test('rechaza piezas que no igualan la suma de las líneas', () => assertRechazado(pedido({ piezas: 17 })));

for (const [piezas, correcto, incorrecto] of [[11, 'Menudeo', 'Mayoreo'], [12, 'Mayoreo', 'Menudeo'], [50, 'Mayoreo Plus', 'Mayoreo'], [200, 'Proyecto', 'Mayoreo Plus']]) {
  const lineas = `${piezas} × Maceta 6" Roja`;
  test(`${piezas} piezas: acepta ${correcto} y rechaza ${incorrecto}`, () => {
    const { enviar, datos } = cargar();
    assert.strictEqual(enviar(pedido({ lineas, piezas, escalon: correcto, total: 100 })), 'ok');
    assert.strictEqual(enviar(pedido({ lineas, piezas, escalon: incorrecto, total: 100 })), 'error');
    assert.strictEqual(datos().length, 1);
  });
}

test('rechaza un total mayor que piezas por el precio máximo', () => {
  const lineas = '2 × Macetón 12" Roja';
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido({ lineas, piezas: 2, escalon: 'Menudeo', total: 2390 })), 'ok');
  assert.strictEqual(enviar(pedido({ lineas, piezas: 2, escalon: 'Menudeo', total: 2391 })), 'error');
  assert.strictEqual(datos().length, 1);
});

test('no guarda campos fuera del contrato, como nombre o teléfono', () => {
  const { enviar, filas, datos } = cargar();
  assert.strictEqual(enviar(pedido({ nombre: 'Persona Prueba', telefono: '8330000000' })), 'ok');
  const texto = JSON.stringify(filas());
  assert.ok(!texto.includes('Persona Prueba'));
  assert.ok(!texto.includes('8330000000'));
  assert.strictEqual(datos()[0].length, 14);
});

for (const [nombre, cambios] of [
  ['zona fuera de catálogo', { zona: 'Monterrey' }],
  ['tipo de cliente fuera de catálogo', { tipo_cliente: 'Otro' }],
  ['escalón fuera de catálogo', { escalon: 'Gratis' }],
  ['zona con tipo equivocado', { zona: ['Madero'] }],
  ['zona falsa', { zona: false }],
  ['tipo de cliente en cero', { tipo_cliente: 0 }],
  ['fecha con otro formato', { fecha_deseada: '28/11/2026' }],
  ['fecha imposible', { fecha_deseada: '2026-13-45' }],
  ['fecha en arreglo', { fecha_deseada: ['2026-11-28'] }],
  ['fecha con fórmula', { fecha_deseada: '=NOW()' }],
]) {
  test(`rechaza ${nombre}`, () => assertRechazado(pedido(cambios)));
}

for (const [nombre, cuerpo] of [['JSON roto', '{no es json'], ['cuerpo vacío', ''], ['null', 'null'], ['arreglo', '[]'], ['número', '5']]) {
  test(`rechaza ${nombre} sin agregar fila`, () => assertRechazado(cuerpo));
}

test('un cuerpo enorme se ignora y no agrega fila', () => {
  const { enviar, datos } = cargar();
  assert.strictEqual(enviar(pedido({ origen: 'x'.repeat(5001) })), 'ignorado');
  assert.strictEqual(datos().length, 0);
});

test('sin postData no truena ni agrega fila', () => {
  const { contexto, datos } = cargar();
  assert.strictEqual(contexto.doPost(undefined).texto, 'error');
  assert.strictEqual(contexto.doPost({}).texto, 'error');
  assert.strictEqual(datos().length, 0);
});

for (const campo of [['preventa', 5], ['factura', 9]]) {
  test(`${campo[0]} acepta booleanos reales`, () => {
    const { enviar, datos } = cargar();
    enviar(pedido({ [campo[0]]: true }));
    enviar(pedido({ [campo[0]]: false }));
    assert.deepStrictEqual(datos().map((f) => f[campo[1]]), ['sí', 'no']);
  });

  for (const valor of ['false', 'true', 0, 1, null, [], {}]) {
    test(`${campo[0]} rechaza ${JSON.stringify(valor)}`, () => assertRechazado(pedido({ [campo[0]]: valor })));
  }

  test(`${campo[0]} es obligatorio`, () => assertRechazado(sin(campo[0])));
}

for (const campo of ['piezas', 'total']) {
  for (const valor of ['16', '', null, true, [16], -1, 1e12]) {
    test(`${campo} rechaza ${JSON.stringify(valor)}`, () => assertRechazado(pedido({ [campo]: valor })));
  }
  test(`${campo} es obligatorio`, () => assertRechazado(sin(campo)));
}

test('más de 30 en un minuto se ignora, se anota y al minuto siguiente vuelve a aceptar', () => {
  const { enviar, datos, reloj, estado } = cargar();
  for (let i = 0; i < 30; i += 1) assert.strictEqual(enviar(pedido()), 'ok');
  assert.strictEqual(enviar(pedido()), 'ignorado');
  assert.strictEqual(datos().length, 30);
  assert.strictEqual(estado.errores.length, 1);
  reloj.ms += 60 * 1000;
  assert.strictEqual(enviar(pedido()), 'ok');
  assert.strictEqual(datos().length, 31);
});

test('un cuerpo inválido no cuenta contra el límite', () => {
  const { enviar, datos } = cargar();
  for (let i = 0; i < 40; i += 1) assert.strictEqual(enviar(pedido({ zona: 'Monterrey' })), 'error');
  assert.strictEqual(enviar(pedido()), 'ok');
  assert.strictEqual(datos().length, 1);
});

test('más de 2,000 en un día se ignora y al día siguiente vuelve a aceptar', () => {
  const { enviar, datos, reloj } = cargar();
  for (let i = 0; i < 2000; i += 1) {
    assert.strictEqual(enviar(pedido()), 'ok');
    reloj.ms += 3 * 1000;
  }
  assert.strictEqual(enviar(pedido()), 'ignorado');
  assert.strictEqual(datos().length, 2000);
  reloj.ms += 24 * 60 * 60 * 1000;
  assert.strictEqual(enviar(pedido()), 'ok');
});

test('con más de 5,000 renglones ya no escribe y lo anota', () => {
  const { enviar, filas, estado } = cargar();
  enviar(pedido());
  estado.hojas.get(NOMBRE_HOJA).filas.push(...Array(5000).fill(['x']));
  const antes = filas().length;
  assert.strictEqual(enviar(pedido()), 'ignorado');
  assert.strictEqual(filas().length, antes);
  assert.strictEqual(estado.errores.length, 1);
});

test('el tráfico lento y constante nunca llega al límite', () => {
  const { enviar, datos, reloj } = cargar();
  for (let i = 0; i < 90; i += 1) {
    assert.strictEqual(enviar(pedido()), 'ok');
    reloj.ms += 50 * 1000;
  }
  assert.strictEqual(datos().length, 90);
});

test('una fila aceptada toma y suelta el candado una sola vez', () => {
  const { enviar, estado } = cargar();
  assert.strictEqual(enviar(pedido()), 'ok');
  assert.deepStrictEqual([estado.candado.esperas, estado.candado.liberados, estado.candado.tomado], [1, 1, false]);
});

test('salir antes de esperar el candado no intenta soltarlo', () => {
  const { enviar, estado } = cargar();
  assert.strictEqual(enviar(pedido({ origen: 'x'.repeat(5001) })), 'ignorado');
  assert.deepStrictEqual([estado.candado.esperas, estado.candado.liberados], [0, 0]);
  assert.ok(!estado.errores.some((e) => e.includes('liberado sin haberse tomado')));
});

test('si no se consigue el candado no intenta soltarlo ni escribe', () => {
  const { enviar, datos, estado } = cargar({ waitLock: 'detalle interno de candado' });
  assert.strictEqual(enviar(pedido()), 'error');
  assert.deepStrictEqual([estado.candado.esperas, estado.candado.liberados], [1, 0]);
  assert.strictEqual(datos().length, 0);
  assert.ok(!estado.errores.some((e) => e.includes('liberado sin haberse tomado')));
});

test('si falla la escritura suelta el candado', () => {
  const { enviar, estado } = cargar({ appendRow: 'detalle interno de hoja' });
  assert.strictEqual(enviar(pedido()), 'error');
  assert.deepStrictEqual([estado.candado.liberados, estado.candado.tomado], [1, false]);
});

for (const servicio of ['getScriptLock', 'waitLock', 'appendRow', 'releaseLock', 'cache']) {
  test(`una falla en ${servicio} responde solo "error" al cliente`, () => {
    const { enviar } = cargar({ [servicio]: 'SECRETO hoja 1a2b3c' });
    assert.strictEqual(enviar(pedido()), 'error');
  });
}

test('los errores se anotan para el dueño del script', () => {
  const { enviar, estado } = cargar();
  enviar(pedido({ zona: 'Monterrey' }));
  assert.strictEqual(estado.errores.length, 1);
});
