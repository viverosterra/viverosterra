// public/js/vt-cuestionario.js
/* Cuestionario de diseño (Etapa 2i): el asistente de 5 pasos de main, enviado y medido como los otros 6 formularios. Dos
   arreglos: no se avanza con los datos obligatorios vacíos (antes el navegador bloqueaba el envío al final, en un paso
   oculto) y Enter a medio camino avanza en vez de enviar. */
(function () {
  'use strict';
  const form = document.getElementById('mainForm');
  if (!form) return;
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
    enviar.textContent = 'Enviar cuestionario';
    enviar.disabled = false;
  });

  pintar();
})();
