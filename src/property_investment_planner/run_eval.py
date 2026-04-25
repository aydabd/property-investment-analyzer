"""Eval runner - checks quality of agent outputs on a PR.

Invoked by .github/workflows/eval.yml when a PR with analysis is opened.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import click
from loguru import logger

if TYPE_CHECKING:
    from anthropic import Anthropic

from property_investment_planner.constants import Settings, load_settings


def _resolve_issue_number(pr_number: int) -> int | None:
    """Try to extract issue number from the PR branch name.

    Branch naming convention: analysis/issue-<N>-<timestamp>.
    Falls back to pr_number if branch name unavailable.
    """
    try:
        import subprocess

        gh = shutil.which("gh")
        if gh is None:
            raise FileNotFoundError("gh")

        result = subprocess.run(
            [gh, "pr", "view", str(pr_number), "--json", "headRefName", "-q", ".headRefName"],
            capture_output=True,
            text=True,
            check=True,
        )  # noqa: S603 - safe since we control the input and it's not shell=True
        match = re.search(r"issue-(\d+)", result.stdout.strip())
        if match:
            return int(match.group(1))
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.debug("Could not resolve issue number from branch name")
    return None


def load_pr_analysis(pr_number: int, settings: Settings) -> dict[str, str]:
    """Load agent outputs from the PR's analyses folder.

    Resolves the actual issue number from the PR branch name since
    PR numbers and issue numbers are different. Falls back to pr_number
    if branch name resolution fails.
    """
    analyses_dir = Path("analyses")
    if not analyses_dir.exists():
        logger.error("No analyses directory found")
        return {}

    # Resolve issue number from PR branch (analysis/issue-<N>-...)
    issue_number = _resolve_issue_number(pr_number) or pr_number
    target_folder = analyses_dir / f"issue-{issue_number}"

    if target_folder.is_dir():
        logger.info(f"Found analysis folder: {target_folder}")
    else:
        logger.warning(
            f"No folder for issue-{issue_number}, scanning for matching analysis folders"
        )
        # Restrict fallback to issue-<N> pattern only
        candidates = [
            f
            for f in sorted(analyses_dir.iterdir())
            if f.is_dir() and re.match(r"^issue-\d+$", f.name)
        ]
        if len(candidates) == 1:
            target_folder = candidates[0]
            logger.warning(f"Using only available folder: {target_folder}")
        elif len(candidates) > 1:
            logger.error(
                f"Multiple analysis folders found: {[c.name for c in candidates]}. "
                "Cannot determine which belongs to this PR."
            )
            return {}
        else:
            return {}

    outputs: dict[str, str] = {}
    agent_outputs_dir = target_folder / "agent-outputs"
    if agent_outputs_dir.exists():
        for md_file in agent_outputs_dir.glob("*.md"):
            outputs[md_file.stem] = md_file.read_text(encoding="utf-8")
    final_report = target_folder / "final-report.md"
    if final_report.exists():
        outputs["final-report"] = final_report.read_text(encoding="utf-8")

    return outputs


def run_eval(
    outputs: dict[str, str],
    client: Anthropic,
    settings: Settings,
) -> str:
    """Execute eval agent against all agent outputs."""
    eval_prompt = (settings.agents_dir / "99-eval.md").read_text(encoding="utf-8")

    # Build context with all agent outputs
    context_parts = ["# Agent Outputs to Evaluate\n"]
    for agent_name, output in outputs.items():
        context_parts.append(f"\n## {agent_name}\n\n{output[:5000]}\n")
        # Truncate very long outputs to keep eval focused

    context_parts.append(
        "\n---\n\nUtvärdera enligt din instruktion."
        " Ge konkret, handlingsbar feedback. Svara på svenska."
    )

    response = client.messages.create(
        model=settings.claude_model_fast,  # Haiku is enough for eval
        max_tokens=4000,
        system=eval_prompt,
        messages=[{"role": "user", "content": "\n".join(context_parts)}],
    )

    return "".join(block.text for block in response.content if hasattr(block, "text"))


@click.command()
@click.option("--pr", type=int, required=True)
def main(pr: int) -> None:
    """Run eval agent against agent outputs in a PR."""
    settings = load_settings()
    logger.info(f"Running eval for PR #{pr}")

    outputs = load_pr_analysis(pr, settings)
    if not outputs:
        logger.warning("No agent outputs found in PR")
        eval_result = (
            "## 🔍 Eval\n\nIngen agent-output hittades i PR:en."
            " Verifiera att `analyses/issue-X/agent-outputs/` finns."
        )
    else:
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.anthropic_api_key)
        eval_result = run_eval(outputs, client, settings)

    settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    result_path = settings.outputs_dir / "eval-result.md"
    result_path.write_text(eval_result, encoding="utf-8")
    logger.info(f"Eval result written: {result_path}")


if __name__ == "__main__":
    main()
