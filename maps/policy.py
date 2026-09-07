# -*- coding: utf-8 -*-
"""Fail-closed POLICY.json checks. Handshake uses this. No Unity."""
from __future__ import annotations

from typing import Any

from allowlist import AVATAR_PREFIX, deny_reason

SCHEMA = 1
PLACEHOLDERS = frozenset({"", "AVATAR_ID"})


def _str_field(data: dict, key: str) -> str | None:
    if key not in data:
        return None
    val = data[key]
    if val is None:
        return ""
    if not isinstance(val, str):
        return None
    return val


def validate_policy(folder_id: str, data: Any) -> list[str]:
    """Return error strings. Empty list = ok."""
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["POLICY.json must be an object"]
    schema = data.get("schema")
    if schema != SCHEMA:
        errs.append("POLICY schema must be integer %s (got %r)" % (SCHEMA, schema))
    avatar = _str_field(data, "avatar")
    if avatar is None:
        errs.append("POLICY avatar must be a string")
    elif avatar.strip() != folder_id:
        errs.append("POLICY avatar %r must equal maps folder %r" % (avatar, folder_id))
    root = _str_field(data, "unity_root_name")
    if root is None:
        errs.append("POLICY unity_root_name must be a string")
    elif root.strip() in PLACEHOLDERS:
        errs.append("POLICY unity_root_name is empty or still AVATAR_ID")
    for path_key in ("nipple_smr_path", "gogo_root_path"):
        if path_key not in data or data[path_key] is None:
            continue
        val = data[path_key]
        if not isinstance(val, str):
            errs.append("POLICY %s must be a string" % path_key)
        elif not val.strip():
            errs.append("POLICY %s is present but empty" % path_key)
    tools = data.get("disable_mcp_tools")
    if tools is None:
        tools = []
    if not isinstance(tools, list) or any(not isinstance(t, str) or not t.strip() for t in tools):
        errs.append("POLICY disable_mcp_tools must be a list of non-empty strings")
    else:
        seen: set[str] = set()
        for t in tools:
            if t in seen:
                errs.append("POLICY disable_mcp_tools duplicate %r" % t)
            seen.add(t)
    needles = data.get("leftover_needles")
    if needles is None:
        needles = []
    if not isinstance(needles, list) or any(not isinstance(n, str) for n in needles):
        errs.append("POLICY leftover_needles must be a list of strings")
    sku = data.get("sku_quota", 1)
    if type(sku) is bool or type(sku) is not int or sku < 1:
        errs.append("POLICY sku_quota must be a positive int")
    ttl = data.get("job_lease_ttl_sec")
    if ttl is not None and (type(ttl) is bool or type(ttl) is not int or ttl < 1):
        errs.append("POLICY job_lease_ttl_sec must be a positive int")
    allow = data.get("allow_mcp_tools")
    if allow is None:
        allow = []
    if not isinstance(allow, list) or any(not isinstance(t, str) or not t.strip() for t in allow):
        errs.append("POLICY allow_mcp_tools must be a list of non-empty strings")
    else:
        seen_allow: set[str] = set()
        for t in allow:
            if t in seen_allow:
                errs.append("POLICY allow_mcp_tools duplicate %r" % t)
            seen_allow.add(t)
            name = t.strip()
            if not name.startswith(AVATAR_PREFIX):
                errs.append("POLICY allow_mcp_tools %r must be a vrc_* name" % t)
                continue
            why = deny_reason(name)
            if why:
                errs.append("POLICY allow_mcp_tools %r is denied (%s)" % (t, why))
    return errs
