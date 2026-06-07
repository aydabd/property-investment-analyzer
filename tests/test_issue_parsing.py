"""Tests for issue body parsing and validation logic."""

from __future__ import annotations

from typing import Any

import pytest

from property_investment_planner.run_analysis import (
    collect_orchestrator_questions,
    detect_agent_questions,
    parse_issue_body,
    validate_issue_data,
)


class TestParseIssueBody:
    """Tests for parse_issue_body()."""

    def test_parses_all_fields_from_sample(self, sample_issue_body: str) -> None:
        result = parse_issue_body(sample_issue_body)

        assert result["kommun"] == "Lund"
        assert result["område"] == "Stångby"
        assert result["tomtpris"] == "2080000"
        assert result["tomtstorlek"] == "660"
        assert result["fastighetsbeteckning"] == "Lund Beryllen 5"
        assert result["byggkoncept"] == "Två hus (parhus/spegelvänt)"

    def test_ignores_no_response_placeholders(self) -> None:
        body = """### Kommun

Lund

### Fastighetsbeteckning

_No response_

### Tomtpris (SEK)

2080000
"""
        result = parse_issue_body(body)
        assert "kommun" in result
        assert "tomtpris" in result
        assert "fastighetsbeteckning" not in result

    def test_handles_empty_body(self) -> None:
        result = parse_issue_body("")
        assert result == {}

    def test_handles_multiline_values(self) -> None:
        body = """### Övrig viktig info

Rad ett
Rad två
Rad tre

### Tomtpris (SEK)

500000
"""
        result = parse_issue_body(body)
        assert "Rad ett" in result["övrig_info"]
        assert "Rad tre" in result["övrig_info"]
        assert result["tomtpris"] == "500000"

    def test_preserves_unknown_fields_under_original_name(self) -> None:
        body = """### Some New Field

Some value
"""
        result = parse_issue_body(body)
        # Unknown fields are kept under their header as-is
        assert "Some New Field" in result


class TestValidateIssueData:
    """Tests for validate_issue_data()."""

    def test_valid_minimal_passes(self, issue_data_minimal: dict[str, Any]) -> None:
        is_valid, missing = validate_issue_data(issue_data_minimal)
        assert is_valid is True
        assert missing == []

    def test_missing_kommun_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        del issue_data_minimal["kommun"]
        is_valid, missing = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "kommun" in missing

    def test_none_kommun_reports_missing_only(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["kommun"] = None
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "kommun" in problems
        assert not any(problem.startswith("kommun:") for problem in problems)

    def test_multiple_missing_reported(self) -> None:
        is_valid, missing = validate_issue_data({})
        assert is_valid is False
        assert len(missing) >= 4

    def test_empty_string_treated_as_missing(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["kommun"] = ""
        is_valid, missing = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "kommun" in missing

    def test_unrecognized_kommun_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["kommun"] = "TestKommun"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert any(problem.startswith("kommun:") for problem in problems)

    def test_kommun_validation_is_case_insensitive(
        self, issue_data_minimal: dict[str, Any]
    ) -> None:
        issue_data_minimal["kommun"] = "lund"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is True
        assert problems == []

    def test_low_tomtpris_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["tomtpris"] = "100000"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "tomtpris" in " ".join(problems)

    def test_invalid_tomtpris_format_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["tomtpris"] = "1000000 kr"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "ogiltigt talformat" in " ".join(problems)

    def test_out_of_range_tomtstorlek_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["tomtstorlek"] = "90"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "tomtstorlek" in " ".join(problems)

    def test_invalid_tomtstorlek_format_fails(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["tomtstorlek"] = "500 kvm"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "ogiltigt talformat" in " ".join(problems)

    def test_inconsistent_partnership_details_fails(
        self, issue_data_minimal: dict[str, Any]
    ) -> None:
        issue_data_minimal["partnerskap"] = (
            "Ja – investerare + byggherre (ingen bygger, en sköter bygget)"
        )
        issue_data_minimal["partner_detaljer"] = "En partner som köper och bygger själv"
        is_valid, problems = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "partnerskap" in " ".join(problems)


class TestCollectOrchestratorQuestions:
    """Tests for collect_orchestrator_questions()."""

    def test_missing_detaljplan_creates_question(self, issue_data_minimal: dict[str, Any]) -> None:
        questions = collect_orchestrator_questions(issue_data_minimal)
        assert any("Detaljplan-nummer" in question for question in questions)

    def test_no_questions_when_required_context_exists(
        self,
        issue_data_minimal: dict[str, Any],
    ) -> None:
        issue_data_minimal["detaljplan_info"] = "1281K-P149"
        issue_data_minimal["deadline"] = "2026-06-20"
        questions = collect_orchestrator_questions(issue_data_minimal)
        assert questions == []


class TestDetectAgentQuestions:
    """Tests for detect_agent_questions()."""

    def test_extracts_question_block(self) -> None:
        output = """## Market Research

Some result.

## Market Research: frågor

1. Fråga ett?
2. Fråga två?
"""
        questions = detect_agent_questions(output)
        assert len(questions) == 1
        assert "Fråga ett" in questions[0]
        assert "Fråga två" in questions[0]

    def test_no_questions_found(self) -> None:
        output = "## Market Research\n\nAllt bra, inga frågor.\n"
        questions = detect_agent_questions(output)
        assert questions == []

    def test_stops_at_next_section(self) -> None:
        output = """## Agent: frågor

Fråga här.

## Nästa Sektion

Annan text.
"""
        questions = detect_agent_questions(output)
        assert len(questions) == 1
        assert "Fråga här" in questions[0]
        assert "Annan text" not in questions[0]

    @pytest.mark.parametrize(
        "header",
        [
            "## Agent: frågor",
            "## agent: frågor",
            "## Agent: fråga",
            "## My Cool Agent: frågor ",
        ],
    )
    def test_recognizes_varied_headers(self, header: str) -> None:
        output = f"{header}\n\nFrågetext här.\n"
        questions = detect_agent_questions(output)
        assert len(questions) == 1
