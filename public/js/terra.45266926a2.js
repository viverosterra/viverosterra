/* Viveros Terra · terra.js · shell compartido (Etapa 1).
   - Mide por delegación cada clic en WhatsApp (generate_lead) y teléfono (click_to_call) con data-cta.
   - Firma los mensajes de WhatsApp con "Vengo de viverosterra.com" para atribuir el chat, tanto en los enlaces como en
     los que las páginas abren con window.open (calculadoras, catálogo, formulario de la home).
   - Mide los enlaces al catálogo (select_content), que antes medían los clic_catalogo_* sueltos.
   - Abre y cierra el menú (paneles de escritorio y menú móvil) y oculta la barra móvil mientras el CTA del hero se ve.
   - En horario antepone "Abierto ahora · " a las promesas marcadas con data-vt-horario; el horario y los festivos
     llegan de ese atributo y de data-vt-festivos (los escribe el build desde datos.py), nunca de este archivo.
   - Expone window.VTMedicion.whatsapp(ctaId, extra) para los WhatsApp que las páginas abren con window.open: manda el
     mismo generate_lead que un clic en enlace (seguro aunque gtag no exista).
   Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const FIRMA = 'Vengo de viverosterra.com';
  // La tienda ya manda sus propios generate_lead (tienda-pasto.js): aquí solo se firman.
  const OMITIR_EVENTO = '[data-cta-wa], #cot-send';

  function tipoEnlace(href) {
    if (!href) return null;
    if (/^tel:/i.test(href)) return 'tel';
    if (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(href)) return 'wa';
    return null;
  }

  function conFirma(href) {
    const partes = href.match(/^([^?#]*)(?:\?([^#]*))?(#.*)?$/);
    const base = partes[1];
    const consulta = partes[2] ? partes[2].split('&') : [];
    const ancla = partes[3] || '';
    const i = consulta.findIndex((p) => p.split('=')[0] === 'text');
    let actual = '';
    if (i >= 0) {
      try {
        actual = decodeURIComponent(consulta[i].slice(5).replace(/\+/g, ' '));
      } catch (error) {
        // Texto mal codificado: no se toca el enlace para no romper el mensaje que armó la página.
        return href;
      }
    }
    if (/viverosterra\.com/i.test(actual)) return href;
    const nuevo = 'text=' + encodeURIComponent(actual ? actual + '\n\n' + FIRMA : FIRMA);
    if (i >= 0) consulta[i] = nuevo;
    else consulta.push(nuevo);
    return base + '?' + consulta.join('&') + ancla;
  }

  const CATALOGO_RE = /^\/catalogo(\.html)?(?:[?#].*)?$/;

  function evento(a, contexto) {
    const href = a.getAttribute('href');
    if (href && CATALOGO_RE.test(href)) {
      const cta = a.getAttribute('data-cta') || contexto.tipo + ':catalogo';
      return { nombre: 'select_content', params: { content_type: 'catalogo', item_id: 'catalogo', cta_id: cta, service: contexto.servicio } };
    }
    const tipo = tipoEnlace(href);
    if (!tipo) return null;
    const cta = a.getAttribute('data-cta') || contexto.tipo + ':sin-etiqueta';
    if (tipo === 'tel') return { nombre: 'click_to_call', params: { link_type: 'tel', cta_id: cta, service: contexto.servicio } };
    return { nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: cta, service: contexto.servicio } };
  }

  // ctaId sin prefijo ("calculadora") toma el tipo de la página: "servicio-pasto:calculadora". `extra` no puede pisar
  // method, cta_id ni service.
  function eventoWhatsapp(ctaId, contexto, extra) {
    const seccion = String(ctaId || 'js');
    const cta = seccion.indexOf(':') >= 0 ? seccion : contexto.tipo + ':' + seccion;
    const base = extra && typeof extra === 'object' ? extra : {};
    return { nombre: 'generate_lead', params: { ...base, method: 'whatsapp', cta_id: cta, service: contexto.servicio } };
  }

  function contextoPagina(doc) {
    const head = doc.querySelector('.vt-head');
    return {
      tipo: (head && head.getAttribute('data-vt-tipo')) || 'desconocido',
      servicio: (head && head.getAttribute('data-vt-servicio')) || 'general',
    };
  }

  // window.open('https://wa.me/...') de las páginas sale con la firma, como los enlaces. conFirma no firma dos veces.
  function firmarAperturas(win) {
    const original = win.open;
    if (typeof original !== 'function' || original.vtFirma) return;
    const firmado = function (url, ...resto) {
      const texto = url == null ? url : String(url);
      return original.call(this, tipoEnlace(texto) === 'wa' ? conFirma(texto) : url, ...resto);
    };
    firmado.vtFirma = true;
    win.open = firmado;
  }

  // Clic normal, con Ctrl/Cmd/Shift (llega como 'click') y clic medio ('auxclick', botón 1). Nunca se impide la
  // navegación: solo se firma el enlace de WhatsApp y se manda el evento.
  function medir(doc, win) {
    const alPulsar = (e) => {
      if (e.type === 'auxclick' && e.button !== 1) return;
      const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      const href = a.getAttribute('href');
      if (tipoEnlace(href) === 'wa') a.setAttribute('href', conFirma(href));
      if (a.matches(OMITIR_EVENTO)) return;
      const ev = evento(a, contextoPagina(doc));
      if (ev && typeof win.gtag === 'function') win.gtag('event', ev.nombre, ev.params);
    };
    doc.addEventListener('click', alPulsar, true);
    doc.addEventListener('auxclick', alPulsar, true);
  }

  // Los paneles de escritorio solo se muestran con aria-expanded="true" (el CSS no usa :hover). Con mouse se abren
  // por hover con retraso, y el panel sigue abierto mientras el puntero esté en el item (WCAG 1.4.13); Escape los
  // cierra y regresa el foco a su botón. Un clic sobre un panel abierto por hover lo fija en vez de cerrarlo.
  const ABRIR_MS = 120;
  const CERRAR_MS = 300;

  function menu(doc, win) {
    const burger = doc.querySelector('.vt-burger');
    const movil = doc.getElementById('vt-mmenu');
    const abrirMovil = (abrir) => {
      burger.setAttribute('aria-expanded', String(abrir));
      movil.hidden = !abrir;
    };
    if (burger && movil) {
      burger.addEventListener('click', () => abrirMovil(burger.getAttribute('aria-expanded') !== 'true'));
    }
    const botones = Array.from(doc.querySelectorAll('.vt-nav [aria-controls]'));
    const origen = new Map();
    const abierto = (b) => b.getAttribute('aria-expanded') === 'true';
    const fijar = (b, abrir, como) => {
      b.setAttribute('aria-expanded', String(abrir));
      if (abrir) origen.set(b, como);
      else origen.delete(b);
    };
    const cerrar = (excepto) => botones.forEach((b) => { if (b !== excepto) fijar(b, false); });
    botones.forEach((b) => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        const abrir = !abierto(b) || origen.get(b) === 'hover';
        cerrar(b);
        fijar(b, abrir, 'clic');
      });
      const item = b.closest ? b.closest('.vt-nav__item') : null;
      if (!item) return;
      let reloj = null;
      const programar = (fn, ms) => { win.clearTimeout(reloj); reloj = win.setTimeout(fn, ms); };
      item.addEventListener('pointerenter', (e) => {
        if (e.pointerType !== 'mouse') return;
        programar(() => { if (!abierto(b)) { cerrar(b); fijar(b, true, 'hover'); } }, ABRIR_MS);
      });
      item.addEventListener('pointerleave', (e) => {
        if (e.pointerType !== 'mouse') return;
        programar(() => { if (origen.get(b) === 'hover') fijar(b, false); }, CERRAR_MS);
      });
      item.addEventListener('focusout', (e) => {
        // Solo cuando el foco pasa a otro elemento (Tab); los clics afuera los cierra el oyente del documento.
        if (e.relatedTarget && !item.contains(e.relatedTarget)) fijar(b, false);
      });
    });
    doc.addEventListener('click', (e) => {
      if (!e.target.closest || !e.target.closest('.vt-nav')) cerrar(null);
    });
    doc.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const panel = botones.find(abierto);
      if (panel) {
        cerrar(null);
        panel.focus();
        return;
      }
      if (burger && movil && !movil.hidden) {
        abrirMovil(false);
        burger.focus();
      }
    });
  }

  function medicion(doc, win) {
    return Object.freeze({
      whatsapp(ctaId, extra) {
        try {
          const ev = eventoWhatsapp(ctaId, contextoPagina(doc), extra);
          if (typeof win.gtag === 'function') win.gtag('event', ev.nombre, ev.params);
          return ev;
        } catch (error) {
          // La medición nunca debe impedir que se abra el WhatsApp que viene justo después.
          return null;
        }
      },
    });
  }

  // CTAs de hero: los marcados a mano, los de servicios, los de la home vieja y los que shell.py etiqueta ":hero".
  const HERO_CTA = '[data-hero-cta], .svc-hero__ctas, .vt-hero__ctas, [data-cta$=":hero"]';

  // La barra oculta queda inerte (y con visibility:hidden en el CSS) para que sus enlaces no reciban el foco. Se oculta
  // mientras se vea cualquiera de los CTAs del hero.
  function barra(doc, win) {
    const bar = doc.querySelector('[data-vt-bar]');
    const heroes = Array.from(doc.querySelectorAll(HERO_CTA));
    if (!bar || !heroes.length || !('IntersectionObserver' in win)) return;
    const visibles = new Set();
    const observador = new win.IntersectionObserver((entradas) => {
      entradas.forEach((e) => (e.isIntersecting ? visibles.add(e.target) : visibles.delete(e.target)));
      const ocultar = visibles.size > 0;
      bar.classList.toggle('is-oculta', ocultar);
      bar.inert = ocultar;
    });
    heroes.forEach((h) => observador.observe(h));
  }

  // "Abierto ahora": el horario llega como "<días>@HH:MM-HH:MM;<días>@HH:MM-HH:MM" (días separados por coma, lunes = 1,
  // hora de México) y los festivos como "MM-DD,MM-DD", cada año. Se abre a la hora de apertura y a la de cierre ya está cerrado.
  const ABIERTO = 'Abierto ahora';
  const ZONA = 'America/Mexico_City';
  const DIAS = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };
  const TRAMO_RE = /^([1-7](?:,[1-7])*)@(\d{2}):(\d{2})-(\d{2}):(\d{2})$/;

  function enMexico(fecha) {
    try {
      const partes = {};
      new Intl.DateTimeFormat('en-US', { timeZone: ZONA, weekday: 'short', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(fecha)
        .forEach((p) => { partes[p.type] = p.value; });
      return { dia: DIAS[partes.weekday], fecha: partes.month + '-' + partes.day,
        minuto: Number(partes.hour) * 60 + Number(partes.minute) };
    } catch (error) {
      // Fecha inválida o navegador sin zonas horarias: no se afirma que está abierto.
      return null;
    }
  }

  function abierto(fecha, horario, festivos) {
    const ahora = enMexico(fecha);
    if (!ahora || !ahora.dia) return false;
    if (String(festivos || '').split(',').includes(ahora.fecha)) return false;
    return String(horario || '').split(';').some((tramo) => {
      const m = tramo.match(TRAMO_RE);
      if (!m || !m[1].split(',').includes(String(ahora.dia))) return false;
      return ahora.minuto >= Number(m[2]) * 60 + Number(m[3]) && ahora.minuto < Number(m[4]) * 60 + Number(m[5]);
    });
  }

  // El prefijo es texto dentro del elemento marcado (la promesa del HTML no se toca) y la clase is-abierto pinta el
  // punto verde: el punto nunca va sin el texto. Fuera de horario se retira y el elemento queda como en el HTML.
  function horario(doc, ahora) {
    doc.querySelectorAll('[data-vt-horario]').forEach((el) => {
      const si = abierto(ahora, el.getAttribute('data-vt-horario'), el.getAttribute('data-vt-festivos'));
      const primero = el.firstChild;
      const puesto = Boolean(primero && primero.hasAttribute && primero.hasAttribute('data-vt-abierto'));
      el.classList.toggle('is-abierto', si);
      if (si && !puesto) {
        const marca = doc.createElement('b');
        marca.setAttribute('data-vt-abierto', '');
        marca.textContent = ABIERTO;
        el.insertBefore(doc.createTextNode(' · '), primero);
        el.insertBefore(marca, el.firstChild);
      } else if (!si && puesto) {
        el.removeChild(primero.nextSibling);
        el.removeChild(primero);
      }
    });
  }

  // Tablas plegables (<details data-vt-plegable>): salen cerradas para acortar la página en celular; desde 768 px se
  // abren. Quien la cierre a mano en escritorio la deja cerrada (solo se abre una vez, al cargar).
  const PLEGABLE_DESDE = '(min-width: 768px)';
  function plegables(doc, win) {
    if (!win.matchMedia || !win.matchMedia(PLEGABLE_DESDE).matches) return;
    doc.querySelectorAll('details[data-vt-plegable]').forEach((d) => { d.open = true; });
  }

  const api = { FIRMA, HERO_CTA, ABIERTO, tipoEnlace, conFirma, evento, eventoWhatsapp, abierto };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ...api, medir, menu, barra, medicion, firmarAperturas, plegables, horario };
    return;
  }
  root.VTTerra = Object.freeze(api);
  root.VTMedicion = medicion(document, root);
  firmarAperturas(root);
  medir(document, root);
  const alDia = () => horario(document, new Date());
  const iniciar = () => { menu(document, root); barra(document, root); plegables(document, root); alDia(); };
  // Al volver a la pestaña se revisa otra vez: una página abierta desde la tarde no sigue diciendo "Abierto ahora".
  document.addEventListener('visibilitychange', () => { if (!document.hidden) alDia(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
