"""Hypothesis edge-case and property tests for processor.py."""

import math

import pytest
from hypothesis import given, strategies as st

from processor import (
    assess_loan_eligibility,
    calculate_debt_to_income_ratio,
    calculate_monthly_payment,
)


@given(
    principal=st.floats(min_value=0.01, max_value=1e9, allow_nan=False, allow_infinity=False),
    term=st.integers(min_value=1, max_value=50),
)
def test_zero_interest_payment_is_principal_over_months(principal, term):
    payment = calculate_monthly_payment(principal, 0, term)
    assert payment == pytest.approx(principal / (term * 12), rel=1e-12)


@given(
    principal=st.floats(min_value=0.01, max_value=1e7, allow_nan=False, allow_infinity=False),
    rate=st.floats(min_value=0.01, max_value=100, allow_nan=False, allow_infinity=False),
    term=st.integers(min_value=1, max_value=50),
)
def test_payment_is_finite_and_positive(principal, rate, term):
    result = calculate_monthly_payment(principal, rate, term)
    assert math.isfinite(result)
    assert result > 0


@given(
    income=st.floats(min_value=0.01, max_value=1e7, allow_nan=False, allow_infinity=False),
    existing=st.floats(min_value=0, max_value=1e7, allow_nan=False, allow_infinity=False),
    proposed=st.floats(min_value=0, max_value=1e7, allow_nan=False, allow_infinity=False),
)
def test_dti_matches_debt_over_income_percent(income, existing, proposed):
    actual = calculate_debt_to_income_ratio(income, existing, proposed)
    assert actual == pytest.approx((existing + proposed) / income * 100)
    assert actual >= 0


@given(
    income=st.floats(min_value=1, max_value=100000, allow_nan=False, allow_infinity=False),
    debt=st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
    principal=st.floats(min_value=0.01, max_value=1000000, allow_nan=False, allow_infinity=False),
    rate=st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False),
    term=st.integers(min_value=1, max_value=50),
    score=st.integers(min_value=300, max_value=850),
)
def test_assessment_is_deterministic_and_has_required_fields(income, debt, principal, rate, term, score):
    result = assess_loan_eligibility(income, debt, principal, rate, term, score)
    assert set(result) == {"eligible", "monthly_payment", "debt_to_income_ratio", "reasons"}
    assert result["eligible"] is (score >= 650 and result["debt_to_income_ratio"] <= 40)
    assert isinstance(result["reasons"], list)


@pytest.mark.parametrize("value", [None, True, "10", float("nan"), float("inf"), -1, 10**1000])
def test_payment_rejects_invalid_principal(value):
    with pytest.raises(ValueError):
        calculate_monthly_payment(value, 5, 10)


@pytest.mark.parametrize("rate", [-0.1, 100.1, float("nan"), float("inf"), "5"])
def test_payment_rejects_invalid_rate(rate):
    with pytest.raises(ValueError):
        calculate_monthly_payment(1000, rate, 10)


@pytest.mark.parametrize("term", [0, 51, 1.5, True, "10", None])
def test_payment_rejects_invalid_term(term):
    with pytest.raises(ValueError):
        calculate_monthly_payment(1000, 5, term)


@pytest.mark.parametrize("values", [(0, 0, 0), (-1, 0, 0), (1000, -1, 0), (1000, 0, -1), (float("nan"), 0, 0)])
def test_dti_rejects_invalid_values(values):
    with pytest.raises(ValueError):
        calculate_debt_to_income_ratio(*values)


@pytest.mark.parametrize("score", [299, 851, 650.0, True, "720", None])
def test_assessment_rejects_invalid_credit_score(score):
    with pytest.raises(ValueError):
        assess_loan_eligibility(5000, 0, 10000, 0, 5, score)


def test_eligibility_thresholds_and_reason_messages():
    approved = assess_loan_eligibility(10000, 0, 48000, 0, 1, 650)
    assert approved["eligible"] is True
    assert approved["debt_to_income_ratio"] == pytest.approx(40)
    assert approved["reasons"] == []

    low_score = assess_loan_eligibility(10000, 0, 48000, 0, 1, 649)
    assert low_score["eligible"] is False
    assert low_score["reasons"] == ["credit score is below 650"]

    high_dti = assess_loan_eligibility(10000, 0, 49200, 0, 1, 700)
    assert high_dti["eligible"] is False
    assert high_dti["reasons"] == ["debt-to-income ratio is above 40%"]

    both = assess_loan_eligibility(10000, 0, 49200, 0, 1, 600)
    assert len(both["reasons"]) == 2

