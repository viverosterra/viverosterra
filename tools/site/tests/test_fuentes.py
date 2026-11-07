import hashlib
import unittest
from pathlib import Path

FUENTES = Path(__file__).resolve().parents[3] / "public" / "fonts"
ESPERADAS = {
    "archivo-latin.woff2": "4c98b9d490d1698ec95f2ff17a6c7d0e72691864c0c5d7bc2a2c161b45afe5ad",
    "fraunces-italic-latin.woff2": "a7125f30fe100bbcf48b07996b6cae585afbdaea57fea1c014505793fa8d43a6",
}


class FuentesTest(unittest.TestCase):
    def test_fuentes_presentes_e_integras(self):
        for nombre, sha in ESPERADAS.items():
            with self.subTest(fuente=nombre):
                datos = (FUENTES / nombre).read_bytes()
                self.assertEqual(datos[:4], b"wOF2")
                self.assertEqual(hashlib.sha256(datos).hexdigest(), sha)

    def test_presupuesto_total(self):
        total = sum((FUENTES / n).stat().st_size for n in ESPERADAS)
        self.assertLess(total, 120 * 1024)


if __name__ == "__main__":
    unittest.main()
