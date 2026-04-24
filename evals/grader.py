"""
LLM-based grader for gastflow prompt evals.

Uses Claude Haiku (cheaper) to evaluate agent outputs against rubrics.
Best practice from Anthropic: use a different model to grade than the one being evaluated.

Grading pattern:
  - Ask Claude to reason in <thinking> tags first (improves accuracy)
  - Extract final verdict from <result> tags
  - Return normalized score 0.0 to 1.0
"""

from __future__ import annotations

import re
import anthropic

# Use Haiku for grading — cheaper and fast enough for evals
GRADER_MODEL = "claude-haiku-4-5-20251001"


def build_grader_prompt(output: str, rubric: str) -> str:
    return f"""You are evaluating the output of an AI agent against a quality rubric.

<rubric>
{rubric}
</rubric>

<agent_output>
{output}
</agent_output>

Think through your evaluation carefully in <thinking> tags, checking each criterion in the rubric.
Then provide a score from 0 to 5 and a one-line verdict in <result> tags.

Format your result exactly like this:
<result>
score: X
verdict: <one sentence explanation>
</result>

Scoring guide:
5 = Perfectly satisfies all rubric criteria
4 = Satisfies most criteria with minor gaps
3 = Partially satisfies criteria, notable gaps
2 = Barely satisfies criteria, significant gaps
1 = Mostly fails the criteria
0 = Completely fails
"""


MAX_GRADER_RETRIES = 2  # total attempts = 1 + MAX_GRADER_RETRIES


def _try_grade_once(client: anthropic.Anthropic, output: str, rubric: str) -> tuple[float, str] | None:
    """Single grader attempt. Returns (score, verdict) on success, None on parse failure."""
    response = client.messages.create(
        model=GRADER_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": build_grader_prompt(output, rubric)}],
    )

    response_text = response.content[0].text

    result_match = re.search(r"<result>(.*?)</result>", response_text, re.DOTALL)
    if not result_match:
        return None

    result_block = result_match.group(1)
    score_match = re.search(r"score:\s*(\d+)", result_block)
    if not score_match:
        return None

    raw_score = int(score_match.group(1))
    normalized = raw_score / 5.0

    verdict_match = re.search(r"verdict:\s*(.+)", result_block)
    verdict = verdict_match.group(1).strip() if verdict_match else "No verdict provided"

    return normalized, verdict


def grade(output: str, rubric: str) -> tuple[float, str]:
    """
    Grades an agent output against a rubric.

    Retries on parse failures so a flaky Haiku response (truncated output,
    malformed tags) doesn't turn into a spurious FAIL with score 0.0. Only
    returns 0.0 after every retry has failed.

    Args:
        output: The agent's response to evaluate
        rubric: Criteria the output should satisfy

    Returns:
        (score, verdict) where score is 0.0-1.0 and verdict is a one-line explanation
    """
    client = anthropic.Anthropic()

    last_error = "Grader failed to produce a result block"
    for attempt in range(1 + MAX_GRADER_RETRIES):
        try:
            result = _try_grade_once(client, output, rubric)
            if result is not None:
                return result
            last_error = f"Grader produced unparseable output (attempt {attempt + 1})"
        except anthropic.APIError as e:
            last_error = f"Grader API error (attempt {attempt + 1}): {e}"

    return 0.0, last_error
