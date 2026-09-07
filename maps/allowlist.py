# -*- coding: utf-8 -*-
"""Names accepted by the station's optional named-tool client. No HTTP. No Unity.

This is not a global filter for native MCP, an installed provider CLI/SDK, or
project-owned Editor builders. See docs/WORLD_PRODUCTION.md for production.
Prefix is not a ship bit: this client accepts only implemented station tools.
IMPLEMENTED_WORLD stays empty until a station World adapter actually ships.
"""
from __future__ import annotations

from typing import Any

ALWAYS_DENY = frozenset(
    {
        "execute_code",
        "execute_csharp",
        "upload_vrchat_avatar",
        "upload_avatar",
    }
)
AVATAR_PREFIX = "vrc_"
WORLD_PREFIX = "world_"
# Prefix is not a ship bit. S01-c may add world_probe only after an authorized Worlds Editor.
IMPLEMENTED_WORLD = frozenset()


def _names(policy: dict | None, key: str) -> list[str]:
    raw = (policy or {}).get(key)
    if raw is None:
        return []
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return out


def _norm(name: str) -> str:
    return (name or "").strip().replace("-", "_").casefold()


def deny_reason(name: str, domain: str = "avatar") -> str | None:
    """Always-deny / upload-publish / wrong-domain prefix. None if not in that set."""
    n = (name or "").strip()
    if not n:
        return "empty tool name"
    low = n.casefold()
    norm = _norm(n)
    if low in {x.casefold() for x in ALWAYS_DENY}:
        return "denied %s (human SDK / upload APIs / execute_code)" % n
    if "execute_code" in norm or "execute_csharp" in norm:
        return "denied %s (human SDK / upload APIs / execute_code)" % n
    if "build_and_publish" in norm:
        return "denied %s (human SDK / upload APIs / execute_code)" % n
    parts = [p for p in norm.split("_") if p]
    if "upload" in parts or "publish" in parts:
        return "denied %s (human SDK / upload APIs / execute_code)" % n
    if domain == "avatar" and low.startswith(WORLD_PREFIX):
        return "cross-domain world_* on an avatar job"
    if domain == "world" and low.startswith(AVATAR_PREFIX):
        return "cross-domain vrc_* on a world job"
    return None


def check_tool(
    name: str,
    policy: dict[str, Any] | None = None,
    *,
    domain: str = "avatar",
) -> tuple[bool, str]:
    """Return (allowed, reason). Avatar: named vrc_*. World: implemented world_* only."""
    n = (name or "").strip()
    if not n:
        return False, "empty tool name"
    d = (domain or "avatar").strip().lower()
    denied = deny_reason(n, d)
    if denied:
        return False, denied
    disabled = set(_names(policy, "disable_mcp_tools"))
    if n in disabled:
        return False, "POLICY disable_mcp_tools %r" % n
    allow = _names(policy, "allow_mcp_tools")
    prefix = WORLD_PREFIX if d == "world" else AVATAR_PREFIX

    def _world_shipped() -> tuple[bool, str] | None:
        if d != "world":
            return None
        if n not in IMPLEMENTED_WORLD:
            return False, "world_* not implemented (S01-c ships world_probe only)"
        return None

    if allow:
        if n not in allow:
            return False, "not on POLICY allow_mcp_tools"
        if not n.startswith(prefix):
            return False, "allow_mcp_tools is still %s* only" % prefix
        blocked = _world_shipped()
        if blocked:
            return blocked
        return True, "allow_mcp_tools"
    if n.startswith(prefix):
        blocked = _world_shipped()
        if blocked:
            return blocked
        return True, "%s prefix" % prefix.rstrip("_")
    if d == "world":
        return False, "not a named world_* tool"
    return False, "not a named vrc_* tool"
