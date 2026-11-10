// public/js/vt-cuestionario.js
/* Cuestionario de diseño (Etapa 2i): el asistente de 5 pasos de main, enviado y medido como los otros 6 formularios. Dos
   arreglos: no se avanza con los datos obligatorios vacíos (antes el navegador bloqueaba el envío al final, en un paso
   oculto) y Enter a medio camino avanza en vez de enviar. Desde la Entrega B de experiencia, las respuestas se guardan en
   sessionStorage mientras se escriben (solo en este navegador y esta pestaña; no se manda nada a ningún lado) y vuelven
   al recargar; el borrador se borra al enviar. Las funciones puras del borrador se exportan para node --test. */
(function (root) {
  'use strict';
  const CLAVE = 'vt-cuestionario-borrador';
  const MAX_TEXTO = 2000;
  // Los campos del cliente: nunca los ocultos del envío (_subject, _next…) ni la trampa _honey.
  const propio = (c) => Boolean(c.name) && c.name[0] !== '_' && c.type !== 'hidden' && c.type !== 'submit';

  // {name: valor} de texto, listas y opciones; las casillas guardan la lista de valores marcados.
  function capturar(campos) {
    const datos = {};
    campos.filter(propio).forEach((c) => {
      if (c.type === 'checkbox') {
        datos[c.name] = (datos[c.name] || []).concat(c.checked ? [c.value] : []);
      } else if (c.type === 'radio') {
        if (c.checked) datos[c.name] = c.value;
      } else if (c.value) {
        datos[c.name] = String(c.value).slice(0, MAX_TEXTO);
      }
    });
    return datos;
  }

  // Lo guardado no es de fiar: solo texto corto o listas de texto, y solo en campos que existen.
  function aplicar(campos, datos) {
    if (!datos || typeof datos !== 'object') return 0;
    let puestos = 0;
    campos.filter(propio).forEach((c) => {
      if (!Object.prototype.hasOwnProperty.call(datos, c.name)) return;
      const v = datos[c.name];
      if (c.type === 'checkbox') {
        if (Array.isArray(v)) { c.checked = v.includes(c.value); puestos += c.checked ? 1 : 0; }
      } else if (c.type === 'radio') {
        if (typeof v === 'string') { c.checked = c.value === v; puestos += c.checked ? 1 : 0; }
      } else if (typeof v === 'string' && v.length <= MAX_TEXTO) {
        c.value = v;
        puestos += 1;
      }
    });
    return puestos;
  }

  function leer(storage) {
    try {
      return JSON.parse((storage && storage.getItem(CLAVE)) || 'null');
    } catch (error) {
      return null;
    }
  }

  // storage puede faltar o lanzar (modo privado, cuota llena): el cuestionario sigue funcionando sin borrador.
  function guardar(storage, datos) {
    try {
      storage.setItem(CLAVE, JSON.stringify(datos));
      return true;
    } catch (error) {
      return false;
    }
  }

  function borrar(storage) {
    try { storage.removeItem(CLAVE); } catch (error) { /* sin almacenamiento no hay borrador que borrar */ }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CLAVE, capturar, aplicar, leer, guardar, borrar };
    return;
  }

  const form = document.getElementById('mainForm');
  if (!form) return;
  let almacen = null;
  try { almacen = root.sessionStorage; } catch (error) { almacen = null; }
  const $ = (id) => document.getElementById(id);
  const pasos = Array.from(form.querySelectorAll('[data-vt-paso]'));
  const total = pasos.length;
  const marcas = Array.from(document.querySelectorAll('[data-vt-marca]'));
  const anterior = $('btn-prev');
  const siguiente = $('btn-next');
  const enviar = $('submit-btn');
  const cuenta = $('step-counter');
  let actual = 1;

  const asistente = document.querySelector('.vt-wizard');
  const HOLGURA = 16; // la misma separación bajo el menú que scroll-margin-top en terra-util.css

  function subirAlAsistente() {
    const menu = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--vt-head-h')) || 0;
    const top = asistente.getBoundingClientRect().top + window.scrollY - menu - HOLGURA;
    const calma = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: Math.max(0, top), behavior: calma ? 'auto' : 'smooth' });
  }

  function pintar() {
    pasos.forEach((p, i) => { p.hidden = i + 1 !== actual; });
    marcas.forEach((m, i) => {
      m.classList.toggle('is-hecho', i + 1 < actual);
      if (i + 1 === actual) m.setAttribute('aria-current', 'step'); else m.removeAttribute('aria-current');
    });
    $('prog').style.transform = `scaleX(${actual / total})`;
    anterior.hidden = actual === 1;
    siguiente.hidden = actual === total;
    enviar.hidden = actual !== total;
    cuenta.textContent = `Paso ${actual} de ${total}`;
  }

  function pasoValido() {
    return Array.from(pasos[actual - 1].querySelectorAll('input,select,textarea')).every((c) => c.reportValidity());
  }

  function ir(delta) {
    const destino = actual + delta;
    if (destino < 1 || destino > total || (delta > 0 && !pasoValido())) return;
    actual = destino;
    pintar();
    subirAlAsistente();
    pasos[actual - 1].querySelector('h2').focus({ preventScroll: true });
  }

  anterior.addEventListener('click', () => ir(-1));
  siguiente.addEventListener('click', () => ir(1));

  // Riego: la pregunta extra aparece con "No" o "Parcial".
  form.querySelectorAll('.riego-trigger').forEach((r) => r.addEventListener('change', () => { $('cond-riego').hidden = false; }));
  const conRiego = form.querySelector('input[name="riego_instalado"][value="Sí"]');
  if (conRiego) conRiego.addEventListener('change', () => { $('cond-riego').hidden = true; });
  // Tipo de espacio "Otro": campo libre.
  form.querySelectorAll('input[name="tipo_espacio"]').forEach((r) => r.addEventListener('change', () => {
    $('otro-esp-wrap').hidden = !$('rb-otro-esp').checked;
  }));

  function calcularTotal() {
    const pasto = parseFloat($('area_pasto').value) || 0;
    const jardinera = parseFloat($('area_jard').value) || 0;
    if (pasto <= 0 && jardinera <= 0) {
      $('area-display').hidden = true;
      $('area-total-val').textContent = '0 m²';
      $('area_total_input').value = '';
      return;
    }
    const suma = Math.round(pasto + jardinera);
    $('area-display').hidden = false;
    $('area-total-val').textContent = `${suma} m²`;
    $('area_total_input').value = suma;
  }
  $('area_pasto').addEventListener('input', calcularTotal);
  $('area_jard').addEventListener('input', calcularTotal);

  // Borrador: se recupera al cargar (con sus condicionales y la suma de áreas) y se guarda en cada cambio.
  const campos = () => Array.from(form.elements);
  if (almacen && aplicar(campos(), leer(almacen))) {
    form.querySelectorAll('input[type="radio"]:checked').forEach((r) => r.dispatchEvent(new Event('change')));
    calcularTotal();
  }
  const anotar = () => { if (almacen) guardar(almacen, capturar(campos())); };
  form.addEventListener('input', anotar);
  form.addEventListener('change', anotar);

  // Como los otros 6 formularios (vt-b2b.js): el navegador hace el POST, formsubmit lleva a /gracias con _next y aquí
  // solo se manda generate_lead con method "formulario".
  let enviando = false;
  form.addEventListener('submit', (e) => {
    if (actual < total || enviando) {
      e.preventDefault();
      if (!enviando) ir(1);
      return;
    }
    enviando = true;
    if (almacen) borrar(almacen);
    enviar.textContent = 'Enviando...';
    enviar.disabled = true;
    const head = document.querySelector('.vt-head');
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'generate_lead', { method: 'formulario', cta_id: form.dataset.ctaForm,
        service: (head && head.dataset.vtServicio) || 'jardin' });
    }
  });
  // Al volver desde /gracias con el botón Atrás, el formulario se puede enviar otra vez.
  window.addEventListener('pageshow', () => {
    enviando = false;
    enviar.textContent = 'Enviar mis respuestas';
    enviar.disabled = false;
  });

  pintar();
})(typeof window !== 'undefined' ? window : globalThis);
