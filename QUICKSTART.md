# ⚡ Quickstart – Första Analysen på 15 Minuter

Du har just forkat eller använt repot som template. Här är snabbaste vägen till
din första investeringsanalys.

## Förutsättningar

- [ ] GitHub-konto med Copilot (Individual, Business, eller Enterprise)
- [ ] Copilot Coding Agent aktiverat i repo-inställningarna

## Steg 1: Setup (5 min)

### 1a. Aktivera Copilot Coding Agent

I repot: **Settings → Copilot → Coding Agent → Enable**.

### 1b. Uppdatera CODEOWNERS

Redigera `.github/CODEOWNERS` och byt:

```text
* @REPLACE_WITH_YOUR_USERNAME
```

till din GitHub-användarnamn (och partners, om tillämpligt).

### 1c. Applicera labels

```bash
# Ett snabbt sätt (om du har Node installerat):
npx github-label-sync --access-token $(gh auth token) \
  --labels .github/labels.yml \
  $(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Eller skapa dem manuellt via `Issues → Labels → New label`.

## Steg 2: Testa med Ett Känt Exempel (5 min)

Testa systemet mot ett känt exempel innan din riktiga analys:

### 2a. Skapa en test-issue

```bash
gh issue create \
  --title "[TEST] Stångby Beryllen – validerar system" \
  --label "investment-analysis" \
  --body-file examples/01-stangby-beryllen.md
```

Eller gå till `Issues → New Issue → Investment Analysis` och kopiera fält från
`examples/01-stangby-beryllen.md`.

### 2b. Följ exekveringen

- Actions-fliken visar workflow igång
- Issue får kommentarer från agenterna
- PR med rapport skapas efter ~10-15 min

### 2c. Jämför resultat

Öppna PR:en och jämför med `examples/01-stangby-beryllen.md`. Siffrorna ska
vara inom några procent. Om de skiljer sig betydligt – kolla Actions-loggen.

## Steg 3: Din Riktiga Analys (5 min)

### 3a. Samla information om tomten

Innan du skapar issue, hämta:

- [ ] Tomtens pris (från säljare eller kommunens prospekt)
- [ ] Storlek i kvm
- [ ] Deadline (om sådan finns)
- [ ] URL till officiellt prospekt/annons
- [ ] Eventuell detaljplan-ID
- [ ] Planerad byggnadstyp

### 3b. Prata med eventuell partner

Om partnerskap:

- [ ] Kom överens om kapitalinsatser (exakt belopp per person)
- [ ] Uppskatta arbetstimmar byggherren kommer lägga
- [ ] Diskutera marknadstimpris (500-600 kr/h är typiskt)
- [ ] Välj vinstdelningsmetod (se `partnership/README.md`)

### 3c. Skapa issue

`Issues → New Issue → Investment Analysis`

Fyll i allt du vet. Lämna tomt om du är osäker – agenterna frågar dig.

### 3d. Vänta på analysen

Inom 15-20 min har du:

- Komplett analys i en PR
- PDF-version som artifact
- Agent-kommentarer om beslutspunkter

## Steg 4: Granska och Agera

### Läs rapporten

`Pull Requests → [din PR] → Files changed → final-report.md`

### Diskutera med partner

PR-kommentarer är perfekt för det:

- Kommentera specifika avsnitt
- Ställ uppföljningsfrågor
- `/rerun all` för att köra om analysen från början

### Fatta beslut

- **GO** → Merge:a PR:en, skapa milestones, börja genomförandet
- **STOPP** → Stäng issue utan merge, analysera lärdomar
- **VILLKORLIGT** → Svara på agenternas villkor, kör om

## Vanliga Frågor

### "Agenterna hittar inga priser för mitt område"

Litet/okänt område? Kommentera i issue:

```text
@01-market-research: Jag har kollat Booli och senaste nyproduktion i området var
[X kr/kvm för Y kvm, sålt datum Z]. Använd detta som referens.
```

Och `/rerun all`.

### "Workflow körs inte"

Kontrollera:

1. Finns ditt GitHub-användarnamn i `.github/authorized-users.txt`?
2. Är Copilot Coding Agent aktiverat? (Settings → Copilot)
3. Har issue label `investment-analysis`?
4. Har Actions körrättighet (Settings → Actions → General)?

### "Rapporten är för generell"

Agenterna kan bara vara så specifika som din input. Nästa gång:

- Bifoga prospekt-URL
- Specificera detaljplan-ID
- Fyll i övrig info med markförhållanden

### "Kan jag använda för flera projekt samtidigt?"

Ja. Varje issue = en analys. Använd labels + Projects för att hålla ordning
(se `instructions/github-projects-setup.md`).

## Tips för Effektiv Användning

- Kör `/rerun all` för att starta om analysen med uppdaterat underlag
- Fyll i issue noggrant → färre iterationer
- Använd `meta-template-generator`-agenten en gång, sedan kan du följa samma mönster själv

## Om Något Går Fel

1. **Kolla Actions-loggen** – detaljerade felmeddelanden
2. **Issue-kommentarer** – agenterna flaggar problem där
3. **Eval-rapport på PR** – flaggar matematiska fel
4. **Lokalt test**:

   ```bash
   pip install -e ".[dev]"
   pytest tests/
   ```

Om du fortfarande är fast:

- Öppna en issue med label `bug`
- Beskriv vad du försökte och felmeddelandet
- Bifoga Actions-loggen (redigera bort känsliga värden)

## Nästa Steg När Du Är Förbi Första Analysen

- **Återkommande analyser** – skapa Projects för att spåra pipeline
- **Partnerskap** – läs `partnership/README.md` noggrant, granska avtal med jurist
- **Anpassa agenter** – redigera `agents/NN-name.md` för dina behov
- **Bidra med exempel** – öppna PR med anonymiserade framgångshistorier

Lycka till!
