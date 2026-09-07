# -*- coding: utf-8 -*-
"""Fail-closed WORLD POLICY.json. Handshake uses this. No Unity."""
from __future__ import annotations

from typing import Any

SCHEMA = 1
PLACEHOLDERS = frozenset({"WORLD_ID", "AVATAR_ID"})


def validate_world_policy(folder_id: str, data: Any) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["WORLD POLICY.json must be an object"]
    if data.get("schema") != SCHEMA:
        errs.append("WORLD POLICY schema must be integer %s (got %r)" % (SCHEMA, data.get("schema")))
    if (data.get("domain") or "") != "world":
        errs.append("WORLD POLICY domain must be 'world'")
    world = data.get("world")
    if not isinstance(world, str) or world.strip() != folder_id:
        errs.append("WORLD POLICY world %r must equal maps/worlds folder %r" % (world, folder_id))
    if data.get("avatar"):
        errs.append("WORLD POLICY must not carry an avatar field")
    tools = data.get("disable_mcp_tools")
    if tools is None:
        tools = []
    if not isinstance(tools, list) or any(not isinstance(t, str) or not t.strip() for t in tools):
        errs.append("WORLD POLICY disable_mcp_tools must be a list of non-empty strings")
    root = data.get("unity_product_fingerprint")
    if root is not None and not isinstance(root, str):
        errs.append("WORLD POLICY unity_product_fingerprint must be a string")
    elif isinstance(root, str) and root.strip() in {"WORLD_ID", "AVATAR_ID"}:
        errs.append("WORLD POLICY unity_product_fingerprint is still a placeholder")
    sku = data.get("sku_quota", 1)
    if type(sku) is bool or type(sku) is not int or sku < 1:
        errs.append("WORLD POLICY sku_quota must be a positive int")
    return errs
