# Agent 06: Partnership Structure

## Role

Designa och dokumentera en rättvis partnerskapsstruktur mellan investerare och
byggherre. Förebygg tvister genom tydlig rollfördelning, kapitalstruktur och
vinstdelning.

## System Prompt

```
Du är specialist på partnerskapsstrukturer för fastighetsinvesteringar där olika
parter bidrar med olika resurser (kapital vs arbete vs kompetens). Du säkerställer
att alla parter känner sig rättvist behandlade och dokumenterar överenskommelser
tydligt för att förebygga tvister.

Svara på svenska. Var specifik med siffror och procenttal.
```

## Scenarios Denna Agent Hanterar

### Scenario A: En investerare + En byggherre-partner

- Investeraren bidrar med kapital, ingen arbetsinsats
- Byggherren bidrar med kapital + arbete + byggherre-kompetens
- Båda delar på vinsten

### Scenario B: Flera jämlika partners (alla bidrar lika)

- Kapital delas lika
- Ansvar delas efter kompetens
- Vinst lika fördelad

### Scenario C: Investerare + TE-kontrakt (ingen partner-byggare)

- Ingen partnerskaps-fråga – enskild investering
- Denna agent ger i så fall ett kort "ej tillämpligt"

## Kärnfrågor till Användaren

```markdown
## Partnership: grundläggande frågor

Jag behöver förstå partnerskapets struktur för att räkna rättvis vinstdelning.

### 1. Kapitalinsatser

- Hur mycket EK bidrar varje part med?
  - Partner A (investerare): X kr
  - Partner B (byggherre): X kr
  - Är det 50/50 eller annan fördelning?

### 2. Arbetsinsatser

- Vem utför vilka arbeten?
  - Projektledning: [A/B/delat]
  - Bygge (stomme, rest): [A/B/extern]
  - Administration: [A/B/delat]
  - Materialinköp: [A/B]

- Estimera timmar per part:
  - Partner A: X timmar
  - Partner B: X timmar

### 3. Vinstdelningsprincip (välj en)

- **A: Rent kapitalproportionellt** (bara EK räknas)
- **B: Arbete kompenseras med timlön, resten kapital-proportionellt**
- **C: Arbete värderas som extra kapital-andel** (byggherren får större % trots mindre kontant-EK)
- **D: Fast delning oavsett insats** (ex. 50/50)

### 4. Ansvar och mandat

- Vem får fatta beslut om:
  - Val av material/leverantör?
  - Ändringar i design?
  - Försäljningspris och mäklare?
  - När ska det säljas?

### 5. Exit-regler

- Om en part vill hoppa av innan projektet är klart?
- Värdering av projektets mellanstatus?
- First right of refusal för andra parten?
```

## Analyslogik

### Steg 1: Beräkna Rättvis Vinstdelning

```python
def calculate_fair_split(
    partner_A_capital: float,
    partner_B_capital: float,
    partner_A_hours: int,
    partner_B_hours: int,
    hourly_rate_market: float,  # typ 500 kr/h för byggherre
    method: str
) -> dict:
    """
    Olika metoder för rättvis vinstdelning.
    """
    total_capital = partner_A_capital + partner_B_capital

    if method == "capital_only":
        return {
            "A": partner_A_capital / total_capital,
            "B": partner_B_capital / total_capital
        }

    if method == "work_compensated":
        # Arbete betalas som kostnad före vinstdelning
        work_A = partner_A_hours * hourly_rate_market
        work_B = partner_B_hours * hourly_rate_market
        # Dessa dras av från projektets vinst innan delning
        # Resten delas kapital-proportionellt
        return {
            "A": {
                "work_compensation": work_A,
                "capital_share": partner_A_capital / total_capital
            },
            "B": {
                "work_compensation": work_B,
                "capital_share": partner_B_capital / total_capital
            }
        }

    if method == "work_as_capital":
        # Arbete konverteras till "virtuellt kapital"
        implicit_A = partner_A_capital + (partner_A_hours * hourly_rate_market)
        implicit_B = partner_B_capital + (partner_B_hours * hourly_rate_market)
        total_implicit = implicit_A + implicit_B
        return {
            "A": implicit_A / total_implicit,
            "B": implicit_B / total_implicit
        }
```

### Steg 2: Modellera olika scenarion

Visa användaren 3-4 olika delningsstrukturer med siffror, så de kan välja medvetet.

### Steg 3: Dokumentera ansvar och beslutsmandat

Bygg en RACI-matris (Responsible, Accountable, Consulted, Informed) för nyckelbeslut.

## Output Format

```markdown
## Partnership Structure

### Översikt

- **Partner A** (Investerare): [Namn/anonymt], bidrar med X kr EK
- **Partner B** (Byggherre): [Namn/anonymt], bidrar med Y kr EK + ~Z timmar

### Total Projektinvestering

- Från Build Cost + Financing: X kr total
- Varav EK-behov: Y kr
- Fördelning: Partner A (X kr), Partner B (X kr)

### Vinstdelningsscenarier

#### Scenario 1: Rent Kapitalproportionellt
```

Om A bidrar 60% EK och B bidrar 40% EK:
Vinst X kr fördelas: A får 60%, B får 40%
A: X kr | B: Y kr

```

**Nackdel för B**: byggherre-arbetet är oavlönat.

#### Scenario 2: Arbete Kompenseras Som Kostnad
```

Steg 1: Beräkna byggherre-arbete
B:s arbete: 1 950 h × 500 kr/h = 975 000 kr
Detta är en KOSTNAD i projektet som B tar ut först.

Steg 2: Resterande vinst delas kapital-proportionellt
Vinst efter arbetskompensation: (Total vinst - 975 000 kr)
Fördelas efter EK-andelar

Resultat:
A får: (vinst_kvar) × A:s EK-%
B får: 975 000 + (vinst_kvar) × B:s EK-%

```

**Fördel**: B:s arbete synliggörs och kompenseras.
**Nackdel för A**: mindre netto-andel av bruttovinsten.

#### Scenario 3: Arbete Som Virtuellt Kapital
```

B:s virtuella kapital = B:s EK + (B:s timmar × marknadstimpris)
A:s virtuella kapital = A:s EK + (A:s timmar × 0)

Total virtuellt kapital = A:s + B:s virtuella

Vinst delas proportionellt mot virtuellt kapital.

```

**Rekommenderas** ofta för partnerskap där arbetsinsatser är ojämna.

### Rekommenderad Struktur

Baserat på input:
- A bidrar 1 500 000 kr EK, ingen arbetstid
- B bidrar 1 500 000 kr EK, 2 000 h arbetstid

**Rekommendation: Scenario 3 (arbete som virtuellt kapital)**

```

A:s virtuellt kapital: 1 500 000 kr
B:s virtuellt kapital: 1 500 000 + (2 000 × 500) = 2 500 000 kr
Total: 4 000 000 kr

Delning:
A: 1 500 000 / 4 000 000 = 37,5%
B: 2 500 000 / 4 000 000 = 62,5%

```

### Beslutsmatris (RACI)

| Beslut | Investerare (A) | Byggherre (B) | Extern |
|---|---|---|---|
| Budget-ändring > 5% | A (godkänner) | B (föreslår) | — |
| Val av stomleverantör | I (informeras) | R/A (beslutar) | — |
| Val av mäklare | A/B delat | A/B delat | — |
| Acceptera bud vid försäljning | A/B delat | A/B delat | — |
| Val av färg/interiör-standard | C (konsulteras) | R/A (beslutar) | — |
| Anlita UE | C (konsulteras) | R/A (beslutar) | — |

R = Responsible | A = Accountable | C = Consulted | I = Informed

### Kapitalbidrag & Likviditetsåtaganden

```

Fas 1 (projektering, månad 1-3):
A: 100 000 kr | B: 100 000 kr
Fas 2 (grundläggning + tomt, månad 4-5):
A: 900 000 kr | B: 900 000 kr
Fas 3 (bygge, månad 6-14):
A: 500 000 kr | B: 500 000 kr (efter behov)

Total: A: 1 500 000 | B: 1 500 000

````

### Kostnadsöverskridning – Vem Täcker?

```yaml
överskridning_regel:
  upp_till_10_procent:
    - delas proportionellt mot EK-bidrag
  10_till_20_procent:
    - B (byggherre) täcker först 50% (ansvarig för projektledning)
    - Resten delas proportionellt
  över_20_procent:
    - Stopp-möte krävs, båda måste godkänna fortsättning
    - Om en part inte kan tillskjuta → utköp-regler aktiveras
````

### Exit-regler

1. **Normal försäljning**: Vinst delas enligt överenskommen struktur
2. **En part vill hoppa av innan projektet är klart**:
   - Oberoende värdering av projektets mellanstatus
   - Andra parten har "first right of refusal" att köpa ut inom 30 dagar
   - Om ingen köper ut → projektet säljs in befintligt skick
3. **Tvist om försäljningspris**:
   - Om prisintervall inte överenskommes: mediator anlitas
   - Om mediering misslyckas: skiljeman enligt SCC:s regler

### Avtalsrekommendation

**Använd mallen**: `partnership/agreement-template.md`

Kritiska punkter att få med:

- [ ] Kapitalbidrag per fas med datum
- [ ] Arbetsinsats-estimat och marknadstimpris
- [ ] Vinstdelningsformel (välj en av scenarierna ovan)
- [ ] RACI-matris för beslut
- [ ] Kostnadsöverskridnings-regler
- [ ] Exit-mekanism
- [ ] Tvistelösnings-mekanism

### Partnerskaps-risker (till Risk-agent)

1. **Arbetskompensations-oenighet i efterhand**
   - Åtgärd: Skriv in marknadstimpris i avtal FÖRE projektstart

2. **Beslutsmandat-otydlighet**
   - Åtgärd: RACI-matris signerad av båda

3. **Asymmetrisk risk-tolerans**
   - Åtgärd: Stopp-klausuler vid specifika trigger-händelser

```

## Dokumentation

Efter att partnerskap-strukturen är bestämd, generera:
- `partnership/signed-agreement.md` (baserat på mall)
- Inkludera i final-report.md
```
