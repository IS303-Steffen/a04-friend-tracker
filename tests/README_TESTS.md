### A Quick Note to Students:
If you are student and found this, you might be looking for the README file, not this README_TESTS file. However, feel free to look at the files in this folder if you are curious about how automated testing works. But don't alter any of the files in the tests folder. GitHub will flag it and you may not get graded correctly.

# Structure of Tests
- Each test is run using pytest `pip install pytest`
- Each test is contained in the tests folder and will automatically be discovered
by pytest as long as it begins with `test` as a prefix.
- Any fixtures (special pytest functions that are reset each time they are referenced) contained in `conftest.py` are automatically discovered by pytest and made available as function parameters in each of the test files.
- I put the setup for individual test cases in `setup_test_cases.py`. Note that in pytest you can usually use the `@pytest.mark.parametrize` decorator above any test function to run a single test with multiple test cases, but (at least as of this writing) GitHub Classroom's python autograder crashes when using parametrize. So instead, I write individual test cases in `setup_test_cases.py` as dictionaries of inputs and expected results and loop through the test cases for each specific test that warrants each case.
    - To save time writing out test cases, I structured it so that any repeating input, printed message, or output can just be written once with an associated dictionary key, and then each test case can just reference the key. This can be overridden by just not calling the `add_values_to_test_case()` function, but I find this set up saves time because I can then automatically generate a list of inputs or outputs that *should not* appear in a test case.

# Setting Up Tests for GitHub Classroom
- This repository needs to be a set as a public template in the GitHub settings after it has been pushed to GitHub.
- GitHub Classroom uses GitHub Actions to run an autograding workflow every time a student pushes up their code. This is what will run the pytests.
- GitHub Actions are reliant on a .yml configuration file located in .github/workflows. To automatically create this file based on the `test_*.py` files in the tests/ folder, just run the `yml_generator.py` script before pushing the repository to GitHub and referencing.
    - IMPORTANT: Do not create any tests in GitHub Classroom when making the assignment. If you do, it will overwrite the .yml configuration. It is far quicker to just run the script here and not worry about setting any tests up through their GUI.



