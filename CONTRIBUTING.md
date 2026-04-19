# Bidra till Property Investment Planner

Tack för ditt intresse! Det finns flera sätt att bidra.

## Sätt att Bidra

### 1. Förbättra en Agent

Agenterna är markdown-filer i `agents/`. Om du märker att en agent:

- Missar något kritiskt område
- Ger för svaga svar
- Inte hanterar ett scenario väl

→ Öppna PR med uppdatering. Visa ett konkret exempel på output före/efter.

### 2. Dela ett Exempel

När du kör en lyckad analys:

1. Anonymisera:
   - Byt ut namn mot "Partner A", "Partner B"
   - Ta bort specifika fastighetsbeteckningar (eller notera tydligt att det är publikt data)
   - Runda av känsliga belopp

2. Kopiera rapport till `examples/NN-kort-namn.md`

3. Öppna PR

Andra användare lär sig från dina framgångar.

### 3. Lägg till Skill

Generisk kunskap som flera agenter kan använda? Skapa en skill i `skills/`.

Exempel på bra skills:

- `skills/va-rates-by-region.md` – kommunspecifika VA-avgifter (uppdateras årligen)
- `skills/build-suppliers.md` – byggmaterial-leverantörer + ungefärliga priser
- `skills/common-planbestämmelser.md` – vanliga planbestämmelser-tolkningar

### 4. Förbättra Python-källkoden

`src/property_investment_planner/` innehåller orkestreringen. Bidrag här kräver:

- Tester (`tests/`)
- Typer (mypy strict mode)
- Docstrings (Google-stil)
- Ruff-clean

Kör lokalt:

```bash
pip install -e ".[dev]"
pytest tests/
ruff check src/ tests/
mypy src/
```

### 5. Rapportera Bugg

Öppna issue med label `bug`. Inkludera:

- Vad du försökte göra
- Vad som hände
- Vad du förväntade
- Actions-logg (redigerad för känslig data)

## PR-process

1. Fork:a repot
2. Skapa feature-branch: `git checkout -b feature/min-ändring`
3. Gör ändring + tester
4. Commit:a med beskrivande meddelande
5. Push:a och öppna PR mot `main`

## Commit-stil

Använd [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: lägg till radon-agent
fix: korrigera ränte-beräkning över månaderna
docs: förtydliga partnerskapsmodellen
test: utöka partnerskap-split tester
refactor: flytta constants till separat fil
```

## Code of Conduct

- Respektfull kommunikation
- Konstruktiv kritik
- Fokusera på kod, inte personer
- Hjälp andra bidragsgivare

## Frågor?

Öppna en Discussion-tråd eller tagga @maintainers i en issue.
