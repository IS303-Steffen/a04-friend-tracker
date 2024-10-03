'''
conftest.py is a configuration file automatically accessed by pytest
any @pytest.fixture created here is available to any other test file
if they reference it as a parameter.
'''

import pytest, re, textwrap, sys, os, inspect, importlib, json, inspect, traceback, time, signal
import builtins, multiprocessing, pickle
from io import StringIO

# ================
# GLOBAL VARIABLES
# ================

# Enter the name of the file to be tested here, but leave out the .py file extention.
default_module_to_test = "a4_friend_tracker"

# default per-test-case timeout amount in seconds:
default_timeout_seconds = 5

# Path to the directory containing this file
CURRENT_DIR = os.path.dirname(__file__)

# ========
# FIXTURES
# ========

@pytest.fixture
def test_cases():
    # Path to the final captured test cases JSON file
    captured_test_cases_file = os.path.join(CURRENT_DIR, 'test_cases_final.json')
    
    # Load the test cases
    with open(captured_test_cases_file, 'r') as f:
        test_cases = json.load(f)
    
    return test_cases


# =====
# HOOKS
# =====

# Global set to track which tests have been run
_run_tests = set()

# Hook that runs before each test is executed
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    test_name = item.nodeid  # Get the test's identifier (e.g., file path + test name)
    
    if test_name not in _run_tests:
        print(f"First time running {test_name}")
        _run_tests.add(test_name)
    else:
        print(f"{test_name} has already been run in this session")

# This is a keyword name of a function for pytest. It will run automatically when done with
# a session of pytest
def pytest_sessionfinish():
    # Path to the file to check and delete
    file_path = os.path.join('tests', 'student_test_module.py')

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Delete the file
            os.remove(file_path)
            print(f"\nCreated flattened file {file_path} during testing, and successfully removed it when finished.")
        except OSError as e:
            print(f"\nError deleting {file_path}: {e}")



# ================
# HELPER FUNCTIONS
# ================

def is_picklable(obj):
    try:
        pickle.dumps(obj)
    except Exception:
        return False
    else:
        return True

def load_or_reload_module(inputs, test_case=None, module_to_test=default_module_to_test):
    """
    Loads the student's code in a subprocess with mocked inputs to prevent hanging the main test process.
    """
    try:
        # Create a queue to communicate with the subprocess
        queue = multiprocessing.Queue()

        # Set the timeout (in seconds)
        timeout_seconds = default_timeout_seconds

        # Start the subprocess
        p = multiprocessing.Process(target=_load_module_subprocess, args=(queue, inputs, test_case, module_to_test))
        p.start()

        # Wait for the subprocess to finish or timeout
        p.join(timeout_seconds)

        if p.is_alive():
            # Subprocess is still running; terminate it
            p.terminate()
            p.join()
            # Handle timeout
            pytest.fail(timeout_message_for_students(test_case))
        else:
            # Subprocess finished; get the result
            if not queue.empty():
                status, payload = queue.get()
                if status == 'success':
                    # get input prompts, printed messages and all other variables from the queue
                    captured_input_prompts, captured_output, module_globals = payload
                    return captured_input_prompts, captured_output, module_globals
                elif status == 'exception':
                    exception_data = payload  # Exception data dictionary
                    exception_message_for_students(exception_data, test_case)
                else:
                    pytest.fail("Unexpected status from subprocess.")
            else:
                pytest.fail("Subprocess finished without returning any data.")
    except Exception as e:
        exception_message_for_students(e, test_case)


def _load_module_subprocess(queue, inputs, test_case, module_to_test):
    try:
        # Mock input function in the subprocess
        captured_input_prompts = []

        def mock_input(prompt=''):
            if prompt != '':
                captured_input_prompts.append(prompt)
            return next(input_iter, '')

        input_iter = iter(inputs)
        builtins.input = mock_input

        # Capture printed output by redirecting sys.stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Initialize main_body to None to avoid UnboundLocalError
        main_body = None  # <-- Add this line

        # Proceed with the original logic
        # Define the path to the test module inside the tests/ directory
        test_module_path = os.path.join(os.getcwd(), "tests", "student_test_module.py")

        # Ensure the tests/ directory is in sys.path for imports
        tests_dir = os.path.join(os.getcwd(), "tests")
        if tests_dir not in sys.path:
            sys.path.insert(0, tests_dir)

        # Check if the student_test_module.py already exists
        if os.path.exists(test_module_path):
            # If the file exists, import or reload the module directly
            if 'student_test_module' in sys.modules:
                dynamic_module = importlib.reload(sys.modules['student_test_module'])
            else:
                dynamic_module = importlib.import_module('student_test_module')
        else:
            # Import or reload the module normally
            if module_to_test in sys.modules:
                module = sys.modules[module_to_test]
                module = importlib.reload(module)
            else:
                module = importlib.import_module(module_to_test)

            module_source = inspect.getsource(module)

            # Handle flattening cases if required
            main_func_name = None
            if hasattr(module, 'main'):
                main_func_name = 'main'
            elif hasattr(module, 'Main'):
                main_func_name = 'Main'

            if main_func_name:
                print(f"Handling case: Flattening {main_func_name}() function.")
                main_body = flatten_main_code(module_source)
            elif re.search(r'^[^#]*if\s+__name__\s*==\s*[\'\"]__main__[\'\"]\s*:', module_source, re.MULTILINE):
                print("Handling case: Flattening if __name__ == '__main__' block.")
                main_body = flatten_main_code(module_source)
            else:
                # No flattening needed
                dynamic_module = module

        if main_body:
            # Write the flattened code to a fixed Python file in the tests/ directory
            os.makedirs(os.path.dirname(test_module_path), exist_ok=True)
            with open(test_module_path, 'w') as test_module_file:
                test_module_file.write(f"# Dynamically generated module for testing\n{main_body}")

            # Import or reload the newly created student_test_module from tests/
            if 'student_test_module' in sys.modules:
                dynamic_module = importlib.reload(sys.modules['student_test_module'])
            else:
                dynamic_module = importlib.import_module('student_test_module')

        # If main_body is None, dynamic_module should already be defined
        if not main_body:
            # Ensure that dynamic_module is assigned
            if 'dynamic_module' not in locals():
                dynamic_module = module  # Assign module to dynamic_module

        # Filter module.__dict__ to include only picklable items
        module_globals = {k: v for k, v in dynamic_module.__dict__.items() if is_picklable(v)}

        # After running the student's code, get the printed output
        captured_output = sys.stdout.getvalue()

        # Reset sys.stdout
        sys.stdout = old_stdout

        # Send back the results
        queue.put(('success', (captured_input_prompts, captured_output, module_globals)))

    except Exception as e:
        # Reset sys.stdout in case of exception
        sys.stdout = old_stdout
        # Send the exception back as a dictionary
        exc_type, exc_value, exc_tb = sys.exc_info()
        exception_data = {
            'type': type(e).__name__,
            'message': str(e),
            'traceback': traceback.format_exception(exc_type, exc_value, exc_tb)
        }
        queue.put(('exception', exception_data))


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
    if isinstance(text, str):
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
    else:
        return text

#74 characters should be the max
def format_error_message(custom_message: str = None,
                         test_case: dict = None,
                         display_inputs: bool = False,
                         display_input_prompts: bool = False,
                         display_invalid_input_prompts: bool = False,
                         display_printed_messages: bool = False,
                         display_invalid_printed_messages: bool = False,
                         line_length: int = 74) -> str:
    
    # some starting strings. All messages will be appended to error_message
    error_message = ''
    divider = f"\n{"-"*line_length}\n"
    error_message += divider
    error_message += f"IS 303 STUDENTS: READ THE ERROR MESSAGES IN RED BELOW\n\n"
    error_message += "↓"*line_length + "\n"
    if test_case:
        error_message += divider
        error_message += f"TEST FAILED DURING TEST CASE: {test_case["id_test_case"]}"
        error_message += divider
        error_message += insert_newline_at_last_space((
            f"\nLook at the \"Test Cases\" section of the instructions in README.md. "
            f"Run your code while inputting the EXACT inputs shown there to see where/why "
            f"your code either breaks or doesn't pass this test.\n\n"
        ), line_length)
        test_case_description = f"FOR TEST CASE: {test_case["id_test_case"]}"
    else:
        test_case_description = ''

    if custom_message:
        error_message += divider
        error_message += f"WHAT WENT WRONG:"
        error_message += divider
        error_message += insert_newline_at_last_space("\n" + custom_message, line_length)

    if display_inputs:
        inputs_concatenated = '\n'.join(test_case["inputs"])
        error_message += divider
        error_message += f"INPUTS ENTERED {test_case_description}"
        error_message += divider
        error_message += insert_newline_at_last_space(f"\nThese inputs will be entered in this exact order during this test case:\n\n\n", line_length)
        error_message += inputs_concatenated + "\n"

    if display_input_prompts:
        expected_input_prompts_concatenated = '\n'.join(test_case["input_prompts"])
        error_message += divider
        error_message += f"EXPECTED INPUT PROMPTS {test_case_description}"
        error_message += divider
        error_message += insert_newline_at_last_space(f"\nThese inputs prompts must appear at least once during this test case:\n\n\n", line_length)
        error_message += expected_input_prompts_concatenated + "\n"

    if display_invalid_input_prompts:
        invalid_input_prompts_concatenated = '\n'.join(test_case["invalid_input_prompts"])
        error_message += divider
        error_message += f"INVALID INPUT PROMPTS {test_case_description}"
        error_message += divider
        error_message += insert_newline_at_last_space(f"\nThe test will fail if any of the following appear during this test case:\n\n\n", line_length)
        error_message += invalid_input_prompts_concatenated + "\n"

    if display_printed_messages:
        expected_printed_messages_concatenated = '\n'.join(test_case["printed_messages"])
        error_message += divider
        error_message += f"EXPECTED PRINTED MESSAGES {test_case_description}"
        error_message += divider               
        error_message += insert_newline_at_last_space(f"\nThese printed messages must appear at least once during this test case:\n\n\n", line_length)
        error_message += expected_printed_messages_concatenated + "\n"

    if display_invalid_printed_messages:
        invalid_printed_messages_concatenated = '\n'.join(test_case["invalid_printed_messages"])
        error_message += divider
        error_message += f"INVALID PRINTED MESSAGES {test_case_description}"
        error_message += divider
        error_message += insert_newline_at_last_space(f"\nThe test will fail if any of the following appear during this test case:\n\n\n", line_length)
        error_message += invalid_printed_messages_concatenated + "\n"

    error_message += "\n"

    return error_message

def insert_newline_at_last_space(s, width=74):
    lines = []
    current_line = ""
    
    for char in s:
        current_line += char
        
        # If we hit a newline, append the current line and reset the line
        if char == '\n':
            lines.append(current_line.strip())  # Add the line and strip any extra spaces
            current_line = ""
            continue
        
        # If the current line exceeds the width, break at the last space
        if len(current_line) > width:
            # Find the last space before the width limit
            break_index = current_line.rfind(' ', 0, width)
            
            # If no space is found, break at the width limit
            if break_index == -1:
                break_index = width
            
            # Append the part of the line before the break
            lines.append(current_line[:break_index].strip())
            
            # Reset current_line to the remaining unprocessed part of the string
            current_line = current_line[break_index:].lstrip()  # Remove leading spaces in the next line
            
    # Append the last part of the string (if any)
    if current_line:
        lines.append(current_line.strip())
    
    return '\n'.join(lines)

def exception_message_for_students(exception_data, test_case):
    import traceback
    import re

    if isinstance(exception_data, dict):
        # Exception data from the subprocess
        error_type = exception_data['type']
        error_message_str = exception_data['message']
        traceback_list = exception_data['traceback']
        # Attempt to get the last traceback entry for the error location
        if traceback_list:
            error_location = ''.join(traceback_list[-2:]) if len(traceback_list) >= 2 else ''.join(traceback_list)
        else:
            error_location = "No traceback available."
    else:
        # Exception object with traceback
        e = exception_data
        tb_list = traceback.extract_tb(e.__traceback__)
        if tb_list:
            last_traceback = [tb_list[-1]]
            error_location = ''.join(traceback.format_list(last_traceback))
        else:
            error_location = "No traceback available."
        error_type = type(e).__name__
        error_message_str = str(e)

    # Apply pattern to error_location to extract just the last part of the filename
    pattern = r'.*\/([^\/]+\.py)(.*)'  # Make it only grab the last part of the filename
    error_location = re.sub(pattern, r'\1\2', error_location)

    error_message = f"\n{error_type}: {error_message_str}"

    # Check if 'inputs' is in test_case and set display_inputs_option accordingly
    if test_case.get("inputs", None):
        display_inputs_option = True
    else:
        display_inputs_option = False

    # Call pytest.fail with the formatted error message
    pytest.fail(f"{format_error_message(
        custom_message=(f"While trying to run the test, python ran into an error.\n\n"
                        f"LOCATION OF ERROR:\n\n{error_location}\n"
                        f"ERROR MESSAGE:\n{error_message}\n\n"
                        f"HOW TO FIX IT:\n\n"
                        f"If the error occurred in {default_module_to_test}.py, go to the location in that file where "
                        f"the error occurred and see if you can repeat the error using the inputs for Test Case {test_case['id_test_case']}. "
                        f"If the error occurred in a different .py file, reach out to your professor.\n\n"), 
        test_case=test_case,
        display_inputs=display_inputs_option
        )}")

def timeout_message_for_students(test_case):
    return format_error_message(
                custom_message=(f"You got a Timeout Error, meaning this test case didn't complete after {default_timeout_seconds} seconds. "
                                f"Check out the inputs for Test Case {test_case["id_test_case"]}. Most likely, "
                                f"you wrote your code in a way that the inputs of this test case make it so your code never exits properly. "
                                f"Double check the test case examples in the instructions and make sure your code isn't asking for additional "
                                f"or fewer inputs than the test case expects.\n\n"),
                test_case=test_case,
                display_inputs=True,
                display_input_prompts=True,
                display_invalid_input_prompts=True)

def timeout_counter(stop_event, pid, timeout_triggered, timeout_seconds = default_timeout_seconds):
    for _ in range(timeout_seconds):
        if stop_event.is_set(): # check every second if the test has finished
            return
        time.sleep(1)

    # If the stop flag was not set within the timeout period, terminate the main process
    print(f"Time's up! Exceeded {timeout_seconds} seconds. Sending termination signal to the main process.")

    # set the multiprocess Value. Used when catching a keyboard interrupt exception to give a 
    # better error message if it was caused by this timeout function.
    timeout_triggered.value = 1 

    # send a KeyboardInterrupt signal (CTRL + C) to whatever process id started this function.
    os.kill(pid, signal.SIGINT)

    
