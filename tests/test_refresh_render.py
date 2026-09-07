"""Compatibility for an existing clone-owned map renderer. No live maps."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "maps"))
import refresh


class RenderCompatibility(unittest.TestCase):
    def test_existing_renderer_is_used(self):
        with tempfile.TemporaryDirectory(prefix="vrc-render-") as tmp:
            root = Path(tmp)
            target = root / "example-render"
            target.mkdir()
            (target / "render.py").write_text(
                "from pathlib import Path\n"
                "Path(__file__).with_name('MAP.md').write_text('custom map', encoding='utf-8')\n",
                encoding="utf-8",
            )
            with patch.object(refresh, "HERE", root):
                refresh.render("example-render")
            self.assertEqual((target / "MAP.md").read_text(encoding="utf-8"), "custom map")

    def test_broken_custom_renderer_reports_failure(self):
        with tempfile.TemporaryDirectory(prefix="vrc-render-") as tmp:
            root = Path(tmp)
            target = root / "example-render"
            target.mkdir()
            (target / "render.py").write_text("raise RuntimeError('renderer failed')\n", encoding="utf-8")
            with patch.object(refresh, "HERE", root), self.assertRaisesRegex(RuntimeError, "renderer failed"):
                refresh.render("example-render")
            self.assertFalse((target / "MAP.md").exists())


if __name__ == "__main__":
    unittest.main()
