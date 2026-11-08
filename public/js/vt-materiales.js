// public/js/vt-materiales.js
/* Calculadoras de cantidad de las páginas de materiales (Etapa 2f): área y capa → cantidad, presentación sugerida y
   equivalente → WhatsApp con el resultado. La lógica es la de main (calcularTierra, calcularTezontle y calcularMarmol,
   que abrían WhatsApp con window.open), línea por línea, incluidos sus redondeos; casos congelados en
   tests/casos-materiales.json y la misma lógica en tools/site/componentes_materiales.py (paridad Python–JS). Los precios
   y los factores (camiones de tierra negra y saco de mármol incluidos) llegan en data-material, escrito desde datos.py:
   aquí no vive ningún precio. El botón es un enlace de WhatsApp con data-cta (terra.js lo mide como generate_lead y lo
   firma al hacer clic); sin área válida manda el mensaje de la página (data-mensaje). Las funciones puras se exportan para node --test. */
(function (root) {
  'use strict';
  const AREA_MAXIMA = 100000;
  const CIERRE = '¿Me pueden dar precio de entrega a domicilio en Tampico, Madero o Altamira?';
  const COLONIA = 'Colonia de entrega: ___';
  const dinero = (n) => '$' + Math.round(n).toLocaleString('es-MX');
  // "3750" → "3,750" y "1250.5" → "1,250.5": separa miles sin redondear los decimales (igual que miles() en Python).
  function miles(n) {
    const [entero, decimales] = String(n).split('.');
    return entero.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (decimales === undefined ? '' : `.${decimales}`);
  }
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

  // Camión de tierra negra donde cabe la cantidad (cfg.camiones: [[8, 5200], [14, 8000]] de datos.py), como
  // camion_tierra() en Python; si no cabe en uno, camiones del más grande.
  function camionTierra(cfg, m3) {
    const cabe = cfg.camiones.find(([capacidad]) => m3 <= capacidad);
    if (cabe) return `Camión volteo de ${cabe[0]} m³ (${dinero(cabe[1])})`;
    const [capacidad, precio] = cfg.camiones[cfg.camiones.length - 1];
    return `${miles(Math.ceil(m3 / capacidad))} camiones volteo de ${capacidad} m³ (${dinero(precio)} c/u)`;
  }

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
      return { sacos, kg: sacos * cfg.kg_saco, por_m2: porM2, total: sacos * cfg.precio_saco };
    }
    return { kg: [Math.round(area * cfg.kg_m2[0]), Math.round(area * cfg.kg_m2[1])] };
  }

  // Mensaje de WhatsApp: el resultado, la colonia por llenar y la pregunta de cierre (las cuatro calculadoras).
  const mensaje = (cfg, titulo, lineas) =>
    [`Hola, quiero cotizar ${cfg.texto}.`, '', titulo, ...lineas, COLONIA, '', CIERRE].join('\n');

  function textos(cfg, area, capa, r, uso) {
    const a = miles(area);
    if (cfg.clave === 'tierra-negra' || cfg.clave === 'tezontle') {
      const m3 = miles(r.m3);
      const c = miles(r.costales);
      let presentacion;
      let equivalente = `~${c} costales`;
      let lineas;
      if (cfg.clave === 'tierra-negra') {
        presentacion = r.tramo === 'costales' ? `${c} costales (${dinero(r.costales * cfg.precio_costal)})`
          : r.tramo === 'm3' ? `${m3} m³ suelto (~${dinero(r.m3 * cfg.precio_m3)})` : camionTierra(cfg, r.m3);
        if (r.tramo === 'costales') equivalente = `${c} costales`;
        lineas = [`Área: ${a} m²`, `Capa: ${Math.round(capa * 100)} cm`, `Cantidad: ${m3} m³`];
      } else {
        presentacion = { costales: `${c} costales`, m3: `${m3} m³ suelto`, camion: 'Camión 14 m³',
          camiones: `${miles(r.camiones)} camiones 14 m³` }[r.tramo];
        lineas = [`Área: ${a} m²`, `Uso: ${uso}`, `Cantidad: ${m3} m³`];
      }
      return { cantidad: `${m3} m³`, presentacion, equivalente,
        mensaje: mensaje(cfg, 'Resultado de la calculadora:', lineas) };
    }
    if (cfg.clave === 'marmol') {
      const g = String(capa);
      const s = miles(r.sacos);
      const total = dinero(r.total);
      const precio = ` A ${dinero(cfg.precio_saco)} c/u.`;
      const nota = capa <= 4 ? `${s} sacos cubren ${a} m² con capa de ${g} cm.${precio}`
        : `${s} sacos para ${a} m² con capa de ${g} cm (alta densidad).${precio}`;
      return { cantidad: `${s} sacos`, total, peso: `${miles(r.kg)} kg`, nota,
        mensaje: mensaje(cfg, 'Datos de mi proyecto:',
          [`Área: ${a} m²`, `Capa: ${g} cm`, `Cantidad: ${s} sacos`, `Precio estimado: ${total}`]) };
    }
    const cantidad = `${miles(r.kg[0])} a ${miles(r.kg[1])} kg`;
    return { cantidad, mensaje: mensaje(cfg, 'Resultado de la calculadora:',
      [`Área: ${a} m²`, `Capa: ${cfg.capa_texto}`, `Cantidad aprox.: ${cantidad}`]) };
  }

  // Estado vacío: el que escribió el HTML (componentes_materiales.VACIO); se lee al arrancar para no repetir textos.
  function iniciar(caja) {
    const cfg = JSON.parse(caja.dataset.material);
    const salida = (n) => caja.querySelector(`[data-vt-o="${n}"]`);
    const area = caja.querySelector('[data-vt-campo="area"]');
    const capa = caja.querySelector('[data-vt-campo="capa"]');
    const nombres = ['cantidad', 'presentacion', 'equivalente', 'total', 'peso'].filter((n) => salida(n));
    const vacio = Object.fromEntries(nombres.map((n) => [n, salida(n).textContent]));
    const nota = salida('nota');
    function actualizar() {
      const a = leerArea(area.value);
      salida('cantidad').parentElement.classList.toggle('is-vacio', !a);
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

  const api = { leerArea, calcular, textos, enlace, miles, CIERRE, COLONIA };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
    return;
  }
  root.VTMateriales = Object.freeze(api);
  const arrancar = () => document.querySelectorAll('[data-vt-material]').forEach(iniciar);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arrancar);
  else arrancar();
})(typeof window !== 'undefined' ? window : globalThis);
