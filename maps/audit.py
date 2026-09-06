# -*- coding: utf-8 -*-
"""Deprecated. Always exit 2. Named vrc_audit in a Unity chat that has unityMCP.

Do not set VRC_DCC_ALLOW_AUDIT_HTTP. Do not POST execute_code.
"""
from __future__ import annotations

import sys


def main() -> int:
    print(
        "error: maps/audit.py HTTP is deprecated (use-vrc-audit). "
        "Call vrc_audit in a Unity window that already has unityMCP. "
        "If Unity MCP is off, do not Start it from station and do not POST 8080.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
