"""
Extracts agent prompts directly from skills/gastflow.md.

This ensures evals always test the prompts that are actually in production.
If gastflow.md changes, the evals automatically test the new version.
"""

import re
from pathlib import Path


def extract_agent_prompts(gastflow_md_path: str | Path) -> dict[str, str]:
    """
    Parses gastflow.md and extracts the prompt for each agent.

    Returns a dict with keys: "orchestrator", "se", "qa", "automation"
    Raises ValueError if a prompt section is not found.
    """
    content = Path(gastflow_md_path).read_text(encoding="utf-8")
    prompts = {}

    # Orchestrator prompt = everything from PHASE 1 through end of PHASE 2
    orchestrator_match = re.search(
        r"## PHASE 1.*?(?=## PHASE 3)", content, re.DOTALL
    )
    if not orchestrator_match:
        raise ValueError("Could not find Orchestrator prompt (PHASE 1/2) in gastflow.md")
    prompts["orchestrator"] = orchestrator_match.group(0).strip()

    # SE, QA, Automation prompts are inside fenced code blocks in PHASE 3
    # Each block is preceded by a label like "**SE Agent prompt:**" or "### Step 1: SE Agent"
    agent_sections = {
        "se": r"(?:SE Agent prompt|Step 1: SE Agent).*?```\n(.*?)```",
        "qa": r"(?:\*\*QA Agent prompt|QA Agent prompt).*?```\n(.*?)```",
        "automation": r"(?:\*\*Automation Agent prompt|Automation Agent prompt).*?```\n(.*?)```",
    }

    for agent, pattern in agent_sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            raise ValueError(
                f"Could not find {agent} agent prompt in gastflow.md. "
                f"Make sure PHASE 3 contains the expected prompt blocks."
            )
        prompts[agent] = match.group(1).strip()

    return prompts
