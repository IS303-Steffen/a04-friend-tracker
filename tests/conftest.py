import pytest
import re
import textwrap
import sys
import os
import inspect
import importlib
from config_test_cases import test_cases_list

# Enter the name of the file to be tested here, but leave out the .py file extention.
default_module_to_test = "a4_solution_friend_tracker"

def load_or_reload_module(mock_inputs, inputs, module_to_test=default_module_to_test):
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

# def load_or_reload_module(mock_inputs, inputs, module_to_test=default_module_to_test):
#     try:
#         captured_input_prompts = mock_inputs(inputs)

#         # Step 1: Import or reload the module normally
#         if module_to_test in sys.modules:
#             module = sys.modules[module_to_test]
#             module = importlib.reload(module)
#         else:
#             module = importlib.import_module(module_to_test)

#         module_source = inspect.getsource(module)

#         # Step 2: Handle flattening cases if required
#         # if the student used any if __name__ statements
#         main_body = None
#         main_func_name = None
#         if hasattr(module, 'main'):
#             main_func_name = 'main'
#         elif hasattr(module, 'Main'):
#             main_func_name = 'Main'

#         if main_func_name:
#             print(f"Handling case 3: Flattening {main_func_name}() function.")
#             main_body = flatten_main_code(module_source)
#         elif re.search(r'^[^#]*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', module_source, re.MULTILINE):
#             print("Handling case 2: Flattening if __name__ == '__main__' block.")
#             main_body = flatten_main_code(module_source)
#         else:
#             return captured_input_prompts, module.__dict__

#         # Step 3: Write the flattened code to a real Python file
#         new_module_path = os.path.join(os.getcwd(), "student_test_module.py")
#         with open(new_module_path, 'w') as new_module_file:
#             new_module_file.write(f"# Dynamically generated module for testing\n{main_body}")

#         # Step 4: Apply the monkeypatch to the dynamically imported module
#         # so that the input function is replaced.
#         captured_input_prompts = mock_inputs(inputs)

#         # Step 5: Import or reload the newly created module
#         if 'student_test_module' in sys.modules:
#             dynamic_module = importlib.reload(sys.modules['student_test_module'])
#         else:
#             dynamic_module = importlib.import_module('student_test_module')

#         # Step 6: Return the captured input prompts and globals from the dynamic module
#         return captured_input_prompts, dynamic_module.__dict__

#     except Exception as e:
#         pytest.fail(f"Error during testing: {e}")

#     finally:
#         # get rid of the created module if it was able to create it
#         if os.path.exists(new_module_path):
#             os.remove(new_module_path)


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

# this replaces the built in input() function using monkeypatch. Can be called by any test.
# it needs to be called for any assignment that uses the input() function, as that will cause
# any test to crash.
@pytest.fixture
def mock_inputs(monkeypatch):
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

# # Function to lookup the actual values based on IDs
# def get_values_from_ids(ids_str, lookup_df, id_col, value_col):
#     # Ensure we are working with strings, since everything was loaded as strings
#     ids = [i.strip() for i in ids_str.split(',')]  # Strip spaces and keep as strings
#     values = lookup_df[lookup_df[id_col].isin(ids)][value_col].tolist()  # Find matching rows and return the values
#     return values

@pytest.fixture
def test_cases():
    return test_cases_list


# @pytest.fixture
# def test_cases():
#     """
#     Loads in test cases from the test_cases.xlsx file
#     test_cases.xlsx is (sort of) designed to be normalized, so after
#     importing each
#     The dataframe it returns will have columns for:
#         'id_test_case' (int),
#         'test_description' (str),
#         'input_ids' (str or int),
#         'expected_input_prompt_ids' (str or int),
#         'expected_printed_message_ids'(str or int),
#         'expected_dictionaries_ids' (str or int),
#         'input_values' (list),
#         'expected_input_prompt_values' (list),
#         'expected_printed_message_values' (list),
#         'expected_dictionaries_values' (list), 
#         'invalid_input_prompt_values' (list),
#         'invalid_printed_message_values' (list)
#     """
#     # Load the Excel file and read all sheets into a dictionary
#     # Load individual sheets from the Excel file, ensuring all columns are loaded as strings

#     excel_file = pd.ExcelFile(test_cases_excel_path)

#     try:
#         test_cases_df = pd.read_excel(excel_file, sheet_name='test_cases', dtype=str)
#         inputs_df = pd.read_excel(excel_file, sheet_name='inputs', dtype=str)
#         input_prompts_df = pd.read_excel(excel_file, sheet_name='input_prompts', dtype=str)
#         printed_messages_df = pd.read_excel(excel_file, sheet_name='printed_messages', dtype=str)
#         dictionaries_df = pd.read_excel(excel_file, sheet_name='dictionaries', dtype=str)
#     finally:
#         excel_file.close() 

#     # Expand the test_cases_df with the actual values from the individual sheets
#     # input values
#     test_cases_df['input_values'] = test_cases_df['input_ids'].apply(
#         lambda x: get_values_from_ids(x, inputs_df, 'id_input', 'input')
#     )
#     # input_prompt values
#     test_cases_df['expected_input_prompt_values'] = test_cases_df['expected_input_prompt_ids'].apply(
#         lambda x: get_values_from_ids(x, input_prompts_df, 'id_input_prompt', 'input_prompt')
#     )
#     # printed message values
#     test_cases_df['expected_printed_message_values'] = test_cases_df['expected_printed_message_ids'].apply(
#         lambda x: get_values_from_ids(x, printed_messages_df, 'id_printed_message', 'printed_message')
#     )
#     # dictionary values
#     test_cases_df['expected_dictionaries_values'] = test_cases_df['expected_dictionaries_ids'].apply(
#         lambda x: get_values_from_ids(x, dictionaries_df, 'id_dictionary', 'dictionary')
#     )

#     # Add invalid_input_prompt_values: those in input_prompts_df that aren't in expected_input_prompt_values
#     all_input_prompts = input_prompts_df['input_prompt'].tolist()

#     test_cases_df['invalid_input_prompt_values'] = test_cases_df['expected_input_prompt_values'].apply(
#         lambda valid_prompts: [prompt for prompt in all_input_prompts if prompt not in valid_prompts]
#     )

#     # Add invalid_printed_message_values: those in printed_messages_df that aren't in expected_printed_message_values
#     all_printed_messages = printed_messages_df['printed_message'].tolist()

#     test_cases_df['invalid_printed_message_values'] = test_cases_df['expected_printed_message_values'].apply(
#         lambda valid_messages: [message for message in all_printed_messages if message not in valid_messages]
#     )

#     return test_cases_df

# @pytest.fixture
# def test_cases():
#     """
#     Returns a list of test cases.
#     Each test case is a dictionary with a description, inputs, and expected
#     results (with result types that can vary depending on the assignment)
#     """

#     # 4 Input Prompts. This exists to copy and paste to individual test cases
#     ("Enter an option (1, 2, or 3): ",
#      "Enter friend's name: ",
#      "Enter {wildcard}'s hobby:", 
#      "Enter a friend's name to find their hobby: "),

#     # 10 Printed Messages. This exists to copy and paste to individual test cases
#     ("Menu: ",
#      "1. Add a Friend",
#      "2. Find a Friend's Hobby",
#      "3. Quit",
#      "{wildcard} is already in your dictionary.",
#      "{wildcard} added to your dictionary!",
#      "{wildcard}'s hobby is {wildcard}.",
#      "{wildcard} is not in the dictionary.",
#      "Exiting the program. Goodbye!",
#      "Invalid choice. Please choose a valid option."),

    # test_cases =[
    #     { # 1: Invalid input choice
    #     "test_description":
    #         "1: Invalid input choice",
    #     "inputs":
    #         ("example of invalid text",
    #          "3"),
    #     "expected_input_prompts":
    #         ("Enter an option (1, 2, or 3): ",),
    #     "invalid_input_prompts":
    #         ("Enter friend's name: ",
    #          "Enter {wildcard}'s hobby:", 
    #          "Enter a friend's name to find their hobby: "),
    #     "expected_printed_messages":
    #         ("Menu: ",
    #          "1. Add a Friend",
    #          "2. Find a Friend's Hobby",
    #          "3. Quit",
    #          "Exiting the program. Goodbye!",
    #          "Invalid choice. Please choose a valid option."),
    #     "invalid_printed_messages":
    #         ("{wildcard} is already in your dictionary.",
    #          "{wildcard} added to your dictionary!",
    #          "{wildcard}'s hobby is {wildcard}.",
    #          "{wildcard} is not in the dictionary."),
    #     "expected_dictionary":
    #         {}
    #     },
    #     { # 2: Single name/hobby, no lookup
    #     "test_description":
    #         "2: Single name/hobby, no lookup",
    #     "inputs":
    #         ("1",
    #          "Jimmer",
    #          "Basketball",
    #          "3"),
    #     "expected_input_prompts":
    #         ("Enter an option (1, 2, or 3): ",
    #          "Enter friend's name: ",
    #          "Enter Jimmer's hobby:"),
    #     "invalid_input_prompts":
    #         ("Enter a friend's name to find their hobby: ",),
    #     "expected_printed_messages":
    #         ("Menu: ",
    #          "1. Add a Friend",
    #          "2. Find a Friend's Hobby",
    #          "3. Quit",
    #          "Jimmer added to your dictionary!",
    #          "Exiting the program. Goodbye!"),
    #     "invalid_printed_messages":
    #         ("{wildcard} is already in your dictionary.",
    #          "{wildcard}'s hobby is {wildcard}.",
    #          "{wildcard} is not in the dictionary.",
    #          "Invalid choice. Please choose a valid option."),
    #     "expected_dictionary":
    #         {"Jimmer": "Basketball"}
    #     },
    #     { # 3: Single name/hobby, with lookup
    #     "test_description":
    #         "3: Single name/hobby, with lookup",
    #     "inputs":
    #         ("1",
    #          "Jimmer",
    #          "Basketball",
    #          "2",
    #          "Jimmer",
    #          "3"),
    #     "expected_input_prompts":
    #         ("Enter an option (1, 2, or 3): ",
    #          "Enter friend's name: ",
    #          "Enter Jimmer's hobby:",
    #          "Enter a friend's name to find their hobby: ",),
    #     "invalid_input_prompts":
    #         (),
    #     "expected_printed_messages":
    #         ("Menu: ",
    #          "1. Add a Friend",
    #          "2. Find a Friend's Hobby",
    #          "3. Quit",
    #          "Jimmer added to your dictionary!",
    #          "Jimmer's hobby is {wildcard}."
    #          "Exiting the program. Goodbye!"),
    #     "invalid_printed_messages":
    #         ("{wildcard} is already in your dictionary.",
    #          "{wildcard} is not in the dictionary.",
    #          "Invalid choice. Please choose a valid option."),
    #     "expected_dictionary":
    #         {"Jimmer": "Basketball"}
    #     },
    #     { # 4: Lookup first, single name/hobby, adding existing name 
    #     "test_description":
    #         "4: Lookup first, single name/hobby, adding existing name",
    #     "inputs":
    #         ("2",
    #          "Jimmer",
    #          "1",
    #          "Jimmer",
    #          "Basketball",
    #          "1",
    #          "Jimmer",
    #          "2",
    #          "Jimmer",
    #          "3"),
    #     "expected_input_prompts":
    #         ("Enter an option (1, 2, or 3): ",
    #          "Enter friend's name: ",
    #          "Enter Jimmer's hobby:",
    #          "Enter a friend's name to find their hobby: ",),
    #     "invalid_input_prompts":
    #         (),
    #     "expected_printed_messages":
    #         ("Menu: ",
    #          "1. Add a Friend",
    #          "2. Find a Friend's Hobby",
    #          "3. Quit",
    #          "Jimmer added to your dictionary!",
    #          "Jimmer's hobby is {wildcard}."
    #          "Exiting the program. Goodbye!"),
    #     "invalid_printed_messages":
    #         ("{wildcard} is already in your dictionary.",
    #          "{wildcard} is not in the dictionary.",
    #          "Invalid choice. Please choose a valid option."),
    #     "expected_dictionary":
    #         {"Jimmer": "Basketball"}
    #     },
    # ]

    # # inputs = ["example of invalid text", # invalid input message
    # #         
    # #         "1", "Jimmer", "Basketball", # correct name/hobby
    # #         "1", "Jimmer", # name already entered
    # #         "2", "Reena", # name not entered in dictionary yet
    # #         "2", "Jimmer", # looking up hobby of name already in dictionary
    # #         "2", "Jimmer", # trying to access a dictionary before anything added to it
    # #         "3"] # exiting
    # return test_cases



# @pytest.fixture
# def inputs_and_expected_outputs():
#     """
#     Returns a list of tuples.
#     Each tuple contains:
#         1. Tuple of inputs
#         2. Dictionary with expected values
#     """
#     test_cases = [
#     # Entering 1 name and hobby, then exiting
#     (("1","Jimmer", "Basketball", "3"),
#             {"Jimmer": "Basketball"}),
#     # Entering 1 name/hobby, looking up the value then exiting
#     (("1","Jimmer", "Basketball", "2", "Jimmer", "3"),
#             {"Jimmer": "Basketball"}),
#     # Entering 1 name/hobby, trying to add it again, then exitin
#     (("1","Jimmer", "Basketball", "1", "Jimmer", "3"),
#             {"Jimmer": "Basketball"}),
#     # Entering 3 names/hobbies, looking up a value then exiting
#     (("1", "Jimmer", "Basketball", "1", "Reena", "Listening to Sonic Youth",
#       "1", "Link", "Breaking pots", "2", "Reena", "3"),
#             {"Jimmer": "Basketball", "Reena": "Listening to Sonic Youth",
#              "Link": "Breaking pots"}),
#     ]
#     return test_cases



# Note that GitHub Classroom currently has an error where it cannot process parametrize in pytest.
# if this is ever fixed, I can use the below syntax on any test.
'''
@pytest.mark.parametrize("mock_inputs", [
    (["Example input response 1", "Example input response 2"]),
    (["Another input 1", "Another input 2"]),
], indirect=True)

'''

