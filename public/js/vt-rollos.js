// public/js/vt-rollos.js
/* ¿Cuántos rollos necesito? Calculadora de /pasto-sintetico/cuantos-rollos (Entrega B del SEO nacional, 2026-11-16).
   corte() es puro (navegador y Node) y hace lo mismo que tools/pasto/rollos.py: tiras de 2 m en el mismo sentido, se
   pide lo mayor entre las tiras y el área + 10%, envío por rollo de 50 m². Casos compartidos: tests/casos-rollos.json.
   En la página pasa los m² al cotizador (#m2) de tienda-pasto.js, que pone precio, flete, folio y WhatsApp. */
(function (root) {
  'use strict';
  const ROLLO_M2 = 50;
  const ROLLO_ANCHO_M = 2;
  const ROLLO_LARGO_M = ROLLO_M2 / ROLLO_ANCHO_M;
  const MARGEN = 0.10;
  const MAX_M2 = 5000;
  const EPS = 1e-9;

  const r2 = (v) => Math.round((v + Number.EPSILON) * 100) / 100;

  function numero(v) {
    if (typeof v === 'number') return v;
    if (typeof v !== 'string' || v.trim() === '') return NaN;
    return Number(v.trim().replace(',', '.'));
  }

  function tiras(aLoLargoDe, cruzado) {
    const n = Math.ceil(cruzado / ROLLO_ANCHO_M - EPS);
    return { n, m2: r2(n * ROLLO_ANCHO_M * aLoLargoDe), largoTira: aLoLargoDe, cruzado };
  }

  function corte(largoIn, anchoIn) {
    const largo = numero(largoIn);
    const ancho = numero(anchoIn);
    if (!Number.isFinite(largo) || !Number.isFinite(ancho) || largo <= 0 || ancho <= 0 || largo * ancho > MAX_M2) {
      return null;
    }
    const a = tiras(largo, ancho);
    const b = tiras(ancho, largo);
    const o = (b.m2 < a.m2 || (b.m2 === a.m2 && b.n < a.n)) ? b : a;
    const area = r2(largo * ancho);
    const m2SinMargen = Math.ceil(o.m2 - EPS);
    const m2 = Math.ceil(Math.max(o.m2, area * (1 + MARGEN)) - EPS);
    return {
      area, tiras: o.n, largoTira: r2(o.largoTira), cruzado: r2(o.cruzado), m2Tiras: o.m2, m2,
      rollos: Math.ceil(m2 / ROLLO_M2), m2SinMargen, rollosSinMargen: Math.ceil(m2SinMargen / ROLLO_M2),
      sobrante: r2(m2 - area), uniones: o.n - 1, tiraConUnion: o.largoTira > ROLLO_LARGO_M,
    };
  }

  const api = { corte, ROLLO_LARGO_M, ROLLO_ANCHO_M };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTRollos = Object.freeze(api);

  /* ---------- página ---------- */
  const SVG = 'http://www.w3.org/2000/svg';
  const fmt = (n) => n.toLocaleString('es-MX', { maximumFractionDigits: 2 });
  const plural = (n, uno, varios) => `${fmt(n)} ${n === 1 ? uno : varios}`;

  function rect(x, y, w, h, clase) {
    const el = document.createElementNS(SVG, 'rect');
    [['x', x], ['y', y], ['width', w], ['height', h], ['class', clase]].forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  }

  /* Croquis: las tiras a lo largo, el contorno del espacio encima; lo que sobra de la última tira va más claro. */
  function dibujar(svg, r) {
    const ancho = 320;
    const alto = 180;
    const total = r.tiras * ROLLO_ANCHO_M;
    const s = Math.min((ancho - 8) / r.largoTira, (alto - 8) / total);
    const g = document.createElementNS(SVG, 'g');
    g.setAttribute('transform', `translate(${Math.round((ancho - r.largoTira * s) * 50) / 100} 4) scale(${s})`);
    for (let i = 0; i < r.tiras; i += 1) {
      const y = i * ROLLO_ANCHO_M;
      const dentro = Math.min(ROLLO_ANCHO_M, r.cruzado - y);
      g.append(rect(0, y, r.largoTira, dentro, `vt-rollos__tira vt-rollos__tira--${i % 2}`));
      if (dentro < ROLLO_ANCHO_M) g.append(rect(0, y + dentro, r.largoTira, ROLLO_ANCHO_M - dentro, 'vt-rollos__sobra'));
    }
    g.append(rect(0, 0, r.largoTira, r.cruzado, 'vt-rollos__espacio'));
    svg.setAttribute('viewBox', `0 0 ${ancho} ${Math.ceil(total * s + 8)}`);
    svg.replaceChildren(g);
  }

  function pintar(form, r) {
    const campo = (k) => form.querySelector(`[data-r="${k}"]`);
    const nota = form.querySelector('[data-r-nota]');
    const plano = form.querySelector('[data-r-plano]');
    form.dataset.valido = String(Boolean(r));
    if (!r) {
      ['area', 'm2', 'tiras', 'rollos', 'sobrante'].forEach((k) => { campo(k).textContent = '—'; });
      nota.textContent = 'Escribe el largo y el ancho en metros (hasta 5,000 m²).';
      plano.replaceChildren();
      return;
    }
    campo('area').textContent = `${fmt(r.area)} m²`;
    campo('m2').textContent = `${fmt(r.m2)} m²`;
    campo('tiras').textContent = `${plural(r.tiras, 'tira', 'tiras')} de ${fmt(r.largoTira)} m`;
    campo('rollos').textContent = plural(r.rollos, 'rollo', 'rollos');
    campo('sobrante').textContent = `${fmt(r.sobrante)} m²`;
    const avisos = [];
    if (r.rollos > r.rollosSinMargen) {
      avisos.push(`El margen de 10% te pasa a ${plural(r.rollos, 'rollo', 'rollos')} de envío: si cortas con cuidado, `
        + `${fmt(r.m2SinMargen)} m² caben en ${plural(r.rollosSinMargen, 'rollo', 'rollos')}.`);
    }
    if (r.tiraConUnion) avisos.push(`Cada tira mide más de ${ROLLO_LARGO_M} m, el largo del rollo: lleva una unión a lo ancho.`);
    if (r.m2 < 25) avisos.push('Para envío el mínimo es 25 m²; abajo de eso, se recoge en el showroom de Cd. Madero.');
    nota.textContent = avisos.join(' ');
    dibujar(plano, r);
  }

  function alCotizador(m2) {
    const inp = document.getElementById('m2');
    if (!inp) return;
    inp.value = String(m2);
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new Event('change', { bubbles: true }));
  }

  let iniciado = false;
  function init() {
    const form = document.getElementById('r-calc');
    if (!form || iniciado) return;
    iniciado = true;
    const largo = form.querySelector('#r-largo');
    const ancho = form.querySelector('#r-ancho');
    let ultimo = null;
    const calcular = () => {
      ultimo = corte(largo.value, ancho.value);
      pintar(form, ultimo);
      if (ultimo) alCotizador(ultimo.m2);
      if (ultimo && root.VTPreguntas) root.VTPreguntas.recordar({ m2: ultimo.m2 });
    };
    [largo, ancho].forEach((el) => el.addEventListener('input', calcular));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      calcular();
      if (!ultimo) return;
      const destino = document.getElementById('comprar');
      if (!destino) return;
      const quieto = root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches;
      destino.scrollIntoView({ behavior: quieto ? 'auto' : 'smooth', block: 'start' });
      const estado = document.getElementById('estado');
      if (estado) estado.focus({ preventScroll: true });
      if (typeof root.gtag === 'function') root.gtag('event', 'calcular_rollos', { value: ultimo.m2 });
    });
    calcular();
  }

  /* El cotizador de tienda-pasto.js avisa con vt:ready; si ya avisó o no está, se calcula igual. */
  if (root.VTTienda) init();
  else {
    document.addEventListener('vt:ready', init, { once: true });
    document.addEventListener('DOMContentLoaded', () => { if (!root.VTTienda) init(); }, { once: true });
  }
})(typeof window !== 'undefined' ? window : globalThis);
