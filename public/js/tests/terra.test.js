// public/js/tests/terra.test.js
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { FIRMA, HERO_CTA, ABIERTO, tipoEnlace, conFirma, evento, eventoWhatsapp, abierto, horario } = require('../terra.js');

const HORARIO = JSON.parse(fs.readFileSync(path.join(__dirname, 'casos-horario.json'), 'utf8'));

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

test('generate_lead lleva cta y servicio; click_to_call lleva cta, tipo y servicio', () => {
  const ctx = { tipo: 'blog', servicio: 'general' };
  assert.deepStrictEqual(evento(enlace({ href: 'https://wa.me/528333268008?text=a', 'data-cta': 'blog:header' }), ctx), {
    nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: 'blog:header', service: 'general' },
  });
  assert.deepStrictEqual(evento(enlace({ href: 'tel:+528333268008' }), ctx), {
    nombre: 'click_to_call', params: { link_type: 'tel', cta_id: 'blog:sin-etiqueta', service: 'general' },
  });
  assert.strictEqual(evento(enlace({ href: '/precios' }), ctx), null);
});

test('click_to_call lleva link_type y servicio de la página', () => {
  const ctx = { tipo: 'servicio', servicio: 'pasto-natural' };
  assert.deepStrictEqual(evento(enlace({ href: 'tel:+528333268008', 'data-cta': 'servicio:barra' }), ctx), {
    nombre: 'click_to_call', params: { link_type: 'tel', cta_id: 'servicio:barra', service: 'pasto-natural' },
  });
});

// ---------- DOM falso mínimo para menu(), barra() y medir() ----------
class Nodo {
  constructor(doc, { clases = [], atributos = {}, padre = null, tag = 'div' } = {}) {
    this.doc = doc;
    this.tag = tag;
    this.clases = new Set(clases);
    this.atributos = { ...atributos };
    this.padre = padre;
    this.oyentes = {};
    this.hidden = false;
    this.inert = false;
    const nodo = this;
    this.classList = {
      contains: (c) => nodo.clases.has(c),
      toggle: (c, si) => { if (si) nodo.clases.add(c); else nodo.clases.delete(c); },
    };
  }
  getAttribute(n) { return n in this.atributos ? this.atributos[n] : null; }
  setAttribute(n, v) { this.atributos[n] = String(v); }
  addEventListener(tipo, fn) { (this.oyentes[tipo] = this.oyentes[tipo] || []).push(fn); }
  matches(selector) {
    return selector.split(',').map((s) => s.trim()).some((s) => {
      if (s.startsWith('.')) return this.clases.has(s.slice(1));
      if (s === 'a[href]') return this.tag === 'a' && 'href' in this.atributos;
      const m = s.match(/^\[([\w-]+)\]$/);
      if (m) return m[1] in this.atributos;
      return false;
    });
  }
  closest(selector) {
    for (let n = this; n; n = n.padre) if (n.matches(selector)) return n;
    return null;
  }
  contains(otro) {
    for (let n = otro; n; n = n.padre) if (n === this) return true;
    return false;
  }
  focus() { this.doc.activeElement = this; }
}

function despachar(objetivo, tipo, extra = {}) {
  const e = { type: tipo, target: objetivo, defaultPrevented: false, stopPropagation() {}, preventDefault() { this.defaultPrevented = true; }, ...extra };
  for (let n = objetivo; n; n = n.padre) (n.oyentes[tipo] || []).forEach((fn) => fn(e));
  (objetivo.doc.oyentes[tipo] || []).forEach((fn) => fn(e));
  return e;
}

function armarPagina() {
  const doc = { oyentes: {}, activeElement: null, addEventListener(t, fn) { (this.oyentes[t] = this.oyentes[t] || []).push(fn); } };
  const n = (opciones) => new Nodo(doc, opciones);
  const body = n({ tag: 'body' });
  const head = n({ clases: ['vt-head'], atributos: { 'data-vt-tipo': 'servicio', 'data-vt-servicio': 'pasto-natural' }, padre: body });
  const nav = n({ clases: ['vt-nav'], padre: head });
  const item1 = n({ clases: ['vt-nav__item'], padre: nav });
  const exp1 = n({ tag: 'button', clases: ['vt-nav__exp'], atributos: { 'aria-expanded': 'false', 'aria-controls': 'p1' }, padre: item1 });
  const enlace1 = n({ tag: 'a', atributos: { href: '/pasto' }, padre: item1 });
  const item2 = n({ clases: ['vt-nav__item'], padre: nav });
  const exp2 = n({ tag: 'button', clases: ['vt-nav__top'], atributos: { 'aria-expanded': 'false', 'aria-controls': 'p2' }, padre: item2 });
  const burger = n({ tag: 'button', clases: ['vt-burger'], atributos: { 'aria-expanded': 'false', 'aria-controls': 'vt-mmenu' }, padre: head });
  const movil = n({ atributos: { id: 'vt-mmenu' }, padre: head });
  movil.hidden = true;
  const afuera = n({ padre: body });
  const bar = n({ clases: ['vt-bar'], atributos: { 'data-vt-bar': '' }, padre: body });
  const hero = n({ atributos: { 'data-hero-cta': '' }, padre: body });
  const wa = n({ tag: 'a', atributos: { href: 'https://wa.me/528333268008?text=Hola', 'data-cta': 'servicio:barra' }, padre: bar });
  const tel = n({ tag: 'a', atributos: { href: 'tel:+528333268008', 'data-cta': 'servicio:barra' }, padre: bar });
  const hero2 = n({ atributos: { 'data-cta': 'home:hero' }, padre: body });
  const consultas = { '.vt-burger': burger, '.vt-head': head, '[data-vt-bar]': bar };
  const listas = { '.vt-nav [aria-controls]': [exp1, exp2], [HERO_CTA]: [hero, hero2] };
  doc.querySelector = (s) => consultas[s] || null;
  doc.querySelectorAll = (s) => listas[s] || [];
  doc.getElementById = (id) => (id === 'vt-mmenu' ? movil : null);
  const relojes = [];
  const enviados = [];
  const win = {
    setTimeout: (fn, ms) => { relojes.push({ fn, ms }); return relojes.length; },
    clearTimeout: (id) => { if (relojes[id - 1]) relojes[id - 1].fn = null; },
    gtag: (...args) => enviados.push(args),
  };
  const correrRelojes = () => relojes.splice(0).forEach((r) => r.fn && r.fn());
  return { doc, win, item1, exp1, enlace1, item2, exp2, burger, movil, afuera, bar, hero, hero2, wa, tel, correrRelojes, enviados };
}

const { menu, barra, medir, medicion } = require('../terra.js');

test('el burger abre y cierra el menú móvil con aria-expanded en sincronía', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.burger, 'click');
  assert.strictEqual(p.burger.getAttribute('aria-expanded'), 'true');
  assert.strictEqual(p.movil.hidden, false);
  despachar(p.burger, 'click');
  assert.strictEqual(p.burger.getAttribute('aria-expanded'), 'false');
  assert.strictEqual(p.movil.hidden, true);
});

test('Escape cierra el menú móvil y regresa el foco al burger', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.burger, 'click');
  p.doc.activeElement = p.movil;
  despachar(p.movil, 'keydown', { key: 'Escape' });
  assert.strictEqual(p.movil.hidden, true);
  assert.strictEqual(p.burger.getAttribute('aria-expanded'), 'false');
  assert.strictEqual(p.doc.activeElement, p.burger);
});

test('un clic abre un panel y cierra el otro; clic afuera cierra todo', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.exp1, 'click');
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'true');
  despachar(p.exp2, 'click');
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
  assert.strictEqual(p.exp2.getAttribute('aria-expanded'), 'true');
  despachar(p.afuera, 'click');
  assert.strictEqual(p.exp2.getAttribute('aria-expanded'), 'false');
});

test('Escape cierra el panel de escritorio y regresa el foco a su botón', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.exp1, 'click');
  p.doc.activeElement = p.enlace1;
  despachar(p.enlace1, 'keydown', { key: 'Escape' });
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
  assert.strictEqual(p.doc.activeElement, p.exp1);
});

test('hover con mouse abre con retraso, mantiene aria en sincronía y Escape lo cierra', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.item1, 'pointerenter', { pointerType: 'mouse' });
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
  p.correrRelojes();
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'true');
  despachar(p.item1, 'keydown', { key: 'Escape' });
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
});

test('salir con el mouse cierra un panel abierto por hover, no uno abierto por clic', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.item1, 'pointerenter', { pointerType: 'mouse' });
  p.correrRelojes();
  despachar(p.exp1, 'click');
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'true', 'el clic sobre un panel abierto por hover lo fija');
  despachar(p.item1, 'pointerleave', { pointerType: 'mouse' });
  p.correrRelojes();
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'true');
  despachar(p.item2, 'pointerenter', { pointerType: 'mouse' });
  p.correrRelojes();
  despachar(p.item2, 'pointerleave', { pointerType: 'mouse' });
  p.correrRelojes();
  assert.strictEqual(p.exp2.getAttribute('aria-expanded'), 'false');
});

test('el tacto no abre por hover', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.item1, 'pointerenter', { pointerType: 'touch' });
  p.correrRelojes();
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
});

test('el foco que sale del item cierra su panel', () => {
  const p = armarPagina();
  menu(p.doc, p.win);
  despachar(p.exp1, 'click');
  despachar(p.enlace1, 'focusout', { relatedTarget: p.exp1 });
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'true');
  despachar(p.enlace1, 'focusout', { relatedTarget: p.exp2 });
  assert.strictEqual(p.exp1.getAttribute('aria-expanded'), 'false');
});

test('la barra se oculta e inerte mientras cualquier CTA del hero se ve', () => {
  const p = armarPagina();
  let avisar = null;
  const observados = [];
  p.win.IntersectionObserver = class { constructor(fn) { avisar = fn; } observe(el) { observados.push(el); } };
  barra(p.doc, p.win);
  assert.deepStrictEqual(observados, [p.hero, p.hero2]);
  avisar([{ target: p.hero, isIntersecting: true }, { target: p.hero2, isIntersecting: true }]);
  assert.ok(p.bar.classList.contains('is-oculta'));
  assert.strictEqual(p.bar.inert, true);
  avisar([{ target: p.hero, isIntersecting: false }]);
  assert.ok(p.bar.classList.contains('is-oculta'), 'sigue oculta: el otro CTA aún se ve');
  avisar([{ target: p.hero2, isIntersecting: false }]);
  assert.ok(!p.bar.classList.contains('is-oculta'));
  assert.strictEqual(p.bar.inert, false);
});

test('el selector de hero cubre los CTAs que marca shell.py y el hero viejo de la home', () => {
  for (const parte of ['[data-hero-cta]', '.svc-hero__ctas', '.vt-hero__ctas', '[data-cta$=":hero"]']) {
    assert.ok(HERO_CTA.split(',').map((x) => x.trim()).includes(parte), parte);
  }
});

test('eventoWhatsapp arma el mismo generate_lead que un clic, con prefijo de la página', () => {
  const ctx = { tipo: 'servicio-pasto', servicio: 'pasto-natural' };
  assert.deepStrictEqual(eventoWhatsapp('calculadora', ctx, { label: 'pasto_calc_wa_solo', cta_id: 'x', method: 'y' }), {
    nombre: 'generate_lead',
    params: { label: 'pasto_calc_wa_solo', method: 'whatsapp', cta_id: 'servicio-pasto:calculadora', service: 'pasto-natural' },
  });
  assert.strictEqual(eventoWhatsapp('home:hero', ctx).params.cta_id, 'home:hero');
  assert.strictEqual(eventoWhatsapp(undefined, ctx).params.cta_id, 'servicio-pasto:js');
});

test('VTMedicion.whatsapp manda el evento con el contexto del header', () => {
  const p = armarPagina();
  const ev = medicion(p.doc, p.win).whatsapp('cta-final', { label: 'pasto_cta_final' });
  assert.deepStrictEqual(p.enviados, [['event', 'generate_lead',
    { label: 'pasto_cta_final', method: 'whatsapp', cta_id: 'servicio:cta-final', service: 'pasto-natural' }]]);
  assert.strictEqual(ev.nombre, 'generate_lead');
});

test('VTMedicion.whatsapp no falla sin gtag ni con un documento roto', () => {
  const p = armarPagina();
  delete p.win.gtag;
  assert.strictEqual(medicion(p.doc, p.win).whatsapp('calculadora').params.cta_id, 'servicio:calculadora');
  const roto = { querySelector() { throw new Error('x'); } };
  assert.strictEqual(medicion(roto, p.win).whatsapp('calculadora'), null);
});

test('clic medio (auxclick) y clic con modificador miden sin impedir la navegación', () => {
  const p = armarPagina();
  medir(p.doc, p.win);
  const medio = despachar(p.wa, 'auxclick', { button: 1 });
  assert.strictEqual(medio.defaultPrevented, false);
  assert.ok(p.wa.getAttribute('href').includes(encodeURIComponent('Vengo de viverosterra.com')));
  despachar(p.tel, 'click', { button: 0, ctrlKey: true });
  despachar(p.tel, 'auxclick', { button: 2 });
  assert.deepStrictEqual(p.enviados.map((e) => e[1]), ['generate_lead', 'click_to_call']);
});

const { firmarAperturas } = require('../terra.js');

test('window.open de WhatsApp sale firmado una sola vez; lo demás no se toca', () => {
  const abiertos = [];
  const win = { open: (url, destino, rasgos) => { abiertos.push([url, destino, rasgos]); return 'ventana'; } };
  firmarAperturas(win);
  firmarAperturas(win);
  assert.strictEqual(win.open('https://wa.me/528333268008?text=Hola', '_blank', 'noopener'), 'ventana');
  win.open('https://wa.me/528333268008?text=' + encodeURIComponent('Hola\n\n' + FIRMA), '_blank');
  win.open('/precios');
  win.open(new URL('https://wa.me/528333268008?text=Pasto'));
  assert.deepStrictEqual(abiertos[0], ['https://wa.me/528333268008?text=' + encodeURIComponent('Hola\n\n' + FIRMA), '_blank', 'noopener']);
  assert.strictEqual(abiertos[1][0].split('viverosterra.com').length, 2, 'no se firma dos veces');
  assert.strictEqual(abiertos[2][0], '/precios');
  assert.strictEqual(abiertos[3][0], 'https://wa.me/528333268008?text=' + encodeURIComponent('Pasto\n\n' + FIRMA));
});

test('firmarAperturas no falla si window.open no existe', () => {
  const win = {};
  firmarAperturas(win);
  assert.strictEqual(win.open, undefined);
});

test('un enlace al catálogo manda select_content con el tipo de la página', () => {
  const ctx = { tipo: 'plantas', servicio: 'plantas' };
  const params = { content_type: 'catalogo', item_id: 'catalogo', cta_id: 'plantas:catalogo', service: 'plantas' };
  for (const href of ['/catalogo', '/catalogo.html', '/catalogo#palmas']) {
    assert.deepStrictEqual(evento(enlace({ href }), ctx), { nombre: 'select_content', params }, href);
  }
  assert.strictEqual(evento(enlace({ href: '/catalogos-viejos' }), ctx), null);
});

test('las tablas plegables se abren desde 768 px y siguen cerradas en celular', () => {
  const { plegables } = require('../terra.js');
  const crear = () => [{ open: false }, { open: false }];
  const doc = (ds) => ({ querySelectorAll: (sel) => (sel === 'details[data-vt-plegable]' ? ds : []) });
  const ancho = (px) => ({ matchMedia: (q) => ({ matches: q === '(min-width: 768px)' && px >= 768 }) });
  const escritorio = crear();
  plegables(doc(escritorio), ancho(1024));
  assert.deepStrictEqual(escritorio.map((d) => d.open), [true, true]);
  const celular = crear();
  plegables(doc(celular), ancho(375));
  assert.deepStrictEqual(celular.map((d) => d.open), [false, false]);
  const sinMatchMedia = crear();
  plegables(doc(sinMatchMedia), {});
  assert.deepStrictEqual(sinMatchMedia.map((d) => d.open), [false, false]);
});

test('abierto: cada caso de casos-horario.json (bordes de viernes y sábado, domingo, festivos y cambio de día en UTC)', () => {
  for (const caso of HORARIO.casos) {
    assert.strictEqual(abierto(new Date(caso.instante), HORARIO.horario, HORARIO.festivos), caso.abierto, caso.nota);
  }
});

test('abierto usa el día y la hora de México, no los de UTC ni los de la máquina', () => {
  // 2026-11-14T02:00Z es viernes 13 a las 20:00 en México (en UTC ya es sábado).
  const instante = new Date('2026-11-14T02:00:00Z');
  assert.strictEqual(abierto(instante, '5@09:00-23:00', ''), true);
  assert.strictEqual(abierto(instante, '6@00:00-23:59', ''), false);
  // 2026-12-26T02:00Z sigue siendo 25 de diciembre en México: festivo aunque el horario lo cubra.
  const navidad = new Date('2026-12-26T02:00:00Z');
  assert.strictEqual(abierto(navidad, '5,6@00:00-23:59', '12-25,01-01'), false);
  assert.strictEqual(abierto(navidad, '5,6@00:00-23:59', ''), true);
});

test('abierto es falso sin horario, con horario ilegible o con una fecha inválida', () => {
  const lunes = new Date('2026-11-16T16:00:00Z');
  assert.strictEqual(abierto(lunes, '', ''), false);
  assert.strictEqual(abierto(lunes, null, null), false);
  assert.strictEqual(abierto(lunes, 'lunes a viernes', ''), false);
  assert.strictEqual(abierto(new Date('no es fecha'), HORARIO.horario, HORARIO.festivos), false);
});

test('el horario y los festivos no viven en terra.js: llegan de los data-* del HTML', () => {
  const fuente = fs.readFileSync(path.join(__dirname, '..', 'terra.js'), 'utf8');
  assert.doesNotMatch(fuente, /\d{2}:\d{2}-\d{2}:\d{2}|['"]\d{2}-\d{2}['"]/);
  assert.match(fuente, /data-vt-horario/);
  assert.match(fuente, /data-vt-festivos/);
  assert.match(fuente, /America\/Mexico_City/);
});

function paginaConPromesa() {
  const promesa = 'Respondemos en menos de 1 hora en horario · Lun a vie 9 a 18 h, sáb 9 a 14 h';
  const crear = (tag) => ({ tag, hijos: [], atributos: {}, clases: new Set(), textContent: '',
    setAttribute(n, v) { this.atributos[n] = String(v); },
    getAttribute(n) { return n in this.atributos ? this.atributos[n] : null; },
    hasAttribute(n) { return n in this.atributos; },
    get firstChild() { return this.hijos[0] || null; },
    insertBefore(nuevo, ref) { const i = ref ? this.hijos.indexOf(ref) : this.hijos.length; this.hijos.splice(i, 0, nuevo); nuevo.padre = this; return nuevo; },
    get nextSibling() { return this.padre.hijos[this.padre.hijos.indexOf(this) + 1] || null; },
    removeChild(hijo) { this.hijos.splice(this.hijos.indexOf(hijo), 1); return hijo; },
    get texto() { return this.hijos.length ? this.hijos.map((h) => h.texto).join('') : this.textContent; },
  });
  const texto = (t) => { const n = crear('#text'); n.textContent = t; return n; };
  const el = crear('span');
  el.atributos = { 'data-vt-horario': HORARIO.horario, 'data-vt-festivos': HORARIO.festivos };
  el.classList = { toggle: (c, si) => (si ? el.clases.add(c) : el.clases.delete(c)) };
  el.insertBefore(texto(promesa), null);
  const doc = { createElement: crear, createTextNode: texto, querySelectorAll: (s) => (s === '[data-vt-horario]' ? [el] : []) };
  return { doc, el, promesa };
}

test('en horario antepone "Abierto ahora · " a la promesa, una sola vez, y la marca con is-abierto', () => {
  const p = paginaConPromesa();
  const lunes = new Date('2026-11-16T16:00:00Z');
  horario(p.doc, lunes);
  horario(p.doc, lunes);
  assert.strictEqual(ABIERTO, 'Abierto ahora');
  assert.strictEqual(p.el.texto, 'Abierto ahora · ' + p.promesa);
  assert.ok(p.el.clases.has('is-abierto'), 'el punto verde va con el texto, nunca solo');
  assert.strictEqual(p.el.getAttribute('aria-live'), null);
});

test('fuera de horario el texto queda exactamente igual; al cerrar se retira el prefijo', () => {
  const p = paginaConPromesa();
  horario(p.doc, new Date('2026-11-15T18:00:00Z'));
  assert.strictEqual(p.el.texto, p.promesa);
  assert.strictEqual(p.el.hijos.length, 1);
  assert.ok(!p.el.clases.has('is-abierto'));
  horario(p.doc, new Date('2026-11-13T23:59:00Z'));
  assert.strictEqual(p.el.texto, 'Abierto ahora · ' + p.promesa);
  horario(p.doc, new Date('2026-11-14T00:00:00Z'));
  assert.strictEqual(p.el.texto, p.promesa);
  assert.ok(!p.el.clases.has('is-abierto'));
});

// ---------- Entrega 2: días de preventa en el banner y select_content de la home ----------
const { diasHasta, textoPreventa, preventa } = require('../terra.js');

test('diasHasta cuenta días de calendario con la fecha de México, no la de UTC', () => {
  assert.strictEqual(diasHasta(new Date('2026-11-09T18:00:00Z'), '2026-11-30'), 21);
  assert.strictEqual(diasHasta(new Date('2026-11-29T18:00:00Z'), '2026-11-30'), 1);
  assert.strictEqual(diasHasta(new Date('2026-11-30T18:00:00Z'), '2026-11-30'), 0);
  // 2026-12-01T03:00Z todavía es 30 de noviembre a las 21:00 en México: sigue siendo el último día.
  assert.strictEqual(diasHasta(new Date('2026-12-01T03:00:00Z'), '2026-11-30'), 0);
  assert.strictEqual(diasHasta(new Date('2026-12-01T06:00:00Z'), '2026-11-30'), -1);
  assert.strictEqual(diasHasta(new Date('2026-12-28T18:00:00Z'), '2027-01-02'), 5);
  for (const malo of ['', null, '30/11/2026', '2026-13-40x']) assert.strictEqual(diasHasta(new Date('2026-11-09T18:00:00Z'), malo), null);
  assert.strictEqual(diasHasta(new Date('no es fecha'), '2026-11-30'), null);
});

test('diasHasta con la fecha del build: reloj atrasado no cuenta y nunca hay más días que del build a la fecha', () => {
  assert.strictEqual(diasHasta(new Date('2026-11-09T18:00:00Z'), '2026-11-30', '2026-11-09'), 21);
  assert.strictEqual(diasHasta(new Date('2026-11-08T18:00:00Z'), '2026-11-30', '2026-11-09'), null);
  assert.strictEqual(diasHasta(new Date('2025-11-25T18:00:00Z'), '2026-11-30', '2026-11-09'), null);
  assert.strictEqual(diasHasta(new Date('2026-11-25T18:00:00Z'), '2026-11-30', '2026-11-09'), 5);
  assert.strictEqual(diasHasta(new Date('2026-12-02T18:00:00Z'), '2026-11-30', '2026-11-09'), -2);
  // Un build ilegible no bloquea: se cuenta como sin fecha de build.
  assert.strictEqual(diasHasta(new Date('2026-11-25T18:00:00Z'), '2026-11-30', 'ayer'), 5);
});

test('textoPreventa: faltan N días, falta 1 día, último día y nada después', () => {
  // Sin el " · " inicial: en escritorio lo pone el CSS; en celular la frase sustituye al renglón de precios.
  assert.strictEqual(textoPreventa(21), 'Preventa: faltan 21 días');
  assert.strictEqual(textoPreventa(2), 'Preventa: faltan 2 días');
  assert.strictEqual(textoPreventa(1), 'Preventa: falta 1 día');
  assert.strictEqual(textoPreventa(0), 'Último día de preventa');
  assert.strictEqual(textoPreventa(-1), '');
  for (const raro of [null, undefined, NaN, 2.5, '3', Infinity]) assert.strictEqual(textoPreventa(raro), '', String(raro));
});

test('preventa escribe el texto en cada [data-vt-hasta]; la fecha llega del HTML, no de terra.js', () => {
  const span = { textContent: '', getAttribute: (n) => ({ 'data-vt-hasta': '2026-11-30', 'data-vt-build': '2026-11-09' }[n] || null) };
  const doc = { querySelectorAll: (s) => (s === '[data-vt-hasta]' ? [span] : []) };
  preventa(doc, new Date('2026-11-09T18:00:00Z'));
  assert.strictEqual(span.textContent, 'Preventa: faltan 21 días');
  // Reloj del cliente atrasado (antes de la fecha del build): no se muestra nada.
  preventa(doc, new Date('2026-10-01T18:00:00Z'));
  assert.strictEqual(span.textContent, '');
  preventa(doc, new Date('2026-11-20T18:00:00Z'));
  assert.strictEqual(span.textContent, 'Preventa: faltan 10 días');
  preventa(doc, new Date('2026-12-05T18:00:00Z'));
  assert.strictEqual(span.textContent, '');
  const fuente = fs.readFileSync(path.join(__dirname, '..', 'terra.js'), 'utf8');
  assert.doesNotMatch(fuente, /20\d\d-\d\d-\d\d/);
});

test('el banner de Nochebuenas y "Calcula tu patio" mandan select_content con su item_id', () => {
  const ctx = { tipo: 'home', servicio: 'general' };
  assert.deepStrictEqual(evento(enlace({ href: '/post/nochebuenas-tampico-madero-mayoreo', 'data-cta': 'home:banner-nochebuenas' }), ctx),
    { nombre: 'select_content', params: { content_type: 'cta', item_id: 'home:banner-nochebuenas', cta_id: 'home:banner-nochebuenas' } });
  assert.deepStrictEqual(evento(enlace({ href: '#medidor', 'data-cta': 'home:hero', id: 'vt-calcula-patio' }), ctx),
    { nombre: 'select_content', params: { content_type: 'cta', item_id: 'vt-calcula-patio', cta_id: 'home:hero' } });
  // Solo esos dos enlaces: otra ancla con data-cta, una sin él o un enlace interno cualquiera no se miden.
  assert.strictEqual(evento(enlace({ href: '#medidor', 'data-cta': 'home:hero' }), ctx), null);
  assert.strictEqual(evento(enlace({ href: '#cotizador', 'data-cta': 'tienda:hero', id: 'otro' }), ctx), null);
  assert.strictEqual(evento(enlace({ href: '#precios' }), ctx), null);
  assert.strictEqual(evento(enlace({ href: '/precios', 'data-cta': 'home:otro' }), ctx), null);
});

test('generate_lead y click_to_call no cambian con la medición nueva', () => {
  const ctx = { tipo: 'home', servicio: 'general' };
  assert.deepStrictEqual(evento(enlace({ href: 'https://wa.me/528333268008?text=Hola', 'data-cta': 'home:hero' }), ctx),
    { nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: 'home:hero', service: 'general' } });
  assert.deepStrictEqual(evento(enlace({ href: 'tel:+528333268008', 'data-cta': 'home:hero' }), ctx),
    { nombre: 'click_to_call', params: { link_type: 'tel', cta_id: 'home:hero', service: 'general' } });
});

test('el clic en el banner manda el evento, no toca el enlace y no falla si gtag no existe', () => {
  const p = armarPagina();
  const banner = new p.afuera.constructor(p.doc, { tag: 'a', atributos: { href: '/post/nochebuenas-tampico-madero-mayoreo', 'data-cta': 'home:banner-nochebuenas' }, padre: p.afuera });
  medir(p.doc, p.win);
  const e = despachar(banner, 'click');
  assert.strictEqual(e.defaultPrevented, false);
  assert.strictEqual(banner.getAttribute('href'), '/post/nochebuenas-tampico-madero-mayoreo');
  assert.deepStrictEqual(p.enviados[p.enviados.length - 1], ['event', 'select_content', { content_type: 'cta', item_id: 'home:banner-nochebuenas', cta_id: 'home:banner-nochebuenas' }]);
  const sin = armarPagina();
  delete sin.win.gtag;
  const otro = new sin.afuera.constructor(sin.doc, { tag: 'a', atributos: { href: '#medidor', 'data-cta': 'home:hero', id: 'vt-calcula-patio' }, padre: sin.afuera });
  medir(sin.doc, sin.win);
  assert.doesNotThrow(() => despachar(otro, 'click'));
});

// ---------- Correcciones de revisión: Intl sin hourCycle, reloj atrasado y recálculo cada minuto ----------
function intlFalso(partes) {
  return { DateTimeFormat: function () { this.formatToParts = () => Object.entries(partes).map(([type, value]) => ({ type, value })); } };
}

test('abierto no afirma nada si Intl devuelve reloj de 12 horas o una hora fuera de 0-23; "24" es medianoche', () => {
  const lunes = new Date('2026-11-16T16:00:00Z');
  const base = { weekday: 'Mon', year: '2026', month: '11', day: '16', minute: '00' };
  const todoElDia = '1@00:00-23:59';
  assert.strictEqual(abierto(lunes, todoElDia, '', intlFalso({ ...base, hour: '10' })), true);
  assert.strictEqual(abierto(lunes, todoElDia, '', intlFalso({ ...base, hour: '10', dayPeriod: 'AM' })), false);
  assert.strictEqual(abierto(lunes, todoElDia, '', intlFalso({ ...base, hour: '25' })), false);
  assert.strictEqual(abierto(lunes, todoElDia, '', intlFalso({ ...base, hour: 'x' })), false);
  assert.strictEqual(abierto(lunes, '1@00:00-00:30', '', intlFalso({ ...base, hour: '24' })), true);
  assert.strictEqual(abierto(lunes, '1@09:00-18:00', '', intlFalso({ ...base, hour: '24' })), false);
  const fuente = fs.readFileSync(path.join(__dirname, '..', 'terra.js'), 'utf8');
  assert.match(fuente, /hour12: false/);
});

test('con el reloj del cliente antes de la fecha del build no se muestra "Abierto ahora"', () => {
  const p = paginaConPromesa();
  p.el.atributos['data-vt-build'] = '2026-11-09';
  horario(p.doc, new Date('2026-11-02T16:00:00Z'));  // lunes 10:00, pero una semana antes del build
  assert.strictEqual(p.el.texto, p.promesa);
  assert.ok(!p.el.clases.has('is-abierto'));
  horario(p.doc, new Date('2026-11-09T16:00:00Z'));
  assert.strictEqual(p.el.texto, 'Abierto ahora · ' + p.promesa);
});

test('reloj: recalcula cada 60 s solo con la página visible y al volver a la pestaña', () => {
  const { reloj } = require('../terra.js');
  let veces = 0;
  const oyentes = {};
  const doc = { hidden: false, addEventListener: (t, fn) => { oyentes[t] = fn; } };
  const intervalos = [];
  const win = { setInterval: (fn, ms) => { intervalos.push({ fn, ms }); return 1; } };
  reloj(doc, win, () => { veces += 1; });
  assert.strictEqual(intervalos.length, 1);
  assert.strictEqual(intervalos[0].ms, 60000);
  intervalos[0].fn();
  assert.strictEqual(veces, 1);
  doc.hidden = true;
  intervalos[0].fn();
  oyentes.visibilitychange();
  assert.strictEqual(veces, 1, 'oculta: no recalcula');
  doc.hidden = false;
  oyentes.visibilitychange();
  assert.strictEqual(veces, 2);
});

// ---------- préstamo de la barra fija y del encabezado (Entrega B de experiencia) ----------
const { prestamos, prestamoVigente } = require('../terra.js');

function nodo(atributos, texto) {
  const el = {
    atributos: { ...atributos },
    getAttribute(n) { return n in this.atributos ? this.atributos[n] : null; },
    setAttribute(n, v) { this.atributos[n] = String(v); },
    textContent: texto || '',
  };
  return el;
}

function paginaConBarra() {
  const rotulo = { nodeType: 3, nodeValue: 'Cotizar por WhatsApp' };
  const go = nodo({ href: 'https://wa.me/1?text=generico', 'data-cta': 'servicio-pasto:barra' });
  go.lastChild = rotulo;
  const largo = nodo({}, 'Cotizar por WhatsApp');
  const corto = nodo({}, 'Cotizar');
  const cabeza = nodo({ href: 'https://wa.me/1?text=generico', 'data-cta': 'servicio-pasto:header' });
  cabeza.querySelector = (s) => (s === '.vt-head__cta-largo' ? largo : s === '.vt-head__cta-corto' ? corto : null);
  const doc = { querySelector: (s) => (s === '[data-vt-bar] .vt-bar__go' ? go : s === '.vt-head__cta' ? cabeza : null) };
  return { doc, go, rotulo, cabeza, largo, corto };
}

test('prestamoVigente: el último préstamo con enlace; sin préstamos, null', () => {
  assert.strictEqual(prestamoVigente([]), null);
  assert.deepStrictEqual(prestamoVigente([{ clave: 'a', href: 'x' }, { clave: 'b', href: 'y' }]), { clave: 'b', href: 'y' });
  assert.deepStrictEqual(prestamoVigente([{ clave: 'a', href: 'x' }, { clave: 'b', href: '' }]), { clave: 'a', href: 'x' });
});

test('una calculadora presta su enlace y su texto a la barra y al encabezado, y al soltar vuelven los del HTML', () => {
  const p = paginaConBarra();
  const b = prestamos(p.doc);
  b.prestar('medidor', 'https://wa.me/1?text=medida', 'Enviar mi medida', 'Enviar');
  assert.strictEqual(p.go.getAttribute('href'), 'https://wa.me/1?text=medida');
  assert.strictEqual(p.rotulo.nodeValue, 'Enviar mi medida');
  assert.strictEqual(p.cabeza.getAttribute('href'), 'https://wa.me/1?text=medida');
  assert.strictEqual(p.largo.textContent, 'Enviar mi medida');
  assert.strictEqual(p.corto.textContent, 'Enviar');
  // El data-cta no cambia: el clic se sigue midiendo como <tipo>:barra y <tipo>:header.
  assert.strictEqual(p.go.getAttribute('data-cta'), 'servicio-pasto:barra');
  assert.strictEqual(p.cabeza.getAttribute('data-cta'), 'servicio-pasto:header');
  b.soltar('medidor');
  assert.strictEqual(p.go.getAttribute('href'), 'https://wa.me/1?text=generico');
  assert.strictEqual(p.rotulo.nodeValue, 'Cotizar por WhatsApp');
  assert.strictEqual(p.largo.textContent, 'Cotizar por WhatsApp');
  assert.strictEqual(p.corto.textContent, 'Cotizar');
});

test('con dos préstamos manda el último; soltarlo devuelve el anterior; un enlace vacío equivale a soltar', () => {
  const p = paginaConBarra();
  const b = prestamos(p.doc);
  b.prestar('medidor', 'https://wa.me/1?text=medida', 'Enviar mi medida');
  b.prestar('simulador', 'https://wa.me/1?text=plan', 'Enviar mi plan de pago');
  assert.strictEqual(p.rotulo.nodeValue, 'Enviar mi plan de pago');
  assert.strictEqual(p.corto.textContent, 'Enviar', 'sin corto, el encabezado del celular dice "Enviar" (cabe a 320 px)');
  b.prestar('medidor', 'https://wa.me/1?text=medida2', 'Enviar mi medida');
  assert.strictEqual(p.go.getAttribute('href'), 'https://wa.me/1?text=medida2', 'el que cambió al último manda');
  b.prestar('medidor', '', 'Enviar mi medida');
  assert.strictEqual(p.go.getAttribute('href'), 'https://wa.me/1?text=plan');
  b.soltar('simulador');
  assert.strictEqual(p.go.getAttribute('href'), 'https://wa.me/1?text=generico');
});

test('un préstamo sin texto cambia solo el enlace y deja los textos del HTML', () => {
  const p = paginaConBarra();
  const b = prestamos(p.doc);
  b.prestar('tienda', 'https://wa.me/1?text=estado');
  assert.strictEqual(p.cabeza.getAttribute('href'), 'https://wa.me/1?text=estado');
  assert.strictEqual(p.rotulo.nodeValue, 'Cotizar por WhatsApp');
  assert.strictEqual(p.largo.textContent, 'Cotizar por WhatsApp');
  assert.strictEqual(p.corto.textContent, 'Cotizar');
});

test('sin barra ni encabezado (páginas sin shell completo) prestar y soltar no fallan', () => {
  const b = prestamos({ querySelector: () => null });
  b.prestar('x', 'https://wa.me/1', 'Enviar');
  b.soltar('x');
});
