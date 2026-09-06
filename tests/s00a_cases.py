# -*- coding: utf-8 -*-
"""S00-a independent regressions. Invoke: python tests/s00a_cases.py T01"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
PY = sys.executable


def run_cmd(args: list[str], *, cwd: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def fingerprint(path: Path) -> str:
    if not path.exists():
        return "ABSENT"
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    st = path.stat()
    return f"{h}:{st.st_mtime_ns}:{st.st_size}"


def assert_exit(proc: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    print("CMD", label)
    print("expected_exit", expected)
    print("actual_exit", proc.returncode)
    print("stdout_len", len(proc.stdout or ""))
    print("stderr_len", len(proc.stderr or ""))
    if proc.stdout:
        print("--- stdout ---")
        print(proc.stdout)
    if proc.stderr:
        print("--- stderr ---")
        print(proc.stderr)
    if proc.returncode != expected:
        raise SystemExit(f"FAIL {label}: expected {expected} got {proc.returncode}")


def t01_cli_requires_avatar() -> None:
    """query/refresh/render with no avatar: argparse error; template files unchanged."""
    watch = [
        MAPS / "templates" / "graph.json",
        MAPS / "templates" / "dump-map.json",
        ROOT / "docs" / "AVATAR_PROFILE.md",
    ]
    before = {p: fingerprint(p) for p in watch}
    cmds = [
        ([PY, str(MAPS / "query.py")], 2, "query.py"),
        ([PY, str(MAPS / "refresh.py")], 2, "refresh.py"),
        ([PY, str(MAPS / "render_map.py")], 2, "render_map.py"),
    ]
    for args, exp, name in cmds:
        proc = run_cmd(args, cwd=MAPS)
        assert_exit(proc, exp, name)
        err = (proc.stderr or "") + (proc.stdout or "")
        if "required" not in err.lower() and "the following arguments are required" not in err:
            raise SystemExit(f"FAIL {name}: expected argparse required-avatar text")
    after = {p: fingerprint(p) for p in watch}
    if before != after:
        raise SystemExit(f"FAIL T01: watched files changed {before} vs {after}")
    print("PASS T01")


def _seed_avatar(aid: str) -> Path:
    dest = MAPS / aid
    if dest.exists():
        shutil.rmtree(dest)
    proc = run_cmd([PY, "init_avatar.py", aid], cwd=MAPS)
    assert_exit(proc, 0, f"init_avatar.py {aid}")
    return dest


def t02_two_synthetic_profiles() -> None:
    a = _seed_avatar("example-alpha")
    b = _seed_avatar("example-beta")
    try:
        ga = json.loads((a / "graph.json").read_text(encoding="utf-8"))
        gb = json.loads((b / "graph.json").read_text(encoding="utf-8"))
        if ga.get("avatar") == gb.get("avatar"):
            raise SystemExit("FAIL T02: avatars not isolated")
        qa = run_cmd([PY, "query.py", "example-alpha"], cwd=MAPS)
        qb = run_cmd([PY, "query.py", "example-beta"], cwd=MAPS)
        assert_exit(qa, 1, "query example-alpha empty")  # 0 hits
        assert_exit(qb, 1, "query example-beta empty")
        if "example-alpha" in (qa.stdout or "") and "example-beta" in (qa.stdout or ""):
            raise SystemExit("FAIL T02: query mixed both avatars")
        ra = run_cmd([PY, "render_map.py", "example-alpha"], cwd=MAPS)
        rb = run_cmd([PY, "render_map.py", "example-beta"], cwd=MAPS)
        assert_exit(ra, 0, "render example-alpha")
        assert_exit(rb, 0, "render example-beta")
        if not (a / "MAP.md").is_file() or not (b / "MAP.md").is_file():
            raise SystemExit("FAIL T02: MAP.md missing")
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)
    print("PASS T02")


def t03_cwd_and_no_auto_init() -> None:
    missing = MAPS / "example-missing"
    if missing.exists():
        shutil.rmtree(missing)
    proc = run_cmd([PY, str(MAPS / "query.py"), "example-missing"], cwd=ROOT)
    assert_exit(proc, 2, "query missing from repo root cwd")
    if missing.exists():
        raise SystemExit("FAIL T03: query auto-created maps/example-missing")
    proc2 = run_cmd([PY, str(MAPS / "query.py"), "example-missing"], cwd=MAPS)
    assert_exit(proc2, 2, "query missing from maps cwd")
    if missing.exists():
        raise SystemExit("FAIL T03: second cwd created the folder")
    a = _seed_avatar("example-alpha")
    try:
        from_root = run_cmd([PY, str(MAPS / "query.py"), "example-alpha"], cwd=ROOT)
        from_maps = run_cmd([PY, str(MAPS / "query.py"), "example-alpha"], cwd=MAPS)
        assert_exit(from_root, 1, "query alpha from root")
        assert_exit(from_maps, 1, "query alpha from maps")
        if "example-alpha" not in (from_root.stderr or "") and "MAP.md" not in (from_root.stdout or ""):
            # empty hits still print map path
            if "hits:" not in (from_root.stdout or "") and "0 hits" not in (from_root.stdout or ""):
                raise SystemExit("FAIL T03: unexpected query output from root")
        if from_root.returncode != from_maps.returncode:
            raise SystemExit("FAIL T03: cwd changed query exit")
    finally:
        shutil.rmtree(a, ignore_errors=True)
        if missing.exists():
            shutil.rmtree(missing)
    print("PASS T03")


def t04_dump_no_false_merge() -> None:
    dest = _seed_avatar("example-alpha")
    try:
        graph = json.loads((dest / "graph.json").read_text(encoding="utf-8"))
        graph["nodes"] = [
            {"id": "plugin.sps", "kind": "plugin", "label": "SPS", "hierarchy": "old"},
            {"id": "outfit.bra_default", "kind": "outfit", "label": "should not be written by Bra name"},
        ]
        (dest / "graph.json").write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
        notes_before = (dest / "notes.json").read_text(encoding="utf-8")
        dump = dest / "dump.txt"
        dump.write_text(
            "SPS\tRoot/SPS\nBra\tRoot/Bra\nPants\tRoot/Pants\n衣服\tRoot/Clothes\n菜单\tRoot/Menu\n",
            encoding="utf-8",
        )
        proc = run_cmd(
            [PY, "refresh.py", "example-alpha", "--from-dump", str(dump), "--mark-missing"],
            cwd=MAPS,
        )
        assert_exit(proc, 0, "refresh dump")
        out = (proc.stdout or "") + (proc.stderr or "")
        if "unresolved dump names" not in out:
            raise SystemExit("FAIL T04: expected unresolved dump names")
        for name in ("Bra", "Pants", "衣服", "菜单"):
            if name not in out:
                raise SystemExit(f"FAIL T04: expected unresolved {name}")
        g2 = json.loads((dest / "graph.json").read_text(encoding="utf-8"))
        by_id = {n["id"]: n for n in g2["nodes"]}
        if by_id["plugin.sps"].get("hierarchy") != "Root/SPS":
            raise SystemExit("FAIL T04: mapped SPS should update")
        if by_id["outfit.bra_default"].get("hierarchy"):
            raise SystemExit("FAIL T04: Bra name merged into outfit.bra_default")
        notes = json.loads((dest / "notes.json").read_text(encoding="utf-8"))
        if "outfit.bra_default" in notes and "gone from dump" in (notes["outfit.bra_default"].get("note") or ""):
            raise SystemExit("FAIL T04: unmapped Bra path triggered mark-missing on bra_default")
        if notes_before.strip() == "{}" and any(
            "outfit.added" in notes or "menu.gimmicks" in notes for _ in [0]
        ):
            if "outfit.added" in notes or "menu.gimmicks" in notes:
                raise SystemExit("FAIL T04: fabricated outfit.added / menu.gimmicks notes")
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS T04")


def t05_library_legacy_key_not_generic() -> None:
    lib = MAPS / "library"
    cat = lib / "catalog.json"
    notes = lib / "notes.json"
    bak_cat = cat.read_bytes() if cat.exists() else None
    bak_notes = notes.read_bytes() if notes.exists() else None
    try:
        cat.write_text(
            json.dumps(
                {
                    "root": "synthetic",
                    "updated": "2026-09-07",
                    "count": 2,
                    "nodes": [
                        {"id": "asset.with-key", "kind": "clothes", "label": "Keyed", "bodies": ["x"], "wear_fusion": True},
                        {"id": "asset.no-key", "kind": "clothes", "label": "Unknown", "bodies": ["x"], "wear_fusion": True},
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        notes.write_text(
            json.dumps({"asset.with-key": {"kaguya": "installed", "status": "observed"}}, indent=2) + "\n",
            encoding="utf-8",
        )
        refuse = run_cmd([PY, "query.py", "library", "--on-body", "installed"], cwd=MAPS)
        assert_exit(refuse, 2, "library --on-body refused")
        listed = run_cmd([PY, "query.py", "library", "--json"], cwd=MAPS)
        assert_exit(listed, 0, "library --json")
        rows = json.loads(listed.stdout)
        by = {r["id"]: r for r in rows}
        if by["asset.with-key"].get("legacy_kaguya_key") != "installed":
            raise SystemExit("FAIL T05: installed key not shown as legacy")
        if by["asset.no-key"].get("legacy_kaguya_key") != "unset":
            raise SystemExit(f"FAIL T05: missing key must be unset not never: {by['asset.no-key']}")
        never_f = run_cmd([PY, "query.py", "library", "--kaguya", "never", "--json"], cwd=MAPS)
        # missing key must not match never
        if never_f.returncode == 0:
            rows_n = json.loads(never_f.stdout or "[]")
            if any(r["id"] == "asset.no-key" for r in rows_n):
                raise SystemExit("FAIL T05: unset displayed/filtered as never")
        inst = run_cmd([PY, "query.py", "library", "--kaguya", "installed", "--json"], cwd=MAPS)
        assert_exit(inst, 0, "library --kaguya installed")
        ids = [r["id"] for r in json.loads(inst.stdout)]
        if ids != ["asset.with-key"]:
            raise SystemExit(f"FAIL T05: unexpected installed filter {ids}")
    finally:
        if bak_cat is None:
            if cat.exists():
                cat.unlink()
        else:
            cat.write_bytes(bak_cat)
        if bak_notes is None:
            if notes.exists():
                notes.unlink()
        else:
            notes.write_bytes(bak_notes)
    print("PASS T05")


def t06_library_namespace() -> None:
    help_p = run_cmd([PY, "query.py", "library", "--help"], cwd=MAPS)
    assert_exit(help_p, 0, "query.py library --help")
    if "USB shelf" not in (help_p.stdout or "") and "catalog" not in (help_p.stdout or "").lower():
        # argparse description
        if "Query the USB shelf catalog" not in (help_p.stdout or ""):
            raise SystemExit("FAIL T06: library --help is not the shelf parser")
    fake_avatar = MAPS / "library" / "graph.json"
    if fake_avatar.exists():
        raise SystemExit("FAIL T06: library treated as avatar graph")
    proc = run_cmd([PY, "query.py", "library", "no-such-pack-token"], cwd=MAPS)
    # 1 = 0 hits or 2 = no catalog. Both OK; must not be 0 with a created avatar.
    print("library query exit", proc.returncode)
    if proc.returncode not in (1, 2):
        if proc.returncode == 0 and "hits:" in (proc.stdout or ""):
            pass  # catalog may exist on this machine
        else:
            raise SystemExit(f"FAIL T06: unexpected exit {proc.returncode}")
    if (MAPS / "library" / "graph.json").exists():
        raise SystemExit("FAIL T06: created graph.json under library")
    print("PASS T06")


def t07_public_eval_and_links() -> None:
    ev = run_cmd([PY, str(ROOT / "scripts" / "eval-agent-contract.py")], cwd=ROOT)
    assert_exit(ev, 0, "eval-agent-contract.py")
    link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    tracked = subprocess.check_output(["git", "ls-files", "*.md"], cwd=str(ROOT), text=True).splitlines()
    bad = []
    for md in tracked:
        p = ROOT / md
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        base = str(p.parent)
        for m in link.finditer(text):
            t = m.group(1).split("#")[0].strip()
            if not t or t.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            tgt = Path(os.path.normpath(os.path.join(base, t)))
            if not tgt.exists():
                bad.append(f"{md} -> {t}")
    if bad:
        print("broken links:")
        print("\n".join(bad))
        raise SystemExit("FAIL T07: broken relative links")
    print("PASS T07")


CASES = {
    "T01": t01_cli_requires_avatar,
    "T02": t02_two_synthetic_profiles,
    "T03": t03_cwd_and_no_auto_init,
    "T04": t04_dump_no_false_merge,
    "T05": t05_library_legacy_key_not_generic,
    "T06": t06_library_namespace,
    "T07": t07_public_eval_and_links,
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CASES:
        print("usage: python tests/s00a_cases.py T01|...|T07", file=sys.stderr)
        return 2
    CASES[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
