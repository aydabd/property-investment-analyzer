# Partnerskapsmodellen – Investerare + Byggherre

Denna modell hanterar ett specifikt scenario: **en passiv investerare och en aktiv
byggherre samarbetar om ett bygg-och-sälj-projekt**.

## Klassisk Problembild

Utan tydlig struktur uppstår tvister:

- "Jag gjorde jobbet, jag borde få mer"
- "Du satsade inget eget arbete, du tar ingen risk"
- "Det blev dyrare än tänkt – vem betalar?"
- "Jag vill sälja nu, du vill vänta"

Den här modellen **förebygger** dessa genom att göra allt explicit i förväg.

## De Tre Vinstdelningsmetoderna

### Metod 1: Rent Kapitalproportionellt

```text
Båda parter bidrar med samma EK → delar 50/50.
Byggherrens arbete är "oavlönat".
```

**När det fungerar**: Om byggherren bidrar med MYCKET mindre kapital (t.ex. 20%)
och därför får acceptabel "lön" via sin stora procentandel av vinsten.

**När det inte fungerar**: Asymmetri mellan kapital och arbete.

### Metod 2: Arbete Kompenseras Som Kostnad

```text
Byggherren tar ut marknadslön för sitt arbete som en projektkostnad.
Resterande vinst delas kapital-proportionellt.
```

**Fördel**: Transparent, byggherrens arbete syns i kalkylen.
**Nackdel**: Minskar bruttovinsten, lägre ROI på papper.

### Metod 3: Arbete Som Virtuellt Kapital (rekommenderas oftast)

```
Byggherrens arbetsinsats omräknas till "virtuellt kapital"
(timmar × marknadstimpris). Total virtuellt kapital används för
att beräkna vinstandelar.
```

**Fördel**: Belönar både kapital och arbete proportionellt.
**Nackdel**: Kräver att parterna enas om marknadstimpriset.

## Praktiskt Räkneexempel

### Utgångsläge

- Total projektkostnad: 7 600 000 kr
- EK-behov (20%): 1 520 000 kr
- Förväntad nettovinst: 1 200 000 kr
- Partner A (Investerare): bidrar 760 000 kr EK, 0 timmar
- Partner B (Byggherre): bidrar 760 000 kr EK + 2 000 timmar arbete
- Marknadstimpris överenskommen: 500 kr/h

### Metod 3 (Virtuellt Kapital) – Uträkning

```text
Partner A:s virtuellt kapital:
  760 000 + (0 × 500) = 760 000 kr

Partner B:s virtuellt kapital:
  760 000 + (2 000 × 500) = 760 000 + 1 000 000 = 1 760 000 kr

Total virtuellt kapital:
  760 000 + 1 760 000 = 2 520 000 kr

Andelar:
  Partner A: 760 000 / 2 520 000 = 30,2%
  Partner B: 1 760 000 / 2 520 000 = 69,8%

Vinstfördelning (1 200 000 kr):
  Partner A: 30,2% × 1 200 000 = 362 400 kr
  Partner B: 69,8% × 1 200 000 = 837 600 kr
```

### Sanity Check (rimlighetstest)

```text
Partner A avkastning på 760 000 EK: 47,7% under 14 månader
  → Annualiserat 40,9% ← bra passivt!

Partner B avkastning:
  - På EK (760 000 kr): samma 47,7%
  - På arbete (2 000 h): 837 600 / 2 000 = 418 kr/h
    (under deras marknadstimpris 500 kr/h men plus kapitalavkastning)

  Alternativ: om hade lönearbetat 2 000 h × 500 kr/h = 1 000 000 kr
  Och tagit 760 000 × 47,7% avkastning på kapital = 362 520 kr
  Summa: 1 362 520 kr

  I partnerskapet får B: 837 600 kr (MINDRE)

  → Metod 3 är orättvis mot B i detta fall!
```

### Iteration

Vid nästa förhandling bör parterna justera marknadstimpriset eller välja Metod 2
istället. Detta är just poängen — genom att visa siffror tidigt undviks senare tvister.

## Justerad Metod 2 (Arbete Som Kostnad)

```
Partner B:s arbetskompensation: 2 000 × 500 = 1 000 000 kr
  (Detta är EN KOSTNAD i projektet före vinstdelning)

Vinst efter arbetskompensation:
  Projekt: 9 400 000 - 7 600 000 - 264 000 (mäklare) = 1 536 000 kr brutto
  Efter skatt 22%: 1 198 000 kr
  Efter B:s arbetskomp: 198 000 kr

Resterande 198 000 kr delas kapital-proportionellt (50/50):
  A: 99 000 kr
  B: 99 000 kr

Total till B: 1 000 000 + 99 000 = 1 099 000 kr
Total till A: 99 000 kr

→ Nu får B nästan "full lön" + lite vinst.
→ Nu får A bara 99 000 kr, vilket är 13% på 14 månader = 11% annualiserat.
   Inte fantastiskt men säkert och passivt.
```

## Vilken Metod Ska Du Välja?

```python
def recommend_method(kapital_ratio_A, arbete_timmar_A, arbete_timmar_B):
    ratio = kapital_ratio_A  # Partner A:s kapital-andel
    work_diff = arbete_timmar_B - arbete_timmar_A

    if work_diff < 200:  # Ungefär lika arbete
        return "Metod 1 (rent kapitalproportionellt)"

    if work_diff > 1500:  # Stor asymmetri
        return "Metod 2 (arbete som kostnad) – skyddar byggherren"

    # Medium asymmetri
    return "Metod 3 (virtuellt kapital) – kräver noggrann kalkyl"
```

## Vanliga Misstag

1. **Oklart marknadstimpris**: Avtala i förväg, inte i efterhand
2. **"Vi litar på varandra"**: Skriv ändå ner allt – skyddar båda
3. **Inga stoppklausuler**: Vad händer om projektet går dåligt?
4. **Glömmer skatteoptimering per part**: Olika ägarstrukturer kan ge olika skatt
5. **Informella beslutsmandat**: Nödvändigt att skriva RACI

## Innan Ni Signerar

- [ ] Båda har läst hela avtalet
- [ ] Vinstdelningsmetod är vald och beräknad
- [ ] Marknadstimpris är överenskommet (om tillämpligt)
- [ ] RACI-matris är granskad
- [ ] Kostnadsöverskridnings-regler är OK
- [ ] Exit-regler är kollade av jurist
- [ ] Försäkringar är tecknade
- [ ] Bankindikation är klar

## Mallarna

- `agreement-template.md` – fullständigt avtal att signera
- `raci-matrix.md` – separat, granskas ofta iterativt
- `monthly-report-template.md` – B:s rapport till A

---

Detta avtal är en STARTPUNKT, inte slutpunkt. Anpassa per ditt specifika scenario
och låt en fastighetsjurist granska det sista steget. Kostnaden för juristgranskning
(~10 000–20 000 kr) är försumbar jämfört med att hamna i domstol.
