# 📊 Investeringsanalys: {{issue:kommun}} – {{issue:område}}

**Analysdatum**: {{meta:date}}
**Fastighet**: {{issue:fastighetsbeteckning}}
**Issue**: #{{meta:issue_number}}
**Strategi**: Bygg-och-sälj (uthyrning ingår ej)

---

## 🎯 Sammanfattning

<!-- Optimizer fyller i 3-4 rader här -->

{{agent:07-optimizer}}

---

## 📍 1. Marknadsanalys

_Ortspriser, värdeutveckling, efterfrågan_

{{agent:01-market-research}}

---

## 🏞️ 2. Tomtanalys

_Detaljplan, kommunala krav, tekniska förutsättningar_

{{agent:02-plot-analysis}}

---

## 🏗️ 3. Byggkostnad

_Detaljerad kostnadsuppdelning – egen entreprenad med material direktinköp_

{{agent:03-build-cost}}

---

## 💰 4. Finansiering

_Kapitalstruktur, räntekostnad under byggtid, skatt_

{{agent:04-financing}}

---

## 🤝 5. Partnerskap

_Kapital-/arbetsfördelning, vinstdelning, beslutsmandat_

{{#if agent:06-partnership}}
{{agent:06-partnership}}
{{else}}
_Ej tillämpligt — enskild investerare._
{{/if}}

---

## ⚠️ 6. Riskanalys

_Planrätt, marknad, bygge, finansiering, partnerskap_

{{agent:05-risk}}

---

## ✅ 7. Slutbeslut och Handlingsplan

_Orchestrator-syntes + 30-dagars plan_

{{agent:00-orchestrator}}

---

## 📎 Bilagor

### Underlag

- Issue med ursprunglig data: #{{meta:issue_number}}
- Agent-outputs (råa): `analyses/issue-{{meta:issue_number}}/agent-outputs/`
- Partnerskapsavtal (mall): `partnership/agreement-template.md`

### Använda datakällor

<!-- Listas automatiskt från agent-outputs -->

### Antaganden som kräver verifiering

<!-- Orchestrator sammanställer -->

---

## 🔄 Revideringshistorik

| Version | Datum         | Ändring        |
| ------- | ------------- | -------------- |
| 1.0     | {{meta:date}} | Första version |

---

## ⚖️ Förbehåll

Denna analys är **inte** finansiell rådgivning. Den är ett beslutsunderlag baserat på
aktuell data och rimliga antaganden. Verifiera alltid kritiska siffror innan bindande
beslut. Konsultera:

- **Revisor** för skatteoptimering per person/bolag
- **Fastighetsjurist** för partnerskapsavtal och fastighetsjuridik
- **Bank** för exakta lånevillkor
- **Kommunens bygglovsavdelning** för planrättsliga frågor

---

_Rapport genererad av Property Investment Planner via GitHub Actions._
_Repo: `{{meta:repo}}` | Commit: `{{meta:sha}}`_
