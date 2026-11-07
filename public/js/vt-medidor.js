// public/js/vt-medidor.js
/* Medidor de m² del híbrido (Etapa 2): largo × ancho → m² → precio en la etiqueta → WhatsApp con la medida.
   Precios y textos llegan en los data-* de cada opción, que escribe tools/site/componentes.py desde datos.py: aquí no
   vive ningún precio. Las mensualidades salen de vt-mensualidades.js (window.VTMensualidades), nunca de una fórmula
   propia. Mismo cálculo que componentes.calculo_medidor / textos_medidor (paridad en tests/casos-medidor.json).
   El número de WhatsApp y el mensaje genérico de la página también llegan del HTML (data-wa y data-mensaje en
   [data-vt-medidor]). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const PLANO = { ancho: 360, alto: 190, x: 44, y: 56, minimo: 24 };

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const formatoM2 = (x) => x.toLocaleString('es-MX', { maximumFractionDigits: 1 });
  const n1 = (v) => v.toFixed(1);
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;

  function numero(valor) {
    const n = parseFloat(String(valor == null ? '' : valor).replace(',', '.'));
    return n > 0 && n < 1000 ? n : 0;
  }

  // modos: { instalado: {precio, desde, texto, rotulo}, solo: {...}, mayoreo: {..., minimo} }
  function calcular(largo, ancho, modo, modos) {
    const m = modos[modo];
    const m2 = Math.round(largo * ancho * 10) / 10;
    let precio = m.precio;
    let desde = m.desde;
    let texto = m.texto;
    let rotulo = m.rotulo;
    let aviso = '';
    if (m.minimo && m2 < m.minimo) {
      precio = modos.solo.precio;
      desde = false;
      texto = modos.solo.texto;
      rotulo = `Solo pasto (mayoreo desde ${m.minimo} m²)`;
      aviso = `El mayoreo aplica desde ${m.minimo} m². Te faltan ${Math.ceil(m.minimo - m2)} m²; mientras, calculamos a $${precio}/m² (solo pasto).`;
    }
    return { m2, precio, desde, texto, rotulo, aviso, total: Math.round(m2 * precio) };
  }

  function textos(largo, ancho, r, colonia, M) {
    const medida = `${largo.toFixed(2)} × ${ancho.toFixed(2)} m = ${formatoM2(r.m2)} m²`;
    const desde = r.desde ? 'desde ' : '';
    const disponibles = M.plazosDisponibles(r.total);
    let plan = `Mensualidades con tarjeta de crédito en cotizaciones desde ${dinero(M.minimoDe(3))}.`;
    if (disponibles.length) {
      const ultimo = disponibles[disponibles.length - 1];
      const total = M.totalAPlazos(r.total, ultimo);
      plan = `O ${ultimo} mensualidades de ${dinero(total / ultimo)} con tarjeta de crédito (total ${dinero(total)}).`;
    }
    const cierre = r.desde ? 'Al medir te damos el precio cerrado.' : 'La entrega se cotiza según tu colonia.';
    const mensaje = [`Hola, quiero cotizar ${r.texto}.`, `Medidas: ${medida}`,
      `Estimado de la web: ${desde}${dinero(r.total)} con IVA`, `Colonia: ${colonia || '___'}`,
      'Te mando foto del área.'].join('\n');
    return { medida, monto: dinero(r.total), calc: `${formatoM2(r.m2)} m² × ${desde}$${r.precio}/m², con IVA. ${cierre}`,
      plan, mensaje };
  }

  function plano(largo, ancho) {
    const escala = Math.min(PLANO.ancho / largo, PLANO.alto / ancho);
    const w = Math.max(PLANO.minimo, largo * escala);
    const h = Math.max(PLANO.minimo, ancho * escala);
    return { x: PLANO.x + (PLANO.ancho - w) / 2, y: PLANO.y + (PLANO.alto - h) / 2, w, h };
  }

  function dibujar(svg, largo, ancho, m2) {
    const { x, y, w, h } = plano(largo, ancho);
    const lado = x + w + 22;
    svg.querySelectorAll('[data-vt-plano]').forEach((r) => {
      r.setAttribute('x', n1(x)); r.setAttribute('y', n1(y)); r.setAttribute('width', n1(w)); r.setAttribute('height', n1(h));
    });
    svg.querySelector('[data-vt-cota="arriba"]').setAttribute('d',
      `M${n1(x)} ${n1(y - 26)} v14 M${n1(x + w)} ${n1(y - 26)} v14 M${n1(x)} ${n1(y - 19)} H${n1(x + w)}`);
    const arriba = svg.querySelector('[data-vt-texto="arriba"]');
    arriba.setAttribute('x', n1(x + w / 2)); arriba.setAttribute('y', n1(y - 32)); arriba.textContent = `${largo.toFixed(2)} m`;
    svg.querySelector('[data-vt-cota="lado"]').setAttribute('d',
      `M${n1(lado - 7)} ${n1(y)} h14 M${n1(lado - 7)} ${n1(y + h)} h14 M${n1(lado)} ${n1(y)} V${n1(y + h)}`);
    const costado = svg.querySelector('[data-vt-texto="lado"]');
    costado.setAttribute('transform', `translate(${n1(lado + 20)} ${n1(y + h / 2)}) rotate(-90)`);
    costado.textContent = `${ancho.toFixed(2)} m`;
    const area = svg.querySelector('[data-vt-texto="area"]');
    area.setAttribute('x', n1(x + w / 2)); area.setAttribute('y', n1(y + h / 2 + 9));
    area.textContent = `${formatoM2(m2)} m²`;
    area.style.display = w > 96 && h > 34 ? '' : 'none';
  }

  function leerModos(caja) {
    const modos = {};
    caja.querySelectorAll('input[type="radio"][data-precio]').forEach((i) => {
      modos[i.value] = { precio: Number(i.dataset.precio), desde: i.dataset.desde === '1', texto: i.dataset.texto,
        rotulo: i.dataset.rotulo, minimo: Number(i.dataset.minimo) || 0 };
    });
    return modos;
  }

  function iniciar(caja, M) {
    const campo = (nombre) => caja.querySelector(`[data-vt-campo="${nombre}"]`);
    const salida = (nombre) => caja.querySelector(`[data-vt-o="${nombre}"]`);
    const svg = caja.querySelector('svg');
    const modos = leerModos(caja);
    const wa = caja.dataset.wa;
    function actualizar() {
      const largo = numero(campo('largo').value);
      const ancho = numero(campo('ancho').value);
      const elegido = caja.querySelector('input[type="radio"]:checked');
      if (!largo || !ancho || !elegido) {
        salida('monto').textContent = '—';
        salida('calc').textContent = 'Escribe el largo y el ancho de tu patio.';
        salida('plan').textContent = '';
        salida('aviso').hidden = true;
        // Sin medida válida, el botón manda el mensaje genérico de la página: nunca un estimado viejo.
        salida('cta').setAttribute('href', enlace(wa, caja.dataset.mensaje));
        return;
      }
      const r = calcular(largo, ancho, elegido.value, modos);
      const t = textos(largo, ancho, r, campo('colonia').value.trim(), M);
      dibujar(svg, largo, ancho, r.m2);
      salida('m2').textContent = t.medida;
      salida('rotulo').textContent = r.rotulo;
      salida('monto').textContent = t.monto;
      salida('calc').textContent = t.calc;
      salida('plan').textContent = t.plan;
      salida('aviso').textContent = r.aviso;
      salida('aviso').hidden = !r.aviso;
      salida('cta').setAttribute('href', enlace(wa, t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { numero, calcular, textos, plano, enlace };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMedidor = Object.freeze(api);
  const arrancar = () => {
    if (!root.VTMensualidades) return; // sin la fórmula oficial no se calcula nada: queda el estimado del HTML
    document.querySelectorAll('[data-vt-medidor]').forEach((caja) => iniciar(caja, root.VTMensualidades));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
