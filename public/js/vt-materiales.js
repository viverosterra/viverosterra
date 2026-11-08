// public/js/vt-materiales.js
/* Calculadoras de cantidad de las páginas de materiales (Etapa 2f): área y capa → cantidad, presentación sugerida y
   equivalente → WhatsApp con el resultado. La lógica es la de main (calcularTierra, calcularTezontle y calcularMarmol,
   que abrían WhatsApp con window.open), línea por línea, incluidos sus redondeos; casos congelados en
   tests/casos-materiales.json y la misma lógica en tools/site/componentes_materiales.py (paridad Python–JS). Los precios
   y los factores llegan en data-material, escrito desde datos.py: aquí no vive ningún precio. El botón es un enlace de
   WhatsApp con data-cta (terra.js lo mide como generate_lead y lo firma al hacer clic); sin área válida manda el mensaje
   de la página (data-mensaje). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const AREA_MAXIMA = 100000;
  const CIERRE = '¿Me pueden dar precio de entrega a domicilio en Tampico?';
  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  const miles = (n) => n.toLocaleString('es-MX');
  const enlace = (wa, texto) => `https://wa.me/${wa}?text=${encodeURIComponent(texto)}`;

  // "1,200" y "1200" son 1200; "12,5" es 12.5; "80 m²" es 80. 0 si no es un número mayor que 0 y hasta AREA_MAXIMA.
  function leerArea(texto) {
    let t = String(texto == null ? '' : texto).replace(/\s|m²|m2/gi, '');
    t = /^\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(t) ? t.replace(/,/g, '') : t.replace(',', '.');
    if (!/^\d+(?:\.\d+)?$/.test(t)) return 0;
    const n = Number(t);
    return n > 0 && n <= AREA_MAXIMA ? n : 0;
  }

  const m3De = (area, capa) => Math.ceil(area * capa * 10) / 10;

  function calcular(cfg, area, capa) {
    if (cfg.clave === 'tierra-negra') {
      const m3 = m3De(area, capa);
      const tramo = m3 <= 1.5 ? 'costales' : m3 <= 7 ? 'm3' : 'camion';
      return { m3, costales: Math.ceil(m3 / cfg.costal_m3), tramo };
    }
    if (cfg.clave === 'tezontle') {
      const m3 = m3De(area, capa);
      const tramo = m3 <= 1 ? 'costales' : m3 <= 5 ? 'm3' : m3 <= cfg.camion_m3 ? 'camion' : 'camiones';
      return { m3, costales: Math.ceil(m3 / cfg.costal_m3), tramo, camiones: Math.ceil(m3 / cfg.camion_m3) };
    }
    if (cfg.clave === 'marmol') {
      const porM2 = capa <= 4 ? 3 : capa <= 5 ? 4 : 5;
      const sacos = Math.ceil(area * porM2);
      return { sacos, kg: sacos * cfg.kg_saco, por_m2: porM2 };
    }
    return { kg: [Math.round(area * cfg.kg_m2[0]), Math.round(area * cfg.kg_m2[1])] };
  }

  function textos(cfg, area, capa, r, uso) {
    const a = String(area);
    if (cfg.clave === 'tierra-negra' || cfg.clave === 'tezontle') {
      const m3 = String(r.m3);
      const c = r.costales;
      let presentacion;
      let equivalente = `~${c} costales`;
      let lineas;
      if (cfg.clave === 'tierra-negra') {
        presentacion = { costales: `${c} costales (${dinero(c * cfg.precio_costal)})`,
          m3: `${m3} m³ suelto (~${dinero(r.m3 * cfg.precio_m3)})`,
          camion: 'Camión volteo de 8 m³ o más (según cotización)' }[r.tramo];
        if (r.tramo === 'costales') equivalente = `${c} costales`;
        lineas = [`Área: ${a} m²`, `Cantidad: ${m3} m³`];
      } else {
        presentacion = { costales: `${c} costales`, m3: `${m3} m³ suelto`, camion: 'Camión 14 m³',
          camiones: `${r.camiones} camiones 14 m³` }[r.tramo];
        lineas = [`Área: ${a} m²`, `Uso: ${uso}`, `Cantidad: ${m3} m³`];
      }
      const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Resultado de la calculadora:', ...lineas, '', CIERRE].join('\n');
      return { cantidad: `${m3} m³`, presentacion, equivalente, mensaje };
    }
    if (cfg.clave === 'marmol') {
      const g = String(capa);
      const nota = capa <= 4 ? `${r.sacos} sacos cubren ${a} m² con capa de ${g} cm.`
        : `${r.sacos} sacos para ${a} m² con capa de ${g} cm (alta densidad).`;
      const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Datos de mi proyecto:', `Área: ${a} m²`, `Capa: ${g} cm`,
        `Cantidad: ${r.sacos} sacos`, '', CIERRE].join('\n');
      return { cantidad: `${r.sacos} sacos`, peso: `${r.kg} kg`, nota, mensaje };
    }
    const cantidad = `${miles(r.kg[0])} a ${miles(r.kg[1])} kg`;
    const mensaje = [`Hola, quiero cotizar ${cfg.texto}.`, '', 'Resultado de la calculadora:', `Área: ${a} m²`,
      'Medida: mediana (capa de 8 a 10 cm)', `Cantidad aprox.: ${cantidad}`, '', CIERRE].join('\n');
    return { cantidad, mensaje };
  }

  // Estado vacío: el que escribió el HTML (componentes_materiales.VACIO); se lee al arrancar para no repetir textos.
  function iniciar(caja) {
    const cfg = JSON.parse(caja.dataset.material);
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    const area = caja.querySelector('[data-vt-campo="area"]');
    const capa = caja.querySelector('[data-vt-campo="capa"]');
    const nombres = ['cantidad', 'presentacion', 'equivalente', 'peso'].filter((n) => salida(n));
    const vacio = Object.fromEntries(nombres.map((n) => [n, salida(n).textContent]));
    const nota = salida('nota');
    function actualizar() {
      const a = leerArea(area.value);
      if (!a) {
        nombres.forEach((n) => { salida(n).textContent = vacio[n]; });
        if (nota) nota.hidden = true;
        salida('cta').setAttribute('href', enlace(caja.dataset.wa, caja.dataset.mensaje));
        return;
      }
      const g = capa ? Number(capa.value) : 0;
      const uso = capa ? capa.options[capa.selectedIndex].text : '';
      const t = textos(cfg, a, g, calcular(cfg, a, g), uso);
      nombres.forEach((n) => { salida(n).textContent = t[n]; });
      if (nota) { nota.textContent = t.nota; nota.hidden = false; }
      salida('cta').setAttribute('href', enlace(caja.dataset.wa, t.mensaje));
    }
    caja.addEventListener('input', actualizar);
    caja.addEventListener('change', actualizar);
    actualizar();
  }

  const api = { leerArea, calcular, textos, enlace, CIERRE };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMateriales = Object.freeze(api);
  const arrancar = () => document.querySelectorAll('[data-vt-material]').forEach(iniciar);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
