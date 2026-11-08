// public/js/vt-cuestionario.js
/* Cuestionario de diseño (Etapa 2i): el asistente de 5 pasos de main y su envío a formsubmit por fetch (el action /ajax/
   responde JSON), con el mismo aviso en la misma página al terminar. Dos arreglos: no se avanza con los datos obligatorios
   vacíos (antes el navegador bloqueaba el envío al final, en un paso oculto) y Enter a medio camino avanza en vez de enviar. */
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
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    if (pasto <= 0 && jardinera <= 0) return;
    const suma = Math.round(pasto + jardinera);
    $('area-display').hidden = false;
    $('area-total-val').textContent = `${suma} m²`;
    $('area_total_input').value = suma;
  }
  $('area_pasto').addEventListener('input', calcularTotal);
  $('area_jard').addEventListener('input', calcularTotal);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (actual < total) { ir(1); return; }
    enviar.textContent = 'Enviando...';
    enviar.disabled = true;
    const fallo = () => { enviar.textContent = 'Error — intenta de nuevo'; enviar.disabled = false; };
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      const datos = res.ok ? await res.json().catch(() => ({})) : {};
      if (res.ok && String(datos.success) !== 'false') {
        form.hidden = true;
        document.querySelector('.vt-wizard').hidden = true;
        $('prog').style.transform = 'scaleX(1)';
        const ok = $('success-screen');
        ok.hidden = false;
        ok.querySelector('h2').focus();
      } else {
        fallo();
      }
    } catch (error) {
      fallo();
    }
  });

  pintar();
})();
