/* Viveros Terra · terra.js · shell compartido (Etapa 1).
   - Mide por delegación cada clic en WhatsApp (generate_lead) y teléfono (click_to_call) con data-cta.
   - Firma los mensajes de WhatsApp con "Vengo de viverosterra.com" para atribuir el chat.
   - Abre y cierra el menú (paneles de escritorio y menú móvil) y oculta la barra móvil mientras el CTA del hero se ve.
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

  function evento(a, contexto) {
    const tipo = tipoEnlace(a.getAttribute('href'));
    if (!tipo) return null;
    const cta = a.getAttribute('data-cta') || contexto.tipo + ':sin-etiqueta';
    if (tipo === 'tel') return { nombre: 'click_to_call', params: { link_type: 'tel', cta_id: cta, service: contexto.servicio } };
    return { nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: cta, service: contexto.servicio } };
  }

  function contextoPagina(doc) {
    const head = doc.querySelector('.vt-head');
    return {
      tipo: (head && head.getAttribute('data-vt-tipo')) || 'desconocido',
      servicio: (head && head.getAttribute('data-vt-servicio')) || 'general',
    };
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

  // La barra oculta queda inerte (y con visibility:hidden en el CSS) para que sus enlaces no reciban el foco.
  function barra(doc, win) {
    const bar = doc.querySelector('[data-vt-bar]');
    const hero = doc.querySelector('[data-hero-cta], .svc-hero__ctas');
    if (!bar || !hero || !('IntersectionObserver' in win)) return;
    new win.IntersectionObserver(([entrada]) => {
      bar.classList.toggle('is-oculta', entrada.isIntersecting);
      bar.inert = entrada.isIntersecting;
    }).observe(hero);
  }

  const api = { FIRMA, tipoEnlace, conFirma, evento };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ...api, medir, menu, barra };
    return;
  }
  root.VTTerra = Object.freeze(api);
  medir(document, root);
  const iniciar = () => { menu(document, root); barra(document, root); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
