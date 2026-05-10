# gastflow Roles for Codex

Use these role instructions inside the single Codex `gastflow` skill. Run roles sequentially unless the user explicitly asks for delegated or parallel work.

## Product Role

Use when the user wants ideas, a backlog, or does not know what to build.

1. Scan the project with `rg --files`, README files, package manifests, routes, commands, and recent `.gastflow` history.
2. Ask 1-2 questions about target user, current goal, and constraints when the code does not answer them.
3. Propose 8-12 ideas grouped as Quick wins, Core bets, and Wild cards.
4. For each idea include title, what, why, effort `S|M|L`, and signals to watch.
5. Show the backlog in chat first.
6. If the user chooses an idea or wants the backlog saved, write `gastflow_backlog.json` and `gastflow_backlog.html`.

Avoid generic SaaS checklist ideas unless the codebase shows they unlock real value.

## SE Role

Use for `type: "feature"`.

1. Read `gastflow_spec.json`, `gastflow_state.json`, and `assets/template.html`.
2. Review current code before planning. Prefer existing patterns and project-native libraries.
3. If up-to-date docs are needed, use available documentation tools or official sources. If unavailable, proceed with current knowledge and state the limitation.
4. Write `gastflow_plan.html` before editing code.
5. Ask whether the user wants a diagram for non-trivial flows.
6. Wait for explicit plan approval.
7. Implement only the approved plan.
8. Run relevant verification commands.
9. Update `agents.se` in `gastflow_state.json`:

```json
{
  "status": "completed",
  "files_created": [
    { "path": "...", "description": "..." }
  ],
  "files_modified": [
    { "path": "...", "description": "..." }
  ],
  "summary": "...",
  "decisions": [
    { "decision": "...", "why": "..." }
  ],
  "notes_for_qa": "..."
}
```

Then re-render `gastflow_state.html`.

Do not write tests in this role; Automation owns tests.

## Bug Fix Role

Use for `type: "bugfix"`.

1. Read `gastflow_spec.json`, `gastflow_state.json`, and `assets/template.html`.
2. Make sure reproduction steps, expected behavior, and actual behavior are clear enough to investigate. Ask concise follow-up questions if needed.
3. Trace from symptom to root cause using search, file reads, tests, logs, and relevant git history.
4. Form a root cause that explains why the wrong behavior happens.
5. Write `gastflow_plan.html` with root cause, call path, exact proposed diffs, and risks.
6. Ask whether the user wants a diagram for non-trivial bugs.
7. Wait for explicit approval.
8. Apply the minimal fix only.
9. Run relevant verification commands.
10. Update `agents.bugfix` in `gastflow_state.json`:

```json
{
  "status": "completed",
  "root_cause": "...",
  "files_modified": [
    { "path": "...", "description": "..." }
  ],
  "fix_summary": "...",
  "repro_steps": ["..."],
  "notes_for_qa": "Confirm the bug no longer reproduces.",
  "notes_for_automation": "Write a regression test encoding the repro steps."
}
```

Then re-render `gastflow_state.html`.

## QA Role

Use after implementation.

1. Read the spec, state, implementation files, and template.
2. Present a testing plan in chat before running tests.
3. For features, map every acceptance criterion to a concrete verification step.
4. For bug fixes, verify the bug no longer reproduces.
5. Identify which files to inspect, which commands to run, whether a dev server is needed, and whether browser testing is appropriate.
6. Wait for explicit approval before executing the QA plan.
7. Run checks and avoid overclaiming; distinguish code review from executed verification.
8. Update `agents.qa` in `gastflow_state.json`:

```json
{
  "status": "completed",
  "criteria_results": [
    { "criterion": "...", "result": "pass", "note": "..." }
  ],
  "bugs": [],
  "verdict": "PASS",
  "verdict_reason": "..."
}
```

Use `PASS`, `FAIL`, or `WARN`, then re-render `gastflow_state.html`.

## Automation Role

Use after QA.

1. Read the spec, state, implementation files, and existing tests.
2. Present a test-writing plan in chat.
3. For features, map each acceptance criterion to at least one automated test.
4. For bug fixes, prioritize one regression test that encodes the reproduction steps.
5. Wait for explicit approval before writing test files.
6. Add tests using the project's existing framework and conventions.
7. Run test discovery or the focused test command.
8. Update `agents.automation` in `gastflow_state.json`:

```json
{
  "status": "completed",
  "test_files": [
    { "path": "...", "test_count": 1, "covers": "..." }
  ],
  "total_tests": 1,
  "coverage_notes": "..."
}
```

For bug fixes, add `"regression_test": "<path>"`. Then re-render `gastflow_state.html`.
