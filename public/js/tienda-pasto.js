/* Tienda de pasto sintético · Viveros Terra
   Cotizador por estado, lista de cotización (localStorage) y envío por WhatsApp. */
(function () {
  'use strict';

  const WA_NUMBER = '528333268008';
  const STORE_KEY = 'vt-cotizacion-v1';
  const ROLLO_M2 = 50;
  const TIER2_MIN_M2 = 10;
  const MIN_NACIONAL_M2 = 25;
  const MIN_SHOWROOM_M2 = 2;
  const MAX_M2 = 5000;
  const PICKUP = 'showroom';
  const TOAST_MS = 4000;

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

  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params);
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

  function quoteLine(model, m2, estado) {
    const isPickup = estado === PICKUP;
    const min = isPickup ? MIN_SHOWROOM_M2 : MIN_NACIONAL_M2;
    if (!Number.isFinite(m2) || m2 < min) {
      return { error: isPickup
        ? `En showroom vendemos desde ${MIN_SHOWROOM_M2} m².`
        : `Para envío nacional el mínimo es ${MIN_NACIONAL_M2} m² (medio rollo).` };
    }
    const pm2 = precioM2(model, m2);
    const material = pm2 * m2;
    const rollos = Math.ceil(m2 / ROLLO_M2);
    const zona = isPickup ? null : ESTADO_ZONA[estado] || null;
    const envio = zona ? ZONAS[zona].tarifa * rollos : 0;
    return { pm2, material, rollos, zona, envio, isPickup, total: material + envio, landed: (material + envio) / m2 };
  }

  /* ---------- Quote list storage ---------- */
  function readStore() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
      const items = Array.isArray(raw.items) ? raw.items.filter(isValidItem) : [];
      return { items, estado: typeof raw.estado === 'string' ? raw.estado : '' };
    } catch (err) {
      return { items: [], estado: '' };
    }
  }

  function isValidItem(it) {
    return it && typeof it.slug === 'string' && typeof it.nombre === 'string' &&
      Number.isFinite(it.m2) && Number.isFinite(it.rollo) && Number.isFinite(it.t2) && Number.isFinite(it.t1);
  }

  let memoryState = readStore();

  function writeStore(next) {
    memoryState = next;
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(next));
    } catch (err) {
      console.warn('[tienda] No se pudo guardar la cotización en este navegador; se conserva mientras la página esté abierta.');
    }
    renderCount();
  }

  function upsertItem(state, item) {
    const exists = state.items.some((it) => it.slug === item.slug);
    const items = exists
      ? state.items.map((it) => (it.slug === item.slug ? { ...it, m2: item.m2 } : it))
      : [...state.items, item];
    return { ...state, items };
  }

  function waLink(text) {
    return `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;
  }

  function estadoLabel(estado) {
    if (estado === PICKUP) return 'Lo recojo en el showroom de Cd. Madero';
    return estado ? `Entrega en ${estado}` : '';
  }

  function listMessage(state) {
    const lines = ['Hola, quiero cotizar pasto sintético:'];
    let total = 0;
    let complete = Boolean(state.estado);
    state.items.forEach((it) => {
      const q = quoteLine(it, it.m2, state.estado || PICKUP);
      lines.push(`• ${it.nombre}: ${it.m2} m²`);
      if (q.error) complete = false; else total += state.estado ? q.total : q.material;
    });
    if (state.estado) lines.push(estadoLabel(state.estado) + '.');
    if (complete && total > 0) lines.push(`Total estimado en la web: ${money(total)}.`);
    lines.push('¿Me confirman el precio final con envío a mi dirección?');
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
  function showToast(message) {
    const toast = $('#toast');
    if (!toast) return;
    $('[data-toast-text]', toast).textContent = message;
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
    $('#cot-total-label').textContent = estado && estado !== PICKUP ? 'Total estimado con envío' : 'Total estimado del material';
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
      writeStore({ ...memoryState, estado: e.target.value });
      renderDrawer();
    });
    $('#cot-send').addEventListener('click', (e) => {
      if (e.currentTarget.getAttribute('aria-disabled') === 'true') { e.preventDefault(); return; }
      track('generate_lead', { method: 'whatsapp_lista', items: memoryState.items.length });
    });
  }

  function fillEstados(select) {
    if (!select || select.options.length > 2) return;
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
    writeStore(upsertItem(memoryState, {
      slug: model.slug, nombre: model.nombre, img: model.img, t1: model.t1, t2: model.t2, rollo: model.rollo, m2: qty,
    }));
    showToast(`${model.nombre} · ${qty} m² en tu cotización`);
    track('add_to_cart', { item_id: model.slug, quantity: qty });
  }

  /* ---------- Quote module (ficha y hub) ---------- */
  function initQuote(models) {
    const inp = $('#m2');
    const sel = $('#estado');
    if (!inp || !sel || models.length === 0) return null;
    const modelSel = $('#modelo');
    fillEstados(sel);
    if (memoryState.estado) sel.value = memoryState.estado;

    if (modelSel) {
      const wanted = normalizeSlug(new URLSearchParams(location.search).get('modelo'));
      const match = models.find((m) => normalizeSlug(m.slug) === wanted);
      if (match) modelSel.value = match.slug;
    }
    const current = () => (modelSel ? models.find((m) => m.slug === modelSel.value) : null) || models[0];

    const setM2 = (n) => { inp.value = String(clampM2(n)); update(); };
    $('#m2-minus').addEventListener('click', () => setM2((parseInt(inp.value, 10) || MIN_NACIONAL_M2) - 5));
    $('#m2-plus').addEventListener('click', () => setM2((parseInt(inp.value, 10) || 0) + 5));
    $$('[data-m2]').forEach((chip) => chip.addEventListener('click', () => setM2(parseInt(chip.dataset.m2, 10))));
    inp.addEventListener('input', update);
    inp.addEventListener('change', () => setM2(parseInt(inp.value, 10)));
    sel.addEventListener('change', () => { writeStore({ ...memoryState, estado: sel.value }); update(); });
    if (modelSel) modelSel.addEventListener('change', update);

    $('#cta-add').addEventListener('click', () => addItem(current(), parseInt(inp.value, 10)));
    $$('[data-cta-wa]').forEach((a) => a.addEventListener('click', () => {
      track('generate_lead', { method: 'whatsapp_cotizador', item_id: current().slug, quantity: parseInt(inp.value, 10) || 0 });
    }));

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
      } else if (estado === PICKUP) {
        envioLabel.textContent = 'Recoger en showroom';
        envioEl.textContent = 'Sin costo';
      } else if (!error) {
        envioLabel.textContent = `Envío · ${q.rollos} rollo${q.rollos > 1 ? 's' : ''} · ${ZONAS[q.zona].nombre}`;
        envioEl.textContent = money(q.envio);
      } else {
        envioLabel.textContent = 'Envío';
        envioEl.textContent = '—';
      }

      $('#q-total').textContent = error ? '—' : money(estado ? q.total : q.material);
      $('#q-total-label').textContent = estado && estado !== PICKUP ? 'Total estimado con envío' : 'Total estimado';
      $('#q-landed').textContent = !error && estado && estado !== PICKUP
        ? `≈ ${money(q.landed)} por m² puesto en tu domicilio` : '';

      const faltan = ROLLO_M2 - m2;
      $('#q-hint').textContent = !error && m2 >= TIER2_MIN_M2 && faltan > 0
        ? `Con ${faltan} m² más llegas a rollo completo y pagas ${money(model.rollo)}/m² en lugar de ${money(model.t2)}/m². El envío cuesta lo mismo.`
        : '';

      const msg = [
        `Hola, quiero cotizar el pasto sintético ${model.nombre}.`,
        Number.isFinite(m2) ? `Necesito ${m2} m².` : '',
        estado ? estadoLabel(estado) + '.' : '¿Me ayudan a calcular el envío a mi ciudad?',
        !error && estado ? `Total estimado en la web: ${money(estado === PICKUP ? q.material : q.total)}.` : '',
        '¿Me confirman el precio final?',
      ].filter(Boolean).join('\n');
      $$('[data-cta-wa]').forEach((a) => { a.href = waLink(msg); });
    }

    update();
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

  /* ---------- Sticky buy bar ---------- */
  function initBuybar() {
    const bar = $('#buybar');
    const anchor = $('#comprar');
    if (!bar || !anchor) return;
    const io = new IntersectionObserver(([en]) => {
      bar.dataset.visible = String(!en.isIntersecting && en.boundingClientRect.top < 0);
    });
    io.observe(anchor);
  }

  function initToast() {
    const btn = $('#toast [data-open-cot]');
    if (btn) btn.addEventListener('click', () => { $('#toast').dataset.visible = 'false'; });
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderCount();
    initDrawer();
    initToast();
    initGallery();
    initBuybar();
    const models = readModels();
    const quote = initQuote(models);
    window.VTTienda = Object.freeze({
      models,
      addItem: (slug, m2) => {
        const model = models.find((m) => m.slug === slug);
        if (model) addItem(model, m2);
      },
      selectModel: (slug) => { if (quote) quote.selectModel(slug); },
    });
    document.dispatchEvent(new CustomEvent('vt:ready'));
  });
})();
