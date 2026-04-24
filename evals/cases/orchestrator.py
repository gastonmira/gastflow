"""
Eval cases for the Orchestrator agent.

Tests:
  1. Clarification quality — does it ask smart, targeted questions?
  2. Spec completeness — when it creates a spec, does it cover all required fields?
  3. Scope discipline — does it correctly identify out-of-scope items?
"""

from dataclasses import dataclass


@dataclass
class EvalCase:
    name: str
    user_input: str       # What the user says to the Orchestrator
    rubric: str           # What we expect in the response
    threshold: float      # Minimum score to pass (0.0 - 1.0)


CASES = [
    EvalCase(
        name="asks_clarifying_questions_for_vague_request",
        user_input="I want to build a todo app.",
        rubric="""The response should:
- Ask ONE or TWO specific clarifying questions (not more)
- Ask about tech stack OR target path (not both at once)
- Use friendly, informal but professional tone
- NOT dump a list of 10 questions
- NOT start implementing yet — it's too early""",
        threshold=0.7,
    ),
    EvalCase(
        name="does_not_over_clarify_when_request_is_clear",
        user_input=(
            "Build a REST API with FastAPI and PostgreSQL for user authentication. "
            "It should handle register, login, and logout. Put it in ./src/auth."
        ),
        rubric="""The response should:
- Recognize that the tech stack (FastAPI, PostgreSQL) is already specified
- Recognize the target path (./src/auth) is already specified
- Ask only about missing info: acceptance criteria OR specific requirements
- NOT re-ask about tech stack or target path
- Ask at most 2 questions — 1 targeted question is ideal""",
        threshold=0.6,
    ),
    EvalCase(
        name="spec_covers_all_required_fields",
        user_input=(
            "Build a REST API with FastAPI for user login and registration. "
            "Use PostgreSQL for storage. Target path is ./src/auth. "
            "Requirements: users can register with email+password, login returns a JWT token, "
            "passwords must be hashed. Done when all endpoints return correct status codes."
        ),
        rubric="""When producing the spec (gastflow_spec.md content), it must contain ALL of:
- A clear title
- A description paragraph
- At least 2 functional requirements
- Tech stack listing FastAPI and PostgreSQL
- At least 2 specific acceptance criteria
- A target path of ./src/auth
- Out of scope section (even if empty or with a placeholder)
The spec must be written in markdown format.""",
        threshold=0.8,
    ),
    EvalCase(
        name="handles_ambiguous_tech_stack",
        user_input="I want a simple login page.",
        rubric="""The response should:
- Ask about the tech stack since it's missing — at minimum frontend framework or language (React, Vue, plain HTML, etc.), and ideally also whether a backend is needed
- Keep it to 1-2 questions maximum
- Be friendly and not make the user feel interrogated
- It is acceptable to ask just ONE targeted question as long as it clearly targets missing tech-stack information""",
        threshold=0.6,
    ),
]
