"""
gastflow eval runner — tests agent prompts against defined rubrics.

Usage:
    python evals/run_evals.py

Exit codes:
    0 — all tests passed (score >= threshold for every test case)
    1 — one or more tests failed

Each test case uses Opción A: individual threshold per case.
If ANY single test scores below its threshold, the run fails.
"""

import sys
import os
from pathlib import Path
from dataclasses import dataclass

import anthropic
from rich.console import Console
from rich.table import Table
from rich import box

# Make sure we can import from the project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from evals.parser import extract_agent_prompts
from evals.grader import grade
from evals.cases.orchestrator import CASES as ORCHESTRATOR_CASES
from evals.cases.se_agent import CASES as SE_CASES
from evals.cases.qa_agent import CASES as QA_CASES
from evals.cases.automation_agent import CASES as AUTOMATION_CASES

# Model used to simulate agents in evals (cheaper than production to keep CI fast)
AGENT_MODEL = "claude-haiku-4-5-20251001"

console = Console()


@dataclass
class EvalResult:
    agent: str
    case_name: str
    score: float
    threshold: float
    verdict: str
    passed: bool


def run_agent(system_prompt: str, user_input: str) -> str:
    """
    Simulates an agent responding to a task.
    Uses the same model as production so evals reflect real behavior.
    """
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}],
    )
    return response.content[0].text


def run_eval_suite(agent_name: str, prompt: str, cases: list) -> list[EvalResult]:
    """Runs all test cases for a single agent and returns results."""
    results = []

    for case in cases:
        console.print(f"  [dim]Running:[/dim] {case.name}...", end=" ")

        # Get the agent's response to the test input
        output = run_agent(
            system_prompt=prompt,
            user_input=case.user_input if hasattr(case, "user_input") else case.spec_input if hasattr(case, "spec_input") else case.context_input,
        )

        # Grade the output against the rubric
        score, verdict = grade(output=output, rubric=case.rubric)

        passed = score >= case.threshold
        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        console.print(f"{status} ({score:.2f} / {case.threshold})")

        results.append(EvalResult(
            agent=agent_name,
            case_name=case.name,
            score=score,
            threshold=case.threshold,
            verdict=verdict,
            passed=passed,
        ))

    return results


def print_summary_table(results: list[EvalResult]) -> None:
    """Prints a Rich table with all eval results."""
    table = Table(
        title="gastflow Eval Results",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Test Case", style="white")
    table.add_column("Score", justify="center", style="bold")
    table.add_column("Threshold", justify="center", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Verdict", style="dim")

    for r in results:
        score_color = "green" if r.passed else "red"
        status_icon = "✓ PASS" if r.passed else "✗ FAIL"
        status_style = "bold green" if r.passed else "bold red"

        table.add_row(
            r.agent,
            r.case_name,
            f"[{score_color}]{r.score:.2f}[/{score_color}]",
            f"{r.threshold:.2f}",
            f"[{status_style}]{status_icon}[/{status_style}]",
            r.verdict[:80] + "..." if len(r.verdict) > 80 else r.verdict,
        )

    console.print()
    console.print(table)


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY is not set.[/red]")
        return 1

    # Load prompts directly from gastflow.md
    gastflow_md = Path(__file__).parent.parent / "skills" / "gastflow.md"
    console.print(f"\n[bold]gastflow Evals[/bold] — reading prompts from [cyan]{gastflow_md}[/cyan]\n")

    try:
        prompts = extract_agent_prompts(gastflow_md)
    except ValueError as e:
        console.print(f"[red]Failed to parse gastflow.md: {e}[/red]")
        return 1

    # Run all eval suites
    all_results: list[EvalResult] = []

    suites = [
        ("Orchestrator", prompts["orchestrator"], ORCHESTRATOR_CASES),
        ("SE Agent",     prompts["se"],           SE_CASES),
        ("QA Agent",     prompts["qa"],            QA_CASES),
        ("Automation",   prompts["automation"],    AUTOMATION_CASES),
    ]

    for agent_name, prompt, cases in suites:
        console.rule(f"[bold cyan]{agent_name}[/bold cyan]")
        results = run_eval_suite(agent_name, prompt, cases)
        all_results.extend(results)

    # Print summary
    print_summary_table(all_results)

    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)
    failed = total - passed

    if failed == 0:
        console.print(f"\n[bold green]✓ All {total} tests passed.[/bold green]\n")
        return 0
    else:
        console.print(
            f"\n[bold red]✗ {failed}/{total} tests failed.[/bold red] "
            f"Fix the prompts in [cyan]skills/gastflow.md[/cyan] and re-run.\n"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
