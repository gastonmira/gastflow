"""
Eval cases for the SE Agent.

The SE Agent prompt has a two-step flow:
  STEP 1 — Present an implementation PLAN and wait for user approval
  STEP 2 — Execute the plan, then update gastflow_state.md with a handoff summary

In a single-turn eval we receive the STEP 1 PLAN. These rubrics evaluate the
quality of that plan (does it cover all requirements? does it list the files
it will create? does it correctly scope tests OUT?) rather than the final
implementation or the end-of-task handoff summary.
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
        name="plan_addresses_all_requirements",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""The SE Agent's implementation plan should:
- Mention a register endpoint (POST /auth/register)
- Mention a login endpoint (POST /auth/login)
- Mention password hashing (bcrypt or passlib)
- Mention JWT token generation
- List the files it will create (file structure)
It is acceptable (and expected) that this is a plan, not executed code — the prompt's STEP 1 produces a plan that the user must approve before STEP 2 implements anything.""",
        threshold=0.75,
    ),
    EvalCase(
        name="plan_is_detailed_enough_for_handoff",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""The plan should be detailed enough that a reviewer can evaluate it before approval:
- List each file it will create with a brief description of what goes in it
- Mention at least one design decision with a WHY (e.g. "JWT expiry 30min because...", "bcrypt with 12 rounds because...")
- Mention any risks, open questions, or things the user should watch for
- Reference libraries and patterns it will use
It does NOT need to include the end-of-task handoff summary that appears in gastflow_state.md — that happens after STEP 2 executes.""",
        threshold=0.7,
    ),
    EvalCase(
        name="plan_keeps_tests_out_of_scope",
        spec_input=FASTAPI_AUTH_SPEC,
        rubric="""In the implementation plan, the SE Agent must treat tests as out of scope:
- Does NOT propose creating test files (test_*.py)
- Does NOT propose creating a tests/ directory
- Does NOT include pytest, unittest, or similar testing imports in the file list
- It is acceptable (and a plus) to explicitly note that tests are the Automation Agent's responsibility.
The focus of the plan must be implementation code only.""",
        threshold=0.75,
    ),
]
