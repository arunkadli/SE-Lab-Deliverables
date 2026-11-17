# Lab 6 - Loan Eligibility Coverage

Student: Vidhwath S (PES2UG24AM182)  
Assigned repository: `SETAPESU26/L6_L7_26_loan_eligibility`

The application is the assigned starter code. The two test modules satisfy the
Lab 6 deliverables separately: one targets full line coverage and one exercises
both outcomes at each decision boundary for branch coverage. The files are in
the assigned repository's `Lab 6/` folder.

Install dependencies from the repository root:

```sh
python3 -m pip install -r requirements.txt
```

## Run the line coverage tests

```sh
coverage run --source=loan_eligibility -m pytest -q CodeCoverageTest_VidhwathS_application.py
coverage report -m
```

## Run the branch coverage tests

```sh
coverage erase
coverage run --branch --source=loan_eligibility -m pytest -q BranchCoverageTest_VidhwathS_application.py
coverage report -m
```

Coverage report images for both successful runs are in `screenshots/`.
