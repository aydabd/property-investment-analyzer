# Instruktion: Analysflödet

Detta är **processinstruktionen** som förklarar vad som händer steg-för-steg när
en användare kör systemet.

## Översiktsdiagram

```text
    Användare               GitHub                     Copilot Agent
       │                       │                           │
       │ 1. Skapar Issue       │                           │
       ├──────────────────────>│                           │
       │                       │ 2. Workflow auth-check    │
       │                       │ 3. Assigns @copilot       │
       │                       ├──────────────────────────>│
       │                       │                           │ 4. Läser issue + agents/*.md
       │                       │                           │ 5. Validerar data
       │                       │ 6. Kommentar om saknat    │
       │                       │<──────────────────────────┤
       │ 7. Svarar/redigerar   │                           │
       ├──────────────────────>│                           │
       │                       │                           │ 8-14. Kör agenter
       │                       │                           │    steg för steg
       │                       │ 15. Varje agent           │
       │                       │<──────────────────────────┤
       │                       │    kommenterar i issue    │
       │                       │                           │
       │                       │ 16. PR med slutrapport    │
       │ 17. Granskar PR       │<──────────────────────────┤
       │<──────────────────────│                           │
       │                       │                           │
       │ 18. Merge eller       │                           │
       │   /rerun <agent>      │                           │
       ├──────────────────────>│                           │
```

## Detaljerade Steg

### Steg 1–3: Issue Creation och Copilot Assignment

Användare använder mallen **Investment Analysis**. När issue skapas triggas
`.github/workflows/run-analysis.yml` som:

1. Kontrollerar att användaren finns i `.github/authorized-users.txt`
2. Verifierar att issue har label `investment-analysis`
3. Tilldelar `@copilot` till issue

### Steg 4–6: Validering

Copilot läser issue-fält och agent-instruktioner. Om obligatoriska fält saknas:

- Copilot kommenterar i issue med lista på saknade fält
- Användare måste redigera issue
- Copilot hanterar automatiskt det uppdaterade issuen

### Steg 7: Användar-input

Användare svarar genom att:

- **Redigera issue** (rekommenderas för huvuddata)
- **Kommentera** (för ad-hoc-frågor)

### Steg 8–14: Agent-exekvering

Copilot följer agent-instruktionerna i `agents/` i denna ordning:

1. **01-market-research** – ortspriser, marknad
2. **02-plot-analysis** – detaljplan, kommunala krav
3. **03-build-cost** – byggkostnader
4. **04-financing** – räntor, kapital, skatt
5. **06-partnership** – (om tillämpligt) partnerstruktur
6. **05-risk** – sammanvägd riskbedömning
7. **07-optimizer** – slutbeslut och rekommendation

Varje agent:

- Har sin instruktionsfil i `agents/NN-name.md`
- Får kontext: issue-data + tidigare agenters outputs
- Kan ställa frågor till användaren om data saknas
- Skriver output till `analyses/issue-X/agent-outputs/NN-name.md`

### Steg 15: Löpande Publikation

Copilot kan kommentera i issue med kort sammanfattning per agent
så användaren ser framsteg.

### Steg 16: Pull Request

När alla agenter är klara:

- Copilot skapar branch och PR
- PR innehåller `analyses/issue-X/final-report.md`
- Plus alla agent-outputs i `analyses/issue-X/agent-outputs/`

### Steg 17: Granskning

Användare (och partner, om tillämpligt):

- Läser `final-report.md` direkt i PR
- Kan kommentera specifika sektioner
- Kan kräva revideringar via `/rerun <agent-name>`

### Steg 18: Slutbeslut

**Merge** när nöjd → analysen arkiveras i `analyses/issue-X/`.
**Close without merge** om analysen är inaktuell.
**/rerun all** om ny iteration behövs (utgångsläge ändrats).

## Kommandon i Issues/PR

| Kommando              | Effekt                                         |
| --------------------- | ---------------------------------------------- |
| `/rerun all`          | Kör om hela analysen från scratch              |
| `/rerun <agent-name>` | Kör bara en agent igen (t.ex. `03-build-cost`) |

## Tid

### Tidsåtgång (typiskt)

- Issue till första response: ~2-5 min
- Komplett analys utan väntetid på användarinput: ~10-20 min
- Om agent behöver input flera gånger: 1-3 timmar (väntetid räknas)

## Felsökning

### Workflow kör inte

- Verifiera att ditt användarnamn finns i `.github/authorized-users.txt`
- Verifiera att Copilot Coding Agent är aktiverat (Settings → Copilot)
- Kolla Actions-loggen för felmeddelanden

### Agent ger dåligt svar

- Kommentera `/rerun <agent-name>`
- Eller redigera din issue med mer data, sedan `/rerun all`

### PR skapas inte

- Kolla att Copilot har rätt permissions i repo
- Kolla loggen i Actions-fliken

## Tips för Bra Resultat

1. **Fyll i så mycket som möjligt i issue** – färre iterationer
2. **Bifoga prospekt-URL** – agenterna kan referera till det
3. **Var tydlig med partnerskap** – inga antaganden om delning
4. **Verifiera ortspriser själv** innan analysen – agenterna uppskattar men kan ha fel
5. **Kör en test-analys först** på ett exempel innan du gör en riktig
