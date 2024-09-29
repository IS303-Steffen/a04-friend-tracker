max_score = 25 # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module, format_error_message
import re

# checks if the expected printed messages actually appear, but doesn't check for specific
# inputs or correct calculations.

def test_2_printed_messages(capsys, mock_inputs, test_cases):
    # test_cases is a list of dictionaries. Each dictionary represents a test case
    for test_case in test_cases:
        # grab the necessary data from the test case dictionary
        inputs = test_case["inputs"]
        expected_printed_messages = test_case["printed_messages"]
        invalid_printed_messages = test_case["invalid_printed_messages"]

        # format the data into a single string (convenient for error messages)
        inputs_concatenated = '\n'.join(inputs)
        expected_printed_messages_concatenated = '\n'.join(expected_printed_messages)
        invalid_printed_messages_concatenated = '\n'.join(invalid_printed_messages)

        # Load in the student's code (which runs anything at a global level)
        # By passing in mock_inputs, the student's input() function will be
        # replaced by a mock version that will auto insert the inputs for the 
        # test case

        load_or_reload_module(mock_inputs, inputs)

        # Capture the output from the print statements
        captured = capsys.readouterr().out

        # This will return a list of strings, each representing a line of the captured output
        # this just makes it easier to read the output if the test goes wrong.
        captured_lines = captured.splitlines()  

        # Normalize the captured output to remove spaces, punctuation, and symbols
        normalized_captured_print_statements = [normalize_text(captured_print) for captured_print in captured_lines]
        normalized_captured_print_statements = '\n'.join(normalized_captured_print_statements)

        # Check that each required phrase (regex pattern) is found in the normalized captured output
        for expected_phrase in expected_printed_messages:
            # Ensure the expected phrase is normalized as well
            expected_phrase = normalize_text(expected_phrase)
            
            # Convert the expected phrase into a regex pattern (replace {name} with a regex wildcard for any text)
            regex_pattern = expected_phrase.replace("wildcard", r".+?")
            
            # Check if the pattern exists in the normalized captured input prompts
            match = re.search(regex_pattern, normalized_captured_print_statements)

            assert match, format_error_message(
                test_case,
                ("The expected printed message (ignoring punctuation / capitalization):\n\n"
                f"\"{expected_phrase}\"\n\n"
                f"wasn't printed in your code.\n\n"
                f"Below are all the printed messages from your code (ignoring punctuation / capitalization):\n\n"
                f"{normalized_captured_print_statements}\n\n"),
                display_inputs=True,
                display_printed_messages=True,
                display_invalid_printed_messages=True
                )


        # Ensure none of the invalid phrases are found in the normalized captured output
        for invalid_phrase in invalid_printed_messages:
            # Ensure the expected phrase is normalized as well
            invalid_phrase = normalize_text(invalid_phrase)
            
            # Convert the expected phrase into a regex pattern (replace {name} with a regex wildcard for any text)
            regex_pattern = invalid_phrase.replace("wildcard", r".+?")
            
            # Check if the pattern exists in the normalized captured input prompts
            match = re.search(regex_pattern, normalized_captured_print_statements)

            assert not match, format_error_message(
                ("You used an invalid printed message (ignoring punctuation / capitalization):\n\n"
                f"\"{invalid_phrase}\"\n\n"
                f"Below are all the printed messages from your code (ignoring punctuation / capitalization):\n\n"
                f"{normalized_captured_print_statements}\n\n"),
                test_case=test_case,
                display_inputs=True,
                display_printed_messages=True,
                display_invalid_printed_messages=True
                )