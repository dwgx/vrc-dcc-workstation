# -*- coding: utf-8 -*-
"""Search maps/<avatar>/graph.json + notes.json. USB shelf: query.py library <words>."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent


def load_avatar(name: str) -> tuple[dict, dict]:
    root = HERE / name
    g = json.loads((root / "graph.json").read_text(encoding="utf-8"))
    n = json.loads((root / "notes.json").read_text(encoding="utf-8"))
    return g, n


def blob(node: dict, note: dict | None) -> str:
    parts = [node.get("id", ""), node.get("kind", ""), node.get("label", ""),
             node.get("path", "") or "", node.get("hierarchy", "") or "",
             str(node.get("param", "")), str(node.get("bits", ""))]
    if note:
        parts += [note.get("status", ""), note.get("note", ""), note.get("source", "")]
    return " ".join(parts).lower()


def main() -> int:
    utf8_stdio()
    if len(sys.argv) >= 2 and sys.argv[1] == "library":
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        from library.find import main as lib_main
        return lib_main()
    p = argparse.ArgumentParser(description="Query maps/<avatar> index. No default product.")
    p.add_argument("avatar", help="maps/<avatar> folder. Required. There is no default character.")
    p.add_argument("terms", nargs="*", help="AND match on id/label/path/note")
    p.add_argument("--confirmed", action="store_true")
    p.add_argument("--observed", action="store_true")
    p.add_argument("--id", dest="node_id")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    root = HERE / args.avatar
    if not (root / "graph.json").exists():
        print("no index:", root, file=sys.stderr)
        print("avatars:", [x.name for x in HERE.iterdir() if (x / "graph.json").exists()])
        print("USB shelf: python query.py library <words>", file=sys.stderr)
        return 2
    graph, notes = load_avatar(args.avatar)
    hits = []
    for node in graph["nodes"]:
        nid = node["id"]
        note = notes.get(nid)
        if args.node_id and nid != args.node_id:
            continue
        st = (note or {}).get("status", "")
        if args.confirmed and st != "confirmed":
            continue
        if args.observed and st != "observed":
            continue
        if args.terms:
            b = blob(node, note)
            if not all(t.lower() in b for t in args.terms):
                continue
        hits.append((node, note))
    terms_l = [t.lower() for t in (args.terms or [])]

    def rank(pair: tuple[dict, dict | None]) -> tuple[int, str]:
        node = pair[0]
        bid = node["id"].lower()
        lab = (node.get("label") or "").lower()
        if terms_l and all(t in bid for t in terms_l):
            return (0, bid)
        if terms_l and all(t in lab for t in terms_l):
            return (1, bid)
        return (2, bid)

    hits.sort(key=rank)
    if not hits:
        if args.json:
            print("[]")
        else:
            print("0 hits. Next: notes/INDEX.md or query.py library, then Booth (see AGENT.md).")
        return 1
    if args.json:
        out = []
        for node, note in hits:
            row = dict(node)
            if note:
                row["note"] = note
            out.append(row)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    for node, note in hits:
        print("id:", node["id"])
        print("  kind:", node.get("kind"), " label:", node.get("label"))
        if node.get("path"):
            print("  path:", node["path"])
        if node.get("hierarchy"):
            print("  hierarchy:", node["hierarchy"])
        if note:
            print("  status:", note.get("status"))
            print("  note:", note.get("note"))
            if note.get("source"):
                print("  source:", note["source"])
        else:
            print("  status: (no remark)")
        print()
    print("hits:", len(hits), "  map:", (HERE / args.avatar / "MAP.md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
