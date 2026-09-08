"""Exercise source/local divergence and copied templates in disposable Git repos."""
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compare_upstream.py"
spec = importlib.util.spec_from_file_location("compare_upstream", SCRIPT)
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


@unittest.skipUnless(shutil.which("git"), "requires Git")
class CompareUpstream(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="upstream-comparison-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces"
        self.source.mkdir()
        self.git("init", "--template=", "--initial-branch=main")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.filemode", "false")
        for name in ("same", "upstream", "local", "both", "converge", "removed"):
            self.put(f"methods/{name}.md", b"base\n")
        self.put("methods/crlf.md", b"line\n")
        self.put("methods/binary.bin", b"\x00line\r\n")
        self.put("methods/-服 file.md", b"literal path\n")
        self.git("add", ".")
        self.git("commit", "-m", "Base")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "-c", "candidate")
        for name in ("upstream", "both", "converge"):
            self.put(f"methods/{name}.md", b"upstream\n")
        (self.source / "methods/removed.md").unlink()
        self.put("methods/empty.md", b"")
        self.git("add", "-A")
        self.git("commit", "-m", "Upstream changes")
        self.candidate = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "-c", "local", self.base)
        for name in ("local", "both"):
            self.put(f"methods/{name}.md", b"local\n")
        self.put("methods/converge.md", b"upstream\n")
        self.put("methods/new-local.md", b"local addition\n")
        self.put("methods/crlf.md", b"line\r\n")
        self.put("methods/binary.bin", b"\x00line\n")

    def git(self, *args, input=None):
        env = os.environ.copy()
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
            env.pop(key, None)
        command = ["git", "-c", "core.hooksPath=" + str(self.root / "no-hooks"),
                   "-c", "commit.gpgsign=false", "-c", "user.name=Fixture",
                   "-c", "user.email=fixture@example.invalid", "-C", str(self.source), *args]
        result = subprocess.run(command, input=input, capture_output=True, env=env, check=True)
        return result.stdout.decode("utf-8")

    def put(self, relative, content):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def report(self, ignore_crlf=False, **kwargs):
        args = dict(upstream="candidate", base=self.base, paths=["methods"])
        args.update(kwargs)
        return subject.compare(subject.Repository(self.source, ignore_crlf), **args)

    def test_three_way_working_files_include_additions_and_deletions(self):
        report = self.report()
        rows = {row["source_path"]: row for row in report["files"]}
        expected = {"same": "unchanged", "upstream": "upstream_changed",
                    "local": "local_changed", "both": "both_changed", "converge": "converged",
                    "removed": "upstream_changed", "empty": "upstream_changed",
                    "new-local": "local_changed"}
        for name, status in expected.items():
            self.assertEqual(rows[f"methods/{name}.md"]["status"], status, name)
        self.assertEqual(rows["methods/removed.md"]["upstream_operation"], "deleted")
        self.assertEqual(rows["methods/empty.md"]["upstream_operation"], "added")
        self.assertEqual(rows["methods/empty.md"]["local"]["kind"], "missing")
        self.assertEqual(rows["methods/empty.md"]["upstream"]["size_bytes"], 0)
        self.assertEqual(rows["methods/-服 file.md"]["status"], "unchanged")
        self.assertEqual(report["candidate_commit"], self.candidate)
        self.assertEqual(report["files"][0]["base_commit"], self.base)

    def test_crlf_is_opt_in_and_does_not_change_binary_comparison(self):
        exact = {x["source_path"]: x for x in self.report()["files"]}
        normal = {x["source_path"]: x for x in self.report(True)["files"]}
        self.assertEqual(exact["methods/crlf.md"]["status"], "local_changed")
        self.assertEqual(normal["methods/crlf.md"]["status"], "unchanged")
        self.assertNotEqual(normal["methods/crlf.md"]["local"]["raw_sha256"],
                            normal["methods/crlf.md"]["upstream"]["raw_sha256"])
        self.assertEqual(normal["methods/binary.bin"]["status"], "local_changed")
        self.assertEqual(normal["methods/binary.bin"]["local"]["comparison_mode"], "bytes")

    def test_copied_files_have_independent_and_unknown_baselines(self):
        project = self.root / "world without git"
        project.mkdir()
        (project / "task.md").write_bytes(b"upstream\n")
        (project / "custom.md").write_bytes(b"local\n")
        rows = [
            {"source_path": "methods/upstream.md", "target_path": "task.md", "base_commit": self.candidate},
            {"source_path": "methods/both.md", "target_path": "custom.md", "base_commit": self.base},
            {"source_path": "methods/same.md", "target_path": "unknown.md", "base_commit": None},
        ]
        manifest = self.root / "mapping.json"
        manifest.write_text(json.dumps({"schema_version": 1, "files": rows}), encoding="utf-8")
        report = self.report(base=None, paths=None, local_root=project, manifest=manifest)
        actual = {r["target_path"]: r for r in report["files"]}
        self.assertEqual(actual["task.md"]["status"], "unchanged")
        self.assertEqual(actual["custom.md"]["status"], "both_changed")
        self.assertEqual(actual["unknown.md"]["status"], "baseline_unknown")
        self.assertIsNone(actual["unknown.md"]["base_commit"])
        self.assertFalse((project / ".git").exists())

    def test_bad_mapping_and_revision_do_not_become_untouched_files(self):
        for path in ("../outside", "/absolute", "C:/drive", "a\\b", "a:stream", "a/../b",
                     "CON.txt", "NUL", "a\0b", "a//b", "a."):
            with self.subTest(path=path), self.assertRaises(subject.ComparisonError):
                subject.relative_path(path)
        manifest = self.root / "duplicate.json"
        row = {"source_path": "methods/same.md", "target_path": "a.md", "base_commit": self.base}
        manifest.write_text(json.dumps({"schema_version": 1, "files": [
            row, {**row, "target_path": "A.md"}]}), encoding="utf-8")
        with self.assertRaisesRegex(subject.ComparisonError, "Duplicate"):
            subject.read_mapping(manifest)
        with self.assertRaises(subject.ComparisonError):
            self.report(base="--output=should-not-exist")
        self.assertFalse((self.source / "should-not-exist").exists())
        with self.assertRaisesRegex(subject.ComparisonError, "No files matched"):
            self.report(paths=["misspelled-scope"])

    def test_nonancestor_is_recorded_without_automatic_rejection(self):
        report = self.report(base=self.candidate, upstream=self.base)
        self.assertTrue(report["files"])
        for row in report["files"]:
            self.assertFalse(row["base_is_candidate_ancestor"])
            self.assertIn("baseline_is_not_candidate_ancestor", row["review_reasons"])

    def test_git_symlink_is_manual_review_without_reading_its_target(self):
        oid = self.git("hash-object", "-w", "--stdin", input=b"/outside/private").strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{oid},methods/link")
        self.git("commit", "-m", "Link fixture")
        report = self.report(upstream="HEAD", paths=["methods/link"])
        row = report["files"][0]
        self.assertEqual(row["status"], "manual_review")
        self.assertEqual(row["upstream"]["reason"], "git_special_entry")
        self.assertNotIn("raw_sha256", row["upstream"])

    def test_only_selected_scope_and_no_index_or_content_writes(self):
        before_status = self.git("status", "--porcelain=v1")
        index = (self.source / ".git/index").read_bytes()
        before_files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                        for p in (self.source / "methods").rglob("*") if p.is_file()}
        report = self.report(paths=["methods/same.md"])
        self.assertEqual(len(report["files"]), 1)
        self.assertEqual((self.source / ".git/index").read_bytes(), index)
        self.assertEqual(before_status, self.git("status", "--porcelain=v1"))
        self.assertEqual(before_files, {p.relative_to(self.source).as_posix(): p.read_bytes()
                                      for p in (self.source / "methods").rglob("*") if p.is_file()})

    def test_cli_creates_receipt_once_and_never_overwrites_it(self):
        receipt = self.root / "receipt.json"
        args = [sys.executable, str(SCRIPT), "--repo", str(self.source), "--base", self.base,
                "--upstream", "candidate", "--path", "methods", "--output", str(receipt)]
        first = subprocess.run(args, capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        content = receipt.read_bytes()
        self.assertTrue(json.loads(content)["read_only"])
        second = subprocess.run(args, capture_output=True)
        self.assertEqual(second.returncode, 2)
        self.assertEqual(receipt.read_bytes(), content)

    def test_stream_chunk_boundary_and_invalid_utf8(self):
        raw = b"x" * 65535 + b"\r\nlast\r"
        a = subject.digest_stream(io.BytesIO(raw), True)
        b = subject.digest_stream(io.BytesIO(raw.replace(b"\r\n", b"\n")), False)
        self.assertEqual(a["comparison_sha256"], b["comparison_sha256"])
        invalid = subject.digest_stream(io.BytesIO(b"\xff\r\n"), True)
        self.assertEqual(invalid["comparison_mode"], "bytes")


if __name__ == "__main__":
    unittest.main()
