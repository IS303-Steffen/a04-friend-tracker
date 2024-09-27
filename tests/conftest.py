'''
conftest.py is a configuration file automatically accessed by pytest
any @pytest.fixture created here is available to any other test file
if they reference it as a parameter.
'''

import pytest
import re
import textwrap
import sys
import os
import inspect
import importlib
import json
from tests.setup_test_cases import test_cases_list

# Enter the name of the file to be tested here, but leave out the .py file extention.
default_module_to_test = "a4_solution_friend_tracker"
# Path to the directory containing this file
CURRENT_DIR = os.path.dirname(__file__)

# ========
# FIXTURES
# ========

@pytest.fixture
def test_cases():
    # Path to the captured test cases JSON file
    captured_test_cases_file = os.path.join(CURRENT_DIR, 'captured_test_cases.json')
    
    # Load the test cases
    with open(captured_test_cases_file, 'r') as f:
        test_cases = json.load(f)
    
    # Return the test cases directly, no need to unpickle variables
    return test_cases

@pytest.fixture
def mock_inputs(monkeypatch):
    """
    this replaces the built in input() function using monkeypatch. Can be called by any test.
    Must to be called for any assignment that uses the input() function, as that will cause
    any test to crash.
    """
    # Create a function to set inputs. Pytest doesn't let you pass arguments
    # into fixtures, so this is just a workaround to allow for passing in the inputs.
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

# ================
# HELPER FUNCTIONS
# ================
    
def load_or_reload_module(mock_inputs, inputs, module_to_test=default_module_to_test):
    """
    Loads in student code with a monkeypatched input() function so that it can
    run without pausing the terminal.

    If students turn in code with variations of "if __name__ == '__main__'
    logic, it will generate an altered version of their code 
    in the "student_test_module.py" file with their main
    logic "flattened" to the global level so that this function can still 
    access their variables as if they were global. This is needed any time
    student code uses input() or you want to check the values of global
    variables for tests.
    """
    
    # Define the path to the test module inside the tests/ directory
    test_module_path = os.path.join(os.getcwd(), "tests", "student_test_module.py")
    
    # Ensure the tests/ directory is in sys.path for imports
    if os.path.join(os.getcwd(), "tests") not in sys.path:
        sys.path.append(os.path.join(os.getcwd(), "tests"))

    # Check if the student_test_module.py already exists
    if os.path.exists(test_module_path):
        print("student_test_module.py exists, loading it directly.")

        captured_input_prompts = mock_inputs(inputs)
        # If the file exists, import or reload the module directly
        if 'student_test_module' in sys.modules:
            dynamic_module = importlib.reload(sys.modules['student_test_module'])
        else:
            dynamic_module = importlib.import_module('student_test_module')

        return captured_input_prompts, dynamic_module.__dict__

    try:
        captured_input_prompts = mock_inputs(inputs)

        # Step 1: Import or reload the module normally
        if module_to_test in sys.modules:
            module = sys.modules[module_to_test]
            module = importlib.reload(module)
        else:
            module = importlib.import_module(module_to_test)

        module_source = inspect.getsource(module)

        # Step 2: Handle flattening cases if required
        main_body = None
        main_func_name = None
        if hasattr(module, 'main'):
            main_func_name = 'main'
        elif hasattr(module, 'Main'):
            main_func_name = 'Main'

        if main_func_name:
            print(f"Handling case 3: Flattening {main_func_name}() function.")
            main_body = flatten_main_code(module_source)
        elif re.search(r'^[^#]*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', module_source, re.MULTILINE):
            print("Handling case 2: Flattening if __name__ == '__main__' block.")
            main_body = flatten_main_code(module_source)
        else:
            return captured_input_prompts, module.__dict__

        # Step 3: Write the flattened code to a fixed Python file in the tests/ directory
        os.makedirs(os.path.dirname(test_module_path), exist_ok=True)
        with open(test_module_path, 'w') as test_module_file:
            test_module_file.write(f"# Dynamically generated module for testing\n{main_body}")

        # Step 4: Apply the monkeypatch to the dynamically imported module
        captured_input_prompts = mock_inputs(inputs)

        # Step 5: Import or reload the newly created student_test_module from tests/
        if 'student_test_module' in sys.modules:
            dynamic_module = importlib.reload(sys.modules['student_test_module'])
        else:
            dynamic_module = importlib.import_module('student_test_module')

        # Step 6: Return the captured input prompts and globals from the dynamic module
        return captured_input_prompts, dynamic_module.__dict__

    except Exception as e:
        pytest.fail(f"Error during testing: {e}")

def flatten_main_code(code):
    """
    Used when the student's code contains an if statement to only run if the
    code's __name___ is main, or they use a main() funciton. It "flattens"
    the code to be at the global level so the tests can access its global
    variables and fuctions.

    Written by ChatGPT, so I haven't examined it closely
    """
    lines = code.splitlines()
    output_lines = []
    # inside_block = False
    # block_lines = []
    # indent_level = None
    skip_lines = set()
    
    # First, find the main function definition and extract its body
    def_main_pattern = re.compile(r'^\s*def\s+main\s*\([^)]*\)\s*:')
    main_func_start = None
    main_func_indent = None
    main_func_body = []
    
    for idx, line in enumerate(lines):
        if main_func_start is None and def_main_pattern.match(line):
            main_func_start = idx
            stripped_line = line.lstrip()
            main_func_indent = len(line) - len(stripped_line)
            continue
        if main_func_start is not None and idx > main_func_start:
            # Check if the line is part of the main function body
            line_expanded = line.expandtabs()
            current_indent = len(line_expanded) - len(line_expanded.lstrip())
            if line.strip() == '':
                # Blank line inside function
                main_func_body.append(line)
            elif current_indent > main_func_indent:
                # Line is part of the main function
                main_func_body.append(line)
            else:
                # End of main function
                break
    
    # Remove the main function definition and its body from the original code
    if main_func_start is not None:
        end_of_main = main_func_start + len(main_func_body) + 1
        skip_lines.update(range(main_func_start, end_of_main))
        # Dedent the main function body
        dedented_main_body = textwrap.dedent('\n'.join(main_func_body))
        dedented_main_lines = dedented_main_body.splitlines()
    else:
        dedented_main_lines = []
    
    # Now, process the rest of the code to handle if __name__ == "__main__"
    inside_if_main = False
    if_main_indent = None
    if_main_body = []
    
    for idx, line in enumerate(lines):
        if idx in skip_lines:
            continue  # Skip lines we've already processed
        line_expanded = line.expandtabs()
        stripped_line = line_expanded.lstrip()
        if not inside_if_main:
            # Check for 'if __name__ == "__main__":' line
            if re.match(r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line_expanded):
                inside_if_main = True
                if_main_indent = len(line_expanded) - len(stripped_line)
                continue
            else:
                output_lines.append(line)
        else:
            # Inside if __name__ == "__main__" block
            current_indent = len(line_expanded) - len(stripped_line)
            if not stripped_line:
                # Empty or whitespace-only line
                if_main_body.append(line)
            elif current_indent > if_main_indent:
                # Line is part of the if __name__ == "__main__" block
                # Check if the line is a call to main()
                line_without_indent = line.lstrip()
                if not re.match(r'^main\s*\([^)]*\)\s*$', line_without_indent):
                    # Not a call to main(), include it
                    if_main_body.append(line)
                else:
                    # It's a call to main(), skip it
                    pass
            else:
                # Exited the block
                # Dedent and add the block lines
                if if_main_body:
                    dedented_if_main_body = textwrap.dedent('\n'.join(if_main_body))
                    dedented_if_main_lines = dedented_if_main_body.splitlines()
                    output_lines.extend(dedented_if_main_lines)
                if_main_body = []
                inside_if_main = False
                if_main_indent = None
                output_lines.append(line)
    # Add any remaining lines from the if __name__ == "__main__" block
    if inside_if_main and if_main_body:
        dedented_if_main_body = textwrap.dedent('\n'.join(if_main_body))
        dedented_if_main_lines = dedented_if_main_body.splitlines()
        output_lines.extend(dedented_if_main_lines)
    
    # Merge the dedented main function body into the output
    output_lines.extend(dedented_main_lines)
    
    return '\n'.join(output_lines)


def normalize_text(text):
    """
    Used by tests that look for specific output or input prompts.
    Makes all text lowercase, reduces all spacing to just one space
    and removes any extra symbols, except for negative signs and decimals
    associated with numbers.
    """
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