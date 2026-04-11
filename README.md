# gastflow

An agentic software development skill for Claude Code.

Tell it what you want to build. It clarifies, specs, and delegates — SE Agent implements, QA Agent tests, Automation Agent writes tests. All following Spec Driven Development.

## Install

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
| **Orchestrator** | Clarifies requirements, creates spec, delegates | Write, Agent |
| **SE Agent** | Implements the feature | Read, Write, Bash, WebFetch |
| **QA Agent** | Tests the implementation | Read, Bash, Browse |
| **Automation Agent** | Writes automated tests | Read, Write, Bash |

## Requirements

- [Claude Code](https://claude.ai/code) installed
- An Anthropic API key configured in Claude Code

## Uninstall

```bash
rm ~/.claude/skills/gastflow.md
```

## Contributing

The entire product is `skills/gastflow.md`. Edit that file to improve agent behavior,
add new phases, or tune the prompts. PRs welcome.

## License

MIT
