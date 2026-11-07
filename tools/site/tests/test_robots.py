import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import paginas  # noqa: E402

ROBOTS = paginas.PUBLIC / "robots.txt"
BOTS = ("OAI-SearchBot", "ChatGPT-User", "GPTBot", "Claude-SearchBot", "Claude-User", "ClaudeBot", "PerplexityBot",
        "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot")


def grupos(texto):
    """Bloques separados por líneas en blanco, sin comentarios."""
    bloques = [[ln for ln in b.splitlines() if ln and not ln.startswith("#")] for b in texto.split("\n\n")]
    return [b for b in bloques if b]


class RobotsTest(unittest.TestCase):
    def setUp(self):
        self.texto = ROBOTS.read_text(encoding="utf-8")

    def test_sin_bloqueos_ni_reglas_para_adsbot(self):
        self.assertNotIn("Disallow:", self.texto)
        self.assertNotIn("User-agent: AdsBot", self.texto)

    def test_bots_de_busqueda_e_ia_con_permiso_explicito(self):
        for bot in BOTS:
            grupo = next((g for g in grupos(self.texto) if f"User-agent: {bot}" in g), None)
            with self.subTest(bot=bot):
                self.assertIsNotNone(grupo)
                self.assertIn("Allow: /", grupo)

    def test_sitemap_declarado(self):
        self.assertIn("Sitemap: https://www.viverosterra.com/sitemap.xml", self.texto)


if __name__ == "__main__":
    unittest.main()
