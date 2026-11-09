// public/js/vt-nochebuenas.js
/* Cotizador por volumen de la página de temporada de Nochebuenas. Sin precios aquí: todo llega de datos.NOCHEBUENAS, que el
   build incrusta como JSON en <script id="nb-config">. Las funciones puras se exportan para node --test; la interfaz solo
   arranca si la página trae [data-nb-cotizador]. WhatsApp se abre con un enlace normal: terra.js lo firma y lo mide. */
(function (root) {
  'use strict';
  const MAX_CANTIDAD = 9999;
  const MAX_FALTAN = 4; // el nudge solo aparece si el siguiente escalón está a 4 piezas o menos
  const RECOJO = 'Recojo en vivero';
  const PREFIJO_SHEETS = 'https://script.google.com/macros/s/';
  const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  const MAX_LINEAS = 12;
  const VENTANA_DUPLICADO_MS = 10000; // un segundo clic idéntico no se registra dos veces en Sheets; WhatsApp sí abre
  const ESCRITORIO = '(min-width: 1024px)';
  const textoPreventa = (cfg) => `Precio preventa: apartando con ${cfg.anticipo_pct}% de anticipo`;
  const TEXTO_SOBRE_PEDIDO = 'Sobre pedido · sujeto a disponibilidad';
  const TEXTO_PROYECTO = 'Precio proyecto: te confirmamos disponibilidad y fecha de entrega';
  const LINEA_NUEVA = Object.freeze({ clave: '6', variedad: 'Roja', cantidad: 1 });

  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;
  const piezasTexto = (n) => `${n} ${n === 1 ? 'pieza' : 'piezas'}`;

  function entero(valor) {
    const n = Math.trunc(Number(valor));
    return n > 0 ? Math.min(n, MAX_CANTIDAD) : 0; // NaN, negativos y cero quedan en 0
  }

  function hoyMX(fecha) {
    const partes = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Mexico_City', year: 'numeric', month: '2-digit', day: '2-digit' })
      .formatToParts(fecha);
    const de = (tipo) => partes.find((p) => p.type === tipo).value;
    return `${de('year')}-${de('month')}-${de('day')}`;
  }

  const productoDe = (cfg, clave) => cfg.productos.find((p) => p.clave === clave);

  // Copias de las líneas con piezas y producto conocido, en su orden.
  function normalizar(lineas, cfg) {
    return lineas
      .map((l) => ({ clave: l.clave, variedad: l.variedad, cantidad: entero(l.cantidad) }))
      .filter((l) => l.cantidad > 0 && productoDe(cfg, l.clave));
  }

  const totalPiezas = (lineas) => lineas.reduce((suma, l) => suma + l.cantidad, 0);
  const escalonDe = (piezas, cortes) => cortes.reduce((actual, corte, i) => (piezas >= corte ? i : actual), -1);
  const importe = (lineas, cfg, escalon) => lineas.reduce((suma, l) => suma + l.cantidad * productoDe(cfg, l.clave).precios[escalon], 0);
  const descuentoDe = (subtotal, cfg) => Math.round(subtotal * cfg.preventa.descuento);
  const aplicaPreventa = (escalon, cfg, hoy) => hoy <= cfg.preventa.hasta && escalon >= 0 && escalon <= cfg.preventa.aplica_hasta_escalon;

  function lineaCotizada(l, cfg, escalon) {
    const producto = productoDe(cfg, l.clave);
    const precio = producto.precios[escalon];
    return { clave: l.clave, nombre: producto.nombre, variedad: l.variedad, cantidad: l.cantidad, precio,
      subtotal: l.cantidad * precio, sobrePedido: Boolean(producto.sobre_pedido) };
  }

  function cotizar(lineas, cfg, hoy) {
    const validas = normalizar(lineas, cfg);
    const piezas = totalPiezas(validas);
    const escalon = escalonDe(piezas, cfg.cortes);
    const cotizadas = validas.map((l) => lineaCotizada(l, cfg, escalon));
    const subtotal = importe(validas, cfg, escalon);
    const preventa = aplicaPreventa(escalon, cfg, hoy);
    const descuento = preventa ? descuentoDe(subtotal, cfg) : 0;
    const total = subtotal - descuento;
    return { piezas, escalon, nombreEscalon: cfg.nombres_escalon[escalon] || '', lineas: cotizadas, subtotal, preventa, descuento,
      total, ahorro: importe(validas, cfg, 0) - subtotal, proyecto: escalon === cfg.cortes.length - 1,
      haySobrePedido: cotizadas.some((l) => l.sobrePedido) };
  }

  function textoNudge(n) {
    const inicio = `Te ${n.faltan === 1 ? 'falta' : 'faltan'} ${piezasTexto(n.faltan)} para precio ${n.nombre}`;
    if (n.diferencia > 0) return `${inicio}: por ${dinero(n.diferencia)} más te llevas ${n.objetivo} y ahorras ${dinero(n.ahorro)}`;
    if (n.diferencia < 0) return `${inicio}: te llevas ${n.objetivo}, pagas ${dinero(-n.diferencia)} menos y ahorras ${dinero(n.ahorro)}`;
    return `${inicio}: por el mismo total te llevas ${n.objetivo} y ahorras ${dinero(n.ahorro)}`;
  }

  function nudge(lineas, cfg, hoy) {
    const actual = cotizar(lineas, cfg, hoy);
    const objetivo = cfg.cortes[actual.escalon + 1];
    if (actual.escalon < 0 || objetivo === undefined) return null;
    const faltan = objetivo - actual.piezas;
    if (faltan > MAX_FALTAN) return null;
    const validas = normalizar(lineas, cfg);
    const ampliadas = validas.map((l, i) => (i === validas.length - 1 ? { ...l, cantidad: l.cantidad + faltan } : l));
    const siguiente = cotizar(ampliadas, cfg, hoy);
    const sinSubir = importe(ampliadas, cfg, actual.escalon);
    const ahorro = sinSubir - (actual.preventa ? descuentoDe(sinSubir, cfg) : 0) - siguiente.total;
    // Al llegar a Proyecto se pierde la preventa: si eso no conviene, no se ofrece el nudge.
    if (ahorro <= 0) return null;
    const datos = { faltan, nombre: cfg.nombres_escalon[actual.escalon + 1], objetivo, diferencia: siguiente.total - actual.total, ahorro };
    return { ...datos, texto: textoNudge(datos) };
  }

  function entrega(total, zona, cfg) {
    if (zona === RECOJO) return null;
    const faltan = cfg.entrega_incluida_desde - total;
    if (faltan <= 0) {
      return { incluida: true, texto: zona ? 'Entrega incluida'
        : `Entrega incluida desde ${dinero(cfg.entrega_incluida_desde)} en Tampico, Madero y Altamira.` };
    }
    return { incluida: false, faltan,
      texto: `Te faltan ${dinero(faltan)} para entrega incluida. Entrega según tu ubicación o colonia; te la cotizamos por WhatsApp.` };
  }

  function fechaCorta(fecha) {
    const m = /^\d{4}-(\d{2})-(\d{2})$/.exec(fecha || '');
    return m ? `${Number(m[2])} ${MESES[Number(m[1]) - 1]}` : '';
  }

  const descripcion = (l) => `${l.cantidad} × ${l.nombre} ${l.variedad}`.trim();

  function mensaje(cot, extras, cfg) {
    const verbo = cfg.modo === 'preventa' ? 'Quiero apartar' : 'Quiero cotizar';
    const entregaTexto = [extras.zona, fechaCorta(extras.fecha), extras.factura ? 'Requiero factura' : ''].filter(Boolean).join(' · ');
    return [
      `Hola Viveros Terra 🌺 ${verbo} Nochebuenas ${cfg.temporada}:`,
      ...cot.lineas.map((l) => `• ${descripcion(l)}`),
      `Total: ${piezasTexto(cot.piezas)} · Escalón: ${cot.nombreEscalon} · Total estimado: ${dinero(cot.total)}`,
      cot.preventa ? textoPreventa(cfg) : '',
      entregaTexto ? `Entrega: ${entregaTexto}` : '',
      extras.tipo ? `Tipo de cliente: ${extras.tipo}` : '',
    ].filter(Boolean).join('\n');
  }

  function registro(cot, extras, cfg, ubicacion) {
    const utm = new URLSearchParams(ubicacion.search || '');
    return { lineas: cot.lineas.map(descripcion).join(' | '), piezas: cot.piezas, escalon: cot.nombreEscalon, total: cot.total,
      preventa: cot.preventa, zona: extras.zona || '', fecha_deseada: extras.fecha || '', tipo_cliente: extras.tipo || '',
      factura: Boolean(extras.factura), origen: ubicacion.pathname || '', utm_source: utm.get('utm_source') || '',
      utm_medium: utm.get('utm_medium') || '', utm_campaign: utm.get('utm_campaign') || '' };
  }

  function enviarRegistro(endpoint, datos, nav) {
    if (typeof endpoint !== 'string' || !endpoint.startsWith(PREFIJO_SHEETS)) return;
    try {
      nav.sendBeacon(endpoint, JSON.stringify(datos));
    } catch (error) {
      // El registro es secundario: si falla, WhatsApp abre igual y al cliente no se le avisa (spec §3).
    }
  }

  const esDuplicado = (previo, clave, ahora) => Boolean(previo && previo.clave === clave && ahora - previo.t < VENTANA_DUPLICADO_MS);

  // Antes de usar el cotizador invita; después muestra el total. Dentro del cotizador lleva al ticket.
  function textoBarra(cot, usado, dentro, cfg) {
    const verbo = cfg.modo === 'preventa' ? 'Apartar' : 'Cotizar';
    if (!usado || !cot.piezas) return { texto: `${verbo} mi pedido`, href: '#cotizador' };
    if (dentro) return { texto: `${piezasTexto(cot.piezas)} · ${dinero(cot.total)} · Ver total`, href: '#nb-ticket' };
    return { texto: `${verbo} · ${dinero(cot.total)}`, href: '#cotizador' };
  }

  /* ---------- Interfaz ---------- */

  const campo = (raiz, nombre) => raiz.querySelector(`[data-nb-campo="${nombre}"]`);
  const filasDe = (caja) => Array.from(caja.querySelectorAll('[data-nb-linea]'));

  // Las salidas vacías se ocultan para no dejar huecos; las que falten en el HTML se ignoran.
  function escribir(raiz, nombre, texto) {
    const salida = raiz.querySelector(`[data-nb-o="${nombre}"]`);
    if (!salida) return;
    salida.textContent = texto;
    salida.hidden = !texto;
  }

  const leerLinea = (fila) => ({ clave: campo(fila, 'producto').value, variedad: campo(fila, 'variedad').value,
    cantidad: campo(fila, 'cantidad').value });

  function leerExtras(caja) {
    const valor = (nombre) => { const c = campo(caja, nombre); return c ? c.value : ''; };
    const factura = campo(caja, 'factura');
    return { zona: valor('zona'), fecha: valor('fecha'), tipo: valor('tipo'), factura: Boolean(factura && factura.checked) };
  }

  const ROTULOS = [['[data-nb-campo="producto"]', 'Tamaño'], ['[data-nb-campo="variedad"]', 'Variedad'], ['[data-nb-campo="cantidad"]', 'Piezas'],
    ['[data-nb-accion="menos"]', 'Una pieza menos'], ['[data-nb-accion="mas"]', 'Una pieza más'], ['[data-nb-accion="quitar"]', 'Quitar']];

  function rotular(fila, numero) {
    ROTULOS.forEach(([selector, texto]) => fila.querySelector(selector).setAttribute('aria-label', `${texto}, línea ${numero}`));
  }

  function pintarFilas(caja, cot, cfg) {
    const filas = filasDe(caja);
    let i = 0;
    filas.forEach((fila, n) => {
      const linea = normalizar([leerLinea(fila)], cfg).length > 0 ? cot.lineas[i++] : null;
      escribir(fila, 'subtotal', dinero(linea ? linea.subtotal : 0));
      escribir(fila, 'unitario', linea ? `${linea.cantidad} × ${dinero(linea.precio)}` : '');
      rotular(fila, n + 1);
      fila.querySelector('[data-nb-accion="quitar"]').hidden = filas.length === 1;
    });
    const agregar = caja.querySelector('[data-nb-accion="agregar"]');
    agregar.disabled = filas.length >= MAX_LINEAS;
    escribir(caja, 'tope', agregar.disabled ? `Máximo ${MAX_LINEAS} líneas por pedido; para más, escríbenos.` : '');
  }

  function pintarResumen(caja, cot, sugerencia, zona, cfg) {
    const conPiezas = cot.piezas > 0;
    const envio = conPiezas ? entrega(cot.total, zona, cfg) : null;
    const hayMaximo = filasDe(caja).some((fila) => entero(campo(fila, 'cantidad').value) >= MAX_CANTIDAD);
    escribir(caja, 'piezas', piezasTexto(cot.piezas));
    escribir(caja, 'total', dinero(cot.total));
    escribir(caja, 'escalon', cot.nombreEscalon || '—');
    escribir(caja, 'desglose', cot.descuento ? `Subtotal ${dinero(cot.subtotal)} · Preventa −${dinero(cot.descuento)}` : '');
    escribir(caja, 'vacio', conPiezas ? '' : 'Agrega al menos 1 pieza');
    escribir(caja, 'ahorro', cot.ahorro > 0 ? `Ahorras ${dinero(cot.ahorro)} vs. menudeo` : '');
    escribir(caja, 'nudge', sugerencia ? sugerencia.texto : '');
    escribir(caja, 'preventa', cot.preventa ? textoPreventa(cfg) : '');
    escribir(caja, 'entrega', envio ? envio.texto : '');
    escribir(caja, 'sobre-pedido', cot.haySobrePedido ? TEXTO_SOBRE_PEDIDO : '');
    escribir(caja, 'proyecto', cot.proyecto ? TEXTO_PROYECTO : '');
    escribir(caja, 'maximo', hayMaximo ? `Máximo ${MAX_CANTIDAD.toLocaleString('es-MX')} por línea; para más, escríbenos` : '');
    const subir = caja.querySelector('[data-nb-accion="subir"]');
    subir.hidden = !sugerencia;
    if (sugerencia) subir.textContent = `Subir a ${sugerencia.objetivo} piezas`;
  }

  // Sin piezas el href apunta al propio cotizador: un enlace de WhatsApp contaría como generate_lead en terra.js aunque no navegue.
  function pintarCta(cta, cot, extras, cfg) {
    if (!cot.piezas) {
      cta.setAttribute('href', '#cotizador');
      cta.setAttribute('aria-disabled', 'true');
      cta.setAttribute('aria-describedby', 'nb-aviso-vacio');
      return;
    }
    cta.setAttribute('href', enlace(cfg.wa, mensaje(cot, extras, cfg)));
    cta.removeAttribute('aria-disabled');
    cta.removeAttribute('aria-describedby');
  }

  function ponerCantidad(fila, valor) {
    campo(fila, 'cantidad').value = String(entero(valor));
  }

  function agregarLinea(caja) {
    const filas = filasDe(caja);
    if (filas.length >= MAX_LINEAS) return;
    const nueva = filas[filas.length - 1].cloneNode(true);
    campo(nueva, 'producto').value = LINEA_NUEVA.clave;
    campo(nueva, 'variedad').value = LINEA_NUEVA.variedad;
    ponerCantidad(nueva, LINEA_NUEVA.cantidad);
    filas[filas.length - 1].after(nueva);
    campo(nueva, 'producto').focus();
  }

  // Suma las piezas que faltan a la última línea con piezas, la misma que usa el nudge.
  function subirAlCorte(caja, cfg, hoy, cta) {
    const filas = filasDe(caja);
    const sugerencia = nudge(filas.map(leerLinea), cfg, hoy);
    const ultima = filas.filter((f) => normalizar([leerLinea(f)], cfg).length > 0).pop();
    if (!sugerencia || !ultima) return;
    ponerCantidad(ultima, entero(campo(ultima, 'cantidad').value) + sugerencia.faltan);
    if (cta) cta.focus({ preventScroll: true }); // el botón desaparece: el foco no se pierde
  }

  function aplicarAccion(caja, boton) {
    const accion = boton.dataset.nbAccion;
    const fila = boton.closest('[data-nb-linea]');
    if (accion === 'agregar') agregarLinea(caja);
    else if (accion === 'mas' || accion === 'menos') ponerCantidad(fila, entero(campo(fila, 'cantidad').value) + (accion === 'mas' ? 1 : -1));
    else if (accion === 'quitar' && filasDe(caja).length > 1) {
      fila.remove();
      const agregar = caja.querySelector('[data-nb-accion="agregar"]');
      if (agregar) agregar.focus();
    }
  }

  const unaVez = (fn) => { let hecho = false; return (...args) => { if (!hecho) { hecho = true; fn(...args); } }; };

  function crearBarra(doc, win, cfg) {
    const barra = doc.querySelector('[data-nb-bar]');
    const enlaceBarra = doc.querySelector('[data-nb-total-barra]');
    if (!barra || !enlaceBarra) return { pintar() {}, usar() {}, foco() {} };
    const vistos = { hero: false, ticket: false, cotizador: false };
    let usado = false;
    let foco = false;
    let cot = { piezas: 0, total: 0 };
    function refrescar() {
      const { texto, href } = textoBarra(cot, usado, vistos.cotizador, cfg);
      enlaceBarra.textContent = texto;
      enlaceBarra.setAttribute('href', href);
      barra.hidden = vistos.hero || vistos.ticket || foco || (vistos.cotizador && !(usado && cot.piezas));
    }
    const objetivos = { hero: doc.querySelector('[data-hero-cta]'), ticket: doc.getElementById('nb-ticket'), cotizador: doc.getElementById('cotizador') };
    const nombres = new Map(Object.entries(objetivos).filter(([, el]) => el).map(([nombre, el]) => [el, nombre]));
    if (win.IntersectionObserver) {
      const observador = new win.IntersectionObserver((entradas) => {
        entradas.forEach((e) => { vistos[nombres.get(e.target)] = e.isIntersecting; });
        refrescar();
      });
      nombres.forEach((_nombre, el) => observador.observe(el));
    } else {
      refrescar();
    }
    return {
      pintar(nuevo) { cot = nuevo; refrescar(); },
      usar() { usado = true; },
      foco(valor) { foco = valor; refrescar(); },
    };
  }

  function abrirExtrasEnEscritorio(caja, win) {
    const extras = caja.querySelector('[data-nb-extras]');
    if (!extras || !win.matchMedia) return;
    const medida = win.matchMedia(ESCRITORIO);
    const aplicar = () => { if (medida.matches) extras.open = true; };
    aplicar();
    medida.addEventListener('change', aplicar);
  }

  function iniciar(doc, win, caja, cfgJson) {
    const cfg = Object.freeze({ ...cfgJson, modo: caja.dataset.nbModo || cfgJson.modo });
    const cta = caja.querySelector('a[data-cta="nochebuenas:cotizador"]');
    const barra = crearBarra(doc, win, cfg);
    const evento = (nombre, params) => { if (typeof win.gtag === 'function') win.gtag('event', nombre, params); };
    const usoMedido = unaVez(() => evento('nb_cotizador_uso', {}));
    const nudgeMedido = unaVez(() => evento('nb_nudge_visto', {}));
    let ultimoRegistro = null;

    function leerEstado() {
      const lineas = filasDe(caja).map(leerLinea);
      const hoy = hoyMX(new win.Date());
      return { lineas, hoy, cot: cotizar(lineas, cfg, hoy), sugerencia: nudge(lineas, cfg, hoy), extras: leerExtras(caja) };
    }

    function actualizar() {
      const { cot, sugerencia, extras } = leerEstado();
      pintarFilas(caja, cot, cfg);
      pintarResumen(caja, cot, sugerencia, extras.zona, cfg);
      if (cta) pintarCta(cta, cot, extras, cfg);
      barra.pintar(cot);
      if (sugerencia) nudgeMedido();
    }
    const alCambiar = () => { usoMedido(); barra.usar(); actualizar(); };

    caja.addEventListener('click', (e) => {
      const boton = e.target.closest('[data-nb-accion]');
      if (!boton) return;
      if (boton.dataset.nbAccion === 'subir') subirAlCorte(caja, cfg, leerEstado().hoy, cta);
      else aplicarAccion(caja, boton);
      alCambiar();
    });
    caja.addEventListener('input', alCambiar);
    caja.addEventListener('change', (e) => {
      if (e.target.matches('[data-nb-campo="cantidad"]')) ponerCantidad(e.target.closest('[data-nb-linea]'), e.target.value);
      alCambiar();
    });
    caja.addEventListener('focusin', (e) => {
      if (e.target.matches('[data-nb-campo="cantidad"]')) e.target.select();
      if (e.target.matches('select, input')) barra.foco(true);
    });
    caja.addEventListener('focusout', (e) => {
      if (e.target.matches('select, input')) barra.foco(false);
    });
    if (cta) {
      cta.addEventListener('click', (e) => {
        const { cot, extras } = leerEstado();
        if (!cot.piezas) { e.preventDefault(); return; }
        const datos = registro(cot, extras, cfg, win.location);
        const clave = JSON.stringify(datos);
        const ahora = win.Date.now();
        if (!esDuplicado(ultimoRegistro, clave, ahora)) {
          enviarRegistro(cfg.sheets_endpoint, datos, win.navigator);
          ultimoRegistro = { clave, t: ahora };
        }
        evento('nb_whatsapp_click', { total: cot.total, escalon: cot.nombreEscalon });
      });
    }
    const total = caja.querySelector('[data-nb-o="total"]');
    if (total) total.setAttribute('aria-live', 'polite');
    const fecha = campo(caja, 'fecha');
    if (fecha) fecha.min = hoyMX(new win.Date());
    abrirExtrasEnEscritorio(caja, win);
    actualizar();
  }

  function ocultarVencidas(doc, hoy) {
    doc.querySelectorAll('[data-nb-hasta]').forEach((el) => { el.hidden = hoy > el.dataset.nbHasta; });
  }

  function leerConfig(doc) {
    const nodo = doc.getElementById('nb-config');
    if (!nodo) return null;
    try {
      return JSON.parse(nodo.textContent);
    } catch (error) {
      return null; // sin configuración válida queda el HTML estático, con su enlace genérico a WhatsApp
    }
  }

  const api = { hoyMX, cotizar, nudge, entrega, mensaje, registro, enviarRegistro, esDuplicado, textoBarra };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTNochebuenas = Object.freeze(api);
  const arrancar = () => {
    const caja = document.querySelector('[data-nb-cotizador]');
    const cfg = caja ? leerConfig(document) : null;
    if (!cfg) return;
    iniciar(document, root, caja, cfg);
    ocultarVencidas(document, hoyMX(new Date()));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
