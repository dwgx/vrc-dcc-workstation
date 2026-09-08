"""Read-only content comparison for source templates and their local adaptations."""
from __future__ import annotations

import argparse
import codecs
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


class ComparisonError(ValueError):
    pass


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ComparisonError(f"Expected a relative slash-separated path: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts) or any(ord(c) < 32 for c in value):
        raise ComparisonError(f"Unsafe relative path: {value!r}")
    if any(part.endswith((".", " ")) for part in parts):
        raise ComparisonError(f"Ambiguous path on Windows: {value!r}")
    if any(re.fullmatch(r"(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?", part, re.I)
           for part in parts):
        raise ComparisonError(f"Device path is not a file: {value!r}")
    return value


def digest_stream(stream, ignore_crlf):
    raw, normalized = hashlib.sha256(), hashlib.sha256()
    decoder = codecs.getincrementaldecoder("utf-8")()
    text_ok, count, carry = True, 0, b""
    while chunk := stream.read(65536):
        raw.update(chunk)
        count += len(chunk)
        if b"\0" in chunk:
            text_ok = False
        if text_ok:
            try:
                decoder.decode(chunk)
            except UnicodeDecodeError:
                text_ok = False
        data = carry + chunk
        carry = b"\r" if data.endswith(b"\r") else b""
        if carry:
            data = data[:-1]
        normalized.update(data.replace(b"\r\n", b"\n"))
    normalized.update(carry)
    if text_ok:
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError:
            text_ok = False
    use_normalized = ignore_crlf and text_ok
    return {
        "kind": "file", "size_bytes": count, "raw_sha256": raw.hexdigest(),
        "comparison_sha256": normalized.hexdigest() if use_normalized else raw.hexdigest(),
        "comparison_mode": "utf8-lf" if use_normalized else "bytes",
    }


def missing():
    return {"kind": "missing"}


def plain_path(path):
    """Reject links/reparse points without following their destination."""
    for component in reversed((path, *path.parents)):
        try:
            info = component.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024)
        ):
            return False
    return True


def local_content(root, name, ignore_crlf):
    path = root.joinpath(*relative_path(name).split("/"))
    try:
        if not plain_path(path):
            return {"kind": "unsupported", "reason": "linked_path"}
        before = path.stat()
        if not stat.S_ISREG(before.st_mode):
            return {"kind": "unsupported", "reason": "not_regular_file"}
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            content = digest_stream(stream, ignore_crlf)
        after = path.stat()
        def identity(info):
            # Windows path stat and descriptor fstat can expose different ctime semantics.
            return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
        if (identity(before) != identity(opened) or identity(before) != identity(after)
                or before.st_ctime_ns != after.st_ctime_ns):
            return {"kind": "unsupported", "reason": "changed_during_read"}
        if not plain_path(path):
            return {"kind": "unsupported", "reason": "linked_path_after_read"}
        return content
    except FileNotFoundError:
        # A file disappearing during a read is not a stable deletion.
        if "before" in locals():
            return {"kind": "unsupported", "reason": "disappeared_during_read"}
        return missing()
    except OSError as exc:
        return {"kind": "unsupported", "reason": type(exc).__name__}


class Repository:
    def __init__(self, path, ignore_crlf=False):
        self.root = Path(path).resolve()
        self.ignore_crlf = ignore_crlf
        self.env = os.environ.copy()
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
            self.env.pop(key, None)
        self.env.update(GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1",
                        GIT_TERMINAL_PROMPT="0")
        self.command = ["git", "-c", "core.fsmonitor=false", "-c", "protocol.allow=never",
                        "-C", str(self.root)]
        actual = Path(self.run("rev-parse", "--show-toplevel").decode().strip()).resolve()
        if actual != self.root:
            raise ComparisonError("--repo must identify the repository root")
        self.trees, self.blobs = {}, {}

    def run(self, *args):
        result = subprocess.run(self.command + list(args), env=self.env,
                                stdin=subprocess.DEVNULL, capture_output=True)
        if result.returncode:
            raise ComparisonError(result.stderr.decode("utf-8", "replace").strip()
                                  or f"Git failed: {args[0]}")
        return result.stdout

    def revision(self, value):
        if not isinstance(value, str) or not value or "\0" in value:
            raise ComparisonError("Expected a Git revision")
        return self.run("rev-parse", "--verify", "--end-of-options",
                        value + "^{commit}").decode("ascii").strip()

    def tree(self, revision):
        if revision not in self.trees:
            entries = {}
            for row in self.run("ls-tree", "-r", "-t", "-z", "--full-tree", revision).split(b"\0"):
                if not row:
                    continue
                metadata, name = row.split(b"\t", 1)
                mode, kind, oid = metadata.decode("ascii").split()
                entries[name.decode("utf-8", "surrogateescape")] = (mode, kind, oid)
            self.trees[revision] = entries
        return self.trees[revision]

    def content(self, revision, name):
        if revision is None:
            return {"kind": "unknown"}
        entry = self.tree(revision).get(name)
        if entry is None:
            return missing()
        mode, kind, oid = entry
        if kind != "blob" or mode not in ("100644", "100755"):
            return {"kind": "unsupported", "reason": "git_special_entry", "git_mode": mode}
        if oid not in self.blobs:
            with subprocess.Popen(self.command + ["cat-file", "blob", oid], env=self.env,
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as process:
                content = digest_stream(process.stdout, self.ignore_crlf)
                error = process.stderr.read()
                if process.wait():
                    raise ComparisonError(error.decode("utf-8", "replace").strip()
                                          or "Cannot read Git blob")
            self.blobs[oid] = content
        return {**self.blobs[oid], "git_mode": mode}

    def ancestor(self, base, candidate):
        result = subprocess.run(self.command + ["merge-base", "--is-ancestor", base, candidate],
                                env=self.env, stdin=subprocess.DEVNULL, capture_output=True)
        if result.returncode not in (0, 1):
            raise ComparisonError(result.stderr.decode("utf-8", "replace").strip())
        return result.returncode == 0

    def working_paths(self):
        return {p.decode("utf-8", "surrogateescape") for p in self.run(
            "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0") if p}


def key(content):
    return content["kind"], content.get("comparison_sha256")


def classify(base, local, upstream):
    if any(x["kind"] == "unsupported" for x in (base, local, upstream)):
        return "manual_review"
    if base["kind"] == "unknown":
        return "baseline_unknown"
    b, loc, up = key(base), key(local), key(upstream)
    if loc == up:
        return "unchanged" if b == loc else "converged"
    if loc == b:
        return "upstream_changed"
    if up == b:
        return "local_changed"
    return "both_changed"


def operation(base, current):
    if base["kind"] not in ("file", "missing") or current["kind"] not in ("file", "missing"):
        return "unknown"
    if key(base) == key(current):
        return "unchanged"
    if base["kind"] == "missing":
        return "added"
    if current["kind"] == "missing":
        return "deleted"
    return "modified"


def read_mapping(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ComparisonError("Mapping requires schema_version: 1")
    files = data.get("files")
    if not isinstance(files, list) or not files:
        raise ComparisonError("Mapping requires a nonempty files array")
    seen, rows = set(), []
    for row in files:
        if not isinstance(row, dict) or set(row) != {"source_path", "target_path", "base_commit"}:
            raise ComparisonError("Each mapping needs source_path, target_path and base_commit")
        source, target = relative_path(row["source_path"]), relative_path(row["target_path"])
        # Avoid two records claiming the same Windows target on another OS.
        normalized = target.casefold()
        if normalized in seen:
            raise ComparisonError(f"Duplicate mapped target: {target}")
        seen.add(normalized)
        base = row["base_commit"]
        if base is not None and (not isinstance(base, str) or not re.fullmatch(
                r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", base)):
            raise ComparisonError("Mapped base_commit must be a full commit hash or null")
        rows.append((source, target, base))
    return rows


def compare(repo, upstream, base=None, paths=None, local_root=None, manifest=None):
    candidate = repo.revision(upstream)
    if manifest:
        if base is not None or paths or local_root is None:
            raise ComparisonError("--manifest needs --local-root and excludes --base/--path")
        rows = read_mapping(manifest)
        root = Path(os.path.abspath(local_root))
        layout = "mapped_files"
    else:
        if base is None or not paths or local_root is not None:
            raise ComparisonError("Clone comparison needs --base and --path; use a mapping for --local-root")
        base = repo.revision(base)
        scopes = [relative_path(p) for p in paths]
        names = set(repo.working_paths())
        for revision in (base, candidate):
            names.update(name for name, entry in repo.tree(revision).items() if entry[1] != "tree")
        rows = [(name, name, base) for name in sorted(names)
                if any(name == scope or name.startswith(scope + "/") for scope in scopes)]
        if not rows:
            raise ComparisonError("No files matched --path in the baseline, candidate or local inventory")
        root, layout = repo.root, "clone_working_files"
    if not root.is_dir() or not plain_path(root):
        raise ComparisonError("--local-root must be an existing directory without linked parents")
    revisions, ancestors, results = {}, {}, []
    for source, target, requested_base in rows:
        relative_path(source)
        if requested_base not in revisions:
            revisions[requested_base] = repo.revision(requested_base) if requested_base else None
        resolved = revisions[requested_base]
        if resolved is not None and resolved not in ancestors:
            ancestors[resolved] = repo.ancestor(resolved, candidate)
        original = repo.content(resolved, source)
        proposed = repo.content(candidate, source)
        local = local_content(root, target, repo.ignore_crlf)
        reasons = []
        if resolved and not ancestors[resolved]:
            reasons.append("baseline_is_not_candidate_ancestor")
        if original.get("git_mode") != proposed.get("git_mode") and (
            original["kind"] == proposed["kind"] == "file"
        ):
            reasons.append("upstream_git_mode_changed")
        for label, content in (("base", original), ("local", local), ("upstream", proposed)):
            if content["kind"] == "unsupported":
                reasons.append(label + ":" + content["reason"])
        results.append({
            "source_path": source, "target_path": target, "base_commit": resolved,
            "base_is_candidate_ancestor": ancestors.get(resolved),
            "status": classify(original, local, proposed), "review_reasons": reasons,
            "local_operation": operation(original, local),
            "upstream_operation": operation(original, proposed),
            "base": original, "local": local, "upstream": proposed,
        })
    return {
        "schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(),
        "layout": layout, "source_root": str(repo.root), "local_root": str(root),
        "candidate_ref": upstream, "candidate_commit": candidate,
        "ignore_crlf": repo.ignore_crlf, "read_only": True,
        "limits": ["Content comparison only; no automatic merge or adoption.",
                   "Working-file permissions, rename semantics, expanded LFS and runtime behavior need review."],
        "summary": dict(sorted(Counter(row["status"] for row in results).items())),
        "files": results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--upstream", required=True)
    parser.add_argument("--base")
    parser.add_argument("--path", action="append")
    parser.add_argument("--local-root")
    parser.add_argument("--manifest")
    parser.add_argument("--ignore-crlf", action="store_true")
    parser.add_argument("--output", help="Create a new receipt; never replace an existing file")
    args = parser.parse_args(argv)
    try:
        repo = Repository(args.repo, args.ignore_crlf)
        report = compare(repo, args.upstream, args.base, args.path, args.local_root, args.manifest)
        output = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
        if args.output:
            with Path(args.output).open("x", encoding="utf-8") as stream:
                stream.write(output)
        else:
            sys.stdout.write(output)
        return 0
    except (ComparisonError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"compare_upstream: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
