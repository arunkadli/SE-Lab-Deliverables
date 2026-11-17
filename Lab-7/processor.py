"""Validated loan payment and eligibility calculations for Lab 7.

This project was assembled from the Lab 7 handout because the assigned GitHub
repository did not contain fetchable starter files. The rules are intentionally
simple and documented in README.md; they are for a classroom exercise only.
"""

from __future__ import annotations

import math
from numbers import Real


def _number(value: object, field: str, *, minimum: float, strict: bool = False) -> float:
    """Return a finite numeric value or raise a clear validation error."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{field} must be a number")
    try:
        result = float(value)
    except (OverflowError, ValueError):
        raise ValueError(f"{field} must be a finite number") from None
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    if result < minimum or (strict and result == minimum):
        relation = "greater than" if strict else "at least"
        raise ValueError(f"{field} must be {relation} {minimum:g}")
    return result


def _term_months(term_years: object) -> int:
    if isinstance(term_years, bool) or not isinstance(term_years, int):
        raise ValueError("term_years must be a whole number")
    if not 1 <= term_years <= 50:
        raise ValueError("term_years must be between 1 and 50")
    return term_years * 12


def _credit_score(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("credit_score must be a whole number")
    if not 300 <= value <= 850:
        raise ValueError("credit_score must be between 300 and 850")
    return value


def calculate_monthly_payment(
    principal: object, annual_interest_rate: object, term_years: object
) -> float:
    """Calculate a fixed monthly payment; interest rate is a percentage."""
    amount = _number(principal, "principal", minimum=0, strict=True)
    rate = _number(annual_interest_rate, "annual_interest_rate", minimum=0)
    if rate > 100:
        raise ValueError("annual_interest_rate must not exceed 100")
    months = _term_months(term_years)
    monthly_rate = rate / 1200
    if monthly_rate == 0:
        payment = amount / months
    else:
        # log1p/expm1 retain precision when a valid interest rate is tiny.
        exponent = months * math.log1p(monthly_rate)
        denominator = -math.expm1(-exponent)
        payment = amount * monthly_rate / denominator
    if not math.isfinite(payment):
        raise ValueError("calculated monthly payment is outside the supported range")
    return payment


def calculate_debt_to_income_ratio(
    monthly_income: object,
    existing_monthly_debt: object,
    proposed_monthly_payment: object,
) -> float:
    """Return total monthly debt as a percentage of gross monthly income."""
    income = _number(monthly_income, "monthly_income", minimum=0, strict=True)
    existing = _number(existing_monthly_debt, "existing_monthly_debt", minimum=0)
    proposed = _number(proposed_monthly_payment, "proposed_monthly_payment", minimum=0)
    total_debt = existing + proposed
    ratio = total_debt / income * 100
    if not math.isfinite(ratio):
        raise ValueError("calculated debt-to-income ratio is outside the supported range")
    return ratio


def assess_loan_eligibility(
    monthly_income: object,
    existing_monthly_debt: object,
    principal: object,
    annual_interest_rate: object,
    term_years: object,
    credit_score: object,
) -> dict[str, object]:
    """Assess eligibility using a 650 score floor and a 40% DTI ceiling."""
    score = _credit_score(credit_score)
    payment = calculate_monthly_payment(principal, annual_interest_rate, term_years)
    dti = calculate_debt_to_income_ratio(monthly_income, existing_monthly_debt, payment)
    reasons = []
    if score < 650:
        reasons.append("credit score is below 650")
    if dti > 40:
        reasons.append("debt-to-income ratio is above 40%")
    return {
        "eligible": not reasons,
        "monthly_payment": payment,
        "debt_to_income_ratio": dti,
        "reasons": reasons,
    }


def main() -> None:
    """Print a representative application decision for the lab run-through."""
    result = assess_loan_eligibility(5000, 500, 100000, 6.5, 5, 720)
    print("Loan eligibility demo")
    print(f"Eligible: {'Yes' if result['eligible'] else 'No'}")
    print(f"Monthly payment: INR {result['monthly_payment']:.2f}")
    print(f"Debt-to-income ratio: {result['debt_to_income_ratio']:.2f}%")
    if result["reasons"]:
        print("Reasons: " + "; ".join(result["reasons"]))


if __name__ == "__main__":  # pragma: no cover
    main()
