// public/js/tests/terra.test.js
const test = require('node:test');
const assert = require('node:assert');
const { FIRMA, HERO_CTA, tipoEnlace, conFirma, evento, eventoWhatsapp } = require('../terra.js');

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
