"""Tests for agent execution and orchestration logic."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from property_investment_planner.run_analysis import (
    build_agent_context,
    decide_agents_to_run,
    load_agent_prompt,
)


class TestDecideAgentsToRun:
    """Tests for decide_agents_to_run()."""

    def test_all_includes_partnership_when_applicable(
        self,
        issue_data_with_partnership: dict[str, Any],
    ) -> None:
        agents = decide_agents_to_run("all", issue_data_with_partnership)
        assert "06-partnership" in agents

    def test_all_skips_partnership_for_solo_investor(
        self,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        agents = decide_agents_to_run("all", issue_data_minimal)
        assert "06-partnership" not in agents

    def test_specific_agent_returns_single_agent(self, issue_data_minimal: dict[str, Any]) -> None:
        agents = decide_agents_to_run("03-build-cost", issue_data_minimal)
        assert agents == ["03-build-cost"]

    def test_unknown_agent_returns_empty(self, issue_data_minimal: dict[str, Any]) -> None:
        agents = decide_agents_to_run("nonexistent-agent", issue_data_minimal)
        assert agents == []


class TestLoadAgentPrompt:
    """Tests for load_agent_prompt()."""

    def test_loads_existing_agent(
        self,
        stub_agent_file: Path,
        tmp_workspace: Path,
        mock_env: None,
    ) -> None:
        settings = _make_settings(tmp_workspace)
        content = load_agent_prompt("01-test-agent", settings)
        assert "Test" in content

    def test_raises_for_missing_agent(self, tmp_workspace: Path, mock_env: None) -> None:
        settings = _make_settings(tmp_workspace)
        with pytest.raises(FileNotFoundError):
            load_agent_prompt("does-not-exist", settings)


class TestBuildAgentContext:
    """Tests for build_agent_context()."""

    def test_context_includes_issue_data(
        self,
        tmp_workspace: Path,
        mock_env: None,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        settings = _make_settings(tmp_workspace)
        context = build_agent_context(
            agent_name="01-test",
            issue_data=issue_data_minimal,
            previous_outputs={},
            settings=settings,
        )
        assert "TestKommun" in context
        assert "## Issue Data" in context

    def test_context_includes_previous_outputs(
        self,
        tmp_workspace: Path,
        mock_env: None,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        settings = _make_settings(tmp_workspace)
        previous = {"01-previous": "Previous analysis content."}
        context = build_agent_context(
            agent_name="02-next",
            issue_data=issue_data_minimal,
            previous_outputs=previous,
            settings=settings,
        )
        assert "Previous analysis content" in context
        assert "01-previous" in context

    def test_context_mentions_current_agent(
        self,
        tmp_workspace: Path,
        mock_env: None,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        settings = _make_settings(tmp_workspace)
        context = build_agent_context(
            agent_name="05-risk",
            issue_data=issue_data_minimal,
            previous_outputs={},
            settings=settings,
        )
        assert "05-risk" in context

    def test_context_includes_default_assumptions(
        self,
        tmp_workspace: Path,
        mock_env: None,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        settings = _make_settings(tmp_workspace)
        context = build_agent_context(
            agent_name="04-financing",
            issue_data=issue_data_minimal,
            previous_outputs={},
            settings=settings,
        )
        assert "Default Assumptions" in context
        assert "bygglåneränta_procent" in context


def _make_settings(workspace: Path) -> Any:
    """Construct a Settings object pointing at the test workspace."""
    from property_investment_planner.constants import Settings

    return Settings(
        agents_dir=workspace / "agents",
        skills_dir=workspace / "skills",
        outputs_dir=workspace / "outputs",
        agent_outputs_dir=workspace / "outputs" / "agent-outputs",
        templates_dir=workspace / "templates",
    )
