/* Viveros Terra · vt-preguntas.js · preguntas rápidas antes de WhatsApp (spec del primer mensaje de WhatsApp).
   Puro (node --test): armarMensaje, preguntasVisibles, respuestasIniciales, leerVisita, recordar.
   Navegador: lee #vt-preguntas (JSON de tools/site/preguntas_wa.py), intercepta los botones de cotizar y abre un
   <dialog> con las preguntas; el enlace final lo toca el cliente (sin window.open). Sin <dialog> o sin el JSON, los
   botones funcionan como siempre. Memoria de la visita: sessionStorage (modelo y m²); el estado elegido en la tienda
   se lee de su propio store (vt-cotizacion-v1). Nunca guarda nombre ni teléfono. */
(function (root) {
  'use strict';
  const CLAVE = 'vt-visita-v1';
  const MAX_M2 = 5000;
  const SLUG = /^[a-z0-9-]+$/;
  const RANGOS = { '<25': 'menos de 25 m²', '25-50': 'entre 25 y 50 m²', '50-100': 'entre 50 y 100 m²', '>100': 'más de 100 m²' };

  const m2Valido = (v) => Number.isInteger(v) && v > 0 && v <= MAX_M2;

  function leerVisita(storage) {
    try {
      const v = JSON.parse((storage && storage.getItem(CLAVE)) || '{}') || {};
      const salida = {};
      if (typeof v.modelo === 'string' && SLUG.test(v.modelo)) salida.modelo = v.modelo;
      if (m2Valido(v.m2)) salida.m2 = v.m2;
      return salida;
    } catch (err) {
      return {};
    }
  }

  function recordar(storage, cambios) {
    const nuevo = { ...leerVisita(storage) };
    if (typeof cambios.modelo === 'string' && SLUG.test(cambios.modelo)) nuevo.modelo = cambios.modelo;
    if (m2Valido(cambios.m2)) nuevo.m2 = cambios.m2;
    try {
      storage.setItem(CLAVE, JSON.stringify(nuevo));
    } catch (err) {
      // Modo privado o almacenamiento bloqueado: solo no se recuerda.
    }
    return nuevo;
  }

  function preguntasVisibles(conjunto, ctx) {
    const fijo = (ctx && ctx.fijo) || {};
    return conjunto.preguntas.filter((q) => !(q.clave === 'modelo' && fijo.modelo) && !(q.clave === 'destino' && fijo.estado));
  }

  function respuestasIniciales(conjunto, ctx) {
    const fijo = ctx.fijo || {};
    const rec = ctx.recordado || {};
    const r = {};
    if (!fijo.modelo && rec.modelo && ctx.modelos && ctx.modelos[rec.modelo]) r.modelo = rec.modelo;
    if (rec.m2) r.m2 = 'exacto';
    if (!fijo.estado && rec.estado) {
      r.destino = 'envio';
      r.estado = rec.estado;
    }
    return r;
  }

  function destinoTexto(r, fijo) {
    if (fijo.estado) {
      const lugar = fijo.ciudad && fijo.ciudad !== fijo.estado ? `${fijo.ciudad} (${fijo.estado})` : fijo.estado;
      return { texto: `con envío a ${lugar}`, entrega: fijo.estado };
    }
    if (r.destino === 'recoger') return { texto: 'para recoger en el vivero de Cd. Madero', entrega: 'showroom' };
    if (r.destino === 'local') return { texto: 'instalado en Tampico, Madero o Altamira', entrega: 'local' };
    if (r.destino === 'envio' && r.estado) return { texto: `con envío a ${r.estado}`, entrega: r.estado };
    return null;
  }

  function armarMensaje(conjunto, r, ctx) {
    const fijo = ctx.fijo || {};
    const rec = ctx.recordado || {};
    const modelo = r.modelo || fijo.modelo || '';
    const nombre = modelo && modelo !== 'no-se' ? (ctx.modelos || {})[modelo] || '' : '';
    const partes = [];
    const m2 = r.m2 === 'exacto' && rec.m2 ? rec.m2 : 0;
    if (m2) partes.push(`unos ${m2} m²`);
    else if (RANGOS[r.m2]) partes.push(RANGOS[r.m2]);
    const destino = destinoTexto(r, fijo);
    if (destino) partes.push(destino.texto);
    let texto = `Hola, quiero cotizar pasto sintético${nombre ? ' ' + nombre : ''}${partes.length ? ', ' + partes.join(', ') : ''}.`;
    if (modelo === 'no-se') texto += '\nQuiero que me recomienden el modelo.';
    if (nombre && m2 && destino && typeof ctx.folio === 'function') {
      const f = ctx.folio([{ slug: modelo, m2 }], destino.entrega);
      if (f) texto += `\nFolio web: ${f}`;
    }
    return texto;
  }

  const api = { CLAVE, leerVisita, recordar, preguntasVisibles, respuestasIniciales, armarMensaje };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  const sesion = (() => {
    try {
      return root.sessionStorage;
    } catch (err) {
      return null;
    }
  })();
  root.VTPreguntas = Object.freeze({ ...api, recordar: (cambios) => recordar(sesion, cambios) });

  const doc = root.document;
  const datosPagina = (() => {
    try {
      return JSON.parse((doc.getElementById('vt-preguntas') || {}).textContent || 'null');
    } catch (err) {
      return null;
    }
  })();
  if (!datosPagina || !root.HTMLDialogElement || !root.HTMLDialogElement.prototype.showModal) return;

  const FIRMA = 'Vengo de viverosterra.com';
  const modelos = Object.fromEntries(datosPagina.conjunto.preguntas[0].opciones || []);
  const textoDe = (href) => {
    try { return new URL(href).searchParams.get('text') || ''; } catch (err) { return ''; }
  };
  const numeroDe = (href) => {
    try { return new URL(href).pathname.replace(/\D/g, ''); } catch (err) { return ''; }
  };
  const enlace = (numero, texto) => `https://wa.me/${numero}?text=${encodeURIComponent(texto + '\n\n' + FIRMA)}`;

  function estadoTienda() {
    try {
      return (JSON.parse(root.localStorage.getItem('vt-cotizacion-v1') || '{}') || {}).estado || '';
    } catch (err) {
      return '';
    }
  }

  // Los botones de cotizar de la página; no el encabezado, el pie, la lista de la tienda ni un mensaje que ya trae
  // la cotización o la lista del cliente.
  function interceptable(a, e) {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button > 0) return false;
    if (a.closest('header, footer, dialog') || a.id === 'cot-send' || a.hasAttribute('data-vt-sin-preguntas')) return false;
    return !/Folio web:|Mi lista/i.test(textoDe(a.href));
  }

  let panel = null;
  function crearPanel() {
    panel = doc.createElement('dialog');
    panel.className = 'vt-wa-panel';
    panel.setAttribute('aria-labelledby', 'vt-wa-titulo');
    panel.innerHTML = '<div class="vt-wa-panel__caja"><div class="vt-wa-panel__cab"><h2 id="vt-wa-titulo"></h2>'
      + '<button type="button" class="vt-wa-panel__cerrar" aria-label="Cerrar">×</button></div>'
      + '<div class="vt-wa-panel__preguntas"></div><p class="vt-wa-panel__rotulo">El mensaje que se va a enviar</p>'
      + '<p class="vt-wa-panel__vista" aria-live="polite"></p>'
      + '<a class="vt-btn vt-btn--wa vt-wa-panel__abrir" data-cta-wa target="_blank" rel="noopener">Abrir WhatsApp</a>'
      + '<a class="vt-wa-panel__corto" data-cta-wa target="_blank" rel="noopener">Solo quiero contactarlos</a></div>';
    doc.body.appendChild(panel);
    panel.querySelector('.vt-wa-panel__cerrar').addEventListener('click', () => panel.close());
    panel.addEventListener('click', (e) => { if (e.target === panel) panel.close(); });
    return panel;
  }

  function grupo(q, r, ctx, pintar) {
    const fs = doc.createElement('fieldset');
    const lg = doc.createElement('legend');
    lg.textContent = q.texto;
    fs.appendChild(lg);
    const opciones = q.clave === 'm2' && ctx.recordado.m2 ? [['exacto', `Unos ${ctx.recordado.m2} m²`], ...q.opciones] : q.opciones;
    opciones.forEach(([v, t]) => {
      const b = doc.createElement('button');
      b.type = 'button';
      b.dataset.q = q.clave;
      b.dataset.v = v;
      b.textContent = t;
      b.addEventListener('click', () => { r[q.clave] = r[q.clave] === v ? '' : v; pintar(); });
      fs.appendChild(b);
    });
    if (q.clave === 'destino') {
      const sel = doc.createElement('select');
      sel.setAttribute('aria-label', 'Estado');
      const vacio = doc.createElement('option');
      vacio.value = '';
      vacio.textContent = 'Elige tu estado';
      sel.appendChild(vacio);
      datosPagina.conjunto.estados.forEach((e) => {
        const o = doc.createElement('option');
        o.value = e;
        o.textContent = e;
        sel.appendChild(o);
      });
      sel.addEventListener('change', () => { r.estado = sel.value; pintar(); });
      fs.appendChild(sel);
    }
    return fs;
  }

  function abrir(original) {
    const p = panel || crearPanel();
    const conjunto = datosPagina.conjunto;
    const estado = estadoTienda();
    const ctx = { fijo: datosPagina.fijo || {}, modelos, folio: root.VTFolio ? root.VTFolio.folio : null,
                  recordado: { ...leerVisita(sesion), ...(estado ? { estado } : {}) } };
    const r = respuestasIniciales(conjunto, ctx);
    const numero = numeroDe(original.href);
    const cta = original.getAttribute('data-cta') || 'pagina:wa';
    const vista = p.querySelector('.vt-wa-panel__vista');
    const abrirWa = p.querySelector('.vt-wa-panel__abrir');
    const corto = p.querySelector('.vt-wa-panel__corto');
    const caja = p.querySelector('.vt-wa-panel__preguntas');
    p.querySelector('#vt-wa-titulo').textContent = conjunto.titulo;
    caja.textContent = '';
    const pintar = () => {
      const texto = armarMensaje(conjunto, r, ctx);
      vista.textContent = texto;
      abrirWa.href = enlace(numero, texto);
      caja.querySelectorAll('[data-v]').forEach((b) => b.setAttribute('aria-pressed', String(r[b.dataset.q] === b.dataset.v)));
      const sel = caja.querySelector('select');
      if (sel) {
        sel.hidden = r.destino !== 'envio';
        sel.value = r.estado || '';
      }
    };
    preguntasVisibles(conjunto, ctx).forEach((q) => caja.appendChild(grupo(q, r, ctx, pintar)));
    corto.href = enlace(numero, datosPagina.corto);
    const al = (tipo) => () => {
      const respondidas = Object.keys(r).some((k) => r[k]);
      const valor = tipo === 'corto' ? 'solo-contacto' : (respondidas ? 'respondidas' : 'omitidas');
      if (root.VTMedicion) root.VTMedicion.whatsapp(`${cta}:panel`, { preguntas: valor });
      p.close();
    };
    abrirWa.onclick = al('abrir');
    corto.onclick = al('corto');
    p.onclose = () => { if (original.isConnected) original.focus(); };
    pintar();
    p.showModal();
  }

  root.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('a[href^="https://wa.me/"]') : null;
    if (!a || !interceptable(a, e)) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    abrir(a);
  }, true);
})(typeof window !== 'undefined' ? window : globalThis);
