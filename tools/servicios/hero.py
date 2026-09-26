"""Portada nueva para las páginas de servicios y productos.

Sustituye la sección <section class="vt-hero"> (o una portada svc-hero previa) por la portada svc-hero:
foto real visible, precio en la primera pantalla, tres datos propios del servicio y WhatsApp guiado.
El mismo mensaje guiado se usa en el botón flotante de WhatsApp.

Uso: python3 tools/servicios/hero.py   (desde la raíz del repo)
"""
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

from pages import PAGES

ROOT = Path(__file__).resolve().parents[2] / "public"
WA = "528333268008"
MAX_BYTES = 150 * 1024
CSS_LINK = '<link rel="stylesheet" href="/css/servicios.css?v=20260926">'
HOURS = "Respondemos el mismo día · Lun a vie 9 a 18 h, sáb 9 a 14 h"
WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41z"/></svg>')
HERO_RE = re.compile(r'(?:<!-- svc-hero -->.*?<!-- /svc-hero -->|<section class="vt-hero".*?</section>)', re.S)
BANNER_RE = re.compile(r'<!-- Catálogo CTA Banner -->.*?Abrir catálogo →\s*</a>\s*</div>\s*</div>\n?', re.S)
FLOAT_RE = re.compile(r'(<a[^>]*href=")https://wa\.me/528333268008(?:\?text=[^"]*)?("[^>]*class="[^"]*(?:wa-float|fab)[^"]*"[^>]*>)')
FLOAT_RE_ALT = re.compile(r'(<a[^>]*class="[^"]*(?:wa-float|fab)[^"]*"[^>]*href=")https://wa\.me/528333268008(?:\?text=[^"]*)?(")')


def wa_link(msg):
    return f"https://wa.me/{WA}?text={quote(msg, safe='')}"


def hero_images(src):
    """Crea versiones de 560 y 960 px (<150 KB) de la foto de portada; devuelve (sm, lg, alto_lg)."""
    source = ROOT / src.lstrip("/")
    stem = source.stem
    out_dir = ROOT / "img" / "portadas"
    out_dir.mkdir(exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    sizes = {}
    for width, suffix in ((560, "-sm"), (960, "")):
        w = min(width, im.width)
        h = round(im.height * w / im.width)
        path = out_dir / f"{stem}{suffix}.webp"
        if not path.exists():
            while True:
                resized = im.resize((w, h), Image.LANCZOS)
                for quality in (62, 54, 46):
                    resized.save(path, "WEBP", quality=quality, method=6)
                    if path.stat().st_size <= MAX_BYTES:
                        break
                if path.stat().st_size <= MAX_BYTES:
                    break
                w, h = round(w * 0.85), round(h * 0.85)
        sizes[suffix] = (f"/img/portadas/{path.name}", w, h)
    return sizes["-sm"], sizes[""]


def hero_html(cfg):
    e = escape
    title = f'{e(cfg["title"])} <em>{e(cfg["accent"])}</em>'
    price = f'<span class="svc-hero__price-main">{e(cfg["price_pre"])} <strong>{e(cfg["price"])}</strong>{e(cfg["price_unit"])}</span>'
    if cfg.get("price_alt"):
        price += f'<span class="svc-hero__price-alt">{e(cfg["price_alt"].lstrip("· "))}</span>'
    facts = "\n".join(f"    <div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>" for value, label in cfg["facts"])
    media, klass = "", "svc-hero"
    if cfg.get("img"):
        (sm, sw, _sh), (lg, lw, lh) = hero_images(cfg["img"])
        pos = f' style="object-position:{cfg["img_pos"]}"' if cfg.get("img_pos") else ""
        media = f"""
    <figure class="svc-hero__media">
      <img src="{sm}" srcset="{sm} {sw}w, {lg} {lw}w" sizes="(min-width: 1024px) 540px, 100vw" width="{lw}" height="{lh}" alt="{e(cfg["alt"])}"{pos} fetchpriority="high" decoding="async">
      <figcaption>{e(cfg["caption"])}</figcaption>
    </figure>"""
    else:
        klass += " svc-hero--nomedia"
    secondary = cfg.get("secondary", ("tel:8333268008", "Llamar 833 326 8008"))
    return f"""<!-- svc-hero -->
<section class="{klass}" aria-labelledby="svc-titulo">
  <div class="svc-hero__wrap">
    <div class="svc-hero__copy">
      <p class="svc-hero__eyebrow">{e(cfg.get("eyebrow", "Tampico · Madero · Altamira"))}</p>
      <h1 class="svc-hero__title" id="svc-titulo">{title}</h1>
      <p class="svc-hero__price">{price}</p>
      <p class="svc-hero__lede">{cfg["lede"]}</p>
      <div class="svc-hero__ctas">
        <a class="svc-hero__cta svc-hero__cta--wa" href="{wa_link(cfg["wa"])}" target="_blank" rel="noopener">{WA_ICON}{e(cfg.get("cta", "Cotizar por WhatsApp"))}</a>
        <a class="svc-hero__cta svc-hero__cta--ghost" href="{secondary[0]}">{e(secondary[1])}</a>
      </div>
      <p class="svc-hero__note">{HOURS}</p>
    </div>{media}
  </div>
  <dl class="svc-hero__facts">
{facts}
  </dl>
</section>
<!-- /svc-hero -->"""


def apply(slug, cfg):
    path = ROOT / slug / "index.html"
    html = path.read_text(encoding="utf-8")
    if not HERO_RE.search(html):
        raise SystemExit(f"{slug}: no encontré la portada")
    html = HERO_RE.sub(lambda _m: hero_html(cfg), html, count=1)
    if CSS_LINK.split("?")[0] not in html:
        html = html.replace("</head>", f"{CSS_LINK}\n</head>", 1)
    html = re.sub(r'<link rel="stylesheet" href="/css/servicios\.css\?v=[^"]*">', CSS_LINK, html)
    # el banner del catálogo iba antes de la portada y empujaba el precio fuera de la primera pantalla
    banner = BANNER_RE.search(html)
    if banner:
        html = html.replace(banner.group(0), "", 1).replace("<!-- /svc-hero -->", "<!-- /svc-hero -->\n" + banner.group(0).strip(), 1)
    link = wa_link(cfg["wa"])
    html, n = FLOAT_RE.subn(lambda m: f"{m.group(1)}{link}{m.group(2)}", html)
    if not n:
        html, n = FLOAT_RE_ALT.subn(lambda m: f"{m.group(1)}{link}{m.group(2)}", html)
    nav_re = re.compile(r'(<a href=")https://wa\.me/528333268008(?:\?text=[^"]*)?(" class="terra-nav__(?:drawer-)?cta")')
    html = nav_re.sub(lambda m: f"{m.group(1)}{link}{m.group(2)}", html)
    # quita la precarga de la foto vieja de portada: ahora la precarga la hace fetchpriority
    html = re.sub(r'<link rel="preload" as="image" href="/img/(?!portadas/)[^"]+"[^>]*>\n?', "", html)
    path.write_text(html, encoding="utf-8")
    print(f"ok {slug} (botón flotante: {n})")


def main():
    for slug, cfg in PAGES.items():
        apply(slug, cfg)


if __name__ == "__main__":
    main()
