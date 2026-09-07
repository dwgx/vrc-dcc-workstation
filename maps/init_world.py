# -*- coding: utf-8 -*-
"""Create maps/worlds/<id>/ overlay. Does not write Unity. Not a live world_* dump."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from _stdio import utf8_stdio
from product import WORLD, product_dir

HERE = Path(__file__).resolve().parent
TEMPL = HERE / "templates"
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")

PROPOSED = ["world_probe", "world_scene_dump", "world_udon_inventory"]


def main() -> None:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Seed maps/worlds/<id>/ (overlay, gitignored)")
    ap.add_argument("world", help="lowercase id, e.g. my-world")
    args = ap.parse_args()
    wid = args.world.strip().lower()
    if not ID_RE.match(wid):
        raise SystemExit("world id must match [a-z][a-z0-9-]*")
    dest = product_dir(wid, WORLD)
    if dest.exists():
        raise SystemExit("already exists: %s" % dest)
    dest.mkdir(parents=True)
    today = date.today().isoformat()

    policy = json.loads((TEMPL / "WORLD_POLICY.json").read_text(encoding="utf-8"))
    policy["world"] = wid
    (dest / "POLICY.json").write_text(
        json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    job = json.loads((TEMPL / "JOB.json").read_text(encoding="utf-8"))
    job.pop("avatar", None)
    job["domain"] = WORLD
    job["world"] = wid
    job["note"] = (
        "World JOB. python maps/world_gate.py %s begin <id>. Set VRC_DCC_JOB_HOLDER. "
        "Named world_* are proposed — not implemented."
    ) % wid
    (dest / "JOB.json").write_text(
        json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    review = {
        "schema": 1,
        "domain": WORLD,
        "world": wid,
        "updated": today,
        "note": "Seeded world map. world_* dumps are S01-c. Human SDK Publish.",
        "lessons": [],
        "items": [
            {
                "id": "example.world-probe",
                "node": "",
                "area": "scene",
                "title": "Read-only world probe (proposed world_probe)",
                "asked": "",
                "status": "unreviewed",
                "gate": "edit",
                "slice": "",
                "owner_ok": False,
                "evidence": [],
                "must_not": ["execute_code", "SDK Publish from the agent"],
                "notes": "Not implemented on com.vrc-dcc.tools yet.",
            }
        ],
    }
    (dest / "REVIEW.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (dest / "EVIDENCE.json").write_text(
        (TEMPL / "EVIDENCE.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (dest / "PLAN.json").write_text((TEMPL / "PLAN.json").read_text(encoding="utf-8"), encoding="utf-8")
    (dest / "STATE.md").write_text(
        "# %s (world overlay)\n\nSeeded %s. Not a Unity project. Proposed tools: %s.\n"
        % (wid, today, " ".join(PROPOSED)),
        encoding="utf-8",
    )
    print("created", dest)
    print("proposed", " ".join(PROPOSED))
    print("next: python maps/world_handshake.py", wid)


if __name__ == "__main__":
    main()
