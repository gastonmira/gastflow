---
name: gastflow
description: Spec-driven agentic software development workflow compatible with Codex. Use when the user wants Codex to clarify requirements, create HTML/JSON specs, plan implementation, implement features or bug fixes, run QA, write automated tests, and produce a final gastflow report.
---

# gastflow

Use gastflow to run a conversational Spec Driven Development workflow in Codex:

1. clarify the request
2. write an approved spec
3. plan implementation before editing code
4. implement the approved plan
5. verify behavior through QA
6. add automated tests
7. write the final report and archive the session

Keep gastflow compatible with Claude Code's artifact model, but follow Codex's tools, approval flow, and sandbox rules.

## Bundled Resources

- Read `assets/template.html` before rendering any HTML artifact.
- Read `references/artifacts.md` when creating or updating `gastflow_spec`, `gastflow_state`, `gastflow_plan`, or `gastflow_backlog`.
- Read `references/agents.md` when running the Product, SE, Bug Fix, QA, or Automation roles.

## Core Rules

- Produce human-facing artifacts as self-contained HTML plus canonical JSON sidecars.
- Keep `.gastflow/memory.md` as Markdown; it is agent-only context.
- Ask only 1-2 clarifying questions at a time.
- Do not start implementation until the user explicitly approves the spec and implementation plan.
- Use Codex-native file and shell tools. Prefer `rg` for search, use `apply_patch` for manual edits, and run project-native verification commands.
- Do not refer to Claude-only tools such as `Skill(...)`, `Read`, `Write`, `Glob`, or `Grep` while executing in Codex.
- Run the roles sequentially in the current Codex session by default. Only use Codex subagents if the user explicitly asks for delegated or parallel agent work.

## Workflow

### Phase 0 - Memory

Check whether `.gastflow/memory.md` exists in the target project. If it exists, read it, briefly summarize remembered stack, recent work, and preferences, then ask whether it is still accurate.

### Phase 1 - Clarify

If the user does not have a feature in mind, offer to run the Product role from `references/agents.md` to generate a backlog.

Classify the request silently:

- `feature`: new functionality, requirements, acceptance criteria, build/create/add/implement language.
- `bugfix`: broken behavior, error, failing test, regression, expected vs actual behavior.

For features, gather what it does, target path, stack, requirements, and acceptance criteria. For bug fixes, gather reproduction steps, expected behavior, actual behavior, relevant logs, and suspected files. Skip anything already provided or available from memory.

### Phase 2 - Spec and Pipeline Setup

Read `references/artifacts.md`, then write:

- `gastflow_spec.json`
- `gastflow_spec.html`

Render HTML with `assets/template.html`. Show the spec to the user and loop on changes until they explicitly approve. Ask whether to use the current branch or create a new branch, then ask for the merge strategy.

After approval, write:

- `gastflow_state.json`
- `gastflow_state.html`

### Phase 3 - Implementation, QA, and Automation

Run exactly one implementation role:

- Use the SE role for `type: "feature"`.
- Use the Bug Fix role for `type: "bugfix"`.

After implementation, run QA and then Automation. Each role reads the JSON sidecars, updates `gastflow_state.json`, and re-renders `gastflow_state.html`.

### Phase 4 - Final Report and Archive

Read `gastflow_state.json`, summarize what changed, QA verdict, tests written, commands run, manual QA steps, and residual risks. Set the root `status` to `"done"` when the pipeline is complete and re-render `gastflow_state.html`.

When the user is satisfied, follow the selected merge strategy if they want a commit/PR. Archive artifacts to:

```bash
.gastflow/history/<spec-title-kebab>_<YYYY-MM-DD>
```

Update `.gastflow/memory.md` with the date, title, branch, PR number if any, stack, preferences, and useful notes.
