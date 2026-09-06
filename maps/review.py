# -*- coding: utf-8 -*-
"""Review board: what was reviewed vs what is new.

  python review.py render <avatar>
  python review.py lint <avatar>
  python review.py coverage <avatar>
  python review.py next <avatar>
  python review.py next <avatar> --json

Source of truth is maps/<avatar>/REVIEW.json. REVIEW.md is generated.
No default character. New Unity work lands as status=unreviewed (or edit if an
Edit dump exists). Never set world without the Owner confirming in VRChat.

MAP = what exists. Board = what was proven. Lessons = failed approaches
the next agent must not retry.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent
STATUSES = ("unreviewed", "edit", "world", "accepted", "blocked", "wontfix")
GATES = ("edit", "world", "blender", "none")
OPEN_STATUSES = ("unreviewed", "edit", "blocked")
COVERAGE_KINDS = ("plugin", "outfit", "menu", "body", "mesh")
EVIDENCE_KINDS = ("dump", "playbook", "screenshot", "note", "unity", "world")
STATUS_LABEL = {
    "unreviewed": "unreviewed — new or never proven",
    "edit": "edit — Editor dump / ObjectToggle / blendshape",
    "world": "world — Owner confirmed after SDK upload",
    "accepted": "accepted — known cost, do not 'fix'",
    "blocked": "blocked — cannot proceed",
    "wontfix": "wontfix — Owner said skip",
}
GATE_ORDER = {"world": 0, "blender": 1, "edit": 2, "none": 3}


def avatar_dir(name: str) -> Path:
    p = HERE / name
    if not p.is_dir():
        raise SystemExit("no maps/%s/" % name)
    return p


def load_review(name: str) -> dict:
    path = avatar_dir(name) / "REVIEW.json"
    if not path.is_file():
        raise SystemExit("missing %s (copy maps/templates/REVIEW.json)" % path)
    return json.loads(path.read_text(encoding="utf-8"))


def load_graph(name: str) -> dict | None:
    path = avatar_dir(name) / "graph.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_list(raw) -> list:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw] if raw else []
    if isinstance(raw, list):
        return raw
    return [raw]


def evidence_ref(item) -> str:
    if isinstance(item, dict):
        return str(item.get("ref") or item.get("path") or "")
    return str(item)


def lint_data(data: dict) -> list[str]:
    errs: list[str] = []
    items = data.get("items")
    if not isinstance(items, list):
        return ["items must be a list"]
    seen: set[str] = set()
    for i, it in enumerate(items):
        loc = "items[%d]" % i
        if not isinstance(it, dict):
            errs.append(loc + " not an object")
            continue
        iid = it.get("id")
        if not iid:
            errs.append(loc + " missing id")
        elif iid in seen:
            errs.append("duplicate id: " + iid)
        else:
            seen.add(iid)
        st = it.get("status")
        if st not in STATUSES:
            errs.append("%s status %r not in %s" % (iid or loc, st, STATUSES))
        gate = it.get("gate")
        if gate not in GATES:
            errs.append("%s gate %r not in %s" % (iid or loc, gate, GATES))
        if st == "world" and not it.get("owner_ok"):
            errs.append("%s status=world needs owner_ok true (Owner said it in VRChat)" % (iid or loc))
        if st == "edit" and not evidence_list(it.get("evidence")):
            errs.append("%s status=edit needs evidence (dump path / field)" % (iid or loc))
        for e in evidence_list(it.get("evidence")):
            if isinstance(e, dict) and e.get("kind") and e["kind"] not in EVIDENCE_KINDS:
                errs.append("%s evidence kind %r not in %s" % (iid or loc, e["kind"], EVIDENCE_KINDS))
    lessons = data.get("lessons") or []
    if lessons and not isinstance(lessons, list):
        errs.append("lessons must be a list")
    else:
        lseen: set[str] = set()
        for i, les in enumerate(lessons):
            if not isinstance(les, dict):
                errs.append("lessons[%d] not an object" % i)
                continue
            lid = les.get("id")
            if not lid:
                errs.append("lessons[%d] missing id" % i)
            elif lid in lseen:
                errs.append("duplicate lesson id: " + lid)
            else:
                lseen.add(lid)
    return errs


def coverage_gaps(name: str, data: dict) -> list[str]:
    graph = load_graph(name)
    if not graph:
        return []
    covered: set[str] = set()
    for it in data.get("items") or []:
        node = it.get("node")
        if node:
            covered.add(node)
        for extra in it.get("nodes") or []:
            covered.add(extra)
        nid = it.get("id")
        if nid:
            covered.add(nid)
    gaps = []
    for n in graph.get("nodes") or []:
        nid = n.get("id")
        if not nid or nid in covered:
            continue
        kind = n.get("kind")
        if kind not in COVERAGE_KINDS:
            continue
        gaps.append("%s\t%s\t%s" % (nid, kind, n.get("label", "")))
    return gaps


def open_items(data: dict) -> list[dict]:
    items = [it for it in (data.get("items") or []) if it.get("status") in OPEN_STATUSES]
    items.sort(key=lambda it: (GATE_ORDER.get(it.get("gate"), 9), it.get("id") or ""))
    return items


def render_evidence_line(e) -> str:
    if isinstance(e, dict):
        kind = e.get("kind") or "note"
        ref = evidence_ref(e)
        cap = e.get("caption") or e.get("note") or ""
        if kind == "screenshot" and ref:
            alt = cap or ref
            extra = (" — " + cap) if cap and cap != ref else ""
            return "  - screenshot: ![%s](%s)%s" % (alt, ref, extra)
        if cap:
            return "  - %s `%s` — %s" % (kind, ref, cap)
        return "  - %s `%s`" % (kind, ref)
    return "  - %s" % e


def render_md(name: str, data: dict) -> str:
    items = list(data.get("items") or [])
    counts = Counter(it.get("status") for it in items)
    lines: list[str] = []
    lines.append("# Review board — %s" % data.get("avatar", name))
    lines.append("")
    lines.append("<!-- agent: python maps/review.py next %s  |  source REVIEW.json  |  do not hand-edit -->" % name)
    lines.append("")
    lines.append("Generated from `REVIEW.json`. Do not hand-edit this file.")
    lines.append("")
    lines.append("- updated: `%s`" % data.get("updated", ""))
    if data.get("note"):
        lines.append("- " + data["note"])
    lines.append(
        "- counts: unreviewed **%d** · edit **%d** · world **%d** · accepted **%d** · blocked **%d** · wontfix **%d**"
        % (
            counts["unreviewed"],
            counts["edit"],
            counts["world"],
            counts["accepted"],
            counts["blocked"],
            counts["wontfix"],
        )
    )
    lines.append("")
    lines.append(
        "Agents: **unreviewed** is the work. **edit** is Editor-only. "
        "**world** only after the Owner says so in VRChat. New writes land unreviewed. "
        "`python maps/review.py next %s` prints the queue."
        % name
    )
    lines.append("")

    lessons = data.get("lessons") or []
    lines.append("## Failed approaches (do not retry)")
    lines.append("")
    if not lessons:
        lines.append("(none recorded)")
        lines.append("")
    else:
        for les in lessons:
            lines.append("### `%s` %s" % (les.get("id"), les.get("title", "")))
            lines.append("")
            if les.get("failed"):
                lines.append("- failed: " + les["failed"])
            if les.get("do"):
                lines.append("- do: " + les["do"])
            if les.get("playbook"):
                lines.append("- playbook: `%s`" % les["playbook"])
            lines.append("")

    nxt = open_items(data)
    lines.append("## Next (agent queue)")
    lines.append("")
    if not nxt:
        lines.append("(board has no unreviewed / edit / blocked rows)")
        lines.append("")
    else:
        for it in nxt:
            lines.append(
                "- **%s** `%s` · gate `%s` — %s"
                % (it.get("status"), it.get("id"), it.get("gate"), it.get("title", ""))
            )
        lines.append("")

    groups = [
        ("unreviewed", "Unreviewed"),
        ("edit", "Edit-proven (not world)"),
        ("world", "World-proven"),
        ("accepted", "Accepted costs"),
        ("blocked", "Blocked"),
        ("wontfix", "Wontfix"),
    ]
    by: dict[str, list] = {k: [] for k, _ in groups}
    for it in items:
        by.setdefault(it.get("status") or "unreviewed", []).append(it)

    for key, title in groups:
        lines.append("## %s" % title)
        lines.append("")
        bucket = by.get(key) or []
        if not bucket:
            lines.append("(none)")
            lines.append("")
            continue
        for it in bucket:
            lines.append("### `%s` %s" % (it.get("id"), it.get("title", "")))
            lines.append("")
            lines.append("- status: **%s** · gate: `%s`" % (it.get("status"), it.get("gate")))
            if it.get("node"):
                lines.append("- map node: `%s`" % it["node"])
            extra_nodes = it.get("nodes") or []
            if extra_nodes:
                lines.append("- also: " + ", ".join("`%s`" % n for n in extra_nodes))
            if it.get("asked"):
                lines.append("- asked: " + it["asked"])
            if it.get("slice"):
                lines.append("- slice: " + it["slice"])
            ev = evidence_list(it.get("evidence"))
            if ev:
                lines.append("- evidence:")
                for e in ev:
                    lines.append(render_evidence_line(e))
            if it.get("must_not"):
                lines.append("- must-not: " + "; ".join(it["must_not"]))
            if it.get("notes"):
                lines.append("- notes: " + it["notes"].replace("\n", " "))
            lines.append("")

    gaps = coverage_gaps(name, data)
    lines.append("## Coverage gaps (on avatar, no review row)")
    lines.append("")
    lines.append(
        "Graph nodes (`plugin` / `outfit` / `menu` / `body` / `mesh`) without a REVIEW `id`, `node`, or `nodes`. "
        "New gizmos/clothes should get a row the same slice they are wired."
    )
    lines.append("")
    if not gaps:
        lines.append("(all mapped plugin/outfit/menu ids have a row or are folders)")
    else:
        for g in gaps:
            parts = g.split("\t", 2)
            if len(parts) == 3:
                lines.append("- `%s` (%s) %s" % (parts[0], parts[1], parts[2]))
            else:
                lines.append("- `%s`" % g.replace("\t", " "))
    lines.append("")
    lines.append("## How")
    lines.append("")
    lines.append("1. Edit `maps/<avatar>/REVIEW.json` (items + lessons).")
    lines.append("2. `python maps/review.py lint <avatar> && python maps/review.py render <avatar>`.")
    lines.append("3. After a Unity slice: upsert the rows you touched. Do not mark `world` yourself.")
    lines.append("4. Queue: `python maps/review.py next <avatar>` (add `--json` for agents).")
    lines.append("5. Screenshots: `maps/<avatar>/evidence/` with `{kind: screenshot, ref: evidence/foo.png}`.")
    lines.append("")
    return "\n".join(lines) + "\n"


def cmd_render(name: str) -> int:
    data = load_review(name)
    errs = lint_data(data)
    if errs:
        print("lint failed:", file=sys.stderr)
        for e in errs:
            print(" -", e, file=sys.stderr)
        return 2
    out = avatar_dir(name) / "REVIEW.md"
    out.write_text(render_md(name, data), encoding="utf-8")
    print("wrote", out)
    nxt = open_items(data)
    print("next", len(nxt), "open;", len(data.get("lessons") or []), "lessons")
    return 0


def cmd_lint(name: str) -> int:
    data = load_review(name)
    errs = lint_data(data)
    if errs:
        for e in errs:
            print(e)
        return 2
    print("ok", len(data.get("items") or []), "items;", len(data.get("lessons") or []), "lessons")
    return 0


def cmd_coverage(name: str) -> int:
    data = load_review(name)
    gaps = coverage_gaps(name, data)
    if not gaps:
        print("ok — no plugin/outfit/menu/body/mesh gaps")
        return 0
    for g in gaps:
        print(g)
    return 0


def cmd_next(name: str, as_json: bool) -> int:
    data = load_review(name)
    errs = lint_data(data)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 2
    nxt = open_items(data)
    if as_json:
        payload = {
            "avatar": data.get("avatar", name),
            "updated": data.get("updated"),
            "open": [
                {
                    "id": it.get("id"),
                    "status": it.get("status"),
                    "gate": it.get("gate"),
                    "title": it.get("title"),
                    "node": it.get("node"),
                    "asked": it.get("asked"),
                    "must_not": it.get("must_not") or [],
                }
                for it in nxt
            ],
            "lessons": data.get("lessons") or [],
            "counts": dict(Counter(it.get("status") for it in (data.get("items") or []))),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if not nxt:
        print("ok — no unreviewed / edit / blocked")
        return 0
    for it in nxt:
        print("%s\t%s\t%s\t%s" % (it.get("status"), it.get("gate"), it.get("id"), it.get("title", "")))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("render", "lint", "coverage", "next"))
    ap.add_argument("avatar")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    if args.cmd == "render":
        return cmd_render(args.avatar)
    if args.cmd == "lint":
        return cmd_lint(args.avatar)
    if args.cmd == "coverage":
        return cmd_coverage(args.avatar)
    return cmd_next(args.avatar, args.as_json)


if __name__ == "__main__":
    utf8_stdio()
    raise SystemExit(main())
