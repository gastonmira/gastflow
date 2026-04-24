"""
Eval cases for the QA Agent.

The QA Agent prompt has a two-step flow:
  STEP 1 — Present a testing PLAN and wait for user approval
  STEP 2 — Execute the plan, then write a final report with a verdict

In a single-turn eval we receive the STEP 1 PLAN output. These rubrics therefore
evaluate the quality of that plan (does it map acceptance criteria to concrete
verification steps? does it acknowledge untestable items? does it describe how
the verdict will be reached?) rather than the final PASS/FAIL verdict, which
only appears after the user approves the plan.
"""

from dataclasses import dataclass


@dataclass
class EvalCase:
    name: str
    context_input: str    # Spec + SE Agent summary
    rubric: str
    threshold: float


SPEC_AND_SE_SUMMARY = """
SPEC:
# Spec: User Authentication API

## Acceptance criteria
- POST /auth/register creates a user and returns 201
- POST /auth/login returns a JWT token on valid credentials
- POST /auth/login returns 401 on invalid credentials
- Passwords are never stored in plain text

---
SE AGENT SUMMARY:
Files created:
- ./src/auth/router.py — FastAPI router with /register and /login endpoints
- ./src/auth/models.py — SQLAlchemy User model
- ./src/auth/schemas.py — Pydantic schemas for request/response
- ./src/auth/service.py — Business logic: password hashing, JWT generation

Implementation notes:
- Used passlib with bcrypt for password hashing (12 rounds)
- JWT tokens expire after 30 minutes
- /register returns 201, /login returns 200 with token
"""

CASES = [
    EvalCase(
        name="plans_to_check_each_acceptance_criterion",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA Agent's testing plan should:
- Reference EACH of the 4 acceptance criteria (register 201, login JWT, login 401, no plain text passwords) and describe how it will verify each one
- Not skip or silently combine criteria
- Reference specific files, endpoints, or data locations when describing the verification approach (e.g. "will inspect ./src/auth/service.py to confirm bcrypt hashing")
- It is acceptable (and expected) that this is a plan rather than a final report — the prompt's STEP 1 produces a plan that the user must approve before STEP 2 executes.""",
        threshold=0.75,
    ),
    EvalCase(
        name="describes_how_verdict_will_be_reached",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA plan must make clear how a final verdict (PASS / FAIL / PASS WITH WARNINGS) will be produced:
- Describe what tools or actions will be used (reading implementation files, running existing tests, starting a dev server, Playwright if there were a UI, etc.)
- Indicate that each acceptance criterion will be checked individually
- Mention the approval/conversation loop OR explicitly ask the user for approval before executing
- It is acceptable that the actual PASS/FAIL labels don't appear yet — they're produced in STEP 2 after approval.""",
        threshold=0.7,
    ),
    EvalCase(
        name="flags_untestable_items_explicitly",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA Agent should:
- Acknowledge when a criterion cannot be fully verified without running the app (e.g. verifying response status codes requires hitting the endpoint)
- Distinguish between "verified by code review" vs "verified by running the app / tests"
- Mention risks, limitations, or items the agent is unsure about
- Not overclaim — avoid asserting something passes purely from file names or the SE summary""",
        threshold=0.7,
    ),
]
