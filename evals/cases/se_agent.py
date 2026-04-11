"""
Eval cases for the SE Agent.

Tests:
  1. Implementation coverage — does it address all requirements?
  2. Code quality — does it write idiomatic, clean code?
  3. No tests — does it correctly leave tests to the Automation Agent?
  4. Summary quality — does it provide a clear handoff summary?
"""

from dataclasses import dataclass


@dataclass
class EvalCase:
    name: str
    spec_input: str       # The spec the SE Agent receives
    rubric: str
    threshold: float


FASTAPI_AUTH_SPEC = """
# Spec: User Authentication API

## Description
A REST API for user registration and login using FastAPI and PostgreSQL.

## Requirements
- Users can register with email and password
- Passwords must be hashed before storage (use bcrypt)
- Login endpoint returns a JWT token on success
- Return 401 for invalid credentials

## Tech stack
- Python, FastAPI, PostgreSQL, SQLAlchemy, python-jose (JWT), passlib (bcrypt)

## Acceptance criteria
- POST /auth/register creates a user and returns 201
- POST /auth/login returns a JWT token on valid credentials
- POST /auth/login returns 401 on invalid credentials
- Passwords are never stored in plain text

## Out of scope
- Password reset flow
- OAuth / social login

## Target path
./src/auth
"""

CASES = [
    EvalCase(
        name="addresses_all_requirements",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""The SE Agent's response should:
- Mention creating a register endpoint (POST /auth/register)
- Mention creating a login endpoint (POST /auth/login)
- Mention password hashing (bcrypt or passlib)
- Mention JWT token generation
- List the files it created or plans to create
- NOT write any test files (that's the Automation Agent's job)""",
        threshold=0.75,
    ),
    EvalCase(
        name="provides_clear_handoff_summary",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""The summary at the end should:
- List each file created with a brief description of what it does
- Mention at least one implementation decision made (e.g., JWT expiry, bcrypt rounds)
- Point out something specific for the QA Agent to check
- Be clear enough that another agent can pick up from here without reading the code""",
        threshold=0.75,
    ),
    EvalCase(
        name="does_not_write_tests",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""The SE Agent must NOT:
- Write test files (test_*.py files)
- Create a tests/ directory
- Include pytest or unittest imports in any file
Tests are the Automation Agent's responsibility.
The SE Agent SHOULD write the implementation code only.""",
        threshold=0.8,
    ),
]
