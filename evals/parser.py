"""
Extracts agent prompts from the gastflow skill files.

Each sub-agent lives in its own skill file (skills/gastflow-<role>.md) and is
invoked by the orchestrator via the Skill tool. The orchestrator prompt lives
in skills/gastflow.md (PHASE 1 through PHASE 2).

This ensures evals always test the prompts that are actually in production.
If any skill file changes, the evals automatically test the new version.
"""

from __future__ import annotations

import re
from pathlib import Path


def extract_agent_prompts(gastflow_md_path: str | Path) -> dict[str, str]:
    """
    Extracts the prompt for each agent from the skills/ directory.

    Returns a dict with keys: "orchestrator", "se", "qa", "automation".
    Raises ValueError if a required prompt file is missing or malformed.
    """
    gastflow_md = Path(gastflow_md_path)
    skills_dir = gastflow_md.parent
    prompts = {}

    # Orchestrator prompt = PHASE 1 through end of PHASE 2 of skills/gastflow.md
    content = gastflow_md.read_text(encoding="utf-8")
    orchestrator_match = re.search(
        r"## PHASE 1.*?(?=## PHASE 3)", content, re.DOTALL
    )
    if not orchestrator_match:
        raise ValueError("Could not find Orchestrator prompt (PHASE 1/2) in gastflow.md")
    prompts["orchestrator"] = orchestrator_match.group(0).strip()

    # Sub-agents each live in their own skill file
    agent_files = {
        "se": "gastflow-se.md",
        "qa": "gastflow-qa.md",
        "automation": "gastflow-automation.md",
    }

    for agent, filename in agent_files.items():
        path = skills_dir / filename
        if not path.exists():
            raise ValueError(
                f"Could not find {agent} agent prompt at {path}. "
                f"Each sub-agent should have its own skill file."
            )
        prompts[agent] = path.read_text(encoding="utf-8").strip()

    return prompts
