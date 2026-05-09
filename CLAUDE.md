# gastflow — Claude Code Instructions

## What is gastflow?

gastflow is an open-source Claude Code skill that implements an agentic software development
workflow based on Spec Driven Development (SDD).

The user invokes `/gastflow` in any project. Claude Code acts as the Orchestrator:
clarifies requirements, writes a spec, and spawns specialized sub-agents (SE, QA, Automation)
using the Agent tool.

## Repository structure

```
gastflow/
├── skills/
│   ├── gastflow.md                    # Orchestrator (the /gastflow entry point)
│   ├── gastflow-product.md            # Product Agent (backlog generation)
│   ├── gastflow-se.md                 # SE Agent (feature implementation)
│   ├── gastflow-bugfix.md             # Bug Fix Agent (root-cause + minimal fix)
│   ├── gastflow-qa.md                 # QA Agent (acceptance testing)
│   ├── gastflow-automation.md         # Automation Agent (writes tests)
│   └── gastflow-html-template.html    # Shared HTML design system (not a skill)
├── install.sh         # Installs skills + template into ~/.claude/skills/
├── CLAUDE.md          # This file
└── README.md
```

## How to work on this project

The product is split across the skill files in `skills/`. The orchestration logic lives in `skills/gastflow.md`; each sub-agent has its own file.

**All artifacts are HTML + JSON pairs** (spec, state, backlog, plan), backed by the shared design system in `skills/gastflow-html-template.html`. The only Markdown that survives is `.gastflow/memory.md` (agent-only context).

When editing skills:
- Keep prompts clear and specific — vague prompts produce vague agent behavior
- If you change the artifact data shape, update both the JSON schema docs in the orchestrator skill AND the agent that writes that section
- The HTML template is the single source of visual truth — change CSS there, not in each skill
- Test by running `./install.sh` and then `/gastflow` in a test project. Open the generated `.html` files in a browser to verify the render.

## Testing changes

1. Edit `skills/gastflow.md`
2. Run `./install.sh` to reinstall
3. Open a test project in Claude Code
4. Run `/gastflow` and test a real feature request
