"""
Eval cases for the QA Agent.

Tests:
  1. Acceptance criteria coverage — checks each criterion one by one
  2. Bug reporting quality — clear, reproducible bug reports
  3. Verdict discipline — gives a clear PASS/FAIL/PASS WITH WARNINGS
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
        name="checks_each_acceptance_criterion",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA Agent report should:
- Explicitly check EACH of the 4 acceptance criteria (register 201, login JWT, login 401, no plain text passwords)
- Mark each as ✓ (pass) or ✗ (fail) or ? (could not verify)
- Not skip or combine criteria
- Reference specific files or endpoints when making claims""",
        threshold=0.75,
    ),
    EvalCase(
        name="provides_clear_overall_verdict",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA report must:
- End with a clear overall verdict: PASS, FAIL, or PASS WITH WARNINGS
- Provide a brief justification for the verdict
- If PASS WITH WARNINGS: list the specific warnings
- If FAIL: list the specific failures with reproduction steps""",
        threshold=0.8,
    ),
    EvalCase(
        name="flags_untestable_items_explicitly",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The QA Agent should:
- Acknowledge when a criterion cannot be fully verified without running the app
- Clearly distinguish between "verified by code review" vs "verified by running tests"
- Not claim something passes if it can only be inferred from the code
- Be honest about limitations of static analysis""",
        threshold=0.7,
    ),
]
