# -*- coding: utf-8 -*-
"""Streamable HTTP client for CoplayDev Unity MCP at http://127.0.0.1:8080/mcp.

Named vrc_* only. Does not write the avatar Unity project tree from a station cwd.

Owner may have Unity MCP off or another product on 8080 — do not Start
CoplayDev from a station window to "fix" a missing catalog.

Examples:
  python maps/unity_mcp_call.py list
  python maps/unity_mcp_call.py vrc_audit maps/<avatar>/vrc-audit-empty.json
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8080/mcp"
FORBIDDEN = frozenset({"execute_code", "execute_csharp"})


def _parse_sse(raw: bytes) -> dict:
    text = raw.decode("utf-8", "replace")
    for line in text.splitlines():
        if line.startswith("data:"):
            return json.loads(line[5:].strip())
    if text.strip().startswith("{"):
        return json.loads(text)
    raise RuntimeError("no json in response: " + text[:400])


def _post(payload: dict, session: str | None, timeout: int = 180) -> tuple[dict, str | None]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session:
        req.add_header("Mcp-Session-Id", session)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            sid = resp.headers.get("mcp-session-id") or session
            data = resp.read()
            if not data:
                return {}, sid
            return _parse_sse(data), sid
    except urllib.error.HTTPError as e:
        err = e.read()
        raise RuntimeError("HTTP %s %s" % (e.code, err[:1500].decode("utf-8", "replace"))) from e


def _session(timeout: int = 30) -> tuple[dict, str | None]:
    init_msg, sid = _post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "vrc-dcc-unity-http", "version": "1.1"},
            },
        },
        None,
        timeout=timeout,
    )
    if "error" in init_msg:
        raise RuntimeError("initialize: " + json.dumps(init_msg, ensure_ascii=False)[:800])
    _post(
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        sid,
        timeout=15,
    )
    return init_msg, sid


def list_tools(timeout: int = 60) -> list[str]:
    _, sid = _session(timeout=30)
    listed, _ = _post(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        sid,
        timeout=timeout,
    )
    tools = listed.get("result", {}).get("tools") or []
    return [t.get("name") for t in tools if t.get("name")]


def call_tool(name: str, arguments: dict, timeout: int = 180) -> dict:
    if name in FORBIDDEN:
        raise RuntimeError(
            "refused %s. Use named vrc_* (vrc_audit …). Do not invent execute_code."
            % name
        )
    _, sid = _session(timeout=30)
    result, _ = _post(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        sid,
        timeout=timeout,
    )
    return result


def _load_arguments(path: str) -> dict:
    if not path.lower().endswith(".json"):
        raise RuntimeError(
            "args must be .json (named vrc_*). Do not pass .txt as codedom execute_code."
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise RuntimeError("args json must be an object")
    return data


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage: unity_mcp_call.py list\n"
            "       unity_mcp_call.py <vrc_tool> <args.json>",
            file=sys.stderr,
        )
        return 2
    cmd = sys.argv[1]
    if cmd in FORBIDDEN:
        print("error: refused %s" % cmd, file=sys.stderr)
        return 2
    if cmd == "list":
        try:
            names = list_tools()
        except Exception as ex:
            print("error:", ex, file=sys.stderr)
            return 2
        vrc = [n for n in names if n.startswith("vrc_")]
        print("count", len(names))
        print("vrc", " ".join(vrc) if vrc else "-")
        print("execute_code", "execute_code" in names)
        return 0
    if len(sys.argv) < 3:
        print("usage: unity_mcp_call.py <vrc_tool> <args.json>", file=sys.stderr)
        return 2
    try:
        arguments = _load_arguments(sys.argv[2])
        out = call_tool(cmd, arguments)
    except Exception as ex:
        print("error:", ex, file=sys.stderr)
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2)
    out_path = sys.argv[2] + ".out.json"
    with open(out_path, "w", encoding="utf-8") as wf:
        wf.write(text)
        wf.write("\n")
    print("wrote", out_path, "chars", len(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
