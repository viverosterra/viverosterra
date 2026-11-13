// public/js/vt-folio.js
/* Folio web de la tienda de pasto: lo escribe tienda-pasto.js al final del WhatsApp ("Folio web: T28-40-NL") y lo lee
   el cotizador de Netlify (este mismo archivo va incrustado allá) para llenar entrega, m² y 3 modelos.
   Puro: sin DOM. Navegador (window.VTFolio) y Node (pruebas). */
(function (root) {
  'use strict';

  const ESTADOS = Object.freeze({
    'Aguascalientes': 'AGS', 'Baja California': 'BC', 'Baja California Sur': 'BCS', 'Campeche': 'CAMP',
    'CDMX': 'CDMX', 'Chiapas': 'CHIS', 'Chihuahua': 'CHIH', 'Coahuila': 'COAH', 'Colima': 'COL', 'Durango': 'DGO',
    'Estado de México': 'MEX', 'Guanajuato': 'GTO', 'Guerrero': 'GRO', 'Hidalgo': 'HGO', 'Jalisco': 'JAL',
    'Michoacán': 'MICH', 'Morelos': 'MOR', 'Nayarit': 'NAY', 'Nuevo León': 'NL', 'Oaxaca': 'OAX', 'Puebla': 'PUE',
    'Querétaro': 'QRO', 'Quintana Roo': 'QROO', 'San Luis Potosí': 'SLP', 'Sinaloa': 'SIN', 'Sonora': 'SON',
    'Tabasco': 'TAB', 'Tamaulipas': 'TAMS', 'Tlaxcala': 'TLAX', 'Veracruz': 'VER', 'Yucatán': 'YUC',
    'Zacatecas': 'ZAC',
  });
  // Entregas sin estado: mismos valores que usan la web y el cotizador.
  const ESPECIALES = Object.freeze({ showroom: 'REC', local: 'LOC' });
  const POR_CODIGO = Object.freeze(Object.fromEntries(
    Object.entries({ ...ESTADOS, ...ESPECIALES }).map(([nombre, cod]) => [cod, nombre])));
  const RE_FOLIO = /folio web:\s*([A-Za-z0-9+-]+)/i;
  const RE_PARTE = /^([A-Z]\d{2})-(\d{1,4})$/;
  const MAX_MODELOS = 3;

  /* "toscana-28" o "toscana28" → "T28". */
  function codigoModelo(clave) {
    const altura = String(clave || '').match(/(\d+)$/);
    return altura ? String(clave)[0].toUpperCase() + altura[1] : '';
  }

  /* items: [{slug, m2}] · entrega: nombre del estado, "showroom", "local" o "". */
  function folio(items, entrega) {
    const partes = (items || [])
      .filter((it) => codigoModelo(it.slug) && Number.isInteger(it.m2) && it.m2 > 0)
      .map((it) => `${codigoModelo(it.slug)}-${it.m2}`);
    if (!partes.length) return '';
    const sufijo = ESTADOS[entrega] || ESPECIALES[entrega] || '';
    return partes.join('+') + (sufijo ? `-${sufijo}` : '');
  }

  /* Texto pegado (el WhatsApp completo) → { items: [{codigo, m2}], entrega } o null si no hay folio legible. */
  function leerFolio(texto) {
    const hallado = RE_FOLIO.exec(String(texto || ''));
    if (!hallado) return null;
    const partes = hallado[1].toUpperCase().split('+');
    let entrega = '';
    const ultima = partes[partes.length - 1].split('-');
    if (ultima.length === 3) {
      entrega = POR_CODIGO[ultima[2]];
      if (!entrega) return null;
      partes[partes.length - 1] = ultima.slice(0, 2).join('-');
    }
    const items = [];
    for (const parte of partes) {
      const p = RE_PARTE.exec(parte);
      if (!p || Number(p[2]) <= 0) return null;
      items.push({ codigo: p[1], m2: Number(p[2]) });
    }
    return { items, entrega };
  }

  /* codigos: ["T28", ...] · modelos: [{k, rollo}] del cotizador → 3 claves (k).
     Uno: él y sus vecinos de precio. Dos: se agrega el más cercano en precio. Tres o más: los tres primeros. */
  function completarModelos(codigos, modelos) {
    const orden = modelos.map((m, i) => ({ ...m, i })).sort((a, b) => a.rollo - b.rollo || a.i - b.i);
    const elegidos = [];
    (codigos || []).forEach((c) => {
      const m = orden.find((x) => codigoModelo(x.k) === c);
      if (m && !elegidos.includes(m) && elegidos.length < MAX_MODELOS) elegidos.push(m);
    });
    if (!elegidos.length) return [];
    if (elegidos.length === 1) {
      const pos = orden.indexOf(elegidos[0]);
      const desde = Math.max(0, Math.min(pos - 1, orden.length - MAX_MODELOS));
      return orden.slice(desde, desde + MAX_MODELOS).map((m) => m.k);
    }
    const resto = orden.filter((m) => !elegidos.includes(m));
    while (elegidos.length < MAX_MODELOS && resto.length) {
      const dist = (m) => Math.min(...elegidos.map((e) => Math.abs(e.rollo - m.rollo)));
      const cercano = resto.reduce((a, b) => (dist(b) < dist(a) ? b : a));
      elegidos.push(cercano);
      resto.splice(resto.indexOf(cercano), 1);
    }
    return elegidos.map((m) => m.k);
  }

  const api = { ESTADOS, codigoModelo, folio, leerFolio, completarModelos };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VTFolio = Object.freeze(api);
})(typeof window !== 'undefined' ? window : globalThis);
