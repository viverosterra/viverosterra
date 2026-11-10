import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / "ci" / "sitio.yml"  # pendiente: volver a .github/workflows/ cuando el token tenga permiso de workflows


class CiTest(unittest.TestCase):
    def test_workflow_con_build_reproducible_y_todas_las_pruebas(self):
        yml = WORKFLOW.read_text(encoding="utf-8")
        for paso in ("python tools/site/build.py", "git diff --exit-code -- public",
                     'test -z "$(git status --porcelain -- public)"', "playwright install --with-deps chromium",
                     "python -m unittest discover -s tests -v", "python -m unittest discover -s tests -t .",
                     "node --test public/js/tests/*.test.js"):
            with self.subTest(paso=paso):
                self.assertIn(paso, yml)
        self.assertNotIn("npm ", yml)
        self.assertIn("uses: actions/cache@v4", yml)
        for ruta in ("~/.cache/pip", "~/.cache/ms-playwright"):
            self.assertIn(ruta, yml)
        self.assertLess(yml.index("actions/cache@v4"), yml.index("playwright install --with-deps chromium"))
        self.assertNotIn("package.json", yml)


if __name__ == "__main__":
    unittest.main()
