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
    if (tipo === 'tel') return { nombre: 'click_to_call', params: { cta_id: cta } };
    return { nombre: 'generate_lead', params: { method: 'whatsapp', cta_id: cta, service: contexto.servicio } };
  }

  function contextoPagina(doc) {
    const head = doc.querySelector('.vt-head');
    return {
      tipo: (head && head.getAttribute('data-vt-tipo')) || 'desconocido',
      servicio: (head && head.getAttribute('data-vt-servicio')) || 'general',
    };
  }

  function medir(doc, win) {
    doc.addEventListener('click', (e) => {
      const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      const href = a.getAttribute('href');
      if (tipoEnlace(href) === 'wa') a.setAttribute('href', conFirma(href));
      if (a.matches(OMITIR_EVENTO)) return;
      const ev = evento(a, contextoPagina(doc));
      if (ev && typeof win.gtag === 'function') win.gtag('event', ev.nombre, ev.params);
    }, true);
  }

  function menu(doc) {
    const burger = doc.querySelector('.vt-burger');
    const movil = doc.getElementById('vt-mmenu');
    if (burger && movil) {
      burger.addEventListener('click', () => {
        const abierto = burger.getAttribute('aria-expanded') === 'true';
        burger.setAttribute('aria-expanded', String(!abierto));
        movil.hidden = abierto;
      });
    }
    const botones = Array.from(doc.querySelectorAll('.vt-nav [aria-controls]'));
    const cerrar = (excepto) => botones.forEach((b) => { if (b !== excepto) b.setAttribute('aria-expanded', 'false'); });
    botones.forEach((b) => b.addEventListener('click', (e) => {
      e.stopPropagation();
      const abierto = b.getAttribute('aria-expanded') === 'true';
      cerrar(b);
      b.setAttribute('aria-expanded', String(!abierto));
    }));
    doc.addEventListener('click', (e) => {
      if (!e.target.closest || !e.target.closest('.vt-nav')) cerrar(null);
    });
    doc.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const abierto = botones.find((b) => b.getAttribute('aria-expanded') === 'true');
      cerrar(null);
      if (abierto) abierto.focus();
    });
  }

  function barra(doc, win) {
    const bar = doc.querySelector('[data-vt-bar]');
    const hero = doc.querySelector('[data-hero-cta], .svc-hero__ctas');
    if (!bar || !hero || !('IntersectionObserver' in win)) return;
    new win.IntersectionObserver(([entrada]) => bar.classList.toggle('is-oculta', entrada.isIntersecting)).observe(hero);
  }

  const api = { FIRMA, tipoEnlace, conFirma, evento };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTTerra = Object.freeze(api);
  medir(document, root);
  const iniciar = () => { menu(document); barra(document, root); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
