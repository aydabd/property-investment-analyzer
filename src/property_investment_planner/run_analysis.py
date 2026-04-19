"""Main runner that orchestrates agents to produce an investment analysis.

Invoked by GitHub Actions when a new issue is created or /rerun is commented.

Flow:
    1. Parse issue into structured data
    2. Run orchestrator to decide which agents to run
    3. Execute agents in order, passing context between them
    4. If agents have questions, comment on issue and exit
    5. Assemble final report
    6. Write outputs for PR creation
"""

from __future__ import annotations

import json
import re
import sys
from typing import TYPE_CHECKING, Any

import click
from loguru import logger

if TYPE_CHECKING:
    from anthropic import Anthropic
    from github import Github

from property_investment_planner.constants import (
    AGENT_EXECUTION_ORDER,
    DEFAULT_ASSUMPTIONS,
    ISSUE_FIELD_MAPPING,
    REQUIRED_ISSUE_FIELDS,
    Settings,
    load_settings,
)


def configure_logging(settings: Settings) -> None:
    """Set up loguru with the configured log level."""
    logger.remove()
    logger.add(sys.stderr, level=settings.log_level)


def parse_issue_body(body: str) -> dict[str, Any]:
    """Extract field values from GitHub issue form submission.

    Issue forms render as markdown with ### headers for field labels.
    """
    fields: dict[str, Any] = {}
    current_field: str | None = None
    current_value: list[str] = []

    for line in body.splitlines():
        if line.startswith("### "):
            # Save previous field
            if current_field:
                normalized = ISSUE_FIELD_MAPPING.get(current_field, current_field)
                fields[normalized] = "\n".join(current_value).strip()

            current_field = line.removeprefix("### ").strip()
            current_value = []
        elif current_field:
            current_value.append(line)

    # Save last field
    if current_field:
        normalized = ISSUE_FIELD_MAPPING.get(current_field, current_field)
        fields[normalized] = "\n".join(current_value).strip()

    # Clean up empty "_No response_" placeholders
    return {k: v for k, v in fields.items() if v and v != "_No response_"}


def validate_issue_data(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Check that required fields are present.

    Returns:
        (is_valid, missing_fields)
    """
    missing = [f for f in REQUIRED_ISSUE_FIELDS if f not in data or not data[f]]
    return len(missing) == 0, missing


def load_agent_prompt(agent_name: str, settings: Settings) -> str:
    """Read the agent's markdown definition as its system prompt."""
    path = settings.agents_dir / f"{agent_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Agent definition not found: {path}")
    return path.read_text(encoding="utf-8")


def load_skill(skill_name: str, settings: Settings) -> str:
    """Load a skill markdown file for inclusion in agent context."""
    path = settings.skills_dir / f"{skill_name}.md"
    if not path.exists():
        logger.warning(f"Skill not found: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def build_agent_context(
    agent_name: str,
    issue_data: dict[str, Any],
    previous_outputs: dict[str, str],
    settings: Settings,
) -> str:
    """Construct the full context to send to an agent.

    Includes:
        - Issue data
        - Relevant skills
        - Previous agents' outputs
        - Default assumptions
    """
    context_parts = [
        "# Analysis Context\n",
        "## Issue Data\n```yaml\n" + _dict_to_yaml(issue_data) + "\n```\n",
    ]

    # Include default assumptions
    context_parts.append(
        "## Default Assumptions (use if user hasn't specified)\n```yaml\n"
        + _dict_to_yaml(DEFAULT_ASSUMPTIONS)
        + "\n```\n"
    )

    # Include relevant skill
    data_sources = load_skill("data-sources", settings)
    if data_sources:
        context_parts.append(f"## Skill: Data Sources\n{data_sources}\n")

    # Include previous agents' outputs (agents reference each other)
    if previous_outputs:
        context_parts.append("## Previous Agents' Outputs\n")
        for prev_agent, prev_output in previous_outputs.items():
            context_parts.append(f"### {prev_agent}\n{prev_output}\n")

    # Agent-specific instruction
    context_parts.append(
        f"\n---\n\nDu kör nu som {agent_name}. Följ instruktionerna i din "
        f"systemprompt. Leverera output i det format som beskrivs där. "
        f"Var generisk – hårdkoda INGA kommuner eller platser."
    )

    return "\n".join(context_parts)


def _dict_to_yaml(d: dict[str, Any]) -> str:
    """Convert dict to YAML string using safe_dump."""
    import yaml

    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True, default_flow_style=False).rstrip()


def run_agent(
    agent_name: str,
    issue_data: dict[str, Any],
    previous_outputs: dict[str, str],
    client: Anthropic,
    settings: Settings,
) -> str:
    """Execute one agent and return its output."""
    logger.info(f"Running agent: {agent_name}")

    system_prompt = load_agent_prompt(agent_name, settings)
    context = build_agent_context(agent_name, issue_data, previous_outputs, settings)

    response = client.messages.create(
        model=settings.claude_model,
        max_tokens=settings.max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": context}],
    )

    # Extract text from response
    output_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            output_text += block.text

    # Save agent output to disk
    settings.agent_outputs_dir.mkdir(parents=True, exist_ok=True)
    output_path = settings.agent_outputs_dir / f"{agent_name}.md"
    output_path.write_text(output_text, encoding="utf-8")

    logger.info(f"Agent {agent_name} finished ({len(output_text)} chars)")
    return output_text


def detect_agent_questions(output: str) -> list[str]:
    """Extract any questions an agent asked the user.

    Agents signal questions via markdown headers like:
        ## [Agent Name]: frågor
    """
    questions = []
    in_question_section = False
    current_block: list[str] = []

    for line in output.splitlines():
        if re.match(r"^##\s+.+?:\s*fråg(?:or|a)?\s*$", line, re.IGNORECASE):
            # Save previous block if we were already collecting
            if in_question_section and current_block:
                questions.append("\n".join(current_block).strip())
                current_block = []
            in_question_section = True
            continue

        if in_question_section:
            if line.startswith("## "):
                # New section, stop collecting
                if current_block:
                    questions.append("\n".join(current_block).strip())
                    current_block = []
                in_question_section = False
                continue
            current_block.append(line)

    if in_question_section and current_block:
        questions.append("\n".join(current_block).strip())

    return questions


def comment_questions_on_issue(
    gh: Github,
    repo_name: str,
    issue_number: int,
    agent_name: str,
    questions: list[str],
) -> None:
    """Post agent questions as issue comment."""
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(issue_number)

    body = f"## 🤖 {agent_name} behöver mer information\n\n"
    body += "\n\n".join(questions)
    body += (
        "\n\n---\n"
        "*Svara genom att kommentera nedan eller redigera issue. "
        "Kommentera `/rerun all` när du är klar så fortsätter analysen.*"
    )

    issue.create_comment(body)
    logger.info(f"Posted questions from {agent_name} to issue #{issue_number}")


def assemble_final_report(
    issue_data: dict[str, Any],
    agent_outputs: dict[str, str],
    settings: Settings,
) -> str:
    """Combine agent outputs into final-report.md."""
    template_path = settings.templates_dir / "report-template.md"
    if not template_path.exists():
        logger.warning("Report template missing, using fallback")
        return _fallback_report(issue_data, agent_outputs)

    template = template_path.read_text(encoding="utf-8")

    # Simple substitution - agents' outputs get inserted at placeholders
    report = template

    # Handle conditional blocks: {{#if agent:NAME}}...{{else}}...{{/if}}
    import re as _re

    def _replace_conditional(match: _re.Match[str]) -> str:
        agent_key = match.group(1)
        if_content = match.group(2)
        else_content = match.group(3) if match.group(3) else ""
        if agent_key in agent_outputs and agent_outputs[agent_key]:
            return if_content.strip()
        return else_content.strip()

    report = _re.sub(
        r"\{\{#if agent:(.+?)\}\}\n?(.*?)\{\{else\}\}\n?(.*?)\{\{/if\}\}",
        _replace_conditional,
        report,
        flags=_re.DOTALL,
    )

    for agent_name, output in agent_outputs.items():
        placeholder = f"{{{{agent:{agent_name}}}}}"
        if placeholder in report:
            report = report.replace(placeholder, output)

    # Substitute issue data fields
    for key, value in issue_data.items():
        placeholder = f"{{{{issue:{key}}}}}"
        report = report.replace(placeholder, str(value))

    # Substitute meta fields
    from datetime import UTC, datetime

    meta: dict[str, str] = {
        "date": datetime.now(tz=UTC).strftime("%Y-%m-%d"),
        "issue_number": str(issue_data.get("_issue_number", "?")),
    }
    for key, value in meta.items():
        report = report.replace(f"{{{{meta:{key}}}}}", value)

    return report


def _fallback_report(
    issue_data: dict[str, Any],
    agent_outputs: dict[str, str],
) -> str:
    """Simple fallback report if template is missing."""
    parts = ["# Investment Analysis Report\n"]
    parts.append("## Issue Data\n```yaml\n" + _dict_to_yaml(issue_data) + "\n```\n")
    for agent_name, output in agent_outputs.items():
        parts.append(f"\n## {agent_name}\n\n{output}\n")
    return "\n".join(parts)


def decide_agents_to_run(
    requested: str,
    issue_data: dict[str, Any],
) -> list[str]:
    """Return list of agent names to execute based on user request and context."""
    if requested == "all":
        agents = AGENT_EXECUTION_ORDER.copy()
        # Eval runs separately via eval.yml; orchestrator validation is in Python
        agents = [a for a in agents if a not in {"99-eval", "00-orchestrator"}]
        # Skip partnership agent if not a partnership
        if issue_data.get("partnerskap", "").startswith("Nej"):
            agents = [a for a in agents if a != "06-partnership"]
        return agents

    # Specific agent requested via /rerun
    if requested in AGENT_EXECUTION_ORDER:
        return [requested]

    logger.warning(f"Unknown agents request: {requested}")
    return []


@click.command()
@click.option("--issue-number", type=int, required=True)
@click.option("--repo", type=str, required=True)
@click.option("--agents", type=str, default="all")
def main(issue_number: int, repo: str, agents: str) -> None:
    """Run investment analysis for a GitHub issue.

    This is the standalone Python runner (requires ANTHROPIC_API_KEY).
    The primary execution path uses Copilot Coding Agent instead.
    """
    settings = load_settings()
    configure_logging(settings)

    if not settings.anthropic_api_key:
        logger.error(
            "ANTHROPIC_API_KEY not set. This runner requires the Anthropic API. "
            "For the default flow, assign @copilot to the issue instead."
        )
        sys.exit(1)

    logger.info(f"Starting analysis for issue #{issue_number} in {repo}")

    from anthropic import Anthropic
    from github import Github

    gh = Github(settings.github_token)
    client = Anthropic(api_key=settings.anthropic_api_key)

    # Fetch issue
    issue = gh.get_repo(repo).get_issue(issue_number)
    issue_data = parse_issue_body(issue.body or "")
    logger.info(f"Parsed {len(issue_data)} fields from issue")

    # Validate
    is_valid, missing = validate_issue_data(issue_data)
    if not is_valid:
        msg = (
            f"❌ Issue saknar obligatoriska fält: {', '.join(missing)}."
            " Redigera issue och kommentera `/rerun all`."
        )
        issue.create_comment(msg)
        sys.exit(1)

    # Decide which agents to run
    agent_list = decide_agents_to_run(agents, issue_data)
    if not agent_list:
        issue.create_comment(
            f"❌ Okänd agent: `{agents}`. Använd `/rerun all` eller `/rerun <agent-namn>`."
        )
        sys.exit(1)
    logger.info(f"Will run agents: {agent_list}")

    # Execute agents sequentially, passing previous outputs
    agent_outputs: dict[str, str] = {}
    for agent_name in agent_list:
        try:
            output = run_agent(
                agent_name=agent_name,
                issue_data=issue_data,
                previous_outputs=agent_outputs,
                client=client,
                settings=settings,
            )
            agent_outputs[agent_name] = output

            # Check if agent asked questions
            questions = detect_agent_questions(output)
            if questions:
                comment_questions_on_issue(gh, repo, issue_number, agent_name, questions)
                # If critical agent has questions, pause
                if agent_name in {"00-orchestrator", "02-plot-analysis"}:
                    logger.info(f"Agent {agent_name} has blocking questions - pausing")
                    issue.create_comment(
                        "⏸ Analysen pausar tills frågor besvarats."
                        " Kommentera `/continue` när du svarat."
                    )
                    return

        except Exception as e:
            logger.exception(f"Agent {agent_name} failed")
            issue.create_comment(
                f"❌ Agent `{agent_name}` misslyckades: {e}. Kolla Actions-loggen för detaljer."
            )
            sys.exit(1)

    # Assemble final report
    final_report = assemble_final_report(issue_data, agent_outputs, settings)

    settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    report_path = settings.outputs_dir / "final-report.md"
    report_path.write_text(final_report, encoding="utf-8")

    # Save structured data for downstream use
    data_path = settings.outputs_dir / "analysis-data.json"
    data_path.write_text(
        json.dumps(
            {
                "issue_number": issue_number,
                "issue_data": issue_data,
                "agents_run": list(agent_outputs.keys()),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    logger.info(f"Final report written: {report_path}")
    issue.create_comment("✅ Analys klar! En Pull Request skapas med fullständig rapport.")


if __name__ == "__main__":
    main()
