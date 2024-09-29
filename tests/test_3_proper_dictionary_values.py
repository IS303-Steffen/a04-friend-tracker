max_score = 45 # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module, format_error_message

# checks if a correct dictionary is created given certain inputs

def test_3_proper_dictionary_values(mock_inputs, test_cases):
    for test_case in test_cases:
        if test_case["id_test_case"] in [3]:
            continue
        inputs = test_case["inputs"]
        # this provides a dictionary of dictionaries. Each key is a variable name,
        # the value is the actual dicitonary we care about.
        expected_dictionaries = test_case["dicts"].values()
        
        # Load in the student's code (which runs anything at a global level)
        # By passing in mock_inputs, the student's input() function will be
        # replaced by a mock version that will auto insert the inputs for the 
        # test case

        _, student_globals = load_or_reload_module(mock_inputs, inputs)
        
        # Find all variables in student's code that are of type dictionary
        student_dictionaries = {name: value for name, value in student_globals.items() if isinstance(value, dict) and name != "__builtins__"}
        
        # if there isn't even a dictionary, fail the test now
        
        # Assert that there is at least one dictionary
        assert student_dictionaries, (
            "No dictionaries found in your code.")
        
        dictionary_match_found = False
        student_dictionaries_string = '' # used to provide details if the test fails

        # Iterate over all dictionaries found in the student's code
        for dict_name, student_dict in student_dictionaries.items():
            # string is useful for error reporting if test fails
            normalized_student_dict = {normalize_text(key): normalize_text(value) for key, value in student_dict.items()}

            student_dictionaries_string += f"{dict_name}: {normalized_student_dict}\n\n"
            
            # Check if student_dict matches any of the expected dictionaries
            for expected_dictionary in expected_dictionaries:
                if expected_dictionary is not None:
                    # Normalize keys and values in both dictionaries for comparison
                    normalized_expected_dict = {normalize_text(key): normalize_text(value) for key, value in expected_dictionary.items()}
                    
                    if all(key in normalized_student_dict and normalized_student_dict[key] == value for key, value in normalized_expected_dict.items()) and \
                       all(key in normalized_expected_dict and normalized_expected_dict[key] == value for key, value in normalized_student_dict.items()):
                        dictionary_match_found = True
                        break  # Stop once we find a matching dictionary
            if dictionary_match_found:
                break

        assert dictionary_match_found, format_error_message(
            (
            f"None of the dictionaries found in your code "
            f"matched any of the expected values for dictionaries in this test case. "
            f"The expected values (ignoring capitalization / punctuation) are:\n\n"
            f"{normalized_expected_dict}\n\n"
            f"Your dictionary/dictionaries (ignoring capitalization / punctuation) look like this:\n\n"
            f"{student_dictionaries_string}"
            f"Make sure you are correctly adding values to your dictionary, or "
            f"that you aren't transforming the inputs in an unexpected way\n"),
            test_case=test_case,
            display_inputs=True
            )