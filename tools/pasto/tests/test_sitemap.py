import tempfile
import unittest
from pathlib import Path

import sitemap

BASE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset>\n'
    "  <url><loc>https://x.com/a</loc><lastmod>2020-01-01</lastmod>"
    "<changefreq>weekly</changefreq><priority>0.9</priority></url>\n</urlset>\n"
)


class SitemapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()) / "sitemap.xml"
        self.tmp.write_text(BASE, encoding="utf-8")
        self.orig = sitemap.SITEMAP
        sitemap.SITEMAP = self.tmp

    def tearDown(self):
        sitemap.SITEMAP = self.orig

    def test_idempotente_sin_duplicados_y_actualiza_lastmod(self):
        urls = ["https://x.com/a", "https://x.com/b"]
        sitemap.upsert(urls, lastmod="2026-10-01")
        sitemap.upsert(urls, lastmod="2026-10-02")
        xml = self.tmp.read_text(encoding="utf-8")
        for u in urls:
            self.assertEqual(xml.count(f"<loc>{u}</loc>"), 1)
        self.assertEqual(xml.count("2026-10-02"), 2)
        self.assertNotIn("2020-01-01", xml)
        self.assertIn("<changefreq>weekly</changefreq><priority>0.9</priority>", xml)
        self.assertTrue(xml.rstrip().endswith("</urlset>"))
