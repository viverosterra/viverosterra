import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datos  # noqa: E402

JS = Path(__file__).resolve().parents[3] / "public" / "js" / "terra.js"


class ParidadTerraJsTest(unittest.TestCase):
    def test_firma_igual_en_js_y_python(self):
        firma = re.search(r"const FIRMA = '([^']+)';", JS.read_text(encoding="utf-8")).group(1)
        self.assertEqual(firma, datos.FIRMA)


if __name__ == "__main__":
    unittest.main()
