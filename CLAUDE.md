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
│   └── gastflow.md    # The /gastflow skill — this is the entire product
├── install.sh         # Copies gastflow.md to ~/.claude/skills/
├── CLAUDE.md          # This file
└── README.md
```

## How to work on this project

The entire product is `skills/gastflow.md`. That's the file to edit when improving gastflow.

When editing the skill:
- The Orchestrator behavior is in PHASE 1 and PHASE 2
- The agent prompts are in PHASE 3
- Keep prompts clear and specific — vague prompts produce vague agent behavior
- Test by running `./install.sh` and then `/gastflow` in a test project

## Testing changes

1. Edit `skills/gastflow.md`
2. Run `./install.sh` to reinstall
3. Open a test project in Claude Code
4. Run `/gastflow` and test a real feature request
