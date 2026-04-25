"""Shared pytest fixtures and setup/teardown for all tests.

Separates concerns per module — each test file can have its own
local conftest.py if needed for module-specific fixtures.
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def tmp_workspace() -> Generator[Path, None, None]:
    """Create a temporary workspace for tests that need filesystem access.

    Setup: creates temp dir with subdirs matching real project layout.
    Teardown: removes temp dir after test.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="property-analysis-test-"))
    (tmp_dir / "agents").mkdir()
    (tmp_dir / "skills").mkdir()
    (tmp_dir / "outputs").mkdir()
    (tmp_dir / "outputs" / "agent-outputs").mkdir()
    (tmp_dir / "templates").mkdir()

    yield tmp_dir

    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set required environment variables for tests."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-key")
    monkeypatch.setenv("GH_TOKEN", "ghp_test_token")
    monkeypatch.setenv("REPO", "test-owner/test-repo")


@pytest.fixture
def sample_issue_body() -> str:
    """Sample issue body as GitHub would produce from the form."""
    return """### Kommun

Lund

### Område / Stadsdel

Stångby

### Fastighetsbeteckning

Lund Beryllen 5

### Tomtpris (SEK)

2080000

### Tomtstorlek (kvm)

660

### Deadline (intresseanmälan / budgivning)

2026-04-20

### Källa-URL till prospekt/tomtbeskrivning

https://example.com/prospekt.pdf

### Byggkoncept

Två hus (parhus/spegelvänt)

### Planerad total BTA (kvm)

200

### Partnerskap?

Ja – investerare + byggherre (ingen bygger, en sköter bygget)

### Partnerskaps-detaljer (om tillämpligt)

Partner A: Investerare, 50% kapital
Partner B: Byggherre med eget AB, 50% kapital, sköter byggnation

### Tillgängligt eget kapital totalt (SEK)

3000000

### Förväntad försäljningspris (om du vet)

9400000

### Detaljplan (om du känner till)

1281K-P149

### Övrig viktig info

Radon normal och högrisk (delar)
"""


@pytest.fixture
def mock_anthropic_client() -> MagicMock:
    """Mocked Anthropic client that returns a canned response."""
    client = MagicMock()
    mock_response = MagicMock()
    mock_text_block = MagicMock()
    mock_text_block.text = "## Mock Agent Output\n\nEverything looks good."
    mock_response.content = [mock_text_block]
    client.messages.create.return_value = mock_response
    return client


@pytest.fixture
def mock_github_issue() -> MagicMock:
    """Mocked GitHub issue object."""
    issue = MagicMock()
    issue.number = 42
    issue.body = ""
    issue.create_comment = MagicMock()
    return issue


@pytest.fixture
def mock_github_client(mock_github_issue: MagicMock) -> MagicMock:
    """Mocked Github client wrapping the issue fixture."""
    gh = MagicMock()
    repo = MagicMock()
    repo.get_issue.return_value = mock_github_issue
    gh.get_repo.return_value = repo
    return gh


@pytest.fixture
def stub_agent_file(tmp_workspace: Path) -> Path:
    """Create a stub agent markdown file for tests."""
    agent_file = tmp_workspace / "agents" / "01-test-agent.md"
    agent_file.write_text(
        "# Agent 01: Test\n\nDu är en test-agent. Svara kort.",
        encoding="utf-8",
    )
    return agent_file


@pytest.fixture
def issue_data_minimal() -> dict[str, Any]:
    """Minimal valid issue data passing validation."""
    return {
        "kommun": "TestKommun",
        "område": "TestOmråde",
        "tomtpris": "1000000",
        "tomtstorlek": "500",
        "byggkoncept": "Ett hus (enkel villa)",
        "partnerskap": "Nej – en investerare",
    }


@pytest.fixture
def issue_data_with_partnership(issue_data_minimal: dict[str, Any]) -> dict[str, Any]:
    """Issue data including partnership details."""
    return {
        **issue_data_minimal,
        "partnerskap": "Ja – investerare + byggherre (ingen bygger, en sköter bygget)",
        "partner_detaljer": "Partner A: passiv. Partner B: byggherre, eget AB.",
    }
