# Skill: Finansiella Beräkningsmallar

Generiska formler och referenser som agenterna använder. Inga hårdkodade platser.

## Räntekostnad Byggkreditiv (månadsvis)

Byggkreditiv debiterar ränta bara på **utnyttjat belopp**, inte beviljad kredit.

```python
def build_credit_interest(
    monthly_drawdowns: list[float],  # hur mycket utnyttjas varje månad
    annual_rate: float,               # t.ex. 0.0499 för 4,99%
) -> dict:
    cumulative_used = 0.0
    total_interest = 0.0
    schedule = []

    for month, drawdown in enumerate(monthly_drawdowns, start=1):
        avg_used = cumulative_used + (drawdown / 2)  # mitt-av-månad approx
        monthly_interest = avg_used * annual_rate / 12
        total_interest += monthly_interest

        cumulative_used += drawdown
        schedule.append({
            "month": month,
            "drawdown": drawdown,
            "cumulative_used": cumulative_used,
            "avg_balance": avg_used,
            "interest": monthly_interest,
        })

    return {"total": total_interest, "schedule": schedule}
```

### Typisk Utbetalningstrappa (fribyggartomt, 14 mån)

```python
# Generisk trappa - anpassa per projekt
drawdown_pattern = {
    1:  170_000,   # projektering, bygglov-handläggning
    2:   80_000,   # arkitekt, KA-upphandling
    3:   80_000,   # bygglovsansökan komplettering
    4:  400_000,   # mark, grundarbete
    5: 2_280_000,  # GRUND KLAR → tomtpris betalas (typisk kommunal fribyggartomt)
    6:  400_000,   # stomme reses
    7:  550_000,   # tak, klimatskal tätt
    8:  600_000,   # fasad, fönster
    9:  500_000,   # el/VS rörläggning
   10:  400_000,   # invändiga väggar
   11:  600_000,   # kök, bad
   12:  450_000,   # ytskikt
   13:  350_000,   # slutinstallationer
   14:  250_000,   # besiktning, smårester
}
```

## ROI-beräkning

```python
def calculate_roi(
    total_investment: float,
    gross_sales: float,
    selling_costs: float,  # mäklare + styling
    tax_rate: float = 0.22,
) -> dict:
    net_sales = gross_sales - selling_costs
    gross_profit = net_sales - total_investment

    if gross_profit <= 0:
        return {
            "gross_profit": gross_profit,
            "tax": 0.0,
            "net_profit": gross_profit,  # ingen skatt på förlust
            "roi_pct": (gross_profit / total_investment) * 100 if total_investment > 0 else 0.0,
            "profitable": False,
        }

    tax = gross_profit * tax_rate
    net_profit = gross_profit - tax
    roi_pct = (net_profit / total_investment) * 100

    return {
        "gross_profit": gross_profit,
        "tax": tax,
        "net_profit": net_profit,
        "roi_pct": roi_pct,
        "profitable": True,
    }


def annualize_roi(roi_pct: float, months: int) -> float:
    """Konvertera projekt-ROI till årlig."""
    if months <= 0:
        raise ValueError("months must be > 0")
    return roi_pct * (12 / months)
```

## Partnerskaps-vinstdelning (tre metoder)

```python
from enum import Enum

class SplitMethod(Enum):
    CAPITAL_ONLY = "capital_only"
    WORK_AS_COST = "work_as_cost"
    WORK_AS_VIRTUAL_CAPITAL = "work_as_virtual_capital"


def split_profit(
    net_profit: float,
    partner_a_capital: float,
    partner_b_capital: float,
    partner_a_hours: float,
    partner_b_hours: float,
    hourly_rate: float,  # marknadstimpris för byggherren
    method: SplitMethod,
) -> dict:
    total_capital = partner_a_capital + partner_b_capital

    if method == SplitMethod.CAPITAL_ONLY:
        if total_capital <= 0:
            raise ValueError("total_capital must be > 0 for CAPITAL_ONLY")
        a_share = partner_a_capital / total_capital
        return {
            "partner_a": net_profit * a_share,
            "partner_b": net_profit * (1 - a_share),
            "method": method.value,
        }

    if method == SplitMethod.WORK_AS_COST:
        if total_capital <= 0:
            raise ValueError("total_capital must be > 0 for WORK_AS_COST")
        work_comp_a = partner_a_hours * hourly_rate
        work_comp_b = partner_b_hours * hourly_rate

        remaining = net_profit - work_comp_a - work_comp_b
        a_share = partner_a_capital / total_capital

        return {
            "partner_a": work_comp_a + remaining * a_share,
            "partner_b": work_comp_b + remaining * (1 - a_share),
            "work_compensation_total": work_comp_a + work_comp_b,
            "method": method.value,
        }

    if method == SplitMethod.WORK_AS_VIRTUAL_CAPITAL:
        virtual_a = partner_a_capital + partner_a_hours * hourly_rate
        virtual_b = partner_b_capital + partner_b_hours * hourly_rate
        total_virtual = virtual_a + virtual_b
        if total_virtual <= 0:
            raise ValueError("total_virtual must be > 0 for WORK_AS_VIRTUAL_CAPITAL")

        return {
            "partner_a": net_profit * (virtual_a / total_virtual),
            "partner_b": net_profit * (virtual_b / total_virtual),
            "virtual_capital_a": virtual_a,
            "virtual_capital_b": virtual_b,
            "method": method.value,
        }
```

## Sensitivity Matrix

```python
def sensitivity_analysis(
    base_params: dict,
    variable: str,
    variations: list[float],  # t.ex. [-0.10, -0.05, 0, 0.05, 0.10]
) -> list[dict]:
    results = []
    base_value = base_params[variable]

    for variation in variations:
        new_params = base_params.copy()
        new_params[variable] = base_value * (1 + variation)
        # Återuppräkna ROI med nya parametrar
        roi = calculate_roi(...)  # anpassa efter variabel
        results.append({
            "variation_pct": variation * 100,
            "new_value": new_params[variable],
            "roi_pct": roi["roi_pct"],
        })

    return results
```

## Break-even-beräkningar

```python
def break_even_sales_price(
    total_investment: float,
    selling_cost_pct: float = 0.025,
    tax_rate: float = 0.22,
    target_roi: float = 0.0,  # 0 = bara täcka kostnaden
) -> float:
    """
    Lägsta försäljningspris som ger target_roi efter skatt och mäklare.
    """
    if not (0 <= selling_cost_pct < 1):
        raise ValueError("selling_cost_pct must be in [0, 1)")
    if not (0 <= tax_rate < 1):
        raise ValueError("tax_rate must be in [0, 1)")
    if total_investment <= 0:
        raise ValueError("total_investment must be > 0")
    # net_profit / investment = target_roi
    # net_profit = gross_profit * (1 - tax_rate)
    # gross_profit = net_sales - total_investment
    # net_sales = gross_sales * (1 - selling_cost_pct)

    target_net_profit = total_investment * target_roi
    required_gross_profit = target_net_profit / (1 - tax_rate)
    required_net_sales = total_investment + required_gross_profit
    required_gross_sales = required_net_sales / (1 - selling_cost_pct)

    return required_gross_sales


def break_even_interest_rate(
    total_investment_excl_interest: float,
    gross_sales: float,
    selling_cost_pct: float = 0.025,
    tax_rate: float = 0.22,
    build_months: int = 14,
) -> float:
    """
    Högsta byggkredit-ränta där projektet precis går jämnt ut (ROI = 0).
    """
    if not (0 <= selling_cost_pct < 1):
        raise ValueError("selling_cost_pct must be in [0, 1)")
    if not (0 <= tax_rate < 1):
        raise ValueError("tax_rate must be in [0, 1)")
    if build_months <= 0:
        raise ValueError("build_months must be > 0")
    if total_investment_excl_interest <= 0:
        raise ValueError("total_investment_excl_interest must be > 0")
    net_sales = gross_sales * (1 - selling_cost_pct)
    # ROI 0% ⇒ gross_profit efter skatt = 0 ⇒ gross_profit = 0
    # gross_profit = net_sales - total_investment
    # total_investment = total_investment_excl_interest + interest_cost
    max_interest_cost = net_sales - total_investment_excl_interest
    # interest_cost ≈ avg_balance * rate * (build_months/12)
    # avg_balance ≈ total_investment_excl_interest / 2
    avg_balance = total_investment_excl_interest / 2
    return (max_interest_cost / avg_balance) * (12 / build_months)
```

## Skatte-scenarier (generiska)

```python
# Sverige-specifika konstanter (verifiera i Skatteverkets aktuella regler)
CAPITAL_GAINS_TAX_PRIVATE = 0.22
CORPORATE_TAX = 0.206
DIVIDEND_TAX_3_12 = 0.20
UPPSKOV_MAX = 3_000_000

# Ränteavdrag
DEDUCTION_LIMIT = 100_000
DEDUCTION_RATE_UNDER_LIMIT = 0.30
DEDUCTION_RATE_OVER_LIMIT = 0.21


def tax_on_sale_private(profit: float) -> float:
    return profit * CAPITAL_GAINS_TAX_PRIVATE


def tax_on_sale_with_uppskov(profit: float, reinvest_in_new_home: bool) -> float:
    if not reinvest_in_new_home:
        return tax_on_sale_private(profit)
    # Uppskov upp till 3 MSEK kan skjutas upp
    deferred = min(profit, UPPSKOV_MAX)
    taxable_now = profit - deferred
    return taxable_now * CAPITAL_GAINS_TAX_PRIVATE


def tax_on_sale_via_ab(profit: float, take_out_as_dividend: bool) -> float:
    corporate_tax = profit * CORPORATE_TAX
    remaining = profit - corporate_tax

    if take_out_as_dividend:
        dividend_tax = remaining * DIVIDEND_TAX_3_12
        return corporate_tax + dividend_tax

    return corporate_tax  # Pengar stannar i bolaget
```

## Användning av denna skill

Agenter (särskilt `04-financing`, `06-partnership`, `07-optimizer`) kan referera till
dessa formler. Agenterna behöver inte exekvera Python-kod — de använder formlerna
som mental modell och skriver ut siffrorna i sin output.

Om framtida versioner kör Python-kod aktivt via workflow kan funktionerna ovan
direkt importeras.
