/* Hub de pasto sintético · filtros del catálogo, selector de modelo y botones de agregar.
   Depende de window.VTTienda (tienda-pasto.js), que se publica en el evento vt:ready. */
(function () {
  'use strict';

  const DEFAULT_M2 = 50;
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  /* Pesos del selector: cada respuesta suma importancia a un atributo del modelo. */
  const WEIGHTS = {
    donde: { jardin: {}, terraza: { ligero: 3, alturaMax: 28 }, patio: { resistencia: 1 } },
    uso: {
      familia: { resistencia: 1.5 },
      perros: { resistencia: 2.5, alturaMax: 30 },
      poco: { resistencia: 0 },
      intenso: { resistencia: 3.5 },
    },
    prioridad: {
      equilibrio: { precio: 1.5, realismo: 1.5 },
      precio: { precio: 3, realismo: 0.5 },
      realismo: { precio: 0.3, realismo: 3 },
    },
  };
  const TIEBREAK = 'toscana-28';

  /* ---------- Filtros ---------- */
  function initFilters() {
    const chips = $$('[data-filter]');
    const cards = $$('.spec-card');
    const count = $('#filters-count');
    if (chips.length === 0) return;

    const apply = (key) => {
      let visible = 0;
      cards.forEach((card) => {
        const show = key === 'todos' || card.dataset.usos.split(' ').includes(key);
        card.hidden = !show;
        if (show) visible += 1;
      });
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.filter === key)));
      if (count) count.textContent = `${visible} modelo${visible === 1 ? '' : 's'}`;
      const url = new URL(location.href);
      if (key === 'todos') url.searchParams.delete('uso'); else url.searchParams.set('uso', key);
      history.replaceState(null, '', url);
    };

    chips.forEach((c) => c.addEventListener('click', () => apply(c.dataset.filter)));
    const initial = new URLSearchParams(location.search).get('uso');
    if (initial && chips.some((c) => c.dataset.filter === initial)) apply(initial);
  }

  /* ---------- Agregar desde el catálogo ---------- */
  function initCardButtons(api) {
    $$('[data-add]').forEach((btn) => btn.addEventListener('click', () => api.addItem(btn.dataset.add, DEFAULT_M2)));
  }

  /* ---------- Selector "¿cuál te conviene?" ---------- */
  function scoreModels(models, answers) {
    const w = { precio: 0, realismo: 0, resistencia: 0, ligero: 0, alturaMax: Infinity };
    Object.entries(answers).forEach(([group, value]) => {
      const add = (WEIGHTS[group] && WEIGHTS[group][value]) || {};
      Object.entries(add).forEach(([k, v]) => {
        w[k] = k === 'alturaMax' ? Math.min(w[k], v) : w[k] + v;
      });
    });
    return models
      .map((m) => {
        const s = m.scores || {};
        let score = (s.precio || 0) * w.precio + (s.realismo || 0) * w.realismo +
          (s.resistencia || 0) * w.resistencia + (s.ligero || 0) * w.ligero;
        if (m.mm > w.alturaMax) score -= 6;
        if (answers.uso === 'poco' && m.mm > 30) score -= 2;
        if (m.slug === TIEBREAK) score += 0.25;
        return { model: m, score };
      })
      .sort((a, b) => b.score - a.score)
      .map((r) => r.model);
  }

  function renderPick(model, label, primary) {
    const wrap = document.createElement('div');
    wrap.className = 'quiz__pick' + (primary ? ' quiz__pick--main' : '');
    const img = document.createElement('img');
    img.src = model.img; img.alt = ''; img.width = 96; img.height = 96; img.loading = 'lazy';
    const body = document.createElement('div');
    const small = document.createElement('p');
    small.className = 'quiz__label'; small.textContent = label;
    const name = document.createElement('a');
    name.className = 'quiz__name'; name.href = `/pasto-sintetico/${model.slug}`; name.textContent = model.nombre;
    const meta = document.createElement('p');
    meta.className = 'quiz__meta num';
    meta.textContent = `${model.tag} · ${model.mm} mm · desde $${model.rollo}/m²`;
    const actions = document.createElement('div');
    actions.className = 'quiz__actions';
    const quote = document.createElement('a');
    quote.className = 'btn btn--primary'; quote.href = '#cotizador'; quote.textContent = 'Cotizar este';
    quote.dataset.pick = model.slug;
    const add = document.createElement('button');
    add.type = 'button'; add.className = 'btn btn--ghost'; add.textContent = 'Agregar';
    add.dataset.add = model.slug;
    actions.append(quote, add);
    body.append(small, name, meta, actions);
    wrap.append(img, body);
    return wrap;
  }

  function initQuiz(api) {
    const form = $('#quiz');
    const out = $('#quiz-result');
    if (!form || !out) return;
    const run = () => {
      const data = new FormData(form);
      const answers = { donde: data.get('donde'), uso: data.get('uso'), prioridad: data.get('prioridad') };
      const [first, second] = scoreModels(api.models, answers);
      out.replaceChildren(renderPick(first, 'Te recomendamos', true), renderPick(second, 'También te puede servir', false));
      $$('[data-add]', out).forEach((b) => b.addEventListener('click', () => api.addItem(b.dataset.add, DEFAULT_M2)));
      $$('[data-pick]', out).forEach((a) => a.addEventListener('click', () => api.selectModel(a.dataset.pick)));
    };
    form.addEventListener('change', run);
    form.addEventListener('submit', (e) => e.preventDefault());
    run();
  }

  /* ---------- Precio puesto por estado ---------- */
  const money = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  let firstPaint = true;

  function landedFor(t, rollo, estado) {
    return window.VTLanded ? window.VTLanded.landedM2(rollo, estado, t.estadoZona, t.zonas) : null;
  }

  function paintLanded(t, estado) {
    const hero = $('[data-landed-hero]');
    if (hero) {
      const rollo = Number(hero.dataset.rollo);
      const v = estado ? landedFor(t, rollo, estado) : null;
      $('[data-landed-value]', hero).textContent = money(v || rollo);
      let note = '+ envío desde $900 por rollo. Elige tu estado para ver el precio puesto.';
      if (v) note = `puesto en ${estado}, envío incluido · llega en 3 a 5 días hábiles`;
      else if (estado && !window.VTLanded) note = '+ envío desde $900 por rollo. Te confirmamos el flete a tu estado.';
      $('[data-landed-note]', hero).textContent = note;
      if (!firstPaint) {
        hero.classList.remove('is-updating'); void hero.offsetWidth; hero.classList.add('is-updating');
      }
    }
    firstPaint = false;
    $$('[data-landed-slug]').forEach((el) => {
      const m = t.models.find((x) => x.slug === el.dataset.landedSlug);
      const v = m && estado ? landedFor(t, m.rollo, estado) : null;
      el.textContent = v ? `· ${money(v)}/m² puesto en ${estado}` : '';
    });
    const sel = $('#hero-estado');
    if (sel && sel.value !== estado) sel.value = estado;
    paintComparador(t, estado);
  }

  function estadoInicial(t) {
    const slug = new URLSearchParams(location.search).get('estado');
    const desdeUrl = slug && window.VTLanded ? window.VTLanded.estadoDesdeSlug(slug, Object.keys(t.estadoZona)) : null;
    return desdeUrl || t.getEstado();
  }

  function initLanded(t) {
    const sel = $('#hero-estado');
    const inicial = estadoInicial(t);
    if (inicial && inicial !== t.getEstado()) t.setEstado(inicial);
    paintLanded(t, inicial);
    if (sel) sel.addEventListener('change', () => t.setEstado(sel.value));
    document.addEventListener('vt:estado', (e) => paintLanded(t, e.detail.estado || ''));
  }

  /* ---------- Comparador ---------- */
  function paintComparador(t, estado) {
    const out = $('#cmp-out');
    if (!out) return;
    const total = Number($('#cmp-total').value);
    const m2 = Number($('#cmp-m2').value);
    const valido = Number.isFinite(total) && total > 0 && Number.isFinite(m2) && m2 > 0;
    if (!t.models || !t.models.length || !valido) {
      out.textContent = 'Escribe el total y los metros para comparar con nuestro precio puesto en tu estado.';
      return;
    }
    const suyo = total / m2;
    const barato = t.models.reduce((a, b) => (a.rollo <= b.rollo ? a : b));
    const nuestro = estado ? landedFor(t, barato.rollo, estado) : null;
    out.textContent = nuestro
      ? `Esa oferta sale en ${money(suyo)}/m². Con nosotros, desde ${money(nuestro)}/m² puesto en ${estado} (${barato.nombre}).`
      : `Esa oferta sale en ${money(suyo)}/m². Elige tu estado arriba para comparar con nuestro precio puesto.`;
  }

  function initComparador(t) {
    ['#cmp-total', '#cmp-m2'].forEach((id) => {
      const el = $(id);
      if (el) el.addEventListener('input', () => paintComparador(t, t.getEstado()));
    });
  }

  function start() {
    const api = window.VTTienda;
    initFilters();
    if (!api) {
      console.error('[tienda-hub] VTTienda no está disponible; el selector y los botones de agregar quedan inactivos.');
      return;
    }
    initCardButtons(api);
    initQuiz(api);
    initLanded(api);
    initComparador(api);
  }

  if (window.VTTienda) start();
  else document.addEventListener('vt:ready', start, { once: true });
})();
