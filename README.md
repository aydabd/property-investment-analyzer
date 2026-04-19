# 🏗️ Property Investment Planner

GitHub-native, AI-driven analyssystem för **bygg-och-sälj-investeringar** i svenska kommuner.
Designad för **partnerskap mellan investerare och byggherre**.

**👉 Ny användare? Börja med [QUICKSTART.md](QUICKSTART.md)**

## Hur det fungerar

```text
1. Skapa Issue (använd mall)
     ↓
2. GitHub Action triggas → Copilot tilldelas issue
     ↓
3. Copilot läser agent-instruktioner och analyserar steg-för-steg
     ↓
4. Copilot kommenterar i issue, ber om data om det behövs
     ↓
5. Copilot skapar PR med komplett rapport
     ↓
6. Granska, kommentera, merge
```

## Vem använder detta?

- **Investerare** – vill bedöma en specifik tomt/kommun
- **Byggherrar** – vill verifiera kalkyl innan budgivning
- **Partnerskap** – 2+ personer som delar investering och arbete

## Snabbstart

1. **Fork detta repo** (eller använd som template)
2. **Aktivera Copilot Coding Agent** i repo-inställningarna
3. **Lägg till dig i `.github/authorized-users.txt`** för agent-trigger
4. **Redigera CODEOWNERS** med ditt användarnamn (för PR-granskning)
5. **Skapa en Issue** med mallen `Investment Analysis`
6. **Copilot analyserar** — ställer frågor och levererar rapport som PR

Detaljer: [QUICKSTART.md](QUICKSTART.md) | [SETUP.md](SETUP.md)

## Dokumentation

| Dokument                                                                       | Syfte                            |
| ------------------------------------------------------------------------------ | -------------------------------- |
| [QUICKSTART.md](QUICKSTART.md)                                                 | 15-min guide för första analysen |
| [SETUP.md](SETUP.md)                                                           | Detaljerad installation          |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)                                     | Filstruktur och design-principer |
| [partnership/README.md](partnership/README.md)                                 | Partnerskapsmodellen             |
| [instructions/analysis-workflow.md](instructions/analysis-workflow.md)         | Hur flödet fungerar              |
| [instructions/github-projects-setup.md](instructions/github-projects-setup.md) | Milestones och kanban            |
| [examples/01-stangby-beryllen.md](examples/01-stangby-beryllen.md)             | Komplett exempel-analys          |

## Repo-struktur

```text
.
├── README.md                  ← Start
├── QUICKSTART.md              ← 15-min guide
├── SETUP.md                   ← Installation
├── pyproject.toml             ← Python-paket (hatchling)
│
├── .github/
│   ├── ISSUE_TEMPLATE/        ← 3 mallar (analys, månadsrapport, sub-task)
│   └── workflows/             ← 3 workflows (analys, eval, tests)
│
├── agents/                    ← 9 generiska agenter
│   ├── 00-orchestrator.md     ← Koordinerar
│   ├── 01-market-research.md  ← Ortspriser
│   ├── 02-plot-analysis.md    ← Detaljplan
│   ├── 03-build-cost.md       ← Byggkostnader
│   ├── 04-financing.md        ← Räntor, skatt
│   ├── 05-risk.md             ← Risker
│   ├── 06-partnership.md      ← Partner-struktur
│   ├── 07-optimizer.md        ← Slutbeslut
│   ├── 99-eval.md             ← QA
│   └── meta-template-generator.md  ← Hjälp nybörjare
│
├── skills/                    ← Återanvändbar kunskap
├── partnership/               ← Avtalsmallar
├── templates/                 ← Rapportmall
├── instructions/              ← Processdokument
├── src/
│   └── property_investment_planner/  ← Python-paket
├── tests/                     ← Pytest-svit
└── examples/                  ← Riktiga analyser
```

## Design-principer

**Generiskt** – agenterna frågar användaren efter kommun, tomt, priser. Ingen hårdkodning.

**Partnerskaps-medvetet** – varje finansiell kalkyl delas upp mellan investerare och byggherre enligt överenskommen modell.

**GitHub-native** – inga servrar, ingen cloud. Bara issues, actions, projects, artifacts.

**Transparent** – alla antaganden, räntor, skatter synliga i rapporten.

**Bygg-och-sälj-fokus** – uthyrning är **inte** inkluderat. Kort horisont, realiserad vinst, reinvestering.

**Testat** – Python-scripten har pytest-tests som körs vid varje PR.

## Tekniska val

- **Copilot Coding Agent** — ingen extern API-nyckel krävs
- GitHub Actions för auth-kontroll och trigger
- Agent-instruktioner i markdown (`agents/*.md`)
- Python 3.13+ verktygskod (pydantic, mypy) för helpers och tester
- Tester med `pytest` och `conftest.py` för modulär setup/teardown
- [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) för isolerad utvecklingsmiljö
- [pre-commit](https://pre-commit.com/) för all linting (single source of truth)

## Utvecklingsmiljö

All lintning och formatering körs via **pre-commit** inuti en
**micromamba**-miljö. Inga manuella installationer behövs.

```bash
# Engångs-setup (installerar miljö + Git hooks)
make install

# Lint och auto-formatera (lokal utveckling)
make lint

# Kör tester
make test

# Kör tester med coverage
make coverage

# Visa alla tillgängliga kommandon
make help
```

### CI

CI kör samma `make lint` med `LINT_MODE=check` — inga auto-fixar,
bara verifiering. Samma verktyg, samma konfiguration, samma resultat.

## Bidra

Har du förbättringar till en agent? Ett nytt skill? Ett exempel att dela?
Öppna en PR. Se [`CONTRIBUTING.md`](CONTRIBUTING.md) för mall och riktlinjer.

## Ingen Garanti

Detta är en **analysassistent**, inte en finansiell rådgivare. Verifiera alltid
kritiska siffror innan bindande beslut. Kontakta:

- Revisor för skatt
- Fastighetsjurist för avtal
- Bank för lånevillkor
- Kommunen för planrätt

## Licens

MIT – använd, fork:a, modifiera efter behov. Se LICENSE.
