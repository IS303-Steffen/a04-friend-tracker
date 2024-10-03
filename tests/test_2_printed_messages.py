max_score = 25  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_student_code, format_error_message, exception_message_for_students, timeout_message_for_students
import re

# Checks if the expected printed messages actually appear, but doesn't check for specific inputs or correct calculations.
def test_2_printed_messages(test_cases):
    try:
        # Ensure test_cases is valid and iterable
        if not isinstance(test_cases, list):
            raise ValueError("test_cases should be a list of dictionaries. Contact your professor.")

        # Loop through each test case
        for test_case in test_cases:
            try:
                # Grab the necessary data from the test case dictionary
                inputs = test_case["inputs"]
                expected_printed_messages = test_case["printed_messages"]
                invalid_printed_messages = test_case["invalid_printed_messages"]

                # Load in the student's code and capture output
                _, captured_output, _ = load_student_code(inputs, test_case)

                # Split the captured output into lines
                captured_lines = captured_output.splitlines()

                # Normalize the captured output to remove spaces, punctuation, and symbols
                normalized_captured_print_statements = [normalize_text(captured_print) for captured_print in captured_lines]
                normalized_captured_print_statements = '\n'.join(normalized_captured_print_statements)

                # Check that each required phrase (regex pattern) is found in the normalized captured output
                for expected_phrase in expected_printed_messages:
                    # Ensure the expected phrase is normalized as well
                    expected_phrase = normalize_text(expected_phrase)

                    # Convert the expected phrase into a regex pattern (replace "wildcard" with a regex wildcard for any text)
                    regex_pattern = expected_phrase.replace("wildcard", r".+?")

                    # Check if the pattern exists in the normalized captured print statements
                    match = re.search(regex_pattern, normalized_captured_print_statements)

                    assert match, format_error_message(
                        custom_message=("The expected printed message (ignoring punctuation / capitalization):\n\n"
                                        f"\"{expected_phrase}\"\n\n"
                                        f"wasn't printed in your code.\n\n"
                                        f"Below are all the printed messages from your code (ignoring punctuation / capitalization):\n\n"
                                        f"{normalized_captured_print_statements}\n\n"),
                        test_case=test_case,
                        display_inputs=True,
                        display_printed_messages=True,
                        display_invalid_printed_messages=True
                    )

                # Ensure none of the invalid phrases are found in the normalized captured output
                for invalid_phrase in invalid_printed_messages:
                    # Ensure the invalid phrase is normalized as well
                    invalid_phrase = normalize_text(invalid_phrase)

                    # Convert the invalid phrase into a regex pattern
                    regex_pattern = invalid_phrase.replace("wildcard", r".+?")

                    # Check if the pattern exists in the normalized captured print statements
                    match = re.search(regex_pattern, normalized_captured_print_statements)

                    assert not match, format_error_message(
                        custom_message=("You used an invalid printed message (ignoring punctuation / capitalization):\n\n"
                                        f"\"{invalid_phrase}\"\n\n"
                                        f"Below are all the printed messages from your code (ignoring punctuation / capitalization):\n\n"
                                        f"{normalized_captured_print_statements}\n\n"),
                        test_case=test_case,
                        display_inputs=True,
                        display_printed_messages=True,
                        display_invalid_printed_messages=True
                    )
            # assert raises an AssertionError, but I don't want to actually catch it
            # this is just so I can have another Exception catch below it in case
            # anything else goes wrong.
            except AssertionError:
                raise
            
            except Exception as e:
                # Handle other exceptions
                exception_message_for_students(e, test_case)
    
    # the first AssertionError raises the problem here, this raises it to the main level so the test will stop
    except AssertionError:
        raise

    except Exception as outer_e:
        # Catches any problem in grabbing the test cases
        test_case = {"id_test_case": None}
        exception_message_for_students(outer_e, test_case=test_case) 