# Setup Guide

## 1. Klona eller fork detta repo

```bash
# Som template (rekommenderas)
gh repo create my-investment-analysis --template <this-repo> --private

# Eller klona
git clone <this-repo> my-investment-analysis
cd my-investment-analysis
```

## 2. Aktivera Copilot Coding Agent

I repot: **Settings → Copilot → Coding Agent → Enable**.

Copilot behöver kunna:

- Läsa issues
- Skapa branches och PRs
- Kommentera i issues

Ingen extern API-nyckel behövs.

## 3. Konfigurera behörigheter

Redigera `.github/CODEOWNERS` (för PR-granskning):

```
# Kodgranskning / PR-godkännande
* @your-github-username @partner-github-username
/partnership/ @your-github-username
```

Redigera `.github/authorized-users.txt` (för agent-trigger):

```
your-github-username
partner-github-username
```

CODEOWNERS styr kodgranskning/PR-godkännande.
`authorized-users.txt` styr vem som kan trigga analyser.

## 4. Skapa en första analys

Gå till **Issues → New Issue → Investment Analysis**.

Fyll i:

- Kommun (ex: Lund)
- Tomt-info (pris, storlek, källa)
- Byggkoncept
- Partnerstruktur (om tillämpligt)

Skicka in. GitHub Action startar automatiskt.

## 5. Följ analysen

- Agenterna kommenterar i issue med frågor om data saknas
- Svara genom att kommentera eller redigera issue
- När alla agenter kört → en PR skapas med `Final Report.md`
- PR innehåller artifact som PDF för delning

## 6. Godkänn eller itera

- Läs rapporten i PR:en
- Om det ser bra ut → merge till `main` (arkiveras)
- Om du vill justera → kommentera `/rerun <agent-name>` i PR

## Alternativa sätt att köra

### Lokalt (med micromamba)

```bash
# Installera miljö och Git hooks
make install

# Aktivera miljön
micromamba activate property-investment-analyzer

# Kör analysen
export ANTHROPIC_API_KEY=sk-ant-...
python -m property_investment_planner.run_analysis --issue-number 1 --repo owner/repo
```

### Via GitHub CLI

```bash
gh issue create --template investment-analysis.md
```

## Utvecklingsverktyg

All lintning och test körs via `make`. Inga manuella installationer.

```bash
make install      # Skapar micromamba-miljö + installerar Git hooks
make lint         # Auto-formatera + lint (lokal utveckling)
make test         # Kör tester
make coverage     # Tester med coverage-rapport
make clean        # Rensa build-artefakter
make help         # Visa alla kommandon
```

Miljön använder [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
för isolerad hantering av Python, linters (ruff, mypy, yamllint), formatters
(prettier, shfmt, markdownlint) och testverktyg (pytest).

CI kör `LINT_MODE=check make lint` — samma verktyg, ingen auto-fix.

## Ingen cloud krävs

Allt körs via:

- **GitHub Actions** – gratis för privata repos upp till viss gräns
- **Anthropic API** – du betalar per token (~$2–5 per komplett analys)
- **GitHub Artifacts** – rapporterna sparas som artifacts i 90 dagar

Inga webbsidor, ingen serverhosting, ingen databas.
