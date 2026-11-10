// public/js/vt-simulador.js
/* Simulador de mensualidades para servicios (monto de una cotización). Depende de vt-mensualidades.js.
   Las filas se crean una sola vez y solo se actualizan: así el foco del teclado no se pierde al cambiar de plan.
   El monto del HTML es un ejemplo: mientras el cliente no escriba uno, el mensaje no lleva ninguna cifra (reescritura 3
   del informe de recorrido) y pide colonia y metros. Con un monto escrito, el mensaje lleva ese monto y la forma de pago,
   y el enlace se presta a la barra fija y al encabezado (window.VTBarra de terra.js). mensaje() se exporta para
   node --test. */
(function () {
  'use strict';
  const WA = '528333268008';
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const BARRA = 'Enviar mi plan de pago';

  // contado: el monto que escribió el cliente (0 si no escribió nada); plazo: el elegido (0 = contado) y su total.
  function mensaje(servicio, contado, plazo, total) {
    if (!contado) {
      return [`Hola, quiero cotizar ${servicio} y me interesa pagar con tarjeta en mensualidades.`,
        plazo ? `Me interesa: ${plazo} mensualidades con tarjeta de crédito.` : '', 'Colonia: ___', 'Metros aprox.: ___']
        .filter(Boolean).join('\n');
    }
    const pago = plazo ? `Me interesa pagar en ${plazo} mensualidades con tarjeta de crédito (total ${money(total)}).`
      : 'Pagaría de contado.';
    return [`Hola, quiero cotizar ${servicio}.`, `Mi cotización es de ${money(contado)}.`, pago, 'Colonia: ___'].join('\n');
  }

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
    // El monto del HTML es un ejemplo: cuenta solo cuando el cliente lo cambia.
    let escrito = false;
    const clave = 'simulador:' + (wa.getAttribute('data-cta') || '');

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
      const propio = escrito ? contado : 0;
      const msg = mensaje(servicio, propio, elegido ? elegido.plazo : 0, elegido ? elegido.total : 0);
      wa.href = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
      const barra = window.VTBarra; // init(root) recibe la caja del simulador: la barra vive en window
      if (barra) {
        if (propio) barra.prestar(clave, wa.href, BARRA);
        else barra.soltar(clave);
      }
    }

    filas.forEach((f) => f.radio.addEventListener('change', () => {
      if (f.radio.checked) { plan = f.plazo; paint(); }
    }));
    input.addEventListener('input', () => { escrito = true; paint(); });
    paint();
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { mensaje, BARRA };
    return;
  }
  function start() { document.querySelectorAll('[data-simulador]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
