/* Tienda de pasto sintético · Viveros Terra
   Cotizador por estado, lista de cotización (localStorage) y envío por WhatsApp. */
(function () {
  'use strict';

  const WA_NUMBER = '528333268008';
  const STORE_KEY = 'vt-cotizacion-v1';
  const ROLLO_M2 = 50;
  const TIER2_MIN_M2 = 10;
  /* Mínimos de compra: los escribe la plantilla desde tools/pasto/data.py en el cotizador (data-min-*); el respaldo solo
     aplica en páginas sin cotizador (test_paridad_js.py lo mantiene igual a data.py). */
  const LIMITES = (document.getElementById('comprar') || { dataset: {} }).dataset;
  const MIN_NACIONAL_M2 = Number(LIMITES.minNacional) || 25;
  const MIN_SHOWROOM_M2 = Number(LIMITES.minShowroom) || 2;
  const MAX_M2 = 5000;
  const PICKUP = 'showroom';
  // Envío local en Tampico, Madero y Altamira (cotizador de /pasto-sintetico-tampico): sin flete nacional por estado;
  // el envío local se cotiza según la colonia.
  const LOCAL = 'local';
  const TOAST_MS = 2500;
  const TOAST_GAP = 12;

  const ZONAS = {
    A: { tarifa: 900, nombre: 'Centro y Occidente' },
    B: { tarifa: 1150, nombre: 'Norte, Golfo y Sur' },
    C: { tarifa: 1400, nombre: 'Sureste y fronteras' },
  };
  const ESTADO_ZONA = {
    'Aguascalientes': 'A', 'CDMX': 'A', 'Colima': 'A', 'Estado de México': 'A', 'Guanajuato': 'A', 'Hidalgo': 'A',
    'Jalisco': 'A', 'Michoacán': 'A', 'Morelos': 'A', 'Nayarit': 'A', 'Puebla': 'A', 'Querétaro': 'A',
    'San Luis Potosí': 'A', 'Tlaxcala': 'A', 'Zacatecas': 'A',
    'Coahuila': 'B', 'Durango': 'B', 'Guerrero': 'B', 'Nuevo León': 'B', 'Oaxaca': 'B', 'Sinaloa': 'B',
    'Tamaulipas': 'B', 'Veracruz': 'B',
    'Baja California': 'C', 'Baja California Sur': 'C', 'Campeche': 'C', 'Chiapas': 'C', 'Chihuahua': 'C',
    'Quintana Roo': 'C', 'Sonora': 'C', 'Tabasco': 'C', 'Yucatán': 'C',
  };
  Object.freeze(ESTADO_ZONA);

  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params);
  }

  // Mismos parámetros que el generate_lead del shell (terra.js): cta_id "<tipo de página>:<sección>" y service.
  function leadWhatsapp(method, seccion, extra) {
    const head = document.querySelector('.vt-head');
    const tipo = (head && head.getAttribute('data-vt-tipo')) || 'tienda';
    track('generate_lead', { ...extra, method, cta_id: tipo + ':' + seccion, service: 'pasto-sintetico' });
  }

  /* ---------- Pricing ---------- */
  function precioM2(model, m2) {
    if (m2 >= ROLLO_M2) return model.rollo;
    return m2 >= TIER2_MIN_M2 ? model.t2 : model.t1;
  }

  function tierFor(m2) {
    if (m2 >= ROLLO_M2) return 'rollo';
    return m2 >= TIER2_MIN_M2 ? 't2' : 't1';
  }

  const sinFleteNacional = (estado) => estado === PICKUP || estado === LOCAL;

  function quoteLine(model, m2, estado) {
    const isPickup = sinFleteNacional(estado);
    const min = isPickup ? MIN_SHOWROOM_M2 : MIN_NACIONAL_M2;
    if (!Number.isFinite(m2) || m2 < min) {
      return { error: isPickup
        ? `En showroom vendemos desde ${MIN_SHOWROOM_M2} m².`
        // Reescritura 14 (Entrega B de experiencia): el aviso dice cómo seguir.
        : `Para envío nacional el mínimo es ${MIN_NACIONAL_M2} m² (medio rollo). Sube a ${MIN_NACIONAL_M2} m² o elige "Recoger en showroom, Cd. Madero", donde vendemos desde ${MIN_SHOWROOM_M2} m².` };
    }
    const pm2 = precioM2(model, m2);
    const material = pm2 * m2;
    const rollos = Math.ceil(m2 / ROLLO_M2);
    const zona = isPickup ? null : ESTADO_ZONA[estado] || null;
    const envio = zona ? ZONAS[zona].tarifa * rollos : 0;
    return { pm2, material, rollos, zona, envio, isPickup, total: material + envio, landed: (material + envio) / m2 };
  }

  /* ---------- Mensualidades ---------- */
  function planesPara(contado) {
    return window.VTMensualidades && contado > 0 ? window.VTMensualidades.planes(contado) : [];
  }

  function planElegido(contado) {
    const p = planesPara(contado).find((x) => x.plazo === memoryState.plan && x.disponible);
    return p || null;
  }

  function renderPlanRow(row, planes, contado) {
    const v = Number(row.dataset.plan);
    const input = $('input', row);
    const amount = $('[data-plan-amount]', row);
    const total = $('[data-plan-total]', row);
    if (v === 0) {
      amount.textContent = '';
      total.textContent = money(contado);
    } else {
      const p = planes.find((x) => x.plazo === v);
      const ok = Boolean(p && p.disponible);
      input.disabled = !ok;
      row.dataset.disabled = String(!ok);
      amount.textContent = ok ? `≈ ${money(p.mensualidad)} al mes` : `Desde ${money(window.VTMensualidades.minimoDe(v))}`;
      total.textContent = ok ? `${money(p.total)} · +${money(p.diferencia)}` : '';
    }
    input.checked = v === memoryState.plan;
  }

  function renderPlans(root, contado) {
    if (!root) return;
    const planes = planesPara(contado);
    root.hidden = planes.length === 0;
    if (planes.length === 0) return;
    if (memoryState.plan && !planes.some((x) => x.plazo === memoryState.plan && x.disponible)) {
      writeStore({ ...memoryState, plan: 0 }, false);
    }
    $$('.plan', root).forEach((row) => renderPlanRow(row, planes, contado));
    const p = planElegido(contado);
    $('[data-trip-contado]', root).textContent = money(contado);
    $('[data-trip-mes]', root).textContent = p ? `≈ ${money(p.mensualidad)}` : '—';
    $('[data-trip-total]', root).textContent = money(p ? p.total : contado);
    const ahorro = p ? p.diferencia : (planes.filter((x) => x.disponible).pop() || {}).diferencia;
    $('[data-plan-save]', root).textContent = ahorro ? `Pagando de contado te ahorras ${money(ahorro)}.` : '';
    const rule = $('.pay-rule', root);
    if (rule) {
      const n = p ? p.plazo : 1;
      rule.replaceChildren(...Array.from({ length: n }, () => document.createElement('i')));
      rule.dataset.plazo = String(n);
    }
  }

  function planLine(contado) {
    const p = planElegido(contado);
    return p
      ? `Forma de pago: ${p.plazo} mensualidades de ≈ ${money(p.mensualidad)} con tarjeta de crédito (total ${money(p.total)}).`
      : 'Forma de pago: contado.';
  }

  function initPlanInputs(onChange) {
    $$('[data-plans] input[type="radio"]').forEach((input) => {
      input.addEventListener('change', () => {
        writeStore({ ...memoryState, plan: Number(input.value) });
        onChange();
      });
    });
  }

  /* ---------- Quote list storage ---------- */
  function readStore() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
      const items = Array.isArray(raw.items) ? raw.items.filter(isValidItem) : [];
      const plan = [0, 3, 6, 9, 12].includes(raw.plan) ? raw.plan : 0;
      return { items, estado: typeof raw.estado === 'string' ? raw.estado : '', plan };
    } catch (err) {
      return { items: [], estado: '', plan: 0 };
    }
  }

  function isValidItem(it) {
    return it && typeof it.slug === 'string' && typeof it.nombre === 'string' &&
      Number.isFinite(it.m2) && Number.isFinite(it.rollo) && Number.isFinite(it.t2) && Number.isFinite(it.t1);
  }

  let memoryState = readStore();

  /* avisar=false: el cambio sale de un render (renderPlans) y no debe volver a disparar update() por vt:lista. */
  function writeStore(next, avisar = true) {
    memoryState = next;
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(next));
    } catch (err) {
      console.warn('[tienda] No se pudo guardar la cotización en este navegador; se conserva mientras la página esté abierta.');
    }
    renderCount();
    if (avisar) document.dispatchEvent(new CustomEvent('vt:lista'));
  }

  /* Si el modelo ya está en la lista se queda la cantidad mayor (agregar 1 rollo no baja unos 120 m² ya elegidos). */
  function upsertItem(state, item) {
    const previo = state.items.find((it) => it.slug === item.slug);
    const items = previo
      ? state.items.map((it) => (it.slug === item.slug ? { ...it, m2: Math.max(it.m2, item.m2) } : it))
      : [...state.items, item];
    return { ...state, items };
  }

  function waLink(text) {
    return `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;
  }

  function estadoLabel(estado) {
    if (estado === PICKUP) return 'Lo recojo en el showroom de Cd. Madero';
    if (estado === LOCAL) return 'Envío local en Tampico, Madero o Altamira (según mi colonia)';
    return estado ? `Entrega en ${estado}` : '';
  }

  /* Último renglón del WhatsApp: "Folio web: T28-40-NL" (vt-folio.js). El cotizador de Netlify lo lee al pegar el
     mensaje y llena entrega, m² y modelos. Sin vt-folio.js o sin folio, no se agrega nada. */
  function folioDe(items, estado) {
    return window.VTFolio ? window.VTFolio.folio(items, estado) : '';
  }
  const folioLinea = (f) => (f ? `Folio web: ${f}` : '');

  const rollosTexto = (n) => `${n} rollo${n > 1 ? 's' : ''}`;

  /* Renglón de flete del mensaje: "Envío: 2 rollos · $2,300" (nunca gratis; se cobra por rollo según el estado). */
  function envioLinea(q) {
    return q && !q.error && q.zona ? `Envío: ${rollosTexto(q.rollos)} · ${money(q.envio)} (${ZONAS[q.zona].nombre}).` : '';
  }

  function listMessage(state) {
    const lines = ['Hola, quiero cotizar pasto sintético:'];
    let total = 0;
    let rollos = 0;
    let envio = 0;
    let zona = null;
    let complete = Boolean(state.estado);
    state.items.forEach((it) => {
      const q = quoteLine(it, it.m2, state.estado || PICKUP);
      lines.push(q.error
        ? `• ${it.nombre}: ${it.m2} m²`
        : `• ${it.nombre}: ${it.m2} m² · ${money(q.pm2)}/m² · material ${money(q.material)}`);
      if (q.error) { complete = false; return; }
      total += state.estado ? q.total : q.material;
      if (q.zona) { rollos += q.rollos; envio += q.envio; zona = q.zona; }
    });
    if (state.estado) lines.push(estadoLabel(state.estado) + '.');
    if (complete && zona) lines.push(envioLinea({ rollos, envio, zona }));
    if (complete && total > 0) lines.push(`Total estimado en la web: ${money(total)}.`);
    if (complete && total > 0) lines.push(planLine(total));
    lines.push('¿Me confirman el precio final con envío a mi dirección?');
    const f = folioLinea(folioDe(state.items, state.estado));
    if (f) lines.push(f);
    return lines.join('\n');
  }

  /* ---------- Count badge ---------- */
  function renderCount() {
    const n = memoryState.items.length;
    $$('[data-cot-count]').forEach((el) => {
      el.textContent = String(n);
      el.dataset.empty = String(n === 0);
    });
  }

  /* ---------- Toast ---------- */
  let toastTimer = null;

  const visible = (el) => {
    if (!el) return false;
    const st = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return st.display !== 'none' && st.visibility !== 'hidden' && r.height > 0 && r.top < innerHeight && r.bottom > 0;
  };

  /* Alto que ocupan abajo las barras fijas visibles (la de compra o la del shell). */
  function altoBarras() {
    return $$('#buybar[data-visible="true"], [data-vt-bar]').filter(visible)
      .reduce((max, el) => Math.max(max, innerHeight - el.getBoundingClientRect().top), 0);
  }

  /* El aviso va arriba de las barras fijas y nunca encima de los botones del cotizador: si chocaría con ellos, se
     coloca justo debajo (si cabe) o justo arriba de los botones. */
  function colocarAviso(toast) {
    const piso = altoBarras() + TOAST_GAP;
    const alto = toast.offsetHeight;
    let bottom = piso;
    const botones = $$('.vt-cotizador__acciones .vt-btn').filter(visible).map((b) => b.getBoundingClientRect());
    if (botones.length) {
      const arriba = Math.min(...botones.map((r) => r.top));
      const abajo = Math.max(...botones.map((r) => r.bottom));
      const topAviso = innerHeight - bottom - alto;
      const choca = topAviso < abajo + TOAST_GAP && innerHeight - bottom > arriba - TOAST_GAP;
      if (choca) {
        const debajo = innerHeight - (abajo + TOAST_GAP) - alto;
        bottom = debajo >= piso ? debajo : innerHeight - arriba + TOAST_GAP;
      }
    }
    toast.style.bottom = `${Math.round(bottom)}px`;
  }

  function showToast(message) {
    const toast = $('#toast');
    if (!toast) return;
    $('[data-toast-text]', toast).textContent = message;
    colocarAviso(toast);
    toast.dataset.visible = 'true';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.dataset.visible = 'false'; }, TOAST_MS);
  }

  /* ---------- Drawer ---------- */
  function renderDrawer() {
    const list = $('#cot-list');
    const foot = $('#cot-foot');
    if (!list || !foot) return;
    const { items, estado } = memoryState;
    list.replaceChildren();
    if (items.length === 0) {
      const empty = document.createElement('p');
      empty.className = 'drawer__empty';
      empty.innerHTML = 'Aún no agregas modelos. <a href="/pasto-sintetico#modelos">Ver los 9 modelos</a>.';
      list.append(empty);
      foot.hidden = true;
      return;
    }
    foot.hidden = false;
    let total = 0;
    let hasError = false;
    items.forEach((it) => {
      const q = quoteLine(it, it.m2, estado || PICKUP);
      if (q.error) hasError = true; else total += estado ? q.total : q.material;
      list.append(buildItemRow(it, q));
    });
    $('#cot-estado').value = estado;
    $('#cot-total').textContent = hasError ? 'Revisa los m²' : money(total);
    $('#cot-total-label').textContent = estado && !sinFleteNacional(estado) ? 'Total estimado con envío' : 'Total estimado del material';
    const send = $('#cot-send');
    send.href = waLink(listMessage(memoryState));
    send.setAttribute('aria-disabled', String(hasError));
  }

  function buildItemRow(it, q) {
    const row = document.createElement('div');
    row.className = 'cot-item';
    const img = document.createElement('img');
    img.src = it.img; img.alt = ''; img.width = 64; img.height = 64; img.loading = 'lazy';
    const body = document.createElement('div');
    const name = document.createElement('div');
    name.className = 'cot-item__name'; name.textContent = it.nombre;
    const meta = document.createElement('div');
    meta.className = 'cot-item__meta num';
    meta.textContent = q.error ? q.error : `${money(q.pm2)}/m² · material ${money(q.material)}`;
    const m2Wrap = document.createElement('label');
    m2Wrap.className = 'cot-item__m2';
    const input = document.createElement('input');
    input.type = 'number'; input.inputMode = 'numeric'; input.min = String(MIN_SHOWROOM_M2); input.max = String(MAX_M2);
    input.value = String(it.m2);
    input.setAttribute('aria-label', `Metros cuadrados de ${it.nombre}`);
    input.addEventListener('change', () => {
      const m2 = clampM2(parseInt(input.value, 10));
      writeStore({ ...memoryState, items: memoryState.items.map((x) => (x.slug === it.slug ? { ...x, m2 } : x)) });
      renderDrawer();
    });
    m2Wrap.append(input, document.createTextNode(' m²'));
    body.append(name, meta, m2Wrap);
    const remove = document.createElement('button');
    remove.type = 'button'; remove.className = 'cot-item__remove'; remove.textContent = 'Quitar';
    remove.addEventListener('click', () => {
      writeStore({ ...memoryState, items: memoryState.items.filter((x) => x.slug !== it.slug) });
      renderDrawer();
    });
    row.append(img, body, remove);
    return row;
  }

  function clampM2(n) {
    if (!Number.isFinite(n)) return MIN_NACIONAL_M2;
    return Math.min(MAX_M2, Math.max(MIN_SHOWROOM_M2, n));
  }

  function openDrawer() {
    const dlg = $('#cotizacion');
    if (!dlg || typeof dlg.showModal !== 'function') return;
    renderDrawer();
    dlg.showModal();
    track('view_cart', { items: memoryState.items.length });
  }

  function initDrawer() {
    const dlg = $('#cotizacion');
    if (!dlg) return;
    $$('[data-open-cot]').forEach((b) => b.addEventListener('click', openDrawer));
    $('#cot-close').addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
    fillEstados($('#cot-estado'));
    $('#cot-estado').addEventListener('change', (e) => {
      const value = e.target.value;
      writeStore({ ...memoryState, estado: value });
      renderDrawer();
      const quoteSel = $('#estado');
      if (quoteSel && quoteSel.value !== value) {
        quoteSel.value = value;
        quoteSel.dispatchEvent(new Event('change'));
      } else {
        document.dispatchEvent(new CustomEvent('vt:estado', { detail: { estado: value === PICKUP ? '' : value } }));
      }
    });
    $('#cot-send').addEventListener('click', (e) => {
      if (e.currentTarget.getAttribute('aria-disabled') === 'true') { e.preventDefault(); return; }
      leadWhatsapp('whatsapp_lista', 'lista', { items: memoryState.items.length });
    });
  }

  function fillEstados(select) {
    if (!select || select.options.length > 2 || 'local' in select.dataset) return;
    Object.keys(ESTADO_ZONA).sort((a, b) => a.localeCompare(b, 'es')).forEach((e) => {
      const opt = document.createElement('option');
      opt.value = e; opt.textContent = e;
      select.append(opt);
    });
  }

  /* ---------- Product data ---------- */
  function isValidModel(m) {
    return m && ['slug', 'nombre', 'img'].every((k) => typeof m[k] === 'string') &&
      ['t1', 't2', 'rollo'].every((k) => Number.isFinite(m[k]));
  }

  function readModels() {
    const many = $('#vt-models');
    const one = $('#vt-model');
    const el = many || one;
    if (!el) return [];
    try {
      const parsed = JSON.parse(el.textContent);
      const list = Array.isArray(parsed) ? parsed : [parsed];
      const valid = list.filter(isValidModel);
      if (valid.length !== list.length) throw new Error('hay modelos con campos faltantes');
      return valid;
    } catch (err) {
      console.error('[tienda] Datos de modelos inválidos:', err.message);
      return [];
    }
  }

  const normalizeSlug = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]/g, '');

  function addItem(model, m2) {
    const qty = clampM2(m2);
    const previo = memoryState.items.find((it) => it.slug === model.slug);
    writeStore(upsertItem(memoryState, {
      slug: model.slug, nombre: model.nombre, img: model.img, t1: model.t1, t2: model.t2, rollo: model.rollo, m2: qty,
    }));
    const queda = previo ? Math.max(previo.m2, qty) : qty;
    showToast(!previo ? `${model.nombre} · ${qty} m² en tu lista`
      : (queda === previo.m2 && qty !== previo.m2 ? `${model.nombre} ya está en tu lista con ${queda} m²`
        : `${model.nombre} actualizado a ${queda} m² en tu lista`));
    track('add_to_cart', { item_id: model.slug, quantity: qty });
  }

  /* Botones "+ Agregar" de la comparativa de la ficha: cada uno trae su modelo en data-agregar (JSON). */
  function initAgregar() {
    $$('[data-agregar]').forEach((btn) => btn.addEventListener('click', () => {
      try {
        const model = JSON.parse(btn.dataset.agregar);
        if (isValidModel(model)) addItem(model, ROLLO_M2);
        else console.error('[tienda] Botón de agregar sin precios completos:', btn.dataset.agregar);
      } catch (err) {
        console.error('[tienda] Botón de agregar con datos inválidos:', err.message);
      }
    }));
  }

  /* ---------- Quote module (ficha y hub) ---------- */
  function initQuote(models) {
    const inp = $('#m2');
    const sel = $('#estado');
    if (!inp || !sel || models.length === 0) return null;
    const modelSel = $('#modelo');
    fillEstados(sel);
    const hayOpcion = (v) => Array.from(sel.options).some((o) => o.value === v);
    if (memoryState.estado && hayOpcion(memoryState.estado)) sel.value = memoryState.estado;

    if (modelSel) {
      const wanted = normalizeSlug(new URLSearchParams(location.search).get('modelo'));
      const match = models.find((m) => normalizeSlug(m.slug) === wanted);
      if (match) modelSel.value = match.slug;
    }
    const current = () => (modelSel ? models.find((m) => m.slug === modelSel.value) : null) || models[0];

    const setM2 = (n) => { inp.value = String(clampM2(n)); tocar(); update(); };
    $('#m2-minus').addEventListener('click', () => setM2((parseInt(inp.value, 10) || MIN_NACIONAL_M2) - 5));
    $('#m2-plus').addEventListener('click', () => setM2((parseInt(inp.value, 10) || 0) + 5));
    $$('[data-m2]').forEach((chip) => chip.addEventListener('click', () => setM2(parseInt(chip.dataset.m2, 10))));
    inp.addEventListener('input', () => { tocar(); update(); });
    inp.addEventListener('change', () => setM2(parseInt(inp.value, 10)));
    sel.addEventListener('change', () => {
      writeStore({ ...memoryState, estado: sel.value });
      update();
      document.dispatchEvent(new CustomEvent('vt:estado', { detail: { estado: sinFleteNacional(sel.value) ? '' : sel.value } }));
    });
    if (modelSel) modelSel.addEventListener('change', () => { tocar(); update(); });

    $('#cta-add').addEventListener('click', () => addItem(current(), parseInt(inp.value, 10)));
    // La barra fija lleva el mismo mensaje del cotizador, pero se mide aparte (cta_id "<tipo>:barra").
    $$('[data-cta-wa]').forEach((a) => a.addEventListener('click', () => {
      leadWhatsapp('whatsapp_cotizador', a.closest('#buybar') ? 'barra' : 'cotizador',
        { item_id: current().slug, quantity: parseInt(inp.value, 10) || 0 });
    }));

    /* Con folio y entrega elegida: "Ya tienes todo listo…", el folio a la vista y el botón "Enviar mi cotización por
       WhatsApp". Sin folio, el botón vuelve a su texto del HTML. */
    const ctaWa = $$('[data-cta-wa]').find((a) => !a.closest('#buybar'));
    const ctaRotulo = ctaWa && ctaWa.lastChild && ctaWa.lastChild.nodeType === 3 ? ctaWa.lastChild : null;
    const ctaTexto = ctaRotulo ? ctaRotulo.nodeValue : '';
    function pintarFolio(f) {
      const caja = $('#q-folio');
      if (caja) {
        caja.hidden = !f;
        const cod = $('[data-folio]', caja);
        if (cod) cod.textContent = f;
      }
      if (ctaRotulo) ctaRotulo.nodeValue = f ? 'Enviar mi cotización por WhatsApp' : ctaTexto;
    }

    function renderModelPrices(model) {
      const price = $('#buy-price');
      if (price) price.textContent = money(model.rollo);
      [['rollo', model.rollo], ['t2', model.t2], ['t1', model.t1]].forEach(([k, v]) => {
        const cell = $(`#tier-${k}`);
        if (cell) cell.textContent = `${money(v)}/m²`;
      });
    }

    function update() {
      const model = current();
      renderModelPrices(model);
      const m2 = parseInt(inp.value, 10);
      const estado = sel.value;
      $$('[data-m2]').forEach((c) => c.setAttribute('aria-pressed', String(parseInt(c.dataset.m2, 10) === m2)));
      $$('[data-tier]').forEach((row) => { row.dataset.active = String(Number.isFinite(m2) && row.dataset.tier === tierFor(m2)); });

      const q = quoteLine(model, m2, estado || PICKUP);
      const nationalError = !estado || estado === PICKUP ? null : quoteLine(model, m2, estado).error;
      const error = nationalError || q.error || '';
      $('#q-error').textContent = error;
      $('#q-pm2').textContent = q.error ? '—' : `${money(q.pm2)}/m²`;
      $('#q-material').textContent = q.error ? '—' : money(q.material);

      const envioEl = $('#q-envio');
      const envioLabel = $('#q-envio-label');
      if (!estado) {
        envioLabel.textContent = 'Envío';
        envioEl.textContent = 'Elige tu estado';
      } else if (estado === LOCAL) {
        envioLabel.textContent = 'Envío local';
        envioEl.textContent = 'Según tu colonia';
      } else if (estado === PICKUP) {
        envioLabel.textContent = 'Recoger en showroom';
        envioEl.textContent = '$0';
      } else if (!error) {
        envioLabel.textContent = `Envío · ${q.rollos} rollo${q.rollos > 1 ? 's' : ''} · ${ZONAS[q.zona].nombre}`;
        envioEl.textContent = money(q.envio);
      } else {
        envioLabel.textContent = 'Envío';
        envioEl.textContent = '—';
      }

      const conFlete = Boolean(estado) && !sinFleteNacional(estado);
      $('#q-total').textContent = error ? '—' : money(estado ? q.total : q.material);
      $('#q-total-label').textContent = conFlete ? 'Total estimado con envío'
        : (estado === LOCAL ? 'Total del material' : 'Total estimado');
      $('#q-landed').textContent = !error && conFlete ? `≈ ${money(q.landed)} por m² puesto en tu domicilio` : '';
      const contado = error ? 0 : (conFlete ? q.total : q.material);
      renderPlans($('#q-plans'), contado);
      lastContado = contado;
      paintBuybarPlan();

      const faltan = ROLLO_M2 - m2;
      $('#q-hint').textContent = !error && m2 >= TIER2_MIN_M2 && faltan > 0
        ? `Con ${faltan} m² más llegas a rollo completo y pagas ${money(model.rollo)}/m² en lugar de ${money(model.t2)}/m².${conFlete ? ' El envío cuesta lo mismo.' : ''}`
        : '';

      const otros = memoryState.items.filter((it) => it.slug !== model.slug);
      const f = error ? '' : folioDe([{ slug: model.slug, m2 }, ...otros], estado);
      pintarFolio(estado ? f : '');
      const msg = [
        `Hola, quiero cotizar el pasto sintético ${model.nombre}.`,
        Number.isFinite(m2) && m2 > 0 ? `Necesito ${m2} m².` : '',
        otros.length ? `También en mi lista: ${otros.map((it) => `${it.nombre} (${it.m2} m²)`).join(', ')}.` : '',
        estado ? estadoLabel(estado) + '.' : '¿Me ayudan a calcular el envío a mi ciudad?',
        !error && conFlete ? envioLinea(q) : '',
        !error && estado ? `Total estimado en la web: ${money(conFlete ? q.total : q.material)}.` : '',
        contado ? planLine(contado) : '',
        '¿Me confirman el precio final?',
        folioLinea(f),
      ].filter(Boolean).join('\n');
      $$('[data-cta-wa]').filter((a) => !a.closest('#buybar')).forEach((a) => { a.href = waLink(msg); });
      mensajeCotizador = msg;
      pintarContexto();
    }

    update();
    initPlanInputs(update);
    // Lo que se agrega a la lista (tarjetas, vecinos, selector) viaja también en el mensaje del cotizador.
    document.addEventListener('vt:lista', update);
    return {
      selectModel(slug) {
        if (!modelSel || !models.some((m) => m.slug === slug)) return;
        modelSel.value = slug;
        update();
      },
    };
  }

  /* ---------- Gallery ---------- */
  function initGallery() {
    const track = $('#gal-track');
    if (!track) return;
    const slides = $$('.gallery__slide', track);
    const thumbs = $$('[data-gal-idx]');
    const counter = $('#gal-count');
    const setCurrent = (i) => {
      if (counter) counter.textContent = `${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      thumbs.forEach((t) => t.setAttribute('aria-current', String(parseInt(t.dataset.galIdx, 10) === i)));
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) setCurrent(slides.indexOf(en.target)); });
    }, { root: track, threshold: 0.6 });
    slides.forEach((s) => io.observe(s));
    thumbs.forEach((t) => t.addEventListener('click', () => {
      const target = slides[parseInt(t.dataset.galIdx, 10)];
      if (target) track.scrollTo({ left: target.offsetLeft, behavior: 'smooth' });
    }));
    setCurrent(0);
  }

  /* ---------- Barra fija con precio puesto ---------- */
  function paintBuybarLanded(estado) {
    const bar = $('#buybar[data-landed-bar]');
    if (!bar) return;
    const nameEl = $('.buybar__name', bar);
    const priceEl = $('.buybar__price', bar);
    if (!bar.dataset.baseName) {
      bar.dataset.baseName = nameEl.textContent;
      bar.dataset.basePrice = priceEl.textContent;
    }
    const zona = estado ? ESTADO_ZONA[estado] : null;
    const rollo = Number(bar.dataset.rollo);
    if (!zona || !(rollo > 0)) {
      nameEl.textContent = bar.dataset.baseName;
      priceEl.textContent = bar.dataset.basePrice;
      return;
    }
    nameEl.textContent = `Puesto en ${estado}`;
    priceEl.textContent = `Desde ${money(Math.round(rollo + ZONAS[zona].tarifa / ROLLO_M2))}/m² con envío`;
  }

  let lastContado = 0;
  function paintBuybarPlan() {
    const bar = $('#buybar');
    const info = bar && $('.buybar__info', bar);
    if (!info) return;
    const disp = window.VTMensualidades ? window.VTMensualidades.plazosDisponibles(lastContado) : [];
    let el = $('.buybar__plan', info);
    if (!el) {
      el = document.createElement('div');
      el.className = 'buybar__plan';
      info.appendChild(el);
    }
    el.textContent = disp.length ? `o hasta ${disp[disp.length - 1]} mensualidades con tarjeta` : '';
  }

  /* ---------- Sticky buy bar ---------- */
  /* Visible en celular desde que el CTA del hero sale de la pantalla hacia arriba, salvo mientras se ve el cotizador
     (#comprar), que tiene su propio botón (Entrega B de experiencia: antes solo aparecía pasado el cotizador). */
  function initBuybar() {
    const bar = $('#buybar');
    const anchor = $('#comprar');
    if (!bar || !anchor || !('IntersectionObserver' in window)) return;
    const hero = $('[data-hero-cta]');
    const vistos = new Map();
    const io = new IntersectionObserver((entradas) => {
      entradas.forEach((en) => vistos.set(en.target, en.isIntersecting));
      const heroArriba = !hero || (!vistos.get(hero) && hero.getBoundingClientRect().bottom < 0);
      bar.dataset.visible = String(heroArriba && !vistos.get(anchor));
    });
    io.observe(anchor);
    if (hero) io.observe(hero);
  }

  /* ---------- CTA según lo que ya eligió el cliente (Entrega B de experiencia) ----------
     La barra de compra (#buybar), el "Cotizar" del encabezado (window.VTBarra de terra.js) y, en el hub, el botón del
     hero llevan lo que el cliente ya hizo: con el cotizador usado, su mensaje; si no, con modelos en la lista, la lista
     completa; si no, el mensaje de la página con el estado elegido (y el modelo, en la ficha). */
  let mensajeCotizador = '';
  let tocado = false;
  function tocar() { tocado = true; }

  function modeloDeFicha() {
    try {
      const m = JSON.parse(($('#vt-model') || {}).textContent || 'null');
      return m && typeof m.nombre === 'string' ? m.nombre : '';
    } catch (err) {
      return '';
    }
  }

  const estadoElegido = () => (memoryState.estado && !sinFleteNacional(memoryState.estado) ? memoryState.estado : '');

  function mensajeBase(estado) {
    const nombre = modeloDeFicha();
    if (nombre) return `Hola, quiero cotizar el pasto sintético ${nombre}.\nMi estado: ${estado || '___'}\nMetros aprox.: ___`;
    if (!estado || !(estado in ESTADO_ZONA)) return '';
    return `Hola, quiero cotizar pasto sintético con envío a ${estado}.\nCiudad: ___\nMetros aprox.: ___\nModelo (si ya lo elegiste): ___`;
  }

  function contextoCta() {
    if (tocado && mensajeCotizador) return { href: waLink(mensajeCotizador), texto: 'Enviar mi cotización' };
    if (memoryState.items.length) return { href: waLink(listMessage(memoryState)), texto: 'Cotizar mi lista' };
    const base = mensajeBase(estadoElegido());
    return base ? { href: waLink(base), texto: '' } : null;
  }

  let ctaOriginal = null;
  function pintarContexto() {
    const bar = $('#buybar a[data-cta-wa]');
    const hero = $('.vt-portada-hub [data-hero-cta] a[href*="wa.me"]');
    const rotulo = bar && bar.lastChild && bar.lastChild.nodeType === 3 ? bar.lastChild : null;
    if (!ctaOriginal) {
      ctaOriginal = { bar: bar && bar.getAttribute('href'), barTexto: rotulo ? rotulo.nodeValue : '', hero: hero && hero.getAttribute('href') };
    }
    const ctx = contextoCta();
    if (bar) bar.setAttribute('href', ctx ? ctx.href : ctaOriginal.bar);
    if (rotulo) rotulo.nodeValue = (ctx && ctx.texto) || ctaOriginal.barTexto;
    // Las filas de WhatsApp de la tienda (data-vt-ctx) llevan el mismo mensaje; su texto no cambia.
    $$('[data-vt-ctx] a[href*="wa.me"]').forEach((a) => {
      if (!a.dataset.vtOriginal) a.dataset.vtOriginal = a.getAttribute('href');
      a.setAttribute('href', ctx ? ctx.href : a.dataset.vtOriginal);
    });
    // El hero del hub cambia solo con el estado elegido (reescritura 11); su texto no cambia.
    if (hero) {
      const base = mensajeBase(estadoElegido());
      hero.setAttribute('href', base ? waLink(base) : ctaOriginal.hero);
    }
    if (window.VTBarra) {
      if (ctx) window.VTBarra.prestar('tienda', ctx.href, ctx.texto);
      else window.VTBarra.soltar('tienda');
    }
  }

  function initToast() {
    const btn = $('#toast [data-open-cot]');
    if (btn) btn.addEventListener('click', () => { $('#toast').dataset.visible = 'false'; });
  }

  /* ?estado=<slug> (enlaces de las páginas de ciudad): la ficha abre con ese estado elegido, como el hub. */
  function estadoDesdeUrl() {
    const slug = new URLSearchParams(location.search).get('estado');
    if (!slug || !window.VTLanded) return;
    const estado = window.VTLanded.estadoDesdeSlug(slug, Object.keys(ESTADO_ZONA));
    if (estado && estado !== memoryState.estado) writeStore({ ...memoryState, estado }, false);
  }

  document.addEventListener('DOMContentLoaded', () => {
    estadoDesdeUrl();
    renderCount();
    initDrawer();
    initToast();
    initGallery();
    initBuybar();
    initAgregar();
    const models = readModels();
    const quote = initQuote(models);
    window.VTTienda = Object.freeze({
      models,
      zonas: Object.fromEntries(Object.entries(ZONAS).map(([z, v]) => [z, v.tarifa])),
      estadoZona: ESTADO_ZONA,
      getEstado: () => (memoryState.estado && !sinFleteNacional(memoryState.estado) ? memoryState.estado : ''),
      setEstado: (estado) => {
        if (estado && !(estado in ESTADO_ZONA)) return;
        writeStore({ ...memoryState, estado });
        const cotSel = $('#cot-estado');
        if (cotSel) cotSel.value = estado;
        if (typeof renderDrawer === 'function') renderDrawer();
        const sel = $('#estado');
        if (sel && sel.value !== estado) {
          sel.value = estado;
          sel.dispatchEvent(new Event('change'));
        } else {
          document.dispatchEvent(new CustomEvent('vt:estado', { detail: { estado } }));
        }
      },
      addItem: (slug, m2) => {
        const model = models.find((m) => m.slug === slug);
        if (model) addItem(model, m2);
      },
      selectModel: (slug) => { if (quote) quote.selectModel(slug); },
    });
    paintBuybarLanded(window.VTTienda.getEstado());
    document.addEventListener('vt:estado', (e) => { paintBuybarLanded((e.detail && e.detail.estado) || ''); pintarContexto(); });
    document.addEventListener('vt:lista', pintarContexto);
    pintarContexto();
    document.dispatchEvent(new CustomEvent('vt:ready'));
  });
})();
