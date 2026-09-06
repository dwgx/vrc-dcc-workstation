# -*- coding: utf-8 -*-
"""Run each S00-a case in its own process. Records expected/actual exit, stdout, stderr, time."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "tests" / "_evidence"
CASES = ["T01", "T02", "T03", "T04", "T05", "T06", "T07"]


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    rows = []
    overall = 0
    for case in CASES:
        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tests" / "s00a_cases.py"), case],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        expected = 0
        rec = {
            "case": case,
            "expected_exit": expected,
            "actual_exit": proc.returncode,
            "elapsed_ms": elapsed_ms,
            "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pass": proc.returncode == expected,
        }
        (EVIDENCE / f"{case}.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
        (EVIDENCE / f"{case}.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        (EVIDENCE / f"{case}.meta.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
        rows.append(rec)
        print(f"{case} expected={expected} actual={proc.returncode} ms={elapsed_ms}")
        if proc.returncode != expected:
            overall = 1
            sys.stderr.write(proc.stderr or "")
            sys.stderr.write(proc.stdout or "")
    (EVIDENCE / "summary.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
