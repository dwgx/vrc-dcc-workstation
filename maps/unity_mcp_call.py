# -*- coding: utf-8 -*-
"""Streamable HTTP client for CoplayDev Unity MCP at http://127.0.0.1:8080/mcp.

Named vrc_* only. Does not write the avatar Unity project tree from a station cwd.

Owner may have Unity MCP off or another product on 8080 — do not Start
CoplayDev from a station window to "fix" a missing catalog.

JSON-RPC errors and MCP result isError are nonzero. Progress notifications
are ignored until the matching request id arrives.

Examples:
  python maps/unity_mcp_call.py list
  python maps/unity_mcp_call.py vrc_audit args.json --avatar <id>
      (after python maps/gate.py <id> begin <review-id>; set VRC_DCC_JOB_HOLDER)
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from allowlist import ALWAYS_DENY, check_tool
from gate import load_job
from lease import require_http, resolve_holder

URL_DEFAULT = "http://127.0.0.1:8080/mcp"
FORBIDDEN = ALWAYS_DENY


def mcp_url() -> str:
    return (os.environ.get("VRC_DCC_MCP_URL") or URL_DEFAULT).rstrip("/")


def _iter_json_messages(raw: bytes) -> list[dict]:
    text = raw.decode("utf-8", "replace")
    found: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:].strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            found.append(obj)
    if not found and text.strip().startswith("{"):
        obj = json.loads(text)
        if isinstance(obj, dict):
            found.append(obj)
    return found


def _message_for_id(messages: list[dict], req_id: int | str) -> dict:
    wanted = req_id
    matched = [m for m in messages if "id" in m and m.get("id") == wanted]
    if matched:
        return matched[-1]
    # Notifications have method and no id — not a result.
    notify = [m for m in messages if m.get("method") and "id" not in m]
    if notify and not matched:
        raise RuntimeError("notify-before-result: no JSON-RPC result for id %r" % wanted)
    if not messages:
        raise RuntimeError("no json in response")
    raise RuntimeError("no JSON-RPC result for id %r in %s" % (wanted, json.dumps(messages)[:400]))


def _unwrap(msg: dict) -> dict:
    if "error" in msg:
        err = msg["error"]
        raise RuntimeError("jsonrpc error: " + json.dumps(err, ensure_ascii=False)[:800])
    result = msg.get("result")
    if isinstance(result, dict) and result.get("isError"):
        raise RuntimeError("tool isError: " + json.dumps(result, ensure_ascii=False)[:800])
    if result is None and "result" not in msg:
        raise RuntimeError("missing result: " + json.dumps(msg, ensure_ascii=False)[:400])
    return msg


def _post(payload: dict, session: str | None, timeout: int = 180, url: str | None = None) -> tuple[dict, str | None]:
    target = url or mcp_url()
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(target, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session:
        req.add_header("Mcp-Session-Id", session)
    req_id = payload.get("id")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            sid = resp.headers.get("mcp-session-id") or session
            data = resp.read()
            if not data:
                if payload.get("method", "").startswith("notifications/"):
                    return {}, sid
                raise RuntimeError("empty MCP body")
            messages = _iter_json_messages(data)
            if req_id is None:
                return (messages[-1] if messages else {}), sid
            return _unwrap(_message_for_id(messages, req_id)), sid
    except urllib.error.HTTPError as e:
        err = e.read()
        raise RuntimeError("HTTP %s %s" % (e.code, err[:1500].decode("utf-8", "replace"))) from e


def _session(timeout: int = 30, url: str | None = None) -> tuple[dict, str | None]:
    init_msg, sid = _post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "vrc-dcc-unity-http", "version": "1.2"},
            },
        },
        None,
        timeout=timeout,
        url=url,
    )
    _post(
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        sid,
        timeout=15,
        url=url,
    )
    return init_msg, sid


def list_tools(timeout: int = 60, url: str | None = None) -> list[str]:
    _, sid = _session(timeout=30, url=url)
    listed, _ = _post(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        sid,
        timeout=timeout,
        url=url,
    )
    tools = listed.get("result", {}).get("tools") or []
    return [t.get("name") for t in tools if t.get("name")]


def load_policy_file(path: Path | None) -> dict | None:
    if path is None or not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def call_tool(
    name: str,
    arguments: dict,
    timeout: int = 180,
    *,
    policy: dict | None = None,
    url: str | None = None,
) -> dict:
    ok, reason = check_tool(name, policy)
    if not ok:
        raise RuntimeError("refused %s: %s. Use named vrc_* after gate.py begin." % (name, reason))
    _, sid = _session(timeout=min(30, timeout), url=url)
    result, _ = _post(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        sid,
        timeout=timeout,
        url=url,
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


def _take_opt(argv: list[str], flag: str) -> str:
    if flag not in argv:
        return ""
    i = argv.index(flag)
    if i + 1 >= len(argv):
        raise RuntimeError("%s needs a value" % flag)
    val = argv[i + 1]
    del argv[i : i + 2]
    return val


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage: unity_mcp_call.py list\n"
            "       unity_mcp_call.py <vrc_tool> <args.json> --avatar <id> [--holder H] [--policy POLICY.json]",
            file=sys.stderr,
        )
        return 2
    cmd = sys.argv[1]
    argv = list(sys.argv[2:])
    try:
        policy_path = _take_opt(argv, "--policy")
        avatar = _take_opt(argv, "--avatar").strip().lower()
        holder = _take_opt(argv, "--holder")
    except RuntimeError as ex:
        print("error:", ex, file=sys.stderr)
        return 2
    policy = load_policy_file(Path(policy_path)) if policy_path else None
    ok, reason = check_tool(cmd, policy) if cmd != "list" else (True, "")
    if cmd != "list" and not ok:
        print("error: refused %s: %s" % (cmd, reason), file=sys.stderr)
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
    if not avatar:
        print(
            "error: tools/call needs --avatar after python maps/gate.py <avatar> begin <id>",
            file=sys.stderr,
        )
        return 2
    held = require_http(load_job(avatar), resolve_holder(holder))
    if held:
        print("error:", held, file=sys.stderr)
        return 2
    if not argv:
        print("usage: unity_mcp_call.py <vrc_tool> <args.json> --avatar <id>", file=sys.stderr)
        return 2
    try:
        arguments = _load_arguments(argv[0])
        out = call_tool(cmd, arguments, policy=policy)
    except Exception as ex:
        print("error:", ex, file=sys.stderr)
        return 2
    text = json.dumps(out, ensure_ascii=False, indent=2)
    out_path = argv[0] + ".out.json"
    with open(out_path, "w", encoding="utf-8") as wf:
        wf.write(text)
        wf.write("\n")
    print("wrote", out_path, "chars", len(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
