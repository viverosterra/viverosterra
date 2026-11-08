// public/js/vt-b2b.js
/* Cotizadores de las páginas para empresas (Etapa 2d). Mismo cálculo y mismos textos que tools/site/componentes.py
   (paridad en tests/casos-b2b.json); los precios no viven aquí:
   - [data-vt-volumen]: m² totales de la obra → precio por volumen con VTMedidor.calcular (vt-medidor.js): mayoreo desde
     el mínimo y, con menos, solo pasto con su aviso. Los modos y precios llegan en data-modos, escritos desde datos.py.
   - [data-vt-palmas]: especie, altura y cantidad por renglón (hasta 8) → un solo mensaje con toda la lista.
   Los botones son enlaces de WhatsApp con data-cta: terra.js los mide (generate_lead) y los firma al hacer clic. Sin JS, el
   botón manda la plantilla de compras de la página (data-mensaje). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const M2_MAXIMO = 1000000;
  const ALTURA_MAXIMA = 40;
  const CANTIDAD_MAXIMA = 100000;
  const FILAS_MAXIMAS = 8;

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const formatoM2 = (x) => x.toLocaleString('es-MX', { maximumFractionDigits: 1 });
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;
  const hueco = (v) => String(v == null ? '' : v).trim() || '___';

  // "1,200" y "1200" son 1200; "12,5" es 12.5; "800 m²" es 800. 0 si no es un número mayor que 0 y hasta M2_MAXIMO.
  function leerM2(texto) {
    let t = String(texto == null ? '' : texto).replace(/\s|m²|m2/gi, '');
    t = /^\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(t) ? t.replace(/,/g, '') : t.replace(',', '.');
    if (!/^\d+(?:\.\d+)?$/.test(t)) return 0;
    const n = Number(t);
    return n > 0 && n <= M2_MAXIMO ? n : 0;
  }

  function textosVolumen(r, campos) {
    const desde = r.desde ? 'desde ' : '';
    const m2 = formatoM2(r.m2);
    const mensaje = [`Hola, quiero cotizar ${r.texto} para un proyecto.`, `m² totales: ${m2} m²`,
      `Estimado de la web: ${desde}${dinero(r.total)} con IVA (${desde}$${r.precio}/m²)`,
      `Empresa: ${hueco(campos.empresa)}`, `Obra y ubicación: ${hueco(campos.obra)}`,
      `Fecha de la primera entrega: ${hueco(campos.fecha)}`].join('\n');
    return { medida: `${m2} m²`, monto: dinero(r.total),
      calc: `${m2} m² × ${desde}$${r.precio}/m², con IVA. Solo pasto: la entrega por etapas y la instalación se cotizan con tu obra.`,
      mensaje };
  }

  function leerAltura(texto) {
    const m = /^\s*(\d+(?:[.,]\d+)?)/.exec(String(texto == null ? '' : texto));
    const n = m ? Math.round(Number(m[1].replace(',', '.')) * 10) / 10 : 0;
    return n > 0 && n <= ALTURA_MAXIMA ? n : 0;
  }

  function leerCantidad(texto) {
    const m = /^\s*(\d+)/.exec(String(texto == null ? '' : texto));
    const n = m ? Number(m[1]) : 0;
    return n > 0 && n <= CANTIDAD_MAXIMA ? n : 0;
  }

  // fila: [especie, altura, cantidad] tal como los escribió el visitante.
  function lineaPalma(fila) {
    const especie = String(fila[0] == null ? '' : fila[0]).trim();
    if (!especie) return '';
    const n = leerCantidad(fila[2]);
    const alto = leerAltura(fila[1]);
    return `- ${n || '___'} × ${especie}, altura aprox.: ${alto ? formatoM2(alto) + ' m' : '___'}`;
  }

  function mensajePalmas(filas, campos) {
    const lineas = filas.map(lineaPalma).filter(Boolean);
    if (!lineas.length) return '';
    return ['Hola, quiero cotizar palmas para un proyecto.', ...lineas, `Empresa: ${hueco(campos.empresa)}`,
      `Obra y ubicación: ${hueco(campos.obra)}`, `Fecha de entrega: ${hueco(campos.fecha)}`].join('\n');
  }

  function resumenPalmas(filas) {
    const conEspecie = filas.filter((f) => String(f[0] == null ? '' : f[0]).trim());
    if (!conEspecie.length) return 'Elige especie y cantidad';
    const n = conEspecie.length;
    const piezas = conEspecie.reduce((suma, f) => suma + leerCantidad(f[2]), 0);
    const especies = `${n} ${n === 1 ? 'especie' : 'especies'}`;
    return piezas ? `${especies} · ${piezas.toLocaleString('es-MX')} piezas` : `${especies} · cantidad por definir`;
  }

  function camposObra(caja) {
    const valor = (n) => caja.querySelector(`[data-vt-campo="${n}"]`).value;
    return { empresa: valor('empresa'), obra: valor('obra'), fecha: valor('fecha') };
  }

  function iniciarVolumen(caja, calcular) {
    const modos = JSON.parse(caja.dataset.modos);
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    const vacio = { medida: salida('m2').textContent, monto: salida('monto').textContent, calc: salida('calc').textContent };
    function actualizar() {
      const m2 = leerM2(caja.querySelector('[data-vt-campo="m2"]').value);
      const precio = salida('monto').parentElement;
      if (!m2) {
        salida('m2').textContent = vacio.medida;
        salida('rotulo').textContent = modos.mayoreo.rotulo;
        salida('monto').textContent = vacio.monto;
        precio.classList.add('is-vacio');
        salida('calc').textContent = vacio.calc;
        salida('aviso').textContent = '';
        salida('aviso').hidden = true;
        salida('cta').setAttribute('href', enlace(caja.dataset.wa, caja.dataset.mensaje));
        return;
      }
      const r = calcular(m2, 1, 'mayoreo', modos);
      const t = textosVolumen(r, camposObra(caja));
      salida('m2').textContent = t.medida;
      salida('rotulo').textContent = r.rotulo;
      salida('monto').textContent = t.monto;
      precio.classList.remove('is-vacio');
      salida('calc').textContent = t.calc;
      salida('aviso').textContent = r.aviso;
      salida('aviso').hidden = !r.aviso;
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    actualizar();
  }

  function iniciarPalmas(caja) {
    const lista = caja.querySelector('[data-vt-filas]');
    const agregar = caja.querySelector('[data-vt-agregar]');
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    function filas() {
      return Array.from(lista.querySelectorAll('[data-vt-fila]')).map((f) =>
        ['especie', 'altura', 'cantidad'].map((n) => f.querySelector(`[data-vt-campo="${n}"]`).value));
    }
    function actualizar() {
      const f = filas();
      const mensaje = mensajePalmas(f, camposObra(caja));
      salida('resumen').textContent = resumenPalmas(f);
      salida('lista').textContent = f.map(lineaPalma).filter(Boolean).join('\n');
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, mensaje || caja.dataset.mensaje));
    }
    // Copia del último renglón, vacía y con ids nuevos (cada label sigue apuntando a su control).
    function otraFila() {
      const renglones = lista.querySelectorAll('[data-vt-fila]');
      const nueva = renglones[renglones.length - 1].cloneNode(true);
      const n = renglones.length + 1;
      nueva.querySelectorAll('[id]').forEach((el) => { el.id = el.id.replace(/\d+$/, String(n)); });
      nueva.querySelectorAll('label[for]').forEach((el) => { el.htmlFor = el.htmlFor.replace(/\d+$/, String(n)); });
      nueva.querySelectorAll('input, select').forEach((el) => { el.value = ''; });
      lista.appendChild(nueva);
      agregar.hidden = n >= FILAS_MAXIMAS;
      nueva.querySelector('select').focus();
    }
    agregar.hidden = false;
    agregar.addEventListener('click', otraFila);
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { leerM2, textosVolumen, leerAltura, leerCantidad, lineaPalma, mensajePalmas, resumenPalmas, enlace };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTB2B = Object.freeze(api);
  const arrancar = () => {
    if (root.VTMedidor) document.querySelectorAll('[data-vt-volumen]').forEach((c) => iniciarVolumen(c, root.VTMedidor.calcular));
    document.querySelectorAll('[data-vt-palmas]').forEach(iniciarPalmas);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
