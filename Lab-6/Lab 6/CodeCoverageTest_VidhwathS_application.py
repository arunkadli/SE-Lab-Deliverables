import pytest

from loan_eligibility import credit_band, interest_rate, is_eligible


def test_credit_band_paths_and_invalid_low_score():
    assert credit_band(800) == "excellent"
    assert credit_band(700) == "good"
    assert credit_band(600) == "fair"
    assert credit_band(400) == "poor"
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(250)


def test_eligibility_rejections_and_success():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)
    assert is_eligible(20, 50000, "salaried", 800) is False
    assert is_eligible(30, 20000, "salaried", 800) is False
    assert is_eligible(30, 50000, "salaried", 500) is False
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_interest_rate_adjustments():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "self_employed", True) == 9
    assert interest_rate(600, "salaried", False) == 13
