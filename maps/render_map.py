# -*- coding: utf-8 -*-
"""Merge maps/<avatar>/graph.json + notes.json -> MAP.md. Generic. Clothes mermaid is data-driven."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent


def render(folder: Path) -> Path:
    graph = json.loads((folder / "graph.json").read_text(encoding="utf-8"))
    notes = json.loads((folder / "notes.json").read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in graph.get("nodes") or []}
    aid = graph.get("avatar") or folder.name
    lines: list[str] = []
    lines.append("# {0} map (plugins / clothes)".format(aid))
    lines.append("")
    lines.append("Generated. Edit `notes.json` (remarks) or refresh `graph.json` (structure), then run `python render_map.py {0}`.".format(aid))
    lines.append("")
    lines.append("- avatar: `{0}`  scene: `{1}`".format(graph.get("avatar"), graph.get("scene")))
    lines.append("- dump: `{0}`  updated: `{1}`".format(graph.get("dump"), graph.get("updated")))
    if graph.get("dump_note"):
        lines.append("- " + graph["dump_note"])
    lines.append("")
    lines.append("Agents: **确定** is locked. **observed** is a lead. Codegraph does not replace this file.")
    lines.append("")

    lines.append("## 确定 (confirmed)")
    lines.append("")
    any_conf = False
    for nid, meta in notes.items():
        if meta.get("status") != "confirmed":
            continue
        any_conf = True
        node = by_id.get(nid, {})
        label = node.get("label", nid)
        path = node.get("path") or node.get("hierarchy") or ""
        lines.append("- **`{0}`** {1}".format(nid, label))
        if path:
            lines.append("  - path: `{0}`".format(path))
        lines.append("  - " + meta.get("note", "").replace("\n", " "))
        if meta.get("source"):
            lines.append("  - source: " + meta["source"])
        lines.append("")
    if not any_conf:
        lines.append("(none yet)")
        lines.append("")

    conflicts_path = folder / "conflicts.json"
    if conflicts_path.is_file():
        try:
            conflicts = json.loads(conflicts_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            conflicts = {}
        bias = conflicts.get("bias") or {}
        lanes = conflicts.get("lanes") or []
        lines.append("## Owner lanes (`conflicts.json`)")
        lines.append("")
        lines.append("Two gizmos on the same playable: do not silently pick. Playbook: `plugin-conflicts.md`.")
        lines.append("")
        if bias:
            for lane, winner in bias.items():
                lines.append("- **`{0}`** → `{1}`".format(lane, winner))
        elif lanes:
            for lane in lanes:
                if not isinstance(lane, dict):
                    continue
                lines.append("- **`{0}`** → `{1}`".format(lane.get("lane"), lane.get("winner")))
        else:
            lines.append("(empty — ask the Owner before overlapping gizmos)")
        lines.append("")

    lines.append("## observed (lead only)")
    lines.append("")
    any_obs = False
    for nid, meta in notes.items():
        if meta.get("status") != "observed":
            continue
        any_obs = True
        node = by_id.get(nid, {})
        lines.append("- **`{0}`** {1}: {2}".format(nid, node.get("label", ""), meta.get("note", "")))
    if not any_obs:
        lines.append("(none)")
    lines.append("")

    lines.append("## Folders / plugins")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("  assetsG[Assets/功能]")
    lines.append("  assetsC[Assets/衣服]")
    for n in graph.get("nodes") or []:
        if n.get("kind") == "plugin":
            safe = n["id"].replace(".", "_")
            lines.append("  {0}[\"{1}\"]".format(safe, str(n.get("label", "")).replace('"', "")))
            if str(n.get("path", "")).startswith("Assets/功能"):
                lines.append("  assetsG --> {0}".format(safe))
        if n.get("kind") in {"outfit", "pack"} and str(n.get("path", "")).startswith("Assets/衣服"):
            safe = n["id"].replace(".", "_")
            lines.append("  {0}[\"{1}\"]".format(safe, str(n.get("label", "")).replace('"', "")))
            lines.append("  assetsC --> {0}".format(safe))
    lines.append("```")
    lines.append("")

    lines.append("## Clothes Int")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TB")
    lines.append("  Clothes[\"Clothes Int\"]")
    selects = [
        e
        for e in (graph.get("edges") or [])
        if e.get("rel") == "selects" and e.get("from") == "param.Clothes"
    ]
    if selects:
        for e in selects:
            tid = e.get("to", "")
            node = by_id.get(tid, {})
            label = str(node.get("label") or tid).replace('"', "")
            param = str(node.get("param") or "")
            bit = param_bit(param)
            safe = tid.replace(".", "_")
            if bit:
                lines.append("  Clothes -->|{0}| {1}[{2}]".format(bit, safe, label))
            else:
                lines.append("  Clothes --> {0}[{1}]".format(safe, label))
    else:
        lines.append("  Clothes --> seed[no selects yet]")
    lines.append("```")
    lines.append("")

    lines.append("## Menus the owner sees")
    lines.append("")
    lines.append("| id | label | path |")
    lines.append("|---|---|---|")
    for n in graph.get("nodes") or []:
        if n.get("kind") == "menu":
            lines.append("| `{0}` | {1} | `{2}` |".format(n["id"], n.get("label"), n.get("path", "")))
    lines.append("")

    lines.append("## Nodes without a note")
    lines.append("")
    missing = [n["id"] for n in graph.get("nodes") or [] if n["id"] not in notes]
    if not missing:
        lines.append("(all mapped ids have a note or are structural-only)")
    else:
        for i in missing:
            n = by_id[i]
            lines.append("- `{0}` {1} `{2}`".format(i, n.get("label"), n.get("path", "")))
    lines.append("")

    lines.append("## How to refresh")
    lines.append("")
    lines.append("1. Avatar Unity window. `unityMCP` once.")
    lines.append("2. One dump (`audit-dump.txt` or `unity-dump.txt`).")
    lines.append("3. `python refresh.py {0} --from-dump dump.txt` (keeps ids + notes.json).".format(aid))
    lines.append("4. Patch `STATE.md` (or this avatar’s snapshot) if bits/hierarchy moved.")
    lines.append("")

    out = folder / "MAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def param_bit(param: str) -> str:
    if not param:
        return ""
    if "=" in param:
        return param.split("=", 1)[-1].strip()
    return ""


def main() -> None:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Render maps/<avatar>/MAP.md. No default product.")
    ap.add_argument("avatar", help="maps/<avatar> folder. Required. There is no default character.")
    args = ap.parse_args()
    folder = HERE / args.avatar
    if not (folder / "graph.json").is_file():
        raise SystemExit("no graph.json in %s" % folder)
    path = render(folder)
    print("wrote", path)


if __name__ == "__main__":
    main()
