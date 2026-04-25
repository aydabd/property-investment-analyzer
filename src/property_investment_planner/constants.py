"""Constants and environment variables for the analysis runner.

All configuration is centralized here. Type-safe access via pydantic Settings.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Anthropic (optional — only needed for standalone Python runner, not Copilot)
    anthropic_api_key: str = Field(
        default="",
        description="API key for Claude (optional when using Copilot Coding Agent)",
    )
    claude_model: str = Field(
        default="claude-opus-4-7",
        description="Claude model to use for agents",
    )
    claude_model_fast: str = Field(
        default="claude-haiku-4-5-20251001",
        description="Faster model for simple tasks like eval",
    )
    max_tokens: int = Field(default=8000)

    # GitHub
    github_token: str = Field(
        ...,
        alias="GH_TOKEN",
        description="GitHub token for issue/PR operations",
    )
    github_repo: str = Field(
        default="",
        alias="REPO",
        description="owner/repo-name",
    )

    # Paths
    agents_dir: Path = Field(default=Path("agents"))
    skills_dir: Path = Field(default=Path("skills"))
    partnership_dir: Path = Field(default=Path("partnership"))
    templates_dir: Path = Field(default=Path("templates"))
    outputs_dir: Path = Field(default=Path("outputs"))
    agent_outputs_dir: Path = Field(default=Path("outputs/agent-outputs"))

    # Behavior
    max_iterations_per_agent: int = Field(default=3)
    ask_user_timeout_minutes: int = Field(default=60)
    log_level: str = Field(default="INFO")


# Agent execution order (orchestrator decides subset to run)
AGENT_EXECUTION_ORDER: Final[list[str]] = [
    "00-orchestrator",
    "01-market-research",
    "02-plot-analysis",
    "03-build-cost",
    "04-financing",
    "06-partnership",  # Before risk, so risk can reference it
    "05-risk",
    "07-optimizer",
    "99-eval",
]

# Agents that require user input before running
AGENTS_REQUIRING_USER_INPUT: Final[set[str]] = {
    "06-partnership",
}

# Required fields from issue for basic analysis
REQUIRED_ISSUE_FIELDS: Final[set[str]] = {
    "kommun",
    "område",
    "tomtpris",
    "tomtstorlek",
    "byggkoncept",
    "partnerskap",
}

# Issue field parsers (label in form → normalized field)
ISSUE_FIELD_MAPPING: Final[dict[str, str]] = {
    "Kommun": "kommun",
    "Område / Stadsdel": "område",
    "Fastighetsbeteckning": "fastighetsbeteckning",
    "Tomtpris (SEK)": "tomtpris",
    "Tomtstorlek (kvm)": "tomtstorlek",
    "Deadline (intresseanmälan / budgivning)": "deadline",
    "Källa-URL till prospekt/tomtbeskrivning": "källa_url",
    "Byggkoncept": "byggkoncept",
    "Planerad total BTA (kvm)": "total_bta",
    "Partnerskap?": "partnerskap",
    "Partnerskaps-detaljer (om tillämpligt)": "partner_detaljer",
    "Tillgängligt eget kapital totalt (SEK)": "eget_kapital",
    "Förväntad försäljningspris (om du vet)": "marknadsvärde",
    "Detaljplan (om du känner till)": "detaljplan_info",
    "Övrig viktig info": "övrig_info",
}

# Default financial assumptions (when user doesn't specify)
DEFAULT_ASSUMPTIONS: Final[dict[str, float | int]] = {
    "bygglåneränta_procent": 5.0,
    "bolåneränta_procent": 4.0,
    "byggtid_månader": 14,
    "oförutsett_procent": 10,
    "kapitalvinstskatt_procent": 22,
    "mäklararvode_procent": 2.5,
    "marknadstimpris_byggherre": 500,
}


def load_settings() -> Settings:
    """Load settings with validation."""
    return Settings()  # type: ignore[call-arg]
