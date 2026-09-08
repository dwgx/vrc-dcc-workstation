"""Run bootstrap only against disposable Windows fixtures, never a live station."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell")


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*") if p.is_file()
    }


@unittest.skipUnless(os.name == "nt" and POWERSHELL, "requires Windows PowerShell")
class BootstrapPreservation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="station-bootstrap-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces"
        (self.source / "scripts").mkdir(parents=True)
        for name in ("bootstrap.ps1", "resolve-locale.ps1"):
            shutil.copyfile(ROOT / "scripts" / name, self.source / "scripts" / name)
        for name in ("local.json.example", "locales.json"):
            shutil.copyfile(ROOT / name, self.source / name)
        (self.source / "mcp").mkdir()
        (self.source / "mcp/cursor.mcp.json.template").write_text(
            '{"mcpServers":{"fixture":{"command":"{{UVX}}","args":[]}}}',
            encoding="utf-8",
        )
        (self.source / "AGENTS.md").write_text("Fixture contract\n", encoding="utf-8")
        (self.source / "templates").mkdir()
        (self.source / "templates/TASK.md").write_text("Template v1\n", encoding="utf-8")

    def run_bootstrap(self, source=None, target=None, apply=True, language=None):
        command = [POWERSHELL, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                   "-File", str((source or self.source) / "scripts/bootstrap.ps1")]
        if target is not None:
            command += ["-InstallRoot", str(target)]
        if apply:
            command.append("-Apply")
        if language:
            command += ["-UiLanguage", language]
        env = os.environ.copy()
        for key in ("WORKSTATION_UI_LANG", "VRC_DCC_UI_LANG", "DEBUGGER_UI_LANG"):
            env.pop(key, None)
        return subprocess.run(command, cwd=self.root, env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=45)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_repeat_keeps_custom_files_and_fills_missing_mcp(self):
        custom = {
            ".mcp.json": '{"mcpServers":{"my-route":{"url":"http://localhost:9911"}}}\n',
            ".cursor/mcp.json": '{"mcpServers":{"different-route":{"command":"my-tool"}}}\n',
            "local.json": json.dumps({"ui_language": "ja", "install_root": "owner-value",
                                      "unity_project": "owner-project", "custom": [1, 2]}),
        }
        for name, content in custom.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        before = snapshot(self.source)
        self.assert_success(self.run_bootstrap())
        after = snapshot(self.source)
        for name in custom:
            self.assertEqual(after[name], before[name], name)
        self.assertIn("mcp/local.mcp.json", after)
        self.assert_success(self.run_bootstrap())
        self.assertEqual(after, snapshot(self.source))

    def test_fresh_install_then_use_its_own_bootstrap(self):
        target = self.root / "new station"
        before = snapshot(self.source)
        self.assert_success(self.run_bootstrap(target=target))
        self.assertEqual((target / "templates/TASK.md").read_bytes(),
                         (self.source / "templates/TASK.md").read_bytes())
        cfg = json.loads((target / "local.json").read_text(encoding="utf-8"))
        self.assertEqual(Path(cfg["install_root"]), target)
        installed = snapshot(target)
        self.assert_success(self.run_bootstrap(source=target))
        self.assertEqual(installed, snapshot(target))
        self.assertEqual(before, snapshot(self.source))

    def test_nonempty_target_rejected_before_writes(self):
        target = self.root / "customized"
        target.mkdir()
        (target / "AGENTS.md").write_text("Owner's independent contract", encoding="utf-8")
        (target / ".mcp.json").write_text("Owner's configuration", encoding="utf-8")
        before = snapshot(target)
        result = self.run_bootstrap(target=target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compare_upstream.py", result.stdout + result.stderr)
        self.assertEqual(before, snapshot(target))

    def test_explicit_locale_fills_only_empty_preference(self):
        self.assert_success(self.run_bootstrap())
        path = self.source / "local.json"
        original = {"ui_language": "", "install_root": "owner-root",
                    "unity_project": "owner-project", "custom": {"nested": [1, 2]}}
        path.write_text(json.dumps(original), encoding="utf-8")
        self.assert_success(self.run_bootstrap(language="ja-JP"))
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")),
                         {**original, "ui_language": "ja"})
        before = snapshot(self.source)
        self.assert_success(self.run_bootstrap(language="ko-KR"))
        self.assertEqual(before, snapshot(self.source))

    def test_all_custom_mcp_and_invalid_local_remain_intact(self):
        self.assert_success(self.run_bootstrap())
        for name in (".mcp.json", ".cursor/mcp.json", "mcp/local.mcp.json"):
            (self.source / name).write_text(json.dumps({"custom": name}), encoding="utf-8")
        (self.source / "local.json").write_text("owner incomplete json {", encoding="utf-8")
        before = snapshot(self.source)
        self.assert_success(self.run_bootstrap())
        self.assertEqual(before, snapshot(self.source))
        result = self.run_bootstrap(language="ja-JP")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, snapshot(self.source))

    def test_overlap_rejected_and_dry_run_does_not_create_target(self):
        before = snapshot(self.source)
        target = self.source / "templates/new station"
        result = self.run_bootstrap(target=target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not overlap", result.stdout + result.stderr)
        self.assertEqual(before, snapshot(self.source))
        self.assertFalse(target.exists())
        target = self.root / "dry run"
        self.assert_success(self.run_bootstrap(target=target, apply=False))
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
