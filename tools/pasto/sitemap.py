"""Agrega o actualiza URLs en public/sitemap.xml sin tocar las demás."""
import re
from datetime import date
from pathlib import Path

SITEMAP = Path(__file__).resolve().parents[2] / "public" / "sitemap.xml"


def upsert(urls, lastmod=None, changefreq="monthly", priority="0.8"):
    """Actualiza lastmod de las URLs que ya existen y agrega las que faltan."""
    lastmod = lastmod or date.today().isoformat()
    xml = SITEMAP.read_text(encoding="utf-8")
    for url in urls:
        entry = re.compile(
            r"(<url>\s*<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)", re.S
        )
        if entry.search(xml):
            xml = entry.sub(lambda m: m.group(1) + lastmod + m.group(2), xml, count=1)
            continue
        line = (
            f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n"
        )
        xml = xml.replace("</urlset>", line + "</urlset>")
    SITEMAP.write_text(xml, encoding="utf-8")
