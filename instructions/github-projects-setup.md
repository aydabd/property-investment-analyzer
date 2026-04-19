# Instruktion: GitHub Projects Setup (Milestones & Planering)

Detta dokument visar hur du använder **GitHub Projects** för att planera och spåra
din investeringspipeline — från analys till färdigställd försäljning.

## Varför GitHub Projects?

En komplett investeringspipeline har många faser:

- Issue-skapande
- Analys-körning
- Beslut
- Byggfas
- Försäljning
- Reinvestering

Projects ger en **kanban-vy** över allt, utan extern programvara.

## Rekommenderad Project-struktur

Skapa ett Project av typen "Board" med dessa kolumner:

```text
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Backlog   │  │ Analyzing   │  │ Decision    │  │ Building    │  │ Completed   │
│             │  │             │  │             │  │             │  │             │
│ Idé-tomter  │  │ Agenter kör │  │ Partner     │  │ Projektet   │  │ Sålt och    │
│ att bevaka  │  │             │  │ granskar    │  │ byggs       │  │ redovisat   │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Milestones per Projekt

För varje aktivt projekt, skapa milestones:

```
Milestone: [Projekt X] - Analysfas
  Due: +2 veckor från issue
  Issues: analysis, planbesked, finansiering-check

Milestone: [Projekt X] - Beslutsfas
  Due: +2 veckor från analys
  Issues: partneravtal, bank-godkännande, arrendeavtal

Milestone: [Projekt X] - Byggfas
  Due: 14 månader från arrendeavtal
  Issues: milstolpar från byggplan (grund klar, stomme, tak, etc.)

Milestone: [Projekt X] - Försäljning
  Due: +2 månader efter slutbesked
  Issues: styling, mäklare, visning, tillträde

Milestone: [Projekt X] - Klart
  Due: +30 dagar efter tillträde
  Issues: vinstutdelning, skatt, reinvesterings-planering
```

## Labels att Använda

### Per fas

- `analysis` – agenter kör
- `decision-pending` – väntar på partner/bank
- `building` – aktivt bygge
- `selling` – till försäljning
- `completed` – klar

### Per risknivå

- `risk-high` – kritisk fråga öppen
- `risk-medium` – bevakning
- `risk-low` – allt under kontroll

### Per typ

- `investment-analysis` – huvud-issue
- `sub-task` – detaljerad uppgift under huvud-issue
- `decision-point` – kritiskt beslut

### Per partner

- `partner-investor` – investerare-fokuserat
- `partner-builder` – byggherre-fokuserat
- `joint` – båda parter

## Automation via Projects

GitHub Projects stöder automation utan kod:

```yaml
# Exempel-regler att sätta upp i UI:
- När issue får label "analysis-complete" → flytta till "Decision" kolumn
- När PR mergeas → flytta relaterat issue till "Building"
- När issue stängs → flytta till "Completed"
- När label "risk-high" läggs till → notifiera authorized-users
```

## Rapportering via Projects

### Månatlig översikt

Projects visar automatiskt:

- Antal projekt per fas
- Velocity (hur länge varje fas tar)
- Blocker-issues
- Resursfördelning per partner

### Partner-reporting

Filtrera Project-vy på label `partner-a` eller `partner-b`:

- Se bara dina egna uppgifter
- Följ månadsrapporter (se `partnership/monthly-report-template.md`)

## Setup-steg (en gång per repo)

1. **Skapa Project**
   - Gå till `https://github.com/<owner>/<repo>/projects`
   - "New Project" → välj "Board" layout
   - Namn: "Investeringspipeline"

2. **Konfigurera kolumner**
   - Lägg till kolumner enligt strukturen ovan
   - Sätt "Welcome" till "Backlog"
   - Sätt "In progress" till "Analyzing"
   - Sätt "Done" till "Completed"

3. **Koppla repot**
   - Project Settings → "Add repository"
   - Välj ditt repo

4. **Skapa labels** (via `.github/labels.yml` eller manuellt)

5. **Skapa första milestones** för ditt första projekt

## Exempel: Hur ett projekt rör sig genom pipeline

```text
Dag 1:   Issue skapas → Backlog
         Label: investment-analysis

Dag 1:   Workflow triggers → Analyzing
         Agenter börjar köra

Dag 1:   Agent-frågor → paused, label "needs-input"

Dag 3:   Användare svarar → "/rerun all" → Analyzing
         Analys återupptas

Dag 4:   Analysrapport klar → PR skapas
         Issue label: "analysis-complete"
         → Flyttas till Decision

Dag 10:  Partners granskar, diskuterar i PR-kommentarer

Dag 14:  PR merged, partneravtal signerat
         Issue label: "decision-made", "building"
         → Flyttas till Building
         Milestone "Byggfas" skapas med underliggande issues

Dag 60:  "Grund klar" sub-issue stängs (milstolpe)
         Månadsrapport postad

...

Dag 470: Slutbesked, huset säljs
         → Flyttas till Selling

Dag 530: Tillträde, pengar fördelade
         Issue stängs → Completed
```

## Tips

- **Ett projekt-issue per investering** – inte per agent-körning
- **Sub-issues** för byggmilstolpar, kopplade till huvudissue via "Tracks"
- **Månadsrapport som separat issue** – spåra historik, label `monthly-report`
- **Template för reinvestering** – när en investering blir klar, använd en issue-template för att snabbt starta nästa
