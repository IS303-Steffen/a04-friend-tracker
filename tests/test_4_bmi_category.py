from conftest import normalize_text, load_or_reload_module

# checks if correct outputs are calculated from the inputs and bmi category
# inputs are gathered from the inputs_and_expected_outputs fixture in conftest.py

def test_4_bmi_category(capsys, mock_inputs, inputs_and_expected_outputs):
    for test_case in inputs_and_expected_outputs:
        test_input = test_case[0] # this returns a tuple of inputs
        expected_output = test_case[1][1] # this grabs the BMI category
        expected_output = normalize_text(expected_output)

        # Call the fixture to mock_input() with the desired inputs
        _ = mock_inputs(test_input)

        # this just puts all inputs into a concatenated string for
        # easy display of errors
        test_input_concatenated = '\n'.join(test_input)

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


        assert expected_output[0] in normalized_captured_print_statements, (
            f"\nGiven these inputs: \n\n{test_input_concatenated}"
            f"\n\nThe text expects this BMI category:"
            f"\n\t{expected_output}"
            f"\nbut the test couldn't find that value."
            f"\n\nBelow is all your printed output, ignoring punctuation and capitalization."
            f"\nDouble check your output and how you are calculating the cateogry of BMI:" 
            f"\n\n{normalized_captured_print_statements}\n\n"
        )