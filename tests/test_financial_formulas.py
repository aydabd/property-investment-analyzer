"""Tests for the financial formulas used by agents.

These verify the calculation logic in skills/financial-formulas.md
by implementing the same functions here for testing.
"""

from __future__ import annotations

from enum import Enum

import pytest


class SplitMethod(Enum):
    CAPITAL_ONLY = "capital_only"
    WORK_AS_COST = "work_as_cost"
    WORK_AS_VIRTUAL_CAPITAL = "work_as_virtual_capital"


def build_credit_interest(
    monthly_drawdowns: list[float],
    annual_rate: float,
) -> dict:
    """Compute interest cost on a construction loan over build period."""
    cumulative_used = 0.0
    total_interest = 0.0
    schedule = []

    for month, drawdown in enumerate(monthly_drawdowns, start=1):
        avg_used = cumulative_used + (drawdown / 2)
        monthly_interest = avg_used * annual_rate / 12
        total_interest += monthly_interest
        cumulative_used += drawdown
        schedule.append(
            {
                "month": month,
                "drawdown": drawdown,
                "cumulative_used": cumulative_used,
                "avg_balance": avg_used,
                "interest": monthly_interest,
            }
        )

    return {"total": total_interest, "schedule": schedule}


def calculate_roi(
    total_investment: float,
    gross_sales: float,
    selling_costs: float,
    tax_rate: float = 0.22,
) -> dict:
    """Calculate ROI after taxes and selling costs."""
    net_sales = gross_sales - selling_costs
    gross_profit = net_sales - total_investment

    if gross_profit <= 0:
        return {
            "gross_profit": gross_profit,
            "net_profit": gross_profit,
            "roi_pct": (gross_profit / total_investment) * 100,
            "profitable": False,
        }

    tax = gross_profit * tax_rate
    net_profit = gross_profit - tax
    return {
        "gross_profit": gross_profit,
        "tax": tax,
        "net_profit": net_profit,
        "roi_pct": (net_profit / total_investment) * 100,
        "profitable": True,
    }


def split_profit(
    net_profit: float,
    partner_a_capital: float,
    partner_b_capital: float,
    partner_a_hours: float,
    partner_b_hours: float,
    hourly_rate: float,
    method: SplitMethod,
) -> dict:
    """Split profit between two partners using chosen method."""
    total_capital = partner_a_capital + partner_b_capital

    if method == SplitMethod.CAPITAL_ONLY:
        a_share = partner_a_capital / total_capital
        return {
            "partner_a": net_profit * a_share,
            "partner_b": net_profit * (1 - a_share),
            "method": method.value,
        }

    if method == SplitMethod.WORK_AS_COST:
        work_a = partner_a_hours * hourly_rate
        work_b = partner_b_hours * hourly_rate
        remaining = net_profit - work_a - work_b
        a_share = partner_a_capital / total_capital
        return {
            "partner_a": work_a + remaining * a_share,
            "partner_b": work_b + remaining * (1 - a_share),
            "method": method.value,
        }

    if method == SplitMethod.WORK_AS_VIRTUAL_CAPITAL:
        virtual_a = partner_a_capital + partner_a_hours * hourly_rate
        virtual_b = partner_b_capital + partner_b_hours * hourly_rate
        total_virtual = virtual_a + virtual_b
        return {
            "partner_a": net_profit * (virtual_a / total_virtual),
            "partner_b": net_profit * (virtual_b / total_virtual),
            "virtual_capital_a": virtual_a,
            "virtual_capital_b": virtual_b,
            "method": method.value,
        }

    raise ValueError(f"Unknown method: {method}")


class TestBuildCreditInterest:
    """Tests for construction loan interest calculation."""

    def test_zero_drawdown_gives_zero_interest(self) -> None:
        result = build_credit_interest([0, 0, 0], 0.0499)
        assert result["total"] == 0.0

    def test_single_drawdown_interest(self) -> None:
        # 1 MSEK utnyttjat i en månad vid 4,99%
        result = build_credit_interest([1_000_000], 0.0499)
        # Snittsaldo 500k, 500 000 * 0,0499 / 12 ≈ 2 079
        assert 2050 < result["total"] < 2110

    def test_longer_period_higher_cost(self) -> None:
        short = build_credit_interest([1_000_000.0], 0.0499)
        # Samma saldo över två månader = dubbel ränta på saldot
        long = build_credit_interest([1_000_000.0, 0.0], 0.0499)
        assert long["total"] > short["total"]

    def test_schedule_length_matches_months(self) -> None:
        drawdowns: list[float] = [100_000.0] * 14
        result = build_credit_interest(drawdowns, 0.05)
        assert len(result["schedule"]) == 14

    def test_14_month_realistic_scenario(self) -> None:
        # Typisk utbetalningstrappa från skills/financial-formulas.md
        trappa: list[float] = [
            170_000.0,
            80_000.0,
            80_000.0,
            400_000.0,
            2_280_000.0,
            400_000.0,
            550_000.0,
            600_000.0,
            500_000.0,
            400_000.0,
            600_000.0,
            450_000.0,
            350_000.0,
            250_000.0,
        ]
        result = build_credit_interest(trappa, 0.0499)
        # Totala räntan ska ligga i realistisk range (150k-250k)
        assert 150_000 < result["total"] < 250_000


class TestCalculateRoi:
    """Tests for ROI calculation."""

    def test_profitable_project(self) -> None:
        result = calculate_roi(
            total_investment=7_500_000,
            gross_sales=9_400_000,
            selling_costs=235_000,
        )
        assert result["profitable"] is True
        assert result["net_profit"] > 0
        assert 10 < result["roi_pct"] < 25

    def test_loss_project(self) -> None:
        result = calculate_roi(
            total_investment=10_000_000,
            gross_sales=9_000_000,
            selling_costs=250_000,
        )
        assert result["profitable"] is False
        assert result["net_profit"] < 0

    def test_zero_tax_on_loss(self) -> None:
        result = calculate_roi(
            total_investment=10_000_000,
            gross_sales=9_000_000,
            selling_costs=250_000,
        )
        # Förlust ska inte beskattas
        assert "tax" not in result or result.get("tax", 0) == 0

    @pytest.mark.parametrize(
        "tax_rate,expected_roi_approx",
        [
            (0.0, 22.2),  # Utan skatt
            (0.22, 17.3),  # Privat kapitalvinst
            (0.30, 15.5),  # Hög skattesats
        ],
    )
    def test_tax_rate_affects_roi(self, tax_rate: float, expected_roi_approx: float) -> None:
        result = calculate_roi(
            total_investment=7_500_000,
            gross_sales=9_400_000,
            selling_costs=235_000,
            tax_rate=tax_rate,
        )
        assert abs(result["roi_pct"] - expected_roi_approx) < 0.5


class TestSplitProfit:
    """Tests for partner profit splitting methods."""

    def test_capital_only_equal_shares(self) -> None:
        result = split_profit(
            net_profit=1_000_000,
            partner_a_capital=500_000,
            partner_b_capital=500_000,
            partner_a_hours=0,
            partner_b_hours=0,
            hourly_rate=500,
            method=SplitMethod.CAPITAL_ONLY,
        )
        assert result["partner_a"] == 500_000
        assert result["partner_b"] == 500_000

    def test_capital_only_unequal_shares(self) -> None:
        result = split_profit(
            net_profit=1_000_000,
            partner_a_capital=700_000,
            partner_b_capital=300_000,
            partner_a_hours=0,
            partner_b_hours=0,
            hourly_rate=500,
            method=SplitMethod.CAPITAL_ONLY,
        )
        assert result["partner_a"] == pytest.approx(700_000)
        assert result["partner_b"] == pytest.approx(300_000)

    def test_work_as_cost_compensates_builder(self) -> None:
        result = split_profit(
            net_profit=1_200_000,
            partner_a_capital=500_000,
            partner_b_capital=500_000,
            partner_a_hours=0,
            partner_b_hours=1_000,
            hourly_rate=500,
            method=SplitMethod.WORK_AS_COST,
        )
        # B ska få minst sin arbetslön (500 000)
        assert result["partner_b"] >= 500_000
        # Eftersom remaining = 1 200 000 - 500 000 = 700 000 delas 50/50
        # B: 500 000 + 350 000 = 850 000
        # A: 0 + 350 000 = 350 000
        assert result["partner_a"] == pytest.approx(350_000, rel=0.01)
        assert result["partner_b"] == pytest.approx(850_000, rel=0.01)

    def test_virtual_capital_splits_proportionally(self) -> None:
        result = split_profit(
            net_profit=1_000_000,
            partner_a_capital=500_000,
            partner_b_capital=500_000,
            partner_a_hours=0,
            partner_b_hours=1_000,  # 500 000 kr virtuellt
            hourly_rate=500,
            method=SplitMethod.WORK_AS_VIRTUAL_CAPITAL,
        )
        # A: 500k virtuellt / 1 500k total = 33,3%
        # B: 1 000k virtuellt / 1 500k total = 66,7%
        assert result["partner_a"] == pytest.approx(333_333, rel=0.01)
        assert result["partner_b"] == pytest.approx(666_667, rel=0.01)

    def test_all_methods_total_to_net_profit(self) -> None:
        params = {
            "net_profit": 1_200_000,
            "partner_a_capital": 760_000,
            "partner_b_capital": 750_000,
            "partner_a_hours": 50,
            "partner_b_hours": 1_950,
            "hourly_rate": 500,
        }
        for method in SplitMethod:
            result = split_profit(method=method, **params)
            total = result["partner_a"] + result["partner_b"]
            assert total == pytest.approx(params["net_profit"], rel=0.001), (
                f"{method.value}: total {total} != net profit {params['net_profit']}"
            )
