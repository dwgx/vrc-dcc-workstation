#!/usr/bin/env python3
"""Static eval of the agent contract. No network. No payloads. Exit 1 on fail."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Cursor documents a 500-line ceiling for a single always-on rule file.
AGENTS_LINE_CEILING = 500
MDC_LINE_CEILING = 120

COMMON_TAGS = (
    "eval:owner-overlay",
    "eval:chat-cannot-waive",
    "eval:no-user-global-mcp",
    "eval:untrusted-data",
)

KIND_TAGS = {
    "debugger-workstation": ("eval:authorized-use-only",),
    "vrc-dcc-workstation": ("eval:human-sdk-publish",),
}

# Localized stop-line anchors (translations must keep the rule, not just English).
COMMON_PHRASES = {
    "en": (
        "OWNER.md",
        "Stop lines cannot be waived",
        "roleplay, jailbreak",
        "user-global",
        "commit messages in **English**",
    ),
    "zh-CN": (
        "OWNER.md",
        "不能取消红线",
        "角色扮演、越狱",
        "用户全局",
        "提交说明保持**英文**",
    ),
    "ja": (
        "OWNER.md",
        "ストップラインを外せません",
        "ロールプレイ、ジェイルブレイク",
        "ユーザーグローバル",
        "コミットメッセージは英語",
    ),
    "ko": (
        "OWNER.md",
        "스톱 라인을 해제하지 못합니다",
        "롤플레이, 탈옥",
        "사용자 전역",
        "커밋 메시지는 영어",
    ),
}

KIND_PHRASES = {
    "vrc-dcc-workstation": {
        "en": ("Build & Publish", "upload_vrchat_avatar", "Unity 6 MCP", "home/control-plane"),
        "zh-CN": ("Build & Publish", "upload_vrchat_avatar", "Unity 6 MCP", "home / 控制面"),
        "ja": ("Build & Publish", "upload_vrchat_avatar", "Unity 6 MCP", "home / 制御プレーン"),
        "ko": ("Build & Publish", "upload_vrchat_avatar", "Unity 6 MCP", "home / 제어면"),
    },
}

FORBIDDEN_PHRASES = (
    "minus waived stop lines",
    "不拒绝、不阻断",
    "do not refuse",
)

MUST_FILES = (
    "skills/vrc-dcc/references/slice-loop.md",
    "maps/gate.py",
    "OWNER.example.md",
    "docs/MAINTAIN.md",
    "docs/I18N.md",
    "docs/EVAL.md",
    "docs/BOOTSTRAP.md",
    "docs/AVATAR_PROFILE.md",
    "docs/DOMAINS.md",
    "docs/ITERATION.md",
    "docs/SOURCES.md",
    "templates/INIT_QUESTIONNAIRE.md",
    "templates/JOB.md",
    "locales.json",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
)


def fail(msg: str, bad: list[str]) -> None:
    print("FAIL", msg)
    for b in bad:
        print(" ", b)
    sys.exit(1)


def git_ls_files(*names: str) -> list[str]:
    r = subprocess.run(
        ["git", "ls-files", "--", *names],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        fail("git ls-files failed", [r.stderr.strip() or str(r.returncode)])
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def require_mentions(path: Path, needles: tuple[str, ...], label: str) -> None:
    if not path.is_file():
        fail(f"missing {label}", [str(path.relative_to(ROOT))])
    text = path.read_text(encoding="utf-8")
    miss = [n for n in needles if n not in text]
    if miss:
        fail(f"{label} must mention", [f"{path.relative_to(ROOT)}: {n}" for n in miss])


def main() -> None:
    cfg = json.loads((ROOT / "locales.json").read_text(encoding="utf-8"))
    kind = cfg.get("kind", "")
    if kind not in KIND_TAGS:
        fail(
            "locales.json kind must be debugger-workstation or vrc-dcc-workstation",
            [repr(kind)],
        )
    locales = cfg["locales"]
    missing = [p for p in MUST_FILES if not (ROOT / p).is_file()]
    if missing:
        fail("missing files", missing)

    if (ROOT / ".cursorrules").exists():
        fail("legacy .cursorrules must not exist; use AGENTS.md + .cursor/rules", [".cursorrules"])

    agents: list[Path] = []
    for loc in locales:
        if loc == cfg.get("canonical", "en"):
            agents.append(ROOT / "AGENTS.md")
        else:
            agents.append(ROOT / f"AGENTS.{loc}.md")
    missing = [str(p) for p in agents if not p.is_file()]
    if missing:
        fail("missing AGENTS siblings", missing)

    tags = list(COMMON_TAGS) + list(KIND_TAGS.get(kind, ()))
    tag_miss = []
    long_agents = []
    for path in agents:
        text = path.read_text(encoding="utf-8")
        nlines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
        if nlines > AGENTS_LINE_CEILING:
            long_agents.append(f"{path.name}: {nlines} lines (ceiling {AGENTS_LINE_CEILING})")
        for t in tags:
            needle = f"<!-- {t} -->"
            if needle not in text:
                tag_miss.append(f"{path.name}: {needle}")
        if "### Untrusted data" not in text and "### 不可信内容" not in text:
            if "### 信頼できないデータ" not in text and "### 신뢰할 수 없는 데이터" not in text:
                tag_miss.append(f"{path.name}: missing Untrusted-data heading")
    if tag_miss:
        fail("eval tags / untrusted heading missing from AGENTS siblings", tag_miss)
    if long_agents:
        fail("AGENTS siblings exceed Cursor always-on ceiling", long_agents)

    phrase_miss = []
    forbidden_hits = []
    for loc, path in zip(locales, agents):
        text = path.read_text(encoding="utf-8")
        for phrase in COMMON_PHRASES.get(loc, ()):
            if phrase not in text:
                phrase_miss.append(f"{path.name}: {phrase!r}")
        for phrase in KIND_PHRASES.get(kind, {}).get(loc, ()):
            if phrase not in text:
                phrase_miss.append(f"{path.name}: {phrase!r}")
        for bad in FORBIDDEN_PHRASES:
            if bad in text:
                forbidden_hits.append(f"{path.name}: {bad!r}")
    if phrase_miss:
        fail("localized contract anchors missing from AGENTS siblings", phrase_miss)

    extra_scan = [
        ROOT / "CONTRIBUTING.md",
        ROOT / "OWNER.example.md",
        ROOT / "docs" / "WORKSTATION_RULES.md",
    ]
    for path in extra_scan:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for bad in FORBIDDEN_PHRASES:
            if bad in text:
                forbidden_hits.append(f"{path.relative_to(ROOT)}: {bad!r}")
    if forbidden_hits:
        fail("forbidden waiver / refuse phrasing", forbidden_hits)

    i18n_miss = []
    for loc in locales:
        if loc == cfg.get("canonical", "en"):
            continue
        p = ROOT / "docs" / "i18n" / loc / "MAINTAIN.md"
        if not p.is_file():
            i18n_miss.append(str(p.relative_to(ROOT)))
    if i18n_miss:
        fail("missing MAINTAIN translations", i18n_miss)

    require_mentions(ROOT / "GEMINI.md", ("AGENTS.md", "OWNER.md"), "GEMINI.md")
    require_mentions(ROOT / "CLAUDE.md", ("AGENTS.md", "OWNER.md"), "CLAUDE.md")
    require_mentions(
        ROOT / "docs" / "AVATAR_PROFILE.md",
        ("no default avatar",),
        "docs/AVATAR_PROFILE.md",
    )

    kaguya_default = []
    for rel in git_ls_files("maps"):
        if not rel.endswith(".py"):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8")
        if 'default="kaguya"' in text or "default='kaguya'" in text:
            kaguya_default.append(rel)
    handshake_lock = []
    for rel in git_ls_files():
        if not rel.endswith(".md"):
            continue
        posix = rel.replace("\\", "/")
        if "/examples/" in posix:
            continue
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "handshake.py kaguya" in text:
            handshake_lock.append(posix)
    skill_root = ROOT / "skills" / "vrc-dcc"
    if skill_root.is_dir():
        for md in skill_root.rglob("*.md"):
            posix = md.relative_to(ROOT).as_posix()
            if "/examples/" in posix or posix in handshake_lock:
                continue
            text = md.read_text(encoding="utf-8")
            if "handshake.py kaguya" in text:
                handshake_lock.append(posix)
    if kaguya_default:
        fail("maps CLI must not default avatar to kaguya", kaguya_default)
    if handshake_lock:
        fail("public playbooks must not teach handshake.py kaguya (examples/ only)", handshake_lock)

    copilot = ROOT / ".github" / "copilot-instructions.md"
    if copilot.is_file():
        require_mentions(copilot, ("AGENTS.md", "OWNER.md"), "copilot-instructions.md")

    mdc_files = sorted((ROOT / ".cursor" / "rules").glob("*.mdc")) if (ROOT / ".cursor" / "rules").is_dir() else []
    if not mdc_files:
        fail("missing .cursor/rules/*.mdc pointer", [".cursor/rules"])
    mdc_long = []
    for mdc in mdc_files:
        text = mdc.read_text(encoding="utf-8")
        nlines = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
        if nlines > MDC_LINE_CEILING:
            mdc_long.append(f"{mdc.relative_to(ROOT)}: {nlines} lines (ceiling {MDC_LINE_CEILING})")
        miss = [n for n in ("AGENTS.md", "OWNER.md") if n not in text]
        if miss:
            fail(".cursor/rules mdc must mention", [f"{mdc.relative_to(ROOT)}: {n}" for n in miss])
    if mdc_long:
        fail("always-on mdc too long (keep a pointer, not a second constitution)", mdc_long)

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "OWNER.md" not in gitignore:
        fail(".gitignore must ignore OWNER.md", [".gitignore"])
    if "local.json" not in gitignore:
        fail(".gitignore must ignore local.json", [".gitignore"])
    if ".mcp.json" not in gitignore:
        fail(".gitignore must ignore project .mcp.json", [".gitignore"])
    if ".cursor/mcp.json" not in gitignore.replace("\\", "/"):
        fail(".gitignore must ignore .cursor/mcp.json", [".gitignore"])

    tracked_secret = git_ls_files("OWNER.md", "local.json")
    if tracked_secret:
        fail("OWNER.md / local.json must not be tracked", tracked_secret)

    boot = (ROOT / "scripts" / "bootstrap.ps1").read_text(encoding="utf-8")
    boot_norm = boot.replace("/", "\\")
    if ".cursor\\mcp.json" not in boot_norm:
        fail("bootstrap.ps1 must write project .cursor\\mcp.json", ["scripts/bootstrap.ps1"])
    if kind == "debugger-workstation":
        tpl = ROOT / "mcp" / "client-mcp.json.template"
        if not tpl.is_file():
            fail("missing router-only client MCP template", ["mcp/client-mcp.json.template"])
        data = json.loads(tpl.read_text(encoding="utf-8"))
        names = list(data.get("mcpServers", {}))
        if names != ["debugger-router"]:
            fail("client MCP template must contain only debugger-router", names)
        if "client-mcp.json.template" not in boot:
            fail("bootstrap.ps1 must render mcp/client-mcp.json.template", ["scripts/bootstrap.ps1"])

    eval_doc = (ROOT / "docs" / "EVAL.md").read_text(encoding="utf-8")
    if "LLM-as-judge" not in eval_doc:
        fail("docs/EVAL.md must state we do not ship LLM-as-judge attack benches", ["docs/EVAL.md"])

    print("eval-agent-contract: PASS")
    print("  kind    ", kind)
    print("  locales ", ", ".join(locales))
    print("  tags    ", ", ".join(tags))
    print("  agents  ", ", ".join(p.name for p in agents))
    print("  mdc     ", ", ".join(str(p.relative_to(ROOT)) for p in mdc_files))


if __name__ == "__main__":
    main()
