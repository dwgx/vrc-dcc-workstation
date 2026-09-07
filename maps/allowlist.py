# -*- coding: utf-8 -*-
"""Fail-closed MCP tool names for avatar jobs. No HTTP. No Unity."""
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
DENY_TOKENS = ("upload", "publish", "build_and_publish")
AVATAR_PREFIX = "vrc_"
WORLD_PREFIX = "world_"


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


def check_tool(name: str, policy: dict[str, Any] | None = None) -> tuple[bool, str]:
    """Return (allowed, reason). Avatar jobs: named vrc_* only."""
    n = (name or "").strip()
    if not n:
        return False, "empty tool name"
    low = n.lower()
    if n in ALWAYS_DENY or any(tok in low for tok in DENY_TOKENS):
        return False, "denied %s (human SDK / upload APIs / execute_code)" % n
    if n.startswith(WORLD_PREFIX):
        return False, "cross-domain world_* on an avatar job"
    disabled = set(_names(policy, "disable_mcp_tools"))
    if n in disabled:
        return False, "POLICY disable_mcp_tools %r" % n
    allow = _names(policy, "allow_mcp_tools")
    if allow:
        if n not in allow:
            return False, "not on POLICY allow_mcp_tools"
        return True, "allow_mcp_tools"
    if n.startswith(AVATAR_PREFIX):
        return True, "vrc prefix"
    return False, "not a named vrc_* tool"
