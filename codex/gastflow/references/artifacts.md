# gastflow Artifacts

Use this reference when creating or updating gastflow files in Codex.

## Template

Read `assets/template.html` from this skill before rendering HTML. Copy the full `<head>` into every generated artifact, set `<body data-artifact="...">`, and keep artifacts self-contained with inline CSS and no external JavaScript.

Use these artifact values:

- `spec`
- `state`
- `backlog`
- `plan`

Every generated HTML artifact must be `lang="en"` and end with:

```html
<script type="application/json" id="gastflow-data" src="./<name>.json"></script>
```

## Spec JSON

Feature specs:

```json
{
  "title": "...",
  "type": "feature",
  "description": "...",
  "tech_stack": ["..."],
  "target_path": "...",
  "requirements": ["..."],
  "acceptance_criteria": ["..."],
  "out_of_scope": ["..."]
}
```

Bug fix specs:

```json
{
  "title": "...",
  "type": "bugfix",
  "description": "...",
  "tech_stack": ["..."],
  "target_path": "...",
  "reproduction_steps": ["..."],
  "expected": "...",
  "actual": "...",
  "suspected_files": ["..."],
  "out_of_scope": ["..."]
}
```

## State JSON

Initial shape:

```json
{
  "feature_name": "...",
  "type": "feature",
  "branch": "...",
  "merge_strategy": "pr",
  "base_branch": "main",
  "status": "running",
  "agents": {
    "se": { "status": "pending" },
    "qa": { "status": "pending" },
    "automation": { "status": "pending" }
  }
}
```

For bug fixes, use `type: "bugfix"` and replace `agents.se` with `agents.bugfix`. Keep the JSON tight; do not include the unused implementation role.

## Spec HTML

Render `gastflow_spec.html` from `gastflow_spec.json`:

- hero with title, type badge, target path, branch placeholder, and date
- requirements and acceptance criteria as cards or lists for features
- reproduction steps as an ordered list for bug fixes
- expected and actual behavior side by side for bug fixes
- out of scope section

Ask before adding diagrams. Use the diagram patterns documented in `assets/template.html`.

## Plan HTML

Render `gastflow_plan.html` before implementation:

- hero with title, type badge, summary, branch, target path, and date
- file structure using `.file-list`
- design decisions as `.card`s with a clear "why"
- libraries and patterns using `.kvs`
- code previews for important new files using `.code`
- diffs for every modified file using `.diff`
- risks or open questions using `.callout-warn`

Do not implement until the user explicitly approves this plan.

## State HTML

Render `gastflow_state.html` from `gastflow_state.json` after every role:

- timeline with Spec, Implementation, QA, and Automation
- branch, merge strategy, and base branch using `.kvs`
- run-level stats using `.stat-icon` by default and `.stat-bar` only when comparing value vs target
- artifact navigator listing existing gastflow artifacts
- explanation that JSON sidecars are canonical and the user can ask the agent to edit artifacts conversationally

When complete, show all timeline steps as done and include the final QA verdict, files changed, tests written, run commands, manual QA steps, and residual risks.

## Backlog JSON

```json
{
  "context": "...",
  "quick_wins": [
    { "title": "...", "what": "...", "why": "...", "effort": "S", "signals": "..." }
  ],
  "core_bets": [],
  "wild_cards": [],
  "recommended_next": { "title": "...", "why": "..." }
}
```

## Backlog HTML

Render `gastflow_backlog.html` with:

- hero with "Product Backlog", date, context, and recommended next callout
- three sections: Quick wins, Core bets, Wild cards
- comparable cards with title, effort badge, what, why, and signals

Show ideas in chat first; persisted backlog files are for handoff and sharing.
