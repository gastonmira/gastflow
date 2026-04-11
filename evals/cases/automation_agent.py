"""
Eval cases for the Automation Agent.

Tests:
  1. Test coverage — at least one test per acceptance criterion
  2. Test naming conventions — follows the defined conventions
  3. Test quality — tests are meaningful, not trivial
  4. No implementation code — only writes test files
"""

from dataclasses import dataclass


@dataclass
class EvalCase:
    name: str
    context_input: str
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

## Tech stack
- Python, FastAPI, pytest

## Target path
./src/auth

---
SE AGENT SUMMARY:
Files created:
- ./src/auth/router.py — FastAPI router with /register and /login endpoints
- ./src/auth/models.py — SQLAlchemy User model
- ./src/auth/schemas.py — Pydantic schemas
- ./src/auth/service.py — password hashing, JWT generation
"""

CASES = [
    EvalCase(
        name="covers_all_acceptance_criteria",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""The Automation Agent should write tests that cover ALL 4 acceptance criteria:
- A test for POST /auth/register returning 201
- A test for POST /auth/login returning a JWT token
- A test for POST /auth/login returning 401 for wrong credentials
- A test that verifies passwords are hashed (not plain text in DB)
Each criterion must have at least one corresponding test case.""",
        threshold=0.8,
    ),
    EvalCase(
        name="follows_naming_conventions",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""Test files must follow these naming conventions:
- Unit tests: tests/unit/test_<module>.py
- Integration tests: tests/integration/test_<feature>.py
- E2E tests: tests/e2e/test_<feature>.spec.py
The agent should choose the appropriate type for each test.
For a FastAPI endpoint, integration tests are most appropriate.""",
        threshold=0.75,
    ),
    EvalCase(
        name="writes_meaningful_not_trivial_tests",
        context_input=SPEC_AND_SE_SUMMARY,
        rubric="""Tests must be meaningful:
- Test functions should have clear names describing what they test (e.g., test_login_returns_401_for_wrong_password)
- Tests should include assertions (assert statements)
- Tests should cover at least one edge case (e.g., duplicate email on register, empty password)
- Tests should NOT just check that a function exists or that it returns a non-None value
- At least one test should verify error behavior, not just happy path""",
        threshold=0.75,
    ),
]
