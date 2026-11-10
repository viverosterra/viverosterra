/* Viveros Terra · vt-catalogo.js · "Arma tu lista" del catálogo (Etapa 2e).
   - Filtra la rejilla, que ya viene en el HTML, con el buscador y los botones de filtro. El estado vive en la URL
     (?q=&cat=&luz=&tam=&riego=&uso=): el hub enlaza filtros (/catalogo?luz=sol) y la búsqueda se puede compartir.
   - Arma la lista con <dialog>: tamaño (o medida especial) y piezas por especie. La misma especie con el mismo tamaño
     actualiza la cantidad, como confirmAdd() de main. La lista es [{name, sc, sz, qty}].
   - El enlace "Cotizar por WhatsApp" de la lista lleva un solo mensaje, el mismo que armaba sendWA() en main (casos en
     public/js/tests/casos-catalogo.json), con data-cta="catalogo:sendWA": terra.js lo mide (generate_lead con el mismo
     cta_id que VTMedicion.whatsapp('sendWA') de main) y lo firma al hacer clic. Sin window.open.
   - La lista se guarda en sessionStorage en cada pintar() y vuelve al recargar o al regresar de otra página, solo con
     especies de #vt-catalogo-datos (validarLista). Con la lista llena, la barra fija ("Cotizar mi lista", directo, sin
     abrir la lista) y el "Cotizar" de la cabecera llevan el mismo mensaje de la lista (window.VTBarra de terra.js; se
     siguen midiendo como <tipo>:barra y <tipo>:header), y el botón "Mi lista · n variedades · n piezas" abre la lista.
     Las filas de WhatsApp entre las tarjetas ([data-vt-cta-rejilla]) también la mandan, y con filtros solo se ve una
     cada CADA_FILA tarjetas visibles.
   - /catalogo?q=<nombre>&add=<slug> (el "Agregar en Arma tu lista" de las subcategorías) abre el diálogo de esa especie;
     un slug desconocido se ignora.
   El texto de las especies llega del HTML (data-*) y de #vt-catalogo-datos; nunca se usa innerHTML.
   Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const WA = 'https://wa.me/528333268008?text=';
  const GRUPOS = ['cat', 'luz', 'tam', 'riego', 'uso'];
  const MAXIMO = 9999;
  const OTRO = '__otro__';
  const CLAVE = 'vt-catalogo-lista';
  const PULSO_MS = 200;
  const MAX_ITEMS = 200;
  const MAX_TAMANO = 60; // maxlength del campo "Otro tamaño o medida especial"
  const CADA_FILA = 12; // tarjetas visibles entre dos filas de WhatsApp (≈ 4 pantallas del celular; múltiplo de 2, 3 y 4 columnas)

  function normalizar(texto) {
    return String(texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/\s+/g, ' ').trim();
  }

  function leerFiltros(search) {
    const p = new URLSearchParams(search || '');
    const f = { q: p.get('q') || '' };
    GRUPOS.forEach((g) => { f[g] = (p.get(g) || '').split(',').map((v) => v.trim()).filter(Boolean); });
    return f;
  }

  function escribirFiltros(f) {
    const partes = f.q ? ['q=' + encodeURIComponent(f.q)] : [];
    GRUPOS.forEach((g) => { if (f[g] && f[g].length) partes.push(g + '=' + f[g].map(encodeURIComponent).join(',')); });
    return partes.length ? '?' + partes.join('&') : '';
  }

  function hayFiltros(f) {
    return Boolean(f.q) || GRUPOS.some((g) => f[g].length > 0);
  }

  // d: dataset de la tarjeta. Dentro de un grupo basta una opción; entre grupos, todas (catalogo_datos.coincide).
  function coincide(d, f) {
    const enGrupos = GRUPOS.every((g) => {
      if (!f[g] || !f[g].length) return true;
      const valores = String(d[g] || '').split(' ');
      return f[g].some((v) => valores.indexOf(v) >= 0);
    });
    if (!enGrupos) return false;
    const q = normalizar(f.q);
    return !q || q.split(' ').every((palabra) => String(d.buscar || '').indexOf(palabra) >= 0);
  }

  function contarFiltros(f) {
    return GRUPOS.reduce((n, g) => n + (f[g] ? f[g].length : 0), 0);
  }

  function cantidad(valor) {
    return Math.max(1, Math.min(MAXIMO, parseInt(valor, 10) || 1));
  }

  function agregar(lista, item) {
    const i = lista.findIndex((x) => x.name === item.name && x.sz === item.sz);
    if (i >= 0) return lista.map((x, j) => (j === i ? { ...x, qty: item.qty } : x));
    return [...lista, item];
  }

  function cambiar(lista, i, delta) {
    return lista.map((x, j) => (j === i ? { ...x, qty: cantidad(x.qty + delta) } : x));
  }

  function quitar(lista, i) {
    return lista.filter((_x, j) => j !== i);
  }

  function enLista(lista, nombre) {
    return lista.some((x) => x.name === nombre);
  }

  // Lo guardado en sessionStorage no es de fiar: solo pasan renglones de especies del catálogo (mismo nombre y mismo
  // científico), con tamaño de texto corto y cantidad entera de 1 a 9999; los repetidos se juntan como en agregar().
  function validarLista(guardada, especies) {
    if (!Array.isArray(guardada) || !especies || typeof especies !== 'object') return [];
    const conocidas = new Map(Object.keys(especies).map((k) => [especies[k].name, especies[k].sc]));
    return guardada
      .filter((x) => x && typeof x === 'object' && typeof x.name === 'string' && conocidas.has(x.name)
        && x.sc === conocidas.get(x.name) && typeof x.sz === 'string' && x.sz.trim() !== ''
        && x.sz.length <= MAX_TAMANO && Number.isInteger(x.qty) && x.qty >= 1 && x.qty <= MAXIMO)
      .slice(0, MAX_ITEMS)
      .reduce((lista, x) => agregar(lista, { name: x.name, sc: x.sc, sz: x.sz.trim(), qty: x.qty }), []);
  }

  // storage puede faltar o lanzar (modo privado, cuota llena, cookies bloqueadas): la lista sigue en memoria.
  function guardarLista(storage, lista) {
    try {
      storage.setItem(CLAVE, JSON.stringify(lista));
      return true;
    } catch (_e) {
      return false;
    }
  }

  function leerLista(storage, especies) {
    try {
      return validarLista(JSON.parse(storage.getItem(CLAVE) || '[]'), especies);
    } catch (_e) {
      return [];
    }
  }

  function almacen(win) {
    try {
      return win.sessionStorage;
    } catch (_e) {
      return null;
    }
  }

  function plural(n, uno, varios) {
    return n + ' ' + (n === 1 ? uno : varios);
  }

  function resumen(lista) {
    const total = lista.reduce((s, i) => s + i.qty, 0);
    return plural(lista.length, 'variedad', 'variedades') + ' · ' + plural(total, 'pieza', 'piezas');
  }

  // Reescritura 7 (Entrega B de experiencia): la colonia de entrega por llenar antes de la pregunta, que es más corta.
  const COLONIA = 'Colonia de entrega: ___';
  const PREGUNTA = '¿Me dan precio y disponibilidad?';
  function mensajeLista(lista) {
    if (!lista.length) return '';
    const lineas = lista.map((i) => `• ${i.name} (${i.sz}) × ${i.qty}`).join('\n');
    const total = lista.reduce((s, i) => s + i.qty, 0);
    return `Hola Viveros Terra\n\nQuisiera cotizar lo siguiente:\n\n${lineas}\n\nTotal: ${lista.length} variedad${lista.length > 1 ? 'es' : ''}, ${total} unidad${total > 1 ? 'es' : ''}\n${COLONIA}\n\n${PREGUNTA}`;
  }

  function enlaceLista(lista) {
    return WA + encodeURIComponent(mensajeLista(lista));
  }

  function mensajeEspecial(texto) {
    const valor = String(texto || '').trim() || '___';
    return 'Hola Viveros Terra\n\nBusco: *' + valor + '*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?';
  }

  // ---------- DOM ----------
  // Una fila de WhatsApp entre las tarjetas solo si la preceden CADA_FILA tarjetas visibles desde la anterior y le
  // sigue alguna: con filtros no se juntan filas seguidas ni queda una al final.
  function repartirFilas(rejilla) {
    let desde = 0;
    let pendiente = null;
    Array.from(rejilla.children).forEach((el) => {
      if (el.hasAttribute('data-vt-cta-rejilla')) {
        el.hidden = true;
        if (desde >= CADA_FILA) pendiente = el;
        return;
      }
      if (el.hidden) return;
      if (pendiente) { pendiente.hidden = false; pendiente = null; desde = 0; }
      desde += 1;
    });
  }

  function filtrar(doc, win) {
    const caja = doc.querySelector('[data-vt-filtros]');
    const rejilla = doc.querySelector('[data-vt-rejilla]');
    if (!caja || !rejilla) return;
    const tarjetas = Array.from(rejilla.querySelectorAll('[data-vt-esp]'));
    const q = caja.querySelector('input[type="search"]');
    const botones = Array.from(caja.querySelectorAll('[data-vt-g]'));
    const cuenta = caja.querySelector('[data-vt-o="cuenta"]');
    const limpiar = caja.querySelector('[data-vt-limpiar]');
    const vacio = doc.querySelector('[data-vt-vacio]');
    const vacioWa = vacio && vacio.querySelector('[data-vt-o="vacio-wa"]');
    const nFiltros = caja.querySelector('[data-vt-o="n-filtros"]');
    const especial = doc.getElementById('vt-especial-q');
    let filtros = leerFiltros(win.location.search);

    function aplicar(escribir) {
      let visibles = 0;
      tarjetas.forEach((t) => {
        const ok = coincide(t.dataset, filtros);
        t.hidden = !ok;
        if (ok) visibles += 1;
      });
      cuenta.textContent = plural(visibles, 'especie', 'especies');
      repartirFilas(rejilla);
      if (vacio) vacio.hidden = visibles > 0;
      if (!visibles) sinResultados();
      if (nFiltros) nFiltros.textContent = contarFiltros(filtros) ? ' (' + contarFiltros(filtros) + ')' : '';
      limpiar.hidden = !hayFiltros(filtros);
      botones.forEach((b) => b.setAttribute('aria-pressed', String(filtros[b.dataset.vtG].indexOf(b.dataset.vtV) >= 0)));
      if (escribir) win.history.replaceState(null, '', win.location.pathname + escribirFiltros(filtros));
    }

    // Sin resultados: el WhatsApp lleva lo buscado y el campo de "¿No está?" queda con el mismo texto.
    function sinResultados() {
      if (vacioWa) vacioWa.setAttribute('href', WA + encodeURIComponent(mensajeEspecial(filtros.q)));
      if (especial && filtros.q.trim()) {
        especial.value = filtros.q.trim();
        especial.dispatchEvent(new win.Event('input'));
      }
    }

    caja.addEventListener('submit', (e) => e.preventDefault());
    q.addEventListener('input', () => { filtros = { ...filtros, q: q.value }; aplicar(true); });
    botones.forEach((b) => b.addEventListener('click', () => {
      const g = b.dataset.vtG;
      const v = b.dataset.vtV;
      const activos = filtros[g].indexOf(v) >= 0 ? filtros[g].filter((x) => x !== v) : [...filtros[g], v];
      filtros = { ...filtros, [g]: activos };
      aplicar(true);
    }));
    limpiar.addEventListener('click', () => { filtros = leerFiltros(''); q.value = ''; aplicar(true); q.focus(); });
    q.value = filtros.q;
    aplicar(false);
  }

  function fila(doc, it, i) {
    const li = doc.createElement('li');
    const texto = doc.createElement('p');
    texto.className = 'vt-lista__item';
    const nombre = doc.createElement('b');
    nombre.textContent = it.name;
    texto.append(nombre, ' · ' + it.sz);
    const ctrl = doc.createElement('p');
    ctrl.className = 'vt-lista__ctrl';
    const boton = (accion, visible, etiqueta) => {
      const b = doc.createElement('button');
      b.type = 'button';
      b.dataset.accion = accion;
      b.dataset.i = String(i);
      b.textContent = visible;
      b.setAttribute('aria-label', etiqueta);
      return b;
    };
    const n = doc.createElement('span');
    n.textContent = String(it.qty);
    ctrl.append(boton('menos', '−', 'Una pieza menos de ' + it.name), n, boton('mas', '+', 'Una pieza más de ' + it.name),
      boton('quitar', 'Quitar', 'Quitar ' + it.name + ' de la lista'));
    li.append(texto, ctrl);
    return li;
  }

  function armarLista(doc, win) {
    const fuente = doc.getElementById('vt-catalogo-datos');
    const dAgregar = doc.getElementById('vt-agregar');
    const dLista = doc.getElementById('vt-lista');
    const abrirLista = doc.querySelector('[data-vt-abrir-lista]');
    if (!fuente || !dAgregar || !dLista || !abrirLista || typeof dAgregar.showModal !== 'function') return;
    let especies;
    try {
      especies = JSON.parse(fuente.textContent);
    } catch (_e) {
      return; // sin datos válidos la rejilla sigue visible y filtrable; solo no se arma la lista
    }
    const sel = dAgregar.querySelector('[data-vt-campo="tam"]');
    const otro = dAgregar.querySelector('[data-vt-campo="otro"]');
    const cajaOtro = dAgregar.querySelector('[data-vt-otro]');
    const n = dAgregar.querySelector('[data-vt-campo="n"]');
    const enviar = dLista.querySelector('[data-vt-o="enviar"]');
    const items = dLista.querySelector('[data-vt-o="items"]');
    const aviso = doc.querySelector('[data-vt-o="aviso"]');
    const botones = Array.from(doc.querySelectorAll('[data-vt-agregar]'));
    const filas = Array.from(doc.querySelectorAll('[data-vt-cta-rejilla] a[href*="wa.me"]'));
    filas.forEach((a) => { a.dataset.vtOriginal = a.getAttribute('href'); });
    const store = almacen(win);
    const conocida = (slug) => Object.prototype.hasOwnProperty.call(especies, slug);
    let seleccion = leerLista(store, especies);
    let actual = null;
    let origen = null;

    function marcar(b) {
      const e = especies[b.dataset.vtAgregar];
      const en = Boolean(e) && enLista(seleccion, e.name);
      if (b.dataset.vtEn === String(en)) return;
      b.dataset.vtEn = String(en);
      b.classList.toggle('vt-cat__add--en', en);
      const texto = doc.createElement('span');
      const nombre = doc.createElement('span');
      nombre.className = 'vt-sr';
      nombre.textContent = ' ' + (e ? e.name : '');
      if (en) texto.append('✓ En tu lista · editar', nombre);
      else texto.append('+ Añadir', nombre, ' a mi lista');
      b.replaceChildren(texto);
    }

    function pulso() {
      if (typeof win.requestAnimationFrame !== 'function') return;
      abrirLista.classList.remove('vt-pulso');
      win.requestAnimationFrame(() => {
        abrirLista.classList.add('vt-pulso');
        win.setTimeout(() => abrirLista.classList.remove('vt-pulso'), PULSO_MS);
      });
    }

    function pintar() {
      abrirLista.hidden = seleccion.length === 0;
      abrirLista.querySelector('[data-vt-o="cuenta-lista"]').textContent = String(seleccion.length);
      const detalle = abrirLista.querySelector('[data-vt-o="resumen-barra"]');
      if (detalle) detalle.textContent = seleccion.length ? resumen(seleccion) : '';
      dLista.querySelector('[data-vt-o="resumen"]').textContent = seleccion.length ? resumen(seleccion) : 'Tu lista está vacía.';
      enviar.hidden = seleccion.length === 0;
      enviar.setAttribute('href', enlaceLista(seleccion));
      items.replaceChildren(...seleccion.map((it, i) => fila(doc, it, i)));
      botones.forEach(marcar);
      filas.forEach((a) => a.setAttribute('href', seleccion.length ? enlaceLista(seleccion) : a.dataset.vtOriginal));
      if (win.VTBarra) {
        if (seleccion.length) win.VTBarra.prestar('catalogo', enlaceLista(seleccion), 'Cotizar mi lista');
        else win.VTBarra.soltar('catalogo');
      }
      guardarLista(store, seleccion);
    }

    function abrirAgregar(b) {
      actual = especies[b.dataset.vtAgregar];
      origen = b;
      const previo = seleccion.find((x) => x.name === actual.name);
      dAgregar.querySelector('[data-vt-o="nombre"]').textContent = actual.name;
      dAgregar.querySelector('[data-vt-o="sci"]').textContent = actual.sc;
      sel.replaceChildren(...actual.sz.map((t) => new win.Option(t, t)), new win.Option('Otro tamaño o medida especial', OTRO));
      sel.value = previo && actual.sz.indexOf(previo.sz) >= 0 ? previo.sz : actual.sz[0];
      n.value = String(previo ? previo.qty : 1);
      otro.value = '';
      cajaOtro.hidden = true;
      dAgregar.returnValue = '';
      dAgregar.showModal();
      sel.focus();
    }

    doc.addEventListener('click', (e) => {
      const b = e.target.closest ? e.target.closest('[data-vt-agregar]') : null;
      if (b && conocida(b.dataset.vtAgregar)) abrirAgregar(b);
    });
    sel.addEventListener('change', () => { cajaOtro.hidden = sel.value !== OTRO; if (!cajaOtro.hidden) otro.focus(); });
    dAgregar.querySelector('[data-vt-menos]').addEventListener('click', () => { n.value = String(cantidad(cantidad(n.value) - 1)); });
    dAgregar.querySelector('[data-vt-mas]').addEventListener('click', () => { n.value = String(cantidad(cantidad(n.value) + 1)); });
    // El envío del <form method="dialog"> llega antes que el evento close (que va en cola): la lista se actualiza aquí,
    // en el mismo turno del clic o del Enter, y close solo devuelve el foco.
    dAgregar.querySelector('form').addEventListener('submit', (e) => {
      if (!actual || (e.submitter && e.submitter.value !== 'agregar')) return;
      const sz = sel.value === OTRO ? (otro.value.trim() || 'Medida especial') : sel.value;
      const qty = cantidad(n.value);
      seleccion = agregar(seleccion, { name: actual.name, sc: actual.sc, sz, qty });
      pintar();
      pulso();
      aviso.textContent = 'Agregaste ' + actual.name + ' (' + sz + ') × ' + qty + '. Llevas ' + resumen(seleccion) + '.';
    });
    dAgregar.querySelector('[data-vt-cancelar]').addEventListener('click', () => dAgregar.close('cancelar'));
    // close va en cola: si el diálogo ya se volvió a abrir (Enter rápido sobre el mismo botón), no se toca la selección.
    dAgregar.addEventListener('close', () => {
      if (dAgregar.open) return;
      actual = null;
      if (origen) origen.focus();
    });
    abrirLista.addEventListener('click', () => { pintar(); dLista.showModal(); });
    dLista.querySelectorAll('[data-vt-cerrar]').forEach((b) => b.addEventListener('click', () => dLista.close()));
    dLista.querySelector('[data-vt-vaciar]').addEventListener('click', () => {
      if (typeof win.confirm === 'function' && !win.confirm('¿Vaciar tu lista? Se quitan todas las plantas.')) return;
      seleccion = [];
      pintar();
      dLista.close();
    });
    items.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-accion]');
      if (!b) return;
      const i = Number(b.dataset.i);
      seleccion = b.dataset.accion === 'quitar' ? quitar(seleccion, i) : cambiar(seleccion, i, b.dataset.accion === 'mas' ? 1 : -1);
      pintar();
      if (!seleccion.length) dLista.querySelector('[data-vt-cerrar]').focus();
    });
    pintar();
    abrirPedido();

    // ?add=<slug>: se quita de la URL (no se vuelve a abrir al recargar) y, si la especie existe, se abre su diálogo.
    function abrirPedido() {
      const slug = new URLSearchParams(win.location.search).get('add');
      if (slug === null) return;
      win.history.replaceState(null, '', win.location.pathname + escribirFiltros(leerFiltros(win.location.search)));
      const b = conocida(slug) ? botones.find((x) => x.dataset.vtAgregar === slug) : null;
      if (b) abrirAgregar(b);
    }
  }

  function especial(doc) {
    const caja = doc.querySelector('[data-vt-especial]');
    if (!caja) return;
    const campo = caja.querySelector('input');
    const enlace = caja.querySelector('a[data-cta]');
    campo.addEventListener('input', () => enlace.setAttribute('href', WA + encodeURIComponent(mensajeEspecial(campo.value))));
  }

  const api = { GRUPOS, CLAVE, CADA_FILA, normalizar, leerFiltros, escribirFiltros, hayFiltros, contarFiltros, coincide, cantidad,
    agregar, cambiar, quitar, enLista, validarLista, guardarLista, leerLista, resumen, mensajeLista, enlaceLista,
    mensajeEspecial };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTCatalogo = Object.freeze(api);
  // especial() primero: filtrar() le copia lo buscado cuando no hay resultados y dispara su evento input.
  const iniciar = () => { especial(document); filtrar(document, root); armarLista(document, root); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
