# Skill: Datakällor för Svenska Investeringsanalyser

## Syfte

Lista av verifierade, uppdaterade källor agenterna kan använda för att hämta
aktuell data. Uppdateras när källor ändras.

## Marknadsdata (Priser, Hyror)

### Officiella Källor

- **SCB** – befolkning, inkomster, byggkostnadsindex (scb.se)
- **Boverket** – bostadsmarknadsanalyser
- **Lantmäteriet** – fastighetsregister, taxeringsvärden

### Marknadsstatistik

- **Booli** – försäljningsstatistik (booli.se)
- **Mäklarstatistik** (maklarstatistik.se)
- **Hemnet** – aktuella annonser
- **Svensk Mäklarstatistik** – kvartalsrapporter

## Räntor och Finansmarknad

### Banker (byggkreditiv)

- **Nordea** (nordea.se/privat/produkter/bolan/byggnadskredit.html)
- **Swedbank** (swedbank.se)
- **SEB** (seb.se)
- **Länsförsäkringar** (lansforsakringar.se)
- **Handelsbanken** (handelsbanken.se)

### Prognoser

- **Riksbanken** – styrränta (riksbank.se)
- **Handelsbanken** – bostadsmarknadsprognoser
- **SBAB** – ränteprognoser (sbab.se)

## Kommunala Data

### Per kommun

Agenter bör alltid söka:

- `[kommunnamn].se/bygga-och-bo` – bygglov, tomter, VA
- `[kommunnamn].se/stadsutveckling` – detaljplaner
- `[kommunnamn].se/bygglovstaxa` – avgifter

### VA-avgifter

- **VA SYD** (Lund, Malmö, Burlöv, Eslöv, Lomma) – vasyd.se
- **Stockholm Vatten och Avfall** – stockholmvattenochavfall.se
- **Göteborg Vatten**
- Kommunspecifika taxadokument (PDF)

### Elnät

- **E.ON Energidistribution** (södra/västra Sverige)
- **Vattenfall Eldistribution**
- **Ellevio** (Stockholm, Dalarna, Värmland)
- **Skånska Energi Nät** (delar av Skåne)
- Sök: `[kommun] elnät`

## Byggkostnader

### Referenspriser

- **Byggstart** (byggstart.se) – aktuella snittpriser villa
- **Nyckelfardigthus.se** – prisstatistik
- **Byggföretagen** – BKI (byggkostnadsindex)

### Material-leverantörer (direktpriser)

- **Ahlsell** – el-, VVS-material
- **Derome** – stomme, trävaror
- **Moelven** – stomme
- **Benders** – betong, tak, fasad
- **Byggmax / Bauhaus** – konsumentpris (som referens)

## Skatte- och Juridisk Information

- **Skatteverket** (skatteverket.se)
  - Kapitalvinstskatt
  - Ränteavdrag
  - Uppskov
- **Boverket** – PBL, BBR
- **Lantmäteriet** – fastighetsdelning, servitut

## Konsumentvägledning

- **Villaägarna** (villaagarna.se) – bevakar hushållsfrågor
- **Konsumenternas försäkringsbyrå** – försäkringar

## Hur Agenter Ska Använda Dessa

### Prioritetsordning

1. **Officiella kommunala prospekt** (verifierade källor)
2. **Banker och finansinstitut** (för räntor)
3. **Statliga myndigheter** (SCB, Boverket, Skatteverket)
4. **Etablerade marknadsstatistik-tjänster** (Booli, Mäklarstatistik)
5. **Byggbranschens statistik** (Byggföretagen, Byggstart)

### Undvik

- Bloggar och privatpersoners uppgifter
- Gamla artiklar (> 12 mån)
- "Uppskattningar" utan källa
- Generiska internationella siffror

### Citat-regler

När agent levererar siffra:

```markdown
Priset X kr [källa: VA SYD taxa 2026, hämtad YYYY-MM-DD]
```

## När Data Saknas

Om ingen tillförlitlig källa hittas:

1. Ställ fråga till användaren om de kan verifiera lokalt
2. Använd närmaste liknande område/kommun som proxy
3. Ange tydligt att det är en approximation
4. Flagga osäkerheten i riskanalysen

## Sök-tips per Datatyp

```yaml
tomtpris:
  query: "[kommun] fribyggartomt pris [område]"
  fallback: "[kommun] kommunal tomt"

va_avgift:
  query: "VA-taxa [kommun] 2026 anläggningsavgift"
  fallback: "[kommun] vattentjänstplan"

bygglovsavgift:
  query: "bygglovstaxa [kommun] 2026"

byggkreditivsränta:
  query: "byggnadskredit ränta [bank] 2026"

marknadshyror:
  query: "hyresrätt [stad] nyproduktion pris kvm"
  fallback: "bostadsannonser [stad] hyra"

ortspris:
  query: "slutpris villa [område] nyproduktion"
  via_booli: "booli.se/hitta/slutpriser"
```
