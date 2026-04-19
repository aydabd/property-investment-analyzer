"""Tests for issue body parsing and validation logic."""

from __future__ import annotations

from typing import Any

import pytest

from property_investment_planner.run_analysis import (
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

    def test_multiple_missing_reported(self) -> None:
        is_valid, missing = validate_issue_data({})
        assert is_valid is False
        assert len(missing) >= 4

    def test_empty_string_treated_as_missing(self, issue_data_minimal: dict[str, Any]) -> None:
        issue_data_minimal["kommun"] = ""
        is_valid, missing = validate_issue_data(issue_data_minimal)
        assert is_valid is False
        assert "kommun" in missing


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
