const test = require('node:test');
const assert = require('node:assert');
const nb = require('../vt-nochebuenas.js');
const cfg = { temporada:2026, cortes:[1,12,50,200], nombres_escalon:['Menudeo','Mayoreo','Mayoreo Plus','Proyecto'],
  productos:[{clave:'5',nombre:'Maceta 5"',precios:[89,75,69,65]},{clave:'6',nombre:'Maceta 6"',precios:[139,119,109,105]},
    {clave:'7',nombre:'Maceta 7"',precios:[199,169,155,149]},{clave:'colgante',nombre:'Colgante',precios:[339,279,259,249]},
    {clave:'12',nombre:'Macetón 12"',precios:[1195,995,899,865],sobre_pedido:true}],
  entrega_incluida_desde:3500, anticipo_pct:50, preventa:{descuento:0.05,hasta:'2026-11-20',aplica_hasta_escalon:2} };
const FUERA = '2026-12-01';
const L = (clave, cantidad, variedad='Roja') => ({clave, variedad, cantidad});
const mixto = [L('6',16), L('7',4,'Jaspeada'), L('colgante',6,'Rosa')];

test('10 de 6" a menudeo, con nudge honesto', () => {
  assert.strictEqual(nb.cotizar([L('6',10)], cfg, FUERA).total, 1390);
  const n = nb.nudge([L('6',10)], cfg, FUERA);
  assert.deepStrictEqual([n.faltan,n.nombre,n.objetivo,n.diferencia,n.ahorro],[2,'Mayoreo',12,38,240]);
  assert.strictEqual(n.texto,'Te faltan 2 piezas para precio Mayoreo: por $38 más te llevas 12 y ahorras $240');
});
test('12 de 6" a mayoreo, sin nudge', () => {
  const c = nb.cotizar([L('6',12)], cfg, FUERA);
  assert.deepStrictEqual([c.total,c.nombreEscalon,c.ahorro],[1428,'Mayoreo',240]);
  assert.strictEqual(nb.nudge([L('6',12)], cfg, FUERA), null);
});
test('26 mezcladas recalculan todas las líneas', () => {
  const c = nb.cotizar(mixto, cfg, FUERA);
  assert.deepStrictEqual([c.piezas,c.total,c.nombreEscalon,c.ahorro],[26,4254,'Mayoreo',800]);
  assert.deepStrictEqual(c.lineas.map(l=>l.subtotal),[1904,676,1674]);
});
test('preventa incluye el último día y no el siguiente', () => {
  assert.deepStrictEqual((({preventa,descuento,total})=>[preventa,descuento,total])(nb.cotizar([L('6',12)],cfg,'2026-11-20')),[true,71,1357]);
  assert.strictEqual(nb.cotizar([L('6',12)],cfg,'2026-11-21').total,1428);
});
test('preventa nunca en Proyecto', () => {
  const c = nb.cotizar([L('5',200)],cfg,'2026-11-10');
  assert.deepStrictEqual([c.preventa,c.total,c.proyecto],[false,13000,true]);
});
test('nudge cuando el pedido completo sale más barato', () => {
  const n = nb.nudge([L('5',199)],cfg,FUERA);
  assert.deepStrictEqual([n.faltan,n.diferencia,n.ahorro],[1,-731,800]);
  assert.strictEqual(n.texto,'Te falta 1 pieza para precio Proyecto: te llevas 200, pagas $731 menos y ahorras $800');
});
test('nudge solo con 4 piezas o menos', () => {
  assert.strictEqual(nb.nudge([L('6',7)],cfg,FUERA),null);
  assert.strictEqual(nb.nudge([L('6',8)],cfg,FUERA).faltan,4);
});
test('pedido vacío y cantidades inválidas', () => {
  const c = nb.cotizar([L('6',-3),L('7','x')],cfg,FUERA);
  assert.deepStrictEqual([c.piezas,c.escalon,c.total],[0,-1,0]);
  assert.strictEqual(nb.nudge([L('6',0)],cfg,FUERA),null);
});
test('macetón marca sobre pedido', () => assert.ok(nb.cotizar([L('12',1)],cfg,FUERA).haySobrePedido));
test('entrega', () => {
  assert.strictEqual(nb.entrega(3500,'Altamira',cfg).texto,'Entrega incluida');
  assert.strictEqual(nb.entrega(3499,'Madero',cfg).faltan,1);
  assert.strictEqual(nb.entrega(9000,'Recojo en vivero',cfg),null);
});
test('mensaje con el formato del dueño', () => {
  const c = nb.cotizar(mixto,cfg,FUERA);
  assert.strictEqual(nb.mensaje(c,{zona:'Madero',fecha:'2026-11-28',tipo:'Restaurante/hotel',factura:true},cfg),
`Hola Viveros Terra 🌺 Quiero cotizar Nochebuenas 2026:
• 16 × Maceta 6" Roja
• 4 × Maceta 7" Jaspeada
• 6 × Colgante Rosa
Total: 26 piezas · Escalón: Mayoreo · Total estimado: $4,254
Entrega: Madero · 28 nov · Requiero factura
Tipo de cliente: Restaurante/hotel`);
});
test('mensaje indica preventa', () => assert.match(nb.mensaje(nb.cotizar([L('6',12)],cfg,'2026-11-10'),{},cfg),/Precio preventa/));
test('un endpoint inválido o una falla no rompen nada', () => {
  let n = 0; const nav = {sendBeacon(){ n++; throw new Error('x'); }};
  nb.enviarRegistro('', {}, nav); nb.enviarRegistro('https://evil.example/', {}, nav); assert.strictEqual(n,0);
  assert.doesNotThrow(()=>nb.enviarRegistro('https://script.google.com/macros/s/abc/exec',{a:1},nav)); assert.strictEqual(n,1);
});
test('hoyMX usa la hora de México', () => assert.strictEqual(nb.hoyMX(new Date('2026-11-21T03:00:00Z')),'2026-11-20'));

// Casos añadidos a los del plan: bordes que el plan no cubre.
test('sin nudge si subir de escalón durante la preventa no ahorra', () => {
  // Con 5% de preventa, 200×$105 cuesta más que 200×$109 con descuento: no se puede prometer un ahorro.
  assert.strictEqual(nb.nudge([L('6',199)],cfg,'2026-11-10'),null);
});
test('el nudge usa el producto de la última línea con piezas', () => {
  const n = nb.nudge([L('5',5),L('7',6),L('6',0)],cfg,FUERA);
  assert.deepStrictEqual([n.faltan,n.diferencia],[1,(5*75+7*169)-(5*89+6*199)]);
});
test('cantidades: se truncan, se topan y claves desconocidas se ignoran', () => {
  const c = nb.cotizar([L('6','3.9'),L('7',20000),L('nada',5)],cfg,FUERA);
  assert.deepStrictEqual(c.lineas.map(l=>l.cantidad),[3,9999]);
});
test('las funciones puras no mutan sus entradas', () => {
  const lineas = Object.freeze([Object.freeze(L('6',10))]);
  assert.doesNotThrow(()=>{ nb.cotizar(lineas,cfg,FUERA); nb.nudge(lineas,cfg,FUERA); });
  assert.strictEqual(lineas[0].cantidad,10);
});
test('entrega abajo del mínimo da el texto completo', () => {
  assert.strictEqual(nb.entrega(3499,'Madero',cfg).texto,'Te faltan $1 para entrega incluida. Entrega según tu ubicación o colonia; te la cotizamos por WhatsApp.');
});
test('mensaje en modo preventa y sin datos opcionales', () => {
  const c = nb.cotizar([L('6',1)],cfg,FUERA);
  assert.strictEqual(nb.mensaje(c,{},{...cfg,modo:'preventa'}),
`Hola Viveros Terra 🌺 Quiero apartar Nochebuenas 2026:
• 1 × Maceta 6" Roja
Total: 1 pieza · Escalón: Menudeo · Total estimado: $139`);
});
test('registro para Sheets', () => {
  assert.deepStrictEqual(nb.registro(nb.cotizar(mixto,cfg,FUERA),{zona:'Madero',fecha:'2026-11-28',tipo:'Gobierno',factura:true},cfg,
    {pathname:'/post/x',search:'?utm_source=fb&utm_medium=cpc&utm_campaign=nb'}),
    {lineas:'16 × Maceta 6" Roja | 4 × Maceta 7" Jaspeada | 6 × Colgante Rosa',piezas:26,escalon:'Mayoreo',total:4254,preventa:false,
     zona:'Madero',fecha_deseada:'2026-11-28',tipo_cliente:'Gobierno',factura:true,origen:'/post/x',utm_source:'fb',utm_medium:'cpc',utm_campaign:'nb'});
});

test('ahorro con preventa no cuenta el descuento: es menudeo menos subtotal', () => {
  const c = nb.cotizar([L('6',12)],cfg,'2026-11-10');
  assert.deepStrictEqual([c.subtotal,c.descuento,c.total,c.ahorro],[1428,71,1357,240]);
});
test('a precio de menudeo no hay ahorro aunque haya preventa', () => {
  const c = nb.cotizar([L('6',2)],cfg,'2026-11-10');
  assert.strictEqual(c.ahorro,0);
  assert.ok(c.descuento > 0);
});
test('entrega sin zona: dice las tres ciudades si alcanza; con zona, igual que antes', () => {
  assert.strictEqual(nb.entrega(3500,'',cfg).texto,'Entrega incluida desde $3,500 en Tampico, Madero y Altamira.');
  assert.strictEqual(nb.entrega(3500,undefined,cfg).incluida,true);
  assert.strictEqual(nb.entrega(3500,'Tampico',cfg).texto,'Entrega incluida');
  assert.strictEqual(nb.entrega(3499,'',cfg).faltan,1);
});
test('el anticipo del mensaje sale de cfg', () => {
  const c = nb.cotizar([L('6',12)],cfg,'2026-11-10');
  assert.match(nb.mensaje(c,{},cfg),/apartando con 50% de anticipo/);
  assert.match(nb.mensaje(c,{},{...cfg,anticipo_pct:40}),/apartando con 40% de anticipo/);
});
test('duplicado: mismo envío dentro de 10 s; distinto o después, no', () => {
  const previo = {clave:'a',t:1000};
  assert.strictEqual(nb.esDuplicado(null,'a',1000),false);
  assert.strictEqual(nb.esDuplicado(previo,'a',10999),true);
  assert.strictEqual(nb.esDuplicado(previo,'a',11000),false);
  assert.strictEqual(nb.esDuplicado(previo,'b',2000),false);
});
test('textos de la barra', () => {
  const c = nb.cotizar([L('6',12)],cfg,'2026-11-10');
  const vacia = nb.cotizar([L('6',0)],cfg,FUERA);
  assert.deepStrictEqual(nb.textoBarra(c,false,false,cfg),{texto:'Cotizar mi pedido',href:'#cotizador'});
  assert.deepStrictEqual(nb.textoBarra(vacia,true,false,cfg),{texto:'Cotizar mi pedido',href:'#cotizador'});
  assert.deepStrictEqual(nb.textoBarra(c,true,false,cfg),{texto:'Cotizar · $1,357',href:'#cotizador'});
  assert.deepStrictEqual(nb.textoBarra(c,true,true,cfg),{texto:'12 piezas · $1,357 · Ver total',href:'#nb-ticket'});
  assert.deepStrictEqual(nb.textoBarra(c,true,false,{...cfg,modo:'preventa'}),{texto:'Apartar · $1,357',href:'#cotizador'});
  assert.deepStrictEqual(nb.textoBarra(c,false,false,{...cfg,modo:'preventa'}),{texto:'Apartar mi pedido',href:'#cotizador'});
});
