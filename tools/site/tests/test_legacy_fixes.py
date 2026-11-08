import re
import unittest
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3] / "public"
HOJAS = ("tailwind.css", "design-system.css", "legacy-fixes.css")
UTILIDAD = re.compile(
    r"^(?:(?:sm|md|lg|xl|hover|focus|group-hover):)*-?(?:p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|w|h|min-h|max-w|text|bg|"
    r"border|rounded|gap|space|grid|col|row|flex|items|justify|font|leading|tracking|opacity|shadow|z|top|left|right|"
    r"bottom|inset|object|overflow|order|self|place|aspect|ring|translate|scale|duration|transition|from|to|via|divide|"
    r"line|whitespace|truncate|underline|uppercase|italic|block|inline|hidden|absolute|relative|fixed|sticky|shrink|"
    r"grow|basis)(?:-|$)"
)


def clases(css):
    return {m.replace("\\", "") for m in re.findall(r"\.((?:\\.|[\w-])+)", css)}


class LegacyFixesTest(unittest.TestCase):
    def test_ninguna_utilidad_usada_queda_sin_definir(self):
        definidas = set()
        for hoja in HOJAS:
            definidas |= clases((PUBLIC / "css" / hoja).read_text(encoding="utf-8"))
        faltan = {}
        for pagina in PUBLIC.rglob("*.html"):
            html = pagina.read_text(encoding="utf-8")
            if "/css/tailwind.css" not in html:
                continue
            locales = set()
            for estilo in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S):
                locales |= clases(estilo)
            for atributo in re.findall(r'class="([^"]*)"', html):
                for clase in atributo.split():
                    if "{" in clase or clase in definidas or clase in locales or not UTILIDAD.match(clase):
                        continue
                    faltan.setdefault(clase, str(pagina.relative_to(PUBLIC)))
        self.assertEqual(faltan, {})


if __name__ == "__main__":
    unittest.main()
