// public/js/vt-simulador.js
/* Simulador de mensualidades para servicios (monto de una cotización). Depende de vt-mensualidades.js.
   Las filas se crean una sola vez y solo se actualizan: así el foco del teclado no se pierde al cambiar de plan. */
(function () {
  'use strict';
  const WA = '528333268008';
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');

  function buildRow(plazo) {
    const label = document.createElement('label');
    label.className = 'sim-plan';
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'sim-plan';
    radio.value = String(plazo);
    const name = document.createElement('span');
    name.className = 'sim-plan__name';
    name.textContent = plazo ? `${plazo} mensualidades` : 'Contado';
    const amt = document.createElement('span');
    amt.className = 'sim-plan__amt num';
    label.append(radio, name, amt);
    return { plazo, label, radio, amt };
  }

  // [texto principal, detalle]: el principal va en negritas
  function amountParts(M, p) {
    if (!p.disponible) return ['', p.plazo && M ? `Desde ${money(M.minimoDe(p.plazo))}` : ''];
    if (!p.plazo) return [money(p.total), ''];
    return [`≈ ${money(p.mensualidad)} al mes`, `total ${money(p.total)} (+${money(p.diferencia)})`];
  }

  function paintAmount(el, parts) {
    el.textContent = '';
    if (parts[0]) {
      const strong = document.createElement('strong');
      strong.textContent = parts[0];
      el.appendChild(strong);
    }
    if (!parts[1]) return;
    if (parts[0]) {
      const sep = document.createElement('span');
      sep.className = 'sim-plan__sep';
      sep.textContent = ' · ';
      el.appendChild(sep);
    }
    const more = document.createElement('span');
    more.className = 'sim-plan__more';
    more.textContent = parts[1];
    el.appendChild(more);
  }

  function init(root) {
    const M = window.VTMensualidades;
    const input = root.querySelector('[data-sim-monto]');
    const list = root.querySelector('[data-sim-list]');
    const wa = root.querySelector('[data-sim-wa]');
    if (!input || !list || !wa) return;
    const servicio = root.dataset.servicio || 'un servicio';
    const plazos = [0].concat(M ? Array.from(M.PLAZOS) : []);
    const filas = plazos.map(buildRow);
    list.textContent = '';
    filas.forEach((f) => list.appendChild(f.label));
    let plan = 0;

    function paint() {
      const contado = Math.max(0, Math.round(Number(input.value) || 0));
      const planes = M && contado > 0 ? M.planes(contado) : [];
      const datos = [{ plazo: 0, total: contado, disponible: contado > 0 }].concat(
        plazos.slice(1).map((plazo) => planes.find((p) => p.plazo === plazo) || { plazo, disponible: false }));
      if (!datos.some((p) => p.plazo === plan && p.disponible)) plan = 0;
      datos.forEach((p, i) => {
        const f = filas[i];
        f.radio.disabled = !p.disponible;
        f.radio.checked = p.disponible && p.plazo === plan;
        f.label.classList.toggle('is-selected', f.radio.checked);
        f.label.classList.toggle('is-disabled', !p.disponible);
        paintAmount(f.amt, amountParts(M, p));
      });
      const elegido = planes.find((p) => p.plazo === plan && p.disponible);
      const pago = !contado ? ''
        : elegido ? `Me interesa pagar en ${elegido.plazo} mensualidades con tarjeta de crédito (total ${money(elegido.total)}).`
          : 'Pagaría de contado.';
      const msg = [`Hola, quiero cotizar ${servicio}.`, contado ? `Mi cotización es de ${money(contado)}.` : '', pago]
        .filter(Boolean).join('\n');
      wa.href = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
    }

    filas.forEach((f) => f.radio.addEventListener('change', () => {
      if (f.radio.checked) { plan = f.plazo; paint(); }
    }));
    input.addEventListener('input', paint);
    paint();
  }

  function start() { document.querySelectorAll('[data-simulador]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
