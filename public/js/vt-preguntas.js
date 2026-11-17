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
  /* PANEL */
})(typeof window !== 'undefined' ? window : globalThis);
