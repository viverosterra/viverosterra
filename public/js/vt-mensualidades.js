// public/js/vt-mensualidades.js
/* Precio en mensualidades con tarjeta de crédito. Misma fórmula que tools/pasto/mensualidades.py:
   la tasa del plazo se suma a la base y el IVA va sobre ambas. Sin DOM. */
(function (root) {
  'use strict';
  const TASA_BASE = 0.036;
  const IVA = 0.16;
  const TASAS = Object.freeze({ 3: 0.0457, 6: 0.0757, 9: 0.1107, 12: 0.1277 });
  const PLAZOS = Object.freeze([3, 6, 9, 12]);
  const UMBRALES = Object.freeze([[15000, [3, 6, 9, 12]], [5000, [3, 6]], [2000, [3]]]);

  function plazosDisponibles(contado) {
    const u = UMBRALES.find(([minimo]) => contado >= minimo);
    return u ? u[1].slice() : [];
  }

  function totalAPlazos(contado, plazo) {
    return Math.ceil(contado / (1 - (TASA_BASE + TASAS[plazo]) * (1 + IVA)));
  }

  function planes(contado) {
    const disp = plazosDisponibles(contado);
    return PLAZOS.map((plazo) => {
      const total = totalAPlazos(contado, plazo);
      return { plazo, total, mensualidad: Math.round(total / plazo),
        diferencia: total - Math.ceil(contado), disponible: disp.includes(plazo) };
    });
  }

  function minimoDe(plazo) {
    return Math.min(...UMBRALES.filter(([, ps]) => ps.includes(plazo)).map(([m]) => m));
  }

  const api = { TASA_BASE, IVA, TASAS, PLAZOS, UMBRALES, plazosDisponibles, totalAPlazos, planes, minimoDe };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VTMensualidades = Object.freeze(api);
})(typeof window !== 'undefined' ? window : globalThis);
