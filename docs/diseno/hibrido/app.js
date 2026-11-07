/* Viveros Terra · Híbrido Plano + Etiqueta · comportamiento de la maqueta (vanilla, sin dependencias).
   La parte de cálculo es pura y se exporta en Node para poder probarla. */
(function (root) {
  'use strict';

  /* ================= Cálculo (sin DOM) ================= */
  const WA = 'https://wa.me/528333268008?text=';
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');

  // Mensualidades con tarjeta de crédito: misma fórmula que public/js/vt-mensualidades.js
  const TASA_BASE = 0.036, IVA = 0.16;
  const TASAS = { 3: 0.0457, 6: 0.0757, 9: 0.1107, 12: 0.1277 };
  const UMBRALES = [[15000, [3, 6, 9, 12]], [5000, [3, 6]], [2000, [3]]];
  const plazos = (c) => { const u = UMBRALES.find(([m]) => c >= m); return u ? u[1].slice() : []; };
  const totalAPlazos = (c, p) => Math.ceil(c / (1 - (TASA_BASE + TASAS[p]) * (1 + IVA)));
  const mensualidad = (c, p) => Math.round(totalAPlazos(c, p) / p);
  const minimoDe = (p) => Math.min(...UMBRALES.filter(([, ps]) => ps.includes(p)).map(([m]) => m));

  // Pasto San Agustín (tools/pasto y /precios): $85 solo pasto, desde $120 instalado, mayoreo desde $60 con 500 m² o más.
  // El mayoreo es precio de solo pasto: si no llega a 500 m², se calcula a $85 (solo pasto), nunca al de instalado.
  const MODOS = {
    instalado: { p: 120, desde: true, txt: 'pasto San Agustín instalado', etiqueta: 'Instalado · desde' },
    solo: { p: 85, desde: false, txt: 'solo el pasto San Agustín (yo lo instalo)', etiqueta: 'Solo pasto' },
    mayoreo: { p: 60, desde: true, min: 500, txt: 'pasto San Agustín de mayoreo (solo pasto)', etiqueta: 'Mayoreo · desde' },
  };
  function pasto(L, A, modo) {
    const m = MODOS[modo];
    const m2 = Math.round(L * A * 10) / 10;
    let p = m.p, warn = '', desde = m.desde;
    if (m.min && m2 < m.min) {
      p = MODOS.solo.p; desde = false;
      warn = `El mayoreo aplica desde ${m.min} m². Te faltan ${Math.ceil(m.min - m2)} m²; mientras, calculamos a $${p}/m² (solo pasto).`;
    }
    return { m2, p, desde, warn, total: m2 * p };
  }

  // Pasto sintético (tools/pasto/data.py y public/js/tienda-pasto.js)
  const ROLLO = 50, T2 = 10, MIN_NAC = 25, MIN_SR = 2;
  const ZONAS = { A: 900, B: 1150, C: 1400 };
  const ESTADO_ZONA = {
    'Aguascalientes': 'A', 'CDMX': 'A', 'Colima': 'A', 'Estado de México': 'A', 'Guanajuato': 'A', 'Hidalgo': 'A',
    'Jalisco': 'A', 'Michoacán': 'A', 'Morelos': 'A', 'Nayarit': 'A', 'Puebla': 'A', 'Querétaro': 'A',
    'San Luis Potosí': 'A', 'Tlaxcala': 'A', 'Zacatecas': 'A', 'Coahuila': 'B', 'Durango': 'B', 'Guerrero': 'B',
    'Nuevo León': 'B', 'Oaxaca': 'B', 'Sinaloa': 'B', 'Tamaulipas': 'B', 'Veracruz': 'B', 'Baja California': 'C',
    'Baja California Sur': 'C', 'Campeche': 'C', 'Chiapas': 'C', 'Chihuahua': 'C', 'Quintana Roo': 'C',
    'Sonora': 'C', 'Tabasco': 'C', 'Yucatán': 'C',
  };
  const MODELOS = {
    'toscana-18': { nombre: 'Toscana 18', rollo: 149, t2: 169, t1: 199 },
    'toscana-28': { nombre: 'Toscana 28', rollo: 199, t2: 229, t1: 279 },
    'irlanda-25': { nombre: 'Irlanda 25', rollo: 209, t2: 239, t1: 279 },
  };
  const precioM2 = (m, m2) => (m2 >= ROLLO ? m.rollo : m2 >= T2 ? m.t2 : m.t1);
  const esShowroom = (estado) => estado === 'showroom';
  function quote(slug, m2, estado) {
    const m = MODELOS[slug];
    if (!(m2 >= MIN_SR)) return { error: `El mínimo es ${MIN_SR} m².` };
    if (estado && !esShowroom(estado) && m2 < MIN_NAC) {
      return { error: `Para envío nacional el mínimo es ${MIN_NAC} m² (medio rollo). De ${MIN_SR} a ${MIN_NAC - 1} m² solo en el showroom de Cd. Madero.` };
    }
    const pm2 = precioM2(m, m2), material = pm2 * m2, rollos = Math.ceil(m2 / ROLLO);
    const tarifa = estado && !esShowroom(estado) ? ZONAS[ESTADO_ZONA[estado]] : 0;
    return { pm2, material, rollos, tarifa, envio: tarifa * rollos, total: material + tarifa * rollos };
  }
  function cartQuote(rows, estado) {
    const lines = rows.map((r) => Object.assign({ slug: r.slug, m2: r.m2 }, quote(r.slug, r.m2, estado)));
    const ok = lines.filter((l) => !l.error);
    const material = ok.reduce((s, l) => s + l.material, 0);
    const envio = ok.reduce((s, l) => s + l.envio, 0);
    const rollos = ok.reduce((s, l) => s + l.rollos, 0);
    return { lines, material, envio, rollos, total: material + envio, blocked: lines.some((l) => l.error) };
  }
  function cartMessage(rows, estado) {
    const q = cartQuote(rows, estado);
    const body = q.lines.map((l, i) => `${i + 1}) ${MODELOS[l.slug].nombre} · ${l.m2} m² × ${money(l.pm2)}/m² = ${money(l.material)}`).join('\n');
    const dest = !estado ? 'Entrega: ___ (mi estado)'
      : esShowroom(estado) ? 'Entrega: recojo en el showroom de Cd. Madero'
        : `Entrega: ${estado} · envío ${q.rollos} ${q.rollos === 1 ? 'rollo' : 'rollos'} × ${money(ZONAS[ESTADO_ZONA[estado]])} = ${money(q.envio)}`;
    return `Hola, quiero cotizar pasto sintético (vengo de viverosterra.com):\n${body}\n${dest}\nTotal estimado: ${money(q.total)} con IVA`;
  }

  const CALC = { money, plazos, totalAPlazos, mensualidad, minimoDe, pasto, quote, cartQuote, cartMessage, MODELOS };
  if (typeof module !== 'undefined' && module.exports) { module.exports = CALC; return; }

  /* ================= DOM ================= */
  const doc = root.document;
  const $ = (s, r) => (r || doc).querySelector(s);
  const $$ = (s, r) => Array.from((r || doc).querySelectorAll(s));
  const num = (v) => { const n = parseFloat(String(v).replace(',', '.')); return Number.isFinite(n) && n > 0 ? n : 0; };
  const fmt2 = (n) => n.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const waHref = (msg) => WA + encodeURIComponent(msg);
  const reduced = root.matchMedia('(prefers-reduced-motion: reduce)').matches;
  doc.documentElement.classList.add('js');
  // Solo para capturas de la maqueta (?shot): carga las imágenes diferidas
  if (/[?&]shot/.test(root.location.search)) $$('img[loading="lazy"]').forEach((i) => { i.loading = 'eager'; });

  // Aparición bajo el pliegue (solo opacity/transform, nunca el hero)
  const reveals = $$('.reveal');
  if (!reduced && 'IntersectionObserver' in root) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px' });
    reveals.forEach((r) => io.observe(r));
  } else reveals.forEach((r) => r.classList.add('is-in'));

  // Menú móvil
  const mb = $('.burger'), mm = $('#menu-movil');
  if (mb && mm) mb.addEventListener('click', () => {
    const open = mb.getAttribute('aria-expanded') === 'true';
    mb.setAttribute('aria-expanded', String(!open)); mm.hidden = open;
  });

  // Barra fija: se oculta mientras el CTA del hero está en pantalla
  const bar = $('.bar'), heroCta = $('[data-hero-cta]');
  if (bar && heroCta && 'IntersectionObserver' in root) {
    new IntersectionObserver(([e]) => bar.classList.toggle('is-hidden', e.isIntersecting)).observe(heroCta);
  }
  function setBar(strong, small, href) {
    if (!bar) return;
    const ctx = $('.ctx', bar);
    if (ctx) { ctx.hidden = !strong; $('b', ctx).textContent = strong || ''; $('span', ctx).textContent = small || ''; }
    if (href) $('.go', bar).href = href;
  }

  /* ---------- Medidor de pasto natural: largo × ancho → m² → precio en la etiqueta → WhatsApp ---------- */
  function drawPlot(svg, L, A) {
    const MW = 360, MH = 190, s = Math.min(MW / L, MH / A);
    const w = Math.max(24, L * s), h = Math.max(24, A * s);
    const X = 44 + (MW - w) / 2, Y = 56 + (MH - h) / 2;
    $$('.plot', svg).forEach((r) => { r.setAttribute('x', X); r.setAttribute('y', Y); r.setAttribute('width', w); r.setAttribute('height', h); });
    $('.c-top', svg).setAttribute('d', `M${X} ${Y - 26} v14 M${X + w} ${Y - 26} v14 M${X} ${Y - 19} H${X + w}`);
    const tt = $('.t-top', svg); tt.setAttribute('x', X + w / 2); tt.setAttribute('y', Y - 32); tt.textContent = fmt2(L) + ' m';
    const cx = X + w + 22;
    $('.c-side', svg).setAttribute('d', `M${cx - 7} ${Y} h14 M${cx - 7} ${Y + h} h14 M${cx} ${Y} V${Y + h}`);
    const ts = $('.t-side', svg); ts.setAttribute('transform', `translate(${cx + 20} ${Y + h / 2}) rotate(-90)`); ts.textContent = fmt2(A) + ' m';
    const ta = $('.t-area', svg); ta.setAttribute('x', X + w / 2); ta.setAttribute('y', Y + h / 2 + 9);
    ta.textContent = (L * A).toLocaleString('es-MX', { maximumFractionDigits: 1 }) + ' m²';
    ta.style.display = w > 96 && h > 34 ? '' : 'none';
  }
  $$('[data-medidor="pasto"]').forEach((box) => {
    const f = (n) => $(`[name="${n}"]`, box);
    const o = (k) => $(`[data-o="${k}"]`, box);
    const svg = $('svg', box);
    let touched = false;
    function update() {
      const L = num(f('largo').value), A = num(f('ancho').value);
      const modo = $('input[name="modo"]:checked', box).value;
      if (L && A) drawPlot(svg, L, A);
      const r = pasto(L, A, modo);
      o('warn').textContent = r.warn; o('warn').hidden = !r.warn;
      o('modo').textContent = r.warn ? 'Solo pasto (mayoreo desde 500 m²)' : MODOS[modo].etiqueta;
      if (!r.m2) { o('amt').textContent = '—'; o('calc').textContent = 'Escribe el largo y el ancho de tu patio.'; o('plan').textContent = ''; return; }
      o('amt').textContent = money(r.total);
      o('m2').textContent = `${fmt2(L)} × ${fmt2(A)} m = ${r.m2.toLocaleString('es-MX')} m²`;
      o('calc').textContent = `${r.m2.toLocaleString('es-MX')} m² × ${r.desde ? 'desde ' : ''}$${r.p}/m², con IVA. ` + (MODOS[modo].desde && !r.warn ? 'Al medir te damos el precio cerrado.' : 'La entrega se cotiza según tu colonia.');
      const ps = plazos(r.total), last = ps[ps.length - 1];
      o('plan').textContent = last ? `O ${last} mensualidades de ${money(mensualidad(r.total, last))} con tarjeta de crédito (total ${money(totalAPlazos(r.total, last))}).` : 'Mensualidades con tarjeta de crédito desde $2,000.';
      const col = f('colonia').value.trim();
      const msg = `Hola, quiero cotizar ${r.warn ? MODOS.solo.txt : MODOS[modo].txt} · ${fmt2(L)} × ${fmt2(A)} m = ${r.m2.toLocaleString('es-MX')} m² · Estimado de la web ${r.desde ? 'desde ' : ''}${money(r.total)} con IVA · Colonia: ${col || '___'} · Te mando foto del área.`;
      o('cta').href = waHref(msg);
      if (touched) setBar(`${r.m2.toLocaleString('es-MX')} m² · ${money(r.total)}`, 'tu medida va en el mensaje', o('cta').href);
    }
    const onInput = () => { touched = true; update(); };
    box.addEventListener('input', onInput); box.addEventListener('change', onInput);
    update();
  });

  /* ---------- Tienda: cotizador por estado, rollo a escala, lista de cotización real ---------- */
  const cart = [];
  const estadoSel = $('#estado');
  if (estadoSel) Object.keys(ESTADO_ZONA).sort((a, b) => a.localeCompare(b, 'es')).forEach((e) => estadoSel.add(new Option(e, e)));
  const estado = () => (estadoSel ? estadoSel.value : '');
  const toast = $('.toast');
  function say(t) { if (!toast) return; toast.textContent = t; toast.hidden = false; clearTimeout(say.t); say.t = setTimeout(() => { toast.hidden = true; }, 3200); }

  const cartBox = $('[data-cart]');
  function renderCart() {
    if (!cartBox) return;
    const n = cart.length;
    $$('[data-cart-n]').forEach((b) => { b.textContent = n ? `(${n})` : ''; });
    cartBox.hidden = !n;
    if (!n) return;
    const q = cartQuote(cart, estado());
    const ul = $('ul', cartBox); ul.textContent = '';
    q.lines.forEach((l, i) => {
      const li = doc.createElement('li');
      const name = doc.createElement('span'); name.innerHTML = `<b></b> · ${l.m2} m²`; $('b', name).textContent = MODELOS[l.slug].nombre;
      const amt = doc.createElement('span'); amt.className = 'amt'; amt.textContent = l.error ? '—' : money(l.material);
      const rm = doc.createElement('button'); rm.type = 'button'; rm.className = 'rm'; rm.textContent = '×';
      rm.setAttribute('aria-label', `Quitar ${MODELOS[l.slug].nombre} de la cotización`);
      rm.addEventListener('click', () => { cart.splice(i, 1); renderCart(); });
      li.append(name, amt, rm);
      if (l.error) { const e = doc.createElement('span'); e.className = 'err'; e.textContent = l.error; li.append(e); }
      ul.append(li);
    });
    const est = estado();
    $('[data-o="cart-envio"]', cartBox).textContent = !est ? 'Elige tu estado para sumar el envío por rollo.' : esShowroom(est) ? 'Recoges en el showroom de Cd. Madero, sin envío.' : `Envío: ${q.rollos} ${q.rollos === 1 ? 'rollo' : 'rollos'} × ${money(ZONAS[ESTADO_ZONA[est]])} = ${money(q.envio)}`;
    $('[data-o="cart-total"]', cartBox).textContent = money(q.total);
    const send = $('[data-o="cart-send"]', cartBox);
    if (q.blocked) { send.removeAttribute('href'); send.setAttribute('aria-disabled', 'true'); send.textContent = 'Ajusta los renglones marcados para enviar'; }
    else { send.href = waHref(cartMessage(cart, est)); send.removeAttribute('aria-disabled'); send.innerHTML = send.dataset.label; }
    setBar(`Cotización (${n})`, `${money(q.total)}${est && !esShowroom(est) ? ' con envío' : ''}`, q.blocked ? null : send.href);
  }
  function addToCart(slug, m2) {
    cart.push({ slug, m2 });
    renderCart();
    say(`${MODELOS[slug].nombre} · ${m2} m² agregado a tu cotización`);
  }
  $$('.card .add').forEach((b) => b.addEventListener('click', () => addToCart(b.dataset.slug, Number(b.dataset.m2) || ROLLO)));
  if (estadoSel) estadoSel.addEventListener('change', renderCart);

  function drawRoll(svg, m2, rollos) {
    const L = m2 / 2, X = 40, Y = 70, MW = 340;
    const w = Math.max(30, Math.min(MW, MW * L / Math.max(25, Math.ceil(L / 25) * 25)));
    const h = Math.max(16, Math.min(70, w * 2 / L));
    $$('.plot', svg).forEach((r) => { r.setAttribute('width', w); r.setAttribute('height', h); r.setAttribute('y', Y); });
    $('.c-top', svg).setAttribute('d', `M${X} 40 v14 M${X + w} 40 v14 M${X} 47 H${X + w}`);
    const tt = $('.t-top', svg); tt.setAttribute('x', X + w / 2); tt.textContent = fmt2(L) + ' m de largo';
    const cx = X + w + 18;
    $('.c-side', svg).setAttribute('d', `M${cx - 7} ${Y} h14 M${cx - 7} ${Y + h} h14 M${cx} ${Y} V${Y + h}`);
    const ts = $('.t-side', svg); ts.setAttribute('x', cx + 12); ts.setAttribute('y', Y + h / 2 + 5); ts.textContent = '2.00 m';
    const joints = $('.joints', svg); joints.textContent = '';
    for (let i = 1; i * 25 < L; i++) {
      const x = X + w * (i * 25) / L;
      const ln = doc.createElementNS('http://www.w3.org/2000/svg', 'line');
      ln.setAttribute('class', 'joint'); ln.setAttribute('x1', x); ln.setAttribute('x2', x); ln.setAttribute('y1', Y); ln.setAttribute('y2', Y + h);
      joints.appendChild(ln);
    }
    const ta = $('.t-area', svg); ta.setAttribute('x', X); ta.setAttribute('y', Y + h + 32);
    ta.textContent = `${m2.toLocaleString('es-MX')} m² · ${rollos} ${rollos === 1 ? 'rollo' : 'rollos'} de 2 × 25 m`;
  }

  $$('[data-cotizador]').forEach((box) => {
    const slug = box.dataset.cotizador, m = MODELOS[slug];
    const inM2 = $('#m2', box), svg = $('svg', box);
    const o = (k) => $(`[data-o="${k}"]`, box);
    const tiers = $$('[data-t]');
    let touched = false;
    function update() {
      const m2 = Math.round(num(inM2.value));
      const est = estado(), q = quote(slug, m2, est);
      tiers.forEach((d) => d.classList.toggle('on', d.dataset.t === (m2 >= ROLLO ? 'rollo' : m2 >= T2 ? 't2' : 't1')));
      o('warn').textContent = q.error || ''; o('warn').hidden = !q.error;
      const cta = o('cta'), add = o('add');
      if (q.error) {
        ['pm2', 'material', 'envio'].forEach((k) => { o(k).textContent = '—'; });
        o('amt').textContent = '—'; o('plan').textContent = '';
        $$('input[name="plan"]', box).forEach((r) => { if (r.value !== '1') { r.disabled = true; $('small', r.closest('label')).textContent = '—'; } });
        cta.removeAttribute('href'); cta.setAttribute('aria-disabled', 'true'); add.disabled = true;
        cta.innerHTML = 'Ajusta los m² o elige recoger en showroom';
        return;
      }
      cta.removeAttribute('aria-disabled'); add.disabled = false; cta.innerHTML = cta.dataset.label;
      drawRoll(svg, m2, q.rollos);
      o('pm2').textContent = money(q.pm2) + '/m²';
      o('material').textContent = money(q.material);
      o('envio').textContent = !est ? 'Elige tu estado' : esShowroom(est) ? 'Recoges en Cd. Madero' : `${q.rollos} × ${money(q.tarifa)} = ${money(q.envio)}`;
      const contado = est ? q.total : q.material;
      o('amt').textContent = money(contado);
      o('lbl').textContent = est && !esShowroom(est) ? 'Total con envío · IVA incluido' : 'Material · IVA incluido';
      const disp = plazos(contado);
      let plan = Number(($('input[name="plan"]:checked', box) || {}).value || 1);
      $$('input[name="plan"]', box).forEach((r) => {
        const p = Number(r.value), ok = p === 1 || disp.includes(p);
        r.disabled = !ok;
        if (p > 1) $('small', r.closest('label')).textContent = ok ? money(mensualidad(contado, p)) + '/mes' : 'desde ' + money(minimoDe(p));
        if (!ok && p === plan) { plan = 1; $('input[name="plan"][value="1"]', box).checked = true; }
      });
      o('plan').textContent = plan > 1
        ? `${plan} mensualidades de ${money(mensualidad(contado, plan))} con tarjeta de crédito · total ${money(totalAPlazos(contado, plan))}. Tu banco debe aceptar el plan.`
        : 'Contado: transferencia, efectivo o tarjeta en una sola exhibición. Es el precio más bajo.';
      const planTxt = plan > 1 ? ` · Forma de pago: ${plan} mensualidades de ${money(mensualidad(contado, plan))} con tarjeta de crédito (total ${money(totalAPlazos(contado, plan))})` : ' · Pago de contado';
      const dest = !est ? ' · Entrega: ___ (mi estado)' : esShowroom(est) ? ' · Recojo en el showroom de Cd. Madero' : ` · Entrega en ${est} (envío ${q.rollos} ${q.rollos === 1 ? 'rollo' : 'rollos'} = ${money(q.envio)})`;
      cta.href = waHref(`Hola, quiero cotizar pasto sintético ${m.nombre} · ${m2} m² × ${money(q.pm2)}/m² = ${money(q.material)}${dest} · Total estimado ${money(contado)} con IVA${planTxt}`);
      if (!cart.length && touched) setBar(`${m.nombre} · ${m2} m²`, money(contado), cta.href);
    }
    $$('[data-step]', box).forEach((b) => b.addEventListener('click', () => { inM2.value = Math.max(MIN_SR, Math.round(num(inM2.value)) + Number(b.dataset.step)); touched = true; update(); }));
    $$('[data-preset]', box).forEach((b) => b.addEventListener('click', () => { inM2.value = b.dataset.preset; touched = true; update(); }));
    o('add').addEventListener('click', () => addToCart(slug, Math.round(num(inM2.value))));
    const onInput = () => { touched = true; update(); renderCart(); };
    box.addEventListener('input', onInput); box.addEventListener('change', onInput);
    update();
  });

  /* ---------- Galería de la ficha ---------- */
  const gmain = $('.gal-main img'), gcap = $('[data-o="gcap"]');
  $$('.thumbs button').forEach((b) => b.addEventListener('click', () => {
    $$('.thumbs button').forEach((x) => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', 'true');
    gmain.src = b.dataset.src; gmain.alt = b.dataset.alt; if (gcap) gcap.innerHTML = b.dataset.cap;
  }));
})(typeof window !== 'undefined' ? window : globalThis);
