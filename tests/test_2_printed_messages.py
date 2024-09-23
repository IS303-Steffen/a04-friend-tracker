from conftest import normalize_text, load_or_reload_module

# checks if the expected printed messages actually appear, but doesn't check for specific
# inputs or correct calculations.

def test_2_printed_messages(capsys, mock_inputs):
    
    # Manually set the inputs for the test
    inputs = ["Amit", "Patel", "6", "7", "140"]
    
    # Call the fixture to mock input() with the desired inputs
    _ = mock_inputs(inputs)

    # Load the module (if it is the first test run) or reload it into memory to reset global functions.
    load_or_reload_module()

    # Capture the output from the print statements
    captured = capsys.readouterr().out

    # This will return a list of strings, each representing a line of the captured output
    # this just makes it easier to read the output if the test goes wrong.
    captured_lines = captured.splitlines()  

    # Normalize the captured output to remove spaces, punctuation, and symbols
    normalized_captured_print_statements = [normalize_text(captured_print) for captured_print in captured_lines]
    normalized_captured_print_statements = '\n'.join(normalized_captured_print_statements)


    # Expected phrases in the print output
    expected_printed_statements = ["has a BMI of", "The associated category is"]

    # Check that each required phrase is found in the normalized captured output
    for expected_phrase in expected_printed_statements:
        expected_phrase = normalize_text(expected_phrase)  # Ensure the expected phrase is normalized as well
        assert expected_phrase in normalized_captured_print_statements, (
            f"\nExpected phrase:\n\n\t'{expected_phrase}'"
            f"\n\nwasn't printed out."
            f"\n\nBelow are all printed statements from your code, ignoring punctuation and capitalization."
            f"\nMake sure to double check your spelling:" 
            f"\n\n{normalized_captured_print_statements}\n\n"
        )