// public/js/vt-medidor.js
/* Medidor de m² del híbrido (Etapa 2): largo × ancho → m² → precio en la etiqueta → WhatsApp con la medida.
   Precios y textos llegan en los data-* de cada opción, que escribe tools/site/componentes.py desde datos.py: aquí no
   vive ningún precio. Las mensualidades salen de vt-mensualidades.js (window.VTMensualidades), nunca de una fórmula
   propia. Mismo cálculo que componentes.calculo_medidor / textos_medidor (paridad en tests/casos-medidor.json).
   El número de WhatsApp y el mensaje genérico de la página también llegan del HTML (data-wa y data-mensaje en
   [data-vt-medidor]). Donde el botón trae data-vt-o="cta-texto" (la home), con medida válida dice "Enviar mi medida
   por WhatsApp". Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const PLANO = { ancho: 360, alto: 190, x: 44, y: 56, minimo: 24 };

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const formatoM2 = (x) => x.toLocaleString('es-MX', { maximumFractionDigits: 1 });
  const n1 = (v) => v.toFixed(1);
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;

  const leer = (valor) => parseFloat(String(valor == null ? '' : valor).replace(',', '.'));
  function numero(valor) {
    const n = leer(valor);
    return n > 0 && n < 1000 ? n : 0;
  }
  // Un lado de 1,000 m o más ya no es un patio: se pide escribirnos y el botón manda el mensaje de proyecto.
  const grande = (valor) => leer(valor) >= 1000;

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

  // Texto del botón con una medida válida (componentes.CTA_MEDIDA). Sin medida vuelve el texto con el que llegó el HTML.
  const CTA_MEDIDA = 'Enviar mi medida por WhatsApp';

  // plazo: 1 (contado) o las mensualidades elegidas; si no aplican a ese total, contado.
  function textos(largo, ancho, r, colonia, M, plazo) {
    const medida = `${largo.toFixed(2)} × ${ancho.toFixed(2)} m = ${formatoM2(r.m2)} m²`;
    const desde = r.desde ? 'desde ' : '';
    const disponibles = M.plazosDisponibles(r.total);
    const elegido = disponibles.includes(plazo) ? plazo : 1;
    let plan = `Mensualidades con tarjeta de crédito en cotizaciones desde ${dinero(M.minimoDe(3))}.`;
    let interes = 'contado';
    if (elegido > 1) {
      const total = M.totalAPlazos(r.total, elegido);
      interes = `${elegido} mensualidades de ${dinero(total / elegido)} con tarjeta de crédito (total ${dinero(total)})`;
      plan = `${interes}. Tu banco debe aceptar el plan.`;
    } else if (disponibles.length) {
      const ultimo = disponibles[disponibles.length - 1];
      const total = M.totalAPlazos(r.total, ultimo);
      plan = `O ${ultimo} mensualidades de ${dinero(total / ultimo)} con tarjeta de crédito (total ${dinero(total)}).`;
    }
    const cierre = r.desde ? 'Al medir te damos el precio cerrado.' : 'La entrega se cotiza según tu colonia.';
    const mensaje = [`Hola, quiero cotizar ${r.texto}.`, `Medidas: ${medida}`,
      `Estimado de la web: ${desde}${dinero(r.total)} con IVA`, `Me interesa: ${interes}`, `Colonia: ${colonia || '___'}`,
      'Te mando foto del área.'].join('\n');
    return { medida, monto: dinero(r.total), calc: `${formatoM2(r.m2)} m² × ${desde}$${r.precio}/m², con IVA. ${cierre}`,
      plan, plazo: elegido, mensaje, cta: CTA_MEDIDA };
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

  // Mismos textos que componentes.VACIO_MEDIDOR: sin medida, la etiqueta queda igual que en el HTML.
  const VACIO = { medida: 'Escribe tus medidas', monto: '—', calc: 'Escribe el largo y el ancho de tu patio.' };

  function iniciar(caja, M) {
    const campo = (nombre) => caja.querySelector(`[data-vt-campo="${nombre}"]`);
    const salida = (nombre) => caja.querySelector(`[data-vt-o="${nombre}"]`);
    const svg = caja.querySelector('svg');
    const modos = leerModos(caja);
    const wa = caja.dataset.wa;
    const plazos = Array.from(caja.querySelectorAll('input[type="radio"][name$="-plazo"]'));
    // Solo donde la página lo pide (data-vt-o="cta-texto"): el botón dice que manda la medida cuando ya hay una.
    const rotuloCta = salida('cta-texto');
    const ctaSinMedida = rotuloCta ? rotuloCta.textContent : '';
    const rotular = (texto) => { if (rotuloCta) rotuloCta.textContent = texto; };
    // Cada plazo muestra su mensualidad si aplica al total; si no, el monto mínimo de cotización y queda deshabilitado.
    function marcarPlazos(total) {
      const disponibles = total ? M.plazosDisponibles(total) : [];
      plazos.forEach((i) => {
        const p = Number(i.value);
        const pie = caja.querySelector(`[data-vt-plazo="${p}"]`);
        if (p === 1) { pie.textContent = total ? dinero(total) : '—'; return; }
        const ok = disponibles.includes(p);
        i.disabled = !ok;
        pie.textContent = ok ? `${dinero(M.totalAPlazos(total, p) / p)}/mes` : `desde ${dinero(M.minimoDe(p))}`;
      });
    }
    function vacio(calc, mensaje, aviso) {
      salida('m2').textContent = VACIO.medida;
      salida('monto').textContent = VACIO.monto;
      salida('monto').parentElement.classList.add('is-vacio');
      salida('calc').textContent = calc;
      salida('plan').textContent = '';
      salida('aviso').textContent = aviso;
      salida('aviso').hidden = !aviso;
      marcarPlazos(0);
      // Sin medida válida, el botón manda el mensaje de la página: nunca un estimado viejo ni el ejemplo del placeholder.
      salida('cta').setAttribute('href', enlace(wa, mensaje));
      rotular(ctaSinMedida);
    }
    function actualizar() {
      const elegido = caja.querySelector('input[name$="-modo"]:checked');
      if (elegido) salida('rotulo').textContent = modos[elegido.value].rotulo;
      if (grande(campo('largo').value) || grande(campo('ancho').value)) {
        vacio('Cada lado debe medir menos de 1,000 m.', caja.dataset.mensajeMayoreo,
          'Para áreas tan grandes, escríbenos: lo cotizamos como proyecto de mayoreo.');
        return;
      }
      const largo = numero(campo('largo').value);
      const ancho = numero(campo('ancho').value);
      if (!largo || !ancho || !elegido) { vacio(VACIO.calc, caja.dataset.mensaje, ''); return; }
      const r = calcular(largo, ancho, elegido.value, modos);
      marcarPlazos(r.total);
      const plazo = caja.querySelector('input[name$="-plazo"]:checked');
      const t = textos(largo, ancho, r, campo('colonia').value.trim(), M, plazo ? Number(plazo.value) : 1);
      if (!plazo || Number(plazo.value) !== t.plazo) plazos.find((i) => i.value === '1').checked = true;
      dibujar(svg, largo, ancho, r.m2);
      salida('m2').textContent = t.medida;
      salida('rotulo').textContent = r.rotulo;
      salida('monto').textContent = t.monto;
      salida('monto').parentElement.classList.remove('is-vacio');
      salida('calc').textContent = t.calc;
      salida('plan').textContent = t.plan;
      salida('aviso').textContent = r.aviso;
      salida('aviso').hidden = !r.aviso;
      salida('cta').setAttribute('href', enlace(wa, t.mensaje));
      rotular(t.cta);
    }
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { numero, grande, calcular, textos, plano, enlace };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMedidor = Object.freeze(api);
  const arrancar = () => {
    if (!root.VTMensualidades) return; // sin la fórmula oficial no se calcula nada: queda el estado vacío del HTML
    document.querySelectorAll('[data-vt-medidor]').forEach((caja) => iniciar(caja, root.VTMensualidades));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
