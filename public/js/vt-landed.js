// public/js/vt-landed.js
/* Precio puesto en casa por estado. Puro: sin DOM. Se usa en el navegador (window.VTLanded) y en Node (pruebas). */
(function (root) {
  'use strict';
  const ROLLO_M2 = 50;

  function landedM2(precioRollo, estado, estadoZona, zonas) {
    const zona = estadoZona[estado];
    if (!zona || !(zona in zonas)) return null;
    return Math.round(precioRollo + zonas[zona] / ROLLO_M2);
  }

  function slugEstado(estado) {
    return estado.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().trim().split(/\s+/).join('-');
  }

  function estadoDesdeSlug(slug, estados) {
    return estados.find((e) => slugEstado(e) === slug) || null;
  }

  const api = { landedM2, slugEstado, estadoDesdeSlug };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VTLanded = Object.freeze(api);
})(typeof window !== 'undefined' ? window : globalThis);
