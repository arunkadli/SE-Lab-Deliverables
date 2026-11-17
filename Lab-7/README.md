# Lab 7 - Loan Eligibility Fuzz Testing

**Student:** Vidhwath S  
**SRN:** PES2UG24AM182  
**Assigned topic:** Loan eligibility (`L6_L7_26_loan_eligibility`)

## Note about the starter repository

The assignment workbook maps this student to the loan eligibility repository. At the time of this work, the assigned repository did not provide fetchable `processor.py` or `test_processor.py` files, and no starter project was supplied separately. This is a self-contained implementation created for the assigned topic from the Lab 7 requirements; it is not represented as a repair of the instructor's original buggy code.

## Rules implemented

- Principal must be a finite positive number.
- Annual interest rate is a finite percentage from 0 through 100.
- Loan term is a whole number of years from 1 through 50.
- Monthly income must be finite and positive; existing debt and proposed payment must be finite and nonnegative.
- Credit score must be a whole number from 300 through 850.
- Eligibility requires a credit score of at least 650 and a debt-to-income ratio no higher than 40%.
- Invalid values raise `ValueError` with a field-specific explanation.

These are explicit classroom assumptions because the repository did not include business rules.

## Run

```sh
python -m pip install -r requirements.txt
python processor.py
python -m pytest -q test_processor.py
```

Hypothesis generates values for payment, debt-to-income, and eligibility properties. Parameterized tests exercise invalid and boundary inputs.
