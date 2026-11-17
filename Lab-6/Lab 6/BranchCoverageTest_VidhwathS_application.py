import pytest

from loan_eligibility import credit_band, interest_rate, is_eligible


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (750, "excellent"),
        (749, "good"),
        (650, "good"),
        (649, "fair"),
        (550, "fair"),
        (549, "poor"),
    ],
)
def test_each_credit_band_boundary(score, expected):
    assert credit_band(score) == expected


@pytest.mark.parametrize("score", [299, 901])
def test_invalid_score_boundaries(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


def test_eligibility_validation_and_age_branches():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)
    assert is_eligible(20, 50000, "salaried", 800) is False
    assert is_eligible(61, 50000, "salaried", 800) is False


@pytest.mark.parametrize(
    ("employment", "income"), [("salaried", 24999), ("self_employed", 39999)]
)
def test_income_threshold_rejections(employment, income):
    assert is_eligible(30, income, employment, 800) is False


@pytest.mark.parametrize("score", [549, 550, 649, 650, 749, 750])
def test_eligible_loan_at_credit_band_boundaries(score):
    expected = score >= 550
    assert is_eligible(21, 40000, "self_employed", score) is expected


def test_interest_rate_all_conditions():
    assert interest_rate(750, "salaried", False) == 8
    assert interest_rate(749, "salaried", True) == 8
    assert interest_rate(650, "self_employed", False) == 11
    assert interest_rate(649, "self_employed", True) == 12
