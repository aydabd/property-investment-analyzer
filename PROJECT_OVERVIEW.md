# 📦 Projekt-översikt: Filstruktur

Komplett filöversikt av repot. Använd som kartbok för att förstå vad som finns var.

## 🗂 Filträd

```
.
├── README.md                          ← Start här
├── SETUP.md                           ← Installation
├── .env.example                       ← Mall för lokala credentials
├── .gitignore
│
├── .github/
│   ├── CODEOWNERS                     ← Kodgranskning/path ownership
│   ├── authorized-users.txt           ← Vem får trigga analyser
│   ├── labels.yml                     ← Label-konfiguration
│   ├── ISSUE_TEMPLATE/
│   │   ├── investment-analysis.yml   ← Huvud-template för ny analys
│   │   ├── monthly-report.yml        ← Byggherrens månadsrapport
│   │   └── sub-task.yml              ← Underuppgifter
│   └── workflows/
│       ├── run-analysis.yml          ← Trigger: issue → agenter körs
│       └── eval.yml                  ← Trigger: PR → kvalitetskontroll
│
├── agents/                            ← Hjärtat – agent-definitioner
│   ├── 00-orchestrator.md            ← Koordinator
│   ├── 01-market-research.md         ← Ortspriser, marknad
│   ├── 02-plot-analysis.md           ← Detaljplan, kommunala krav
│   ├── 03-build-cost.md              ← Byggkostnader
│   ├── 04-financing.md               ← Räntor, kapital, skatt
│   ├── 05-risk.md                    ← Riskbedömning
│   ├── 06-partnership.md             ← Partnerstruktur (KÄRNAN)
│   ├── 07-optimizer.md               ← Slutbeslut
│   ├── 99-eval.md                    ← Kvalitetskontroll
│   └── meta-template-generator.md    ← Hjälp nybörjare starta
│
├── skills/                            ← Återanvändbar kunskap
│   ├── data-sources.md               ← Verifierade datakällor
│   └── financial-formulas.md         ← Formler agenterna använder
│
├── partnership/                       ← Partnerskapsmodellen
│   ├── README.md                     ← Förklarar modellen
│   ├── agreement-template.md         ← Färdigt avtal att signera
│   └── monthly-report-template.md    ← Månadsrapport B→A
│
├── templates/
│   └── report-template.md            ← Slutrapport-format
│
├── instructions/                      ← Processdokumentation
│   ├── analysis-workflow.md          ← Hur flödet fungerar
│   └── github-projects-setup.md      ← Projects/milestones
│
├── src/property_investment_planner/  ← Python som kör agenterna
│   ├── constants.py                  ← Config, types
│   ├── run_analysis.py               ← Main runner
│   └── run_eval.py                   ← Eval runner
│
└── examples/
    ├── README.md
    └── 01-stangby-beryllen.md        ← Komplett exempel-analys
```

## 📊 Räkneexempel (filmängd)

- **8 agenter** som kan köras individuellt eller i sekvens
- **3 issue-templates** för olika scenarier
- **2 workflows** som triggar automation
- **2 Python-scripts** som gör det körbart
- **3 partnerskap-dokument** för konfliktförebyggande
- **2 skills** (data + formler) som alla agenter kan referera till

## 🎯 Design-principer Uppfyllda

| Din Önskning                          | Hur det Lösts                                                                                       |
| ------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1. Investerare + byggherre utan tvist | `partnership/` – agreement-mall, 3 vinstdelningsmetoder, RACI-matris, kostnadsöverskridnings-regler |
| 2. Bara bygg-och-sälj                 | Ingen uthyrnings-agent. Optimizer fokuserar på reinvestering. Issue-template frågar aktivt          |
| 3. Generiska agenter                  | Alla agenter har "ingen hårdkodning" i sin systemprompt. Frågar användaren om platsdata             |
| 4. GitHub-baserat, ingen cloud        | GitHub Actions + Copilot Coding Agent. Inga API-nycklar, inga servrar, ingen databas                |
| 5. Enkel för användare                | Issue-template → agenterna sköter resten → PR med läsbar rapport + PDF-artifact                     |
| Meta-template-agent                   | `agents/meta-template-generator.md` hjälper nybörjare skapa första issue genom dialog               |

## 🚀 Att göra innan första körning

1. **Fork eller template-klona** repot
2. **Redigera `.github/CODEOWNERS`** – byt `@REPLACE_WITH_YOUR_USERNAME` mot riktiga användarnamn
3. **Aktivera Copilot Coding Agent** i repo-inställningarna (Settings → Copilot)
4. **Lägg till dig i `.github/authorized-users.txt`**
5. **Applicera labels** (manuellt eller via GitHub API):

   ```bash
   gh label create analysis-in-progress --color fbca04 --description "Agenter kör"
   # (upprepa för alla labels i labels.yml)
   ```

6. **Skapa ett Project** enligt `instructions/github-projects-setup.md`
7. **Testkör** med exempel-data från `examples/01-stangby-beryllen.md`

## 💡 Tips

- **Börja enkelt**: Kör en analys utan partnerskap först för att förstå flödet
- **Läs exemplen**: `examples/01-stangby-beryllen.md` visar vad som kommer ut
- **Iterera agenter**: Om en agent ger konstigt svar, justera `agents/NN-name.md` och commit → samma issue kan köras om
- **Repo-template**: När allt fungerar, gör repot till GitHub Template så andra kan fork:a

## 🔐 Säkerhet och Integritet

- Känsliga avtal (`partnership/signed-*.md`) ignoreras i git (se `.gitignore`)
- API-nyckel lagras som repo-secret, aldrig i kod
- CODEOWNERS gate:ar vem som kan trigga analyser
- Privata repos rekommenderas – analyser innehåller finansiell data

## 📚 Att Läsa i Ordning (för ny användare)

1. `README.md` – förstå vad systemet är
2. `SETUP.md` – sätt upp ditt eget repo
3. `examples/01-stangby-beryllen.md` – se hur en färdig analys ser ut
4. `partnership/README.md` – förstå partnerskapsmodellen
5. `instructions/analysis-workflow.md` – förstå exekveringen
6. Skapa din första issue via `.github/ISSUE_TEMPLATE/investment-analysis.yml`

## 🧪 Återanvändbarhet

Hela repot är designat som **mall**. När det blir klart i din instans:

1. Gör `Settings → Template repository: on`
2. Andra fork:ar och använder för sina egna investeringar
3. Deras analyser blir separata instanser – ditt data delas inte

Detta är inte en SaaS-produkt – det är en **repeterbar process i form av kod och
dokumentation** som var och en driver själv.
