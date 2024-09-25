# Automated Tests Structure
Tests are written in test_cases.xlsx. Each row in the test_cases sheet represents a separate test case, from which specific things can be tested in each of the pytests in this folder.

If you add a new sheet to test_cases.xlsx, you must update the test_cases() fixture in conftest.py to add that sheet to the test_cases_df dataframe that is used in each individual test file.

### For use in GitHub Classroom
Make sure to include:
`pip install pandas openpyxl`
in each tests' setup
