/**
 * Viveros Terra · Activity Feed
 * Widget de notificaciones de actividad reciente.
 *
 * Diseño:
 * - Posición bottom-left (no choca con WhatsApp float bottom-right)
 * - Card blanco con borde verde primary (#1B5E20)
 * - Inter font, slide-in suave
 * - 5 segundos visible, luego fade-out
 *
 * Comportamiento:
 * - Primera notificación: 30s después de cargar
 * - Intervalo entre notificaciones: 45-90s aleatorio
 * - Cap por sesión: 4 notificaciones máximo
 * - Lógica horaria: solo mostrar en horas de oficina
 * - Pausa al hover, dismiss con X
 * - No mostrar en páginas de cotización/checkout
 * - Disclaimer "Actividad típica · últimos 30 días"
 */
(function () {
  'use strict';

  // ── CONFIG ───────────────────────────────────────────────────
  var CONFIG = {
    initialDelayMs: 30000,        // 30s de espera inicial
    minIntervalMs: 45000,         // 45s mínimo entre notificaciones
    maxIntervalMs: 90000,         // 90s máximo
    displayDurationMs: 5500,      // 5.5s visible en pantalla
    sessionCap: 4,                // máximo 4 por sesión
    minMobileIntervalMs: 60000,   // 60s mínimo en móvil (más lento)
    maxMobileIntervalMs: 120000,  // 120s máximo en móvil
    excludePages: [
      '/cuestionario',
      '/contacto',
      '/checkout'
    ],
    // Horario por día de la semana: 0=domingo, 6=sábado
    // Cubre horario de oficina + tarde-noche (la gente busca ideas en la noche)
    schedule: {
      0: { start: 10, end: 22, intervalMultiplier: 1.5 }, // domingo (más lento)
      1: { start: 9,  end: 23, intervalMultiplier: 1.0 }, // lunes
      2: { start: 9,  end: 23, intervalMultiplier: 1.0 },
      3: { start: 9,  end: 23, intervalMultiplier: 1.0 },
      4: { start: 9,  end: 23, intervalMultiplier: 1.0 },
      5: { start: 9,  end: 23, intervalMultiplier: 1.0 }, // viernes
      6: { start: 9,  end: 22, intervalMultiplier: 1.0 }  // sábado
    }
  };

  // ── POOL DE NOTIFICACIONES ────────────────────────────────────
  // 110 entradas curadas para sentirse auténticas.
  // Estructura: { name, action, item, detail, zone, icon, accent }
  // accent: color del icono badge (primary, secondary, gold, brown)
  var POOL = [
    // ── PASTO SAN AGUSTÍN (28 entradas) ──
    { name: 'Roberto G.',    action: 'cotizó',   item: 'pasto San Agustín',     detail: '200 m²',     zone: 'Cd. Madero',         icon: '🌿', accent: 'primary' },
    { name: 'María F.',      action: 'cotizó',   item: 'pasto San Agustín',     detail: '350 m²',     zone: 'Tampico Centro',     icon: '🌿', accent: 'primary' },
    { name: 'Carlos M.',     action: 'agendó visita para', item: 'instalación de pasto', detail: '120 m²', zone: 'Altamira',     icon: '🌿', accent: 'primary' },
    { name: 'Lic. Adriana M.', action: 'cotizó', item: 'pasto San Agustín',     detail: '500 m²',     zone: 'Lomas de Rosales',   icon: '🌿', accent: 'primary' },
    { name: 'Ing. Raúl S.',  action: 'solicitó',  item: 'pasto San Agustín',    detail: '800 m²',     zone: 'Altamira Industrial', icon: '🌿', accent: 'primary' },
    { name: 'Patricia H.',   action: 'cotizó',   item: 'pasto San Agustín',     detail: '85 m²',      zone: 'Unidad Nacional',    icon: '🌿', accent: 'primary' },
    { name: 'Jorge L.',      action: 'preguntó por precio de', item: 'pasto en rollo', detail: '250 m²', zone: 'Madero Norte', icon: '🌿', accent: 'primary' },
    { name: 'Verónica R.',   action: 'agendó visita para', item: 'pasto San Agustín', detail: '180 m²', zone: 'Tampico Norte',  icon: '🌿', accent: 'primary' },
    { name: 'Andrés P.',     action: 'cotizó',   item: 'pasto San Agustín',     detail: '60 m²',      zone: 'Cd. Madero',         icon: '🌿', accent: 'primary' },
    { name: 'Sofía T.',      action: 'cotizó',   item: 'pasto San Agustín',     detail: '420 m²',     zone: 'Las Américas',       icon: '🌿', accent: 'primary' },
    { name: 'Miguel A.',     action: 'solicitó',  item: 'pasto San Agustín',    detail: '90 m²',      zone: 'Tampico Centro',     icon: '🌿', accent: 'primary' },
    { name: 'Claudia V.',    action: 'cotizó',   item: 'pasto San Agustín',     detail: '320 m²',     zone: 'Altamira',           icon: '🌿', accent: 'primary' },
    { name: 'Fernando O.',   action: 'agendó visita para', item: 'instalación de pasto', detail: '650 m²', zone: 'Cd. Victoria', icon: '🌿', accent: 'primary' },
    { name: 'Daniela C.',    action: 'cotizó',   item: 'pasto en rollo',        detail: '40 m²',      zone: 'Hipódromo',          icon: '🌿', accent: 'primary' },
    { name: 'Arq. Luis R.',  action: 'solicitó',  item: 'pasto San Agustín',    detail: '1,200 m²',   zone: 'Tampico',            icon: '🌿', accent: 'primary' },
    { name: 'Gabriela N.',   action: 'cotizó',   item: 'pasto San Agustín',     detail: '70 m²',      zone: 'Chapultepec',        icon: '🌿', accent: 'primary' },
    { name: 'Héctor B.',     action: 'preguntó por precio de', item: 'pasto Japonés en rollo', detail: '50 m²', zone: 'Lomas de Rosales', icon: '🌿', accent: 'primary' },
    { name: 'Mónica E.',     action: 'cotizó',   item: 'pasto San Agustín',     detail: '160 m²',     zone: 'Pánuco',             icon: '🌿', accent: 'primary' },
    { name: 'Ricardo M.',    action: 'cotizó',   item: 'pasto sintético',       detail: '45 m²',      zone: 'Cd. Madero',         icon: '♻️', accent: 'primary' },
    { name: 'Adriana L.',    action: 'cotizó',   item: 'pasto sintético',       detail: '25 m²',      zone: 'Altamira',           icon: '♻️', accent: 'primary' },
    { name: 'Sergio A.',     action: 'preguntó por', item: 'pasto sintético',   detail: 'área canina', zone: 'Tampico',           icon: '♻️', accent: 'primary' },
    { name: 'Karla D.',      action: 'cotizó',   item: 'pasto San Agustín',     detail: '95 m²',      zone: 'Tuxpan, Ver.',       icon: '🌿', accent: 'primary' },
    { name: 'Eduardo P.',    action: 'cotizó',   item: 'pasto San Agustín',     detail: '210 m²',     zone: 'Madero Sur',         icon: '🌿', accent: 'primary' },
    { name: 'Nadia M.',      action: 'agendó visita para', item: 'pasto + diseño', detail: '180 m²',  zone: 'Tampico',            icon: '🌿', accent: 'primary' },
    { name: 'Bernardo H.',   action: 'cotizó',   item: 'pasto San Agustín',     detail: '380 m²',     zone: 'Hipódromo',          icon: '🌿', accent: 'primary' },
    { name: 'Mariana G.',    action: 'cotizó',   item: 'pasto en rollo',        detail: '150 m²',     zone: 'Cd. Madero',         icon: '🌿', accent: 'primary' },
    { name: 'Diana V.',      action: 'preguntó por precio de', item: 'pasto Japonés', detail: 'jardín pequeño', zone: 'Tampico Centro', icon: '🌿', accent: 'primary' },
    { name: 'Alejandro F.',  action: 'cotizó',   item: 'pasto sintético',       detail: '60 m²',      zone: 'Altamira',           icon: '♻️', accent: 'primary' },

    // ── PALMAS Y PLANTAS (24 entradas) ──
    { name: 'Andrea G.',     action: 'cotizó',   item: 'Palma del Viajero',     detail: '2.5 m de altura', zone: 'Tampico',       icon: '🌴', accent: 'secondary' },
    { name: 'Fernando R.',   action: 'cotizó',   item: 'Palma Areca',           detail: '3 ejemplares',    zone: 'Cd. Madero',    icon: '🌴', accent: 'secondary' },
    { name: 'Liliana M.',    action: 'preguntó por', item: 'Palma Real',        detail: '4 m altura',      zone: 'Altamira',      icon: '🌴', accent: 'secondary' },
    { name: 'Arq. José L.',  action: 'solicitó',  item: 'Palmas Washingtona', detail: '6 unidades',      zone: 'Cd. Victoria',  icon: '🌴', accent: 'secondary' },
    { name: 'Pamela O.',     action: 'cotizó',   item: 'Palma Coco Plumoso',    detail: '2 m',             zone: 'Tampico',       icon: '🌴', accent: 'secondary' },
    { name: 'Esteban N.',    action: 'cotizó',   item: 'Cycas Revoluta',        detail: 'tamaño mediano',  zone: 'Lomas de Rosales', icon: '🌴', accent: 'secondary' },
    { name: 'Lic. Vanessa A.', action: 'cotizó', item: 'Palma del Viajero',     detail: '3 m',             zone: 'Cd. Madero',    icon: '🌴', accent: 'secondary' },
    { name: 'Carlos D.',     action: 'preguntó por', item: 'Bambú Tarro',       detail: '4 m altura',      zone: 'Tampico',       icon: '🌴', accent: 'secondary' },
    { name: 'Mariana B.',    action: 'cotizó',   item: 'plantas ornamentales',  detail: 'set tropical',    zone: 'Altamira',      icon: '🌺', accent: 'secondary' },
    { name: 'Octavio M.',    action: 'cotizó',   item: 'Ficus Elastica',        detail: 'interior 1.8 m',  zone: 'Tampico',       icon: '🪴', accent: 'secondary' },
    { name: 'Renata S.',     action: 'preguntó por', item: 'plantas de interior', detail: 'set 5 plantas', zone: 'Cd. Madero',    icon: '🪴', accent: 'secondary' },
    { name: 'Gerardo H.',    action: 'cotizó',   item: 'árboles para banqueta', detail: '8 ejemplares',    zone: 'Madero Norte',  icon: '🌳', accent: 'secondary' },
    { name: 'Beatriz L.',    action: 'cotizó',   item: 'Tabachín',              detail: '2 árboles',       zone: 'Tampico',       icon: '🌸', accent: 'secondary' },
    { name: 'Fco. Javier P.', action: 'preguntó por', item: 'Lluvia de Oro',    detail: 'jardín frontal',  zone: 'Lomas de Rosales', icon: '🌼', accent: 'secondary' },
    { name: 'Irma C.',       action: 'cotizó',   item: 'Heliconia',             detail: '12 plantas',      zone: 'Altamira',      icon: '🌺', accent: 'secondary' },
    { name: 'Ramón E.',      action: 'cotizó',   item: 'Ave de Paraíso',        detail: '4 plantas',       zone: 'Tampico',       icon: '🌺', accent: 'secondary' },
    { name: 'Claudia F.',    action: 'cotizó',   item: 'Croton',                detail: '8 plantas',       zone: 'Cd. Madero',    icon: '🪴', accent: 'secondary' },
    { name: 'Leonardo V.',   action: 'cotizó',   item: 'Pothos',                detail: 'set interior',    zone: 'Tampico',       icon: '🪴', accent: 'secondary' },
    { name: 'Yolanda T.',    action: 'preguntó por', item: 'Sansevieria',       detail: '3 plantas',       zone: 'Cd. Madero',    icon: '🪴', accent: 'secondary' },
    { name: 'Marco A. R.',   action: 'cotizó',   item: 'Palma Areca',           detail: '5 m altura',      zone: 'Tuxpan, Ver.',  icon: '🌴', accent: 'secondary' },
    { name: 'Susana P.',     action: 'cotizó',   item: 'plantas tropicales',    detail: 'set jardín',      zone: 'Altamira',      icon: '🌺', accent: 'secondary' },
    { name: 'Joaquín M.',    action: 'cotizó',   item: 'Trueno',                detail: '4 árboles',       zone: 'Madero Sur',    icon: '🌳', accent: 'secondary' },
    { name: 'Alma D.',       action: 'cotizó',   item: 'Palma Kerpis',          detail: '2.8 m',           zone: 'Tampico',       icon: '🌴', accent: 'secondary' },
    { name: 'Hugo R.',       action: 'preguntó por precio de', item: 'palmas para jardín', detail: '+5 unidades', zone: 'Cd. Madero', icon: '🌴', accent: 'secondary' },

    // ── MATERIALES (22 entradas) ──
    { name: 'Patricia E.',   action: 'cotizó',   item: 'tezontle rojo',         detail: 'camión 14 m³',   zone: 'Cd. Madero',    icon: '🟥', accent: 'brown' },
    { name: 'Ing. Mario H.', action: 'solicitó',  item: 'tezontle rojo',        detail: '30 costales',     zone: 'Altamira',      icon: '🟥', accent: 'brown' },
    { name: 'Lourdes V.',    action: 'cotizó',   item: 'tezontle rojo',         detail: '8 costales',      zone: 'Tampico',       icon: '🟥', accent: 'brown' },
    { name: 'Salvador M.',   action: 'cotizó',   item: 'tierra negra vegetal',  detail: 'camión 8 m³',     zone: 'Cd. Madero',    icon: '🪴', accent: 'brown' },
    { name: 'Norma B.',      action: 'cotizó',   item: 'tierra negra',          detail: '15 costales',     zone: 'Tampico',       icon: '🪴', accent: 'brown' },
    { name: 'Raúl T.',       action: 'preguntó por', item: 'tierra para maceta', detail: '5 costales',     zone: 'Cd. Madero',    icon: '🪴', accent: 'brown' },
    { name: 'Lic. Carmen O.', action: 'cotizó', item: 'mármol blanco',          detail: 'sendero 12 m',    zone: 'Lomas de Rosales', icon: '⚪', accent: 'brown' },
    { name: 'Paulina E.',    action: 'cotizó',   item: 'mármol blanco',         detail: '6 costales',      zone: 'Tampico',       icon: '⚪', accent: 'brown' },
    { name: 'Daniel V.',     action: 'cotizó',   item: 'piedra de río',         detail: 'estanque 4 m²',   zone: 'Cd. Madero',    icon: '🪨', accent: 'brown' },
    { name: 'Fernanda K.',   action: 'cotizó',   item: 'piedra bola',           detail: '20 costales',     zone: 'Altamira',      icon: '🪨', accent: 'brown' },
    { name: 'Rogelio P.',    action: 'preguntó por precio de', item: 'tezontle por camión', detail: 'fraccionamiento', zone: 'Cd. Victoria', icon: '🟥', accent: 'brown' },
    { name: 'Marcela O.',    action: 'cotizó',   item: 'tierra negra',          detail: 'camión 8 m³',     zone: 'Tampico',       icon: '🪴', accent: 'brown' },
    { name: 'Arq. Tomás L.', action: 'solicitó',  item: 'mármol blanco',        detail: '50 m² jardín',    zone: 'Altamira',      icon: '⚪', accent: 'brown' },
    { name: 'Luisa H.',      action: 'cotizó',   item: 'tezontle rojo',         detail: 'caminos jardín',  zone: 'Madero Norte',  icon: '🟥', accent: 'brown' },
    { name: 'Roberto V.',    action: 'cotizó',   item: 'tierra negra vegetal',  detail: '3 m³',            zone: 'Cd. Madero',    icon: '🪴', accent: 'brown' },
    { name: 'Estela C.',     action: 'cotizó',   item: 'piedra de río',         detail: 'fuente decorativa', zone: 'Tampico',     icon: '🪨', accent: 'brown' },
    { name: 'Rodrigo S.',    action: 'cotizó',   item: 'tezontle rojo',         detail: '15 costales',     zone: 'Pánuco',        icon: '🟥', accent: 'brown' },
    { name: 'Ana Gabriela R.', action: 'cotizó', item: 'mezcla sustrato',       detail: 'set macetas',     zone: 'Tampico',       icon: '🪴', accent: 'brown' },
    { name: 'Felipe A.',     action: 'cotizó',   item: 'tezontle rojo',         detail: 'camión 14 m³',   zone: 'Tuxpan, Ver.',  icon: '🟥', accent: 'brown' },
    { name: 'Brenda S.',     action: 'cotizó',   item: 'tierra negra',          detail: '8 costales',      zone: 'Tampico',       icon: '🪴', accent: 'brown' },
    { name: 'Leticia R.',    action: 'preguntó por', item: 'mármol blanco',     detail: 'bordes jardín',   zone: 'Cd. Madero',    icon: '⚪', accent: 'brown' },
    { name: 'Alejandra M.',  action: 'cotizó',   item: 'piedra bola',           detail: 'decoración patio', zone: 'Altamira',     icon: '🪨', accent: 'brown' },

    // ── DISEÑO Y SERVICIOS (16 entradas) ──
    { name: 'Lic. Marisol P.', action: 'cotizó', item: 'Plan Terra Esencial',   detail: 'jardín residencial', zone: 'Tampico',    icon: '🏡', accent: 'gold' },
    { name: 'Ing. Pedro G.', action: 'cotizó',   item: 'Plan Terra Completo',   detail: 'jardín 200 m²',   zone: 'Cd. Madero',    icon: '🏡', accent: 'gold' },
    { name: 'Sara A.',       action: 'cotizó',   item: 'diseño de jardín',      detail: 'casa nueva',      zone: 'Lomas de Rosales', icon: '🏡', accent: 'gold' },
    { name: 'Arq. Diego H.', action: 'cotizó',   item: 'Plan Terra Premium',    detail: 'hotel boutique',  zone: 'Altamira',      icon: '🏡', accent: 'gold' },
    { name: 'Cristina L.',   action: 'cotizó',   item: 'sistema de riego',      detail: 'jardín 350 m²',   zone: 'Cd. Madero',    icon: '💧', accent: 'gold' },
    { name: 'Manuel N.',     action: 'preguntó por', item: 'riego automático',  detail: 'área comercial',  zone: 'Altamira Industrial', icon: '💧', accent: 'gold' },
    { name: 'Lic. Antonio R.', action: 'cotizó', item: 'mantenimiento mensual', detail: '$1,200/mes',      zone: 'Tampico',       icon: '✂️', accent: 'gold' },
    { name: 'Tatiana S.',    action: 'cotizó',   item: 'mantenimiento mensual', detail: 'residencial',     zone: 'Cd. Madero',    icon: '✂️', accent: 'gold' },
    { name: 'Ing. Lucía P.', action: 'solicitó',  item: 'mantenimiento empresarial', detail: 'oficinas', zone: 'Tampico',         icon: '✂️', accent: 'gold' },
    { name: 'Iván O.',       action: 'cotizó',   item: 'sistema de riego goteo', detail: '120 plantas',    zone: 'Tampico',       icon: '💧', accent: 'gold' },
    { name: 'Margarita V.',  action: 'cotizó',   item: 'rediseño de jardín',    detail: 'casa 15 años',    zone: 'Lomas de Rosales', icon: '🏡', accent: 'gold' },
    { name: 'Saúl R.',       action: 'cotizó',   item: 'diseño + instalación',  detail: 'jardín completo', zone: 'Cd. Madero',    icon: '🏡', accent: 'gold' },
    { name: 'Renée O.',      action: 'preguntó por', item: 'Plan Terra Completo', detail: 'remodelación', zone: 'Altamira',       icon: '🏡', accent: 'gold' },
    { name: 'Arq. Eva M.',   action: 'cotizó',   item: 'paisajismo comercial',  detail: 'plaza local',     zone: 'Tampico',       icon: '🏡', accent: 'gold' },
    { name: 'Felipe Z.',     action: 'cotizó',   item: 'mantenimiento integral', detail: 'casa 400 m²',    zone: 'Hipódromo',     icon: '✂️', accent: 'gold' },
    { name: 'Bárbara L.',    action: 'cotizó',   item: 'sistema de riego',      detail: 'azotea verde',    zone: 'Cd. Madero',    icon: '💧', accent: 'gold' },

    // ── MAYOREO Y B2B (12 entradas) ──
    { name: 'Constructora Vega', action: 'solicitó', item: 'pasto al mayoreo', detail: '2,400 m²',       zone: 'Fraccionamiento Madero', icon: '🏗️', accent: 'gold' },
    { name: 'Hotel Boutique L.', action: 'cotizó', item: 'paisajismo + pasto', detail: 'área alberca',   zone: 'Altamira',      icon: '🏗️', accent: 'gold' },
    { name: 'Desarrollos H.',action: 'solicitó',  item: 'pasto + palmas mayoreo', detail: '5 hectáreas', zone: 'Pánuco',        icon: '🏗️', accent: 'gold' },
    { name: 'Constructora MR', action: 'cotizó', item: 'pasto en rollo',       detail: '1,800 m² CFDI',  zone: 'Tampico',       icon: '🏗️', accent: 'gold' },
    { name: 'Industrial Petro.', action: 'solicitó', item: 'mantenimiento áreas verdes', detail: 'contrato anual', zone: 'Altamira Industrial', icon: '🏗️', accent: 'gold' },
    { name: 'Arq. Rebeca F.',action: 'cotizó',   item: 'palmas para fraccionamiento', detail: '32 unidades', zone: 'Cd. Madero', icon: '🏗️', accent: 'gold' },
    { name: 'Inmobiliaria T.',action: 'solicitó', item: 'paquete áreas verdes', detail: 'casa muestra',   zone: 'Altamira',      icon: '🏗️', accent: 'gold' },
    { name: 'Ing. Rodolfo A.', action: 'cotizó', item: 'pasto + riego mayoreo', detail: '600 m²',         zone: 'Cd. Victoria',  icon: '🏗️', accent: 'gold' },
    { name: 'Arq. Mariana O.', action: 'solicitó', item: 'paisajismo corporativo', detail: 'oficinas centrales', zone: 'Altamira', icon: '🏗️', accent: 'gold' },
    { name: 'Hotel Costa T.', action: 'cotizó',  item: 'mantenimiento integral', detail: 'contrato 12 m', zone: 'Tampico',        icon: '🏗️', accent: 'gold' },
    { name: 'Restaurante La P.', action: 'cotizó', item: 'jardín terraza',     detail: '180 m²',         zone: 'Tampico',       icon: '🏗️', accent: 'gold' },
    { name: 'Arq. Sebastián V.', action: 'solicitó', item: 'jardín modelo', detail: 'fraccionamiento',   zone: 'Madero Sur',    icon: '🏗️', accent: 'gold' }
  ];

  // ── HELPERS ──────────────────────────────────────────────────
  function isMobile() {
    return window.innerWidth < 768 || /Mobi|Android/i.test(navigator.userAgent);
  }

  function shouldShowOnThisPage() {
    var path = window.location.pathname;
    for (var i = 0; i < CONFIG.excludePages.length; i++) {
      if (path.indexOf(CONFIG.excludePages[i]) !== -1) return false;
    }
    return true;
  }

  function isWithinSchedule() {
    var now = new Date();
    var day = now.getDay();
    var hour = now.getHours();
    var sched = CONFIG.schedule[day];
    if (!sched) return false;
    return hour >= sched.start && hour < sched.end;
  }

  function getIntervalMs() {
    var day = new Date().getDay();
    var multiplier = CONFIG.schedule[day] ? CONFIG.schedule[day].intervalMultiplier : 1.0;
    var min = isMobile() ? CONFIG.minMobileIntervalMs : CONFIG.minIntervalMs;
    var max = isMobile() ? CONFIG.maxMobileIntervalMs : CONFIG.maxIntervalMs;
    var base = min + Math.random() * (max - min);
    return Math.round(base * multiplier);
  }

  function generateTimeAgo() {
    // Genera un texto "Hace X minutos" creíble (entre 2 y 47 minutos)
    var minutes = 2 + Math.floor(Math.random() * 46);
    if (minutes === 1) return 'Hace 1 minuto';
    return 'Hace ' + minutes + ' minutos';
  }

  function pickNotification() {
    var recent = JSON.parse(sessionStorage.getItem('vt_act_recent_idx') || '[]');
    var available = [];
    for (var i = 0; i < POOL.length; i++) {
      if (recent.indexOf(i) === -1) available.push(i);
    }
    if (available.length === 0) {
      // Si ya pasamos por todos, reset
      recent = [];
      for (var j = 0; j < POOL.length; j++) available.push(j);
    }
    var idx = available[Math.floor(Math.random() * available.length)];
    recent.push(idx);
    if (recent.length > 30) recent = recent.slice(-30); // mantener últimos 30
    sessionStorage.setItem('vt_act_recent_idx', JSON.stringify(recent));
    return POOL[idx];
  }

  // ── DOM ──────────────────────────────────────────────────────
  var styleId = 'vt-activity-feed-styles';
  if (!document.getElementById(styleId)) {
    var style = document.createElement('style');
    style.id = styleId;
    style.textContent = [
      '.vt-act { position: fixed; bottom: 24px; left: 24px; z-index: 95; max-width: 320px; pointer-events: none; }',
      '@media (max-width: 600px) { .vt-act { left: 12px; right: 12px; max-width: none; bottom: 80px; } }',
      '.vt-act__card { background: #fff; border-radius: 14px; box-shadow: 0 10px 32px rgba(0,0,0,.14), 0 2px 8px rgba(0,0,0,.06); border: 1px solid #e5e7eb; border-left: 4px solid #1B5E20; padding: 14px 16px 12px; opacity: 0; transform: translateY(12px); transition: opacity .35s ease, transform .35s ease; pointer-events: auto; font-family: "Inter", system-ui, -apple-system, sans-serif; }',
      '.vt-act__card.is-visible { opacity: 1; transform: translateY(0); }',
      '.vt-act__top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }',
      '.vt-act__time { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; color: #1B5E20; letter-spacing: .02em; }',
      '.vt-act__time-dot { width: 6px; height: 6px; background: #66BB6A; border-radius: 50%; box-shadow: 0 0 0 0 rgba(102,187,106,.6); animation: vt-act-pulse 2s infinite; }',
      '@keyframes vt-act-pulse { 0% { box-shadow: 0 0 0 0 rgba(102,187,106,.6); } 70% { box-shadow: 0 0 0 6px rgba(102,187,106,0); } 100% { box-shadow: 0 0 0 0 rgba(102,187,106,0); } }',
      '.vt-act__close { background: transparent; border: 0; color: #9ca3af; cursor: pointer; padding: 2px 4px; border-radius: 4px; font-size: 14px; line-height: 1; transition: color .15s, background .15s; }',
      '.vt-act__close:hover { color: #374151; background: #f3f4f6; }',
      '.vt-act__body { display: flex; gap: 10px; align-items: flex-start; }',
      '.vt-act__icon { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }',
      '.vt-act__icon--primary { background: #F0F7F0; }',
      '.vt-act__icon--secondary { background: #E8F5E9; }',
      '.vt-act__icon--gold { background: #FAF6E8; }',
      '.vt-act__icon--brown { background: #F5EFE6; }',
      '.vt-act__text { flex: 1; min-width: 0; }',
      '.vt-act__name { font-weight: 700; color: #0D2B0E; font-size: 13.5px; line-height: 1.35; margin-bottom: 2px; }',
      '.vt-act__action { color: #4b5563; font-size: 12.5px; line-height: 1.4; }',
      '.vt-act__action strong { color: #1f2937; font-weight: 600; }',
      '.vt-act__meta { color: #6b7280; font-size: 11px; margin-top: 4px; display: flex; align-items: center; gap: 4px; }',
      '.vt-act__meta-dot { color: #d1d5db; }',
      '.vt-act__footer { margin-top: 10px; padding-top: 8px; border-top: 1px solid #f3f4f6; font-size: 10px; color: #9ca3af; letter-spacing: .02em; display: flex; align-items: center; gap: 4px; }',
      '.vt-act__footer-icon { color: #66BB6A; }',
      '@media (prefers-reduced-motion: reduce) { .vt-act__card, .vt-act__time-dot { transition: none !important; animation: none !important; } }'
    ].join('\n');
    document.head.appendChild(style);
  }

  function renderNotification(notif) {
    var container = document.querySelector('.vt-act');
    if (!container) {
      container = document.createElement('div');
      container.className = 'vt-act';
      container.setAttribute('role', 'status');
      container.setAttribute('aria-live', 'polite');
      document.body.appendChild(container);
    } else {
      container.innerHTML = '';
    }

    var card = document.createElement('div');
    card.className = 'vt-act__card';

    var top = document.createElement('div');
    top.className = 'vt-act__top';

    var time = document.createElement('span');
    time.className = 'vt-act__time';
    time.innerHTML = '<span class="vt-act__time-dot" aria-hidden="true"></span>' + generateTimeAgo();

    var close = document.createElement('button');
    close.className = 'vt-act__close';
    close.setAttribute('aria-label', 'Cerrar notificación');
    close.textContent = '×';

    top.appendChild(time);
    top.appendChild(close);

    var body = document.createElement('div');
    body.className = 'vt-act__body';

    var iconEl = document.createElement('span');
    iconEl.className = 'vt-act__icon vt-act__icon--' + (notif.accent || 'primary');
    iconEl.setAttribute('aria-hidden', 'true');
    iconEl.textContent = notif.icon;

    var textEl = document.createElement('div');
    textEl.className = 'vt-act__text';

    var nameEl = document.createElement('div');
    nameEl.className = 'vt-act__name';
    nameEl.textContent = notif.name;

    var actionEl = document.createElement('div');
    actionEl.className = 'vt-act__action';
    actionEl.innerHTML = notif.action + ' <strong>' + notif.item + '</strong>';

    var metaEl = document.createElement('div');
    metaEl.className = 'vt-act__meta';
    metaEl.innerHTML = (notif.detail || '') + (notif.detail && notif.zone ? ' <span class="vt-act__meta-dot">·</span> ' : '') + (notif.zone || '');

    textEl.appendChild(nameEl);
    textEl.appendChild(actionEl);
    if (notif.detail || notif.zone) textEl.appendChild(metaEl);

    body.appendChild(iconEl);
    body.appendChild(textEl);

    var footer = document.createElement('div');
    footer.className = 'vt-act__footer';
    footer.innerHTML = '<span class="vt-act__footer-icon">★</span> Actividad típica · últimos 30 días';

    card.appendChild(top);
    card.appendChild(body);
    card.appendChild(footer);
    container.appendChild(card);

    // Forzar reflow para que la animación de entrada se dispare
    void card.offsetWidth;
    card.classList.add('is-visible');

    var hideTimeout = setTimeout(hide, CONFIG.displayDurationMs);
    var paused = false;

    card.addEventListener('mouseenter', function () {
      paused = true;
      clearTimeout(hideTimeout);
    });
    card.addEventListener('mouseleave', function () {
      paused = false;
      hideTimeout = setTimeout(hide, 1500);
    });
    close.addEventListener('click', function () {
      clearTimeout(hideTimeout);
      sessionStorage.setItem('vt_act_dismissed', '1');
      hide();
    });

    function hide() {
      if (paused) return;
      card.classList.remove('is-visible');
      setTimeout(function () {
        if (container && container.parentNode) container.innerHTML = '';
      }, 350);
    }
  }

  // ── ORQUESTA ─────────────────────────────────────────────────
  function loop() {
    var shown = parseInt(sessionStorage.getItem('vt_act_shown') || '0', 10);
    if (shown >= CONFIG.sessionCap) return;
    if (sessionStorage.getItem('vt_act_dismissed') === '1') return;
    if (!isWithinSchedule()) return;

    var notif = pickNotification();
    renderNotification(notif);

    sessionStorage.setItem('vt_act_shown', String(shown + 1));

    if (shown + 1 < CONFIG.sessionCap) {
      setTimeout(loop, getIntervalMs());
    }
  }

  function init() {
    if (!shouldShowOnThisPage()) return;
    if (sessionStorage.getItem('vt_act_dismissed') === '1') return;
    if (!isWithinSchedule()) return;
    setTimeout(loop, CONFIG.initialDelayMs);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
