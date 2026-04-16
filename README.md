# gastflow

An agentic software development skill for Claude Code.

Tell it what you want to build. It clarifies, specs, and delegates — SE Agent implements, QA Agent tests, Automation Agent writes tests. All following Spec Driven Development.

Don't know what to build? Run `/gastflow-product` — the Product Agent scans your project and proposes a backlog of feature ideas.

## Install

One-liner (no clone needed):

```bash
curl -fsSL https://raw.githubusercontent.com/gastonmira/gastflow/main/install.sh | bash
```

Or clone and install:

```bash
git clone https://github.com/gastonmira/gastflow
cd gastflow
./install.sh
```

## Usage

Open any project in Claude Code and run:

```
/gastflow
```

The Orchestrator will chat with you, understand what you want to build, and kick off the agent pipeline.

## How it works

```
(optional) /gastflow-product → Product Agent → gastflow_backlog.md
                                                      ↓
You → /gastflow (Orchestrator)
         ↓
   Clarify requirements
         ↓
   Write gastflow_spec.md
         ↓
   SE Agent → implements the feature
         ↓
   QA Agent ──────── Automation Agent
   (tests)           (writes tests)
         ↓
   Summary presented to you
```

All agents run inside Claude Code using the built-in tools (Read, Write, Bash, Browse, etc.)
No API keys to manage. No Python environment to set up.

## What each agent does

| Agent | Job | Tools it uses |
|-------|-----|---------------|
| **Product Agent** | Scans the project, proposes a feature backlog | Read, Glob, Grep, Write |
| **Orchestrator** | Clarifies requirements, creates spec, delegates | Write, Agent |
| **SE Agent** | Implements the feature | Read, Write, Bash, WebFetch |
| **QA Agent** | Tests the implementation | Read, Bash, Browse |
| **Automation Agent** | Writes automated tests | Read, Write, Bash |

## Requirements

- [Claude Code](https://claude.ai/code) installed
- An Anthropic API key configured in Claude Code

## Uninstall

```bash
rm -rf ~/.claude/skills/gastflow ~/.claude/skills/gastflow-product ~/.claude/skills/gastflow-se ~/.claude/skills/gastflow-qa ~/.claude/skills/gastflow-automation
```

## Contributing

The entire product is `skills/gastflow.md`. Edit that file to improve agent behavior,
add new phases, or tune the prompts. PRs welcome.

## License

MIT
