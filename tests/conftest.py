import pytest
import re
import sys
import importlib

# Enter the name of the file to be tested here, but leave out the .py file extention.
module_to_test = "a3_BMI"

def load_or_reload_module():
    if module_to_test in sys.modules:
        module = sys.modules[module_to_test]
        importlib.reload(module)          
    else:
        module = importlib.import_module(module_to_test)

def normalize_text(text):
    # Lowercase the input
    text = text.lower()
    
    # Replace newlines with a single space
    text = text.replace('\n', ' ')
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove periods not between digits
    text = re.sub(r'(?<!\d)\.(?!\d)', '', text)
    
    # Remove hyphens not followed by digits (negative signs at the beginning of numbers)
    text = re.sub(r'-(?!\d)', '', text)
    
    # Remove all other punctuation and symbols
    text = re.sub(r'[!"#$%&\'()*+,/:;<=>?@\[\]^_`{|}~]', '', text)
    
    # Replace multiple spaces again in case punctuation removal created extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing spaces
    return text.strip()


@pytest.fixture
def inputs_and_expected_outputs():
    """
    Returns a list of tuples.
    Each tuple contains:
        1st tuple: test inputs
        2nd tuple: expected outputs
            - 1st tuple is 2 possible calculations of BMI
              The first is using round(2), the 2nd using f string rounding.
            - 2nd value string is the BMI category
    """

    test_cases = [
    # Underweight category (BMI < 18.5)
    (("John", "Doe", "5", "6", "114"), (("18.4", "18.40"), "Underweight")),
    (("Jane", "Smith", "5", "6", "115"), (("18.56", "18.56"), "Normal weight")),

    # Normal weight category (18.5 <= BMI < 25)
    (("Bob", "Brown", "5", "6", "154"), (("24.85", "24.85"), "Normal weight")),

    # Overweight category (25 <= BMI < 30)
    (("Charlie", "Johnson", "5", "6", "185"), (("29.86", "29.86"), "Overweight")),

    # Boundary condition at BMI = 30
    (("Diana", "Wilson", "5", "6", "186"), (("30.02","30.02"), "Obese")),
    ]
    return test_cases

# this replaces the built in input() function using monkeypatch. Can be called by any test.
# it needs to be called for any assignment that uses the input() function, as that will cause
# any test to crash.
@pytest.fixture
def mock_inputs(monkeypatch):
    # Create a function to set inputs
    def _mock_inputs(simulated_inputs):
        input_iter = iter(simulated_inputs)
        captured_input_prompts = []

        # Define the mock input function
        def mock_input(prompt):
            captured_input_prompts.append(prompt)
            return next(input_iter, '') # grabs the next input, or a blank string if empty

        # Use monkeypatch to replace the built-in input() with the mock input function
        monkeypatch.setattr('builtins.input', mock_input)

        return captured_input_prompts

    return _mock_inputs

# Note that GitHub Classroom currently has an error where it cannot process parametrize in pytest.
# if this is ever fixed, I can use the below syntax on any test.
'''
@pytest.mark.parametrize("mock_inputs", [
    (["Example input response 1", "Example input response 2"]),
    (["Another input 1", "Another input 2"]),
], indirect=True)

'''

