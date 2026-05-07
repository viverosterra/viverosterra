#!/usr/bin/env python3
"""
Reemplaza el navbar terra-nav en todos los HTML del sitio viverosterra.com.
Aplica 3 transformaciones por archivo:
1. CSS: actualiza .terra-nav__dropdown width y añade reglas de sección
2. HTML: reemplaza <nav class="terra-nav">...</nav>
3. JS: reemplaza el <script> IIFE que viene después del </nav>
Preserva el data-page="..." específico de cada página.
"""
import re
import pathlib
import sys

BASE = pathlib.Path('/tmp/viverosterra-site/public')

NEW_NAV_INNER = '''
  <div class="terra-nav__inner">

    <!-- LOGO -->
    <a href="/" class="terra-nav__logo" aria-label="Viveros Terra — Inicio">
      <img src="/img/logo-viveros-terra-tampico.svg" alt="Viveros Terra" />
    </a>

    <!-- LINKS DESKTOP -->
    <div class="terra-nav__links">
      <div class="terra-nav__drop">
        <button class="terra-nav__drop-trigger" aria-expanded="false" aria-haspopup="true">
          Servicios
          <svg class="terra-nav__chevron" viewBox="0 0 10 6" fill="none">
            <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="terra-nav__dropdown" id="dropdown-servicios" role="menu">
          <div class="terra-nav__drop-col">
            <div class="terra-nav__drop-section">
              <div class="terra-nav__drop-header">Servicios de Jardinería</div>
              <a class="terra-nav__drop-item" href="/pasto-en-rollo-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🌿</span>
                <span class="terra-nav__drop-text"><strong>Pasto en Rollo San Agustín</strong><span>Instalación desde $85/m² · Mayoreo</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/pasto-sintetico-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">♻️</span>
                <span class="terra-nav__drop-text"><strong>Pasto Sintético</strong><span>Verde todo el año, sin mantenimiento</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/diseno-jardines-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🏡</span>
                <span class="terra-nav__drop-text"><strong>Diseño de Jardines</strong><span>Plan Terra desde $3,000</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/mantenimiento-jardines-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">✂️</span>
                <span class="terra-nav__drop-text"><strong>Mantenimiento</strong><span>Desde $750/mes · Residencial e industrial</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/sistema-riego-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">💧</span>
                <span class="terra-nav__drop-text"><strong>Sistema de Riego</strong><span>Automatizado · Ahorra 40% agua</span></span>
              </a>
            </div>
            <div class="terra-nav__drop-section">
              <div class="terra-nav__drop-header">Plantas y Palmas</div>
              <a class="terra-nav__drop-item" href="/plantas-palmas-arboles-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🌴</span>
                <span class="terra-nav__drop-text"><strong>Catálogo de Plantas</strong><span>+118 especies del vivero</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/palmas-tropicales-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🥥</span>
                <span class="terra-nav__drop-text"><strong>Palmas Tropicales</strong><span>Viajero, Areca, Real, Coco y más</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/arboles-para-banqueta-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🌳</span>
                <span class="terra-nav__drop-text"><strong>Árboles para Banqueta</strong><span>7 especies que no levantan pavimento</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/plantas-de-interior-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🪟</span>
                <span class="terra-nav__drop-text"><strong>Plantas de Interior</strong><span>Pothos, Sansevieria, Aglaonema</span></span>
              </a>
            </div>
          </div>
          <div class="terra-nav__drop-col">
            <div class="terra-nav__drop-section">
              <div class="terra-nav__drop-header">Materiales</div>
              <a class="terra-nav__drop-item" href="/tierra-negra-vegetal-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🪴</span>
                <span class="terra-nav__drop-text"><strong>Tierra Negra y Sustratos</strong><span>Costal $90 · Camión volteo</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/tezontle-rojo-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🟥</span>
                <span class="terra-nav__drop-text"><strong>Tezontle Rojo</strong><span>Costal $120 · Por m³</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/marmol-blanco-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">⚪</span>
                <span class="terra-nav__drop-text"><strong>Mármol Blanco</strong><span>Decorativo · Senderos · Bordes</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/piedra-bola-rio-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🪨</span>
                <span class="terra-nav__drop-text"><strong>Piedra de Río / Bola</strong><span>Senderos · Estanques · Drenaje</span></span>
              </a>
            </div>
            <div class="terra-nav__drop-section">
              <div class="terra-nav__drop-header">Por Zona · B2B</div>
              <a class="terra-nav__drop-item" href="/vivero-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">📍</span>
                <span class="terra-nav__drop-text"><strong>Vivero en Tampico</strong><span>+150 variedades en Cd. Madero</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/jardineria-ciudad-madero" role="menuitem">
                <span class="terra-nav__drop-icon">📍</span>
                <span class="terra-nav__drop-text"><strong>Jardinería Ciudad Madero</strong><span>Local · Sin recargo por zona</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/jardineria-altamira" role="menuitem">
                <span class="terra-nav__drop-icon">📍</span>
                <span class="terra-nav__drop-text"><strong>Jardinería Altamira</strong><span>Industrial y residencial</span></span>
              </a>
              <a class="terra-nav__drop-item" href="/mayoreo-pasto-tampico" role="menuitem">
                <span class="terra-nav__drop-icon">🏗️</span>
                <span class="terra-nav__drop-text"><strong>Mayoreo Constructoras</strong><span>Precio por volumen · CFDI</span></span>
              </a>
            </div>
          </div>
        </div>
      </div>
      <a href="/catalogo" class="terra-nav__link">Catálogo</a>
      <a href="/blog" class="terra-nav__link">Blog</a>
    </div>

    <div class="terra-nav__right">
      <a href="tel:8333268008" class="terra-nav__tel" aria-label="Llamar a Viveros Terra">
        <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.169c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58L3.654 1.328z"/></svg>
        833 326 8008
      </a>
      <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20una%20cotización%20de%20Viveros%20Terra" class="terra-nav__cta" target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Cotizar por WhatsApp
      </a>
    </div>

    <button class="terra-nav__hamburger" aria-expanded="false" aria-controls="terra-nav-drawer" aria-label="Abrir menú">
      <span></span><span></span><span></span>
    </button>
  </div>

  <div class="terra-nav__drawer" id="terra-nav-drawer">
    <button class="terra-nav__drawer-sub-toggle" aria-expanded="false" data-target="drawer-sub-servicios">
      🌱 Servicios de Jardinería
      <svg class="terra-nav__chevron" style="margin-left:auto;width:12px;height:12px;" viewBox="0 0 10 6" fill="none">
        <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="terra-nav__drawer-sub" id="drawer-sub-servicios">
      <a href="/pasto-en-rollo-tampico">Pasto en Rollo San Agustín</a>
      <a href="/pasto-sintetico-tampico">Pasto Sintético</a>
      <a href="/diseno-jardines-tampico">Diseño de Jardines</a>
      <a href="/mantenimiento-jardines-tampico">Mantenimiento</a>
      <a href="/sistema-riego-tampico">Sistema de Riego</a>
    </div>
    <button class="terra-nav__drawer-sub-toggle" aria-expanded="false" data-target="drawer-sub-plantas">
      🌴 Plantas y Palmas
      <svg class="terra-nav__chevron" style="margin-left:auto;width:12px;height:12px;" viewBox="0 0 10 6" fill="none">
        <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="terra-nav__drawer-sub" id="drawer-sub-plantas">
      <a href="/plantas-palmas-arboles-tampico">Catálogo de Plantas</a>
      <a href="/palmas-tropicales-tampico">Palmas Tropicales</a>
      <a href="/arboles-para-banqueta-tampico">Árboles para Banqueta</a>
      <a href="/plantas-de-interior-tampico">Plantas de Interior</a>
    </div>
    <button class="terra-nav__drawer-sub-toggle" aria-expanded="false" data-target="drawer-sub-materiales">
      🪨 Materiales
      <svg class="terra-nav__chevron" style="margin-left:auto;width:12px;height:12px;" viewBox="0 0 10 6" fill="none">
        <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="terra-nav__drawer-sub" id="drawer-sub-materiales">
      <a href="/tierra-negra-vegetal-tampico">Tierra Negra y Sustratos</a>
      <a href="/tezontle-rojo-tampico">Tezontle Rojo</a>
      <a href="/marmol-blanco-tampico">Mármol Blanco</a>
      <a href="/piedra-bola-rio-tampico">Piedra de Río / Bola</a>
    </div>
    <button class="terra-nav__drawer-sub-toggle" aria-expanded="false" data-target="drawer-sub-zonas">
      📍 Por Zona y Mayoreo
      <svg class="terra-nav__chevron" style="margin-left:auto;width:12px;height:12px;" viewBox="0 0 10 6" fill="none">
        <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="terra-nav__drawer-sub" id="drawer-sub-zonas">
      <a href="/vivero-tampico">Vivero en Tampico</a>
      <a href="/jardineria-ciudad-madero">Jardinería Ciudad Madero</a>
      <a href="/jardineria-altamira">Jardinería Altamira</a>
      <a href="/mayoreo-pasto-tampico">Mayoreo Constructoras</a>
    </div>
    <a href="/catalogo">📋 Catálogo</a>
    <a href="/blog">📝 Blog</a>
    <a href="tel:8333268008">📞 833 326 8008</a>
    <a href="https://wa.me/528333268008?text=Hola%2C%20quiero%20una%20cotización%20de%20Viveros%20Terra" class="terra-nav__drawer-cta" target="_blank" rel="noopener noreferrer">
      💬 Cotizar por WhatsApp
    </a>
  </div>
</nav>'''

NEW_SCRIPT = '''
<script>
(function() {
  var nav = document.querySelector('.terra-nav');
  if (!nav) return;
  var currentPage = nav.dataset.page || window.location.pathname;
  nav.querySelectorAll('a[href]').forEach(function(link) {
    var href = link.getAttribute('href');
    if (href && href !== '/' && currentPage.startsWith(href)) link.classList.add('is-active');
    if (href === '/' && currentPage === '/') link.classList.add('is-active');
  });
  var trigger = nav.querySelector('.terra-nav__drop-trigger');
  var dropdown = document.getElementById('dropdown-servicios');
  if (trigger && dropdown) {
    trigger.addEventListener('click', function(e) {
      e.stopPropagation();
      var open = trigger.getAttribute('aria-expanded') === 'true';
      trigger.setAttribute('aria-expanded', String(!open));
      dropdown.classList.toggle('is-open', !open);
    });
    document.addEventListener('click', function(e) {
      if (!nav.contains(e.target)) {
        trigger.setAttribute('aria-expanded', 'false');
        dropdown.classList.remove('is-open');
      }
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        trigger.setAttribute('aria-expanded', 'false');
        dropdown.classList.remove('is-open');
      }
    });
  }
  var hamburger = nav.querySelector('.terra-nav__hamburger');
  var drawer = document.getElementById('terra-nav-drawer');
  if (hamburger && drawer) {
    hamburger.addEventListener('click', function() {
      var open = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!open));
      drawer.classList.toggle('is-open', !open);
    });
  }
  nav.querySelectorAll('.terra-nav__drawer-sub-toggle').forEach(function(subToggle) {
    var targetId = subToggle.getAttribute('data-target');
    var subMenu = document.getElementById(targetId);
    if (!subMenu) return;
    subToggle.addEventListener('click', function() {
      var open = subToggle.getAttribute('aria-expanded') === 'true';
      subToggle.setAttribute('aria-expanded', String(!open));
      subMenu.classList.toggle('is-open', !open);
      var ch = subToggle.querySelector('.terra-nav__chevron');
      if (ch) ch.style.transform = open ? '' : 'rotate(180deg)';
    });
  });
})();
</script>'''

NEW_CSS_RULES = '''
.terra-nav__dropdown {
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  width: 720px;
}
.terra-nav__drop-col {
  display: flex;
  flex-direction: column;
}
.terra-nav__drop-section {
  margin-top: 14px;
}
.terra-nav__drop-section:first-child {
  margin-top: 0;
}
.terra-nav__drop-header {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #1B5E20;
  padding: 6px 12px 6px;
  border-bottom: 1px solid #e8f0e8;
  margin-bottom: 4px;
}
@media (max-width: 900px) {
  .terra-nav__dropdown { width: 100%; grid-template-columns: 1fr; }
}
'''

NAV_PATTERN = re.compile(
    r'(<nav class="terra-nav" data-page="[^"]*">)[\s\S]*?(</nav>)',
    re.DOTALL
)

SCRIPT_PATTERN = re.compile(
    r'<script>\s*\(function\(\) \{\s*var nav = document\.querySelector\(\'\.terra-nav\'\);[\s\S]*?\}\)\(\);\s*</script>',
    re.DOTALL
)

CSS_INJECT_PATTERN = re.compile(
    r'(\.terra-nav__cta:active \{ transform: translateY\(0\); \}\s*\.terra-nav__cta svg \{[^}]*\})',
    re.DOTALL
)


def process_file(path: pathlib.Path) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  WARNING  ERROR lectura: {e}")
        return False

    original = text
    changes = []

    def nav_repl(match):
        opening_tag = match.group(1)
        return opening_tag + NEW_NAV_INNER

    new_text, n = NAV_PATTERN.subn(nav_repl, text, count=1)
    if n > 0:
        changes.append(f'nav HTML ({n})')
        text = new_text

    new_text, n = SCRIPT_PATTERN.subn(NEW_SCRIPT, text, count=1)
    if n > 0:
        changes.append(f'script JS ({n})')
        text = new_text

    if '.terra-nav__drop-section' not in text:
        new_text, n = CSS_INJECT_PATTERN.subn(
            lambda m: m.group(1) + NEW_CSS_RULES,
            text,
            count=1
        )
        if n > 0:
            changes.append(f'CSS rules ({n})')
            text = new_text
        else:
            if '</style>' in text:
                text = text.replace('</style>', NEW_CSS_RULES + '\n</style>', 1)
                changes.append('CSS rules (fallback </style>)')

    if text != original:
        path.write_text(text, encoding='utf-8')
        rel = path.relative_to(BASE)
        print(f"  OK {rel} -- {', '.join(changes)}")
        return True
    else:
        rel = path.relative_to(BASE)
        print(f"  SKIP {rel} -- sin cambios")
        return False


def main():
    if not BASE.exists():
        print(f"ERROR: {BASE} no existe", file=sys.stderr)
        sys.exit(1)

    html_files = list(BASE.rglob('*.html'))
    print(f"Encontrados {len(html_files)} archivos HTML\n")

    modified = 0
    for path in sorted(html_files):
        if process_file(path):
            modified += 1

    print(f"\nTotal modificados: {modified}/{len(html_files)}")


if __name__ == '__main__':
    main()
