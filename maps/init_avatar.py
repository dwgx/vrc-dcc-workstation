# -*- coding: utf-8 -*-
"""Create maps/<avatar>/ from templates. Does not write Unity or notes/CURRENT.md."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent
TEMPL = HERE / "templates"
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def main() -> None:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Seed maps/<avatar>/ from templates")
    ap.add_argument("avatar", help="lowercase id, e.g. my-avatar")
    args = ap.parse_args()
    aid = args.avatar.strip().lower()
    if not ID_RE.match(aid):
        raise SystemExit("avatar id must match [a-z][a-z0-9-]*")
    dest = HERE / aid
    if dest.exists():
        raise SystemExit("already exists: %s" % dest)

    dest.mkdir()
    today = date.today().isoformat()

    graph = json.loads((TEMPL / "graph.json").read_text(encoding="utf-8"))
    graph["avatar"] = aid
    graph["updated"] = today
    (dest / "graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (dest / "notes.json").write_text("{}\n", encoding="utf-8")

    state = (TEMPL / "STATE.md").read_text(encoding="utf-8").replace("AVATAR_ID", aid)
    (dest / "STATE.md").write_text(state, encoding="utf-8")

    readme = (TEMPL / "folder-README.md").read_text(encoding="utf-8").replace(
        "AVATAR_ID", aid
    )
    (dest / "README.md").write_text(readme, encoding="utf-8")

    review = json.loads((TEMPL / "REVIEW.json").read_text(encoding="utf-8"))
    review["avatar"] = aid
    review["updated"] = today
    review["note"] = "Seeded %s. New Unity work = unreviewed." % today
    (dest / "REVIEW.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    conf = json.loads((TEMPL / "conflicts.json").read_text(encoding="utf-8"))
    conf["avatar"] = aid
    conf["updated"] = today
    (dest / "conflicts.json").write_text(
        json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    job = json.loads((TEMPL / "JOB.json").read_text(encoding="utf-8"))
    job["avatar"] = aid
    (dest / "JOB.json").write_text(
        json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    policy = json.loads((TEMPL / "POLICY.json").read_text(encoding="utf-8"))
    policy["avatar"] = aid
    policy["unity_root_name"] = aid
    (dest / "POLICY.json").write_text(
        json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    dump_map = TEMPL / "dump-map.json"
    if dump_map.is_file():
        (dest / "dump-map.json").write_text(dump_map.read_text(encoding="utf-8"), encoding="utf-8")

    print("wrote", dest)
    print("next: python handshake.py", aid)
    print("then: python render_map.py", aid)
    print("then: python review.py render", aid)
    print("then: python review.py next", aid)


if __name__ == "__main__":
    main()
