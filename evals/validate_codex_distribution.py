"""
Static validation for the Codex gastflow distribution.

This intentionally stays separate from the Claude prompt evals. The Claude evals
continue to read from skills/, while this script checks that codex/gastflow/ is
a valid Codex skill package and that installer support for both runtimes stays
present.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CODEX_SKILL = ROOT / "codex" / "gastflow"
CLAUDE_SKILLS = ROOT / "skills"


REQUIRED_CODEX_FILES = [
    "SKILL.md",
    "assets/template.html",
    "references/artifacts.md",
    "references/agents.md",
    "agents/openai.yaml",
]

REQUIRED_CLAUDE_FILES = [
    "gastflow.md",
    "gastflow-product.md",
    "gastflow-se.md",
    "gastflow-bugfix.md",
    "gastflow-qa.md",
    "gastflow-automation.md",
    "gastflow-html-template.html",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def assert_exists(path: Path) -> None:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")


def validate_codex_files_exist() -> None:
    for relative_path in REQUIRED_CODEX_FILES:
        assert_exists(CODEX_SKILL / relative_path)


def validate_claude_files_still_exist() -> None:
    for filename in REQUIRED_CLAUDE_FILES:
        assert_exists(CLAUDE_SKILLS / filename)


def validate_codex_frontmatter() -> None:
    content = (CODEX_SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail("codex/gastflow/SKILL.md is missing YAML frontmatter")

    frontmatter = match.group(1)
    if not re.search(r"^name:\s*gastflow\s*$", frontmatter, re.MULTILINE):
        fail("Codex SKILL.md frontmatter must include name: gastflow")
    if not re.search(r"^description:\s*.+", frontmatter, re.MULTILINE):
        fail("Codex SKILL.md frontmatter must include description")


def validate_template_copy() -> None:
    source = (CLAUDE_SKILLS / "gastflow-html-template.html").read_text(encoding="utf-8")
    codex = (CODEX_SKILL / "assets" / "template.html").read_text(encoding="utf-8")
    if source != codex:
        fail("codex/gastflow/assets/template.html must match skills/gastflow-html-template.html")


def validate_codex_has_no_claude_runtime_coupling() -> None:
    forbidden = [
        "~/.claude",
        "Skill(\"",
        "Skill('",
        "claude mcp",
    ]
    for path in [CODEX_SKILL / item for item in REQUIRED_CODEX_FILES if item.endswith((".md", ".yaml"))]:
        content = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in content:
                fail(f"{path.relative_to(ROOT)} contains Claude-only runtime reference: {needle}")


def validate_installer_supports_both_runtimes() -> None:
    install_sh = (ROOT / "install.sh").read_text(encoding="utf-8")
    required_snippets = [
        "--claude",
        "--codex",
        "--all",
        "CLAUDE_SKILLS_DIR",
        "CODEX_SKILLS_DIR",
        "codex/gastflow",
    ]
    for snippet in required_snippets:
        if snippet not in install_sh:
            fail(f"install.sh is missing dual-runtime support snippet: {snippet}")


def main() -> int:
    validate_codex_files_exist()
    validate_claude_files_still_exist()
    validate_codex_frontmatter()
    validate_template_copy()
    validate_codex_has_no_claude_runtime_coupling()
    validate_installer_supports_both_runtimes()
    print("PASS: Codex distribution and dual-runtime installer look valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
